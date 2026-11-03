# Subagent: T-126 r2 staff review (T-126 r2 staff review)

Source: `agent-af695467894a2e15b.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T11:49:25.120Z

This is the round-2 review of board card T-126 in /Users/arsis/zlayt-pm-project. Read reviews/T-126-staff-engineer.md and `python3 tools/board.py show T-126`, including the handoff.

On a `git archive HEAD` copy in your scratchpad:
- Re-run your round-1 repro. No tray flag of any kind (judge-rejected, non-verbatim or FILTERED_BY_RULE) may count as pending in store.export_case, or print in the internal notes or the letter. The notes count must match the UI.
- Probe that no quote absent from its record is ever printed in any export.
- Re-run your mutants. Check the minors: the grounding reason, the merge trace, the api.md example and the single marker constant.
- Run the unit suite.

Write reviews/T-126-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-sonnet-5-5, verdict, findings. Stop only your own PIDs. Reply in 2 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:26.582Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:49:26.592Z

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

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:26.974Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer.md"
}
````

### User / tool · 2026-11-02T11:49:26.982Z

**tool result**
````
1	# T-126 review (round 1) — staff-engineer-reviewer
2	
3	Scope: commit 6d01774 (D-057, rule-filtered model flags), checked on a `git archive` copy of c559ce2 (card files unchanged at HEAD f7829c1; the later diff touches only an unrelated `gap_changes_removed` key). Exercised: full unit suite, the 5 new tests, ten mutants, three probes, code-path grep, api.md.
4	
5	Verdict: changes. The feature works: the filtered proposals are listed, collapsed and counted with the rule named (D-032), and they stay out of flags, queue, counts, gate and the letter. One major remains. A rejected tray flag of any other kind still leaks into the export notes and the pending count, which the contract says it must not (api.md, D-053). The card narrowed its exclusion to `FILTERED_BY_RULE` instead of all rejected flags.
6	
7	Deterministic results (archive of c559ce2, `.venv/bin/python -m pytest tests/unit -q`): `2939 passed, 4 skipped in 191.40s`.
8	
9	Mutants (T-126 test file plus `test_flags_pass.py`):
10	- Killed: M1 (merge drops filtered again), M2 (tray keeps filtered), M7 (filtered not last), M8 (`collapsed` False), M9 (dedupe key without category), M10 (reasons not set).
11	- Survived in the card's own tests: M3 (`review_view` counts filtered), M4 (`export_case` includes filtered), M5 (trace judge rows count filtered), M6 (trace gate counts filtered).
12	- Whole suite: M3-M6 are killed, but only by incidental tests (`test_trace.py`, `test_lib09_t110*.py`), not by anything that names D-057.
13	
14	## Findings
15	1. **Major: other rejected tray flags still count as pending and print in the internal notes.**
16	   - Repro: `probe/probe1.py` runs the sample case with a model flag on record 4 whose quote is not in the record.
17	   - `review.counts.pending` is 23. `store.export_case` returns `pending_count 24` because `f_r4_1` (state `rejected`, review_status `pending`) is in `flags`.
18	   - The notes say "Items not reviewed: 24" and "PENDING ITEMS NOT INCLUDED" lists `Flag, Causation language: record 4 ... "Discharged from PT after two missed appointments."`, a quote that is not in record 4.
19	   - api.md D-053 says a tray flag "is never in `flags`, `review.queue` or the export". The card added the skip at `store.py:69` for `FILTERED_BY_RULE` only; the same bug exists for `JUDGE_DISAGREES`, `LLM_ONLY` and grounding-rejected flags.
20	2. **Minor: the FILTERED branch of `_to_tray` discards the other reasons.**
21	   - `flags.py:~346` sets `reasons=[FILTERED]` and returns early. A non-verbatim model quote loses `GROUNDING_EXCERPT_NOT_VERBATIM` (probe2: `reasons ['FILTERED_BY_RULE']`, `excerpt_verbatim False`), and `INJECTION_SUSPECTED` is likely lost too.
22	   - The quote then shows in `tray_filtered` as "the AI's proposal" with no mark that it is not in the record.
23	   - The comment at `flags.py:~253` ("a rung-1 failure keeps its own reason") is no longer true for this path.
24	3. **Minor: the card's tests do not pin the exclusions they claim.**
25	   - The letter assertion in `test_case_payload_has_a_collapsed_counted_group...` builds the export from an empty case (`{"records": [], "entries": [], ...}`), so it passes whatever the code does.
26	   - Nothing in the T-126 file asserts `review.counts`, the trace gate or judge counts, or `export_case`. Mutants M3-M6 survive it.
27	   - Fix: assert `counts.rejected`, `pending_count`, `case_trace` `gate` and `judges` counts and `export_case(...)["flags"]` with and without the filtered item on the stored case.
28	4. **Minor: two model proposals for the same quote collapse into one without a trace.**
29	   - The dedupe key in `merge` (`flags.py:~122`) is `(type, excerpt)` with no category (probe3: prior_condition and degenerative_language on one quote gives one `pre_existing` flag).
30	   - D-053 says nothing the model proposes is silently dropped. At minimum, record the collapsed category in the audit. Same-category duplicates collapsing is fine.
31	5. **Minor: docs are only partly updated.**
32	   - The api.md paragraph and the reason-code row are good, but the GET example JSON has no `tray_filtered` key (`api.md:232-250`).
33	   - `docs/LLM_VS_CODE.md` rows 11 and 12 describe D-053 and say nothing about D-057 or rule-filtered proposals (architect-owned, so this needs a card).
34	6. **Nit: the rule marker is copied as a literal.**
35	   - `[:1] == ["FILTERED_BY_RULE"]` appears in `store.py`, `trace.py` (twice) and `present.py`. Add one helper, `is_filtered(row)`, next to `FT.FILTERED`.
36	   - `api.py:407` run-progress `counts.flags` counts tray and filtered rows. It is a progress counter and not a "needs review" count, so low value.
37	
38	Right: (a) the filtered id order is protected, with filtered items placed last so recorded judge prompts keep their ids (test 2 plus mutant M7); (b) a per-item dedupe key that includes the category; (c) the contract paragraph and the reason-code row are specific.
39	
40	```json
41	{"card": "T-126", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
42	 "scope": "commit 6d01774 (D-057 filtered-by-rule tray group); git archive of c559ce2 in scratchpad t126r1/a (card files same at HEAD f7829c1); memory/contracts/api.md; sample case via FakeCall",
43	 "exercised": ["pytest tests/unit on git archive of c559ce2: 2939 passed, 4 skipped", "read git show 6d01774 in full (flags, present, store, trace, why, confidence, flag_templates, api.md, tests)", "10 mutants M1-M10 against the T-126 test file plus test_flags_pass (M3-M6 survive; M3-M6 each killed only by incidental tests in the full suite: test_trace.py, test_lib09_t110.py, test_lib09_t110_r2.py)", "probe1: sample case with a model flag on record 4 plus an objective_negative flag; case_view, store.export_case, build_export notes", "probe2: filtered proposal with non-verbatim quote (reasons lose GROUNDING_EXCERPT_NOT_VERBATIM)", "probe3: two model proposals, same quote, different category (collapse to one flag)", "grep of list_items, rejected, flag readers in app/backend, evals/run.py tray handling, api.py progress counts, pipeline finalize", "read memory/contracts/api.md and docs/LLM_VS_CODE.md for D-057"],
44	 "verdict": "changes",
45	 "scores": {"d057_filter_placement": 4, "no_silent_drop": 3, "tests_pin_behaviour": 3, "contract_docs": 4, "determinism_ids": 5},
46	 "findings": [
47	  {"severity": "major", "title": "Rejected tray flags other than FILTERED_BY_RULE are still counted as pending and printed in the export notes",
48	   "evidence": "probe1 (scratchpad t126r1/probe/probe1.py) on archive: review.counts.pending 23 but export_case pending_count 24; flags list contains f_r4_1 state rejected, review_status pending; internal_notes_text 'Items not reviewed: 24' and PENDING ITEMS NOT INCLUDED lists 'Flag, Causation language: record 4 ... \"Discharged from PT after two missed appointments.\"' (quote not in record 4). store.py:69 skips only FILTERED_BY_RULE; api.md D-053: tray flag 'is never in flags, review.queue or the export'.",
49	   "why_it_matters": "D-053 tray items must not be review work or export content; the notes count disagrees with the UI and print a non-verbatim quote. The card touched this exact loop and chose the narrow predicate.",
50	   "fix": "In store.export_case skip every flag with state == 'rejected' (and keep the filtered skip only as a subset); same for trace allitems/judge rows if any other rejected flag is counted as pending.",
51	   "acceptance_test": "Run a case with a J4-disagree model-only flag and a grounding-rejected model flag; assert export_case flags exclude both, pending_count == review.counts.pending, and the notes pending list has no flag line for them."},
52	  {"severity": "minor", "title": "FILTERED branch of _to_tray drops other reasons (grounding failure, injection)",
53	   "evidence": "flags.py _to_tray: 'if code == FILTERED: ... f[\"reasons\"] = [FILTERED]; return'. probe2: filtered proposal with a quote not in the record shows reasons ['FILTERED_BY_RULE'], ladder.code_checks.excerpt_verbatim False. Comment in run_flag_pass says a rung-1 failure keeps its own reason.",
54	   "why_it_matters": "The tray_filtered group then shows a quote that is not in the record with no marker, and the audit loses why the ladder would have rejected it.",
55	   "fix": "Keep reasons = [FILTERED] + the rung-1 and injection reasons (as the LLM_ONLY branch does), and render a 'not found in the record' note for such items.",
56	   "acceptance_test": "Unit test: objective_negative proposal with a non-verbatim quote gives reasons[0] FILTERED_BY_RULE and GROUNDING_EXCERPT_NOT_VERBATIM in reasons."},
57	  {"severity": "minor", "title": "T-126 tests do not pin counts, gate or export exclusions; the letter assertion is vacuous",
58	   "evidence": "tests/unit/test_t126_filtered_by_rule.py: 'case = {\"records\": [], \"entries\": [], \"amounts\": [], \"flags\": []}; assert \"Plan of care: 12 visits.\" not in export.build_export(case)[\"letter_text\"]' passes for any code. Mutants M3 (present.py review_view), M4 (store.py:69), M5 (trace.py:751), M6 (trace.py:901) all survive test_t126_filtered_by_rule.py plus test_flags_pass.py.",
59	   "why_it_matters": "AC says not in counts, gate or letter; those guarantees ride on unrelated tests and would regress silently if those tests change.",
60	   "fix": "Add assertions on review.counts.rejected, case_trace gate/judges counts, and store.export_case flags/pending_count for the stored case with a filtered item; build the export from export_case, not an empty dict.",
61	   "acceptance_test": "Mutants M3-M6 each make a T-126 test fail."},
62	  {"severity": "minor", "title": "Model proposals with the same quote and different category collapse silently in merge",
63	   "evidence": "flags.py merge dedupe key k = (lf['type'], grounding.normalize(lf['excerpt'])) (no category). probe3: prior_condition and degenerative_language on one quote give one flag ('pre_existing','both','needs_review'); the second category is not recorded anywhere.",
64	   "why_it_matters": "D-053/D-057 say nothing the model proposes is silently dropped; the filtered path keys on category, the main path does not.",
65	   "fix": "Record collapsed categories in the kept flag's ladder/audit (or keep both when categories differ).",
66	   "acceptance_test": "Two proposals, same quote, different category: output carries both categories or a ladder note naming the second."},
67	  {"severity": "minor", "title": "Docs partly updated: api.md example lacks tray_filtered; LLM_VS_CODE rows 11/12 do not mention D-057",
68	   "evidence": "memory/contracts/api.md:232-250 example has 'tray' but no 'tray_filtered'; docs/LLM_VS_CODE.md row 11 and row 12 cover D-053 only; grep D-057 docs/*.md returns nothing.",
69	   "why_it_matters": "The frontend and graders read the example and the table; the table is the graded LLM/code boundary.",
70	   "fix": "Add tray_filtered to the example JSON; open an architect card to add one sentence on rule-filtered proposals to rows 11-12.",
71	   "acceptance_test": "grep tray_filtered in the api.md example block and D-057 in docs/LLM_VS_CODE.md both match."},
72	  {"severity": "nit", "title": "FILTERED_BY_RULE marker repeated as string literals; progress counter includes tray rows",
73	   "evidence": "store.py:69, trace.py:752, trace.py:901 each test [:1] == ['FILTERED_BY_RULE'], present.py uses FT.FILTERED; api.py:407 counts.flags = len(list_items flag).",
74	   "why_it_matters": "A fourth reader that forgets the check is how the first review missed three counters.",
75	   "fix": "One is_filtered(row) helper beside FT.FILTERED; optional: exclude rejected rows from the progress count.",
76	   "acceptance_test": "grep FILTERED_BY_RULE app/backend shows one literal definition."}
77	 ],
78	 "whats_right": ["Filtered items are placed after every other tray item so recorded judge prompts keep their f_r<n>_<k> ids (test plus mutant M7 kill)", "tray_filtered carries rule, ref D-032, label, explanation and count per rule, with needs_action false, and the full unit suite stays green (2939 passed)", "api.md documents the payload and adds a FILTERED_BY_RULE reason-code row"],
79	 "questions_for_chris": []}
80	```
81	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:27.728Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-126; git log --oneline | head -5; git status --short | head"
}
````

### User / tool · 2026-11-02T11:49:27.916Z

**tool result**
````
---
id: "T-126"
title: "D-057: D-032-filtered model flags (objective_negative) go to a collapsed 'Filtered by rule' tray group, never silently dropped"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T11:11:07Z"
updated_at: "2026-11-02T11:49:21Z"
claimed_by: "backend"
claimed_at: "2026-11-02T11:43:05Z"
rounds: 1
commits: ["6d01774", "a44dced"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-126-staff-engineer.md", "at": "2026-11-02T11:42:57Z"}
ac:
  - {"n": 1, "text": "flags filtered by D-032 appear in the API tray payload with the rule name and a count; never in timeline/letter; unit test proves no model proposal is dropped silently", "done": true, "evidence": "tests/unit/test_t126_filtered_by_rule.py (5 tests): case payload tray_filtered {label, collapsed, count, rules[rule, ref D-032, count, items]}; not in flags/tray/queue/counts/gate/letter; counts match stored rows; evals fixture flag P/R unchanged 1.000"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T11:11:34Z backend: claimed
- 2026-11-02T11:15:03Z backend: Frontend note (do not edit app/frontend): render case.tray_filtered as a collapsed 'Filtered by rule' group under the tray: header label + count, one sub-row per rules[] (label, ref, count) expanding to items (attempt.excerpt, why). needs_action is false; it must not add to any 'needs review' count. Shape in memory/contracts/api.md (D-057 paragraph).
- 2026-11-02T11:18:56Z backend: AC 1 checked: tests/unit/test_t126_filtered_by_rule.py (5 tests): case payload tray_filtered {label, collapsed, count, rules[rule, ref D-032, count, items]}; not in flags/tray/queue/counts/gate/letter; counts match stored rows; evals fixture flag P/R unchanged 1.000
- 2026-11-02T11:18:57Z backend: moved in_progress -> in_review
- 2026-11-02T11:21:57Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T11:42:57Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-126-staff-engineer.md; round 1; findings:
    - [major] Rejected tray flags other than FILTERED_BY_RULE are still counted as pending and printed in the export notes — fix: In store.export_case skip every flag with state == 'rejected' (and keep the filtered skip only as a subset); same for trace allitems/judge rows if any other rejected flag is counted as pending.
    - [minor] FILTERED branch of _to_tray drops other reasons (grounding failure, injection) — fix: Keep reasons = [FILTERED] + the rung-1 and injection reasons (as the LLM_ONLY branch does), and render a 'not found in the record' note for such items.
    - [minor] T-126 tests do not pin counts, gate or export exclusions; the letter assertion is vacuous — fix: Add assertions on review.counts.rejected, case_trace gate/judges counts, and store.export_case flags/pending_count for the stored case with a filtered item; build the export from export_case, not an empty dict.
    - [minor] Model proposals with the same quote and different category collapse silently in merge — fix: Record collapsed categories in the kept flag's ladder/audit (or keep both when categories differ).
    - [minor] Docs partly updated: api.md example lacks tray_filtered; LLM_VS_CODE rows 11/12 do not mention D-057 — fix: Add tray_filtered to the example JSON; open an architect card to add one sentence on rule-filtered proposals to rows 11-12.
- 2026-11-02T11:42:57Z orchestrator: assigned: backend
- 2026-11-02T11:43:05Z backend: claimed
- 2026-11-02T11:49:08Z backend: moved in_progress -> in_review
- 2026-11-02T11:49:21Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
Round 2. Major: store.export_case now skips every state=rejected flag, so pending_count equals review.counts.pending and no non-record quote reaches the notes (test builds the export from the stored case; probe repro was 24 vs 23). Minors: FILTERED keeps grounding/injection reasons and the why says the quote is not word for word; one FT.is_filtered helper replaces 4 literals; same-quote proposals under other categories are recorded in ladder.code_checks.merged_categories and shown as trace step proposals_merged; api.md example has tray_filtered; letter assertion now on the real export. Verified: test_t126 11 pass, mutants M3-M6 and 5 new ones each fail it, full unit 3129 pass, evals.run metrics unchanged (fixture, same pre-existing blockers). Left: LLM_VS_CODE D-057 sentence noted on T-109 for the architect. Surprised: ground() rebuilt code_checks and wiped the merge note; M6 (trace allitems) only died after asserting grounding-step counts.

a44dced fix(backend): T-126 r2 every tray flag stays out of export counts and notes, merge trace, one filtered helper
f7829c1 fix(backend): T-120 r3 history-source skip strips only the attribution phrase and scans what is left (no condition guessing)
93de5f2 feat(backend): T-127 keep gap_change on the gap flag, gap_changes_removed in GET case
3a74f75 fix(backend): T-129 a preamble no longer shifts record numbers
3d53ca5 feat(backend): T-128 summary trim never leaves a fragment, pin r3 mutants
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:30.686Z

**tool call — Bash**
````
{
 "command": "git show a44dced --stat | cat; git rev-parse HEAD; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer | head -3; ls reviews | grep T-126"
}
````

### User / tool · 2026-11-02T11:49:30.829Z

**tool result**
````
commit a44dced47c4baf691ad21b99fb2c7c373236e13a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:49:03 2026 -0600

    fix(backend): T-126 r2 every tray flag stays out of export counts and notes, merge trace, one filtered helper
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/backend/flag_templates.py            |   5 ++
 app/backend/flags.py                     |  22 +++++--
 app/backend/present.py                   |   4 +-
 app/backend/store.py                     |   2 +-
 app/backend/trace.py                     |  19 ++++--
 memory/contracts/api.md                  |   9 ++-
 tests/unit/test_t126_filtered_by_rule.py | 101 ++++++++++++++++++++++++++++++-
 7 files changed, 146 insertions(+), 16 deletions(-)
a44dced47c4baf691ad21b99fb2c7c373236e13a
MEMORY.md
feedback_exact_count_vs_presence.md
feedback_review_write_once.md
T-126-staff-engineer.md
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:34.095Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/t126r2/a && git archive HEAD | tar -x -C $S/t126r2/a && ls $S/t126r1 2>/dev/null; ls $S/t126r1/probe 2>/dev/null; git diff HEAD --stat -- app tests memory/contracts | tail -2; ls -d .venv; (cd $S/t126r2/a && ls | head -20)"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:34.363Z

**tool call — Bash**
````
{
 "command": "git show a44dced -- app memory | cat"
}
````

### User / tool · 2026-11-02T11:49:34.653Z

**tool result**
````
a
m
m_M3
m_M4
m_M5
m_M6
probe
mut.py
mut2.py
out_M3.txt
out_M4.txt
out_M5.txt
out_M6.txt
probe1.py
probe2.py
probe3.py
 tests/unit/test_t105_added_qualifier_lexicon.py | 148 ++++++++++++++++++++++--
 6 files changed, 277 insertions(+), 81 deletions(-)
.venv
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

### User / tool · 2026-11-02T11:49:34.750Z

**tool result**
````
commit a44dced47c4baf691ad21b99fb2c7c373236e13a
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 05:49:03 2026 -0600

    fix(backend): T-126 r2 every tray flag stays out of export counts and notes, merge trace, one filtered helper
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/backend/flag_templates.py b/app/backend/flag_templates.py
index b44d830..a4f6afa 100644
--- a/app/backend/flag_templates.py
+++ b/app/backend/flag_templates.py
@@ -219,3 +219,8 @@ def render(flag_type: str, subtype: str, **vars) -> tuple:
 FILTER_RULES = {"objective_negative": ("D-032", "Normal or negative findings",
                                        "A normal or negative finding is context, not a flag, so the rule filtered it out. Nothing is needed from you.")}
 FILTERED = "FILTERED_BY_RULE"
+
+
+def is_filtered(reasons) -> bool:
+    """T-126 r2: THE test for a rule-filtered proposal (its reason code comes first). Every reader uses this, never the literal."""
+    return list(reasons or [])[:1] == [FILTERED]
diff --git a/app/backend/flags.py b/app/backend/flags.py
index d6d68a4..75a8d5a 100644
--- a/app/backend/flags.py
+++ b/app/backend/flags.py
@@ -110,11 +110,18 @@ def _overlap(a, b) -> bool:
     return bool(a and b and a[0] < b[1] and b[0] < a[1])
 
 
+def _note_merged(f: dict, lf: dict) -> None:
+    """Other categories the model proposed for the same quote (collapsed into this flag) go in the audit trail: ladder.code_checks.merged_categories."""
+    extra = sorted(c for c in lf.get("_merged", []) if c and c != f["category"])
+    if extra:
+        f["ladder"] = dict(f["ladder"], code_checks=dict(f["ladder"].get("code_checks") or {}, merged_categories=extra))
+
+
 def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False, *, llm_failed: bool = False, fixture_miss: bool = False) -> list:
     """Combine model flags and lexicon flags. Same type with overlapping spans -> origin 'both'; one side only -> LEXICON_ONLY / LLM_ONLY
     (needs_review). Grounding of model quotes is checked separately (ground()); a tagged record adds INJECTION_SUSPECTED to every flag."""
     body, out, used = record["excerpt"], [], set()
-    uniq, seen, filtered, fseen = [], set(), [], set()
+    uniq, seen, filtered, fseen = [], {}, [], set()
     for lf in llm_flags:
         if lf.get("category") in _CONTEXT_ONLY:       # D-032 + D-057: never a flag, but listed (collapsed, counted) rather than dropped
             k = (lf["type"], lf["category"], grounding.normalize(lf["excerpt"]))
@@ -124,8 +131,10 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
             continue
         k = (lf["type"], grounding.normalize(lf["excerpt"]))
         if k not in seen:
-            seen.add(k)
+            seen[k] = lf
             uniq.append(lf)
+        elif lf.get("category") != seen[k].get("category") and lf.get("category") not in seen[k].setdefault("_merged", []):
+            seen[k]["_merged"].append(lf.get("category"))       # T-126 r2 / D-053: a second category on the same quote is not silently lost; the kept flag's code_checks names it
     # R-CO-7: the model's flag order must not decide ids or which model flag a lexicon flag pairs with. Sort by position in the record,
     # then type, category and text (code decides what code can decide).
     uniq.sort(key=lambda lf: ((grounding.locate(body, lf["excerpt"]) or (10 ** 9, 0))[0], lf["type"], lf["category"], grounding.normalize(lf["excerpt"])))
@@ -138,6 +147,7 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
             used.add(match)
             lx["origin"], lx["_stage"]["agreement"], lx["_stage"]["judge"] = "both", "both", "unavailable"
             lx["ladder"] = dict(lx["ladder"], judge=None)
+            _note_merged(lx, uniq[match])
             # D-030: evidence is the verbatim phrase span the model returned (still grounded by ground()); the lexicon sentence is
             # only the fallback quote for phrase-list-only flags. A credibility flag is the exception (D-043, T-092): its excerpt is the whole
             # period sentence, so a model clause never replaces it (the positive half of a mixed sentence must stay in the quote).
@@ -159,6 +169,7 @@ def merge(llm_flags: list, lex_flags: list, record: dict, tagged: bool = False,
         if i in used:
             continue
         f = _flag(record, lf["type"], lf["category"], lf["excerpt"], "llm", llm_spans[i], tagged, "llm_only")
+        _note_merged(f, lf)
         if lf.get("category") in _NEEDS_LEXICON:
             f["_tray"] = "LLM_ONLY"      # D-032 + D-053: a scene_facts flag needs a phrase-list hit; the model's alone is shown in the tray, never dropped
         out.append(f)
@@ -207,7 +218,8 @@ def ground(flags: list, record: dict) -> list:
         elif f["origin"] == "llm" and FT.TYPE_OF.get(f["category"]) != f["type"]:
             fail.append("SCHEMA_INVALID")
         f["_stage"]["grounding_failures"] = fail
-        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
+        f["ladder"]["code_checks"] = {**{k: v for k, v in (f["ladder"].get("code_checks") or {}).items() if k == "merged_categories"},
+                                      "excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
         _compose(f)
     return flags
 
@@ -345,8 +357,8 @@ def _to_tray(f: dict, code: str, judge_reason=None) -> None:
     f["state"] = "rejected"
     if code == FILTERED:
         f["_stage"]["judge"] = None
-        f["reasons"] = [FILTERED]
-        f["why"] = why.why(FILTERED)
+        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding failure / injection reason (T-126 r2)
+        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERBATIM"))
         return
     if code == "LLM_ONLY":
         # never sent to a judge by design (model-only, not code-confirmed): it carries its real reason, not the compose default "judge unavailable"
diff --git a/app/backend/present.py b/app/backend/present.py
index 9e1d949..70858c1 100644
--- a/app/backend/present.py
+++ b/app/backend/present.py
@@ -186,7 +186,7 @@ def rejected_count(conn, case_id):
 def review_view(conn, case_id):
     items = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, case_id, k)]
     handled = generator.resolved_placeholders([r for k, r in items if k == "entry"])
-    items = [(k, r) for k, r in items if r["id"] not in handled and (r.get("state_reasons") or [])[:1] != [FT.FILTERED]]       # D-057: rule-filtered proposals need no action and are not counted
+    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered proposals need no action and are not counted
     live = [(k, r) for k, r in items if r["state"] != "rejected"]
     counts = {s: sum(1 for _, r in live if r["review_status"] == s) for s in ("pending", "accepted", "edited", "dismissed")}
     counts.update({s: sum(1 for _, r in items if r["state"] == s) for s in ("needs_review", "verified", "rejected")})
@@ -288,7 +288,7 @@ def case_view(conn, case_id, *, backend, models, demo_mode):
                 "attempt": {"summary": x.get("title"), "excerpt": " / ".join(e["excerpt"] for e in x["evidence"] if e.get("excerpt"))},
                 "ladder": {"item_id": x["id"], "state": "rejected"}}
     rejected_flags = [x for x in its["flag"] if x["state"] == "rejected"]
-    filtered = [x for x in rejected_flags if x["reasons"][:1] == [FT.FILTERED]]
+    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
     tray += [_tray_flag(x) for x in rejected_flags if x not in filtered]
     # D-057: model proposals a code rule filtered out are a collapsed, counted group of their own (never in `tray`, `flags`, the queue or the letter)
     rules = []
diff --git a/app/backend/store.py b/app/backend/store.py
index c51bc5c..04802ee 100644
--- a/app/backend/store.py
+++ b/app/backend/store.py
@@ -66,7 +66,7 @@ def export_case(conn, case_id: str) -> dict:
                  excerpt=a["excerpt"], review_status=a["review_status"]) for a in DB.list_items(conn, case_id, "amount") if a["state"] != "rejected"]
     fl = []
     for f in DB.list_items(conn, case_id, "flag"):
-        if (f.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:        # D-057: a rule-filtered proposal is not an item to review, count or export
+        if f["state"] == "rejected":        # D-053/D-057: every tray flag (judge-rejected, not word for word, rule-filtered) is not an item to review, count or export; its quote may not be in the record
             continue
         c = f.get("computed") or {}
         ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
diff --git a/app/backend/trace.py b/app/backend/trace.py
index b98f214..dc65e8f 100644
--- a/app/backend/trace.py
+++ b/app/backend/trace.py
@@ -10,7 +10,7 @@ closed reason_code (D-028), written by code; the model never supplies prose. Eve
 """
 import json
 
-from app.backend import generator, grounding, narrative, present, review, store, why
+from app.backend import flag_templates as FT, generator, grounding, narrative, present, review, store, why
 from app.backend import judges as J
 from app.db import db as DB
 from app.llm import audited as AU
@@ -525,7 +525,7 @@ def _amount_steps(cx, row):
 
 
 # ------------------------------------------------------------------ flags
-def _flag_steps(cx, row):
+def _flag_steps_core(cx, row):
     R = set(row.get("state_reasons") or [])
     lad = row.get("ladder") or {}
     cc = lad.get("code_checks") or {}
@@ -740,6 +740,17 @@ def item_trace(conn, case_id: str, item_id: str, full: bool = False) -> dict:
     return _finish(cx, item_id, kind, row, steps)
 
 
+def _flag_steps(cx, row):
+    """_flag_steps_core plus, when the model proposed other categories for this same quote, a code step that names them (T-126 r2: a merge is not silent)."""
+    st = _flag_steps_core(cx, row)
+    merged = ((row.get("ladder") or {}).get("code_checks") or {}).get("merged_categories")
+    if merged:
+        st.insert(0, step("proposals_merged", "Same quote proposed more than once", "code", PASS,
+                          "The AI proposed this quote under more than one category (" + ", ".join(m.replace("_", " ") for m in merged) + " as well as " + row["category"].replace("_", " ")
+                          + "); code kept one flag.", rule="row 11", evidence={"values": {"merged_categories": merged}}))
+    return st
+
+
 _STEPS_OF.update({"entry": _entry_steps, "amount": _amount_steps, "flag": _flag_steps})
 
 
@@ -749,7 +760,7 @@ def _judge_rows(cx):
     out = []
     for kind in ("entry", "amount", "flag"):
         for row in DB.list_items(cx.conn, cx.case_id, kind):
-            if kind == "flag" and (row.get("state_reasons") or [])[:1] == ["FILTERED_BY_RULE"]:      # D-057: never judged, never counted
+            if kind == "flag" and FT.is_filtered(row.get("state_reasons")):      # D-057: never judged, never counted
                 continue
             jd = (row.get("ladder") or {}).get("judge")
             if not jd or not jd.get("verdict"):
@@ -898,7 +909,7 @@ def case_trace(conn, case_id: str, full: bool = False) -> dict:
     failed_ents = [x for x in ents if (x.get("ladder") or {}).get("failure") and x["id"] not in handled]       # tray placeholders for records the extract step made no output for (not drafted items: nothing to ground or judge)
     ents = [x for x in ents if not (x.get("ladder") or {}).get("failure")]      # (a hand-entered record's placeholder is dropped here too)
     amts = DB.list_items(conn, case_id, "amount")
-    flgs = [x for x in DB.list_items(conn, case_id, "flag") if (x.get("state_reasons") or [])[:1] != ["FILTERED_BY_RULE"]]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
+    flgs = [x for x in DB.list_items(conn, case_id, "flag") if not FT.is_filtered(x.get("state_reasons"))]      # D-057: rule-filtered proposals are listed in the payload, not checked or counted here
     allitems = [("entry", x) for x in ents] + [("amount", x) for x in amts] + [("flag", x) for x in flgs]
     cfg = case.get("config") or {}
     rv = present.review_view(conn, case_id)
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index ea1064c..eee97ce 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -234,6 +234,13 @@ Read once, then patch local state from review responses. `entries` are **chronol
       "why": "The model's quote does not appear word for word in the record, so it cannot be used.",
       "attempt": {"summary": "Visit 8: pain 4/10, improving.", "excerpt": "Pain is 4/10 and improving."},
       "ladder": {"item_id": "e5x", "state": "rejected"} } ],
+  "tray_filtered": {
+    "label": "Filtered by rule", "collapsed": true, "needs_action": false, "count": 1,
+    "rules": [ { "rule": "objective_negative", "ref": "D-032", "label": "Normal or negative findings", "explanation": "A normal or negative finding is context, not a flag, so the rule filtered it out. Nothing is needed from you.", "count": 1,
+                 "items": [ { "id": "f_r2_3", "kind": "flag", "record_ids": ["r2"], "state": "rejected", "reasons": ["FILTERED_BY_RULE"],
+                              "why": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag.",
+                              "flag": {"type": "causation", "category": "objective_negative"}, "attempt": {"summary": null, "excerpt": "X-ray negative for fracture."},
+                              "ladder": {"item_id": "f_r2_3", "state": "rejected"} } ] } ] },
   "dates_to_confirm": [],
   "injection": {"records": [], "banner": null},
   "review": {
@@ -756,6 +763,6 @@ Before judge 1, code (`app/backend/summary_trim.py`) splits each AI summary into
 | `AI_TRANSLATION` | needs_review | the item comes from a record routed Spanish or LANGUAGE_UNCERTAIN (D-050); "AI translation — check against the original"; never verified by any check, only the paralegal's accept |
 | `OCR_DERIVED` | needs_review | the item's record lies on a page read by OCR (T-086); always needs_review, added by code after the model steps, never cleared by a judge or a date confirmation |
 | `LLM_FAILED_AFTER_RETRIES` | needs_review | the model call failed on all three attempts; the record has no entry from it |
-| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D-032 `objective_negative`). Listed only in the case payload's `tray_filtered` (collapsed group with the rule named and a count); not a flag, not in the queue, counts, gate or export; no action needed |
+| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D-032 `objective_negative`). Listed only in the case payload's `tray_filtered` (collapsed group with the rule named and a count); not a flag, not in the queue, counts, gate or export; no action needed. `reasons[0]` is this code; a grounding or injection reason follows it when it applies (a filtered quote that is not word for word in the record carries `GROUNDING_EXCERPT_NOT_VERBATIM` and its `why` says so; the export never prints it). T-126 r2: **every** tray flag (state `rejected`: judge-rejected, not word for word, rule-filtered) is left out of the export's `flags`, its pending count and its internal notes, so the notes' "Items not reviewed" equals `review.counts.pending`. When the AI proposes one quote under several categories, code keeps one flag and lists the others in `ladder.code_checks.merged_categories` (item trace step `proposals_merged`) |
 | `SUMMARY_NOT_IN_QUOTE` | rejected | D-054: code removed every clause of the AI summary because each added content its own quote lacks; the record has no entry, only a could-not-verify tray placeholder (`ladder.failure`, `ladder.summary_trim` lists the removed clauses); write the entry by hand. The same placeholder is made when a record is split out with `not_duplicate` (the response `warnings[]` then carries this code, the new tray item's `item_id` and a message saying code removed the summary; its trace shows later steps as skipped, not as a failed word-for-word check) |
 | `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:38.721Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/a && ls -la .venv 2>&1 | head -2; ls /Users/arsis/zlayt-pm-project/.venv/bin/python; cat ../../t126r1/probe/probe1.py"
}
````

### User / tool · 2026-11-02T11:49:38.819Z

**tool result**
````
ls: .venv: No such file or directory
/Users/arsis/zlayt-pm-project/.venv/bin/python
import sys, tempfile, pathlib
sys.path.insert(0, sys.argv[1])
from app.backend import pipeline as PL, present, store, export as X
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record
tmp = pathlib.Path(tempfile.mkdtemp())
extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),
         dict(type="causation", category="prior_condition" , excerpt="Discharged from PT after two missed appointments.")]
def flags(user):
    return {"flags": extra} if which_record(user) == [4] else {"flags": []}
conn = DB.connect(str(tmp/"c.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=flags, j4={"verdict":"disagree","reason_code":"NONE"})), now=lambda: 1.0)
v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
print("tray flags:", [(t["id"], t["reasons"][:1], t["flag"]["category"]) for t in v["tray"] if t["kind"]=="flag"])
print("filtered:", v["tray_filtered"]["count"], [i["id"] for r in v["tray_filtered"]["rules"] for i in r["items"]])
print("review counts:", v["review"]["counts"])
c = store.export_case(conn, cid)
print("export_case flags:", [(f["id"], f["type"], f["subtype"], f["review_status"]) for f in c["flags"]], "pending_count", c["pending_count"])
try:
    out = X.build_export(c)
    notes = out["internal_notes_text"]
    i = notes.find("PENDING ITEMS NOT INCLUDED"); print(notes[:300]); print("...."); print(notes[i:i+1500])
    print("letter has tray text:", "Discharged from PT" in out["letter_text"])
except Exception as e:
    print("export:", type(e).__name__, str(e)[:300])
print("PENDING FLAG LINES:")
for ln in notes[i:].splitlines():
    if ln.startswith("- Flag") or "Discharged from PT after two missed appointments" in ln and "Entry" not in ln: print(ln[:200])
print(sum(1 for ln in notes[i:].splitlines() if ln.startswith("- ")))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:42.823Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t126r2/a && ls tests/unit/_golden.py tests/unit/_fakes.py && (/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -x -p no:cacheprovider > $S/t126r2/unit.txt 2>&1 &) ; sleep 1; echo started\nmkdir -p $S/t126r2/probe; cp $S/t126r1/probe/probe*.py $S/t126r2/probe/; cd $S/t126r2/a && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/t126r2/probe/probe1.py $PWD 2>&1 | tail -40"
}
````

### User / tool · 2026-11-02T11:49:44.553Z

**tool result**
````
tests/unit/_fakes.py
tests/unit/_golden.py
started
tray flags: [('f_r4_1', ['GROUNDING_EXCERPT_NOT_VERBATIM'], 'prior_condition')]
filtered: 1 ['f_r4_2']
review counts: {'pending': 23, 'accepted': 0, 'edited': 0, 'dismissed': 0, 'needs_review': 9, 'verified': 14, 'rejected': 1}
export_case flags: [('f_gap_r6_r7', 'gap', 'gap_over_30', 'pending'), ('f_accident_date_after_treatment_1_2_7', 'conflict', 'accident_date', 'pending'), ('f_cx1', 'conflict', 'treatment_plan_vs_actual', 'pending'), ('f_r3_1', 'pre_existing', 'pre_existing', 'pending'), ('f_r8_1', 'pre_existing', 'degenerative_language', 'pending'), ('f_r6_1', 'causation', 'missed_care', 'pending'), ('f_r7_1', 'causation', 'accident_date_provenance', 'pending'), ('f_r7_2', 'causation', 'new_onset', 'pending'), ('f_r8_2', 'causation', 'speculative_language', 'pending'), ('f_r9_1', 'causation', 'patient_report', 'pending')] pending_count 23
INTERNAL REVIEW NOTES — DO NOT SEND

This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 23.

FLAGS ACCEPTED
- none

FLAGS DISMISSED
- none

FLAGGED LANGUAGE QUOTED IN THE LETTER (your call whether it goes out; edit t
....
PENDING ITEMS NOT INCLUDED
- Entry, record 1 (Austin EMS run report, January 9, 2026): "Restrained driver rear-ended at approx. 35 mph; complained of neck pain 7/10 and headache; alert and oriented; transported to Central ER."
- Entry, record 2 (Central ER discharge summary, January 9, 2026): "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week."
- Entry, record 3 (Dr. Alvarez, primary care, January 16, 2026): "Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks."
- Entry, record 4 (Capital PT, initial evaluation, January 23, 2026): "Cervical range of motion reduced approx. 40%; plan of care 12 visits."
- Entry, record 5 (Capital PT, visit 8, February 20, 2026): "Pain 4/10, improving."
- Entry, record 6 (Capital PT, visit 9, March 6, 2026): "Discharged from physical therapy after two missed appointments; pain 3/10."
- Entry, record 7 (Hill Country Pain Management, new patient, May 18, 2026): "New onset pain radiating to right arm with numbness in fingers, 7/10; MRI ordered."
- Entry, record 8 (Austin Imaging, cervical MRI, May 29, 2026): "C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically."
- Entry, record 9 (Hill Country Pain Management, follow-up, June 12, 2026): "Cervical epidural steroid injection recommended; patient states symp
letter has tray text: False
PENDING FLAG LINES:
- Flag, Gap: 73 days, March 6, 2026 to May 18, 2026: record 6 (Capital PT, visit 9, March 6, 2026) to record 7 (Hill Country Pain Management, new patient, May 18, 2026).
- Flag, Conflict, accident date: record 7 (Hill Country Pain Management, new patient, May 18, 2026): "Date of accident per intake form: 2026-01-19." Record 1 (Austin EMS run report, January 9, 2026): 
- Flag, Conflict, PT plan: record 4 (Capital PT, initial evaluation, January 23, 2026) "Plan of care: 12 visits."; record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed ap
- Flag, Prior condition: record 3 (Dr. Alvarez, primary care, January 16, 2026) "Patient reports low back pain in 2023, resolved."
- Flag, Prior condition: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change; correlate clinically."
- Flag, Causation language: record 6 (Capital PT, visit 9, March 6, 2026) "Discharged from PT after two missed appointments."
- Flag, Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "Date of accident per intake form: 2026-01-19."
- Flag, Causation language: record 7 (Hill Country Pain Management, new patient, May 18, 2026) "New onset pain radiating to right arm with numbness in fingers."
- Flag, Causation language: record 8 (Austin Imaging, cervical MRI, May 29, 2026) "Findings may represent degenerative change; correlate clinically."
- Flag, Causation language: record 9 (Hill Country Pain Management, follow-up, June 12, 2026) "Patient states symptoms began after the January collision."
23
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:49.290Z

**tool call — Bash**
````
{
 "command": "grep -rn \"export_case\\|build_export\\|def .*export\" app/backend/*.py | grep -v \"^app/backend/export.py.*#\" | head -30; cat /private/tmp/claude-501/*/*/scratchpad/t126r1/probe/probe2.py 2>/dev/null | head -0; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat $S/t126r2/probe/probe2.py $S/t126r2/probe/probe3.py"
}
````

### User / tool · 2026-11-02T11:49:49.433Z

**tool result**
````
app/backend/api.py:520:    def export(token: str, style: str = None):
app/backend/api.py:527:            case = store.export_case(c, token)
app/backend/case_extras.py:140:    def export_config_get(token: str):
app/backend/case_extras.py:149:    async def export_config_put(token: str, request: Request):
app/backend/case_extras.py:164:    def export_config_delete(token: str):
app/backend/export.py:4:    build_export(case) -> {"letter_text": str, "internal_notes_text": str, "counts": {...}}  (counts: R-EX-5, outside both blocks)
app/backend/export.py:650:def build_export(case: dict, style: str = None) -> dict:
app/backend/export.py:652:    Raises JudgeNotRun when the case lists accepted items whose judge never ran (`case["judge_not_run"]`, set by store.export_case). The run-state and nothing-accepted
app/backend/export_routes.py:1:"""GET /api/cases/{token}/export: thin router around export.build_export (T-041). Code only.
app/backend/export_routes.py:27:def export_payload(token: str, case: dict, now: datetime = None, style: str = None) -> dict:
app/backend/export_routes.py:30:    out = export.build_export(case, style)
app/backend/export_routes.py:67:def get_export(token: str, style: str = None):
app/backend/store.py:36:def export_case(conn, case_id: str) -> dict:
app/backend/store.py:37:    """The plain dict export.build_export() documents, assembled from the DB (edited text wins; originals travel along)."""
app/backend/store.py:84:    out["export_blockers"] = trace.export_blockers(conn, case_id)           # D-045: build_export refuses while this is non-empty; it is the export gate's blocker list
app/backend/narrative.py:78:    entries = [e for e in accepted_entries(store.export_case(conn, case_id)) if not e.get("translation_label")]    # D-042: the firm-voice paragraph is English-only; translated entries keep their own labelled lines
app/backend/narrative.py:156:def for_export(nar: dict) -> dict:
app/backend/narrative.py:157:    """The small dict export.build_export() reads."""
app/backend/trace.py:1061:def export_blockers(conn, case_id: str, cx=None, rv=None) -> list:
app/backend/trace.py:1063:    Pending items are NOT here: they stay out of the letter and the AI disclosure line counts them. The gate's `ready` is (this list is empty); store.export_case hands the same list to build_export."""
head: illegal line count -- 0
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import flags as F
from tests.unit._fakes import FakeCall
R = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative for fracture.", date_iso="2026-06-01")
llm = [dict(type="causation", category="objective_negative", excerpt="MRI shows no fracture whatsoever.")]
for tagged in (False, True):
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}), tagged=tagged)
    print(tagged, [(f["state"], f["reasons"], f["ladder"]["code_checks"].get("excerpt_verbatim"), f["_stage"].get("grounding_failures"), f["_stage"].get("injection")) for f in out])
import sys
sys.path.insert(0, sys.argv[1])
from app.backend import flags as F
from tests.unit._fakes import FakeCall
R = dict(n=1, source="EMS", excerpt="Patient reports low back pain in 2023, resolved. Ankle exam normal.", date_iso="2026-06-01")
llm = [dict(type="pre_existing", category="prior_condition", excerpt="Patient reports low back pain in 2023, resolved."),
       dict(type="pre_existing", category="degenerative_language", excerpt="Patient reports low back pain in 2023, resolved.")]
out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
print([(f["category"], f["origin"], f["state"]) for f in out])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:49:54.422Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t126r2/a; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; for p in 2 3; do echo == probe$p; $PY -I $S/t126r2/probe/probe$p.py $PWD 2>&1 | tail -6; done\ncat > $S/t126r2/probe/probe3b.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import flags as F, trace\nfrom tests.unit._fakes import FakeCall\nR = dict(n=1, source=\"EMS\", excerpt=\"Patient reports low back pain in 2023, resolved. Ankle exam normal.\", date_iso=\"2026-06-01\")\nllm = [dict(type=\"pre_existing\", category=\"prior_condition\", excerpt=\"Patient reports low back pain in 2023, resolved.\"),\n       dict(type=\"pre_existing\", category=\"degenerative_language\", excerpt=\"Patient reports low back pain in 2023, resolved.\"),\n       dict(type=\"pre_existing\", category=\"prior_condition\", excerpt=\"Patient reports low back pain in 2023, resolved.\")]\nout = F.run_flag_pass(R, call=FakeCall({\"flags\": {\"flags\": llm}}))\nfor f in out: print(f[\"category\"], f[\"origin\"], f[\"state\"], f[\"ladder\"].get(\"code_checks\"), [k for k in f if k.startswith(\"_\")])\n# leak of _merged into model dict / persisted?\nimport json; print(\"_merged\" in json.dumps(out, default=str))\nEOF\n$PY -I $S/t126r2/probe/probe3b.py $PWD 2>&1 | tail -8"
}
````

### User / tool · 2026-11-02T11:49:55.344Z

**tool result**
````
== probe2
False [('rejected', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM'], False, ['GROUNDING_EXCERPT_NOT_VERBATIM'], False)]
Traceback (most recent call last):
  File "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/probe/probe2.py", line 9, in <module>
    print(tagged, [(f["state"], f["reasons"], f["ladder"]["code_checks"].get("excerpt_verbatim"), f["_stage"].get("grounding_failures"), f["_stage"].get("injection")) for f in out])
                                                                                                  ~^^^^^^^^^^
KeyError: '_stage'
== probe3
[('pre_existing', 'both', 'needs_review')]
pre_existing both needs_review {'merged_categories': ['degenerative_language'], 'excerpt_verbatim': True, 'highlight_found': True} ['_stage', '_span']
False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:00.447Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; cd $S/t126r1/a && $PY -I $S/t126r2/probe/probe2.py $PWD 2>&1 | tail -3\ncd $S/t126r2/a; cat > $S/t126r2/probe/probe2b.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import flags as F\nfrom tests.unit._fakes import FakeCall\nR = dict(n=1, source=\"EMS\", excerpt=\"Cyclist struck by a car at low speed. X-ray negative for fracture.\", date_iso=\"2026-06-01\")\nllm = [dict(type=\"causation\", category=\"objective_negative\", excerpt=\"MRI shows no fracture whatsoever.\")]\nout = F.run_flag_pass(R, call=FakeCall({\"flags\": {\"flags\": llm}}), tagged=True)\nprint([(f[\"state\"], f[\"reasons\"], sorted(f.keys())) for f in out])\nEOF\n$PY -I $S/t126r2/probe/probe2b.py $PWD 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T11:50:01.027Z

**tool result**
````
    print(tagged, [(f["state"], f["reasons"], f["ladder"]["code_checks"].get("excerpt_verbatim"), f["_stage"].get("grounding_failures"), f["_stage"].get("injection")) for f in out])
                                                                                                  ~^^^^^^^^^^
KeyError: '_stage'
[('rejected', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM', 'INJECTION_SUSPECTED'], ['_stage', 'category', 'evidence', 'excerpt', 'explanation', 'ladder', 'origin', 'reasons', 'record_id', 'record_no', 'review_status', 'source_kind', 'state', 'title', 'type', 'why']), ('needs_review', ['INJECTION_SUSPECTED'], ['category', 'evidence', 'excerpt', 'explanation', 'ladder', 'origin', 'reasons', 'record_id', 'record_no', 'review_status', 'source_kind', 'state', 'title', 'type', 'why'])]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:05.929Z

**tool call — Bash**
````
{
 "command": "sed -n 1,60p tests/unit/test_t126_filtered_by_rule.py; grep -n \"^def test\" tests/unit/test_t126_filtered_by_rule.py; sed -n 20,70p app/backend/export_routes.py"
}
````

### User / tool · 2026-11-02T11:50:06.025Z

**tool result**
````
"""T-126 (D-057): a model proposal that a code rule filters out (D-032 objective_negative) is listed, not dropped: a collapsed, counted
'Filtered by rule' group in the case payload with the rule named. Never a flag, never in the review queue, timeline or letter; needs no action."""
import json

from app.backend import export, flag_templates as FT, flags as F, present, store, trace
from app.backend import pipeline as PL
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script, which_record

R = dict(n=1, source="EMS", excerpt="Cyclist struck by a car at low speed. X-ray negative for fracture. Ankle exam normal. Full cervical ROM.", date_iso="2026-06-01")


def test_a_model_objective_negative_proposal_is_a_filtered_item_not_a_silent_drop():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),          # duplicate: one item
           dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert len(out) == 2 and all(f["state"] == "rejected" and f["reasons"][0] == "FILTERED_BY_RULE" and f["origin"] == "llm" for f in out)
    assert [f["excerpt"] for f in out] == ["X-ray negative for fracture.", "Ankle exam normal."]
    assert not [f for f in out if f["state"] != "rejected"]


def test_filtered_items_come_after_every_other_tray_item_so_no_recorded_id_moves():
    llm = [dict(type="causation", category="objective_negative", excerpt="X-ray negative for fracture."),
           dict(type="causation", category="scene_facts", excerpt="Cyclist struck by a car at low speed."),
           dict(type="conflict", category="other_fact_mismatch", excerpt="Ankle exam normal.", excerpt_b="Full cervical ROM.")]
    out = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["reasons"][0] for f in out] == ["LLM_ONLY", "LLM_ONLY", "FILTERED_BY_RULE"]


def test_the_rule_filter_does_not_touch_a_phrase_list_flag_in_the_same_sentence():
    r = dict(R, excerpt="Patient reports prior neck pain. Ankle exam normal.")
    llm = [dict(type="causation", category="objective_negative", excerpt="Ankle exam normal.")]
    out = F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}}))
    assert [f["category"] for f in out if f["state"] != "rejected"] and [f for f in out if f["reasons"][0] == "FILTERED_BY_RULE"]


def _view(tmp_path, extra):
    conn = DB.connect(str(tmp_path / "c.sqlite"))
    cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script(flags=lambda user: {"flags": extra} if which_record(user) == [4] else {"flags": []})),
                    now=lambda: 1.0)
    return conn, cid, present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)


def test_case_payload_has_a_collapsed_counted_group_with_the_rule_named_and_nothing_else_changes(tmp_path):
    (tmp_path / "a").mkdir()
    _, _, base = _view(tmp_path / "a", [])
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),
             dict(type="causation", category="objective_negative", excerpt="Discharged from PT after two missed appointments.")]
    (tmp_path / "b").mkdir()
    conn, cid, v = _view(tmp_path / "b", extra)
    g = v["tray_filtered"]
    assert g["label"] == "Filtered by rule" and g["collapsed"] is True and g["count"] == 2 and g["needs_action"] is False
    (rule,) = g["rules"]
    assert rule["rule"] == "objective_negative" and rule["ref"] == "D-032" and rule["count"] == 2 and "normal" in rule["label"].lower()
    ids = [i["id"] for i in rule["items"]]
    assert len(ids) == 2 and all(i["flag"]["category"] == "objective_negative" and i["attempt"]["excerpt"] for i in rule["items"])
    assert all(i["reasons"][0] == "FILTERED_BY_RULE" and i["why"] for i in rule["items"])
14:def test_a_model_objective_negative_proposal_is_a_filtered_item_not_a_silent_drop():
24:def test_filtered_items_come_after_every_other_tray_item_so_no_recorded_id_moves():
32:def test_the_rule_filter_does_not_touch_a_phrase_list_flag_in_the_same_sentence():
47:def test_case_payload_has_a_collapsed_counted_group_with_the_rule_named_and_nothing_else_changes(tmp_path):
73:def test_no_model_proposal_is_dropped_silently_counts_match(tmp_path):
98:def test_the_grounding_failure_stays_on_a_filtered_item_and_the_why_says_so():
107:def test_every_tray_flag_stays_out_of_the_export_pending_count_and_notes(tmp_path):
121:def test_tray_flags_are_not_counted_by_the_review_counts_the_gate_or_the_judge_rows(tmp_path):
142:def test_one_helper_names_the_marker():
149:def test_same_quote_different_category_keeps_one_flag_and_names_the_other_category():
160:def test_the_merge_shows_in_the_item_trace(tmp_path):
    _loader = fn


def _not_found():
    return JSONResponse(status_code=404, content={"error": {"code": "not_found", "message": "No case with that link.", "detail": {}}})


def export_payload(token: str, case: dict, now: datetime = None, style: str = None) -> dict:
    if case.get("export_blockers"):                  # D-045: the same list the export gate reports; pending items are not on it
        raise export.ExportBlocked(case["export_blockers"])
    out = export.build_export(case, style)
    now = now or datetime.now(timezone.utc)
    ok = ("accepted", "edited")
    return {
        "token": token,
        "generated_at": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
        "letter_text": out["letter_text"],
        "internal_notes_text": out["internal_notes_text"],
        "counts": out["counts"],
        "items": {
            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
                         "edited": e["review_status"] == "edited", "excerpt": e["excerpt"],
                         "entered_by": "reviewer" if e.get("entered_by_reviewer") else None}
                        for e in case.get("entries", []) if e.get("review_status") in ok],
            "amounts": [{"id": a["id"], "kind": a["cls"], "counted_in_total": a["cls"] == "charge" and a.get("cents") is not None,
                         "edited": a["review_status"] == "edited", "excerpt": a["excerpt"]}
                        for a in case.get("amounts", []) if a.get("review_status") in ok],
        },
        "warnings": [],
    }


def invalid_style_message() -> str:
    return "The letter style must be 'standard' or 'oneline'."


def blocked_message(e) -> str:
    if e.code == "judge_not_run":
        return judge_not_run_message(len(e.items))
    return e.items[0]["why"] + " The export is blocked."


def judge_not_run_message(n: int) -> str:
    return f"{n} accepted item{'s have' if n != 1 else ' has'} not had the second AI check, so the export is blocked. Run the second check again."


@router.get("/api/cases/{token}/export")
def get_export(token: str, style: str = None):
    case = _loader(token) if _loader else None
    if case is None:
        return _not_found()
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:08.959Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def \" app/backend/review.py | head -30; grep -n \"accept\" tests/unit/test_t126_filtered_by_rule.py | head; sed -n 107,125p tests/unit/test_t126_filtered_by_rule.py"
}
````

### User / tool · 2026-11-02T11:50:09.059Z

**tool result**
````
27:def _now(now):
31:def _item(conn, case_id, item_id):
41:def _bad(msg, **detail):
45:def date_unconfirmed(conn, case_id: str, kind: str, item: dict) -> bool:
57:def _date_unconfirmed_error():
76:def current_text(item: dict):
81:def code_check_failures(rec, item: dict) -> dict:
106:def code_check_message(fails: dict) -> str:
131:def code_check_detail(item_id: str, fails: dict) -> dict:
139:def code_check_error(item_id: str, rec, item: dict):
147:def entry_record(item: dict, recs: list):
152:def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None) -> dict:
170:def apply_review(conn, case_id: str, item_id: str, body: dict, *, call=None, now=None) -> dict:
192:def ocr_record_ids(conn, case_id: str) -> set:
202:def enforce_ocr(conn, case_id: str, t) -> int:
231:def _quoted_words(toks) -> str:
236:def _check_summary(item_id, new_sum, new_exc, label, date_iso, span, rec, call, ocr_derived=False):
276:def _edit(conn, case_id, kind, item, body, call, t):
330:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
368:def _without_date_doubt(item: dict) -> dict:
383:def _log_confirm_date(conn, case_id, item_id, rec, date_iso, cleared, t, gap_changes=()):
391:def _drop(conn, case_id, flag_id):
396:def _gap_figures(flag: dict) -> dict:
401:def _gap_changes(old: dict, new: dict) -> list:
424:def _gap_change_sentence(ch: dict, seq) -> str:
433:def _recompute_gaps(conn, case_id, t, changes=None):
477:def manual_entry(conn, case_id: str, record_id: str, body: dict, *, call=None, now=None) -> dict:
525:def not_duplicate(conn, case_id: str, entry_id: str, record_id: str, *, call=None, now=None) -> dict:
588:def _upsert(conn, case_id, kind, item, t):
598:def judges_for(dollars, call, case_text):
def test_every_tray_flag_stays_out_of_the_export_pending_count_and_notes(tmp_path):
    conn, cid = _stored(tmp_path)
    filtered, other = _tray_flag_ids(conn, cid)
    assert len(filtered) == 2 and len(other) >= 2, (filtered, other)         # filtered x2; the grounding-rejected and the scene_facts flag
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    ex = store.export_case(conn, cid)
    assert not {f["id"] for f in ex["flags"]} & (filtered | other)
    assert ex["pending_count"] == v["review"]["counts"]["pending"]            # the notes count is the UI count (was 24 against 23)
    out = export.build_export(ex)
    for q in (NOT_IN_RECORD, NOWHERE):                                         # a quote that is not in the record is never printed
        assert q not in out["internal_notes_text"] and q not in out["letter_text"]
    assert f"Items not reviewed: {v['review']['counts']['pending']}" in out["internal_notes_text"]


def test_tray_flags_are_not_counted_by_the_review_counts_the_gate_or_the_judge_rows(tmp_path):
    conn, cid = _stored(tmp_path)
    filtered, other = _tray_flag_ids(conn, cid)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert not filtered & {t["id"] for t in v["tray"]} and not (filtered | other) & set(v["review"]["queue"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:10.666Z

**tool call — Bash**
````
{
 "command": "sed -n 152,192p app/backend/review.py; sed -n 60,130p tests/unit/test_t126_filtered_by_rule.py | head -0; sed -n 73,106p tests/unit/test_t126_filtered_by_rule.py"
}
````

### User / tool · 2026-11-02T11:50:10.758Z

**tool result**
````
def set_review(conn, case_id: str, item_id: str, action: str, *, now, edited: dict = None, kind: str = None, item: dict = None, recs: list = None) -> dict:
    """THE one place a review decision is written (DB.apply_review is called from here for accept, edit, dismiss, reset and the batch).
    D-051: whenever the decision leaves an ENTRY accepted or edited (so in the letter), the code checks are recomputed from the wording that
    decision would leave (`edited` replaces the current text; stored code reasons are dropped because the new text is what counts) and a
    failure is a 422 CODE_CHECK_FAILED before anything is written. The judge verdict, the stored state and who wrote the wording do not matter."""
    if kind is None or item is None:
        kind, item = _item(conn, case_id, item_id)
    if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):
        cand = dict(item)
        if edited is not None:
            cand["edited"] = edited
            cand["state_reasons"] = [c for c in item.get("state_reasons") or [] if c not in CODE_CHECK_REASONS]
        err = code_check_error(item_id, entry_record(cand, recs if recs is not None else store.load_records(conn, case_id)), cand)
        if err:
            raise err
    return DB.apply_review(conn, item_id, action, edited=edited, now=now, case=case_id)


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
        set_review(conn, case_id, item_id, action, now=t, kind=kind, item=item)
        if kind == "flag" and action == "dismiss" and body.get("note"):
            DB.update_item(conn, item_id, now=t, case=case_id, reviewer_note=str(body["note"])[:2000])
    else:
        warnings = _edit(conn, case_id, kind, item, body, call, t)
    from app.backend import present
    return {"item": present.item_view(conn, case_id, item_id), "totals": present.totals_view(conn, case_id),
            "review": present.review_view(conn, case_id), "warnings": warnings}


def ocr_record_ids(conn, case_id: str) -> set:
head: illegal line count -- 0
def test_no_model_proposal_is_dropped_silently_counts_match(tmp_path):
    extra = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits.")]
    conn, cid, v = _view(tmp_path, extra)
    rows = [r for r in present.all_items(conn, cid)["flag"] if r["state"] == "rejected" and r["reasons"][0] == "FILTERED_BY_RULE"]
    assert len(rows) == 1 == v["tray_filtered"]["count"]


# ---- T-126 round 2 (reviews/T-126-staff-engineer.md) ---------------------------------------------------------------------------------------------------------
NOT_IN_RECORD = "Patient was discharged after a fall from the roof."
NOWHERE = "Another quote nobody wrote."
STORED = [dict(type="causation", category="objective_negative", excerpt="Plan of care: 12 visits."),                    # rule-filtered, verbatim
          dict(type="causation", category="objective_negative", excerpt=NOT_IN_RECORD),                                 # rule-filtered AND not in the record
          dict(type="causation", category="degenerative_language", excerpt=NOWHERE),                                    # model-only, not in the record: grounding-rejected tray flag
          dict(type="causation", category="scene_facts", excerpt="Discharged from PT after two missed appointments.")]   # model-only scene_facts: LLM_ONLY tray flag


def _stored(tmp_path):
    return _view(tmp_path, STORED)[:2]


def _tray_flag_ids(conn, cid):
    rows = [r for r in DB.list_items(conn, cid, "flag") if r["state"] == "rejected"]
    return {r["id"] for r in rows if FT.is_filtered(r.get("state_reasons"))}, {r["id"] for r in rows if not FT.is_filtered(r.get("state_reasons"))}


def test_the_grounding_failure_stays_on_a_filtered_item_and_the_why_says_so():
    llm = [dict(type="causation", category="objective_negative", excerpt="This sentence is not in the record at all.")]
    (f,) = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": llm}}))
    assert f["reasons"][0] == FT.FILTERED and "GROUNDING_EXCERPT_NOT_VERBATIM" in f["reasons"] and "JUDGE_UNAVAILABLE" not in f["reasons"]
    assert "not word for word in the record" in f["why"]
    (g,) = F.run_flag_pass(R, call=FakeCall({"flags": {"flags": [dict(llm[0], excerpt="Ankle exam normal.")]}}))
    assert g["reasons"] == [FT.FILTERED] and "word for word" not in g["why"]                           # a verbatim one has no such note
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:23.059Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t126r2/a; cat > $S/t126r2/probe/probe4.py <<'EOF'\nimport sys, tempfile, pathlib, json\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import pipeline as PL, present, store, export as X, review as RV, export_routes as ER, trace\nfrom app.db import db as DB\nfrom tests.unit import _golden as G\nfrom tests.unit._fakes import FakeCall, sample_script, which_record\nM = [\"ZQ-NV-OBJNEG quote one nowhere.\", \"ZQ-NV-DEGEN quote two nowhere.\", \"ZQ-NV-CAUS quote three nowhere.\", \"ZQ-NV-SCENE quote four nowhere.\"]\nextra = [dict(type=\"causation\", category=\"objective_negative\", excerpt=M[0]),\n         dict(type=\"pre_existing\", category=\"degenerative_language\", excerpt=M[1]),\n         dict(type=\"causation\", category=\"prior_condition\", excerpt=M[2]),\n         dict(type=\"causation\", category=\"scene_facts\", excerpt=M[3]),\n         dict(type=\"causation\", category=\"objective_negative\", excerpt=\"Plan of care: 12 visits.\"),\n         dict(type=\"causation\", category=\"new_onset\", excerpt=\"Discharged from PT after two missed appointments.\")]\ndef flags(user):\n    return {\"flags\": extra} if which_record(user) in ([4],[6]) else {\"flags\": []}\nfor j4 in ({\"verdict\":\"disagree\",\"reason_code\":\"NONE\"}, None):\n    tmp = pathlib.Path(tempfile.mkdtemp())\n    conn = DB.connect(str(tmp/\"c.sqlite\")); cid = DB.create_case(conn, G.raw(\"sample\"), now=1.0)\n    kw = dict(j4=j4) if j4 else {}\n    PL.run_pipeline(conn, cid, G.raw(\"sample\"), call=FakeCall(sample_script(flags=flags, **kw)), now=lambda: 1.0)\n    rej = [(r[\"id\"], r[\"state_reasons\"][:2]) for r in DB.list_items(conn, cid, \"flag\") if r[\"state\"]==\"rejected\"]\n    print(\"j4\", j4, \"rejected flags:\", rej)\n    for stage in (\"before_accept\", \"after_accept\"):\n        if stage == \"after_accept\":\n            for k in (\"entry\",\"amount\",\"flag\"):\n                for r in DB.list_items(conn, cid, k):\n                    if r[\"state\"] != \"rejected\":\n                        try: RV.apply_review(conn, cid, r[\"id\"], {\"action\":\"accept\"}, now=lambda: 2.0)\n                        except Exception as e: pass\n        v = present.case_view(conn, cid, backend=\"fixture\", models={}, demo_mode=False)\n        c = store.export_case(conn, cid)\n        try:\n            out = X.build_export(c)\n        except Exception as e:\n            print(stage, \"export refused:\", type(e).__name__, str(e)[:100]); out = None\n        pc = v[\"review\"][\"counts\"][\"pending\"]\n        print(stage, \"pending ui\", pc, \"export_case\", c[\"pending_count\"], \"rejected in flags:\", [f[\"id\"] for f in c[\"flags\"] if f.get(\"state\")==\"rejected\"])\n        blob = json.dumps(c, default=str)\n        if out: \n            blob += json.dumps(out, default=str)\n            try: blob += json.dumps(ER.export_payload(\"tok\", c), default=str)\n            except Exception as e: print(\"payload\", type(e).__name__)\n            print(\" notes count line:\", [l for l in out[\"internal_notes_text\"].splitlines() if \"not reviewed\" in l])\n        print(\" markers present:\", [m for m in M+[] if m in blob], \"'ZQ-NV' in blob:\", \"ZQ-NV\" in blob)\n        t = trace.case_trace(conn, cid)\n        print(\" gate:\", {k: t[\"gate\"].get(k) for k in t[\"gate\"] if k in (\"ready\",\"pending\",\"counts\")} if isinstance(t.get(\"gate\"), dict) else t.get(\"gate\"))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/t126r2/probe/probe4.py $PWD 2>&1 | tail -30"
}
````

### User / tool · 2026-11-02T11:50:24.025Z

**tool result**
````
j4 {'verdict': 'disagree', 'reason_code': 'NONE'} rejected flags: [('f_r4_1', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_2', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_3', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_4', ['LLM_ONLY', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r4_5', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r4_6', ['FILTERED_BY_RULE']), ('f_r6_2', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r6_3', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r6_4', ['LLM_ONLY', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r6_5', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r6_6', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM'])]
before_accept pending ui 23 export_case 23 rejected in flags: []
payload ExportBlocked
 notes count line: ['This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 23.', '- Record 1 (Austin EMS run report, January 9, 2026) — not reviewed', '- Record 2 (Central ER discharge summary, January 9, 2026) — not reviewed', '- Record 3 (Dr. Alvarez, primary care, January 16, 2026) — not reviewed', '- Record 4 (Capital PT, initial evaluation, January 23, 2026) — not reviewed', '- Record 5 (Capital PT, visit 8, February 20, 2026) — not reviewed', '- Record 6 (Capital PT, visit 9, March 6, 2026) — not reviewed', '- Record 7 (Hill Country Pain Management, new patient, May 18, 2026) — not reviewed', '- Record 8 (Austin Imaging, cervical MRI, May 29, 2026) — not reviewed', '- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026) — not reviewed']
 markers present: [] 'ZQ-NV' in blob: False
 gate: None
after_accept pending ui 0 export_case 0 rejected in flags: []
 notes count line: ['This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.']
 markers present: [] 'ZQ-NV' in blob: False
 gate: None
j4 None rejected flags: [('f_r4_1', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_2', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_3', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r4_4', ['LLM_ONLY', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r4_5', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r4_6', ['FILTERED_BY_RULE']), ('f_r6_2', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r6_3', ['GROUNDING_EXCERPT_NOT_VERBATIM', 'JUDGE_UNAVAILABLE']), ('f_r6_4', ['LLM_ONLY', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r6_5', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']), ('f_r6_6', ['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM'])]
before_accept pending ui 23 export_case 23 rejected in flags: []
payload ExportBlocked
 notes count line: ['This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 23.', '- Record 1 (Austin EMS run report, January 9, 2026) — not reviewed', '- Record 2 (Central ER discharge summary, January 9, 2026) — not reviewed', '- Record 3 (Dr. Alvarez, primary care, January 16, 2026) — not reviewed', '- Record 4 (Capital PT, initial evaluation, January 23, 2026) — not reviewed', '- Record 5 (Capital PT, visit 8, February 20, 2026) — not reviewed', '- Record 6 (Capital PT, visit 9, March 6, 2026) — not reviewed', '- Record 7 (Hill Country Pain Management, new patient, May 18, 2026) — not reviewed', '- Record 8 (Austin Imaging, cervical MRI, May 29, 2026) — not reviewed', '- Record 9 (Hill Country Pain Management, follow-up, June 12, 2026) — not reviewed']
 markers present: [] 'ZQ-NV' in blob: False
 gate: None
after_accept pending ui 0 export_case 0 rejected in flags: []
 notes count line: ['This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.']
 markers present: [] 'ZQ-NV' in blob: False
 gate: None
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:30.702Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; tail -3 $S/t126r2/unit.txt; cat $S/t126r1/probe/mut.py | head -40; grep -rn \"FILTERED_BY_RULE\" /Users/arsis/zlayt-pm-project/app --include=*.py | grep -v \"^.*#\" | head; grep -rn '\"FILTERED_BY_RULE\"\\|\\[:1\\] == \\[' $S/t126r2/a/app/backend/*.py | head"
}
````

### User / tool · 2026-11-02T11:50:30.891Z

**tool result**
````
........................................................................ [ 46%]
........................................................................ [ 48%]
.................................................................import sys, shutil, subprocess, os
src, work = sys.argv[1], sys.argv[2]
PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
muts = {
 "M1 merge drops filtered again": ("app/backend/flags.py", "            if k not in fseen:\n                fseen.add(k)\n                filtered.append(lf)\n", "            pass\n"),
 "M2 tray keeps filtered": ("app/backend/present.py", "if x not in filtered]", "]"),
 "M3 review_view counts filtered": ("app/backend/present.py", " and (r.get(\"state_reasons\") or [])[:1] != [FT.FILTERED]]", "]"),
 "M4 store.export_case includes filtered": ("app/backend/store.py", "        if (f.get(\"state_reasons\") or [])[:1] == [\"FILTERED_BY_RULE\"]:", "        if False:"),
 "M5 trace judge_rows counts filtered": ("app/backend/trace.py", "            if kind == \"flag\" and (row.get(\"state_reasons\") or [])[:1] == [\"FILTERED_BY_RULE\"]:", "            if False:"),
 "M6 trace gate flgs counts filtered": ("app/backend/trace.py", " if (x.get(\"state_reasons\") or [])[:1] != [\"FILTERED_BY_RULE\"]]", "]"),
 "M7 filtered not last": ("app/backend/flags.py", "+ _model_conflicts(conflicts, record, tagged) + last", "+ _model_conflicts(conflicts, record, tagged)"),
 "M8 tray_filtered collapsed False": ("app/backend/present.py", "\"collapsed\": True", "\"collapsed\": False"),
 "M9 filtered dedupe key drops category": ("app/backend/flags.py", "k = (lf[\"type\"], lf[\"category\"], grounding.normalize(lf[\"excerpt\"]))", "k = (lf[\"type\"],)"),
 "M10 _to_tray FILTERED reasons not set": ("app/backend/flags.py", "        f[\"reasons\"] = [FILTERED]\n", ""),
}
tests = "tests/unit/test_t126_filtered_by_rule.py tests/unit/test_flags_pass.py"
only = sys.argv[3:] 
for name, (path, old, new) in muts.items():
    if only and not any(name.startswith(o) for o in only): continue
    d = work + "/m"
    shutil.rmtree(d, ignore_errors=True); shutil.copytree(src, d)
    p = os.path.join(d, path); s = open(p).read()
    assert old in s, name
    open(p, "w").write(s.replace(old, new, 1))
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "-x", *tests.split()], cwd=d, capture_output=True, text=True)
    print(name, "->", "KILLED" if r.returncode else "SURVIVED", r.stdout.strip().splitlines()[-1])
/bin/bash: child setpgid (64276 to 64276): Operation not permitted
/Users/arsis/zlayt-pm-project/app/backend/why.py:26:    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
/Users/arsis/zlayt-pm-project/app/backend/confidence.py:14:    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
/Users/arsis/zlayt-pm-project/app/backend/flag_templates.py:221:FILTERED = "FILTERED_BY_RULE"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/a/app/backend/confidence.py:14:    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/a/app/backend/flag_templates.py:221:FILTERED = "FILTERED_BY_RULE"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/a/app/backend/flag_templates.py:226:    return list(reasons or [])[:1] == [FILTERED]
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t126r2/a/app/backend/why.py:26:    "FILTERED_BY_RULE": "The AI proposed this as a flag, but a fixed rule filtered it out (see the rule named with it). It is listed so nothing the AI proposed is hidden; it is not a flag and needs no action.",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:33.338Z

**tool call — Bash**
````
{
 "command": "grep -rn \"FILTERED\\|is_filtered\" app evals --include=*.py --include=*.js --include=*.html | grep -v \"^app/backend/why.py\" | cut -c1-170"
}
````

### User / tool · 2026-11-02T11:50:33.431Z

**tool result**
````
app/backend/trace.py:763:            if kind == "flag" and FT.is_filtered(row.get("state_reasons")):      # D-057: never judged, never counted
app/backend/trace.py:912:    flgs = [x for x in DB.list_items(conn, case_id, "flag") if not FT.is_filtered(x.get("state_reasons"))]      # D-057: rule-filtered proposals 
app/backend/confidence.py:14:    "AI_TRANSLATION", "SUMMARY_NOT_IN_QUOTE", "FILTERED_BY_RULE",
app/backend/present.py:189:    items = [(k, r) for k, r in items if r["id"] not in handled and not FT.is_filtered(r.get("state_reasons"))]       # D-057: rule-filtered pr
app/backend/present.py:291:    filtered = [x for x in rejected_flags if FT.is_filtered(x["reasons"])]
app/backend/flag_templates.py:221:FILTERED = "FILTERED_BY_RULE"
app/backend/flag_templates.py:224:def is_filtered(reasons) -> bool:
app/backend/flag_templates.py:226:    return list(reasons or [])[:1] == [FILTERED]
app/backend/flags.py:22:FILTER_RULES, FILTERED = FT.FILTER_RULES, FT.FILTERED       # D-057 (T-126): data lives in flag_templates so present.py can read it without import
app/backend/flags.py:178:        f["_tray"] = FILTERED
app/backend/flags.py:358:    if code == FILTERED:
app/backend/flags.py:360:        f["reasons"] = [FILTERED] + [r for r in f["reasons"] if r not in (FILTERED, "JUDGE_UNAVAILABLE", "LLM_ONLY")]       # keeps a grounding f
app/backend/flags.py:361:        f["why"] = why.why(FILTERED) + ("" if "GROUNDING_EXCERPT_NOT_VERBATIM" not in f["reasons"] else " " + why.why("GROUNDING_EXCERPT_NOT_VERB
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:37.048Z

**tool call — Bash**
````
{
 "command": "sed -n 121,175p tests/unit/test_t126_filtered_by_rule.py"
}
````

### User / tool · 2026-11-02T11:50:37.132Z

**tool result**
````
def test_tray_flags_are_not_counted_by_the_review_counts_the_gate_or_the_judge_rows(tmp_path):
    conn, cid = _stored(tmp_path)
    filtered, other = _tray_flag_ids(conn, cid)
    v = present.case_view(conn, cid, backend="fixture", models={}, demo_mode=False)
    assert not filtered & {t["id"] for t in v["tray"]} and not (filtered | other) & set(v["review"]["queue"])
    all_rejected = [r["id"] for k in ("entry", "amount", "flag") for r in DB.list_items(conn, cid, k) if r["state"] == "rejected"]
    assert v["review"]["counts"]["rejected"] == len([i for i in all_rejected if i not in filtered]) > 0     # filtered ones are not in the rejected count either
    assert not filtered & {j["item_id"] for j in trace._judge_rows(trace._Cx(conn, cid, True))}
    assert sum(p["items"] for p in trace.judge_report(conn, cid)["judges"]) == len(trace._judge_rows(trace._Cx(conn, cid, False)))
    t = trace.case_trace(conn, cid)
    gate = next(s for s in t["steps"] if s["id"] == "export_gate")
    assert gate["counts"]["pending_items"] == v["review"]["counts"]["pending"]
    live = [(k, r) for k in ("entry", "amount", "flag") for r in DB.list_items(conn, cid, k) if not FT.is_filtered(r.get("state_reasons"))
            and not (r.get("ladder") or {}).get("failure")]
    grounding_step = next(s for s in t["steps"] if s["id"] == "grounding")
    assert grounding_step["counts"]["items_checked"] == len(live)               # a rule-filtered proposal is not an item the checks ran over
    assert grounding_step["counts"]["rejected"] == sum(1 for _, r in live if r["state"] == "rejected")
    assert gate["counts"]["rejected_not_blocking"] == grounding_step["counts"]["rejected"]
    assert not any(i in json.dumps(t) for i in filtered)


def test_one_helper_names_the_marker():
    assert FT.is_filtered(["FILTERED_BY_RULE", "GROUNDING_EXCERPT_NOT_VERBATIM"]) and not FT.is_filtered(["LLM_ONLY", "FILTERED_BY_RULE"]) and not FT.is_filtered(None)
    import pathlib
    lits = sorted(p.name for p in pathlib.Path("app/backend").glob("*.py") if '"FILTERED_BY_RULE"' in p.read_text())
    assert lits == ["confidence.py", "flag_templates.py", "why.py"], lits       # the code list, the constant, the reason sentence: no copy in a reader


def test_same_quote_different_category_keeps_one_flag_and_names_the_other_category():
    r = dict(R, excerpt="Patient reports prior neck pain. Ankle exam normal.")
    llm = [dict(type="pre_existing", category="prior_condition", excerpt="prior neck pain"),
           dict(type="pre_existing", category="degenerative_language", excerpt="prior neck pain"),
           dict(type="pre_existing", category="prior_condition", excerpt="prior neck pain")]            # the same category again: nothing to say
    out = [f for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm}})) if f["type"] == "pre_existing"]
    assert len(out) == 1 and out[0]["ladder"]["code_checks"]["merged_categories"] == ["degenerative_language"]
    lone = [f for f in F.run_flag_pass(r, call=FakeCall({"flags": {"flags": llm[:1]}})) if f["type"] == "pre_existing"]
    assert "merged_categories" not in lone[0]["ladder"]["code_checks"]


def test_the_merge_shows_in_the_item_trace(tmp_path):
    llm = [dict(type="causation", category="causation_language", excerpt="Discharged from PT after two missed appointments."),
           dict(type="causation", category="mechanism_language", excerpt="Discharged from PT after two missed appointments.")]
    conn, cid, _v = _view(tmp_path, llm)
    rows = [r for r in DB.list_items(conn, cid, "flag") if (r.get("ladder") or {}).get("code_checks", {}).get("merged_categories")]
    assert rows, "the stored flag keeps the merged category"
    tr = trace.item_trace(conn, cid, rows[0]["id"]) if hasattr(trace, "item_trace") else None
    assert tr is not None and any(s["id"] == "proposals_merged" for s in tr["steps"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:50:48.327Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > $S/t126r2/probe/mut.py <<'EOF'\nimport sys, shutil, subprocess, os\nsrc, work = sys.argv[1], sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nmuts = {\n \"N1 export_case skips nothing\": (\"app/backend/store.py\", '        if f[\"state\"] == \"rejected\":', \"        if False:\"),\n \"N2 export_case skips only filtered (r1 bug)\": (\"app/backend/store.py\", '        if f[\"state\"] == \"rejected\":', '        if (f.get(\"state_reasons\") or [])[:1] == [\"FILTERED_BY_RULE\"]:'),\n \"N3 export_case skips only judge-unavailable\": (\"app/backend/store.py\", '        if f[\"state\"] == \"rejected\":', '        if \"JUDGE_UNAVAILABLE\" in (f.get(\"state_reasons\") or []):'),\n \"M3 review_view counts filtered\": (\"app/backend/present.py\", \" and not FT.is_filtered(r.get(\\\"state_reasons\\\"))]\", \"]\"),\n \"M5 judge_rows counts filtered\": (\"app/backend/trace.py\", 'if kind == \"flag\" and FT.is_filtered(row.get(\"state_reasons\")):', \"if False:\"),\n \"M6 gate flgs counts filtered\": (\"app/backend/trace.py\", ' if not FT.is_filtered(x.get(\"state_reasons\"))]', \"]\"),\n \"M2 tray keeps filtered\": (\"app/backend/present.py\", \"if x not in filtered]\", \"]\"),\n \"M10 _to_tray drops other reasons\": (\"app/backend/flags.py\", '[FILTERED] + [r for r in f[\"reasons\"] if r not in (FILTERED, \"JUDGE_UNAVAILABLE\", \"LLM_ONLY\")]', \"[FILTERED]\"),\n \"R1 why omits not-verbatim note\": (\"app/backend/flags.py\", ' + (\"\" if \"GROUNDING_EXCERPT_NOT_VERBATIM\" not in f[\"reasons\"] else \" \" + why.why(\"GROUNDING_EXCERPT_NOT_VERBATIM\"))', \"\"),\n \"R2 _merged never recorded in merge\": (\"app/backend/flags.py\", 'seen[k][\"_merged\"].append(lf.get(\"category\"))', \"pass\"),\n \"R3 ground() wipes merged_categories\": (\"app/backend/flags.py\", '{k: v for k, v in (f[\"ladder\"].get(\"code_checks\") or {}).items() if k == \"merged_categories\"}', \"{}\"),\n \"R4 _note_merged not called for both-origin\": (\"app/backend/flags.py\", \"            _note_merged(lx, uniq[match])\\n\", \"\"),\n \"R5 _note_merged not called for llm-only\": (\"app/backend/flags.py\", \"        _note_merged(f, lf)\\n\", \"\"),\n \"R6 trace step proposals_merged removed\": (\"app/backend/trace.py\", \"    if merged:\\n        st.insert\", \"    if False:\\n        st.insert\"),\n \"R7 is_filtered always False\": (\"app/backend/flag_templates.py\", \"return list(reasons or [])[:1] == [FILTERED]\", \"return False\"),\n}\ntests = \"tests/unit/test_t126_filtered_by_rule.py\"\nonly = sys.argv[3:]\nfor name, (path, old, new) in muts.items():\n    if only and not any(name.startswith(o) for o in only): continue\n    d = work + \"/m\"\n    shutil.rmtree(d, ignore_errors=True); shutil.copytree(src, d)\n    p = os.path.join(d, path); s = open(p).read()\n    assert old in s, name\n    open(p, \"w\").write(s.replace(old, new, 1))\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", *tests.split()], cwd=d, capture_output=True, text=True)\n    fails = [l for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n    print(name, \"->\", \"KILLED\" if r.returncode else \"SURVIVED\", r.stdout.strip().splitlines()[-1], [f.split(\"::\")[-1][:60] for f in fails][:3], flush=True)\nEOF\ncd $S/t126r2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I probe/mut.py $PWD/a $PWD 2>&1 | tail -20"
}
````

### User / tool · 2026-11-02T11:51:12.096Z

**tool result**
````
N1 export_case skips nothing -> KILLED 2 failed, 9 passed in 0.69s ['test_case_payload_has_a_collapsed_counted_group_with_the_rul', 'test_every_tray_flag_stays_out_of_the_export_pending_count_a']
N2 export_case skips only filtered (r1 bug) -> KILLED 2 failed, 9 passed in 0.67s ['test_every_tray_flag_stays_out_of_the_export_pending_count_a', 'test_one_helper_names_the_marker']
N3 export_case skips only judge-unavailable -> KILLED 2 failed, 9 passed in 0.68s ['test_case_payload_has_a_collapsed_counted_group_with_the_rul', 'test_every_tray_flag_stays_out_of_the_export_pending_count_a']
M3 review_view counts filtered -> KILLED 1 failed, 10 passed in 0.70s ['test_tray_flags_are_not_counted_by_the_review_counts_the_gat']
M5 judge_rows counts filtered -> KILLED 1 failed, 10 passed in 0.77s ['test_tray_flags_are_not_counted_by_the_review_counts_the_gat']
M6 gate flgs counts filtered -> KILLED 1 failed, 10 passed in 0.66s ['test_tray_flags_are_not_counted_by_the_review_counts_the_gat']
M2 tray keeps filtered -> KILLED 2 failed, 9 passed in 0.66s ['test_case_payload_has_a_collapsed_counted_group_with_the_rul', 'test_tray_flags_are_not_counted_by_the_review_counts_the_gat']
M10 _to_tray drops other reasons -> KILLED 1 failed, 10 passed in 0.70s ['test_the_grounding_failure_stays_on_a_filtered_item_and_the_']
R1 why omits not-verbatim note -> KILLED 1 failed, 10 passed in 0.70s ['test_the_grounding_failure_stays_on_a_filtered_item_and_the_']
R2 _merged never recorded in merge -> KILLED 2 failed, 9 passed in 0.68s ['test_same_quote_different_category_keeps_one_flag_and_names_', 'test_the_merge_shows_in_the_item_trace']
R3 ground() wipes merged_categories -> KILLED 2 failed, 9 passed in 0.70s ['test_same_quote_different_category_keeps_one_flag_and_names_', 'test_the_merge_shows_in_the_item_trace']
R4 _note_merged not called for both-origin -> KILLED 1 failed, 10 passed in 0.66s ['test_same_quote_different_category_keeps_one_flag_and_names_']
R5 _note_merged not called for llm-only -> KILLED 1 failed, 10 passed in 0.72s ['test_the_merge_shows_in_the_item_trace']
R6 trace step proposals_merged removed -> KILLED 1 failed, 10 passed in 0.71s ['test_the_merge_shows_in_the_item_trace']
R7 is_filtered always False -> KILLED 4 failed, 7 passed in 0.66s ['test_case_payload_has_a_collapsed_counted_group_with_the_rul', 'test_no_model_proposal_is_dropped_silently_counts_match', 'test_every_tray_flag_stays_out_of_the_export_pending_count_a']
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:51:23.736Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd $S/t126r2/a; cat > $S/t126r2/probe/probe5.py <<'EOF'\nimport sys\nsys.path.insert(0, sys.argv[1])\nfrom app.backend import flags as F\nfrom tests.unit._fakes import FakeCall\nR = dict(n=1, source=\"EMS\", excerpt=\"Patient reports low back pain in 2023, resolved. Ankle exam normal.\", date_iso=\"2026-06-01\")\nfor cats in ([\"degenerative_language\"], [\"degenerative_language\",\"new_onset\"], [\"prior_condition\"]):\n    llm = [dict(type=\"pre_existing\", category=c, excerpt=\"Patient reports low back pain in 2023, resolved.\") for c in cats]\n    out = F.run_flag_pass(R, call=FakeCall({\"flags\": {\"flags\": llm}}))\n    print(cats, [(f[\"category\"], f[\"origin\"], f[\"ladder\"].get(\"code_checks\",{}).get(\"merged_categories\")) for f in out])\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $S/t126r2/probe/probe5.py $PWD 2>&1 | tail -5; tail -2 $S/t126r2/unit.txt"
}
````

### User / tool · 2026-11-02T11:51:24.149Z

**tool result**
````
['degenerative_language'] [('pre_existing', 'both', None)]
['degenerative_language', 'new_onset'] [('pre_existing', 'both', ['new_onset'])]
['prior_condition'] [('pre_existing', 'both', None)]
/bin/bash: child setpgid (66089 to 66089): Operation not permitted
........................................................................ [ 50%]
.............................
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:51:31.818Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for i in $(seq 1 50); do if tail -1 $S/t126r2/unit.txt | grep -q \"passed\\|failed\\|error\"; then break; fi; sleep 8; done; tail -4 $S/t126r2/unit.txt"
}
````

### User / tool · 2026-11-02T11:52:52.144Z

**tool result**
````
........................................................................ [ 96%]
........................................................................ [ 98%]
..................................                                       [100%]
3126 passed, 4 skipped in 184.47s (0:03:04)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:52:57.636Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD; grep -c \"D-057\" docs/LLM_VS_CODE.md; python3 tools/board.py show T-109 | grep -n \"D-057\" | cut -c1-260; grep -n \"tray_filtered\" memory/contracts/api.md | head -3 | cut -c1-120; grep -n \"D-057\" memory/SCOPE_CUTS.md | head -3"
}
````

### User / tool · 2026-11-02T11:52:57.822Z

**tool result**
````
a44dced
0
60:- 2026-11-02T11:45:38Z backend: From T-126 r2 (staff review minor 5): docs/LLM_VS_CODE.md rows 11/12 describe D-053 only. Please add one sentence for D-057: a model flag that a fixed code rule filters out (today D-032 objective_negative) is listed in a coll
131:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain 
237:  "tray_filtered": {
766:| `FILTERED_BY_RULE` | rejected | D-057 / T-126: the AI proposed a flag that a fixed code rule filtered out (today D
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:52:59.936Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-109 | sed -n 1,16p | cut -c1-200"
}
````

### User / tool · 2026-11-02T11:53:00.135Z

**tool result**
````
---
id: "T-109"
title: "LLM_VS_CODE row 11: conflicts are code-proposed candidates classified by judge_conflict_v4; model-only flags rejected by the flag judge are suppressed and listed"
milestone: "M2"
role: "architect"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:30:37Z"
updated_at: "2026-11-02T11:45:38Z"
claimed_by: "architect"
claimed_at: "2026-11-02T09:21:29Z"
rounds: 2
commits: ["bf0c748", "4bdf366"]
reviews:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:53:22.094Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer-r2.md",
 "content": "# T-126 review (round 2) — staff-engineer-reviewer\n\nScope: commit a44dced (HEAD, confirmed with `git rev-parse --short HEAD` = a44dced), checked on a `git archive HEAD` copy in the scratchpad (`t126r2/a`). Round 1 is `reviews/T-126-staff-engineer.md`.\n\nVerdict: pass. The round-1 major is fixed. `store.export_case` now skips every `state == \"rejected\"` flag, so no tray flag counts as pending or prints in the notes or the letter. One minor remains (the merge record is incomplete when a lexicon flag pairs with the model flag).\n\nDeterministic results:\n- `.venv/bin/python -m pytest tests/unit -q` on the archive: `3126 passed, 4 skipped in 184.47s`. The handoff says 3129; the difference is working-tree-only tests, not a failure.\n- `tests/unit/test_t126_filtered_by_rule.py`: 11 tests, all pass.\n\nRound-1 repro (probe1, unchanged script):\n- Before: `review.counts.pending` 23, `export_case.pending_count` 24, notes \"Items not reviewed: 24\", and a PENDING line printed the non-record quote \"Discharged from PT after two missed appointments.\" under record 4.\n- Now: `export_case` pending_count 23, notes \"Items not reviewed: 23\", `f_r4_1` stays in the tray (GROUNDING_EXCERPT_NOT_VERBATIM) and is not in `export_case.flags`. The 23 \"- \" lines under PENDING ITEMS NOT INCLUDED match the count, and the only \"Discharged from PT after two missed appointments.\" lines are record 6, which does contain it.\n\nWider probe (probe4): model flags on records 4 and 6 using four quotes that exist nowhere (objective_negative, degenerative_language, prior_condition, scene_facts) plus two verbatim ones.\n- Eleven rejected flags in the tray (JUDGE_UNAVAILABLE, LLM_ONLY and FILTERED_BY_RULE, each with GROUNDING_EXCERPT_NOT_VERBATIM; two FILTERED with and without it).\n- Before accepting anything and after accepting every live item: UI pending == `export_case.pending_count` (23 and 0). No rejected flag is in `export_case.flags`.\n- The marker `ZQ-NV` is absent from the whole `export_case` JSON, `build_export` output and `export_routes.export_payload`.\n- Run with the fixture J4 both \"disagree\" and default; same results.\n\nMutants (T-126 test file only, 15 mutants, all KILLED): N1 export skip removed, N2 skip only FILTERED (the round-1 bug), N3 skip only JUDGE_UNAVAILABLE, M2 tray keeps filtered, M3 review_view counts filtered, M5 judge rows count filtered, M6 gate counts filtered, M10 `_to_tray` drops other reasons, R1 why loses the not-verbatim note, R2 merge does not record, R3 `ground()` wipes the merge note, R4 and R5 `_note_merged` not called on the two paths, R6 trace step removed, R7 `is_filtered` always False. Round-1 survivors M3-M6 now die in the card's own tests.\n\nMinors from round 1:\n- Grounding reason on filtered items: fixed. probe2 gives `['FILTERED_BY_RULE', 'GROUNDING_EXCERPT_NOT_VERBATIM']`, and with an injection tag `INJECTION_SUSPECTED` as well; the `why` says \"not word for word\".\n- Merge trace: recorded (`ladder.code_checks.merged_categories`, trace step `proposals_merged`) but see finding 1.\n- api.md: the GET example has `tray_filtered`, and the FILTERED_BY_RULE row covers all tray flags.\n- Single marker: `grep FILTERED app` shows one definition (`flag_templates.FILTERED`) and one predicate (`is_filtered`), used in trace.py (2), present.py (2) and flags.py. The remaining literals are `confidence.py:14` (reason-code list) and `why.py:26` (sentence key), which are vocabulary tables, not checks.\n- `docs/LLM_VS_CODE.md` rows 11 and 12 still have no D-057 sentence (`grep -c D-057` = 0). The handoff moved it to an open architect card (T-109, in_progress, note at line 60), so I am not filing it again.\n\n## Findings\n1. Minor: when a lexicon flag pairs with the model flag, the model's own category is not in the record.\n   - `flags.py` `_note_merged` lists only categories other than the first model flag's.\n   - probe5 gives `['degenerative_language'] -> category pre_existing, origin both, merged_categories None`, and `['degenerative_language','new_onset'] -> merged_categories ['new_onset']`.\n   - The new api.md text says \"code keeps one flag and lists the others\"; here the first-proposed category is not listed, only the later ones.\n   - This is smaller than the round-1 loss. A lexicon flag is the code-confirmed one, and keeping the lexicon category predates this card.\n   - Fix: when a lexicon flag pairs, record the model's category in `merged_categories` too, or state in api.md that the list names only the extra categories.\n\n```json\n{\"card\": \"T-126\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit a44dced (HEAD); git archive HEAD in scratchpad t126r2/a; reviews/T-126-staff-engineer.md round 1; sample case via FakeCall; memory/contracts/api.md\",\n \"exercised\": [\"git rev-parse --short HEAD = a44dced; git show a44dced -- app memory read in full\", \"pytest tests/unit -q on the archive: 3126 passed, 4 skipped in 184.47s\", \"round-1 probe1 re-run: pending 23 == export_case pending_count 23, notes 'Items not reviewed: 23', no record-4 non-record quote\", \"probe4: four non-record quotes across objective_negative/degenerative_language/prior_condition/scene_facts plus verbatim ones; 11 rejected tray flags; before/after accepting every live item; export_case, build_export and export_payload JSON scanned for the marker (absent)\", \"probe2/probe2b: filtered proposal with non-verbatim quote keeps GROUNDING_EXCERPT_NOT_VERBATIM and INJECTION_SUSPECTED\", \"probe3/3b/5: same-quote merge, merged_categories, lexicon-paired case\", \"15 mutants N1-N3, M2, M3, M5, M6, M10, R1-R7 against tests/unit/test_t126_filtered_by_rule.py: all killed\", \"grep FILTERED/is_filtered across app and evals; read tests/unit/test_t126_filtered_by_rule.py (11 tests); api.md example and reason-code row; docs/LLM_VS_CODE.md grep D-057; board show T-109\"],\n \"verdict\": \"pass\",\n \"scores\": {\"d057_filter_placement\": 5, \"no_silent_drop\": 4, \"tests_pin_behaviour\": 5, \"contract_docs\": 4, \"determinism_ids\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"merged_categories omits the model's own category when a lexicon flag pairs with it\",\n   \"evidence\": \"app/backend/flags.py _note_merged: extra = sorted(c for c in lf.get('_merged', []) if c and c != f['category']); probe5 (scratchpad t126r2/probe/probe5.py): ['degenerative_language'] gives (pre_existing, both, None); ['degenerative_language','new_onset'] gives merged_categories ['new_onset'] (degenerative_language not named).\",\n   \"why_it_matters\": \"api.md and the handoff say the other categories the model proposed for one quote are listed on the kept flag (D-053: nothing proposed is silently lost); on the both path the first one is not.\",\n   \"fix\": \"In the lexicon-paired path, include the first model flag's category in merged_categories when it differs from the lexicon category, or narrow the api.md sentence to say the list names only the extra categories.\",\n   \"acceptance_test\": \"A lexicon-paired flag with model categories [degenerative_language, new_onset] yields merged_categories containing both.\"}\n ],\n \"whats_right\": [\"export_case skips on state == rejected, the one predicate that covers judge-rejected, not-verbatim and rule-filtered flags, and the test builds the export from the stored case\", \"FT.is_filtered is the single marker predicate and a test pins that no reader carries a literal\", \"All 15 mutants die in the card's own test file, including the round-1 survivors M3-M6\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T11:53:22.259Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T11:53:24.648Z

Verdict is **pass**. The round-1 major is fixed, and I filed one minor. The unit suite is 3126 passed and 4 skipped on a `git archive` of HEAD a44dced (the handoff says 3129). No tray flag counts as pending or prints in the notes or letter (23 equals 23), and no non-record quote reaches any export. All 15 mutants die in the card's own tests.

The minor: when a lexicon flag pairs with a model flag, `merged_categories` leaves out the model's first category. Review file: `/Users/arsis/zlayt-pm-project/reviews/T-126-staff-engineer-r2.md`.
