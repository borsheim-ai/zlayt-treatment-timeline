# Subagent: T-141 r2 staff review (T-141 r2 staff review)

Source: `agent-a673b51d9992db19d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T13:44:13.007Z

This is the round-2 review of board card T-141 (commit 68b8685) in /Users/arsis/zlayt-pm-project. Read reviews/T-141-staff-engineer.md and `python3 tools/board.py show T-141`, including the direction note and the handoff.

On a `git archive HEAD` copy:
- **Accident-date variants.** Re-run your 6 accident-date variants. A pre-accident record with collision or mechanism wording must still conflict, and one without it must be info-only. Write at least 10 fresh variants, including billing and intake records dated before the accident.
- **checks.** `checks` must be per case and come from the stored run summary, with `skipped[]` reasons covering Spanish, deadline, failed and not-yet-run. Check that it never claims a rule ran when it did not.
- **lib11.** Still correct: two denial conflicts, and no false date conflict.
- **Changed test.** The worker changed one existing test, test_t116_r4_all_dated_records.py. Was that the right call?
- **Tests.** Run the conflict suites and mutate the code to test the tests. The 12 unit failures in T-139 charge_text and export golden belong to other work in flight; note them only.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-141-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings, exercised. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:17.870Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T13:44:17.878Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:18.190Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer.md"
}
````

### User / tool · 2026-11-02T13:44:18.200Z

**tool result**
````
1	# T-141 staff-engineer review (c4bb4da), Marcus Lee persona, with the paralegal view
2	
3	Verdict: **changes** (0 blockers, 2 major, 3 minor, 1 nit). The target works: on lib11 (fixture backend, ZLAYT_MODE=local) the app shows two conflict cards, "Prior accidents? Yes [ ] No [X]." and "Prior injuries? Yes [ ] No IX]." against the PCP's "car accidents in 2019 and 2022", and no accident-date conflict. All 3600 unit tests pass on the commit archive. The two majors are about what the new code can hide: the accident-date skip can drop a true date conflict (five of six plausible variants), and the new `checks` field says the same thing on every case, including Spanish cases where the pair rules cannot fire.
4	
5	## Answers to the five questions
6	1. **Intake denials.** 25 pairs, pre vs HEAD. New and correct: checked No [X], OCR No IX], reversed box order, "Prior accidents: No.", "Prior injuries: None." pair with accident sentences; Yes checked, both boxes empty, both boxes checked, a bare question, an accident in the denial's own year, a husband's or other driver's accident do not pair. Wrong pairs (minor finding 3): a topic-free stem ("Previous employer: None.", "Prior authorization ... No [X]", "Previous visits to this clinic: None.") pairs with any prior-condition sentence; a negated history ("No car accidents in 2019 or 2022") counts as a prior event; a scoped question ("in the last year") pairs with a 2019 accident. "No prior accidents since 2010" vs a 2005 accident pairs on both builds (inherited from T-094). The roommate pair reaches the judge on purpose (J3V20). One live J3 run rejected every wrong pair I tried and confirmed the lib11 pair, so the judge held; no control covers these shapes.
7	2. **Accident-date skip.** It can hide a true conflict (major finding 1): five variants flagged before the commit return nothing now.
8	3. **Controls.** Labels were fixed in the same commit, before any run, with a rationale per row and a locked table in the test; the reachability test passes. The live 3x run is not required to accept this card (AC 1 does not ask for it and "controls unaffected" is verified by the 27-packet diff), but it is required before the M2 gate (D-046) and nobody owns it (minor finding 4).
9	4. **lib11 expected.** Three additive edits, each with a written reason: C1 summary suffix (nit), N2 must_not (false accident-date conflict; red on the old code, green on HEAD), T1 tolerated (second form field against the problem-list sentence). Nothing was loosened.
10	5. **checks.conflict_types.** Present and correct for English; the four types match the code paths and the not_checked list is honest about what is absent. It is a constant, so it overclaims for Spanish and skipped stages (major finding 2).
11	
12	## Paralegal view (lib11 in the app, Maria's reading)
13	- The conflict is easy to see: "Conflicts between records (2)" with each card quoting the intake form line with the answer ("Prior accidents? Yes [ ] No [X].") next to the PCP line, record numbers and dates, "Open records 6 and 1". No "records disagree" accident-date card, no "No conflicts found" text.
14	- The OCR quote "No IX]" is shown as scanned; a paralegal can read it, but it is the one line that asks for a second look.
15	- Two cards cite the same PCP sentence, and two label-only "mentions a prior or pre-existing condition: Prior accidents?" flags remain (minor finding 6).
16	- The `checks` list is not shown in the UI yet (T-142 in progress), so the empty-state wording was not testable here.
17	- Still wrong on lib11 and outside this card: the ledger total and balance due count as charges (M1 in the library report); not counted against T-141.
18	
19	Server stopped by PID 82002. Evidence and scripts: `artifacts/review-evidence/T-141/`.
20	
21	```json
22	{
23	 "card": "T-141",
24	 "persona": "staff-engineer-reviewer",
25	 "model": "claude-sonnet-5-5",
26	 "scope": "git c4bb4da (and c4bb4da~1 for differential); app from a git archive copy, http://127.0.0.1:7921 (PID 82002, stopped), fixture backend, ZLAYT_MODE=local; lib11 (evals/library/case_lib11_priors_and_ledger.txt) as the paralegal view; sample case not exercised in the UI",
27	 "exercised": [
28	  "Read personas/staff-engineer.md, reviews/GATE-M2-paralegal.md, `python3 tools/board.py show T-141`, D-046/D-053/D-057 in memory/ORCHESTRATOR_DECISIONS.md, git show c4bb4da in full (conflict_candidates.py, conflicts.py, j3_controls.py, judge_controls.jsonl, expected.json, tests)",
29	  "git archive c4bb4da and c4bb4da~1 into separate scratchpad directories (T141_head, T141_pre); all probes ran on those, never on the working tree",
30	  "Conflict suites on the HEAD archive: pytest tests/unit/test_conflict_candidates.py test_conflicts.py test_t093_j3_controls_reachable.py -> 116 passed; full pytest tests/unit -> 3600 passed, 8 skipped, 0 failed (the unit failures the brief mentions are from the dirty working tree, not the commit)",
31	  "25 intake/history candidate probes on both archives (probe1.py), 12 accident-date scenarios on both archives (probe2.py), Spanish probe (probe3.py), candidates + accident-date diff over all 27 golden and library packets pre vs HEAD (diff_packets.py: only lib11 changes)",
32	  "11 mutants on a scratch copy (mutate.py): 9 killed; survivors M4 (guard in _earlier_year_accident, covered by callers) and M9 (len(distinct)<2 inside the skip, equivalent because two distinct dates take the other branch)",
33	  "evals.library_report on c4bb4da~1, c4bb4da, and c4bb4da~1 with the new expected file: lib11 must flags 3/4 -> 4/4; must_not_flag hits for the new N2: 1 on the old code, 0 on HEAD (N2 discriminates); remaining M1 hit (ledger charges) is the separate GATE-M2 blocker",
34	  "Live J3 (claude-cli, ENABLE_LIVE=1, one run each, exploratory): 6 false pairs benign, real lib11 pair conflict (live_j3.py)",
35	  "App from the HEAD archive: fixture backend, ZLAYT_MODE=local, ZLAYT_DB in the scratchpad, port 7921, listener PID 82002 verified by lsof and ps before kill; stopped by PID (lsof empty, curl 000); port 7860 (PID 66274) untouched. Loaded lib11 from the synthetic library by Playwright (ui_lib11.py), read the full page text, screenshotted the conflict cards, fetched GET case JSON (case.json), POSTed the Spanish library packet and read its checks",
36	  "Read memory/contracts/api.md:133 and checked checks.conflict_types, labels and not_checked against code; checked the latest controls report for the new ids"
37	 ],
38	 "verdict": "changes",
39	 "scores": {
40	  "determinism": 5,
41	  "honest_failure": 3,
42	  "tests_assert_behaviour": 4,
43	  "llm_code_boundary": 4,
44	  "controls_discipline": 4
45	 },
46	 "findings": [
47	  {
48	   "severity": "major",
49	   "title": "Accident-date corroboration skip silently drops a true date conflict when the earliest record words the collision in a way its word list misses",
50	   "evidence": "app/backend/conflicts.py:14-15 (_EVENT, _HISTORICAL), :19-28 (_describes_event: a sentence counts only if it has no prior/history word and no 4-digit year earlier than the stated year), :31-36 (_corroborated), :76 (later = ...). Repro on a git archive of c4bb4da: `.venv/bin/python -I artifacts/review-evidence/T-141/probe2.py <archive>` (same script on c4bb4da~1 flags all of them). Each case is ER on the collision date, a PT follow-up on the date the intake states, intake 'Date of accident per intake form: <follow-up date>'. HEAD returns [] (no conflict, no tray item, no note) for: B ER 'Restrained driver, vehicle hit from behind at a stoplight. Neck pain.' (2026-01-09 vs stated 2026-01-19); C ER 'MVA 12/30/2025, neck pain.' with stated 2026-01-05 (previous year's digits make the sentence 'historical'); D ER 'Rear-end collision, no history of loss of consciousness.' ('history' makes the sentence 'historical'); F ER 'Pt in car when another vehicle hit them.'; G ER 'Rear-end collision, driver of a 2019 Honda Civic.' (model year < stated year). Only the plain 'Rear-end collision. Neck pain.' (E) still conflicts. The new tests (tests/unit/test_conflicts.py::test_t141_a_stated_date_still_conflicts_when_an_earlier_record_describes_the_collision) use exactly that plain wording, so none of B, C, D, F, G is pinned.",
51	   "why_it_matters": "R-FL-2 makes the accident-date conflict a must for the sample, and the 'accident_date' check is advertised in GET case checks. The skip turns a deterministic check into a word-list guess and its failure is invisible: the paralegal sees neither a conflict nor a could-not-verify item, so a real discrepancy between the stated accident date and the first treatment disappears. Before c4bb4da all five cases were flagged. The sample and all 27 golden/library packets are unchanged (diff of conflicts and candidates pre vs HEAD: only lib11), which is why the existing suites stay green. Not a blocker only because it needs the stated date to coincide with another record's date and a collision wording outside the list; it is a lost conflict (rate by D.2 'loses facts' if Chris disagrees).",
52	   "fix": "Do not drop. Either (a) widen _EVENT (hit, struck by, vehicle, motor vehicle, car, airbag, T-boned, side-swiped) and apply the _HISTORICAL / earlier-year exclusion to the clause that names the accident, not to the whole sentence, and treat a year equal to the stated year minus 0 or 1 with a month as possibly the index event; or (b) when the skip would apply and an earlier record is not provably a pre-accident visit, keep the flag but state the other reading (the stated date matches record N) so the paralegal decides, as D-055 does for paperwork.",
53	   "acceptance_test": "tests/unit/test_conflicts.py: the five variants B, C, D, F, G each return one accident_date_after_treatment conflict; the lib11 shape (annual PCP visit 2026-03-04 listing 2019 and 2022 accidents, EMS 2026-03-18 'struck from behind', intake 2026-03-18) still returns []."
54	  },
55	  {
56	   "severity": "major",
57	   "title": "GET case `checks` is the same on every case, so a Spanish case, or a run whose conflicts stage was skipped, is still told 'checked for denial vs history' and 'plan vs early end'",
58	   "evidence": "app/backend/conflict_candidates.py:244-247 (checks() takes no argument), app/backend/present.py:317 (\"checks\": conflict_candidates.checks()), memory/contracts/api.md:133 ('always present, the same on every case'). The candidate rules are English regexes (_DENIAL, _FORM_STEM, _ENDED, _EN_*): `artifacts/review-evidence/T-141/probe3.py` on the HEAD archive, records lang='es': 'La paciente niega lesiones previas en el cuello.' vs 'Historial de accidente de tráfico en 2019...' -> False; 'Accidentes previos: No.' -> False; a Spanish plan/outcome pair -> []. Live API on the HEAD copy: POST the Spanish library packet evals/library/case_lib09_spanish_interpreter_espalda.txt, then GET case -> checks.conflict_types = ['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] and not_checked has no language entry. pipeline.py:360-362 also lets `guard(\"conflicts\")` skip the whole conflict pass (deadline), with checks unchanged.",
59	   "why_it_matters": "T-142 exists to stop the UI overclaiming ('No conflicts found'). It now gets a list that says what was checked on this case, but the list is a constant, so on a Spanish case or a timed-out run the UI can say 'Checked for: a denial of prior problems...' when nothing could have fired. Same failure family as the empty-state overclaim, moved one layer down, and it is in the new field this card adds.",
60	   "fix": "Make checks a function of the case: add `skipped: [{type, reason}]` (or move a type into not_checked) when records are lang 'es' for the two English-rule checks, when the conflicts stage was skipped or errored, and when no record has a parsed date for accident_date. Keep the constant lists for the default.",
61	   "acceptance_test": "tests/unit/test_api_routes.py: GET case for a Spanish packet has denial_vs_history and plan_vs_early_end under not_checked (or skipped) with a language reason; an English case is unchanged; a case whose conflicts stage was guarded off lists all pair-rule types as skipped."
62	  },
63	  {
64	   "severity": "minor",
65	   "title": "The new denial rule has no topic restriction on its stem, and the year-named accident route has no negation or scope guard; the judge is the only filter and the controls do not cover those shapes",
66	   "evidence": "app/backend/conflict_candidates.py:49 and :53 (_FORM_STEM / _FORM_ONE accept any 'Prior|Previous|Pre-existing|Earlier + letters' stem answered No/None), :55 + :106-111 (_earlier_year_accident: accident word within 40 characters of 'in <year>' < denial year, no negation check beyond _DENIAL). `artifacts/review-evidence/T-141/probe1.py` (25 pairs, run on c4bb4da~1 and c4bb4da): HEAD now pairs 'Previous employer: None.', 'Prior authorization required? Yes [ ] No [X].', 'Previous visits to this clinic: None.' with 'History of lumbar strain in 2022.'; pairs 'Prior accidents? Yes [ ] No [X].' with 'No car accidents in 2019 or 2022.', 'Patient denies accidents in 2019 and 2022.', 'Records show no motor vehicle accident in 2019.' (the prior side is itself a negation); pairs a scoped question 'Prior accidents in the last year? ... No [X].' with 'Car accident in 2019'; and 'Rear-end collision at Main St, patient first seen here in 2019.' (index collision plus an unrelated year). Correct as designed: Yes checked, both boxes empty, both boxes checked, a bare question, an accident in the denial's own year, husband and other driver (P04, P06, P07, P17, P19, P23). Roommate (P05) pairs on purpose (J3V20). 'No prior accidents since 2010' vs 'Car accident in 2005' (P08, P25) pairs on both builds (T-094 inherited, not new). Live check, one run each, claude-cli with ENABLE_LIVE=1 (exploratory, not the 3x controls): J3 answered benign CAN_BOTH_BE_TRUE on P13, P14, P15, P09, P10, P08 and conflict FACT_MISMATCH on the real lib11 pair; script artifacts/review-evidence/T-141/live_j3.py. judge_conflict_v6 rule 2(c) answers conflict for 'the denial is general' and has no time-scope, negated-history or topic rule.",
67	   "why_it_matters": "Candidate generation is the first rung of the ladder; a wrong candidate costs a judge call and, if the judge is unavailable or answers unsure, shows the paralegal a needs_review conflict about an employer or a prior authorization (flags.py: judge unavailable keeps the flag). The single live run held, but J3 is a model and no control covers these shapes. Labelled 'I would tighten it' rather than a spec violation: the ladder as designed puts the judge behind the rule.",
68	   "fix": "Restrict _FORM_STEM/_FORM_ONE nouns to a closed list (accident, collision, injury, injuries, surgery, surgeries, condition, treatment, claim, back/neck problems); skip a prior sentence that is negated ('no', 'denies', 'never' before the accident word); skip a denial stem containing 'in the last|past|since'. Add wrong controls (J3V21..) for a topic stem, a negated history and a scoped question.",
69	   "acceptance_test": "tests/unit/test_conflict_candidates.py: history_denials returns [] for P09, P10, P11, P12, P13, P14, P15; the lib11 pair and 'Prior injuries: None.' vs 'History of lumbar strain in 2022.' still pair."
70	  },
71	  {
72	   "severity": "minor",
73	   "title": "The live 3x controls run for J3R5, J3R6, J3R7 and J3V20 is owed and no card or owner exists; the changelog has no entry for the new rows",
74	   "evidence": "Latest committed report evals/reports/controls-20261102T123937Z.json (source_commit bea3984, controls_ok True) has 64 rows and none of J3R5, J3R6, J3R7, J3V20 (checked: set intersection empty). Its `hashes` block does not include judge_controls.jsonl, so nothing marks the report stale. `python3 tools/board.py list | grep -i control` shows no open card for the run; the handoff text says 'qa/orchestrator: python -m evals.run --controls on a clean tree'. evals/golden/judge_controls.CHANGELOG.md has no round for this change (last entry is T-093 round 4). Labels themselves are fine: locked in evals/j3_controls.py with a rationale per row and in LOCKED in tests/unit/test_t093_j3_controls_reachable.py in the same commit as the rows, committed before any run of them (git show c4bb4da), and the reachability test passes (116 passed on the three conflict/controls modules).",
75	   "why_it_matters": "Answer to the brief: the live run is not required for acceptance of this card (AC 1 asks for unit tests, expected update and 'controls unaffected', and I verified that: candidates and accident-date output over all 27 golden and library packets are identical pre vs HEAD except lib11). It is required before the M2 gate: D-046 makes J3 'catch every seeded wrong item, 0 false agrees' a ship-bar condition, J3V20 is a new wrong item with no result, and a fixture run will report not_measured for it. Without an owner it will surface at the gate.",
76	   "fix": "Open a qa card for `LLM_BACKEND=claude-cli ENABLE_LIVE=1 python -m evals.run --controls` (3 repeats) on a clean tree after the F-findings above land, so the rows for any new wrong controls run once; add the round entry to judge_controls.CHANGELOG.md with the four labels and reasons.",
77	   "acceptance_test": "A controls report newer than c4bb4da whose rows include J3R5, J3R6, J3R7 and J3V20 with 3 verdicts each; the changelog names them."
78	  },
79	  {
80	   "severity": "minor",
81	   "title": "A prior commit calls conflict_candidates.checks() before it exists: GET case raised AttributeError from T-143 until this commit",
82	   "evidence": "`git show 225e666:app/backend/present.py | grep -c 'conflict_candidates.checks()'` -> 1 and `git show 225e666:app/backend/conflict_candidates.py | grep -c 'def checks'` -> 0 (T-143 swept this hunk of T-141/T-142's work into its commit through the shared index). On the c4bb4da~1 archive: `.venv/bin/python -m pytest tests/unit/test_api_routes.py -q -x` -> `ERROR zlayt.api:api.py:184 unhandled AttributeError`, 1 failed (test_whole_case_after_run_matches_contract). Fixed at c4bb4da.",
83	   "why_it_matters": "Five commits (225e666 to e25098d) have a broken case endpoint; bisect lands on the wrong commit, and any reviewer pinned to one of them sees a 500 on every case.",
84	   "fix": "No code change needed now. Stage with pathspec per file-ownership rule; if a hunk of another card is in the index, commit them together or leave it unstaged.",
85	   "acceptance_test": "Each commit on main passes tests/unit/test_api_routes.py (a pre-push loop over the range)."
86	  },
87	  {
88	   "severity": "minor",
89	   "title": "lib11 still shows two 'mentions a prior or pre-existing condition' flags whose quotes are only the form labels, beside the new conflicts (paralegal view)",
90	   "evidence": "artifacts/review-evidence/T-141/lib11-body.txt:333 'Fennimoor Spine Clinic ... mentions a prior or pre-existing condition: “Prior accidents?”.' and :349 same for 'Prior injuries?'; screenshot artifacts/review-evidence/T-141/lib11-conflicts.png shows the two conflict cards. The flags carry the question without the answer (No), so they read as the form admitting a prior accident; the conflict cards beside them quote the answer. Two conflict cards also cite the same PCP sentence (accidents, injuries), so the paralegal decides the same fact twice. The GATE-M2 paralegal report listed the label-only flags as evidence; this card did not change them.",
91	   "why_it_matters": "A paralegal skimming 'mentions a prior or pre-existing condition: Prior accidents?' can quote it as an admission. The correct reading is in the conflict card, not in these.",
92	   "fix": "Suppress the lexicon pre_existing flag when the matched unit is a form stem answered No (the same _FORM_STEM + _FORM_NO test), or extend the quote to include the answer; show the two denial conflicts as one card with both quotes.",
93	   "acceptance_test": "lib11 case JSON: no pre_existing flag whose excerpt is 'Prior accidents?' or 'Prior injuries?'."
94	  },
95	  {
96	   "severity": "nit",
97	   "title": "Implementation notes written into the golden C1 summary",
98	   "evidence": "evals/library/case_lib11_priors_and_ledger.expected.json (C1 summary) now ends 'T-141: the code reads a checked No [X] (OCR No IX]) as the denial ... so this pair is now proposed and sent to the judge.'",
99	   "why_it_matters": "An expected file describes what the records say, not how the code finds it; the sentence will go stale with the next rule change.",
100	   "fix": "Keep the T-141 reason in the changelog or the card, not in the expected summary.",
101	   "acceptance_test": "C1 summary states only the record facts."
102	  }
103	 ],
104	 "whats_right": [
105	  "Intake form denials now read as a conflict with the answer quoted (No [X] and OCR No IX]), and the 27-packet differential shows only lib11 changed, so the existing J3 control text is untouched.",
106	  "N2 discriminates: the false accident-date conflict is red against the old code and green on HEAD; 9 of 11 mutants on the new rules are killed.",
107	  "Control labels were locked in code and in the test table in the same commit as the rows, before any run, with a reason per row."
108	 ],
109	 "questions_for_chris": [
110	  "Is the accident-date skip worth its recall cost? The alternative is to keep the conflict and print the other reading (the stated date matches record N), as D-055 does for paperwork."
111	 ]
112	}
113	```
114	
115	Erratum: the summary line above says 3 minor; the JSON block lists 4 minor findings (3, 4, 5, 6) and is authoritative.
116	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:18.987Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-141; git log --oneline | head -5; git status --short | head"
}
````

### User / tool · 2026-11-02T13:44:19.183Z

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
updated_at: "2026-11-02T13:44:07Z"
claimed_by: "backend"
claimed_at: "2026-11-02T13:31:30Z"
rounds: 1
commits: ["c4bb4da", "68b8685"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-141-staff-engineer.md", "at": "2026-11-02T13:31:22Z"}
ac:
  - {"n": 1, "text": "lib11 raises the denial-vs-history conflict (intake form as the denial side, D-053/T-113 rules) and no false accident-date conflict; unit + library expected update with a written reason; controls unaffected", "done": true, "evidence": "tests/unit/test_conflict_candidates.py::test_t141_* + test_conflicts.py::test_t141_* pass; lib11 fixture run: must flags 4/4, no accident-date conflict, J3 live verdict conflict on both denial pairs; no existing control text changed (candidate diff vs HEAD only adds lib11 pairs)"}
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

## Handoff
Round 2 (68b8685). What changed: accident-date conflict now decided by content: a record dated before the stated date is a conflict only if a clause of it names a collision/injury mechanism (widened word list; history/bare earlier year/full date >1y/model year judged per clause), compared against the earliest such record; else info note checks.notes RECORDS_PREDATE_ACCIDENT ('N records predate the stated accident date'). 'Single stated date' skip removed. GET case checks computed per case from a run summary stored in case config (pipeline._store_run_checks at ingest, run start, finalize): skipped[] with NOT_RUN, STAGE_SKIPPED, RUN_FAILED, LANGUAGE, LANGUAGE_PARTIAL (record_nos), NO_DATED_RECORD; conflict_types lists only what ran. api.md updated. How verified: reviewer variants B,C,D,E,F,G(+G2) conflict, lib11 shape and 5 old-note-history wordings do not (tests/unit/test_conflicts.py); checks tests in test_conflict_candidates.py, new test_t141_checks_per_case.py (ingested, deadline, failed, lib09 partial-language, lib11), test_api_routes t142; conflict suites + controls-reachable + flags/pipeline 204 pass; 27-packet diff: only sample conflicts, lib11 note=1; library_report lib11 must flags 4/4, must_not hits 0. Full unit: 12 failures, all T-139 charge_text / export-golden work of other workers (test_narrative passes alone). Changed one existing expected: test_t116_r4 blocker2 (statement dated before stated date, no collision wording = info, not conflict) plus a twin test for never-naming-paperwork. Left: round-1 minors 3 (stem topic list/negation guard), 6 (label-only pre_existing flags on lib11) not in this direction; live 3x controls owned by orchestrator; frontend T-142 should render skipped[]/notes[]. Surprised: GET case at ingest state had no pair stage so checks needed a NOT_RUN state; ingest runs the structural checks before any run.

68b8685 fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
07c7558 docs(orchestrator): D-059 letter total from one-at-a-time accepted charges with code flags
c5c18a6 feat(frontend): T-142 conflict group names the kinds checked (from GET case checks, fixed fallback) and says others are not checked; never a bare 'No conflicts found.'
4872cdb feat(frontend): T-136 r2 compared edit no longer reads Needs review; D-058 held re-picked quote says the export stays blocked and offers Write the summary; plain e2e run starts a private server with a temp ZLAYT_DB; mutant-killing tests
d19ae46 feat(backend): GET /api/cases summary list for the case overview (T-148)
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:21.302Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git show --stat 68b8685 | head -30; ls artifacts/review-evidence/T-141/; ls .claude/agent-memory/staff-engineer-reviewer | head -3; cat .claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md | head -20"
}
````

### User / tool · 2026-11-02T13:44:21.426Z

**tool result**
````
68b868575403c86cdac00d4fdc641ecd2494c613
commit 68b868575403c86cdac00d4fdc641ecd2494c613
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:43:47 2026 -0600

    fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
    
    A record dated before the stated accident date is a conflict only if a clause of it describes a collision or injury mechanism (per clause, history and
    model years excluded); otherwise it is an info note (checks.notes RECORDS_PREDATE_ACCIDENT). checks lists what ran: LANGUAGE / LANGUAGE_PARTIAL,
    STAGE_SKIPPED, RUN_FAILED, NOT_RUN, NO_DATED_RECORD, from the run summary stored in the case config.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/conflict_candidates.py           |  61 ++++++++++++++-
 app/backend/conflicts.py                     |  80 +++++++++++++++-----
 app/backend/pipeline.py                      |  16 +++-
 app/backend/present.py                       |   2 +-
 memory/contracts/api.md                      |   6 +-
 tests/unit/test_api_routes.py                |  11 ++-
 tests/unit/test_conflict_candidates.py       |  45 +++++++++++-
 tests/unit/test_conflicts.py                 | 106 ++++++++++++++++++++-------
 tests/unit/test_t116_r4_all_dated_records.py |  13 +++-
 tests/unit/test_t141_checks_per_case.py      |  76 +++++++++++++++++++
 10 files changed, 355 insertions(+), 61 deletions(-)
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
ui_conflict_shot.py
ui_lib11.py
MEMORY.md
feedback_differential_probe_prior_build.md
feedback_exact_count_vs_presence.md
---
name: feedback_shared_scratchpad
description: the scratchpad path is shared with other agents; use a unique card-round subdir, verify archive copies with diff -rq against a fresh git archive, never background a setup chain you depend on
metadata:
  type: feedback
---

Name scratch directories with the card and round (for example `T108_verify`), and run `ls -la` before reusing any directory. Check an archive copy with `diff -rq` against a fresh `git archive <sha>` before trusting results.

**Why:** during T-108 r1 the `probe/` folder I used already held another agent's repo archive, and sibling folders (`T106_*`) appeared in the same scratchpad during my run. My own setup line `mkdir -p X && cp ... && cd ... &` was backgrounded as one chain, so the following commands ran before the directory existed and wrote nothing.

**How to apply:** do not background setup you depend on; run it in the foreground or wait on it. Keep probe scripts in your own unique directory and copy the final ones to `artifacts/review-evidence/<card>/` as the evidence.

Related: [[project_t108_quote_units_patterns]].
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:26.783Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la $S; mkdir -p $S/T141r2_head && git archive 68b8685 | tar -x -C $S/T141r2_head && ls $S/T141r2_head | head -30; ls -la .venv/bin/python; cat artifacts/review-evidence/T-141/probe2.py"
}
````

### User / tool · 2026-11-02T13:44:28.349Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:31.536Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls $S/T141r2_head | head -30; ls $S | grep -i T141; ls -la .venv/bin/python; cat artifacts/review-evidence/T-141/probe2.py"
}
````

### User / tool · 2026-11-02T13:44:31.681Z

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
T141_head
T141_mut
T141_pre
T141_preN2
T141_probe
T141_run
T141r2_head
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:34.558Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; diff -rq <(git archive 68b8685 | tar -t | sort) <(cd $S/T141r2_head && find . -type f | sed 's|^\\./||' | sort) | head -3; git show 68b8685 -- app/backend/conflicts.py app/backend/conflict_candidates.py app/backend/pipeline.py app/backend/present.py"
}
````

### User / tool · 2026-11-02T13:44:35.053Z

**tool result**
````
Files /dev/fd/63 and /dev/fd/62 differ
commit 68b868575403c86cdac00d4fdc641ecd2494c613
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:43:47 2026 -0600

    fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
    
    A record dated before the stated accident date is a conflict only if a clause of it describes a collision or injury mechanism (per clause, history and
    model years excluded); otherwise it is an info note (checks.notes RECORDS_PREDATE_ACCIDENT). checks lists what ran: LANGUAGE / LANGUAGE_PARTIAL,
    STAGE_SKIPPED, RUN_FAILED, NOT_RUN, NO_DATED_RECORD, from the run summary stored in the case config.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/conflict_candidates.py b/app/backend/conflict_candidates.py
index d5e4f10..1fff031 100644
--- a/app/backend/conflict_candidates.py
+++ b/app/backend/conflict_candidates.py
@@ -241,7 +241,60 @@ NOT_CHECKED = [
 ]
 
 
-def checks() -> dict:
-    """{conflict_types: [..], labels: {type: sentence}, not_checked: [{type, label}]}: a fixed list; the same on every case."""
-    types = list(CONFLICT_LABELS)
-    return {"conflict_types": types, "labels": dict(CONFLICT_LABELS), "not_checked": [dict(x) for x in NOT_CHECKED]}
+_PAIR_TYPES = ("plan_vs_early_end", "denial_vs_history")
+_ENGLISH_RULE_TYPES = _PAIR_TYPES + ("accident_date",)       # these read English wording; provider_name compares header labels and is language-free
+_LANG_WORD = {"es": "Spanish", "uncertain": "an unidentified language", "other": "an unsupported language"}
+
+
+def run_summary(records: list, *, stage: str) -> dict:
+    """What THIS case's check stage did, for GET case `checks` (stored in the case config by the pipeline). stage: 'pending' (ingested or running),
+    'ran', or 'skipped' (the run deadline passed before the conflict stage). {conflicts_stage, read_records, unread: {lang: [record nos]},
+    dated_records, notes}. `read_records` counts records the English rules can read; Spanish, uncertain and unsupported-language records are listed in `unread`."""
+    from app.backend import conflicts
+    unread = {}
+    for r in records:
+        lang = r.get("lang") or "en"
+        if lang != "en":
+            unread.setdefault(lang, []).append(r["n"])
+    note = conflicts.accident_date_note(records)
+    return {"conflicts_stage": stage, "read_records": sum(1 for r in records if (r.get("lang") or "en") == "en"),
+            "unread": {k: sorted(v) for k, v in sorted(unread.items())}, "dated_records": sum(1 for r in records if r.get("date_iso")),
+            "notes": [note] if note else []}
+
+
+def checks(run: dict = None, state: str = "complete") -> dict:
+    """GET case `checks`, computed from what this case actually ran (T-141 r2). `run` is run_summary() as stored; `state` is 'complete', 'not_run'
+    (created, not analysed) or 'failed'. {conflict_types: [what ran], labels: {type: sentence}, skipped: [{type, label, reason_code, reason, record_nos?}],
+    not_checked: [{type, label}], notes: [..]}. A type is in `skipped` without `record_nos` when it did not run at all (and is then absent from
+    conflict_types), and with `record_nos` when it ran but could not read those records (Spanish and the like)."""
+    known = run is not None
+    run = run or {}
+    stage = run.get("conflicts_stage")
+    skipped = []
+
+    def skip(t, code, reason, nos=None):
+        skipped.append({"type": t, "label": CONFLICT_LABELS[t], "reason_code": code, "reason": reason, **({"record_nos": nos} if nos else {})})
+
+    for t in CONFLICT_LABELS:
+        if state == "failed" and not known:
+            skip(t, "RUN_FAILED", "The run stopped before this check finished, so nothing is known about it.")
+        elif t in _PAIR_TYPES and not (stage == "ran" or (stage is None and state == "complete")):
+            if stage == "skipped":
+                skip(t, "STAGE_SKIPPED", "The run reached its time limit before the comparison between records. Run it again to check.")
+            elif state == "failed":
+                skip(t, "RUN_FAILED", "The run stopped before the comparison between records finished.")
+            else:
+                skip(t, "NOT_RUN", "The comparison between records has not run yet.")
+        elif t == "accident_date" and run.get("dated_records") == 0:
+            skip(t, "NO_DATED_RECORD", "No record has a date the code could read, so there is nothing to compare a stated accident date with.")
+        elif t in _ENGLISH_RULE_TYPES and run.get("unread"):
+            unread = run["unread"]
+            nos = sorted(n for v in unread.values() for n in v)
+            langs = " and ".join(_LANG_WORD.get(k, k) for k in unread)
+            if run.get("read_records") == 0:
+                skip(t, "LANGUAGE", f"This check reads English wording and every record is in {langs}, so it could not find anything.")
+            else:
+                skip(t, "LANGUAGE_PARTIAL", f"This check reads English wording; the records in {langs} were not read.", nos)
+    whole = {x["type"] for x in skipped if "record_nos" not in x}
+    return {"conflict_types": [t for t in CONFLICT_LABELS if t not in whole], "labels": dict(CONFLICT_LABELS), "skipped": skipped,
+            "not_checked": [dict(x) for x in NOT_CHECKED], "notes": [dict(n) for n in run.get("notes") or []]}
diff --git a/app/backend/conflicts.py b/app/backend/conflicts.py
index a15d27d..f2ccd78 100644
--- a/app/backend/conflicts.py
+++ b/app/backend/conflicts.py
@@ -8,31 +8,56 @@ from app.backend.ingest import evidence_span
 
 PHRASE_TO_DATE_CHARS = 40
 
-# T-141 (GATE-M2 lib11): an annual visit two weeks BEFORE the collision is not treatment for it. A stated date later than the earliest record is
-# not a disagreement when (a) another record is dated exactly that day and (b) no record dated before that day describes a collision/accident of
-# its own. "Accidents in 2019 and 2022" in an old note is history (a year before the stated one, or a prior/history word), not this collision.
-_EVENT = re.compile(r"\b(?:collision|crash\w*|MVA|MVC|rear[- ]?end\w*|struck|wreck\w*|accident\w*|fell|fall)\b", re.I)
-_HISTORICAL = re.compile(r"\b(?:prior|previous|previously|earlier|history|hx|remote|years?\s+ago)\b", re.I)
+# T-141 r2 (GATE-M2 lib11): the content decides, not a coinciding date. A stated accident date later than the earliest record is a conflict only when
+# a record dated before it describes the collision or an injury mechanism (a clause of its own that is not history). Records dated before it that
+# do not are earlier visits: the case notes how many (accident_date_note), nothing is raised. "Accidents in 2019 and 2022" in an old note is history.
+_EVENT = re.compile(r"\b(?:collision|collided|crash\w*|MVA|MVC|MVI|rear[- ]?end\w*|struck|hit|wreck\w*|accident\w*|vehicle|airbag\w*|seat\s?belt\w*|"
+                    r"t-?bone\w*|side-?swip\w*|run\s+over|fell|fall(?:ing)?\s+(?:from|off|down))\b", re.I)
+_HISTORICAL = re.compile(r"\b(?:prior|previous|previously|earlier|history|hx|remote|years?\s+ago|as\s+a\s+child)\b", re.I)
 _YEAR = re.compile(r"\b(19\d\d|20\d\d)\b")
+_MODEL_YEAR = re.compile(r"\b(?:19|20)\d\d(?=\s+[A-Z][a-z])")
+_CLAUSE_SPLIT = re.compile(r"[;,]|\s[-\u2013\u2014]\s|\s\(|\)")
+
+
+def _historical(clause: str, iso: str) -> bool:
+    """A clause is history when it says so, names a bare year before the stated one, or holds a full date more than a year before it. A full date within the
+    year before (MVA 12/30/2025 against a stated 2026-01-05) is a possible index event, and a model year ('a 2019 Honda Civic') is not a date."""
+    if _HISTORICAL.search(clause):
+        return True
+    rest = clause
+    for d in sorted(dates.find_dates(clause), key=lambda x: -x["start"]):
+        if d["status"] == "parsed" and d["iso"] < iso and (_days_between(d["iso"], iso) or 0) > 365:
+            return True
+        rest = rest[:d["start"]] + " " * (d["end"] - d["start"]) + rest[d["end"]:]
+    rest = _MODEL_YEAR.sub("    ", rest)
+    return any(int(y) < int(iso[:4]) for y in _YEAR.findall(rest))
+
+
+def _days_between(a: str, b: str):
+    from datetime import date
+    try:
+        return (date.fromisoformat(b) - date.fromisoformat(a)).days
+    except ValueError:
+        return None
 
 
 def _describes_event(rec: dict, iso: str) -> bool:
-    """The record has a sentence that names a collision or accident and is not history (no prior/history word, no year earlier than the stated date's year)."""
+    """The record has a clause that names a collision, accident or injury mechanism and is not history (judged per clause, not per sentence)."""
     from app.backend import sentences
     text = rec.get("excerpt") or ""
-    year = int(iso[:4])
     for a, b in sentences.stripped_spans(text):
-        u = text[a:b]
-        if _EVENT.search(u) and not _HISTORICAL.search(u) and not any(int(y) < year for y in _YEAR.findall(u)):
-            return True
+        unit = text[a:b]
+        for d in dates.find_dates(unit):                                     # "January 9, 2026" is one date, not two clauses
+            unit = unit[:d["start"]] + d["text"].replace(",", "\x01") + unit[d["end"]:]
+        for clause in (c.replace("\x01", ",") for c in _CLAUSE_SPLIT.split(unit)):
+            if _EVENT.search(clause) and not _historical(clause, iso):
+                return True
     return False
 
 
-def _corroborated(s: dict, records: list) -> bool:
-    """The stated date is also the date of a different record, and nothing dated earlier describes the collision itself."""
-    if not any(o["n"] != s["record_no"] and o.get("date_iso") == s["iso"] for o in records):
-        return False
-    return not any(o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"]) for o in records)
+def _event_records(s: dict, records: list) -> list:
+    """Records dated before the stated date that describe the collision itself."""
+    return [o for o in records if o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"])]
 
 
 def _encounters(records):
@@ -70,10 +95,14 @@ def accident_date_conflicts(records: list) -> list:
     if not stated or not enc:
         return []
     first = min(r["date_iso"] for r in enc)
-    first_recs = [r for r in enc if r["date_iso"] == first]
     by_n = {r["n"]: r for r in records}
     distinct = sorted({s["iso"] for s in stated})
-    later = [s for s in stated if s["iso"] > first and not (len(distinct) < 2 and _corroborated(s, records))]
+    later = [s for s in stated if s["iso"] > first]
+    if len(distinct) < 2:
+        later = [s for s in later if _event_records(s, enc)]         # T-141 r2: an earlier visit that does not describe the collision is info, not a conflict
+        if later:
+            first = min(r["date_iso"] for r in _event_records(later[0], enc))      # compare with the earliest record that describes it
+    first_recs = [r for r in enc if r["date_iso"] == first]
     if len(distinct) < 2 and not later:
         return []
     if len(distinct) >= 2:
@@ -107,6 +136,23 @@ def accident_date_conflicts(records: list) -> list:
              "body_date": a["iso"], "stated_dates": distinct, "first_treatment_date": first, "record_nos": nos, "evidence": ev}]
 
 
+def accident_date_note(records: list):
+    """T-141 r2: when one stated accident date is later than some records and no conflict is raised for it, how many records predate it.
+    Info for the case's `checks.notes`; never a flag. None when there is nothing to say."""
+    enc = _encounters(records)
+    distinct = sorted({s["iso"] for s in stated_accident_dates(records)})
+    if len(distinct) != 1 or not enc or accident_date_conflicts(records):
+        return None
+    iso = distinct[0]
+    before = sorted((r for r in enc if r["date_iso"] < iso), key=lambda r: r["n"])
+    if not before:
+        return None
+    n = len(before)
+    lead = f"{n} record predates" if n == 1 else f"{n} records predate"
+    return {"type": "accident_date", "code": "RECORDS_PREDATE_ACCIDENT", "count": n, "record_nos": [r["n"] for r in before], "stated_date": iso,
+            "text": f"{lead} the stated accident date, {dates.long_date(iso)}. None describes a collision, so no date conflict is raised; check that they are earlier care."}
+
+
 _TITLES = {"dr", "md", "do", "dc", "np", "pa", "pac", "dpm", "dds", "dpt", "pt", "phd", "rn", "mr", "ms", "mrs"}
 _WORD = re.compile(r"[A-Za-z][A-Za-z'-]*\.?")
 
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index eb86544..9221f82 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -11,7 +11,7 @@ import sys
 import time
 from concurrent.futures import ThreadPoolExecutor
 
-from app.backend import (amounts as AM, confidence, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
+from app.backend import (amounts as AM, confidence, conflict_candidates as CC, conflicts as CF, flags as FL, gaps as GP, generator, ingest as IN,
                          judges, language, split_llm, totals as TT, why as WHY)
 from app.db import db as DB
 from app.llm import audited as AU, provider as P
@@ -157,6 +157,14 @@ def _store_record_marks(conn, cid: str, ing: dict) -> None:
     DB.update_case(conn, cid, config_json=cfg or None)
 
 
+def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
+    """T-141 r2: what the conflict checks did on THIS case (language routing, whether the pair stage ran), kept in the case config so GET case `checks`
+    is computed from the run, not a constant. stage: 'pending' (ingested, or the run has started), 'ran', 'skipped' (deadline before the stage)."""
+    cfg = dict((DB.get_case(conn, cid) or {}).get("config") or {})
+    cfg["run_checks"] = CC.run_summary(recs, stage=stage)
+    DB.update_case(conn, cid, config_json=cfg)
+
+
 def _item_record_ids(item: dict) -> list:
     return list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
 
@@ -268,6 +276,7 @@ def ingest_case(conn, cid: str, raw_text: str, now: float = 0.0) -> dict:
     """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
     ing = run_ingest(raw_text, not_duplicates=_not_duplicates(conn, cid))
     _store_records(conn, cid, ing, now)
+    _store_run_checks(conn, cid, ing["records"], "pending")
     _persist(conn, cid, "flag", ing["flags"], now)
     _persist(conn, cid, "amount", [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]], now)
     DB.update_case(conn, cid, injection_records_json=ing["injection_records"], backend=P.backend_name())
@@ -337,6 +346,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     if ing.get("split_detail") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
         errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_detail"] == "FIXTURE_MISS" else None))
     _store_records(conn, cid, ing, clock())
+    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
     dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
     entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
     code_amounts = [_finish_amount(a, ing, None) for a in ing["amounts"] + ing["damages"]]
@@ -379,7 +389,8 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     # 5: cross-record conflicts. Code proposes the candidate pairs; J3 classifies each (T-094). No model search, so the candidate set cannot vary.
     llm_flags = []
     distinct = [by_n[g[0]] for g in ing["groups"] if by_n[g[0]].get("lang") != "other"]     # unsupported-language records are skipped (warning + error)
-    if guard("conflicts"):
+    conflicts_ran = guard("conflicts")
+    if conflicts_ran:
         llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
     # 6: per-record flags (one call per distinct record) + J4
     if guard("flags"):
@@ -425,6 +436,7 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t, additive=timed_out)
     _persist(conn, cid, "amount", final_amounts, now_t, additive=timed_out)
     _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t, additive=timed_out)
+    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
     if timed_out:
         status = "timeout"
         err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
diff --git a/app/backend/present.py b/app/backend/present.py
index d9ad869..4d494e4 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -314,7 +314,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
     return {"token": case_id, "name": case["name"], "status": case["status"], "demo_mode": demo_mode, "backend": backend, "models": models,
             "records": record_views, "undated_entries": undated, "entries": dated,
             "amounts": [a for a in its["amount"] if a["state"] != "rejected"], "totals": totals_view(conn, case_id),
-            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks(), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
+            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete"), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
             "injection": {"records": injected, "banner": "Some records contain instruction-like text; everything from them needs review." if injected else None},
             "review": review_view(conn, case_id), "warnings": [], "error": err,
             "created_at": store.iso(case["created_at"]), "updated_at": store.iso(case.get("run_finished_at") or case["created_at"]),
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:47.680Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head && grep -n \"accident_date_conflicts\\|provider_name_conflicts\\|accident_date_note\\|run_conflict_pass\\|\\\"conflicts\\\"\" -r app | grep -v \"^app/frontend\"; grep -n \"def run_conflict_pass\" -A40 app/backend/flags.py | head -80"
}
````

### User / tool · 2026-11-02T13:44:47.785Z

**tool result**
````
app/backend/trace.py:609:        step_name = "conflicts" if ftype == "conflict" else "flags"
app/backend/flags.py:188:    """A conflict the model proposed in the per-record pass (T-113, D-053; T-109 r2): only a code candidate (run_conflict_pass) can be a conflict flag, so the
app/backend/flags.py:299:def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
app/backend/flags.py:379:    A model-proposed CONFLICT is never a flag: only a code candidate (run_conflict_pass) can make one, so the model's goes to the tray (D-053)."""
app/backend/api.py:36:STAGES = ["ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize"]
app/backend/pipeline.py:19:STAGES = ("ingest", "extract", "verify", "judge_entries", "amounts", "conflicts", "flags", "finalize")
app/backend/pipeline.py:59:    code = GP.gap_flags(recs) + CF.accident_date_conflicts(recs) + CF.provider_conflicts(recs)
app/backend/pipeline.py:392:    conflicts_ran = guard("conflicts")
app/backend/pipeline.py:394:        llm_flags += FL.run_conflict_pass(distinct, call=call, any_tagged=bool(ing["injection_records"]), case_text=text)
app/backend/review.py:510:    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
app/backend/conflicts.py:2:accident_date_conflicts: stated accident dates (lexicon `accident_date_phrases`) vs the earliest recorded treatment date.
app/backend/conflicts.py:13:# do not are earlier visits: the case notes how many (accident_date_note), nothing is raised. "Accidents in 2019 and 2022" in an old note is history.
app/backend/conflicts.py:64:    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
app/backend/conflicts.py:91:def accident_date_conflicts(records: list) -> list:
app/backend/conflicts.py:139:def accident_date_note(records: list):
app/backend/conflicts.py:144:    if len(distinct) != 1 or not enc or accident_date_conflicts(records):
app/backend/conflict_candidates.py:259:    note = conflicts.accident_date_note(records)
299:def run_conflict_pass(records: list, *, call, any_tagged: bool = False, case_text: str = "") -> list:
300-    """Conflicts between records (T-094, R-CO-7). CODE proposes the candidate pairs (conflict_candidates.py: a stated plan against a later early end,
301-    a denial of prior problems against a prior-condition sentence; frequency x duration is multiplied out, so '2x/week for 6 weeks' agrees with
302-    '12 visits' and is never asked about). The model's only job is the classification of each candidate, by J3 (judge_conflict_v6). There is no
303-    open-ended search call, so the set of candidates cannot vary between runs.
304-    Policy for the answer: conflict -> flag (verified when the other checks hold); unsure / judge failed -> flag stays needs_review;
305-    benign -> the could-not-verify tray (state rejected, JUDGE_DISAGREES), shown to the paralegal, never exported. For a denial, candidates are
306-    judged one at a time in record order and the first confirmed conflict stands (later ones are not asked)."""
307-    by_n = {r["n"]: r for r in records}
308-    cands = CC.candidates(records)
309-    flags, settled = [], set()
310-    for i, c in enumerate(cands, 1):
311-        f = _candidate_flag(c, by_n, any_tagged, f"f_cx{i}")
312-        flags.append(f)
313-        if c["group"] in settled and c["rule"] == "history_denial":
314-            f["_skip"] = True
315-            continue
316-        if f["state"] == "rejected":
317-            continue
318-        _judge_one(f, i - 1, call=call, case_text=case_text)
319-        if c["rule"] == "history_denial" and f["state"] != "rejected" and f["ladder"]["judge"]["verdict"] == "conflict":
320-            settled.add(c["group"])
321-    return [{k: v for k, v in f.items() if k not in ("_skip", "_group")} for f in flags if not f.get("_skip")]
322-
323-
324-# ------------------------------------------------------------------ rung 2 for flags (J3 / J4)
325-def _judge_one(f: dict, i: int, *, call, case_text: str = "") -> None:
326-    item = f.get("id") or f"f{i}"
327-    nonce = promptlib.nonce(case_text, "j3" if f["type"] == "conflict" else "j4", item)
328-    try:
329-        if f["type"] == "conflict":
330-            if not f.get("excerpt_b"):
331-                return
332-            v, cid, reason = judges.run_j3_meta(f["excerpt"], f["excerpt_b"], call=call, nonce=nonce, item_id=item, category=f["category"])
333-            step, pv = "j3", JUDGE_PROMPT["j3"]
334-        elif f["origin"] in ("llm", "both"):
335-            v, cid, reason = judges.run_j4_meta(f["excerpt"], f["type"], f["category"], call=call, nonce=nonce, item_id=item)
336-            step, pv = "j4", JUDGE_PROMPT["j4"]
337-        else:
338-            return
339-    except P.FixtureMiss:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:44:52.260Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp && R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/probe2.py $R"
}
````

### User / tool · 2026-11-02T13:44:52.506Z

**tool result**
````
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

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:45:01.937Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head && sed -n 55,140p app/backend/conflicts.py; git -C /Users/arsis/zlayt-pm-project show 68b8685 -- tests/unit/test_t116_r4_all_dated_records.py"
}
````

### User / tool · 2026-11-02T13:45:02.045Z

**tool result**
````
    return False


def _event_records(s: dict, records: list) -> list:
    """Records dated before the stated date that describe the collision itself."""
    return [o for o in records if o.get("date_iso") and o["date_iso"] < s["iso"] and _describes_event(o, s["iso"])]


def _encounters(records):
    """D-055: every dated record counts for the earliest date. Whether the earliest one is paperwork is shown beside it (see accident_date_conflicts)."""
    return [r for r in records if r.get("date_iso")]


def stated_accident_dates(records: list) -> list:
    """[{record_no, iso, quote, start, end}]: a lexicon phrase followed within 40 characters by a parsed date, per record excerpt."""
    out = []
    for r in records:
        text = r.get("excerpt") or ""
        for e in lexicon.code_list("accident_date_phrases"):
            for m in e["regex"].finditer(text):
                for d in dates.find_dates(text[m.end():m.end() + PHRASE_TO_DATE_CHARS + 12]):
                    if d["start"] > PHRASE_TO_DATE_CHARS:
                        break
                    if d["status"] == "parsed":
                        end = m.end() + d["end"]
                        out.append({"record_no": r["n"], "iso": d["iso"], "quote": text[m.start():end], "start": m.start(), "end": end})
                    break
    seen, uniq = set(), []
    for s in sorted(out, key=lambda x: (x["record_no"], x["start"], -x["end"])):
        k = (s["record_no"], s["iso"])
        if k not in seen:
            seen.add(k)
            uniq.append(s)
    return uniq


def accident_date_conflicts(records: list) -> list:
    """At most one conflict per case. (a) a stated date later than the earliest treatment date, or (b) two different stated dates."""
    stated = stated_accident_dates(records)
    enc = _encounters(records)
    if not stated or not enc:
        return []
    first = min(r["date_iso"] for r in enc)
    by_n = {r["n"]: r for r in records}
    distinct = sorted({s["iso"] for s in stated})
    later = [s for s in stated if s["iso"] > first]
    if len(distinct) < 2:
        later = [s for s in later if _event_records(s, enc)]         # T-141 r2: an earlier visit that does not describe the collision is info, not a conflict
        if later:
            first = min(r["date_iso"] for r in _event_records(later[0], enc))      # compare with the earliest record that describes it
    first_recs = [r for r in enc if r["date_iso"] == first]
    if len(distinct) < 2 and not later:
        return []
    if len(distinct) >= 2:
        a, b = stated[0], next(s for s in stated if s["iso"] != stated[0]["iso"])
        category = "accident_dates_differ"
        title, expl = flag_templates.render("conflict", category, date_a=a["iso"], date_b=b["iso"], quote_a=a["quote"], quote_b=b["quote"],
                                            provider_a=by_n[a["record_no"]].get("source"), provider_b=by_n[b["record_no"]].get("source"))
        cited = [a, b]
    else:
        a = later[0]
        category = "accident_date_after_treatment"
        # D-055 (T-116 r4/T-123): never state paperwork as the first treatment. If ANY record on the earliest date looks like paperwork (alone, or
        # sharing the date with a visit, in either order), the sentence names that record, says it looks like paperwork, and gives the other reading
        # (the first recorded visit); the paralegal decides.
        extra = {}
        paper = [r for r in first_recs if gaps.admin_label(r)]
        if paper:
            visits = sorted((r for r in enc if not gaps.admin_label(r)), key=lambda r: (r["date_iso"], r["n"]))
            extra = {"record_no": paper[0]["n"]}
            if visits:
                extra.update(alt_record_no=visits[0]["n"], alt_date=visits[0]["date_iso"], alt_provider=visits[0].get("source") or "the record",
                             alt_later="also" if a["iso"] > visits[0]["date_iso"] else "not")
        ordered = paper + [r for r in first_recs if r not in paper]
        title, expl = flag_templates.render("conflict", category, stated=a["iso"], quote=a["quote"], date=first,
                                            provider_a=ordered[0].get("source"),
                                            provider_b=ordered[1].get("source") if len(ordered) > 1 else None, **extra)
        cited = [a]
    ev = [evidence_span(by_n[s["record_no"]], "excerpt", s["quote"]) for s in cited] + [evidence_span(r, "date") for r in first_recs]
    nos = sorted({s["record_no"] for s in cited} | {r["n"] for r in first_recs})
    return [{"subtype": "accident_date", "category": category, "type": "conflict", "origin": "code", "title": title, "explanation": expl,
             "body_date": a["iso"], "stated_dates": distinct, "first_treatment_date": first, "record_nos": nos, "evidence": ev}]


def accident_date_note(records: list):
    """T-141 r2: when one stated accident date is later than some records and no conflict is raised for it, how many records predate it.
commit 68b868575403c86cdac00d4fdc641ecd2494c613
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:43:47 2026 -0600

    fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
    
    A record dated before the stated accident date is a conflict only if a clause of it describes a collision or injury mechanism (per clause, history and
    model years excluded); otherwise it is an info note (checks.notes RECORDS_PREDATE_ACCIDENT). checks lists what ran: LANGUAGE / LANGUAGE_PARTIAL,
    STAGE_SKIPPED, RUN_FAILED, NOT_RUN, NO_DATED_RECORD, from the run summary stored in the case config.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_t116_r4_all_dated_records.py b/tests/unit/test_t116_r4_all_dated_records.py
index 4bc825f..9300133 100644
--- a/tests/unit/test_t116_r4_all_dated_records.py
+++ b/tests/unit/test_t116_r4_all_dated_records.py
@@ -153,11 +153,20 @@ def test_blocker2_a_visit_on_the_earliest_date_keeps_the_plain_wording():
 
 
 def test_blocker2_a_billing_statement_dated_before_the_first_visit_does_not_become_the_first_treatment():
+    """T-141 r2: the statement (01-05) predates the stated accident (01-09) but says nothing about a collision, so it is an info note, not a conflict; the first
+    visit (01-12) is after the stated date. Expected changed from 'conflict naming the statement' (old rule: any earlier-dated record was 'treatment')."""
     recs = I.ingest(pk(("2026-01-05", "Hobbleton Clinic, billing statement", "Balance forward."), ("2026-01-12", "Capital PT, visit 1", "Exam: ok. Date of accident: 2026-01-09"),
                        ("2026-01-20", "Capital PT, visit 2", "Exam: ok.")))["records"]
+    assert CF.accident_date_conflicts(recs) == []
+    assert CF.accident_date_note(recs)["record_nos"] == [1]
+
+
+def test_blocker2_a_billing_statement_dated_before_the_first_visit_is_never_named_as_the_first_treatment():
+    """Stated 01-15, statement 01-05, visit 01-12 whose text states the accident: the conflict compares with the visit, never with the statement."""
+    recs = I.ingest(pk(("2026-01-05", "Hobbleton Clinic, billing statement", "Balance forward."), ("2026-01-12", "Capital PT, visit 1", "Exam: ok. Date of accident: 2026-01-15"),
+                       ("2026-01-20", "Capital PT, visit 2", "Exam: ok.")))["records"]
     (c,) = CF.accident_date_conflicts(recs)
-    assert "first recorded treatment" not in c["explanation"] and "record 1: Hobbleton Clinic, billing statement" in c["explanation"]
-    assert "the first recorded visit is January 12, 2026" in c["explanation"]
+    assert "first recorded treatment, January 12, 2026" in c["explanation"] and "paperwork" not in c["explanation"] and c["record_nos"] == [2]
 
 
 # ---- through the API (fixture backend): both numbers reach the flag's explanation, why and trace
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:45:33.279Z

**tool call — Bash**
````
{
 "command": "cat artifacts/review-evidence/T-141/diff_packets.py; cat artifacts/review-evidence/T-141/mutate.py | head -60; grep -n \"accident\" spec/SAMPLE_CASE_TRUTHS.md | head"
}
````

### User / tool · 2026-11-02T13:45:33.410Z

**tool result**
````
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
import subprocess, sys, pathlib
root = pathlib.Path(sys.argv[1])
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
muts = [
 ("app/backend/conflict_candidates.py", "elif _FORM_ONE.match(u):", "elif False:", "M1 form-one colon denial off"),
 ("app/backend/conflict_candidates.py", "and _FORM_NO.match(text[spans[i + 1][0]:spans[i + 1][1]].strip()):", "and True:", "M2 any next unit is an answer"),
 ("app/backend/conflict_candidates.py", "return any(int(m.group(1)) < int(year) for m in _ACCIDENT_IN_YEAR.finditer(unit))", "return any(int(m.group(1)) <= int(year) for m in _ACCIDENT_IN_YEAR.finditer(unit))", "M3 year < -> <="),
 ("app/backend/conflict_candidates.py", "if not year.isdigit() or _DENIAL.search(unit) or _FORM_STEM.match(unit):", "if not year.isdigit():", "M4 drop denial/stem guard in earlier_year"),
 ("app/backend/conflict_candidates.py", "priors = [(o, q) for o, q in priors if _PRIOR_EVENT.search(q) or _earlier_year_accident(q, r)]", "pass", "M5 accident stem narrowing off"),
 ("app/backend/conflict_candidates.py", "_BOX = r\"[\\[(]?\\s*(?:[Il1]\\s*)?[xX\\u2713\\u2714]\\s*[\\])]\"", "_BOX = r\"[\\[(]?\\s*[xX\\u2713\\u2714]\\s*[\\])]\"", "M6 OCR I-prefix removed"),
 ("app/backend/conflicts.py", "if not any(o[\"n\"] != s[\"record_no\"] and o.get(\"date_iso\") == s[\"iso\"] for o in records):\n        return False", "if False:\n        return False", "M7 corroboration needs other record -> off"),
 ("app/backend/conflicts.py", "return not any(o.get(\"date_iso\") and o[\"date_iso\"] < s[\"iso\"] and _describes_event(o, s[\"iso\"]) for o in records)", "return True", "M8 earlier-event check off"),
 ("app/backend/conflicts.py", "not (len(distinct) < 2 and _corroborated(s, records))", "not _corroborated(s, records)", "M9 corroboration applies with 2 distinct dates"),
 ("app/backend/conflicts.py", "and not _HISTORICAL.search(u) and not any(int(y) < year for y in _YEAR.findall(u))", "and not _HISTORICAL.search(u)", "M10 prior-year digits no longer disqualify"),
 ("app/backend/conflict_candidates.py", "def checks() -> dict:", "def checks() -> dict:\n    return {'conflict_types': [], 'labels': {}, 'not_checked': []}", "M11 checks empty"),
]
for rel, old, new, label in muts:
    p = root / rel; src = p.read_text()
    if old not in src: print("SKIP (pattern not found)", label); continue
    p.write_text(src.replace(old, new, 1))
    r = subprocess.run([PY, "-I", "-m", "pytest", "tests/unit/test_conflict_candidates.py", "tests/unit/test_conflicts.py", "tests/unit/test_t093_j3_controls_reachable.py", "tests/unit/test_api_routes.py", "-q", "-x", "-p", "no:cacheprovider"], cwd=root, capture_output=True, text=True)
    p.write_text(src)
    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]
    print(("KILLED  " if r.returncode else "SURVIVED"), label, "|", tail[:110])
7:- **Conflict:** accident date — 2026-01-09 per EMS and ER records vs "Date of accident per intake form: 2026-01-19" (record 7). Also a treatment-plan discrepancy: 12 planned PT visits vs discharge at visit 9 after two missed appointments (records 4, 6).
9:- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).
13:Things the tool must not do on this case: state a diagnosis of disc herniation caused by the collision; convert "may represent degenerative change" into either "degenerative" or "traumatic"; compute a PT total; merge the two accident dates into one; treat "concussion without loss of consciousness" as anything other than what it says.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:45:39.500Z

**tool call — Bash**
````
{
 "command": "cd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; P=/Users/arsis/zlayt-pm-project/.venv/bin/python; E=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141; ls $S/T141_head | head -3; for d in T141_head T141_pre T141r2_head; do $P -I $E/diff_packets.py $S/$d > $S/T141r2_pk_$d.json 2>$S/T141r2_pk_$d.err; echo $d $?; done; diff $S/T141r2_pk_T141_head.json $S/T141r2_pk_T141r2_head.json; echo ---; diff $S/T141r2_pk_T141_pre.json $S/T141r2_pk_T141r2_head.json | head -40"
}
````

### User / tool · 2026-11-02T13:45:40.277Z

**tool result**
````
CLAUDE.md
MASTER_PROMPT.md
app
T141_head 0
T141_pre 0
T141r2_head 0
---
101c101,102
<   "acc": [
---
>   "acc": [],
>   "cands": [
103,106c104,122
<     "accident_date_after_treatment",
<     [
<      "2026-03-18"
<     ]
---
>     "history_denial",
>     6,
>     "Prior accidents? Yes [ ] No [X].",
>     1,
>     "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
>    ],
>    [
>     "history_denial",
>     6,
>     "Prior injuries? Yes [ ] No IX].",
>     1,
>     "History per patient: car accidents in 2019 and 2022 with neck and low back pain, treated with physical therapy."
>    ],
>    [
>     "history_denial",
>     6,
>     "Prior injuries? Yes [ ] No IX].",
>     1,
>     "Problem list: hypertension, type 2 diabetes, chronic low back pain."
108,109c124
<   ],
<   "cands": []
---
>   ]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:45:44.322Z

**tool call — Bash**
````
{
 "command": "cd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; python3 - <<EOF\nimport json\nd=json.load(open(\"$S/T141r2_pk_T141r2_head.json\"))\nprint(len(d))\nfor k,v in d.items():\n    if isinstance(v,dict) and v[\"acc\"]: print(k,v[\"acc\"])\nEOF"
}
````

### User / tool · 2026-11-02T13:45:44.424Z

**tool result**
````
27
sample.txt [['accident_date_after_treatment', ['2026-01-19']]]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:04.641Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141 && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_variants.py <<'EOF'\nimport sys\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import conflicts as C\ndef R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind=\"encounter\")\nINT = lambda n, d, date: R(n, d, \"Intake\", f\"Date of accident per intake form: {date}.\")\nV = [\n # (label, expected: 'conflict' | 'info', records)\n (\"V1 billing stmt before accident NAMES the collision\", \"conflict\",\n  [R(1,\"2026-01-05\",\"Hobbleton Clinic, billing statement\",\"Emergency services after motor vehicle collision. Balance forward.\"), R(2,\"2026-01-12\",\"Capital PT, visit 1\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V2 billing stmt before accident, no mechanism\", \"info\",\n  [R(1,\"2026-01-05\",\"Hobbleton Clinic, billing statement\",\"Balance forward.\"), R(2,\"2026-01-12\",\"Capital PT, visit 1\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V3 intake dated before accident, says rear-ended\", \"conflict\",\n  [R(1,\"2026-01-05\",\"Intake\",\"New patient intake. Neck pain after being rear-ended. Date of accident: 2026-01-09.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\")]),\n (\"V4 intake dated before accident, no mechanism, states date (form dated before the accident it states)\", \"info\",\n  [R(1,\"2026-01-05\",\"Intake\",\"New patient intake. Prior accidents? Yes [ ] No [X]. Date of accident: 2026-01-09.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\")]),\n (\"V5 PT note before accident: slipped and fell on ice (mechanism)\", \"conflict\",\n  [R(1,\"2026-01-05\",\"PT\",\"Slipped and fell on ice, wrist pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V6 earlier note: 'slip and fall at the store' (no 'fell')\", \"conflict\",\n  [R(1,\"2026-01-05\",\"PT\",\"Slip and fall at the grocery store, wrist pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V7 earlier note: pedestrian vs auto, neck pain\", \"conflict\",\n  [R(1,\"2026-01-05\",\"ER\",\"Pedestrian vs auto. Neck pain 7/10.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V8 earlier note: 'Neck pain since the incident, whiplash'\", \"conflict\",\n  [R(1,\"2026-01-05\",\"Chiro\",\"Neck pain since the incident. Whiplash pattern.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V9 earlier note: 'car accident last year, recovered' (history, no year digits)\", \"info\",\n  [R(1,\"2026-01-05\",\"PCP\",\"Annual physical. Reports a car accident last year, fully recovered.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V10 earlier note: 'rear-ended in March 2025' (history)\", \"info\",\n  [R(1,\"2026-01-05\",\"PCP\",\"Annual physical. Was rear-ended in March 2025, resolved.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V11 earlier ER (Dec 30 2025) 'rear-ended in December 2025', stated Jan 5\", \"conflict\",\n  [R(1,\"2025-12-30\",\"ER\",\"Rear-ended in December 2025. Neck pain.\"), R(2,\"2026-01-05\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-02-20\",\"2026-01-05\")]),\n (\"V12 earlier record is paperwork with 'vehicle' as a noun (vehicle registration form)\", \"info\",\n  [R(1,\"2026-01-05\",\"DMV\",\"Vehicle registration renewed.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V13 earlier PCP: 'hit' as verb in unrelated meaning ('hit the gym', 'hit 150 lb')\", \"info\",\n  [R(1,\"2026-01-05\",\"PCP\",\"Patient hit her weight goal of 150 lb. Annual physical.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V14 earlier PCP: 'fall' as season / 'fall risk screening'\", \"info\",\n  [R(1,\"2026-01-05\",\"PCP\",\"Annual physical. Fall risk screen negative. Flu shot given in the fall.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V15 earlier PCP: 'Previous accident' wording lowercase prior event with clause split by comma\", \"info\",\n  [R(1,\"2026-01-05\",\"PCP\",\"Annual physical, history reviewed; MVA in 2019, resolved.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V16 earlier ER same day cluster: mechanism in 2nd clause after comma, history word in 1st\", \"conflict\",\n  [R(1,\"2026-01-05\",\"ER\",\"No prior neck problems, was struck by a car while crossing the street. Neck pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V17 earlier ER: 'No history of prior injury; restrained driver, MVC' (semicolon)\", \"conflict\",\n  [R(1,\"2026-01-05\",\"ER\",\"No history of prior injury; restrained driver, MVC. Neck pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V18 earlier ER: 'no history of injury in MVC' same clause (history word, mechanism same clause)\", \"conflict\",\n  [R(1,\"2026-01-05\",\"ER\",\"MVC with no history of loss of consciousness\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n (\"V19 two records before: first benign, second collision; compare against earliest EVENT record\", \"conflict\",\n  [R(1,\"2026-01-02\",\"PCP\",\"Annual physical.\"), R(2,\"2026-01-05\",\"ER\",\"Rear-end collision. Neck pain.\"), R(3,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(4,\"2026-01-20\",\"2026-01-09\")]),\n (\"V20 record AFTER the stated date describes collision, nothing before: no record predates\", \"none\",\n  [R(1,\"2026-01-09\",\"ER\",\"Rear-end collision. Neck pain.\"), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), INT(3,\"2026-01-20\",\"2026-01-09\")]),\n]\nbad = 0\nfor label, exp, recs in V:\n    out = C.accident_date_conflicts(recs)\n    note = C.accident_date_note(recs)\n    got = \"conflict\" if out else (\"info\" if note else \"none\")\n    flag = \"\" if got == exp else \"   <<< MISMATCH\"\n    bad += bool(flag)\n    first = out[0][\"first_treatment_date\"] if out else None\n    print(f\"{got:8} exp={exp:8} | {label} | first={first} | note={note['count'] if note else None}{flag}\")\nprint(\"mismatches:\", bad)\nEOF\ncd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_variants.py $S/T141r2_head"
}
````

### User / tool · 2026-11-02T13:46:04.872Z

**tool result**
````
conflict exp=conflict | V1 billing stmt before accident NAMES the collision | first=2026-01-05 | note=None
info     exp=info     | V2 billing stmt before accident, no mechanism | first=None | note=1
conflict exp=conflict | V3 intake dated before accident, says rear-ended | first=2026-01-05 | note=None
conflict exp=info     | V4 intake dated before accident, no mechanism, states date (form dated before the accident it states) | first=2026-01-05 | note=None   <<< MISMATCH
conflict exp=conflict | V5 PT note before accident: slipped and fell on ice (mechanism) | first=2026-01-05 | note=None
info     exp=conflict | V6 earlier note: 'slip and fall at the store' (no 'fell') | first=None | note=1   <<< MISMATCH
info     exp=conflict | V7 earlier note: pedestrian vs auto, neck pain | first=None | note=1   <<< MISMATCH
info     exp=conflict | V8 earlier note: 'Neck pain since the incident, whiplash' | first=None | note=1   <<< MISMATCH
conflict exp=info     | V9 earlier note: 'car accident last year, recovered' (history, no year digits) | first=2026-01-05 | note=None   <<< MISMATCH
info     exp=info     | V10 earlier note: 'rear-ended in March 2025' (history) | first=None | note=1
info     exp=conflict | V11 earlier ER (Dec 30 2025) 'rear-ended in December 2025', stated Jan 5 | first=None | note=1   <<< MISMATCH
conflict exp=info     | V12 earlier record is paperwork with 'vehicle' as a noun (vehicle registration form) | first=2026-01-05 | note=None   <<< MISMATCH
conflict exp=info     | V13 earlier PCP: 'hit' as verb in unrelated meaning ('hit the gym', 'hit 150 lb') | first=2026-01-05 | note=None   <<< MISMATCH
info     exp=info     | V14 earlier PCP: 'fall' as season / 'fall risk screening' | first=None | note=1
info     exp=info     | V15 earlier PCP: 'Previous accident' wording lowercase prior event with clause split by comma | first=None | note=1
conflict exp=conflict | V16 earlier ER same day cluster: mechanism in 2nd clause after comma, history word in 1st | first=2026-01-05 | note=None
conflict exp=conflict | V17 earlier ER: 'No history of prior injury; restrained driver, MVC' (semicolon) | first=2026-01-05 | note=None
info     exp=conflict | V18 earlier ER: 'no history of injury in MVC' same clause (history word, mechanism same clause) | first=None | note=1   <<< MISMATCH
conflict exp=conflict | V19 two records before: first benign, second collision; compare against earliest EVENT record | first=2026-01-05 | note=None
none     exp=none     | V20 record AFTER the stated date describes collision, nothing before: no record predates | first=None | note=None
mismatches: 9
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:24.151Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; grep -n \"checks\\b\\|\\.notes\\|skipped\" app/frontend/*.js app/frontend/*.html 2>/dev/null | grep -i \"check\\|skipped\\|notes\" | head -20; ls app/frontend | head; sed -n 125,145p memory/contracts/api.md"
}
````

### User / tool · 2026-11-02T13:46:24.273Z

**tool result**
````
app/frontend/batch.js:10:  const skippedUndated = (c) => (c.undated_entries || []).concat((c.entries || []).filter((e) => !e.date)).filter((e) => (e.review_status || "pending") === "pending").length;
app/frontend/batch.js:11:  const skipText = (n) => n + (n === 1 ? " undated entry was" : " undated entries were") + " skipped: confirm the date first (Dates to confirm).";
app/frontend/batch.js:17:    const ids = eligible(c).map((e) => e.id), skipped = skippedUndated(c);
app/frontend/batch.js:18:    if (!ids.length) { if (skipped) RV.say("Nothing to accept. " + skipText(skipped)); return; }
app/frontend/batch.js:38:      RV.say("Accepted " + ids.length + " verified " + (ids.length === 1 ? "entry" : "entries") + ". Undo is available." + (skipped ? " " + skipText(skipped) : ""));
app/frontend/batch.js:79:    const n = eligible(c).length, sk = skippedUndated(c);
app/frontend/batch.js:84:      sk ? el("span", { class: "rv-help rv-blocked", "data-testid": "batch-skipped-note" }, skipText(sk)) : null,
app/frontend/judges.js:2:   each objection with its fixed-sentence reason, and where the code checks and the AI read an item differently. Every row links to the item's stepper.
app/frontend/judges.js:4:   Placement (round 2): mounted by ZL.stepper.mountCase right under the case checks, collapsed by default to ONE summary row that carries the signal
app/frontend/judges.js:13:    judge_objects: "Code checks passed, the AI objected",
app/frontend/judges.js:33:  // wrote or edited from the judge, but not from the code checks, so an edited item can lack a judge answer and be ready, or fail a code check and block. gate is null while the trace is loading.
app/frontend/judges.js:46:  // A flag the AI suggested and the checks did not confirm sits in the Could-not-verify tray: nothing can be accepted there, so the row neither shows a decision nor says "accept".
app/frontend/judges.js:155:    det.append(el("p", { class: "rv-help", "data-testid": "judge-label" }, el("strong", {}, "AI quality checks. "),
app/frontend/judges.js:157:    if (!d) { det.append(el("p", { class: "muted", role: "status" }, note || "Loading the AI checks…")); return; }
app/frontend/judges.js:167:    const verdictLine = cblk.length && gate.verdict && gate.verdict.label   // the case verdict exactly as the server words it (the same text as the case checks)
app/frontend/judges.js:190:  // Mounted right under the case checks by ZL.stepper.mountCase, so the AI-check signal sits at the top of the results.
app/frontend/flags.js:45:      return el("p", { class: "rv-note" }, "No readable date was found for this record, so it stays off the timeline and out of the gap checks.");
app/frontend/flags.js:83:  // T-142 (legal nurse, GATE-M2 major 1): "No conflicts found." read as an all-clear. The code checks a few kinds of conflict and nothing else, so the group says which, from GET case `checks`
app/frontend/flags.js:84:  // (T-141: {conflict_types, labels, not_checked}), and says the rest are not checked. With no `checks` it says that too, in fixed words that are true of every build.
app/frontend/flags.js:89:    const ch = c.checks && Array.isArray(c.checks.conflict_types) && c.checks.conflict_types.length ? c.checks : null;
api.js
app.js
audit.js
batch.js
charges.js
dev
dom.js
excerpt.js
export.js
exportcfg.js
  "counts": {"entries": 9, "amounts": 3, "flags": 1},
  "error": null, "elapsed_ms": 21540 }
```
`status`: `ingested` | `running` | `ready` | `failed`. When `failed`, `error` is `{"code": "run_deadline", "message": "..."}`; finished items are kept. Poll every second. Partial results are readable from the case endpoint while running.

## GET /api/cases/{token}
Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`. **D-053:** a `tray` item has `kind` `entry`, `amount` or `flag`. A `flag` tray item is a model-only flag the second AI check (J4) disagreed with, a code-proposed conflict the conflict check (J3) judged benign, or a conflict the model proposed that no code candidate made: it carries `flag: {type, category}`, `reasons[0]` (`JUDGE_DISAGREES`, or `LLM_ONLY` for the unconfirmed model conflict), `why` (fixed sentences, including the judge's fixed reason sentence), `attempt: {summary: <flag title>, excerpt: <quote(s), " / " between two>}` and `record_ids`. It is never in `flags`, `review.queue` or the export. Nothing the model proposes is silently dropped. **D-057 / T-126, filtered by rule:** a model proposal that a code rule filters out (today D-032 `objective_negative`: a normal finding is not a flag) is not in `tray`, `flags`, `review.queue`, the review counts, the trace gate counts or the export. It is listed in the case payload's `tray_filtered`: `{label: "Filtered by rule", collapsed: true, needs_action: false, count, rules: [{rule: "objective_negative", ref: "D-032", label, explanation, count, items: [<tray flag items, reasons[0] FILTERED_BY_RULE>]}]}` (`count: 0, rules: []` when none). The frontend shows it as a collapsed group with the count and the rule name; no action is needed. **T-110, nothing vanishes:** a record the AI extract step made no output for (`LLM_FAILED_AFTER_RETRIES`, `FIXTURE_MISS`, or `UNSUPPORTED_LANGUAGE` for a language other than English or Spanish) is a `tray` item: id `e<n>`, `kind: "entry"`, `state: "rejected"`, `reasons: [<that code>]`, the fixed `why` sentence, `attempt: {summary: null, excerpt: null}`, `ladder.failure` set, `ai_drafted: false`. It never enters `entries`, the review queue, the export or the letter; the paralegal can dismiss it or write the entry by hand (`POST .../records/{rid}/entry`, id `e<n>_m`), and a rerun that succeeds removes it. **T-110 r2:** once the record has a live entry (the hand-written one), the placeholder leaves `tray`, the `review.counts.rejected` count, the trace `in_tray` count and the export's `excluded.rejected`; its row stays for audit. The case trace `extract` step counts it in `counts.in_tray` (present only when there is one) (and in `records_without_entry` until an entry exists); the `grounding` step does not count it.

**T-141 / T-142, `checks` (GET case, top level; always present; computed per case from what the run did, no model):** what the conflict check looked for on THIS case and what it did not, so the UI can say it honestly ("Checked for: ... Not checked: ..."; never "no conflicts found" without it). `{conflict_types: [..], labels: {<type>: one plain sentence}, skipped: [{type, label, reason_code, reason, record_nos?}], not_checked: [{type, label}], notes: [{type, code, count, record_nos, stated_date, text}]}`. The four types are `plan_vs_early_end` and `denial_vs_history` (pair rules in `conflict_candidates.py`; a judge classifies each pair), `accident_date` and `provider_name` (structural checks in `conflicts.py`). **`conflict_types` lists only the types that ran on the case**; `labels` has all four. **`skipped`** says why a type did not run, or ran only in part. `reason_code`: `NOT_RUN` (case created, comparison between records not run yet; the two code checks ran at ingest), `STAGE_SKIPPED` (the run hit its time limit before the comparison between records), `RUN_FAILED` (the run stopped; nothing known), `LANGUAGE` (every record is Spanish, uncertain or unsupported: the English wording rules could not find anything; the type is absent from `conflict_types`), `LANGUAGE_PARTIAL` (the type ran, but `record_nos` lists the Spanish/uncertain/unsupported records it did not read), `NO_DATED_RECORD` (no parsed record date; `accident_date`). The language-bound types are `plan_vs_early_end`, `denial_vs_history` and `accident_date`; `provider_name` compares header labels. `not_checked` types today: `dosage`, `laterality`, `diagnosis`, `pain_score`, `treatment_duration_months`, `informant_history` (`memory/SCOPE_CUTS.md` row 13). **`notes`** are info lines, never flags: `RECORDS_PREDATE_ACCIDENT` = a single stated accident date is later than N records and none of them describes a collision or injury mechanism, so no date conflict is raised; `text` is the sentence to show ("1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; check that they are earlier care."). The decision is by content (T-141 round 2, no "a record is dated that day" shortcut): a record dated before the stated date that has a clause naming a collision, crash, MVA, vehicle, "hit", fall or similar that is not history (no prior/history word, no bare earlier year, no full date over a year earlier) makes the accident-date conflict, and the conflict then compares with the earliest such record. `denial_vs_history` reads a form field answered No ("Prior accidents? Yes [ ] No [X]." including OCR "No IX]", or "Prior injuries: None.") as a denial; the denial flag quotes the question and the checked answer together.

**T-143 (round 2), `records[].uncovered[]` (GET case; review aid, code only):** EVERY sentence of the record that no live entry's excerpt overlaps, so a pain score, a chief complaint, a baseline-history line, a patient-stated mechanism or onset ("Patient states she was struck by a car..."), an exam finding, a medication, a work-status line or an interpreter / history-source line an entry left out does not vanish silently. Each item is `{text, start, end, kinds}`: `text` the verbatim sentence (the shared splitter, over the same quotable body as `sentences[]`), `start`/`end` offsets into the case text (the same frame as `sentences[]`), `kinds` a **hint only** and possibly empty (`number`, `body_part`, `term`, `negation`); it never decides whether a sentence is listed, so the frontend must not filter on it. A form answer carries its question: `Accidentes anteriores? Si [ ] No [X].` is one item. Skipped only when the line is POSITIVELY administrative by an anchored whole-line pattern: a signature line (`Electronically signed by ...`, `Signed: ...`, `Firma de la paciente: ...`, a bare `Name, MD`), a header field (`Date of service: ...`, `Fax: ...`), a page / fax / print stamp, a billing line (a dollar figure or CPT code, a CMS-1500 item with a billing label, `Balance due.`), or a legal / cost boilerplate line without a dollar sign (`No payments posted.`, `Letter of protection requested.`, `Cost of the collar was covered.`); a line with a pain score N/10 is never skipped, and a bare word such as "adjustment", "balance" or "signed" never removes a line (any other wording of a cost or legal sentence stays listed). A duplicate record (`duplicate_of` set; the original carries the entry) and a record with no quotable body (`sentences_reason` set) give `[]`; `[]` also when nothing is left out, and the field is always present. A rejected (tray) entry covers nothing; a dismissed or pending entry does. It is never in `entries`, the review queue, the counts, the letter or the internal notes (an accepted flag may still quote its own evidence sentence in the notes, as before); the frontend may show it as "Also in this record, not in any entry" next to the record, read-only (a sentence is added to the letter only by the existing manual-entry or edit-quote routes).
```json
{
  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
  "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "records": [
    { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "unsplit": false, "preamble": false, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
      "sentences": [ {"text": "Dx: cervical strain;", "start": 396, "end": 416}, {"text": "concussion without loss of consciousness.", "start": 417, "end": 458}, {"text": "CT head negative.", "start": 459, "end": 476},
                     {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ],
      "uncovered": [] } ],
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:28.325Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; sed -n 80,130p app/frontend/flags.js | cut -c1-260; grep -rn \"skipped\\|\\.notes\" app/frontend/flags.js | head"
}
````

### User / tool · 2026-11-02T13:46:28.419Z

**tool result**
````
    return a;
  }

  // T-142 (legal nurse, GATE-M2 major 1): "No conflicts found." read as an all-clear. The code checks a few kinds of conflict and nothing else, so the group says which, from GET case `checks`
  // (T-141: {conflict_types, labels, not_checked}), and says the rest are not checked. With no `checks` it says that too, in fixed words that are true of every build.
  const FALLBACK_CHECKED = ["A stated plan of care against a later record where the course ended early", "A denial of prior problems against a prior condition, surgery or accident in another record", "A stated accident date against the dates of the records"];
  const FALLBACK_NOT = ["Left versus right across records", "A change in loss of consciousness history between records"];
  const humanType = (t) => { const s = String(t || "").replace(/_/g, " "); return s.charAt(0).toUpperCase() + s.slice(1); };
  function coverage(c, open) {
    const ch = c.checks && Array.isArray(c.checks.conflict_types) && c.checks.conflict_types.length ? c.checks : null;
    const checked = ch ? ch.conflict_types.map((t) => (ch.labels && ch.labels[t]) || humanType(t)) : FALLBACK_CHECKED;
    const not = ch ? (ch.not_checked || []).map((x) => x.label || humanType(x.type)) : FALLBACK_NOT;
    const d = el("details", { class: "rv-coverage", "data-testid": "conflict-coverage", open: open || null },
      el("summary", {}, "What the conflict check covers (" + checked.length + " kinds checked)"),
      el("p", { class: "rv-help" }, el("strong", {}, "Checked: "), "the code compares records for these kinds of conflict only."),
      el("ul", { class: "rv-cov-list" }, checked.map((t) => el("li", { "data-testid": "conflict-checked-item" }, t))),
      el("p", { class: "rv-help" }, el("strong", {}, "Not checked: "), (ch ? "anything not listed above, including these, is not looked for. Read the records for them." : "any other kind of conflict, including these. Read the records for them.")),
      not.length ? el("ul", { class: "rv-cov-list" }, not.map((t) => el("li", { "data-testid": "conflict-not-checked-item" }, t))) : null,
      ch ? null : el("p", { class: "rv-help", "data-testid": "conflict-coverage-note" }, "The server did not send its own list for this case, so this is the standing summary."));
    return d;
  }

  function render(root, c) {
    ZL.clear(root);
    root.setAttribute("data-testid", "flags-panel");
    root.setAttribute("aria-labelledby", "rv-flags-h");
    root.append(el("h2", { id: "rv-flags-h" }, "Flags"),
      el("p", { class: "rv-help" }, "Flags point to things worth checking. Accepting one means you have seen it: it goes to the internal notes, never into the letter."));
    if (c.injection && c.injection.banner) root.append(el("p", { class: "rv-banner", role: "note" }, c.injection.banner));
    if (ZL.sg) root.append(ZL.sg.dismissalBox(c));
    const flags = (c.flags || []).filter((f) => f.review_status !== "dismissed"), gone = (c.flags || []).filter((f) => f.review_status === "dismissed");
    GROUPS.forEach(([type, title, empty]) => {
      const list = RV.needsReviewFirst(flags.filter((f) => f.type === type));
      const g = el("section", { class: "rv-group", "data-group": type, "aria-labelledby": "rv-g-" + type },
        el("h3", { id: "rv-g-" + type }, title + " (" + list.length + ")"));
      if (type === "gap" && ZL.gapChanges) ZL.gapChanges.removed(c).forEach((t) => g.append(el("p", { class: "rv-gap-change", "data-testid": "gap-change-removed" }, t)));
      if (type === "conflict") {
        const dropped = gone.filter((f) => f.type === "conflict").length;
        if (!list.length) g.append(el("p", { class: "rv-empty", "data-testid": "conflict-empty" }, dropped ? "No open conflicts among the kinds checked (" + dropped + " dismissed, below). Other kinds are not checked." : "No conflicts found among the kinds chec
      } else if (!list.length) g.append(el("p", { class: "rv-empty" }, empty));
      list.forEach((f) => g.append(card(c, f)));
      if (type === "conflict") g.append(coverage(c, !list.length));
      root.append(g);
    });
    if (gone.length) root.append(RV.dismissedBox("flags", gone.length, el("div", { class: "rv-dismissed-list", "data-testid": "dismissed-flags" }, gone.map((f) => card(c, f)))));   // T-136 (pass 5 F2)
  }
  RV.registerPanel("flags", render);
  RV.renderFlags = render;
})();
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:36.356Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; cat tests/unit/test_t141_checks_per_case.py; grep -n \"deadline\" app/backend/pipeline.py | head -30"
}
````

### User / tool · 2026-11-02T13:46:36.448Z

**tool result**
````
"""T-141 round 2: GET case `checks` is computed from what THIS case ran (language routing, skipped stage, never run), not a constant."""
import pathlib

from app.backend import pipeline as PL, present
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit.test_t145_judge_not_run import Clock, _run

LIB = pathlib.Path(__file__).resolve().parents[2] / "evals" / "library"
ALL = ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"]


def _view(conn, cid):
    return present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)["checks"]


def _lib_checks(name, tmp_path):
    text = (LIB / f"{name}.txt").read_text()
    with PL._Backend("fixture"):
        conn, cid, call = PL._scratch_call(str(tmp_path), PL.IN.normalize_text(text))
        PL.run_pipeline(conn, cid, text, call=call)
        out = _view(conn, cid)
        conn.close()
    return out


def test_ingested_but_not_run_case_says_the_comparison_between_records_has_not_run(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    PL.ingest_case(conn, cid, G.raw("sample"), 0.0)
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ["accident_date", "provider_name"]
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "NOT_RUN", "denial_vs_history": "NOT_RUN"}


def test_a_finished_english_case_lists_all_four_and_skips_nothing(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ALL and ch["skipped"] == []


def test_a_run_that_hit_its_deadline_before_the_conflict_stage_says_so(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock("amounts"))              # the deadline passes as the amounts stage starts: the conflicts stage is never reached
    ch = _view(conn, cid)
    assert ch["conflict_types"] == ["accident_date", "provider_name"]
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "STAGE_SKIPPED", "denial_vs_history": "STAGE_SKIPPED"}


def test_a_run_that_died_before_the_conflict_stage_is_run_failed(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=0.0)
    _run(conn, cid, Clock())
    DB.update_case(conn, cid, status="failed")
    cfg = dict(DB.get_case(conn, cid)["config"])
    cfg["run_checks"] = dict(cfg["run_checks"], conflicts_stage="pending")      # what a crash between 'run started' and 'conflict stage done' leaves behind
    DB.update_case(conn, cid, config_json=cfg)
    ch = _view(conn, cid)
    assert {x["type"]: x["reason_code"] for x in ch["skipped"]} == {"plan_vs_early_end": "RUN_FAILED", "denial_vs_history": "RUN_FAILED"}


def test_a_mixed_language_case_names_the_records_the_english_rules_could_not_read(tmp_path):
    ch = _lib_checks("case_lib09_spanish_interpreter_espalda", tmp_path)
    sk = {x["type"]: x for x in ch["skipped"]}
    assert set(sk) == {"plan_vs_early_end", "denial_vs_history", "accident_date"}
    assert all(x["reason_code"] == "LANGUAGE_PARTIAL" and x["record_nos"] == [2, 4, 7] for x in sk.values())
    assert "provider_name" in ch["conflict_types"] and "denial_vs_history" in ch["conflict_types"]


def test_lib11_no_false_accident_date_conflict_and_the_predate_note_counts_the_annual_visit(tmp_path):
    ch = _lib_checks("case_lib11_priors_and_ledger", tmp_path)
    assert ch["skipped"] == [] and ch["conflict_types"] == ALL
    assert [n["code"] for n in ch["notes"]] == ["RECORDS_PREDATE_ACCIDENT"] and ch["notes"][0]["count"] >= 1
162:    is computed from the run, not a constant. stage: 'pending' (ingested, or the run has started), 'ran', 'skipped' (deadline before the stage)."""
230:    """T-145: an AI entry that has no judge-1 answer (the run hit its deadline before or during the stage) is recorded as judge `unavailable` with reason_code
243:    `additive` (T-146, a run that stopped at its deadline): only items with no stored row are added. A stopped run is partial, so it must not delete, downgrade or
323:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
335:        return clock() - t0 > deadline_s
376:    _mark_judge_not_run(entries, by_n)           # T-145: judge 1 did not run (deadline) -> never 'verified'
400:            if expired():                    # the deadline also applies inside the stage, record by record
442:        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:46:57.574Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; sed -n 1,60p tests/unit/test_t145_judge_not_run.py | head -70; sed -n 440,470p app/backend/pipeline.py; grep -n \"status=\\\"failed\\\"\\|'failed'\\|\\\"failed\\\"\" app/backend/pipeline.py app/backend/api.py | head; grep -n \"accident_date_phrases\" -A12 app/llm/lexicon.yaml | head -30"
}
````

### User / tool · 2026-11-02T13:46:57.691Z

**tool result**
````
"""T-145 (GATE-M2 staff blocker): an entry whose second check (judge 1) never ran is never `verified`, says JUDGE_NOT_RUN, and batch accept refuses it."""
import json

import pytest
from app.backend import case_extras, pipeline as PL, present
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script


class Clock:
    """Injected clock: jumps past the deadline when a named stage starts (on_stage), so the run stops exactly there."""
    def __init__(self, jump_at=None):
        self.t, self.jump_at = 0.0, jump_at

    def __call__(self):
        return self.t

    def on_stage(self, name):
        if name == self.jump_at:
            self.t = 10_000.0


def _case(tmp_path):
    conn = DB.connect(str(tmp_path / "d.sqlite"))
    return conn, DB.create_case(conn, G.raw("sample"), now=0.0)


def _run(conn, cid, clock):
    return PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=clock, on_stage=clock.on_stage, deadline_s=480)


@pytest.mark.parametrize("jump_at", ["extract", "verify"])      # the clock jumps as that stage starts, so the next guard (verify / judge_entries) fails
def test_deadline_before_judge1_leaves_no_verified_entry(tmp_path, jump_at):
    conn, cid = _case(tmp_path)
    out = _run(conn, cid, Clock(jump_at))
    assert out["status"] == "timeout"
    rows = DB.list_items(conn, cid, "entry")
    assert len(rows) == 9
    for r in rows:
        assert r["state"] == "needs_review" and "JUDGE_UNAVAILABLE" in r["state_reasons"], r["id"]
        jd = r["ladder"]["judge"]
        assert jd["verdict"] == "unavailable" and jd["reason_code"] == "JUDGE_NOT_RUN" and jd["call_id"] is None
        assert r["ladder"]["state"] == "needs_review"
    assert all(e["state"] == "needs_review" for e in out["entries"])
    assert out["counts"]["verified"] == 0 or all(i["state"] != "verified" for i in out["entries"])


def test_deadline_case_view_says_judge_not_run_and_never_that_the_check_agreed(tmp_path):
    conn, cid = _case(tmp_path)
    _run(conn, cid, Clock("verify"))
    for r in DB.list_items(conn, cid, "entry"):
        why = present._common(r)["why"]
        assert "JUDGE_NOT_RUN" in why and "agreed" not in why, r["id"]


def test_deadline_batch_accept_refuses_every_unjudged_entry(tmp_path):
    conn, cid = _case(tmp_path)
    _run(conn, cid, Clock("verify"))
    ids = [r["id"] for r in DB.list_items(conn, cid, "entry")]
    if timed_out:
        status = "timeout"
        err = {"code": "run_deadline", "message": "The run passed its time limit; every item from earlier runs and every decision of yours was kept unchanged."}
    else:
        status = "done_with_errors" if errors else "done"
        err = None
    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
                   run_finished_at=now_t, injection_records_json=ing["injection_records"])
    tot = TT.totals([{"cls": a["cls"], "cents": a["cents"], "review_status": a["review_status"]} for a in final_amounts])
    all_items = dated + undated + final_amounts + flag_items
    return {"status": status, "error": err, "errors": errors, "text": text, "records": recs, "entries": dated, "undated_entries": undated,
            "split_method": ing["split_method"], "split_failure": ing.get("split_failure"), "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
            "dates_to_confirm": ing["dates_to_confirm"], "injection_records": ing["injection_records"],
            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}


# ------------------------------------------------------------------ eval / API view
def case_view(out: dict) -> dict:
    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
    computed {from, to, days}. Built from a run result; the HTTP layer builds the same shape from the database."""
    flags = []
    for f in out["flags"] + out["tray"]:
        if "summary" in f:
            continue
        g = dict(f)
        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
        if f["type"] == "gap":
            g["computed"] = {"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}
        flags.append(g)
app/backend/pipeline.py:341:        DB.update_case(conn, cid, status="failed", error=json.dumps({"code": "unsupported_language", "message": "The records are not in English or Spanish."}))
app/backend/pipeline.py:446:    DB.update_case(conn, cid, status="failed" if timed_out else "ready", stage="finalize", error=json.dumps(err) if err else None,
app/backend/api.py:343:            DB.update_case(c, token, status="failed", run_finished_at=time.time(),
3:# (accident_date_phrases), the injection tag (injection) and amount classification (damages).
4-# Binding contract: memory/ORCHESTRATOR_DECISIONS.md D-013, D-018 (also D-001, D-003, D-005, D-017) and
5-# memory/DECISIONS.md ADR-008, ADR-010, ADR-011, ADR-013, ADR-014.
6-# Research basis: research/adjuster-attacks.md (attacks A1–A15, "AA src N"), research/texas-pi-notes.md,
7-# research/chronology-practice.md. Reviews addressed in round 2: reviews/T-009-legal-nurse.md and
8-# reviews/T-009-claims-adjuster.md.
9-#
10-# HOW TO USE (binding semantics)
11-# T-027 (generalization pass): patterns were widened for spinal levels (C5-6, L4-S1), "<symptom> since <year>",
12-# "may be <finding>", probable/presumed/favors, "attributes/relates ... to", and narrowed for post-accident wording
13-# (dates on/after the accident year, "secondary to the MVA", "Prior injuries? Denies."). Held-out probes live in
14-# evals/lexicon_heldout.jsonl and are never copied into `examples`; the self-check fails on any overlap and scores
15-# low-only hits as non-flags. Categories are exactly the ADR-013 closed list (the self-check asserts it).
--
1332:  accident_date_phrases:
1333-    applies_to: record_text
1334-    consumer: 'ADR-014: code extracts stated accident dates where a phrase is followed within 40 characters by a date in a listed format. A conflict arises if a stated date is later than the earliest record date, or if two different stated dates exist. Dates are never merged (D-017).'
1335-    rationale: 'The accident-date conflict (Appendix C: 2026-01-09 per EMS/ER vs "Date of accident per intake form: 2026-01-19") is the case''s headline conflict, and it must be producible without an LLM.'
1336-    source: 'ADR-014; D-017; Appendix C record 7; AA A7 (JLG Trucking)'
1337-    false_positive: '"DOA" also means "dead on arrival" and "DOI" can mean "digital object identifier". Neither is followed by a date within 40 characters, so the code rule ignores them. "Collision on I-35" is followed by a road, not a date, and is ignored for the same reason. "Injured on the job" has no date.'
1338-    entries:
1339-      - id: accident_date_label
1340-        pattern: '\b(?:date\s+of\s+(?:the\s+)?(?:accident|injury|incident|loss|collision|crash|MVA|MVC)|(?:accident|injury|incident|loss|collision|crash|MVA|MVC)\s+date|DOA|DOI|DOL|D/A|D\.O\.A\.?|D\.O\.I\.?)\b'
1341-      - id: event_on_date
1342-        pattern: '\b(?:collision|accident|crash|wreck|MVA|MVC|incident|rear-?ended|injured|hurt)\s+(?:on|dated)\b'
1343-    examples:
1344-      hit: ['Date of accident per intake form: 2026-01-19.', 'DOA: 01/09/2026', 'Date of injury 1/9/26', 'MVA on 01/09/2026', 'Collision on January 9, 2026.', 'Accident date: 2026-01-09', 'DOI 2026-01-09']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:10.396Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; ls evals/library | grep -v expected | head -30; grep -ln \"lang.*es\\|Spanish\" evals/library/*.txt | head; sed -n 1,40p tests/unit/_fakes.py | head -50"
}
````

### User / tool · 2026-11-02T13:47:10.513Z

**tool result**
````
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.txt
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
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:15.066Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; head -40 evals/library/case_lib09_spanish_interpreter_espalda.txt | cut -c1-200"
}
````

### User / tool · 2026-11-02T13:47:15.157Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-03-03
Source: Quillmere Regional ED
Excerpt: "Hx obtained via patient's son, who interpreted. Patient states she was struck by a car while walking in a parking lot. Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx:

=== Record 2 ===
Date: 14/04/2026
Source: Consultorio Médico Aguaclara, nota de consulta
Excerpt: "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo. Refiere dolor 6/10 que empeora al levantar el brazo. Niega pérdida del conocimiento. Exploración: d

=== Record 3 ===
Date: 2026-04-21
Source: Dr. Lucan Ostrowe, orthopedics, new patient
Excerpt: "Interpreter: patient's daughter. Patient states she fell in the parking lot after a car brushed her. Right shoulder pain 6/10. MRI right shoulder ordered."

=== Record 4 ===
Date: 03/05/2026
Source: Consultorio Médico Aguaclara, formulario de admisión (OCR)
Excerpt: "Fecha de ingreso: 03/O5/2026. Motivo de la visita: dolor de espaIda y hombro derecho. Accidentes anteriores? Si [ ] No [X]. Firma de la paciente: illegible."

=== Record 5 ===
Date: 2026-05-05
Source: Cinder Valley Imaging, right shoulder MRI
Excerpt: "Partial-thickness supraspinatus tear. MRI charge: $2,150."

=== Record 6 ===
Date: 2026-05-12
Source: Dr. Lucan Ostrowe, orthopedics, follow-up
Excerpt: "Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10."

=== Record 7 ===
Date: 2026-05-20
Source: Consultorio Médico Aguaclara, estado de cuenta (billing statement)
Excerpt: "Estado de cuenta: consultas $1,300.00; terapia física, 4 sesiones a $400.00 por sesión. Saldo: $2,900.00."
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:32.510Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_checks_matrix.py <<'EOF'\nimport sys, json, pathlib, tempfile\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import pipeline as PL, present, conflict_candidates as CC\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit.test_t145_judge_not_run import Clock, _run\nLIB = pathlib.Path(root) / \"evals\" / \"library\"\ntmp = pathlib.Path(tempfile.mkdtemp(prefix=\"t141r2_\"))\ndef view(conn, cid): return present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)[\"checks\"]\ndef show(label, ch):\n    sk = [(x[\"type\"], x[\"reason_code\"], x.get(\"record_nos\")) for x in ch[\"skipped\"]]\n    print(f\"{label:58} ran={ch['conflict_types']} skipped={sk} notes={[n['code'] for n in ch['notes']]}\")\ndef fresh(name):\n    conn = DB.connect(str(tmp / f\"{name}.sqlite\")); return conn\n# 1 English ingested only\nconn = fresh(\"a\"); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); PL.ingest_case(conn, cid, G.raw(\"sample\"), 0.0); show(\"S1 sample ingested only\", view(conn, cid))\n# 2 English complete\nconn = fresh(\"b\"); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); _run(conn, cid, Clock()); show(\"S2 sample complete\", view(conn, cid))\nst = DB.get_case(conn, cid)[\"status\"]; print(\"   db status after complete:\", st)\n# 3 deadline at various stages\nfor stage in [\"extract\", \"verify\", \"amounts\", \"conflicts\", \"flags\"]:\n    conn = fresh(\"c\" + stage); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); out = _run(conn, cid, Clock(stage))\n    print(\"   db status:\", DB.get_case(conn, cid)[\"status\"], out[\"status\"]); show(f\"S3 deadline when '{stage}' starts\", view(conn, cid))\n# 4 rerun-in-flight: complete case then run start marks pending, status running\nconn = fresh(\"d\"); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); _run(conn, cid, Clock())\nDB.update_case(conn, cid, status=\"running\"); cfg = dict(DB.get_case(conn, cid)[\"config\"]); cfg[\"run_checks\"] = dict(cfg[\"run_checks\"], conflicts_stage=\"pending\"); DB.update_case(conn, cid, config_json=cfg)\nshow(\"S4 re-run in flight (running, pending)\", view(conn, cid))\n# 5 legacy: complete case whose config lacks run_checks (created before this commit)\nconn = fresh(\"e\"); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); _run(conn, cid, Clock())\ncfg = dict(DB.get_case(conn, cid)[\"config\"]); cfg.pop(\"run_checks\"); DB.update_case(conn, cid, config_json=cfg or None); show(\"S5 legacy ready, no run_checks\", view(conn, cid))\nconn = fresh(\"e2\"); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0); _run(conn, cid, Clock()); DB.update_case(conn, cid, status=\"failed\")\ncfg = dict(DB.get_case(conn, cid)[\"config\"]); cfg.pop(\"run_checks\"); DB.update_case(conn, cid, config_json=cfg or None); show(\"S5b legacy failed, no run_checks\", view(conn, cid))\n# 6 Spanish partial via real pipeline\nfor lib in [\"case_lib09_spanish_interpreter_espalda\", \"case_lib11_priors_and_ledger\"]:\n    text = (LIB / f\"{lib}.txt\").read_text()\n    with PL._Backend(\"fixture\"):\n        conn, cid, call = PL._scratch_call(str(tmp / lib), PL.IN.normalize_text(text)); PL.run_pipeline(conn, cid, text, call=call)\n        show(f\"S6 {lib[:24]} complete\", view(conn, cid))\n# 7 all-Spanish synthetic\nes = \"\"\"SYNTHETIC — invented for evaluation; not real patient data\n\n=== Record 1 ===\nDate: 2026-03-03\nSource: Consultorio Médico Aguaclara, nota de consulta\nExcerpt: \"Motivo de consulta: dolor de espalda desde el atropello del 3 de marzo. Refiere dolor 6/10. Niega pérdida del conocimiento. Exploración: dolor a la palpación lumbar.\"\n\n=== Record 2 ===\nDate: 2026-03-24\nSource: Consultorio Médico Aguaclara, nota de seguimiento\nExcerpt: \"Fecha del accidente: 2026-03-24. Dolor de espalda 5/10. Se recomienda terapia física, 12 sesiones. Paciente niega lesiones previas en la espalda.\"\n\"\"\"\nwith PL._Backend(\"fixture\"):\n    conn, cid, call = PL._scratch_call(str(tmp / \"es\"), PL.IN.normalize_text(es)); \n    try: PL.run_pipeline(conn, cid, es, call=call)\n    except Exception as e: print(\"   run raised\", type(e).__name__, e)\n    c = DB.get_case(conn, cid); print(\"   status\", c[\"status\"]); show(\"S7 all-Spanish run\", view(conn, cid))\n    print(\"   langs:\", [(r[\"n\"], r.get(\"lang\")) for r in PL.IN.run_ingest(es)[\"records\"]] if hasattr(PL.IN, \"run_ingest\") else \"\")\n# 8 unit-level: checks() directly\nshow(\"U1 checks() default\", CC.checks())\nshow(\"U2 checks(None,'failed')\", CC.checks(None, \"failed\"))\nshow(\"U3 checks(None,'not_run')\", CC.checks(None, \"not_run\"))\nEOF\ncd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PYTHONHASHSEED=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_checks_matrix.py $S/T141r2_head 2>&1 | cut -c1-330"
}
````

### User / tool · 2026-11-02T13:47:33.728Z

**tool result**
````
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
S5 legacy ready, no run_checks                             ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=[]
S5b legacy failed, no run_checks                           ran=[] skipped=[('plan_vs_early_end', 'RUN_FAILED', None), ('denial_vs_history', 'RUN_FAILED', None), ('accident_date', 'RUN_FAILED', None), ('provider_name', 'RUN_FAILED', None)] notes=[]
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_checks_matrix.py", line 37, in <module>
    conn, cid, call = PL._scratch_call(str(tmp / lib), PL.IN.normalize_text(text)); PL.run_pipeline(conn, cid, text, call=call)
                      ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head/app/backend/pipeline.py", line 500, in _scratch_call
    conn = DB.connect(os.path.join(tmp, "scratch.sqlite"))
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head/app/db/db.py", line 54, in connect
    conn = sqlite3.connect(path, check_same_thread=False, isolation_level=None)  # autocommit; helpers use explicit txns
           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
sqlite3.OperationalError: unable to open database file
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:43.357Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141 && python3 - <<'EOF'\np=\"r2_checks_matrix.py\"; s=open(p).read()\ns=s.replace('PL._scratch_call(str(tmp / lib),','PL._scratch_call(str((tmp / lib).resolve().__class__(tmp / lib).mkdir() or tmp / lib),').replace('PL._scratch_call(str(tmp / \"es\"),','PL._scratch_call(str((tmp / \"es\").mkdir() or tmp / \"es\"),')\nopen(p,\"w\").write(s)\nEOF\ncd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PYTHONHASHSEED=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_checks_matrix.py $S/T141r2_head 2>&1 | sed -n '/S5b/,$p' | cut -c1-420"
}
````

### User / tool · 2026-11-02T13:47:44.926Z

**tool result**
````
S5b legacy failed, no run_checks                           ran=[] skipped=[('plan_vs_early_end', 'RUN_FAILED', None), ('denial_vs_history', 'RUN_FAILED', None), ('accident_date', 'RUN_FAILED', None), ('provider_name', 'RUN_FAILED', None)] notes=[]
S6 case_lib09_spanish_inter complete                       ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'LANGUAGE_PARTIAL', [2, 4, 7]), ('denial_vs_history', 'LANGUAGE_PARTIAL', [2, 4, 7]), ('accident_date', 'LANGUAGE_PARTIAL', [2, 4, 7])] notes=[]
S6 case_lib11_priors_and_le complete                       ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=['RECORDS_PREDATE_ACCIDENT']
   status ready
S7 all-Spanish run                                         ran=['provider_name'] skipped=[('plan_vs_early_end', 'LANGUAGE', None), ('denial_vs_history', 'LANGUAGE', None), ('accident_date', 'LANGUAGE', None)] notes=[]
   langs: 
U1 checks() default                                        ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[] notes=[]
U2 checks(None,'failed')                                   ran=[] skipped=[('plan_vs_early_end', 'RUN_FAILED', None), ('denial_vs_history', 'RUN_FAILED', None), ('accident_date', 'RUN_FAILED', None), ('provider_name', 'RUN_FAILED', None)] notes=[]
U3 checks(None,'not_run')                                  ran=['accident_date', 'provider_name'] skipped=[('plan_vs_early_end', 'NOT_RUN', None), ('denial_vs_history', 'NOT_RUN', None)] notes=[]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:47:57.106Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; sed -n 490,540p app/backend/review.py | cut -c1-240; grep -n \"run_checks\\|_store_run_checks\" -r app | grep -v \"^app/frontend\""
}
````

### User / tool · 2026-11-02T13:47:57.229Z

**tool result**
````
def _gap_change_sentence(ch: dict, seq) -> str:
    """The plain-words line the UI can announce. The numbers come from the figures in the entry, not from a model."""
    if ch["change"] == "removed":
        return f"A gap of {ch['old_days']} days no longer applies after you confirmed the date of record {seq}."
    if ch["change"] == "added":
        return f"A gap of {ch['new_days']} days now applies after you confirmed the date of record {seq}."
    return f"Gap recalculated after you confirmed record {seq}: now {ch['new_days']} days (was {ch['old_days']})."


def _recompute_gaps(conn, case_id, t, changes=None):
    """Gaps and the accident-date / provider conflicts are code over the dates: recompute them. Unchanged pair+dates keep review status
    and note; a changed one restarts as pending; one that no longer exists is dropped (ADR-002). `changes` (a list) receives the gap figures that moved (T-114)."""
    from app.backend import pipeline as PL
    before = {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}
    case = DB.get_case(conn, case_id)
    recs = store.load_records(conn, case_id, case["raw_text"])
    by_n = {r["n"]: r for r in recs}
    backend = DB.get_case(conn, case_id).get("backend") or "code"
    new = {}
    for f in gaps.gap_flags(recs) + conflicts.accident_date_conflicts(recs) + conflicts.provider_conflicts(recs):
        nos = f["record_nos"]
        state, codes = PL._compose_code(by_n, nos, list(f.get("reasons") or []), f["evidence"], case["raw_text"])
        item = {"id": f.get("id") or f"f_{f['category']}_{'_'.join(str(n) for n in nos)}", "type": f["type"], "category": f["category"],
                "origin": "code", "title": f["title"], "explanation": f["explanation"], "evidence": f["evidence"], "record_nos": nos,
                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
        for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "names", "endpoint_warnings", "conditional"):
            if k in f:
                item[k] = f[k]
        item["ladder"] = PL._ladder(item["id"], backend, {"computed_by": "code", "spans_match_input": state != "rejected"}, state)
        new[item["id"]] = item
    removed = []
    for old in DB.list_items(conn, case_id, "flag"):
        if old["origin"] != "code" or old["type"] not in ("gap", "conflict"):
            continue
        item = new.get(old["id"])
        if item is None:
            conn.execute("DELETE FROM flags WHERE id=? AND case_id=?", (old["id"], case_id))
            removed.append(old["id"])
            continue
        oc = old.get("computed") or {}
        DB.update_item(conn, old["id"], now=t, case=case_id, **PL._row("flag", item))
        if old["review_status"] != "pending" and any(oc.get(k) != item.get(k) for k in ("from_date", "to_date", "days", "stated_dates", "first_treatment_date")):
            DB.apply_review(conn, old["id"], "reset", now=t, case=case_id)
    have = {r["id"] for r in conn.execute("SELECT id FROM flags WHERE case_id=?", (case_id,))}
    for iid, item in new.items():
        if iid not in have:
            DB.add_item(conn, case_id, "flag", {"id": iid, **PL._row("flag", item)}, now=t)
    if changes is not None:
        changes.extend(_gap_changes(before, {f["id"]: _gap_figures(f) for f in DB.list_items(conn, case_id, "flag") if f["type"] == "gap"}))
    return removed
app/backend/present.py:317:            "flags": [f for f in its["flag"] if f["state"] != "rejected"], "gap_changes_removed": its["gap_changes_removed"], "checks": conflict_candidates.checks((case.get("config") or {}).get("run_checks"), "failed" if case["status"] == "failed" else "not_run" if case["status"] in ("ingested", "running") else "complete"), "tray": tray, "tray_filtered": tray_filtered, "dates_to_confirm": dates_to_confirm(conn, case_id),
app/backend/pipeline.py:160:def _store_run_checks(conn, cid: str, recs: list, stage: str) -> None:
app/backend/pipeline.py:164:    cfg["run_checks"] = CC.run_summary(recs, stage=stage)
app/backend/pipeline.py:279:    _store_run_checks(conn, cid, ing["records"], "pending")
app/backend/pipeline.py:349:    _store_run_checks(conn, cid, recs, "pending")           # a run that dies before the conflict stage leaves 'pending' (GET case: RUN_FAILED)
app/backend/pipeline.py:439:    _store_run_checks(conn, cid, recs, "ran" if conflicts_ran else "skipped")
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:48:03.396Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; grep -n \"^def confirm_date\\|^def .*confirm\" app/backend/review.py; grep -n \"def confirm_date\" -A30 app/backend/review.py | head -50 | cut -c1-200"
}
````

### User / tool · 2026-11-02T13:48:03.501Z

**tool result**
````
45:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
57:def _date_unconfirmed_error():
81:def edit_unconfirmed(kind: str, item: dict) -> bool:
397:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
450:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
397:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
398-    t = _now(now)
399-    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
400-    if row is None:
401-        raise ReviewError(404, "not_found", message="No such record.")
402-    rec = DB._decode(row)
403-    if rec["date_status"] != "ambiguous":
404-        raise _bad("Only a record whose date can be read two ways can be confirmed.")
405-    if date_iso not in (rec["date_candidates"] or []):
406-        raise ReviewError(422, "date_invalid", {"candidates": rec["date_candidates"]}, "Choose one of the readings offered for this record.")
407-    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
408-    moved, cleared = None, []
409-    for e in DB.list_items(conn, case_id, "entry"):
410-        if record_id in (e["record_ids"] or []):
411-            DB.update_item(conn, e["id"], now=t, case=case_id, date_iso=date_iso, **_without_date_doubt(e))
412-            if "DATE_AMBIGUOUS" in (e.get("state_reasons") or []):
413-                cleared.append(e["id"])
414-            moved = {"id": e["id"], "date": date_iso, "moved_from": "undated_entries"}
415-    for a in DB.list_items(conn, case_id, "amount"):
416-        if record_id in (a["record_ids"] or []) and "DATE_AMBIGUOUS" in (a.get("state_reasons") or []):
417-            DB.update_item(conn, a["id"], now=t, case=case_id, **_without_date_doubt(a))
418-            cleared.append(a["id"])
419-    removed = _drop(conn, case_id, f"f_date_r{rec['seq']}")
420-    gap_changes = []
421-    removed += _recompute_gaps(conn, case_id, t, gap_changes)
422-    for ch in gap_changes:
423-        ch["record_seq"] = rec["seq"]
424-        ch["sentence"] = _gap_change_sentence(ch, rec["seq"])
425-    # Audit: which reading the paralegal chose (and what it cleared). Written here because apply_review logs only review_status.
426-    _log_confirm_date(conn, case_id, moved["id"] if moved else record_id, rec, date_iso, cleared, t, gap_changes)
427-    enforce_ocr(conn, case_id, t)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:48:19.762Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_stale_checks.py <<'EOF'\nimport sys, pathlib, tempfile\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import pipeline as PL, present, review\nfrom app.db import db as DB\ntmp = pathlib.Path(tempfile.mkdtemp(prefix=\"t141r2s_\"))\ntext = \"\"\"SYNTHETIC — invented for evaluation; not real patient data\n\n=== Record 1 ===\nDate: 2026-03-04\nSource: Dr. A, primary care, annual visit\nExcerpt: \"Annual visit. Blood pressure 120/80. No complaints.\"\n\n=== Record 2 ===\nDate: 03/06/2026\nSource: Central ER discharge summary\nExcerpt: \"Restrained driver in a rear-end collision. Neck pain 7/10. CT head negative.\"\n\n=== Record 3 ===\nDate: 2026-03-27\nSource: Intake form\nExcerpt: \"Date of accident per intake form: 2026-03-18.\"\n\"\"\"\nconn = DB.connect(str(tmp / \"d.sqlite\")); cid = DB.create_case(conn, text, now=0.0)\nPL.ingest_case(conn, cid, text, 0.0)\ndef show(tag):\n    v = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\n    ch = v[\"checks\"]\n    print(tag, \"| notes:\", [n[\"text\"] for n in ch[\"notes\"]], \"| skipped:\", [(s[\"type\"], s[\"reason_code\"]) for s in ch[\"skipped\"] if s[\"type\"] == \"accident_date\"],\n          \"| accident-date flags:\", [f[\"category\"] for f in v[\"flags\"] if f.get(\"subtype\") == \"accident_date\" or f.get(\"category\", \"\").startswith(\"accident_date\")])\n    return v\nv = show(\"ingested\")\nrec2 = [r for r in v[\"records\"] if r[\"seq\"] == 2][0]; print(\"record 2 date_status:\", rec2[\"date_status\"], rec2[\"date_candidates\"])\nreview.confirm_date(conn, cid, rec2[\"id\"], \"2026-03-06\")\nshow(\"after confirming record 2 = 2026-03-06\")\nEOF\ncd /tmp && S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_stale_checks.py $S/T141r2_head 2>&1 | tail -12 | cut -c1-500"
}
````

### User / tool · 2026-11-02T13:48:20.157Z

**tool result**
````
ingested | notes: ['1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; check that they are earlier care.'] | skipped: [] | accident-date flags: []
record 2 date_status: ambiguous ['2026-03-06', '2026-06-03']
after confirming record 2 = 2026-03-06 | notes: ['1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; check that they are earlier care.'] | skipped: [] | accident-date flags: ['accident_date_after_treatment']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:48:28.375Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; $PY -I -m pytest tests/unit/test_conflict_candidates.py tests/unit/test_conflicts.py tests/unit/test_t093_j3_controls_reachable.py tests/unit/test_t141_checks_per_case.py tests/unit/test_t116_r4_all_dated_records.py tests/unit/test_api_routes.py -q -p no:cacheprovider 2>&1 | tail -5; (timeout 900 $PY -I -m pytest tests/unit -q -p no:cacheprovider -x -q 2>&1 | tail -5) ",
 "timeout": 1000000
}
````

### User / tool · 2026-11-02T13:48:37.690Z

**tool result**
````
tests/unit/test_api_routes.py:170: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted
1 failed, 203 passed in 8.83s
/bin/bash: timeout: command not found
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:48:42.672Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; (cd T141r2_head && $PY -I -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -16); (cd T141_head && $PY -I -m pytest tests/unit/test_api_routes.py -q -p no:cacheprovider 2>&1 | tail -3)",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T13:52:22.481Z

**tool result**
````
            r = c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
            if r.status_code == 422 and r.json()["error"]["detail"].get("reason_code") == "CHARGE_TEXT_IN_ENTRY":     # T-139: an entry whose quote cannot be narrowed is held out until re-quoted
                held.append(it["id"])
                continue
            assert r.status_code == 200
>       assert held == []                                   # T-139 narrowing: the sample's e2/e4 lose their trailing charge sentence, so nothing is held out
        ^^^^^^^^^^^^^^^^^
E       AssertionError: assert ['e2', 'e4'] == []
E         
E         Left contains 2 more items, first extra item: 'e2'
E         Use -v to get more diff

tests/unit/test_api_routes.py:170: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted
1 failed, 3799 passed, 8 skipped in 211.01s (0:03:31)
..................................                                       [100%]
34 passed in 6.75s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:52:29.198Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/T141r2_parent && git archive 68b8685~1 | tar -x -C $S/T141r2_parent && cd $S/T141r2_parent && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_api_routes.py -q -p no:cacheprovider 2>&1 | tail -3; git -C /Users/arsis/zlayt-pm-project log --oneline c4bb4da..68b8685 | head -20; git -C /Users/arsis/zlayt-pm-project show 68b8685 -- tests/unit/test_api_routes.py | head -40",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T13:52:36.452Z

**tool result**
````
..................................                                       [100%]
34 passed in 6.08s
68b8685 fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
07c7558 docs(orchestrator): D-059 letter total from one-at-a-time accepted charges with code flags
c5c18a6 feat(frontend): T-142 conflict group names the kinds checked (from GET case checks, fixed fallback) and says others are not checked; never a bare 'No conflicts found.'
4872cdb feat(frontend): T-136 r2 compared edit no longer reads Needs review; D-058 held re-picked quote says the export stays blocked and offers Write the summary; plain e2e run starts a private server with a temp ZLAYT_DB; mutant-killing tests
d19ae46 feat(backend): GET /api/cases summary list for the case overview (T-148)
5de16d3 docs(orchestrator): scope cut 13e T-132 quote edge cases
ed45b4a fix(backend): T-132 r5 extension stops only at caps labels, closed section/vitals list, bullets
78554d1 fix(backend): T-140 a total, balance, payment or adjustment line is never class charge; a charge equal to the others is a likely total; library accept-all total check
5f7ef96 fix(backend): T-139 no dollar amount reaches the carrier letter through entries; CHARGE_TEXT_IN_ENTRY holds them out; dismissed charge not under Bills to request; letter-level eval check
7d3ca35 fix(backend): T-146 a timed-out re-run keeps every previous item and decision
b604ff2 fix(backend): T-145 an entry whose judge 1 never ran is needs_review, JUDGE_NOT_RUN, and batch accept refuses it
5a388d5 fix(backend): T-143 r2 uncovered lists every sentence no entry covers; only anchored administrative lines skipped; form answer carries its question
commit 68b868575403c86cdac00d4fdc641ecd2494c613
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 07:43:47 2026 -0600

    fix(backend): T-141 r2 accident-date conflict decided by content, not a coinciding date; GET case checks computed per case
    
    A record dated before the stated accident date is a conflict only if a clause of it describes a collision or injury mechanism (per clause, history and
    model years excluded); otherwise it is an info note (checks.notes RECORDS_PREDATE_ACCIDENT). checks lists what ran: LANGUAGE / LANGUAGE_PARTIAL,
    STAGE_SKIPPED, RUN_FAILED, NOT_RUN, NO_DATED_RECORD, from the run summary stored in the case config.
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_api_routes.py b/tests/unit/test_api_routes.py
index a817ba0..4f2a4b0 100644
--- a/tests/unit/test_api_routes.py
+++ b/tests/unit/test_api_routes.py
@@ -163,11 +163,11 @@ def test_export_equals_golden_when_everything_accepted(env):
     held = []
     for it in g["entries"] + [a for a in g["amounts"] if a["kind"] == "charge"] + g["flags"]:
         r = c.post(f"/api/cases/{tok}/items/{it['id']}/review", json={"action": "accept"})
-        if r.status_code == 422 and r.json()["error"]["detail"].get("reason_code") == "CHARGE_TEXT_IN_ENTRY":     # T-139: the recorded e2/e4 state an amount; held out until re-quoted
+        if r.status_code == 422 and r.json()["error"]["detail"].get("reason_code") == "CHARGE_TEXT_IN_ENTRY":     # T-139: an entry whose quote cannot be narrowed is held out until re-quoted
             held.append(it["id"])
             continue
         assert r.status_code == 200
-    assert held == ["e2", "e4"]
+    assert held == []                                   # T-139 narrowing: the sample's e2/e4 lose their trailing charge sentence, so nothing is held out
     ex = c.get(f"/api/cases/{tok}/export").json()
     assert "$6,240" not in ex["letter_text"].split("BILLED CHARGES")[0] and "$185" not in ex["letter_text"]
     lines = ex["letter_text"].split("\n")
@@ -381,10 +381,13 @@ def test_no_409_confirm_path_for_edits_or_manual_entry_remains_d047():
 
 
 def test_t142_case_view_states_what_the_conflict_check_covers(env):
-    """T-142: GET case carries `checks` (conflict types checked, and examples not checked) so the UI can say it honestly."""
+    """T-142 / T-141 r2: GET case carries `checks` computed from the case: a created case has only the code checks, a finished English case all four."""
     _, c = env
     tok = c.post("/api/cases", json={"sample": True}).json()["token"]
     ch = c.get(f"/api/cases/{tok}").json()["checks"]
-    assert ch["conflict_types"] == ["plan_vs_early_end", "denial_vs_history", "accident_date", "provider_name"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:52:46.405Z

**tool call — Bash**
````
{
 "command": "git status --short | grep -v \"agent-memory\" | head -20"
}
````

### User / tool · 2026-11-02T13:52:46.587Z

**tool result**
````
 M app/backend/amounts.py
 M app/backend/case_extras.py
 M app/backend/flags.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/reclassify.py
 M app/backend/review.py
 M app/backend/why.py
 M app/frontend/api.js
 M app/frontend/app.js
 M app/frontend/index.html
 M app/frontend/stepper.js
 M app/frontend/switcher.js
 M app/frontend/timeline.js
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:53:08.247Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/T141r2_mut; mkdir -p $S/T141r2_mut && git archive 68b8685 | tar -x -C $S/T141r2_mut; cat > artifacts/review-evidence/T-141/r2_mutate.py <<'EOF'\nimport subprocess, sys, pathlib\nroot = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCF, CC, PLN, PR = \"app/backend/conflicts.py\", \"app/backend/conflict_candidates.py\", \"app/backend/pipeline.py\", \"app/backend/present.py\"\nmuts = [\n (CF, 'r\"t-?bone\\\\w*|side-?swip\\\\w*|run\\\\s+over|fell|', 'r\"fell|', \"N1 drop t-bone/sideswipe/run over words\"),\n (CF, \"airbag\\\\w*|seat\\\\s?belt\\\\w*|\", \"\", \"N2 drop airbag/seatbelt words\"),\n (CF, \"|hit|wreck\", \"|wreck\", \"N3 drop 'hit'\"),\n (CF, \"accident\\\\w*|vehicle|\", \"accident\\\\w*|\", \"N4 drop 'vehicle'\"),\n (CF, \"    if _HISTORICAL.search(clause):\\n        return True\", \"    if False:\\n        return True\", \"N5 history word no longer historical\"),\n (CF, \"> 365:\\n            return True\", \"> 365000:\\n            return True\", \"N6 full date >1y never historical\"),\n (CF, \"rest = _MODEL_YEAR.sub(\\\"    \\\", rest)\", \"pass\", \"N7 model year not masked\"),\n (CF, \"return any(int(y) < int(iso[:4]) for y in _YEAR.findall(rest))\", \"return False\", \"N8 bare earlier year never historical\"),\n (CF, \"_CLAUSE_SPLIT = re.compile(r\\\"[;,]|\\\\s[-\\\\u2013\\\\u2014]\\\\s|\\\\s\\\\(|\\\\)\\\")\", \"_CLAUSE_SPLIT = re.compile(r\\\"[;]\\\")\", \"N9 split only on ;\"),\n (CF, \"_CLAUSE_SPLIT = re.compile(r\\\"[;,]|\", \"_CLAUSE_SPLIT = re.compile(r\\\"[;]|\", \"N10 no comma split\"),\n (CF, \"return [o for o in records if o.get(\\\"date_iso\\\") and o[\\\"date_iso\\\"] < s[\\\"iso\\\"] and _describes_event(o, s[\\\"iso\\\"])]\", \"return [o for o in records if o.get(\\\"date_iso\\\") and o[\\\"date_iso\\\"] < s[\\\"iso\\\"]]\", \"N11 content test off (any earlier record)\"),\n (CF, \"first = min(r[\\\"date_iso\\\"] for r in _event_records(later[0], enc))\", \"pass\", \"N12 compare with earliest record, not earliest event record\"),\n (CF, \"later = [s for s in later if _event_records(s, enc)]\", \"pass\", \"N13 no content filter at all\"),\n (CF, \"    if len(distinct) < 2:\\n        later\", \"    if True:\\n        later\", \"N14 content filter also with two stated dates\"),\n (CF, \"return None\\n    iso = distinct[0]\", \"return None\\n    iso = distinct[0]; return None\", \"N15 note always None\"),\n (CF, \"or accident_date_conflicts(records):\\n        return None\", \":\\n        pass\", \"N16 note emitted even with a conflict\"),\n (CF, \"paper = [r for r in first_recs if gaps.admin_label(r)]\", \"paper = []\", \"N17 paperwork branch off\"),\n (CF, \"if d[\\\"status\\\"] == \\\"parsed\\\" and d[\\\"iso\\\"] < iso\", \"if False and d[\\\"status\\\"] == \\\"parsed\\\" and d[\\\"iso\\\"] < iso\", \"N18 full-date-before check off\"),\n (CC, \"        elif t in _PAIR_TYPES and not (stage == \\\"ran\\\" or (stage is None and state == \\\"complete\\\")):\", \"        elif False:\", \"C1 pair types never skipped\"),\n (CC, 'skip(t, \"STAGE_SKIPPED\"', 'skip(t, \"NOT_RUN\"', \"C2 STAGE_SKIPPED relabelled\"),\n (CC, \"elif t == \\\"accident_date\\\" and run.get(\\\"dated_records\\\") == 0:\", \"elif False:\", \"C3 NO_DATED_RECORD off\"),\n (CC, \"elif t in _ENGLISH_RULE_TYPES and run.get(\\\"unread\\\"):\", \"elif False:\", \"C4 language skip off\"),\n (CC, \"if run.get(\\\"read_records\\\") == 0:\", \"if False:\", \"C5 all-Spanish treated as partial\"),\n (CC, \"whole = {x[\\\"type\\\"] for x in skipped if \\\"record_nos\\\" not in x}\", \"whole = set()\", \"C6 conflict_types ignores whole skips\"),\n (CC, \"if lang != \\\"en\\\":\", \"if lang not in ('en', 'uncertain'):\", \"C7 uncertain counted as read\"),\n (CC, \"if state == \\\"failed\\\" and not known:\", \"if False:\", \"C8 failed w/o summary claims all ran\"),\n (PLN, \"\\\"ran\\\" if conflicts_ran else \\\"skipped\\\"\", \"\\\"ran\\\"\", \"P1 stage always ran (deadline)\"),\n (PLN, \"    _store_run_checks(conn, cid, recs, \\\"pending\\\")           #\", \"    pass           #\", \"P2 no pending at run start\"),\n (PLN, \"    _store_run_checks(conn, cid, ing[\\\"records\\\"], \\\"pending\\\")\\n\", \"\", \"P3 no summary at ingest\"),\n (PR, \"\\\"failed\\\" if case[\\\"status\\\"] == \\\"failed\\\" else \\\"not_run\\\" if case[\\\"status\\\"] in (\\\"ingested\\\", \\\"running\\\") else \\\"complete\\\"\", \"\\\"complete\\\"\", \"R1 state always complete\"),\n]\ntests = [\"tests/unit/test_conflicts.py\", \"tests/unit/test_conflict_candidates.py\", \"tests/unit/test_t141_checks_per_case.py\", \"tests/unit/test_t116_r4_all_dated_records.py\", \"tests/unit/test_api_routes.py\", \"tests/unit/test_t093_j3_controls_reachable.py\"]\nfor rel, old, new, label in muts:\n    p = root / rel; src = p.read_text()\n    if old not in src: print(\"SKIP (pattern not found)\", label); continue\n    p.write_text(src.replace(old, new, 1))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", *tests, \"-q\", \"-p\", \"no:cacheprovider\", \"--deselect\", \"tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted\"], cwd=root, capture_output=True, text=True)\n    p.write_text(src)\n    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), label, \"|\", tail[:100], flush=True)\nEOF\necho ok"
}
````

### User / tool · 2026-11-02T13:53:08.322Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; rm -rf $S/T141r2_mut; mkdir -p $S/T141r2_mut && git archive 68b8685 has been denied.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:53:12.713Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -d $S/T141r2_mut2 2>&1 | head -1; mkdir $S/T141r2_mut2 && git archive 68b8685 | tar -x -C $S/T141r2_mut2 && ls $S/T141r2_mut2 | wc -l"
}
````

### User / tool · 2026-11-02T13:53:13.357Z

**tool result**
````
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_mut2: No such file or directory
      17
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:53:24.601Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_mutate.py",
 "content": "import subprocess, sys, pathlib\nroot = pathlib.Path(sys.argv[1]); PY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCF, CC, PLN, PR = \"app/backend/conflicts.py\", \"app/backend/conflict_candidates.py\", \"app/backend/pipeline.py\", \"app/backend/present.py\"\nmuts = [\n (CF, 'r\"t-?bone\\\\w*|side-?swip\\\\w*|run\\\\s+over|fell|', 'r\"fell|', \"N1 drop t-bone/sideswipe/run over words\"),\n (CF, \"airbag\\\\w*|seat\\\\s?belt\\\\w*|\", \"\", \"N2 drop airbag/seatbelt words\"),\n (CF, \"|hit|wreck\", \"|wreck\", \"N3 drop 'hit'\"),\n (CF, \"accident\\\\w*|vehicle|\", \"accident\\\\w*|\", \"N4 drop 'vehicle'\"),\n (CF, \"    if _HISTORICAL.search(clause):\\n        return True\", \"    if False:\\n        return True\", \"N5 history word no longer historical\"),\n (CF, \"> 365:\\n            return True\", \"> 365000:\\n            return True\", \"N6 full date >1y never historical\"),\n (CF, \"rest = _MODEL_YEAR.sub(\\\"    \\\", rest)\", \"pass\", \"N7 model year not masked\"),\n (CF, \"return any(int(y) < int(iso[:4]) for y in _YEAR.findall(rest))\", \"return False\", \"N8 bare earlier year never historical\"),\n (CF, \"_CLAUSE_SPLIT = re.compile(r\\\"[;,]|\\\\s[-\\\\u2013\\\\u2014]\\\\s|\\\\s\\\\(|\\\\)\\\")\", \"_CLAUSE_SPLIT = re.compile(r\\\"[;]\\\")\", \"N9 split only on ;\"),\n (CF, \"_CLAUSE_SPLIT = re.compile(r\\\"[;,]|\", \"_CLAUSE_SPLIT = re.compile(r\\\"[;]|\", \"N10 no comma split\"),\n (CF, \"return [o for o in records if o.get(\\\"date_iso\\\") and o[\\\"date_iso\\\"] < s[\\\"iso\\\"] and _describes_event(o, s[\\\"iso\\\"])]\", \"return [o for o in records if o.get(\\\"date_iso\\\") and o[\\\"date_iso\\\"] < s[\\\"iso\\\"]]\", \"N11 content test off (any earlier record)\"),\n (CF, \"first = min(r[\\\"date_iso\\\"] for r in _event_records(later[0], enc))\", \"pass\", \"N12 compare with earliest record, not earliest event record\"),\n (CF, \"later = [s for s in later if _event_records(s, enc)]\", \"pass\", \"N13 no content filter at all\"),\n (CF, \"    if len(distinct) < 2:\\n        later\", \"    if True:\\n        later\", \"N14 content filter also with two stated dates\"),\n (CF, \"return None\\n    iso = distinct[0]\", \"return None\\n    iso = distinct[0]; return None\", \"N15 note always None\"),\n (CF, \"or accident_date_conflicts(records):\\n        return None\", \":\\n        pass\", \"N16 note emitted even with a conflict\"),\n (CF, \"paper = [r for r in first_recs if gaps.admin_label(r)]\", \"paper = []\", \"N17 paperwork branch off\"),\n (CF, \"if d[\\\"status\\\"] == \\\"parsed\\\" and d[\\\"iso\\\"] < iso\", \"if False and d[\\\"status\\\"] == \\\"parsed\\\" and d[\\\"iso\\\"] < iso\", \"N18 full-date-before check off\"),\n (CC, \"        elif t in _PAIR_TYPES and not (stage == \\\"ran\\\" or (stage is None and state == \\\"complete\\\")):\", \"        elif False:\", \"C1 pair types never skipped\"),\n (CC, 'skip(t, \"STAGE_SKIPPED\"', 'skip(t, \"NOT_RUN\"', \"C2 STAGE_SKIPPED relabelled\"),\n (CC, \"elif t == \\\"accident_date\\\" and run.get(\\\"dated_records\\\") == 0:\", \"elif False:\", \"C3 NO_DATED_RECORD off\"),\n (CC, \"elif t in _ENGLISH_RULE_TYPES and run.get(\\\"unread\\\"):\", \"elif False:\", \"C4 language skip off\"),\n (CC, \"if run.get(\\\"read_records\\\") == 0:\", \"if False:\", \"C5 all-Spanish treated as partial\"),\n (CC, \"whole = {x[\\\"type\\\"] for x in skipped if \\\"record_nos\\\" not in x}\", \"whole = set()\", \"C6 conflict_types ignores whole skips\"),\n (CC, \"if lang != \\\"en\\\":\", \"if lang not in ('en', 'uncertain'):\", \"C7 uncertain counted as read\"),\n (CC, \"if state == \\\"failed\\\" and not known:\", \"if False:\", \"C8 failed w/o summary claims all ran\"),\n (PLN, \"\\\"ran\\\" if conflicts_ran else \\\"skipped\\\"\", \"\\\"ran\\\"\", \"P1 stage always ran (deadline)\"),\n (PLN, \"    _store_run_checks(conn, cid, recs, \\\"pending\\\")           #\", \"    pass           #\", \"P2 no pending at run start\"),\n (PLN, \"    _store_run_checks(conn, cid, ing[\\\"records\\\"], \\\"pending\\\")\\n\", \"\", \"P3 no summary at ingest\"),\n (PR, \"\\\"failed\\\" if case[\\\"status\\\"] == \\\"failed\\\" else \\\"not_run\\\" if case[\\\"status\\\"] in (\\\"ingested\\\", \\\"running\\\") else \\\"complete\\\"\", \"\\\"complete\\\"\", \"R1 state always complete\"),\n]\ntests = [\"tests/unit/test_conflicts.py\", \"tests/unit/test_conflict_candidates.py\", \"tests/unit/test_t141_checks_per_case.py\", \"tests/unit/test_t116_r4_all_dated_records.py\", \"tests/unit/test_api_routes.py\", \"tests/unit/test_t093_j3_controls_reachable.py\"]\nfor rel, old, new, label in muts:\n    p = root / rel; src = p.read_text()\n    if old not in src: print(\"SKIP (pattern not found)\", label); continue\n    p.write_text(src.replace(old, new, 1))\n    r = subprocess.run([PY, \"-I\", \"-m\", \"pytest\", *tests, \"-q\", \"-p\", \"no:cacheprovider\", \"--deselect\", \"tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted\"], cwd=root, capture_output=True, text=True)\n    p.write_text(src)\n    tail = [l for l in r.stdout.splitlines() if l.strip()][-1]\n    print((\"KILLED  \" if r.returncode else \"SURVIVED\"), label, \"|\", tail[:100], flush=True)\n"
}
````

### User / tool · 2026-11-02T13:53:24.696Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_mutate.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:53:28.606Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_mutate.py $S/T141r2_mut2 2>&1 | tee $S/T141r2_mutants.txt",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T13:57:35.681Z

**tool result**
````
SURVIVED N1 drop t-bone/sideswipe/run over words | 203 passed, 1 deselected in 8.02s
SURVIVED N2 drop airbag/seatbelt words | 203 passed, 1 deselected in 7.43s
SURVIVED N3 drop 'hit' | 203 passed, 1 deselected in 7.65s
SURVIVED N4 drop 'vehicle' | 203 passed, 1 deselected in 8.02s
KILLED   N5 history word no longer historical | 1 failed, 202 passed, 1 deselected in 7.81s
SURVIVED N6 full date >1y never historical | 203 passed, 1 deselected in 7.90s
KILLED   N7 model year not masked | 1 failed, 202 passed, 1 deselected in 7.40s
KILLED   N8 bare earlier year never historical | 1 failed, 202 passed, 1 deselected in 7.71s
KILLED   N9 split only on ; | 1 failed, 202 passed, 1 deselected in 8.47s
KILLED   N10 no comma split | 1 failed, 202 passed, 1 deselected in 7.99s
KILLED   N11 content test off (any earlier record) | 8 failed, 195 passed, 1 deselected in 7.51s
KILLED   N12 compare with earliest record, not earliest event record | 2 failed, 201 passed, 1 deselected in 7.98s
KILLED   N13 no content filter at all | 6 failed, 197 passed, 1 deselected in 7.90s
SURVIVED N14 content filter also with two stated dates | 203 passed, 1 deselected in 7.53s
KILLED   N15 note always None | 5 failed, 198 passed, 1 deselected in 8.13s
KILLED   N16 note emitted even with a conflict | 12 failed, 191 passed, 1 deselected in 6.69s
KILLED   N17 paperwork branch off | 3 failed, 200 passed, 1 deselected in 7.78s
SURVIVED N18 full-date-before check off | 203 passed, 1 deselected in 7.43s
KILLED   C1 pair types never skipped | 5 failed, 198 passed, 1 deselected in 7.21s
KILLED   C2 STAGE_SKIPPED relabelled | 2 failed, 201 passed, 1 deselected in 8.64s
KILLED   C3 NO_DATED_RECORD off | 1 failed, 202 passed, 1 deselected in 7.80s
KILLED   C4 language skip off | 3 failed, 200 passed, 1 deselected in 7.92s
KILLED   C5 all-Spanish treated as partial | 1 failed, 202 passed, 1 deselected in 7.58s
KILLED   C6 conflict_types ignores whole skips | 6 failed, 197 passed, 1 deselected in 7.76s
SURVIVED C7 uncertain counted as read | 203 passed, 1 deselected in 8.35s
KILLED   C8 failed w/o summary claims all ran | 1 failed, 202 passed, 1 deselected in 7.78s
KILLED   P1 stage always ran (deadline) | 1 failed, 202 passed, 1 deselected in 7.99s
SURVIVED P2 no pending at run start | 203 passed, 1 deselected in 8.60s
SURVIVED P3 no summary at ingest | 203 passed, 1 deselected in 7.78s
KILLED   R1 state always complete | 1 failed, 202 passed, 1 deselected in 8.01s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:57:58.026Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_real_crash.py <<'EOF'\nimport sys, tempfile, pathlib\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import pipeline as PL, present\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit.test_t145_judge_not_run import Clock, _run\nfrom tests.unit._fakes import FakeCall, sample_script\ntmp = pathlib.Path(tempfile.mkdtemp(prefix=\"t141r2c_\"))\nconn = DB.connect(str(tmp / \"d.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=0.0)\n_run(conn, cid, Clock())                                   # first run completes\ndef chk():\n    ch = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)[\"checks\"]\n    return ch[\"conflict_types\"], [(s[\"type\"], s[\"reason_code\"]) for s in ch[\"skipped\"]]\nprint(\"after first run :\", chk())\norig = PL.FL.run_conflict_pass\ndef boom(*a, **k): raise RuntimeError(\"simulated crash inside the conflict stage\")\nPL.FL.run_conflict_pass = boom\ntry:\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script()), now=Clock(), deadline_s=480)\nexcept RuntimeError as e:\n    print(\"re-run raised:\", e)\nDB.update_case(conn, cid, status=\"failed\")                  # what api.py:343 does on an escaped exception\nprint(\"after crashed re-run:\", chk())\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_real_crash.py $S/T141r2_head 2>&1 | tail -5; echo \"--- with P2 mutant (no pending at run start)\"; cp $S/T141r2_mut2/app/backend/pipeline.py $S/T141r2_pl_orig.py; python3 - <<EOF\nimport pathlib\np=pathlib.Path(\"$S/T141r2_mut2/app/backend/pipeline.py\"); s=p.read_text()\np.write_text(s.replace('    _store_run_checks(conn, cid, recs, \"pending\")           #','    pass           #',1))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_real_crash.py $S/T141r2_mut2 2>&1 | tail -4; cp $S/T141r2_pl_orig.py $S/T141r2_mut2/app/backend/pipeline.py; diff -q $S/T141r2_mut2/app/backend/pipeline.py $S/T141r2_head/app/backend/pipeline.py && echo restored"
}
````

### User / tool · 2026-11-02T13:57:59.782Z

**tool result**
````
after first run : (['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'], [])
re-run raised: simulated crash inside the conflict stage
after crashed re-run: (['accident_date', 'provider_name'], [('plan_vs_early_end', 'RUN_FAILED'), ('denial_vs_history', 'RUN_FAILED')])
--- with P2 mutant (no pending at run start)
after first run : (['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'], [])
re-run raised: simulated crash inside the conflict stage
after crashed re-run: (['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'], [])
restored
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:22.083Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_variants2.py <<'EOF'\nimport sys\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import conflicts as C\ndef R(n, d, src, ex): return dict(n=n, date_iso=d, source=src, excerpt=ex, kind=\"encounter\")\ndef case(first_text, src=\"PCP\"): return [R(1,\"2026-01-05\",src,first_text), R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"), R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")]\nV = [\n (\"W1 PCP annual: 'Denies any accidents or falls.'\", \"info\", case(\"Annual physical. Denies any accidents or falls.\")),\n (\"W2 PCP annual: 'No recent accidents or injuries.'\", \"info\", case(\"Annual physical. No recent accidents or injuries.\")),\n (\"W3 ER: 'Healthy prior to the rear-end collision. Neck pain since.'\", \"conflict\", case(\"Healthy prior to the rear-end collision. Neck pain since.\", \"ER\")),\n (\"W4 ER: 'Previously asymptomatic until the motor vehicle collision.'\", \"conflict\", case(\"Previously asymptomatic until the motor vehicle collision.\", \"ER\")),\n (\"W5 ER: 'MVC with no history of LOC.'\", \"conflict\", case(\"MVC with no history of LOC.\", \"ER\")),\n (\"W6 Billing before accident: 'Services after MVA of 03/04/2024' (old full date, history)\", \"info\", case(\"Statement. Prior balance from MVA of 03/04/2024.\", \"Clinic billing statement\")),\n (\"W7 PCP: 'MVA on 03/04/2024, resolved' (full date >1y, no history word)\", \"info\", case(\"Annual physical. MVA on 03/04/2024, resolved.\")),\n (\"W8 Insurance card: 'Auto insurance card on file; vehicle: 2019 Honda' (model year)\", \"info\", case(\"Registration. Auto insurance card on file; vehicle: 2019 Honda Civic.\", \"Intake\")),\n (\"W9 PCP: 'Patient hit by a car 2 days ago' (true event)\", \"conflict\", case(\"Patient hit by a car 2 days ago. Neck pain.\")),\n (\"W10 PCP: 'rear-ended' plus 'Date of accident' absent, hyphen clause 'rear-ended - resolved 2021' (year in 2nd clause)\", \"info\", case(\"Annual physical - rear-ended in 2021, resolved.\")),\n]\nbad=0\nfor label, exp, recs in V:\n    out = C.accident_date_conflicts(recs); note = C.accident_date_note(recs)\n    got = \"conflict\" if out else (\"info\" if note else \"none\"); flag = \"\" if got == exp else \"   <<< MISMATCH\"; bad += bool(flag)\n    print(f\"{got:8} exp={exp:8} | {label}{flag}\")\nprint(\"mismatches:\", bad)\nfor label, recs in [(\"V1-like\", [R(1,\"2026-01-05\",\"Hobbleton Clinic, billing statement\",\"Emergency services after motor vehicle collision. Balance forward.\"), R(2,\"2026-01-12\",\"Capital PT, visit 1\",\"Exam: ok.\"), R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")])]:\n    print(C.accident_date_conflicts(recs)[0][\"explanation\"])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_variants2.py $S/T141r2_head"
}
````

### User / tool · 2026-11-02T13:58:22.440Z

**tool result**
````
conflict exp=info     | W1 PCP annual: 'Denies any accidents or falls.'   <<< MISMATCH
conflict exp=info     | W2 PCP annual: 'No recent accidents or injuries.'   <<< MISMATCH
info     exp=conflict | W3 ER: 'Healthy prior to the rear-end collision. Neck pain since.'   <<< MISMATCH
info     exp=conflict | W4 ER: 'Previously asymptomatic until the motor vehicle collision.'   <<< MISMATCH
info     exp=conflict | W5 ER: 'MVC with no history of LOC.'   <<< MISMATCH
info     exp=info     | W6 Billing before accident: 'Services after MVA of 03/04/2024' (old full date, history)
conflict exp=info     | W7 PCP: 'MVA on 03/04/2024, resolved' (full date >1y, no history word)   <<< MISMATCH
conflict exp=info     | W8 Insurance card: 'Auto insurance card on file; vehicle: 2019 Honda' (model year)   <<< MISMATCH
conflict exp=conflict | W9 PCP: 'Patient hit by a car 2 days ago' (true event)
info     exp=info     | W10 PCP: 'rear-ended' plus 'Date of accident' absent, hyphen clause 'rear-ended - resolved 2021' (year in 2nd clause)
mismatches: 7
Stated accident date January 9, 2026 (“Date of accident per intake form: 2026-01-09”) is later than the earliest recorded date, January 5, 2026 (record 1: Hobbleton Clinic, billing statement), which looks like paperwork, not a visit. The records disagree; the tool does not choose between them. If record 1: Hobbleton Clinic, billing statement is paperwork, not a visit, the first recorded visit is January 12, 2026 (record 2: Capital PT, visit 1), and the stated date is not later than it. Check when treatment actually began before relying on this comparison.
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:44.869Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sys; sys.path.insert(0,\"$S/T141r2_head\")\nfrom app.backend import conflicts as C, dates\ndef R(n,d,s,e): return dict(n=n,date_iso=d,source=s,excerpt=e,kind=\"encounter\")\nfor t in [\"Annual physical. MVA on 03/14/2024, resolved.\",\"Annual physical. MVA on 03/04/2024, resolved.\",\"Annual physical. MVA on March 4, 2024, resolved.\",\"Annual physical. MVA 2024-03-04, resolved.\"]:\n    recs=[R(1,\"2026-01-05\",\"PCP\",t),R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"),R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")]\n    print(\"conflict\" if C.accident_date_conflicts(recs) else \"info/none\", \"|\", t, \"|\", [(d[\"text\"],d[\"status\"]) for d in dates.find_dates(t)])\nEOF\ncd $S/T141r2_mut2 && python3 - <<EOF\nimport pathlib,subprocess\np=pathlib.Path(\"app/backend/conflicts.py\"); s=p.read_text()\np.write_text(s.replace(\"|hit|wreck\",\"|wreck\",1).replace(\"accident\\\\\\\\w*|vehicle|\",\"accident\\\\\\\\w*|\",1))\nr=subprocess.run([\"/Users/arsis/zlayt-pm-project/.venv/bin/python\",\"-I\",\"-m\",\"pytest\",\"tests/unit/test_conflicts.py\",\"tests/unit/test_t116_r4_all_dated_records.py\",\"-q\",\"-p\",\"no:cacheprovider\"],capture_output=True,text=True)\nprint(\"both hit+vehicle dropped:\", r.stdout.strip().splitlines()[-1])\np.write_text(s)\nEOF\ndiff -q $S/T141r2_mut2/app/backend/conflicts.py $S/T141r2_head/app/backend/conflicts.py && echo restored"
}
````

### User / tool · 2026-11-02T13:58:46.583Z

**tool result**
````
conflict | Annual physical. MVA on 03/14/2024, resolved. | [('03/14/2024', 'parsed')]
conflict | Annual physical. MVA on 03/04/2024, resolved. | [('03/04/2024', 'ambiguous')]
conflict | Annual physical. MVA on March 4, 2024, resolved. | [('March 4, 2024', 'parsed')]
info/none | Annual physical. MVA 2024-03-04, resolved. | [('2024-03-04', 'parsed')]
both hit+vehicle dropped: 1 failed, 53 passed in 1.22s
restored
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:58:57.631Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF\nimport sys; sys.path.insert(0,\"$S/T141r2_head\")\nfrom app.backend import conflicts as C, dates, sentences\nt=\"Annual physical. MVA on 03/14/2024, resolved.\"\nrec=dict(n=1,date_iso=\"2026-01-05\",source=\"PCP\",excerpt=t)\nprint([t[a:b] for a,b in sentences.stripped_spans(t)])\nfor a,b in sentences.stripped_spans(t):\n    u=t[a:b]\n    for d in dates.find_dates(u): u=u[:d[\"start\"]]+d[\"text\"].replace(\",\",\"\\x01\")+u[d[\"end\"]:]\n    for c in (x.replace(\"\\x01\",\",\") for x in C._CLAUSE_SPLIT.split(u)):\n        print(repr(c), C._EVENT.search(c) is not None, C._historical(c,\"2026-01-09\"))\nEOF"
}
````

### User / tool · 2026-11-02T13:58:57.832Z

**tool result**
````
['Annual physical.', 'MVA on 03/14/2024, resolved.']
'Annual physical.' False False
'MVA on 03/14/2024' True True
' resolved.' False False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:17.274Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; $PY -I -m evals.library_report --help 2>&1 | head -15"
}
````

### User / tool · 2026-11-02T13:59:17.380Z

**tool result**
````
/Users/arsis/zlayt-pm-project/.venv/bin/python: Error while finding module specification for 'evals.library_report' (ModuleNotFoundError: No module named 'evals')
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:20.903Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; ls evals | head -30; PYTHONPATH=. $PY -m evals.library_report --help 2>&1 | head -12"
}
````

### User / tool · 2026-11-02T13:59:21.102Z

**tool result**
````
__init__.py
__pycache__
adversarial
golden
heldout_audit.py
j3_controls.py
letter_check.py
lexicon_heldout.jsonl
library
library_build_v2.py
library_report.py
matching.py
reports
run.py
usage: python -m evals.library_report [-h] [--out OUT]

options:
  -h, --help  show this help message and exit
  --out OUT
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:26.051Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_head; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; ZLAYT_MODE=local PYTHONPATH=. $PY -m evals.library_report --out ../T141r2_libreport.json 2>&1 | tail -5; $PY -I - <<'EOF'\nimport json\nd=json.load(open(\"../T141r2_libreport.json\"))\nprint(type(d), list(d)[:8] if isinstance(d,dict) else len(d))\ncases = d.get(\"cases\") or d\nfor c in (cases if isinstance(cases,list) else cases.values()):\n    if \"lib11\" in json.dumps(c)[:200]:\n        print(json.dumps({k:v for k,v in c.items() if k in (\"case\",\"must_flags\",\"must_not_flag_hits\",\"must_hits\",\"must\",\"must_not\")}, default=str)[:900]); print(list(c)[:20])\nEOF",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T13:59:28.107Z

**tool result (error)**
````
Exit code 1
| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
Traceback (most recent call last):
  File "<stdin>", line 2, in <module>
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 293, in load
    return loads(fp.read(),
           ^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/__init__.py", line 346, in loads
    return _default_decoder.decode(s)
           ^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 337, in decode
    obj, end = self.raw_decode(s, idx=_w(s, 0).end())
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  File "/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/json/decoder.py", line 355, in raw_decode
    raise JSONDecodeError("Expecting value", s, err.value) from None
json.decoder.JSONDecodeError: Expecting value: line 1 column 1 (char 0)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:32.531Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; grep -n \"lib11\" T141r2_libreport.json | head -12 | cut -c1-300; grep -n \"must_not\\|must flags\\|N2\\|accident\" T141r2_libreport.json | grep -i lib11 | head | cut -c1-300"
}
````

### User / tool · 2026-11-02T13:59:32.653Z

**tool result**
````
19:| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | True | ok | 4/4 | 0 | - | 0 | - |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T13:59:40.739Z

**tool call — Bash**
````
{
 "command": "cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_lib11.py <<'EOF'\nimport sys, pathlib, tempfile\nroot = sys.argv[1]; sys.path.insert(0, root)\nfrom app.backend import pipeline as PL, present\ntmp = pathlib.Path(tempfile.mkdtemp(prefix=\"t141r2l_\"))\ntext = (pathlib.Path(root) / \"evals/library/case_lib11_priors_and_ledger.txt\").read_text()\nwith PL._Backend(\"fixture\"):\n    conn, cid, call = PL._scratch_call(str(tmp), PL.IN.normalize_text(text)); PL.run_pipeline(conn, cid, text, call=call)\n    v = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\nfor f in v[\"flags\"]:\n    if f[\"type\"] == \"conflict\": print(\"CONFLICT\", f[\"category\"], f[\"state\"], \"|\", f[\"title\"][:90], \"| records\", f.get(\"record_nos\"))\nprint(\"accident-date flags:\", [f[\"category\"] for f in v[\"flags\"] if str(f.get(\"category\")).startswith(\"accident_date\")])\nch = v[\"checks\"]; print(\"checks types:\", ch[\"conflict_types\"], \"skipped:\", ch[\"skipped\"], \"notes:\", [n[\"text\"] for n in ch[\"notes\"]])\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; ZLAYT_MODE=local /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_lib11.py $S/T141r2_head 2>&1 | tail -6 | cut -c1-400",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T13:59:41.436Z

**tool result**
````
CONFLICT other_fact_mismatch verified | Records differ on a fact | records None
CONFLICT other_fact_mismatch verified | Records differ on a fact | records None
accident-date flags: []
checks types: ['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped: [] notes: ['1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; check that they are earlier care.']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:00:50.330Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py list 2>/dev/null | grep -i \"skipped\\|notes\\[\\]\\|T-142\\|checks\" | head; python3 tools/board.py list --status ready 2>/dev/null | head -12; python3 tools/board.py list --status in_review 2>/dev/null | grep -i \"142\\|141\""
}
````

### User / tool · 2026-11-02T14:00:50.677Z

**tool result**
````
T-098	M3	backend    	done             	P1	AC 1/1	Export gate must block human-edited items whose code checks fail (D-045b: exempt from judge, not from code checks)
T-142	M2	frontend   	blocked          	P1	AC 1/1	GATE-M2 major (legal nurse): conflict empty state overclaims ('No conflicts found') though only plan-vs-early-end and denial-vs-history are checked; laterality (lib09 L vs R shoulder) and LOC (lib08) contradictions are not
T-151	M2	frontend   	ready            	P1	AC 0/1	UI: render checks.skipped[] (why a check did not run for this case) and checks.notes[] ('N records predate the stated accident date') in the Conflicts group (T-141 r2 follow-up to T-142)
T-147	M3	backend    	ready            	P1	AC 0/1	Perf: flags._hedge_run is quadratic when many hits share one huge unit (24k-char attribution chain takes ~11 s); add a per-unit memo
T-151	M2	frontend   	ready            	P1	AC 0/1	UI: render checks.skipped[] (why a check did not run for this case) and checks.notes[] ('N records predate the stated accident date') in the Conflicts group (T-141 r2 follow-up to T-142)
T-141	M2	backend    	in_review        	P1	AC 1/1	GATE-M2 major: lib11 intake 'Prior accidents: No' vs PCP note listing 2019/2022 accidents not flagged as a conflict; a false accident-date 'records disagree' conflict is shown instead
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:01:02.790Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /tmp; for f in r2_variants2 ; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/$f.py $S/T141_head 2>&1 | head -12 | cut -c1-120; done; echo ----V1; /Users/arsis/zlayt-pm-project/.venv/bin/python -I - <<EOF 2>&1 | tail -3\nimport sys; sys.path.insert(0,\"$S/T141_head\")\nfrom app.backend import conflicts as C\ndef R(n,d,s,e): return dict(n=n,date_iso=d,source=s,excerpt=e,kind=\"encounter\")\nINT=R(3,\"2026-01-20\",\"Intake\",\"Date of accident per intake form: 2026-01-09.\")\nfor lab,t in [(\"V9\",\"Annual physical. Reports a car accident last year, fully recovered.\"),(\"V12\",\"Vehicle registration renewed.\"),(\"V13\",\"Patient hit her weight goal of 150 lb. Annual physical.\")]:\n    print(lab,\"conflict\" if C.accident_date_conflicts([R(1,\"2026-01-05\",\"PCP\",t),R(2,\"2026-01-12\",\"PT\",\"Exam: ok.\"),INT]) else \"none\")\nEOF"
}
````

### User / tool · 2026-11-02T14:01:03.292Z

**tool result**
````
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/r2_variants2.py", line 20, in <module>
    out = C.accident_date_conflicts(recs); note = C.accident_date_note(recs)
                                                  ^^^^^^^^^^^^^^^^^^^^
AttributeError: module 'app.backend.conflicts' has no attribute 'accident_date_note'. Did you mean: 'accident_date_confl
----V1
V9 conflict
V12 conflict
V13 conflict
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:05.880Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md",
 "content": "# T-141 staff-engineer review, round 2 (68b8685), Marcus Lee persona\n\nVerdict: **changes** (0 blockers, 2 major, 4 minor). Everything I asked for in round 1 moved: my six accident-date variants (B, C, D, F, G and the plain E) all conflict now, lib11 still gives exactly two denial conflicts and no date conflict, and `checks` is computed per case from a stored run summary with real skipped[] reasons. Two things are still wrong: the \"describes a collision\" word test still loses true conflicts on ordinary wordings, and the stored summary goes stale after `confirm_date` and then contradicts a live flag.\n\n## Answers to the brief\n1. **Accident-date variants.** Round-1 set (probe2.py, A-L) on the r2 archive: B, C, D, E, F, G and H conflict, A, J, K, L are quiet, I (two stated dates) conflicts. Fresh variants: 30 (`r2_variants.py` V1-V20, `r2_variants2.py` W1-W10), including a billing statement and an intake form dated before the accident. Right: V1 billing that names the collision conflicts, V2 billing without mechanism is info-only, V3 intake naming \"rear-ended\" conflicts, V5 \"slipped and fell\" conflicts, V10 and V14-V15 history/\"fall risk\" are info-only, V16-V17 and V19 conflict, V20 is quiet. V4 (an intake dated before the accident it states) conflicts because its own \"Date of accident:\" phrase matches the event list; I think that is the right result, not a defect. Wrong: 8 pre-accident records that name the collision are info-only (finding 1), and 6 benign ones conflict (finding 3).\n2. **checks.** Matrix over the real pipeline and the case view (`r2_checks_matrix.py`): ingested only gives accident_date + provider_name with NOT_RUN for the two pair rules; finished English gives all four, skipped []; deadline before the conflict stage gives STAGE_SKIPPED; deadline after it gives all four; a real crash in the conflict stage of a re-run gives RUN_FAILED (`r2_real_crash.py`, not the faked state the unit test uses); lib09 gives LANGUAGE_PARTIAL on records [2, 4, 7] for three types; an all-Spanish packet gives LANGUAGE for three types and `conflict_types == ['provider_name']`. Never claims a rule ran when it did not, on any of those. The two exceptions are finding 2 (stale after confirm_date) and finding 5 (rows with no summary).\n3. **lib11.** Still correct. `evals.library_report` on the archive: lib11 must flags 4/4, must_not hits 0. Case view after a fixture run: two denial conflicts, accident-date flags [], note \"1 record predates the stated accident date, March 18, 2026. None describes a collision...\" (true, and the PCP's \"car accidents in 2019 and 2022\" is read as history). Candidates and accident-date output over all 27 golden and library packets are identical between c4bb4da and 68b8685; versus the pre-T-141 build only lib11 changes; the sample still raises accident_date_after_treatment (2026-01-19).\n4. **Changed test (test_t116_r4_all_dated_records.py).** Right call. The old expectation (a statement dated before the stated accident is a conflict naming the statement) is exactly what the Round 2 direction removes, the new expectation is `== []` plus a note with record_nos [1], and the docstring says why. The twin test keeps the D-055 invariant (paperwork is never named as the first treatment) and N17 (paperwork branch off) is killed by three tests, so the invariant is still pinned. One caveat, not a defect: in the twin the \"collision\" that makes it a conflict is the stating visit's own phrase \"Date of accident: 2026-01-15\", so the twin proves the self-contradiction path, not a described collision.\n5. **Tests.** Six conflict modules on the r2 archive: 203 passed. Full `tests/unit` on the 68b8685 archive: 1 failed, 3799 passed, 8 skipped (the failure is finding 6; the 12 working-tree T-139 failures are other work, noted only). 30 mutants (`r2_mutate.py`): 22 killed, 8 survived. Survivors and what they mean are in finding 4.\n\n```json\n{\n \"card\": \"T-141\",\n \"persona\": \"staff-engineer-reviewer\",\n \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"git 68b8685 (T-141 round 2), compared with c4bb4da and 68b8685~1; all probes on git archives in the scratchpad (T141r2_head, T141r2_mut2, T141r2_parent, T141_head, T141_pre), never the dirty working tree; fixture backend, ZLAYT_MODE=local; sample and lib09/lib11 packets; no server started\",\n \"exercised\": [\n  \"Read personas/staff-engineer.md, reviews/T-141-staff-engineer.md (round 1), `python3 tools/board.py show T-141` (direction note, handoff), `git show 68b8685` in full (conflicts.py, conflict_candidates.py, pipeline.py, present.py, api.md, tests), `git rev-parse HEAD` = 68b868575403c86cdac00d4fdc641ecd2494c613\",\n  \"git archive 68b8685 into T141r2_head, T141r2_mut2 (mutants), 68b8685~1 into T141r2_parent; reused the round-1 archives T141_head (c4bb4da) and T141_pre for differentials\",\n  \"Round-1 variants: artifacts/review-evidence/T-141/probe2.py on the r2 archive (A-L)\",\n  \"30 fresh accident-date variants: r2_variants.py (V1-V20) and r2_variants2.py (W1-W10), incl. billing statement and intake dated before the accident; r2_variants2.py also run on c4bb4da to see which wrongs are inherited\",\n  \"checks matrix through the real pipeline and present.case_view: r2_checks_matrix.py (ingested, complete, deadline at extract/verify/amounts/conflicts/flags, re-run in flight, legacy rows without run_checks, lib09 partial Spanish, lib11, all-Spanish synthetic, checks() defaults); r2_real_crash.py (crash in the conflict stage of a re-run, also with the P2 mutant); r2_stale_checks.py (ingest, then review.confirm_date)\",\n  \"27-packet differential (diff_packets.py) c4bb4da vs 68b8685 (identical) and pre vs 68b8685 (only lib11), sample accident-date conflict still present\",\n  \"evals.library_report on the r2 archive: lib11 4/4 must flags, 0 must_not hits; lib11 case view after a fixture run (r2_lib11.py)\",\n  \"pytest: conflict modules (test_conflicts, test_conflict_candidates, test_t093_j3_controls_reachable, test_t141_checks_per_case, test_t116_r4_all_dated_records, test_api_routes) 203 passed; full tests/unit on 68b8685 archive 1 failed (test_export_equals_golden_when_everything_accepted), 3799 passed, 8 skipped; same test passes on the 68b8685~1 archive (34 passed in test_api_routes)\",\n  \"30 mutants (r2_mutate.py) on T141r2_mut2: 22 killed, 8 survived; the file was restored and diffed against T141r2_head after the manual mutants\",\n  \"Read app/frontend/flags.js coverage() (what the UI does with checks), memory/contracts/api.md checks section, board list for the owner of rendering skipped[] and notes[] (T-151, ready)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\n  \"determinism\": 5,\n  \"honest_failure\": 3,\n  \"tests_assert_behaviour\": 4,\n  \"llm_code_boundary\": 5,\n  \"controls_discipline\": 4\n },\n \"findings\": [\n  {\n   \"severity\": \"major\",\n   \"title\": \"The 'describes a collision' test still loses true accident-date conflicts: 8 of 30 fresh variants where an earlier record names the collision come back info-only, and the note then says 'None describes a collision'\",\n   \"evidence\": \"app/backend/conflicts.py:14-18 (_EVENT, _HISTORICAL), :21-31 (_historical: a history word anywhere in the clause, or any bare year before the stated year, makes the clause history), :57-59 (_event_records). Repro on a git archive of 68b8685: `.venv/bin/python -I artifacts/review-evidence/T-141/r2_variants.py <archive>` and `r2_variants2.py <archive>`; each case is a record dated 2026-01-05, a PT visit 2026-01-12, intake 'Date of accident per intake form: 2026-01-09'. Info-only, should conflict: V6 'Slip and fall at the grocery store, wrist pain.' (no 'fell'); V7 'Pedestrian vs auto. Neck pain 7/10.'; V8 'Neck pain since the incident. Whiplash pattern.'; V11 ER 2025-12-30 'Rear-ended in December 2025. Neck pain.' (bare 2025 < 2026 makes it history; stated 2026-01-05); V18 'MVC with no history of LOC.' (same clause, so 'history' wins; round 1's variant D only passes because it had a comma); W3 'Healthy prior to the rear-end collision. Neck pain since.'; W4 'Previously asymptomatic until the motor vehicle collision.'; W5 same as V18. 'prior to' and 'previously ... until' are temporal words about the collision, and ER, PT and chiro narratives use them all the time. Passing and correct: V1, V3, V5, V16, V17, V19, W9. Note text app/backend/conflicts.py:~150: 'None describes a collision, so no date conflict is raised' is false for the 8; the UI does not show notes yet (T-151, ready), so today the loss is invisible.\",\n   \"why_it_matters\": \"Same failure family as round-1 major 1, moved from sentence to clause: a deterministic R-FL-2 check becomes a word-list guess and a true discrepancy between the stated accident date and an earlier record disappears, now with a sentence that asserts there is nothing to find. Round 2 fixed the six wordings I tried and left the class open. This is a spec violation of the Round 2 direction ('one that DOES describe the collision ... is a date conflict'), not a preference. Not a blocker because it needs a stated date later than the earliest record plus one of these wordings, and the loss is limited to the date-conflict flag, not an entry or a total.\",\n   \"fix\": \"(a) 'prior' / 'previously' / 'history' make a clause history only when they modify the event noun ('prior accident', 'history of MVA', 'previous collision'); 'prior to', 'previously ... until' and 'no history of <other noun>' in the same clause do not. (b) A bare year equal to the year of the record's own date, or the year before it when the record date is within 60 days of January, is not history. (c) Add incident, pedestrian, auto, slip and fall, whiplash, impact. (d) Soften the note: do not assert 'none describes a collision'; say what the code looked for ('no record names a collision, crash, MVA, fall or similar') so the paralegal can read the records.\",\n   \"acceptance_test\": \"tests/unit/test_conflicts.py: V6, V7, V8, V11, V18, W3, W4, W5 each return one accident_date_after_treatment conflict; the lib11 shape (annual visit listing 2019 and 2022 accidents, EMS 'struck from behind') and the V10/V14/V15 history wordings still return [].\"\n  },\n  {\n   \"severity\": \"major\",\n   \"title\": \"`checks.notes` and the language/dated-record facts are a snapshot taken at run time; `confirm_date` recomputes the accident-date conflict live, so the case then shows a conflict flag and a note saying no conflict is raised\",\n   \"evidence\": \"app/backend/pipeline.py:160-165 (_store_run_checks writes run_summary into case config at ingest, run start and finalize only), app/backend/review.py:499-533 (_recompute_gaps recomputes accident_date_conflicts after confirm_date and never touches run_checks), app/backend/present.py:317 (checks built from the stored summary). Repro: `.venv/bin/python -I artifacts/review-evidence/T-141/r2_stale_checks.py <68b8685 archive>`: records 2026-03-04 annual visit, 03/06/2026 (ambiguous) ER 'rear-end collision', intake 2026-03-27 'Date of accident per intake form: 2026-03-18'. Output: `ingested | notes: ['1 record predates the stated accident date, March 18, 2026. None describes a collision, so no date conflict is raised; ...'] | accident-date flags: []`, then after `review.confirm_date(.., '2026-03-06')`: `notes: [same text] | accident-date flags: ['accident_date_after_treatment']`. The same snapshot holds dated_records, so a case whose dates were all ambiguous at run time keeps NO_DATED_RECORD and drops accident_date from conflict_types after the user confirms them.\",\n   \"why_it_matters\": \"The field exists so the UI can say honestly what was checked on this case. After any date confirmation it can contradict a flag on the same screen ('no date conflict is raised' beside 'records disagree'), and under-reports what ran. The first reader of this is the paralegal in T-151. The part of the summary that comes from the records (note, dated count) is a pure function of the records and should not be stored.\",\n   \"fix\": \"Compute notes and the NO_DATED_RECORD condition at GET time from the current records (accident_date_note and the dated count are cheap and deterministic); store only what cannot be recomputed (conflicts_stage, per-record language). Or refresh run_checks at the end of _recompute_gaps.\",\n   \"acceptance_test\": \"tests/unit/test_t141_checks_per_case.py: the r2_stale_checks scenario (ambiguous collision record, confirm_date) ends with an accident_date flag and notes == []; a case whose only dated record was ambiguous at run time lists accident_date in conflict_types after confirm_date.\"\n  },\n  {\n   \"severity\": \"minor\",\n   \"title\": \"Benign wording in an earlier record still produces a 'records disagree' accident-date conflict: negated mechanism words, 'last year', and 'vehicle' / 'hit' in other senses\",\n   \"evidence\": \"Same scripts, 68b8685 archive. Conflict, should be info-only: W1 'Annual physical. Denies any accidents or falls.'; W2 'No recent accidents or injuries.'; V9 'Reports a car accident last year, fully recovered.'; V12 'Vehicle registration renewed.'; V13 'Patient hit her weight goal of 150 lb.'; W8 'Auto insurance card on file; vehicle: 2019 Honda Civic.' conflicts.py:14-15 (_EVENT includes bare 'hit', 'vehicle', 'accident\\\\w*'; no negation or 'last year' handling). Inherited, not new: r2_variants2.py on the c4bb4da archive and the V9/V12/V13 rows on c4bb4da also conflict (round 1 only skipped when another record was dated that day). Labelled 'I would tighten it': the paralegal sees and can dismiss a code conflict, nothing is lost.\",\n   \"why_it_matters\": \"The card's own target was a false accident-date conflict from an annual visit. 'Denies any accidents' is the commonest pre-accident PCP line there is, so the false conflict class that GATE-M2 reported on lib11 is narrower but not closed.\",\n   \"fix\": \"Skip a clause when a negator ('no', 'denies', 'without', 'negative for') precedes the event word within the clause; drop bare 'hit' and 'vehicle' in favour of 'hit by', 'struck', 'vehicle (accident|collision|crash)'; add 'last year' and 'N months ago' to _HISTORICAL.\",\n   \"acceptance_test\": \"tests/unit/test_conflicts.py: W1, W2, V9, V12, V13, W8 each return [] and a note; V1, V3, V5, W9 still conflict.\"\n  },\n  {\n   \"severity\": \"minor\",\n   \"title\": \"Eight mutants survive: the old-full-date history branch, run-start 'pending', the 'uncertain' language rule and four word-list members are not pinned\",\n   \"evidence\": \"`r2_mutate.py` (30 mutants over conflicts.py, conflict_candidates.py, pipeline.py, present.py; run against test_conflicts, test_conflict_candidates, test_t141_checks_per_case, test_t116_r4, test_api_routes, test_t093): SURVIVED N6 and N18 (full date more than a year before the stated date no longer history: conflicts.py `> 365` and the `d[\\\"iso\\\"] < iso` test; nothing uses 'Rear-end collision 03/14/2024, resolved.'); P2 (pipeline.py:349 `_store_run_checks(.., \\\"pending\\\")` at run start removed: `r2_real_crash.py` shows a crashed re-run of a finished case then reports all four types as ran, and test_a_run_that_died_before_the_conflict_stage fakes the stored state instead of producing it); P3 (ingest-time summary removed, equivalent for English); C7 ('uncertain' language counted as read); N1, N2, N3, N4 (t-bone/sideswipe/run over, airbag/seatbelt, 'hit', 'vehicle' removed one at a time; dropping 'hit' and 'vehicle' together is killed). N14 is equivalent. Killed: N5, N7-N13, N15-N17, C1-C6, C8, P1, R1 (22 of 30). Real behaviour of P2 is correct at HEAD (`after crashed re-run: RUN_FAILED` for both pair rules).\",\n   \"why_it_matters\": \"P2 is the line that keeps a crashed re-run from claiming the previous run's result; its only test builds the failed state by hand. N6/N18 is a documented rule ('full date over a year before') with no test.\",\n   \"fix\": \"Add a unit test that crashes the conflict stage of a re-run (monkeypatch FL.run_conflict_pass to raise) and asserts RUN_FAILED; a test for 'Rear-end collision 03/14/2024, resolved.' being info-only; one test per word-list member or a table test over _EVENT.\",\n   \"acceptance_test\": \"Re-run r2_mutate.py: P2, N6, N18, N1-N4 and C7 are killed.\"\n  },\n  {\n   \"severity\": \"minor\",\n   \"title\": \"A case with no stored run summary (created before this commit) claims every check ran, and a failed one with none sends an empty list to the UI fallback\",\n   \"evidence\": \"r2_checks_matrix.py S5: `legacy ready, no run_checks | ran=['plan_vs_early_end', 'denial_vs_history', 'accident_date', 'provider_name'] skipped=[]` (conflict_candidates.py checks(): `known = run is not None`, stage None and state complete is treated as ran); S5b: `legacy failed, no run_checks | ran=[] skipped=[all four RUN_FAILED]`. app/frontend/flags.js:89 treats `conflict_types.length == 0` as 'server sent no list' and prints FALLBACK_CHECKED under 'Checked:' (three kinds), which is the overclaim this field exists to prevent.\",\n   \"why_it_matters\": \"Any database that already holds cases (the dev DB at port 7860) shows full coverage for a Spanish case created before the commit. New cases always get a summary at ingest, so this is a migration edge, not a live path.\",\n   \"fix\": \"When no summary is stored, say so: return conflict_types [] and one skipped entry per type with reason_code UNKNOWN ('this case was analysed before per-case checks were recorded'); the frontend should render an empty list as 'none checked', not as the fallback.\",\n   \"acceptance_test\": \"tests/unit/test_t141_checks_per_case.py: a finished case whose config lacks run_checks lists no type under conflict_types and every type under skipped with UNKNOWN.\"\n  },\n  {\n   \"severity\": \"minor\",\n   \"title\": \"Commit 68b8685 carries a T-139 test hunk without its code and is red at the commit: test_export_equals_golden_when_everything_accepted passes at the parent and fails at 68b8685\",\n   \"evidence\": \"`git archive 68b8685~1` then `pytest tests/unit/test_api_routes.py -q` -> `34 passed`; `git archive 68b8685` then `pytest tests/unit -q` -> `1 failed, 3799 passed, 8 skipped in 211.01s`, `FAILED tests/unit/test_api_routes.py::test_export_equals_golden_when_everything_accepted`, `assert held == []` / `AssertionError: assert ['e2', 'e4'] == []` (tests/unit/test_api_routes.py:170). `git show 68b8685 -- tests/unit/test_api_routes.py` shows the hunk `assert held == [\\\"e2\\\", \\\"e4\\\"]` -> `assert held == []  # T-139 narrowing`; the narrowing code is still uncommitted in the working tree (`git status --short`: M app/backend/amounts.py, flags.py, pipeline.py, present.py, review.py). Same shared-index pattern as round-1 minor 5.\",\n   \"why_it_matters\": \"A commit on main that breaks the committed suite makes bisect and any reviewer pinned to HEAD see a red test that is not T-141's. Noted per the brief; it is distinct from the 12 working-tree failures because it is inside this commit's own diff.\",\n   \"fix\": \"No change to T-141 code. Land the T-139 narrowing code (or revert that one test hunk) so HEAD is green; stage by pathspec per the file-ownership rule.\",\n   \"acceptance_test\": \"`pytest tests/unit/test_api_routes.py -q` passes on a git archive of the commit that follows.\"\n  }\n ],\n \"whats_right\": [\n  \"The Round 2 shape is right: the content decides, the skip rule is gone, and all six round-1 variants (B, C, D, E, F, G) conflict while the lib11 shape stays quiet; lib11 library report is 4/4 with 0 must_not hits and the other 26 packets are unchanged.\",\n  \"checks is computed from the run, not a constant: ingested, deadline-skipped, crashed re-run, partial Spanish and all-Spanish each give a different, correct skipped[] with a reason code, and conflict_types lists only what ran; api.md documents the shape and the T-142 fields are kept.\",\n  \"The changed T-116 test was changed for the right reason, with a reason in the docstring, a twin test that keeps the paperwork invariant, and the paperwork branch still killed by three tests.\"\n ],\n \"questions_for_chris\": []\n}\n```\n"
}
````

### User / tool · 2026-11-02T14:02:06.263Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:17.160Z

**tool call — Bash**
````
{
 "command": "grep -c \"SURVIVED\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_mutants.txt; grep -c \"KILLED\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T141r2_mutants.txt"
}
````

### User / tool · 2026-11-02T14:02:17.369Z

**tool result**
````
10
20
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:22.636Z

**tool call — Bash**
````
{
 "command": "sed -i 's/30 mutants (`r2_mutate.py`): 22 killed, 8 survived\\./30 mutants (`r2_mutate.py`): 20 killed, 10 survived (N14 and P3 are equivalent)./; s/\"Eight mutants survive: the old-full-date history branch/\"Ten mutants survive (two equivalent): the old-full-date history branch/; s/Killed: N5, N7-N13, N15-N17, C1-C6, C8, P1, R1 (22 of 30)\\./Killed: N5, N7-N13, N15-N17, C1-C6, C8, P1, R1 (20 of 30)./; s/30 mutants (r2_mutate.py) on T141r2_mut2: 22 killed, 8 survived/30 mutants (r2_mutate.py) on T141r2_mut2: 20 killed, 10 survived/' reviews/T-141-staff-engineer-r2.md; grep -n \"22 \\|8 survived\\|Eight\\|20 killed\\|Ten mutants\" reviews/T-141-staff-engineer-r2.md | cut -c1-120; python3 - <<'EOF'\nimport re,json\ns=open(\"/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md\").read()\nj=json.loads(re.findall(r\"```json\\n(.*?)\\n```\",s,re.S)[0]); print(j[\"verdict\"],[f[\"severity\"] for f in j[\"findings\"]])\nEOF\npython3 tools/board.py validate 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T14:02:23.189Z

**tool result**
````
sed: -I or -i may not be used with stdin
10:5. **Tests.** Six conflict modules on the r2 archive: 203 passed. Full `tests/unit` on the 68b8685 archive: 1 failed,
27:  "30 mutants (r2_mutate.py) on T141r2_mut2: 22 killed, 8 survived; the file was restored and diffed against T141r2_h
45:   "acceptance_test": "tests/unit/test_conflicts.py: V6, V7, V8, V11, V18, W3, W4, W5 each return one accident_date_a
65:   "title": "Eight mutants survive: the old-full-date history branch, run-start 'pending', the 'uncertain' language r
66:   "evidence": "`r2_mutate.py` (30 mutants over conflicts.py, conflict_candidates.py, pipeline.py, present.py; run ag
changes ['major', 'major', 'minor', 'minor', 'minor', 'minor']
ok (152 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:29.322Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md",
 "old_string": "30 mutants (`r2_mutate.py`): 22 killed, 8 survived.",
 "new_string": "30 mutants (`r2_mutate.py`): 20 killed, 10 survived (N14 and P3 are equivalent)."
}
````

### User / tool · 2026-11-02T14:02:29.455Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-141-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:30.173Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md",
 "old_string": "on T141r2_mut2: 22 killed, 8 survived;",
 "new_string": "on T141r2_mut2: 20 killed, 10 survived;"
}
````

### User / tool · 2026-11-02T14:02:30.240Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-141-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:30.924Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md",
 "old_string": "\"title\": \"Eight mutants survive:",
 "new_string": "\"title\": \"Ten mutants survive (two equivalent):"
}
````

### User / tool · 2026-11-02T14:02:31.000Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-141-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:31.505Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md",
 "old_string": "C8, P1, R1 (22 of 30)",
 "new_string": "C8, P1, R1 (20 of 30)"
}
````

### User / tool · 2026-11-02T14:02:31.581Z

**tool result (error)**
````
PreToolUse:Edit hook error: reviewer-write-guard: T-141-staff-engineer-r2.md already exists; reviews are append-only — write a new file (e.g. -r2/-r3 suffix)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:36.044Z

**tool call — Bash**
````
{
 "command": "printf '\\nErratum: mutant counts. The summary and the JSON say 22 killed and 8 survived (and finding 4 is titled \"Eight mutants survive\"); the run (r2_mutate.py output) is 20 killed and 10 survived: N1, N2, N3, N4, N6, N14, N18, C7, P2, P3 (N14 and P3 equivalent). The finding text lists all ten by id, so the finding stands as written; the JSON block is otherwise authoritative.\\n' >> reviews/T-141-staff-engineer-r2.md; tail -3 reviews/T-141-staff-engineer-r2.md | cut -c1-200; python3 tools/board.py validate 2>&1 | tail -2"
}
````

### User / tool · 2026-11-02T14:02:36.749Z

**tool result**
````
```

Erratum: mutant counts. The summary and the JSON say 22 killed and 8 survived (and finding 4 is titled "Eight mutants survive"); the run (r2_mutate.py output) is 20 killed and 10 survived: N1, N2, N3,
ok (152 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:44.341Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r2_patterns.md",
 "content": "---\nname: project_t141_r2_patterns\ndescription: T-141 r2 68b8685 changes — clause-level word list still loses true accident-date conflicts, stored run summary goes stale after confirm_date, test hunk from another card makes commit red\nmetadata:\n  type: project\n---\n\nT-141 r2 (68b8685, verdict changes, 2 major 4 minor).\n\n- Fix for a lost-conflict class moved the boundary from sentence to clause but left the class: \"prior to / previously until / no history of LOC\" in the same clause as the collision word still makes it history; unlisted mechanism words (slip and fall, pedestrian vs auto, the incident) and month-year in prior year are info-only. Always run 20+ fresh wordings, not only the prior round's list.\n- A snapshot stored at run time (case config run_checks: notes, dated_records) is not refreshed by review.confirm_date -> _recompute_gaps, so a live flag and a stored note contradict. Grep every writer of the thing the snapshot summarises.\n- Lexicon event_on_date (\"MVA on 03/14/2024\") makes an OLD accident a stated accident date, so accident_dates_differ fires; inherited, not r2.\n- Commit swept another card's test hunk (held == []) without its code: red at the commit, green at the parent. Check the failing test with git archive of commit and parent.\n- Method that worked: real-pipeline crash probe (monkeypatch FL.run_conflict_pass) to show a faked-state unit test hides the P2 line; mutate script with 30 mutants over a git archive copy.\n- reviews/*.md is write-once even for Edit; fix counts by appending an Erratum with printf >>.\n\n**How to apply:** for word-list rules ask what the clause-level negation/temporal words do; for stored summaries ask what refreshes them.\n"
}
````

### User / tool · 2026-11-02T14:02:44.546Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t141_r2_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:45.431Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && printf -- '- [T-141 r2 patterns](project_t141_r2_patterns.md) — 68b8685 changes: clause word list still loses conflicts (prior to/no history of), stored run summary stale after confirm_date, sibling test hunk red at commit\\n' >> MEMORY.md && tail -1 MEMORY.md | cut -c1-80"
}
````

### User / tool · 2026-11-02T14:02:45.653Z

**tool result**
````
- [T-141 r2 patterns](project_t141_r2_patterns.md) — 68b8685 changes: clause w
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T14:02:53.265Z

T-141 round 2 (68b8685) verdict is **changes**: 0 blockers, 2 major, 4 minor. Review is in `/Users/arsis/zlayt-pm-project/reviews/T-141-staff-engineer-r2.md`; my mutant counts there were wrong and are corrected in the erratum at the end of the file. The right counts are 20 of 30 mutants killed and 10 survived, two of them equivalent.

- **Major 1:** the "describes a collision" word test still turns a true accident-date conflict into an info note on 8 of 30 fresh variants. Examples are "Healthy prior to the rear-end collision", "MVC with no history of LOC", "Pedestrian vs auto" and "Rear-ended in December 2025". The note then claims "None describes a collision".
- **Major 2:** `checks.notes` is stored at run time and `confirm_date` doesn't refresh it. After confirming a date, the case shows an accident-date conflict beside a note saying no conflict is raised.
- **Minor:**
  - 6 benign wordings (e.g. "Denies any accidents") still raise a conflict; this behaves the same on c4bb4da.
  - Surviving mutants: the old-full-date branch, the run-start "pending" write and the "uncertain" language rule are not pinned.
  - A case with no stored summary claims every check ran.
  - Commit 68b8685 carries a T-139 test hunk without its code, so `test_export_equals_golden_when_everything_accepted` passes at the parent and fails at the commit.

Your other questions:
- **Round-1 variants:** all six conflict now.
- **lib11:** unchanged. It still gives two denial conflicts, no date conflict, 4/4 must flags and 0 must_not hits.
- **Per-case `checks`:** correct in the ingested, deadline-skipped, crashed re-run, partial-Spanish and all-Spanish cases; the stale and no-summary cases above are the exceptions.
- **Changed test:** changing `test_t116_r4_all_dated_records.py` was the right call. The reason is in the docstring, and the twin test keeps the paperwork rule.

Probe scripts are in `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-141/` (the `r2_*.py` files).
