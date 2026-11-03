# Subagent: T-103 r2 check (haiku staff) (T-103 r2 check (haiku staff))

Source: `agent-ad52e1ada2d041276.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:06:20.359Z

Round-2 check of board card T-103 (billing as a cited line listing) in /Users/arsis/zlayt-pm-project (commit bcdcb91). Read reviews/T-103-staff-engineer.md and D-052, applied strictly: no sums or comparisons of any kind. Removing BALANCE_STEP_MISMATCH is in line with that.

On a `git archive HEAD` copy in your scratchpad, re-run your r1 probes and confirm:
- the per-service sums and EOB-versus-ledger checks are gone;
- an EOB amount with no cents appears as a line or as unreconciled;
- the fail-safe accounting test covers EOB records and fails when a token is made to drop (mutate in a scratch copy);
- the route output has no total-like fields.

Run `.venv/bin/python -m pytest -q tests/unit/test_billing.py`. Write reviews/T-103-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:22.062Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T06:06:22.072Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:22.331Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t103_listing_review_patterns.md"
}
````

### User / tool · 2026-11-02T06:06:22.340Z

**tool result**
````
1	---
2	name: t103-listing-review-patterns
3	description: T-103 r1 (2dc5be2, fail): fail-safe oracle exempts whole payer/rate rows so drops inside them pass, a kept EOB check silently skips on an unreadable figure, per-service sums shown in check objects against D-052
4	metadata:
5	  type: project
6	---
7	
8	T-103 r1 (2dc5be2, billing as a cited line listing, D-052). Verdict fail: 2 blockers, 3 majors, 2 minors, 1 nit. Review at reviews/T-103-staff-engineer.md; evidence in artifacts/review-evidence/T-103-r1/ (RUN_ORDER.txt, mutation_results.txt).
9	
10	- **A fail-safe oracle that exempts whole rows cannot fail for drops inside them.** `unaccounted()` marks every payer-report line and every rate/LOP entry as accounted for its whole excerpt (test_billing.py `_items`, `whole=True`). Mutant: EOB row `unclear` emptied, 157/157 green. Probe: EOB billed "$140" is in no structured field. Check the oracle's own exemptions before trusting a "every token accounted" test.
11	- **A kept reconciliation check that skips on an unreadable input is a silent fallback.** `if not led or not el.get("billed"): continue` (billing.py ~859) drops the EOB billed comparison when the EOB figure has no cents. Printed $140 vs ledger 130.00 raises nothing; the control "140.00" raises LEDGER_EOB_BILLED_MISMATCH.
12	- **Removing a sum from a total field does not remove sums.** The EOB check objects carried `ledger: {cents, usd}` computed by `_sum`. Grep every dict a check emits for `_sum`/`_tot` output, not just the top-level total keys.
13	- **Partial sums hide the discrepancy they should show.** `_sum` drops unclear rows, so a same-service second charge that cannot be read leaves the check agreeing with the EOB (silent pass).
14	- **Docstring and API doc say "no balance reconciliation" while a per-line balance check exists** (BALANCE_STEP_MISMATCH). Mismatch between doc and code is a finding even when the code is arithmetically sound.
15	- **Pre-existing red at HEAD:** tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts fails on 841be23 and on 2dc5be2. Not a billing finding; check its own card before blaming a commit.
16	
17	**Why:** r1 found that the T-083 fail-safe was fixed for parser shapes and tested through an oracle with whole-row exemptions, and the EOB path had no accounting pass at all.
18	
19	**How to apply:** for any "every token is accounted" card, (1) list the oracle's exemptions and mutate each exempt path; (2) add an EOB/payer-style probe with a no-cents figure; (3) grep check payloads for sums; (4) when a check says "agrees", probe a case where one input row is unreadable.
20	
21	**Method notes (this card):**
22	- Scratch mutation runs: copy the archive per mutant, replace with exact-once matches (run_mutants.py). A board-guard hook blocked an in-place `sed -i` on a scratch helper, so write fresh files instead.
23	- Non-zero D-019 totals need charges accepted: POST each charge to `/api/cases/{token}/items/{id}/review` with `{"action": "accept"}`, then `present.totals_view`. Ingest alone gives accepted 0.
24	- Copy timings and counts from the tool output, not from memory. My r1 body had the wrong archive timing and an overstated verifier scope (corrected in artifacts/review-evidence/T-103-r1/CORRECTION-1.txt, since the review file is write-once).
25	
26	See also [[t083-billing-review-patterns]], [[t083-r4-accounting-patterns]], [[t083-r5-cross-family-patterns]], [[feedback_review_write_once]].
27	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:22.535Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer.md"
}
````

### User / tool · 2026-11-02T06:06:22.548Z

**tool result**
````
1	# T-103 staff-engineer review, r1 (commit 2dc5be2)
2	
3	Reviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (as dispatched). CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed.
4	
5	**Verdict: fail.** Two blockers, three majors, two minors, one nit.
6	
7	**Your two calls.**
8	- Per-service EOB-vs-ledger checks: keep the mismatch flags. They are reconciliations, not totals, and nothing from them reaches the letter. Reject what they carry: the per-service billed and paid sums (B2) and the silent skip when a figure is unreadable (B1, M1). Compare row by row.
9	- Rates, LOP amounts, printed totals and balance forwards as lines with `detail`: accepted. Probe results: rate gives class rate, detail rate; LOP gives unclear with detail reduction, asserted_balance or lien_amount; printed totals give unclear with detail stated_total_billed/paid/adjustment/balance; balance forward gives unclear with detail balance_forward; estimate gives unclear with detail estimate. Caveats are M2 and m2.
10	
11	**Pin.** HEAD is 2dc5be2 (`git rev-parse HEAD`). `git show --stat 2dc5be2` lists app/backend/billing.py, tests/unit/test_billing.py and memory/contracts/api.md only. Those three files are clean in the working tree (`git status --short` shows nothing for them). Checks ran on `git archive 2dc5be2` and on the parent `git archive 841be23`.
12	
13	**Brief checks.**
14	1. Route returns only cited lines, unreconciled rows, skipped records and payer reports: partly. Lines, unreconciled rows, skipped records and payer lines carry verbatim excerpts, and `verify_citations` returned [] on every probe and golden case I ran. Not met for EOB figures without a decimal point (B1).
15	2. No provider totals, complete flag or balance sums: `complete`, `providers`, `totals`, `stated_totals` and `balance_convention` are absent from the route output. Not met: payer checks carry per-service billed and paid sums (B2). The per-line BALANCE_STEP check remains (m1).
16	3. D-019 case total unchanged: met. `totals.py`, `present.py` and `api.py` are not touched by the commit. Accepting every charge and reading `present.totals_view` gives identical output at 2dc5be2 and 841be23: case_03 $335.00, case_09 $275.00, sample $8,390.00.
17	4. Fail-safe test under a scratch-copy drop: met for parser drops. M02, M03, M04 and M07 each turn the random-insertion property test red, and M01 (accounting net off) does too. Not met for EOB and payer rows: M06 (an EOB unreadable figure dropped) leaves 157 of 157 green (M3).
18	5. `test_fixture_runs_write_no_artifacts`: fails on the archive. It is unrelated to T-103. It lives in tests/unit/test_t093_eval_signature.py, imports evals.run, and fails the same way on the parent 841be23. The commit touches none of those files. It is a red at HEAD and needs its own card. I did not run the full tests/unit suite.
19	6. `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: 157 passed in 1.06s on the project tree and in 1.06s on the archive copy.
20	
21	**Strongest evidence.**
22	- Printed EOB billed '$140' against a ledger 130.00 for the same service and date: no LEDGER_EOB_BILLED_MISMATCH, and the oracle reports nothing unaccounted. The same probe with '140.00' raises the mismatch (artifacts/review-evidence/T-103-r1/eob_mismatch_output.txt). The route response for this case has no billed figure on the EOB row (artifacts/review-evidence/T-103-r1/route_eob140.json).
23	- The same route response carries `{'code': 'LEDGER_EOB_PAID_MISMATCH', 'service': '97140', 'ledger': {'cents': 0, 'usd': '$0.00'}, ...}`, a per-service paid sum that D-052 forbids showing.
24	- Mutation runs (artifacts/review-evidence/T-103-r1/mutation_results.txt): every drop of a table, CMS, unreconciled or rate token is caught; the EOB drop is not.
25	
26	**Not exercised.** The full tests/unit suite; the frontend beyond a grep (no billing references); Spanish records; security depth (deferred to security-reviewer); UX copy. I did not run the app over HTTP on a port; the route was run through TestClient.
27	
28	```json
29	{"card": "T-103", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
30	 "scope": "git 2dc5be2 (HEAD at review time): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copies of git archive 2dc5be2 and parent 841be23; billing route via TestClient on evals/golden case_03_rate_and_ocr, case_09_nonvisit_hides_gap, sample and synthetic EOB probes; no app URL exercised",
31	 "exercised": [
32	   "git rev-parse HEAD -> 2dc5be21bd790d548ccdfce74c308aef88045ea9; git show --stat 2dc5be2 (3 files); git diff --name-only 841be23 2dc5be2 (billing.py, api.md, test_billing.py only)",
33	   "git status --short on app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md: clean",
34	   ".venv/bin/python -m pytest -q tests/unit/test_billing.py -> 157 passed in 1.06s (project tree and archive copy)",
35	   "test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts run on archive 2dc5be2 and parent 841be23: fails on both",
36	   "GET /api/cases/{token}/billing via TestClient (fixture backend, ingest only) on case_03, case_09, sample, and on synthetic EOB probe case_eob_140.txt",
37	   "D-019: accepted every charge via POST /api/cases/{token}/items/{id}/review, then present.totals_view, on case_03, case_09, sample at 2dc5be2 and 841be23: identical (accepted 33500, 27500, 839000 cents)",
38	   "read billing.py: analyze, _ledger_table, _ledger_text, _cms1500, _eob, _account, _checks_for_line, verify_citations, module docstring; read test_billing.py: helpers, PROBES, BARE_PROBES, unaccounted(), property test",
39	   "probe listings of T-083 PROBES (ledger, prose, CMS-1500, UB-04, rates, LOP, printed totals, balance forwards, EOB) via a loader of tests/unit/test_billing.py from the archive",
40	   "EOB probes: '$140' vs ledger 130.00 with '140.00' control; '$130' and '1O0.00' EOB figures; same-service second unreadable ledger row with EOB 130.00; rate row 'Charge per visit 185.00 999.00'; estimate row",
41	   "scratch-copy mutants M01-M08 (run_mutants.py, run_m04.py): full file and property/probe selections; results in artifacts/review-evidence/T-103-r1/mutation_results.txt",
42	   "grep billing.py and test_billing.py for float, except, sleep, retry, random; grep app/frontend for billing (no matches); memory/contracts/api.md lines 664, 692, 693; memory/ORCHESTRATOR_DECISIONS.md line 60 (D-052)",
43	   "evidence saved: artifacts/review-evidence/T-103-r1/ (RUN_ORDER.txt, mutation_results.txt, eob_mismatch_output.txt, route_eob140.json, pytest_billing_HEAD_2dc5be2.txt, probe scripts)"
44	 ],
45	 "verdict": "fail",
46	 "scores": {"fail_safe_completeness": 2, "decision_D052_conformance": 2, "honest_failure_no_silent_skip": 2, "api_doc_matches_code": 2, "money_integer_cents": 5, "no_llm_in_deterministic_path": 5, "test_mutation_catch": 3, "D019_total_unchanged": 5},
47	 "findings": [
48	   {"severity": "blocker", "title": "EOB money token lost from every structured field; the kept EOB-vs-ledger billed check silently skips; EOB records have no accounting pass",
49	    "evidence": "artifacts/review-evidence/T-103-r1/eob_mismatch_output.txt: EOB 97110 billed '$140' vs ledger 13000 cents -> 'EOB billed-mismatch checks for 97110: []' and 'oracle unaccounted: []'; control with '140.00' -> ['LEDGER_EOB_BILLED_MISMATCH']. route copy artifacts/review-evidence/T-103-r1/route_eob140.json: payer row 97110 has no billed key, unclear ['52.00','78.00']. Code: app/backend/billing.py:505 (_NUM is decimal-only), :511 row['unclear'], :859 'if not led or not el.get(billed): continue', :775-776 _account runs only for ledger_table, ledger_text, cms1500, ub04 (not eob). Test: tests/unit/test_billing.py:583 payer rows count as accounted (whole=True).",
50	    "why_it_matters": "D-049 (billing.py:13-18) and api.md:693 promise every money token is a line, an unreconciled row, an unclear figure on its row, or in skipped_records. '$140' is none of these. The EOB amount that disagrees with the ledger is not reported, and the fail-safe test cannot see it. A fact is lost and a check the worker kept silently does not run.",
51	    "fix": "(a) Run an accounting pass for form eob: add 'eob' to the form tuple at billing.py:775-776 with an EOB unit list (every $ figure, decimal or not, and every bare figure under a money column). (b) In _eob, when a service row's figures do not map to its columns, list each money token of the row as unclear, and raise a visible check when the billed or paid figure is unreadable instead of the continue at billing.py:859. (c) Stop whole=True for payer rows in tests/unit/test_billing.py:583 (see M3).",
52	    "acceptance_test": "New test: EOB 97110 billed '$140' against ledger 130.00 -> unaccounted() == [] AND the payer output carries a check for 97110 (LEDGER_EOB_BILLED_MISMATCH with 140, or an EOB-amount-unreadable check). Mutant M06 (drop the EOB unclear list) turns at least one test red."},
53	   {"severity": "blocker", "title": "Per-service ledger billed and paid sums are computed and shown on EOB payer checks (D-052)",
54	    "evidence": "artifacts/review-evidence/T-103-r1/route_eob140.json: payer_reports[0].checks = [{'code': 'LEDGER_EOB_PAID_MISMATCH', 'service': '97140', 'ledger': {'cents': 0, 'usd': '$0.00'}, 'eob': {'cents': 1600, ...}}]. Code: app/backend/billing.py:861 lb, lp = _sum(led, 'billed'), _sum(led, 'paid') or 0; :864 'ledger': _tot(lb); :866 'ledger': _tot(lp). Decision: memory/ORCHESTRATOR_DECISIONS.md:60 'no billed/paid/balance totals ... are computed or shown'. Spec: memory/contracts/api.md:664 'No provider totals, no billed/paid/balance sums'.",
55	    "why_it_matters": "A billed or paid sum is the mechanism D-052 retired (five review rounds found totals that silently omit figures). The output contradicts the binding decision and the API doc. A reader sees 'ledger $0.00' and takes it for the ledger's paid total. The sum is also partial: unreadable rows are left out of _sum (see M1).",
56	    "fix": "Remove the 'ledger' value from both checks. Cite the matching ledger rows by their own excerpt and their own figures. Compare row by row (each ledger row for that service and date against the EOB figure), so no sum is computed anywhere. Keep the check codes and the mismatch flag, which are consistent with D-052.",
57	    "acceptance_test": "Route output for any raised payer check contains no 'ledger' key holding a cents value; the check's cites list the ledger rows with their own excerpts. Test: assert 'ledger' not in each payer check, and that each cite excerpt is a ledger row."},
58	   {"severity": "major", "title": "Kept per-service check goes silent when one same-service ledger row is unreadable",
59	    "evidence": "artifacts/review-evidence/T-103-r1/eob_probe2.py (ledger 97110 on 06/10/26 twice: one 130.00 parsed, one bare '130' -> LINE_UNCLEAR; EOB 97110 130.00): output 'payer checks: [LEDGER_EOB_PAID_MISMATCH 97140]' with no BILLED mismatch. Code: app/backend/billing.py:859-861 sums only parsed billed figures (_sum drops None).",
60	    "why_it_matters": "A second charge for the same service and day that cannot be read is listed on its row but the reconciliation the worker kept reports nothing. The row is visible; the discrepancy is not raised.",
61	    "fix": "If any ledger row for that service and date has an unclear or unparsed figure, raise a visible check (for example SERVICE_NOT_RECONCILED with the row cites) instead of comparing a partial sum. Do this row by row, as in B2.",
62	    "acceptance_test": "Ledger 97110 on 06/10/26 with a bare '130' second row and EOB 130.00 -> a visible check for 97110 is raised; a mutant that drops unclear rows from the comparison turns a test red."},
63	   {"severity": "major", "title": "Rate-row running balance is listed only inside its excerpt; the oracle accepts it",
64	    "evidence": "app/backend/billing.py:271 line['balance'] = None  # the running balance of a price row is in the excluded entry's excerpt. Probe artifacts/review-evidence/T-103-r1/rate_balance.py on row 'Charge per visit 185.00 999.00': lines = [('rate','rate','185.00')]; '999.00' occurs only in the excerpt; tests/unit/test_billing.py unaccounted() == []. Spec: billing.py:13-18 'sit on its row as an unclear figure'.",
65	    "why_it_matters": "The balance is a money token. A paralegal finds it only in the verbatim text, not as a figure. This is the same blind spot as B1, via the whole-row rule for rate entries.",
66	    "fix": "Carry the balance on the rate entry as an unclear figure (class rate, detail rate, unclear ['999.00'] or a balance figure with cents). Then the oracle needs no whole-row exception for it.",
67	    "acceptance_test": "Row 'Charge per visit 185.00 999.00' -> '999.00' appears in a structured figure field of the rate entry, and unaccounted() == [] with the whole-row rule for rate entries removed."},
68	   {"severity": "major", "title": "Fail-safe test cannot fail for tokens dropped inside payer rows or whole-row entries",
69	    "evidence": "tests/unit/test_billing.py:567 _WHOLE_ROW; :583 items += [(x['excerpt'], set(), True) for e in out['payer_reports'] for x in e['lines']]. Mutant M06 (billing.py:511 row['unclear'] = []): 157 passed, 0 failed (artifacts/review-evidence/T-103-r1/mutation_results.txt). Card AC and api.md:693 say the test fails if a token is missing.",
70	    "why_it_matters": "The test's name and the card say it guards every money token, but for EOB rows it guards nothing. A regression in EOB figure handling would pass CI.",
71	    "fix": "Payer rows and whole-row entries claim only the figure texts they actually list. Add the '$140', '$130' and '1O0.00' EOB probes and the rate-balance probe to PROBES.",
72	    "acceptance_test": "Mutant M06 turns at least one test red; the new EOB probes pass the oracle only when their figures are placed in a structured field."},
73	   {"severity": "minor", "title": "Docs and code disagree on 'no balance reconciliation' (BALANCE_STEP_MISMATCH)",
74	    "evidence": "app/backend/billing.py:4-5 docstring 'no balance reconciliation (D-052...)'; billing.py:668-679 _checks_for_line emits BALANCE_STEP_MISMATCH from charge minus paid minus adjustment per line; memory/contracts/api.md:664 'no balance reconciliation' versus api.md:692 'BALANCE_STEP_MISMATCH on the line catches a wrongly read column'.",
75	    "why_it_matters": "A reader of the doc will assume no balance arithmetic happens. The step check is per-line arithmetic, not a total. Whether it is allowed under D-052 is Chris's ruling (questions_for_chris).",
76	    "fix": "Either reword the docstring and api.md to 'no balance sum and no cross-line reconciliation', or drop the check, once Chris rules.",
77	    "acceptance_test": "grep for 'no balance reconciliation' agrees with the code; a test pins the ruling."},
78	   {"severity": "minor", "title": "detail carries two different things (reason for ledger rows, kind for extra lines)",
79	    "evidence": "app/backend/billing.py:810 ledger rows set detail to reversal, balance_only or None; extra lines (billing.py:821 extra()) carry rate, estimate, reduction, lien_amount, asserted_balance, stated_total_<kind>, balance_forward. tests/unit/test_billing.py:567 _WHOLE_ROW keys on these strings.",
80	    "why_it_matters": "A client has to know which kind of detail it is reading. The oracle's leniency also depends on those strings.",
81	    "fix": "Split into a closed 'kind' list for what the line is and a 'reason' for why it is listed; document both in api.md.",
82	    "acceptance_test": "Every line has kind from a closed list; a test pins the list."},
83	   {"severity": "nit", "title": "Printed totals and balance forwards sit in lines with class unclear and a figure field, not billed",
84	    "evidence": "Probe output for table_balance_forward and sample_ledger: EXTRA class=unclear detail=stated_total_billed fig=445.00; EXTRA class=unclear detail=balance_forward fig=100.00.",
85	    "why_it_matters": "This matches the brief (printed totals as lines with detail). A consumer that sums the figure field would double count them.",
86	    "fix": "Say in api.md that figure fields on extra lines are never summed by the client.",
87	    "acceptance_test": "api.md states the rule; no test needed."}
88	 ],
89	 "whats_right": [
90	   "Money is whole cents throughout: no float in billing.py, fmt() is integer // and %, and the tests assert integer cents.",
91	   "The D-019 accepted case total is byte-identical at 2dc5be2 and 841be23 (case_03 $335.00, case_09 $275.00, sample $8,390.00); totals.py, present.py and api.py are untouched.",
92	   "Parser drops are caught: M02, M03, M04 and M07 each turn the random-insertion property test red, and the verifier stub (M08) turns four citation tests red."
93	 ],
94	 "questions_for_chris": [
95	   "Does D-052's 'no balance reconciliation' cover the per-line BALANCE_STEP_MISMATCH check (billing.py:668-679)? I read the check as allowed (no sum, no total, no complete flag), but api.md:664 says otherwise.",
96	   "May a per-service ledger sum be computed internally to decide whether to raise an EOB check, if it is never shown? I read D-052's 'computed or shown' as forbidding it; the row-by-row fix removes the need either way."
97	 ]}
98	```
99	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:23.038Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git rev-parse HEAD && grep -n \"D-052\" -A 30 memory/ORCHESTRATOR_DECISIONS.md | head -80",
 "description": "Show recent git log, HEAD sha, and D-052 decision text"
}
````

### User / tool · 2026-11-02T06:06:23.158Z

**tool result**
````
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
1335f21 fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
2dc5be2 feat(backend): billing ships as a cited line listing, no provider totals or complete flag (T-103, D-052)
841be23 docs: D-052 billing ships as cited line listing without totals (§7.4)
bcdcb919f1723f51579db03d9426443860a91680
60:| D-052 | Billing ships as a **cited line listing without provider totals** (2026-11-02, §7.4 as pre-declared on T-083). Each parsed billing line is shown with its verbatim excerpt and classification (charge, adjustment, payment, rate, unclear), and unreconciled lines are listed; no billed/paid/balance totals and no 'complete' badge are computed or shown. The existing case-level charge total (D-019, stated charges only) is unchanged. | Five review rounds kept finding ways a per-provider total could silently omit or overwrite a figure; a listing cannot hide a missing line. | T-083 staff r5 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:27.740Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -20 && echo \"--- stat 2dc5be2..bcdcb91\" && git diff --stat 2dc5be2 bcdcb91 && echo \"--- r2 file exists?\" && ls -la reviews/T-103* artifacts/review-evidence/ 2>&1 | head -30",
 "description": "Pin HEAD, show diff stat from r1 commit to r2, check existing review files"
}
````

### User / tool · 2026-11-02T06:06:27.943Z

**tool result**
````
bcdcb919f1723f51579db03d9426443860a91680
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
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/export.py
 M app/backend/flags.py
 M app/backend/judges.py
--- stat 2dc5be2..bcdcb91
 app/backend/api.py               |   2 +
 app/backend/billing.py           | 170 +++++++++++++++------------------
 app/backend/case_extras.py       |   3 +-
 app/backend/export.py            |  11 ++-
 app/backend/narrative.py         |   2 +-
 app/backend/pdf_checks.py        |  34 +++++--
 app/backend/pdf_hidden.py        | 196 +++++++++++++++++++++++++++++----------
 app/backend/pdf_text.py          |  12 ++-
 app/backend/review.py            |  63 ++++++++-----
 app/backend/store.py             |   3 +
 app/backend/trace.py             |  20 ++--
 memory/contracts/api.md          |  41 ++++----
 tests/unit/test_billing.py       | 141 ++++++++++++++++++++++------
 tests/unit/test_pdf_hidden_r2.py |  16 ++--
 tests/unit/test_pdf_hidden_r3.py |   4 +-
 tests/unit/test_pdf_hidden_r4.py | 194 ++++++++++++++++++++++++++++++++++++++
 tests/unit/test_trace.py         | 127 ++++++++++++++++++++++++-
 17 files changed, 791 insertions(+), 248 deletions(-)
--- r2 file exists?
-rw-r--r--@ 1 arsis  staff  17057 Nov  2 00:01 reviews/T-103-staff-engineer.md

artifacts/review-evidence/:
total 162408
drwxr-xr-x@ 976 arsis  staff    31232 Nov  2 00:00 .
drwxr-xr-x@   6 arsis  staff      192 Nov  1 18:20 ..
-rw-r--r--@   1 arsis  staff     5624 Nov  1 18:41 M0-r2-staff-resolution.md
-rw-r--r--@   1 arsis  staff     3998 Nov  1 18:17 T-001-exercise-1.txt
-rw-r--r--@   1 arsis  staff     4574 Nov  1 18:17 T-001-exercise-2.txt
-rw-r--r--@   1 arsis  staff     2738 Nov  1 18:23 T-001-exercise-3.txt
-rw-r--r--@   1 arsis  staff     3536 Nov  1 18:37 T-001-r2-readonly-repros.txt
-rw-r--r--@   1 arsis  staff     5099 Nov  1 18:59 T-001-r3-repro.out.txt
-rw-r--r--@   1 arsis  staff     4156 Nov  1 18:59 T-001-r3-repro.sh
-rw-r--r--@   1 arsis  staff    13729 Nov  1 18:22 T-002-curl.txt
-rw-r--r--@   1 arsis  staff   118831 Nov  1 18:42 T-002-r2-activity-390.png
-rw-r--r--@   1 arsis  staff    82140 Nov  1 18:42 T-002-r2-board-390.png
-rw-r--r--@   1 arsis  staff     1300 Nov  1 18:42 T-002-r2-csrf-curl.txt
-rw-r--r--@   1 arsis  staff    73730 Nov  1 18:42 T-002-r2-inbox-390.png
-rw-r--r--@   1 arsis  staff    80417 Nov  1 18:42 T-002-r2-milestones-390.png
-rw-r--r--@   1 arsis  staff    92057 Nov  1 18:42 T-002-r2-personas-390.png
-rw-r--r--@   1 arsis  staff    40406 Nov  1 18:42 T-002-r2-state-390.png
-rw-r--r--@   1 arsis  staff     1126 Nov  1 18:42 T-002-r2-xss.json
-rw-r--r--@   1 arsis  staff      488 Nov  1 19:00 T-002-r3-404.py
-rw-r--r--@   1 arsis  staff   116259 Nov  1 19:00 T-002-r3-activity-390.png
-rw-r--r--@   1 arsis  staff    80919 Nov  1 19:00 T-002-r3-board-390.png
-rw-r--r--@   1 arsis  staff    72782 Nov  1 19:00 T-002-r3-inbox-390.png
-rw-r--r--@   1 arsis  staff    80730 Nov  1 19:00 T-002-r3-milestones-390.png
-rw-r--r--@   1 arsis  staff    89842 Nov  1 19:00 T-002-r3-personas-390.png
-rw-r--r--@   1 arsis  staff     2910 Nov  1 19:00 T-002-r3-probe.out.txt
-rw-r--r--@   1 arsis  staff     3551 Nov  1 19:00 T-002-r3-probe.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:28.068Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md"
}
````

### User / tool · 2026-11-02T06:06:28.076Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:32.881Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%H%n%s' bcdcb91 && echo \"--- archive\" && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf \"$SCR/t103r2\" && mkdir -p \"$SCR/t103r2/head\" && git archive bcdcb91 | tar -x -C \"$SCR/t103r2/head\" && ls \"$SCR/t103r2/head\" && ls -la \"$SCR/t103r2/head/.venv\" 2>&1 | head -2; echo \"--- project venv\"; ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1",
 "description": "Show commit bcdcb91 file list and extract git archive copy into scratchpad"
}
````

### User / tool · 2026-11-02T06:06:33.292Z

**tool result**
````
bcdcb919f1723f51579db03d9426443860a91680
fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)

 app/backend/billing.py     | 170 ++++++++++++++++++++-------------------------
 memory/contracts/api.md    |  31 +++++----
 tests/unit/test_billing.py | 141 +++++++++++++++++++++++++++++--------
 3 files changed, 204 insertions(+), 138 deletions(-)
--- archive
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
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/head/.venv: No such file or directory
--- project venv
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:38.043Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_billing.py 2>&1 | tail -15; echo \"exit=$?\"; echo \"--- archive run\"; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/head && cd \"$SCR\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py 2>&1 | tail -15",
 "description": "Run billing unit tests on project tree and on archive copy"
}
````

### User / tool · 2026-11-02T06:06:40.845Z

**tool result**
````
........................................................................ [ 40%]
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 1.07s
exit=0
--- archive run
........................................................................ [ 40%]
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 1.13s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:42.471Z

**tool call — Bash**
````
{
 "command": "git diff 2dc5be2 bcdcb91 -- app/backend/billing.py | head -400",
 "description": "Show billing.py diff from r1 commit to r2 commit"
}
````

### User / tool · 2026-11-02T06:06:42.570Z

**tool result**
````
diff --git a/app/backend/billing.py b/app/backend/billing.py
index 6c39298..354de77 100644
--- a/app/backend/billing.py
+++ b/app/backend/billing.py
@@ -1,19 +1,19 @@
 """Billing as a cited line listing (T-083, D-042, D-052). CODE ONLY: no model is asked anything here.
 
 What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
-record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED here: no per-provider billed, paid or balance sum, no
-'complete' flag, no balance reconciliation (D-052; five review rounds kept finding ways a total could silently omit a figure, and a listing
-cannot hide a missing line). The one total in the product is the case-level charge total of stated charges (D-019, totals.py), unchanged.
+record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED OR COMPARED here: no sum of any kind, no
+'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
+figure, and a listing cannot hide a missing line). The one total in the product is the case-level charge total of stated charges (D-019, totals.py), unchanged.
 A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as class rate; an estimate, an LOP or lien amount, a printed total
-(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB is a
-payer report (its amounts restate the bill). A figure that cannot be read cleanly (OCR letters, odd decimals, a column that cannot be told
+(UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB service
+row is a line of class unclear, detail `eob`, with its payer figures in `eob` (they restate the bill and are never added to it). A figure that cannot be read cleanly (OCR letters, odd decimals, a column that cannot be told
 apart) is listed with cents None. A row that fits no layout is listed in `unreconciled`; a record the code could not parse is in
-`skipped_records`. The analysis is computed on read, never stored, and never reaches the letter. Money is whole cents (int).
+`skipped_records`. Billing returns only these three lists. The analysis is computed on read, never stored, and never reaches the letter. Money is whole cents (int).
 
 MONEY TOKEN (D-049; the one definition the completeness pass uses). A money token is, in a billing record: (a) a number with a decimal point
 (two decimals, or an odd decimal like 95.5, OCR letters tolerated), with or without '$'; (b) a '$' figure with no cents; or (c) a bare whole
 number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
-CMS-1500 charge box, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
+CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
 else (a stray line outside every money column, a code, a count, a year) is NOT a money token and is not accounted for. Every money token must be a
 listed line, an unreconciled line, or sit on its row as an 'unclear' figure: the final accounting pass lists whatever no parser placed.
 Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
@@ -24,17 +24,14 @@ from app.backend import amounts as A, dates
 
 # ------------------------------------------------------------------ fixed texts (closed list; the contract appendix mirrors it)
 CHECKS = {
-    "BALANCE_STEP_MISMATCH": "This line's running balance does not follow from the line before it, so a column may have been read wrongly.",
-    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed but not totaled.",
-    "LEDGER_EOB_PAID_MISMATCH": "The ledger shows a different payment than the EOB for the same date and service. Neither is picked; paid versus incurred is a legal question.",
-    "LEDGER_EOB_BILLED_MISMATCH": "The ledger's billed amount for this date and service differs from the amount billed on the EOB.",
+    "LINE_UNCLEAR": "A figure on this line could not be read cleanly. It is listed with its text and no value.",
     "NO_DATE_OF_SERVICE": "Charges on this statement carry no date of service; they are counted as stated but cannot be tied to a visit.",
     "ROW_NOT_PARSED": "This row carries a figure or a date but did not fit the form's layout, so it was not read into any column. It is listed here, not totaled; check the original.",
 }
 RULES = [
-    "Every figure is listed with the line it was read from; nothing is totaled here, and a missing figure is never hidden by a sum.",
+    "Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.",
     "A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as a rate, never a charge; a row or sentence that says per visit/session/hour/day, each or x N is a rate even beside the word charge.",
-    "A running balance, a printed total and an EOB's amount billed are listed or shown beside the lines and never added to them.",
+    "A running balance, a printed total and an EOB row's amounts are listed beside the lines and never added to them or checked against them.",
     "LOP, lien and attorney-reduction amounts are listed apart from the charges.",
     "A figure that cannot be read cleanly is listed with no value.",
     "A row that does not fit the layout is listed as unreconciled with its text; it is never dropped.",
@@ -76,8 +73,7 @@ def parse_figure(token: str) -> dict:
 
 
 def _mag(f):
-    """Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept. The running
-    balance step check is what catches a column that was read the wrong way."""
+    """Payment/adjustment figures are reductions: credit notation and plain positives mean the same, so the magnitude is kept."""
     return {**f, "cents": None if f["cents"] is None else abs(f["cents"]), "usd": None if f["cents"] is None else fmt(abs(f["cents"]))}
 
 
@@ -289,7 +285,7 @@ _STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIGX})", re.IGN
 
 
 def _stated(rec, text):
-    """Totals the statement prints itself. Returned with the line they were read from; compared with the parsed lines, never used instead."""
+    """Totals the statement prints itself. Returned with the line they were read from; listed as printed, compared with nothing."""
     out = {}
     for kind, rx in _STATED.items():
         m = rx.search(text)
@@ -483,34 +479,58 @@ def _ub04(rec, lines):
     return out, stated, rates
 
 
-# ------------------------------------------------------------------ EOB (payer figures; never added to charges)
+# ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
 _EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
             ("coinsurance", r"COINS\w*"), ("plan_paid", r"PLAN\s+PAID"), ("patient_owes", r"YOU\s+MAY\s+OWE|PATIENT\s+RESP\w*"))
+_EOBROW = re.compile(rf"^\s*({_DATE})\s+(\S+)\s+")
 
 
-def _eob(rec, lines):
+def _eob_header(lines):
+    """(index, {column name: (start, end)}) of the EOB column header (BILLED and PLAN PAID on one line), or (None, None)."""
     hi = next((i for i, ln in enumerate(lines) if re.search(r"\bBILLED\b", ln) and re.search(r"PLAN\s+PAID", ln, re.IGNORECASE)), None)
-    prov = next((re.sub(r"\s+", " ", m.group(1)).strip() for ln in lines for m in [re.match(r"\s*Provider\s*:\s*(.+?)\s*$", ln, re.IGNORECASE)] if m), None)
     if hi is None:
-        return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": [], "unparsed": [_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]) for ln in lines if _tokens(ln)]}
-    order = sorted(((m.start(), k) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m))
-    names = [k for _, k in order]
-    out, unparsed = [], [_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]) for ln in lines[:hi] if _tokens(ln)]
+        return None, None
+    return hi, {k: (m.start(), m.end()) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m}
+
+
+def _eob_tokens(ln, cols, service=None):
+    """Money-shaped tokens of an EOB line: decimals, '$' figures with no cents and whole numbers under a money column. The service code of a row and
+    the number inside a reason code (PR-1, CO-45) are not money."""
+    out = []
+    for m in _tokens(ln, cols):
+        if service and m.start() < service[1] and service[0] < m.end():
+            continue
+        if re.fullmatch(r"[\d,]+", m.group(0)) and re.search(r"[A-Za-z]-$", ln[:m.start()]):
+            continue
+        out.append(m)
+    return out
+
+
+def _eob(rec, lines):
+    """(row lines, unparsed lines). Each service row (date, service code, figures) is one line of form eob: its figures are in `eob` (by column) when
+    every figure was read and there is one per column; otherwise EVERY money token of the row is in `unclear` with its text, never dropped."""
+    hi, cols = _eob_header(lines)
+    unp = lambda ln, toks: _blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in toks])
+    if hi is None:
+        return [], [unp(ln, _tokens(ln)) for ln in lines if _tokens(ln)]
+    names = [k for _, k in sorted((s0, k) for k, (s0, _e) in cols.items())]
+    out, unparsed = [], [unp(ln, _tokens(ln)) for ln in lines[:hi] if _tokens(ln)]
     for ln in lines[hi + 1:]:
-        m = re.match(rf"^\s*({_DATE})\s+(\S+)\s+", ln)
+        m = _EOBROW.match(ln)
         if not m:
             if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
-                unparsed.append(_blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in _tokens(ln)]))
+                unparsed.append(unp(ln, _tokens(ln)))
             continue
-        figs = [parse_figure(f.group(0)) for f in _NUM.finditer(ln)]
-        row = {"record_no": rec["n"], "dos": m.group(1), "dos_iso": _dos(m.group(1)), "service": m.group(2), "excerpt": ln.strip(), "unclear": [],
-               "codes": (ln[list(_NUM.finditer(ln))[-1].end():].strip() or None) if figs else None}
+        toks = _eob_tokens(ln, cols, m.span(2))
+        figs = [parse_figure(t.group(0)) for t in toks]
+        line = _blank_line(rec, "eob", ln, dos=m.group(1), code=m.group(2))
+        line["eob"], line["eob_codes"] = {}, (ln[toks[-1].end():].strip() or None) if toks else None
         if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
-            row.update({k: _mag(f) for k, f in zip(names, figs)})
+            line["eob"] = {k: _mag(f) for k, f in zip(names, figs)}
         else:
-            row["unclear"] = [f["text"] for f in figs]
-        out.append(row)
-    return {"record_no": rec["n"], "provider": prov or _provider(rec), "lines": out, "unparsed": unparsed}
+            line["unclear"] = [f["text"] for f in figs]
+        out.append(line)
+    return out, unparsed
 
 
 # ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
@@ -592,6 +612,9 @@ def _unit_tokens(form, u, cols, below_header):
         found += [(m.start(), m.end(), m.group(0)) for m in _prose_bare(u)]
     elif form == "ub04":
         found += [(m.start(), m.end(), m.group(0)) for m in (_tokens(u, cols) if below_header else _tokens(u))]
+    elif form == "eob":
+        row = _EOBROW.match(u)
+        found += [(m.start(), m.end(), m.group(0)) for m in (_eob_tokens(u, cols, row.span(2) if row else None) if below_header else _tokens(u))]
     elif form == "cms1500":
         found += [(m.start(), m.end(), m.group(0).strip()) for m in _CMS_MONEY.finditer(u)]
         strict = _CMS.match(u)
@@ -617,12 +640,14 @@ def _account(rec, form, body, ls, got, stated, bfs, rates, lop):
         for k in _FIG_KEYS:
             if isinstance(l.get(k), dict) and "text" in l[k]:
                 add(l["excerpt"], l[k]["text"])
+        for f in (l.get("eob") or {}).values():
+            add(l["excerpt"], f["text"])
         for t in l["unclear"]:
             add(l["excerpt"], t)
     for v in list(stated.values()) + list(bfs):
         add(v["cite"]["excerpt"], v["text"])
     whole = [x["excerpt"].strip() for x in list(rates) + list(lop)]      # an excluded rate / LOP entry carries its whole row (running balance included)
-    hi, cols = _header(ls) if form == "ledger_table" else _ub_header(ls) if form == "ub04" else (None, None)
+    hi, cols = _header(ls) if form == "ledger_table" else _ub_header(ls) if form == "ub04" else _eob_header(ls) if form == "eob" else (None, None)
     units = [(body[s:e], True) for s, e in _segments(body)] if form == "ledger_text" else [(u, hi is not None and i > hi) for i, u in enumerate(ls)]
     lform = "ledger" if form.startswith("ledger") else form
     extra = []
@@ -661,23 +686,11 @@ def _line_around(body, start, end):
     return line.strip()
 
 
-def _cents(fig):
-    return fig["cents"] if fig and fig["cents"] is not None else None
-
-
-def _checks_for_line(line, prev_balance):
-    """LINE_UNCLEAR when a figure could not be read; BALANCE_STEP_MISMATCH when this line's balance is not the previous balance plus its
-    charge minus its payment and adjustment (only checked when every figure on the line was read)."""
-    codes = []
+def _checks_for_line(line):
+    """ROW_NOT_PARSED for a row that fit no layout, LINE_UNCLEAR when a figure could not be read. Nothing is computed from the figures."""
     if line.get("unparsed"):
-        codes.append("ROW_NOT_PARSED")
-    elif line["unclear"]:
-        codes.append("LINE_UNCLEAR")
-    elif _cents(line.get("balance")) is not None and prev_balance is not None:
-        delta = (_cents(line["billed"]) or 0) - (_cents(line["paid"]) or 0) - (_cents(line["adjustment"]) or 0)
-        if line["balance"]["cents"] - prev_balance != delta:
-            codes.append("BALANCE_STEP_MISMATCH")
-    return codes
+        return ["ROW_NOT_PARSED"]
+    return ["LINE_UNCLEAR"] if line["unclear"] else []
 
 
 def _line_key(l):
@@ -714,15 +727,6 @@ def _listed_elsewhere(line, rates, lop):
     return bool(own) and own <= seen
 
 
-def _sum(lines, kind):
-    vals = [l[kind]["cents"] for l in lines if l.get(kind) and l[kind]["cents"] is not None]
-    return sum(vals) if vals else None
-
-
-def _tot(cents):
-    return {"cents": cents, "usd": fmt(cents)}
-
-
 def _billing_looking(rec, body):
     """A record that is a bill by its source label or its own words (invoice, total charges) and carries a decimal figure, but fits no known form."""
     src = rec.get("source") or ""
@@ -732,7 +736,7 @@ def _billing_looking(rec, body):
 def analyze(records: list) -> dict:
     """The whole analysis of a case from its ingested records (needs n, excerpt; uses text, source, duplicate_of). Pure; no I/O."""
     recs = [r for r in records if not r.get("duplicate_of")]
-    lines, stated_by_rec, eobs, lop, excluded, balfwds, rec_form, checks = [], {}, [], [], [], {}, {}, []
+    lines, stated_by_rec, lop, excluded, balfwds, rec_form = [], {}, [], [], {}, {}
     skipped = []
     for r in recs:
         body = r.get("excerpt") or r.get("text") or ""
@@ -756,8 +760,8 @@ def analyze(records: list) -> dict:
             got, st, rates = _ub04(r, ls)
             stated_by_rec[r["n"]] = st
         elif form == "eob":
-            eobs.append(_eob(r, ls))
-            got = eobs[-1].pop("unparsed")
+            rows_, unp_ = _eob(r, ls)
+            got = rows_ + unp_
         elif _billing_looking(r, body):                  # a bill in a layout no parser here knows (an ambulance invoice, say): shown, not silently absent
             skipped.append({"record_no": r["n"], "reason_code": "UNRECOGNISED_BILLING_FORM"})
         if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
@@ -772,7 +776,7 @@ def analyze(records: list) -> dict:
                         rates.append(_rate_entry(r, {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, ex))
         lop_here = _lop_lien(r)
         got = [l for l in got if not (l.get("unparsed") and _listed_elsewhere(l, rates, lop_here))]
-        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
+        if form in ("ledger_table", "ledger_text", "cms1500", "ub04", "eob"):
             got = got + _account(r, form, body, ls, got, stated_by_rec.get(r["n"]) or {}, balfwds.get(r["n"]) or [], rates, lop_here)      # D-049: the last word on what was lost
         lines += got
         excluded += rates
@@ -798,16 +802,10 @@ def analyze(records: list) -> dict:
     for ln in lines:
         ln["provider"] = _provider(by_n[ln["record_no"]])
     lines = _merge_duplicates(lines)
-    prev = {}                                            # running-balance steps follow the order printed within each record
     for l in lines:
-        n = l["record_no"]
-        bfs = balfwds.get(n) or []
-        if n not in prev:
-            prev[n] = bfs[0]["cents"] if len(bfs) == 1 else None
-        l["checks"] = _checks_for_line(l, prev[n])
-        prev[n] = l["balance"]["cents"] if l.get("balance") and l["balance"]["cents"] is not None else prev[n]
+        l["checks"] = _checks_for_line(l)
     for l in lines:
-        l["detail"] = ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
+        l["detail"] = "eob" if l["form"] == "eob" and not l.get("unparsed") else ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
                        "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
         l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
         l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
@@ -846,29 +844,8 @@ def analyze(records: list) -> dict:
         l["id"] = f"b{i}"
     for i, u in enumerate(unreconciled, 1):
         u["id"] = f"u{i}"
-    # EOB cross-checks against the matching provider's ledger lines
-    payer = []
-    for e in eobs:
-        match = next((l["provider"] for l in parsed if l["form"] == "ledger" and (_norm(l["provider"]) in _norm(e["provider"]) or _norm(e["provider"]) in _norm(l["provider"]))), None)
-        ledger_ls = [l for l in parsed if l["form"] == "ledger" and l["provider"] == match]
-        e["matched_provider"] = match
-        e["not_added_note"] = "The EOB restates the provider's charge; its amounts are never added to the charges."
-        e["checks"] = []
-        for el in e["lines"] if match else []:
-            led = [l for l in ledger_ls if _norm(l["code"]) == _norm(el["service"]) and ((l["dos_iso"] and l["dos_iso"] == el["dos_iso"]) or _norm(l["dos"]) == _norm(el["dos"]))]
-            if not led or not el.get("billed"):
-                continue
-            lb, lp = _sum(led, "billed"), _sum(led, "paid") or 0
-            cites = [{"record_no": el["record_no"], "excerpt": el["excerpt"]}] + [c for l in led for c in l["cites"]]
-            if lb is not None and lb != el["billed"]["cents"]:
-                e["checks"].append({"code": "LEDGER_EOB_BILLED_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lb), "eob": el["billed"], "cites": cites})
-            if el.get("plan_paid") and lp != el["plan_paid"]["cents"]:
-                e["checks"].append({"code": "LEDGER_EOB_PAID_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lp), "eob": el["plan_paid"], "cites": cites})
-        for c in e["checks"]:
-            c["message"] = CHECKS[c["code"]]
-        payer.append(e)
-    return {"status": "listed" if (listing or unreconciled or payer or skipped) else "none_found",
-            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "payer_reports": payer, "rules": RULES}
+    return {"status": "listed" if (listing or unreconciled or skipped) else "none_found",
+            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "rules": RULES}
 
 
 _FIG_KEYS = ("billed", "adjustment", "paid", "balance", "discount", "allowed", "deductible", "copay", "coinsurance", "plan_paid", "patient_owes", "non_covered")
@@ -894,8 +871,8 @@ def _walk(o):
 
 def verify_citations(analysis: dict, records: list) -> list:
     """[] when every cited excerpt anywhere in the analysis is a verbatim substring of the record it names, and every figure text sits inside the
-    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines, cites,
-    unreconciled rows and payer-report lines and their check cites. Returns [{ref, reason}]; `for_case` puts the list in the response as
+    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines (EOB row figures
+    included), cites and unreconciled rows. Returns [{ref, reason}]; `for_case` puts the list in the response as
     `citation_failures`."""
     text_of = {r["n"]: (r.get("text") or r.get("excerpt") or "") for r in records}
     bad = []
@@ -907,6 +884,9 @@ def verify_citations(analysis: dict, records: list) -> list:
             for k, v in d.items():
                 if k in _FIG_KEYS and _figure_like(v) and not _in(v["text"], d["excerpt"]):
                     bad.append({"ref": ref, "reason": f"{k}_not_in_excerpt"})
+            for k, v in (d.get("eob") or {}).items():
+                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
+                    bad.append({"ref": ref, "reason": f"eob_{k}_not_in_excerpt"})
             if _figure_like(d.get("figure")) and not _in(d["figure"]["text"], d["excerpt"]):
                 bad.append({"ref": ref, "reason": "figure_not_in_excerpt"})
     seen, out = set(), []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:44.519Z

**tool call — Bash**
````
{
 "command": "git diff 2dc5be2 bcdcb91 -- app/backend/billing.py | sed -n 400,600p; echo \"=== api.md diff\"; git diff 2dc5be2 bcdcb91 -- memory/contracts/api.md",
 "description": "Show remaining billing.py diff and api.md diff for the r2 commit"
}
````

### User / tool · 2026-11-02T06:06:44.645Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:45.878Z

**tool call — Bash**
````
{
 "command": "git diff 2dc5be2 bcdcb91 -- app/backend/billing.py | sed -n 225,420p",
 "description": "Show the tail of the billing.py diff"
}
````

### User / tool · 2026-11-02T06:06:45.984Z

**tool result**
````
         body = r.get("excerpt") or r.get("text") or ""
@@ -756,8 +760,8 @@ def analyze(records: list) -> dict:
             got, st, rates = _ub04(r, ls)
             stated_by_rec[r["n"]] = st
         elif form == "eob":
-            eobs.append(_eob(r, ls))
-            got = eobs[-1].pop("unparsed")
+            rows_, unp_ = _eob(r, ls)
+            got = rows_ + unp_
         elif _billing_looking(r, body):                  # a bill in a layout no parser here knows (an ambulance invoice, say): shown, not silently absent
             skipped.append({"record_no": r["n"], "reason_code": "UNRECOGNISED_BILLING_FORM"})
         if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
@@ -772,7 +776,7 @@ def analyze(records: list) -> dict:
                         rates.append(_rate_entry(r, {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, ex))
         lop_here = _lop_lien(r)
         got = [l for l in got if not (l.get("unparsed") and _listed_elsewhere(l, rates, lop_here))]
-        if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
+        if form in ("ledger_table", "ledger_text", "cms1500", "ub04", "eob"):
             got = got + _account(r, form, body, ls, got, stated_by_rec.get(r["n"]) or {}, balfwds.get(r["n"]) or [], rates, lop_here)      # D-049: the last word on what was lost
         lines += got
         excluded += rates
@@ -798,16 +802,10 @@ def analyze(records: list) -> dict:
     for ln in lines:
         ln["provider"] = _provider(by_n[ln["record_no"]])
     lines = _merge_duplicates(lines)
-    prev = {}                                            # running-balance steps follow the order printed within each record
     for l in lines:
-        n = l["record_no"]
-        bfs = balfwds.get(n) or []
-        if n not in prev:
-            prev[n] = bfs[0]["cents"] if len(bfs) == 1 else None
-        l["checks"] = _checks_for_line(l, prev[n])
-        prev[n] = l["balance"]["cents"] if l.get("balance") and l["balance"]["cents"] is not None else prev[n]
+        l["checks"] = _checks_for_line(l)
     for l in lines:
-        l["detail"] = ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
+        l["detail"] = "eob" if l["form"] == "eob" and not l.get("unparsed") else ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
                        "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
         l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
         l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
@@ -846,29 +844,8 @@ def analyze(records: list) -> dict:
         l["id"] = f"b{i}"
     for i, u in enumerate(unreconciled, 1):
         u["id"] = f"u{i}"
-    # EOB cross-checks against the matching provider's ledger lines
-    payer = []
-    for e in eobs:
-        match = next((l["provider"] for l in parsed if l["form"] == "ledger" and (_norm(l["provider"]) in _norm(e["provider"]) or _norm(e["provider"]) in _norm(l["provider"]))), None)
-        ledger_ls = [l for l in parsed if l["form"] == "ledger" and l["provider"] == match]
-        e["matched_provider"] = match
-        e["not_added_note"] = "The EOB restates the provider's charge; its amounts are never added to the charges."
-        e["checks"] = []
-        for el in e["lines"] if match else []:
-            led = [l for l in ledger_ls if _norm(l["code"]) == _norm(el["service"]) and ((l["dos_iso"] and l["dos_iso"] == el["dos_iso"]) or _norm(l["dos"]) == _norm(el["dos"]))]
-            if not led or not el.get("billed"):
-                continue
-            lb, lp = _sum(led, "billed"), _sum(led, "paid") or 0
-            cites = [{"record_no": el["record_no"], "excerpt": el["excerpt"]}] + [c for l in led for c in l["cites"]]
-            if lb is not None and lb != el["billed"]["cents"]:
-                e["checks"].append({"code": "LEDGER_EOB_BILLED_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lb), "eob": el["billed"], "cites": cites})
-            if el.get("plan_paid") and lp != el["plan_paid"]["cents"]:
-                e["checks"].append({"code": "LEDGER_EOB_PAID_MISMATCH", "dos": el["dos"], "service": el["service"], "ledger": _tot(lp), "eob": el["plan_paid"], "cites": cites})
-        for c in e["checks"]:
-            c["message"] = CHECKS[c["code"]]
-        payer.append(e)
-    return {"status": "listed" if (listing or unreconciled or payer or skipped) else "none_found",
-            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "payer_reports": payer, "rules": RULES}
+    return {"status": "listed" if (listing or unreconciled or skipped) else "none_found",
+            "lines": listing, "unreconciled": unreconciled, "skipped_records": skipped, "rules": RULES}
 
 
 _FIG_KEYS = ("billed", "adjustment", "paid", "balance", "discount", "allowed", "deductible", "copay", "coinsurance", "plan_paid", "patient_owes", "non_covered")
@@ -894,8 +871,8 @@ def _walk(o):
 
 def verify_citations(analysis: dict, records: list) -> list:
     """[] when every cited excerpt anywhere in the analysis is a verbatim substring of the record it names, and every figure text sits inside the
-    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines, cites,
-    unreconciled rows and payer-report lines and their check cites. Returns [{ref, reason}]; `for_case` puts the list in the response as
+    excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines (EOB row figures
+    included), cites and unreconciled rows. Returns [{ref, reason}]; `for_case` puts the list in the response as
     `citation_failures`."""
     text_of = {r["n"]: (r.get("text") or r.get("excerpt") or "") for r in records}
     bad = []
@@ -907,6 +884,9 @@ def verify_citations(analysis: dict, records: list) -> list:
             for k, v in d.items():
                 if k in _FIG_KEYS and _figure_like(v) and not _in(v["text"], d["excerpt"]):
                     bad.append({"ref": ref, "reason": f"{k}_not_in_excerpt"})
+            for k, v in (d.get("eob") or {}).items():
+                if _figure_like(v) and not _in(v["text"], d["excerpt"]):
+                    bad.append({"ref": ref, "reason": f"eob_{k}_not_in_excerpt"})
             if _figure_like(d.get("figure")) and not _in(d["figure"]["text"], d["excerpt"]):
                 bad.append({"ref": ref, "reason": "figure_not_in_excerpt"})
     seen, out = set(), []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:46.205Z

**tool call — Bash**
````
{
 "command": "git diff 2dc5be2 bcdcb91 -- memory/contracts/api.md | sed -n 1,80p",
 "description": "Show api.md billing section diff at r2 commit"
}
````

### User / tool · 2026-11-02T06:06:46.313Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:49.456Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"billing\\|balance\\|total\\|eob\\|complete\" memory/contracts/api.md | sed -n 1,80p",
 "description": "Locate billing, total and EOB references in the API contract"
}
````

### User / tool · 2026-11-02T06:06:49.542Z

**tool result**
````
26:| POST | `/api/cases/{token}/records/{rid}/entry` | D-031 manual entry for a record without a usable entry: body `{summary, excerpt}`; `excerpt` must be whole verbatim sentences of that record (`422 invalid_edit` with `reasons[]` otherwise); same code checks and judge 1 as an edit (D-034/D-047: a number, date, $ figure, side or negation word missing from the quote, a dropped qualifier, or an unlocatable quote is a hard `422 invalid_edit` with `detail.reason` and `detail.tokens`/`detail.qualifiers`, no override; a judge objection saves the entry as `pending`/`needs_review` with a `warnings[]` code, no 409); `201` with `item` (id `e<n>_m`, `review_status: pending`, `entered_by: "reviewer"`, `entered_by_reviewer: true`, `ai_drafted: false`; pending notes carry `[entered by reviewer]`), `totals`, `review`, `warnings`; logged as a `manual_entry` event; notes list it under EDITED ITEMS as entered by reviewer |
27:| POST | `/api/cases/{token}/items/{item_id}/not_duplicate` | D-031 split one record out of a merged entry: body `{record_id}` (a non-first record of that entry, else `422 invalid_edit`); the entry keeps its other records, the record gets its own entry and amounts (`entry_ids` lists both), gaps are recomputed, the decision is stored in the case config and survives a rerun, and the split record's charges come back as their own amounts (`ax<n>_<k>`, never merged with the other record's), so the accepted total counts both; logged as a `not_duplicate` event |
37:| GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
39:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
108:Request: `{"action": "accept" | "reset", "item_ids": ["e1", "e2"]}` (1 to 200 distinct ids). **Entries only.** `accept` needs every id to be an entry with `state: "verified"` and `review_status: "pending"`; `reset` (the undo) needs entries only. Amounts, flags, needs_review and rejected items are never accepted in bulk. All ids are checked before the first write: one bad id gives `422 invalid_batch` with `detail.rejected: [{id, reason}]` (`not_an_entry` | `not_verified` | `not_pending` | `not_found`) and nothing changes. The batch is atomic (if a write fails midway the applied items are put back, each undo logged). One `review_events` row per item, written through the same `apply_review` as single reviews. Response 200: `{"items": [{"id", "review_status"}], "totals", "review", "warnings": []}`. Other malformed bodies: `400 bad_request`. **D-041:** an entry with no confirmed date (see `undated_entries`) is refused for `accept` with reason `date_unconfirmed`; when any rejected id has that reason the response is `422 DATE_UNCONFIRMED` (instead of `invalid_batch`; same `detail.rejected` list, which still names every refused id and its reason), and nothing changes. After `confirm_date` the entry can be accepted singly or in a batch.
124:  "progress": {"done": 4, "total": 9, "label": "Checking summaries 4 of 9"},
175:      "state": "needs_review", "reasons": ["AMOUNT_RATE_NOT_TOTALED"],
176:      "why": "This is a per-visit rate; the records never say how many visits were billed, so it is not totaled.",
182:  "totals": {
185:    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
186:    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}]
246:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phrase-list flag, not a speaker label.) (The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (context only, never raises, D-032), `credibility_language` (code-only family match in `app/backend/credibility.py`; Waddell, out of proportion, symptom magnification, non-physiologic, inconsistent/sub-maximal effort in any word order; negated or negative results such as "Waddell signs negative" raise nothing; neutral title "Credibility-related wording"; D-038), `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`, `llm_split` (one per LLM-split record, reason `LLM_SPLIT`), `analysis_incomplete` (the cross-record conflict check did not finish; carries `pipeline_warning: CONFLICT_PASS_INCOMPLETE`, reason CONFLICT_CHECK_INCOMPLETE; the run status is `done_with_errors` and `warnings[]` gains `CONFLICT_PASS_INCOMPLETE`)). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
271:`convention` is `MDY` or `DMY`. `iso` is the candidate that reading gives, always one of `candidates`, or `null` when the year is also ambiguous (two-digit year above 40). `reason` is plain words: one date reads "Another date in this packet uses month first (Record 1: 03/14/2026)"; several read "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)" (each example names the record the date sits in; the evidence dates come from the packet, never described as "in this record") (at most two examples in `evidence`, the total in `evidence_count`). `auto_applied` is always `false`.
333:  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
341:The paralegal says a dollar figure is, or is not, a billed charge. Taking a figure **out** of the total is always her call; putting one **in** needs evidence. Body: `{ "to": "charge" | "not_a_charge", "note": "optional, 500 chars" }`.
342:- `to: "not_a_charge"` on a `charge`: always allowed. The class becomes `unclear` (response `amount.kind: "unclear"`; shown as "not added to the total", never totaled).
343:- `to: "charge"` on a `rate`, `estimate`, `unclear` or `damages`: allowed only if **(1) code** finds charged-amount wording (charged, charge(s), billed, invoiced, amount due, balance due, total billed) in the *same sentence* as the figure, not negated ("not billed", "unbilled"), the figure has a parsed value and its record is not injection-tagged, **and (2) judge 2** re-checks the figure against class `charge` and answers `agree`. Code runs first; the judge is not called when the code check fails. Undoing her own earlier demotion of a figure the code first called a charge skips both checks (the original class returns with the judge answer it had; works with no judge available).
355:  "totals": { "...": "as in review" }, "review": { "...": "as in review" },
359:Note `item.kind` is the item type (`"amount"`, as in the review response); the amount's class is `amount.kind`, the same field the case endpoint uses. Patch local state from `amount`, `totals` and `review`; no refetch needed.
449:        "counted_in_total": true,
456:        "counted_in_total": true,
476:  "totals": {
485:    "records_total": 9
510:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte.
522:  "summary": { "calls": 30, "cost_usd": 0.19, "latency_ms_total": 71200, "by_backend": {"fixture": 30} } }
545:  "reason_code": null,                  // closed code when status is fail, or when a pass still explains a state (e.g. AMOUNT_RATE_NOT_TOTALED); else null
563:  "progress": { "done": 10, "total": 11, "label": "10 of 11 steps settled" },
581:- **amount:** `found_in_text` (code, `GROUNDING_AMOUNT_NOT_IN_TEXT`), `amount_class` (code; pass for a charge; pass with `reason_code` `AMOUNT_RATE_NOT_TOTALED`/`AMOUNT_ESTIMATE`/`AMOUNT_DAMAGES` for the classes that are never totaled; fail for `AMOUNT_UNCLEAR`), `injection_scan`, `judge_2` (llm; `skipped` for damages, which are not judged), `total_inclusion` (code: pass when it is an accepted charge counted in the total, pending when a charge is undecided, skipped when it is not a charge or was dismissed), `human`.
593:  "progress": { "done": 8, "total": 10, "label": "8 of 10 steps settled" },
605:    { "id": "flags", "kind": "code", "counts": {"total": 4, "by_type": {"gap": 1}, "by_origin": {"code": 2, "llm": 1}} },
606:    { "id": "totals", "kind": "code", "counts": {"accepted_cents": 0, "pending_cents": 839000, "pending_charges": 2, "not_totaled": 1} },
615:Each case step has the shared step keys plus `counts` (object, may be `{}`); `export_gate` also has `ready` and `blockers[]`. Step order is fixed: `ingest, split, dates, extract, grounding, judges, flags, totals, review, export_gate`. Before the AI run (`status: "ingested"`) `extract`, `grounding`, `judges` and `flags` (AI part) are `pending`; the code-made flags and amounts already count.
624:  "totals": { "items_judged": 18, "supported": 15, "unsupported": 2, "unsure": 0, "unavailable": 1, "human_overrides": 1 },
635:`totals.unavailable` counts every verdict `unavailable` AND every live item whose judge never ran (no stored verdict, run finished; it appears in `unresolved` with `state_reason` `JUDGE_UNAVAILABLE`/`FIXTURE_MISS`), so it equals the item traces' skipped judge steps; the case `judges` step is `fail` (`pending` while the run is going) whenever it is above 0 and never says "agreed with all". Export gate invariant: `ready == (blockers == [])` and `status == pass` iff ready (a failed or running run lists `RUN_FAILED`/`RUN_IN_PROGRESS`). Item `next_action` is `null` once the item is accepted, edited or dismissed (step-level hints stay); every `state_reasons[].step_id` is a step id in the trace. An unknown item is 404; an internal error is the standard 500. `totals.unsupported` = partially + unsupported + disagrees (the judge objected); `items_judged` = items whose judge answered (every verdict except `unavailable`). `rejections` = every objection, with the fixed-sentence `rationale`; `unresolved` = `unsure` and `unavailable`. `disagreements[]` (code vs judge): `judge_objects` (every code check passed and the judge objected: `code_says` is the check summary, for an amount the rule's class), `judge_agrees_code_flags` (code raised a doubt (token, qualifier, date) and the judge found it supported; the item stays `needs_review`), `sources_disagree` (flag: the phrase list and the AI disagree, `LEXICON_ONLY`/`LLM_ONLY`). `human_overrides` counts items accepted or edited although a judge objected. Counts cover live and rejected items; narrative sentences are not included. The same visibility split applies (no raw responses in metadata mode; `rejections[].response_raw` is full-mode only).
657:- `{"status": "ok", "calibration": {...}, "message": null}`. `calibration` has exactly: `schema` (`evals.calibration/1`), `backend` (`fixture` or a live backend name), `case_count` (the sample size: golden cases pooled), `small_sample` (bool), `source_commit`, `generated_at`, `by_state` (`verified` and `needs_review`, each `{matched, total, cases[]}`), `by_type` (`entry`, `amount`, `flag`, each with the two states as `{matched, total, by_case: {case: [m, t]}}`), `not_scored` (`entry`, `amount`, `flag`, `total`) and `sentences` (`overall` and `by_type`, each state a string).
659:- `{"status": "invalid", "calibration": null, "message": "..."}`: the file is not a valid measurement (bad JSON or encoding, wrong schema, a count out of range, totals that do not add up, or a statement that does not quote its own `m/t`). The file's contents are never echoed; the reasons go to the server log.
663:## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
664:Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line). Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2):** no provider totals, no billed/paid/balance sums, no `complete` flag, no running-balance step check, no ledger-versus-EOB check. A listing cannot hide a missing line; a sum or a comparison can. The response has exactly `status`, `citation_failures`, `lines`, `unreconciled`, `skipped_records`, `rules`. The only billing total in the product is the case-level charge total of stated charges (D-019, `totals`), unchanged. Unknown token: `404 not_found`.
666:{ "billing": {
667:  "status": "listed",                         // listed | citation_failed | none_found. "listed" says only that something was found; it is not a completeness claim
671:      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | "eob" (an EOB service row) | see the extra-line details below
672:      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04 | eob
674:      "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
682:    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "record_nos": [2], "form": "eob",
683:      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row
684:      "eob": {"billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}},
685:      "eob_codes": "PR-1, PR-2, CO-45", "unclear": [], "checks": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures
689:  "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"}, {"record_no": 5, "reason_code": "UNRECOGNISED_BILLING_FORM"} ],
690:  "rules": [ "Every figure is listed with the line it was read from; nothing is totaled here, ...", "..." ] } }
692:**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28 and Item 29, TOTAL CHARGES, BALANCE DUE; listed as printed, compared with nothing), `balance_forward`. **Figure fields on an extra line, a running `balance`, and everything in `eob` are never summed or compared by a client.** The class is `unclear` because the code does not decide what such a figure means. A figure that is both an LOP amount and a printed balance is one line.
693:**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept). A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a room line is a `rate` and the `0001` line is a printed total. A fee-schedule or per-unit figure is a rate; a table row or a sentence that carries a rate cue (per visit/session/hour/day, each, /visit, x N, daily rate; one shared test, `amounts.has_rate_cue`, also used by reclassify) is a rate even beside the word charge or billed, is listed once, and a `RATE` column's figures are rates too. A ledger-table figure with no cents (`$185`, `185`) under a money column stays on its row as `unclear` text (`LINE_UNCLEAR`); on a rate row it is a `rate` line with `cents: null`. A blank DOS cell stays blank (`dos: null`, `NO_DATE_OF_SERVICE`); the posting date is never read as the service date. A figure with OCR letters, other than two decimals, or inside an injection-tagged record has `cents: null` / the record is in `skipped_records`. A billing-looking record in no known layout is a `skipped_records` entry `UNRECOGNISED_BILLING_FORM`. An EOB service row (date, service code, then one figure per header column: BILLED, DISCOUNT, ALLOWED, DEDUCT, COINS, PLAN PAID, YOU MAY OWE) is a line of form `eob`; it is never compared with the ledger, so a difference in billed or paid is simply two cited lines. A service code and the number in a reason code (`PR-1`, `CO-45`) are not money. Every cited excerpt anywhere in the response (lines, cites, unreconciled) is checked against the record's own text, and every figure text (including each `eob` figure) against its excerpt, by `verify_citations`, which the route runs on every call; failures are returned as `citation_failures` and make the status `citation_failed`.
694:**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of these holds is added to `unreconciled` as a `ROW_NOT_PARSED` row (one already on that row is extended). The test replays every money token of the T-083 probe sets (r1 to r5 reviews, `artifacts/review-evidence/T-083-*`) plus 600 random insertions and fails if one is missing. Repeated summary rows are never overwritten: two balance-forward rows, and a second TOTAL CHARGES / BALANCE DUE / paid / adjustment row (in one record, or in a second statement of the same provider and form family) are all listed (the earlier ones in `unreconciled`, the last as a line; a byte-identical copy of one statement is one line citing both records). An EOB money token is a `$` figure with or without cents, a decimal (OCR letters tolerated), or a whole number under one of the EOB money columns; a row whose figures do not map one-to-one to the columns (a `$140`, `1O0.00`, `130.5`, a bare `130`, a missing or extra figure) keeps every token on its row in `unclear`. A printed total on an EOB (its TOTAL row) is an `unreconciled` row of form `eob`. The test also deletes each EOB figure in turn and requires the oracle to name it.
695:**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, and the response fields `payer_reports`, `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
712:- **Not covered:** amounts in Spanish records are classified by the English billing phrases, so a Spanish charge or rate is usually `unclear` and goes to the paralegal (T-084 reclassify); Latin-American `$1.250,00` figures are read as `$1.250` with no value (`unclear`), never as a wrong number.
736:| `AMOUNT_RATE_NOT_TOTALED` | needs_review | a rate, not a charge |
746:| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplete`, no single record) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:56.557Z

**tool call — Bash**
````
{
 "command": "ls -la artifacts/review-evidence/T-103-r1/ && echo \"=== RUN_ORDER\" && cat artifacts/review-evidence/T-103-r1/RUN_ORDER.txt 2>/dev/null | head -60; echo \"=== CORRECTION\" && cat artifacts/review-evidence/T-103-r1/CORRECTION-1.txt 2>/dev/null | head -30",
 "description": "List r1 evidence directory and read run order notes"
}
````

### User / tool · 2026-11-02T06:06:56.651Z

**tool result**
````
total 232
drwxr-xr-x@  29 arsis  staff    928 Nov  2 00:01 .
drwxr-xr-x@ 976 arsis  staff  31232 Nov  2 00:00 ..
-rw-r--r--@   1 arsis  staff   1111 Nov  2 00:01 CORRECTION-1.txt
-rw-r--r--@   1 arsis  staff   2731 Nov  2 00:00 RUN_ORDER.txt
drwxr-xr-x@   3 arsis  staff     96 Nov  2 00:00 __pycache__
-rw-r--r--@   1 arsis  staff   1276 Nov  1 23:59 accept_totals.py
-rw-r--r--@   1 arsis  staff    461 Nov  1 23:59 case_03_rate_and_ocr.HEAD_accept.json
-rw-r--r--@   1 arsis  staff    461 Nov  1 23:59 case_03_rate_and_ocr.PARENT_accept.json
-rw-r--r--@   1 arsis  staff   1453 Nov  1 23:59 case_03_rate_and_ocr_HEAD_billing.json
-rw-r--r--@   1 arsis  staff    297 Nov  1 23:59 case_09_nonvisit_hides_gap.HEAD_accept.json
-rw-r--r--@   1 arsis  staff   2157 Nov  1 23:59 case_eob_140.txt
-rw-r--r--@   1 arsis  staff   2156 Nov  1 23:59 case_eob_ok.txt
-rw-r--r--@   1 arsis  staff   1297 Nov  1 23:59 eob_mismatch.py
-rw-r--r--@   1 arsis  staff    202 Nov  2 00:00 eob_mismatch_output.txt
-rw-r--r--@   1 arsis  staff    956 Nov  1 23:59 eob_oracle.py
-rw-r--r--@   1 arsis  staff   1127 Nov  1 23:59 eob_probe2.py
-rw-r--r--@   1 arsis  staff    769 Nov  1 23:59 mk_case_text.py
-rw-r--r--@   1 arsis  staff   2104 Nov  2 00:00 mutation_results.txt
-rw-r--r--@   1 arsis  staff    227 Nov  1 23:59 probe_detail2.py
-rw-r--r--@   1 arsis  staff    260 Nov  1 23:59 pytest_billing_HEAD_2dc5be2.txt
-rw-r--r--@   1 arsis  staff   1242 Nov  1 23:59 rate_balance.py
-rw-r--r--@   1 arsis  staff  14960 Nov  1 23:59 route_eob140.json
-rw-r--r--@   1 arsis  staff   1111 Nov  1 23:59 route_file.py
-rw-r--r--@   1 arsis  staff   1184 Nov  1 23:59 run_m04.py
-rw-r--r--@   1 arsis  staff   3189 Nov  1 23:59 run_mutants.py
-rw-r--r--@   1 arsis  staff    365 Nov  1 23:59 sample.HEAD_accept.json
-rw-r--r--@   1 arsis  staff    365 Nov  1 23:59 sample.PARENT_accept.json
-rw-r--r--@   1 arsis  staff    290 Nov  1 23:59 sample_HEAD_totals.json
-rw-r--r--@   1 arsis  staff   1404 Nov  1 23:59 tbv2.py
=== RUN_ORDER
T-103 r1 (commit 2dc5be2) - how to reproduce the evidence in this folder

0. Pin the code. From the project root:
     git rev-parse HEAD                      -> 2dc5be2...
     mkdir <A> && git archive 2dc5be2 | tar -x -C <A>        (archive copy, used as ARCH below)
     mkdir <P> && git archive 841be23 | tar -x -C <P>        (parent, for the D-019 and unrelated-test checks)

1. Unit tests on the project tree (billing files are clean in the working tree):
     .venv/bin/python -m pytest -q tests/unit/test_billing.py      -> pytest_billing_HEAD_2dc5be2.txt (157 passed)

2. Route, golden cases, billing listing (route_file.py; MODE billing | totals):
     .venv/bin/python -I route_file.py <A> <A>/evals/golden/case_03_rate_and_ocr.txt billing  -> case_03_rate_and_ocr_HEAD_billing.json
   (the file holds the route response: status, lines, unreconciled, skipped_records, payer_reports, citation_failures)

3. D-019 case total unchanged (accept_totals.py accepts every charge via POST .../review, then prints present.totals_view):
     .venv/bin/python -I accept_totals.py <A> <A>/evals/golden/case_03_rate_and_ocr.txt   -> case_03_rate_and_ocr.HEAD_accept.json
     same with <P> -> case_03_rate_and_ocr.PARENT_accept.json   (byte-identical; accepted $335.00)
     same for case_09_nonvisit_hides_gap (HEAD only saved; accepted $275.00) and sample (sample.HEAD_accept.json / sample.PARENT_accept.json; accepted $8,390.00)

4. EOB probes (ARCH via env T103_ARCH; each script loads tests/unit/test_billing.py from ARCH):
     T103_ARCH=<A> .venv/bin/python -I eob_mismatch.py   -> eob_mismatch_output.txt
     T103_ARCH=<A> .venv/bin/python -I eob_probe2.py     (same-service unreadable second ledger row, no BILLED check)
     T103_ARCH=<A> .venv/bin/python -I eob_oracle.py     ($130 and 1O0.00 EOB figures; oracle says nothing unaccounted)
     mk_case_text.py writes case_eob_140.txt / case_eob_ok.txt; route_file.py on case_eob_140.txt -> route_eob140.json
       (payer check object carries "ledger": {"cents": 0, ...}; no LEDGER_EOB_BILLED_MISMATCH for 97110)

5. Rate-row balance and estimate detail: T103_ARCH=<A> .venv/bin/python -I rate_balance.py
   Probe listings for the T-083 probe set: probe_detail2.py (T103_ARCH=<A>, args = PROBES names).

6. Mutants (scratch copies; the archive itself is never edited):
     .venv/bin/python -I run_mutants.py <A> <MUTDIR>      (M01-M03, M05-M08)
     .venv/bin/python -I run_m04.py <A> <MUTDIR>          (M04)
     results in mutation_results.txt

7. Unrelated failing test (not T-103): tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts
   fails on <P> (841be23) and on <A> (2dc5be2). T-103 changed billing.py, test_billing.py and api.md only.
=== CORRECTION
CORRECTION-1 to reviews/T-103-staff-engineer.md (the review file is append-only; the findings and verdict are unchanged).

1. Timing. The review says "157 passed in 1.06s ... and in 1.06s on the archive copy". The archive runs printed "157 passed in 1.08s" (run with -I) and "157 passed in 0.92s" (run without -I). The project-tree run printed "157 passed in 1.09s" (first run) and "157 passed in 1.06s" (pytest_billing_HEAD_2dc5be2.txt). Same pass count on both.

2. Citation check scope. The review says verify_citations "returned [] on every probe and golden case I ran". Accurate scope: the route responses for case_03, case_09 and sample show citation_failures []; the probes run through the test module's one() helper assert verify_citations == []; the tbv2 listing helper (probe_detail2.py) does not call verify_citations.

3. LOP detail kinds. The review lists "reduction, asserted_balance or lien_amount" as observed. Observed in probes: reduction and asserted_balance. lien_amount exists in the code (billing.py _lop_lien) but no probe produced it.

No change to any finding, citation or the verdict.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:06:58.450Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r1 && for f in route_file.py eob_mismatch.py eob_probe2.py eob_oracle.py rate_balance.py mk_case_text.py; do echo \"=== $f\"; cat \"$f\"; echo; done; echo \"=== mutation_results\"; cat mutation_results.txt",
 "description": "Read r1 probe scripts and mutation results"
}
````

### User / tool · 2026-11-02T06:06:58.546Z

**tool result**
````
=== route_file.py
import json, os, sys, tempfile, time
ARCH, FILE, MODE = sys.argv[1], sys.argv[2], sys.argv[3]   # MODE: billing | totals
sys.path.insert(0, ARCH)
os.chdir(ARCH)
os.environ["LLM_BACKEND"] = "fixture"; os.environ["ZLAYT_MODE"] = "local"
os.environ.pop("ANTHROPIC_API_KEY", None); os.environ.pop("ENABLE_LIVE", None)
from fastapi.testclient import TestClient
from app.backend.api import create_app
from app.db import db as DB
from app.backend import pipeline as PL, present
d = tempfile.mkdtemp(prefix="t103probe_")
text = open(FILE, encoding="utf-8").read()
c = TestClient(create_app(os.path.join(d, "x.sqlite"), static_dir=d), client=("127.0.0.1", 5000))
conn = DB.connect(c.app.state.db_path)
tok = DB.create_case(conn, text, now=time.time())
PL.ingest_case(conn, tok, text, time.time())
if MODE == "totals":
    print(json.dumps(present.totals_view(conn, tok), sort_keys=True, ensure_ascii=False))
    conn.close()
else:
    conn.close()
    r = c.get(f"/api/cases/{tok}/billing")
    print(json.dumps({"http": r.status_code, "billing": r.json().get("billing")}, indent=1, sort_keys=True, ensure_ascii=False))

=== eob_mismatch.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbv2 as T
tb = T.tb
LED, EOB = tb.LEDGER, tb.EOB
e140 = EOB.replace("06/10/26  97110    130.00", "06/10/26  97110    $140   ")
recs = [tb.rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LED), tb.rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", e140)]
out = tb.B.analyze(recs)
row = next(x for x in out["payer_reports"][0]["lines"] if x["service"] == "97110")
print("EOB row billed:", row.get("billed"), "unclear:", row["unclear"][:2])
print("ledger 97110 billed:", [(l["billed"] or {}).get("cents") for l in out["lines"] if l.get("code") == "97110"])
print("EOB billed-mismatch checks for 97110:", [c["code"] for c in out["payer_reports"][0]["checks"] if c["service"] == "97110" and c["code"] == "LEDGER_EOB_BILLED_MISMATCH"])
print("oracle unaccounted:", [t for t, _ in tb.unaccounted(recs, out)])
e140b = EOB.replace("06/10/26  97110    130.00", "06/10/26  97110    140.00")
recs2 = [tb.rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LED), tb.rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", e140b)]
out2 = tb.B.analyze(recs2)
print("CONTROL with 140.00 printed:", [c["code"] for c in out2["payer_reports"][0]["checks"] if c["service"] == "97110"])

=== eob_probe2.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbv2 as T
tb = T.tb
LED, EOB = tb.LEDGER, tb.EOB
led_dup = LED.replace("06/10/26  06/11/26  97014  E-stim unattended              35.00", "06/10/26  06/11/26  97110  Therapeutic exercise x2          130       ", 1)
recs = [tb.rec(1, "Larkspur Hollow Physical Therapy, itemized statement", led_dup), tb.rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)]
out = tb.one(recs)
for l in out["lines"]:
    if l.get("code") == "97110":
        print("LEDGER 97110 row:", "billed", (l["billed"] or {}).get("cents"), "unclear", l["unclear"], "checks", l["checks"], "dos", l["dos"], "excerpt", l["excerpt"][:60])
for e in out["payer_reports"]:
    print("payer checks:", [(c["code"], c["service"]) for c in e["checks"]])
print("EOB 97110 billed cents:", [(x["service"], (x.get("billed") or {}).get("cents")) for x in out["payer_reports"][0]["lines"] if x["service"]=="97110"])
print("ledger 97110 billed sum from lines:", sum((l["billed"] or {}).get("cents") or 0 for l in out["lines"] if l.get("code")=="97110" and l.get("billed")))

=== eob_oracle.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbv2 as T
tb = T.tb
LED, EOB = tb.LEDGER, tb.EOB
cases = {
 "EOB 97110 billed '$130' (no cents)": EOB.replace("06/10/26  97110    130.00", "06/10/26  97110    $130   "),
 "EOB 97110 billed OCR '1O0.00'": EOB.replace("06/10/26  97110    130.00", "06/10/26  97110    1O0.00 "),
}
for label, e in cases.items():
    recs = [tb.rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LED), tb.rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", e)]
    out = tb.B.analyze(recs)
    row = next(x for x in out["payer_reports"][0]["lines"] if x["service"] == "97110")
    print(label, "| billed:", row.get("billed"), "| unclear:", row["unclear"][:3], "| 97110 checks:", [c["code"] for c in out["payer_reports"][0]["checks"] if c["service"] == "97110"],
          "| oracle unaccounted:", [t for t, _ in tb.unaccounted(recs, out)], "| status:", out["status"])

=== rate_balance.py
import os, sys, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbv2 as T
tb = T.tb
rec_txt = tb.tbl(tb.HEAD_TXT, [tb.row("06/10/26", "06/11/26", "99213", "Charge per visit", "185.00", "999.00")], "")
recs = [tb.rec(1, "Medlark Clinic, itemized statement", rec_txt)]
out = tb.B.analyze(recs)
structured = json.dumps({k: v for k, v in out.items() if k not in ("rules",)}, ensure_ascii=False)
print("lines:", [(l["class"], l["detail"], l.get("figure", {}).get("text") if "figure" in l else (l["balance"] or {}).get("text")) for l in out["lines"]])
print("'999.00' occurs in structured fields other than excerpt:", structured.count("999.00"), "times in JSON; in excerpts only:", [l["excerpt"][:70] for l in out["lines"] if "999.00" in l["excerpt"]])
print("tb.unaccounted:", [t for t, _ in tb.unaccounted(recs, out)])
out2 = tb.B.analyze([tb.rec(1, "Medlark Clinic, itemized statement", "06/10/26  06/11/26  99213  Office visit  185.00  999.00")])
print("control, non-rate row lines:", [(l["class"], (l["balance"] or {}).get("text")) for l in out2["lines"]])
out3 = tb.B.analyze(tb.PROBES["prose_estimate"])
print("estimate probe:", [(l["class"], l["detail"], l.get("figure", {}).get("text")) for l in out3["lines"]])

=== mk_case_text.py
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import tbv2 as T
tb = T.tb
LED, EOB = tb.LEDGER, tb.EOB
def case(ledger, eob, out):
    txt = ("=== Record 1 ===\nDate: 2026-06-15\nSource: Larkspur Hollow Physical Therapy, itemized statement\nExcerpt: \"" + ledger + "\"\n\n"
           "=== Record 2 ===\nDate: 2026-07-22\nSource: Quoinmere Mutual Health Plan, explanation of benefits\nExcerpt: \"" + eob + "\"\n")
    open(out, "w", encoding="utf-8").write(txt)
case(LED, LED.replace("", "") and EOB, os.path.join(os.path.dirname(os.path.abspath(__file__)), "case_eob_ok.txt"))
case(LED, EOB.replace("06/10/26  97110    130.00", "06/10/26  97110    $140   "), os.path.join(os.path.dirname(os.path.abspath(__file__)), "case_eob_140.txt"))

=== mutation_results
T-103 staff-engineer r1 - scratch-copy mutation runs
Pin: HEAD 2dc5be2 (git archive into a scratch dir; billing.py is the only product file mutated, in a copy).
Runner: run_mutants.py (M01-M03, M05-M08) and run_m04.py (M04). Each replacement must match exactly once or it is reported NOT APPLIED.
Suite: tests/unit/test_billing.py (157 tests) unless stated.

Mutant                                              full suite                     selection "property_a_random" / "property_a_random or probe_set"
M01 accounting net off (_account returns [])        5 failed, 152 passed           property: 1 failed (selection with probes: 1 failed, 45 passed)
M02 table unreadable figure dropped + net off       12 failed, 145 passed         property: 1 failed (selection with probes: 2 failed, 44 passed)
M03 CMS unreadable box dropped + net off            7 failed, 150 passed          property: 1 failed (selection with probes: 1 failed, 45 passed)
M04 unreconciled list dropped (unparsed lines gone) 57 failed, 100 passed         property: 1 failed (selection with probes: 14 failed, 32 passed)
M05 printed totals / balance forwards not listed    64 failed, 93 passed          selection with probes: 36 failed, 10 passed
M06 EOB unreadable figure dropped (row unclear=[])  157 passed, 0 failed          selection with probes: 46 passed (NOT CAUGHT)
M07 rate row dropped + net off                      15 failed, 142 passed         property: 1 failed (selection with probes: 2 failed, 44 passed)
M08 verify_citations stubbed to []                  4 failed, 153 passed          selection with probes: 46 passed (caught only by the four verifier tests)

Reading: every drop of a table, CMS, unreconciled or rate token turns the random-insertion property test red, including with the accounting net off.
M06 is not caught. Its oracle (test_billing.py _items, payer rows whole=True) cannot see a figure dropped inside an EOB row.
Real-defect check (no mutant needed): EOB billed "$140" is absent from every structured field and no BILLED check is raised; see eob_mismatch.py output in eob_mismatch_output.txt.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:00.212Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r1 && cat tbv2.py; echo \"=== run_mutants\"; cat run_mutants.py; echo \"=== run_m04\"; cat run_m04.py",
 "description": "Read r1 helper module and mutation runners"
}
````

### User / tool · 2026-11-02T06:07:00.303Z

**tool result**
````
import importlib.util, os, sys
ARCH = os.environ["T103_ARCH"]
sys.path.insert(0, ARCH); os.chdir(ARCH)
spec = importlib.util.spec_from_file_location("tb", os.path.join(ARCH, "tests/unit/test_billing.py"))
tb = importlib.util.module_from_spec(spec); spec.loader.exec_module(tb)
def summary(recs):
    out = tb.B.analyze(recs)
    lines = []
    for l in out["lines"]:
        if "figure" in l:
            lines.append(f"  EXTRA class={l['class']} detail={l['detail']} fig={l['figure']['text']}/{l['figure']['cents']} rec={l['record_no']} ex={l['excerpt'][:60]!r}")
        else:
            lines.append(f"  ROW class={l['class']} detail={l['detail']} b={(l['billed'] or {}).get('cents')} p={(l['paid'] or {}).get('cents')} a={(l['adjustment'] or {}).get('cents')} bal={(l['balance'] or {}).get('cents')} unclear={l['unclear']} checks={l['checks']} ex={l['excerpt'][:60]!r}")
    for u in out["unreconciled"]:
        lines.append(f"  UNREC rec={u['record_no']} figs={u['figures']} ex={u['excerpt'][:60]!r}")
    for s in out["skipped_records"]:
        lines.append(f"  SKIP {s}")
    for e in out["payer_reports"]:
        lines.append(f"  PAYER matched={e['matched_provider']} rows={[(x['service'], x.get('billed'), x.get('plan_paid'), x['unclear'], x['excerpt'][:40]) for x in e['lines']]} checks={[ (c['code'], c.get('ledger'), c.get('eob')) for c in e['checks']]}")
    return out["status"], lines
=== run_mutants
import os, re, shutil, subprocess, sys
ARCH = sys.argv[1]; MUT = sys.argv[2]; PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
NET_OFF = ("        got = got + _account(r, form, body, ls, got, stated_by_rec.get(r[\"n\"]) or {}, balfwds.get(r[\"n\"]) or [], rates, lop_here)",
           "        got = got + []")
MUTANTS = {
 "M01_accounting_net_off": [NET_OFF],
 "M02_table_unreadable_figure_dropped_and_net_off": [NET_OFF,
    ("            elif kind is None or f[\"cents\"] is None:\n                line[\"unclear\"].append(f[\"text\"])",
     "            elif kind is None or f[\"cents\"] is None:\n                pass")],
 "M03_cms_unreadable_box_dropped_and_net_off": [NET_OFF,
    ("            if fig[\"cents\"] is None:\n                line[\"unclear\"].append(fig[\"text\"])",
     "            if fig[\"cents\"] is None:\n                pass")],
 "M04_unreconciled_list_dropped": [
    ("    for l in lines if l[\"unparsed\"]]", "    for l in lines if l[\"unparsed\"] and False]")],
 "M05_printed_totals_not_listed": [
    ("            ex = v[\"cite\"][\"excerpt\"]\n            if (r[\"n\"]", "            continue\n            ex = v[\"cite\"][\"excerpt\"]\n            if (r[\"n\"]")],
 "M06_eob_unreadable_figure_dropped_oracle_blind": [
    ("        row = {\"record_no\": rec[\"n\"], \"dos\": m.group(1)", "        row = {\"record_no\": rec[\"n\"], \"dos\": m.group(1)"),
    ("            row[\"unclear\"] = [f[\"text\"] for f in figs]", "            row[\"unclear\"] = []")],
 "M07_rate_row_dropped_and_net_off": [NET_OFF,
    ("                rates.append(_rate_entry(rec, f, ln.strip(), \"This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled.\"))",
     "                pass")],
 "M08_verifier_stubbed": [
    ("    text_of = {r[\"n\"]: (r.get(\"text\") or r.get(\"excerpt\") or \"\") for r in records}\n    bad = []",
     "    return []\n    text_of = {r[\"n\"]: (r.get(\"text\") or r.get(\"excerpt\") or \"\") for r in records}\n    bad = []")],
}
TESTS = sys.argv[3:] or ["tests/unit/test_billing.py"]
for name, reps in MUTANTS.items():
    dst = os.path.join(MUT, name)
    if os.path.exists(dst): shutil.rmtree(dst)
    shutil.copytree(ARCH, dst, ignore=shutil.ignore_patterns("__pycache__"))
    p = os.path.join(dst, "app/backend/billing.py")
    src = open(p, encoding="utf-8").read()
    ok = True
    for old, new in reps:
        n = src.count(old)
        if n != 1:
            print(f"{name}: NOT APPLIED (matches={n}) for: {old[:70]!r}"); ok = False; break
        src = src.replace(old, new)
    if not ok: continue
    open(p, "w", encoding="utf-8").write(src)
    r = subprocess.run([PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", *TESTS], cwd=dst, capture_output=True, text=True)
    failed = [l.split("::",1)[1].split(" ")[0] for l in r.stdout.splitlines() if l.startswith("FAILED")]
    summary = [l for l in r.stdout.splitlines() if re.search(r"\d+ (passed|failed)", l)]
    print(f"{name}: rc={r.returncode} {summary[-1] if summary else r.stdout[-200:]}")
    for f in failed[:12]: print("    FAILED", f)
    if len(failed) > 12: print(f"    ... {len(failed)} failing in total")
=== run_m04
import os, re, shutil, subprocess, sys
ARCH, MUT = sys.argv[1], sys.argv[2]; PY = "/Users/arsis/zlayt-pm-project/.venv/bin/python"
name = "M04_unreconciled_list_dropped"
reps = [('for l in lines if l["unparsed"]]', 'for l in lines if l["unparsed"] and False]')]
dst = os.path.join(MUT, name)
if os.path.exists(dst): shutil.rmtree(dst)
shutil.copytree(ARCH, dst, ignore=shutil.ignore_patterns("__pycache__"))
p = os.path.join(dst, "app/backend/billing.py")
src = open(p, encoding="utf-8").read()
for old, new in reps:
    assert src.count(old) == 1, src.count(old)
    src = src.replace(old, new)
open(p, "w", encoding="utf-8").write(src)
for sel in ["", "property or probe or bare or oracle"]:
    cmd = [PY, "-m", "pytest", "-q", "-p", "no:cacheprovider", "tests/unit/test_billing.py"] + (["-k", sel] if sel else [])
    r = subprocess.run(cmd, cwd=dst, capture_output=True, text=True)
    summ = [l for l in r.stdout.splitlines() if re.search(r"\d+ (passed|failed)", l)]
    print(f"{name} [{sel or 'all'}]: rc={r.returncode} {summ[-1] if summ else r.stdout[-300:]}")
    print("   ", [l.split('::',1)[1].split(' ')[0] for l in r.stdout.splitlines() if l.startswith('FAILED')][:8])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:02.022Z

**tool call — Bash**
````
{
 "command": "wc -l tests/unit/test_billing.py app/backend/billing.py && grep -n \"^def \\|^_\\|^[A-Z_]* = \\|^PROBES\\|^class \\|@pytest\" tests/unit/test_billing.py",
 "description": "Outline the billing test module structure"
}
````

### User / tool · 2026-11-02T06:07:02.108Z

**tool result**
````
    1103 tests/unit/test_billing.py
     924 app/backend/billing.py
    2027 total
12:LEDGER = """SYNTHETIC RECORD
26:EOB = """SYNTHETIC RECORD - THIS IS NOT A BILL
37:CMS_CLEAN = """SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
47:CMS_OCR = """SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
55:UB_ROOM = """SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
66:PROSE = ("Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00; x-ray charge $180.00; treatment visits 1 through 14 charge $2,310.00; "
69:LOP = ("Letter of protection to Fennimoor Spine Clinic. The client's current balance is $4,860.00. Provider agrees to accept $3,100.00 in full satisfaction "
73:def rec(n, source, text, **kw):
77:_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
81:def one(records):
90:def rows(out, name):
95:def detail(out, d):
99:def rates(out):
103:def figs(out):
107:def checks(out):
111:def cents(l, k="billed"):
116:def test_ledger_lines_parse_to_four_figures_each_cited_and_classed():
128:def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
137:def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
144:def test_fee_schedule_rate_is_a_rate_line_and_never_a_charge():
151:def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them():
159:def test_a_running_balance_that_does_not_follow_is_listed_as_printed_with_no_verdict():
166:def test_unreadable_figure_is_listed_with_no_value():
172:def test_extra_decimals_are_never_rounded():
177:def test_duplicate_statement_is_one_line_citing_both_records():
185:def test_two_identical_lines_inside_one_record_are_both_listed():
192:def test_balance_forward_is_a_cited_line_and_not_a_charge():
201:def test_payments_adjustments_in_their_own_columns_by_position():
214:def test_ledger_prose_statement_lists_charges_payment_adjustment_and_its_printed_figures():
223:def test_nothing_found_for_a_clinical_record():
229:def test_lop_and_lien_amounts_are_unclear_lines_apart_from_the_charges():
236:def test_atty_reduction_on_a_ledger_is_listed_as_an_lop_amount():
244:def test_cms1500_boxes_are_implied_cents_and_item_28_is_a_listed_total():
250:def test_cms1500_ocr_text_never_reads_8500_as_dollars():
260:def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
268:def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
280:def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
288:def test_verify_citations_catches_an_uncited_line():
295:@pytest.fixture
296:def client(tmp_path, monkeypatch):
304:def _seed(client, text):
311:def test_billing_route_returns_the_listing(client):
325:def test_table_survives_ingest_with_the_quote_on_its_own_line_or_the_first_line(client):
337:def test_prose_charges_without_a_date_of_service_are_listed_and_flagged():
342:def test_injection_tagged_record_is_skipped_not_listed():
347:def test_duplicate_records_are_ignored_and_no_model_is_imported():
355:HEAD_TXT = "DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE"
358:def tbl(header, rows_, footer=""):
373:def row(dos, posted, code, desc, charges=None, balance=None, **kw):
383:PT = "Medlark Clinic, itemized statement"
386:@pytest.mark.parametrize("fig", ["185.00", "$185.00"])
387:def test_table_row_charge_per_visit_is_a_rate_line_listed_once(fig):
396:@pytest.mark.parametrize("desc", ["Visit fee per session", "Rate each", "Hourly rate", "Charge /visit", "Daily rate"])
397:def test_every_rate_cue_in_a_table_row_wins_even_beside_charge(desc):
404:def test_unit_notation_x1_is_still_a_normal_charge_in_a_table_row():
409:PROSE_RATES = ["Charge per visit $185.00.", "Billed $150.00 per visit.", "Each session charge $95.00.", "Treatment charge $65.00 x 14.", "Daily rate charge $90.00."]
412:@pytest.mark.parametrize("sent", PROSE_RATES)
413:def test_prose_rate_cue_beats_the_word_charge(sent):
420:def test_prose_rate_is_a_rate_even_when_the_printed_total_includes_it():
428:def test_one_rate_cue_function_is_shared_with_reclassify():
436:def test_rate_column_figures_are_listed_as_rates():
451:def test_cms1500_printed_decimal_is_read_not_dropped():
456:def test_cms1500_slash_dated_line_is_read():
461:def test_cms1500_line_that_does_not_fit_is_unreconciled_with_its_excerpt():
470:def test_ledger_row_with_no_date_is_unreconciled_and_its_total_is_a_line():
481:def test_a_fee_schedule_line_is_a_rate_not_an_unreconciled_row():
486:def test_blank_dos_cell_does_not_take_the_posted_date():
492:AMBULANCE = """SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS
501:def test_a_bill_in_an_unrecognised_layout_is_skipped_visibly_not_none_found():
506:def test_a_clinical_note_with_a_dollar_amount_is_not_flagged_unrecognised():
511:def test_an_unreadable_provider_does_not_touch_another_providers_lines():
519:def test_verifier_reference_is_the_record_text_not_the_excerpt():
527:def test_verifier_covers_every_cite_bearing_field():
546:def test_billing_route_returns_citation_failures_and_flags_the_status(client, monkeypatch):
569:_TOKEN = re.compile(r"\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|(?<![\w/.$])[\dO][\dO,]*\.[\dO]{2}(?!\w|\.\d)|(?<![\w/.])\d+\s*\|\s*\d\d\b")
570:_WHOLE_ROW = ("rate", "estimate", "reduction", "lien_amount", "asserted_balance")      # an excluded rate or LOP entry stands for its whole row
573:def _nt(t):
577:def _items(out):
590:def unaccounted(records, out, bare=()):
611:def cms(*lines, total=None):
617:CMS_SRC = "Brightwater Spine & Wellness, CMS-1500"
618:CMS_OK = "    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001"
621:def _ledger(*rows_, footer="          TOTAL CHARGES 130.00  BALANCE DUE 130.00"):
625:def _prose(*sentences, total="Total charges $250.00. Balance due $250.00."):
629:TOTALS_ROW = "TOTAL" + " " * 52 + "130.00" + " " * 26 + "130.00"          # right-aligned under CHARGES (ends col 63) and BALANCE (ends col 95)
632:def _fwd(*fwd_rows):
638:def _stmt(code, desc, charges, total, dos="06/01/26"):
642:EOB_SRC = "Quoinmere Mutual Health Plan, explanation of benefits"
643:_EOB_HEAD = EOB.split("\n")[:5]
644:_EOB_COLS = "DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES"
645:_EOB_TAIL = "CO-97: payment included in allowance for another service."
648:def eob_text(*service_rows, total="TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00"):
653:def eob_row(billed="130.00", plan_paid="16.00", service="97110", codes="PR-1, CO-45", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00"):
658:PROBES = {
718:BARE_PROBES = {
736:def _texts(out):
741:@pytest.mark.parametrize("name", sorted(PROBES))
742:def test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped(name):
747:@pytest.mark.parametrize("name", sorted(BARE_PROBES))
748:def test_bare_or_dateless_money_token_is_shown(name):
757:def test_oracle_is_not_vacuous():
776:def _eob_line(out, service="97110"):
780:@pytest.mark.parametrize("fig", ["$140", "$130", "1O0.00", "130", "130.5"])
781:def test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text(fig):
790:def test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised():
798:def test_eob_row_reason_codes_and_service_code_are_not_money_tokens():
804:def test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept():
826:@pytest.mark.parametrize("fig", ["$185", "185"])
827:def test_table_charge_with_no_cents_is_on_its_row_as_unclear(fig):
833:@pytest.mark.parametrize("fig", ["185", "$185"])
834:def test_table_rate_row_with_no_cents_is_a_rate_line_with_its_text(fig):
840:def test_table_payment_on_a_rate_row_is_kept_as_a_payment_line():
848:def test_table_totals_row_printed_under_the_columns_is_read_as_printed_totals():
853:def test_table_total_with_no_cents_is_unreconciled():
858:def test_table_figure_above_the_header_is_unreconciled():
863:def test_one_balance_forward_is_a_line_with_its_cite():
870:def test_two_balance_forward_rows_are_both_unreconciled_none_overwritten():
875:def test_balance_forward_in_two_records_of_one_provider_lists_both():
882:def test_prose_previous_balance_is_a_balance_forward_not_the_statement_balance():
887:def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_and_no_verdict_is_given():
897:def test_a_balance_step_that_does_not_follow_raises_nothing_and_an_unreadable_charge_is_class_unclear():
905:def test_prose_unlabelled_figure_is_unreconciled_not_a_charge():
912:def test_prose_figure_with_no_billing_word_is_unreconciled_and_its_total_is_a_line():
918:def test_prose_statement_with_only_a_printed_total_is_listed_not_none_found():
923:def test_prose_rate_only_statement_lists_the_rate_and_both_printed_totals():
928:def test_prose_unreadable_figure_is_listed_with_its_text():
932:def test_prose_decimal_figure_with_no_dollar_sign_is_unreconciled():
937:def test_prose_estimate_is_an_unclear_line_not_a_charge():
943:def test_two_different_printed_totals_are_both_listed_none_picked():
949:def test_cms1500_line_with_no_dates_is_unreconciled_with_only_its_figure():
955:def test_cms1500_line_with_no_units_lists_only_the_money_token_not_the_tail():
960:def test_cms1500_unreadable_total_is_unreconciled():
964:def test_an_unparsed_claim_line_is_unreconciled_beside_the_ledger_rows():
969:def test_ub04_line_with_a_figure_that_fits_no_revenue_row_is_unreconciled():
973:def test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none():
979:def test_dateless_table_row_lists_its_bare_charge_with_the_decimal():
984:def test_second_statement_total_never_overwrites_the_first():
989:def test_first_statement_total_is_visible_when_a_second_statement_follows():
995:def test_identical_copy_of_one_statement_is_one_line_citing_both_records():
1001:def test_second_claim_form_total_is_listed_too():
1005:@pytest.mark.parametrize("name,token", [("M2_second_total_charges", "99.00"), ("M3_second_total_bare", "99"), ("M4_second_balance_due", "55.00"), ("M2b_second_total_equal", "210.00")])
1006:def test_repeated_summary_row_in_one_record_is_listed_the_earlier_one_unreconciled(name, token):
1011:def test_clean_statement_has_nothing_unreconciled():
1015:def test_two_statements_each_with_a_forward_list_both_forwards():
1021:@pytest.mark.parametrize("name,token", [("r5_prose_two_totals", "99.00"), ("r5_prose_previous_balance_twice", "$75.00")])
1022:def test_repeated_prose_summary_is_unreconciled(name, token):
1027:def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
1034:def test_eob_is_lines_not_a_skip():
1042:def test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is():
1053:_BASES = {
1062:_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04",
1064:_TOKENS = ["$123.45", "123.45", "$77", "88", "(45.00)", "1,234.50", "45.00-", "$9,999", "2O0.00", "9.999", "310"]
1067:def _insert(text, tok, rnd, base):
1092:def test_property_a_random_money_token_is_never_silently_missing():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:03.394Z

**tool call — Bash**
````
{
 "command": "sed -n 73,135p tests/unit/test_billing.py",
 "description": "Read test helpers and the no-totals test"
}
````

### User / tool · 2026-11-02T06:07:03.476Z

**tool result**
````
def rec(n, source, text, **kw):
    return {"n": n, "source": source, "excerpt": text, "text": text, **kw}


_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
         "stated_billed", "line_sum_billed", "line_flags", "negotiated_reductions", "balance_forwards"}


def one(records):
    """The analysis, with its citations verified and none of the removed total-shaped fields anywhere in it (D-052)."""
    out = B.analyze(records)
    assert B.verify_citations(out, records) == []
    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "rules"}
    assert not [k for d in B._walk(out) for k in d if k in _GONE]
    return out


def rows(out, name):
    """The parsed ledger / claim-form rows of a provider (a row has billed / paid / adjustment / balance; an extra line has `figure`)."""
    return [l for l in out["lines"] if l["provider"].startswith(name) and "figure" not in l]


def detail(out, d):
    return [l for l in out["lines"] if l["detail"] == d]


def rates(out):
    return [l for l in out["lines"] if l["class"] == "rate"]


def figs(out):
    return [f for u in out["unreconciled"] for f in u["figures"]]


def checks(out):
    return [c for l in out["lines"] for c in l.get("checks", [])]


def cents(l, k="billed"):
    return l[k]["cents"] if l.get(k) else None


# ------------------------------------------------------------------ itemized ledger
def test_ledger_lines_parse_to_four_figures_each_cited_and_classed():
    r = [rec(1, "Larkspur Hollow Physical Therapy (SYNTHETIC), itemized statement", LEDGER)]
    ls = rows(one(r), "Larkspur")
    assert [l["code"] for l in ls] == ["97162", "97110", "97140", "97014", "97140", "97140", "ADJ"]
    first = ls[0]
    assert (first["class"], cents(first), cents(first, "balance"), first["paid"], first["adjustment"]) == ("charge", 21000, 21000, None, None)
    assert first["dos"] == "05/27/26" and first["dos_iso"] == "2026-05-27" and first["posted"] == "05/28/26" and first["record_no"] == 1
    assert first["cites"] == [{"record_no": 1, "excerpt": first["excerpt"]}] and first["excerpt"] in LEDGER
    adj = ls[-1]
    assert adj["adjustment"]["cents"] == 4500 and adj["adjustment"]["text"] == "45.00-" and cents(adj, "balance") == 40000 and adj["class"] == "adjustment"


def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
    """D-052: a listing, not a ledger reconciliation. Whatever the statement prints is a cited line; nothing is summed or compared with a sum."""
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
    assert {l["provider"] for l in out["lines"]} == {"Larkspur Hollow Physical Therapy", "Fennimoor Spine Clinic"}
    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH", "BALANCE_STEP_MISMATCH",
            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
    assert set(B.CHECKS) == {"LINE_UNCLEAR", "NO_DATE_OF_SERVICE", "ROW_NOT_PARSED"}      # nothing in billing sums or compares figures
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:03.746Z

**tool call — Bash**
````
{
 "command": "sed -n 565,611p tests/unit/test_billing.py",
 "description": "Read the oracle and its exemptions in the billing test module"
}
````

### User / tool · 2026-11-02T06:07:03.830Z

**tool result**
````
# printed total, balance forward), an unreconciled row, or on its row as an unclear figure; or the whole record is in skipped_records.
import random
import re

_TOKEN = re.compile(r"\$\s?[\dOolISB][\dOolISB,]*(?:\.[\dOolISB]+)?|(?<![\w/.$])[\dO][\dO,]*\.[\dO]{2}(?!\w|\.\d)|(?<![\w/.])\d+\s*\|\s*\d\d\b")
_WHOLE_ROW = ("rate", "estimate", "reduction", "lien_amount", "asserted_balance")      # an excluded rate or LOP entry stands for its whole row


def _nt(t):
    return re.sub(r"[$()\s-]", "", t or "")


def _items(out):
    """(excerpt, figure texts, whole_row): every place the analysis shows a printed row."""
    items = []
    for l in out["lines"]:
        if "figure" in l:
            items.append((l["excerpt"], {_nt(l["figure"]["text"])}, l["detail"] in _WHOLE_ROW))
        else:
            items.append((l["excerpt"], {_nt(l[k]["text"]) for k in ("billed", "paid", "adjustment", "balance") if l.get(k) and l[k]["cents"] is not None} | {_nt(t) for t in l["unclear"]}
                          | {_nt(f["text"]) for f in (l.get("eob") or {}).values() if f["cents"] is not None}, False))      # an EOB row claims only the figures it lists
    items += [(u["excerpt"], {_nt(f) for f in u["figures"]}, False) for u in out["unreconciled"]]
    return items


def unaccounted(records, out, bare=()):
    """The tokens printed in the input that no row of the output carries. `bare` names whole-number texts that are money in this input; each
    digit-bounded occurrence outside a longer token is counted as a token too. A figure whose cents is None counts only when it sits in `unclear`
    (a parsed slot with no value is not a placement). A record in skipped_records is accounted for as a whole."""
    items, missing, skipped = _items(out), [], {s["record_no"] for s in out["skipped_records"]}
    for r in records:
        if r["n"] in skipped:
            continue
        body = r["excerpt"]
        for s, e in B._segments(body):
            unit = body[s:e].strip()
            toks = list(_TOKEN.finditer(unit))
            for b in bare:
                toks += [m for m in re.finditer(r"(?<![\w/.,$])" + re.escape(b) + r"(?![\w/]|[.,]\d)", unit) if not any(m.start() < t.end() and t.start() < m.end() for t in toks)]
            for t in toks:
                hit = [(texts, whole) for ex, texts, whole in items if unit in ex or (ex in unit and t.group(0) in ex)]
                if not any(whole or _nt(t.group(0)) in texts for texts, whole in hit):
                    missing.append((t.group(0), unit))
    return missing


def cms(*lines, total=None):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:04.213Z

**tool call — Bash**
````
{
 "command": "sed -n 736,826p tests/unit/test_billing.py",
 "description": "Read the probe-set, oracle-sanity and EOB fail-safe tests"
}
````

### User / tool · 2026-11-02T06:07:04.291Z

**tool result**
````
def _texts(out):
    """Every figure text the analysis shows anywhere a paralegal can read it: unreconciled, rates and other extra lines, on-row unclear."""
    return {_nt(f) for f in figs(out)} | {_nt(l["figure"]["text"]) for l in out["lines"] if "figure" in l} | {_nt(x) for l in out["lines"] for x in l.get("unclear", [])}


@pytest.mark.parametrize("name", sorted(PROBES))
def test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped(name):
    recs = PROBES[name]
    assert unaccounted(recs, one(recs)) == [], name


@pytest.mark.parametrize("name", sorted(BARE_PROBES))
def test_bare_or_dateless_money_token_is_shown(name):
    recs, tok, in_unreconciled = BARE_PROBES[name]
    out = one(recs)
    assert _nt(tok) in _texts(out), name
    if in_unreconciled:
        assert _nt(tok) in {_nt(f) for f in figs(out)}, name
    assert unaccounted(recs, out, bare=(tok,) if tok[0] != "$" and "." not in tok else ()) == []


def test_oracle_is_not_vacuous():
    """Erase what the analysis shows and the oracle names every figure; keep it and the oracle is silent."""
    recs = PROBES["prose_unlabelled"]
    out = B.analyze(recs)
    assert unaccounted(recs, out) == []
    out["lines"], out["unreconciled"] = [], []
    assert [t for t, _u in unaccounted(recs, out)] == ["$250.00", "$250.00", "$250.00"]
    recs = BARE_PROBES["P11_bare_prose_figure"][0]
    out = B.analyze(recs)
    out["unreconciled"] = []
    assert [t for t, _u in unaccounted(recs, out, bare=("250",))] == ["250"]
    recs = BARE_PROBES["A_table_bare_charge"][0]
    out = B.analyze(recs)
    bad = next(l for l in out["lines"] if l.get("unclear"))
    bad["billed"], bad["unclear"] = {"text": "185", "cents": None, "usd": None}, []      # a parsed slot with no value is not a placement
    assert [t for t, _u in unaccounted(recs, out, bare=("185",))] == ["185"]


# ---- EOB rows (T-103 r2): every figure of a service row is a structured figure or sits on its row as unclear; nothing is compared with the ledger
def _eob_line(out, service="97110"):
    return next(l for l in out["lines"] if l["form"] == "eob" and l["code"] == service)


@pytest.mark.parametrize("fig", ["$140", "$130", "1O0.00", "130", "130.5"])
def test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text(fig):
    recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]
    out = one(recs)
    line = _eob_line(out)
    assert fig in line["unclear"] and line["eob"] == {} and line["class"] == "unclear" and line["detail"] == "eob" and line["checks"] == ["LINE_UNCLEAR"]
    assert line["excerpt"] in recs[0]["text"] and fig in line["excerpt"]
    assert unaccounted(recs, out, bare=(fig,) if re.fullmatch(r"\d+", fig) else ()) == []


def test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised():
    """r1 B1/B2/M1: '$140' against a ledger 130.00. No check, no ledger sum, no payer report: both rows are lines with their own excerpt."""
    out = one(PROBES["eob_ledger_conflict"])
    assert "$140" in _eob_line(out)["unclear"] and checks(out) == ["LINE_UNCLEAR"]
    assert next(l for l in out["lines"] if l["code"] == "97110" and l["form"] == "ledger")["billed"]["cents"] == 13000
    assert not [k for d in B._walk(out) for k in d if k in ("ledger", "payer_reports", "matched_provider")]


def test_eob_row_reason_codes_and_service_code_are_not_money_tokens():
    out = one([rec(1, EOB_SRC, EOB)])
    assert [l["excerpt"] for l in out["unreconciled"]][0].startswith("TOTAL") and len(out["unreconciled"]) == 1
    assert all(l["unclear"] == [] for l in out["lines"] if l["form"] == "eob")


def test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept():
    """The accounting test must be able to fail for EOB rows (r1 M3, mutant M06). Distinct figures, so each drop is visible to the set-based oracle."""
    row_ = eob_row(billed="130.00", plan_paid="16.00", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00")
    recs = [rec(1, EOB_SRC, eob_text(row_))]
    assert unaccounted(recs, B.analyze(recs)) == []
    for k in ("billed", "discount", "allowed", "deductible", "coinsurance", "plan_paid", "patient_owes"):
        out = B.analyze(recs)
        del _eob_line(out)["eob"][k]
        assert len(unaccounted(recs, out)) == 1, k
    for fig in ("$140", "1O0.00"):
        recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]
        out = B.analyze(recs)
        assert unaccounted(recs, out) == []
        _eob_line(out)["unclear"] = []                                  # mutant M06: the unclear list dropped
        assert fig in {t for t, _u in unaccounted(recs, out)}, fig
    recs = [rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              $235   115.00"))]
    out = B.analyze(recs)
    out["unreconciled"] = []
    assert {t for t, _u in unaccounted(recs, out)} == {"$235", "115.00"}


# ---- a figure with no cents is kept as text; a row that does not fit is listed; a printed total is a line
@pytest.mark.parametrize("fig", ["$185", "185"])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:31.108Z

**tool call — Bash**
````
{
 "command": "sed -n 653,735p tests/unit/test_billing.py | cut -c1-260",
 "description": "Read the probe dictionaries used by the accounting oracle"
}
````

### User / tool · 2026-11-02T06:07:31.190Z

**tool result**
````
def eob_row(billed="130.00", plan_paid="16.00", service="97110", codes="PR-1, CO-45", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00"):
    return f"06/10/26  {service:<7} {billed:>7}   {discount:>7}   {allowed:>7}  {deduct:>7} {coins:>6}   {plan_paid:>8}   {owes:>9}     {codes}"


# the T-083 probe sets (r1 to r5 reviews, artifacts/review-evidence/T-083-*): each is run through the oracle
PROBES = {
    "sample_ledger": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)],
    "prose": [rec(1, "Fennimoor Spine Clinic, itemized ledger", PROSE)],
    "cms_clean": [rec(1, CMS_SRC, CMS_CLEAN)],
    "cms_no_28": [rec(1, CMS_SRC, CMS_NO_28)],
    "cms_printed_dollar": [rec(1, CMS_SRC, CMS_NO_28.replace("85.00         1", "$85.00        1") + "\n28. TOTAL CHARGE  260 | 00")],
    "cms_no_dates": [rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "cms_no_units": [rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     85.00      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"))],
    "cms_unreadable_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  1O0 | 00     29. AMOUNT PAID  0 | 00"))],
    "ub04": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM)],
    "ub04_stray_figure": [rec(1, "Saltmarrow General Hospital, UB-04", UB_ROOM.replace("67 S42.201A", "   SURCHARGE NOTE        125.00\n67 S42.201A"))],
    "lop": [rec(1, "Letter of protection to Fennimoor Spine Clinic", LOP)],
    "table_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "$185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_bare_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00"), footer="          TOTAL CHARGES 315.00  BALANCE DUE 315.00"))],
    "table_rate_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "185", "315.00")))],
    "table_rate_dollar_no_cents": [rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Charge per visit", "$185", "315.00")))],
    "table_no_date": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35.00", "165.00"), footer="          TOTAL CHARGES 165.00  BALANCE DUE 165.00"))],
    "table_totals_under_columns": [rec(1, PT, _ledger(footer=TOTALS_ROW))],
    "table_total_no_cents": [rec(1, PT, _ledger(footer="          TOTAL CHARGES 130  BALANCE DUE 130.00"))],
    "table_figure_above_header": [rec(1, PT, "Previous statement balance $400.00\n" + _ledger())],
    "prose_unlabelled": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")],
    "prose_balance_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Balance due $250.00.")],
    "prose_rate_only": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Charge per visit $185.00. Total charges $185.00. Balance due $185.00.")],
    "prose_ocr": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Physical therapy $2O0.00. Total charges $200.00. Balance due $200.00.")],
    "prose_no_dollar_sign": [rec(1, PT, _prose("Payment received 300.00."))],
    "prose_estimate": [rec(1, PT, _prose("Estimated cost of care $500.00."))],
    "prose_rates": [rec(1, PT, _prose(*PROSE_RATES))],
    "table_balance_forward": [rec(1, PT, _fwd("Balance forward  100.00"))],
    "table_two_balance_forwards": [rec(1, PT, _fwd("Balance forward  100.00", "Balance forward   50.00"))],
    "two_totals_disagree": [rec(1, PT, _prose(total="Total charges $250.00. Balance due $250.00. Total charges $310.00."))],
    "ledger_plus_claim": [rec(1, PT, _ledger()), rec(2, "Medlark Clinic, CMS-1500", cms("    060126   060126   11     98941              AB     85.00         1      SYN-NPI-0001"))],
    "r3_prose_previous_balance": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00. Balance due $750.00.")],
    "r3_prose_previous_balance_no_due": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Total charges $250.00.")],
    "r3_dateless_row_dollar_no_cents": [rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "$35", "165.00")))],
    "r3_cms_words_box": [rec(1, CMS_SRC, cms(CMS_OK, "    060426   060426   11     97010          A   ten dollars   1      SYN-NPI-0001"))],
    "r5_two_statements": [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00")), rec(2, PT, _stmt("97110", "Therapeutic exercise", "130.00", "130.00", "06/10/26"))],
    "r5_second_claim_total": [rec(1, CMS_SRC, cms(CMS_OK, total="28. TOTAL CHARGE  85 | 00")),
                              rec(2, CMS_SRC, cms("    060226   060226   11     98941              AB     90 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  90 | 00"))],
    "r5_prose_two_totals": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Total charges $250.00. Total charges 99.00.")],
    "r5_prose_previous_balance_twice": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Previous balance $75.00. Total charges $250.00.")],
    "r5_ledger_with_eob": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)],
    "eob_sample": [rec(1, EOB_SRC, EOB)],
    "eob_dollar_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(billed="$140")))],                    # T-103 r1 B1: '$140' was lost from every field
    "eob_dollar_no_cents_paid": [rec(1, EOB_SRC, eob_text(eob_row(plan_paid="$16")))],
    "eob_ocr_letters": [rec(1, EOB_SRC, eob_text(eob_row(billed="1O0.00")))],
    "eob_bare_under_column": [rec(1, EOB_SRC, eob_text(eob_row(billed="130", plan_paid="16")))],
    "eob_odd_decimals": [rec(1, EOB_SRC, eob_text(eob_row(billed="130.5", allowed="78.123")))],
    "eob_missing_column": [rec(1, EOB_SRC, eob_text(eob_row().replace("   26.00", "")))],
    "eob_extra_figure": [rec(1, EOB_SRC, eob_text(eob_row() + "  104.00"))],
    "eob_figure_above_header": [rec(1, EOB_SRC, eob_text(eob_row()).replace("Provider:", "Billed to date $75.00\nProvider:"))],
    "eob_total_row_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              $235   115.00"))],
    "eob_ledger_conflict": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, EOB_SRC, eob_text(eob_row(billed="$140")))],
    "r5_skipped_ambulance": [rec(1, "Brightwater Ambulance invoice", "Brightwater Ambulance (SYNTHETIC) invoice\nALS transport 1234.00 mileage 1234.00 supplies 1234.00")],
    "r5_skipped_injection": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)],
}
for _name, _extra in {"M2_second_total_charges": "\n          TOTAL CHARGES 99.00", "M3_second_total_bare": "\n          TOTAL CHARGES 99",
                      "M4_second_balance_due": "\n          BALANCE DUE 55.00", "M2b_second_total_equal": "\n          TOTAL CHARGES 210.00"}.items():
    PROBES[_name] = [rec(1, PT, _stmt("97162", "PT eval", "210.00", "210.00") + _extra)]

# whole numbers that are money in these inputs (D-049), with where each must end up
BARE_PROBES = {
    "P11_bare_prose_figure": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250. Total charges $500.00.")], "250", True),
    "P12_dollar_no_cents_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit $250. Total charges $500.00.")], "$250", True),
    "P10_unlabelled_decimal_prose": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Office visit 250.00. Total charges $500.00.")], "250.00", True),
    "P13_bare_labelled_charge": ([rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge 250. Total charges $250.00.")], "250", True),
    "P16_dateless_cms_bare": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     85       1      SYN-NPI-0001"))], "85", True),
    "P16b_dateless_cms_dollar": ([rec(1, CMS_SRC, cms(CMS_OK, "    11     98941              AB     $85.00      1      SYN-NPI-0001"))], "$85.00", True),
    "P7_dateless_table_row_bare": ([rec(1, PT, _ledger(row("", "", "97014", "E-stim unattended", "35", "165.00")))], "35", True),
    "P4_balance_forward_bare": ([rec(1, PT, _fwd("Balance forward  100"))], "100", True),
    "P18_balance_forward_dollar_no_cents": ([rec(1, PT, _fwd("Balance forward  $100"))], "$100", True),
    "P15_dated_cms_bare_box": ([rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     45       1      SYN-NPI-0001"))], "45", False),
    "eob_bare_charge": ([rec(1, EOB_SRC, eob_text(eob_row(billed="130")))], "130", False),
    "eob_bare_paid": ([rec(1, EOB_SRC, eob_text(eob_row(plan_paid="16")))], "16", False),
    "eob_bare_total_row": ([rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              235   115.00"))], "235", True),
    "A_table_bare_charge": ([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00")))], "185", False),
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:31.597Z

**tool call — Bash**
````
{
 "command": "sed -n 1034,1103p tests/unit/test_billing.py | cut -c1-260",
 "description": "Read EOB parser tests and the random-insertion property test"
}
````

### User / tool · 2026-11-02T06:07:31.687Z

**tool result**
````
def test_eob_is_lines_not_a_skip():
    out = one(PROBES["r5_ledger_with_eob"])
    assert out["skipped_records"] == [] and len([l for l in out["lines"] if l["form"] == "eob"]) == 3
    (u,) = out["unreconciled"]
    assert u["form"] == "eob" and u["excerpt"].startswith("TOTAL") and u["figures"][0] == "235.00"      # the EOB's printed total row is listed, not dropped


# ---- the money-token definition (D-049): a bare whole number is a token only in an amount column
def test_bare_whole_number_on_a_stray_line_is_not_a_money_token_but_one_under_a_column_is():
    """Pins the definition in the module docstring. Fuzz class r4 finding 3: a stray '208' outside every column is not a token; the same number
    right-aligned under CHARGES is, and then it is listed."""
    base = _ledger()
    assert B._tokens("          208", B._header(base.split("\n"))[1]) == []
    assert "208" not in _texts(one([rec(1, PT, base + "\n          208")]))
    assert "208" in _texts(one([rec(1, PT, base + "\n" + " " * 61 + "208")]))
    assert "MONEY TOKEN" in B.__doc__ and "amount column" in B.__doc__


# ---- property: a random money token put anywhere in a billing record is a line, unreconciled, or its record is skipped
_BASES = {
    "table": lambda: _ledger(),
    "table_sample": lambda: LEDGER,
    "prose": lambda: PROSE,
    "cms": lambda: cms(CMS_OK, "    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"),
    "ub04": lambda: UB_ROOM,
    "eob": lambda: EOB,
    "eob_rows": lambda: eob_text(eob_row(), eob_row(service="97140", billed="70.00", plan_paid="16.00")),
}
_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04",
        "eob": EOB_SRC, "eob_rows": EOB_SRC}
_TOKENS = ["$123.45", "123.45", "$77", "88", "(45.00)", "1,234.50", "45.00-", "$9,999", "2O0.00", "9.999", "310"]


def _insert(text, tok, rnd, base):
    """Put the token somewhere in the ledger. A whole number (no '$', no cents) is money only in an amount position (D-049): in a sentence for
    prose, right-aligned under a money column on a line of its own for a table or a UB-04. It is not put in a CMS-1500 (that form's boxes are tested by name)."""
    lines = text.split("\n")
    if re.fullmatch(r"\d+", tok):
        if base == "prose":
            return text.replace(". Balance due", f". Office visit {tok}. Balance due", 1) if rnd.random() < 0.5 else text + f" Visit fee {tok}."
        hdr, cols = B._header(lines) if base.startswith("table") else B._eob_header(lines) if base.startswith("eob") else B._ub_header(lines)
        if hdr is None:
            return text
        kind = rnd.choice(sorted(k for k in cols if k != "rate"))
        lines.insert(rnd.randrange(hdr + 1, len(lines) + 1), " " * max(0, cols[kind][1] - len(tok)) + tok)
        return "\n".join(lines)
    mode = rnd.choice(["append_line", "own_line", "mid_line"])
    i = rnd.randrange(len(lines))
    if mode == "own_line":
        lines.insert(i, "          " + tok)
    elif mode == "append_line":
        lines[i] = lines[i] + "   " + tok
    else:
        cut = rnd.choice([m.end() for m in re.finditer(r"\s+", lines[i])] or [len(lines[i])])
        lines[i] = lines[i][:cut] + tok + " " + lines[i][cut:]
    return "\n".join(lines)


def test_property_a_random_money_token_is_never_silently_missing():
    rnd, n = random.Random(20261102), 0
    for _ in range(600):
        base, tok = rnd.choice(sorted(_BASES)), rnd.choice(_TOKENS)
        text = _insert(_BASES[base](), tok, rnd, base)
        recs = [rec(1, _SRC[base], text)]
        out = B.analyze(recs)
        assert B.verify_citations(out, recs) == [], (base, tok, text)
        missing = unaccounted(recs, out, bare=(tok,) if re.fullmatch(r"\d+", tok) else ())
        assert missing == [], (base, tok, missing, text)
        n += text != _BASES[base]()
    assert n > 400, n            # the token really was inserted in most draws
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:34.554Z

**tool call — Bash**
````
{
 "command": "F=app/backend/billing.py; echo \"--- sum/total/tot/complete/ledger/payer/balance/check/compare words\"; grep -n -i \"sum\\|_tot\\|total\\|complete\\|ledger\\|payer\\|_sum\\|eob\\|check\" $F | grep -v '^\\s*#' | cut -c1-220; echo \"--- comparison ops on figures\"; grep -n \"cents\\\"\\] *[<>=!]=\\|cents\\\"\\] *[<>]\\| < 0\\| > 0\\| == \\| != \\| <= \\| >= \\|abs(\\| + \\| - \" $F | cut -c1-220",
 "description": "Grep billing.py for sums, totals, EOB and comparison operators"
}
````

### User / tool · 2026-11-02T06:07:34.628Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =!]=\|cents"\] *[<>]\| < 0\| > 0\| == \| != \| <= \| >= \|abs(\| + \| - )
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:07:39.617Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $SCR/t103r2/probes && cat > $SCR/t103r2/probes/grep_head.py <<'EOF'\nimport re, sys\npath = sys.argv[1]\npats = [r\"sum\", r\"_tot\\b\", r\"total\", r\"complete\", r\"ledger\", r\"payer\", r\"eob\", r\"check\", r\"abs\\(\", r\"cents\\\"\\]\\s*(<|>|==|!=|<=|>=)\", r\"\\s(<|>|==|!=|<=|>=)\\s\", r\"\\+\\s\", r\"\\s-\\s\"]\nfor i, ln in enumerate(open(path, encoding=\"utf-8\"), 1):\n    if any(re.search(p, ln, re.IGNORECASE) for p in pats[:9]) or re.search(pats[10], ln) or re.search(pats[11], ln) or re.search(pats[12], ln):\n        print(f\"{i}: {ln.rstrip()[:200]}\")\nEOF\ncd /Users/arsis/zlayt-pm-project && python3 $SCR/t103r2/probes/grep_head.py app/backend/billing.py",
 "description": "Scan billing.py for sums, totals, EOB terms and comparisons"
}
````

### User / tool · 2026-11-02T06:07:39.733Z

**tool result**
````
3: What it does: every ledger line parses to billed / adjustment / paid / balance figures, each cited to its line (a verbatim excerpt of the
4: record) and classed charge, adjustment, payment, rate or unclear. NOTHING IS TOTALED OR COMPARED here: no sum of any kind, no
5: 'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
6: figure, and a listing cannot hide a missing line). The one total in the product is the case-level charge total of stated charges (D-019, totals.py), unchanged.
7: A rate (per visit, per unit, fee schedule, UB-04 line 44) is listed as class rate; an estimate, an LOP or lien amount, a printed total
8: (UB-04 line 0001, CMS-1500 Item 28, TOTAL CHARGES, BALANCE DUE) and a balance forward are listed as class unclear with a `detail`; an EOB service
9: row is a line of class unclear, detail `eob`, with its payer figures in `eob` (they restate the bill and are never added to it). A figure that cannot be read cleanly (OCR letters, odd decimals, a colu
13: MONEY TOKEN (D-049; the one definition the completeness pass uses). A money token is, in a billing record: (a) a number with a decimal point
15: number (no '$', no decimal) ONLY when it sits in an amount column (under a ledger CHARGES/PAYMENTS/ADJ/BALANCE header, a UB-04 money column, a
16: CMS-1500 charge box, an EOB money column, a balance-forward row, or as the figure of a labelled charge/total/balance sentence in prose). A bare whole number anywhere
19: Repeated summary rows (a second TOTAL CHARGES, BALANCE DUE or balance forward, in one record or in several) are listed in full, never overwritten.
26: CHECKS = {
29:     "ROW_NOT_PARSED": "This row carries a figure or a date but did not fit the form's layout, so it was not read into any column. It is listed here, not totaled; check the original.",
32:     "Every figure is listed with the line it was read from; nothing is totaled or compared here, and a missing figure is never hidden by a sum.",
34:     "A running balance, a printed total and an EOB row's amounts are listed beside the lines and never added to them or checked against them.",
38:     "This view is for review only. The letter's total line is still accepted charges only.",
55:          "rate": re.compile(r"\bRATE\b", re.IGNORECASE)}                    # a RATE column is a price list: its figures are listed as rates, never totaled
63:     return ("-" if cents < 0 else "") + f"${abs(cents) // 100:,}.{abs(cents) % 100:02d}"
77:     return {**f, "cents": None if f["cents"] is None else abs(f["cents"]), "usd": None if f["cents"] is None else fmt(abs(f["cents"]))}
87:     name = re.sub(r"\s+(?:itemized\s+)?(?:ledger|statement|billing|bill|claim|eob)\s*$", "", name, flags=re.IGNORECASE).strip()
93:     return p["iso"] if p.get("status") == "parsed" else None
102:     """ledger_table | ledger_text | cms1500 | ub04 | eob | None, decided from the record's own words."""
106:     if "EXPLANATION OF BENEFITS" in up or "THIS IS NOT A BILL" in up or re.search(r"\bEOB\b", src, re.IGNORECASE) or ("PLAN PAID" in up and "BILLED" in up):
107:         return "eob"
108:     if "UB-04" in up or "UB04" in up or "CMS-1450" in up or "47 TOTAL CHARGES" in up or re.search(r"\bUB-?04\b", src, re.IGNORECASE):
110:     if "TOTAL CHARGE" in up and "AMOUNT PAID" in up or "1500" in src or "HEALTH INSURANCE CLAIM FORM" in up:
113:         return "ledger_table"
114:     if "$" in body and (A._is_billing_source(src) or re.search(r"\bitemized\s+(?:ledger|statement)\b|\bledger\b", body, re.IGNORECASE)):
115:         return "ledger_text"
120:     """(index, {kind: (start, end)}) of the ledger column header, or (None, None). Needs billed and balance and one more column."""
122:         if _ROW.match(ln) or re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or "$" in ln or not re.search(r"\S\s{2,}\S", ln):
129:         if "billed" in cols and "balance" in cols and len([k for k in cols if k != "rate"]) >= 3:
137:     d = sorted((min(abs(s - hs), abs(e - he)), kind) for kind, (hs, he) in cols.items())
138:     if d[0][0] > TOL or (len(d) > 1 and d[1][0] == d[0][0]):
143: # ------------------------------------------------------------------ itemized ledger table
158:     """Money-shaped tokens of a ledger line, in text order: decimals, '$' figures without cents and, only when `cols` is given, whole numbers that
164:         found += [m for m in _BARE.finditer(plain) if (all_bare or _column(m.span(), cols) is not None) and not any(m.start() < f.end() and f.start() < m.end() for f in found)]
169:     """Record the totals a statement prints. A second figure for the same total (equal or different) is never guessed between or silently
170:     absorbed: the earlier one is listed as an unparsed line (the paralegal sees it, the provider is incomplete), the later one is kept (D-049)."""
174:             out.append(_blank_line(rec, "ledger", old["cite"]["excerpt"], unparsed=True, unclear=[old["text"]]))
179:     """A printed total that could not be read (cents None), or that belongs to a statement with no readable line at all, is listed as an unparsed
180:     line with the total's own excerpt: the provider is incomplete, and the figure is not left only in a field nobody opens."""
189:     """Ledger tables and ledger prose are one family (a statement); each claim form is its own."""
190:     return "ledger" if (form or "ledger").startswith("ledger") else form
194:     return min(abs(span[0] - hdr[0]), abs(span[1] - hdr[1]))
197: def _ledger_table(rec, lines):
198:     """(lines, stated totals, balance-forward rows [list], rate entries). A row whose description carries a rate cue and whose CHARGES figure was found (read
199:     or not) is a price, not a charge: it goes to the rate entries and into no total. Every other line that carries a figure and is not a clean
200:     dated row (above the header, below it, a total it cannot place) is emitted as an unparsed line (unclear, not totaled), never dropped."""
206:         out.append(_blank_line(rec, "ledger", ln, unparsed=True, unclear=[parse_figure(t.group(0))["text"] for t in toks]))
211:     for ln in lines[hi + 1:]:
212:         if re.match(r"\s*TOTAL\b", ln, re.IGNORECASE) or re.search(r"\bBALANCE\s+DUE\b", ln, re.IGNORECASE):
221:                     stated[kind] = {**(_mag(f) if kind in ("paid", "adjustment") else f), "cite": _cite(rec, ln)}      # a totals row printed under the columns
231:                 if bf["cents"] is None or len(toks) > 1:
239:             if figs:                                  # a figure on a line that is not a dated row: listed, not totaled (the caller may drop it if it is a rate or LOP line)
243:         row_m = _ROW.match(head + " ")
245:         code = parts[0] if parts and re.fullmatch(r"[A-Za-z0-9]{2,7}", parts[0]) and (len(parts) > 1 or not figs) else None
246:         desc = (parts[1] if code and len(parts) > 1 else " ".join(parts)).strip() if parts else ""
248:         if posted is None and len(dcols) == 2 and _near((m.start(1), m.end(1)), dcols["posted"]) < _near((m.start(1), m.end(1)), dcols["dos"]):
250:         line = _blank_line(rec, "ledger", ln, dos=dos, posted=posted, code=code, description=desc)
255:             if kind == "billed" and ratey:           # a price, whether or not its cents could be read: listed once, never a line
256:                 rates.append(_rate_entry(rec, f, ln.strip(), "This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled."))
260:             elif kind == "rate":
271:     _put_stated(rec, stated, {k: v for k, v in _stated(rec, "\n".join(lines[hi + 1:])).items() if k not in stated}, out)
281: _STATED = {"billed": re.compile(rf"TOTAL\s+CHARGES?\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
282:            "paid": re.compile(rf"TOTAL\s+(?:PMTS?|PAYMENTS?)\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
283:            "adjustment": re.compile(rf"TOTAL\s+ADJ\w*\s*[:=]?\s*({_FIGX})", re.IGNORECASE),
284:            "balance": re.compile(rf"(?:BALANCE\s+DUE|AMOUNT\s+DUE|TOTAL\s+BALANCE)\s*[:=]?\s*({_FIGX})", re.IGNORECASE)}
288:     """Totals the statement prints itself. Returned with the line they were read from; listed as printed, compared with nothing."""
300: # ------------------------------------------------------------------ ledger written as a sentence ("New patient exam charge $250.00; ...")
301: _PROSE = (("billed_total", re.compile(r"\btotal\s+(?:billed\s+)?charges?\b|\btotal\s+billed\b", re.IGNORECASE)),
311:         out.append((pos, m.start() + (1 if text[m.start()] == "." else 0)))
317: def _ledger_text(rec, body):
318:     """(lines, stated totals, rate entries, balance-forward figures). A figure the classifier calls a rate, or a charge-worded figure whose sentence also carries a rate cue
320:     figure is either a charge (a line), a paid/adjustment/balance/total by its label, or an unparsed line with its text: an unlabelled figure is
321:     never totaled and never dropped."""
332:             neg = seg[max(0, a["start"] - 1):a["start"]] == "-" or label.endswith("-")
333:             raw = ("-" if neg else "") + a["raw"]
338:             if cls == "rate" or (kind is None and cls == "charge" and A.has_rate_cue(seg)):
340:             elif kind == "billed_total":
344:             elif kind == "balance" and _BALFWD.search(label):
346:             elif kind == "balance":
348:             elif cls == "charge":
350:             elif cls == "estimate":
351:                 rates.append(_rate_entry(rec, fig, seg.strip(), "An estimate is not a charge. It is not totaled.", kind="estimate"))
353:                 bad.append(raw)                              # no label the code recognises: listed, not totaled, never guessed to be a charge
355:             if not any(m.start() < e2 and s2 < m.end() for s2, e2 in spans):
358:             lines.append(_blank_line(rec, "ledger", seg, description=seg.strip(), unparsed=True, unclear=bad))
363:     line = _blank_line(rec, "ledger", seg, description=seg.strip())
372: _CMS_TOTAL = re.compile(rf"\bTOTAL\s+CHARGE\s+({_AMT}|{_FIG})")
387:         cents = int(d) * 100 + int(c)
388:     elif re.fullmatch(r"\d+ \d\d", raw):
390:         cents = int(d) * 100 + int(c)
404:             line = {"record_no": rec["n"], "form": "cms1500", "dos": m.group(1) if m.group(1) == m.group(2) else f"{m.group(1)}-{m.group(2)}", "dos_iso": None,
414:             for kind, rx in (("billed", _CMS_TOTAL), ("paid", _CMS_PAID)):
428: # ------------------------------------------------------------------ UB-04 (FL 44 rate is never a charge; FL 47 is; 0001 is the total)
433:     hi = next((i for i, ln in enumerate(lines) if re.search(r"TOTAL\s+CHARGES", ln, re.IGNORECASE) and re.search(r"\bREV\b|SERV", ln)), None)
437:     for kind, rx in (("rate", r"HCPCS/RATE|RATE"), ("billed", r"TOTAL\s+CHARGES"), ("noncovered", r"NON-COVERED")):
449:     for ln in lines[hi + 1:]:
457:         if m.group(1) == "0001":
459:                 if k == "billed":
470:             elif k == "rate":
472:             elif k == "noncovered":
482: # ------------------------------------------------------------------ EOB (payer figures; listed as lines, never added to charges or compared)
483: _EOBCOLS = (("billed", r"BILLED"), ("discount", r"DISCOUNT|NOT\s+COVERED"), ("allowed", r"ALLOWED"), ("deductible", r"DEDUCT\w*"), ("copay", r"COPAY"),
485: _EOBROW = re.compile(rf"^\s*({_DATE})\s+(\S+)\s+")
488: def _eob_header(lines):
489:     """(index, {column name: (start, end)}) of the EOB column header (BILLED and PLAN PAID on one line), or (None, None)."""
493:     return hi, {k: (m.start(), m.end()) for k, rx in _EOBCOLS for m in [re.search(rx, lines[hi], re.IGNORECASE)] if m}
496: def _eob_tokens(ln, cols, service=None):
497:     """Money-shaped tokens of an EOB line: decimals, '$' figures with no cents and whole numbers under a money column. The service code of a row and
501:         if service and m.start() < service[1] and service[0] < m.end():
509: def _eob(rec, lines):
510:     """(row lines, unparsed lines). Each service row (date, service code, figures) is one line of form eob: its figures are in `eob` (by column) when
512:     hi, cols = _eob_header(lines)
513:     unp = lambda ln, toks: _blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in toks])
518:     for ln in lines[hi + 1:]:
519:         m = _EOBROW.match(ln)
521:             if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
524:         toks = _eob_tokens(ln, cols, m.span(2))
526:         line = _blank_line(rec, "eob", ln, dos=m.group(1), code=m.group(2))
527:         line["eob"], line["eob_codes"] = {}, (ln[toks[-1].end():].strip() or None) if toks else None
528:         if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
529:             line["eob"] = {k: _mag(f) for k, f in zip(names, figs)}
536: # ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
556:                         "figure": {"text": a["raw"], "cents": a["cents"], "usd": fmt(a["cents"])}, "excerpt": seg.strip(), "in_totals": False})
561: # Every money-shaped token the record prints must end up in one of four places: a parsed figure (a line, a stated total, a balance forward), an
563: # its OWN tokenizer, after every parser has run, and lists whatever no parser placed; the provider of such a line is complete: false.
591:     nums = [m for m in re.finditer(r"(?<![\w/.-])\d+(?![\w/-])", _blank_dates(u)) if m.start() > c.end()]
592:     return nums[:-1] if len(nums) > 1 else nums
598:     for a in sorted(found, key=lambda t: (t[0], -(t[1] - t[0]))):
599:         if not out or a[0] >= out[-1][1]:
606:     if form == "ledger_table":
611:     elif form == "ledger_text":
613:     elif form == "ub04":
615:     elif form == "eob":
616:         row = _EOBROW.match(u)
617:         found += [(m.start(), m.end(), m.group(0)) for m in (_eob_tokens(u, cols, row.span(2) if row else None) if below_header else _tokens(u))]
618:     elif form == "cms1500":
623:         for rx in (_CMS_TOTAL, _CMS_PAID):
627:         if not strict and not _CMS_TOTAL.search(u) and not _CMS_PAID.search(u):
643:         for f in (l.get("eob") or {}).values():
647:     for v in list(stated.values()) + list(bfs):
649:     whole = [x["excerpt"].strip() for x in list(rates) + list(lop)]      # an excluded rate / LOP entry carries its whole row (running balance included)
650:     hi, cols = _header(ls) if form == "ledger_table" else _ub_header(ls) if form == "ub04" else _eob_header(ls) if form == "eob" else (None, None)
651:     units = [(body[s:e], True) for s, e in _segments(body)] if form == "ledger_text" else [(u, hi is not None and i > hi) for i, u in enumerate(ls)]
652:     lform = "ledger" if form.startswith("ledger") else form
658:         mine = next((l for l in got if l.get("unparsed") and l["excerpt"].strip() == us), None)
662:             hit = next((it for it in items if not it[2] and it[1] == key and (it[0] in us or us in it[0])), None)
667:             elif not (mine and form == "cms1500" and not _CMS_MONEY.search(text)):      # a bare number on a row already listed whole stays on that row's excerpt
673:                 extra.append(_blank_line(rec, lform, us, description=us if form == "ledger_text" else "", unparsed=True, unclear=missing))
680:     a, b = body.rfind("\n", 0, start) + 1, body.find("\n", end)
681:     line = body[a:(b if b >= 0 else len(body))]
682:     if len(line) > 240:
684:             if s <= start < e:
689: def _checks_for_line(line):
707:         if hit and key[4:7] != (None, None, None):
725:     seen = {_nt(x["figure"]["text"]) for x in rates if x["excerpt"].strip() == ex}
727:     return bool(own) and own <= seen
731:     """A record that is a bill by its source label or its own words (invoice, total charges) and carries a decimal figure, but fits no known form."""
733:     return bool(_NUM.search(body) and (A._is_billing_source(src) or re.search(r"\binvoice\b|\bTOTAL\s+CHARGES?\b", body, re.IGNORECASE)))
750:         if form == "ledger_table":
751:             got, st, bf, rates = _ledger_table(r, ls)
753:         elif form == "ledger_text":
754:             got, st, rates, bf = _ledger_text(r, body)
756:         elif form == "cms1500":
759:         elif form == "ub04":
762:         elif form == "eob":
763:             rows_, unp_ = _eob(r, ls)
764:             got = rows_ + unp_
767:         if form in ("ledger_table", "ledger_text", "cms1500", "ub04"):
768:             got = got + _stated_orphans(r, "ledger" if form.startswith("ledger") else form, got, stated_by_rec.get(r["n"]) or {})
769:         if form == "ledger_table":                       # a statement's fee-schedule line is a rate and carries no date of service
772:                 if a["cents"] is not None and A.classify(body, a, source=r.get("source")) == "rate":
779:         if form in ("ledger_table", "ledger_text", "cms1500", "ub04", "eob"):
780:             got = got + _account(r, form, body, ls, got, stated_by_rec.get(r["n"]) or {}, balfwds.get(r["n"]) or [], rates, lop_here)      # D-049: the last word on what was lost
789:         if len(found_fwd) > 1:                           # several balance-forward rows for one provider: every one is listed, none is picked (D-049)
791:                 lines.append(_blank_line(r, "ledger", bf["cite"]["excerpt"], unparsed=True, unclear=[bf["text"]]))
793:     for r in recs:                                       # a second statement's TOTAL CHARGES / BALANCE DUE (a summary row of one kind, same form family) is listed, never overwritten
798:         if len(found_st) > 1:
806:         l["checks"] = _checks_for_line(l)
808:         l["detail"] = "eob" if l["form"] == "eob" and not l.get("unparsed") else ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "
813:         if l["form"] == "ledger" and l["billed"] and not l["dos"]:
814:             l["checks"].append("NO_DATE_OF_SERVICE")
817:                      "message": CHECKS["ROW_NOT_PARSED"], "excerpt": l["excerpt"], "figures": l["unclear"]} for l in lines if l["unparsed"]]
820:         """A cited line that is not a ledger row: a rate, an estimate, an LOP/lien amount, a printed total or a balance forward."""
824:     extras = [extra(x["record_no"], "rate" if x["kind"] == "rate" else "unclear", x["kind"], x["figure"], x["excerpt"], x["why"]) for x in excluded]
828:     for r in recs:                                       # a printed total or a balance forward is a line too (a copy of one statement is one line citing both records)
829:         for kind, v in list((stated_by_rec.get(r["n"]) or {}).items()) + [("balance_forward", bf) for bf in balfwds.get(r["n"]) or []]:
831:             if (r["n"], ex.strip(), v["text"]) in shown or any(e["record_no"] == r["n"] and _nt(e["figure"]["text"]) == _nt(v["text"]) and (e["excerpt"] in ex or ex in e["excerpt"]) for e in listed_ap
839:             by_key[key] = extra(r["n"], "unclear", kind if kind == "balance_forward" else f"stated_total_{kind}", {k: v[k] for k in ("text", "cents", "usd")}, ex,
842:     listing = sorted(parsed + extras, key=lambda l: l["record_no"])
874:     excerpt it is cited to. The reference is the record's own text (the ingested block), never the excerpt being checked. Covers lines (EOB row figures
879:     for d in _walk({k: v for k, v in analysis.items() if k != "rules"}):
887:             for k, v in (d.get("eob") or {}).items():
889:                     bad.append({"ref": ref, "reason": f"eob_{k}_not_in_excerpt"})
901: def checked(analysis: dict, records: list) -> dict:
902:     """The analysis plus its citation check. A failure is shown (`citation_failures`, status `citation_failed`), never swallowed; nothing is dropped silently."""
913:     return checked(analyze(records), records)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:05.435Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2; ls $SCR/head/evals/golden/ | head -30; echo; cd /Users/arsis/zlayt-pm-project && git diff --quiet 2dc5be2 bcdcb91 -- app/backend/billing.py; echo \"billing diff vs r1 exit=$?\"; git diff 2dc5be2 bcdcb91 -- tests/unit/test_billing.py | grep \"^[-+]\" | grep -i \"whole\\|_WHOLE\\|eob\" | head -20 | cut -c1-200",
 "description": "List golden case files in the archive and check test diff"
}
````

### User / tool · 2026-11-02T06:08:05.584Z

**tool result**
````
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
case_09_nonvisit_hides_gap.expected.json
case_09_nonvisit_hides_gap.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
sample.expected.json
sample.export.expected.txt
sample.txt
unsplit_paste.split.json
unsplit_paste.txt

billing diff vs r1 exit=1
+            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
-def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():
+def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
-    assert {l["record_no"] for l in out["lines"]} == {1}                     # the EOB's 235.00 billed is not a line of the ledger
-    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
-    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
+    eob = [l for l in out["lines"] if l["form"] == "eob"]
+    assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
+    l140 = next(l for l in eob if l["code"] == "97140")
+    assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
+    assert l140["billed"] is None and l140["paid"] is None and l140["checks"] == [] and l140["excerpt"] in EOB     # an EOB row is never a charge or a payment
+    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised
+    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})
+    assert broken(lambda o: pick(o, "eob").update(excerpt="made up")) != []
+    assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
+                          | {_nt(f["text"]) for f in (l.get("eob") or {}).values() if f["cents"] is not None}, False))      # an EOB row claims only the figures it lists
-    items += [(x["excerpt"], set(), True) for e in out["payer_reports"] for x in e["lines"]]      # a payer-report row stands for its whole row
+EOB_SRC = "Quoinmere Mutual Health Plan, explanation of benefits"
+_EOB_HEAD = EOB.split("\n")[:5]
+_EOB_COLS = "DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:08.213Z

**tool call — Bash**
````
{
 "command": "grep -n \"def broken\\|def pick\\|broken(\" tests/unit/test_billing.py | cut -c1-220; echo ---; sed -n 268,290p tests/unit/test_billing.py | cut -c1-240; echo ---; sed -n 519,560p tests/unit/test_billing.py | cut -c1-240",
 "description": "Read broken-output helper and EOB and verifier tests"
}
````

### User / tool · 2026-11-02T06:08:08.331Z

**tool result**
````
531:    def broken(fn):
536:    assert broken(lambda o: pick(o, "eob").update(excerpt="made up")) != []
537:    assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
538:    assert broken(lambda o: pick(o, "stated_total_billed").update(excerpt="made up")) != []
539:    assert broken(lambda o: pick(o, "stated_total_billed")["figure"].update(text="999.99")) != []          # a printed total must sit inside its own cite
540:    assert broken(lambda o: pick(o, "rate").update(excerpt="made up")) != []
541:    assert broken(lambda o: o["unreconciled"][0].update(excerpt="made up")) != []
542:    assert broken(lambda o: o["lines"][0]["billed"].update(text="999.99")) != []
543:    assert broken(lambda o: None) == []
---
def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
    out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
    eob = [l for l in out["lines"] if l["form"] == "eob"]
    assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
    l140 = next(l for l in eob if l["code"] == "97140")
    assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
    assert l140["billed"] is None and l140["paid"] is None and l140["checks"] == [] and l140["excerpt"] in EOB     # an EOB row is never a charge or a payment
    assert [cents(l) for l in rows(out, "Larkspur") if l["form"] == "ledger"][:2] == [21000, 13000]
    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised
    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})


def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
    r = [rec(1, "Brightwater Spine & Wellness, itemized ledger", "Itemized ledger, statement date 07/01/2026. Care charge $390.00. Total charges $390.00. Balance due $390.00."),
         rec(2, "Brightwater Spine & Wellness, CMS-1500", CMS_CLEAN)]
    ls = rows(one(r), "Brightwater")
    assert [(l["form"], cents(l)) for l in ls] == [("ledger", 39000)] + [("cms1500", c) for c in (8500, 8500, 8500, 9000, 4500)]


# ------------------------------------------------------------------ citations, API
def test_verify_citations_catches_an_uncited_line():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    out = B.analyze(r)
---
def test_verifier_reference_is_the_record_text_not_the_excerpt():
    r = [{"n": 1, "source": "Larkspur Hollow Physical Therapy, itemized statement", "excerpt": LEDGER, "text": "A"}]
    out = B.analyze(r)
    assert out["lines"] and B.verify_citations(out, r) != []                       # the excerpt is not in the record's own text
    ok = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)]
    assert B.verify_citations(B.analyze(ok), ok) == []


def test_verifier_covers_every_cite_bearing_field():
    r = [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB),
         rec(3, "Medlark Clinic, itemized statement", "Itemized ledger, statement date 06/15/2026. Office visit $250.00. Total charges $250.00. Balance due $250.00.")]

    def broken(fn):
        out = B.analyze(r)
        fn(out)
        return B.verify_citations(out, r)
    pick = lambda o, d: next(l for l in o["lines"] if l["detail"] == d)
    assert broken(lambda o: pick(o, "eob").update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
    assert broken(lambda o: pick(o, "stated_total_billed").update(excerpt="made up")) != []
    assert broken(lambda o: pick(o, "stated_total_billed")["figure"].update(text="999.99")) != []          # a printed total must sit inside its own cite
    assert broken(lambda o: pick(o, "rate").update(excerpt="made up")) != []
    assert broken(lambda o: o["unreconciled"][0].update(excerpt="made up")) != []
    assert broken(lambda o: o["lines"][0]["billed"].update(text="999.99")) != []
    assert broken(lambda o: None) == []


def test_billing_route_returns_citation_failures_and_flags_the_status(client, monkeypatch):
    text = "=== Record 1 ===\nDate: 2026-06-15\nSource: Fennimoor Spine Clinic, itemized ledger\nExcerpt: \"" + PROSE + "\"\n"
    conn, tok = _seed(client, text)
    conn.close()
    clean = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert clean["citation_failures"] == [] and clean["status"] == "listed"
    real = B.analyze

    def tampered(records):
        out = real(records)
        out["lines"][0]["cites"][0]["excerpt"] = "not in the record"
        return out
    monkeypatch.setattr(B, "analyze", tampered)
    bad = client.get(f"/api/cases/{tok}/billing").json()["billing"]
    assert bad["status"] == "citation_failed" and bad["citation_failures"][0]["reason"] == "excerpt_not_verbatim"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:18.449Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/probes/tbr2.py",
 "content": "\"\"\"Loader for the T-103 r2 probes. Loads tests/unit/test_billing.py from the archive named by T103_ARCH (never from the project tree).\"\"\"\nimport importlib.util, os, sys\nARCH = os.environ[\"T103_ARCH\"]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\nspec = importlib.util.spec_from_file_location(\"tb\", os.path.join(ARCH, \"tests/unit/test_billing.py\"))\ntb = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(tb)\n"
}
````

### User / tool · 2026-11-02T06:08:18.502Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/probes/tbr2.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:29.946Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/probes/r1_reprobe.py",
 "content": "\"\"\"Re-run of the T-103 r1 probes against the r2 archive. Prints the analysis facts for each r1 finding; no assertions.\"\"\"\nimport json, os, re, sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport tbr2 as T\ntb = T.tb\nB = tb.B\nLED, EOB = tb.LEDGER, tb.EOB\nPAYER_KEYS = {\"payer_reports\", \"matched_provider\", \"not_added_note\", \"checks\", \"providers\", \"totals\", \"complete\", \"stated_totals\", \"balance_convention\"}\n\n\ndef keys_anywhere(o):\n    return sorted({k for d in B._walk(o) for k in d})\n\n\ndef unaccounted_texts(recs, out):\n    return [t for t, _u in tb.unaccounted(recs, out)]\n\n\ndef show_eob(out, service):\n    for l in out[\"lines\"]:\n        if l.get(\"form\") == \"eob\" and l.get(\"code\") == service:\n            return {\"dos\": l.get(\"dos\"), \"class\": l[\"class\"], \"detail\": l[\"detail\"], \"billed\": l.get(\"billed\"), \"paid\": l.get(\"paid\"),\n                    \"eob\": {k: v[\"text\"] + \"/\" + str(v[\"cents\"]) for k, v in (l.get(\"eob\") or {}).items()}, \"unclear\": l[\"unclear\"],\n                    \"checks\": l[\"checks\"], \"excerpt\": l[\"excerpt\"]}\n    return None\n\n\nprint(\"== R1-B1 / R1-B2 / R1-M1: EOB $140 against ledger 130.00 (r1 eob_mismatch.py)\")\ne140 = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    $140   \")\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e140)]\nout = tb.one(recs)\nprint(\"status:\", out[\"status\"], \"| top keys:\", sorted(out))\nprint(\"EOB 97110 row:\", json.dumps(show_eob(out, \"97110\"), ensure_ascii=False))\nprint(\"any check anywhere (lines[].checks):\", [c for l in out[\"lines\"] for c in l[\"checks\"]])\nprint(\"unaccounted:\", unaccounted_texts(recs, out))\nprint(\"'ledger' or 'payer_reports' keys anywhere:\", [k for k in keys_anywhere(out) if k in (\"ledger\", \"payer_reports\", \"eob_cents\")])\n\nprint(\"\\n== control: EOB 140.00 against ledger 130.00\")\ne140b = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    140.00\")\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e140b)]\nout = tb.one(recs)\nprint(\"EOB 97110 row:\", json.dumps(show_eob(out, \"97110\"), ensure_ascii=False))\nprint(\"any check anywhere:\", [c for l in out[\"lines\"] for c in l[\"checks\"]])\n\nprint(\"\\n== R1-B1 probes: EOB figures without clean cents (r1 eob_oracle.py)\")\nfor label, fig in [(\"$130\", \"$130   \"), (\"1O0.00\", \"1O0.00 \"), (\"130 bare\", \"130    \"), (\"130.5\", \"130.5  \")]:\n    e = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    \" + fig)\n    recs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e)]\n    out = tb.one(recs)\n    r = show_eob(out, \"97110\")\n    print(label, \"| class:\", r[\"class\"], \"| unclear:\", r[\"unclear\"], \"| eob:\", r[\"eob\"], \"| checks:\", r[\"checks\"], \"| unaccounted:\", unaccounted_texts(recs, out))\n\nprint(\"\\n== R1-M1: same-service second ledger row unreadable (bare 130), EOB 130.00 (r1 eob_probe2.py)\")\nled_dup = LED.replace(\"06/10/26  06/11/26  97014  E-stim unattended              35.00\", \"06/10/26  06/11/26  97110  Therapeutic exercise x2          130       \", 1)\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", led_dup), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)]\nout = tb.one(recs)\nfor l in out[\"lines\"]:\n    if l.get(\"code\") == \"97110\":\n        print(\"ledger 97110 row:\", \"billed\", (l[\"billed\"] or {}).get(\"cents\"), \"unclear\", l[\"unclear\"], \"checks\", l[\"checks\"], \"dos\", l[\"dos\"])\nprint(\"EOB 97110:\", json.dumps(show_eob(out, \"97110\"), ensure_ascii=False))\nprint(\"all checks:\", [c for l in out[\"lines\"] for c in l[\"checks\"]], \"| payer keys:\", [k for k in keys_anywhere(out) if k in PAYER_KEYS])\n\nprint(\"\\n== R1-M2: rate row 'Charge per visit 185.00 999.00' (r1 rate_balance.py)\")\nrec_txt = tb.tbl(tb.HEAD_TXT, [tb.row(\"06/10/26\", \"06/11/26\", \"99213\", \"Charge per visit\", \"185.00\", \"999.00\")], \"\")\nrecs = [tb.rec(1, \"Medlark Clinic, itemized statement\", rec_txt)]\nout = tb.one(recs)\nprint(\"lines:\", [(l[\"class\"], l[\"detail\"], l.get(\"figure\", {}).get(\"text\") if \"figure\" in l else None, (l[\"balance\"] or {}).get(\"text\") if \"figure\" not in l else None) for l in out[\"lines\"]])\nstructured = json.dumps({k: v for k, v in out.items() if k != \"rules\"}, ensure_ascii=False)\nprint(\"'999.00' in structured output:\", structured.count(\"999.00\"), \"| in excerpts only:\", [l[\"excerpt\"][:60] for l in out[\"lines\"] if \"999.00\" in l[\"excerpt\"]])\nprint(\"unaccounted (whole-row rate exemption in the oracle):\", unaccounted_texts(recs, out))\nprint(\"'999.00' unaccounted with whole-row exemption removed:\", end=\" \")\nitems = tb._items(out)\nprint([t for t, _u in tb.unaccounted(recs, out)] or \"(none)\", \"| _WHOLE_ROW =\", tb._WHOLE_ROW)\n\nprint(\"\\n== R1-M3: EOB unclear list dropped inside the oracle (test-internal, see the r2 mutant runner for the code mutant)\")\nout = B.analyze([tb.rec(1, EOB_SRC if False else \"Quoinmere Mutual Health Plan, explanation of benefits\", tb.eob_text(tb.eob_row(billed=\"$140\")))])\nline = show_eob(out, \"97110\")\nprint(\"EOB row unclear:\", line[\"unclear\"], \"| checks:\", line[\"checks\"])\n\nprint(\"\\n== R1-m1: detail values present in output\")\nout_all = []\nfor name, recs in [(\"sample\", [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)]),\n                   (\"rate\", [tb.rec(1, \"Medlark Clinic, itemized statement\", rec_txt)])]:\n    o = B.analyze(recs)\n    out_all += [(l[\"detail\"], l[\"class\"]) for l in o[\"lines\"]] + [(l[\"detail\"], l[\"class\"]) for l in o[\"lines\"]]\nprint(\"(detail, class) pairs seen:\", sorted(set(out_all), key=str))\n\nprint(\"\\n== R1-M4 / nit: docstring and api wording on balance checks\")\nprint(\"BALANCE_STEP_MISMATCH in CHECKS:\", \"BALANCE_STEP_MISMATCH\" in B.CHECKS, \"| CHECKS keys:\", sorted(B.CHECKS))\nprint(\"CHECKS['LEDGER_EOB_BILLED_MISMATCH'] exists:\", \"LEDGER_EOB_BILLED_MISMATCH\" in B.CHECKS)\nprint(\"module doc has 'no balance step check':\", \"no balance step check\" in B.__doc__, \"| 'no balance reconciliation' in doc:\", \"no balance reconciliation\" in B.__doc__)\n"
}
````

### User / tool · 2026-11-02T06:08:30.030Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/probes/r1_reprobe.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:36.541Z

The write guard only allows `reviews/` and `artifacts/review-evidence/`, so I'll keep the probe scripts there as evidence and leave the archive copy in the scratchpad.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:37.404Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/tbr2.py",
 "content": "\"\"\"Loader for the T-103 r2 probes. Loads tests/unit/test_billing.py from the archive named by T103_ARCH (never from the project tree).\"\"\"\nimport importlib.util, os, sys\nARCH = os.environ[\"T103_ARCH\"]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\nspec = importlib.util.spec_from_file_location(\"tb\", os.path.join(ARCH, \"tests/unit/test_billing.py\"))\ntb = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(tb)\n"
}
````

### User / tool · 2026-11-02T06:08:37.502Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/tbr2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:45.478Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r1_reprobe.py",
 "content": "\"\"\"Re-run of the T-103 r1 probes against the r2 archive (T103_ARCH). Prints the facts for each r1 finding; no assertions here.\"\"\"\nimport json, os, sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport tbr2 as T\ntb = T.tb\nB = tb.B\nLED, EOB = tb.LEDGER, tb.EOB\nPAYER_KEYS = {\"payer_reports\", \"matched_provider\", \"not_added_note\", \"checks\", \"providers\", \"totals\", \"complete\", \"stated_totals\", \"balance_convention\", \"ledger\"}\n\n\ndef keys_anywhere(o):\n    return sorted({k for d in B._walk(o) for k in d})\n\n\ndef unaccounted_texts(recs, out):\n    return [t for t, _u in tb.unaccounted(recs, out)]\n\n\ndef eob_row(out, service):\n    for l in out[\"lines\"]:\n        if l.get(\"form\") == \"eob\" and l.get(\"code\") == service:\n            return {\"class\": l[\"class\"], \"detail\": l[\"detail\"], \"billed\": l.get(\"billed\"), \"paid\": l.get(\"paid\"),\n                    \"eob\": {k: v[\"text\"] + \"/\" + str(v[\"cents\"]) for k, v in (l.get(\"eob\") or {}).items()}, \"unclear\": l[\"unclear\"],\n                    \"checks\": l[\"checks\"], \"excerpt\": l[\"excerpt\"]}\n    return None\n\n\nLEDGER_REC = tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED)\n\nprint(\"== R1-B1 / R1-B2 / R1-M1: EOB $140 against ledger 130.00 (r1 eob_mismatch.py)\")\ne140 = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    $140   \")\nrecs = [LEDGER_REC, tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e140)]\nout = tb.one(recs)\nprint(\"status:\", out[\"status\"], \"| top keys:\", sorted(out))\nprint(\"EOB 97110 row:\", json.dumps(eob_row(out, \"97110\"), ensure_ascii=False))\nprint(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l[\"checks\"]])\nprint(\"unaccounted:\", unaccounted_texts(recs, out))\nprint(\"payer or ledger keys anywhere:\", [k for k in keys_anywhere(out) if k in PAYER_KEYS])\n\nprint(\"\\n== control: EOB 140.00 against ledger 130.00 (r1 expected LEDGER_EOB_BILLED_MISMATCH)\")\ne140b = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    140.00\")\nrecs = [LEDGER_REC, tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e140b)]\nout = tb.one(recs)\nprint(\"EOB 97110 row:\", json.dumps(eob_row(out, \"97110\"), ensure_ascii=False))\nprint(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l[\"checks\"]], \"| payer or ledger keys:\", [k for k in keys_anywhere(out) if k in PAYER_KEYS])\n\nprint(\"\\n== R1-B1: EOB figures without clean cents (r1 eob_oracle.py)\")\nfor label, fig in [(\"$130\", \"$130   \"), (\"1O0.00\", \"1O0.00 \"), (\"130 bare\", \"130    \"), (\"130.5\", \"130.5  \")]:\n    e = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    \" + fig)\n    recs = [LEDGER_REC, tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", e)]\n    out = tb.one(recs)\n    r = eob_row(out, \"97110\")\n    print(label, \"| class:\", r[\"class\"], \"| unclear:\", r[\"unclear\"], \"| eob:\", r[\"eob\"], \"| checks:\", r[\"checks\"], \"| unaccounted:\", unaccounted_texts(recs, out))\n\nprint(\"\\n== R1-M1: same-service second ledger row unreadable (bare 130), EOB 130.00 (r1 eob_probe2.py)\")\nled_dup = LED.replace(\"06/10/26  06/11/26  97014  E-stim unattended              35.00\", \"06/10/26  06/11/26  97110  Therapeutic exercise x2          130       \", 1)\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", led_dup), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)]\nout = tb.one(recs)\nfor l in out[\"lines\"]:\n    if l.get(\"code\") == \"97110\" and l[\"form\"] == \"ledger\":\n        print(\"ledger 97110 row:\", \"billed\", (l[\"billed\"] or {}).get(\"cents\"), \"unclear\", l[\"unclear\"], \"checks\", l[\"checks\"], \"dos\", l[\"dos\"])\nprint(\"EOB 97110:\", json.dumps(eob_row(out, \"97110\"), ensure_ascii=False))\nprint(\"all checks:\", [c for l in out[\"lines\"] for c in l[\"checks\"]], \"| payer or ledger keys:\", [k for k in keys_anywhere(out) if k in PAYER_KEYS])\n\nprint(\"\\n== R1-M2: rate row 'Charge per visit 185.00 999.00' (r1 rate_balance.py)\")\nrec_txt = tb.tbl(tb.HEAD_TXT, [tb.row(\"06/10/26\", \"06/11/26\", \"99213\", \"Charge per visit\", \"185.00\", \"999.00\")], \"\")\nrecs = [tb.rec(1, \"Medlark Clinic, itemized statement\", rec_txt)]\nout = tb.one(recs)\nfor l in out[\"lines\"]:\n    print(\"line:\", l[\"class\"], l[\"detail\"], \"figure\" in l and (\"figure\", l[\"figure\"][\"text\"]) or (\"balance\", (l[\"balance\"] or {}).get(\"text\")), \"excerpt:\", l[\"excerpt\"][:70])\nstructured = json.dumps({k: v for k, v in out.items() if k != \"rules\"}, ensure_ascii=False)\nprint(\"'999.00' occurrences in structured output:\", structured.count(\"999.00\"))\nprint(\"unaccounted (oracle, with whole-row rate exemption):\", unaccounted_texts(recs, out))\nprint(\"_WHOLE_ROW in test module:\", tb._WHOLE_ROW)\n\nprint(\"\\n== R1-m1: (class, detail) pairs for the probe set\")\npairs = set()\nfor name in sorted(tb.PROBES):\n    o = B.analyze(tb.PROBES[name])\n    pairs |= {(l[\"class\"], l[\"detail\"]) for l in o[\"lines\"]}\nprint(sorted(pairs, key=str))\n\nprint(\"\\n== R1-M4 / nit: balance-check wording\")\nprint(\"CHECKS keys:\", sorted(B.CHECKS))\nprint(\"'no balance step check' in module doc:\", \"no balance step check\" in B.__doc__, \"| 'no balance reconciliation' in module doc:\", \"no balance reconciliation\" in B.__doc__)\n"
}
````

### User / tool · 2026-11-02T06:08:45.573Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r1_reprobe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:47.914Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/r1_reprobe.py 2>&1 | tee artifacts/review-evidence/T-103-r2/r1_reprobe_output.txt",
 "description": "Run the r1 probe re-run against the r2 archive copy"
}
````

### User / tool · 2026-11-02T06:08:48.397Z

**tool result**
````
== R1-B1 / R1-B2 / R1-M1: EOB $140 against ledger 130.00 (r1 eob_mismatch.py)
status: listed | top keys: ['lines', 'rules', 'skipped_records', 'status', 'unreconciled']
EOB 97110 row: {"class": "unclear", "detail": "eob", "billed": null, "paid": null, "eob": {}, "unclear": ["$140", "52.00", "78.00", "78.00", "0.00", "0.00", "78.00"], "checks": ["LINE_UNCLEAR"], "excerpt": "06/10/26  97110    $140       52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45"}
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r1_reprobe.py", line 36, in <module>
    print("checks anywhere:", [c for l in out["lines"] for c in l["checks"]])
                                                                ~^^^^^^^^^^
KeyError: 'checks'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:08:53.977Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2 && python3 - <<'PYEOF'\nimport pathlib\np = pathlib.Path(\"/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r1_reprobe.py\")\ns = p.read_text(encoding=\"utf-8\")\ns2 = s.replace('l[\"checks\"] for l in out[\"lines\"]', 'l.get(\"checks\", []) for l in out[\"lines\"]')\ns2 = s2.replace('[c for l in out[\"lines\"] for c in l[\"checks\"]]', '[c for l in out[\"lines\"] for c in l.get(\"checks\", [])]')\ns2 = s2.replace('[c for l in out[\"lines\"] for c in l[\"checks\"]], \"|', '[c for l in out[\"lines\"] for c in l.get(\"checks\", [])], \"|')\ns2 = s2.replace('print(\"all checks:\", [c for l in out[\"lines\"] for c in l[\"checks\"]]', 'print(\"all checks:\", [c for l in out[\"lines\"] for c in l.get(\"checks\", [])]')\ns2 = s2.replace('print(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l[\"checks\"]])', 'print(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l.get(\"checks\", [])])')\ns2 = s2.replace('print(\"EOB 97110 row:\", json.dumps(eob_row(out, \"97110\"), ensure_ascii=False))\\nprint(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l.get(\"checks\", [])], \"| payer', 'print(\"EOB 97110 row:\", json.dumps(eob_row(out, \"97110\"), ensure_ascii=False))\\nprint(\"checks anywhere:\", [c for l in out[\"lines\"] for c in l.get(\"checks\", [])], \"| payer')\np.write_text(s2, encoding=\"utf-8\")\nprint(s2.count('l[\"checks\"]'), \"remaining direct accesses\")\nPYEOF\ncd /Users/arsis/zlayt-pm-project && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/r1_reprobe.py > artifacts/review-evidence/T-103-r2/r1_reprobe_output.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-103-r2/r1_reprobe_output.txt",
 "description": "Patch the probe to tolerate lines without checks, then rerun it"
}
````

### User / tool · 2026-11-02T06:08:54.504Z

**tool result**
````
2 remaining direct accesses
exit=0
== R1-B1 / R1-B2 / R1-M1: EOB $140 against ledger 130.00 (r1 eob_mismatch.py)
status: listed | top keys: ['lines', 'rules', 'skipped_records', 'status', 'unreconciled']
EOB 97110 row: {"class": "unclear", "detail": "eob", "billed": null, "paid": null, "eob": {}, "unclear": ["$140", "52.00", "78.00", "78.00", "0.00", "0.00", "78.00"], "checks": ["LINE_UNCLEAR"], "excerpt": "06/10/26  97110    $140       52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45"}
checks anywhere: ['LINE_UNCLEAR']
unaccounted: []
payer or ledger keys anywhere: ['checks']

== control: EOB 140.00 against ledger 130.00 (r1 expected LEDGER_EOB_BILLED_MISMATCH)
EOB 97110 row: {"class": "unclear", "detail": "eob", "billed": null, "paid": null, "eob": {"billed": "140.00/14000", "discount": "52.00/5200", "allowed": "78.00/7800", "deductible": "78.00/7800", "coinsurance": "0.00/0", "plan_paid": "0.00/0", "patient_owes": "78.00/7800"}, "unclear": [], "checks": [], "excerpt": "06/10/26  97110    140.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45"}
checks anywhere: [] | payer or ledger keys: ['checks']

== R1-B1: EOB figures without clean cents (r1 eob_oracle.py)
$130 | class: unclear | unclear: ['$130', '52.00', '78.00', '78.00', '0.00', '0.00', '78.00'] | eob: {} | checks: ['LINE_UNCLEAR'] | unaccounted: []
1O0.00 | class: unclear | unclear: ['1O0.00', '52.00', '78.00', '78.00', '0.00', '0.00', '78.00'] | eob: {} | checks: ['LINE_UNCLEAR'] | unaccounted: []
130 bare | class: unclear | unclear: ['130', '52.00', '78.00', '78.00', '0.00', '0.00', '78.00'] | eob: {} | checks: ['LINE_UNCLEAR'] | unaccounted: []
130.5 | class: unclear | unclear: ['130.5', '52.00', '78.00', '78.00', '0.00', '0.00', '78.00'] | eob: {} | checks: ['LINE_UNCLEAR'] | unaccounted: []

== R1-M1: same-service second ledger row unreadable (bare 130), EOB 130.00 (r1 eob_probe2.py)
ledger 97110 row: billed 13000 unclear [] checks [] dos 06/10/26
ledger 97110 row: billed None unclear ['130'] checks ['LINE_UNCLEAR'] dos 06/10/26
EOB 97110: {"class": "unclear", "detail": "eob", "billed": null, "paid": null, "eob": {"billed": "130.00/13000", "discount": "52.00/5200", "allowed": "78.00/7800", "deductible": "78.00/7800", "coinsurance": "0.00/0", "plan_paid": "0.00/0", "patient_owes": "78.00/7800"}, "unclear": [], "checks": [], "excerpt": "06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45"}
all checks: ['LINE_UNCLEAR'] | payer or ledger keys: ['checks']

== R1-M2: rate row 'Charge per visit 185.00 999.00' (r1 rate_balance.py)
line: rate rate ('figure', '185.00') excerpt: 06/10/26  06/11/26  99213  Charge per visit              185.00       
'999.00' occurrences in structured output: 2
unaccounted (oracle, with whole-row rate exemption): []
_WHOLE_ROW in test module: ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance')

== R1-m1: (class, detail) pairs for the probe set
[('adjustment', None), ('charge', 'reversal'), ('charge', None), ('payment', None), ('rate', 'rate'), ('unclear', 'asserted_balance'), ('unclear', 'balance_forward'), ('unclear', 'eob'), ('unclear', 'estimate'), ('unclear', 'reduction'), ('unclear', 'stated_total_adjustment'), ('unclear', 'stated_total_balance'), ('unclear', 'stated_total_billed'), ('unclear', 'stated_total_paid'), ('unclear', None)]

== R1-M4 / nit: balance-check wording
CHECKS keys: ['LINE_UNCLEAR', 'NO_DATE_OF_SERVICE', 'ROW_NOT_PARSED']
'no balance step check' in module doc: True | 'no balance reconciliation' in module doc: False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:06.465Z

**tool call — Bash**
````
{
 "command": "grep -rn \"LEDGER_EOB\\|_sum(\\|_tot(\\|payer_reports\\|BALANCE_STEP\\|balance_convention\\|stated_totals\\|complete\\b\" app/ tests/unit/test_billing.py memory/contracts/api.md --include=*.py --include=*.md --include=*.html --include=*.js --include=*.jsx --include=*.ts --include=*.tsx 2>/dev/null | cut -c1-230 | head -60",
 "description": "Grep app, tests and API doc for removed total and check names"
}
````

### User / tool · 2026-11-02T06:09:06.566Z

**tool result**
````
app/README-arch.md:32:  provider.py      complete(model, system, user, json_schema) -> dict ; complete_with_meta
app/llm/provider.py:1:"""Provider interface (ADR-004, R-CO-2/6): complete(model, system, user, json_schema) -> dict over three backends.
app/llm/provider.py:113:def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
app/backend/ingest.py:79:    cov, f = [], {"date_raw": "", "source": "", "excerpt": "", "complete": False}
app/backend/ingest.py:96:    f["complete"] = found == 3
app/backend/ingest.py:126:        if not f["complete"]:
app/backend/ingest.py:191:        f = f or {"date_raw": "", "source": "", "excerpt": "", "complete": False}
app/backend/ingest.py:268:        # (one labelled but incomplete record gets no reason: SPLIT_AMBIGUOUS already describes it, and "several records" would be false)
app/backend/billing.py:5:'complete' flag, no balance step check, no ledger-versus-EOB check (D-052; five review rounds kept finding ways a total could silently omit a
app/backend/billing.py:170:    absorbed: the earlier one is listed as an unparsed line (the paralegal sees it, the provider is incomplete), the later one is kept (D-049)."""
app/backend/billing.py:180:    line with the total's own excerpt: the provider is incomplete, and the figure is not left only in a field nobody opens."""
app/backend/billing.py:563:# its OWN tokenizer, after every parser has run, and lists whatever no parser placed; the provider of such a line is complete: false.
app/backend/trace.py:529:        code = {"injection_suspected": "INJECTION_SUSPECTED", "analysis_incomplete": "CONFLICT_CHECK_INCOMPLETE", "llm_split": "LLM_SPLIT", "date_ambiguous": "DATE_AMBIGUOUS"}.get(cat) \
app/backend/trace.py:954:    if any(f["category"] == "analysis_incomplete" for f in flgs):
app/backend/flag_templates.py:38:    "date_ambiguous": "record_warning", "injection_suspected": "record_warning", "analysis_incomplete": "record_warning", "llm_split": "record_warning",
app/backend/flag_templates.py:138:    "analysis_incomplete": lambda v: ("Cross-record check did not finish",
app/backend/totals.py:28:    status = "none_found" if not found else ("partial_unclear" if unclear else "complete")
tests/unit/test_billing.py:77:_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
tests/unit/test_billing.py:132:    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH", "BALANCE_STEP_MISMATCH",
tests/unit/test_billing.py:133:            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
tests/unit/test_billing.py:277:    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})
tests/unit/test_billing.py:795:    assert not [k for d in B._walk(out) for k in d if k in ("ledger", "payer_reports", "matched_provider")]
memory/contracts/api.md:39:| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled r
memory/contracts/api.md:246:(D-040: `source_kind` is always `"record"`. No chip or label says who is speaking; the verbatim excerpt shows it. The field stays for compatibility. The flag category `patient_report` is a lexicon phras
memory/contracts/api.md:664:Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line). Computed on re
memory/contracts/api.md:695:**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D
memory/contracts/api.md:746:| `CONFLICT_CHECK_INCOMPLETE` | needs_review | the cross-record conflict check failed or had no recorded answer; conflicts between records may be missing (case-level `record_warning` `analysis_incomplet
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:16.866Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/route_keys.py",
 "content": "\"\"\"T-103 r2: the billing route (fixture backend, ingest only, TestClient) on the golden cases and the EOB probe. Prints every key path in the\n`billing` object (list indices collapsed) and the total-like names found, plus the HTTP status. Run with T103_ARCH set to the archive copy.\"\"\"\nimport json, os, re, sys, tempfile, time\nARCH = os.environ[\"T103_ARCH\"]\nsys.path.insert(0, ARCH)\nos.chdir(ARCH)\nos.environ[\"LLM_BACKEND\"] = \"fixture\"; os.environ[\"ZLAYT_MODE\"] = \"local\"\nos.environ.pop(\"ANTHROPIC_API_KEY\", None); os.environ.pop(\"ENABLE_LIVE\", None)\nfrom fastapi.testclient import TestClient\nfrom app.backend.api import create_app\nfrom app.db import db as DB\nfrom app.backend import pipeline as PL\n\nTOTAL_LIKE = re.compile(r\"total|sum|complete|balance_convention|stated|providers|payer|ledger|matched|not_added|grand|overall|count_billed\", re.IGNORECASE)\nEOB_CASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), \"case_eob_140.txt\")\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport tbr2 as T\ntb = T.tb\nLEDGER, EOB = tb.LEDGER, tb.EOB\ne140 = EOB.replace(\"06/10/26  97110    130.00\", \"06/10/26  97110    $140   \")\nwith open(EOB_CASE, \"w\", encoding=\"utf-8\") as fh:\n    fh.write(\"=== Record 1 ===\\nDate: 2026-06-15\\nSource: Larkspur Hollow Physical Therapy, itemized statement\\nExcerpt: \\\"\" + LEDGER + \"\\\"\\n\\n\"\n             \"=== Record 2 ===\\nDate: 2026-07-22\\nSource: Quoinmere Mutual Health Plan, explanation of benefits\\nExcerpt: \\\"\" + e140 + \"\\\"\\n\")\n\nCASES = {\n    \"sample\": os.path.join(ARCH, \"evals/golden/sample.txt\"),\n    \"case_03_rate_and_ocr\": os.path.join(ARCH, \"evals/golden/case_03_rate_and_ocr.txt\"),\n    \"case_09_nonvisit_hides_gap\": os.path.join(ARCH, \"evals/golden/case_09_nonvisit_hides_gap.txt\"),\n    \"eob_140_vs_ledger\": EOB_CASE,\n}\n\n\ndef key_paths(o, prefix=\"\"):\n    out = set()\n    if isinstance(o, dict):\n        for k, v in o.items():\n            p = f\"{prefix}.{k}\" if prefix else k\n            out.add(p)\n            out |= key_paths(v, p)\n    elif isinstance(o, list):\n        for v in o:\n            out |= key_paths(v, prefix + \"[]\")\n    return out\n\n\nfor name, path in CASES.items():\n    d = tempfile.mkdtemp(prefix=\"t103r2_\")\n    text = open(path, encoding=\"utf-8\").read()\n    c = TestClient(create_app(os.path.join(d, \"x.sqlite\"), static_dir=d), client=(\"127.0.0.1\", 5000))\n    conn = DB.connect(c.app.state.db_path)\n    tok = DB.create_case(conn, text, now=time.time())\n    PL.ingest_case(conn, tok, text, time.time())\n    conn.close()\n    r = c.get(f\"/api/cases/{tok}/billing\")\n    body = r.json()\n    billing = body.get(\"billing\") or {}\n    paths = sorted(key_paths(billing))\n    top = sorted(billing)\n    print(f\"== {name}: HTTP {r.status_code}; billing top-level keys: {top}\")\n    print(\"   total-like key paths:\", [p for p in paths if TOTAL_LIKE.search(p)] or \"none\")\n    print(\"   distinct key paths:\", len(paths))\n    print(\"   status:\", billing.get(\"status\"), \"| citation_failures:\", billing.get(\"citation_failures\"), \"| lines:\", len(billing.get(\"lines\", [])),\n          \"| unreconciled:\", len(billing.get(\"unreconciled\", [])), \"| skipped:\", len(billing.get(\"skipped_records\", [])))\n    if name == \"eob_140_vs_ledger\":\n        eob = [l for l in billing.get(\"lines\", []) if l.get(\"form\") == \"eob\"]\n        print(\"   EOB lines:\", json.dumps([{k: l[k] for k in (\"code\", \"class\", \"detail\", \"unclear\", \"checks\")} for l in eob], ensure_ascii=False))\n        print(\"   any check codes:\", sorted({c for l in billing.get(\"lines\", []) for c in l.get(\"checks\", [])}))\n    print(\"   key paths:\", paths)\n"
}
````

### User / tool · 2026-11-02T06:09:16.962Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/route_keys.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:19.770Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/route_keys.py > artifacts/review-evidence/T-103-r2/route_keys_output.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-103-r2/route_keys_output.txt | cut -c1-1500",
 "description": "Run the billing route on golden cases and the EOB probe, saving key paths"
}
````

### User / tool · 2026-11-02T06:09:20.343Z

**tool result**
````
exit=0
== sample: HTTP 200; billing top-level keys: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled']
   total-like key paths: none
   distinct key paths: 6
   status: none_found | citation_failures: [] | lines: 0 | unreconciled: 0 | skipped: 0
   key paths: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled']
== case_03_rate_and_ocr: HTTP 200; billing top-level keys: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled']
   total-like key paths: none
   distinct key paths: 15
   status: listed | citation_failures: [] | lines: 0 | unreconciled: 1 | skipped: 0
   key paths: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled', 'unreconciled[].class', 'unreconciled[].excerpt', 'unreconciled[].figures', 'unreconciled[].form', 'unreconciled[].id', 'unreconciled[].message', 'unreconciled[].provider', 'unreconciled[].reason_code', 'unreconciled[].record_no']
== case_09_nonvisit_hides_gap: HTTP 200; billing top-level keys: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled']
   total-like key paths: none
   distinct key paths: 33
   status: listed | citation_failures: [] | lines: 1 | unreconciled: 0 | skipped: 0
   key paths: ['citation_failures', 'lines', 'lines[].adjustment', 'lines[].balance', 'lines[].billed', 'lines[].billed.cents', 'lines[].billed.text', 'lines[].billed.usd', 'lines[].checks', 'lines[].cites', 'lines[].cites[].excerpt', 'lines[].cites[].record_no', 'lines[].class', 'lines[].code', 'lines[].description', 'lines[].detail', 'lines[].dos', 'lines[].dos_iso', 'lines[].excerpt', 'lines[].form', 'lines[].id', 'lines[].negotiated', 'lines[].paid', 'lines[].posted', 'lines[].provider', 'lines[].record_no', 'lines[].record_nos', 'lines[].unclear', 'lines[].unparsed', 'rules', 'skipped_records', 'status', 'unreconciled']
== eob_140_vs_ledger: HTTP 200; billing top-level keys: ['citation_failures', 'lines', 'rules', 'skipped_records', 'status', 'unreconciled']
   total-like key paths: none
   distinct key paths: 83
   status: listed | citation_failures: [] | lines: 15 | unreconciled: 1 | skipped: 0
   EOB lines: [{"code": "97110", "class": "unclear", "detail": "eob", "unclear": ["$140", "52.00", "78.00", "78.00", "0.00", "0.00", "78.00"], "checks": ["LINE_UNCLEAR"]}, {"code": "97140", "class": "unclear", "detail": "eob", "unclear": [], "checks": []}, {"code": "97014", "class": "unclear", "detail": "eob", "unclear": [], "checks": []}]
   any check codes: ['LINE_UNCLEAR']
   key paths: ['citation_failures', 'lines', 'lines[].adjustment', 'lines[].adjustment.cents', 'lines[].adjustment.text', 'lines[].adjustment.usd', 'lines[].balance', 'lines[].balance.cents', 'lines[].balance.text', 'lines[].balance.usd', 'lines[].billed', 'lines[].billed.cents', 'lines[].billed.text', 'lines[].billed.usd', 'lines[].checks', 'lines[].cites', 'lines[].cites[].excerpt', 'lines[].cites[].record_no', 'lines[].class', 'lines[].code', 'lines[].description', 'lines[].detail', 'lines[].dos', 'lines[].dos_iso', 'lines[].eob', 'lines[].eob.allowed', 'lines[].eob.allowed.cents', 'lines[].eob.allowed.text', 'lines[].eob.allowed.usd', 'lines[].eob.billed', 'lines[].eob.billed.cents', 'lines[].eob.billed.text', 'lines[].eob.billed.usd', 'lines[].eob.coinsurance', 'lines[].eob.coinsurance.cents', 'lines[].eob.coinsurance.text', 'lines[].eob.coinsurance.usd', 'lines[].eob.deductible', 'lines[].eob.deductible.cents', 'lines[].eob.deductible.text', 'lines[].eob.deductible.usd', 'lines[].eob.discount', 'lines[].eob.discount.cents', 'lines[].eob.discount.text', 'lines[].eob.discount.usd', 'lines[].eob.patient_owes', 'lines[].eob.patient_owes.cents', 'lines[].eob.patient_owes.text', 'lines[].eob.patient_owes.usd', 'lines[].eob.plan_paid', 'lines[].eob.plan_paid.cents', 'lines[].eob.plan_paid.text', 'lines[].eob.plan_paid.usd', 'lines[].eob_codes', 'lines[].excerpt', 'lines[].figure', 'lines[].figure.cents', 'lines[].figure.text', 'lines[].figure.usd', 'lines[].form', 'lines[].id'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:31.767Z

The route is clean: no total-like key paths on any of the four cases. Next I'll run the mutants in scratch copies, starting with anchor counts so nothing silently fails to apply.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:38.752Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/run_mutants_r2.py",
 "content": "\"\"\"T-103 r2 mutation runner. Copies the archive (argv[1]) into one scratch dir per mutant (argv[2]), applies one replacement set per mutant\n(each anchor must match exactly once, otherwise the mutant is reported NOT APPLIED), and runs tests/unit/test_billing.py in that copy.\nThe archive itself is never edited. Usage: run_mutants_r2.py <ARCH> <MUTDIR>\"\"\"\nimport os, re, shutil, subprocess, sys\nARCH, MUT = sys.argv[1], sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nBILL = \"app/backend/billing.py\"\nTEST = \"tests/unit/test_billing.py\"\nEOB_SEL = \"eob or probe or property or bare or oracle\"\n\nMUTANTS = {\n    # EOB accounting (T-103 r1 M06 analogue, now aimed at the r2 code)\n    \"R01_eob_unreadable_figure_unclear_dropped\": (BILL, [\n        ('line[\"unclear\"] = [f[\"text\"] for f in figs]', 'line[\"unclear\"] = []')]),\n    \"R02_eob_unparsed_rows_and_printed_total_dropped\": (BILL, [\n        ('got = rows_ + unp_', 'got = rows_')]),\n    \"R03_eob_accounting_pass_off\": (BILL, [\n        ('if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\", \"eob\"):', 'if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\"):')]),\n    \"R04_eob_structured_first_column_dropped\": (BILL, [\n        ('line[\"eob\"] = {k: _mag(f) for k, f in zip(names, figs)}', 'line[\"eob\"] = {k: _mag(f) for k, f in list(zip(names, figs))[1:]}')]),\n    \"R05_eob_unclear_dropped_and_accounting_off\": (BILL, [\n        ('line[\"unclear\"] = [f[\"text\"] for f in figs]', 'line[\"unclear\"] = []'),\n        ('if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\", \"eob\"):', 'if form in (\"ledger_table\", \"ledger_text\", \"cms1500\", \"ub04\"):')]),\n    # the r1 set, re-aimed at the r2 code (generic accounting net and the other forms)\n    \"R06_accounting_net_off_all_forms\": (BILL, [\n        ('got = got + _account(r, form, body, ls, got, stated_by_rec.get(r[\"n\"]) or {}, balfwds.get(r[\"n\"]) or [], rates, lop_here)', 'got = got + []')]),\n    \"R07_unreconciled_list_dropped\": (BILL, [\n        ('for l in lines if l[\"unparsed\"]]', 'for l in lines if l[\"unparsed\"] and False]')]),\n    \"R08_verifier_stubbed\": (BILL, [\n        ('    text_of = {r[\"n\"]: (r.get(\"text\") or r.get(\"excerpt\") or \"\") for r in records}', '    return []\\n    text_of = {r[\"n\"]: (r.get(\"text\") or r.get(\"excerpt\") or \"\") for r in records}')]),\n    \"R09_rate_row_dropped_and_accounting_off\": (BILL, [\n        ('got = got + _account(r, form, body, ls, got, stated_by_rec.get(r[\"n\"]) or {}, balfwds.get(r[\"n\"]) or [], rates, lop_here)', 'got = got + []'),\n        ('rates.append(_rate_entry(rec, f, ln.strip(), \"This row says it is a per-visit/unit/rate figure: a rate is a price, not a charge. It is not totaled.\"))', 'pass')]),\n    # test-side probe of the r1 M2 gap: the oracle's whole-row exemption for a rate row is what lets its running balance pass\n    \"T01_oracle_rate_whole_row_exemption_removed\": (TEST, [\n        ('_WHOLE_ROW = (\"rate\", \"estimate\", \"reduction\", \"lien_amount\", \"asserted_balance\")', '_WHOLE_ROW = (\"estimate\", \"reduction\", \"lien_amount\", \"asserted_balance\")')]),\n}\n\nSELECTIONS = [None, EOB_SEL]\nIGNORE = shutil.ignore_patterns(\"__pycache__\", \"artifacts\", \"board\", \"reviews\", \"research\", \"submission\", \"*.sqlite\", \".git\")\nos.makedirs(MUT, exist_ok=True)\nfor name, (rel, reps) in MUTANTS.items():\n    dst = os.path.join(MUT, name)\n    if os.path.exists(dst):\n        shutil.rmtree(dst)\n    shutil.copytree(ARCH, dst, ignore=IGNORE)\n    p = os.path.join(dst, rel)\n    src = open(p, encoding=\"utf-8\").read()\n    counts = [src.count(old) for old, _new in reps]\n    if any(c != 1 for c in counts):\n        print(f\"{name}: NOT APPLIED (anchor match counts {counts})\")\n        continue\n    for old, new in reps:\n        src = src.replace(old, new)\n    open(p, \"w\", encoding=\"utf-8\").write(src)\n    for sel in SELECTIONS:\n        cmd = [PY, \"-m\", \"pytest\", \"-q\", \"-p\", \"no:cacheprovider\", TEST] + ([\"-k\", sel] if sel else [])\n        r = subprocess.run(cmd, cwd=dst, capture_output=True, text=True)\n        summ = [l for l in r.stdout.splitlines() if re.search(r\"\\d+ (passed|failed)\", l)]\n        failed = [l.split(\"::\", 1)[1].split(\" \")[0] for l in r.stdout.splitlines() if l.startswith(\"FAILED\")]\n        label = sel or \"full file\"\n        print(f\"{name} [{label}]: rc={r.returncode} {summ[-1] if summ else r.stdout[-200:]}\")\n        for f in failed[:10]:\n            print(\"    FAILED\", f)\n        if len(failed) > 10:\n            print(f\"    ... {len(failed)} failing in total\")\n"
}
````

### User / tool · 2026-11-02T06:09:38.856Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/run_mutants_r2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:09:41.578Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && .venv/bin/python -I artifacts/review-evidence/T-103-r2/run_mutants_r2.py $SCR/head $SCR/mut > artifacts/review-evidence/T-103-r2/mutation_results_r2.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-103-r2/mutation_results_r2.txt",
 "description": "Run the billing mutants in scratch copies and save results"
}
````

### User / tool · 2026-11-02T06:10:10.201Z

**tool result**
````
exit=0
R01_eob_unreadable_figure_unclear_dropped [full file]: rc=1 7 failed, 172 passed in 1.44s
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[$140]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[$130]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[1O0.00]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[130]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[130.5]
    FAILED test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised
    FAILED test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept
R01_eob_unreadable_figure_unclear_dropped [eob or probe or property or bare or oracle]: rc=1 7 failed, 78 passed, 94 deselected in 1.03s
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[$140]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[$130]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[1O0.00]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[130]
    FAILED test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text[130.5]
    FAILED test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised
    FAILED test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept
R02_eob_unparsed_rows_and_printed_total_dropped [full file]: rc=0 179 passed in 1.10s
R02_eob_unparsed_rows_and_printed_total_dropped [eob or probe or property or bare or oracle]: rc=0 85 passed, 94 deselected in 0.92s
R03_eob_accounting_pass_off [full file]: rc=1 2 failed, 177 passed in 0.75s
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_property_a_random_money_token_is_never_silently_missing
R03_eob_accounting_pass_off [eob or probe or property or bare or oracle]: rc=1 2 failed, 83 passed, 94 deselected in 0.54s
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_property_a_random_money_token_is_never_silently_missing
R04_eob_structured_first_column_dropped [full file]: rc=1 4 failed, 175 passed in 1.21s
    FAILED test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger
    FAILED test_eob_row_reason_codes_and_service_code_are_not_money_tokens
    FAILED test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept
    FAILED test_eob_is_lines_not_a_skip
R04_eob_structured_first_column_dropped [eob or probe or property or bare or oracle]: rc=1 4 failed, 81 passed, 94 deselected in 1.01s
    FAILED test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger
    FAILED test_eob_row_reason_codes_and_service_code_are_not_money_tokens
    FAILED test_eob_fail_safe_names_a_figure_dropped_from_a_row_and_stays_silent_when_it_is_kept
    FAILED test_eob_is_lines_not_a_skip
R05_eob_unclear_dropped_and_accounting_off [full file]: rc=1 19 failed, 160 passed in 1.02s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_bare_under_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents_paid]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_extra_figure]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_ledger_conflict]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_missing_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_ocr_letters]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_odd_decimals]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_paid]
    ... 19 failing in total
R05_eob_unclear_dropped_and_accounting_off [eob or probe or property or bare or oracle]: rc=1 19 failed, 66 passed, 94 deselected in 0.81s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_bare_under_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents_paid]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_extra_figure]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_ledger_conflict]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_missing_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_ocr_letters]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_odd_decimals]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_paid]
    ... 19 failing in total
R06_accounting_net_off_all_forms [full file]: rc=1 6 failed, 173 passed in 0.77s
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none
    FAILED test_property_a_random_money_token_is_never_silently_missing
R06_accounting_net_off_all_forms [eob or probe or property or bare or oracle]: rc=1 5 failed, 80 passed, 94 deselected in 0.58s
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_property_a_random_money_token_is_never_silently_missing
R07_unreconciled_list_dropped [full file]: rc=1 78 failed, 101 passed in 2.02s
    FAILED test_cms1500_line_that_does_not_fit_is_unreconciled_with_its_excerpt
    FAILED test_ledger_row_with_no_date_is_unreconciled_and_its_total_is_a_line
    FAILED test_verifier_covers_every_cite_bearing_field
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_no_dates]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_no_units]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_printed_dollar]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_bare_under_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents_paid]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_extra_figure]
    ... 78 failing in total
R07_unreconciled_list_dropped [eob or probe or property or bare or oracle]: rc=1 49 failed, 36 passed, 94 deselected in 1.29s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_no_dates]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_no_units]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[cms_printed_dollar]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_bare_under_column]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_dollar_no_cents_paid]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_extra_figure]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_figure_above_header]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_ledger_conflict]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[eob_missing_column]
    ... 49 failing in total
R08_verifier_stubbed [full file]: rc=1 4 failed, 175 passed in 1.13s
    FAILED test_verify_citations_catches_an_uncited_line
    FAILED test_verifier_reference_is_the_record_text_not_the_excerpt
    FAILED test_verifier_covers_every_cite_bearing_field
    FAILED test_billing_route_returns_citation_failures_and_flags_the_status
R08_verifier_stubbed [eob or probe or property or bare or oracle]: rc=0 85 passed, 94 deselected in 0.88s
R09_rate_row_dropped_and_accounting_off [full file]: rc=1 16 failed, 163 passed in 1.07s
    FAILED test_table_row_charge_per_visit_is_a_rate_line_listed_once[185.00]
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Visit
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Rate
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Hourly
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Charge
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Daily
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_no_cents]
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    ... 16 failing in total
R09_rate_row_dropped_and_accounting_off [eob or probe or property or bare or oracle]: rc=1 6 failed, 79 passed, 94 deselected in 0.60s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_no_cents]
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_property_a_random_money_token_is_never_silently_missing
T01_oracle_rate_whole_row_exemption_removed [full file]: rc=1 2 failed, 177 passed in 1.16s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_no_cents]
T01_oracle_rate_whole_row_exemption_removed [eob or probe or property or bare or oracle]: rc=1 2 failed, 83 passed, 94 deselected in 0.97s
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_dollar_no_cents]
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_no_cents]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:19.628Z

Results so far: the EOB unclear-drop mutant (R01) is caught by 7 tests, but R02 survives. I want to confirm why before recording it, and also pin down what the rate-row exemption (T01) is hiding.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:23.217Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r2_survivor_and_m2_check.py",
 "content": "\"\"\"T-103 r2: why mutant R02 survives (EOB unparsed rows dropped), and what the rate-row whole-row exemption hides (r1 M2).\nRun with T103_ARCH = the archive copy (R02 and T01 mutant copies are passed as T103_ARCH by the caller).\"\"\"\nimport json, os, sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport tbr2 as T\ntb = T.tb\nB = tb.B\nLED, EOB = tb.LEDGER, tb.EOB\n\nprint(\"== R02 check: EOB with a printed TOTAL row (unparsed row), the TOTAL row's excerpt and figures in the output\")\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", LED), tb.rec(2, \"Quoinmere Mutual Health Plan, explanation of benefits\", EOB)]\nout = B.analyze(recs)\nprint(\"unreconciled rows:\", [(u[\"form\"], u[\"excerpt\"][:40], u[\"figures\"]) for u in out[\"unreconciled\"]])\nprint(\"unaccounted:\", [t for t, _u in tb.unaccounted(recs, out)])\n\nprint(\"\\n== T01 check: rate-row running balance with the whole-row exemption (the r1 M2 gap)\")\nrec_txt = tb.tbl(tb.HEAD_TXT, [tb.row(\"06/10/26\", \"06/11/26\", \"99213\", \"Charge per visit\", \"185.00\", \"999.00\")], \"\")\nrecs = [tb.rec(1, \"Medlark Clinic, itemized statement\", rec_txt)]\nout = B.analyze(recs)\nrate = [l for l in out[\"lines\"] if l[\"class\"] == \"rate\"]\nprint(\"rate line keys:\", sorted(rate[0].keys()))\nprint(\"rate line figure:\", rate[0].get(\"figure\"), \"| balance:\", rate[0].get(\"balance\"))\nprint(\"rate line whole-row flag detail:\", rate[0][\"detail\"])\nprint(\"tokens with the exemption in force:\", [t for t, _u in tb.unaccounted(recs, out)])\nprint(\"tokens with the exemption removed in the oracle:\", [t for t, _u in tb.unaccounted(recs, out)] if False else \"(see T01 mutant run)\")\nprint(\"oracle items for the rate row:\", [(ex[:40], sorted(texts), whole) for ex, texts, whole in tb._items(out)])\nprint(\"_WHOLE_ROW:\", tb._WHOLE_ROW)\n"
}
````

### User / tool · 2026-11-02T06:10:23.311Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/r2_survivor_and_m2_check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:26.955Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && echo \"### run on HEAD archive copy\" && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/r2_survivor_and_m2_check.py 2>&1; echo \"### run on R02 mutant copy (EOB unparsed rows dropped)\" && T103_ARCH=$SCR/mut/R02_eob_unparsed_rows_and_printed_total_dropped .venv/bin/python -I artifacts/review-evidence/T-103-r2/r2_survivor_and_m2_check.py 2>&1 | head -4; echo \"### T01 mutant copy: the rate row with exemption removed\"; T103_ARCH=$SCR/mut/T01_oracle_rate_whole_row_exemption_removed .venv/bin/python -I artifacts/review-evidence/T-103-r2/r2_survivor_and_m2_check.py 2>&1 | sed -n 5,7p",
 "description": "Check the surviving R02 mutant and the rate-row exemption"
}
````

### User / tool · 2026-11-02T06:10:28.343Z

**tool result**
````
### run on HEAD archive copy
== R02 check: EOB with a printed TOTAL row (unparsed row), the TOTAL row's excerpt and figures in the output
unreconciled rows: [('eob', 'TOTAL              235.00   115.00    12', ['235.00', '115.00', '120.00', '100.00', '4.00', '16.00', '104.00'])]
unaccounted: []

== T01 check: rate-row running balance with the whole-row exemption (the r1 M2 gap)
rate line keys: ['cites', 'class', 'detail', 'excerpt', 'figure', 'form', 'id', 'provider', 'record_no', 'record_nos', 'why']
rate line figure: {'text': '185.00', 'cents': 18500, 'usd': '$185.00'} | balance: None
rate line whole-row flag detail: rate
tokens with the exemption in force: []
tokens with the exemption removed in the oracle: (see T01 mutant run)
oracle items for the rate row: [('06/10/26  06/11/26  99213  Charge per vi', ['185.00'], True)]
_WHOLE_ROW: ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance')
### run on R02 mutant copy (EOB unparsed rows dropped)
== R02 check: EOB with a printed TOTAL row (unparsed row), the TOTAL row's excerpt and figures in the output
unreconciled rows: [('eob', 'TOTAL              235.00   115.00    12', ['235.00', '115.00', '120.00', '100.00', '4.00', '16.00', '104.00'])]
unaccounted: []

### T01 mutant copy: the rate row with exemption removed
== T01 check: rate-row running balance with the whole-row exemption (the r1 M2 gap)
rate line keys: ['cites', 'class', 'detail', 'excerpt', 'figure', 'form', 'id', 'provider', 'record_no', 'record_nos', 'why']
rate line figure: {'text': '185.00', 'cents': 18500, 'usd': '$185.00'} | balance: None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:32.418Z

R02 survives because the accounting pass re-lists the dropped TOTAL row's seven figures, so that drop loses nothing. The rate-row balance (T01) is confirmed as a gap that only the whole-row exemption covers. Next I need to confirm the three billing files are clean in the working tree, since the project-tree pytest run is only meaningful if they are.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:33.670Z

**tool call — Bash**
````
{
 "command": "git status --short -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; echo \"status-exit=$? (empty above = clean)\"; git diff --stat HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; echo \"HEAD=$(git rev-parse --short HEAD)\"; echo \"--- project-tree pytest\"; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_billing.py > artifacts/review-evidence/T-103-r2/pytest_billing_HEAD_bcdcb91.txt 2>&1; echo \"pytest-exit=$?\"; tail -3 artifacts/review-evidence/T-103-r2/pytest_billing_HEAD_bcdcb91.txt",
 "description": "Check billing files are clean at HEAD and run the billing unit tests"
}
````

### User / tool · 2026-11-02T06:10:35.098Z

**tool result**
````
status-exit=0 (empty above = clean)
HEAD=c2a5d1f
--- project-tree pytest
pytest-exit=0
........................................................................ [ 80%]
...................................                                      [100%]
179 passed in 1.04s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:37.103Z

HEAD has moved from bcdcb91 to c2a5d1f during the review. I need to see what changed and whether the three billing files differ from the pinned commit.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:38.180Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && echo \"--- billing files bcdcb91 vs HEAD:\" && git diff --stat bcdcb91 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md; echo \"(empty = identical)\"; echo \"--- all files changed bcdcb91..HEAD:\" && git diff --stat bcdcb91 HEAD | tail -5; echo \"--- c2a5d1f subject:\"; git show -s --format='%H %s' c2a5d1f",
 "description": "Show new HEAD commits and whether billing files changed since bcdcb91"
}
````

### User / tool · 2026-11-02T06:10:38.337Z

**tool result**
````
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
3462ad0 fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
--- billing files bcdcb91 vs HEAD:
(empty = identical)
--- all files changed bcdcb91..HEAD:
 tests/unit/test_provider.py            |   4 +-
 tests/unit/test_provider_backends.py   |   2 +-
 tests/unit/test_t093_eval_signature.py |   5 +-
 tests/unit/test_trace.py               |  23 ++++
 15 files changed, 317 insertions(+), 23 deletions(-)
--- c2a5d1f subject:
c2a5d1fd1d7514de8daac1d75f395c9801c8399b fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:43.925Z

HEAD moved to c2a5d1f with two later commits (3462ad0, c2a5d1f), and the three billing files are byte-identical to bcdcb91, so the pinned review stands. Next I'll check the remaining comparisons under the strict reading and the stale comments that still mention a removed provider-completeness concept.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:44.816Z

**tool call — Bash**
````
{
 "command": "F=app/backend/billing.py && for r in 166,172 177,182 560,565 646,672 700,728 806,812; do echo \"--- $F $r\"; awk -v a=${r%,*} -v b=${r#*,} 'NR>=a && NR<=b {printf \"%d: %s\\n\", NR, substr($0,1,240)}' $F; done",
 "description": "Read billing.py sections with comparisons and stale comments"
}
````

### User / tool · 2026-11-02T06:10:44.871Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to =a && NR<=b {printf "%d: %s\n", NR, substr($0,1,240)})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:46.711Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 166,
 "limit": 16
}
````

### User / tool · 2026-11-02T06:10:46.722Z

**tool result**
````
166	
167	
168	def _put_stated(rec, stated, new, out):
169	    """Record the totals a statement prints. A second figure for the same total (equal or different) is never guessed between or silently
170	    absorbed: the earlier one is listed as an unparsed line (the paralegal sees it, the provider is incomplete), the later one is kept (D-049)."""
171	    for k, v in new.items():
172	        old = stated.get(k)
173	        if old:
174	            out.append(_blank_line(rec, "ledger", old["cite"]["excerpt"], unparsed=True, unclear=[old["text"]]))
175	        stated[k] = v
176	
177	
178	def _stated_orphans(rec, lform, got, stated):
179	    """A printed total that could not be read (cents None), or that belongs to a statement with no readable line at all, is listed as an unparsed
180	    line with the total's own excerpt: the provider is incomplete, and the figure is not left only in a field nobody opens."""
181	    by_ex = {}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:47.020Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 558,
 "limit": 8
}
````

### User / tool · 2026-11-02T06:10:47.027Z

**tool result**
````
558	
559	
560	# ------------------------------------------------------------------ D-049: the final accounting pass
561	# Every money-shaped token the record prints must end up in one of four places: a parsed figure (a line, a stated total, a balance forward), an
562	# unreconciled line, an excluded rate (or an LOP/lien amount, which is listed apart), or on its row as `unclear`. This pass reads the raw text with
563	# its OWN tokenizer, after every parser has run, and lists whatever no parser placed; the provider of such a line is complete: false.
564	_A = r"[0-9OolISB]"
565	_ACC_MONEY = re.compile(rf"\(?-?\$\s?{_A}[0-9OolISB,]*(?:\.{_A}+)?\)?-?(?![\w/])|(?<![\w/.$])\(?-?[0-9OolISB,]*[0-9][0-9OolISB,]*\.{_A}{{2}}\)?-?(?![\w/]|\.\d)")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:47.349Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 646,
 "limit": 28
}
````

### User / tool · 2026-11-02T06:10:47.358Z

**tool result**
````
646	            add(l["excerpt"], t)
647	    for v in list(stated.values()) + list(bfs):
648	        add(v["cite"]["excerpt"], v["text"])
649	    whole = [x["excerpt"].strip() for x in list(rates) + list(lop)]      # an excluded rate / LOP entry carries its whole row (running balance included)
650	    hi, cols = _header(ls) if form == "ledger_table" else _ub_header(ls) if form == "ub04" else _eob_header(ls) if form == "eob" else (None, None)
651	    units = [(body[s:e], True) for s, e in _segments(body)] if form == "ledger_text" else [(u, hi is not None and i > hi) for i, u in enumerate(ls)]
652	    lform = "ledger" if form.startswith("ledger") else form
653	    extra = []
654	    for u, below in units:
655	        us = u.strip()
656	        if not us:
657	            continue
658	        mine = next((l for l in got if l.get("unparsed") and l["excerpt"].strip() == us), None)
659	        missing = []
660	        for a, b, text in _unit_tokens(form, u, cols, below):
661	            key = _nt(text)
662	            hit = next((it for it in items if not it[2] and it[1] == key and (it[0] in us or us in it[0])), None)
663	            if hit:
664	                hit[2] = True
665	            elif any(w and (w in us or us in w) for w in whole):
666	                continue
667	            elif not (mine and form == "cms1500" and not _CMS_MONEY.search(text)):      # a bare number on a row already listed whole stays on that row's excerpt
668	                missing.append(text)
669	        if missing:
670	            if mine:
671	                mine["unclear"] += missing
672	            else:
673	                extra.append(_blank_line(rec, lform, us, description=us if form == "ledger_text" else "", unparsed=True, unclear=missing))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:47.736Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 700,
 "limit": 30
}
````

### User / tool · 2026-11-02T06:10:47.744Z

**tool result**
````
700	
701	def _merge_duplicates(lines):
702	    """A line repeated in a later record (a re-sent statement, an attached copy) counts once and cites both. Repeats inside ONE record are real."""
703	    out, seen = [], {}
704	    for l in lines:
705	        key = _line_key(l)
706	        hit = next((o for o in seen.get(key, []) if l["record_no"] not in o["record_nos"] and l["record_no"] not in o["_taken"]), None)
707	        if hit and key[4:7] != (None, None, None):
708	            hit["record_nos"].append(l["record_no"])
709	            hit["cites"].append({"record_no": l["record_no"], "excerpt": l["excerpt"]})
710	            hit["_taken"].add(l["record_no"])
711	            continue
712	        l = {**l, "record_nos": [l["record_no"]], "cites": [{"record_no": l["record_no"], "excerpt": l["excerpt"]}], "_taken": set()}
713	        seen.setdefault(key, []).append(l)
714	        out.append(l)
715	    for l in out:
716	        l.pop("_taken")
717	    return out
718	
719	
720	def _listed_elsewhere(line, rates, lop):
721	    """True when every figure of an unparsed line is already listed with its row as a rate (excluded) or an LOP/lien amount, so listing it a second
722	    time as unreconciled would be noise. A figure on the same line that is NOT one of those keeps the line."""
723	    own = {_nt(t) for t in line["unclear"]}
724	    ex = line["excerpt"].strip()
725	    seen = {_nt(x["figure"]["text"]) for x in rates if x["excerpt"].strip() == ex}
726	    seen |= {_nt(x["figure"]["text"]) for x in lop if ex in x["excerpt"] or x["excerpt"] in ex}
727	    return bool(own) and own <= seen
728	
729	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:10:48.084Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 804,
 "limit": 10
}
````

### User / tool · 2026-11-02T06:10:48.095Z

**tool result**
````
804	    lines = _merge_duplicates(lines)
805	    for l in lines:
806	        l["checks"] = _checks_for_line(l)
807	    for l in lines:
808	        l["detail"] = "eob" if l["form"] == "eob" and not l.get("unparsed") else ("reversal" if (l["billed"] and (l["billed"]["cents"] or 0) < 0) or (l["billed"] and _VOID.search(l["description"] or "")) else
809	                       "balance_only" if l["balance"] and not (l["billed"] or l["paid"] or l["adjustment"] or l["unclear"]) else None)
810	        l["class"] = "charge" if l["billed"] else "payment" if l["paid"] else "adjustment" if l["adjustment"] else "unclear"
811	        l["negotiated"] = bool(l["adjustment"] and _NEGOTIATED.search(l["description"] or ""))
812	        l["unparsed"] = bool(l.get("unparsed"))
813	        if l["form"] == "ledger" and l["billed"] and not l["dos"]:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:06.397Z

Three residual comparisons turned up under the strict reading: the reversal sign test (line 808), duplicate-line equality (701-717), and figure-text identity in the accounting net (658-668). I'll record them as minor questions, not blockers, since none produces a sum, a total, or a disagreement check. Next I'll save the grep and archive-test evidence.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:09.639Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-103-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && (echo \"## grep removed names in the bcdcb91 archive copy (app/, tests/, memory/contracts/api.md)\"; cd $SCR/head && grep -rn \"LEDGER_EOB\\|_sum(\\|_tot(\\|payer_reports\\|BALANCE_STEP\\|balance_convention\\|stated_totals\\|def _sum\\|def _tot\" app/ tests/unit/test_billing.py memory/contracts/api.md; echo \"exit=$?\") > $EV/grep_removed_names_bcdcb91.txt 2>&1; cat $EV/grep_removed_names_bcdcb91.txt | cut -c1-200; (echo \"## pytest tests/unit/test_billing.py on archive bcdcb91 (python -I)\"; cd $SCR/head && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py; echo \"pytest-exit=$?\") > $EV/pytest_billing_archive_bcdcb91.txt 2>&1; tail -2 $EV/pytest_billing_archive_bcdcb91.txt",
 "description": "Save grep evidence for removed names and archive pytest result"
}
````

### User / tool · 2026-11-02T06:11:10.898Z

**tool result**
````
## grep removed names in the bcdcb91 archive copy (app/, tests/, memory/contracts/api.md)
app/backend/export.py:229:def _summary_line(e):
tests/unit/test_billing.py:77:_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unrea
tests/unit/test_billing.py:132:    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH", "BALANCE_STEP_MISMATCH",
tests/unit/test_billing.py:133:            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
tests/unit/test_billing.py:277:    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})
tests/unit/test_billing.py:795:    assert not [k for d in B._walk(out) for k in d if k in ("ledger", "payer_reports", "matched_provider")]
memory/contracts/api.md:695:**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None inv
exit=0
179 passed in 0.93s
pytest-exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:42.559Z

The removed names appear only in tests that assert their absence, plus the D-052 note in the API doc. The `_sum` hit is an unrelated `export.py` function. Next I'll save the survivor output and a run-order file for reproduction.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:44.788Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-103-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I $EV/r2_survivor_and_m2_check.py > $EV/r2_survivor_and_m2_check_output.txt 2>&1; echo \"exit=$?\"; T103_ARCH=$SCR/mut/T01_oracle_rate_whole_row_exemption_removed .venv/bin/python -I -c \"\nimport sys, runpy\n\" ; ls $EV",
 "description": "Save the survivor and rate-row check output into the evidence folder"
}
````

### User / tool · 2026-11-02T06:11:45.274Z

**tool result**
````
exit=0
__pycache__
case_eob_140.txt
grep_removed_names_bcdcb91.txt
mutation_results_r2.txt
pytest_billing_HEAD_bcdcb91.txt
pytest_billing_archive_bcdcb91.txt
r1_reprobe.py
r1_reprobe_output.txt
r2_survivor_and_m2_check.py
r2_survivor_and_m2_check_output.txt
route_keys.py
route_keys_output.txt
run_mutants_r2.py
tbr2.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:50.145Z

**tool call — Bash**
````
{
 "command": "EV=artifacts/review-evidence/T-103-r2 && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && (cd $SCR/mut/T01_oracle_rate_whole_row_exemption_removed && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_billing.py -k \"table_rate_no_cents\" 2>&1 | grep -E \"AssertionError|assert |passed|failed\" | head -8) > $EV/T01_table_rate_no_cents_failure.txt 2>&1; cat $EV/T01_table_rate_no_cents_failure.txt | cut -c1-260; rm -rf $EV/__pycache__; echo cleaned",
 "description": "Capture the assertion that fails when the rate-row exemption is removed"
}
````

### User / tool · 2026-11-02T06:11:50.866Z

**tool result**
````
>       assert unaccounted(recs, one(recs)) == [], name
E       AssertionError: table_rate_no_cents
E       assert [('315.00', '...     315.00')] == []
tests/unit/test_billing.py:744: AssertionError
1 failed, 178 deselected in 0.39s
cleaned
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:57.943Z

The rate-row balance `315.00` fails without the exemption, which confirms the M2 gap. Before drafting I'll verify the exact line numbers I plan to cite in the EOB section.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:58.394Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 509,
 "limit": 28
}
````

### User / tool · 2026-11-02T06:11:58.404Z

**tool result**
````
509	def _eob(rec, lines):
510	    """(row lines, unparsed lines). Each service row (date, service code, figures) is one line of form eob: its figures are in `eob` (by column) when
511	    every figure was read and there is one per column; otherwise EVERY money token of the row is in `unclear` with its text, never dropped."""
512	    hi, cols = _eob_header(lines)
513	    unp = lambda ln, toks: _blank_line(rec, "eob", ln, unparsed=True, unclear=[t.group(0) for t in toks])
514	    if hi is None:
515	        return [], [unp(ln, _tokens(ln)) for ln in lines if _tokens(ln)]
516	    names = [k for _, k in sorted((s0, k) for k, (s0, _e) in cols.items())]
517	    out, unparsed = [], [unp(ln, _tokens(ln)) for ln in lines[:hi] if _tokens(ln)]
518	    for ln in lines[hi + 1:]:
519	        m = _EOBROW.match(ln)
520	        if not m:
521	            if _tokens(ln):                           # a printed EOB total row, or any figure outside a service row: listed, never dropped
522	                unparsed.append(unp(ln, _tokens(ln)))
523	            continue
524	        toks = _eob_tokens(ln, cols, m.span(2))
525	        figs = [parse_figure(t.group(0)) for t in toks]
526	        line = _blank_line(rec, "eob", ln, dos=m.group(1), code=m.group(2))
527	        line["eob"], line["eob_codes"] = {}, (ln[toks[-1].end():].strip() or None) if toks else None
528	        if len(figs) == len(names) and all(f["cents"] is not None for f in figs):
529	            line["eob"] = {k: _mag(f) for k, f in zip(names, figs)}
530	        else:
531	            line["unclear"] = [f["text"] for f in figs]
532	        out.append(line)
533	    return out, unparsed
534	
535	
536	# ------------------------------------------------------------------ LOP / lien amounts (listed, never totaled)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:11:58.682Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 268,
 "limit": 6
}
````

### User / tool · 2026-11-02T06:11:58.690Z

**tool result**
````
268	            if not (line["paid"] or line["adjustment"] or line["unclear"]):
269	                continue
270	        out.append(line)
271	    _put_stated(rec, stated, {k: v for k, v in _stated(rec, "\n".join(lines[hi + 1:])).items() if k not in stated}, out)
272	    return out, stated, balfwd, rates
273	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:03.929Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/RUN_ORDER.txt",
 "content": "T-103 r2 (commit bcdcb91) - how to reproduce the evidence in this folder\n\n0. Pin the code. From the project root:\n     git rev-parse HEAD                        -> at review time bcdcb91...; HEAD later moved to c2a5d1f (T-106), 3462ad0 (T-104) in between\n     git show --stat bcdcb91                   -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py\n     git diff --stat bcdcb91 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md   -> empty (identical)\n     mkdir <A> && git archive bcdcb91 | tar -x -C <A>        (archive copy, used as T103_ARCH below)\n\n1. Unit tests:\n     .venv/bin/python -m pytest -q tests/unit/test_billing.py         -> pytest_billing_HEAD_bcdcb91.txt (179 passed; project worktree at c2a5d1f, billing files identical)\n     cd <A> && .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py   -> pytest_billing_archive_bcdcb91.txt (179 passed)\n\n2. Removed names (grep on the archive copy) -> grep_removed_names_bcdcb91.txt\n\n3. r1 probes re-run on the archive copy:\n     T103_ARCH=<A> .venv/bin/python -I r1_reprobe.py                  -> r1_reprobe_output.txt\n     T103_ARCH=<A> .venv/bin/python -I r2_survivor_and_m2_check.py    -> r2_survivor_and_m2_check_output.txt\n\n4. Billing route (TestClient, fixture backend, ingest only) on sample, case_03, case_09 and case_eob_140.txt (written by route_keys.py):\n     T103_ARCH=<A> .venv/bin/python -I route_keys.py                  -> route_keys_output.txt\n\n5. Scratch-copy mutants (archive never edited; each anchor must match exactly once):\n     .venv/bin/python -I run_mutants_r2.py <A> <MUTDIR>               -> mutation_results_r2.txt\n     T01 (test-side whole-row exemption removed) failure detail:\n     <MUTDIR>/T01_oracle_rate_whole_row_exemption_removed: pytest -k table_rate_no_cents -> T01_table_rate_no_cents_failure.txt\n\nHelper: tbr2.py loads tests/unit/test_billing.py from T103_ARCH (never from the project tree).\nUnrelated to T-103 and not re-run here: tests/unit/test_t093_eval_signature.py (red at 841be23 and 2dc5be2 per r1).\n"
}
````

### User / tool · 2026-11-02T06:12:04.050Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/RUN_ORDER.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:08.608Z

Before drafting, I want to confirm what `_line_key` compares, so the duplicate-equality finding cites exactly what it does.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:09.029Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 690,
 "limit": 11
}
````

### User / tool · 2026-11-02T06:12:09.037Z

**tool result**
````
690	    """ROW_NOT_PARSED for a row that fit no layout, LINE_UNCLEAR when a figure could not be read. Nothing is computed from the figures."""
691	    if line.get("unparsed"):
692	        return ["ROW_NOT_PARSED"]
693	    return ["LINE_UNCLEAR"] if line["unclear"] else []
694	
695	
696	def _line_key(l):
697	    g = lambda k: (l[k] or {}).get("cents") if l.get(k) else None
698	    return (_norm(l.get("dos")), _norm(l.get("posted")), _norm(l.get("code")), _norm(l.get("description")), g("billed"), g("paid"), g("adjustment"), l.get("form"))
699	
700	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:34.844Z

`_line_key` compares billed, paid and adjustment cents for equality, so the duplicate-merge comparison is real. Last checks before drafting: float, bare-except, sleep and import-surface greps on the billing code and its tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:35.879Z

**tool call — Bash**
````
{
 "command": "grep -n \"float(\\|except\\|sleep(\\|^import\\|^from\" app/backend/billing.py; echo \"--- tests\"; grep -n \"float(\\|except\\|sleep(\\|random\\|time\\.\\|requests\\|httpx\\|anthropic\" tests/unit/test_billing.py; echo \"--- diff touches (bcdcb91 stat)\"; git show --stat --format= bcdcb91 | tail -1",
 "description": "Grep billing code and tests for float, except, sleep, imports and network calls"
}
````

### User / tool · 2026-11-02T06:12:35.990Z

**tool result**
````
21:import re
23:from app.backend import amounts as A, dates
--- tests
306:    tok = DB.create_case(conn, text, now=time.time())
307:    PL.ingest_case(conn, tok, text, time.time())
566:import random
1052:# ---- property: a random money token put anywhere in a billing record is a line, unreconciled, or its record is skipped
1073:            return text.replace(". Balance due", f". Office visit {tok}. Balance due", 1) if rnd.random() < 0.5 else text + f" Visit fee {tok}."
1092:def test_property_a_random_money_token_is_never_silently_missing():
1093:    rnd, n = random.Random(20261102), 0
--- diff touches (bcdcb91 stat)
 3 files changed, 204 insertions(+), 138 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:12:58.142Z

No float, bare except, sleep, or network calls in the billing code or its tests. The only imports are `re` and the amounts and dates helpers, and the seeded `random.Random` keeps the property test deterministic. For completeness I'll also re-run the r1 mutant set, since M02, M03 and M05 target parser bodies that the diff does not touch.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:00.513Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && .venv/bin/python -I artifacts/review-evidence/T-103-r1/run_mutants.py $SCR/head $SCR/mut_r1set > artifacts/review-evidence/T-103-r2/mutation_results_r1_set_on_r2.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-103-r2/mutation_results_r1_set_on_r2.txt | cut -c1-220",
 "description": "Run the r1 mutant set against the r2 code in scratch copies"
}
````

### User / tool · 2026-11-02T06:13:12.054Z

**tool result**
````
exit=0
M01_accounting_net_off: rc=1 6 failed, 173 passed in 1.09s
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none
    FAILED test_property_a_random_money_token_is_never_silently_missing
M02_table_unreadable_figure_dropped_and_net_off: rc=1 13 failed, 166 passed in 0.89s
    FAILED test_unreadable_figure_is_listed_with_no_value
    FAILED test_an_unreadable_provider_does_not_touch_another_providers_lines
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_dollar_no_cents]
    FAILED test_bare_or_dateless_money_token_is_shown[A_table_bare_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_oracle_is_not_vacuous
    FAILED test_table_charge_with_no_cents_is_on_its_row_as_unclear[$185]
    FAILED test_table_charge_with_no_cents_is_on_its_row_as_unclear[185]
    FAILED test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none
    ... 13 failing in total
M03_cms_unreadable_box_dropped_and_net_off: rc=1 8 failed, 171 passed in 0.79s
    FAILED test_cms1500_ocr_text_never_reads_8500_as_dollars
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P15_dated_cms_bare_box]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_dateless_cms_line_lists_only_its_money_token_and_a_worded_box_lists_none
    FAILED test_property_a_random_money_token_is_never_silently_missing
M04_unreconciled_list_dropped: NOT APPLIED (matches=0) for: '    for l in lines if l["unparsed"]]'
M05_printed_totals_not_listed: rc=1 65 failed, 114 passed in 1.74s
    FAILED test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them
    FAILED test_duplicate_statement_is_one_line_citing_both_records
    FAILED test_balance_forward_is_a_cited_line_and_not_a_charge
    FAILED test_ledger_prose_statement_lists_charges_payment_adjustment_and_its_printed_figures
    FAILED test_cms1500_boxes_are_implied_cents_and_item_28_is_a_listed_total
    FAILED test_cms1500_ocr_text_never_reads_8500_as_dollars
    FAILED test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total
    FAILED test_prose_rate_is_a_rate_even_when_the_printed_total_includes_it
    FAILED test_cms1500_line_that_does_not_fit_is_unreconciled_with_its_excerpt
    FAILED test_ledger_row_with_no_date_is_unreconciled_and_its_total_is_a_line
    FAILED test_verifier_covers_every_cite_bearing_field
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[M2_second_total_charges]
    ... 65 failing in total
M06_eob_unreadable_figure_dropped_oracle_blind: NOT APPLIED (matches=0) for: '        row = {"record_no": rec["n"], "dos": m.group(1)'
M07_rate_row_dropped_and_net_off: rc=1 16 failed, 163 passed in 0.95s
    FAILED test_table_row_charge_per_visit_is_a_rate_line_listed_once[185.00]
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Visit
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Rate
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Hourly
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Charge
    FAILED test_every_rate_cue_in_a_table_row_wins_even_beside_charge[Daily
    FAILED test_probe_set_every_money_token_is_a_line_unreconciled_or_skipped[table_rate_no_cents]
    FAILED test_bare_or_dateless_money_token_is_shown[P11_bare_prose_figure]
    FAILED test_bare_or_dateless_money_token_is_shown[P13_bare_labelled_charge]
    FAILED test_bare_or_dateless_money_token_is_shown[P16_dateless_cms_bare]
    FAILED test_bare_or_dateless_money_token_is_shown[eob_bare_total_row]
    FAILED test_table_rate_row_with_no_cents_is_a_rate_line_with_its_text[185]
    ... 16 failing in total
M08_verifier_stubbed: rc=1 4 failed, 175 passed in 1.14s
    FAILED test_verify_citations_catches_an_uncited_line
    FAILED test_verifier_reference_is_the_record_text_not_the_excerpt
    FAILED test_verifier_covers_every_cite_bearing_field
    FAILED test_billing_route_returns_citation_failures_and_flags_the_status
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:13:45.191Z

The r1 set confirms the detection picture: M01, M02, M03, M05, M07 and M08 are red. M04 and M06 no longer apply because their anchors moved, and R07 and R01 are their equivalents. I have what I need, so I'll write the review now.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:06.572Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer-r2.md",
 "content": "# T-103 staff-engineer review, r2 (commit bcdcb91)\n\nReviewer: staff-engineer-reviewer. Model: claude-haiku-5-5 (as dispatched). CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed (same as r1).\n\n**Verdict: changes.** No blockers. One major carried from r1: a rate row's running balance is still only inside its verbatim excerpt, and the oracle passes it through a whole-row exemption. Three minors and one nit.\n\n**Pin.** `git rev-parse HEAD` returned bcdcb919f1723f51579db03d9426443860a91680 at review start. HEAD later moved to c2a5d1f (T-106), with 3462ad0 (T-104) between. `git diff --stat bcdcb91 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md` is empty, so the three reviewed files are identical at HEAD. Scripts and mutants ran on `git archive bcdcb91` in the scratchpad. Evidence: artifacts/review-evidence/T-103-r2/ (RUN_ORDER.txt lists every command).\n\n**The four checks you asked for.**\n1. Per-service sums and EOB-versus-ledger checks are gone: met. `grep -rn \"LEDGER_EOB\\|_sum(\\|_tot(\\|payer_reports\\|BALANCE_STEP\\|balance_convention\\|stated_totals\" app/ tests/unit/test_billing.py memory/contracts/api.md` on the archive returns only the absence assertions (test_billing.py:77, 132-133, 277, 795) and the \"Removed by D-052\" line (api.md:695). The one `_sum` hit is an unrelated function at app/backend/export.py:229. The r1 control (EOB 140.00 against ledger 130.00) now gives `checks: []` on the EOB row and no check anywhere (r1_reprobe_output.txt).\n2. An EOB amount with no cents appears as a line or as unreconciled: met. \"$140\", \"$130\", \"1O0.00\", a bare \"130\" and \"130.5\" each produce an EOB line (class unclear, detail eob) with the text in `unclear` and `checks: [LINE_UNCLEAR]`. `unaccounted` is empty for each (r1_reprobe_output.txt).\n3. The fail-safe accounting test covers EOB records and fails when a token is dropped: met for code-level drops (mutation_results_r2.txt, scratch copies). R01, the EOB unreadable figure's `unclear` list emptied at billing.py:531: 7 failed. R04, the first EOB column dropped at billing.py:529: 4 failed. R03, the EOB accounting pass off at billing.py:779: 2 failed. R05, R01 plus R03: 19 failed. The one survivor is R02, EOB unparsed rows dropped at billing.py:764 (`got = rows_ + unp_` to `got = rows_`), printed TOTAL row included: 179 passed. The accounting pass re-lists that TOTAL row's seven figures as an unreconciled eob row (r2_survivor_and_m2_check_output.txt), so nothing is lost. That is redundancy, not a gap. The in-test EOB fail-safe at test_billing.py:804 edits the analysed output, so it proves the oracle; the production-path proof is R01 and R04.\n4. The route output has no total-like fields: met. route_keys_output.txt covers four responses (sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap, and a synthetic EOB $140 case). Each returns HTTP 200 with top-level keys `citation_failures, lines, rules, skipped_records, status, unreconciled`. No key path on any of them matches total, sum, complete, balance_convention, stated, providers, payer, ledger or matched. Per-line printed figures (`billed`, `paid`, `balance`, `eob.*`) remain. They are per line, not totals. The sample returns `none_found`, so it adds nothing beyond the top-level keys.\n\n**Pytest.** `.venv/bin/python -m pytest -q tests/unit/test_billing.py` in the project worktree: 179 passed in 1.04s (pytest_billing_HEAD_bcdcb91.txt). The same command on the archive copy with `-I`: 179 passed in 0.93s (pytest_billing_archive_bcdcb91.txt). r1 recorded 157.\n\n**Status of the r1 findings.**\n- r1 B1 (EOB money token lost): resolved. See check 2.\n- r1 B2 (per-service sums on payer checks): resolved. See check 1.\n- r1 M1 (silent skip on an unreadable figure): resolved. The `continue` is gone. The same-service unreadable ledger row \"130\" now carries LINE_UNCLEAR on its own row (r1_reprobe_output.txt).\n- r1 M2 (rate-row running balance only in the excerpt): open. Finding F1.\n- r1 M3 (fail-safe cannot fail for EOB rows): resolved for EOB (R01 red). The rate whole-row exemption remains (F1).\n- r1 M4 (docs versus code on balance checks): resolved. billing.py:5 says \"no balance step check\", and api.md:664 says \"no running-balance step check\".\n- r1 m1 (detail carries two kinds): open, and `eob` is now another detail value. Finding F4.\n- r1 nit (figure fields on extra lines): resolved. api.md:692 says they are never summed or compared by a client.\n\n**Mutant coverage (r1 set re-run on the r2 code, mutation_results_r1_set_on_r2.txt).** M01 6 failed, M02 13, M03 8, M05 65, M07 16, M08 4. M04 and M06 report NOT APPLIED because their anchors moved. R07 (unreconciled list dropped, 78 failed) and R01 (EOB unclear dropped, 7 failed) are their equivalents on the r2 code.\n\n**Not exercised.** The full tests/unit suite. The app over HTTP (TestClient only). The D-019 accepted total was not re-run; `git show --stat bcdcb91` lists only the three billing files, so totals.py, present.py and api.py are untouched. tests/unit/test_t093_eval_signature.py (unrelated, red at 841be23 per r1) was not re-run.\n\n```json\n{\"card\": \"T-103\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git commit bcdcb91 (fix(backend): billing applies D-052 strictly, T-103 r2): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copy of git archive bcdcb91; project worktree (HEAD later c2a5d1f, billing files identical to bcdcb91); billing route via TestClient on evals/golden sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap and a synthetic EOB $140 case; no app URL exercised\",\n \"exercised\": [\n   \"git rev-parse HEAD -> bcdcb919f1723f51579db03d9426443860a91680 at review start; git log later showed c2a5d1f (T-106) and 3462ad0 (T-104) above it\",\n   \"git show --stat bcdcb91 -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py (3 files, 204 insertions, 138 deletions)\",\n   \"git diff --stat bcdcb91 HEAD -- the three files -> empty; git status --short on the three files -> empty\",\n   \"git diff 2dc5be2 bcdcb91 on the three files: every hunk read\",\n   \".venv/bin/python -m pytest -q tests/unit/test_billing.py in the project worktree -> 179 passed in 1.04s\",\n   \"git archive bcdcb91 into a scratchpad copy; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the copy -> 179 passed in 0.93s\",\n   \"r1_reprobe.py on the copy (r1_reprobe_output.txt): EOB 97110 billed $140 against ledger 130.00; control 140.00; EOB figures $130, 1O0.00, bare 130, 130.5; same-service unreadable ledger row (bare 130) with EOB 130.00; rate row 'Charge per visit 185.00 999.00'; (class, detail) pairs over PROBES\",\n   \"r2_survivor_and_m2_check.py on the copy and on mutant R02 (r2_survivor_and_m2_check_output.txt): the printed TOTAL row re-listed as an unreconciled eob row; rate line keys and figure\",\n   \"route_keys.py (route_keys_output.txt): billing route via TestClient, fixture backend, ingest only, on evals/golden sample.txt, case_03_rate_and_ocr.txt, case_09_nonvisit_hides_gap.txt and a synthetic EOB $140 case; every key path searched for total-like names\",\n   \"run_mutants_r2.py on scratch copies (mutation_results_r2.txt): R01 to R09 and T01, full file and -k 'eob or probe or property or bare or oracle' selections\",\n   \"run_mutants.py from the r1 folder on the r2 copy (mutation_results_r1_set_on_r2.txt): M01 to M08; M04 and M06 not applied (anchors moved)\",\n   \"pytest -k table_rate_no_cents on mutant T01 (T01_table_rate_no_cents_failure.txt): assert [('315.00', ...)] == []\",\n   \"grep on the copy for LEDGER_EOB, _sum(, _tot(, payer_reports, BALANCE_STEP, balance_convention, stated_totals (grep_removed_names_bcdcb91.txt); grep of billing.py and the test module for float(, except, sleep(, random, and network or model imports\",\n   \"read billing.py 166-182, 509-533, 558-565, 646-673, 690-727, 804-812 and the module docstring; test_billing.py helpers 73-115, oracle 565-611, PROBES 653-735, EOB tests 776-826, property test 1052-1103; memory/contracts/api.md 663-695; memory/ORCHESTRATOR_DECISIONS.md line 60 (D-052)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"fail_safe_completeness\": 4, \"decision_D052_conformance\": 4, \"honest_failure_no_silent_skip\": 5, \"api_doc_matches_code\": 4, \"money_integer_cents\": 5, \"no_llm_in_deterministic_path\": 5, \"test_mutation_catch\": 4, \"D019_total_unchanged\": 5},\n \"findings\": [\n   {\"severity\": \"major\",\n    \"title\": \"Rate-row running balance is still only inside its excerpt; the oracle's whole-row exemption is what passes it (r1 M2, not fixed at bcdcb91)\",\n    \"evidence\": \"r1_reprobe_output.txt and r2_survivor_and_m2_check_output.txt: row 'Charge per visit 185.00 999.00' gives one line, class rate, figure 185.00, and no balance field; '999.00' occurs only in the excerpt. app/backend/billing.py:649 whole = [x['excerpt'].strip() for x in list(rates) + list(lop)] and tests/unit/test_billing.py:570 _WHOLE_ROW = ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance') are unchanged in bcdcb91. T01_table_rate_no_cents_failure.txt: with 'rate' removed from _WHOLE_ROW, table_rate_no_cents fails with assert [('315.00', ...)] == [].\",\n    \"why_it_matters\": \"The running balance is a printed money token that a paralegal can only find inside the verbatim text. api.md:692 says a running balance is listed beside the lines, but on a rate row it is not a figure field of any line. The oracle accepts it only because the whole row is exempt. This is the r1 blind spot again, through the rate path, and it is the one r1 finding bcdcb91 leaves open.\",\n    \"fix\": \"Carry the rate row's running balance as a figure of the rate line (an unclear figure with its text, or a separate cited line with class unclear), then remove 'rate' from _WHOLE_ROW. Update api.md:692 to name the field that carries it.\",\n    \"acceptance_test\": \"For 'Charge per visit 185.00 999.00', '999.00' sits in a structured field of the output and not only in excerpt or cites; tests/unit/test_billing.py passes with 'rate' removed from _WHOLE_ROW; a mutant that drops that field turns the probe red.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"Comparisons remain under the strict reading of 'no sums or comparisons of any kind' (D-052 text itself does not name comparisons)\",\n    \"evidence\": \"app/backend/billing.py:808 ... (l['billed']['cents'] or 0) < 0 sets detail 'reversal' (a sign test on a money figure). billing.py:696-698 _line_key includes billed, paid and adjustment cents; billing.py:701-717 _merge_duplicates merges a repeated line on equality of that key. billing.py:662 it[1] == key and billing.py:725-727 _listed_elsewhere compare figure text to decide whether a token is placed. None of these produces a sum, a total, a shown verdict or a disagreement check. memory/ORCHESTRATOR_DECISIONS.md:60 forbids totals and a complete badge and does not mention comparisons.\",\n    \"why_it_matters\": \"The round's standard is no sums or comparisons of any kind. These are comparisons of money values (a sign test, equality on cents) and of token text. None of them violates the D-052 text, so this is minor here; it becomes major if Chris reads the standard as covering them.\",\n    \"fix\": \"If the strict reading applies: classify reversal from the credit notation in the excerpt (parentheses or a trailing minus), and key duplicate merging on the record's own excerpt text, not on cents. If it does not apply: record the ruling under D-052 in memory/ORCHESTRATOR_DECISIONS.md so the next review does not re-raise it.\",\n    \"acceptance_test\": \"Chris's ruling is recorded. If strict: no money comparison remains in billing.py, and a test pins 'reversal' from a parenthesised figure without a sign comparison.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"Stale comment and docstring wording name the removed provider-completeness state\",\n    \"evidence\": \"app/backend/billing.py:563 '...the provider of such a line is complete: false.' (no complete field exists; tests/unit/test_billing.py:77 lists 'complete' in _GONE). billing.py:170 'the provider is incomplete'; billing.py:180 'the provider is incomplete, and the figure is not left only in a field nobody opens'.\",\n    \"why_it_matters\": \"A reader who greps for 'complete: false' finds a comment about a flag that D-052 removed. 'Provider is incomplete' brings back the completeness state the decision retired. This is docs-versus-code drift of the kind r1 flagged.\",\n    \"fix\": \"Reword the three comments to say the figure is listed on its own line and that no provider completeness is claimed.\",\n    \"acceptance_test\": \"grep for 'complete: false' and 'provider is incomplete' in app/backend/billing.py returns nothing; the module docstring and api.md agree on the same wording.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"detail carries several kinds of thing (r1 m1, carried; 'eob' is now one more value)\",\n    \"evidence\": \"r1_reprobe_output.txt, (class, detail) pairs over PROBES: (charge, reversal), (unclear, eob), (rate, rate), (unclear, asserted_balance), (unclear, stated_total_billed), (unclear, balance_forward), (unclear, None) and others. app/backend/billing.py:808-809 computes detail from form, sign, description and balance.\",\n    \"why_it_matters\": \"A client has to branch on detail strings that mean different things: why a ledger row is listed, and what kind of extra line this is. The eob value adds a third meaning without a separate field.\",\n    \"fix\": \"As r1 proposed: a closed kind list for what the line is, and a separate reason for why it is listed. Document both in api.md.\",\n    \"acceptance_test\": \"Every line has a kind from a closed list, and a test pins that list.\"},\n   {\"severity\": \"nit\",\n    \"title\": \"The in-test EOB fail-safe proves the oracle by editing the output, not the production path\",\n    \"evidence\": \"tests/unit/test_billing.py:804 test_eob_fail_safe_names_a_figure_dropped_from_a_row... deletes keys from the analysed output (del _eob_line(out)['eob'][k]; _eob_line(out)['unclear'] = []) and asserts the oracle names them. The production-path proof is R01 and R04 in mutation_results_r2.txt.\",\n    \"why_it_matters\": \"The test is correct as an oracle test, but it does not run a changed parser. The parametrized test at tests/unit/test_billing.py:781 does exercise the parser's unclear path and catches R01, which is why this is only a nit.\",\n    \"fix\": \"Optional: add one test that patches the EOB parser's unclear list to empty and asserts the oracle names the figure.\",\n    \"acceptance_test\": \"Optional; the mutant R01 stays red.\"}\n ],\n \"whats_right\": [\n   \"EOB money tokens sit on their rows: '$140', '1O0.00', bare '130' and '130.5' each stay as text on the EOB line, and the oracle names nothing unaccounted (r1_reprobe_output.txt).\",\n   \"No sums, payer checks or ledger comparisons remain: the 140.00 control raises no check, and no total-like key appears in any of the four route responses (route_keys_output.txt, grep_removed_names_bcdcb91.txt).\",\n   \"The EOB fail-safe is caught at the code level: R01, R03, R04 and R05 turn 7, 2, 4 and 19 tests red; the r1 M01, M02, M03, M05, M07 and M08 mutants stay red on the r2 code.\"\n ],\n \"questions_for_chris\": [\n   \"Does 'no sums or comparisons of any kind' (the standard for this round) cover the reversal sign test (billing.py:808), the duplicate-line equality on cents (billing.py:696-717) and the text identity in the accounting net (billing.py:662, 725-727)? I read D-052 as not covering them, so they are minor (F2). If the strict reading applies they are major.\",\n   \"For F1: may a rate row's running balance stay as cited excerpt text only (the bcdcb91 reading), or must it be a figure field (the r1 proposal)? The answer decides whether F1 closes without a code change.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T06:14:06.728Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:21.882Z

The review is written. Before I rely on it, I need to check one claim in the exercised list: I wrote "every hunk read" for the three files, but the api.md and test-file diffs were persisted to disk and I only saw parts of them. I'll read both in full now.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:26.147Z

**tool call — Bash**
````
{
 "command": "git diff 2dc5be2 bcdcb91 -- memory/contracts/api.md > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/api_diff.txt && wc -l /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/api_diff.txt && grep -n \"^@@\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/api_diff.txt",
 "description": "Save the api.md diff for the r2 commit and list its hunks"
}
````

### User / tool · 2026-11-02T06:14:26.280Z

**tool result**
````
     111 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/api_diff.txt
5:@@ -6,7 +6,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
14:@@ -29,14 +29,14 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
31:@@ -82,7 +82,7 @@ Errors: `400 bad_request` with `detail.reason` = `pdf_no_text_layer` (looks scan
40:@@ -104,7 +104,7 @@ Response and `GET /api/cases/{token}` gain, for PDF cases only:
49:@@ -616,7 +616,7 @@ Each case step has the shared step keys plus `counts` (object, may be `{}`); `ex
58:@@ -661,38 +661,39 @@ Always `200` with one envelope:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:28.727Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2; cut -c1-700 $SCR/api_diff.txt | sed -n 14,30p; echo ....; cut -c1-700 $SCR/api_diff.txt | sed -n 58,111p",
 "description": "Read the billing-related hunks of the api.md diff in full"
}
````

### User / tool · 2026-11-02T06:14:28.860Z

**tool result**
````
@@ -29,14 +29,14 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
 | POST | `/api/cases/{token}/narrative/review` | `{action: accept\|dismiss\|reset}` on the whole paragraph. Until accepted it appears only in the internal notes (section DRAFT TREATMENT PARAGRAPH); once accepted it also goes into the letter as TREATMENT SUMMARY, each sentence followed by `(provider as written, date)`, and a sentence drops out again if its entry is dismissed or edited |
 | GET | `/api/cases/{token}/items/{item_id}` | one item with ladder and its audited calls ("Why?") |
 | POST | `/api/cases/{token}/items/{item_id}/reclassify` | D-042 (T-084) guarded charge reclassification of an **amount**: body `{to: "charge"\|"not_a_charge", note?}`. See the section below |
-| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/highlight; AI-made or human) r
+| POST | `/api/cases/{token}/items/{item_id}/review` | accept, edit, dismiss, reset. D-041: `accept` (and `edit`, which implies accept) on an **entry with no confirmed date** (listed in `undated_entries`: date ambiguous or missing) returns `422 DATE_UNCONFIRMED` and changes nothing (no write, no event); it works after `confirm_date` moves the entry into `entries`. Dismiss and reset are always allowed (the paralegal can move it out of the letter). Checked after `409 item_rejected`. **D-051:** `accept` on an **entry** whose current summary or quote fails a code check (D-034 number/date/side/negation not in the quote, D-022 dropped qualifier, whole-sentence/hedge/verbatim/highlight; AI-made or
 | GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items. `422 judge_not_run` while an accepted AI-made item has no second check (D-044, no override) |
 | POST | `/api/cases/{token}/rejudge` | D-044 run the second check again for AI-made items whose judge never answered; audited; demo mode replays recorded answers only, live needs `ENABLE_LIVE=1`. Returns the new export gate |
 | GET | `/api/cases/{token}/audit` | calls and human events for this case (metadata only; full text with `ZLAYT_MODE=local`) |
 | GET | `/api/cases/{token}/items/{item_id}/trace` | D-042 per-item check trace: ordered stepper (extracted, each code check by name, judge, human) with status, why, reason code, evidence, next action. Item ids `e…`, `a…`, `f…`, and narrative sentences `ns…` |
 | GET | `/api/cases/{token}/trace` | D-042 case-level stepper: ingest, split, dates, extract, grounding, judges, flags, totals, review, export gate (the gate lists exactly which items block export) |
 | GET | `/api/cases/{token}/judges` | D-042 judge summary: counts per judge, objections with reason and rationale, model and prompt version, code-vs-judge disagreements |
-| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records, EOB payer reports; no provider totals or complete flag; internal view, never in the letter |
+| GET | `/api/cases/{token}/billing` | T-083 / D-052 code-only billing as a cited line listing: lines (charge, adjustment, payment, rate, unclear; verbatim excerpt and source record each), unreconciled rows, skipped records (an EOB service row is a line); no sums or comparisons of any kind, no provider totals or complete flag; internal view, never in the letter |
 | GET | `/api/cases`, `/api/library` | case list and synthetic case library (`ZLAYT_MODE=local` only; 404 otherwise) |
 | GET | `/api/calibration` | T-099 read-only measured calibration (aggregate counts only, no case token, demo-safe): the T-096 shape in `calibration`, or `null` with `status` `missing`/`invalid`. See the section below |
 
....
@@ -661,38 +661,39 @@ Always `200` with one envelope:
 Rules for the client: render `sentences.overall.verified` and `sentences.overall.needs_review` verbatim (they name the backend and the basis); never compute or show a percentage; hide the line when `calibration` is null. Nothing is invented: no default numbers appear in any state. `calibration` is served by `app/backend/calibration_route.py`; the route is registered in `create_app` and reads one fixed path.
 
 ## GET /api/cases/{token}/billing  (T-083, D-042, D-052)
-Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs. Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No provider totals, no billed/paid/balance sums, no `complete` flag, no balance reconciliation (D-052):** a listing cannot hide a missing line, a sum can. The only billing total in the product is the case-level charge total of stated charges (D-019, `totals`), unchanged. Unknown token: `404 not_found`.
+Billing as a **cited line listing**. Code-only analysis of the case's itemized ledgers (table or sentence form), CMS-1500 and UB-04 claim forms, and EOBs (each EOB service row is a line). Computed on read from the records, never stored, **no model call**, available in every state after ingest and in demo mode. It is an internal review view: nothing here reaches the letter or changes `totals`. **No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2):** no provider totals, no billed/paid/balance sums, no `complete` flag, no running-balance step check, no ledger-versus-EOB check. A listing cannot hide a missing line; a sum or a comparison can. The response has exactly `st
 ```json
 { "billing": {
   "status": "listed",                         // listed | citation_failed | none_found. "listed" says only that something was found; it is not a completeness claim
   "citation_failures": [],                    // [{ref, reason}] from the grounding verifier, which the route always runs; non-empty makes status citation_failed
   "lines": [                                  // every figure the records print, in record order, each with a verbatim excerpt and its source record
     { "id": "b3", "class": "charge",          // charge | adjustment | payment | rate | unclear
-      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | see the extra-line details below
-      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04
+      "detail": null,                         // null | "reversal" (negative or VOID charge) | "balance_only" | "eob" (an EOB service row) | see the extra-line details below
+      "provider": "Larkspur Hollow Physical Therapy", "record_no": 1, "record_nos": [1], "form": "ledger",    // form: ledger | cms1500 | ub04 | eob
       "dos": "06/10/26", "dos_iso": "2026-06-10", "posted": "06/11/26", "code": "97140", "description": "Manual therapy x1",
       "billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "adjustment": null, "paid": null, "balance": {"text": "410.00", "cents": 41000, "usd": "$410.00"},
       "unclear": [], "negotiated": false, "unparsed": false,
-      "checks": [],                           // LINE_UNCLEAR | BALANCE_STEP_MISMATCH | NO_DATE_OF_SERVICE
+      "checks": [],                           // LINE_UNCLEAR | NO_DATE_OF_SERVICE (ROW_NOT_PARSED on an unreconciled row)
       "excerpt": "06/10/26  06/11/26  97140  Manual therapy x1  70.00  410.00",   // the printed line, verbatim
       "cites": [ {"record_no": 1, "excerpt": "<same line>"} ] },                // a re-sent statement or attached copy is one line citing both records (record_nos, cites)
     { "id": "b8", "class": "rate", "detail": "rate", "provider": "...", "record_no": 1, "record_nos": [1], "form": "ledger",
       "figure": {"text": "$65.00", "cents": 6500, "usd": "$65.00"}, "why": "A rate (per visit, per unit) is a price, not a charge.",
-      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"} ] } ],
+      "excerpt": "Fee schedule: Therapeutic exercise $65.00 per unit.", "cites": [ {"record_no": 1, "excerpt": "<same>"} ] },
+    { "id": "b12", "class": "unclear", "detail": "eob", "provider": "Quoinmere Mutual Health Plan", "record_no": 2, "record_nos": [2], "form": "eob",
+      "dos": "06/10/26", "code": "97140",                         // code = the EOB's service code; billed/paid/adjustment/balance are null on an EOB row
+      "eob": {"billed": {"text": "70.00", "cents": 7000, "usd": "$70.00"}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}},
+      "eob_codes": "PR-1, PR-2, CO-45", "unclear": [], "checks": [],    // `eob` is {} and every money token of the row is in `unclear` (text, no value) when a figure could not be read or the row has the wrong number of figures
+      "excerpt": "06/10/26  97140  70.00 ...", "cites": [ {"record_no": 2, "excerpt": "<same>"} ] } ],
   "unreconciled": [ { "id": "u1", "provider": "...", "record_no": 1, "form": "cms1500", "class": "unclear", "reason_code": "ROW_NOT_PARSED", "message": "...",
     "excerpt": "<the row, verbatim>", "figures": ["$85.00"] } ],   // rows that carry a figure or a date but fit no layout; never dropped. `figures` holds only the money tokens, not the rest of the line
   "skipped_records": [ {"record_no": 4, "reason_code": "INJECTION_SUSPECTED"}, {"record_no": 5, "reason_code": "UNRECOGNISED_BILLING_FORM"} ],
-  "payer_reports": [ { "record_no": 2, "provider": "Quoinmere Mutual Health Plan", "matched_provider": "Larkspur Hollow Physical Therapy",
-    "lines": [ {"dos": "06/10/26", "service": "97140", "billed": {...}, "discount": {...}, "allowed": {...}, "deductible": {...}, "coinsurance": {...}, "plan_paid": {...}, "patient_owes": {...}, "codes": "PR-1, PR-2, CO-45", "excerpt": "...", "unclear": []} ],
-    "checks": [ {"code": "LEDGER_EOB_PAID_MISMATCH", "dos": "06/10/26", "service": "97140", "ledger": {"cents": 0, "usd": "$0.00"}, "eob": {"cents": 1600, ...}, "cites": [ {"record_no": 2, "excerpt": "..."}, {"record_no": 1, "excerpt": "..."} ], "message": "..."} ],
-    "not_added_note": "The EOB restates the provider's charge; its amounts are never added to the charges." } ],
   "rules": [ "Every figure is listed with the line it was read from; nothing is totaled here, ...", "..." ] } }
 ```
-**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adjustment` | `stated_total_balance` (a total the statement prints: UB-04 line 0001, CMS-1500 Item 28
-**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept; `BALANCE_STEP_MISMATCH` on the line catches a wrongly read column). Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a charge; the FL 44 figure on a ro
-**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of t
-**Check codes (closed list, fixed message each):** `BALANCE_STEP_MISMATCH`, `LINE_UNCLEAR`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, and the response fields `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
-**Ladder.** All steps are code (parse, cite, compare); there is no model step, so no judge. The human step is reading the view; none of it is exportable.
+**Line classes.** `charge`, `adjustment`, `payment` come from the column or label the figure sits under (a line with several figures takes the first of charge, payment, adjustment); `rate` is a price, never a charge. `unclear` is everything else: a line whose figure could not be read, an **EOB service row** (`detail: eob`; its payer figures are in `eob`, never in `billed`/`paid`), and the **extra lines** (they carry `figure` and `why` instead of the four figure fields), told apart by `detail`: `rate` (class rate), `estimate`, `lien_amount` | `asserted_balance` | `reduction` (LOP and lien amounts, listed apart from the charges), `stated_total_billed` | `stated_total_paid` | `stated_total_adj
+**Rules (tested).** Figures are whole cents; credit notation (`(70.00)`, `45.00-`, `-45.00`) makes a charge negative (`detail: reversal`) and is read as a reduction in the payment and adjustment columns (magnitude kept). A running balance that does not follow from the line before it is listed as printed, with no flag. Ledger columns are assigned by position under the header (`CHARGES`, `PAYMENTS`, `ADJ`, `BALANCE`); two equally near columns or a figure far from every header is `unclear`, never guessed. `Bal fwd` is not a charge. A repeated line inside one record is listed twice. CMS-1500 money boxes have no decimal point: `85 | 00`, `85 00` and `8500` are all $85.00. UB-04: only FL 47 is a 
+**Nothing is silently missing (D-049, tested).** After every parser has run, the code reads each billing record again with its own tokenizer and collects every money-shaped token: a `$` figure, a number with two decimals (OCR letters tolerated), and a whole number in an amount position (under a ledger or UB-04 money column, in a prose sentence, in a balance-forward row, in the box of a dateless CMS-1500 service line; dates, times, codes, years and counts of visits/units/days are not tokens; definition in the `app/backend/billing.py` docstring). Each token is a `lines` entry, an `unreconciled` row, an `unclear` figure on its row, or its whole record is in `skipped_records`. A token none of t
+**Check codes (closed list, fixed message each):** `LINE_UNCLEAR`, `NO_DATE_OF_SERVICE`, `ROW_NOT_PARSED` (the last is the `reason_code` of an `unreconciled` row). None involves arithmetic. Removed by D-052: `LEDGER_TOTAL_MISMATCH`, `LEDGER_BALANCE_MISMATCH`, `CLAIM_TOTAL_MISMATCH`, `CLAIM_LEDGER_BILLED_MISMATCH`, `BALANCE_STEP_MISMATCH`, `LEDGER_EOB_PAID_MISMATCH`, `LEDGER_EOB_BILLED_MISMATCH`, and the response fields `payer_reports`, `providers`, `totals`, `complete`, `balance_convention`, `stated_totals`, `checks`, `line_flags`, `lop_lien`, `excluded`.
+**Ladder.** All steps are code (parse, cite); there is no model step, so no judge. The human step is reading the view; none of it is exportable.
 
 ## Spanish-language records (T-085, D-042)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:42.413Z

The api.md diff is consistent with the code, but it changes my F2 evidence. Line 664 of api.md says "no sums and no comparisons of any kind", and line 693 describes the reversal sign rule and duplicate merging as contract behaviour. My review says the contract does not name comparisons, which is incomplete. I'll read the test-file diff too, so the "every hunk" claim is true.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:44.144Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && git diff 2dc5be2 bcdcb91 -- tests/unit/test_billing.py > $SCR/test_diff.txt && wc -l $SCR/test_diff.txt && grep -n \"^@@\" $SCR/test_diff.txt && cut -c1-330 $SCR/test_diff.txt | sed -n 1,95p",
 "description": "Save the test-file diff and read its first hunks"
}
````

### User / tool · 2026-11-02T06:14:44.257Z

**tool result**
````
     277 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2/test_diff.txt
5:@@ -1,4 +1,4 @@
11:@@ -74,7 +74,7 @@ def rec(n, source, text, **kw):
20:@@ -82,7 +82,7 @@ def one(records):
29:@@ -129,14 +129,16 @@ def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
48:@@ -154,10 +156,11 @@ def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them(
62:@@ -262,16 +265,16 @@ def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
88:@@ -313,7 +316,7 @@ def test_billing_route_returns_the_listing(client):
97:@@ -530,8 +533,8 @@ def test_verifier_covers_every_cite_bearing_field():
108:@@ -578,9 +581,9 @@ def _items(out):
120:@@ -636,6 +639,21 @@ def _stmt(code, desc, charges, total, dos="06/01/26"):
142:@@ -678,6 +696,17 @@ PROBES = {
160:@@ -697,6 +726,9 @@ BARE_PROBES = {
170:@@ -740,6 +772,56 @@ def test_oracle_is_not_vacuous():
227:@@ -809,13 +891,13 @@ def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_an
244:@@ -949,9 +1031,9 @@ def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
256:@@ -974,8 +1056,11 @@ _BASES = {
269:@@ -986,7 +1071,7 @@ def _insert(text, tok, rnd, base):
diff --git a/tests/unit/test_billing.py b/tests/unit/test_billing.py
index 031d063..13a9a7f 100644
--- a/tests/unit/test_billing.py
+++ b/tests/unit/test_billing.py
@@ -1,4 +1,4 @@
-"""Billing analysis (T-083, D-042): code-only, every figure cited, nothing totaled that is not stated. SYNTHETIC ledgers from research/record-formats.md."""
+"""Billing analysis (T-083, T-103, D-042, D-052): code-only, every figure cited, nothing totaled or compared. SYNTHETIC ledgers from research/record-formats.md."""
 import time
 
 import pytest
@@ -74,7 +74,7 @@ def rec(n, source, text, **kw):
     return {"n": n, "source": source, "excerpt": text, "text": text, **kw}
 
 
-_GONE = {"complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
+_GONE = {"payer_reports", "matched_provider", "not_added_note", "complete", "balance_convention", "totals", "providers", "stated_totals", "stated_totals_repeated", "unreadable_providers",
          "stated_billed", "line_sum_billed", "line_flags", "negotiated_reductions", "balance_forwards"}
 
 
@@ -82,7 +82,7 @@ def one(records):
     """The analysis, with its citations verified and none of the removed total-shaped fields anywhere in it (D-052)."""
     out = B.analyze(records)
     assert B.verify_citations(out, records) == []
-    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules"}
+    assert set(out) == {"status", "lines", "unreconciled", "skipped_records", "rules"}
     assert not [k for d in B._walk(out) for k in d if k in _GONE]
     return out
 
@@ -129,14 +129,16 @@ def test_no_per_provider_totals_no_complete_flag_no_balance_check_anywhere():
     """D-052: a listing, not a ledger reconciliation. Whatever the statement prints is a cited line; nothing is summed or compared with a sum."""
     out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Fennimoor Spine Clinic, itemized ledger", PROSE)])
     assert {l["provider"] for l in out["lines"]} == {"Larkspur Hollow Physical Therapy", "Fennimoor Spine Clinic"}
-    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
+    assert {"LEDGER_TOTAL_MISMATCH", "LEDGER_BALANCE_MISMATCH", "CLAIM_TOTAL_MISMATCH", "CLAIM_LEDGER_BILLED_MISMATCH", "BALANCE_STEP_MISMATCH",
+            "LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"}.isdisjoint(B.CHECKS)
+    assert set(B.CHECKS) == {"LINE_UNCLEAR", "NO_DATE_OF_SERVICE", "ROW_NOT_PARSED"}      # nothing in billing sums or compares figures
 
 
 def test_void_is_a_reversal_charge_line_and_the_running_balance_is_just_a_figure():
     out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)])
     void = next(l for l in rows(out, "Larkspur") if "VOID" in l["description"])
     assert cents(void) == -7000 and void["class"] == "charge" and void["detail"] == "reversal"
-    assert "BALANCE_STEP_MISMATCH" not in checks(out) and [l["excerpt"] for l in rates(out)] != []
+    assert checks(out) == [] and [l["excerpt"] for l in rates(out)] != []
 
 
 def test_fee_schedule_rate_is_a_rate_line_and_never_a_charge():
@@ -154,10 +156,11 @@ def test_a_printed_total_is_a_cited_line_beside_the_rows_not_compared_with_them(
     assert [cents(l) for l in rows(out, "Larkspur")][:2] == [21000, 13000] and out["unreconciled"] == []      # the rows are as printed; no verdict on the total
 
 
-def test_running_balance_step_mismatch_is_flagged_on_the_line():
+def test_a_running_balance_that_does_not_follow_is_listed_as_printed_with_no_verdict():
+    """D-052 (strict): no arithmetic on a line either. A balance that is not the previous balance plus the charge is a figure, not a flag."""
     bad = LEDGER.replace("410.00\n", "415.00\n", 1)
     out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", bad)])
-    assert "BALANCE_STEP_MISMATCH" in checks(out)
+    assert checks(out) == [] and "415.00" in {l["balance"]["text"] for l in rows(out, "Larkspur") if l["balance"]}
 
 
 def test_unreadable_figure_is_listed_with_no_value():
@@ -262,16 +265,16 @@ def test_ub04_rate_on_the_charge_line_is_a_rate_and_0001_is_a_listed_total():
     assert all(l["code"] != "0001" for l in ls) and detail(out, "stated_total_billed")[0]["figure"]["cents"] == 916575
 
 
-def test_eob_is_a_payer_report_and_a_ledger_eob_paid_mismatch_is_raised():
+def test_eob_rows_are_lines_with_class_and_detail_and_no_check_against_the_ledger():
     out = one([rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)])
-    assert {l["record_no"] for l in out["lines"]} == {1}                     # the EOB's 235.00 billed is not a line of the ledger
-    e = out["payer_reports"][0]
-    assert e["matched_provider"].startswith("Larkspur") and len(e["lines"]) == 3
-    l140 = next(x for x in e["lines"] if x["service"] == "97140")
-    assert l140["plan_paid"]["cents"] == 1600 and l140["codes"] == "PR-1, PR-2, CO-45"
-    mism = [(c["code"], c["service"], c["ledger"]["cents"], c["eob"]["cents"]) for c in e["checks"]]
-    assert mism == [("LEDGER_EOB_PAID_MISMATCH", "97140", 0, 1600)]       # billed agrees after the void is netted; the ledger posted no payment
-    assert len(e["checks"][0]["cites"]) >= 3 and e["checks"][0]["cites"][0]["record_no"] == 2
+    eob = [l for l in out["lines"] if l["form"] == "eob"]
+    assert [(l["code"], l["class"], l["detail"], l["record_no"]) for l in eob] == [("97110", "unclear", "eob", 2), ("97140", "unclear", "eob", 2), ("97014", "unclear", "eob", 2)]
+    l140 = next(l for l in eob if l["code"] == "97140")
+    assert l140["eob"]["plan_paid"]["cents"] == 1600 and l140["eob"]["billed"]["cents"] == 7000 and l140["eob_codes"] == "PR-1, PR-2, CO-45"
+    assert l140["billed"] is None and l140["paid"] is None and l140["checks"] == [] and l140["excerpt"] in EOB     # an EOB row is never a charge or a payment
+    assert [cents(l) for l in rows(out, "Larkspur") if l["form"] == "ledger"][:2] == [21000, 13000]
+    assert checks(out) == []            # the ledger shows no payment for 97140 and the EOB $16.00; nothing is compared, so nothing is raised
+    assert B.CHECKS.keys().isdisjoint({"LEDGER_EOB_PAID_MISMATCH", "LEDGER_EOB_BILLED_MISMATCH"})
 
 
 def test_claim_form_and_ledger_for_one_provider_are_both_listed_each_with_its_form():
@@ -313,7 +316,7 @@ def test_billing_route_returns_the_listing(client):
     r = client.get(f"/api/cases/{tok}/billing")
     assert r.status_code == 200
     b = r.json()["billing"]
-    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "payer_reports", "rules", "citation_failures"} and b["status"] == "listed"
+    assert set(b) == {"status", "lines", "unreconciled", "skipped_records", "rules", "citation_failures"} and b["status"] == "listed"
     assert [cents(l) for l in b["lines"] if l["class"] == "charge"] == [25000, 18000, 231000]
     assert [x["figure"]["cents"] for x in b["lines"] if x["detail"] in ("asserted_balance", "reduction")] == [486000, 310000]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:47.467Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2; cut -c1-330 $SCR/test_diff.txt | sed -n 96,190p",
 "description": "Read the middle hunks of the test-file diff"
}
````

### User / tool · 2026-11-02T06:14:47.564Z

**tool result**
````
     assert client.get("/api/cases/nope/billing").status_code == 404
@@ -530,8 +533,8 @@ def test_verifier_covers_every_cite_bearing_field():
         fn(out)
         return B.verify_citations(out, r)
     pick = lambda o, d: next(l for l in o["lines"] if l["detail"] == d)
-    assert broken(lambda o: o["payer_reports"][0]["lines"][0].update(excerpt="made up")) != []
-    assert broken(lambda o: o["payer_reports"][0]["checks"][0]["cites"][0].update(excerpt="made up")) != []
+    assert broken(lambda o: pick(o, "eob").update(excerpt="made up")) != []
+    assert broken(lambda o: pick(o, "eob")["eob"]["plan_paid"].update(text="999.99")) != []          # an EOB figure must sit inside its own row
     assert broken(lambda o: pick(o, "stated_total_billed").update(excerpt="made up")) != []
     assert broken(lambda o: pick(o, "stated_total_billed")["figure"].update(text="999.99")) != []          # a printed total must sit inside its own cite
     assert broken(lambda o: pick(o, "rate").update(excerpt="made up")) != []
@@ -578,9 +581,9 @@ def _items(out):
         if "figure" in l:
             items.append((l["excerpt"], {_nt(l["figure"]["text"])}, l["detail"] in _WHOLE_ROW))
         else:
-            items.append((l["excerpt"], {_nt(l[k]["text"]) for k in ("billed", "paid", "adjustment", "balance") if l.get(k) and l[k]["cents"] is not None} | {_nt(t) for t in l["unclear"]}, False))
+            items.append((l["excerpt"], {_nt(l[k]["text"]) for k in ("billed", "paid", "adjustment", "balance") if l.get(k) and l[k]["cents"] is not None} | {_nt(t) for t in l["unclear"]}
+                          | {_nt(f["text"]) for f in (l.get("eob") or {}).values() if f["cents"] is not None}, False))      # an EOB row claims only the figures it lists
     items += [(u["excerpt"], {_nt(f) for f in u["figures"]}, False) for u in out["unreconciled"]]
-    items += [(x["excerpt"], set(), True) for e in out["payer_reports"] for x in e["lines"]]      # a payer-report row stands for its whole row
     return items
 
 
@@ -636,6 +639,21 @@ def _stmt(code, desc, charges, total, dos="06/01/26"):
     return tbl(HEAD_TXT, [row(dos, "06/02/26", code, desc, charges)], f"          TOTAL CHARGES {total}  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {total}")
 
 
+EOB_SRC = "Quoinmere Mutual Health Plan, explanation of benefits"
+_EOB_HEAD = EOB.split("\n")[:5]
+_EOB_COLS = "DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES"
+_EOB_TAIL = "CO-97: payment included in allowance for another service."
+
+
+def eob_text(*service_rows, total="TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00"):
+    """The sample EOB with the given service rows (a row is DOS, service, then the seven figure texts, then codes)."""
+    return "\n".join([*_EOB_HEAD[:4], _EOB_COLS, *service_rows, *([total] if total else []), _EOB_TAIL])
+
+
+def eob_row(billed="130.00", plan_paid="16.00", service="97110", codes="PR-1, CO-45", discount="52.00", allowed="78.00", deduct="22.00", coins="4.00", owes="26.00"):
+    return f"06/10/26  {service:<7} {billed:>7}   {discount:>7}   {allowed:>7}  {deduct:>7} {coins:>6}   {plan_paid:>8}   {owes:>9}     {codes}"
+
+
 # the T-083 probe sets (r1 to r5 reviews, artifacts/review-evidence/T-083-*): each is run through the oracle
 PROBES = {
     "sample_ledger": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER)],
@@ -678,6 +696,17 @@ PROBES = {
     "r5_prose_two_totals": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. New patient exam charge $250.00. Total charges $250.00. Total charges 99.00.")],
     "r5_prose_previous_balance_twice": [rec(1, PT, "Itemized ledger, statement date 06/15/2026. Previous balance $500.00. New patient exam charge $250.00. Previous balance $75.00. Total charges $250.00.")],
     "r5_ledger_with_eob": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, "Quoinmere Mutual Health Plan, explanation of benefits", EOB)],
+    "eob_sample": [rec(1, EOB_SRC, EOB)],
+    "eob_dollar_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(billed="$140")))],                    # T-103 r1 B1: '$140' was lost from every field
+    "eob_dollar_no_cents_paid": [rec(1, EOB_SRC, eob_text(eob_row(plan_paid="$16")))],
+    "eob_ocr_letters": [rec(1, EOB_SRC, eob_text(eob_row(billed="1O0.00")))],
+    "eob_bare_under_column": [rec(1, EOB_SRC, eob_text(eob_row(billed="130", plan_paid="16")))],
+    "eob_odd_decimals": [rec(1, EOB_SRC, eob_text(eob_row(billed="130.5", allowed="78.123")))],
+    "eob_missing_column": [rec(1, EOB_SRC, eob_text(eob_row().replace("   26.00", "")))],
+    "eob_extra_figure": [rec(1, EOB_SRC, eob_text(eob_row() + "  104.00"))],
+    "eob_figure_above_header": [rec(1, EOB_SRC, eob_text(eob_row()).replace("Provider:", "Billed to date $75.00\nProvider:"))],
+    "eob_total_row_no_cents": [rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              $235   115.00"))],
+    "eob_ledger_conflict": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER), rec(2, EOB_SRC, eob_text(eob_row(billed="$140")))],
     "r5_skipped_ambulance": [rec(1, "Brightwater Ambulance invoice", "Brightwater Ambulance (SYNTHETIC) invoice\nALS transport 1234.00 mileage 1234.00 supplies 1234.00")],
     "r5_skipped_injection": [rec(1, "Larkspur Hollow Physical Therapy, itemized statement", LEDGER, injection_tag=True)],
 }
@@ -697,6 +726,9 @@ BARE_PROBES = {
     "P4_balance_forward_bare": ([rec(1, PT, _fwd("Balance forward  100"))], "100", True),
     "P18_balance_forward_dollar_no_cents": ([rec(1, PT, _fwd("Balance forward  $100"))], "$100", True),
     "P15_dated_cms_bare_box": ([rec(1, CMS_SRC, cms(CMS_OK, "    060226   060226   11     98941              AB     45       1      SYN-NPI-0001"))], "45", False),
+    "eob_bare_charge": ([rec(1, EOB_SRC, eob_text(eob_row(billed="130")))], "130", False),
+    "eob_bare_paid": ([rec(1, EOB_SRC, eob_text(eob_row(plan_paid="16")))], "16", False),
+    "eob_bare_total_row": ([rec(1, EOB_SRC, eob_text(eob_row(), total="TOTAL              235   115.00"))], "235", True),
     "A_table_bare_charge": ([rec(1, PT, _ledger(row("06/10/26", "06/11/26", "99213", "Office visit", "185", "315.00")))], "185", False),
 }
 
@@ -740,6 +772,56 @@ def test_oracle_is_not_vacuous():
     assert [t for t, _u in unaccounted(recs, out, bare=("185",))] == ["185"]
 
 
+# ---- EOB rows (T-103 r2): every figure of a service row is a structured figure or sits on its row as unclear; nothing is compared with the ledger
+def _eob_line(out, service="97110"):
+    return next(l for l in out["lines"] if l["form"] == "eob" and l["code"] == service)
+
+
+@pytest.mark.parametrize("fig", ["$140", "$130", "1O0.00", "130", "130.5"])
+def test_eob_amount_without_clean_cents_is_on_its_row_as_unclear_with_its_text(fig):
+    recs = [rec(1, EOB_SRC, eob_text(eob_row(billed=fig)))]
+    out = one(recs)
+    line = _eob_line(out)
+    assert fig in line["unclear"] and line["eob"] == {} and line["class"] == "unclear" and line["detail"] == "eob" and line["checks"] == ["LINE_UNCLEAR"]
+    assert line["excerpt"] in recs[0]["text"] and fig in line["excerpt"]
+    assert unaccounted(recs, out, bare=(fig,) if re.fullmatch(r"\d+", fig) else ()) == []
+
+
+def test_eob_figure_that_disagrees_with_the_ledger_is_listed_and_nothing_is_raised():
+    """r1 B1/B2/M1: '$140' against a ledger 130.00. No check, no ledger sum, no payer report: both rows are lines with their own excerpt."""
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:14:50.774Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2; cut -c1-330 $SCR/test_diff.txt | sed -n 227,277p",
 "description": "Read the final hunks of the test-file diff"
}
````

### User / tool · 2026-11-02T06:14:50.857Z

**tool result**
````
@@ -809,13 +891,13 @@ def test_a_printed_balance_due_is_listed_as_printed_with_or_without_a_forward_an
                 f"          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE {due}").replace("\n06/01/26", "\n          Balance forward  100.00\n06/01/26", 1)
         out = one([rec(1, PT, t)])
         assert detail(out, "stated_total_balance")[0]["figure"]["text"] == due and detail(out, "balance_forward")[0]["figure"]["cents"] == 10000
-        assert out["unreconciled"] == [] and not [c for c in checks(out) if "BALANCE" in c and c != "BALANCE_STEP_MISMATCH"]
+        assert out["unreconciled"] == [] and checks(out) == []
 
 
-def test_balance_step_mismatch_is_flagged_on_the_line_and_an_unreadable_charge_is_class_unclear():
+def test_a_balance_step_that_does_not_follow_raises_nothing_and_an_unreadable_charge_is_class_unclear():
     t = tbl(HEAD_TXT, [row("06/01/26", "06/02/26", "97162", "PT eval", "210.00", "210.00"), row("06/10/26", "06/11/26", "97110", "Therapeutic exercise", "130.00", "999.00")],
             "          TOTAL CHARGES 340.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 340.00")
-    assert checks(one([rec(1, PT, t)])) == ["BALANCE_STEP_MISMATCH"]
+    assert checks(one([rec(1, PT, t)])) == []            # D-052: no arithmetic on a line; 999.00 is listed as printed
     assert next(l for l in rows(one(BARE_PROBES["A_table_bare_charge"][0]), "Medlark") if l["code"] == "99213")["class"] == "unclear"
 
 
@@ -949,9 +1031,9 @@ def test_unrecognised_billing_form_and_injection_are_skipped_never_none_found():
     assert [x["reason_code"] for x in out["skipped_records"]] == ["INJECTION_SUSPECTED"] and out["status"] == "listed" and out["lines"] == []
 
 
-def test_eob_is_a_payer_report_not_a_skip():
+def test_eob_is_lines_not_a_skip():
     out = one(PROBES["r5_ledger_with_eob"])
-    assert out["skipped_records"] == [] and len(out["payer_reports"]) == 1
+    assert out["skipped_records"] == [] and len([l for l in out["lines"] if l["form"] == "eob"]) == 3
     (u,) = out["unreconciled"]
     assert u["form"] == "eob" and u["excerpt"].startswith("TOTAL") and u["figures"][0] == "235.00"      # the EOB's printed total row is listed, not dropped
 
@@ -974,8 +1056,11 @@ _BASES = {
     "prose": lambda: PROSE,
     "cms": lambda: cms(CMS_OK, "    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001", total="28. TOTAL CHARGE  170 | 00     29. AMOUNT PAID  0 | 00"),
     "ub04": lambda: UB_ROOM,
+    "eob": lambda: EOB,
+    "eob_rows": lambda: eob_text(eob_row(), eob_row(service="97140", billed="70.00", plan_paid="16.00")),
 }
-_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04"}
+_SRC = {"table": PT, "table_sample": PT, "prose": "Fennimoor Spine Clinic, itemized ledger", "cms": CMS_SRC, "ub04": "Saltmarrow General Hospital, UB-04",
+        "eob": EOB_SRC, "eob_rows": EOB_SRC}
 _TOKENS = ["$123.45", "123.45", "$77", "88", "(45.00)", "1,234.50", "45.00-", "$9,999", "2O0.00", "9.999", "310"]
 
 
@@ -986,7 +1071,7 @@ def _insert(text, tok, rnd, base):
     if re.fullmatch(r"\d+", tok):
         if base == "prose":
             return text.replace(". Balance due", f". Office visit {tok}. Balance due", 1) if rnd.random() < 0.5 else text + f" Visit fee {tok}."
-        hdr, cols = B._header(lines) if base.startswith("table") else B._ub_header(lines)
+        hdr, cols = B._header(lines) if base.startswith("table") else B._eob_header(lines) if base.startswith("eob") else B._ub_header(lines)
         if hdr is None:
             return text
         kind = rnd.choice(sorted(k for k in cols if k != "rate"))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:17.109Z

I have now read every hunk of the commit's own changes to the three files, and the test diff raises no new findings. Next I'll check that the review's JSON parses, that there is exactly one json fence, and that the verdict follows the rule.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:18.800Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json, re\ns = open('reviews/T-103-staff-engineer-r2.md', encoding='utf-8').read()\nprint('fence count (all):', s.count('\\x60\\x60\\x60'), '| json fences:', len(re.findall(r'\\x60\\x60\\x60json', s)))\nblocks = re.findall(r'\\x60\\x60\\x60json\\n(.*?)\\n\\x60\\x60\\x60', s, re.S)\nd = json.loads(blocks[0])\nsev = [f['severity'] for f in d['findings']]\nrule = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('keys:', sorted(d))\nprint('card/persona/model:', d['card'], d['persona'], d['model'])\nprint('verdict:', d['verdict'], '| rule gives:', rule, '| severities:', sev)\nprint('whats_right:', len(d['whats_right']), '| questions:', len(d['questions_for_chris']))\nprint('exercised items:', len(d['exercised']))\n\"",
 "description": "Parse the review JSON and check fences and verdict rule"
}
````

### User / tool · 2026-11-02T06:15:18.905Z

**tool result**
````
fence count (all): 2 | json fences: 1
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
card/persona/model: T-103 staff-engineer-reviewer claude-haiku-5-5
verdict: changes | rule gives: changes | severities: ['major', 'minor', 'minor', 'minor', 'nit']
whats_right: 3 | questions: 2
exercised items: 14
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:33.759Z

The JSON parses, there is one json fence, and the verdict follows the rule. Before I write the correction, I want to test one thing I noticed in `_line_key`: it does not include the provider, so identical rows from two different providers in two records may merge into one line. That would hide a charge.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:37.250Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py",
 "content": "\"\"\"T-103 r2 extra probe: _line_key (billing.py:696-698) has no provider, and _merge_duplicates (billing.py:701-717) merges a line repeated in a\nlater record on that key. Two DIFFERENT providers with the same date, code, description and amounts in two records: are both kept?\nAlso the intended case: the same provider's statement re-sent (must merge). Run with T103_ARCH = the archive copy.\"\"\"\nimport os, sys\nsys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))\nimport tbr2 as T\ntb = T.tb\nB = tb.B\n\nROW = tb.row(\"06/10/26\", \"06/11/26\", \"97110\", \"Therapeutic exercise\", \"130.00\", \"130.00\")\nTXT = tb.tbl(tb.HEAD_TXT, [ROW], \"          TOTAL CHARGES 130.00  TOTAL PMTS 0.00  TOTAL ADJ 0.00  BALANCE DUE 130.00\")\n\nprint(\"== A: two different providers, identical 97110 row on 06/10/26 for 130.00\")\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", TXT), tb.rec(2, \"Medlark Clinic, itemized statement\", TXT)]\nout = tb.one(recs)\nfor l in out[\"lines\"]:\n    print(\"line providers:\", l[\"provider\"], \"| record_nos:\", l[\"record_nos\"], \"| cites:\", [c[\"record_no\"] for c in l[\"cites\"]], \"| billed:\", (l[\"billed\"] or {}).get(\"cents\"))\nprint(\"count of charge lines for 97110:\", len([l for l in out[\"lines\"] if l.get(\"code\") == \"97110\"]))\n\nprint(\"\\n== B: the same provider, same statement re-sent as record 2 (intended: one line, both cited)\")\nrecs = [tb.rec(1, \"Larkspur Hollow Physical Therapy, itemized statement\", TXT), tb.rec(2, \"Larkspur Hollow Physical Therapy, itemized statement\", TXT)]\nout = tb.one(recs)\nfor l in out[\"lines\"]:\n    print(\"line providers:\", l[\"provider\"], \"| record_nos:\", l[\"record_nos\"], \"| billed:\", (l[\"billed\"] or {}).get(\"cents\"))\nprint(\"count of charge lines for 97110:\", len([l for l in out[\"lines\"] if l.get(\"code\") == \"97110\"]))\n\nprint(\"\\n== C: _line_key fields\")\nprint(B._line_key({\"dos\": \"06/10/26\", \"posted\": \"06/11/26\", \"code\": \"97110\", \"description\": \"x\", \"billed\": {\"cents\": 13000}, \"paid\": None, \"adjustment\": None, \"form\": \"ledger\", \"provider\": \"P\"}))\n"
}
````

### User / tool · 2026-11-02T06:15:37.346Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:40.475Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py > artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt 2>&1; echo \"exit=$?\"; cat artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt | cut -c1-300",
 "description": "Run the cross-provider duplicate-merge probe on the archive copy"
}
````

### User / tool · 2026-11-02T06:15:40.936Z

**tool result**
````
exit=1
== A: two different providers, identical 97110 row on 06/10/26 for 130.00
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | cites: [1, 2] | billed: 13000
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py", line 17, in <module>
    print("line providers:", l["provider"], "| record_nos:", l["record_nos"], "| cites:", [c["record_no"] for c in l["cites"]], "| billed:", (l["billed"] or {}).get("cents"))
                                                                                                                                              ~^^^^^^^^^^
KeyError: 'billed'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:43.329Z

The merge is confirmed: two different providers' identical rows collapse into one line, record_nos [1, 2], provider Larkspur. The traceback is only my probe reading `billed` on a non-ledger line, so I'll fix that and rerun.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:15:45.646Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport pathlib\np = pathlib.Path('artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py')\ns = p.read_text(encoding='utf-8')\ns = s.replace('(l[\\\"billed\\\"] or {}).get(\\\"cents\\\")', '(l.get(\\\"billed\\\") or {}).get(\\\"cents\\\")')\ns = s.replace('for l in out[\\\"lines\\\"]:\\n    print(\\\"line providers:\\\"', 'for l in out[\\\"lines\\\"]:\\n    print(\\\"line providers:\\\"')\np.write_text(s, encoding='utf-8')\nprint('patched', s.count('l.get(\\\"billed\\\")'))\n\" && SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t103r2 && T103_ARCH=$SCR/head .venv/bin/python -I artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py > artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt 2>&1; echo \"exit=$?\"; cut -c1-300 artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt",
 "description": "Fix the probe's field access and rerun the merge check"
}
````

### User / tool · 2026-11-02T06:15:46.137Z

**tool result**
````
patched 2
exit=0
== A: two different providers, identical 97110 row on 06/10/26 for 130.00
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | cites: [1, 2] | billed: 13000
line providers: Larkspur Hollow Physical Therapy | record_nos: [1] | cites: [1] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1] | cites: [1] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1] | cites: [1] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1] | cites: [1] | billed: None
line providers: Medlark Clinic | record_nos: [2] | cites: [2] | billed: None
line providers: Medlark Clinic | record_nos: [2] | cites: [2] | billed: None
line providers: Medlark Clinic | record_nos: [2] | cites: [2] | billed: None
line providers: Medlark Clinic | record_nos: [2] | cites: [2] | billed: None
count of charge lines for 97110: 1

== B: the same provider, same statement re-sent as record 2 (intended: one line, both cited)
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | billed: 13000
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | billed: None
line providers: Larkspur Hollow Physical Therapy | record_nos: [1, 2] | billed: None
count of charge lines for 97110: 1

== C: _line_key fields
('06 10 26', '06 11 26', '97110', 'x', 13000, None, None, 'ledger')
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:03.620Z

The probe confirms the merge: record 2's identical Medlark charge is absorbed into the Larkspur line and no Medlark charge line remains. This is a fact-loss blocker, so my submitted review is wrong on its verdict. I'll check the existing duplicate test's coverage, then the board validator's accepted filenames.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:04.089Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_billing.py",
 "offset": 994,
 "limit": 8
}
````

### User / tool · 2026-11-02T06:16:04.097Z

**tool result**
````
994	
995	def test_identical_copy_of_one_statement_is_one_line_citing_both_records():
996	    t = _stmt("97162", "PT eval", "210.00", "210.00")
997	    out = one([rec(1, PT, t), rec(2, PT, t)])
998	    assert out["unreconciled"] == [] and [x["record_nos"] for x in detail(out, "stated_total_billed")] == [[1, 2]]
999	
1000	
1001	def test_second_claim_form_total_is_listed_too():
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:05.290Z

**tool call — Bash**
````
{
 "command": "grep -n \"validate\" tools/board.py | head -20; echo \"---\"; git show --stat --format= bcdcb91 -- memory/contracts/api.md | tail -1; git show bcdcb91 -- memory/contracts/api.md | grep -c \"^@@\"; git show -s --format=%H%n%s 1335f21 | head -2; git show --stat --format= faee448 | grep -c \"api.md\"; git show --stat --format= 1335f21 | grep \"api.md\"",
 "description": "Read the duplicate test and check validator usage and api.md scope in the commit"
}
````

### User / tool · 2026-11-02T06:16:05.488Z

**tool result**
````
740:    errs = validate_review_file(rp)
896:def validate_review_file(p: Path) -> list[str]:
927:def cmd_validate(a):
949:            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
1119:    s = sub.add_parser("validate"); s.add_argument("path", nargs="?"); s.set_defaults(fn=cmd_validate)
---
 1 file changed, 16 insertions(+), 15 deletions(-)
2
1335f21cbd92ab03f21a87b0c0949e6fb5bd9967
fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
1
 memory/contracts/api.md    |   6 +--
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:08.923Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tools/board.py",
 "offset": 896,
 "limit": 56
}
````

### User / tool · 2026-11-02T06:16:08.931Z

**tool result**
````
896	def validate_review_file(p: Path) -> list[str]:
897	    errs = []
898	    if p.name.startswith("GATE-") or p.name.startswith("CONTRACT-"):
899	        if len(p.read_text(encoding="utf-8").strip()) < 50:
900	            errs.append("gate summary is empty")
901	        return errs
902	    d = review_json(p)
903	    if d is None:
904	        return ["review must contain a ```json block (Appendix D.2) with a verdict"]
905	    for k in ("card", "persona", "verdict", "findings", "exercised"):
906	        if k not in d:
907	            errs.append(f"review JSON missing '{k}'")
908	    if d.get("verdict") not in VERDICTS:
909	        errs.append(f"verdict must be one of {VERDICTS}")
910	    if not isinstance(d.get("findings"), list):
911	        return ["review JSON 'findings' must be a list (use [] for none)"]
912	    sev = [f.get("severity") for f in d.get("findings", []) if isinstance(f, dict)]
913	    for f in d.get("findings", []):
914	        if not isinstance(f, dict) or f.get("severity") not in ("blocker", "major", "minor", "nit"):
915	            errs.append(f"finding has bad severity: {str(f)[:80]}")
916	        elif not f.get("evidence"):
917	            errs.append(f"finding without evidence: {f.get('title')}")
918	    if "blocker" in sev and d.get("verdict") != "fail":
919	        errs.append("a blocker finding requires verdict 'fail' (§7.4)")
920	    elif "major" in sev and "blocker" not in sev and d.get("verdict") != "changes":
921	        errs.append("a major finding (no blockers) requires verdict 'changes' (§7.4)")
922	    if not d.get("exercised"):
923	        errs.append("'exercised' is empty — a review that didn't exercise the artifact is invalid")
924	    return errs
925	
926	
927	def cmd_validate(a):
928	    targets = [Path(a.path)] if a.path else sorted(CARDS.glob("T-*.md"))
929	    errors = []
930	    shadow = _read_shadow()
931	    for t in targets:
932	        p = t if t.is_absolute() else (Path.cwd() / t)
933	        if not p.exists() and not t.is_absolute() and (ROOT / t).exists():
934	            p = ROOT / t
935	        p = Path(os.path.realpath(p))
936	        if not p.exists():
937	            errors.append(f"{t}: no such file")
938	            continue
939	        try:
940	            rel = p.relative_to(Path(os.path.realpath(ROOT)))
941	        except ValueError:
942	            errors.append(f"{t}: not inside the project")
943	            continue
944	        if not rel.parts or rel.parts[0] not in ("board", "reviews"):
945	            errors.append(f"{t}: not a board or review file")
946	            continue
947	        parts = rel.parts
948	        if parts[0] == "reviews" and p.suffix == ".md":
949	            errors += [f"{rel}: {e}" for e in validate_review_file(p)]
950	        elif parts[:2] == ("board", "cards") and p.suffix == ".md":
951	            try:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:29.916Z

The validator accepts any `reviews/*.md` name and checks the verdict rule, so a supersession file will validate. Before I write it, I need the exact line numbers for the provider assignment that runs before the merge.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:30.359Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/billing.py",
 "offset": 797,
 "limit": 8
}
````

### User / tool · 2026-11-02T06:16:30.367Z

**tool result**
````
797	        found_st = list({(v["cents"], v["text"], v["cite"]["excerpt"].strip()): (r, v) for r, v in reversed(found_st)}.values())[::-1]      # a byte-identical copy of one statement is one row
798	        if len(found_st) > 1:
799	            for r, v in found_st:
800	                lines.append(_blank_line(r, _family(rec_form.get(r["n"])), v["cite"]["excerpt"], unparsed=True, unclear=[v["text"]]))
801	    by_n = {r["n"]: r for r in recs}
802	    for ln in lines:
803	        ln["provider"] = _provider(by_n[ln["record_no"]])
804	    lines = _merge_duplicates(lines)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:40.076Z

Confirmed: the provider is set at lines 802-803 and the merge runs at 804. I'll check two more facts for the supersession file: that the merge code predates this commit, and which api.md hunks bcdcb91 itself changed.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:41.630Z

**tool call — Bash**
````
{
 "command": "echo \"--- _line_key / _merge_duplicates at 2dc5be2 (parent of r2)\"; git show 2dc5be2:app/backend/billing.py | grep -n \"def _line_key\\|def _merge_duplicates\\|return (_norm(l.get(\\\"dos\\\"))\" | cut -c1-200; echo \"--- same at bcdcb91\"; git show bcdcb91:app/backend/billing.py | grep -n \"def _line_key\\|def _merge_duplicates\" ; echo \"--- api.md hunks in bcdcb91 commit\"; git show bcdcb91 -- memory/contracts/api.md | grep \"^@@\" ; echo \"--- merge test at HEAD (same provider both records)\"; git show HEAD:tests/unit/test_billing.py | grep -n \"def test_identical_copy\" -A2 | cut -c1-200",
 "description": "Confirm the merge code predates the r2 commit and list the commit's api.md hunks"
}
````

### User / tool · 2026-11-02T06:16:41.787Z

**tool result**
````
--- _line_key / _merge_duplicates at 2dc5be2 (parent of r2)
683:def _line_key(l):
685:    return (_norm(l.get("dos")), _norm(l.get("posted")), _norm(l.get("code")), _norm(l.get("description")), g("billed"), g("paid"), g("adjustment"), l.get("form"))
688:def _merge_duplicates(lines):
--- same at bcdcb91
696:def _line_key(l):
701:def _merge_duplicates(lines):
--- api.md hunks in bcdcb91 commit
@@ -36,7 +36,7 @@ Status: drafted by the architect (T-014, round 2). From M2 the backend worker is
@@ -661,38 +661,39 @@ Always `200` with one envelope:
--- merge test at HEAD (same provider both records)
995:def test_identical_copy_of_one_statement_is_one_line_citing_both_records():
996-    t = _stmt("97162", "PT eval", "210.00", "210.00")
997-    out = one([rec(1, PT, t), rec(2, PT, t)])
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:16:56.165Z

The merge code is unchanged from the parent commit, so it predates this round. Two facts are now confirmed: the blocker is real, and the only api.md hunks in bcdcb91 are the route-table row and the billing section. I'll write the supersession review. The write-once guard blocks editing the r2 file, so this goes in a new `r2b` file that says it supersedes r2.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:19.466Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer-r2b.md",
 "content": "# T-103 staff-engineer review, r2b (commit bcdcb91): supersedes reviews/T-103-staff-engineer-r2.md\n\nReviewer: staff-engineer-reviewer. Model: claude-haiku-5-5. CLAUDE.md §6 and D-024 call for Sonnet on engineering reviewers; flagged, not changed (same as r1).\n\n**Verdict: fail.** One blocker, found after the r2 file was written: identical rows from two different providers are merged into one line, so one provider's charge disappears from the listing. Record this file, not r2.\n\n**Why r2 is superseded.** reviews/T-103-staff-engineer-r2.md gives verdict changes with no blocker. That verdict is wrong because of B1 below. Three statements in it also need correcting:\n1. Exercised: \"git diff 2dc5be2 bcdcb91 on the three files: every hunk read\" was overstated when written. The api.md and test-file diffs were persisted and only partly shown. Both are now read in full. The commit's own api.md change is two hunks: the billing route-table row (line 36) and the billing section (lines 661-699). The other api.md hunks in the 2dc5be2..bcdcb91 range come from 1335f21 and faee448, other cards. test_billing.py: every hunk of the commit read; no new finding there.\n2. F2 said the D-052 text does not name comparisons. That is true of memory/ORCHESTRATOR_DECISIONS.md:60 only. memory/contracts/api.md:664 says \"No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2)\". F2 below is updated.\n3. Check 1 said the one `_sum` hit is \"an unrelated function\". It is `def _summary_line` at app/backend/export.py:229, a prefix match of `def _sum`. Nothing is affected.\n\n**B1 (blocker): two providers' identical rows merge into one line.** Probe: artifacts/review-evidence/T-103-r2/merge_cross_provider_probe.py; output merge_cross_provider_probe_output.txt. Record 1 is Larkspur Hollow Physical Therapy and record 2 is Medlark Clinic. Both carry the same row `06/10/26 06/11/26 97110 Therapeutic exercise 130.00 130.00`. The output has one charge line for 97110, provider Larkspur Hollow Physical Therapy, record_nos [1, 2], billed 13000. Medlark's record produces only its four printed-total lines; its 97110 charge has no line of its own.\n\nCause: app/backend/billing.py:696-698 `_line_key` has no provider. billing.py:701-717 `_merge_duplicates` merges a later-record line whose key matches (merge condition at 706-707). The provider is assigned at billing.py:802-803, before the merge at 804. The key is the same at the parent commit (`git show 2dc5be2:app/backend/billing.py`, lines 683-685), so this predates bcdcb91. The identical-copy test at tests/unit/test_billing.py:995-998 puts the same provider in both records, so no test can see it. Persona checklist item 19 requires the dedupe key to include source and provider.\n\nWhy it matters: D-052's reason for a listing is that a listing cannot hide a missing line (api.md:664). Here a second provider's charge is hidden inside another provider's line, and the line attributes the charge only to Larkspur. That loses a fact, which is a blocker under D.2.\n\nFix: include the provider in the merge key. Merge only the same provider's re-sent statement (byte-identical excerpt, same provider and form). Otherwise keep both lines.\n\nAcceptance: a test with Larkspur and Medlark carrying the same row gives two 97110 charge lines, one per provider, each with its own record_no. The same-provider re-sent test (test_billing.py:995) still gives one line citing both records. A mutant that removes the provider from `_line_key` turns the new test red.\n\n**The rest of r2, updated.**\n- Checks 1-4 of r2 (sums and EOB checks gone; EOB tokens on their rows; R01/R03/R04/R05 red; no total-like route keys) still hold. The new probe does not change them.\n- F1 (major, carried): the rate row's running balance is still only inside its excerpt, and the whole-row exemption passes it (billing.py:649, test_billing.py:570; T01_table_rate_no_cents_failure.txt).\n- F2 (minor, updated): comparisons remain. The reversal sign test (billing.py:808) and the same-provider merge equality (billing.py:696-717) compare money values; the accounting net compares token text (billing.py:662, 725-727). memory/contracts/api.md:664 says \"no sums and no comparisons of any kind\", while api.md:693 describes the sign-based reversal rule. The contract conflicts with itself, so this needs Chris's ruling. If api.md:664 is read literally, F2 becomes major.\n- F3, F4, F5 as in r2 (stale comments; detail kinds; in-test EOB proof).\n\n**Pytest.** `.venv/bin/python -m pytest -q tests/unit/test_billing.py`: 179 passed in 1.04s in the project worktree (pytest_billing_HEAD_bcdcb91.txt). The same on the archive copy with `-I`: 179 passed in 0.93s (pytest_billing_archive_bcdcb91.txt). The suite passes because no test covers a cross-provider repeat.\n\n**Not exercised.** The full tests/unit suite. The app over HTTP (TestClient only). The D-019 accepted total was not re-run; the commit does not touch totals.py, present.py or api.py. Other providers' identical rows in real statements (the probe is synthetic).\n\nEvidence: artifacts/review-evidence/T-103-r2/ (RUN_ORDER.txt lists every command; the r2 file's evidence list still applies, plus merge_cross_provider_probe.py and its output).\n\n```json\n{\"card\": \"T-103\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git commit bcdcb91 (fix(backend): billing applies D-052 strictly, T-103 r2): app/backend/billing.py, tests/unit/test_billing.py, memory/contracts/api.md; scratch copy of git archive bcdcb91; project worktree (HEAD later c2a5d1f, billing files identical to bcdcb91); billing route via TestClient on evals/golden sample, case_03_rate_and_ocr, case_09_nonvisit_hides_gap and a synthetic EOB $140 case; a synthetic two-provider probe; no app URL exercised. Supersedes reviews/T-103-staff-engineer-r2.md.\",\n \"exercised\": [\n   \"git rev-parse HEAD -> bcdcb919f1723f51579db03d9426443860a91680 at review start; git log later showed c2a5d1f (T-106) and 3462ad0 (T-104) above it\",\n   \"git show --stat bcdcb91 -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py (3 files, 204 insertions, 138 deletions); git show bcdcb91 -- memory/contracts/api.md -> two hunks (@@ -36,7 and @@ -661,38)\",\n   \"git diff --stat bcdcb91 HEAD -- the three files -> empty; git status --short on the three files -> empty\",\n   \"git diff 2dc5be2 bcdcb91 read in full for billing.py, memory/contracts/api.md and tests/unit/test_billing.py (saved to the scratchpad and read hunk by hunk)\",\n   \".venv/bin/python -m pytest -q tests/unit/test_billing.py in the project worktree -> 179 passed in 1.04s\",\n   \"git archive bcdcb91 into a scratchpad copy; .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py on the copy -> 179 passed in 0.93s\",\n   \"merge_cross_provider_probe.py on the copy (merge_cross_provider_probe_output.txt): two providers, identical 97110 row, 06/10/26, 130.00 -> one charge line, provider Larkspur, record_nos [1, 2]; same provider re-sent -> one line citing both records; _line_key fields\",\n   \"git show 2dc5be2:app/backend/billing.py and bcdcb91 grep for _line_key and _merge_duplicates: key has no provider at both commits (lines 683-685 at 2dc5be2)\",\n   \"read billing.py 696-717, 801-804 (provider assignment and merge order); tests/unit/test_billing.py 995-998 (identical-copy test uses one provider)\",\n   \"r1_reprobe.py, route_keys.py, run_mutants_r2.py (R01 to R09, T01), run_mutants.py (r1 set), r2_survivor_and_m2_check.py, T01 failure detail: outputs in artifacts/review-evidence/T-103-r2/ (the r2 file's evidence list)\",\n   \"grep on the copy for LEDGER_EOB, _sum(, _tot(, payer_reports, BALANCE_STEP, balance_convention, stated_totals; grep of billing.py and the test module for float(, except, sleep(, random, network or model imports\",\n   \"memory/contracts/api.md 663-699 and memory/ORCHESTRATOR_DECISIONS.md:60 (D-052) read\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"fail_safe_completeness\": 3, \"decision_D052_conformance\": 3, \"honest_failure_no_silent_skip\": 3, \"api_doc_matches_code\": 3, \"money_integer_cents\": 5, \"no_llm_in_deterministic_path\": 5, \"test_mutation_catch\": 3, \"D019_total_unchanged\": 5},\n \"findings\": [\n   {\"severity\": \"blocker\",\n    \"title\": \"Identical rows from two different providers are merged into one line: a second provider's charge disappears from the listing (pre-existing, in scope)\",\n    \"evidence\": \"artifacts/review-evidence/T-103-r2/merge_cross_provider_probe_output.txt, case A: record 1 Larkspur Hollow Physical Therapy and record 2 Medlark Clinic, each with the row '06/10/26 06/11/26 97110 Therapeutic exercise 130.00 130.00'. One charge line for 97110: provider Larkspur Hollow Physical Therapy, record_nos [1, 2], billed 13000; Medlark's record gives only its four printed-total lines. Cause: app/backend/billing.py:696-698 _line_key has no provider; billing.py:701-717 _merge_duplicates merges a later-record line whose key matches (merge condition at 706-707); billing.py:802-803 assigns the provider before the merge at 804. Same key at 2dc5be2 (billing.py:683-685). tests/unit/test_billing.py:995-998 test_identical_copy_of_one_statement uses the same provider in both records.\",\n    \"why_it_matters\": \"D-052's reason for a listing is that a listing cannot hide a missing line (memory/contracts/api.md:664). Here a second provider's charge is hidden inside another provider's line, and the line attributes the charge only to Larkspur. The fact that Medlark billed the service is lost from the listing. That is a loss of a fact under D.2. Persona checklist item 19 requires the dedupe key to include source and provider, and it does not.\",\n    \"fix\": \"Include the provider in the merge key. Merge only a same provider re-sent statement (byte-identical excerpt, same provider and form, a second record). Otherwise keep both lines. Chris's answer to question 1 decides whether same-provider identical rows in two different statements also merge.\",\n    \"acceptance_test\": \"A test with Larkspur and Medlark carrying the same 97110 row gives two charge lines for 97110, one per provider, each with its own record_no. The same-provider re-sent test (test_billing.py:995) still gives one line citing both records. A mutant that removes the provider from _line_key turns the new test red.\"},\n   {\"severity\": \"major\",\n    \"title\": \"Rate-row running balance is still only inside its excerpt; the oracle's whole-row exemption is what passes it (r1 M2, not fixed at bcdcb91)\",\n    \"evidence\": \"r1_reprobe_output.txt and r2_survivor_and_m2_check_output.txt: row 'Charge per visit 185.00 999.00' gives one line, class rate, figure 185.00, and no balance field; '999.00' occurs only in the excerpt. app/backend/billing.py:649 whole = [x['excerpt'].strip() for x in list(rates) + list(lop)] and tests/unit/test_billing.py:570 _WHOLE_ROW = ('rate', 'estimate', 'reduction', 'lien_amount', 'asserted_balance') are unchanged in bcdcb91. T01_table_rate_no_cents_failure.txt: with 'rate' removed from _WHOLE_ROW, table_rate_no_cents fails with assert [('315.00', ...)] == [].\",\n    \"why_it_matters\": \"The running balance is a printed money token that a paralegal can only find inside the verbatim text. api.md:692 says a running balance is listed beside the lines, but on a rate row it is not a figure field of any line. The oracle accepts it only because the whole row is exempt. This is the r1 blind spot again, through the rate path.\",\n    \"fix\": \"Carry the rate row's running balance as a figure of the rate line (an unclear figure with its text, or a separate cited line with class unclear), then remove 'rate' from _WHOLE_ROW. Update api.md:692 to name the field.\",\n    \"acceptance_test\": \"For 'Charge per visit 185.00 999.00', '999.00' sits in a structured field of the output and not only in excerpt or cites; tests/unit/test_billing.py passes with 'rate' removed from _WHOLE_ROW; a mutant that drops that field turns the probe red.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"Comparisons remain: memory/contracts/api.md:664 says 'no sums and no comparisons of any kind', and the code still compares money values and token text\",\n    \"evidence\": \"app/backend/billing.py:808 (l['billed']['cents'] or 0) < 0 sets detail 'reversal' (a sign test on a money figure); billing.py:696-717 equality on billed, paid and adjustment cents for the merge (see B1); billing.py:662 it[1] == key and billing.py:725-727 _listed_elsewhere compare token text to decide whether a token is placed. memory/contracts/api.md:664 'No sums and no comparisons of any kind (D-052, applied strictly in T-103 r2)'. api.md:693 describes the sign rule ('credit notation ... makes a charge negative (detail: reversal)'). memory/ORCHESTRATOR_DECISIONS.md:60 forbids totals and a complete badge and does not mention comparisons.\",\n    \"why_it_matters\": \"The contract's own sentence is broader than the decision text, and the contract also describes the sign rule. None of the remaining comparisons produces a sum, a total, a shown verdict or a disagreement check. The merge comparison is the one that can hide a line, and B1 covers it. So this is minor pending Chris's ruling; if api.md:664 is read literally, F2 is major.\",\n    \"fix\": \"Chris rules on api.md:664. If literal: classify reversal from the excerpt's credit notation (parentheses or a trailing minus) and reword the sentence to say which comparisons remain. If not literal: reword api.md:664 to name the comparisons that are forbidden (checks that can say two figures disagree).\",\n    \"acceptance_test\": \"The ruling is recorded in memory/ORCHESTRATOR_DECISIONS.md under D-052 and api.md:664 matches the code. If literal: no money comparison remains in billing.py, and a test pins 'reversal' from a parenthesised figure.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"Stale comment and docstring wording name the removed provider-completeness state\",\n    \"evidence\": \"app/backend/billing.py:563 '...the provider of such a line is complete: false.' (no complete field exists; tests/unit/test_billing.py:77 lists 'complete' in _GONE). billing.py:170 'the provider is incomplete'; billing.py:180 'the provider is incomplete, and the figure is not left only in a field nobody opens'.\",\n    \"why_it_matters\": \"A reader who greps for 'complete: false' finds a comment about a flag that D-052 removed. 'Provider is incomplete' brings back the completeness state the decision retired.\",\n    \"fix\": \"Reword the three comments to say the figure is listed on its own line and that no provider completeness is claimed.\",\n    \"acceptance_test\": \"grep for 'complete: false' and 'provider is incomplete' in app/backend/billing.py returns nothing; the module docstring and api.md agree.\"},\n   {\"severity\": \"minor\",\n    \"title\": \"detail carries several kinds of thing (r1 m1, carried; 'eob' is one more value)\",\n    \"evidence\": \"r1_reprobe_output.txt, (class, detail) pairs over PROBES: (charge, reversal), (unclear, eob), (rate, rate), (unclear, asserted_balance), (unclear, stated_total_billed), (unclear, balance_forward), (unclear, None) and others. billing.py:808-809 computes detail from form, sign, description and balance.\",\n    \"why_it_matters\": \"A client has to branch on detail strings that mean different things: why a ledger row is listed, and what kind of extra line this is.\",\n    \"fix\": \"As r1 proposed: a closed kind list for what the line is, and a separate reason for why it is listed. Document both in api.md.\",\n    \"acceptance_test\": \"Every line has a kind from a closed list, and a test pins that list.\"},\n   {\"severity\": \"nit\",\n    \"title\": \"The in-test EOB fail-safe proves the oracle by editing the output, not the production path\",\n    \"evidence\": \"tests/unit/test_billing.py:804 test_eob_fail_safe_names_a_figure_dropped_from_a_row... deletes keys from the analysed output and asserts the oracle names them. The production-path proof is R01 and R04 in mutation_results_r2.txt.\",\n    \"why_it_matters\": \"The test is correct as an oracle test but does not run a changed parser. The parametrized test at tests/unit/test_billing.py:781 does exercise the parser's unclear path and catches R01, so this is only a nit.\",\n    \"fix\": \"Optional: add one test that patches the EOB parser's unclear list to empty and asserts the oracle names the figure.\",\n    \"acceptance_test\": \"Optional; mutant R01 stays red.\"}\n ],\n \"whats_right\": [\n   \"EOB money tokens sit on their rows: '$140', '1O0.00', bare '130' and '130.5' each stay as text on the EOB line, and the oracle names nothing unaccounted (r1_reprobe_output.txt).\",\n   \"No sums, payer checks or ledger comparisons remain: the 140.00 control raises no check, and no total-like key appears in the four route responses (route_keys_output.txt, grep_removed_names_bcdcb91.txt).\",\n   \"The EOB fail-safe is caught at the code level: R01, R03, R04 and R05 turn 7, 2, 4 and 19 tests red (mutation_results_r2.txt).\"\n ],\n \"questions_for_chris\": [\n   \"Two identical rows for the same provider in two different statements (not a re-sent copy): one charge or two? memory/contracts/api.md:664 says a re-sent statement is one line; the code also merges any identical row from a later record. The fix for B1 depends on the answer.\",\n   \"Does 'no sums and no comparisons of any kind' (memory/contracts/api.md:664) cover the reversal sign test (billing.py:808) and the same-provider merge equality? If yes, F2 becomes major.\",\n   \"For F1: may a rate row's running balance stay as cited excerpt text only (the bcdcb91 reading), or must it be a figure field (the r1 proposal)?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T06:17:19.755Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer-r2b.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:22.483Z

**tool call — Bash**
````
{
 "command": "python3 -c \"\nimport json, re\ns = open('reviews/T-103-staff-engineer-r2b.md', encoding='utf-8').read()\nprint('fence count (all):', s.count('\\x60\\x60\\x60'), '| json fences:', len(re.findall(r'\\x60\\x60\\x60json', s)))\nblocks = re.findall(r'\\x60\\x60\\x60json\\n(.*?)\\n\\x60\\x60\\x60', s, re.S)\nd = json.loads(blocks[0])\nsev = [f['severity'] for f in d['findings']]\nrule = 'fail' if 'blocker' in sev else ('changes' if 'major' in sev else 'pass')\nprint('verdict:', d['verdict'], '| rule gives:', rule, '| severities:', sev)\nprint('model:', d['model'], '| whats_right:', len(d['whats_right']), '| questions:', len(d['questions_for_chris']), '| exercised:', len(d['exercised']))\n\" && .venv/bin/python tools/board.py validate reviews/T-103-staff-engineer-r2b.md; echo \"validate-r2b-exit=$?\"; .venv/bin/python tools/board.py validate reviews/T-103-staff-engineer-r2.md; echo \"validate-r2-exit=$?\"",
 "description": "Parse the r2b JSON, check the verdict rule, and run the read-only board validator on both files"
}
````

### User / tool · 2026-11-02T06:17:22.700Z

**tool result**
````
fence count (all): 2 | json fences: 1
verdict: fail | rule gives: fail | severities: ['blocker', 'major', 'minor', 'minor', 'minor', 'nit']
model: claude-haiku-5-5 | whats_right: 3 | questions: 3 | exercised: 12
ok (1 file(s))
validate-r2b-exit=0
ok (1 file(s))
validate-r2-exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:36.827Z

Both files pass the read-only validator. While proofreading r2b against my notes, I found one imprecision: I cited "line 36" for the billing route-table row, but line 36 is where the hunk starts and the row itself is at line 39. The review file is write-once, so I'll record the fix as a correction in the evidence folder, following the r1 precedent.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:39.387Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/CORRECTION-1.txt",
 "content": "CORRECTION-1 to reviews/T-103-staff-engineer-r2b.md (the review file is write-once; verdict and findings are unchanged).\n\n1. Line citation. The r2b body says \"the billing route-table row (line 36)\" in api.md. Line 36 is where the hunk header starts (@@ -36,7 +36,7 @@). The billing row itself is at memory/contracts/api.md:39 (grep: \"39:| GET | `/api/cases/{token}/billing`\").\n\n2. Everything else cited in r2b was re-checked against command output before this note:\n   - billing.py 696-698 (_line_key), 701-717 (_merge_duplicates), 706-707 (merge condition), 802-804 (provider assignment, then merge), 662 and 725-727 (text identity), 808 (sign test), 563, 170, 180 (stale wording), 529, 531, 764, 779 (EOB rows and accounting pass), 649 (whole-row exemption).\n   - test_billing.py 77 (_GONE), 570 (_WHOLE_ROW), 781 (parametrized EOB test), 804 (in-test EOB fail-safe), 995-998 (identical-copy test, one provider).\n   - api.md 664, 693, 692; memory/ORCHESTRATOR_DECISIONS.md 60; app/backend/export.py 229 (def _summary_line, prefix match of def _sum).\n   - 2dc5be2:app/backend/billing.py 683-685 (same _line_key without provider); bcdcb91 api.md hunks at -36,7 and -661,38.\n   - Other cards' api.md hunks: 1335f21 changes memory/contracts/api.md (6 lines); faee448 changes it too.\n\nNo other change.\n"
}
````

### User / tool · 2026-11-02T06:17:39.493Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/CORRECTION-1.txt (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:48.799Z

Now the memory updates. The T-103 pattern file needs the r2 lessons: the provider-less dedupe key, the rate-row gap that stayed open, the HEAD move, and the overclaimed "every hunk read". I'll read the index first, since I'm editing it.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:49.059Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T06:17:49.068Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048 r2: verify stage no-op, skipif on untracked fixtures, shared sqlite across threads, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035 r1, T-033 r2: untested wiring, label-window bleed in amount classification, scratch controls
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039 r1-r2: hook contract vs specs, optional-hook proofs, judge-path mutation, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050 r1-r2: producer case= fix, delete-on-upgrade silent loss, guard in wrong file, pin HEAD by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038 r1-r3: fake hides real keys, fix picks internal not API shape, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057 r1-r4: stale-on-failed-rerun, freeze trigger untested beyond accept, orphan probe needs pre-fix control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043 r2: HEAD moves mid-review, archive needs untracked fixtures, guard traps, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — r1 "code only" docs that call models; r2 fixed defects still named open; r3 "no card" goes stale, None branch drops reason, HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts (D-033 blocker, not major)
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — r1-r2: mock fan-out, undo test, contract red at commit, mock contract drift, skipped e2e guard
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — r1-r3: elif reason wider than its message, gate survives, r3 pass: assert reason absence, not only wrong text
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059 r2: fix inside another card's commit, overstated mutant counts, $-anchor sweep, diagnosis wording
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — r1-r4: judge-never-ran summaries, gate vs export agreement, D-045(a) fixed in r4, carry-over minors need their file in the diff, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read citations before the first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — r6 e3cea6f: later decision supersedes old acceptance clause, allow-list "exactly" comment drift, reviewer write guard
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — r1 3104213: signature narrower than R-CO-7, vacuous order test; r2 b5b9b34: sort and J3/J4 mutants red, pass
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — r1 e491cad + r2 7df65fb (fail): audit prompt-id mismatch, 0.95 gate vs "every", arithmetic in controls, relabel basis
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1 f218263, r2 8bc7f90, r3 db08276 (all fail): bare figures vanish in prose/CMS/balance-forward, second balance-forward overwrites, counter blind to bare numbers, mutant label checks
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4 6bca71e (fail): repeated statement totals overwritten while counted as placed, skipped billing records leave complete true, stray bare-number definition gap
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation list, HEAD moved past card
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untested); T-099 r2 f345bc8 pass: case_count clause untested, F2 debt needs SCOPE_CUTS row
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — r5 690a0e3 fail: ledger+CMS totals share a [-1] slot, bare charge beyond TOL=8 dropped, complete ignores reconciliation checks
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — r1 4c5f9bf changes; r2 fdc2506 pass: guard tested for golden only, recheck test passes via backstop, latest.json blocks run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — dd84122 fail: summary-only edit bypasses accept guard, gate recomputes 2 of 5 checks, notes print AI wording
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — 2dc5be2 fail: whole-row oracle exemption hides EOB drops, silent EOB skip, D-052 sums in check objects, t093 red at HEAD
35	- [T-100 r2 patterns](project_t100_r2_patterns.md) — r2 288c1d3 changes: shared new_tokens, vocabulary narrower than _EN_* lists, fixture eval diff method, Spanish branches unpinned
36	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — 1335f21 pass: choke point verified by grep+probe; unchecked removed narrative text still printed; 4 unrelated unit failures
37	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:55.493Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t103_listing_review_patterns.md",
 "content": "---\nname: t103-listing-review-patterns\ndescription: T-103 billing listing, r1 2dc5be2 fail; r2 bcdcb91 changes, superseded by r2b fail: identical rows from two providers merge (dedupe key has no provider), rate-row balance still only in excerpt\nmetadata:\n  type: project\n---\n\nT-103 (billing as a cited line listing, D-052). Reviews: reviews/T-103-staff-engineer.md (r1, fail); reviews/T-103-staff-engineer-r2.md (changes, superseded); reviews/T-103-staff-engineer-r2b.md (fail, supersedes r2). Evidence: artifacts/review-evidence/T-103-r1/ and T-103-r2/.\n\n- r1 (2dc5be2): the oracle's whole-row exemption (test_billing.py `_items`) hid EOB drops; an unreadable EOB figure skipped its check silently; per-service ledger sums sat in payer checks.\n- r2 (bcdcb91) fixed the sums, the EOB checks and the EOB exemption: EOB $140, 1O0.00, 130, 130.5 now sit on their rows; R01/R03/R04/R05 turn tests red. Rate-row running balance (r1 M2) NOT fixed: billing.py:649 whole-row exemption still passes '999.00' (rate row has no balance field; T01 mutant shows 315.00 fails without it).\n- **Dedupe key has no provider.** billing.py `_line_key` (696-698, unchanged since 2dc5be2) + `_merge_duplicates` (701-717): two different providers with the same 97110 row in two records collapse into one line, provider of record 1, record_nos [1,2]. The identical-copy test uses one provider, so it cannot see it. Blocker (loses a fact). Missed by r1 and by my first r2 pass; found by probing the merge after the r2 file was written.\n- The rate of misses: a probe of \"two different sources, identical figures\" for every merge path would have caught it in r1.\n\n**Why:** the merge was only ever tested with the same source in both records; persona checklist item 19 says the dedupe key must include source/provider.\n\n**How to apply:** (1) for any \"repeat counts once\" rule, probe two different sources with identical figures; (2) grep the key tuple for a provider or source field; (3) for an output-shape card, still re-read the untouched merge code on the path; (4) a test named \"identical copy\" must put two different sources in its cases only if it means to test the same-source case.\n\n**Method notes (T-103):**\n- HEAD moved mid-review (bcdcb91 to c2a5d1f with 3462ad0 between). Pin by `git diff --stat <sha> HEAD -- <files>` being empty for the card's files.\n- Persisted tool output (over ~30KB) is not read in full. Save the diff to the scratchpad and read hunk by hunk before writing \"every hunk read\". My r2 claimed that before reading api.md and the test diff; the fix was a supersession file (r2b) plus CORRECTION-1.txt.\n- reviewer-write-guard refused Write to the scratchpad. Evidence scripts go under artifacts/review-evidence/T-103-r2/. Bash redirects into the scratchpad worked for the archive copy.\n- board-guard refuses bash commands containing unquoted `<` or `>`, even inside grep patterns. Use the Read tool for line ranges and Python for pattern scans.\n- A review file is write-once. A wrong verdict found later needs a suffixed file (r2b here) that says it supersedes; `board.py validate` accepts any reviews/*.md. r1's test_t093 red at HEAD remains unrelated to T-103.\n\nSee also [[t083-billing-review-patterns]], [[t083-r4-accounting-patterns]], [[t083-r5-cross-family-patterns]], [[feedback_review_write_once]].\n"
}
````

### User / tool · 2026-11-02T06:17:55.593Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t103_listing_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:57.984Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t103_listing_review_patterns.md",
 "old_string": "- The rate of misses: a probe of \"two different sources, identical figures\" for every merge path would have caught it in r1.",
 "new_string": "- A \"two different sources, identical figures\" probe on every merge path would have caught it in r1."
}
````

### User / tool · 2026-11-02T06:17:58.091Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t103_listing_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:17:58.921Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-103 listing patterns](project_t103_listing_review_patterns.md) — 2dc5be2 fail: whole-row oracle exemption hides EOB drops, silent EOB skip, D-052 sums in check objects, t093 red at HEAD",
 "new_string": "- [T-103 listing patterns](project_t103_listing_review_patterns.md) — r1 2dc5be2 fail; r2 bcdcb91 superseded by r2b fail: identical rows from two providers merge (key has no provider), rate balance in excerpt"
}
````

### User / tool · 2026-11-02T06:17:59.036Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:18:04.041Z

Memory is updated. Last housekeeping: remove the bytecode cache my probes created in the evidence folder, and add the merge probe to the run order so the evidence reproduces.

### Assistant · claude-haiku-5-5 · 2026-11-02T06:18:04.429Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/RUN_ORDER.txt"
}
````

### User / tool · 2026-11-02T06:18:04.439Z

**tool result**
````
1	T-103 r2 (commit bcdcb91) - how to reproduce the evidence in this folder
2	
3	0. Pin the code. From the project root:
4	     git rev-parse HEAD                        -> at review time bcdcb91...; HEAD later moved to c2a5d1f (T-106), 3462ad0 (T-104) in between
5	     git show --stat bcdcb91                   -> app/backend/billing.py, memory/contracts/api.md, tests/unit/test_billing.py
6	     git diff --stat bcdcb91 HEAD -- app/backend/billing.py tests/unit/test_billing.py memory/contracts/api.md   -> empty (identical)
7	     mkdir <A> && git archive bcdcb91 | tar -x -C <A>        (archive copy, used as T103_ARCH below)
8	
9	1. Unit tests:
10	     .venv/bin/python -m pytest -q tests/unit/test_billing.py         -> pytest_billing_HEAD_bcdcb91.txt (179 passed; project worktree at c2a5d1f, billing files identical)
11	     cd <A> && .venv/bin/python -I -m pytest -q -p no:cacheprovider tests/unit/test_billing.py   -> pytest_billing_archive_bcdcb91.txt (179 passed)
12	
13	2. Removed names (grep on the archive copy) -> grep_removed_names_bcdcb91.txt
14	
15	3. r1 probes re-run on the archive copy:
16	     T103_ARCH=<A> .venv/bin/python -I r1_reprobe.py                  -> r1_reprobe_output.txt
17	     T103_ARCH=<A> .venv/bin/python -I r2_survivor_and_m2_check.py    -> r2_survivor_and_m2_check_output.txt
18	
19	4. Billing route (TestClient, fixture backend, ingest only) on sample, case_03, case_09 and case_eob_140.txt (written by route_keys.py):
20	     T103_ARCH=<A> .venv/bin/python -I route_keys.py                  -> route_keys_output.txt
21	
22	5. Scratch-copy mutants (archive never edited; each anchor must match exactly once):
23	     .venv/bin/python -I run_mutants_r2.py <A> <MUTDIR>               -> mutation_results_r2.txt
24	     T01 (test-side whole-row exemption removed) failure detail:
25	     <MUTDIR>/T01_oracle_rate_whole_row_exemption_removed: pytest -k table_rate_no_cents -> T01_table_rate_no_cents_failure.txt
26	
27	Helper: tbr2.py loads tests/unit/test_billing.py from T103_ARCH (never from the project tree).
28	Unrelated to T-103 and not re-run here: tests/unit/test_t093_eval_signature.py (red at 841be23 and 2dc5be2 per r1).
29	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:18:04.971Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-103-r2/__pycache__ && ls artifacts/review-evidence/T-103-r2/ && git status --short -- reviews/ artifacts/review-evidence/T-103-r2/ | head -40",
 "description": "Remove the probe bytecode cache and list the evidence folder and review files"
}
````

### User / tool · 2026-11-02T06:18:05.090Z

**tool result**
````
CORRECTION-1.txt
RUN_ORDER.txt
T01_table_rate_no_cents_failure.txt
case_eob_140.txt
grep_removed_names_bcdcb91.txt
merge_cross_provider_probe.py
merge_cross_provider_probe_output.txt
mutation_results_r1_set_on_r2.txt
mutation_results_r2.txt
pytest_billing_HEAD_bcdcb91.txt
pytest_billing_archive_bcdcb91.txt
r1_reprobe.py
r1_reprobe_output.txt
r2_survivor_and_m2_check.py
r2_survivor_and_m2_check_output.txt
route_keys.py
route_keys_output.txt
run_mutants_r2.py
tbr2.py
?? artifacts/review-evidence/T-103-r2/
?? reviews/T-006-security-r2.md
?? reviews/T-006-security-r3.md
?? reviews/T-006-security.md
?? reviews/T-046-ux-designer-r2.md
?? reviews/T-046-ux-designer.md
?? reviews/T-053-security-r2.md
?? reviews/T-055-security-r2.md
?? reviews/T-057-staff-engineer-r4.md
?? reviews/T-058-security-r2.md
?? reviews/T-059-staff-engineer-r2.md
?? reviews/T-061-claims-adjuster-r4.md
?? reviews/T-063-staff-engineer-r2.md
?? reviews/T-063-staff-engineer-r3.md
?? reviews/T-064-ux-designer-r2.md
?? reviews/T-064-ux-designer.md
?? reviews/T-065-staff-engineer-r2.md
?? reviews/T-065-staff-engineer.md
?? reviews/T-066-staff-engineer-r2.md
?? reviews/T-066-staff-engineer-r3.md
?? reviews/T-066-staff-engineer.md
?? reviews/T-067-claims-adjuster-r2.md
?? reviews/T-067-claims-adjuster-r3.md
?? reviews/T-067-claims-adjuster-r4.md
?? reviews/T-067-claims-adjuster-r5.md
?? reviews/T-067-claims-adjuster.md
?? reviews/T-067-staff-engineer-r6.md
?? reviews/T-068-paralegal-r2.md
?? reviews/T-068-paralegal-r3.md
?? reviews/T-068-paralegal.md
?? reviews/T-069-claims-adjuster.md
?? reviews/T-070-staff-engineer-r2.md
?? reviews/T-070-staff-engineer.md
?? reviews/T-071-claims-adjuster-r2.md
?? reviews/T-071-claims-adjuster.md
?? reviews/T-072-claims-adjuster-r2.md
?? reviews/T-072-claims-adjuster-r3.md
?? reviews/T-072-claims-adjuster-r4.md
?? reviews/T-072-claims-adjuster.md
?? reviews/T-073-staff-engineer-r2.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:18:08.633Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/RUN_ORDER.txt",
 "old_string": "Helper: tbr2.py loads tests/unit/test_billing.py from T103_ARCH (never from the project tree).",
 "new_string": "6. Dedupe across two providers (the r2b blocker): T103_ARCH=<A> .venv/bin/python -I merge_cross_provider_probe.py   -> merge_cross_provider_probe_output.txt\n   Case A (two providers, identical 97110 row) must give two charge lines; the output gives one (record_nos [1, 2], provider Larkspur).\n\n7. Corrections: CORRECTION-1.txt (r2b line citation). The r2 file is superseded by reviews/T-103-staff-engineer-r2b.md.\n\nHelper: tbr2.py loads tests/unit/test_billing.py from T103_ARCH (never from the project tree)."
}
````

### User / tool · 2026-11-02T06:18:08.729Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-103-r2/RUN_ORDER.txt has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:18:12.543Z

T-103 r2: verdict fail, and `/Users/arsis/zlayt-pm-project/reviews/T-103-staff-engineer-r2b.md` supersedes my earlier `reviews/T-103-staff-engineer-r2.md` (verdict changes), because identical rows from two providers merge into one line (`/Users/arsis/zlayt-pm-project/app/backend/billing.py:696-717`, so one provider's charge is hidden); major: rate-row balance is still only in the excerpt (billing.py:649); pytest tests/unit/test_billing.py 179 passed; the four asked checks hold.
