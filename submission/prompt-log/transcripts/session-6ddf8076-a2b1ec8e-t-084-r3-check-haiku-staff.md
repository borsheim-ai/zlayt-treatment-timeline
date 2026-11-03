# Subagent: T-084 r3 check (haiku staff) (T-084 r3 check (haiku staff))

Source: `agent-a2b1ec8e5c9897f01.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T04:56:15.903Z

Final check of board card T-084 (guarded charge reclassification) in /Users/arsis/zlayt-pm-project; get the latest commit from `python3 tools/board.py show T-084`. Using reviews/T-084-staff-engineer-r3.md, confirm:
- the restore-after-class-only-change test exists, and mutant T84-3 now fails it;
- the wording gate uses the shared rate-cue function in app/backend/amounts.py, so "unit price $X", "@ $X", "$X/visit" and "rate of $X" are refused before the judge.

Mutate the gate in a scratch copy to confirm a test fails. Test a `git archive HEAD` copy in your scratchpad, since reviewers can't use worktree. Run `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_billing.py`. Write reviews/T-084-staff-engineer-r4.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:17.500Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T04:56:17.510Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:17.726Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r3.md"
}
````

### User / tool · 2026-11-02T04:56:17.735Z

**tool result**
````
1	# T-084 r2 review, filed as r3 (staff-engineer-reviewer, round 2)
2	
3	This file supersedes `reviews/T-084-staff-engineer-r2.md`. That file was written without its ```json block, so the board validator rejects it, and the append-only guard refuses an in-place edit. Use this file for the T-084 round-2 verdict; do not register the r2 file.
4	
5	Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (T-084 r2, committed with the T-073 r2 changes), with e2b4e3f (billing restored) underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both "restore ... reverted by 2fca530"). The verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad. The working tree has uncommitted edits to reclassify.py (it now imports `amounts.RATE_CUE`), amounts.py, billing.py and audited.py. Those are not reviewed here.
6	
7	## Summary
8	
9	The three r1 invariants hold on HEAD for the paths the tests and probes reach, with two gaps. (1) A restore re-runs both checks when the sentence changes and when the code's class changes (reclassify.py:145-153), and the code is right for both. Only the sentence arm has a test, so a class-only change has no test that would catch the removal of its check (F1). (2) The code wording gate refuses "Charge per visit $185." and "Billed $150 per visit." before the judge, as the brief asks, and 17 rate-cue sentences. It still passes six unit-price phrasings that the amount classifier calls a rate or a unit price, so for those the judge is the only gate (F2).
10	
11	One r1 blocker is closed, but not by this card. c8a9874 alone does not work: its own test file fails 9 of 120 tests, and a reclassify request returns 500 after it has already changed the item and written no audit row. HEAD a850be0 is correct because 6feb2ff restored the T-095 schema that 2fca530 had reverted. The card's commit list does not name 6feb2ff.
12	
13	Billing is back in HEAD and identical to f218263. The worker's extra behaviour (a promoted charge falls back to the code's class when a rerun changes its sentence) goes the safe direction, but it drops the paralegal's decision without a visible note (F4).
14	
15	Verdict: changes (0 blockers, 2 majors) on HEAD a850be0.
16	
17	## Exercised (what I actually ran or read)
18	
19	- `python3 tools/board.py show T-084`, `show T-094`, `show T-095` (header).
20	- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44, then a850be0); `git show --stat` for c8a9874, e2b4e3f, 6feb2ff, a850be0.
21	- `git show c8a9874:app/db/schema.sql | grep -c "'reclassify'"` = 0; a850be0 schema.sql:57 has 'reclassify' and 'rejudge'.
22	- `git diff --stat bc12d44 a850be0` over the in-scope files: only app/db/db.py and app/db/schema.sql. `git diff --stat f218263 a850be0 -- app/backend/billing.py tests/unit/test_billing.py`: empty. `git ls-tree -r --name-only a850be0 | grep -i billing`: both files. a850be0 api.py lines 510 (billing) and 512 (reclassify).
23	- `git blame -L 496,502 a850be0 -- app/backend/pipeline.py`: lines 500-501 from 865b1865 (T-085).
24	- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed. The 9 failures are all in test_reclassify.py, with `IntegrityError` at reclassify.py:90 and `assert (500 == 200)` in test_route.
25	- `.venv/bin/python -m pytest -q tests/unit/test_audited.py` at a850be0: 19 passed. `tests/unit/test_billing.py`: 27 passed.
26	- `.venv/bin/python -m pytest -q tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. The 7 are test_e2e_contract::test_every_test_id_is_declared, test_t037_backend::test_cli_sample_on_fixture_backend_under_60s, test_t075_determinism::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2, and four in test_trace.py. The handoff's "1417 pass" was measured on the working tree.
27	- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` in the a850be0 archive: `UnboundLocalError: cannot access local variable 'raw'` at pipeline.py:501.
28	- Read in full at a850be0: app/backend/reclassify.py and tests/unit/test_reclassify.py (both unchanged since bc12d44), app/backend/judge_guard.py, app/llm/audited.py. Also db.py:54 (autocommit), :215, :227, :287 (BEGIN); amounts.py:14 (`_UNIT`).
29	- Probes in `artifacts/review-evidence/T-073-T-084-r2/`, each run as `.venv/bin/python -I <probe> <archive root>`: `probe_reclassify_audit_route.py` (c8a9874: HTTP 500, stored kind changed to unclear, `review_events` empty; a850be0: HTTP 200, one reclassify event); `probe_rate_cue_gaps.py` (output `rate-cue-gaps-run.txt`); `probe_classifier_vs_wording_gate.py` (output `classifier-vs-gate-run.txt`); `probe_restore_class_only_flip.py` on a850be0 and on mutant m03 (output `restore-class-only-flip-run.txt`).
30	- Scratch mutants via `mutate_r2.py` on copies of the archive (log `mutation-run-r2.txt`). Control 139 passed. T84-1 (rate cue removed from the wording gate) 21 failed; T84-2 ('per' removed from the rate-cue pattern) 11 failed; T84-3 (restore ignores the code class) 139 passed; T84-4 (restore ignores the sentence change) 1 failed; T84-5 (restore always skips the checks, the r1 bug) 2 failed; T84-6 (promoted charge kept when its sentence changes) 1 failed. T73-1 to T73-4 are in the T-073 r2 review.
31	- `grep -rn "judge_guard.guarded" app/`: review.py:102 and reclassify.py:167 only.
32	
33	## Findings
34	
35	### F1 (major): restore after a class-only change is untested; mutant T84-3 survives
36	
37	- The code is right. `_may_restore` (reclassify.py:145-153) requires `rerun.code_class == "charge"` and an unchanged sentence sha. Probe `probe_restore_class_only_flip.py` on a850be0 (the rerun changes only the code's class of $310; the excerpt is identical): `4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE`; `5. stored kind = unclear`; `pending total cents = 0`.
38	- The gap is the test. Mutant T84-3 (reclassify.py:153 without the class clause) passes all 139 tests. The same probe on that mutant gives `restored=True kind=charge` and `pending total cents = 31000`.
39	- The tests cover the sentence arm only. test_reclassify.py:190 `RATE_R3` changes the sentence and the class together; test_reclassify.py:198-216 uses it. test_reclassify.py:219-230 changes the sentence only.
40	- Why it matters: the brief asks that a restore re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to `_may_restore` can reopen the r1 blocker with no failing test.
41	- Fix: patch `amounts.classify` so the rerun's code class of $310 is "rate" while the excerpt is identical. `reclassify(..., {"to": "charge"}, call=None)` must raise 422 JUDGE_UNAVAILABLE with the item still `unclear`. Add the same case with `call=FakeCall(J2("agree"))`: the judge is called once and `restored` is False. Keep test_reclassify.py:233-240 passing.
42	- Acceptance test: mutant T84-3 fails the new test.
43	
44	### F2 (major): the code wording gate passes unit-price phrasings that the amount classifier calls rates
45	
46	- Probe `probe_classifier_vs_wording_gate.py`: "Charged $150 an hour." is `rate` by amounts.classify and passes charge_wording; "Charged $75 a unit." is `rate` and passes; "Billed $120 an appointment." is `rate` and passes. amounts.py:14 `_UNIT` includes hour, unit and appointment; the gate's rate-cue pattern (reclassify.py:31-33) has none of them.
47	- Probe `probe_rate_cue_gaps.py`: "Billed $150 hourly.", "Charged $90 apiece.", "Billed $40 daily." and "Billed $200 a month." also pass the code gate. The two named strings are refused, so F2 is not about the brief's named cases.
48	- Why it matters: D-042 as written is met, because the sentence has charged wording and the judge re-checks it. But the code gate and the classifier disagree about the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.
49	- Fix: one rate-unit test shared by amounts.classify and reclassify.charge_wording. The uncommitted working tree already moves toward `amounts.RATE_CUE` (not reviewed here). Whatever lands, refuse the six phrasings before the judge.
50	- Acceptance test: `charge_wording` returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for "Charged $150 an hour.", "Charged $75 a unit." and "Billed $120 an appointment."; a parametrized test asserts that for every fixture sentence, `amounts.classify == "rate"` implies `charge_wording is None`.
51	
52	### F3 (minor): the state change and its audit row are separate autocommit writes; the consequence is observed
53	
54	- reclassify.py:135 `DB.update_item` commits on its own (db.py:54 `isolation_level=None`). reclassify.py:137 `review.batch_apply` (for a non-pending item) and reclassify.py:138 `_log` follow as separate statements.
55	- Observed on c8a9874: `POST reclassify a1 -> HTTP 500`, `a1 stored after request: kind=unclear`, `review_events for a1: []`. The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).
56	- Fix: wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as `apply_review` does (db.py:227, :287).
57	- Acceptance test: monkeypatch `RC._log` to raise; assert the item's kind is still `charge` after the call.
58	
59	### F4 (minor): a promoted charge is dropped silently when its sentence changes
60	
61	- reclassify.py:188-189 returns the fresh item when the sentence sha differs, which discards the reclassification record with no note. The figure falls back to the code's class (fail-closed: it leaves the total).
62	- test_reclassify.py:249-250 asserts only `kind != "charge"`. The audit row stays, but the item view does not say why the figure changed.
63	- Fix: keep the record with `dropped: "SENTENCE_CHANGED"` in `ladder.reclassification` and show it in the item view and stepper.
64	- Acceptance test: after a sentence change, `item.ladder.reclassification.dropped == "SENTENCE_CHANGED"`.
65	
66	## Closed at HEAD (not findings at a850be0)
67	
68	- c8a9874 on its own tree (blocker at c8a9874, closed at HEAD). `git show c8a9874:app/db/schema.sql` has no 'reclassify' in the CHECK, while reclassify.py:27 sets `AUDIT_ACTION = "reclassify"`. The INSERT fails with IntegrityError (reclassify.py:90), the route returns 500, and the item is already changed (F3). 2fca530 (T-087/T-086, a sibling commit) reverted the T-095 CHECK and migration; 6feb2ff ("fix: restore T-095 work reverted by 2fca530") restored them. At a850be0 the CHECK is at schema.sql:57, SCHEMA_VERSION is 4 (db.py:33), the four files pass 120 of 120, and the probe returns 200 with a `reclassify` event. The card should cite 6feb2ff, since c8a9874 alone does not pass.
69	- r1 F4 (audit action 'edit'): closed. AUDIT_ACTION is "reclassify" (reclassify.py:27) and test_route (test_reclassify.py:319) asserts `["reclassify"]`, which passes at HEAD.
70	- r1 F2 (billing removed by ec33bf0): closed. billing.py and test_billing.py are identical to f218263 at a850be0; api.py:510 registers the routes; test_billing.py passes (27).
71	- r1 F1 (restore after a rerun), sentence arm: closed. Mutants T84-4, T84-5 and T84-6 fail 1, 2 and 1 tests. Class arm: code correct (probe), test missing (F1).
72	- r1 F3 (rate phrase passes the wording gate), named strings: closed. "Charge per visit $185." and "Billed $150 per visit." are refused before the judge (test_reclassify.py:161-171, `call.log == []`). Mutant T84-1 fails 21 tests and T84-2 fails 11. The remaining gap is F2.
73	
74	## Judgement on the worker's extra behaviour
75	
76	A promoted charge falls back to the code's class when a rerun changes its sentence (reclassify.py:188-189). I judge this right: it fails closed, and it applies the same rule as the restore path (a sentence change means the earlier judge answer no longer applies). The silent drop is F4.
77	
78	## What is right
79	
80	- reclassify.py:145-153 (`_may_restore`) requires a charge original, a previous judge, and, after any rerun, the same sentence sha and a charge code class. The probe confirms the refusal (422 JUDGE_UNAVAILABLE, total 0).
81	- The refusals stay before the judge: test_reclassify.py:170 asserts `call.log == []` and the item stays `rate`, `needs_review`.
82	- Billing is back in HEAD: identical to f218263, registered at api.py:510, 27 tests pass.
83	
84	## Outside these cards (observed at a850be0, not attributed to T-073 or T-084)
85	
86	- The sample CLI crashes: `python -m app.pipeline evals/golden/sample.txt` ends in UnboundLocalError at pipeline.py:501. `git blame` puts lines 500-501 in 865b1865 (T-085). This is persona checklist item 20, and it fails on HEAD.
87	- Seven unit tests fail at a850be0 (listed in Exercised). I did not trace them to a cause. None is in the T-073 or T-084 files.
88	
89	## Scores
90	
91	```
92	no_rate_into_total_without_both_checks 3 (both checks run on every path; the class-only restore is untested, F1; the code gate passes six classifier-rate phrasings, F2)
93	restore_rule_tested 3 (sentence arm killed; class arm not, F1)
94	code_check_strength 2 (named strings and 17 cues refused; six classifier-rate phrasings pass, F2)
95	judge_gate 4 (judge disagree, unsure and unavailable give 422 with nothing changed)
96	audit_trail 3 (written at HEAD; the item change and the audit row are not one transaction, F3; the promoted drop is not shown, F4)
97	commit_integrity 2 (c8a9874 alone fails 9 tests and returns 500 with the item changed; closed at HEAD by 6feb2ff, which is not in this card's commit list)
98	billing_restored 5 (identical to f218263; route registered; 27 tests pass)
99	tests_kill_mutants 4 (T84-1, T84-2, T84-4, T84-5, T84-6 and the four T-073 mutants killed; T84-3 survives)
100	```
101	
102	## Questions for Chris
103	
104	- D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should "Charged $150 an hour.", "Charged $75 a unit." and "Billed $120 an appointment." be refused by the code gate before the judge, given that the amount classifier calls them rates? My reading is that they should be refused. The decision text does not say.
105	
106	```json
107	{"card": "T-084", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
108	 "scope": "commit c8a9874 (T-084 r2, committed with the T-073 r2 changes) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/backend/reclassify.py, app/backend/amounts.py (read), app/backend/api.py (routes), app/db/db.py and app/db/schema.sql (read, restored by 6feb2ff), tests/unit/test_reclassify.py, tests/unit/test_billing.py; c8a9874 alone fails 9 tests and is closed at HEAD by 6feb2ff (not a finding at a850be0); no app URL; the sample CLI run at a850be0 crashes (outside this card, see body)",
109	 "exercised": ["python3 tools/board.py show T-084, T-094, T-095", "git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874, e2b4e3f, 6feb2ff, a850be0; git show c8a9874:app/db/schema.sql | grep -c reclassify (0); git diff --stat bc12d44 a850be0 over the in-scope files (db.py and schema.sql only); git diff --stat f218263 a850be0 over the billing files (empty); git ls-tree a850be0 | grep billing (both files); a850be0 api.py lines 510 and 512; git blame -L 496,502 a850be0 -- app/backend/pipeline.py", ".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; a850be0 120 passed; c8a9874 9 failed 111 passed (IntegrityError at reclassify.py:90)", ".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed; tests/unit/test_billing.py: 27 passed; tests/unit at a850be0: 7 failed 1392 passed 2 skipped", ".venv/bin/python -m app.pipeline evals/golden/sample.txt at a850be0: UnboundLocalError at pipeline.py:501", "read in full at a850be0: reclassify.py and test_reclassify.py (both unchanged since bc12d44), judge_guard.py, audited.py; db.py:54, :215, :227, :287; amounts.py:14", "probes via .venv/bin/python -I in artifacts/review-evidence/T-073-T-084-r2/: probe_reclassify_audit_route.py (c8a9874: HTTP 500, item changed, no event; a850be0: HTTP 200, one reclassify event); probe_rate_cue_gaps.py (rate-cue-gaps-run.txt); probe_classifier_vs_wording_gate.py (classifier-vs-gate-run.txt); probe_restore_class_only_flip.py on a850be0 (422 JUDGE_UNAVAILABLE, total 0) and on mutant m03 (restored, total 31000; restore-class-only-flip-run.txt)", "scratch mutants via mutate_r2.py (mutation-run-r2.txt): control 139 passed; T84-1 21 failed; T84-2 11 failed; T84-3 139 passed (survives); T84-4 1 failed; T84-5 2 failed; T84-6 1 failed", "grep -rn judge_guard.guarded app/ (review.py:102 and reclassify.py:167 only)"],
110	 "verdict": "changes",
111	 "scores": {"no_rate_into_total_without_both_checks": 3, "restore_rule_tested": 3, "code_check_strength": 2, "judge_gate": 4, "audit_trail": 3, "commit_integrity": 2, "billing_restored": 5, "tests_kill_mutants": 4},
112	 "findings": [
113	  {"severity": "major", "title": "Restore after a class-only change is untested; mutant T84-3 (restore ignores the rerun's code class) passes all 139 tests",
114	   "evidence": "reclassify.py:153 'return rerun.get(code_class) == charge and rerun.get(excerpt_sha) == prior.get(excerpt_sha) == _sha(row[excerpt])'; mutant without the class clause: mutation-run-r2.txt 'T84-3 ... 139 passed'; restore-class-only-flip-run.txt: HEAD '4. restore with no judge: 422 reclassify_refused reason=JUDGE_UNAVAILABLE', mutant 'restored=True kind=charge' and 'pending total cents = 31000'; tests/unit/test_reclassify.py:190 RATE_R3 and :198-216 change the sentence, not only the class",
115	   "why_it_matters": "The brief requires a restore to re-run the full guard when the class or the sentence changed. A classifier or lexicon change on rerun with identical text is the realistic trigger (r1 F1). Without a class-only test, a later edit to _may_restore can reopen the r1 blocker and no test fails.",
116	   "fix": "Add a test that patches amounts.classify so the rerun's code class of $310 is rate while the excerpt is identical; reclassify to charge with call=None must raise 422 JUDGE_UNAVAILABLE with the item still unclear. Add the same case with call=FakeCall(J2 agree): the judge is called once and restored is False. Keep test_reclassify.py:233-240 passing.",
117	   "acceptance_test": "Mutant T84-3 (reclassify.py:153 without the code_class clause) fails the new test."},
118	  {"severity": "major", "title": "The code wording gate passes unit-price phrasings that the amount classifier calls rates, so the judge is the only gate for them",
119	   "evidence": "classifier-vs-gate-run.txt: 'Charged $150 an hour.' classifier rate, gate passes (Charged); 'Charged $75 a unit.' rate, passes; 'Billed $120 an appointment.' rate, passes. rate-cue-gaps-run.txt: 'Billed $150 hourly.', 'Charged $90 apiece.', 'Billed $40 daily.', 'Billed $200 a month.' pass the gate. reclassify.py:31-33 _RATE_CUE has no hour, unit or appointment; amounts.py:14 _UNIT = (visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?",
120	   "why_it_matters": "D-042 as written is met (charged wording plus a judge re-check), but the code gate and the classifier disagree on the same sentence. For these phrasings the judge is the only gate before a figure reaches pending, and the paralegal can then accept it into the total. The r1 fix list asked for the rate unit next to the figure, and the gate covers that only in part.",
121	   "fix": "Use one rate-unit test for amounts.classify and reclassify.charge_wording (the uncommitted working tree already moves toward amounts.RATE_CUE; not reviewed here). Refuse the six phrasings before the judge.",
122	   "acceptance_test": "charge_wording returns None and reclassify raises 422 NO_CHARGE_WORDING with the judge not called for 'Charged $150 an hour.', 'Charged $75 a unit.', 'Billed $120 an appointment.'; a parametrized test asserts that for every fixture sentence, amounts.classify == rate implies charge_wording is None."},
123	  {"severity": "minor", "title": "State change and audit row are separate autocommit writes; a failed audit write leaves the item changed and no event (observed)",
124	   "evidence": "reclassify.py:135 DB.update_item (autocommit, db.py:54 isolation_level=None); reclassify.py:137 batch_apply; reclassify.py:138 _log. Probe probe_reclassify_audit_route.py on c8a9874: 'POST reclassify a1 -> HTTP 500', 'a1 stored after request: kind=unclear', 'review_events for a1 (action, payload event): []'",
125	   "why_it_matters": "The paralegal sees an error, the item has changed, and there is no audit row. The brief allows this as a minor (F5).",
126	   "fix": "Wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).",
127	   "acceptance_test": "Monkeypatch RC._log to raise; assert the item kind is still charge after the call."},
128	  {"severity": "minor", "title": "A promoted charge is dropped silently when a rerun changes its sentence",
129	   "evidence": "reclassify.py:188-189 'if rc.get(to) == charge and rc.get(excerpt_sha) != _sha(it.get(excerpt)): return it' discards the reclassification record with no note; tests/unit/test_reclassify.py:249-250 asserts only kind != charge",
130	   "why_it_matters": "Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign that her promotion was withdrawn, and the item view does not say why the figure changed.",
131	   "fix": "Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.",
132	   "acceptance_test": "After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED and the item view names the reason."}
133	 ],
134	 "whats_right": [
135	  "reclassify.py:145-153 (_may_restore) refuses a restore after a class or sentence change; probe restore-class-only-flip-run.txt shows 422 JUDGE_UNAVAILABLE with the total at 0.",
136	  "test_reclassify.py:161-171 refuses 'Charge per visit $185.' and 'Billed $150 per visit.' before the judge (call.log == []); mutant T84-1 fails 21 tests.",
137	  "tests/unit/test_billing.py and app/backend/billing.py are identical to f218263, the billing route is registered at api.py:510, and 27 billing tests pass at a850be0."
138	 ],
139	 "questions_for_chris": ["D-042 says a rate becomes a charge only with code-verified charged wording and a judge re-check. Should 'Charged $150 an hour.', 'Charged $75 a unit.' and 'Billed $120 an appointment.' be refused by the code gate before the judge, given that the amount classifier calls them rates? The decision text does not say."]}
140	```
141	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:18.071Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-084 && git log --oneline -5 && git rev-parse HEAD",
 "description": "Show card T-084 and recent commit history"
}
````

### User / tool · 2026-11-02T04:56:18.246Z

**tool result**
````
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
updated_at: "2026-11-02T04:56:12Z"
claimed_by: "backend"
claimed_at: "2026-11-02T04:53:14Z"
rounds: 2
commits: ["ec33bf0", "c8a9874", "e2b4e3f", "9c1af01"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-084-staff-engineer.md", "at": "2026-11-02T04:33:32Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-084-staff-engineer-r3.md", "at": "2026-11-02T04:53:11Z"}
ac:
  - {"n": 1, "text": "Paralegal can reclassify charge<->not-a-charge; rate->charge only if code finds charged-amount wording in the excerpt AND judge re-check passes, else 422 with reason; audit event; unit tests", "done": true, "evidence": "tests/unit/test_reclassify.py + test_billing.py: 148 passed; class-only restore tests kill T84-3; unit-price phrasings refused before judge (9c1af01)"}
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
- 2026-11-02T04:53:11Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-084-staff-engineer-r3.md; round 2; findings:
    - [major] Restore after a class-only change is untested; mutant T84-3 (restore ignores the rerun's code class) passes all 139 tests — fix: Add a test that patches amounts.classify so the rerun's code class of $310 is rate while the excerpt is identical; reclassify to charge with call=None must raise 422 JUDGE_UNAVAILABLE with the item still unclear. Add the same case with call=FakeCall(J2 agre
    - [major] The code wording gate passes unit-price phrasings that the amount classifier calls rates, so the judge is the only gate for them — fix: Use one rate-unit test for amounts.classify and reclassify.charge_wording (the uncommitted working tree already moves toward amounts.RATE_CUE; not reviewed here). Refuse the six phrasings before the judge.
    - [minor] State change and audit row are separate autocommit writes; a failed audit write leaves the item changed and no event (observed) — fix: Wrap update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).
    - [minor] A promoted charge is dropped silently when a rerun changes its sentence — fix: Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.
- 2026-11-02T04:53:14Z backend: claimed
- 2026-11-02T04:55:58Z backend: AC 1 checked: tests/unit/test_reclassify.py + test_billing.py: 148 passed; class-only restore tests kill T84-3; unit-price phrasings refused before judge (9c1af01)
- 2026-11-02T04:55:58Z backend: moved in_progress -> in_review
- 2026-11-02T04:56:12Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
r3: (F1) class-only restore tests (test_restore_after_a_class_only_change_needs_the_judge_again, ..._runs_the_judge_once...) patch amounts.classify for the rerun with identical excerpt; mutant T84-3 now fails 2 tests. (F2) charge_wording also refuses when amounts.classify calls the figure a rate; shared RATE_CUE in amounts.py gained an hour/a unit/an appointment/a month, hourly/daily/weekly/monthly/apiece, unit price, '@ $' cues; _RATE_AFTER (classifier) gained hourly/daily/apiece/a month so 'Billed $150 hourly' is a rate everywhere. Tests with reviewer strings incl. parametrized classifier-rate => gate-None. Verified: pytest test_reclassify.py test_billing.py 148 passed; tests/unit 1605 passed, 1 failed (test_api_routes export, judge j3 call failure, other agents' uncommitted judges.py work, not amounts). Commit 9c1af01. Surprised me: my first commit 57a08ba used a stale shared /tmp temp index and reverted 12 of T-085 r2's files; 9c1af01 restores them (net diff vs 1b1c711 is only my 3 files). F3/F4 minors left open.

9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
9c1af01da6c7ec3dfc1f3f48faf035705bea8866
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:23.783Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i T-084; ls -la reviews/T-084-staff-engineer-r4.md 2>&1; git rev-parse HEAD; git status --short | head -20; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/head_9c1af01\" && git archive 9c1af01 | tar -x -C \"$S/head_9c1af01\" && ls \"$S/head_9c1af01\" | head -40",
 "description": "Check for existing r4 file, pin HEAD via git archive into scratchpad"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:24.111Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md"
}
````

### User / tool · 2026-11-02T04:56:24.242Z

**tool result**
````
T-084-staff-engineer-r2.md
T-084-staff-engineer-r3.md
T-084-staff-engineer.md
ls: reviews/T-084-staff-engineer-r4.md: No such file or directory
9c1af01da6c7ec3dfc1f3f48faf035705bea8866
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
MM .claude/agent-memory/qa/MEMORY.md
D  .claude/agent-memory/qa/project_judge_controls.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/amounts.py
 M app/backend/api.py
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
````

### User / tool · 2026-11-02T04:56:24.254Z

**tool result**
````
1	---
2	name: t073-t084-review-patterns
3	description: T-073 r1 (7724412) narrowed catch, real path retries bugs; T-084 r1 (ec33bf0) restore bypass, rate phrase, commit deleted T-083 billing; r2 (c8a9874, HEAD a850be0) commit fails its own tree, class-only restore untested, gate passes classifier-rate phrasings
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
18	## r2 (c8a9874 + e2b4e3f, HEAD a850be0; reviews/T-073-staff-engineer-r2.md pass, reviews/T-084-staff-engineer-r3.md changes)
19	
20	- **A fix commit can fail its own tree while the working tree is green.** c8a9874 alone: 9 of 120 fail (IntegrityError at reclassify.py:90) because it set AUDIT_ACTION to 'reclassify' while 2fca530 had removed the schema CHECK entry; the worker's runs were on a working tree that still had the T-095 schema uncommitted. A reclassify request 500'd and left the item changed with no audit row. Closed at HEAD by 6feb2ff (T-095 restore). **Why:** worker test runs use the working tree. **How to apply:** run the card's test files on `git archive <card commit>` as well as HEAD, and check any schema or migration the constants depend on. See [[project_t095_head_revert_patterns]].
21	- **Two-arm predicate with one arm untested:** `_may_restore` skips the checks only when the class AND the sentence are unchanged. The tests changed both together, so dropping the class clause passed all 139 tests (mutant T84-3). The code was right; the test was missing. **How to apply:** for each `and`-clause of a guard predicate, write a test where only that input changes, and mutate each clause separately.
22	- **Gate and classifier disagree on the same sentence:** charge_wording used its own rate-cue list; amounts.classify uses `_UNIT` (hour, unit, appointment). Six phrasings the classifier calls rates ("Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.") passed the gate, so the judge was the only gate. **How to apply:** run both functions on the same fixture sentences and list the disagreements (probe_classifier_vs_wording_gate.py pattern).
23	- **Restored sentence-arm mutants were caught;** the class-only arm was not. The worker's "17 rate cues" test pinned the named strings, not the classifier's vocabulary.
24	- **Handoff cites a card that is unrelated:** T-073's deferral said "T-094"; `board.py show T-094` is a live ship-bar card. **How to apply:** for every card a handoff names, check `board.py show` returns the matching work.
25	- **Probe and mutant indexing:** mutate_r2 writes m00..m10 in list order (control is m00, T84-3 is m03). I ran the T84-4 mutant (m04) by mistake once; check the directory name against the log before a probe.
26	
27	Related: [[project_backend_llm_review_patterns]] (judge reason prose, label-window bleed), [[project_r2_fix_verification_patterns]] (partial fixes), [[project_t095_head_revert_patterns]] (the 2fca530 revert, closed by 6feb2ff), [[feedback_review_write_once]] (the JSON block in the first Write).
28	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:24.333Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md"
}
````

### User / tool · 2026-11-02T04:56:24.339Z

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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:31.548Z

**tool call — Bash**
````
{
 "command": "git show --stat 9c1af01 | head -30; echo ---; git show --stat 57a08ba | head -30; echo ---; git log --oneline -3 -- app/backend/reclassify.py app/backend/amounts.py tests/unit/test_reclassify.py; echo ---; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/head_9c1af01\" && grep -n \"RATE_CUE\\|_RATE\\|def charge_wording\\|def _may_restore\\|code_class\\|def reclassify\\|NO_CHARGE_WORDING\\|JUDGE_UNAVAILABLE\" app/backend/reclassify.py; echo ---; grep -n \"RATE_CUE\\|_RATE_AFTER\\|_UNIT\\|def classify\" app/backend/amounts.py",
 "description": "Show commit stat and locate gate and restore logic in pinned HEAD"
}
````

### User / tool · 2026-11-02T04:56:31.723Z

**tool result**
````
commit 9c1af01da6c7ec3dfc1f3f48faf035705bea8866
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:55:49 2026 -0600

    fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
    
    57a08ba picked up a stale temp index and reverted 12 files of 1b1c711. This commit puts them back byte-for-byte; the only net change from 1b1c711 is the T-084 r3 amounts.py, reclassify.py and test_reclassify.py edits.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/confidence.py                  |   2 +-
 app/backend/generator.py                   |   8 +-
 app/backend/language.py                    | 158 +++++++++++++------
 app/backend/pipeline.py                    |  10 +-
 app/backend/review.py                      |   4 +-
 app/backend/spanish.py                     |   6 +-
 app/backend/spanish_text.py                |  77 +++++++---
 app/backend/why.py                         |   1 +
 memory/contracts/api.md                    |   8 +-
 tests/unit/spanish_translation_pairs.jsonl |  54 +++++++
 tests/unit/test_spanish_failsafe.py        | 238 +++++++++++++++++++++++++++++
 tests/unit/test_spanish_records.py         |   7 +-
 12 files changed, 485 insertions(+), 88 deletions(-)
---
commit 57a08ba1a14af2e3e206e151cd63ae0ddde1ca84
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 22:55:30 2026 -0600

    fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/amounts.py                     |   5 +-
 app/backend/confidence.py                  |   2 +-
 app/backend/generator.py                   |   8 +-
 app/backend/language.py                    | 158 ++++++-------------
 app/backend/pipeline.py                    |  10 +-
 app/backend/reclassify.py                  |   7 +-
 app/backend/review.py                      |   4 +-
 app/backend/spanish.py                     |   6 +-
 app/backend/spanish_text.py                |  77 +++-------
 app/backend/why.py                         |   1 -
 memory/contracts/api.md                    |   8 +-
 tests/unit/spanish_translation_pairs.jsonl |  54 -------
 tests/unit/test_reclassify.py              |  73 +++++++++
 tests/unit/test_spanish_failsafe.py        | 238 -----------------------------
 tests/unit/test_spanish_records.py         |   7 +-
 15 files changed, 170 insertions(+), 488 deletions(-)
---
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
8bc7f90 fix(backend): billing never totals per-visit rate rows, lists unparsed CMS-1500/ledger rows as unreconciled, verifier runs on the route, unreadable provider is not $0 (T-083 r2)
c8a9874 fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
---
31:_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
37:    "NO_CHARGE_WORDING": "The sentence with this figure has no wording that says it was charged or billed (such as charged, billed, invoiced or amount due), so it stays a figure that is not a charge.",
40:    "JUDGE_UNAVAILABLE": "The second AI check did not run or did not finish, so this figure cannot become a charge yet. Try again.",
69:def charge_wording(excerpt: str, row: dict, rec=None):
77:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
84:    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
97:def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
148:def _may_restore(row: dict, prior: dict, original: str) -> bool:
156:    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])
167:        raise _refuse("NO_CHARGE_WORDING")
169:        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
173:        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
193:    ladder = {**old["ladder"], "reclassification": {**rc, "rerun": {"code_class": it["cls"], "excerpt_sha": _sha(it.get("excerpt"))}}}     # what the code says now
200:    async def reclassify_item(token: str, item_id: str, request: Request):
---
14:_UNIT = r"(?:visit|session|treatment|hour|hr|day|unit|appointment|procedure|adjustment)s?"
15:_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
16:_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
19:_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
27:RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
28:_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)
34:    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))
68:def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
76:    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:34.505Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && echo \"== reclassify.py 25-95, 140-200 ==\" && sed -n '25,35p;66,96p;145,160p;160,195p' app/backend/reclassify.py && echo \"== amounts.py 1-40 ==\" && sed -n '1,40p' app/backend/amounts.py && echo \"== amounts.py classify ==\" && sed -n '66,80p' app/backend/amounts.py",
 "description": "Read gate, restore and amounts rate-cue code at pinned HEAD"
}
````

### User / tool · 2026-11-02T04:56:34.609Z

**tool result**
````
== reclassify.py 25-95, 140-200 ==
TARGETS = ("charge", "not_a_charge")
NOT_A_CHARGE_KIND = "unclear"
AUDIT_ACTION = "reclassify"      # review_events.action (schema v4, T-095)
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
_WORDING = re.compile(r"\b(?:charged|charges?|billed|invoiced|amount\s+due|balance\s+due|total\s+billed)\b", re.IGNORECASE)
# a rate cue is decisive: the figure is a unit price, whatever else the sentence says (D-042 reading, T-084 r2)
_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
_NEGATED = re.compile(r"\b(?:not|never|no|without|unbilled|uncharged)\s+(?:\w+\s+)?(?:charged|charges?|billed|invoiced)\b|\b(?:unbilled|uncharged)\b", re.IGNORECASE)

REFUSALS = {
    "NO_VALUE": "The dollar value of this figure could not be read, so it cannot become a charge.",
    return A.classify(excerpt, {"start": start, "end": end, "cents": 1}) == "rate"


def charge_wording(excerpt: str, row: dict, rec=None):
    """Code check: the charged-amount phrase in the figure's own sentence (every occurrence of the figure must have one, no negation, no rate
    cue), or None. A rate cue decides: "Charge per visit $185" and "Billed $150 per visit" are rates."""
    spans = _figure_spans(excerpt or "", row, rec)
    found = None
    for s, _e in spans:
        sent = next((t for a, b, t in _sentences(excerpt) if a <= s <= b), "")
        m = _WORDING.search(sent)
        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
            return None
        found = found or m.group(0)
    return found


def _refuse(reason: str, **detail):
    return review.ReviewError(422, "reclassify_refused", {"reason": reason, "check": "code" if reason in ("NO_VALUE", "INJECTION_SUSPECTED", "NO_CHARGE_WORDING") else "judge",
                                                          **detail}, REFUSALS[reason])


def _sha(text) -> str:
    return hashlib.sha256((text or "").encode("utf-8")).hexdigest()[:16]


def _log(conn, case_id, item_id, before, after, t):
    conn.execute("INSERT INTO review_events (id, case_id, item_id, action, before_json, after_json, at) VALUES (?,?,?,?,?,?,?)",
                 (DB._tok("v"), case_id, item_id, AUDIT_ACTION, DB._enc(before), DB._enc(after), t))


                                           "restored": restored}, [])


def _may_restore(row: dict, prior: dict, original: str) -> bool:
    """Undoing her own demotion may skip both checks only while the code's original call still stands: the figure was a charge and has a judge
    answer, and no rerun has since changed the code's class of the figure or its sentence. Otherwise the guard runs in full."""
    if original != "charge" or prior.get("previous_judge") is None:
        return False
    rerun = prior.get("rerun")
    if rerun is None:
        return prior.get("excerpt_sha") in (None, _sha(row["excerpt"]))
    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])


def _guard(row: dict, rec, call):
    """The two checks for putting a figure into the total, code first. Returns (wording, {'judge': ladder judge dict}) or raises 422."""
    """The two checks for putting a figure into the total, code first. Returns (wording, {'judge': ladder judge dict}) or raises 422."""
    if row["value_cents"] is None:
        raise _refuse("NO_VALUE")
    if rec is not None and rec.get("injection_tag"):
        raise _refuse("INJECTION_SUSPECTED")
    wording = charge_wording(row["excerpt"], row, rec)
    if wording is None:
        raise _refuse("NO_CHARGE_WORDING")
    if call is None:
        raise _refuse("JUDGE_UNAVAILABLE", wording=wording)
    verdict, call_id, code, err = judge_guard.guarded(judges.run_j2_meta, row["excerpt"], row["text"], "charge", call=call, item_id=row["id"])
    ladder_verdict = judges.to_ladder("j2", verdict)
    if ladder_verdict != "supported":
        reason = {"disagrees": "JUDGE_DISAGREES", "unsure": "JUDGE_UNSURE"}.get(ladder_verdict, "JUDGE_UNAVAILABLE")
        raise _refuse(reason, wording=wording, **({"error_class": err} if err else {}))
    return wording, {"judge": {"model": judges.judge_model(), "prompt_version": "judge_amount_class_v1", "call_id": call_id, "verdict": verdict,
                               "reason_code": code}}


def _result(conn, case_id, item_id, change, warnings):
    from app.backend import present
    amount = present._VIEW["amount"](DB.get_item(conn, item_id, case_id), present._recs_by_id(conn, case_id))     # the GET /cases shape: `kind` is the class
    return {"item": present.item_view(conn, case_id, item_id), "amount": amount, "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "reclassified": change, "warnings": warnings}


def carry_over(old: dict, it: dict) -> dict:
    """pipeline._persist hook: a rerun re-derives the code's class, but a figure the paralegal reclassified keeps her class (same figure only)."""
    rc = (old.get("ladder") or {}).get("reclassification")
    if not rc or old["kind"] == it["cls"] or old["text"] != it["text"] or old["value_cents"] != it["cents"]:
        return it
    if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(it.get("excerpt")):      # her promotion was checked against another sentence
        return it
    ladder = {**old["ladder"], "reclassification": {**rc, "rerun": {"code_class": it["cls"], "excerpt_sha": _sha(it.get("excerpt"))}}}     # what the code says now
    return {**it, "cls": old["kind"], "kind": old["kind"], "state": old["state"], "reasons": old["state_reasons"], "ladder": ladder,
            "why": " ".join(WHY.why(c) for c in old["state_reasons"])}
== amounts.py 1-40 ==
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
_RATE_WORD = re.compile(rf"\b(?:(?:per|each)[\s-]+{_UNIT}|rate\s+of)\b|/\s*{_UNIT}\b", re.IGNORECASE)
_RATE_AFTER = re.compile(rf"^\s*(?:(?:per|each|an?)[\s-]+{_UNIT}\b|/\s*{_UNIT}\b|each\b|(?:hourly|daily|weekly|monthly|apiece)\b|an?\s+(?:month|week)\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)(?:\s+per\s+(?!(?:%s)\b)[\w#-]+(?:\s+[\w#-]+)?)?\s*:?\s*$" % _UNIT, re.IGNORECASE)
# ONE rate-cue test for every code path that decides "is this figure a unit price?" (reclassify.py wording gate, billing.py ledger rows and
# sentences). A cue is decisive: "Charge per visit $185" and "Billed $150 per visit" state a rate, whatever else the text says (D-042, T-084 r2).
_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
              r"|\ban?\s+(?:visit|session|hour|hr|day|treatment|appointment|unit|procedure|month|week)\b|\b(?:daily|hourly|weekly|monthly|session|visit|unit|flat)\s+(?:rate|fee|price|cost)\b|\brate\b"
              r"|\b(?:hourly|daily|weekly|monthly|apiece)\b|\bunit\s+(?:price|cost|charge)\b|@\s*\$"
              r"|\b\d+\s*[x\u00d7]\s*\$?\d")
_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)


def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
    """True when the text carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate, rate of ...). `unit_notation=True` is for a
    ledger row's description, where "x1" / "x2" is the unit count of a normal charge line and not a multiplier."""
    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))


_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
== amounts.py classify ==


def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
    needs it to be a billing document."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:36.015Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && grep -n \"^def \\|^async def \\|class-only\\|class_only\\|T-084\\|def test_\" tests/unit/test_reclassify.py | head -120",
 "description": "List test functions in pinned test_reclassify.py"
}
````

### User / tool · 2026-11-02T04:56:36.106Z

**tool result**
````
1:"""T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun."""
43:def seeded(tmp_path, judge="agree"):
50:def kinds(conn, cid):
54:def aid(conn, cid, text, rec):
58:def events(conn, cid, item_id):
62:def test_fixture_classes_are_what_the_tests_assume(tmp_path):
70:def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
84:def test_same_direction_is_a_noop_without_an_event(tmp_path):
91:def test_undoing_her_own_demotion_restores_the_code_class_without_a_judge(tmp_path):
102:def test_rate_without_charge_wording_is_422_and_the_judge_is_never_asked(tmp_path):
112:def test_negated_wording_does_not_count(tmp_path):
119:def test_figure_with_charge_wording_and_judge_agreement_becomes_a_pending_verified_charge(tmp_path):
135:def test_judge_objection_is_422_and_changes_nothing(tmp_path, verdict, code, reason):
145:def test_judge_that_cannot_answer_is_422_judge_unavailable(tmp_path, call):
153:def test_unexpected_judge_bug_propagates(tmp_path):
162:def test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge(tmp_path, rec, text):
178:def test_rate_cues_are_decisive(sentence):
184:UNIT_PRICE_SENTENCES = [        # T-084 r3 F2 (reviewer strings) + the brief's phrasings
191:def test_every_unit_price_phrasing_is_refused_by_the_code_gate(sentence):
199:def test_classifier_rate_implies_the_wording_gate_refuses(sentence):
210:def test_unit_price_phrasings_are_refused_before_the_judge(tmp_path, sentence):
224:def test_plain_charge_statements_still_pass_the_wording_check(sentence):
232:def rerun(conn, cid, text):
237:def test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again(tmp_path):
258:def _class_only_flip(tmp_path, monkeypatch):
274:def test_restore_after_a_class_only_change_needs_the_judge_again(tmp_path, monkeypatch):
276:    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
285:def test_class_only_change_restore_with_a_judge_runs_the_judge_once_and_is_not_a_restore(tmp_path, monkeypatch):
286:    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
292:def test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again(tmp_path):
306:def test_restore_after_an_unchanged_rerun_still_needs_no_judge(tmp_path):
316:def test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence(tmp_path):
327:def test_bad_body_non_amount_and_rejected_item(tmp_path):
346:def test_injection_tagged_record_and_missing_value_never_become_charges(tmp_path):
360:def test_charge_wording_unit():
371:def test_a_rerun_keeps_her_reclassification(tmp_path):
381:def test_route(tmp_path, monkeypatch):
395:def test_judge_unavailable_refusal_names_the_error_class(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:41.257Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && sed -n '160,292p' tests/unit/test_reclassify.py",
 "description": "Read unit-price and class-only restore tests at pinned HEAD"
}
````

### User / tool · 2026-11-02T04:56:41.341Z

**tool result**
````
@pytest.mark.parametrize("rec,text", [("r2", "$185"), ("r6", "$150")])
def test_a_rate_sentence_that_also_says_charge_or_billed_is_refused_before_the_judge(tmp_path, rec, text):
    """Reviewer strings: "Charge per visit $185" and "Billed $150 per visit" state a rate; a rate cue is decisive."""
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, text, rec)
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] == "rate" and not events(conn, cid, a)
    assert DB.get_item(conn, a, cid)["state"] == "needs_review"


@pytest.mark.parametrize("sentence", [
    "Charge per visit $185.", "Billed $150 per visit.", "Billed $150 per session.", "Charged $40 per hour.", "Billed $40 per day.",
    "Charged $90 each.", "Each visit billed $90.", "Billed $90/visit.", "Billed $90 /session.", "Billed $90 x 3.", "Billed $90 \u00d7 4.",
    "Billed 3 x $90.", "Daily rate billed $400.", "Billed $185 a visit.", "Billed at a rate of $185.", "Billed $90 per-visit.", "Billed $90, per unit."])
def test_rate_cues_are_decisive(sentence):
    ex = "Visit done. " + sentence
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    assert RC.charge_wording(ex, {"text": raw, "excerpt_start": None}) is None


UNIT_PRICE_SENTENCES = [        # T-084 r3 F2 (reviewer strings) + the brief's phrasings
    "Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.", "Billed $150 hourly.", "Charged $90 apiece.", "Billed $40 daily.",
    "Billed $200 a month.", "Billed unit price $90.", "Charged unit price of $90.", "Billed @ $90.", "Billed $90 @ each.", "Billed $90/visit.",
    "Billed at a rate of $90.", "Billed $90 weekly."]


@pytest.mark.parametrize("sentence", UNIT_PRICE_SENTENCES)
def test_every_unit_price_phrasing_is_refused_by_the_code_gate(sentence):
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    assert RC.charge_wording("Visit done. " + sentence, {"text": raw, "excerpt_start": None}) is None


@pytest.mark.parametrize("sentence", UNIT_PRICE_SENTENCES + [
    "Charge per visit $185.", "Billed $150 per visit.", "Billed $150 for every visit.", "Billed $185 for the visit.", "Charged $310.", "Total billed $185.",
    "Billed $90 x 3.", "Amount due $90 on receipt.", "Charge: $310.", "Not billed $90 per visit to this patient."])
def test_classifier_rate_implies_the_wording_gate_refuses(sentence):
    """One rate test, two readers: whenever amounts.classify calls the figure a rate, charge_wording returns None."""
    from app.backend import amounts as AM
    ex = "Visit done. " + sentence
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;").split("/")[0]
    a = next(x for x in AM.find_amounts(ex) if x["raw"].replace(" ", "") == raw)
    if AM.classify(ex, a) == "rate":
        assert RC.charge_wording(ex, {"text": a["raw"], "excerpt_start": None}) is None


@pytest.mark.parametrize("sentence", ["Charged $150 an hour.", "Charged $75 a unit.", "Billed $120 an appointment.", "Billed $150 hourly.", "Billed unit price $90."])
def test_unit_price_phrasings_are_refused_before_the_judge(tmp_path, sentence):
    conn, cid = seeded(tmp_path)
    text = TEXT.replace("Visit completed. $185 was billed to the patient.", "Visit completed. " + sentence)
    rerun(conn, cid, text)
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;")
    a = aid(conn, cid, raw, "r5")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert (e.value.status, e.value.detail["reason"], e.value.detail["check"]) == (422, "NO_CHARGE_WORDING", "code")
    assert call.log == [] and DB.get_item(conn, a, cid)["kind"] != "charge" and not events(conn, cid, a)


@pytest.mark.parametrize("sentence", ["Billed $185 for the visit.", "Total billed $185.", "Charged $310.", "Amount due $90 on receipt.", "The visit was billed at $185 in total."])
def test_plain_charge_statements_still_pass_the_wording_check(sentence):
    raw = "$" + sentence.split("$")[1].split()[0].rstrip(".,;")
    assert RC.charge_wording("Visit done. " + sentence, {"text": raw, "excerpt_start": None}) is not None


RATE_R3 = TEXT.replace('Excerpt: "MRI performed. Charge: $310."', 'Excerpt: "MRI performed. Rate of $310 per visit."')


def rerun(conn, cid, text):
    call = FakeCall(sample_script(extract=lambda u: dict(summary="Visit completed.", excerpt="Visit completed.")))
    PL.run_pipeline(conn, cid, text, call=call, now=lambda: 3.0)


def test_restore_after_a_rerun_that_made_the_figure_a_rate_runs_both_checks_again(tmp_path):
    """Reviewer F1: demote $310, rerun with the code now calling it a rate, restore with no judge: 422, the figure stays out of the total."""
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    rerun(conn, cid, RATE_R3)
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and row["ladder"]["reclassification"]["rerun"]["code_class"] == "rate"
    n = len(events(conn, cid, a))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert (e.value.status, e.value.detail["reason"]) == (422, "NO_CHARGE_WORDING")
    call = FakeCall(J2("agree"))
    with pytest.raises(RV.ReviewError):
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert call.log == []                                                                        # the code check stops it before the judge
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and row["state"] == "needs_review" and len(events(conn, cid, a)) == n
    assert present.totals_view(conn, cid)["pending"]["cents"] == 0


def _class_only_flip(tmp_path, monkeypatch):
    """Demote $310, then rerun with the SAME text but the amount classifier now calling $310 a rate (a lexicon/classifier change). Excerpt unchanged."""
    from app.backend import amounts as AM
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$310", "r3")
    RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
    real = AM.classify
    monkeypatch.setattr(AM, "classify", lambda ex, am, *x, **k: "rate" if am.get("cents") == 31000 else real(ex, am, *x, **k))
    rerun(conn, cid, TEXT)
    monkeypatch.setattr(AM, "classify", real)
    row = DB.get_item(conn, a, cid)
    rr = row["ladder"]["reclassification"]["rerun"]
    assert rr["code_class"] == "rate" and rr["excerpt_sha"] == row["ladder"]["reclassification"]["excerpt_sha"]      # class changed, sentence did not
    return conn, cid, a


def test_restore_after_a_class_only_change_needs_the_judge_again(tmp_path, monkeypatch):
    """T84-3: restore must not skip the checks when only the rerun's code class changed (identical excerpt)."""
    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
    n = len(events(conn, cid, a))
    with pytest.raises(RV.ReviewError) as e:
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=None)
    assert (e.value.status, e.value.detail["reason"]) == (422, "JUDGE_UNAVAILABLE")
    row = DB.get_item(conn, a, cid)
    assert row["kind"] == "unclear" and len(events(conn, cid, a)) == n and present.totals_view(conn, cid)["pending"]["cents"] == 0


def test_class_only_change_restore_with_a_judge_runs_the_judge_once_and_is_not_a_restore(tmp_path, monkeypatch):
    conn, cid, a = _class_only_flip(tmp_path, monkeypatch)
    call = FakeCall(J2("agree"))
    r = RC.reclassify(conn, cid, a, {"to": "charge"}, call=call)
    assert call.steps() == ["j2"] and r["reclassified"]["restored"] is False


def test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:56:59.048Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && ls -a | head -50; ls tests/ | head; ls tests/unit | grep -i \"conftest\\|__init__\"; cat pytest.ini setup.cfg 2>/dev/null | head -20; sed -n '1,42p' tests/unit/test_reclassify.py; ls /Users/arsis/zlayt-pm-project/.venv/bin/python && /Users/arsis/zlayt-pm-project/.venv/bin/python --version",
 "description": "Inspect pinned copy layout, pytest config and test helpers"
}
````

### User / tool · 2026-11-02T04:56:59.187Z

**tool result**
````
.
..
.claude
.gitignore
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
__init__.py
conftest.py
e2e
fixtures
unit
__init__.py
"""T-084 (D-042): guarded charge reclassification. Code wording check first, judge 2 second, 422 with a fixed reason otherwise; audited; survives a rerun."""
import pytest
from fastapi.testclient import TestClient
from app.backend import pipeline as PL, present, reclassify as RC, review as RV
from app.backend.api import create_app
from app.db import db as DB
from app.llm import audited as AU
from tests.unit._fakes import FakeCall, sample_script

TEXT = """=== Record 1 ===
Date: 2026-03-02
Source: Capital PT, visit 1
Excerpt: "Visit completed. Rate of $185 per visit."

=== Record 2 ===
Date: 2026-03-09
Source: Capital PT, visit 2
Excerpt: "Visit completed. Charge per visit $185."

=== Record 3 ===
Date: 2026-03-16
Source: Capital Imaging
Excerpt: "MRI performed. Charge: $310."

=== Record 4 ===
Date: 2026-03-23
Source: Capital PT, visit 4
Excerpt: "Visit completed. Not billed $90 per visit to this patient."

=== Record 5 ===
Date: 2026-03-30
Source: Capital PT, visit 5
Excerpt: "Visit completed. $185 was billed to the patient."

=== Record 6 ===
Date: 2026-04-06
Source: Capital PT, visit 6
Excerpt: "Visit completed. Billed $150 per visit."
"""
J2 = lambda v, code="NONE": {"j2": {"verdict": v, "reason_code": code}}     # noqa: E731


/Users/arsis/zlayt-pm-project/.venv/bin/python
Python 3.12.2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:05.774Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/head_9c1af01\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py 2>&1 | tail -25; echo \"exit=$?\"",
 "description": "Run reclassify and billing unit tests on pinned HEAD archive"
}
````

### User / tool · 2026-11-02T04:57:07.949Z

**tool result**
````
........................................................................ [ 48%]
........................................................................ [ 97%]
....                                                                     [100%]
148 passed in 1.75s
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:57:28.843Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/t84r4\" && cat > \"$S/t84r4/mutate_t84_r4.py\" <<'EOF'\n\"\"\"Scratch mutation driver for T-084 r4. Writes only under the scratchpad. Each mutant is a copy of the pinned git archive.\"\"\"\nimport shutil, subprocess, sys, pathlib\n\nBASE = pathlib.Path(sys.argv[1])           # pinned archive of HEAD (read-only source)\nSCR = pathlib.Path(sys.argv[2])            # scratch root for mutant copies\nVENV_PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n\nMUTANTS = [\n    # (name, file, old, new)\n    (\"M0_control\", None, None, None),\n    (\"T84-3_restore_ignores_code_class\", \"app/backend/reclassify.py\",\n     'rerun.get(\"code_class\") == \"charge\" and ', \"\"),\n    (\"T84-s_restore_ignores_sentence_sha\", \"app/backend/reclassify.py\",\n     'rerun.get(\"excerpt_sha\") == prior.get(\"excerpt_sha\") == _sha(row[\"excerpt\"])', \"True\"),\n    (\"G1_gate_ignores_shared_rate_cue\", \"app/backend/reclassify.py\",\n     \"or _RATE_CUE.search(sent) or\", \"or\"),\n    (\"G1b_gate_ignores_classifier_rate\", \"app/backend/reclassify.py\",\n     \" or _classified_rate(excerpt, s, _e)\", \"\"),\n    (\"G2_no_at_dollar_cue\", \"app/backend/amounts.py\",\n     '|@\\\\s*\\\\$\"', '\"'),\n    (\"G3_no_rate_of_cue\", \"app/backend/amounts.py\",\n     '|\\\\brate\\\\b\"', '\"'),\n    (\"G4_no_slash_visit_cue\", \"app/backend/amounts.py\",\n     \"/\\\\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\\\\b\", \"(?!)\"),\n    (\"G5_no_unit_price_cue\", \"app/backend/amounts.py\",\n     \"\\\\bunit\\\\s+(?:price|cost|charge)\\\\b|\", \"\"),\n]\n\nsummary = []\nfor name, rel, old, new in MUTANTS:\n    dst = SCR / name\n    if dst.exists():\n        shutil.rmtree(dst)\n    shutil.copytree(BASE, dst, symlinks=True, ignore=shutil.ignore_patterns(\"reviews\", \"board\", \"artifacts\", \"memory\", \".claude\"))\n    if rel:\n        p = dst / rel\n        src = p.read_text(encoding=\"utf-8\")\n        n = src.count(old)\n        if n != 1:\n            summary.append(f\"{name}: APPLY FAILED, pattern count={n}\")\n            continue\n        p.write_text(src.replace(old, new), encoding=\"utf-8\")\n    r = subprocess.run([VENV_PY, \"-I\", \"-m\", \"pytest\", \"-q\", \"-rf\", \"-p\", \"no:cacheprovider\",\n                        \"tests/unit/test_reclassify.py\", \"tests/unit/test_billing.py\"],\n                       cwd=dst, capture_output=True, text=True, env={\"PYTHONDONTWRITEBYTECODE\": \"1\", \"PATH\": \"/usr/bin:/bin\"})\n    lines = [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\") or \" passed\" in l or \" failed\" in l]\n    summary.append(f\"{name}: rc={r.returncode} | \" + \" || \".join(lines[-12:]))\nprint(\"\\n\".join(summary))\nEOF\ncd \"$S/t84r4\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I mutate_t84_r4.py \"$S/head_9c1af01\" \"$S/t84r4/mutants\" 2>&1 | tee \"$S/t84r4/mutation-run-r4.txt\"",
 "description": "Run scratch mutants of the wording gate and restore predicate"
}
````

### User / tool · 2026-11-02T04:57:49.006Z

**tool result**
````
M0_control: rc=0 | 148 passed in 1.63s
T84-3_restore_ignores_code_class: rc=1 | FAILED tests/unit/test_reclassify.py::test_restore_after_a_class_only_change_needs_the_judge_again || FAILED tests/unit/test_reclassify.py::test_class_only_change_restore_with_a_judge_runs_the_judge_once_and_is_not_a_restore || 2 failed, 146 passed in 1.61s
T84-s_restore_ignores_sentence_sha: rc=1 | FAILED tests/unit/test_reclassify.py::test_restore_after_a_rerun_that_changed_the_sentence_needs_the_judge_again || 1 failed, 147 passed in 1.67s
G1_gate_ignores_shared_rate_cue: rc=1 | FAILED tests/unit/test_reclassify.py::test_rate_cues_are_decisive[Billed $90 x 3.] || FAILED tests/unit/test_reclassify.py::test_rate_cues_are_decisive[Billed $90 \xd7 4.] || FAILED tests/unit/test_reclassify.py::test_rate_cues_are_decisive[Billed 3 x $90.] || FAILED tests/unit/test_reclassify.py::test_rate_cues_are_decisive[Daily rate billed $400.] || FAILED tests/unit/test_reclassify.py::test_rate_cues_are_decisive[Billed $90, per unit.] || FAILED tests/unit/test_reclassify.py::test_every_unit_price_phrasing_is_refused_by_the_code_gate[Billed unit price $90.] || FAILED tests/unit/test_reclassify.py::test_every_unit_price_phrasing_is_refused_by_the_code_gate[Charged unit price of $90.] || FAILED tests/unit/test_reclassify.py::test_every_unit_price_phrasing_is_refused_by_the_code_gate[Billed @ $90.] || FAILED tests/unit/test_reclassify.py::test_every_unit_price_phrasing_is_refused_by_the_code_gate[Billed $90 @ each.] || FAILED tests/unit/test_reclassify.py::test_unit_price_phrasings_are_refused_before_the_judge[Billed unit price $90.] || 10 failed, 138 passed in 1.73s
G1b_gate_ignores_classifier_rate: rc=0 | 148 passed in 1.72s
G2_no_at_dollar_cue: rc=1 | FAILED tests/unit/test_reclassify.py::test_every_unit_price_phrasing_is_refused_by_the_code_gate[Billed @ $90.] || 1 failed, 147 passed in 1.61s
G3_no_rate_of_cue: rc=0 | 148 passed in 1.56s
G4_no_slash_visit_cue: rc=1 | FAILED tests/unit/test_billing.py::test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Charge /visit] || 1 failed, 147 passed in 1.71s
G5_no_unit_price_cue: rc=0 | 148 passed in 1.66s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:06.436Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/t84r4/probe_gate_layers_t84_r4.py\" <<'EOF'\n\"\"\"Scratch probe (T-084 r4): which layer refuses each unit-price sentence. Run with -I; argv[1] is an archive root (read-only use).\"\"\"\nimport sys\nroot = sys.argv[1]\nsys.path.insert(0, root)\nfrom app.backend import amounts as AM, reclassify as RC\n\nSENTENCES = [\n    \"Billed unit price $90.\", \"Charged unit price of $90.\", \"Billed at a rate of $90.\", \"Billed @ $90.\",\n    \"Billed $90/visit.\", \"Billed $90 /visit.\", \"Charged $150 an hour.\", \"Charged $75 a unit.\",\n    \"Billed $120 an appointment.\", \"Billed $150 hourly.\", \"Billed $185 for the visit.\", \"Charged $310.\",\n]\nprint(f\"root={root}\")\nprint(f\"{'sentence':34} {'cue':>4} {'classify':>9} {'wording_gate':>13}\")\nfor s in SENTENCES:\n    ex = \"Visit done. \" + s\n    raw = \"$\" + s.split(\"$\")[1].split()[0].rstrip(\".,;\").split(\"/\")[0]\n    cue = bool(AM.RATE_CUE.search(s))\n    a = next((x for x in AM.find_amounts(ex) if x[\"raw\"].replace(\" \", \"\") == raw), None)\n    cls = AM.classify(ex, a) if a else \"NO_AMOUNT\"\n    gate = RC.charge_wording(ex, {\"text\": raw, \"excerpt_start\": None})\n    print(f\"{s:34} {str(cue):>4} {cls:>9} {('refused' if gate is None else 'passes:' + gate):>13}\")\nEOF\ncd \"$S/t84r4\" && for d in \"$S/head_9c1af01\" \"$S/t84r4/mutants/G3_no_rate_of_cue\" \"$S/t84r4/mutants/G5_no_unit_price_cue\"; do PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/t84r4/probe_gate_layers_t84_r4.py\" \"$d\"; echo; done 2>&1 | tee \"$S/t84r4/gate-layers-run-r4.txt\"",
 "description": "Probe which gate layer refuses each unit-price sentence"
}
````

### User / tool · 2026-11-02T04:58:07.393Z

**tool result**
````
root=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01
sentence                            cue  classify  wording_gate
Billed unit price $90.             True    charge       refused
Charged unit price of $90.         True   unclear       refused
Billed at a rate of $90.           True      rate       refused
Billed @ $90.                      True    charge       refused
Billed $90/visit.                  True      rate       refused
Billed $90 /visit.                 True      rate       refused
Charged $150 an hour.              True      rate       refused
Charged $75 a unit.                True      rate       refused
Billed $120 an appointment.        True      rate       refused
Billed $150 hourly.                True      rate       refused
Billed $185 for the visit.         False    charge passes:Billed
Charged $310.                      False   unclear passes:Charged

root=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t84r4/mutants/G3_no_rate_of_cue
sentence                            cue  classify  wording_gate
Billed unit price $90.             True    charge       refused
Charged unit price of $90.         True   unclear       refused
Billed at a rate of $90.           False      rate       refused
Billed @ $90.                      True    charge       refused
Billed $90/visit.                  True      rate       refused
Billed $90 /visit.                 True      rate       refused
Charged $150 an hour.              True      rate       refused
Charged $75 a unit.                True      rate       refused
Billed $120 an appointment.        True      rate       refused
Billed $150 hourly.                True      rate       refused
Billed $185 for the visit.         False    charge passes:Billed
Charged $310.                      False   unclear passes:Charged

root=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t84r4/mutants/G5_no_unit_price_cue
sentence                            cue  classify  wording_gate
Billed unit price $90.             True    charge       refused
Charged unit price of $90.         True   unclear       refused
Billed at a rate of $90.           True      rate       refused
Billed @ $90.                      True    charge       refused
Billed $90/visit.                  True      rate       refused
Billed $90 /visit.                 True      rate       refused
Charged $150 an hour.              True      rate       refused
Charged $75 a unit.                True      rate       refused
Billed $120 an appointment.        True      rate       refused
Billed $150 hourly.                True      rate       refused
Billed $185 for the visit.         False    charge passes:Billed
Charged $310.                      False   unclear passes:Charged
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:27.544Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf \"$S/t84r4/probe_head\" && cp -R \"$S/head_9c1af01\" \"$S/t84r4/probe_head\" && cat > \"$S/t84r4/probe_head/tests/unit/test_zz_t84_r4_probe.py\" <<'EOF'\n\"\"\"Scratch probe (T-084 r4), not product: the four brief phrasings through the real reclassify path must 422 before any judge call.\"\"\"\nimport pytest\nfrom app.backend import reclassify as RC, review as RV\nfrom app.db import db as DB\nfrom tests.unit.test_reclassify import TEXT, seeded, aid, rerun, FakeCall, J2\n\n\n@pytest.mark.parametrize(\"sentence\", [\"Billed unit price $90.\", \"Billed @ $90.\", \"Billed $90/visit.\", \"Billed at a rate of $90.\", \"Billed $90 /visit.\"])\ndef test_brief_phrasing_refused_before_judge_on_real_path(tmp_path, sentence):\n    conn, cid = seeded(tmp_path)\n    text = TEXT.replace(\"Visit completed. $185 was billed to the patient.\", \"Visit completed. \" + sentence)\n    rerun(conn, cid, text)\n    raw = \"$\" + sentence.split(\"$\")[1].split()[0].rstrip(\".,;\").split(\"/\")[0]\n    a = aid(conn, cid, raw, \"r5\")\n    call = FakeCall(J2(\"agree\"))\n    with pytest.raises(RV.ReviewError) as e:\n        RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=call)\n    assert (e.value.status, e.value.detail[\"reason\"], e.value.detail[\"check\"]) == (422, \"NO_CHARGE_WORDING\", \"code\")\n    assert call.log == [] and DB.get_item(conn, a, cid)[\"kind\"] != \"charge\"\nEOF\ncd \"$S/t84r4/probe_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -rf tests/unit/test_zz_t84_r4_probe.py 2>&1 | tail -30; echo \"--- billing/shared-cue users:\"; grep -rn \"RATE_CUE\\|has_rate_cue\" \"$S/head_9c1af01/app\" | grep -v \"^.*#\" | head",
 "description": "Run probe test through real reclassify path and grep shared cue users"
}
````

### User / tool · 2026-11-02T04:58:29.223Z

**tool result**
````
.....                                                                    [100%]
5 passed in 0.76s
--- billing/shared-cue users:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/billing.py:190:        if line["billed"] is not None and A.has_rate_cue(desc, unit_notation=True):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/billing.py:256:            if cls == "rate" or (kind is None and cls == "charge" and A.has_rate_cue(seg)):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/reclassify.py:77:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/amounts.py:27:RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/amounts.py:28:_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/amounts.py:31:def has_rate_cue(text: str, unit_notation: bool = False) -> bool:
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01/app/backend/amounts.py:34:    return bool((_RATE_CUE_ROW if unit_notation else RATE_CUE).search(text or ""))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:47.378Z

**tool call — Bash**
````
{
 "command": "echo \"== net diff 1b1c711..9c1af01\"; git diff --stat 1b1c711 9c1af01; echo \"== 57a08ba..9c1af01\"; git diff --stat 57a08ba 9c1af01 | tail -1; echo \"== does 9c1af01 touch T-084 files?\"; git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py; echo \"(end)\"; echo \"== 57a08ba stat T-084 files\"; git show --stat --format= 57a08ba -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py; echo \"== card commits vs 57a08ba in log\"; git log --oneline 1b1c711..9c1af01; echo \"== HEAD grep lines\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && grep -n \"update_item\\|batch_apply\\|_log(conn\\|dropped\\|SENTENCE_CHANGED\\|return it$\\|def test_a_promoted\" app/backend/reclassify.py tests/unit/test_reclassify.py; sed -n '316,326p' tests/unit/test_reclassify.py; echo \"== 1b1c711 vs HEAD amounts/reclassify ident?\"; cd /Users/arsis/zlayt-pm-project && git diff --stat 1b1c711 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py | tail -1",
 "description": "Check commit ranges, T-084 file ownership in commits, and open minors at HEAD"
}
````

### User / tool · 2026-11-02T04:58:47.583Z

**tool result**
````
== net diff 1b1c711..9c1af01
 app/backend/amounts.py        |  5 +--
 app/backend/reclassify.py     |  7 ++++-
 tests/unit/test_reclassify.py | 73 +++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 82 insertions(+), 3 deletions(-)
== 57a08ba..9c1af01
 12 files changed, 485 insertions(+), 88 deletions(-)
== does 9c1af01 touch T-084 files?
(end)
== 57a08ba stat T-084 files
 app/backend/amounts.py        |  5 +--
 app/backend/reclassify.py     |  7 ++++-
 tests/unit/test_reclassify.py | 73 +++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 82 insertions(+), 3 deletions(-)
== card commits vs 57a08ba in log
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
== HEAD grep lines
tests/unit/test_reclassify.py:316:def test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence(tmp_path):
tests/unit/test_reclassify.py:340:    DB.update_item(conn, a, now=2.0, case=cid, state="rejected")
tests/unit/test_reclassify.py:349:    DB.update_item(conn, a, now=2.0, case=cid, value_cents=None)
tests/unit/test_reclassify.py:353:    DB.update_item(conn, a, now=2.0, case=cid, value_cents=18500)
app/backend/reclassify.py:14:- A rerun keeps her class for the same figure; a charge she promoted is dropped back to the code's class if the sentence under it changed.
app/backend/reclassify.py:92:def _log(conn, case_id, item_id, before, after, t):
app/backend/reclassify.py:138:    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
app/backend/reclassify.py:140:        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
app/backend/reclassify.py:141:    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
app/backend/reclassify.py:190:        return it
app/backend/reclassify.py:192:        return it
def test_a_promoted_charge_is_dropped_when_a_rerun_changes_its_sentence(tmp_path):
    conn, cid = seeded(tmp_path)
    a = aid(conn, cid, "$185", "r5")
    RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
    rerun(conn, cid, TEXT)                                                                        # same sentence: her class is kept
    assert DB.get_item(conn, a, cid)["kind"] == "charge"
    rerun(conn, cid, TEXT.replace("$185 was billed to the patient.", "$185 was billed to the patient per visit."))
    assert DB.get_item(conn, a, cid)["kind"] != "charge"


# ---------------------------------------------------------------- structure
== 1b1c711 vs HEAD amounts/reclassify ident?
 3 files changed, 82 insertions(+), 3 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:58:57.207Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && rm -rf \"$S/c57a08ba\" && mkdir -p \"$S/c57a08ba\" && git archive 57a08ba | tar -x -C \"$S/c57a08ba\" && cd \"$S/c57a08ba\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py 2>&1 | tail -3; echo \"== HEAD lines\"; sed -n '136,141p;186,192p' \"$S/head_9c1af01/app/backend/reclassify.py\"; echo \"== mutant dirs cleanup check\"; ls \"$S/t84r4/mutants\" | head -20",
 "description": "Test the T-084 r3 commit 57a08ba on its own archive and view open-minor lines"
}
````

### User / tool · 2026-11-02T04:58:57.279Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && rm -rf "$S/c57a08ba" && mkdir -p "$S/c57a08ba" && git archive 57a08ba has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:00.516Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/arch_57a08ba\" && cd /Users/arsis/zlayt-pm-project && git archive 57a08ba | tar -x -C \"$S/arch_57a08ba\" && cd \"$S/arch_57a08ba\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py 2>&1 | tail -3; echo \"== HEAD lines\"; sed -n '136,141p;186,192p' \"$S/head_9c1af01/app/backend/reclassify.py\"",
 "description": "Test commit 57a08ba on its own archive and view open-minor lines"
}
````

### User / tool · 2026-11-02T04:59:02.932Z

**tool result**
````
........................................................................ [ 97%]
....                                                                     [100%]
148 passed in 1.69s
== HEAD lines
        "previous_judge": lad.get("judge") if to == "not_a_charge" else prior.get("previous_judge")})
    before = {"kind": old_kind, "review_status": row["review_status"], "state": row["state"]}
    DB.update_item(conn, item_id, now=t, case=case_id, kind=new_kind, state=state, state_reasons_json=reasons, ladder=lad)
    if row["review_status"] != "pending":                                  # her earlier decision was about the old meaning
        review.batch_apply(conn, case_id, item_id, "reset", t)               # review.py is the only caller of DB.apply_review
    _log(conn, case_id, item_id, before, {"event": "reclassify", "kind": new_kind, "review_status": "pending", "wording": wording,
def carry_over(old: dict, it: dict) -> dict:
    """pipeline._persist hook: a rerun re-derives the code's class, but a figure the paralegal reclassified keeps her class (same figure only)."""
    rc = (old.get("ladder") or {}).get("reclassification")
    if not rc or old["kind"] == it["cls"] or old["text"] != it["text"] or old["value_cents"] != it["cents"]:
        return it
    if rc.get("to") == "charge" and rc.get("excerpt_sha") != _sha(it.get("excerpt")):      # her promotion was checked against another sentence
        return it
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:13.777Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/head_9c1af01; cd \"$S\" && grep -n '_RATE_CORE = \\|\\\\brate\\\\b\"\\|@\\\\s\\*\\\\\\$\"\\|unit\\\\s+(?:price\\|^RATE_CUE\\|_RATE_X_COUNT = \\|_RATE_CUE_ROW = ' app/backend/amounts.py; grep -n \"_RATE_CUE\\|def test_\\(every\\|classifier\\|unit_price\\|class_only\\|restore_after_a_class\\|rate_cues\\)\" app/backend/reclassify.py tests/unit/test_reclassify.py | head -20; grep -n \"if wording is None\\|raise _refuse(\\\"NO_CHARGE_WORDING\\\")\\|if call is None\" app/backend/reclassify.py; grep -n \"rerun.get(\\\"code_class\\\")\" app/backend/reclassify.py; grep -n \"def test_\" tests/unit/test_reclassify.py | sed -n '1,3p'",
 "description": "Pin exact line numbers at pinned HEAD for review citations"
}
````

### User / tool · 2026-11-02T04:59:13.899Z

**tool result**
````
22:_RATE_CORE = (r"\bper\b|\beach\b|\bevery\b|/\s*(?:visit|session|hr|hour|day|unit|treatment|appt|appointment|dose|injection)\b"
23:              r"|\ban?\s+(?:visit|session|hour|hr|day|treatment|appointment|unit|procedure|month|week)\b|\b(?:daily|hourly|weekly|monthly|session|visit|unit|flat)\s+(?:rate|fee|price|cost)\b|\brate\b"
24:              r"|\b(?:hourly|daily|weekly|monthly|apiece)\b|\bunit\s+(?:price|cost|charge)\b|@\s*\$"
26:_RATE_X_COUNT = r"(?<![\w$])[x\u00d7]\s*\d+\b"            # "x 14": a multiplier in a sentence, but plain unit notation ("Manual therapy x1") in a ledger row
27:RATE_CUE = re.compile(_RATE_CORE + "|" + _RATE_X_COUNT, re.IGNORECASE)
28:_RATE_CUE_ROW = re.compile(_RATE_CORE, re.IGNORECASE)
app/backend/reclassify.py:31:_RATE_CUE = A.RATE_CUE          # one shared rate-cue test (app/backend/amounts.py), also used by billing.py
app/backend/reclassify.py:77:        if not m or _NEGATED.search(sent) or _RATE_CUE.search(sent) or _classified_rate(excerpt, s, _e):
tests/unit/test_reclassify.py:178:def test_rate_cues_are_decisive(sentence):
tests/unit/test_reclassify.py:191:def test_every_unit_price_phrasing_is_refused_by_the_code_gate(sentence):
tests/unit/test_reclassify.py:199:def test_classifier_rate_implies_the_wording_gate_refuses(sentence):
tests/unit/test_reclassify.py:210:def test_unit_price_phrasings_are_refused_before_the_judge(tmp_path, sentence):
tests/unit/test_reclassify.py:274:def test_restore_after_a_class_only_change_needs_the_judge_again(tmp_path, monkeypatch):
tests/unit/test_reclassify.py:285:def test_class_only_change_restore_with_a_judge_runs_the_judge_once_and_is_not_a_restore(tmp_path, monkeypatch):
166:    if wording is None:
167:        raise _refuse("NO_CHARGE_WORDING")
168:    if call is None:
156:    return rerun.get("code_class") == "charge" and rerun.get("excerpt_sha") == prior.get("excerpt_sha") == _sha(row["excerpt"])
62:def test_fixture_classes_are_what_the_tests_assume(tmp_path):
70:def test_charge_to_not_a_charge_is_allowed_leaves_the_total_and_is_audited(tmp_path):
84:def test_same_direction_is_a_noop_without_an_event(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:31.653Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat >> \"$S/t84r4/probe_head/tests/unit/test_zz_t84_r4_probe.py\" <<'EOF'\n\n\ndef test_zz_f3_audit_write_failure_leaves_item_changed(tmp_path, monkeypatch):\n    \"\"\"r3 F3 at HEAD: the item update commits before the audit row; a failing audit write leaves the item changed (expected: unchanged).\"\"\"\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r5\")\n    def boom(*x, **k):\n        raise RuntimeError(\"audit write failed\")\n    monkeypatch.setattr(RC, \"_log\", boom)\n    with pytest.raises(RuntimeError):\n        RC.reclassify(conn, cid, a, {\"to\": \"not_a_charge\"}, call=None)\n    assert DB.get_item(conn, a, cid)[\"kind\"] == \"charge\"\n\n\ndef test_zz_f4_promoted_charge_drop_is_silent(tmp_path):\n    \"\"\"r3 F4 at HEAD: after a sentence change the promotion record is gone and nothing names the drop (expected: a dropped marker).\"\"\"\n    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \"$185\", \"r5\")\n    RC.reclassify(conn, cid, a, {\"to\": \"charge\"}, call=FakeCall(J2(\"agree\")))\n    rerun(conn, cid, TEXT.replace(\"$185 was billed to the patient.\", \"$185 was billed to the patient per visit.\"))\n    rc = DB.get_item(conn, a, cid)[\"ladder\"].get(\"reclassification\")\n    print(\"\\nF4 ladder.reclassification after sentence change =\", rc)\n    assert rc is not None and rc.get(\"dropped\") == \"SENTENCE_CHANGED\"\nEOF\ncd \"$S/t84r4/probe_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -rf -s tests/unit/test_zz_t84_r4_probe.py 2>&1 | grep -v \"^$\" | tail -20",
 "description": "Reproduce open minors F3 and F4 on pinned HEAD copy"
}
````

### User / tool · 2026-11-02T04:59:32.702Z

**tool result**
````
>       with pytest.raises(RuntimeError):
E       Failed: DID NOT RAISE RuntimeError
tests/unit/test_zz_t84_r4_probe.py:29: Failed
__________________ test_zz_f4_promoted_charge_drop_is_silent ___________________
tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-3059/test_zz_f4_promoted_charge_dro0')
    def test_zz_f4_promoted_charge_drop_is_silent(tmp_path):
        """r3 F4 at HEAD: after a sentence change the promotion record is gone and nothing names the drop (expected: a dropped marker)."""
        conn, cid = seeded(tmp_path)
        a = aid(conn, cid, "$185", "r5")
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
        rerun(conn, cid, TEXT.replace("$185 was billed to the patient.", "$185 was billed to the patient per visit."))
        rc = DB.get_item(conn, a, cid)["ladder"].get("reclassification")
        print("\nF4 ladder.reclassification after sentence change =", rc)
>       assert rc is not None and rc.get("dropped") == "SENTENCE_CHANGED"
E       assert (None is not None)
tests/unit/test_zz_t84_r4_probe.py:42: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f3_audit_write_failure_leaves_item_changed
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f4_promoted_charge_drop_is_silent
2 failed, 5 passed in 0.74s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:42.621Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; F=\"$S/t84r4/probe_head/tests/unit/test_zz_t84_r4_probe.py\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport pathlib,sys\np=pathlib.Path(sys.argv[1]); s=p.read_text()\nold='''    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \\\"\\$185\\\", \\\"r5\\\")\n    def boom'''\nnew='''    conn, cid = seeded(tmp_path)\n    a = aid(conn, cid, \\\"\\$310\\\", \\\"r3\\\")\n    def boom'''\nassert s.count(old)==1, s.count(old)\np.write_text(s.replace(old,new))\nprint('patched')\n\" \"$F\" && cd \"$S/t84r4/probe_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -rf -s tests/unit/test_zz_t84_r4_probe.py -k \"zz\" 2>&1 | grep -v \"^$\" | tail -12",
 "description": "Fix F3 probe to use a demoted charge and rerun both minor probes"
}
````

### User / tool · 2026-11-02T04:59:43.690Z

**tool result**
````
patched
        a = aid(conn, cid, "$185", "r5")
        RC.reclassify(conn, cid, a, {"to": "charge"}, call=FakeCall(J2("agree")))
        rerun(conn, cid, TEXT.replace("$185 was billed to the patient.", "$185 was billed to the patient per visit."))
        rc = DB.get_item(conn, a, cid)["ladder"].get("reclassification")
        print("\nF4 ladder.reclassification after sentence change =", rc)
>       assert rc is not None and rc.get("dropped") == "SENTENCE_CHANGED"
E       assert (None is not None)
tests/unit/test_zz_t84_r4_probe.py:42: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f3_audit_write_failure_leaves_item_changed
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f4_promoted_charge_drop_is_silent
2 failed, 5 passed in 0.74s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:47.211Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t84r4/probe_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -s tests/unit/test_zz_t84_r4_probe.py -k \"f3\" 2>&1 | grep -v \"^$\" | head -30; PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -s tests/unit/test_zz_t84_r4_probe.py -k \"f4\" 2>&1 | grep \"F4 ladder\"; sed -n '97,108p' \"$S/head_9c1af01/app/backend/reclassify.py\"",
 "description": "Show F3 probe failure detail and F4 printed ladder value"
}
````

### User / tool · 2026-11-02T04:59:48.740Z

**tool result**
````
F
=================================== FAILURES ===================================
______________ test_zz_f3_audit_write_failure_leaves_item_changed ______________
tmp_path = PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-3061/test_zz_f3_audit_write_failure0')
monkeypatch = <_pytest.monkeypatch.MonkeyPatch object at 0x10be67fe0>
    def test_zz_f3_audit_write_failure_leaves_item_changed(tmp_path, monkeypatch):
        """r3 F3 at HEAD: the item update commits before the audit row; a failing audit write leaves the item changed (expected: unchanged)."""
        conn, cid = seeded(tmp_path)
        a = aid(conn, cid, "$310", "r3")
        def boom(*x, **k):
            raise RuntimeError("audit write failed")
        monkeypatch.setattr(RC, "_log", boom)
        with pytest.raises(RuntimeError):
            RC.reclassify(conn, cid, a, {"to": "not_a_charge"}, call=None)
>       assert DB.get_item(conn, a, cid)["kind"] == "charge"
E       AssertionError: assert 'unclear' == 'charge'
E         
E         - charge
E         + unclear
tests/unit/test_zz_t84_r4_probe.py:31: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f3_audit_write_failure_leaves_item_changed
1 failed, 6 deselected in 0.47s
F4 ladder.reclassification after sentence change = None
        print("\nF4 ladder.reclassification after sentence change =", rc)
def reclassify(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
    t = review._now(now)
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
````

### Assistant · claude-haiku-5-5 · 2026-11-02T04:59:58.473Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-084-r4; mkdir -p \"$E\" && cp \"$S/t84r4/mutate_t84_r4.py\" \"$S/t84r4/probe_gate_layers_t84_r4.py\" \"$S/t84r4/mutation-run-r4.txt\" \"$S/t84r4/gate-layers-run-r4.txt\" \"$E/\" && cp \"$S/t84r4/probe_head/tests/unit/test_zz_t84_r4_probe.py\" \"$E/probe_real_path_and_f3_f4_r4.py\" && cd \"$S/t84r4/probe_head\" && PYTHONDONTWRITEBYTECODE=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider -rf -s tests/unit/test_zz_t84_r4_probe.py 2>&1 | tee \"$E/probe-real-path-f3-f4-run-r4.txt\" | tail -8; ls -la \"$E\"",
 "description": "Copy review evidence into artifacts/review-evidence and rerun probes to save output"
}
````

### User / tool · 2026-11-02T04:59:59.821Z

**tool result**
````
>       assert rc is not None and rc.get("dropped") == "SENTENCE_CHANGED"
E       assert (None is not None)

tests/unit/test_zz_t84_r4_probe.py:42: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f3_audit_write_failure_leaves_item_changed
FAILED tests/unit/test_zz_t84_r4_probe.py::test_zz_f4_promoted_charge_drop_is_silent
2 failed, 5 passed in 0.97s
total 48
drwxr-xr-x@   8 arsis  staff    256 Nov  1 22:59 .
drwxr-xr-x@ 860 arsis  staff  27520 Nov  1 22:59 ..
-rw-r--r--@   1 arsis  staff   3321 Nov  1 22:59 gate-layers-run-r4.txt
-rw-r--r--@   1 arsis  staff   2467 Nov  1 22:59 mutate_t84_r4.py
-rw-r--r--@   1 arsis  staff   2153 Nov  1 22:59 mutation-run-r4.txt
-rw-r--r--@   1 arsis  staff   2508 Nov  1 22:59 probe-real-path-f3-f4-run-r4.txt
-rw-r--r--@   1 arsis  staff   1132 Nov  1 22:59 probe_gate_layers_t84_r4.py
-rw-r--r--@   1 arsis  staff   2397 Nov  1 22:59 probe_real_path_and_f3_f4_r4.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:51.427Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r4.md",
 "content": "# T-084 r4 review (staff-engineer-reviewer)\n\nCommit under review: 9c1af01 (board HEAD). The T-084 r3 code is not in 9c1af01. It is in 57a08ba, which 9c1af01 keeps; 9c1af01 restores the 12 T-085 files that 57a08ba had reverted by mistake. HEAD was pinned with `git archive 9c1af01` into the session scratchpad (reviewers cannot use worktree). Model: claude-haiku-5-5, as the environment reports. The persona header expects claude-sonnet-5-5; the record shows the model I actually ran as.\n\n## Summary\n\nBoth r3 majors are closed at HEAD. (F1) The class-only restore test exists (test_reclassify.py:274 and :285), and mutant T84-3 (the code-class clause removed from `_may_restore`) now fails 2 tests. (F2) The wording gate calls the shared `amounts.RATE_CUE` (reclassify.py:31, :77). The four named phrasings (\"unit price $X\", \"@ $X\", \"$X/visit\", \"rate of $X\") and the two brief strings are refused with 422 NO_CHARGE_WORDING before the judge is called.\n\nThree things are weaker than the card says. (a) For \"rate of $X\" and \"/visit\", the refusal depends on the classifier arm or on the other cue, and no test isolates either. Removing either arm passes all 148 tests. (b) The r3 minors F3 (item change and audit row are separate writes) and F4 (a promoted charge is dropped with no note) are still present, and I reproduced both. (c) The card's commit list names 9c1af01, which touches none of the three T-084 files; it omits 57a08ba, which carries the change.\n\nNo blocker. No major. Verdict: pass (per rule: no blocker, no major).\n\n## Exercised (what I actually ran or read)\n\n- `python3 tools/board.py show T-084`: status in_review, commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01], AC 1 evidence cites 9c1af01, Notes and handoff for r3.\n- `git log --oneline -5`; `git rev-parse HEAD` gives 9c1af01da6c7ec3dfc1f3f48faf035705bea8866.\n- `git archive 9c1af01 | tar -x` into the scratchpad (head_9c1af01). Every test below ran there, not in the dirty working tree.\n- `.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py` on the pinned archive: `148 passed in 1.75s`, exit 0.\n- `git archive 57a08ba` into the scratchpad, same two files with the same command: `148 passed in 1.69s`.\n- `git show --stat 9c1af01` (12 T-085 files, no T-084 file); `git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py` (empty output); `git diff --stat 1b1c711 9c1af01` (3 files, 82 insertions, 3 deletions); `git diff --stat 57a08ba 9c1af01` (12 files); `git show --stat 57a08ba` (15 files, including 12 T-085 deletions).\n- Read in full at the pinned HEAD: app/backend/reclassify.py lines 25-35, 66-96, 97-141, 148-200 (the gate, `_may_restore`, `_guard`, `carry_over`); app/backend/amounts.py lines 14-34 (the shared cue); tests/unit/test_reclassify.py lines 160-330.\n- `grep -rn \"RATE_CUE\\|has_rate_cue\" app/` at HEAD: reclassify.py:31 and :77; billing.py:190 and :256 use `A.has_rate_cue`.\n- Mutation driver `artifacts/review-evidence/T-084-r4/mutate_t84_r4.py`, run on copies of the pinned archive with `.venv/bin/python -I`; output in `artifacts/review-evidence/T-084-r4/mutation-run-r4.txt`:\n  - M0 control: 148 passed.\n  - T84-3 (reclassify.py:156 code-class clause removed): 2 failed (test_reclassify.py:274 and :285).\n  - T84-s (reclassify.py:156 sentence-sha clause replaced by True): 1 failed.\n  - G1 (reclassify.py:77 shared cue removed from the gate): 10 failed.\n  - G1b (reclassify.py:77 classifier arm `_classified_rate` removed): 148 passed. Survives.\n  - G2 (amounts.py:24 `@ $` cue removed): 1 failed (`Billed @ $90.`).\n  - G3 (amounts.py:23 `rate` word cue removed): 148 passed. Survives.\n  - G4 (amounts.py:22 `/visit` cue removed): 1 failed, and it is in test_billing.py only (`Charge /visit`). No reclassify test fails.\n  - G5 (amounts.py:24 `unit price` alternative removed): 148 passed. Survives; `unit` plus `price` is still matched by the daily/hourly alternative at amounts.py:23.\n- Gate-layer probe `artifacts/review-evidence/T-084-r4/probe_gate_layers_t84_r4.py` on HEAD, G3 and G5: output in `gate-layers-run-r4.txt`. On HEAD all four brief phrasings and the two extra ones are refused. In G3, \"Billed at a rate of $90.\" has cue False and is still refused, with classify = rate.\n- Real-path probe (a copy of HEAD with a scratch test file, saved as `artifacts/review-evidence/T-084-r4/probe_real_path_and_f3_f4_r4.py`): `5 passed` for the brief phrasings \"Billed unit price $90.\", \"Billed @ $90.\", \"Billed $90/visit.\", \"Billed $90 /visit.\", \"Billed at a rate of $90.\" The reclassify call with a judge FakeCall gives 422 NO_CHARGE_WORDING, `call.log == []`, and the item is not charge.\n- Reproduction of r3 F3 and F4 at HEAD (same probe file, output in `probe-real-path-f3-f4-run-r4.txt`): with `RC._log` raising, `reclassify` raises and the item is then `unclear`, not `charge` (`assert 'unclear' == 'charge'`); after a sentence change, `ladder.reclassification` is `None` (printed).\n\n## Findings\n\n### F1 (minor): the shared cue is not pinned for \"rate of $X\" or \"/visit\"; each refusal rests on the other arm\n\n- Evidence: `artifacts/review-evidence/T-084-r4/mutation-run-r4.txt`: `G3_no_rate_of_cue: rc=0 | 148 passed`; `G1b_gate_ignores_classifier_rate: rc=0 | 148 passed`; `G4_no_slash_visit_cue: 1 failed` in test_billing.py only. Gate probe: `Billed at a rate of $90.` cue False in the G3 copy, refused anyway (classify = rate). The refusal comes from reclassify.py:77 `_classified_rate`, which is the amounts.classify verdict.\n- Why it matters: the card says the gate uses the shared cue so these phrasings are refused before the judge. That holds at HEAD (the 5 real-path probes pass). But no test fails if the shared cue loses \"rate\" or \"/visit\", or if the classifier arm is removed. Each arm covers the other, so one regression in either can go unnoticed. The brief asked (r3 F2) for one rate-unit test that pins the shared cue. This is a test-strength gap, not a spec violation.\n- Fix: parametrize over \"Billed unit price $90.\", \"Billed @ $90.\", \"Billed $90/visit.\", \"Billed at a rate of $90.\" and assert `amounts.RATE_CUE.search(sentence)` is truthy (the cue alone). Also assert `charge_wording` is None with `RC._classified_rate` monkeypatched to return False, so the cue arm is the only decider.\n- Acceptance test: mutant G3 (the rate word removed from amounts.py:23) and mutant G1b (reclassify.py:77 `_classified_rate` removed) each fail at least one test in tests/unit/test_reclassify.py.\n\n### F2 (minor, carried from r3 F3): the item change and the audit row are separate writes; reproduced at HEAD\n\n- Evidence: reclassify.py:138 `DB.update_item(...)` (autocommit), :140 `review.batch_apply(...)`, :141 `_log(...)`. Probe in `probe-real-path-f3-f4-run-r4.txt`: with `RC._log` raising RuntimeError, `reclassify` raises as expected, and the item is then `unclear`; the test expected `charge` and got `'unclear' == 'charge'`.\n- Why it matters: a failed audit write now surfaces as an error (not silent), but the item has already changed and no audit row exists for it. Minor, as in r3, because the error is visible.\n- Fix: run update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as `apply_review` does (db.py:227, :287).\n- Acceptance test: the probe's `test_zz_f3_...` passes at HEAD (the item stays `charge` after the raised audit write).\n\n### F3 (minor, carried from r3 F4): a promoted charge is dropped with no note; reproduced at HEAD\n\n- Evidence: reclassify.py:191-192 (`if rc.get(\"to\") == \"charge\" and rc.get(\"excerpt_sha\") != _sha(...)`: `return it`). Probe output: `F4 ladder.reclassification after sentence change = None`. test_reclassify.py:316-325 asserts only `kind != \"charge\"`.\n- Why it matters: fail-closed is right (the figure leaves the total), but the paralegal gets no sign her promotion was withdrawn. Minor, as in r3.\n- Fix: keep the record with `dropped: \"SENTENCE_CHANGED\"` in `ladder.reclassification` and show it in the item view and stepper.\n- Acceptance test: after a sentence change, `ladder.reclassification.dropped == \"SENTENCE_CHANGED\"` (the probe's `test_zz_f4_...` passes then).\n\n### F4 (minor, new): the card's commit trail names 9c1af01, which carries none of the T-084 change\n\n- Evidence: `git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py` prints nothing. `git diff --stat 1b1c711 9c1af01` lists exactly those 3 files. `git show --stat 57a08ba` shows the same 3 files plus 12 T-085 deletions. `board.py show T-084` gives commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01] and the AC 1 evidence cites 9c1af01. 9c1af01's message says \"T-084 r3 change stays\", which describes the tree, not that commit.\n- Why it matters: the audit trail for the r3 fix points at a commit that does not contain it. Anyone who runs `git show 9c1af01` for the F1/F2 fix finds only T-085 files. The 57a08ba commit on its own passes the 148 tests (run above), so the code is fine; the record is wrong. Its T-085 deletions are undone by 9c1af01, but that is in the history.\n- Fix (orchestrator, card only): add 57a08ba to the card's commits and cite it in AC 1 evidence. Do not rewrite history.\n- Acceptance test: every commit in `git log --oneline -- app/backend/reclassify.py app/backend/amounts.py tests/unit/test_reclassify.py` since ec33bf0 appears in the card's commits list. (At HEAD that log shows 57a08ba, 8bc7f90 (T-083 r2) and c8a9874. 8bc7f90 belongs to another card, so it is not required on T-084.)\n\n## What is right\n\n- `_may_restore` (reclassify.py:148-156) has both clauses tested on their own. T84-3 (class clause removed) fails 2 tests; T84-s (sentence clause removed) fails 1.\n- The wording check runs before the judge (reclassify.py:166-168). The brief phrasings reach 422 NO_CHARGE_WORDING with the judge never called (5 real-path tests pass).\n- The gate and the classifier share one compiled cue (reclassify.py:31, amounts.py:27) and billing reaches the same core via `has_rate_cue` (billing.py:190, :256). The \"@ $\" cue is pinned by a test (G2 fails 1).\n\n```json\n{\"card\": \"T-084\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 9c1af01 (board HEAD, pinned with git archive into the scratchpad); T-084 r3 code is in 57a08ba (also archived and tested); files app/backend/reclassify.py, app/backend/amounts.py, tests/unit/test_reclassify.py, tests/unit/test_billing.py; no app URL; no sample CLI run (outside this card's files)\",\n \"exercised\": [\"python3 tools/board.py show T-084 (commits, AC 1 evidence, notes, handoff)\", \"git log --oneline -5; git rev-parse HEAD (9c1af01da6c7ec3dfc1f3f48faf035705bea8866)\", \"git archive 9c1af01 | tar -x into the scratchpad; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_reclassify.py tests/unit/test_billing.py: 148 passed\", \"git archive 57a08ba into the scratchpad; same command: 148 passed\", \"git show --stat 9c1af01; git show --stat --format= 9c1af01 -- amounts.py reclassify.py test_reclassify.py (empty); git diff --stat 1b1c711 9c1af01 (3 files); git diff --stat 57a08ba 9c1af01 (12 files); git show --stat 57a08ba\", \"read in full at 9c1af01: reclassify.py 25-35, 66-200; amounts.py 14-34; test_reclassify.py 160-330\", \"grep -rn RATE_CUE/has_rate_cue app/ at 9c1af01\", \"mutation driver artifacts/review-evidence/T-084-r4/mutate_t84_r4.py on pinned copies (mutation-run-r4.txt): M0 148 passed; T84-3 2 failed; T84-s 1 failed; G1 10 failed; G1b 148 passed; G2 1 failed; G3 148 passed; G4 1 failed (billing only); G5 148 passed\", \"gate-layer probe artifacts/review-evidence/T-084-r4/probe_gate_layers_t84_r4.py on HEAD, G3, G5 (gate-layers-run-r4.txt)\", \"real-path probe artifacts/review-evidence/T-084-r4/probe_real_path_and_f3_f4_r4.py on a HEAD copy: 5 brief phrasings 422 NO_CHARGE_WORDING, call.log empty (5 passed); F3 and F4 reproduced (probe-real-path-f3-f4-run-r4.txt)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"no_rate_into_total_without_both_checks\": 4, \"restore_rule_tested\": 5, \"code_check_strength\": 4, \"judge_gate\": 4, \"audit_trail\": 3, \"commit_integrity\": 3, \"billing_restored\": 5, \"tests_kill_mutants\": 4},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"The shared rate cue is not pinned for rate of and /visit; each refusal rests on the other arm, and no test fails if either arm is removed\",\n   \"evidence\": \"artifacts/review-evidence/T-084-r4/mutation-run-r4.txt: G3_no_rate_of_cue rc=0 148 passed (amounts.py:23 rate word removed); G1b_gate_ignores_classifier_rate rc=0 148 passed (reclassify.py:77 _classified_rate removed); G4_no_slash_visit_cue fails only tests/unit/test_billing.py (amounts.py:22 removed). gate-layers-run-r4.txt: Billed at a rate of $90. cue False in the G3 copy, still refused (classify rate)\",\n   \"why_it_matters\": \"The card says the gate uses the shared cue so these phrasings are refused before the judge. That holds at HEAD, but a regression in either arm for these phrasings passes all 148 tests. This is test strength, not a spec violation, so minor.\",\n   \"fix\": \"Parametrize over Billed unit price $90., Billed @ $90., Billed $90/visit., Billed at a rate of $90. and assert amounts.RATE_CUE.search is truthy for each; also assert charge_wording is None with RC._classified_rate monkeypatched to False so the cue arm alone decides.\",\n   \"acceptance_test\": \"Mutant G3 (rate word removed at amounts.py:23) and mutant G1b (reclassify.py:77 _classified_rate removed) each fail at least one test in tests/unit/test_reclassify.py.\"},\n  {\"severity\": \"minor\", \"title\": \"Item change and audit row are separate writes; a failed audit write leaves the item changed (carried from r3 F3, reproduced at HEAD)\",\n   \"evidence\": \"reclassify.py:138 DB.update_item (autocommit), :140 review.batch_apply, :141 _log. artifacts/review-evidence/T-084-r4/probe-real-path-f3-f4-run-r4.txt: with RC._log raising RuntimeError, the call raises and the item is then unclear (assert 'unclear' == 'charge')\",\n   \"why_it_matters\": \"The failure is visible (the error propagates), but the paralegal's item has changed and no audit row exists for it. Minor, as in r3.\",\n   \"fix\": \"Run update_item, batch_apply and _log in one BEGIN/COMMIT with rollback on error, as apply_review does (db.py:227, :287).\",\n   \"acceptance_test\": \"With RC._log raising, the item's kind is still charge after the call raises (the probe test test_zz_f3 passes).\"},\n  {\"severity\": \"minor\", \"title\": \"A promoted charge is dropped with no note when its sentence changes (carried from r3 F4, reproduced at HEAD)\",\n   \"evidence\": \"reclassify.py:191-192 (if rc.get to == charge and excerpt_sha differs: return it). Probe output: F4 ladder.reclassification after sentence change = None. test_reclassify.py:316-325 asserts only kind != charge\",\n   \"why_it_matters\": \"Fail-closed is the right direction (the figure leaves the total), but the paralegal gets no sign her promotion was withdrawn and the item view cannot say why. Minor, as in r3.\",\n   \"fix\": \"Keep the record with dropped SENTENCE_CHANGED in ladder.reclassification and show it in the item view and stepper.\",\n   \"acceptance_test\": \"After a sentence change, item.ladder.reclassification.dropped == SENTENCE_CHANGED (the probe test test_zz_f4 passes).\"},\n  {\"severity\": \"minor\", \"title\": \"The card's commit trail names 9c1af01, which contains none of the T-084 r3 change; 57a08ba, which does, is not listed\",\n   \"evidence\": \"git show --stat --format= 9c1af01 -- app/backend/amounts.py app/backend/reclassify.py tests/unit/test_reclassify.py prints nothing; git diff --stat 1b1c711 9c1af01 lists those 3 files; git show --stat 57a08ba lists them plus 12 T-085 deletions; board.py show T-084 commits [ec33bf0, c8a9874, e2b4e3f, 9c1af01]; AC 1 evidence cites 9c1af01\",\n   \"why_it_matters\": \"The audit trail for the r3 fix points at a commit that does not contain it. The code is fine: 57a08ba on its own archive passes 148 tests. The record is wrong.\",\n   \"fix\": \"Orchestrator: add 57a08ba to the card's commits and cite it in AC 1 evidence. Do not rewrite history.\",\n   \"acceptance_test\": \"Every commit in git log --oneline -- app/backend/reclassify.py app/backend/amounts.py tests/unit/test_reclassify.py since ec33bf0 is in the card's commits list.\"}\n ],\n \"whats_right\": [\n  \"_may_restore (reclassify.py:148-156): both clauses are now tested on their own; T84-3 fails 2 tests (test_reclassify.py:274, :285).\",\n  \"The wording check runs before the judge (reclassify.py:166-168); the brief phrasings reach 422 NO_CHARGE_WORDING with the judge never called (5 real-path tests pass).\",\n  \"The gate and the classifier share one compiled cue (reclassify.py:31, amounts.py:27), and the @ dollar cue is pinned by a test (mutant G2 fails 1).\"\n ],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T05:00:51.579Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r4.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:00:56.160Z

**tool call — Bash**
````
{
 "command": "/Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,re,sys\nt=open(sys.argv[1],encoding='utf-8').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json fences:', len(blocks), 'total fences:', t.count('\\`\\`\\`'))\nd=json.loads(blocks[0])\nsev=[f['severity'] for f in d['findings']]\nv='fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('card',d['card'],'persona',d['persona'],'model',d['model'],'verdict',d['verdict'],'rule_verdict',v,'findings',sev)\nprint('keys ok:', all(k in d for k in ['card','persona','model','scope','exercised','verdict','scores','findings','whats_right','questions_for_chris']))\nprint('whats_right n', len(d['whats_right']))\n\" reviews/T-084-staff-engineer-r4.md; ls -la artifacts/review-evidence/T-084-r4/",
 "description": "Parse the review JSON block and check the verdict rule"
}
````

### User / tool · 2026-11-02T05:00:56.217Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:00.133Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/t84r4/check_review_json.py\" <<'EOF'\nimport json, re, sys\nt = open(sys.argv[1], encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, t, re.S)\nprint(\"json fences:\", len(blocks), \"total fences:\", t.count(fence))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nrule = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"card\", d[\"card\"], \"persona\", d[\"persona\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"], \"rule_verdict\", rule, \"findings\", sev)\nprint(\"keys ok:\", all(k in d for k in [\"card\", \"persona\", \"model\", \"scope\", \"exercised\", \"verdict\", \"scores\", \"findings\", \"whats_right\", \"questions_for_chris\"]))\nprint(\"whats_right n:\", len(d[\"whats_right\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/t84r4/check_review_json.py\" /Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r4.md; ls -la /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-084-r4/",
 "description": "Parse the review JSON block and check the verdict rule"
}
````

### User / tool · 2026-11-02T05:01:00.252Z

**tool result**
````
json fences: 1 total fences: 2
card T-084 persona staff-engineer-reviewer model claude-haiku-5-5 verdict pass rule_verdict pass findings ['minor', 'minor', 'minor', 'minor']
keys ok: True
whats_right n: 3
total 48
drwxr-xr-x@   8 arsis  staff    256 Nov  1 22:59 .
drwxr-xr-x@ 860 arsis  staff  27520 Nov  1 22:59 ..
-rw-r--r--@   1 arsis  staff   3321 Nov  1 22:59 gate-layers-run-r4.txt
-rw-r--r--@   1 arsis  staff   2467 Nov  1 22:59 mutate_t84_r4.py
-rw-r--r--@   1 arsis  staff   2153 Nov  1 22:59 mutation-run-r4.txt
-rw-r--r--@   1 arsis  staff   2508 Nov  1 22:59 probe-real-path-f3-f4-run-r4.txt
-rw-r--r--@   1 arsis  staff   1132 Nov  1 22:59 probe_gate_layers_t84_r4.py
-rw-r--r--@   1 arsis  staff   2397 Nov  1 22:59 probe_real_path_and_f3_f4_r4.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:05.538Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md",
 "old_string": "Related: [[project_backend_llm_review_patterns]]",
 "new_string": "## r4 (9c1af01, pass; reviews/T-084-staff-engineer-r4.md)\n\n- **Both r3 majors closed.** Class-only restore has two tests (T84-3 killed by 2); the gate calls the shared RATE_CUE and refuses the brief phrasings before the judge (5 real-path probes pass).\n- **Redundant layers hide each other:** the gate has a cue arm and a classifier arm (`_classified_rate`). For \"rate of\" and \"/visit\" each arm covers the other, so removing either passes 148 tests. Mutate each arm alone, not only both.\n- **Carried minors reproduced again:** audit write failure leaves the item changed (`_log` raising, item stays changed); promoted charge dropped with `ladder.reclassification` None. Both still open at HEAD.\n- **The fix commit can hold none of the card's change:** 9c1af01 only restored T-085 files; the T-084 r3 code is in 57a08ba, which the card did not list. Check `git show --stat --format= <commit> -- <card files>` for each commit a card cites.\n- **Why:** a worker's \"restore\" commit reverted another card's files and then re-restored them; the card cites the restore, not the change.\n- **How to apply:** on any card that cites a fix commit, grep the commit's stat for the card's own files. Also run each card commit on its own `git archive` (57a08ba passed 148 on its own tree).\n- Harness: `rm -rf` on a scratch dir was denied for this reviewer; use fresh dir names. A Bash command with escaped backticks (for a regex on a file) tripped the git-guard parser (\"could not parse command safely\"); put such scripts in a file and run it.\n\nRelated: [[project_backend_llm_review_patterns]]"
}
````

### User / tool · 2026-11-02T05:01:05.633Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t073_t084_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:07.521Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass, rate phrase; r2 c8a9874 fails its own tree (closed 6feb2ff), class-only restore untested, gate vs classifier gap",
 "new_string": "- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change"
}
````

### User / tool · 2026-11-02T05:01:07.628Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:01:09.453Z

Verdict pass (0 blockers, 0 majors, 4 minors) on 9c1af01: both r3 majors are closed, T84-3 fails 2 tests, the gate refuses the four phrasings before the judge, and the review is at /Users/arsis/zlayt-pm-project/reviews/T-084-staff-engineer-r4.md.
