# Subagent: T-165 review (T-165 review)

Source: `agent-a1ef77688f6691e68.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T16:13:46.377Z

Review board card T-165 (commit 312efe6) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-165` and reviews/T-161-staff-engineer-r2.md.

On a `git archive HEAD` copy, verify:
- a first run with the extract step down on any record reads run_partial, names those records, and the gate reads RUN_FAILED;
- a record entered by hand gives an ENTERED_BY_HAND warning instead;
- a run where every record extracted stays ready;
- a re-run keeps a pending hand-entered entry;
- the four changed pins in the T-161 and T-146 test files are justified.

Run the unit suite. The lib01 demo fixture gap is tracked separately as T-168.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-165-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:47.954Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T16:13:47.964Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:48.502Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-165 && echo ---- && cat reviews/T-161-staff-engineer-r2.md && echo ---- && git log --oneline -5 && git rev-parse HEAD && git show --stat 312efe6 | head -40",
 "description": "Show T-165 card, prior T-161 review, and recent commits"
}
````

### User / tool · 2026-11-02T16:13:48.713Z

**tool result**
````
---
id: "T-165"
title: "Partial extract on a first run: any record whose extract step failed makes the case run_partial with those records named (today 8 of 9 records down still reads 'ready'); orchestrator decision, not a Chris question"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T15:36:08Z"
updated_at: "2026-11-02T16:13:42Z"
claimed_by: "backend"
claimed_at: "2026-11-02T15:36:20Z"
rounds: 0
commits: ["312efe6"]
reviews: []
ac:
  - {"n": 1, "text": "first run with extract failing on N>=1 records -> run_partial naming the records, gate RUN_FAILED (or a named warning if the paralegal entered them by hand); all-records-ok stays ready; tests", "done": true, "evidence": "tests/unit/test_t165_partial_extract.py (one down, 8 of 9 down, all ok, hand-entered, undated boundary, hand entry after run, rerun keeps hand entry); 5 mutants killed; full tests/unit on git archive of HEAD + my hunks: 4961 passed, 8 skipped"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T15:36:10Z orchestrator: assigned: backend
- 2026-11-02T15:36:20Z backend: claimed
- 2026-11-02T16:13:26Z backend: AC 1 checked: tests/unit/test_t165_partial_extract.py (one down, 8 of 9 down, all ok, hand-entered, undated boundary, hand entry after run, rerun keeps hand entry); 5 mutants killed; full tests/unit on git archive of HEAD + my hunks: 4961 passed, 8 skipped
- 2026-11-02T16:13:33Z backend: moved in_progress -> in_review
- 2026-11-02T16:13:42Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: pipeline.py first-run extract failure is now run_partial naming the records (error.records, extract_only) with RUN_FAILED; a record the paralegal entered by hand is excluded and shown as an ENTERED_BY_HAND warning (GET case warnings[], run result); review.manual_entry calls PL.refresh_extract_error so entering the last failed record clears an extract-only failure to ready; _persist no longer sweeps a pending hand-entered entry whose record still has no AI entry on a re-run (it was deleted before: found by probe). api.md already carries the text (swept into ea988f8). Supersedes the T-161 r2 'failed only at zero entries' rule; the reviewer's 'not dated' mutant no longer exists, the boundary is pinned by the undated-entry test. · Verified: tests/unit/test_t165_partial_extract.py (11 tests), 5 mutants killed; full tests/unit on a git archive of HEAD + my hunks: 4961 passed, 8 skipped. Commit 312efe6 via temp index. · Surprised me: lib01 record 3 has no recorded extract answer at the current prompt (FIXTURE_MISS, key 83bcee07...), so every fixture-backend run of lib01 now reads failed/run_partial (also in the demo). I did not fabricate a fixture; 5 test files (test_api_routes.wait_ready allow_failed, new tests/unit/_hand_entry.py, test_case_list, test_t114, test_t139_charge_text) enter record 3 by hand. A real re-record of lib01 e3 (QA/T-139) would make those a no-op. Pins updated: T-161 (2), T-146 r3 (2). · Left: nobody committed untracked tests/fixtures/llm/*.json (38 files, not mine). Scratch note: I overwrote a few files (p.py, n.py, rec.py, scan.py, head/) in the shared scratchpad dir before noticing it is shared.

----
# T-161 staff-engineer review, round 2 (flag step read from failed_steps; extract-down first run with no entries is failed)

Reviewed commit 99438fb as contained in c0e2b86, on a `git archive` copy taken at c0e2b86. HEAD later moved to 67be38d; `git diff c0e2b86 HEAD --stat` for app/backend/pipeline.py, flags.py, tests/unit/test_t161_first_run_stage_down.py and the two T-146 test files is empty.

Verdict: **pass**. No blocker, no major. The round-1 blocker is closed: a first run with the flag step down on a note with no phrase-list hit now reads `failed | run_partial | RUN_FAILED` with the step named, and the export is blocked. Extract down with no entry at all on a first run reads failed with the step named. Two minors (one surviving mutant, one case that still reads ready) and one nit.

What I exercised (archive copy of c0e2b86, `.venv/bin/python`):
- `pytest tests/unit -q`: 4880 passed, 8 skipped (281 s). The T-161 file, both T-146 pin files and the T-146 re-run files pass.
- Round-1 repro, in-process (`PL.run_pipeline`, FakeCall) on the two-record plain note: flags down (LLMFailed) and flags fixture-miss both give `failed`, code `run_partial`, message "The AI step (finding the flags) failed on this run, so nothing from it could be used. Run it again to retry.", blockers `RUN_FAILED`. The golden sample with flags down still gives "The AI step failed for 7 items (finding the flags) on this run, and there is no earlier result to keep." (no double naming).
- Same repro through the API (TestClient POST /run, GET /status, accept both entries, GET /export): status `failed`, error run_partial as above, export 422 `export_blocked` with blocker `RUN_FAILED`. Round 1 had status ready and export 200.
- Extract matrix: all 9 records down gives failed with "9 items (writing the entries)"; 8 of 9 down gives `done_with_errors`, 1 entry, case `ready`, no error (the tray-shape rule, see question).
- Three flipped pins, read in full: see the section below.
- 9 mutants of pipeline.py (down always empty, flags never in failed_steps, drop the `named` dedupe, old extract filter, extract never filtered, `not dated` instead of `not (dated or undated)`, `_partial_error` ignoring `down`, wording without the step name, down on first run only) against the T-161 file and the T-146 r2, r3, r4 and re-run files: 8 killed, 1 survived (finding 1).
- Read `git show 99438fb` in full, and run_flag_pass, _noting, _failure and run_pipeline.

The three flipped pins (checked one by one):
- `test_t146_r2_failed_rerun_keeps_items.py` (renamed `test_first_run_with_extract_down_still_stores_its_stubs_and_is_failed_with_the_step_named`): still asserts 9 stored stub rows, all rejected with LLM_FAILED_AFTER_RETRIES; the only flip is `err is None / ready` to `failed`, `run_partial` and "(writing the entries)". Justified: it is exactly the decision the orchestrator made for r2; the stub assertions are kept.
- `test_t146_r3_decided_items_never_lowered.py` (`test_rerun_with_nothing_to_keep_still_says_the_step_failed`): `== ("ready", None)` became `case_error(...)[0] == "failed"`. Justified, but the status-only assertion is looser than the old exact tuple; the exact first-run message is pinned in test_t161 (`err == {...9 items (writing the entries)...}`) so nothing is lost. The re-run half of that test is unchanged and exact.
- The T-161 file's own extract-down test: rewritten from "unchanged ready" to the failed shape, and a partial-extract test added that keeps the old ready shape. Justified.
None of the three flips hides a regression: each moves one assertion to the behaviour the brief named, and the surrounding assertions still bite (mutants 4 and 5 are killed by these files).

Labels: both findings are test or edge gaps, not spec violations (minor). The nit is a defensive branch that the production call layer cannot reach.

```json
{"card": "T-161", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 99438fb within c0e2b86 (app/backend/pipeline.py hunk, tests/unit/test_t161_first_run_stage_down.py, test_t146_r2 and r3 pin flips) in a git archive copy; golden sample and a two-record plain synthetic note; HEAD later 67be38d with none of these files changed",
 "exercised": ["python3 tools/board.py show T-161; read reviews/T-161-staff-engineer.md", "git archive c0e2b86 copy: pytest tests/unit -q -> 4880 passed, 8 skipped", "git show 99438fb in full (pipeline.py, T-161 file, both T-146 files); git diff c0e2b86 HEAD --stat on these files: empty", "round-1 repro in-process: plain note with flags down (LLMFailed and fixture-miss) -> failed/run_partial/RUN_FAILED; sample with flags down -> one naming of the step", "API run: POST /run, GET /status, accept entries, GET /export on the plain note with flags down -> 422 export_blocked RUN_FAILED", "extract matrix: 9 of 9 down -> failed, 8 of 9 down -> ready with 1 entry", "9 pipeline.py mutants vs T-161 + T-146 r2/r3/r4/re-run files: 8 killed, 1 survived", "schema-invalid flag output via FakeCall on the plain note (ready), then read app/llm/provider.py:107 validate_schema"],
 "verdict": "pass",
 "scores": {"stage_coverage": 4, "gate_agreement": 5, "message_names_step": 5, "test_strength": 4, "pin_flips_justified": 5},
 "findings": [
  {"severity": "minor", "title": "Mutant survives: the 'no entry at all' test counts dated entries only",
   "evidence": "app/backend/pipeline.py:590 `empty if (rerun or not (dated or undated)) else ...`; change `not (dated or undated)` to `not dated` -> 134 passed (tests/unit/test_t161_first_run_stage_down.py + test_t146_r2/r3/r4/re-run files). Every extract-down test in the T-161 file produces dated entries or none.",
   "why_it_matters": "A first run where the only entry that came out is undated, and every other record failed extraction, must keep the tray shape (some entries came out). With the mutant it would read failed. The boundary of the new rule is unpinned.",
   "fix": "Add a first-run test with one record whose extract gives an undated entry and the rest down: case ready, failed records as tray items, no RUN_FAILED.",
   "acceptance_test": "The `not dated` mutant fails that test; HEAD passes it."},
  {"severity": "minor", "title": "A first run where extract fails for 8 of 9 records still reads ready with no error",
   "evidence": "probe on the sample, extract raises LLMFailed for every record except record 1: out['status'] done_with_errors, counts.entries 1, case status ready, error None. Pinned by tests/unit/test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records_keeps_its_old_shape (written for one record down).",
   "why_it_matters": "The orchestrator's rule is 'no entry at all'; the stubs are visible in the tray, so this is not a silent fallback. But a case where most records produced nothing reads the same as one record down, and the message that names the step appears only at zero.",
   "fix": "Decide whether a majority-down first run should read failed or carry a non-blocking note; if the current rule stays, say so in the test name and in api.md.",
   "acceptance_test": "A test for a mostly-down first run asserting the chosen status and message."},
  {"severity": "nit", "title": "The flag step's schema-invalid branch is not recorded in failed_steps",
   "evidence": "app/backend/flags.py:255-256 sets failed = True on a pydantic ValidationError without raising, so _noting never appends 'flags'. FakeCall returning {'flags': 'not a list'} on the plain note gives ('ready', None). In production the provider validates the JSON schema first (app/llm/provider.py:107 validate_schema), which raises and reaches _noting as LLMFailed, so I could not reach the branch outside a test double.",
   "why_it_matters": "If the pydantic model ever gets a rule the JSON schema does not carry, the r1 blocker returns through that door.",
   "fix": "Raise or record the step in failed_steps on that branch, or delete the branch and let validation failures propagate.",
   "acceptance_test": "Plain note, flags returns a schema-invalid object -> case failed, run_partial, 'finding the flags'."}
 ],
 "whats_right": ["the flag step is now read from the steps that were down, with a dedupe against rows that already carry the failure, so the sample's message names the step once and the plain note's names it without an item count", "the same _partial_error path serves first run and re-run, so message and RUN_FAILED gate cannot drift apart; 8 of 9 mutants die", "the three flipped pins each change one assertion to the decided behaviour and keep the surrounding stub and message assertions"],
 "questions_for_chris": ["An extract-down first run with some entries (even 1 of 9) reads ready with tray stubs. Is 'failed only at zero entries' the intended threshold?"]}
```
----
312efe6 fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
ea988f8 fix(backend): T-139 r5 the export gate scans Billed charges (a charge line carries its own amount; other money trimmed by code or blocks naming the line); number words after a money label are money
9db2cec fix(frontend): a side panel that throws is reported, not swallowed; the no-console-errors smoke asserts all 7 panels mount (T-162 r3)
95ffe36 docs(orchestrator): D-063 P0 + UX/UI only until the MVP is polished (Chris)
f31b146 fix(backend): T-157 r3 an unconfirmed edit is pinned as a next_action item (mutant dies), exact waiting-set and demo-gate tests, plain_title keeps words after a lone <, hitl.needs_review_open
312efe663327539df1b712832e23bf1d2c495d42
commit 312efe663327539df1b712832e23bf1d2c495d42
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 10:13:08 2026 -0600

    fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/generator.py                           |  19 +++
 app/backend/pipeline.py                            |  61 ++++++--
 app/backend/present.py                             |   2 +-
 app/backend/review.py                              |   2 +
 tests/unit/_hand_entry.py                          |  15 ++
 tests/unit/test_api_routes.py                      |   4 +-
 tests/unit/test_case_list.py                       |   2 +
 tests/unit/test_t114_rates_and_demo_judges.py      |   2 +
 tests/unit/test_t139_charge_text.py                |  13 +-
 .../test_t146_r3_decided_items_never_lowered.py    |   5 +-
 tests/unit/test_t161_first_run_stage_down.py       |  10 +-
 tests/unit/test_t165_partial_extract.py            | 158 +++++++++++++++++++++
 12 files changed, 272 insertions(+), 21 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:52.369Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -30 && git diff 312efe6^ 312efe6 -- app/backend/pipeline.py app/backend/generator.py app/backend/present.py app/backend/review.py",
 "description": "Show HEAD sha, working status, and the production diff of T-165"
}
````

### User / tool · 2026-11-02T16:13:52.561Z

**tool result**
````
312efe663327539df1b712832e23bf1d2c495d42
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
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/calibration_route.py
 M app/backend/export.py
 M app/backend/present.py
 M app/backend/review.py
 M app/backend/why.py
MM app/frontend/api.js
MM app/frontend/app.js
diff --git a/app/backend/generator.py b/app/backend/generator.py
index ec50009..12a9ae5 100644
--- a/app/backend/generator.py
+++ b/app/backend/generator.py
@@ -202,6 +202,25 @@ def resolved_placeholders(entries: list) -> set:
     return {e["id"] for e in entries if (e.get("ladder") or {}).get("failure") and e["state"] == "rejected" and live & set(e["record_ids"] or [])}
 
 
+def entered_by_hand(entries: list) -> set:
+    """T-165: record ids ("r6") that have a live entry the paralegal wrote by hand (manual entry, D-031: `ladder.entered_by == "reviewer"`, not rejected)."""
+    return {r for e in entries if e["state"] != "rejected" and (e.get("ladder") or {}).get("entered_by") == "reviewer" for r in (e["record_ids"] or [])}
+
+
+def hand_entered_warnings(entries: list) -> list:
+    """T-165: one named warning per could-not-verify placeholder whose record the paralegal has since entered by hand. The extract step failed for that record, but nothing is
+    missing from the timeline any more, so it is information for the case (not a run failure): `{code: ENTERED_BY_HAND, record_no, item_id (the placeholder), message}`."""
+    hand = entered_by_hand(entries)
+    out = []
+    for e in entries:
+        rids = e["record_ids"] or []
+        if e["state"] == "rejected" and (e.get("ladder") or {}).get("failure") and rids and rids[0] in hand:
+            n = int(rids[0][1:])
+            out.append({"code": "ENTERED_BY_HAND", "record_no": n, "item_id": e["id"],
+                        "message": f"The AI step could not write an entry for record {n}; you entered it by hand."})
+    return sorted(out, key=lambda w: w["record_no"])
+
+
 def extract_entries(records: list, groups: list, *, call, case_text: str = "", workers: int = CONCURRENCY):
     """Stages 1-2 over distinct records (only the first record of each duplicate group is sent). Returns
     (entries, rejected, failures). `entries` are chronological by (date, seq) and never contain a rejected item; `rejected` goes to the
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index e9b7bed..4b5eb5c 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -310,7 +310,7 @@ def _disagrees(kind: str, old: dict, it: dict) -> bool:
     return (old.get("type"), old.get("category"), _evidence_texts(old)) != (it.get("type"), it.get("category"), {e.get("text") for e in it.get("evidence", [])})
 
 
-def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True) -> tuple:
+def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True, empty_ids: list = None) -> tuple:
     """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
     computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed.
     `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or
@@ -319,7 +319,9 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
     or changes it (`_disagrees`), the stored row is kept as it is and `ladder.rerun_note` says so (shown on the item). A row that is not decided is kept the same way,
     without a note, when the new row is a failure over stored output (a stub, a flag made while the flag step failed, a lost second-check answer).
     Returns (kept, nothing_to_keep): `kept` is [(stored row, step, 'failed' | 'disagreed')]; `nothing_to_keep` is [(step)] for new rows that are failures with no stored
-    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale)."""
+    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale).
+    `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
+    reviewer) is not a stale row while its record has no live entry in `items`: a re-run in which the record's extract fails again must not sweep the paralegal's work."""
     table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
     existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
     kept, empty = [], []
@@ -345,6 +347,8 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
         fail = _failure(kind, it)
         if fail:
             empty.append(fail)
+            if empty_ids is not None:
+                empty_ids.append(it["id"])
         row = _row(kind, it)
         if old is None:
             DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
@@ -361,8 +365,11 @@ def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bo
     if additive:
         return kept, empty
     keep = {i["id"] for i in items}
+    live_rids = {r for i in items if kind == "entry" and i.get("state") != "rejected" for r in (i.get("record_ids") or [])}
     for oid, old in existing.items():
         if oid not in keep and old["review_status"] == "pending":
+            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer" and not live_rids & set(old["record_ids"] or []):
+                continue                                # T-165: the paralegal's own entry for a record the AI could not do
             if not prune:
                 kept.append((old, "finding the flags", "failed"))
                 continue
@@ -423,10 +430,11 @@ def _items(n: int) -> str:
     return f"{n} item{'s' if n != 1 else ''}"
 
 
-def _partial_error(kept: list, empty: list, down: tuple = ()):
+def _partial_error(kept: list, empty: list, down: tuple = (), records: list = ()):
     """T-146 r3: the case's honest message for a re-run that kept earlier work or had a step fail with nothing to fall back on (code `run_partial`), or None.
     It names how many items and which steps, and says exactly what was kept. `down` (T-161 r2): steps that failed without leaving any row to count (the flag step on
-    records with no phrase-list hit makes no flag at all), named without a count."""
+    records with no phrase-list hit makes no flag at all), named without a count. `records` (T-165): the record numbers whose extract step failed with nothing to keep; the message names
+    them and the error carries them (`records`, plus `extract_only` when that is the whole failure, so a hand entry can clear it)."""
     failed, differed = [k for k in kept if k[2] == "failed"], [k for k in kept if k[2] == "disagreed"]
     parts = []
     if failed:
@@ -440,7 +448,35 @@ def _partial_error(kept: list, empty: list, down: tuple = ()):
                      f"The AI step failed for {_items(len(empty))} ({' and '.join(sorted(set(empty)))}) on this run, and there is no earlier result to keep.")
     if down:
         parts.append(f"The AI step ({' and '.join(sorted(down))}) failed on this run, so nothing from it could be used.")
-    return {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
+    if records:
+        parts.append(f"No entry was made for record{'s' if len(records) != 1 else ''} {_nos(records)}.")
+    err = {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
+    if err and records:
+        err["records"] = list(records)
+        if not kept and not down and set(empty) == {_EXTRACT_STEP}:
+            err["extract_only"] = True
+    return err
+
+
+def _nos(ns: list) -> str:
+    ns = [str(n) for n in ns]
+    return ns[0] if len(ns) == 1 else ", ".join(ns[:-1]) + " and " + ns[-1]
+
+
+def refresh_extract_error(conn, cid: str) -> None:
+    """T-165: after the paralegal enters a record by hand, a case that failed ONLY because the extract step failed for named records stops counting the ones now entered:
+    it reads ready (no error, no RUN_FAILED) when none is left, and names the rest otherwise. A failure with any other cause (a second check, the flag step, a kept earlier result) is left as
+    it is; it needs a re-run."""
+    case = DB.get_case(conn, cid)
+    err = json.loads(case["error"]) if case.get("error") else None
+    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
+        return
+    hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))
+    left = [n for n in err["records"] if f"r{n}" not in hand]
+    if left == err["records"]:
+        return
+    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
+    DB.update_case(conn, cid, status="failed" if new else "ready", error=json.dumps(new) if new else None)
 
 
 def _noting(raw_call, failed_steps: list):
@@ -568,8 +604,12 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     from app.backend import pdf_checks as PC      # T-086: items on OCR-read pages are always needs_review, whatever the judges said
     PC.mark_ocr_items(dated + undated + final_amounts + flag_items, recs, ((DB.get_case(conn, cid).get("config") or {}).get("pages")), WHY.why("OCR_DERIVED"))
     now_t = clock()
-    rerun = bool(DB.list_items(conn, cid, "entry"))      # entries exist only after an earlier run: this is a re-run
-    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
+    by_hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))      # T-165: records the paralegal already entered by hand
+    empty_eids = []
+    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out, empty_ids=empty_eids)
+    stub_rid = {e["id"]: e["record_ids"][0] for e in tray if e.get("record_ids")}
+    no_entry = sorted(int(stub_rid[i][1:]) for s, i in zip(empty_e, empty_eids) if s == _EXTRACT_STEP and stub_rid.get(i) not in by_hand)      # extract failed, nothing earlier kept, not entered by hand
+    empty_e = [s for s, i in zip(empty_e, empty_eids) if not (s == _EXTRACT_STEP and stub_rid.get(i) in by_hand)]
     for a in final_amounts:                     # an amount stays linked to the entry whose record failed this time (that entry's stored row was kept)
         if not a.get("entry_id"):
             a["entry_id"] = next((o["id"] for o, _, _ in kept_e if f"r{a['record_nos'][0]}" in (o["record_ids"] or [])), None)
@@ -584,16 +624,17 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     else:
         status = "done_with_errors" if errors else "done"
         # T-161: a first run with a judge or the flag step down fails like a re-run. The flag step is read from the steps that were down (a note with no phrase-list hit has no flag row to carry the failure).
-        # A first run's extract failures stay tray items while some entries came out; with no entry at all there is nothing to review, so it is failed and the step is named.
+        # T-165: an extract failure fails the case on a first run too, however many other records came out, and the records are named; a record the paralegal entered by hand is not one of them.
         named = {c for _, c, _ in kept} | set(empty)
         down = ("finding the flags",) if "flags" in failed_steps and "finding the flags" not in named else ()
-        err = _partial_error(kept, empty if (rerun or not (dated or undated)) else [s for s in empty if s != _EXTRACT_STEP], down)
+        err = _partial_error(kept, empty, down, no_entry)
     DB.update_case(conn, cid, status="failed" if (timed_out or err) else "ready", stage="finalize", error=json.dumps(err) if err else None,
                    run_finished_at=now_t, injection_records_json=ing["injection_records"])
     tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
     all_items = dated + undated + final_amounts + flag_items
     return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
-            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
+            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot,
+            "warnings": ing["warnings"] + generator.hand_entered_warnings(DB.list_items(conn, cid, "entry")),
             "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
             "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                        "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
diff --git a/app/backend/present.py b/app/backend/present.py
index bbd0847..c0f6a2a 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -348,7 +348,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
             "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
-            "review": review_view(conn, case_id), "warnings": [], "error": err,
+            "review": review_view(conn, case_id), "warnings": generator.hand_entered_warnings(DB.list_items(conn, case_id, "entry")), "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
             **{k: (case.get("config") or {})[k] for k in ("pdf_checks",) if (case.get("config") or {}).get(k)},     # T-086/T-087 (PDF cases only)
             **({"pdf_pages": (case.get("config") or {})["pages"]} if (case.get("config") or {}).get("pages") else {})}
diff --git a/app/backend/review.py b/app/backend/review.py
index 80a65a0..7eed93b 100644
--- a/app/backend/review.py
+++ b/app/backend/review.py
@@ -674,6 +674,8 @@ def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, n
         "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
     DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
     enforce_ocr(conn, case_id, t)
+    from app.backend import pipeline as PL
+    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no longer fails
     from app.backend import present
     return {"item": present.item_view(conn, case_id, eid), "totals": present.totals_view(conn, case_id),
             "review": present.review_view(conn, case_id), "warnings": chk["warnings"]}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:53.088Z

**tool call — Bash**
````
{
 "command": "git diff 312efe6^ 312efe6 -- tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py tests/unit/test_api_routes.py tests/unit/_hand_entry.py tests/unit/test_case_list.py tests/unit/test_t114_rates_and_demo_judges.py tests/unit/test_t139_charge_text.py",
 "description": "Show T-165 test-file diffs including pinned tests"
}
````

### User / tool · 2026-11-02T16:13:53.189Z

**tool result**
````
diff --git a/tests/unit/_hand_entry.py b/tests/unit/_hand_entry.py
new file mode 100644
index 0000000..28924a9
--- /dev/null
+++ b/tests/unit/_hand_entry.py
@@ -0,0 +1,15 @@
+"""T-165 test helper. lib01's record 3 has no recorded extract answer at the current prompt (FIXTURE_MISS stub), so a fixture-backend run of that packet reads
+`failed` / `run_partial` naming record 3 (the extract step failed for a record). The paralegal's way out is the tray manual entry (D-031): enter each named record by
+hand (its first sentence, as summary and quote), which clears an extract-only failure (T-165). Tests that need a ready case call this after waiting."""
+
+
+def enter_failed_records_by_hand(c, tok):
+    """If the case failed only because the extract step failed for named records, enter each by hand and return the new status; otherwise return the status unchanged."""
+    case = c.get(f"/api/cases/{tok}").json()
+    err = case.get("error") or {}
+    if case["status"] != "failed" or not err.get("extract_only"):
+        return case["status"]
+    for n in err["records"]:
+        first = next(r for r in case["records"] if r["id"] == f"r{n}")["sentences"][0]["text"]
+        assert c.post(f"/api/cases/{tok}/records/r{n}/entry", json={"summary": first, "excerpt": first}).status_code == 201
+    return c.get(f"/api/cases/{tok}/status").json()["status"]
diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index b30a859..4d540d6 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -21,13 +21,13 @@ def env(tmp_path, monkeypatch):
     return db, TestClient(create_app(db, static_dir=str(tmp_path)), client=("127.0.0.1", 50000))   # real loopback peer: local mode checks it (D-036)
 
 
-def wait_ready(c, tok):
+def wait_ready(c, tok, allow_failed=False):
     for _ in range(160):
         s = c.get(f"/api/cases/{tok}/status").json()
         if s["status"] in ("ready", "failed"):
             break
         time.sleep(0.25)
-    assert s["status"] == "ready", s
+    assert s["status"] == "ready" or (allow_failed and s["status"] == "failed"), s
     return s
 
 
diff --git a/tests/unit/test_case_list.py b/tests/unit/test_case_list.py
index 7c194e0..3e7ee45 100644
--- a/tests/unit/test_case_list.py
+++ b/tests/unit/test_case_list.py
@@ -394,6 +394,8 @@ def _fresh(local, lib_id):
     tok = local.post("/api/cases", json={"library": lib_id}).json()["token"]
     assert local.post(f"/api/cases/{tok}/run", json={}).status_code == 202
     _wait(local, tok)
+    from tests.unit._hand_entry import enter_failed_records_by_hand
+    enter_failed_records_by_hand(local, tok)      # T-165: lib01's record 3 has no recorded extract answer; the paralegal enters it by hand
     return tok
 
 
diff --git a/tests/unit/test_t114_rates_and_demo_judges.py b/tests/unit/test_t114_rates_and_demo_judges.py
index dad9b20..4960cb3 100644
--- a/tests/unit/test_t114_rates_and_demo_judges.py
+++ b/tests/unit/test_t114_rates_and_demo_judges.py
@@ -32,6 +32,8 @@ def _load(c, lib_id):
         if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed", "done_with_errors"):
             break
         time.sleep(0.25)
+    from tests.unit._hand_entry import enter_failed_records_by_hand
+    enter_failed_records_by_hand(c, tok)      # T-165: lib01's record 3 has no recorded extract answer; the paralegal enters it by hand
     assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready", lib_id
     return tok
 
diff --git a/tests/unit/test_t139_charge_text.py b/tests/unit/test_t139_charge_text.py
index 62eb9d2..f15a773 100644
--- a/tests/unit/test_t139_charge_text.py
+++ b/tests/unit/test_t139_charge_text.py
@@ -11,7 +11,16 @@ from app.backend import charge_text as CT
 from app.backend import confidence, why
 from app.backend import export as X
 from app.backend.api import create_app
-from tests.unit.test_api_routes import wait_ready
+from tests.unit._hand_entry import enter_failed_records_by_hand
+from tests.unit.test_api_routes import wait_ready as _wait_ready
+
+
+def wait_ready(c, tok):
+    """Wait for the run; lib01's record 3 has no recorded extract answer (T-165: failed / run_partial), so the record is entered by hand."""
+    _wait_ready(c, tok, allow_failed=True)
+    enter_failed_records_by_hand(c, tok)
+    return _wait_ready(c, tok)
+
 
 LIB01 = "case_lib01_er_only_then_gap"
 
@@ -212,7 +221,7 @@ def test_lib01_letter_has_no_amount_outside_the_charges_section_and_no_per_visit
         letter = c.get(f"/api/cases/{tok}/export?style={style}").json()["letter_text"]
         assert _letter_money(letter) == [], letter
         assert "per visit" not in letter.lower() and "$140" not in letter
-    assert j["counts"]["entries"] == 3                      # e1, e5, e6; e2 and e4 are held out
+    assert j["counts"]["entries"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready); e2 and e4 are held out
     notes = j["internal_notes_text"]
     assert "states a dollar amount, not exported" in notes
 
diff --git a/tests/unit/test_t146_r3_decided_items_never_lowered.py b/tests/unit/test_t146_r3_decided_items_never_lowered.py
index ae5e6a4..0ef1f6b 100644
--- a/tests/unit/test_t146_r3_decided_items_never_lowered.py
+++ b/tests/unit/test_t146_r3_decided_items_never_lowered.py
@@ -216,7 +216,8 @@ def test_rerun_with_nothing_to_keep_still_says_the_step_failed(tmp_path):
     assert again["status"] == "done_with_errors"
     status, err = case_error(conn, cid)
     assert status == "failed"
-    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep." + TAIL}
+    assert err == {"code": "run_partial", "records": list(range(1, 10)), "extract_only": True,      # T-165: the records are named
+                   "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL}
 
 
 def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
@@ -231,7 +232,7 @@ def test_nothing_to_keep_and_something_kept_are_both_said(tmp_path):
     rerun(conn, cid, extract=extract)
     _, err = case_error(conn, cid)
     assert err["message"] == ("The AI step failed for 1 item (writing the entries) on this run. Their earlier results and every decision of yours were kept unchanged. "
-                              "The AI step also failed for 1 item (writing the entries) with no earlier result to keep." + TAIL)
+                              "The AI step also failed for 1 item (writing the entries) with no earlier result to keep. No entry was made for record 4." + TAIL)      # T-165: the record is named
 
 
 # ---- a later good run clears the notes and the error
diff --git a/tests/unit/test_t161_first_run_stage_down.py b/tests/unit/test_t161_first_run_stage_down.py
index e9ca938..dd0443a 100644
--- a/tests/unit/test_t161_first_run_stage_down.py
+++ b/tests/unit/test_t161_first_run_stage_down.py
@@ -1,7 +1,7 @@
 """T-161: a FIRST run with a stage down (flags, judge 1-4) reads like a re-run that fails: the case is failed / run_partial, the message names the step, and the export
 gate lists RUN_FAILED. A clean first run stays ready.
 r2: the flag step is read from the steps that were down (not from lexicon flag rows), so it fails the case on a note with no phrase-list hit too; a first run whose extract
-step gave NO entries at all is failed too (writing the entries named); a first run where only some records failed extraction keeps its old shape (tray items, case ready)."""
+step gave NO entries at all is failed too (writing the entries named); a first run where only some records failed extraction kept its old shape (tray items, case ready) until T-165, which fails it too and names the records."""
 import pytest
 from app.backend import pipeline as PL, trace
 from app.db import db as DB
@@ -113,11 +113,12 @@ def test_first_run_with_extract_down_and_no_entries_fails_and_names_the_step(tmp
     assert out["status"] == "done_with_errors" and out["counts"]["entries"] == 0
     status, err = case_error(conn, cid)
     assert status == "failed" and out["error"] == err
-    assert err == {"code": "run_partial", "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep." + TAIL}
+    assert err == {"code": "run_partial", "records": list(range(1, 10)), "extract_only": True,      # T-165: the records are named
+                   "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL}
     assert "RUN_FAILED" in blockers(conn, cid)
 
 
-def test_first_run_with_extract_down_for_some_records_keeps_its_old_shape(tmp_path):
+def test_first_run_with_extract_down_for_some_records_is_failed_too_t165(tmp_path):      # T-161 r2 kept this 'ready'; T-165 supersedes it (tests/unit/test_t165_partial_extract.py)
     good = sample_script()["extract"]
 
     def extract(user):
@@ -126,7 +127,8 @@ def test_first_run_with_extract_down_for_some_records_keeps_its_old_shape(tmp_pa
         return good(user)
     conn, cid, out = first_run(tmp_path, extract=extract)
     assert out["status"] == "done_with_errors" and out["counts"]["entries"] > 0
-    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
+    status, err = case_error(conn, cid)
+    assert status == "failed" and err["records"] == [1] and "RUN_FAILED" in blockers(conn, cid)
 
 
 def test_a_good_second_run_clears_a_failed_first_run(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:53.444Z

**tool call — Bash**
````
{
 "command": "cat tests/unit/test_t165_partial_extract.py",
 "description": "Read the new T-165 unit test file"
}
````

### User / tool · 2026-11-02T16:13:53.548Z

**tool result**
````
"""T-165: on a FIRST run, when the extract step failed on N >= 1 records the case is run_partial with those records named and the export gate lists RUN_FAILED
(one record down, 8 of 9 down, all ok, hand-entered). A record the paralegal has since entered by hand (D-053 tray manual entry, D-031) is no longer a failure: it becomes a
named warning, and a case whose only failures were hand-entered reads ready again. A run where every record extracted stays ready.
(Replaces the T-161 r2 rule 'failed only at zero entries'; the `not dated` mutant of T-161 r2 no longer exists, the boundary is pinned by the undated-entry test.)"""
import pytest
from app.backend import pipeline as PL, present, review as RV, trace
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
from tests.unit.test_t146_r3_decided_items_never_lowered import TAIL, case_error, down, model_flag

TAIL_ = " Run it again to retry."
J1_OK = FakeCall({"j1": {"verdict": "supported", "reason_code": "NONE"}})


def extract_down(*nos):
    good = sample_script()["extract"]

    def extract(user):
        if which_record(user)[0] in nos:
            raise down("extract")
        return good(user)
    return extract


def run(tmp_path, *nos, again=None, now=1.0):
    """First run on a new case, or (again=(conn, cid)) a re-run of that case."""
    conn, cid = again or (DB.connect(str(tmp_path / "d.sqlite")), None)
    cid = cid or DB.create_case(conn, G.raw("sample"), now=0.0)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(*nos), flags=model_flag)), now=lambda: now)
    return conn, cid, out


def blockers(conn, cid):
    return [b["reason_code"] for b in trace.export_blockers(conn, cid)]


def hand_entry(conn, cid, n):
    rec = G.records("sample")[n - 1]
    return RV.manual_entry(conn, cid, f"r{n}", {"summary": rec["excerpt"], "excerpt": rec["excerpt"]}, call=J1_OK)


def test_all_records_extracted_stays_ready(tmp_path):
    conn, cid, out = run(tmp_path)
    assert out["error"] is None and case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["warnings"] == []


def test_one_record_down_on_a_first_run_is_run_partial_naming_the_record(tmp_path):
    conn, cid, out = run(tmp_path, 1)
    assert out["counts"]["entries"] == 8                                     # the other eight came out; the failed one is a tray placeholder
    status, err = case_error(conn, cid)
    assert status == "failed" and out["error"] == err
    assert err == {"code": "run_partial", "records": [1], "extract_only": True,
                   "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1." + TAIL_}
    assert "RUN_FAILED" in blockers(conn, cid)
    view = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert [t["record_ids"] for t in view["tray"]] == [["r1"]] and view["error"] == err


def test_eight_of_nine_down_is_run_partial_naming_all_eight(tmp_path):
    conn, cid, out = run(tmp_path, *range(2, 10))
    assert out["counts"]["entries"] == 1
    status, err = case_error(conn, cid)
    assert status == "failed" and err["code"] == "run_partial" and err["records"] == list(range(2, 10))
    assert err["message"] == ("The AI step failed for 8 items (writing the entries) on this run, and there is no earlier result to keep. "
                              "No entry was made for records 2, 3, 4, 5, 6, 7, 8 and 9." + TAIL_)
    assert "RUN_FAILED" in blockers(conn, cid)


def test_all_nine_down_names_all_nine(tmp_path):
    conn, cid, out = run(tmp_path, *range(1, 10))
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == list(range(1, 10)) and "records 1, 2, 3, 4, 5, 6, 7, 8 and 9." in err["message"]


NOTE = ('=== Record 1 ===\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen for follow up of neck stiffness. Range of motion improved."\n\n'
        '=== Record 2 ===\nDate: 2026-05-10\nSource: Brindlewood Physical Therapy, visit note\n'
        'Excerpt: "Patient seen. Physical therapy continued 2x per week."\n')      # SYNTHETIC; record 1 has no date


def test_an_undated_entry_is_still_an_entry_the_failed_record_is_named(tmp_path):
    """The boundary the T-161 r2 reviewer's `not dated` mutant probed: the only entry that came out is undated, every other record failed."""
    conn = DB.connect(str(tmp_path / "n.sqlite"))
    cid = DB.create_case(conn, NOTE, now=0.0)

    def extract(u):
        if "Physical therapy continued" in u:
            raise down("extract")
        return dict(summary="Range of motion improved.", excerpt="Range of motion improved.")
    out = PL.run_pipeline(conn, cid, NOTE, call=FakeCall(sample_script(extract=extract)), now=lambda: 1.0)
    assert out["entries"] == [] and len(out["undated_entries"]) == 1          # the one entry is undated
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == [2] and "No entry was made for record 2." in err["message"] and "RUN_FAILED" in blockers(conn, cid)


# ---------------------------------------------------------------------------------------- hand-entered (D-053 tray manual entry)
def hand_warnings(conn, cid):
    return present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["warnings"]


def test_a_record_entered_by_hand_before_the_run_is_a_named_warning_not_a_failure(tmp_path):
    conn = DB.connect(str(tmp_path / "h.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.ingest_case(conn, cid, G.raw("sample"))
    hand_entry(conn, cid, 1)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(1), flags=model_flag)), now=lambda: 1.0)
    assert out["error"] is None and case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert [e["id"] for e in DB.list_items(conn, cid, "entry") if e["id"] == "e1_m"] == ["e1_m"]      # the hand-entered row survived the run
    w = [x for x in out["warnings"] if x["code"] == "ENTERED_BY_HAND"]
    assert [(x["record_no"], x["item_id"]) for x in w] == [(1, "e1")] and "record 1" in w[0]["message"] and "by hand" in w[0]["message"]
    assert [x["record_no"] for x in hand_warnings(conn, cid) if x["code"] == "ENTERED_BY_HAND"] == [1]


def test_entering_the_failed_record_by_hand_after_the_run_clears_the_failure_into_a_warning(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    assert case_error(conn, cid)[0] == "failed"
    hand_entry(conn, cid, 1)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]
    assert present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["tray"] == []      # T-110 r2: it left the tray


def test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named(tmp_path):
    conn, cid, _ = run(tmp_path, 1, 2)
    hand_entry(conn, cid, 1)
    status, err = case_error(conn, cid)
    assert status == "failed" and err["records"] == [2]
    assert err["message"] == "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 2." + TAIL_
    assert "RUN_FAILED" in blockers(conn, cid)
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]


def test_a_failure_with_another_cause_is_not_cleared_by_a_hand_entry(tmp_path):
    conn = DB.connect(str(tmp_path / "o.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(extract=extract_down(1), j2=down("j2"), flags=model_flag)), now=lambda: 1.0)
    status, err = case_error(conn, cid)
    assert status == "failed" and "extract_only" not in err
    hand_entry(conn, cid, 1)
    assert case_error(conn, cid)[0] == "failed" and "RUN_FAILED" in blockers(conn, cid)


def test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    hand_entry(conn, cid, 1)
    run(tmp_path, 1, again=(conn, cid), now=2.0)
    assert case_error(conn, cid) == ("ready", None)
    assert "e1_m" in {e["id"] for e in DB.list_items(conn, cid, "entry")}      # the pending hand-entered row is not swept as a stale row
    assert [x["record_no"] for x in hand_warnings(conn, cid)] == [1]


def test_a_rerun_that_extracts_the_record_clears_the_failure(tmp_path):
    conn, cid, _ = run(tmp_path, 1)
    assert case_error(conn, cid)[0] == "failed"
    run(tmp_path, again=(conn, cid), now=2.0)
    assert case_error(conn, cid) == ("ready", None) and "RUN_FAILED" not in blockers(conn, cid)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:13:57.685Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo $S && ls -la \"$S\" | head -5; git status --short | grep '^??' | head -50; echo; git status --short | grep '^??' | wc -l",
 "description": "Check scratchpad and list untracked files"
}
````

### User / tool · 2026-11-02T16:13:57.923Z

**tool result**
````
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad
total 376912
drwx------@ 1601 arsis  wheel    51232 Nov  2 10:13 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
?? .claude/agent-memory/accessibility-reviewer/
?? .claude/agent-memory/architect/
?? .claude/agent-memory/backend/project_t113_conflict_rules.md
?? .claude/agent-memory/backend/project_t139_r4_money_module.md
?? .claude/agent-memory/backend/project_t140_d060_default_deny.md
?? .claude/agent-memory/backend/project_t141_accident_date_checks.md
?? .claude/agent-memory/backend/project_t146_rerun_decided_rule.md
?? .claude/agent-memory/claims-adjuster-reviewer/feedback_persona_identity_on_filing.md
?? .claude/agent-memory/claims-adjuster-reviewer/feedback_reviewer_write_and_parse_guards.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_d040_label_cut_residue.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_gate_m2_curated_vs_recorded.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t061_r4_separator_list.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t067_credibility_negation_and_recall.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t071_chip_cut_harness_sweep.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t092_allow_list_reading.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t111_positive_count_recall.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t139_charge_text_r0.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t140_ledger_label_leaks.md
?? .claude/agent-memory/claims-adjuster-reviewer/project_t154_charge_confirm_ui.md
?? .claude/agent-memory/claims-adjuster-reviewer/reference_spare_port_app_server.md
?? .claude/agent-memory/frontend/feedback_verify_from_archive.md
?? .claude/agent-memory/frontend/project_t060_polish.md
?? .claude/agent-memory/legal-nurse-reviewer/feedback_spanish_routing_and_cues.md
?? .claude/agent-memory/legal-nurse-reviewer/project_gate_m2_0c24f5f.md
?? .claude/agent-memory/legal-nurse-reviewer/project_t085_r4_d050_pass.md
?? .claude/agent-memory/legal-nurse-reviewer/project_t143_uncovered_list.md
?? .claude/agent-memory/legal-nurse-reviewer/project_t144_uncovered_ui.md
?? .claude/agent-memory/legal-nurse-reviewer/project_t151_t142_r2.md
?? .claude/agent-memory/paralegal-reviewer/d041-date-gate-patterns.md
?? .claude/agent-memory/paralegal-reviewer/record-format-review-patterns.md
?? .claude/agent-memory/paralegal-reviewer/reviewer-api-shape-gotchas.md
?? .claude/agent-memory/paralegal-reviewer/reviewer-run-pitfalls-pass4.md
?? .claude/agent-memory/paralegal-reviewer/t060-pass4-state-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t060-pass5-state-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t060-ui-polish-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t068-dates-to-confirm-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t079-library-v2-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t114-r3-gap-change-persistence.md
?? .claude/agent-memory/paralegal-reviewer/t114-rates-gap-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t116-gap-endpoint-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t118-lib11-truth-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t120-123-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t120-r2-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t120-r3-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t120-r4-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t136-r2-t142-patterns.md
?? .claude/agent-memory/paralegal-reviewer/t149-r2-overview-patterns.md
?? .claude/agent-memory/qa/project_calibration_route.md
?? .claude/agent-memory/researcher/
?? .claude/agent-memory/staff-engineer-reviewer/feedback_differential_probe_prior_build.md

    2346
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:01.293Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && mkdir -p \"$S/head\" && git archive 312efe6 | tar -x -C \"$S/head\" && echo \"archived to $S/head\" && cd \"$S/head\" && git -C /Users/arsis/zlayt-pm-project ls-tree -r --name-only 312efe6 | wc -l && ls \"$S/head\" && ls \"$S/head/tests/fixtures\" 2>/dev/null | head; cd /Users/arsis/zlayt-pm-project && git ls-files tests/fixtures/llm | wc -l; ls tests/fixtures/llm | wc -l; git status --short tests/fixtures | head -5",
 "description": "Archive HEAD commit 312efe6 into scratchpad and compare fixtures"
}
````

### User / tool · 2026-11-02T16:14:02.049Z

**tool result**
````
archived to /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head
    2249
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
llm
make_curated.py
t140_restating_labels.txt
t140_synthetic_ledger_r1.txt
t140_synthetic_ledger_r2.txt
t140_synthetic_ledger_r3.txt
    1213
    1209
?? tests/fixtures/llm/0cc7a873e16a2f0572848c8c047cc0aeb4d32e2b42dfc81274ea28ca63fa3b84.json
?? tests/fixtures/llm/11a811729af462550cae9432916cf92b314ef5912bdbf4fa459763a20caf03b7.json
?? tests/fixtures/llm/2044a87296034da2ca563dedde30cd3b1a42f41df16d53bcbdba36770368e9b7.json
?? tests/fixtures/llm/23a42e78f6f5e66dfaeda880459bbbbf14d34b4945c40aca56c2d0bd19babf84.json
?? tests/fixtures/llm/249e2de6179c20db35f047d07665f84dcea759a937141dbc2f80ca48a96692f4.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:07.487Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && ls \"$S/head/tests/fixtures/llm\" | wc -l && git ls-files tests/fixtures/llm | sed 's#.*/##' | sort > \"$S/tracked.txt\" && (cd \"$S/head/tests/fixtures/llm\" && ls | sort) > \"$S/archived.txt\" && diff \"$S/tracked.txt\" \"$S/archived.txt\" | head -5; ls -la .venv/bin/python 2>/dev/null; cat \"$S/head/requirements-dev.txt\" 2>/dev/null | head; ls /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python --version",
 "description": "Compare archived fixture list with tracked list and check venv"
}
````

### User / tool · 2026-11-02T16:14:07.638Z

**tool result**
````
    1171
49d48
< 0d2d2b592ec2c8e1621a00e5751cf3746830d597c634169e67687cd2469f11f4.json
59d57
< 0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
115d112
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
-r requirements.txt
# test and browser-check tools (not shipped in the image)
greenlet==3.5.6
iniconfig==2.3.1
playwright==1.64.1
pluggy==1.7.0
pyee==14.0.0
Pygments==2.21.0
pytest==9.2.0
/Users/arsis/zlayt-pm-project/.venv/bin/python
Python 3.12.2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:11.914Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && git ls-tree -r --name-only 312efe6 tests/fixtures/llm | wc -l && git ls-tree -r --name-only 312efe6 tests/fixtures/llm | sed 's#.*/##' | sort > \"$S/head_tracked.txt\" && diff \"$S/head_tracked.txt\" \"$S/archived.txt\" && echo SAME_AS_HEAD && ls tests/fixtures/llm | wc -l && git status --short tests/fixtures/llm | grep -c '^??'",
 "description": "Confirm archived fixtures match HEAD tree listing"
}
````

### User / tool · 2026-11-02T16:14:12.049Z

**tool result**
````
    1213
49d48
< 0d2d2b592ec2c8e1621a00e5751cf3746830d597c634169e67687cd2469f11f4.json
59d57
< 0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
115d112
< 1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
145d141
< 20d9f32e425d426df6e3468c363ce8cfc31f0834cf3eb4488200b3100738a0fe.json
154d149
< 228350fb06e4cf872348f390212b959eebee7313b76f0edf051977846aacbc56.json
215d209
< 312262d8eda74074e8d727b89bf84bf0a2f67b5d4569f7ad269462e2c885c9ba.json
226d219
< 33ce48091065bc630e441778ba5e3a347ce433e3475b6f2dd73438c65640783a.json
245d237
< 37318d752543b06d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json
275d266
< 3cd867fd11c3c1e0119249144fd160a3d2ccc9ae4262b93f5ee10714fd46f61b.json
285d275
< 3e70853a6fadff0e4991350de156ea38d30b396597dbab5bc74601b2508eb6d7.json
316d305
< 45fc31f49cdb482624af416c87b5ac48d359cce6b490b1ed97b3e151e8c8eb97.json
327d315
< 4770363f6bf66fd6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json
346d333
< 4a4f531c922d869d060a0bf7b1d33b777c496b90570dd511f38559feded30334.json
375d361
< 4ed3d9961f3523183444f9fe85f8d460762306ec1bc8d89ddca81e621c7a6198.json
416d401
< 56923188ab8a48f2a34d2f41218286bd2af9ffe3eef013de2aa9260e075659db.json
433d417
< 5ab9b495155ea7ea9bda41e4818c38ca1973870ecf42ea3348fd84ef3a279e1c.json
483d466
< 6472dca543e0a4d4835b86da3e5361255353d60a3909f79d3c40f99518993c51.json
493d475
< 677a0dcb1f0a3d199926401c3ad5ced64d31d37f96083b78acd16d93118e4a36.json
500d481
< 689d2a7fb759bfa428927e7df073f0892bfb17d9ed829da3a51da4acf8c267ca.json
608d588
< 7f9e06e6e15e75756fa39c3aca5bb45dcaa75e29d727b0d9b3a4da164dc54519.json
621d600
< 82df7e9af4e06f5688fe0db20eb4957c3f0a5e34815683f0029afce35a03a327.json
633d611
< 85a544a335859c486aaa581be110146353bbe09d65a0b3946d121a72f463ad81.json
682d659
< 9283f0b1ae9e6fbf879dc23b62a24e9655eed20767a9a3b9b939beb3c1d70e25.json
710d686
< 98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
717d692
< 9a6221e090158ce21bd3d9d358347c184a75b2611f39cf890d99ab6f658ebc73.json
721d695
< 9a7a4f2b74a545cf1d324702af6348faf4db8afae938c8dc2506c6be30cbb407.json
761d734
< a1f0777e7722b161b62e8d670366303c827a2daff336fa324944e50a38f01c85.json
768d740
< a3f0e26ea728d289fec7de9c1a0de532e5a7b68efdbb86a20f8dd418c7d461d8.json
770d741
< a43109058a77805f8760288cea391804ef2174d3f22fed172532c87ea573bb25.json
797d767
< aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d368d6a5bbc1c8c3d3bb3.json
813d782
< acb899e670e980f5f109f70272c816ed4c88c3c10ae33572ee5557dd7b3b6c4b.json
829d797
< b0511a4e8269eaffd9832fbd4d21b731b8a552b0d09aa0ba6294f427fbc83eca.json
865d832
< b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3310718364dbfd51aee.json
889d855
< bbbf529af0ef0dfcb51ca2e09448f6f46c07c96645bde35bc2294914f8b7632f.json
904d869
< bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json
909d873
< be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d0117aabc60fc6202636ee.json
918d881
< c04cf7f6b365c7332b87b85e629ce7c8d0aee5783852e04f9811476040cb5791.json
948d910
< c7b86cc41ee9b7d77451f9e1ef024cffcd050a4a80f6eca3ab7f30b05e8b6c97.json
988a951
> curated
998d960
< d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
1097d1058
< e7ed16d363ed2bfc9082eff9545c29396c6639f24cf28336480f09bad13ef6d8.json
1102d1062
< e875141c2a384d6994a68973d69014da526f8a82b9742e4c7591a1e488f17f96.json
1111d1070
< e96d7b5567ab88d474f50f8babe5143929de9fd53340e2c708e97bed1c8e7899.json
1119d1077
< eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json
1132d1089
< edc5b1df0e4a2b7b36a0f0ca79fe17623863030eb0d78cdc3898a9c0aaae18ef.json
1184d1140
< f918b3c1933215f471a8b8f6e67761e01448f3baae041142723af29044397a58.json
1213a1170,1171
> narrative
> split
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:16.295Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && git ls-tree -r --name-only 312efe6 | sort > \"$S/head_all.txt\" && (cd \"$S/head\" && find . -type f | sed 's#^\\./##' | sort) > \"$S/archive_all.txt\" && diff \"$S/head_all.txt\" \"$S/archive_all.txt\" && echo ARCHIVE_MATCHES_HEAD_TREE; git ls-tree -r --name-only 312efe6 | grep -c 'tests/fixtures/llm'; find \"$S/head/tests/fixtures/llm\" -type f | wc -l",
 "description": "Verify archive file set matches HEAD tree exactly"
}
````

### User / tool · 2026-11-02T16:14:16.458Z

**tool result**
````
ARCHIVE_MATCHES_HEAD_TREE
1213
    1213
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:22.088Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider > ../unit_head.txt 2>&1; echo \"EXIT=$?\" >> ../unit_head.txt",
 "description": "Run full unit suite on HEAD archive copy",
 "run_in_background": true
}
````

### User / tool · 2026-11-02T16:14:22.164Z

**tool result**
````
Command running in background with ID: b631a9j1y. Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/b631a9j1y.output. You will be notified when it completes — do not poll that file or sleep while waiting. Read the file only if the user asks for progress, or if you need a line it prints before you can go on, such as a server's ready line or port.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:50.488Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"_EXTRACT_STEP\\|def _failure\\|empty_ids\\|def _persist\\|def run_pipeline\\|entered_by\" app/backend/pipeline.py | head -60; echo ---; sed -n 322,380p app/backend/pipeline.py",
 "description": "Locate extract-step and persist code in HEAD archive"
}
````

### User / tool · 2026-11-02T16:14:50.592Z

**tool result**
````
244:_EXTRACT_STEP = "writing the entries"
247:def _failure(kind: str, it: dict):
251:        return _EXTRACT_STEP
262:    if cause == _EXTRACT_STEP:
313:def _persist(conn, cid: str, kind: str, items: list, now: float, *, additive: bool = False, prune: bool = True, empty_ids: list = None) -> tuple:
323:    `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
350:            if empty_ids is not None:
351:                empty_ids.append(it["id"])
371:            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer" and not live_rids & set(old["record_ids"] or []):
456:        if not kept and not down and set(empty) == {_EXTRACT_STEP}:
474:    hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))
478:    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
494:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
607:    by_hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))      # T-165: records the paralegal already entered by hand
609:    kept_e, empty_e = _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out, empty_ids=empty_eids)
611:    no_entry = sorted(int(stub_rid[i][1:]) for s, i in zip(empty_e, empty_eids) if s == _EXTRACT_STEP and stub_rid.get(i) not in by_hand)      # extract failed, nothing earlier kept, not entered by hand
612:    empty_e = [s for s, i in zip(empty_e, empty_eids) if not (s == _EXTRACT_STEP and stub_rid.get(i) in by_hand)]
---
    output to fall back on. `prune=False`: the stale-pending delete is skipped (a failed flag step cannot tell which flags are stale).
    `empty_ids` (T-165): when given, the id of each `nothing_to_keep` row is appended in step (the caller names the records). A hand-entered pending entry (`ladder.entered_by`
    reviewer) is not a stale row while its record has no live entry in `items`: a re-run in which the record's extract fails again must not sweep the paralegal's work."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    kept, empty = [], []
    for it in items:
        old = existing.get(it["id"])
        if additive and old is not None:
            continue
        if old is not None and kind == "amount":        # T-084: a rerun keeps the class the paralegal gave a figure
            from app.backend import reclassify as RC
            it = RC.carry_over(old, it)
        decided = old is not None and old["review_status"] != "pending"
        cause = _degrades(kind, old, it) if old is not None else None
        how = "failed" if cause else None
        if decided and not cause and _disagrees(kind, old, it):
            cause, how = "a different result", "disagreed"
        if cause:
            kept.append((old, cause, how))
            if decided:
                msg = (f"The re-run could not redo this item ({cause}). Your decision and the earlier result were kept." if how == "failed" else
                       "The re-run gave a different result for this item (its summary, quote or checks no longer match what you decided on). Your decision and the earlier result were kept; the new result was not applied.")
                DB.update_item(conn, it["id"], now=now, case=cid, ladder={**(old.get("ladder") or {}), "rerun_note": {"kind": how, "step": cause, "message": msg, "at": now}})
            continue
        fail = _failure(kind, it)
        if fail:
            empty.append(fail)
            if empty_ids is not None:
                empty_ids.append(it["id"])
        row = _row(kind, it)
        if old is None:
            DB.add_item(conn, cid, kind, {"id": it["id"], **row}, now=now)
            continue
        DB.update_item(conn, it["id"], now=now, case=cid, **row)
        if kind == "flag" and old["review_status"] != "pending":
            oc = old.get("computed") or {}
            if any(oc.get(k) != it.get(k) for k in ("from_date", "to_date", "days")):
                DB.apply_review(conn, it["id"], "reset", now=now, case=cid)
            else:
                it["review_status"] = old["review_status"]
        elif old["review_status"] != "pending":
            it["review_status"] = old["review_status"]
    if additive:
        return kept, empty
    keep = {i["id"] for i in items}
    live_rids = {r for i in items if kind == "entry" and i.get("state") != "rejected" for r in (i.get("record_ids") or [])}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            if kind == "entry" and (old.get("ladder") or {}).get("entered_by") == "reviewer" and not live_rids & set(old["record_ids"] or []):
                continue                                # T-165: the paralegal's own entry for a record the AI could not do
            if not prune:
                kept.append((old, "finding the flags", "failed"))
                continue
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
    return kept, empty


def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:14:54.392Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"def manual_entry\" -A 40 app/backend/review.py | head -70; echo ----; grep -n \"def apply_review\" -A 25 app/db/db.py | head -45",
 "description": "Read manual_entry and apply_review status transitions"
}
````

### User / tool · 2026-11-02T16:14:54.534Z

**tool result**
````
635:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
636-    """The paralegal writes an entry for a record the AI could not make one for (rejected or failed). The quote must be whole verbatim
637-    sentences of that record (same rule as an excerpt edit, 422 invalid_edit otherwise); the summary goes through the same token check and
638-    judge 1 as an edit. The entry is stored as `pending` and labelled entered by the reviewer; nothing accepts it for them."""
639-    t = _now(now)
640-    case = DB.get_case(conn, case_id)
641-    recs = store.load_records(conn, case_id, case["raw_text"])
642-    rec = next((r for r in recs if r["id"] == record_id), None)
643-    if rec is None:
644-        raise ReviewError(404, "not_found", message="No such record.")
645-    if rec.get("duplicate_of"):
646-        raise _bad("This record is merged into another; enter the entry on the record it duplicates.")
647-    live = [e for e in DB.list_items(conn, case_id, "entry") if record_id in (e["record_ids"] or []) and e["state"] != "rejected"]
648-    if live:
649-        raise _bad("This record already has an entry; edit that entry instead.")
650-    summary, excerpt = (body or {}).get("summary"), (body or {}).get("excerpt")
651-    if not all(isinstance(v, str) and v.strip() for v in (summary, excerpt)):
652-        raise _bad("Provide a summary and the quoted sentences.")
653-    summary, excerpt = summary.strip(), excerpt.strip()
654-    problems = spanish.module_for(language.record_lang(rec)).check_excerpt(rec["excerpt"], excerpt)
655-    if problems:
656-        raise _bad("The quote must be whole sentences of this record, in order, with any hedge sentence that qualifies them.", reasons=problems)
657-    span = grounding.locate(rec["excerpt"], excerpt)
658-    eid = f"e{rec['seq']}_m"
659-    chk = _check_summary(eid, summary, excerpt, rec["source"] or "", rec.get("date_iso") or "", span, rec, call,
660-                         ocr_derived=record_id in ocr_record_ids(conn, case_id), bill_state=lambda: bill_state_for(conn, case_id, [record_id]))
661-    base = generator.body_offset(rec)
662-    ladder = {"item_id": eid, "generator": None, "entered_by": "reviewer",
663-              "judge": {"model": judges.judge_model(), "prompt_version": spanish.judge_prompt_version(language.record_lang(rec)), "call_id": chk["call_id"], "verdict": chk["ladder_verdict"],
664-                        "reason_code": chk["judge_code"], **({"error_class": chk["judge_error"]} if chk["judge_error"] else {})},
665-              "code_checks": {"excerpt_verbatim": True, "excerpt_whole_sentence": True, "summary_tokens_not_in_excerpt": chk["toks"],
666-                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
667-                              "date_provider_from_header": True},
668-              "human": {"action": None, "edited_text": None, "at": None}, "state": chk["state"]}
669-    if language.is_translated(language.record_lang(rec)):      # the reviewer wrote this English summary of a Spanish (or unidentified-language) quote: labelled as the reviewer's translation (D-042)
670-        ladder["translation"] = {**spanish.translation_info(language.record_lang(rec), True), "human_written": True}
671-    DB.add_item(conn, case_id, "entry", {
672-        "id": eid, "record_ids_json": [record_id], "seq": rec["seq"], "date_iso": rec.get("date_iso"), "provider": rec["source"],
673-        "summary": summary, "excerpt": excerpt, "excerpt_start": base + span[0] if span else None, "excerpt_end": base + span[1] if span else None,
674-        "state": chk["state"], "state_reasons_json": chk["reasons"], "ladder_json": ladder}, now=t)
675-    DB.apply_review(conn, eid, "manual_entry", now=t, case=case_id)
----
215:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
216-    """THE writer of review_status. Logs before/after to review_events in one transaction. Originals stay in the
217-    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
218-    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
220-    table, row = _find(conn, item_id, case)
221-    before = {"review_status": row["review_status"], "edited": json.loads(row["edited_json"]) if row["edited_json"] else None}
222-    status = ACTIONS[action] or row["review_status"]
223-    new_edited = (edited or before["edited"]) if action == "edit" else (None if action == "reset" else before["edited"])
224-    if action == "edit" and not new_edited:
225-        raise ValueError("edit requires a non-empty edited payload")
226-    after = {"review_status": status, "edited": new_edited}
227-    conn.execute("BEGIN")
228-    try:
229-        conn.execute(f"UPDATE {table} SET review_status=?, edited_json=?, updated_at=? WHERE id=? AND case_id=?",
230-                     (status, _enc(new_edited), now, item_id, row["case_id"]))
231-        conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
232-                     (_tok("v"), row["case_id"], item_id, action, _enc(before), _enc(after), now))
233-        conn.execute("COMMIT")
234-    except Exception:
235-        conn.execute("ROLLBACK")
236-        raise
237-    return get_item(conn, item_id, row["case_id"])
238-
239-
240-def log_event(conn, case_id: str, item_id: str, action: str, before=None, after=None, now: float = 0) -> str:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:15:05.432Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && sed -n 1,80p tests/unit/_fakes.py; echo ----; grep -n \"def case_error\\|def down\\|def model_flag\\|def rerun\\|^TAIL\\|def first_run\" -A 6 tests/unit/test_t146_r3_decided_items_never_lowered.py tests/unit/test_t161_first_run_stage_down.py | head -80; echo ---; grep -n \"ACTIONS\" -A 12 app/db/db.py | head -30",
 "description": "Read test fakes and helper functions used by T-165 tests"
}
````

### User / tool · 2026-11-02T16:15:05.550Z

**tool result**
````
"""Scripted fake LLM `call` for pipeline/judge/flag tests. No key, no network (fixture-style, in memory)."""
import itertools, json, re
from tests.unit import _golden as G

_RUNS = itertools.count()

class FakeCall:
    """call(step, system, user, schema, *, item_id=None) -> (output, call_id). Records every prompt."""
    def __init__(self, script=None):
        self.script = script or {}
        self.log = []
    def __call__(self, step, system, user, schema, *, item_id=None):
        self.log.append(dict(step=step, system=system, user=user, item_id=item_id))
        out = self.script[step](user) if callable(self.script.get(step)) else self.script.get(step, {})
        if isinstance(out, Exception):
            raise out
        return out, f"call{len(self.log)}"
    def steps(self):
        return [l["step"] for l in self.log]
    def prompts(self, step):
        return [l["user"] for l in self.log if l["step"] == step]

def golden_summaries():
    """{record_no: (summary, quote)} from the golden letter block."""
    letter, _ = G.export_blocks()
    ex = G.expected("sample"); recs = {r["record_no"]: r for r in ex["records"]}
    from datetime import datetime
    out = {}
    for blk in letter.split("BILLED CHARGES")[0].strip().split("\n\n")[1:]:
        h, summ, src = blk.split("\n")
        m = re.match(r"([A-Z][a-z]+ \d+, \d{4}) — (.+)$", h)
        iso = datetime.strptime(m.group(1), "%B %d, %Y").strftime("%Y-%m-%d")
        n = [k for k, r in recs.items() if r["source"] == m.group(2) and r["date"] == iso][0]
        out[n] = (summ, re.search(r'"(.+)"', src).group(1))
    return out

def which_record(user, case="sample"):
    """Record numbers whose excerpt appears in the prompt text."""
    return [r["n"] for r in G.records(case) if r["excerpt"] in user or r["excerpt"][:40] in user]


def sample_script(**over):
    """Happy-path script for the sample case (extract returns the golden summary and quote; judges agree; no LLM flags). `over` replaces steps."""
    sums = golden_summaries()
    def extract(user):
        n = which_record(user)[0]
        return dict(summary=sums[n][0], excerpt=sums[n][1])
    sc = {"extract": extract, "j1": {"verdict": "supported", "reason_code": "NONE"}, "j2": {"verdict": "agree", "reason_code": "NONE"},
          "j3": {"verdict": "conflict", "reason_code": "NONE"}, "j4": {"verdict": "agree", "reason_code": "NONE"},
          "conflicts": {"flags": []}, "flags": {"flags": []}}
    sc.update(over)
    return sc

def run_sample(tmp_path, case="sample", call=None, now=lambda: 1.0, **kw):
    """Run the whole pipeline on a golden case with a FakeCall; returns (output, call). Pipeline output keys used by tests:
    entries, amounts, flags, tray (rejected attempts), errors [{code, ...}], status, warnings."""
    from app.backend import pipeline as PL
    from app.db import db as DB
    conn = DB.connect(str(tmp_path / f"{case}-{next(_RUNS)}.sqlite"))
    cid = DB.create_case(conn, G.raw(case), now=1.0)
    call = call or FakeCall(sample_script())
    return PL.run_pipeline(conn, cid, G.raw(case), call=call, now=now, **kw), call

def items_for(out, n):
    """Every entry-like item (timeline, undated, tray) that cites record number n."""
    rid = f"r{n}"
    pool = list(out.get("entries", [])) + list(out.get("undated_entries", [])) + list(out.get("tray", []))
    return [i for i in pool if rid in i.get("record_ids", [])]
----
tests/unit/test_t161_first_run_stage_down.py:15:def first_run(tmp_path, **script):
tests/unit/test_t161_first_run_stage_down.py-16-    conn = DB.connect(str(tmp_path / "d.sqlite"))
tests/unit/test_t161_first_run_stage_down.py-17-    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
tests/unit/test_t161_first_run_stage_down.py-18-    script.setdefault("flags", model_flag)
tests/unit/test_t161_first_run_stage_down.py-19-    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 1.0)
tests/unit/test_t161_first_run_stage_down.py-20-    return conn, cid, out
tests/unit/test_t161_first_run_stage_down.py-21-
tests/unit/test_t146_r3_decided_items_never_lowered.py:14:TAIL = " Run it again to retry."
tests/unit/test_t146_r3_decided_items_never_lowered.py-15-DECIDED = ("e1", "e2", "e3", "a1", "f_r3_1", "f_r6_1", "f_gap_r6_r7")
tests/unit/test_t146_r3_decided_items_never_lowered.py-16-
tests/unit/test_t146_r3_decided_items_never_lowered.py-17-
tests/unit/test_t146_r3_decided_items_never_lowered.py:18:def down(step):
tests/unit/test_t146_r3_decided_items_never_lowered.py-19-    return AU.LLMFailed(f"{step} down", last_error="TIMEOUT")
tests/unit/test_t146_r3_decided_items_never_lowered.py-20-
tests/unit/test_t146_r3_decided_items_never_lowered.py-21-
tests/unit/test_t146_r3_decided_items_never_lowered.py:22:def model_flag(user):
tests/unit/test_t146_r3_decided_items_never_lowered.py-23-    """A model flag for record 3 with the same quote as the lexicon flag f_r3_1: the two corroborate (origin lexicon+llm, verified)."""
tests/unit/test_t146_r3_decided_items_never_lowered.py-24-    return {"flags": [dict(type="pre_existing", category="pre_existing", excerpt="Patient reports low back pain in 2023, resolved.")] if which_record(user)[0] == 3 else []}
tests/unit/test_t146_r3_decided_items_never_lowered.py-25-
tests/unit/test_t146_r3_decided_items_never_lowered.py-26-
tests/unit/test_t146_r3_decided_items_never_lowered.py-27-def _no_calls(v):
tests/unit/test_t146_r3_decided_items_never_lowered.py-28-    return {a: _no_calls(b) for a, b in v.items() if a not in ("call_id", "rerun_note")} if isinstance(v, dict) else v
--
tests/unit/test_t146_r3_decided_items_never_lowered.py:49:def rerun(conn, cid, **script):
tests/unit/test_t146_r3_decided_items_never_lowered.py-50-    script.setdefault("flags", model_flag)
tests/unit/test_t146_r3_decided_items_never_lowered.py-51-    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(**script)), now=lambda: 3.0)
tests/unit/test_t146_r3_decided_items_never_lowered.py-52-
tests/unit/test_t146_r3_decided_items_never_lowered.py-53-
tests/unit/test_t146_r3_decided_items_never_lowered.py:54:def case_error(conn, cid):
tests/unit/test_t146_r3_decided_items_never_lowered.py-55-    c = DB.get_case(conn, cid)
tests/unit/test_t146_r3_decided_items_never_lowered.py-56-    return c["status"], (json.loads(c["error"]) if c["error"] else None)
tests/unit/test_t146_r3_decided_items_never_lowered.py-57-
tests/unit/test_t146_r3_decided_items_never_lowered.py-58-
tests/unit/test_t146_r3_decided_items_never_lowered.py-59-def note(conn, cid, i):
tests/unit/test_t146_r3_decided_items_never_lowered.py-60-    return (DB.get_item(conn, i, cid)["ladder"] or {}).get("rerun_note")
---
19:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
20-           "confirm_date": None, "keep_my_wording": None,
21-           "not_duplicate": None, "manual_entry": None}          # None = logged only, status unchanged
22-_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
23-_ITEM_TABLE_OF = {"entry": "entries", "amount": "amounts", "flag": "flags"}
24-_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
25-_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
26-_SCHEMA = os.path.join(os.path.dirname(__file__), "schema.sql")
27-
28-
29-def init(path: str = ":memory:"):
30-    return connect(path)
31-
--
34:AUDIT_ONLY_ACTIONS = ("reclassify", "rejudge")          # logged by log_event(); never change review_status, so apply_review() refuses them
35-log = logging.getLogger("zlayt.db")
36-
37-
38-def connect(path: str):
39-    """Open (and create) the database. A file written by an older schema version is deleted and rebuilt (one log line, no data
40-    text): the schema uses CREATE IF NOT EXISTS, so an old file would otherwise keep its old keys, and keeping it aside would keep
41-    pasted text past the 24 h purge (T-040 security r2)."""
42-    if path != ":memory:" and os.path.exists(path) and os.path.getsize(path) > 0:
43-        probe = sqlite3.connect(path)
44-        try:
45-            version = probe.execute("PRAGMA user_version").fetchone()[0]
46-            has_tables = probe.execute("SELECT count(*) FROM sqlite_master WHERE type='table'").fetchone()[0] > 0
--
218:    if action not in ACTIONS:
219-        raise ValueError(f"invalid review action {action!r}")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:15:17.076Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/probe_t165.py",
 "content": "\"\"\"Reviewer probe for T-165 (staff-engineer-reviewer). Runs against the git-archive copy of HEAD 312efe6 (PYTHONPATH=<archive>, cwd=<archive>).\nEach scenario prints the observable state: case status, error, export blockers, warnings, tray, entry ids.\"\"\"\nimport json, os, sys, tempfile\n\nfrom app.backend import pipeline as PL, present, review as RV, trace\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script, which_record\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import model_flag, down\n\nTMP = tempfile.mkdtemp(prefix=\"t165probe_\")\nJ1_OK = FakeCall({\"j1\": {\"verdict\": \"supported\", \"reason_code\": \"NONE\"}})\n\n\ndef extract_down(*nos):\n    good = sample_script()[\"extract\"]\n\n    def extract(user):\n        if which_record(user)[0] in nos:\n            raise down(\"extract\")\n        return good(user)\n    return extract\n\n\ndef new_case(name):\n    conn = DB.connect(os.path.join(TMP, f\"{name}.sqlite\"))\n    cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    return conn, cid\n\n\ndef run(conn, cid, nos=(), now=1.0):\n    out = PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(extract=extract_down(*nos), flags=model_flag)), now=lambda: now)\n    return out\n\n\ndef state(conn, cid, label):\n    c = DB.get_case(conn, cid)\n    err = json.loads(c[\"error\"]) if c[\"error\"] else None\n    view = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\n    entries = sorted(e[\"id\"] for e in DB.list_items(conn, cid, \"entry\"))\n    print(f\"== {label}\")\n    print(\"   status:\", c[\"status\"], \"| error:\", json.dumps(err, sort_keys=True))\n    print(\"   export_blockers:\", sorted(b[\"reason_code\"] for b in trace.export_blockers(conn, cid)))\n    print(\"   warnings:\", [(w[\"code\"], w.get(\"record_no\"), w.get(\"item_id\")) for w in view[\"warnings\"]])\n    print(\"   tray record_ids:\", [t[\"record_ids\"] for t in view[\"tray\"]])\n    print(\"   entry ids:\", entries)\n\n\ndef hand(conn, cid, n):\n    rec = G.records(\"sample\")[n - 1]\n    return RV.manual_entry(conn, cid, f\"r{n}\", {\"summary\": rec[\"excerpt\"], \"excerpt\": rec[\"excerpt\"]}, call=J1_OK)\n\n\nwhich = sys.argv[1:] or [\"all\"]\n\nif \"all\" in which or \"A\" in which:\n    conn, cid = new_case(\"A\")\n    out = run(conn, cid, nos=(1,))\n    print(\"A run status:\", out[\"status\"], \"counts.entries:\", out[\"counts\"][\"entries\"])\n    state(conn, cid, \"A one record down, first run\")\n\nif \"all\" in which or \"B\" in which:\n    conn, cid = new_case(\"B\")\n    out = run(conn, cid, nos=range(1, 10))\n    print(\"B run status:\", out[\"status\"])\n    state(conn, cid, \"B all nine down, first run\")\n\nif \"all\" in which or \"C\" in which:\n    conn, cid = new_case(\"C\")\n    out = run(conn, cid, nos=())\n    print(\"C run status:\", out[\"status\"])\n    state(conn, cid, \"C every record extracted, first run\")\n\nif \"all\" in which or \"D\" in which:\n    conn = DB.connect(os.path.join(TMP, \"D.sqlite\"))\n    cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    PL.ingest_case(conn, cid, G.raw(\"sample\"))\n    hand(conn, cid, 1)\n    out = run(conn, cid, nos=(1,))\n    state(conn, cid, \"D hand-entered BEFORE run, extract down on record 1\")\n\nif \"all\" in which or \"E\" in which:\n    conn, cid = new_case(\"E\")\n    run(conn, cid, nos=(1,))\n    hand(conn, cid, 1)\n    state(conn, cid, \"E hand-entered AFTER failed first run\")\n\nif \"all\" in which or \"F\" in which:\n    conn, cid = new_case(\"F\")\n    run(conn, cid, nos=(1,))\n    hand(conn, cid, 1)\n    run(conn, cid, nos=(1,), now=2.0)\n    state(conn, cid, \"F hand-entry pending, re-run with record 1 still down\")\n\nif \"all\" in which or \"G\" in which:\n    conn, cid = new_case(\"G\")\n    run(conn, cid, nos=(1,))\n    hand(conn, cid, 1)\n    run(conn, cid, nos=(), now=2.0)\n    state(conn, cid, \"G hand-entry pending, re-run where record 1 NOW extracts (AI entry e1 created)\")\n\nif \"all\" in which or \"H\" in which:\n    conn, cid = new_case(\"H\")\n    run(conn, cid, nos=(1,))\n    hand(conn, cid, 1)\n    RV.apply_action(conn, cid, \"e1_m\", \"dismiss\", now=3.0) if hasattr(RV, \"apply_action\") else None\n    state(conn, cid, \"H hand-entry then dismissed (dismiss call attempted if RV.apply_action exists)\")\n"
}
````

### User / tool · 2026-11-02T16:15:17.152Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/probe_t165.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:15:21.552Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"^def \" app/backend/review.py | head -60",
 "description": "List review module functions in HEAD archive"
}
````

### User / tool · 2026-11-02T16:15:21.657Z

**tool result**
````
29:def _now(now):
33:def _item(conn, case_id, item_id):
43:def _bad(msg, **detail):
47:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
59:def _date_unconfirmed_error():
78:def current_text(item: dict):
83:def edit_unconfirmed(kind: str, item: dict) -> bool:
92:def code_check_failures(rec, item: dict) -> dict:
117:def code_check_message(fails: dict) -> str:
142:def code_check_detail(item_id: str, fails: dict) -> dict:
150:def code_check_error(item_id: str, rec, item: dict):
158:def bill_state_for(conn, case_id: str, record_ids) -> str:
164:def charge_text_error(item_id: str, item: dict, state_fn=None):
179:def hold_hints(conn, case_id: str, entry_views: list) -> None:
194:def entry_record(item: dict, recs: list):
199:def confirm_error(item_id: str, item: dict, confirm):
212:def confirmed_accept(item: dict) -> bool:
218:def _record_confirm(conn, case_id: str, item_id: str, item: dict, t) -> None:
237:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None, confirm=None) -> dict:
271:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
298:def ocr_record_ids(conn, case_id: str) -> set:
308:def enforce_ocr(conn, case_id: str, t) -> int:
337:def _quoted_words(toks) -> str:
342:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False, bill_state=None):
385:def _edit(conn, case_id, kind, item, body, call, t):
458:def restore_pre_edit(conn, case_id: str, item_id: str, kind: str, item: dict, t) -> bool:
488:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
526:def _without_date_doubt(item: dict) -> dict:
541:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
549:def _drop(conn, case_id, flag_id):
554:def _gap_figures(flag: dict) -> dict:
559:def _gap_changes(old: dict, new: dict) -> list:
582:def _gap_change_sentence(ch: dict, seq) -> str:
591:def _recompute_gaps(conn, case_id, t, changes=None):
635:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
685:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
748:def _upsert(conn, case_id, kind, item, t):
758:def judges_for(dollars, call, case_text):
764:def batch_apply(conn, case_id: str, item_id: str, action: str, now: float, recs: list = None) -> None:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:15:25.591Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && sed -n 271,297p app/backend/review.py; cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/unit_head.txt 2>/dev/null | tail -3",
 "description": "Read review apply_review body contract"
}
````

### User / tool · 2026-11-02T16:15:25.715Z

**tool result**
````
def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = _now(now)
    kind, item = _item(conn, case_id, item_id)
    action = (body or {}).get("action")
    if action not in ACTIONS:
        raise _bad("That action is not allowed.")
    if item["state"] == "rejected" and action in ("accept", "edit"):
        raise ReviewError(409, "item_rejected", message="This item could not be verified; it can only be dismissed or reset.")
    if action in ("accept", "edit") and date_unconfirmed(conn, case_id, kind, item):    # D-041; before any write, edit implies accept
        raise _date_unconfirmed_error()
    warnings = []
    if action in ("accept", "dismiss", "reset"):
        confirm = body.get("confirm")
        if confirm is not None and not isinstance(confirm, str):
            raise _bad("The confirm must be the name of the flag.")
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item, confirm=confirm)
        if action == "reset":
            restore_pre_edit(conn, case_id, item_id, kind, item, t)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


/bin/bash: child setpgid (64438 to 64438): Operation not permitted
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:15:34.993Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165 && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py <<'EOF'\n\"\"\"Reviewer probe for T-165 (staff-engineer-reviewer), run against a git archive of HEAD 312efe6.\nRun: cd <archive> && PYTHONPATH=<archive> <repo>/.venv/bin/python <this file> [A B C D E F G H]\nPrints observable state per scenario: case status/error, export blockers (trace.export_blockers), warnings, tray, entry ids.\"\"\"\nimport json, os, sys, tempfile\n\nfrom app.backend import pipeline as PL, present, review as RV, trace\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script, which_record\nfrom tests.unit.test_t146_r3_decided_items_never_lowered import model_flag, down\n\nTMP = tempfile.mkdtemp(prefix=\"t165probe_\")\nJ1_OK = FakeCall({\"j1\": {\"verdict\": \"supported\", \"reason_code\": \"NONE\"}})\n\n\ndef extract_down(*nos):\n    good = sample_script()[\"extract\"]\n\n    def extract(user):\n        if which_record(user)[0] in nos:\n            raise down(\"extract\")\n        return good(user)\n    return extract\n\n\ndef new_case(name):\n    conn = DB.connect(os.path.join(TMP, f\"{name}.sqlite\"))\n    return conn, DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n\n\ndef run(conn, cid, nos=(), now=1.0):\n    return PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(extract=extract_down(*nos), flags=model_flag)), now=lambda: now)\n\n\ndef state(conn, cid, label):\n    c = DB.get_case(conn, cid)\n    err = json.loads(c[\"error\"]) if c[\"error\"] else None\n    view = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\n    print(f\"== {label}\")\n    print(\"   status:\", c[\"status\"], \"| error:\", json.dumps(err, sort_keys=True))\n    print(\"   export_blockers:\", sorted(b[\"reason_code\"] for b in trace.export_blockers(conn, cid)))\n    print(\"   warnings:\", [(w[\"code\"], w.get(\"record_no\"), w.get(\"item_id\")) for w in view[\"warnings\"]])\n    print(\"   tray record_ids:\", [t[\"record_ids\"] for t in view[\"tray\"]])\n    print(\"   entries:\", sorted((e[\"id\"], e[\"review_status\"], e[\"state\"]) for e in DB.list_items(conn, cid, \"entry\")))\n\n\ndef hand(conn, cid, n):\n    rec = G.records(\"sample\")[n - 1]\n    return RV.manual_entry(conn, cid, f\"r{n}\", {\"summary\": rec[\"excerpt\"], \"excerpt\": rec[\"excerpt\"]}, call=J1_OK)\n\n\nwhich = sys.argv[1:] or list(\"ABCDEFGH\")\nprint(\"TMP\", TMP)\n\nif \"A\" in which:\n    conn, cid = new_case(\"A\"); out = run(conn, cid, nos=(1,))\n    print(\"A pipeline status:\", out[\"status\"], \"counts.entries:\", out[\"counts\"][\"entries\"], \"warnings:\", out[\"warnings\"])\n    state(conn, cid, \"A one of nine down, first run\")\nif \"B\" in which:\n    conn, cid = new_case(\"B\"); out = run(conn, cid, nos=range(1, 10))\n    print(\"B pipeline status:\", out[\"status\"])\n    state(conn, cid, \"B all nine down, first run\")\nif \"C\" in which:\n    conn, cid = new_case(\"C\"); out = run(conn, cid, nos=())\n    print(\"C pipeline status:\", out[\"status\"], \"errors:\", out[\"errors\"], \"warnings:\", out[\"warnings\"])\n    state(conn, cid, \"C every record extracted, first run\")\nif \"D\" in which:\n    conn = DB.connect(os.path.join(TMP, \"D.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n    PL.ingest_case(conn, cid, G.raw(\"sample\")); hand(conn, cid, 1)\n    out = run(conn, cid, nos=(1,))\n    print(\"D pipeline warnings:\", [(w[\"code\"], w[\"record_no\"]) for w in out[\"warnings\"]])\n    state(conn, cid, \"D hand-entered BEFORE the run, extract down on record 1\")\nif \"E\" in which:\n    conn, cid = new_case(\"E\"); run(conn, cid, nos=(1,)); hand(conn, cid, 1)\n    state(conn, cid, \"E hand-entered AFTER failed first run\")\nif \"F\" in which:\n    conn, cid = new_case(\"F\"); run(conn, cid, nos=(1,)); hand(conn, cid, 1)\n    run(conn, cid, nos=(1,), now=2.0)\n    state(conn, cid, \"F hand-entry pending, re-run with record 1 still down\")\nif \"G\" in which:\n    conn, cid = new_case(\"G\"); run(conn, cid, nos=(1,)); hand(conn, cid, 1)\n    run(conn, cid, nos=(), now=2.0)\n    state(conn, cid, \"G hand-entry pending, re-run where record 1 NOW extracts\")\nif \"H\" in which:\n    conn, cid = new_case(\"H\"); run(conn, cid, nos=(1,)); hand(conn, cid, 1)\n    RV.apply_review(conn, cid, \"e1_m\", {\"action\": \"dismiss\"}, now=3.0)\n    state(conn, cid, \"H hand-entry then dismissed by paralegal\")\nEOF\ncd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_out.txt",
 "description": "Run T-165 probe scenarios against HEAD archive copy"
}
````

### User / tool · 2026-11-02T16:15:36.577Z

**tool result**
````
TMP /var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/t165probe_cl83x68l
A pipeline status: done_with_errors counts.entries: 8 warnings: []
== A one of nine down, first run
   status: failed | error: {"code": "run_partial", "extract_only": true, "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1. Run it again to retry.", "records": [1]}
   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
   warnings: []
   tray record_ids: [['r1']]
   entries: [('e1', 'pending', 'rejected'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
B pipeline status: done_with_errors
== B all nine down, first run
   status: failed | error: {"code": "run_partial", "extract_only": true, "message": "The AI step failed for 9 items (writing the entries) on this run, and there is no earlier result to keep. No entry was made for records 1, 2, 3, 4, 5, 6, 7, 8 and 9. Run it again to retry.", "records": [1, 2, 3, 4, 5, 6, 7, 8, 9]}
   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
   warnings: []
   tray record_ids: [['r1'], ['r2'], ['r3'], ['r4'], ['r5'], ['r6'], ['r7'], ['r8'], ['r9']]
   entries: [('e1', 'pending', 'rejected'), ('e2', 'pending', 'rejected'), ('e3', 'pending', 'rejected'), ('e4', 'pending', 'rejected'), ('e5', 'pending', 'rejected'), ('e6', 'pending', 'rejected'), ('e7', 'pending', 'rejected'), ('e8', 'pending', 'rejected'), ('e9', 'pending', 'rejected')]
C pipeline status: done errors: [] warnings: []
== C every record extracted, first run
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: []
   tray record_ids: []
   entries: [('e1', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
D pipeline warnings: [('ENTERED_BY_HAND', 1)]
== D hand-entered BEFORE the run, extract down on record 1
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== E hand-entered AFTER failed first run
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== F hand-entry pending, re-run with record 1 still down
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== G hand-entry pending, re-run where record 1 NOW extracts
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: []
   tray record_ids: []
   entries: [('e1', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
== H hand-entry then dismissed by paralegal
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: [('ENTERED_BY_HAND', 1, 'e1')]
   tray record_ids: []
   entries: [('e1', 'pending', 'rejected'), ('e1_m', 'dismissed', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:00.675Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -rn -i \"never decides\\|decides for the paralegal\\|re-run\\|rerun\" memory/contracts/api.md memory/ORCHESTRATOR_DECISIONS.md docs/CONTRACT.md spec/REQUIREMENTS.md 2>/dev/null | grep -i \"pending\\|decid\\|keep\\|hand\\|manual\\|stale\" | head -30; echo ---; grep -rn -i \"entered by hand\\|ENTERED_BY_HAND\\|hand-entered\\|by hand\" memory/contracts/api.md memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md 2>/dev/null | head -20",
 "description": "Grep spec and API contract for rerun and hand-entry rules"
}
````

### User / tool · 2026-11-02T16:16:00.779Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:04.446Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"D-031\\|D-053\\|D-046\\|D-047\\|D-058\" memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md 2>/dev/null | cut -c1-600 | head -12; echo ---API; grep -n -i \"manual\\|entered_by\\|run_partial\\|ENTERED\" memory/contracts/api.md | cut -c1-400 | head -20",
 "description": "Show decisions on manual entry and API run_partial text"
}
````

### User / tool · 2026-11-02T16:16:04.711Z

**tool result**
````
memory/ORCHESTRATOR_DECISIONS.md:39:| D-031 | *(Reclassification cut here is superseded by D-042.)* **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_
memory/ORCHESTRATOR_DECISIONS.md:44:| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
memory/ORCHESTRATOR_DECISIONS.md:54:| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
memory/ORCHESTRATOR_DECISIONS.md:55:| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
memory/ORCHESTRATOR_DECISIONS.md:59:| D-051 | Code checks bind accept for **every** item (2026-11-02, T-098 review blocker): an item whose current summary fails any D-034/D-047/D-022 code check (e.g. an AI draft 'Pain 5/10' over a quote without 5/10) cannot be accepted, single or batch (422 with the reason; the paralegal must edit it to match the quote), and the export gate blocks it if such a state exists anyway. Only the judge step is exempt for human wording (D-045b); the code rung never is. | A one-click accept exported an invented number. | T-098 staff r1 F1 |
memory/ORCHESTRATOR_DECISIONS.md:61:| D-053 | Nothing the model proposes is silently dropped (2026-11-02, T-094 review blocker). A model-only flag or conflict that the judge rejects, or a model-proposed conflict that no code candidate confirms (the no-candidate rule applies to conflicts only; ADR-020), goes to the **could-not-verify tray** with the judge's reason; it is never a flag and never reaches the letter. The eval scores precision on emitted flags only (tray items are not assertions), and reports tray counts separately; R-CO-7's flag-set signature covers flags, not tray items. Conflict 
memory/ORCHESTRATOR_DECISIONS.md:65:| D-057 | Rule-filtered model proposals are listed, not dropped (2026-11-02, after T-113). A model-proposed flag that a code rule filters out (e.g. D-032 `objective_negative`: a normal finding is not a flag) goes to a collapsed, counted "Filtered by rule" group in the could-not-verify tray with the rule named; it is never in the timeline or letter and needs no action. | D-053 says nothing the model proposes is silently dropped; trays full of normal findings would be noise, so they are listed collapsed with a count. | T-113 backend question |
memory/ORCHESTRATOR_DECISIONS.md:66:| D-058 | A re-picked quote does not make the AI summary human-authored (2026-11-02, T-134 r3 / T-136 F-2). When she picks a different quote but keeps the AI summary, the summary is still LLM-made and its judge ran on the old quote, so D-044 still applies: the new summary–quote pair needs judge 1, and her "I compared it with the quote" does not replace it. If the judge cannot answer, the item stays out of the letter and the UI says so and names the way out (write the summary herself, which makes it human text under D-045). | The ladder rule: nothing LLM-ma
memory/DECISIONS.md:9:018 second-wave additions (D-031 to D-040) · 019 amendments after T-094 and D-047 to D-052 (amends 005, 011, 012, 013, 014, 017 in place; items 1 and 2 superseded by 020) · 020 amendments after T-094 round 2: D-042, D-052 to D-054, T-110 (amends 005, 011, 013, 014, 015, 017 in place).
memory/DECISIONS.md:143:- Status: accepted (M1, amended rounds 2 and 3; D-006, D-010, D-011, D-012, D-021; amended by ADR-019: no 409 edit path, D-047 and D-051 checks on accept; amended by ADR-020: guarded charge reclassification, D-042)
memory/DECISIONS.md:154:  - **Edit re-check order (R-RV-3, D-006):** (1) structure, else 422. (2) Code token check (ADR-012, widened by D-047 to sides, negations and qualifiers). A miss is a hard `422 invalid_edit`; nothing is saved; there is no confirm or `keep_my_wording` path (ADR-019). (3) Judge 1 re-runs against the edited text. If it objects (`partially`/`unsupported`): the edit is saved as `needs_review` with a warning; the judge never blocks a human-written edit (D-045b, ADR-019). If the judge fails (error, timeout) or there is no recorded fixture for the edit (always the case in demo 
memory/DECISIONS.md:220:- Status: accepted (round 2, amended round 3; D-004, D-005, D-010; amended by ADR-019: rate cue, D-047 and D-051 checks; amended by ADR-020: guarded reclassification, D-042)
---API
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409, re-run of a case that already has decisions only; never an edit or manual entry, D-047), `item_rejected` (409), `unsupported_language` 
27:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an un
104:**Items.** Every non-rejected entry, amount and flag whose record lies on an OCR page is `needs_review` with reason `OCR_DERIVED` (appendix), added by code after the model steps; no judge answer, edit, manual entry, not-a-duplicate split, reclassify, date confirmation or rejudge clears it (an edit of an OCR item stays `needs_review` with `OCR_DERIVED`, because the edit does not show that the p
129:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item fro
138:**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left 
372:- T-134 r3: `/judges` `totals.human_overrides` ("you accepted despite an objection") counts only her explicit accept; an open edit (`edit_to_check`) whose re-check objected stays in `rejections` and `totals.unsupported` but not in `human_overrides`. For a re-picked quote under the AI's own summary (`edit_to_check` with no second-check answer) the item `human` step, the `EDIT_NOT_CONFIRMED` gat
397:**Flags that need a named confirm (D-059).** A charge can carry `flag` (else `null`): `{flag: "likely_duplicate" | "likely_total", name, message, confirm_with, of, confirmed_at?}` and `confirm_required: true` while it is `pending`. `likely_duplicate`: set only when a paralegal PROMOTES a figure to a charge (reclassify, below) and it has the same normalized service date, service and amount as a
581:**Judge rationale is a closed reason code plus a fixed sentence (D-028).** The judge returns `verdict` + `reason_code` from a closed list, never prose, so `rationale` is the fixed sentence for that code (`why.judge_detail`), written by code. `reason_code` is read from `ladder.judge.reason_code`; for items stored before it was kept (amounts, edits, manual entries) it is read from the audited ca
661:`verdict.code` for the case: `ready` (export gate open), `needs_attention` (nothing accepted yet, or accepted items not double-checked), `running`, `failed`. The judge's closed `reason_code` is now kept in `ladder.judge.reason_code` for entries, amounts, flags, edits and manual entries (in `ladder_json`; no schema change).
663:**Export gate (exact, D-045).** `ready` equals "GET /export is allowed" in every state, and `ready == (blockers == [])`: both come from one function (`trace.export_blockers`), which the export endpoint refuses on. `blockers[]` holds only: `RUN_IN_PROGRESS` (a run is going), `RUN_FAILED` (the last run stopped; finished items are kept), `JUDGE_NOT_RUN` (D-044, below), `NOTHING_ACCEPTED` (nothing
731:      "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
735:      "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
762:- **Entry field `translation`** (every entry view; `null` for English records): `{source_language: "es", source_language_name: "Spanish", label: "AI translation", summary_is_translation: true, quote_is_original: true}`. After the paralegal edits the summary, or writes a manual entry, `label` is `"Translation (edited by reviewer)"`. The UI must show `label` next to the summary and show the quot
763:- **Never auto-verified (D-050).** Every item (entry, amount, flag) made from a record routed `es` or `uncertain` is `needs_review` with reason `AI_TRANSLATION` ("AI translation — check against the original"), whatever the Spanish code checks and the translation judge said. Their failures still show in the trace; passing them never yields `verified`. Enforced once, in `confidence.compose_sta
773:Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into clauses (`;` `,` sentence-ending `.` and the join ` and `; ` with ` is not a boundary, so `Neck pain consistent with sprain.` is one clause) and removes a clause only when it adds salient content its own quote lacks (T-112 r2): a procedure/treatment/device/drug term, a body part, or a diagnosis noun that the quote
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:08.181Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && sed -n 129p memory/contracts/api.md; echo; grep -n \"T-165\" memory/contracts/api.md | cut -c1-1500",
 "description": "Read the API contract rerun-erases rule and T-165 text"
}
````

### User / tool · 2026-11-02T16:16:08.282Z

**tool result**
````
`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was down) and the stored rows it would have overwritten, or deleted as stale, were left exactly as they were; `message` names how many items and which step ("The AI step failed for N items (writing the entries / the second check / finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."). **T-146 r3, one rule for every stage:** a re-run never lowers or replaces a *decided* item (accepted, dismissed or edited). If the new output for it fails a check (a stub, a flag made while the flag step was down, no second-check answer) or differs from it (a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false), the stored row is kept whole and its `ladder.rerun_note` is set to `{kind: "failed" | "disagreed", step, message, at}`; every item view also carries `rerun_note` (the message string, or `null`), to be shown on the item. `run_partial` then also has a sentence "The re-run gave a different result for N items you had already decided; your decision and the earlier result were kept, and each item carries a note." An undecided item is kept the same way only when the new row is a failure over stored output (no note); a new check result on an undecided item stands (a summary that fails the summary-in-quote check goes to the tray). The deadline path adds no note (nothing was redone) and keeps `run_deadline`. A re-run (the case already had entries) where a step failed and there was no earlier result to keep also reads `failed` / `run_partial`: "The AI step failed for N items (writing the entries) on this run, and there is no earlier result to keep. Run it again to retry." **T-161 / T-165, first run:** a first run with a failing step (a second check, the flag step, or the extract step on ANY record) stores its failure stubs and reads `failed` / `run_partial` too, and the export gate lists `RUN_FAILED`. When the extract step failed with nothing to keep, the message ends with "No entry was made for record 4." / "No entry was made for records 2, 3 and 7." and the error carries `records` (the record numbers, ascending; the first record of a duplicate group) and, when the extract step is the whole failure, `extract_only: true`. **Hand-entered exception (D-031/D-053):** a record the paralegal has entered by hand (tray manual entry, `POST /records/{rid}/entry`) is not a failure: it is left out of `records`, and `GET case` `warnings[]` (always `[]` before) carries one `{code: "ENTERED_BY_HAND", record_no, item_id (the could-not-verify placeholder), message: "The AI step could not write an entry for record 6; you entered it by hand."}` per such record (computed on read; the run result carries the same). Entering a record by hand also re-reads an `extract_only` failure: the entered records leave `records` and the message, and when none is left the case reads `ready` with `error: null` (no re-run needed); a failure with any other cause is left as it is. A re-run whose extract fails again for a hand-entered record keeps the pending hand-entered entry (it is not swept as a stale row). A run where every record extracted stays `ready` with `error: null`. A good re-run clears the error and the notes (the row is replaced by the new one). **Second-check wording (T-145/T-146):** the `why` of a `JUDGE_UNAVAILABLE` item reads "JUDGE_NOT_RUN: the second AI check did not run or did not finish..." when no judge ran, and "The second check failed (the AI check was asked and gave no usable answer)..." when the judge was called and gave no answer (`ladder.judge.verdict: "unavailable"`, `reason_code` other than `JUDGE_NOT_RUN`); the state reason code is `JUDGE_UNAVAILABLE` in both. Poll every second. Partial results are readable from the case endpoint while running.

129:`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline" | "run_partial", "message": "..."}`. **T-146 (r1+r2): a re-run never erases earlier work.** `run_deadline`: the run passed its time limit; it only adds items that had no stored row, and every earlier item, second-check answer and decision of the paralegal is kept unchanged ("every item from earlier runs and every decision of yours was kept unchanged"). `run_partial`: an AI step failed on a re-run (the extract step made a failure stub, a second check gave no answer, or the flag step was down) and the stored rows it would have overwritten, or deleted as stale, were left exactly as they were; `message` names how many items and which step ("The AI step failed for N items (writing the entries / the second check / finding the flags) on this run. Their earlier results and every decision of yours were kept unchanged. Run it again to retry."). **T-146 r3, one rule for every stage:** a re-run never lowers or replaces a *decided* item (accepted, dismissed or edited). If the new output for it fails a check (a stub, a flag made while the flag step was down, no second-check answer) or differs from it (a worse state, a different summary, quote, date, amount or flag evidence, or worse checks inside the same state: a reason code the stored row did not have, a backing second-check answer (agree, supported, conflict) that is now negative, a code check that was true and is now false), th
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:24.859Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && sed -n 244,262p app/backend/pipeline.py; echo ---; grep -n \"tray_filtered\\|tray =\" app/backend/present.py | head; echo ---; grep -n \"_EXTRACT_STEP\\|def _noting\" -n app/backend/pipeline.py | head -3; sed -n 470,493p app/backend/pipeline.py",
 "description": "Read failure classification and tray filtering code"
}
````

### User / tool · 2026-11-02T16:16:24.975Z

**tool result**
````
_EXTRACT_STEP = "writing the entries"


def _failure(kind: str, it: dict):
    """T-146 r3: what failed in the NEW row `it` alone, as the step's name, or None: an entry that is a failure stub (the AI step gave nothing), a flag made while the flag
    step failed, or an item whose second check was asked and gave no answer."""
    if kind == "entry" and it.get("state") == "rejected" and set(it.get("reasons") or []) & _STUB_REASONS:
        return _EXTRACT_STEP
    if kind == "flag" and set(it.get("reasons") or []) & _FLAG_FAIL:
        return "finding the flags"
    return "the second check" if ((it.get("ladder") or {}).get("judge") or {}).get("verdict") == "unavailable" else None


def _degrades(kind: str, old: dict, it: dict):
    """T-146 r2/r3: would storing `it` over the stored row `old` replace output with a failure, or take back a second-check answer? Returns the step's name or None.
    (entry) the AI step gave nothing where the stored row has a summary and a quote; (flag) the flag step failed and the stored row was not made from a failure;
    (any AI-made item) the second check gave no answer where the stored row had one. A failure is never allowed to erase earlier work."""
    cause = _failure(kind, it)
    if cause == _EXTRACT_STEP:
---
321:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
341:    tray_filtered = {"label": "Filtered by rule", "collapsed": True, "needs_action": False, "count": len(filtered), "rules": rules}
349:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
---
244:_EXTRACT_STEP = "writing the entries"
251:        return _EXTRACT_STEP
262:    if cause == _EXTRACT_STEP:
    case = DB.get_case(conn, cid)
    err = json.loads(case["error"]) if case.get("error") else None
    if case["status"] != "failed" or not err or err.get("code") != "run_partial" or not err.get("extract_only"):
        return
    hand = generator.entered_by_hand(DB.list_items(conn, cid, "entry"))
    left = [n for n in err["records"] if f"r{n}" not in hand]
    if left == err["records"]:
        return
    new = _partial_error([], [_EXTRACT_STEP] * len(left), records=left) if left else None
    DB.update_case(conn, cid, status="failed" if new else "ready", error=json.dumps(new) if new else None)


def _noting(raw_call, failed_steps: list):
    """T-146 r2: the same `call`, remembering the steps whose call failed (the AI layer gave up, or a fixture was missing). The failure still propagates to the
    caller's own handling; this only lets the run say which steps were down."""
    def call(step, system, user, schema, *, item_id=None):
        try:
            return raw_call(step, system, user, schema, item_id=item_id)
        except (AU.LLMFailed, P.FixtureMiss):
            failed_steps.append(step)
            raise
    return call
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:30.507Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && ls -la && tail -c 600 unit_head.txt",
 "description": "Check progress of background unit suite run"
}
````

### User / tool · 2026-11-02T16:16:30.603Z

**tool result**
````
total 1096
drwxr-xr-x@    9 arsis  wheel     288 Nov  2 10:14 .
drwx------@ 1609 arsis  wheel   51488 Nov  2 10:16 ..
-rw-r--r--@    1 arsis  wheel  149102 Nov  2 10:14 archive_all.txt
-rw-r--r--@    1 arsis  wheel   81784 Nov  2 10:14 archived.txt
drwxr-xr-x@   21 arsis  wheel     672 Nov  2 10:14 head
-rw-r--r--@    1 arsis  wheel  149102 Nov  2 10:14 head_all.txt
-rw-r--r--@    1 arsis  wheel   84910 Nov  2 10:14 head_tracked.txt
-rw-r--r--@    1 arsis  wheel   84910 Nov  2 10:14 tracked.txt
-rw-r--r--@    1 arsis  wheel    2253 Nov  2 10:16 unit_head.txt
................... [ 29%]
........................................................................ [ 31%]
........................................................................ [ 32%]
........................................................................ [ 34%]
........................................................................ [ 35%]
........................................................................ [ 36%]
........................................................................ [ 38%]
........................................................................ [ 39%]
.............
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:43.107Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && cat > mut.py <<'EOF'\nimport sys, pathlib\n# usage: mut.py <src_root> <dst_root> <relpath> <old> <new>   (exactly one occurrence required)\nsrc, dst, rel, old, new = sys.argv[1:6]\np = pathlib.Path(dst) / rel\nt = p.read_text()\nassert t.count(old) == 1, (\"count\", t.count(old))\np.write_text(t.replace(old, new))\nprint(\"mutated\", rel)\nEOF\nfor m in m1 m2 m3; do rm -rf $m; cp -R head $m; done\n/Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m1 app/backend/pipeline.py 'continue                                # T-165: the paralegal'\"'\"'s own entry for a record the AI could not do' 'pass' && \\\n/Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m2 app/backend/review.py '    PL.refresh_extract_error(conn, case_id)' '    pass' && \\\n/Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m3 app/backend/generator.py '    return sorted(out, key=lambda w: w[\"record_no\"])' '    return []'\nfor m in m1 m2 m3; do (cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/$m && echo \"== $m\" && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t165_partial_extract.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py 2>&1 | tail -n 12); done",
 "description": "Apply three mutants to scratch copies and run targeted tests"
}
````

### User / tool · 2026-11-02T16:16:43.169Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion ($m) is blocked | command: cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf80
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:47.441Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && cp -R head m1 && cp -R head m2 && cp -R head m3 && ls -d m1 m2 m3 && /Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m1 app/backend/pipeline.py 'continue                                # T-165: the paralegal'\"'\"'s own entry for a record the AI could not do' 'pass' && /Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m2 app/backend/review.py '    PL.refresh_extract_error(conn, case_id)' '    pass' && /Users/arsis/zlayt-pm-project/.venv/bin/python mut.py head m3 app/backend/generator.py '    return sorted(out, key=lambda w: w[\"record_no\"])' '    return []'",
 "description": "Create three mutant copies of the HEAD archive"
}
````

### User / tool · 2026-11-02T16:16:49.833Z

**tool result (error)**
````
Exit code 2
m1
m2
m3
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python: can't open file '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/mut.py': [Errno 2] No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:54.263Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/mut.py <<'EOF'\n\"\"\"Apply one exact-once text mutation to a copy: mut.py <dst_root> <relpath> <old> <new>.\"\"\"\nimport sys, pathlib\ndst, rel, old, new = sys.argv[1:5]\np = pathlib.Path(dst) / rel\nt = p.read_text()\nassert t.count(old) == 1, (\"count\", t.count(old))\np.write_text(t.replace(old, new))\nprint(\"mutated\", rel)\nEOF\ncd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && M=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/mut.py && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && $PY $M m1 app/backend/pipeline.py '                continue                                # T-165: the paralegal'\"'\"'s own entry for a record the AI could not do' '                pass' ; $PY $M m2 app/backend/review.py '    PL.refresh_extract_error(conn, case_id)' '    pass' ; $PY $M m3 app/backend/generator.py '    return sorted(out, key=lambda w: w[\"record_no\"])' '    return []'",
 "description": "Apply three single-line mutations to the mutant copies"
}
````

### User / tool · 2026-11-02T16:16:54.441Z

**tool result**
````
mutated app/backend/pipeline.py
mutated app/backend/review.py
mutated app/backend/generator.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:16:58.133Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && for m in m1 m2 m3; do echo \"== $m\"; (cd $m && PYTHONPATH=. timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t165_partial_extract.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py 2>&1 | grep -E \"^FAILED|passed|failed\" | head -12); done",
 "description": "Run targeted T-165 tests against each mutant copy"
}
````

### User / tool · 2026-11-02T16:16:58.252Z

**tool result**
````
== m1
== m2
== m3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:01.297Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/m1 && PYTHONPATH=. timeout 300 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t165_partial_extract.py 2>&1 | tail -n 30",
 "description": "Run T-165 test file against mutant m1 with full output"
}
````

### User / tool · 2026-11-02T16:17:01.390Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:04.112Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/m1 && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t165_partial_extract.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py 2>&1 | tail -n 15",
 "description": "Run targeted tests against mutant m1 with output"
}
````

### User / tool · 2026-11-02T16:17:10.140Z

**tool result**
````
    def test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready(tmp_path):
        conn, cid, _ = run(tmp_path, 1)
        hand_entry(conn, cid, 1)
        run(tmp_path, 1, again=(conn, cid), now=2.0)
        assert case_error(conn, cid) == ("ready", None)
>       assert "e1_m" in {e["id"] for e in DB.list_items(conn, cid, "entry")}      # the pending hand-entered row is not swept as a stale row
        ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       AssertionError: assert 'e1_m' in {'e1', 'e2', 'e3', 'e4', 'e5', 'e6', ...}

tests/unit/test_t165_partial_extract.py:150: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_t165_partial_extract.py::test_a_record_entered_by_hand_before_the_run_is_a_named_warning_not_a_failure
FAILED tests/unit/test_t165_partial_extract.py::test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready
2 failed, 85 passed in 5.69s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:14.081Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && for m in m2 m3; do echo \"== $m\"; (cd $m && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t165_partial_extract.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py 2>&1 | grep -E \"^FAILED|passed|failed\" | tail -n 8); done; echo; echo \"== H-scenario tests coverage: grep dismiss in T-165 test file\"; grep -n \"dismiss\\|G_\\|extract_only\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_out.txt | head -2; cd head && grep -n \"dismiss\" tests/unit/test_t165_partial_extract.py | head",
 "description": "Report mutant results and check dismiss coverage in T-165 tests"
}
````

### User / tool · 2026-11-02T16:17:24.677Z

**tool result**
````
== m2
____ test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named ____
    def test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named(tmp_path):
>       assert status == "failed" and err["records"] == [2]
E       AssertionError: assert ('failed' == 'failed'
E           failed and [1, 2] == [2]
FAILED tests/unit/test_t165_partial_extract.py::test_entering_the_failed_record_by_hand_after_the_run_clears_the_failure_into_a_warning
FAILED tests/unit/test_t165_partial_extract.py::test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named
2 failed, 85 passed in 4.85s
== m3
    def test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named(tmp_path):
        assert status == "failed" and err["records"] == [2]
        assert err["message"] == "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 2." + TAIL_
FAILED tests/unit/test_t165_partial_extract.py::test_a_record_entered_by_hand_before_the_run_is_a_named_warning_not_a_failure
FAILED tests/unit/test_t165_partial_extract.py::test_entering_the_failed_record_by_hand_after_the_run_clears_the_failure_into_a_warning
FAILED tests/unit/test_t165_partial_extract.py::test_entering_one_of_two_failed_records_by_hand_leaves_the_other_named
FAILED tests/unit/test_t165_partial_extract.py::test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready
4 failed, 83 passed in 5.19s

== H-scenario tests coverage: grep dismiss in T-165 test file
4:   status: failed | error: {"code": "run_partial", "extract_only": true, "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. No entry was made for record 1. Run it again to retry.", "records": [1]}
5:   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:34.592Z

**tool call — Bash**
````
{
 "command": "sleep 60; cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 400 unit_head.txt; echo; grep -n \"export_blockers\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head/app/backend/*.py | head -5",
 "description": "Wait briefly and check unit suite result file"
}
````

### User / tool · 2026-11-02T16:17:34.594Z

**tool result (error)**
````
<tool_use_error>Blocked: sleep 60 followed by: cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review tail -c 400 unit_head.txt echo grep -n "export_blockers" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head/app/backend/*.py head -5. To wait for a condition, use Monitor with an until-loop (e.g. `until <check>; do sleep 2; done`). To wait for a command you started, use run_in_background: true. Do not chain shorter sleeps to work around this block.</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:37.164Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 400 unit_head.txt; echo; grep -rn \"export_blockers\" head/app/backend/ | cut -c1-160 | head -6",
 "description": "Check unit suite progress and export gate call sites"
}
````

### User / tool · 2026-11-02T16:17:37.254Z

**tool result**
````
................................................................. [ 54%]
........................................................................ [ 55%]
........................................................................ [ 56%]
........................................................................ [ 58%]
........................................................................ [ 59%]
.......
head/app/backend/store.py:115:    if blockers:                                        # trace.export_blockers calls this with blockers=False to build the letter
head/app/backend/store.py:117:        out["export_blockers"] = trace.export_blockers(conn, case_id, case=out)       # D-045: build_export refuses while this is 
head/app/backend/store.py:118:        out["judge_not_run"] = [b for b in out["export_blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
head/app/backend/trace.py:1132:    blockers = export_blockers(conn, case_id, cx, rv)          # D-045: the same list GET /export refuses on; ready == (blockers 
head/app/backend/trace.py:1198:def export_blockers(conn, case_id: str, cx=None, rv=None, case=None) -> list:
head/app/backend/export.py:836:    line number), so the answer does not depend on the style asked for, and the trace export gate (trace.export_blockers) and GET
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:43.362Z

**tool call — Bash**
````
{
 "command": "P=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && mkdir -p $P/parent && git archive ea988f8 | tar -x -C $P/parent && cd $P/parent && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py G 2>&1 | tail -n 8",
 "description": "Run scenario G against the parent commit ea988f8 archive"
}
````

### User / tool · 2026-11-02T16:17:44.731Z

**tool result**
````
TMP /var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/t165probe_n3fakn7z
== G hand-entry pending, re-run where record 1 NOW extracts
   status: ready | error: null
   export_blockers: ['NOTHING_ACCEPTED']
   warnings: []
   tray record_ids: []
   entries: [('e1', 'pending', 'verified'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:17:47.837Z

**tool call — Bash**
````
{
 "command": "P=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && cd $P/parent && PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-165/probe_t165.py F 2>&1 | tail -n 6",
 "description": "Run scenario F against parent archive to confirm the fix delta"
}
````

### User / tool · 2026-11-02T16:17:48.829Z

**tool result**
````
== F hand-entry pending, re-run with record 1 still down
   status: failed | error: {"code": "run_partial", "message": "The AI step failed for 1 item (writing the entries) on this run, and there is no earlier result to keep. Run it again to retry."}
   export_blockers: ['NOTHING_ACCEPTED', 'RUN_FAILED']
   warnings: []
   tray record_ids: [['r1']]
   entries: [('e1', 'pending', 'rejected'), ('e2', 'pending', 'verified'), ('e3', 'pending', 'verified'), ('e4', 'pending', 'verified'), ('e5', 'pending', 'verified'), ('e6', 'pending', 'verified'), ('e7', 'pending', 'verified'), ('e8', 'pending', 'verified'), ('e9', 'pending', 'verified')]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:14.198Z

**tool call — Bash**
````
{
 "command": "git show 312efe6 -- app tests | grep -E \"^\\+\" | grep -nE \"except|float\\(|sleep\\(|retry|https?://|api_key|sk-\" | head; echo \"grep-exit=$?\"; cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && grep -rn \"allow_failed\" head/tests/unit | cut -c1-150; tail -c 300 unit_head.txt",
 "description": "Grep T-165 diff for banned patterns and check suite progress"
}
````

### User / tool · 2026-11-02T16:18:14.318Z

**tool result**
````
36:+    err = {"code": "run_partial", "message": " ".join(parts + ["Run it again to retry."])} if parts else None
138:+TAIL_ = " Run it again to retry."
grep-exit=0
head/tests/unit/test_t139_charge_text.py:20:    _wait_ready(c, tok, allow_failed=True)
head/tests/unit/test_api_routes.py:24:def wait_ready(c, tok, allow_failed=False):
head/tests/unit/test_api_routes.py:30:    assert s["status"] == "ready" or (allow_failed and s["status"] == "failed"), s
...................... [ 72%]
........................................................................ [ 73%]
........................................................................ [ 75%]
............ss.......................................................... [ 76%]
..............................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:26.778Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 250 unit_head.txt",
 "description": "Check unit suite progress again"
}
````

### User / tool · 2026-11-02T16:18:26.882Z

**tool result**
````
.............................................. [ 79%]
........................................................................ [ 81%]
........................................................................ [ 82%]
....................................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:31.382Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"live_rids = \\|T-165: the paralegal's own entry\\|def refresh_extract_error\\|def entered_by_hand\\|def hand_entered_warnings\\|PL.refresh_extract_error\\|e\\[\\\"state\\\"\\] != \\\"rejected\\\" and (e.get\" app/backend/pipeline.py app/backend/review.py app/backend/generator.py; grep -n \"def test_a_rerun_that_extracts\\|def test_a_rerun_with_the_record_still_down\\|def test_a_record_entered_by_hand_before\" tests/unit/test_t165_partial_extract.py; grep -n \"T-165 test\\|ENTERED_BY_HAND\" app/backend/present.py | head -3; grep -n \"warnings\\\": generator.hand\" app/backend/present.py | cut -c1-80",
 "description": "Collect HEAD file:line references for findings"
}
````

### User / tool · 2026-11-02T16:18:31.509Z

**tool result**
````
app/backend/generator.py:205:def entered_by_hand(entries: list) -> set:
app/backend/generator.py:207:    return {r for e in entries if e["state"] != "rejected" and (e.get("ladder") or {}).get("entered_by") == "reviewer" for r in (e["record_ids"] or [])}
app/backend/generator.py:210:def hand_entered_warnings(entries: list) -> list:
app/backend/pipeline.py:368:    live_rids = {r for i in items if kind == "entry" and i.get("state") != "rejected" for r in (i.get("record_ids") or [])}
app/backend/pipeline.py:372:                continue                                # T-165: the paralegal's own entry for a record the AI could not do
app/backend/pipeline.py:466:def refresh_extract_error(conn, cid: str) -> None:
app/backend/review.py:678:    PL.refresh_extract_error(conn, case_id)      # T-165: a case that failed only because this record had no entry no longer fails
103:def test_a_record_entered_by_hand_before_the_run_is_a_named_warning_not_a_failure(tmp_path):
145:def test_a_rerun_with_the_record_still_down_keeps_the_hand_entry_and_reads_ready(tmp_path):
154:def test_a_rerun_that_extracts_the_record_clears_the_failure(tmp_path):
351:            "review": review_view(conn, case_id), "warnings": generator.hand
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:36.044Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review/head && grep -n \"DELETE FROM {table}\" app/backend/pipeline.py; sleep 1; tail -c 200 ../unit_head.txt",
 "description": "Locate stale-row DELETE line and recheck suite"
}
````

### User / tool · 2026-11-02T16:18:37.185Z

**tool result**
````
376:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
............ [ 89%]
........................................................................ [ 90%]
........................................................................ [ 92%]
....................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:40.559Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:40.651Z

**tool result**
````
...................... [ 89%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
..............................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:43.105Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress again"
}
````

### User / tool · 2026-11-02T16:18:43.185Z

**tool result**
````
... [ 89%]
........................................................................ [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
.................................................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:45.641Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress once more"
}
````

### User / tool · 2026-11-02T16:18:45.733Z

**tool result**
````
......................................... [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
...........
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:48.083Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:48.211Z

**tool result**
````
.. [ 90%]
........................................................................ [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
..................................................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:50.512Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:50.599Z

**tool result**
````
..................................................................... [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
...............................................................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:52.894Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:52.984Z

**tool result**
````
............................................................. [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
.......................................................................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:55.498Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:55.613Z

**tool result**
````
....................................... [ 92%]
........................................................................ [ 93%]
........................................................................ [ 95%]
........................................................................ [ 96%]
.............
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:18:57.940Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 300 unit_head.txt",
 "description": "Check unit suite progress"
}
````

### User / tool · 2026-11-02T16:18:58.021Z

**tool result**
````
............................. [ 95%]
........................................................................ [ 96%]
........................................................................ [ 98%]
........................................................................ [ 99%]
.......................
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:00.644Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t165-review && tail -c 400 unit_head.txt",
 "description": "Check unit suite final output"
}
````

### User / tool · 2026-11-02T16:19:00.732Z

**tool result**
````
..................... [ 95%]
........................................................................ [ 96%]
........................................................................ [ 98%]
........................................................................ [ 99%]
..........................                                               [100%]
5058 passed, 8 skipped in 276.41s (0:04:36)
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:19.652Z

**tool call — Bash**
````
{
 "command": "ls -la reviews/ | grep -i \"T-165\" ; echo \"exists-check-done\"; grep -c \"\" artifacts/review-evidence/T-165/probe_out.txt",
 "description": "Check whether a T-165 review file already exists"
}
````

### User / tool · 2026-11-02T16:19:19.775Z

**tool result**
````
exists-check-done
53
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:40.604Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer.md",
 "content": "# T-165 staff-engineer review (commit 312efe6)\n\nVerdict: **fail**. One blocker: a re-run that extracts a hand-entered record again deletes the paralegal's pending entry with no note. The contract says a re-run never erases earlier work. The T-165 hand-entry protection covers only the branch where the record stays down.\n\nScope: commit 312efe6 (HEAD at review time), read on a `git archive 312efe6` copy. The working tree is dirty with other agents' files and was not used. Golden sample and synthetic two-record notes only.\n\nWhat holds (checked by running the code):\n- A first run with the extract step down on one record (1 of 9), eight of nine, or all nine reads `failed` / `run_partial`, names the records, and the export gate lists `RUN_FAILED`. Probe A, B.\n- A run where every record extracted reads `ready`, `error: null`, no warnings. Probe C.\n- A record entered by hand before the run, or after a failed run, gives an `ENTERED_BY_HAND` warning and no failure. Probe D, E.\n- A re-run where the record is still down keeps the pending hand-entered entry `e1_m`. Probe F. On the parent `ea988f8` the same probe deletes `e1_m`, so the fix is real for this branch.\n\nBlocker, detail: scenario G. A hand-entered record (`e1_m`, pending) is entered, then the re-run extracts record 1 successfully. The final entries are `e1` (AI, pending) only; `e1_m` is gone, the case reads `ready`, and no warning is shown. The sweep at `app/backend/pipeline.py:368-376` skips the delete only when `live_rids` does not cover the record; once the AI writes a live `e1`, the `DELETE` at line 376 removes the paralegal's row. `memory/contracts/api.md:129` says \"a re-run never erases earlier work\", and the T-165 text in the same line protects a hand-entered entry only \"whose extract fails again\". The same G probe on `ea988f8` also loses `e1_m`, so this was already present and T-165 did not close it. No test covers it: `tests/unit/test_t165_partial_extract.py:154` (`test_a_rerun_that_extracts_the_record_clears_the_failure`) has no hand entry.\n\nMinor, detail: scenario H. After the paralegal dismisses `e1_m`, the case reads `ready`, the tray is empty, the failure does not come back, and the `ENTERED_BY_HAND` warning still says \"you entered it by hand\". No test covers dismissal.\n\nMinor, detail: the four pins named in the brief are justified (see the JSON). A fifth changed assertion, `tests/unit/test_t139_charge_text.py` `counts.entries` 3 to 4, counts the hand entry as an entry; it is a workaround for the T-168 fixture gap and should be reverted with T-168.\n\nPin justification (each one checked against the api.md T-165 text):\n1. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_and_no_entries...`: exact error now carries `records` and `extract_only` and names records 1 to 9. Justified by the AC.\n2. `test_t161_first_run_stage_down.py::test_first_run_with_extract_down_for_some_records...`: `ready` flipped to `failed`, `records == [1]`. Justified by \"any record whose extract step failed makes the case run_partial\".\n3. `test_t146_r3_decided_items_never_lowered.py::test_rerun_with_nothing_to_keep...`: exact error gains `records` and `extract_only` and the names. Justified by the AC.\n4. `test_t146_r3_decided_items_never_lowered.py::test_nothing_to_keep_and_something_kept...`: message gains \"No entry was made for record 4.\" Justified by the AC.\n\nMutation spot-checks on scratch copies of the archive (mutant text is in the commands below):\n- m1: remove the hand-entry skip at pipeline.py:372. Targeted tests: 2 fail (`test_a_rerun_with_the_record_still_down_keeps_the_hand_entry...`, `test_a_record_entered_by_hand_before_the_run...`). Killed.\n- m2: drop `PL.refresh_extract_error` at review.py:678. Targeted tests: 2 fail. Killed.\n- m3: `hand_entered_warnings` returns `[]`. Targeted tests: 4 fail. Killed.\n\nCommands and outputs are saved in `artifacts/review-evidence/T-165/` (`probe_t165.py`, `probe_out.txt`, `mut.py`).\n\n```json\n{\"card\": \"T-165\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 312efe6 (HEAD at review time) via git archive copy at artifacts-free scratch dir; files: app/backend/pipeline.py, generator.py, present.py, review.py; tests/unit/test_t165_partial_extract.py, _hand_entry.py, test_t161_first_run_stage_down.py, test_t146_r3_decided_items_never_lowered.py, test_t139_charge_text.py, test_api_routes.py, test_case_list.py, test_t114_rates_and_demo_judges.py; contract memory/contracts/api.md:129; synthetic golden sample and two-record synthetic note; no app URL exercised (in-process only)\",\n \"exercised\": [\n  \"python3 tools/board.py show T-165 (card read: status in_review, ac 1 done, handoff)\",\n  \"reviews/T-161-staff-engineer-r2.md read in full\",\n  \"git show 312efe6 --stat and git diff 312efe6^ 312efe6 for all app and test files in the commit\",\n  \"git archive 312efe6 | tar -x into scratchpad t165-review/head; file list diffed against git ls-tree -r 312efe6 (identical, 1213 fixture files included)\",\n  \"cd head && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 5058 passed, 8 skipped, exit 0 (276 s). Worker handoff quoted 4961 on archive plus hunks; not reconciled, does not change the verdict\",\n  \"artifacts/review-evidence/T-165/probe_t165.py run on HEAD archive, scenarios A-H -> artifacts/review-evidence/T-165/probe_out.txt (status, error, export_blockers via trace.export_blockers, warnings, tray, entries)\",\n  \"same probe scenario F and G on git archive ea988f8 (parent): G deletes e1_m on the parent too (pre-existing); F deletes e1_m on the parent (fixed by T-165)\",\n  \"mutant m1 (pipeline.py:372 continue -> pass) on scratch copy: t165 + t161 + t146_r3 files -> 2 failed, 85 passed\",\n  \"mutant m2 (review.py:678 PL.refresh_extract_error -> pass): 2 failed, 85 passed\",\n  \"mutant m3 (generator.py hand_entered_warnings return [] ): 4 failed, 83 passed\",\n  \"grep of the T-165 diff for except, float(, sleep(, network or key strings: none added (only the word 'retry' in a message string)\",\n  \"grep -rn dismiss on the T-165 test file: no test covers a dismissed hand entry\",\n  \"grep allow_failed and export_blockers call sites in head/app/backend (export gate is trace.export_blockers, per api.md:663 and export.py:836)\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"first_run_partial_names_records\": 4, \"all_extracted_stays_ready\": 5, \"hand_entry_warning_not_failure\": 4, \"rerun_keeps_pending_hand_entry\": 2, \"dismiss_and_recover_states\": 2, \"pins_justified\": 4, \"test_strength_mutants\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"A re-run that extracts a hand-entered record again silently deletes the paralegal's pending entry\",\n   \"evidence\": \"Probe G (artifacts/review-evidence/T-165/probe_out.txt, block '== G'): after hand entry on record 1 and a re-run with record 1 extracting, entries are e1 (AI, pending, verified) only; e1_m is gone; status ready, warnings []. Code: app/backend/pipeline.py:368 live_rids; :372 continue applies only when the record has no live row; :376 DELETE FROM entries ... review_status='pending' removes e1_m. Contract: memory/contracts/api.md:129 'a re-run never erases earlier work'; T-165 text in the same line protects the hand entry only 'whose extract fails again'. Pre-existing: the same probe on git archive ea988f8 also loses e1_m. Repro: git archive 312efe6 | tar -x -C D; cd D && PYTHONPATH=$PWD <repo>/.venv/bin/python <repo>/artifacts/review-evidence/T-165/probe_t165.py G\",\n   \"why_it_matters\": \"The paralegal's typed summary and quote are removed by a re-run with no note and no warning, while the case reads ready. The contract states that a re-run never erases earlier work. The card that claims to protect hand-entered entries leaves this path open, and the brief's check 'a re-run keeps a pending hand-entered entry' fails for this case.\",\n   \"fix\": \"Keep a pending hand-entered entry on every re-run, not only while its record has no live AI row. When the AI also now has an entry for that record, keep both and set a rerun_note on the hand entry (for example 'the AI step now has an entry for record 1; your entry was kept, it is pending'). Remove the live_rids condition at pipeline.py:372 for entered_by=reviewer rows.\",\n   \"acceptance_test\": \"tests/unit/test_t165_partial_extract.py: run with record 1 down, hand-enter record 1, re-run with record 1 extracting. Assert e1_m is still in DB.list_items(conn, cid, 'entry') with review_status 'pending', its ladder.rerun_note is set, and the case status is ready. On HEAD this test fails (e1_m is absent).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Dismissing a hand-entered entry leaves a stale ENTERED_BY_HAND warning and the failure never returns\",\n   \"evidence\": \"Probe H (probe_out.txt, block '== H'): after RV.apply_review(conn, cid, 'e1_m', {'action': 'dismiss'}), e1_m has review_status 'dismissed', case status ready, error null, tray [], warnings [('ENTERED_BY_HAND', 1, 'e1')]. generator.py:205-207 entered_by_hand counts any non-rejected entry, dismissed included. No test in tests/unit/test_t165_partial_extract.py mentions dismiss.\",\n   \"why_it_matters\": \"The warning tells the paralegal 'you entered it by hand' about an entry they dismissed. Record 1 has no usable entry, and the case no longer shows the extract failure. The dismissed entry is still visible in the entry list, so this is not silent, but the case-level message is wrong.\",\n   \"fix\": \"Exclude dismissed hand entries from entered_by_hand, or word the warning by state. Decide with Chris whether dismissing the hand entry re-opens the extract failure (see questions_for_chris).\",\n   \"acceptance_test\": \"Hand-enter record 1 after a failed run, then dismiss e1_m. Assert the chosen state: either RUN_FAILED and record 1 named again, or no ENTERED_BY_HAND warning. Pin the chosen one.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Fifth changed assertion outside the named pins: test_t139 counts.entries 3 to 4 counts a hand entry as an entry\",\n   \"evidence\": \"tests/unit/test_t139_charge_text.py diff: '-    assert j[\\\"counts\\\"][\\\"entries\\\"] == 3' / '+    assert j[\\\"counts\\\"][\\\"entries\\\"] == 4                      # e1, e5, e6 and the hand-entered record 3 (wait_ready)'. Caused by the lib01 fixture gap (T-168) worked around with enter_failed_records_by_hand (tests/unit/_hand_entry.py).\",\n   \"why_it_matters\": \"An assertion about the AI-made timeline now counts a paralegal entry. It is documented in the comment and is a test-data workaround, but it will need reverting when T-168 lands, and it can hide a real AI regression on lib01.\",\n   \"fix\": \"Keep the workaround, but assert the AI-made count separately from the hand entry (for example count entries whose ladder.entered_by is not 'reviewer' equals 3, and the hand entry id is present). Revert with T-168.\",\n   \"acceptance_test\": \"test_t139 lib01 assertion: AI-made entries == 3 and the hand entry e3_m present; mutant that drops one AI entry fails the test.\"}\n ],\n \"whats_right\": [\n  \"A first run with the extract step down on one, eight or all nine records reads failed / run_partial, names the records, and the export gate lists RUN_FAILED; all-extracted stays ready with error null (probe A, B, C)\",\n  \"A hand entry before the run or after a failed run gives an ENTERED_BY_HAND warning, not a failure; a still-down re-run keeps the pending hand entry, where the parent ea988f8 deleted it (probe D, E, F vs parent)\",\n  \"The four pins in tests/unit/test_t161_first_run_stage_down.py and tests/unit/test_t146_r3_decided_items_never_lowered.py each change one assertion to the behaviour the api.md T-165 text names; mutants m1, m2, m3 are killed by the T-165 file\"\n ],\n \"questions_for_chris\": [\n  \"When a record's extract failed and the paralegal hand-enters it, then dismisses that entry: should the extract failure (RUN_FAILED and the tray placeholder) come back, or stay cleared?\",\n  \"On a re-run that extracts a record the paralegal had entered by hand and that entry is still pending: keep both (with a note), or is the sweep a deliberate decision? Reading of api.md:129 is keep both.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T16:19:40.760Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:46.655Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer.md",
 "old_string": "Mutation spot-checks on scratch copies of the archive (mutant text is in the commands below):\n- m1: remove the hand-entry skip at pipeline.py:372. Targeted tests: 2 fail (`test_a_rerun_with_the_record_still_down_keeps_the_hand_entry...`, `test_a_record_entered_by_hand_before_the_run...`). Killed.\n- m2: drop `PL.refresh_extract_error` at review.py:678. Targeted tests: 2 fail. Killed.\n- m3: `hand_entered_warnings` returns `[]`. Targeted tests: 4 fail. Killed.\n\nCommands and outputs are saved in `artifacts/review-evidence/T-165/` (`probe_t165.py`, `probe_out.txt`, `mut.py`).",
 "new_string": "Mutation spot-checks on scratch copies of the archive (targeted run: `tests/unit/test_t165_partial_extract.py tests/unit/test_t161_first_run_stage_down.py tests/unit/test_t146_r3_decided_items_never_lowered.py`; mutation helper `artifacts/review-evidence/T-165/mut.py`):\n- m1: `pipeline.py:372` `continue` replaced by `pass`. 2 fail (`test_a_rerun_with_the_record_still_down_keeps_the_hand_entry...`, `test_a_record_entered_by_hand_before_the_run...`). Killed.\n- m2: `review.py:678` `PL.refresh_extract_error(...)` replaced by `pass`. 2 fail. Killed.\n- m3: `generator.py` `hand_entered_warnings` returns `[]`. 4 fail. Killed.\n\nProbe scenarios and output: `artifacts/review-evidence/T-165/probe_t165.py` and `probe_out.txt`. Scenarios F and G were also run on the parent archive `ea988f8`; those outputs are in the transcript, not saved as a file."
}
````

### User / tool · 2026-11-02T16:19:46.706Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-165-staff-engineer.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:51.380Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,re\nt=open('reviews/T-165-staff-engineer.md').read()\nm=re.findall(r'\\`\\`\\`json\\n(.*?)\\`\\`\\`', t, re.S)\nprint('json blocks:', len(m))\nd=json.loads(m[0])\nprint(d['card'], d['persona'], d['model'], d['verdict'])\nsev=[f['severity'] for f in d['findings']]\nprint(sev)\nexp='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('verdict rule expects:', exp, 'match:', exp==d['verdict'])\n\"",
 "description": "Validate review JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T16:19:51.432Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:54.084Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py review --help 2>&1 | head -5; /Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-165/check_json.py 2>/dev/null; echo \"---\"; cat > artifacts/review-evidence/T-165/check_json.py <<'EOF'\n\"\"\"Parse the JSON block of reviews/T-165-staff-engineer.md and apply the verdict rule.\"\"\"\nimport json, re, sys\nt = open(sys.argv[1]).read()\nblocks = re.findall(r\"`{3}json\\n(.*?)`{3}\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(d[\"card\"], d[\"persona\"], d[\"model\"], d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"severities:\", sev, \"| rule expects:\", exp, \"| match:\", exp == d[\"verdict\"])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-165/check_json.py reviews/T-165-staff-engineer.md",
 "description": "Validate review JSON block and verdict rule via evidence script"
}
````

### User / tool · 2026-11-02T16:19:54.140Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: `board.py review` is orchestrator-only
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:19:56.511Z

**tool call — Bash**
````
{
 "command": "cat > artifacts/review-evidence/T-165/check_json.py <<'EOF'\n\"\"\"Parse the JSON block of reviews/T-165-staff-engineer.md and apply the verdict rule.\"\"\"\nimport json, re, sys\nt = open(sys.argv[1]).read()\nblocks = re.findall(r\"`{3}json\\n(.*?)`{3}\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(d[\"card\"], d[\"persona\"], d[\"model\"], d[\"verdict\"])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"severities:\", sev, \"| rule expects:\", exp, \"| match:\", exp == d[\"verdict\"])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python artifacts/review-evidence/T-165/check_json.py reviews/T-165-staff-engineer.md",
 "description": "Validate review JSON block and verdict rule via evidence script"
}
````

### User / tool · 2026-11-02T16:19:56.628Z

**tool result**
````
json blocks: 1
T-165 staff-engineer-reviewer claude-haiku-5-5 fail
severities: ['blocker', 'minor', 'minor'] | rule expects: fail | match: True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:20:00.371Z

Verdict fail: blocker is a re-run that recovers a record silently deletes the paralegal's pending hand entry (`app/backend/pipeline.py:368-376`); the `ENTERED_BY_HAND` warning, the still-down keep, the all-ready path and the four pins all check out. Review at `/Users/arsis/zlayt-pm-project/reviews/T-165-staff-engineer.md`; its prose has two wording slips I could not correct because the write-once guard blocks edits, but the JSON block parses and the verdict rule holds.
