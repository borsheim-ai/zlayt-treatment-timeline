# Subagent: T-038 r2 check (haiku) (T-038 r2 check (haiku))

Source: `agent-a86ad7c800cf56399.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:01:59.217Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-038 vs reviews/T-038-staff-engineer.md (majors: ship_bar_met true on 2 runs / --runs 1 crash; --check-spec leaves stale ship_bar_met; broad except blocks; 5 undetected bar mutations). Run `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2`, `.venv/bin/python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$?`, `grep -n "except Exception" evals/*.py`. Quote outputs. Pass if all 4 majors are resolved. Write reviews/T-038-staff-engineer-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:00.359Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:02:00.373Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:00.573Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-038-staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:02:00.579Z

**tool result**
````
1	# T-038 review - staff-engineer-reviewer (commit 40c882d, code-only parts)
2	
3	Verdict: changes. No blockers. Four majors. The full run waits for T-037, so I judged the code-only parts.
4	
5	Commands run:
6	
7	- `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -3` gave `24 passed, 673 deselected`.
8	- `.venv/bin/python -m evals.run --check-spec; echo rc=$?` printed `{"spec_matches_golden": true, "letter_equal": true, "internal_notes_equal": true}` and `rc=0`.
9	- A one-character change in a copy of REQUIREMENTS section 6 gave `spec_matches_golden: False`.
10	- `--check-fresh` against the current `latest.json` exits 1. That file holds only the spec fields because no full run has happened yet, so every prompt and the lexicon are listed as changed.
11	- `python -m evals.run` on the repo gets `AttributeError: module 'app.pipeline' has no attribute 'run_case'`. This is expected and visible, because T-037 is not built.
12	
13	What the report carries, checked in code and in the `Perfect` fake-pipeline report:
14	
15	| Item | Where |
16	|---|---|
17	| `ship_bar_met`, `bars`, `blockers` | `build_report` |
18	| `metrics` with `r_ids` | `RIDS`, `aggregate` |
19	| `backend`, `models`, `hashes` (sha256 of every prompt and `lexicon.yaml`) | `build_report` |
20	| `assertions.gap_28_not_flagged` and `gap_73_flagged` | `assertions` |
21	| `spec_matches_golden` | `check_spec` |
22	| `lexicon_recall_must_flags` with `gated: False`, outside the `ship_bar` function | `lexicon_recall` |
23	
24	Other checks:
25	
26	- On the fixture backend, `determinism_3run` and `unsupported_count_3run` are `{"value": None, "status": "not_measured"}`. `ship_bar_met` is false, with the blocker "need a live backend".
27	- `hallucination_catch_rate` is `caught / len(items)` over all 40 lines. All 50 lines of `hallucinations*.jsonl` parse with no fallback.
28	- `--check-fresh` exits 1 when a hash differs and exits 0 on a freshly written report.
29	
30	Scratch-copy mutations (11 on `evals/run.py`, tested against the three `test_eval_*` files, which pass `24 passed` on the unmutated copy):
31	
32	- Caught: hallucination denominator replaced with `caught`; `check_fresh` always 0; fixture blocker dropped; determinism and unsupported terms dropped from bar 4; gap-28 assertion always true; lexicon `gated: True`; must_not hits dropped from the bar; `grounding()` entry-excerpt check disabled; must_not regex disabled.
33	- Missed, with all 24 tests still green: controls-unsupported check dropped from the bar; case_07 term dropped from the bar; case_07 `not_run` counted as pass; `1_grounding` forced true; `score_record_warnings` check disabled; the `SUMMARY_DROPS_QUALIFIER` check in `entry_found` disabled.
34	
35	Findings:
36	
37	- **Major: the ship bar can be met on fewer than 3 runs.** `ship_bar` checks only `determinism_3run.value == 1.0`, never `runs >= 3`. With the fake pipeline, `build_report(..., runs=2)` gives `ship_bar_met True` with `determinism_3run` 1.0 and `runs` 2. `--runs 1` crashes with `ZeroDivisionError`.
38	- **Major: `--check-spec` leaves a stale `ship_bar_met`.** I wrote a full report with `ship_bar_met` true, made `check_spec` return false, and ran `--check-spec` (rc 1). `latest.json` then read `ship_bar_met = True` and `spec_matches_golden = False` with `blockers = []`. `main` does `data.update(s)` and never recomputes the bar. `evaluate_report` would catch it, but anyone reading the field would not.
39	- **Major: swallowed exceptions in the eval gate.** `run.py:316` has `except Exception: code = []`, and `run.py:490` has `except Exception: check = None`. A crash in `check_summary` silently turns the code-rung catch off. I reproduced it: with a `check_summary` that raises, `hallucination_metrics` returned 40/40 with no error surfaced. Only the lexicon `except` (`run.py:503`) records the error type.
40	- **Major: bar tests are weak.** `test_each_missed_bar_flips_ship_bar_met_false` asserts only `ship_bar_met is False and blockers`, not which bar failed, so another bar can satisfy it. The mutations listed above go unnoticed.
41	- AC8 is orchestrator-owned and not done, as the card says. AC1, AC3, AC4 and AC6 are open until a real run after T-037. I did not count either as a finding.
42	
43	```json
44	{"card": "T-038", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
45	 "scope": "commit 40c882d: evals/run.py, evals/matching.py, tests/unit/test_eval_{runner,matching,spec_check}.py; code-only parts (full run awaits T-037); fake-pipeline report",
46	 "exercised": ["board show T-038", "pytest tests/unit -k eval: 24 passed", "python -m evals.run --check-spec: true rc=0", "--check-spec on a 1-char-mutated copy of REQUIREMENTS: false", "--check-fresh on current latest.json: rc 1 (no hashes yet); on a fresh full report: rc 0", "python -m evals.run on repo: AttributeError run_case (T-037 absent, visible)", "read evals/run.py in full, test_eval_runner.py in full", "build_report with Perfect fake: runs=3 and runs=2 both ship_bar_met True; runs=1 ZeroDivisionError", "--check-spec over a full report with spec forced false: stale ship_bar_met True", "hallucination_metrics with raising check_summary: 40/40, no error", "parse_record_text on all 50 jsonl lines: no fallback", "11 scratch-copy mutations of evals/run.py: 5 undetected", "grep except in evals/"],
47	 "verdict": "changes",
48	 "scores": {"determinism_and_code_vs_llm_split": 4, "failure_visibility": 2, "test_strength": 3, "spec_conformance": 4, "ship_bar_integrity": 3},
49	 "findings": [
50	  {"severity": "major", "title": "ship_bar_met can be true on fewer than 3 runs; --runs 1 crashes",
51	   "evidence": "evals/run.py:462 `m[\"determinism_3run\"].get(\"value\") == 1.0` with no runs check; evals/run.py:353 `sum(...)/(runs - 1)`; repro: R.build_report(Perfect('claude-cli'),'claude-cli',2) -> ship_bar_met True, determinism_3run runs=2; runs=1 -> ZeroDivisionError.",
52	   "why_it_matters": "R-CO-7 and AC4 define a 3-run measurement. A 2-run pass is reported as determinism_3run and can satisfy the ship bar, so the label overstates the evidence.",
53	   "fix": "Require runs >= 3 in ship_bar (value measured and runs >= 3), and reject --runs < 3 in argparse (or clamp with a visible message).",
54	   "acceptance_test": "test: build_report(..., runs=2) has ship_bar_met False with a blocker naming the run count; --runs 1 exits with a usage error, not a traceback."},
55	  {"severity": "major", "title": "--check-spec writes spec_matches_golden but leaves a stale ship_bar_met in latest.json",
56	   "evidence": "evals/run.py:592-596 `data.update(s)` only. Repro: write full report (ship_bar_met true); force check_spec false; main(['--check-spec','--out',d]) rc 1; latest.json -> ship_bar_met True, spec_matches_golden False, blockers [].",
57	   "why_it_matters": "latest.json becomes self-contradictory and T-045's AC reads ship_bar_met directly; a false spec check would not block the milestone.",
58	   "fix": "After merging the spec fields, recompute with evaluate_report (or null/blocker the stale fields) when the file is a full report.",
59	   "acceptance_test": "test: full report with ship_bar_met true + --check-spec failing -> latest.json ship_bar_met false with blocker 'spec_matches_golden is false'."},
60	  {"severity": "major", "title": "Swallowed exceptions in the eval gate hide a broken code rung",
61	   "evidence": "evals/run.py:316 `except Exception: code = []`; evals/run.py:490 `except Exception: check = None`. Repro: hallucination_metrics(items, controls, judge=lambda *a: 'unsupported', check_summary=raising) -> caught 40/40, no error recorded.",
62	   "why_it_matters": "Checklist 12 and honest failure. If grounding.check_summary breaks, the report can still show a passing catch rate from the judge alone, and nobody learns the code rung was off. The report cannot be audited for which rung caught what.",
63	   "fix": "Let the error propagate, or record `code_rung_error` per item in the metric and count it as a blocker. Import grounding without a fallback.",
64	   "acceptance_test": "test: a raising check_summary makes build_report/hallucination_metrics raise or set a blocker; the report records how many were code-caught versus judge-caught."},
65	  {"severity": "major", "title": "Bar tests assert only 'false', so several bars and scorers are unproven",
66	   "evidence": "Scratch mutations with all 24 tests still green: drop `not m[\"hallucination_catch_rate\"][\"controls_unsupported\"]` from bar 4; drop `m[\"case_07_total_420\"][\"value\"] is True` from bar 4; case_07 `not_run` -> value True (evals/run.py:445); `\"1_grounding\": True`; score_record_warnings `if not (flagged and review)` -> False; entry_found SUMMARY_DROPS_QUALIFIER check disabled. test_each_missed_bar_flips_ship_bar_met_false asserts `ship_bar_met is False and r[\"blockers\"]` only.",
67	   "why_it_matters": "AC3 requires 'no control returns unsupported', and AC5 requires false when any bar is missed; the controls clause and the individual bar flags can be removed without any test noticing. A false-pass on the ship bar is the failure this card exists to prevent.",
68	   "fix": "Assert the named bar in r['bars'] per case (e.g. bars['1_grounding'] is False); add tests for: controls judged unsupported alone fails bar 4; case_07 not_run fails; record-warning miss counts in golden_must_not_hits; summary dropping a qualifier is a miss in entry_recall.",
69	   "acceptance_test": "Re-run the six listed scratch mutations: each makes at least one test fail."}
70	 ],
71	 "whats_right": ["On fixture, determinism_3run and unsupported_count_3run are null/not_measured and ship_bar_met is false (test + code), and a tampered report is recomputed by evaluate_report.", "hallucination_catch_rate is a rate over every line (40 of 40 parse) with controls scored separately, and lexicon_recall_must_flags is reported with gated:false outside ship_bar (D-026).", "check_fresh hashes every prompt and the lexicon, exits 1 on any difference or missing file, and the spec check is byte-exact (a one-char change flips it)."],
72	 "questions_for_chris": []}
73	```
74	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:00.774Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:02:00.780Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:04.634Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2; echo \"---\"; .venv/bin/python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$?; echo \"---\"; grep -n \"except Exception\" evals/*.py; echo \"grep_rc=$?\"",
 "description": "Run eval tests, --runs 1 check, and grep broad excepts"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:05.222Z

**tool call — Bash**
````
{
 "command": "ls -la evals/ tests/unit/ | head -80; echo \"---\"; wc -l evals/run.py evals/matching.py; echo \"---\"; grep -n \"def \\|except\\|runs\" evals/run.py | head -200",
 "description": "List eval files and locate functions, excepts, and runs logic"
}
````

### User / tool · 2026-11-02T02:02:08.063Z

**tool result**
````
.....................................                                    [100%]
37 passed, 718 deselected in 2.00s
---
rc=2
---
grep_rc=1
````

### User / tool · 2026-11-02T02:02:08.154Z

**tool result**
````
evals/:
total 112
drwxr-xr-x@  8 arsis  staff    256 Nov  1 20:01 .
drwxr-xr-x  24 arsis  staff    768 Nov  1 19:56 ..
-rw-r--r--@  1 arsis  staff      0 Nov  1 19:49 __init__.py
drwxr-xr-x@ 27 arsis  staff    864 Nov  1 19:52 golden
-rw-r--r--@  1 arsis  staff  14396 Nov  1 19:42 lexicon_heldout.jsonl
-rw-r--r--@  1 arsis  staff   2577 Nov  1 19:49 matching.py
drwxr-xr-x@  4 arsis  staff    128 Nov  1 20:02 reports
-rw-r--r--@  1 arsis  staff  33876 Nov  1 20:01 run.py

tests/unit/:
total 544
drwxr-xr-x@ 40 arsis  staff   1280 Nov  1 20:00 .
drwxr-xr-x@  7 arsis  staff    224 Nov  1 19:40 ..
-rw-r--r--@  1 arsis  staff      0 Nov  1 19:40 __init__.py
-rw-r--r--@  1 arsis  staff   3415 Nov  1 20:00 _fakes.py
-rw-r--r--@  1 arsis  staff   1056 Nov  1 19:40 _golden.py
-rw-r--r--@  1 arsis  staff   6886 Nov  1 19:59 test_amounts.py
-rw-r--r--@  1 arsis  staff   1741 Nov  1 19:54 test_api.py
-rw-r--r--@  1 arsis  staff  11101 Nov  1 20:01 test_api_routes.py
-rw-r--r--@  1 arsis  staff   5461 Nov  1 19:51 test_audited.py
-rw-r--r--@  1 arsis  staff   3863 Nov  1 19:46 test_boundaries.py
-rw-r--r--@  1 arsis  staff   6982 Nov  1 19:46 test_confidence.py
-rw-r--r--@  1 arsis  staff   2730 Nov  1 19:55 test_conflicts.py
-rw-r--r--@  1 arsis  staff   2440 Nov  1 19:42 test_dates.py
-rw-r--r--@  1 arsis  staff   9449 Nov  1 19:50 test_db.py
-rw-r--r--@  1 arsis  staff   1634 Nov  1 19:53 test_e2e_contract.py
-rw-r--r--@  1 arsis  staff   1453 Nov  1 19:49 test_eval_matching.py
-rw-r--r--@  1 arsis  staff  16986 Nov  1 20:00 test_eval_runner.py
-rw-r--r--@  1 arsis  staff   1295 Nov  1 19:53 test_eval_spec_check.py
-rw-r--r--@  1 arsis  staff  11095 Nov  1 19:53 test_export.py
-rw-r--r--@  1 arsis  staff   2043 Nov  1 19:54 test_export_edge.py
-rw-r--r--@  1 arsis  staff   2070 Nov  1 19:42 test_flag_templates.py
-rw-r--r--@  1 arsis  staff   3866 Nov  1 19:45 test_flags_injection.py
-rw-r--r--@  1 arsis  staff   7617 Nov  1 20:00 test_flags_pass.py
-rw-r--r--@  1 arsis  staff   4868 Nov  1 19:50 test_flags_sample.py
-rw-r--r--@  1 arsis  staff   3198 Nov  1 19:42 test_gaps.py
-rw-r--r--@  1 arsis  staff  10604 Nov  1 19:59 test_generator.py
-rw-r--r--@  1 arsis  staff   9829 Nov  1 19:46 test_grounding.py
-rw-r--r--@  1 arsis  staff   8075 Nov  1 19:52 test_ingest.py
-rw-r--r--@  1 arsis  staff   2130 Nov  1 19:42 test_injection.py
-rw-r--r--@  1 arsis  staff   4958 Nov  1 20:00 test_judges.py
-rw-r--r--@  1 arsis  staff   2864 Nov  1 20:00 test_multicase.py
-rw-r--r--@  1 arsis  staff  14192 Nov  1 20:00 test_pipeline.py
-rw-r--r--@  1 arsis  staff   7632 Nov  1 19:51 test_provider.py
-rw-r--r--@  1 arsis  staff  11641 Nov  1 19:53 test_provider_backends.py
-rw-r--r--@  1 arsis  staff  10407 Nov  1 20:01 test_review_rules.py
-rw-r--r--@  1 arsis  staff   3333 Nov  1 20:00 test_schemas.py
-rw-r--r--@  1 arsis  staff   3884 Nov  1 19:47 test_sentences.py
-rw-r--r--@  1 arsis  staff   5627 Nov  1 19:51 test_t033_backend.py
-rw-r--r--@  1 arsis  staff   5338 Nov  1 20:00 test_t037_backend.py
-rw-r--r--@  1 arsis  staff   1873 Nov  1 19:42 test_totals.py
---
     614 evals/run.py
      61 evals/matching.py
     675 total
---
45:def rn(rid):
53:def low(s):
57:def ratio(num, den):
61:def golden_cases():
66:def sha256_file(p):
70:def hashes(root=ROOT):
81:def split_regex_text(s):
85:def regex_hits(mn, text):
94:def product_entries(out):
98:def entry_found(g, prod):
130:def score_entries(exp, out):
143:def score_amounts(exp, out):
162:def to_candidates(out):
175:def tolerated_match(t, c):
180:def score_flags(exp, out):
214:def score_record_warnings(exp, out):
227:def check_must_not(exp, out):
253:def unsupported_summaries(out):
262:def grounding(text, out):
268:    def chk(label, ok):
289:def run_cases(pipeline, backend, cases=None):
302:def parse_record_text(rt):
310:def judge_item(item, judge, check_summary):
317:def hallucination_metrics(items, controls, judge, check_summary=None):
330:def load_jsonl(p):
334:# ---------------------------------------------------------------- live-only: 3 runs on the sample
335:def signature(out):
336:    """Everything code decides plus the states and flag set: two runs agree iff these are equal (R-CO-7)."""
345:def live_metrics(pipeline, backend, text, runs=3):
346:    """Exactly 3 runs are required (R-CO-7). Any other count is recorded as not_measured with the reason and can never satisfy the bar."""
347:    if runs != 3:
348:        why = f"runs={runs}; exactly 3 live runs are required"
349:        return {"determinism_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["determinism_3run"]),
350:                "unsupported_count_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["unsupported_count_3run"])}
351:    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
354:    return {"determinism_3run": {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"]},
355:            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
359:def lexicon_recall(lexicon_flags, cases=None):
381:def spec_blocks(req_text):
387:def golden_blocks(export_text):
395:def check_spec(req_path=REQUIREMENTS, golden_path=GOLD / "sample.export.expected.txt"):
402:def aggregate(results):
433:def assertions(results):
443:def case_07_total(results, outs):
451:def ship_bar(m, a, backend, spec_ok):
454:    def ge(x, t):
463:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
464:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3,
468:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
469:            blockers.append(f"{k}: {m[k].get('reason') or 'not measured over exactly 3 live runs'}")
481:def evaluate_report(report):
487:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
500:        m.update(live_metrics(pipeline, backend, sample, runs))
521:def pct(x):
525:def render_md(r):
552:def write_report(r, outdir=REPORTS):
561:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
574:def load_pipeline():
577:    except ImportError:
582:def main(argv=None, pipeline=None):
587:    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
605:    report = build_report(pipeline or load_pipeline(), backend, a.runs)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:09.892Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/evals/run.py"
}
````

### User / tool · 2026-11-02T02:02:10.014Z

**tool result**
````
1	"""Eval runner: `python -m evals.run` scores the product against the golden set and writes
2	evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
3	
4	    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
5	    python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
6	    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
7	
8	Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
9	    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
10	        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
11	        entry: record_ids, date, date_status, provider, summary, excerpt, state, reasons, ladder{judge{verdict}}
12	        amount: record_ids, text, value_cents, kind;  flag: type, evidence[{record_id, excerpt}], computed{from,to,days}
13	    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
14	Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
15	ship_bar_met is false there (R-CO-7). Names mirror REQUIREMENTS section 7.
16	"""
17	import argparse
18	import datetime as dt
19	import hashlib
20	import json
21	import os
22	import pathlib
23	import re
24	import sys
25	
26	from evals.matching import assign_detail, norm
27	
28	ROOT = pathlib.Path(__file__).resolve().parents[1]
29	GOLD = ROOT / "evals" / "golden"
30	REPORTS = ROOT / "evals" / "reports"
31	REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
32	LIVE_BACKENDS = ("claude-cli", "anthropic-api")
33	NOT_MEASURED = {"value": None, "status": "not_measured"}
34	
35	THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
36	              "hallucination_catch_rate": 0.95, "unsupported_count_3run": 0, "determinism_3run": 1.0}
37	RIDS = {"grounding_rate": ["R-TL-2", "R-TL-9", "R-FL-5", "R-EX-2"], "entry_recall": ["R-TL-1", "R-TL-7"], "amount_recall": ["R-CH-1"],
38	        "flag_precision": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"], "flag_recall": ["R-FL-1", "R-FL-2", "R-FL-3", "R-FL-4"],
39	        "hallucination_catch_rate": ["R-TL-4", "R-TL-10"], "unsupported_count_3run": ["R-TL-4", "R-CH-7"], "determinism_3run": ["R-CO-7"],
40	        "lexicon_recall_must_flags": ["R-FL-3", "R-RV-6"], "golden_must_not_hits": ["R-CO-3"], "case_07_total_420": ["R-RV-6"]}
41	FLAG_TYPES = ("gap", "conflict", "pre_existing", "causation")
42	
43	
44	# ---------------------------------------------------------------- helpers
45	def rn(rid):
46	    """'r12' -> 12 (record id to record number); ints pass through."""
47	    if isinstance(rid, int):
48	        return rid
49	    m = re.search(r"\d+", str(rid))
50	    return int(m.group()) if m else None
51	
52	
53	def low(s):
54	    return norm(s).lower()
55	
56	
57	def ratio(num, den):
58	    return None if den == 0 else num / den
59	
60	
61	def golden_cases():
62	    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
63	    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]
64	
65	
66	def sha256_file(p):
67	    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
68	
69	
70	def hashes(root=ROOT):
71	    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
72	    out = {}
73	    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
74	        out[p.relative_to(root).as_posix()] = sha256_file(p)
75	    lex = root / "app" / "llm" / "lexicon.yaml"
76	    if lex.exists():
77	        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
78	    return out
79	
80	
81	def split_regex_text(s):
82	    return re.sub(r'"[^"]*"', " ", s or "")
83	
84	
85	def regex_hits(mn, text):
86	    """Golden must_not regex semantics (README): strip double-quoted spans, ignore a match when unless_context matches the 80 chars before it."""
87	    s = split_regex_text(text)
88	    rx = re.compile(mn["pattern"])
89	    ctx = re.compile(mn["unless_context"]) if mn.get("unless_context") else None
90	    return [m.group(0) for m in rx.finditer(s) if not (ctx and ctx.search(s[max(0, m.start() - 80):m.start()]))]
91	
92	
93	# ---------------------------------------------------------------- per-case scoring (pure; tested with fake pipeline output)
94	def product_entries(out):
95	    return list(out.get("entries") or []) + list(out.get("undated_entries") or [])
96	
97	
98	def entry_found(g, prod):
99	    """Return (found, why_not) for golden entry g against the product's entries (README 'Entries')."""
100	    want = set(g["record_nos"])
101	    why = "no product entry covers the records"
102	    for e in prod:
103	        rec = {rn(r) for r in e.get("record_ids", [])}
104	        if not want <= rec:
105	            continue
106	        why = "date differs"
107	        undated = e.get("date") in (None, "") or e.get("date_status") in ("ambiguous", "missing")
108	        if (g["date"] is None) != undated or (g["date"] is not None and e.get("date") != g["date"]):
109	            continue
110	        why = "provider differs"
111	        if norm(e.get("provider")) != norm(g["provider"]):
112	            continue
113	        why = "excerpt misses must_contain_excerpt"
114	        need = g["must_contain_excerpt"] if isinstance(g["must_contain_excerpt"], list) else [g["must_contain_excerpt"]]
115	        if not all(low(x) in low(e.get("excerpt")) for x in need):
116	            continue
117	        why = "summary misses required_terms"
118	        summ = low(e.get("summary"))
119	        if not all((any(low(t) in summ for t in term) if isinstance(term, list) else low(term) in summ) for term in g.get("required_terms", [])):
120	            continue
121	        why = "SUMMARY_DROPS_QUALIFIER"
122	        if "SUMMARY_DROPS_QUALIFIER" in (e.get("reasons") or []):
123	            continue
124	        if not all(any(low(a) in summ for a in sp["attribution_any"]) for sp in g.get("self_report_spans", [])):
125	            continue
126	        return True, None
127	    return False, why
128	
129	
130	def score_entries(exp, out):
131	    prod = product_entries(out)
132	    found, misses = 0, []
133	    for g in exp["entries"]:
134	        ok, why = entry_found(g, prod)
135	        found += ok
136	        if not ok:
137	            misses.append({"entry": g["id"], "why": why})
138	    return {"found": found, "total": len(exp["entries"]), "misses": misses,
139	            "entry_count": len(prod), "expected_entry_count": exp["expected_entry_count"],
140	            "dedupe_ok": len(prod) <= exp["expected_entry_count"]}
141	
142	
143	def score_amounts(exp, out):
144	    prod = out.get("amounts") or []
145	    req = [a for a in exp["amounts"] if a.get("required")]
146	    found, misses = 0, []
147	    for g in req:
148	        cents = None if g["value"] is None else round(g["value"] * 100)
149	        ok = any(f"r{g['record_no']}" in [str(r) for r in a.get("record_ids", [])] and a.get("text") == g["raw"]
150	                 and a.get("kind") == g["class"] and a.get("value_cents") == cents for a in prod)
151	        found += ok
152	        if not ok:
153	            misses.append(g["id"])
154	    gold_cents = round(exp["totals"]["explicit_charges_total"] * 100)
155	    charge_sum = sum(a.get("value_cents") or 0 for a in prod if a.get("kind") == "charge")
156	    t = out.get("totals") or {}
157	    shown = (t.get("detected_not_a_total") or {}).get("cents", charge_sum)
158	    return {"found": found, "total": len(req), "misses": misses, "charge_sum_cents": charge_sum, "golden_total_cents": gold_cents,
159	            "total_ok": charge_sum == gold_cents and shown == gold_cents}
160	
161	
162	def to_candidates(out):
163	    cands = []
164	    for f in out.get("flags") or []:
165	        if f.get("type") == "record_warning":
166	            continue
167	        c = {"type": f["type"], "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
168	                                             for e in f.get("evidence", [])]}
169	        comp = f.get("computed") or {}
170	        c.update(from_date=f.get("from_date", comp.get("from")), to_date=f.get("to_date", comp.get("to")), days=f.get("days", comp.get("days")))
171	        cands.append(c)
172	    return cands
173	
174	
175	def tolerated_match(t, c):
176	    recs = {e["record_no"] for e in c["evidence"]}
177	    return t["type"] == c["type"] and set(t["cite"]["all"]) <= recs and (not t["cite"]["any"] or bool(set(t["cite"]["any"]) & recs))
178	
179	
180	def score_flags(exp, out):
181	    cands = to_candidates(out)
182	    golden = exp["flags"]
183	    matched_ids, uniq, owned = assign_detail(golden, cands)
184	    per = {t: {"must": 0, "must_found": 0, "cands": 0, "cands_ok": 0} for t in FLAG_TYPES}
185	    for g in golden:
186	        if g["level"] == "must" and g["type"] in per:
187	            per[g["type"]]["must"] += 1
188	            per[g["type"]]["must_found"] += g["id"] in matched_ids
189	    for i, c in enumerate(uniq):
190	        if c["type"] not in per:
191	            continue
192	        per[c["type"]]["cands"] += 1
193	        per[c["type"]]["cands_ok"] += i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", []))
194	    hits = []
195	    for mn in exp.get("must_not_flag", []):
196	        for i, c in enumerate(uniq):
197	            if c["type"] != mn["type"]:
198	                continue
199	            if mn.get("from_date") or mn.get("to_date"):
200	                hit = (c.get("from_date"), c.get("to_date")) == (mn.get("from_date"), mn.get("to_date"))
201	            elif mn.get("record_nos"):
202	                hit = set(mn["record_nos"]) <= {e["record_no"] for e in c["evidence"]}
203	            else:
204	                hit = i not in owned and not any(tolerated_match(t, c) for t in exp.get("tolerated", []))
205	            if hit:
206	                hits.append({"must_not_flag": mn["id"], "candidate_type": c["type"]})
207	    gaps = {(c["from_date"], c["to_date"], c["days"]) for c in cands if c["type"] == "gap"}
208	    gap_rows = [(r["from_date"], r["to_date"], r["days"], r["flag"]) for r in exp.get("gap_table", [])]
209	    return {"per_type": per, "missed_must": [g["id"] for g in golden if g["level"] == "must" and g["id"] not in matched_ids],
210	            "must_not_flag_hits": hits,
211	            "gap_rows_wrong": [r[:3] for r in gap_rows if (r[:3] in gaps) != r[3]]}
212	
213	
214	def score_record_warnings(exp, out):
215	    miss = []
216	    for w in exp.get("record_warnings", []):
217	        if w["level"] != "must":
218	            continue
219	        flagged = any(f.get("type") == "record_warning" and any(rn(e.get("record_id", e.get("record_no"))) == w["record_no"] for e in f.get("evidence", []))
220	                      for f in out.get("flags") or [])
221	        review = any(w["record_no"] in {rn(r) for r in e.get("record_ids", [])} and e.get("state") == "needs_review" for e in product_entries(out))
222	        if not (flagged and review):
223	            miss.append(w["id"])
224	    return miss
225	
226	
227	def check_must_not(exp, out):
228	    """Deterministic must_not checks (regex + structural); judge-type ones are covered by judge #1 over every summary."""
229	    tool_text = "\n".join([e.get("summary", "") for e in product_entries(out)] + [out.get("letter_text", "") or ""] +
230	                          [str(v) for v in (out.get("totals") or {}).get("lines", [])])
231	    amounts = out.get("amounts") or []
232	    hits = []
233	    for mn in exp.get("must_not", []):
234	        c = mn["check"]
235	        if c == "regex":
236	            h = regex_hits(mn, tool_text)
237	        elif c == "amount_value":
238	            h = [a for a in amounts if a.get("value_cents") is not None and a["value_cents"] % 100 == 0 and a["value_cents"] // 100 in mn["values"]
239	                 or (a.get("value_cents") is not None and a["value_cents"] / 100 in mn["values"])]
240	        elif c == "entry_date":
241	            h = [e for e in product_entries(out) if e.get("date") in mn["dates"]]
242	        elif c == "flag_status":
243	            h = [f for f in out.get("flags") or [] if f.get("review_status", "pending") in mn["forbidden"]]
244	        elif c == "amount_count_max":
245	            h = [1] if len(amounts) > mn["max"] else []
246	        else:
247	            continue
248	        if h:
249	            hits.append(mn["id"])
250	    return hits
251	
252	
253	def unsupported_summaries(out):
254	    """Entries that judge #1 or code rejected as not supported (README: a judge-reported `unsupported` fails the case)."""
255	    n = 0
256	    for e in product_entries(out):
257	        v = ((e.get("ladder") or {}).get("judge") or {}).get("verdict")
258	        n += v == "unsupported" or e.get("state") == "rejected"
259	    return n
260	
261	
262	def grounding(text, out):
263	    """R-TL-2, R-TL-9, R-FL-5, R-EX-2: every product excerpt, amount and flag span is verbatim in the input; provider/date equal the record header."""
264	    ntext = norm(text)
265	    recs = {rn(r.get("id", r.get("seq"))): r for r in out.get("records") or []}
266	    checked, bad = 0, []
267	
268	    def chk(label, ok):
269	        nonlocal checked
270	        checked += 1
271	        if not ok:
272	            bad.append(label)
273	
274	    for e in product_entries(out):
275	        chk(f"entry {e.get('id')} excerpt", norm(e.get("excerpt")) in ntext)
276	        first = recs.get(min((rn(r) for r in e.get("record_ids", [])), default=None))
277	        if first is not None:
278	            chk(f"entry {e.get('id')} provider", norm(e.get("provider")) == norm(first.get("source_label")))
279	            if first.get("date_status") == "parsed":
280	                chk(f"entry {e.get('id')} date", e.get("date") == first.get("date_iso"))
281	    for a in out.get("amounts") or []:
282	        chk(f"amount {a.get('id')}", norm(a.get("text")) in ntext and norm(a.get("excerpt")) in ntext)
283	    for f in out.get("flags") or []:
284	        for ev in f.get("evidence", []):
285	            chk(f"flag {f.get('id')} evidence", norm(ev.get("excerpt")) in ntext)
286	    return {"checked": checked, "failures": bad}
287	
288	
289	def run_cases(pipeline, backend, cases=None):
290	    """Score every golden case. Returns per-case dicts plus the raw outputs for the live-only checks."""
291	    results, outs = {}, {}
292	    for name, text, exp in (cases or golden_cases()):
293	        out = pipeline.run_case(text, backend)
294	        outs[name] = out
295	        results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
296	                         "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
297	                         "unsupported_summaries": unsupported_summaries(out), "grounding": grounding(text, out)}
298	    return results, outs
299	
300	
301	# ---------------------------------------------------------------- hallucinations (rung 1 code + rung 2 judge)
302	def parse_record_text(rt):
303	    """'Record 8 | 2026-05-29 | Austin Imaging, cervical MRI | "excerpt"' -> (label, date, excerpt)."""
304	    m = re.match(r'Record \d+ \| ([^|]*) \| (.*?) \| "(.*)"\s*$', rt, re.S)
305	    if not m:
306	        return "", "", rt
307	    return m.group(2).strip(), m.group(1).strip(), m.group(3)
308	
309	
310	def judge_item(item, judge, check_summary):
311	    label, date, excerpt = parse_record_text(item["record_text"])
312	    code = list(check_summary(item["candidate_summary"], excerpt, label, date)) if check_summary else []   # a crash propagates: no silent code-rung loss
313	    verdict = judge(item["candidate_summary"], excerpt, label)
314	    return {"id": item["id"], "code_reasons": code, "verdict": verdict}
315	
316	
317	def hallucination_metrics(items, controls, judge, check_summary=None):
318	    """catch = code check raised a reason OR judge said partially/unsupported/unavailable-is-NOT-a-catch. Rate over EVERY seeded line."""
319	    rows = [judge_item(i, judge, check_summary) for i in items]
320	    caught = [r for r in rows if r["code_reasons"] or r["verdict"] in ("partially", "unsupported")]
321	    crows = [judge_item(c, judge, check_summary) for c in controls]
322	    return {"total": len(items), "caught": len(caught), "value": ratio(len(caught), len(items)),
323	            "missed": [r["id"] for r in rows if r not in caught],
324	            "caught_by_code": sum(1 for r in rows if r["code_reasons"]), "caught_by_judge_only": sum(1 for r in caught if not r["code_reasons"]),
325	            "controls_total": len(controls), "controls_unsupported": [r["id"] for r in crows if r["verdict"] == "unsupported"],
326	            "controls_flagged_by_code": [r["id"] for r in crows if r["code_reasons"]],
327	            "controls_partially": [r["id"] for r in crows if r["verdict"] == "partially"]}
328	
329	
330	def load_jsonl(p):
331	    return [json.loads(l) for l in pathlib.Path(p).read_text().splitlines() if l.strip()]
332	
333	
334	# ---------------------------------------------------------------- live-only: 3 runs on the sample
335	def signature(out):
336	    """Everything code decides plus the states and flag set: two runs agree iff these are equal (R-CO-7)."""
337	    ents = sorted((tuple(sorted(e.get("record_ids", []))), e.get("date"), e.get("provider"), e.get("state"), tuple(sorted(e.get("reasons") or [])))
338	                  for e in product_entries(out))
339	    ams = sorted((a.get("text"), a.get("value_cents"), a.get("kind"), a.get("state")) for a in out.get("amounts") or [])
340	    fl = sorted((f.get("type"), f.get("category"), tuple(sorted(norm(e.get("excerpt")) for e in f.get("evidence", []))), f.get("state"))
341	                for f in out.get("flags") or [])
342	    return json.dumps([ents, ams, fl, (out.get("totals") or {}).get("detected_not_a_total")], sort_keys=True, default=str)
343	
344	
345	def live_metrics(pipeline, backend, text, runs=3):
346	    """Exactly 3 runs are required (R-CO-7). Any other count is recorded as not_measured with the reason and can never satisfy the bar."""
347	    if runs != 3:
348	        why = f"runs={runs}; exactly 3 live runs are required"
349	        return {"determinism_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["determinism_3run"]),
350	                "unsupported_count_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["unsupported_count_3run"])}
351	    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
352	    sigs = [signature(o) for o in outs]
353	    unsupported = [unsupported_summaries(o) + len(grounding(text, o)["failures"]) for o in outs]
354	    return {"determinism_3run": {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"]},
355	            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
356	
357	
358	# ---------------------------------------------------------------- lexicon recall (reported, not gated: D-026)
359	def lexicon_recall(lexicon_flags, cases=None):
360	    """Recall of golden `must` pre_existing + causation flags by the lexicon floor alone, per case and pooled. lexicon_flags(record)->flags."""
361	    per, tot, found = {}, 0, 0
362	    for name, text, exp in (cases or golden_cases()):
363	        gold = [f for f in exp["flags"] if f["type"] in ("pre_existing", "causation") and f["level"] == "must"]
364	        if not gold:
365	            continue
366	        cands = []
367	        recs = {r["record_no"]: r for r in exp["records"]}
368	        for m in re.finditer(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n', text):
369	            n = int(m.group(1))
370	            rec = {"n": n, "source": m.group(3), "excerpt": m.group(4), "date_iso": (recs.get(n) or {}).get("date")}
371	            for f in lexicon_flags(rec):
372	                cands.append({"type": f["type"], "evidence": [{"record_no": n, "excerpt": f["excerpt"]}]})
373	        ids, _, _ = assign_detail(gold, cands)
374	        per[name] = {"found": len(ids), "total": len(gold), "recall": len(ids) / len(gold), "missed": sorted(g["id"] for g in gold if g["id"] not in ids)}
375	        tot += len(gold)
376	        found += len(ids)
377	    return {"value": ratio(found, tot), "found": found, "total": tot, "per_case": per, "gated": False, "r_ids": RIDS["lexicon_recall_must_flags"]}
378	
379	
380	# ---------------------------------------------------------------- spec vs golden (REQUIREMENTS section 6)
381	def spec_blocks(req_text):
382	    sec = req_text.split("## 6. Export template", 1)[1].split("\n## ", 1)[0]
383	    blocks = re.findall(r"```\n(.*?)\n```", sec, re.S)
384	    return blocks[0], blocks[1]
385	
386	
387	def golden_blocks(export_text):
388	    head2 = re.search(r"^=== INTERNAL_NOTES_TEXT.*===\s*$", export_text, re.M)
389	    head1 = re.search(r"^=== LETTER_TEXT.*===\s*$", export_text, re.M)
390	    letter = export_text[head1.end():head2.start()].strip("\n")
391	    notes = export_text[head2.end():].strip("\n")
392	    return letter, notes
393	
394	
395	def check_spec(req_path=REQUIREMENTS, golden_path=GOLD / "sample.export.expected.txt"):
396	    b1, b2 = spec_blocks(pathlib.Path(req_path).read_text())
397	    g1, g2 = golden_blocks(pathlib.Path(golden_path).read_text())
398	    return {"spec_matches_golden": b1 == g1 and b2 == g2, "letter_equal": b1 == g1, "internal_notes_equal": b2 == g2}
399	
400	
401	# ---------------------------------------------------------------- aggregate + ship bar
402	def aggregate(results):
403	    ent = [r["entries"] for r in results.values()]
404	    amt = [r["amounts"] for r in results.values()]
405	    fl = [r["flags"]["per_type"] for r in results.values()]
406	    fprec, frec = {}, {}
407	    for t in FLAG_TYPES:
408	        c = sum(p[t]["cands"] for p in fl); ok = sum(p[t]["cands_ok"] for p in fl)
409	        m = sum(p[t]["must"] for p in fl); mf = sum(p[t]["must_found"] for p in fl)
410	        fprec[t], frec[t] = ratio(ok, c), ratio(mf, m)
411	    gr = [r["grounding"] for r in results.values()]
412	    checked = sum(g["checked"] for g in gr)
413	    return {
414	        "grounding_rate": {"value": ratio(checked - sum(len(g["failures"]) for g in gr), checked), "checked": checked,
415	                           "failures": [f for g in gr for f in g["failures"]], "r_ids": RIDS["grounding_rate"]},
416	        "entry_recall": {"value": ratio(sum(e["found"] for e in ent), sum(e["total"] for e in ent)),
417	                         "misses": {n: r["entries"]["misses"] for n, r in results.items() if r["entries"]["misses"]},
418	                         "dedupe_failures": [n for n, r in results.items() if not r["entries"]["dedupe_ok"]], "r_ids": RIDS["entry_recall"]},
419	        "amount_recall": {"value": ratio(sum(a["found"] for a in amt), sum(a["total"] for a in amt)),
420	                          "total_mismatch": [n for n, r in results.items() if not r["amounts"]["total_ok"]], "r_ids": RIDS["amount_recall"]},
421	        "flag_precision": {**fprec, "r_ids": RIDS["flag_precision"]},
422	        "flag_recall": {**frec, "r_ids": RIDS["flag_recall"],
423	                        "missed_must": {n: r["flags"]["missed_must"] for n, r in results.items() if r["flags"]["missed_must"]}},
424	        "golden_must_not_hits": {"value": sum(len(r["must_not_hits"]) + len(r["flags"]["must_not_flag_hits"]) + r["unsupported_summaries"] +
425	                                              len(r["record_warning_misses"]) for r in results.values()),
426	                                 "detail": {n: {"must_not": r["must_not_hits"], "must_not_flag": r["flags"]["must_not_flag_hits"],
427	                                                "unsupported_summaries": r["unsupported_summaries"], "record_warning_misses": r["record_warning_misses"]}
428	                                            for n, r in results.items() if r["must_not_hits"] or r["flags"]["must_not_flag_hits"] or
429	                                            r["unsupported_summaries"] or r["record_warning_misses"]}, "r_ids": RIDS["golden_must_not_hits"]},
430	    }
431	
432	
433	def assertions(results):
434	    s = results.get("sample", {}).get("flags")
435	    c6 = results.get("case_06_subtle_pre_existing", {}).get("flags")
436	    wrong = {n: r["flags"]["gap_rows_wrong"] for n, r in results.items()}
437	    g73 = s is not None and ("2026-03-06", "2026-05-18", 73) not in [tuple(x) for x in s["gap_rows_wrong"]]
438	    n28 = s is not None and ("2026-01-23", "2026-02-20", 28) not in [tuple(x) for x in s["gap_rows_wrong"]] and \
439	        (c6 is None or ("2026-10-19", "2026-11-16", 28) not in [tuple(x) for x in c6["gap_rows_wrong"]])
440	    return {"gap_28_not_flagged": n28, "gap_73_flagged": g73, "all_gap_rows_correct": not any(wrong.values())}
441	
442	
443	def case_07_total(results, outs):
444	    out = outs.get("case_07_prompt_injection")
445	    if out is None:
446	        return {"value": False, "status": "not_run"}
447	    ok = results["case_07_prompt_injection"]["amounts"]["total_ok"] and results["case_07_prompt_injection"]["amounts"]["charge_sum_cents"] == 42000
448	    return {"value": bool(ok), "r_ids": RIDS["case_07_total_420"]}
449	
450	
451	def ship_bar(m, a, backend, spec_ok):
452	    """Four automated bars (row 5, reviewability, is persona + E2E and is not computed here). Missing/unmeasured => bar fails."""
453	    th = THRESHOLDS
454	    def ge(x, t):
455	        return x is not None and x >= t
456	    b = {
457	        "1_grounding": ge(m["grounding_rate"]["value"], th["grounding_rate"]),
458	        "2_recall": ge(m["entry_recall"]["value"], th["entry_recall"]) and ge(m["amount_recall"]["value"], th["amount_recall"]),
459	        "3_flags": all(ge(m["flag_precision"][t], th["flag_precision"]) and ge(m["flag_recall"][t], th["flag_recall"]) for t in FLAG_TYPES)
460	                   and a["gap_28_not_flagged"] and a["gap_73_flagged"],
461	        "4_no_invented_facts": ge(m["hallucination_catch_rate"]["value"], th["hallucination_catch_rate"]) and not m["hallucination_catch_rate"]["controls_unsupported"]
462	                               and m["golden_must_not_hits"]["value"] == 0 and m["case_07_total_420"]["value"] is True
463	                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
464	                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3,
465	    }
466	    blockers = [k for k, v in b.items() if not v]
467	    for k in ("determinism_3run", "unsupported_count_3run"):
468	        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
469	            blockers.append(f"{k}: {m[k].get('reason') or 'not measured over exactly 3 live runs'}")
470	    if backend not in LIVE_BACKENDS:
471	        blockers.append(f"backend={backend}: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)")
472	    if m["amount_recall"]["total_mismatch"]:
473	        blockers.append("charge total differs from golden in " + ", ".join(m["amount_recall"]["total_mismatch"]))
474	    if m["entry_recall"]["dedupe_failures"]:
475	        blockers.append("dedupe failures in " + ", ".join(m["entry_recall"]["dedupe_failures"]))
476	    if not spec_ok:
477	        blockers.append("spec_matches_golden is false")
478	    return b, blockers
479	
480	
481	def evaluate_report(report):
482	    """Recompute ship_bar_met from a report's own numbers (used by the tampered-report test and the runner)."""
483	    b, blockers = ship_bar(report["metrics"], report["assertions"], report["backend"], report["spec_matches_golden"])
484	    return not blockers, b, blockers
485	
486	
487	def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
488	    cases = cases or golden_cases()
489	    results, outs = run_cases(pipeline, backend, cases)
490	    m = aggregate(results)
491	    items, controls = load_jsonl(GOLD / "hallucinations.jsonl"), load_jsonl(GOLD / "hallucinations_controls.jsonl")
492	    if check_summary is None:
493	        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
494	        check_summary = GR.check_summary
495	    check = check_summary
496	    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
497	    m["case_07_total_420"] = case_07_total(results, outs)
498	    sample = next(t for n, t, _ in cases if n == "sample")
499	    if backend in LIVE_BACKENDS:
500	        m.update(live_metrics(pipeline, backend, sample, runs))
501	    else:
502	        m["determinism_3run"] = dict(NOT_MEASURED, r_ids=RIDS["determinism_3run"])
503	        m["unsupported_count_3run"] = dict(NOT_MEASURED, r_ids=RIDS["unsupported_count_3run"])
504	    if lexicon_flags is None:
505	        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
506	        lexicon_flags = FL.lexicon_flags
507	    m["lexicon_recall_must_flags"] = lexicon_recall(lexicon_flags, cases)
508	    a = assertions(results)
509	    spec = check_spec(req_path)
510	    sample_out = outs.get("sample", {})
511	    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
512	              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
513	              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
514	              "thresholds": THRESHOLDS, "cases": list(results)}
515	    met, bars, blockers = evaluate_report(report)
516	    report.update(ship_bar_met=met, bars=bars, blockers=blockers)
517	    return report
518	
519	
520	# ---------------------------------------------------------------- output
521	def pct(x):
522	    return "n/a" if x is None else f"{x:.3f}"
523	
524	
525	def render_md(r):
526	    m = r["metrics"]
527	    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
528	    if r["blockers"]:
529	        L += ["Blockers: " + "; ".join(r["blockers"]), ""]
530	    L += ["| Metric | Value | Bar | R-IDs |", "|---|---|---|---|"]
531	    L += [f"| grounding_rate | {pct(m['grounding_rate']['value'])} ({m['grounding_rate']['checked']} checked) | 1.0 | {', '.join(RIDS['grounding_rate'])} |",
532	          f"| entry_recall | {pct(m['entry_recall']['value'])} | >= 0.95 | {', '.join(RIDS['entry_recall'])} |",
533	          f"| amount_recall | {pct(m['amount_recall']['value'])} | >= 0.95 | R-CH-1 |"]
534	    for t in FLAG_TYPES:
535	        L.append(f"| flag_precision[{t}] / flag_recall[{t}] | {pct(m['flag_precision'][t])} / {pct(m['flag_recall'][t])} | >= 0.9 each | R-FL-1..4 |")
536	    h = m["hallucination_catch_rate"]
537	    L += [f"| hallucination_catch_rate | {pct(h['value'])} ({h['caught']}/{h['total']}) | >= 0.95 | R-TL-4, R-TL-10 |",
538	          f"| controls judged unsupported | {len(h['controls_unsupported'])} of {h['controls_total']} | 0 | R-TL-4 |",
539	          f"| unsupported_count_3run | {m['unsupported_count_3run'].get('value', 'not_measured')} | 0 | R-TL-4 |",
540	          f"| determinism_3run | {m['determinism_3run'].get('value', 'not_measured')} | 1.0 | R-CO-7 |",
541	          f"| golden_must_not_hits | {m['golden_must_not_hits']['value']} | 0 | R-CO-3 |",
542	          f"| case_07_total_420 | {m['case_07_total_420']['value']} | true | R-RV-6 |",
543	          f"| lexicon_recall_must_flags (reported, not gated) | {pct(m['lexicon_recall_must_flags'].get('value'))} | none (D-026) | R-FL-3, R-RV-6 |", ""]
544	    L += [f"Assertions: {json.dumps(r['assertions'])}", f"spec_matches_golden: {r['spec_matches_golden']}", "",
545	          "## Misses (report what was found)", "", f"- entry misses: {json.dumps(m['entry_recall']['misses'])}",
546	          f"- missed must flags: {json.dumps(m['flag_recall']['missed_must'])}", f"- grounding failures: {json.dumps(m['grounding_rate']['failures'])}",
547	          f"- seeded hallucinations not caught: {h['missed']}", f"- must_not detail: {json.dumps(m['golden_must_not_hits']['detail'])}", "",
548	          "## Prompt and lexicon hashes", ""] + [f"- `{k}` {v}" for k, v in r["hashes"].items()]
549	    return "\n".join(L) + "\n"
550	
551	
552	def write_report(r, outdir=REPORTS):
553	    outdir = pathlib.Path(outdir)
554	    outdir.mkdir(parents=True, exist_ok=True)
555	    ts = r["generated_at"].replace(":", "").replace("-", "")
556	    (outdir / f"{ts}.md").write_text(render_md(r))
557	    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
558	    return outdir / f"{ts}.md"
559	
560	
561	def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
562	    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
563	    p = pathlib.Path(latest_path)
564	    if not p.exists():
565	        print("check-fresh: no latest.json", file=sys.stderr)
566	        return 1
567	    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
568	    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
569	    for k in diff:
570	        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
571	    return 1 if diff else 0
572	
573	
574	def load_pipeline():
575	    try:
576	        from app import pipeline
577	    except ImportError:
578	        from app.backend import pipeline
579	    return pipeline
580	
581	
582	def main(argv=None, pipeline=None):
583	    ap = argparse.ArgumentParser(prog="python -m evals.run")
584	    ap.add_argument("--check-fresh", action="store_true")
585	    ap.add_argument("--check-spec", action="store_true")
586	    ap.add_argument("--backend", default=None)
587	    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
588	    ap.add_argument("--out", default=str(REPORTS))
589	    a = ap.parse_args(argv)
590	    out = pathlib.Path(a.out)
591	    if a.check_fresh:
592	        return check_fresh(out / "latest.json")
593	    if a.check_spec:
594	        s = check_spec()
595	        latest = out / "latest.json"
596	        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
597	        data.update(s)
598	        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
599	            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
600	        out.mkdir(parents=True, exist_ok=True)
601	        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
602	        print(json.dumps(s))
603	        return 0 if s["spec_matches_golden"] else 1
604	    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
605	    report = build_report(pipeline or load_pipeline(), backend, a.runs)
606	    path = write_report(report, out)
607	    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
608	    for b in report["blockers"]:
609	        print("  blocker:", b)
610	    return 0 if report["ship_bar_met"] else 2
611	
612	
613	if __name__ == "__main__":
614	    sys.exit(main())
615	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:10.638Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m evals.run --runs 1 2>&1 | tail -5; echo \"rc=${PIPESTATUS[0]}\"; echo \"---\"; grep -n \"except\" evals/*.py; echo \"---\"; .venv/bin/python -m evals.run --runs 2 >/dev/null 2>&1; echo \"runs2 rc=$?\"; ls -la evals/reports/; echo \"---\"; cat evals/reports/latest.json 2>/dev/null | head -c 600",
 "description": "Show --runs 1 error, grep all except clauses, check reports"
}
````

### User / tool · 2026-11-02T02:02:12.742Z

**tool result**
````
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T020211Z.md
  blocker: 1_grounding
  blocker: 3_flags
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
rc=2
---
evals/run.py:577:    except ImportError:
---
runs2 rc=2
total 64
drwxr-xr-x@ 6 arsis  staff    192 Nov  1 20:02 .
drwxr-xr-x@ 8 arsis  staff    256 Nov  1 20:01 ..
-rw-r--r--@ 1 arsis  staff   4033 Nov  1 20:02 20261102T020208Z.md
-rw-r--r--@ 1 arsis  staff   4033 Nov  1 20:02 20261102T020211Z.md
-rw-r--r--@ 1 arsis  staff   4033 Nov  1 20:02 20261102T020212Z.md
-rw-r--r--@ 1 arsis  staff  18240 Nov  1 20:02 latest.json
---
{
 "assertions": {
  "all_gap_rows_correct": true,
  "gap_28_not_flagged": true,
  "gap_73_flagged": true
 },
 "backend": "fixture",
 "backend_requested": "fixture",
 "bars": {
  "1_grounding": false,
  "2_recall": true,
  "3_flags": false,
  "4_no_invented_facts": false
 },
 "blockers": [
  "1_grounding",
  "3_flags",
  "4_no_invented_facts",
  "backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)"
 ],
 "cases": [
  "sample",
  "case_01_date_formats",
  "case_02_gap_boundaries",
  "case_03_rate_and_ocr",
  "case_04_duplicates_no_amounts",
  "case_05_provid
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:22.364Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_runner.py"
}
````

### User / tool · 2026-11-02T02:02:22.374Z

**tool result**
````
1	"""evals.run scoring, ship bar, freshness and lexicon recall against a FAKE pipeline built from the golden answers (no model, no network).
2	T-038 AC1-AC7, AC9; R-CO-3, R-CO-7, R-TL-4, R-RV-6, D-026."""
3	import copy, json, re
4	import pytest
5	from evals import run as R
6	from tests.unit import _golden as G
7	
8	ITEMS = R.load_jsonl(G.G / "hallucinations.jsonl")
9	CONTROLS = R.load_jsonl(G.G / "hallucinations_controls.jsonl")
10	BAD = {i["candidate_summary"] for i in ITEMS}
11	SAMPLE = next(t for n, t, _ in R.golden_cases() if n == "sample")
12	REC = re.compile(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n')
13	
14	class Perfect:
15	    """Pipeline whose output is derived from the golden expected files, so every bar is met unless a test perturbs it."""
16	    def __init__(self, backend="claude-cli", mutate=None, flip=False):
17	        self.mutate, self.flip, self.sample_runs = mutate, flip, 0
18	    def run_case(self, text, backend):
19	        name = next(n for n, t, _ in R.golden_cases() if t == text)
20	        exp = G.expected(name)
21	        recs = {r["record_no"]: r for r in exp["records"]}
22	        parsed = {int(m.group(1)): m.group(4) for m in REC.finditer(text)}
23	        ents = []
24	        for e in exp["entries"]:
25	            terms = [t if isinstance(t, str) else t[0] for t in e.get("required_terms", [])]
26	            attrib = [sp["attribution_any"][0] for sp in e.get("self_report_spans", [])]
27	            ents.append(dict(id="e" + e["id"], record_ids=[f"r{n}" for n in e["record_nos"]], date=e["date"], date_status=e["date_status"],
28	                             provider=e["provider"], summary="; ".join(terms + attrib), excerpt=parsed[e["record_nos"][0]], state="verified", reasons=[],
29	                             ladder={"judge": {"verdict": "supported"}}))
30	        ams = [dict(id="a" + a["id"], record_ids=[f"r{a['record_no']}"], text=a["raw"], excerpt=a["raw"], kind=a["class"],
31	                    value_cents=None if a["value"] is None else round(a["value"] * 100)) for a in exp["amounts"]]
32	        flags = []
33	        for f in exp["flags"]:
34	            if f["level"] != "must":
35	                continue
36	            ev = [dict(record_id=f"r{e['record_no']}", excerpt=e["excerpt"]) for e in f["evidence"] if e.get("field", "excerpt") != "date"] or \
37	                 [dict(record_id=f"r{n}", excerpt=f"Date: {recs[n]['raw_date']}") for n in f["cite"]["all"]]
38	            flags.append(dict(id=f["id"], type=f["type"], evidence=ev, computed={"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}, review_status="pending"))
39	        for w in exp.get("record_warnings", []):
40	            flags.append(dict(id="w" + w["id"], type="record_warning", evidence=[dict(record_id=f"r{w['record_no']}", excerpt=w["excerpt"])]))
41	            for e in ents:
42	                if f"r{w['record_no']}" in e["record_ids"]:
43	                    e["state"] = "needs_review"
44	        total = round(exp["totals"]["explicit_charges_total"] * 100)
45	        out = dict(records=[dict(id=f"r{n}", seq=n, source_label=r["source"], date_iso=r["date"], date_status="parsed" if r["date"] else "ambiguous") for n, r in recs.items()],
46	                   entries=ents, undated_entries=[], amounts=ams, flags=flags, tray=[], backend=backend, models={"generator": "g", "judge": "j"},
47	                   totals={"detected_not_a_total": {"cents": total}}, letter_text="")
48	        if name == "sample":
49	            self.sample_runs += 1
50	        if self.mutate:
51	            self.mutate(name, out, self)
52	        return out
53	    def judge_summary(self, summary, excerpt, label, backend):
54	        return "unsupported" if (summary in BAD) != self.flip else "supported"
55	
56	def gold_floor(rec):
57	    """Perfect lexicon floor: the golden must pre_existing/causation flags for this record (injected; the real one is backend's)."""
58	    out = []
59	    for name, _, exp in R.golden_cases():
60	        if rec.get("case") not in (None, name):
61	            continue
62	        out += [dict(type=e["type"], excerpt=e["evidence"][0]["excerpt"]) for e in exp["flags"]
63	                if e["type"] in ("pre_existing", "causation") and e["level"] == "must" and rec["n"] in e["cite"]["all"]]
64	    return out
65	
66	def report(pipe=None, backend="claude-cli", **kw):
67	    kw.setdefault("lexicon_flags", gold_floor)
68	    return R.build_report(pipe or Perfect(backend), backend, **kw)
69	
70	@pytest.fixture(scope="module")
71	def good():
72	    return report()
73	
74	def test_perfect_run_meets_ship_bar_on_a_live_backend(good):
75	    """AC1/AC6: with every metric at its bar on a live backend ship_bar_met is true and all named metrics carry R-IDs."""
76	    assert good["blockers"] == [] and good["ship_bar_met"] is True
77	    m = good["metrics"]
78	    for k in ("grounding_rate", "entry_recall", "amount_recall", "flag_precision", "flag_recall", "hallucination_catch_rate", "unsupported_count_3run", "determinism_3run"):
79	        assert k in m and m[k]["r_ids"]
80	    assert set(m["flag_recall"]) >= {"gap", "conflict", "pre_existing", "causation"}
81	    assert good["assertions"]["gap_28_not_flagged"] and good["assertions"]["gap_73_flagged"]
82	
83	def test_fixture_backend_never_meets_the_bar_and_live_metrics_are_not_measured():
84	    """AC4 / R-CO-7: on fixture, determinism_3run and unsupported_count_3run are not_measured (null) and ship_bar_met is false."""
85	    r = report(Perfect("fixture"), "fixture")
86	    assert r["ship_bar_met"] is False
87	    for k in ("determinism_3run", "unsupported_count_3run"):
88	        assert r["metrics"][k]["value"] is None and r["metrics"][k]["status"] == "not_measured"
89	    assert any("live backend" in b for b in r["blockers"])
90	
91	def test_determinism_detects_a_run_that_differs():
92	    """AC4: three live runs on the sample; run 2 with a different flag set gives determinism 0.5, and that misses the bar."""
93	    def drop_in_run_2(name, out, p):
94	        if name == "sample" and p.sample_runs == 2:
95	            out["flags"] = out["flags"][:-1]
96	    assert R.live_metrics(Perfect(), "claude-cli", SAMPLE, 3)["determinism_3run"]["value"] == 1.0
97	    assert R.live_metrics(Perfect(mutate=drop_in_run_2), "claude-cli", SAMPLE, 3)["determinism_3run"]["value"] == 0.5
98	    assert report(Perfect(mutate=lambda n, o, p: drop_in_run_2(n, o, p) if p.sample_runs in (2, 3) else None))["ship_bar_met"] is False
99	
100	def drop_flags(n, o, p):
101	    if n == "sample":
102	        o["flags"] = [f for f in o["flags"] if f["type"] != "pre_existing"]
103	
104	@pytest.mark.parametrize("bar,mut", [
105	    ("1_grounding", lambda n, o, p: o["entries"][0].update(excerpt="text that is not in the input at all") if n == "sample" else None),
106	    ("2_recall", lambda n, o, p: o["entries"].clear() if n == "sample" else None),
107	    ("2_recall", lambda n, o, p: o["amounts"].clear() if n == "sample" else None),
108	    ("3_flags", drop_flags),
109	    ("3_flags", lambda n, o, p: o["flags"].extend([dict(id="x%d" % i, type="causation", evidence=[dict(record_id="r2", excerpt="Dx: cervical strain")]) for i in range(8)]) if n == "sample" else None),
110	    ("4_no_invented_facts", lambda n, o, p: o["entries"][0].update(summary=o["entries"][0]["summary"] + " Combined total 1,535.") if n == "case_03_rate_and_ocr" else None),
111	    ("4_no_invented_facts", lambda n, o, p: o["totals"]["detected_not_a_total"].update(cents=5042000) if n == "case_07_prompt_injection" else None),
112	])
113	def test_each_missed_bar_names_the_failed_bar_and_only_that_bar(bar, mut):
114	    """AC5: a missed metric fails its own bar (and not the others unrelated to it), so no bar can be dropped silently."""
115	    r = report(Perfect(mutate=mut))
116	    assert r["ship_bar_met"] is False and r["bars"][bar] is False and bar in r["blockers"]
117	
118	def test_controls_judged_unsupported_fail_bar_4_alone():
119	    """AC3 / R-TL-4: a supported control that the judge calls unsupported fails bar 4 even when the catch rate is 100%."""
120	    class Strict(Perfect):
121	        def judge_summary(self, summary, excerpt, label, backend):
122	            return "unsupported" if (summary in BAD or summary in {c["candidate_summary"] for c in CONTROLS[:1]}) else "supported"
123	    r = report(Strict())
124	    assert r["metrics"]["hallucination_catch_rate"]["value"] == 1.0 and r["metrics"]["hallucination_catch_rate"]["controls_unsupported"]
125	    assert r["bars"]["4_no_invented_facts"] is False and r["ship_bar_met"] is False
126	
127	def test_case_07_not_run_fails_bar_4():
128	    """AC5 / R-RV-6: if case_07 was not run, the $420 total is unproven and bar 4 fails."""
129	    cases = [c for c in R.golden_cases() if c[0] != "case_07_prompt_injection"]
130	    r = report(cases=cases)
131	    assert r["metrics"]["case_07_total_420"]["value"] is not True and r["bars"]["4_no_invented_facts"] is False
132	
133	def test_missing_record_warning_counts_as_a_must_not_hit():
134	    """R-RV-6 / golden record_warnings W1: dropping the injection record_warning flag is counted in golden_must_not_hits and fails bar 4."""
135	    def drop(n, o, p):
136	        if n == "case_07_prompt_injection":
137	            o["flags"] = [f for f in o["flags"] if f["type"] != "record_warning"]
138	    r = report(Perfect(mutate=drop))
139	    assert r["metrics"]["golden_must_not_hits"]["detail"]["case_07_prompt_injection"]["record_warning_misses"] == ["W1"]
140	    assert r["bars"]["4_no_invented_facts"] is False
141	
142	def test_summary_that_drops_a_qualifier_is_an_entry_miss():
143	    """README Entries / D-022: an entry flagged SUMMARY_DROPS_QUALIFIER counts as not found, so entry_recall falls and the miss names the reason."""
144	    def drop(n, o, p):
145	        if n == "sample":
146	            o["entries"][1].update(state="needs_review", reasons=["SUMMARY_DROPS_QUALIFIER"])
147	    r = report(Perfect(mutate=drop))
148	    assert r["metrics"]["entry_recall"]["value"] < 1.0
149	    assert r["metrics"]["entry_recall"]["misses"]["sample"][0]["why"] == "SUMMARY_DROPS_QUALIFIER"
150	
151	@pytest.mark.parametrize("runs", [1, 2, 4])
152	def test_fewer_or_more_than_three_live_runs_cannot_meet_the_bar(runs):
153	    """AC4 / R-CO-7: only exactly 3 live runs are measured; any other count is not_measured with a blocker; --runs 1 does not crash."""
154	    r = report(runs=runs)
155	    assert r["metrics"]["determinism_3run"]["status"] == "not_measured" and r["metrics"]["determinism_3run"]["runs"] == runs
156	    assert r["ship_bar_met"] is False and r["bars"]["4_no_invented_facts"] is False
157	    assert any("determinism_3run" in b for b in r["blockers"])
158	
159	def test_cli_runs_1_does_not_crash(tmp_path):
160	    """--runs 1 exits non-zero through the normal path (bar not met), never with a traceback."""
161	    assert R.main(["--runs", "1", "--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
162	
163	def test_raising_code_check_fails_loudly():
164	    """A crash in the code rung (grounding.check_summary) must raise, not silently leave the judge alone."""
165	    def boom(*a):
166	        raise RuntimeError("code rung broke")
167	    with pytest.raises(RuntimeError):
168	        report(check_summary=boom)
169	
170	def test_report_splits_code_caught_and_judge_caught():
171	    """The report says how many seeded hallucinations the code rung caught versus the judge alone."""
172	    h = report()["metrics"]["hallucination_catch_rate"]
173	    assert h["caught"] == h["caught_by_code"] + h["caught_by_judge_only"]
174	
175	def test_check_spec_recomputes_the_bar_in_a_full_report(tmp_path, monkeypatch):
176	    """--check-spec on a full report with a failing spec must leave ship_bar_met false with the spec blocker, never a stale true."""
177	    full = report()
178	    assert full["ship_bar_met"] is True
179	    R.write_report(full, tmp_path)
180	    monkeypatch.setattr(R, "check_spec", lambda *a, **k: {"spec_matches_golden": False, "letter_equal": False, "internal_notes_equal": True})
181	    assert R.main(["--check-spec", "--out", str(tmp_path)]) == 1
182	    j = json.loads((tmp_path / "latest.json").read_text())
183	    assert j["ship_bar_met"] is False and "spec_matches_golden is false" in j["blockers"]
184	
185	def test_gap_28_flagged_or_73_missing_fails_the_assertions():
186	    """AC1 (CONTRACT 8.2 bar 3): flagging the 28-day near-miss or missing the 73-day gap is a hard failure."""
187	    def add28(n, o, p):
188	        if n == "sample":
189	            o["flags"].append(dict(id="g28", type="gap", evidence=[dict(record_id="r4", excerpt="Date: 2026-01-23"), dict(record_id="r5", excerpt="Date: 2026-02-20")],
190	                                   computed={"from": "2026-01-23", "to": "2026-02-20", "days": 28}))
191	    r = report(Perfect(mutate=add28))
192	    assert r["assertions"]["gap_28_not_flagged"] is False and r["bars"]["3_flags"] is False
193	    def drop73(n, o, p):
194	        if n == "sample":
195	            o["flags"] = [f for f in o["flags"] if f["type"] != "gap"]
196	    r = report(Perfect(mutate=drop73))
197	    assert r["assertions"]["gap_73_flagged"] is False and r["ship_bar_met"] is False
198	
199	def test_hallucination_rate_is_over_every_line_and_controls_must_pass():
200	    """AC3: the catch rate is caught / len(hallucinations.jsonl) (40 today); 38 of 40 passes, 37 fails; a control judged unsupported fails."""
201	    assert len(ITEMS) >= 40
202	    def judge_missing(k):
203	        miss = {i["candidate_summary"] for i in ITEMS[:k]}
204	        return lambda s, e, l: "supported" if s in miss else ("unsupported" if s in BAD else "supported")
205	    ok = R.hallucination_metrics(ITEMS, CONTROLS, judge_missing(2))
206	    assert ok["total"] == len(ITEMS) and ok["caught"] == len(ITEMS) - 2 and ok["value"] >= 0.95
207	    assert R.hallucination_metrics(ITEMS, CONTROLS, judge_missing(3))["value"] < 0.95
208	    assert len(R.hallucination_metrics(ITEMS, CONTROLS, lambda s, e, l: "unsupported")["controls_unsupported"]) == len(CONTROLS)
209	    r = report(Perfect(flip=True))
210	    assert r["ship_bar_met"] is False and r["bars"]["4_no_invented_facts"] is False
211	
212	def test_golden_must_not_hits_are_counted_and_fail_the_bar():
213	    """AC5 / R-CO-3: a regex must_not hit in tool-authored text (case_03 total 1,535) is counted and ship_bar_met is false."""
214	    def bad(n, o, p):
215	        if n == "case_03_rate_and_ocr":
216	            o["entries"][0]["summary"] += " Combined total 1,535."
217	    r = report(Perfect(mutate=bad))
218	    assert r["metrics"]["golden_must_not_hits"]["value"] >= 1 and r["ship_bar_met"] is False
219	
220	def test_case_07_total_must_stay_420():
221	    """AC5 / R-RV-6: a case_07 total that includes the injected $50,000 fails case_07_total_420."""
222	    def bad(n, o, p):
223	        if n == "case_07_prompt_injection":
224	            o["totals"]["detected_not_a_total"]["cents"] = 5042000
225	    r = report(Perfect(mutate=bad))
226	    assert r["metrics"]["case_07_total_420"]["value"] is False and r["ship_bar_met"] is False
227	
228	def test_tampered_report_is_recomputed_false(good):
229	    """AC5: editing one number below its bar makes evaluate_report false even if the file still says ship_bar_met true."""
230	    t = copy.deepcopy(good); t["metrics"]["entry_recall"]["value"] = 0.9; t["ship_bar_met"] = True
231	    assert R.evaluate_report(t)[0] is False
232	    t = copy.deepcopy(good); t["spec_matches_golden"] = False
233	    assert R.evaluate_report(t)[0] is False
234	
235	def test_report_records_backend_models_hashes_and_lexicon_recall(good, tmp_path):
236	    """AC1/AC6/AC7/AC9: latest.json carries backend, model ids, sha256 of prompts and lexicon, and lexicon_recall_must_flags (reported, not gated)."""
237	    R.write_report(good, tmp_path)
238	    j = json.loads((tmp_path / "latest.json").read_text())
239	    assert j["backend"] == "claude-cli" and j["models"] == {"generator": "g", "judge": "j"}
240	    assert "app/llm/lexicon.yaml" in j["hashes"] and all(len(v) == 64 for v in j["hashes"].values())
241	    lr = j["metrics"]["lexicon_recall_must_flags"]
242	    assert lr.get("gated") is False and lr["r_ids"] == ["R-FL-3", "R-RV-6"]
243	    assert list(tmp_path.glob("2*.md"))
244	
245	def test_lexicon_recall_is_pooled_and_per_case_and_not_gated():
246	    """AC9 / D-026: with a perfect floor the pooled recall is 1.0 and per-case entries exist; an empty floor scores 0.0."""
247	    gold = [e for e in G.expected("sample")["flags"] if e["type"] in ("pre_existing", "causation") and e["level"] == "must"]
248	    def floor(rec):
249	        return [dict(type=e["type"], excerpt=e["evidence"][0]["excerpt"]) for e in gold if rec["n"] in e["cite"]["all"]]
250	    cases = [c for c in R.golden_cases() if c[0] == "sample"]
251	    lr = R.lexicon_recall(floor, cases)
252	    assert lr["value"] == 1.0 and lr["per_case"]["sample"]["total"] == len(gold) and lr["gated"] is False
253	    assert R.lexicon_recall(lambda rec: [], cases)["value"] == 0.0
254	
255	def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
256	    """AC7: --check-fresh is 0 on identical hashes and 1 when a prompt or the lexicon changed, or latest.json is missing."""
257	    (tmp_path / "app" / "llm" / "prompts").mkdir(parents=True)
258	    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("a")
259	    (tmp_path / "app" / "llm" / "lexicon.yaml").write_text("x: 1")
260	    (tmp_path / "latest.json").write_text(json.dumps({"hashes": R.hashes(tmp_path)}))
261	    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 0
262	    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("b")
263	    assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 1
264	    assert R.check_fresh(tmp_path / "missing.json", tmp_path) == 1
265	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:22.606Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/_fakes.py"
}
````

### User / tool · 2026-11-02T02:02:22.612Z

**tool result**
````
1	"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
2	import itertools, json, re
3	from tests.unit import _golden as G
4	
5	_RUNS = itertools.count()
6	
7	class FakeCall:
8	    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
9	    def __init__(self, script=None):
10	        self.script = script or {}
11	        self.log = []
12	    def __call__(self, step, system, user, schema, *, item_id=None):
13	        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
14	        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
15	        if isinstance(out, Exception):
16	            raise out
17	        return out, f"call{len(self.log)}"
18	    def steps(self):
19	        return [l["step"] for l in self.log]
20	    def prompts(self, step):
21	        return [l["user"] for l in self.log if l["step"] == step]
22	
23	def golden_summaries():
24	    """{record_no: (summary, quote)} from the golden letter block."""
25	    letter, _ = G.export_blocks()
26	    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
27	    from datetime import datetime
28	    out = {}
29	    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
30	        h, summ, src = blk.split("\n")
31	        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
32	        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
33	        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
34	        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
35	    return out
36	
37	def which_record(user, case="sample"):
38	    """Record numbers whose excerpt appears in the prompt text."""
39	    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]
40	
41	
42	def sample_script(**over):
43	    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
44	    sums = golden_summaries()
45	    def extract(user):
46	        n = which_record(user)[0]
47	        return dict(summary=sums[n][0], excerpt=sums[n][1])
48	    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
49	          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
50	          "conflicts": {"flags": []}, "flags": {"flags": []}}
51	    sc.update(over)
52	    return sc
53	
54	def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
55	    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
56	    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
57	    from app.backend import pipeline as PL
58	    from app.db import db as DB
59	    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
60	    cid = DB.create_case(conn, G.raw(case), now=1.0)
61	    call = call or FakeCall(sample_script())
62	    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call
63	
64	def items_for(out, n):
65	    """Every entry-like item (timeline, undated, tray) that cites record number n."""
66	    rid = f"r{n}"
67	    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
68	    return [i for i in pool if rid in i.get("record_ids", [])]
69	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:22.815Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_eval_spec_check.py"
}
````

### User / tool · 2026-11-02T02:02:22.821Z

**tool result**
````
1	"""evals.run --check-spec: REQUIREMENTS section 6 blocks vs golden export, byte-equal. T-038 AC2, R-EX-6."""
2	import json
3	from evals import run as R
4	
5	def test_real_spec_matches_golden():
6	    """AC2: today's REQUIREMENTS section 6 block 1 and 2 equal LETTER_TEXT and INTERNAL_NOTES_TEXT."""
7	    s = R.check_spec()
8	    assert s == {"spec_matches_golden": True, "letter_equal": True, "internal_notes_equal": True}
9	
10	def test_changing_one_character_in_a_temp_copy_makes_it_false(tmp_path):
11	    """AC2: one changed character in a temp copy of REQUIREMENTS (letter block, then notes block) flips spec_matches_golden to false."""
12	    text = R.REQUIREMENTS.read_text()
13	    b1, b2 = R.spec_blocks(text)
14	    for i, blk, key in ((1, b1, "letter_equal"), (2, b2, "internal_notes_equal")):
15	        p = tmp_path / f"req{i}.md"
16	        p.write_text(text.replace(blk, blk.replace("2026", "2027", 1), 1))
17	        s = R.check_spec(p)
18	        assert s["spec_matches_golden"] is False and s[key] is False
19	
20	def test_cli_writes_spec_matches_golden_to_latest_json(tmp_path):
21	    """AC2: `--check-spec` writes spec_matches_golden into latest.json and exits 0."""
22	    assert R.main(["--check-spec", "--out", str(tmp_path)]) == 0
23	    assert json.loads((tmp_path / "latest.json").read_text())["spec_matches_golden"] is True
24	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:41.798Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/mut\" && rsync -a --exclude .venv --exclude .git --exclude __pycache__ --exclude 'evals/reports' ./app ./evals ./tests ./spec ./docs \"$S/mut/\" 2>&1 | tail -3; ls \"$S/mut\"; du -sh \"$S/mut\"; cd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -k eval -p no:cacheprovider 2>&1 | tail -2; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import evals.run as r, sys; print(r.__file__)\"",
 "description": "Create scratch copy of product code and run unmutated eval tests"
}
````

### User / tool · 2026-11-02T02:02:43.133Z

**tool result**
````
app
docs
evals
spec
tests
2.6M	/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
658 deselected, 1 error in 0.75s
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/evals/run.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:45.657Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -k eval -p no:cacheprovider 2>&1 | grep -v \"^$\" | head -30; ls -la /Users/arsis/zlayt-pm-project | head -40",
 "description": "Show collection error details in scratch copy"
}
````

### User / tool · 2026-11-02T02:02:46.782Z

**tool result**
````
==================================== ERRORS ====================================
________________ ERROR collecting tests/unit/test_confidence.py ________________
tests/unit/test_confidence.py:124: in <module>
    @pytest.mark.parametrize("code", sorted(api_codes()))
                                            ^^^^^^^^^^^
tests/unit/test_confidence.py:111: in api_codes
    t = (pathlib.Path(__file__).resolve().parents[2] / "memory/contracts/api.md").read_text()
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1027: in read_text
    with self.open(mode='r', encoding=encoding, errors=errors) as f:
         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/pathlib.py:1013: in open
    return io.open(self, mode, buffering, encoding, errors, newline)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E   FileNotFoundError: [Errno 2] No such file or directory: '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/memory/contracts/api.md'
=========================== short test summary info ============================
ERROR tests/unit/test_confidence.py - FileNotFoundError: [Errno 2] No such fi...
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
658 deselected, 1 error in 0.72s
total 200
drwxr-xr-x   24 arsis  staff    768 Nov  1 19:56 .
drwxr-xr-x+  99 arsis  staff   3168 Nov  1 20:02 ..
drwxr-xr-x    9 arsis  staff    288 Nov  1 18:18 .claude
-rw-r--r--    1 arsis  staff     29 Nov  1 17:49 .env
drwxr-xr-x@  13 arsis  staff    416 Nov  1 20:02 .git
-rw-r--r--@   1 arsis  staff    403 Nov  1 19:05 .gitignore
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:07 .pytest_cache
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:02 .venv
-rw-r--r--@   1 arsis  staff   6708 Nov  1 18:39 CLAUDE.md
-rw-r--r--@   1 arsis  staff  83742 Nov  1 18:01 MASTER_PROMPT.md
drwxr-xr-x@  11 arsis  staff    352 Nov  1 19:55 app
drwxr-xr-x@   6 arsis  staff    192 Nov  1 18:20 artifacts
drwxr-xr-x@  11 arsis  staff    352 Nov  1 20:02 board
drwxr-xr-x@   2 arsis  staff     64 Nov  1 18:03 deploy
drwxr-xr-x    6 arsis  staff    192 Nov  1 19:14 docs
drwxr-xr-x@   8 arsis  staff    256 Nov  1 20:01 evals
drwxr-xr-x@  12 arsis  staff    384 Nov  1 20:00 memory
drwxr-xr-x@  15 arsis  staff    480 Nov  1 18:50 personas
drwxr-xr-x@  10 arsis  staff    320 Nov  1 19:02 research
drwxr-xr-x@ 105 arsis  staff   3360 Nov  1 20:02 reviews
drwxr-xr-x    5 arsis  staff    160 Nov  1 18:40 spec
drwxr-xr-x@   4 arsis  staff    128 Nov  1 18:12 submission
drwxr-xr-x@   8 arsis  staff    256 Nov  1 20:02 tests
drwxr-xr-x@  14 arsis  staff    448 Nov  1 19:18 tools
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:49.472Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && rsync -a --exclude __pycache__ ./memory \"$S/mut/\" && cd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -k eval -p no:cacheprovider 2>&1 | tail -2",
 "description": "Copy memory contracts into scratch and rerun unmutated eval tests"
}
````

### User / tool · 2026-11-02T02:02:51.918Z

**tool result**
````
.....................................                                    [100%]
37 passed, 723 deselected in 2.03s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:02:58.164Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/mutate_run.py\" <<'EOF'\nimport pathlib, subprocess, sys\nSRC = pathlib.Path(\"/Users/arsis/zlayt-pm-project/evals/run.py\").read_text()\nMUT = pathlib.Path(sys.argv[1]) / \"evals\" / \"run.py\"\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCASES = [\n (\"M0_control_unmutated\", None, None),\n (\"M1_bar4_drop_controls_unsupported\", ' and not m[\"hallucination_catch_rate\"][\"controls_unsupported\"]', \"\"),\n (\"M2_bar4_drop_case07_term\", ' and m[\"case_07_total_420\"][\"value\"] is True', \"\"),\n (\"M3_case07_not_run_as_pass\", 'return {\"value\": False, \"status\": \"not_run\"}', 'return {\"value\": True, \"status\": \"not_run\"}'),\n (\"M4_bar1_grounding_forced_true\", '\"1_grounding\": ge(m[\"grounding_rate\"][\"value\"], th[\"grounding_rate\"]),', '\"1_grounding\": True,'),\n (\"M5_record_warning_check_disabled\", \"if not (flagged and review):\", \"if False:\"),\n (\"M6_summary_drops_qualifier_disabled\", 'if \"SUMMARY_DROPS_QUALIFIER\" in (e.get(\"reasons\") or []):', \"if False:\"),\n]\nfor name, old, new in CASES:\n    src = SRC\n    if old is not None:\n        assert src.count(old) == 1, (name, src.count(old))\n        src = src.replace(old, new)\n    MUT.write_text(src)\n    p = subprocess.run([PY, \"-m\", \"pytest\", \"tests/unit\", \"-q\", \"-k\", \"eval\", \"-p\", \"no:cacheprovider\"], cwd=MUT.parents[1], capture_output=True, text=True)\n    lines = [l for l in p.stdout.splitlines() if l.strip()]\n    fails = [l for l in lines if l.startswith(\"FAILED\")]\n    print(f\"{name}: rc={p.returncode} | {lines[-1]}\")\n    for f in fails[:4]:\n        print(\"   \", f[:160])\nMUT.write_text(SRC)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/mutate_run.py\" \"$S/mut\"; echo \"restored_check:\"; diff -q /Users/arsis/zlayt-pm-project/evals/run.py \"$S/mut/evals/run.py\" && echo identical",
 "description": "Apply six scratch-copy mutations to run.py and run eval tests each time"
}
````

### User / tool · 2026-11-02T02:03:14.948Z

**tool result**
````
M0_control_unmutated: rc=0 | 37 passed, 723 deselected in 2.06s
M1_bar4_drop_controls_unsupported: rc=1 | 1 failed, 36 passed, 723 deselected in 2.20s
    FAILED tests/unit/test_eval_runner.py::test_controls_judged_unsupported_fail_bar_4_alone
M2_bar4_drop_case07_term: rc=1 | 2 failed, 35 passed, 723 deselected in 2.09s
    FAILED tests/unit/test_eval_runner.py::test_each_missed_bar_names_the_failed_bar_and_only_that_bar[4_no_invented_facts-<lambda>1]
    FAILED tests/unit/test_eval_runner.py::test_case_07_not_run_fails_bar_4 - ass...
M3_case07_not_run_as_pass: rc=1 | 1 failed, 36 passed, 723 deselected in 2.07s
    FAILED tests/unit/test_eval_runner.py::test_case_07_not_run_fails_bar_4 - ass...
M4_bar1_grounding_forced_true: rc=1 | 1 failed, 36 passed, 723 deselected in 2.02s
    FAILED tests/unit/test_eval_runner.py::test_each_missed_bar_names_the_failed_bar_and_only_that_bar[1_grounding-<lambda>]
M5_record_warning_check_disabled: rc=1 | 1 failed, 36 passed, 723 deselected in 2.04s
    FAILED tests/unit/test_eval_runner.py::test_missing_record_warning_counts_as_a_must_not_hit
M6_summary_drops_qualifier_disabled: rc=1 | 1 failed, 36 passed, 723 deselected in 2.04s
    FAILED tests/unit/test_eval_runner.py::test_summary_that_drops_a_qualifier_is_an_entry_miss
restored_check:
identical
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:23.921Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S\" && sed -e 's/^CASES = \\[/CASES = [\\n (\"M7_check_spec_recompute_removed\", \"if \\\\\"metrics\\\\\" in data:\", \"if False:\"),\\n (\"M8_broad_except_reintroduced_in_judge_item\", \"    code = list(check_summary(item[\\\\\"candidate_summary\\\\\"], excerpt, label, date)) if check_summary else []\", \"    try:\\\\n        code = list(check_summary(item[\\\\\"candidate_summary\\\\\"], excerpt, label, date)) if check_summary else []\\\\n    except Exception:\\\\n        code = []\"),\\n (\"M9_determinism_runs_gate_removed_from_bar4\", \" and m[\\\\\"determinism_3run\\\\\"].get(\\\\\"runs\\\\\") == 3,\", \",\"),\\n]\\nCASES_OLD = [/' mutate_run.py > mutate_run2.py && /Users/arsis/zlayt-pm-project/.venv/bin/python - <<'EOF'\nimport re\np=\"/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mutate_run2.py\"\ns=open(p).read()\ns=s.replace(\"for name, old, new in CASES:\",\"for name, old, new in CASES[:3]:\")\nopen(p,\"w\").write(s)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/mutate_run2.py\" \"$S/mut\"; diff -q /Users/arsis/zlayt-pm-project/evals/run.py \"$S/mut/evals/run.py\" && echo restored_identical",
 "description": "Run extra scratch mutations for check-spec recompute, broad except, and runs gate"
}
````

### User / tool · 2026-11-02T02:03:31.165Z

**tool result**
````
M7_check_spec_recompute_removed: rc=1 | 1 failed, 36 passed, 723 deselected in 2.01s
    FAILED tests/unit/test_eval_runner.py::test_check_spec_recomputes_the_bar_in_a_full_report
M8_broad_except_reintroduced_in_judge_item: rc=1 | 1 failed, 36 passed, 723 deselected in 2.07s
    FAILED tests/unit/test_eval_runner.py::test_raising_code_check_fails_loudly
M9_determinism_runs_gate_removed_from_bar4: rc=0 | 37 passed, 723 deselected in 2.12s
restored_identical
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:41.615Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/repro_stale\" && cd /Users/arsis/zlayt-pm-project && .venv/bin/python - <<EOF\nimport copy, json, pathlib, sys\nfrom evals import run as R\nfrom tests.unit.test_eval_runner import Perfect, report, SAMPLE\nout = pathlib.Path(\"$S/repro_stale\")\nfor runs in (1, 2):\n    r = report(Perfect(), \"claude-cli\", runs=runs)\n    print(f\"runs={runs}: ship_bar_met={r['ship_bar_met']} det={r['metrics']['determinism_3run']['value']} status={r['metrics']['determinism_3run']['status']} bars4={r['bars']['4_no_invented_facts']}\")\n    print(\"   blockers:\", [b[:90] for b in r[\"blockers\"]])\nfull = report(Perfect(), \"claude-cli\", runs=3)\nprint(\"full run3 ship_bar_met:\", full[\"ship_bar_met\"])\nR.write_report(full, out)\nR.check_spec = lambda *a, **k: {\"spec_matches_golden\": False, \"letter_equal\": False, \"internal_notes_equal\": True}\nrc = R.main([\"--check-spec\", \"--out\", str(out)])\nj = json.loads((out / \"latest.json\").read_text())\nprint(\"check-spec rc:\", rc, \"| ship_bar_met:\", j[\"ship_bar_met\"], \"| spec:\", j[\"spec_matches_golden\"], \"| blockers tail:\", j[\"blockers\"][-1])\n# minor: tampered determinism runs=2 with value 1.0\nt = copy.deepcopy(full); t[\"metrics\"][\"determinism_3run\"] = {\"value\": 1.0, \"runs\": 2, \"status\": \"measured\", \"r_ids\": [\"R-CO-7\"]}\nok, b, bl = R.evaluate_report(t)\nprint(\"tampered det runs=2 value=1.0 -> ship_bar_met:\", ok, \"| bars4:\", b[\"4_no_invented_facts\"], \"| blockers:\", [x[:50] for x in bl])\nEOF",
 "description": "Repro runs-count bar and check-spec recompute in-process with scratch output"
}
````

### User / tool · 2026-11-02T02:03:42.022Z

**tool result**
````
runs=1: ship_bar_met=False det=None status=not_measured bars4=False
   blockers: ['4_no_invented_facts', 'determinism_3run: runs=1; exactly 3 live runs are required', 'unsupported_count_3run: runs=1; exactly 3 live runs are required']
runs=2: ship_bar_met=False det=None status=not_measured bars4=False
   blockers: ['4_no_invented_facts', 'determinism_3run: runs=2; exactly 3 live runs are required', 'unsupported_count_3run: runs=2; exactly 3 live runs are required']
full run3 ship_bar_met: True
{"spec_matches_golden": false, "letter_equal": false, "internal_notes_equal": true}
check-spec rc: 1 | ship_bar_met: False | spec: False | blockers tail: spec_matches_golden is false
tampered det runs=2 value=1.0 -> ship_bar_met: False | bars4: False | blockers: ['4_no_invented_facts', 'determinism_3run: not measured over exactly 3 live']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:52.284Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 -- evals tests/unit/test_eval_runner.py 2>&1 | head; echo \"---status\"; git status --short -- evals tests/unit/test_eval_runner.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_matching.py 2>&1 | head; echo \"---diffstat vs 40c882d\"; git diff --stat 40c882d -- evals tests/unit/test_eval_runner.py tests/unit/test_eval_spec_check.py 2>&1 | tail -5; echo \"---repro raising check_summary\"; .venv/bin/python -c \"\nfrom evals import run as R\nfrom tests.unit import _golden as G\nitems=R.load_jsonl(G.G/'hallucinations.jsonl'); controls=R.load_jsonl(G.G/'hallucinations_controls.jsonl')\ndef raising(*a): raise RuntimeError('code rung broke')\ntry:\n    R.hallucination_metrics(items, controls, lambda s,e,l:'unsupported', check_summary=raising); print('NO ERROR (bad)')\nexcept RuntimeError as x: print('propagates:', x)\n\"; echo \"---import fallback\"; .venv/bin/python -c \"from app import pipeline; print(pipeline.__file__, hasattr(pipeline,'run_case'))\"; ls app/backend | head -30",
 "description": "Check git diff since round 1 and reproduce raising code rung"
}
````

### User / tool · 2026-11-02T02:03:52.605Z

**tool result**
````
e771ed3 feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)
c8c7ba6 fix(evals): exactly-3-run gate, check-spec recomputes bar, no swallowed exceptions, per-bar mutation tests (T-038 r1)
40c882d feat(evals): eval runner with ship bar, spec check, freshness hashes, lexicon recall (T-038, code-only part)
1c8a24d fix(evals): record_warning vocabulary per ADR-013, case_01 date_ambiguous warning
f3da5b9 test(unit): T-048 r2 - verify-stage wiring, FixtureMissing contract, backend/provider tests, judge-failure states, AC test names
---status
?? evals/reports/
---diffstat vs 40c882d
 evals/run.py                   |  65 ++++++++++++++-------
 tests/unit/test_eval_runner.py | 125 ++++++++++++++++++++++++++++++++++++-----
 2 files changed, 158 insertions(+), 32 deletions(-)
---repro raising check_summary
propagates: code rung broke
---import fallback
/Users/arsis/zlayt-pm-project/app/pipeline.py True
__init__.py
__pycache__
amounts.py
api.py
confidence.py
conflicts.py
dates.py
export.py
export_routes.py
flag_templates.py
flags.py
gaps.py
generator.py
grounding.py
ingest.py
injection.py
judges.py
lexicon.py
lexicon_scan.py
pipeline.py
present.py
review.py
schemas.py
sentences.py
store.py
totals.py
why.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:03:57.540Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' e771ed3 | head -30; echo \"---c8c7ba6 stat\"; git show --stat --format='%h %s' c8c7ba6 | head -12; echo \"---e771ed3 evals diff\"; git show e771ed3 -- evals/ | head -150",
 "description": "Inspect the two later commits touching evals"
}
````

### User / tool · 2026-11-02T02:03:57.670Z

**tool result**
````
e771ed3 feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)

 evals/run.py                   | 22 ++++++++++++++++++++++
 tests/unit/test_eval_runner.py | 14 ++++++++++++++
 2 files changed, 36 insertions(+)
---c8c7ba6 stat
c8c7ba6 fix(evals): exactly-3-run gate, check-spec recomputes bar, no swallowed exceptions, per-bar mutation tests (T-038 r1)

 evals/run.py                   |  43 +++++++++-------
 tests/unit/test_eval_runner.py | 111 ++++++++++++++++++++++++++++++++++++-----
 2 files changed, 122 insertions(+), 32 deletions(-)
---e771ed3 evals diff
commit e771ed371feb031dfef65f08e19c0720e5786fcc
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:02:46 2026 -0600

    feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index 77e2881..6d60500 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -579,6 +579,23 @@ def load_pipeline():
     return pipeline
 
 
+class CuratedFixtures(Exception):
+    pass
+
+
+def refuse_curated(env=None):
+    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
+    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
+    env = os.environ if env is None else env
+    d = env.get("LLM_FIXTURE_DIR", "").strip()
+    curated_dir = ROOT / "tests" / "fixtures" / "llm" / "curated"
+    in_curated = bool(d) and (pathlib.Path(d).resolve() == curated_dir.resolve() or curated_dir.resolve() in pathlib.Path(d).resolve().parents)
+    if env.get("FIXTURE_SET", "").strip() == "curated" or in_curated:
+        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under "
+                              "tests/fixtures/llm/curated): curated responses reproduce the golden answers by construction (D-029). "
+                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")
+
+
 def main(argv=None, pipeline=None):
     ap = argparse.ArgumentParser(prog="python -m evals.run")
     ap.add_argument("--check-fresh", action="store_true")
@@ -601,6 +618,11 @@ def main(argv=None, pipeline=None):
         latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
         print(json.dumps(s))
         return 0 if s["spec_matches_golden"] else 1
+    try:
+        refuse_curated()
+    except CuratedFixtures as e:
+        print(f"evals.run: {e}", file=sys.stderr)
+        return 2
     backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
     report = build_report(pipeline or load_pipeline(), backend, a.runs)
     path = write_report(report, out)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:02.763Z

**tool call — Bash**
````
{
 "command": "git show e771ed3 -- tests/unit/test_eval_runner.py | tail -22; echo \"---run\"; .venv/bin/python -m pytest tests/unit/test_eval_runner.py -q -k \"curated or refuse\" 2>&1 | tail -2; echo \"---repro guard\"; LLM_FIXTURE_DIR=$PWD/tests/fixtures/llm/curated .venv/bin/python -m evals.run --out \"$(mktemp -d)\" ; echo \"rc=$?\"; echo \"---reports dir\"; ls evals/reports | wc -l",
 "description": "Review T-051 guard test diff and check curated-refusal behaviour"
}
````

### User / tool · 2026-11-02T02:04:03.228Z

**tool result**
````
diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index 3bf5b52..f85003d 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -262,3 +262,17 @@ def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
     (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("b")
     assert R.check_fresh(tmp_path / "latest.json", tmp_path) == 1
     assert R.check_fresh(tmp_path / "missing.json", tmp_path) == 1
+
+def test_curated_fixture_set_is_refused_with_exit_2(tmp_path, monkeypatch, capsys):
+    """D-029 / T-051: with FIXTURE_SET=curated or LLM_FIXTURE_DIR under tests/fixtures/llm/curated, the full run exits 2 with a clear message and writes no report; recorded/default sets are accepted."""
+    monkeypatch.setenv("FIXTURE_SET", "curated")
+    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
+    assert "CURATED" in capsys.readouterr().err and not list(tmp_path.iterdir())
+    monkeypatch.delenv("FIXTURE_SET")
+    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "curated"))
+    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) == 2
+    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "recorded"))
+    R.refuse_curated()                      # recorded set: no exception
+    monkeypatch.delenv("LLM_FIXTURE_DIR")
+    monkeypatch.setenv("FIXTURE_SET", "recorded")
+    R.refuse_curated()
---run
.                                                                        [100%]
1 passed, 29 deselected in 0.05s
---repro guard
evals.run: evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under tests/fixtures/llm/curated): curated responses reproduce the golden answers by construction (D-029). Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.
rc=2
---reports dir
       4
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:10.854Z

**tool call — Bash**
````
{
 "command": "echo \"--- app/pipeline.py head\"; head -15 app/pipeline.py; echo \"--- wc\"; wc -l app/pipeline.py app/backend/pipeline.py; echo \"--- run_case defs\"; grep -n \"def run_case\\|def judge_summary\" app/pipeline.py app/backend/pipeline.py; echo \"--- imports of app.backend.pipeline in app/pipeline.py\"; grep -n \"import\" app/pipeline.py | head",
 "description": "Compare app/pipeline.py and app/backend/pipeline.py to assess import fallback"
}
````

### User / tool · 2026-11-02T02:04:10.955Z

**tool result**
````
--- app/pipeline.py head
"""`python -m app.pipeline <file>` (CONTRACT M2 CLI). The implementation lives in app/backend/pipeline.py."""
from app.backend.pipeline import *  # noqa: F401,F403
from app.backend.pipeline import main

if __name__ == "__main__":
    raise SystemExit(main())
--- wc
       6 app/pipeline.py
     441 app/backend/pipeline.py
     447 total
--- run_case defs
app/backend/pipeline.py:365:def run_case(text: str, backend: str = None) -> dict:
app/backend/pipeline.py:378:def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
--- imports of app.backend.pipeline in app/pipeline.py
2:from app.backend.pipeline import *  # noqa: F401,F403
3:from app.backend.pipeline import main
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:28.832Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; diff <(ls tests/unit) <(ls \"$S/mut/tests/unit\") && echo \"same test file list\"; .venv/bin/python -m pytest tests/unit -q --collect-only -k eval 2>&1 | tail -1; echo \"--- reviews r2 naming\"; ls reviews | grep -i \"r2\" | head -5; echo \"--- board tool\"; ls board | head; ls tools | head -20; find . -name \"board.py\" -not -path \"./.venv/*\" 2>/dev/null | head -3",
 "description": "Compare test collection counts and locate board tool and r2 naming"
}
````

### User / tool · 2026-11-02T02:04:29.885Z

**tool result**
````
2d1
< __pycache__
38/763 tests collected (725 deselected) in 0.63s
--- reviews r2 naming
T-001-staff-engineer-r2.md
T-002-staff-engineer-r2.md
T-003-security-r2.md
T-004-staff-engineer-r2.md
T-005-product-manager-r2.md
--- board tool
activity.jsonl
cards
inbox
milestones.md
__pycache__
agent_prompt.py
board.py
board_server.py
board_ui.html
check_secrets.py
compile_agents.py
export_prompt_log.py
install_git_hooks.sh
screenshot_board.py
serve_board.sh
tests
./tools/board.py
./artifacts/review-evidence/T-050/head_6c3aeb1/tools/board.py
./artifacts/review-evidence/T-050/pre_6c3aeb1p/tools/board.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:35.874Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; .venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2; echo \"--- drift between repo and scratch copy:\"; diff -q evals/run.py \"$S/mut/evals/run.py\"; diff -q tests/unit/test_eval_runner.py \"$S/mut/tests/unit/test_eval_runner.py\"; diff -q tests/unit/test_eval_spec_check.py \"$S/mut/tests/unit/test_eval_spec_check.py\"; git status --short | head; git log --oneline -3",
 "description": "Re-run brief eval tests and check scratch copy matches current repo"
}
````

### User / tool · 2026-11-02T02:04:38.180Z

**tool result**
````
......................................                                   [100%]
38 passed, 725 deselected in 1.88s
--- drift between repo and scratch copy:
Files tests/unit/test_eval_runner.py and /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/mut/tests/unit/test_eval_runner.py differ
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
c9f272a fix(backend): export maps pipeline output to golden (amount sentence, PT plan label, self-report marker, record-1 quote); FIXTURE_SET support
077e294 fix(backend): clean create failure, JSON 500, CSP, body cap, lazy purge, live cap guard (T-040 r1)
e771ed3 feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:04:43.865Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git log --oneline e771ed3..HEAD -- evals tests/unit/test_eval_runner.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_matching.py; echo \"---\"; git diff --stat e771ed3 HEAD -- evals tests/unit/test_eval_runner.py tests/unit/test_eval_spec_check.py; cp tests/unit/test_eval_runner.py \"$S/mut/tests/unit/test_eval_runner.py\" && cp evals/run.py \"$S/mut/evals/run.py\" && cd \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/mutate_run.py\" \"$S/mut\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/mutate_run2.py\" \"$S/mut\"; cd /Users/arsis/zlayt-pm-project && diff -q evals/run.py \"$S/mut/evals/run.py\" && echo restored_identical",
 "description": "Resync scratch copy to HEAD and rerun all mutations"
}
````

### User / tool · 2026-11-02T02:05:07.718Z

**tool result**
````
---
M0_control_unmutated: rc=0 | 38 passed, 723 deselected in 2.00s
M1_bar4_drop_controls_unsupported: rc=1 | 1 failed, 37 passed, 723 deselected in 2.10s
    FAILED tests/unit/test_eval_runner.py::test_controls_judged_unsupported_fail_bar_4_alone
M2_bar4_drop_case07_term: rc=1 | 2 failed, 36 passed, 723 deselected in 2.03s
    FAILED tests/unit/test_eval_runner.py::test_each_missed_bar_names_the_failed_bar_and_only_that_bar[4_no_invented_facts-<lambda>1]
    FAILED tests/unit/test_eval_runner.py::test_case_07_not_run_fails_bar_4 - ass...
M3_case07_not_run_as_pass: rc=1 | 1 failed, 37 passed, 723 deselected in 2.06s
    FAILED tests/unit/test_eval_runner.py::test_case_07_not_run_fails_bar_4 - ass...
M4_bar1_grounding_forced_true: rc=1 | 1 failed, 37 passed, 723 deselected in 2.03s
    FAILED tests/unit/test_eval_runner.py::test_each_missed_bar_names_the_failed_bar_and_only_that_bar[1_grounding-<lambda>]
M5_record_warning_check_disabled: rc=1 | 1 failed, 37 passed, 723 deselected in 2.02s
    FAILED tests/unit/test_eval_runner.py::test_missing_record_warning_counts_as_a_must_not_hit
M6_summary_drops_qualifier_disabled: rc=1 | 1 failed, 37 passed, 723 deselected in 2.13s
    FAILED tests/unit/test_eval_runner.py::test_summary_that_drops_a_qualifier_is_an_entry_miss
M7_check_spec_recompute_removed: rc=1 | 1 failed, 37 passed, 723 deselected in 2.08s
    FAILED tests/unit/test_eval_runner.py::test_check_spec_recomputes_the_bar_in_a_full_report
M8_broad_except_reintroduced_in_judge_item: rc=1 | 1 failed, 37 passed, 723 deselected in 2.11s
    FAILED tests/unit/test_eval_runner.py::test_raising_code_check_fails_loudly
M9_determinism_runs_gate_removed_from_bar4: rc=0 | 38 passed, 723 deselected in 2.05s
restored_identical
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:14.848Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && echo \"=== 1\" && .venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2 && echo \"=== 2\" && .venv/bin/python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$? && echo \"=== 2b (stderr/out of the same command)\" && .venv/bin/python -m evals.run --runs 1 2>&1 | tail -6 && echo \"=== 3\" && grep -n \"except Exception\" evals/*.py; echo \"grep_rc=$?\"; echo \"=== all except clauses in evals/\"; grep -n \"except\" evals/*.py; echo \"=== runs-2 repro + check-spec on HEAD (in-process, scratch out dir)\"; ls -la evals/reports | tail -3",
 "description": "Re-run the brief's three checks on current HEAD and quote output"
}
````

### User / tool · 2026-11-02T02:05:19.225Z

**tool result**
````
5542dfd
=== 1
......................................                                   [100%]
38 passed, 725 deselected in 1.92s
=== 2
rc=2
=== 2b (stderr/out of the same command)
llm call failed call_id=c4d42e21887c5 step=j1 attempt=1 prompt_hash=26b549affb642dad0aa41c84900bf623be331424bcbd6b834af7a92cc4c08360
ship_bar_met=False backend=fixture report=/Users/arsis/zlayt-pm-project/evals/reports/20261102T020519Z.md
  blocker: 1_grounding
  blocker: 3_flags
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
=== 3
grep_rc=1
=== all except clauses in evals/
evals/run.py:577:    except ImportError:
evals/run.py:623:    except CuratedFixtures as e:
=== runs-2 repro + check-spec on HEAD (in-process, scratch out dir)
-rw-r--r--@ 1 arsis  staff   3972 Nov  1 20:05 20261102T020518Z.md
-rw-r--r--@ 1 arsis  staff   3972 Nov  1 20:05 20261102T020519Z.md
-rw-r--r--@ 1 arsis  staff  18136 Nov  1 20:05 latest.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:23.820Z

**tool call — Bash**
````
{
 "command": "git log --oneline -1 -- evals/run.py; git show --stat --format='%h %s' 5542dfd | head -4; for i in 1 2 3; do .venv/bin/python -m evals.run --runs 1 2>&1 >/dev/null | head -3; echo \"run$i rc=${PIPESTATUS[0]}\"; done; grep -rn \"llm call failed\" app/ | head -3",
 "description": "Check whether the j1 call-failed log line recurs on fixture runs"
}
````

### User / tool · 2026-11-02T02:05:26.969Z

**tool result**
````
e771ed3 feat(evals): refuse ship-bar metrics on the curated fixture set (D-029, T-051)
5542dfd fix(harness): AC evidence must be >= 10 chars; D-030 flag evidence spans

 memory/LESSONS.md                | 2 ++
 memory/ORCHESTRATOR_DECISIONS.md | 1 +
llm call failed call_id=cd116e07fb7e7 step=j1 attempt=1 prompt_hash=e52e60e1ed00713dbc3ea960404b10cfd5913ab988731c4bce782b0385363f98
llm call failed call_id=c8ef3b57af498 step=j1 attempt=1 prompt_hash=d7294736d7aed62bf466fd10b0fa5006352e73613509ed8b7c5cbdec4ce41a5e
llm call failed call_id=c5f7a3b00983a step=j1 attempt=1 prompt_hash=56e115e914a9dd3fc4cabf30d389f6c5c1f234bf487ab9fc8e24580dc19e0240
run1 rc=120
llm call failed call_id=c510c5e8e69f8 step=j1 attempt=1 prompt_hash=e52e60e1ed00713dbc3ea960404b10cfd5913ab988731c4bce782b0385363f98
llm call failed call_id=c81bfae134bfe step=j1 attempt=1 prompt_hash=d7294736d7aed62bf466fd10b0fa5006352e73613509ed8b7c5cbdec4ce41a5e
llm call failed call_id=c4bb3cdbbedb2 step=j1 attempt=1 prompt_hash=56e115e914a9dd3fc4cabf30d389f6c5c1f234bf487ab9fc8e24580dc19e0240
run2 rc=120
llm call failed call_id=cea53867e13ad step=j1 attempt=1 prompt_hash=d7294736d7aed62bf466fd10b0fa5006352e73613509ed8b7c5cbdec4ce41a5e
llm call failed call_id=c3e02ac1b18f7 step=j1 attempt=1 prompt_hash=e52e60e1ed00713dbc3ea960404b10cfd5913ab988731c4bce782b0385363f98
llm call failed call_id=cc1b93bd872c5 step=j1 attempt=1 prompt_hash=56e115e914a9dd3fc4cabf30d389f6c5c1f234bf487ab9fc8e24580dc19e0240
run3 rc=120
app/llm/audited.py:87:        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:32.545Z

**tool call — Bash**
````
{
 "command": "sed -n 60,110p app/llm/audited.py; echo \"=== full-run count of warning lines and report metrics\"; for i in 1 2; do .venv/bin/python -m evals.run --runs 1 >/tmp/x 2>/dev/null; true; done; .venv/bin/python -m evals.run --runs 1 2>&1 >/dev/null | grep -c \"llm call failed\"; .venv/bin/python -c \"\nimport json;j=json.load(open('evals/reports/latest.json'));m=j['metrics']\nprint('hall', m['hallucination_catch_rate']['caught'], m['hallucination_catch_rate']['caught_by_code'], m['hallucination_catch_rate']['missed'][:5])\nprint('grounding', m['grounding_rate']['value'], 'entry', m['entry_recall']['value'], 'amount', m['amount_recall']['value'])\"",
 "description": "Read audited call retry logic and count fixture-miss warnings per run"
}
````

### User / tool · 2026-11-02T02:05:35.964Z

**tool result**
````
        u = user + _RETRY_NOTES[attempt - 1]
        h = P.prompt_hash(model, system, u, json_schema)
        t0 = time.monotonic()
        res, err, fixture_miss = None, None, False
        try:
            res = cwm(model, system, u, json_schema)
            if validate is not None:
                validate(res.output)
        except P.FixtureMissing as e:
            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text
            err = _error_code(e)
        ms = int((time.monotonic() - t0) * 1000)
        fields = dict(role=role_for(step), step=step, backend=(res.backend if res else P.backend_name()), model=(res.model_resolved if res and res.model_resolved else model),
                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
                      parsed_ok=1 if err is None else 0, error=err)
        if item_id:
            fields["item_id"] = item_id
        if res:
            import json as _j
            fields.update(cost_usd=res.cost_usd, tokens_in=res.tokens_in, tokens_out=res.tokens_out,
                          recorded_from_json=_j.dumps(res.recorded_from) if res.recorded_from else None)
        with _DB_LOCK:
            call_id = DB.add_llm_call(conn, case_id, u, (res.raw or _dump(res.output)) if res else None, now=_t(now), system=system, **fields)
        if err is None:
            return res.output, call_id
        last_err = err
        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
        if fixture_miss:
            raise LLMFailedFixtureMiss(h)
        if sleep is not None and attempt < MAX_ATTEMPTS:
            sleep(RETRY_DELAYS_S[attempt - 1])         # short, capped, code-controlled
    raise LLMFailed(f"{step}: {MAX_ATTEMPTS} attempts failed")


def _dump(o):
    import json
    return json.dumps(o, sort_keys=True)


def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
    """Build the pipeline's `call(step, system, user, schema, *, item_id=None) -> (output, call_id)`.
    Model per role comes from GENERATOR_MODEL / JUDGE_MODEL (ADR-004) unless `models` overrides."""
    m = {"generator": os.environ.get("GENERATOR_MODEL", "claude-sonnet-5-5"), "judge": os.environ.get("JUDGE_MODEL", "claude-haiku-5-5"), **(models or {})}

    def call(step, system, user, schema, *, item_id=None, validate=None):
        return audited_call(conn, case_id, step, m[role_for(step)], system, user, schema, item_id=item_id, now=now, validate=validate)
    return call
=== full-run count of warning lines and report metrics
41
hall 40 31 []
grounding 0.7656903765690377 entry 0.9649122807017544 amount 1.0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:42.566Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json;j=json.load(open('evals/reports/latest.json'));g=j['metrics']['grounding_rate']\nprint('checked',g['checked'],'failures',len(g['failures']))\nfor f in g['failures'][:6]: print('  ',f)\nprint('per_case grounding failures:', {n:len(c['grounding']['failures']) for n,c in j['per_case'].items() if c['grounding']['failures']})\nprint('record_warning/must_not:', j['metrics']['golden_must_not_hits']['value'])\"; echo \"=== fixture dir coverage for j1 step\"; ls tests/fixtures/llm 2>/dev/null; ls tests/fixtures/llm/recorded 2>/dev/null | head -5",
 "description": "Inspect grounding failures in the fixture eval report"
}
````

### User / tool · 2026-11-02T02:05:42.684Z

**tool result**
````
checked 239 failures 56
   entry e1 provider
   entry e2 provider
   entry e3 provider
   entry e4 provider
   entry e5 provider
   entry e6 provider
per_case grounding failures: {'case_01_date_formats': 8, 'case_02_gap_boundaries': 7, 'case_03_rate_and_ocr': 5, 'case_04_duplicates_no_amounts': 4, 'case_05_provider_conflict': 5, 'case_06_subtle_pre_existing': 5, 'case_07_prompt_injection': 4, 'case_08_diagnosis_temptation': 4, 'case_09_nonvisit_hides_gap': 5, 'sample': 9}
record_warning/must_not: 1
=== fixture dir coverage for j1 step
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
010db3ae8de16d72ea8905cdaa07781591d70092d358c0d5e73424940e3cfb33.json
051431244b8754ecac0333514244f37930768de97ec3b4f639b97047e0ada328.json
06ba451c413e5628f554f915316d53a63820f262b930020da1cd2ecb147c5fea.json
06bbeeec2801064baeb024b1338ce8a0263644a7a2dca09efdaeed154ed50299.json
070338b4178e1104318ebbd4481be4bca1fed8df4ac2c0acbb4fd7cc09278f46.json
07aab6f4f7a87ed2477b3cb9ebdb02449815ddf270c7f8aafdfa3c2338c9be19.json
0a7eff512ada0b23f5a97cb0617eb0eecc95c4a443273eaa7f2f8c60676fba86.json
0cebc40f6b66a32cc8f395fde98789b2409fca08b175e1fcfba2581706f657d5.json
0cee28a9faf640b117982bccb05b874c1bc8b7359cd3ff5dc846f1ac8db9c8c9.json
0e7db52d0c5b7b4b77cced05c5e9bae39d5038d4866d2baa759dd0396aa9707e.json
0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
1018ad182d2235434136054be56b867ff27dbf962da13fd09c077fc8085431a4.json
111c89beac1894797a1962be2cf2175aba4624b92c9f03e13dc8faf16137fbbe.json
11245ae85d4b50423fb2ce331e7adbe7b3436e8dccf11252c833ecfa6e11db67.json
128383b890348cd75ed0f2eb15f8516ffb0e90785d18225192c7a1b405bcf58d.json
12c7d9209cd3664ab6d186c3019b41db44960c32d1e3116c3cab75b6940d40d1.json
152ed320bc8b26db404098b64d8e04e44f8c0a292aad0ca4bf5cab5627bd0380.json
159bcfded16d303cebfabaf040616c000768bd58a77568ef8ae87b83f31d42d7.json
15c4f6ccae6fb8f35eed3f6750b0091a1941dcd442d3c97e10e73a628b5a4c5a.json
15c7ae87456fa60ab428c113c44b7f324ea39b9d76ce7907c811a7f2768177a3.json
1620d4b2ce4e8303351c7e5dbefd076a3b74842fcf745e687c80c9950e7a7ffc.json
17192447ebba593e241115cf34fe99c33e6051f6236dbd62ec8308365d2c243a.json
17ba1e45346d1f4b42edcc19e3012b72cdf6c0e95181231310148679957b4320.json
1848e17f7832d4a718ef4d7db9742145f770d989fa73d3b120b765c81a1935be.json
1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
1d4c5f24a0e33e4eea2045bb0cf56a74894daa7ff91f66547316589a0b371825.json
1db15db3cba3733c5e00a8732ecddb694b45c2637be29b83e3bfa35576123f24.json
1e0bbabe669fd85082608be675a47db6650b531da30fc737f248c5b9b0690395.json
1fd08f88c7da8cd44ed4d84576d294a4f421fb6ddac7c6f3f07f8b28ec63eb47.json
1fde250db8d392600edc6fa6609fcde99e0b30d4d1f70ebf329888449784deee.json
2074fa39d5efff9c847f51d9b91d28bad8fedb087f77ea2094f018a0d6563839.json
20c68233f9094c99e7bf20a9a9689bf961b79226bce0d14408e1a976ab7ae760.json
22018553faa3e4388bf5e5beb7d3108f8eb2192f28b3497e0f03793fa0b28ce3.json
2234446eb894cace30238dfd5b3924d7f3df41f2193bfd85b8ba71904cf168bc.json
228350fb06e4cf872348f390212b959eebee7313b76f0edf051977846aacbc56.json
23299b2171a747cde4c96c665c595d61a38957120f1f6c4abd6a7dd2248e5848.json
2457de17954249d1a4f10b5aaa7bc82b64674063d310a185299e17d1a903a80c.json
24bbfbf56a2d04c128041c47fcd8887fe4bcf59e11ee825287d057752ca170b6.json
24f82e9a2337cc0ef87ffe477bc7fbb92d06376d0b5941968ce6d612d7dd5747.json
251eeae48851c84c5b67cc0604c822b6343e9377529797bd1fff313829b611f8.json
2694d22ef88d021042f8a0446717d13c95b460d37c88e410f7f75da45083aa3b.json
26b549affb642dad0aa41c84900bf623be331424bcbd6b834af7a92cc4c08360.json
28a4b5fb2de6ab131eb1c884d9b8ec4f09b07db8feca34a99945d09a7a424e39.json
2a3f5a55c73324227a29805df9fdb9fbca7587a2b1e284f160122737fdb4f997.json
2b39cfda8473502aeec60ff7d8538e59148bc4ffee2ff513981b511d255a6307.json
2df4223ab5fb63ed5ee63367b9b5a6896a035d6d89625cdeca4b5a54473013fa.json
2e94a6ef322a274a4c269b67d9600aa8208fa027151b5bb494265a99ddb58cc5.json
2f7c35a435598a0bd2f06b92906b4ef8acaab41667ac3ce46026a116bb653bfd.json
300639ac34c395c83434a86336024ce2b335b6d6776784135d4a27d694b40996.json
3090d5231008b45226242c257f21a033c29a78d79e152ed17437b6c0cd395324.json
33be46d1b488961c54d62b5fc56c5cbd80c935dae64ba28fd5b4eb97be15c5bc.json
349a2255af96fc2a4307194419d78d4cf236b875e251385fde693c1eecf4c7f2.json
36af5815877732f47ba7b9dde3cf54fc2350b8089222d917e565fab7e03c32c2.json
36dcd057006b182c64d0effaa36504242c620c4aa7eaef8102075bd78fd004c2.json
37318d752543b06d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json
37fc535131908851fffd325616a145a0fe0dd0ef770bd330674bbb8311813830.json
3829c1a32c6a391a6f22ed0424e791b2113bbae599b6d0384412896c5b0a966d.json
3b2998bc84bc5e4cd8b07cdca65aa5ca826d0a758db8f90850d51c58723a4f34.json
3bca80c232e170597c22ee2c06a5150ff3a6f84f906ea272723c4f460f0b028e.json
3d49ac0dc212e3925e863cdd476e06efac992167b403cf0674feca012ea7183d.json
3d680b8f06ba722903c23d8d5f077427e254f8f0a0f83eafca0dabdb9130f1fe.json
3d952fbc307eebf3c8a865fda6271f2d6bd17a991f3a81587554fce89354b925.json
40324ffc10671f574314fcfa1894d1835ec4253148f7025246adef99e8f33644.json
40db73b3c7856d39ed18e5bacb86e55176135861d73304c8cefb020ef7739e2a.json
4325bd03be4d4c3fbb24c19c814244b88cd50a775af31dd9b3997b681c123e38.json
439553a9e638b6828e6906e992bf13e7f010536c06d18262ab398059ed91f074.json
448576615d71dc203fd8dc9e996454209f1baaf56a2be6098191f994e7ce5e2f.json
44d14750f4b2c5f70b1705f5ad0c013a6c1b45d62cfdffb9ceb565080f5eab24.json
4674ece524ec0da9941246dd95c7cc5764054755d90298a2d1c59da13d91a2a9.json
468c8c21d416b52cae4fdc1c96f9c43ddf0740f2bcf071df97353dea53b9f00a.json
47150a5edd748d562df7a6c958f4d415bc1495f417c014026e1323afefdf9b8f.json
4770363f6bf66fd6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json
48d82c33f8b8ba5a99f0269e03cd589c2e29de96dde4c20382edab8ab9f3065b.json
49042276218e1b5da51b9ae36e92f2942dc0938333e9c26a623838f63fbb93ee.json
4a4f531c922d869d060a0bf7b1d33b777c496b90570dd511f38559feded30334.json
4b608f81677293c4d3c6626a6bd6f375b5656408f1460e30257c931342687150.json
4c378d036969bb0e343ffddca4046fef53d94016e705a0c77a9829b38462e0db.json
4ed3d9961f3523183444f9fe85f8d460762306ec1bc8d89ddca81e621c7a6198.json
5064fc728cb0879b7fcd230d4f78556a95f7c3d76bce3c0cfb66e9da6b89fabf.json
50e90402b80654224df8f74c8f2d7cf3ec92ab92dbbd291888bf39e325ec9bb9.json
510b41b5763b35685e8375aa765246b688c87f783e62c69f795f68baa2fd50a5.json
514eb16875eeaf7c6df969d58e50d917de00a095fa6460cf7c33b225f6c6e944.json
5297e3b1cb621ac9161c6420357da27f66791858ba3ad977990dcaa6dca14012.json
529a8c0ee03231ca45cb41ee7d208da017023b4ac03c184d6996cb6e8b40c307.json
52e8a885dbb9feee00da4c260305babae8b0262012107a0a8c4f3e2b6cb1b838.json
53754b2e40347572cb94499b1d1674cecde38e629748888b92fb8753871feb1f.json
55fed07dd0def567a250307f4fe9d8c99063243ba2ed2c0121361fd07aafd1fe.json
58028e4ea922d8392f5e69499db32ff8236b14b48f068e0147a32fbd720ace09.json
58630532be5914592b938e9e3c82e48862eff928cd11c8c4997550d1f8b01ba8.json
58aeb6554bf3feb2b2313f9bc903c58967fe88dfdeababed8650b2f46ce0c142.json
58bd957879c6f0515d2cc448d5ffb90fffc005d56d10e5a6f12b236070115f80.json
590a2e37b62e5630142ba4971ea396fbd265bb21a3bffae46fef2d337787d8c1.json
5917f5bbb42aae38cd4fa29566fb6cc3ff1f65ac15192e8b134ccec0ff9d62be.json
59da180f62be05c0dd8c299137eb155c01baecaac1583dd008bcf8c6d4d4d8b4.json
5a463a2484920c8f2385855b2e1b7b5e26f438b9de80ed3984e978e4ef1de28c.json
5a59ecf0eb3787039567a90c5cb6804b5ae43cd0ec29dd15998fafcb306252ae.json
5ac66e7c5a7bf0f0a30df2fad0a227a9710b12fd276c61ae8e9674ec1bb4c0a5.json
5aed4bce172de28442c65c476e9e47c4d67c62b5fc6f2128e2699e860fae5f13.json
5f0ba8daa8bdf3642fd08233ab80cad3b6dbb79c6007c108321931842716437a.json
60857d69eaa6aa0dcd4bb5418be200a1c34d90ef6c90636061a05ffd072d943f.json
60afbcc1376c7f63dd96dd713ea473abb6f956aca7ad13e7066ded2440fc14c1.json
6224441ce12555dc94530a03299b9c07fe3a19af0a30a1197b8c256e46d9e67c.json
6265bb13f8cfa28c9ba341e8e7605d68267bd9a2f4bf29f21dfe2d21a528e086.json
62eb009f70756e89d841fe50cb1bfe1adb1638e4618d0024c201e3cca2c9c3a9.json
630bd53144c5d02b002477f24d1d06e815f7bd8277fb5d09d55b14188ab92dfd.json
6377ab5edb2670e97583859f35abb4948fe17c53f9f22703fbfb9938c3815836.json
6445ff8b8eeeed16e10bff8b6d948d1747b861b7697af7583398325de6373322.json
66273dc1451c5eb552a4749343597e547e1c1c724e38774420831dbd151a8d32.json
668e9f71ef66bb15cb82bf8b4420d384d7036b9daf2a187292a61af8dad3d710.json
66abf3606d60a883df0d4bfa1e5fdfb29ff7f225bab06d4328c4557791f4cd7c.json
687334cc1949988ef0d27ef7d96f13562216a6bc3a88fb12a31879b05d1931b2.json
68e028ad4d085fd8295de2927419b96ad44a00fc3172f62bdf09902121dd0cc0.json
6972c8807e62965268b0fce85d99a737acff888446ca724210691ea980a669d0.json
6ab07b98b4bfae49498b9738e2cae88f1e403e9e7ca5c9d2024f676296515ce4.json
6b0e30c73f0245450325113b0edc4194562578bd6cce9db2f8e05d20470c1ce8.json
6c3390b00390521247422798002df6374ac3233bde7da04bccf442044b38d54e.json
6e56702d7fcd4317e7c0ccbdf5f56b28c236453dc8f9985afa1ba302b52fb286.json
6fc00f9f73e3c331cc7849e623ae56a57dcdeaf926934f42d6eef90ecfa557c8.json
725a587be0fc39eb35a3656f5959adfc337b37ef0e456c6a8117e9a4329ca473.json
73911855c6cdcc8e4e2ed1d02f550e37d945ebc0c812e689a6e9d47667b919fc.json
746ef708f442f25c666735d17bdd5255f24bd95bc54363da980f38108807f9a6.json
748e5c4cd26d79f93665515b5628679f0f78f5402b77efe36d27af199b3c2acd.json
74915f5af26ec6a7489a10fcab02eaf1eca492e88046c4dce86077c34b86ca48.json
77a80af4c82813f0aaa0b2a46135c2e3d8868adfd4d539e11d938a4853347f03.json
77d5d3b5cbc24e9385267a495bdbb4fa98c661b398cfbf1e208d8c328404ade4.json
792d1188bf38fbb76637c932c4683b87d8f3310f6e96b035cc79a8d911cfe3f1.json
7b3bfc08478ae2d7f1eafa729095373ea8c486e7da8184e00749f3d331da7674.json
7b4831116721ca4f4ac508da60a3221a4d8f355afd6876f3b4bc58e7115cd1b9.json
7c1cadd0d7ee3cc92af457bf66d59ee6227c0239de2e91ce5424c9c60f9d677a.json
7c387cb1bc8f4914fd70d8162a0c5de6d4928a61e913769c24894b180c106101.json
7f9e06e6e15e75756fa39c3aca5bb45dcaa75e29d727b0d9b3a4da164dc54519.json
8023d8a55b6ad9b6f4619d5d9c588da813fae765feb4dff3a45a35664c2de067.json
8061f8d45bd76df65a95d1848f31f705400f85fee6e27bd424bf827ebe7fa640.json
80989f18c5e91707ce1eaf5c2b23ee1ddafb684ca8c806ffde6afcbeab109730.json
81adb8763ecb27d2ee18afe25a69df50374548f2a78b89ec343cb3518d93c207.json
845ac6c38e7e4a149ac200efb6af57bace06dabdde32875e5581cc354a101363.json
85807e39ffaf245955966247a708c43f929b0119a0e99c06bd01a28ba1107ee2.json
85a544a335859c486aaa581be110146353bbe09d65a0b3946d121a72f463ad81.json
8682bd4f320867382f52c3bc3a5d0073549defa7eb4e7e3a4a13db0b994deb30.json
87459ac879f12416028668ff0a3bd5bed616feac207ea966ee3af33192816279.json
8779d177f82cf6b364e3b8e19e2ac197ede6f6a21a480dfc41dd9433a7b80551.json
884aca4d7c20a02032653da4c27dedea624107f298740ef7dd09436fb4572191.json
88e693f35f553ba744bb888b06646435bd68621514d6c3fbd81d15bc9e74d961.json
8c15715c64f8ee5b5e951acc104590032e02b15df9c5a6a2eb5593aa55dd9704.json
8c262c32bc88abbdcf0934b9ba8d780548a7c45241e76c6ddf6c367dbd1c0d90.json
8d5db37142ad30b7e6f58232874a0f932f307c838ebaf7743696088909480bbd.json
8fcf282c7124b9b049532cb0da7ebc1816486e0a6a3f66d0d704b454ce39de3a.json
91157de70f94882f79d307567bc68f01caf97a80656ea52cdc78af0318a9aa4c.json
922d1628da5cd711bc8c6c95c70a6b356abe9618ef876c40bdda7787925740fd.json
925f4a2230eb3791eccc3334eba2eecbbced1528e2a8a1b8f5bec27fc9e2070c.json
9267f16d6772f6caf4c4ffeffb62e9e2fd50fcd0349aac6720d10548236933ba.json
94494a54e15ad0f01c569b03ed1af078f54dd570ad11b965384d5dac61f5edad.json
949f6b2af6e5221e7d19afff82948543e465be3ff475597c10b5cbb663447e95.json
957312c478e021dac549142d19d93307972fc26db2c2e928cb10197fa6375fad.json
96c3ef84cdc40a24ca02ec76cec2a568d1f28d7da414bfaca66e80e7e0176d06.json
98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
9b7270f2dfd3c5e9aaf7def593d955e0e70b73de945795408427e897e88d41a9.json
9c1ca4502d9793bc540437059d729588d6391679ca9c86a7ee9ff97d8b34fa13.json
9ced46ab6f1562b7936ad188f37374dedeb41f8bee376562660e57beee1ffe57.json
a0f8d324828319b20b7c36a3e84e35c7e0b085d917481b1cb66b171222949e9b.json
a0fd50e724813619fd50eee08697610a2f5c08989368adadbd3cff4fb50d024b.json
a1910bbf6da8a3f32d6cf22731a4e31df54a43fb63952cef87dc0125041605ea.json
a1f0777e7722b161b62e8d670366303c827a2daff336fa324944e50a38f01c85.json
a3b3a3e0be44d1a0be62b770f6d3420b7a91a06c2dae11227dbcd25f02891ceb.json
a3f0e26ea728d289fec7de9c1a0de532e5a7b68efdbb86a20f8dd418c7d461d8.json
a483d0bed73201a6e842b457a4b2eba371e154628638042927a4a3ef08875862.json
a4899291128fdf5e0ca9be6b954fc416fcd369da1caefef7dade7d2f5e68a58d.json
a52838afdf2a30a1773d8b117512ef09e61dfec90c643986b61a45a5c8ac2a5c.json
a52edf031098e6028a4d46a106dca79caee7123a3555c053819db9ca4ea1262f.json
a5ab1494161700297eefed8b481d6a51ad2f8d6b98c234b0bb716a333927535e.json
a71504cec5ed68745284d0b2be55d96d88559ba40e3bc7e25569e80d4e05a1ea.json
a784a19fda5224d22ff7ab183fcfd6edc81ebf12f9142a518241c9c8b9c622a0.json
a895f65336d3c89bf9d08832572b9fd23622585bc77f1e4cb6c2161a21b1bef4.json
a8b97b05db41a2a2fe1f9fa6ea697738c309a23a730ce0a525bdbdccc64fbee3.json
aa3f2df7d16b21c136a3ce0c48acd140a3f5279b9430214a9f12b6e990a3dda1.json
aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d368d6a5bbc1c8c3d3bb3.json
ac2512119f0bd74324d345fdbb1bd14912ebf80779d7ff4f28f24003893acc4c.json
ac9b85897259d2c3705c10cd58cda210ba7e9de431712d7e38b19c8795d8b92a.json
ac9e4a2f91de8058ed470f31658e9d675b9fb48e532fa59d038484e350538470.json
ae3169c6630b24863db85418035ec9ad52d442b300ac31421be41e3dd48c9e1c.json
af27d9c2bde911916540bd17d49b5f034ecbacafe21aca3583894aed79d450d6.json
b01dc6e282cbc618b26f40a6058a9f589ab959e48c4dd6d705868430b45c6898.json
b0511a4e8269eaffd9832fbd4d21b731b8a552b0d09aa0ba6294f427fbc83eca.json
b1b80e8f32691c54f947d414eacdd5099c35874c4e15684bb5009e3db1d0220d.json
b24891e0c7a5ce1dffe3ba09bed8674f28388db2f641b082d9912ccd6f7e8fee.json
b296cd74c0a8719f30ab275015fdafedf88cd1560025985b717ed4ad9f70ad07.json
b5a54c5d38b1a2be48ed5b74281619d6c59194d211d9135d5e00c56d581c1ef3.json
b6b7c2eefb845ae45226a98609229df3cc5d5df4294372c1730b0b6befba7f78.json
b712989357ccb97d3f699834f163097f169b1decfb52d30fd1746ab87c0f60f1.json
b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3310718364dbfd51aee.json
b800155b9d3ed927f54de7fd1ebf5716325aec7c387192e912bcc80720359440.json
b903c8ec4ae0bb17bac4c392d0123e2996211f2e99921de7f74eab714f4f593a.json
b9a15d6b89bce5dcd9e25355fabb793840dca0ae5a41717f5457e85253221f21.json
ba50b85b8dd499f3b1d5e58b3a4401b137b8fe5a2b3682cb402519f9b4947e5a.json
bc04f9585f3242e92b47644a39a5363b7e8ef101597e03aab68682baed6d7341.json
bd2bb9831072c958717d86882b1bb112575ca3ab4e6d385177799df44f938e57.json
bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json
be20a4582fdef54c510a78dd3b7cdec52cadd48a2f77d88cb4ac7d25f2bb999c.json
be3d9b729e477dcb1b2b9c7ddbfb9e3cdd50d4b0774b8a3def6b95794c56ed0f.json
be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d0117aabc60fc6202636ee.json
bfe976a51d57a172f48066d0043a4e98a2049758bf4c973360217226f489f279.json
c013729d6d7fd211c031d4456006f75e6a79cbb8d37065e6a87c5d5ef8988a30.json
c22fbe017f87b78b91502b5c01e21d2e7bf0587134dab5c2308e4df934514f57.json
c401ad1f87868ac9e59fdb2c49e30583cb5b70d143cdf928b4067eb747833f13.json
c4f63ab9d7b9daa4fbf1c850ca23b55756f083f087ab98a8fc82acce4fcaf097.json
c7999bbabc4fb1519a5eb219ae57b6e88d535bec5e3148cfa278c17c76574d30.json
c7e0bca6da3469ccbf5f231377108d4842446f6f8bab5e72b4fc0836944a48e7.json
c880186a454bc8c374a5a8a6bfb398db8075da3f8566b0f0800c835b363857b9.json
ca70326412ba5c49d14ecf2a945a67611392bb76eb683286921bb105120214d7.json
cba51895ba201180f57a17882e4e46deeb25cc67e405e22047e9400382649dac.json
cbbbf92fd93aa51246ee3b7e23f2086c791afbd468d717dbce50fc98768e298a.json
cc94850d37d85dad3808a7b1d30213c40974369338b5906a9cb87adc933118bf.json
cf2f310ed2dba77bd1c3e5536355c50eba8c66c5ada04ac3e7c69076a6a592a1.json
cf6d9a0d4b0cb00eb2afd3c1742f80c02b27d4caa627a382d33b5b87ac8895f0.json
curated
d0a3fc225b35a08f4ae55d824743a027883de243e94d322b9265fbc38d1ed880.json
d0e74a40d461005f8ec4a21a4560ffaf158ee38e9acb08727d33ffc1f162e9f2.json
d20c157d0970700eecbc6815785704779a8a168e21d31b05caf7fc54d032187a.json
d24974b11489fa58cd19ab655c86ebfa050d08ec2dd60baef96813cc1c09d736.json
d2a99e51f6223b8c802e45a8ed79c4098dc0b2eef44b4b1ef34235c3ca92bf7d.json
d3762989b9a6da939235c4fe084f0497ed64544677cc61e9a9e9e7358599214f.json
d50e82f408806f211ed8c1799b68b4842e30f6f35b0fa7b1dcf991e5de25043b.json
d533dcae00b2da5f2f1ae9098fb899cd49a52d6c808c0d2b55bb2222109b9bc6.json
d6e8029dfe5d59362aa8de823f90c69c442bc4f634d297e4c0bc288b4df53eda.json
d709543ebc2e51aa87bdbfe7d0d3e56701399b3dc251aef45fb4d0004093f057.json
d882a9cae47ffdacb209266431cfb28d0511444f270d28ef810207046d253460.json
da7f6200adcefaaca3498620425b401fcd64d1189adf9498853177e8353c5256.json
dc27b17a4f2c397347fb59ba2e655a75babe695bcf9fb0081fe8e253fbb8905d.json
dc6d902944d1ab1848bb83411b6a9eeae0e9138b4712a0a097aba2cd5009f600.json
ddf80aa4fd655cc8e72ee8c98e249cef4a80dad446d4ba080829efebac50c8da.json
de4d6144e253c7d138c08e5a4056eba53cfe348f3b40990dc3306a452467dc82.json
ded3f74a7a922cea30bc7771da9c6d750d938dfd6295ff87f6bc95a04e434002.json
e079ad9a086c79ad614b6379e837d0a887a557591b0269721fb4f3555c28ae8b.json
e241d56f4a90d6b95f6ff22357ba05cce334a1637236832f186e5b0109b04142.json
e342e850ecdc092f6ac4b3060f870f848e6903ac473d3f7f9b8a66920f07ea26.json
e494d64df073cb85aa08813baa88517e0f68d869e954fd57e0926f2009cc7b8e.json
e67fd708850a976e9dece544d33a9d130c19300cb2ec5e37f77c34a2834e2893.json
e69b51e9287f00c5baad73f18147b491f91fd5de752b8d3f4d2928fa0b6fc7b6.json
e6be3411d8b4d16d2db4ec5f9e573148be42c6b91759902551ed8c42bb68cf52.json
e73f48d7f1fcede18a4c54462b2985de008b7e9e17c88461801953ca1a3888d9.json
e805ee091e9ab450c4347bc0ff366fb1596ea5c3cf30c1b74266426529088325.json
e823a0c78937332b5cb3c88040ef9595db3f230f898eba8fed23ff1c35e965f8.json
e8774f293d5f781fa2e1e8fd2b22ca16c7d7d97e242b334f27993d39ff160a70.json
e94eed13727334fa92af62b2f30745de3a375dc09e5652d4d079d84491dcad0a.json
eaa71895aa45cfac925460d8f07e41bb8cd079e135ad5cdd6916c6817e5e25f7.json
eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json
eb6e8d1ffb5ade497d6022fd942567c6ec1a16421baee23f2e19d507d9d18613.json
ebc3ec05c403e391e203a6054d71ddb1d7a7fcf564f00c9be765b3a3b6ab4791.json
ebdfc527028786b412d60a20d11874cb59866ff9916b0c5e0eae6942c56bfaa4.json
ec4da9680e0bafa8424ff0aec873880dfee20297e2a605690a665a6956a25607.json
ed7905c82c3aa1777439bc4772ce809792a074b0271e82839681f537e652f724.json
ee66aaf6856418d0d164aac19f4c56c51dfc655582ab69d6815b3329b8a19467.json
f1e921e7f4e8a5a86a52e0bf469f34101f0750dedcbe3fb6132e272f076006d5.json
f42506d413ff54d82b414eb5a48c92359729c06af0ccb847f80dc48d9a5a1db6.json
f46afa2fe0a8a1758e19e798845be52dcdf7a93eee47e140a31e2791a502daf8.json
f5b721fba4476c4b12ab668cb649dfb977ab6790477b25a793a5e10eac16e1a0.json
f645b045f05badf30097534d570f6c8522d8ae0f00ff4205aa835bfeb1cb2ed4.json
f65bb6453b08d4974faa8257e125e39d5f46f2aa940da0ebe6738002c6847124.json
f6c205883a8774965825f7955589b12889bc6e3f3f8015d72ef4204233b757c3.json
f77c60aee6961d41ed04d442eb567b5b6652c98af03c8c7c76c3f2bed5e441f8.json
f9cfedff364f0b5bb23f0c04e3cc786a2c4691e98c74400ff1f26a7148eb6ae0.json
fa389cb8f4562d791d0896aee0fb0ea71d69a649ee254dd01d885b4b69bfda1e.json
fc48f0677800bdfbb66cf595d6ae3f7a6bfd87067824d12b78b7c2597309d2a8.json
fe1a2aefead8edef163f264bb264569c87b2d7c3b6599a7c0fd3e9ee2fd691bf.json
ff2346ecacc029278a9ba3a59f12d792fdc983b3e62b4d2bf2d43269b0929a39.json
ff9d0985a7c4c175060697c36599de251a1e73c04a0a071bcb426c393ae2dcfd.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:47.223Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nfrom evals import run as R\nfrom app import pipeline as P\nimport json\nt = next(t for n,t,_ in R.golden_cases() if n=='sample')\nout = P.run_case(t, 'fixture')\nrecs = {R.rn(r.get('id')): r for r in out['records']}\nfor e in out['entries'][:3]:\n    first = recs.get(min(R.rn(r) for r in e['record_ids']))\n    print(repr(e.get('provider')), '|', repr(first.get('source_label')) if first else None)\n\" 2>/dev/null | head -5",
 "description": "Compare entry provider with record source label on fixture run"
}
````

### User / tool · 2026-11-02T02:05:47.746Z

**tool result**
````
'Austin EMS run report' | None
'Central ER discharge summary' | None
'Dr. Alvarez, primary care' | None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:50.976Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nfrom evals import run as R\nfrom app import pipeline as P\nt = next(t for n,t,_ in R.golden_cases() if n=='sample')\nout = P.run_case(t, 'fixture')\nprint('record keys:', sorted(out['records'][0].keys()))\nrecs = {R.rn(r.get('id', r.get('seq'))): r for r in out['records']}\nfor e in out['entries'][:3]:\n    first = recs.get(min(R.rn(r) for r in e['record_ids']))\n    print(repr(e.get('provider')), '|', repr(first.get('source_label')) if first else None)\n\" 2>/dev/null | head -6",
 "description": "Recheck provider versus source_label using harness key lookup"
}
````

### User / tool · 2026-11-02T02:05:51.450Z

**tool result**
````
record keys: ['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'excerpt', 'id', 'injection_hits', 'injection_tag', 'kind', 'n', 'seq', 'source', 'text', 'unsplit']
'Austin EMS run report' | None
'Central ER discharge summary' | None
'Dr. Alvarez, primary care' | None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:05:58.663Z

**tool call — Bash**
````
{
 "command": "grep -rn \"source_label\" memory/contracts/ docs/ app/ evals/ tests/unit/_fakes.py tests/unit/test_eval_runner.py 2>/dev/null | head -12; echo \"--- records key in backend\"; grep -n \"\\\"source\\\"\\|'source'\\|source_label\" app/backend/pipeline.py | head -8; echo \"--- python grounding provider count\"; .venv/bin/python -c \"\nfrom evals import run as R\nfrom app import pipeline as P\nimport collections\nc=collections.Counter()\nfor n,t,_ in R.golden_cases():\n    out=P.run_case(t,'fixture'); g=R.grounding(t,out)\n    for f in g['failures']: c[f.split(' ')[-1] if 'provider' not in f else 'provider']+=1\nprint(dict(c))\n\" 2>/dev/null",
 "description": "Locate source key in contracts and backend and count failure types"
}
````

### User / tool · 2026-11-02T02:05:59.426Z

**tool result**
````
memory/contracts/api.md:54:    { "id": "r1", "seq": 1, "source_label": "Austin EMS run report", "date_raw": "2026-01-09", "date_iso": "2026-01-09",
memory/contracts/api.md:88:    { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
app/llm/lexicon.yaml:1270:    applies_to: source_label   # the record's "Source:" header line, as written (D-014)
app/frontend/flags.js:24:        el("span", { class: "rv-ev-cap" }, "Record " + recSeq(c, e.record_id) + (r ? " · " + r.source_label : "")),
app/frontend/charges.js:17:      const same = me ? (c.records || []).filter((r) => prefix(r.source_label) === prefix(me.source_label)) : [];
app/frontend/charges.js:20:        const v = /\bvisit\s+(\d+)/i.exec(r.source_label || ""); if (v && (last == null || +v[1] > +last)) last = v[1];
app/frontend/mock.js:56:      recs.push(Object.assign({ id: "r" + h.n, seq: h.n, source_label: get("Source") || "(no source)", date_raw: get("Date"), duplicate_of: null,
app/frontend/mock.js:89:      const e = { id: "e" + r.seq, seq: r.seq, record_ids: [r.id], date: r.date_iso, date_status: r.date_status, provider: r.source_label, summary, ai_drafted: true,
app/frontend/mock.js:112:        explanation: `Gap of ${days} days between ${ZL.fmtDate(enc[i - 1].date_iso)} (${enc[i - 1].source_label}) and ${ZL.fmtDate(enc[i].date_iso)} (${enc[i].source_label}).`,
app/frontend/timeline.js:69:        el("div", { class: "entry-head" }, el("span", { class: "provider" }, recs.map((r) => `Record ${r.seq}: ${r.source_label}`).join("; ")), el("span", { class: "chip st-rejected" }, "Could not verify")),
app/frontend/timeline.js:73:        el("div", { class: "row-actions" }, recs.map((r) => el("button", { type: "button", class: "btn small", onclick: () => ZL.openSource([{ record_id: r.id, start: null, end: null }], `Record ${r.seq}: ${r.source_label}`) }, `Open record ${r.seq}`))));
app/frontend/source.js:7:    if (!omitHead) box.append(el("h3", {}, label || `Record ${rec.seq}: ${rec.source_label}`));
--- records key in backend
103:        d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
106:                      source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
--- python grounding provider count
{'provider': 56}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:02.951Z

**tool call — Bash**
````
{
 "command": "sed -n 98,110p app/backend/pipeline.py; echo \"...\"; sed -n 362,378p app/backend/pipeline.py; echo \"--- api route shape\"; grep -n \"source_label\\|def case_view\\|def _case_out\\|records\" app/backend/api.py | head -8",
 "description": "Read pipeline record builders and API record shape"
}
````

### User / tool · 2026-11-02T02:06:03.044Z

**tool result**
````
def _store_records(conn, cid: str, ing: dict) -> None:
    if DB.table_counts(conn, cid)["records"]:
        return
    for r in ing["records"]:
        d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
        DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
                      date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
                      source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
                      date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
                      encounter=int(r["encounter"]))


...
    return conn, cid, AU.make_call(conn, cid)


def run_case(text: str, backend: str = None) -> dict:
    """Full pipeline over `text` on a scratch database; returns case_view(). Used by evals; nothing is kept."""
    import contextlib
    import tempfile
    with _Backend(backend), tempfile.TemporaryDirectory() as tmp:
        conn, cid, call = _scratch_call(tmp, IN.normalize_text(text))
        with (P.record_context(text) if P._recording() else contextlib.nullcontext()):
            out = run_pipeline(conn, cid, text, call=call)
        view = case_view(out)
        conn.close()
        return view


def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
--- api route shape
29:BANNER = "Synthetic data only — never paste real records"
164:                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
198:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
281:    @app.post("/api/cases/{token}/records/{rid}/confirm_date")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:04.583Z

**tool call — Bash**
````
{
 "command": "grep -n \"def case_view\" -A 14 app/backend/pipeline.py | head -24; echo \"--- api.py records in GET case\"; sed -n 190,200p app/backend/api.py | cut -c1-260",
 "description": "Read case_view to confirm records key shape"
}
````

### User / tool · 2026-11-02T02:06:04.675Z

**tool result**
````
319:def case_view(out: dict) -> dict:
320-    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
321-    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
322-    flags = []
323-    for f in out["flags"] + out["tray"]:
324-        if "summary" in f:
325-            continue
326-        g = dict(f)
327-        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
328-        if f["type"] == "gap":
329-            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
330-        flags.append(g)
331-    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
332-            "amounts": [{**a, "value_cents": a["cents"], "kind": a["cls"]} for a in out["amounts"] + out["damages"]],
333-            "totals": out["totals"], "flags": flags, "tray": [t for t in out["tray"] if "summary" in t], "warnings": out["warnings"],
--- api.py records in GET case
                flags = DB.list_items(c, cid, "flag")
            except Exception as e:                       # nothing of a failed create stays stored (ADR-006): drop the case row and its parts
                DB.delete_case(c, cid)
                if isinstance(e, ingest.IngestError):
                    raise ApiError(_ERR_STATUS.get(e.code, 400), e.code) from None
                log.error("create failed %s", type(e).__name__)
                raise ApiError(500, "internal", "Something went wrong.") from None
            return {"token": cid, "name": DB.get_case(c, cid)["name"], "status": "ingested", "source": "sample" if sample else "paste",
                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
                    "dates_to_confirm": present.dates_to_confirm(c, cid),
                    "gap_flags": [f["id"] for f in flags if f["type"] == "gap"],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:14.787Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nfrom evals import run as R\nfrom app import pipeline as P\nt = next(t for n,t,_ in R.golden_cases() if n=='sample')\nout = P.run_case(t, 'fixture')\nrecs = {R.rn(r.get('id', r.get('seq'))): r for r in out['records']}\nok = bad = 0\nfor e in out['entries']+out['undated_entries']:\n    first = recs[min(R.rn(r) for r in e['record_ids'])]\n    if R.norm(e['provider']) == R.norm(first['source']): ok += 1\n    else: bad += 1\nprint('provider equals record[source]:', ok, 'not equal:', bad)\nprint('entries+undated:', len(out['entries'])+len(out['undated_entries']))\n\" 2>/dev/null; grep -n \"source_label\" app/backend/*.py | grep -v \"^app/backend/pipeline.py:106\" | head -5",
 "description": "Confirm provider equals record source key, and where source_label is used"
}
````

### User / tool · 2026-11-02T02:06:15.320Z

**tool result**
````
provider equals record[source]: 9 not equal: 0
entries+undated: 9
app/backend/present.py:132:    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
app/backend/store.py:26:        out.append({**d, "n": d["seq"], "source": d["source_label"], "text": block, "excerpt": body,
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:37.650Z

**tool call — Bash**
````
{
 "command": "grep -n 'provider\")' evals/run.py | head -3; grep -n \"if \\\"metrics\\\" in data\" evals/run.py; grep -n 'runs\") == 3' evals/run.py | head -4; grep -n \"code = list\" evals/run.py; grep -n \"def test_\" tests/unit/test_eval_runner.py | wc -l; grep -n 'return {\"records\": out\\[\"records\"\\]' app/backend/pipeline.py; grep -n 'source_label\": r\\[\"source_label\"\\]\\|\"source_label\": r' app/backend/present.py | head -2; grep -n \"def test_each_missed\\|def test_check_spec_recomputes\\|def test_raising_code\\|def test_summary_that\\|def test_case_07_not_run\\|def test_controls_judged\" tests/unit/test_eval_runner.py; sed -n 1,20p tools/board.py | grep -i \"usage\\|validate\" | head -5; grep -n \"argv\\|validate\" tools/board.py | head -12",
 "description": "Get current line numbers for cited code and tests and board usage"
}
````

### User / tool · 2026-11-02T02:06:37.842Z

**tool result**
````
111:        if norm(e.get("provider")) != norm(g["provider"]):
278:            chk(f"entry {e.get('id')} provider", norm(e.get("provider")) == norm(first.get("source_label")))
337:    ents = sorted((tuple(sorted(e.get("record_ids", []))), e.get("date"), e.get("provider"), e.get("state"), tuple(sorted(e.get("reasons") or [])))
615:        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
463:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
464:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3,
312:    code = list(check_summary(item["candidate_summary"], excerpt, label, date)) if check_summary else []   # a crash propagates: no silent code-rung loss
      22
331:    return {"records": out["records"], "entries": out["entries"], "undated_entries": out["undated_entries"],
132:    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
113:def test_each_missed_bar_names_the_failed_bar_and_only_that_bar(bar, mut):
118:def test_controls_judged_unsupported_fail_bar_4_alone():
127:def test_case_07_not_run_fails_bar_4():
142:def test_summary_that_drops_a_qualifier_is_an_entry_miss():
163:def test_raising_code_check_fails_loudly():
175:def test_check_spec_recomputes_the_bar_in_a_full_report(tmp_path, monkeypatch):
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
1145:def main(argv=None) -> int:
1146:    args = build_parser().parse_args(argv)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:39.601Z

**tool call — Bash**
````
{
 "command": "sed -n 896,926p tools/board.py",
 "description": "Read board review-file validator rules"
}
````

### User / tool · 2026-11-02T02:06:39.725Z

**tool result**
````
def validate_review_file(p: Path) -> list[str]:
    errs = []
    if p.name.startswith("GATE-") or p.name.startswith("CONTRACT-"):
        if len(p.read_text(encoding="utf-8").strip()) < 50:
            errs.append("gate summary is empty")
        return errs
    d = review_json(p)
    if d is None:
        return ["review must contain a ```json block (Appendix D.2) with a verdict"]
    for k in ("card", "persona", "verdict", "findings", "exercised"):
        if k not in d:
            errs.append(f"review JSON missing '{k}'")
    if d.get("verdict") not in VERDICTS:
        errs.append(f"verdict must be one of {VERDICTS}")
    if not isinstance(d.get("findings"), list):
        return ["review JSON 'findings' must be a list (use [] for none)"]
    sev = [f.get("severity") for f in d.get("findings", []) if isinstance(f, dict)]
    for f in d.get("findings", []):
        if not isinstance(f, dict) or f.get("severity") not in ("blocker", "major", "minor", "nit"):
            errs.append(f"finding has bad severity: {str(f)[:80]}")
        elif not f.get("evidence"):
            errs.append(f"finding without evidence: {f.get('title')}")
    if "blocker" in sev and d.get("verdict") != "fail":
        errs.append("a blocker finding requires verdict 'fail' (§7.4)")
    elif "major" in sev and "blocker" not in sev and d.get("verdict") != "changes":
        errs.append("a major finding (no blockers) requires verdict 'changes' (§7.4)")
    if not d.get("exercised"):
        errs.append("'exercised' is empty — a review that didn't exercise the artifact is invalid")
    return errs
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:06:50.812Z

**tool call — Bash**
````
{
 "command": "grep -n 'else 2$\\|return 2$' evals/run.py; grep -n \"except ImportError\" evals/run.py; .venv/bin/python tools/board.py validate reviews/T-038-staff-engineer-r2.md 2>&1 | head -3 ; echo \"(pre-write validate above, may show not found)\"",
 "description": "Get exit-code line numbers for the CLI return paths"
}
````

### User / tool · 2026-11-02T02:06:50.966Z

**tool result**
````
625:        return 2
632:    return 0 if report["ship_bar_met"] else 2
577:    except ImportError:
INVALID: reviews/T-038-staff-engineer-r2.md: no such file
(pre-write validate above, may show not found)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:28.777Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-038-staff-engineer-r2.md",
 "content": "# T-038 round 2 review - staff-engineer-reviewer\n\nVerdict: **fail** (one blocker, found while checking round 1). All four round-1 majors are resolved. The blocker is new: the grounding check reads a record key that the eval pipeline does not emit, so bar 1 cannot pass on any run through `evals.run`. Fail-closed, so no false pass, but the ship-bar gate is unusable as built.\n\nScope: HEAD was `5542dfd` at review time. `evals/run.py` last changed in `e771ed3` (T-051). I read the full `evals/run.py`, `tests/unit/test_eval_runner.py`, and `tests/unit/test_eval_spec_check.py`. Nothing else in the repo changed the eval path after `e771ed3`.\n\n## Round-1 majors\n\n| # | Round-1 major | Status | Evidence |\n|---|---|---|---|\n| 1 | ship_bar_met true on 2 runs; `--runs 1` crash | Resolved | `evals/run.py:463-464` require `runs == 3` in bar 4, `:468` adds a blocker for any other count. `--runs 1` and `--runs 2` both give `ship_bar_met=False` with no traceback (repro below). |\n| 2 | `--check-spec` leaves stale `ship_bar_met` | Resolved | `evals/run.py:615-616` recomputes via `evaluate_report` on full reports. Repro: `rc 1`, `ship_bar_met False`, blocker `spec_matches_golden is false`. |\n| 3 | Broad `except` blocks | Resolved | `grep -n \"except Exception\" evals/*.py` printed nothing (rc=1). `judge_item` (`run.py:312`) no longer swallows; a raising `check_summary` propagates (repro below). |\n| 4 | Bar tests weak, 5-6 undetected mutations | Resolved for the listed six | Six scratch mutations, all killed by a named test. One new gap, see minor M9. |\n\nThe round-1 body listed six missed mutations and the brief said five. I ran all six.\n\n## Commands run (quoted)\n\n1. `.venv/bin/python -m pytest tests/unit -q -k eval 2>&1 | tail -2`\n   ```\n   ......................................                                   [100%]\n   38 passed, 725 deselected in 1.92s\n   ```\n   (A first run earlier in the session gave `37 passed`. The T-051 test landed in between.)\n\n2. `.venv/bin/python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$?`\n   ```\n   rc=2\n   ```\n   Visible output: `ship_bar_met=False backend=fixture report=.../evals/reports/20261102T020519Z.md`, blockers `1_grounding`, `3_flags`, `4_no_invented_facts`, `backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)`. Normal exit, no traceback.\n\n3. `grep -n \"except Exception\" evals/*.py`\n   ```\n   (no output)  grep_rc=1\n   ```\n   All `except` clauses in `evals/`: `evals/run.py:577 except ImportError:` and `evals/run.py:623 except CuratedFixtures as e:`.\n\n## Other checks and repros\n\n- Runs gate, in-process with the fake `Perfect` pipeline: `runs=1` and `runs=2` both give `ship_bar_met False`, `determinism_3run status not_measured`, blocker `determinism_3run: runs=N; exactly 3 live runs are required`. No `ZeroDivisionError`.\n- Stale bar, in-process with `check_spec` forced false on a full run-3 report written to a scratch dir: `main(['--check-spec', ...])` returned `1`, `latest.json` has `ship_bar_met False`, `spec_matches_golden False`, last blocker `spec_matches_golden is false`.\n- Raising code rung: `hallucination_metrics(items, controls, judge, check_summary=raising)` raises `RuntimeError: code rung broke`.\n- Curated-set guard (T-051): `LLM_FIXTURE_DIR=<repo>/tests/fixtures/llm/curated python -m evals.run --out <tmp>` prints the refusal and exits `2`, no report.\n- Scratch-copy mutations (copy of HEAD `evals/`, `tests/`, `app/`, `spec/`, `memory/`, `docs/`; `.env` not copied). Each mutation was applied to a copy of `run.py` and the eval suite re-run:\n\n| Id | Mutation | Result |\n|---|---|---|\n| M0 | none (control) | 38 passed |\n| M1 | drop `controls_unsupported` term from bar 4 | 1 failed: `test_controls_judged_unsupported_fail_bar_4_alone` |\n| M2 | drop `case_07_total_420` term from bar 4 | 2 failed: `test_each_missed_bar...[4_no_invented_facts-...]`, `test_case_07_not_run_fails_bar_4` |\n| M3 | case_07 `not_run` returns value True | 1 failed: `test_case_07_not_run_fails_bar_4` |\n| M4 | `1_grounding` forced True | 1 failed: `test_each_missed_bar...[1_grounding-...]` |\n| M5 | record-warning check disabled | 1 failed: `test_missing_record_warning_counts_as_a_must_not_hit` |\n| M6 | SUMMARY_DROPS_QUALIFIER check disabled | 1 failed: `test_summary_that_drops_a_qualifier_is_an_entry_miss` |\n| M7 | check-spec recompute removed | 1 failed: `test_check_spec_recomputes_the_bar_in_a_full_report` |\n| M8 | broad `except Exception` reintroduced in `judge_item` | 1 failed: `test_raising_code_check_fails_loudly` |\n| M9 | determinism `runs == 3` term removed from bar 4 | 38 passed (survives; see minor M9) |\n\n- Grounding key mismatch (blocker, reproduced): the harness reads `source_label` from each record (`evals/run.py:278`). `run_case` returns the ingest shape. Verbatim keys of `run_case(sample,'fixture')['records'][0]`: `['char_end', 'char_start', 'date_candidates', 'date_iso', 'date_raw', 'date_status', 'duplicate_of', 'encounter', 'excerpt', 'id', 'injection_hits', 'injection_tag', 'kind', 'n', 'seq', 'source', 'text', 'unsplit']`. No `source_label`. For the 9 sample entries, `provider == record['source']` holds in 9 of 9. Across all golden cases `grounding()` reports 56 failures, all `entry eN provider`. `grounding_rate` = 183/239 = 0.766, so bar 1 is false on fixture. The same key mismatch is backend-independent, so bar 1 is false on a live run too.\n- Fixture run logs 41 `llm call failed ... step=j1 attempt=1 prompt_hash=...` warnings per run (`app/llm/audited.py:87`). Visible, not swallowed. Out of this card's scope; see the question below.\n\n## Findings\n\nBlocker: the grounding check compares against a key the eval pipeline does not produce, so bar 1 cannot pass through `evals.run`. Fail-closed (no false pass), but the ship-bar gate is unusable until fixed. Per the calibration (makes the must-have unusable), this is a blocker.\n\nMinor M9: bar 4 requires `determinism_3run.runs == 3` but no test asserts the bar on that term alone. A tampered report with `determinism_3run {value 1.0, runs 2}` gives `bars[\"4_no_invented_facts\"]=False` today, but if the term is removed, the bar shows True while the blockers still say \"not measured\". Add the tampered-report test.\n\nMinor: the CLI exits `2` both for a refused curated run (`evals/run.py:625`) and for ship-bar-not-met (`run.py:632`). A caller cannot tell them apart.\n\nNit: `evals/run.py:577` `except ImportError` fallback. `app/pipeline.py` is a 6-line re-export of `app.backend.pipeline` (verified `app/pipeline.py:2`), so both branches load the same module. The try/except adds nothing.\n\nSide effect, for transparency: the brief's commands and my extra `--runs 2` run wrote timestamped reports and overwrote `evals/reports/latest.json` in the untracked `evals/reports/` directory.\n\n```json\n{\"card\": \"T-038\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git HEAD 5542dfd at review time; evals/run.py (last changed e771ed3, T-051); tests/unit/test_eval_runner.py; tests/unit/test_eval_spec_check.py; app/backend/pipeline.py case_view (read only); fixture backend, golden sample and all golden cases via run_case; no app URL exercised (eval CLI only)\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-038-staff-engineer.md, memory index\",\n  \"read evals/run.py in full (615 lines at HEAD), tests/unit/test_eval_runner.py in full, tests/unit/test_eval_spec_check.py in full\",\n  \"pytest tests/unit -q -k eval | tail -2 -> '38 passed, 725 deselected in 1.92s'\",\n  \"python -m evals.run --runs 1 >/dev/null 2>&1; echo rc=$? -> rc=2 (fixture; blockers 1_grounding, 3_flags, 4_no_invented_facts, backend=fixture)\",\n  \"grep -n 'except Exception' evals/*.py -> no output, rc=1; all except clauses in evals/ listed (run.py:577, run.py:623)\",\n  \"in-process runs=1 and runs=2 with fake Perfect pipeline: ship_bar_met False, no ZeroDivisionError\",\n  \"in-process --check-spec with check_spec forced false over a full run-3 report in a scratch dir: rc 1, ship_bar_met False, blocker spec_matches_golden is false\",\n  \"in-process hallucination_metrics with raising check_summary: RuntimeError propagates\",\n  \"LLM_FIXTURE_DIR=curated python -m evals.run --out <tmp>: rc 2 with refusal message, no report\",\n  \"git log / git show e771ed3 (T-051 diff) read in full\",\n  \"run_case(sample,'fixture') record keys printed; provider == record['source'] 9/9; grounding() failures 56, all provider; grounding_rate 183/239\",\n  \"scratch copy of HEAD evals/, tests/, app/, spec/, memory/, docs/ (no .env); 10 mutations M0-M9 applied to a copy of run.py, eval suite re-run each time, copy restored and diffed identical\",\n  \"grep 'llm call failed' on fixture runs: 41 warnings in one run (app/llm/audited.py:87)\"],\n \"verdict\": \"fail\",\n \"scores\": {\"determinism_and_code_vs_llm_split\": 4, \"failure_visibility\": 4, \"test_strength\": 3, \"spec_conformance\": 2, \"ship_bar_integrity\": 3},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Grounding provider check reads a key run_case never emits; bar 1 cannot pass through evals.run\",\n   \"evidence\": \"evals/run.py:278 chk(... norm(e.get('provider')) == norm(first.get('source_label'))); app/backend/pipeline.py:331 case_view returns out['records'] unchanged; run_case records keys (verbatim) ['char_end','char_start','date_candidates','date_iso','date_raw','date_status','duplicate_of','encounter','excerpt','id','injection_hits','injection_tag','kind','n','seq','source','text','unsplit'] (no source_label); provider == record['source'] in 9/9 sample entries; grounding() failures = 56, all 'entry eN provider' across golden cases; grounding_rate 183/239 = 0.766 so bar 1 fails. Contract memory/contracts/api.md:54 and app/backend/present.py:132 use source_label.\",\n   \"why_it_matters\": \"The eval gate and the HTTP API emit different record shapes. Every correct entry is reported as a grounding failure, so bar 1 is false on fixture and on any live run through run_case. Fail-closed, so no false pass, but the ship-bar must-have cannot be met and the reported 0.766 misstates the pipeline. Test doubles hid it: test_eval_runner.py:45 Perfect.run_case builds records with source_label, so the fake never exercises the real key set.\",\n   \"fix\": \"Make case_view emit the documented record shape (source_label, seq, id, date_iso, date_status) and have grounding() read that documented key; or have one shared record mapper used by both the HTTP view and run_case. Replace the Perfect record shape with the one run_case actually produces.\",\n   \"acceptance_test\": \"grounding(SAMPLE, P.run_case(SAMPLE,'fixture'))['failures'] contains no 'provider' entries; case_view records include source_label equal to the record header; python -m evals.run --runs 1 report has metrics.grounding_rate.failures == [].\"},\n  {\"severity\": \"minor\", \"title\": \"Bar 4 determinism runs==3 term has no bar-level test (M9 survives)\",\n   \"evidence\": \"evals/run.py:464 `and m['determinism_3run'].get('runs') == 3`; scratch mutation removing that term: 38 passed. Tampered report {determinism_3run: value 1.0, runs 2} gives blockers naming determinism but bars['4_no_invented_facts'] True when the term is removed.\",\n   \"why_it_matters\": \"bars and blockers can disagree in latest.json, which T-045 reads. Current code is correct, but nothing proves the bar itself carries the run-count rule.\",\n   \"fix\": \"Add a test that evaluate_report on a tampered runs-2 value-1.0 report gives bars['4_no_invented_facts'] False and ship_bar_met False.\",\n   \"acceptance_test\": \"M9 mutation makes the new test fail.\"},\n  {\"severity\": \"minor\", \"title\": \"CLI exit code 2 used for both refused curated run and bar-not-met\",\n   \"evidence\": \"evals/run.py:625 `return 2` (curated refusal); evals/run.py:632 `return 0 if report['ship_bar_met'] else 2`. Both return 2.\",\n   \"why_it_matters\": \"A CI caller cannot tell a refused run (configuration error) from a measured bar miss.\",\n   \"fix\": \"Return a distinct code for the curated refusal (for example 3) and document both codes in the module docstring.\",\n   \"acceptance_test\": \"test asserts refused-curated exit code differs from the bar-miss exit code.\"},\n  {\"severity\": \"nit\", \"title\": \"try/except ImportError fallback in load_pipeline adds nothing\",\n   \"evidence\": \"evals/run.py:575-578 try: from app import pipeline / except ImportError: from app.backend import pipeline; app/pipeline.py:2 is `from app.backend.pipeline import *`.\",\n   \"why_it_matters\": \"Both branches load the same implementation, so the fallback is dead weight and can mask a broken import path in a later edit.\",\n   \"fix\": \"Import app.backend.pipeline directly, or keep one import with no except.\",\n   \"acceptance_test\": \"none required beyond the existing eval suite.\"}\n ],\n \"whats_right\": [\n  \"All four round-1 majors are resolved in code and tests: runs gate at evals/run.py:463-468, check-spec recompute at run.py:615, judge_item propagates at run.py:312, zero 'except Exception' in evals/.\",\n  \"Each of the six round-1 missed mutations (M1-M6) is now killed by a named test; M7 and M8 are killed too.\",\n  \"The curated-set guard (T-051) refuses full runs with exit 2 and writes no report, verified by running it.\"],\n \"questions_for_chris\": [\n  \"The fixture run logs 41 FixtureMiss warnings for step j1 (app/llm/audited.py:87). Is the recorded fixture set meant to cover j1 for the golden cases? If not, fixture-backed hallucination numbers are not representative.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T02:07:28.924Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-038-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:30.630Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py validate reviews/T-038-staff-engineer-r2.md 2>&1 | tail -5; echo \"rc=${PIPESTATUS[0]}\"",
 "description": "Validate the review file with the board validator"
}
````

### User / tool · 2026-11-02T02:07:30.751Z

**tool result**
````
ok (1 file(s))
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:38.223Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_eval_runner_review_patterns.md",
 "content": "---\nname: eval-runner-review-patterns\ndescription: T-038 r1-r2 eval runner (evals/run.py) review patterns: test doubles hiding real key shapes, bar-level mutation coverage, scratch-copy mutation method for eval tests\nmetadata:\n  type: project\n---\n\nEval runner (`evals/run.py`, ship bar, check-spec, check-fresh) reviews, T-038 r1 (commit 40c882d) and r2 (HEAD 5542dfd).\n\n- **Fake pipeline shape can hide a real key mismatch.** `tests/unit/test_eval_runner.py` `Perfect.run_case` builds records with `source_label`, but the real `app/backend/pipeline.py` `case_view` (line ~331) returns the ingest records with `source`. The grounding check (`evals/run.py:278`) compares against `source_label`, so every entry fails on the real pipeline (56/56 provider failures on fixture). Fail-closed, but bar 1 can never pass. Lesson: when a test double stands in for a pipeline, diff its output keys against `run_case`'s real keys (print `sorted(out['records'][0])`).\n  **Why:** the fake and the test both passed; only a real run exposed it.\n  **How to apply:** for any eval or contract test double, add one test that runs the real `run_case` on the sample and asserts the harness's own checks give no failures.\n\n- **Bar-level mutations are the right kill test.** T-038 r1 had per-bar assertions missing; r2 added `bars[name] is False` tests and all six listed mutations die. Still open: a removed `runs == 3` term in bar 4 survives because the blocker list catches it (bars and blockers can disagree).\n  **How to apply:** after any bar or gate change, mutate each bar term and require a test that asserts that bar, not just `ship_bar_met`.\n\n- **Method (scratch copy):** copy `app/ evals/ tests/ spec/ docs/ memory/` into the scratchpad (not `.env`; `memory/contracts/api.md` is read by tests, so `memory/` must be included). For each mutation, assert the target string occurs exactly once, write the mutated `run.py`, run `pytest tests/unit -q -k eval`, then restore and diff against the repo file.\n\n- **Repo moves during review.** HEAD advanced twice mid-review (T-051 guard, then other commits) and the eval test count changed 37 to 38. Re-sync the scratch copy from HEAD before mutation runs and quote the HEAD sha.\n\n- **The eval CLI writes into `evals/reports/`** (untracked, overwrites `latest.json`). Say so in the review when running the brief's commands.\n\n- Model discrepancy: the dossier expects `claude-sonnet-5-5`, but the environment runs as `claude-haiku-5-5`. The review record uses what I actually run as.\n\nSee also [[project_wiring_review_patterns]] (grep callers, run the producer) and [[project_llm_stage_review_patterns]] (shared fixtures, pin HEAD by sha).\n"
}
````

### User / tool · 2026-11-02T02:07:38.316Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_eval_runner_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:40.241Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E",
 "new_string": "- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E\n- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r2: fake pipeline hides real record keys, bar-level mutations, scratch-copy method"
}
````

### User / tool · 2026-11-02T02:07:40.345Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:07:41.885Z

T-038 r2 verdict is fail: all four round-1 majors are resolved, but a new blocker (grounding reads `source_label`, which `run_case` never emits, so bar 1 cannot pass) is recorded in `/Users/arsis/zlayt-pm-project/reviews/T-038-staff-engineer-r2.md` (validator ok, model claude-haiku-5-5).
