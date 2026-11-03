# Subagent: T-141 fix-up scoped check (T-141 fix-up scoped check)

Source: `agent-a2ff4a3fe46077c5f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:37:57.994Z

This is a scoped check of the T-141 fix-up (commit 93a2ffc) in /Users/arsis/zlayt-pm-project. Read reviews/T-141-staff-engineer-r3.md and the orchestrator's §7.4 rule note on `python3 tools/board.py show T-141`.

On a `git archive HEAD` copy, verify only these:
- All 33 r3 variants behave per the rule. Generic negated or explicitly prior history is info-only; any reference to THE accident or its mechanism is a date conflict, even when another word is negated.
- lib11 is unchanged.
- The conflict suites pass.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-141-staff-engineer-r4.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:00.176Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:00.178Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r3.md"
}
````

### User / tool · 2026-11-02T14:38:00.189Z

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

### User / tool · 2026-11-02T14:38:00.189Z

**tool result**
````
1	# T-141 staff-engineer review, round 3 (ad8b7d1), Marcus Lee persona
2	
3	Verdict: **changes** (0 blockers, 1 major, 2 nits). The read-time notes, the no-summary rule and the mutant kills are all fixed and verified. The worker's deviation is the problem: "negated or plainly history stays info-only" is implemented as a bag-of-words window, and the window hides true date conflicts. 10 of my 33 fresh variants are real earlier-collision descriptions that come back info-only, and the note then says "No record names a collision, crash, accident, injury or similar in words of its own", which is false for each.
4	
5	Method: all probes ran on `git archive ad8b7d1` copies in the scratchpad (T141r3_head, T141r3_mut for mutants), not the dirty working tree. HEAD moved to 25f585c during the review (frontend and T-139 commits); `git diff --stat ad8b7d1 HEAD` over conflicts.py, conflict_candidates.py, present.py and the T-141 test files is empty, so ad8b7d1 is the T-141 state.
6	
7	## Answers to the brief
8	
9	1. **Does the deviation hide a true date conflict? Yes.** Scripts: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r3_scripts/r3_variants.py` (33 fresh variants). Each case is one record dated 2026-01-05, a PT visit 2026-01-12 and an intake "Date of accident per intake form: 2026-01-09".
10	   - Correct as the worker intended: `No prior accidents.`, `Denies MVC.`, `MVA in 2015, resolved.`, `History of MVA 2015.`, `Hx rear-end collision 2018.`, `MVA remote past`, `Fall risk screen negative.` all info-only. lib11 still has no date conflict.
11	   - Hidden true conflicts (info-only, should conflict): T1 `No LOC after the accident.`; T2 `Has not worked since the accident.`; T5 `No improvement since the crash.`; T6 `No airbag deployment in the collision.`; T7 `Without fracture after the MVC.`; T8 `Never lost consciousness during the crash.`; T10 `Negative for fracture after rear-end collision.`; H1 `History: rear-ended at a stoplight.`; H6 `Old man hit by a car crossing the street.`; H7 `Neck pain started years ago and worsened after the rear-end collision.` Cause: conflicts.py `_is_event_word` negates any event word with a negator in the five words before it, whatever sits between ("after", "since", "during", "in"); `_HIST_WORD` ("history", "old", "past") within three words counts as history even as a section label ("History:"); `_CLAUSE_HISTORY` makes the whole clause history when "years ago" appears anywhere in it.
12	   - Still conflict, correctly: T3, T4, T9, H2-H5, H8-H10, Y2, and all reviewer r2 variants V1-V3, V5-V8, V11, V16-V19, W3-W5, W9 (r2 variants rerun: 1 mismatch, V4, which is the intake-form self-contradiction I called right in round 2). Round-1 A-L: unchanged, B-H conflict, A, J, K, L quiet, I conflicts.
13	   - Safe-direction false positives (conflict where info is better): `Denies any motor vehicle collision or injury.` (the word "injury" is six words from "denies") and `Impact of diabetes on diet counselled.` The brief prefers these to hidden conflicts, so nit only.
14	2. **Notes at read time, refresh after confirm_date: fixed.** `r2_stale_checks.py` on the archive: ingested shows the predates note and no flag; after `review.confirm_date(.., '2026-03-06')` notes `[]` and flag `accident_date_after_treatment`. The note and the NO_DATED_RECORD count are computed in `checks(..., records)` from `store.load_records` (present.py case_view).
15	3. **No stored summary: fixed.** `r2_checks_matrix.py`: S5 (legacy ready) and S5b (legacy failed) report `ran=[]`, all four types skipped NOT_RUN, notes `[]`. A failed legacy case says NOT_RUN rather than RUN_FAILED; the reason text is honest about it.
16	   Other matrix rows are unchanged from round 2: ingested only, deadline at each stage, re-run in flight, lib09 partial Spanish (records 2, 4, 7), all-Spanish, crashed re-run RUN_FAILED (`r2_real_crash.py`).
17	4. **Mutants.** `r3_mutate.py` (32 mutants over conflicts.py, conflict_candidates.py, present.py, pipeline.py, with the r2 survivors): 31 of 31 applied mutants killed, 0 survived, plus the present.py "no records passed" mutant applied by hand (3 failed). The r2 survivors N6/N18 (old full date), P2 (run-start pending), P3, C7 (uncertain) and the word members t-bone, sideswipe, run over, airbag, seatbelt and 'vehicle'/'hit' replacements are all red now. Archive restored and diffed against the head copy (source files identical).
18	5. **Suites.** `tests/unit/test_conflicts.py test_conflict_candidates.py test_t093_j3_controls_reachable.py test_t141_checks_per_case.py test_t141_r3_variants.py test_t116_r4_all_dated_records.py test_api_routes.py` on the ad8b7d1 archive: 291 passed. 27-packet differential (`diff_packets.py`) between 68b8685 and ad8b7d1: identical, 27 accident-date result sets, sample still raises accident_date_after_treatment (2026-01-19). lib11 case view after a fixture run: two denial conflicts, no accident-date flag, note present.
19	
20	```json
21	{
22	 "card": "T-141",
23	 "persona": "staff-engineer-reviewer",
24	 "model": "claude-sonnet-5-5",
25	 "scope": "git ad8b7d1 (T-141 round 3, final) vs 68b8685; probes on git archives of ad8b7d1 and 68b8685 in the scratchpad (T141r3_head, T141r3_mut, T141r3_r2), never the dirty working tree; HEAD moved to 25f585c mid-review with no change to the T-141 files; fixture backend, no server started",
26	 "exercised": [
27	  "Read personas/staff-engineer.md, reviews/T-141-staff-engineer-r2.md, `python3 tools/board.py show T-141` (round-3 note, handoff), `git show ad8b7d1` for conflicts.py, conflict_candidates.py, present.py; `git rev-parse HEAD` = ad8b7d1 at start, 25f585c at end; `git diff --stat ad8b7d1 HEAD` over the T-141 files empty",
28	  "git archive ad8b7d1 into T141r3_head and T141r3_mut; git archive 68b8685 into T141r3_r2",
29	  "Reviewer r2 variants V1-V20 (r2_variants.py) and W1-W10 (r2_variants2.py) and round-1 A-L (probe2.py) on the r3 archive",
30	  "33 fresh variants (scratchpad T141r3_scripts/r3_variants.py): negations (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury), historical (MVA in 2015, History of MVA 2015, Hx rear-end collision 2018), negator-before-true-collision (T1-T10), history-word-before-true-collision (H1-H11), bare year and month-year (Y1-Y3), benign (B1-B3); r3_note.py for the note text on a hidden case",
31	  "Read-time notes: r2_stale_checks.py (ingest then review.confirm_date); checks matrix r2_checks_matrix.py (ingested, complete, deadline at each stage, re-run in flight, legacy rows with no run_checks, lib09, lib11, all-Spanish, defaults); r2_real_crash.py (crash in the conflict stage of a re-run)",
32	  "27-packet differential diff_packets.py 68b8685 vs ad8b7d1 (identical, sample accident-date conflict kept); r2_lib11.py case view after a fixture run",
33	  "Mutation: r3_mutate.py, 31 mutants on T141r3_mut (all killed), plus a manual present.py mutant (records not passed, 3 tests failed); archive diffed against T141r3_head after (source identical)",
34	  "pytest on the ad8b7d1 archive: 7 conflict and checks modules, 291 passed"
35	 ],
36	 "verdict": "changes",
37	 "scores": {
38	  "determinism": 5,
39	  "honest_failure": 4,
40	  "tests_assert_behaviour": 3,
41	  "llm_code_boundary": 5,
42	  "controls_discipline": 4
43	 },
44	 "findings": [
45	  {
46	   "severity": "major",
47	   "title": "Negated-or-history exemption hides true accident-date conflicts: 10 of 33 fresh variants where an earlier record describes the collision come back info-only, and the note says no record names a collision or injury",
48	   "evidence": "app/backend/conflicts.py `_is_event_word` (negator anywhere in the 5 words before the event word negates it, so prepositions between them do not stop it; `_HIST_WORD` includes 'history', 'old', 'past' within 3 words before, so a 'History:' label counts), `_CLAUSE_HISTORY` ('years ago' anywhere in the clause makes the whole clause history), `_describes_event` (all event words must fail). Repro on a git archive of ad8b7d1: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <archive>`; info-only but a real collision: T1 'No LOC after the accident.'; T2 'Has not worked since the accident.'; T5 'No improvement since the crash.'; T6 'No airbag deployment in the collision.'; T7 'Without fracture after the MVC.'; T8 'Never lost consciousness during the crash.'; T10 'Negative for fracture after rear-end collision.'; H1 'History: rear-ended at a stoplight.'; H6 'Old man hit by a car crossing the street.'; H7 'Neck pain started years ago and worsened after the rear-end collision.' (each as the only mention in a record dated 2026-01-05 with the stated accident date 2026-01-09; `accident_date_conflicts` returns [] and `accident_date_note` text reads: '1 record predates the stated accident date, January 9, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.', r3_note.py). Correctly still conflict: T3, T4, T9, H2-H5, H8-H10, Y2. 'No LOC after the accident' and 'has not worked since the accident' are among the commonest ER and follow-up phrasings, so this is not contrived.",
49	   "why_it_matters": "This is the same lost-conflict class as round-1 major 1 and round-2 major 1 (a deterministic R-FL-2 check becomes a word guess and a true discrepancy between the stated accident date and an earlier record disappears), now moved from 'wording the list misses' to 'wording the exemption over-reaches on'. The worker's reading of the Round 3 note (keep history and negation info-only so lib11 stays closed) is defensible, but the implementation negates the whole event instead of the noun the negator governs, and the note text then asserts the opposite of what the record says. Not a blocker for the same reason as rounds 1 and 2: it needs a stated accident date later than the earliest record plus one of these wordings, the record count is still surfaced as a note, and the loss is limited to the date-conflict flag, not an entry or a total.",
50	   "fix": "Scope the exemptions to the phrase they govern. (a) Negation: a negator only negates an event word when nothing but determiners, adjectives and event-noun modifiers sit between them ('no prior accidents', 'denies any motor vehicle collision', 'no recent injuries'); any of after, since, during, in, following, from, at, with, when, while, because, of between the two ends the scope. (b) History: 'history', 'hx', 'prior', 'previous', 'remote', 'old' count only immediately before the event noun or 'of <event>' ('prior accident', 'history of MVA', 'old MVC'), never when the word ends a label ('History:', 'History of present illness') or is followed by 'to'. (c) 'years ago', 'last year', 'as a child' make history only the sub-clause they sit in, split on 'and', 'but', 'worse', 'worsened', 'since', 'after'. (d) Reword the note so it says what was looked for and does not assert absence of injury: 'Records predate the stated accident date; none was read as describing a collision, so no date conflict is raised. Read them.'",
51	   "acceptance_test": "tests/unit/test_t141_r3_variants.py: T1, T2, T5, T6, T7, T8, T10, H1, H6, H7 each return one accident_date_after_treatment conflict; the info-only set (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury, MVA in 2015, History of MVA 2015, Hx rear-end collision 2018, Fall risk screen negative) and the lib11 shape still return []; mutants that widen the negator window back to 5 words regardless of prepositions are killed."
52	  },
53	  {
54	   "severity": "nit",
55	   "title": "Two safe-direction false positives: 'Denies any motor vehicle collision or injury' and 'Impact of diabetes on diet' still raise a date conflict",
56	   "evidence": "r3_variants.py N3 (conflict; 'injury' sits six words after 'denies', outside the 5-word window) and B2 (conflict; bare 'impact\\w*' in conflicts.py `_EVENT`). The paralegal can dismiss the conflict; nothing is lost.",
57	   "why_it_matters": "The Round 3 direction prefers a false positive to a hidden conflict, so this is not a defect. It does show the negation window is by word count, which is the cause of the major finding in the other direction.",
58	   "fix": "Fixing the major finding's negation scope (adjective list, not a word count) also closes N3; restrict 'impact' to 'impact with/of the collision' or 'on impact'.",
59	   "acceptance_test": "N3 returns [] and B2 returns [] in test_t141_r3_variants.py after the scope change."
60	  },
61	  {
62	   "severity": "nit",
63	   "title": "A bare year earlier than the record's own year always counts as history, so 'Rear-ended in 2025' in a record dated mid-2026 is info-only",
64	   "evidence": "conflicts.py `_clause_is_history` last line `int(y) < ry - (0 if rm > 2 else 1)`; r3_variants.py Y1 (record 2026-06-05 'Intake. Rear-ended in 2025.', stated 2026-06-09): info-only. Y3 'Rear-ended in October 2025' in a 2026-01-05 record is also info-only (three months, outside the two-month month-year window). Both are ambiguous rather than clearly wrong; lib11's '2019 and 2022' needs the rule.",
65	   "why_it_matters": "A bare year says nothing about whether the event is the index accident; within the last ~15 months it could be. Low likelihood, and the brief set the threshold as 'plainly history'.",
66	   "fix": "Treat a bare year as history only when it is at least two calendar years before the record's year, or when the clause also has a history marker.",
67	   "acceptance_test": "Y1 and Y3 conflict; lib11 (2019, 2022) and 'MVA in 2015' stay info-only."
68	  }
69	 ],
70	 "whats_right": [
71	  "Notes and the dated-record count are computed from the current records at GET time; confirm_date now moves the flag and the note together, and the stored run summary keeps only language, read count and stage.",
72	  "A case with no stored summary reports all four checks as NOT_RUN with an honest reason and conflict_types [], and the matrix (deadline at each stage, crashed re-run, partial and all-Spanish) still never claims a check that did not run.",
73	  "Mutant discipline: 31 of 31 mutants killed including every round-2 survivor (old full date, run-start pending, uncertain language, individual word-list members), and the 27-packet differential is identical to 68b8685 with the sample conflict kept."
74	 ],
75	 "questions_for_chris": []
76	}
77	```
78	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:00.308Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r3_patterns.md"
}
````

### User / tool · 2026-11-02T14:38:00.315Z

**tool result**
````
1	---
2	name: project_t141_r3_patterns
3	description: T-141 r3 ad8b7d1 changes — negator/history windows by word count hide true collisions (No LOC after the accident, History: rear-ended); read-time notes and no-summary fixed, 31/31 mutants killed
4	metadata:
5	  type: project
6	---
7	
8	T-141 r3 (ad8b7d1, verdict changes, 1 major 2 nits). Notes computed at read time, no-summary = NOT_RUN, r2 survivors all killed, 27-packet diff identical.
9	
10	- Open class: _is_event_word negates on a negator within 5 words before (prepositions after/since/during do not stop it) and counts "History:" / "old" / "past" within 3 words as history; "years ago" anywhere makes the whole clause history. 10 of 33 fresh variants hid a true collision. Note text asserted "no record names a collision/injury" (false).
11	- Method that worked: probe sets of "negator + preposition + event noun" (No LOC after the accident, has not worked since the accident, without fracture after the MVC) and "section label + event" (History: rear-ended). Always test the scope of a negation/history word, not only its presence.
12	- Mutants: write mutants against the NEW code (old patterns SKIP); a missing pattern prints SKIP, apply by hand.
13	- Stray write hazard: `cp file /tmp/x` when /tmp/x is an existing dir copies into it; use scratchpad paths only.
14	- HEAD moved mid-review: confirm with `git diff --stat <sha> HEAD -- <files>` that the card's files are unchanged.
15	
16	**How to apply:** for word-window rules ask whether the window crosses a preposition/verb; probe both directions (hidden and false positives).
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:00.712Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-141 && git log --oneline -5 && git cat-file -t 93a2ffc",
 "description": "Show T-141 card, recent log, and confirm commit 93a2ffc exists"
}
````

### User / tool · 2026-11-02T14:38:00.882Z

**tool result**
````
---
id: "T-141"
title: "GATE-M2 major: lib11 intake 'Prior accidents: No' vs PCP note listing 2019/2022 accidents not flagged as a conflict; a false accident-date 'records disagree' conflict is shown instead"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T13:03:00Z"
updated_at: "2026-11-02T14:37:57Z"
claimed_by: "backend"
claimed_at: "2026-11-02T14:24:21Z"
rounds: 3
commits: ["c4bb4da", "68b8685", "ad8b7d1", "93a2ffc"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer.md", "at": "2026-11-02T13:31:22Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer-r2.md", "at": "2026-11-02T14:04:00Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer-r3.md", "at": "2026-11-02T14:24:15Z"}
ac:
  - {"n": 1, "text": "lib11 raises the denial-vs-history conflict (intake form as the denial side, D-053/T-113 rules) and no false accident-date conflict; unit + library expected update with a written reason; controls unaffected", "done": true, "evidence": "r4: tests/unit/test_t141_r3_variants.py (33 reviewer r3 variants + scope tests) pass; conflict suites 352 pass; lib11 shape (A) stays info-only; full unit: 12 failures all in T-139 amounts/reclassify/trace (dirty amounts.py of another card), none in conflicts"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T13:03:19Z orchestrator: assigned: backend
- 2026-11-02T13:03:38Z backend: claimed
- 2026-11-02T13:10:21Z backend: Fix in conflict_candidates (form-field No denial, year-named prior accident), conflicts (accident-date corroboration), present/api.md (checks). Candidate diff vs HEAD across golden+library: only lib11 gains pairs, so no existing J3 control text changed (no live rerun). lib11 fixture: must flags 4/4, no accident-date conflict. Running full unit suite.
- 2026-11-02T13:16:59Z backend: AC 1 checked: tests/unit/test_conflict_candidates.py::test_t141_* + test_conflicts.py::test_t141_* pass; lib11 fixture run: must flags 4/4, no accident-date conflict, J3 live verdict conflict on both denial pairs; no existing control text changed (candidate diff vs HEAD only adds lib11 pairs)
- 2026-11-02T13:16:59Z backend: moved in_progress -> in_review
- 2026-11-02T13:17:14Z orchestrator: review dispatched: staff-engineer-reviewer, paralegal-reviewer
- 2026-11-02T13:31:22Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-141-staff-engineer.md; round 1; findings:
    - [major] Accident-date corroboration skip silently drops a true date conflict when the earliest record words the collision in a way its word list misses — fix: Do not drop. Either (a) widen _EVENT (hit, struck by, vehicle, motor vehicle, car, airbag, T-boned, side-swiped) and apply the _HISTORICAL / earlier-year exclusion to the clause that names the accident, not to the whole sentence, and t
    - [major] GET case `checks` is the same on every case, so a Spanish case, or a run whose conflicts stage was skipped, is still told 'checked for denial vs history' and 'plan vs early end' — fix: Make checks a function of the case: add `skipped: [{type, reason}]` (or move a type into not_checked) when records are lang 'es' for the two English-rule checks, when the conflicts stage was skipped or
    - [minor] The new denial rule has no topic restriction on its stem, and the year-named accident route has no negation or scope guard; the judge is the only filter and the controls do not cover those shapes — fix: Restrict _FORM_STEM/_FORM_ONE nouns to a closed list (accident, collision, injury, injuries, surgery, surgeries, condition, treatment, claim, back/neck problems); skip a prior sentenc
    - [minor] The live 3x controls run for J3R5, J3R6, J3R7 and J3V20 is owed and no card or owner exists; the changelog has no entry for the new rows — fix: Open a qa card for `LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --controls` (3 repeats) on a clean tree after the F-findings above land, so the rows for any new wrong controls run once; add the round entry to judge_controls.CHANG
    - [minor] A prior commit calls conflict_candidates.checks() before it exists: GET case raised AttributeError from T-143 until this commit — fix: No code change needed now. Stage with pathspec per file-ownership rule; if a hunk of another card is in the index, commit them together or leave it unstaged.
    - [minor] lib11 still shows two 'mentions a prior or pre-existing condition' flags whose quotes are only the form labels, beside the new conflicts (paralegal view) — fix: Suppress the lexicon pre_existing flag when the matched unit is a form stem answered No (the same _FORM_STEM + _FORM_NO test), or extend the quote to include the answer; show the two denial conflicts as one card with both quo
- 2026-11-02T13:31:22Z orchestrator: Round 2 direction: remove the 'skip a single stated date' rule (it hides true conflicts). Decide by content instead: a record dated before the stated accident date that does NOT describe a collision/injury mechanism is a prior record (shown as info 'N records predate the stated accident date', never a conflict); one that DOES describe the collision (hit from behind, MVA 12/30/2025, rear-ended...) is a date conflict, as before. Test with the reviewer's 6 variants. checks must reflect what ran for this case (language routing, skipped stages, failed runs): per-case, not a constant. The live 3x controls run is owned by the orchestrator's M2 confirming run.
- 2026-11-02T13:31:22Z orchestrator: assigned: backend
- 2026-11-02T13:31:30Z backend: claimed
- 2026-11-02T13:37:32Z orchestrator: Frontend T-142 (c5c18a6) already reads checks.conflict_types/labels/not_checked; make sure the per-case checks payload keeps that shape and document it in api.md.
- 2026-11-02T13:44:00Z backend: moved in_progress -> in_review
- 2026-11-02T13:44:07Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T14:04:00Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-141-staff-engineer-r2.md; round 2; findings:
    - [major] The 'describes a collision' test still loses true accident-date conflicts: 8 of 30 fresh variants where an earlier record names the collision come back info-only, and the note then says 'None describes a collision' — fix: (a) 'prior' / 'previously' / 'history' make a clause history only when they modify the event noun ('prior accident', 'history of MVA', 'previous collision'); 'prior
    - [major] `checks.notes` and the language/dated-record facts are a snapshot taken at run time; `confirm_date` recomputes the accident-date conflict live, so the case then shows a conflict flag and a note saying no conflict is raised — fix: Compute notes and the NO_DATED_RECORD condition at GET time from the current records (accident_date_note and the dated count are cheap and deterministic); s
    - [minor] Benign wording in an earlier record still produces a 'records disagree' accident-date conflict: negated mechanism words, 'last year', and 'vehicle' / 'hit' in other senses — fix: Skip a clause when a negator ('no', 'denies', 'without', 'negative for') precedes the event word within the clause; drop bare 'hit' and 'vehicle' in favour of 'hit by', 'struck', 'vehicle (accident|collision
    - [minor] Eight mutants survive: the old-full-date history branch, run-start 'pending', the 'uncertain' language rule and four word-list members are not pinned — fix: Add a unit test that crashes the conflict stage of a re-run (monkeypatch FL.run_conflict_pass to raise) and asserts RUN_FAILED; a test for 'Rear-end collision 03/14/2024, resolved.' being info-only; one test per word-list member 
    - [minor] A case with no stored run summary (created before this commit) claims every check ran, and a failed one with none sends an empty list to the UI fallback — fix: When no summary is stored, say so: return conflict_types [] and one skipped entry per type with reason_code UNKNOWN ('this case was analysed before per-case checks were recorded'); the frontend should render an empty list as '
    - [minor] Commit 68b8685 carries a T-139 test hunk without its code and is red at the commit: test_export_equals_golden_when_everything_accepted passes at the parent and fails at 68b8685 — fix: No change to T-141 code. Land the T-139 narrowing code (or revert that one test hunk) so HEAD is green; stage by pathspec per the file-ownership rule.
- 2026-11-02T14:04:00Z orchestrator: Round 3 (final) direction: invert the test. A pre-accident record is info-only ONLY when it has no injury/mechanism/accident vocabulary at all (routine/annual/wellness visit, paperwork); any of MVC/MVA/collision/crash/rear/pedestrian/struck/hit/accident/injury/whiplash/LOC/ER-for-trauma -> date conflict as before (a safe false positive beats a hidden conflict). Notes are computed at read time from current dates (not stored), so confirm_date refreshes them; no-summary case reports checks as not run. Test with the reviewer's 30 variants.
- 2026-11-02T14:04:00Z orchestrator: assigned: backend
- 2026-11-02T14:04:09Z backend: claimed
- 2026-11-02T14:19:25Z backend: AC 1 checked: r3: tests/unit/test_t141_r3_variants.py (30 reviewer variants + round-1 A-L + word-list table), test_t141_checks_per_case.py (read-time notes, no summary, crashed re-run) pass; conflict suites 288 pass; 27-packet diff vs HEAD identical (sample conflict kept); lib11 no date conflict, note present
- 2026-11-02T14:19:25Z backend: moved in_progress -> in_review
- 2026-11-02T14:19:36Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T14:24:15Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-141-staff-engineer-r3.md; round 3; findings:
    - [major] Negated-or-history exemption hides true accident-date conflicts: 10 of 33 fresh variants where an earlier record describes the collision come back info-only, and the note says no record names a collision or injury — fix: Scope the exemptions to the phrase they govern. (a) Negation: a negator only negates an event word when nothing but determiners, adjectives and event-noun modifiers
- 2026-11-02T14:24:15Z orchestrator: §7.4 at round cap: bounded fix-up + scoped check. Rule: a pre-accident record is info-only ONLY when its accident wording is generic prior history that is negated or explicitly prior ('no prior accidents', 'denies previous MVA', 'prior accidents: No'). Any reference to THE accident or its mechanism ('after/since the accident', 'the collision', 'rear-ended', 'struck', 'hit', 'MVC' without 'prior/previous') makes it a date conflict, even when other words are negated ('No LOC after the accident'). A false conflict is the safe direction (D-055). Test with the reviewer's 33 r3 variants; lib11 stays as accepted in r2.
- 2026-11-02T14:24:15Z orchestrator: assigned: backend
- 2026-11-02T14:24:21Z backend: claimed
- 2026-11-02T14:37:49Z backend: AC 1 checked: r4: tests/unit/test_t141_r3_variants.py (33 reviewer r3 variants + scope tests) pass; conflict suites 352 pass; lib11 shape (A) stays info-only; full unit: 12 failures all in T-139 amounts/reclassify/trace (dirty amounts.py of another card), none in conflicts
- 2026-11-02T14:37:49Z backend: moved in_progress -> in_review
- 2026-11-02T14:37:57Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Round 4 (93a2ffc, section 7.4 fix-up). What changed: conflicts.py only. A negator or history word governs an event word only by walking back over determiners/adjectives/compound nouns/other event words ('no prior accidents', 'denies any motor vehicle collision or injury', 'previous accident with whiplash'); 'the', prepositions, verbs, nouns, label colons ('History:') and 'prior to' end the walk, so 'No LOC after the accident', 'History: rear-ended' are conflicts. Year/date/'years ago' history is judged on the sub-clause around the event word (split at and/but/since/after/worsened). Also: bare year history needs >=2 calendar years before the record; 'impact' narrowed; note reworded (no assertion of absence). How verified: tests/unit/test_t141_r3_variants.py (reviewer's 33 variants + scope tests); conflict suites 352 pass; lib11 shape unchanged. Left: full unit has 12 failures from T-139 dirty amounts.py (not mine); e2e test_conflict_skipped fixture still has the old note text (frontend/qa fixture, harmless). Surprised: 'previous accident with whiplash' (existing r2 test) needed 'with' as walk-through word.

93a2ffc fix(backend): T-141 r4 accident-date: a pre-accident record is info-only only when its accident wording is negated or explicitly prior generic history; a negator or history word no longer reaches across the, prepositions, verbs or label colons (33 reviewer variants pinned)
d34182b docs(frontend): memory notes for T-144 and T-154
25f585c fix(frontend): T-136 r3 e2e private server that fails to start stops the run with its log; never falls back to :7860
b5f40c0 fix(frontend): T-151 empty checks.conflict_types says 'No conflict checks ran for this case' with the skipped reasons, never an empty list or 'No conflicts found'
4abec86 fix(backend): T-139 r2 money written without a dollar sign (TOTAL CHARGE 49100, AMOUNT PAID 0 00, 24F, FL47) is held out and caught by an independent letter check; Bills to request lists treating providers only; the held-out hint offers only actions that clear it
commit
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:25.652Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo \"HEAD=$(git rev-parse HEAD)\" && git log -1 --format='%h %s' 93a2ffc && git diff --stat ad8b7d1 93a2ffc && mkdir -p \"$SCR/T141r4_head\" && git archive HEAD | tar -x -C \"$SCR/T141r4_head\" && ls \"$SCR/T141r4_head\" && ls \"$SCR/T141r3_scripts/\" && ls -la reviews/ | grep T-141",
 "description": "Archive HEAD into scratchpad, diff commit range, list r3 variant scripts"
}
````

### User / tool · 2026-11-02T14:38:26.392Z

**tool result**
````
HEAD=93a2ffc8595e16d66257207a4a8c2c8a31c99b8f
93a2ffc fix(backend): T-141 r4 accident-date: a pre-accident record is info-only only when its accident wording is negated or explicitly prior generic history; a negator or history word no longer reaches across the, prepositions, verbs or label colons (33 reviewer variants pinned)
 .claude/agent-memory/frontend/project_uncovered.md |   4 +-
 app/backend/charge_text.py                         |  71 +++++-
 app/backend/conflicts.py                           |  70 ++++--
 app/backend/export.py                              |  40 +++-
 app/backend/why.py                                 |   2 +-
 app/frontend/batch.js                              |  11 +-
 app/frontend/charges.js                            |  37 ++-
 app/frontend/flags.js                              |  15 +-
 app/frontend/review.js                             |  10 +
 app/frontend/uncovered.css                         |   5 +-
 app/frontend/uncovered.js                          |  18 +-
 evals/letter_check.py                              |  37 ++-
 memory/contracts/api.md                            |   6 +-
 tests/e2e/conftest.py                              |  21 +-
 tests/e2e/test_charge_confirm.py                   | 182 +++++++++++++++
 tests/e2e/test_conflict_skipped.py                 |  33 +++
 tests/e2e/test_uncovered_ui.py                     |  54 +++--
 tests/unit/test_e2e_private_server.py              |  38 ++++
 tests/unit/test_t139_unmarked.py                   | 248 +++++++++++++++++++++
 tests/unit/test_t141_r3_variants.py                |  97 +++++++-
 20 files changed, 906 insertions(+), 93 deletions(-)
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
p_head.json
p_r2.json
r3_mutate.py
r3_note.py
r3_variants.py
-rw-r--r--@   1 arsis  staff   20224 Nov  2 08:02 T-141-staff-engineer-r2.md
-rw-r--r--@   1 arsis  staff   14397 Nov  2 08:23 T-141-staff-engineer-r3.md
-rw-r--r--@   1 arsis  staff   21273 Nov  2 07:31 T-141-staff-engineer.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:29.863Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' 93a2ffc && echo ---LIB11--- && grep -rl \"lib11\" --include=*.py --include=*.yaml --include=*.json --include=*.md . 2>/dev/null | grep -v \"^./.venv\" | head -30 && echo ---SCRIPT--- && cat \"$(dirname \"$0\")\" 2>/dev/null; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat \"$SCR/T141r3_scripts/r3_variants.py\"",
 "description": "Show T-141 commit files, locate lib11, read r3 variants script"
}
````

### User / tool · 2026-11-02T14:38:37.011Z

**tool result**
````
93a2ffc fix(backend): T-141 r4 accident-date: a pre-accident record is info-only only when its accident wording is negated or explicitly prior generic history; a negator or history word no longer reaches across the, prepositions, verbs or label colons (33 reviewer variants pinned)

 app/backend/conflicts.py            | 70 ++++++++++++++++++--------
 tests/unit/test_t141_r3_variants.py | 97 +++++++++++++++++++++++++++++++++++--
 2 files changed, 141 insertions(+), 26 deletions(-)
---LIB11---
research/case-library-sources-v2.md
artifacts/review-evidence/T-120-r2-paralegal-probe.py
artifacts/review-evidence/T-120-r4-probe.py
artifacts/review-evidence/T-116-paralegal-lib11-apply.py
artifacts/review-evidence/T-118-paralegal-mutB.py
artifacts/review-evidence/T-118-paralegal-lib11-view.py
artifacts/review-evidence/T-120-r4-http-library-parent-0c47356.json
artifacts/review-evidence/T-114-paralegal-api-checks.out.json
artifacts/review-evidence/T-046-ux-designer-r2-overlay-selected-results.json
artifacts/review-evidence/T-120-r3-paralegal-draft.json
artifacts/review-evidence/T-060-accessibility-pass2-audit-results.json
artifacts/review-evidence/T-116-paralegal-r2-f3-lib11.py
artifacts/review-evidence/T-120-r4-http-library-head-a44dced.json
artifacts/review-evidence/T-046-ux-designer-r2-overlay-results.json
artifacts/review-evidence/T-060-accessibility-audit-results.json
artifacts/review-evidence/T-046-ux-designer-r2-results.json
artifacts/review-evidence/T-060-accessibility-pass3-audit-results.json
artifacts/review-evidence/T-123-paralegal-survey.out.json
artifacts/review-evidence/T-120-r2-http-HEAD-433ac1c.json
artifacts/review-evidence/T-120-123-paralegal-probe.py
artifacts/review-evidence/T-120-r4-draft.md
artifacts/review-evidence/T-120-paralegal-draft.md
artifacts/review-evidence/T-116-paralegal-r3-compare.py
artifacts/review-evidence/T-079-paralegal-r2-check.py
artifacts/review-evidence/T-116-paralegal-r2-packets-compare.py
artifacts/review-evidence/T-060-accessibility-pass2-explore.json
artifacts/review-evidence/T-123-paralegal-sample-compare.py
artifacts/review-evidence/T-120-r3-http-HEAD-f7829c1.json
artifacts/review-evidence/T-120-123-paralegal-probe.out.json
artifacts/review-evidence/T-060-accessibility-tabwalk-from-top.json
---SCRIPT---
import sys
root = sys.argv[1]; sys.path.insert(0, root)
from app.backend import conflicts as C
def R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")
INT = lambda n, d, date: R(n, d, "Intake", f"Date of accident per intake form: {date}.")
def case(ex, d="2026-01-05"):
    return [R(1,d,"ER",ex), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]
# (label, expected, excerpt)  conflict = a real earlier-collision description a paralegal must see
X = [
 # negations the brief names
 ("N1 'No prior accidents' (history/negated)", "info", "Annual physical. No prior accidents."),
 ("N2 'Denies MVC'", "info", "Annual physical. Denies MVC."),
 ("N3 'Denies any motor vehicle collision or injury'", "info", "Annual physical. Denies any motor vehicle collision or injury."),
 ("N4 'MVA in 2015'", "info", "Annual physical. MVA in 2015, resolved."),
 ("N5 'History of MVA 2015'", "info", "Annual physical. History of MVA 2015."),
 ("N6 'Hx: rear-end collision 2018'", "info", "Annual physical. Hx rear-end collision 2018."),
 # negator window hides a TRUE collision
 ("T1 'No LOC after the accident'", "conflict", "ER visit. No LOC after the accident. Neck pain."),
 ("T2 'Has not worked since the accident'", "conflict", "Follow-up. Has not worked since the accident. Neck pain."),
 ("T3 'No relief of neck pain since the MVA'", "conflict", "Follow-up. No relief of neck pain since the MVA."),
 ("T4 'Patient was not wearing a seatbelt in the rear-end collision'", "conflict", "ER visit. Patient was not wearing a seatbelt in the rear-end collision."),
 ("T5 'Unable to drive, no improvement after the crash'", "conflict", "Follow-up. No improvement since the crash."),
 ("T6 'No airbag deployment in the collision' (airbag negated, collision 4 words after 'no')", "conflict", "ER visit. No airbag deployment in the collision. Neck pain."),
 ("T7 'Without fracture after the MVC'", "conflict", "ER visit. Without fracture after the MVC."),
 ("T8 'Never lost consciousness during the crash'", "conflict", "ER visit. Never lost consciousness during the crash."),
 ("T9 'No other injuries; was in an MVA' (semicolon ok)", "conflict", "ER visit. No other injuries; was in an MVA."),
 ("T10 'Negative for fracture after rear-end collision'", "conflict", "ER visit. Negative for fracture after rear-end collision."),
 # history word window hides a TRUE collision
 ("H1 'History: rear-ended at a stoplight'", "conflict", "ER visit. History: rear-ended at a stoplight. Neck pain."),
 ("H2 'Neck pain for the past week since the MVA'", "conflict", "Chiro visit. Neck pain for the past week since the MVA."),
 ("H3 'History of present illness: MVC today'", "conflict", "ER visit. History of present illness: MVC today."),
 ("H4 'Earlier today the pt was in an MVA' ", "conflict", "ER visit. Earlier today the pt was in an MVA. Neck pain."),
 ("H5 'Past medical history none. Pt in MVC'", "conflict", "ER visit. PMH none; pt in MVC this week."),
 ("H6 'Old man hit by a car'", "conflict", "ER visit. Old man hit by a car crossing the street."),
 ("H7 'Neck pain started a few years ago, worse after rear-end collision' (years ago in same clause)", "conflict", "Chiro visit. Neck pain started years ago and worsened after the rear-end collision."),
 ("H8 'last year' + this-week event same clause", "conflict", "ER visit. Seen last year for knee, now rear-ended this week."),
 ("H9 'Prior to arrival, pt was in MVC' (not hist)", "conflict", "ER visit. Prior to arrival the patient was in an MVC. Neck pain."),
 ("H10 'previous visit ... MVA' ", "conflict", "Follow-up. At the previous visit she reported the MVA and neck pain."),
 ("H11 'remote' wording fine: 'MVA remote past' ", "info", "Annual physical. MVA remote past, resolved."),
 # bare years / month-year
 ("Y1 'MVA in 2025' record dated 2026-06, stated later", "conflict_late", "Intake. Rear-ended in 2025."),
 ("Y2 'rear-ended in November 2025' record 2026-01-05", "conflict", "ER visit. Rear-ended in November 2025."),
 ("Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)", "conflict_or_info", "ER visit. Rear-ended in October 2025."),
 # benign wording
 ("B1 'Fall risk screen negative'", "info", "Annual physical. Fall risk screen negative."),
 ("B2 'Impact of diabetes on diet counselled'", "info", "Annual physical. Impact of diabetes on diet counselled."),
 ("B3 'Injury prevention handout given'", "conflict_ok", "Annual physical. Injury prevention handout given."),
]
for label, exp, ex in X:
    recs = case(ex, "2026-06-05" if label.startswith("Y1") else "2026-01-05")
    if label.startswith("Y1"):
        recs = [R(1,"2026-06-05","ER",ex), R(2,"2026-06-12","PT","Exam: ok."), INT(3,"2026-06-20","2026-06-09")]
    out = C.accident_date_conflicts(recs)
    got = "conflict" if out else "info"
    print(f"{got:9} exp={exp:16} | {label}")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:38:56.203Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && mkdir -p \"$SCR/T141r4_prev\" && git archive ad8b7d1 | tar -x -C \"$SCR/T141r4_prev\" && echo \"== NEW (93a2ffc) ==\" && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I \"$SCR/T141r3_scripts/r3_variants.py\" \"$SCR/T141r4_head\" && echo \"== PREV (ad8b7d1) control ==\" && PYTHONDONTWRITEBYTECODE=1 .venv/bin/python -I \"$SCR/T141r3_scripts/r3_variants.py\" \"$SCR/T141r4_prev\"",
 "description": "Run the 33 r3 variants on the new archive and the prior-round control"
}
````

### User / tool · 2026-11-02T14:38:57.262Z

**tool result**
````
== NEW (93a2ffc) ==
info      exp=info             | N1 'No prior accidents' (history/negated)
info      exp=info             | N2 'Denies MVC'
info      exp=info             | N3 'Denies any motor vehicle collision or injury'
info      exp=info             | N4 'MVA in 2015'
info      exp=info             | N5 'History of MVA 2015'
info      exp=info             | N6 'Hx: rear-end collision 2018'
conflict  exp=conflict         | T1 'No LOC after the accident'
conflict  exp=conflict         | T2 'Has not worked since the accident'
conflict  exp=conflict         | T3 'No relief of neck pain since the MVA'
conflict  exp=conflict         | T4 'Patient was not wearing a seatbelt in the rear-end collision'
conflict  exp=conflict         | T5 'Unable to drive, no improvement after the crash'
conflict  exp=conflict         | T6 'No airbag deployment in the collision' (airbag negated, collision 4 words after 'no')
conflict  exp=conflict         | T7 'Without fracture after the MVC'
conflict  exp=conflict         | T8 'Never lost consciousness during the crash'
conflict  exp=conflict         | T9 'No other injuries; was in an MVA' (semicolon ok)
conflict  exp=conflict         | T10 'Negative for fracture after rear-end collision'
conflict  exp=conflict         | H1 'History: rear-ended at a stoplight'
conflict  exp=conflict         | H2 'Neck pain for the past week since the MVA'
conflict  exp=conflict         | H3 'History of present illness: MVC today'
conflict  exp=conflict         | H4 'Earlier today the pt was in an MVA' 
conflict  exp=conflict         | H5 'Past medical history none. Pt in MVC'
conflict  exp=conflict         | H6 'Old man hit by a car'
conflict  exp=conflict         | H7 'Neck pain started a few years ago, worse after rear-end collision' (years ago in same clause)
conflict  exp=conflict         | H8 'last year' + this-week event same clause
conflict  exp=conflict         | H9 'Prior to arrival, pt was in MVC' (not hist)
conflict  exp=conflict         | H10 'previous visit ... MVA' 
info      exp=info             | H11 'remote' wording fine: 'MVA remote past' 
conflict  exp=conflict_late    | Y1 'MVA in 2025' record dated 2026-06, stated later
conflict  exp=conflict         | Y2 'rear-ended in November 2025' record 2026-01-05
info      exp=conflict_or_info | Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)
info      exp=info             | B1 'Fall risk screen negative'
info      exp=info             | B2 'Impact of diabetes on diet counselled'
conflict  exp=conflict_ok      | B3 'Injury prevention handout given'
== PREV (ad8b7d1) control ==
info      exp=info             | N1 'No prior accidents' (history/negated)
info      exp=info             | N2 'Denies MVC'
conflict  exp=info             | N3 'Denies any motor vehicle collision or injury'
info      exp=info             | N4 'MVA in 2015'
info      exp=info             | N5 'History of MVA 2015'
info      exp=info             | N6 'Hx: rear-end collision 2018'
info      exp=conflict         | T1 'No LOC after the accident'
info      exp=conflict         | T2 'Has not worked since the accident'
conflict  exp=conflict         | T3 'No relief of neck pain since the MVA'
conflict  exp=conflict         | T4 'Patient was not wearing a seatbelt in the rear-end collision'
info      exp=conflict         | T5 'Unable to drive, no improvement after the crash'
info      exp=conflict         | T6 'No airbag deployment in the collision' (airbag negated, collision 4 words after 'no')
info      exp=conflict         | T7 'Without fracture after the MVC'
info      exp=conflict         | T8 'Never lost consciousness during the crash'
conflict  exp=conflict         | T9 'No other injuries; was in an MVA' (semicolon ok)
info      exp=conflict         | T10 'Negative for fracture after rear-end collision'
info      exp=conflict         | H1 'History: rear-ended at a stoplight'
conflict  exp=conflict         | H2 'Neck pain for the past week since the MVA'
conflict  exp=conflict         | H3 'History of present illness: MVC today'
conflict  exp=conflict         | H4 'Earlier today the pt was in an MVA' 
conflict  exp=conflict         | H5 'Past medical history none. Pt in MVC'
info      exp=conflict         | H6 'Old man hit by a car'
info      exp=conflict         | H7 'Neck pain started a few years ago, worse after rear-end collision' (years ago in same clause)
conflict  exp=conflict         | H8 'last year' + this-week event same clause
conflict  exp=conflict         | H9 'Prior to arrival, pt was in MVC' (not hist)
conflict  exp=conflict         | H10 'previous visit ... MVA' 
info      exp=info             | H11 'remote' wording fine: 'MVA remote past' 
info      exp=conflict_late    | Y1 'MVA in 2025' record dated 2026-06, stated later
conflict  exp=conflict         | Y2 'rear-ended in November 2025' record 2026-01-05
info      exp=conflict_or_info | Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)
info      exp=info             | B1 'Fall risk screen negative'
conflict  exp=info             | B2 'Impact of diabetes on diet counselled'
conflict  exp=conflict_ok      | B3 'Injury prevention handout given'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:39:14.435Z

**tool call — Bash**
````
{
 "command": "git show 93a2ffc -- app/backend/conflicts.py",
 "description": "Show the T-141 r4 diff to conflicts.py"
}
````

### User / tool · 2026-11-02T14:39:14.544Z

**tool result**
````
commit 93a2ffc8595e16d66257207a4a8c2c8a31c99b8f
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:37:41 2026 -0600

    fix(backend): T-141 r4 accident-date: a pre-accident record is info-only only when its accident wording is negated or explicitly prior generic history; a negator or history word no longer reaches across the, prepositions, verbs or label colons (33 reviewer variants pinned)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/conflicts.py b/app/backend/conflicts.py
index 226eecb..64cbf12 100644
--- a/app/backend/conflicts.py
+++ b/app/backend/conflicts.py
@@ -9,24 +9,29 @@ from app.backend.ingest import evidence_span
 PHRASE_TO_DATE_CHARS = 40
 
 # T-141 r2/r3 (GATE-M2 lib11): the content decides, not a coinciding date. A stated accident date later than the earliest record is a conflict when a record
-# dated before it has any clause with injury, mechanism or accident vocabulary that is not clearly history or negated (a safe false positive beats a hidden
-# conflict). Only a record with none (a routine or annual visit, paperwork) or whose every such clause is plainly history ("car accidents in 2019 and 2022",
-# "Hx of MVA", "denies any accidents") is an earlier visit: the case notes how many (accident_date_note), nothing is raised.
+# dated before it has any clause with injury, mechanism or accident vocabulary that is not generic prior history (a safe false positive beats a hidden
+# conflict). Only a record with none (a routine or annual visit, paperwork) or whose every such word is generic history, negated or explicitly prior
+# ("car accidents in 2019 and 2022", "Hx of MVA", "no prior accidents", "denies any accidents"), is an earlier visit: the case notes how many
+# (accident_date_note), nothing is raised. T-141 r4 (section 7.4): a negator or history word governs only the event noun it directly modifies, through
+# determiners, adjectives and event words ("no recent injuries", "denies any motor vehicle collision or injury"); it never reaches across "the", a preposition,
+# a verb or a label colon, so "No LOC after the accident" and "History: rear-ended" still refer to the accident and are conflicts.
 _EVENT = re.compile(r"\b(?:collision|collided|crash\w*|MVA|MVC|MVI|rear[- ]?end\w*|struck|wreck\w*|accident\w*|incident|pedestrian|motor\s+vehicle|vehicular|"
                     r"hit\s+by|(?:was|were|got)\s+hit|(?:vehicle|car|truck|driver)\s+hit|hit\s+(?:them|him|us|me)|"
                     r"hit\s+(?:a|the|my|our)\s+(?:car|vehicle|truck|pole|tree|wall|guardrail|curb)|"
                     r"airbag\w*|seat\s?belt\w*|t-?bone\w*|side-?swip\w*|(?:run|ran)\s+over|run-over|"
-                    r"fell|fall(?:ing)?\s+(?:from|off|down)|slip(?:ped)?\s+and\s+fall|whiplash|injur\w*|trauma\w*|impact\w*|LOC|loss\s+of\s+consciousness)\b", re.I)
+                    r"fell|fall(?:ing)?\s+(?:from|off|down)|slip(?:ped)?\s+and\s+fall|whiplash|injur\w*|trauma\w*|impact(?:ed)?\s+(?:with|to|from|on\s+the)|on\s+impact|impacted|LOC|loss\s+of\s+consciousness)\b", re.I)
 _NEGATOR = {"no", "not", "denies", "denied", "denying", "without", "never", "negative", "neg", "none", "nor", "free"}
 _HIST_WORD = {"prior", "previous", "remote", "past", "earlier", "old", "hx", "history"}              # history only when it modifies the event noun, not "prior to"
-_HIST_ADVERB = re.compile(r"\bpreviously\s+(?:had|reported|involved|in|was|suffered)\s+(?:\w+\s+){0,3}$", re.I)
+_HIST_VERBS = {"had", "suffered", "been", "involved", "in", "was"}                                      # "previously had an MVA"; not "previously reported the MVA"
+_FILLER = {"a", "an", "any", "all", "some", "other", "further", "known", "recent", "major", "minor", "serious", "significant", "new", "or", "and", "of", "for",
+           "motor", "vehicle", "vehicular", "car", "auto", "traffic", "head", "neck", "back", "rear", "end", "with"}      # words a negator or history word may reach through to the event noun ('previous accident with whiplash')
+_SUBCLAUSE = re.compile(r"\b(?:and|but|then|now|since|after|following|while|when|because|worse(?:ned|ns)?)\b", re.I)
 _CLAUSE_HISTORY = re.compile(r"\b(?:years?\s+ago|last\s+year|as\s+a\s+child|remote(?:ly)?)\b", re.I)
 _YEAR = re.compile(r"\b(19\d\d|20\d\d)\b")
 _MODEL_YEAR = re.compile(r"\b(?:19|20)\d\d(?=\s+[A-Z][a-z])")
 _MONTH_YEAR = re.compile(r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?,?\s+((?:19|20)\d\d)\b", re.I)
 _MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
 _CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")
-_NEG_WINDOW, _HIST_WINDOW = 5, 3
 
 
 def _days_between(a: str, b: str):
@@ -40,7 +45,7 @@ def _days_between(a: str, b: str):
 def _clause_is_history(clause: str, stated: str, rec_iso: str) -> bool:
     """The clause as a whole dates itself to the past: 'last year', 'N years ago', 'as a child', a full date more than a year before the STATED date (a full
     date within the year before is a possible index event: MVA 12/30/2025 against a stated 2026-01-05), a month and year more than two months before the RECORD's
-    own date, or a bare year before the record's year (the year before it only when the record is not in January or February). A model year ('a 2019 Honda') is
+    own date, or a bare year at least two calendar years before the record's year (last year is a possible index event). A model year ('a 2019 Honda') is
     not a date."""
     if _CLAUSE_HISTORY.search(clause):
         return True
@@ -56,20 +61,42 @@ def _clause_is_history(clause: str, stated: str, rec_iso: str) -> bool:
         if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2:
             return True
     rest = _MODEL_YEAR.sub("    ", _MONTH_YEAR.sub("    ", rest))
-    return any(int(y) < ry - (0 if rm > 2 else 1) for y in _YEAR.findall(rest))
+    return any(int(y) <= ry - 2 for y in _YEAR.findall(rest))
 
 
-def _is_event_word(clause: str, m) -> bool:
-    """One vocabulary match in a clause counts as an event unless a negator stands within five words before it ('denies any accidents', 'no recent injuries')
-    or a history word modifies it within three words before it ('prior accident', 'history of MVA'; not 'prior to the collision')."""
-    pre = clause[:m.start()]
-    words = [w.strip(".:()\"'").lower() for w in pre.split()]
-    if any(w in _NEGATOR for w in words[-_NEG_WINDOW:]):
-        return False
-    tail = words[-_HIST_WINDOW:]
-    if any(w in _HIST_WORD and not (i + 1 < len(tail) and tail[i + 1] == "to") for i, w in enumerate(tail)):
+def _governed(clause: str, m) -> bool:
+    """The event word is generic history when a negator or a history word governs it: walk back from it over determiners, adjectives, the nouns of a compound
+    ('motor vehicle collision') and other event words; reaching a negator ('no prior accidents', 'denies any collision or injury') or a history word ('prior
+    accident', 'history of MVA', 'previously had an MVA') ends the walk as history. Anything else ('the', a preposition, a verb, a noun, a label colon, 'prior to')
+    ends it as a reference to the accident itself."""
+    toks = clause[:m.start()].split()
+    for i in range(len(toks) - 1, -1, -1):
+        raw = toks[i]
+        w = raw.strip(".:()\"'?[]").lower()
+        if raw.endswith(":") or not w:                                                    # a label ("History:", "Allergies:") closes the scope
+            return False
+        if w in _NEGATOR:
+            return True
+        if w in _HIST_WORD:
+            return True
+        if w in _HIST_VERBS and i and any(t.strip(".:()\"'?[]").lower() == "previously" for t in toks[max(0, i - 2):i]):
+            return True
+        if w in _FILLER or _EVENT.fullmatch(w):
+            continue
         return False
-    return not _HIST_ADVERB.search(pre)
+    return False
+
+
+def _subclause(clause: str, pos: int) -> str:
+    """The part of the clause around the event word, cut at 'and', 'but', 'since', 'after', 'worsened'...: a date or 'years ago' elsewhere in the clause is not about it."""
+    start, end = 0, len(clause)
+    for c in _SUBCLAUSE.finditer(clause):
+        if c.end() <= pos:
+            start = c.end()
+        elif c.start() >= pos:
+            end = c.start()
+            break
+    return clause[start:end]
 
 
 def _describes_event(rec: dict, stated: str) -> bool:
@@ -81,8 +108,9 @@ def _describes_event(rec: dict, stated: str) -> bool:
         for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
             unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
         for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
-            if any(_is_event_word(clause, m) for m in _EVENT.finditer(clause)) and not _clause_is_history(clause, stated, rec["date_iso"]):
-                return True
+            for m in _EVENT.finditer(clause):
+                if not _governed(clause, m) and not _clause_is_history(_subclause(clause, m.start()), stated, rec["date_iso"]):
+                    return True
     return False
 
 
@@ -181,7 +209,7 @@ def accident_date_note(records: list):
     n = len(before)
     lead = f"{n} record predates" if n == 1 else f"{n} records predate"
     return {"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": n, "record_nos": [r["n"] for r in before], "stated_date": iso,
-            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."}
+            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. None was read as describing the collision itself, so no date conflict is raised; read them to check they are earlier care."}
 
 
 _TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:39:45.962Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && echo \"--- lib11 tracked paths ---\" && git ls-files | grep -i 'lib11' ; echo \"--- lib11 diff ad8b7d1..HEAD (paths) ---\"; git diff --stat ad8b7d1 HEAD -- $(git ls-files | grep -i 'lib11') ; echo \"(end)\"; echo \"--- lib11 mentions in T-141 test ---\"; grep -n \"lib11\" \"$SCR/T141r4_head/tests/unit/test_t141_r3_variants.py\" | head; echo \"--- Y3/month-year test pins in r4 test ---\"; grep -n \"October 2025\\|Y3\\|Y1\" \"$SCR/T141r4_head/tests/unit/test_t141_r3_variants.py\" | head",
 "description": "Locate lib11 files, check they are untouched, find lib11 and Y3 pins"
}
````

### User / tool · 2026-11-02T14:39:46.115Z

**tool result**
````
--- lib11 tracked paths ---
evals/library/case_lib11_priors_and_ledger.expected.json
evals/library/case_lib11_priors_and_ledger.txt
--- lib11 diff ad8b7d1..HEAD (paths) ---
(end)
--- lib11 mentions in T-141 test ---
48:    ("A lib11 shape", "info", [R(1, "2026-03-04", "PCP", "Annual visit. Car accidents in 2019 and 2022."), R(2, "2026-03-18", "EMS", "Passenger vehicle struck from behind."), R(3, "2026-03-27", "Intake", "Date of injury: 2026-03-18.")]),
112:    """T-141 r4 (reviewer Y1): a bare year says nothing about whether it is the index accident within the last ~15 months. 2019 and 2022 (lib11) stay history."""
--- Y3/month-year test pins in r4 test ---
112:    """T-141 r4 (reviewer Y1): a bare year says nothing about whether it is the index accident within the last ~15 months. 2019 and 2022 (lib11) stay history."""
153:    ("Y3 rear-ended in October 2025", "info", "ER visit. Rear-ended in October 2025."),
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:39:54.221Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SCR/T141r4_head\" && ls tests/unit | grep -c . && ls tests/unit/conftest.py tests/conftest.py conftest.py pytest.ini setup.cfg pyproject.toml 2>/dev/null; PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py 2>&1 | tail -25",
 "description": "Run the seven conflict suites on the new archive copy",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:40:03.205Z

**tool result**
````
114
tests/conftest.py
........................................................................ [ 20%]
........................................................................ [ 40%]
........................................................................ [ 61%]
........................................................................ [ 81%]
................................................................         [100%]
352 passed in 8.48s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:09.212Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cd \"$SCR/T141r4_head\" && grep -rl \"lib11\" tests/ | sort && echo \"--- prev vs head lib11 test files diff ---\" && cd /Users/arsis/zlayt-pm-project && git diff --stat ad8b7d1 HEAD -- $(cd /Users/arsis/zlayt-pm-project && grep -rl \"lib11\" tests/ | sort) ; echo \"(end)\"; echo \"--- lib11 expected conflicts via the case-level test modules ---\"; cd \"$SCR/T141r4_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q $(grep -rl \"lib11\" tests/ | sort) 2>&1 | tail -15",
 "description": "Find lib11 tests, confirm unchanged since ad8b7d1, run them",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T14:40:27.273Z

**tool result**
````
tests/e2e/test_conflict_skipped.py
tests/unit/test_amounts_t140.py
tests/unit/test_conflict_candidates.py
tests/unit/test_conflicts.py
tests/unit/test_t139_unmarked.py
tests/unit/test_t141_checks_per_case.py
tests/unit/test_t141_r3_variants.py
--- prev vs head lib11 test files diff ---
 tests/e2e/test_conflict_skipped.py  |  33 +++++
 tests/unit/test_t139_unmarked.py    | 248 ++++++++++++++++++++++++++++++++++++
 tests/unit/test_t141_r3_variants.py |  97 +++++++++++++-
 3 files changed, 373 insertions(+), 5 deletions(-)
(end)
--- lib11 expected conflicts via the case-level test modules ---
........................................................................ [ 18%]
........................................................................ [ 36%]
........................................................................ [ 54%]
........................................................................ [ 73%]
........................................................................ [ 91%]
.................................                                        [100%]
393 passed in 16.83s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:40:43.662Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && grep -n \"more than two months\\|> 2:\\|int(y) <= ry\\|_CLAUSE_HISTORY.search\\|def _clause_is_history\\|def _governed\\|rear\\[- \\]?end\" \"$SCR/T141r4_head/app/backend/conflicts.py\"; echo \"--- test pins ---\"; grep -n '\"Y1\\|\"Y3\\|\"Y2' \"$SCR/T141r4_head/tests/unit/test_t141_r3_variants.py\"; echo \"--- Y3 direct, sub-probe: same sentence, record dated Nov 2025 vs Jan 2026 ---\"; cd \"$SCR/T141r4_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c '\nimport sys; sys.path.insert(0, \".\")\nfrom app.backend import conflicts as C\nR=lambda n,d,s,e: dict(n=n,date_iso=d,source=s,excerpt=e,kind=\"encounter\")\nfor ex,d in [(\"ER visit. Rear-ended in October 2025.\",\"2026-01-05\"),(\"ER visit. Rear-ended in November 2025.\",\"2026-01-05\"),(\"ER visit. Rear-ended in 2025.\",\"2026-01-05\")]:\n    recs=[R(1,d,\"ER\",ex),R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"),R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")]\n    print(\"conflict\" if C.accident_date_conflicts(recs) else \"info    \", \"|\", ex, \"| record\", d)\n'",
 "description": "Locate Y3-relevant code lines and tests, probe month-year boundary"
}
````

### User / tool · 2026-11-02T14:40:43.866Z

**tool result**
````
18:_EVENT = re.compile(r"\b(?:collision|collided|crash\w*|MVA|MVC|MVI|rear[- ]?end\w*|struck|wreck\w*|accident\w*|incident|pedestrian|motor\s+vehicle|vehicular|"
45:def _clause_is_history(clause: str, stated: str, rec_iso: str) -> bool:
47:    date within the year before is a possible index event: MVA 12/30/2025 against a stated 2026-01-05), a month and year more than two months before the RECORD's
50:    if _CLAUSE_HISTORY.search(clause):
61:        if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2:
64:    return any(int(y) <= ry - 2 for y in _YEAR.findall(rest))
67:def _governed(clause: str, m) -> bool:
--- test pins ---
152:    ("Y2 rear-ended in November 2025", "conflict", "ER visit. Rear-ended in November 2025."),
153:    ("Y3 rear-ended in October 2025", "info", "ER visit. Rear-ended in October 2025."),
--- Y3 direct, sub-probe: same sentence, record dated Nov 2025 vs Jan 2026 ---
info     | ER visit. Rear-ended in October 2025. | record 2026-01-05
conflict | ER visit. Rear-ended in November 2025. | record 2026-01-05
conflict | ER visit. Rear-ended in 2025. | record 2026-01-05
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:14.265Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD now: $(git rev-parse HEAD)\" && git diff --stat 93a2ffc HEAD -- app/backend/conflicts.py tests/unit/test_t141_r3_variants.py | tail -1; echo \"(empty above = T-141 files unchanged since 93a2ffc)\"; ls reviews/T-141-staff-engineer-r4.md 2>&1 | head -1",
 "description": "Recheck HEAD and that the T-141 files and r4 review path are as expected"
}
````

### User / tool · 2026-11-02T14:41:14.389Z

**tool result**
````
HEAD now: 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e
(empty above = T-141 files unchanged since 93a2ffc)
ls: reviews/T-141-staff-engineer-r4.md: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:16.509Z

**tool call — Bash**
````
{
 "command": "git log --oneline 93a2ffc..HEAD | head -5 && git diff --stat 93a2ffc HEAD -- evals/library/ | tail -1; echo \"(empty = lib11 files unchanged since 93a2ffc)\"",
 "description": "List commits after 93a2ffc and confirm evals library unchanged"
}
````

### User / tool · 2026-11-02T14:41:16.625Z

**tool result**
````
20b3a42 test(e2e): T-155 update stale e2e for D-059 (L6 has 4 objections), T-134 r2 edit_to_check verdict wording, T-144 uncovered-list row height; harden shortcut-sheet focus race
bf53087 fix(backend): T-146 r3 a re-run never lowers or replaces a decided item: it is kept whole with a visible note and the case reads run_partial (flag step down, summary check failed, extract down, judge down, nothing to keep)
(empty = lib11 files unchanged since 93a2ffc)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:36.485Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r4.md",
 "content": "# T-141 staff-engineer review, round 4 (93a2ffc), scoped check\n\nVerdict: **changes** (0 blockers, 1 major, 1 nit).\n\nScope was limited to the three checks in the brief. Against the section 7.4 rule, 32 of the 33 r3 variants behave correctly. The miss is Y3, \"Rear-ended in October 2025\" in a 2026-01-05 record. It stays info-only because the month-year cut-off is still two months (conflicts.py:61), while the same record with \"November 2025\" (Y2) raises a conflict. The r3 acceptance test asked for Y1 and Y3 to conflict; Y1 was fixed and Y3 was pinned as info.\n\n- Negated generic prior history (N1, N2, N3): info. Correct, including N3 \"Denies any motor vehicle collision or injury\".\n- Explicitly prior history (N4 \"MVA in 2015\", N5 \"History of MVA 2015\", N6 \"Hx: rear-end collision 2018\", H11 \"MVA remote past\"): info. Correct under my reading that a dated or Hx/remote-labelled prior is explicit prior. See questions_for_chris.\n- Negated or governed mechanisms (T1 to T10, including \"No LOC after the accident\", \"Has not worked since the accident\", \"No airbag deployment in the collision\"): all conflict. Correct.\n- History label or prior-marker wrapped mechanisms (H1 to H10, including \"History: rear-ended\", \"Prior to arrival, pt was in MVC\"): all conflict. Correct.\n- Bare year and month-year mechanisms (Y1, Y2): conflict. Correct. Y3: info. Rule miss (finding 1).\n- Benign (B1 \"Fall risk screen negative\", B2 \"Impact of diabetes\"): info. Correct. B3 \"Injury prevention handout given\" conflicts; a safe-direction over-fire (finding 2).\n\nlib11 is unchanged: the commit touches only conflicts.py and the r3 variants test, and the lib11 case files have an empty diff since 93a2ffc. The conflict suites pass: 352 passed. The seven lib11-referencing test modules pass: 393 passed.\n\nMethod and state: HEAD was 93a2ffc when the checks ran, and is 20b3a42 now. `git diff --stat 93a2ffc HEAD` over conflicts.py, the r3 variants test and evals/library/ is empty, so the reviewed code is the current code. Probes ran on git archive copies, not the working tree.\n\n```json\n{\"card\": \"T-141\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git 93a2ffc (T-141 round 4, section 7.4 fix-up): app/backend/conflicts.py and tests/unit/test_t141_r3_variants.py. Probes on a git archive of 93a2ffc (/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r4_head) with ad8b7d1 as the control archive (.../scratchpad/T141r4_prev). HEAD was 93a2ffc at check time and is 20b3a42 now; the T-141 files and evals/library/ are unchanged since 93a2ffc. Fixture backend only; no server started.\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md, reviews/T-141-staff-engineer-r3.md, .claude/agent-memory/staff-engineer-reviewer/project_t141_r3_patterns.md, `python3 tools/board.py show T-141` (round-4 brief and rule note at 14:24:15Z)\",\n  \"`git rev-parse HEAD` = 93a2ffc8595e16d66257207a4a8c2c8a31c99b8f at check time; `git cat-file -t 93a2ffc` = commit; later `git rev-parse HEAD` = 20b3a42be9d2faadf451ff4f5b9375b1f9aa795e with `git diff --stat 93a2ffc HEAD -- app/backend/conflicts.py tests/unit/test_t141_r3_variants.py` empty\",\n  \"`git show --stat 93a2ffc`: 2 files (app/backend/conflicts.py, tests/unit/test_t141_r3_variants.py); `git show 93a2ffc -- app/backend/conflicts.py` read in full\",\n  \"`git archive HEAD` into .../scratchpad/T141r4_head and `git archive ad8b7d1` into .../scratchpad/T141r4_prev\",\n  \".venv/bin/python -I .../scratchpad/T141r3_scripts/r3_variants.py .../scratchpad/T141r4_head: all 33 variants, classified per the rule (32 match; Y3 'Rear-ended in October 2025' prints info where the rule requires conflict)\",\n  \".venv/bin/python -I .../scratchpad/T141r3_scripts/r3_variants.py .../scratchpad/T141r4_prev: control; differs from the new archive on exactly T1, T2, T5, T6, T7, T8, T10, H1, H6, H7 (now conflict) and N3 (now info)\",\n  \"Direct probe on the new archive, record 2026-01-05, stated 2026-01-09: 'Rear-ended in October 2025.' -> info; 'Rear-ended in November 2025.' -> conflict; 'Rear-ended in 2025.' -> conflict\",\n  \"grep of app/backend/conflicts.py for the month-year cut-off (line 61: `> 2`) and bare-year rule (line 64: `int(y) <= ry - 2`); grep of tests/unit/test_t141_r3_variants.py lines 152-153 (Y2 conflict, Y3 info pinned)\",\n  \"pytest -I -p no:cacheprovider on the new archive: tests/unit/test_conflicts.py, test_conflict_candidates.py, test_t093_j3_controls_reachable.py, test_t141_checks_per_case.py, test_t141_r3_variants.py, test_t116_r4_all_dated_records.py, test_api_routes.py: 352 passed\",\n  \"lib11: `git ls-files | grep -i lib11` (evals/library/case_lib11_priors_and_ledger.{txt,expected.json}); `git diff --stat ad8b7d1 HEAD` and `93a2ffc HEAD` over those files empty; pytest -I on the 7 tests/ modules that reference lib11: 393 passed\",\n  \"Not run (outside the brief): mutation checks, the pipeline CLI, the full unit suite, the 27-packet differential\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"determinism\": 5, \"honest_failure\": 4, \"tests_assert_behaviour\": 3, \"llm_code_boundary\": 5, \"controls_discipline\": 4},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Y3 'Rear-ended in October 2025' in a 2026-01-05 record stays info-only; the round-4 rule requires a date conflict and the r3 acceptance test asked for Y3 to conflict\",\n   \"evidence\": \"Repro: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <scratchpad>/T141r4_head` prints `info      exp=conflict_or_info | Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)`. Cause: app/backend/conflicts.py:61 `if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2: return True` (a month and year more than two months before the record counts as history). Test pin: tests/unit/test_t141_r3_variants.py:153 `(\\\"Y3 rear-ended in October 2025\\\", \\\"info\\\", \\\"ER visit. Rear-ended in October 2025.\\\")`. Same record with the month one later: tests/unit/test_t141_r3_variants.py:152 `(\\\"Y2 rear-ended in November 2025\\\", \\\"conflict\\\", ...)` and the probe prints conflict. Direct probe on the new archive, record 2026-01-05: 'Rear-ended in October 2025.' -> info; 'Rear-ended in November 2025.' -> conflict. The bare-year form was fixed at conflicts.py:64 (`int(y) <= ry - 2`), so 'Rear-ended in 2025.' (Y1) now conflicts; the month-year form was not aligned.\",\n   \"why_it_matters\": \"The section 7.4 rule says info-only only for generic negated or explicitly prior history. 'Rear-ended in October 2025' names the mechanism with no negator and no prior label; it is hidden only by a date window, and a one-month change flips it. A rear-end described in an earlier record is a real discrepancy against a stated accident date of 2026-01-09, which is the lost-conflict class the GATE-M2 finding and r2/r3 majors were about. Severity is major, not blocker, on the same calibration as r3: the record count still appears as a note and the loss is the date-conflict flag, not an entry or a total. The r4 handoff says 'bare year history needs >=2 calendar years', but the month-year window was left at two months, so the r3 acceptance test ('Y1 and Y3 conflict') is only half met. The test file pins Y3 to the code's output, so the handoff's '33 reviewer variants pinned' is pinned to the worker's reading, not the reviewer's.\",\n   \"fix\": \"Apply the bare-year rule to month-year dates too. In _clause_is_history (conflicts.py:61), delete the `> 2` month window and count a month-and-year as history only when its year is at least two calendar years before the record's year, or when the sub-clause carries a history marker (_CLAUSE_HISTORY or _HIST_WORD). Change tests/unit/test_t141_r3_variants.py:153 to expect conflict.\",\n   \"acceptance_test\": \"On the r4 archive plus the fix: r3_variants.py prints conflict for Y1, Y2 and Y3; info for N1-N6, H11, B1 and the lib11 shape A (`Car accidents in 2019 and 2022`, `Passenger vehicle struck from behind`, `Date of injury: 2026-03-18`); tests/unit/test_t141_r3_variants.py:153 expects conflict; the seven conflict suites stay green (352 passed) and the 7 lib11-referencing modules stay green (393 passed).\"},\n  {\"severity\": \"nit\",\n   \"title\": \"'Injury prevention handout given.' raises a date conflict because 'injury' alone is a mechanism word\",\n   \"evidence\": \"Repro: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <scratchpad>/T141r4_head` prints `conflict  exp=conflict_ok | B3 'Injury prevention handout given'`; the same output on the ad8b7d1 control. _EVENT (conflicts.py:18-25) matches `injur\\\\w*` with no mechanism context.\",\n   \"why_it_matters\": \"Not a rule violation: the round-3 direction prefers a false positive to a hidden conflict. It is an over-fire, and a paralegal must dismiss it on an annual physical.\",\n   \"fix\": \"Leave as is and list it as a known over-fire, or match 'injury' only when it is followed by or preceded by mechanism words (collision, MVA, fall, struck, from).\",\n   \"acceptance_test\": \"Optional. If changed: 'Injury prevention handout given.' returns [] and 'Injury from rear-end collision' still conflicts in test_t141_r3_variants.py.\"}\n ],\n \"whats_right\": [\n  \"The ten negated or governed mechanisms (T1-T10) and the history-labelled mechanisms (H1-H10) now conflict; the control on ad8b7d1 misses seven of T1-T10 and H1, H6, H7, so the fix does what the handoff says.\",\n  \"The scope held: the commit touches only conflicts.py and the r3 variants test; evals/library/ lib11 files are unchanged; the conflict suites (352) and the lib11-referencing modules (393) pass on a clean archive.\",\n  \"The note text no longer asserts that no record names a collision or injury (app/backend/conflicts.py accident_date_note), which closes the false-note part of r3's major.\"\n ],\n \"questions_for_chris\": [\n  \"Non-negotiable 6 says engineering reviewers run Sonnet; this scoped check ran as claude-haiku-5-5 because the brief named that model. Is a Haiku run acceptable for this record, or should T-141 r4 be re-run as Sonnet?\",\n  \"Under the section 7.4 rule, is a month and year more than two months before the record 'explicitly prior'? If yes, Y3 is a nit and the rule needs that sentence; if no, finding 1 stands.\",\n  \"The rule lists 'rear-ended' and 'MVC without prior/previous' as mechanism words. I treated dated or Hx/remote-labelled history ('MVA in 2015', 'Hx: rear-end collision 2018', 'MVA remote past') as explicit prior and info-only. Confirm that reading.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T14:41:36.632Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:40.334Z

**tool call — Bash**
````
{
 "command": "python3 -I -c '\nimport json,re\nt=open(\"reviews/T-141-staff-engineer-r4.md\",encoding=\"utf-8\").read()\nblocks=re.findall(r\"```json\\n(.*?)\\n```\", t, re.S)\nprint(\"json blocks:\", len(blocks))\nd=json.loads(blocks[0])\nsev=[f[\"severity\"] for f in d[\"findings\"]]\nprint(\"verdict:\", d[\"verdict\"], \"| severities:\", sev, \"| model:\", d[\"model\"], \"| card:\", d[\"card\"], \"| persona:\", d[\"persona\"])\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict rule expects:\", exp, \"OK\" if exp==d[\"verdict\"] else \"MISMATCH\")\n'",
 "description": "Parse the review JSON and check the verdict rule"
}
````

### User / tool · 2026-11-02T14:41:40.464Z

**tool result**
````
json blocks: 1
verdict: changes | severities: ['major', 'nit'] | model: claude-haiku-5-5 | card: T-141 | persona: staff-engineer-reviewer
verdict rule expects: changes OK
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:46.498Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r4_patterns.md",
 "content": "---\nname: project_t141_r4_patterns\ndescription: T-141 r4 93a2ffc scoped check (changes, 1 major): month-year two-month cut-off leaves 'Rear-ended in October 2025' info while the bare-year fix flipped; worker pinned a variant the reviewer's acceptance test said must conflict\nmetadata:\n  type: project\n---\n\nT-141 r4 (93a2ffc, verdict changes, 1 major Y3, 1 nit B3). Scoped check: 32 of 33 r3 variants per the section 7.4 rule. Y1 fixed by the bare-year rule (`int(y) <= ry - 2`), but the month-year window (conflicts.py `> 2` months before the record) still hides Y3 (Oct 2025 vs record 2026-01-05) while Y2 (Nov 2025) conflicts.\n\n- Pattern: when a fix aligns one date form to a new rule, check its sibling forms (bare year, month-year, full date) in the same probe. A one-month change flipping the result is the tell.\n- Pattern: the worker pinned Y3 to info in tests/unit/test_t141_r3_variants.py while the reviewer's r3 acceptance test said Y3 conflicts. Read the reviewer's acceptance test, not only the script's expectation column (the script said `conflict_or_info`, which hid the conflict in the reviewer's own prose).\n- Method that worked: run the variant script on the new archive AND on the prior-round archive (control); the set of changed verdicts should equal the intended fixes (here: T1-T10, H1, H6, H7 flipped to conflict; N3 flipped to info).\n- Reproduce with `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <archive>`; the record-date and stated-date fixtures are in the script.\n- Open question for the orchestrator: whether a dated month-year more than two months before the record counts as \"explicitly prior\" under section 7.4.\n\n**How to apply:** for any date-window rule, probe adjacent months/years on both sides of the cut-off and check that every date form uses the same rule.\n\nRelated: [[project_t141_r3_patterns]] (round 3 word-window class), [[feedback_exact_count_vs_presence]].\n"
}
````

### User / tool · 2026-11-02T14:41:46.586Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r4_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:49.514Z

**tool call — Bash**
````
{
 "command": "tail -n 3 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md && wc -l .claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "description": "Show the tail of the memory index"
}
````

### User / tool · 2026-11-02T14:41:49.631Z

**tool result**
````
- [T-140 r2 patterns](project_t140_r2_patterns.md) — a0e2639 changes: tests read untracked reviewer file (clean pytest aborts), after-figure position gap, reclassify skips duplicate/total flags
- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed
- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — r1 changes: untracked ledger read at import breaks clean collection, golden-named test without golden compare, git show not working tree, HEAD moved 3x
      74 .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:51.829Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed\n",
 "new_string": "- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed\n- [T-141 r4 patterns](project_t141_r4_patterns.md) — 93a2ffc changes: month-year two-month cut-off hides 'Rear-ended in October 2025' while bare-year fix flipped; pinned variant contradicts r3 acceptance\n"
}
````

### User / tool · 2026-11-02T14:41:51.927Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T14:41:53.590Z

changes, 0 blockers, 1 major (Y3 "Rear-ended in October 2025" stays info-only via the two-month cut-off at conflicts.py:61), 1 nit; 32 of 33 variants per rule, lib11 unchanged, 352 conflict tests pass. Review: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r4.md
