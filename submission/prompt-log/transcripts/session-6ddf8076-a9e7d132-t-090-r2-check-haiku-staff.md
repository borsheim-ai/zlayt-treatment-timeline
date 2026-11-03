# Subagent: T-090 r2 check (haiku staff) (T-090 r2 check (haiku staff))

Source: `agent-a9e7d1321020f0ad0.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:31:46.710Z

Round-2 check of board card T-090 in /Users/arsis/zlayt-pm-project (commits 823b718 and 02ff244). Using reviews/T-090-staff-engineer.md, confirm:
- evals/reports/calibration.json reproduces exactly from its recorded source commit: regenerate it yourself from `git worktree add <scratchpad>/wt 823b718` and compare, ignoring generated_at, then remove the worktree;
- the header records the commit, a clean tree, the backend and the prompt hashes;
- the tests fail if the file is hand-edited;
- the majors are fixed;
- AC 1 is narrowed to the eval side, with the UI under T-096.

Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Write reviews/T-090-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:48.171Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:31:48.179Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:48.402Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:31:48.409Z

**tool result**
````
1	---
2	name: t090-calibration-review-patterns
3	description: T-090 r1 d0aee83 calibrated-confidence review: committed artifact not reproducible from its commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive, fixture-miss log noise from score_unsplit
4	metadata:
5	  type: project
6	---
7	
8	T-090 r1 (commit d0aee83, calibrated confidence as N/M counts, D-042) written to reviews/T-090-staff-engineer.md: fail, 1 blocker, 3 majors, 4 minors, 1 nit.
9	
10	- **Committed artifact must be regenerated, not trusted.** evals/reports/calibration.json said 82/83 and 11/13, but `git archive d0aee83` + `evals.run --out` (fixture) gives 83/84 and 10/10 twice, and HEAD ec33bf0 gives the same. No `*T041847Z.md` report existed for its generated_at. Method: pin with git archive, regenerate with --out, diff counts ignoring generated_at, then hand-check two cells from a dump of the raw items.
11	- **Hand-check cells from raw items, not from the counters.** A dump script (run.py's golden_cases + pipeline.run_case, fixture) lets you tally verified amounts (9/9) and needs-review flags (2/2) by reading golden against live. Found the file's flag cell (3/5) unreproducible.
12	- **"llm call failed ... FIXTURE_MISS" lines on the eval CLI come from score_unsplit**, not from the golden cases (checked: score_unsplit alone prints 7). Do not read them as calibration misses.
13	- **Working tree evals/run.py was modified mid-review (uncommitted).** Working-tree counts (84/85, 9/9) differ from the commit's. Use archives for every count you cite.
14	- **Mutants that survive a green suite here:** dropping the class term in amount matching (test gap; golden counts identical, so the rate-vs-charge blind spot is real), dropping the tolerated term, lowering CAL_SMALL_N to 5 (the boundary test uses 30 names, never 29), and dropping the record_warning filter before zip (positional alignment, untested).
15	- **AC closed with an unbuilt clause.** Card AC 1 said "UI shows ..." and was done:true with "UI line pending frontend". Check for any route/UI reference (grep app/) before accepting an AC that names the UI.
16	- **Sentence without provenance.** The generated sentence the UI would show verbatim named N/M and a case count, not the backend. A fixture replay read as live precision. Check the rendered sentence, not only the file's top-level fields.
17	
18	**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.
19	
20	Related: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps).
21	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:48.607Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:31:48.614Z

**tool result**
````
1	# T-090 review: calibrated confidence as measured counts (D-042, scope cut 10)
2	
3	**Verdict: fail.** One blocker: the committed `evals/reports/calibration.json` does not come from the code that committed it. Three majors, four minors, one nit.
4	
5	Scope: commit d0aee83 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/calibration.json). Line numbers below are at d0aee83, pinned with `git archive` into `artifacts/review-evidence/T-090-staff/base/`. HEAD moved to ec33bf0 during the review; the archive of ec33bf0 gives the same counts, so the finding stands at HEAD too. The working-tree `evals/run.py` is modified by an uncommitted change, so working-tree numbers are not used as evidence. No app URL exists for this card: there is no calibration route or UI yet (`grep -rln calibration app/` returns nothing).
6	
7	## What reproduces and what does not
8	
9	| Source | verified | needs_review | Amount / flag cells |
10	|---|---|---|---|
11	| Committed `evals/reports/calibration.json` (card AC 1 cites it) | 82/83 | 11/13 | flags needs_review 3/5, flags verified 19/19 |
12	| Regenerated at d0aee83, run 1 and run 2 (`evals.run --out`, fixture) | 83/84 | 10/10 | flags needs_review 2/2, flags verified 20/20 |
13	| Regenerated at ec33bf0 (HEAD at write time) | 83/84 | 10/10 | same as above |
14	| Working tree (uncommitted evals/run.py and app changes) | 84/85 | 9/9 | not evidence for this commit |
15	
16	Runs 1 and 2 at d0aee83 differ only in `generated_at` (`artifacts/review-evidence/T-090-staff/regen-1`, `regen-2`). The committed file's `generated_at` is 2026-11-02T04:18:47Z; no `evals/reports/*0418*.md` exists, and `evals/reports/latest.json` (04:09:33Z) has no `calibration` key.
17	
18	Hand recompute from the raw fixture outputs (`artifacts/review-evidence/T-090-staff/dump-items-pinned.txt`, golden expectations beside each live item):
19	- Verified amounts, 9/9: sample r2 $6,240 and r8 $2,150 (charge, 624000 and 215000 cents), case_01 r1 $310.00, case_03 r3 $95.00 and r5 $240, case_05 r2 $4,380, case_07 r1 $420, case_08 r2 $1,875, case_09 r2 $275. Each matches a golden amount on record, raw text, class and value. Agrees with the file.
20	- Needs-review flags, 2/2: case_06 conflict (r1 and r2, cite C1) and case_07 gap 2026-03-16 to 2026-05-04, 49 days (cite G1). The file says 3/5. The dump has no sample needs-review flag and only one case_06 needs-review flag. Disagrees with the file.
21	
22	## Other checks
23	
24	- Percent: zero `%` or `percent` in the calibration code (evals/run.py:228-317 and the render function), in `calibration.json`, or in the rendered `## Calibrated confidence` section of the regenerated report. Passes.
25	- Backend and sample size: the file states `backend: fixture`, `case_count: 10`, `small_sample: true`. The sentences do not name the backend (see finding 4).
26	- Mutation: 13 mutants of the matching and pooling logic in a scratch copy of d0aee83 (`artifacts/review-evidence/T-090-staff/mutate_calibration.py`, results in `mutation-results.txt`). 9 killed, 4 survived (M2, M3, M9, M13).
27	- Tests: `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` gives 71 passed in the working tree and 71 passed in the d0aee83 archive. The card says 126 eval tests pass; the brief's selector does not reproduce that number.
28	
29	## Findings
30	
31	Each finding has its evidence in the JSON block. The blocker is the reason for the verdict.
32	
33	1. **blocker**: committed calibration.json cannot be reproduced and has no traceable run (see table above).
34	2. **major**: AC 1 is marked done while its UI clause is unbuilt (card line 18).
35	3. **major**: the amount class check is not exercised; mutant M2 survives on tests and on the golden set.
36	4. **major**: the rendered sentence names no backend and no golden-set provenance.
37	5. **minor**: small-sample threshold boundary at 29 is untested; M9 survives.
38	6. **minor**: tolerated-flag and record_warning alignment mutants (M3, M13) survive.
39	7. **minor**: items are dropped from the denominator silently (stateless items, duplicate candidates, extraction failures).
40	8. **minor**: calibration.json is not in the freshness check, and it embeds a wall-clock timestamp.
41	9. **nit**: card says "6 new tests" and the diff adds 7.
42	
43	## What is right
44	
45	- Counts regenerate deterministically at a fixed tree; only `generated_at` moves.
46	- No percentage is rendered anywhere in this change; sentences are generated in code with N/M and a caveat.
47	- The matching reuses the existing golden rules (entry_found, amount raw/class/value, flag one-to-one), and hand-checked amount cells agree; 9 of 13 mutants die, including the denominator, pooling, percent and state-guard mutants.
48	
49	## Outside my lens
50	
51	The same fixture run reports `ship_bar_met=False` (blockers: 4_no_invented_facts, determinism and judge controls not measured). That is the existing ship bar, not T-090.
52	
53	```json
54	{"card": "T-090", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
55	 "scope": "commit d0aee83 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/calibration.json), pinned by git archive to artifacts/review-evidence/T-090-staff/base; HEAD moved to ec33bf0 mid-review (same counts there); working-tree evals/run.py is uncommitted-modified and not used; sample case = fixture backend over the 10 golden cases (sample, case_01..case_09); no app URL (no calibration route or UI exists)",
56	 "exercised": [
57	  "read personas/staff-engineer.md, board/cards/T-090.md, memory/ORCHESTRATOR_DECISIONS.md D-042, memory/SCOPE_CUTS.md row 10",
58	  "git show d0aee83 --stat; git show d0aee83 -- evals/run.py; git show d0aee83 -- tests/unit/test_eval_runner.py",
59	  "git archive d0aee83 (app evals tests spec docs memory tools) into artifacts/review-evidence/T-090-staff/base; cmp: archive calibration.json identical to committed file",
60	  ".venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' in the working tree: 71 passed, 1102 deselected; same in the d0aee83 archive: 71 passed, 1046 deselected",
61	  "archive d0aee83: .venv/bin/python -m evals.run --out .../regen-1 and --out .../regen-2 (fixture, no --backend): identical except generated_at (diff line 213); both give verified 83/84, needs_review 10/10; diff against committed calibration.json shows different counts",
62	  "working tree: evals.run --out .../regen-wt: verified 84/85, needs_review 9/9; archive ec33bf0 (HEAD): regen-head: verified 83/84, needs_review 10/10",
63	  "dump_items.py (pinned, fixture, all 10 cases) to dump-items-pinned.txt; hand recompute of verified amounts (9/9, agrees) and needs_review flags (2/2, committed says 3/5, disagrees); verified flags 20/20 by the same dump (committed says 19/19)",
64	  "mutate_calibration.py: 13 scratch mutants on the d0aee83 copy, each run with the calibration and eval_runner selector: 9 killed, 4 survived (M2, M3, M9, M13); mutant counts regenerated for M2 and M13 (regen-mut-M2, regen-mut-M13) are identical to base",
65	  "grep for percent signs in evals/run.py calibration code, calibration.json, and the rendered calibration section of regen-pinned-b: 0 hits; grep -rln calibration app/: no hits",
66	  "ls evals/reports/*0418*: none; evals/reports/latest.json generated_at 2026-11-02T04:09:33Z, no calibration key",
67	  "git show d0aee83 -- tests/unit/test_eval_runner.py | grep -c '^+def test_': 7 new tests"
68	 ],
69	 "verdict": "fail",
70	 "scores": {"counts_reproduce_from_commit": 1, "hand_recompute_agrees": 2, "provenance_traceable": 1, "no_bare_percent": 5,
71	            "regeneration_deterministic": 4, "backend_and_sample_stated": 3, "mutants_killed": 3, "ac_closed_honestly": 2},
72	 "findings": [
73	  {"severity": "blocker",
74	   "title": "Committed calibration.json does not reproduce from the commit and has no traceable run",
75	   "evidence": "evals/reports/calibration.json:28-29 shows matched 82 total 83 (verified) and :12-13 shows matched 11 total 13 (needs_review); :240-241 carries the same sentences. Regenerating at d0aee83 with .venv/bin/python -m evals.run --out <dir> (fixture) gives verified 83/84 and needs_review 10/10, identical across two runs (artifacts/review-evidence/T-090-staff/regen-1 and regen-2; only line 213 generated_at differs). Regenerating at HEAD ec33bf0 gives the same (regen-head). Flag cells also differ: committed needs_review 3/5 at :165-166 and verified 19/19 at :199-200, regenerated 2/2 and 20/20. Provenance: committed generated_at 2026-11-02T04:18:47Z (:217) has no matching evals/reports/20261102T041847Z.md, and evals/reports/latest.json (04:09:33Z) has no calibration key.",
76	   "why_it_matters": "The served file is the number a paralegal will read ('matched the record 82/83 times in testing'). No run of the committed code produces it, so it is not measured from evals as D-042 requires, and the next reviewer cannot reproduce the card's evidence. A figure that cannot be traced to a run is an invented number even if the code is right.",
77	   "fix": "Regenerate calibration.json with a full python -m evals.run at the commit being shipped (fixture backend) and commit it with its report .md and latest.json in the same commit. Do not hand-place or copy the file. Update the card evidence to the regenerated counts (83/84 and 10/10 at d0aee83).",
78	   "acceptance_test": "At the shipped commit: python -m evals.run --out <tmp> then compare <tmp>/calibration.json with evals/reports/calibration.json ignoring generated_at (must be equal); and a unit test that builds calibration over the golden cases with the fixture backend and asserts by_state and by_type equal the committed file's values."},
79	  {"severity": "major",
80	   "title": "AC 1 is marked done while its UI clause is unbuilt",
81	   "evidence": "board/cards/T-090.md:18 has the AC text \"UI shows 'Verified items matched the record N/M times in testing' instead of a %\" with \"done\": true; the same line's evidence ends \"UI line pending frontend (note)\". grep -rln calibration app/ returns no files at d0aee83 or the working tree, so no endpoint serves calibration.json and no UI renders sentences.overall.",
82	   "why_it_matters": "A clause of the AC is not met and the AC is closed anyway. The D-042 requirement is that the displayed statement shows measured counts; the displayed statement does not exist yet, so the card's done state overstates what shipped.",
83	   "fix": "Set AC 1 to done: false, or split it: AC 1a (eval counts, done) and AC 1b (served read-only calibration field and UI line rendered verbatim, no percent), with 1b linked to the frontend and backend cards that will build it.",
84	   "acceptance_test": "board.py show T-090 shows AC 1b open until a running app returns the calibration sentence (curl the route) and the rendered UI text contains it verbatim with no percent sign."},
85	  {"severity": "major",
86	   "title": "Amount matching ignores class in no test; mutant survives and golden counts do not change",
87	   "evidence": "evals/run.py:253 `and a.get(\"kind\") == g[\"class\"] and a.get(\"value_cents\") == cents):` (d0aee83). Mutant M2 removes the class term: SURVIVED, 71 passed (artifacts/review-evidence/T-090-staff/mutation-results.txt, line for M2). Golden counts under M2 are identical to base (regen-mut-M2/calibration.json).",
88	   "why_it_matters": "The amount rule is the only place the calibration separates a rate from a charge. If a rate were classified as a charge with the same text and value, the calibrated amount precision would still count it as matched. That inflates the measured number in the exact area the spec treats as a blocker ($185 rate must never be totalled as a charge).",
89	   "fix": "Keep the class term and add a unit test in tests/unit/test_eval_runner.py: in the sample, change the kind of one verified amount (for example $6,240 charge to rate) and assert that the verified amount count falls from 2/2 to 1/2 for the sample.",
90	   "acceptance_test": "The new test fails under mutant M2 (remove the class term at evals/run.py:253) and passes at d0aee83."},
91	  {"severity": "major",
92	   "title": "The sentence the UI will render verbatim names no backend and no provenance",
93	   "evidence": "evals/run.py:300 builds sentences.overall from 'Verified items matched the record {m}/{t} times in testing' plus caveat; the string has no backend. evals/reports/calibration.json:241 reads \"Verified items matched the record 82/83 times in testing (small sample: 10 cases).\" The backend 'fixture' appears only in the top-level field (:2) and the report heading. The card note (board/cards/T-090.md:26) asks the frontend to show the backend beside the sentence, which no test enforces.",
94	   "why_it_matters": "The fixture backend replays recorded replies on the 10 golden cases; it is not live model output. A reader of 'matched the record 82/83 times in testing' will take it as live precision. The file says fixture; the statement a paralegal reads does not. D-042 requires the shown statement to be exactly what was measured.",
95	   "fix": "Put the backend and the golden-set basis into the sentence, for example 'Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases).' Build it in build_calibration so the UI cannot drop it.",
96	   "acceptance_test": "A unit test asserts each sentence in sentences.overall contains the backend name (build_calibration(res, 'fixture') contains 'fixture'; build_calibration(res, 'claude-cli') contains 'claude-cli')."},
97	  {"severity": "minor",
98	   "title": "Small-sample threshold boundary at 29 cases is not tested; lowering CAL_SMALL_N to 5 survives",
99	   "evidence": "evals/run.py:231 `CAL_SMALL_N = 30`. Mutant M9 (CAL_SMALL_N = 5): SURVIVED, 71 passed. tests/unit/test_eval_runner.py:519 builds range(29) plus 'few' = 30 cases, so the test only checks the 30-case side.",
100	   "why_it_matters": "The caveat is the guard that keeps a 3-of-3 result from reading as a rate. The threshold is a code choice, not a spec number, and nothing pins it at 29 versus 30.",
101	   "fix": "Add the 29-case assertion beside the 30-case one: at 29 cases the overall sentence carries 'small sample'; at 30 it does not.",
102	   "acceptance_test": "The new 29-case test fails under M9 (CAL_SMALL_N = 5) and under a raised threshold of 31 (the 30-case assertion already covers that)."},
103	  {"severity": "minor",
104	   "title": "Tolerated-flag and record_warning alignment mutants survive",
105	   "evidence": "evals/run.py:264 `add(\"flag\", c[\"_state\"], i in owned or any(tolerated_match(...)))`: mutant M3 drops the tolerated term and SURVIVES. evals/run.py:257 filters record_warning out of flags, and zip(cands, flags) at evals/run.py:259 pairs them by position; mutant M13 drops the filter and SURVIVES. Golden counts under M13 are identical to base (regen-mut-M13).",
106	   "why_it_matters": "A tolerated (documented allowed) candidate would count as wrong, understating precision. A record_warning in the flags list would shift every later flag's state by one position, silently assigning needs_review where verified belongs. Neither is covered, and the golden numbers would not show it.",
107	   "fix": "Add a test with one tolerated candidate (expect it counted as matched) and one case with a record_warning placed before a flag (expect the states to stay aligned). Prefer matching by candidate identity over zip position.",
108	   "acceptance_test": "M3 and M13 each turn at least one test red."},
109	  {"severity": "minor",
110	   "title": "Items are dropped from the denominator silently",
111	   "evidence": "evals/run.py:242 `if state in CAL_STATES:` drops items with a missing or other state; tests/unit/test_eval_runner.py:459 asserts that exclusion as intended. evals/matching.py:37-42 (assign_detail) keeps the first of duplicate candidates and drops later ones, so a duplicate's state never counts. app/backend/generator.py:51 returns {'failure': 'FIXTURE_MISS'} for a record with no extraction, so that record never becomes an item and never reaches M.",
112	   "why_it_matters": "The sentence reads as the share of produced items that were right; it does not say how many produced items were not scored, or that records with no output are outside the count. Precision of produced items is the stated D-042 measure, so this is a disclosure gap rather than a wrong number, but it hides output-schema bugs (a missing state looks like 'not an item').",
113	   "fix": "Count the excluded items per cell and print them beside the sentence ('N items not scored'); or state in the sentence that the count covers produced items only.",
114	   "acceptance_test": "A build_calibration test with one stateless item reports 'not scored: 1' beside the sentence; the sentence no longer reads as complete."},
115	  {"severity": "minor",
116	   "title": "calibration.json is outside the freshness check and embeds a wall-clock timestamp",
117	   "evidence": "evals/reports/calibration.json:217 \"generated_at\" wall-clock value; two regenerations at the same tree differ in that one line (artifacts/review-evidence/T-090-staff/regen-1 vs regen-2). evals/run.py:71-80 hashes() covers only app/llm/prompts/*.md and app/llm/lexicon.yaml, so check_fresh (evals/run.py:915) cannot see a stale calibration.json.",
118	   "why_it_matters": "This is how finding 1 went unnoticed: the served file can drift from latest.json with nothing to flag it. Counts are deterministic, which is good; the file is not checked.",
119	   "fix": "Add the calibration.json hash to the check-fresh comparison, and either drop generated_at from the served file or exclude it from the hash.",
120	   "acceptance_test": "Edit one count in evals/reports/calibration.json, then python -m evals.run --check-fresh exits 1."},
121	  {"severity": "nit",
122	   "title": "Card claims 6 new tests; the diff adds 7; the selector result differs from the card's 126",
123	   "evidence": "board/cards/T-090.md:18 says 'tests/unit/test_eval_runner.py 6 new tests'. git show d0aee83 -- tests/unit/test_eval_runner.py | grep -c '^+def test_' returns 7 (tests/unit/test_eval_runner.py:444, 459, 469, 480, 494, 515, 524). The brief's selector gives 71 passed, not 126.",
124	   "why_it_matters": "The card note is the only record of what was verified; small count errors reduce trust in the handoff.",
125	   "fix": "Correct the count in the card note and name the selector used for the 126 figure, or drop it.",
126	   "acceptance_test": "Card note matches the diff and the selector."}
127	 ],
128	 "whats_right": [
129	  "Counts regenerate deterministically at a fixed tree: two pinned runs differ only in generated_at.",
130	  "No percent sign is produced anywhere in the calibration code, calibration.json, or the rendered section; sentences are built in code with N/M and a caveat.",
131	  "Matching reuses the existing golden rules; the hand-checked amount cells agree (9/9 verified, 6/6 needs_review), and 9 of 13 scratch mutants die."
132	 ],
133	 "questions_for_chris": [
134	  "Is fixture-replay precision (recorded replies on the golden cases) an acceptable basis for the D-042 statement, or should the statement wait for a live-backend run before it is shown?"
135	 ]}
136	```
137	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:49.050Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && git status --short | head -40 && ls evals/reports/ && ls reviews/ | grep T-090",
 "description": "Show recent commits, working tree status, and T-090 review files"
}
````

### User / tool · 2026-11-02T04:31:49.192Z

**tool result**
````
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
823b718 feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
e92b6ed feat(frontend): Run the second check again button, refused export shown beside Export, pending items as a gate warning (T-081 r3, T-082 r3, D-044, D-045)
17cc9c7 feat(backend): speaker attribution v2 behind adversarial eval gate, disabled (T-091)
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
f218263 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/confidence.py
 M app/backend/date_convention.py
 M app/backend/dates.py
 M app/backend/export.py
 M app/backend/flags.py
 M app/backend/generator.py
 M app/backend/judges.py
 M app/backend/narrative.py
D  app/backend/pdf_checks.py
D  app/backend/pdf_hidden.py
D  app/backend/pdf_ocr.py
D  app/backend/pdf_routes.py
MM app/backend/pdf_text.py
MM app/backend/pipeline.py
MM app/backend/present.py
M  app/backend/reclassify.py
MM app/backend/rejudge.py
 M app/backend/review.py
 M app/backend/sentences.py
 M app/backend/store.py
MM app/backend/trace.py
MM app/backend/why.py
M  app/db/db.py
M  app/db/schema.sql
 M app/llm/audited.py
20261102T020824Z.md
20261102T020933Z.md
20261102T021029Z.md
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T023155Z.md
20261102T023203Z.md
20261102T023204Z.md
20261102T023208Z.md
20261102T023603Z.md
20261102T023911Z.md
20261102T023916Z.md
20261102T024348Z.md
20261102T024355Z.md
20261102T024653Z.md
20261102T024822Z.md
20261102T025055Z.md
20261102T025219Z.md
20261102T025526Z.md
20261102T025715Z.md
20261102T030405Z.md
20261102T031209Z.md
20261102T032024Z.md
20261102T032823Z.md
20261102T035750Z.md
20261102T040933Z.md
calibration.json
controls-20261102T042306Z.json
controls-20261102T042306Z.md
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
T-090-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:53.371Z

**tool call — Bash**
````
{
 "command": "git show --stat 823b718 | head -40 && echo ---- && git show --stat 02ff244 | head -20 && echo ---- && head -c 1500 evals/reports/calibration.json && echo && echo ---- && cat board/cards/T-090.md",
 "description": "Show both commits' file stats, calibration header, and T-090 card"
}
````

### User / tool · 2026-11-02T04:31:53.497Z

**tool result**
````
commit 823b718817cacf6d38cf179724fd374ad09dffdf
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:30:48 2026 -0600

    feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
    
    States follow the flag candidate itself instead of list position; tests pin the amount class, tolerated flags, record_warning alignment, the 29/30-case boundary and git provenance.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/run.py                   |  88 ++++++++++++++++-----
 tests/unit/test_eval_runner.py | 170 ++++++++++++++++++++++++++++++++++++++++-
 2 files changed, 237 insertions(+), 21 deletions(-)
----
commit 02ff2440f195580a19627586ac44d7df25906d0c
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:16 2026 -0600

    chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
    
    Header carries source_commit, source_tree_clean, backend and prompt/lexicon hashes.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/reports/calibration.json | 70 ++++++++++++++++++++++++++----------------
 1 file changed, 44 insertions(+), 26 deletions(-)
----
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,
   "total": 10
  },
  "verified": {
   "cases": [
    "case_01_date_formats",
    "case_02_gap_boundaries",
    "case_03_rate_and_ocr",
    "case_04_duplicates_no_amounts",
    "case_05_provider_conflict",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "case_08_diagnosis_temptation",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 83,
   "total": 84
  }
 },
 "by_type": {
  "amount": {
   "needs_review": {
    "by_case": {
     "case_03_rate_and_ocr": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 6,
    "total": 6
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_03_rate_and_ocr": [
      2,
      2
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 9,
    "total": 9
   }
  },
  "entry": {
   "needs_review": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
   
----
---
id: "T-090"
title: "Calibrated confidence: measured precision per state from evals"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:31:43Z"
claimed_by: "qa"
claimed_at: "2026-11-02T04:27:39Z"
rounds: 1
commits: ["d0aee83", "02ff244", "823b718"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-090-staff-engineer.md", "at": "2026-11-02T04:27:39Z"}
ac:
  - {"n": 1, "text": "evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)", "done": true, "evidence": "evals/reports/calibration.json generated from a clean worktree of 823b718 (source_commit, source_tree_clean=true, backend=fixture in header): verified 83/84, needs_review 10/10; tests/unit/test_eval_runner.py regenerates it from git archive of source_commit and compares; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T04:16:04Z qa: claimed
- 2026-11-02T04:19:52Z qa: AC 1 checked: evals/run.py score_calibration/build_calibration; evals/reports/calibration.json (fixture backend: verified 82/83, needs_review 11/13, 10 golden cases, small-sample caveat); tests/unit/test_eval_runner.py 6 new tests incl. no-percent check; eval-suite tests 126 pass. UI line pending frontend (note).
- 2026-11-02T04:19:52Z qa: FOR BACKEND: serve evals/reports/calibration.json (regenerated by every full 'python -m evals.run'; keys: backend, case_count, small_sample, by_state{verified,needs_review:{matched,total,cases}}, by_type{entry|amount|flag:{state:{matched,total,by_case}}}, sentences{overall,by_type}) as a read-only 'calibration' field (e.g. GET /api/meta or /api/calibration; null when the file is absent). FOR FRONTEND: render sentences.overall.verified verbatim (it reads 'Verified items matched the record N/M times in testing (small sample: 10 cases).'); never compute or show a %. Show backend name (fixture = recorded model replies) beside it. Numbers shipped now are from the FIXTURE backend; a live run overwrites the file with its own backend field.
- 2026-11-02T04:19:52Z qa: moved in_progress -> in_review
- 2026-11-02T04:19:58Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T04:27:39Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-090-staff-engineer.md; round 1; findings:
    - [blocker] Committed calibration.json does not reproduce from the commit and has no traceable run — fix: Regenerate calibration.json with a full python -m evals.run at the commit being shipped (fixture backend) and commit it with its report .md and latest.json in the same commit. Do not hand-place or copy the file. Update the card evidence to the regenerated counts (83/84 and 10/10 at d0aee83
    - [major] AC 1 is marked done while its UI clause is unbuilt — fix: Set AC 1 to done: false, or split it: AC 1a (eval counts, done) and AC 1b (served read-only calibration field and UI line rendered verbatim, no percent), with 1b linked to the frontend and backend cards that will build it.
    - [major] Amount matching ignores class in no test; mutant survives and golden counts do not change — fix: Keep the class term and add a unit test in tests/unit/test_eval_runner.py: in the sample, change the kind of one verified amount (for example $6,240 charge to rate) and assert that the verified amount count falls from 2/2 to 1/2 for the sample.
    - [major] The sentence the UI will render verbatim names no backend and no provenance — fix: Put the backend and the golden-set basis into the sentence, for example 'Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases).' Build it in build_calibration so the UI cannot drop it.
    - [minor] Small-sample threshold boundary at 29 cases is not tested; lowering CAL_SMALL_N to 5 survives — fix: Add the 29-case assertion beside the 30-case one: at 29 cases the overall sentence carries 'small sample'; at 30 it does not.
    - [minor] Tolerated-flag and record_warning alignment mutants survive — fix: Add a test with one tolerated candidate (expect it counted as matched) and one case with a record_warning placed before a flag (expect the states to stay aligned). Prefer matching by candidate identity over zip position.
    - [minor] Items are dropped from the denominator silently — fix: Count the excluded items per cell and print them beside the sentence ('N items not scored'); or state in the sentence that the count covers produced items only.
    - [minor] calibration.json is outside the freshness check and embeds a wall-clock timestamp — fix: Add the calibration.json hash to the check-fresh comparison, and either drop generated_at from the served file or exclude it from the hash.
- 2026-11-02T04:27:39Z qa: claimed
- 2026-11-02T04:31:37Z qa: AC 1 edited: evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)
- 2026-11-02T04:31:37Z qa: AC 1 checked: evals/reports/calibration.json generated from a clean worktree of 823b718 (source_commit, source_tree_clean=true, backend=fixture in header): verified 83/84, needs_review 10/10; tests/unit/test_eval_runner.py regenerates it from git archive of source_commit and compares; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed
- 2026-11-02T04:31:37Z qa: r2: commits 823b718 (code, tests) and 02ff244 (calibration.json from clean worktree 823b718, worktree removed). Blocker: header has source_commit, source_tree_clean, backend, hashes; tests: ancestor-of-HEAD, regenerate-from-source-commit equality, check-fresh fails on edited count/changed hashes. Major 2: AC 1 narrowed to the eval side, served field + UI line is T-096. Major 3: amount class test. Major 4: sentences name backend + golden set (+ 'recorded replies' for fixture). Minors: 29/30 boundary, tolerated flag, record_warning alignment (state now travels with the candidate, no zip), not_scored counts, check-fresh covers calibration.json. Nit: 7 tests originally, not 6; selector now gives 84. generated_at kept in file (test ignores it). Not done: latest.json/.md not regenerated (latest.json is the live claude-cli report). FOR FRONTEND T-096: sentences now end with backend+basis already, render verbatim.
- 2026-11-02T04:31:37Z qa: moved in_progress -> in_review
- 2026-11-02T04:31:43Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: calibration.json regenerated from a clean worktree of 823b718 (fixture 83/84 verified, 10/10 needs_review) with source_commit/source_tree_clean/backend/hashes in the header; sentences name backend, golden set and recorded replies; not_scored counts; flag state follows the candidate (no zip); check-fresh validates calibration.json. How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed, incl. a test that regenerates the file from git archive of its source commit and compares (ignoring generated_at). Left: served field (backend) and UI line (T-096). Surprise: the dirty shared tree gave 84/85 vs the clean 83/84, so provenance has to be recorded, not assumed.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:55.474Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json\nd=json.load(open('evals/reports/calibration.json'))\nprint(list(d.keys()))\nfor k in d:\n    if k not in ('by_state','by_type','sentences'): print(k, json.dumps(d[k])[:400])\nprint(json.dumps(d.get('sentences'),indent=1))\n\" ; echo ----; grep -n '\"generated_at\"\\|\"source\\|\"hash\\|\"prompt\\|\"lexicon\\|\"backend\"\\|\"tree' evals/reports/calibration.json | head -30",
 "description": "Print calibration.json header keys and sentences"
}
````

### User / tool · 2026-11-02T04:31:55.596Z

**tool result**
````
['backend', 'by_state', 'by_type', 'case_count', 'cases', 'generated_at', 'hashes', 'match_rule', 'models', 'not_scored', 'schema', 'sentences', 'small_sample', 'source', 'source_commit', 'source_tree_clean']
backend "fixture"
case_count 10
cases ["sample", "case_01_date_formats", "case_02_gap_boundaries", "case_03_rate_and_ocr", "case_04_duplicates_no_amounts", "case_05_provider_conflict", "case_06_subtle_pre_existing", "case_07_prompt_injection", "case_08_diagnosis_temptation", "case_09_nonvisit_hides_gap"]
generated_at "2026-11-02T04:31:09Z"
hashes {"app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263", "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca", "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2", "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725", "app
match_rule "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count."
models {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}
not_scored {"amount": 0, "entry": 0, "flag": 0, "total": 0}
schema "evals.calibration/1"
small_sample true
source "evals.run over the golden cases; measured counts only (D-042, scope cut 10)"
source_commit "823b718817cacf6d38cf179724fd374ad09dffdf"
source_tree_clean true
{
 "by_type": {
  "amount": {
   "needs_review": "Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  },
  "entry": {
   "needs_review": "Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  },
  "flag": {
   "needs_review": "Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  }
 },
 "overall": {
  "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
  "verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
 }
}
----
2: "backend": "fixture",
213: "generated_at": "2026-11-02T04:31:09Z",
214: "hashes": {
261: "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
262: "source_commit": "823b718817cacf6d38cf179724fd374ad09dffdf",
263: "source_tree_clean": true
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:31:57.319Z

**tool call — Bash**
````
{
 "command": "sed -n 214,262p evals/reports/calibration.json && echo ---- && git -C /Users/arsis/zlayt-pm-project worktree list && echo ---- && git show 823b718:evals/run.py | grep -n 'def hashes' -A 25 | head -50",
 "description": "Show full hashes block and the hashes() function at 823b718"
}
````

### User / tool · 2026-11-02T04:31:57.379Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git worktree` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:00.342Z

**tool call — Bash**
````
{
 "command": "sed -n 214,262p evals/reports/calibration.json && echo ---- && git show 823b718:evals/run.py | grep -n 'def hashes' -A 25 | head -40",
 "description": "Show full hashes block and hashes() function at 823b718"
}
````

### User / tool · 2026-11-02T04:32:00.448Z

**tool result**
````
 "hashes": {
  "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
  "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca",
  "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
  "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
  "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
  "app/llm/prompts/judge_conflict_v1.md": "10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa",
  "app/llm/prompts/judge_conflict_v2.md": "6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6",
  "app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b",
  "app/llm/prompts/judge_flag_v1.md": "97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432",
  "app/llm/prompts/judge_flag_v2.md": "7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe",
  "app/llm/prompts/narrative_v1.md": "3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac",
  "app/llm/prompts/split_v1.md": "9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b"
 },
 "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
 "models": {
  "generator": "claude-sonnet-5-5",
  "judge": "claude-haiku-5-5"
 },
 "not_scored": {
  "amount": 0,
  "entry": 0,
  "flag": 0,
  "total": 0
 },
 "schema": "evals.calibration/1",
 "sentences": {
  "by_type": {
   "amount": {
    "needs_review": "Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "entry": {
    "needs_review": "Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "flag": {
    "needs_review": "Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   }
  },
  "overall": {
   "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  }
 },
 "small_sample": true,
 "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
 "source_commit": "823b718817cacf6d38cf179724fd374ad09dffdf",
----
83:def hashes(root=ROOT):
84-    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
85-    out = {}
86-    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
87-        out[p.relative_to(root).as_posix()] = sha256_file(p)
88-    lex = root / "app" / "llm" / "lexicon.yaml"
89-    if lex.exists():
90-        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
91-    return out
92-
93-
94-def split_regex_text(s):
95-    return re.sub(r'"[^"]*"', " ", s or "")
96-
97-
98-def regex_hits(mn, text):
99-    """Golden must_not regex semantics (README): strip double-quoted spans, ignore a match when unless_context matches the 80 chars before it."""
100-    s = split_regex_text(text)
101-    rx = re.compile(mn["pattern"])
102-    ctx = re.compile(mn["unless_context"]) if mn.get("unless_context") else None
103-    return [m.group(0) for m in rx.finditer(s) if not (ctx and ctx.search(s[max(0, m.start() - 80):m.start()]))]
104-
105-
106-# ---------------------------------------------------------------- per-case scoring (pure; tested with fake pipeline output)
107-def product_entries(out):
108-    return list(out.get("entries") or []) + list(out.get("undated_entries") or [])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:07.733Z

**tool call — Bash**
````
{
 "command": "git show 823b718:evals/run.py | grep -n 'add_argument\\|def main\\|latest.json\\|ROOT =\\|source_tree_clean\\|def git_' | head -40",
 "description": "Inspect run.py CLI args and output paths at 823b718"
}
````

### User / tool · 2026-11-02T04:32:07.830Z

**tool result**
````
2:evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
6:    python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
28:ROOT = pathlib.Path(__file__).resolve().parents[1]
67:def git_source(root=ROOT):
338:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "hashes": hashes_ or {},
940:    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
946:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
947:    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
950:        print("check-fresh: no latest.json", file=sys.stderr)
1010:def main(argv=None, pipeline=None):
1012:    ap.add_argument("--check-fresh", action="store_true")
1013:    ap.add_argument("--check-spec", action="store_true")
1014:    ap.add_argument("--backend", default=None)
1015:    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
1016:    ap.add_argument("--out", default=str(REPORTS))
1020:        return check_fresh(out / "latest.json")
1023:        latest = out / "latest.json"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:09.023Z

**tool call — Bash**
````
{
 "command": "git show 823b718:evals/run.py | sed -n 60,82p && echo ---- && git show 823b718:evals/run.py | sed -n 1010,1060p",
 "description": "Read git_source and main() at 823b718"
}
````

### User / tool · 2026-11-02T04:32:09.139Z

**tool result**
````
def golden_cases():
    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]


def git_source(root=ROOT):
    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
    import subprocess
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        return {"commit": head, "clean": not dirty}
    except Exception:
        return {"commit": None, "clean": None}


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


----
def main(argv=None, pipeline=None):
    ap = argparse.ArgumentParser(prog="python -m evals.run")
    ap.add_argument("--check-fresh", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.check_fresh:
        return check_fresh(out / "latest.json")
    if a.check_spec:
        s = check_spec()
        latest = out / "latest.json"
        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
        data.update(s)
        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
        out.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps(s))
        return 0 if s["spec_matches_golden"] else 1
    try:
        refuse_curated()
    except CuratedFixtures as e:
        print(f"evals.run: {e}", file=sys.stderr)
        return 2
    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
    backend = normalize_backend(raw)
    if backend is None:
        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
              f"Nothing was run.", file=sys.stderr)
        return 2
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    real = pipeline is None
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
    path = write_report(report, out)
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:19.178Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad\nmkdir -p \"$SCR/t090r2\" && cd \"$SCR/t090r2\" && rm -rf clone && git clone -q /Users/arsis/zlayt-pm-project clone && git -C clone checkout -q --detach 823b718 && echo \"HEAD: $(git -C clone rev-parse HEAD)\" && echo \"tracked dirty (expect empty): [$(git -C clone status --porcelain --untracked-files=no)]\" && echo \"env LLM_BACKEND=[${LLM_BACKEND:-unset}] ENABLE_LIVE=[${ENABLE_LIVE:-unset}]\"",
 "description": "Clone project into scratchpad and check out 823b718 detached"
}
````

### User / tool · 2026-11-02T04:32:22.053Z

**tool result**
````
HEAD: 823b718817cacf6d38cf179724fd374ad09dffdf
tracked dirty (expect empty): []
env LLM_BACKEND=[unset] ENABLE_LIVE=[unset]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:24.776Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\ncd \"$SCR/clone\" && for n in 1 2; do mkdir -p \"$SCR/out$n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys,runpy; sys.path.insert(0, '$SCR/clone'); sys.argv=['python -m evals.run','--out','$SCR/out$n']; import evals.run as r; print('module from', r.__file__); runpy.run_module('evals.run', run_name='__main__')\" ; echo \"exit=$?\"; done; ls \"$SCR/out1\" \"$SCR/out2\"",
 "description": "Regenerate calibration twice from clean clone of 823b718",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T04:32:27.242Z

**tool result**
````
<frozen runpy>:128: RuntimeWarning: 'evals.run' found in sys.modules after import of package 'evals', but prior to execution of 'evals.run'; this may result in unpredictable behaviour
llm call failed call_id=c5dc144ff36e8 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c8c594aaf314d step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=cd3476de5d318 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c41967b20b966 step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=c4c7edf028a0d step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
llm call failed call_id=c558ea3d8646e step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
llm call failed call_id=ccaf75804f686 step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
module from /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/clone/evals/run.py
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/out1/20261102T043225Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
exit=1
<frozen runpy>:128: RuntimeWarning: 'evals.run' found in sys.modules after import of package 'evals', but prior to execution of 'evals.run'; this may result in unpredictable behaviour
llm call failed call_id=c2afe5c4c9d1c step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c5597d26dc369 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c22fff1728ee3 step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=cd9361ad038c4 step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=c9748b4661ee8 step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
llm call failed call_id=c8319a157e299 step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
llm call failed call_id=c185824fd199f step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
module from /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/clone/evals/run.py
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/out2/20261102T043227Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
exit=1
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/out1:
20261102T043225Z.md
calibration.json
latest.json

/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/out2:
20261102T043227Z.md
calibration.json
latest.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:32.067Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\ncd /Users/arsis/zlayt-pm-project && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,sys\ndef load(p):\n    d=json.load(open(p)); d.pop('generated_at',None); return d\nc=load('evals/reports/calibration.json')\nfor n in (1,2):\n    r=load('$SCR/out%d/calibration.json'%n)\n    print('out%d == committed (minus generated_at):'%n, r==c)\n    if r!=c:\n        for k in sorted(set(r)|set(c)):\n            if r.get(k)!=c.get(k): print('  differs at key', k)\nr1=load('$SCR/out1/calibration.json'); r2=load('$SCR/out2/calibration.json')\nprint('out1 == out2 (minus generated_at):', r1==r2)\nprint('regen source_commit', r1.get('source_commit'), 'clean', r1.get('source_tree_clean'), 'backend', r1.get('backend'))\nprint('committed source_commit', c.get('source_commit'), 'clean', c.get('source_tree_clean'), 'backend', c.get('backend'))\nprint('regen overall', r1['sentences']['overall']['verified'], '|', r1['sentences']['overall']['needs_review'])\nprint('committed generated_at', json.load(open('evals/reports/calibration.json'))['generated_at'])\nprint('regen generated_at', json.load(open('$SCR/out1/calibration.json'))['generated_at'])\n\"; echo ---; diff <(python3 -c \"import json;d=json.load(open('evals/reports/calibration.json'));d.pop('generated_at');print(json.dumps(d,indent=1,sort_keys=True))\") <(python3 -c \"import json;d=json.load(open('$SCR/out1/calibration.json'));d.pop('generated_at');print(json.dumps(d,indent=1,sort_keys=True))\") && echo \"diff: identical after sort (python3 system)\"; echo; cmp <(grep -v generated_at evals/reports/calibration.json) <(grep -v generated_at \"$SCR/out1/calibration.json\") && echo \"byte-identical excluding generated_at line\"",
 "description": "Compare regenerated calibration.json with committed file ignoring generated_at"
}
````

### User / tool · 2026-11-02T04:32:32.221Z

**tool result**
````
out1 == committed (minus generated_at): True
out2 == committed (minus generated_at): True
out1 == out2 (minus generated_at): True
regen source_commit 823b718817cacf6d38cf179724fd374ad09dffdf clean True backend fixture
committed source_commit 823b718817cacf6d38cf179724fd374ad09dffdf clean True backend fixture
regen overall Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample). | Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).
committed generated_at 2026-11-02T04:31:09Z
regen generated_at 2026-11-02T04:32:25Z
---
diff: identical after sort (python3 system)

byte-identical excluding generated_at line
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:33.686Z

**tool call — Bash**
````
{
 "command": "git show 823b718 -- evals/run.py",
 "description": "Show code diff of evals/run.py in 823b718"
}
````

### User / tool · 2026-11-02T04:32:33.788Z

**tool result**
````
commit 823b718817cacf6d38cf179724fd374ad09dffdf
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:30:48 2026 -0600

    feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
    
    States follow the flag candidate itself instead of list position; tests pin the amount class, tolerated flags, record_warning alignment, the 29/30-case boundary and git provenance.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index 9d533a3..0337af1 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -64,6 +64,18 @@ def golden_cases():
     return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]
 
 
+def git_source(root=ROOT):
+    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
+    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
+    import subprocess
+    try:
+        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
+        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
+        return {"commit": head, "clean": not dirty}
+    except Exception:
+        return {"commit": None, "clean": None}
+
+
 def sha256_file(p):
     return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
 
@@ -165,7 +177,7 @@ def to_candidates(out):
     for f in out.get("flags") or []:
         if f.get("type") == "record_warning":
             continue
-        c = {"type": f["type"], "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
+        c = {"type": f["type"], "state": f.get("state"), "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
                                              for e in f.get("evidence", [])]}
         comp = f.get("computed") or {}
         c.update(from_date=f.get("from_date", comp.get("from")), to_date=f.get("to_date", comp.get("to")), days=f.get("days", comp.get("days")))
@@ -231,17 +243,23 @@ CAL_TYPES = ("entry", "amount", "flag")
 CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
 
 
-def score_calibration(exp, out):
+def score_calibration(exp, out, unscored=None):
     """Per product item that is live (verified or needs_review): did it match the golden answer?  Returns
     {item type: {state: [matched, total]}}.  Same match rules as the recall/precision metrics (no new notion of 'correct'):
     entry = some golden entry is found in it (entry_found); amount = a golden amount with the same record, raw text, class and value;
-    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored."""
+    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored on purpose.
+    `unscored` (optional dict) is filled with {item type: n} for produced items that carry no usable state (missing or unknown) or that
+    were dropped as duplicates of an earlier flag, so the denominator never silently shrinks (T-090 r2)."""
     tally = {t: {s: [0, 0] for s in CAL_STATES} for t in CAL_TYPES}
+    if unscored is not None:
+        unscored.update({t: 0 for t in CAL_TYPES})
 
     def add(kind, state, ok):
         if state in CAL_STATES:
             tally[kind][state][1] += 1
             tally[kind][state][0] += bool(ok)
+        elif unscored is not None and state != "rejected":
+            unscored[kind] += 1
 
     for e in product_entries(out):
         add("entry", e.get("state"), any(entry_found(g, [e])[0] for g in exp["entries"]))
@@ -254,18 +272,18 @@ def score_calibration(exp, out):
                 ok = True
                 break
         add("amount", a.get("state"), ok)
-    flags = [f for f in out.get("flags") or [] if f.get("type") != "record_warning"]
-    cands = to_candidates(out)
-    for c, f in zip(cands, flags):
-        c["_state"] = f.get("state")
+    cands = to_candidates(out)                    # each candidate carries its own state; record_warning flags are not candidates
     _, uniq, owned = assign_detail(exp["flags"], cands)
     for i, c in enumerate(uniq):
         if c["type"] in FLAG_TYPES:
-            add("flag", c["_state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
+            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
+    if unscored is not None:
+        unscored["flag"] += sum(1 for c in cands if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES) - \
+            sum(1 for c in uniq if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES)       # duplicates of an earlier flag
     return tally
 
 
-def build_calibration(results, backend, models=None, generated_at=None):
+def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
     """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
     Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
     names = list(results)
@@ -286,11 +304,17 @@ def build_calibration(results, backend, models=None, generated_at=None):
         cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
         by_state[s] = {"matched": m, "total": tot, "cases": cs}
     small_cases = len(names) < CAL_SMALL_N
+    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
+    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)
 
     def caveat(total):
+        """Names the backend and what was run, so the sentence cannot be read as live-model precision when it is a replay (T-090 r2)."""
+        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{len(names)} golden cases"]
         if small_cases:
-            return f" (small sample: {len(names)} cases)"
-        return f" (small sample: {total} items)" if total < CAL_SMALL_N else ""
+            parts.append("small sample")
+        elif total < CAL_SMALL_N:
+            parts.append(f"small sample: {total} items")
+        return f" on the {backend} backend ({', '.join(parts)})"
 
     label = {"verified": "Verified items matched the record {m}/{t} times in testing",
              "needs_review": "Items marked needs review matched the record {m}/{t} times in testing"}
@@ -298,7 +322,9 @@ def build_calibration(results, backend, models=None, generated_at=None):
     for s in CAL_STATES:
         b = by_state[s]
         sentences["overall"][s] = ((label[s].format(m=b["matched"], t=b["total"]) + caveat(b["total"]) + ".") if b["total"]
-                                   else f"No {s.replace('_', ' ')} items were seen in testing.")
+                                   else f"No {s.replace('_', ' ')} items were seen in testing on the {backend} backend.")
+        if b["total"] and not_scored["total"]:
+            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
     noun = {"entry": "entries", "amount": "amounts", "flag": "flags"}
     for t in CAL_TYPES:
         sentences["by_type"][t] = {}
@@ -306,11 +332,14 @@ def build_calibration(results, backend, models=None, generated_at=None):
             c = cells[t][s]
             sentences["by_type"][t][s] = (f"{('Verified' if s == 'verified' else 'Needs-review')} {noun[t]} matched the record {c['matched']}/{c['total']} "
                                           f"times in testing{caveat(c['total'])}." if c["total"] else
-                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing.")
+                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
     return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
             "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
+            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "hashes": hashes_ or {},
             "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
-                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored.",
+                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
+                          "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
+            "not_scored": not_scored,
             "cases": names, "case_count": len(names), "small_sample": small_cases or any(by_state[s]["total"] < CAL_SMALL_N for s in CAL_STATES),
             "by_state": by_state, "by_type": cells, "sentences": sentences}
 
@@ -428,12 +457,13 @@ def run_cases(pipeline, backend, cases=None, runs_dir=None):
     results, outs = {}, {}
     for name, text, exp in (cases or golden_cases()):
         out = pipeline.run_case(text, backend)
+        unscored = {}
         outs[name] = out
         write_run_artifact(runs_dir, name, out, name)
         results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
                          "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
                          "unsupported_summaries": unsupported_summaries(out), "judge_unavailable": judge_unavailable_in(out), "grounding": grounding(text, out),
-                         "calibration": score_calibration(exp, out)}
+                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
     return results, outs
 
 
@@ -831,11 +861,12 @@ def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, c
     a = assertions(results)
     spec = check_spec(req_path)
     sample_out = outs.get("sample", {})
+    source = git_source()
     report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
               "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
               "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
               "thresholds": THRESHOLDS, "cases": list(results)}
-    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"])
+    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
     if runs_dir is not None:
         report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
     met, bars, blockers = evaluate_report(report)
@@ -860,7 +891,7 @@ def render_calibration(c):
     """Calibrated confidence (T-090): counts per state and per type, backend named, no percentages."""
     if not c:
         return []
-    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases)", ""]
+    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases, source commit `{(c.get('source_commit') or 'unknown')[:10]}`)", ""]
     L += [f"- {c['sentences']['overall'][s]}" for s in CAL_STATES]
     L += ["", "| Item type | Verified (matched/seen) | Needs review (matched/seen) |", "|---|---|---|"]
     for t in CAL_TYPES:
@@ -922,7 +953,28 @@ def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
     diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
     for k in diff:
         print(f"check-fresh: {k} changed since the report", file=sys.stderr)
-    return 1 if diff else 0
+    bad = check_calibration(p.parent / "calibration.json", root)
+    for m in bad:
+        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
+    return 1 if diff or bad else 0
+
+
+def check_calibration(path, root=ROOT):
+    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
+    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
+    p = pathlib.Path(path)
+    if not p.exists():
+        return []
+    c = json.loads(p.read_text())
+    bad = []
+    for s in CAL_STATES:
+        for k in ("matched", "total"):
+            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
+                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
+    old = c.get("hashes") or {}
+    now = hashes(root)
+    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
+    return bad
 
 
 def load_pipeline():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:36.318Z

**tool call — Bash**
````
{
 "command": "git show 823b718 -- tests/unit/test_eval_runner.py | head -300",
 "description": "Show test diff in 823b718 for eval runner"
}
````

### User / tool · 2026-11-02T04:32:36.427Z

**tool result**
````
commit 823b718817cacf6d38cf179724fd374ad09dffdf
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:30:48 2026 -0600

    feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
    
    States follow the flag candidate itself instead of list position; tests pin the amount class, tolerated flags, record_warning alignment, the 29/30-case boundary and git provenance.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index df8ca7e..ebc9d1a 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -487,8 +487,9 @@ def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
     assert c["by_state"]["needs_review"] == {"matched": 1, "total": 3, "cases": ["a", "b"]}
     assert c["by_type"]["entry"]["verified"]["by_case"] == {"a": [3, 4], "b": [1, 1]}
     assert c["backend"] == "fixture" and c["case_count"] == 2 and c["small_sample"] is True
-    assert c["sentences"]["overall"]["verified"] == "Verified items matched the record 6/7 times in testing (small sample: 2 cases)."
-    assert c["sentences"]["by_type"]["flag"]["verified"] == "No verified flags were seen in testing."
+    assert c["sentences"]["overall"]["verified"] == ("Verified items matched the record 6/7 times in testing on the fixture backend "
+                                                      "(recorded replies, 2 golden cases, small sample).")
+    assert c["sentences"]["by_type"]["flag"]["verified"] == "No verified flags were seen in testing on the fixture backend."
 
 
 def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
@@ -518,7 +519,88 @@ def test_large_sample_drops_the_case_caveat_but_keeps_the_item_caveat():
     few = {"calibration": {**row["calibration"], "entry": {"verified": [0, 0], "needs_review": [1, 2]}}}
     c = R.build_calibration({**{f"c{i}": row for i in range(29)}, "few": few}, "claude-cli")
     assert "small sample" not in c["sentences"]["overall"]["verified"]
-    assert "(small sample: 2 items)" in c["sentences"]["overall"]["needs_review"]
+    assert "(30 golden cases, small sample: 2 items)" in c["sentences"]["overall"]["needs_review"]
+
+
+def test_small_sample_boundary_is_29_vs_30_cases():
+    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
+                           "flag": {"verified": [0, 0], "needs_review": [0, 0]}}}
+    assert R.CAL_SMALL_N == 30
+    at29 = R.build_calibration({f"c{i}": row for i in range(29)}, "claude-cli")
+    at30 = R.build_calibration({f"c{i}": row for i in range(30)}, "claude-cli")
+    assert "small sample" in at29["sentences"]["overall"]["verified"] and at29["small_sample"] is True
+    assert "small sample" not in at30["sentences"]["overall"]["verified"]
+
+
+@pytest.mark.parametrize("backend,recorded", [("fixture", True), ("claude-cli", False), ("anthropic-api", False)])
+def test_every_sentence_names_the_backend_and_the_golden_set(backend, recorded):
+    """The UI renders these verbatim, so a replay on the fixture backend cannot read as live-model precision (T-090 r2)."""
+    row = {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}
+    c = R.build_calibration({"a": row}, backend)
+    sents = list(c["sentences"]["overall"].values()) + [x for by in c["sentences"]["by_type"].values() for x in by.values()]
+    assert sents and all(f"on the {backend} backend" in x and "golden case" in x for x in sents)
+    assert all(("recorded replies" in x) == recorded for x in sents)
+    empty = R.build_calibration({"a": {"calibration": {}}}, backend)
+    assert all(f"{backend} backend" in x for x in empty["sentences"]["overall"].values())
+
+
+def test_amount_class_is_part_of_the_match():
+    """A verified rate that carries the same text and value as a golden charge is NOT a match (the $185-rate-is-not-a-charge rule)."""
+    def m(out):
+        for a in out["amounts"][:2]:
+            a["state"] = "verified"
+        a0 = out["amounts"][0]
+        a0["kind"] = "rate" if a0["kind"] == "charge" else "charge"
+    assert _tally("sample", m)["amount"]["verified"] == [1, 2]
+
+
+def test_tolerated_flag_counts_as_matched():
+    def m(out):
+        for f in out["flags"]:
+            f["state"] = "verified"
+        out["flags"].append({"id": "x", "type": "pre_existing", "state": "needs_review", "review_status": "pending",
+                             "evidence": [{"record_id": "r1", "excerpt": "zzz unrelated to the golden span"}]})
+    t = _tally("case_06_subtle_pre_existing", m)
+    assert t["flag"]["needs_review"] == [1, 1]                         # case_06 tolerates a pre_existing flag citing record 1 (T1)
+
+
+def test_record_warning_flags_cannot_shift_flag_states():
+    """States follow the candidate itself, not its position among the flags (a record_warning placed first used to shift every later state)."""
+    def states(out):
+        for i, f in enumerate(out["flags"]):
+            f["state"] = "verified" if i % 2 == 0 else "needs_review"
+    def plain(out):
+        states(out)
+    def with_warning(out):
+        states(out)
+        out["flags"].insert(0, {"id": "w", "type": "record_warning", "state": "needs_review", "evidence": [{"record_id": "r1", "excerpt": "x"}]})
+    a = _tally("case_06_subtle_pre_existing", plain)["flag"]
+    b = _tally("case_06_subtle_pre_existing", with_warning)["flag"]
+    assert a == b and a["verified"][1] and a["needs_review"][1]
+
+
+def test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently():
+    def m(out):
+        for f in out["flags"]:
+            f["state"] = "verified"
+        out["flags"].append({**out["flags"][0], "id": "dup"})                  # duplicate of an earlier flag: dropped by assign_detail
+        out["flags"].append({**out["flags"][0], "id": "nostate", "state": None, "evidence": [{"record_id": "r1", "excerpt": "other"}]})
+        out["flags"].append({**out["flags"][0], "id": "rej", "state": "rejected", "evidence": [{"record_id": "r1", "excerpt": "another"}]})
+        for a in out["amounts"]:
+            a["state"] = "verified"
+        out["amounts"][0].pop("state", None)
+        out["amounts"][1]["state"] = "weird"
+        out["entries"][0]["state"] = None
+    exp = G.expected("sample")
+    text = next(t for n, t, _ in R.golden_cases() if n == "sample")
+    out = Perfect().run_case(text, "claude-cli")
+    m(out)
+    un = {}
+    R.score_calibration(exp, out, un)
+    assert un == {"entry": 1, "amount": 2, "flag": 2}                          # rejected is excluded on purpose; duplicate and stateless flags are not
+    c = R.build_calibration({"sample": {"calibration": {t: {"verified": [1, 1], "needs_review": [0, 0]} for t in R.CAL_TYPES}, "calibration_unscored": un}}, "fixture")
+    assert c["not_scored"] == {"entry": 1, "amount": 2, "flag": 2, "total": 5}
+    assert "Not scored: 5 produced items" in c["sentences"]["overall"]["verified"]
 
 
 def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
@@ -529,3 +611,85 @@ def test_full_report_carries_calibration_and_write_report_emits_calibration_json
     R.write_report(rep, tmp_path)
     assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
     assert "Calibrated confidence" in next(tmp_path.glob("2*.md")).read_text()
+
+
+# ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
+import os, shutil, subprocess, sys
+CAL = R.REPORTS / "calibration.json"
+
+
+def _git(*a, cwd=None):
+    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)
+
+
+def _committed():
+    return json.loads(CAL.read_text())
+
+
+def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
+    c = _committed()
+    assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
+    assert c["source_tree_clean"] is True and c["hashes"]
+
+
+def test_committed_calibration_source_commit_is_an_ancestor_of_head():
+    c = _committed()
+    if _git("rev-parse", "--git-dir").returncode or _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode:
+        pytest.skip("no git history here (shallow or exported tree)")
+    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0
+
+
+def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
+    """T-090 r2 blocker: the shipped counts must come from the code of the commit named in the header. Export that commit
+    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at."""
+    c = _committed()
+    if _git("rev-parse", "--git-dir").returncode or _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode:
+        pytest.skip("source commit not available in this checkout")
+    src = tmp_path / "src"
+    src.mkdir()
+    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
+    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
+    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
+    env["PYTHONPATH"] = str(src)
+    out = tmp_path / "out"
+    r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
+    assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
+    fresh = json.loads((out / "calibration.json").read_text())
+    for d in (fresh, c):
+        d.pop("generated_at")
+    fresh["source_tree_clean"] = c["source_tree_clean"]                        # the export has no .git, so it cannot attest cleanliness itself
+    assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
+    assert {k: v for k, v in fresh.items() if k != "source_commit"} == {k: v for k, v in c.items() if k != "source_commit"}
+
+
+def test_git_source_reports_commit_and_dirtiness(tmp_path):
+    if shutil.which("git") is None:
+        pytest.skip("git missing")
+    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
+    (tmp_path / "f").write_text("a")
+    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
+    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
+    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
+    a = R.git_source(tmp_path)
+    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
+    (tmp_path / "f").write_text("b")
+    assert R.git_source(tmp_path)["clean"] is False
+    assert R.git_source(tmp_path / "nowhere") == {"commit": None, "clean": None}
+
+
+def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
+    rep = tmp_path / "latest.json"
+    rep.write_text(json.dumps({"hashes": R.hashes()}))
+    cal = _committed()
+    cal["hashes"] = R.hashes()                                                  # consistent with this checkout; the committed hashes go stale on any prompt edit
+    (tmp_path / "calibration.json").write_text(json.dumps(cal))
+    assert R.check_fresh(rep) == 0                                              # the committed pair is consistent with the repo
+    cal["by_state"]["verified"]["matched"] += 1
+    (tmp_path / "calibration.json").write_text(json.dumps(cal))
+    assert R.check_fresh(rep) == 1
+    cal = _committed()
+    cal["hashes"] = R.hashes()
+    k = sorted(cal["hashes"])[0]
+    cal["hashes"][k] = "0" * 64
+    (tmp_path / "calibration.json").write_text(json.dumps(cal))
+    assert R.check_fresh(rep) == 1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:48.365Z

**tool call — Bash**
````
{
 "command": "timeout 900 .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -25; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run the calibration and eval_runner unit test selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:32:48.453Z

**tool result**
````
/bin/bash: timeout: command not found
exit=127
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:49.723Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -25; echo \"exit=${PIPESTATUS[0]}\"",
 "description": "Run the calibration and eval_runner unit test selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:32:56.377Z

**tool result**
````
........................................................................ [ 85%]
............                                                             [100%]
84 passed, 1284 deselected in 6.21s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:32:58.994Z

**tool call — Bash**
````
{
 "command": "sed -n 1,25p tests/unit/test_eval_runner.py && ls tests/unit | head -3 && ls tests/ && cat tests/conftest.py 2>/dev/null | head -20; cat tests/unit/conftest.py 2>/dev/null | head -20; grep -n 'pythonpath\\|testpaths\\|rootdir' pytest.ini setup.cfg pyproject.toml 2>/dev/null",
 "description": "Inspect test imports and pytest config"
}
````

### User / tool · 2026-11-02T04:32:59.094Z

**tool result (error)**
````
Exit code 2
"""evals.run scoring, ship bar, freshness and lexicon recall against a FAKE pipeline built from the golden answers (no model, no network).
T-038 AC1-AC7, AC9; R-CO-3, R-CO-7, R-TL-4, R-RV-6, D-026."""
import copy, json, re
import pytest
from evals import run as R
from tests.unit import _golden as G

ITEMS = R.load_jsonl(G.G / "hallucinations.jsonl")
CONTROLS = R.load_jsonl(G.G / "hallucinations_controls.jsonl")
BAD = {i["candidate_summary"] for i in ITEMS}
SAMPLE = next(t for n, t, _ in R.golden_cases() if n == "sample")
REC = re.compile(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n')

UNSPLIT = (R.GOLD / "unsplit_paste.txt").read_text()
USPLIT = json.loads((R.GOLD / "unsplit_paste.split.json").read_text())

class Perfect:
    """Pipeline whose output is derived from the golden expected files, so every bar is met unless a test perturbs it."""
    def __init__(self, backend="claude-cli", mutate=None, flip=False):
        self.mutate, self.flip, self.sample_runs = mutate, flip, 0
    def run_case(self, text, backend):
        if text == UNSPLIT:
            return self.unsplit(backend)
        name = next(n for n, t, _ in R.golden_cases() if t == text)
        exp = G.expected(name)
__init__.py
__pycache__
_fakes.py
__init__.py
__pycache__
conftest.py
e2e
fixtures
unit
"""Puts the repo root on sys.path so tests import `app.*` (tests only; no key, no network: fixture backend only)."""
import pathlib, sys
ROOT = pathlib.Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:08.206Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nC=$SCR/clone\nrun() { (cd $C && env -u LLM_BACKEND -u ENABLE_LIVE $PY -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | grep -E \"passed|failed|SKIPPED|FAILED\" | tail -6); git -C $C checkout -q -- evals/reports/calibration.json; }\necho \"== baseline (unmodified 823b718 clone)\"; run\necho \"== M-A: by_state.verified.matched 83->84 only (by_type untouched)\"\n$PY -c \"import json;p='$C/evals/reports/calibration.json';d=json.load(open(p));d['by_state']['verified']['matched']+=1;open(p,'w').write(json.dumps(d,indent=1)+'\\n')\"; run\necho \"== M-B: sentences.overall.verified text edited (drop 'recorded replies')\"\n$PY -c \"import json;p='$C/evals/reports/calibration.json';d=json.load(open(p));d['sentences']['overall']['verified']=d['sentences']['overall']['verified'].replace('recorded replies','live model replies');open(p,'w').write(json.dumps(d,indent=1)+'\\n')\"; run\necho \"== M-C: source_commit replaced by a non-existent 40-hex hash\"\n$PY -c \"import json;p='$C/evals/reports/calibration.json';d=json.load(open(p));d['source_commit']='1'*40;open(p,'w').write(json.dumps(d,indent=1)+'\\n')\"; run\necho \"== M-D: counts edited in by_type only (amount verified matched 9->8 and by_state untouched)\"\n$PY -c \"import json;p='$C/evals/reports/calibration.json';d=json.load(open(p));d['by_type']['amount']['verified']['matched']=8;open(p,'w').write(json.dumps(d,indent=1)+'\\n')\"; run\necho \"== M-E: hashes edited to a stale value\"\n$PY -c \"import json;p='$C/evals/reports/calibration.json';d=json.load(open(p));k=sorted(d['hashes'])[0];d['hashes'][k]='0'*64;open(p,'w').write(json.dumps(d,indent=1)+'\\n')\"; run\ngit -C $C status --porcelain --untracked-files=no; echo \"clone restored: [$(git -C $C status --porcelain --untracked-files=no)]\"",
 "description": "Mutate scratch clone calibration.json and run selector for each hand-edit",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:33:08.260Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to 84)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:16.432Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\ncd $SCR/clone && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -4",
 "description": "Run baseline selector in unmodified scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:33:21.582Z

**tool result**
````
E       KeyError: 'source_commit'

tests/unit/test_eval_runner.py:646: KeyError
3 failed, 81 passed, 1116 deselected in 4.73s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:29.253Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\ncd $SCR/clone && cd $SCR/clone && git checkout -q --detach 02ff244 && echo \"HEAD $(git rev-parse --short HEAD) dirty=[$(git status --porcelain --untracked-files=no)]\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -3",
 "description": "Check out the file commit 02ff244 in scratch clone and rerun selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:33:32.751Z

**tool result**
````
HEAD 02ff244 dirty=[]
.......................................................................  [100%]
71 passed, 1153 deselected in 3.00s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:39.094Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest --collect-only -q tests/unit -k \"calibration or eval_runner\" 2>/dev/null | sed 's/::.*//' | sort | uniq -c; echo ---; cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/clone && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest --collect-only -q tests/unit -k \"calibration or eval_runner\" 2>/dev/null | sed 's/::.*//' | sort | uniq -c; echo ---; cd /Users/arsis/zlayt-pm-project && git diff --stat HEAD -- tests/unit | tail -3; git status --porcelain -- tests/unit evals | head",
 "description": "Compare collected test counts between working tree and committed clone"
}
````

### User / tool · 2026-11-02T04:33:42.760Z

**tool result**
````
   1 
   1 84/1370 tests collected (1286 deselected) in 1.39s
  84 tests/unit/test_eval_runner.py
---
   1 
   1 71/1224 tests collected (1153 deselected) in 1.26s
  71 tests/unit/test_eval_runner.py
---
 tests/unit/test_t093_eval_signature.py | 102 +++++++-
 tests/unit/test_trace.py               |  16 ++
 16 files changed, 528 insertions(+), 951 deletions(-)
 M evals/golden/judge_controls.jsonl
 M evals/run.py
D  tests/unit/_pdf_raw.py
 M tests/unit/test_date_convention.py
M  tests/unit/test_db.py
 M tests/unit/test_dismissal_patterns.py
 M tests/unit/test_eval_runner.py
 M tests/unit/test_flags_injection.py
 M tests/unit/test_flags_pass.py
D  tests/unit/test_pdf_checks_api.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:46.432Z

**tool call — Bash**
````
{
 "command": "git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/golden/judge_controls.jsonl && echo --- && git diff HEAD -- tests/unit/test_eval_runner.py | grep '^[+-]def test_\\|^[+-]@pytest' | head -30 && echo --- && git diff HEAD -- evals/run.py | head -60",
 "description": "Show uncommitted working-tree changes to eval runner and its tests"
}
````

### User / tool · 2026-11-02T04:33:46.592Z

**tool result**
````
 evals/golden/judge_controls.jsonl |  71 ++++++++-----
 evals/run.py                      | 212 ++++++++++++++++++++++++++++++--------
 tests/unit/test_eval_runner.py    | 170 +++++++++++++++++++++++++++++-
 3 files changed, 383 insertions(+), 70 deletions(-)
---
+def test_small_sample_boundary_is_29_vs_30_cases():
+@pytest.mark.parametrize("backend,recorded", [("fixture", True), ("claude-cli", False), ("anthropic-api", False)])
+def test_every_sentence_names_the_backend_and_the_golden_set(backend, recorded):
+def test_amount_class_is_part_of_the_match():
+def test_tolerated_flag_counts_as_matched():
+def test_record_warning_flags_cannot_shift_flag_states():
+def test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently():
+def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
+def test_committed_calibration_source_commit_is_an_ancestor_of_head():
+def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
+def test_git_source_reports_commit_and_dirtiness(tmp_path):
+def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
---
diff --git a/evals/run.py b/evals/run.py
index 9d533a3..981b70b 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -64,6 +64,18 @@ def golden_cases():
     return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]
 
 
+def git_source(root=ROOT):
+    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
+    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
+    import subprocess
+    try:
+        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
+        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
+        return {"commit": head, "clean": not dirty}
+    except Exception:
+        return {"commit": None, "clean": None}
+
+
 def sha256_file(p):
     return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
 
@@ -165,7 +177,7 @@ def to_candidates(out):
     for f in out.get("flags") or []:
         if f.get("type") == "record_warning":
             continue
-        c = {"type": f["type"], "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
+        c = {"type": f["type"], "state": f.get("state"), "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
                                              for e in f.get("evidence", [])]}
         comp = f.get("computed") or {}
         c.update(from_date=f.get("from_date", comp.get("from")), to_date=f.get("to_date", comp.get("to")), days=f.get("days", comp.get("days")))
@@ -231,17 +243,23 @@ CAL_TYPES = ("entry", "amount", "flag")
 CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
 
 
-def score_calibration(exp, out):
+def score_calibration(exp, out, unscored=None):
     """Per product item that is live (verified or needs_review): did it match the golden answer?  Returns
     {item type: {state: [matched, total]}}.  Same match rules as the recall/precision metrics (no new notion of 'correct'):
     entry = some golden entry is found in it (entry_found); amount = a golden amount with the same record, raw text, class and value;
-    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored."""
+    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored on purpose.
+    `unscored` (optional dict) is filled with {item type: n} for produced items that carry no usable state (missing or unknown) or that
+    were dropped as duplicates of an earlier flag, so the denominator never silently shrinks (T-090 r2)."""
     tally = {t: {s: [0, 0] for s in CAL_STATES} for t in CAL_TYPES}
+    if unscored is not None:
+        unscored.update({t: 0 for t in CAL_TYPES})
 
     def add(kind, state, ok):
         if state in CAL_STATES:
             tally[kind][state][1] += 1
             tally[kind][state][0] += bool(ok)
+        elif unscored is not None and state != "rejected":
+            unscored[kind] += 1
 
     for e in product_entries(out):
         add("entry", e.get("state"), any(entry_found(g, [e])[0] for g in exp["entries"]))
@@ -254,18 +272,18 @@ def score_calibration(exp, out):
                 ok = True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:53.461Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD now: $(git rev-parse --short HEAD) $(git log -1 --format=%s)\" && git log --oneline -4 -- evals/run.py tests/unit/test_eval_runner.py && echo --- && for r in HEAD 02ff244 823b718; do echo \"$r: run.py has git_source=$(git show $r:evals/run.py | grep -c 'def git_source') test_has_r2=$(git show $r:tests/unit/test_eval_runner.py | grep -c 'def test_committed_calibration_regenerates')\"; done && echo --- && git merge-base --is-ancestor 823b718 HEAD && echo \"823b718 is ancestor of HEAD\" ; git log --oneline 823b718..HEAD | head",
 "description": "Check whether HEAD contains the 823b718 code and test changes"
}
````

### User / tool · 2026-11-02T04:33:53.535Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($) | command: echo "HEAD now: $(git rev-parse --short HEAD) $(git log -1 --format=%s)" && git log --oneline -4 -- evals/run.py tests/unit/test_eval_runner.py && echo --- && for r in HEAD 02ff244 823b718; do echo "$
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:54.815Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git log -1 --format=%s && git log --oneline -4 -- evals/run.py tests/unit/test_eval_runner.py",
 "description": "Show HEAD commit and recent history of eval runner files"
}
````

### User / tool · 2026-11-02T04:33:54.955Z

**tool result**
````
865b186
feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
823b718 feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
d0aee83 feat(evals): calibrated confidence from measured matches per state and item type (T-090)
e491cad feat(evals): determinism signature covers every R-CO-7 field, per-run artifacts, J3/J4 seeded controls (T-093)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:33:56.892Z

**tool call — Bash**
````
{
 "command": "git log --oneline -6 && echo --- && git show 02ff244:tests/unit/test_eval_runner.py | grep -c 'def test_committed_calibration_regenerates' ; git show 823b718:tests/unit/test_eval_runner.py | grep -c 'def test_committed_calibration_regenerates'; git show 02ff244:evals/run.py | grep -c 'def git_source'; git show 823b718:evals/run.py | grep -c 'def git_source'; git merge-base --is-ancestor 823b718 02ff244 && echo \"823b718 is ancestor of 02ff244\"; git log --oneline 823b718..02ff244",
 "description": "Check git_source and regen test presence at 823b718 and 02ff244"
}
````

### User / tool · 2026-11-02T04:33:57.105Z

**tool result**
````
865b186 feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
823b718 feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
e92b6ed feat(frontend): Run the second check again button, refused export shown beside Export, pending items as a gate warning (T-081 r3, T-082 r3, D-044, D-045)
---
0
1
0
1
823b718 is ancestor of 02ff244
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:00.462Z

**tool call — Bash**
````
{
 "command": "git show --stat 2fca530 | head -30 && echo --- && git show 2fca530 -- evals/run.py tests/unit/test_eval_runner.py | head -120",
 "description": "Inspect 2fca530 changes to eval runner files"
}
````

### User / tool · 2026-11-02T04:34:00.600Z

**tool result**
````
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
---
commit 2fca530363a43f5e886a441234ba2cfc7a6725ea
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:31:03 2026 -0600

    feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
    
    Hidden text (white/background-coloured, off-page, tiny, invisible mode, covered) is found by comparing the text layer with the rendered page
    (pypdfium2 5.14.0 pinned), reported per page and kept out of the case text until the paralegal confirms the page. Scanned pages are OCR'd
    locally on request (ocr=true) with the page image served beside the text, low-confidence words marked, and every item on an OCR page held at
    needs_review (OCR_DERIVED). Missing tesseract gives a clear message. Tests skip cleanly without tesseract.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index 0337af1..9d533a3 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -64,18 +64,6 @@ def golden_cases():
     return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]
 
 
-def git_source(root=ROOT):
-    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
-    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
-    import subprocess
-    try:
-        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
-        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
-        return {"commit": head, "clean": not dirty}
-    except Exception:
-        return {"commit": None, "clean": None}
-
-
 def sha256_file(p):
     return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
 
@@ -177,7 +165,7 @@ def to_candidates(out):
     for f in out.get("flags") or []:
         if f.get("type") == "record_warning":
             continue
-        c = {"type": f["type"], "state": f.get("state"), "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
+        c = {"type": f["type"], "evidence": [{"record_no": rn(e.get("record_id", e.get("record_no"))), "excerpt": e.get("excerpt", "")}
                                              for e in f.get("evidence", [])]}
         comp = f.get("computed") or {}
         c.update(from_date=f.get("from_date", comp.get("from")), to_date=f.get("to_date", comp.get("to")), days=f.get("days", comp.get("days")))
@@ -243,23 +231,17 @@ CAL_TYPES = ("entry", "amount", "flag")
 CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
 
 
-def score_calibration(exp, out, unscored=None):
+def score_calibration(exp, out):
     """Per product item that is live (verified or needs_review): did it match the golden answer?  Returns
     {item type: {state: [matched, total]}}.  Same match rules as the recall/precision metrics (no new notion of 'correct'):
     entry = some golden entry is found in it (entry_found); amount = a golden amount with the same record, raw text, class and value;
-    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored on purpose.
-    `unscored` (optional dict) is filled with {item type: n} for produced items that carry no usable state (missing or unknown) or that
-    were dropped as duplicates of an earlier flag, so the denominator never silently shrinks (T-090 r2)."""
+    flag = counted as ok by flag_precision (one-to-one golden match, or tolerated).  Rejected items and record_warning flags are not scored."""
     tally = {t: {s: [0, 0] for s in CAL_STATES} for t in CAL_TYPES}
-    if unscored is not None:
-        unscored.update({t: 0 for t in CAL_TYPES})
 
     def add(kind, state, ok):
         if state in CAL_STATES:
             tally[kind][state][1] += 1
             tally[kind][state][0] += bool(ok)
-        elif unscored is not None and state != "rejected":
-            unscored[kind] += 1
 
     for e in product_entries(out):
         add("entry", e.get("state"), any(entry_found(g, [e])[0] for g in exp["entries"]))
@@ -272,18 +254,18 @@ def score_calibration(exp, out, unscored=None):
                 ok = True
                 break
         add("amount", a.get("state"), ok)
-    cands = to_candidates(out)                    # each candidate carries its own state; record_warning flags are not candidates
+    flags = [f for f in out.get("flags") or [] if f.get("type") != "record_warning"]
+    cands = to_candidates(out)
+    for c, f in zip(cands, flags):
+        c["_state"] = f.get("state")
     _, uniq, owned = assign_detail(exp["flags"], cands)
     for i, c in enumerate(uniq):
         if c["type"] in FLAG_TYPES:
-            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
-    if unscored is not None:
-        unscored["flag"] += sum(1 for c in cands if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES) - \
-            sum(1 for c in uniq if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES)       # duplicates of an earlier flag
+            add("flag", c["_state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
     return tally
 
 
-def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
+def build_calibration(results, backend, models=None, generated_at=None):
     """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
     Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
     names = list(results)
@@ -304,17 +286,11 @@ def build_calibration(results, backend, models=None, generated_at=None, source=N
         cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
         by_state[s] = {"matched": m, "total": tot, "cases": cs}
     small_cases = len(names) < CAL_SMALL_N
-    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
-    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)
 
     def caveat(total):
-        """Names the backend and what was run, so the sentence cannot be read as live-model precision when it is a replay (T-090 r2)."""
-        parts = (["recorded replies"] if backend == "fixture" else []) + [f"{len(names)} golden cases"]
         if small_cases:
-            parts.append("small sample")
-        elif total < CAL_SMALL_N:
-            parts.append(f"small sample: {total} items")
-        return f" on the {backend} backend ({', '.join(parts)})"
+            return f" (small sample: {len(names)} cases)"
+        return f" (small sample: {total} items)" if total < CAL_SMALL_N else ""
 
     label = {"verified": "Verified items matched the record {m}/{t} times in testing",
              "needs_review": "Items marked needs review matched the record {m}/{t} times in testing"}
@@ -322,9 +298,7 @@ def build_calibration(results, backend, models=None, generated_at=None, source=N
     for s in CAL_STATES:
         b = by_state[s]
         sentences["overall"][s] = ((label[s].format(m=b["matched"], t=b["total"]) + caveat(b["total"]) + ".") if b["total"]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:13.311Z

**tool call — Bash**
````
{
 "command": "git show --stat 2fca530 | sed -n 30,60p; echo ---; git show 2fca530 -- tests/unit/test_eval_runner.py | grep -c '^-def test_'; git show 2fca530 -- tests/unit/test_eval_runner.py | grep '^-def test_\\|^+def test_' ; echo ---; git show 865b186 --stat | head -12; echo ---; git diff --stat 02ff244 HEAD -- evals/ tests/unit/test_eval_runner.py",
 "description": "Inspect full 2fca530 stat and test file changes, and HEAD diff for eval files"
}
````

### User / tool · 2026-11-02T04:34:13.529Z

**tool result**
````
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
---
11
-def test_small_sample_boundary_is_29_vs_30_cases():
-def test_every_sentence_names_the_backend_and_the_golden_set(backend, recorded):
-def test_amount_class_is_part_of_the_match():
-def test_tolerated_flag_counts_as_matched():
-def test_record_warning_flags_cannot_shift_flag_states():
-def test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently():
-def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
-def test_committed_calibration_source_commit_is_an_ancestor_of_head():
-def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
-def test_git_source_reports_commit_and_dirtiness(tmp_path):
-def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
---
commit 865b18650a311f8b0950d4adf7076b6fe45e3ce8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:33:19 2026 -0600

    feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
    
    Language detection by code (en/es/other), unsupported languages refused clearly (case: 400 unsupported_language; record in a mixed packet: warning, skipped).
    Spanish records use extract_es_v1 and judge_faithfulness_es_v1; D-034/D-022 token checks map Spanish months, sides, negations, hedges, number formats.
    Entries carry a translation label; letter shows it; edits/rejudge check against the Spanish quote. Fixtures recorded for lib09 records 2, 4, 7.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:21.774Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2\ncd $SCR/clone && git checkout -q --detach 865b186 && echo \"HEAD $(git rev-parse --short HEAD) dirty=[$(git status --porcelain --untracked-files=no)]\" && echo \"--- selector at HEAD 865b186:\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -2; echo \"--- regen at HEAD:\"; mkdir -p $SCR/outhead && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys,runpy; sys.path.insert(0, '$SCR/clone'); sys.argv=['evals.run','--out','$SCR/outhead']; runpy.run_module('evals.run', run_name='__main__')\" 2>/dev/null | head -1; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nh=json.load(open('$SCR/outhead/calibration.json'))\nc=json.load(open('/Users/arsis/zlayt-pm-project/evals/reports/calibration.json'))\nprint('HEAD regen keys:', sorted(h.keys()))\nprint('HEAD regen by_state', h['by_state'])\nprint('committed by_state', c['by_state'])\nprint('HEAD regen source_commit', h.get('source_commit'))\n\"",
 "description": "Check out HEAD in scratch clone and run selector and regeneration",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:34:23.098Z

**tool result**
````
fatal: git checkout: --detach does not take a path argument '865b186'
--- regen at HEAD:
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/outhead/20261102T043423Z.md
HEAD regen keys: ['backend', 'by_state', 'by_type', 'case_count', 'cases', 'generated_at', 'match_rule', 'models', 'schema', 'sentences', 'small_sample', 'source']
HEAD regen by_state {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'sample'], 'matched': 10, 'total': 10}, 'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap', 'sample'], 'matched': 83, 'total': 84}}
committed by_state {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'sample'], 'matched': 10, 'total': 10}, 'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap', 'sample'], 'matched': 83, 'total': 84}}
HEAD regen source_commit None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:33.648Z

**tool call — Bash**
````
{
 "command": "git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py && echo \"HEAD evals/ and test_eval_runner.py identical to 02ff244\" ; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && git checkout -q --detach 823b718 && git checkout -q 02ff244 -- evals/reports/calibration.json && echo \"clone HEAD $(git rev-parse --short HEAD); calibration.json from 02ff244; tree: $(git status --porcelain --untracked-files=no)\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -2",
 "description": "Set scratch clone to 823b718 code with 02ff244 calibration file and run selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:34:40.350Z

**tool result**
````
HEAD evals/ and test_eval_runner.py identical to 02ff244
clone HEAD 823b718; calibration.json from 02ff244; tree: M  evals/reports/calibration.json
............                                                             [100%]
84 passed, 1116 deselected in 6.18s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:43.992Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,sys\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['by_state']['verified']['matched']+=1\njson.dump(d,open(p,'w'),indent=1)\nprint('mutated by_state.verified.matched ->', d['by_state']['verified']['matched'])\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -4",
 "description": "Hand-edit scratch clone calibration count and run selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:34:50.652Z

**tool result**
````
mutated by_state.verified.matched -> 84
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
2 failed, 82 passed, 1116 deselected in 6.18s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:34:55.788Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['sentences']['overall']['verified']=d['sentences']['overall']['verified'].replace('recorded replies','live model replies')\njson.dump(d,open(p,'w'),indent=1)\nprint('M-B sentence now:', d['sentences']['overall']['verified'][:90])\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; echo \"=== M-C\"; git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['source_commit']='1'*40\njson.dump(d,open(p,'w'),indent=1)\nprint('M-C source_commit set to', d['source_commit'][:8])\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -rs 2>&1 | tail -5; git checkout -q 02ff244 -- evals/reports/calibration.json",
 "description": "Mutate sentence and source_commit in scratch clone calibration file and run selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:35:07.507Z

**tool result**
````
M-B sentence now: Verified items matched the record 83/84 times in testing on the fixture backend (live mode
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
1 failed, 83 passed, 1116 deselected in 6.16s
=== M-C
M-C source_commit set to 11111111
........ss..                                                             [100%]
=========================== short test summary info ============================
SKIPPED [1] tests/unit/test_eval_runner.py:638: no git history here (shallow or exported tree)
SKIPPED [1] tests/unit/test_eval_runner.py:647: source commit not available in this checkout
82 passed, 2 skipped, 1116 deselected in 4.66s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:35:18.309Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['by_type']['amount']['verified']['matched']=8\njson.dump(d,open(p,'w'),indent=1)\nprint('M-D by_type amount verified matched -> 8; by_state untouched =', d['by_state']['verified']['matched'])\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; echo \"=== M-E\"; git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); k=sorted(d['hashes'])[0]; d['hashes'][k]='0'*64\njson.dump(d,open(p,'w'),indent=1)\nprint('M-E stale hash for', k)\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; echo \"=== M-F not_scored\"; git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['not_scored']['total']=0\njson.dump(d,open(p,'w'),indent=1)\nprint('M-F not_scored.total -> 0 (was 0 already)')\n\"; git checkout -q 02ff244 -- evals/reports/calibration.json; echo \"=== M-G source_tree_clean false\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['source_tree_clean']=False\njson.dump(d,open(p,'w'),indent=1)\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; git checkout -q 02ff244 -- evals/reports/calibration.json; echo restored: $(git status --porcelain --untracked-files=no)",
 "description": "Run by_type, stale hash, and clean-flag hand-edit mutations in scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:35:18.364Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to  8; by_state untouched =,)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:35:24.830Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['by_type']['amount']['verified']['matched']=8\njson.dump(d,open(p,'w'),indent=1)\nprint('M-D by_type amount verified matched set to 8; by_state verified matched is', d['by_state']['verified']['matched'])\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; echo \"=== M-E\"; git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); k=sorted(d['hashes'])[0]; d['hashes'][k]='0'*64\njson.dump(d,open(p,'w'),indent=1)\nprint('M-E stale hash set for', k)\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; echo \"=== M-G clean flag false\"; git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\np='evals/reports/calibration.json'\nd=json.load(open(p)); d['source_tree_clean']=False\njson.dump(d,open(p,'w'),indent=1)\nprint('M-G source_tree_clean set to False')\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; git checkout -q 02ff244 -- evals/reports/calibration.json; echo restored: [$(git status --porcelain --untracked-files=no)]",
 "description": "Run by_type, stale hash, and clean-flag hand-edit mutations in scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:35:44.535Z

**tool result**
````
M-D by_type amount verified matched set to 8; by_state verified matched is 83
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
2 failed, 82 passed, 1116 deselected in 6.11s
=== M-E
M-E stale hash set for app/llm/lexicon.yaml
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
1 failed, 83 passed, 1116 deselected in 6.09s
=== M-G clean flag false
M-G source_tree_clean set to False
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
1 failed, 83 passed, 1116 deselected in 6.20s
restored: [M evals/reports/calibration.json]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:35:56.314Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && git checkout -q 02ff244 -- evals/reports/calibration.json && git diff --cached --quiet 02ff244 -- evals/reports/calibration.json && echo \"clone calibration.json == 02ff244 version\" ; grep -n 'g\\[\"class\"\\]\\|CAL_SMALL_N = \\|i in owned or any\\|on the {backend} backend\\|Not scored' evals/run.py",
 "description": "Locate mutation targets in scratch clone evals/run.py"
}
````

### User / tool · 2026-11-02T04:35:56.451Z

**tool result**
````
clone calibration.json == 02ff244 version
163:                 and a.get("kind") == g["class"] and a.get("value_cents") == cents for a in prod)
206:        per[c["type"]]["cands_ok"] += i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", []))
243:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
271:                    and a.get("kind") == g["class"] and a.get("value_cents") == cents):
279:            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
317:        return f" on the {backend} backend ({', '.join(parts)})"
325:                                   else f"No {s.replace('_', ' ')} items were seen in testing on the {backend} backend.")
327:            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
335:                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:01.180Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nmut() { $PY -c \"\nimport sys\np='evals/run.py'; s=open(p).read(); old, new = sys.argv[1], sys.argv[2]\nassert s.count(old)==1, ('count', s.count(old))\nopen(p,'w').write(s.replace(old,new)); print('mutant applied')\n\" \"$1\" \"$2\" && env -u LLM_BACKEND -u ENABLE_LIVE $PY -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -4; git checkout -q -- evals/run.py; }\necho \"=== C1 drop class term in amount match (line 271)\"; mut ' and a.get(\"kind\") == g[\"class\"] and a.get(\"value_cents\") == cents):' ' and a.get(\"value_cents\") == cents):'\necho \"=== C2 drop backend from caveat\"; mut \"return f\\\" on the {backend} backend ({', '.join(parts)})\\\"\" \"return f\\\" ({', '.join(parts)})\\\"\"\necho \"=== C3 small-sample threshold 30 -> 5\"; mut \"CAL_SMALL_N = 30 \" \"CAL_SMALL_N = 5 \"\necho \"=== C4 drop tolerated term (line 279)\"; mut 'i in owned or any(tolerated_match(t, c) for t in exp.get(\"tolerated\", [])))' 'i in owned)'\necho \"=== C5 drop not-scored sentence\"; mut \"            sentences[\\\"overall\\\"][s] += f\\\" Not scored: {not_scored['total']} produced items without a usable state.\\\"\" \"            pass\"\ngit status --porcelain --untracked-files=no",
 "description": "Apply code mutants in scratch clone and run selector for each",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:36:35.097Z

**tool result**
````
=== C1 drop class term in amount match (line 271)
mutant applied
tests/unit/test_eval_runner.py:554: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_amount_class_is_part_of_the_match
1 failed, 83 passed, 1116 deselected in 6.52s
=== C2 drop backend from caveat
mutant applied
FAILED tests/unit/test_eval_runner.py::test_every_sentence_names_the_backend_and_the_golden_set[fixture-True]
FAILED tests/unit/test_eval_runner.py::test_every_sentence_names_the_backend_and_the_golden_set[claude-cli-False]
FAILED tests/unit/test_eval_runner.py::test_every_sentence_names_the_backend_and_the_golden_set[anthropic-api-False]
4 failed, 80 passed, 1116 deselected in 6.59s
=== C3 small-sample threshold 30 -> 5
mutant applied
tests/unit/test_eval_runner.py:528: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_small_sample_boundary_is_29_vs_30_cases
1 failed, 83 passed, 1116 deselected in 6.28s
=== C4 drop tolerated term (line 279)
mutant applied
tests/unit/test_eval_runner.py:564: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_tolerated_flag_counts_as_matched
1 failed, 83 passed, 1116 deselected in 6.10s
=== C5 drop not-scored sentence
mutant applied
tests/unit/test_eval_runner.py:603: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently
1 failed, 83 passed, 1116 deselected in 6.33s
M  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:41.749Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\n$PY -c \"\np='evals/run.py'; s=open(p).read(); old='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"state\\\": f.get(\\\"state\\\"), \\\"evidence\\\"'; new='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"evidence\\\"'\nassert s.count(old)==1, s.count(old); open(p,'w').write(s.replace(old,new)); print('C6 applied: candidate state dropped')\n\" && env -u LLM_BACKEND -u ENABLE_LIVE $PY -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; git checkout -q -- evals/run.py; echo \"clone clean: [$(git status --porcelain --untracked-files=no)]\"; cd /Users/arsis/zlayt-pm-project && echo \"--- board T-096:\" && python3 tools/board.py show T-096 2>&1 | head -12; echo \"--- app grep:\" && grep -rn \"calibration\" app/ --include=*.py | head -5; echo \"--- % in calibration sentence code:\" && git show 823b718:evals/run.py | sed -n 300,340p | grep -n '%' ; echo \"(end)\"",
 "description": "Run candidate-state mutant, check T-096 card and app routes for calibration",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:36:41.807Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git checkout` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:46.822Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\np='evals/run.py'; s=open(p).read(); old='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"state\\\": f.get(\\\"state\\\"), \\\"evidence\\\"'; new='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"evidence\\\"'\nassert s.count(old)==1, s.count(old); open(p,'w').write(s.replace(old,new)); print('C6 applied: candidate state dropped')\n\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; git checkout -q -- evals/run.py; echo \"clone status: [$(git status --porcelain --untracked-files=no)]\"",
 "description": "Apply candidate-state mutant in scratch clone and run selector",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:36:46.882Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git checkout` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:52.774Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cp $SCR/clone/evals/run.py $SCR/run_pristine_823b718.py && cmp $SCR/run_pristine_823b718.py $SCR/clone/evals/run.py && echo pristine-copy-ok && grep -c 'def git_source' $SCR/run_pristine_823b718.py",
 "description": "Save pristine copy of scratch clone evals/run.py for restore"
}
````

### User / tool · 2026-11-02T04:36:52.888Z

**tool result**
````
pristine-copy-ok
1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:36:56.266Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; cd $SCR/clone && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\np='evals/run.py'; s=open(p).read(); old='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"state\\\": f.get(\\\"state\\\"), \\\"evidence\\\"'; new='        c = {\\\"type\\\": f[\\\"type\\\"], \\\"evidence\\\"'\nassert s.count(old)==1, s.count(old); open(p,'w').write(s.replace(old,new)); print('C6 applied: candidate state dropped')\n\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -3; cp $SCR/run_pristine_823b718.py $SCR/clone/evals/run.py && cmp $SCR/run_pristine_823b718.py $SCR/clone/evals/run.py && echo \"restored pristine\"",
 "description": "Apply candidate-state mutant, run selector, restore pristine file",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T04:37:01.607Z

**tool result**
````
C6 applied: candidate state dropped
ERROR tests/unit/test_eval_runner.py::test_tampered_two_run_determinism_fails_bar_4_alone
ERROR tests/unit/test_eval_runner.py::test_full_report_carries_calibration_and_write_report_emits_calibration_json
35 failed, 44 passed, 1116 deselected, 5 errors in 4.79s
restored pristine
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:04.310Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-096 2>&1 | head -20",
 "description": "Show card T-096 read-only via board CLI"
}
````

### User / tool · 2026-11-02T04:37:04.441Z

**tool result**
````
---
id: "T-096"
title: "UI for suggestions and confidence: date-convention suggestion, dismissal suggestions, measured-precision line"
milestone: "M3"
role: "frontend"
status: "ready"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T04:30:07Z"
updated_at: "2026-11-02T04:30:16Z"
claimed_by: null
claimed_at: null
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "Dates-to-confirm row pre-selects the suggested convention with its reason and still requires one confirm (T-088); dismissal suggestion banner with Hide-similar action that the paralegal must click (T-089); 'Verified items matched the record N/M times in testing' line with small-sample note (T-090); e2e tests", "done": false, "evidence": null}
---
## Description
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:04.579Z

**tool call — Bash**
````
{
 "command": "grep -rln \"calibration\" app/ 2>/dev/null; echo \"grep-exit=$?\"; grep -n \"calibrat\" app/backend/api.py | head -5; echo \"---\"; python3 tools/board.py show T-090 2>&1 | sed -n 1,12p",
 "description": "Grep app for calibration references and show T-090 card header"
}
````

### User / tool · 2026-11-02T04:37:04.729Z

**tool result**
````
grep-exit=1
---
---
id: "T-090"
title: "Calibrated confidence: measured precision per state from evals"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:05Z"
updated_at: "2026-11-02T04:31:43Z"
claimed_by: "qa"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:27.217Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\nh=json.load(open('$SCR/outhead/calibration.json'))\nc=json.load(open('/Users/arsis/zlayt-pm-project/evals/reports/calibration.json'))\nprint('regen-from-02ff244-code keys missing vs committed:', sorted(set(c)-set(h)))\nprint('regen-from-02ff244-code by_state == committed:', h['by_state']==c['by_state'], '| sentences equal:', h['sentences']==c['sentences'])\nprint('committed header: backend', c['backend'], '| source_commit', c['source_commit'], '| clean', c['source_tree_clean'], '| hashes', len(c['hashes']))\n\"; grep -c '%' /Users/arsis/zlayt-pm-project/evals/reports/calibration.json; cd /Users/arsis/zlayt-pm-project && git show 823b718:evals/run.py | grep -n 'def build_calibration' ; git show 823b718:evals/run.py | awk 'NR>=290 && NR<=340 && /%/' | head -3; echo \"pct-hits-in-build_calibration-section: $(git show 823b718:evals/run.py | awk 'NR>=290 && NR<=340' | grep -c '%')\"",
 "description": "Compare header keys, verify no percent signs, and check percent in sentence builder"
}
````

### User / tool · 2026-11-02T04:37:27.270Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =290)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:31.349Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json\nh=json.load(open('$SCR/outhead/calibration.json'))\nc=json.load(open('/Users/arsis/zlayt-pm-project/evals/reports/calibration.json'))\nprint('regen-from-02ff244-code keys missing vs committed:', sorted(set(c)-set(h)))\nprint('regen-from-02ff244-code by_state equal:', h['by_state']==c['by_state'], '| sentences equal:', h['sentences']==c['sentences'])\nprint('committed header: backend', c['backend'], '| source_commit', c['source_commit'], '| clean', c['source_tree_clean'], '| hashes', len(c['hashes']))\n\"; echo \"percent signs in committed calibration.json: $(grep -c '%' /Users/arsis/zlayt-pm-project/evals/reports/calibration.json)\"; echo \"percent signs in 823b718 build_calibration section: $(cd /Users/arsis/zlayt-pm-project && git show 823b718:evals/run.py | sed -n 290,340p | grep -c '%')\"",
 "description": "Compare regenerated-at-02ff244 header keys and count percent signs"
}
````

### User / tool · 2026-11-02T04:37:31.521Z

**tool result**
````
regen-from-02ff244-code keys missing vs committed: ['hashes', 'not_scored', 'source_commit', 'source_tree_clean']
regen-from-02ff244-code by_state equal: True | sentences equal: False
committed header: backend fixture | source_commit 823b718817cacf6d38cf179724fd374ad09dffdf | clean True | hashes 12
percent signs in committed calibration.json: 0
percent signs in 823b718 build_calibration section: 0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:40.870Z

**tool call — Bash**
````
{
 "command": "git show 823b718:tests/unit/test_eval_runner.py | grep -n 'def test_committed\\|def test_git_source\\|def test_check_fresh\\|def test_amount_class\\|def test_tolerated\\|def test_record_warning\\|def test_items_without\\|def test_small_sample_boundary\\|def test_every_sentence\\|pytest.skip\\|env\\[\"PYTHONPATH\"\\]\\|fresh\\[\"source_tree_clean\"\\]'; echo ---; git show 823b718:evals/run.py | grep -n 'def git_source\\|def check_calibration\\|def check_fresh\\|CAL_SMALL_N = \\|def caveat\\|Not scored\\|on the {backend} backend (\\|\"source_commit\": (source\\|\\[\"state\"\\]\\|c\\[\"state\"\\], i in owned\\|def score_calibration'; echo ---; git show 2fca530 -- tests/unit/test_eval_runner.py | grep -c '^-def test_'; git show 2fca530 -- evals/run.py | grep -c '^-def git_source'",
 "description": "Collect line numbers for cited tests and code at 823b718"
}
````

### User / tool · 2026-11-02T04:37:41.033Z

**tool result**
````
272:def test_check_fresh_exits_1_when_a_hash_differs(tmp_path):
525:def test_small_sample_boundary_is_29_vs_30_cases():
536:def test_every_sentence_names_the_backend_and_the_golden_set(backend, recorded):
547:def test_amount_class_is_part_of_the_match():
557:def test_tolerated_flag_counts_as_matched():
567:def test_record_warning_flags_cannot_shift_flag_states():
582:def test_items_without_a_usable_state_are_counted_as_not_scored_not_dropped_silently():
629:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
635:def test_committed_calibration_source_commit_is_an_ancestor_of_head():
638:        pytest.skip("no git history here (shallow or exported tree)")
642:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
647:        pytest.skip("source commit not available in this checkout")
653:    env["PYTHONPATH"] = str(src)
660:    fresh["source_tree_clean"] = c["source_tree_clean"]                        # the export has no .git, so it cannot attest cleanliness itself
665:def test_git_source_reports_commit_and_dirtiness(tmp_path):
667:        pytest.skip("git missing")
680:def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
---
67:def git_source(root=ROOT):
243:CAL_SMALL_N = 30            # fewer cases (or items in a cell) than this is reported as a small sample, never rounded up to a rate
246:def score_calibration(exp, out, unscored=None):
279:            add("flag", c["state"], i in owned or any(tolerated_match(t, c) for t in exp.get("tolerated", [])))
281:        unscored["flag"] += sum(1 for c in cands if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES) - \
282:            sum(1 for c in uniq if c["type"] in FLAG_TYPES and c["state"] in CAL_STATES)       # duplicates of an earlier flag
310:    def caveat(total):
317:        return f" on the {backend} backend ({', '.join(parts)})"
327:            sentences["overall"][s] += f" Not scored: {not_scored['total']} produced items without a usable state."
338:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "hashes": hashes_ or {},
946:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
962:def check_calibration(path, root=ROOT):
---
11
1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:37:58.750Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; mkdir -p $SCR/cf && cd $SCR/clone && git checkout -q 02ff244 -- evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport sys, json, pathlib\nsys.path.insert(0, '$SCR/clone')\nfrom evals import run as R\nd = pathlib.Path('$SCR/cf')\ncal = json.load(open('$SCR/clone/evals/reports/calibration.json'))\n(d / 'latest.json').write_text(json.dumps({'hashes': R.hashes()}))\ncal['sentences']['overall']['verified'] = 'Verified items matched the record 84/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'\n(d / 'calibration.json').write_text(json.dumps(cal))\nprint('check_fresh with edited sentence (by_state and by_type untouched):', R.check_fresh(d / 'latest.json'))\n\" ; echo \"exit=$?\"",
 "description": "Check whether check_fresh catches an edited served sentence"
}
````

### User / tool · 2026-11-02T04:37:58.932Z

**tool result**
````
check_fresh with edited sentence (by_state and by_type untouched): 0
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:03.999Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2; mkdir -p $E/regen-823b718-run1 $E/regen-823b718-run2 $E/regen-02ff244-code && cp $SCR/out1/calibration.json $SCR/out1/latest.json $E/regen-823b718-run1/ && cp $SCR/out2/calibration.json $E/regen-823b718-run2/ && cp $SCR/outhead/calibration.json $E/regen-02ff244-code/ && ls -R $E | head -20",
 "description": "Copy regeneration outputs into review evidence folder"
}
````

### User / tool · 2026-11-02T04:38:04.175Z

**tool result**
````
regen-02ff244-code
regen-823b718-run1
regen-823b718-run2

/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code:
calibration.json

/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/regen-823b718-run1:
calibration.json
latest.json

/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/regen-823b718-run2:
calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:12.162Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt",
 "content": "T-090 round-2 review evidence (staff-engineer-reviewer, claude-haiku-5-5)\n\nScratch clone: git clone of the project, then detached checkouts (scratchpad t090r2/clone).\nA git worktree was not used: board-guard blocks git worktree in the project tree.\n\n1. Regeneration from the source commit 823b718 (clean detached clone, fixture backend, env LLM_BACKEND/ENABLE_LIVE unset)\n   python -I -c \"sys.path.insert(0, <clone>); runpy.run_module('evals.run', run_name='__main__')\" --out <dir>   (run twice)\n   run1 and run2 calibration.json are identical except generated_at (cmp of grep -v generated_at: byte-identical).\n   Committed evals/reports/calibration.json vs run1 (generated_at removed, dict compare): True; vs run2: True.\n   Header of regenerated file: source_commit 823b718817cacf6d38cf179724fd374ad09dffdf, source_tree_clean true, backend fixture, 12 hashes.\n   overall verified: 83/84, overall needs_review: 10/10. Percent signs in committed file: 0.\n\n2. Selector at 823b718 code + 02ff244 calibration.json (scratch clone):\n   .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -> 84 passed, 1116 deselected, 0 skipped.\n\n3. Selector in the project working tree (HEAD 865b186 plus uncommitted edits by other workers):\n   84 passed, 1286 deselected. The eval files differ from HEAD (git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py: 2 files, 383 insertions).\n\n4. Selector at the file commit 02ff244 (code reverted by commit 2fca530):\n   71 passed, 1153 deselected. 2fca530 deleted 11 r2 tests (git show 2fca530 -- tests/unit/test_eval_runner.py | grep -c '^-def test_' = 11)\n   and git_source (git show 2fca530 -- evals/run.py | grep -c '^-def git_source' = 1).\n   git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py -> identical (HEAD carries the same reverted code).\n   Regeneration at 02ff244 code: keys missing vs committed = hashes, not_scored, source_commit, source_tree_clean; by_state equal; sentences differ.\n   Copy: regen-02ff244-code/calibration.json.\n\n5. Hand-edit mutants on the scratch clone (823b718 code, 02ff244 calibration.json). Selector result:\n   M-A  by_state.verified.matched +1 (84)                       -> 2 failed (regenerates_exactly, check_fresh_fails_on_hand_edit)  KILLED\n   M-B  sentences.overall.verified: \"recorded replies\" -> \"live model replies\"  -> 1 failed (regenerates_exactly)                    KILLED\n   M-C  source_commit = \"1\"*40 (non-existent commit)            -> 82 passed, 2 SKIPPED (test lines 638 and 647)                   SURVIVED (skip)\n   M-D  by_type.amount.verified.matched = 8 (by_state untouched) -> 2 failed                                                         KILLED\n   M-E  hashes[lexicon-or-first] = \"0\"*64                       -> 1 failed (regenerates_exactly)                                  KILLED\n   M-G  source_tree_clean = false                               -> 1 failed (header test)                                          KILLED\n   Sentence-only edit through check-fresh (python -I, R.check_fresh on a tmp dir, sentence 83/84 -> 84/84): returns 0           SURVIVED (check-fresh only checks sums and hashes)\n\n6. Code mutants on the 823b718 evals/run.py (restored from a saved pristine copy after each):\n   C1  drop class term (line 271)           -> 1 failed (test_amount_class_is_part_of_the_match)                        KILLED\n   C2  drop \"on the {backend} backend\" in caveat (line 317) -> 4 failed (test_every_sentence_names_the_backend, 3 params)     KILLED\n   C3  CAL_SMALL_N 30 -> 5 (line 243)       -> 1 failed (test_small_sample_boundary_is_29_vs_30_cases)                 KILLED\n   C4  drop tolerated term (line 279)       -> 1 failed (test_tolerated_flag_counts_as_matched)                        KILLED\n   C5  drop \"Not scored\" sentence (line 327) -> 1 failed (test_items_without_a_usable_state...)                         KILLED\n   C6  drop candidate state in to_candidates -> 35 failed, 5 errors (broad)                                              KILLED\n\n7. Card AC and app wiring:\n   board.py show T-096: AC 1 covers the \"measured-precision line (T-090)\" only; no backend route in its AC; status ready.\n   grep -rln calibration app/ -> no output, exit 1.\n"
}
````

### User / tool · 2026-11-02T04:38:12.280Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:23.432Z

**tool call — Bash**
````
{
 "command": "git show 823b718:evals/run.py > /dev/null && git show 823b718:evals/run.py | cmp - evals/run.py && echo \"working-tree evals/run.py identical to 823b718\"; git show 823b718:tests/unit/test_eval_runner.py | cmp - tests/unit/test_eval_runner.py && echo \"working-tree test_eval_runner.py identical to 823b718\"; git show 823b718:evals/reports/calibration.json | cmp - evals/reports/calibration.json; echo \"cmp calibration vs 823b718 exit=$?\"; ls reviews/ | grep 'T-090'",
 "description": "Check working-tree eval files against 823b718 and confirm review path is free"
}
````

### User / tool · 2026-11-02T04:38:23.614Z

**tool result**
````
stdin evals/run.py differ: char 27497, line 505
working-tree test_eval_runner.py identical to 823b718
stdin evals/reports/calibration.json differ: char 232, line 12
cmp calibration vs 823b718 exit=1
T-090-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:53.543Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r2.md",
 "content": "# T-090 round 2 review: calibrated confidence, provenance and majors (commits 823b718, 02ff244)\n\n**Verdict: fail.** The file itself reproduces exactly from its source commit 823b718, and the r1 majors are mostly fixed in the commit. But a later commit, 2fca530 (T-087/T-086, sits between 823b718 and 02ff244), deleted the r2 code and its 11 tests, so HEAD (865b186) has neither. That re-opens the r1 blocker at HEAD. Two more majors and two minors remain.\n\nMethod notes. The brief named `git worktree add`, which board-guard blocks in the project tree, so I used a scratch clone of the project with `git checkout --detach 823b718` (same result: a clean tree at 823b718). Scratch evidence is in `artifacts/review-evidence/T-090-staff-r2/` (`mutation-and-command-log.txt`, regenerated `calibration.json` copies). Regeneration used `python -I` with the scratch clone on `sys.path`, fixture backend, `LLM_BACKEND` and `ENABLE_LIVE` unset.\n\n## What reproduces\n\n| Check | Result |\n|---|---|\n| Regenerate at 823b718, run 1 vs committed file (generated_at removed) | equal |\n| Regenerate at 823b718, run 2 vs run 1 | byte-identical except generated_at |\n| Counts | verified 83/84, needs_review 10/10 (same as committed) |\n| Header | `source_commit` 823b718817cacf6d38cf179724fd374ad09dffdf, `source_tree_clean` true, `backend` fixture, 12 hashes (11 prompts + lexicon), `models` generator claude-sonnet-5-5 / judge claude-haiku-5-5 |\n| Percent signs in calibration.json and in the sentence builder | 0 |\n| `.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"` in the project tree | 84 passed, 1284 deselected, 0 skipped |\n| Same selector at 823b718 code with the 02ff244 file (scratch clone) | 84 passed, 0 skipped |\n| Same selector at 02ff244 (file commit, code as left by 2fca530) | 71 passed |\n\n## Finding 1 (blocker): the r2 fix is not in HEAD\n\n`git show 2fca530 -- evals/run.py` removes `git_source` and reverts the `unscored`/candidate-state changes. `git show 2fca530 -- tests/unit/test_eval_runner.py` removes 11 `^-def test_` lines, including `test_committed_calibration_regenerates_exactly_from_its_source_commit`. `git show 02ff244:evals/run.py | grep -c 'def git_source'` is 0. `git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py` exits 0, so HEAD carries the reverted code. The 84 passed in the project tree comes from uncommitted edits (`git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py`: 383 insertions, and the working-tree `evals/run.py` also differs from 823b718 at line 505). The card's AC evidence therefore cannot be reproduced from HEAD.\n\nThe consequence is the r1 blocker again. Running `python -m evals.run` at 02ff244 code overwrites calibration.json without `hashes`, `not_scored`, `source_commit` and `source_tree_clean`, and the sentences change (`artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json`). The committed header still names 823b718, and nothing in HEAD can check it.\n\nWhy blocker and not major: the shipped provenance guard (the traceability the card exists for) is absent from the committed code, so a rerun at HEAD does not produce the file it ships. I cannot downgrade this because the fix lives in another card's commit.\n\n## Finding 2 (major): a forged source_commit passes by skipping\n\n`tests/unit/test_eval_runner.py:635-638` skips the ancestor test when `cat-file -e <source_commit>^{commit}` fails, labelled \"no git history here\". `:642-647` skips the regeneration test with \"source commit not available in this checkout\". So a hand-edited header naming a commit that does not exist passes, with 2 skips. Mutant M-C (`source_commit` = `\"1\"*40`, 823b718 code, 02ff244 file): `82 passed, 2 skipped`. The brief asked that hand-edits fail the tests. This one does not.\n\n## Finding 3 (major): the served field has no owner\n\nCard AC 1 (board/cards/T-090.md) now reads \"served field and UI line are carried by T-096 (frontend)\". `python3 tools/board.py show T-096` shows its AC 1 covers only the \"Verified items matched the record N/M times in testing\" line \"(T-090)\". No backend route is in any AC. `grep -rln calibration app/` returns nothing (exit 1). The r1 fix asked that the served field be linked to a backend card; the narrowing removed the link rather than adding one.\n\n## Finding 4 (minor): check-fresh passes an edited sentence\n\nThe card says check-fresh validates calibration.json. `evals/run.py:962` (`check_calibration`) checks only that by_state equals the sum of by_type and that hashes match the files. With the sentence changed from 83/84 to 84/84 and counts untouched, `R.check_fresh` returns 0 (log item 5). The regeneration test catches it, but only under pytest with git history.\n\n## Finding 5 (minor): the clean flag is not checked by the regeneration test\n\n`tests/unit/test_eval_runner.py:660` sets `fresh[\"source_tree_clean\"] = c[\"source_tree_clean\"]`, copying the file's own value into the comparison. Only the header test (`:629-633`) pins it to true. A file generated from a dirty tree that forges `true` passes both tests. This is minor because the committed file's commit is clean, but the header field is not verified.\n\n## Majors from r1: status\n\n- Blocker (not reproducible): fixed in 823b718/02ff244 (regeneration reproduces); reopened at HEAD by Finding 1.\n- Major 2 (AC 1 closed with UI unbuilt): narrowed to the eval side; the UI is claimed by T-096, but the served field is not (Finding 3).\n- Major 3 (amount class not tested): fixed. Mutant C1 (drop class term) turns `test_amount_class_is_part_of_the_match` red.\n- Major 4 (sentences name no backend): fixed. Mutant C2 (drop backend from caveat) turns 3 parametrized sentence tests red. The fixture sentence reads \"on the fixture backend (recorded replies, 10 golden cases, small sample)\".\n- Minors: 29/30 boundary (C3 killed), tolerated flag (C4 killed), not-scored disclosure (C5 killed), record_warning alignment (C6, candidate state dropped, killed broadly), check-fresh covers calibration.json (partly; Finding 4).\n\nHand-edit mutants on the 823b718 code with the 02ff244 file: count in by_state (killed, 2 tests), sentence text (killed), count in by_type only (killed, 2 tests), stale hash (killed), clean flag false (killed). Only the forged source_commit survives (Finding 2).\n\n## Outside my lens\n\nThe ship bar is not met on the fixture run (`4_no_invented_facts`, determinism and judge controls not measured). Those are existing ship-bar items, not T-090. I did not judge the frontend wording.\n\n```json\n{\"card\": \"T-090\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commits 823b718 (evals/run.py, tests/unit/test_eval_runner.py) and 02ff244 (evals/reports/calibration.json); HEAD 865b186 checked for the code; scratch clone of the project at detached 823b718 and 02ff244 (git worktree blocked by board-guard); no app URL (no calibration route or UI exists: grep -rln calibration app/ returns nothing); sample case = fixture backend over the 10 golden cases\",\n \"exercised\": [\n  \"read personas/staff-engineer.md, reviews/T-090-staff-engineer.md (r1), board/cards/T-090.md, board/cards/T-096.md via board.py show\",\n  \"git show --stat 823b718, 02ff244, 2fca530; git show 823b718 -- evals/run.py and -- tests/unit/test_eval_runner.py; git show 2fca530 -- evals/run.py and -- tests/unit/test_eval_runner.py (11 removed test defs, git_source removed)\",\n  \"git clone of the project into scratchpad t090r2/clone, git checkout --detach 823b718; regenerated twice: python -I -c runpy evals.run --out <scratch>/out1 and out2 (fixture); out1 and out2 equal to each other and to evals/reports/calibration.json ignoring generated_at (dict compare True, cmp of lines without generated_at byte-identical)\",\n  \"header check on committed calibration.json: backend fixture, source_commit 823b718817cacf6d38cf179724fd374ad09dffdf, source_tree_clean true, 12 hashes, models; grep -c '%' calibration.json = 0; percent in build_calibration section of 823b718 = 0\",\n  \".venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' in the project tree: 84 passed, 1284 deselected, 0 skipped\",\n  \"same selector at 823b718 code with the 02ff244 calibration.json in the scratch clone: 84 passed; at 02ff244 (clone detached): 71 passed; at 823b718 with its own pre-r2 file: 3 failed, 81 passed (stale file, not recorded further)\",\n  \"regeneration at 02ff244 code (scratch clone): keys missing vs committed = hashes, not_scored, source_commit, source_tree_clean; by_state equal; sentences differ (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json)\",\n  \"git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exit 0; git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py: 383 insertions; cmp working-tree evals/run.py vs 823b718: differ at line 505; cmp working-tree test_eval_runner.py vs 823b718: identical\",\n  \"hand-edit mutants in scratch clone (823b718 code, 02ff244 file): by_state count +1 -> 2 failed; sentence text -> 1 failed; by_type count -> 2 failed; stale hash -> 1 failed; source_tree_clean false -> 1 failed; source_commit = 1*40 -> 82 passed, 2 skipped (test_eval_runner.py:638, :647)\",\n  \"code mutants in scratch clone evals/run.py (restored from saved pristine copy): drop class term line 271 -> 1 failed; drop backend in caveat line 317 -> 4 failed; CAL_SMALL_N 30->5 line 243 -> 1 failed; drop tolerated term line 279 -> 1 failed; drop Not-scored sentence line 327 -> 1 failed; drop candidate state in to_candidates -> 35 failed, 5 errors\",\n  \"check_fresh(latest.json) with edited sentence, python -I on scratch clone: returned 0\",\n  \"board.py show T-096 (AC 1 text, status ready); grep -rln calibration app/ (no output, exit 1)\",\n  \"full log: artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"counts_reproduce_from_commit\": 5, \"header_provenance_at_commit\": 4, \"provenance_guard_at_HEAD\": 1, \"hand_edit_detected\": 3, \"r1_majors_fixed\": 3, \"ac_closed_honestly\": 2, \"no_bare_percent\": 5, \"mutants_killed\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"The r2 provenance fix and its tests are reverted at HEAD by commit 2fca530; the card's test evidence is not reproducible from HEAD\",\n   \"evidence\": \"git show 2fca530 -- tests/unit/test_eval_runner.py removes 11 test defs (grep -c '^-def test_' = 11), including test_committed_calibration_regenerates_exactly_from_its_source_commit; git show 2fca530 -- evals/run.py removes def git_source (git show 02ff244:evals/run.py | grep -c 'def git_source' = 0). git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exits 0, so HEAD has the reverted code. Selector at 02ff244: 71 passed (no r2 tests). Project-tree 84 passed comes from uncommitted edits (git diff --stat HEAD: evals/run.py and tests/unit/test_eval_runner.py, 383 insertions). Regeneration at 02ff244 code omits hashes, not_scored, source_commit, source_tree_clean (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json).\",\n   \"why_it_matters\": \"This is the r1 blocker again. The served calibration.json names a source commit whose provenance guard is no longer in the shipped code, so a rerun of python -m evals.run at HEAD overwrites the file with one that has no provenance. The tests that were supposed to fail on a hand edit do not exist at HEAD, so the card's '84 passed' cannot be reproduced from the commits it lists. The 823b718 and 02ff244 commits themselves are correct; the loss happened after them.\",\n   \"fix\": \"Restore the 823b718 versions of evals/run.py and tests/unit/test_eval_runner.py in a new commit that stages those two paths explicitly (git show 823b718:evals/run.py and :tests/unit/test_eval_runner.py are the reference). Do not hand-merge the uncommitted working-tree edits, which differ from 823b718 in evals/run.py (first difference at line 505). Ask the author of 2fca530 to stage by explicit path; the commit staged a stale evals/run.py and test file.\",\n   \"acceptance_test\": \"git show HEAD:evals/run.py | grep -c 'def git_source' is at least 1; at the new HEAD, .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' reports 84 passed with 0 skipped from a clean tree; a regeneration at HEAD (fixture, --out) equals evals/reports/calibration.json ignoring generated_at.\"},\n  {\"severity\": \"major\",\n   \"title\": \"A forged source_commit that names no existing commit passes the two provenance tests by skipping\",\n   \"evidence\": \"tests/unit/test_eval_runner.py:635-638 (skip 'no git history here (shallow or exported tree)' when cat-file -e <source_commit>^{commit} fails) and :642-647 (skip 'source commit not available in this checkout'). Mutant on scratch clone (823b718 code, 02ff244 file, source_commit set to '1'*40): .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 82 passed, 2 skipped.\",\n   \"why_it_matters\": \"The brief requires the tests to fail when the file is hand-edited. A header that cites a commit which does not exist is the provenance lie the card was opened to stop, and it is reported green. The skip conflates 'no git at all' (a legitimate export) with 'the cited commit is missing' (a fabricated header).\",\n   \"fix\": \"Skip only when there is no git repository (git rev-parse --git-dir fails). When a repository exists and the cited commit is missing, or the commit is not an ancestor of HEAD, fail with the commit name.\",\n   \"acceptance_test\": \"Set source_commit to '1'*40 in calibration.json; the selector reports at least one failed test and no skip for the provenance tests.\"},\n  {\"severity\": \"major\",\n   \"title\": \"The served calibration field has no owner after AC 1 was narrowed\",\n   \"evidence\": \"board/cards/T-090.md AC 1 evidence: 'served field and UI line are carried by T-096 (frontend)'. python3 tools/board.py show T-096 shows AC 1: 'Dates-to-confirm row ... Verified items matched the record N/M times in testing line with small-sample note (T-090); e2e tests', done false, status ready. No AC names a backend route or a read of evals/reports/calibration.json. grep -rln calibration app/ returns no files (exit 1).\",\n   \"why_it_matters\": \"The r1 major asked for the served field to be linked to a backend card. The narrowing moved the UI line to T-096 but left the backend route with no card and no AC, so the sentence the paralegal reads has no path to the screen. The card's AC is narrower and honest about the UI, but the handoff to the backend is unowned.\",\n   \"fix\": \"Add an explicit backend AC (route that returns the calibration.json fields, or null when the file is absent, read-only) to an existing backend card or a new one, and name it in T-090 AC 1 or the T-096 AC.\",\n   \"acceptance_test\": \"board.py show <owning card> lists the route AC; grep -rn calibration app/backend finds the route; curl of the route returns the sentences.overall.verified string from evals/reports/calibration.json verbatim.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"check-fresh exits 0 for an edited sentence; it validates sums and hashes only\",\n   \"evidence\": \"evals/run.py:962 check_calibration checks by_state vs sum of by_type and hashes vs files. Scratch-clone repro (python -I, R.check_fresh on a tmp dir with latest.json and the edited calibration.json, verified sentence changed to '84/84 ...'): returned 0.\",\n   \"why_it_matters\": \"The card says check-fresh validates calibration.json. A hand-edited sentence, which the UI renders verbatim, passes the freshness command. Only the pytest regeneration test catches it, and that test needs git history.\",\n   \"fix\": \"Add the calibration.json sentences and not_scored to check_calibration, or regenerate the sentences inside check_calibration from by_state and by_type and compare.\",\n   \"acceptance_test\": \"Edit sentences.overall.verified in a copy of calibration.json; R.check_fresh returns 1.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes\",\n   \"evidence\": \"tests/unit/test_eval_runner.py:660 fresh[\\\"source_tree_clean\\\"] = c[\\\"source_tree_clean\\\"] (823b718 numbering). Only the header test (:629-633) asserts the value is True.\",\n   \"why_it_matters\": \"The clean flag is the only evidence the counts came from an unmodified tree. The regeneration test cannot check it, so a file produced from a dirty tree that says true is indistinguishable from a clean one.\",\n   \"fix\": \"Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.\",\n   \"acceptance_test\": \"A calibration.json whose recorded tree hash differs from the source commit's tree fails the regeneration test.\"}\n ],\n \"whats_right\": [\n  \"calibration.json regenerates exactly from its source commit 823b718 (two runs identical except generated_at; counts 83/84 and 10/10), and the header records source_commit, source_tree_clean true, backend fixture and 12 prompt/lexicon hashes.\",\n  \"Hand edits to by_state counts, by_type counts, the sentence text, the hashes and the clean flag each turn at least one test red at 823b718 (mutants M-A, M-B, M-D, M-E, M-G).\",\n  \"Sentences name the backend and '(recorded replies, N golden cases)' for the fixture, no percent sign appears anywhere, and the r1 amount-class, tolerated, 29/30 boundary and not-scored mutants are each killed.\"\n ],\n \"questions_for_chris\": [\n  \"Which card should own the backend route that serves calibration.json: a new backend card, or an AC added to T-096?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T04:38:53.712Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:38:57.594Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-090-staff-engineer-r2.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nrule='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('keys ok:', all(k in d for k in ['card','persona','model','scope','exercised','verdict','scores','findings','whats_right','questions_for_chris']))\nprint('verdict', d['verdict'], '| rule gives', rule, '| severities', sev, '| whats_right', len(d['whats_right']))\nprint('model', d['model'], '| persona', d['persona'], '| card', d['card'])\n\"",
 "description": "Validate the review JSON block parses and verdict follows the rule"
}
````

### User / tool · 2026-11-02T04:38:57.650Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No escaped character) | command: /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c "
import json,re
t=open('reviews/T-090-staff-engineer-r2.md').read()
blocks=re.findall(r'\`\`\`json\n(.*?)\n\`\`\`', t, re.S)
print('json blocks:',
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:00.170Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/check_json.py 2>&1 | head -3; echo \"(checked)\"",
 "description": "Placeholder check to confirm shell is responsive"
}
````

### User / tool · 2026-11-02T04:39:00.297Z

**tool result**
````
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python: can't open file '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t090r2/check_json.py': [Errno 2] No such file or directory
(checked)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:03.196Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/check_review_json.py",
 "content": "import json\nimport re\nimport sys\n\ntext = open(sys.argv[1], encoding=\"utf-8\").read()\nfence = chr(96) * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nneed = [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]\nprint(\"keys present:\", all(k in d for k in need))\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict:\", d[\"verdict\"], \"| rule gives:\", rule, \"| match:\", d[\"verdict\"] == rule)\nprint(\"severities:\", sev)\nprint(\"whats_right lines:\", len(d[\"whats_right\"]))\nprint(\"card:\", d[\"card\"], \"| persona:\", d[\"persona\"], \"| model:\", d[\"model\"])\nprint(\"score values in 1-5:\", all(1 <= v <= 5 for v in d[\"scores\"].values()))\n"
}
````

### User / tool · 2026-11-02T04:39:03.305Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-090-staff-r2/check_review_json.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:04.502Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-090-staff-r2/check_review_json.py reviews/T-090-staff-engineer-r2.md",
 "description": "Parse review JSON block and check verdict against the rule"
}
````

### User / tool · 2026-11-02T04:39:04.626Z

**tool result**
````
json blocks: 1
keys present: True
verdict: fail | rule gives: fail | match: True
severities: ['blocker', 'major', 'major', 'minor', 'minor']
whats_right lines: 3
card: T-090 | persona: staff-engineer-reviewer | model: claude-haiku-5-5
score values in 1-5: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:06.646Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; echo \"exit=$?\"",
 "description": "Run read-only board validator"
}
````

### User / tool · 2026-11-02T04:39:06.803Z

**tool result**
````
ok (96 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:10.899Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:39:10.907Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:13.469Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command",
 "new_string": "- (T-090 r2, 2026-11-01) `->` inside a `python -c` print string is read as a redirect (\"redirect to 84\"); `git worktree` is denied in the project (\"allowed only in scratch repos under /tmp\"). Use `git clone <project> <scratch>/clone` then `git checkout --detach <sha>` inside the clone. `git checkout` in the clone was denied once when the Bash cwd had been the project; split the call and use a saved pristine copy plus `cp` to restore a mutated file. `-I` runs need `sys.path.insert(0, clone)` plus `runpy.run_module` because `-I` drops cwd from sys.path.\n- (T-080 r3, 2026-11-02) board-guard reads a `>` inside a Bash command"
}
````

### User / tool · 2026-11-02T04:39:13.607Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:18.056Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md",
 "old_string": "**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.",
 "new_string": "**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.\n\nT-090 r2 (commits 823b718 code, 02ff244 file; review reviews/T-090-staff-engineer-r2.md): fail, 1 blocker, 2 majors, 2 minors.\n- **A later commit reverted the fix.** 2fca530 (another card, committed 15 s after 823b718, before 02ff244) deleted git_source and the 11 r2 tests. HEAD evals/ and test file == 02ff244. Project-tree \"84 passed\" was uncommitted. Always check `git diff --quiet <fix> HEAD -- <files>` and `git log --oneline <fix>..HEAD -- <files>` before accepting a fix commit as shipped.\n- **Skip is a silent pass for a forged header.** Provenance tests skip on \"no git history\" and on \"commit not available\", so a source_commit naming a non-existent commit reports 2 skipped and no failure. Skips must be scoped to \"no .git\"; a missing cited commit must fail.\n- **check-fresh validates sums and hashes only.** An edited served sentence returns 0 from check_fresh; only the pytest regeneration test catches it.\n- **Scratch method that worked:** clone, detached checkout of the commit, regenerate with `python -I` plus sys.path insert and runpy, compare ignoring generated_at, then mutate the clone's file and run the selector per mutant. Restore by copying a saved pristine file (not git checkout).\n- Narrowing an AC to \"UI is under T-096\" left the backend serve route with no AC anywhere (grep for the route name in the owning card)."
}
````

### User / tool · 2026-11-02T04:39:18.191Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t090_calibration_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:19.986Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible from commit, AC closed with UI unbuilt, class/tolerated/threshold mutants survive",
 "new_string": "- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83: committed counts not reproducible; r2 823b718/02ff244: fix reverted at HEAD by 2fca530, forged source_commit skips"
}
````

### User / tool · 2026-11-02T04:39:20.116Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:39:22.720Z

T-090 r2 verdict is fail: `calibration.json` reproduces from 823b718 (83/84, 10/10), but commit 2fca530 reverted the r2 code and its 11 tests at HEAD (blocker), a forged source_commit passes by skipping and the served field has no owner (majors); review at /Users/arsis/zlayt-pm-project/reviews/T-090-staff-engineer-r2.md.
