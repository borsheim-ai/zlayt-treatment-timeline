# Subagent: T-169 r2 quick check (T-169 r2 quick check)

Source: `agent-a7cbe40c84fc3db4d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T17:17:16.451Z

Run the round-2 check of board card T-169 (commit 6e1294f, test-only) in /Users/arsis/zlayt-pm-project. Read reviews/T-169-staff-engineer.md and `python3 tools/board.py show T-169`.

In a fresh `git clone`:
- The new tests tie calibration.json to report 20261102T164038Z.md and to run folder runs/20261102T161327Z.
- Forging a count in calibration.json makes them fail; prove it on a copy.
- The minors are fixed.
- tests/unit/test_eval_runner.py passes.

Major 1, the e2e contract ids, is owned by T-166; don't count it here.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-169-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:18.579Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T17:17:18.592Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:18.785Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer.md"
}
````

### User / tool · 2026-11-02T17:17:18.798Z

**tool result**
````
1	# T-169 review (staff-engineer-reviewer), commit 5ed37ad
2	
3	Scope: `tests/unit/test_eval_runner.py` at 5ed37ad only (test-only card). Reviewed in a fresh `git clone` in the session scratchpad, detached at 5ed37ad. The project tree's HEAD has moved to 8398bee; findings are for 5ed37ad.
4	
5	Verdict: **changes** (0 blockers, 2 majors, 2 minors, 1 nit). No §5 red flag: the skip is visible in pytest output with a written reason, nothing swallows errors, no money or LLM arithmetic, and the diff adds no network call or sleep.
6	
7	What I ran (details in `artifacts/review-evidence/T-169-staff-engineer/`):
8	- Header positive: `pytest -k committed_calibration_header` on the committed live header (backend claude-cli, source_tree_clean true): PASSED.
9	- Dirty-tree negative: edited the clone's `evals/reports/calibration.json` to `source_tree_clean=false` with backend claude-cli. Header test FAILED at line 805 with `assert (False is True)`. Restored bytes; header test PASSED again.
10	- Regeneration skip: on the live header it is SKIPPED at line 853 with reason "committed calibration is a live claude-cli measurement; exact regeneration needs the live backend".
11	- Regeneration on a real fixture header (`git show f3ac48f:evals/reports/calibration.json`, backend fixture, source 6fa8ecc): the test ran (not skipped) and PASSED.
12	- Mutant A (clean-tree clause removed from line 805): `test_calibration_header_check_still_fails_on_a_dirty_tree` FAILED, "DID NOT RAISE". The guard is real.
13	- Mutant B (live skip at line 850 removed): regen test FAILED on the live header. The skip is the only thing that hides this mismatch; it is needed offline, but it means no test checks the live counts.
14	- `pytest tests/unit/test_eval_runner.py -q`: 108 passed, 1 skipped (the regen skip).
15	- `pytest tests/unit -q` on the clone at 5ed37ad: 1 failed, 5329 passed, 2 skipped. The failure is `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared`, not in this card's file.
16	
17	## Findings
18	
19	**F1 major, AC 1 says "unit suite green" and it is red at the card commit.** The card's evidence cites only `test_eval_runner.py` (108 passed, 1 skipped). The full unit suite at 5ed37ad is 1 failed, 5329 passed, 2 skipped; the failure is `test_every_test_id_is_declared` at `tests/unit/test_e2e_contract.py:13`. That red is not caused by this commit, but the AC as written is not met. Fix: either fix the e2e id declaration in its owner's card, or narrow the AC to the file and say so. Acceptance test: `pytest tests/unit -q` returns rc 0 at the card commit, or the AC text names the file.
20	
21	**F2 major, the skip removes the only count-level check on the live calibration, and the header cites no report.** The handoff says the live counts are covered by "the live report it cites". `evals/reports/calibration.json` has no report field. The tracked live report `evals/reports/20261102T164038Z.md` does match today (source 312efe6, verified 82/83, needs review 11/11), but only by timestamp. Probe 2 shows that editing one served sentence (82/83 to 83/83) is caught by `test_committed_report_is_valid_when_present` and `test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes`. A coordinated edit of counts and sentences that stays internally consistent is not caught by any test; I did not run that mutant. Fix: record the report path and its sha256 in the header, and add a test that the cited report's counts equal the committed counts. Acceptance test: change `by_state.verified.matched` and the matching sentence together in a clone; the new test must fail.
22	
23	**F3 minor, the dirty-tree negative test passes for the wrong reason.** `tests/unit/test_eval_runner.py:820` uses `pytest.raises(AssertionError)` with no match, and the clean-tree assert at line 805 has no message. With `CAL_BACKENDS = ("fixture",)` (line 799), `-k dirty_tree` still passes (rc 0, "2 passed", probe2.log). The header test catches that case, but the negative test does not prove what its docstring says. Fix: add a message to line 805 and match it. Acceptance test: `CAL_BACKENDS = ("fixture",)` makes the dirty-tree test fail.
24	
25	**F4 minor, outside the card AC: the live numbers describe older code.** The live header is `source_commit` 312efe6. Seven commits separate it from 5ed37ad, and 56004f0 (T-168 r2: "every judge (j1-j4) and other step parses strictly") and 235e135 (T-168) change judge reply parsing. The served sentences therefore describe code that is no longer at HEAD. The ancestor test passes, so nothing flags this. Fix: record it in `memory/DECISIONS.md` or re-measure at HEAD. This is an orchestrator decision.
26	
27	**F5 nit, the skip condition is broader than its reason.** `tests/unit/test_eval_runner.py:850` skips for any `backend != "fixture"`, but the reason only covers claude-cli. The header test rejects unknown backends, so this is harmless today. Fix: skip only when `backend == "claude-cli"`.
28	
29	## What is right
30	- The clean-tree requirement holds for both backends: the dirty-tree header fails at line 805, and mutant A kills the negative test.
31	- The regen skip is visible (SKIPPED with a written reason at line 853), and the fixture branch still runs and passes on the real fixture header from f3ac48f.
32	- The diff adds no `except`, `float(`, `sleep(`, retry, or network call.
33	
34	```json
35	{"card": "T-169", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
36	 "scope": "commit 5ed37ad, tests/unit/test_eval_runner.py only; fresh clone at scratchpad T169_staff_r1/clone detached at 5ed37ad; project HEAD is 8398bee (moved); sample case n/a (unit tests)",
37	 "exercised": [
38	   "fresh git clone detached at 5ed37ad; pytest tests/unit/test_eval_runner.py -q -> 108 passed, 1 skipped (skip = regen test, line 853)",
39	   "pytest -k committed_calibration_header on committed live header (claude-cli, source_tree_clean true) -> PASSED",
40	   "edited clone copy of evals/reports/calibration.json to source_tree_clean=false -> header test FAILED at line 805 (AssertionError); restored bytes; PASSED again",
41	   "regen test on committed live header -> SKIPPED with reason 'committed calibration is a live claude-cli measurement; exact regeneration needs the live backend'",
42	   "regen test on real fixture header (git show f3ac48f:evals/reports/calibration.json, backend fixture, source 6fa8ecc) -> ran, PASSED (not skipped)",
43	   "mutant A: clean-tree clause removed at line 805 -> test_calibration_header_check_still_fails_on_a_dirty_tree FAILED (DID NOT RAISE)",
44	   "mutant B: live skip (line 850) removed -> regen test FAILED on the live header (counts differ under fixture backend)",
45	   "mutant C: CAL_BACKENDS without claude-cli (line 799) -> dirty-tree test still PASSED (wrong reason)",
46	   "full pytest tests/unit -q in clone at 5ed37ad -> 1 failed, 5329 passed, 2 skipped; failure test_e2e_contract.py::test_every_test_id_is_declared",
47	   "mutant D: one served sentence edited (82/83 -> 83/83), counts unchanged, full tests/unit -> 3 failed (incl. test_committed_report_is_valid_when_present and test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes)",
48	   "git ls-files evals/reports; grep of header keys; dated live report evals/reports/20261102T164038Z.md read (source 312efe6, 82/83 and 11/11)",
49	   "git rev-list --count 312efe6..5ed37ad = 7; commits 56004f0 and 235e135 touch judge parsing",
50	   "grep of the 5ed37ad diff for except, float(, sleep(, retry, network, model ids: only comment and docstring matches",
51	   "board.py show T-169 (AC 1 text and notes)",
52	   "probe scripts and logs: artifacts/review-evidence/T-169-staff-engineer/t169_probe.py, t169_probe2.py, probe.log, probe2.log"
53	 ],
54	 "verdict": "changes",
55	 "scores": {"dirty_tree_guard": 4, "live_regen_skip_provenance": 2, "suite_green_at_card_commit": 2, "negative_test_specificity": 3, "determinism_offline": 4, "honest_skips": 4},
56	 "findings": [
57	   {"severity": "major", "title": "AC 1 says unit suite green; full unit suite is red at 5ed37ad",
58	    "evidence": "probe2.log baseline: full tests/unit at 5ed37ad 1 failed, 5329 passed, 2 skipped; FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared (test_e2e_contract.py:13); board.py show T-169 AC 1 text ends 'unit suite green'",
59	    "why_it_matters": "The card's own AC is not met at its commit, and the evidence cites only one file.",
60	    "fix": "Fix the e2e id declaration in its owner's card, or narrow AC 1 to the file and name the red test.",
61	    "acceptance_test": "pytest tests/unit -q returns rc 0 at the card commit, or AC 1 text names the file scope"},
62	   {"severity": "major", "title": "Live skip leaves the served live counts with no test binding them to a run; the header cites no report",
63	    "evidence": "evals/reports/calibration.json header has no report field; tracked evals/reports/20261102T164038Z.md matches today (82/83, 11/11, source 312efe6) by timestamp only; probe2.log mutant D: served sentence edit caught by test_calibration_route.py::test_committed_report_is_valid_when_present and test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes; coordinated count+sentence edit not run",
64	    "why_it_matters": "The regen check was the test that caught unreproducible committed counts in T-090 r1. The skip removes it for the live file, and the handoff's 'live report it cites' does not exist in the header.",
65	    "fix": "Record report path and sha256 in the header; add a test that the cited report's counts equal calibration.json.",
66	    "acceptance_test": "In a clone, change by_state.verified.matched and its sentence together; the new test fails"},
67	   {"severity": "minor", "title": "Dirty-tree negative test passes for the wrong reason",
68	    "evidence": "tests/unit/test_eval_runner.py:820 'with pytest.raises(AssertionError):' (no match); line 805 clean-tree assert has no message; probe2.log C: CAL_BACKENDS=('fixture',) (line 799) -> rc 0, 2 passed",
69	    "why_it_matters": "The test's docstring claims it proves the clean-tree requirement; it does not, and only the positive test catches the wrong-backend case.",
70	    "fix": "Give the clean-tree assert at line 805 a message and match it in the test.",
71	    "acceptance_test": "With CAL_BACKENDS=('fixture',), test_calibration_header_check_still_fails_on_a_dirty_tree fails"},
72	   {"severity": "minor", "title": "Served live numbers were measured at a commit 7 behind 5ed37ad, before judge parsing changed (outside card AC)",
73	    "evidence": "calibration.json source_commit 312efe6; git rev-list --count 312efe6..5ed37ad = 7; 56004f0 'every judge (j1-j4) and other step parses strictly'; 235e135 T-168 parser change",
74	    "why_it_matters": "The served sentences describe code no longer at HEAD; the ancestor test passes, so nothing flags it.",
75	    "fix": "Record the gap in memory/DECISIONS.md or re-measure at HEAD (orchestrator decision).",
76	    "acceptance_test": "A decision entry or a fresh live header at HEAD exists and the served sentence matches it"},
77	   {"severity": "nit", "title": "Regen skip condition broader than its written reason",
78	    "evidence": "tests/unit/test_eval_runner.py:850 'if c[\"backend\"] != \"fixture\":' with reason text naming claude-cli only (line 853)",
79	    "why_it_matters": "Any future unknown backend would skip silently. Header test rejects unknown backends, so it is harmless today.",
80	    "fix": "Skip only when backend == 'claude-cli'.",
81	    "acceptance_test": "An unknown backend in the header makes the regen test run, not skip"}
82	 ],
83	 "whats_right": [
84	   "Dirty-tree header fails at tests/unit/test_eval_runner.py:805; mutant A kills the negative test",
85	   "Regen skip is visible with a written reason at line 853; the fixture branch still runs and passes on f3ac48f's header",
86	   "Diff adds no except, float(, sleep(, retry or network call"
87	 ],
88	 "questions_for_chris": ["Should the live calibration be re-measured at HEAD now that judge parsing changed (56004f0, 235e135), or is 312efe6 the accepted source for M2?"]}
89	```
90	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:19.025Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-169",
 "description": "Show board card T-169"
}
````

### User / tool · 2026-11-02T17:17:19.146Z

**tool result**
````
---
id: "T-169"
title: "Unit test test_committed_calibration_header_names_backend_and_a_clean_source_commit expects backend 'fixture' but the committed calibration.json is now the live claude-cli re-measure (7cfdb0b); accept the live backend (live is the intended source)"
milestone: "M2"
role: "qa"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T16:51:41Z"
updated_at: "2026-11-02T17:17:13Z"
claimed_by: "qa"
claimed_at: "2026-11-02T17:12:59Z"
rounds: 1
commits: ["5ed37ad", "6e1294f"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-169-staff-engineer.md", "at": "2026-11-02T17:12:52Z"}
ac:
  - {"n": 1, "text": "test accepts a live claude-cli calibration with a clean source commit; still fails on a dirty tree; unit suite green", "done": true, "evidence": "tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit accepts claude-cli; tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree passes; unit file 108 passed 1 skipped in source tree; fresh clone at 8398bee-descendant 21 passed 1 skipped"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T16:51:49Z qa: claimed
- 2026-11-02T16:51:58Z qa: Relaxed backend check to ('fixture','claude-cli'); clean-tree assertion unchanged; added dirty-header negative test. Running tests/unit/test_eval_runner.py.
- 2026-11-02T16:56:44Z qa: Fresh git clone (HEAD contains 5ed37ad): calibration tests 21 passed, 1 skipped (exact regen skipped for live claude-cli header, reason recorded). Dirty-header negative test passes.
- 2026-11-02T16:56:44Z qa: AC 1 checked: tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit accepts claude-cli; tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree passes; unit file 108 passed 1 skipped in source tree; fresh clone at 8398bee-descendant 21 passed 1 skipped
- 2026-11-02T16:56:44Z qa: moved in_progress -> in_review
- 2026-11-02T16:56:48Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T17:12:52Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-169-staff-engineer.md; round 1; findings:
    - [major] AC 1 says unit suite green; full unit suite is red at 5ed37ad — fix: Fix the e2e id declaration in its owner's card, or narrow AC 1 to the file and name the red test.
    - [major] Live skip leaves the served live counts with no test binding them to a run; the header cites no report — fix: Record report path and sha256 in the header; add a test that the cited report's counts equal calibration.json.
    - [minor] Dirty-tree negative test passes for the wrong reason — fix: Give the clean-tree assert at line 805 a message and match it in the test.
    - [minor] Served live numbers were measured at a commit 7 behind 5ed37ad, before judge parsing changed (outside card AC) — fix: Record the gap in memory/DECISIONS.md or re-measure at HEAD (orchestrator decision).
- 2026-11-02T17:12:52Z orchestrator: Major 1 (suite red) is the e2e contract ids owned by T-166, not this card. Major 2: bind the live calibration to its run - a test that the committed calibration.json names a run/report that exists in evals/reports (runs/<id>, report md) and that its counts equal that report's counts.
- 2026-11-02T17:12:52Z orchestrator: assigned: qa
- 2026-11-02T17:12:59Z qa: claimed
- 2026-11-02T17:17:02Z qa: r2: calibration.json has no run id; link derived from generated_at 2026-11-02T16:40:38Z -> evals/reports/20261102T164038Z.md (exists, commit 7cfdb0b). No runs/20261102T164038Z dir: run dirs are start-time ids, so the test checks the newest runs/<id> <= report id (runs/20261102T161327Z) holds all 10 cases. Counts (overall sentences + per-type table) and source commit/backend compared with the report; coordinated count+sentence forgery test fails as required. Minors: F3 fixed (assert messages, match; mutant CAL_BACKENDS=('fixture',) now fails), F5 skip only for claude-cli. F1 left to T-166; F4 orchestrator decision. Fresh clone at 6e1294f: 111 passed 1 skipped.
- 2026-11-02T17:17:02Z qa: moved in_progress -> in_review
- 2026-11-02T17:17:13Z orchestrator: No re-measure: at 312efe6 the judge parse was strict; T-168 r1 made it lenient and r2 restored strict for every judge, so judge behaviour at HEAD equals the measured commit (extract-only leniency only adds the lib01 record-3 answer, which the live run called directly).
- 2026-11-02T17:17:13Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Changed: tests/unit/test_eval_runner.py (6e1294f). New tests bind committed calibration.json to report 20261102T164038Z.md (derived from generated_at; file has no run id) incl. counts, source commit, backend, and to the newest run dir (161327Z) holding all cases; forged count+sentence edit fails. F3 (messages + match) and F5 (skip only claude-cli) fixed. Verified: fresh clone 111 passed 1 skipped; mutant CAL_BACKENDS=(fixture,) fails dirty-tree test. Left: F1 red test_e2e_contract is T-166; F4 re-measure vs record gap is orchestrator. Surprised: run dir id (start) != report id (finish), no runs/164038Z exists.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:23.894Z

**tool call — Bash**
````
{
 "command": "M=.claude/agent-memory/staff-engineer-reviewer && cat $M/feedback_reviewer_scratch_writes.md $M/feedback_review_write_once.md $M/feedback_evidence_sha_vs_commit.md $M/project_eval_runner_review_patterns.md $M/project_t090_calibration_review_patterns.md 2>&1 | head -250",
 "description": "Read relevant reviewer memory notes"
}
````

### User / tool · 2026-11-02T17:17:23.972Z

**tool result**
````
---
name: reviewer-scratch-writes
description: Reviewer Write tool is blocked outside reviews/ and artifacts/review-evidence/ (scratchpad refused); keep helper scripts and sweep outputs there; shell lines with backticks or triple backticks trip the board guard
metadata:
  type: feedback
---

Write tool calls to the session scratchpad were refused by reviewer-write-guard. Shell `cp` and `cat >` into the scratchpad still worked. Keep reviewer helper scripts and copied evidence in artifacts/review-evidence/<card>-rN/ so the Write tool is allowed.

**Why:** the write guard allows only reviews/, artifacts/review-evidence/ and the agent memory dir. The scratchpad is outside that list for Write, and the error came back on the first Write.

**How to apply:** put sweep scripts, mutants and copied outputs under artifacts/review-evidence/. Do not put backticks or triple backticks inside a shell command line; the git-guard board-guard denies unparseable commands. Write a small .py file instead and run it with python -I.

Related: [[project_t167_plain_wording_patterns]].
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

**T-141 r5 addendum:** the first Write carried one control claim I had not yet run ("V10 and W10 print info on 93a2ffc"). It was true, but the guard then refused an Edit to fix a muddled sentence about it. Run every "X prints Y on the control archive" claim before the first Write, and proof-read the evidence sentence, not only the JSON. Accurate-but-clumsy wording can stay, but it cannot be corrected in place. See [[project_t141_r5_patterns]].

**T-155 r2 / T-164 addendum:** two wrong body facts went out in first Writes: a file name (test_multicase.py for test_rerun_note.py) and "the card names X" when the card does not. Both were caught only after the Write. Before the first Write, grep each file name and each "the card says" phrase against `board.py show` output. The corrected records are `-r2b` and `-r1` files, and each names the file it corrects. See [[project_t155_r2_t164_patterns]].
---
name: feedback_evidence_sha_vs_commit
description: a card's green run and its "stale test" triage can cite an older sha; run the cited test at that sha and at the reviewed commit before accepting either, and count the commits between them
metadata:
  type: feedback
---

Before accepting "full suite green at clean HEAD" or "this red is a stale test", check which sha the evidence ran on. Run `git rev-list --count <evidence-sha>..<commit>` and run the disputed test file at both shas. If the file at the evidence sha fails the same way the card says it is stale, the triage is backwards.

**Why:** T-155 r1 (20b3a42): the AC evidence was a run at 078c5ae, 12 commits behind. At 078c5ae the density budgets really failed (179 > 150); a later frontend fix (f262223) cured them. The card called them stale and loosened the budget with a false comment. A first-screen red at the reviewed commit was not on the card.

**How to apply:** in any e2e review, record the evidence sha and the reviewed sha on the first line of the exercised list. Use an archive per sha (git archive | tar -x into a unique scratch dir, own port, E2E_REQUIRE_DB=1). If HEAD moves during the review, say so and state which sha the findings are for.

Related: [[project_t155_e2e_triage_patterns]], [[project_round2_snapshot_review_patterns]].

**T-158 data point (r1, 2026-11-02):** HEAD moved four times during one review (83f1afd, a7302fe, f31b146, 9db2cec). The card's green came from 2de5ba9 (another card), not from its own commit 0b2ce9c. See [[project_t158_settle_patterns]].
---
name: eval-runner-review-patterns
description: T-038 r1-r2 eval runner (evals/run.py) review patterns: test doubles hiding real key shapes, bar-level mutation coverage, scratch-copy mutation method for eval tests
metadata:
  type: project
---

Eval runner (`evals/run.py`, ship bar, check-spec, check-fresh) reviews, T-038 r1 (commit 40c882d) and r2 (HEAD 5542dfd).

- **Fake pipeline shape can hide a real key mismatch.** `tests/unit/test_eval_runner.py` `Perfect.run_case` builds records with `source_label`, but the real `app/backend/pipeline.py` `case_view` (line ~331) returns the ingest records with `source`. The grounding check (`evals/run.py:278`) compares against `source_label`, so every entry fails on the real pipeline (56/56 provider failures on fixture). Fail-closed, but bar 1 can never pass. Lesson: when a test double stands in for a pipeline, diff its output keys against `run_case`'s real keys (print `sorted(out['records'][0])`).
  **Why:** the fake and the test both passed; only a real run exposed it.
  **How to apply:** for any eval or contract test double, add one test that runs the real `run_case` on the sample and asserts the harness's own checks give no failures.

- **Bar-level mutations are the right kill test.** T-038 r1 had per-bar assertions missing; r2 added `bars[name] is False` tests and all six listed mutations die. Still open: a removed `runs == 3` term in bar 4 survives because the blocker list catches it (bars and blockers can disagree).
  **How to apply:** after any bar or gate change, mutate each bar term and require a test that asserts that bar, not just `ship_bar_met`.

- **Method (scratch copy):** copy `app/ evals/ tests/ spec/ docs/ memory/` into the scratchpad (not `.env`; `memory/contracts/api.md` is read by tests, so `memory/` must be included). For each mutation, assert the target string occurs exactly once, write the mutated `run.py`, run `pytest tests/unit -q -k eval`, then restore and diff against the repo file.

- **Repo moves during review.** HEAD advanced twice mid-review (T-051 guard, then other commits) and the eval test count changed 37 to 38. Re-sync the scratch copy from HEAD before mutation runs and quote the HEAD sha.

- **The eval CLI writes into `evals/reports/`** (untracked, overwrites `latest.json`). Say so in the review when running the brief's commands.

- Model discrepancy: the dossier expects `claude-sonnet-5-5`, but the environment runs as `claude-haiku-5-5`. The review record uses what I actually run as.

See also [[project_wiring_review_patterns]] (grep callers, run the producer) and [[project_llm_stage_review_patterns]] (shared fixtures, pin HEAD by sha).

## T-038 r3 (commit 7364096) — addendum
- **Fix verified by reverting it.** Reverting `first["source"]` to `source_label` fails three tests, including the real-`run_case` test. A real-run test needs a negative control (inject a wrong provider, expect a failure) or it can be vacuous.
- **The fix chose the internal shape, not the API shape.** `run_case` records use `source` (store.py:26); the API record view and `memory/contracts/api.md` use `source_label` (present.py:132). The eval never imports `present`, so the API mapping is untested. Check the docstring claim that a function "is the shape the eval reads" against the real output.
- **Pin the review to the commit.** HEAD moved mid-review and the working tree was dirty with another agent's uncommitted `evals/run.py`. Use `git archive <sha> | tar -x -C <scratch>` and run everything there. Report working-tree results separately.
- **Check the CLI with `--out <scratch>`.** It writes `latest.json` into `--out`, not into the repo's `evals/reports/`.
- **Tools path:** `board.py` lives at `tools/board.py`, not the repo root. `validate <review.md>` returns `ok`.
- See [[project_wiring_review_patterns]] for the same "fake hides the real shape" failure mode.
---
name: t090-calibration-review-patterns
description: T-090 calibrated-confidence r1-r3: committed counts not reproducible, reverted fix at HEAD, forged source_commit skip (git-less copies still skip), served field owner missing, sentence check mutant
metadata:
  type: project
---

T-090 r1 (commit d0aee83, calibrated confidence as N/M counts, D-042) written to reviews/T-090-staff-engineer.md: fail, 1 blocker, 3 majors, 4 minors, 1 nit.

- **Committed artifact must be regenerated, not trusted.** evals/reports/calibration.json said 82/83 and 11/13, but `git archive d0aee83` + `evals.run --out` (fixture) gives 83/84 and 10/10 twice, and HEAD ec33bf0 gives the same. No `*T041847Z.md` report existed for its generated_at. Method: pin with git archive, regenerate with --out, diff counts ignoring generated_at, then hand-check two cells from a dump of the raw items.
- **Hand-check cells from raw items, not from the counters.** A dump script (run.py's golden_cases + pipeline.run_case, fixture) lets you tally verified amounts (9/9) and needs-review flags (2/2) by reading golden against live. Found the file's flag cell (3/5) unreproducible.
- **"llm call failed ... FIXTURE_MISS" lines on the eval CLI come from score_unsplit**, not from the golden cases (checked: score_unsplit alone prints 7). Do not read them as calibration misses.
- **Working tree evals/run.py was modified mid-review (uncommitted).** Working-tree counts (84/85, 9/9) differ from the commit's. Use archives for every count you cite.
- **Mutants that survive a green suite here:** dropping the class term in amount matching (test gap; golden counts identical, so the rate-vs-charge blind spot is real), dropping the tolerated term, lowering CAL_SMALL_N to 5 (the boundary test uses 30 names, never 29), and dropping the record_warning filter before zip (positional alignment, untested).
- **AC closed with an unbuilt clause.** Card AC 1 said "UI shows ..." and was done:true with "UI line pending frontend". Check for any route/UI reference (grep app/) before accepting an AC that names the UI.
- **Sentence without provenance.** The generated sentence the UI would show verbatim named N/M and a case count, not the backend. A fixture replay read as live precision. Check the rendered sentence, not only the file's top-level fields.

**How to apply:** for any measured-number artifact, (1) regenerate at the pinned sha into a scratch --out, (2) diff against the committed file, (3) hand-check two cells from raw items, (4) mutate the matching rule per term (class, tolerated, state guard, threshold) and require a boundary test each.

T-090 r2 (commits 823b718 code, 02ff244 file; review reviews/T-090-staff-engineer-r2.md): fail, 1 blocker, 2 majors, 2 minors.
- **A later commit reverted the fix.** 2fca530 (another card, committed 15 s after 823b718, before 02ff244) deleted git_source and the 11 r2 tests. HEAD evals/ and test file == 02ff244. Project-tree "84 passed" was uncommitted. Always check `git diff --quiet <fix> HEAD -- <files>` and `git log --oneline <fix>..HEAD -- <files>` before accepting a fix commit as shipped.
- **Skip is a silent pass for a forged header.** Provenance tests skip on "no git history" and on "commit not available", so a source_commit naming a non-existent commit reports 2 skipped and no failure. Skips must be scoped to "no .git"; a missing cited commit must fail.
- **check-fresh validates sums and hashes only.** An edited served sentence returns 0 from check_fresh; only the pytest regeneration test catches it.
- **Scratch method that worked:** clone, detached checkout of the commit, regenerate with `python -I` plus sys.path insert and runpy, compare ignoring generated_at, then mutate the clone's file and run the selector per mutant. Restore by copying a saved pristine file (not git checkout).
- Narrowing an AC to "UI is under T-096" left the backend serve route with no AC anywhere (grep for the route name in the owning card).

T-090 r3 (commits b85fc1b code, 172028c file, a850be0 restores r2; review reviews/T-090-staff-engineer-r3.md): changes, 0 blockers, 1 major, 1 minor, 2 nits.
- **Fix verified at HEAD, then the residual moved.** r2 blocker closed (a850be0 restored git_source and 11 tests). Forged source_commit now fails in a git clone (2 failed, 0 skipped). But a .git-less copy (git archive) skips both provenance tests, so the forged header passes with 3 skipped. Test for "fails not skips" in a clone AND in an archive, not only in one.
- **Served field owner still missing.** T-090 AC 1 says "carried by T-096"; T-096 AC 1 names no route, and its note says "Backend AC needed". Check the owning card's AC text for the route term, not the note.
- **Sentence rebuild in check_calibration is real.** Removing the 2-line block (not just the `if` line) kills test_check_fresh_fails_on_an_edited_calibration_sentence; check_fresh returns 1 on an edited 83/84 -> 84/84.
- **Mutants to run for the header/tree pattern:** source_commit 1*40 (expect fail), commit-tree orphan commit (non-ancestor, expect 1 fail), source_tree 0*40 (expect 1 fail), r2 skip logic restored (expect 3 skipped, the silent green).
- **Regeneration from git archive matches exactly** except the git-derived fields: run twice, byte-identical except generated_at. Archive copies report source_commit None (expected; test ignores git fields).

Related: [[project_eval_runner_review_patterns]] (scratch-copy method, --out flag), [[project_r2_fix_verification_patterns]] (overstated mutant counts), [[project_t093_signature_controls_patterns]] (scratch-mutant guard traps), [[project_harness_review_patterns]] (git-guard quirks in scratch runs).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:24.750Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>&1; git rev-parse HEAD 2>&1; git rev-parse --verify 6e1294f^{commit} 2>&1; git log --oneline -3 6e1294f 2>&1; git show --stat 6e1294f 2>&1 | head -30; ls -la reviews/ | head -50; ls artifacts/review-evidence/ 2>&1",
 "description": "Check git state, commit 6e1294f, and review dirs"
}
````

### User / tool · 2026-11-02T17:17:24.956Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:28.939Z

**tool call — Bash**
````
{
 "command": "git rev-parse 6e1294f && git ls-files evals/reports | head -50 && echo \"--- runs tracked:\" && git ls-files runs | head -20 && echo \"--- runs on disk:\" && ls runs 2>&1 | tail -5 && ls runs/20261102T161327Z 2>&1 | head -20 && echo \"--- report:\" && ls -la evals/reports/20261102T164038Z.md 2>&1 && git ls-files evals/reports/20261102T164038Z.md && git status --short | head -20 && echo \"--- git check-ignore runs:\" && git check-ignore -v runs 2>&1",
 "description": "Check tracked evidence files and runs directory state"
}
````

### User / tool · 2026-11-02T17:17:29.165Z

**tool result (error)**
````
Exit code 1
6e1294f171cd1e9a3e82014a9d321286d1a527eb
evals/reports/20261102T020824Z.md
evals/reports/20261102T020933Z.md
evals/reports/20261102T021029Z.md
evals/reports/20261102T021046Z.md
evals/reports/20261102T022701Z.md
evals/reports/20261102T022927Z.md
evals/reports/20261102T023039Z.md
evals/reports/20261102T025219Z.md
evals/reports/20261102T025715Z.md
evals/reports/20261102T032823Z.md
evals/reports/20261102T035750Z.md
evals/reports/20261102T040933Z.md
evals/reports/20261102T081339Z.md
evals/reports/20261102T083252Z.md
evals/reports/20261102T085207Z.md
evals/reports/20261102T095640Z.md
evals/reports/20261102T104043Z.md
evals/reports/20261102T111004Z.md
evals/reports/20261102T113305Z.md
evals/reports/20261102T115041Z.md
evals/reports/20261102T115607Z.md
evals/reports/20261102T120809Z.md
evals/reports/20261102T121612Z.md
evals/reports/20261102T123428Z.md
evals/reports/20261102T124856Z.md
evals/reports/20261102T164038Z.md
evals/reports/calibration.json
evals/reports/controls-20261102T042306Z.json
evals/reports/controls-20261102T042306Z.md
evals/reports/controls-20261102T063331Z.json
evals/reports/controls-20261102T063331Z.md
evals/reports/controls-20261102T075238Z.json
evals/reports/controls-20261102T075238Z.md
evals/reports/controls-20261102T090925Z.json
evals/reports/controls-20261102T090925Z.md
evals/reports/controls-20261102T102626Z.json
evals/reports/controls-20261102T102626Z.md
evals/reports/controls-20261102T123937Z.json
evals/reports/controls-20261102T123937Z.md
evals/reports/determinism-diagnosis.md
evals/reports/latest.json
evals/reports/library-latest.md
evals/reports/m3-sensors.md
evals/reports/runs/20261102T034706Z/case_01_date_formats.json
evals/reports/runs/20261102T034706Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T034706Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T034706Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T034706Z/case_05_provider_conflict.json
evals/reports/runs/20261102T034706Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T034706Z/case_07_prompt_injection.json
--- runs tracked:
--- runs on disk:
ls: runs: No such file or directory
ls: runs/20261102T161327Z: No such file or directory
--- report:
-rw-r--r--@ 1 arsis  staff  15006 Nov  2 10:41 evals/reports/20261102T164038Z.md
evals/reports/20261102T164038Z.md
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
--- git check-ignore runs:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:31.364Z

**tool call — Bash**
````
{
 "command": "git ls-files evals/reports/runs | cut -d/ -f4 | sort | uniq -c; echo \"--- 161327Z tracked at 6e1294f:\"; git ls-tree -r --name-only 6e1294f evals/reports/runs/20261102T161327Z | head -20; echo \"--- on disk:\"; ls -la evals/reports/runs/20261102T161327Z 2>&1 | head -20; echo \"--- calibration.json at 6e1294f:\"; git show 6e1294f:evals/reports/calibration.json | head -c 3000",
 "description": "Locate run folder and calibration.json at pinned commit"
}
````

### User / tool · 2026-11-02T17:17:31.530Z

**tool result**
````
  13 20261102T034706Z
  13 20261102T035806Z
  14 20261102T075514Z
  14 20261102T081339Z
  14 20261102T083312Z
  14 20261102T105126Z
  14 20261102T111525Z
  14 20261102T113305Z
  14 20261102T115041Z
  13 20261102T161327Z
--- 161327Z tracked at 6e1294f:
evals/reports/runs/20261102T161327Z/case_01_date_formats.json
evals/reports/runs/20261102T161327Z/case_02_gap_boundaries.json
evals/reports/runs/20261102T161327Z/case_03_rate_and_ocr.json
evals/reports/runs/20261102T161327Z/case_04_duplicates_no_amounts.json
evals/reports/runs/20261102T161327Z/case_05_provider_conflict.json
evals/reports/runs/20261102T161327Z/case_06_subtle_pre_existing.json
evals/reports/runs/20261102T161327Z/case_07_prompt_injection.json
evals/reports/runs/20261102T161327Z/case_08_diagnosis_temptation.json
evals/reports/runs/20261102T161327Z/case_09_nonvisit_hides_gap.json
evals/reports/runs/20261102T161327Z/run1.json
evals/reports/runs/20261102T161327Z/run2.json
evals/reports/runs/20261102T161327Z/run3.json
evals/reports/runs/20261102T161327Z/sample.json
--- on disk:
total 328
drwxr-xr-x@ 15 arsis  staff    480 Nov  2 10:41 .
drwxr-xr-x@ 46 arsis  staff   1472 Nov  2 10:41 ..
-rw-r--r--@  1 arsis  staff   9591 Nov  2 10:41 case_01_date_formats.json
-rw-r--r--@  1 arsis  staff  10776 Nov  2 10:41 case_02_gap_boundaries.json
-rw-r--r--@  1 arsis  staff   7403 Nov  2 10:41 case_03_rate_and_ocr.json
-rw-r--r--@  1 arsis  staff   4226 Nov  2 10:41 case_04_duplicates_no_amounts.json
-rw-r--r--@  1 arsis  staff   6590 Nov  2 10:41 case_05_provider_conflict.json
-rw-r--r--@  1 arsis  staff   7699 Nov  2 10:41 case_06_subtle_pre_existing.json
-rw-r--r--@  1 arsis  staff   8498 Nov  2 10:41 case_07_prompt_injection.json
-rw-r--r--@  1 arsis  staff   4938 Nov  2 10:41 case_08_diagnosis_temptation.json
-rw-r--r--@  1 arsis  staff   6350 Nov  2 10:41 case_09_nonvisit_hides_gap.json
-rw-r--r--@  1 arsis  staff  17939 Nov  2 10:41 run1.json
-rw-r--r--@  1 arsis  staff  17939 Nov  2 10:41 run2.json
-rw-r--r--@  1 arsis  staff  17939 Nov  2 10:41 run3.json
-rw-r--r--@  1 arsis  staff  17942 Nov  2 10:41 sample.json
--- calibration.json at 6e1294f:
{
 "backend": "claude-cli",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_07_prompt_injection",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 11,
   "total": 11
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
   "matched": 82,
   "total": 83
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
     "case_03_rate_and_ocr": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ]
    },
    "matched": 4,
    "total": 4
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      7,
      7
     ],
     "case_02_gap_boundaries": [
      8,
      8
     ],
     "case_03_rate_and_ocr": [
      4,
      4
     ],
     "case_04_duplicates_no_amounts": [
      4,
      4
     ],
     "case_05_provider_conflict": [
      5,
      5
     ],
     "case_06_subtle_pre_existing": [
      4,
      5
     ],
     "case_07_prompt_injection": [
      3,
      3
     ],
     "case_08_diagnosis_temptation": [
      4,
      4
     ],
     "case_09_nonvisit_hides_gap": [
      4,
      4
     ],
     "sample": [
      9,
      9
     ]
    },
    "matched": 52,
    "total": 53
   }
  },
  "flag": {
   "needs_review": {
    "by_case": {
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 1,
    "total": 1
   },
   "verified": {
    "by_case": {
     "case_02_gap_boundaries": [
      3,
      3
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_06_subtle_pre_existing": [
      4,
      4
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
      10,
      10
     ]
    },
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:36.891Z

**tool call — Bash**
````
{
 "command": "set -e; EV=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2; mkdir -p \"$EV\"; cd \"$EV\" && rm -rf clone && git clone -q /Users/arsis/zlayt-pm-project clone && cd clone && git checkout -q --detach 6e1294f && git rev-parse HEAD && git status --short | head -5; echo \"--- venv:\"; ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1; echo \"--- diff 5ed37ad..6e1294f stat:\"; git diff --stat 5ed37ad 6e1294f; echo \"--- commits between:\"; git rev-list --count 5ed37ad..6e1294f",
 "description": "Fresh clone of repo detached at 6e1294f"
}
````

### User / tool · 2026-11-02T17:17:36.949Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may not run `git checkout` in the project (allowed only in scratch repos under /tmp)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:40.121Z

**tool call — Bash**
````
{
 "command": "EV=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2; ls -la $EV 2>&1; ls $EV/clone 2>&1 | head; git -C $EV/clone rev-parse HEAD 2>&1",
 "description": "Check whether the scratch clone was created"
}
````

### User / tool · 2026-11-02T17:17:40.221Z

**tool result (error)**
````
Exit code 128
ls: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2: No such file or directory
ls: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/clone: No such file or directory
fatal: cannot change to '/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/clone': No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:44.754Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR/T169_staff_r2\" && git clone -q /Users/arsis/zlayt-pm-project \"$SCR/T169_staff_r2/clone\" && git -C \"$SCR/T169_staff_r2/clone\" checkout -q --detach 6e1294f && git -C \"$SCR/T169_staff_r2/clone\" rev-parse HEAD && git -C \"$SCR/T169_staff_r2/clone\" status --short | head -5; echo \"rc=$?\"",
 "description": "Clone repo into scratchpad and detach at 6e1294f"
}
````

### User / tool · 2026-11-02T17:17:50.027Z

**tool result**
````
6e1294f171cd1e9a3e82014a9d321286d1a527eb
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:17:51.730Z

**tool call — Bash**
````
{
 "command": "git diff 5ed37ad 6e1294f -- tests/unit/test_eval_runner.py",
 "description": "Show the full T-169 r2 test diff"
}
````

### User / tool · 2026-11-02T17:17:51.822Z

**tool result**
````
diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index eb93b68..487400b 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -802,7 +802,8 @@ CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; cl
 def _assert_calibration_header(c):
     assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
     assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
-    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")
+    assert c["source_tree_clean"] is True, "calibration source tree is not clean"
+    assert c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or ""), "calibration has no source tree or hashes"
 
 
 def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
@@ -811,13 +812,13 @@ def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
 
 def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
     """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
-    for backend in CAL_BACKENDS:
+    for backend in ("fixture", "claude-cli"):  # literal on purpose: shrinking CAL_BACKENDS must fail this test
         dirty = _committed()
         dirty["backend"], dirty["source_tree_clean"] = backend, False
         p = tmp_path / f"dirty_{backend}.json"
         p.write_text(json.dumps(dirty))
         monkeypatch.setattr(sys.modules[__name__], "CAL", p)
-        with pytest.raises(AssertionError):
+        with pytest.raises(AssertionError, match="source tree is not clean"):
             _assert_calibration_header(_committed())
         monkeypatch.undo()
 
@@ -847,9 +848,9 @@ def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_pa
     (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
     c = _committed()
     _require_source_commit(c)
-    if c["backend"] != "fixture":
+    if c["backend"] == "claude-cli":
         # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
-        # ancestor and clean-tree tests plus the live report it cites; this exact-regeneration check only covers the fixture backend.
+        # ancestor and clean-tree tests plus the report-binding test below (the report is found from generated_at; the file has no run id).
         pytest.skip(f"committed calibration is a live {c['backend']} measurement; exact regeneration needs the live backend")
     src = tmp_path / "src"
     src.mkdir()
@@ -1082,3 +1083,59 @@ def test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir(m
     import os
     assert seen == {"dir": None, "set": "split"}
     assert os.environ.get("FIXTURE_SET") == "recorded" and "LLM_FIXTURE_DIR" not in os.environ
+
+
+def _report_for(c):
+    """The calibration file has no run id or report field, so the link is derived: generated_at 2026-11-02T16:40:38Z is the report id 20261102T164038Z (T-169 r2)."""
+    rid = re.sub(r"[-:]", "", c["generated_at"])
+    assert re.fullmatch(r"\d{8}T\d{6}Z", rid), f"generated_at {c['generated_at']!r} is not a UTC timestamp"
+    return rid, R.REPORTS / f"{rid}.md"
+
+
+def _report_counts(md):
+    """matched/seen read from the report's own text: the two overall sentences and the per-type table."""
+    got = {"sentences": [l[2:] for l in md.splitlines() if l.startswith("- ") and " matched the record " in l]}
+    got["table"] = {m[0]: [tuple(map(int, x.split("/"))) for x in m[1:]]
+                    for m in re.findall(r"^\| (entry|amount|flag) \| (\d+/\d+) \| (\d+/\d+) \|$", md, re.M)}
+    return got
+
+
+def test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts():
+    """T-169 r2 F2: the live calibration cannot be regenerated offline, so tie it to the report of its run. The report must exist in
+    evals/reports, name the same source commit and backend, and carry the same overall sentences and per-type matched/seen counts."""
+    c = _committed()
+    rid, rep = _report_for(c)
+    assert rep.exists(), f"calibration.json generated_at {c['generated_at']} names report {rep.name}, which is not in evals/reports"
+    md = rep.read_text()
+    assert f"backend `{c['backend']}`" in md and f"Source commit `{c['source_commit']}`" in md, f"{rep.name} names a different backend or source commit"
+    got = _report_counts(md)
+    assert got["sentences"] == [c["sentences"]["overall"]["verified"], c["sentences"]["overall"]["needs_review"]], f"{rep.name} overall counts differ from calibration.json"
+    want = {t: [tuple(c["by_type"][t][s][k] for k in ("matched", "total")) for s in ("verified", "needs_review")] for t in ("entry", "amount", "flag")}
+    assert got["table"] == want, f"{rep.name} per-type counts differ from calibration.json"
+    for s in ("verified", "needs_review"):
+        assert f"{c['by_state'][s]['matched']}/{c['by_state'][s]['total']} times" in c["sentences"]["overall"][s], "by_state disagrees with its own sentence"
+
+
+def test_committed_calibration_run_directory_exists_with_every_case():
+    """The raw outputs of the run: the newest evals/reports/runs/<id> not later than the report id must hold one file per calibration case.
+    (Run ids are the run's start time, the report id its finish time, so they differ; the file carries neither.)"""
+    c = _committed()
+    rid, _ = _report_for(c)
+    runs = sorted(d.name for d in (R.REPORTS / "runs").iterdir() if d.is_dir() and d.name <= rid)
+    assert runs, f"no evals/reports/runs/<id> at or before {rid}"
+    have = {p.stem for p in (R.REPORTS / "runs" / runs[-1]).glob("*.json")}
+    assert set(c["cases"]) <= have, f"runs/{runs[-1]} lacks {sorted(set(c['cases']) - have)}"
+
+
+def test_report_binding_fails_on_a_coordinated_count_and_sentence_edit(tmp_path, monkeypatch):
+    """T-169 r2 F2 acceptance: change by_state.verified.matched and its sentence together; the binding test must fail."""
+    c = _committed()
+    c["by_state"]["verified"]["matched"] = c["by_state"]["verified"]["total"]
+    c["sentences"]["overall"]["verified"] = c["sentences"]["overall"]["verified"].replace(
+        f"{c['by_state']['verified']['total'] - 1}/", f"{c['by_state']['verified']['total']}/")
+    c["by_type"]["entry"]["verified"]["matched"] = c["by_type"]["entry"]["verified"]["total"]
+    forged = tmp_path / "calibration.json"
+    forged.write_text(json.dumps(c))
+    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
+    with pytest.raises(AssertionError, match="differ from calibration.json"):
+        test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:18:28.498Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && grep -n \"^CAL\\|def _committed\\|def _require_source_commit\\|^R\\b\\|REPORTS\\|^import\\|^from\\|CAL_BACKENDS\" tests/unit/test_eval_runner.py | head -40; echo ---; sed -n 780,870p tests/unit/test_eval_runner.py",
 "description": "Read calibration helpers and header tests in clone"
}
````

### User / tool · 2026-11-02T17:18:28.629Z

**tool result**
````
3:import copy, json, re
4:import pytest
5:from evals import run as R
6:from tests.unit import _golden as G
631:    monkeypatch.setattr(R, "REPORTS", tmp_path)
643:    monkeypatch.setattr(R, "REPORTS", tmp_path)
775:import os, shutil, subprocess, sys
776:CAL = R.REPORTS / "calibration.json"
783:def _committed():
791:def _require_source_commit(c):
799:CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
803:    assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
815:    for backend in ("fixture", "claude-cli"):  # literal on purpose: shrinking CAL_BACKENDS must fail this test
1092:    return rid, R.REPORTS / f"{rid}.md"
1124:    runs = sorted(d.name for d in (R.REPORTS / "runs").iterdir() if d.is_dir() and d.name <= rid)
1126:    have = {p.stem for p in (R.REPORTS / "runs" / runs[-1]).glob("*.json")}
---
    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)


def _committed():
    return json.loads(CAL.read_text())


def _has_git():
    return shutil.which("git") is not None and _git("rev-parse", "--git-dir").returncode == 0


def _require_source_commit(c):
    """Skip only when this is not a git checkout at all (an exported tree).  In a repository a cited commit that is missing is a forged header: fail."""
    if not _has_git():
        pytest.skip("no git repository here (exported tree)")
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or ""), "calibration.json source_commit is not a commit hash"
    assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"


CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)


def _assert_calibration_header(c):
    assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
    assert c["source_tree_clean"] is True, "calibration source tree is not clean"
    assert c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or ""), "calibration has no source tree or hashes"


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    _assert_calibration_header(_committed())


def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
    """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
    for backend in ("fixture", "claude-cli"):  # literal on purpose: shrinking CAL_BACKENDS must fail this test
        dirty = _committed()
        dirty["backend"], dirty["source_tree_clean"] = backend, False
        p = tmp_path / f"dirty_{backend}.json"
        p.write_text(json.dumps(dirty))
        monkeypatch.setattr(sys.modules[__name__], "CAL", p)
        with pytest.raises(AssertionError, match="source tree is not clean"):
            _assert_calibration_header(_committed())
        monkeypatch.undo()


def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
    c = _committed()
    _require_source_commit(c)
    assert _git("merge-base", "--is-ancestor", c["source_commit"], "HEAD").returncode == 0, f"{c['source_commit']} is not an ancestor of HEAD"
    assert _git("rev-parse", c["source_commit"] + "^{tree}").stdout.strip() == c["source_tree"], "source_tree is not the tree of source_commit"


def test_forged_source_commit_fails_instead_of_skipping(tmp_path, monkeypatch):
    c = _committed()
    c["source_commit"] = "1" * 40
    forged = tmp_path / "calibration.json"
    forged.write_text(json.dumps(c))
    monkeypatch.setattr(sys.modules[__name__], "CAL", forged)
    if not _has_git():
        pytest.skip("no git repository here")
    with pytest.raises(AssertionError, match="does not exist"):
        _require_source_commit(_committed())


def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
    """T-090 r2 blocker: the shipped counts must come from the code of the commit named in the header. Export that commit
    (never the shared working tree, which other workers keep dirty) and compare, ignoring only generated_at and the git-derived fields
    (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
    c = _committed()
    _require_source_commit(c)
    if c["backend"] == "claude-cli":
        # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
        # ancestor and clean-tree tests plus the report-binding test below (the report is found from generated_at; the file has no run id).
        pytest.skip(f"committed calibration is a live {c['backend']} measurement; exact regeneration needs the live backend")
    src = tmp_path / "src"
    src.mkdir()
    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
    # The cited commit's own code decides where the file lands: commits before T-101 write out/calibration.json, later ones only a
    # scratch copy under out/runs/<ts>/ (T-101). Exactly one must exist either way.
    found = [p for p in [out / "calibration.json", *sorted((out / "runs").glob("*/calibration.json"))] if p.exists()]
    assert len(found) == 1, r.stdout[-400:] + r.stderr[-800:]
    fresh = json.loads(found[0].read_text())
    git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
    assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
    assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:18:32.369Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && head -30 evals/reports/20261102T164038Z.md; echo ...; grep -n \"matched the record\\|^| entry\\|^| amount\\|^| flag\\|161327\\|runs/\\|run \" evals/reports/20261102T164038Z.md | head -30; echo \"--- calibration header keys + sentences:\"; python3 -c \"\nimport json;c=json.load(open('evals/reports/calibration.json'))\nprint({k:v for k,v in c.items() if k not in ('by_state','by_type','sentences','cases')})\nprint(json.dumps(c['sentences'],indent=1)[:1500])\nprint('cases',len(c['cases']))\n\"; echo \"--- grep 161327 anywhere in tracked evidence:\"; grep -rl \"161327\" evals/ docs/ memory/ board/ 2>/dev/null | head",
 "description": "Inspect report file, calibration header and run-id references"
}
````

### User / tool · 2026-11-02T17:18:32.511Z

**tool result**
````
# Eval report 2026-11-02T16:40:38Z

**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.

| Metric | Value | Bar | R-IDs |
|---|---|---|---|
| grounding_rate | 1.000 (242 checked) | 1.0 | R-TL-2, R-TL-9, R-FL-5, R-EX-2 |
| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
| hallucination_catch_rate | 1.000 (40/40; measured; judge unavailable 0) | >= 0.95 | R-TL-4, R-TL-10 |
| controls judged unsupported | 0 of 10 | 0 | R-TL-4 |
| unsupported_count_3run | 0 | 0 | R-TL-4 |
| determinism_3run | 1.0 | 1.0 | R-CO-7 |
| J3 judge_conflict_v6 seeded catch rate | 1.000 (20/20 wrong caught x3 runs; in-sample 14/14; held-out 6/6; false agree 0 []; correct accepted 21/21; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| J4 judge_flag_v3 seeded catch rate | 1.000 (12/12 wrong caught x3 runs; in-sample 9/9; held-out 3/3; false agree 0 []; correct accepted 15/15; unstable []; unavailable 0) | all wrong caught, 0 false agree | R-CO-2 |
| golden_must_not_hits | 0 | 0 | R-CO-3 |
| unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1 |
| case_07_total_420 | True | true | R-RV-6 |
| letter_currency_outside_charges (fixture export, 25 cases; 11 entries held out) | 0 | 0 | R-CH-7, R-EX-8 |
| lexicon_recall_must_flags (reported, not gated) | 1.000 | none (D-026) | R-FL-3, R-RV-6 |


## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `312efe6633`)

- Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).
...
9:| entry_recall | 0.982 | >= 0.95 | R-TL-1, R-TL-7 |
10:| amount_recall | 1.000 | >= 0.95 | R-CH-1 |
11:| flag_precision[gap] / flag_recall[gap] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
12:| flag_precision[conflict] / flag_recall[conflict] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
13:| flag_precision[pre_existing] / flag_recall[pre_existing] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
14:| flag_precision[causation] / flag_recall[causation] | 1.000 / 1.000 | >= 0.9 each | R-FL-1..4 |
17:| unsupported_count_3run | 0 | 0 | R-TL-4 |
18:| determinism_3run | 1.0 | 1.0 | R-CO-7 |
30:- Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).
31:- Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).
35:| entry | 52/53 | 4/4 |
36:| amount | 9/9 | 6/6 |
37:| flag | 21/21 | 1/1 |
44:| id | judge | split | kind | pair | origin | expected | verdict per run | ok |
131:- per-run artifacts: `evals/reports/runs/20261102T161327Z`
--- calibration header keys + sentences:
{'backend': 'claude-cli', 'case_count': 10, 'generated_at': '2026-11-02T16:40:38Z', 'hashes': {'app/llm/lexicon.yaml': 'fbefe801fb3d582c48e93bfbe54ccb1e34e9640a5b6cbf800e42a5aa7f612a8b', 'app/llm/prompts/extract_es_v1.md': '985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb', 'app/llm/prompts/extract_v1.md': '11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2', 'app/llm/prompts/flags_v1.md': 'd5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725', 'app/llm/prompts/judge_amount_class_v1.md': 'e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8', 'app/llm/prompts/judge_conflict_v1.md': '10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa', 'app/llm/prompts/judge_conflict_v2.md': '6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6', 'app/llm/prompts/judge_conflict_v4.md': '15df87e8655a014111bbcddb2fee769d01e28149072ceea76f3f9d51fcae4649', 'app/llm/prompts/judge_conflict_v5.md': '90deea934564aa0fda0ad34dc38477104e371c0267259c38c61f58635819dffd', 'app/llm/prompts/judge_conflict_v6.md': '8a09702a5c12a9f08a162cad574374827d3a367cbcca7080e1331c76406318b5', 'app/llm/prompts/judge_faithfulness_es_v1.md': 'd51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898', 'app/llm/prompts/judge_faithfulness_v1.md': '636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b', 'app/llm/prompts/judge_flag_v1.md': '97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432', 'app/llm/prompts/judge_flag_v2.md': '7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe', 'app/llm/prompts/judge_flag_v3.md': '64d65c0182360d4ef84b5f4b62e19a6707ee3f508d975aec4ea6e527c9a5a664', 'app/llm/prompts/narrative_v1.md': '3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac', 'app/llm/prompts/split_v1.md': '9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b'}, 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'models': {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5'}, 'not_scored': {'amount': 0, 'entry': 0, 'flag': 0, 'total': 0}, 'schema': 'evals.calibration/1', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': '312efe663327539df1b712832e23bf1d2c495d42', 'source_tree': '6b761a5e9e52539270e3c7c20bd68d1f8c0bd45a', 'source_tree_clean': True}
{
 "by_type": {
  "amount": {
   "needs_review": "Needs-review amounts matched the record 6/6 times in testing on the claude-cli backend (10 golden cases, small sample).",
   "verified": "Verified amounts matched the record 9/9 times in testing on the claude-cli backend (10 golden cases, small sample)."
  },
  "entry": {
   "needs_review": "Needs-review entries matched the record 4/4 times in testing on the claude-cli backend (10 golden cases, small sample).",
   "verified": "Verified entries matched the record 52/53 times in testing on the claude-cli backend (10 golden cases, small sample)."
  },
  "flag": {
   "needs_review": "Needs-review flags matched the record 1/1 times in testing on the claude-cli backend (10 golden cases, small sample).",
   "verified": "Verified flags matched the record 21/21 times in testing on the claude-cli backend (10 golden cases, small sample)."
  }
 },
 "overall": {
  "needs_review": "Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).",
  "verified": "Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample)."
 }
}
cases 10
--- grep 161327 anywhere in tracked evidence:
evals/reports/20261102T164038Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:18:49.833Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && du -sh . && ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; $PY -c \"import sys;print(sys.version)\"; $PY -c \"import evals,app;print(evals.__file__, app.__file__)\"; echo \"--- test_eval_runner:\"; $PY -m pytest tests/unit/test_eval_runner.py -q -p no:cacheprovider 2>&1 | tail -8; echo \"--- new tests verbose:\"; $PY -m pytest tests/unit/test_eval_runner.py -v -p no:cacheprovider -k \"calibration or report_binding or run_directory\" 2>&1 | tail -20",
 "description": "Run test_eval_runner.py and new calibration tests in clone"
}
````

### User / tool · 2026-11-02T17:20:05.592Z

**tool result**
````
151M	.
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
3.12.2 (main, Feb  6 2024, 20:19:44) [Clang 15.0.0 (clang-1500.1.0.2.5)]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone/evals/__init__.py /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone/app/__init__.py
--- test_eval_runner:
........................................................................ [ 64%]
......................s.................                                 [100%]
111 passed, 1 skipped in 48.06s
--- new tests verbose:
tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run PASSED [ 34%]
tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src0] PASSED [ 38%]
tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src1] PASSED [ 42%]
tests/unit/test_eval_runner.py::test_write_calibration_refusal_rule_is_clean_tree_at_a_commit PASSED [ 46%]
tests/unit/test_eval_runner.py::test_write_calibration_refusal_names_every_dirty_path_it_is_given PASSED [ 50%]
tests/unit/test_eval_runner.py::test_write_calibration_is_refused_with_controls_before_anything_runs PASSED [ 53%]
tests/unit/test_eval_runner.py::test_scratch_copy_and_live_run_artifacts_share_one_run_directory PASSED [ 57%]
tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header PASSED [ 61%]
tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit PASSED [ 65%]
tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree PASSED [ 69%]
tests/unit/test_eval_runner.py::test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head PASSED [ 73%]
tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit SKIPPED [ 76%]
tests/unit/test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git PASSED [ 80%]
tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes PASSED [ 84%]
tests/unit/test_eval_runner.py::test_check_fresh_fails_on_an_edited_calibration_sentence PASSED [ 88%]
tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts PASSED [ 92%]
tests/unit/test_eval_runner.py::test_committed_calibration_run_directory_exists_with_every_case PASSED [ 96%]
tests/unit/test_eval_runner.py::test_report_binding_fails_on_a_coordinated_count_and_sentence_edit PASSED [100%]

================ 25 passed, 1 skipped, 86 deselected in 27.10s =================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:20:22.793Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && sed -n 125,135p evals/reports/20261102T164038Z.md; echo ---; python3 -I -c \"\nimport json,glob\nd=json.load(open('evals/reports/runs/20261102T161327Z/case_01_date_formats.json'))\nprint(type(d).__name__, list(d)[:12] if isinstance(d,dict) else len(d))\n\"; echo \"--- grep runs refs in evals/run.py:\"; grep -n \"runs\" evals/run.py | head -20",
 "description": "Check report run-folder reference and run file structure"
}
````

### User / tool · 2026-11-02T17:20:22.964Z

**tool result**
````
- summary clauses removed by code (D-054, reported not gated): {"items_trimmed": 5, "clauses_removed": 5, "tray_placeholders": 0, "per_case": {"case_03_rate_and_ocr": {"items_trimmed": 3, "clauses_removed": 3, "tray_placeholders": 0}, "case_07_prompt_injection": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}, "case_08_diagnosis_temptation": {"items_trimmed": 1, "clauses_removed": 1, "tray_placeholders": 0}}}
- flag tray (could-not-verify flags, D-053; not scored, not in the R-CO-7 flag signature): 6 {"FILTERED_BY_RULE": 5, "LLM_ONLY": 1} by case {"case_01_date_formats": 3, "case_05_provider_conflict": 1, "case_07_prompt_injection": 1, "sample": 1}
- grounding failures: []
- seeded hallucinations not caught: []
- must_not detail: {}

- per-run artifacts: `evals/reports/runs/20261102T161327Z`

## Prompt and lexicon hashes

- `app/llm/prompts/extract_es_v1.md` 985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb
---
dict ['backend', 'case', 'errors', 'items', 'models', 'run', 'schema', 'signature_parts', 'status', 'tray_flag_count', 'warning_codes']
--- grep runs refs in evals/run.py:
5:                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
415:    summary was removed (could-not-verify tray); clauses_removed = clauses removed over both. Reported, not gated: it shows the clean 3-runs came from the trim and not from luck."""
515:def run_cases(pipeline, backend, cases=None, runs_dir=None):
517:    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
523:        write_run_artifact(runs_dir, name, out, name)
570:CONTROL_REPEATS = 3          # live: every control item is judged on the same three runs as R-CO-7, and the gate needs all three to agree
661:# ---------------------------------------------------------------- live-only: 3 runs on the sample
680:    across runs; LLM-derived states (every entry, amount and flag) must match; flags are compared by (type, set of cited record IDs, evidence excerpt)
710:    """Name every R-CO-7 field that differs between two runs and the items present in only one of them (so a determinism failure is diagnosable)."""
755:def write_run_artifact(runs_dir, fname, out, name=None, run=None):
756:    """Write evals/reports/runs/<ts>/<fname>.json. Refuses (raises) if anything secret-looking would be written."""
757:    if runs_dir is None:
762:    d = pathlib.Path(runs_dir)
768:def live_metrics(pipeline, backend, text, runs=3, runs_dir=None):
769:    """Exactly 3 runs are required (R-CO-7). Any other count is recorded as not_measured with the reason and can never satisfy the bar.
770:    With runs_dir each run's artifact (run1.json ..) is written there, and a mismatch lists the differing fields and items."""
771:    if runs != 3:
772:        why = f"runs={runs}; exactly 3 live runs are required"
773:        return {"determinism_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["determinism_3run"]),
774:                "unsupported_count_3run": dict(NOT_MEASURED, runs=runs, reason=why, r_ids=RIDS["unsupported_count_3run"])}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:20:27.636Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && python3 -I -c \"\nimport json,glob,collections\ntot=collections.Counter()\nfor f in sorted(glob.glob('evals/reports/runs/20261102T161327Z/case_*.json')):\n    d=json.load(open(f))\n    its=d['items']\n    c=collections.Counter()\n    for it in its:\n        c[(it.get('kind') or it.get('type'), it.get('state'))]+=1\n    tot.update(c)\nprint(list(its[0].keys()) if its else None)\nprint(sorted(tot.items(), key=str))\n\"",
 "description": "Tally item states in the cited run folder"
}
````

### User / tool · 2026-11-02T17:20:27.770Z

**tool result**
````
['date', 'date_status', 'generator_prompt_version', 'id', 'judge', 'kind', 'provider', 'reasons', 'record_ids', 'state', 'summary_sha']
[(('amount', 'needs_review'), 4), (('amount', 'verified'), 7), (('entry', 'needs_review'), 3), (('entry', 'verified'), 44), (('flag', 'needs_review'), 3), (('flag', 'rejected'), 5), (('flag', 'verified'), 11), (('undated_entry', 'needs_review'), 1)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:20:47.758Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && grep -rn \"def test_committed_report_is_valid_when_present\\|def test_check_fresh_fails_on_a_hand_edited\\|def test_check_fresh_fails_on_an_edited_calibration_sentence\" tests/ ; grep -n \"^CAL_BACKENDS\\|^def _assert\\|test_committed_calibration_is_bound\\|raise\\b\" tests/unit/test_eval_runner.py | head; echo; sed -n 799p tests/unit/test_eval_runner.py; sed -n 805p tests/unit/test_eval_runner.py; sed -n 820p tests/unit/test_eval_runner.py; sed -n 850p tests/unit/test_eval_runner.py; grep -n 'got\\[\"table\"\\] == want\\|got\\[\"sentences\"\\] ==\\|times\" in c\\[\"sentences\"\\]' tests/unit/test_eval_runner.py",
 "description": "Locate related tests and exact line numbers for mutants"
}
````

### User / tool · 2026-11-02T17:20:47.910Z

**tool result**
````
tests/unit/test_calibration_route.py:81:def test_committed_report_is_valid_when_present():
tests/unit/test_eval_runner.py:931:def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
tests/unit/test_eval_runner.py:949:def test_check_fresh_fails_on_an_edited_calibration_sentence(tmp_path):
181:    """A crash in the code rung (grounding.check_summary) must raise, not silently leave the judge alone."""
183:        raise RuntimeError("code rung broke")
674:        raise AssertionError("the pipeline ran although --write-calibration was refused")
713:        raise AssertionError("controls ran although --write-calibration --controls was refused")
799:CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
802:def _assert_calibration_header(c):
1103:def test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts():
1141:        test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts()

CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
    assert c["source_tree_clean"] is True, "calibration source tree is not clean"
        monkeypatch.setattr(sys.modules[__name__], "CAL", p)
    _require_source_commit(c)
1112:    assert got["sentences"] == [c["sentences"]["overall"]["verified"], c["sentences"]["overall"]["needs_review"]], f"{rep.name} overall counts differ from calibration.json"
1114:    assert got["table"] == want, f"{rep.name} per-type counts differ from calibration.json"
1116:        assert f"{c['by_state'][s]['matched']}/{c['by_state'][s]['total']} times" in c["sentences"]["overall"][s], "by_state disagrees with its own sentence"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:21:23.654Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe.py",
 "content": "\"\"\"T-169 r2 probe (staff-engineer-reviewer), run with: python3 -I t169r2_probe.py <scratch clone detached at 6e1294f>\n\nForges evals/reports/calibration.json and mutates tests/unit/test_eval_runner.py inside the scratch clone only,\nruns the calibration tests, restores the exact bytes, and checks the restore. Nothing is written to the project tree.\n\"\"\"\nimport hashlib\nimport json\nimport pathlib\nimport shutil\nimport subprocess\nimport sys\n\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCLONE = pathlib.Path(sys.argv[1]).resolve()\nCAL = CLONE / \"evals/reports/calibration.json\"\nTEST = CLONE / \"tests/unit/test_eval_runner.py\"\nNODES = [\n    \"tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit\",\n    \"tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree\",\n    \"tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts\",\n    \"tests/unit/test_eval_runner.py::test_committed_calibration_run_directory_exists_with_every_case\",\n    \"tests/unit/test_eval_runner.py::test_report_binding_fails_on_a_coordinated_count_and_sentence_edit\",\n    \"tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes\",\n    \"tests/unit/test_eval_runner.py::test_check_fresh_fails_on_an_edited_calibration_sentence\",\n    \"tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present\",\n]\nREGEN = [\"tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit\"]\n\n\ndef sha(b):\n    return hashlib.sha256(b).hexdigest()[:16]\n\n\ndef pytest_run(label, nodes=NODES, cwd=CLONE):\n    p = subprocess.run([PY, \"-m\", \"pytest\", *nodes, \"-q\", \"-p\", \"no:cacheprovider\", \"--tb=line\", \"-rfEs\"],\n                       cwd=str(cwd), capture_output=True, text=True, timeout=900)\n    out = p.stdout.splitlines()\n    summ = out[-1] if out else p.stderr[-300:]\n    flagged = [l for l in out if l.startswith((\"FAILED\", \"SKIPPED\", \"ERROR\"))]\n    print(f\"== {label}\\n   rc={p.returncode} :: {summ}\")\n    for l in flagged:\n        print(\"   \" + l[:240])\n    sys.stdout.flush()\n    return p.returncode\n\n\norig_cal = CAL.read_bytes()\norig_test = TEST.read_bytes()\nprint(\"pristine calibration.json sha256[:16]\", sha(orig_cal), \"test file sha256[:16]\", sha(orig_test))\n\n\ndef forge(label, fn, nodes=NODES):\n    c = json.loads(orig_cal)\n    fn(c)\n    CAL.write_text(json.dumps(c, indent=1))\n    try:\n        return pytest_run(label, nodes)\n    finally:\n        CAL.write_bytes(orig_cal)\n        assert CAL.read_bytes() == orig_cal, \"calibration restore failed\"\n\n\ndef mutate_line(label, needle, replacement, nodes=NODES, forge_fn=None):\n    lines = orig_test.decode().split(\"\\n\")\n    hits = [i for i, l in enumerate(lines) if needle in l]\n    assert len(hits) == 1, (label, needle, hits)\n    lines[hits[0]] = replacement\n    TEST.write_text(\"\\n\".join(lines))\n    try:\n        if forge_fn is None:\n            return pytest_run(label, nodes)\n        return forge(label, forge_fn, nodes)\n    finally:\n        TEST.write_bytes(orig_test)\n        assert TEST.read_bytes() == orig_test, \"test restore failed\"\n\n\nprint(\"\\n### A. calibration.json forges on the pristine test file (expect each to fail the binding tests)\")\nforge(\"A1 by_state.verified.matched 82->83 only\", lambda c: c[\"by_state\"][\"verified\"].__setitem__(\"matched\", 83))\nforge(\"A2 by_type.entry.verified.matched 52->53 only\", lambda c: c[\"by_type\"][\"entry\"][\"verified\"].__setitem__(\"matched\", 53))\nforge(\"A3 by_type.amount.verified.matched 9->8 only\", lambda c: c[\"by_type\"][\"amount\"][\"verified\"].__setitem__(\"matched\", 8))\nforge(\"A4 sentences.overall.verified 82/83 -> 83/83 only\",\n      lambda c: c[\"sentences\"][\"overall\"].__setitem__(\"verified\", c[\"sentences\"][\"overall\"][\"verified\"].replace(\"82/83\", \"83/83\")))\nforge(\"A5 by_state.needs_review.matched 11->10 only\", lambda c: c[\"by_state\"][\"needs_review\"].__setitem__(\"matched\", 10))\nforge(\"A6 generated_at moved to a report that does not exist\", lambda c: c.__setitem__(\"generated_at\", \"2026-11-02T16:40:39Z\"))\n\n\ndef coordinated(c):\n    c[\"by_state\"][\"verified\"][\"matched\"] = 83\n    c[\"sentences\"][\"overall\"][\"verified\"] = c[\"sentences\"][\"overall\"][\"verified\"].replace(\"82/83\", \"83/83\")\n\n\nforge(\"A7 coordinated by_state + sentence 83/83 (file-level)\", coordinated)\n\nprint(\"\\n### B. test-file mutants on pristine calibration.json (expect killed unless noted)\")\nmutate_line(\"B1 drop the per-type table assertion\", 'assert got[\"table\"] == want', \"    pass\")\nmutate_line(\"B2 drop the overall sentence assertion\", 'assert got[\"sentences\"] == [', \"    pass\")\nmutate_line(\"B3 drop the by_state-vs-sentence assertion\", \"by_state disagrees with its own sentence\", \"        pass\")\nmutate_line(\"B4 CAL_BACKENDS shrunk to fixture only (F3 check)\", 'CAL_BACKENDS = (\"fixture\", \"claude-cli\")',\n            'CAL_BACKENDS = (\"fixture\",)  # mutant')\nmutate_line(\"B5 clean-tree message removed (F3 check)\", 'assert c[\"source_tree_clean\"] is True, \"calibration source tree is not clean\"',\n            '    assert c[\"source_tree_clean\"] is True')\n\nprint(\"\\n### C. F5: regen skip condition, unknown backend 'foo' in the header\")\n\n\ndef unknown_backend(c):\n    c[\"backend\"] = \"foo\"\n\n\nforge(\"C1 fixed test file, backend foo (expect regen runs and fails, not skipped)\", unknown_backend, REGEN)\nmutate_line(\"C2 reverted skip condition, backend foo (expect SKIPPED: the bug F5 named)\",\n            'if c[\"backend\"] == \"claude-cli\":', '    if c[\"backend\"] != \"fixture\":', REGEN, unknown_backend)\n\nprint(\"\\n### D. run-folder binding: the report names its run folder at line 131; test picks the newest run <= report id\")\nrep_line = [l for l in (CLONE / \"evals/reports/20261102T164038Z.md\").read_text().splitlines() if \"per-run artifacts\" in l]\nprint(\"report names:\", rep_line)\nRUN_NODE = [\"tests/unit/test_eval_runner.py::test_committed_calibration_run_directory_exists_with_every_case\"]\npytest_run(\"D1 baseline clone: cited folder 161327Z present\", RUN_NODE)\nCLONE2 = CLONE.parent / \"clone_decoy\"\nif CLONE2.exists():\n    shutil.rmtree(CLONE2)\nshutil.copytree(CLONE, CLONE2, symlinks=True, ignore=shutil.ignore_patterns(\".git\"))\nruns = CLONE2 / \"evals/reports/runs\"\nshutil.rmtree(runs / \"20261102T161327Z\")\nshutil.copytree(CLONE / \"evals/reports/runs/20261102T161327Z\", runs / \"20261102T163000Z\")\nshutil.rmtree(runs / \"20261102T163000Z\")\nshutil.copytree(CLONE / \"evals/reports/runs/20261102T161327Z\", runs / \"20261102T163000Z\")\nprint(\"decoy copy: cited folder removed, decoy 20261102T163000Z holds\", len(list((runs / \"20261102T163000Z\").glob(\"*.json\"))), \"json files\")\npytest_run(\"D2 decoy copy: cited folder 161327Z MISSING, decoy 163000Z present\", RUN_NODE, cwd=CLONE2)\nshutil.rmtree(CLONE2)\n\nprint(\"\\nrestore check: calibration sha\", sha(CAL.read_bytes()) == sha(orig_cal), \"test sha\", sha(TEST.read_bytes()) == sha(orig_test))\n"
}
````

### User / tool · 2026-11-02T17:21:23.748Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:21:29.141Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; EVD=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2; cd $EVD && time python3 -I $EVD/t169r2_probe.py $SCR > $EVD/probe.log 2>&1; echo rc=$?; cat $EVD/probe.log",
 "description": "Run forge and mutation probe in scratch clone",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T17:21:49.402Z

**tool result**
````
real	0m20.156s
user	0m14.811s
sys	0m4.895s
rc=0
pristine calibration.json sha256[:16] 9eb5d63e5f5c4c34 test file sha256[:16] a2fa71c4f115d174

### A. calibration.json forges on the pristine test file (expect each to fail the binding tests)
== A1 by_state.verified.matched 82->83 only
   rc=1 :: 3 failed, 5 passed in 0.52s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
== A2 by_type.entry.verified.matched 52->53 only
   rc=1 :: 3 failed, 5 passed in 0.53s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
== A3 by_type.amount.verified.matched 9->8 only
   rc=1 :: 3 failed, 5 passed in 0.55s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
== A4 sentences.overall.verified 82/83 -> 83/83 only
   rc=1 :: 3 failed, 5 passed in 0.51s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
== A5 by_state.needs_review.matched 11->10 only
   rc=1 :: 3 failed, 5 passed in 0.48s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
== A6 generated_at moved to a report that does not exist
   rc=1 :: 2 failed, 6 passed in 0.53s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_report_binding_fails_on_a_coordinated_count_and_sentence_edit
== A7 coordinated by_state + sentence 83/83 (file-level)
   rc=1 :: 3 failed, 5 passed in 0.51s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts
   FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
   FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present

### B. test-file mutants on pristine calibration.json (expect killed unless noted)
== B1 drop the per-type table assertion
   rc=0 :: 8 passed in 0.61s
== B2 drop the overall sentence assertion
   rc=0 :: 8 passed in 0.55s
== B3 drop the by_state-vs-sentence assertion
   rc=0 :: 8 passed in 0.54s
== B4 CAL_BACKENDS shrunk to fixture only (F3 check)
   rc=1 :: 2 failed, 6 passed in 0.53s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
   FAILED tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree
== B5 clean-tree message removed (F3 check)
   rc=1 :: 1 failed, 7 passed in 0.52s
   FAILED tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree

### C. F5: regen skip condition, unknown backend 'foo' in the header
== C1 fixed test file, backend foo (expect regen runs and fails, not skipped)
   rc=1 :: 1 failed in 8.86s
   FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
== C2 reverted skip condition, backend foo (expect SKIPPED: the bug F5 named)
   rc=0 :: 1 skipped in 0.18s
   SKIPPED [1] tests/unit/test_eval_runner.py:854: committed calibration is a live foo measurement; exact regeneration needs the live backend

### D. run-folder binding: the report names its run folder at line 131; test picks the newest run <= report id
report names: ['- per-run artifacts: `evals/reports/runs/20261102T161327Z`']
== D1 baseline clone: cited folder 161327Z present
   rc=0 :: 1 passed in 0.13s
decoy copy: cited folder removed, decoy 20261102T163000Z holds 13 json files
== D2 decoy copy: cited folder 161327Z MISSING, decoy 163000Z present
   rc=0 :: 1 passed in 0.13s

restore check: calibration sha True test sha True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:15.619Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe2.py",
 "content": "\"\"\"T-169 r2 probe 2 (staff-engineer-reviewer): does a single binding sub-check get killed by the binding tests alone?\nRun as: python3 -I t169r2_probe2.py <scratch clone detached at 6e1294f>. Restores the clone bytes after every run.\"\"\"\nimport hashlib\nimport json\nimport pathlib\nimport subprocess\nimport sys\n\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCLONE = pathlib.Path(sys.argv[1]).resolve()\nCAL = CLONE / \"evals/reports/calibration.json\"\nTEST = CLONE / \"tests/unit/test_eval_runner.py\"\nBIND = [\n    \"tests/unit/test_eval_runner.py::test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts\",\n    \"tests/unit/test_eval_runner.py::test_report_binding_fails_on_a_coordinated_count_and_sentence_edit\",\n    \"tests/unit/test_eval_runner.py::test_committed_calibration_run_directory_exists_with_every_case\",\n]\n\n\ndef sha(b):\n    return hashlib.sha256(b).hexdigest()[:16]\n\n\ndef run(label, nodes):\n    p = subprocess.run([PY, \"-m\", \"pytest\", *nodes, \"-q\", \"-p\", \"no:cacheprovider\", \"--tb=line\"],\n                       cwd=str(CLONE), capture_output=True, text=True, timeout=600)\n    print(f\"== {label}\\n   rc={p.returncode} :: {p.stdout.strip().splitlines()[-1]}\")\n    sys.stdout.flush()\n\n\noc, ot = CAL.read_bytes(), TEST.read_bytes()\nprint(\"pristine\", sha(oc), sha(ot))\n\n\ndef forge_file(fn):\n    c = json.loads(oc)\n    fn(c)\n    CAL.write_text(json.dumps(c, indent=1))\n\n\ndef mut(needle, repl):\n    lines = ot.decode().split(\"\\n\")\n    hits = [i for i, l in enumerate(lines) if needle in l]\n    assert len(hits) == 1, (needle, hits)\n    lines[hits[0]] = repl\n    TEST.write_text(\"\\n\".join(lines))\n\n\ndef table_only(c):\n    c[\"by_type\"][\"entry\"][\"verified\"][\"matched\"] = 53\n\n\ndef sentence_only(c):\n    c[\"sentences\"][\"overall\"][\"verified\"] = c[\"sentences\"][\"overall\"][\"verified\"].replace(\"82/83\", \"83/83\")\n\n\ndef state_only(c):\n    c[\"by_state\"][\"verified\"][\"matched\"] = 83\n\n\ntry:\n    run(\"P0 pristine test, pristine calibration, binding tests\", BIND)\n    # Each pair: one sub-check removed from the test file, one forge that only that sub-check should catch.\n    mut('assert got[\"table\"] == want', \"    pass\")\n    forge_file(table_only)\n    run(\"P1 table check removed + table-only forge (A2 shape), binding tests\", BIND)\n    TEST.write_bytes(ot); CAL.write_bytes(oc)\n\n    mut('assert got[\"sentences\"] == [', \"    pass\")\n    forge_file(sentence_only)\n    run(\"P2 sentence check removed + sentence-only forge, binding tests\", BIND)\n    TEST.write_bytes(ot); CAL.write_bytes(oc)\n\n    mut(\"by_state disagrees with its own sentence\", \"        pass\")\n    forge_file(state_only)\n    run(\"P3 by_state check removed + by_state-only forge, binding tests\", BIND)\n    TEST.write_bytes(ot); CAL.write_bytes(oc)\nfinally:\n    TEST.write_bytes(ot)\n    CAL.write_bytes(oc)\n    print(\"restored\", sha(CAL.read_bytes()) == sha(oc), sha(TEST.read_bytes()) == sha(ot))\n"
}
````

### User / tool · 2026-11-02T17:22:15.734Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:19.180Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; EVD=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2; cd $EVD && python3 -I $EVD/t169r2_probe2.py $SCR > $EVD/probe2.log 2>&1; echo rc=$?; cat $EVD/probe2.log; echo \"--- clone status:\"; git -C $SCR status --short | head -5; echo \"(end status)\"; echo \"--- project calibration untouched:\"; git -C /Users/arsis/zlayt-pm-project diff --stat -- evals/reports/calibration.json | tail -1",
 "description": "Run binding sub-check escape probes in scratch clone",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T17:22:20.947Z

**tool result**
````
rc=0
pristine 9eb5d63e5f5c4c34 a2fa71c4f115d174
== P0 pristine test, pristine calibration, binding tests
   rc=0 :: 3 passed in 0.15s
== P1 table check removed + table-only forge (A2 shape), binding tests
   rc=0 :: 3 passed in 0.29s
== P2 sentence check removed + sentence-only forge, binding tests
   rc=1 :: 1 failed, 2 passed in 0.15s
== P3 by_state check removed + by_state-only forge, binding tests
   rc=0 :: 3 passed in 0.14s
restored True True
--- clone status:
(end status)
--- project calibration untouched:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:25.511Z

**tool call — Bash**
````
{
 "command": "echo \"--- DECISIONS/ASSUMPTIONS/SCOPE_CUTS mentions of 312efe6 or T-169:\"; grep -n \"312efe6\\|T-169\\|live calibration\\|calibration\" memory/DECISIONS.md memory/ORCHESTRATOR_DECISIONS.md memory/ASSUMPTIONS.md memory/SCOPE_CUTS.md 2>/dev/null | tail -15; echo \"--- commits 312efe6..6e1294f:\"; git rev-list --count 312efe6..6e1294f; echo \"--- changed files touching app/llm or judge parsing:\"; git diff --stat 312efe6 6e1294f -- app/llm app/backend evals | tail -15; echo \"--- 56004f0 and 235e135 in range?\"; git merge-base --is-ancestor 56004f0 312efe6 && echo \"56004f0 in 312efe6 history\" || echo \"56004f0 NOT in 312efe6 history\"; git merge-base --is-ancestor 235e135 312efe6 && echo \"235e135 in 312efe6 history\" || echo \"235e135 NOT in 312efe6 history\"; git log --oneline 312efe6..6e1294f -- app/llm app/backend/judge.py app/backend/pipeline.py evals | head -20",
 "description": "Check decision record and judge-parse changes since measured commit"
}
````

### User / tool · 2026-11-02T17:22:25.723Z

**tool result**
````
--- DECISIONS/ASSUMPTIONS/SCOPE_CUTS mentions of 312efe6 or T-169:
memory/SCOPE_CUTS.md:62:| debt | T-090 accepted with documented debt after 3 rounds (§7.4) | 3 rounds; calibration reproducible from its recorded commit. Major (serving route) moved to T-099; minor (no-.git copy skips provenance tests) carried. | see card | M3 |
--- commits 312efe6..6e1294f:
10
--- changed files touching app/llm or judge parsing:
 evals/reports/calibration.json                     |   59 +-
 .../20261102T161327Z/case_01_date_formats.json     |  543 +++++++++++
 .../20261102T161327Z/case_02_gap_boundaries.json   |  590 ++++++++++++
 .../20261102T161327Z/case_03_rate_and_ocr.json     |  423 +++++++++
 .../case_04_duplicates_no_amounts.json             |  242 +++++
 .../case_05_provider_conflict.json                 |  364 +++++++
 .../case_06_subtle_pre_existing.json               |  411 ++++++++
 .../20261102T161327Z/case_07_prompt_injection.json |  476 ++++++++++
 .../case_08_diagnosis_temptation.json              |  279 ++++++
 .../case_09_nonvisit_hides_gap.json                |  364 +++++++
 evals/reports/runs/20261102T161327Z/run1.json      | 1002 ++++++++++++++++++++
 evals/reports/runs/20261102T161327Z/run2.json      | 1002 ++++++++++++++++++++
 evals/reports/runs/20261102T161327Z/run3.json      | 1002 ++++++++++++++++++++
 evals/reports/runs/20261102T161327Z/sample.json    | 1002 ++++++++++++++++++++
 28 files changed, 8213 insertions(+), 60 deletions(-)
--- 56004f0 and 235e135 in range?
56004f0 NOT in 312efe6 history
235e135 NOT in 312efe6 history
56004f0 fix(backend): T-168 r2 the closing-object JSON read is opt-in and extract-only; every judge (j1-j4) and other step parses strictly, two objects in a reply is INVALID_JSON
7cfdb0b test(qa): M2 re-gate live evidence: claude-cli 3-run at 312efe6 clean, ship_bar_met True, controls gate included, live calibration regenerated, letter_check 0
235e135 fix(backend): T-168 lib01 record 3 recorded live (claude-cli): extract + judge 1 answers; a reply that ends with its corrected JSON object is read as that object (earlier draft ignored)
56d746c fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:31.042Z

**tool call — Bash**
````
{
 "command": "git log --oneline 312efe6..6e1294f; echo \"--- code diff stat (app/ evals/*.py docs/ memory/ tests/):\"; git diff --stat 312efe6 6e1294f -- app evals/*.py app/llm | tail -20; echo \"--- hashes of prompts/lexicon at 312efe6 vs 6e1294f:\"; for f in app/llm/lexicon.yaml app/llm/prompts/judge_flag_v3.md app/llm/prompts/judge_conflict_v6.md app/llm/prompts/extract_v1.md; do a=$(git rev-parse 312efe6:$f 2>/dev/null); b=$(git rev-parse 6e1294f:$f 2>/dev/null); echo \"$f $([ \"$a\" = \"$b\" ] && echo same || echo DIFFERENT)\"; done",
 "description": "List commits since measured source and code diff stat"
}
````

### User / tool · 2026-11-02T17:22:31.103Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: git log --oneline 312efe6..6e1294f; echo "--- code diff stat (app/ evals/*.py docs/ memory/ tests/):"; git diff --stat 312efe6 6e1294f -- app evals/*.py app/llm | tail -20; echo "--- hashes of prompts
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:32.740Z

**tool call — Bash**
````
{
 "command": "git log --oneline 312efe6..6e1294f && git diff --stat 312efe6 6e1294f -- app evals/run.py | tail -20",
 "description": "List commits since measured source and app code diff stat"
}
````

### User / tool · 2026-11-02T17:22:32.870Z

**tool result**
````
6e1294f test(qa): bind live calibration to its report and run dir; dirty-tree test matches its message (T-169 r2)
2bfd396 feat(backend): T-171 D-064 every amount says why it is not counted (not_counted_reason, countable); count action with confirm separate_charge makes a held-back ledger line an accepted charge
8398bee docs(orchestrator): D-064 two kinds of not-counted amounts; missing-detail lines countable with a named confirm
5ed37ad test(qa): accept live claude-cli calibration header; keep clean-tree check (T-169)
56004f0 fix(backend): T-168 r2 the closing-object JSON read is opt-in and extract-only; every judge (j1-j4) and other step parses strictly, two objects in a reply is INVALID_JSON
7cfdb0b test(qa): M2 re-gate live evidence: claude-cli 3-run at 312efe6 clean, ship_bar_met True, controls gate included, live calibration regenerated, letter_check 0
235e135 fix(backend): T-168 lib01 record 3 recorded live (claude-cli): extract + judge 1 answers; a reply that ends with its corrected JSON object is read as that object (earlier draft ignored)
56d746c fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses
da6afb2 feat(backend): plain wording, no reason codes or test-mode text in paralegal-facing sentences or the notes (T-167, audit F4/F7)
f7a8f2a feat(frontend): T-149 r3 Do this first names the item and Start review goes to it, New case button, case checks never green while items are unreviewed, j/k hint, list skeleton and plain error, phone puts the jump strip and case checks under the entries
 app/backend/amounts.py           | 77 ++++++++++++++++++++++++++++++++++
 app/backend/calibration_route.py |  4 +-
 app/backend/count_charge.py      | 90 ++++++++++++++++++++++++++++++++++++++++
 app/backend/export.py            | 20 +++++----
 app/backend/pipeline.py          | 29 +++++++++++--
 app/backend/present.py           | 36 +++++++++++++---
 app/backend/reclassify.py        |  2 +-
 app/backend/review.py            |  7 +++-
 app/backend/trace.py             |  6 ++-
 app/backend/why.py               | 26 +++++++++---
 app/frontend/input.js            |  3 +-
 app/frontend/overview.css        | 42 ++++++++++++++++++-
 app/frontend/overview.js         | 65 +++++++++++++++++++++++------
 app/frontend/stepper.js          |  8 +++-
 app/llm/_types.py                | 57 +++++++++++++++++++++++--
 app/llm/audited.py               |  7 +++-
 app/llm/backends/claude_cli.py   |  2 +-
 17 files changed, 430 insertions(+), 51 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:46.489Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe3.py",
 "content": "\"\"\"T-169 r2 probe 3 (staff-engineer-reviewer): does the deterministic fixture eval give the same calibration counts at the\nmeasured source commit 312efe6 as at the reviewed commit 6e1294f? Run as: python3 -I t169r2_probe3.py <scratch clone>.\nExports each commit with git archive into its own scratch dir, runs evals.run --out with the fixture backend (the same env the\ncommitted regen test uses), and compares by_state, by_type and sentences. Read-only on the project tree.\"\"\"\nimport json\nimport os\nimport pathlib\nimport subprocess\nimport sys\n\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCLONE = pathlib.Path(sys.argv[1]).resolve()\nWORK = CLONE.parent / \"probe3\"\nSHAS = [\"312efe6\", \"6e1294f\"]\n\n\ndef export(sha):\n    d = WORK / sha\n    if d.exists():\n        subprocess.run([\"rm\", \"-rf\", str(d)], check=True)\n    d.mkdir(parents=True)\n    tar = subprocess.run([\"git\", \"archive\", sha], cwd=str(CLONE), capture_output=True, check=True).stdout\n    subprocess.run([\"tar\", \"-x\", \"-C\", str(d)], input=tar, check=True)\n    return d\n\n\nresults = {}\nfor sha in SHAS:\n    src = export(sha)\n    out = WORK / f\"out_{sha}\"\n    env = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    env[\"PYTHONPATH\"] = str(src)\n    r = subprocess.run([PY, \"-m\", \"evals.run\", \"--out\", str(out)], cwd=str(src), env=env, capture_output=True, text=True, timeout=900)\n    found = [p for p in [out / \"calibration.json\", *sorted((out / \"runs\").glob(\"*/calibration.json\"))] if p.exists()]\n    print(f\"{sha}: rc={r.returncode} calibration files={[str(p.relative_to(WORK)) for p in found]}\")\n    if len(found) != 1:\n        print((r.stdout[-400:] + r.stderr[-400:]))\n        continue\n    c = json.loads(found[0].read_text())\n    results[sha] = c\n    print(f\"  by_state verified {c['by_state']['verified']['matched']}/{c['by_state']['verified']['total']}, needs_review {c['by_state']['needs_review']['matched']}/{c['by_state']['needs_review']['total']}\")\n    print(\"  by_type\", {t: {s: f\"{c['by_type'][t][s]['matched']}/{c['by_type'][t][s]['total']}\" for s in ('verified', 'needs_review')} for t in ('entry', 'amount', 'flag')})\n    print(\"  source_commit\", c.get(\"source_commit\"), \"backend\", c.get(\"backend\"))\n\nif len(results) == 2:\n    a, b = (results[s] for s in SHAS)\n    skip = {\"generated_at\", \"source_commit\", \"source_tree_clean\", \"source_tree\"}\n    print(\"by_state equal:\", a[\"by_state\"] == b[\"by_state\"])\n    print(\"by_type equal:\", a[\"by_type\"] == b[\"by_type\"])\n    print(\"sentences equal:\", a[\"sentences\"] == b[\"sentences\"])\n    print(\"hashes equal:\", a.get(\"hashes\") == b.get(\"hashes\"))\n    print(\"all non-git fields equal:\", {k: v for k, v in a.items() if k not in skip} == {k: v for k, v in b.items() if k not in skip})\n"
}
````

### User / tool · 2026-11-02T17:22:46.587Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe3.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:22:49.460Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; EVD=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2; cd $EVD && python3 -I $EVD/t169r2_probe3.py $SCR > $EVD/probe3.log 2>&1; echo rc=$?; cat $EVD/probe3.log",
 "description": "Compare fixture eval counts at 312efe6 and 6e1294f",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T17:23:06.699Z

**tool result**
````
rc=0
312efe6: rc=1 calibration files=['out_312efe6/runs/20261102T172250Z/calibration.json']
  by_state verified 82/83, needs_review 11/11
  by_type {'entry': {'verified': '52/53', 'needs_review': '4/4'}, 'amount': {'verified': '9/9', 'needs_review': '6/6'}, 'flag': {'verified': '21/21', 'needs_review': '1/1'}}
  source_commit None backend fixture
6e1294f: rc=1 calibration files=['out_6e1294f/runs/20261102T172258Z/calibration.json']
  by_state verified 82/83, needs_review 11/11
  by_type {'entry': {'verified': '52/53', 'needs_review': '4/4'}, 'amount': {'verified': '9/9', 'needs_review': '6/6'}, 'flag': {'verified': '21/21', 'needs_review': '1/1'}}
  source_commit None backend fixture
by_state equal: True
by_type equal: True
sentences equal: True
hashes equal: True
all non-git fields equal: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:23:11.430Z

**tool call — Bash**
````
{
 "command": "git diff 312efe6 6e1294f -- app/llm/_types.py app/llm/backends/claude_cli.py app/llm/audited.py | head -150",
 "description": "Read judge-reply parsing diff since measured commit"
}
````

### User / tool · 2026-11-02T17:23:11.618Z

**tool result**
````
diff --git a/app/llm/_types.py b/app/llm/_types.py
index a56b252..fcef667 100644
--- a/app/llm/_types.py
+++ b/app/llm/_types.py
@@ -1,4 +1,6 @@
 """Shared provider types, JSON parsing and a small JSON-Schema checker (no jsonschema dependency). ADR-004."""
+import contextlib
+import contextvars
 import json
 import re
 from dataclasses import dataclass, field
@@ -34,9 +36,32 @@ class LLMResult:
 
 _FENCE = re.compile(r"^```(?:json)?\s*\n(.*)\n```\Z", re.S)
 
+# T-168 r2: the lenient "take the closing object" read is OPT-IN and belongs to the extract call only (audited_call turns it on for the extract
+# steps). A contextvar, not a parameter, so the 4-argument complete_with_meta seam (and every fake of it) is unchanged; it is per thread/context,
+# set and reset around exactly one provider call, and defaults to off.
+_LENIENT = contextvars.ContextVar("lenient_json_reply", default=False)
 
-def parse_json_reply(text: str) -> dict:
-    """Reply must be exactly one JSON object, bare or in one ```json fence; anything else is LLMError."""
+
+@contextlib.contextmanager
+def lenient_json():
+    """Within this block parse_json_reply may take the closing object of a reply that drafted, said 'Wait', and corrected itself. Extract call only."""
+    tok = _LENIENT.set(True)
+    try:
+        yield
+    finally:
+        _LENIENT.reset(tok)
+
+
+def lenient_json_enabled() -> bool:
+    return _LENIENT.get()
+
+
+def parse_json_reply(text: str, *, lenient: bool = None) -> dict:
+    """STRICT by default: the reply must be exactly one JSON object, bare or in one ```json fence; anything else (a second object, prose, a
+    truncated object) is LLMError INVALID_JSON. Every judge (j1-j4) and every non-extract step parses this way: a reply holding two objects with
+    different verdicts is a judge that is unavailable, never a silent choice of the later one.
+    lenient=True (or inside `with lenient_json():`, which the extract call alone uses) also accepts a reply that drafts an object, thinks aloud, and
+    ends with its corrected object; see _closing_object for exactly what counts."""
     t = (text or "").strip()
     m = _FENCE.match(t)
     if m:
@@ -44,12 +69,38 @@ def parse_json_reply(text: str) -> dict:
     try:
         obj = json.loads(t)
     except (ValueError, TypeError):
-        raise LLMError("INVALID_JSON: reply is not a single JSON object") from None
+        obj = _closing_object(t) if (_LENIENT.get() if lenient is None else lenient) else None
+        if obj is None:
+            raise LLMError("INVALID_JSON: reply is not a single JSON object") from None
     if not isinstance(obj, dict):
         raise LLMError("INVALID_JSON: reply is not a JSON object")
     return obj
 
 
+def _closing_object(t: str):
+    """Lenient (extract-only) read, T-168: a reply that thinks aloud and then states its final answer ("{...} Wait, that is wrong. Corrected output: {...}")
+    ends with one JSON object. That closing object is the answer; earlier complete objects are the model's own discarded drafts. Rules:
+      - scan left to right; a complete object that does not end the reply is skipped whole (its inner braces are never tried);
+      - a '{' that is not valid JSON in the middle of prose ("Wait {see above}") is skipped;
+      - a '{' whose object runs out of text (truncated reply, or a cut-off closing object) ends the scan: INVALID_JSON, no inner object is salvaged;
+      - the answer is an object that runs to the very end of the reply; trailing prose after it, or a non-object, is INVALID_JSON.
+    Schema, grounding and the judges still check what comes out. Never used for a judge."""
+    dec = json.JSONDecoder()
+    i = t.find("{")
+    while i != -1:
+        try:
+            obj, end = dec.raw_decode(t, i)
+        except json.JSONDecodeError as e:
+            if e.pos >= len(t):          # ran out of text: an unterminated object, not a stray brace
+                return None
+            i = t.find("{", i + 1)
+            continue
+        if isinstance(obj, dict) and end == len(t):
+            return obj
+        i = t.find("{", end)
+    return None
+
+
 _ANNOTATIONS = {"title", "description", "default", "examples", "$schema", "$id", "$defs", "definitions", "format"}
 _KEYWORDS = _ANNOTATIONS | {"type", "enum", "const", "required", "properties", "additionalProperties", "items", "$ref", "anyOf",
                             "maxLength", "minLength", "maximum", "minimum", "maxItems", "minItems"}
diff --git a/app/llm/audited.py b/app/llm/audited.py
index 288350a..27895e7 100644
--- a/app/llm/audited.py
+++ b/app/llm/audited.py
@@ -3,16 +3,18 @@
 1 attempt + 2 retries; every retry changes the request (stricter-format note in the user prompt); one llm_calls row per
 attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
 """
+import contextlib
 import logging
 import os
 import threading
 import time
 
 from app.db import db as DB
-from app.llm import provider as P
+from app.llm import _types as T, provider as P
 
 log = logging.getLogger("zlayt.llm")
 MAX_ATTEMPTS = 3
+LENIENT_JSON_STEPS = frozenset({"extract", "extract_es"})   # T-168 r2: the only steps whose reply may be read by its closing object; every judge and other step is strict
 _DB_LOCK = threading.Lock()   # one sqlite3 connection is shared by the worker threads; its cursors are not safe to interleave
 RETRY_DELAYS_S = (0.5, 1.5)
 # Errors that are retried: the provider layer gave up (LLMError: timeout, backend failure, invalid JSON, schema-invalid) or the transport did
@@ -77,7 +79,8 @@ def audited_call(conn, case_id: str, step: str, model: str, system: str, user: s
         t0 = time.monotonic()
         res, err, fixture_miss, bug = None, None, False, None
         try:
-            res = cwm(model, system, u, json_schema)
+            with (T.lenient_json() if step in LENIENT_JSON_STEPS else contextlib.nullcontext()):
+                res = cwm(model, system, u, json_schema)
             if validate is not None:
                 try:
                     validate(res.output)
diff --git a/app/llm/backends/claude_cli.py b/app/llm/backends/claude_cli.py
index a5b8025..a4379c9 100644
--- a/app/llm/backends/claude_cli.py
+++ b/app/llm/backends/claude_cli.py
@@ -64,7 +64,7 @@ def call(model: str, system: str, user: str, json_schema: dict, *, key: str = ""
     if not isinstance(env_json, dict) or env_json.get("is_error"):
         raise LLMError("BACKEND_FAILED claude-cli reported an error")
     text = env_json.get("result") or ""
-    out = parse_json_reply(text)
+    out = parse_json_reply(text)      # strict unless audited_call opened `lenient_json()` (extract steps only)
     mu = env_json.get("modelUsage") or {}
     resolved = next(iter(mu), model)
     u = mu.get(resolved, {}) if mu else {}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:23:59.619Z

**tool call — Bash**
````
{
 "command": "C=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r2/clone; cd $C && grep -n 'source tree is not clean\"\\|pytest.raises(AssertionError, match=\\|if c\\[\"backend\"\\] == \"claude-cli\"\\|def _report_for\\|def test_committed_calibration_is_bound\\|def test_committed_calibration_run_directory\\|runs = sorted\\|have = {p.stem\\|assert got\\[\"table\"\\]\\|assert got\\[\"sentences\"\\]\\|by_state disagrees\\|def test_report_binding\\|CAL_BACKENDS = \\|for backend in (\"fixture\"' tests/unit/test_eval_runner.py; echo; grep -c \"except\\|float(\\|sleep(\" <(git -C $C diff 5ed37ad 6e1294f -- tests/unit/test_eval_runner.py | grep \"^+\") ; cd /Users/arsis/zlayt-pm-project && git diff 5ed37ad 6e1294f -- tests/unit/test_eval_runner.py | grep \"^+\" | grep -c \"except\\|float(\\|sleep(\\|retry\\|http\"",
 "description": "Get exact line numbers and grep the r2 diff for banned patterns"
}
````

### User / tool · 2026-11-02T17:23:59.754Z

**tool result**
````
799:CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
805:    assert c["source_tree_clean"] is True, "calibration source tree is not clean"
815:    for backend in ("fixture", "claude-cli"):  # literal on purpose: shrinking CAL_BACKENDS must fail this test
821:        with pytest.raises(AssertionError, match="source tree is not clean"):
841:    with pytest.raises(AssertionError, match="does not exist"):
851:    if c["backend"] == "claude-cli":
1088:def _report_for(c):
1103:def test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts():
1112:    assert got["sentences"] == [c["sentences"]["overall"]["verified"], c["sentences"]["overall"]["needs_review"]], f"{rep.name} overall counts differ from calibration.json"
1114:    assert got["table"] == want, f"{rep.name} per-type counts differ from calibration.json"
1116:        assert f"{c['by_state'][s]['matched']}/{c['by_state'][s]['total']} times" in c["sentences"]["overall"][s], "by_state disagrees with its own sentence"
1119:def test_committed_calibration_run_directory_exists_with_every_case():
1124:    runs = sorted(d.name for d in (R.REPORTS / "runs").iterdir() if d.is_dir() and d.name <= rid)
1126:    have = {p.stem for p in (R.REPORTS / "runs" / runs[-1]).glob("*.json")}
1130:def test_report_binding_fails_on_a_coordinated_count_and_sentence_edit(tmp_path, monkeypatch):
1140:    with pytest.raises(AssertionError, match="differ from calibration.json"):

0
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:24:57.859Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer-r2.md",
 "content": "# T-169 round 2 review (staff-engineer-reviewer), commit 6e1294f\n\nScope: `tests/unit/test_eval_runner.py` at 6e1294f only (test-only card). Reviewed in a fresh `git clone` detached at 6e1294f, in the session scratchpad (`T169_staff_r2/clone`), status clean. The project tree's HEAD is 28437b2 at review time; these findings are for 6e1294f.\n\nVerdict: **changes** (0 blockers, 1 major, 2 minors). Count binding and forge detection work, and the two r1 minors F3 and F5 are closed. The run-folder binding does not do what the card and the orchestrator's round-2 request say: the test never reads the run folder the report names, and it still passes when that folder is deleted. The r1 F4 minor is not closed.\n\nBrief checks:\n- Ties to report 20261102T164038Z.md: yes. The link is derived from `generated_at`, and the test compares the report's sentences, per-type table, backend and source commit with the file. Seven forges of `calibration.json` each turn at least one binding or route test red (probe.log section A).\n- Ties to the run folder: no. The brief's `runs/20261102T161327Z` is `evals/reports/runs/20261102T161327Z` in the tree. The test picks the newest folder at or before the report id and checks file-name presence only. See F1.\n- Forged counts fail: yes, A1 to A7.\n- Minors: F3 fixed, F5 fixed, F4 not closed (F3 below).\n- `tests/unit/test_eval_runner.py`: 111 passed, 1 skipped in the clone. The skip is the live regen test (line 851).\n- Not counted: the r1 F1 red e2e test (T-166), per the brief.\n\n## Findings\n\n**F1 major (round 2), the run binding picks \"the newest folder at or before the report id\", not the folder the report names.** `tests/unit/test_eval_runner.py:1124-1126` sorts `runs/<id>` folders with `d.name <= rid` and checks `runs[-1]` for the ten case stems. The report itself names its folder at `evals/reports/20261102T164038Z.md:131`: \"per-run artifacts: `evals/reports/runs/20261102T161327Z`\". The test never reads that line. Probe D2 deletes `evals/reports/runs/20261102T161327Z` in a copy, adds `runs/20261102T163000Z` with the same ten case files, and runs `test_committed_calibration_run_directory_exists_with_every_case`: `1 passed` (probe.log, section D). Today the test passes only because no other folder falls between 161327Z and 164038Z. Why it matters: r1 F2 was about live counts with no test binding them to a run. A run folder can be deleted or replaced without a red test. Fix: take the run id from the report's \"per-run artifacts\" line (or record it in the header), assert that exact folder exists and holds all ten case files, and keep the newest-folder rule out. Acceptance: in a clone, delete `evals/reports/runs/20261102T161327Z` and add `runs/20261102T163000Z` with the ten case files; the run test must fail and name 161327Z.\n\n**F2 minor (round 2), the binding tests do not pin the table or by_state comparisons on their own.** Removing the per-type table assertion (line 1114) or the by_state-vs-sentence assertion (line 1116), and then forging only that dimension, leaves the three binding tests green: probe2.log P1 `3 passed` (table-only forge, `by_type.entry.verified.matched` 52 to 53) and P3 `3 passed` (by_state-only forge, `by_state.verified.matched` 82 to 83). The same forges are caught by `test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes` and `test_committed_report_is_valid_when_present` (probe.log A1, A2), so the suite as a whole is not blind to them. The binding test itself is only kill-tested by the coordinated forge. Fix: add single-dimension forge cases (table-only and by_state-only) to `test_report_binding_fails_on_a_coordinated_count_and_sentence_edit`. Acceptance: deleting line 1114 or line 1116 turns a single-dimension forge of the binding test red.\n\n**F3 minor (r1 F4 carried, not closed), the served live numbers describe 312efe6; the decision is only in a card note.** `grep -n` of `memory/DECISIONS.md`, `memory/ORCHESTRATOR_DECISIONS.md`, `memory/ASSUMPTIONS.md` and `memory/SCOPE_CUTS.md` for `312efe6`, `T-169` and `calibration` finds no decision entry for the gap (only a T-090 line in SCOPE_CUTS). The r1 fix was \"record the gap in memory/DECISIONS.md or re-measure\". The orchestrator note of 17:17:13Z is a rationale in the board, not a decision entry. Facts I checked: `git log --oneline 312efe6..6e1294f` lists 10 commits, including 56004f0 and 235e135 (judge parsing) and 2bfd396 (T-171, `app/backend/pipeline.py`, `count_charge.py`). `git diff 312efe6 6e1294f -- app/llm/_types.py app/llm/audited.py app/llm/backends/claude_cli.py` shows the closing-object read is opt-in and applies to the extract and extract_es steps only (`app/llm/audited.py`, `LENIENT_JSON_STEPS`); judges parse strictly. Mitigation: probe3.log shows that the fixture eval at 312efe6 and at 6e1294f gives identical by_state (82/83, 11/11), by_type, sentences and hashes. That covers the deterministic path only. The live extract path changed, and nothing in the card shows that it changes only the lib01 record-3 answer. Fix: write a decision entry in `memory/DECISIONS.md` naming 312efe6, the ten later commits, the identical fixture result and the live-only residual, or re-measure at HEAD. Acceptance: `grep -n 312efe6 memory/DECISIONS.md` finds the entry, or a live header at HEAD exists and the served sentence matches it.\n\nRound-1 minors closed:\n- F3 (dirty-tree negative test): line 805 has a message and line 821 matches it. Probe B4 (`CAL_BACKENDS` shrunk to fixture, line 799) turns the dirty-tree test red (2 failed); probe B5 (message removed) turns it red (1 failed). The literal tuple at line 815 is what makes B4 fail, as the comment says.\n- F5 (regen skip too broad): line 851 now skips only for `claude-cli`. Probe C2 (condition reverted) skips a header with backend `foo`; with the fix (C1) the regen test runs and fails.\n\nChecks with no finding: the r2 diff adds no `except`, `float(`, `sleep(`, retry, or network call (grep of the `+` lines: 0 matches). The regen skip is visible with its reason at line 853 and the fixture branch still runs.\n\n## What is right\n- Forged counts are caught: seven single or coordinated forges of `calibration.json` each turn a binding or route test red, and a dangling `generated_at` fails loudly (probe.log A1 to A7).\n- F3 and F5 are closed, and each has a mutant that proves it (B4, B5, C1, C2).\n- The report link fails loudly when the report is missing (A6), so the derived link is not silent.\n\n```json\n{\"card\": \"T-169\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 6e1294f, tests/unit/test_eval_runner.py (round 2); fresh clone detached at 6e1294f in the session scratchpad (T169_staff_r2/clone), status clean; project HEAD is 28437b2 at review time and was not used; cited run folder is evals/reports/runs/20261102T161327Z; sample case n/a (unit tests)\",\n \"exercised\": [\n   \"git rev-parse 6e1294f and git clone of the project into the scratchpad, detached at 6e1294f (6e1294f171cd1e9a3e82014a9d321286d1a527eb), git status clean\",\n   \"board.py show T-169 (round-1 findings, orchestrator notes 17:12:52Z and 17:17:13Z, handoff); read reviews/T-169-staff-engineer.md (round-1 F1 to F5)\",\n   \"git diff 5ed37ad 6e1294f -- tests/unit/test_eval_runner.py read in full; grep of the + lines for except, float(, sleep(, retry, http: 0 matches\",\n   \".venv/bin/python -m pytest tests/unit/test_eval_runner.py -q in the clone: 111 passed, 1 skipped (regen skip at line 851)\",\n   \".venv/bin/python -m pytest -v -k calibration subset in the clone: 25 passed, 1 skipped; the three new tests PASSED\",\n   \"git show 6e1294f:evals/reports/calibration.json and evals/reports/20261102T164038Z.md read in the clone: generated_at 2026-11-02T16:40:38Z, source 312efe6, backend claude-cli, by_state verified 82/83, needs_review 11/11; report line 131 names evals/reports/runs/20261102T161327Z\",\n   \"artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe.py -> probe.log: section A seven forges of calibration.json (by_state verified matched 83; by_type entry matched 53; by_type amount matched 8; sentence 83/83; by_state needs_review matched 10; generated_at moved to a missing report; coordinated by_state plus sentence): each rc=1, 2 or 3 failures; section B mutants B1 to B5; section C regen with backend foo (C1 fixed FAILED, C2 reverted SKIPPED); section D baseline 1 passed and decoy copy with the cited folder removed 1 passed; calibration and test sha256 restored (True, True)\",\n   \"artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe2.py -> probe2.log: binding-only node set; P0 pristine 3 passed; P1 table check removed plus table-only forge 3 passed; P2 sentence check removed plus sentence-only forge 1 failed; P3 by_state check removed plus by_state-only forge 3 passed; restored True True\",\n   \"artifacts/review-evidence/T-169-staff-engineer-r2/t169r2_probe3.py -> probe3.log: git archive of 312efe6 and 6e1294f, evals.run --out with the fixture backend (LLM_BACKEND and ENABLE_LIVE unset): by_state, by_type, sentences and hashes identical at both shas (rc=1 at both, not investigated)\",\n   \"git log --oneline 312efe6..6e1294f (10 commits); git diff 312efe6 6e1294f -- app/llm/_types.py app/llm/audited.py app/llm/backends/claude_cli.py: lenient read opt-in, extract and extract_es only; judges strict\",\n   \"grep -n 312efe6, T-169 and calibration over memory/DECISIONS.md, memory/ORCHESTRATOR_DECISIONS.md, memory/ASSUMPTIONS.md, memory/SCOPE_CUTS.md: no 312efe6 or T-169 decision entry\",\n   \"Not run: full pytest tests/unit (its one red test is T-166's, excluded by the brief)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"report_binding\": 4, \"run_binding\": 2, \"forged_count_detection\": 4, \"minors_closed\": 3, \"eval_runner_suite_green\": 5, \"honest_skips\": 4},\n \"findings\": [\n   {\"severity\": \"major\", \"title\": \"Run binding picks the newest run folder at or before the report id, not the folder the report names; a deleted cited folder still passes\",\n    \"evidence\": \"tests/unit/test_eval_runner.py:1124-1126 (runs = sorted(... if d.name <= rid); have = ... runs[-1]); evals/reports/20261102T164038Z.md:131 '- per-run artifacts: `evals/reports/runs/20261102T161327Z`'; probe.log section D: D2 cited folder removed, decoy runs/20261102T163000Z with the ten case files -> 1 passed\",\n    \"why_it_matters\": \"r1 F2 asked for a test that binds the live counts to a run. As written, any folder with the ten case stems at or before the report id satisfies it, so the cited run can be deleted or replaced with no red test. It passes today only because no other folder falls between 161327Z and 164038Z.\",\n    \"fix\": \"Take the run id from the report's 'per-run artifacts' line (or record it in the header); assert that exact folder exists and holds all ten case files; drop the newest-folder rule.\",\n    \"acceptance_test\": \"In a clone, delete evals/reports/runs/20261102T161327Z and add runs/20261102T163000Z with the ten case files; the run test fails and names 161327Z\"},\n   {\"severity\": \"minor\", \"title\": \"Binding tests do not pin the table or by_state comparisons on their own\",\n    \"evidence\": \"tests/unit/test_eval_runner.py:1114 (assert got[\\\"table\\\"] == want) and :1116 (by_state disagrees with its own sentence); probe2.log P1 3 passed (table-only forge), P3 3 passed (by_state-only forge); probe.log A1 and A2 caught only by test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes and test_committed_report_is_valid_when_present\",\n    \"why_it_matters\": \"A future edit that drops either comparison in the binding test is invisible to the binding tests; the other tests still catch the forges, so the gap is in the card's own test, not in the suite.\",\n    \"fix\": \"Add single-dimension forge cases (table-only, by_state-only) to the binding tests alongside the coordinated one.\",\n    \"acceptance_test\": \"Deleting line 1114 or line 1116 makes a single-dimension forge of test_committed_calibration_is_bound_to_a_report_that_exists_with_the_same_counts fail\"},\n   {\"severity\": \"minor\", \"title\": \"r1 F4 not closed: the live numbers at 312efe6 have no decision entry; the rationale is in a card note\",\n    \"evidence\": \"grep of memory/DECISIONS.md, ORCHESTRATOR_DECISIONS.md, ASSUMPTIONS.md, SCOPE_CUTS.md for 312efe6 or T-169: no entry; git log 312efe6..6e1294f = 10 commits incl. 56004f0, 235e135, 2bfd396; git diff 312efe6 6e1294f -- app/llm/audited.py: LENIENT_JSON_STEPS = frozenset({\\\"extract\\\", \\\"extract_es\\\"}); probe3.log: fixture counts identical at 312efe6 and 6e1294f\",\n    \"why_it_matters\": \"The served sentences describe code that is no longer at HEAD, and the disposition rests on the claim that extract-only leniency changes only the lib01 record-3 answer. The fixture path does not exercise the live lenient read, so the claim is unverified for the other nine golden cases.\",\n    \"fix\": \"Write a memory/DECISIONS.md entry naming 312efe6, the ten later commits, the identical fixture result and the live-only residual; or re-measure the live calibration at HEAD.\",\n    \"acceptance_test\": \"grep -n 312efe6 memory/DECISIONS.md finds the entry, or a live calibration header at HEAD exists and the served sentence matches it\"}\n ],\n \"whats_right\": [\n   \"Seven forges of calibration.json each turn a binding or route test red, and a dangling generated_at fails loudly (probe.log A1 to A7)\",\n   \"r1 F3 and F5 are closed: the clean-tree message and match (lines 805, 821) and the claude-cli-only skip (line 851) each have a mutant that proves them (B4, B5, C1, C2)\",\n   \"The diff adds no except, float(, sleep(, retry or network call; test_eval_runner.py is 111 passed, 1 skipped in a clean clone\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T17:24:58.018Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:01.108Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-169-staff-engineer-r2.md; echo \"rc=$?\"; python3 -c \"\nimport json,re\nt=open('reviews/T-169-staff-engineer-r2.md').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks', len(blocks))\nj=json.loads(blocks[0])\nprint(j['card'], j['persona'], j['model'], j['verdict'])\nprint([ (f['severity']) for f in j['findings']])\n\"",
 "description": "Validate the round-2 review file and parse its JSON block"
}
````

### User / tool · 2026-11-02T17:25:01.166Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:02.846Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-169-staff-engineer-r2.md; echo \"rc=$?\"",
 "description": "Validate the round-2 review file with the board validator"
}
````

### User / tool · 2026-11-02T17:25:02.990Z

**tool result**
````
ok (1 file(s))
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:05.370Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/parse_review.py",
 "content": "\"\"\"Parse the round-2 review: exactly one json fence, verdict by rule (blocker fail, major changes, else pass).\"\"\"\nimport json\nimport re\nimport sys\n\ntext = open(sys.argv[1], encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nj = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in j[\"findings\"]]\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", j[\"card\"], \"persona\", j[\"persona\"], \"model\", j[\"model\"])\nprint(\"findings\", sev)\nprint(\"verdict\", j[\"verdict\"], \"rule says\", rule, \"match\", j[\"verdict\"] == rule)\nprint(\"exercised entries\", len(j[\"exercised\"]), \"whats_right\", len(j[\"whats_right\"]))\n"
}
````

### User / tool · 2026-11-02T17:25:05.491Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer-r2/parse_review.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:06.886Z

**tool call — Bash**
````
{
 "command": "python3 -I artifacts/review-evidence/T-169-staff-engineer-r2/parse_review.py reviews/T-169-staff-engineer-r2.md",
 "description": "Parse review JSON block and check verdict against the rule"
}
````

### User / tool · 2026-11-02T17:25:07.005Z

**tool result**
````
json blocks: 1
card T-169 persona staff-engineer-reviewer model claude-haiku-5-5
findings ['major', 'minor', 'minor']
verdict changes rule says changes match True
exercised entries 12 whats_right 3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:17.085Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t169_r2_binding_patterns.md",
 "content": "---\nname: t169-r2-binding-patterns\ndescription: T-169 r2 6e1294f changes: report link derived from generated_at and killed by 7 forges; run binding picks newest folder not the one the report names (decoy passes); table and by_state sub-checks unpinned; r1 F4 decision missing\nmetadata:\n  type: project\n---\n\nT-169 r2 (commit 6e1294f, calibration binding tests in tests/unit/test_eval_runner.py): changes, 0 blockers, 1 major, 2 minors. Review at reviews/T-169-staff-engineer-r2.md.\n\n- **Report link is sound.** calibration.json has no run id or report field; the test derives the report from generated_at (16:40:38Z -> 20261102T164038Z.md). Seven single or coordinated forges of calibration.json each turned a binding or route test red; a dangling generated_at fails loudly.\n- **Run link is weak.** The report names its run folder at line 131 (\"per-run artifacts: evals/reports/runs/20261102T161327Z\"). The test picks the newest runs/<id> at or before the report id and checks file-name presence only. Decoy copy (cited folder deleted, runs/20261102T163000Z added with the same case files) still passes. It passes today only because no folder sits between 161327Z and 164038Z.\n- **Sub-checks unpinned by the binding set.** Removing the table assertion (line 1114) or the by_state-vs-sentence assertion (line 1116) and forging only that dimension leaves the three binding tests green; route and check_fresh tests still catch it.\n- **r1 F4 still open.** The \"no re-measure\" rationale is a card note, not a memory/DECISIONS.md entry. Fixture eval at 312efe6 and 6e1294f gives identical counts and hashes (probe3), but the lenient extract read (app/llm/audited.py, extract and extract_es only) is live-only and unverified for the other golden cases.\n- **Fixed minors:** dirty-tree match and message (lines 805, 821) and the claude-cli-only regen skip (line 851) each have a killing mutant.\n\n**How to apply:** when a card says a test ties an artifact to its evidence, read the reference the artifact names and assert that exact one; a newest-by-name pick passes after the cited evidence is deleted. See [[feedback_bind_to_named_reference]]. Method and earlier calibration patterns: [[project_t090_calibration_review_patterns]], [[project_eval_runner_review_patterns]].\n"
}
````

### User / tool · 2026-11-02T17:25:17.187Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t169_r2_binding_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:20.254Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_bind_to_named_reference.md",
 "content": "---\nname: bind-to-named-reference\ndescription: a test that ties an artifact to its evidence must read the reference the artifact names; \"newest folder by name\" passes after the cited evidence is deleted; prove it with a decoy copy\nmetadata:\n  type: feedback\n---\n\nRule: when a test links a committed artifact to its evidence (run folder, report, raw outputs), resolve the link through the reference the artifact itself names, then assert that exact evidence exists and matches. Do not pick \"the newest one that fits\" by name or timestamp.\n\n**Why:** T-169 r2 (6e1294f). The report named runs/20261102T161327Z, but the test took the newest run folder at or before the report id. Deleting the cited folder and adding a decoy with the same case files left the test green. The card's acceptance did not catch it because it was written as \"some run exists\".\n\n**How to apply:** for any \"binding\" or \"provenance\" test, run the decoy probe: copy the clone, delete the named evidence, add a same-shaped decoy with a different name, and require red. If the test stays green, the link is a heuristic. Related: [[project_t169_r2_binding_patterns]], [[project_t090_calibration_review_patterns]] (committed artifacts must be regenerated, not trusted).\n"
}
````

### User / tool · 2026-11-02T17:25:20.383Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_bind_to_named_reference.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:21.971Z

**tool call — Bash**
````
{
 "command": "tail -5 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md; wc -l .claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "description": "Check end of memory index before appending"
}
````

### User / tool · 2026-11-02T17:25:22.070Z

**tool result**
````
- [T-167 plain-wording patterns](project_t167_plain_wording_patterns.md) — r1 da6afb2 changes: AC universal grep overclaimed (qa calibration sentences), sibling commit reds e2e id contract, fallback doubles phrase
- [Reviewer scratch writes](feedback_reviewer_scratch_writes.md) — Write blocked in scratchpad; put helpers and evidence under artifacts/review-evidence; no backticks in shell lines
- [T-165 r2 patterns](project_t165_r2_patterns.md) — 56d746c pass: hand entry kept with rerun_note, m1-m3 killed, r1 minors carried, f7a8f2a e2e red out of scope
- [T-168 parser patterns](project_t168_parser_patterns.md) — r1 235e135 changes: closing-object parser is global (judge replies resolve last-wins), truncated sub-object accepted, boundary tests thin
- [GATE-M2 r2 patterns](project_gate_m2_r2_patterns.md) — 7cfdb0b changes: r1 fixes hold; suite red (live calibration vs fixture guards, e2e ids), run suite in a git clone, check-fresh rc 1
      98 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:24.257Z

**tool call — Bash**
````
{
 "command": "cat >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md <<'EOF'\n- [T-169 r2 binding patterns](project_t169_r2_binding_patterns.md) — 6e1294f changes: report link sound (7 forges killed), run link picks newest folder not the one the report names (decoy passes), r1 F4 decision missing\n- [Bind to named reference](feedback_bind_to_named_reference.md) — a binding test must read the reference the artifact names; newest-by-name passes after the cited evidence is deleted; run a decoy copy\nEOF\ntail -3 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "description": "Append two index lines to reviewer memory"
}
````

### User / tool · 2026-11-02T17:25:24.350Z

**tool result**
````
- [GATE-M2 r2 patterns](project_gate_m2_r2_patterns.md) — 7cfdb0b changes: r1 fixes hold; suite red (live calibration vs fixture guards, e2e ids), run suite in a git clone, check-fresh rc 1
- [T-169 r2 binding patterns](project_t169_r2_binding_patterns.md) — 6e1294f changes: report link sound (7 forges killed), run link picks newest folder not the one the report names (decoy passes), r1 F4 decision missing
- [Bind to named reference](feedback_bind_to_named_reference.md) — a binding test must read the reference the artifact names; newest-by-name passes after the cited evidence is deleted; run a decoy copy
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:26.813Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_reviewer_scratch_writes.md"
}
````

### User / tool · 2026-11-02T17:25:26.825Z

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
14	Related: [[project_t167_plain_wording_patterns]].
15	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:29.135Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_reviewer_scratch_writes.md",
 "old_string": "Related: [[project_t167_plain_wording_patterns]].",
 "new_string": "**T-169 r2 addendum:** `git clone` plus `git checkout --detach <sha>` was denied by board-guard when the clone sat under artifacts/review-evidence/ (\"reviewers may not run git checkout in the project\"). The same two commands worked in a clone under the session scratchpad (/private/tmp/...), so put pinned clones in the scratchpad and evidence in artifacts/review-evidence/. A python -c line containing backtick-escaped fences was also denied; use a .py file.\n\nRelated: [[project_t167_plain_wording_patterns]], [[feedback_bind_to_named_reference]]."
}
````

### User / tool · 2026-11-02T17:25:29.244Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_reviewer_scratch_writes.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:25:33.277Z

Round 2 of T-169 at 6e1294f is **changes** (0 blockers, 1 major, 2 minors): the report binding and forge detection work, but the run binding passes with the cited run folder deleted, and the r1 F4 decision is still unrecorded. Review: /Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer-r2.md
