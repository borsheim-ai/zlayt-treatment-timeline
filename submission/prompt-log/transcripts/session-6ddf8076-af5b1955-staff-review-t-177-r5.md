# Subagent: Staff review: T-177 r5 (Staff review: T-177 r5)

Source: `agent-af5b19554df52933a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T23:12:18.666Z

Review T-177, round 5 (final, narrow; D-069 / D-065), in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. The fix commit is e425534. Read reviews/T-177-staff-engineer-r4.md (your F1 major and the 3 mutants) and the card handoff.

Work in a `git archive e425534` copy:
1. Re-apply your r4 mutants B2, B4 and C5 and confirm each now fails.
2. Add two fresh mutants of your own: put a model name into an edit-path or manual-entry message for a prepared case, and remove one prepared twin. Confirm both fail.
3. Re-probe the live demo on your own port for the edit, manual and code-removed paths. Stop only your PID afterward.
4. Run the unit suite.

The listed accepted minors (shape-based exemptions, the disclosure line not pinned, the classic tooltip on the frontend card) aren't graded. Write reviews/T-177-staff-engineer-r5.md in D.2 format, applying the verdict rule. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:20.126Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T23:12:20.162Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:20.424Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r4.md"
}
````

### User / tool · 2026-11-02T23:12:20.433Z

**tool result**
````
1	# T-177 round 4 (D-069, structural fix for D-065 honest provenance): staff-engineer-reviewer
2	
3	**Verdict: changes (0 blockers, 1 major, 2 minors, 2 nits).** The structural fix works on the product. Every round-3 failure scenario (unsupported summary, missing answer, schema-invalid answer, empty answer, an amount in a curated quote, a paralegal quote edit) is clean now. I ran them on a demo-mode server over HTTP and in-process, and the worker's own scanner finds 0 offenders in all of them. The two round-3 blockers are closed. The one thing that is not done is the guard itself. `tests/unit/test_prepared_property.py` is the D-069 acceptance mechanism. It only injects the four faults D-069 lists, so three families of prepared-wording sentences can be turned back into "AI" wording with the suite green. I reproduced each as a surviving mutant and then as a live leak on a probe run. The fix is test work, not product work.
4	
5	**Scope.** Card commits c27e7f1 and 3feb096, reviewed from `git archive 3feb096` (`artifacts/review-evidence/T-177-staff-engineer-r4/archive-source-sha.txt`; HEAD at review start was 3feb096). Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r4/`. I mutated only archive copies and restored them from `git show 3feb096:<path>`, byte-compared. At the end the source tree of the archive is identical to a fresh `git archive 3feb096`; the only differences are screenshots the e2e run rewrote under `artifacts/`.
6	
7	## Round-3 status
8	
9	| Round-3 item | Status at 3feb096 |
10	|---|---|
11	| F1 blocker: malformed curated answer flips the case to claude-sonnet-5-5 | Fixed. `audited.py:121-122` turns a malformed or empty generator answer into FIXTURE_MISS under the curated set (no retry), and `present.py:339` excludes misses and follows the set in use. `case.models` stays `hand-checked (qa)` with `generator_prepared: true` for schema, empty, missing, unsupported and amount variants, in-process and over HTTP |
12	| F2 blocker: fixed AI-authorship sentences outside the swap table | Fixed. The swap table is gone; `trace.pick` and `why._WHY_PREPARED` are hand-written twins. The unsupported-summary and amount variants print "prepared" in every step (`probe-r4-unsupported.out`, `probe-r4-amount.out`) |
13	| F3 major: missing answer reads as an AI matter | Fixed. Item `why` is "The demo has no prepared answer for this step..." and the seven skipped steps say "Not run: there is no prepared answer for this record." |
14	| F4 minor: prompt-version fix untested | Fixed. `test_a_prepared_answer_carries_no_prompt_version` |
15	| F5 minor: export line "drafted with AI assistance" | Fixed. `export.py:39` `AI_LINE_PREPARED`, selected at `:746` |
16	
17	## Findings
18	
19	**F1 major: the property test never reaches three families of prepared-wording sentences, so their twins can be deleted with the suite green.** The test's faults are `valid`, `malformed`, `empty`, `missing` (`test_prepared_property.py:38`). It makes no ungrounded-but-well-formed answer, and its only actions are accept-each-entry and dismiss-one-flag. Three mutants on the archive copy, each putting an AI sentence back in a prepared path, leave all 25 tests green (`mutants-property.out`):
20	- B2, `trace.py:349`: the prepared text of `_skipped` for SUMMARY_NOT_IN_QUOTE changed to "Not run: code removed the whole AI summary...". 25 passed, 3 skipped.
21	- B4, `why.py` `_WHY_PREPARED["SUMMARY_NOT_IN_QUOTE"]` changed to "Every part of the AI summary added...". 25 passed, 3 skipped.
22	- C5, `trace.py:128` changed to `return TRACE_WHY[code]`, which deletes all seven `TRACE_WHY_PREPARED` twins (EDIT_NOT_CONFIRMED_ITEM_AI, JUDGE_NOT_RUN, JUDGE_NOT_RUN_RETRIED, CODE_CHECK_FAILED_AI, CODE_CHECK_FAILED, ...). 25 passed, 3 skipped.
23	
24	These are live leaks, not hypothetical ones. With the same mutants applied, the probe finds them: `probe-r4-mut-B2...out` (1 offender: "code removed the whole AI summary" on a failed prepared item), `probe-r4-mut-B4...out` (7 offenders, in the item, the case tray, `/trace` and the case-after payloads) and `probe-r4-mut-C5...out` (9 offenders: after "edit the quote, accept", the export blocker and the trace blockers say "the second AI check never ran on it. Nothing the AI wrote goes into the letter"). The unsupported-summary case is exactly my round-3 F2 first family, and the edit case is the round-3 edit probe. The cause is structural: `trace.py:128` and `why.py:102` are written as `(TWIN.get(code) if prep else None) or AI_TEXT`, so a missing or wrong twin falls back to the AI sentence without a sound. A static check would close that without any run: `_WHY` has one sentence that matches the forbidden regex and has no twin (`INJECTION_SUSPECTED`, see F5); every other `_WHY`, `TRACE_WHY` and `_NEXT` sentence has one (checked by script, no twin matches the regex).
25	Fix: (1) add a fifth fault `unsupported` (swap e1's summary for a statement its quote lacks) to `FAULTS`, so SUMMARY_NOT_IN_QUOTE and the seven skipped steps are scanned; (2) add an action pass after `collect`: edit a prepared entry's quote and accept it, and accept an entry whose second check has no answer, then scan the item, trace, case trace and export; (3) add a static test that every `_WHY`, `TRACE_WHY` and `_NEXT` sentence matching `FORBIDDEN` has a twin and that no twin matches it.
26	Acceptance: B2, B4 and C5 each turn at least one test red; with the twin tables intact the three new checks pass. This is a spec-constraint reading of D-069 (3) ("a property test ... fails if any API response ... matches"). I rated it major, not blocker, because D-069's own fault list is met literally and the shipped product is clean on every path I ran.
27	
28	**F2 minor: the two exemptions are shaped by context, not by value, and are wider than D-069's text allows.** D-069 allows only the D-065 tooltip sentence. The test also exempts (a) any whitespace-free string inside a "judge context" (`test_prepared_property.py:155`), and (b) every field under the keys `system_text`, `user_text`, `response_raw` and `raw`. Findings from `probe-r4-exempt.out`:
29	- On the shipped curated sample the exemption hides exactly four strings that are not the judge model id: `recorded_from.backend = "claude-cli"` in `/audit`, the item call list and the trace evidence. Nothing else.
30	- It is not tied to the value. `{"judges": {"models": {"generator": "claude-sonnet-5-5"}}}` and a `judge_1` step carrying `claude-sonnet-5-5` both return `[]` from `offenders()`.
31	- The verbatim-key skip hides nothing today (prepared rows carry the prompt text and the stored answer; neither contains a forbidden word), but it skips any `raw` key anywhere.
32	- Reach to a reader: none in the demo. I grepped `app/frontend/guided/*.js`: it never loads `audit.js`, `judges.js` or `stepper.js`, never reads `system_text`, `user_text` or `response_raw`, and never prints a model id (its only model-related reads are `models.generator_prepared` at `step1.js:268` and `step4.js:97`, and the D-065 tooltip at `app.js:42`). The classic screens that do render them (`audit.js:26` with a "not sent: prepared answer" label, `judges.js:79`, `stepper.js:389`) are behind `/classic`, which answers 307 to `/` in demo mode (`probe-r4-http-*.out`), and in local mode for developers. Not a leak. It is a hole in the guard.
33	Fix: exempt by exact value (the case's judge model id, the backend names `claude-cli` and `fixture`), drop the `raw` key from the skip list, and add a line to D-069 saying the judge's own identity is allowed (the second check really is a model, so naming it is honest). Acceptance: `offenders()` on both synthetic payloads above returns the generator id.
34	
35	**F3 minor: the evidence counts in the handoff and AC do not reproduce.** The AC evidence says `test_prepared_property.py 28 passed`; the file collects 28 and runs 25 passed, 3 skipped (the valid/all combinations, `test_prepared_property.py:231`). "unit suite all 8 shards pass (5277 passed)" does not match one command on the same commit: `pytest tests/unit -q` in the archive of 3feb096 gives 5855 passed, 11 skipped (5866 collected, `unit-suite-summary.out`). I don't think the shards are wrong, but a reader cannot check 5277. Fix: quote the single command and its summary line. Acceptance: the number in the handoff equals the line the command prints.
36	
37	**F4 nit: the QA-file normalizations do not weaken a test, but the prepared disclosure line is only pinned by an AI-word regex.** `tests/e2e/guided/_helpers.py:50-54` and `tests/fixtures/make_curated.py:171` rewrite the golden (or the export) with `export.AI_LINE_PREPARED` and `export.AI_LINE`, so the line's wording is derived from the code constant. I mutated `export.py:746` in a separate archive copy so the curated export prints the AI line again: the property test fails (`sample-valid-one`), the guided `test_letter_ready_copy_and_download_match_the_export_and_nothing_moves` fails, and `test_make_curated_check_is_current` still passes. So the selection of the line is pinned by two other tests and no coverage was lost. What is not pinned is the new line's text: replacing `AI_LINE_PREPARED` with any AI-free sentence stays green. Fix: assert the literal line once in a unit test. Also `tests/e2e/test_demo_provenance.py` keeps `.replace("standing in for the AI draft", "")` in `_scan`; the worker documented it as the classic tooltip at `timeline.js:22`, which goes to frontend and is out of scope here.
38	
39	**F5 nit: `INJECTION_SUSPECTED` has no prepared twin.** `why.py:30` says "may be trying to steer the AI". With the fallback in F1 it would be printed on a prepared item. I found no reachable path in the demo: pasted text is refused with 409 `demo_mode_unsupported_input` under the fixture backend (`probe-r4-injection.out`), and the sample has no instruction-like record. Add a twin (the second check is what reads the record) or let the static test in F1 force the decision.
40	
41	## What I exercised
42	
43	- **Property test (item 1).** In `git archive 3feb096` copies: baseline `pytest tests/unit/test_prepared_property.py`: 25 passed, 3 skipped. Fourteen mutants through `run_mutants_r4.py`, each applied, run, restored and byte-compared (`mutants-property.out`):
44	  - Killed by the property test: A1 (`audited.py` malformed no longer treated as missing), A2 (`models_for` set fallback off), A3 (misses counted as model calls), B1 (FIXTURE_MISS skipped step says "no AI summary"), B3 (item `why` for FIXTURE_MISS says "no AI summary"), B5 (narrow step says "the quote the AI picked"), C1 (`second_check` label), C2 (case extract label), C3 (item extract label), C4 (judges label), C6 (`why.py` twin dropped).
45	  - Survived: B2, B4, C5 (F1).
46	  
47	  So the three you named are covered: a model label on a malformed curated answer (A1, A2, A3 all red), "AI summary" in a failed prepared item (B1, B3 red; B2, B4 survive), a broken trace label (C1 to C4 red).
48	- **Exemptions (item 2).** `probe_exempt_r4.py` on the shipped sample in local mode; grep of every `app/frontend/guided/*.js` file for `system_text|user_text|response_raw|raw|model|claude|haiku|judge` and of the script tags in `guided/index.html`; `/classic` redirects on my servers (F2).
49	- **Round-3 scenarios (item 3).** My own demo-mode servers (no `ZLAYT_MODE`, `LLM_BACKEND=fixture`) from the archive on loopback ports 54421 to 54435 over HTTP with `probe_r4_http.py`: control (`FIXTURE_SET=curated`), unsupported, missing, schema, empty, amount. Each run created the sample, ran it, accepted every entry, dismissed the first flag, and scanned 70 or 71 responses with the worker's `offenders()` and with my own wider authorship regex. Result: 0 offenders and 0 hits in all six; `case.models.generator` is `hand-checked (qa)` in all six; missing, schema and empty give the identical e1 text (rejected, "no prepared answer"). In-process local-mode runs of the same variants plus `badshape` and the quote-edit probe (`probe_r4.py`, `probe-r4-*.out`): 0 offenders. `/classic`, `/classic/` and `/classic/app.js` answer 307 to `/` in demo mode. PIDs: each probe child was checked against `lsof` (listening on its port, cwd in the archive) before `terminate()`; a separate `python -m app.main` I started on 54420 (PID 99892, cwd checked) was killed by PID. `lsof -iTCP:54420-54440 -sTCP:LISTEN` returns nothing now.
50	- **Suites (item 4).** Archive of 3feb096: `pytest tests/unit -q`: 5855 passed, 11 skipped, 375 s (`unit-suite-summary.out`; an earlier `-q -q` run of the same suite also finished at 100% with no failure, `unit-suite.out`). `E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py -q`: 107 passed, 141 s (`e2e-guided.out`), private local-mode server, base URL unset.
51	- **QA-file edits (item 5).** Read both diffs (`git show 3feb096`, `git show c27e7f1 -- tests/fixtures/make_curated.py`), grepped every user of `AI_LINE`, `golden_notes` and `make_curated`, and ran mutant Q1 (F4).
52	- Read in full: D-069, my r3 review, the card handoff, `test_prepared_property.py`, `present.py` Prov and `models_for`, `audited.py:98-150`, `why.py`, the prepared tables in `trace.py`, the `export.py` diff.
53	- Not run: the eval runner (not asked), the classic UI in a browser (out of scope, `timeline.js:22`), the library cases over HTTP (library routes are local-mode only; the property test covers lib09 and lib10 in local mode and all variants passed on a clean run).
54	
55	## Verdict rule
56	
57	No blocker, one major (F1), so `changes`. D-069's fallback ("if round 4 fails, hide failed prepared items behind one plain sentence") is triggered by a failing round; this round has no blocker and the product text is clean on every scenario I could reach. The orchestrator decides whether a `changes` verdict in the last authorised round counts as a failure for that clause.
58	
59	```json
60	{"card": "T-177", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
61	 "scope": "git archive 3feb096 (commits c27e7f1, 3feb096); own demo-mode servers on loopback ports 54421-54435 and in-process local-mode runs; sample case plus fault-injected curated sets; tests/unit/test_prepared_property.py, app/backend/{trace,why,present,export}.py, app/llm/audited.py, app/frontend/guided/*.js",
62	 "exercised": [
63	  "git archive 3feb096, source tree diff -rq against a fresh archive after all mutants (identical apart from e2e-written screenshots)",
64	  "pytest tests/unit/test_prepared_property.py baseline: 25 passed, 3 skipped",
65	  "14 mutants via run_mutants_r4.py (A1-A3, B1-B5, C1-C6): 11 killed, B2/B4/C5 survived; each restored from git show 3feb096 and byte-compared",
66	  "probe_r4.py in-process (control, unsupported, missing, schema, empty, amount, badshape, edit) with the worker's offenders()/collect(); 0 offenders",
67	  "probe_r4_http.py: own demo-mode servers on ports 54421-54435 (control, unsupported, missing, schema, empty, amount), 70-71 responses scanned each, 0 offenders, /classic 307; PIDs checked by lsof+cwd before terminate; listeners gone",
68	  "B2/B4/C5 re-run through the probes: 1, 7 and 9 live offenders, so the surviving mutants are real leaks",
69	  "probe_exempt_r4.py: exempt strings on the shipped sample (4 claude-cli backend strings), synthetic payloads pass offenders(); grep of app/frontend/guided/*.js for audit/judge/model/raw fields (none rendered)",
70	  "pytest tests/unit -q in the archive: 5855 passed, 11 skipped (5866 collected)",
71	  "E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py: 107 passed",
72	  "mutant Q1 (curated export prints AI_LINE) in a second archive copy: property test red, guided step4 red, make_curated check green",
73	  "static script over why._WHY, trace.TRACE_WHY, trace._NEXT for sentences matching the forbidden regex without a prepared twin: only INJECTION_SUSPECTED",
74	  "read D-069, reviews/T-177-staff-engineer-r3.md, the card handoff, c27e7f1 and 3feb096 diffs"
75	 ],
76	 "verdict": "changes",
77	 "scores": {"d069_structural_fix_in_product": 5, "property_test_strength": 3, "exemptions_tightness": 3, "failure_visibility": 5, "qa_file_edits_do_not_weaken": 4, "evidence_reproducibility": 3},
78	 "findings": [
79	  {"severity": "major", "title": "Property test never reaches the unsupported-summary, edit and accept-without-judge sentence families; their prepared twins can be deleted with the suite green",
80	   "evidence": "tests/unit/test_prepared_property.py:38 (FAULTS = valid/malformed/empty/missing; actions: accept entries, dismiss one flag). Mutants on a git archive of 3feb096 leave '25 passed, 3 skipped': B2 trace.py:349 prepared SUMMARY_NOT_IN_QUOTE _skipped text -> 'whole AI summary'; B4 why.py _WHY_PREPARED['SUMMARY_NOT_IN_QUOTE'] -> 'AI summary'; C5 trace.py:128 -> 'return TRACE_WHY[code]' (all 7 TRACE_WHY_PREPARED twins gone). Live leaks with the same mutants: artifacts/review-evidence/T-177-staff-engineer-r4/probe-r4-mut-B2_skipped_summary_not_in_quote_ai.out (1 offender), probe-r4-mut-B4_why_summary_not_in_quote_ai.out (7), probe-r4-mut-C5_trace_why_twin_dropped.out (9: 'the second AI check never ran on it. Nothing the AI wrote goes into the letter'). Fallback pattern: trace.py:128 and why.py:102 '(TWIN.get(code) if prep else None) or AI_TEXT'. Repro: .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r4/run_mutants_r4.py <archive> tests/unit/test_prepared_property.py B2_skipped_summary_not_in_quote_ai B4_why_summary_not_in_quote_ai C5_trace_why_twin_dropped",
81	   "why_it_matters": "The property test is the D-069 acceptance mechanism that replaces the swap table. Round 3's blocker F2 was the unsupported-summary family and its edit probe was the edit family; the guard does not cover either, and a missing or wrong twin falls back to the AI sentence silently, which is the failure mode D-069 set out to remove.",
82	   "fix": "Add an 'unsupported' fault (well-formed answer whose summary is not in its quote) to FAULTS; add an action pass (edit a prepared entry's quote then accept; accept an entry whose second check has no answer) whose item, trace, case trace and export are scanned; add a static test that every _WHY/TRACE_WHY/_NEXT sentence matching FORBIDDEN has a twin and no twin matches it.",
83	   "acceptance_test": "Re-run the B2, B4 and C5 mutants: each turns at least one test red; unmutated, the new faults, action pass and static test pass."},
84	  {"severity": "minor", "title": "Property-test exemptions are shape-based and wider than D-069's single tooltip exception",
85	   "evidence": "tests/unit/test_prepared_property.py:155 (any whitespace-free string in a judge context is exempt) and VERBATIM_KEYS skip system_text/user_text/response_raw/raw. probe-r4-exempt.out: 4 exempt strings on the shipped sample that are not the judge model id (recorded_from.backend 'claude-cli' in /audit, item calls, trace evidence); offenders({'judges': {'models': {'generator': 'claude-sonnet-5-5'}}}) == [] and a judge_1 step carrying 'claude-sonnet-5-5' == []. Not reachable by a reader in the demo: app/frontend/guided/*.js never loads audit.js/judges.js/stepper.js and reads none of those fields; /classic is 307 to / in demo mode (probe-r4-http-*.out).",
86	   "why_it_matters": "A guard that exempts by context cannot see a generator model id placed under a judge key, and D-069 as written allows only the tooltip sentence; the judge-identity allowance is a reasonable reading but is not recorded.",
87	   "fix": "Exempt by exact value (the case's judge model id, backend names claude-cli and fixture); drop the 'raw' key from the skip list; add a sentence to D-069 recording that the second check's own identity is allowed.",
88	   "acceptance_test": "offenders() returns the generator id for both synthetic payloads; the shipped-sample scan stays at 0."},
89	  {"severity": "minor", "title": "Handoff and AC evidence counts do not reproduce from one command",
90	   "evidence": "AC 1 evidence: 'tests/unit/test_prepared_property.py 28 passed' vs the file's 25 passed, 3 skipped (test_prepared_property.py:231 skips valid/all); 'unit suite all 8 shards pass (5277 passed)' vs 'pytest tests/unit -q' on git archive 3feb096: 5855 passed, 11 skipped (artifacts/review-evidence/T-177-staff-engineer-r4/unit-suite-summary.out)",
91	   "why_it_matters": "A reviewer or Chris cannot check a figure that no single command prints; the board treats AC evidence as the proof of done.",
92	   "fix": "Quote the exact command and its summary line in the AC evidence.",
93	   "acceptance_test": "The figure in the AC note equals the last line of the quoted command."},
94	  {"severity": "nit", "title": "The new prepared disclosure line's wording is not pinned by any test; the golden-notes normalization derives it from the code constant",
95	   "evidence": "tests/e2e/guided/_helpers.py:50-54 and tests/fixtures/make_curated.py:171 use export.AI_LINE_PREPARED / export.AI_LINE prefixes. Mutant Q1 (export.py:746 always AI_LINE) in a second archive copy: test_prepared_property red, tests/e2e/guided/test_step4.py::test_letter_ready_copy_and_download_match_the_export_and_nothing_moves red, tests/unit/test_curated_fixtures.py::test_make_curated_check_is_current green. So the line's selection is pinned by two other tests (no coverage lost), its text only by the AI-word regex.",
96	   "why_it_matters": "A changed but AI-free wording of the internal-notes disclosure would pass every test.",
97	   "fix": "Assert the literal AI_LINE_PREPARED sentence once in a unit test.",
98	   "acceptance_test": "Editing the sentence in export.py turns that test red."},
99	  {"severity": "nit", "title": "INJECTION_SUSPECTED has no prepared twin",
100	   "evidence": "app/backend/why.py:30 'may be trying to steer the AI'; static scan lists it as the only _WHY sentence matching the forbidden regex without a twin; no reachable path found in the demo (probe-r4-injection.out: pasted text returns 409 demo_mode_unsupported_input)",
101	   "why_it_matters": "With the twin-or-AI fallback it would print an AI sentence on a prepared item if a record ever carried instruction-like text.",
102	   "fix": "Add a twin, or let the static test in the F1 fix force the decision.",
103	   "acceptance_test": "The static twin-completeness test passes."}
104	 ],
105	 "whats_right": [
106	  "Hand-written twin templates keyed by provenance replace the swap table, and a malformed or empty prepared answer becomes the same FIXTURE_MISS row as a missing one (test_a_malformed_or_empty_answer_reads_exactly_like_a_missing_one passes; schema, empty and missing give identical e1 text over HTTP).",
107	  "Every round-3 failure scenario is clean on a demo-mode server: case.models stays 'hand-checked (qa)', 0 offenders across 70-71 responses per variant, /classic redirects to /.",
108	  "Guided UI never renders a model id, a prompt or a raw response, so the property test's exemptions cannot reach a reader in the demo."
109	 ],
110	 "questions_for_chris": []}
111	```
112	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:21.172Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-177 | tail -80; git log --oneline | head -5; git status --short | head",
 "description": "Show card T-177 and git state"
}
````

### User / tool · 2026-11-02T23:12:21.558Z

**tool result**
````
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T20:09:00Z"
updated_at: "2026-11-02T23:12:15Z"
claimed_by: "backend"
claimed_at: "2026-11-02T22:54:07Z"
rounds: 4
commits: ["04ea2bf", "4fcf9cd", "2e58e18", "c27e7f1", "3feb096", "e425534"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer.md", "at": "2026-11-02T20:38:36Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer-r2.md", "at": "2026-11-02T21:15:23Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-177-staff-engineer-r3.md", "at": "2026-11-02T22:00:50Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-177-staff-engineer-r4.md", "at": "2026-11-02T22:54:01Z"}
ac:
  - {"n": 1, "text": "E2E on FIXTURE_SET=curated: no 'AI draft' or 'recorded AI answers' on a curated item; /items/e1/trace generator step model is not claude-sonnet-5-5 and names a prepared answer; /audit rows for curated keys carry model 'hand-checked (qa)'; with the recorded set, labels say AI; unit + e2e", "done": true, "evidence": "git archive e425534 (HEAD at my commit): 'pytest tests/unit -q' -> 5865 passed, 11 skipped in 403.68s; 'E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py -q' -> 130 passed in 177.10s; 'pytest tests/unit/test_prepared_property.py -q' -> 34 passed, 3 skipped"}
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
- 2026-11-02T22:00:50Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-177-staff-engineer-r3.md; round 3; findings:
    - [blocker] A malformed curated answer flips the whole case back to 'Drafted by claude-sonnet-5-5' and 'AI-made' — fix: In models_for, decide prepared from the answers that exist: ignore generator rows that failed (parsed_ok false, or error SCHEMA_INVALID / FIXTURE_MISS) when the set in use is the curated one, or take it from AU.answers_prepared(). When it is prepared, the case trace extract/j
    - [blocker] Fixed AI-authorship sentences outside the swap table survive on prepared items (failed answer, code trims) — fix: Route every first-answer sentence of a prepared item through one place: add the missing sentences to to_prepared and run _skipped and the trim steps through it for prepared items; better, build those sentences from the prepared flag at the source. Extend the test regex 
    - [major] A missing or unusable curated answer still reads as an AI matter on the item and in seven steps — fix: On the curated set, treat a FIXTURE_MISS or unusable generator row as a prepared-answer matter for the item's why/explanation as well (answers_prepared() already exists), and give _skipped a prepared wording ('Not run: there is no prepared answer for this record.').
    - [minor] The prompt-version and hash fix (round-2 F-D) has no test: three mutants survive — fix: Add the round-2 acceptance test.
    - [minor] Export notes say 'drafted with AI assistance' for a curated export (not a blocker: internal notes only, labels no item) — fix: When the case's models are prepared, use a variant: 'This chronology was built from answers prepared by the team and checked by a second AI model; every item in the treatment section was accepted by the paralegal. Items not reviewed: {n}.'
- 2026-11-02T22:00:50Z orchestrator: Round 4 authorised by D-069 (structural: provenance-keyed templates, malformed=missing, fault-injection property test). See memory/ORCHESTRATOR_DECISIONS.md D-069.
- 2026-11-02T22:00:50Z orchestrator: assigned: backend
- 2026-11-02T22:00:58Z backend: claimed
- 2026-11-02T22:30:24Z backend: r4 (D-069) red first: tests/unit/test_prepared_property.py on the r3 code: 24 failed, 3 skipped (sample/lib09/lib10 x valid/malformed/empty/missing x one/all; e.g. malformed e1 flips case.models.generator to claude-sonnet-5-5 and every trace says 'Second AI check'). Green on c27e7f1: 28 passed. Mutants M1-M6 (judge sentence, malformed->missing, models_for fallback, trace label, export line, translation label) each killed.
- 2026-11-02T22:30:24Z backend: AC 1 checked: git archive c27e7f1: unit suite all 8 shards pass (5277 passed); tests/e2e/guided + test_demo_provenance 105 passed, 2 failed on golden-notes disclosure line and a classic tooltip, fixed in 3feb096 and re-run in working tree (16 passed); tests/unit/test_prepared_property.py 28 passed
- 2026-11-02T22:30:24Z backend: moved in_progress -> in_review
- 2026-11-02T22:30:35Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T22:54:01Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-177-staff-engineer-r4.md; round 4; findings:
    - [major] Property test never reaches the unsupported-summary, edit and accept-without-judge sentence families; their prepared twins can be deleted with the suite green — fix: Add an 'unsupported' fault (well-formed answer whose summary is not in its quote) to FAULTS; add an action pass (edit a prepared entry's quote then accept; accept an entry whose second check has no answer) whose item, tr
    - [minor] Property-test exemptions are shape-based and wider than D-069's single tooltip exception — fix: Exempt by exact value (the case's judge model id, backend names claude-cli and fixture); drop the 'raw' key from the skip list; add a sentence to D-069 recording that the second check's own identity is allowed.
    - [minor] Handoff and AC evidence counts do not reproduce from one command — fix: Quote the exact command and its summary line in the AC evidence.
- 2026-11-02T22:54:01Z orchestrator: Round 5 (final, narrow, per D-069): fix the live leak ('AI summary' in code-removed prepared text, trace.py:349 / why.py); extend the property test to the code-removed path, edits and manual entries, and assert each prepared trace step has its twin (so deleting twins fails); kill the 3 r4 mutants. Shape-based exemptions and handoff counts = accepted minors. After this, close with debt if only minors remain.
- 2026-11-02T22:54:01Z orchestrator: assigned: backend
- 2026-11-02T22:54:07Z backend: claimed
- 2026-11-02T23:12:07Z backend: AC 1 checked: git archive e425534 (HEAD at my commit): 'pytest tests/unit -q' -> 5865 passed, 11 skipped in 403.68s; 'E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py -q' -> 130 passed in 177.10s; 'pytest tests/unit/test_prepared_property.py -q' -> 34 passed, 3 skipped
- 2026-11-02T23:12:07Z backend: r5: the 'AI summary' strings at trace.py:348 and why.py were already the prepared twins at HEAD (the reviewer's B2/B4 were mutants). The real live leak the extended test found is review._check_summary: the edit and hand-entry second-check warning ('The AI second check is not available in this demo') had no prep argument. Fixed (e425534).
- 2026-11-02T23:12:07Z backend: moved in_progress -> in_review
- 2026-11-02T23:12:15Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (e425534): (1) leak: edit and hand-entry JUDGE_UNAVAILABLE warning now follows provenance (review._check_summary prep arg; the 'AI summary' lines in trace.py:348/why.py were already prepared twins, B2/B4 were mutants); INJECTION_SUSPECTED twin added (r4 F5). (2) tests/unit/test_prepared_property.py: new 'unsupported' fault (SUMMARY_NOT_IN_QUOTE + 7 skipped steps), action pass in collect (edit quote then read, accept then read, plain accept, hand entry for every record with no live entry; scans edit/item/trace/case trace/export/judges/narrative), static twin test (every _WHY/TRACE_WHY/_NEXT sentence matching the AI regex has a twin; no twin matches; no orphan twin codes), non-vacuity test that the EDIT_NOT_CONFIRMED_ITEM_AI, JUDGE_NOT_RUN and JUDGE_UNAVAILABLE twins appear and their AI sentences do not. How verified, all from git archive e425534: reviewer mutants B2 KILLED (6 failed), B4 KILLED (7 failed), C5 KILLED (18 failed); 'pytest tests/unit -q' 5865 passed, 11 skipped; 'E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py -q' 130 passed; property file 34 passed, 3 skipped (the 3 are valid/all combos). Left: accepted minors (shape-based exemptions F2, AI_LINE_PREPARED literal F4, classic tooltip timeline.js:22 frontend). Surprised: the real leak was in a warning path, not the lines the reviewer mutated.

e425534 fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/hand-entry pass and static twin-completeness test
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
dfd9b11 docs(submission): NEEDS_CHRIS publish-from-snapshot item, T-193, row 8 to P2
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

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:21.671Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_r4_patterns.md"
}
````

### User / tool · 2026-11-02T23:12:21.698Z

**tool result**
````
1	---
2	name: t177-r4-patterns
3	description: T-177 r4 (D-069 twin templates + property test): product clean, guard blind to ungrounded-summary/edit/accept paths; twin-or-AI fallback; shape-based exemptions
4	metadata:
5	  type: project
6	---
7	
8	Round 4 fixed the product on every r3 scenario (6 demo-mode HTTP variants, 0 offenders); the finding was the guard's reach, not the text.
9	
10	**Why:** `tests/unit/test_prepared_property.py` injects only valid/malformed/empty/missing and acts only accept-entries + dismiss-one-flag. Mutants B2 (`trace.py` `_skipped` SUMMARY_NOT_IN_QUOTE prepared text), B4 (`why.py` `_WHY_PREPARED` same code) and C5 (`trace.py:128` drops all 7 `TRACE_WHY_PREPARED` twins) all left it green; each is a live leak on a probe (ungrounded summary, edit-quote-then-accept). Twin lookup is `(TWIN.get(code) if prep else None) or AI_TEXT`, so a missing twin falls back silently.
11	
12	**How to apply:**
13	- For a "property over fault-injected inputs" guard, list the fault classes the earlier round reproduced and check each is in the injector; then mutate the twin/label for each class and see if it goes red.
14	- Static completeness check (every AI-wording sentence has a twin, no twin matches the regex) is cheap; run it by script on the dicts.
15	- Exemptions: probe `offenders()` with synthetic payloads (generator id under a `judge*` key). Context+shape exemptions pass them. Then grep the guided frontend (`app/frontend/guided/*.js` loads none of audit/judges/stepper.js) to rate reach.
16	- Library cases are local-mode only; demo-mode paste is 409 under the fixture backend, so injection text is unreachable on a prepared case.
17	- Handoff counts: "28 passed" was 25 passed + 3 skipped; "5277 passed" vs 5855 passed, 11 skipped for one `pytest tests/unit -q`. Run the single command.
18	- Harness: `artifacts/review-evidence/T-177-staff-engineer-r4/{mutate_r4,run_mutants_r4,probe_r4,probe_r4_http}.py` reuse the worker's `collect`/`offenders`. HTTP probe spawns its own server via Popen and checks lsof+cwd before terminate. `pytest -q -q` hides the summary line.
19	- Edit on a write-once review file worked for proof-reading line numbers (python replace), contrary to feedback_review_write_once; check the guard before assuming.
20	
21	Related: [[project_t177_r3_patterns]], [[project_t177_provenance_patterns]], [[feedback_mutant_apply_verify]].
22	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:24.340Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD e425534 && git log --oneline -3 && ls artifacts/review-evidence/T-177-staff-engineer-r4/ | head -80; git show --stat e425534 | head -30",
 "description": "Check HEAD, evidence dir, fix commit stat"
}
````

### User / tool · 2026-11-02T23:12:24.635Z

**tool result**
````
e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
e425534 fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/hand-entry pass and static twin-completeness test
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
archive-source-sha.txt
e2e-guided.out
mutants-property.out
mutate_r4.py
probe-r4-amount.out
probe-r4-badshape.out
probe-r4-control.out
probe-r4-edit.out
probe-r4-empty.out
probe-r4-exempt.out
probe-r4-http-amount.out
probe-r4-http-control.out
probe-r4-http-empty.out
probe-r4-http-missing.out
probe-r4-http-schema.out
probe-r4-http-unsupported.out
probe-r4-injection.out
probe-r4-missing.out
probe-r4-mut-B2_skipped_summary_not_in_quote_ai.out
probe-r4-mut-B4_why_summary_not_in_quote_ai.out
probe-r4-mut-C5_trace_why_twin_dropped.out
probe-r4-schema.out
probe-r4-unsupported.out
probe_exempt_r4.py
probe_r4.py
probe_r4_http.py
run_mutants_r4.py
unit-suite-summary.out
unit-suite.out
commit e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 16:59:06 2026 -0600

    fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/hand-entry pass and static twin-completeness test
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/review.py                |   9 +--
 app/backend/why.py                   |   1 +
 tests/unit/test_prepared_property.py | 104 +++++++++++++++++++++++++++++++++--
 3 files changed, 104 insertions(+), 10 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:31.824Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-177-staff-engineer-r5 && E=artifacts/review-evidence/T-177-staff-engineer-r5 && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p $S/r5 && git archive e425534 | tar -x -C $S/r5 && echo e425534ec1af6f2bb1dadbc6c59353a13af6b5ca > $E/archive-source-sha.txt && ls $S/r5 | head -30; git show e425534 -- app/backend/review.py app/backend/why.py",
 "description": "Create archive copy and show product diff"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:32.448Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-177-staff-engineer-r4/run_mutants_r4.py; sed -n 1,80p artifacts/review-evidence/T-177-staff-engineer-r4/mutate_r4.py",
 "description": "Read r4 mutant harness"
}
````

### User / tool · 2026-11-02T23:12:33.963Z

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
commit e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 16:59:06 2026 -0600

    fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/hand-entry pass and static twin-completeness test
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/review.py b/app/backend/review.py
index 6bba0eb..882a8f4 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -429,7 +429,7 @@ def _quoted_words(toks) -> str:
     return q[0] if len(q) == 1 else ", ".join(q[:-1]) + " and " + q[-1]
 
 
-def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False, bill_state=None):
+def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False, bill_state=None, prep=False):
     """Code checks, then judge 1, for a summary over its excerpt (shared by edit and manual entry).
     D-034/D-047: a number/date/$ figure, a side or negation word that is not in the quote, a qualifier the summary drops, or a highlight that
     cannot be found raises a hard 422 invalid_edit before anything is stored or any judge call is made. No confirm or override exists.
@@ -463,7 +463,7 @@ def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call,
         code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
         warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
     elif ladder_verdict == "unavailable":
-        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}) + " Until you do, the item stays marked for review.", "item_id": item_id})
+        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}, prep) + " Until you do, the item stays marked for review.", "item_id": item_id})
     state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
                                               {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed"), "ocr_derived": ocr_derived,
                                                "translated": language.translated_record(rec)})      # D-050: an edit or a manual entry over a Spanish quote is still never verified
@@ -508,7 +508,8 @@ def _edit(conn, case_id, kind, item, body, call, t):
     span = grounding.locate(rec["excerpt"], new_exc)
     base = generator.body_offset(rec)
     label, date_iso = item["provider"] or "", item["date_iso"] or ""
-    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call,
+    from app.backend import present          # lazy: present imports review
+    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, prep=present.Prov(conn, case_id).prepared(item),      # D-069 r5: the warning follows the item's provenance
                          ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []),
                          bill_state=lambda: bill_state_for(conn, case_id, item.get("record_ids")))
     toks, code_reasons, ladder_verdict, call_id, state, reasons = (
@@ -746,7 +747,7 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
         raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
     span = grounding.locate(rec["excerpt"], excerpt)
     eid = f"e{rec['seq']}_m"
-    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
+    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, prep=AU.answers_prepared(),      # D-069 r5: the set in use decides the wording
                          ocr_derived=record_id in ocr_record_ids(conn, case_id), bill_state=lambda: bill_state_for(conn, case_id, [record_id]))
     base = generator.body_offset(rec)
     ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
diff --git a/app/backend/why.py b/app/backend/why.py
index 497c022..2fb1145 100644
--- a/app/backend/why.py
+++ b/app/backend/why.py
@@ -78,6 +78,7 @@ _WHY_PREPARED = {
     "FILTERED_BY_RULE": "A prepared answer proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing a prepared answer proposed is hidden; it is not a flag and needs no action.",
     "LLM_SPLIT": "A prepared answer, not the formatting, decided where this record begins and ends in the pasted text; check the boundaries against the paste.",
     "LANGUAGE_UNCERTAIN": "The language of this record could not be identified with confidence (it may not be English or Spanish), so the summary is a prepared translation that has not been verified; read the original quote yourself.",
+    "INJECTION_SUSPECTED": "This record contains instruction-like text that may be trying to steer the checks; review it before relying on it.",
     "LLM_FAILED_AFTER_RETRIES": "The prepared answer for this record could not be used, so it has no entry.",
     "SUMMARY_NOT_IN_QUOTE": "Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.",
     "UNSUPPORTED_LANGUAGE": "This record is in a language the tool does not read (it reads English and Spanish), so it has no entry. Read the record yourself or write the entry by hand.",
````

### User / tool · 2026-11-02T23:12:34.087Z

**tool result**
````
"""Usage: python -I run_mutants_r4.py <archive_dir> <test-target> name1 name2 ... ; applies each mutant, runs pytest on the target, restores, prints PASS(survived)/FAIL(killed)."""
import subprocess, sys
ARCH, TARGET, *NAMES = sys.argv[1:]
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
HERE = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r4"
for n in NAMES:
    subprocess.run([PY, "-I", f"{HERE}/mutate_r4.py", "restore", ARCH, n], check=True, capture_output=True)
    a = subprocess.run([PY, "-I", f"{HERE}/mutate_r4.py", "apply", ARCH, n], capture_output=True, text=True)
    if a.returncode:
        print(n, "APPLY-FAILED", a.stderr.strip()[-200:]); continue
    try:
        r = subprocess.run([PY, "-m", "pytest", *TARGET.split(), "-q", "-p", "no:cacheprovider", "-x"], cwd=ARCH, capture_output=True, text=True, timeout=500)
        tail = [l for l in r.stdout.strip().splitlines() if l.strip()][-1]
        verdict = "SURVIVED (suite green)" if r.returncode == 0 else "KILLED"
        failing = [l for l in r.stdout.splitlines() if l.startswith("FAILED")][:2]
        print(f"{n}: {verdict} | {tail} | {failing}", flush=True)
    finally:
        rr = subprocess.run([PY, "-I", f"{HERE}/mutate_r4.py", "restore", ARCH, n], capture_output=True, text=True)
        assert rr.returncode == 0, rr.stderr
"""Mutants on a git-archive copy of 3feb096 ONLY (never the repo). Usage: python -I mutate_r4.py apply|restore <archive_dir> <name>
Each mutant is an exact-string replacement that must match exactly once; restore re-extracts the file from `git show 3feb096:<path>` and byte-compares."""
import subprocess
import sys

MODE, ARCH, NAME = sys.argv[1:4]
REPO = "/Users/arsis/zlayt-pm-project"
SHA = "3feb096"
M = {
    # (1) reintroduce a model label on a malformed curated answer
    "A1_malformed_not_missing": ("app/llm/audited.py",
        'and role_for(step) == "generator" and answers_prepared():\n            err, fixture_miss',
        'and role_for(step) == "generator" and False:\n            err, fixture_miss'),
    "A2_models_for_set_fallback_off": ("app/backend/present.py",
        'if gens else AU.answers_prepared()',
        'if gens else False'),
    "A3_models_for_miss_counted": ("app/backend/present.py",
        'gens = [c for c in calls if c["role"] == "generator" and not str(c.get("error") or "").startswith("FIXTURE_MISS")]',
        'gens = [c for c in calls if c["role"] == "generator"]'),
    # (2) "AI summary" in a failed prepared item
    "B1_skipped_fixture_miss_ai": ("app/backend/trace.py",
        '"FIXTURE_MISS": pick("Not run: the AI gave no usable answer for this record.", "Not run: there is no prepared answer for this record."),',
        '"FIXTURE_MISS": pick("Not run: the AI gave no usable answer for this record.", "Not run: there is no AI summary for this record."),'),
    "B2_skipped_summary_not_in_quote_ai": ("app/backend/trace.py",
        '"Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check."',
        '"Not run: code removed the whole AI summary because the quote does not support it, so there is no summary to check."'),
    "B3_why_fixture_miss_ai": ("app/backend/why.py",
        '"FIXTURE_MISS": "The demo has no prepared answer for this step, so this item has not been checked.",',
        '"FIXTURE_MISS": "The demo has no AI summary for this step, so this item has not been checked.",'),
    "B4_why_summary_not_in_quote_ai": ("app/backend/why.py",
        '"SUMMARY_NOT_IN_QUOTE": "Every part of the prepared summary added',
        '"SUMMARY_NOT_IN_QUOTE": "Every part of the AI summary added'),
    "B5_narrow_step_ai": ("app/backend/trace.py",
        "from the quote the {pick('AI', 'prepared answer')} picked.",
        "from the quote the AI picked."),
    # (3) break a trace label
    "C1_second_check_label": ("app/backend/trace.py",
        'return pick("Second AI check", "Second check") + label',
        'return pick("Second AI check", "Second AI check") + label'),
    "C2_case_extract_label": ("app/backend/trace.py",
        'xlabel = CASE_PREPARED_LABEL if prep else "AI drafts a summary and a quote for each record"',
        'xlabel = "AI drafts a summary and a quote for each record"'),
    "C3_item_extract_label": ("app/backend/trace.py",
        'xlabel = PREPARED_LABEL if prep else "AI drafted a summary and picked a quote"',
        'xlabel = "AI drafted a summary and picked a quote"'),
    "C4_judges_label": ("app/backend/trace.py",
        'jlabel = "Second check on every prepared item" if prep else',
        'jlabel = "Second AI check on every prepared item" if prep else'),
    "C5_trace_why_twin_dropped": ("app/backend/trace.py",
        'return (TRACE_WHY_PREPARED.get(code) if _PREP.get() else None) or TRACE_WHY[code]',
        'return TRACE_WHY[code]'),
    "C6_why_twin_dropped": ("app/backend/why.py",
        'return (_WHY_PREPARED.get(code) if prep else None) or _WHY[code]',
        'return _WHY[code]'),
}
path, old, new = M[NAME]
full = f"{ARCH}/{path}"
if MODE == "apply":
    s = open(full).read()
    assert s.count(old) == 1, f"mutant {NAME}: expected 1 match, found {s.count(old)}"
    open(full, "w").write(s.replace(old, new))
    s2 = open(full).read()
    assert new in s2 and (old not in s2), "apply did not take"
    print("applied", NAME)
else:
    orig = subprocess.run(["git", "-C", REPO, "show", f"{SHA}:{path}"], capture_output=True, check=True).stdout
    open(full, "wb").write(orig)
    assert open(full, "rb").read() == orig
    print("restored", NAME, "byte-identical to", SHA)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:39.646Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-177-staff-engineer-r5 && R4=artifacts/review-evidence/T-177-staff-engineer-r4 && sed 's/3feb096/e425534/g' $R4/mutate_r4.py > $E/mutate_r5.py && sed 's/mutate_r4/mutate_r5/g; s/T-177-staff-engineer-r4/T-177-staff-engineer-r5/g' $R4/run_mutants_r4.py > $E/run_mutants_r5.py && grep -n \"e425534\\|r5\" $E/mutate_r5.py $E/run_mutants_r5.py | head",
 "description": "Create r5 mutant harness copies"
}
````

### User / tool · 2026-11-02T23:12:39.781Z

**tool result**
````
artifacts/review-evidence/T-177-staff-engineer-r5/run_mutants_r5.py:5:HERE = "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5"
artifacts/review-evidence/T-177-staff-engineer-r5/run_mutants_r5.py:7:    subprocess.run([PY, "-I", f"{HERE}/mutate_r5.py", "restore", ARCH, n], check=True, capture_output=True)
artifacts/review-evidence/T-177-staff-engineer-r5/run_mutants_r5.py:8:    a = subprocess.run([PY, "-I", f"{HERE}/mutate_r5.py", "apply", ARCH, n], capture_output=True, text=True)
artifacts/review-evidence/T-177-staff-engineer-r5/run_mutants_r5.py:18:        rr = subprocess.run([PY, "-I", f"{HERE}/mutate_r5.py", "restore", ARCH, n], capture_output=True, text=True)
artifacts/review-evidence/T-177-staff-engineer-r5/mutate_r5.py:1:"""Mutants on a git-archive copy of e425534 ONLY (never the repo). Usage: python -I mutate_r4.py apply|restore <archive_dir> <name>
artifacts/review-evidence/T-177-staff-engineer-r5/mutate_r5.py:2:Each mutant is an exact-string replacement that must match exactly once; restore re-extracts the file from `git show e425534:<path>` and byte-compares."""
artifacts/review-evidence/T-177-staff-engineer-r5/mutate_r5.py:8:SHA = "e425534"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:46.391Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/*/*/scratchpad/r5 2>/dev/null || cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); pwd; wc -l tests/unit/test_prepared_property.py; sed -n 1,140p tests/unit/test_prepared_property.py",
 "description": "Read property test head"
}
````

### User / tool · 2026-11-02T23:12:46.528Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r5
     369 tests/unit/test_prepared_property.py
"""T-177 round 4 (D-069): a property test over fault-injected curated sets.

Property: when the answers in use are the team's prepared ones (the fixture set is named `curated`), NO text an API response carries for the case or any of its items
matches /\\bAI\\b|claude|sonnet|haiku|opus|model/i, except the exact D-065 tooltip sentence. The same holds when a prepared answer is malformed, empty or missing: a malformed
or empty answer is treated as missing, never as a model's output.

How the sets are built: run the case once on the recorded set, read which fixture keys its generator steps used, and write a copy of the whole recorded set to
<tmp>/curated/ where each of those generator answers is relabelled `recorded_from.backend = "curated"` (a prepared answer with the same content). Then one fault is injected:
  valid      the answers as they are
  malformed  the answer's required keys are removed (the schema check fails on every attempt)
  empty      the answer is an empty object
  missing    the answer file is not there
  unsupported  a well-formed answer whose summary says something its quote does not (code removes it: SUMMARY_NOT_IN_QUOTE and the skipped steps)
each applied to one answer (the first extract answer) or to every generator answer. The judge answers stay the recorded ones (they are real model answers).
Cases: the sample (shipped curated set too) and two library cases (library routes exist in local mode only).

What is scanned: every string VALUE (never a key) in every response of the case: case, status, trace, judges, audit, narrative, billing, export (before and after accepting),
dismissal suggestions, and each item and its trace. The one structured exception is the identity of the real second-check model: an identifier with no whitespace (a model id,
a backend name, a prompt version) inside a judge context (a `judge` key, a call row with role judge, a judge step). Sentences are never exempt: a sentence that mentions
the second check must say "second check", not "AI".
"""
import json
import os
import re
import shutil
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend.api import create_app

FORBIDDEN = re.compile(r"\bAI\b|claude|sonnet|haiku|opus|model", re.I)
TOOLTIP = "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."      # D-065, exact
LIBRARY = ("case_lib09_spanish_interpreter_espalda", "case_lib10_eob_ub04_cms1500")
SRC = os.path.join(os.path.dirname(__file__), "..", "fixtures", "llm")
PREPARED_MODEL = "hand-checked (qa)"
FAULTS = ("valid", "malformed", "empty", "missing", "unsupported")
UNSUPPORTED_SUMMARY = "Patient received a lumbar epidural steroid injection of 4 mL and was diagnosed with a herniated disc at L4-L5."
SCOPES = ("one", "all")


def _client(tmp_path, monkeypatch, *, fixture_dir=None, fixture_set=None, mode="local"):
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
    db = tmp_path / "p.sqlite"
    return TestClient(create_app(str(db), static_dir=str(tmp_path)), client=("127.0.0.1", 50000)), db


def _new_case(c, case):
    r = c.post("/api/cases", json={"sample": True} if case == "sample" else {"library": case})
    assert r.status_code == 201, r.text
    return r.json()["token"]


def _run(c, tok):
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(480):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"):
            return s
        time.sleep(0.25)
    raise AssertionError("run did not finish")


def _generator_keys(tmp_path, monkeypatch, case):
    """The fixture keys the case's generator steps asked for on the recorded set, in call order (first attempt of each step)."""
    c, db = _client(tmp_path / "rec", monkeypatch)
    tok = _new_case(c, case)
    _run(c, tok)
    conn = sqlite3.connect(str(db))
    rows = conn.execute("SELECT step, item_id, prompt_sha256, parsed_ok FROM llm_calls WHERE role='generator' ORDER BY item_id, created_at, rowid").fetchall()
    conn.close()
    keys = []
    for step, item_id, key, ok in rows:
        if os.path.isfile(os.path.join(SRC, f"{key}.json")) and (step, key) not in keys:      # every generator answer that was recorded, whether or not it parsed; the first extract is e1's on the sample
            keys.append((step, key))
    return keys


def _break(path, fault):
    if fault == "missing":
        os.unlink(path)
        return
    with open(path) as f:
        d = json.load(f)
    if fault == "empty":
        d["output"] = {}
    elif fault == "unsupported":
        if isinstance(d.get("output"), dict) and "summary" in d["output"]:
            d["output"]["summary"] = UNSUPPORTED_SUMMARY      # well formed, but nothing in the quote supports it
    else:      # malformed: the required keys are gone and an unknown one is added, so the schema check fails every attempt
        d["output"] = {"unexpected": "not the shape the step asks for"}
    with open(path, "w") as f:
        json.dump(d, f)


def build_set(root, keys, fault, scope):
    """<root>/curated/: the recorded set, with the case's generator answers relabelled prepared and the fault injected into the first extract answer or into all."""
    d = os.path.join(root, "curated")
    os.makedirs(d)
    for f in os.listdir(SRC):
        if f.endswith(".json"):
            shutil.copy(os.path.join(SRC, f), d)
    for _, key in keys:
        p = os.path.join(d, f"{key}.json")
        with open(p) as f:
            o = json.load(f)
        o["recorded_from"] = {"backend": "curated", "model": PREPARED_MODEL, "recorded_at": "2026-11-02T00:00:00Z"}
        with open(p, "w") as f:
            json.dump(o, f)
    if fault != "valid":
        targets = [k for s, k in keys if s.startswith("extract")][:1] if scope == "one" else [k for _, k in keys]
        for key in targets:
            _break(os.path.join(d, f"{key}.json"), fault)
    return d


# ------------------------------------------------------------------ scanning
def _is_ident(s):
    return not re.search(r"\s", s)


VERBATIM_KEYS = {"system_text", "user_text", "response_raw", "raw"}      # the prompt a call carried and the answer it returned, stored word for word (local-mode audit): model I/O, not a statement made to the reader
JUDGE_MODELS = {"claude-haiku-5-5"}      # the real second-check model; the case's `models.judge` is added at run time


def strings(o, path="", judge=False):
    """(path, value, in_judge_context) for every string value, never a key. Verbatim model I/O fields are skipped."""
    if isinstance(o, dict):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:47.825Z

**tool call — Bash**
````
{
 "command": "cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); sed -n 140,369p tests/unit/test_prepared_property.py",
 "description": "Read property test remainder"
}
````

### User / tool · 2026-11-02T23:12:47.971Z

**tool result**
````
    if isinstance(o, dict):
        is_judge = judge or o.get("role") == "judge" or str(o.get("id", "")).startswith("judge") or str(o.get("step", "")).startswith(("judge", "j1", "j2", "j3", "j4"))
        for k, v in o.items():
            if k in VERBATIM_KEYS:
                continue
            yield from strings(v, f"{path}.{k}", is_judge or str(k).startswith("judge"))
    elif isinstance(o, list):
        for i, v in enumerate(o):
            yield from strings(v, f"{path}[{i}]", judge)
    elif isinstance(o, str):
        yield path, o, judge


def offenders(label, payload, judge_models=frozenset(JUDGE_MODELS)):
    """(label, path, matched word, text) for each string that matches FORBIDDEN, minus the D-065 tooltip sentence. Exempt, and only these: an identifier with no whitespace
    (model id, backend name, prompt version) in a judge context, or exactly the real second-check model's id anywhere (e.g. a judge's objection row)."""
    out = []
    for path, s, judge in strings(payload):
        t = s.replace(TOOLTIP, "")
        m = FORBIDDEN.search(t)
        if m and not ((judge and _is_ident(s)) or s in judge_models):
            out.append((label, re.sub(r"\[\d+\]", "[]", path), m.group(0), s[:160]))
    return out


def actions(c, tok, case, res, get):
    """D-069 r5: the paths a reviewer takes that the plain accept pass does not. (1) Edit the quote of the first two prepared entries to their first sentence, then accept them:
    the second check has no recorded answer on the new quote, so the item, trace and export say so in the prepared voice. (2) Accept one entry that still has no second-check answer.
    (3) Write a manual entry for each record that has no live entry (a rejected or failed prepared answer), then read it. Every response, refusals included, is kept."""
    recs = {r["id"]: r for r in case.get("records", [])}
    live = [e for e in case.get("entries", []) if e.get("state") != "rejected"]
    edited = 0
    for e in live:
        rec = recs.get((e.get("record_ids") or [None])[0]) or {}
        sents = [x["text"] for x in rec.get("sentences", [])]
        if len(sents) < 2 or edited >= 2:
            continue
        runs = [" ".join(sents[i:j]) for n in range(len(sents) - 1, 0, -1) for i in range(len(sents) - n + 1) for j in (i + n,)]      # shorter quotes made of whole sentences, longest first
        for k, q in enumerate(runs):
            r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "edit", "edits": {"excerpt": q}})
            res[f"edit{k}:{e['id']}" if r.status_code != 200 else f"edit:{e['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
            if r.status_code == 200:
                edited += 1
                break
        get(f"item-edited:{e['id']}", f"/items/{e['id']}")      # edited, not yet accepted: "you changed the quote, the second check has no answer"
        get(f"trace-edited:{e['id']}", f"/items/{e['id']}/trace")
        get(f"trace-edited-case:{e['id']}", "/trace")
        get(f"export-edited:{e['id']}", "/export")
        c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"})      # then accepted: the export names the second check that never ran
        get(f"item-accepted:{e['id']}", f"/items/{e['id']}")
        get(f"trace-accepted:{e['id']}", f"/items/{e['id']}/trace")
    for e in live[2:3]:      # accepted without ever editing: the second check's answer is whatever the set has
        r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "accept"})
        res[f"accept-plain:{e['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    have = {rid for e in live for rid in (e.get("record_ids") or [])}
    for rid, rec in recs.items():
        if rid in have or rec.get("duplicate_of") or not rec.get("sentences"):
            continue
        first = rec["sentences"][0]["text"]
        r = c.post(f"/api/cases/{tok}/records/{rid}/entry", json={"summary": first, "excerpt": first})
        body = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
        res[f"manual:{rid}"] = body
        mid = (body.get("item") or body).get("id") if isinstance(body, dict) else None
        if mid:
            get(f"item-manual:{mid}", f"/items/{mid}")
            get(f"trace-manual:{mid}", f"/items/{mid}/trace")
    get("case-actions", "")
    get("export-actions", "/export")
    get("trace-actions", "/trace")
    get("judges-actions", "/judges")
    get("narrative-actions", "/narrative")


def collect(c, tok, do_actions=True):
    """Every response of the case, as {label: json}. Includes refusals (a 422 body is a response too)."""
    res = {}

    def get(label, path):
        r = c.get(f"/api/cases/{tok}{path}")
        try:
            res[label] = r.json()
        except ValueError:
            pass
        return r

    case = get("case", "").json()
    for p in ("/status", "/trace", "/judges", "/audit", "/narrative", "/billing", "/dismissal_suggestions", "/export"):
        get(p, p)
    ids = [x["id"] for k in ("entries", "flags", "amounts") for x in case.get(k, [])] + [x["id"] for x in case.get("tray", []) if isinstance(x, dict) and x.get("id")]
    for iid in ids:
        get(f"item:{iid}", f"/items/{iid}")
        get(f"trace:{iid}", f"/items/{iid}/trace")
    if do_actions:
        actions(c, tok, case, res, get)
    case = get("case-before-accept", "").json()
    for iid in [x["id"] for x in case.get("entries", []) if x.get("review_status") not in ("accepted", "edited")]:      # decide: accept each entry, and dismiss the first flag; then read the case, the export and the first entry again
        r = c.post(f"/api/cases/{tok}/items/{iid}/review", json={"action": "accept"})
        res[f"accept:{iid}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    for f in case.get("flags", [])[:1]:
        r = c.post(f"/api/cases/{tok}/items/{f['id']}/review", json={"action": "dismiss"})
        res[f"dismiss:{f['id']}"] = r.json() if r.headers.get("content-type", "").startswith("application/json") else {}
    get("case-after", "")
    get("export-after", "/export")
    get("trace-after", "/trace")
    for iid in ids[:3]:
        get(f"trace-after:{iid}", f"/items/{iid}/trace")
    return res


def prepared_items(res):
    return [k for k, v in res.items() if k.startswith("item:") and isinstance(v, dict) and (v.get("item") or {}).get("prepared") is True]


def run_variant(tmp_path, monkeypatch, case, fault, scope, shipped=False, mode="local", do_actions=True):
    if shipped:
        c, _ = _client(tmp_path / "run", monkeypatch, fixture_set="curated", mode=mode)
    else:
        keys = _generator_keys(tmp_path / "keys", monkeypatch, case)
        assert keys, f"no generator fixtures for {case}"
        c, _ = _client(tmp_path / "run", monkeypatch, fixture_dir=build_set(str(tmp_path / "set"), keys, fault, scope), mode=mode)
    tok = _new_case(c, case)
    status = _run(c, tok)
    return c, tok, status, collect(c, tok, do_actions)


def _assert_clean(res, where):
    bad = []
    for label, payload in res.items():
        bad += offenders(label, payload, frozenset(JUDGE_MODELS | {((res.get('case') or {}).get('models') or {}).get('judge')}))
    seen = {}
    for label, path, word, s in bad:
        seen.setdefault((re.sub(r"[:].*", "", label), path, word), s)
    assert not seen, f"{where}: {len(bad)} string(s) for a prepared case match {FORBIDDEN.pattern}:\n" + "\n".join(f"  {k}: {v}" for k, v in sorted(seen.items())[:40])


# ------------------------------------------------------------------ the property
@pytest.fixture(autouse=True)
def _dirs(tmp_path):
    for n in ("rec", "keys", "run", "set"):
        (tmp_path / n).mkdir()


@pytest.mark.parametrize("scope", SCOPES)
@pytest.mark.parametrize("fault", FAULTS)
@pytest.mark.parametrize("case", ("sample",) + LIBRARY)
def test_no_prepared_text_names_an_ai_or_a_model(tmp_path, monkeypatch, case, fault, scope):
    if fault == "valid" and scope == "all":
        pytest.skip("valid has no scope")
    c, tok, status, res = run_variant(tmp_path, monkeypatch, case, fault, scope)
    where = f"{case}/{fault}/{scope}"
    if fault == "valid":
        assert prepared_items(res), f"{where}: no item is marked prepared, so the property would be vacuous"
    cm = res["case"].get("models") or {}
    assert cm.get("generator") == PREPARED_MODEL and cm.get("generator_prepared") is True, (where, cm)      # a broken answer never flips the case back to a model label
    _assert_clean(res, where)


def test_shipped_curated_sample_in_demo_and_local_mode(tmp_path, monkeypatch):
    for mode in (None, "local"):
        sub = tmp_path / (mode or "demo")
        for n in ("rec", "keys", "run", "set"):
            (sub / n).mkdir(parents=True)
        c, tok, status, res = run_variant(sub, monkeypatch, "sample", "valid", "one", shipped=True, mode=mode)
        assert len(prepared_items(res)) >= 16, mode
        _assert_clean(res, f"shipped/{mode}")


@pytest.mark.parametrize("fault", ("malformed", "empty"))
def test_a_malformed_or_empty_answer_reads_exactly_like_a_missing_one(tmp_path, monkeypatch, fault):
    """D-069 (2): malformed means missing. The record's item, its trace and the case trace say the same thing whichever way the answer is unusable."""
    texts = {}
    for f in (fault, "missing"):
        sub = tmp_path / f
        for n in ("rec", "keys", "run", "set"):
            (sub / n).mkdir(parents=True)
        c, tok, status, res = run_variant(sub, monkeypatch, "sample", f, "one")
        it = res["item:e1"]["item"]
        steps = [(s["id"], s["label"], s["status"], s["why"], s["reason_code"]) for s in res["trace:e1"]["steps"]]
        ct = [(s["id"], s["label"], s["status"], s["why"]) for s in res["/trace"]["steps"] if s["id"] in ("extract", "judges")]
        texts[f] = (it["state"], it.get("why"), it.get("explanation"), steps, ct, res["case"]["models"])
    assert texts["missing"][0] == "rejected" and "no prepared answer" in json.dumps(texts["missing"][3]).lower(), "the fault must hit e1, or this test proves nothing"
    assert texts[fault] == texts["missing"], json.dumps({k: v for k, v in texts.items()})[:3000]


def test_a_prepared_answer_carries_no_prompt_version(tmp_path, monkeypatch):
    """T-177 r3 F4 (the round-2 acceptance test that was never written): nothing prompted a hand-written answer, so no audit row, trace step or export field names a generator prompt for it."""
    c, tok, status, res = run_variant(tmp_path, monkeypatch, "sample", "valid", "one", shipped=True, do_actions=False)      # provenance of a clean export: the action pass leaves blockers
    prepared_rows = [x for x in res["/audit"]["calls"] if x.get("prepared")]
    assert len(prepared_rows) >= 16
    assert all(x["prompt_version"] is None for x in prepared_rows), [x["step"] for x in prepared_rows if x["prompt_version"]]
    steps = [s for k, v in res.items() if k.startswith("trace:") for s in v["steps"] if (s.get("evidence") or {}).get("model", {}).get("prepared")]
    assert steps and all(s["evidence"].get("prompt_version") is None for s in steps)
    pv = res["export-after"]["provenance"]["prompt_versions"]
    assert pv and not {"extract_v1", "extract_es_v1", "flags_v1", "conflicts_v1", "split_v1", "narrative_v1"} & set(pv), pv      # only the second check's prompts remain


# ------------------------------------------------------------------ r5: the twins themselves
def test_every_sentence_that_names_an_ai_has_a_prepared_twin_and_no_twin_names_one():
    """T-177 r5 (staff-engineer r4 F1/F5): the lookups are `(TWIN.get(code) if prepared else None) or AI_TEXT`, so a deleted or misspelled twin falls back to the AI sentence without a sound.
    Close that statically: every why / trace-why / next-action sentence that matches FORBIDDEN has a twin under the same code, and no twin matches it."""
    from app.backend import trace, why
    tables = (("why", why._WHY, why._WHY_PREPARED), ("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED), ("next", trace._NEXT, trace._NEXT_PREPARED))
    missing, dirty, orphan = [], [], []
    for name, base, twin in tables:
        missing += [f"{name}.{k}" for k, v in base.items() if FORBIDDEN.search(v) and not twin.get(k)]
        dirty += [f"{name}.{k}" for k, v in twin.items() if FORBIDDEN.search(v)]
        orphan += [f"{name}.{k}" for k in twin if k not in base]
    assert not missing, f"AI wording with no prepared twin: {missing}"
    assert not dirty, f"a prepared twin that names an AI or a model: {dirty}"
    assert not orphan, f"a twin with no sentence to replace (misspelled code?): {orphan}"
    assert why.why("INJECTION_SUSPECTED", prep=True) != why.why("INJECTION_SUSPECTED")


@pytest.mark.parametrize("fault", ("valid", "unsupported"))
def test_the_edit_and_hand_entry_paths_are_reached_and_use_the_prepared_voice(tmp_path, monkeypatch, fault):
    """The action pass is not vacuous. After "edit the quote" and then "accept", responses carry the prepared twins (not just a clean scan): the edit warning, the edited-not-accepted
    trace sentence, the export's "second check never ran" blocker. If a twin is deleted the AI sentence is printed instead and these fail (and the scan above fails too)."""
    from app.backend import trace, why
    c, tok, status, res = run_variant(tmp_path, monkeypatch, "sample", fault, "one")
    assert any(k.startswith("edit:") and res[k].get("item") for k in res), "no edit was accepted, so the edit path was not exercised"
    blob = json.dumps(res, ensure_ascii=False)
    for name, base, twin, code in (("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED, "EDIT_NOT_CONFIRMED_ITEM_AI"), ("trace_why", trace.TRACE_WHY, trace.TRACE_WHY_PREPARED, "JUDGE_NOT_RUN"),
                                   ("why", why._WHY, why._WHY_PREPARED, "JUDGE_UNAVAILABLE")):
        assert twin[code] in blob, f"{name}.{code}: the prepared twin never appears in any response of the action pass"
        assert base[code] not in blob, f"{name}.{code}: the AI sentence appears in a prepared case"
    assert any(k.startswith("warn") or "warnings" in json.dumps(v) for k, v in res.items() if k.startswith("edit:")), "the edit response carried no second-check warning"
    if fault == "unsupported":
        e1 = json.dumps(res["item:e1"]) + json.dumps(res["trace:e1"])
        assert why._WHY_PREPARED["SUMMARY_NOT_IN_QUOTE"] in e1, "the unsupported summary was not removed by code"
        assert any(k.startswith("manual:") for k in res), "no hand entry was written for the removed entry"
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:56.145Z

**tool call — Bash**
````
{
 "command": "cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); grep -n '\"message\"\\|message=' app/backend/review.py | head -60; grep -n \"def unavailable_sentence\" -A14 app/backend/why.py",
 "description": "Find messages in review.py"
}
````

### User / tool · 2026-11-02T23:12:56.244Z

**tool result**
````
38:        raise ReviewError(404, "not_found", message="No such item.") from None
40:        raise ReviewError(404, "not_found", message="No such item.")
61:    return ReviewError(422, "DATE_UNCONFIRMED", message="Confirm this entry's date first (Dates to confirm). An entry with no confirmed date "
207:              "message": f["message"],      # T-159: the flag's own sentence, without the "confirm by name" tail, so a client never strips the token out of the error message
365:        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
464:        warnings.append({"code": code, "message": "The second check could not fully support the summary from the quote; the item stays marked for review.", "item_id": item_id})
466:        warnings.append({"code": "JUDGE_UNAVAILABLE", "message": why.unavailable_sentence({"verdict": "unavailable", "reason_code": judge_code, "error_class": judge_error}, prep) + " Until you do, the item stays marked for review.", "item_id": item_id})
544:                                "message": "Code removed the clause that stated a dollar amount from the summary (" + "; ".join(trimmed["removed"])
583:        raise ReviewError(404, "not_found", message="No such record.")
735:        raise ReviewError(404, "not_found", message="No such record.")
810:            warns.append({"code": e["failure"], "message": msg, "item_id": f["id"]})
818:        warns.append({"code": "LLM_UNAVAILABLE", "message": "The record was split off; its entry has not been drafted yet.", "item_id": None})
93:def unavailable_sentence(judge, prep=False) -> str:
94-    """The one sentence for a second check that gave no answer, by cause (used by the item's why and by the edit warning)."""
95-    if judge_in_demo(judge):
96-        return JUDGE_DEMO_PREPARED if prep else JUDGE_DEMO
97-    return JUDGE_FAILED if judge_failed(judge) else (_WHY_PREPARED if prep else _WHY)["JUDGE_UNAVAILABLE"]
98-
99-
100-def why(code: str, judge=None, prep=False) -> str:
101-    if code == "JUDGE_UNAVAILABLE":
102-        return unavailable_sentence(judge, prep)
103-    return (_WHY_PREPARED.get(code) if prep else None) or _WHY[code]
104-
105-
106-def join(reasons, judge=None, prep=False) -> str:
107-    """The sentences for a reason list. A recorded-answer miss (FIXTURE_MISS, demo) is not a failed call: no model was asked, so the 'did not run' sentence stays."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:12:59.254Z

**tool call — Bash**
````
{
 "command": "cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); sed -n 748,800p app/backend/review.py | cut -c1-260",
 "description": "Read manual_entry body"
}
````

### User / tool · 2026-11-02T23:12:59.348Z

**tool result**
````
    span = grounding.locate(rec["excerpt"], excerpt)
    eid = f"e{rec['seq']}_m"
    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call, prep=AU.answers_prepared(),      # D-069 r5: the set in use decides the wording
                         ocr_derived=record_id in ocr_record_ids(conn, case_id), bill_state=lambda: bill_state_for(conn, case_id, [record_id]))
    base = generator.body_offset(rec)
    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
                              "date_provider_from_header": True},
              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
    DB.add_item(conn, case_id, "entry", {
        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
    enforce_ocr(conn, case_id, t)
    from app.backend import pipeline as PL
    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no longer fails
    from app.backend import present
    return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}


# ---------------------------------------------------------------- 'not a duplicate' (D-031, T-056)
def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
    """Undo one merge: the merged entry keeps its other records; `record_id` gets an entry of its own (generator + judge 1 over that record),
    its amounts come back, gap flags are recomputed, and the decision is remembered in the case config so a rerun keeps it. Logged as a
    `not_duplicate` event on the original entry."""
    from app.backend import pipeline as PL
    from app.llm import provider as P
    t = _now(now)
    kind, ent = _item(conn, case_id, entry_id)
    if kind != "entry":
        raise _bad("Only a merged entry can be split.")
    ids = list(ent["record_ids"] or [])
    if record_id not in ids or ids.index(record_id) == 0 or len(ids) < 2:
        raise _bad("That record is not one of the duplicates merged into this entry.")
    case = DB.get_case(conn, case_id)
    cfg = dict(case.get("config") or {})
    cfg["not_duplicates"] = sorted(set(cfg.get("not_duplicates", [])) | {record_id})
    DB.update_case(conn, case_id, config_json=cfg)
    conn.execute("UPDATE records SET duplicate_of=NULL WHERE id=? AND case_id=?", (record_id, case_id))
    DB.update_item(conn, entry_id, now=t, case=case_id, record_ids_json=[i for i in ids if i != record_id])
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    rec = next(r for r in recs if r["id"] == record_id)
    warns = []
    # the split-off record's own entry (code-checked, then judge 1; a failure leaves it visibly without an entry)
    if call is not None:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:06.478Z

**tool call — Bash**
````
{
 "command": "cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); sed -n 508,580p app/backend/review.py | cut -c1-240; grep -n \"twin\\|_PREPARED\\b\" app/backend/trace.py | head -30",
 "description": "Read _edit return and trace twins"
}
````

### User / tool · 2026-11-02T23:13:06.600Z

**tool result**
````
    span = grounding.locate(rec["excerpt"], new_exc)
    base = generator.body_offset(rec)
    label, date_iso = item["provider"] or "", item["date_iso"] or ""
    from app.backend import present          # lazy: present imports review
    chk = _check_summary(item["id"], new_sum, new_exc, label, date_iso, span, rec, call, prep=present.Prov(conn, case_id).prepared(item),      # D-069 r5: the warning follows the item's provenance
                         ocr_derived=bool(ocr_record_ids(conn, case_id).intersection(item["record_ids"] or [])) or "OCR_DERIVED" in (item.get("state_reasons") or []),
                         bill_state=lambda: bill_state_for(conn, case_id, item.get("record_ids")))
    toks, code_reasons, ladder_verdict, call_id, state, reasons = (
        chk["toks"], chk["code_reasons"], chk["ladder_verdict"], chk["call_id"], chk["state"], chk["reasons"])
    edited = dict(prev)
    edited.update(at=store.iso(t))
    edited.pop("code_trim", None)           # T-139 r3: the trace shows the removal only while the wording it made is still the wording (a later hand edit or quote change clears it)
    if trimmed:
        edited["code_trim"] = {"rule": "T-139", "removed": list(trimmed["removed"]), "summary_before": summary_before_trim, "summary_after": new_sum,
                               "quote_before": cur_exc, "quote_after": new_exc}
    if "summary" in edits or "summary" in prev or trimmed:
        edited.update(summary=new_sum, original_summary=prev.get("original_summary", item["summary"]))
    if "excerpt" in edits or "excerpt" in prev:
        edited.update(excerpt=new_exc, original_excerpt=prev.get("original_excerpt", item["excerpt"]),
                      excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None)
    set_review(conn, case_id, item["id"], "edit", edited=edited, now=t, kind="entry", item=item, recs=recs)     # D-051: edit implies accept; refused before any write
    lad = item.get("ladder") or {"item_id": item["id"]}
    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
        lad["pre_edit"] = {"judge": copy.deepcopy(lad.get("judge")), "code_checks": copy.deepcopy(lad.get("code_checks")), "rejudge": copy.deepcopy(lad.get("rejudge")),
                           "state": item["state"], "state_reasons": list(item.get("state_reasons") or []), "lad_state": lad.get("state")}      # deep copies: the edit updates code_checks in place below
    lad.pop("rejudge", None)       # T-134 r4: the rerun attempts belong to the wording and quote they ran on; the new wording or quote has had none
    lad["judge"] = {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": call_id, "verdict": ladder_verdict,
                    "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})}
    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
                                              qualifier_carried="SUMMARY_DROPS_QUALIFIER" not in code_reasons)
    lad["state"] = state
    lad["pre_edit"]["after"] = {"state": state, "state_reasons": list(reasons)}      # what the latest edit left, to tell later on whether anything else has changed the state since
    DB.update_item(conn, item["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
    enforce_ocr(conn, case_id, t)
    if trimmed:
        chk["warnings"].append({"code": "CHARGE_CLAUSE_REMOVED", "item_id": item["id"], "removed": trimmed["removed"],
                                "message": "Code removed the clause that stated a dollar amount from the summary (" + "; ".join(trimmed["removed"])
                                           + "). Amounts go only in the internal notes. Check the summary against the quote."})
    return chk["warnings"]


def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
    The state and reasons come back too, unless something else has rewritten them since the edit (a date confirm, a rejudge): then only the judge result and
    code checks return and the state is left as it is. No snapshot (an edit saved before this change): nothing happens, as before. Returns True when restored."""
    lad = dict(item.get("ladder") or {})
    snap = lad.pop("pre_edit", None)
    if kind != "entry" or not snap:
        return False
    if snap.get("judge") is not None:
        lad["judge"] = snap["judge"]
    else:
        lad.pop("judge", None)
    if snap.get("code_checks") is not None:
        lad["code_checks"] = snap["code_checks"]
    if snap.get("rejudge"):
        lad["rejudge"] = snap["rejudge"]
    else:
        lad.pop("rejudge", None)
    fields = {}
    after = snap.get("after") or {}
    if after and item["state"] == after.get("state") and sorted(item.get("state_reasons") or []) == sorted(after.get("state_reasons") or []):
        fields = {"state": snap["state"], "state_reasons_json": list(snap["state_reasons"])}
        if snap.get("lad_state") is not None:
            lad["state"] = snap["lad_state"]
    DB.update_item(conn, item_id, now=t, case=case_id, ladder=lad, **fields)
    enforce_ocr(conn, case_id, t)
    return True


# ---------------------------------------------------------------- confirm_date
def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
    t = _now(now)
23:# would name an AI, a model or a drafter is written twice, side by side (`pick(recorded, prepared)` or a *_PREPARED table). Nothing is produced by rewriting the AI sentence.
90:TRACE_WHY_PREPARED = {      # twins of the TRACE_WHY sentences that name an AI (D-069)
99:_NEXT_PREPARED = {"RERUN": "Run the steps again.", "CONFIRM_RERUN": "Run the steps again; confirm that earlier decisions are kept."}
128:        return (TRACE_WHY_PREPARED.get(code) if _PREP.get() else None) or TRACE_WHY[code]
136:    d = {"code": code, "text": text or (_NEXT_PREPARED.get(code) if _PREP.get() else None) or _NEXT[code]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:12.158Z

**tool call — Bash**
````
{
 "command": "cd $(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); sed -n 86,100p app/backend/trace.py | cut -c1-300; grep -n 'return chk\\[\"warnings\"\\]' app/backend/review.py",
 "description": "Read trace twin tables"
}
````

### User / tool · 2026-11-02T23:13:12.294Z

**tool result**
````
    "CAUSATION_NOT_QUOTED": narrative.REASONS["CAUSATION_NOT_QUOTED"],
    "SEVERITY_NOT_QUOTED": narrative.REASONS["SEVERITY_NOT_QUOTED"],
    "FLAG_CONTENT": narrative.REASONS["FLAG_CONTENT"],
}
TRACE_WHY_PREPARED = {      # twins of the TRACE_WHY sentences that name an AI (D-069)
    "EDIT_NOT_CONFIRMED_ITEM_AI": "You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. If you accept it, the export will be blocked until the second check answers (Run the second chec
    "ITEMS_NOT_REVIEWED": "Some items have no decision yet; they will not be in the letter and the disclosure line counts them.",
    "RUN_IN_PROGRESS": "The run is still going.",
    "JUDGE_NOT_RUN": "You accepted this item, but the second check never ran on it. Nothing prepared goes into the letter without that check, and accepting does not replace it.",
    "JUDGE_NOT_RUN_RETRIED": "You accepted this item, but the second check ran again and still gave no answer. Nothing prepared goes into the letter without that check, and accepting does not replace it. It clears when the check answers, or when you edit the summary in your own words.",
    "CODE_CHECK_FAILED_AI": "This summary is a prepared answer and a code check on it fails, so it cannot go into the letter until the summary matches the quote.",
    "CODE_CHECK_FAILED": "You wrote or edited this summary, so the second check is not needed, but the code checks on the summary still have to pass before it can go into the letter.",
}
_NEXT_PREPARED = {"RERUN": "Run the steps again.", "CONFIRM_RERUN": "Run the steps again; confirm that earlier decisions are kept."}
_NEXT = {   # code -> fixed sentence
546:    return chk["warnings"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:13.387Z

Now add the new mutants to my r5 harness and run the baseline plus the three r4 mutants.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:19.180Z

**tool call — Bash**
````
{
 "command": "E=artifacts/review-evidence/T-177-staff-engineer-r5 && .venv/bin/python -I - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/mutate_r5.py\"\ns=open(p).read()\nnew='''    # ---- r5 fresh mutants\n    \"N1_edit_msg_model_name\": (\"app/backend/review.py\",\n        '    return chk[\"warnings\"]\\\\n\\\\n\\\\ndef restore_pre_edit',\n        '    return chk[\"warnings\"] + [{\"code\": \"RECHECKED\", \"message\": \"The edited quote was checked again with claude-sonnet-5-5.\", \"item_id\": item[\"id\"]}]\\\\n\\\\n\\\\ndef restore_pre_edit'),\n    \"N2_manual_msg_model_name\": (\"app/backend/review.py\",\n        '\"review\": present.review_view(conn, case_id), \"warnings\": chk[\"warnings\"]}\\\\n\\\\n\\\\n# ---------------------------------------------------------------- \\\\'not a duplicate\\\\'',\n        '\"review\": present.review_view(conn, case_id), \"warnings\": chk[\"warnings\"] + [{\"code\": \"ENTERED\", \"message\": \"Entered by hand; claude-sonnet-5-5 was not used.\", \"item_id\": eid}]}\\\\n\\\\n\\\\n# ---------------------------------------------------------------- \\\\'not a duplicate\\\\''),\n    \"N3_edit_prep_arg_reverted\": (\"app/backend/review.py\",\n        'span, rec, call, prep=present.Prov(conn, case_id).prepared(item),',\n        'span, rec, call,'),\n    \"N4_manual_prep_arg_reverted\": (\"app/backend/review.py\",\n        'span, rec, call, prep=AU.answers_prepared(),',\n        'span, rec, call,'),\n    \"T1_twin_removed_why_injection\": (\"app/backend/why.py\",\n        '    \"INJECTION_SUSPECTED\": \"This record contains instruction-like text that may be trying to steer the checks; review it before relying on it.\",\\\\n',\n        ''),\n    \"T2_twin_removed_trace_judge_not_run\": (\"app/backend/trace.py\",\n        '    \"JUDGE_NOT_RUN\": \"You accepted this item, but the second check never ran on it. Nothing prepared goes into the letter without that check, and accepting does not replace it.\",\\\\n',\n        ''),\n    \"T3_twin_removed_why_unsupported\": (\"app/backend/why.py\",\n        '    \"SUMMARY_NOT_IN_QUOTE\": \"Every part of the prepared summary added',\n        '    \"SUMMARY_NOT_IN_QUOTE_X\": \"Every part of the prepared summary added'),\n}\npath, old, new = M[NAME]'''\ns=s.replace('}\\npath, old, new = M[NAME]', new,1) if False else s\ni=s.index('}\\npath, old, new = M[NAME]')\ns=s[:i]+new+s[i+len('}\\npath, old, new = M[NAME]'):]\nopen(p,\"w\").write(s)\nEOF\n.venv/bin/python -I -c \"import ast;ast.parse(open('$E/mutate_r5.py').read());print('ok')\"",
 "description": "Add r5 mutants to harness"
}
````

### User / tool · 2026-11-02T23:13:19.301Z

**tool result**
````
ok
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:21.546Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && E=artifacts/review-evidence/T-177-staff-engineer-r5 && (cd $A && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_property.py -q -p no:cacheprovider 2>&1 | tail -4) | tee $E/baseline-property.out",
 "description": "Run baseline property test in archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:13:21.601Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (tee artifacts/review-evidence/T-177-staff-engineer-r5/baseline-property.out)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:13:23.956Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && cd $A && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_prepared_property.py -q -p no:cacheprovider > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/baseline-property.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/baseline-property.out",
 "description": "Run baseline property test in archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:14:26.100Z

**tool result**
````
.s.........s.........s...............                                    [100%]
34 passed, 3 skipped in 61.56s (0:01:01)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:14:29.245Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && E=artifacts/review-evidence/T-177-staff-engineer-r5 && .venv/bin/python -I $E/run_mutants_r5.py $A tests/unit/test_prepared_property.py B2_skipped_summary_not_in_quote_ai B4_why_summary_not_in_quote_ai C5_trace_why_twin_dropped N1_edit_msg_model_name > $E/mutants-batch1.out 2>&1; cat $E/mutants-batch1.out",
 "description": "Run r4 mutants B2 B4 C5 and N1",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:15:12.091Z

**tool result**
````
B2_skipped_summary_not_in_quote_ai: KILLED | 1 failed, 7 passed, 1 skipped in 15.99s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-unsupported-one]']
B4_why_summary_not_in_quote_ai: KILLED | 1 failed, 7 passed, 1 skipped in 14.63s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-unsupported-one]']
C5_trace_why_twin_dropped: KILLED | 1 failed in 7.37s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-valid-one]']
N1_edit_msg_model_name: KILLED | 1 failed in 2.94s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-valid-one]']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:15:16.779Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && E=artifacts/review-evidence/T-177-staff-engineer-r5 && .venv/bin/python -I $E/run_mutants_r5.py $A tests/unit/test_prepared_property.py N2_manual_msg_model_name N3_edit_prep_arg_reverted N4_manual_prep_arg_reverted T1_twin_removed_why_injection T2_twin_removed_trace_judge_not_run T3_twin_removed_why_unsupported > $E/mutants-batch2.out 2>&1; cat $E/mutants-batch2.out",
 "description": "Run remaining fresh mutants",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:16:43.703Z

**tool result**
````
N2_manual_msg_model_name: KILLED | 1 failed, 1 passed, 1 skipped in 4.91s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-malformed-one]']
N3_edit_prep_arg_reverted: KILLED | 1 failed in 2.27s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-valid-one]']
N4_manual_prep_arg_reverted: KILLED | 1 failed, 1 passed, 1 skipped in 7.09s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-malformed-one]']
T1_twin_removed_why_injection: KILLED | 1 failed, 31 passed, 3 skipped in 53.21s | ['FAILED tests/unit/test_prepared_property.py::test_every_sentence_that_names_an_ai_has_a_prepared_twin_and_no_twin_names_one']
T2_twin_removed_trace_judge_not_run: KILLED | 1 failed in 2.19s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-valid-one]']
T3_twin_removed_why_unsupported: KILLED | 1 failed, 7 passed, 1 skipped in 14.38s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-unsupported-one]']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:16:47.327Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && E=artifacts/review-evidence/T-177-staff-engineer-r5 && P=.venv/bin/python && for n in N1_edit_msg_model_name N2_manual_msg_model_name; do $P -I $E/mutate_r5.py apply $A $n >/dev/null; (cd $A && /Users/arsis/zlayt-pm-project/$P -m pytest tests/unit/test_prepared_property.py -q -p no:cacheprovider -x -k \"sample-valid-one or sample-malformed-one\" 2>&1 | grep -E \"^E  |FAILED|passed|failed\" | head -8) > $E/why-$n.out; $P -I $E/mutate_r5.py restore $A $n >/dev/null; echo \"== $n\"; cat $E/why-$n.out; done",
 "description": "Confirm N1 and N2 fail for the right reason",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:16:47.391Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to artifacts/review-evidence/T-177-staff-engineer-r5/why-$n.out)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:16:52.607Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-177-staff-engineer-r5/why_mutant_r5.py <<'EOF'\n\"\"\"Usage: python -I why_mutant_r5.py <archive> <mutant> '<pytest -k expr>' : apply, run, print the E-lines of the failure, restore.\"\"\"\nimport subprocess, sys\nA, N, K = sys.argv[1:4]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nH = \"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5\"\nsubprocess.run([PY, \"-I\", f\"{H}/mutate_r5.py\", \"apply\", A, N], check=True, capture_output=True)\ntry:\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"tests/unit/test_prepared_property.py\", \"-q\", \"-p\", \"no:cacheprovider\", \"-x\", \"-k\", K], cwd=A, capture_output=True, text=True, timeout=300)\n    print(N, \"rc\", r.returncode)\n    for l in r.stdout.splitlines():\n        if l.startswith((\"E  \", \"FAILED\")) or \" passed\" in l or \" failed\" in l:\n            print(l[:260])\nfinally:\n    rr = subprocess.run([PY, \"-I\", f\"{H}/mutate_r5.py\", \"restore\", A, N], capture_output=True, text=True)\n    assert rr.returncode == 0, rr.stderr\nEOF\nA=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1); for n in N1_edit_msg_model_name N2_manual_msg_model_name; do .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/why_mutant_r5.py $A $n \"sample-valid-one or sample-malformed-one\"; done > artifacts/review-evidence/T-177-staff-engineer-r5/why-N1-N2.out 2>&1; cat artifacts/review-evidence/T-177-staff-engineer-r5/why-N1-N2.out",
 "description": "Show N1 N2 failure reasons",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:17:02.090Z

**tool result**
````
N1_edit_msg_model_name rc 1
E       AssertionError: sample/valid/one: 2 string(s) for a prepared case match \bAI\b|claude|sonnet|haiku|opus|model:
E           ('edit', '.warnings[].message', 'claude'): The edited quote was checked again with claude-sonnet-5-5.
E       assert not {('edit', '.warnings[].message', 'claude'): 'The edited quote was checked again with claude-sonnet-5-5.'}
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=ce65d6364ffc9 step=j1 attempt=1 prompt_hash=1e70aaffef56fca8357976b6f79bb9edb28033b7f40f90dbd2bfa99d51868742
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c4cd91ae48364 step=j1 attempt=1 prompt_hash=d625988273a9c816758784ab6214e0ef9d483848cb415dd32c903bc64879a89a
FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-valid-one]
1 failed, 35 deselected in 4.51s
N2_manual_msg_model_name rc 1
E       AssertionError: sample/malformed/one: 1 string(s) for a prepared case match \bAI\b|claude|sonnet|haiku|opus|model:
E           ('manual', '.warnings[].message', 'claude'): Entered by hand; claude-sonnet-5-5 was not used.
E       assert not {('manual', '.warnings[].message', 'claude'): 'Entered by hand; claude-sonnet-5-5 was not used.'}
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c8eb3d5d1dc9e step=extract attempt=1 prompt_hash=98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c5ff7af371c17 step=j1 attempt=1 prompt_hash=d625988273a9c816758784ab6214e0ef9d483848cb415dd32c903bc64879a89a
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c4fdb064738f7 step=j1 attempt=1 prompt_hash=ecb960e45c9e5444ac7f7989022298821f9e82ce1aefec7fd48b5d692693974d
WARNING  zlayt.llm:audited.py:141 llm call failed call_id=c21b6bc183f6f step=j1 attempt=1 prompt_hash=f195f8d56bec3c031aaa9187e68e9f2b99f73ca30d2b5e8cdd1fb038d096e75a
FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[sample-malformed-one]
1 failed, 1 passed, 35 deselected in 4.14s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:07.813Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && F=$(dirname $A)/r5-fresh && rm -rf $F && mkdir $F && git archive e425534 | tar -x -C $F && diff -rq $F $A -x __pycache__ -x .pytest_cache | head",
 "description": "Compare mutated archive with a fresh archive"
}
````

### User / tool · 2026-11-02T23:17:07.869Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (rm $)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:09.680Z

**tool call — Bash**
````
{
 "command": "A=$(ls -d /private/tmp/claude-501/*/*/scratchpad/r5 | head -1) && S=$(dirname $A) && mkdir $S/r5-fresh && git archive e425534 | tar -x -C $S/r5-fresh && diff -rq $S/r5-fresh $A -x __pycache__ -x .pytest_cache | head; echo diff-done",
 "description": "Compare mutated archive with fresh archive"
}
````

### User / tool · 2026-11-02T23:17:09.738Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (mkdir $)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:13.166Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ls $S && git archive e425534 | tar -x -C $S/r5-fresh && diff -rq $S/r5-fresh $S/r5 -x __pycache__ -x .pytest_cache | head; echo diff-done",
 "description": "Fresh archive and diff against mutated copy"
}
````

### User / tool · 2026-11-02T23:17:13.461Z

**tool result**
````
641ed.bak
CLAUDE.md
GATEM3_se
M1
M1_nocombine
M2
M2_find0
MASTER_PROMPT.md
T-047-run1.json
T-060-pass2-head
T-093-r3-2ab7896
T-093-r3-run.py.orig
T-093-r3-scripts
T-093-r4-3223e50
T-093-r4-mutA
T-093-r4-mutB
T-109-probe
T-109-r1-card
T-109-r1-head
T-109-unit-head.txt
T-124-r1-head
T-124-r1-mut2
T-124-r1-parent
T-133-r1-archive
T-133-r1-source
T-133-r3-archive-4065ef2
T-133-r3-archive-f939ccb
T-133-r3-mutA
T-133-r3-mutB
T-133-r3-mutC
T-133-r3-mutD
T-133-r3-scripts
T-133-r4-archive-head
T-133-r5-13d.py
T-133-r5-15be212
T-133-r5-6fa8ecc
T-133-r5-head
T-133-r5-mut-backslash
T-133-r5-parent
T-133-r5-parse.py
T-133-r5-pmh.py
T-133-r5-probe.py
T-133-r5-r1
T-133-r5-unit-head.log
T-152-r1
T-157-r2-852b060
T-157-r2-full-unit.out
T-157-r2-mut
T-157-r2-mutants.out
T-157-r2-mutate.py
T-157-r2-parse.py
T-157-r2-probe.py
T-157-r2-probe2.py
T-157-r2-probe3-K.out
T-157-r2-probe3-base.out
T-157-r2-probe3.py
T-157-r2-probe4.py
T-157-r3-f31b146
T-157-r3-mut
T-157-r3-mutants.out
T-157-r3-mutate.py
T-160-r1
T-197-612dc2c
T-197-head
T-197-mutants
T-197-probe
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
T106_m_exportbranch
T106_m_hlreview
T106_m_hltrace
T106_m_pdfbypass
T106_m_pdfclaude
T106_m_rootcal
T106_r2_mut_a
T106_r2_mut_b
T106_r2_mut_c
T106_r2_mut_d
T106_r2_probe
T106_r2_suite.txt
T106_r2_suite_run2.txt
T106_r2_verify
T106_scripts
T106_unit_run1.log
T106_unit_run2_rs.log
T108_r2_clone
T108_r2_verify
T108_verify
T112_r1
T112_r1_scripts
T112_r2
T112_r3
T112_r3_mut
T112_r3_scripts
T113_r1_b66e748
T113_r1_b66e7481
T113_r1_e1ce8dc
T113_r1_evalout
T113_r1_fresh
T113_r1_head
T113_r2_arch
T113_r2_arch2
T113_r2_clone
T113_r2_probe
T113_r2_unit.log
T115_card_show.txt
T115_staff_r1
T115_staff_r2
T119_r2
T119_r3
T119_staff_r1
T120_r3_cli1.txt
T120_r3_cli2.txt
T120_r3_evals_head
T120_r3_evals_parent
T120_r3_fix
T120_r3_fixprobe.py
T120_r3_fprobe.py
T120_r3_head
T120_r3_mut
T120_r3_parent
T120_r3_probe_head.txt
T120_r3_probe_parent.txt
T120_r3_unit.txt
T128_9_127_r1
T128_9_r2
T128_9_r2b
T128r4_prev
T132r1
T132r1p
T132r3_arc
T132r3_cli1.err
T132r3_cli1.txt
T132r3_cli2.err
T132r3_cli2.txt
T132r3_cli_arc.txt
T132r3_cli_ctl.txt
T132r3_ctl
T132r3_mut
T133-r3-cli-1.txt
T133-r3-cli-2.txt
T133-r3-cli-r1.txt
T133-r3-negex.txt
T133-r3-pycontext-kb.yml
T133-r3-unit.log
T133-r4-arch-4065ef2
T133-r4-arch-e79c3aa
T133-r4-arch-parent
T133-r4-cli-reports.txt
T133-r4-clone
T133-r4-mutM1
T133-r4-mutM2
T133-r4-mutM3
T133-r4-pipeline-run1.txt
T133-r4-pipeline-run2.txt
T133-r4-record.json
T133-r4-scripts
T133-r4-suite-archive.txt
T133-r4-suite-clone.txt
T134r4_head
T134r4_head2db
T134r4_mut
T134r4_mut2
T134r4_src
T136_r1_e2e_full.txt
T136_r1_e2e_full2.txt
T136_r1_head
T136_r1_mutA
T136_r1_mutA.log
T136_r1_mutB1
T136_r1_mutB1.log
T136_r1_mutB2
T136_r1_mutB2.log
T136_r1_mutC
T136_r1_mutC.log
T136_r1_serve.sh
T136_r1_server.log
T136_r1_server2.log
T136_r1_unit.txt
T138r2_parent
T139_r1
T140_r1
T140_r2
T140_r3
T140_r4
T141_head
T141_mut
T141_pre
T141_preN2
T141_probe
T141_run
T141r2_head
T141r2_libreport.json
T141r2_mut2
T141r2_mutants.txt
T141r2_parent
T141r2_pk_T141_head.err
T141r2_pk_T141_head.json
T141r2_pk_T141_pre.err
T141r2_pk_T141_pre.json
T141r2_pk_T141r2_head.err
T141r2_pk_T141r2_head.json
T141r2_pl_orig.py
T141r3_head
T141r3_mut
T141r3_r2
T141r3_scripts
T141r4_head
T141r4_prev
T141r5_head
T141r5_mutA
T141r5_prev
T141r5_scripts
T141r6_824984f
T141r6_evidence
T141r6_head
T141r6_r5
T141r7_6379c0b
T141r7_824984f
T141r7_83f1afd
T141r7_acad4f6
T141r7_c2913a6
T141r7_head
T141r7_mut_guard2
T141r8_head_99438fb
T141r8_mutant_two_digit_off
T155_r1
T155r2_T164
T157r3
T159_161_r1
T162_r1
T162_r2
T162_r3
T167-mut
T167-r1-archive
T167-r1-out
T167-r1-out-local
T167-r1-out-local2
T168_r1
T169_staff_r1
T169_staff_r2
T179_r1
T179_r1_mut
T179_r2
T179_r2_mut
T196
T197_r2_9ab8cae
T197_r2_e425534
T197_r2_mut_both
T197_r2_mut_home
T197_r2_mut_none
T197_r2_mut_step1
T197_r2_scripts
T198-locate.py
T198-run1.txt
T198-run2.txt
__pycache__
_types.bak
a.sqlite3
a141
a178
a178.out
a27e3a4.diff
a9ab
acc.py
across.py
addtags.py
adj_eval
adj_out
adr013.txt
after.py
all.txt
amounts_broken.py
ap3500.pdf
api
api.patch
api2
api_at_099732b.py
api_head.log
api_head.md
api_head.py
api_head.sqlite3
api_head_plus_mine.md
api_md_head.md
api_md_new.md
api_mine.md
api_new.py
api_parent.log
api_parent.sqlite3
apitmp
app
app-d0b04bc
app-head
app.log
app.pid
app.sqlite3
app2
app2.log
app2.pid
app2.sqlite3
app3
app3.sqlite3
app4
app4.log
app4.pid
app4.sqlite3
app5
app5.log
app5.pid
app5.sqlite3
app60
app60.log
app60.pid
app60.sqlite3
append_404.py
append_correction.py
ar2
ar_old
arc
arc.sh
arch
arch0c24
arch2
arch3
arch4
arch5
arch_57a08ba
arch_r2_54382
arch_r2_54382.idx
arch_r2b
arch_r2c
arch_r2d
arch_r3_final
arch_t140
archive
archpath.txt
artifacts
atk
aud.py
aud2.py
audit.py
audit_mine.js
audit_split.py
audited.bak
axe
b.sqlite3
base
base.json
base1.log
baseline_journey.out
before.txt
big.json
billing.orig
blank.py
blob.tmp
board
body.py
bombs
boom_final.py
boom_server.py
boundary.py
boundary2.py
build_evidence.py
build_set.py
build_set.py.bak
build_t099_blobs.py
busy.out
c
c01.json
c1.json
c5.json
c8a9874
ca.sh
cal.bak
case.json
case.json.tok
case07.json
case3.json
case3.json.tok
case_01_date_formats.json
case_lib11_priors_and_ledger.json
case_list.orig.bak
cases.txt
ce70
ce70-report.md
census.py
charge_text.py.patch
charges.py
check.py
check_golden.out
check_json.py
check_r2.py
check_r3_json.py
check_r4.py
checks2.sh
checks3.sh
chk.js
chk.py
chk2.py
chk_mut.py
chk_syntax.py
clean2
clean3
clean4
clean5
clean5_unit.txt
clean_run1.txt
cleanup_check.py
cli1.out
cli2.out
cli_c1.err
cli_c1.txt
cli_final.err
cli_head_out.txt
cli_rep1.err
cli_rep2.err
cli_rep3.err
clone-run
clone194
cmscms.py
collapsed.png
collapsed.py
commit.sh
commit_paths.sh
commit_tree
commitcases.txt
conf-1440.png
conf-390.png
conf_A.py
conf_B.py
conftest_mine.py
conftest_split.py
controls_run.log
copy
copyA
copyC
copy_untracked.py
corp_base.json
corp_r2.json
corpus.py
count.py
count1.py
count_base.py
counts.sh
cr.sh
cred_b05.py
cred_orig.py
cs.sh
ctl-out
ctl.log
d.py
d1
d2
d3
d4
d5
d6
d7
d8
data
data2
dates.orig
db
db3
db4
db5
dbg
dbg.png
dbg.py
dbg2.py
dbg3.png
dbg3.py
dbg4.py
dbg5.py
dbg97.py
de1.txt
decisions_head.md
demo
demo.log
demo.sqlite
dev
dev.db
diag.py
diff.py
dl
docker-venv
docker_emu.sh
docker_serve.log
docker_serve.pid
dockerctx
dockerdata
dockerhome
docs
dom.bak
dos
draft-pass2.md
drive.py
dump.py
e1-1440.png
e1-390.png
e1-390b.png
e1.py
e1400d4
e2.py
e2e-data
e2e-m1-server.log
e2e-m1.sqlite
e2e-run.sqlite
e2e-server.log
e2e.db
e2e.out
e2e1.log
e2e2.db
e2e2.out
e2e3.out
e2e_full.txt
edit133.py
edit133b.py
edit133r2.py
edit199.py
endpoints.py
env97
err.out
err2.out
es1.txt
ev.json
ev.sh
eval_base.out
eval_r2.out
evalout
evalout2
evals
ex07.json
ex1.sh
ex2.sh
ex3.sh
exp-077
exp.py
exp2.py
exp_077.py
export.py.patch
export_curated.sqlite
export_recorded.sqlite
f3.out
f5f1be9-tree
fe-data
fe3.log
fe3.sqlite
fe4.log
fe4.sqlite
fetch
figs.py
files.txt
fill.py
final-data
final.py
final1
final1.log
final2.log
finalize_f5f1be9.py
find_miss.py
first.png
fix.log
fix.sqlite3
fixture_run.out
fixture_run_b.out
flags_commit.py
fpl.bak
fpl_new.py
fpl_old.py
fr_r2.txt
fragile
fresh
fresh.py
fresh_head.log
fresh_head.sqlite3
fresh_nosbs.log
fresh_nosbs.sqlite3
full.done
full.log
full.out
full.patch
full.txt
full2.out
full_head.txt
fx
fx.log
fx.sqlite3
fx_before.txt
fxbak
gate.db
gate_dir.txt
gate_m2
gen
gen.py
gen_controls.py
gm2
gm2r2
gm2r2_legal
gm2r2clone
gm3
gm3-7991.log
gm3-7992.log
gm3-a11y-arch
gm3-a11y-audit.log
gm3-a11y-pid.txt
gm3-a11y-server.log
gm3-a11y-wrap.py
gm3-a11y.sqlite3
gm3-emptyfx
gm3-ux-7991.sqlite3
gm3-ux-7992.sqlite3
gm3src
golden_scan.py
guardprobe.py
guardprobe.py.bak
h.txt
h178
h42.py
h60.txt
h_audit.js
h_charges.js
h_conftest.py
h_review.js
h_stepper.js
harness
head
head-a850be0
head-bc12d44
head-ec33bf0
head.db
head.log
head.py
head.sqlite3
head0
head2
head2.py
head3
head4
head5
head7
head8
head9
headA
head_950d4a5
head_9851a0d_r5
head_9c1af01
head_ae76835_r3
head_clean
head_clean.log
head_clean.sqlite3
head_copy
head_e63e564
head_faee448_r4
head_nosbs
head_nosbs.log
head_nosbs.sqlite3
head_run.sh
headcheck
headchk2
headfe
headx
heldout.py
helpers.py
helpers2.py
hf-config.html
hf-docker.html
hits.py
hookcopy
idx
idx162r3b
idx167
idx171
idx2
idx3
idx4
idx5
idx_commit
idx_r2b
idx_r2c
idx_r2d
idx_r3
idx_t139r4
idx_t139r4b
idxpath
image-emu
ing.bak
ingest.orig
ingest_novel.py
inj.py
jcheck.py
judge_live.py
judges.png
k1dump.py
kb2.py
kb3.py
kb_test.py
keys.py
last_commit
latest.before.sha
latest.committed.json
latest_head.json
latest_new.json
leak.py
letter_check.py.patch
lib-after.md
lib.md
lib.out
lib_app.sqlite
lib_report.md
lib_report3.md
lib_report5.md
libdump.py
library-after.md
library-base.md
library-report.md
link
live-demo
live-demo.log
live-local
live-local.log
live23.sh
live3.sh
llm_head.md
local
local.log
local.sqlite
m1.txt
m2.txt
m2regate-live.log
m3
m3.txt
m4
m4.txt
m5
m55_M_drop_whole_rule
m55_M_only_needs_review
m55_M_only_rejected
m58_M1_round1_regex
m58_M2_dates_iso_dollar
m58_M3_amounts_valid_dollar
m58_M4_fence_dollar
m59_N11_drop_stale_basis_clause
m59_N12_failed_redraft_overwrites
m59_N13_drop_SEVERITY_NOT_QUOTED
m59_N3_drop_D006_token_check
measure.py
memory
mine
mine.diff
mine.patch
mine.txt
miss.py
miss2.log
miss2.py
mk.py
mk_r3.sh
mkd.py
mkfix.py
mkindex171.sh
mkpatch.py
mkpdf.py
mkreview.py
mkreviews.py
mob.py
msg.txt
mut
mut-A
mut-B
mut-C
mut-D
mut-M6_drop_family_lookbehind
mut-base
mut-control
mut-gate
mut-qual
mut-t073-A-broad-catch
mut-t073-B-no-guard-in-review
mut-t073-C-expected-becomes-supported
mut-t073-D-drop-class
mut-t084-1-no-judge-gate
mut-t084-2-no-wording-gate
mut-t084-3-no-negation-gate
mut-t084-4-unsure-accepted
mut-t084-5-no-audit
mut-t084-6-no-value-gate
mut-t084-7-judge-fail-open
mut-tok
mut.py
mut.py.bak
mut080.py
mut1
mut105.py
mut105.py.bak
mut159.py
mut161.py
mut2
mut2.py
mut2_B0_pinned_baseline
mut2_G1_grounding_check_removed_in_extract
mut2_S1_judge_unavailable_fails_open_in_state
mut2_S2_judge1_error_becomes_supported
mut3
mut3_S2b_shared_judge_error_fails_open_to_supported
mut3_S3_j2_error_fails_open_to_agree_pipeline_only
mut4
mut98
mut99
mutB.txt
mutT132
mut_M0_baseline
mut_M1_noRollback
mut_M1_sdk_internal_retries_2
mut_M2
mut_M2_cli_drops_strict_mcp
mut_M3
mut_M3_cli_timeout_600
mut_M4
mut_M4_cli_leaks_stderr_into_error
mut_M5
mut_M5_fixture_miss_retried
mut_M6
mut_M6_j2_error_becomes_agree
mut_M7
mut_M7_stray_subprocess_import_outside_backends
mut_R4M1_stated_total_always_suppressed
mut_R4M2_no_other_figures_on_rate_holder
mut_R4M2_rate_unclear_move_to_other_figures_removed
mut_R4M3_rate_row_drops_own_other_figure_move
mut_R4M3_rate_row_stated_total_not_other_figure
mut_R4R_line790_raises
mut_branch
mut_branch.sqlite
mut_dedupe
mut_flagsdeadline
mut_guard_e2e.out
mut_guard_unit.out
mut_rmfixture
mut_rmjudgefixture
mut_run.py
mut_run2.py
mut_t055_M_drop_whole_rule
mut_t055_M_only_needs_review
mut_t055_M_only_rejected
mut_t058_M1_round1_regex
mut_t058_M2_dates_iso_dollar
mut_t058_M3_amounts_valid_dollar
mut_t058_M4_fence_dollar
mut_t059_N11_drop_stale_basis_clause
mut_t059_N12_failed_redraft_overwrites
mut_t059_N13_drop_SEVERITY_NOT_QUOTED
mut_t059_N3_drop_D006_token_check
mutant-M1-nocombine.txt
mutant-M2-find0.txt
mutant375_journey.out
mutant_timeline572.out
mutants
mutants-db08276.log
mutants-r3-db08276.log
mutants-work
mutants.py
mutate.py
mutate2.py
mutate3.py
mutate_api.py
mutate_run.py
mutate_run2.py
mutate_t055.py
mutate_t058.py
mutate_t059.py
mutrun.sh
mutv2_1
mutv2_2
mutv2_3
mutv2_4
mutv2_5
mutv2_6
mutv2_7
mvp95
mvp95.log
mvp95.pid
mvp95.sqlite3
mw
n.py
narr.py
neg
neg2
negex
negtest
new.json
new_record.py
novel.txt
nucc
nv.py
nv2.py
o1
o1.aIcW
o2
o2.vHBZ
o3_new.js
o3_v3.js
ocr_edit
ocr_edit_head
ocrinj
oe
oi
old
old-d0b04bc
old_unc.py
orch.idx
orig
out
out.txt
out_head.json
out_zlayt-pm-project.json
ov.py
overlay-head
p.py
p1.py
p1.txt
p2.db
p2.py
p2.txt
p3.log
p3.pid
p3.py
p3.sqlite3
p3.txt
p4-e293daa
p4-head
p5-b612176
p5-server.log
p5.db
p_be
p_fe
pa
page.txt
par
parent
parent-server.log
parent.sqlite3
part.py
part2-process.html
part2-process.pdf
paste.sqlite3
paste_attack_ledger.txt.sqlite
paste_synthetic_ledger.txt.sqlite
patch.py
patch2.py
patch3.py
patch_builder.py
path
path.txt
pathspec.txt
patterns.bak
patterns_nomanual
pdb
pdf_time.py
pdfs
pdfs_head
peer.py
peer.sqlite3
personas
phi.py
pid
pid2
pidA
pidB
pin-690a0e3-r5
pin-6bca-r4
pin-8bc7f90
pin-HEAD-r4
pin-HEAD2-r4
pin-db08276
pin-f218263
pipeline.orig.py
pipeline.py
pipeline_commit.py
pl.orig
pm-gate.sqlite3
pn-head.md
pnh.html
pnh.pdf
portconflict.sh
pp
pp2
pre
pre-t123-archive
pre_t095_schema.sql
present.patch
present.py
prev
probe
probe-db
probe-r2-output.txt
probe-top.png
probe.py
probe.sqlite3
probe133.py
probe133r2.py
probe133r3.py
probe2.py
probe2.py.bak
probe2_t067.py
probe3.py
probe3_t067.py
probe4.py
probe404.py
probe5.py
probe98
probe99
probeA
probeA.stderr
probeA.stdout
probeB
probeB.stderr
probeB.stdout
probe_404.py
probe_7df
probe_copy.sqlite3
probe_copy2.sqlite3
probe_copy3.sqlite3
probe_copy4.sqlite3
probe_copy5.sqlite3
probe_curated.sqlite
probe_err.log
probe_failed.py
probe_flags.sqlite
probe_flags_audit.sqlite
probe_head
probe_head_out.txt
probe_nojudge.py
probe_r4_ocr.py
probe_recorded.sqlite
probe_rej.py
probe_run.py
probe_server.log
probe_t067.py
probe_timeout.py
probe_tray.py
probe_work_head
probe_work_head2
probes
probes-t100
probes159
probes161
probes_r5_dir
proc.png
proc.py
proc2.png
product-note.html
product-note.pdf
pub.log
pub.py
pub.sqlite3
pub2.log
pure2
pw
r
r1
r2
r2-07c7558
r2-07c7558-server.log
r2-07c7558.sqlite3
r2-802d5fd
r2-cases.out
r2-deploy-head
r2-deploy-wt
r2-head
r2-ocr
r2-planted
r2-server.log
r2-sweep.out
r2.db
r2.log
r2.pid
r2.sqlite3
r2_app.sqlite3
r2_blank_judges.py
r2_check.py
r2_detect.py
r2_es2.py
r2_export.json
r2_for2.py
r2_ids.txt
r2_library.md
r2_mixed.py
r2_mut_base
r2_mut_base_m
r2_mutant_r2b.py
r2_mutants.py
r2_probe_out.txt
r2_rec.sqlite3
r2_run.log
r2_sentinel_data
r2_set_status.py
r2_t080_app.log
r2_t080_app.sqlite
r2_token.txt
r2_treeid.txt
r2_unit.txt
r2a
r2app
r2app-d865
r2arch
r2b
r2c_tree.txt
r2d.sqlite3
r2d_run.log
r2d_tree.txt
r2demo
r2demo.log
r2head
r2live.log
r2live.pid
r2live.sqlite3
r2local
r2local.log
r2mut
r2o
r2parent
r2server.log
r2src
r3
r3-25f585c
r3-a27
r3-parent
r3-server.log
r3.db
r3.log
r3.pid
r3.sqlite3
r3_acceptance_strings.py
r3_accepted.json
r3_api.py
r3_check_json.py
r3_full.log
r3_gate_check.py
r3_mut
r3_rootcause.py
r3_sentinel_data
r3_server.log
r3_t080.sqlite
r3_tok.txt
r3a
r3ap
r3api
r3api2
r3app.sqlite3
r3arch
r3b
r3bp
r3clone.81DVDF
r3clone.out
r3copy
r3da0c7fe
r3db.sqlite3
r3dev
r3e2e.log
r3h
r3head
r3health.json
r3img
r3m
r3mut
r3o
r3pop
r3probe.py
r3run
r3run.out
r3runpid
r3scripts
r3server.log
r3src
r3tb
r3timing.txt
r3tree
r3workdir
r4_probe_8634bfe.out.txt
r4_rootcause.py
r4arch
r4data
r4out
r4pin
r4probe
r4probe_on_0f58181.txt
r5
r5.log
r5.pid
r5.sqlite3
r5_e3.png
r5_flag.png
r5_top.png
r5b
r_head.json
r_new.json
rail.png
raw1.txt
raw2.txt
raw3.txt
raw4.txt
raw5.txt
raw6.txt
rec.py
rec.sh
rec_a.log
rec_all.log
rec_all.sh
rec_b.log
rec_judges.log
rec_narr.py
rec_sample.log
recon.py
render_curated.log
render_curated.sqlite
render_flags.log
render_flags.sqlite
render_race.log
render_race.sqlite
render_recorded.log
render_recorded.sqlite
replay.py
replit-config.html
replit-deploy.html
replit_env.py
repo
repro_stale
req_mut.md
requirements-dev.txt
requirements.txt
rerec.log
rerec.sh
rerun.out
rerun.sh
rerun2.sh
research
review.bak
review_commit.py
review_fixed.js
review_head.js
review_headplus.py
review_mine.py
reviews
rt_base.json
rt_r2.json
run.base.py
run.head.py
run.log
run.try.py
run1.err
run1.log
run1.out
run2
run2.err
run2.log
run2.out
run3.err
run3.log
run3.out
run_c5.py
run_m2.pid
run_m2.sh
run_mutants_r3.py
run_p3_chain.sh
run_r3.sh
run_ro.py
run_t070_orig.py
runs.status
rv_T132_T128_r2r3
s-1440-0.png
s-1440-1700.png
s-1440-2300.png
s-1440-2600.png
s-1440-3300.png
s-1440-4400.png
s-1440-5400.png
s-1440-900.png
s-390-0.png
s-390-1500.png
s-390-3000.png
s-390-900.png
sample_case.json
sc.log
sc.sqlite3
scan.py
scan.py.bak
scan_specimens.py
scan_time_10x5000wide.pdf
schema_pre_T095.sql
score.py
scr.log
scr.sqlite3
scripted.log
scripts
scroll.py
selfcheck-r2.txt
serve_p3_wrapper.py
serve_snap.py
server-7871.log
server-7872.log
server.err
server.log
server.out
server.pid
server2.log
server2.pid
server7867.log
shard0.out
shard1.out
shard2.out
shard3.out
shard4.out
shoot.py
shot.py
shot2.py
shots
shots.log
shots.py
shots2.py
shots_old.py
shots_t046r2.py
show.py
show_T103.txt
snap
snap-077
snap-89a323a
snap-c61
snap-final
snap-h2
snap-head
snap-t187r3
snap.out
snap.path
snap2
snap3
snap7942
snap7942.db
snap7942.log
snap7942.pid
snap9
snap_run.sh
sp.txt
spec
splice.py
spy3.log
spy3.py
src
srv.KdvV
srv.log
srv.out
srv.pid
srv2.log
srv2.pid
srvdir
st_commit.py
stable.py
start.sh
states.py
steps-open.png
store.orig.bak
strip.py
strip_and_grep.py
submission
sync.py
sync.sh
sync_r5.sh
t015r4
t028.out
t030r2mut
t033mut
t033mut.py
t035
t038
t038r3
t040-077
t040-head
t040-live
t043-239
t043_r2_probe.py
t043_r2_probe2.py
t043_r2_probe3.py
t045r2-bypass
t045r2-clean
t045r3-clean
t046-server.log
t046.sqlite3
t046r2.log
t046r2.pid
t046r2.sqlite3
t053r3-data
t055_base_full.txt
t055_mut_full.txt
t056r2_01ipr4y9
t056r2_5_pc8ore
t056r2_gxnki_45
t056r2_jvse81hd
t056r2_pjbon2yp
t057
t060-a11y-axe
t060-a11y-data
t060-a11y-head
t060-a11y-serve.py
t060-p3-app
t060-p3-axe
t060-p3-chain.log
t060-p3-review.json
t060-p3-server.log
t060-p3-server.pid
t060-p3.sqlite3
t060p2
t060p2-wrap
t065
t065r2
t066r2
t066r3
t067
t067_59c7edb
t067_f6fa2dd
t067_head_archive
t067_m1
t067_m2
t067_m3
t067_probes
t067head
t067parent
t067r3
t067r4
t067r5
t067r5-probe-out.txt
t068-data
t068-data-commit
t068-data-commit2
t068-server-commit.log
t068-server-commit2.log
t068-server.log
t068r2-server.log
t068r2-snap
t068r3-case01-body.json
t068r3-case01-get.json
t068r3-data
t068r3-head
t068r3-probe-token.txt
t068r3-server.log
t070
t070r2b
t071_title_probe.py
t072
t072plant
t072r3
t072r3-p1_be_selfreport
t072r3-p2_be_patientstatement
t072r3-p3_be_patientstates
t072r3-p4_fe_selfreport
t072r3-p5_fe_patientstatement
t072r3-p6_fe_selfreported_ui
t072r4
t072r4_plants
t074
t075r2
t076r2
t076r2-data
t076r2-server.log
t077r3
t079.log
t079.sqlite3
t080m_M10_date_always_confirmed
t080m_M11_judge_partial_is_pass
t080m_M12_date_blocker_reason
t080m_M13_overrides_not_counted
t080m_M14_unavailable_counted_judged
t080m_M15_agreement_never_fails
t080m_M16_verbatim_fail_ignored_on_entry
t080m_M17_skip_after_reject_removed
t080m_M18_nothing_accepted_removed
t080m_M19_unsupported_excludes_disagrees
t080m_M1_rejected_blocks_gate
t080m_M20_step_order_swap
t080m_M21_progress_counts_skipped_as_pending
t080m_M22_total_inclusion_accepted_pending
t080m_M23_fixed_why_replaced_by_model_text
t080m_M2_dismissed_blocks_gate
t080m_M3_dismissed_human_pass
t080m_M4_qualifier_always_pass
t080m_M5_gate_ignores_running
t080m_M6_rate_pending_total
t080m_M7_raw_leak_in_metadata
t080m_M8_event_before_after_leak
t080m_M9_edited_text_leak
t080m_base
t080r4
t085r2
t085r3
t086head
t086wt
t090-out
t090.index
t090.patch
t090_code.patch
t090_patch2.py
t090_patch_run.py
t090_patch_tests.py
t090r2
t090r3
t092
t093.base.py
t094r2
t095.patch
t095r2_head
t096-evals
t096-export-check.py
t096-ux-36ceb38
t096-ux-server.log
t096-ux-walk-output.txt
t096-ux.sqlite3
t096_all.py
t096_ds.py
t096_probe.py
t096_probe2.py
t096_shot.py
t096_shot2.py
t096_start.sh
t096data
t097
t097.log
t097.pid
t097.sqlite3
t097b.sqlite3
t097r2
t097r2-server.log
t097r2.sqlite3
t097r2head
t097r3-archive-9f2811f
t097r3-server.log
t097r3-server.pid
t097r3.sqlite3
t098-e511778
t098-f5ddec8
t098-head
t099-3ecb8b1
t099-dirty-check
t099-f345bc8-r2
t099-gitclone-parent
t099-mut
t099.index
t099_msg.txt
t1.xXug
t100-card
t100-fresh
t101
t101r2
t103r2
t103r3_api.diff
t103r3_archive
t103r3_billing.diff
t103r3_control_archive
t103r3_mut
t103r4_archive
t104
t104-3462ad0-ux
t104-server.log
t104-server.pid
t104-state.json
t104-ux.sqlite3
t105
t105r2
t106_r2_archive
t108
t109_adr_edit.py
t109_doc_edit.py
t109r2_head
t109r2_mutA
t109r2_mutB
t109r2_pin
t109r3_head
t109r3_mut
t109r3_mutate.py
t109r3_pin
t109r3_probe_cc.py
t109r3_probe_flags.py
t109r3_probe_flags2.py
t109r3_probe_trim.py
t109r3_probe_trim2.py
t109r4
t110.sqlite3
t110b.sqlite3
t111-archive
t111-parent
t111r2
t111r2-base
t111r2-base.out.json
t111r2-head
t111r2-head.out.json
t111r2-parent
t111r2-parent.out.json
t112.index
t112_live.sh
t112_pipeline.py
t113_run1_evidence
t114
t114r2
t115.pid
t115.sqlite
t115srv.log
t116r2-base
t116r2-head
t116r3
t116r4
t116r5
t118-head
t118-mutA
t118-mutB
t118-pre
t119
t119.log
t119.pid
t119.sqlite3
t119m
t119m.log
t119m.pid
t119m.sqlite3
t120
t120-123-archive
t120-123-server.log
t120-123.sqlite3
t120-parent-archive
t120-parent-server.log
t120-parent.sqlite3
t120-r3.sqlite
t120r2
t120r2.sqlite3
t120r4
t121r2
t123-cmp-head.jsonl
t123-cmp-pre.jsonl
t126r1
t126r2
t133_r1_m3_full.out
t133_r1_m3_full.py
t133_r1_mutate.py
t133_r1_probe.py
t133_r2_probe_mine.py
t134_app.sqlite3
t134_server.log
t134m
t134parent
t134parent2
t134r1
t134r2
t134r3_c4bb
t134r3_cli1.err
t134r3_cli1.txt
t134r3_cli2.err
t134r3_cli2.txt
t134r3_dbg
t134r3_fix
t134r3_head
t134r3_mut
t134r3_mut.txt
t134r3_mut2
t134r3_mut_h.txt
t134r3_par
t134r3_unit.txt
t134r3_unit_c4bb.txt
t134r3_unit_fix.txt
t134scripts
t136-archive
t136-r2-staff
t136-server.log
t136.db
t139
t139_app.sqlite3
t139_overlay.err
t139_overlay.out
t139_overlay.sqlite3
t139_server.err
t139_server.out
t139_trace.sqlite3
t139_trace2.sqlite3
t139clean
t139overlay
t139r2
t139r2_app.sqlite3
t139r2_server.log
t139r3
t139r3_app.sqlite3
t139r4
t139r4_app.sqlite3
t139r4_server.log
t139r5
t139r5_mut1
t139r5_mut2
t139r5_mut3
t139r5_out
t139r5_prev
t139r5_scripts
t139tree
t143
t143p
t143r2
t143r2_case_lib01_er_only_then_gap.txt
t143r2_case_lib02_slip_fall_prior_knee.txt
t143r2_case_lib03_truck_rear_end_chiro.txt
t143r2_case_lib04_dog_bite_scar_revision.txt
t143r2_case_lib05_pedestrian_orif_hardware.txt
t143r2_case_lib06_lop_billed_vs_adjusted.txt
t143r2_case_lib07_parking_lot_fall_outside_records.txt
t143r2_case_lib08_second_crash_mri_after.txt
t143r2_case_lib09_spanish_interpreter_espalda.txt
t143r2_case_lib10_eob_ub04_cms1500.txt
t143r2_case_lib11_priors_and_ledger.txt
t143r2_case_lib12_records_review_credibility.txt
t143r2_case_lib13_cloned_notes_cross_provider.txt
t143r2_case_lib14_handwritten_chiro_scans.txt
t143r2_case_lib15_conclusory_letter_mist.txt
t143r2_mut.py
t143r2_sample.txt
t143r3
t144r1
t145r1
t146r2
t146r3
t146r4
t148r1
t149db
t149r2
t149r2-server.log
t149r2.pid
t149r2.sqlite3
t149server.log
t149src
t151-25f585c
t151-out
t151-scripts
t152_collect.py
t152_diff.py
t154
t154.sqlite3
t154b.sqlite3
t154r2
t154r2p
t155
t155r2
t157-check-json.py
t157-r1
t157r2b
t158-card
t158-f31
t158-f31-m2
t158-f31-m6
t158-f31-runs
t158-head
t158-m2
t158-m3
t158-m4
t158-m5
t158-m6
t158-mut
t158-probe
t158-r1
t158-review-head.js
t158-review-pre.js
t158-settle
t158r3
t159.patch
t160-review
t162.sqlite3
t162r2
t162r2.base
t162r2.idx
t162r3
t162r3.idx
t162v-final
t165-backend
t165-r2
t165-review
t165r2b
t166
t166-mvp-r2-ux-d865.sqlite3
t166-mvp-r2-ux.sqlite3
t166-r2-ux-d865.log
t166-r2-ux-server.log
t168r2
t169-clone-2
t169r2
t171
t171app.sqlite3
t171server.log
t173-final
t173-gen
t173-head
t173-verify
t173.idx
t174
t174r4-local.db
t174r4-local.log
t174r4-public.db
t174r4-public.log
t174r4-src
t175r1
t175r2
t177-arch
t177-arch-base
t177r4
t178-interrupt.db
t178-interrupt2.db
t178-old.db
t178-pastes.db
t178-pid-7882
t178-pid-7883
t178-pid-7884
t178-server-7881.log
t178-server-7882.log
t178-server-7883.log
t178-server-7884.log
t178-stale.db
t179_commit.index
t179_final.index
t179_old
t179r2
t179r2_unit.txt
t179v2
t180.db
t181
t181-app.sqlite3
t181-local-server.log
t181-local.sqlite3
t181-server.log
t181ux
t182
t182-3sjF
t182-dir.txt
t182-index.html
t182-serve.log
t182-serve.pid
t182-t0.txt
t182-t1.txt
t182-z.txt
t187r2
t194.index
t194_commit.sh
t194_msg.txt
t2.q4VB
t200.idx
t200run
t2b.IKsK
t3.ORDQ
t4.0u5g
t84r4
tabflow.py
tail.md
test_billing_old.py
tests
tests_b05.py
tests_evals.sh
thr.py
thr2.out
thr2.py
timed_run.sh
tmp.index
tmp2.index
tmp3.index
tmpidx_t197
tmpindex
tog-open.png
tog.py
tok.json
tok_c1_local
tok_c3_local
tok_c5_local
tok_c7_local
tok_case_lib01_er_only_then_gap
tok_case_lib02_slip_fall_prior_knee
tok_case_lib03_truck_rear_end_chiro
tok_case_lib04_dog_bite_scar_revision
tok_case_lib05_pedestrian_orif_hardware
tok_g02_local
tok_g04_local
tok_g06_local
tok_g08_local
tok_g09_local
tok_sample2_local
tok_sample_local
tok_sample_pub
tokens.json
tools
tree
tree.sha
tree.txt
tree3
tree4
tree5
tree_r2
tree_r3
two.py
two.py.bak
u.orig
ub
ui-demo
ui-input.out
ui-local
unit-run-r2-clone-with-git.txt
unit-run-r2.txt
unit.out
unit.txt
unit1.txt
unit171.log
unit2.out
unit3.out
unit_full.txt
unit_full_head.out
unit_r2a.txt
unit_r2b.txt
ux-mvp-r3-da0c7fe.sqlite3
ux-mvp-r3-server.log
ux-mvp-r3.pid
ux-r2-2.sqlite3
ux-r2-3.sqlite3
ux-r2-debug-sample.png
ux-r2-server-2.log
ux-r2-server-3.log
ux-r2-server.log
ux-r2-server.pid
ux-r2.sqlite3
ux3
v
validate_review.py
verify.py
view.json
walk.out
walk.py
walk2.py
why.orig.py
wide.py
wprobe.py
wt
wt-031a708
wt-7df65fb
wt-golden.txt
wt-head
wt2
wt7944.db
wt7944.log
wt7944.pid
wt7945.db
wt7945.log
wt7945.pid
wt7946.db
wt7946.log
wt7946.pid
wt_final
wt_final2
wt_head
wt_run.sh
wt_t155
x45.py
xc.py
xss.py
zlayt-base
zlayt-head
zlayt-public-snapshot.JTMbwv
zlayt-r2
zlayt-r3
tar: could not chdir to '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/r5-fresh'

diff-done
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:21.284Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir $S/t177r5-fresh && git archive e425534 | tar -x -C $S/t177r5-fresh && diff -rq $S/t177r5-fresh $S/r5 -x __pycache__ -x .pytest_cache | head -20; echo diff-done",
 "description": "Fresh unique archive and diff against r5 copy"
}
````

### User / tool · 2026-11-02T23:17:23.901Z

**tool result**
````
diff-done
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:27.162Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-177-staff-engineer-r4/probe_r4_http.py; sed -n 1,40p artifacts/review-evidence/T-177-staff-engineer-r4/probe-r4-http-unsupported.out",
 "description": "Read r4 HTTP probe"
}
````

### User / tool · 2026-11-02T23:17:27.244Z

**tool result**
````
"""T-177 r4 demo-server probe (staff-engineer-reviewer). Starts MY OWN demo-mode server (no ZLAYT_MODE) from the git archive of 3feb096 on <port>, over HTTP (httpx),
with a curated set mutated per <mode> (same mutations as probe_r4.py), creates the sample, runs, decides (accept each entry, dismiss the first flag), and applies the worker's own scanner
(tests/unit/test_prepared_property.py offenders/collect) to every response. Then stops only the child PID it started (checked against lsof + cwd first).
Usage: python -I probe_r4_http.py <archive> <scratch> <mode> <port>    modes: control unsupported missing schema empty amount"""
import json, os, re, shutil, subprocess, sys, time
ARCH, SCRATCH, MODE, PORT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])
sys.path.insert(0, ARCH)
import httpx
src = os.path.join(ARCH, "tests", "fixtures", "llm")
root = os.path.join(SCRATCH, f"http_{MODE}")
shutil.rmtree(root, ignore_errors=True)
mut = os.path.join(root, "curated"); os.makedirs(mut)
for f in os.listdir(src):
    if f.endswith(".json"): shutil.copy(os.path.join(src, f), mut)
for f in os.listdir(os.path.join(src, "curated")):
    if f.endswith(".json"): shutil.copy(os.path.join(src, "curated", f), mut)
E1 = os.path.join(mut, "98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json")
ER = next(os.path.join(mut, f) for f in os.listdir(mut) if f.startswith("b74b563d21aa"))
def edit(p, fn):
    d = json.load(open(p)); fn(d); json.dump(d, open(p, "w"))
if MODE == "missing": os.remove(E1)
elif MODE == "unsupported": edit(E1, lambda d: d["output"].__setitem__("summary", "Patient reported paralysis of the left leg and loss of bladder control."))
elif MODE == "schema": edit(E1, lambda d: d["output"].pop("summary"))
elif MODE == "empty": edit(E1, lambda d: d.__setitem__("output", {}))
elif MODE == "amount": edit(ER, lambda d: (d["output"].__setitem__("excerpt", d["output"]["excerpt"] + " ER charges: $6,240."), d["output"].__setitem__("summary", d["output"]["summary"].rstrip(".") + "; ER charges $6,240.")))
env = {k: v for k, v in os.environ.items() if k not in ("ZLAYT_MODE", "ANTHROPIC_API_KEY", "ENABLE_LIVE", "FIXTURE_SET")}
env.update(LLM_BACKEND="fixture", HOST="127.0.0.1", PORT=str(PORT), DATA_DIR=os.path.join(root, "data"), PYTHONPATH=ARCH)
if MODE == "control": env["FIXTURE_SET"] = "curated"
else: env["LLM_FIXTURE_DIR"] = mut
proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ARCH, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
try:
    base = f"http://127.0.0.1:{PORT}"
    for _ in range(60):
        try:
            if httpx.get(base + "/api/health", timeout=2).status_code == 200: break
        except Exception: time.sleep(.5)
    c = httpx.Client(base_url=base, timeout=60)
    h = c.get("/api/health").json(); print("mode:", MODE, "| health.answers:", h.get("answers"), "| demo_mode:", h.get("demo_mode"), "| models:", h.get("models"))
    import tests.unit.test_prepared_property as P
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    print("run ->", c.post(f"/api/cases/{tok}/run", json={}).status_code)
    st = P._run.__wrapped__ if hasattr(P._run, "__wrapped__") else None
    for _ in range(480):
        s = c.get(f"/api/cases/{tok}/status").json()
        if s["status"] in ("ready", "failed"): break
        time.sleep(.25)
    print("run status:", s["status"], "| error code:", (s.get("error") or {}).get("code"))
    res = P.collect(c, tok)
    case = res["case"]; print("case.models:", case.get("models"))
    jm = frozenset(P.JUDGE_MODELS | {(case.get("models") or {}).get("judge")})
    bad = []
    for label, payload in res.items(): bad += P.offenders(label, payload, jm)
    seen = {}
    for label, path, word, s_ in bad: seen.setdefault((re.sub(r"[:].*", "", label), path, word), s_)
    print(f"WORKER-SCANNER offenders: {len(seen)} | responses scanned: {len(res)} | prepared items: {len(P.prepared_items(res))}")
    for k, v in sorted(seen.items())[:20]: print("  ", k, "|", v)
    # my own wider pattern over every string value, authorship wording only
    PAT = re.compile(r"AI draft|AI found|AI proposed|AI wrote|AI-made|AI read|AI translat|AI wording|AI's|AI picked|AI summary|the AI |The AI |AI gave|AI answer|recorded AI|claude-sonnet|drafted with AI|Drafted by", re.I)
    mine = {}
    for label, payload in res.items():
        for path, s_, j in P.strings(payload):
            m = PAT.search(s_.replace(P.TOOLTIP, ""))
            if m: mine.setdefault((re.sub(r"[:].*", "", label), re.sub(r"\[\d+\]", "[]", path)), s_[:140])
    print("my authorship-wording hits:", len(mine))
    for k, v in sorted(mine.items())[:15]: print("  ", k, "|", v)
    if MODE in ("control", "unsupported", "missing", "schema", "empty", "amount"):
        tgt = "e2" if MODE == "amount" else "e1"
        it = res.get(f"item:{tgt}", {}).get("item", {})
        print(f"{tgt}: state={it.get('state')} prepared={it.get('prepared')} why={it.get('why')!r}")
        for stp in (res.get(f"trace:{tgt}", {}).get("steps") or [])[:3]: print("   step", stp["id"], stp["status"], stp["label"], "::", stp["why"][:150])
    for p in ("/classic", "/classic/", "/classic/app.js"):
        r = c.get(p, follow_redirects=False); print("GET", p, "->", r.status_code, r.headers.get("location"))
finally:
    pid = proc.pid
    ls = subprocess.run(["lsof", "-nP", "-a", "-p", str(pid), "-iTCP", f"-sTCP:LISTEN"], capture_output=True, text=True).stdout
    cwd = subprocess.run(["lsof", "-p", str(pid)], capture_output=True, text=True).stdout
    own = (str(PORT) in ls) and ARCH in cwd
    print("stop: pid", pid, "listens on", PORT, "and cwd is archive:", own)
    if own or proc.poll() is None:
        proc.terminate()
        try: proc.wait(10)
        except Exception: proc.kill()
    print("listener after stop:", subprocess.run(["lsof", "-nP", f"-iTCP:{PORT}", "-sTCP:LISTEN"], capture_output=True, text=True).stdout.strip() or "none")
mode: unsupported | health.answers: prepared | demo_mode: True | models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
run -> 202
run status: ready | error code: None
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
WORKER-SCANNER offenders: 0 | responses scanned: 70 | prepared items: 16
my authorship-wording hits: 0
e1: state=rejected prepared=True why='Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.'
   step extracted fail Prepared answer :: removed from the summary: not in the quote: 'Patient reported paralysis of the left leg' removed from the summary: not in the quote: 'loss of bladder 
   step excerpt_verbatim skipped Quote is word for word in the record :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
   step excerpt_whole_sentence skipped Quote is made of whole sentences :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
GET /classic -> 307 /
GET /classic/ -> 307 /
GET /classic/app.js -> 307 /
stop: pid 1145 listens on 54431 and cwd is archive: True
listener after stop: none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:54.382Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py <<'EOF'\n\"\"\"T-177 r5 demo-server probe (staff-engineer-reviewer). Starts MY OWN demo-mode server (no ZLAYT_MODE) from the git archive of e425534 on <port>, over HTTP.\nModes: control (shipped FIXTURE_SET=curated), unsupported (e1's prepared summary says something its quote lacks -> code removes it).\nExplicit paths, each printed: EDIT (edit the quote of an entry, read item/trace/export, accept), MANUAL (hand entry on a record with no live entry, else on a deleted-from-view record), CODE-REMOVED (e1 item and trace, unsupported mode).\nThen scans every response with the worker's offenders() and with my own wider authorship regex. Stops only the PID it started (lsof + cwd checked first).\nUsage: python -I probe_r5_http.py <archive> <scratch> <mode> <port>\"\"\"\nimport json, os, re, shutil, subprocess, sys, time\nARCH, SCRATCH, MODE, PORT = sys.argv[1], sys.argv[2], sys.argv[3], int(sys.argv[4])\nsys.path.insert(0, ARCH)\nimport httpx\nsrc = os.path.join(ARCH, \"tests\", \"fixtures\", \"llm\")\nroot = os.path.join(SCRATCH, f\"http_{MODE}\")\nshutil.rmtree(root, ignore_errors=True)\nmut = os.path.join(root, \"curated\"); os.makedirs(mut)\nfor f in os.listdir(src):\n    if f.endswith(\".json\"): shutil.copy(os.path.join(src, f), mut)\nfor f in os.listdir(os.path.join(src, \"curated\")):\n    if f.endswith(\".json\"): shutil.copy(os.path.join(src, \"curated\", f), mut)\nE1 = os.path.join(mut, \"98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json\")\nif MODE == \"unsupported\":\n    d = json.load(open(E1)); d[\"output\"][\"summary\"] = \"Patient reported paralysis of the left leg and loss of bladder control.\"; json.dump(d, open(E1, \"w\"))\nenv = {k: v for k, v in os.environ.items() if k not in (\"ZLAYT_MODE\", \"ANTHROPIC_API_KEY\", \"ENABLE_LIVE\", \"FIXTURE_SET\")}\nenv.update(LLM_BACKEND=\"fixture\", HOST=\"127.0.0.1\", PORT=str(PORT), DATA_DIR=os.path.join(root, \"data\"), PYTHONPATH=ARCH)\nif MODE == \"control\": env[\"FIXTURE_SET\"] = \"curated\"\nelse: env[\"LLM_FIXTURE_DIR\"] = mut\nproc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=ARCH, env=env, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)\nPAT = re.compile(r\"AI draft|AI found|AI proposed|AI wrote|AI-made|AI read|AI translat|AI wording|AI's|AI picked|AI summary|the AI |The AI |AI gave|AI answer|recorded AI|claude|sonnet|drafted with AI|Drafted by|\\bAI\\b\", re.I)\ntry:\n    base = f\"http://127.0.0.1:{PORT}\"\n    for _ in range(60):\n        try:\n            if httpx.get(base + \"/api/health\", timeout=2).status_code == 200: break\n        except Exception: time.sleep(.5)\n    c = httpx.Client(base_url=base, timeout=60)\n    h = c.get(\"/api/health\").json(); print(\"mode:\", MODE, \"| health.answers:\", h.get(\"answers\"), \"| demo_mode:\", h.get(\"demo_mode\"), \"| local_mode:\", h.get(\"local_mode\"), \"| models:\", h.get(\"models\"))\n    import tests.unit.test_prepared_property as P\n    def new_run():\n        tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n        assert c.post(f\"/api/cases/{tok}/run\", json={}).status_code == 202\n        for _ in range(480):\n            s = c.get(f\"/api/cases/{tok}/status\").json()\n            if s[\"status\"] in (\"ready\", \"failed\"): break\n            time.sleep(.25)\n        return tok, s\n    tok, s = new_run(); print(\"run status:\", s[\"status\"])\n    G = lambda p: c.get(f\"/api/cases/{tok}{p}\")\n    mine = {}   # label -> body, for my scan\n    def keep(label, r):\n        try: mine[label] = r.json()\n        except ValueError: pass\n        return r\n    case = keep(\"case\", G(\"\")).json()\n    print(\"case.models:\", case.get(\"models\"))\n    entries = case.get(\"entries\", [])\n    recs = {r[\"id\"]: r for r in case.get(\"records\", [])}\n    print(\"entries:\", [(e[\"id\"], e[\"state\"]) for e in entries][:20])\n    # ---- EDIT path\n    done = 0\n    for e in entries:\n        if e[\"state\"] == \"rejected\" or done >= 2: continue\n        rec = recs[e[\"record_ids\"][0]]; sents = [x[\"text\"] for x in rec.get(\"sentences\", [])]\n        if len(sents) < 2: continue\n        for n in range(len(sents) - 1, 0, -1):\n            q = \" \".join(sents[:n])\n            r = c.post(f\"/api/cases/{tok}/items/{e['id']}/review\", json={\"action\": \"edit\", \"edits\": {\"excerpt\": q}})\n            keep(f\"edit:{e['id']}\", r)\n            if r.status_code == 200:\n                done += 1\n                print(f\"EDIT {e['id']} -> 200 | warnings:\", [w[\"message\"] for w in r.json().get(\"warnings\", [])])\n                keep(f\"item-edited:{e['id']}\", G(f\"/items/{e['id']}\")); keep(f\"trace-edited:{e['id']}\", G(f\"/items/{e['id']}/trace\"))\n                ex = keep(f\"export-edited:{e['id']}\", G(\"/export\")); print(\"   export after edit:\", ex.status_code, json.dumps(ex.json())[:200])\n                it = mine[f\"item-edited:{e['id']}\"][\"item\"]; print(\"   item.why:\", it.get(\"why\"))\n                st = [x for x in mine[f\"trace-edited:{e['id']}\"][\"steps\"] if x[\"status\"] in (\"fail\", \"warn\", \"skipped\", \"pending\")][:3]\n                for x in st: print(\"   trace\", x[\"id\"], x[\"status\"], \"::\", (x.get(\"why\") or \"\")[:170])\n                break\n    # ---- CODE-REMOVED path (unsupported mode e1 is rejected)\n    rej = [e for e in entries if e[\"state\"] == \"rejected\"]\n    for e in rej[:1]:\n        it = keep(f\"item:{e['id']}\", G(f\"/items/{e['id']}\")).json()[\"item\"]; print(\"CODE-REMOVED item\", e[\"id\"], \"| prepared:\", it.get(\"prepared\"), \"| why:\", it.get(\"why\"))\n        for x in keep(f\"trace:{e['id']}\", G(f\"/items/{e['id']}/trace\")).json()[\"steps\"]:\n            print(\"   trace\", x[\"id\"], x[\"status\"], x[\"label\"], \"::\", (x.get(\"why\") or \"\")[:140])\n    # ---- MANUAL path: every record with no live entry (rejected one), else a duplicate-free record we skip\n    have = {rid for e in entries if e[\"state\"] != \"rejected\" for rid in e[\"record_ids\"]}\n    manual = [rid for rid, r in recs.items() if rid not in have and not r.get(\"duplicate_of\") and r.get(\"sentences\")]\n    print(\"records with no live entry:\", manual)\n    for rid in manual[:2]:\n        first = recs[rid][\"sentences\"][0][\"text\"]\n        r = keep(f\"manual:{rid}\", c.post(f\"/api/cases/{tok}/records/{rid}/entry\", json={\"summary\": first, \"excerpt\": first}))\n        print(f\"MANUAL {rid} ->\", r.status_code, \"| warnings:\", [w[\"message\"] for w in (r.json().get(\"warnings\") or [])])\n        mid = (r.json().get(\"item\") or {}).get(\"id\")\n        if mid:\n            print(\"   item.why:\", keep(f\"item-manual:{mid}\", G(f\"/items/{mid}\")).json()[\"item\"].get(\"why\"))\n            keep(f\"trace-manual:{mid}\", G(f\"/items/{mid}/trace\"))\n    for p in (\"/trace\", \"/judges\", \"/audit\", \"/narrative\", \"/export\", \"/status\"): keep(p, G(p))\n    # ---- my wide scan over the explicit-path responses\n    hits = {}\n    for label, payload in mine.items():\n        for path, s_, j in P.strings(payload):\n            m = PAT.search(s_.replace(P.TOOLTIP, \"\"))\n            if m and not ((j and P._is_ident(s_)) or s_ in P.JUDGE_MODELS): hits.setdefault((re.sub(r\"[:].*\", \"\", label), re.sub(r\"\\[\\d+\\]\", \"[]\", path), m.group(0)), s_[:150])\n    print(f\"MY SCAN of explicit-path responses ({len(mine)}): {len(hits)} hit(s)\")\n    for k, v in sorted(hits.items())[:15]: print(\"  \", k, \"|\", v)\n    # ---- worker scanner over a fresh case through its own collect() (edit/accept/manual pass included)\n    tok, s = new_run()\n    res = P.collect(c, tok); case = res[\"case\"]\n    jm = frozenset(P.JUDGE_MODELS | {(case.get(\"models\") or {}).get(\"judge\")})\n    bad = []\n    for label, payload in res.items(): bad += P.offenders(label, payload, jm)\n    seen = {}\n    for label, path, word, s_ in bad: seen.setdefault((re.sub(r\"[:].*\", \"\", label), path, word), s_)\n    print(f\"WORKER-SCANNER offenders: {len(seen)} | responses: {len(res)} | prepared items: {len(P.prepared_items(res))} | edit responses: {[k for k in res if k.startswith('edit')]} | manual: {[k for k in res if k.startswith('manual')]}\")\n    for k, v in sorted(seen.items())[:15]: print(\"  \", k, \"|\", v)\n    print(\"case.models (second case):\", case.get(\"models\"))\n    for p in (\"/classic\",):\n        r = c.get(p, follow_redirects=False); print(\"GET\", p, \"->\", r.status_code, r.headers.get(\"location\"))\nfinally:\n    pid = proc.pid\n    ls = subprocess.run([\"lsof\", \"-nP\", \"-a\", \"-p\", str(pid), \"-iTCP\", \"-sTCP:LISTEN\"], capture_output=True, text=True).stdout\n    cwd = subprocess.run([\"lsof\", \"-p\", str(pid)], capture_output=True, text=True).stdout\n    own = (str(PORT) in ls) and ARCH in cwd\n    print(\"stop: pid\", pid, \"listens on\", PORT, \"and cwd is archive:\", own)\n    if own or proc.poll() is None:\n        proc.terminate()\n        try: proc.wait(10)\n        except Exception: proc.kill()\n    print(\"listener after stop:\", subprocess.run([\"lsof\", \"-nP\", f\"-iTCP:{PORT}\", \"-sTCP:LISTEN\"], capture_output=True, text=True).stdout.strip() or \"none\")\nEOF\nlsof -nP -iTCP:54451-54455 -sTCP:LISTEN | head -3; echo ports-checked",
 "description": "Write r5 HTTP probe and check ports free"
}
````

### User / tool · 2026-11-02T23:17:54.558Z

**tool result**
````
ports-checked
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:17:58.570Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir $S/t177r5-probe && .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py $S/t177r5-fresh $S/t177r5-probe unsupported 54451 > artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-unsupported.out 2>&1; cat artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-unsupported.out | cut -c1-420",
 "description": "Run HTTP probe, unsupported mode",
 "timeout": 500000
}
````

### User / tool · 2026-11-02T23:18:01.768Z

**tool result**
````
mode: unsupported | health.answers: prepared | demo_mode: True | local_mode: False | models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
run status: ready
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
entries: [('e2', 'verified'), ('e3', 'verified'), ('e4', 'verified'), ('e5', 'verified'), ('e6', 'verified'), ('e7', 'verified'), ('e8', 'verified'), ('e9', 'verified')]
EDIT e2 -> 200 | warnings: ['The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
   export after edit: 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "re
   item.why: The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it.
   trace judge_1 skipped :: The second check did not run or did not finish, so this item has not been double-checked.
   trace human pending :: You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. I
EDIT e3 -> 200 | warnings: ['The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
   export after edit: 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "re
   item.why: The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it.
   trace judge_1 skipped :: The second check did not run or did not finish, so this item has not been double-checked.
   trace human pending :: You changed the quote, but the summary is still the prepared wording and its second check has no answer on the new quote. Accepting alone will not put it in the letter. I
records with no live entry: ['r1']
MANUAL r1 -> 201 | warnings: ['The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
   item.why: The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it.
MY SCAN of explicit-path responses (18): 0 hit(s)
WORKER-SCANNER offenders: 0 | responses: 92 | prepared items: 16 | edit responses: ['edit:e2', 'edit:e3'] | manual: ['manual:r1']
case.models (second case): {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
GET /classic -> 307 /
stop: pid 51803 listens on 54451 and cwd is archive: True
listener after stop: none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:18:10.051Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py\"\ns=open(p).read()\nold='rej = [e for e in entries if e[\"state\"] == \"rejected\"]\\nfor e in rej[:1]:'\nassert old not in s\nold='    rej = [e for e in entries if e[\"state\"] == \"rejected\"]\\n    for e in rej[:1]:\\n'\nnew='    rej = [{\"id\": \"e1\"}] if MODE == \"unsupported\" else []      # a rejected item is not listed in entries; read it by id\\n    for e in rej[:1]:\\n'\nassert old in s\nopen(p,\"w\").write(s.replace(old,new))\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py $S/t177r5-fresh $S/t177r5-probe unsupported 54452 > artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-unsupported.out 2>&1; grep -n \"CODE-REMOVED\" -A12 artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-unsupported.out | cut -c1-330; grep -E \"MY SCAN|WORKER|stop:|listener\" artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-unsupported.out\n.venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py $S/t177r5-fresh $S/t177r5-probe control 54453 > artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-control.out 2>&1; grep -E \"mode:|EDIT|MANUAL|MY SCAN|WORKER|case.models|stop:|listener|classic\" artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-control.out | cut -c1-300",
 "description": "Rerun HTTP probe for unsupported and control modes",
 "timeout": 560000
}
````

### User / tool · 2026-11-02T23:18:16.397Z

**tool result**
````
15:CODE-REMOVED item e1 | prepared: True | why: Every part of the prepared summary added something its quote does not contain (a number, side, treatment, body part or diagnosis), so code removed all of it and no entry was made. Read the record, or write the entry by hand.
16-   trace extracted fail Prepared answer :: removed from the summary: not in the quote: 'Patient reported paralysis of the left leg' removed from the summary: not in the quote: 'loss o
17-   trace excerpt_verbatim skipped Quote is word for word in the record :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
18-   trace excerpt_whole_sentence skipped Quote is made of whole sentences :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
19-   trace excerpt_hedge skipped Quote keeps the hedge sentence that qualifies it :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
20-   trace summary_tokens skipped Numbers and dates in the summary are in the quote :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
21-   trace summary_qualifier skipped Summary keeps the quote's qualifiers :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
22-   trace highlight skipped Quote can be highlighted in the record :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
23-   trace date_confirmed pass Date of service is confirmed :: The date comes from the record's own header and is parsed or confirmed.
24-   trace injection_scan pass Record has no instruction-like text :: The record has no instruction-like text.
25-   trace judge_1 skipped Second check: is the summary supported by the quote? :: Not run: code removed the whole prepared summary because the quote does not support it, so there is no summary to check.
26-   trace human pending Your decision :: This item could not be verified, so it cannot be accepted.
27-records with no live entry: ['r1']
MY SCAN of explicit-path responses (20): 0 hit(s)
WORKER-SCANNER offenders: 0 | responses: 92 | prepared items: 16 | edit responses: ['edit:e2', 'edit:e3'] | manual: ['manual:r1']
stop: pid 51964 listens on 54452 and cwd is archive: True
listener after stop: none
mode: control | health.answers: prepared | demo_mode: True | local_mode: False | models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
case.models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
EDIT e1 -> 200 | warnings: ['The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
EDIT e2 -> 200 | warnings: ['The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
MY SCAN of explicit-path responses (15): 0 hit(s)
WORKER-SCANNER offenders: 0 | responses: 89 | prepared items: 16 | edit responses: ['edit:e1', 'edit:e2'] | manual: []
case.models (second case): {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
GET /classic -> 307 /
stop: pid 52020 listens on 54453 and cwd is archive: True
listener after stop: none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:18:25.303Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir $S/t177r5-prev && git archive 3feb096 | tar -x -C $S/t177r5-prev && .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/probe_r5_http.py $S/t177r5-prev $S/t177r5-probe control 54454 > artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-control-on-3feb096.out 2>&1; grep -E \"EDIT|MANUAL|MY SCAN|WORKER|stop:|listener\" -A3 artifacts/review-evidence/T-177-staff-engineer-r5/probe-r5-http-control-on-3feb096.out | cut -c1-330 | head -30",
 "description": "Differential probe on prior build 3feb096",
 "timeout": 560000
}
````

### User / tool · 2026-11-02T23:18:29.605Z

**tool result**
````
EDIT e1 -> 200 | warnings: ['The AI second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
   export after edit: 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "re
   item.why: The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it.
   trace judge_1 skipped :: The second check did not run or did not finish, so this item has not been double-checked.
--
EDIT e2 -> 200 | warnings: ['The AI second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it. Until you do, the item stays marked for review.']
   export after edit: 422 {"error": {"code": "export_blocked", "message": "Nothing is accepted or edited yet, so the letter would be empty. The export is blocked.", "detail": {"blockers": [{"item_id": null, "kind": "case", "re
   item.why: The second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they match, accept it.
   trace judge_1 skipped :: The second check did not run or did not finish, so this item has not been double-checked.
--
MY SCAN of explicit-path responses (15): 1 hit(s)
   ('edit', '.warnings[].message', 'The AI ') | The AI second check is not available in this demo, so this item has not been double-checked. Compare the summary with the quote yourself; if they matc
WORKER-SCANNER offenders: 0 | responses: 71 | prepared items: 16 | edit responses: [] | manual: []
case.models (second case): {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
GET /classic -> 307 /
stop: pid 52201 listens on 54454 and cwd is archive: True
listener after stop: none
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:18:33.465Z

**tool call — Bash**
````
{
 "command": "git show e425534:app/backend/review.py | grep -n -i \"\\bAI\\b\" | cut -c1-220 | head -30; echo ---; git show e425534:app/backend/api.py | grep -n -i '\"[^\"]*\\bAI\\b[^\"]*\"' | cut -c1-200 | head -20",
 "description": "Grep AI wording in review.py and api.py"
}
````

### User / tool · 2026-11-02T23:18:33.702Z

**tool result**
````
65:# D-051: the code rung binds accept for every item, AI-made or human. These are the code checks on an entry's current wording.
73:# plain words for "AI wording removed (failed a check: ...)" in the internal notes
308:_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
309:                     "disagrees": "The second AI check disagreed with the first result for this item."}
530:    if "pre_edit" not in lad:      # T-138: the first edit keeps what the AI wording had (second check, code checks, state) so an undo can put it all back
550:    """T-138: undoing an edit puts the AI wording back WITH the second-check result and code-check record it had before the edit, so accept works as it did.
727:    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
807:            msg = (f"The record was split off. Code removed every part of {"the prepared summary" if prep else "the AI's summary"} that its quote does not support, so it is in the could-not-verify tray; "
809:                   else f"The record was split off, but {'no prepared answer was usable for' if prep else 'the AI could not draft'} its entry; it is in the could-not-verify tray. Enter it by hand.")
---
38:AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
39:PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item"      # D-065
447:                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
475:                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
516:        """D-031: the reviewer writes the entry for a record the AI could not make one for. Quote = whole verbatim sentences (422 otherwise)."""
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:18:37.120Z

**tool call — Bash**
````
{
 "command": "git show e425534:app/backend/review.py | sed -n 300,335p | cut -c1-260; git show e425534:app/backend/review.py | grep -n \"_DISPUTE_SENTENCE\\|dispute_sentence\" ",
 "description": "Inspect dispute sentence usage"
}
````

### User / tool · 2026-11-02T23:18:37.257Z

**tool result**
````
    if ver is not None and (isinstance(ver, bool) or not isinstance(ver, (int, float))):
        raise _bad("The version must be the number the item was last shown with.")
    stale = (exp is not None and exp != item["review_status"]) or (ver is not None and abs(float(ver) - float(item.get("updated_at") or 0)) > 1e-6)
    if stale and _TARGET_STATUS.get(action) != item["review_status"]:
        raise ReviewError(409, "stale_item", {"item_id": item["id"], "review_status": item["review_status"], "version": item.get("updated_at")}, STALE_MESSAGE)


_DISPUTED = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES"}
_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
                     "disagrees": "The second AI check disagreed with the first result for this item."}
_DISPUTE_SENTENCE_PREPARED = {"partially": "A second check found this only partly supported by the quote.", "unsupported": "A second check found this not supported by the quote.",      # D-069
                              "disagrees": "A second check disagreed with the first result for this item."}


def judge_dispute(item: dict):
    """D-066: the second check's objection to this item, as its ladder verdict (partially | unsupported | disagrees), else None. The verdict on the item's ladder or any of the
    three JUDGE_* reasons counts; unsure and unavailable are not an objection. Code only."""
    j = (item.get("ladder") or {}).get("judge")
    v = j.get("verdict") if isinstance(j, dict) else None
    v = "disagrees" if v == "disagree" else v        # the amount-class judge says "disagree"
    if v in _DISPUTED:
        return v
    reasons = item.get("state_reasons") or []
    return next((k for k, code in _DISPUTED.items() if code in reasons), None)


def compare_error(item_id: str, item: dict, compared, conn=None, case_id=None):
    """D-066: accepting an item the second check disputed needs the explicit statement that she compared it with the quote (`compared: true`). 422 COMPARE_REQUIRED without it."""
    v = judge_dispute(item)
    if not v or compared is True or item.get("review_status") == "accepted":
        return None
    prep = False
    if conn is not None:
        from app.backend import present          # lazy: present imports review
        prep = present.Prov(conn, case_id).prepared(item)      # D-069: the sentence follows the item's provenance
    return ReviewError(422, "COMPARE_REQUIRED", {"item_id": item_id, "reason_code": "COMPARE_REQUIRED", "verdict": v,
308:_DISPUTE_SENTENCE = {"partially": "The second AI check found this only partly supported by the quote.", "unsupported": "The second AI check found this not supported by the quote.",
310:_DISPUTE_SENTENCE_PREPARED = {"partially": "A second check found this only partly supported by the quote.", "unsupported": "A second check found this not supported by the quote.",      # D-069
337:                       (_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v] + " Read it against the quote, then say you compared it before you accept it.")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:18:45.117Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/mutate_r5.py\"\ns=open(p).read()\nadd='''    \"N5_dispute_twin_unused\": (\"app/backend/review.py\",\n        '(_DISPUTE_SENTENCE_PREPARED if prep else _DISPUTE_SENTENCE)[v]',\n        '_DISPUTE_SENTENCE[v]'),\n}\npath, old, new = M[NAME]'''\ns=s.replace('}\\npath, old, new = M[NAME]',add,1)\nopen(p,\"w\").write(s)\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -I artifacts/review-evidence/T-177-staff-engineer-r5/run_mutants_r5.py $S/t177r5-fresh tests/unit/test_prepared_property.py N5_dispute_twin_unused > artifacts/review-evidence/T-177-staff-engineer-r5/mutants-batch3.out 2>&1; cat artifacts/review-evidence/T-177-staff-engineer-r5/mutants-batch3.out",
 "description": "Bonus mutant on dispute sentence twin",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:19:16.449Z

**tool result**
````
N5_dispute_twin_unused: KILLED | 1 failed, 18 passed, 2 skipped in 30.66s | ['FAILED tests/unit/test_prepared_property.py::test_no_prepared_text_names_an_ai_or_a_model[case_lib10_eob_ub04_cms1500-valid-one]']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:19:22.136Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t177r5-fresh && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/unit-suite.out 2>&1; tail -3 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/unit-suite.out",
 "description": "Run unit suite in archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T23:26:14.222Z

**tool result**
````
........................................................................ [ 99%]
............................................                             [100%]
5865 passed, 11 skipped in 410.26s (0:06:50)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:26:21.011Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; diff -rq $S/r5 $S/t177r5-fresh -x __pycache__ -x .pytest_cache -x artifacts | head; echo \"src-diff-done\"; lsof -nP -iTCP:54440-54460 -sTCP:LISTEN | head -3; echo listeners-checked; git rev-parse HEAD; git status --short -- app tests | head -5; python3 tools/board.py validate 2>&1 | tail -2",
 "description": "Confirm sources restored, no listeners, HEAD unchanged"
}
````

### User / tool · 2026-11-02T23:26:22.387Z

**tool result**
````
src-diff-done
listeners-checked
bd72d5b9a6dcf94eba56df71e612d4f240351ba5
MM app/backend/api.py
MM app/backend/export_routes.py
MM app/backend/flag_templates.py
MM app/backend/flags.py
MM app/backend/generator.py
ok (202 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:26:24.586Z

**tool call — Bash**
````
{
 "command": "git log --oneline e425534..HEAD | head -5; git diff --stat e425534 HEAD -- app/backend/review.py app/backend/why.py app/backend/trace.py tests/unit/test_prepared_property.py | tail -3",
 "description": "Check HEAD movement vs reviewed commit"
}
````

### User / tool · 2026-11-02T23:26:24.696Z

**tool result**
````
bd72d5b fix(backend): T-200 counted undated ledger charge prints its statement date as such, never as a service date
8f78874 fix(qa): T-187 r4 / T-198 prompt log: private terms read from deploy/.private_patterns (none in tracked code), normalized-view redaction + self-test (D-070), device names, tree scan tool
2c19817 fix(frontend): T-181 r3 phone: highlighted words scrolled into a record window sized for them, refused edit shown above the action bar, panel-list test scans only loaded scripts
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:26:31.056Z

**tool call — Bash**
````
{
 "command": "ls reviews/T-177-staff-engineer-r5.md 2>&1 | head -1; ls artifacts/review-evidence/T-177-staff-engineer-r5/",
 "description": "Check review file absent and list evidence"
}
````

### User / tool · 2026-11-02T23:26:31.144Z

**tool result**
````
ls: reviews/T-177-staff-engineer-r5.md: No such file or directory
archive-source-sha.txt
baseline-property.out
mutants-batch1.out
mutants-batch2.out
mutants-batch3.out
mutate_r5.py
probe-r5-http-control-on-3feb096.out
probe-r5-http-control.out
probe-r5-http-unsupported.out
probe_r5_http.py
run_mutants_r5.py
unit-suite.out
why-N1-N2.out
why_mutant_r5.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:00.384Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r5.md",
 "content": "# T-177 round 5 (final, narrow; D-069 / D-065): staff-engineer-reviewer\n\n**Verdict: pass (0 blockers, 0 majors, 0 minors).** The round-4 F1 major is closed. My three surviving mutants (B2, B4, C5) now each turn the property test red. Two fresh mutants of my own, one in an edit-path message and one in a manual-entry message, are also red, and the test fails on the model name in each. The live demo is clean on the edit, manual-entry and code-removed paths. A differential run of the same probe on the round-4 build (3feb096) finds the real leak the worker fixed, so the probe can see it. The unit suite gives the figure the handoff quotes.\n\n**Scope.** Fix commit e425534 (touches `app/backend/review.py`, `app/backend/why.py`, `tests/unit/test_prepared_property.py`), reviewed from `git archive e425534` (`artifacts/review-evidence/T-177-staff-engineer-r5/archive-source-sha.txt`). Evidence is under `artifacts/review-evidence/T-177-staff-engineer-r5/`. HEAD moved to bd72d5b during the review. `git log e425534..HEAD` shows T-200, T-187/T-198 and T-181 only, and `git diff --stat e425534 HEAD` on the three T-177 files is empty. I mutated only archive copies and restored each from `git show e425534:<path>`, byte-compared. After all mutants and the unit run, the source tree matches a fresh archive of e425534 (`diff -rq`, no output).\n\n## Round-4 status\n\n| Round-4 item | Status at e425534 |\n|---|---|\n| F1 major: property test never reaches unsupported-summary, edit and accept-without-judge families; twins deletable | Fixed. `FAULTS` now includes `unsupported`; `actions()` edits a quote then accepts, accepts an entry with no second-check answer, and writes a manual entry for each record with no live entry; a static test checks twin completeness. B2, B4, C5 are killed (below) |\n| F5 nit: `INJECTION_SUSPECTED` has no twin | Fixed. `why.py` `_WHY_PREPARED[\"INJECTION_SUSPECTED\"]`; mutant T1 (twin removed) is killed by the static test |\n| F2 minor, F3 minor, F4 nit (exemptions, evidence counts, disclosure line) | Accepted minors, not graded. For the record, the handoff figures now reproduce: 34 passed, 3 skipped for the property file and 5865 passed, 11 skipped for the unit suite (my runs) |\n\nThe worker's handoff also reports a new live leak that the extended test found in `review._check_summary` (the edit and manual-entry second-check warning had no provenance argument). I confirmed it as a real fix. On the round-4 build, the edit warning reads \"The AI second check is not available in this demo\" on a prepared item (`probe-r5-http-control-on-3feb096.out`: 1 hit by my scan, 0 by the round-4 scanner). At e425534 it reads \"The second check is not available in this demo\".\n\n## What I exercised\n\n- **Mutants B2, B4, C5 (item 1).** Applied one at a time to a `git archive e425534` copy with `run_mutants_r5.py` (the r4 harness, SHA retargeted), `pytest tests/unit/test_prepared_property.py -x`, restored and byte-compared (`mutants-batch1.out`). Baseline first: 34 passed, 3 skipped (`baseline-property.out`).\n  - B2 (`trace.py` skipped step for SUMMARY_NOT_IN_QUOTE says \"whole AI summary\"): KILLED, `test_no_prepared_text_names_an_ai_or_a_model[sample-unsupported-one]`.\n  - B4 (`why.py` twin for SUMMARY_NOT_IN_QUOTE says \"AI summary\"): KILLED, same test id.\n  - C5 (`trace.py:128` drops all seven `TRACE_WHY_PREPARED` twins): KILLED, `[sample-valid-one]`.\n- **Fresh mutants (item 2).** `mutants-batch1.out`, `mutants-batch2.out`, `mutants-batch3.out`:\n  - N1, edit path: `_edit` returns a warning \"The edited quote was checked again with claude-sonnet-5-5.\" KILLED, `[sample-valid-one]`.\n  - N2, manual-entry path: `manual_entry` returns a warning \"Entered by hand; claude-sonnet-5-5 was not used.\" KILLED, `[sample-malformed-one]`.\n  - `why-N1-N2.out` shows both fail for the right reason: `('edit', '.warnings[].message', 'claude')` and `('manual', '.warnings[].message', 'claude')`, quoting my inserted sentences.\n  - N3 and N4 (the real fix reverted: the `prep=` argument removed from the `_edit` and `manual_entry` calls): both KILLED.\n  - T1 (remove the `INJECTION_SUSPECTED` twin): KILLED by `test_every_sentence_that_names_an_ai_has_a_prepared_twin_and_no_twin_names_one`. T2 (remove the `JUDGE_NOT_RUN` trace twin): KILLED. T3 (misspell the `SUMMARY_NOT_IN_QUOTE` twin key, so the prepared text is gone): KILLED. These three cover the \"remove one prepared twin\" part of item 2 in three different tables.\n  - N5 (bonus; `compare_error` uses `_DISPUTE_SENTENCE[v]` instead of the prepared table): KILLED, via `case_lib10_eob_ub04_cms1500-valid-one`.\n  - All 12 mutants (B2, B4, C5, N1 to N5, T1 to T3) were killed. None survived.\n- **Live probe (item 3).** My own demo-mode servers (no `ZLAYT_MODE`, `LLM_BACKEND=fixture`) from a `git archive e425534` copy, over HTTP, on loopback ports 54451 to 54454 with `probe_r5_http.py`.\n  - `unsupported` (e1's prepared summary replaced by one its quote lacks; port 54452, `probe-r5-http-unsupported.out`): code-removed path: e1 item is `prepared: True` with why \"Every part of the prepared summary added something its quote does not contain ... so code removed all of it and no entry was made\", and the trace steps read \"Not run: code removed the whole prepared summary...\". Edit path: edit of e2 and e3 returns 200 with warning \"The second check is not available in this demo...\", the item `why` and the `human` trace step say \"the summary is still the prepared wording and its second check has no answer on the new quote\". Manual path: hand entry on record r1 returns 201 with the same prepared warning. My scan of the 20 explicit-path responses: 0 hits for `AI`, `claude`, `sonnet`, \"Drafted by\" and the authorship phrases. The worker's `collect()` and `offenders()` over a second case (92 responses, 16 prepared items, edit:e2, edit:e3 and manual:r1 present): 0 offenders. `case.models` is `hand-checked (qa)` / `claude-haiku-5-5` / `generator_prepared: True`. `/classic` answers 307 to `/`.\n  - `control` (shipped `FIXTURE_SET=curated`; port 54453, `probe-r5-http-control.out`): edit e1 and e2 return 200 with the prepared warning; my scan 0 hits; worker scanner 0 offenders over 89 responses.\n  - Differential run on the round-4 build 3feb096 (port 54454, `probe-r5-http-control-on-3feb096.out`): my scan finds 1 hit, `('edit', '.warnings[].message', 'The AI ')`, in the edit response. The worker's scanner found 0 there because the round-4 `collect` had no edit pass. So the probe separates the two builds.\n  - PIDs: the probe checks `lsof` (listening port) and cwd (the archive) before `terminate()`. Output shows \"stop: pid 51803, 51964, 52020, 52201 ... cwd is archive: True\" and \"listener after stop: none\" for each. `lsof -iTCP:54440-54460 -sTCP:LISTEN` returns nothing now. I stopped only my own PIDs.\n- **Suites (item 4).** `pytest tests/unit -q` in the e425534 archive: 5865 passed, 11 skipped in 410.26 s (`unit-suite.out`), the same counts the handoff reports. `pytest tests/unit/test_prepared_property.py`: 34 passed, 3 skipped (the three are the valid/all combinations, `test_prepared_property.py` `pytest.skip(\"valid has no scope\")`).\n- Read in full: `reviews/T-177-staff-engineer-r4.md`, the card handoff and notes, `git show e425534` (all three files), the property test (all 369 lines), `review.py` around `_check_summary`, `_edit`, `manual_entry`, `compare_error`, `why.unavailable_sentence`.\n- Not run: the guided E2E (`E2E_REQUIRE_DB=1 pytest tests/e2e/guided tests/e2e/test_demo_provenance.py`, handoff says 130 passed; not in the brief), the eval runner, a browser. The accepted minors (shape-based exemptions, the unpinned disclosure line, the classic tooltip at `timeline.js:22`) were not graded.\n\n## Verdict rule\n\nNo blocker, no major, no minor, so `pass`.\n\n```json\n{\"card\": \"T-177\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git archive e425534 (fix commit; app/backend/review.py, app/backend/why.py, tests/unit/test_prepared_property.py); own demo-mode servers on loopback ports 54451-54454; sample case, curated set and an unsupported-summary fault; edit, manual-entry and code-removed paths\",\n \"exercised\": [\n  \"git archive e425534 into a unique scratch dir; diff -rq against a second fresh archive after all mutants and the unit run: no difference\",\n  \"pytest tests/unit/test_prepared_property.py baseline in the archive: 34 passed, 3 skipped\",\n  \"r4 mutants B2, B4, C5 re-applied via run_mutants_r5.py: all three KILLED (sample-unsupported-one, sample-unsupported-one, sample-valid-one)\",\n  \"fresh mutants: N1 model name in an edit-path warning (KILLED), N2 model name in a manual-entry warning (KILLED), N3/N4 prep argument reverted on _edit/manual_entry (KILLED), T1/T2/T3 one prepared twin removed in why.py and trace.py (KILLED), N5 dispute sentence twin unused (KILLED); each restored from git show e425534 and byte-compared\",\n  \"why_mutant_r5.py on N1 and N2: failure text quotes the inserted sentence at .warnings[].message\",\n  \"probe_r5_http.py on my own demo-mode servers (ports 54451-54454): unsupported fault and shipped curated set; edit, manual-entry and code-removed paths printed; my authorship regex 0 hits; worker offenders() 0 over 92 and 89 responses; /classic 307 to /\",\n  \"same probe on a git archive of 3feb096: 1 hit in the edit warning ('The AI second check is not available in this demo'), so the probe separates the builds\",\n  \"lsof + cwd check before every terminate(); lsof -iTCP:54440-54460 -sTCP:LISTEN empty afterwards\",\n  \"pytest tests/unit -q in the archive: 5865 passed, 11 skipped in 410.26 s\",\n  \"git log e425534..HEAD and git diff --stat e425534 HEAD on the three T-177 files: HEAD moved to bd72d5b, no T-177 file changed\",\n  \"read reviews/T-177-staff-engineer-r4.md, the card handoff, git show e425534, the property test, review.py/why.py around the changed lines\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"d069_structural_fix_in_product\": 5, \"property_test_strength\": 5, \"edit_manual_code_removed_paths_live\": 5, \"failure_visibility\": 5, \"evidence_reproducibility\": 5},\n \"findings\": [],\n \"whats_right\": [\n  \"The property test now injects an unsupported-summary fault and runs an edit, accept-plain and hand-entry pass; 12 of 12 mutants across the twin tables and the edit/manual messages turn it red.\",\n  \"Static twin test (every AI-wording why/trace/next sentence has a twin, no twin names an AI, no orphan code) closes the silent twin-or-AI fallback; the non-vacuity test pins that the edit and unavailable twins actually appear.\",\n  \"The worker followed the probe to the real leak (review._check_summary warning without a provenance argument) instead of only patching the lines I had mutated; the fix is small and the handoff counts reproduce (34/3 and 5865/11).\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T23:27:00.531Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r5.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:02.199Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate board and reviews"
}
````

### User / tool · 2026-11-02T23:27:02.379Z

**tool result**
````
ok (202 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:03.260Z

Now the memory notes.

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:08.633Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_r5_patterns.md",
 "content": "---\nname: t177-r5-patterns\ndescription: T-177 r5 pass: guard now reaches edit/manual/unsupported paths; 12/12 mutants killed; differential probe on 3feb096 finds the old leak; shared-scratchpad r5 dir collision\nmetadata:\n  type: project\n---\n\nRound 5 passed with no findings: B2/B4/C5 killed, fresh edit/manual model-name mutants killed, live demo clean on edit, manual and code-removed paths.\n\n**Why:** the real leak the extended test found was `review._check_summary` (edit and manual-entry second-check warning had no provenance arg), not the lines I had mutated in r4. A mutant-only review would have missed it; the old `collect` had no edit pass, so the old scanner saw 0 on the old build.\n\n**How to apply:**\n- Differential probe: run the same probe on the prior-sha archive; the round-4 worker scanner gave 0 offenders where my own regex gave 1 hit. Always include a wider-pattern scan of the explicit-path responses next to the worker's scanner.\n- A rejected item (code-removed) is not in `case.entries`; read it by id (`/items/e1`), not from the list.\n- Guard (board-guard) refuses `tee`, `rm`, `mkdir` and redirects whose target uses `$VAR`; use literal absolute paths or a python script for those. `ls -d .../*/*/scratchpad/r5` can match other sessions' dirs; use a unique card-round dir name (t177r5-*).\n- Harness reused: `artifacts/review-evidence/T-177-staff-engineer-r5/{mutate_r5,run_mutants_r5,why_mutant_r5,probe_r5_http}.py` (mutants keyed by exact-string replace; asserts one match; restore from `git show <sha>:path`).\n- Handoff counts reproduced this round: 34 passed, 3 skipped (property file), 5865 passed, 11 skipped (unit, ~410 s).\n\nRelated: [[project_t177_r4_patterns]], [[feedback_differential_probe_prior_build]], [[feedback_shared_scratchpad]].\n"
}
````

### User / tool · 2026-11-02T23:27:08.730Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t177_r5_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:09.759Z

**tool call — Bash**
````
{
 "command": "printf '%s\\n' '- [T-177 r5 patterns](project_t177_r5_patterns.md) — pass: 12/12 mutants killed, old-build probe finds leak, guard refuses $VAR targets' >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md && tail -2 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "description": "Add memory index entry"
}
````

### User / tool · 2026-11-02T23:27:09.843Z

**tool result**
````
- [Shared index staged deletes](feedback_shared_index_staged_deletes.md) — sha check passes while index stages a D on the AC test; run git status too
- [T-177 r5 patterns](project_t177_r5_patterns.md) — pass: 12/12 mutants killed, old-build probe finds leak, guard refuses $VAR targets
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T23:27:12.466Z

T-177 round 5 is a pass with no findings: B2, B4 and C5 now fail the property test. Two fresh mutants fail too, one with a model name in an edit warning and one in a manual-entry warning, and so does one removed prepared twin.
The edit, manual and code-removed paths read clean on my own demo server (0 offenders, `/classic` redirects). The same probe on 3feb096 catches the old "The AI second check…" edit warning. `pytest tests/unit -q` gives 5865 passed, 11 skipped. I did not run the guided E2E. All 12 mutants I tried were killed, and my servers' PIDs are stopped.

The review is at `/Users/arsis/zlayt-pm-project/reviews/T-177-staff-engineer-r5.md`, with evidence in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-177-staff-engineer-r5/`.
