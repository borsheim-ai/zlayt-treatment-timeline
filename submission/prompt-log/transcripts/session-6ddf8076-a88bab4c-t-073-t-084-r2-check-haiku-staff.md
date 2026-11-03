# Subagent: T-073/T-084 r2 check (haiku staff) (T-073/T-084 r2 check (haiku staff))

Source: `agent-a88bab4c35ad5927a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:39:29.902Z

Round-2 check of board cards T-073 and T-084 in /Users/arsis/zlayt-pm-project (commit c8a9874, with billing restored in e2b4e3f). Read reviews/T-073-staff-engineer.md and reviews/T-084-staff-engineer.md, and test a clean worktree of HEAD (`git worktree add <scratchpad>/wt HEAD`, then remove it).

- **T-084:**
  - a restore after a rerun runs the full guard when the class or the sentence changed;
  - "Charge per visit $185" and "Billed $150 per visit" are refused before the judge;
  - a rate can never reach totals without both checks.
  Mutate the rate-cue rule in a scratch copy to confirm a test fails. Also judge the extra behaviour the worker added: a promoted charge falls back to the code's class when a rerun changes its sentence. Open finding F5 (the item change and audit row not in one transaction) is fine to carry as a minor.
- **T-073:**
  - audited_call retries only provider, transport and validation errors, and programmer errors propagate after one llm_calls row;
  - ladder.judge.error_class is set for LLMFailed (it's done in judge_guard.py).
- **Billing:** confirm billing.py, test_billing.py and the api hook are back in HEAD.

Run `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`. Write reviews/T-073-staff-engineer-r2.md and reviews/T-084-staff-engineer-r2.md. Each needs a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:31.660Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:39:31.670Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:31.866Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-073-staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:39:31.874Z

**tool result**
````
1	# T-073 review: narrow the broad except in the review.py judge path (staff-engineer)
2	
3	Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit reviewed: 7724412 (T-073). HEAD at review time was ec33bf0 (T-084); the T-073 files are unchanged between 7724412 and ec33bf0 (`git diff --stat 7724412 ec33bf0 -- app/backend/review.py app/backend/judge_guard.py app/backend/judges.py app/llm/audited.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py` prints nothing). The working tree moved during the review (other workers' uncommitted changes, including app/backend/reclassify.py and tests/unit/test_reclassify.py), so I pinned HEAD with `git archive ec33bf0` into the session scratchpad.
4	
5	## Summary
6	
7	The guard itself is narrow and does what the card says at the seam it is tested at: `judge_guard.guarded` (judge_guard.py:15-16) returns `unavailable` with the class name for `LLMFailed`, `LLMError` and `FixtureMissing`, and lets everything else raise. Four deliberate mutations of the guard are all caught (4/4).
8	
9	The acceptance criterion does not hold on the real call path, though. Two gaps:
10	1. A programmer bug raised inside the real judge call is not propagated. `app/llm/audited.py:70` has its own `except Exception`, which retries the call three times and reports it as a judge that did not answer. The unit test that claims propagation fakes the call one layer above, so it never reaches that code.
11	2. `LLMFailed`, the error the card's AC names as recorded with `ladder.judge.error_class`, never reaches the guard. `judges._run` turns it into `unavailable` with reason `NONE` and no class.
12	
13	Neither gap lets an unverified item through as verified (the state is `needs_review`), so both are major, not blocker. Verdict: changes.
14	
15	## Exercised (what I actually ran or read)
16	
17	- `python3 tools/board.py show T-073` (card AC, handoff, note "Left: LLMFailed is already swallowed inside judges._run").
18	- `git show --stat 7724412`; `git show 7724412 -- app/backend/judge_guard.py app/backend/review.py tests/unit/test_review_rules.py`; `cat -n tests/unit/test_judge_guard.py`; `cat -n app/backend/judge_guard.py`.
19	- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` in the working tree: `109 passed, 1173 deselected`.
20	- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass" --collect-only -q | grep -c judge_guard`: `0`. The brief's `-k` selector does not collect `tests/unit/test_judge_guard.py` at all, so I also ran that file on its own: `.venv/bin/python -m pytest -q tests/unit/test_judge_guard.py` gives `10 passed`.
21	- HEAD archive (`git archive ec33bf0` into the scratchpad, `head-ec33bf0`): `-k "review or reclass"` gives `107 passed, 1068 deselected`; `test_judge_guard.py` gives `10 passed`.
22	- Scratch mutants (`artifacts/review-evidence/T-073-T-084/mutate.py`, log in `artifacts/review-evidence/T-073-T-084/mutation-run.txt`), run on the HEAD archive with `test_judge_guard.py` and `test_review_rules.py`. Control: `55 passed`.
23	  - A, `judge_guard.py` `except EXPECTED_JUDGE_ERRORS` changed to `except Exception`: `4 failed` (the three unexpected-error cases and the edit-propagates case).
24	  - B, `review.py:100` guard call replaced by a direct `judges.run_j1_meta` call: `3 failed`.
25	  - C, expected errors return `supported` instead of `unavailable`: `6 failed`.
26	  - D, error class dropped (`None` instead of `type(e).__name__`): `4 failed`.
27	- Probes on the HEAD archive (`artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py`, `probe_t073_adapter_bug_through_audited.py`; output in `artifacts/review-evidence/T-073-T-084/probe-run.txt`).
28	- `grep -n "except" app/backend/review.py app/backend/judge_guard.py app/backend/judges.py app/llm/audited.py` and `git show 7724412:app/llm/audited.py | grep -n "except Exception as e:"` (line 70).
29	
30	## Findings
31	
32	### F1 (major): a programmer bug in the real judge call is retried and hidden as JUDGE_UNAVAILABLE
33	
34	- `app/llm/audited.py:70`: `        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text`. Any exception from the provider call or `validate` is caught here, recorded as `_error_code(e)`, and retried (`MAX_ATTEMPTS = 3` at audited.py:15, `raise LLMFailed(...)` at audited.py:92).
35	- `app/backend/judges.py:33-34`: `except AU.LLMFailed:` then `return "unavailable", None, "NONE"`. The reason is `NONE` and the class is not kept on the ladder.
36	- Reproduction: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py` run against the HEAD archive. A provider adapter raising `RuntimeError("programmer bug in provider adapter")`, called through the real `AU.audited_call`, gives:
37	  - `llm_calls: [{'step': 'j1', 'attempt': 1, 'error': 'RuntimeError'}, {'step': 'j1', 'attempt': 2, 'error': 'RuntimeError'}, {'step': 'j1', 'attempt': 3, 'error': 'RuntimeError'}]`
38	  - `warnings: ['JUDGE_UNAVAILABLE'] state: needs_review judge: {'verdict': 'unavailable', 'reason_code': 'NONE'} error_class in ladder: False`
39	- The propagation test in the card (`tests/unit/test_judge_guard.py:45-52`) raises `RuntimeError` from a raw fake call that is passed straight to `apply_review`. It never enters `audited_call`, so the mutation that matters here is invisible to it.
40	- Why it matters: the AC says "others propagate". On the production path they are retried three times and shown to the paralegal as a judge that did not answer, with the reason `NONE`. The class survives only in the `llm_calls` rows. This is the "swallowed exception" pattern from the dossier (§3, checklist item 12). It is not a verified-item leak, so it is major.
41	- Fix: narrow `audited.py:70` to provider and LLM errors (`P.LLMError` and our own codes). Let every other exception propagate out of `audited_call` without a retry. The owner is backend, but `app/llm/**` and `judges.py` are outside this card's stated scope (handoff: "judges.py off limits"), so this needs its own card.
42	- Acceptance test: `audited_call` with a `complete_with_meta` that raises `RuntimeError` raises `RuntimeError` to the caller and writes exactly one `llm_calls` row. The same provider through `apply_review` raises and saves nothing (the card's own propagation assertion, now on the real path).
43	
44	### F2 (major): error_class is not recorded for LLMFailed, which the AC names
45	
46	- Card AC (`board.py show T-073`, ac[0].text): "LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class". The AC evidence says the same.
47	- `app/backend/judges.py:33-34` returns before the guard sees the exception, so `judge_guard.py:15` never handles `LLMFailed` on the production path.
48	- Reproduction: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py`. With `FakeCall({"j1": AU.LLMFailed("down")})`: `LLMFailed path judge ladder: {'reason_code': 'NONE', 'verdict': 'unavailable'} warnings: ['JUDGE_UNAVAILABLE'] state: needs_review`. There is no `error_class`. The same probe with `P.LLMError("TIMEOUT")` does record `'error_class': 'LLMError'`, because that one escapes `_run`.
49	- Tests do not catch it. `tests/unit/test_judge_guard.py:15-16` asserts only the reason code `NONE` for `LLMFailed`. `tests/unit/test_review_rules.py:148-156` (the parametrized `AU.LLMFailed` case) asserts state, reasons and verdict, not `error_class`.
50	- The handoff's "Left" note admits this, but the AC evidence still lists `LLMFailed` as recorded with its class. The evidence overstates what the code does.
51	- Fix: have `judges._run` return the class (for example `"LLMFailed"`) or re-raise `LLMFailed` to the guard, so the ladder carries `error_class` for every expected failure. If that stays out of scope, correct the AC evidence now.
52	- Acceptance test: add `assert it["ladder"]["judge"]["error_class"] == "LLMFailed"` to the `AU.LLMFailed` case in `tests/unit/test_review_rules.py:148`. It fails on HEAD today.
53	
54	### F3 (minor): the brief's test selector drops the T-073 guard tests
55	
56	- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` collects 0 tests from `tests/unit/test_judge_guard.py` (see Exercised). The guard's 10 tests run only when the file is named explicitly.
57	- Fix: add `or guard` to the selector (or name `test_judge_guard.py` in the brief). Not a product defect; it is a verification gap in how the card was checked.
58	
59	## What is right
60	
61	- `app/backend/judge_guard.py:15-16` maps expected errors to `unavailable` with the class name, never to a positive verdict. Mutant C (expected becomes `supported`) is caught by 6 tests.
62	- Unexpected errors at the guard seam propagate and save nothing: `tests/unit/test_judge_guard.py:31-33` and `:45-52`. Mutant A (broad catch) is caught by 4 tests.
63	- Mutants B (guard removed from `review.py:100`) and D (class dropped) are both caught, so the wiring at `review.py:100` and the ladder write are tested, not just the helper.
64	
65	## Scores
66	
67	```
68	no_silent_fallback 3 (expected errors visible as needs_review; the unexpected path is not)
69	error_class_recorded 2 (only when the error escapes judges._run)
70	propagation_on_real_path 2 (audited.py:70 retries bugs)
71	tests_kill_mutants 4 (4/4 seam mutants caught; real-path mutant not covered)
72	ac_evidence_matches_code 2 (LLMFailed class claim)
73	```
74	
75	## Questions for Chris
76	
77	- Should a judge that hits a programmer bug show `JUDGE_UNAVAILABLE` (ADR-005 wording, the paralegal can retry) or a visible error state (a bug, not a judge outcome)? The answer decides where F1 is fixed.
78	
79	<!-- Verdict rule: 0 blockers, 2 majors -> changes. -->
80	
81	```json
82	{"card": "T-073", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
83	 "scope": "commit 7724412 (T-073), pinned HEAD ec33bf0 via git archive; files app/backend/judge_guard.py, app/backend/review.py, tests/unit/test_judge_guard.py, tests/unit/test_review_rules.py; app/llm/audited.py and app/backend/judges.py read for the real path; no app URL; no sample case (unit-level card)",
84	 "exercised": ["python3 tools/board.py show T-073", "git show --stat 7724412; git show 7724412 -- app/backend/judge_guard.py app/backend/review.py tests/unit/test_review_rules.py", "cat -n app/backend/judge_guard.py tests/unit/test_judge_guard.py", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' (working tree: 109 passed, 1173 deselected)", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' --collect-only -q | grep -c judge_guard (0)", ".venv/bin/python -m pytest -q tests/unit/test_judge_guard.py (10 passed)", "git archive ec33bf0 into scratchpad head-ec33bf0: -k 'review or reclass' 107 passed; test_judge_guard.py 10 passed", "scratch mutants A-D via artifacts/review-evidence/T-073-T-084/mutate.py: A 4 failed, B 3 failed, C 6 failed, D 4 failed; control 55 passed", "probes: artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py (3x RuntimeError in llm_calls, JUDGE_UNAVAILABLE, no class), probe_t073_llmfailed_class.py (LLMFailed: no error_class)", "grep -n except on review.py, judge_guard.py, judges.py, audited.py; git show 7724412:app/llm/audited.py line 70"],
85	 "verdict": "changes",
86	 "scores": {"no_silent_fallback": 3, "error_class_recorded": 2, "propagation_on_real_path": 2, "tests_kill_mutants": 4, "ac_evidence_matches_code": 2},
87	 "findings": [
88	  {"severity": "major", "title": "A programmer bug in the real judge call is retried 3x and hidden as JUDGE_UNAVAILABLE (broad except one layer down)",
89	   "evidence": "app/llm/audited.py:70 `except Exception as e:` (then retry, MAX_ATTEMPTS=3 at audited.py:15, raise LLMFailed at audited.py:92); app/backend/judges.py:33-34 `except AU.LLMFailed:` -> return unavailable/NONE; repro artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py -> llm_calls error RuntimeError x3, warnings ['JUDGE_UNAVAILABLE'], state needs_review, error_class absent; tests/unit/test_judge_guard.py:45-52 raises from a raw fake call that bypasses audited_call",
90	   "why_it_matters": "The AC says anything other than an expected judge error propagates. On the production path a bug is retried and reported to the paralegal as a judge that did not answer, with reason NONE. The class survives only in llm_calls. Not a verified-item leak (state is needs_review), so major, not blocker.",
91	   "fix": "Narrow audited.py:70 to provider/LLM errors (P.LLMError and our own codes); let other exceptions propagate without retry. app/llm and judges.py are outside this card's stated scope, so raise it as its own backend card.",
92	   "acceptance_test": "audited_call with complete_with_meta raising RuntimeError raises RuntimeError to the caller and writes one llm_calls row; the same provider through apply_review raises and saves nothing."},
93	  {"severity": "major", "title": "error_class is not recorded for LLMFailed, which the AC names explicitly",
94	   "evidence": "card T-073 ac[0].text: 'LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class'; app/backend/judges.py:33-34 returns before the guard sees the exception; repro artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py -> 'LLMFailed path judge ladder: {'reason_code': 'NONE', 'verdict': 'unavailable'} ... state: needs_review'; tests/unit/test_judge_guard.py:15-16 asserts only code NONE; tests/unit/test_review_rules.py:148-156 does not assert error_class",
95	   "why_it_matters": "The class is the audit's answer to 'why did the judge not run'. For the most common expected failure (LLMFailed after retries) the ladder records NONE. The AC evidence claims otherwise.",
96	   "fix": "Make judges._run return the class (e.g. 'LLMFailed') or re-raise LLMFailed to the guard, so every expected failure lands in ladder.judge.error_class. If deferred, correct the AC evidence now.",
97	   "acceptance_test": "In tests/unit/test_review_rules.py:148 (the AU.LLMFailed case) assert it['ladder']['judge']['error_class'] == 'LLMFailed'; fails on HEAD today."},
98	  {"severity": "minor", "title": "The brief's -k selector collects zero tests from test_judge_guard.py",
99	   "evidence": ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' --collect-only -q | grep -c judge_guard -> 0; .venv/bin/python -m pytest -q tests/unit/test_judge_guard.py -> 10 passed",
100	   "why_it_matters": "The guard file that holds the T-073 behaviour tests is skipped by the standard selection for this card, so a regression there does not show in the card's selector run.",
101	   "fix": "Add 'or guard' to the -k expression, or list tests/unit/test_judge_guard.py explicitly.",
102	   "acceptance_test": "The selector collects at least the 10 test_judge_guard.py tests (--collect-only shows them)."}
103	 ],
104	 "whats_right": [
105	  "app/backend/judge_guard.py:15-16 maps expected errors to unavailable with the class name and never to a positive verdict (mutant C caught by 6 tests).",
106	  "Unexpected errors at the guard seam propagate and save nothing (tests/unit/test_judge_guard.py:31-33 and :45-52); mutant A (broad catch) caught by 4 tests.",
107	  "Mutants B (guard removed at review.py:100) and D (class dropped) are both caught, so the wiring and the ladder write are tested, not only the helper."
108	 ],
109	 "questions_for_chris": ["For a judge that hits a programmer bug, should the paralegal see JUDGE_UNAVAILABLE (retryable, ADR-005 wording) or a visible error state (a bug, not a judge outcome)? The answer decides where F1 is fixed."]}
110	```
111	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:32.070Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:39:32.078Z

**tool result**
````
1	# T-084 review: guarded charge reclassification (D-042) (staff-engineer)
2	
3	Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit reviewed: ec33bf0 (T-084), with the T-073 commit 7724412 underneath it. HEAD was pinned with `git archive ec33bf0` into the session scratchpad because the working tree moved during the review (app/backend/reclassify.py and tests/unit/test_reclassify.py now show uncommitted edits from another worker; I did not review those).
4	
5	## Summary
6	
7	The guard works for the cases the tests name. Judge disagree, unsure or unavailable gives a 422 with nothing changed. Missing wording gives a 422 with the judge never called. Seven scratch mutants of the guard are all caught. Demotion from charge to not-a-charge is allowed, leaves the total, and is audited.
8	
9	Three things break the invariant the brief asked me to check, "totals never include a reclassified rate without both checks passing":
10	
11	1. **Blocker.** Undoing a demotion ("restore") skips both checks, and it does so on the stored judge answer from the old sentence. If a rerun changes the code's class for the same figure, a restore turns a current rate into a charge with no check at all. Reproduced.
12	2. **Blocker.** The commit ec33bf0 deletes T-083's billing module, its tests, its API route and its API documentation, which were committed in f218263. The deletion is not in the commit message or the card. HEAD no longer serves `GET /api/cases/{token}/billing`, which D-042 reinstates.
13	3. **Major.** The code wording check accepts the rate phrase itself. "Charge per visit $185" and "Billed $150 per visit" both pass as "charged-amount wording", so the judge is the only gate for the exact case the brief names. Reproduced.
14	
15	Verdict: fail (two blockers).
16	
17	## Exercised (what I actually ran or read)
18	
19	- `python3 tools/board.py show T-084` and `show T-083` (AC, handoff, the "NEEDS DB CARD" note, the T-083 commit list).
20	- `git show --stat ec33bf0`; `git show ec33bf0 -- app/backend/api.py app/backend/pipeline.py`; `git show ec33bf0 -- memory/contracts/api.md` (39 lines removed, 24 added).
21	- `git ls-tree -r --name-only ec33bf0 | grep -i billing` gave no output. `git ls-tree -r --name-only f218263 | grep -i billing` gave `app/backend/billing.py` and `tests/unit/test_billing.py`. `git show ec33bf0:app/backend/api.py | grep -n billing` gave no output. `git show f218263:app/backend/api.py` lines 497-498 are the billing hook. `git status --short app/backend/billing.py tests/unit/test_billing.py` gave `?? app/backend/billing.py` and `?? tests/unit/test_billing.py` (the files exist on disk, untracked).
22	- `git show ec33bf0:app/backend/reclassify.py` (full read; line numbers cited below are HEAD's), and `git show ec33bf0:tests/unit/test_reclassify.py` (full read).
23	- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` in the working tree: `109 passed, 1173 deselected`. HEAD archive: `107 passed, 1068 deselected`.
24	- Scratch mutants on the HEAD archive (`artifacts/review-evidence/T-073-T-084/mutate.py`, log `artifacts/review-evidence/T-073-T-084/mutation-run.txt`):
25	  - t084-1 judge gate removed: 5 failed.
26	  - t084-2 wording gate removed: 2 failed.
27	  - t084-3 negation gate removed: 2 failed.
28	  - t084-4 judge "unsure" accepted: 1 failed.
29	  - t084-5 audit write removed: 4 failed.
30	  - t084-6 value gate removed: 1 failed.
31	  - t084-7 judge refusal turned into a pass: 5 failed.
32	  - Control: 55 passed.
33	- Probes on the HEAD archive (`artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py`, `probe_t084_billed_150_per_visit.py`; output `artifacts/review-evidence/T-073-T-084/probe-run.txt`).
34	- Grep for `except` in reclassify.py, judge_guard.py, review.py (none in reclassify.py).
35	
36	## Findings
37	
38	### F1 (blocker): restore after a rerun turns a current rate into a charge with no check
39	
40	- `app/backend/reclassify.py:102-104` (HEAD): `restored = original == "charge" and prior.get("previous_judge") is not None`, then `if not restored:` skips `_guard` (both checks). `carry_over` at `reclassify.py:157-163` keeps her demotion when a rerun reaches the same figure text and value (`reclassify.py:160`: `old["text"] != it["text"] or old["value_cents"] != it["cents"]`). It does not compare the sentence, so a changed sentence still matches.
41	- Reproduction (`artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py`, `test_probe_restore_after_rerun_class_flip`). Seed TEXT (charge `$310` in record 3, "MRI performed. Charge: $310."). Demote it to not-a-charge. Rerun the pipeline with record 3 changed to "MRI performed. Rate of $310 per visit." (same figure, same value). The current code now calls it a rate. Then reclassify to charge with `call=None` (no judge available). Output:
42	  ```
43	  rerun with code class flipped to rate:
44	     a3 $310 ['r3'] kind= unclear
45	  RESTORE WITHOUT ANY CHECK -> charge restored= True pending total= 31000
46	  ```
47	  The sentence "Rate of $310 per visit." has no charged wording and the judge never ran on it, yet the figure is a charge in the pending total.
48	- Why it matters: D-042 says a rate becomes a charge only with code-verified charged wording AND a judge re-check. The restore path uses a judge answer about the old sentence ("Charge: $310.") and skips the code check. The brief's invariant ("totals never include a reclassified rate without both checks passing") fails. The trigger is a rerun that changes the code's class of a figure with the same text and value, which is what a classifier or lexicon change does. The sample case is not affected, but the defect is the one that ends in a total the records do not support (dossier §5, "a total that includes the $185 rate").
49	- Fix: a restore may skip the checks only when the current rerun's code class still equals the class at demotion and the sentence is unchanged. Otherwise run `_guard` again. Compare the sentence (or a hash of the excerpt), not only text and cents, in `carry_over`.
50	- Acceptance test: seed as above, demote, rerun with the flipped sentence, then reclassify to charge with `call=None`. Expect 422 `NO_CHARGE_WORDING` (or `JUDGE_UNAVAILABLE`), kind stays `unclear`, no reclassify event. Add a second case where the sentence is unchanged and the restore still passes without a judge (keeps `test_undoing_her_own_demotion_...` at `test_reclassify.py:80-87` true).
51	
52	### F2 (blocker): commit ec33bf0 deletes T-083's committed billing module, tests and API route
53	
54	- `git show --stat ec33bf0` lists `app/backend/billing.py | 642 ------` and `tests/unit/test_billing.py | 330 ----------`. Neither is in the commit message ("feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)").
55	- `git ls-tree -r --name-only ec33bf0 | grep -i billing` gives nothing. `git ls-tree -r --name-only f218263 | grep -i billing` gives both files.
56	- `app/backend/api.py`: at f218263, lines 497-498 are `from app.backend import billing` and `billing.add_routes(app, conn=conn, get_case=get_case)       # T-083`. At ec33bf0 those lines are replaced by the reclassify hook (`api.py:497-498`), so `GET /api/cases/{token}/billing` is no longer registered.
57	- `git show ec33bf0 -- memory/contracts/api.md` removes the `GET /api/cases/{token}/billing` row and the "T-083, D-042" section.
58	- The T-083 card still lists `commits: ["f218263"]` with its evidence `tests/unit/test_billing.py: 27 passed`. That file does not exist at HEAD, so the evidence cannot be reproduced at HEAD.
59	- D-042 (`memory/ORCHESTRATOR_DECISIONS.md:50`) reinstates "billing analysis on synthetic itemized ledgers". Removing it from HEAD without a recorded scope decision violates that decision. The files are not lost: they are on disk, untracked, and in f218263.
60	- Why it matters: a commit labelled as one feature silently removes another card's delivered work from the tree. The T-084 review cannot tell whether the removal is intended.
61	- Fix: restore `app/backend/billing.py`, `tests/unit/test_billing.py`, the `billing.add_routes` hook and the api.md section in a commit under T-083 (`git add` those paths explicitly). If the removal was intended, record it in `memory/SCOPE_CUTS.md` and `memory/ORCHESTRATOR_DECISIONS.md` and update T-083 first. Do not rewrite history.
62	- Acceptance test: `git ls-tree -r --name-only HEAD | grep billing` lists both files. `tests/unit/test_billing.py` passes at HEAD. A route test gets 200 from `GET /api/cases/{token}/billing`.
63	
64	### F3 (major): the code wording check passes the rate phrase itself
65	
66	- `app/backend/reclassify.py:24` `_WORDING` matches `charges?` and `billed`. `charge_wording` only checks that some charged-amount word is in the same sentence. It does not check whether the figure is a rate.
67	- Reproduction (`probe-run.txt`): `wording(Charge per visit $185): Charge` and `wording(Billed $150 per visit): Billed`. Full path with the brief's example, "Visit completed. Billed $150 per visit.", judge answering `agree`: `after judge agree: charge wording: Billed pending total cents: 15000 accepted: 0`. With record 2 of the test fixture ("Charge per visit $185."): `sneak: amount kind after judge agree = charge pending total cents = 49500`.
68	- The tests encode this as the expected path. `tests/unit/test_reclassify.py:108-116` (HEAD) reclassifies the rate "Charge per visit $185." to a charge on judge agreement alone and asserts a pending total of 31000 + 18500.
69	- Why it matters: D-042 is literally met (wording present, judge agrees), so this is not a spec breach as written. But the code check is supposed to be the first independent gate, and for a rate sentence it always passes. The only gate left for the exact case the brief names is one LLM judge, and the record states a rate, not a charge, so a $150-per-visit figure is summed as if it were billed. If Chris reads D-042 as excluding rate sentences, this becomes a blocker.
70	- Fix: the code check refuses a figure whose sentence carries a rate unit ("per", "each", "a visit", "per unit", "rate of") next to the figure. Keep the wording check for statements of charge.
71	- Acceptance test: `charge_wording` and `reclassify` return `None` / 422 `NO_CHARGE_WORDING` (judge not called) for "Visit completed. Charge per visit $185." and "Visit completed. Billed $150 per visit.". Move the positive case at `test_reclassify.py:108` to a sentence with no rate unit (for example "Billed $185 for the visit.").
72	
73	### F4 (minor): the reclassify audit row is stored with action 'edit'
74	
75	- `app/backend/reclassify.py:22` `AUDIT_ACTION = "edit"`. The payload carries `event: "reclassify"` (`reclassify.py:123`). `test_reclassify.py:215` asserts the action is `["edit"]`.
76	- The AC ("an audit event is written") is met. The action column still says a summary was edited, which misleads anyone reading `review_events` directly.
77	- Fix: as the card notes, the DB card adds `reclassify` to the CHECK (bump SCHEMA_VERSION per `app/db/db.py:32`) and then flips the constant.
78	- Acceptance test: `GET /audit` shows action `reclassify` for the event, and the test at `test_reclassify.py:215` asserts it.
79	
80	### F5 (minor, read from code, not reproduced): the state change and its audit row are separate writes
81	
82	- `reclassify.py:120` (`DB.update_item`), `:122` (`review.batch_apply`, which has its own `BEGIN`/`COMMIT` in `db.py`), and `:123` (`_log` INSERT) are three separate statements. A failure after `:120` leaves the item changed with no event.
83	- Fix: write the audit row and the item change in one transaction, the way `db.apply_review` does.
84	- Acceptance test: inject a failure at the `_log` call and assert the item is unchanged.
85	
86	## What is right
87	
88	- Seven of seven scratch mutants of the reclassify guard are caught (judge gate, wording gate, negation, "unsure" accepted, audit, value gate, judge refusal turned into a pass). See `artifacts/review-evidence/T-073-T-084/mutation-run.txt`.
89	- Judge disagree, unsure or unavailable gives a 422 with the item unchanged and no event (`test_reclassify.py:124-139`).
90	- Demotion from charge to not-a-charge leaves the total unchanged, moves the item back to pending and writes the audit (`test_reclassify.py:59-70`).
91	
92	## Scores
93	
94	```
95	no_rate_into_total_without_both_checks 2 (F1 restore bypass)
96	code_check_strength 2 (F3 rate phrase passes)
97	judge_gate 4 (mutants caught; refusals leave nothing changed)
98	audit_trail 3 (written; wrong action label)
99	commit_scope 1 (F2 deletes T-083 from HEAD)
100	tests_kill_mutants 5
101	```
102	
103	## Questions for Chris
104	
105	- Was the removal of `app/backend/billing.py` and `tests/unit/test_billing.py` in ec33bf0 intended as a scope cut? If yes, it needs a SCOPE_CUTS entry and a D-042 update before T-083 can be closed. If no, it needs a restore commit (F2).
106	- Does D-042 allow a rate sentence ("Charge per visit $185.") to satisfy "charged-amount wording"? My reading is that it should not. The decision text does not say.
107	
108	```json
109	{"card": "T-084", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
110	 "scope": "commit ec33bf0 (T-084, D-042) pinned via git archive, with 7724412 (T-073) underneath; files app/backend/reclassify.py, app/backend/api.py, app/backend/pipeline.py, memory/contracts/api.md, tests/unit/test_reclassify.py; no app URL; no sample-case CLI run (unit-level card)",
111	 "exercised": ["python3 tools/board.py show T-084 and show T-083", "git show --stat ec33bf0; git show ec33bf0 -- app/backend/api.py app/backend/pipeline.py memory/contracts/api.md", "git ls-tree -r --name-only ec33bf0 | grep -i billing (none) vs f218263 (2 files); git show f218263:app/backend/api.py lines 497-498", "git status --short app/backend/billing.py tests/unit/test_billing.py (both untracked)", "full read of git show ec33bf0:app/backend/reclassify.py and tests/unit/test_reclassify.py", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass': working tree 109 passed; HEAD archive 107 passed", "scratch mutants t084-1..7 on HEAD archive via artifacts/review-evidence/T-073-T-084/mutate.py: 5,2,2,1,4,1,5 failed; control 55 passed", "probes artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py and probe_t084_billed_150_per_visit.py (output probe-run.txt): restore after class flip -> charge, restored True, pending 31000; 'Billed $150 per visit' with judge agree -> charge, pending 15000; 'Charge per visit $185' -> pending 49500", "grep -n except on reclassify.py (none)"],
112	 "verdict": "fail",
113	 "scores": {"no_rate_into_total_without_both_checks": 2, "code_check_strength": 2, "judge_gate": 4, "audit_trail": 3, "commit_scope": 1, "tests_kill_mutants": 5},
114	 "findings": [
115	  {"severity": "blocker", "title": "Restore after a rerun turns a current rate into a charge with neither check",
116	   "evidence": "app/backend/reclassify.py:102-104 (HEAD ec33bf0): restored = original == 'charge' and prior.get('previous_judge') is not None; if not restored skips _guard; carry_over reclassify.py:157-163 compares only text and value (line 160). Repro artifacts/review-evidence/T-073-T-084/probe_t084_sneak_and_restore.py -> 'RESTORE WITHOUT ANY CHECK -> charge restored= True pending total= 31000' after the rerun changed the sentence to 'Rate of $310 per visit.'",
117	   "why_it_matters": "D-042 requires code wording AND a judge re-check before a rate becomes a charge. The restore path uses a judge answer about the old sentence and skips the code check, so a figure the current code calls a rate enters the pending total. This breaks the brief's invariant, and the trigger (a classifier or lexicon change on rerun) is realistic.",
118	   "fix": "Allow the restore to skip the checks only if the rerun's code class still equals the class at demotion and the sentence is unchanged; otherwise re-run _guard. Compare the sentence or an excerpt hash in carry_over, not only text and cents.",
119	   "acceptance_test": "Demote, rerun with the flipped sentence, reclassify to charge with call=None: expect 422 (NO_CHARGE_WORDING or JUDGE_UNAVAILABLE), kind stays unclear, no reclassify event. Keep test_reclassify.py:80-87 passing for the unchanged-sentence restore."},
120	  {"severity": "blocker", "title": "Commit ec33bf0 silently deletes T-083's billing module, tests, route and API doc",
121	   "evidence": "git show --stat ec33bf0: 'app/backend/billing.py | 642 ----' and 'tests/unit/test_billing.py | 330 ----'; git ls-tree -r --name-only ec33bf0 | grep -i billing -> none, while f218263 has both; git show f218263:app/backend/api.py lines 497-498 (billing hook) replaced in ec33bf0 api.py; git show ec33bf0 -- memory/contracts/api.md removes the GET /api/cases/{token}/billing section; D-042 at memory/ORCHESTRATOR_DECISIONS.md:50 reinstates billing analysis",
122	   "why_it_matters": "The commit message describes only the reclassify feature. HEAD no longer serves the billing endpoint D-042 reinstates, and T-083's evidence (tests/unit/test_billing.py: 27 passed) cannot be reproduced at HEAD. Recoverable (files are on disk and in f218263), but not in any recorded decision.",
123	   "fix": "Restore billing.py, test_billing.py, the billing.add_routes hook and the api.md section in a commit under T-083, adding paths explicitly. If the removal was intended, record it in SCOPE_CUTS and ORCHESTRATOR_DECISIONS and update T-083 first. Do not rewrite history.",
124	   "acceptance_test": "git ls-tree -r --name-only HEAD | grep billing lists both files; tests/unit/test_billing.py passes at HEAD; GET /api/cases/{token}/billing returns 200 in a route test."},
125	  {"severity": "major", "title": "The code wording check accepts the rate phrase itself, so the judge is the only gate for 'Charge per visit $185'",
126	   "evidence": "app/backend/reclassify.py:24 _WORDING matches charges? and billed; probe-run.txt: 'wording(Charge per visit $185): Charge', 'wording(Billed $150 per visit): Billed', 'after judge agree: charge ... pending total cents: 15000' for 'Billed $150 per visit', and 'pending total cents = 49500' for the fixture rate; tests/unit/test_reclassify.py:108-116 (HEAD) asserts the rate reclassifies to charge on judge agreement",
127	   "why_it_matters": "The first independent gate is defeated by the sentence's own rate unit. D-042 is literally met, so this is a design weakness, not a written breach, but a $150-per-visit rate is summed as a billed charge on one LLM judge. If D-042 is read to exclude rate sentences, this becomes a blocker.",
128	   "fix": "Refuse the wording when the figure's sentence has a rate unit ('per', 'each', 'a visit', 'per unit', 'rate of') next to the figure. Keep the charge-wording check for statements of charge.",
129	   "acceptance_test": "charge_wording returns None and reclassify returns 422 NO_CHARGE_WORDING (judge not called) for 'Visit completed. Charge per visit $185.' and 'Visit completed. Billed $150 per visit.'; move the positive case at test_reclassify.py:108 to a sentence with no rate unit (e.g. 'Billed $185 for the visit.')."},
130	  {"severity": "minor", "title": "The reclassify audit row is stored with action 'edit'",
131	   "evidence": "app/backend/reclassify.py:22 AUDIT_ACTION = 'edit'; payload event 'reclassify' at reclassify.py:123; tests/unit/test_reclassify.py:215 asserts [e['action'] for e in ev] == ['edit']",
132	   "why_it_matters": "The audit event exists (AC met), but the action column reports a summary edit to anyone reading review_events directly.",
133	   "fix": "DB card adds 'reclassify' to the review_events CHECK (bump SCHEMA_VERSION per app/db/db.py:32), then flip the constant.",
134	   "acceptance_test": "GET /audit shows action 'reclassify' for the event; test_reclassify.py:215 asserts it."},
135	  {"severity": "minor", "title": "State change and audit row are separate writes (read from code, not reproduced)",
136	   "evidence": "app/backend/reclassify.py:120 (DB.update_item), :122 (review.batch_apply with its own BEGIN/COMMIT in db.py), :123 (_log INSERT)",
137	   "why_it_matters": "A failure after :120 leaves the item changed with no audit event, which the audit trail requirement does not allow.",
138	   "fix": "Write the change and the audit row in one transaction, as db.apply_review does.",
139	   "acceptance_test": "Inject a failure at _log and assert the item is unchanged."}
140	 ],
141	 "whats_right": [
142	  "Seven of seven scratch mutants of the reclassify guard are caught (judge gate, wording, negation, unsure accepted, audit, value, judge refusal as pass); artifacts/review-evidence/T-073-T-084/mutation-run.txt.",
143	  "Judge disagree, unsure or unavailable gives 422 with nothing changed and no event (tests/unit/test_reclassify.py:124-139).",
144	  "Demotion from charge to not-a-charge leaves the total unchanged, returns the item to pending and writes the audit (tests/unit/test_reclassify.py:59-70)."
145	 ],
146	 "questions_for_chris": [
147	  "Was removing app/backend/billing.py and tests/unit/test_billing.py in ec33bf0 an intended scope cut? If yes, it needs a SCOPE_CUTS entry and a D-042 update before T-083 closes; if no, it needs a restore commit (F2).",
148	  "Does D-042 let a rate sentence ('Charge per visit $185.') satisfy 'charged-amount wording'? My reading is no; the decision text does not say."
149	 ]}
150	```
151	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:32.356Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:39:32.364Z

**tool result**
````
1	---
2	name: t073-t084-review-patterns
3	description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording gate, commit deleted T-083 billing
4	metadata:
5	  type: project
6	---
7	
8	T-073 r1 (7724412): the narrowed guard (judge_guard.py) is right at the seam, but the production path still hides programmer bugs: `app/llm/audited.py:70` has its own `except Exception` that retries 3x and surfaces as JUDGE_UNAVAILABLE/NONE. The card's propagation test raises from a raw fake call one layer above, so it cannot see this. Also `judges._run` catches LLMFailed before the guard, so `error_class` is never recorded for the failure the AC names.
9	**Why:** a card's test proves the behaviour at the seam it fakes; the broad catch moved one layer down and the card's AC was still marked done.
10	**How to apply:** for any "narrow the except" card, run the real call path with the provider raising a plain RuntimeError (audited_call with complete_with_meta raising) and check llm_calls rows and the ladder. Do not accept a raw FakeCall as proof of propagation.
11	
12	T-084 r1 (ec33bf0): (a) restore (undo own demotion) skips both checks and reuses the judge answer for the OLD sentence; `carry_over` keys on figure text and cents only, so a rerun that flips the code class of the same figure lets a current rate become a charge with no check. (b) The code wording gate matches "Charge" in "Charge per visit $185." and "Billed" in "Billed $150 per visit", so the judge is the only gate; the test at test_reclassify.py:108-116 encodes the sneak as expected. (c) The commit deleted T-083's committed billing.py, test_billing.py, api billing hook and api.md section; the cards' commit list and the commit message did not say so.
13	**Why:** the gate tests cover each check alone; the bypass needs a rerun between two calls. Commit-level deletions are only visible in `git show --stat`.
14	**How to apply:** on any "skip checks when restored/previous" path, rerun the pipeline with a changed sentence before the restore and check the outcome. On any keyword gate, feed it the rate phrase the spec names. On every review, run `git show --stat <commit>` and grep for deletions of other cards' paths.
15	
16	Harness notes (this review): the brief's `-k "review or reclass"` selector collects zero tests from tests/unit/test_judge_guard.py, so name guard files explicitly. The working tree moved mid-review (reclassify.py and test_reclassify.py edited by another worker), so the review pinned HEAD with `git archive ec33bf0`. The review-write guard refused an Edit to my own T-084 file after I had written one unverified sentence ("the sample case is not affected"); I disclosed it in the reply instead of creating an -r2 file. Proof-read before the first Write, as in [[feedback_review_write_once]].
17	
18	Related: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes).
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:32.595Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md"
}
````

### User / tool · 2026-11-02T04:39:32.602Z

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
12	**How to apply:** before the first Write of a review, grep every cited line number and re-check each "checked and fine" claim against a command you actually ran. If a correction is needed later, write a new suffixed file (`-r3`) and say so in the reply, not a silent overwrite. Do not try to get around the guard with shell writes.
13	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:35.149Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && echo \"---HEAD\" && git rev-parse HEAD && echo \"---status\" && git status --short | head -40 && echo \"---show c8a9874 stat\" && git show --stat c8a9874 | head -60 && echo \"---show e2b4e3f stat\" && git show --stat e2b4e3f | head -40",
 "description": "Show git log, HEAD, status, and the two commits' stats"
}
````

### User / tool · 2026-11-02T04:39:35.364Z

**tool result**
````
bc12d44 fix(frontend): side-by-side pane floats over the right margin, flag button in the pane, Enter selects, one record heading (T-046 r2)
c8a9874 fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
d3130e3 harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
55300e9 fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
49c4600 memory: T-091 speaker attribution v2 fails fresh adversary; stays cut (D-040)
e2b4e3f fix: restore T-083 billing deleted by ec33bf0
865b186 feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
---HEAD
bc12d4404d1cbd53e08583073ccfd2aaa205be92
---status
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
MM .claude/agent-memory/qa/MEMORY.md
D  .claude/agent-memory/qa/project_judge_controls.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/backend/rejudge.py
 M app/backend/trace.py
 M app/db/db.py
 M app/db/schema.sql
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
 M board/cards/T-059.md
 M board/cards/T-060.md
 M board/cards/T-061.md
 M board/cards/T-063.md
 M board/cards/T-064.md
 M board/cards/T-065.md
 M board/cards/T-066.md
---show c8a9874 stat
commit c8a9874e62124d4d329158bdbd1d98c9b65317a2
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:38:59 2026 -0600

    fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/judge_guard.py     |  17 ++++-
 app/backend/reclassify.py      |  41 ++++++++++--
 app/llm/audited.py             |  31 +++++++--
 tests/unit/test_audited.py     |  40 ++++++++++++
 tests/unit/test_judge_guard.py |  68 ++++++++++++++++++++
 tests/unit/test_reclassify.py  | 141 ++++++++++++++++++++++++++++++++++++-----
 6 files changed, 311 insertions(+), 27 deletions(-)
---show e2b4e3f stat
commit e2b4e3f42001a2cc5905756de8b2a5ee225a4040
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:34:06 2026 -0600

    fix: restore T-083 billing deleted by ec33bf0
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py         |   2 +
 app/backend/billing.py     | 642 +++++++++++++++++++++++++++++++++++++++++++++
 tests/unit/test_billing.py | 330 +++++++++++++++++++++++
 3 files changed, 974 insertions(+)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:35.543Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-073 && echo ===== && python3 tools/board.py show T-084",
 "description": "Show board cards T-073 and T-084"
}
````

### User / tool · 2026-11-02T04:39:35.878Z

**tool result**
````
---
id: "T-073"
title: "Narrow the broad except in review.py:83 judge path (keep error class, log reason)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:46:15Z"
updated_at: "2026-11-02T04:39:23Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:33:32Z"
rounds: 1
commits: ["7724412", "c8a9874"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-073-staff-engineer.md", "at": "2026-11-02T04:33:32Z"}
ac:
  - {"n": 1, "text": "review.py catches only expected judge errors; others propagate or are recorded with their class; unit test for both", "done": true, "evidence": "tests/unit/test_audited.py: RuntimeError/TypeError/KeyError/AttributeError from provider or validate propagate after 1 attempt and 1 llm_calls row; Timeout/Connection errors still retried; tests/unit/test_judge_guard.py (run as a file, not via -k): bug through real audited_call + guard + apply_review raises and saves nothing; LLMFailed / LLMFailedFixtureMiss / FixtureMissing / LLMError each give ladder.judge.error_class = own class name; tests/unit 1417 pass"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:25:25Z backend: AC 1 checked: tests/unit/test_judge_guard.py (10 tests) + test_review_rules.py::test_expected_judge_exception_on_edit_is_judge_unavailable_never_supported: LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class; RuntimeError/KeyError/AttributeError propagate and save nothing
- 2026-11-02T04:25:25Z backend: moved in_progress -> in_review
- 2026-11-02T04:25:29Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:33:32Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-073-staff-engineer.md; round 1; findings:
    - [major] A programmer bug in the real judge call is retried 3x and hidden as JUDGE_UNAVAILABLE (broad except one layer down) — fix: Narrow audited.py:70 to provider/LLM errors (P.LLMError and our own codes); let other exceptions propagate without retry. app/llm and judges.py are outside this card's stated scope, so raise it as its own backend card.
    - [major] error_class is not recorded for LLMFailed, which the AC names explicitly — fix: Make judges._run return the class (e.g. 'LLMFailed') or re-raise LLMFailed to the guard, so every expected failure lands in ladder.judge.error_class. If deferred, correct the AC evidence now.
    - [minor] The brief's -k selector collects zero tests from test_judge_guard.py — fix: Add 'or guard' to the -k expression, or list tests/unit/test_judge_guard.py explicitly.
- 2026-11-02T04:33:32Z backend: claimed
- 2026-11-02T04:39:16Z backend: AC 1 checked: tests/unit/test_audited.py: RuntimeError/TypeError/KeyError/AttributeError from provider or validate propagate after 1 attempt and 1 llm_calls row; Timeout/Connection errors still retried; tests/unit/test_judge_guard.py (run as a file, not via -k): bug through real audited_call + guard + apply_review raises and saves nothing; LLMFailed / LLMFailedFixtureMiss / FixtureMissing / LLMError each give ladder.judge.error_class = own class name; tests/unit 1417 pass
- 2026-11-02T04:39:16Z backend: moved in_progress -> in_review
- 2026-11-02T04:39:23Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: audited.py retries only P.LLMError, TimeoutError, ConnectionError and validate ValueError; any other exception is logged as one llm_calls row (class name) and re-raised, no retry. LLMFailed carries last_error. judge_guard.guarded wraps the judge's call to note an expected error's class, so ladder.judge.error_class is set even though judges._run swallows LLMFailed (judges.py untouched, T-094). How verified: .venv/bin/python -m pytest -q tests/unit/test_audited.py tests/unit/test_judge_guard.py tests/unit/test_reclassify.py (84 pass), full tests/unit 1417 pass + 1 unrelated e2e-contract failure; include tests/unit/test_judge_guard.py explicitly in any -k selector. Left: judges._run still returns reason NONE for LLMFailed (class is in the ladder, not the reason); reviewer question on JUDGE_UNAVAILABLE vs visible error for bugs: bugs now propagate as errors. Surprised me: provider.py ValueErrors in record mode also now propagate (config bugs), which is intended.

=====
---
id: "T-084"
title: "Guarded charge reclassification by the paralegal"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:39:24Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:33:32Z"
rounds: 1
commits: ["ec33bf0", "c8a9874", "e2b4e3f"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-084-staff-engineer.md", "at": "2026-11-02T04:33:32Z"}
ac:
  - {"n": 1, "text": "Paralegal can reclassify charge<->not-a-charge; rate->charge only if code finds charged-amount wording in the excerpt AND judge re-check passes, else 422 with reason; audit event; unit tests", "done": true, "evidence": "tests/unit/test_reclassify.py (46 tests): restore after rerun re-runs both checks (rate flip -> 422 NO_CHARGE_WORDING, sentence change -> judge needed, unchanged rerun still no judge); 'Charge per visit $185' and 'Billed $150 per visit' refused 422 before the judge; 17 rate-cue strings; 5 plain-charge strings pass; mutant (restore w/o rerun check) fails 2 tests; full tests/unit 1417 pass (1 unrelated e2e-contract failure from frontend sbs ids)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z backend: claimed
- 2026-11-02T04:25:25Z backend: AC 1 checked: tests/unit/test_reclassify.py (18 tests): charge->not-charge, restore, rate+wording+judge agree -> charge, no wording 422 (judge not called), judge disagree/unsure/unavailable 422, injection/no value, audit event, rerun keeps class, HTTP route
- 2026-11-02T04:25:25Z backend: FOR FRONTEND/UX: POST /api/cases/{token}/items/{id}/reclassify body {to:'charge'|'not_a_charge', note?}. Show 'Not a charge' on a charge row and 'This is a charge' on a rate/estimate/unclear row. 200 returns amount (kind=class, patch row), totals, review, reclassified; item returns to pending, so she must accept again. 422 reclassify_refused: show error.message (fixed plain sentence) and detail.reason/check; JUDGE_UNAVAILABLE = offer 'Try again'. Demo mode has no recorded judge answer so rate->charge is always refused there. Item stepper: classified_by reads 'reviewer:reclassified', ladder.reclassification has from/to/wording/note. Contract: api.md section 'POST .../reclassify'.
- 2026-11-02T04:25:25Z backend: NEEDS DB CARD: review_events.action CHECK has no 'reclassify', so the audit row is written as action 'edit' with after.event='reclassify' (constant reclassify.AUDIT_ACTION). When db adds the action, flip the constant. Also trace.py amount_class step text says 'A billing phrase ... labels this figure a charge' for reclassified charges; owner of trace.py may want a reviewer-set variant.
- 2026-11-02T04:25:25Z backend: moved in_progress -> in_review
- 2026-11-02T04:25:29Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:33:32Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-084-staff-engineer.md; round 1; findings:
    - [blocker] Restore after a rerun turns a current rate into a charge with neither check — fix: Allow the restore to skip the checks only if the rerun's code class still equals the class at demotion and the sentence is unchanged; otherwise re-run _guard. Compare the sentence or an excerpt hash in carry_over, not only text and cents.
    - [blocker] Commit ec33bf0 silently deletes T-083's billing module, tests, route and API doc — fix: Restore billing.py, test_billing.py, the billing.add_routes hook and the api.md section in a commit under T-083, adding paths explicitly. If the removal was intended, record it in SCOPE_CUTS and ORCHESTRATOR_DECISIONS and update T-083 first. Do not rewrite history.
    - [major] The code wording check accepts the rate phrase itself, so the judge is the only gate for 'Charge per visit $185' — fix: Refuse the wording when the figure's sentence has a rate unit ('per', 'each', 'a visit', 'per unit', 'rate of') next to the figure. Keep the charge-wording check for statements of charge.
    - [minor] The reclassify audit row is stored with action 'edit' — fix: DB card adds 'reclassify' to the review_events CHECK (bump SCHEMA_VERSION per app/db/db.py:32), then flip the constant.
    - [minor] State change and audit row are separate writes (read from code, not reproduced) — fix: Write the change and the audit row in one transaction, as db.apply_review does.
- 2026-11-02T04:33:32Z backend: claimed
- 2026-11-02T04:34:13Z backend: ec33bf0 had deleted T-083 billing from git; restored in e2b4e3f via fresh temp index from HEAD. Now fixing r2 findings.
- 2026-11-02T04:39:15Z backend: AC 1 checked: tests/unit/test_reclassify.py (46 tests): restore after rerun re-runs both checks (rate flip -> 422 NO_CHARGE_WORDING, sentence change -> judge needed, unchanged rerun still no judge); 'Charge per visit $185' and 'Billed $150 per visit' refused 422 before the judge; 17 rate-cue strings; 5 plain-charge strings pass; mutant (restore w/o rerun check) fails 2 tests; full tests/unit 1417 pass (1 unrelated e2e-contract failure from frontend sbs ids)
- 2026-11-02T04:39:16Z backend: moved in_progress -> in_review
- 2026-11-02T04:39:24Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: T-083 billing restored to HEAD (e2b4e3f, temp index from HEAD). reclassify.py: restore skips both checks only if no rerun changed the code class or the sentence (excerpt_sha + rerun marker via carry_over), else _guard runs and 422 leaves the item unchanged at needs_review; a promoted charge is dropped if its sentence changes on rerun; rate cues (per/each/every/rate/ /visit / x N / a visit / daily rate) are decisive in charge_wording; AUDIT_ACTION now 'reclassify' (T-095, F4). How verified: .venv/bin/python -m pytest -q tests/unit/test_reclassify.py (46 pass), full tests/unit 1417 pass, 1 fail test_e2e_contract (sbs-show-flag ids from frontend, not mine); mutant check on restore. Left: F5 (item change + audit row in one transaction) not done. Surprised me: sample case a2 'Charge per visit $185' is now a code refusal, so the route test asserts NO_CHARGE_WORDING; JUDGE_UNAVAILABLE route path is covered by unit tests.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:40.676Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo \"SP=$SP\" && git merge-base --is-ancestor c8a9874 HEAD && echo \"c8a9874 is ancestor of HEAD\" && git merge-base --is-ancestor e2b4e3f HEAD && echo \"e2b4e3f is ancestor of HEAD\" && echo \"--- files changed c8a9874..HEAD\" && git diff --stat c8a9874 HEAD | tail -30 && echo \"--- billing files in HEAD\" && git ls-tree -r --name-only HEAD | grep -i billing && echo \"--- api.py billing hook at HEAD\" && git show HEAD:app/backend/api.py | grep -n -i \"billing\" && echo \"--- diff of in-scope files c8a9874..HEAD\" && git diff --stat c8a9874 HEAD -- app/backend/judge_guard.py app/backend/reclassify.py app/llm/audited.py tests/unit/test_audited.py tests/unit/test_judge_guard.py tests/unit/test_reclassify.py app/backend/api.py app/backend/billing.py tests/unit/test_billing.py app/backend/judges.py app/backend/review.py; echo \"exit=$?\"",
 "description": "Check ancestry, billing files at HEAD, and in-scope diffs since c8a9874"
}
````

### User / tool · 2026-11-02T04:39:40.910Z

**tool result**
````
SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
c8a9874 is ancestor of HEAD
e2b4e3f is ancestor of HEAD
--- files changed c8a9874..HEAD
 app/frontend/sidebyside.css                        |  18 ++++----
 app/frontend/sidebyside.js                         |  37 ++++++++++++----
 artifacts/screenshots/sidebyside-1280-empty.png    | Bin 177415 -> 188003 bytes
 artifacts/screenshots/sidebyside-1280-entry8.png   | Bin 185982 -> 184407 bytes
 artifacts/screenshots/sidebyside-1280-gap-flag.png | Bin 183006 -> 193712 bytes
 .../sidebyside-1440-gap-flag-button.png            | Bin 0 -> 181249 bytes
 .../screenshots/sidebyside-1440-gap-flag-click.png | Bin 0 -> 195830 bytes
 artifacts/screenshots/sidebyside-375-modal.png     | Bin 75980 -> 75989 bytes
 tests/e2e/test_side_by_side.py                     |  47 +++++++++++++++++++++
 9 files changed, 86 insertions(+), 16 deletions(-)
--- billing files in HEAD
app/backend/billing.py
tests/unit/test_billing.py
--- api.py billing hook at HEAD
509:    from app.backend import billing
510:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
--- diff of in-scope files c8a9874..HEAD
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:43.404Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && git worktree add --detach \"$SP/wt\" HEAD 2>&1 && cd \"$SP/wt\" && git rev-parse HEAD && git status --short | head && ls app/backend | head -50 && ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python",
 "description": "Create a detached worktree of HEAD in scratchpad"
}
````

### User / tool · 2026-11-02T04:39:43.482Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git worktree` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:47.218Z

The board guard refuses `git worktree` from the project, so I'll pin HEAD with `git archive` into an empty scratchpad directory, the same method the earlier reviews used.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:49.111Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SP/head-bc12d44\" && cd /Users/arsis/zlayt-pm-project && git archive bc12d44 | tar -x -C \"$SP/head-bc12d44\" && cd \"$SP/head-bc12d44\" && ls && echo \"---billing\" && ls app/backend | grep -i -E \"billing|reclass|judge|audited\" ; ls tests/unit | grep -E \"billing|reclass|judge_guard|review_rules|audited\"; echo \"--- pytest config\"; ls pytest.ini setup.cfg pyproject.toml conftest.py tests/conftest.py 2>/dev/null; cat pytest.ini 2>/dev/null | head -20",
 "description": "Extract HEAD archive into scratchpad and list relevant files"
}
````

### User / tool · 2026-11-02T04:39:50.175Z

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
---billing
billing.py
judge_guard.py
judges.py
reclassify.py
rejudge.py
test_audited.py
test_billing.py
test_judge_guard.py
test_reclassify.py
test_review_rules.py
--- pytest config
tests/conftest.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:52.428Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py 2>&1 | tail -30; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run the four required test files against the HEAD archive"
}
````

### User / tool · 2026-11-02T04:39:55.451Z

**tool result**
````
app/backend/reclassify.py:90: IntegrityError
__________________________________ test_route __________________________________

tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-2877/test_route0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x1085457c0>

    def test_route(tmp_path, monkeypatch):
        monkeypatch.setenv("LLM_BACKEND", "fixture")
        c = TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
        tok = c.post("/api/cases", json={"sample": True}).json()["token"]
        assert c.post(f"/api/cases/{tok}/items/a1/reclassify", json={}).status_code == 400
        r = c.post(f"/api/cases/{tok}/items/a1/reclassify", json={"to": "not_a_charge"})
>       assert r.status_code == 200 and r.json()["amount"]["kind"] == "unclear" and r.json()["reclassified"]["from"] == "charge"
E       assert (500 == 200)
E        +  where 500 = <Response [500 Internal Server Error]>.status_code

tests/unit/test_reclassify.py:314: AssertionError
------------------------------ Captured log call -------------------------------
ERROR    zlayt.api:api.py:184 unhandled IntegrityError
=========================== short test summary info ============================
FAILED tests/unit/test_reclassify.py::test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited
FAILED tests/unit/test_reclassify.py::test_undoing_her_own_demotion_restores_the_code_class_without_a_judge
FAILED tests/unit/test_reclassify.py::test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge
FAILED tests/unit/test_reclassify.py::test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again
FAILED tests/unit/test_reclassify.py::test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again
FAILED tests/unit/test_reclassify.py::test_restore_after_an_unchanged_rerun_still_needs_no_judge
FAILED tests/unit/test_reclassify.py::test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence
FAILED tests/unit/test_reclassify.py::test_a_rerun_keeps_her_reclassification
FAILED tests/unit/test_reclassify.py::test_route - assert (500 == 200)
9 failed, 111 passed in 2.58s
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:57.992Z

Nine reclassify tests fail on the HEAD archive with an IntegrityError. I'll check whether the committed schema accepts the `reclassify` action.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:00.032Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && echo \"--- AUDIT_ACTION at HEAD\" && grep -n \"AUDIT_ACTION\" app/backend/reclassify.py && echo \"--- action CHECK in HEAD schema\" && grep -n -i \"check\" app/db/schema.sql | grep -i action; grep -n -i \"review_events\" -A12 app/db/schema.sql | head -30; echo \"--- SCHEMA_VERSION HEAD\" && grep -n \"SCHEMA_VERSION\" app/db/db.py | head -5; echo \"--- reclassify.py:80-95 HEAD\" && sed -n 80,95p app/backend/reclassify.py",
 "description": "Inspect HEAD audit action constant, schema CHECK, and failing line"
}
````

### User / tool · 2026-11-02T04:40:00.150Z

**tool result**
````
--- AUDIT_ACTION at HEAD
27:AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
91:                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))
--- action CHECK in HEAD schema
57:  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
55:CREATE TABLE IF NOT EXISTS review_events (
56-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
57-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
58-  before_json TEXT, after_json TEXT, at REAL
59-);
60-CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
61-CREATE INDEX IF NOT EXISTS ix_entries_case ON entries(case_id);
62-CREATE INDEX IF NOT EXISTS ix_amounts_case ON amounts(case_id);
63-CREATE INDEX IF NOT EXISTS ix_flags_case ON flags(case_id);
64-CREATE INDEX IF NOT EXISTS ix_calls_case ON llm_calls(case_id);
65:CREATE INDEX IF NOT EXISTS ix_events_case ON review_events(case_id);
--- SCHEMA_VERSION HEAD
32:SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
47:        if has_tables and version != SCHEMA_VERSION:
51:            log.warning("database schema version %s != %s: old file deleted and rebuilt", version, SCHEMA_VERSION)
58:    conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
--- reclassify.py:80-95 HEAD
def _refuse(reason: str, **detail):
    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
                                                          **detail}, REFUSALS[reason])


def _sha(text) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def _log(conn, case_id, item_id, before, after, t):
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))


def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = review._now(now)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:00.724Z

**tool call — Bash**
````
{
 "command": "echo \"--- git log for schema.sql and db.py\" && git log --oneline -4 -- app/db/schema.sql app/db/db.py && echo \"--- working tree diff of schema (uncommitted)\" && git diff -- app/db/schema.sql | head -40 && echo \"--- working tree AUDIT_ACTION\" && grep -n AUDIT_ACTION app/backend/reclassify.py",
 "description": "Compare committed and working-tree schema and audit constant"
}
````

### User / tool · 2026-11-02T04:40:00.872Z

**tool result**
````
--- git log for schema.sql and db.py
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
c61e84f fix(db): bump schema version to 3, real v2 rebuild test (T-062 r2)
864676f fix(db): delete old-schema database at rebuild instead of keeping a copy (T-050, T-040 security r2)
--- working tree diff of schema (uncommitted)
diff --git a/app/db/schema.sql b/app/db/schema.sql
index 5037c31..c72eb0f 100644
--- a/app/db/schema.sql
+++ b/app/db/schema.sql
@@ -54,7 +54,7 @@ CREATE TABLE IF NOT EXISTS llm_calls (
 );
 CREATE TABLE IF NOT EXISTS review_events (
   id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
+  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry','reclassify','rejudge')),
   before_json TEXT, after_json TEXT, at REAL
 );
 CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
--- working tree AUDIT_ACTION
27:AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
91:                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:04.385Z

**tool call — Bash**
````
{
 "command": "echo \"--- commits touching the review_events CHECK\" && git log --oneline -S\"'reclassify','rejudge'\" -- app/db/schema.sql && git log --oneline -S\"'manual_entry'\" -- app/db/schema.sql && echo \"--- 031a708 schema diff\" && git show 031a708 -- app/db/schema.sql | head -30 && echo \"--- 2fca530 touches of db\" && git show --stat 2fca530 | head -30 && git show 2fca530 -- app/db/schema.sql app/db/db.py | head -60",
 "description": "Trace which commit added or reverted the reclassify audit action"
}
````

### User / tool · 2026-11-02T04:40:04.654Z

**tool result**
````
--- commits touching the review_events CHECK
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
5f8858f feat(db): log-only review actions not_duplicate, manual_entry; schema version rebuild (T-062)
--- 031a708 schema diff
commit 031a7088d0740f4a045f62213997dc648d39d5a8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:30:42 2026 -0600

    feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/db/schema.sql b/app/db/schema.sql
index 5037c31..c72eb0f 100644
--- a/app/db/schema.sql
+++ b/app/db/schema.sql
@@ -54,7 +54,7 @@ CREATE TABLE IF NOT EXISTS llm_calls (
 );
 CREATE TABLE IF NOT EXISTS review_events (
   id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
-  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry')),
+  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry','reclassify','rejudge')),
   before_json TEXT, after_json TEXT, at REAL
 );
 CREATE INDEX IF NOT EXISTS ix_records_case ON records(case_id);
--- 2fca530 touches of db
commit 2fca530363a43f5e886a441234ba2cfc7a6725ea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:03 2026 -0600

    feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
    
    Hidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page
    (pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd
    locally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at
    needs_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/api.py                   |  26 +++--
 app/backend/confidence.py            |   2 +-
 app/backend/pdf_checks.py            | 125 +++++++++++++++++++++++
 app/backend/pdf_hidden.py            | 188 +++++++++++++++++++++++++++++++++++
 app/backend/pdf_ocr.py               | 178 +++++++++++++++++++++++++++++++++
 app/backend/pdf_routes.py            |  25 +++++
 app/backend/pdf_text.py              |  41 ++++++--
 app/backend/pipeline.py              |   2 +
 app/backend/present.py               |   6 +-
 app/backend/reclassify.py            |   2 +-
 app/backend/rejudge.py               |   8 --
 app/backend/trace.py                 |  14 ++-
 app/backend/why.py                   |   1 +
 app/db/db.py                         |  52 +---------
 app/db/schema.sql                    |   2 +-
 evals/run.py                         |  88 ++++------------
 memory/contracts/api.md              |  23 +++++
commit 2fca530363a43f5e886a441234ba2cfc7a6725ea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:03 2026 -0600

    feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
    
    Hidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page
    (pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd
    locally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at
    needs_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/db/db.py b/app/db/db.py
index 5bc2d33..f95bcad 100644
--- a/app/db/db.py
+++ b/app/db/db.py
@@ -9,7 +9,6 @@ import hashlib
 import json
 import logging
 import os
-import re
 import secrets
 import sqlite3
 import time
@@ -30,8 +29,7 @@ def init(path: str = ":memory:"):
     return connect(path)
 
 
-SCHEMA_VERSION = 4          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062); 4 = += reclassify, rejudge (T-095; v3 -> v4 is an in-place migration)
-AUDIT_ONLY_ACTIONS = ("reclassify", "rejudge")          # logged by log_event(); never change review_status, so apply_review() refuses them
+SCHEMA_VERSION = 3          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062)
 log = logging.getLogger("zlayt.db")
 
 
@@ -46,7 +44,7 @@ def connect(path: str):
             has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
         finally:
             probe.close()
-        if has_tables and version != SCHEMA_VERSION and version != 3:
+        if has_tables and version != SCHEMA_VERSION:
             for ext in ("", "-wal", "-shm", "-journal"):          # deleted, not kept: an old file would hold pasted text past the 24 h purge
                 if os.path.exists(path + ext):
                     os.remove(path + ext)
@@ -56,45 +54,11 @@ def connect(path: str):
     conn.execute("PRAGMA secure_delete=ON")
     conn.execute("PRAGMA foreign_keys=ON")
     with open(_SCHEMA, encoding="utf-8") as f:
-        schema = f.read()
-    if path != ":memory:" and conn.execute("PRAGMA user_version").fetchone()[0] == 3 and \
-            conn.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='review_events'").fetchone():
-        _migrate_v3_to_v4(conn, schema)
-    conn.executescript(schema)
+        conn.executescript(f.read())
     conn.execute(f"PRAGMA user_version={SCHEMA_VERSION}")
     return conn
 
 
-def _migrate_v3_to_v4(conn, schema: str) -> None:
-    """v3 -> v4 in place, keeping every row (T-095). SQLite cannot alter a CHECK, so review_events is rebuilt inside one transaction:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:11.272Z

Commit 2fca530 (another card, committed 36 seconds after 031a708) reverted the T-095 schema and migration that the reclassify audit depends on. I'll run the brief's command in the working tree and the HEAD archive side by side, and check the reclassify write order.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:11.916Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD=$(git rev-parse --short HEAD)\" && .venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py 2>&1 | tail -8; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run the brief's four-file pytest command in the project working tree"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:13.760Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && .venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py 2>/dev/null | tail -2; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py -p no:cacheprovider 2>&1 | tail -3; echo \"--- reclassify route body HEAD (lines 96-140)\"; sed -n 96,140p app/backend/reclassify.py",
 "description": "Run the four-file command on the HEAD archive and read the reclassify write order"
}
````

### User / tool · 2026-11-02T04:40:15.106Z

**tool result**
````
HEAD=bc12d44
........................................................................ [ 60%]
................................................                         [100%]
120 passed in 2.76s
exit=0
````

### User / tool · 2026-11-02T04:40:18.413Z

**tool result**
````
FAILED tests/unit/test_reclassify.py::test_a_rerun_keeps_her_reclassification
FAILED tests/unit/test_reclassify.py::test_route - assert (500 == 200)
9 failed, 111 passed in 2.82s
--- reclassify route body HEAD (lines 96-140)
    to = (body or {}).get("to")
    if to not in TARGETS:
        raise review.ReviewError(400, "bad_request", message='Send "to": "charge" or "not_a_charge".')
    note = (body or {}).get("note")
    if note is not None and not isinstance(note, str):
        raise review.ReviewError(400, "bad_request", message="The note must be text.")
    kind, row = review._item(conn, case_id, item_id)
    if kind != "amount":
        raise review._bad("Only a dollar figure can be reclassified.")
    if row["state"] == "rejected":
        raise review.ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    old_kind = row["kind"]
    if (to == "charge") == (old_kind == "charge"):                         # already there: nothing to do, nothing logged
        return _result(conn, case_id, item_id, None, [])
    lad = dict(row.get("ladder") or {"item_id": item_id})
    prior = lad.get("reclassification") or {}
    original = prior.get("original_kind", old_kind)
    rec = next((r for r in store.load_records(conn, case_id) if r["id"] == (row["record_ids"] or [None])[0]), None)
    wording, judge_res, restored = None, None, False
    if to == "charge":
        restored = _may_restore(row, prior, original)
        if not restored:
            wording, judge_res = _guard(row, rec, call)
    new_kind = "charge" if to == "charge" else NOT_A_CHARGE_KIND
    cc = dict(lad.get("code_checks") or {})
    cc.update(classified_by="reviewer:reclassified", **({"charge_wording": wording} if wording else {}))
    if to == "charge":
        jd = prior["previous_judge"] if restored else judge_res["judge"]
        ladder_verdict = judges.to_ladder("j2", (jd or {}).get("verdict", "unavailable")) if jd else "unavailable"
    else:
        jd, ladder_verdict = None, None
    state, reasons = confidence.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": ladder_verdict},
                                              {"injection": bool(rec and rec.get("injection_tag")), "amount_class": new_kind})
    lad.update(judge=jd, code_checks=cc, state=state, reclassification={
        "from": old_kind, "to": new_kind, "at": store.iso(t), "by": "reviewer", "original_kind": original, "wording": wording, "restored": restored,
        "excerpt_sha": _sha(row["excerpt"]),
        "note": (note or "").strip()[:500] or None,
        "previous_judge": lad.get("judge") if to == "not_a_charge" else prior.get("previous_judge")})
    before = {"kind": old_kind, "review_status": row["review_status"], "state": row["state"]}
    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
    if row["review_status"] != "pending":                                  # her earlier decision was about the old meaning
        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
                                          "judge_verdict": (jd or {}).get("verdict"), "judge_call_id": (jd or {}).get("call_id"), "restored": restored,
                                          "note": lad["reclassification"]["note"]}, t)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:31.402Z

The working tree passes 120 tests only because the schema fix is uncommitted, and HEAD fails 9. Next I'll pull the rest of the evidence: what 2fca530 changed in the reclassify and rejudge files, the T-095 card, and whether the restored billing files match f218263.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:32.628Z

**tool call — Bash**
````
{
 "command": "echo \"--- 2fca530 full stat tail\" && git show --stat 2fca530 | tail -12 && echo \"--- 2fca530 reclassify/rejudge/trace hunks\" && git show 2fca530 -- app/backend/reclassify.py app/backend/rejudge.py | head -60 && echo \"--- T-095 card\" && python3 tools/board.py show T-095 2>&1 | head -30 && echo \"--- billing diff vs f218263 (expect empty)\" && git diff f218263 HEAD -- app/backend/billing.py tests/unit/test_billing.py | wc -l && git diff f218263 HEAD -- app/backend/api.py | head -30 && echo \"--- api.md billing section at HEAD\" && grep -n -i \"billing\" memory/contracts/api.md | head",
 "description": "Inspect the 2fca530 hunks, the T-095 card, and billing restore parity"
}
````

### User / tool · 2026-11-02T04:40:32.881Z

**tool result**
````
--- 2fca530 full stat tail
 requirements.txt                     |   1 +
 tests/unit/_pdf_raw.py               |  68 +++++++++++++
 tests/unit/test_db.py                |  77 +-------------
 tests/unit/test_eval_runner.py       | 170 +------------------------------
 tests/unit/test_pdf_checks_api.py    | 128 ++++++++++++++++++++++++
 tests/unit/test_pdf_hidden.py        |  97 ++++++++++++++++++
 tests/unit/test_pdf_ocr.py           | 152 ++++++++++++++++++++++++++++
 tests/unit/test_provider.py          |   7 +-
 tests/unit/test_provider_backends.py |   3 +
 tests/unit/test_reclassify.py        |   2 +-
 tests/unit/test_trace.py             |  16 ---
 28 files changed, 1096 insertions(+), 408 deletions(-)
--- 2fca530 reclassify/rejudge/trace hunks
commit 2fca530363a43f5e886a441234ba2cfc7a6725ea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:03 2026 -0600

    feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
    
    Hidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page
    (pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd
    locally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at
    needs_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/reclassify.py b/app/backend/reclassify.py
index 09ca7be..687def0 100644
--- a/app/backend/reclassify.py
+++ b/app/backend/reclassify.py
@@ -19,7 +19,7 @@ from app.db import db as DB
 
 TARGETS = ("charge", "not_a_charge")
 NOT_A_CHARGE_KIND = "unclear"
-AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
+AUDIT_ACTION = "edit"      # review_events.action CHECK has no 'reclassify' yet (db card); the payload's `event` says what it was
 _BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
 _WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
 _NEGATED = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)
diff --git a/app/backend/rejudge.py b/app/backend/rejudge.py
index 31fc5de..086e225 100644
--- a/app/backend/rejudge.py
+++ b/app/backend/rejudge.py
@@ -53,12 +53,6 @@ def recompose(row: dict, ladder_verdict: str):
     return ("needs_review" if reasons else "verified"), reasons
 
 
-def _log(conn, case_id, row, jid, call_id, verdict, state, t):
-    """One audit row per asked item (review_events action 'rejudge'); review_status is never touched."""
-    DB.log_event(conn, case_id, row["id"], "rejudge", {"state": row["state"], "review_status": row["review_status"]},
-                 {"event": "rejudge", "judge": jid, "verdict": verdict, "state": state, "call_id": call_id}, t)
-
-
 def rejudge(conn, case_id: str, call, now: float = None) -> dict:
     t = time.time() if now is None else now
     case = DB.get_case(conn, case_id)
@@ -76,7 +70,6 @@ def rejudge(conn, case_id: str, call, now: float = None) -> dict:
         base = {"item_id": row["id"], "kind": tg["kind"], "judge": jid, "review_status": row["review_status"]}
         if ladder_verdict == "unavailable":
             DB.update_item(conn, row["id"], now=t, case=case_id, ladder=lad)
-            _log(conn, case_id, row, jid, call_id, "unavailable", row["state"], t)
             still.append(dict(base, verdict="unavailable"))
             continue
         lad["judge"] = {**(lad.get("judge") or {}), "model": judges.judge_model(), "prompt_version": trace.JUDGE_PROMPT[jid], "call_id": call_id,
@@ -84,7 +77,6 @@ def rejudge(conn, case_id: str, call, now: float = None) -> dict:
         state, reasons = recompose(row, ladder_verdict)
         lad["state"] = state
         DB.update_item(conn, row["id"], now=t, case=case_id, state=state, state_reasons_json=reasons, ladder=lad)
-        _log(conn, case_id, row, jid, call_id, ladder_verdict, state, t)
         done.append(dict(base, verdict=ladder_verdict, state=state, state_reasons=reasons))
     gate = next(s for s in trace.case_trace(conn, case_id)["steps"] if s["id"] == "export_gate")
     return {"token": case_id, "asked": len(targets), "rejudged": done, "still_unavailable": still,
--- T-095 card
---
id: "T-095"
title: "review_events CHECK: add reclassify and rejudge actions (migrate existing edit+event rows)"
milestone: "M3"
role: "db"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:25:37Z"
updated_at: "2026-11-02T04:30:57Z"
claimed_by: "db"
claimed_at: "2026-11-02T04:25:39Z"
rounds: 0
commits: ["031a708"]
reviews: []
ac:
  - {"n": 1, "text": "app/db/schema.sql review_events action CHECK includes reclassify and rejudge; user_version bumped with a migration that keeps existing rows; review.py/reclassify and rejudge write their own action; unit tests", "done": true, "evidence": "tests/unit/test_db.py::test_v3_to_v4_migrates_in_place_keeping_rows_and_converts_reclassify_edits, ::test_v3_migration_rolls_back_if_it_fails, ::test_log_event_only_writes_audit_actions...; test_reclassify.py (action reclassify); test_trace.py::test_rejudge_writes_one_rejudge_event...; full tests/unit 1350 passed (1 flaky spanish test passes on rerun)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:25:39Z db: claimed
- 2026-11-02T04:25:46Z orchestrator: assigned: db
- 2026-11-02T04:25:46Z orchestrator: Queued: 12-subagent concurrency limit reached; starts when a slot frees.
- 2026-11-02T04:30:52Z db: AC 1 checked: tests/unit/test_db.py::test_v3_to_v4_migrates_in_place_keeping_rows_and_converts_reclassify_edits, ::test_v3_migration_rolls_back_if_it_fails, ::test_log_event_only_writes_audit_actions...; test_reclassify.py (action reclassify); test_trace.py::test_rejudge_writes_one_rejudge_event...; full tests/unit 1350 passed (1 flaky spanish test passes on rerun)
- 2026-11-02T04:30:52Z db: moved in_progress -> in_review
- 2026-11-02T04:30:57Z orchestrator: review dispatched: staff-engineer-reviewer

--- billing diff vs f218263 (expect empty)
       0
diff --git a/app/backend/api.py b/app/backend/api.py
index 9547667..021d5f8 100644
--- a/app/backend/api.py
+++ b/app/backend/api.py
@@ -20,7 +20,7 @@ from starlette.exceptions import HTTPException as StarletteHTTPException
 
 from starlette.concurrency import run_in_threadpool
 
-from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, narrative, pdf_text, present, review, store, trace
+from app.backend import case_extras, dismissal_patterns, export as export_mod, ingest, language, narrative, pdf_text, present, review, store, trace
 from app.db import db as DB
 
 MAX_BODY_BYTES = 512 * 1024      # cheap rejection before the 60,000-character rule: UTF-8 worst case plus JSON overhead
@@ -34,10 +34,12 @@ VERSION = "0.1.0"
 BANNER = "Synthetic data only — never paste real records"
 AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
 STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
-_ERR_STATUS = {"bad_request": 400, "input_too_large": 413}
+_ERR_STATUS = {"bad_request": 400, "input_too_large": 413, "unsupported_language": 400}
 _PDF_MESSAGES = {"pdf_no_text_layer": "This PDF has no text layer (it looks scanned). Scanned pages are not read; paste the text instead.",
                  "pdf_unreadable": "This file could not be read as a PDF.", "pdf_encrypted": "This PDF is password-protected and cannot be read.",
                  "pdf_too_large": "The PDF is too large."}
+from app.backend import pdf_checks as _pdf_checks      # noqa: E402  (T-086/T-087)
+_PDF_MESSAGES.update(_pdf_checks.MESSAGES)
 
 
 log = logging.getLogger("zlayt.api")
@@ -246,8 +248,9 @@ def create_app(db_path: str = None, *, call_factory=None, static_dir=None, pipel
         return make_case(text, b.get("name") if isinstance(b.get("name"), str) else (lib["name"] if lib else None), sample)
 
--- api.md billing section at HEAD
39:| GET | `/api/cases/{token}/billing` | T-083 code-only billing analysis: ledger lines (billed, adjustment, paid, balance, each cited), totals by provider, LOP and lien amounts listed separately, rates excluded, ledger-vs-EOB checks; internal view, never in the letter |
242:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
651:## GET /api/cases/{token}/billing  (T-083, D-042)
652:Code-only billing analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals` (the letter's total line is still accepted charges only, D-019). Unknown token: `404 not_found`.
654:{ "billing": {
699:- **Not covered:** amounts in Spanish records are classified by the English billing phrases, so a Spanish charge or rate is usually `unclear` and goes to the paralegal (T-084 reclassify); Latin-American `$1.250,00` figures are read as `$1.250` with no value (`unclear`), never as a wrong number.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:33.172Z

**tool call — Bash**
````
{
 "command": "echo \"--- 2fca530 files\" && git show --stat --format= 2fca530 | cat && echo \"--- audited.py at HEAD\" && cat -n app/llm/audited.py | head -140",
 "description": "List 2fca530 files and read audited.py at HEAD"
}
````

### User / tool · 2026-11-02T04:40:33.281Z

**tool result**
````
--- 2fca530 files
 app/backend/api.py                   |  26 +++--
 app/backend/confidence.py            |   2 +-
 app/backend/pdf_checks.py            | 125 +++++++++++++++++++++++
 app/backend/pdf_hidden.py            | 188 +++++++++++++++++++++++++++++++++++
 app/backend/pdf_ocr.py               | 178 +++++++++++++++++++++++++++++++++
 app/backend/pdf_routes.py            |  25 +++++
 app/backend/pdf_text.py              |  41 ++++++--
 app/backend/pipeline.py              |   2 +
 app/backend/present.py               |   6 +-
 app/backend/reclassify.py            |   2 +-
 app/backend/rejudge.py               |   8 --
 app/backend/trace.py                 |  14 ++-
 app/backend/why.py                   |   1 +
 app/db/db.py                         |  52 +---------
 app/db/schema.sql                    |   2 +-
 evals/run.py                         |  88 ++++------------
 memory/contracts/api.md              |  23 +++++
 requirements.txt                     |   1 +
 tests/unit/_pdf_raw.py               |  68 +++++++++++++
 tests/unit/test_db.py                |  77 +-------------
 tests/unit/test_eval_runner.py       | 170 +------------------------------
 tests/unit/test_pdf_checks_api.py    | 128 ++++++++++++++++++++++++
 tests/unit/test_pdf_hidden.py        |  97 ++++++++++++++++++
 tests/unit/test_pdf_ocr.py           | 152 ++++++++++++++++++++++++++++
 tests/unit/test_provider.py          |   7 +-
 tests/unit/test_provider_backends.py |   3 +
 tests/unit/test_reclassify.py        |   2 +-
 tests/unit/test_trace.py             |  16 ---
 28 files changed, 1096 insertions(+), 408 deletions(-)
--- audited.py at HEAD
     1	"""Audited call wrapper (ADR-003.7, ADR-004, LLM_VS_CODE row 20). The only entry point pipeline code uses.
     2	
     3	1 attempt + 2 retries; every retry changes the request (stricter-format note in the user prompt); one llm_calls row per
     4	attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
     5	"""
     6	import logging
     7	import os
     8	import threading
     9	import time
    10	
    11	from app.db import db as DB
    12	from app.llm import provider as P
    13	
    14	log = logging.getLogger("zlayt.llm")
    15	MAX_ATTEMPTS = 3
    16	_DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
    17	RETRY_DELAYS_S = (0.5, 1.5)
    18	# Errors that are retried: the provider layer gave up (LLMError: timeout, backend failure, invalid JSON, schema-invalid) or the transport did
    19	# (timeout, connection). Output that fails the caller's `validate` (ValueError) is retried too, but only from the validate step. Anything else
    20	# (TypeError, KeyError, AttributeError ... a bug in our code) is logged as one row and propagates: retrying it three times hides it (T-073).
    21	RETRYABLE_PROVIDER_ERRORS = (P.LLMError, TimeoutError, ConnectionError)
    22	RETRYABLE_VALIDATION_ERRORS = (ValueError,)
    23	_CODE = __import__('re').compile(r"^([A-Z][A-Z_]{2,40})\b")
    24	
    25	_RETRY_NOTES = (
    26	    "",
    27	    "\n\n[RETRY 1 of 2: your previous reply was unusable. Reply with exactly one JSON object that satisfies the schema, with no prose and no code fence.]",
    28	    "\n\n[FINAL RETRY: reply with ONLY the raw JSON object, no markdown, no commentary, every required key present, no extra keys.]",
    29	)
    30	
    31	
    32	class LLMFailed(Exception):
    33	    """The LLM layer gave up (every attempt failed, or a fixture was missing). `last_error` is the last attempt's failure code
    34	    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
    35	    code = "LLM_FAILED_AFTER_RETRIES"
    36	    last_error = "LLM_ERROR"
    37	
    38	    def __init__(self, *args, last_error: str = None):
    39	        super().__init__(*args)
    40	        if last_error:
    41	            self.last_error = last_error
    42	
    43	
    44	class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
    45	    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
    46	
    47	    last_error = "FIXTURE_MISS"
    48	
    49	    def __init__(self, prompt_hash: str = ""):
    50	        P.FixtureMissing.__init__(self, prompt_hash)
    51	
    52	
    53	def _error_code(e: Exception) -> str:
    54	    """Our own codes only (SCHEMA_INVALID, TIMEOUT, BACKEND_FAILED ...); anything else is reduced to the exception class."""
    55	    if isinstance(e, P.LLMError):
    56	        m = _CODE.match(str(e))
    57	        return m.group(1) if m else "LLM_ERROR"
    58	    return "VALIDATION_FAILED" if isinstance(e, ValueError) else type(e).__name__
    59	
    60	
    61	def role_for(step: str) -> str:
    62	    s = str(step)
    63	    return "judge" if s.startswith("judge") or (len(s) == 2 and s[0] == "j" and s[1].isdigit()) else "generator"
    64	
    65	
    66	def _t(now):
    67	    return now() if callable(now) else (time.time() if now is None else now)
    68	
    69	
    70	def audited_call(conn, case_id: str, step: str, model: str, system: str, user: str, json_schema: dict, *,
    71	                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
    72	    cwm = complete_with_meta or P.complete_with_meta
    73	    last_err = "unknown"
    74	    for attempt in range(1, MAX_ATTEMPTS + 1):
    75	        u = user + _RETRY_NOTES[attempt - 1]
    76	        h = P.prompt_hash(model, system, u, json_schema)
    77	        t0 = time.monotonic()
    78	        res, err, fixture_miss, bug = None, None, False, None
    79	        try:
    80	            res = cwm(model, system, u, json_schema)
    81	            if validate is not None:
    82	                try:
    83	                    validate(res.output)
    84	                except RETRYABLE_VALIDATION_ERRORS as e:
    85	                    err = _error_code(e)               # schema-invalid output: a failed attempt, retried with a stricter note
    86	        except P.FixtureMissing as e:
    87	            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
    88	        except RETRYABLE_PROVIDER_ERRORS as e:          # only our own error codes are stored, never model- or record-derived text
    89	            err = _error_code(e)
    90	        except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
    91	            err, bug = _error_code(e), e
    92	        ms = int((time.monotonic() - t0) * 1000)
    93	        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
    94	                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
    95	                      parsed_ok=1 if err is None else 0, error=err)
    96	        if item_id:
    97	            fields["item_id"] = item_id
    98	        if res:
    99	            import json as _j
   100	            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
   101	                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
   102	        with _DB_LOCK:
   103	            call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
   104	        if err is None:
   105	            return res.output, call_id
   106	        if bug is not None:
   107	            log.error("llm call raised a programmer error call_id=%s step=%s class=%s", call_id, step, type(bug).__name__)
   108	            raise bug
   109	        last_err = err
   110	        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
   111	        if fixture_miss:
   112	            raise LLMFailedFixtureMiss(h)
   113	        if sleep is not None and attempt < MAX_ATTEMPTS:
   114	            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
   115	    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed", last_error=(last_err or "LLM_ERROR").split()[0])
   116	
   117	
   118	def _dump(o):
   119	    import json
   120	    return json.dumps(o, sort_keys=True)
   121	
   122	
   123	PROMPT_OF_STEP = {"extract": "extract_v1", "j1": "judge_faithfulness_v1", "j2": "judge_amount_class_v1", "j3": "judge_conflict_v4",
   124	                  "j4": "judge_flag_v2", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
   125	PROMPT_OF_STEP.update({"extract_es": "extract_es_v1", "judge_faithfulness_es": "judge_faithfulness_es_v1"})     # Spanish records (D-042, T-085)
   126	
   127	
   128	def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
   129	    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
   130	    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
   131	    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}
   132	
   133	    def call(step, system, user, schema, *, item_id=None, validate=None):
   134	        # a live backend that just failed (rate limit, timeout) is retried after a short pause, not at once (T-075); the fixture backend never sleeps
   135	        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate,
   136	                            prompt_version=PROMPT_OF_STEP.get(step), sleep=None if P.backend_name() == "fixture" else time.sleep)
   137	    return call
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:42.600Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && echo \"=== judge_guard.py\" && cat -n app/backend/judge_guard.py && echo \"=== judges.py 1-60\" && cat -n app/backend/judges.py | sed -n 1,60p && echo \"=== review.py around 90-110\" && cat -n app/backend/review.py | sed -n 88,112p",
 "description": "Read judge_guard.py, judges.py head, and review.py judge call at HEAD"
}
````

### User / tool · 2026-11-02T04:40:42.695Z

**tool result**
````
=== judge_guard.py
     1	"""Narrow judge-call guard (T-073). A judge that cannot answer for an EXPECTED reason (the LLM layer gave up, a fixture is missing, the
     2	backend failed) never blocks the human: the result is 'unavailable' and the exception class is kept so the audit says why. Any other
     3	exception is a bug in our code and propagates (audited_call no longer retries or hides those either).
     4	judges._run turns LLMFailed into 'unavailable' without saying why, so the guard hands the judge a `call` that notes the expected error's class
     5	on its way through; the class (LLMFailed, LLMError, FixtureMissing ...) is returned whichever layer swallowed the exception."""
     6	from app.llm import audited as AU, provider as P
     7	
     8	EXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError)
     9	
    10	
    11	def guarded(fn, *args, **kwargs):
    12	    """Run a judges.run_*_meta function. Returns (verdict, call_id, reason_code, error_class); error_class is None unless the judge could
    13	    not answer for an expected reason (then verdict 'unavailable', reason_code 'NONE')."""
    14	    seen = []
    15	    call = kwargs.get("call")
    16	    if call is not None:
    17	        def noting(*a, **k):
    18	            try:
    19	                return call(*a, **k)
    20	            except EXPECTED_JUDGE_ERRORS as e:
    21	                seen.append(type(e).__name__)
    22	                raise
    23	        kwargs["call"] = noting
    24	    try:
    25	        verdict, call_id, code = fn(*args, **kwargs)
    26	    except EXPECTED_JUDGE_ERRORS as e:
    27	        return "unavailable", None, "NONE", type(e).__name__
    28	    if seen and verdict == "unavailable":
    29	        return verdict, call_id, code, seen[-1]
    30	    return verdict, call_id, code, None
=== judges.py 1-60
     1	"""Judges J1-J4 (rung 2 of the validation ladder; LLM_VS_CODE rows 4, 7, 11, 12; ADR-003.8, ADR-008.5).
     2	Each judge sees only the record text and the candidate (never the generator's reasoning), in nonce delimiters, and returns an
     3	enum. A judge failure is "unavailable", never an exception into the pipeline; invalid output (out-of-enum, missing reason_code) is "unavailable", never positive.
     4	`call(step, system, user, schema, *, item_id=None) -> (output, call_id)` is supplied by the pipeline (audited_call bound to a case)."""
     5	import os
     6	
     7	from pydantic import ValidationError
     8	
     9	from app.backend import injection, schemas
    10	from app.llm import audited as AU, promptlib
    11	
    12	DEFAULT_GENERATOR_MODEL = "claude-sonnet-5-5"
    13	DEFAULT_JUDGE_MODEL = "claude-haiku-5-5"
    14	
    15	
    16	def generator_model() -> str:
    17	    return os.environ.get("GENERATOR_MODEL") or DEFAULT_GENERATOR_MODEL
    18	
    19	
    20	def judge_model() -> str:
    21	    return os.environ.get("JUDGE_MODEL") or DEFAULT_JUDGE_MODEL
    22	
    23	
    24	def _run(step: str, prompt: str, model_cls, quotes: list, lines: list, call, nonce, item_id):
    25	    """Returns (verdict, call_id, reason_code). verdict in the model's enum, or 'unavailable' / 'unsure'."""
    26	    n = nonce or promptlib.nonce(step, *quotes, *[x if isinstance(x, str) else x[1] for x in lines])
    27	    p = promptlib.load(prompt)
    28	    blocks = "\n".join(f"{label}:\n{injection.wrap(q, n)}" for label, q in quotes_labelled(quotes, step))
    29	    extra = "\n".join(f"{x[0]}:\n{injection.wrap(x[1], n)}" if isinstance(x, tuple) else x for x in lines)   # (name, text) = record-derived, wrapped
    30	    user = blocks + "\n" + extra + "\nReturn the JSON object."
    31	    try:
    32	        out, call_id = call(step, p.text, user, model_cls.model_json_schema(), item_id=item_id)
    33	    except AU.LLMFailed:
    34	        return "unavailable", None, "NONE"
    35	    try:
    36	        m = model_cls.model_validate(out)
    37	    except (ValidationError, TypeError, ValueError):
    38	        return "unavailable", call_id, "NONE"   # invalid judge output (bad enum, missing reason_code) = judge did not answer
    39	    return m.verdict, call_id, m.reason_code
    40	
    41	
    42	def quotes_labelled(quotes: list, step: str):
    43	    names = {"j3": ["QUOTE A", "QUOTE B"]}.get(step, ["RECORD TEXT"] * len(quotes))
    44	    return zip(names, quotes)
    45	
    46	
    47	def run_j1_meta(summary: str, excerpt: str, label: str, *, call, nonce=None, item_id=None):
    48	    return _run("j1", "judge_faithfulness_v1", schemas.Judge1, [excerpt],
    49	                [("SOURCE LABEL", label), f"CANDIDATE SUMMARY: {summary}"], call, nonce, item_id)
    50	
    51	
    52	def run_j2_meta(excerpt: str, raw_amount: str, code_class: str, *, call, nonce=None, item_id=None):
    53	    return _run("j2", "judge_amount_class_v1", schemas.Judge2, [excerpt],
    54	                [f"AMOUNT: {raw_amount}", f"CLASS: {code_class}"], call, nonce, item_id)
    55	
    56	
    57	def run_j3_meta(excerpt_a: str, excerpt_b: str, *, call, nonce=None, item_id=None, category=None):
    58	    """`category` (the flag category the software proposed) selects the decision rule in judge_conflict_v2 (T-075)."""
    59	    return _run("j3", "judge_conflict_v2", schemas.Judge3, [excerpt_a, excerpt_b], [f"FLAG CATEGORY: {category}"] if category else [],
    60	                call, nonce, item_id)
=== review.py around 90-110
    88	    numeric = [t for t in toks if _NUMERIC_TOKEN.search(t)]
    89	    if numeric:    # D-034: a number, date or $ figure that is not in the quote is never saved, with or without confirm_warnings
    90	        raise _bad("The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(numeric) + ". Remove it or change the quote.",
    91	                   tokens=numeric, reason="SUMMARY_NUMBER_NOT_IN_EXCERPT")
    92	    blocking = []
    93	    if toks:
    94	        code_reasons.append("SUMMARY_TOKEN_NOT_IN_EXCERPT")
    95	        blocking.append({"code": "SUMMARY_TOKEN_NOT_IN_EXCERPT", "message": "\u201c" + "\u201d, \u201c".join(toks) + "\u201d is not in the quote.", "item_id": item_id})
    96	    if g.dropped_qualifiers(new_sum, new_exc):
    97	        code_reasons.append("SUMMARY_DROPS_QUALIFIER")
    98	    if span is None:
    99	        code_reasons.append("HIGHLIGHT_NOT_FOUND")
   100	    verdict, call_id, ladder_verdict, judge_code, judge_error = "unavailable", None, "unavailable", "NONE", None
   101	    if call is not None:
   102	        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
   103	        ladder_verdict = judges.to_ladder("j1", verdict)
   104	    if ladder_verdict in ("partially", "unsupported"):
   105	        code = "JUDGE_PARTIAL" if ladder_verdict == "partially" else "JUDGE_UNSUPPORTED"
   106	        blocking.append({"code": code, "message": "The second check could not fully support the summary from the quote.", "item_id": item_id})
   107	    if blocking and not bool(body.get("confirm_warnings")):
   108	        raise ReviewError(409, "needs_confirm", {"warnings": blocking}, "This edit adds a number or fact that is not in the quote.")
   109	    state, reasons = confidence.compose_state({"grounding_failures": [], "code_reasons": code_reasons, "judge": ladder_verdict},
   110	                                              {"injection": bool(rec.get("injection_tag")), "date_status": rec.get("date_status", "parsed")})
   111	    return {"toks": toks, "code_reasons": code_reasons, "blocking": blocking, "ladder_verdict": ladder_verdict, "call_id": call_id, "judge_code": judge_code,
   112	            "judge_error": judge_error,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:48.659Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && grep -n -E \"^class |class .*Error|class .*Missing\" app/llm/provider.py && echo \"--- test_audited.py at HEAD\" && cat -n tests/unit/test_audited.py | head -150",
 "description": "Check provider exception hierarchy and read test_audited.py at HEAD"
}
````

### User / tool · 2026-11-02T04:40:48.750Z

**tool result (error)**
````
Exit code 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:51.350Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && grep -n -E \"class \" app/llm/provider.py | head -30; echo \"--- test_audited\"; wc -l tests/unit/test_audited.py",
 "description": "Grep provider exception classes and count test_audited lines"
}
````

### User / tool · 2026-11-02T04:40:51.442Z

**tool result**
````
--- test_audited
     146 tests/unit/test_audited.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:54.607Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && ls app/llm/ && grep -rn -E \"class (LLMError|FixtureMissing)\" app/ | head; grep -n \"import\\|provider\" app/llm/provider.py | head -5",
 "description": "Locate LLMError and FixtureMissing definitions"
}
````

### User / tool · 2026-11-02T04:40:54.707Z

**tool result**
````
__init__.py
_types.py
audited.py
backends
lexicon.yaml
promptlib.py
prompts
provider.py
record.py
app/llm/_types.py:7:class LLMError(Exception):
app/llm/_types.py:11:class FixtureMissing(LLMError):
8:import contextlib
9:import hashlib
10:import json
11:import os
12:import pathlib
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:40:57.500Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n tests/unit/test_audited.py",
 "description": "Read test_audited.py at HEAD"
}
````

### User / tool · 2026-11-02T04:40:57.595Z

**tool result**
````
     1	"""Audited call wrapper: retries and audit rows. ADR-003.7, ADR-004, privacy invariants (never log record text); fixture/fake backend only."""
     2	import pytest
     3	from app.llm import audited as AU, provider as P
     4	from app.db import db as DB
     5	
     6	MISS = getattr(P, "FixtureMissing", None) or P.FixtureMiss   # T-034 AC8 name is FixtureMissing; test_provider pins that the name exists
     7	SCHEMA = {"type": "object", "properties": {"v": {"type": "string"}}, "required": ["v"]}
     8	
     9	@pytest.fixture
    10	def env(tmp_path):
    11	    conn = DB.connect(str(tmp_path / "a.sqlite"))
    12	    return conn, DB.create_case(conn, "SYNTHETIC text", now=1.0)
    13	
    14	def seq(*outs):
    15	    """complete_with_meta fake: each item is an output dict or an Exception; records the user prompts."""
    16	    state = dict(i=0, users=[])
    17	    def f(model, system, user, schema):
    18	        state["users"].append(user)
    19	        o = outs[min(state["i"], len(outs) - 1)]; state["i"] += 1
    20	        if isinstance(o, Exception):
    21	            raise o
    22	        return P.LLMResult(output=o, backend="fixture", model_resolved=model)
    23	    f.state = state
    24	    return f
    25	
    26	def ac(conn, cid, *a, **kw):
    27	    """audited_call; retries are immediate (no backoff, so no sleep hook is needed - if backend adds one, patch it here)."""
    28	    return AU.audited_call(conn, cid, *a, **kw)
    29	
    30	def rows(conn, cid):
    31	    return DB.table_counts(conn, cid).get("llm_calls", 0)
    32	
    33	def test_first_success_writes_one_row_and_returns_call_id(env):
    34	    """ADR-004: returns (output, call_id); one llm_calls row per attempt."""
    35	    conn, cid = env
    36	    out, call_id = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=seq({"v": "x"}))
    37	    assert out == {"v": "x"} and call_id and rows(conn, cid) == 1
    38	
    39	def test_retries_up_to_two_then_succeeds(env):
    40	    """ADR-003.7: 1 + 2 retries; third attempt succeeds -> 3 rows."""
    41	    conn, cid = env
    42	    f = seq(P.LLMError("timeout"), P.LLMError("bad json"), {"v": "ok"})
    43	    out, _ = ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    44	    assert out == {"v": "ok"} and rows(conn, cid) == 3
    45	
    46	def test_three_failures_raise_llm_failed_after_retries(env):
    47	    """ADR-003.7 / LLM_FAILED_AFTER_RETRIES: exactly 3 attempts, then a visible failure; no fourth call."""
    48	    conn, cid = env
    49	    f = seq(P.LLMError("x"))
    50	    with pytest.raises(AU.LLMFailed) as e:
    51	        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    52	    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 3 and rows(conn, cid) == 3
    53	
    54	def test_retries_change_something(env):
    55	    """ADR-003.7: a retry is never an identical request - the user prompt carries a stricter-format request."""
    56	    conn, cid = env
    57	    f = seq(P.LLMError("x"), {"v": "ok"})
    58	    ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    59	    assert f.state["users"][0] != f.state["users"][1]
    60	
    61	def test_fixture_missing_is_one_attempt_and_becomes_llm_failed(env):
    62	    """T-034 AC8 / T-037 AC7 / FIXTURE_MISS: a miss is final (one attempt, one row); the wrapper turns it into LLMFailed(LLM_FAILED_AFTER_RETRIES) and the row logs the prompt hash."""
    63	    conn, cid = env
    64	    f = seq(MISS("abc123hash"))
    65	    with pytest.raises(AU.LLMFailed) as e:
    66	        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f)
    67	    assert e.value.code == "LLM_FAILED_AFTER_RETRIES" and len(f.state["users"]) == 1
    68	    (row,) = DB.list_llm_calls(conn, cid)
    69	    assert "abc123hash" in (row["error"] or "")
    70	
    71	def test_audit_rows_record_model_backend_attempt_and_error_code(env):
    72	    """Checklist 9 / ADR-004: one row per attempt with the pinned model, backend, attempt index and a failure code; no prompt text in the error column."""
    73	    conn, cid = env
    74	    f = seq(P.LLMError("TIMEOUT"), P.LLMError("INVALID_JSON"), {"v": "ok"})
    75	    ac(conn, cid, "extract", "model-x", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=f)
    76	    rs = sorted(DB.list_llm_calls(conn, cid), key=lambda r: r["attempt"])
    77	    assert [r["attempt"] for r in rs] == [1, 2, 3]
    78	    assert all(r["model"] == "model-x" and r["backend"] == "fixture" and r["step"] == "extract" for r in rs)
    79	    assert rs[0]["error"] and rs[1]["error"] and not rs[2]["error"]
    80	    assert all("SECRET RECORD TEXT" not in (r["error"] or "") for r in rs)
    81	
    82	def test_schema_invalid_output_counts_as_failed_attempt(env):
    83	    """ADR-005 SCHEMA_INVALID: output failing `validate` is retried; after 3 -> LLMFailed."""
    84	    conn, cid = env
    85	    def validate(o):
    86	        if "v" not in o:
    87	            raise ValueError("missing v")
    88	    f = seq({"zzz": 1})
    89	    with pytest.raises(AU.LLMFailed):
    90	        ac(conn, cid, "extract", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
    91	    assert len(f.state["users"]) == 3
    92	
    93	def test_prompts_stored_so_delete_case_removes_them(env):
    94	    """ADR-006: prompts live in llm_calls, which delete_case empties."""
    95	    conn, cid = env
    96	    ac(conn, cid, "extract", "m", "s", "RECORD TEXT HERE", SCHEMA, complete_with_meta=seq({"v": "x"}))
    97	    DB.delete_case(conn, cid)
    98	    assert rows(conn, cid) == 0
    99	
   100	def test_never_prints_record_text(env, capsys, caplog):
   101	    """Arch invariant: never log record text, prompts or responses (errors log call_id only)."""
   102	    conn, cid = env
   103	    with pytest.raises(AU.LLMFailed):
   104	        ac(conn, cid, "extract", "m", "s", "SECRET RECORD TEXT", SCHEMA, complete_with_meta=seq(P.LLMError("SECRET RECORD TEXT in error")))
   105	    out = capsys.readouterr()
   106	    assert "SECRET RECORD TEXT" not in out.out + out.err + caplog.text
   107	
   108	
   109	# ---------------------------------------------------------------- T-073 r2: retry provider and transport errors only; bugs propagate
   110	@pytest.mark.parametrize("bug", [RuntimeError("programmer bug in provider adapter"), TypeError("x"), KeyError("k"), AttributeError("a"), ZeroDivisionError()])
   111	def test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates(env, bug):
   112	    conn, cid = env
   113	    f = seq(bug)
   114	    with pytest.raises(type(bug)):
   115	        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f)
   116	    assert len(f.state["users"]) == 1                                                      # one attempt, not three
   117	    (row,) = DB.list_llm_calls(conn, cid)                                                  # and the bug is on the audit trail by class name only
   118	    assert row["error"] == type(bug).__name__ and not row["parsed_ok"]
   119	
   120	
   121	def test_a_type_error_inside_validate_is_a_bug_and_propagates(env):
   122	    conn, cid = env
   123	    def validate(o):
   124	        return o["v"] + 1                                                                  # TypeError: our code, not the model's output
   125	    f = seq({"v": "x"})
   126	    with pytest.raises(TypeError):
   127	        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f, validate=validate)
   128	    assert len(f.state["users"]) == 1 and rows(conn, cid) == 1
   129	
   130	
   131	@pytest.mark.parametrize("transport", [TimeoutError("t"), ConnectionError("c"), ConnectionResetError("r")])
   132	def test_transport_errors_are_retried(env, transport):
   133	    conn, cid = env
   134	    f = seq(transport, {"v": "ok"})
   135	    out, _ = ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=f)
   136	    assert out == {"v": "ok"} and rows(conn, cid) == 2
   137	
   138	
   139	def test_llm_failed_names_the_last_failure_code(env):
   140	    conn, cid = env
   141	    with pytest.raises(AU.LLMFailed) as e:
   142	        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=seq(P.LLMError("TIMEOUT claude-cli")))
   143	    assert e.value.last_error == "TIMEOUT"
   144	    with pytest.raises(AU.LLMFailed) as e:
   145	        ac(conn, cid, "j1", "m", "s", "u", SCHEMA, complete_with_meta=seq(MISS("abc")))
   146	    assert e.value.last_error == "FIXTURE_MISS"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:01.431Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n tests/unit/test_judge_guard.py",
 "description": "Read test_judge_guard.py at HEAD"
}
````

### User / tool · 2026-11-02T04:41:01.544Z

**tool result**
````
     1	"""T-073: the review.py judge path catches only expected judge errors, keeps the error class in the recorded ladder, and lets bugs propagate."""
     2	import pytest
     3	from app.backend import judge_guard, judges, review as RV
     4	from app.db import db as DB
     5	from app.llm import audited as AU, provider as P
     6	from tests.unit.test_review_rules import ent, judge, seeded
     7	
     8	
     9	def _raising(exc):
    10	    def call(step, system, user, schema, *, item_id=None):
    11	        raise exc
    12	    return call
    13	
    14	
    15	def test_judges_own_handling_of_llmfailed_is_unavailable():
    16	    assert judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=_raising(AU.LLMFailed()))[:3] == ("unavailable", None, "NONE")
    17	
    18	
    19	@pytest.mark.parametrize("exc", [AU.LLMFailed(), P.FixtureMissing("abc"), P.LLMError("TIMEOUT")])
    20	def test_guard_turns_expected_errors_into_unavailable_with_class(exc):
    21	    v, cid, code, err = judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))
    22	    assert (v, cid, code, err) == ("unavailable", None, "NONE", type(exc).__name__)
    23	
    24	
    25	def test_guard_passes_a_normal_answer_through():
    26	    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=judge("supported"))
    27	    assert (v, code, err) == ("supported", "NONE", None)
    28	
    29	
    30	@pytest.mark.parametrize("exc", [RuntimeError("bug"), KeyError("x"), AttributeError("y")])
    31	def test_guard_does_not_swallow_unexpected_errors(exc):
    32	    with pytest.raises(type(exc)):
    33	        judge_guard.guarded(lambda *a, **k: (_ for _ in ()).throw(exc))
    34	
    35	
    36	def test_edit_with_expected_judge_error_saves_as_unavailable_and_keeps_class(tmp_path):
    37	    conn, cid, out = seeded(tmp_path)
    38	    eid = ent(out, 5)
    39	    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(P.FixtureMissing("h")))
    40	    assert [w["code"] for w in r["warnings"]] == ["JUDGE_UNAVAILABLE"]
    41	    jd = DB.get_item(conn, eid, cid)["ladder"]["judge"]
    42	    assert jd["verdict"] == "unavailable" and jd["error_class"] == "FixtureMissing"
    43	
    44	
    45	def test_edit_with_unexpected_error_propagates_and_saves_nothing(tmp_path):
    46	    conn, cid, out = seeded(tmp_path)
    47	    eid = ent(out, 5)
    48	    before = DB.get_item(conn, eid, cid)
    49	    with pytest.raises(RuntimeError):
    50	        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(RuntimeError("bug")))
    51	    after = DB.get_item(conn, eid, cid)
    52	    assert after["review_status"] == before["review_status"] and not after.get("edited")
    53	
    54	
    55	# ---------------------------------------------------------------- r2: the real call path (audited_call underneath), error_class for LLMFailed
    56	def _through_audited(tmp_path, provider):
    57	    """A review `call` that runs the real audited_call over a fake provider, as the pipeline's make_call does."""
    58	    conn = DB.connect(str(tmp_path / "ag.sqlite"))
    59	    cid = DB.create_case(conn, "SYNTHETIC text", now=1.0)
    60	
    61	    def call(step, system, user, schema, *, item_id=None, validate=None):
    62	        return AU.audited_call(conn, cid, step, "m", system, user, schema, complete_with_meta=provider, validate=validate, item_id=item_id)
    63	    return conn, cid, call
    64	
    65	
    66	def _provider(exc):
    67	    n = {"calls": 0}
    68	
    69	    def cwm(model, system, user, schema):
    70	        n["calls"] += 1
    71	        raise exc
    72	    cwm.n = n
    73	    return cwm
    74	
    75	
    76	def test_a_bug_in_the_provider_adapter_propagates_through_the_real_audited_call_and_the_guard(tmp_path):
    77	    conn, cid, call = _through_audited(tmp_path, p := _provider(RuntimeError("programmer bug in provider adapter")))
    78	    with pytest.raises(RuntimeError):
    79	        judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=call)
    80	    assert p.n["calls"] == 1 and len(DB.list_llm_calls(conn, cid)) == 1
    81	
    82	
    83	def test_a_bug_in_the_provider_adapter_through_apply_review_raises_and_saves_nothing(tmp_path):
    84	    conn, cid, out = seeded(tmp_path)
    85	    eid = ent(out, 5)
    86	    before = DB.get_item(conn, eid, cid)
    87	    _c, _i, call = _through_audited(tmp_path, p := _provider(RuntimeError("programmer bug in provider adapter")))
    88	    with pytest.raises(RuntimeError):
    89	        RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=call)
    90	    after = DB.get_item(conn, eid, cid)
    91	    assert p.n["calls"] == 1 and after["review_status"] == before["review_status"] and not after.get("edited")
    92	
    93	
    94	def test_llmfailed_is_returned_with_its_class_even_though_judges_run_swallows_it():
    95	    v, cid, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=_raising(AU.LLMFailed("down")))
    96	    assert (v, cid, code, err) == ("unavailable", None, "NONE", "LLMFailed")
    97	
    98	
    99	def test_provider_failure_through_the_real_audited_call_records_llmfailed(tmp_path):
   100	    conn, cid, call = _through_audited(tmp_path, p := _provider(P.LLMError("TIMEOUT claude-cli")))
   101	    v, call_id, code, err = judge_guard.guarded(judges.run_j1_meta, "Pain.", "Pain.", "PT", call=call)
   102	    assert (v, err) == ("unavailable", "LLMFailed") and p.n["calls"] == 3
   103	
   104	
   105	@pytest.mark.parametrize("exc,cls", [(AU.LLMFailed("down"), "LLMFailed"), (AU.LLMFailedFixtureMiss("h"), "LLMFailedFixtureMiss"),
   106	                                     (P.FixtureMissing("h"), "FixtureMissing"), (P.LLMError("TIMEOUT"), "LLMError")])
   107	def test_edit_records_error_class_on_the_ladder_for_every_expected_failure(tmp_path, exc, cls):
   108	    conn, cid, out = seeded(tmp_path)
   109	    eid = ent(out, 5)
   110	    r = RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=_raising(exc))
   111	    assert [w["code"] for w in r["warnings"]] == ["JUDGE_UNAVAILABLE"]
   112	    jd = DB.get_item(conn, eid, cid)["ladder"]["judge"]
   113	    assert jd["verdict"] == "unavailable" and jd["error_class"] == cls
   114	
   115	
   116	def test_a_judge_that_answers_normally_has_no_error_class(tmp_path):
   117	    conn, cid, out = seeded(tmp_path)
   118	    eid = ent(out, 5)
   119	    RV.apply_review(conn, cid, eid, dict(action="edit", edits=dict(summary="Pain improving.")), call=judge("supported"))
   120	    assert not DB.get_item(conn, eid, cid)["ladder"]["judge"].get("error_class")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:06.412Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n app/backend/reclassify.py | sed -n 1,95p",
 "description": "Read reclassify.py lines 1-95 at HEAD"
}
````

### User / tool · 2026-11-02T04:41:06.504Z

**tool result**
````
     1	"""Guarded charge reclassification by the paralegal (T-084, D-042; supersedes the D-010 'a rate can never become a charge' cut).
     2	
     3	Two directions, one rule of thumb: taking a figure OUT of the billed-charges total is always the paralegal's call; putting a figure INTO it
     4	needs evidence.
     5	- charge -> not-a-charge: always allowed. The row's kind becomes `unclear` (shown as "not added to the total", never totaled).
     6	- not-a-charge (rate, estimate, unclear, damages) -> charge: allowed only when (1) CODE finds charged-amount wording (charged, charges, billed,
     7	  invoiced, amount due ...) in the same sentence as the figure, with no negation, the figure has a parsed value and the record is not
     8	  injection-tagged, AND (2) judge 2 re-checks the figure against the class `charge` and agrees. Otherwise 422 `reclassify_refused` with a
     9	  fixed reason and nothing changes. Undoing the paralegal's own earlier demotion of a figure the code first called a charge skips both
    10	  checks ONLY while nothing under it has moved: a rerun that changed the code's class of the figure, or its sentence, makes the restore
    11	  run both checks again like any other rate-to-charge (the stored judge answer was about the old sentence).
    12	- A sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of) never passes the code wording check, even
    13	  when it also says charge or billed: "Charge per visit $185" and "Billed $150 per visit" state a rate and stay refused.
    14	- A rerun keeps her class for the same figure; a charge she promoted is dropped back to the code's class if the sentence under it changed.
    15	Whatever the direction: the item goes back to `pending` (she decides again), the ladder keeps who/what/when, and an audit event is written.
    16	The judge sees only the record text, the figure and the class (judges.run_j2_meta); the model supplies no prose that is stored."""
    17	import hashlib
    18	import re
    19	
    20	from fastapi import Request
    21	
    22	from app.backend import confidence, generator, judge_guard, judges, review, store, why as WHY
    23	from app.db import db as DB
    24	
    25	TARGETS = ("charge", "not_a_charge")
    26	NOT_A_CHARGE_KIND = "unclear"
    27	AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
    28	_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
    29	_WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
    30	# a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
    31	_RATE_CUE = re.compile(r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
    32	                       r"|\ba\s+(?:visit|session|hour|day|treatment|appointment)\b|\b(?:daily|hourly|session|visit|unit|flat)\s+(?:rate|fee|price)\b|\brate\b"
    33	                       r"|(?<![\w$])[x\u00d7]\s*\d+\b|\b\d+\s*[x\u00d7]\s*\$?\d", re.IGNORECASE)
    34	_NEGATED = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)
    35	
    36	REFUSALS = {
    37	    "NO_VALUE": "The dollar value of this figure could not be read, so it cannot become a charge.",
    38	    "INJECTION_SUSPECTED": "This record has instruction-like text, so a figure from it cannot become a charge.",
    39	    "NO_CHARGE_WORDING": "The sentence with this figure has no wording that says it was charged or billed (such as charged, billed, invoiced or amount due), so it stays a figure that is not a charge.",
    40	    "JUDGE_DISAGREES": "A second AI check read this figure as something other than a charge, so it stays as it is.",
    41	    "JUDGE_UNSURE": "A second AI check could not tell whether this figure is a charge, so it stays as it is.",
    42	    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
    43	}
    44	
    45	
    46	def _sentences(excerpt: str):
    47	    """[(start, end, text)] of the excerpt's sentences, the same boundary rule amounts.classify uses."""
    48	    out, pos = [], 0
    49	    for m in _BOUNDARY.finditer(excerpt):
    50	        out.append((pos, m.start(), excerpt[pos:m.start()]))
    51	        pos = m.end()
    52	    out.append((pos, len(excerpt), excerpt[pos:]))
    53	    return out
    54	
    55	
    56	def _figure_spans(excerpt: str, row: dict, rec):
    57	    """Where this amount sits in the excerpt: the stored absolute offsets when they check out, else every occurrence of its text."""
    58	    raw = row["text"]
    59	    if rec is not None and row.get("excerpt_start") is not None:
    60	        i = row["excerpt_start"] - generator.body_offset(rec)
    61	        if 0 <= i and excerpt[i:i + len(raw)] == raw:
    62	            return [(i, i + len(raw))]
    63	    return [(m.start(), m.end()) for m in re.finditer(re.escape(raw), excerpt)]
    64	
    65	
    66	def charge_wording(excerpt: str, row: dict, rec=None):
    67	    """Code check: the charged-amount phrase in the figure's own sentence (every occurrence of the figure must have one, no negation, no rate
    68	    cue), or None. A rate cue decides: "Charge per visit $185" and "Billed $150 per visit" are rates."""
    69	    spans = _figure_spans(excerpt or "", row, rec)
    70	    found = None
    71	    for s, _e in spans:
    72	        sent = next((t for a, b, t in _sentences(excerpt) if a <= s <= b), "")
    73	        m = _WORDING.search(sent)
    74	        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent):
    75	            return None
    76	        found = found or m.group(0)
    77	    return found
    78	
    79	
    80	def _refuse(reason: str, **detail):
    81	    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
    82	                                                          **detail}, REFUSALS[reason])
    83	
    84	
    85	def _sha(text) -> str:
    86	    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]
    87	
    88	
    89	def _log(conn, case_id, item_id, before, after, t):
    90	    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
    91	                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))
    92	
    93	
    94	def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    95	    t = review._now(now)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:09.235Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n app/backend/reclassify.py | sed -n 140,240p",
 "description": "Read reclassify.py lines 140-240 at HEAD"
}
````

### User / tool · 2026-11-02T04:41:09.326Z

**tool result**
````
   140	                                          "note": lad["reclassification"]["note"]}, t)
   141	    return _result(conn, case_id, item_id, {"from": old_kind, "to": new_kind, "wording": wording, "judge_verdict": (jd or {}).get("verdict"),
   142	                                           "restored": restored}, [])
   143	
   144	
   145	def _may_restore(row: dict, prior: dict, original: str) -> bool:
   146	    """Undoing her own demotion may skip both checks only while the code's original call still stands: the figure was a charge and has a judge
   147	    answer, and no rerun has since changed the code's class of the figure or its sentence. Otherwise the guard runs in full."""
   148	    if original != "charge" or prior.get("previous_judge") is None:
   149	        return False
   150	    rerun = prior.get("rerun")
   151	    if rerun is None:
   152	        return prior.get("excerpt_sha") in (None, _sha(row["excerpt"]))
   153	    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])
   154	
   155	
   156	def _guard(row: dict, rec, call):
   157	    """The two checks for putting a figure into the total, code first. Returns (wording, {'judge': ladder judge dict}) or raises 422."""
   158	    if row["value_cents"] is None:
   159	        raise _refuse("NO_VALUE")
   160	    if rec is not None and rec.get("injection_tag"):
   161	        raise _refuse("INJECTION_SUSPECTED")
   162	    wording = charge_wording(row["excerpt"], row, rec)
   163	    if wording is None:
   164	        raise _refuse("NO_CHARGE_WORDING")
   165	    if call is None:
   166	        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
   167	    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row["excerpt"], row["text"], "charge", call=call, item_id=row["id"])
   168	    ladder_verdict = judges.to_ladder("j2", verdict)
   169	    if ladder_verdict != "supported":
   170	        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
   171	        raise _refuse(reason, wording=wording, **({"error_class": err} if err else {}))
   172	    return wording, {"judge": {"model": judges.judge_model(), "prompt_version": "judge_amount_class_v1", "call_id": call_id, "verdict": verdict,
   173	                               "reason_code": code}}
   174	
   175	
   176	def _result(conn, case_id, item_id, change, warnings):
   177	    from app.backend import present
   178	    amount = present._VIEW["amount"](DB.get_item(conn, item_id, case_id), present._recs_by_id(conn, case_id))     # the GET /cases shape: `kind` is the class
   179	    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
   180	            "review": present.review_view(conn, case_id), "reclassified": change, "warnings": warnings}
   181	
   182	
   183	def carry_over(old: dict, it: dict) -> dict:
   184	    """pipeline._persist hook: a rerun re-derives the code's class, but a figure the paralegal reclassified keeps her class (same figure only)."""
   185	    rc = (old.get("ladder") or {}).get("reclassification")
   186	    if not rc or old["kind"] == it["cls"] or old["text"] != it["text"] or old["value_cents"] != it["cents"]:
   187	        return it
   188	    if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(it.get("excerpt")):      # her promotion was checked against another sentence
   189	        return it
   190	    ladder = {**old["ladder"], "reclassification": {**rc, "rerun": {"code_class": it["cls"], "excerpt_sha": _sha(it.get("excerpt"))}}}     # what the code says now
   191	    return {**it, "cls": old["kind"], "kind": old["kind"], "state": old["state"], "reasons": old["state_reasons"], "ladder": ladder,
   192	            "why": " ".join(WHY.why(c) for c in old["state_reasons"])}
   193	
   194	
   195	def add_routes(app, *, conn, get_case, body_of, make_call):
   196	    @app.post("/api/cases/{token}/items/{item_id}/reclassify")
   197	    async def reclassify_item(token: str, item_id: str, request: Request):
   198	        b = await body_of(request)
   199	        c = conn()
   200	        try:
   201	            get_case(c, token)
   202	            return reclassify(c, token, item_id, b, call=make_call(c, token))
   203	        finally:
   204	            c.close()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:41.650Z

The reclassify write path at HEAD ends in `_log` after `update_item`, so I need to see whether the failed 500 leaves the item changed. Next I'll read the new T-084 tests and the restore helpers.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:43.654Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n tests/unit/test_reclassify.py | sed -n 1,140p",
 "description": "Read test_reclassify.py lines 1-140 at HEAD"
}
````

### User / tool · 2026-11-02T04:41:43.752Z

**tool result**
````
     1	"""T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun."""
     2	import pytest
     3	from fastapi.testclient import TestClient
     4	from app.backend import pipeline as PL, present, reclassify as RC, review as RV
     5	from app.backend.api import create_app
     6	from app.db import db as DB
     7	from app.llm import audited as AU
     8	from tests.unit._fakes import FakeCall, sample_script
     9	
    10	TEXT = """=== Record 1 ===
    11	Date: 2026-03-02
    12	Source: Capital PT, visit 1
    13	Excerpt: "Visit completed. Rate of $185 per visit."
    14	
    15	=== Record 2 ===
    16	Date: 2026-03-09
    17	Source: Capital PT, visit 2
    18	Excerpt: "Visit completed. Charge per visit $185."
    19	
    20	=== Record 3 ===
    21	Date: 2026-03-16
    22	Source: Capital Imaging
    23	Excerpt: "MRI performed. Charge: $310."
    24	
    25	=== Record 4 ===
    26	Date: 2026-03-23
    27	Source: Capital PT, visit 4
    28	Excerpt: "Visit completed. Not billed $90 per visit to this patient."
    29	
    30	=== Record 5 ===
    31	Date: 2026-03-30
    32	Source: Capital PT, visit 5
    33	Excerpt: "Visit completed. $185 was billed to the patient."
    34	
    35	=== Record 6 ===
    36	Date: 2026-04-06
    37	Source: Capital PT, visit 6
    38	Excerpt: "Visit completed. Billed $150 per visit."
    39	"""
    40	J2 = lambda v, code="NONE": {"j2": {"verdict": v, "reason_code": code}}     # noqa: E731
    41	
    42	
    43	def seeded(tmp_path, judge="agree"):
    44	    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    45	    conn = DB.connect(str(tmp_path / "rc.sqlite")); cid = DB.create_case(conn, TEXT, now=1.0)
    46	    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 1.0)
    47	    return conn, cid
    48	
    49	
    50	def kinds(conn, cid):
    51	    return {a["text"] + "@" + a["record_ids"][0]: a for a in DB.list_items(conn, cid, "amount")}
    52	
    53	
    54	def aid(conn, cid, text, rec):
    55	    return kinds(conn, cid)[f"{text}@{rec}"]["id"]
    56	
    57	
    58	def events(conn, cid, item_id):
    59	    return [e for e in DB.list_events(conn, cid, item_id) if (e.get("after") or {}).get("event") == "reclassify"]
    60	
    61	
    62	def test_fixture_classes_are_what_the_tests_assume(tmp_path):
    63	    conn, cid = seeded(tmp_path)
    64	    k = kinds(conn, cid)
    65	    assert (k["$185@r1"]["kind"], k["$185@r2"]["kind"], k["$310@r3"]["kind"], k["$90@r4"]["kind"]) == ("rate", "rate", "charge", "rate")
    66	    assert (k["$185@r5"]["kind"], k["$150@r6"]["kind"]) == ("unclear", "rate")       # r5: charged wording, no rate cue; r2 and r6: wording AND a rate cue
    67	
    68	
    69	# ---------------------------------------------------------------- charge -> not a charge
    70	def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
    71	    conn, cid = seeded(tmp_path)
    72	    a = aid(conn, cid, "$310", "r3")
    73	    RV.apply_review(conn, cid, a, {"action": "accept"})
    74	    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge", "note": "This is a retainer, not a bill."}, call=None, now=5.0)
    75	    assert r["amount"]["kind"] == "unclear" and r["item"]["review_status"] == "pending"          # her earlier accept was about the old meaning
    76	    assert r["totals"]["accepted"]["cents"] == 0 and r["reclassified"] == {"from": "charge", "to": "unclear", "wording": None, "judge_verdict": None, "restored": False}
    77	    [ev] = events(conn, cid, a)
    78	    assert ev["before"]["kind"] == "charge" and ev["after"]["kind"] == "unclear" and ev["after"]["note"] == "This is a retainer, not a bill."
    79	    row = DB.get_item(conn, a, cid)
    80	    assert row["ladder"]["reclassification"]["by"] == "reviewer" and row["ladder"]["code_checks"]["classified_by"] == "reviewer:reclassified"
    81	    assert any(e["action"] == "reset" for e in DB.list_events(conn, cid, a))                    # the reset is its own audited event
    82	
    83	
    84	def test_same_direction_is_a_noop_without_an_event(tmp_path):
    85	    conn, cid = seeded(tmp_path)
    86	    a = aid(conn, cid, "$185", "r1")
    87	    r = RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    88	    assert r["reclassified"] is None and not events(conn, cid, a)
    89	
    90	
    91	def test_undoing_her_own_demotion_restores_the_code_class_without_a_judge(tmp_path):
    92	    conn, cid = seeded(tmp_path)
    93	    a = aid(conn, cid, "$310", "r3")
    94	    before = DB.get_item(conn, a, cid)["ladder"]["judge"]
    95	    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    96	    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)                                # no judge call available: still fine
    97	    assert r["amount"]["kind"] == "charge" and r["reclassified"]["restored"] is True
    98	    assert DB.get_item(conn, a, cid)["ladder"]["judge"] == before and len(events(conn, cid, a)) == 2
    99	
   100	
   101	# ---------------------------------------------------------------- not a charge -> charge (guarded)
   102	def test_rate_without_charge_wording_is_422_and_the_judge_is_never_asked(tmp_path):
   103	    conn, cid = seeded(tmp_path)
   104	    a = aid(conn, cid, "$185", "r1")
   105	    call = FakeCall(J2("agree"))
   106	    with pytest.raises(RV.ReviewError) as e:
   107	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
   108	    assert (e.value.status, e.value.code, e.value.detail["reason"], e.value.detail["check"]) == (422, "reclassify_refused", "NO_CHARGE_WORDING", "code")
   109	    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)
   110	
   111	
   112	def test_negated_wording_does_not_count(tmp_path):
   113	    conn, cid = seeded(tmp_path)
   114	    with pytest.raises(RV.ReviewError) as e:
   115	        RC.reclassify(conn, cid, aid(conn, cid, "$90", "r4"), {"to": "charge"}, call=FakeCall(J2("agree")))
   116	    assert e.value.detail["reason"] == "NO_CHARGE_WORDING"
   117	
   118	
   119	def test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge(tmp_path):
   120	    conn, cid = seeded(tmp_path)
   121	    a = aid(conn, cid, "$185", "r5")
   122	    call = FakeCall(J2("agree"))
   123	    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call, now=7.0)
   124	    assert call.steps() == ["j2"] and "CLASS: charge" in call.log[0]["user"]
   125	    it = r["item"]
   126	    assert r["amount"]["kind"] == "charge" and it["review_status"] == "pending" and it["state"] == "verified"
   127	    assert r["totals"]["pending"]["cents"] == 31000 + 18500 and r["totals"]["accepted"]["cents"] == 0     # counted only after she accepts it
   128	    row = DB.get_item(conn, a, cid)
   129	    assert row["ladder"]["judge"]["verdict"] == "agree" and row["ladder"]["reclassification"]["wording"].lower() == "billed"
   130	    [ev] = events(conn, cid, a)
   131	    assert ev["after"]["judge_verdict"] == "agree" and ev["after"]["wording"].lower() == "billed" and ev["before"]["kind"] == "unclear"
   132	
   133	
   134	@pytest.mark.parametrize("verdict,code,reason", [("disagree", "SHOULD_BE_RATE", "JUDGE_DISAGREES"), ("unsure", "TEXT_AMBIGUOUS", "JUDGE_UNSURE")])
   135	def test_judge_objection_is_422_and_changes_nothing(tmp_path, verdict, code, reason):
   136	    conn, cid = seeded(tmp_path)
   137	    a = aid(conn, cid, "$185", "r5")
   138	    with pytest.raises(RV.ReviewError) as e:
   139	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2(verdict, code)))
   140	    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, reason, "judge")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:46.472Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-bc12d44\" && cat -n tests/unit/test_reclassify.py | sed -n 140,330p",
 "description": "Read test_reclassify.py lines 140-330 at HEAD"
}
````

### User / tool · 2026-11-02T04:41:46.569Z

**tool result**
````
   140	    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, reason, "judge")
   141	    assert e.value.detail["wording"].lower() == "billed" and DB.get_item(conn, a, cid)["kind"] == "unclear" and not events(conn, cid, a)
   142	
   143	
   144	@pytest.mark.parametrize("call", [None, FakeCall(J2("agree", "BAD CODE")), lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed())])
   145	def test_judge_that_cannot_answer_is_422_judge_unavailable(tmp_path, call):
   146	    conn, cid = seeded(tmp_path)
   147	    a = aid(conn, cid, "$185", "r5")
   148	    with pytest.raises(RV.ReviewError) as e:
   149	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
   150	    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and DB.get_item(conn, a, cid)["kind"] == "unclear"
   151	
   152	
   153	def test_unexpected_judge_bug_propagates(tmp_path):
   154	    conn, cid = seeded(tmp_path)
   155	    a = aid(conn, cid, "$185", "r5")
   156	    with pytest.raises(RuntimeError):
   157	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=lambda *x, **k: (_ for _ in ()).throw(RuntimeError("bug")))
   158	    assert DB.get_item(conn, a, cid)["kind"] == "unclear"
   159	
   160	
   161	@pytest.mark.parametrize("rec,text", [("r2", "$185"), ("r6", "$150")])
   162	def test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge(tmp_path, rec, text):
   163	    """Reviewer strings: "Charge per visit $185" and "Billed $150 per visit" state a rate; a rate cue is decisive."""
   164	    conn, cid = seeded(tmp_path)
   165	    a = aid(conn, cid, text, rec)
   166	    call = FakeCall(J2("agree"))
   167	    with pytest.raises(RV.ReviewError) as e:
   168	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
   169	    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
   170	    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)
   171	    assert DB.get_item(conn, a, cid)["state"] == "needs_review"
   172	
   173	
   174	@pytest.mark.parametrize("sentence", [
   175	    "Charge per visit $185.", "Billed $150 per visit.", "Billed $150 per session.", "Charged $40 per hour.", "Billed $40 per day.",
   176	    "Charged $90 each.", "Each visit billed $90.", "Billed $90/visit.", "Billed $90 /session.", "Billed $90 x 3.", "Billed $90 \u00d7 4.",
   177	    "Billed 3 x $90.", "Daily rate billed $400.", "Billed $185 a visit.", "Billed at a rate of $185.", "Billed $90 per-visit.", "Billed $90, per unit."])
   178	def test_rate_cues_are_decisive(sentence):
   179	    ex = "Visit done. " + sentence
   180	    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
   181	    assert RC.charge_wording(ex, {"text": raw, "excerpt_start": None}) is None
   182	
   183	
   184	@pytest.mark.parametrize("sentence", ["Billed $185 for the visit.", "Total billed $185.", "Charged $310.", "Amount due $90 on receipt.", "The visit was billed at $185 in total."])
   185	def test_plain_charge_statements_still_pass_the_wording_check(sentence):
   186	    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;")
   187	    assert RC.charge_wording("Visit done. " + sentence, {"text": raw, "excerpt_start": None}) is not None
   188	
   189	
   190	RATE_R3 = TEXT.replace('Excerpt: "MRI performed. Charge: $310."', 'Excerpt: "MRI performed. Rate of $310 per visit."')
   191	
   192	
   193	def rerun(conn, cid, text):
   194	    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
   195	    PL.run_pipeline(conn, cid, text, call=call, now=lambda: 3.0)
   196	
   197	
   198	def test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again(tmp_path):
   199	    """Reviewer F1: demote $310, rerun with the code now calling it a rate, restore with no judge: 422, the figure stays out of the total."""
   200	    conn, cid = seeded(tmp_path)
   201	    a = aid(conn, cid, "$310", "r3")
   202	    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
   203	    rerun(conn, cid, RATE_R3)
   204	    row = DB.get_item(conn, a, cid)
   205	    assert row["kind"] == "unclear" and row["ladder"]["reclassification"]["rerun"]["code_class"] == "rate"
   206	    n = len(events(conn, cid, a))
   207	    with pytest.raises(RV.ReviewError) as e:
   208	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
   209	    assert (e.value.status, e.value.detail["reason"]) == (422, "NO_CHARGE_WORDING")
   210	    call = FakeCall(J2("agree"))
   211	    with pytest.raises(RV.ReviewError):
   212	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
   213	    assert call.log == []                                                                        # the code check stops it before the judge
   214	    row = DB.get_item(conn, a, cid)
   215	    assert row["kind"] == "unclear" and row["state"] == "needs_review" and len(events(conn, cid, a)) == n
   216	    assert present.totals_view(conn, cid)["pending"]["cents"] == 0
   217	
   218	
   219	def test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again(tmp_path):
   220	    conn, cid = seeded(tmp_path)
   221	    a = aid(conn, cid, "$310", "r3")
   222	    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
   223	    rerun(conn, cid, TEXT.replace("MRI performed. Charge: $310.", "MRI performed. Charge: $310 for the scan."))      # still a charge, different sentence
   224	    assert DB.get_item(conn, a, cid)["ladder"]["reclassification"]["rerun"]["code_class"] == "charge"
   225	    with pytest.raises(RV.ReviewError) as e:
   226	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
   227	    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and DB.get_item(conn, a, cid)["kind"] == "unclear"
   228	    call = FakeCall(J2("agree"))
   229	    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
   230	    assert call.steps() == ["j2"] and r["reclassified"]["restored"] is False and r["amount"]["kind"] == "charge"
   231	
   232	
   233	def test_restore_after_an_unchanged_rerun_still_needs_no_judge(tmp_path):
   234	    conn, cid = seeded(tmp_path)
   235	    a = aid(conn, cid, "$310", "r3")
   236	    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
   237	    rerun(conn, cid, TEXT)
   238	    assert DB.get_item(conn, a, cid)["ladder"]["reclassification"]["rerun"]["code_class"] == "charge"
   239	    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
   240	    assert r["reclassified"]["restored"] is True and r["amount"]["kind"] == "charge"
   241	
   242	
   243	def test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence(tmp_path):
   244	    conn, cid = seeded(tmp_path)
   245	    a = aid(conn, cid, "$185", "r5")
   246	    RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
   247	    rerun(conn, cid, TEXT)                                                                        # same sentence: her class is kept
   248	    assert DB.get_item(conn, a, cid)["kind"] == "charge"
   249	    rerun(conn, cid, TEXT.replace("$185 was billed to the patient.", "$185 was billed to the patient per visit."))
   250	    assert DB.get_item(conn, a, cid)["kind"] != "charge"
   251	
   252	
   253	# ---------------------------------------------------------------- structure
   254	def test_bad_body_non_amount_and_rejected_item(tmp_path):
   255	    conn, cid = seeded(tmp_path)
   256	    a = aid(conn, cid, "$310", "r3")
   257	    for body in ({}, {"to": "rate"}, {"to": "charge", "note": 5}):
   258	        with pytest.raises(RV.ReviewError) as e:
   259	            RC.reclassify(conn, cid, a, body, call=None)
   260	        assert e.value.status == 400
   261	    with pytest.raises(RV.ReviewError) as e:
   262	        RC.reclassify(conn, cid, "e1", {"to": "charge"}, call=None)
   263	    assert (e.value.status, e.value.code) == (422, "invalid_edit")
   264	    with pytest.raises(RV.ReviewError) as e:
   265	        RC.reclassify(conn, cid, "a99", {"to": "charge"}, call=None)
   266	    assert e.value.status == 404
   267	    DB.update_item(conn, a, now=2.0, case=cid, state="rejected")
   268	    with pytest.raises(RV.ReviewError) as e:
   269	        RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
   270	    assert (e.value.status, e.value.code) == (409, "item_rejected")
   271	
   272	
   273	def test_injection_tagged_record_and_missing_value_never_become_charges(tmp_path):
   274	    conn, cid = seeded(tmp_path)
   275	    a = aid(conn, cid, "$185", "r2")
   276	    DB.update_item(conn, a, now=2.0, case=cid, value_cents=None)
   277	    with pytest.raises(RV.ReviewError) as e:
   278	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
   279	    assert e.value.detail["reason"] == "NO_VALUE"
   280	    DB.update_item(conn, a, now=2.0, case=cid, value_cents=18500)
   281	    conn.execute("UPDATE records SET injection_tag='ignore previous instructions' WHERE case_id=? AND id='r2'", (cid,))
   282	    with pytest.raises(RV.ReviewError) as e:
   283	        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
   284	    assert e.value.detail["reason"] == "INJECTION_SUSPECTED"
   285	
   286	
   287	def test_charge_wording_unit():
   288	    ex = "Visit done. Billed $90 for the visit. Rate of $120 per visit. Not billed $50 per visit. Billed $70 per visit."
   289	    row = lambda raw: {"text": raw, "excerpt_start": None}      # noqa: E731
   290	    assert RC.charge_wording(ex, row("$90")).lower() == "billed"
   291	    assert RC.charge_wording(ex, row("$70")) is None            # a rate cue beats the word "billed"
   292	    assert RC.charge_wording(ex, row("$120")) is None
   293	    assert RC.charge_wording(ex, row("$50")) is None
   294	    assert RC.charge_wording("Amount due $40. Rate $40 per visit.", row("$40")) is None      # every occurrence of the figure needs its own wording
   295	
   296	
   297	# ---------------------------------------------------------------- rerun and HTTP
   298	def test_a_rerun_keeps_her_reclassification(tmp_path):
   299	    conn, cid = seeded(tmp_path)
   300	    a = aid(conn, cid, "$310", "r3")
   301	    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
   302	    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
   303	    PL.run_pipeline(conn, cid, TEXT, call=call, now=lambda: 2.0)
   304	    row = DB.get_item(conn, a, cid)
   305	    assert row["kind"] == "unclear" and row["ladder"]["reclassification"]["by"] == "reviewer" and row["state"] == "needs_review"
   306	
   307	
   308	def test_route(tmp_path, monkeypatch):
   309	    monkeypatch.setenv("LLM_BACKEND", "fixture")
   310	    c = TestClient(create_app(str(tmp_path / "h.sqlite"), static_dir=str(tmp_path)), client=("127.0.0.1", 50000))
   311	    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
   312	    assert c.post(f"/api/cases/{tok}/items/a1/reclassify", json={}).status_code == 400
   313	    r = c.post(f"/api/cases/{tok}/items/a1/reclassify", json={"to": "not_a_charge"})
   314	    assert r.status_code == 200 and r.json()["amount"]["kind"] == "unclear" and r.json()["reclassified"]["from"] == "charge"
   315	    r = c.post(f"/api/cases/{tok}/items/a2/reclassify", json={"to": "charge"})              # "Charge per visit $185.": a rate, refused by the code check
   316	    assert r.status_code == 422 and r.json()["error"]["code"] == "reclassify_refused" and r.json()["error"]["detail"]["reason"] == "NO_CHARGE_WORDING"
   317	    assert c.post(f"/api/cases/{tok}/items/a99/reclassify", json={"to": "charge"}).status_code == 404
   318	    ev = [e for e in c.get(f"/api/cases/{tok}/audit").json()["events"] if e["item_id"] == "a1"]
   319	    assert [e["action"] for e in ev] == ["reclassify"]                # T-095: its own audit action (schema v4)
   320	
   321	
   322	def test_judge_unavailable_refusal_names_the_error_class(tmp_path):
   323	    conn, cid = seeded(tmp_path)
   324	    with pytest.raises(RV.ReviewError) as e:
   325	        RC.reclassify(conn, cid, aid(conn, cid, "$185", "r5"), {"to": "charge"}, call=lambda *a, **k: (_ for _ in ()).throw(AU.LLMFailed("down")))
   326	    assert e.value.detail["reason"] == "JUDGE_UNAVAILABLE" and e.value.detail["error_class"] == "LLMFailed"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:54.206Z

The `test_route` assertion expects action `reclassify`, which only works with the uncommitted schema. I'll check whether c8a9874 itself is the commit that introduced the constant, and whether `update_item` commits before the failing `_log`.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:41:57.063Z

**tool call — Bash**
````
{
 "command": "echo \"--- AUDIT_ACTION history in reclassify.py\" && git log --oneline -- app/backend/reclassify.py | head -6 && git show c8a9874 -- app/backend/reclassify.py | grep -n \"AUDIT_ACTION\" ; echo \"--- db.update_item at HEAD\" && SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -n -A12 \"^def update_item\" \"$SP/head-bc12d44/app/db/db.py\" | head -30; echo \"--- commit() / BEGIN in db.py\" && grep -n -E \"commit\\(|BEGIN|isolation_level\" \"$SP/head-bc12d44/app/db/db.py\" | head -20; echo \"--- review.batch_apply\" && grep -n -A6 \"^def batch_apply\" \"$SP/head-bc12d44/app/backend/review.py\" | head -12",
 "description": "Trace the AUDIT_ACTION commit and the db update and commit semantics"
}
````

### User / tool · 2026-11-02T04:41:57.263Z

**tool result**
````
--- AUDIT_ACTION history in reclassify.py
c8a9874 fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
33:-AUDIT_ACTION = "edit"      # review_events.action CHECK has no 'reclassify' yet (db card); the payload's `event` says what it was
34:+AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
71:                  (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))
--- db.update_item at HEAD
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
165-    """Update non-review fields (state, ladder_json, ...). review_status is refused: use apply_review."""
166-    fields = {("ladder_json" if k == "ladder" else k): v for k, v in fields.items()}
167-    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
168-    if locked & set(fields):
169-        raise ValueError(f"{sorted(locked & set(fields))} cannot be written by update_item (edits go through apply_review)")
170-    table, found = _find(conn, item_id, case)
171-    bad = set(fields) - _cols(conn, table)
172-    if bad:
173-        raise ValueError(f"unknown {table} fields {sorted(bad)}")
174-    fields["updated_at"] = now
175-    sets = ", ".join(f"{k}=?" for k in fields)
176-    conn.execute(f"UPDATE {table} SET {sets} WHERE id=? AND case_id=?", [_enc(v) for v in fields.values()] + [item_id, found["case_id"]])
--- commit() / BEGIN in db.py
52:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
191:    conn.execute("BEGIN")
241:    conn.execute("BEGIN")
--- review.batch_apply
397:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float) -> None:
398-    """One audited status change for the batch endpoint (case_extras.apply_batch validates the whole batch first). review.py stays the only
399-    caller of DB.apply_review; there is no code path that accepts amounts or flags in bulk."""
400-    DB.apply_review(conn, item_id, action, now=now, case=case_id)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:08.497Z

Autocommit is on (`isolation_level=None`), so `update_item` commits before the failing audit INSERT. I'll confirm the consequence on the HEAD archive with a route-level probe, and confirm the committed schema at c8a9874 lacks the action.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:09.844Z

**tool call — Bash**
````
{
 "command": "echo \"schema at c8a9874 CHECK has reclassify? -> $(git show c8a9874:app/db/schema.sql | grep -c \"'reclassify'\")\" && echo \"schema at HEAD CHECK has reclassify? -> $(git show HEAD:app/db/schema.sql | grep -c \"'reclassify'\")\" && echo \"schema in working tree CHECK has reclassify? -> $(grep -c \"'reclassify'\" app/db/schema.sql)\" && echo \"PRAGMA/user_version schema in HEAD db.py: $(git show HEAD:app/db/db.py | grep -c 'SCHEMA_VERSION = 4')\" && mkdir -p artifacts/review-evidence/T-073-T-084-r2 && ls artifacts/review-evidence/ | head -30",
 "description": "Confirm schema CHECK state at c8a9874, HEAD, and working tree"
}
````

### User / tool · 2026-11-02T04:42:09.914Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to $)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:12.420Z

**tool call — Bash**
````
{
 "command": "git show c8a9874:app/db/schema.sql | grep -c \"'reclassify'\"; git show HEAD:app/db/schema.sql | grep -c \"'reclassify'\"; grep -c \"'reclassify'\" app/db/schema.sql; git show HEAD:app/db/db.py | grep -n \"SCHEMA_VERSION = \"",
 "description": "Count reclassify CHECK entries in committed and working-tree schema"
}
````

### User / tool · 2026-11-02T04:42:12.576Z

**tool result**
````
0
1
1
33:SCHEMA_VERSION = 4          # bump on EVERY schema.sql change. 1 = global ids (pre T-050); 2 = (case_id, id) keys; 3 = review_events actions += not_duplicate, manual_entry (T-062); 4 = += reclassify, rejudge (T-095; v3 -> v4 is an in-place migration)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:18.359Z

HEAD now shows the reclassify CHECK, which differs from the archive I read earlier. I'll check whether HEAD moved during the review.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:18.987Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log --oneline -6 && git log --oneline -3 -- app/db/schema.sql && git show HEAD:app/db/schema.sql | grep -n \"CHECK (action\" ",
 "description": "Re-check current HEAD and the schema CHECK after possible movement"
}
````

### User / tool · 2026-11-02T04:42:19.230Z

**tool result**
````
a850be0
a850be0 fix: restore T-090 work reverted by 2fca530
6feb2ff fix: restore T-095 work reverted by 2fca530
bc12d44 fix(frontend): side-by-side pane floats over the right margin, flag button in the pane, Enter selects, one record heading (T-046 r2)
c8a9874 fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
d3130e3 harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
6feb2ff fix: restore T-095 work reverted by 2fca530
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
57:  action TEXT NOT NULL CHECK (action IN ('accept','edit','dismiss','reset','confirm_date','keep_my_wording','not_duplicate','manual_entry','reclassify','rejudge')),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:29.857Z

HEAD moved from bc12d44 to a850be0 during the session: 6feb2ff and a850be0 restore the T-095 schema that 2fca530 reverted. I'll pin a850be0 as the review target, check what changed since bc12d44, and keep c8a9874 pinned separately to show the failure at the commit under review.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:31.144Z

**tool call — Bash**
````
{
 "command": "git diff --stat bc12d44 a850be0 | tail -15 && echo \"--- in-scope diffs bc12d44..a850be0\" && git diff --stat bc12d44 a850be0 -- app/backend/judge_guard.py app/backend/reclassify.py app/llm/audited.py app/backend/judges.py app/backend/review.py app/db/ tests/unit/test_audited.py tests/unit/test_judge_guard.py tests/unit/test_reclassify.py tests/unit/test_review_rules.py tests/unit/test_billing.py app/backend/billing.py app/backend/api.py; echo \"exit=$?\"; echo \"--- working tree status of app/db and reclassify\" && git status --short app/db app/backend/reclassify.py app/backend/judge_guard.py app/llm/audited.py | head",
 "description": "Diff HEAD movement since bc12d44 for in-scope files"
}
````

### User / tool · 2026-11-02T04:42:31.318Z

**tool result**
````
 app/backend/rejudge.py         |   8 ++
 app/db/db.py                   |  52 ++++++++++++-
 app/db/schema.sql              |   2 +-
 evals/run.py                   |  88 ++++++++++++++++-----
 tests/unit/test_db.py          |  77 ++++++++++++++++++-
 tests/unit/test_eval_runner.py | 170 ++++++++++++++++++++++++++++++++++++++++-
 tests/unit/test_trace.py       |  16 ++++
 7 files changed, 387 insertions(+), 26 deletions(-)
--- in-scope diffs bc12d44..a850be0
 app/db/db.py      | 52 +++++++++++++++++++++++++++++++++++++++++++++++++---
 app/db/schema.sql |  2 +-
 2 files changed, 50 insertions(+), 4 deletions(-)
exit=0
--- working tree status of app/db and reclassify
 M app/backend/reclassify.py
MM app/db/db.py
MM app/db/schema.sql
 M app/llm/audited.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:35.585Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SP/head-a850be0\" \"$SP/c8a9874\" && cd /Users/arsis/zlayt-pm-project && git archive a850be0 | tar -x -C \"$SP/head-a850be0\" && git archive c8a9874 | tar -x -C \"$SP/c8a9874\" && cd \"$SP/head-a850be0\" && echo \"--- HEAD a850be0: four files\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py 2>&1 | tail -3; echo \"--- HEAD a850be0: test_audited\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_audited.py 2>&1 | tail -2; cd \"$SP/c8a9874\" && echo \"--- c8a9874 (commit under review): four files\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py 2>&1 | tail -3",
 "description": "Archive a850be0 and c8a9874 and run the four test files on each"
}
````

### User / tool · 2026-11-02T04:42:42.301Z

**tool result**
````
--- HEAD a850be0: four files
........................................................................ [ 60%]
................................................                         [100%]
120 passed in 2.44s
--- HEAD a850be0: test_audited
...................                                                      [100%]
19 passed in 0.16s
--- c8a9874 (commit under review): four files
FAILED tests/unit/test_reclassify.py::test_a_rerun_keeps_her_reclassification
FAILED tests/unit/test_reclassify.py::test_route - assert (500 == 200)
9 failed, 111 passed in 2.52s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:45.318Z

The c8a9874 tree fails 9 tests and HEAD a850be0 passes 120. Next I'll run a route-level probe on both trees to see what the paralegal's request does when the audit INSERT fails.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:48.387Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py",
 "content": "\"\"\"Staff-engineer r2 probe (T-084): what a paralegal's reclassify request does on a given tree.\n\nRun from the root of a pinned archive, e.g.:  cd <archive> && PYTHONPATH=. <venv>/bin/python <this file>\nUses the fixture backend and a temporary database only; no network, no real records.\nPrints the HTTP status, the item kind before/after, and the review_events actions written.\n\"\"\"\nimport os\nimport sys\nimport tempfile\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend.api import create_app  # noqa: E402\n\nroot = os.getcwd()\nprint(\"tree:\", root)\ntmp = tempfile.mkdtemp(prefix=\"r2probe_\")\nc = TestClient(create_app(os.path.join(tmp, \"h.sqlite\"), static_dir=tmp), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n\n\ndef item(i):\n    for a in c.get(f\"/api/cases/{tok}\").json()[\"items\"]:\n        if a.get(\"id\") == i:\n            return a\n    return None\n\n\nbefore = item(\"a1\")\nprint(\"a1 before: kind=%s state=%s review_status=%s\" % (before.get(\"kind\"), before.get(\"state\"), before.get(\"review_status\")))\nr = c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={\"to\": \"not_a_charge\"})\nprint(\"POST reclassify a1 -> HTTP\", r.status_code, (r.text[:160] if r.status_code >= 500 else \"\"))\nafter = item(\"a1\")\nprint(\"a1 after:  kind=%s state=%s review_status=%s\" % (after.get(\"kind\"), after.get(\"state\"), after.get(\"review_status\")))\nev = c.get(f\"/api/cases/{tok}/audit\").json().get(\"events\", [])\nprint(\"review_events for a1:\", [e[\"action\"] for e in ev if e.get(\"item_id\") == \"a1\"])\nprint(\"reclassify events:\", sum(1 for e in ev if (e.get(\"after\") or {}).get(\"event\") == \"reclassify\"))\nsys.exit(0)\n"
}
````

### User / tool · 2026-11-02T04:42:48.480Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:51.525Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py && cd \"$SP/c8a9874\" && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" 2>&1 | grep -v \"^  \" | tail -12; echo \"=== a850be0\"; cd \"$SP/head-a850be0\" && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" 2>&1 | tail -8",
 "description": "Run the reclassify route probe on c8a9874 and a850be0 archives"
}
````

### User / tool · 2026-11-02T04:42:52.042Z

**tool result**
````
Traceback (most recent call last):
ModuleNotFoundError: No module named 'app'
=== a850be0
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py", line 14, in <module>
    from app.backend.api import create_app  # noqa: E402
    ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
ModuleNotFoundError: No module named 'app'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:56.268Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py",
 "old_string": "Run from the root of a pinned archive, e.g.:  cd <archive> && PYTHONPATH=. <venv>/bin/python <this file>\nUses the fixture backend and a temporary database only; no network, no real records.\nPrints the HTTP status, the item kind before/after, and the review_events actions written.\n\"\"\"\nimport os\nimport sys\nimport tempfile\n\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend.api import create_app  # noqa: E402\n\nroot = os.getcwd()\nprint(\"tree:\", root)",
 "new_string": "Run as:  <venv>/bin/python -I <this file> <absolute path of the pinned archive root>\nThe archive root is passed as an argument (not via PYTHONPATH or cwd), so -I can be used.\nUses the fixture backend and a temporary database only; no network, no real records.\nPrints the HTTP status, the item kind before/after, and the review_events actions written.\n\"\"\"\nimport os\nimport sys\nimport tempfile\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfrom fastapi.testclient import TestClient  # noqa: E402\n\nfrom app.backend.api import create_app  # noqa: E402\n\nprint(\"tree:\", root)"
}
````

### User / tool · 2026-11-02T04:42:56.357Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:42:59.960Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py && echo \"=== c8a9874 (commit under review)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/c8a9874\" 2>/dev/null | tail -8; echo \"=== a850be0 (HEAD)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>/dev/null | tail -8",
 "description": "Run the reclassify route probe on c8a9874 and a850be0"
}
````

### User / tool · 2026-11-02T04:43:00.893Z

**tool result**
````
=== c8a9874 (commit under review)
tree: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/c8a9874
=== a850be0 (HEAD)
tree: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:03.805Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/c8a9874\" 2>&1 | tail -15",
 "description": "Show full stderr of the probe run on c8a9874"
}
````

### User / tool · 2026-11-02T04:43:04.245Z

**tool result**
````
tree: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/c8a9874
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py", line 32, in <module>
    before = item("a1")
             ^^^^^^^^^^
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py", line 26, in item
    for a in c.get(f"/api/cases/{tok}").json()["items"]:
             ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~^^^^^^^^^
KeyError: 'items'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:09.571Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py",
 "old_string": "tmp = tempfile.mkdtemp(prefix=\"r2probe_\")\nc = TestClient(create_app(os.path.join(tmp, \"h.sqlite\"), static_dir=tmp), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n\n\ndef item(i):\n    for a in c.get(f\"/api/cases/{tok}\").json()[\"items\"]:\n        if a.get(\"id\") == i:\n            return a\n    return None\n\n\nbefore = item(\"a1\")\nprint(\"a1 before: kind=%s state=%s review_status=%s\" % (before.get(\"kind\"), before.get(\"state\"), before.get(\"review_status\")))\nr = c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={\"to\": \"not_a_charge\"})\nprint(\"POST reclassify a1 -> HTTP\", r.status_code, (r.text[:160] if r.status_code >= 500 else \"\"))\nafter = item(\"a1\")\nprint(\"a1 after:  kind=%s state=%s review_status=%s\" % (after.get(\"kind\"), after.get(\"state\"), after.get(\"review_status\")))\nev = c.get(f\"/api/cases/{tok}/audit\").json().get(\"events\", [])\nprint(\"review_events for a1:\", [e[\"action\"] for e in ev if e.get(\"item_id\") == \"a1\"])\nprint(\"reclassify events:\", sum(1 for e in ev if (e.get(\"after\") or {}).get(\"event\") == \"reclassify\"))\nsys.exit(0)",
 "new_string": "from app.db import db as DB  # noqa: E402\n\ntmp = tempfile.mkdtemp(prefix=\"r2probe_\")\ndb_path = os.path.join(tmp, \"h.sqlite\")\nc = TestClient(create_app(db_path, static_dir=tmp), client=(\"127.0.0.1\", 50000))\ntok = c.post(\"/api/cases\", json={\"sample\": True}).json()[\"token\"]\n\n\ndef item(i):\n    conn = DB.connect(db_path)              # a second connection, read-only use: what is actually stored\n    try:\n        return DB.get_item(conn, i, tok)\n    finally:\n        conn.close()\n\n\ndef audit_actions(i):\n    conn = DB.connect(db_path)\n    try:\n        return [(e[\"action\"], (e.get(\"after\") or {}).get(\"event\")) for e in DB.list_events(conn, tok, i)]\n    finally:\n        conn.close()\n\n\nbefore = item(\"a1\")\nprint(\"a1 before: kind=%s state=%s review_status=%s\" % (before[\"kind\"], before[\"state\"], before[\"review_status\"]))\nr = c.post(f\"/api/cases/{tok}/items/a1/reclassify\", json={\"to\": \"not_a_charge\"})\nprint(\"POST reclassify a1 -> HTTP\", r.status_code, (r.text[:160] if r.status_code >= 500 else \"\"))\nafter = item(\"a1\")\nprint(\"a1 stored after request: kind=%s state=%s review_status=%s\" % (after[\"kind\"], after[\"state\"], after[\"review_status\"]))\nprint(\"review_events for a1 (action, payload event):\", audit_actions(\"a1\"))\nsys.exit(0)"
}
````

### User / tool · 2026-11-02T04:43:09.665Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:12.793Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def list_events\\|^def get_item\" app/db/db.py; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_reclassify_audit_route.py && echo \"=== c8a9874 (commit under review)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/c8a9874\" 2>&1 | grep -v \"^tree\" | tail -12; echo \"=== a850be0 (HEAD)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>&1 | grep -v \"^tree\" | tail -12",
 "description": "Rerun the reclassify route probe on both pinned trees with stored-state readout"
}
````

### User / tool · 2026-11-02T04:43:13.593Z

**tool result**
````
191:def get_item(conn, item_id: str, case: str = None) -> dict:
257:def list_events(conn, case_id: str, item_id: str = None) -> list:
=== c8a9874 (commit under review)
unhandled IntegrityError
a1 before: kind=charge state=needs_review review_status=pending
POST reclassify a1 -> HTTP 500 {"error":{"code":"internal","message":"Something went wrong.","detail":{}}}
a1 stored after request: kind=unclear state=needs_review review_status=pending
review_events for a1 (action, payload event): []
=== a850be0 (HEAD)
a1 before: kind=charge state=needs_review review_status=pending
POST reclassify a1 -> HTTP 200 
a1 stored after request: kind=unclear state=needs_review review_status=pending
review_events for a1 (action, payload event): [('reclassify', 'reclassify')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:43.657Z

The probe confirms the blocker at c8a9874 (HTTP 500, stored kind changed from charge to unclear, no audit row), and HEAD a850be0 returns 200 with a `reclassify` row. Next I'll probe whether the rate-cue rule misses unit-price phrasings the brief did not name.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:46.257Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_rate_cue_gaps.py",
 "content": "\"\"\"Staff-engineer r2 probe (T-084): does the code wording gate (charge_wording) refuse rate sentences the brief did not name?\n\nRun as:  <venv>/bin/python -I <this file> <absolute path of the pinned archive root>\nPure function calls on fixed strings (no database, no LLM). A result of None means the code gate REFUSES the figure.\nA non-None result means the code gate PASSES the sentence as charged-amount wording and only the judge stands between it and the total.\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nfrom app.backend import reclassify as RC  # noqa: E402\n\nSENTENCES = [\n    # the brief's two named rate strings (must be refused)\n    \"Charge per visit $185.\", \"Billed $150 per visit.\",\n    # unit-price phrasings without per/each/a visit/rate of\n    \"Charged $150 an hour.\", \"Billed $150 hourly.\", \"Charged $90 apiece.\", \"Billed $40 daily.\",\n    \"Billed $150 for every visit.\", \"Charged $75 a unit.\", \"Billed $200 a month.\", \"Billed $120 an appointment.\",\n    # plain charge statements (must pass)\n    \"Billed $185 for the visit.\", \"Charged $310.\",\n]\nfor s in SENTENCES:\n    ex = \"Visit done. \" + s\n    raw = \"$\" + s.split(\"$\")[1].split()[0].rstrip(\".,;\")\n    got = RC.charge_wording(ex, {\"text\": raw, \"excerpt_start\": None})\n    print(\"%-32s -> %s\" % (s, \"REFUSED by code (None)\" if got is None else \"PASSES code gate (%r)\" % got))\n"
}
````

### User / tool · 2026-11-02T04:43:46.383Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_rate_cue_gaps.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:43:49.212Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_rate_cue_gaps.py && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/rate-cue-gaps-run.txt",
 "description": "Run the rate-cue coverage probe on the HEAD a850be0 archive"
}
````

### User / tool · 2026-11-02T04:43:49.516Z

**tool result**
````
Charge per visit $185.           -> REFUSED by code (None)
Billed $150 per visit.           -> REFUSED by code (None)
Charged $150 an hour.            -> PASSES code gate ('Charged')
Billed $150 hourly.              -> PASSES code gate ('Billed')
Charged $90 apiece.              -> PASSES code gate ('Charged')
Billed $40 daily.                -> PASSES code gate ('Billed')
Billed $150 for every visit.     -> REFUSED by code (None)
Charged $75 a unit.              -> PASSES code gate ('Charged')
Billed $200 a month.             -> PASSES code gate ('Billed')
Billed $120 an appointment.      -> PASSES code gate ('Billed')
Billed $185 for the visit.       -> PASSES code gate ('Billed')
Charged $310.                    -> PASSES code gate ('Charged')
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:44:02.511Z

The gate misses six unit-price phrasings the brief did not name (hourly, an hour, apiece, daily, a unit, a month, an appointment), so the judge is the only gate for those. Next I'll run a mutation harness on a scratch copy of a850be0, covering the rate-cue rule, the restore rules, the carry-over rule, and the T-073 seams.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:44:09.818Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py",
 "content": "\"\"\"Staff-engineer r2 scratch mutants (T-073, T-084). Each mutant is applied to a fresh copy of a pinned archive (never to the project tree\nand never committed). Every replacement must match exactly once, or the mutant is reported as NOT APPLIED.\n\nUsage: <venv>/bin/python <this file> <absolute path of the pinned archive root> <absolute path of an empty scratch dir>\n\"\"\"\nimport os\nimport re\nimport shutil\nimport subprocess\nimport sys\n\nARCHIVE, SCRATCH = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nTESTS = [\"tests/unit/test_reclassify.py\", \"tests/unit/test_judge_guard.py\", \"tests/unit/test_review_rules.py\",\n         \"tests/unit/test_billing.py\", \"tests/unit/test_audited.py\"]\n\nMUTANTS = [\n    (\"control\", \"no mutation\", None, None, None),\n    # ---- T-084: rate-cue rule and restore / carry-over rules\n    (\"T84-1 rate cue removed from the wording gate\", \"app/backend/reclassify.py\",\n     \"if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent):\", \"if not m or _NEGATED.search(sent):\", None),\n    (\"T84-2 'per' removed from the rate-cue pattern\", \"app/backend/reclassify.py\",\n     r're.compile(r\"\\bper\\b|\\beach\\b', r're.compile(r\"\\beach\\b', None),\n    (\"T84-3 restore ignores the rerun's code class\", \"app/backend/reclassify.py\",\n     'return rerun.get(\"code_class\") == \"charge\" and rerun.get(\"excerpt_sha\") == prior.get(\"excerpt_sha\") == _sha(row[\"excerpt\"])',\n     'return rerun.get(\"excerpt_sha\") == prior.get(\"excerpt_sha\") == _sha(row[\"excerpt\"])', None),\n    (\"T84-4 restore ignores whether the sentence changed\", \"app/backend/reclassify.py\",\n     'return rerun.get(\"code_class\") == \"charge\" and rerun.get(\"excerpt_sha\") == prior.get(\"excerpt_sha\") == _sha(row[\"excerpt\"])',\n     'return rerun.get(\"code_class\") == \"charge\"', None),\n    (\"T84-5 restore always skips the checks (the r1 F1 bug)\", \"app/backend/reclassify.py\",\n     \"restored = _may_restore(row, prior, original)\", 'restored = original == \"charge\" and prior.get(\"previous_judge\") is not None', None),\n    (\"T84-6 promoted charge kept when its sentence changes\", \"app/backend/reclassify.py\",\n     'if rc.get(\"to\") == \"charge\" and rc.get(\"excerpt_sha\") != _sha(it.get(\"excerpt\")):', \"if False:\", None),\n    # ---- T-073: retry set, bug propagation, error class\n    (\"T73-1 every exception retried (broad provider catch)\", \"app/llm/audited.py\",\n     \"RETRYABLE_PROVIDER_ERRORS = (P.LLMError, TimeoutError, ConnectionError)\",\n     \"RETRYABLE_PROVIDER_ERRORS = (P.LLMError, TimeoutError, ConnectionError, Exception)\", None),\n    (\"T73-2 programmer error recorded but not re-raised\", \"app/llm/audited.py\",\n     \"            raise bug\\n\", \"            pass\\n\", None),\n    (\"T73-3 guard does not note the expected error's class\", \"app/backend/judge_guard.py\",\n     '        kwargs[\"call\"] = noting\\n', \"        pass\\n\", None),\n    (\"T73-4 guard catches every exception as expected\", \"app/backend/judge_guard.py\",\n     \"EXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError)\", \"EXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError, Exception)\", None),\n]\n\n\ndef apply(src_root, dst_root, rel, old, new):\n    p = os.path.join(dst_root, rel)\n    s = open(p, encoding=\"utf-8\").read()\n    n = s.count(old)\n    if n != 1:\n        return False, n\n    open(p, \"w\", encoding=\"utf-8\").write(s.replace(old, new, 1))\n    return True, 1\n\n\ndef run_tests(root):\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", *TESTS], cwd=root, capture_output=True, text=True)\n    summary = [ln for ln in r.stdout.splitlines() if re.search(r\"\\d+ (passed|failed)\", ln)]\n    failed = sorted({ln.split(\"::\", 1)[1].split(\" \")[0] for ln in r.stdout.splitlines() if ln.startswith(\"FAILED \")})\n    return (summary[-1] if summary else \"NO SUMMARY (rc=%s)\" % r.returncode), failed\n\n\nprint(\"archive:\", ARCHIVE)\nfor i, (name, rel, old, new, _x) in enumerate(MUTANTS):\n    dst = os.path.join(SCRATCH, \"m%02d\" % i)\n    if os.path.exists(dst):\n        shutil.rmtree(dst)\n    shutil.copytree(ARCHIVE, dst, symlinks=True)\n    if old is None:\n        summary, failed = run_tests(dst)\n        print(\"[%s] %s\\n    %s\" % (name, rel or \"\", summary))\n        continue\n    ok, n = apply(ARCHIVE, dst, rel, old, new)\n    if not ok:\n        print(\"[%s] NOT APPLIED (matches=%d)\" % (name, n))\n        continue\n    summary, failed = run_tests(dst)\n    print(\"[%s] in %s\\n    %s\" % (name, rel, summary))\n    for f in failed[:12]:\n        print(\"    FAILED\", f)\n"
}
````

### User / tool · 2026-11-02T04:44:09.924Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:44:13.105Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SP/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py \"$SP/head-a850be0\" \"$SP/mut\" 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/mutation-run-r2.txt",
 "description": "Run the scratch mutants against the a850be0 archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:44:51.258Z

**tool result**
````
archive: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0
[control] no mutation
    139 passed in 2.60s
[T84-1 rate cue removed from the wording gate] in app/backend/reclassify.py
    21 failed, 118 passed in 2.90s
    FAILED test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge[r2-$185]
    FAILED test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge[r6-$150]
    FAILED test_charge_wording_unit
    FAILED test_rate_cues_are_decisive[Billed
    FAILED test_rate_cues_are_decisive[Charge
    FAILED test_rate_cues_are_decisive[Charged
    FAILED test_rate_cues_are_decisive[Daily
    FAILED test_rate_cues_are_decisive[Each
    FAILED test_route
[T84-2 'per' removed from the rate-cue pattern] in app/backend/reclassify.py
    11 failed, 128 passed in 2.60s
    FAILED test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge[r2-$185]
    FAILED test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge[r6-$150]
    FAILED test_charge_wording_unit
    FAILED test_rate_cues_are_decisive[Billed
    FAILED test_rate_cues_are_decisive[Charge
    FAILED test_rate_cues_are_decisive[Charged
    FAILED test_route
[T84-3 restore ignores the rerun's code class] in app/backend/reclassify.py
    139 passed in 2.65s
[T84-4 restore ignores whether the sentence changed] in app/backend/reclassify.py
    1 failed, 138 passed in 2.73s
    FAILED test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again
[T84-5 restore always skips the checks (the r1 F1 bug)] in app/backend/reclassify.py
    2 failed, 137 passed in 2.89s
    FAILED test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again
    FAILED test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again
[T84-6 promoted charge kept when its sentence changes] in app/backend/reclassify.py
    1 failed, 138 passed in 2.83s
    FAILED test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence
[T73-1 every exception retried (broad provider catch)] in app/llm/audited.py
    8 failed, 131 passed in 2.76s
    FAILED test_a_bug_in_the_provider_adapter_propagates_through_the_real_audited_call_and_the_guard
    FAILED test_a_bug_in_the_provider_adapter_through_apply_review_raises_and_saves_nothing
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug0]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug1]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug2]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug3]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug4]
    FAILED test_a_type_error_inside_validate_is_a_bug_and_propagates
[T73-2 programmer error recorded but not re-raised] in app/llm/audited.py
    8 failed, 131 passed in 2.75s
    FAILED test_a_bug_in_the_provider_adapter_propagates_through_the_real_audited_call_and_the_guard
    FAILED test_a_bug_in_the_provider_adapter_through_apply_review_raises_and_saves_nothing
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug0]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug1]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug2]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug3]
    FAILED test_a_programmer_error_from_the_provider_call_is_not_retried_and_propagates[bug4]
    FAILED test_a_type_error_inside_validate_is_a_bug_and_propagates
[T73-3 guard does not note the expected error's class] in app/backend/judge_guard.py
    5 failed, 134 passed in 2.74s
    FAILED test_edit_records_error_class_on_the_ladder_for_every_expected_failure[exc0-LLMFailed]
    FAILED test_edit_records_error_class_on_the_ladder_for_every_expected_failure[exc1-LLMFailedFixtureMiss]
    FAILED test_judge_unavailable_refusal_names_the_error_class
    FAILED test_llmfailed_is_returned_with_its_class_even_though_judges_run_swallows_it
    FAILED test_provider_failure_through_the_real_audited_call_records_llmfailed
[T73-4 guard catches every exception as expected] in app/backend/judge_guard.py
    7 failed, 132 passed in 2.82s
    FAILED test_a_bug_in_the_provider_adapter_propagates_through_the_real_audited_call_and_the_guard
    FAILED test_a_bug_in_the_provider_adapter_through_apply_review_raises_and_saves_nothing
    FAILED test_edit_with_unexpected_error_propagates_and_saves_nothing
    FAILED test_guard_does_not_swallow_unexpected_errors[exc0]
    FAILED test_guard_does_not_swallow_unexpected_errors[exc1]
    FAILED test_guard_does_not_swallow_unexpected_errors[exc2]
    FAILED test_unexpected_judge_bug_propagates
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:22.774Z

Most mutants die, with one surviving: dropping the restore's code-class check (T84-3) leaves all 139 tests green. I'll confirm that gap with a same-sentence class flip, check the D-042 wording, and run the full unit suite at a850be0.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:23.651Z

**tool call — Bash**
````
{
 "command": "grep -n \"^- \\*\\*D-042\\|D-042\" memory/ORCHESTRATOR_DECISIONS.md | head -5; echo \"---\"; grep -n \"classify\" app/backend/amounts.py | head -8; echo \"--- pipeline uses\"; grep -n \"amounts\\.\\|from app.backend import.*amounts\\|amounts import\" app/backend/pipeline.py | head -8",
 "description": "Locate D-042 text and the amount classifier used by the pipeline"
}
````

### User / tool · 2026-11-02T04:45:23.776Z

**tool result**
````
50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
---
1:"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
20:# ONE rate-cue test for every code path that decides "is this figure a unit price?" (reclassify.py wording gate, billing.py ledger rows and
67:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
139:        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
--- pipeline uses
14:from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
102:    """The pipeline's amount item from an amounts.extract_amounts row and its record."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:30.027Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && sed -n 15,30p app/backend/amounts.py && echo \"--- rate cue uses\" && grep -rn \"RATE_CUE\\|rate_cue\" app/ | head -20",
 "description": "Read amounts.py rate-cue comment and find all rate-cue definitions"
}
````

### User / tool · 2026-11-02T04:45:30.133Z

**tool result**
````
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)

--- rate cue uses
app/backend/reclassify.py:31:_RATE_CUE = re.compile(r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
app/backend/reclassify.py:74:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:34.346Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && sed -n 1,14p app/backend/amounts.py && echo \"--- lines 18-22\" && sed -n 18,22p app/backend/amounts.py | cut -c1-400",
 "description": "Read amounts.py header and the unit vocabulary"
}
````

### User / tool · 2026-11-02T04:45:34.439Z

**tool result**
````
"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import re

from app.backend import injection, lexicon

# '$' + a whole numeric token (extra decimals are kept so to_cents can refuse them: never truncated).
# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]+)?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?\Z")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
# Rate = unit-rate phrasing only. 'Charge per invoice 4471: $400' is NOT a rate (per + a non-unit noun stays a charge or unclear).
_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
--- lines 18-22
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:38.335Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && grep -n \"^def \" app/backend/amounts.py",
 "description": "List function signatures in amounts.py"
}
````

### User / tool · 2026-11-02T04:45:38.425Z

**tool result**
````
23:def to_cents(figure: str):
32:def find_amounts(excerpt: str) -> list:
45:def _label(excerpt: str, start: int) -> str:
51:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
72:def _is_billing_source(source: str) -> bool:
76:def damages_mentions(excerpt: str) -> list:
90:def _norm(s):
94:def dedupe_amounts(amounts: list, separate=frozenset()) -> list:
114:def extract_amounts(records: list, separate=frozenset()) -> list:
144:def _prefix(source):
148:def rate_note(records: list, record_no: int) -> dict:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:42.206Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_classifier_vs_wording_gate.py",
 "content": "\"\"\"Staff-engineer r2 probe (T-084): does the amount CLASSIFIER (amounts.classify, which sets rate/charge on ingest) agree with the\nreclassify WORDING GATE (reclassify.charge_wording) on the same sentences?\n\nRun as:  <venv>/bin/python -I <this file> <absolute path of the pinned archive root>\nPure function calls on fixed strings (no database, no LLM). A sentence the classifier calls a rate but the wording gate PASSES is a\ndisagreement: the paralegal can promote it with one judge answer.\n\"\"\"\nimport os\nimport sys\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nfrom app.backend import amounts as AM, reclassify as RC  # noqa: E402\n\nSENTENCES = [\n    \"Charge per visit $185.\", \"Billed $150 per visit.\",\n    \"Charged $150 an hour.\", \"Billed $150 hourly.\", \"Charged $90 apiece.\", \"Billed $40 daily.\",\n    \"Billed $150 for every visit.\", \"Charged $75 a unit.\", \"Billed $200 a month.\", \"Billed $120 an appointment.\",\n    \"Billed $185 for the visit.\", \"Charged $310.\",\n]\nprint(\"%-30s %-10s %-24s\" % (\"sentence\", \"classifier\", \"wording gate\"))\nfor s in SENTENCES:\n    ex = \"Visit done. \" + s\n    found = AM.find_amounts(ex)\n    a = next(x for x in found if x.get(\"text\", \"\").startswith(\"$\") or \"$\" in str(x.get(\"raw\", x.get(\"text\", \"\"))))\n    cls = AM.classify(ex, a)\n    raw = \"$\" + s.split(\"$\")[1].split()[0].rstrip(\".,;\")\n    got = RC.charge_wording(ex, {\"text\": raw, \"excerpt_start\": None})\n    gate = \"None (refused)\" if got is None else \"passes (%s)\" % got\n    flag = \"  <-- DISAGREES\" if cls == \"rate\" and got is not None else \"\"\n    print(\"%-30s %-10s %-24s%s\" % (s, cls, gate, flag))\n"
}
````

### User / tool · 2026-11-02T04:45:42.412Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_classifier_vs_wording_gate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:45.442Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_classifier_vs_wording_gate.py && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/classifier-vs-gate-run.txt",
 "description": "Run classifier-vs-wording-gate probe on the HEAD archive"
}
````

### User / tool · 2026-11-02T04:45:45.831Z

**tool result**
````
sentence                       classifier wording gate            
Charge per visit $185.         rate       None (refused)          
Billed $150 per visit.         rate       None (refused)          
Charged $150 an hour.          rate       passes (Charged)          <-- DISAGREES
Billed $150 hourly.            charge     passes (Billed)         
Charged $90 apiece.            unclear    passes (Charged)        
Billed $40 daily.              charge     passes (Billed)         
Billed $150 for every visit.   charge     None (refused)          
Charged $75 a unit.            rate       passes (Charged)          <-- DISAGREES
Billed $200 a month.           charge     passes (Billed)         
Billed $120 an appointment.    rate       passes (Billed)           <-- DISAGREES
Billed $185 for the visit.     charge     passes (Billed)         
Charged $310.                  unclear    passes (Charged)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:56.591Z

The classifier calls "Charged $150 an hour", "Charged $75 a unit" and "Billed $120 an appointment" rates, while the wording gate passes all three. The working tree has an uncommitted amounts.py comment about a shared rate-cue, so I'll check what that uncommitted edit is before I write this up.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:45:57.354Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend/amounts.py app/backend/reclassify.py app/backend/billing.py app/backend/judge_guard.py app/llm/audited.py tests/unit/test_reclassify.py tests/unit/test_audited.py tests/unit/test_judge_guard.py | tail -8; echo \"--- working-tree reclassify.py diff (first 40 lines)\"; git diff -- app/backend/reclassify.py | head -40",
 "description": "Check uncommitted working-tree edits to the in-scope files"
}
````

### User / tool · 2026-11-02T04:45:57.496Z

**tool result**
````
 app/backend/amounts.py    |  16 ++++
 app/backend/billing.py    | 233 ++++++++++++++++++++++++++++++++++------------
 app/backend/reclassify.py |   6 +-
 app/llm/audited.py        |   2 +-
 4 files changed, 193 insertions(+), 64 deletions(-)
--- working-tree reclassify.py diff (first 40 lines)
diff --git a/app/backend/reclassify.py b/app/backend/reclassify.py
index d2fd369..0044dd3 100644
--- a/app/backend/reclassify.py
+++ b/app/backend/reclassify.py
@@ -19,7 +19,7 @@ import re
 
 from fastapi import Request
 
-from app.backend import confidence, generator, judge_guard, judges, review, store, why as WHY
+from app.backend import amounts as A, confidence, generator, judge_guard, judges, review, store, why as WHY
 from app.db import db as DB
 
 TARGETS = ("charge", "not_a_charge")
@@ -28,9 +28,7 @@ AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
 _BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
 _WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
 # a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
-_RATE_CUE = re.compile(r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
-                       r"|\ba\s+(?:visit|session|hour|day|treatment|appointment)\b|\b(?:daily|hourly|session|visit|unit|flat)\s+(?:rate|fee|price)\b|\brate\b"
-                       r"|(?<![\w$])[x\u00d7]\s*\d+\b|\b\d+\s*[x\u00d7]\s*\$?\d", re.IGNORECASE)
+_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
 _NEGATED = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)
 
 REFUSALS = {
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:04.756Z

The uncommitted working tree already moves reclassify onto a shared `amounts.RATE_CUE`, so that gap is in flight but not reviewed here. Next I'll show the surviving mutant as a real behaviour gap: a same-sentence class flip on rerun, then restore with no judge.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:10.191Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py",
 "content": "\"\"\"Staff-engineer r2 probe (T-084): restore after a rerun that changes the code's CLASS of a figure while its SENTENCE is unchanged.\n\nRun as:  <venv>/bin/python -I <this file> <absolute path of the pinned archive root>\nFixture backend, temporary database, no network, no real records. The rerun's classifier is patched (amounts.classify returns \"rate\" for\n$310) to simulate a classifier or lexicon change on rerun; the excerpt text stays identical.\nExpected under the design (D-042, T-084 r2): the restore runs both checks again, so with no judge available it is refused with 422\nJUDGE_UNAVAILABLE, the item stays `unclear`, and no reclassify event is written.\n\"\"\"\nimport os\nimport sys\nimport tempfile\n\nroot = os.path.abspath(sys.argv[1])\nsys.path.insert(0, root)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"\nfrom app.backend import amounts as AM, pipeline as PL  # noqa: E402\nfrom app.backend import reclassify as RC, review as RV, present  # noqa: E402\nfrom app.db import db as DB  # noqa: E402\nfrom tests.unit._fakes import FakeCall, sample_script  # noqa: E402\n\nTEXT = \"\"\"=== Record 1 ===\nDate: 2026-03-02\nSource: Capital PT, visit 1\nExcerpt: \"Visit completed. Rate of $185 per visit.\"\n\n=== Record 2 ===\nDate: 2026-03-09\nSource: Capital PT, visit 2\nExcerpt: \"Visit completed. Charge per visit $185.\"\n\n=== Record 3 ===\nDate: 2026-03-16\nSource: Capital Imaging\nExcerpt: \"MRI performed. Charge: $310.\"\n\"\"\"\n\n\ndef run(conn, cid, text, now):\n    call = FakeCall(sample_script(extract=lambda u: dict(summary=\"Visit completed.\", excerpt=\"Visit completed.\")))\n    PL.run_pipeline(conn, cid, text, call=call, now=lambda: now)\n\n\ntmp = tempfile.mkdtemp(prefix=\"r2flip_\")\nconn = DB.connect(os.path.join(tmp, \"f.sqlite\"))\ncid = DB.create_case(conn, TEXT, now=1.0)\nrun(conn, cid, TEXT, 1.0)\na = next(x[\"id\"] for x in DB.list_items(conn, cid, \"amount\") if x[\"text\"] == \"$310\")\nprint(\"tree:\", root)\nprint(\"1. seeded: $310 kind =\", DB.get_item(conn, a, cid)[\"kind\"])\nRC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\nprint(\"2. demoted: kind =\", DB.get_item(conn, a, cid)[\"kind\"])\n\nreal_classify = AM.classify\n\n\ndef flipped(excerpt, amount, *args, **kwargs):\n    return \"rate\" if amount.get(\"text\") == \"$310\" or \"$310\" in str(amount.get(\"text\", \"\")) else real_classify(excerpt, amount, *args, **kwargs)\n\n\nAM.classify = flipped\ntry:\n    run(conn, cid, TEXT, 3.0)            # same text, same sentence; only the code's class of $310 changes\nfinally:\n    AM.classify = real_classify\nrow = DB.get_item(conn, a, cid)\nprint(\"3. after rerun: kind =\", row[\"kind\"], \"| rerun marker =\", row[\"ladder\"][\"reclassification\"].get(\"rerun\"))\nn_before = len([e for e in DB.list_events(conn, cid, a) if (e.get(\"after\") or {}).get(\"event\") == \"reclassify\"])\ntry:\n    r = RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=None)\n    print(\"4. restore with no judge: HTTP 200 restored=%s kind=%s  <-- restore skipped both checks\" % (r[\"reclassified\"][\"restored\"], r[\"amount\"][\"kind\"]))\nexcept RV.ReviewError as e:\n    print(\"4. restore with no judge: %s %s reason=%s\" % (e.status, e.code, e.detail.get(\"reason\")))\nrow = DB.get_item(conn, a, cid)\nn_after = len([e for e in DB.list_events(conn, cid, a) if (e.get(\"after\") or {}).get(\"event\") == \"reclassify\"])\nprint(\"5. stored kind =\", row[\"kind\"], \"| reclassify events before/after =\", n_before, n_after)\nprint(\"   pending total cents =\", present.totals_view(conn, cid)[\"pending\"][\"cents\"])\n"
}
````

### User / tool · 2026-11-02T04:46:10.284Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:13.649Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py && echo \"=== HEAD a850be0 (current code)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>&1 | tail -12; echo \"=== scratch mutant T84-3 (restore ignores the code class)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/mut/m04\" 2>&1 | tail -12",
 "description": "Run the class-only flip restore probe on HEAD and on the T84-3 mutant"
}
````

### User / tool · 2026-11-02T04:46:14.688Z

**tool result**
````
=== HEAD a850be0 (current code)
tree: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0
1. seeded: $310 kind = charge
2. demoted: kind = unclear
3. after rerun: kind = unclear | rerun marker = {'code_class': 'charge', 'excerpt_sha': '1c9760cf18fb99fc'}
4. restore with no judge: HTTP 200 restored=True kind=charge  <-- restore skipped both checks
5. stored kind = charge | reclassify events before/after = 1 2
   pending total cents = 31000
=== scratch mutant T84-3 (restore ignores the code class)
tree: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/m04
1. seeded: $310 kind = charge
2. demoted: kind = unclear
3. after rerun: kind = unclear | rerun marker = {'code_class': 'charge', 'excerpt_sha': '1c9760cf18fb99fc'}
4. restore with no judge: HTTP 200 restored=True kind=charge  <-- restore skipped both checks
5. stored kind = charge | reclassify events before/after = 1 2
   pending total cents = 31000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:18.604Z

The probe patch did not take effect (the rerun marker still says charge), and I pointed at m04, which is T84-4, not T84-3. I'll fix both and rerun.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:19.411Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py",
 "old_string": "def flipped(excerpt, amount, *args, **kwargs):\n    return \"rate\" if amount.get(\"text\") == \"$310\" or \"$310\" in str(amount.get(\"text\", \"\")) else real_classify(excerpt, amount, *args, **kwargs)",
 "new_string": "def flipped(excerpt, amount, *args, **kwargs):\n    return \"rate\" if \"$310\" in excerpt else real_classify(excerpt, amount, *args, **kwargs)"
}
````

### User / tool · 2026-11-02T04:46:19.513Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:23.047Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && PROBE=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/probe_restore_class_only_flip.py && echo \"=== HEAD a850be0 (current code)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/head-a850be0\" 2>&1 | grep -v \"^tree\" | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/restore-class-only-flip-run.txt; echo \"=== scratch mutant T84-3 (m03: restore ignores the code class)\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$PROBE\" \"$SP/mut/m03\" 2>&1 | grep -v \"^tree\" | tee -a /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084-r2/restore-class-only-flip-run.txt",
 "description": "Rerun the class-only flip probe on HEAD and the T84-3 mutant and save output"
}
````

### User / tool · 2026-11-02T04:46:24.082Z

**tool result**
````
=== HEAD a850be0 (current code)
1. seeded: $310 kind = charge
2. demoted: kind = unclear
3. after rerun: kind = unclear | rerun marker = {'code_class': 'rate', 'excerpt_sha': '1c9760cf18fb99fc'}
4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE
5. stored kind = unclear | reclassify events before/after = 1 1
   pending total cents = 0
=== scratch mutant T84-3 (m03: restore ignores the code class)
1. seeded: $310 kind = charge
2. demoted: kind = unclear
3. after rerun: kind = unclear | rerun marker = {'code_class': 'rate', 'excerpt_sha': '1c9760cf18fb99fc'}
4. restore with no judge: HTTP 200 restored=True kind=charge  <-- restore skipped both checks
5. stored kind = charge | reclassify events before/after = 1 2
   pending total cents = 31000
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:27.227Z

The class-only flip is now confirmed: HEAD refuses the restore with 422, and the T84-3 mutant restores into the total at 31000 cents while the suite stays green. Next I'll run the full unit suite on the pinned HEAD.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:29.147Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && timeout 580 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -6",
 "description": "Run the full unit suite on the pinned HEAD a850be0 archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:46:29.234Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:46:31.902Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | tail -6",
 "description": "Run the full unit suite on the pinned HEAD a850be0 archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:47:12.663Z

**tool result**
````
FAILED tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2
FAILED tests/unit/test_trace.py::test_every_item_has_an_ordered_well_formed_trace
FAILED tests/unit/test_trace.py::test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them
FAILED tests/unit/test_trace.py::test_every_emitted_reason_code_has_a_fixed_sentence
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
7 failed, 1392 passed, 2 skipped in 39.31s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:47:16.188Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit 2>&1 | grep -E \"^FAILED|^E  \" | head -30",
 "description": "List the seven failing unit tests at HEAD with their first assertion lines",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:47:56.925Z

**tool result**
````
E       AssertionError: ['sbs-flags', 'sbs-show-flag']
E       assert not ['sbs-flags', 'sbs-show-flag']
E       AssertionError: ude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0/app/backend/pipeline.py", line 501, in main
E             language.case_check(language.annotate(IN.ingest(raw)["records"]))
E                                                             ^^^
E         UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value
E         
E       assert (1 == 0)
E        +  where 1 = CompletedProcess(args=['/Users/arsis/zlayt-pm-project/.venv/bin/python', '-m', 'app.pipeline', 'evals/golden/sample.tx...               ^^^\nUnboundLocalError: cannot access local variable \'raw\' where it is not associated with a value\n').returncode
E       AssertionError: assert ('judge_conflict_v3' == 'judge_conflict_v2'
E         
E         - judge_conflict_v2
E         ?                 ^
E         + judge_conflict_v3
E         ?                 ^)
E           AssertionError: f_cx1
E           assert 500 == 200
E            +  where 500 = <Response [500 Internal Server Error]>.status_code
E           KeyError: 'mode'
E                   KeyError: 'steps'
E           KeyError: 'steps'
FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
FAILED tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s
FAILED tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2
FAILED tests/unit/test_trace.py::test_every_item_has_an_ordered_well_formed_trace
FAILED tests/unit/test_trace.py::test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them
FAILED tests/unit/test_trace.py::test_every_emitted_reason_code_has_a_fixed_sentence
FAILED tests/unit/test_trace.py::test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:05.657Z

Seven unit tests fail at HEAD, all outside the two cards except that the CLI test fails on a pipeline.py line. I'll confirm the CLI failure directly, check the billing count, and see whether the r1 probes can rerun against HEAD.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:07.969Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && echo \"--- CLI sample at HEAD\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.pipeline evals/golden/sample.txt 2>&1 | tail -3; echo \"rc=$?\"; echo \"--- billing tests at HEAD\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_billing.py 2>&1 | tail -1; echo \"--- r1 probe path header\" && head -12 /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py",
 "description": "Run the sample CLI and billing tests at HEAD and read the r1 probe header",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T04:48:08.862Z

**tool result**
````
--- CLI sample at HEAD
    language.case_check(language.annotate(IN.ingest(raw)["records"]))
                                                    ^^^
UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value
rc=0
--- billing tests at HEAD
27 passed in 0.36s
--- r1 probe path header
from app.backend import review as RV
from app.db import db as DB
from app.llm import audited as AU
from tests.unit.test_review_rules import ent, seeded

def _bug(*a, **k):
    raise RuntimeError("programmer bug in provider adapter")

def test_probe_real_path_bug_is_hidden(tmp_path):
    conn, cid, out = seeded(tmp_path)
    eid = ent(out, 5)
    calls = []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:18.460Z

The sample CLI crashes at HEAD with an UnboundLocalError, and billing's 27 tests pass. I'll pin the exact line numbers I plan to cite and find which commit restored the T-095 schema.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:21.917Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && grep -n \"_RATE_CUE\\|def charge_wording\\|if not m or\\|def _may_restore\\|return rerun.get\\|def carry_over\\|if rc.get(\\\"to\\\")\\|return it$\\|def _log\\|AUDIT_ACTION = \\|DB.update_item(conn, item_id\\|_log(conn, case_id, item_id, before\\|batch_apply(conn, case_id, item_id, \\\"reset\\\"\\|restored = _may_restore\\|if not restored\" app/backend/reclassify.py && echo \"--- judge_guard\" && grep -n \"EXPECTED_JUDGE_ERRORS\\|kwargs\\[\\\"call\\\"\\] = noting\\|def guarded\\|except EXPECTED\" app/backend/judge_guard.py && echo \"--- audited\" && grep -n \"RETRYABLE_PROVIDER_ERRORS =\\|RETRYABLE_VALIDATION_ERRORS =\\|except RETRYABLE_PROVIDER_ERRORS\\|except Exception as e\\|raise bug\\|MAX_ATTEMPTS = \\|RETRY_DELAYS_S = \" app/llm/audited.py && echo \"--- restore commit\" && cd /Users/arsis/zlayt-pm-project && git show --stat --format='%h %s' 6feb2ff | head -4 && git show --stat --format='%h %s' a850be0 | head -3 && echo \"--- blame pipeline.py CLI raw\" && git blame -L 496,502 a850be0 -- app/backend/pipeline.py | cut -c1-120",
 "description": "Pin line numbers for citations and identify restore and CLI blame commits"
}
````

### User / tool · 2026-11-02T04:48:22.239Z

**tool result**
````
27:AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
31:_RATE_CUE = re.compile(r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
66:def charge_wording(excerpt: str, row: dict, rec=None):
74:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent):
89:def _log(conn, case_id, item_id, before, after, t):
116:        restored = _may_restore(row, prior, original)
117:        if not restored:
135:    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
137:        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
138:    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
145:def _may_restore(row: dict, prior: dict, original: str) -> bool:
153:    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])
183:def carry_over(old: dict, it: dict) -> dict:
187:        return it
188:    if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(it.get("excerpt")):      # her promotion was checked against another sentence
189:        return it
--- judge_guard
8:EXPECTED_JUDGE_ERRORS = (AU.LLMFailed, P.LLMError)
11:def guarded(fn, *args, **kwargs):
20:            except EXPECTED_JUDGE_ERRORS as e:
23:        kwargs["call"] = noting
26:    except EXPECTED_JUDGE_ERRORS as e:
--- audited
15:MAX_ATTEMPTS = 3
17:RETRY_DELAYS_S = (0.5, 1.5)
21:RETRYABLE_PROVIDER_ERRORS = (P.LLMError, TimeoutError, ConnectionError)
22:RETRYABLE_VALIDATION_ERRORS = (ValueError,)
88:        except RETRYABLE_PROVIDER_ERRORS as e:          # only our own error codes are stored, never model- or record-derived text
90:        except Exception as e:                         # a bug in our code: keep the row (class name only), then let it propagate below
108:            raise bug
--- restore commit
6feb2ff fix: restore T-095 work reverted by 2fca530

 app/backend/rejudge.py   |  8 +++++
 app/db/db.py             | 52 ++++++++++++++++++++++++++++++--
a850be0 fix: restore T-090 work reverted by 2fca530

 evals/run.py                   |  88 ++++++++++++++++-----
--- blame pipeline.py CLI raw
d67a82d6 (Chris Borsheim 2026-11-01 19:55:53 -0600 496)     ap = argparse.ArgumentParser(prog="python -m app.pipeline", 
d67a82d6 (Chris Borsheim 2026-11-01 19:55:53 -0600 497)     ap.add_argument("file")
d67a82d6 (Chris Borsheim 2026-11-01 19:55:53 -0600 498)     ap.add_argument("--db", default=None, help="SQLite file (def
d67a82d6 (Chris Borsheim 2026-11-01 19:55:53 -0600 499)     ap.add_argument("--json", action="store_true", help="print t
865b1865 (Chris Borsheim 2026-11-01 22:33:19 -0600 500)     try:
865b1865 (Chris Borsheim 2026-11-01 22:33:19 -0600 501)         language.case_check(language.annotate(IN.ingest(raw)["re
865b1865 (Chris Borsheim 2026-11-01 22:33:19 -0600 502)     except language.UnsupportedLanguage as e:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:32.217Z

The CLI crash comes from 865b186 (T-085), outside these cards. Last checks: whether any judge call bypasses the guard (so `error_class` would be missing there), and whether both the billing and reclassify routes are registered at HEAD.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:48:34.288Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && echo \"--- judge calls outside judge_guard\" && grep -rn \"judges\\.run_j[0-9]_meta\\|spanish\\.run_j[0-9]_meta\\|run_j[0-9]_meta(\" app/ | grep -v \"def run_j\" | head -20; echo \"--- guarded callers\" && grep -rn \"judge_guard.guarded\" app/ | head; echo \"--- api routes\" && grep -n \"reclassify\\|billing.add_routes\" app/backend/api.py | head",
 "description": "Find judge call sites that bypass the guard and confirm routes at HEAD"
}
````

### User / tool · 2026-11-02T04:48:34.405Z

**tool result**
````
--- judge calls outside judge_guard
app/backend/spanish.py:15:    Same return as judges.run_j1_meta: (verdict, call_id, reason_code)."""
app/backend/spanish.py:17:        return judges.run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)
app/backend/rejudge.py:30:        return spanish.run_j1_meta(ed.get("summary", row["summary"]), ed.get("excerpt", row["excerpt"]), row["provider"] or "", call=call,
app/backend/rejudge.py:33:        return judges.run_j2_meta(row["excerpt"], row["text"], row["kind"], call=call, nonce=nonce, item_id=item)
app/backend/rejudge.py:37:        return judges.run_j3_meta(comp["excerpt"], comp["excerpt_b"], call=call, nonce=nonce, item_id=item, category=row["category"])
app/backend/rejudge.py:40:    return judges.run_j4_meta(comp["excerpt"], row["type"], row["category"], call=call, nonce=nonce, item_id=item)
app/backend/flags.py:291:                v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
app/backend/flags.py:294:                v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
app/backend/narrative.py:108:        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
app/backend/review.py:102:        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
app/backend/generator.py:150:            return e, spanish.run_j1_meta(e["summary"], e["excerpt"], rec["source"], call=call, nonce=n, item_id=e["id"], lang=language.record_lang(rec)), False
app/backend/judges.py:69:    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]
app/backend/judges.py:73:    return run_j2_meta(excerpt, raw_amount, code_class, call=call, nonce=nonce, item_id=item_id)[0]
app/backend/judges.py:77:    return run_j3_meta(excerpt_a, excerpt_b, call=call, nonce=nonce, item_id=item_id, category=category)[0]
app/backend/judges.py:81:    return run_j4_meta(excerpt, flag_type, category, call=call, nonce=nonce, item_id=item_id)[0]
app/backend/judges.py:108:            v, cid, code = run_j2_meta(it["excerpt"], it["raw"], it["cls"], call=call, nonce=n, item_id=it["id"])
app/backend/reclassify.py:16:The judge sees only the record text, the figure and the class (judges.run_j2_meta); the model supplies no prose that is stored."""
app/backend/reclassify.py:167:    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row["excerpt"], row["text"], "charge", call=call, item_id=row["id"])
--- guarded callers
app/backend/review.py:102:        verdict, call_id, judge_code, judge_error = judge_guard.guarded(spanish.run_j1_meta, new_sum, new_exc, label, call=call, item_id=item_id, lang=lang)   # T-073
app/backend/reclassify.py:167:    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row["excerpt"], row["text"], "charge", call=call, item_id=row["id"])
--- api routes
510:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
511:    from app.backend import reclassify
512:    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:11.073Z

The judge call sites are clear: only review.py and reclassify.py go through the guard, so `error_class` is recorded only on those two seams. I'll confirm the r2 review files do not already exist (the write guard is append-only) and confirm the billing and reclassify route registrations at the pinned HEAD.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:13.821Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/ | grep -E \"T-073|T-084\" ; echo \"---\"; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && ls \"$SP/head-a850be0/app/backend/billing.py\" \"$SP/head-a850be0/tests/unit/test_billing.py\" && grep -c \"billing\" \"$SP/head-a850be0/memory/contracts/api.md\" && cd /Users/arsis/zlayt-pm-project && git ls-tree -r --name-only a850be0 | grep -i billing && git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py | tail -1; echo \"(empty above means identical to f218263)\"; git show a850be0:app/backend/api.py | grep -n \"billing.add_routes\\|reclassify.add_routes\"",
 "description": "Check for existing r2 review files, billing parity at HEAD, and route registration"
}
````

### User / tool · 2026-11-02T04:49:13.997Z

**tool result**
````
-rw-r--r--@   1 arsis  staff  15387 Nov  1 22:31 T-073-staff-engineer.md
-rw-r--r--@   1 arsis  staff  20940 Nov  1 22:32 T-084-staff-engineer.md
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0/app/backend/billing.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head-a850be0/tests/unit/test_billing.py
6
app/backend/billing.py
tests/unit/test_billing.py
(empty above means identical to f218263)
510:    billing.add_routes(app, conn=conn, get_case=get_case)       # T-083
512:    reclassify.add_routes(app, conn=conn, get_case=get_case, body_of=body_of, make_call=make_call)     # T-084
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:32.845Z

Both r2 review files are absent, and billing matches f218263 at the pinned HEAD. One last board read to see whether the deferred `judges._run` card exists before I cite it.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:33.417Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-094 2>&1 | head -6; echo \"---\"; python3 tools/board.py show T-095 2>&1 | sed -n 1,4p",
 "description": "Read board cards T-094 and T-095 headers (read-only)"
}
````

### User / tool · 2026-11-02T04:49:33.627Z

**tool result**
````
---
id: "T-094"
title: "Live ship-bar flap: case_02 golden must_not hit and entry recall 0.965 on a live run"
milestone: "M2"
role: "backend"
status: "in_progress"
---
---
id: "T-095"
title: "review_events CHECK: add reclassify and rejudge actions (migrate existing edit+event rows)"
milestone: "M3"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:49:51.766Z

T-094 is an unrelated live ship-bar card, so the worker's deferral note points at the wrong card. I have enough evidence for the T-073 round-2 file, so I'll write it now.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:09.097Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-073-staff-engineer-r2.md",
 "content": "# T-073 r2 review: narrow the broad except in the judge path (staff-engineer-reviewer, round 2)\n\nReviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (the T-073 r2 fix, committed together with the T-084 r2 changes), with e2b4e3f underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both \"restore ... reverted by 2fca530\"). The T-073 files are unchanged from c8a9874 through a850be0, so the verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad instead (same tree, no worktree).\n\n## Summary\n\nBoth r1 findings are closed at HEAD. `audited_call` now retries only `LLMError`, `TimeoutError`, `ConnectionError`, and a `validate` `ValueError` (audited.py:21-22). Any other exception writes one `llm_calls` row with the class name only and is re-raised (audited.py:90-91, 106-108). The guard records `ladder.judge.error_class` for `LLMFailed`, `LLMFailedFixtureMiss`, `FixtureMissing` and `LLMError` on the two seams that use it (judge_guard.py:17-23; review.py:102, reclassify.py:167). Four scratch mutants of this code are each caught (5 to 8 failing tests each). No blocker, no major. Verdict: pass, with one minor (error_class is recorded only on the two guarded seams) and one minor record problem (the deferred judges.py change points at the wrong card).\n\n## Exercised (what I actually ran or read)\n\n- `python3 tools/board.py show T-073` and `show T-094` (T-094 is \"Live ship-bar flap ...\", not the judges.py card the handoff names).\n- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44 at start, a850be0 at the end); `git show --stat c8a9874`; `git show --stat e2b4e3f`.\n- `git diff --stat c8a9874 bc12d44 -- app/backend/judge_guard.py app/llm/audited.py app/backend/judges.py tests/unit/test_audited.py tests/unit/test_judge_guard.py`: empty. `git diff --stat bc12d44 a850be0 -- <same files>`: empty.\n- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed (the working tree has uncommitted edits, not reviewed); pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed (all 9 in test_reclassify.py, see T-084 r2).\n- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_audited.py` at a850be0: 19 passed.\n- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. None of the 7 is in test_audited.py or test_judge_guard.py (names in reviews/T-084-staff-engineer-r2.md).\n- Read in full at a850be0: app/llm/audited.py, app/backend/judge_guard.py, app/backend/judges.py:24-39, tests/unit/test_audited.py, tests/unit/test_judge_guard.py, app/llm/_types.py:7-11.\n- `grep -rn \"judge_guard.guarded\" app/` (review.py:102, reclassify.py:167 only) and `grep -rn \"run_j[0-9]_meta(\" app/` (judge call sites).\n- Scratch mutants T73-1 to T73-4 with `artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py`, log `artifacts/review-evidence/T-073-T-084-r2/mutation-run-r2.txt`. Control on the pinned archive: 139 passed (the four files plus test_audited.py).\n- The brief's selector `-k \"review or reclass\"` still does not collect test_judge_guard.py; I named the files explicitly, as r1 asked.\n\n## Findings\n\n### F1 (minor): error_class is recorded only on the two guarded seams\n\n- `grep -rn \"judge_guard.guarded\" app/` returns review.py:102 and reclassify.py:167 only. Other judge call sites call `judges.run_*_meta` directly: rejudge.py:30-40, flags.py:291-294, narrative.py:108, generator.py:150, and the pipeline batch at judges.py:108. judges.py:33-34 still turns `LLMFailed` into `(\"unavailable\", None, \"NONE\")`, so on those paths the ladder records reason NONE and no class.\n- Why it matters: the card's AC is scoped to review.py, so the AC is met. The same expected failure on rejudge, flags or narrative still leaves the audit unable to say why the judge did not run. This is the same gap as r1 F2, now on the other seams.\n- Fix: return the class from `judges._run` with the verdict (for example `(verdict, call_id, reason, error_class)`), or route each direct call through `judge_guard.guarded`. judges.py is outside this card's stated scope, so it needs its own card (see F2).\n- Acceptance test: a fixture backend raising `AU.LLMFailed` through `rejudge` (rejudge.py:30) records `ladder.judge.error_class == \"LLMFailed\"`.\n\n### F2 (minor): the deferred judges.py change has no card\n\n- The handoff says \"judges._run still returns reason NONE for LLMFailed ... (judges.py untouched, T-094)\". `python3 tools/board.py show T-094` returns \"Live ship-bar flap: case_02 golden must_not hit and entry recall 0.965 on a live run\". The deferral points at an unrelated card, so it is effectively unrecorded.\n- Fix: the orchestrator opens a backend card for the judges._run change (`board.py new` with the F1 acceptance test as its AC) and corrects the handoff reference.\n\n### F3 (nit): retry delays are fixed, not jittered\n\n- audited.py:17 `RETRY_DELAYS_S = (0.5, 1.5)`. The cap (audited.py:15, `MAX_ATTEMPTS = 3`, so two retries) and the per-attempt logging are right. The dossier (persona §9) asks for jitter on retries. This is optional for the fixture backend, which never sleeps.\n- Fix (optional): add a small jitter to the live-backend sleep. Acceptance: a test that patches the sleep hook and asserts each delay lies within the jittered bounds.\n\n## What is right\n\n- audited.py:21-22 and :88-108: retries are limited to provider, transport and validation errors. Any other exception writes one `llm_calls` row (class name only) and is re-raised. test_audited.py:109-136 covers it; mutant T73-1 (broad retry) fails 8 tests and mutant T73-2 (bug not re-raised) fails 8 tests.\n- judge_guard.py:17-23 notes the expected error's class on the way through judges._run, so review.py:102 and reclassify.py:167 record `ladder.judge.error_class`. test_judge_guard.py:94-113 covers LLMFailed, LLMFailedFixtureMiss, FixtureMissing and LLMError. Mutant T73-3 (class not noted) fails 5 tests.\n- judge_guard.py:8 covers `FixtureMissing` through its base class (_types.py:11 `class FixtureMissing(LLMError)`). Mutant T73-4 (guard catches every exception) fails 7 tests.\n\nOutside this card, not attributed to it: the full unit run at a850be0 has 7 failures, and the sample CLI crashes at pipeline.py:501. Details are in reviews/T-084-staff-engineer-r2.md.\n\n## Scores\n\n```\nno_silent_fallback 4 (expected errors become unavailable with a class; no positive verdict; judges._run still hides the class on other seams, F1)\nerror_class_recorded 4 (both guarded seams; other judge call sites still NONE, F1)\npropagation_on_real_path 5 (one row, re-raised, not retried; mutants T73-1 and T73-2 caught)\ntests_kill_mutants 5 (4 of 4 seam mutants caught on the pinned HEAD)\nac_evidence_matches_code 4 (AC holds for review.py; the deferral is not recorded on a card, F2)\n```\n\n## Questions for Chris\n\nNone for this card.\n\n```json\n{\"card\": \"T-073\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit c8a9874 (T-073 r2, committed with T-084 r2) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/llm/audited.py, app/backend/judge_guard.py, app/backend/judges.py (read), tests/unit/test_audited.py, tests/unit/test_judge_guard.py, app/llm/_types.py (read); no app URL; unit-level card, no sample-case run\",\n \"exercised\": [\"python3 tools/board.py show T-073 and show T-094\", \"git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874 and e2b4e3f\", \"git diff --stat c8a9874 bc12d44 and bc12d44 a850be0 over the T-073 files (both empty)\", \".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed 111 passed\", \".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed\", \".venv/bin/python -m pytest -q tests/unit at a850be0: 7 failed 1392 passed 2 skipped (none in the T-073 files)\", \"read audited.py, judge_guard.py, judges.py:24-39, test_audited.py, test_judge_guard.py, _types.py:7-11 at a850be0\", \"grep -rn judge_guard.guarded app/ and grep -rn run_j[0-9]_meta( app/\", \"scratch mutants T73-1..T73-4 via artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py (log mutation-run-r2.txt): T73-1 8 failed, T73-2 8 failed, T73-3 5 failed, T73-4 7 failed; control 139 passed\"],\n \"verdict\": \"pass\",\n \"scores\": {\"no_silent_fallback\": 4, \"error_class_recorded\": 4, \"propagation_on_real_path\": 5, \"tests_kill_mutants\": 5, \"ac_evidence_matches_code\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"error_class is recorded only on the two guarded seams; other judge call sites still turn LLMFailed into reason NONE with no class\",\n   \"evidence\": \"grep -rn 'judge_guard.guarded' app/ -> review.py:102 and reclassify.py:167 only; judges.py:33-34 'except AU.LLMFailed: return unavailable, None, NONE' unchanged; direct callers rejudge.py:30-40, flags.py:291-294, narrative.py:108, generator.py:150, judges.py:108\",\n   \"why_it_matters\": \"The card AC is scoped to review.py and is met. The same expected failure on rejudge, flags, narrative or the pipeline still leaves the audit without the reason the judge did not run (the r1 F2 gap on other seams).\",\n   \"fix\": \"Return the class from judges._run with the verdict, or route each direct call through judge_guard.guarded. judges.py is outside this card, so it needs its own backend card (see F2).\",\n   \"acceptance_test\": \"A fixture backend raising AU.LLMFailed through rejudge.py:30 records ladder.judge.error_class == 'LLMFailed' on the item.\"},\n  {\"severity\": \"minor\", \"title\": \"The deferred judges.py change has no card: the handoff cites T-094, which is an unrelated live ship-bar card\",\n   \"evidence\": \"T-073 handoff text 'judges._run still returns reason NONE for LLMFailed ... (judges.py untouched, T-094)'; python3 tools/board.py show T-094 -> title 'Live ship-bar flap: case_02 golden must_not hit and entry recall 0.965 on a live run'\",\n   \"why_it_matters\": \"A deferral that points at the wrong card is effectively unrecorded; the next reader will chase the wrong work.\",\n   \"fix\": \"Orchestrator opens a backend card for the judges._run class capture (board.py new, AC = the F1 acceptance test) and corrects the handoff reference.\",\n   \"acceptance_test\": \"board.py show <new card> lists the judges._run change in its AC; the T-073 handoff names that card.\"},\n  {\"severity\": \"nit\", \"title\": \"Retry delays are fixed, not jittered\",\n   \"evidence\": \"app/llm/audited.py:17 RETRY_DELAYS_S = (0.5, 1.5); cap at audited.py:15 MAX_ATTEMPTS = 3 is correct\",\n   \"why_it_matters\": \"The persona's retry guidance (AWS, persona §9) asks for jitter on retries. The fixture backend never sleeps, so this does not affect tests.\",\n   \"fix\": \"Optional: add a small jitter to the live-backend sleep.\",\n   \"acceptance_test\": \"A test that patches the sleep hook and asserts each delay lies within the jittered bounds.\"}\n ],\n \"whats_right\": [\n  \"audited.py:21-22 and :88-108: retries only provider, transport and validation errors; any other exception writes one llm_calls row (class name only) and re-raises; mutants T73-1 and T73-2 each fail 8 tests.\",\n  \"judge_guard.py:17-23 notes the expected error's class on the way through judges._run, so review.py:102 and reclassify.py:167 record ladder.judge.error_class; test_judge_guard.py:94-113 covers it; mutant T73-3 fails 5 tests.\",\n  \"judge_guard.py:8 covers FixtureMissing through its base class (_types.py:11), and mutant T73-4 (guard catches everything) fails 7 tests.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T04:50:09.244Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-073-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:14.088Z

The T-073 round-2 file is written and cannot be edited in place, so I'll verify the call-site line numbers I cited in it against the pinned HEAD before I write the T-084 file.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:16.890Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && echo \"--- judges.py 98-110\" && sed -n 98,110p app/backend/judges.py | cut -c1-150 && echo \"--- rejudge 28-41\" && sed -n 28,41p app/backend/rejudge.py | cut -c1-120 && echo \"--- flags 289-295\" && sed -n 289,295p app/backend/flags.py | cut -c1-120 && echo \"--- narrative 107-109\" && sed -n 107,109p app/backend/narrative.py | cut -c1-120 && echo \"--- generator 149-151\" && sed -n 149,151p app/backend/generator.py | cut -c1-120 && echo \"--- _types 7-12\" && sed -n 7,12p app/llm/_types.py && echo \"--- judges 33-34\" && sed -n 33,34p app/backend/judges.py && echo \"--- judge_guard 15-27 lines\" && grep -n \"def noting\\|kwargs\\[\\\"call\\\"\\] = noting\\|except EXPECTED_JUDGE_ERRORS\" app/backend/judge_guard.py",
 "description": "Verify cited call-site and line numbers in the pinned HEAD archive"
}
````

### User / tool · 2026-11-02T04:50:17.023Z

**tool result**
````
--- judges.py 98-110


def judge_amounts(items: list, *, call, case_text: str = "") -> dict:
    """Judge 2 on every amount, rule-made or not (R-CH-2, row 7). items: [{'id', 'raw', 'cls', 'excerpt'}].
    Returns {id: {'verdict', 'ladder', 'call_id', 'reason_code', 'fixture_miss', 'model', 'prompt_version'}}. FixtureMiss -> ladder 'unavailable' + fi
    from app.llm import promptlib as _pl, provider as _P
    out = {}
    for it in items:
        n = _pl.nonce(case_text, "j2", it["id"])
        try:
            v, cid, code = run_j2_meta(it["excerpt"], it["raw"], it["cls"], call=call, nonce=n, item_id=it["id"])
            miss = False
        except _P.FixtureMiss:
--- rejudge 28-41
        edited = "summary" in ed or "excerpt" in ed
        lang = "es" if (row.get("ladder") or {}).get("translation") else "en"          # D-042: the Spanish-record judge
        return spanish.run_j1_meta(ed.get("summary", row["summary"]), ed.get("excerpt", row["excerpt"]), row["provider"]
                                   nonce=None if edited else nonce, item_id=item, lang=lang)           # an edit's judge
    if kind == "amount":
        return judges.run_j2_meta(row["excerpt"], row["text"], row["kind"], call=call, nonce=nonce, item_id=item)
    if jid == "j3":
        if not (comp.get("excerpt") and comp.get("excerpt_b")):
            return _UNAVAILABLE
        return judges.run_j3_meta(comp["excerpt"], comp["excerpt_b"], call=call, nonce=nonce, item_id=item, category=row
    if not comp.get("excerpt"):
        return _UNAVAILABLE
    return judges.run_j4_meta(comp["excerpt"], row["type"], row["category"], call=call, nonce=nonce, item_id=item)

--- flags 289-295
                if not f.get("excerpt_b"):
                    continue
                v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, 
                step, pv = "j3", "judge_conflict_v2"
            elif f["origin"] in ("llm", "both"):
                v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item
                step, pv = "j4", "judge_flag_v2"
--- narrative 107-109
        # the date of service lives in the record header, not the quote: give the judge the header it may rely on
        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_dat
                                                   call=call, item_id=item["id"])
--- generator 149-151
        try:
            return e, spanish.run_j1_meta(e["summary"], e["excerpt"], rec["source"], call=call, nonce=n, item_id=e["id"]
        except P.FixtureMiss:
--- _types 7-12
class LLMError(Exception):
    """Timeout, backend failure, invalid JSON or schema-invalid output. Messages must never contain record text."""


class FixtureMissing(LLMError):
    """No recorded answer for this prompt hash. Never retried, never answered with a default."""
--- judges 33-34
    except AU.LLMFailed:
        return "unavailable", None, "NONE"
--- judge_guard 15-27 lines
17:        def noting(*a, **k):
20:            except EXPECTED_JUDGE_ERRORS as e:
23:        kwargs["call"] = noting
26:    except EXPECTED_JUDGE_ERRORS as e:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:39.618Z

The call-site references hold up. Before writing the T-084 file, I'll pin the last few line numbers I plan to cite (the amounts unit list and the db transaction lines at a850be0), since db.py changed in 6feb2ff.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:42.263Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SP/head-a850be0\" && grep -n \"^_UNIT = \" app/backend/amounts.py && grep -n \"isolation_level=None\\|conn.execute(\\\"BEGIN\\\")\" app/db/db.py && grep -n \"^def apply_review\" app/db/db.py && grep -n \"^def connect\" app/db/db.py && grep -n \"CHECK (action\" app/db/schema.sql | cut -c1-60 && grep -n \"SCHEMA_VERSION = \" app/db/db.py | cut -c1-40 && grep -n \"AUDIT_ACTION\" app/backend/reclassify.py | head -2 && grep -n \"reclassify\" tests/unit/test_reclassify.py | grep \"action\" | head -3",
 "description": "Pin amounts unit list, db transaction, schema CHECK, and audit-action line numbers at HEAD"
}
````

### User / tool · 2026-11-02T04:50:42.403Z

**tool result**
````
14:_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
54:    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
227:    conn.execute("BEGIN")
287:    conn.execute("BEGIN")
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
38:def connect(path: str):
57:  action TEXT NOT NULL CHECK (action IN ('accept','edit',
33:SCHEMA_VERSION = 4          # bump on
27:AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
91:                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))
319:    assert [e["action"] for e in ev] == ["reclassify"]                # T-095: its own audit action (schema v4)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:50:51.670Z

I have every citation pinned. Writing the T-084 round-2 file now, with the closed c8a9874 failure recorded in the body and the two open majors and two minors in the JSON.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:17.962Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r2.md",
 "content": "# T-084 r2 review: guarded charge reclassification (D-042) (staff-engineer-reviewer, round 2)\n\nReviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (T-084 r2, committed with the T-073 r2 changes), with e2b4e3f (billing restored) underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both \"restore ... reverted by 2fca530\"). The verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad. The working tree has uncommitted edits to reclassify.py (it now imports `amounts.RATE_CUE`), amounts.py, billing.py and audited.py. Those are not reviewed here.\n\n## Summary\n\nThe three r1 invariants hold on HEAD for the paths the tests and probes reach, with two gaps. (1) A restore re-runs both checks when the sentence changes and when the code's class changes (reclassify.py:145-153), and the code is right for both. Only the sentence arm has a test, so a class-only change has no test that would catch its removal (F1). (2) The code wording gate refuses \"Charge per visit $185.\" and \"Billed $150 per visit.\" before the judge, as the brief asks, and it refuses 17 rate-cue sentences. It still passes six unit-price phrasings that the amount classifier calls a rate or a unit price, so for those the judge is the only gate (F2).\n\nOne r1 blocker is closed, but not by this card. c8a9874 alone does not work: its own test file fails 9 of 120 tests, and a reclassify request returns 500 after it has already changed the item and written no audit row. HEAD a850be0 is correct because 6feb2ff restored the T-095 schema that 2fca530 had reverted. The card's commit list does not name 6feb2ff.\n\nBilling is back in HEAD and identical to f218263. The worker's extra behaviour (a promoted charge falls back to the code's class when a rerun changes its sentence) goes the safe direction, but it drops the paralegal's decision without any visible note (F4).\n\nVerdict: changes (0 blockers, 2 majors) on HEAD a850be0.\n\n## Exercised (what I actually ran or read)\n\n- `python3 tools/board.py show T-084`, `show T-094`, `show T-095` (the 031a708 card; header only).\n- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44, then a850be0). `git show --stat c8a9874`, `e2b4e3f`, `6feb2ff`, `a850be0`.\n- `git show c8a9874:app/db/schema.sql | grep -c \"'reclassify'\"` = 0; `git show a850be0:app/db/schema.sql` line 57 contains 'reclassify' and 'rejudge'.\n- `git diff --stat bc12d44 a850be0 -- <in-scope>`: only app/db/db.py and app/db/schema.sql changed. `git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py`: empty. `git ls-tree -r --name-only a850be0 | grep -i billing`: both files. `git show a850be0:app/backend/api.py`: line 510 `billing.add_routes(...)`, line 512 `reclassify.add_routes(...)`.\n- `git blame -L 496,502 a850be0 -- app/backend/pipeline.py`: lines 500-501 from 865b1865 (T-085).\n- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed. The 9 failures are test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited, test_undoing_her_own_demotion_restores_the_code_class_without_a_judge, test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge, test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again, test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again, test_restore_after_an_unchanged_rerun_still_needs_no_judge, test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence, test_a_rerun_keeps_her_reclassification, test_route (the last with \"assert (500 == 200)\" and IntegrityError at reclassify.py:90).\n- `.venv/bin/python -m pytest -q tests/unit/test_audited.py` at a850be0: 19 passed. `.venv/bin/python -m pytest -q tests/unit/test_billing.py` at a850be0: 27 passed.\n- `.venv/bin/python -m pytest -q tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. The 7 are tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s, test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2, and four in test_trace.py (test_every_item_has_an_ordered_well_formed_trace, test_metadata_mode_has_no_raw_answers_or_edit_text_and_local_mode_only_adds_them, test_every_emitted_reason_code_has_a_fixed_sentence, test_items_whose_judge_never_ran_are_counted_and_fail_the_judges_step). The handoff's \"1417 pass\" was measured on the working tree.\n- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` run in the a850be0 archive: traceback ends `UnboundLocalError: cannot access local variable 'raw' where it is not associated with a value` at pipeline.py:501. Exit status non-zero.\n- Read in full at a850be0: app/backend/reclassify.py (unchanged since bc12d44) and tests/unit/test_reclassify.py (unchanged since bc12d44), plus app/backend/judge_guard.py and app/llm/audited.py for the T-073 side. db.py:54 (autocommit), :215 (apply_review), :227 and :287 (BEGIN). amounts.py:14 (`_UNIT`).\n- Probes, all in `artifacts/review-evidence/T-073-T-084-r2/`, each run with `.venv/bin/python -I <probe> <archive root>`:\n  - `probe_reclassify_audit_route.py` on c8a9874 and a850be0 (output in the transcript; c8a9874: HTTP 500, stored kind changed charge to unclear, `review_events for a1: []`; a850be0: HTTP 200, `[('reclassify', 'reclassify')]`).\n  - `probe_rate_cue_gaps.py` on a850be0, output `rate-cue-gaps-run.txt`.\n  - `probe_classifier_vs_wording_gate.py` on a850be0, output `classifier-vs-gate-run.txt`.\n  - `probe_restore_class_only_flip.py` on a850be0 and on mutant m03, output `restore-class-only-flip-run.txt`.\n- Scratch mutants via `mutate_r2.py` (applied to copies, never to the project; log `mutation-run-r2.txt`). Control: 139 passed. Results: T84-1 (rate cue removed from the wording gate) 21 failed; T84-2 ('per' removed from the rate-cue pattern) 11 failed; T84-3 (restore ignores the code class) 139 passed; T84-4 (restore ignores whether the sentence changed) 1 failed; T84-5 (restore always skips the checks, the r1 bug) 2 failed; T84-6 (promoted charge kept when its sentence changes) 1 failed. T73-1 to T73-4: see the T-073 r2 review.\n- `grep` on the judge call sites (`judge_guard.guarded` only at review.py:102 and reclassify.py:167).\n\n## Findings\n\n### F1 (major): restore after a class-only change is not tested; mutant survives\n\n- The code is right: `_may_restore` (reclassify.py:145-153) requires `rerun.code_class == \"charge\"` and an unchanged sentence sha. Probe `probe_restore_class_only_flip.py` on a850be0 (the rerun changes only the code's class of $310; the excerpt text is identical): `4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE`, `5. stored kind = unclear | reclassify events before/after = 1 1`, `pending total cents = 0`.\n- The gap is the test. Mutant T84-3 (reclassify.py:153 reduced to `return rerun.get(\"excerpt_sha\") == prior.get(\"excerpt_sha\") == _sha(row[\"excerpt\"])`) passes all 139 tests. The same probe on that mutant: `4. restore with no judge: HTTP 200 restored=True kind=charge`, `pending total cents = 31000`.\n- The tests exercise the sentence arm only: test_reclassify.py:190 `RATE_R3` changes the sentence and the class together, and test_reclassify.py:198-216 uses it. test_reclassify.py:219-230 changes the sentence, not the class.\n- Why it matters: the brief asks that a restore re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without the test, a later edit to `_may_restore` could reopen the r1 blocker and no test would fail.\n- Fix: add a test that patches `amounts.classify` so the rerun's code class of $310 is \"rate\" while the excerpt stays identical. Then `reclassify(..., {\"to\": \"charge\"}, call=None)` must raise 422 JUDGE_UNAVAILABLE with the item still `unclear`. Add the case with `call=FakeCall(J2(\"agree\"))`: the judge is called once and `restored` is False. Keep test_reclassify.py:233-240 (unchanged rerun, no judge) passing.\n- Acceptance test: mutant T84-3 fails the new test.\n\n### F2 (major): the code wording gate passes unit-price phrasings that the amount classifier calls rates\n\n- Probe `probe_classifier_vs_wording_gate.py` (a850be0, output `classifier-vs-gate-run.txt`): \"Charged $150 an hour.\" is `rate` by amounts.classify and passes charge_wording (`passes (Charged)`); \"Charged $75 a unit.\" is `rate` and passes; \"Billed $120 an appointment.\" is `rate` and passes. The unit vocabulary is amounts.py:14 `_UNIT = ... hour|hr|day|unit|appointment|procedure|adjustment`, while the gate's rate-cue pattern is reclassify.py:31-33, which has no hour, unit or appointment.\n- Probe `probe_rate_cue_gaps.py` (output `rate-cue-gaps-run.txt`): \"Billed $150 hourly.\", \"Charged $90 apiece.\", \"Billed $40 daily.\" and \"Billed $200 a month.\" also pass the code gate. The two named strings are refused (`None (refused)`), so F2 is not about the brief's named cases.\n- Why it matters: D-042 as written is met, because the sentence has charged wording and the judge re-checks it. But the code gate and the classifier disagree about the same sentence. For these phrasings the judge is the only gate before a figure goes to pending, and the paralegal can then accept it into the total. This is the first independent gate the card depends on. The r1 fix list named \"per unit\" and \"a visit\", and the gate covers those only partly.\n- Fix: one rate-unit test shared by amounts.classify and reclassify.charge_wording. The uncommitted working tree already moves toward `amounts.RATE_CUE` (not reviewed). Whatever form lands, refuse the six phrasings before the judge.\n- Acceptance test: `charge_wording` returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for \"Charged $150 an hour.\", \"Charged $75 a unit.\", \"Billed $120 an appointment.\". A parametrized test asserts that for every fixture sentence, `amounts.classify == \"rate\"` implies `charge_wording is None`.\n\n### F3 (minor): the state change and its audit row are separate autocommit writes; the consequence is now observed\n\n- reclassify.py:135 `DB.update_item(...)` commits on its own (db.py:54 `isolation_level=None`, autocommit). reclassify.py:137 `review.batch_apply` (for a non-pending item) and reclassify.py:138 `_log` follow as separate statements.\n- Observed on c8a9874 (`probe_reclassify_audit_route.py`): `POST reclassify a1 -> HTTP 500`, `a1 stored after request: kind=unclear`, `review_events for a1 (action, payload event): []`. The paralegal sees an error, the item has changed, and there is no audit row.\n- The brief allows this as a minor. The fix is the one from r1: wrap update_item, batch_apply and _log in one transaction with rollback on error, as db.py:227 and :287 do for apply_review.\n- Acceptance test: monkeypatch `RC._log` to raise; assert the item's kind is still `charge` after the call.\n\n### F4 (minor): a promoted charge is dropped silently when its sentence changes\n\n- reclassify.py:188-189 `if rc.get(\"to\") == \"charge\" and rc.get(\"excerpt_sha\") != _sha(it.get(\"excerpt\")): return it`. The reclassification record is discarded and the figure returns to the code's class. The same figure becomes `rate`, which is the safe direction (it leaves the total).\n- But the response to the rerun carries no note that her promotion was withdrawn. test_reclassify.py:249-250 asserts only `kind != \"charge\"`. The audit row stays (review_events), but the item view does not say why the figure changed.\n- Fix: keep the record with `dropped: \"SENTENCE_CHANGED\"` in `ladder.reclassification` and show it in the item view and the stepper.\n- Acceptance test: after a sentence change, `item.ladder.reclassification.dropped == \"SENTENCE_CHANGED\"` and the item view names the reason.\n\n## Closed at HEAD (not findings at a850be0)\n\n- c8a9874 on its own tree (blocker at c8a9874, closed at HEAD). Schema: `git show c8a9874:app/db/schema.sql | grep -c \"'reclassify'\"` = 0, and reclassify.py:27 sets `AUDIT_ACTION = \"reclassify\"`. The reclassify INSERT fails with IntegrityError (reclassify.py:90), the route returns 500, and the item is already changed (F3 evidence). 2fca530 (T-087/T-086, a sibling commit) reverted the T-095 CHECK and migration. 6feb2ff (\"fix: restore T-095 work reverted by 2fca530\") restores them. At a850be0 the CHECK is at schema.sql:57, SCHEMA_VERSION is 4 (db.py:33), the four files pass 120 of 120, and the probe returns 200 with a `reclassify` row. The card should cite 6feb2ff, since c8a9874 alone does not pass.\n- r1 F4 (audit action 'edit'): closed. AUDIT_ACTION is \"reclassify\" (reclassify.py:27) and test_route:319 asserts `[\"reclassify\"]`, which passes at HEAD.\n- r1 F2 (billing removed by ec33bf0): closed. billing.py and test_billing.py are identical to f218263 at a850be0; api.py:510 registers the billing routes. test_billing.py: 27 passed.\n- r1 F1 (restore after a rerun), sentence arm: closed. Mutant T84-4 fails 1 test, mutant T84-5 (the r1 bug) fails 2, mutant T84-6 fails 1. Class arm: code correct (probe), test missing (F1 above).\n- r1 F3 (rate phrase passes the wording gate), named strings: closed. \"Charge per visit $185.\" and \"Billed $150 per visit.\" are refused before the judge (test_reclassify.py:161-171, `call.log == []`). Mutant T84-1 fails 21 tests and mutant T84-2 fails 11. The remaining gap is F2.\n\n## Judgement on the worker's extra behaviour\n\n- A promoted charge falls back to the code's class when a rerun changes its sentence (reclassify.py:188-189). I judge this right: it fails closed, and it is the same rule as the restore path (any sentence change means the earlier judge answer no longer applies). The silent drop is F4.\n\n## What is right\n\n- reclassify.py:145-153 (`_may_restore`) requires a charge original, a previous judge, and, after any rerun, the same sentence sha and a charge code class. The probe confirms the refusal (422 JUDGE_UNAVAILABLE, total 0).\n- The refusals stay before the judge: test_reclassify.py:170 asserts `call.log == []` and the item stays `rate`, `needs_review`.\n- Billing is back in HEAD: identical to f218263, registered at api.py:510, 27 tests pass.\n\n## Outside these cards (observed at a850be0, not attributed to T-073 or T-084)\n\n- The sample CLI crashes. `.venv/bin/python -m app.pipeline evals/golden/sample.txt` ends in UnboundLocalError at pipeline.py:501 (`raw` is referenced before assignment). `git blame` puts lines 500-501 in 865b1865 (T-085). This is persona checklist item 20 and it fails on HEAD.\n- Seven unit tests fail at a850be0 (listed in Exercised). I did not trace them to a cause. None is in the T-073 or T-084 files.\n\n## Scores\n\n```\nno_rate_into_total_without_both_checks 3 (both checks run on every path; the class-only restore is untested, F1; the code gate passes six classifier-rate phrasings, F2)\nrestore_rule_tested 3 (sentence arm killed; class arm not, F1)\ncode_check_strength 2 (named strings and 17 cues refused; six classifier-rate phrasings pass, F2)\njudge_gate 4 (judge disagree, unsure and unavailable give 422 with nothing changed)\naudit_trail 3 (written at HEAD; the item change and the audit row are not one transaction, F3; the promoted drop is not shown, F4)\ncommit_integrity 2 (c8a9874 alone fails 9 tests and 500s with the item changed; closed at HEAD by 6feb2ff, which is not in this card's commit list)\nbilling_restored 5 (identical to f218263; route registered; 27 tests pass)\ntests_kill_mutants 4 (T84-1, T84-2, T84-4, T84-5, T84-6 and all four T-073 mutants killed; T84-3 survives)\n```\n\n## Questions for Chris\n\n- D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should \"Charged $150 an hour.\", \"Charged $75 a unit.\" and \"Billed $120 an appointment.\" be refused by the code gate, even though they say \"charged\" or \"billed\" and the judge would then have to say so? My reading is that they should be refused, because the amount classifier calls them rates. The decision text does not say.\n"
}
````

### User / tool · 2026-11-02T04:51:18.115Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:31.449Z

The validator rejected the T-084 round-2 file because I left out the ```json block. I'll append the block to that file (adding the missing block, not rewriting the body) and check whether the write guard allows it.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:43.173Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r2.md",
 "old_string": "My reading is that they should be refused, because the amount classifier calls them rates. The decision text does not say.",
 "new_string": "My reading is that they should be refused, because the amount classifier calls them rates. The decision text does not say.\n\n```json\n{\"card\": \"T-084\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit c8a9874 (T-084 r2, committed with the T-073 r2 changes) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/backend/reclassify.py, app/backend/amounts.py (read), app/backend/api.py (routes), app/db/db.py and app/db/schema.sql (read, restored by 6feb2ff), tests/unit/test_reclassify.py, tests/unit/test_billing.py; c8a9874 alone fails 9 tests and is closed at HEAD by 6feb2ff (not a finding at a850be0); no app URL; sample CLI run at a850be0 crashes (outside this card, see body)\",\n \"exercised\": [\"python3 tools/board.py show T-084, T-094, T-095\", \"git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874, e2b4e3f, 6feb2ff, a850be0; git show c8a9874:app/db/schema.sql | grep -c reclassify (0); git diff --stat bc12d44 a850be0 over in-scope files (db.py and schema.sql only); git diff --stat f218263 a850be0 over the billing files (empty); git ls-tree a850be0 | grep billing (both files); git show a850be0:app/backend/api.py (lines 510, 512); git blame -L 496,502 a850be0 -- app/backend/pipeline.py\", \".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; a850be0 120 passed; c8a9874 9 failed 111 passed (IntegrityError at reclassify.py:90)\", \".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed; tests/unit/test_billing.py at a850be0: 27 passed; tests/unit at a850be0: 7 failed 1392 passed 2 skipped\", \".venv/bin/python -m app.pipeline evals/golden/sample.txt at a850be0: UnboundLocalError pipeline.py:501\", \"read in full at a850be0: reclassify.py and test_reclassify.py (both unchanged since bc12d44), judge_guard.py, audited.py; db.py:54, :215, :227, :287; amounts.py:14\", \"probes via .venv/bin/python -I in artifacts/review-evidence/T-073-T-084-r2/: probe_reclassify_audit_route.py (c8a9874 HTTP 500 and item changed with no event; a850be0 HTTP 200 and a reclassify event); probe_rate_cue_gaps.py (output rate-cue-gaps-run.txt); probe_classifier_vs_wording_gate.py (output classifier-vs-gate-run.txt); probe_restore_class_only_flip.py on a850be0 (422 JUDGE_UNAVAILABLE, total 0) and on mutant m03 (restored, total 31000; output restore-class-only-flip-run.txt)\", \"scratch mutants via mutate_r2.py (log mutation-run-r2.txt): control 139 passed; T84-1 21 failed; T84-2 11 failed; T84-3 139 passed (survives); T84-4 1 failed; T84-5 2 failed; T84-6 1 failed\", \"grep -rn judge_guard.guarded app/ (review.py:102 and reclassify.py:167 only)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"no_rate_into_total_without_both_checks\": 3, \"restore_rule_tested\": 3, \"code_check_strength\": 2, \"judge_gate\": 4, \"audit_trail\": 3, \"commit_integrity\": 2, \"billing_restored\": 5, \"tests_kill_mutants\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Restore after a class-only change is untested; mutant T84-3 (restore ignores the rerun's code class) passes all 139 tests\",\n   \"evidence\": \"reclassify.py:153 'return rerun.get(code_class) == charge and rerun.get(excerpt_sha) == prior.get(excerpt_sha) == _sha(row[excerpt])'; mutant without the class clause: mutation-run-r2.txt 'T84-3 ... 139 passed'; restore-class-only-flip-run.txt: HEAD '4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE', mutant 'restored=True kind=charge' and 'pending total cents = 31000'; tests/unit/test_reclassify.py:190 RATE_R3 and :198-216 change the sentence, not only the class\",\n   \"why_it_matters\": \"The brief requires a restore to re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to _may_restore can reopen the r1 blocker and no test fails.\",\n   \"fix\": \"Add a test that patches amounts.classify so the rerun's code class of $310 is rate while the excerpt is identical; reclassify to charge with call=None must raise 422 JUDGE_UNAVAILABLE with the item still unclear. Add the same case with call=FakeCall(J2 agree): the judge is called once and restored is False. Keep test_reclassify.py:233-240 passing.\",\n   \"acceptance_test\": \"Mutant T84-3 (reclassify.py:153 without the code_class clause) fails the new test.\"},\n  {\"severity\": \"major\", \"title\": \"The code wording gate passes unit-price phrasings that the amount classifier calls rates, so the judge is the only gate for them\",\n   \"evidence\": \"classifier-vs-gate-run.txt: 'Charged $150 an hour.' classifier rate, gate passes (Charged); 'Charged $75 a unit.' rate, passes; 'Billed $120 an appointment.' rate, passes. rate-cue-gaps-run.txt: 'Billed $150 hourly.', 'Charged $90 apiece.', 'Billed $40 daily.', 'Billed $200 a month.' pass the gate. reclassify.py:31-33 _RATE_CUE has no hour, unit or appointment; amounts.py:14 _UNIT = (visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?\",\n   \"why_it_matters\": \"D-042 as written is met (charged wording plus a judge re-check), but the code gate and the classifier disagree on the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only partly.\",\n   \"fix\": \"Use one rate-unit test for amounts.classify and reclassify.charge_wording (the uncommitted working tree already moves toward amounts.RATE_CUE; not reviewed here). Refuse the six phrasings before the judge.\",\n   \"acceptance_test\": \"charge_wording returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for 'Charged $150 an hour.', 'Charged $75 a unit.', 'Billed $120 an appointment.'; a parametrized test asserts that for every fixture sentence, amounts.classify == rate implies charge_wording is None.\"},\n  {\"severity\": \"minor\", \"title\": \"State change and audit row are separate autocommit writes; a failed audit write leaves the item changed and no event (observed)\",\n   \"evidence\": \"reclassify.py:135 DB.update_item (autocommit, db.py:54 isolation_level=None); reclassify.py:137 batch_apply; reclassify.py:138 _log. Probe probe_reclassify_audit_route.py on c8a9874: 'POST reclassify a1 -> HTTP 500', 'a1 stored after request: kind=unclear', 'review_events for a1 (action, payload event): []'\",\n   \"why_it_matters\": \"The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).\",\n   \"fix\": \"Wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).\",\n   \"acceptance_test\": \"Monkeypatch RC._log to raise; assert the item kind is still charge after the call.\"},\n  {\"severity\": \"minor\", \"title\": \"A promoted charge is dropped silently when a rerun changes its sentence\",\n   \"evidence\": \"reclassify.py:188-189 'if rc.get(to) == charge and rc.get(excerpt_sha) != _sha(it.get(excerpt)): return it' discards the reclassification record with no note; tests/unit/test_reclassify.py:249-250 asserts only kind != charge\",\n   \"why_it_matters\": \"Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign that her promotion was withdrawn, and the item view does not say why the figure changed.\",\n   \"fix\": \"Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.\",\n   \"acceptance_test\": \"After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED and the item view names the reason.\"}\n ],\n \"whats_right\": [\n  \"reclassify.py:145-153 (_may_restore) refuses a restore after a class or sentence change; probe restore-class-only-flip-run.txt shows 422 JUDGE_UNAVAILABLE with the total at 0.\",\n  \"test_reclassify.py:161-171 refuses 'Charge per visit $185.' and 'Billed $150 per visit.' before the judge (call.log == []); mutant T84-1 fails 21 tests.\",\n  \"tests/unit/test_billing.py and app/backend/billing.py are identical to f218263, the billing route is registered at api.py:510, and 27 billing tests pass at a850be0.\"\n ],\n \"questions_for_chris\": [\"D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should 'Charged $150 an hour.', 'Charged $75 a unit.' and 'Billed $120 an appointment.' be refused by the code gate before the judge, given that the amount classifier calls them rates? The decision text does not say.\"]}\n```"
}
````

### User / tool · 2026-11-02T04:51:43.230Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-084-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:51:51.305Z

The write guard refuses Edit on an existing review file, so the r2 file cannot be patched in place. The guidance for corrections is a new suffixed file, so I'll write the complete review as `-r3` and state that it supersedes the invalid r2 file.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:19.065Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r3.md",
 "content": "# T-084 r2 review, filed as r3 (staff-engineer-reviewer, round 2)\n\nThis file supersedes `reviews/T-084-staff-engineer-r2.md`. That file was written without its ```json block, so the board validator rejects it, and the append-only guard refuses an in-place edit. Use this file for the T-084 round-2 verdict; do not register the r2 file.\n\nReviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (T-084 r2, committed with the T-073 r2 changes), with e2b4e3f (billing restored) underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both \"restore ... reverted by 2fca530\"). The verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad. The working tree has uncommitted edits to reclassify.py (it now imports `amounts.RATE_CUE`), amounts.py, billing.py and audited.py. Those are not reviewed here.\n\n## Summary\n\nThe three r1 invariants hold on HEAD for the paths the tests and probes reach, with two gaps. (1) A restore re-runs both checks when the sentence changes and when the code's class changes (reclassify.py:145-153), and the code is right for both. Only the sentence arm has a test, so a class-only change has no test that would catch the removal of its check (F1). (2) The code wording gate refuses \"Charge per visit $185.\" and \"Billed $150 per visit.\" before the judge, as the brief asks, and 17 rate-cue sentences. It still passes six unit-price phrasings that the amount classifier calls a rate or a unit price, so for those the judge is the only gate (F2).\n\nOne r1 blocker is closed, but not by this card. c8a9874 alone does not work: its own test file fails 9 of 120 tests, and a reclassify request returns 500 after it has already changed the item and written no audit row. HEAD a850be0 is correct because 6feb2ff restored the T-095 schema that 2fca530 had reverted. The card's commit list does not name 6feb2ff.\n\nBilling is back in HEAD and identical to f218263. The worker's extra behaviour (a promoted charge falls back to the code's class when a rerun changes its sentence) goes the safe direction, but it drops the paralegal's decision without a visible note (F4).\n\nVerdict: changes (0 blockers, 2 majors) on HEAD a850be0.\n\n## Exercised (what I actually ran or read)\n\n- `python3 tools/board.py show T-084`, `show T-094`, `show T-095` (header).\n- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44, then a850be0); `git show --stat` for c8a9874, e2b4e3f, 6feb2ff, a850be0.\n- `git show c8a9874:app/db/schema.sql | grep -c \"'reclassify'\"` = 0; a850be0 schema.sql:57 has 'reclassify' and 'rejudge'.\n- `git diff --stat bc12d44 a850be0` over the in-scope files: only app/db/db.py and app/db/schema.sql. `git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py`: empty. `git ls-tree -r --name-only a850be0 | grep -i billing`: both files. a850be0 api.py lines 510 (billing) and 512 (reclassify).\n- `git blame -L 496,502 a850be0 -- app/backend/pipeline.py`: lines 500-501 from 865b1865 (T-085).\n- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed. The 9 failures are all in test_reclassify.py, with `IntegrityError` at reclassify.py:90 and `assert (500 == 200)` in test_route.\n- `.venv/bin/python -m pytest -q tests/unit/test_audited.py` at a850be0: 19 passed. `tests/unit/test_billing.py`: 27 passed.\n- `.venv/bin/python -m pytest -q tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. The 7 are test_e2e_contract::test_every_test_id_is_declared, test_t037_backend::test_cli_sample_on_fixture_backend_under_60s, test_t075_determinism::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2, and four in test_trace.py. The handoff's \"1417 pass\" was measured on the working tree.\n- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` in the a850be0 archive: `UnboundLocalError: cannot access local variable 'raw'` at pipeline.py:501.\n- Read in full at a850be0: app/backend/reclassify.py and tests/unit/test_reclassify.py (both unchanged since bc12d44), app/backend/judge_guard.py, app/llm/audited.py. Also db.py:54 (autocommit), :215, :227, :287 (BEGIN); amounts.py:14 (`_UNIT`).\n- Probes in `artifacts/review-evidence/T-073-T-084-r2/`, each run as `.venv/bin/python -I <probe> <archive root>`: `probe_reclassify_audit_route.py` (c8a9874: HTTP 500, stored kind changed to unclear, `review_events` empty; a850be0: HTTP 200, one reclassify event); `probe_rate_cue_gaps.py` (output `rate-cue-gaps-run.txt`); `probe_classifier_vs_wording_gate.py` (output `classifier-vs-gate-run.txt`); `probe_restore_class_only_flip.py` on a850be0 and on mutant m03 (output `restore-class-only-flip-run.txt`).\n- Scratch mutants via `mutate_r2.py` on copies of the archive (log `mutation-run-r2.txt`). Control 139 passed. T84-1 (rate cue removed from the wording gate) 21 failed; T84-2 ('per' removed from the rate-cue pattern) 11 failed; T84-3 (restore ignores the code class) 139 passed; T84-4 (restore ignores the sentence change) 1 failed; T84-5 (restore always skips the checks, the r1 bug) 2 failed; T84-6 (promoted charge kept when its sentence changes) 1 failed. T73-1 to T73-4 are in the T-073 r2 review.\n- `grep -rn \"judge_guard.guarded\" app/`: review.py:102 and reclassify.py:167 only.\n\n## Findings\n\n### F1 (major): restore after a class-only change is untested; mutant T84-3 survives\n\n- The code is right. `_may_restore` (reclassify.py:145-153) requires `rerun.code_class == \"charge\"` and an unchanged sentence sha. Probe `probe_restore_class_only_flip.py` on a850be0 (the rerun changes only the code's class of $310; the excerpt is identical): `4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE`; `5. stored kind = unclear`; `pending total cents = 0`.\n- The gap is the test. Mutant T84-3 (reclassify.py:153 without the class clause) passes all 139 tests. The same probe on that mutant gives `restored=True kind=charge` and `pending total cents = 31000`.\n- The tests cover the sentence arm only. test_reclassify.py:190 `RATE_R3` changes the sentence and the class together; test_reclassify.py:198-216 uses it. test_reclassify.py:219-230 changes the sentence only.\n- Why it matters: the brief asks that a restore re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to `_may_restore` can reopen the r1 blocker with no failing test.\n- Fix: patch `amounts.classify` so the rerun's code class of $310 is \"rate\" while the excerpt is identical. `reclassify(..., {\"to\": \"charge\"}, call=None)` must raise 422 JUDGE_UNAVAILABLE with the item still `unclear`. Add the same case with `call=FakeCall(J2(\"agree\"))`: the judge is called once and `restored` is False. Keep test_reclassify.py:233-240 passing.\n- Acceptance test: mutant T84-3 fails the new test.\n\n### F2 (major): the code wording gate passes unit-price phrasings that the amount classifier calls rates\n\n- Probe `probe_classifier_vs_wording_gate.py`: \"Charged $150 an hour.\" is `rate` by amounts.classify and passes charge_wording; \"Charged $75 a unit.\" is `rate` and passes; \"Billed $120 an appointment.\" is `rate` and passes. amounts.py:14 `_UNIT` includes hour, unit and appointment; the gate's rate-cue pattern (reclassify.py:31-33) has none of them.\n- Probe `probe_rate_cue_gaps.py`: \"Billed $150 hourly.\", \"Charged $90 apiece.\", \"Billed $40 daily.\" and \"Billed $200 a month.\" also pass the code gate. The two named strings are refused, so F2 is not about the brief's named cases.\n- Why it matters: D-042 as written is met, because the sentence has charged wording and the judge re-checks it. But the code gate and the classifier disagree about the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.\n- Fix: one rate-unit test shared by amounts.classify and reclassify.charge_wording. The uncommitted working tree already moves toward `amounts.RATE_CUE` (not reviewed here). Whatever lands, refuse the six phrasings before the judge.\n- Acceptance test: `charge_wording` returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for \"Charged $150 an hour.\", \"Charged $75 a unit.\" and \"Billed $120 an appointment.\"; a parametrized test asserts that for every fixture sentence, `amounts.classify == \"rate\"` implies `charge_wording is None`.\n\n### F3 (minor): the state change and its audit row are separate autocommit writes; the consequence is observed\n\n- reclassify.py:135 `DB.update_item` commits on its own (db.py:54 `isolation_level=None`). reclassify.py:137 `review.batch_apply` (for a non-pending item) and reclassify.py:138 `_log` follow as separate statements.\n- Observed on c8a9874: `POST reclassify a1 -> HTTP 500`, `a1 stored after request: kind=unclear`, `review_events for a1: []`. The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).\n- Fix: wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as `apply_review` does (db.py:227, :287).\n- Acceptance test: monkeypatch `RC._log` to raise; assert the item's kind is still `charge` after the call.\n\n### F4 (minor): a promoted charge is dropped silently when its sentence changes\n\n- reclassify.py:188-189 returns the fresh item when the sentence sha differs, which discards the reclassification record with no note. The figure falls back to the code's class (fail-closed: it leaves the total).\n- test_reclassify.py:249-250 asserts only `kind != \"charge\"`. The audit row stays, but the item view does not say why the figure changed.\n- Fix: keep the record with `dropped: \"SENTENCE_CHANGED\"` in `ladder.reclassification` and show it in the item view and stepper.\n- Acceptance test: after a sentence change, `item.ladder.reclassification.dropped == \"SENTENCE_CHANGED\"`.\n\n## Closed at HEAD (not findings at a850be0)\n\n- c8a9874 on its own tree (blocker at c8a9874, closed at HEAD). `git show c8a9874:app/db/schema.sql` has no 'reclassify' in the CHECK, while reclassify.py:27 sets `AUDIT_ACTION = \"reclassify\"`. The INSERT fails with IntegrityError (reclassify.py:90), the route returns 500, and the item is already changed (F3). 2fca530 (T-087/T-086, a sibling commit) reverted the T-095 CHECK and migration; 6feb2ff (\"fix: restore T-095 work reverted by 2fca530\") restored them. At a850be0 the CHECK is at schema.sql:57, SCHEMA_VERSION is 4 (db.py:33), the four files pass 120 of 120, and the probe returns 200 with a `reclassify` event. The card should cite 6feb2ff, since c8a9874 alone does not pass.\n- r1 F4 (audit action 'edit'): closed. AUDIT_ACTION is \"reclassify\" (reclassify.py:27) and test_route (test_reclassify.py:319) asserts `[\"reclassify\"]`, which passes at HEAD.\n- r1 F2 (billing removed by ec33bf0): closed. billing.py and test_billing.py are identical to f218263 at a850be0; api.py:510 registers the routes; test_billing.py passes (27).\n- r1 F1 (restore after a rerun), sentence arm: closed. Mutants T84-4, T84-5 and T84-6 fail 1, 2 and 1 tests. Class arm: code correct (probe), test missing (F1).\n- r1 F3 (rate phrase passes the wording gate), named strings: closed. \"Charge per visit $185.\" and \"Billed $150 per visit.\" are refused before the judge (test_reclassify.py:161-171, `call.log == []`). Mutant T84-1 fails 21 tests and T84-2 fails 11. The remaining gap is F2.\n\n## Judgement on the worker's extra behaviour\n\nA promoted charge falls back to the code's class when a rerun changes its sentence (reclassify.py:188-189). I judge this right: it fails closed, and it applies the same rule as the restore path (a sentence change means the earlier judge answer no longer applies). The silent drop is F4.\n\n## What is right\n\n- reclassify.py:145-153 (`_may_restore`) requires a charge original, a previous judge, and, after any rerun, the same sentence sha and a charge code class. The probe confirms the refusal (422 JUDGE_UNAVAILABLE, total 0).\n- The refusals stay before the judge: test_reclassify.py:170 asserts `call.log == []` and the item stays `rate`, `needs_review`.\n- Billing is back in HEAD: identical to f218263, registered at api.py:510, 27 tests pass.\n\n## Outside these cards (observed at a850be0, not attributed to T-073 or T-084)\n\n- The sample CLI crashes: `python -m app.pipeline evals/golden/sample.txt` ends in UnboundLocalError at pipeline.py:501. `git blame` puts lines 500-501 in 865b1865 (T-085). This is persona checklist item 20, and it fails on HEAD.\n- Seven unit tests fail at a850be0 (listed in Exercised). I did not trace them to a cause. None is in the T-073 or T-084 files.\n\n## Scores\n\n```\nno_rate_into_total_without_both_checks 3 (both checks run on every path; the class-only restore is untested, F1; the code gate passes six classifier-rate phrasings, F2)\nrestore_rule_tested 3 (sentence arm killed; class arm not, F1)\ncode_check_strength 2 (named strings and 17 cues refused; six classifier-rate phrasings pass, F2)\njudge_gate 4 (judge disagree, unsure and unavailable give 422 with nothing changed)\naudit_trail 3 (written at HEAD; the item change and the audit row are not one transaction, F3; the promoted drop is not shown, F4)\ncommit_integrity 2 (c8a9874 alone fails 9 tests and returns 500 with the item changed; closed at HEAD by 6feb2ff, which is not in this card's commit list)\nbilling_restored 5 (identical to f218263; route registered; 27 tests pass)\ntests_kill_mutants 4 (T84-1, T84-2, T84-4, T84-5, T84-6 and the four T-073 mutants killed; T84-3 survives)\n```\n\n## Questions for Chris\n\n- D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should \"Charged $150 an hour.\", \"Charged $75 a unit.\" and \"Billed $120 an appointment.\" be refused by the code gate before the judge, given that the amount classifier calls them rates? My reading is that they should be refused. The decision text does not say.\n\n```json\n{\"card\": \"T-084\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit c8a9874 (T-084 r2, committed with the T-073 r2 changes) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/backend/reclassify.py, app/backend/amounts.py (read), app/backend/api.py (routes), app/db/db.py and app/db/schema.sql (read, restored by 6feb2ff), tests/unit/test_reclassify.py, tests/unit/test_billing.py; c8a9874 alone fails 9 tests and is closed at HEAD by 6feb2ff (not a finding at a850be0); no app URL; the sample CLI run at a850be0 crashes (outside this card, see body)\",\n \"exercised\": [\"python3 tools/board.py show T-084, T-094, T-095\", \"git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874, e2b4e3f, 6feb2ff, a850be0; git show c8a9874:app/db/schema.sql | grep -c reclassify (0); git diff --stat bc12d44 a850be0 over the in-scope files (db.py and schema.sql only); git diff --stat f218263 a850be0 over the billing files (empty); git ls-tree a850be0 | grep billing (both files); a850be0 api.py lines 510 and 512; git blame -L 496,502 a850be0 -- app/backend/pipeline.py\", \".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; a850be0 120 passed; c8a9874 9 failed 111 passed (IntegrityError at reclassify.py:90)\", \".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed; tests/unit/test_billing.py: 27 passed; tests/unit at a850be0: 7 failed 1392 passed 2 skipped\", \".venv/bin/python -m app.pipeline evals/golden/sample.txt at a850be0: UnboundLocalError at pipeline.py:501\", \"read in full at a850be0: reclassify.py and test_reclassify.py (both unchanged since bc12d44), judge_guard.py, audited.py; db.py:54, :215, :227, :287; amounts.py:14\", \"probes via .venv/bin/python -I in artifacts/review-evidence/T-073-T-084-r2/: probe_reclassify_audit_route.py (c8a9874: HTTP 500, item changed, no event; a850be0: HTTP 200, one reclassify event); probe_rate_cue_gaps.py (rate-cue-gaps-run.txt); probe_classifier_vs_wording_gate.py (classifier-vs-gate-run.txt); probe_restore_class_only_flip.py on a850be0 (422 JUDGE_UNAVAILABLE, total 0) and on mutant m03 (restored, total 31000; restore-class-only-flip-run.txt)\", \"scratch mutants via mutate_r2.py (mutation-run-r2.txt): control 139 passed; T84-1 21 failed; T84-2 11 failed; T84-3 139 passed (survives); T84-4 1 failed; T84-5 2 failed; T84-6 1 failed\", \"grep -rn judge_guard.guarded app/ (review.py:102 and reclassify.py:167 only)\"],\n \"verdict\": \"changes\",\n \"scores\": {\"no_rate_into_total_without_both_checks\": 3, \"restore_rule_tested\": 3, \"code_check_strength\": 2, \"judge_gate\": 4, \"audit_trail\": 3, \"commit_integrity\": 2, \"billing_restored\": 5, \"tests_kill_mutants\": 4},\n \"findings\": [\n  {\"severity\": \"major\", \"title\": \"Restore after a class-only change is untested; mutant T84-3 (restore ignores the rerun's code class) passes all 139 tests\",\n   \"evidence\": \"reclassify.py:153 'return rerun.get(code_class) == charge and rerun.get(excerpt_sha) == prior.get(excerpt_sha) == _sha(row[excerpt])'; mutant without the class clause: mutation-run-r2.txt 'T84-3 ... 139 passed'; restore-class-only-flip-run.txt: HEAD '4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE', mutant 'restored=True kind=charge' and 'pending total cents = 31000'; tests/unit/test_reclassify.py:190 RATE_R3 and :198-216 change the sentence, not only the class\",\n   \"why_it_matters\": \"The brief requires a restore to re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to _may_restore can reopen the r1 blocker and no test fails.\",\n   \"fix\": \"Add a test that patches amounts.classify so the rerun's code class of $310 is rate while the excerpt is identical; reclassify to charge with call=None must raise 422 JUDGE_UNAVAILABLE with the item still unclear. Add the same case with call=FakeCall(J2 agree): the judge is called once and restored is False. Keep test_reclassify.py:233-240 passing.\",\n   \"acceptance_test\": \"Mutant T84-3 (reclassify.py:153 without the code_class clause) fails the new test.\"},\n  {\"severity\": \"major\", \"title\": \"The code wording gate passes unit-price phrasings that the amount classifier calls rates, so the judge is the only gate for them\",\n   \"evidence\": \"classifier-vs-gate-run.txt: 'Charged $150 an hour.' classifier rate, gate passes (Charged); 'Charged $75 a unit.' rate, passes; 'Billed $120 an appointment.' rate, passes. rate-cue-gaps-run.txt: 'Billed $150 hourly.', 'Charged $90 apiece.', 'Billed $40 daily.', 'Billed $200 a month.' pass the gate. reclassify.py:31-33 _RATE_CUE has no hour, unit or appointment; amounts.py:14 _UNIT = (visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?\",\n   \"why_it_matters\": \"D-042 as written is met (charged wording plus a judge re-check), but the code gate and the classifier disagree on the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.\",\n   \"fix\": \"Use one rate-unit test for amounts.classify and reclassify.charge_wording (the uncommitted working tree already moves toward amounts.RATE_CUE; not reviewed here). Refuse the six phrasings before the judge.\",\n   \"acceptance_test\": \"charge_wording returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for 'Charged $150 an hour.', 'Charged $75 a unit.', 'Billed $120 an appointment.'; a parametrized test asserts that for every fixture sentence, amounts.classify == rate implies charge_wording is None.\"},\n  {\"severity\": \"minor\", \"title\": \"State change and audit row are separate autocommit writes; a failed audit write leaves the item changed and no event (observed)\",\n   \"evidence\": \"reclassify.py:135 DB.update_item (autocommit, db.py:54 isolation_level=None); reclassify.py:137 batch_apply; reclassify.py:138 _log. Probe probe_reclassify_audit_route.py on c8a9874: 'POST reclassify a1 -> HTTP 500', 'a1 stored after request: kind=unclear', 'review_events for a1 (action, payload event): []'\",\n   \"why_it_matters\": \"The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).\",\n   \"fix\": \"Wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).\",\n   \"acceptance_test\": \"Monkeypatch RC._log to raise; assert the item kind is still charge after the call.\"},\n  {\"severity\": \"minor\", \"title\": \"A promoted charge is dropped silently when a rerun changes its sentence\",\n   \"evidence\": \"reclassify.py:188-189 'if rc.get(to) == charge and rc.get(excerpt_sha) != _sha(it.get(excerpt)): return it' discards the reclassification record with no note; tests/unit/test_reclassify.py:249-250 asserts only kind != charge\",\n   \"why_it_matters\": \"Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign that her promotion was withdrawn, and the item view does not say why the figure changed.\",\n   \"fix\": \"Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.\",\n   \"acceptance_test\": \"After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED and the item view names the reason.\"}\n ],\n \"whats_right\": [\n  \"reclassify.py:145-153 (_may_restore) refuses a restore after a class or sentence change; probe restore-class-only-flip-run.txt shows 422 JUDGE_UNAVAILABLE with the total at 0.\",\n  \"test_reclassify.py:161-171 refuses 'Charge per visit $185.' and 'Billed $150 per visit.' before the judge (call.log == []); mutant T84-1 fails 21 tests.\",\n  \"tests/unit/test_billing.py and app/backend/billing.py are identical to f218263, the billing route is registered at api.py:510, and 27 billing tests pass at a850be0.\"\n ],\n \"questions_for_chris\": [\"D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should 'Charged $150 an hour.', 'Charged $75 a unit.' and 'Billed $120 an appointment.' be refused by the code gate before the judge, given that the amount classifier calls them rates? The decision text does not say.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T04:52:19.216Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:21.809Z

The r3 file was accepted by the validator on write. I'll run the read-only board validator to confirm the state of all four review files before I update memory.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:22.643Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -15; echo \"exit=$?\"; echo \"--- json block presence\"; for f in reviews/T-073-staff-engineer-r2.md reviews/T-084-staff-engineer-r2.md reviews/T-084-staff-engineer-r3.md; do echo \"$f json-fences=$(grep -c '^```json' $f)\"; done",
 "description": "Run read-only board validation and count JSON fences in the review files"
}
````

### User / tool · 2026-11-02T04:52:22.804Z

**tool result**
````
ok (97 file(s))
exit=0
--- json block presence
reviews/T-073-staff-engineer-r2.md json-fences=1
reviews/T-084-staff-engineer-r2.md json-fences=0
reviews/T-084-staff-engineer-r3.md json-fences=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:25.015Z

The validator reports ok, but the r2 file still has no JSON fence. I'll parse the JSON blocks in the two valid files to confirm they load.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:26.311Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport json,re\nfor f in [\"reviews/T-073-staff-engineer-r2.md\",\"reviews/T-084-staff-engineer-r3.md\"]:\n    s=open(f,encoding=\"utf-8\").read()\n    m=re.search(r\"```json\\n(.*?)\\n```\", s, re.S)\n    d=json.loads(m.group(1))\n    sev=[x[\"severity\"] for x in d[\"findings\"]]\n    v=d[\"verdict\"]\n    rule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\n    print(f, \"card=\",d[\"card\"], \"persona=\",d[\"persona\"], \"model=\",d[\"model\"], \"verdict=\",v, \"rule=\",rule, \"match=\", v==rule, \"findings=\",sev)\nEOF",
 "description": "Parse both review JSON blocks and check the verdict rule"
}
````

### User / tool · 2026-11-02T04:52:26.411Z

**tool result**
````
reviews/T-073-staff-engineer-r2.md card= T-073 persona= staff-engineer-reviewer model= claude-haiku-5-5 verdict= pass rule= pass match= True findings= ['minor', 'minor', 'nit']
reviews/T-084-staff-engineer-r3.md card= T-084 persona= staff-engineer-reviewer model= claude-haiku-5-5 verdict= changes rule= changes match= True findings= ['major', 'major', 'minor', 'minor']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:30.427Z

Both JSON blocks parse, and each verdict matches the verdict rule. Last, I'll update my memory: the r2 outcomes for T-073/T-084, the write-guard lesson about the JSON block, and the worktree guard.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:31.135Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && grep -ril \"worktree\" . ; echo \"---\"; grep -n \"worktree\" project_harness_review_patterns.md | head -5; echo \"---\"; grep -n \"t073_t084\\|T-073\" MEMORY.md",
 "description": "Check memory for existing worktree notes and the T-073/T-084 index line"
}
````

### User / tool · 2026-11-02T04:52:31.237Z

**tool result**
````
project_t095_head_revert_patterns.md
project_t093_signature_controls_patterns.md
project_harness_review_patterns.md
---
40:- (T-090 r2, 2026-11-01) `->` inside a `python -c` print string is read as a redirect ("redirect to 84"); `git worktree` is denied in the project ("allowed only in scratch repos under /tmp"). Use `git clone <project> <scratch>/clone` then `git checkout --detach <sha>` inside the clone. `git checkout` in the clone was denied once when the Bash cwd had been the project; split the call and use a saved pristine copy plus `cp` to restore a mutated file. `-I` runs need `sys.path.insert(0, clone)` plus `runpy.run_module` because `-I` drops cwd from sys.path.
41:- (T-093 r2, 2026-11-02) board-guard denies `git worktree` in the project and `git worktree list` too, even with a scratchpad path under /private/tmp ("allowed only in scratch repos under /tmp"). Use `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-<sha>/` for a clean HEAD tree; it covers tracked files only, which is what a clean worktree gives. `rm -rf` of that copy was denied, so leave it and say so in `exercised`.
43:- (T-088/T-089 r2, 2026-11-02) board-guard denied `git worktree` in the project; `git archive <sha> | tar -x -C artifacts/review-evidence/<card>-r2/clean` worked. git-guard failed closed on `H=$(git rev-parse HEAD)` in command position, so use literal shas. reviewer-write-guard denied an Edit to my own existing `reviews/T-089-staff-engineer-r2.md` (append-only), so a wrong summary sentence stayed and was disclosed in the reply; proof-read the summary before the first Write.
---
27:- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof (audited.py:70 hides bugs), T-084 r1 restore-after-rerun bypass, rate phrase passes wording, commit deleted T-083
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:34.284Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && ls -la && echo \"--- t095 file\" && cat project_t095_head_revert_patterns.md && echo \"--- MEMORY.md tail\" && tail -5 MEMORY.md",
 "description": "Read the existing T-095 revert memory and the memory index tail"
}
````

### User / tool · 2026-11-02T04:52:34.388Z

**tool result**
````
total 296
drwxr-xr-x@ 30 arsis  staff   960 Nov  1 22:51 .
drwxr-xr-x@ 17 arsis  staff   544 Nov  1 20:38 ..
-rw-r--r--@  1 arsis  staff  4991 Nov  1 22:51 MEMORY.md
-rw-r--r--@  1 arsis  staff  1141 Nov  1 21:42 feedback_review_write_once.md
-rw-r--r--@  1 arsis  staff  1132 Nov  1 20:37 feedback_severity_vs_brief.md
-rw-r--r--@  1 arsis  staff  2587 Nov  1 19:58 project_backend_llm_review_patterns.md
-rw-r--r--@  1 arsis  staff  1928 Nov  1 19:49 project_db_review_patterns.md
-rw-r--r--@  1 arsis  staff  5931 Nov  1 20:00 project_design_review_patterns.md
-rw-r--r--@  1 arsis  staff  3131 Nov  1 19:59 project_e2e_contract_review_patterns.md
-rw-r--r--@  1 arsis  staff  3886 Nov  1 20:12 project_eval_runner_review_patterns.md
-rw-r--r--@  1 arsis  staff  8144 Nov  1 22:51 project_harness_review_patterns.md
-rw-r--r--@  1 arsis  staff  3078 Nov  1 20:01 project_llm_stage_review_patterns.md
-rw-r--r--@  1 arsis  staff  2932 Nov  1 20:51 project_r2_fix_verification_patterns.md
-rw-r--r--@  1 arsis  staff  2703 Nov  1 20:20 project_round2_snapshot_review_patterns.md
-rw-r--r--@  1 arsis  staff  7305 Nov  1 20:44 project_split_llm_review_patterns.md
-rw-r--r--@  1 arsis  staff  3940 Nov  1 20:20 project_t050_namespacing_review_patterns.md
-rw-r--r--@  1 arsis  staff  7326 Nov  1 20:52 project_t063_doc_vs_code_review_patterns.md
-rw-r--r--@  1 arsis  staff  3970 Nov  1 20:57 project_t065_batch_fallback_review_patterns.md
-rw-r--r--@  1 arsis  staff  4390 Nov  1 21:04 project_t066_no_model_reason_patterns.md
-rw-r--r--@  1 arsis  staff  2519 Nov  1 21:29 project_t067_r6_d043_patterns.md
-rw-r--r--@  1 arsis  staff  4538 Nov  1 21:06 project_t070_t067_review_patterns.md
-rw-r--r--@  1 arsis  staff  3020 Nov  1 22:33 project_t073_t084_review_patterns.md
-rw-r--r--@  1 arsis  staff  2673 Nov  1 21:47 project_t075_determinism_review_patterns.md
-rw-r--r--@  1 arsis  staff  6430 Nov  1 22:08 project_t080_trace_review_patterns.md
-rw-r--r--@  1 arsis  staff  3178 Nov  1 22:34 project_t083_billing_review_patterns.md
-rw-r--r--@  1 arsis  staff  3722 Nov  1 22:46 project_t088_t089_review_patterns.md
-rw-r--r--@  1 arsis  staff  4203 Nov  1 22:39 project_t090_calibration_review_patterns.md
-rw-r--r--@  1 arsis  staff  3917 Nov  1 22:45 project_t093_signature_controls_patterns.md
-rw-r--r--@  1 arsis  staff  3579 Nov  1 22:51 project_t095_head_revert_patterns.md
-rw-r--r--@  1 arsis  staff  1645 Nov  1 19:53 project_wiring_review_patterns.md
--- t095 file
---
name: t095-head-revert-patterns
description: T-095 r1 (card commit 031a708) - a later commit (2fca530, T-086/T-087) silently reverted the card's files; HEAD moved twice mid-review; git worktree denied by board-guard, use git archive; migration probe and mutants
metadata:
  type: project
---

Recurring pattern from the T-095 review (v3 to v4 review_events migration, reclassify/rejudge actions). Review: reviews/T-095-staff-engineer.md, verdict fail.

- **A card can be "done" on the board while its commit is gone from HEAD.** 031a708 carried the change; 2fca530 (another card's commit, built from a stale shared index per the orchestrator lesson and the d3130e3 message) restored the pre-change bytes of all seven files. Check: `git diff --stat <card_commit>^ HEAD -- <card files>` must be empty, and `git diff --stat <card_commit> HEAD -- <files>` must not show removals of card lines. Do this before reviewing the commit's own content.
- **HEAD moves mid-review.** 02ff244 became 7df65fb during the review. Pin every tree by sha and re-run the tests on the current HEAD before writing the verdict.
- **Clean tree without git worktree:** board-guard denies `git worktree` for reviewers (and also matches the string in `git worktree list`). Use `git archive <sha> | tar -x -C <scratch dir>`; it gives the same clean tree and writes nothing to .git.
- **git-guard denies `$(...)` in command position** in Bash (e.g. `cd "$(mktemp ...)"`). Set variables with plain assignments.
- **Migration probe pattern (worked):** build a real vN file from `git show <sha>^:app/db/schema.sql`, insert mixed rows in every table, snapshot all tables, call connect(), compare every non-target table and every non-target column, check the action mapping with an independent rule, then force a mid-copy failure with an FK-orphan row (not by monkeypatching json.loads) and check the file is byte-for-byte the old state.
- **Mutant that survived on a rule change:** a substring match for `"reclassify" in after_json` passed all 101 tests. Tests must include a user edit whose text contains the trigger word.
- **Rollback test can pass without the ROLLBACK:** the test reads through a fresh connection, so a leaked open transaction looks the same. Assert `conn.in_transaction is False` on the migration connection.
- **AC count not reproducible:** the card claimed 1350 passed; the commit gives 1187. Claimed counts must come from a clean export of the commit.

Related: [[project_db_review_patterns]], [[project_harness_review_patterns]].

## r2 (HEAD 31b7ceb, reviews/T-095-staff-engineer-r2.md, verdict pass)

- **A restore can be partial.** 6feb2ff restored the four files that 2fca530 reverted. reclassify.py, rejudge.py and test_reclassify.py had been changed by later cards, so their diffs against 031a708 were non-empty and looked like a loss. Check the card's own lines by identifier (AUDIT_ACTION, `_log`, the `reclassify` assert), and grep the removed lines of `git diff <card> HEAD` for the same identifiers. Later-card hunks are fine.
- **Verdict pattern for a restore r2:** re-run the probe and mutants on a fresh archive of the new HEAD. The r1 minors that were untouched stayed open in r2, so cite each one with its mutant or grep result.
- **Out-of-scope HEAD breakage:** the sample CLI crashed at HEAD (pipeline.py:501, UnboundLocalError, from 865b186). Report it, but keep it out of the card's findings so the card verdict reflects the card.
- **Mutant copies:** `cp -R <archive> <scratch>/mut_X` with literal names works; `rm -rf` with a loop variable is denied by the hook.
--- MEMORY.md tail
- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263: card files deleted at HEAD by sibling commit, table rate rows totaled, silent line drops, tautological verifier, $0.00 total
- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible; r2 823b718/02ff244: fix reverted at HEAD by 2fca530, forged source_commit skips
- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof (audited.py:70 hides bugs), T-084 r1 restore-after-rerun bypass, rate phrase passes wording, commit deleted T-083
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:45.323Z

The memory index and the existing T-073/T-084 notes need the round-2 outcomes, plus two process lessons: the JSON block must be in the first Write, and the handoff cited an unrelated card. I'll update the notes now.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:49.898Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md",
 "old_string": "Related: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes).",
 "new_string": "## r2 (c8a9874 + e2b4e3f, HEAD a850be0; reviews/T-073-staff-engineer-r2.md pass, reviews/T-084-staff-engineer-r3.md changes)\n\n- **A fix commit can fail its own tree while the working tree is green.** c8a9874 alone: 9 of 120 fail (IntegrityError at reclassify.py:90) because it set AUDIT_ACTION to 'reclassify' while 2fca530 had removed the schema CHECK entry; the worker's runs were on a working tree that still had the T-095 schema uncommitted. A reclassify request 500'd and left the item changed with no audit row. Closed at HEAD by 6feb2ff (T-095 restore). **Why:** worker test runs use the working tree. **How to apply:** run the card's test files on `git archive <card commit>` as well as HEAD, and check any schema or migration the constants depend on. See [[project_t095_head_revert_patterns]].\n- **Two-arm predicate with one arm untested:** `_may_restore` skips the checks only when the class AND the sentence are unchanged. The tests changed both together, so dropping the class clause passed all 139 tests (mutant T84-3). The code was right; the test was missing. **How to apply:** for each `and`-clause of a guard predicate, write a test where only that input changes, and mutate each clause separately.\n- **Gate and classifier disagree on the same sentence:** charge_wording used its own rate-cue list; amounts.classify uses `_UNIT` (hour, unit, appointment). Six phrasings the classifier calls rates (\"Charged $150 an hour.\", \"Charged $75 a unit.\", \"Billed $120 an appointment.\") passed the gate, so the judge was the only gate. **How to apply:** run both functions on the same fixture sentences and list the disagreements (probe_classifier_vs_wording_gate.py pattern).\n- **Restored sentence-arm mutants were caught;** the class-only arm was not. The worker's \"17 rate cues\" test pinned the named strings, not the classifier's vocabulary.\n- **Handoff cites a card that is unrelated:** T-073's deferral said \"T-094\"; `board.py show T-094` is a live ship-bar card. **How to apply:** for every card a handoff names, check `board.py show` returns the matching work.\n- **Probe and mutant indexing:** mutate_r2 writes m00..m10 in list order (control is m00, T84-3 is m03). I ran the T84-4 mutant (m04) by mistake once; check the directory name against the log before a probe.\n\nRelated: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes), [[project_t095_head_revert_patterns]] (the 2fca530 revert, closed by 6feb2ff), [[feedback_review_write_once]] (the JSON block in the first Write)."
}
````

### User / tool · 2026-11-02T04:52:49.994Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:51.450Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md",
 "old_string": "**How to apply:** before the first Write of a review, grep every cited line number and re-check each \"checked and fine\" claim against a command you actually ran.",
 "new_string": "**The ```json block belongs to the first Write.** T-084 r2 (this session): I wrote `reviews/T-084-staff-engineer-r2.md` without its json fence. The board-validate PostToolUse hook rejected it (\"review must contain a ```json block\"), and reviewer-write-guard refused the Edit that would have added it. The fix was a complete `-r3` file that says it supersedes the r2 file. **How to apply:** before the Write, count the fences (exactly one ```json block) and parse the block with `json.loads`; check the verdict against the rule.\n\n**How to apply:** before the first Write of a review, grep every cited line number and re-check each \"checked and fine\" claim against a command you actually ran."
}
````

### User / tool · 2026-11-02T04:52:51.551Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:52.523Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof (audited.py:70 hides bugs), T-084 r1 restore-after-rerun bypass, rate phrase passes wording, commit deleted T-083",
 "new_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass, rate phrase; r2 c8a9874 fails its own tree (closed 6feb2ff), class-only restore untested, gate vs classifier gap"
}
````

### User / tool · 2026-11-02T04:52:52.627Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:55.162Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md",
 "old_string": "description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording, commit deleted T-083 billing",
 "new_string": "description: T-073 r1 narrowed catch (audited.py:70); T-084 r1 restore bypass, rate phrase, commit deleted T-083 billing; r2 (c8a9874, HEAD a850be0) commit fails its own tree, class-only restore untested, gate passes classifier-rate phrasings"
}
````

### User / tool · 2026-11-02T04:52:55.165Z

**tool result (error)**
````
<tool_use_error>String to replace not found in file.
String: description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording, commit deleted T-083 billing</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:57.171Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && head -4 project_t073_t084_review_patterns.md",
 "description": "Read the frontmatter of the T-073/T-084 memory file"
}
````

### User / tool · 2026-11-02T04:52:57.262Z

**tool result**
````
---
name: t073-t084-review-patterns
description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording gate, commit deleted T-083 billing
metadata:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:52:59.262Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md",
 "old_string": "description: T-073 r1 (7724412) narrowed catch fixed at unit seam only, real path retries bugs via audited.py:70; T-084 r1 (ec33bf0) restore-after-rerun bypass, rate-phrase passes wording gate, commit deleted T-083 billing",
 "new_string": "description: T-073 r1 (7724412) narrowed catch, real path retries bugs; T-084 r1 (ec33bf0) restore bypass, rate phrase, commit deleted T-083 billing; r2 (c8a9874, HEAD a850be0) commit fails its own tree, class-only restore untested, gate passes classifier-rate phrasings"
}
````

### User / tool · 2026-11-02T04:52:59.363Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:53:02.561Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- (T-093 r2, 2026-11-02) board-guard denies `git worktree` in the project",
 "new_string": "- (T-073/T-084 r2, 2026-11-02) `timeout` is not installed on this macOS host (`timeout: command not found`); use the Bash tool's `timeout` parameter for long pytest runs. HEAD moved twice during the review (bc12d44 to 6feb2ff to a850be0): pin each sha with `git archive` and say which sha the verdict covers. `python -I` needs the archive root passed as an argument and `sys.path.insert(0, root)`, not PYTHONPATH.\n- (T-093 r2, 2026-11-02) board-guard denies `git worktree` in the project"
}
````

### User / tool · 2026-11-02T04:53:02.663Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:53:08.812Z

T-073 r2 passes and T-084 r2 needs changes (2 majors, 0 blockers): `/Users/arsis/zlayt-pm-project/reviews/T-073-staff-engineer-r2.md` and `/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r3.md`. The c8a9874 commit alone fails 9 tests and returns 500 with no audit row, which 6feb2ff fixed at HEAD a850be0. Billing is restored. Do not register `/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r2.md`: it has no JSON block and I could not edit it.
