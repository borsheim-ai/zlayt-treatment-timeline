# Subagent: T-141 r3 final check (T-141 r3 final check)

Source: `agent-acf77b6cafa1a83f6.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T14:19:41.003Z

This is the final round-3 review of board card T-141 (commit ad8b7d1) in /Users/arsis/zlayt-pm-project. Read reviews/T-141-staff-engineer-r2.md and `python3 tools/board.py show T-141`, including the orchestrator's round-3 note and the handoff.

The worker deviated from the note: negated or plainly historical accident wording stays info-only, so as not to re-open lib11. Judge whether that deviation hides any true date conflict.

On a `git archive HEAD` copy:
- Re-run your 30 variants plus at least 10 fresh ones, including negations ('no prior accidents', 'denies MVC') and historical ones ('MVA in 2015').
- Check that notes are computed at read time and refresh after confirm_date.
- Check that a case with no stored summary reports its checks as not run.
- Check that the named mutants are killed.
- Run the conflict suites.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-141-staff-engineer-r3.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:43.276Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T14:19:43.284Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:43.598Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-02T14:19:43.609Z

**tool result**
````
1	# T-141 staff-engineer review, round 2 (68b8685), Marcus Lee persona
2	
3	Verdict: **changes** (0 blockers, 2 major, 4 minor). Everything I asked for in round 1 moved: my six accident-date variants (B, C, D, F, G and the plain E) all conflict now, lib11 still gives exactly two denial conflicts and no date conflict, and `checks` is computed per case from a stored run summary with real skipped[] reasons. Two things are still wrong: the "describes a collision" word test still loses true conflicts on ordinary wordings, and the stored summary goes stale after `confirm_date` and then contradicts a live flag.
4	
5	## Answers to the brief
6	1. **Accident-date variants.** Round-1 set (probe2.py, A-L) on the r2 archive: B, C, D, E, F, G and H conflict, A, J, K, L are quiet, I (two stated dates) conflicts. Fresh variants: 30 (`r2_variants.py` V1-V20, `r2_variants2.py` W1-W10), including a billing statement and an intake form dated before the accident. Right: V1 billing that names the collision conflicts, V2 billing without mechanism is info-only, V3 intake naming "rear-ended" conflicts, V5 "slipped and fell" conflicts, V10 and V14-V15 history/"fall risk" are info-only, V16-V17 and V19 conflict, V20 is quiet. V4 (an intake dated before the accident it states) conflicts because its own "Date of accident:" phrase matches the event list; I think that is the right result, not a defect. Wrong: 8 pre-accident records that name the collision are info-only (finding 1), and 6 benign ones conflict (finding 3).
7	2. **checks.** Matrix over the real pipeline and the case view (`r2_checks_matrix.py`): ingested only gives accident_date + provider_name with NOT_RUN for the two pair rules; finished English gives all four, skipped []; deadline before the conflict stage gives STAGE_SKIPPED; deadline after it gives all four; a real crash in the conflict stage of a re-run gives RUN_FAILED (`r2_real_crash.py`, not the faked state the unit test uses); lib09 gives LANGUAGE_PARTIAL on records [2, 4, 7] for three types; an all-Spanish packet gives LANGUAGE for three types and `conflict_types == ['provider_name']`. Never claims a rule ran when it did not, on any of those. The two exceptions are finding 2 (stale after confirm_date) and finding 5 (rows with no summary).
8	3. **lib11.** Still correct. `evals.library_report` on the archive: lib11 must flags 4/4, must_not hits 0. Case view after a fixture run: two denial conflicts, accident-date flags [], note "1 record predates the stated accident date, March 18, 2026. None describes a collision..." (true, and the PCP's "car accidents in 2019 and 2022" is read as history). Candidates and accident-date output over all 27 golden and library packets are identical between c4bb4da and 68b8685; versus the pre-T-141 build only lib11 changes; the sample still raises accident_date_after_treatment (2026-01-19).
9	4. **Changed test (test_t116_r4_all_dated_records.py).** Right call. The old expectation (a statement dated before the stated accident is a conflict naming the statement) is exactly what the Round 2 direction removes, the new expectation is `== []` plus a note with record_nos [1], and the docstring says why. The twin test keeps the D-055 invariant (paperwork is never named as the first treatment) and N17 (paperwork branch off) is killed by three tests, so the invariant is still pinned. One caveat, not a defect: in the twin the "collision" that makes it a conflict is the stating visit's own phrase "Date of accident: 2026-01-15", so the twin proves the self-contradiction path, not a described collision.
10	5. **Tests.** Six conflict modules on the r2 archive: 203 passed. Full `tests/unit` on the 68b8685 archive: 1 failed, 3799 passed, 8 skipped (the failure is finding 6; the 12 working-tree T-139 failures are other work, noted only). 30 mutants (`r2_mutate.py`): 22 killed, 8 survived. Survivors and what they mean are in finding 4.
11	
12	```json
13	{
14	 "card": "T-141",
15	 "persona": "staff-engineer-reviewer",
16	 "model": "claude-sonnet-5-5",
17	 "scope": "git 68b8685 (T-141 round 2), compared with c4bb4da and 68b8685~1; all probes on git archives in the scratchpad (T141r2_head, T141r2_mut2, T141r2_parent, T141_head, T141_pre), never the dirty working tree; fixture backend, ZLAYT_MODE=local; sample and lib09/lib11 packets; no server started",
18	 "exercised": [
19	  "Read personas/staff-engineer.md, reviews/T-141-staff-engineer.md (round 1), `python3 tools/board.py show T-141` (direction note, handoff), `git show 68b8685` in full (conflicts.py, conflict_candidates.py, pipeline.py, present.py, api.md, tests), `git rev-parse HEAD` = 68b868575403c86cdac00d4fdc641ecd2494c613",
20	  "git archive 68b8685 into T141r2_head, T141r2_mut2 (mutants), 68b8685~1 into T141r2_parent; reused the round-1 archives T141_head (c4bb4da) and T141_pre for differentials",
21	  "Round-1 variants: artifacts/review-evidence/T-141/probe2.py on the r2 archive (A-L)",
22	  "30 fresh accident-date variants: r2_variants.py (V1-V20) and r2_variants2.py (W1-W10), incl. billing statement and intake dated before the accident; r2_variants2.py also run on c4bb4da to see which wrongs are inherited",
23	  "checks matrix through the real pipeline and present.case_view: r2_checks_matrix.py (ingested, complete, deadline at extract/verify/amounts/conflicts/flags, re-run in flight, legacy rows without run_checks, lib09 partial Spanish, lib11, all-Spanish synthetic, checks() defaults); r2_real_crash.py (crash in the conflict stage of a re-run, also with the P2 mutant); r2_stale_checks.py (ingest, then review.confirm_date)",
24	  "27-packet differential (diff_packets.py) c4bb4da vs 68b8685 (identical) and pre vs 68b8685 (only lib11), sample accident-date conflict still present",
25	  "evals.library_report on the r2 archive: lib11 4/4 must flags, 0 must_not hits; lib11 case view after a fixture run (r2_lib11.py)",
26	  "pytest: conflict modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t116_r4_all_dated_records, test_api_routes) 203 passed; full tests/unit on 68b8685 archive 1 failed (test_export_equals_golden_when_everything_accepted), 3799 passed, 8 skipped; same test passes on the 68b8685~1 archive (34 passed in test_api_routes)",
27	  "30 mutants (r2_mutate.py) on T141r2_mut2: 22 killed, 8 survived; the file was restored and diffed against T141r2_head after the manual mutants",
28	  "Read app/frontend/flags.js coverage() (what the UI does with checks), memory/contracts/api.md checks section, board list for the owner of rendering skipped[] and notes[] (T-151, ready)"
29	 ],
30	 "verdict": "changes",
31	 "scores": {
32	  "determinism": 5,
33	  "honest_failure": 3,
34	  "tests_assert_behaviour": 4,
35	  "llm_code_boundary": 5,
36	  "controls_discipline": 4
37	 },
38	 "findings": [
39	  {
40	   "severity": "major",
41	   "title": "The 'describes a collision' test still loses true accident-date conflicts: 8 of 30 fresh variants where an earlier record names the collision come back info-only, and the note then says 'None describes a collision'",
42	   "evidence": "app/backend/conflicts.py:14-18 (_EVENT, _HISTORICAL), :21-31 (_historical: a history word anywhere in the clause, or any bare year before the stated year, makes the clause history), :57-59 (_event_records). Repro on a git archive of 68b8685: `.venv/bin/python -I artifacts/review-evidence/T-141/r2_variants.py <archive>` and `r2_variants2.py <archive>`; each case is a record dated 2026-01-05, a PT visit 2026-01-12, intake 'Date of accident per intake form: 2026-01-09'. Info-only, should conflict: V6 'Slip and fall at the grocery store, wrist pain.' (no 'fell'); V7 'Pedestrian vs auto. Neck pain 7/10.'; V8 'Neck pain since the incident. Whiplash pattern.'; V11 ER 2025-12-30 'Rear-ended in December 2025. Neck pain.' (bare 2025 < 2026 makes it history; stated 2026-01-05); V18 'MVC with no history of LOC.' (same clause, so 'history' wins; round 1's variant D only passes because it had a comma); W3 'Healthy prior to the rear-end collision. Neck pain since.'; W4 'Previously asymptomatic until the motor vehicle collision.'; W5 same as V18. 'prior to' and 'previously ... until' are temporal words about the collision, and ER, PT and chiro narratives use them all the time. Passing and correct: V1, V3, V5, V16, V17, V19, W9. Note text app/backend/conflicts.py:~150: 'None describes a collision, so no date conflict is raised' is false for the 8; the UI does not show notes yet (T-151, ready), so today the loss is invisible.",
43	   "why_it_matters": "Same failure family as round-1 major 1, moved from sentence to clause: a deterministic R-FL-2 check becomes a word-list guess and a true discrepancy between the stated accident date and an earlier record disappears, now with a sentence that asserts there is nothing to find. Round 2 fixed the six wordings I tried and left the class open. This is a spec violation of the Round 2 direction ('one that DOES describe the collision ... is a date conflict'), not a preference. Not a blocker because it needs a stated date later than the earliest record plus one of these wordings, and the loss is limited to the date-conflict flag, not an entry or a total.",
44	   "fix": "(a) 'prior' / 'previously' / 'history' make a clause history only when they modify the event noun ('prior accident', 'history of MVA', 'previous collision'); 'prior to', 'previously ... until' and 'no history of <other noun>' in the same clause do not. (b) A bare year equal to the year of the record's own date, or the year before it when the record date is within 60 days of January, is not history. (c) Add incident, pedestrian, auto, slip and fall, whiplash, impact. (d) Soften the note: do not assert 'none describes a collision'; say what the code looked for ('no record names a collision, crash, MVA, fall or similar') so the paralegal can read the records.",
45	   "acceptance_test": "tests/unit/test_conflicts.py: V6, V7, V8, V11, V18, W3, W4, W5 each return one accident_date_after_treatment conflict; the lib11 shape (annual visit listing 2019 and 2022 accidents, EMS 'struck from behind') and the V10/V14/V15 history wordings still return []."
46	  },
47	  {
48	   "severity": "major",
49	   "title": "`checks.notes` and the language/dated-record facts are a snapshot taken at run time; `confirm_date` recomputes the accident-date conflict live, so the case then shows a conflict flag and a note saying no conflict is raised",
50	   "evidence": "app/backend/pipeline.py:160-165 (_store_run_checks writes run_summary into case config at ingest, run start and finalize only), app/backend/review.py:499-533 (_recompute_gaps recomputes accident_date_conflicts after confirm_date and never touches run_checks), app/backend/present.py:317 (checks built from the stored summary). Repro: `.venv/bin/python -I artifacts/review-evidence/T-141/r2_stale_checks.py <68b8685 archive>`: records 2026-03-04 annual visit, 03/06/2026 (ambiguous) ER 'rear-end collision', intake 2026-03-27 'Date of accident per intake form: 2026-03-18'. Output: `ingested | notes: ['1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; ...'] | accident-date flags: []`, then after `review.confirm_date(.., '2026-03-06')`: `notes: [same text] | accident-date flags: ['accident_date_after_treatment']`. The same snapshot holds dated_records, so a case whose dates were all ambiguous at run time keeps NO_DATED_RECORD and drops accident_date from conflict_types after the user confirms them.",
51	   "why_it_matters": "The field exists so the UI can say honestly what was checked on this case. After any date confirmation it can contradict a flag on the same screen ('no date conflict is raised' beside 'records disagree'), and under-reports what ran. The first reader of this is the paralegal in T-151. The part of the summary that comes from the records (note, dated count) is a pure function of the records and should not be stored.",
52	   "fix": "Compute notes and the NO_DATED_RECORD condition at GET time from the current records (accident_date_note and the dated count are cheap and deterministic); store only what cannot be recomputed (conflicts_stage, per-record language). Or refresh run_checks at the end of _recompute_gaps.",
53	   "acceptance_test": "tests/unit/test_t141_checks_per_case.py: the r2_stale_checks scenario (ambiguous collision record, confirm_date) ends with an accident_date flag and notes == []; a case whose only dated record was ambiguous at run time lists accident_date in conflict_types after confirm_date."
54	  },
55	  {
56	   "severity": "minor",
57	   "title": "Benign wording in an earlier record still produces a 'records disagree' accident-date conflict: negated mechanism words, 'last year', and 'vehicle' / 'hit' in other senses",
58	   "evidence": "Same scripts, 68b8685 archive. Conflict, should be info-only: W1 'Annual physical. Denies any accidents or falls.'; W2 'No recent accidents or injuries.'; V9 'Reports a car accident last year, fully recovered.'; V12 'Vehicle registration renewed.'; V13 'Patient hit her weight goal of 150 lb.'; W8 'Auto insurance card on file; vehicle: 2019 Honda Civic.' conflicts.py:14-15 (_EVENT includes bare 'hit', 'vehicle', 'accident\\w*'; no negation or 'last year' handling). Inherited, not new: r2_variants2.py on the c4bb4da archive and the V9/V12/V13 rows on c4bb4da also conflict (round 1 only skipped when another record was dated that day). Labelled 'I would tighten it': the paralegal sees and can dismiss a code conflict, nothing is lost.",
59	   "why_it_matters": "The card's own target was a false accident-date conflict from an annual visit. 'Denies any accidents' is the commonest pre-accident PCP line there is, so the false conflict class that GATE-M2 reported on lib11 is narrower but not closed.",
60	   "fix": "Skip a clause when a negator ('no', 'denies', 'without', 'negative for') precedes the event word within the clause; drop bare 'hit' and 'vehicle' in favour of 'hit by', 'struck', 'vehicle (accident|collision|crash)'; add 'last year' and 'N months ago' to _HISTORICAL.",
61	   "acceptance_test": "tests/unit/test_conflicts.py: W1, W2, V9, V12, V13, W8 each return [] and a note; V1, V3, V5, W9 still conflict."
62	  },
63	  {
64	   "severity": "minor",
65	   "title": "Eight mutants survive: the old-full-date history branch, run-start 'pending', the 'uncertain' language rule and four word-list members are not pinned",
66	   "evidence": "`r2_mutate.py` (30 mutants over conflicts.py, conflict_candidates.py, pipeline.py, present.py; run against test_conflicts, test_conflict_candidates, test_t141_checks_per_case, test_t116_r4, test_api_routes, test_t093): SURVIVED N6 and N18 (full date more than a year before the stated date no longer history: conflicts.py `> 365` and the `d[\"iso\"] < iso` test; nothing uses 'Rear-end collision 03/14/2024, resolved.'); P2 (pipeline.py:349 `_store_run_checks(.., \"pending\")` at run start removed: `r2_real_crash.py` shows a crashed re-run of a finished case then reports all four types as ran, and test_a_run_that_died_before_the_conflict_stage fakes the stored state instead of producing it); P3 (ingest-time summary removed, equivalent for English); C7 ('uncertain' language counted as read); N1, N2, N3, N4 (t-bone/sideswipe/run over, airbag/seatbelt, 'hit', 'vehicle' removed one at a time; dropping 'hit' and 'vehicle' together is killed). N14 is equivalent. Killed: N5, N7-N13, N15-N17, C1-C6, C8, P1, R1 (22 of 30). Real behaviour of P2 is correct at HEAD (`after crashed re-run: RUN_FAILED` for both pair rules).",
67	   "why_it_matters": "P2 is the line that keeps a crashed re-run from claiming the previous run's result; its only test builds the failed state by hand. N6/N18 is a documented rule ('full date over a year before') with no test.",
68	   "fix": "Add a unit test that crashes the conflict stage of a re-run (monkeypatch FL.run_conflict_pass to raise) and asserts RUN_FAILED; a test for 'Rear-end collision 03/14/2024, resolved.' being info-only; one test per word-list member or a table test over _EVENT.",
69	   "acceptance_test": "Re-run r2_mutate.py: P2, N6, N18, N1-N4 and C7 are killed."
70	  },
71	  {
72	   "severity": "minor",
73	   "title": "A case with no stored run summary (created before this commit) claims every check ran, and a failed one with none sends an empty list to the UI fallback",
74	   "evidence": "r2_checks_matrix.py S5: `legacy ready, no run_checks | ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[]` (conflict_candidates.py checks(): `known = run is not None`, stage None and state complete is treated as ran); S5b: `legacy failed, no run_checks | ran=[] skipped=[all four RUN_FAILED]`. app/frontend/flags.js:89 treats `conflict_types.length == 0` as 'server sent no list' and prints FALLBACK_CHECKED under 'Checked:' (three kinds), which is the overclaim this field exists to prevent.",
75	   "why_it_matters": "Any database that already holds cases (the dev DB at port 7860) shows full coverage for a Spanish case created before the commit. New cases always get a summary at ingest, so this is a migration edge, not a live path.",
76	   "fix": "When no summary is stored, say so: return conflict_types [] and one skipped entry per type with reason_code UNKNOWN ('this case was analysed before per-case checks were recorded'); the frontend should render an empty list as 'none checked', not as the fallback.",
77	   "acceptance_test": "tests/unit/test_t141_checks_per_case.py: a finished case whose config lacks run_checks lists no type under conflict_types and every type under skipped with UNKNOWN."
78	  },
79	  {
80	   "severity": "minor",
81	   "title": "Commit 68b8685 carries a T-139 test hunk without its code and is red at the commit: test_export_equals_golden_when_everything_accepted passes at the parent and fails at 68b8685",
82	   "evidence": "`git archive 68b8685~1` then `pytest tests/unit/test_api_routes.py -q` -> `34 passed`; `git archive 68b8685` then `pytest tests/unit -q` -> `1 failed, 3799 passed, 8 skipped in 211.01s`, `FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted`, `assert held == []` / `AssertionError: assert ['e2', 'e4'] == []` (tests/unit/test_api_routes.py:170). `git show 68b8685 -- tests/unit/test_api_routes.py` shows the hunk `assert held == [\"e2\", \"e4\"]` -> `assert held == []  # T-139 narrowing`; the narrowing code is still uncommitted in the working tree (`git status --short`: M app/backend/amounts.py, flags.py, pipeline.py, present.py, review.py). Same shared-index pattern as round-1 minor 5.",
83	   "why_it_matters": "A commit on main that breaks the committed suite makes bisect and any reviewer pinned to HEAD see a red test that is not T-141's. Noted per the brief; it is distinct from the 12 working-tree failures because it is inside this commit's own diff.",
84	   "fix": "No change to T-141 code. Land the T-139 narrowing code (or revert that one test hunk) so HEAD is green; stage by pathspec per the file-ownership rule.",
85	   "acceptance_test": "`pytest tests/unit/test_api_routes.py -q` passes on a git archive of the commit that follows."
86	  }
87	 ],
88	 "whats_right": [
89	  "The Round 2 shape is right: the content decides, the skip rule is gone, and all six round-1 variants (B, C, D, E, F, G) conflict while the lib11 shape stays quiet; lib11 library report is 4/4 with 0 must_not hits and the other 26 packets are unchanged.",
90	  "checks is computed from the run, not a constant: ingested, deadline-skipped, crashed re-run, partial Spanish and all-Spanish each give a different, correct skipped[] with a reason code, and conflict_types lists only what ran; api.md documents the shape and the T-142 fields are kept.",
91	  "The changed T-116 test was changed for the right reason, with a reason in the docstring, a twin test that keeps the paperwork invariant, and the paperwork branch still killed by three tests."
92	 ],
93	 "questions_for_chris": []
94	}
95	```
96	
97	Erratum: mutant counts. The summary and the JSON say 22 killed and 8 survived (and finding 4 is titled "Eight mutants survive"); the run (r2_mutate.py output) is 20 killed and 10 survived: N1, N2, N3, N4, N6, N14, N18, C7, P2, P3 (N14 and P3 equivalent). The finding text lists all ten by id, so the finding stands as written; the JSON block is otherwise authoritative.
98	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:44.042Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r2_patterns.md"
}
````

### User / tool · 2026-11-02T14:19:44.051Z

**tool result**
````
1	---
2	name: project_t141_r2_patterns
3	description: T-141 r2 68b8685 changes — clause-level word list still loses true accident-date conflicts, stored run summary goes stale after confirm_date, test hunk from another card makes commit red
4	metadata:
5	  type: project
6	---
7	
8	T-141 r2 (68b8685, verdict changes, 2 major 4 minor).
9	
10	- Fix for a lost-conflict class moved the boundary from sentence to clause but left the class: "prior to / previously until / no history of LOC" in the same clause as the collision word still makes it history; unlisted mechanism words (slip and fall, pedestrian vs auto, the incident) and month-year in prior year are info-only. Always run 20+ fresh wordings, not only the prior round's list.
11	- A snapshot stored at run time (case config run_checks: notes, dated_records) is not refreshed by review.confirm_date -> _recompute_gaps, so a live flag and a stored note contradict. Grep every writer of the thing the snapshot summarises.
12	- Lexicon event_on_date ("MVA on 03/14/2024") makes an OLD accident a stated accident date, so accident_dates_differ fires; inherited, not r2.
13	- Commit swept another card's test hunk (held == []) without its code: red at the commit, green at the parent. Check the failing test with git archive of commit and parent.
14	- Method that worked: real-pipeline crash probe (monkeypatch FL.run_conflict_pass) to show a faked-state unit test hides the P2 line; mutate script with 30 mutants over a git archive copy.
15	- reviews/*.md is write-once even for Edit; fix counts by appending an Erratum with printf >>.
16	
17	**How to apply:** for word-list rules ask what the clause-level negation/temporal words do; for stored summaries ask what refreshes them.
18	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:44.719Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-141 | tail -80; git log --oneline | head -5"
}
````

### User / tool · 2026-11-02T14:19:44.864Z

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
updated_at: "2026-11-02T14:19:36Z"
claimed_by: "backend"
claimed_at: "2026-11-02T14:04:09Z"
rounds: 2
commits: ["c4bb4da", "68b8685", "ad8b7d1"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer.md", "at": "2026-11-02T13:31:22Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer-r2.md", "at": "2026-11-02T14:04:00Z"}
ac:
  - {"n": 1, "text": "lib11 raises the denial-vs-history conflict (intake form as the denial side, D-053/T-113 rules) and no false accident-date conflict; unit + library expected update with a written reason; controls unaffected", "done": true, "evidence": "r3: tests/unit/test_t141_r3_variants.py (30 reviewer variants + round-1 A-L + word-list table), test_t141_checks_per_case.py (read-time notes, no summary, crashed re-run) pass; conflict suites 288 pass; 27-packet diff vs HEAD identical (sample conflict kept); lib11 no date conflict, note present"}
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

## Handoff
Round 3 (ad8b7d1). What changed: pre-accident record is info-only only if every injury/mechanism/accident clause is negated (5 words before) or plainly history (history word within 3 words before the word, not 'prior to'; last year/years ago/as a child; full date >1y before stated; month+year >2 months before the record; bare year before the record's year, last-year only outside Jan/Feb); word list widened (incident, pedestrian, whiplash, injur*, LOC, trauma, impact, slip and fall, 'hit by'/'vehicle hit'/'hit them', no bare hit/vehicle). Notes and the dated-record count are computed in GET case from load_records (run_summary no longer stores them); no stored run summary -> all four types skipped NOT_RUN, conflict_types []. api.md updated. How verified: reviewer's 30 variants + A-L + a table over each word-list member as tests; stale-note scenario (confirm_date) and crashed re-run tests; mutants: reviewer's survivors (old-full-date, run-start pending, uncertain, word members) all killed, plus 3 extra I added killed; 27-packet diff identical to HEAD; conflict suites 288 pass; full unit 2 failures, both others' (T-139 CHARGE_TEXT_IN_ENTRY why template, frontend data-entry-id e2e contract). Left: frontend should render an empty conflict_types as 'none checked'. Surprised: orchestrator's literal 'any accident vocabulary = conflict' would re-open lib11 (PCP lists 2019/2022 accidents), so history/negated clauses stay info per the reviewer's acceptance tests; also the 2 live-DB legacy cases now show not run.

ad8b7d1 fix(backend): T-141 r3 pre-accident records are info-only only without injury/mechanism vocabulary; checks notes computed at read time; no stored summary = not run
2a6f40b docs(orchestrator): D-060 charge candidates are default-deny (amends D-059)
078c5ae fix(frontend): T-136 r3 the open quote-pick card no longer says the export stays blocked while the gate passes: conditional fallback, server human why shown as given (no regex swap)
a0e2639 feat(backend): D-059 charge rules, named confirms, no batch accept, expected totals (T-140 r2)
f5ad979 feat(frontend): T-136 r3 case-level steps and the AI-check panel read second_check_pending; a held re-picked quote offers Write the summary and a rerun only until one gave no answer (rerun_no_answer), never 'dismiss it'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:47.655Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD; git status --short | head; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $SP | head -50; ls artifacts/review-evidence/T-141/; git show --stat ad8b7d1 | head -30"
}
````

### User / tool · 2026-11-02T14:19:48.010Z

**tool result**
````
ad8b7d1fea26299284de15dbe481b5ea20a297e8
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
641ed.bak
CLAUDE.md
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
T102_staff_r1
T102_staff_r2
T103_archive
T103_parent
T106_cli_out
T106_head_archive
case.json
diff_packets.py
lib11-body.txt
lib11-conflicts.png
lib11-full.png
live_j3.py
mutate.py
probe1.py
probe2.py
probe3.py
r2_checks_matrix.py
r2_lib11.py
r2_mutate.py
r2_real_crash.py
r2_stale_checks.py
r2_variants.py
r2_variants2.py
ui_conflict_shot.py
ui_lib11.py
commit ad8b7d1fea26299284de15dbe481b5ea20a297e8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:19:14 2026 -0600

    fix(backend): T-141 r3 pre-accident records are info-only only without injury/mechanism vocabulary; checks notes computed at read time; no stored summary = not run
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/conflict_candidates.py      |  46 +++++++------
 app/backend/conflicts.py                |  79 +++++++++++++++-------
 app/backend/present.py                  |   2 +-
 memory/contracts/api.md                 |   2 +-
 tests/unit/test_conflict_candidates.py  |  28 +++++---
 tests/unit/test_conflicts.py            |   4 +-
 tests/unit/test_t141_checks_per_case.py |  96 ++++++++++++++++++++++++++
 tests/unit/test_t141_r3_variants.py     | 115 ++++++++++++++++++++++++++++++++
 8 files changed, 314 insertions(+), 58 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:19:51.613Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/T141r3_head $SP/T141r3_mut && git archive HEAD | tar -x -C $SP/T141r3_head && git archive HEAD | tar -x -C $SP/T141r3_mut && ls $SP/T141r3_head | head -30; git show ad8b7d1 -- app/backend/conflicts.py app/backend/conflict_candidates.py app/backend/present.py"
}
````

### User / tool · 2026-11-02T14:19:52.909Z

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
commit ad8b7d1fea26299284de15dbe481b5ea20a297e8
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 08:19:14 2026 -0600

    fix(backend): T-141 r3 pre-accident records are info-only only without injury/mechanism vocabulary; checks notes computed at read time; no stored summary = not run
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/conflict_candidates.py b/app/backend/conflict_candidates.py
index 1fff031..55c3db6 100644
--- a/app/backend/conflict_candidates.py
+++ b/app/backend/conflict_candidates.py
@@ -247,45 +247,46 @@ _LANG_WORD = {"es": "Spanish", "uncertain": "an unidentified language", "other":
 
 
 def run_summary(records: list, *, stage: str) -> dict:
-    """What THIS case's check stage did, for GET case `checks` (stored in the case config by the pipeline). stage: 'pending' (ingested or running),
-    'ran', or 'skipped' (the run deadline passed before the conflict stage). {conflicts_stage, read_records, unread: {lang: [record nos]},
-    dated_records, notes}. `read_records` counts records the English rules can read; Spanish, uncertain and unsupported-language records are listed in `unread`."""
-    from app.backend import conflicts
+    """What THIS case's check stage did, for GET case `checks` (stored in the case config by the pipeline): only what cannot be recomputed from the stored
+    records. stage: 'pending' (ingested or running), 'ran', or 'skipped' (the run deadline passed before the conflict stage). {conflicts_stage,
+    read_records, unread: {lang: [record nos]}}. `read_records` counts records the English rules can read; Spanish, uncertain and unsupported-language
+    records are listed in `unread`. The dated-record count and the notes are NOT stored: `checks` computes them from the current dates (T-141 r3)."""
     unread = {}
     for r in records:
         lang = r.get("lang") or "en"
         if lang != "en":
             unread.setdefault(lang, []).append(r["n"])
-    note = conflicts.accident_date_note(records)
     return {"conflicts_stage": stage, "read_records": sum(1 for r in records if (r.get("lang") or "en") == "en"),
-            "unread": {k: sorted(v) for k, v in sorted(unread.items())}, "dated_records": sum(1 for r in records if r.get("date_iso")),
-            "notes": [note] if note else []}
-
-
-def checks(run: dict = None, state: str = "complete") -> dict:
-    """GET case `checks`, computed from what this case actually ran (T-141 r2). `run` is run_summary() as stored; `state` is 'complete', 'not_run'
-    (created, not analysed) or 'failed'. {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}],
-    not_checked: [{type, label}], notes: [..]}. A type is in `skipped` without `record_nos` when it did not run at all (and is then absent from
-    conflict_types), and with `record_nos` when it ran but could not read those records (Spanish and the like)."""
-    known = run is not None
-    run = run or {}
-    stage = run.get("conflicts_stage")
+            "unread": {k: sorted(v) for k, v in sorted(unread.items())}}
+
+
+def checks(run: dict = None, state: str = "complete", records: list = None) -> dict:
+    """GET case `checks`, computed from what this case actually ran (T-141 r2/r3). `run` is run_summary() as stored; `state` is 'complete', 'not_run'
+    (created, not analysed) or 'failed'; `records` are the case's records as they are NOW (store.load_records): the dated-record count and `notes` come from
+    them, so confirming a date refreshes both. A case with no stored summary reports every check as not run (NOT_RUN): nothing is claimed about it.
+    {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}],
+    notes: [..]}. A type is in `skipped` without `record_nos` when it did not run at all (and is then absent from conflict_types), and with `record_nos`
+    when it ran but could not read those records (Spanish and the like)."""
+    from app.backend import conflicts
+    run = run or None
+    stage = (run or {}).get("conflicts_stage")
+    dated = sum(1 for r in records if r.get("date_iso")) if records is not None else None
     skipped = []
 
     def skip(t, code, reason, nos=None):
         skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})
 
     for t in CONFLICT_LABELS:
-        if state == "failed" and not known:
-            skip(t, "RUN_FAILED", "The run stopped before this check finished, so nothing is known about it.")
-        elif t in _PAIR_TYPES and not (stage == "ran" or (stage is None and state == "complete")):
+        if run is None:
+            skip(t, "NOT_RUN", "This case was analysed before the record of what ran was kept, so nothing is claimed about this check. Run it again to check.")
+        elif t in _PAIR_TYPES and stage != "ran":
             if stage == "skipped":
                 skip(t, "STAGE_SKIPPED", "The run reached its time limit before the comparison between records. Run it again to check.")
             elif state == "failed":
                 skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
             else:
                 skip(t, "NOT_RUN", "The comparison between records has not run yet.")
-        elif t == "accident_date" and run.get("dated_records") == 0:
+        elif t == "accident_date" and dated == 0:
             skip(t, "NO_DATED_RECORD", "No record has a date the code could read, so there is nothing to compare a stated accident date with.")
         elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
             unread = run["unread"]
@@ -296,5 +297,6 @@ def checks(run: dict = None, state: str = "complete") -> dict:
             else:
                 skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
     whole = {x["type"] for x in skipped if "record_nos" not in x}
+    note = conflicts.accident_date_note(records) if records is not None and "accident_date" not in whole else None
     return {"conflict_types": [t for t in CONFLICT_LABELS if t not in whole], "labels": dict(CONFLICT_LABELS), "skipped": skipped,
-            "not_checked": [dict(x) for x in NOT_CHECKED], "notes": [dict(n) for n in run.get("notes") or []]}
+            "not_checked": [dict(x) for x in NOT_CHECKED], "notes": [note] if note else []}
diff --git a/app/backend/conflicts.py b/app/backend/conflicts.py
index f2ccd78..226eecb 100644
--- a/app/backend/conflicts.py
+++ b/app/backend/conflicts.py
@@ -8,41 +8,72 @@ from app.backend.ingest import evidence_span
 
 PHRASE_TO_DATE_CHARS = 40
 
-# T-141 r2 (GATE-M2 lib11): the content decides, not a coinciding date. A stated accident date later than the earliest record is a conflict only when
-# a record dated before it describes the collision or an injury mechanism (a clause of its own that is not history). Records dated before it that
-# do not are earlier visits: the case notes how many (accident_date_note), nothing is raised. "Accidents in 2019 and 2022" in an old note is history.
-_EVENT = re.compile(r"\b(?:collision|collided|crash\w*|MVA|MVC|MVI|rear[- ]?end\w*|struck|hit|wreck\w*|accident\w*|vehicle|airbag\w*|seat\s?belt\w*|"
-                    r"t-?bone\w*|side-?swip\w*|run\s+over|fell|fall(?:ing)?\s+(?:from|off|down))\b", re.I)
-_HISTORICAL = re.compile(r"\b(?:prior|previous|previously|earlier|history|hx|remote|years?\s+ago|as\s+a\s+child)\b", re.I)
+# T-141 r2/r3 (GATE-M2 lib11): the content decides, not a coinciding date. A stated accident date later than the earliest record is a conflict when a record
+# dated before it has any clause with injury, mechanism or accident vocabulary that is not clearly history or negated (a safe false positive beats a hidden
+# conflict). Only a record with none (a routine or annual visit, paperwork) or whose every such clause is plainly history ("car accidents in 2019 and 2022",
+# "Hx of MVA", "denies any accidents") is an earlier visit: the case notes how many (accident_date_note), nothing is raised.
+_EVENT = re.compile(r"\b(?:collision|collided|crash\w*|MVA|MVC|MVI|rear[- ]?end\w*|struck|wreck\w*|accident\w*|incident|pedestrian|motor\s+vehicle|vehicular|"
+                    r"hit\s+by|(?:was|were|got)\s+hit|(?:vehicle|car|truck|driver)\s+hit|hit\s+(?:them|him|us|me)|"
+                    r"hit\s+(?:a|the|my|our)\s+(?:car|vehicle|truck|pole|tree|wall|guardrail|curb)|"
+                    r"airbag\w*|seat\s?belt\w*|t-?bone\w*|side-?swip\w*|(?:run|ran)\s+over|run-over|"
+                    r"fell|fall(?:ing)?\s+(?:from|off|down)|slip(?:ped)?\s+and\s+fall|whiplash|injur\w*|trauma\w*|impact\w*|LOC|loss\s+of\s+consciousness)\b", re.I)
+_NEGATOR = {"no", "not", "denies", "denied", "denying", "without", "never", "negative", "neg", "none", "nor", "free"}
+_HIST_WORD = {"prior", "previous", "remote", "past", "earlier", "old", "hx", "history"}              # history only when it modifies the event noun, not "prior to"
+_HIST_ADVERB = re.compile(r"\bpreviously\s+(?:had|reported|involved|in|was|suffered)\s+(?:\w+\s+){0,3}$", re.I)
+_CLAUSE_HISTORY = re.compile(r"\b(?:years?\s+ago|last\s+year|as\s+a\s+child|remote(?:ly)?)\b", re.I)
 _YEAR = re.compile(r"\b(19\d\d|20\d\d)\b")
 _MODEL_YEAR = re.compile(r"\b(?:19|20)\d\d(?=\s+[A-Z][a-z])")
+_MONTH_YEAR = re.compile(r"\b(Jan(?:uary)?|Feb(?:ruary)?|Mar(?:ch)?|Apr(?:il)?|May|June?|July?|Aug(?:ust)?|Sep(?:t(?:ember)?)?|Oct(?:ober)?|Nov(?:ember)?|Dec(?:ember)?)\.?,?\s+((?:19|20)\d\d)\b", re.I)
+_MONTHS = {m: i for i, m in enumerate(["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"], 1)}
 _CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")
+_NEG_WINDOW, _HIST_WINDOW = 5, 3
 
 
-def _historical(clause: str, iso: str) -> bool:
-    """A clause is history when it says so, names a bare year before the stated one, or holds a full date more than a year before it. A full date within the
-    year before (MVA 12/30/2025 against a stated 2026-01-05) is a possible index event, and a model year ('a 2019 Honda Civic') is not a date."""
-    if _HISTORICAL.search(clause):
+def _days_between(a: str, b: str):
+    from datetime import date
+    try:
+        return (date.fromisoformat(b) - date.fromisoformat(a)).days
+    except ValueError:
+        return None
+
+
+def _clause_is_history(clause: str, stated: str, rec_iso: str) -> bool:
+    """The clause as a whole dates itself to the past: 'last year', 'N years ago', 'as a child', a full date more than a year before the STATED date (a full
+    date within the year before is a possible index event: MVA 12/30/2025 against a stated 2026-01-05), a month and year more than two months before the RECORD's
+    own date, or a bare year before the record's year (the year before it only when the record is not in January or February). A model year ('a 2019 Honda') is
+    not a date."""
+    if _CLAUSE_HISTORY.search(clause):
         return True
     rest = clause
     for d in sorted(dates.find_dates(clause), key=lambda x: -x["start"]):
-        if d["status"] == "parsed" and d["iso"] < iso and (_days_between(d["iso"], iso) or 0) > 365:
+        cands = [d["iso"]] if d["status"] == "parsed" else list(d.get("candidates") or [])
+        if cands and all((_days_between(c, stated) or 0) > 365 for c in cands):
             return True
         rest = rest[:d["start"]] + " " * (d["end"] - d["start"]) + rest[d["end"]:]
-    rest = _MODEL_YEAR.sub("    ", rest)
-    return any(int(y) < int(iso[:4]) for y in _YEAR.findall(rest))
+    ry, rm = int(rec_iso[:4]), int(rec_iso[5:7])
+    for m in _MONTH_YEAR.finditer(rest):
+        mo = _MONTHS[m.group(1)[:3].lower()]
+        if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2:
+            return True
+    rest = _MODEL_YEAR.sub("    ", _MONTH_YEAR.sub("    ", rest))
+    return any(int(y) < ry - (0 if rm > 2 else 1) for y in _YEAR.findall(rest))
 
 
-def _days_between(a: str, b: str):
-    from datetime import date
-    try:
-        return (date.fromisoformat(b) - date.fromisoformat(a)).days
-    except ValueError:
-        return None
+def _is_event_word(clause: str, m) -> bool:
+    """One vocabulary match in a clause counts as an event unless a negator stands within five words before it ('denies any accidents', 'no recent injuries')
+    or a history word modifies it within three words before it ('prior accident', 'history of MVA'; not 'prior to the collision')."""
+    pre = clause[:m.start()]
+    words = [w.strip(".:()\"'").lower() for w in pre.split()]
+    if any(w in _NEGATOR for w in words[-_NEG_WINDOW:]):
+        return False
+    tail = words[-_HIST_WINDOW:]
+    if any(w in _HIST_WORD and not (i + 1 < len(tail) and tail[i + 1] == "to") for i, w in enumerate(tail)):
+        return False
+    return not _HIST_ADVERB.search(pre)
 
 
-def _describes_event(rec: dict, iso: str) -> bool:
-    """The record has a clause that names a collision, accident or injury mechanism and is not history (judged per clause, not per sentence)."""
+def _describes_event(rec: dict, stated: str) -> bool:
+    """The record has a clause with injury, mechanism or accident vocabulary that is neither negated nor history (judged per clause and per word)."""
     from app.backend import sentences
     text = rec.get("excerpt") or ""
     for a, b in sentences.stripped_spans(text):
@@ -50,7 +81,7 @@ def _describes_event(rec: dict, iso: str) -> bool:
         for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
             unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
         for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
-            if _EVENT.search(clause) and not _historical(clause, iso):
+            if any(_is_event_word(clause, m) for m in _EVENT.finditer(clause)) and not _clause_is_history(clause, stated, rec["date_iso"]):
                 return True
     return False
 
@@ -138,7 +169,7 @@ def accident_date_conflicts(records: list) -> list:
 
 def accident_date_note(records: list):
     """T-141 r2: when one stated accident date is later than some records and no conflict is raised for it, how many records predate it.
-    Info for the case's `checks.notes`; never a flag. None when there is nothing to say."""
+    Info for the case's `checks.notes` (computed when the case is read, from the current dates); never a flag. None when there is nothing to say."""
     enc = _encounters(records)
     distinct = sorted({s["iso"] for s in stated_accident_dates(records)})
     if len(distinct) != 1 or not enc or accident_date_conflicts(records):
@@ -150,7 +181,7 @@ def accident_date_note(records: list):
     n = len(before)
     lead = f"{n} record predates" if n == 1 else f"{n} records predate"
     return {"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": n, "record_nos": [r["n"] for r in before], "stated_date": iso,
-            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. None describes a collision, so no date conflict is raised; check that they are earlier care."}
+            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care."}
 
 
 _TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
diff --git a/app/backend/present.py b/app/backend/present.py
index 27f121f..038cd92 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -335,7 +335,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
     return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
             "records": record_views, "undated_entries": undated, "entries": dated,
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete"), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete", store.load_records(conn, case_id, raw)), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:17.421Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141 && sed -n 1,80p r2_variants.py; echo ======; sed -n 1,40p probe2.py; echo =====; wc -l r2_*.py"
}
````

### User / tool · 2026-11-02T14:20:17.561Z

**tool result**
````
import sys
root = sys.argv[1]; sys.path.insert(0, root)
from app.backend import conflicts as C
def R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")
INT = lambda n, d, date: R(n, d, "Intake", f"Date of accident per intake form: {date}.")
V = [
 # (label, expected: 'conflict' | 'info', records)
 ("V1 billing stmt before accident NAMES the collision", "conflict",
  [R(1,"2026-01-05","Hobbleton Clinic, billing statement","Emergency services after motor vehicle collision. Balance forward."), R(2,"2026-01-12","Capital PT, visit 1","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V2 billing stmt before accident, no mechanism", "info",
  [R(1,"2026-01-05","Hobbleton Clinic, billing statement","Balance forward."), R(2,"2026-01-12","Capital PT, visit 1","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V3 intake dated before accident, says rear-ended", "conflict",
  [R(1,"2026-01-05","Intake","New patient intake. Neck pain after being rear-ended. Date of accident: 2026-01-09."), R(2,"2026-01-12","PT","Exam: ok.")]),
 ("V4 intake dated before accident, no mechanism, states date (form dated before the accident it states)", "info",
  [R(1,"2026-01-05","Intake","New patient intake. Prior accidents? Yes [ ] No [X]. Date of accident: 2026-01-09."), R(2,"2026-01-12","PT","Exam: ok.")]),
 ("V5 PT note before accident: slipped and fell on ice (mechanism)", "conflict",
  [R(1,"2026-01-05","PT","Slipped and fell on ice, wrist pain."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V6 earlier note: 'slip and fall at the store' (no 'fell')", "conflict",
  [R(1,"2026-01-05","PT","Slip and fall at the grocery store, wrist pain."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V7 earlier note: pedestrian vs auto, neck pain", "conflict",
  [R(1,"2026-01-05","ER","Pedestrian vs auto. Neck pain 7/10."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V8 earlier note: 'Neck pain since the incident, whiplash'", "conflict",
  [R(1,"2026-01-05","Chiro","Neck pain since the incident. Whiplash pattern."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V9 earlier note: 'car accident last year, recovered' (history, no year digits)", "info",
  [R(1,"2026-01-05","PCP","Annual physical. Reports a car accident last year, fully recovered."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V10 earlier note: 'rear-ended in March 2025' (history)", "info",
  [R(1,"2026-01-05","PCP","Annual physical. Was rear-ended in March 2025, resolved."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V11 earlier ER (Dec 30 2025) 'rear-ended in December 2025', stated Jan 5", "conflict",
  [R(1,"2025-12-30","ER","Rear-ended in December 2025. Neck pain."), R(2,"2026-01-05","PT","Exam: ok."), INT(3,"2026-02-20","2026-01-05")]),
 ("V12 earlier record is paperwork with 'vehicle' as a noun (vehicle registration form)", "info",
  [R(1,"2026-01-05","DMV","Vehicle registration renewed."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V13 earlier PCP: 'hit' as verb in unrelated meaning ('hit the gym', 'hit 150 lb')", "info",
  [R(1,"2026-01-05","PCP","Patient hit her weight goal of 150 lb. Annual physical."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V14 earlier PCP: 'fall' as season / 'fall risk screening'", "info",
  [R(1,"2026-01-05","PCP","Annual physical. Fall risk screen negative. Flu shot given in the fall."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V15 earlier PCP: 'Previous accident' wording lowercase prior event with clause split by comma", "info",
  [R(1,"2026-01-05","PCP","Annual physical, history reviewed; MVA in 2019, resolved."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V16 earlier ER same day cluster: mechanism in 2nd clause after comma, history word in 1st", "conflict",
  [R(1,"2026-01-05","ER","No prior neck problems, was struck by a car while crossing the street. Neck pain."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V17 earlier ER: 'No history of prior injury; restrained driver, MVC' (semicolon)", "conflict",
  [R(1,"2026-01-05","ER","No history of prior injury; restrained driver, MVC. Neck pain."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V18 earlier ER: 'no history of injury in MVC' same clause (history word, mechanism same clause)", "conflict",
  [R(1,"2026-01-05","ER","MVC with no history of loss of consciousness"), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
 ("V19 two records before: first benign, second collision; compare against earliest EVENT record", "conflict",
  [R(1,"2026-01-02","PCP","Annual physical."), R(2,"2026-01-05","ER","Rear-end collision. Neck pain."), R(3,"2026-01-12","PT","Exam: ok."), INT(4,"2026-01-20","2026-01-09")]),
 ("V20 record AFTER the stated date describes collision, nothing before: no record predates", "none",
  [R(1,"2026-01-09","ER","Rear-end collision. Neck pain."), R(2,"2026-01-12","PT","Exam: ok."), INT(3,"2026-01-20","2026-01-09")]),
]
bad = 0
for label, exp, recs in V:
    out = C.accident_date_conflicts(recs)
    note = C.accident_date_note(recs)
    got = "conflict" if out else ("info" if note else "none")
    flag = "" if got == exp else "   <<< MISMATCH"
    bad += bool(flag)
    first = out[0]["first_treatment_date"] if out else None
    print(f"{got:8} exp={exp:8} | {label} | first={first} | note={note['count'] if note else None}{flag}")
print("mismatches:", bad)
======
import sys
root = sys.argv[1]; sys.path.insert(0, root)
from app.backend import conflicts as C
def R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind="encounter")
sc = {
 "A baseline lib11-like (expect no conflict)": [R(1,"2026-03-04","PCP","Annual visit. Car accidents in 2019 and 2022."), R(2,"2026-03-18","EMS","Passenger vehicle struck from behind."), R(3,"2026-03-27","Intake","Date of injury: 2026-03-18.")],
 "B ER describes collision in unlisted words (hit from behind), stated date = follow-up date (TRUE conflict)": [R(1,"2026-01-09","ER","Restrained driver, vehicle hit from behind at a stoplight. Neck pain."), R(2,"2026-01-19","PT","Follow-up. Neck pain 5/10."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-19.")],
 "C collision in Dec of PRIOR year, stated date in Jan matches follow-up (TRUE conflict)": [R(1,"2025-12-30","ER","MVA 12/30/2025, neck pain."), R(2,"2026-01-05","PT","Follow-up. Neck pain 5/10."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-05.")],
 "D ER sentence also contains the word 'history' (TRUE conflict)": [R(1,"2026-01-09","ER","Rear-end collision, no history of loss of consciousness. Neck pain."), R(2,"2026-01-19","PT","Follow-up. Neck pain 5/10."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-19.")],
 "E ER with plain collision (expect conflict)": [R(1,"2026-01-09","ER","Rear-end collision. Neck pain."), R(2,"2026-01-19","PT","Follow-up. Neck pain 5/10."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-19.")],
 "F earliest record no collision word at all, neck pain 'after being in a car' (TRUE conflict)": [R(1,"2026-01-09","ER","Pt in car when another vehicle hit them. Neck pain 7/10."), R(2,"2026-01-19","PT","Follow-up. Neck pain 5/10."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-19.")],
 "G earlier-year digits in same sentence as collision (TRUE conflict)": [R(1,"2026-01-09","ER","Rear-end collision, driver of a 2019 Honda Civic. Neck pain."), R(2,"2026-01-19","PT","Follow-up."), R(3,"2026-02-20","Intake","Date of accident per intake form: 2026-01-19.")],
 "H earlier record says 'fell' (event word) pre-accident fall, then collision (expect no skip -> conflict; hmm)": [R(1,"2026-03-04","PCP","Patient fell off a ladder last week. Wrist pain."), R(2,"2026-03-18","EMS","Passenger vehicle struck from behind."), R(3,"2026-03-27","Intake","Date of injury: 2026-03-18.")],
 "I two stated dates (still conflict)": [R(1,"2026-03-04","PCP","Annual visit."), R(2,"2026-03-18","EMS","Collision on 2026-03-18."), R(3,"2026-03-27","Intake","Date of injury: 2026-03-20.")],
 "J stated date also dated by the SAME record only": [R(1,"2026-03-04","PCP","Annual visit."), R(3,"2026-03-27","Intake","Date of injury: 2026-03-27.")],
 "K stated date earlier than first record but another record on that day (no skip needed)": [R(1,"2026-03-18","ER","Collision."), R(3,"2026-03-27","Intake","Date of injury: 2026-03-10.")],
 "L collision mention only on a LATER record than stated date; first record neck pain pre-dates (genuine pre-accident neck pain; skip hides)": [R(1,"2026-03-04","Chiro","Neck pain 6/10, adjusted."), R(2,"2026-03-18","ER","Neck strain."), R(3,"2026-03-19","Intake","Date of injury: 2026-03-18. Rear-end collision.")],
}
for k, rs in sc.items():
    out = C.accident_date_conflicts(rs)
    print(("CONFLICT" if out else "none    "), "|", k, "|", [o["category"] for o in out])
=====
      61 r2_checks_matrix.py
      12 r2_lib11.py
      44 r2_mutate.py
      23 r2_real_crash.py
      34 r2_stale_checks.py
      58 r2_variants.py
      25 r2_variants2.py
     257 total
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:21.549Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141 && SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/T141r3_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; for f in r2_variants.py r2_variants2.py; do $PY -I $f $A 2>&1 | tail -35; done; $PY -I probe2.py $A"
}
````

### User / tool · 2026-11-02T14:20:22.021Z

**tool result**
````
conflict exp=conflict | V1 billing stmt before accident NAMES the collision | first=2026-01-05 | note=None
info     exp=info     | V2 billing stmt before accident, no mechanism | first=None | note=1
conflict exp=conflict | V3 intake dated before accident, says rear-ended | first=2026-01-05 | note=None
conflict exp=info     | V4 intake dated before accident, no mechanism, states date (form dated before the accident it states) | first=2026-01-05 | note=None   <<< MISMATCH
conflict exp=conflict | V5 PT note before accident: slipped and fell on ice (mechanism) | first=2026-01-05 | note=None
conflict exp=conflict | V6 earlier note: 'slip and fall at the store' (no 'fell') | first=2026-01-05 | note=None
conflict exp=conflict | V7 earlier note: pedestrian vs auto, neck pain | first=2026-01-05 | note=None
conflict exp=conflict | V8 earlier note: 'Neck pain since the incident, whiplash' | first=2026-01-05 | note=None
info     exp=info     | V9 earlier note: 'car accident last year, recovered' (history, no year digits) | first=None | note=1
info     exp=info     | V10 earlier note: 'rear-ended in March 2025' (history) | first=None | note=1
conflict exp=conflict | V11 earlier ER (Dec 30 2025) 'rear-ended in December 2025', stated Jan 5 | first=2025-12-30 | note=None
info     exp=info     | V12 earlier record is paperwork with 'vehicle' as a noun (vehicle registration form) | first=None | note=1
info     exp=info     | V13 earlier PCP: 'hit' as verb in unrelated meaning ('hit the gym', 'hit 150 lb') | first=None | note=1
info     exp=info     | V14 earlier PCP: 'fall' as season / 'fall risk screening' | first=None | note=1
info     exp=info     | V15 earlier PCP: 'Previous accident' wording lowercase prior event with clause split by comma | first=None | note=1
conflict exp=conflict | V16 earlier ER same day cluster: mechanism in 2nd clause after comma, history word in 1st | first=2026-01-05 | note=None
conflict exp=conflict | V17 earlier ER: 'No history of prior injury; restrained driver, MVC' (semicolon) | first=2026-01-05 | note=None
conflict exp=conflict | V18 earlier ER: 'no history of injury in MVC' same clause (history word, mechanism same clause) | first=2026-01-05 | note=None
conflict exp=conflict | V19 two records before: first benign, second collision; compare against earliest EVENT record | first=2026-01-05 | note=None
none     exp=none     | V20 record AFTER the stated date describes collision, nothing before: no record predates | first=None | note=None
mismatches: 1
info     exp=info     | W1 PCP annual: 'Denies any accidents or falls.'
info     exp=info     | W2 PCP annual: 'No recent accidents or injuries.'
conflict exp=conflict | W3 ER: 'Healthy prior to the rear-end collision. Neck pain since.'
conflict exp=conflict | W4 ER: 'Previously asymptomatic until the motor vehicle collision.'
conflict exp=conflict | W5 ER: 'MVC with no history of LOC.'
info     exp=info     | W6 Billing before accident: 'Services after MVA of 03/04/2024' (old full date, history)
info     exp=info     | W7 PCP: 'MVA on 03/04/2024, resolved' (full date >1y, no history word)
info     exp=info     | W8 Insurance card: 'Auto insurance card on file; vehicle: 2019 Honda' (model year)
conflict exp=conflict | W9 PCP: 'Patient hit by a car 2 days ago' (true event)
info     exp=info     | W10 PCP: 'rear-ended' plus 'Date of accident' absent, hyphen clause 'rear-ended - resolved 2021' (year in 2nd clause)
mismatches: 0
Stated accident date January 9, 2026 (“Date of accident per intake form: 2026-01-09”) is later than the earliest recorded date, January 5, 2026 (record 1: Hobbleton Clinic, billing statement), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Hobbleton Clinic, billing statement is paperwork, not a visit, the first recorded visit is January 12, 2026 (record 2: Capital PT, visit 1), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
none     | A baseline lib11-like (expect no conflict) | []
CONFLICT | B ER describes collision in unlisted words (hit from behind), stated date = follow-up date (TRUE conflict) | ['accident_date_after_treatment']
CONFLICT | C collision in Dec of PRIOR year, stated date in Jan matches follow-up (TRUE conflict) | ['accident_date_after_treatment']
CONFLICT | D ER sentence also contains the word 'history' (TRUE conflict) | ['accident_date_after_treatment']
CONFLICT | E ER with plain collision (expect conflict) | ['accident_date_after_treatment']
CONFLICT | F earliest record no collision word at all, neck pain 'after being in a car' (TRUE conflict) | ['accident_date_after_treatment']
CONFLICT | G earlier-year digits in same sentence as collision (TRUE conflict) | ['accident_date_after_treatment']
CONFLICT | H earlier record says 'fell' (event word) pre-accident fall, then collision (expect no skip -> conflict; hmm) | ['accident_date_after_treatment']
CONFLICT | I two stated dates (still conflict) | ['accident_dates_differ']
none     | J stated date also dated by the SAME record only | []
none     | K stated date earlier than first record but another record on that day (no skip needed) | []
none     | L collision mention only on a LATER record than stated date; first record neck pain pre-dates (genuine pre-accident neck pain; skip hides) | []
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:40.468Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SP/T141r3_scripts; cat > $SP/T141r3_scripts/r3_variants.py <<'EOF'\nimport sys\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import conflicts as C\ndef R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind=\"encounter\")\nINT = lambda n, d, date: R(n, d, \"Intake\", f\"Date of accident per intake form: {date}.\")\ndef case(ex, d=\"2026-01-05\"):\n    return [R(1,d,\"ER\",ex), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]\n# (label, expected, excerpt)  conflict = a real earlier-collision description a paralegal must see\nX = [\n # negations the brief names\n (\"N1 'No prior accidents' (history/negated)\", \"info\", \"Annual physical. No prior accidents.\"),\n (\"N2 'Denies MVC'\", \"info\", \"Annual physical. Denies MVC.\"),\n (\"N3 'Denies any motor vehicle collision or injury'\", \"info\", \"Annual physical. Denies any motor vehicle collision or injury.\"),\n (\"N4 'MVA in 2015'\", \"info\", \"Annual physical. MVA in 2015, resolved.\"),\n (\"N5 'History of MVA 2015'\", \"info\", \"Annual physical. History of MVA 2015.\"),\n (\"N6 'Hx: rear-end collision 2018'\", \"info\", \"Annual physical. Hx rear-end collision 2018.\"),\n # negator window hides a TRUE collision\n (\"T1 'No LOC after the accident'\", \"conflict\", \"ER visit. No LOC after the accident. Neck pain.\"),\n (\"T2 'Has not worked since the accident'\", \"conflict\", \"Follow-up. Has not worked since the accident. Neck pain.\"),\n (\"T3 'No relief of neck pain since the MVA'\", \"conflict\", \"Follow-up. No relief of neck pain since the MVA.\"),\n (\"T4 'Patient was not wearing a seatbelt in the rear-end collision'\", \"conflict\", \"ER visit. Patient was not wearing a seatbelt in the rear-end collision.\"),\n (\"T5 'Unable to drive, no improvement after the crash'\", \"conflict\", \"Follow-up. No improvement since the crash.\"),\n (\"T6 'No airbag deployment in the collision' (airbag negated, collision 4 words after 'no')\", \"conflict\", \"ER visit. No airbag deployment in the collision. Neck pain.\"),\n (\"T7 'Without fracture after the MVC'\", \"conflict\", \"ER visit. Without fracture after the MVC.\"),\n (\"T8 'Never lost consciousness during the crash'\", \"conflict\", \"ER visit. Never lost consciousness during the crash.\"),\n (\"T9 'No other injuries; was in an MVA' (semicolon ok)\", \"conflict\", \"ER visit. No other injuries; was in an MVA.\"),\n (\"T10 'Negative for fracture after rear-end collision'\", \"conflict\", \"ER visit. Negative for fracture after rear-end collision.\"),\n # history word window hides a TRUE collision\n (\"H1 'History: rear-ended at a stoplight'\", \"conflict\", \"ER visit. History: rear-ended at a stoplight. Neck pain.\"),\n (\"H2 'Neck pain for the past week since the MVA'\", \"conflict\", \"Chiro visit. Neck pain for the past week since the MVA.\"),\n (\"H3 'History of present illness: MVC today'\", \"conflict\", \"ER visit. History of present illness: MVC today.\"),\n (\"H4 'Earlier today the pt was in an MVA' \", \"conflict\", \"ER visit. Earlier today the pt was in an MVA. Neck pain.\"),\n (\"H5 'Past medical history none. Pt in MVC'\", \"conflict\", \"ER visit. PMH none; pt in MVC this week.\"),\n (\"H6 'Old man hit by a car'\", \"conflict\", \"ER visit. Old man hit by a car crossing the street.\"),\n (\"H7 'Neck pain started a few years ago, worse after rear-end collision' (years ago in same clause)\", \"conflict\", \"Chiro visit. Neck pain started years ago and worsened after the rear-end collision.\"),\n (\"H8 'last year' + this-week event same clause\", \"conflict\", \"ER visit. Seen last year for knee, now rear-ended this week.\"),\n (\"H9 'Prior to arrival, pt was in MVC' (not hist)\", \"conflict\", \"ER visit. Prior to arrival the patient was in an MVC. Neck pain.\"),\n (\"H10 'previous visit ... MVA' \", \"conflict\", \"Follow-up. At the previous visit she reported the MVA and neck pain.\"),\n (\"H11 'remote' wording fine: 'MVA remote past' \", \"info\", \"Annual physical. MVA remote past, resolved.\"),\n # bare years / month-year\n (\"Y1 'MVA in 2025' record dated 2026-06, stated later\", \"conflict_late\", \"Intake. Rear-ended in 2025.\"),\n (\"Y2 'rear-ended in November 2025' record 2026-01-05\", \"conflict\", \"ER visit. Rear-ended in November 2025.\"),\n (\"Y3 'rear-ended in October 2025' record 2026-01-05 (3 months)\", \"conflict_or_info\", \"ER visit. Rear-ended in October 2025.\"),\n # benign wording\n (\"B1 'Fall risk screen negative'\", \"info\", \"Annual physical. Fall risk screen negative.\"),\n (\"B2 'Impact of diabetes on diet counselled'\", \"info\", \"Annual physical. Impact of diabetes on diet counselled.\"),\n (\"B3 'Injury prevention handout given'\", \"conflict_ok\", \"Annual physical. Injury prevention handout given.\"),\n]\nfor label, exp, ex in X:\n    recs = case(ex, \"2026-06-05\" if label.startswith(\"Y1\") else \"2026-01-05\")\n    if label.startswith(\"Y1\"):\n        recs = [R(1,\"2026-06-05\",\"ER\",ex), R(2,\"2026-06-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-06-20\",\"2026-06-09\")]\n    out = C.accident_date_conflicts(recs)\n    got = \"conflict\" if out else \"info\"\n    print(f\"{got:9} exp={exp:16} | {label}\")\nEOF\ncd $SP/T141r3_scripts && /Users/arsis/zlayt-pm-project/.venv/bin/python -I r3_variants.py $SP/T141r3_head"
}
````

### User / tool · 2026-11-02T14:20:40.690Z

**tool result**
````
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

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:20:55.710Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/T141r3_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141; cat > $SP/T141r3_scripts/r3_note.py <<'EOF'\nimport sys\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import conflicts as C\ndef R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind=\"encounter\")\nrecs=[R(1,\"2026-01-05\",\"ER\",\"ER visit. No LOC after the accident. Neck pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")]\nprint(C.accident_date_conflicts(recs)); print(C.accident_date_note(recs))\nEOF\n$PY -I $SP/T141r3_scripts/r3_note.py $A; echo ==== stale; $PY -I r2_stale_checks.py $A 2>&1 | tail -15; echo === matrix; $PY -I r2_checks_matrix.py $A 2>&1 | tail -40; echo === crash; $PY -I r2_real_crash.py $A 2>&1 | tail -10"
}
````

### User / tool · 2026-11-02T14:20:58.130Z

**tool result**
````
[]
{'type': 'accident_date', 'code': 'RECORDS_PREDATE_ACCIDENT', 'count': 1, 'record_nos': [1], 'stated_date': '2026-01-09', 'text': '1 record predates the stated accident date, January 9, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.'}
==== stale
ingested | notes: ['1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.'] | skipped: [] | accident-date flags: []
record 2 date_status: ambiguous ['2026-03-06', '2026-06-03']
after confirming record 2 = 2026-03-06 | notes: [] | skipped: [] | accident-date flags: ['accident_date_after_treatment']
=== matrix
llm call failed call_id=c1c6fe9b7b287 step=extract_es attempt=1 prompt_hash=dfcf30c03eee15e6c8d6dfef3c55737d074e5eaba704225c99f09ad867361de2
llm call failed call_id=cc5cd3b21e392 step=extract_es attempt=1 prompt_hash=c239943994d9e08d323e7f8253d5713061b0472372f8b7aca57d68f3a18d7d53
llm call failed call_id=cc16cf39b9bc1 step=flags attempt=1 prompt_hash=35115068add54c861c98cc346a70423e67ce9e8d3734d19fe7087efff3bd66dd
llm call failed call_id=cc2a7a3be6f35 step=flags attempt=1 prompt_hash=884b2d3c2b3553b852f4d24b8f7becc6e4bc0eaf08bc3cd91427bfeb7a0a03c7
S1 sample ingested only                                    ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None)] notes=[]
S2 sample complete                                         ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=[]
   db status after complete: ready
   db status: failed timeout
S3 deadline when 'extract' starts                          ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'STAGE_SKIPPED', None), ('denial_vs_history', 'STAGE_SKIPPED', None)] notes=[]
   db status: failed timeout
S3 deadline when 'verify' starts                           ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'STAGE_SKIPPED', None), ('denial_vs_history', 'STAGE_SKIPPED', None)] notes=[]
   db status: failed timeout
S3 deadline when 'amounts' starts                          ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'STAGE_SKIPPED', None), ('denial_vs_history', 'STAGE_SKIPPED', None)] notes=[]
   db status: failed timeout
S3 deadline when 'conflicts' starts                        ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=[]
   db status: failed timeout
S3 deadline when 'flags' starts                            ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=[]
S4 re-run in flight (running, pending)                     ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None)] notes=[]
S5 legacy ready, no run_checks                             ran=[] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes=[]
S5b legacy failed, no run_checks                           ran=[] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes=[]
S6 case_lib09_spanish_inter complete                       ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'LANGUAGE_PARTIAL', [2, 4, 7]), ('denial_vs_history', 'LANGUAGE_PARTIAL', [2, 4, 7]), ('accident_date', 'LANGUAGE_PARTIAL', [2, 4, 7])] notes=[]
S6 case_lib11_priors_and_le complete                       ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=['RECORDS_PREDATE_ACCIDENT']
   status ready
S7 all-Spanish run                                         ran=['provider_name'] skipped=[('plan_vs_early_end', 'LANGUAGE', None), ('denial_vs_history', 'LANGUAGE', None), ('accident_date', 'LANGUAGE', None)] notes=[]
   langs: 
U1 checks() default                                        ran=[] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes=[]
U2 checks(None,'failed')                                   ran=[] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes=[]
U3 checks(None,'not_run')                                  ran=[] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None), ('accident_date', 'NOT_RUN', None), ('provider_name', 'NOT_RUN', None)] notes=[]
=== crash
after first run : (['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'], [])
re-run raised: simulated crash inside the conflict stage
after crashed re-run: (['accident_date', 'provider_name'], [('plan_vs_early_end', 'RUN_FAILED'), ('denial_vs_history', 'RUN_FAILED')])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:03.061Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141; cat r2_mutate.py"
}
````

### User / tool · 2026-11-02T14:21:03.141Z

**tool result**
````
import subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1]); PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
CF, CC, PLN, PR = "app/backend/conflicts.py", "app/backend/conflict_candidates.py", "app/backend/pipeline.py", "app/backend/present.py"
muts = [
 (CF, 'r"t-?bone\\w*|side-?swip\\w*|run\\s+over|fell|', 'r"fell|', "N1 drop t-bone/sideswipe/run over words"),
 (CF, "airbag\\w*|seat\\s?belt\\w*|", "", "N2 drop airbag/seatbelt words"),
 (CF, "|hit|wreck", "|wreck", "N3 drop 'hit'"),
 (CF, "accident\\w*|vehicle|", "accident\\w*|", "N4 drop 'vehicle'"),
 (CF, "    if _HISTORICAL.search(clause):\n        return True", "    if False:\n        return True", "N5 history word no longer historical"),
 (CF, "> 365:\n            return True", "> 365000:\n            return True", "N6 full date >1y never historical"),
 (CF, "rest = _MODEL_YEAR.sub(\"    \", rest)", "pass", "N7 model year not masked"),
 (CF, "return any(int(y) < int(iso[:4]) for y in _YEAR.findall(rest))", "return False", "N8 bare earlier year never historical"),
 (CF, "_CLAUSE_SPLIT = re.compile(r\"[;,]|\\s[-\\u2013\\u2014]\\s|\\s\\(|\\)\")", "_CLAUSE_SPLIT = re.compile(r\"[;]\")", "N9 split only on ;"),
 (CF, "_CLAUSE_SPLIT = re.compile(r\"[;,]|", "_CLAUSE_SPLIT = re.compile(r\"[;]|", "N10 no comma split"),
 (CF, "return [o for o in records if o.get(\"date_iso\") and o[\"date_iso\"] < s[\"iso\"] and _describes_event(o, s[\"iso\"])]", "return [o for o in records if o.get(\"date_iso\") and o[\"date_iso\"] < s[\"iso\"]]", "N11 content test off (any earlier record)"),
 (CF, "first = min(r[\"date_iso\"] for r in _event_records(later[0], enc))", "pass", "N12 compare with earliest record, not earliest event record"),
 (CF, "later = [s for s in later if _event_records(s, enc)]", "pass", "N13 no content filter at all"),
 (CF, "    if len(distinct) < 2:\n        later", "    if True:\n        later", "N14 content filter also with two stated dates"),
 (CF, "return None\n    iso = distinct[0]", "return None\n    iso = distinct[0]; return None", "N15 note always None"),
 (CF, "or accident_date_conflicts(records):\n        return None", ":\n        pass", "N16 note emitted even with a conflict"),
 (CF, "paper = [r for r in first_recs if gaps.admin_label(r)]", "paper = []", "N17 paperwork branch off"),
 (CF, "if d[\"status\"] == \"parsed\" and d[\"iso\"] < iso", "if False and d[\"status\"] == \"parsed\" and d[\"iso\"] < iso", "N18 full-date-before check off"),
 (CC, "        elif t in _PAIR_TYPES and not (stage == \"ran\" or (stage is None and state == \"complete\")):", "        elif False:", "C1 pair types never skipped"),
 (CC, 'skip(t, "STAGE_SKIPPED"', 'skip(t, "NOT_RUN"', "C2 STAGE_SKIPPED relabelled"),
 (CC, "elif t == \"accident_date\" and run.get(\"dated_records\") == 0:", "elif False:", "C3 NO_DATED_RECORD off"),
 (CC, "elif t in _ENGLISH_RULE_TYPES and run.get(\"unread\"):", "elif False:", "C4 language skip off"),
 (CC, "if run.get(\"read_records\") == 0:", "if False:", "C5 all-Spanish treated as partial"),
 (CC, "whole = {x[\"type\"] for x in skipped if \"record_nos\" not in x}", "whole = set()", "C6 conflict_types ignores whole skips"),
 (CC, "if lang != \"en\":", "if lang not in ('en', 'uncertain'):", "C7 uncertain counted as read"),
 (CC, "if state == \"failed\" and not known:", "if False:", "C8 failed w/o summary claims all ran"),
 (PLN, "\"ran\" if conflicts_ran else \"skipped\"", "\"ran\"", "P1 stage always ran (deadline)"),
 (PLN, "    _store_run_checks(conn, cid, recs, \"pending\")           #", "    pass           #", "P2 no pending at run start"),
 (PLN, "    _store_run_checks(conn, cid, ing[\"records\"], \"pending\")\n", "", "P3 no summary at ingest"),
 (PR, "\"failed\" if case[\"status\"] == \"failed\" else \"not_run\" if case[\"status\"] in (\"ingested\", \"running\") else \"complete\"", "\"complete\"", "R1 state always complete"),
]
tests = ["tests/unit/test_conflicts.py", "tests/unit/test_conflict_candidates.py", "tests/unit/test_t141_checks_per_case.py", "tests/unit/test_t116_r4_all_dated_records.py", "tests/unit/test_api_routes.py", "tests/unit/test_t093_j3_controls_reachable.py"]
for rel, old, new, label in muts:
    p = root / rel; src = p.read_text()
    if old not in src: print("SKIP (pattern not found)", label); continue
    p.write_text(src.replace(old, new, 1))
    r = subprocess.run([PY, "-I", "-m", "pytest", *tests, "-q", "-p", "no:cacheprovider", "--deselect", "tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted"], cwd=root, capture_output=True, text=True)
    p.write_text(src)
    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]
    print(("KILLED  " if r.returncode else "SURVIVED"), label, "|", tail[:100], flush=True)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:06.048Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP/T141r3_head && timeout 900 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T14:21:06.144Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:10.012Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP/T141r3_head && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_conflicts.py tests/unit/test_conflict_candidates.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t141_r3_variants.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T14:21:19.227Z

**tool result**
````
........................................................................ [ 24%]
........................................................................ [ 49%]
........................................................................ [ 74%]
........................................................................ [ 98%]
...                                                                      [100%]
291 passed in 8.76s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:25.412Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP/T141r3_head; grep -n \"_store_run_checks\" app/backend/*.py; grep -n \"elif t in _ENGLISH_RULE_TYPES\" -A8 app/backend/conflict_candidates.py | head -20"
}
````

### User / tool · 2026-11-02T14:21:25.511Z

**tool result**
````
app/backend/pipeline.py:161:def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
app/backend/pipeline.py:305:    _store_run_checks(conn, cid, ing["records"], "pending")
app/backend/pipeline.py:388:    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
app/backend/pipeline.py:483:    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
291:        elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
292-            unread = run["unread"]
293-            nos = sorted(n for v in unread.values() for n in v)
294-            langs = " and ".join(_LANG_WORD.get(k, k) for k in unread)
295-            if run.get("read_records") == 0:
296-                skip(t, "LANGUAGE", f"This check reads English wording and every record is in {langs}, so it could not find anything.")
297-            else:
298-                skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
299-    whole = {x["type"] for x in skipped if "record_nos" not in x}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:21:39.093Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $SP/T141r3_scripts/r3_mutate.py <<'EOF'\nimport subprocess, sys, pathlib\nroot = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCF, CC, PLN, PR = \"app/backend/conflicts.py\", \"app/backend/conflict_candidates.py\", \"app/backend/pipeline.py\", \"app/backend/present.py\"\nmuts = [\n (CF, \"if ((ry * 12 + rm) - (int(m.group(2)) * 12 + mo)) > 2:\", \"if False:\", \"M1 month-year history off\"),\n (CF, \"if cands and all((_days_between(c, stated) or 0) > 365 for c in cands):\", \"if False:\", \"M2 full-date >1y history off (r2 N6/N18)\"),\n (CF, \"(_days_between(c, stated) or 0) > 365\", \"(_days_between(c, stated) or 0) > 36500\", \"M2b >365 -> never\"),\n (CF, \"return any(int(y) < ry - (0 if rm > 2 else 1) for y in _YEAR.findall(rest))\", \"return False\", \"M3 bare earlier year never history\"),\n (CF, \"return any(int(y) < ry - (0 if rm > 2 else 1) for y in\", \"return any(int(y) < ry for y in\", \"M3b no Jan/Feb leniency\"),\n (CF, \"    if _CLAUSE_HISTORY.search(clause):\\n        return True\", \"    if False:\\n        return True\", \"M4 last year/years ago off\"),\n (CF, \"if any(w in _NEGATOR for w in words[-_NEG_WINDOW:]):\\n        return False\", \"if False:\\n        return False\", \"M5 negation off\"),\n (CF, \"if any(w in _HIST_WORD and\", \"if False and any(w in _HIST_WORD and\", \"M6 history-word off\"),\n (CF, \"and not (i + 1 < len(tail) and tail[i + 1] == \\\"to\\\")\", \"\", \"M7 'prior to' counts as history\"),\n (CF, \"return not _HIST_ADVERB.search(pre)\", \"return True\", \"M8 'previously had' adverb off\"),\n (CF, \"t-?bone\\\\w*|\", \"\", \"W1 drop t-bone\"), (CF, \"side-?swip\\\\w*|\", \"\", \"W2 drop sideswipe\"), (CF, \"(?:run|ran)\\\\s+over|run-over|\", \"\", \"W3 drop run over\"),\n (CF, \"airbag\\\\w*|\", \"\", \"W4 drop airbag\"), (CF, \"seat\\\\s?belt\\\\w*|\", \"\", \"W5 drop seatbelt\"), (CF, \"pedestrian|\", \"\", \"W6 drop pedestrian\"),\n (CF, \"incident|\", \"\", \"W7 drop incident\"), (CF, \"whiplash|\", \"\", \"W8 drop whiplash\"), (CF, \"|trauma\\\\w*\", \"\", \"W9 drop trauma\"), (CF, \"|impact\\\\w*\", \"\", \"W10 drop impact\"),\n (CF, \"|LOC|loss\\\\s+of\\\\s+consciousness\", \"\", \"W11 drop LOC\"), (CF, \"injur\\\\w*|\", \"\", \"W12 drop injur\"), (CF, \"motor\\\\s+vehicle|\", \"\", \"W13 drop motor vehicle\"),\n (CF, \"struck|\", \"\", \"W14 drop struck\"), (CF, \"hit\\\\s+by|\", \"\", \"W15 drop hit by\"),\n (CC, \"if lang != \\\"en\\\":\", \"if lang not in ('en', 'uncertain'):\", \"C7 uncertain counted as read\"),\n (CC, \"        if run is None:\\n            skip(t, \\\"NOT_RUN\\\"\", \"        if False:\\n            skip(t, \\\"NOT_RUN\\\"\", \"C9 no summary claims ran\"),\n (CC, \"note = conflicts.accident_date_note(records) if records is not None and \\\"accident_date\\\" not in whole else None\", \"note = None\", \"C10 notes never\"),\n (CC, \"dated = sum(1 for r in records if r.get(\\\"date_iso\\\")) if records is not None else None\", \"dated = None\", \"C11 dated count never\"),\n (PR, \"else \\\"complete\\\"), store.load_records(conn, case_id, raw)),\", \"else \\\"complete\\\"), None),\", \"R2 present passes no records (notes stale/none)\"),\n (PLN, \"    _store_run_checks(conn, cid, recs, \\\"pending\\\")           #\", \"    pass           #\", \"P2 no pending at run start\"),\n (PLN, \"    _store_run_checks(conn, cid, ing[\\\"records\\\"], \\\"pending\\\")\\n\", \"\", \"P3 no summary at ingest\"),\n]\ntests = [\"tests/unit/test_conflicts.py\", \"tests/unit/test_conflict_candidates.py\", \"tests/unit/test_t141_checks_per_case.py\", \"tests/unit/test_t141_r3_variants.py\", \"tests/unit/test_t116_r4_all_dated_records.py\", \"tests/unit/test_api_routes.py\", \"tests/unit/test_t093_j3_controls_reachable.py\"]\nk=s=0\nfor rel, old, new, label in muts:\n    p = root / rel; src = p.read_text()\n    if old not in src: print(\"SKIP (pattern not found)\", label); continue\n    p.write_text(src.replace(old, new, 1))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", *tests, \"-q\", \"-x\", \"-p\", \"no:cacheprovider\"], cwd=root, capture_output=True, text=True)\n    p.write_text(src)\n    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]\n    if r.returncode: k+=1\n    else: s+=1\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), label, \"|\", tail[:90], flush=True)\nprint(\"killed\", k, \"survived\", s)\nEOF\ncd $SP/T141r3_scripts && /Users/arsis/zlayt-pm-project/.venv/bin/python -I r3_mutate.py $SP/T141r3_mut 2>&1 | tail -45",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T14:22:29.189Z

**tool result**
````
KILLED   M1 month-year history off | 1 failed, 135 passed in 2.62s
KILLED   M2 full-date >1y history off (r2 N6/N18) | 1 failed, 152 passed in 1.45s
KILLED   M2b >365 -> never | 1 failed, 152 passed in 1.51s
KILLED   M3 bare earlier year never history | 1 failed, 6 passed in 0.38s
KILLED   M3b no Jan/Feb leniency | 1 failed, 206 passed in 1.64s
KILLED   M4 last year/years ago off | 1 failed, 134 passed in 1.44s
KILLED   M5 negation off | 1 failed, 146 passed in 1.43s
KILLED   M6 history-word off | 1 failed, 10 passed in 0.50s
KILLED   M7 'prior to' counts as history | 1 failed, 205 passed in 1.48s
KILLED   M8 'previously had' adverb off | 1 failed, 204 passed in 1.54s
KILLED   W1 drop t-bone | 1 failed, 164 passed in 1.48s
KILLED   W2 drop sideswipe | 1 failed, 165 passed in 1.54s
KILLED   W3 drop run over | 1 failed, 166 passed in 1.62s
KILLED   W4 drop airbag | 1 failed, 168 passed in 1.44s
KILLED   W5 drop seatbelt | 1 failed, 169 passed in 1.45s
KILLED   W6 drop pedestrian | 1 failed, 132 passed in 1.52s
KILLED   W7 drop incident | 1 failed, 180 passed in 1.77s
KILLED   W8 drop whiplash | 1 failed, 184 passed in 1.66s
KILLED   W9 drop trauma | 1 failed, 186 passed in 1.66s
KILLED   W10 drop impact | 1 failed, 187 passed in 1.49s
KILLED   W11 drop LOC | 1 failed, 188 passed in 1.40s
KILLED   W12 drop injur | 1 failed, 185 passed in 1.47s
KILLED   W13 drop motor vehicle | 1 failed, 175 passed in 1.38s
KILLED   W14 drop struck | 1 failed, 141 passed in 1.42s
KILLED   W15 drop hit by | 1 failed, 154 passed in 1.44s
KILLED   C7 uncertain counted as read | 1 failed, 113 passed in 0.77s
KILLED   C9 no summary claims ran | 1 failed, 110 passed in 0.76s
KILLED   C10 notes never | 1 failed, 112 passed in 0.84s
KILLED   C11 dated count never | 1 failed, 111 passed in 0.77s
SKIP (pattern not found) R2 present passes no records (notes stale/none)
KILLED   P2 no pending at run start | 1 failed, 124 passed in 1.36s
KILLED   P3 no summary at ingest | 1 failed, 115 passed in 0.89s
killed 31 survived 0
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:22:34.923Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP/T141r3_mut; diff -rq . ../T141r3_head | head; cp app/backend/present.py /tmp/x 2>/dev/null; python3 - <<'EOF'\nimport pathlib\np=pathlib.Path(\"app/backend/present.py\"); s=p.read_text()\nold='\"complete\", store.load_records(conn, case_id, raw)), \"tray\"'\nprint(old in s)\np.write_text(s.replace(old,'\"complete\", None), \"tray\"',1))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_t141_checks_per_case.py tests/unit/test_api_routes.py tests/unit/test_conflicts.py 2>&1 | tail -4; cp ../T141r3_head/app/backend/present.py app/backend/present.py; diff -rq . ../T141r3_head | head -3; rm -f /tmp/x"
}
````

### User / tool · 2026-11-02T14:22:42.627Z

**tool result (error)**
````
Exit code 1
Files ./app/__pycache__/__init__.cpython-312.pyc and ../T141r3_head/app/__pycache__/__init__.cpython-312.pyc differ
Files ./app/backend/__pycache__/__init__.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/__init__.cpython-312.pyc differ
Files ./app/backend/__pycache__/amounts.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/amounts.cpython-312.pyc differ
Files ./app/backend/__pycache__/api.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/api.cpython-312.pyc differ
Only in ../T141r3_head/app/backend/__pycache__: billing.cpython-312.pyc
Only in ../T141r3_head/app/backend/__pycache__: calibration_route.cpython-312.pyc
Files ./app/backend/__pycache__/case_extras.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/case_extras.cpython-312.pyc differ
Files ./app/backend/__pycache__/case_list.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/case_list.cpython-312.pyc differ
Files ./app/backend/__pycache__/charge_text.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/charge_text.cpython-312.pyc differ
Files ./app/backend/__pycache__/confidence.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/confidence.cpython-312.pyc differ
True
FAILED tests/unit/test_t141_checks_per_case.py::test_lib11_no_false_accident_date_conflict_and_the_predate_note_counts_the_annual_visit
FAILED tests/unit/test_t141_checks_per_case.py::test_confirming_a_date_refreshes_the_note_and_the_flag_together
FAILED tests/unit/test_t141_checks_per_case.py::test_a_case_whose_only_dated_record_was_ambiguous_lists_accident_date_after_confirming_it
3 failed, 57 passed in 6.87s
Files ./app/__pycache__/__init__.cpython-312.pyc and ../T141r3_head/app/__pycache__/__init__.cpython-312.pyc differ
Files ./app/backend/__pycache__/__init__.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/__init__.cpython-312.pyc differ
Files ./app/backend/__pycache__/amounts.cpython-312.pyc and ../T141r3_head/app/backend/__pycache__/amounts.cpython-312.pyc differ
rm: /tmp/x: is a directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:22:47.198Z

**tool call — Bash**
````
{
 "command": "ls -la /tmp/x | head; SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $SP; diff -rq -x __pycache__ -x .pytest_cache T141r3_mut T141r3_head && echo mut-archive-restored"
}
````

### User / tool · 2026-11-02T14:22:47.439Z

**tool result**
````
total 2864
drwxr-xr-x@  16 arsis  wheel     512 Nov  2 08:22 .
drwxrwxrwt  467 root   wheel   14944 Nov  2 08:22 ..
-rw-r--r--@   1 arsis  wheel     187 Nov  2 04:08 41e42a2978854c340fcf3f43360478c22289d982857f3abc73377b804535ad59.json
-rw-r--r--@   1 arsis  wheel     239 Nov  1 22:40 S
-rw-r--r--@   1 arsis  wheel  179021 Nov  2 04:30 a.png
-rw-r--r--@   1 arsis  wheel  217268 Nov  2 04:28 b.png
-rw-r--r--@   1 arsis  wheel  202832 Nov  2 04:32 c.png
-rw-r--r--@   1 arsis  wheel    5617 Nov  2 07:34 case_list.py
-rw-r--r--@   1 arsis  wheel  151037 Nov  2 04:42 f.png
mut-archive-restored
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:22:49.073Z

**tool call — Bash**
````
{
 "command": "ls -la /tmp/x/present.py && rm /tmp/x/present.py; ls /tmp/x | wc -l"
}
````

### User / tool · 2026-11-02T14:22:49.181Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  25648 Nov  2 08:22 /tmp/x/present.py
      13
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:22:54.059Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=$SP/T141r3_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141; sed -n 1,12p r2_lib11.py; $PY -I r2_lib11.py $A 2>&1 | tail -8; sed -n 1,25p diff_packets.py | head -30"
}
````

### User / tool · 2026-11-02T14:22:54.844Z

**tool result**
````
import sys, pathlib, tempfile
root = sys.argv[1]; sys.path.insert(0, root)
from app.backend import pipeline as PL, present
tmp = pathlib.Path(tempfile.mkdtemp(prefix="t141r2l_"))
text = (pathlib.Path(root) / "evals/library/case_lib11_priors_and_ledger.txt").read_text()
with PL._Backend("fixture"):
    conn, cid, call = PL._scratch_call(str(tmp), PL.IN.normalize_text(text)); PL.run_pipeline(conn, cid, text, call=call)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
for f in v["flags"]:
    if f["type"] == "conflict": print("CONFLICT", f["category"], f["state"], "|", f["title"][:90], "| records", f.get("record_nos"))
print("accident-date flags:", [f["category"] for f in v["flags"] if str(f.get("category")).startswith("accident_date")])
ch = v["checks"]; print("checks types:", ch["conflict_types"], "skipped:", ch["skipped"], "notes:", [n["text"] for n in ch["notes"]])
CONFLICT other_fact_mismatch verified | Records differ on a fact | records None
CONFLICT other_fact_mismatch verified | Records differ on a fact | records None
accident-date flags: []
checks types: ['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped: [] notes: ['1 record predates the stated accident date, March 18, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.']
import sys, json, pathlib
root = sys.argv[1]; sys.path.insert(0, root)
from evals import j3_controls as J
from app.backend import conflict_candidates as CC, conflicts as C
out = {}
for p in J.packet_paths():
    try:
        recs = J.packet_records(p)
    except Exception as e:
        out[p.name] = f"ERR {e}"; continue
    cands = sorted((c["rule"], c["a"].record_no, c["a"].text, c["b"].record_no, c["b"].text) for c in CC.candidates(recs))
    out[p.name] = dict(cands=cands, acc=[(o["category"], o["stated_dates"]) for o in C.accident_date_conflicts(recs)])
print(json.dumps(out, sort_keys=True, indent=1, default=str))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:00.630Z

**tool call — Bash**
````
{
 "command": "SP=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cd /Users/arsis/zlayt-pm-project; mkdir -p $SP/T141r3_r2 && git archive 68b8685 | tar -x -C $SP/T141r3_r2; cd artifacts/review-evidence/T-141; $PY -I diff_packets.py $SP/T141r3_head > $SP/T141r3_scripts/p_head.json; $PY -I diff_packets.py $SP/T141r3_r2 > $SP/T141r3_scripts/p_r2.json; diff $SP/T141r3_scripts/p_r2.json $SP/T141r3_scripts/p_head.json && echo IDENTICAL; grep -c '\"acc\"' $SP/T141r3_scripts/p_head.json; grep -n \"2026-01-19\" $SP/T141r3_scripts/p_head.json | head -3; cd /Users/arsis/zlayt-pm-project; git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T14:23:01.667Z

**tool result**
````
IDENTICAL
27
151:     "2026-01-19"
25f585cfd99e910ca6555c773ae7afded2f0238c
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:03.914Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; git log --oneline ad8b7d1..HEAD; git diff --stat ad8b7d1 HEAD -- app/backend/conflicts.py app/backend/conflict_candidates.py app/backend/present.py tests/unit/test_conflicts.py tests/unit/test_t141_r3_variants.py tests/unit/test_t141_checks_per_case.py | tail -3; grep -n \"r3_variants\\|negat\" tests/unit/test_t141_r3_variants.py | head -20"
}
````

### User / tool · 2026-11-02T14:23:04.039Z

**tool result**
````
25f585c fix(frontend): T-136 r3 e2e private server that fails to start stops the run with its log; never falls back to :7860
b5f40c0 fix(frontend): T-151 empty checks.conflict_types says 'No conflict checks ran for this case' with the skipped reasons, never an empty list or 'No conflicts found'
4abec86 fix(backend): T-139 r2 money written without a dollar sign (TOTAL CHARGE 49100, AMOUNT PAID 0 00, 24F, FL47) is held out and caught by an independent letter check; Bills to request lists treating providers only; the held-out hint offers only actions that clear it
e2bb025 test(frontend): declare data-entry-id and data-flag in the e2e hook contract (T-144, T-154)
611bdcc feat(frontend): T-154 charges are never batch-accepted (note + CHARGES_NOT_BATCHED message); a flagged charge shows its flag and accepts only through a named confirm
f262223 fix(frontend): T-144 the uncovered list opens from a short link in the entry head so compact rows keep their height
2:when every such clause is negated or plainly history. Any other record is a date conflict (a safe false positive beats a hidden conflict). The reviewer's
30:    ("V14 fall risk screen", "info", STD("Annual physical. Fall risk screen negative. Flu shot given in the fall.")),
32:    ("V16 struck by a car after a negated clause", "conflict", STD("No prior neck problems, was struck by a car while crossing the street. Neck pain.", "ER")),
84:def test_history_and_negated_wording_is_an_earlier_visit(sentence):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:23:54.441Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r3.md",
 "content": "# T-141 staff-engineer review, round 3 (ad8b7d1), Marcus Lee persona\n\nVerdict: **changes** (0 blockers, 1 major, 2 nits). The read-time notes, the no-summary rule and the mutant kills are all fixed and verified. The worker's deviation is the problem: \"negated or plainly history stays info-only\" is implemented as a bag-of-words window, and the window hides true date conflicts. 10 of my 33 fresh variants are real earlier-collision descriptions that come back info-only, and the note then says \"No record names a collision, crash, accident, injury or similar in words of its own\", which is false for each.\n\nMethod: all probes ran on `git archive ad8b7d1` copies in the scratchpad (T141r3_head, T141r3_mut for mutants), not the dirty working tree. HEAD moved to 25f585c during the review (frontend and T-139 commits); `git diff --stat ad8b7d1 HEAD` over conflicts.py, conflict_candidates.py, present.py and the T-141 test files is empty, so ad8b7d1 is the T-141 state.\n\n## Answers to the brief\n\n1. **Does the deviation hide a true date conflict? Yes.** Scripts: `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r3_scripts/r3_variants.py` (33 fresh variants). Each case is one record dated 2026-01-05, a PT visit 2026-01-12 and an intake \"Date of accident per intake form: 2026-01-09\".\n   - Correct as the worker intended: `No prior accidents.`, `Denies MVC.`, `MVA in 2015, resolved.`, `History of MVA 2015.`, `Hx rear-end collision 2018.`, `MVA remote past`, `Fall risk screen negative.` all info-only. lib11 still has no date conflict.\n   - Hidden true conflicts (info-only, should conflict): T1 `No LOC after the accident.`; T2 `Has not worked since the accident.`; T5 `No improvement since the crash.`; T6 `No airbag deployment in the collision.`; T7 `Without fracture after the MVC.`; T8 `Never lost consciousness during the crash.`; T10 `Negative for fracture after rear-end collision.`; H1 `History: rear-ended at a stoplight.`; H6 `Old man hit by a car crossing the street.`; H7 `Neck pain started years ago and worsened after the rear-end collision.` Cause: conflicts.py `_is_event_word` negates any event word with a negator in the five words before it, whatever sits between (\"after\", \"since\", \"during\", \"in\"); `_HIST_WORD` (\"history\", \"old\", \"past\") within three words counts as history even as a section label (\"History:\"); `_CLAUSE_HISTORY` makes the whole clause history when \"years ago\" appears anywhere in it.\n   - Still conflict, correctly: T3, T4, T9, H2-H5, H8-H10, Y2, and all reviewer r2 variants V1-V3, V5-V8, V11, V16-V19, W3-W5, W9 (r2 variants rerun: 1 mismatch, V4, which is the intake-form self-contradiction I called right in round 2). Round-1 A-L: unchanged, B-H conflict, A, J, K, L quiet, I conflicts.\n   - Safe-direction false positives (conflict where info is better): `Denies any motor vehicle collision or injury.` (the word \"injury\" is six words from \"denies\") and `Impact of diabetes on diet counselled.` The brief prefers these to hidden conflicts, so nit only.\n2. **Notes at read time, refresh after confirm_date: fixed.** `r2_stale_checks.py` on the archive: ingested shows the predates note and no flag; after `review.confirm_date(.., '2026-03-06')` notes `[]` and flag `accident_date_after_treatment`. The note and the NO_DATED_RECORD count are computed in `checks(..., records)` from `store.load_records` (present.py case_view).\n3. **No stored summary: fixed.** `r2_checks_matrix.py`: S5 (legacy ready) and S5b (legacy failed) report `ran=[]`, all four types skipped NOT_RUN, notes `[]`. A failed legacy case says NOT_RUN rather than RUN_FAILED; the reason text is honest about it.\n   Other matrix rows are unchanged from round 2: ingested only, deadline at each stage, re-run in flight, lib09 partial Spanish (records 2, 4, 7), all-Spanish, crashed re-run RUN_FAILED (`r2_real_crash.py`).\n4. **Mutants.** `r3_mutate.py` (32 mutants over conflicts.py, conflict_candidates.py, present.py, pipeline.py, with the r2 survivors): 31 of 31 applied mutants killed, 0 survived, plus the present.py \"no records passed\" mutant applied by hand (3 failed). The r2 survivors N6/N18 (old full date), P2 (run-start pending), P3, C7 (uncertain) and the word members t-bone, sideswipe, run over, airbag, seatbelt and 'vehicle'/'hit' replacements are all red now. Archive restored and diffed against the head copy (source files identical).\n5. **Suites.** `tests/unit/test_conflicts.py test_conflict_candidates.py test_t093_j3_controls_reachable.py test_t141_checks_per_case.py test_t141_r3_variants.py test_t116_r4_all_dated_records.py test_api_routes.py` on the ad8b7d1 archive: 291 passed. 27-packet differential (`diff_packets.py`) between 68b8685 and ad8b7d1: identical, 27 accident-date result sets, sample still raises accident_date_after_treatment (2026-01-19). lib11 case view after a fixture run: two denial conflicts, no accident-date flag, note present.\n\n```json\n{\n \"card\": \"T-141\",\n \"persona\": \"staff-engineer-reviewer\",\n \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git ad8b7d1 (T-141 round 3, final) vs 68b8685; probes on git archives of ad8b7d1 and 68b8685 in the scratchpad (T141r3_head, T141r3_mut, T141r3_r2), never the dirty working tree; HEAD moved to 25f585c mid-review with no change to the T-141 files; fixture backend, no server started\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md, reviews/T-141-staff-engineer-r2.md, `python3 tools/board.py show T-141` (round-3 note, handoff), `git show ad8b7d1` for conflicts.py, conflict_candidates.py, present.py; `git rev-parse HEAD` = ad8b7d1 at start, 25f585c at end; `git diff --stat ad8b7d1 HEAD` over the T-141 files empty\",\n  \"git archive ad8b7d1 into T141r3_head and T141r3_mut; git archive 68b8685 into T141r3_r2\",\n  \"Reviewer r2 variants V1-V20 (r2_variants.py) and W1-W10 (r2_variants2.py) and round-1 A-L (probe2.py) on the r3 archive\",\n  \"33 fresh variants (scratchpad T141r3_scripts/r3_variants.py): negations (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury), historical (MVA in 2015, History of MVA 2015, Hx rear-end collision 2018), negator-before-true-collision (T1-T10), history-word-before-true-collision (H1-H11), bare year and month-year (Y1-Y3), benign (B1-B3); r3_note.py for the note text on a hidden case\",\n  \"Read-time notes: r2_stale_checks.py (ingest then review.confirm_date); checks matrix r2_checks_matrix.py (ingested, complete, deadline at each stage, re-run in flight, legacy rows with no run_checks, lib09, lib11, all-Spanish, defaults); r2_real_crash.py (crash in the conflict stage of a re-run)\",\n  \"27-packet differential diff_packets.py 68b8685 vs ad8b7d1 (identical, sample accident-date conflict kept); r2_lib11.py case view after a fixture run\",\n  \"Mutation: r3_mutate.py, 31 mutants on T141r3_mut (all killed), plus a manual present.py mutant (records not passed, 3 tests failed); archive diffed against T141r3_head after (source identical)\",\n  \"pytest on the ad8b7d1 archive: 7 conflict and checks modules, 291 passed\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\n  \"determinism\": 5,\n  \"honest_failure\": 4,\n  \"tests_assert_behaviour\": 3,\n  \"llm_code_boundary\": 5,\n  \"controls_discipline\": 4\n },\n \"findings\": [\n  {\n   \"severity\": \"major\",\n   \"title\": \"Negated-or-history exemption hides true accident-date conflicts: 10 of 33 fresh variants where an earlier record describes the collision come back info-only, and the note says no record names a collision or injury\",\n   \"evidence\": \"app/backend/conflicts.py `_is_event_word` (negator anywhere in the 5 words before the event word negates it, so prepositions between them do not stop it; `_HIST_WORD` includes 'history', 'old', 'past' within 3 words before, so a 'History:' label counts), `_CLAUSE_HISTORY` ('years ago' anywhere in the clause makes the whole clause history), `_describes_event` (all event words must fail). Repro on a git archive of ad8b7d1: `.venv/bin/python -I <scratchpad>/T141r3_scripts/r3_variants.py <archive>`; info-only but a real collision: T1 'No LOC after the accident.'; T2 'Has not worked since the accident.'; T5 'No improvement since the crash.'; T6 'No airbag deployment in the collision.'; T7 'Without fracture after the MVC.'; T8 'Never lost consciousness during the crash.'; T10 'Negative for fracture after rear-end collision.'; H1 'History: rear-ended at a stoplight.'; H6 'Old man hit by a car crossing the street.'; H7 'Neck pain started years ago and worsened after the rear-end collision.' (each as the only mention in a record dated 2026-01-05 with the stated accident date 2026-01-09; `accident_date_conflicts` returns [] and `accident_date_note` text reads: '1 record predates the stated accident date, January 9, 2026. No record names a collision, crash, accident, injury or similar in words of its own, so no date conflict is raised; read them to check they are earlier care.', r3_note.py). Correctly still conflict: T3, T4, T9, H2-H5, H8-H10, Y2. 'No LOC after the accident' and 'has not worked since the accident' are among the commonest ER and follow-up phrasings, so this is not contrived.\",\n   \"why_it_matters\": \"This is the same lost-conflict class as round-1 major 1 and round-2 major 1 (a deterministic R-FL-2 check becomes a word guess and a true discrepancy between the stated accident date and an earlier record disappears), now moved from 'wording the list misses' to 'wording the exemption over-reaches on'. The worker's reading of the Round 3 note (keep history and negation info-only so lib11 stays closed) is defensible, but the implementation negates the whole event instead of the noun the negator governs, and the note text then asserts the opposite of what the record says. Not a blocker for the same reason as rounds 1 and 2: it needs a stated accident date later than the earliest record plus one of these wordings, the record count is still surfaced as a note, and the loss is limited to the date-conflict flag, not an entry or a total.\",\n   \"fix\": \"Scope the exemptions to the phrase they govern. (a) Negation: a negator only negates an event word when nothing but determiners, adjectives and event-noun modifiers sit between them ('no prior accidents', 'denies any motor vehicle collision', 'no recent injuries'); any of after, since, during, in, following, from, at, with, when, while, because, of between the two ends the scope. (b) History: 'history', 'hx', 'prior', 'previous', 'remote', 'old' count only immediately before the event noun or 'of <event>' ('prior accident', 'history of MVA', 'old MVC'), never when the word ends a label ('History:', 'History of present illness') or is followed by 'to'. (c) 'years ago', 'last year', 'as a child' make history only the sub-clause they sit in, split on 'and', 'but', 'worse', 'worsened', 'since', 'after'. (d) Reword the note so it says what was looked for and does not assert absence of injury: 'Records predate the stated accident date; none was read as describing a collision, so no date conflict is raised. Read them.'\",\n   \"acceptance_test\": \"tests/unit/test_t141_r3_variants.py: T1, T2, T5, T6, T7, T8, T10, H1, H6, H7 each return one accident_date_after_treatment conflict; the info-only set (No prior accidents, Denies MVC, Denies any motor vehicle collision or injury, MVA in 2015, History of MVA 2015, Hx rear-end collision 2018, Fall risk screen negative) and the lib11 shape still return []; mutants that widen the negator window back to 5 words regardless of prepositions are killed.\"\n  },\n  {\n   \"severity\": \"nit\",\n   \"title\": \"Two safe-direction false positives: 'Denies any motor vehicle collision or injury' and 'Impact of diabetes on diet' still raise a date conflict\",\n   \"evidence\": \"r3_variants.py N3 (conflict; 'injury' sits six words after 'denies', outside the 5-word window) and B2 (conflict; bare 'impact\\\\w*' in conflicts.py `_EVENT`). The paralegal can dismiss the conflict; nothing is lost.\",\n   \"why_it_matters\": \"The Round 3 direction prefers a false positive to a hidden conflict, so this is not a defect. It does show the negation window is by word count, which is the cause of the major finding in the other direction.\",\n   \"fix\": \"Fixing the major finding's negation scope (adjective list, not a word count) also closes N3; restrict 'impact' to 'impact with/of the collision' or 'on impact'.\",\n   \"acceptance_test\": \"N3 returns [] and B2 returns [] in test_t141_r3_variants.py after the scope change.\"\n  },\n  {\n   \"severity\": \"nit\",\n   \"title\": \"A bare year earlier than the record's own year always counts as history, so 'Rear-ended in 2025' in a record dated mid-2026 is info-only\",\n   \"evidence\": \"conflicts.py `_clause_is_history` last line `int(y) < ry - (0 if rm > 2 else 1)`; r3_variants.py Y1 (record 2026-06-05 'Intake. Rear-ended in 2025.', stated 2026-06-09): info-only. Y3 'Rear-ended in October 2025' in a 2026-01-05 record is also info-only (three months, outside the two-month month-year window). Both are ambiguous rather than clearly wrong; lib11's '2019 and 2022' needs the rule.\",\n   \"why_it_matters\": \"A bare year says nothing about whether the event is the index accident; within the last ~15 months it could be. Low likelihood, and the brief set the threshold as 'plainly history'.\",\n   \"fix\": \"Treat a bare year as history only when it is at least two calendar years before the record's year, or when the clause also has a history marker.\",\n   \"acceptance_test\": \"Y1 and Y3 conflict; lib11 (2019, 2022) and 'MVA in 2015' stay info-only.\"\n  }\n ],\n \"whats_right\": [\n  \"Notes and the dated-record count are computed from the current records at GET time; confirm_date now moves the flag and the note together, and the stored run summary keeps only language, read count and stage.\",\n  \"A case with no stored summary reports all four checks as NOT_RUN with an honest reason and conflict_types [], and the matrix (deadline at each stage, crashed re-run, partial and all-Spanish) still never claims a check that did not run.\",\n  \"Mutant discipline: 31 of 31 mutants killed including every round-2 survivor (old full date, run-start pending, uncertain language, individual word-list members), and the 27-packet differential is identical to 68b8685 with the sample conflict kept.\"\n ],\n \"questions_for_chris\": []\n}\n```\n"
}
````

### User / tool · 2026-11-02T14:23:54.589Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:01.575Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -3; cat > .claude/agent-memory/staff-engineer-reviewer/project_t141_r3_patterns.md <<'EOF'\n---\nname: project_t141_r3_patterns\ndescription: T-141 r3 ad8b7d1 changes — negator/history windows by word count hide true collisions (No LOC after the accident, History: rear-ended); read-time notes and no-summary fixed, 31/31 mutants killed\nmetadata:\n  type: project\n---\n\nT-141 r3 (ad8b7d1, verdict changes, 1 major 2 nits). Notes computed at read time, no-summary = NOT_RUN, r2 survivors all killed, 27-packet diff identical.\n\n- Open class: _is_event_word negates on a negator within 5 words before (prepositions after/since/during do not stop it) and counts \"History:\" / \"old\" / \"past\" within 3 words as history; \"years ago\" anywhere makes the whole clause history. 10 of 33 fresh variants hid a true collision. Note text asserted \"no record names a collision/injury\" (false).\n- Method that worked: probe sets of \"negator + preposition + event noun\" (No LOC after the accident, has not worked since the accident, without fracture after the MVC) and \"section label + event\" (History: rear-ended). Always test the scope of a negation/history word, not only its presence.\n- Mutants: write mutants against the NEW code (old patterns SKIP); a missing pattern prints SKIP, apply by hand.\n- Stray write hazard: `cp file /tmp/x` when /tmp/x is an existing dir copies into it; use scratchpad paths only.\n- HEAD moved mid-review: confirm with `git diff --stat <sha> HEAD -- <files>` that the card's files are unchanged.\n\n**How to apply:** for word-window rules ask whether the window crosses a preposition/verb; probe both directions (hidden and false positives).\nEOF\necho \"- [T-141 r3 patterns](project_t141_r3_patterns.md) — ad8b7d1 changes: negator/history word windows hide true collisions, read-time notes fixed, 31/31 mutants killed\" >> .claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T14:24:01.742Z

**tool result**
````
ok (155 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:24:04.058Z

Verdict is **changes**: 1 major, 0 blockers, 2 nits. The worker's "negated or historical stays info-only" rule hides true date conflicts. 10 of my 33 fresh variants (for example "No LOC after the accident", "Has not worked since the accident", "History: rear-ended at a stoplight") come back info-only. The note then wrongly says no record names a collision or injury.
Read-time notes after `confirm_date`, NOT_RUN for a case with no stored summary, and the named mutants are all fixed: 31 of 31 killed. The 291 conflict-suite tests pass and the 27-packet differential matches the previous round. Review: `/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r3.md`
