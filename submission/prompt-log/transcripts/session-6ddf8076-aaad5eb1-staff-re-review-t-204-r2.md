# Subagent: Staff re-review: T-204 r2 (Staff re-review: T-204 r2)

Source: `agent-aaad5eb15d0550481.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-03T01:14:24.329Z

Re-review T-204, round 2, in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. The fix commit is 679b63e; read reviews/T-204-staff-engineer.md and the handoff.

In a fresh `git archive 679b63e`:
1. Re-run your probes from artifacts/review-evidence/T204_*. Check that the rail, the AI-check panel and every screen show no AI-attributing wording on the prepared sample, in both the classic UI (with ZLAYT_MODE=local) and the guided UI.
2. Judge the two exceptions:
   - the guided step 1 banner uses the server's ai_banner: what does it say in demo mode?
   - the suggestions.js line "tested on the claude-cli backend" is allow-listed: is it accurate and acceptable?
3. Mutate a fallback back to AI wording in the rail and confirm the document-wide observer test fails.

Write reviews/T-204-staff-engineer-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:26.286Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-03T01:14:26.300Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:26.583Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-204-staff-engineer.md"
}
````

### User / tool · 2026-11-03T01:14:26.592Z

**tool result**
````
1	# T-204 review — staff-engineer-reviewer (round 1), commit 9b37b9c
2	
3	Verdict: fail (one blocker). The commit itself is clean and the two things the card changed work and are well pinned. But AC 1 says "for a prepared case no screen ever paints 'AI' wording", and the same prepared item the new test drives still gets "kept the AI's summary" on the case rail and in the AI-check panel, in static text the card never touched.
4	
5	1. Commit content: confirmed. `git diff --name-status 105d212 9b37b9c` lists exactly app/frontend/input.js, review.js, switcher.js (M) and tests/e2e/test_prepared_first_paint.py (A). 9b37b9c has parent 105d212, and `git diff b4af023 9b37b9c` over those four paths is empty (same content as the replaced commit). b4af023 also had parent 105d212, but its tree was stale: `git diff --stat b4af023^ b4af023` = 151 files changed, 49927 deletions. It is not an ancestor of HEAD, so it is orphaned; HEAD (d23687e) descends from 9b37b9c. Nobody's work is reverted by 9b37b9c. One caveat is the shared index (finding 3).
6	2. Prepared items, classic review.js: first paint and swap are correct for the three nodes it watches (edit-check-hint, edit-compare-prompt, compare-export-note). Mutants M1-M3 (isPrepared always false; heldText always AI; accepted note always AI) each fail the new test. Guided review.js: confirmed no client-side AI fallback. Item text goes through R.plain(item.why) from the server, R.tagFor checks item.prepared first, and step4 blockers come from the server trace. Grep for "no answer", "AI's wording" and "AI wrote" in app/frontend/guided/*.js found nothing painted for an item. Read and grep only, not exercised in a browser. Not covered by the card: stepper.js and judges.js (finding 1).
7	3. Late library: works. Removing the listener (M4), removing the dispatch in switcher.js (M5) and rebuilding on every event (M6, overwrites an unrelated error) each fail one of the three tests.
8	4. Tests: new file 3 passed on the clean archive. Full tests/e2e from a fresh `git archive 9b37b9c` with E2E_REQUIRE_DB=1: 561 passed, 1 skipped, 0 failed (796.88 s). test_code_check_refusal::test_case_verdict_reads_the_backend_label_in_rail_and_panel passed in that run and 5 of 5 alone (about 2 s each). I could not reproduce the worker's failure. It is outside the card's four files. My hypothesis, not tested: open_rail clicks the summary only if the details is closed, so a late auto-open could toggle it shut under load. Machine load average was 11-14 during my run.
9	
10	```json
11	{"card": "T-204", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
12	 "scope": "commit 9b37b9c vs parent 105d212 (app/frontend/input.js, review.js, switcher.js, tests/e2e/test_prepared_first_paint.py); stepper.js and judges.js read for the same prepared-item flow; git archive copies of 9b37b9c with private fixture-backend servers; HEAD at review time d23687e (descends from 9b37b9c)",
13	 "exercised": [
14	  "Read personas/staff-engineer.md, the card and handoff (board.py show T-204), memory/ORCHESTRATOR_DECISIONS.md D-065 and D-069",
15	  "git diff --name-status 105d212 9b37b9c: 4 files (3 M, 1 A); git diff 105d212 9b37b9c -- app/frontend read in full; git diff b4af023 9b37b9c on the four paths: empty",
16	  "git merge-base --is-ancestor: b4af023 NOT an ancestor of HEAD, 9b37b9c is; git diff --stat b4af023^ b4af023: 151 files, 49927 deletions (the stale commit)",
17	  "git diff --cached --stat in the shared repo: index holds the reverse of the card (6 files, 122 deletions); git status shows 'D  tests/e2e/test_prepared_first_paint.py' staged, the file untracked in the tree, identical content to HEAD for the other three",
18	  "Read tests/e2e/test_prepared_first_paint.py in full; read guided/review.js 1-130, guided step2/3/4 reason paths, stepper.js 505-535, judges.js lines 96/163/189 by grep and sed",
19	  "git archive 9b37b9c into scratchpad T204_r1/clean; tests/e2e/test_prepared_first_paint.py with E2E_REQUIRE_DB=1: 3 passed",
20	  "Mutants in separate archive copies (grep-confirmed counts): M1 isPrepared=>false, M2 heldText=>AI_HELD, M3 accepted note=>ACCEPTED_HELD: each 1 failed, 2 passed (first_paint test, lines 46/46/60); M4 no zl:switcher listener, M5 no dispatch: late-library test fails; M6 always rebuild: unrelated-error test fails (scripts artifacts/review-evidence/T204_mutate.py and T204_mutate_input.py)",
21	  "Full tests/e2e from a fresh archive (diff -rq clean == full) at 9b37b9c, E2E_REQUIRE_DB=1: 561 passed, 1 skipped in 796.88s (artifacts/review-evidence/T204_full_e2e_9b37b9c.log)",
22	  "test_case_verdict_reads_the_backend_label_in_rail_and_panel alone x5 on the same archive: 5 passed",
23	  "Probe artifacts/review-evidence/T204_probe_rail.py copied into the clean archive as tests/e2e/test_probe_t204.py: same prepared held item as the card's test, then reload, open the case rail and the AI-check panel: fails with 'kept the AI's summary' in rail_all (3 places) and judge_panel (screenshot artifacts/review-evidence/T204_probe_rail.png)",
24	  "grep of the new test for except/float(/sleep(/wait_for_timeout/setInterval: wait_for_timeout 200 and 800, setInterval 20"
25	 ],
26	 "verdict": "fail",
27	 "scores": {"AC 1 coverage of prepared wording": 2, "input.js late-library fix": 5, "test strength (mutation)": 4, "commit hygiene": 4, "determinism of tests": 4},
28	 "findings": [
29	  {"severity": "blocker",
30	   "title": "Prepared held item still reads 'kept the AI's summary' on the case rail and the AI-check panel, so AC 1 ('no screen ever paints AI wording') is not met",
31	   "evidence": "app/frontend/stepper.js:523-526 S.HELD_NO_RERUN / S.HELD_CAN_RERUN hard-code \"kept the AI's summary ... the second AI check\", used by heldWords at stepper.js:273 and :292 and by judges.js:96 and :189; none of them checks item.prepared or models.generator_prepared (judges.js:163 does for another sentence). Repro: cp artifacts/review-evidence/T204_probe_rail.py <git archive 9b37b9c>/tests/e2e/test_probe_t204.py; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_probe_t204.py -q -s. The probe first asserts the entry is prepared (entries[].prepared is True), then output: PROBE rail_all -> [\" You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote.\", \"... What you need to do: You changed the quote on an accepted entry and kept the AI's summary, ...\"] and PROBE judge_panel -> [\"... What you need to do: You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote.\"]. The card's WATCH in tests/e2e/test_prepared_first_paint.py:14-19 only observes edit-check-hint, edit-compare-prompt and compare-export-note, so the green test cannot see this.",
32	   "why_it_matters": "D-065 forbids presenting a curated answer as the AI's, and D-069 requires every user-facing string for a prepared item to come from a prepared-specific template. The card's own AC is 'no screen ever' for a prepared case. These sentences are static, not transient, and appear on the same page and item the new test drives, so the card reports a fixed over-claim that is still on screen. This is the GATE-M3 PM blocker class (an over-claim of provenance).",
33	   "fix": "Give S.HELD_NO_RERUN / S.HELD_CAN_RERUN a prepared twin keyed by the item (isPrepared in the same way as review.js: item.prepared or case models.generator_prepared), without rewriting the AI text. Pass the item or case into heldWords (stepper.js:273, :292) and the two judges.js call sites. Share one isPrepared helper rather than a second copy. Use plural-aware prepared wording (one and many), and keep 'second AI check' only where the real judge is meant, or drop AI to match the card's own regex.",
34	   "acceptance_test": "Extend tests/e2e/test_prepared_first_paint.py: after the held accept, open the case rail and the AI-check panel and assert no /\\bAI\\b|\\bmodel\\b/i match in gate-blocker, case-step, zs-todo-text and the export-blocked message text (or one page-text scan with a named allow-list for real judge verdict chips such as 'AI did not check'); mutate S.HELD_* back to the AI wording and confirm the test fails."},
35	  {"severity": "minor",
36	   "title": "Shared index stages the reverse of the card, including a staged delete of the new test",
37	   "evidence": "git diff --cached --stat: .claude/hooks/git_guard.py, app/frontend/input.js (6), review.js (12), switcher.js (1), tests/e2e/test_prepared_first_paint.py (104 deletions), tools/tests/test_git_guard.py; git status --short: 'D  tests/e2e/test_prepared_first_paint.py' and '?? tests/e2e/test_prepared_first_paint.py'; MM on the three frontend files. The staged state is the 105d212 tree, left behind when HEAD was moved by plumbing.",
38	   "why_it_matters": "Any commit without a pathspec (the CLAUDE.md rule exists for this) would silently revert T-204 and the git_guard change from the very commit this review approves, and the tree would show no diff. The 9b37b9c content is fine; the hazard is the index.",
39	   "fix": "Orchestrator resets the index for those paths (git reset -q -- <the 6 paths>) after confirming nobody has real staged work there; commit by pathspec only.",
40	   "acceptance_test": "git diff --cached --name-only is empty for those paths and git status does not show the staged D."},
41	  {"severity": "minor",
42	   "title": "AC 1 evidence ran on the stale tree and recorded a red; it does not support the checked box",
43	   "evidence": "Card AC 1 evidence: '555 passed, 1 skipped, 1 failed ... full tests/e2e from git archive of the commit tree'. Note 2026-11-03T00:35:51Z says that run was on the older base tree and only 5 touching files were re-run on 9b37b9c. The AC text is 'full tests/e2e green from a fresh archive'. My run on 9b37b9c: 561 passed, 1 skipped, 0 failed.",
44	   "why_it_matters": "A checked AC cited a run that was not green and was not on the reviewed commit; evidence should be at the same sha as the commit that ships.",
45	   "fix": "Re-record AC 1 evidence with the sha and the 561/1/0 result (or this review's log path).",
46	   "acceptance_test": "AC evidence names 9b37b9c and a green full-suite count."},
47	  {"severity": "nit",
48	   "title": "New test settles with fixed timeouts",
49	   "evidence": "tests/e2e/test_prepared_first_paint.py:31 page.wait_for_timeout(200) before releasing held routes; :101 wait_for_timeout(800) before the negative assertion; WATCH setInterval(scan, 20) at :20. The negative tests have teeth (M6 killed it), so this is a determinism preference, not a failure.",
50	   "why_it_matters": "Fowler: avoid bare sleeps. Under heavy load 800 ms may elapse before the late event, making the check weaker, not flaky-red.",
51	   "fix": "Wait on a condition (the held route was released and the library request finished) instead of a sleep.",
52	   "acceptance_test": "No wait_for_timeout in the file; the three tests and mutants M4-M6 behave as above."}
53	 ],
54	 "whats_right": [
55	  "Prepared fallback sentences in review.js are keyed by the item, not by rewriting the AI text, and the new test watches every text a node held via MutationObserver: three mutants all die.",
56	  "The zl:switcher event plus a refusing flag rebuilds only the demo refusal; M4, M5 and M6 are each caught by a different one of the three tests.",
57	  "Replacement commit 9b37b9c has exactly the four intended files on the right parent, and the full tests/e2e is green at that sha (561 passed, 1 skipped)."
58	 ],
59	 "questions_for_chris": []}
60	```
61	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:27.022Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t204_prepared_wording_patterns.md"
}
````

### User / tool · 2026-11-03T01:14:27.035Z

**tool result**
````
1	---
2	name: project_t204_prepared_wording_patterns
3	description: T-204 r1: fix covered the three watched nodes in review.js but static AI-worded constants in stepper.js/judges.js still paint on the same prepared item; shared index held the reverse of a plumbing-swapped commit
4	metadata:
5	  type: project
6	---
7	T-204 r1 (9b37b9c, 2026-11-02): fail, one blocker. The card fixed review.js fallbacks and input.js late-library refusal; mutants M1-M6 all died; full e2e 561/1 skip/0 fail.
8	The miss: "no screen ever paints AI wording for a prepared case" still failed on the case rail and AI-check panel (stepper.js S.HELD_NO_RERUN/S.HELD_CAN_RERUN, judges.js:96,189 say "kept the AI's summary"). The test's WATCH selector list covered only three nodes.
9	**Why:** AC with a universal claim ("no screen ever") was proven by a test that watched a closed list of nodes.
10	**How to apply:** for any "no X wording anywhere for prepared" card, grep app/frontend for the AI constants (`AI's`, `second AI check`) and run a probe that reads the whole rail/panel text on the same item; run a property-style page-text scan, not a node list. Compare with [[project_t177_provenance_patterns]] and [[project_t167_plain_wording_patterns]].
11	Also: the replaced commit b4af023 had the right parent but a stale tree (151 files, 49927 deletions). After HEAD was moved by plumbing the shared index kept the reverse of the card (staged D on the new test) - check `git diff --cached --stat` and see [[feedback_shared_index_staged_deletes]]. The rail test test_case_verdict_reads_the_backend_label_in_rail_and_panel passed 6/6 for me (worker saw one red under load); not reproduced.
12	
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:27.874Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-204 | tail -60; git log --oneline | head -5; ls artifacts/review-evidence | grep T204"
}
````

### User / tool · 2026-11-03T01:14:28.159Z

**tool result**
````
---
id: "T-204"
title: "Frontend: no AI-worded fallback sentence painted for a prepared item before the server text arrives (review.js); input.js refusal updates when the library loads late"
milestone: "M3"
role: "frontend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-03T00:15:43Z"
updated_at: "2026-11-03T01:14:20Z"
claimed_by: "frontend"
claimed_at: "2026-11-03T00:54:53Z"
rounds: 1
commits: ["b4af023", "9b37b9c", "679b63e"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "fail", "file": "reviews/T-204-staff-engineer.md", "at": "2026-11-03T00:54:45Z"}
ac:
  - {"n": 1, "text": "for a prepared case no screen ever paints 'AI' wording, even transiently (e2e asserts on first paint and after swap); refused-paste message re-renders when the library list arrives; full tests/e2e green from a fresh archive", "done": true, "evidence": "commit 679b63e: tests/e2e/test_prepared_first_paint.py (5 tests incl. whole-document MutationObserver classic walk, 2 mutants die); full tests/e2e from git archive 679b63e E2E_REQUIRE_DB=1: 567 passed, 1 skipped, 0 failed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-03T00:15:56Z frontend: claimed
- 2026-11-03T00:33:40Z frontend: AC 1 checked: tests/e2e/test_prepared_first_paint.py (3 tests) pass; 2 fail on the old HEAD; full tests/e2e from git archive of the commit tree (E2E_REQUIRE_DB=1): 555 passed, 1 skipped, 1 failed (test_code_check_refusal::test_case_verdict_reads_the_backend_label_in_rail_and_panel, case-step hidden under load; passes alone, file 23/23)
- 2026-11-03T00:33:40Z frontend: moved in_progress -> in_review
- 2026-11-03T00:35:51Z frontend: Commit b4af023 was built on a stale base (HEAD moved to 105d212 meanwhile) and would have reverted others; replaced by 9b37b9c (parent 105d212, 4 files only, HEAD ref moved from b4af023). Full 555-pass run was on the older base tree; re-ran the 5 touching files on 9b37b9c.
- 2026-11-03T00:36:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-03T00:54:45Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): fail — reviews/T-204-staff-engineer.md; round 1; findings:
    - [blocker] Prepared held item still reads 'kept the AI's summary' on the case rail and the AI-check panel, so AC 1 ('no screen ever paints AI wording') is not met — fix: Give S.HELD_NO_RERUN / S.HELD_CAN_RERUN a prepared twin keyed by the item (isPrepared in the same way as review.js: item.prepared or case models.generator_prepared), without rewriting the AI text. Pass the item or case into h
    - [minor] Shared index stages the reverse of the card, including a staged delete of the new test — fix: Orchestrator resets the index for those paths (git reset -q -- <the 6 paths>) after confirming nobody has real staged work there; commit by pathspec only.
    - [minor] AC 1 evidence ran on the stale tree and recorded a red; it does not support the checked box — fix: Re-record AC 1 evidence with the sha and the 561/1/0 result (or this review's log path).
- 2026-11-03T00:54:45Z orchestrator: assigned: frontend
- 2026-11-03T00:54:53Z frontend: claimed
- 2026-11-03T01:14:09Z frontend: r2: swept AI wording; committed 679b63e; full tests/e2e from git archive 679b63e, E2E_REQUIRE_DB=1: 567 passed, 1 skipped, 0 failed (792 s).
- 2026-11-03T01:14:16Z frontend: AC 1 checked: commit 679b63e: tests/e2e/test_prepared_first_paint.py (5 tests incl. whole-document MutationObserver classic walk, 2 mutants die); full tests/e2e from git archive 679b63e E2E_REQUIRE_DB=1: 567 passed, 1 skipped, 0 failed
- 2026-11-03T01:14:16Z frontend: moved in_progress -> in_review
- 2026-11-03T01:14:20Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed (r2, 679b63e): every AI-wording site keyed on item.prepared / models.generator_prepared (stepper HELD_* + S.preparedFor, judges rows/group/loading label, rail legend, found-by words, rerun texts, tray flag/attempt, Why 'Model calls', audit headings, banner, guided plain()/legend); real second check keeps 'second AI check'. Test: whole-document observer walk of prepared sample (rail, AI-check panel, Why, audit, flags, charges, tray) with judge-phrase allow-list; fixed waits replaced by condition waits. How verified: mutants (HELD wording back to AI; judges loading state) each fail the walk; full tests/e2e from git archive 679b63e, E2E_REQUIRE_DB=1: 567 passed, 1 skipped, 0 failed. Left: suggestions.js 'tested on the claude-cli backend' accuracy line is allow-listed as an evaluation statement; guided step1 banner still uses health.ai_banner. Surprised: hidden banner kept stale AI text; judge panel painted AI wording while loading.

8aa14e1 test(qa): T-208 r2 the AI translation label is exempt only with a translated entry's quote; label on an English letter fails
679b63e fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
973b542 feat(backend): T-202 r3 D-071 addendum: every line with no certain service date prints the fillable blank 'date of service [__________] (statement dated X)'; letter_check accepts that form and nothing else for such lines
901ad5a docs(architect): T-207 LLM_VS_CODE rows 2 and 3: charge-line service dates are code-only, an allow-list of positive evidence, fillable blank when not certain (D-071)
T204_full_e2e_9b37b9c.log
T204_mutate.py
T204_mutate_input.py
T204_probe_rail.png
T204_probe_rail.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:29.665Z

**tool call — Bash**
````
{
 "command": "git show --stat 679b63e | head -40; cat artifacts/review-evidence/T204_probe_rail.py; ls tests/e2e/test_prepared_first_paint.py"
}
````

### User / tool · 2026-11-03T01:14:29.773Z

**tool result**
````
commit 679b63eb331b72580fb0c571d27c6a9afece2653
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:00:16 2026 -0600

    fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/frontend/app.js                    |   3 +-
 app/frontend/audit.js                  |  12 +--
 app/frontend/guided/review.js          |   2 +-
 app/frontend/guided/step2.js           |   2 +-
 app/frontend/index.html                |   2 +-
 app/frontend/judges.js                 |   6 +-
 app/frontend/stepper.js                |  28 ++++---
 app/frontend/timeline.js               |  18 +++--
 tests/e2e/test_prepared_first_paint.py | 142 +++++++++++++++++++++++++++++++--
 9 files changed, 176 insertions(+), 39 deletions(-)
"""T-204 review probe (staff-engineer). Copy into a git-archive of 9b37b9c as tests/e2e/test_probe_t204.py and run with E2E_REQUIRE_DB=1.
Question: for a PREPARED item held by the second check (quote re-picked, compared, accepted), do the case rail / gate / AI-check panel / export-blocked message
paint 'the AI's summary'?  The card's own test only watches edit-check-hint, edit-compare-prompt and compare-export-note."""
import re
from playwright.sync_api import expect
from tests.e2e import conftest as C
from tests.e2e.conftest import api
from tests.e2e.test_edit_to_check import edited_quote, _row, _accept_something_else   # noqa: F401
from tests.e2e.test_stepper import open_rail

AI = re.compile(r"\bAI\b|\bmodel\b", re.I)


def test_probe_rail_for_prepared_held_item(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    assert next(x for x in C.api("GET", f"/api/cases/{t['tok']}")[1]["entries"] if x["id"] == t["id"])["prepared"] is True
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); row.focus(); page.keyboard.press("a")
    row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    expect(row.get_by_test_id("compare-export-note")).to_be_visible()
    page.reload(); page.get_by_test_id("timeline").wait_for()
    cs = open_rail(page)
    page.wait_for_timeout(1500)
    out = {}
    out["rail_blockers"] = [b.inner_text() for b in cs.get_by_test_id("gate-blocker").all()]
    out["rail_all"] = cs.inner_text()
    jp = page.get_by_test_id("judge-panel")
    if jp.count():
        jp.get_by_test_id("judge-summary").click(); page.wait_for_timeout(1500)
        out["judge_panel"] = jp.inner_text()
    hits = {k: [m for m in re.findall(r"[^.]*\b(?:the AI's|AI's)[^.]*\.", v if isinstance(v, str) else " ".join(v))] for k, v in out.items()}
    for k, v in hits.items():
        print("PROBE", k, "->", v)
    page.screenshot(path="probe_t204_rail.png", full_page=True)
    ai = {k: v for k, v in hits.items() if v}
    assert not ai, ai
tests/e2e/test_prepared_first_paint.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:32.618Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/T204_r2/clean && git archive 679b63e | tar -x -C $S/T204_r2/clean && echo ok; git show 679b63e -- app/frontend | head -400; ls -a .venv/bin/python; ls $S/T204_r2/clean | head -30"
}
````

### User / tool · 2026-11-03T01:14:34.157Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:37.132Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; cat $C/tests/e2e/test_prepared_first_paint.py"
}
````

### User / tool · 2026-11-03T01:14:37.215Z

**tool result**
````
"""T-204 (frontend; D-065, D-069): a prepared answer is never described as the AI's wording, not even for the moment before the server's sentence arrives.
The classic review row paints a fallback sentence for "quote re-picked, second check has no answer" and for "accepted, export blocked"; for an item that is a prepared answer (item.prepared)
the fallback is the prepared twin. The test holds the trace requests, so the first paint is observable, reads it, releases them, and reads the swapped-in server sentence. A MutationObserver
also records every text those nodes ever held, so a flash between two reads cannot hide. Second test: the demo's refused-paste message is rebuilt when the library list loads late.
r2 (staff review): a fourth test walks the whole classic UI for the prepared sample (rail, AI-check panel, Why panels, flags, charges, tray, export gate, audit) with a document-wide observer and fails on any
AI-attributing phrase that is not the real second-check wording. No fixed waits: every wait is on a condition. No new test ids."""
import re
import pytest
from playwright.sync_api import expect
from tests.e2e import conftest as C
from tests.e2e.conftest import api, BASE
from tests.e2e.test_edit_to_check import edited_quote, _row, _accept_something_else   # noqa: F401  (edited_quote is a fixture)
from tests.e2e.test_mvp_finish import NOT_A_RECORDED_CASE

AI = re.compile(r"\bAI\b|\bmodel\b|claude|sonnet|haiku|opus", re.I)
WATCH = """(() => {
  window.__seen = [];
  const SEL = '[data-testid=edit-check-hint],[data-testid=edit-compare-prompt],[data-testid=compare-export-note]';
  const scan = () => document.querySelectorAll(SEL).forEach((n) => { const t = n.textContent; if (t && !window.__seen.includes(t)) window.__seen.push(t); });
  new MutationObserver(scan).observe(document, { subtree: true, childList: true, characterData: true });
  setInterval(scan, 20);
})();"""


def _hold(page):
    held = []
    page.route(re.compile(r"/api/cases/[^/]+(/items/[^/]+)?/trace$"), lambda route: held.append(route))
    return held


def _until(page, cond, what, timeout=15.0):
    """Wait on a condition, polling through the page's own animation frames (no fixed sleep)."""
    import time
    end = time.monotonic() + timeout
    while not cond():
        assert time.monotonic() < end, "timed out waiting for " + what
        page.evaluate("new Promise((r) => requestAnimationFrame(r))")


def _release(page, held, wait_for_one=True):
    """Release every held route. With wait_for_one (the default for the first release of a test) it first waits until the page has actually issued a held request."""
    if wait_for_one:
        _until(page, lambda: bool(held), "a held request")
    while held:
        held.pop().continue_()


def test_a_prepared_item_paints_no_ai_wording_before_or_after_the_server_sentence(page, edited_quote):
    t = edited_quote; _accept_something_else(t)
    assert next(x for x in C.api("GET", f"/api/cases/{t['tok']}")[1]["entries"] if x["id"] == t["id"])["prepared"] is True, "the setup: a prepared answer"
    page.add_init_script(WATCH)
    held = _hold(page)
    try:
        page.reload(); page.get_by_test_id("timeline").wait_for()
        row = _row(page, t["id"])
        hint = row.get_by_test_id("edit-check-hint"); expect(hint).to_be_visible()
        first = hint.inner_text()
        assert not AI.search(first), first                                        # first paint: the server has not answered yet
        assert "prepared wording" in first and "second check has no answer" in first, first
        row.focus(); page.keyboard.press("a")
        prompt = row.get_by_test_id("edit-compare-prompt"); expect(prompt).to_be_visible()
        assert not AI.search(prompt.inner_text()), prompt.inner_text()
        assert "will be blocked" in prompt.inner_text() and "prepared wording" in prompt.inner_text()
        _release(page, held)                                                       # the swap, item sentence
        why = next(s for s in api("GET", f"/api/cases/{t['tok']}/items/{t['id']}/trace")[1]["steps"] if s["id"] == "human")["why"]
        expect(prompt).to_contain_text(why)
        assert why and not AI.search(why) and not AI.search(prompt.inner_text()), prompt.inner_text()
        assert not AI.search(hint.inner_text()), hint.inner_text()
        held = _hold(page)                                                         # hold the case trace again for the blocker sentence
        row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
        note = row.get_by_test_id("compare-export-note"); expect(note).to_be_visible()
        assert not AI.search(note.inner_text()), note.inner_text()                # the blocker sentence has not arrived yet
        assert "second check still has no answer" in note.inner_text()
        _release(page, held)                                                       # the swap, blocker sentence
        expect(note).to_contain_text("Nothing prepared goes into the letter")
        assert not AI.search(note.inner_text()), note.inner_text()
        seen = page.evaluate("window.__seen")
        assert seen, "the observer saw nothing"
        assert not [s for s in seen if AI.search(s)], [s for s in seen if AI.search(s)]   # not for a moment, on any of the three nodes
    finally:
        _release(page, held, wait_for_one=False)


def test_the_refused_paste_message_follows_the_library_when_it_loads_late(page):
    """T-174 r2 F15 / T-204: the message offers 'Choose a library case' only where the library is on the page. If the list arrives after the refusal was painted, the message is built again."""
    held = []
    page.route(re.compile(r"/api/library$"), lambda route: held.append(route))
    try:
        page.goto(BASE); page.get_by_test_id("input-text").wait_for()
        page.get_by_test_id("input-text").fill(NOT_A_RECORDED_CASE); page.get_by_test_id("btn-analyze").click()
        err = page.get_by_test_id("error"); expect(err).to_contain_text("only runs the recorded sample case", timeout=15000)
        assert held, "the library request was held"
        expect(err.get_by_test_id("btn-error-library")).to_have_count(0)
        _release(page, held)
        expect(err.get_by_test_id("btn-error-library")).to_have_text("Choose a library case", timeout=15000)
        expect(err).to_contain_text("sample and library cases")
        expect(err).not_to_contain_text("only runs the recorded sample case,")
        expect(err.get_by_test_id("btn-error-action")).to_have_text("Open the sample")
        err.get_by_test_id("btn-error-library").click()
        expect(page.get_by_test_id("library-list")).to_be_visible()
    finally:
        _release(page, held, wait_for_one=False)


def test_an_unrelated_error_is_not_replaced_when_the_library_loads(page):
    """The rebuild is for the refusal only: a different message (here, no text to read) stays as it is when the list arrives."""
    held = []
    page.route(re.compile(r"/api/library$"), lambda route: held.append(route))
    try:
        page.goto(BASE); page.get_by_test_id("input-text").wait_for()
        page.get_by_test_id("btn-analyze").click()
        err = page.get_by_test_id("error"); expect(err).to_contain_text("There is no text to read")
        # the late event the rebuild would hang on: wait for the library answer and for the page's own zl:switcher event (a listener registered after the app's, so it fires last), then one more frame
        page.evaluate("window.__sw = false; document.addEventListener('zl:switcher', () => { window.__sw = true; })")
        _release(page, held); _until(page, lambda: page.evaluate("window.__sw === true"), "the zl:switcher event")
        page.evaluate("new Promise((r) => requestAnimationFrame(() => requestAnimationFrame(r)))")
        expect(err).to_contain_text("There is no text to read"); expect(err.get_by_test_id("btn-error-library")).to_have_count(0)
    finally:
        _release(page, held, wait_for_one=False)


# ---- the whole classic UI, one prepared case (T-204 r2) ----------------------------------------------------------------------------------------------------------------------------------
# What the observer collects: the text of every node and element that is ever added or changed, every title / aria-label, and (every 40 ms) the page's visible text. Nothing is filtered in the page.
WATCH_ALL = """(() => {
  window.__all = new Set();
  const add = (t) => { if (t) { t = t.replace(/\\s+/g, ' ').trim(); if (t) window.__all.add(t); } };
  const ATTRS = ['title', 'aria-label', 'placeholder', 'alt'];
  const el = (n) => {
    if (n.nodeType === 3) { add(n.data); if (n.parentElement) add(n.parentElement.textContent.length < 700 ? n.parentElement.textContent : ''); return; }
    if (n.nodeType !== 1) return;
    if (n.textContent.length < 700) add(n.textContent);
    ATTRS.forEach((a) => add(n.getAttribute(a)));
    n.querySelectorAll('*').forEach((c) => { ATTRS.forEach((a) => add(c.getAttribute(a))); });
  };
  const scan = () => {
    if (!document.body) return;
    document.body.innerText.split('\\n').forEach(add);
    document.querySelectorAll('[title],[aria-label]').forEach((c) => ATTRS.forEach((a) => add(c.getAttribute(a))));
  };
  const mo = new MutationObserver((ms) => ms.forEach((m) => {
    if (m.type === 'attributes') add(m.target.getAttribute(m.attributeName));
    else if (m.type === 'characterData') el(m.target);
    else { m.addedNodes.forEach(el); if (m.target.nodeType === 1 && m.target.textContent.length < 700) add(m.target.textContent); }
  }));
  mo.observe(document, { subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: ATTRS });
  setInterval(scan, 40);
  window.__scanAll = scan;
})();"""

# The second check is a real AI step (api.md T-177 r3): these phrases are about the judge and may say AI or model. Everything else that is left after they are removed must not name an AI, a model or a model's name.
SECOND_CHECK = [re.compile(p, re.I) for p in (
    r"second (AI )?(check|model)", r"another model", r"AI[- ]?checks?\b", r"AI-checked", r"checked by (AI|[\w.:/-]+)", r"how the AI was checked", r"AI quality checks",
    r"\b(the )?AI (objected|agreed|did not check|could not (check|decide)|did not give|said|found|reads?|read|judge|disagree)", r"\bAI judge", r"no AI model can answer",
    r"not (written )?by an AI model", r"\(not AI\)", r"(model )?claude-haiku-[\w.-]+",       # the judge's own model id, and the "(not AI)" of a code step
    r"independent of the (drafting )?model", r"on the [\w-]+ backend",                                       # the measured accuracy of the pipeline is a statement about the evaluation, not about a case answer
)]
LEAK = re.compile(r"\bAI\b|\bmodel|claude|sonnet|haiku|opus", re.I)


def _leaks(seen):
    out = []
    for t in seen:
        rest = t
        for p in SECOND_CHECK:
            rest = p.sub(" ", rest)
        m = LEAK.search(rest)
        if m:
            out.append(t[:300])
    return sorted(set(out), key=len)[:40]


def _clean_seen(page):
    page.evaluate("window.__scanAll()")
    return page.evaluate("[...window.__all]")


def test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai(page, edited_quote):
    """A prepared sample, an accepted entry whose quote she changed (held by the second check), the whole classic UI walked with a document-wide observer: the case rail, its legend and every step,
    the AI-check panel (collapsed, opened, with the held item in it), a Why panel and Audit, flags, charges, the tray, the export gate. Any phrase that names an AI or a model, other than about the real
    second check, fails. Before this the rail and the panel said 'kept the AI's summary' (staff review T-204 r1)."""
    from tests.e2e.test_stepper import open_rail, open_judges
    t = edited_quote; _accept_something_else(t)
    assert next(x for x in C.api("GET", f"/api/cases/{t['tok']}")[1]["entries"] if x["id"] == t["id"])["prepared"] is True, "the setup: a prepared answer"
    page.add_init_script(WATCH_ALL)
    page.reload(); page.get_by_test_id("timeline").wait_for()
    row = _row(page, t["id"]); row.focus(); page.keyboard.press("a")
    expect(row.get_by_test_id("edit-compare-prompt")).to_be_visible()
    row.get_by_test_id("btn-accept").click(); expect(row).to_have_attribute("data-review", "accepted")
    expect(row.get_by_test_id("compare-export-note")).to_be_visible()
    # a fresh load: the held item is now in the gate, so the rail, the panel and the export message are painted from the server's case
    page.reload(); page.get_by_test_id("timeline").wait_for()
    cs = open_rail(page)
    held_blockers = cs.get_by_test_id("gate-blocker"); expect(held_blockers.first).to_be_visible()
    assert "prepared wording" in cs.inner_text(), cs.inner_text()                  # the rail says it in the prepared words, not just says nothing
    steps = cs.get_by_test_id("case-step")
    for i in range(steps.count()):                                                  # every step of the rail, with its details opened where it has them
        for d in steps.nth(i).locator("details").all():
            if not d.evaluate("n => n.open"):
                d.locator("summary").first.click()
    jp = open_judges(page)
    assert "prepared wording" in jp.inner_text(), jp.inner_text()
    for d in jp.locator("details").all():
        if not d.evaluate("n => n.open"):
            d.locator("summary").first.click()
    from tests.e2e.conftest import reveal
    for tid in ("entry-why", "btn-audit"):                                          # Why this status and Audit on the prepared row
        loc = reveal(row.get_by_test_id(tid))
        if loc.count():
            loc.first.click()
            page.locator("dialog[open], #why-modal:visible, [data-testid=audit-panel]:visible").first.wait_for()
            page.keyboard.press("Escape")
    for panel in ("flags-panel", "charges-panel"):
        p = page.get_by_test_id(panel)
        if p.count():
            btn = reveal(p.get_by_test_id("btn-trace"))
            if btn.count():
                btn.first.click(); page.get_by_test_id("item-stepper").wait_for(); page.keyboard.press("Escape")
    tray_box = page.get_by_test_id("rejected-tray")
    if tray_box.count():
        tray_box.scroll_into_view_if_needed()
    seen = _clean_seen(page)
    assert len(seen) > 50, "the observer saw too little: " + str(len(seen))
    assert page.get_by_test_id("tag-ai-draft").count() == 0, "a prepared case paints no 'draft' (AI) tag"
    assert not _leaks(seen), "\n".join(_leaks(seen))


def test_the_leak_check_itself_catches_the_old_wording():
    """The allow-list only forgives second-check phrases: the r1 sentences, and a model name, still fail it."""
    assert _leaks(["You changed the quote on an accepted entry and kept the AI's summary, and the second AI check has no answer on the new quote."])
    assert _leaks(["The model's attempt (not used): x"]) and _leaks(["Drafted by claude-sonnet-4"]) and _leaks(["Run the AI steps again"])
    assert not _leaks(["The second AI check found this not supported by the quote.", "Prepared by our team (not by an AI model), checked by claude-haiku-4-5.", "How the AI was checked",
                       "You changed the quote on an accepted entry and kept the prepared wording, and the second AI check has no answer on the new quote."])
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:42.031Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; sed -n 1,80p tests/e2e/conftest.py; grep -n \"ZLAYT_MODE\\|ai_banner\\|demo_mode\" -r app/backend/*.py | head -30; cat artifacts/review-evidence/T204_mutate.py | head -40"
}
````

### User / tool · 2026-11-03T01:14:42.128Z

**tool result**
````
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
  Wording: a refused number is shown as the paralegal typed it ('$9,000', not '9000'); the AI-check row for a flag the checks left out says 'Left out of the letter' and 'Nothing to accept here', has no decision line, and its button reads 'Why this status'; the row's More / Less control is named 'More of ...' / 'Less of ...'; library cases are titled in plain words (no 'lib09' or 'case ' in case-name).
T-136 round 2: compare-export-note (D-058: a note on an accepted, compared quote-only edit under the AI's summary whose second AI check has no answer: the server's blocker sentence; holds btn-write-summary 'Write the summary', which opens the edit box; NO rerun button), data-blocker-code (the reason code on a gate-blocker row, e.g. JUDGE_NOT_RUN), btn-gate-write-summary (the same action on that item's JUDGE_NOT_RUN gate-blocker row); the row's entry-state chip of a compared edit reads
  'Compared by you' (not 'Needs review') with entry-reasons 'Compared by you with the quote; the second AI check ...'; edited-note of a quote-only edit reads 'Quote changed by you' and shows the original excerpt.
T-142: conflict-empty (the Conflicts group's empty state: 'No conflicts found among the kinds checked. Other kinds of conflict are not checked.'), conflict-coverage (details in the Conflicts group: open when empty, collapsed when conflicts are listed; words from GET case `checks`
  {conflict_types, labels, not_checked}, a fixed fallback without it) holding conflict-checked-item, conflict-not-checked-item and, in the fallback only, conflict-coverage-note.
T-149 (multi-case, tests/e2e/test_multicase.py): cases-overview (the home section, local mode only), cases-row (one per case, data-token), cases-open (the link that opens it), cases-title, cases-dates (<time> elements), cases-stage, cases-progress-<kind> (a <progress>, kind = entries | flags | amounts)
  with cases-progress-text-<kind> ('2 of 5'), call-out chips cases-chip-needs-review, cases-chip-edits, cases-chip-tray, cases-chip-blocked ('Export blocked (n)') with cases-blocker-reason (one per distinct reason, first two), cases-chip-ready; cases-filter-all / cases-filter-attention / cases-filter-ready (aria-pressed),
  cases-sort (select: attention, recent, least_done, title), cases-count, cases-empty. Detail: case-overview (first block of the timeline), co-progress-<kind> / co-progress-text-<kind>, co-chip-needs-review / co-chip-edits / co-chip-tray / co-chip-blocked / co-chip-ready, co-blocker-reason,
  co-gate-steps (<details>) with co-gate-toggle (its summary), co-gate-verdict, co-gate-step (one per step of GET trace; data-step-id, data-step-status) holding co-gate-word and co-gate-why; btn-all-cases (header: back to the overview).
  Literal forms used by specs: cases-progress-entries, cases-progress-<seq>, cases-progress-text-entries, cases-progress-text-<seq>, co-progress-entries, co-progress-<seq>, co-progress-text-entries, co-progress-text-<seq> (<seq> = flags | amounts).
T-149 round 2 (tests/e2e/test_multicase.py): the overview block is ONE block: it holds todo-strip and checks-card (case-stepper, judge-panel) in its .co-slot; co-gate-* are gone (the Case checks rail is the one place for the steps). need-review-count is now the block's
  needs-review chip (open items only), co-chip-edits, co-chip-tray (quiet), cases-chip-can-export and co-chip-can-export ('Can export \u2014 N not reviewed (they stay out of the letter)', amber), co-chip-ready ('Everything decided', green, only when nothing is undecided), co-chip-blocked; the same chip ids with the cases- prefix on a row.
  Row: cases-decided ('n of N decided'), cases-next (the one call-out of a not-analyzed or failed row), cases-search (title), cases-list (data-ready="true" after the first settled paint), cases-loading, cases-load-error with cases-retry, cases-open-error, filter cases-filter-ready is now 'Ready to send'.
  Detail: case-heading (the h2, tabindex -1, focused when a case opens from the list, aria-label names the case), do-first with btn-do-first (one line from next_action {item_id, kind, reason}), btn-rename-case, case-rename-input, btn-save-rename, case-rename-error, todo-more (phone: the jump list behind one line),
  data-do-first (attribute on the overview block while the line is shown), LiveRerun and JudgeNotRun (stubs that make GET case say rerun_available true), rerun-unavailable (the sentence that replaces the rerun button when no item says rerun_available), input-title (the case name field beside Analyze).
T-151 (tests/e2e/test_conflict_skipped.py): conflict-skipped (box in the Conflicts group listing checks that did not run), conflict-skipped-item (data-skip-type = the check type, data-reason-code = the server's reason code, never shown as text), conflict-skipped-records ('Records 2, 4 and 7 were not read.'),
  conflict-notes / conflict-note (info lines from checks.notes, not flag cards), conflict-not-checked-line (always visible: left versus right, loss of consciousness history, any other kind are not checked). A skipped type is not in conflict-checked-item.
T-136 r3 (tests/e2e/test_held_quote_gate.py): btn-write-summary-case ('Write the summary' on the case-level places: the 'Ready to export?' and 'Second AI check' steps of the case rail and the 'How the AI was checked' rows; opens the entry's summary box like the blocker row's btn-gate-write-summary). A held re-picked quote offers btn-rerun-judge only until a rerun gave no answer (the blocker's rerun_no_answer).
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
  T-060 round 5 / T-131: entry-reasons (the row's one-line reason: the backend's plain `why` sentence, never a code; also title = the full text), need-review-count (a <p> in todo-strip: 'N items need review', the SAME number as the header '... . N items need review' and the Timeline's review-counts warn chip; it falls on dismiss),
app/backend/api.py:84:    return os.environ.get("ZLAYT_MODE") == "local"
app/backend/api.py:116:        raise RuntimeError("ZLAYT_MODE=local exposes the case list and every case token: HOST must be 127.0.0.1, ::1 or localhost")
app/backend/api.py:127:    def demo_mode():
app/backend/api.py:266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
app/backend/api.py:268:                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
app/backend/api.py:308:        if demo_mode():            # the public demo only runs recorded text and an extracted PDF is never that: refuse before reading or parsing a byte
app/backend/api.py:309:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:352:        if demo_mode() and digest(text) not in allowed_hashes():
app/backend/api.py:353:            raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:361:                                 source="sample" if sample else "paste", backend=backend(), demo_mode=int(demo_mode()),
app/backend/api.py:377:                    "demo_mode": demo_mode(), "record_count": len(recs), "split_method": ing["split_method"], "records": recs,
app/backend/api.py:390:            v = present.case_view(c, token, backend=backend(), models=present.models_for(c, token, config_models()), demo_mode=demo_mode())
app/backend/api.py:444:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:445:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:446:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:472:            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py:473:                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py:474:            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py:632:                                "demo_mode": demo_mode(), "prompt_versions": sorted({x["prompt_version"] for x in calls if x["prompt_version"] and not AU.is_prepared(x.get("recorded_from"))}),
app/backend/api.py:640:        """D-042: the validation ladder for one item as ordered steps. Metadata only unless ZLAYT_MODE=local (same split as /audit)."""
app/backend/api.py:674:            return present.audit_view(c, token, full=os.environ.get("ZLAYT_MODE") == "local")
app/backend/api.py:700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
app/backend/dismissal_patterns.py:5:ZLAYT_MODE=local the history is this case only, so a public/demo token never sees another case's dismissals.
app/backend/limits.py:2:public build makes no model call). Two caps, public mode only (ZLAYT_MODE != local); local/dev stays unlimited:
app/backend/present.py:483:def case_view(conn, case_id, *, backend, models, demo_mode):
app/backend/present.py:518:    return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
app/backend/present.py:559:    """full=True (ZLAYT_MODE=local only) adds prompt, response and edit text; otherwise metadata only (model, backend, prompt hash, verdict, latency)."""
app/backend/trace.py:7:Visibility is the /audit split (D-020/D-036): full=False (public/demo) returns metadata only; full=True (ZLAYT_MODE=local) adds the model's raw
app/backend/store.py:68:    """T-157 r2: the one definition of "live", used by api.demo_mode (its negation) and by rerun_available. ENABLE_LIVE=1 and something to call: the claude CLI, or an API key.
import sys, pathlib
root, which = pathlib.Path(sys.argv[1]), sys.argv[2]
p = root / "app/frontend/review.js"; s = p.read_text()
muts = {
 "M1_isPrepared_false": ('const isPrepared = (item) => { const c', 'const isPrepared = (item) => false && { const c'),
 "M2_heldText_ai": ('(isPrepared(item) ? PREPARED_HELD : AI_HELD)', 'AI_HELD'),
 "M3_accepted_ai": ('isPrepared(item) ? PREPARED_ACCEPTED_HELD : ACCEPTED_HELD', 'ACCEPTED_HELD'),
}
a, b = muts[which]
assert s.count(a) == 1, (which, s.count(a))
if which == "M1_isPrepared_false":
    a = 'const isPrepared = (item) => { const c = ZL.state.get().case, '; 
    i = s.index('const isPrepared'); j = s.index('\n', i)
    s = s[:i] + 'const isPrepared = (item) => false;' + s[j:]
else:
    s = s.replace(a, b)
p.write_text(s)
print(which, "applied;", "AI_HELD-only count:", s.count("AI_HELD"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:46.632Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; grep -n \"BASE\\s*=\\|E2E_\\|subprocess\\|Popen\\|environ\" $C/tests/e2e/conftest.py | head -40; ls $C/tests/e2e/*.py | wc -l; ls $C/tests/e2e | grep -i \"guided\\|prepared\"; ls $C/.venv 2>&1 | head -2"
}
````

### User / tool · 2026-11-03T01:14:46.757Z

**tool result**
````
106:SERVER = os.environ.get("E2E_BASE_URL", "http://localhost:7860")      # the app's root: the guided UI (D-068) is served here, and every /api call goes here
107:BASE = SERVER + "/classic"                                              # D-068: the old screen moved to /classic; the whole classic suite navigates from BASE, API calls use SERVER
118:    which used to skip silently). When neither E2E_BASE_URL nor ZLAYT_DB is set, start a private app instance on a free loopback port (fixture backend, curated set, ZLAYT_MODE=local, a temp
119:    ZLAYT_DB) and point BASE at it, so the file the specs write is the file the server reads. It never touches the shared app on :7860. Set E2E_BASE_URL to test a server you started (then
120:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
122:    if os.environ.get("E2E_BASE_URL") or os.environ.get("ZLAYT_DB"):
124:    import atexit, shutil, socket, subprocess, sys, tempfile, time
127:    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", ZLAYT_MODE="local", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "e2e.sqlite3"))
130:    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
156:    os.environ["ZLAYT_DB"] = env["ZLAYT_DB"]; SERVER = base; BASE = base + "/classic"
166:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
168:    path = os.environ.get("ZLAYT_DB")
170:        msg = "needs ZLAYT_DB (the SQLite file of the server under test); a plain `pytest tests/e2e` starts its own server and sets it, a run against E2E_BASE_URL does not"
171:        if os.environ.get("E2E_REQUIRE_DB") == "1":
      45
guided
test_prepared_first_paint.py
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T204_r2/clean/.venv: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:14:51.144Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cp artifacts/review-evidence/T204_probe_rail.py $C/tests/e2e/test_probe_t204.py; cd $C && E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_prepared_first_paint.py tests/e2e/test_probe_t204.py -q -s -p no:cacheprovider 2>&1 | tail -30",
 "timeout": 400000
}
````

### User / tool · 2026-11-03T01:15:04.419Z

**tool result**
````
.....PROBE rail_blockers -> []
PROBE rail_all -> []
PROBE judge_panel -> []
.
6 passed in 12.22s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:07.992Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.. 2>/dev/null; cd /Users/arsis/zlayt-pm-project && ls tests/e2e/guided | head -30; sed -n 1,60p tests/e2e/guided/conftest.py 2>/dev/null; ls app/frontend/guided; grep -n \"ai_banner\\|PREPARED_BANNER\\|AI_BANNER\" -r app/backend app/frontend | grep -v \"^app/frontend/.*\\.map\" | head -20"
}
````

### User / tool · 2026-11-03T01:15:08.105Z

**tool result**
````
__init__.py
__pycache__
_helpers.py
test_golden_path.py
test_home.py
test_round2.py
test_round3.py
test_shell_smoke.py
test_step1.py
test_step2.py
test_step3.py
test_step4.py
test_t203.py
test_t205.py
test_t206.py
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
app/backend/api.py:38:AI_BANNER = "Summaries and flags are drafted by AI and checked by code; you decide every item"
app/backend/api.py:39:PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item"      # D-065
app/backend/api.py:268:                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}
app/frontend/app.js:5:  const PREPARED_BANNER = "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item";   // the same words as the server's (D-065)
app/frontend/app.js:11:    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = ai.hidden ? "" : s.case && s.case.models && s.case.models.generator_prepared ? PREPARED_BANNER : (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";   // T-204 r2: the case says whose answers they are
app/frontend/guided/review.js:70:  R.aiNote = () => { const p = G.provenance(), hl = G.store.health; return p.kind === "live" && hl && hl.ai_banner ? hl.ai_banner : p.note; };
app/frontend/mock.js:147:        ai_banner: "Summaries and flags are drafted by AI and checked by code; you decide every item", sample_available: true });
app/frontend/guided/step1.js:272:        hl.ai_banner ? h("p", { class: "muted ai-line", "data-testid": "ai-banner" }, hl.ai_banner) : null,
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:11.314Z

**tool call — Bash**
````
{
 "command": "sed -n 120,135p app/backend/api.py; sed -n 255,270p app/backend/api.py; sed -n 262,278p app/frontend/guided/step1.js; sed -n 55,80p app/frontend/guided/review.js; grep -n \"tested on the claude-cli\" -r app/frontend | head"
}
````

### User / tool · 2026-11-03T01:15:11.430Z

**tool result**
````
    def backend():
        from app.llm import provider
        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says

    def live_enabled():
        return store.live_enabled()          # T-157 r2: one definition, shared with rerun_available

    def demo_mode():
        return not live_enabled()

    def answers():
        """D-065: where the answers on screen come from: `live` (a model, now), `recorded` (a replay of real model answers) or `prepared` (hand-checked by the team, curated set)."""
        if live_enabled():
            return "live"
        from app.llm.backends import fixture
        return "prepared" if backend() == "fixture" and fixture.answer_source() == "prepared" else "recorded"
            b = json.loads(raw)
        except ValueError:
            raise ApiError(400, "bad_request", "Request body is not valid JSON.") from None
        if not isinstance(b, dict):
            raise ApiError(400, "bad_request", "Request body must be a JSON object.")
        return _clean_strings(b)

    # -------------------------------------------------- routes
    @app.get("/api/health")
    def health():
        ans = answers()
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
                "retention_hours": DB.RETENTION_SECONDS // 3600, "ai_banner": PREPARED_BANNER if ans == "prepared" else AI_BANNER, "sample_available": (GOLDEN / "sample.txt").exists()}

    @app.get("/api/cases")
    /* ---- done ---- */
    function drawDone() {
      ctx.layout("page"); ctx.setStepStatus(1, "Done", "done");
      const n = counts(), hl = G.store.health || {}, [label, href] = nextTarget();
      const msg = `${plural(n.lines, "timeline item")} and ${n.bills ? plural(n.bills, "bill amount") : "no bill amounts"} ${n.lines + n.bills === 1 ? "is" : "are"} ready for you to check.`;
      const go = h("a", { class: "btn primary lg sbar-main", href, "data-testid": "btn-next-step", "data-autofocus": "" }, label);
      const b = G.sbar("Step 1 is done.", go);
      const prep = (c.models && c.models.generator_prepared) || prepared();
      put(b, heading("Records added"), h("div", { class: "panel", "data-testid": "draft-done" },
        h("div", { class: "done-hero" }, h("div", { class: "big-check", "aria-hidden": "true" }, "✓"), h("div", {}, h("h2", { "data-testid": "done-title" }, "All set."), h("p", { "data-testid": "done-counts" }, msg))),
        hl.ai_banner ? h("p", { class: "muted ai-line", "data-testid": "ai-banner" }, hl.ai_banner) : null,
        prep ? h("p", { class: "prov" }, h("span", { class: "tag prep", title: G.provenance().note, "data-testid": "prepared-badge" }, "Prepared by our team"), " ", G.provenance().note) : null),
        h("div", { class: "panel" }, h("h2", {}, `${plural((c.records || []).length, "record")} added`), recList(), h("p", { class: "muted after-list" }, "To add more records, start a new case. ", h("a", { href: G.url.new() }, "Start a new case"))));
      focusTitle();
    }

    /* ---- stopped ---- */
  /* ---------- dates and money (code only) ---------- */
  const MONTHS = ["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"];
  R.longDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1]} ${+m[3]}, ${m[1]}` : ""; };
  R.shortDate = (iso) => { const m = /^(\d{4})-(\d{2})-(\d{2})/.exec(iso || ""); return m ? `${MONTHS[+m[2] - 1].slice(0, 3)} ${+m[3]}, ${m[1]}` : "No date"; };
  R.money = (cents) => (cents < 0 ? "-" : "") + "$" + (Math.abs(cents) / 100).toLocaleString("en-US", { minimumFractionDigits: 2, maximumFractionDigits: 2 });

  /* ---------- provenance tags (D-065): a prepared answer says "Prepared answer", never "AI" ---------- */
  R.tagFor = function (item) {
    const p = G.provenance();
    if (item.entered_by_reviewer || (item.edited && item.edited.summary)) return { cls: "you", text: "Written by you" };
    if (item.prepared) return { cls: "prep", text: "Prepared answer", title: p.note };
    if (item.ai_drafted === false || item.origin === "code") return null;
    return { cls: "ai", text: "AI draft", title: p.kind === "live" ? p.note : "Drafted by an AI. " + p.note };
  };
  // G.provenance() follows the open case: a case whose lines an AI wrote says so, never "not written by an AI model" (T-181 r2)
  R.aiNote = () => { const p = G.provenance(), hl = G.store.health; return p.kind === "live" && hl && hl.ai_banner ? hl.ai_banner : p.note; };

  /* ---------- the second check disputed this item (D-066; the same rule as review.judge_dispute) ---------- */
  const DISPUTE = { partially: "A second AI check found this only partly supported by the highlighted words.", unsupported: "A second AI check found this not supported by the highlighted words.",
    disagrees: "A second AI check disagreed with the first result for this item." };
  R.dispute = function (item) {
    const j = item && item.ladder && item.ladder.judge, vv = j && j.verdict, v = vv === "disagree" ? "disagrees" : vv;
    if (DISPUTE[v]) return v;
    const rs = (item && (item.state_reasons || item.reasons)) || [];
    return rs.includes("JUDGE_PARTIAL") ? "partially" : rs.includes("JUDGE_UNSUPPORTED") ? "unsupported" : rs.includes("JUDGE_DISAGREES") ? "disagrees" : null;
  };
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:19.535Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; sed -n 1,80p $C/tests/e2e/guided/_helpers.py; sed -n 1,50p $C/tests/e2e/guided/test_golden_path.py"
}
````

### User / tool · 2026-11-03T01:15:19.644Z

**tool result**
````
"""Shared helpers for the guided specs of Builder A (home, step 1, step 4). T-181 (D-068). Not a test module."""
import json
import os
import re
import time
import uuid
import tests.e2e.conftest as C

SHOTS = os.path.join(C.ROOT, "artifacts", "screenshots", "guided")


def uid():
    return uuid.uuid4().hex[:6]


def api(method, path, body=None):
    return C.api(method, path, body)


def make_case(title, run=True, decide=False, sample=True):
    """A sample case over the API: ingested, or drafted (ready), or drafted with every item accepted."""
    st, c = api("POST", "/api/cases", {"sample": True, "title": title}); assert st == 201, c
    tok = c["token"]
    if run:
        assert api("POST", f"/api/cases/{tok}/run", {"confirm_rerun": False})[0] == 202
        for _ in range(240):
            s = api("GET", f"/api/cases/{tok}/status")[1]
            if s["status"] in ("ready", "failed"):
                break
            time.sleep(.5)
        assert s["status"] == "ready", s
    if decide:
        decide_all(tok)
    return tok


def decide_all(tok, action="accept"):
    """Step 2 and 3 are another builder's: answer every item over the API (accept)."""
    c = api("GET", f"/api/cases/{tok}")[1]
    for i in c["entries"] + c["undated_entries"] + c["flags"] + c["amounts"]:
        st, r = api("POST", f"/api/cases/{tok}/items/{i['id']}/review", {"action": action})
        assert st == 200, (i["id"], st, r)


def golden_letter():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    return txt.split("=== LETTER_TEXT (block 1: paste into letter) ===\n")[1].split("=== INTERNAL_NOTES_TEXT")[0].rstrip("\n")


def golden_notes():
    txt = open(os.path.join(C.SAMPLE_PATH, "sample.export.expected.txt")).read()
    notes = txt.split("=== INTERNAL_NOTES_TEXT (block 2: do not send) ===\n")[1].rstrip("\n")
    from app.backend import export      # D-069: the golden predates the prepared disclosure line the curated demo now prints
    return notes.replace(export.AI_LINE.split("{n}")[0], export.AI_LINE_PREPARED.split("{n}")[0])


def browser(pw, w, h, scheme="light", **kw):
    b = pw.chromium.launch()
    ctx = b.new_context(viewport={"width": w, "height": h}, color_scheme=scheme, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True, **kw)
    return b, ctx.new_page()


def shot(page, name, w):
    os.makedirs(SHOTS, exist_ok=True)
    page.screenshot(path=os.path.join(SHOTS, f"{name}-{w}.png"))


def in_view(page, loc):
    """True when the element's whole box is inside the viewport with the page scrolled to the top (nothing to scroll to reach it)."""
    page.evaluate("window.scrollTo(0, 0)")
    b = loc.bounding_box(); vh = page.viewport_size["height"]; vw = page.viewport_size["width"]
    return bool(b) and b["y"] >= 0 and b["y"] + b["height"] <= vh and b["x"] >= 0 and b["x"] + b["width"] <= vw


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth")


def go(page, path="/"):
    page.goto(C.SERVER + path)
"""T-181 (D-068) README golden path, smoke: in demo mode a first-time visitor opens `/`, clicks Open the sample case, drafts it and lands on Step 2 with an entry on screen.
Public/demo mode has no case list (GET /api/cases is 404 by design, spec 3.3), so the browser starts with an empty list and Home offers the sample. The route stub below makes the shared
local-mode test server answer like the public one. Step 2 itself is Builder B's page: this test needs it to show the entry text."""
import re
from playwright.sync_api import expect
import tests.e2e.conftest as C
from tests.e2e.guided._helpers import api, browser, jbody, err
from tests.e2e.guided.test_shell_smoke import watch


def test_demo_sample_reachable_from_root(pw):
    br, page = browser(pw, 1440, 900)
    tok = None
    try:
        page.route("**/api/cases", lambda r: jbody(r, 404, err("not_found", "Not found.")) if r.request.method == "GET" else r.continue_())
        page.goto(C.SERVER + "/")
        page.get_by_test_id("btn-sample-case").click(timeout=10000)               # Open the sample case
        expect(page).to_have_url(re.compile(r"/case/[^/]+/records$"), timeout=10000)
        tok = page.url.split("/case/")[1].split("/")[0]
        page.get_by_test_id("btn-draft").click()                                   # Draft the timeline (instant on the prepared set)
        expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=15000)
        page.get_by_test_id("btn-next-step").click()                               # Go to step 2: Check the timeline
        expect(page).to_have_url(re.compile(r"/case/[^/]+/timeline$"), timeout=10000)
        expect(page.get_by_test_id("page-title")).to_have_text("Check the timeline")
        first = api("GET", f"/api/cases/{tok}")[1]["entries"][0]["summary"][:30]
        expect(page.locator("body")).to_contain_text(first, timeout=10000)          # at least one entry is on screen
    finally:
        if tok:
            api("DELETE", f"/api/cases/{tok}")
        br.close()
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:22.096Z

**tool call — Bash**
````
{
 "command": "grep -n \"url = \\|url\\.\\w* *=\\|records\\b.*timeline\\|/case/\" app/frontend/guided/core.js | head -20; grep -n \"ZLAYT_CLASSIC\\|/classic\" app/backend/api.py | head"
}
````

### User / tool · 2026-11-03T01:15:22.193Z

**tool result**
````
6:  G.pages = {};           // G.pages.home | new | records | timeline | bills | letter = async (ctx) => optional cleanup fn   (see app.js, "page contract")
7:  G.LABELS = [["Add records", "Records"], ["Check the timeline", "Timeline"], ["Check the bills", "Bills"], ["Get your letter", "Letter"]];
26:  G.url = {
28:    records: (t) => "/case/" + enc(t) + "/records",
29:    timeline: (t, item) => "/case/" + enc(t) + "/timeline" + (item ? "?item=" + enc(item) : ""),
30:    bills: (t, item) => "/case/" + enc(t) + "/bills" + (item ? "?item=" + enc(item) : ""),
31:    letter: (t) => "/case/" + enc(t) + "/letter",
32:    step: (t, n, item) => [null, G.url.records, G.url.timeline, G.url.bills, G.url.letter][n](t, item),
682:        if (guided / "index.html").is_file():                                           # D-068: the guided app is the front door; the old screen stays reachable at /classic
687:                /api and /classic never fall through to it (an unknown /api path must stay a JSON 404)."""
700:                """T-177 r3 / D-068: /classic is a developer screen. It answers in local mode (ZLAYT_MODE=local) or with ZLAYT_CLASSIC=1; in demo or public mode it sends the visitor to the guided UI at /."""
701:                return local_mode() or os.environ.get("ZLAYT_CLASSIC") == "1"
709:            app.add_api_route("/classic", lambda: RedirectResponse("/classic/" if classic_open() else "/"), include_in_schema=False)       # the mount only answers /classic/ ; /classic would fall to the guided mount
710:            app.mount("/classic", ClassicFiles(directory=str(sd), html=True), name="classic")
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:40.631Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_probe_guided.py <<'EOF'\n\"\"\"T-204 r2 probe (staff-engineer). Copy into a git-archive of 679b63e as tests/e2e/test_probe_t204_r2.py; run with E2E_REQUIRE_DB=1 -s.\nWalks the GUIDED UI (home, step1 done, step2 timeline, step3 bills, step4 letter) and the CLASSIC UI for the prepared sample, with a held (quote re-picked) item in the case.\nCollects every text/title/aria-label ever painted (document-wide MutationObserver + 30 ms scan of innerText), applies NO allow-list, prints each line with an AI/model/vendor word.\"\"\"\nimport re, time\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.conftest import api\nfrom tests.e2e.test_edit_to_check import edited_quote, _row, _accept_something_else   # noqa: F401\nfrom tests.e2e.guided._helpers import browser\n\nLEAK = re.compile(r\"\\bAI\\b|\\bA\\.I\\.|\\bmodels?\\b|claude|sonnet|haiku|opus|\\bLLM\\b|\\bGPT\\b|anthropic|machine|automat\", re.I)\nOBS = \"\"\"(() => {\n  window.__all = new Set();\n  const add = (t) => { if (t) { t = t.replace(/\\\\s+/g, ' ').trim(); if (t) window.__all.add(t); } };\n  const A = ['title','aria-label','placeholder','alt','aria-description'];\n  const attrs = (n) => { if (n.nodeType === 1) { A.forEach(a => add(n.getAttribute(a))); n.querySelectorAll('*').forEach(c => A.forEach(a => add(c.getAttribute(a)))); } };\n  const scan = () => { if (!document.body) return; document.body.innerText.split('\\\\n').forEach(add); document.querySelectorAll('[title],[aria-label]').forEach(c => A.forEach(a => add(c.getAttribute(a))));\n     document.querySelectorAll('details:not([open])').forEach(d => d.querySelectorAll('*').forEach(c => { if (c.children.length === 0) add(c.textContent); })); };\n  new MutationObserver(ms => ms.forEach(m => { if (m.type === 'attributes') add(m.target.getAttribute(m.attributeName)); else if (m.type === 'characterData') { add(m.target.data); }\n     else m.addedNodes.forEach(n => { if (n.nodeType === 3) add(n.data); else if (n.nodeType === 1) { n.querySelectorAll('*').forEach(c => { if (c.children.length === 0) add(c.textContent); }); if (n.children.length === 0) add(n.textContent); attrs(n); } }); }))\n   .observe(document, {subtree: true, childList: true, characterData: true, attributes: true, attributeFilter: A});\n  setInterval(scan, 30); window.__scanAll = scan;\n})();\"\"\"\n\n\ndef _open_all(page):\n    page.evaluate(\"document.querySelectorAll('details').forEach(d => d.open = true)\")\n\n\ndef _click_all(page, sel, limit=8):\n    for _ in range(2):\n        loc = page.locator(sel)\n        for i in range(min(loc.count(), limit)):\n            try:\n                if loc.nth(i).is_visible():\n                    loc.nth(i).click(timeout=1500); page.wait_for_timeout(250); page.keyboard.press(\"Escape\")\n            except Exception:\n                pass\n\n\ndef _report(label, page):\n    page.evaluate(\"window.__scanAll()\")\n    seen = sorted(page.evaluate(\"[...window.__all]\"), key=len)\n    hits = [t[:260] for t in seen if LEAK.search(t)]\n    print(f\"\\n=== {label}: {len(seen)} texts seen, {len(hits)} with AI/model words\")\n    for t in hits:\n        print(\"   LEAK>\", t)\n    return hits\n\n\ndef test_probe_guided_and_classic(pw, edited_quote):\n    t = edited_quote; _accept_something_else(t)\n    c = api(\"GET\", f\"/api/cases/{t['tok']}\")[1]\n    assert next(x for x in c[\"entries\"] if x[\"id\"] == t[\"id\"])[\"prepared\"] is True\n    h = api(\"GET\", \"/api/health\")[1]\n    print(\"HEALTH answers=%s demo_mode=%s local_mode=%s ai_banner=%r\" % (h[\"answers\"], h[\"demo_mode\"], h[\"local_mode\"], h[\"ai_banner\"]))\n    print(\"CASE models:\", c.get(\"models\"))\n    br, page = browser(pw, 1440, 900)\n    try:\n        page.add_init_script(OBS)\n        # ---------------- guided\n        page.goto(C.SERVER + \"/\"); page.wait_for_timeout(1200); _open_all(page)\n        # accept the held item in the guided flow via API so step 4 shows its blocker\n        r = api(\"POST\", f\"/api/cases/{t['tok']}/items/{t['id']}/review\", {\"action\": \"accept\"}); print(\"accept held:\", r[0])\n        for name, path in ((\"g_records\", \"records\"), (\"g_timeline\", \"timeline\"), (\"g_bills\", \"bills\"), (\"g_letter\", \"letter\")):\n            page.goto(C.SERVER + f\"/case/{t['tok']}/{path}\"); page.wait_for_timeout(1800); _open_all(page)\n            _click_all(page, \"button:has-text('Why'), button:has-text('How'), button:has-text('check'), summary\")\n            _open_all(page); page.wait_for_timeout(300)\n        # a fresh sample case through the draft button (step 1 done screen, with the server's banner)\n        page.goto(C.SERVER + \"/\"); page.get_by_test_id(\"btn-sample-case\").click(timeout=10000)\n        page.wait_for_url(re.compile(r\"/records$\"), timeout=10000)\n        page.get_by_test_id(\"btn-draft\").click(); expect(page.get_by_test_id(\"draft-done\")).to_be_visible(timeout=20000)\n        print(\"STEP1 done banner:\", page.get_by_test_id(\"ai-banner\").inner_text() if page.get_by_test_id(\"ai-banner\").count() else None)\n        print(\"STEP1 prov:\", page.locator(\"p.prov\").inner_text() if page.locator(\"p.prov\").count() else None)\n        _open_all(page); page.wait_for_timeout(500)\n        g = _report(\"GUIDED\", page)\n        # ---------------- classic\n        page.goto(C.BASE); page.wait_for_timeout(1500); page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n        _open_all(page)\n        _click_all(page, \"[data-testid=btn-trace], [data-testid=entry-why], [data-testid=btn-audit], summary\", 12)\n        _open_all(page); page.wait_for_timeout(500)\n        k = _report(\"CLASSIC\", page)\n        out = {\"guided\": g, \"classic\": k}\n        import json, os\n        open(os.path.join(os.environ.get(\"PROBE_OUT\", \".\"), \"probe_t204_r2_out.json\"), \"w\").write(json.dumps(out, indent=1))\n    finally:\n        br.close()\nEOF\necho done"
}
````

### User / tool · 2026-11-03T01:15:40.717Z

**tool result**
````
done
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:15:44.734Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cp artifacts/review-evidence/T204_r2_probe_guided.py $C/tests/e2e/test_probe_t204_r2.py; grep -n \"def pw\\|def page\" $C/tests/e2e/conftest.py | head; cd $C && PROBE_OUT=$S/T204_r2 E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_probe_t204_r2.py -q -s -p no:cacheprovider 2>&1 | tail -80",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:16:09.610Z

**tool result**
````
253:def pw():
259:def page(pw):
HEALTH answers=prepared demo_mode=True local_mode=True ai_banner='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item'
CASE models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
accept held: 200
F
=================================== FAILURES ===================================
________________________ test_probe_guided_and_classic _________________________

pw = <playwright._impl._playwright.Playwright object at 0x109a3cda0>
edited_quote = {'tok': 'J10s0BiOIq7WMAJ-8op3RQ', 'id': 'e2', 'before': (0, 23, 4, 0), 'orig': 'Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'}

    def test_probe_guided_and_classic(pw, edited_quote):
        t = edited_quote; _accept_something_else(t)
        c = api("GET", f"/api/cases/{t['tok']}")[1]
        assert next(x for x in c["entries"] if x["id"] == t["id"])["prepared"] is True
        h = api("GET", "/api/health")[1]
        print("HEALTH answers=%s demo_mode=%s local_mode=%s ai_banner=%r" % (h["answers"], h["demo_mode"], h["local_mode"], h["ai_banner"]))
        print("CASE models:", c.get("models"))
        br, page = browser(pw, 1440, 900)
        try:
            page.add_init_script(OBS)
            # ---------------- guided
            page.goto(C.SERVER + "/"); page.wait_for_timeout(1200); _open_all(page)
            # accept the held item in the guided flow via API so step 4 shows its blocker
            r = api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"}); print("accept held:", r[0])
            for name, path in (("g_records", "records"), ("g_timeline", "timeline"), ("g_bills", "bills"), ("g_letter", "letter")):
                page.goto(C.SERVER + f"/case/{t['tok']}/{path}"); page.wait_for_timeout(1800); _open_all(page)
                _click_all(page, "button:has-text('Why'), button:has-text('How'), button:has-text('check'), summary")
                _open_all(page); page.wait_for_timeout(300)
            # a fresh sample case through the draft button (step 1 done screen, with the server's banner)
>           page.goto(C.SERVER + "/"); page.get_by_test_id("btn-sample-case").click(timeout=10000)
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/e2e/test_probe_t204_r2.py:70: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py:11021: in click
    self._sync(
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py:174: in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py:598: in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:78: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x10975cce0>
cb = <function Channel.send.<locals>.<lambda> at 0x109ed3420>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        parsed_st = _attach_api_call_information(
            getattr(task, "__pw_stack__", None) or _capture_stack_trace(),
            is_internal,
            title,
        )
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.click: Timeout 10000ms exceeded.
E           Call log:
E             - waiting for get_by_test_id("btn-sample-case")

/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: TimeoutError
=========================== short test summary info ============================
FAILED tests/e2e/test_probe_t204_r2.py::test_probe_guided_and_classic - playw...
1 failed in 23.89s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:16:16.107Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\npython3 - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_probe_guided.py\"\ns=open(p).read()\ns=s.replace('''        page.goto(C.SERVER + \"/\"); page.get_by_test_id(\"btn-sample-case\").click(timeout=10000)''','''        from tests.e2e.guided._helpers import jbody, err\n        page.route(\"**/api/cases\", lambda r: jbody(r, 404, err(\"not_found\", \"Not found.\")) if r.request.method == \"GET\" else r.continue_())   # as the public demo answers: no case list\n        page.goto(C.SERVER + \"/\"); page.get_by_test_id(\"btn-sample-case\").click(timeout=10000)''')\ns=s.replace('''        page.get_by_test_id(\"btn-draft\").click(); expect''','''        page.unroute(\"**/api/cases\"); page.get_by_test_id(\"btn-draft\").click(); expect''')\nopen(p,\"w\").write(s)\nEOF\ncp artifacts/review-evidence/T204_r2_probe_guided.py $C/tests/e2e/test_probe_t204_r2.py; cd $C && PROBE_OUT=$S/T204_r2 E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_probe_t204_r2.py -q -s -p no:cacheprovider 2>&1 | tail -60",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:16:41.172Z

**tool result**
````
        print("HEALTH answers=%s demo_mode=%s local_mode=%s ai_banner=%r" % (h["answers"], h["demo_mode"], h["local_mode"], h["ai_banner"]))
        print("CASE models:", c.get("models"))
        br, page = browser(pw, 1440, 900)
        try:
            page.add_init_script(OBS)
            # ---------------- guided
            page.goto(C.SERVER + "/"); page.wait_for_timeout(1200); _open_all(page)
            # accept the held item in the guided flow via API so step 4 shows its blocker
            r = api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"}); print("accept held:", r[0])
            for name, path in (("g_records", "records"), ("g_timeline", "timeline"), ("g_bills", "bills"), ("g_letter", "letter")):
                page.goto(C.SERVER + f"/case/{t['tok']}/{path}"); page.wait_for_timeout(1800); _open_all(page)
                _click_all(page, "button:has-text('Why'), button:has-text('How'), button:has-text('check'), summary")
                _open_all(page); page.wait_for_timeout(300)
            # a fresh sample case through the draft button (step 1 done screen, with the server's banner)
            from tests.e2e.guided._helpers import jbody, err
            page.route("**/api/cases", lambda r: jbody(r, 404, err("not_found", "Not found.")) if r.request.method == "GET" else r.continue_())   # as the public demo answers: no case list
>           page.goto(C.SERVER + "/"); page.get_by_test_id("btn-sample-case").click(timeout=10000)
                                       ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/e2e/test_probe_t204_r2.py:72: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py:11021: in click
    self._sync(
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py:174: in click
    return await self._frame._click(self._selector, strict=True, **params)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py:598: in _click
    await self._channel.send("click", self._timeout, locals_to_params(locals()))
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:78: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x10956bd10>
cb = <function Channel.send.<locals>.<lambda> at 0x10fb67b00>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        parsed_st = _attach_api_call_information(
            getattr(task, "__pw_stack__", None) or _capture_stack_trace(),
            is_internal,
            title,
        )
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.click: Timeout 10000ms exceeded.
E           Call log:
E             - waiting for get_by_test_id("btn-sample-case")

/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: TimeoutError
=========================== short test summary info ============================
FAILED tests/e2e/test_probe_t204_r2.py::test_probe_guided_and_classic - playw...
1 failed in 24.03s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:16:47.612Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\npython3 - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_probe_guided.py\"\ns=open(p).read()\ni=s.index(\"        from tests.e2e.guided._helpers import jbody, err\")\nj=s.index(\"        page.unroute\")\ns=s[:i]+'''        st, nc = api(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"probe step1\"}); assert st == 201\n        page.goto(C.SERVER + f\"/case/{nc['token']}/records\"); page.wait_for_timeout(1000)\n'''+s[j:].replace('page.unroute(\"**/api/cases\"); ','',1)\nopen(p,\"w\").write(s)\nEOF\ncp artifacts/review-evidence/T204_r2_probe_guided.py $C/tests/e2e/test_probe_t204_r2.py; cd $C && PROBE_OUT=$S/T204_r2 E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_probe_t204_r2.py -q -s -p no:cacheprovider 2>&1 | tail -60",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:17:37.153Z

**tool result**
````
            # ---------------- guided
            page.goto(C.SERVER + "/"); page.wait_for_timeout(1200); _open_all(page)
            # accept the held item in the guided flow via API so step 4 shows its blocker
            r = api("POST", f"/api/cases/{t['tok']}/items/{t['id']}/review", {"action": "accept"}); print("accept held:", r[0])
            for name, path in (("g_records", "records"), ("g_timeline", "timeline"), ("g_bills", "bills"), ("g_letter", "letter")):
                page.goto(C.SERVER + f"/case/{t['tok']}/{path}"); page.wait_for_timeout(1800); _open_all(page)
                _click_all(page, "button:has-text('Why'), button:has-text('How'), button:has-text('check'), summary")
                _open_all(page); page.wait_for_timeout(300)
            # a fresh sample case through the draft button (step 1 done screen, with the server's banner)
            st, nc = api("POST", "/api/cases", {"sample": True, "title": "probe step1"}); assert st == 201
            page.goto(C.SERVER + f"/case/{nc['token']}/records"); page.wait_for_timeout(1000)
            page.get_by_test_id("btn-draft").click(); expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=20000)
            print("STEP1 done banner:", page.get_by_test_id("ai-banner").inner_text() if page.get_by_test_id("ai-banner").count() else None)
            print("STEP1 prov:", page.locator("p.prov").inner_text() if page.locator("p.prov").count() else None)
            _open_all(page); page.wait_for_timeout(500)
            g = _report("GUIDED", page)
            # ---------------- classic
>           page.goto(C.BASE); page.wait_for_timeout(1500); page.reload(); page.get_by_test_id("timeline").wait_for()
                                                                           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

tests/e2e/test_probe_t204_r2.py:78: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/sync_api/_generated.py:13635: in wait_for
    self._sync(
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_locator.py:767: in wait_for
    await self._frame.wait_for_selector(
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_frame.py:395: in wait_for_selector
    await self._channel.send(
/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:78: in send
    return await self._connection.wrap_api_call(
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 

self = <playwright._impl._connection.Connection object at 0x10aedd190>
cb = <function Channel.send.<locals>.<lambda> at 0x11145aca0>
is_internal = False, title = None

    async def wrap_api_call(
        self, cb: Callable[[], Any], is_internal: bool = False, title: str = None
    ) -> Any:
        if self._api_zone.get():
            return await cb()
        task = asyncio.current_task(self._loop)
        parsed_st = _attach_api_call_information(
            getattr(task, "__pw_stack__", None) or _capture_stack_trace(),
            is_internal,
            title,
        )
        self._api_zone.set(parsed_st)
        try:
            return await cb()
        except Exception as error:
>           raise rewrite_error(error, f"{parsed_st['apiName']}: {error}") from None
E           playwright._impl._errors.TimeoutError: Locator.wait_for: Timeout 30000ms exceeded.
E           Call log:
E             - waiting for get_by_test_id("timeline") to be visible

/Users/arsis/zlayt-pm-project/.venv/lib/python3.12/site-packages/playwright/_impl/_connection.py:636: TimeoutError
=========================== short test summary info ============================
FAILED tests/e2e/test_probe_t204_r2.py::test_probe_guided_and_classic - playw...
1 failed in 48.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:17:47.089Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\npython3 - <<'EOF'\np=\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_probe_guided.py\"\ns=open(p).read()\ni=s.index(\"        # ---------------- classic\")\nj=s.index(\"    finally:\\n        br.close()\")\nclassic=s[i:j]\ns=s[:i]+\"        return\\n\"+s[j:]\ns=s.replace(\"def test_probe_guided_and_classic(pw, edited_quote):\",\"def test_probe_guided(pw, edited_quote):\")\ns+='''\n\ndef test_probe_classic(page, edited_quote):\n    from tests.e2e.test_stepper import open_rail, open_judges\n    from tests.e2e.conftest import reveal\n    t = edited_quote; _accept_something_else(t)\n    page.add_init_script(OBS)\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    row = _row(page, t[\"id\"]); row.focus(); page.keyboard.press(\"a\"); row.get_by_test_id(\"btn-accept\").click()\n    expect(row).to_have_attribute(\"data-review\", \"accepted\")\n    page.reload(); page.get_by_test_id(\"timeline\").wait_for()\n    cs = open_rail(page); _open_all(page)\n    jp = open_judges(page); _open_all(page)\n    _click_all(page, \"[data-testid=btn-trace], [data-testid=entry-why], [data-testid=btn-audit], [data-testid=btn-export]\", 14)\n    _open_all(page); page.wait_for_timeout(600)\n    k = _report(\"CLASSIC\", page)\n    import json, os\n    open(os.path.join(os.environ.get(\"PROBE_OUT\", \".\"), \"probe_t204_r2_classic.json\"), \"w\").write(json.dumps(k, indent=1))\n'''\ns=s.replace('''        out = {\"guided\": g, \"classic\": k}\n''','')\ns=s.replace('''        import json, os\n        open(os.path.join(os.environ.get(\"PROBE_OUT\", \".\"), \"probe_t204_r2_out.json\"), \"w\").write(json.dumps(out, indent=1))\n''','''        import json, os\n        open(os.path.join(os.environ.get(\"PROBE_OUT\", \".\"), \"probe_t204_r2_guided.json\"), \"w\").write(json.dumps(g, indent=1))\n''')\nopen(p,\"w\").write(s)\nEOF\ngrep -n \"return$\\|classic\\|out =\" artifacts/review-evidence/T204_r2_probe_guided.py | head; "
}
````

### User / tool · 2026-11-03T01:17:47.209Z

**tool result**
````
77:        return
82:def test_probe_classic(page, edited_quote):
97:    open(os.path.join(os.environ.get("PROBE_OUT", "."), "probe_t204_r2_classic.json"), "w").write(json.dumps(k, indent=1))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:17:52.446Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nsed -n 70,80p artifacts/review-evidence/T204_r2_probe_guided.py\ncp artifacts/review-evidence/T204_r2_probe_guided.py $C/tests/e2e/test_probe_t204_r2.py; cd $C && PROBE_OUT=$S/T204_r2 E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_probe_t204_r2.py -q -s -p no:cacheprovider 2>&1 | grep -v \"^\\s*$\" | tail -80",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:18:13.812Z

**tool result**
````
        st, nc = api("POST", "/api/cases", {"sample": True, "title": "probe step1"}); assert st == 201
        page.goto(C.SERVER + f"/case/{nc['token']}/records"); page.wait_for_timeout(1000)
        page.get_by_test_id("btn-draft").click(); expect(page.get_by_test_id("draft-done")).to_be_visible(timeout=20000)
        print("STEP1 done banner:", page.get_by_test_id("ai-banner").inner_text() if page.get_by_test_id("ai-banner").count() else None)
        print("STEP1 prov:", page.locator("p.prov").inner_text() if page.locator("p.prov").count() else None)
        _open_all(page); page.wait_for_timeout(500)
        g = _report("GUIDED", page)
        return
    finally:
        br.close()

HEALTH answers=prepared demo_mode=True local_mode=True ai_banner='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item'
CASE models: {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}
accept held: 200
STEP1 done banner: In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item
STEP1 prov: Prepared by our team Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
=== GUIDED: 97 texts seen, 6 with AI/model words
   LEAK> A second AI check of each line
   LEAK> Summaries and warnings are drafted by AI and checked by code; you decide every item.
   LEAK> Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
   LEAK> In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item
   LEAK> Prepared by our team Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
   LEAK> Demo: sample answers prepared by our team. Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
.
=== CLASSIC: 736 texts seen, 45 with AI/model words
   LEAK> model
   LEAK> · model
   LEAK> AI check
   LEAK> AI objected
   LEAK> the AI said
   LEAK> The AI said:
   LEAK> AI agreed 18
   LEAK> AI objected 0
   LEAK> AI check totals
   LEAK> claude-haiku-5-5
   LEAK> AI did not check
   LEAK> AI quality checks.
   LEAK> items checked by AI
   LEAK> Where the AI objected
   LEAK> How the AI was checked
   LEAK> Loading the AI checks…
   LEAK> records split by code (not AI)
   LEAK> Where the AI objected (0 items)
   LEAK> The phrase list and the AI disagree
   LEAK> Where the AI could not check or decide
   LEAK> Show the 1 item the AI could not check
   LEAK> Where code and the AI read an item differently
   LEAK> Where the AI could not check or decide (1 item)
   LEAK> The AI said: The prepared answers did not include it.
   LEAK> Where code and the AI read an item differently (1 item)
   LEAK> AI did not checkBlocks the exportYour decision: Accepted
   LEAK> The phrase list and the AI disagreeYour decision: Not reviewed
   LEAK> Compared by you with the quote. The second AI check did not run.
   LEAK> Prepared by our team (not by an AI model), checked by claude-haiku-5-5.
   LEAK> model claude-haiku-5-5prompt judge_faithfulness_v1your decision Accepted
   LEAK> What you need to do: 1 accepted item cannot go in the letter until the second AI check has run on it.
   LEAK> Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.
   LEAK> The second check cannot be run again here: no AI model can answer it right now. The items stay out of the letter until it has run.
   LEAK> In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item
   LEAK> 6 checked: 6 agreed, 0 partly, 0 not supported, 0 read differently, 0 undecided, 0 unavailable. Prompt judge_flag_v3 · model claude-haiku-5-5
   LEAK> 1 checked: 1 agreed, 0 partly, 0 not supported, 0 read differently, 0 undecided, 0 unavailable. Prompt judge_conflict_v6 · model claude-haiku-5-5
   LEAK> 9 checked: 8 agreed, 0 partly, 0 not supported, 0 read differently, 0 undecided, 1 unavailable. Prompt judge_faithfulness_v1 · model claude-haiku-5-5
   LEAK> 3 checked: 3 agreed, 0 partly, 0 not supported, 0 read differently, 0 undecided, 0 unavailable. Prompt judge_amount_class_v1 · model claude-haiku-5-5
   LEAK> kind of disagreement sources_disagreeresolution needs_reviewthe code check said The phrase list found it.the AI said The prepared answers did not include it.
   LEAK> When you save, the code checks every number, date and negation in your wording against the quote, then a second AI check reads it. Nothing is added to the letter until it passes.
   LEAK> AI quality checks. This shows how a second AI model checked the answers our team prepared for this demo. It is not a verdict on the case, the care or the claim, and it does not replace your review.
   LEAK> What you need to do: You changed the quote on an accepted entry and kept the prepared wording, and the second AI check has no answer on the new quote. Run the second check again, or write the summary in your own words.
   LEAK> Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample). Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).
   LEAK> ✓ passed · ✕ failed or blocked · – skipped · ○ not done yet, or waiting for you. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “You” steps are your decisions, and “Prepared answer” steps are our team’s wording for this
   LEAK> What you need to do: The second AI check did not run on 1 item. Run it again; accepted items it never checked cannot go in the letter. You changed the quote on an accepted entry and kept the prepared wording, and the second AI check has no answer on the new qu
.
2 passed in 20.26s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:16.838Z

**tool call — Bash**
````
{
 "command": "grep -rn \"drafted by AI\" app/frontend | head; "
}
````

### User / tool · 2026-11-03T01:18:16.931Z

**tool result**
````
app/frontend/mock.js:147:        ai_banner: "Summaries and flags are drafted by AI and checked by code; you decide every item", sample_available: true });
app/frontend/app.js:11:    const ai = $("#banner-ai"); ai.hidden = !(s.case && s.case.status === "ready"); ai.textContent = ai.hidden ? "" : s.case && s.case.models && s.case.models.generator_prepared ? PREPARED_BANNER : (h && h.ai_banner) || "Summaries and flags are drafted by AI and checked by code; you decide every item";   // T-204 r2: the case says whose answers they are
app/frontend/guided/app.js:48:    return { kind, label: DEMO[kind] ? DEMO[kind][0] : "", note: DEMO[kind] ? DEMO[kind][1] : "Summaries and warnings are drafted by AI and checked by code; you decide every item.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:18.410Z

**tool call — Bash**
````
{
 "command": "sed -n 25,75p app/frontend/guided/app.js; git show 679b63e -- app/frontend/guided | head -60"
}
````

### User / tool · 2026-11-03T01:18:18.520Z

**tool result**
````
  const FRAME = { timeline: true, bills: true };

  /* ---- theme (spec 2.2): follows the OS until she picks; remembered in localStorage inside try/catch ---- */
  const isDark = () => { const t = root.getAttribute("data-theme"); return t ? t === "dark" : matchMedia("(prefers-color-scheme: dark)").matches; };
  try { const t = localStorage.getItem("zl.guided.theme"); if (t === "light" || t === "dark") root.setAttribute("data-theme", t); } catch (_) { /* follows the OS */ }
  function themeLabel() { const b = $("[data-theme-btn]"); if (b) { b.textContent = isDark() ? "Light mode" : "Dark mode"; b.setAttribute("aria-label", b.textContent); } }
  matchMedia("(prefers-color-scheme: dark)").addEventListener("change", themeLabel);
  function themeButton() {
    return h("button", { type: "button", class: "theme-btn", "data-theme-btn": "", "data-testid": "btn-theme", onclick: () => {
      const next = isDark() ? "light" : "dark"; root.setAttribute("data-theme", next);
      try { localStorage.setItem("zl.guided.theme", next); } catch (_) { /* not remembered */ }
      themeLabel();
    } }, "Dark mode");
  }

  /* ---- banner, demo label and footer (spec 2.1, 2.3, 2.8; D-065): wording by health.answers, never softened ---- */
  // D-065 as amended in T-177 r2: the prepared-answers sentence is the amended one (the spec 2.3 sentence about the evaluation report is superseded)
  const DEMO = { prepared: ["Demo: sample answers prepared by our team", "Prepared by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote."],
    recorded: ["Demo: recorded AI answers", "These are real AI answers recorded earlier; nothing new is sent to an AI."] };
  // A case whose lines were written by a model (models.generator_prepared === false) is never described as prepared by the team, even when the server's curated set is on (T-181 r2, paralegal minor).
  G.provenance = function (c) {
    const hl = G.store.health, cur = c === undefined ? G.store.current : c, notPrepared = !!(cur && cur.models && cur.models.generator_prepared === false);
    const kind = hl && hl.demo_mode ? (hl.answers === "prepared" && !notPrepared ? "prepared" : "recorded") : "live";
    return { kind, label: DEMO[kind] ? DEMO[kind][0] : "", note: DEMO[kind] ? DEMO[kind][1] : "Summaries and warnings are drafted by AI and checked by code; you decide every item.",
      hours: hl && !hl.demo_mode ? hl.retention_hours : null };
  };
  function drawBanner() {
    const hl = G.store.health, p = G.provenance();
    $("#banner-text").textContent = (hl && hl.banner) || "Synthetic data only — never paste real records";
    $("#banner-demo").textContent = p.label;
    const f = $("#footer"); f.replaceChildren(...[h("span", { "data-testid": "footer-note" }, p.label ? p.label + ". " + p.note : p.note),
      p.hours ? h("span", { class: "f-live" }, `Pasted text is deleted after ${p.hours} hours.`) : null].filter(Boolean));     // replaceChildren(null) would print the text "null"
  }
  let headerState = { title: null, sub: null };
  function drawHeader() {
    const p = G.provenance(), t = headerState.title;
    const left = t == null
      ? h("a", { class: "brand", href: "/", "data-testid": "brand" }, h("span", { class: "brand-mark", "aria-hidden": "true" }, "TT"), h("span", {}, "Treatment Timeline"))
      : [h("a", { class: "back-cases", href: "/", "data-testid": "btn-your-cases" }, h("span", { "aria-hidden": "true" }, "‹"), h("span", { class: "long" }, "Your cases"), h("span", { class: "short" }, "Cases")),
         h("div", { class: "hd-case" }, h("span", { class: "case-title", "data-testid": "case-title", title: t }, t), headerState.sub ? h("span", { class: "case-sub" }, headerState.sub) : null)];
    headerEl.replaceChildren(...[].concat(left), h("span", { class: "spacer" }), ...(p.label ? [h("span", { class: "demo-pill", "data-testid": "demo-badge", title: p.note }, p.label)] : []), themeButton());
    themeLabel();
  }
  G.store.healthP = G.api.health();
  G.store.healthP.then((hl) => { G.store.health = hl; drawBanner(); drawHeader(); G.emit("health", hl); }).catch(() => { /* the static banner stays; pages that need health read G.store.health and cope with null */ });

  /* ---- step bar (spec 2.4): same four steps in the same place; only classes, statuses and links change ---- */
  const overrides = {};      // token -> { n: [text, state?] }
  function drawBar(route, token, c, step) {
    const show = route === "new" || (token && step);
    bar.hidden = !show; if (!show) return;
commit 679b63eb331b72580fb0c571d27c6a9afece2653
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 19:00:16 2026 -0600

    fix(frontend): T-204 r2 a prepared answer is never the AI's wording on the case rail, AI-check panel, audit, tray, banner or legends; whole-DOM observer walk of the prepared sample; condition waits
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/frontend/guided/review.js b/app/frontend/guided/review.js
index 0aeeda3..a1bff76 100644
--- a/app/frontend/guided/review.js
+++ b/app/frontend/guided/review.js
@@ -27,7 +27,7 @@
       .replace(/\bsummary or quote\b/g, "line or highlighted words").replace(/\bthe quotes?\b/g, "the highlighted words").replace(/\bQuote\b/g, "The highlighted words").replace(/\bquotes?\b/g, "highlighted words")
       .replace(/\bthe summary\b/g, "the line").replace(/\bThe summary\b/g, "The line").replace(/\bsummary\b/g, "line")
       .replace(/\ban itemized service line\b/g, "a single dated bill line").replace(/\bitemized service line\b/g, "single dated bill line").replace(/\ban itemized\b/g, "a line-by-line").replace(/\bitemized\b/g, "line-by-line")
-      .replace(/\binternal notes\b/g, "notes for the attorney").replace(/\bthe model's\b/gi, "the AI's").replace(/\bmodel\b/g, "AI")
+      .replace(/\binternal notes\b/g, "notes for the attorney").replace(/\bthe model's\b/gi, G.provenance().kind === "prepared" ? "the prepared answer's" : "the AI's").replace(/\bmodel\b/g, G.provenance().kind === "prepared" ? "prepared answer" : "AI")
       .replace(/\bflags\b/g, "warnings").replace(/\bflag\b/g, "warning").replace(/\bthis entry\b/g, "this line"))).join("");
   };
 
diff --git a/app/frontend/guided/step2.js b/app/frontend/guided/step2.js
index a1e4833..f13e38c 100644
--- a/app/frontend/guided/step2.js
+++ b/app/frontend/guided/step2.js
@@ -366,7 +366,7 @@
         first ? h("a", { class: "btn primary lg", href: G.url.timeline(S.token, first.q.id), "data-testid": "btn-first-undecided" }, "Go to the first one") : null,
         h("a", { class: "btn lg " + (first ? "" : "primary"), href: nextHref, "data-testid": "btn-next-step" }, nextLabel))),
       h("div", { class: "panel" }, h("h2", {}, "Your answers"), h("p", { class: "muted" }, "Every item in the order you saw it. Change any answer here."), h("ol", { class: "answers", "data-testid": "answers-list" }, rows),
-        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. “AI draft” means an AI wrote it. “Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
+        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. " + (G.provenance().kind === "prepared" ? "" : "“AI draft” means an AI wrote it. ") + "“Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
       trayDone.length ? h("div", { class: "panel", "data-testid": "tray-done" }, h("h2", {}, "Items we couldn't check"), h("p", { class: "muted" }, "These are optional. They stay out of the letter unless you wrote the line yourself."),
         h("ul", { class: "plain-list" }, trayDone.map((t) => h("li", {}, h("a", { href: G.url.timeline(S.token, t.id) }, t.kind === "flag" ? "A suggested warning we couldn't confirm" : "A record with no line"), t.review_status === "dismissed" ? " (skipped)" : "")))) : null,
       filtered ? h("div", { class: "panel", "data-testid": "filtered-rules" }, h("h2", {}, "Suggestions a rule ruled out (nothing to do)"),
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:21.966Z

**tool call — Bash**
````
{
 "command": "grep -n \"drafted\\|AI\\b\" app/frontend/guided/index.html | head; grep -rn \"G.provenance()\\|provenance(\" app/frontend/guided/*.js | grep -v \"^app/frontend/guided/app.js:4[0-9]\" | head -30"
}
````

### User / tool · 2026-11-03T01:18:22.067Z

**tool result**
````
app/frontend/guided/app.js:52:    const hl = G.store.health, p = G.provenance();
app/frontend/guided/app.js:60:    const p = G.provenance(), t = headerState.title;
app/frontend/guided/step1.js:176:    const prepared = () => G.provenance().kind === "prepared";
app/frontend/guided/step1.js:273:        prep ? h("p", { class: "prov" }, h("span", { class: "tag prep", title: G.provenance().note, "data-testid": "prepared-badge" }, "Prepared by our team"), " ", G.provenance().note) : null),
app/frontend/guided/review.js:30:      .replace(/\binternal notes\b/g, "notes for the attorney").replace(/\bthe model's\b/gi, G.provenance().kind === "prepared" ? "the prepared answer's" : "the AI's").replace(/\bmodel\b/g, G.provenance().kind === "prepared" ? "prepared answer" : "AI")
app/frontend/guided/review.js:63:    const p = G.provenance();
app/frontend/guided/review.js:69:  // G.provenance() follows the open case: a case whose lines an AI wrote says so, never "not written by an AI model" (T-181 r2)
app/frontend/guided/review.js:70:  R.aiNote = () => { const p = G.provenance(), hl = G.store.health; return p.kind === "live" && hl && hl.ai_banner ? hl.ai_banner : p.note; };
app/frontend/guided/step4.js:98:      const prov = prep ? h("p", { class: "prov" }, h("span", { class: "tag prep", title: G.provenance().note, "data-testid": "prepared-badge" }, "Prepared by our team"), " ", G.provenance().note) : null;
app/frontend/guided/step2.js:369:        h("p", { class: "muted legend" }, "“Prepared answer” means our team wrote that line for this demo. " + (G.provenance().kind === "prepared" ? "" : "“AI draft” means an AI wrote it. ") + "“Written by you” means you did. A second AI check read each one against the record, unless the line says it was not double-checked.")),
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:23.761Z

**tool call — Bash**
````
{
 "command": "grep -n \"drawBanner\\|drawHeader\" app/frontend/guided/app.js | head -20"
}
````

### User / tool · 2026-11-03T01:18:23.843Z

**tool result**
````
51:  function drawBanner() {
59:  function drawHeader() {
69:  G.store.healthP.then((hl) => { G.store.health = hl; drawBanner(); drawHeader(); G.emit("health", hl); }).catch(() => { /* the static banner stays; pages that need health read G.store.health and cope with null */ });
111:    G.store.current = null; headerState = { title: r.name === "new" ? "New case" : null, sub: null }; drawHeader(); drawBanner();
117:      setCaseTitle: (t) => { if (!stale()) { headerState.title = t; drawHeader(); } },
121:    function paintCase(j) { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, r.token, j, r.step); }
166:  G.on("case", (token, j) => { const r = now; if (r && r.token === token && r.name !== "redirect") { G.store.current = j; drawBanner(); headerState = { title: G.titleOf(j), sub: j.records ? `${j.records.length} record${j.records.length === 1 ? "" : "s"}` : null }; drawHeader(); drawBar(r.name, token, j, r.step); } });
167:  drawBanner(); drawHeader();
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:33.906Z

**tool call — Bash**
````
{
 "command": "grep -n \"the AI said\\|The AI said\\|phrase list and the AI\\|code and the AI\\|AI disagree\" -r app/frontend app/backend | head -20"
}
````

### User / tool · 2026-11-03T01:18:33.998Z

**tool result**
````
app/frontend/judges.js:15:    sources_disagree: "The phrase list and the AI disagree",
app/frontend/judges.js:75:    it.dis.forEach((x) => bits.push(kv("kind of disagreement", x.type), kv("resolution", x.resolution), kv("the code check said", x.code_says), kv("the AI said", noCode(x.judge_says))));
app/frontend/judges.js:101:      tray ? null : it.dis.map((x) => el("p", { class: "zs-ev" }, el("span", { class: "zs-k" }, "The code check said: "), x.code_says || "", el("br"), el("span", { class: "zs-k" }, "The AI said: "), noCode(x.judge_says))),
app/frontend/judges.js:192:    if (differ.length) det.append(list("judge-disagreements", "Where code and the AI read an item differently", differ, (i) => row(i, "judge-disagreement"), ""));
app/backend/trace.py:787:        st.append(step("agreement", _AGREE[1 if prep else 0], "code", PASS, pick("Both the phrase list and the AI found this flag.", "Both the phrase list and the prepared answers include this flag."), rule="row 12"))
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:38.160Z

**tool call — Bash**
````
{
 "command": "grep -rn \"did not include it\" app/backend | head; grep -n \"judge_says\" app/backend/*.py | head"
}
````

### User / tool · 2026-11-03T01:18:38.259Z

**tool result**
````
app/backend/trace.py:1096:                                      "judge_says": ((("The prepared answers did not include it." if c == "LEXICON_ONLY" else "The prepared answers included it.") if prepared_item(cx, row, "flag") or cx.prep
app/backend/trace.py:1078:                                      "judge_says": f"{says} ({r['reason_code']})" if says and r["reason_code"] != "NONE" else "not a " + row["kind"],
app/backend/trace.py:1082:                                      "judge_says": rationale_or(r["reason_code"], v), "resolution": "needs_review", "review_status": row["review_status"]})
app/backend/trace.py:1088:                                  "code_says": " ".join(reason_text(c) for c in sorted(R & _CODE_CHECK_REASONS)), "judge_says": _J_OK[r["judge"]],
app/backend/trace.py:1096:                                      "judge_says": ((("The prepared answers did not include it." if c == "LEXICON_ONLY" else "The prepared answers included it.") if prepared_item(cx, row, "flag") or cx.prep
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:18:39.719Z

**tool call — Bash**
````
{
 "command": "sed -n 1090,1100p app/backend/trace.py | cut -c1-600"
}
````

### User / tool · 2026-11-03T01:18:39.806Z

**tool result**
````
    for row in DB.list_items(conn, case_id, "flag"):
        R = set(row.get("state_reasons") or [])
        for c in ("LEXICON_ONLY", "LLM_ONLY"):
            if c in R:
                disagreements.append({"item_id": row["id"], "kind": "flag", "type": "sources_disagree",
                                      "code_says": "The phrase list found it." if c == "LEXICON_ONLY" else "The phrase list did not find it.",
                                      "judge_says": ((("The prepared answers did not include it." if c == "LEXICON_ONLY" else "The prepared answers included it.") if prepared_item(cx, row, "flag") or cx.prep
                                                     else ("The AI did not find it." if c == "LEXICON_ONLY" else "The AI found it."))),
                                      "resolution": "needs_review", "review_status": row["review_status"]})
    j = lambda *ks: sum(sum(p[k] for p in per.values()) for k in ks)      # noqa: E731
    judges_out = [dict(p, models=sorted(p["models"])) for p in per.values()]
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:00.908Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_probe_narrow.py <<'EOF'\n\"\"\"T-204 r2 probes (staff-engineer). Copy into a git-archive of 679b63e as tests/e2e/test_probe_t204_r2b.py; E2E_REQUIRE_DB=1 -s.\nP1: plain prepared sample (no edits), classic: the AI-check panel's disagreement rows say 'The AI said:' over the sentence 'The prepared answers did not include it.'\nP2: guided UI, /api/health held: what does the footer / header paint for the prepared sample before health answers? (G.provenance() with health undefined = 'live')\"\"\"\nimport re\nfrom playwright.sync_api import expect\nimport tests.e2e.conftest as C\nfrom tests.e2e.conftest import api\nfrom tests.e2e.guided._helpers import browser, make_case\nfrom tests.e2e.test_stepper import open_rail, open_judges\n\n\ndef test_p1_plain_sample_panel(page):\n    st, c = api(\"POST\", \"/api/cases\", {\"sample\": True, \"title\": \"p1\"}); tok = c[\"token\"]\n    api(\"POST\", f\"/api/cases/{tok}/run\", {\"confirm_rerun\": False})\n    import time\n    for _ in range(100):\n        if api(\"GET\", f\"/api/cases/{tok}/status\")[1][\"status\"] == \"ready\": break\n        time.sleep(.3)\n    j = api(\"GET\", f\"/api/cases/{tok}/judges\")\n    print(\"P1 judges status\", j[0]); dis = (j[1] or {}).get(\"disagreements\")\n    print(\"P1 API disagreements:\", dis)\n    page.goto(C.BASE); page.evaluate(\"t => localStorage.setItem('x', t)\", tok)\n    # open the case the way the app does: via the cases overview link\n    page.goto(C.BASE + \"#\" + tok); page.wait_for_timeout(500)\n    try:\n        page.get_by_test_id(\"cases-open\").first.wait_for(timeout=3000)\n    except Exception:\n        pass\n    ln = page.locator(f\"[data-token='{tok}'] [data-testid=cases-open]\")\n    if ln.count(): ln.first.click()\n    page.get_by_test_id(\"timeline\").wait_for()\n    jp = open_judges(page)\n    page.evaluate(\"document.querySelectorAll('details').forEach(d => d.open = true)\")\n    txt = jp.inner_text()\n    hits = [l for l in txt.split(\"\\n\") if re.search(r\"the AI\\b|AI said|AI disagree|read an item differently\", l, re.I)]\n    print(\"P1 panel lines:\", hits)\n    jp.screenshot(path=\"probe_t204_r2_panel.png\")\n    assert not [l for l in hits if re.search(r\"AI said|and the AI\", l, re.I)], hits\n\n\ndef test_p2_guided_footer_before_health(pw):\n    tok = make_case(\"p2\", run=True)\n    br, page = browser(pw, 1440, 900)\n    held = []\n    page.route(\"**/api/health\", lambda r: held.append(r))\n    seen = []\n    try:\n        page.goto(C.SERVER + f\"/case/{tok}/timeline\", wait_until=\"domcontentloaded\"); page.wait_for_timeout(1500)\n        f = page.get_by_test_id(\"footer-note\")\n        seen.append((\"before health\", f.inner_text() if f.count() else None))\n        page.screenshot(path=\"probe_t204_r2_guided_prehealth.png\")\n        while held: held.pop().continue_()\n        page.wait_for_timeout(1500)\n        seen.append((\"after health\", page.get_by_test_id(\"footer-note\").inner_text()))\n    finally:\n        br.close()\n    for s in seen: print(\"P2\", s)\n    assert not re.search(r\"drafted by AI\", seen[0][1] or \"\"), seen\nEOF\ncd /Users/arsis/zlayt-pm-project && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\ncp artifacts/review-evidence/T204_r2_probe_narrow.py $C/tests/e2e/test_probe_t204_r2b.py; cd $C && E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_probe_t204_r2b.py -q -s -p no:cacheprovider 2>&1 | grep -v \"^\\s*$\" | tail -50",
 "timeout": 300000
}
````

### User / tool · 2026-11-03T01:19:07.787Z

**tool result**
````
        print("P1 API disagreements:", dis)
        page.goto(C.BASE); page.evaluate("t => localStorage.setItem('x', t)", tok)
        # open the case the way the app does: via the cases overview link
        page.goto(C.BASE + "#" + tok); page.wait_for_timeout(500)
        try:
            page.get_by_test_id("cases-open").first.wait_for(timeout=3000)
        except Exception:
            pass
        ln = page.locator(f"[data-token='{tok}'] [data-testid=cases-open]")
        if ln.count(): ln.first.click()
        page.get_by_test_id("timeline").wait_for()
        jp = open_judges(page)
        page.evaluate("document.querySelectorAll('details').forEach(d => d.open = true)")
        txt = jp.inner_text()
        hits = [l for l in txt.split("\n") if re.search(r"the AI\b|AI said|AI disagree|read an item differently", l, re.I)]
        print("P1 panel lines:", hits)
        jp.screenshot(path="probe_t204_r2_panel.png")
>       assert not [l for l in hits if re.search(r"AI said|and the AI", l, re.I)], hits
E       AssertionError: ['How the AI was checked', 'Where the AI objected (0 items)', 'Where code and the AI read an item differently (1 item)...olution needs_reviewthe code check said The phrase list found it.the AI said The prepared answers did not include it.']
E       assert not ['Where code and the AI read an item differently (1 item)', 'The phrase list and the AI disagreeYour decision: Not rev...olution needs_reviewthe code check said The phrase list found it.the AI said The prepared answers did not include it.']
tests/e2e/test_probe_t204_r2b.py:38: AssertionError
_____________________ test_p2_guided_footer_before_health ______________________
pw = <playwright._impl._playwright.Playwright object at 0x109420140>
    def test_p2_guided_footer_before_health(pw):
        tok = make_case("p2", run=True)
        br, page = browser(pw, 1440, 900)
        held = []
        page.route("**/api/health", lambda r: held.append(r))
        seen = []
        try:
            page.goto(C.SERVER + f"/case/{tok}/timeline", wait_until="domcontentloaded"); page.wait_for_timeout(1500)
            f = page.get_by_test_id("footer-note")
            seen.append(("before health", f.inner_text() if f.count() else None))
            page.screenshot(path="probe_t204_r2_guided_prehealth.png")
            while held: held.pop().continue_()
            page.wait_for_timeout(1500)
            seen.append(("after health", page.get_by_test_id("footer-note").inner_text()))
        finally:
            br.close()
        for s in seen: print("P2", s)
>       assert not re.search(r"drafted by AI", seen[0][1] or ""), seen
E       AssertionError: [('before health', 'Summaries and warnings are drafted by AI and checked by code; you decide every item.'), ('after he...by our team for this demo, not written by an AI model. A second AI model then checked each answer against its quote.')]
E       assert not <re.Match object; span=(27, 40), match='drafted by AI'>
E        +  where <re.Match object; span=(27, 40), match='drafted by AI'> = <function search at 0x107cd87c0>('drafted by AI', ('Summaries and warnings are drafted by AI and checked by code; you decide every item.'))
E        +    where <function search at 0x107cd87c0> = re.search
tests/e2e/test_probe_t204_r2b.py:58: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_probe_t204_r2b.py::test_p1_plain_sample_panel - Asserti...
FAILED tests/e2e/test_probe_t204_r2b.py::test_p2_guided_footer_before_health
2 failed in 5.77s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:19.815Z

**tool call — Bash**
````
{
 "command": "grep -rn \"backend (\" app/frontend/suggestions.js | head -5; grep -rn \"testing on the\" app/backend app/frontend | head; ls evals/ | head -20; ls evals/reports 2>/dev/null | tail -5"
}
````

### User / tool · 2026-11-03T01:19:19.929Z

**tool result**
````
__init__.py
__pycache__
adversarial
finalize_prompt_log.py
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
privacy_tree_scan.py
reports
run.py
determinism-diagnosis.md
latest.json
library-latest.md
m3-sensors.md
runs
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:21.634Z

**tool call — Bash**
````
{
 "command": "grep -n \"backend\" app/frontend/suggestions.js | head; grep -rn \"calibration\" app/backend/*.py | grep -n \"def \\|backend\" | head"
}
````

### User / tool · 2026-11-03T01:19:21.732Z

**tool result**
````
4:   ZL.sg.calibration   measured precision: the backend's own sentences, a small-sample note, plain words when the file is missing or invalid (T-099)
142:        // T-166 F7: the counts in plain words, from the measured numbers themselves; the report's own sentence (it names the test backend and the golden set) is kept in a Technical detail toggle, verbatim.
1:app/backend/calibration_route.py:1:"""GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).
2:app/backend/calibration_route.py:3:Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
3:app/backend/calibration_route.py:6:Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
4:app/backend/calibration_route.py:7:- "ok": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the
5:app/backend/calibration_route.py:14:- "missing": no file. `calibration` is null. Nothing is invented.
6:app/backend/calibration_route.py:16:  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.
7:app/backend/calibration_route.py:17:The UI hides the accuracy line when `calibration` is null (T-096) and shows "numbers from an older version" when `stale` is true.
8:app/backend/calibration_route.py:26:REPORT = ROOT / "evals" / "reports" / "calibration.json"
9:app/backend/calibration_route.py:27:SCHEMA = "evals.calibration/1"
10:app/backend/calibration_route.py:34:MISSING = "No calibration has been measured yet, so no accuracy line is shown."
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:26.242Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json;d=json.load(open('evals/reports/calibration.json'));print({k:(v if not isinstance(v,(list,dict)) else '...') for k,v in d.items()});print(d.get('statements') or d.get('totals'))\"; sed -n 136,160p app/frontend/suggestions.js | cut -c1-400; git log --oneline -3 -- evals/reports/calibration.json"
}
````

### User / tool · 2026-11-03T01:19:26.404Z

**tool result**
````
{'backend': 'claude-cli', 'by_state': '...', 'by_type': '...', 'case_count': 10, 'cases': '...', 'generated_at': '2026-11-02T16:40:38Z', 'hashes': '...', 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'models': '...', 'not_scored': '...', 'schema': 'evals.calibration/1', 'sentences': '...', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': '312efe663327539df1b712832e23bf1d2c495d42', 'source_tree': '6b761a5e9e52539270e3c7c20bd68d1f8c0bd45a', 'source_tree_clean': True}
None
      }
      const o = c.sentences.overall; if (c.stale) box.setAttribute("data-stale", "true");
      box.append(...[
        // T-102: the counts were measured with other prompts than the ones the app runs now. Said once, ABOVE the numbers so the warning is read first; the changed-prompt detail sits behind a disclosure.
        c.stale ? el("div", { class: "sg-cal-stale", role: "note", "data-testid": "calibration-stale" }, el("strong", {}, "These counts were measured before the latest change to the AI checks."), " Treat them as a rough guide.",
          c.stale_reason ? el("details", { class: "sg-cal-why" }, el("summary", {}, "Technical detail"), el("p", {}, c.stale_reason)) : null) : null,
        // T-166 F7: the counts in plain words, from the measured numbers themselves; the report's own sentence (it names the test backend and the golden set) is kept in a Technical detail toggle, verbatim.
        el("p", { class: "sg-cal-s", "data-testid": "calibration-verified" }, plainCount(c, "verified", "verified items") || "Measured on synthetic test cases."),
        c.small_sample ? el("p", { class: "sg-muted", "data-testid": "calibration-small-sample" },
          "Small sample: " + c.case_count + " synthetic test cases, so these counts are a rough indication, not a promise about your records.") : null,
        el("details", { class: "sg-cal-more" }, el("summary", {}, "The other side of the measurement"),
          el("p", { class: "sg-cal-s", "data-testid": "calibration-needs-review" }, plainCount(c, "needs_review", "items marked needs review") || "Measured on synthetic test cases."),
          el("details", { class: "sg-cal-tech", "data-testid": "calibration-tech" }, el("summary", {}, "Technical detail"), el("p", { class: "sg-muted" }, [o.verified, o.needs_review].filter(Boolean).join(" "))),
          c.not_scored && c.not_scored.total ? el("p", { class: "sg-muted" }, c.not_scored.total + (c.not_scored.total === 1 ? " item was" : " items were") + " not scored.") : null)].filter(Boolean));
    }
    draw();
    if (!cal) { calSubs.push(() => { if (box.isConnected) draw(); }); loadCalibration(); }
    return box;
  };

  // ---- 4. possible overlap warning -------------------------------------------------------------------------------------------------
  function goToAmount(id) {
    const row = document.querySelector('[data-testid="charges-panel"] [data-item-id="' + String(id).replace(/"/g, "") + '"]');
    if (!row) return;
    row.scrollIntoView({ block: "center" }); row.focus();
7cfdb0b test(qa): M2 re-gate live evidence: claude-cli 3-run at 312efe6 clean, ship_bar_met True, controls gate included, live calibration regenerated, letter_check 0
f3ac48f chore(evals): regenerate calibration.json from a clean worktree of 6fa8ecc (fixture; lexicon.yaml T-133 r3)
4065ef2 chore(evals): regenerate calibration.json from a clean worktree of f939ccb (fixture; lexicon.yaml T-133 r2)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:36.102Z

**tool call — Bash**
````
{
 "command": "grep -rln \"generator_prepared\" tests | head; grep -n \"generator_prepared\" app/backend/present.py | head -5; sed -n 160,180p app/frontend/guided/step1.js | cut -c1-300"
}
````

### User / tool · 2026-11-03T01:19:36.255Z

**tool result**
````
tests/unit/test_prepared_property.py
tests/unit/test_prepared_provenance_r3.py
tests/unit/test_prepared_provenance.py
tests/e2e/test_letter_matrix.py
283:        self.case_prepared = models_for(conn, case_id, {"generator": "", "judge": ""}, self.calls)["generator_prepared"]
338:    'hand-checked (qa)' and `generator_prepared` is true, so no screen names a model for an answer no model gave. A case with any recorded or live answer keeps the configured model; one with no usable answer follows the set in use."""
342:    return dict(base, generator=PREPARED_MODEL if prepared else base["generator"], generator_prepared=prepared)
        demo ? h("div", { class: "note-box demo-note", "data-testid": "demo-note" }, h("span", { class: "nb-text" }, ONLY(), h("span", {}, "Pasting your own records or uploading a file isn't available here."))) : null,
        h("div", { class: "field" }, h("label", { for: "case-name" }, "Name this case (optional)"), nameInput, h("span", { class: "hint", id: "name-hint" }, "For example the client's name. You can change it later."), nameErr),
        h("fieldset", { class: "how" }, h("legend", { class: "sr" }, "How do you want to add the records?"), h("div", { class: "tiles" + (tiles.length > 3 ? " four" : "") }, tileEls)),
        box, fileInput));
    ctx.view.append(main, bar.el);
    sync();
  };

  /* ---------------------------------------------------------------- /case/<token>/records */
  const STAGES = [["ingest", "Reading the records"], ["extract", "Writing one line for each record", "Getting the line our team prepared for each record"], ["verify", "Checking every line word for word against the record"],
    ["judge_entries", "A second AI check of each line"], ["amounts", "Finding the bill amounts"], ["conflicts", "Comparing the records with each other"],
    ["flags", "Looking for things the attorney should know"], ["finalize", "Putting it all together"]];

  G.pages.records = async function (ctx) {
    const token = ctx.token; let c = ctx.case, dead = false, timer = null, bar = null;
    G.cases.add(token);
    const prepared = () => G.provenance().kind === "prepared";
    const counts = () => { const n = G.steps.counts(c); return { lines: n.step2.total, bills: n.step3.total }; };
    const nextTarget = () => { const n = counts(); return n.lines > 0 ? ["Go to step 2: Check the timeline", G.url.timeline(token)] : n.bills > 0 ? ["Go to step 3: Check the bills", G.url.bills(token)] : ["Go to step 4: Get your letter", G.url.letter(token)]; };
    const main = h("main", { class: "wrap", id: "main" });
    ctx.view.append(main);
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:43.920Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; grep -n \"HELD_NO_RERUN\\|HELD_CAN_RERUN\\|preparedFor\" $C/app/frontend/stepper.js | cut -c1-330"
}
````

### User / tool · 2026-11-03T01:19:44.009Z

**tool result**
````
134:    try { msgNode.textContent = ""; await ZL.api.run(s.token, confirm); ZL.pollRun(); } catch (e) { msgNode.textContent = (S.preparedFor(null) ? "The checks could not be started: " : "The AI steps could not be started: ") + e.message; }
199:    if (e.code === "run_in_progress") return S.preparedFor(null) ? "The run is still going. Try again when it finishes." : "The AI run is still going. Try again when it finishes.";
338:        btn(S.preparedFor(null) ? "Run the checks again" : "Run the AI steps again", () => rerun(na.code === "CONFIRM_RERUN", msg)); break;
403:        const inner = Object.entries(v).map(([a, b]) => ((S.preparedFor(null) && PREP_WORD[a]) || WORD[a] || humanize(a)) + " " + b).join(", ");
406:      else if (v != null && v !== "") out.push((KEY[k] || humanize(k)) + " " + (k === "method" ? ((S.preparedFor(null) && PREP_WORD[v]) || WORD[v] || v) + (v === "code" ? " (not AI)" : "") : v));
524:  S.preparedFor = (id) => { const c = caseNow(), e = c && id ? [].concat(c.entries || [], c.undated_entries || []).find((x) => x.id === id) : null; return !!(e && e.prepared) || !!(c && c.models && c.models.generator_prepared); };
525:  S.allPrepared = (ids) => !!ids.length && ids.every((id) => S.preparedFor(id));
527:  S.HELD_NO_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ". The second AI check ran again and gave no answer on the new quote."
529:  S.HELD_CAN_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ", and the second AI check has no answer on the new quote."
532:  const heldWords = (held) => { const prep = S.allPrepared(held.map((b) => b.item_id)); return held.some((b) => !noAnswer(b)) ? S.HELD_CAN_RERUN(held.length, prep) : S.HELD_NO_RERUN(held.length, prep); };
585:      el("p", { class: "zs-legend" }, "✓ passed · ✕ failed or blocked · – skipped · ○ not done yet, or waiting for you. “Needs your decision” means the next move is yours. “Code” steps are done by a program, “You” steps are your decisions, and " + (S.preparedFor(null) ? "“Prepared answer” steps are
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:48.645Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; sed -n 524,531p $C/app/frontend/stepper.js | cut -c1-400; grep -n \"Loading the\\|preparedFor\\|allPrepared\" $C/app/frontend/judges.js | cut -c1-260"
}
````

### User / tool · 2026-11-03T01:19:48.747Z

**tool result**
````
  S.preparedFor = (id) => { const c = caseNow(), e = c && id ? [].concat(c.entries || [], c.undated_entries || []).find((x) => x.id === id) : null; return !!(e && e.prepared) || !!(c && c.models && c.models.generator_prepared); };
  S.allPrepared = (ids) => !!ids.length && ids.every((id) => S.preparedFor(id));
  const keepsWords = (n, prep) => (prep ? "the prepared wording" : "the AI's summary");
  S.HELD_NO_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ". The second AI check ran again and gave no answer on the new quote."
    : plural(n, "accepted entry keeps", "accepted entries keep") + " " + keepsWords(n, prep) + " under a quote you changed. The second AI check ran again and gave no answer on the new quotes.") + " Write the summary in your own words" + (n === 1 ? "." : " for each.");
  S.HELD_CAN_RERUN = (n, prep) => (n === 1 ? "You changed the quote on an accepted entry and kept " + keepsWords(n, prep) + ", and the second AI check has no answer on the new quote."
    : plural(n, "accepted entry keeps", "accepted entries keep") + " " + keepsWords(n, prep) + " under a quote you changed, and the second AI check has no answer on the new quotes.") + " Run the second check again, or write the summary in your own words.";
  // the one sentence for the held items of a gate: says what is left that can clear them
96:    const todo = tray ? TODO_TRAY : heldFinal(it) ? ZL.stepper.HELD_NO_RERUN(1, ZL.stepper.preparedFor(it.id)) : held(it) ? ZL.stepper.HELD_CAN_RERUN(1, ZL.stepper.preparedFor(it.id)) : blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u 
163:    const prepared = d && d.models ? !!d.models.generator_prepared : ZL.stepper.preparedFor(null);   // before the data arrives the case says whose answers they are      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing he
166:    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
189:      nHeld ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), ZL.stepper.HELD_NO_RERUN(nHeld, ZL.stepper.allPrepared(open.filter(heldFinal).map((i) => i.id)))) : null,
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:19:59.309Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; M=$S/T204_r2/mut; rm -rf $M; mkdir -p $M\ncat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T204_r2_mutate.py <<'EOF'\n\"\"\"T-204 r2 mutants (staff-engineer): python -I T204_r2_mutate.py <archive-root> <name>. Each puts one prepared-keyed fallback back to AI wording; asserts exactly one match.\"\"\"\nimport sys, pathlib\nroot, which = pathlib.Path(sys.argv[1]), sys.argv[2]\nM = {\n \"A_rail_held_words\": (\"app/frontend/stepper.js\", 'const keepsWords = (n, prep) => (prep ? \"the prepared wording\" : \"the AI\\'s summary\");', 'const keepsWords = (n, prep) => \"the AI\\'s summary\";'),\n \"B_rerun_button\": (\"app/frontend/stepper.js\", 'btn(S.preparedFor(null) ? \"Run the checks again\" : \"Run the AI steps again\"', 'btn(\"Run the AI steps again\"'),\n \"C_rail_legend\": (\"app/frontend/stepper.js\", '(S.preparedFor(null) ? \"“Prepared answer” steps are', '(false ? \"“Prepared answer” steps are'),\n \"D_judges_loading_prepared\": (\"app/frontend/judges.js\", 'const prepared = d && d.models ? !!d.models.generator_prepared : ZL.stepper.preparedFor(null);', 'const prepared = false;'),\n \"E_classic_banner\": (\"app/frontend/app.js\", 's.case && s.case.models && s.case.models.generator_prepared ? PREPARED_BANNER : (h && h.ai_banner)', '(h && h.ai_banner)'),\n}\nf, a, b = M[which]; p = root / f; s = p.read_text(); assert s.count(a) == 1, (which, s.count(a)); p.write_text(s.replace(a, b)); print(which, \"applied to\", f)\nEOF\nfor m in A_rail_held_words B_rerun_button C_rail_legend D_judges_loading_prepared E_classic_banner; do cp -R $C $M/$m; python3 -I artifacts/review-evidence/T204_r2_mutate.py $M/$m $m; done"
}
````

### User / tool · 2026-11-03T01:20:05.239Z

**tool result**
````
A_rail_held_words applied to app/frontend/stepper.js
B_rerun_button applied to app/frontend/stepper.js
C_rail_legend applied to app/frontend/stepper.js
D_judges_loading_prepared applied to app/frontend/judges.js
E_classic_banner applied to app/frontend/app.js
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:20:09.793Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=$S/T204_r2/mut; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nfor m in A_rail_held_words B_rerun_button; do echo \"== $m\"; (cd $M/$m && E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_prepared_first_paint.py -q -p no:cacheprovider 2>&1 | tail -4); done",
 "timeout": 400000
}
````

### User / tool · 2026-11-03T01:20:24.224Z

**tool result**
````
== A_rail_held_words
tests/e2e/test_prepared_first_paint.py:194: AssertionError
=========================== short test summary info ============================
FAILED tests/e2e/test_prepared_first_paint.py::test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai
1 failed, 4 passed in 5.85s
== B_rerun_button
.....                                                                    [100%]
5 passed in 6.60s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:20:29.321Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; M=$S/T204_r2/mut; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python\nfor m in C_rail_legend D_judges_loading_prepared E_classic_banner; do echo \"== $m\"; (cd $M/$m && E2E_REQUIRE_DB=1 $PY -m pytest tests/e2e/test_prepared_first_paint.py -q -p no:cacheprovider 2>&1 | tail -3); done",
 "timeout": 400000
}
````

### User / tool · 2026-11-03T01:20:52.251Z

**tool result**
````
== C_rail_legend
=========================== short test summary info ============================
FAILED tests/e2e/test_prepared_first_paint.py::test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai
1 failed, 4 passed in 6.65s
== D_judges_loading_prepared
=========================== short test summary info ============================
FAILED tests/e2e/test_prepared_first_paint.py::test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai
1 failed, 4 passed in 6.90s
== E_classic_banner
.....                                                                    [100%]
5 passed in 6.52s
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:20:56.627Z

**tool call — Bash**
````
{
 "command": "git log --oneline -1 679b63e^; git rev-parse HEAD; git merge-base --is-ancestor 679b63e HEAD && echo ancestor; git diff --cached --stat | tail -3; git status --short | head -8; git show 679b63e -- app/frontend/judges.js | grep \"^[-+]\" | cut -c1-300 | head -20"
}
````

### User / tool · 2026-11-03T01:20:56.853Z

**tool result**
````
b96c08f test(qa): T-208 letter_check fails any AI or model wording in every carrier letter (25 cases, prepared and live); matrix e2e binds the provenance line to the case kind
8aa14e1ecebed88c632204a914f252e26dea0c33
ancestor
 tests/e2e/test_prepared_first_paint.py | 142 ++-------------------------------
 tests/unit/test_t208_ai_wording.py     |  51 ++----------
 11 files changed, 55 insertions(+), 257 deletions(-)
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
--- a/app/frontend/judges.js
+++ b/app/frontend/judges.js
-    const todo = tray ? TODO_TRAY : heldFinal(it) ? ZL.stepper.HELD_NO_RERUN(1) : held(it) ? ZL.stepper.HELD_CAN_RERUN(1) : blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u ? (u && !r ? TODO_UNCHECKED : it.kind === "amount" ? TODO_AMOUNT : TODO_COMPARE) : null;
+    const todo = tray ? TODO_TRAY : heldFinal(it) ? ZL.stepper.HELD_NO_RERUN(1, ZL.stepper.preparedFor(it.id)) : held(it) ? ZL.stepper.HELD_CAN_RERUN(1, ZL.stepper.preparedFor(it.id)) : blk ? TODO_BLOCKED : mine ? null : waiting(it) ? TODO_PENDING : r || u ? (u && !r ? TODO_UNCHECKED : it.kind === 
-    const prepared = !!(d && d.models && d.models.generator_prepared);      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing here may say it was
+    const prepared = d && d.models ? !!d.models.generator_prepared : ZL.stepper.preparedFor(null);   // before the data arrives the case says whose answers they are      // D-065: a prepared (hand-checked) demo answer was not drafted by a model; nothing here may say it was
-      nHeld ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), ZL.stepper.HELD_NO_RERUN(nHeld)) : null,
+      nHeld ? el("p", { class: "zs-todo-text" }, el("strong", {}, "What you need to do: "), ZL.stepper.HELD_NO_RERUN(nHeld, ZL.stepper.allPrepared(open.filter(heldFinal).map((i) => i.id)))) : null,
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:20:59.347Z

**tool call — Bash**
````
{
 "command": "git diff --cached --name-status | head -14"
}
````

### User / tool · 2026-11-03T01:20:59.445Z

**tool result**
````
M	app/frontend/app.js
M	app/frontend/audit.js
M	app/frontend/guided/review.js
M	app/frontend/guided/step2.js
M	app/frontend/index.html
M	app/frontend/judges.js
M	app/frontend/stepper.js
M	app/frontend/timeline.js
M	evals/letter_check.py
M	tests/e2e/test_prepared_first_paint.py
M	tests/unit/test_t208_ai_wording.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:21:09.967Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; C=$S/T204_r2/clean; cat > $S/T204_r2/leakcheck.py <<'EOF'\nimport sys; sys.path.insert(0, sys.argv[1])\nimport tests.e2e.test_prepared_first_paint as t\nfor s in [\"The AI said: The prepared answers did not include it.\", \"The phrase list and the AI disagree\", \"Where code and the AI read an item differently (1 item)\", \"Summaries and warnings are drafted by AI and checked by code; you decide every item.\", \"The AI found it.\", \"the AI said The prepared answers did not include it.\", \"Drafted by an AI. x\"]:\n    print(repr(s), \"->\", \"LEAK\" if t._leaks([s]) else \"allowed\")\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/T204_r2/leakcheck.py $C; grep -n \"SECOND_CHECK = \\|r\\\"\\\\\\\\b(the )?AI (objected\" $C/tests/e2e/test_prepared_first_paint.py | cut -c1-80; grep -n \"on the \\[\" $C/tests/e2e/test_prepared_first_paint.py | cut -c1-60"
}
````

### User / tool · 2026-11-03T01:21:10.249Z

**tool result**
````
'The AI said: The prepared answers did not include it.' -> allowed
'The phrase list and the AI disagree' -> allowed
'Where code and the AI read an item differently (1 item)' -> allowed
'Summaries and warnings are drafted by AI and checked by code; you decide every item.' -> LEAK
'The AI found it.' -> allowed
'the AI said The prepared answers did not include it.' -> allowed
'Drafted by an AI. x' -> LEAK
151:SECOND_CHECK = [re.compile(p, re.I) for p in (
153:    r"\b(the )?AI (objected|agreed|did not check|could not (check|decide)|di
155:    r"independent of the (drafting )?model", r"on the [\
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:21:16.404Z

**tool call — Bash**
````
{
 "command": "grep -rln \"PREPARED_BANNER\" tests | head; grep -n \"wait_for_timeout\\|setInterval\" tests/e2e/test_prepared_first_paint.py | cut -c1-120"
}
````

### User / tool · 2026-11-03T01:21:16.529Z

**tool result**
````
21:  setInterval(scan, 20);
146:  setInterval(scan, 40);
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:21:58.080Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-204-staff-engineer-r2.md",
 "content": "# T-204 review — staff-engineer-reviewer (round 2), commit 679b63e\n\nVerdict: fail (one blocker, one major). The r1 blocker is fixed: my r1 probe (case rail and AI-check panel on the held prepared item) now passes, and mutating the rail's HELD wording back to \"the AI's summary\" fails the new document-wide walk. But AC 1 says \"for a prepared case no screen ever paints 'AI' wording\", and a second AI attribution is still on screen on the plain prepared sample: the AI-check panel row for the code-versus-prepared flag disagreement reads \"The AI said: The prepared answers did not include it.\" The new test's allow-list forgives it, so the green test cannot see it. The guided UI footer also paints \"drafted by AI\" for the prepared sample until /api/health answers.\n\n1. Commit content: `679b63e` has parent b96c08f and is an ancestor of HEAD (8aa14e1). It touches 9 files, all frontend plus the one test. The shared index again holds the pre-679b63e state of those 9 files (finding 5).\n2. r1 probe on a fresh `git archive 679b63e`: tests/e2e/test_prepared_first_paint.py 5 passed; my r1 probe (T204_probe_rail.py) 1 passed (rail_blockers, rail_all and judge_panel all empty of \"the AI's\").\n3. Exception 1, guided step 1 banner (`hl.ai_banner`, guided/step1.js:272): in demo mode with the curated set `/api/health` returns `answers=prepared` and `ai_banner = \"In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item\"`. The step 1 done screen printed exactly that, with the badge \"Prepared by our team\". It names an AI only for the real second check and says the summaries were prepared by the team, so it is accurate and acceptable as wording. Two caveats are in finding 4 (not keyed to the case; the sentence is copied in app.js:5).\n4. Exception 2, suggestions.js \"tested on the claude-cli backend\": the sentence is the server's calibration statement, built from `evals/reports/calibration.json` (`backend: claude-cli`, `case_count: 10`, `small_sample: true`, source_commit 312efe6, last touched by commit 7cfdb0b \"claude-cli 3-run at 312efe6 clean\"). Verified 82/83 and needs-review 11/11 come from that file. It appears in the closed \"Technical detail\" toggles (suggestions.js:142-155), not as a case answer. Accurate and acceptable as an evaluation statement. The allow-list regex that forgives it is wider than the sentence (finding 3).\n5. Mutation (asked item 3): mutant A, `keepsWords` always \"the AI's summary\" (stepper.js:526), fails `test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai` (1 failed, 4 passed). Mutant C (rail legend always the AI version, stepper.js:585) and D (judges loading label `prepared=false`, judges.js:163) are killed too. Mutant B (rerun button label back to \"Run the AI steps again\", stepper.js:338) survives, as does E (classic banner falls back to the server's string; equivalent on the test server because the server already sends the prepared sentence).\n\n```json\n{\"card\": \"T-204\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 679b63e (parent b96c08f, ancestor of HEAD 8aa14e1): app/frontend app.js, audit.js, guided/review.js, guided/step2.js, index.html, judges.js, stepper.js, timeline.js and tests/e2e/test_prepared_first_paint.py; fresh git archive 679b63e with private fixture-backend servers (curated set, ZLAYT_MODE=local); classic UI at /classic and guided UI at /; prepared sample case\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md, reviews/T-204-staff-engineer.md (r1), the card and handoff (board.py show T-204), my memory file project_t204_prepared_wording_patterns.md\",\n  \"git show --stat 679b63e (9 files); git log --oneline -1 679b63e^ = b96c08f; git merge-base --is-ancestor 679b63e HEAD: ancestor; git show 679b63e -- app/frontend judges.js and guided read\",\n  \"git archive 679b63e into a scratch dir; tests/e2e/test_prepared_first_paint.py with E2E_REQUIRE_DB=1: 5 passed; r1 probe artifacts/review-evidence/T204_probe_rail.py copied in as tests/e2e/test_probe_t204.py: passed (rail and judge panel empty of the AI's)\",\n  \"New probe artifacts/review-evidence/T204_r2_probe_guided.py (no allow-list; document-wide MutationObserver plus 30 ms innerText scan; guided home, step 1 done screen, step 2 timeline, step 3 bills, step 4 letter with the held accepted item; classic rail, AI-check panel, Why/trace/audit, export): guided 6 texts with AI/model words, classic 45; read every one\",\n  \"New probe artifacts/review-evidence/T204_r2_probe_narrow.py: P1 plain prepared sample, classic AI-check panel: fails with 'the AI said The prepared answers did not include it.', 'The phrase list and the AI disagree', 'Where code and the AI read an item differently (1 item)'; P2 guided UI with /api/health held: footer-note reads 'Summaries and warnings are drafted by AI and checked by code; you decide every item.' before health, the prepared sentence after\",\n  \"GET /api/health on the test server: answers=prepared demo_mode=True ai_banner='In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item'; case models {'generator': 'hand-checked (qa)', 'judge': 'claude-haiku-5-5', 'generator_prepared': True}\",\n  \"Called the new test's _leaks() directly (python -I script, scratch T204_r2/leakcheck.py): 'The AI said: The prepared answers did not include it.', 'The phrase list and the AI disagree', 'Where code and the AI read an item differently (1 item)' and 'The AI found it.' all return no leak\",\n  \"Mutants in separate archive copies (artifacts/review-evidence/T204_r2_mutate.py, grep-confirmed single match each): A keepsWords always AI, C rail legend always AI, D judges prepared=false: each 1 failed 4 passed; B rerun button label AI and E classic banner fallback: 5 passed (survive)\",\n  \"Read evals/reports/calibration.json (backend claude-cli, 10 cases, small_sample true, source_commit 312efe6) and suggestions.js 136-155 for exception 2; read guided/app.js 40-70, 111, 167 and guided/step1.js 262-275 for the banner and footer\",\n  \"git diff --cached --name-status in the shared repo: the 9 T-204 files and 2 T-208 files show as staged changes (index holds the pre-679b63e state)\",\n  \"Did not run the full tests/e2e (about 13 minutes); the card's 567/1/0 is the worker's claim, not re-run here\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"AC 1: no AI wording for a prepared case, every screen\": 2, \"r1 blocker fixed (rail, AI-check panel held item)\": 5, \"test strength (mutation)\": 3, \"allow-list precision\": 2, \"commit hygiene\": 4},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"AI-check panel still attributes a prepared flag disagreement to 'the AI' on the plain prepared sample, and the new test's allow-list forgives it\",\n   \"evidence\": \"app/frontend/judges.js:15 sources_disagree: \\\"The phrase list and the AI disagree\\\"; :75 and :101 kv(\\\"the AI said\\\", noCode(x.judge_says)) / \\\"The AI said: \\\"; :192 \\\"Where code and the AI read an item differently\\\". The server fills judge_says for a prepared flag with \\\"The prepared answers did not include it.\\\" (app/backend/trace.py:1096). Repro: cp artifacts/review-evidence/T204_r2_probe_narrow.py <git archive 679b63e>/tests/e2e/test_probe_t204_r2b.py; E2E_REQUIRE_DB=1 .venv/bin/python -m pytest tests/e2e/test_probe_t204_r2b.py::test_p1_plain_sample_panel -q -s. Output: AssertionError ['How the AI was checked', 'Where the AI objected (0 items)', 'Where code and the AI read an item differently (1 item)', 'The phrase list and the AI disagree... the code check said The phrase list found it.the AI said The prepared answers did not include it.']. This is the unedited prepared sample (no held item). The test passes because tests/e2e/test_prepared_first_paint.py:153 allows r\\\"\\\\b(the )?AI (objected|agreed|...|said|found|reads?|read|judge|disagree)\\\"; python -I leakcheck.py: _leaks(['The AI said: The prepared answers did not include it.']) is empty.\",\n   \"why_it_matters\": \"AC 1 and D-065/D-069: a prepared answer is never presented as the AI's. Here the side that omitted the flag is the prepared answers (the server says so), and the panel labels it 'The AI said' and 'the AI disagree'. The sentence contradicts itself on screen. It is the same class as r1 (provenance over-claim in static text on the AI-check panel), narrower in extent, and it sits in a place the green test is built to ignore. The card's claim that the panel shows no AI-attributing wording on the prepared sample is false.\",\n   \"fix\": \"Give the sources_disagree labels a prepared twin keyed by the case or item (the server already sends prepared sentences): 'The phrase list and the prepared answers disagree', 'The prepared answers said:', 'Where code and the prepared answers read an item differently'. Use ZL.stepper.preparedFor(item.id) as in judges.js:96. Tighten the allow-list so that 'AI said', 'AI found' and 'AI disagree' pass only when the line is about the real judge (for example require a judge verdict context), and add this panel to the walk with the plain sample as well as the held item.\",\n   \"acceptance_test\": \"Extend test_the_whole_classic_ui_never_attributes_a_prepared_answer_to_an_ai (or a sibling) to open the AI-check panel on the plain curated sample and assert no match of 'the AI said' / 'and the AI' beside 'prepared answers'; the probe above passes; mutate judges.js:101 back to 'The AI said: ' and confirm the test fails.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Guided UI footer paints 'drafted by AI' for the prepared sample until /api/health answers; the new test never visits the guided UI\",\n   \"evidence\": \"app/frontend/guided/app.js:46-48 G.provenance(): with G.store.health undefined `kind` is 'live' and the note is 'Summaries and warnings are drafted by AI and checked by code; you decide every item.'; drawBanner() is called at :111 (every route) and :167 (startup) before the health promise resolves (:69). Repro: T204_r2_probe_narrow.py::test_p2_guided_footer_before_health (health route held on a prepared sample case): P2 ('before health', 'Summaries and warnings are drafted by AI and checked by code; you decide every item.') then ('after health', '...Prepared by our team for this demo, not written by an AI model...'). The footer is on every guided screen. The test file's walk (test_the_whole_classic_ui_...) only drives the classic UI; its own _leaks() flags this exact sentence, but nothing feeds it from the guided page.\",\n   \"why_it_matters\": \"AC 1 says 'even transiently'. Until the server says whose answers they are, the page defaults to the live-AI sentence on every screen of the demo. If /api/health fails, the catch at app.js:69 leaves that sentence permanently. The window is short on a local server, but r1 already set the standard that a transient fallback counts.\",\n   \"fix\": \"Draw no provenance sentence until health has arrived (or default to a neutral line with no AI claim), in G.provenance() or drawBanner(). Add a guided walk: hold /api/health, assert the footer has no AI-attributing wording, release, assert the prepared sentence; then walk home, step 1 done, step 2, step 3, step 4 for the prepared sample with a document-wide observer.\",\n   \"acceptance_test\": \"test_p2_guided_footer_before_health passes; mutate drawBanner back to the 'live' default and confirm the test fails.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Allow-list is wider than the sentences it excuses; two fallbacks are not reached by the walk\",\n   \"evidence\": \"tests/e2e/test_prepared_first_paint.py:151-156: the verb list `AI (objected|agreed|...|said|found|reads?|read|judge|disagree)` forgives any 'the AI said/found/read/disagree' sentence, which is how finding 1 passes; `on the [\\\\w-]+ backend` forgives any backend name, not just 'claude-cli' with the calibration counts. Mutant B (stepper.js:338, 'Run the AI steps again' for 'Run the checks again') survives all 5 tests: the demo server never offers the rerun button, so the walk never paints it.\",\n   \"why_it_matters\": \"A closed list of excused phrases that is open-ended in its verbs lets the next AI-attributing sentence through (same lesson as r1: a universal claim proved by a closed list). Unpainted fallbacks are unguarded.\",\n   \"fix\": \"Pin the allow-list to whole sentences or to judge row contexts; pin the backend sentence to 'testing on the claude-cli backend (10 golden cases'. Cover the rerun paths with the LiveRerun/JudgeNotRun stubs the contract names, or assert the constants directly.\",\n   \"acceptance_test\": \"Mutant B fails a test; _leaks(['The AI said: The prepared answers did not include it.']) returns a leak.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Guided step 1 banner is the server's global string, not keyed to the case; the prepared sentence is copied in two places\",\n   \"evidence\": \"app/frontend/guided/step1.js:272 prints hl.ai_banner for every case, while guided/app.js:46-48 and review.js:70 key on the open case (models.generator_prepared === false gives 'recorded'); classic app.js:11 keys on the case. app/frontend/app.js:5 PREPARED_BANNER duplicates app/backend/api.py:39 ('same words as the server's'); grep -rl PREPARED_BANNER tests finds no test pinning the two. Read only; I did not build a case with generator_prepared=false on a prepared server.\",\n   \"why_it_matters\": \"On a prepared server a case written by a model would still read 'prepared by our team' on step 1, the opposite error (T-181 r2 noted this for the footer). A copied string drifts.\",\n   \"fix\": \"Derive the step 1 sentence from G.provenance() of the open case, and add a unit/e2e test that the client and server strings are equal (or drop the client copy).\",\n   \"acceptance_test\": \"A case stub with models.generator_prepared=false on a prepared server prints no 'prepared by our team' on step 1; a test fails if app.js:5 and api.py:39 differ.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Shared index again stages the pre-679b63e state of the card's files\",\n   \"evidence\": \"git diff --cached --name-status: M app/frontend/app.js, audit.js, guided/review.js, guided/step2.js, index.html, judges.js, stepper.js, timeline.js, tests/e2e/test_prepared_first_paint.py (plus evals/letter_check.py and tests/unit/test_t208_ai_wording.py). The staged diff of tests/e2e/test_prepared_first_paint.py is 142 lines, i.e. the reverse of the commit.\",\n   \"why_it_matters\": \"A commit without a pathspec would silently revert T-204 r2 and T-208 r2 (the r1 hazard, again).\",\n   \"fix\": \"Orchestrator: git reset -q -- those 11 paths after confirming nobody has real staged work there; commit by pathspec only.\",\n   \"acceptance_test\": \"git diff --cached --name-only is empty for those paths.\"}\n ],\n \"whats_right\": [\n  \"The r1 blocker is fixed with prepared twins keyed by item or case (S.preparedFor, keepsWords) and the document-wide observer walk kills the HELD wording, rail legend and judges loading-label mutants.\",\n  \"Fixed sleeps are gone: no wait_for_timeout in the test file; every wait is a condition (_until on animation frames).\",\n  \"Both named exceptions hold up as wording: the step 1 banner states 'prepared by our team' with the AI only for the real second check, and the claude-cli sentence is the measured calibration statement from evals/reports/calibration.json.\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-03T01:21:58.237Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-204-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:22:00.540Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport re,json;s=open('reviews/T-204-staff-engineer-r2.md').read();b=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',s,re.S);print(len(b));d=json.loads(b[0]);print(d['verdict'],[f['severity'] for f in d['findings']])\"; python3 tools/board.py --help 2>&1 | grep -i valid | head -3"
}
````

### User / tool · 2026-11-03T01:22:00.596Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:22:02.618Z

**tool call — Bash**
````
{
 "command": "cat > /private/tmp/claude-501/chk204.py <<'EOF'\nimport re, json\ns = open(\"/Users/arsis/zlayt-pm-project/reviews/T-204-staff-engineer-r2.md\").read()\nb = re.findall(r\"```json\\n(.*?)\\n```\", s, re.S)\nd = json.loads(b[0])\nprint(len(b), d[\"verdict\"], [f[\"severity\"] for f in d[\"findings\"]])\nEOF\npython3 -I /private/tmp/claude-501/chk204.py"
}
````

### User / tool · 2026-11-03T01:22:02.733Z

**tool result**
````
1 fail ['blocker', 'major', 'minor', 'minor', 'minor']
````

### Assistant · claude-sonnet-5-5 · 2026-11-03T01:22:08.007Z

Verdict: fail (1 blocker, 1 major). The JSON block parses; I did not run `board.py` validation. Review is at `/Users/arsis/zlayt-pm-project/reviews/T-204-staff-engineer-r2.md`.

- **Blocker:** on the unedited prepared sample, the classic AI-check panel still says "The AI said: The prepared answers did not include it." It also has "The phrase list and the AI disagree" and "Where code and the AI read an item differently" (`judges.js:15,75,101,192`). The new test's allow-list (`test_prepared_first_paint.py:153`) forgives these lines.
- **Major:** in the guided UI, the footer says "drafted by AI" for the prepared sample until `/api/health` answers (`guided/app.js:46-48`, `drawBanner` at 111 and 167). The new test never opens the guided UI.
- **r1 blocker fixed:** my old probe now passes on 679b63e. Mutating the rail's HELD wording back to "the AI's summary" makes the document-wide walk fail. Two other rail and panel mutants are also killed.
- **Mutants that survive:** the rerun-button label mutant (`stepper.js:338`) survives. The classic-banner fallback mutant also survives, but it is equivalent on the test server, which already sends the prepared sentence.
- **Step 1 banner:** in demo mode it reads "In this demo the sample summaries and flags were prepared by our team, then checked by code and by a second AI model; you decide every item". That is accurate and acceptable. Minor note: it is the server's global string, not keyed to the case.
- **"tested on the claude-cli backend":** the line is the server's calibration statement from `evals/reports/calibration.json` (claude-cli, 10 golden cases). It is accurate and acceptable. Minor: the allow-list regex behind it is wider than the sentence.
- **Shared index:** it again stages the pre-679b63e state of the card's files (minor).
- **Not run:** I did not re-run the full `tests/e2e`.

Probes and mutation script are in `artifacts/review-evidence/` as `T204_r2_probe_guided.py`, `T204_r2_probe_narrow.py` and `T204_r2_mutate.py`.
