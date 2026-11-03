# Subagent: T-108 r2 check (haiku staff) (T-108 r2 check (haiku staff))

Source: `agent-a62a844caf0659aac.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:38:29.015Z

Round-2 check of board card T-108 (quote picker units) in /Users/arsis/zlayt-pm-project (commit a271014). Read reviews/T-108-staff-engineer.md. On a `git archive HEAD` copy in your scratchpad, confirm:
- hedge-qualified sentences are offered as combined units that save alone;
- a label-only record offers no units and gives a plain sentences_reason;
- the invariant test passes: every offered unit saves, on the sample, case_01 to case_09 and all 15 library packets;
- removing the combining logic in a scratch copy fails a test.

Minors F4, F6 and F7 are left for later; note them as still open. Run `.venv/bin/python -m pytest -q tests/unit`. Write reviews/T-108-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:30.185Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T06:38:30.195Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:30.370Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer.md"
}
````

### User / tool · 2026-11-02T06:38:30.378Z

**tool result**
````
1	# T-108 review (staff-engineer-reviewer, r1): quote picker units from the quotable body
2	
3	Commit d3e127c, `fix(backend): quote picker units come from the quotable body only`. Reviewed on a fresh `git archive d3e127c` copy. The live repo is at 1526a1f with uncommitted edits, so no live-tree result is cited here. Model recorded is the model I actually ran as, claude-haiku-5-5 (the dossier's expected id is claude-sonnet-5-5).
4	
5	**Verdict: changes** (0 blockers, 2 majors, 5 minors, 1 nit).
6	
7	## Summary
8	
9	On the sample and case_01..09 the change works. 59 records and 150 units: no `Excerpt`, `Date:`, `Source:`, `===`, or quote-mark text, every unit is a verbatim slice at its true offset, and every unit plus its trailing hedge chain passes the same check the save routes run. The real-backend Change-the-quote e2e passes 3/3. Reverting the units to the whole block fails 13/13 unit tests and 3/3 e2e tests.
10	
11	Three gaps remain:
12	1. A sentence that a hedge qualifies cannot be picked alone. The picker never adds the hedge, but the unit test helper assumes it does, so the test is green while the UI refuses those sentences (F1, major).
13	2. `quote_body` falls back silently to the whole record block. A record with an `Excerpt:` line and no Date/Source line still shows the label and header lines in the units (F2, major).
14	3. The offset branch can be deleted without any test failing, and curly quotes are not covered (F3, F4, minor).
15	
16	## Exercised
17	
18	- `git archive d3e127c` into the scratchpad copy `T108_verify`. A second copy matched it file for file (the only differences were `__pycache__`).
19	- `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit` on that copy: `2077 passed, 4 skipped`. Skips: 3 need a `.git` directory the export lacks, and 1 is the live-judge eval gated by env. Output saved at `artifacts/review-evidence/T-108/unit-run.txt`.
20	- `pytest tests/unit/test_quote_units.py -v`: 13 passed.
21	- `artifacts/review-evidence/T-108/probe_units.py` over sample and case_01..09 (10 cases, 59 records, 150 units). Each unit is checked with `spanish.module_for(...).check_excerpt`, the call review.py:300 and :451 make, both alone and with the trailing hedge chain. Output: `artifacts/review-evidence/T-108/probe-units-output.json`.
22	- `artifacts/review-evidence/T-108/probe_shapes2.py` over six synthetic record shapes (A to F) through `ingest.split_records` and `present.quote_body`. No API call. Output: `artifacts/review-evidence/T-108/probe-shapes-output.txt`.
23	- Real backend: the archive copy served on 127.0.0.1:7971 with `ZLAYT_DB` set to a scratch sqlite file, `DATA_DIR` set to an empty sentinel directory, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`. `tests/e2e/test_change_the_quote.py`: 3 passed (`artifacts/review-evidence/T-108/e2e-head-run.txt`). The scratch sqlite file received the writes and the sentinel stayed empty.
24	- `artifacts/review-evidence/T-108/single_unit.py` against that server: a sample case, entry e8 on r8, `POST .../items/e8/review` with `{"action":"edit","edits":{"excerpt":<unit 0 alone>}}` gave 422 `invalid_edit` with reasons `["EXCERPT_OMITS_QUALIFIER"]`. Output: `artifacts/review-evidence/T-108/single-unit-output.txt`.
25	- Mutants, scratch copies only, not committed. M1: `quote_body` returns `(0, block)` (the pre-fix behaviour). M2: the label/quote-mark branch disabled at present.py:165 (`if False:`). Results in `mutant-M1-unit.txt`, `mutant-M1-e2e.txt` (run on a second server on :7972) and `mutant-M2-unit.txt`. `artifacts/review-evidence/T-108/mutate.py` is the helper.
26	- Read in full: `personas/staff-engineer.md`; `app/backend/present.py`; `app/backend/sentences.py`; `app/backend/grounding.py` (`check_excerpt`); `app/backend/spanish_text.py` (`check_excerpt`); `app/backend/review.py` (edit and manual_entry); `app/backend/store.py` (`load_records`); `app/backend/ingest.py` (`_excerpt_extent`); `app/backend/api.py` (demo gate); `app/frontend/excerpt.js`; `app/frontend/manual.js`; `tests/unit/test_quote_units.py`; `tests/e2e/test_change_the_quote.py`; the `tests/e2e/conftest.py` diff.
27	- Not exercised: a non-demo paste (no API key, no `claude-cli`); the browser DOM outside the e2e spec.
28	
29	## Findings
30	
31	**F1 (major). A sentence that a hedge qualifies cannot be picked on its own.** The picker never adds the qualifying hedge. The unit test's `_pick` helper does add it, and its docstring says the picker does. The UI-built quote is refused.
32	Evidence: `app/frontend/excerpt.js:35` (`pick(i)` only moves `lo`/`hi`) and `:38` (text is `units[lo].start` to `units[hi].end`, no hedge extension). `tests/unit/test_quote_units.py:25` says "The quote the picker builds for unit i: the unit plus any hedge units that immediately follow it"; `_pick` (lines 24-30) implements that rule. Repro: with the archive server on :7971, run `artifacts/review-evidence/T-108/single_unit.py`. Sample r8 unit 0, "C5-C6 disc protrusion with mild right foraminal narrowing.", alone gives 422 `invalid_edit` / `EXCERPT_OMITS_QUALIFIER`. Across 150 units, 3 fail alone: sample r8 (2 units) and case_08 r2, "Signal change in the supraspinatus tendon." (`probe-units-output.json`, `alone_fail`).
33	Why it matters: the card AC says "picking whole sentences yields a valid verbatim quote on sample and case_01..09". That is false for 3 sentences. The green `test_every_offered_unit_is_a_valid_quote` cannot catch it because `_pick` supplies the hedge. The handoff's "Left" note discloses the rule, but the AC and the docstring say the opposite of what the UI does.
34	Fix: choose one. (a) `excerpt.js` extends a selection through the trailing hedge run, the same chain `_pick` builds, and checks those boxes. (b) Keep the UI, restate the AC and the docstring, and make the test drive the UI rule: unit alone gives 422 `EXCERPT_OMITS_QUALIFIER`, unit plus hedge chain gives 201.
35	Acceptance test: for sample r8 unit 0 and case_08 r2 unit 0, the text the picker would submit is saved (201) under (a), or is refused with `EXCERPT_OMITS_QUALIFIER` under (b). The test must submit the UI-built text, not the `_pick` text, and must fail if the picker stops extending.
36	
37	**F2 (major). `quote_body` falls back silently to the whole record block, so label-only and date-less records leak `Excerpt:` and header lines into the units.** This is the bug the card claims to fix, and it still happens for a reachable record shape.
38	Evidence: `app/backend/present.py:160-163` (`try: body = ingest.split_records(block)[0]["excerpt"]` / `except Exception: body = block`) and `:167-168` (`i = block.find(body)`; `return (i, body) if i >= 0 else (0, block)`). Verbatim output from `probe-shapes-output.txt`:
39	`A_excerpt_only | units=['Excerpt: "Pain persists after two weeks.', 'Taking meds daily."']`
40	`C_source_excerpt | units=['Source: Synthetic Clinic', 'Excerpt: "Pain persists after two weeks.', 'Taking meds daily."']`
41	Repro: `/Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-108/probe_shapes2.py <path to an archive copy of d3e127c>`.
42	The stored excerpt (`app/backend/store.py:22-25`, same split) also keeps the label for these shapes, so the save route checks quotes against text that includes it. The label comes from upstream, but this commit's fallback is what puts it in the picker.
43	Reachability: `POST /api/cases` with pasted text returns 409 `demo_mode_unsupported_input` unless live mode is on (`api.py:287-288`; live gate at `api.py:116-120`). I saw that 409 with `ENABLE_LIVE` unset. I did not exercise live mode, so reachability in live mode is inferred from the code.
44	Why it matters: the commit's invariant (no label, quote marks, or header lines; "cut from the excerpt body") fails silently on an input the golden set does not contain. The broad `except` and the `(0, block)` return turn a split failure into exactly the bug this card fixes, with no status shown. That is a silent fallback (persona 4.12). Not a blocker: no fact is invented and the save route still checks verbatim. Major because the AC is stated generically.
45	Fix: a record whose body cannot be located gives no units and a visible state (for example a `record_warning`), not the block. Remove the broad `except` so the split error surfaces. Strip the `Excerpt:` label and any `Date:`/`Source:` lines for unsplit records, or classify the record as unsplit with its own state.
46	Acceptance test: `test_quote_body_cases` (tests/unit/test_quote_units.py:80) gains shapes A and C. Each asserts that no unit starts with `Excerpt` or `Source:` and no unit contains a double quote. A record that cannot be split yields no units plus a reason. The current `(0, block)` branch must fail this test.
47	
48	**F3 (minor). Removing the label/quote-mark offset branch passes every quote test.** Evidence: present.py:164-166. Mutant M2 (`if False:` at :165) passes 13/13 (`mutant-M2-unit.txt`). For shape F (`Source:` repeats the body), the correct base is 69 and `block.find` gives 25, which is the Source line (`probe-shapes-output.txt`). Without the branch, unit offsets point into the Source line. No golden case or test covers this. The only offset test that touches `quote_body` (line 83) uses a body that appears once.
49	Why it matters: the card's "at their true offsets" claim is untested for repeated text.
50	Fix and acceptance: add shape F to `test_quote_body_cases` and assert `raw[u.start:u.end] == u.text` and that `u.start` lies inside the excerpt body. M2 must fail it.
51	
52	**F4 (minor). Curly quotes survive as wrapper, and the quote-mark assertions cover the sample only.** Evidence: `app/backend/ingest.py:63` strips only straight `"`. Shape D gives `units=['“Pain persists after two weeks.', 'Taking meds daily.”']`. The no-quote-mark check is in `test_sample_units_have_no_wrapper` (test_quote_units.py:59-66) and in e2e `test_change_the_quote.py:27` and `:51`. Both are sample-only. `test_every_offered_unit_is_a_valid_quote` (line 49) checks only `startswith`. Golden cases show no quote marks today (`probe-units-output.json`, `wrapper` = 0 everywhere), so this is a latent gap.
53	Fix: strip matched curly pairs in the excerpt extent, or give the record a state. Extend the quote-mark assertion to every case at line 49.
54	Acceptance test: shape D gives units with no `“`, `”`, or `"`, and line 49's assertion covers case_01..09 as well as the sample.
55	
56	**F5 (minor). The "2110 passed" evidence does not reproduce at the cited commit.** Card T-108 AC says "tests/unit full run 2110 passed". At d3e127c, `pytest --collect-only -q tests/unit` collects 2081 and the run gives `2077 passed, 4 skipped` (`unit-run.txt`). The live tree at 1526a1f, with 1291 untracked files and uncommitted edits, collects 2206. The 2110 figure probably comes from a different tree.
57	Fix: rerun at d3e127c, and name the commit and the pytest tail line in the AC evidence.
58	
59	**F6 (minor). The frontend strips the wrapper again in `manual.js`, which can hide a backend regression.** `app/frontend/manual.js:14-23` (`quotable(rec)`) removes `===`/`Date:`/`Source:` lines, the `Excerpt:` label, and a trailing quote from `rec.sentences` on the client. A backend leak would be hidden in the manual-entry tray, and the rule now lives in two places that can drift.
60	Fix: have the tray take the backend units as they are (or assert on the tray's inputs), and keep one copy of the rule.
61	
62	**F7 (minor). The "excerpt-error hidden" check in the e2e runs before the save response.** Evidence: `tests/e2e/test_change_the_quote.py:59` (`expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()`) runs straight after the `btn-save-excerpt` click. The error box starts hidden, so the check passes at once. The real check is the poll at lines 60-65.
63	Fix: wait for the save response (for example `expect_response`) or drop line 59.
64	Acceptance test: with the line dropped or the wait added, the spec still passes on the fixed build and fails when the picker's submit is broken. (This is also a nit under F7, kept at minor because it sits in a required AC test.)
65	
66	**F8 (nit). Naming.** `_pick` in `test_quote_units.py` builds the quote the picker should build, not what the picker builds. Rename it `_hedge_chain_quote` (or similar) once F1 is decided.
67	
68	## What is right
69	
70	- Units come from the same body the save route checks, at absolute offsets: 150 units with zero not-verbatim, out-of-block, or wrapper hits on sample and case_01..09, and zero pick failures once the trailing hedge is included (`probe-units-output.json`).
71	- The fix is locked by tests: reverting to whole-block units fails all 13 quote unit tests and all 3 real-backend e2e tests (`mutant-M1-unit.txt`, `mutant-M1-e2e.txt`).
72	- The picker's quote check is the same call the save routes make (`spanish.module_for(...).check_excerpt`, review.py:300 and :451). No LLM is on this path, and the tests use the fixture backend.
73	
74	## Questions for Chris
75	
76	- For F1: should a picked sentence that a hedge qualifies get the hedge added automatically (option a), or keep the refusal and name the hedge in the message (option b)?
77	- For F2: is a pasted record that starts with `Excerpt: "..."` and has no Date or Source line an expected live input, or out of scope for the prototype?
78	
79	```json
80	{"card": "T-108", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
81	 "scope": "commit d3e127c (git archive copy, scratchpad T108_verify); app/backend/present.py, tests/unit/test_quote_units.py, tests/e2e/test_change_the_quote.py, tests/e2e/conftest.py; app: archive server on 127.0.0.1:7971 (ZLAYT_DB scratch sqlite, DATA_DIR empty sentinel, LLM_BACKEND=fixture), not :7860; sample and evals/golden case_01..case_09",
82	 "exercised": [
83	  "git archive d3e127c copy; second archive copy diff -rq identical (pycache only)",
84	  ".venv/bin/python -m pytest -q tests/unit on the archive copy: 2077 passed, 4 skipped (artifacts/review-evidence/T-108/unit-run.txt)",
85	  "pytest tests/unit/test_quote_units.py -v: 13 passed",
86	  "probe_units.py: 10 cases, 59 records, 150 units through spanish.module_for(...).check_excerpt, alone and with trailing hedge chain (probe-units-output.json)",
87	  "probe_shapes2.py: synthetic record shapes A-F through ingest.split_records + present.quote_body (probe-shapes-output.txt)",
88	  "real backend on 127.0.0.1:7971: tests/e2e/test_change_the_quote.py 3 passed; ZLAYT_DB scratch file written, DATA_DIR sentinel empty (e2e-head-run.txt)",
89	  "single_unit.py: POST /api/cases/{tok}/items/e8/review with unit 0 alone -> 422 invalid_edit EXCERPT_OMITS_QUALIFIER (single-unit-output.txt)",
90	  "mutant M1 (quote_body returns (0, block)): 13 unit quote tests failed, 3 e2e failed on :7972 (mutant-M1-unit.txt, mutant-M1-e2e.txt)",
91	  "mutant M2 (present.py:165 if False:): 13 unit quote tests passed (mutant-M2-unit.txt)",
92	  "pytest --collect-only tests/unit on archive (2081) and on live tree at 1526a1f (2206)",
93	  "read present.py, sentences.py, grounding.py check_excerpt, spanish_text.py check_excerpt, review.py edit and manual_entry, store.py load_records, ingest.py _excerpt_extent, api.py demo gate, excerpt.js, manual.js, the three test files"
94	 ],
95	 "verdict": "changes",
96	 "scores": {"deterministic_no_llm": 5, "golden_units_clean": 5, "save_route_parity": 3, "edge_shapes_clean": 2, "silent_fallback_honesty": 2, "test_strength": 3, "e2e_real_backend": 4, "evidence_reproducible": 3},
97	 "findings": [
98	  {"severity": "major",
99	   "title": "A sentence that a hedge qualifies cannot be picked alone; the picker never adds the hedge and the unit test helper models a picker that does not exist",
100	   "evidence": "app/frontend/excerpt.js:35 (pick only moves lo/hi), :38 (text from units[lo].start to units[hi].end); tests/unit/test_quote_units.py:25 docstring and _pick at :24-30; artifacts/review-evidence/T-108/single-unit-output.txt: sample r8 unit 0 alone -> 422 invalid_edit EXCERPT_OMITS_QUALIFIER; probe-units-output.json alone_fail: sample r8 x2, case_08 r2 (3 of 150)",
101	   "why_it_matters": "The card AC says picking whole sentences yields a valid verbatim quote on sample and case_01..09; it does not for 3 sentences. The green unit test passes only because _pick adds the hedge the UI never adds.",
102	   "fix": "Either (a) excerpt.js extends a single selection through the trailing hedge run and checks those boxes, or (b) keep the UI, restate the AC and the docstring, and test the UI rule (unit alone -> 422 EXCERPT_OMITS_QUALIFIER; unit plus hedge chain -> 201).",
103	   "acceptance_test": "For sample r8 unit 0 and case_08 r2 unit 0, the UI-built text is saved (201) under (a) or refused with EXCERPT_OMITS_QUALIFIER under (b). The test submits the UI-built text, not the _pick text, and fails if the picker stops extending."},
104	  {"severity": "major",
105	   "title": "quote_body falls back silently to the whole record block; label-only and date-less records leak Excerpt: and header lines into the picker",
106	   "evidence": "app/backend/present.py:160-163 (try split_records / except Exception: body = block) and :167-168 (block.find(body); return (0, block) on miss); artifacts/review-evidence/T-108/probe-shapes-output.txt: A_excerpt_only units=['Excerpt: \"Pain persists after two weeks.', 'Taking meds daily.\"'], C_source_excerpt units=['Source: Synthetic Clinic', 'Excerpt: \"Pain persists after two weeks.', 'Taking meds daily.\"']; api.py:287-288 demo gate (409 with ENABLE_LIVE unset)",
107	   "why_it_matters": "The commit's invariant fails silently on a reachable input shape that the golden set does not contain. The broad except and whole-block return turn a split failure into the bug this card fixes, with no status shown. Silent fallback (persona 4.12). Not a blocker: no fact is invented and the save route still checks verbatim. Reachability in live mode is inferred from code; live mode not exercised.",
108	   "fix": "A record whose body cannot be located yields no units and a visible state (for example record_warning), not the block. Remove the broad except so the split error surfaces. Strip the Excerpt: label and Date:/Source: lines for unsplit records, or classify the record as unsplit with its own state.",
109	   "acceptance_test": "test_quote_body_cases (tests/unit/test_quote_units.py:80) gains shapes A and C: no unit starts with Excerpt or Source:, no unit contains a double quote; an unsplittable record yields no units plus a reason. The current (0, block) branch must fail it."},
110	  {"severity": "minor",
111	   "title": "Removing the label/quote-mark offset branch passes every quote test; header repeating the body gives a wrong offset",
112	   "evidence": "app/backend/present.py:164-166; artifacts/review-evidence/T-108/mutant-M2-unit.txt: 13 passed with if False: at present.py:165; probe-shapes-output.txt F_header_repeats_body base=69 vs block.find=25",
113	   "why_it_matters": "The 'at their true offsets' claim is untested for repeated text. Only test_quote_body_cases line 83 touches offsets and its body appears once.",
114	   "fix": "Add shape F to test_quote_body_cases; assert raw[u.start:u.end] == u.text and u.start inside the excerpt body.",
115	   "acceptance_test": "Mutant M2 fails the new shape F assertion."},
116	  {"severity": "minor",
117	   "title": "Curly quotes survive as wrapper; quote-mark assertions cover the sample only",
118	   "evidence": "app/backend/ingest.py:63 strips only straight quotes; probe-shapes-output.txt D_curly_quotes units=['“Pain persists after two weeks.', 'Taking meds daily.”']; tests/unit/test_quote_units.py:59-66 and tests/e2e/test_change_the_quote.py:27 and :51 are sample-only; test_quote_units.py:49 checks startswith only",
119	   "why_it_matters": "The card and brief require no quote marks in units. Word-pasted records keep curly marks. Golden cases are clean today (probe-units-output.json wrapper 0), so this is latent.",
120	   "fix": "Strip matched curly pairs in the excerpt extent or give the record a state; extend the quote-mark assertion at test_quote_units.py:49 to every case.",
121	   "acceptance_test": "Shape D yields units with no curly or straight double quote marks, and the line-49 assertion covers case_01..09."},
122	  {"severity": "minor",
123	   "title": "The 2110 passed evidence does not reproduce at the cited commit",
124	   "evidence": "board card T-108 AC evidence 'tests/unit full run 2110 passed'; artifacts/review-evidence/T-108/unit-run.txt: 2077 passed, 4 skipped; pytest --collect-only at d3e127c: 2081 collected; live tree at 1526a1f with 1291 untracked files and uncommitted edits: 2206 collected",
125	   "why_it_matters": "Evidence must match the commit it cites. The 2110 figure probably comes from a different tree.",
126	   "fix": "Rerun at d3e127c and name the commit and the pytest tail line in the AC evidence.",
127	   "acceptance_test": "AC evidence names d3e127c and the tail line that reproduces it."},
128	  {"severity": "minor",
129	   "title": "The frontend strips the wrapper again in manual.js, which can hide a backend regression",
130	   "evidence": "app/frontend/manual.js:14-23 (quotable(rec) drops ===/Date:/Source: lines, the Excerpt: label and a trailing quote from rec.sentences)",
131	   "why_it_matters": "A backend leak would be hidden in the manual-entry tray, and the rule now lives in two places that can drift.",
132	   "fix": "The tray takes backend units as they are, and the rule has one copy.",
133	   "acceptance_test": "A unit fixture with an Excerpt: prefix shown in the tray fails the test."},
134	  {"severity": "minor",
135	   "title": "The excerpt-error hidden check in the e2e runs before the save response and passes at once",
136	   "evidence": "tests/e2e/test_change_the_quote.py:59 expect(excerpt-error).to_be_hidden() right after btn-save-excerpt click; real check is the poll at :60-65",
137	   "why_it_matters": "A required AC test carries a check that cannot fail at that point. The final assert still protects the outcome.",
138	   "fix": "Wait for the save response (expect_response) or drop line 59.",
139	   "acceptance_test": "The spec passes on the fixed build and fails when the picker submit is broken."},
140	  {"severity": "nit",
141	   "title": "_pick is misnamed",
142	   "evidence": "tests/unit/test_quote_units.py:24-30 builds the quote the picker should build",
143	   "why_it_matters": "Name suggests it mirrors the UI, which F1 shows it does not.",
144	   "fix": "Rename to _hedge_chain_quote once F1 is decided.",
145	   "acceptance_test": "None needed beyond F1."}
146	 ],
147	 "whats_right": [
148	  "Units come from the save-route body at absolute offsets: 150 units, zero not-verbatim, out-of-block or wrapper hits on sample and case_01..09; zero pick failures once the trailing hedge is included",
149	  "Reverting to whole-block units fails all 13 quote unit tests and all 3 real-backend e2e tests (mutant-M1-unit.txt, mutant-M1-e2e.txt)",
150	  "The picker's quote check is the save routes' own call (spanish.module_for check_excerpt, review.py:300 and :451); no LLM on this path, fixture backend in tests"
151	 ],
152	 "questions_for_chris": [
153	  "F1: should a picked sentence that a hedge qualifies get the hedge added automatically (option a), or keep the refusal and name the hedge in the message (option b)?",
154	  "F2: is a pasted record that starts with Excerpt: and has no Date or Source line an expected live input, or out of scope for the prototype?"
155	 ]}
156	```
157	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:30.635Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t108_quote_units_patterns.md"
}
````

### User / tool · 2026-11-02T06:38:30.641Z

**tool result**
````
1	---
2	name: project_t108_quote_units_patterns
3	description: T-108 r1 d3e127c (changes): test helper builds a hedge chain the picker never adds, quote_body silent whole-block fallback leaks Excerpt label, offset branch mutant survives, curly quotes
4	metadata:
5	  type: project
6	---
7	
8	T-108 r1 (d3e127c, quote-picker units from the excerpt body; reviews/T-108-staff-engineer.md; changes: 0 blockers, 2 majors, 5 minors, 1 nit).
9	
10	- **A test helper that models the UI but is not the UI.** `_pick` in tests/unit/test_quote_units.py added the trailing hedge chain, and its docstring says the picker does too. excerpt.js `pick(i)` never adds it, so 3 of 150 units (sample r8 two units, case_08 r2) are refused when picked alone (422 EXCERPT_OMITS_QUALIFIER) while the unit test stays green. How to apply: when a test builds the input "the way the UI does", diff it against the UI source and submit the UI-built text in the probe.
11	- **Wrapper-stripping helper with a whole-block fallback.** `quote_body` has `except Exception: body = block` and `return (0, block)` on a miss, so a record with only an `Excerpt:` line (no Date/Source) gets the label and header lines back in the units. Reachable only in live mode (demo gate api.py:287-288 refuses pasted text). How to apply: for any helper that strips wrappers, probe the shapes the golden set lacks: label-only, date-less, curly quotes, a header that repeats the body.
12	- **Surviving mutant on a redundant branch.** Disabling the label-offset branch (present.py:165) passes all 13 quote tests because `block.find(body)` gives the same offset on golden data. It differs only when the body text also appears in the header (shape F: base 69 vs find 25). How to apply: when a mutant survives, check whether a fallback makes the branch equivalent on the inputs tested, then build the input that separates them.
13	- **Exemplary parts.** Reverting to whole-block units fails 13/13 unit and 3/3 real-backend e2e. The save-route check is the same call the picker is tested against (review.py:300 and :451).
14	- **Count does not reproduce.** The card cites "tests/unit 2110 passed"; at d3e127c collect-only gives 2081 and the run gives 2077 passed, 4 skipped. Live HEAD had moved to 1526a1f with 1291 untracked files. How to apply: collect at the cited commit, not the live tree.
15	- **Real-backend e2e method that worked.** `git archive <sha>` copy; server with `HOST`, `PORT`, `ZLAYT_DB` (scratch sqlite) and `DATA_DIR` (empty sentinel); `E2E_BASE_URL` pointing at it; mutant server on a second port; stop both by PID from `lsof -nP -iTCP:<port> -sTCP:LISTEN -t`.
16	
17	Environment: git-guard denies Bash commands that contain backslash escapes or backticks ("could not parse command safely"). Put the check in a script written with the Write tool under artifacts/review-evidence and run that.
18	
19	Related: [[feedback_shared_scratchpad]], [[project_t080_trace_review_patterns]], [[feedback_review_write_once]], [[project_e2e_contract_review_patterns]].
20	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:31.137Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>/dev/null; git log --oneline -5 2>/dev/null; git cat-file -t a271014 2>/dev/null",
 "description": "Check git state and commit a271014 exists"
}
````

### User / tool · 2026-11-02T06:38:31.256Z

**tool result**
````
true
a271014 fix(backend): every quote-picker unit saves alone: hedge-qualified sentences are combined units; label-only records offer no units with a reason (T-108 r2)
2ab7896 test(qa): controls evidence from a clean worktree of 9217f8a: J3 17/17, J4 11/12 (J4W7 unstable), controls_ok False (T-093 r3)
81aa55e fix(backend): credibility flag keeps the whole period-sentence excerpt through merge and hedge runs; allow-list is exactly D-043's forms (T-092)
bf0c748 docs(architect): LLM_VS_CODE row 11 code-proposed conflicts; D-047 to D-052 in rows and ADR-019 (T-109)
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
commit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:34.157Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git rev-parse --short a271014 && git show --stat a271014 | head -40 && ls artifacts/review-evidence/T-108/ 2>/dev/null",
 "description": "Show HEAD, commit stats and evidence dir"
}
````

### User / tool · 2026-11-02T06:38:34.293Z

**tool result**
````
a2710140214365c5ef6e8c8d04268cc77ca5d8d5
a271014
commit a2710140214365c5ef6e8c8d04268cc77ca5d8d5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:38:11 2026 -0600

    fix(backend): every quote-picker unit saves alone: hedge-qualified sentences are combined units; label-only records offer no units with a reason (T-108 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/present.py         |  54 ++++++++++---
 memory/contracts/api.md        |   2 +-
 tests/unit/test_quote_units.py | 176 +++++++++++++++++++++++++++++++++--------
 3 files changed, 184 insertions(+), 48 deletions(-)
check_review.py
e2e-head-run.txt
mutant-M1-e2e.txt
mutant-M1-unit.txt
mutant-M2-unit.txt
mutate.py
probe-shapes-output.txt
probe-units-output.json
probe_shapes2.py
probe_units.py
single-unit-output.txt
single_unit.py
unit-quote-tests.txt
unit-run.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:36.310Z

**tool call — Bash**
````
{
 "command": "git show a271014 -- app/backend/present.py memory/contracts/api.md",
 "description": "Show the present.py and api.md diff for the commit"
}
````

### User / tool · 2026-11-02T06:38:36.409Z

**tool result**
````
commit a2710140214365c5ef6e8c8d04268cc77ca5d8d5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:38:11 2026 -0600

    fix(backend): every quote-picker unit saves alone: hedge-qualified sentences are combined units; label-only records offer no units with a reason (T-108 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/present.py b/app/backend/present.py
index 56098ec..212798f 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -148,24 +148,54 @@ def record_view(r, raw, with_sentences=True, pages=None):
         from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
         v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
     if with_sentences:
-        base, body = quote_body(block)           # T-108: units come from the quotable body only, the same text the save route checks the quote against
-        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in sentences.stripped_spans(body)]
+        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
+        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
+        v["sentences"] = [{"text": body[a:b], "start": r["char_start"] + base + a, "end": r["char_start"] + base + b} for a, b in units]
+        if why_none:
+            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
     return v
 
 
+NO_UNITS_LAYOUT = ("No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, "
+                   "so a quote cut from it could not be checked against the record. Read the record text instead.")
+_LABEL_LINE = re.compile(r"^[ \t]*(?:Excerpt:|Date:|Source:|=== Record \d+ ===)", re.MULTILINE)
+
+
 def quote_body(block):
-    """(offset in block, text) of the part of a record a quote can be cut from: the excerpt body, without the date/source/header lines, the
-    `Excerpt:` label and the quote marks around a quoted block. It is the string review.py / generator.py check a saved quote against (rec["excerpt"]),
-    found at its true position in the block, so every unit cut from it is a verbatim slice of the record text."""
+    """(offset in block, text, reason) of the part of a record a quote can be cut from: the excerpt body, without the date/source/header
+    lines, the `Excerpt:` label and the quote marks around a quoted block. The text is the string review.py / generator.py check a saved quote
+    against (rec["excerpt"]), found at its true position in the block (searched from the end of the `Excerpt:` label, so a Source line that
+    repeats the text is not mistaken for it), so every unit cut from it is a verbatim slice of the record text.
+    A record whose excerpt still carries label or header lines (no Date/Source line, so the layout was not recognised) or whose body cannot be
+    located gives (0, "", reason): no unit is offered, because a quote cut without the label would not be whole sentences of the text the
+    save route checks against."""
     try:
         body = ingest.split_records(block)[0]["excerpt"]
-    except Exception:
-        body = block
-    m = re.search(r"^Excerpt:[ \t]*\"?", block, re.MULTILINE)
-    if m and body and block[m.end():].startswith(body[:20]):
-        return m.end(), body
-    i = block.find(body) if body else -1
-    return (i, body) if i >= 0 else (0, block)
+    except ingest.IngestError:
+        return 0, "", NO_UNITS_LAYOUT
+    if not body or _LABEL_LINE.search(body):
+        return 0, "", NO_UNITS_LAYOUT
+    m = ingest._F_EXC.search(block)
+    i = block.find(body, m.end() if m else 0)
+    if i < 0:
+        return 0, "", NO_UNITS_LAYOUT
+    return i, body, None
+
+
+def quote_units(body, rec):
+    """Whole-sentence spans of `body` the quote picker offers. A sentence that a hedge sentence qualifies cannot be saved without it
+    (EXCERPT_OMITS_QUALIFIER), so it is offered as ONE combined unit with the hedge sentence(s) that follow it: the same check the save
+    routes run (language module for the record, Spanish hedge words included) decides, so every unit offered saves on its own."""
+    check = spanish.module_for(language.record_lang(rec)).check_excerpt
+    spans = sentences.stripped_spans(body)
+    out, i = [], 0
+    while i < len(spans):
+        j = i
+        while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
+            j += 1
+        out.append((spans[i][0], spans[j][1]))
+        i = j + 1
+    return out
 
 
 def case_view(conn, case_id, *, backend, models, demo_mode):
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index 9054d92..b842889 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -243,7 +243,7 @@ Read once, then patch local state from review responses. `entries` are **chronol
   "created_at": "2026-11-02T01:00:00Z", "updated_at": "2026-11-02T01:03:10Z"
 }
 ```
-(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
+(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). **T-108:** units are cut from the quotable excerpt body only (no `Excerpt:` label, quote marks or Date/Source/=== lines), at true offsets, and every unit saves on its own: a sentence that a hedge sentence qualifies is ONE combined unit with the hedge sentence(s) after it (the save route's own check decides, Spanish hedge words included), so the picker never builds a quote the route refuses. A record whose Excerpt label cannot be separated from its text (no Date/Source layout) has `sentences: []` and a plain-words `sentences_reason`; the frontend shows no picker for it. `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
 
 ## POST /api/cases/{token}/records/{rid}/confirm_date
 Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot be confirmed; it stays excluded and flagged. Request:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:36.565Z

**tool call — Bash**
````
{
 "command": "git show a271014 -- tests/unit/test_quote_units.py",
 "description": "Show the test file diff for the commit"
}
````

### User / tool · 2026-11-02T06:38:36.658Z

**tool result**
````
commit a2710140214365c5ef6e8c8d04268cc77ca5d8d5
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 00:38:11 2026 -0600

    fix(backend): every quote-picker unit saves alone: hedge-qualified sentences are combined units; label-only records offer no units with a reason (T-108 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_quote_units.py b/tests/unit/test_quote_units.py
index ffa16af..d314274 100644
--- a/tests/unit/test_quote_units.py
+++ b/tests/unit/test_quote_units.py
@@ -1,6 +1,10 @@
 """T-108: the quote picker's sentence units (record_view 'sentences') are cut from the quotable body of a record only: no
 `Excerpt:` label, no quote marks around a quoted block, no Date:/Source:/=== header lines. Each unit is a verbatim slice of the case text
-at whole-sentence boundaries and passes the same check the save routes run (review.edit / review.manual_entry -> check_excerpt)."""
+at whole-sentence boundaries and passes the same check the save routes run (review.edit / review.manual_entry -> check_excerpt),
+ALONE: the picker submits exactly raw[unit.start:unit.end] (app/frontend/excerpt.js), so a sentence that a hedge sentence qualifies is offered as one
+combined unit with its hedge (T-108 r2). A record whose Excerpt label cannot be separated from its text offers no units and says why."""
+import pathlib
+
 import pytest
 from fastapi.testclient import TestClient
 
@@ -10,6 +14,7 @@ from app.db import db as DB
 from tests.unit import _golden as G
 
 CASES = G.case_names()
+LIBRARY = sorted(p.stem for p in (pathlib.Path(__file__).resolve().parents[2] / "evals" / "library").glob("*.txt"))
 
 
 @pytest.fixture
@@ -21,39 +26,100 @@ def env(tmp_path, monkeypatch):
     return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
 
 
-def _pick(rec_text, units, i):
-    """The quote the picker builds for unit i: the unit plus any hedge units that immediately follow it (the qualifier has to travel with it)."""
-    from app.backend.grounding import is_hedge_unit
-    j = i
-    while j + 1 < len(units) and is_hedge_unit(units[j + 1]["text"]):
-        j += 1
-    return units[i]["start"], units[j]["end"]
+def _case(env, monkeypatch, body):
+    db, c = env
+    tok = c.post("/api/cases", json=body).json()["token"]
+    return db, c, tok
 
 
-@pytest.mark.parametrize("name", CASES)
-def test_every_offered_unit_is_a_valid_quote(env, name):
-    db, c = env
-    text = G.raw(name)
-    tok = c.post("/api/cases", json={"text": text}).json()["token"]
+def _check_all_units(db, c, tok, label):
+    """Every offered unit, built the way the picker builds it (the text from unit.start to unit.end, nothing added), passes the save-route check."""
     case = c.get(f"/api/cases/{tok}").json()
     conn = DB.connect(db)
     raw = DB.get_case(conn, tok)["raw_text"]
     recs = {r["id"]: r for r in store.load_records(conn, tok, raw)}
-    n_units = 0
+    n = 0
     for rv in case["records"]:
         rec = recs[rv["id"]]
-        for i, u in enumerate(rv["sentences"]):
-            n_units += 1
-            assert raw[u["start"]:u["end"]] == u["text"], "a unit is a verbatim slice of the case text"
+        for u in rv["sentences"]:
+            n += 1
+            quote = raw[u["start"]:u["end"]]
+            assert quote == u["text"], "a unit is a verbatim slice of the case text"
             assert rv["char_start"] <= u["start"] < u["end"] <= rv["char_end"]
-            assert not u["text"].startswith(("Excerpt:", "Date:", "Source:", "===")), u["text"]
-            a, b = _pick(rv["text"], rv["sentences"], i)
-            quote = raw[a:b]
+            assert not u["text"].startswith(("Excerpt", "Date:", "Source:", "===")), u["text"]
+            assert not any(q in u["text"] for q in ('"', "\u201c", "\u201d")), u["text"]
             problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], quote)
-            assert problems == [], (name, rv["id"], quote, problems)
+            assert problems == [], (label, rv["id"], quote, problems)
             assert grounding.locate(rec["excerpt"], quote) is not None
-    assert n_units
     conn.close()
+    return n, case
+
+
+@pytest.mark.parametrize("name", CASES)
+def test_every_offered_unit_saves_alone_golden(env, monkeypatch, name):
+    db, c = env
+    tok = c.post("/api/cases", json={"text": G.raw(name)}).json()["token"]
+    assert _check_all_units(db, c, tok, name)[0]
+
+
+def test_every_offered_unit_saves_alone_sample(env):
+    db, c = env
+    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
+    n, case = _check_all_units(db, c, tok, "sample")
+    assert n
+    raw = DB.get_case(DB.connect(db), tok)["raw_text"]
+    by_rec = {e["record_ids"][0]: e for e in case["entries"] + case["undated_entries"] if len(e["record_ids"]) == 1}
+    for rv in case["records"]:                 # the real routes a picked quote goes to, for every unit of every record
+        for u in rv["sentences"]:
+            q = raw[u["start"]:u["end"]]
+            e = by_rec.get(rv["id"])
+            if e:                              # "Change the quote": POST .../items/{id}/review {action: edit, edits: {excerpt}}
+                r = c.post(f"/api/cases/{tok}/items/{e['id']}/review", json={"action": "edit", "edits": {"excerpt": q}})
+                reasons = (r.json().get("error", {}).get("detail") or {}).get("reasons", []) if r.status_code != 200 else []
+                assert not set(reasons) & {"EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "GROUNDING_EXCERPT_NOT_VERBATIM"}, (rv["id"], q, r.text)
+                assert r.status_code != 422 or r.json()["error"]["code"] != "invalid_edit", (rv["id"], q, r.text)
+            else:                              # record without an entry (tray): manual entry; the first unit saves, later ones meet "already has an entry"
+                r = c.post(f"/api/cases/{tok}/records/{rv['id']}/entry", json={"summary": q, "excerpt": q})
+                assert r.status_code == 201 or "already has an entry" in r.text, (rv["id"], q, r.text)
+
+
+@pytest.mark.parametrize("lib", LIBRARY)
+def test_every_offered_unit_saves_alone_library(tmp_path, monkeypatch, lib):
+    monkeypatch.setenv("LLM_BACKEND", "fixture")
+    monkeypatch.setenv("ZLAYT_MODE", "local")
+    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    db = str(tmp_path / "l.sqlite")
+    c = TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
+    r = c.post("/api/cases", json={"library": lib})
+    assert r.status_code == 201, r.text
+    _check_all_units(db, c, r.json()["token"], lib)
+
+
+def test_hedge_qualified_sentence_is_one_combined_unit(env):
+    """Sample record 8: 'C5-C6 disc protrusion with mild right foraminal narrowing.' is qualified by the hedge sentence after it, so it is
+    offered together with it; the unit alone saves (201), while the bare sentence is still refused by the route (the rule is unchanged)."""
+    db, c = env
+    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
+    r8 = next(r for r in c.get(f"/api/cases/{tok}").json()["records"] if r["id"] == "r8")
+    texts = [s["text"] for s in r8["sentences"]]
+    first = next(t for t in texts if t.startswith("C5-C6 disc protrusion with mild right foraminal narrowing."))
+    assert first != "C5-C6 disc protrusion with mild right foraminal narrowing." and len(first) > len("C5-C6 disc protrusion with mild right foraminal narrowing.")
+    raw = DB.get_case(DB.connect(db), tok)["raw_text"]
+    bare = "C5-C6 disc protrusion with mild right foraminal narrowing."
+    assert c.post(f"/api/cases/{tok}/records/r8/entry", json={"summary": bare, "excerpt": bare}).status_code == 422
+    assert c.post(f"/api/cases/{tok}/records/r8/entry", json={"summary": first, "excerpt": first}).status_code == 201
+    assert bare not in texts
+
+
+def test_golden_hedge_qualified_sentences_are_combined(env):
+    """case_08: 'Signal change in the supraspinatus tendon.' is qualified by the hedge sentence after it; it is never offered bare."""
+    db, c = env
+    name = next(n for n in CASES if n.startswith("case_08"))
+    tok = c.post("/api/cases", json={"text": G.raw(name)}).json()["token"]
+    texts = [s["text"] for r in c.get(f"/api/cases/{tok}").json()["records"] for s in r["sentences"]]
+    assert "Signal change in the supraspinatus tendon." not in texts
+    assert any(t.startswith("Signal change in the supraspinatus tendon.") and len(t) > len("Signal change in the supraspinatus tendon.") for t in texts)
 
 
 def test_sample_units_have_no_wrapper(env):
@@ -63,24 +129,64 @@ def test_sample_units_have_no_wrapper(env):
     texts = [s["text"] for s in r1["sentences"]]
     assert texts[0] == "41M restrained driver, rear-ended at approx. 35 mph."
     assert texts[-1] == "Transported to Central ER."          # no closing quote mark
+    assert "sentences_reason" not in r1
     assert not any("Excerpt" in t or '"' in t or t.startswith(("Date:", "Source:")) for t in texts)
 
 
-def test_sample_save_route_accepts_picked_units(env):
-    """The route a picked quote goes to (POST /records/{rid}/entry) accepts a quote built from the offered units on every record of the sample."""
-    db, c = env
-    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
-    for rv in c.get(f"/api/cases/{tok}").json()["records"]:
-        a, b = _pick(rv["text"], rv["sentences"], 0)
-        raw = DB.get_case(DB.connect(db), tok)["raw_text"]
-        r = c.post(f"/api/cases/{tok}/records/{rv['id']}/entry", json={"summary": raw[a:b], "excerpt": raw[a:b]})
-        assert r.status_code == 201, (rv["id"], r.text)
+def _units_of(block, rec=None):
+    base, body, why = present.quote_body(block)
+    if why:
+        return why, []
+    units = present.quote_units(body, {"excerpt": body, **(rec or {})})
+    return None, [(base + a, base + b) for a, b in units]
 
 
 def test_quote_body_cases():
     blk = '=== Record 1 ===\nDate: 2026-01-01\nSource: X\nExcerpt: "One. Two."'
-    off, body = present.quote_body(blk)
-    assert body == "One. Two." and blk[off:off + len(body)] == body
+    off, body, why = present.quote_body(blk)
+    assert why is None and body == "One. Two." and blk[off:off + len(body)] == body
     assert present.quote_body("Date: 2026-01-01\nSource: X\nExcerpt: Plain text here.")[1] == "Plain text here."
-    off, body = present.quote_body("Just a paragraph with no labels. Second one.")
-    assert body == "Just a paragraph with no labels. Second one." and off == 0
+    off, body, why = present.quote_body("Just a paragraph with no labels. Second one.")
+    assert why is None and body == "Just a paragraph with no labels. Second one." and off == 0
+
+
+@pytest.mark.parametrize("txt", ['Excerpt: "Pain persists after two weeks. Taking meds daily."',
+                                 'Source: Synthetic Clinic\nExcerpt: "Pain persists after two weeks. Taking meds daily."',
+                                 'Date: 2026-01-05\nExcerpt: "Pain persists after two weeks. Taking meds daily."'])
+def test_label_only_or_header_missing_records_offer_no_units(txt):
+    """T-108 r2 F2: a record with an Excerpt label but no full Date/Source layout keeps the label in the text the save route checks against;
+    no unit is offered (never the whole block), and the reason is plain words."""
+    recs = ingest_records(txt)
+    for rec in recs:
+        why, units = _units_of(rec["text"])
+        if "Excerpt:" in rec["excerpt"] or "Source:" in rec["excerpt"]:
+            assert units == [] and why == present.NO_UNITS_LAYOUT
+        else:                                       # date+excerpt: the body is separable, units carry no label or quote mark
+            assert why is None and units
+            for a, b in units:
+                t = rec["text"][a:b]
+                assert not t.startswith(("Excerpt", "Source:")) and '"' not in t
+
+
+def ingest_records(txt):
+    from app.backend import ingest
+    return ingest.split_records(txt)
+
+
+def test_record_view_reports_reason_for_label_only_record():
+    r = {"id": "r1", "seq": 1, "source_label": "", "date_raw": "", "date_iso": None, "date_status": "missing", "date_candidates": [],
+         "duplicate_of": None, "injection_tag": 0, "encounter": 0, "char_start": 0, "char_end": 56}
+    raw = 'Excerpt: "Pain persists after two weeks. Taking meds daily."'
+    r["char_end"] = len(raw)
+    v = present.record_view(r, raw)
+    assert v["sentences"] == [] and v["sentences_reason"] == present.NO_UNITS_LAYOUT
+
+
+def test_units_sit_at_true_offsets_when_source_repeats_the_body():
+    """T-108 r2 F3: the Source line repeats the excerpt text; offsets still point into the Excerpt, not the Source line."""
+    blk = 'Date: 2026-01-05\nSource: Pain persists. Taking meds daily.\nExcerpt: "Pain persists. Taking meds daily."'
+    why, units = _units_of(blk)
+    assert why is None and len(units) == 2
+    ex = blk.index('Excerpt:')
+    for a, b in units:
+        assert a > ex and blk[a:b] in ("Pain persists.", "Taking meds daily.")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:40.138Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/T108_r2_verify\" && cd /Users/arsis/zlayt-pm-project && git archive a271014 | tar -x -C \"$S/T108_r2_verify\" && ls \"$S/T108_r2_verify\" | head -50 && ls \"$S/T108_r2_verify/evals/library\" | wc -l && ls /Users/arsis/zlayt-pm-project/.venv/bin/python && ls \"$S/T108_r2_verify/evals/golden\" | head -30",
 "description": "Extract a271014 archive into scratchpad verify dir"
}
````

### User / tool · 2026-11-02T06:38:40.545Z

**tool result**
````
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
      30
/Users/arsis/zlayt-pm-project/.venv/bin/python
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:43.194Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls \"$S/T108_r2_verify/evals/library\"; ls \"$S/T108_r2_verify/tests/unit\" | grep -i -E \"quote|golden|_G|_g\" ; ls \"$S/T108_r2_verify/tests/unit/_golden.py\" && sed -n 1,60p \"$S/T108_r2_verify/tests/unit/_golden.py\"",
 "description": "List library packets and golden helper module"
}
````

### User / tool · 2026-11-02T06:38:43.290Z

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
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
_golden.py
test_gaps.py
test_generator.py
test_grounding.py
test_grounding_may.py
test_judge_guard.py
test_quote_units.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T108_r2_verify/tests/unit/_golden.py
"""Helpers: load golden records/expected files from evals/golden (the only test data; synthetic)."""
import json, pathlib, re
G = pathlib.Path(__file__).resolve().parents[2] / "evals" / "golden"

def case_names():
    return sorted(p.name[:-len(".expected.json")] for p in G.glob("*.expected.json"))

def expected(case):
    return json.loads((G / f"{case}.expected.json").read_text())

def raw(case):
    return (G / f"{case}.txt").read_text()

def records(case):
    """[{n, date_raw, source, excerpt}] parsed from the golden paste format."""
    out = []
    for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', raw(case)):
        out.append(dict(n=int(m.group(1)), date_raw=m.group(2), source=m.group(3), excerpt=m.group(4)))
    return out

def record(case, n):
    return next(r for r in records(case) if r["n"] == n)

def export_blocks():
    t = (G / "sample.export.expected.txt").read_text()
    letter, notes = t.split("=== INTERNAL_NOTES_TEXT")
    return letter.split("\n", 1)[1], notes.split("\n", 1)[1]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:46.941Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && timeout 580 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit > \"$S/unit-run-r2.txt\" 2>&1; echo EXIT=$?; tail -15 \"$S/unit-run-r2.txt\"",
 "description": "Run unit test suite on a271014 archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:38:47.027Z

**tool result**
````
EXIT=127
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:38:49.291Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit > \"$S/unit-run-r2.txt\" 2>&1; echo EXIT=$?; tail -15 \"$S/unit-run-r2.txt\"",
 "description": "Run unit test suite on a271014 archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:41:32.434Z

**tool result**
````
EXIT=0
........................................................................ [ 61%]
........................................................................ [ 64%]
........................................................................ [ 67%]
........................................................................ [ 70%]
........................................................................ [ 73%]
........................................................................ [ 77%]
........................................................................ [ 80%]
........................................................................ [ 83%]
..............................................s......................... [ 86%]
........................................................................ [ 90%]
........................................................................ [ 93%]
........................................................................ [ 96%]
........................................................................ [ 99%]
........                                                                 [100%]
2236 passed, 4 skipped in 161.76s (0:02:41)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:41:36.760Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-108/probe_units.py; echo ----; cat artifacts/review-evidence/T-108/probe_shapes2.py | head -60",
 "description": "Read existing round-1 probe scripts for reuse"
}
````

### User / tool · 2026-11-02T06:41:36.848Z

**tool result**
````
"""Probe (scratch only): every offered quote-picker unit on sample + case_01..09 against the save-route check."""
import os, sys, json, tempfile
os.environ["LLM_BACKEND"] = "fixture"
os.environ.pop("ANTHROPIC_API_KEY", None); os.environ.pop("ENABLE_LIVE", None)
ROOT = sys.argv[1]
sys.path.insert(0, ROOT); os.chdir(ROOT)
from fastapi.testclient import TestClient
from app.backend import grounding, language, present, spanish, store
from app.backend.api import create_app
from app.db import db as DB
from tests.unit import _golden as G

tmp = tempfile.mkdtemp(prefix="t108probe")
db = os.path.join(tmp, "p.sqlite")
c = TestClient(create_app(db, static_dir=tmp), client=("127.0.0.1", 50000))
HEDGE_FIRST = lambda u: present.__dict__  # placeholder
names = ["sample"] + [n for n in G.case_names() if n.startswith("case_0") and int(n[5:7]) <= 9]
report = {}
for name in names:
    tok = c.post("/api/cases", json={"sample": True} if name == "sample" else {"text": G.raw(name)}).json()["token"]
    case = c.get(f"/api/cases/{tok}").json()
    conn = DB.connect(db)
    raw = DB.get_case(conn, tok)["raw_text"]
    recs = {r["id"]: r for r in store.load_records(conn, tok, raw)}
    stats = dict(records=0, units=0, alone_fail=[], pick_fail=[], wrapper=[], not_verbatim=[], out_of_block=[], body_mismatch=[])
    for rv in case["records"]:
        stats["records"] += 1
        rec = recs[rv["id"]]
        block = raw[rv["char_start"]:rv["char_end"]]
        for i, u in enumerate(rv["sentences"]):
            stats["units"] += 1
            t = u["text"]
            if raw[u["start"]:u["end"]] != t: stats["not_verbatim"].append((rv["id"], t))
            if not (rv["char_start"] <= u["start"] < u["end"] <= rv["char_end"]): stats["out_of_block"].append((rv["id"], u["start"], u["end"]))
            bad = [m for m in ('Excerpt', 'Date:', 'Source:', '===', '"', "“", "”", "\n") if m in t]
            if bad or t.startswith(("Excerpt", "Date:", "Source:", "===")): stats["wrapper"].append((name, rv["id"], t[:80], bad))
            al = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], raw[u["start"]:u["end"]])
            if al: stats["alone_fail"].append((name, rv["id"], al, t[:70]))
            j = i
            while j + 1 < len(rv["sentences"]) and grounding.is_hedge_unit(rv["sentences"][j + 1]["text"]): j += 1
            q = raw[u["start"]:rv["sentences"][j]["end"]]
            pk = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], q)
            if pk: stats["pick_fail"].append((name, rv["id"], pk, q[:70]))
        # the body the units came from must equal the stored excerpt, and sit at its true position
        if rec["excerpt"] and rv["sentences"]:
            first = rv["sentences"][0]["start"]; last = rv["sentences"][-1]["end"]
            body_span = raw[first:last]
            if grounding.locate(rec["excerpt"], body_span) is None and not rec["excerpt"].startswith(body_span[:5]):
                stats["body_mismatch"].append((rv["id"], body_span[:40]))
    conn.close()
    report[name] = {k: (v if not isinstance(v, list) else len(v)) for k, v in stats.items()}
    report[name]["_samples"] = {k: stats[k][:3] for k in ("alone_fail", "pick_fail", "wrapper", "not_verbatim", "out_of_block", "body_mismatch") if stats[k]}
print(json.dumps(report, ensure_ascii=False, indent=1))
----
"""Probe (scratch only): quote_body on record blocks of synthetic inputs (no API; demo mode refuses custom text)."""
import os, sys
ROOT = sys.argv[1]; sys.path.insert(0, ROOT); os.chdir(ROOT)
from app.backend import ingest, present, sentences
INPUTS = {
 "A_excerpt_only": 'Excerpt: "Pain persists after two weeks. Taking meds daily."',
 "B_date_excerpt": 'Date: 2026-01-05\nExcerpt: "Pain persists after two weeks. Taking meds daily."',
 "C_source_excerpt": 'Source: Synthetic Clinic\nExcerpt: "Pain persists after two weeks. Taking meds daily."',
 "D_curly_quotes": 'Date: 2026-01-05\nSource: Synthetic Clinic\nExcerpt: “Pain persists after two weeks. Taking meds daily.”',
 "E_plain_unsplit": 'Pain persists after two weeks. Taking meds daily.',
 "F_header_repeats_body": 'Date: 2026-01-05\nSource: Pain persists. Taking meds daily.\nExcerpt: "Pain persists. Taking meds daily."',
}
for k, txt in INPUTS.items():
    for rec in ingest.split_records(txt):
        block = rec["text"]
        base, body = present.quote_body(block)
        units = [body[a:b] for a, b in sentences.stripped_spans(body)]
        true_off = block.find(body)
        print(k, "| stored excerpt=%r" % rec["excerpt"][:60])
        print("    units=%r" % units, "| base=%d block.find=%d" % (base, true_off))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:41:45.950Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && cat evals/golden/unsplit_paste.txt; echo ----; head -c 1500 evals/golden/unsplit_paste.split.json; echo; echo ----; grep -rn \"unsplit_paste\" --include=*.py . | head; echo ----; sed -n 110,125p app/backend/api.py; echo ----; sed -n 280,292p app/backend/api.py",
 "description": "Inspect unsplit paste golden and API demo gate"
}
````

### User / tool · 2026-11-02T06:41:46.060Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

May 4, 2026 — Pottsworth Emergency Department
Fell from a ladder at a worksite. Right wrist swelling. X-ray: distal radius fracture. Splint applied.

May 11, 2026 — Dr. Tabitha Wrenfield, orthopedics
Right wrist pain 5/10. Fracture alignment satisfactory. Continue splint for two more weeks.

May 25, 2026 — Dr. Tabitha Wrenfield, orthopedics
Splint removed. Pain 2/10. Begin hand therapy.
----
{
  "schema_version": "golden-split/1",
  "case_id": "unsplit_paste",
  "synthetic": true,
  "input_file": "unsplit_paste.txt",
  "description": "D-031 LLM split fallback: three records pasted with no '=== Record N ===' headers, no Date:/Source: labels and no separator lines. The code split finds one unsplit block; the model proposes boundary offsets; code validates them (contiguous, cover the text, on line starts). Record fields come from code. Every LLM-split record carries the record_warning LLM_SPLIT.",
  "stress_types": ["unsplit_paste", "llm_split"],
  "code_split": {"record_count": 1, "split_method": "ambiguous"},
  "records": [
    {"record_no": 1, "date": "2026-05-04", "source": "Pottsworth Emergency Department", "starts_with": "May 4, 2026"},
    {"record_no": 2, "date": "2026-05-11", "source": "Dr. Tabitha Wrenfield, orthopedics", "starts_with": "May 11, 2026"},
    {"record_no": 3, "date": "2026-05-25", "source": "Dr. Tabitha Wrenfield, orthopedics", "starts_with": "May 25, 2026"}
  ],
  "llm_split": {"split_method": "llm", "warning_code": "LLM_SPLIT", "record_warning_category": "llm_split", "record_warnings_per_record": 1},
  "must_not": [
    {"id": "M1", "statement": "Accepts boundaries that are not on a line start or do not cover the whole text (keeps one record instead)."},
    {"id": "M2", "statement": "Takes any date, provider or excerpt from the model: record fields are parsed by code from the pasted text."},
    {"id": "M3", "statement": "Presents an LLM-
----
evals/run.py:437:    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
evals/run.py:440:    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
evals/run.py:441:    text = (GOLD / "unsplit_paste.txt").read_text()
evals/run.py:864:                               and m["golden_must_not_hits"]["value"] == 0 and m["unsplit_paste"]["value"] is True and m["case_07_total_420"]["value"] is True
evals/run.py:909:    m["unsplit_paste"] = score_unsplit(pipeline, backend)
evals/run.py:1002:          f"| unsplit_paste (LLM split, D-031) | {m['unsplit_paste']['value']} {m['unsplit_paste']['misses']} | true | R-IN-1 |",
tests/unit/test_split_llm.py:17:def test_no_model_for_unsplit_paste_emits_split_rejected_no_model():
tests/unit/test_split_llm.py:97:# ---- recorded fixture replay (python -m app.llm.record evals/golden/unsplit_paste.txt, LLM_FIXTURE_DIR=tests/fixtures/llm/split)
tests/unit/test_split_llm.py:100:EXP = json.loads((ROOT / "evals" / "golden" / "unsplit_paste.split.json").read_text())
tests/unit/test_split_llm.py:115:def test_golden_unsplit_paste_code_split_is_one_block():
----

    # -------------------------------------------------- config (read per call so tests can monkeypatch env)
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))

    def demo_mode():
        return not live_enabled()

    def models():
        return {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5")}

    def conn():
----
        return out

    def make_case(text, name, sample, pdf_pages=None, pdf_extra=None):
        try:
            text = ingest.check_limits(text)                     # empty -> 400, oversize -> 413, before anything else
        except ingest.IngestError as e:
            raise ApiError(_ERR_STATUS.get(e.code, 400), e.code, "Input is empty." if e.code == "bad_request" else "Input is too large.") from None
        if demo_mode() and digest(text) not in allowed_hashes():
            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
        c = conn()
        try:
            now = time.time()
            DB.purge_expired(c, now)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:41:52.004Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && grep -n \"def load_records\" -A30 app/backend/store.py | head -50; echo ----; grep -n \"def record_view\" -A12 app/backend/present.py | head -30; echo ----; grep -n \"_F_EXC\\|def split_records\\|class IngestError\\|def _excerpt_extent\" app/backend/ingest.py | head",
 "description": "Read store.load_records and record_view signatures"
}
````

### User / tool · 2026-11-02T06:41:52.114Z

**tool result**
````
14:def load_records(conn, case_id: str, raw: str = None) -> list:
15-    """Unit-dict records (what gaps.py / generator.py expect) rebuilt from the records table."""
16-    if raw is None:
17-        raw = DB.get_case(conn, case_id)["raw_text"]
18-    out = []
19-    for r in conn.execute("SELECT * FROM records WHERE case_id=? ORDER BY seq", (case_id,)):
20-        d = DB._decode(r)
21-        block = raw[d["char_start"]:d["char_end"]]
22-        try:
23-            body = ingest.split_records(block)[0]["excerpt"]
24-        except Exception:
25-            body = block
26-        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
27-                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
28-    return out
29-
30-
31-def _by_id(records):
32-    return {r["id"]: r for r in records}
33-
34-
35-# ---------------------------------------------------------------- unit dicts for export / totals
36-def export_case(conn, case_id: str) -> dict:
37-    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
38-    case = DB.get_case(conn, case_id)
39-    recs = load_records(conn, case_id, case["raw_text"])
40-    n_of = {r["id"]: r["n"] for r in recs}
41-    rec_of = {r["id"]: r for r in recs}
42-    from app.backend import review as review_mod        # lazy: review imports store
43-    ents = []
44-    for e in DB.list_items(conn, case_id, "entry"):
----
140:def record_view(r, raw, with_sentences=True, pages=None):
141-    block = raw[r["char_start"]:r["char_end"]]
142-    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
143-         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
144-         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
145-         "char_end": r["char_end"], "text": block, "language": language.block_lang(block)}
146-    if pages:                                    # PDF source (D-031): the page where the record starts
147-        v["page"] = pdf_text.page_for(pages, r["char_start"])
148-        from app.backend import pdf_checks            # T-086: true when the record lies on a page read by OCR
149-        v["ocr_derived"] = pdf_checks.is_ocr_span(pages, r["char_start"], r["char_end"])
150-    if with_sentences:
151-        base, body, why_none = quote_body(block)  # T-108: units come from the quotable body only, the same text the save route checks the quote against
152-        units = [] if why_none else quote_units(body, {**r, "excerpt": body})
----
20:_F_EXC = re.compile(r"^Excerpt:[ \t]*", re.MULTILINE)
23:class IngestError(ValueError):
55:    if starts and (_F_SRC.search(text) or _F_EXC.search(text)):
60:def _excerpt_extent(rest: str):
90:    e = _F_EXC.search(block)
206:def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:42:12.674Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && echo \"== frontend refs to sentences / sentences_reason\" && grep -rn \"sentences_reason\\|\\.sentences\\b\" app/frontend | head -20; echo \"== manual_entry dup order\" && grep -n \"already has an entry\\|def manual_entry\\|check_excerpt\\|EXCERPT_OMITS\" app/backend/review.py | head -20; echo \"== split_records raise path\" && sed -n 200,215p app/backend/ingest.py; echo \"== stored excerpt fallback\" && sed -n 20,27p app/backend/store.py",
 "description": "Check frontend use of sentences_reason and entry route order"
}
````

### User / tool · 2026-11-02T06:42:12.804Z

**tool result**
````
== frontend refs to sentences / sentences_reason
app/frontend/manual.js:16:    (rec.sentences || []).forEach((s) => {
app/frontend/narrative.js:56:      if ((nar.sentences || []).length)
app/frontend/narrative.js:57:        root.append(el("ol", { class: "au-list", "data-testid": "narrative-sentences" }, nar.sentences.map((s) => el("li", { class: "au-call", "data-testid": "narrative-sentence" },
app/frontend/narrative.js:67:        el("button", { type: "button", class: "rv-btn", "data-testid": "btn-accept-narrative", "aria-pressed": String(nar.status === "accepted"), disabled: !(nar.sentences || []).length, onclick: () => act("accept", "Paragraph accepted.") }, "Accept paragraph"),
app/frontend/mock.js:96:      r.sentences = ex.sents;
app/frontend/mock.js:98:        const at = r.char_start + r.text.indexOf(t); const sent = r.sentences.find((s) => s.start <= at && at < s.end) || { text: t, start: at, end: at + t.length };
app/frontend/excerpt.js:20:    if (!rec || !rec.sentences || rec.sentences.length < 2 || entry.record_ids.length !== 1) return;
app/frontend/excerpt.js:21:    const units = rec.sentences;
== manual_entry dup order
63:CODE_CHECK_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_NOT_WHOLE_SENTENCE", "EXCERPT_OMITS_QUALIFIER",
66:                   "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge", "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight"}
67:QUOTE_LEVEL_REASONS = ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND")   # only a change to the QUOTE clears these
72:                "GROUNDING_EXCERPT_NOT_VERBATIM": "the quote is not word for word in the record", "EXCERPT_OMITS_QUALIFIER": "the quote leaves out a hedge sentence",
95:        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence
96:            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE"):
120:    elif c == "EXCERPT_OMITS_QUALIFIER":
300:        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
432:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
446:        raise _bad("This record already has an entry; edit that entry instead.")
451:    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
== split_records raise path
                    f["source"] = right.strip()
                    f["excerpt"] = text[s0:e0].split("\n", 1)[1].strip() if "\n" in text[s0:e0] else f["excerpt"]
        out.append(_record(len(out) + 1, text[s0:e0], s0, e0, f))
    return out


def split_records(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_RECORDS) -> list:
    text = check_limits(raw_text, max_chars)
    recs, _ = _split(text)
    if len(recs) > max_records:
        raise IngestError("input_too_large")
    return recs


def record_kind(source: str, excerpt: str = "") -> str:
    """encounter | billing_statement | phone_note (| records_admin), decided by the lexicon `non_encounter` list on the header label only (D-003)."""
== stored excerpt fallback
        d = DB._decode(r)
        block = raw[d["char_start"]:d["char_end"]]
        try:
            body = ingest.split_records(block)[0]["excerpt"]
        except Exception:
            body = block
        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
                    "kind": "encounter" if d["encounter"] else "other", "date_candidates": d["date_candidates"] or []})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:42:18.903Z

**tool call — Bash**
````
{
 "command": "cat board/cards/T-108.md | head -120",
 "description": "Read the T-108 card acceptance criteria"
}
````

### User / tool · 2026-11-02T06:42:18.987Z

**tool result**
````
---
id: "T-108"
title: "Quote picker cannot save a valid quote on the sample: sentence units include the 'Excerpt: \"' wrapper"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:08:42Z"
updated_at: "2026-11-02T06:38:25Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:31:11Z"
rounds: 1
commits: ["d3e127c", "a271014"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-108-staff-engineer.md", "at": "2026-11-02T06:31:11Z"}
ac:
  - {"n": 1, "text": "Sentence units offered by the quote picker exclude labels/wrappers so picking whole sentences yields a valid verbatim quote on sample and case_01..09; 'Change the quote' completes end to end (e2e on the real backend); unit test on the sentence splitter", "done": true, "evidence": "a271014: tests/unit/test_quote_units.py (35 passed): every offered unit, as the picker submits it (raw[start:end], no hedge added), passes the save-route check on sample, case_01..09 and all 15 library packets; sample units also saved through the real entry/edit routes; hedge-qualified sentences are combined units (sample r8, case_08); label-only/date-less records give sentences [] + sentences_reason; Source-repeats-body offsets test. tests/unit full: 2239 passed, 1 skipped at a271014. e2e test_change_the_quote.py 3 passed on own server :7966 with ZLAYT_DB"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T06:08:48Z backend: claimed
- 2026-11-02T06:14:46Z backend: AC 1 checked: d3e127c: tests/unit/test_quote_units.py (sample + case_01..09: every offered unit, plus trailing hedge units, passes check_excerpt; sample records saved via POST /records/{rid}/entry 201) and tests/e2e/test_change_the_quote.py (real backend, ZLAYT_DB, :7957: refused Accept -> Change the quote -> save -> quote restored, accept 200; 3 passed); tests/unit full run 2110 passed, e2e contract fixed (excerpt-error declared)
- 2026-11-02T06:14:46Z backend: moved in_progress -> in_review
- 2026-11-02T06:14:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T06:31:11Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-108-staff-engineer.md; round 1; findings:
    - [major] A sentence that a hedge qualifies cannot be picked alone; the picker never adds the hedge and the unit test helper models a picker that does not exist — fix: Either (a) excerpt.js extends a single selection through the trailing hedge run and checks those boxes, or (b) keep the UI, restate the AC and the docstring, and test the UI rule (unit alone -> 422 EXCERPT_OMITS_QUALIFIER; unit 
    - [major] quote_body falls back silently to the whole record block; label-only and date-less records leak Excerpt: and header lines into the picker — fix: A record whose body cannot be located yields no units and a visible state (for example record_warning), not the block. Remove the broad except so the split error surfaces. Strip the Excerpt: label and Date:/Source: lines for unsplit records,
    - [minor] Removing the label/quote-mark offset branch passes every quote test; header repeating the body gives a wrong offset — fix: Add shape F to test_quote_body_cases; assert raw[u.start:u.end] == u.text and u.start inside the excerpt body.
    - [minor] Curly quotes survive as wrapper; quote-mark assertions cover the sample only — fix: Strip matched curly pairs in the excerpt extent or give the record a state; extend the quote-mark assertion at test_quote_units.py:49 to every case.
    - [minor] The 2110 passed evidence does not reproduce at the cited commit — fix: Rerun at d3e127c and name the commit and the pytest tail line in the AC evidence.
    - [minor] The frontend strips the wrapper again in manual.js, which can hide a backend regression — fix: The tray takes backend units as they are, and the rule has one copy.
    - [minor] The excerpt-error hidden check in the e2e runs before the save response and passes at once — fix: Wait for the save response (expect_response) or drop line 59.
- 2026-11-02T06:31:11Z backend: claimed
- 2026-11-02T06:38:17Z backend: AC 1 checked: a271014: tests/unit/test_quote_units.py (35 passed): every offered unit, as the picker submits it (raw[start:end], no hedge added), passes the save-route check on sample, case_01..09 and all 15 library packets; sample units also saved through the real entry/edit routes; hedge-qualified sentences are combined units (sample r8, case_08); label-only/date-less records give sentences [] + sentences_reason; Source-repeats-body offsets test. tests/unit full: 2239 passed, 1 skipped at a271014. e2e test_change_the_quote.py 3 passed on own server :7966 with ZLAYT_DB
- 2026-11-02T06:38:17Z backend: moved in_progress -> in_review
- 2026-11-02T06:38:25Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (a271014): r2 F1: present.quote_units merges a sentence with the hedge sentence(s) after it into ONE unit (decided by the save route's own check_excerpt, Spanish module included), so every offered unit saves alone and excerpt.js needs no change; F2: quote_body returns (offset, body, reason), the broad except and the whole-block fallback are gone, a record whose Excerpt label cannot be separated gets sentences [] + sentences_reason, offsets searched from the end of the Excerpt label (F3). api.md documents both. | Verified: tests/unit/test_quote_units.py 35 passed incl. invariant over sample, case_01..09, library; unit suite 2239 passed 1 skipped; e2e 3 passed (:7966, ZLAYT_DB); mutants: no-merge fails 4 tests, find-from-0 fails the repeat-body test. | Left: curly-quote wrapper (F4), manual.js duplicate stripping (F6) and e2e line 59 (F7) not touched this round; tray shows 'no sentences to pick from' without the reason (frontend). | Surprised: label-guard regex is redundant with find-after-label, kept as a second layer.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:42:36.947Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && grep -rn \"no sentences\\|to pick from\" app/frontend | head; echo ---; sed -n 14,30p app/frontend/manual.js; echo ---; sed -n 15,30p app/frontend/excerpt.js; echo ---; grep -n \"def _record\" -A6 app/backend/ingest.py | head -12",
 "description": "Check frontend empty-units message and picker guard"
}
````

### User / tool · 2026-11-02T06:42:37.056Z

**tool result**
````
app/frontend/manual.js:55:        sents.length ? boxes.map((b) => b.label) : el("p", { class: "rv-empty" }, "This record has no sentences to pick from.")),
---
  function quotable(rec) {
    const out = [];
    (rec.sentences || []).forEach((s) => {
      let a = s.start, b = s.end, txt = rec.text.slice(a - rec.char_start, b - rec.char_start);
      if (/^(===|Date:|Source:)/.test(txt)) return;
      const m = /^Excerpt:\s*"?/.exec(txt); if (m) { a += m[0].length; txt = txt.slice(m[0].length); }
      if (/"\s*$/.test(txt) && !txt.slice(0, -1).includes('"')) { const k = txt.length - txt.replace(/"\s*$/, "").length; b -= k; txt = txt.slice(0, txt.length - k); }
      if (txt.trim()) out.push({ text: txt, start: a, end: b });
    });
    return out;
  }

  function control(c, t, rec) {
    const d = draft[t.id] || (draft[t.id] = { open: false, picked: [], summary: "" });
    const sents = quotable(rec);
    const msg = el("p", { class: "rv-error", role: "alert", "data-testid": "manual-error" });
    const sum = el("textarea", { class: "rv-text", rows: "3", maxlength: "2000", name: "summary", "data-testid": "manual-summary", "aria-label": "Your summary, written from the quote" });
---
  };
  ZL.hasQuoteEditor = (id) => !!(pickers[id] || []).some((p) => p.panel.isConnected);
  ZL.registerRowActions((entry, row) => {
    if (entry.state === "rejected") return;
    const rec = ZL.state.get().case.records.find((r) => r.id === entry.record_ids[0]);
    if (!rec || !rec.sentences || rec.sentences.length < 2 || entry.record_ids.length !== 1) return;
    const units = rec.sentences;
    let lo = units.findIndex((u) => u.start >= entry.excerpt_start && u.start < entry.excerpt_end), hi = -1;
    units.forEach((u, i) => { if (u.end > entry.excerpt_start && u.end <= entry.excerpt_end) hi = i; });
    if (lo < 0 || hi < lo) { lo = 0; hi = units.length - 1; }
    const panel = el("form", { class: "ex-units", hidden: true, "data-testid": "excerpt-editor" });
    const msg = el("p", { class: "error", role: "alert", hidden: true, "data-testid": "excerpt-error" });
    function draw() {
      clear(panel);
      panel.append(el("p", { class: "muted small" }, "Choose which sentences of this record the letter quotes. Only whole sentences of this record; a hedge that qualifies a chosen sentence has to stay."),
        el("ul", { class: "ex-unit-list" }, units.map((u, i) => el("li", {}, el("label", {},
---
137:def _record(n: int, block: str, start: int, end: int, p: dict) -> dict:
138-    return {"n": n, "date_raw": p["date_raw"], "source": p["source"], "excerpt": p["excerpt"],
139-            "text": block, "char_start": start, "char_end": end, "unsplit": bool(p.get("unsplit"))}
140-
141-
142-class SplitFailed(Exception):
143-    """The model could not give a split (call failed, no recorded answer, unusable output). `code` is a reason code; never model text."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:42:50.930Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe_r2.py",
 "content": "\"\"\"T-108 r2 probe (scratch only, reviewer). Run as: python -I probe_r2.py <archive root>.\nFor sample, case_01..09 and the 15 library packets: every offered unit, submitted the way the picker submits it\n(raw[start:end], nothing added), is checked with the save-route call (check_excerpt) and grounding.locate.\nAlso: combined units, label-only records (units [] + sentences_reason), and the two r1 failing sentences via the real route.\"\"\"\nimport os, sys, json, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.insert(0, ROOT)\nos.chdir(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nfrom fastapi.testclient import TestClient\nfrom app.backend import grounding, language, present, spanish, store, sentences, ingest\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\n\ntmp = tempfile.mkdtemp(prefix=\"t108r2probe\")\ndb = os.path.join(tmp, \"p.sqlite\")\nc = TestClient(create_app(db, static_dir=tmp), client=(\"127.0.0.1\", 50000))\nLIB = sorted(p.stem for p in pathlib.Path(ROOT, \"evals\", \"library\").glob(\"*.txt\"))\nGOLD = [n for n in G.case_names() if n.startswith(\"case_0\") and int(n[5:7]) <= 9]\njobs = [(\"sample\", {\"sample\": True})] + [(n, {\"text\": G.raw(n)}) for n in GOLD] + [(l, {\"library\": l}) for l in LIB]\n\nWRAP = ('\"', \"“\", \"”\")\ntotals = dict(cases=0, records=0, units=0, combined=0, not_verbatim=0, alone_fail=[], locate_fail=[], wrapper=[], reason_records=0, empty_records=0)\nper_case = {}\nfor name, body in jobs:\n    r = c.post(\"/api/cases\", json=body)\n    if r.status_code != 201:\n        per_case[name] = {\"create_status\": r.status_code, \"body\": r.text[:200]}\n        totals[\"alone_fail\"].append((name, \"create\", r.status_code))\n        continue\n    tok = r.json()[\"token\"]\n    case = c.get(f\"/api/cases/{tok}\").json()\n    conn = DB.connect(db)\n    raw = DB.get_case(conn, tok)[\"raw_text\"]\n    recs = {x[\"id\"]: x for x in store.load_records(conn, tok, raw)}\n    st = dict(records=0, units=0, combined=0, alone_fail=0, wrapper=0, reason=0)\n    for rv in case[\"records\"]:\n        st[\"records\"] += 1\n        totals[\"records\"] += 1\n        rec = recs[rv[\"id\"]]\n        if rv.get(\"sentences_reason\"):\n            st[\"reason\"] += 1; totals[\"reason_records\"] += 1\n        if not rv[\"sentences\"]:\n            totals[\"empty_records\"] += 1\n        for u in rv[\"sentences\"]:\n            st[\"units\"] += 1; totals[\"units\"] += 1\n            picked = raw[u[\"start\"]:u[\"end\"]]\n            if picked != u[\"text\"]:\n                totals[\"not_verbatim\"] += 1\n            if len(sentences.stripped_spans(u[\"text\"])) > 1:\n                st[\"combined\"] += 1; totals[\"combined\"] += 1\n            if any(q in u[\"text\"] for q in WRAP) or u[\"text\"].startswith((\"Excerpt\", \"Date:\", \"Source:\", \"===\")):\n                st[\"wrapper\"] += 1; totals[\"wrapper\"].append((name, rv[\"id\"], u[\"text\"][:60]))\n            probs = spanish.module_for(language.record_lang(rec)).check_excerpt(rec[\"excerpt\"], picked)\n            if probs:\n                st[\"alone_fail\"] += 1; totals[\"alone_fail\"].append((name, rv[\"id\"], probs, picked[:70]))\n            if grounding.locate(rec[\"excerpt\"], picked) is None:\n                totals[\"locate_fail\"].append((name, rv[\"id\"], picked[:60]))\n    conn.close()\n    totals[\"cases\"] += 1\n    per_case[name] = st\n\nprint(json.dumps({\"per_case\": per_case, \"totals\": {k: (v if not isinstance(v, list) else (len(v), v[:5])) for k, v in totals.items()}}, ensure_ascii=False, indent=1))\n\n# ---- real route for the two sentences that failed alone in r1 (sample r8 unit 0, case_08 r2 unit 0)\ndef route_check(name, body, rid):\n    tok = c.post(\"/api/cases\", json=body).json()[\"token\"]\n    case = c.get(f\"/api/cases/{tok}\").json()\n    raw = DB.get_case(DB.connect(db), tok)[\"raw_text\"]\n    rv = next(x for x in case[\"records\"] if x[\"id\"] == rid)\n    u0 = rv[\"sentences\"][0]\n    picked = raw[u0[\"start\"]:u0[\"end\"]]\n    out = {\"unit_text\": picked}\n    bare = picked.split(\" \")  # placeholder, replaced below\n    first_sent = sentences.stripped_spans(picked)[0]\n    bare_txt = picked[first_sent[0]:first_sent[1]]\n    for label, txt in ((\"picked_unit\", picked), (\"bare_first_sentence\", bare_txt)):\n        r = c.post(f\"/api/cases/{tok}/records/{rid}/entry\", json={\"summary\": txt, \"excerpt\": txt})\n        out[label] = {\"status\": r.status_code, \"text\": txt, \"body\": r.text[:160]}\n        # fresh case per submission so the duplicate-entry check cannot mask the quote check\n        tok = c.post(\"/api/cases\", json=body).json()[\"token\"]\n    return out\n\nprint(json.dumps({\"r8_sample\": route_check(\"sample\", {\"sample\": True}, \"r8\"),\n                  \"case_08_r2\": route_check(\"case_08\", {\"text\": G.raw(\"case_08_diagnosis_temptation\")}, \"r2\")}, ensure_ascii=False, indent=1))\n\n# ---- label-only and date-less records through the real ingest + record_view (no DB, no API; demo mode refuses custom text)\nLAB = {\n    \"label_only\": 'Excerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n    \"source_excerpt_only\": 'Source: Synthetic Clinic\\nExcerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n    \"date_excerpt\": 'Date: 2026-01-05\\nExcerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n}\nfor k, txt in LAB.items():\n    for rec in ingest.split_records(txt):\n        block = rec[\"text\"]\n        r = {\"id\": \"rx\", \"seq\": 1, \"source_label\": \"\", \"date_raw\": \"\", \"date_iso\": None, \"date_status\": \"missing\", \"date_candidates\": [],\n             \"duplicate_of\": None, \"injection_tag\": 0, \"encounter\": 0, \"char_start\": 0, \"char_end\": len(txt), \"language\": None}\n        v = present.record_view(r, txt)\n        print(json.dumps({\"shape\": k, \"sentences\": [s[\"text\"] for s in v[\"sentences\"]], \"sentences_reason\": v.get(\"sentences_reason\")}, ensure_ascii=False))\n"
}
````

### User / tool · 2026-11-02T06:42:50.989Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe_r2.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:01.599Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/probe_r2.py",
 "content": "\"\"\"T-108 r2 probe (reviewer scratch evidence). Run as: python -I probe_r2.py <archive root of a271014>.\nFor sample, case_01..09 and the 15 library packets: every offered unit, submitted the way the picker submits it\n(raw[start:end], nothing added), is checked with the save-route call (check_excerpt) and grounding.locate.\nAlso: combined units, the two r1 failing sentences through the real entry route, and label-only / date-less shapes through record_view.\"\"\"\nimport os, sys, json, tempfile, pathlib\nROOT = sys.argv[1]\nsys.path.insert(0, ROOT)\nos.chdir(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ENABLE_LIVE\", None)\nos.environ[\"ZLAYT_MODE\"] = \"local\"\nfrom fastapi.testclient import TestClient\nfrom app.backend import grounding, language, present, spanish, store, sentences, ingest\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\n\ntmp = tempfile.mkdtemp(prefix=\"t108r2probe\")\ndb = os.path.join(tmp, \"p.sqlite\")\nc = TestClient(create_app(db, static_dir=tmp), client=(\"127.0.0.1\", 50000))\nLIB = sorted(p.stem for p in pathlib.Path(ROOT, \"evals\", \"library\").glob(\"*.txt\"))\nGOLD = [n for n in G.case_names() if n.startswith(\"case_0\") and int(n[5:7]) <= 9]\njobs = [(\"sample\", {\"sample\": True})] + [(n, {\"text\": G.raw(n)}) for n in GOLD] + [(l, {\"library\": l}) for l in LIB]\n\nWRAP = ('\"', \"“\", \"”\")\ntotals = dict(cases=0, records=0, units=0, combined=0, not_verbatim=[], alone_fail=[], locate_fail=[], wrapper=[], reason_records=0, empty_records=0)\nper_case = {}\nfor name, body in jobs:\n    r = c.post(\"/api/cases\", json=body)\n    if r.status_code != 201:\n        per_case[name] = {\"create_status\": r.status_code, \"body\": r.text[:200]}\n        totals[\"alone_fail\"].append((name, \"create\", r.status_code))\n        continue\n    tok = r.json()[\"token\"]\n    case = c.get(f\"/api/cases/{tok}\").json()\n    conn = DB.connect(db)\n    raw = DB.get_case(conn, tok)[\"raw_text\"]\n    recs = {x[\"id\"]: x for x in store.load_records(conn, tok, raw)}\n    st = dict(records=0, units=0, combined=0, alone_fail=0, wrapper=0, reason=0)\n    for rv in case[\"records\"]:\n        st[\"records\"] += 1\n        totals[\"records\"] += 1\n        rec = recs[rv[\"id\"]]\n        if rv.get(\"sentences_reason\"):\n            st[\"reason\"] += 1\n            totals[\"reason_records\"] += 1\n        if not rv[\"sentences\"]:\n            totals[\"empty_records\"] += 1\n        for u in rv[\"sentences\"]:\n            st[\"units\"] += 1\n            totals[\"units\"] += 1\n            picked = raw[u[\"start\"]:u[\"end\"]]\n            if picked != u[\"text\"]:\n                totals[\"not_verbatim\"].append((name, rv[\"id\"]))\n            if len(sentences.stripped_spans(u[\"text\"])) > 1:\n                st[\"combined\"] += 1\n                totals[\"combined\"] += 1\n            if any(q in u[\"text\"] for q in WRAP) or u[\"text\"].startswith((\"Excerpt\", \"Date:\", \"Source:\", \"===\")):\n                st[\"wrapper\"] += 1\n                totals[\"wrapper\"].append((name, rv[\"id\"], u[\"text\"][:60]))\n            probs = spanish.module_for(language.record_lang(rec)).check_excerpt(rec[\"excerpt\"], picked)\n            if probs:\n                st[\"alone_fail\"] += 1\n                totals[\"alone_fail\"].append((name, rv[\"id\"], probs, picked[:70]))\n            if grounding.locate(rec[\"excerpt\"], picked) is None:\n                totals[\"locate_fail\"].append((name, rv[\"id\"], picked[:60]))\n    conn.close()\n    totals[\"cases\"] += 1\n    per_case[name] = st\n\ndef summarise(v):\n    return v if not isinstance(v, list) else {\"count\": len(v), \"first\": v[:5]}\n\nprint(json.dumps({\"per_case\": per_case, \"totals\": {k: summarise(v) for k, v in totals.items()}}, ensure_ascii=False, indent=1))\n\n\n# ---- the real entry route for the two sentences that failed alone in r1 (sample r8 unit 0, case_08 r2 unit 0)\ndef route_check(body, rid):\n    out = {}\n    tok0 = c.post(\"/api/cases\", json=body).json()[\"token\"]\n    case0 = c.get(f\"/api/cases/{tok0}\").json()\n    raw0 = DB.get_case(DB.connect(db), tok0)[\"raw_text\"]\n    rv0 = next(x for x in case0[\"records\"] if x[\"id\"] == rid)\n    u0 = rv0[\"sentences\"][0]\n    picked = raw0[u0[\"start\"]:u0[\"end\"]]\n    first = sentences.stripped_spans(picked)[0]\n    bare = picked[first[0]:first[1]]\n    out[\"unit_text\"] = picked\n    out[\"bare_first_sentence\"] = bare\n    for label, txt in ((\"picked_unit\", picked), (\"bare_first_sentence\", bare)):\n        tok = c.post(\"/api/cases\", json=body).json()[\"token\"]          # fresh case: the duplicate-entry check cannot mask the quote check\n        r = c.post(f\"/api/cases/{tok}/records/{rid}/entry\", json={\"summary\": txt, \"excerpt\": txt})\n        out[label + \"_status\"] = r.status_code\n        out[label + \"_body\"] = r.text[:160]\n    return out\n\n\nprint(json.dumps({\"r8_sample\": route_check({\"sample\": True}, \"r8\"),\n                  \"case_08_r2\": route_check({\"text\": G.raw(\"case_08_diagnosis_temptation\")}, \"r2\")}, ensure_ascii=False, indent=1))\n\n# ---- label-only and date-less shapes through the real ingest, then record_view (no API; demo mode refuses pasted text)\nLAB = {\n    \"label_only\": 'Excerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n    \"source_excerpt_only\": 'Source: Synthetic Clinic\\nExcerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n    \"date_excerpt\": 'Date: 2026-01-05\\nExcerpt: \"Pain persists after two weeks. Taking meds daily.\"',\n}\nfor k, txt in LAB.items():\n    for rec in ingest.split_records(txt):\n        r = {\"id\": \"rx\", \"seq\": 1, \"source_label\": \"\", \"date_raw\": \"\", \"date_iso\": None, \"date_status\": \"missing\", \"date_candidates\": [],\n             \"duplicate_of\": None, \"injection_tag\": 0, \"encounter\": 0, \"char_start\": 0, \"char_end\": len(txt)}\n        v = present.record_view(r, txt)\n        print(json.dumps({\"shape\": k, \"sentences\": [s[\"text\"] for s in v[\"sentences\"]], \"sentences_reason\": v.get(\"sentences_reason\")}, ensure_ascii=False))\n"
}
````

### User / tool · 2026-11-02T06:43:01.694Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/probe_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:04.490Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/probe_r2.py \"$S/T108_r2_verify\" > \"$S/probe-r2-output.txt\" 2>&1; echo EXIT=$?; cat \"$S/probe-r2-output.txt\" | head -300",
 "description": "Run the r2 invariant probe on the a271014 archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:43:05.710Z

**tool result**
````
EXIT=0
llm call failed call_id=ce7bb936a3c0c step=j1 attempt=1 prompt_hash=0902a5475ab9fce32b9f924bb78c34138cd6263bd27c6255b888be49eb2793b8
llm call failed call_id=c94b8050c98a9 step=j1 attempt=1 prompt_hash=4d1faa1fb04506288cc1b9852e78fe1757af0ddeddbf4819fe6d116802d05f77
{
 "per_case": {
  "sample": {
   "records": 9,
   "units": 28,
   "combined": 1,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_01_date_formats": {
   "records": 8,
   "units": 16,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_02_gap_boundaries": {
   "records": 8,
   "units": 17,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_03_rate_and_ocr": {
   "records": 5,
   "units": 12,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_04_duplicates_no_amounts": {
   "records": 6,
   "units": 18,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_05_provider_conflict": {
   "records": 5,
   "units": 13,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_06_subtle_pre_existing": {
   "records": 5,
   "units": 13,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_07_prompt_injection": {
   "records": 4,
   "units": 10,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_08_diagnosis_temptation": {
   "records": 4,
   "units": 10,
   "combined": 1,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_09_nonvisit_hides_gap": {
   "records": 5,
   "units": 10,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib01_er_only_then_gap": {
   "records": 6,
   "units": 18,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib02_slip_fall_prior_knee": {
   "records": 7,
   "units": 22,
   "combined": 2,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib03_truck_rear_end_chiro": {
   "records": 7,
   "units": 21,
   "combined": 1,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib04_dog_bite_scar_revision": {
   "records": 6,
   "units": 20,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib05_pedestrian_orif_hardware": {
   "records": 8,
   "units": 24,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib06_lop_billed_vs_adjusted": {
   "records": 7,
   "units": 23,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib07_parking_lot_fall_outside_records": {
   "records": 7,
   "units": 21,
   "combined": 1,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib08_second_crash_mri_after": {
   "records": 12,
   "units": 39,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib09_spanish_interpreter_espalda": {
   "records": 7,
   "units": 31,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib10_eob_ub04_cms1500": {
   "records": 9,
   "units": 37,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib11_priors_and_ledger": {
   "records": 9,
   "units": 40,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib12_records_review_credibility": {
   "records": 10,
   "units": 39,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib13_cloned_notes_cross_provider": {
   "records": 9,
   "units": 28,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib14_handwritten_chiro_scans": {
   "records": 8,
   "units": 35,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  },
  "case_lib15_conclusory_letter_mist": {
   "records": 9,
   "units": 46,
   "combined": 0,
   "alone_fail": 0,
   "wrapper": 0,
   "reason": 0
  }
 },
 "totals": {
  "cases": 25,
  "records": 180,
  "units": 591,
  "combined": 6,
  "not_verbatim": {
   "count": 0,
   "first": []
  },
  "alone_fail": {
   "count": 0,
   "first": []
  },
  "locate_fail": {
   "count": 0,
   "first": []
  },
  "wrapper": {
   "count": 0,
   "first": []
  },
  "reason_records": 0,
  "empty_records": 0
 }
}
{
 "r8_sample": {
  "unit_text": "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.",
  "bare_first_sentence": "C5-C6 disc protrusion with mild right foraminal narrowing.",
  "picked_unit_status": 201,
  "picked_unit_body": "{\"item\":{\"id\":\"e8_m\",\"state\":\"needs_review\",\"reasons\":[\"JUDGE_UNAVAILABLE\"],\"why\":\"The second AI check did not run or did not finish, so this item has not been ",
  "bare_first_sentence_status": 422,
  "bare_first_sentence_body": "{\"error\":{\"code\":\"invalid_edit\",\"message\":\"The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.\",\"detail\":{\""
 },
 "case_08_r2": {
  "unit_text": "Signal change in the supraspinatus tendon. Clinical correlation recommended.",
  "bare_first_sentence": "Signal change in the supraspinatus tendon.",
  "picked_unit_status": 201,
  "picked_unit_body": "{\"item\":{\"id\":\"e2_m\",\"state\":\"needs_review\",\"reasons\":[\"JUDGE_UNAVAILABLE\"],\"why\":\"The second AI check did not run or did not finish, so this item has not been ",
  "bare_first_sentence_status": 422,
  "bare_first_sentence_body": "{\"error\":{\"code\":\"invalid_edit\",\"message\":\"The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.\",\"detail\":{\""
 }
}
{"shape": "label_only", "sentences": [], "sentences_reason": "No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, so a quote cut from it could not be checked against the record. Read the record text instead."}
{"shape": "source_excerpt_only", "sentences": [], "sentences_reason": "No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, so a quote cut from it could not be checked against the record. Read the record text instead."}
{"shape": "date_excerpt", "sentences": ["Pain persists after two weeks.", "Taking meds daily."], "sentences_reason": null}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:16.605Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cp -R \"$S/T108_r2_verify\" \"$S/M1_nocombine\" && cp -R \"$S/T108_r2_verify\" \"$S/M2_find0\" && cd \"$S/M1_nocombine\" && sed -i '' 's/while j + 1 < len(spans) and \"EXCERPT_OMITS_QUALIFIER\"/while False and \"EXCERPT_OMITS_QUALIFIER\"/' app/backend/present.py && cd \"$S/M2_find0\" && sed -i '' 's/i = block.find(body, m.end() if m else 0)/i = block.find(body)/' app/backend/present.py && cd \"$S\" && diff \"$S/T108_r2_verify/app/backend/present.py\" \"$S/M1_nocombine/app/backend/present.py\"; diff \"$S/T108_r2_verify/app/backend/present.py\" \"$S/M2_find0/app/backend/present.py\"; echo DIFFS_DONE",
 "description": "Create two scratch mutant copies of the archive"
}
````

### User / tool · 2026-11-02T06:43:17.908Z

**tool result**
````
194c194
<         while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
---
>         while False and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
179c179
<     i = block.find(body, m.end() if m else 0)
---
>     i = block.find(body)
DIFFS_DONE
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:21.507Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/M1_nocombine\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_quote_units.py > \"$S/mutant-M1-nocombine.txt\" 2>&1; echo M1_EXIT=$?; grep -E \"passed|failed\" \"$S/mutant-M1-nocombine.txt\" | tail -3; grep -E \"^FAILED\" \"$S/mutant-M1-nocombine.txt\" | head -40; cd \"$S/M2_find0\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_quote_units.py > \"$S/mutant-M2-find0.txt\" 2>&1; echo M2_EXIT=$?; grep -E \"passed|failed\" \"$S/mutant-M2-find0.txt\" | tail -3; grep -E \"^FAILED\" \"$S/mutant-M2-find0.txt\" | head",
 "description": "Run quote unit tests against both scratch mutants",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:43:25.371Z

**tool result**
````
M1_EXIT=1
8 failed, 27 passed in 1.48s
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_golden[case_08_diagnosis_temptation]
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_golden[sample]
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_sample
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_library[case_lib02_slip_fall_prior_knee]
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_library[case_lib03_truck_rear_end_chiro]
FAILED tests/unit/test_quote_units.py::test_every_offered_unit_saves_alone_library[case_lib07_parking_lot_fall_outside_records]
FAILED tests/unit/test_quote_units.py::test_hedge_qualified_sentence_is_one_combined_unit
FAILED tests/unit/test_quote_units.py::test_golden_hedge_qualified_sentences_are_combined
M2_EXIT=1
1 failed, 34 passed in 1.63s
FAILED tests/unit/test_quote_units.py::test_units_sit_at_true_offsets_when_source_repeats_the_body
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:36.428Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys\nsys.path.insert(0, '$S/T108_r2_verify')\nfrom app.backend import ingest, present\nfor t in ['Excerpt: \\\"Pain persists after two weeks. Taking meds daily.\\\"', 'Source: Synthetic Clinic\\nExcerpt: \\\"Pain persists after two weeks. Taking meds daily.\\\"']:\n    try:\n        r = ingest.split_records(t)\n        print('split ok; excerpt=', repr(r[0]['excerpt']))\n    except Exception as e:\n        print('split raised', type(e).__name__, getattr(e, 'code', ''))\n    print('quote_body ->', present.quote_body(t)[1:2], present.quote_body(t)[2] is not None)\n\"",
 "description": "Check split_records output for label-only shapes"
}
````

### User / tool · 2026-11-02T06:43:36.653Z

**tool result**
````
split ok; excerpt= 'Excerpt: "Pain persists after two weeks. Taking meds daily."'
quote_body -> ('',) True
split ok; excerpt= 'Source: Synthetic Clinic\nExcerpt: "Pain persists after two weeks. Taking meds daily."'
quote_body -> ('',) True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:43:45.338Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git clone --quiet /Users/arsis/zlayt-pm-project \"$S/T108_r2_clone\" && cd \"$S/T108_r2_clone\" && git checkout --quiet --detach a271014 && git rev-parse --short HEAD && git status --short | head -3; cd \"$S/T108_r2_clone\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit > \"$S/unit-run-r2-clone-with-git.txt\" 2>&1; echo EXIT=$?; tail -2 \"$S/unit-run-r2-clone-with-git.txt\"; grep -c . \"$S/unit-run-r2-clone-with-git.txt\" >/dev/null; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_quote_units.py 2>&1 | tail -1",
 "description": "Clone repo at a271014 and run unit suite with git metadata",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:46:35.354Z

**tool result**
````
a271014
EXIT=0
........                                                                 [100%]
2239 passed, 1 skipped in 163.32s (0:02:43)
35 passed in 1.59s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:46:41.921Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && grep -n 'strip\\|\\\"' app/backend/ingest.py | sed -n 1,3p >/dev/null; sed -n 60,66p app/backend/ingest.py; echo ---; grep -n \"excerpt-error\" tests/e2e/test_change_the_quote.py; echo ---; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys\nsys.path.insert(0, '$S/T108_r2_verify')\nfrom app.backend import ingest, present\nt = 'Date: 2026-01-05\\nSource: Synthetic Clinic\\nExcerpt: “Pain persists after two weeks. Taking meds daily.”'\nfor rec in ingest.split_records(t):\n    why, body = present.quote_body(rec['text'])[2], present.quote_body(rec['text'])[1]\n    print('F4 curly: body=', repr(body), 'why=', why)\n    print('units=', [body[a:b] for a,b in present.sentences.stripped_spans(body)] if body else [])\n\" ",
 "description": "Confirm F4, F7 still open at a271014"
}
````

### User / tool · 2026-11-02T06:46:42.159Z

**tool result**
````
/bin/bash: child setpgid (56987 to 56987): Operation not permitted
def _excerpt_extent(rest: str):
    """(excerpt, consumed_chars) for the text after 'Excerpt:'. A quoted excerpt ends at the first line that ends with a quote;
    anything after it is NOT part of the excerpt (it surfaces as unsplit text). Unquoted or unterminated: the rest of the block."""
    if rest.startswith('"'):
        i = 0
        while True:
            j = rest.find("\n", i)
---
4:No new test ids: btn-accept, accept-refused, btn-accept-refused-quote, excerpt-editor, excerpt-unit, btn-save-excerpt, excerpt-error (all declared in conftest)."""
59:        expect(ed.get_by_test_id("excerpt-error")).to_be_hidden()
---
F4 curly: body= '“Pain persists after two weeks. Taking meds daily.”' why= None
units= ['“Pain persists after two weeks.', 'Taking meds daily.”']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:46:59.267Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport os, sys, tempfile\nsys.path.insert(0, '$S/T108_r2_verify'); os.chdir('$S/T108_r2_verify')\nos.environ['LLM_BACKEND']='fixture'; os.environ.pop('ANTHROPIC_API_KEY', None); os.environ.pop('ENABLE_LIVE', None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\ntmp = tempfile.mkdtemp(); c = TestClient(create_app(os.path.join(tmp,'p.sqlite'), static_dir=tmp), client=('127.0.0.1', 50000))\ntok = c.post('/api/cases', json={'sample': True}).json()['token']\ncase = c.get('/api/cases/%s' % tok).json()\nhas = {}\nfor e in case['entries'] + case['undated_entries']:\n    if len(e['record_ids']) == 1: has[e['record_ids'][0]] = e['id']\ntray = [(rv['id'], len(rv['sentences'])) for rv in case['records'] if rv['id'] not in has]\nedit = [(rv['id'], len(rv['sentences'])) for rv in case['records'] if rv['id'] in has]\nprint('records with entry (edit route):', edit)\nprint('records without entry (tray, manual route):', tray)\nprint('tray units not route-checked (after first):', sum(max(n-1,0) for _, n in tray))\n\" 2>&1 | grep -v \"llm call failed\"",
 "description": "Count sample units that reach only the duplicate check"
}
````

### User / tool · 2026-11-02T06:46:59.833Z

**tool result**
````
records with entry (edit route): []
records without entry (tray, manual route): [('r1', 4), ('r2', 6), ('r3', 3), ('r4', 3), ('r5', 2), ('r6', 2), ('r7', 4), ('r8', 2), ('r9', 2)]
tray units not route-checked (after first): 19
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:47:09.001Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport os, sys, tempfile, collections\nsys.path.insert(0, '$S/T108_r2_verify'); os.chdir('$S/T108_r2_verify')\nos.environ['LLM_BACKEND']='fixture'; os.environ.pop('ANTHROPIC_API_KEY', None); os.environ.pop('ENABLE_LIVE', None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.db import db as DB\ntmp = tempfile.mkdtemp(); dbp = os.path.join(tmp,'p.sqlite')\nc = TestClient(create_app(dbp, static_dir=tmp), client=('127.0.0.1', 50000))\ntok0 = c.post('/api/cases', json={'sample': True}).json()['token']\ncase = c.get('/api/cases/%s' % tok0).json()\nraw = DB.get_case(DB.connect(dbp), tok0)['raw_text']\njobs = [(rv['id'], raw[u['start']:u['end']]) for rv in case['records'] for u in rv['sentences']]\nres = collections.Counter(); bad = []\nfor rid, q in jobs:\n    tok = c.post('/api/cases', json={'sample': True}).json()['token']\n    r = c.post('/api/cases/%s/records/%s/entry' % (tok, rid), json={'summary': q, 'excerpt': q})\n    res[r.status_code] += 1\n    if r.status_code != 201: bad.append((rid, r.status_code, r.text[:120]))\nprint('fresh-case manual entry per unit, sample: n=%d' % len(jobs), dict(res))\nprint('non-201:', bad[:5])\n\" 2>&1 | grep -v \"llm call failed\"",
 "description": "Route-check every sample unit on a fresh case each",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:47:09.959Z

**tool result**
````
fresh-case manual entry per unit, sample: n=28 {201: 28}
non-201: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:47:13.519Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep T-108; echo ---; cat .claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md; echo ---; cat .claude/agent-memory/staff-engineer-reviewer/feedback_exact_count_vs_presence.md | head -30; echo ---; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"print(1)\" >/dev/null; ls /Users/arsis/zlayt-pm-project/tools/board.py && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/tools/board.py show T-108 2>&1 | head -8",
 "description": "Check review file state and memory guidance before writing"
}
````

### User / tool · 2026-11-02T06:47:13.695Z

**tool result**
````
T-108-staff-engineer.md
---
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
---
---
name: feedback_exact_count_vs_presence
description: A presence oracle (each token appears somewhere) cannot see a dropped or doubled occurrence; run the test module's own random generator with exact per-record counts before passing a "nothing silently missing" claim
metadata:
  type: feedback
---

When a card claims "every money token is placed", check multiplicity, not presence. A presence oracle passes when a second printed copy of the same figure is dropped, because the first copy still satisfies it. T-103 r3: the test oracle (`unaccounted`) was presence-only, the exact count ran only over a fixed PROBES dict, and 31 of 600 generated draws differed per record (10 dropped occurrences, 2 doubled, 18 bare counts listed as figures).

**Why:** the handoff said "per-record count in==out for every probe" and the suite was green, but a fixed probe set cannot find an equal-text collision in a shape nobody wrote down. The fix was claimed for one collision (210.00) and a different collision class (130.00 twice in one excerpt) was still lost.

**How to apply:**
1. Import the test module's generator (`tests/unit/test_billing.py` `_BASES`, `_TOKENS`, `_insert`) and run the same draws with exact per-record Counters, outside pytest, with `-I` against a git-archive copy. Count mismatches by class (drop, double, bare over-list).
2. Any suppression keyed by text (count of (record, excerpt, text)) is suspect: two equal figures in one excerpt cannot be told apart.
3. Mutate a suppression to "always suppress" and a drop-only mutant to confirm the exact count goes red, not just the presence oracle.

Related: [[t103-listing-review-patterns]], [[project_t083_billing_review_patterns]].
---
/Users/arsis/zlayt-pm-project/tools/board.py
---
id: "T-108"
title: "Quote picker cannot save a valid quote on the sample: sentence units include the 'Excerpt: \"' wrapper"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:47:56.937Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/T108_r2_verify\" && grep -n \"def quote_body\\|def quote_units\\|NO_UNITS_LAYOUT = \\|while j + 1\\|sentences_reason\\|except ingest.IngestError\\|return 0, \\\"\\\", NO_UNITS\\|return i, body\" app/backend/present.py; echo ---; grep -n \"already has an entry\\|check_excerpt\" app/backend/review.py | sed -n 1,6p; echo ---; grep -n \"def test_\" tests/unit/test_quote_units.py; echo ---; grep -n \"already has an entry\" tests/unit/test_quote_units.py; echo ---; grep -n \"except Exception\" app/backend/store.py; echo ---; grep -n \"sentences_reason\" -r app/frontend | wc -l; grep -n \"no sentences to pick\" app/frontend/manual.js; grep -n \"excerpt.length\\|sentences.length < 2\" app/frontend/excerpt.js | head -2",
 "description": "Collect exact line numbers for review citations"
}
````

### User / tool · 2026-11-02T06:47:57.072Z

**tool result**
````
155:            v["sentences_reason"] = why_none           # no sentence is offered; the reason is plain words for the review screen
159:NO_UNITS_LAYOUT = ("No sentences are offered for this record: its Date, Source and Excerpt lines could not be told apart from its text, "
164:def quote_body(block):
174:    except ingest.IngestError:
175:        return 0, "", NO_UNITS_LAYOUT
177:        return 0, "", NO_UNITS_LAYOUT
181:        return 0, "", NO_UNITS_LAYOUT
182:    return i, body, None
185:def quote_units(body, rec):
194:        while j + 1 < len(spans) and "EXCERPT_OMITS_QUALIFIER" in check(body, body[spans[i][0]:spans[j][1]]):
---
95:        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence
300:        problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], new_exc)
446:        raise _bad("This record already has an entry; edit that entry instead.")
451:    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
---
59:def test_every_offered_unit_saves_alone_golden(env, monkeypatch, name):
65:def test_every_offered_unit_saves_alone_sample(env):
87:def test_every_offered_unit_saves_alone_library(tmp_path, monkeypatch, lib):
99:def test_hedge_qualified_sentence_is_one_combined_unit(env):
115:def test_golden_hedge_qualified_sentences_are_combined(env):
125:def test_sample_units_have_no_wrapper(env):
144:def test_quote_body_cases():
156:def test_label_only_or_header_missing_records_offer_no_units(txt):
176:def test_record_view_reports_reason_for_label_only_record():
185:def test_units_sit_at_true_offsets_when_source_repeats_the_body():
---
81:            else:                              # record without an entry (tray): manual entry; the first unit saves, later ones meet "already has an entry"
83:                assert r.status_code == 201 or "already has an entry" in r.text, (rv["id"], q, r.text)
---
24:        except Exception:
---
       0
55:        sents.length ? boxes.map((b) => b.label) : el("p", { class: "rv-empty" }, "This record has no sentences to pick from.")),
20:    if (!rec || !rec.sentences || rec.sentences.length < 2 || entry.record_ids.length !== 1) return;
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:48:01.234Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; D=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2; mkdir -p \"$D\" && cp \"$S/probe-r2-output.txt\" \"$D/probe-r2-output.txt\" && cp \"$S/unit-run-r2.txt\" \"$D/unit-run-archive-no-git.txt\" && cp \"$S/unit-run-r2-clone-with-git.txt\" \"$D/unit-run-clone-with-git.txt\" && cp \"$S/mutant-M1-nocombine.txt\" \"$D/mutant-M1-nocombine.txt\" && cp \"$S/mutant-M2-find0.txt\" \"$D/mutant-M2-find0.txt\" && ls -la \"$D\" && tail -1 \"$D/unit-run-clone-with-git.txt\" && tail -1 \"$D/unit-run-archive-no-git.txt\" && tail -1 \"$D/mutant-M1-nocombine.txt\" && tail -1 \"$D/mutant-M2-find0.txt\"",
 "description": "Copy round-2 evidence into review-evidence folder"
}
````

### User / tool · 2026-11-02T06:48:01.388Z

**tool result**
````
total 80
drwxr-xr-x@  7 arsis  staff    224 Nov  2 00:48 .
drwxr-xr-x@ 18 arsis  staff    576 Nov  2 00:48 ..
-rw-r--r--@  1 arsis  staff  19922 Nov  2 00:48 mutant-M1-nocombine.txt
-rw-r--r--@  1 arsis  staff   1082 Nov  2 00:48 mutant-M2-find0.txt
-rw-r--r--@  1 arsis  staff   6326 Nov  2 00:48 probe-r2-output.txt
-rw-r--r--@  1 arsis  staff   2604 Nov  2 00:48 unit-run-archive-no-git.txt
-rw-r--r--@  1 arsis  staff   2604 Nov  2 00:48 unit-run-clone-with-git.txt
2239 passed, 1 skipped in 163.32s (0:02:43)
2236 passed, 4 skipped in 161.76s (0:02:41)
8 failed, 27 passed in 1.48s
1 failed, 34 passed in 1.63s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:48:34.602Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/route_fresh_sample.py",
 "content": "\"\"\"T-108 r2 (reviewer scratch evidence). Run as: python -I route_fresh_sample.py <archive root of a271014>.\nEvery sample unit, as the picker submits it (raw[start:end]), goes to the real manual-entry route on a FRESH case, so the\n'already has an entry' duplicate branch (review.py:446) cannot mask the quote check (review.py:451). Expect 201 for all.\"\"\"\nimport os, sys, tempfile, collections\nROOT = sys.argv[1]\nsys.path.insert(0, ROOT)\nos.chdir(ROOT)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None)\nos.environ.pop(\"ENABLE_LIVE\", None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.db import db as DB\n\ntmp = tempfile.mkdtemp(prefix=\"t108r2route\")\ndbp = os.path.join(tmp, \"p.sqlite\")\nc = TestClient(create_app(dbp, static_dir=tmp), client=(\"127.0.0.1\", 50000))\ntok0 = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\ncase = c.get(\"/api/cases/%s\" % tok0).json()\nraw = DB.get_case(DB.connect(dbp), tok0)[\"raw_text\"]\njobs = [(rv[\"id\"], raw[u[\"start\"]:u[\"end\"]]) for rv in case[\"records\"] for u in rv[\"sentences\"]]\nres = collections.Counter()\nbad = []\nfor rid, q in jobs:\n    tok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n    r = c.post(\"/api/cases/%s/records/%s/entry\" % (tok, rid), json={\"summary\": q, \"excerpt\": q})\n    res[r.status_code] += 1\n    if r.status_code != 201:\n        bad.append((rid, r.status_code, r.text[:160]))\nprint(\"sample units submitted to manual entry on fresh cases: n=%d\" % len(jobs))\nprint(\"status counts:\", dict(res))\nprint(\"non-201:\", bad)\n"
}
````

### User / tool · 2026-11-02T06:48:34.716Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/route_fresh_sample.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:48:38.905Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/route_fresh_sample.py \"$S/T108_r2_verify\" > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/route-fresh-sample-output.txt 2>/dev/null; echo EXIT=$?; cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/route-fresh-sample-output.txt; cd \"$S/T108_r2_verify\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys\nsys.path.insert(0, '$S/T108_r2_verify')\nfrom app.backend import present\nt = 'Date: 2026-01-05\\nSource: Synthetic Clinic\\nExcerpt: “Pain persists after two weeks. Taking meds daily.”'\nb = present.quote_body(t)\nprint('shape D body:', repr(b[1]))\nfrom app.backend import sentences\nprint('shape D units:', [b[1][x:y] for x, y in sentences.stripped_spans(b[1])])\n\" 2>/dev/null | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/curly-shape-output.txt",
 "description": "Run fresh-case route check and save output; reproduce curly-quote gap",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:48:39.963Z

**tool result**
````
EXIT=0
sample units submitted to manual entry on fresh cases: n=28
status counts: {201: 28}
non-201: []
shape D body: '“Pain persists after two weeks. Taking meds daily.”'
shape D units: ['“Pain persists after two weeks.', 'Taking meds daily.”']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:07.736Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer-r2.md",
 "content": "# T-108 review r2 (staff-engineer-reviewer): every quote-picker unit saves alone\n\nCommit a271014 (`fix(backend): every quote-picker unit saves alone ... (T-108 r2)`), which is HEAD. I reviewed a `git archive a271014` copy and a `git clone` checked out at a271014, both in the scratchpad. The live tree has uncommitted edits and no result here depends on it. Model I ran as: claude-haiku-5-5.\n\n**Verdict: pass.** 0 blockers, 0 majors. Round-1 F1 and F2 (both major) are resolved, and F3, F5 and F8 are resolved. Three new minors (N1 to N3) and three r1 minors still open as the brief allows (F4, F6, F7).\n\n## Brief checks\n\n1. **Hedge-qualified sentences are offered as combined units that save alone: yes.** Sample r8 unit 0 is two sentences (\"C5-C6 disc protrusion ... narrowing. Findings may represent degenerative change; correlate clinically.\"). The text the picker submits (raw[start:end]) on a fresh case returns 201 at POST /api/cases/{tok}/records/r8/entry. The bare first sentence returns 422 invalid_edit. case_08 r2 gives the same result (combined unit 201, bare sentence 422). Six combined units in total across the 25 cases (sample 1, case_08 1, case_lib02 2, case_lib03 1, case_lib07 1). The save rule is unchanged: the bare sentence is still refused.\n2. **Label-only record: no units and a plain sentences_reason: yes.** `Excerpt: \"...\"` alone and `Source:` plus `Excerpt:` (no Date) both give `sentences: []` and `sentences_reason` = NO_UNITS_LAYOUT (present.py:159-160, :174-181). `Date:` plus `Excerpt:` still gives two units. Output in artifacts/review-evidence/T-108/r2/probe-r2-output.txt (last three lines).\n3. **Invariant over sample, case_01 to case_09 and all 15 library packets: passes.** 25 cases, 180 records, 591 units. Zero not verbatim, zero failing `check_excerpt` on the unit alone, zero failing `grounding.locate`, zero units with quote marks or a Label/Date/Source/=== prefix. Also `tests/unit/test_quote_units.py`: 35 passed.\n4. **Removing the combining logic fails a test: yes.** Scratch copy, not committed: `sed -i '' 's/while j + 1 < len(spans) and \"EXCERPT_OMITS_QUALIFIER\"/while False and \"EXCERPT_OMITS_QUALIFIER\"/' app/backend/present.py`, then `.venv/bin/python -m pytest -q tests/unit/test_quote_units.py` gives `8 failed, 27 passed`. The failures are the golden case_08, golden sample, sample-route, library lib02, lib03, lib07, `test_hedge_qualified_sentence_is_one_combined_unit` and `test_golden_hedge_qualified_sentences_are_combined`. Output: artifacts/review-evidence/T-108/r2/mutant-M1-nocombine.txt. The handoff says this mutant \"fails 4 tests\"; the same one-line change gives 8 here (see N1).\n\n**Unit suite, `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit`:**\n- on the archive copy (no .git): `2236 passed, 4 skipped in 161.76s`. Three of the four skips need a .git directory.\n- on the clone at a271014 (with .git): `2239 passed, 1 skipped in 163.32s`. This matches the card's AC, so the r1 F5 count now reproduces.\n- Output: artifacts/review-evidence/T-108/r2/unit-run-archive-no-git.txt and unit-run-clone-with-git.txt.\n\n## Round-1 findings\n\n- **F1 (major): resolved.** The picker now receives units that save alone, so the test helper that added the hedge (`_pick`) is gone. excerpt.js was not changed in this commit and does not need to be.\n- **F2 (major): resolved in quote_body.** The broad except and the whole-block return are removed from present.py (`quote_body`, :164-182). A record whose label cannot be separated gets no units and a reason. Two remainders are carried as N2 and N3.\n- **F3 (minor): resolved.** The offset fix (search for the body from the end of the Excerpt label, present.py:179) is now covered. Mutant M2 (`i = block.find(body)` with no start offset) gives `1 failed, 34 passed` in tests/unit/test_quote_units.py, and the failure is `test_units_sit_at_true_offsets_when_source_repeats_the_body`. Output: artifacts/review-evidence/T-108/r2/mutant-M2-find0.txt.\n- **F5 (minor): resolved.** The 2239 passed count reproduces at a271014 with .git.\n- **F8 (nit): resolved.** `_pick` no longer exists.\n- **F4, F6, F7 (minor): still open, as the brief says.** See below.\n\n## New findings\n\n- **N1 (minor).** The sample route test does not check the quote for most units. For each record it posts the first unit, which creates the entry. Later units get \"already has an entry\" back, and `tests/unit/test_quote_units.py:81-83` accepts that. That check is at review.py:446 and runs before the quote check at review.py:451. Of 28 sample units, only 9 reach the quote check through the route in the test. The other 19 are checked only by the direct `check_excerpt` call in `_check_all_units`. All 28 pass when each is sent to a fresh case (`artifacts/review-evidence/T-108/r2/route_fresh_sample.py`, output route-fresh-sample-output.txt: `{201: 28}`), so the behaviour is right and the evidence is overstated. The AC sentence \"sample units also saved through the real entry/edit routes\" and the handoff's \"no-merge fails 4 tests\" (the mutant gives 8) need correcting.\n- **N2 (minor).** The plain-words reason is not shown anywhere in the UI. `grep -rn sentences_reason app/frontend` returns no matches. The tray shows only the generic line at app/frontend/manual.js:55 (\"This record has no sentences to pick from.\"). excerpt.js:20 returns silently when a record has fewer than two units. The handoff already lists this as left. The API has the status, but the user does not see the reason.\n- **N3 (minor).** The broad fallback in the stored excerpt is still there. `app/backend/store.py:24-25` is `except Exception:` followed by `body = block`. The r1 F2 fix asked for this to be removed, and this commit changes only quote_body. In the shapes I probed `split_records` does not raise, so I saw no wrong result. Any internal exception would still turn the save-check text into the whole block with no status.\n\n## Still open (r1 minors, as the brief allows)\n\n- **F4 (minor).** Curly quotes stay as wrappers. `app/backend/ingest.py:63` strips only straight quotes. One-off run on the archive: `quote_body` on `Date: ...\\nSource: ...\\nExcerpt: <curly open>Pain persists after two weeks. Taking meds daily.<curly close>` gives units `['<curly open>Pain persists after two weeks.', 'Taking meds daily.<curly close>']` (artifacts/review-evidence/T-108/r2/curly-shape-output.txt). The golden cases are clean, so this is latent.\n- **F6 (minor).** `app/frontend/manual.js:14-23` (`quotable`) still removes `===`, `Date:`, `Source:`, the `Excerpt:` label and a trailing quote on the client.\n- **F7 (minor).** `tests/e2e/test_change_the_quote.py:59` (`expect(ed.get_by_test_id(\"excerpt-error\")).to_be_hidden()`) still runs right after the save click, so it passes at once.\n\n## Exercised\n\n- `git show a271014 --stat`, `git show a271014 -- app/backend/present.py memory/contracts/api.md tests/unit/test_quote_units.py`; `git rev-parse HEAD` = a271014.\n- `git archive a271014` into the scratchpad copy `T108_r2_verify`.\n- `.venv/bin/python -m pytest -q tests/unit` on that copy: 2236 passed, 4 skipped.\n- `git clone` of the repo, `git checkout --detach a271014`, then `pytest -q tests/unit`: 2239 passed, 1 skipped; `pytest -q tests/unit/test_quote_units.py`: 35 passed.\n- `.venv/bin/python -I artifacts/review-evidence/T-108/probe_r2.py <archive>`: 25 cases, 591 units, 0 failures on each of the checks above; route check for sample r8 and case_08 r2 (fresh cases).\n- `.venv/bin/python -I artifacts/review-evidence/T-108/r2/route_fresh_sample.py <archive>`: 28 of 28 sample units 201.\n- Label-only, Source-plus-Excerpt and Date-plus-Excerpt shapes through `ingest.split_records` and `present.record_view`.\n- Scratch mutants M1 (no combining) and M2 (find from 0): run on `tests/unit/test_quote_units.py`.\n- Greps: `sentences_reason` in app/frontend; `already has an entry` in review.py and the test; `except Exception` in store.py; manual.js:14-23 and :55; excerpt.js:20; ingest.py:63; test_change_the_quote.py:59.\n- Fixture judge: entries created on the route came back `needs_review` with reason JUDGE_UNAVAILABLE, not verified. That is the expected visible state, though the fixture has no recorded answers for those texts.\n\n**Not exercised:** the e2e `test_change_the_quote.py` was not re-run (the card cites 3 passed on :7966). Live mode was not run, so reachability of the label-only shapes rests on code (api.py:116-120 and :287-288 demo gate). No browser run of the tray or excerpt editor. The CLI `python -m app.pipeline` was not run (not in the brief).\n\n**Outside my lens:** the wording of the tray line in N2.\n\n## What is right\n\n- Each unit the picker can offer saves alone: 591 units across 25 cases, zero failures. The bare hedge-qualified sentence is still refused, so the save rule was not weakened.\n- Tests catch the regressions: removing the merge fails 8 tests, and dropping the start offset fails the repeated-body test.\n- Label-only and Source-plus-Excerpt records now give no units and a plain reason. No LLM is on this path.\n\n```json\n{\"card\": \"T-108\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit a271014 (HEAD): app/backend/present.py (quote_body, quote_units, record_view), tests/unit/test_quote_units.py, memory/contracts/api.md; read-only context: app/backend/store.py:23-25, app/backend/review.py:446 and :451, app/backend/ingest.py:63, app/frontend/manual.js:14-23 and :55, app/frontend/excerpt.js:20, tests/e2e/test_change_the_quote.py:59. Checked on a git archive copy and a git clone at a271014 (scratchpad). App URL not used (no server). Sample case, evals/golden case_01..case_09, 15 library packets in evals/library.\",\n \"exercised\": [\n  \"git show a271014 (stat and per-file diff); git rev-parse HEAD = a271014\",\n  \"git archive a271014 into scratchpad T108_r2_verify; .venv/bin/python -m pytest -q tests/unit: 2236 passed, 4 skipped (artifacts/review-evidence/T-108/r2/unit-run-archive-no-git.txt)\",\n  \"git clone + checkout a271014 (with .git): pytest -q tests/unit: 2239 passed, 1 skipped (unit-run-clone-with-git.txt); pytest -q tests/unit/test_quote_units.py: 35 passed\",\n  \"artifacts/review-evidence/T-108/probe_r2.py (python -I): 25 cases, 180 records, 591 units; 0 not verbatim, 0 alone check failures, 0 grounding.locate failures, 0 wrapper hits; 6 combined units (probe-r2-output.txt)\",\n  \"route: sample r8 unit 0 picked text on a fresh case -> 201; bare first sentence -> 422 invalid_edit; case_08 r2 the same (probe-r2-output.txt)\",\n  \"artifacts/review-evidence/T-108/r2/route_fresh_sample.py (python -I): 28 of 28 sample units -> 201 on fresh cases (route-fresh-sample-output.txt)\",\n  \"label-only, Source-plus-Excerpt, Date-plus-Excerpt shapes through ingest.split_records and present.record_view: [] + sentences_reason; [] + sentences_reason; 2 units\",\n  \"mutant M1 (scratch copy): while False and at present.py:194: pytest tests/unit/test_quote_units.py -> 8 failed, 27 passed (mutant-M1-nocombine.txt)\",\n  \"mutant M2 (scratch copy): find(body) without the label start: pytest tests/unit/test_quote_units.py -> 1 failed, 34 passed (mutant-M2-find0.txt)\",\n  \"greps: sentences_reason in app/frontend (0 matches); already has an entry (review.py:446, test :83); except Exception (store.py:24); manual.js:55; excerpt.js:20; ingest.py:63; test_change_the_quote.py:59\",\n  \"one-off -I run: curly-quote shape gives units with curly marks at both ends (curly-shape-output.txt)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"deterministic_no_llm\": 5, \"golden_units_clean\": 5, \"save_route_parity\": 4, \"edge_shapes_clean\": 4, \"silent_fallback_honesty\": 3, \"test_strength\": 4, \"evidence_reproducible\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"N1: the sample route test checks the quote for 9 of 28 units; the rest pass on the duplicate-entry branch, and the card overstates route coverage and the mutant count\",\n   \"evidence\": \"tests/unit/test_quote_units.py:81-83 (assert r.status_code == 201 or 'already has an entry' in r.text); app/backend/review.py:446 raises the duplicate error before app/backend/review.py:451 runs check_excerpt; artifacts/review-evidence/T-108/r2/route-fresh-sample-output.txt: status counts {201: 28} on fresh cases; handoff text 'no-merge fails 4 tests' vs mutant-M1-nocombine.txt '8 failed, 27 passed'\",\n   \"why_it_matters\": \"The behaviour is correct (28 of 28 save on fresh cases), but the test does not show it for 19 units. A later regression in the route's quote check would pass the sample route test. The AC evidence sentence claims more than the test checks.\",\n   \"fix\": \"In the sample test, submit each unit to the route on a fresh case (or assert that the duplicate response carries no quote-level reason). Correct the AC evidence sentence and the mutant count in the handoff.\",\n   \"acceptance_test\": \"A fresh-case test over all sample units asserts 201 for each. Removing the check_excerpt call in review.manual_entry (review.py:451) makes that test fail.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"N2: sentences_reason is not rendered; the tray shows only a generic line\",\n   \"evidence\": \"grep -rn sentences_reason app/frontend returns no matches; app/frontend/manual.js:55 shows 'This record has no sentences to pick from.'; app/frontend/excerpt.js:20 returns with no message when a record has fewer than two units; handoff lists this as left\",\n   \"why_it_matters\": \"The backend status exists, but the reviewer and the paralegal never see why no picker is offered. The card's visible-state requirement from r1 F2 is only partly met.\",\n   \"fix\": \"Render sentences_reason in the tray (manual.js) and in the excerpt editor when sentences is empty.\",\n   \"acceptance_test\": \"For a record view with sentences [] and a sentences_reason, the tray shows that text (a DOM test or an e2e spec on a label-only input in live mode). Removing the render fails the test.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"N3: the broad except in store.load_records still turns any split error into the whole block\",\n   \"evidence\": \"app/backend/store.py:23-25: try: body = ingest.split_records(block)[0]['excerpt'] / except Exception: / body = block; r1 F2 asked for this to be removed and commit a271014 changes only quote_body\",\n   \"why_it_matters\": \"Any internal exception during the stored-excerpt split silently becomes the whole block, and the save check then runs against header text. No invented fact results (the quote is still verbatim), and the probed shapes do not raise, so I saw no wrong output. It is still the swallow the r1 finding named.\",\n   \"fix\": \"Remove the try/except in store.load_records, or catch only ingest.IngestError and give that record a visible state.\",\n   \"acceptance_test\": \"Monkeypatch ingest.split_records to raise RuntimeError: load_records raises instead of returning the block.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"F4 (r1, still open): curly quotes survive as wrappers in units\",\n   \"evidence\": \"app/backend/ingest.py:63 strips only straight quotes; artifacts/review-evidence/T-108/r2/curly-shape-output.txt: units ['<curly open>Pain persists after two weeks.', 'Taking meds daily.<curly close>']\",\n   \"why_it_matters\": \"The card requires no quote marks in units. Golden cases are clean, so this is latent for pasted text with curly quotes.\",\n   \"fix\": \"Strip matched curly pairs in the excerpt extent, or give the record a state. Extend the quote-mark assertion in test_every_offered_unit_saves_alone_golden to every case.\",\n   \"acceptance_test\": \"The curly shape yields units with no curly or straight double quote marks.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"F6 (r1, still open): manual.js strips the wrapper again on the client\",\n   \"evidence\": \"app/frontend/manual.js:14-23 (quotable): removes === / Date: / Source: lines, the Excerpt: label and a trailing quote from rec.sentences\",\n   \"why_it_matters\": \"A backend leak would be hidden in the tray, and the rule lives in two places that can drift.\",\n   \"fix\": \"The tray takes backend units as they are; keep one copy of the rule.\",\n   \"acceptance_test\": \"A unit fixture with an Excerpt: prefix shown in the tray fails the test.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"F7 (r1, still open): the excerpt-error hidden check runs before the save response\",\n   \"evidence\": \"tests/e2e/test_change_the_quote.py:59 expect(ed.get_by_test_id('excerpt-error')).to_be_hidden() runs right after the btn-save-excerpt click\",\n   \"why_it_matters\": \"The check passes at once, so it proves nothing. The final assertion still protects the outcome.\",\n   \"fix\": \"Wait for the save response (expect_response), or drop line 59.\",\n   \"acceptance_test\": \"The spec passes on the fixed build and fails when the picker submit is broken.\"}\n ],\n \"whats_right\": [\n  \"Every unit the picker can offer saves alone: 591 units over 25 cases, zero alone or grounding failures; the bare hedge-qualified sentence is still refused, so the rule was not weakened\",\n  \"The tests catch the regressions: removing the merge fails 8 tests, and dropping the start offset fails the repeated-body test\",\n  \"Label-only and Source-plus-Excerpt records give no units and a plain sentences_reason; no LLM is on this path\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T06:49:07.902Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:12.499Z

**tool call — Bash**
````
{
 "command": "grep -c '```' reviews/T-108-staff-engineer-r2.md; grep -n '```' reviews/T-108-staff-engineer-r2.md; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json, re\nt = open('/Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer-r2.md', encoding='utf-8').read()\nblocks = re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd = json.loads(blocks[0])\nprint('verdict:', d['verdict'], '| card:', d['card'], '| persona:', d['persona'], '| model:', d['model'])\nsev = [f['severity'] for f in d['findings']]\nprint('findings:', len(sev), {s: sev.count(s) for s in set(sev)})\nblk = [s for s in sev if s == 'blocker' or s == 'major']\nrule = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('rule verdict:', rule, 'matches:', rule == d['verdict'])\n\"",
 "description": "Validate the review's single JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T06:49:12.554Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:15.665Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/check_review_r2.py",
 "content": "\"\"\"Reviewer check (scratch): the r2 review has exactly one json fence, parses, and its verdict follows the D.2 rule.\"\"\"\nimport json\nimport re\nimport sys\n\npath = sys.argv[1]\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nprint(\"fence lines:\", text.count(fence))\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"card:\", d[\"card\"], \"| persona:\", d[\"persona\"], \"| model:\", d[\"model\"], \"| verdict:\", d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"findings by severity:\", {s: sev.count(s) for s in sorted(set(sev))})\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"rule verdict:\", rule, \"| matches file:\", rule == d[\"verdict\"])\n"
}
````

### User / tool · 2026-11-02T06:49:15.768Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-108/r2/check_review_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:17.188Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I artifacts/review-evidence/T-108/r2/check_review_r2.py /Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer-r2.md",
 "description": "Validate the review file fence count, JSON, and verdict rule"
}
````

### User / tool · 2026-11-02T06:49:17.292Z

**tool result**
````
fence lines: 2
json blocks: 1
card: T-108 | persona: staff-engineer-reviewer | model: claude-haiku-5-5 | verdict: pass
findings by severity: {'minor': 6}
rule verdict: pass | matches file: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:27.303Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t108_quote_units_patterns.md",
 "content": "---\nname: project_t108_quote_units_patterns\ndescription: T-108 r1 d3e127c (changes) and r2 a271014 (pass): test helper vs UI, whole-block fallback, surviving offset mutant, combined units, store.py broad except, sentences_reason not rendered\nmetadata:\n  type: project\n---\n\nT-108 (quote-picker units from the excerpt body). r1 d3e127c: reviews/T-108-staff-engineer.md, changes (0 blockers, 2 majors, 5 minors, 1 nit). r2 a271014: reviews/T-108-staff-engineer-r2.md, pass (0 blockers, 0 majors, 6 minors).\n\nr1 patterns (still useful):\n- **A test helper that models the UI but is not the UI.** `_pick` added the trailing hedge chain; excerpt.js `pick(i)` never did, so the unit test was green while the UI refused 3 of 150 units. How to apply: diff any \"the way the UI does it\" helper against the UI source and submit the UI-built text in the probe.\n- **Wrapper-stripping helper with a whole-block fallback.** `quote_body` returned `(0, block)` on a miss, so label-only or date-less records leaked `Excerpt:` and header lines into units. How to apply: probe the shapes the golden set lacks (label-only, date-less, curly quotes, a header that repeats the body).\n- **Surviving mutant on a redundant branch.** Disabling the label-offset branch passed all quote tests on golden data; only a repeated body (header and excerpt both contain it) separates them. How to apply: when a mutant survives, build the input where the two branches differ.\n\nr2 patterns:\n- **Fix at the point the tests read, not the point the defect lives.** r2 made the picker's units combined (`quote_units` in present.py, decided by the save route's own check) so excerpt.js did not change and every unit saves alone. Verified: 591 units over 25 cases, 0 alone failures; bare hedge-qualified sentence still 422. How to apply: check the save rule still refuses the bare sentence, or the fix may have weakened it.\n- **Route-level evidence masked by a duplicate branch.** In the sample route test, only the first unit per tray record reaches the quote check: review.py:446 (duplicate entry) runs before :451 (check_excerpt), and the test accepts \"already has an entry\". 9 of 28 sample units are route-checked in the test; 28 of 28 pass on fresh cases. How to apply: when a route test loops over one record, look for a duplicate or idempotency branch that returns success before the check under test.\n- **Reason computed but not rendered.** `sentences_reason` exists in record_view but nothing in app/frontend reads it (grep count 0). The tray shows a generic line. How to apply: grep the frontend for every new API field the commit documents as \"shown\".\n- **Broad except left in a sibling file.** store.py:24-25 keeps `except Exception: body = block` after the fix removed the same pattern in present.py. How to apply: when a finding names a pattern, grep the whole package for it, not just the file in the diff.\n- **Handoff counts need a re-run.** Handoff said no-merge mutant fails 4 tests; the same one-line change fails 8 in test_quote_units.py.\n- **Count depends on .git.** Archive copy: 2236 passed, 4 skipped; git clone at the same commit: 2239 passed, 1 skipped (3 tests skip without .git). Reproduce counts in a clone, not a bare archive.\n\nEnvironment (both rounds):\n- reviewer-write-guard refused a Write under the scratchpad; put probes under artifacts/review-evidence/T-108/ (r2 files in r2/).\n- git-guard denies Bash commands with backslash escapes, including a `python -c` with `\\`` regex. Put checks in a script file under artifacts/review-evidence and run it.\n- `timeout` is not installed on this host; run pytest without it.\n- Clone for a .git-dependent count: `git clone --quiet <repo> <scratch>` then `git checkout --detach <sha>` (reads the repo, writes nothing to it).\n\nRelated: [[feedback_review_write_once]], [[project_e2e_contract_review_patterns]], [[feedback_shared_scratchpad]], [[project_t080_trace_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T06:49:27.392Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t108_quote_units_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:28.719Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && grep -n \"T-108 quote-units\" MEMORY.md",
 "description": "Locate the T-108 index line in memory index"
}
````

### User / tool · 2026-11-02T06:49:28.798Z

**tool result**
````
39:- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — d3e127c changes: test helper adds hedge the picker never adds, whole-block fallback leaks label, surviving offset mutant
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:30.613Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — d3e127c changes: test helper adds hedge the picker never adds, whole-block fallback leaks label, surviving offset mutant",
 "new_string": "- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — r1 d3e127c changes; r2 a271014 pass: masked route checks, sentences_reason unrendered, store.py broad except, clone for .git count"
}
````

### User / tool · 2026-11-02T06:49:30.717Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:49:33.066Z

T-108 r2 (a271014) passes with 0 blockers and 0 majors: 6 minors (3 new, F4/F6/F7 still open), unit suite 2239 passed / 1 skipped in a git clone (2236 / 4 on a bare archive), review at /Users/arsis/zlayt-pm-project/reviews/T-108-staff-engineer-r2.md.
