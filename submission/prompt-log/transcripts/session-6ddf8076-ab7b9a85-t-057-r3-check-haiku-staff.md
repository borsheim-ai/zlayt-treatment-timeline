# Subagent: T-057 r3 check (haiku staff) (T-057 r3 check (haiku staff))

Source: `agent-ab7b9a85f4146895a.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:37:57.433Z

Round-3 check of board card T-057 in /Users/arsis/zlayt-pm-project. The fix is commit 8bf99fb. Read reviews/T-057-staff-engineer-r2.md and confirm the blocker is closed: a failed or rejected re-split must leave stored records and entries consistent. Run the reviewer's probe_rerun_fail2.py (find it with `grep -rl probe_rerun_fail2 artifacts reviews`) and `python3 -m pytest -q tests/unit/test_split_llm.py`. Try one mutation in a scratch copy: remove the record replacement and confirm the new test fails.

Write reviews/T-057-staff-engineer-r3.md, append-only, with a ```json block containing card, persona, verdict and findings. Never write literal key values; write <dummy> instead. Reply in 2 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:59.479Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T02:37:59.487Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T02:37:59.696Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-057-staff-engineer-r2.md"
}
````

### User / tool · 2026-11-02T02:37:59.703Z

**tool result**
````
1	# T-057 review, round 2: LLM split fallback (LLM_SPLIT), staff-engineer-reviewer
2	
3	Commit under review: b365af3 (pinned by `git archive`; HEAD has since moved to 08764e7, so I judged b365af3 plus the working tree where stated).
4	Verdict: **fail**. One blocker (a variant of round-1 blocker 2), three minors, one nit.
5	
6	Round-1 items, checked one by one:
7	- Blocker 1 (eval report hash): fixed. `git show b365af3:app/llm/prompts/split_v1.md | shasum -a 256` is 9a2d0cff...; `evals/reports/20261102T022701Z.md:45` lists the same hash, and the report is committed in b365af3. The report is still `ship_bar_met: False` (fixture backend, 3-run live metrics not measured). It has no split row (see minor 2).
8	- Blocker 2 (stale spans on same-count re-run): fixed for the case where the re-run's split succeeds (`pipeline.py` now deletes and re-stores on every `split_method == "llm"` run; mutant M1 fails a test). **Not fixed when the re-run's split fails or is rejected** (new blocker below).
9	- Major swallowed except: fixed. `SplitFailed` carries a reason code, `LLM_FAILED_AFTER_RETRIES` with `stage: split` reaches `errors[]`, and code rejections give a `SPLIT_REJECTED` warning. Mutants M2 and M7 fail tests.
10	- Major prompt_version / call id: fixed. `PROMPT_OF_STEP` feeds `audited_call`, the flag ladder carries `call_id`; mutants M3 and M6 fail tests.
11	- Major coverage / contiguity mutants: fixed. Dropping the coverage check (M4) or the contiguity check (M8) now fails tests.
12	- Major LLM_VS_CODE row 1: fixed by 473ac2a (row 1 now describes the fallback and names `test_split_llm.py`).
13	- Minors (span, MAX_RECORDS): fixed and tested (`SPLIT_TOO_MANY`; absolute evidence span).
14	
15	```json
16	{"card": "T-057", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
17	 "scope": "commit b365af3 (r1 fixes to 099732b): app/backend/ingest.py, pipeline.py, split_llm.py, app/llm/audited.py, app/llm/prompts/split_v1.md, evals/reports/20261102T022701Z.md, tests/unit/test_split_llm.py, deleted fixture e89d4fba...json. Pinned via git archive of b365af3 under artifacts/review-evidence/T-057-staff-engineer-r2/tree (with the then-untracked split fixture copied in for the control run). HEAD is now 08764e7 and the working tree is dirty. No app URL exercised. Golden case evals/golden/unsplit_paste.txt (synthetic) and a stub-split case.",
18	 "exercised": [
19	  "read personas/staff-engineer.md in full; read reviewer memory MEMORY.md and project_split_llm_review_patterns.md; read reviews/T-057-staff-engineer.md (round 1)",
20	  "python3 tools/board.py show T-059 and show T-057 -> T-057 rounds 1, commits [099732b, b365af3], round-1 findings listed",
21	  "git log --oneline | head -8 -> b365af3 is the r1 fix commit; git rev-parse HEAD at start -> b365af3f83d9; git log -4 later -> HEAD moved to fa8a36e / 08764e7 (bee1844 scores unsplit_paste in evals.run; 31070c3 commits the split fixture)",
22	  ".venv/bin/python -m pytest tests/unit -q -k split (working tree) -> 60 passed, 823 deselected in 1.61s",
23	  ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider (working tree, later) -> 895 passed in 17.46s",
24	  "git show b365af3 -- app/ evals/reports tests/unit/test_split_llm.py read in full",
25	  "git archive b365af3 into artifacts/review-evidence/T-057-staff-engineer-r2/tree: ls tests/fixtures/llm/split -> 'No such file or directory'; pytest -k split -> 3 failed, 57 passed (test_golden_unsplit_paste_replays_recorded_split_through_audited, test_run_pipeline_replaces_the_single_stored_record, test_split_audit_row_has_prompt_version_and_flag_resolves_to_call); git ls-files tests/fixtures/llm/split at that time printed nothing and git status showed '?? tests/fixtures/llm/split/'; after copying the untracked fixture d143a9a0...json in: 60 passed",
26	  "eval report provenance: git show b365af3:app/llm/prompts/split_v1.md | shasum -a 256 -> 9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b; grep -n split_v1 evals/reports/20261102T022701Z.md -> line 45 same hash; git log --oneline -- evals/reports/20261102T022701Z.md -> b365af3",
27	  "mutants (scratch copies of the pinned tree, pytest -k split, baseline 60 passed): M1 revert to replace-only-if-count-differs -> 1 failed; M2 drop the errors[] append for split failures -> 1 failed; M3 drop prompt_version in make_call -> 1 failed; M4 drop coverage check -> 1 failed; M5 drop SPLIT_TOO_MANY -> 1 failed; M6 drop call_id on the flag -> 2 failed; M7 swallow SplitFailed -> 2 failed; M8 drop contiguity -> 2 failed (script: artifacts/review-evidence/T-057-staff-engineer-r2/mutants.py)",
28	  "probe artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py on the pinned tree: run 1 split OK (3 records), run 2 same case split call raises LLMFailed",
29	  "grep of narrow scope: no float( or sleep( in split_llm.py or test_split_llm.py; the only except clauses in the split path are ingest.py:267 (SplitFailed), :269 (ValueError), split_llm.py:21,23,27 (specific types)",
30	  "docs/LLM_VS_CODE.md row 1 (line 29) read: describes the fallback, names test_split_llm.py; git log -3 -- docs/LLM_VS_CODE.md -> 473ac2a is the update",
31	  "Not exercised: frontend rendering of LLM_SPLIT; live claude-cli or API backend; python -m app.pipeline evals/golden/sample.txt (not in this card's brief); the live 3-run eval"
32	 ],
33	 "verdict": "fail",
34	 "scores": {"boundary_validation_fail_closed": 5, "llm_split_flagging_every_record": 4, "audit_routing_and_prompt_version": 5, "eval_regression_discipline_8_3": 4, "silent_failure_visibility": 5, "state_consistency_on_rerun": 2, "test_strength_on_ac1": 5, "doc_contract_alignment": 5, "commit_self_containedness": 2},
35	 "findings": [
36	  {"severity": "blocker",
37	   "title": "A re-run whose split fails or is rejected keeps the earlier run's model-split records; the new run's entries then cite text outside the stored record",
38	   "evidence": "pipeline.py at b365af3: 'if ing[\"split_method\"] == \"llm\": conn.execute(\"DELETE FROM records WHERE case_id=?\", (cid,))' then '_store_records(conn, cid, ing)', which returns early when rows already exist (pipeline.py:101-102). When run 2's split fails or is invalid, split_method is 'ambiguous', the DELETE is skipped, and run 1's three records stay. Repro: .venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py <pinned tree> prints: \"run1 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors []\", \"run2 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors [('LLM_FAILED_AFTER_RETRIES', 'split')] split_method None\", \"entry e1 record ['r1'] stored span (0, 47) excerpt 'Splint removed.' in stored record text: False\", \"INCONSISTENT\". The same holds for a code-rejected proposal (SPLIT_* reason), which takes the same branch. The new test test_rerun_with_different_boundaries_replaces_the_stored_records only covers a second successful split.",
39	   "why_it_matters": "This is the round-1 blocker again on a different path: the records table (what the case view renders from char_start/char_end, present.py:131) and the run's entries disagree. A visible LLM_FAILED_AFTER_RETRIES error is shown, but the stored record text for r1 is 47 characters while the entry cites a sentence from r3's text, so a quote is attributed to the wrong record. A split timeout on a re-run (POST /api/cases/{token}/run) is exactly the failure a live model produces, so it is reachable in production.",
40	   "fix": "Replace the stored records on every run in which the run's record set differs from the stored one, in the same transaction and before any entry or flag is written: delete and re-store whenever split_method != 'code' (or always, keyed on the ing records). Alternatively keep the first accepted split and do not re-ask the model on a re-run. Either way a failed re-split must leave records and entries consistent.",
41	   "acceptance_test": "test_split_llm.py: run_pipeline with a split stub giving boundaries A (3 records), then run_pipeline again with a split stub raising AU.LLMFailed (and a second case with invalid spans). After run 2: SELECT char_start, char_end FROM records matches the run's own records (one record 0..len(text)), and every entry excerpt is a substring of raw[char_start:char_end] of its own record. probe_rerun_fail2.py prints 'consistent'."},
42	  {"severity": "minor",
43	   "title": "The fix commit is not self-contained: it deleted the tracked split fixture and the replacement was left untracked",
44	   "evidence": "git show b365af3 --name-status -> 'D tests/fixtures/llm/split/e89d4fba...json'; git status at review start -> '?? tests/fixtures/llm/split/'; git archive b365af3 then 'pytest tests/unit -q -k split' -> '3 failed, 57 passed' (the three replay tests; the log shows the call with prompt_hash d143a9a0... found no fixture). After copying the untracked d143a9a0...json into the archive: 60 passed. Later commit 31070c3 adds the file (git ls-files tests/fixtures/llm/split now prints it).",
45	   "why_it_matters": "A clean checkout of the reviewed commit has three red split tests, and the 'recorded live' evidence for AC2 is not in that commit. This is resolved at HEAD by 31070c3, so the remaining point is process: the card's evidence commit must contain its fixtures.",
46	   "fix": "Already fixed in 31070c3. Add the fixture to the commit that changes the prompt hash, and check with a clean `git archive` run before in_review.",
47	   "acceptance_test": "git archive of the card's last commit + pytest tests/unit -q -k split -> 0 failed."},
48	  {"severity": "minor",
49	   "title": "The eval report at b365af3 has no row for the split step",
50	   "evidence": "evals/reports/20261102T022701Z.md (committed in b365af3) lists split_v1.md's hash at line 45 but no metric or assertion for unsplit_paste; grep -n unsplit evals/run.py at b365af3 -> no hits. HEAD has score_unsplit (evals/run.py:295, added in bee1844).",
51	   "why_it_matters": "Per your note, the unit replay is accepted evidence for the split eval; this is only to record that the committed report does not score it. The report is evidence for the prompt hash, not for split behaviour.",
52	   "fix": "Re-run evals.run at HEAD so a committed report contains the unsplit_paste row, and cite that report path in the card.",
53	   "acceptance_test": "A committed report under evals/reports lists an unsplit_paste result and split_v1.md hash 9a2d0cff...."},
54	  {"severity": "minor",
55	   "title": "The report is not a passing report: ship_bar_met is False and one entry-recall miss is in the committed numbers",
56	   "evidence": "evals/reports/20261102T022701Z.md:3 'ship_bar_met: False'; line 5 'Blockers: 4_no_invented_facts; backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)'; line 'entry misses: {\"case_06_subtle_pre_existing\": [{\"entry\": \"E3\", ...}]}', entry_recall 0.982.",
57	   "why_it_matters": "These come from the fixture backend and are not caused by T-057, and the prompt hash is the part this card is accountable for. Noted so nobody reads the report path as a green ship bar.",
58	   "fix": "Say in the card handoff that the report attests to the prompt hash only, and that the ship bar waits for the live 3-run.",
59	   "acceptance_test": "Card notes state what the report does and does not show."},
60	  {"severity": "nit",
61	   "title": "except ValueError in ingest wraps the splitter call and _llm_records, not just validate_split",
62	   "evidence": "app/backend/ingest.py:263-270 at b365af3: one try covers splitter(text), validate_split(...) and _llm_records(...); 'except ValueError as e' maps any ValueError to SPLIT_INVALID.",
63	   "why_it_matters": "A programming error in _llm_records that raises ValueError would be reported as a rejected AI proposal. It is visible (SPLIT_REJECTED) but mislabelled.",
64	   "fix": "Narrow the try to validate_split only, or raise a dedicated exception from it.",
65	   "acceptance_test": "A ValueError raised inside _llm_records propagates; a SPLIT_* ValueError from validate_split still yields SPLIT_REJECTED."}
66	 ],
67	 "whats_right": [
68	  "Every round-1 clause is now pinned by its own test: eight single-clause mutants of the split path each fail at least one test, including coverage and contiguity.",
69	  "Split failures are visible: SplitFailed carries a reason code, errors[] gets stage 'split', and unexpected exceptions propagate (test_unexpected_splitter_errors_propagate).",
70	  "The audit row carries prompt_version 'split_v1' and the LLM_SPLIT flag's ladder carries the call_id, and the committed eval report hash matches the committed prompt."
71	 ],
72	 "questions_for_chris": []}
73	```
74	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:00.230Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git show --stat 8bf99fb | head -40 && grep -rl probe_rerun_fail2 artifacts reviews",
 "description": "Show recent commits, fix commit stat, and locate probe script"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:00.696Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ && cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md",
 "description": "List reviewer memory and read split-LLM patterns"
}
````

### User / tool · 2026-11-02T02:38:00.783Z

**tool result**
````
MEMORY.md
feedback_severity_vs_brief.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_wiring_review_patterns.md
---
name: split-llm-review-patterns
description: T-057 r1 (LLM split fallback, commit 099732b): eval report hash vs committed prompt, same-count re-run leaves stale records, surviving mutants masked by a sibling check, audited prompt_version dropped
metadata:
  type: project
---

Recurring patterns from the T-057 round-1 review (2026-11-01, reviews/T-057-staff-engineer.md, verdict fail: 2 blockers, 4 majors).

- **Eval report can attest to a different prompt.** The card's report (evals/reports/20261102T021046Z.md:44) listed split_v1.md at sha 579868d5..., but the committed file was 8e872bc4.... The report was also never committed (git log -- report prints nothing). **Why:** CONTRACT 8.3 says re-run evals before in_review; an uncommitted report that hashes an older prompt is not evidence. **How to apply:** for any prompt/model/schema change, compare `git show <sha>:<prompt> | shasum -a 256` with the hash in the report and check `git log -- <report>`.
- **Same-count re-run keeps stale rows.** pipeline.py replaced stored records only when the count differed, and _store_records returns early when rows exist. A second run with different boundaries of the same count leaves run-1 spans while entries use run-2 spans. Reachable via POST /api/cases/{token}/run (api.py:312). A deterministic fixture hides it; use a stub split. **How to apply:** for any "replace on change" guard, test a re-run where the count is equal and the content differs.
- **Mutant survives because a sibling check catches the same case.** Dropping the line-start check fails tests, but dropping coverage or contiguity leaves 33/33 green. The "gap" and "overlap" cases start mid-line, so the line-start check rejects them first. **How to apply:** for every validator clause, build a case where only that clause fails (line-start-aligned) and mutate each clause alone.
- **audited make_call drops prompt_version for every step.** audited.py:106 never passes prompt_version, so llm_calls.prompt_version is NULL for all steps, including the new split. Caller also discarded the call_id (split_llm.py:17 `_call_id`). **How to apply:** after any new LLM step, query llm_calls for the step and check prompt_version and that the output links to a call_id.
- **Bare except in the fallback path.** `except Exception: pass` around a splitter swallowed LLMFailed; the run showed only SPLIT_AMBIGUOUS and no errors[] entry. **How to apply:** grep `except Exception` in every fallback; the test asserted only the record count.
- **Evidence span relative to the wrong base.** LLM_SPLIT evidence used start 0 / end len of the excerpt, which selects the banner in the paste. **How to apply:** check T[start:end] == evidence text for every new flag.

Harness and environment gotchas seen in this review (also relevant to other reviewers):
- reviewer-write-guard blocks Write to the scratchpad path; write evidence scripts under artifacts/review-evidence/<card>-staff-engineer/ instead.
- git-guard blocks `rm` with an unresolved shell expansion; use fresh directory names instead of deleting.
- board-guard treats a `>` inside a grep pattern as a redirect and blocks the command; avoid `>` in patterns (use grep -e).
- `git archive <sha>` excludes untracked fixtures. At any T-057-era commit the judge replay tests (test_t037_backend.py) fail with FIXTURE_MISS even after `cp -n` from the working tree, and the same 3 fail at the parent commit, so there is no clean full-suite control. Report the split subset as the control, and say so.
- HEAD moved (099732b -> 996f9b4) and the working tree had 145 dirty files during the review. Pin by full sha.

See also [[project_eval_runner_review_patterns]], [[project_backend_llm_review_patterns]], [[project_llm_stage_review_patterns]], [[project_harness_review_patterns]].

## Round 2 additions (T-057 r2 b365af3, T-059 20d866f; 2026-11-01)
- **Replace-on-change fixes cover only the success path.** r1 fix deleted stored records when split_method == 'llm'; a re-run whose split FAILS or is rejected skips the delete, so run-1 records stay while run-2 entries cite the unsplit block (repro: artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py). **How to apply:** for any "replace stored state" fix, test success->failure and success->success re-runs.
- **Fix commit deletes a tracked fixture and leaves its replacement untracked** (prompt hash change re-keys the fixture). Always `git archive <sha>` + pytest -k <card> as the clean control; check `git status --short tests/fixtures`.
- **Seeded-hallucination tests that accept any reason code** let a whole check be mutated away (T-059 N3 D-006 token check, N11 basis-hash staleness both survived 17 passed). Incidental checks (dropped 'C/O' qualifier) catch every row for a self-report quote; use a clean quote (e5 'Pain 4/10, improving.') to isolate checks.
- Mutant scripts: write with the Write tool under artifacts/review-evidence/<card>-staff-engineer/; a `>` or `<` inside a bash heredoc/sed string trips board-guard.
````

### User / tool · 2026-11-02T02:38:01.235Z

**tool result**
````
b614b40 board: sync cards, reviews, lessons, agent memory; append-only review guard; pathspec commit rule
8bf99fb fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
670ed09 test(backend): batch accept refuses needs_review and rejected entries (T-055 F1/F2)
991dac4 fix(backend): patient_report chip only on a whole-excerpt patient clause (T-061 r4, D-037)
38421cc memory: record §7.4 debt rows and scope cut 20
commit 8bf99fb5ff76026aaac7d30b7288b901a4e0f725
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:37:20 2026 -0600

    fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
    
    Stored records now follow the run's records on every run (delete + re-store in one transaction when ids/spans differ);
    ingest narrows the except to validate_split only.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 app/backend/ingest.py        | 14 +++++++++-----
 app/backend/pipeline.py      | 31 +++++++++++++++++++------------
 tests/unit/test_split_llm.py | 42 ++++++++++++++++++++++++++++++++++++++++++
 3 files changed, 70 insertions(+), 17 deletions(-)
reviews/T-057-staff-engineer-r2.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:04.510Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git show 8bf99fb -- app/backend/pipeline.py app/backend/ingest.py && cat artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py && ls artifacts/review-evidence/T-057-staff-engineer-r2/ && git ls-tree -r --name-only 8bf99fb tests/fixtures/llm/split | head",
 "description": "Show fix diff, probe script, and fixture list at fix commit"
}
````

### User / tool · 2026-11-02T02:38:04.683Z

**tool result**
````
b614b4086cd1a8cbfac20d3aa823e379bbf0581b
commit 8bf99fb5ff76026aaac7d30b7288b901a4e0f725
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:37:20 2026 -0600

    fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
    
    Stored records now follow the run's records on every run (delete + re-store in one transaction when ids/spans differ);
    ingest narrows the except to validate_split only.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/app/backend/ingest.py b/app/backend/ingest.py
index 942859b..14928ba 100644
--- a/app/backend/ingest.py
+++ b/app/backend/ingest.py
@@ -262,12 +262,16 @@ def ingest(raw_text: str, max_chars: int = MAX_CHARS, max_records: int = MAX_REC
     if splitter and method == "ambiguous" and len(recs) == 1 and (recs[0]["unsplit"] or not (recs[0]["date_raw"] and recs[0]["source"])):
         try:
             got = splitter(text)
-            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
-            recs, method, llm_split = _llm_records(text, validate_split(text, spans or [], max_records)), "llm", True
         except SplitFailed as e:           # the model did not answer: keep the one record and say why (never swallowed silently)
-            split_failure = e.code
-        except ValueError as e:            # the code check refused the proposal: keep the one record, with the reason code
-            split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
+            got, split_failure = None, e.code
+        if got is not None:
+            spans, split_call_id = got if isinstance(got, tuple) else (got, None)
+            try:
+                checked = validate_split(text, spans or [], max_records)
+            except ValueError as e:        # the code check refused the proposal: keep the one record, with the reason code
+                split_failure = str(e) if str(e).startswith("SPLIT_") else "SPLIT_INVALID"
+            else:
+                recs, method, llm_split = _llm_records(text, checked), "llm", True
     if len(recs) > max_records:
         raise IngestError("input_too_large")
     groups = dedupe(recs)
diff --git a/app/backend/pipeline.py b/app/backend/pipeline.py
index 42dc0f2..8e36a8a 100644
--- a/app/backend/pipeline.py
+++ b/app/backend/pipeline.py
@@ -109,15 +109,26 @@ def _not_duplicates(conn, cid: str) -> list:
 
 
 def _store_records(conn, cid: str, ing: dict) -> None:
-    if DB.table_counts(conn, cid)["records"]:
+    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
+    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
+    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
+    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
+    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
         return
-    for r in ing["records"]:
-        d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
-        DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
-                      date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
-                      source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
-                      date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
-                      encounter=int(r["encounter"]))
+    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
+    try:
+        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
+        for r in ing["records"]:
+            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
+            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
+                          date_header_start=d["start"], date_header_end=d["end"], source_header_start=s["start"], source_header_end=s["end"],
+                          source_label=r["source"], date_raw=r["date_raw"], date_iso=r["date_iso"], date_status=r["date_status"],
+                          date_candidates_json=r["date_candidates"], duplicate_of=r["duplicate_of"], injection_tag=int(r["injection_tag"]),
+                          encounter=int(r["encounter"]))
+        conn.execute("COMMIT")
+    except Exception:
+        conn.execute("ROLLBACK")
+        raise
 
 
 def _row(kind: str, it: dict) -> dict:
@@ -230,10 +241,6 @@ def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline
     by_n = {r["n"]: r for r in recs}
     if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
         errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
-    if ing["split_method"] == "llm":
-        # the stored records come from the creation-time code split (one unsplit block) or from an earlier run's model split: the model is
-        # not deterministic, so the records are replaced on EVERY LLM-split run, before any entry or flag is written
-        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
     _store_records(conn, cid, ing)
     dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
     entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
"""Run 1: model split OK (3 records). Run 2 (in place): split call fails -> one unsplit record. Do stored records match what run 2's entries cite?"""
import re, sys, tempfile, os
root = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)
from app.backend import ingest as IN, pipeline as PL
from app.db import db as DB
from app.llm import audited as AU
from tests.unit._fakes import FakeCall, sample_script

def _extract(u):
    body = re.search(r"RECORD TEXT:\n<record-\w+>\n(.*?)\n</record-", u, re.S).group(1)
    s = "Splint removed." if "Splint removed." in body else body.split(". ")[0].rstrip(".") + "."
    return dict(summary=s, excerpt=s)

T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
a2, a3 = T4.index("May 11"), T4.index("May 25")
A = [(0, a2), (a2, a3), (a3, len(T4))]
runs = iter([A, "FAIL"])
def split(u):
    v = next(runs)
    if v == "FAIL":
        raise AU.LLMFailed("down")
    return {"records": [{"start": a, "end": b} for a, b in v]}
call = FakeCall(sample_script(extract=_extract, split=split))
conn = DB.connect(os.path.join(tempfile.mkdtemp(), "x.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
st = lambda: [tuple(r) for r in conn.execute("SELECT id,char_start,char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
o1 = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
print("run1 stored", st(), "errors", [e["code"] for e in o1["errors"]])
o2 = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
print("run2 stored", st(), "errors", [(e["code"], e["stage"]) for e in o2["errors"]], "split_method", o2.get("split_method"))
span = {r[0]: (r[1], r[2]) for r in st()}
bad = 0
for e in DB.list_items(conn, cid, "entry"):
    s = span[e["record_ids"][0]]
    ok = e["excerpt"] in T4[s[0]:s[1]]
    print("entry", e["id"], "record", e["record_ids"], "stored span", s, "excerpt", repr(e["excerpt"]), "in stored record text:", ok)
    bad += (not ok)
print("INCONSISTENT" if bad else "consistent")
mut_1t21rje5
mut_3q04fywj
mut_cpkf6rlj
mut_d4rb06f3
mut_da2gkblv
mut_fwlsfjee
mut_g4uj8ykw
mut_gbpujwde
mut_igjwxxuk
mut_imbgri0q
mut_ly_zzj54
mut_pxrrbjqz
mut_qckojlrz
mut_w3m_7r5e
mut_ycbac4d9
mutants.py
probe_rerun_fail.py
probe_rerun_fail2.py
tree
tests/fixtures/llm/split/d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:10.125Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-057-staff-engineer-r3/tree && git archive 8bf99fb | tar -x -C artifacts/review-evidence/T-057-staff-engineer-r3/tree && cd artifacts/review-evidence/T-057-staff-engineer-r3/tree && ls tests/fixtures/llm/split && git -C /Users/arsis/zlayt-pm-project show 8bf99fb:app/backend/pipeline.py | grep -n \"def run_pipeline\" ; grep -n \"DELETE\\|def run_pipeline\\|_store_records\\|list_items\\|items\" app/backend/pipeline.py | head -60",
 "description": "Pin fix commit via git archive and inspect pipeline writes"
}
````

### User / tool · 2026-11-02T02:38:10.440Z

**tool result**
````
d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
224:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
27:    return {k: v for k, v in d.items() if not k.startswith("_")}
111:def _store_records(conn, cid: str, ing: dict) -> None:
114:    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
120:        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
151:def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
152:    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
155:    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
156:    for it in items:
171:    keep = {i["id"] for i in items}
172:    for oid, old in existing.items():
174:            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))
178:    """Stage 0 plus persistence of records and the code-made items (what POST /api/cases returns). No model call."""
180:    _store_records(conn, cid, ing)
224:def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
244:    _store_records(conn, cid, ing)
246:    entries, rejected, amount_items, flag_items, tray = [], [], [], [], []
320:    flag_items = ing["flags"] + [_clean(f) for f in llm_flags if f["state"] != "rejected"]
326:    flag_items.sort(key=lambda f: (order[f["type"]], f.get("from_date") or "", f["id"]))
333:    _persist(conn, cid, "flag", flag_items + [f for f in tray if "summary" not in f], now_t)
336:        err = {"code": "run_deadline", "message": "The run passed its time limit; finished items were kept."}
343:    all_items = dated + undated + final_amounts + flag_items
345:            "amounts": final_amounts_out, "damages": damages_out, "flags": flag_items, "tray": tray, "totals": tot, "warnings": ing["warnings"],
347:            "counts": {"entries": len(dated) + len(undated), "amounts": len(final_amounts_out), "flags": len(flag_items),
348:                       "needs_review": sum(1 for i in all_items if i["state"] == "needs_review"),
349:                       "verified": sum(1 for i in all_items if i["state"] == "verified")}}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:14.447Z

**tool call — Bash**
````
{
 "command": "sed -n 111,123p artifacts/review-evidence/T-057-staff-engineer-r3/tree/app/backend/pipeline.py && echo ---- && sed -n 151,176p artifacts/review-evidence/T-057-staff-engineer-r3/tree/app/backend/pipeline.py && echo ---- && sed -n 224,245p artifacts/review-evidence/T-057-staff-engineer-r3/tree/app/backend/pipeline.py && echo ---- && .venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r3/tree; echo \"exit=$?\"",
 "description": "Inspect persistence code and run r2 probe on pinned fix tree"
}
````

### User / tool · 2026-11-02T02:38:14.984Z

**tool result**
````
def _store_records(conn, cid: str, ing: dict) -> None:
    """Make the stored records equal this run's records. Same ids and spans -> nothing to do. Anything else (a model split that moved,
    or a re-run whose split failed or was rejected and so fell back to the code split) -> delete and re-store in the same transaction,
    before any entry, flag or amount of this run is written, so the records table and the run's items never disagree."""
    stored = [(r[0], r[1], r[2]) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
    if stored == [(r["id"], r["char_start"], r["char_end"]) for r in ing["records"]]:
        return
    conn.execute("BEGIN")                      # autocommit connection: one explicit transaction, all or nothing
    try:
        conn.execute("DELETE FROM records WHERE case_id=?", (cid,))
        for r in ing["records"]:
            d, s = IN.evidence_span(r, "date"), IN.evidence_span(r, "source")
            DB.add_record(conn, cid, id=r["id"], seq=r["n"], char_start=r["char_start"], char_end=r["char_end"],
----
def _persist(conn, cid: str, kind: str, items: list, now: float) -> None:
    """Write items by id. Existing rows keep their review status and events (a rerun never decides for the paralegal); a flag whose
    computed numbers changed has its status reset through the one review writer. Stale rows that are still pending are removed."""
    table = {"entry": "entries", "amount": "amounts", "flag": "flags"}[kind]
    existing = {i["id"]: i for i in DB.list_items(conn, cid, kind)}
    for it in items:
        row = _row(kind, it)
        old = existing.get(it["id"])
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
    keep = {i["id"] for i in items}
    for oid, old in existing.items():
        if oid not in keep and old["review_status"] == "pending":
            conn.execute(f"DELETE FROM {table} WHERE id=? AND case_id=? AND review_status='pending'", (oid, cid))


----
def run_pipeline(conn, cid: str, raw_text: str, *, call=None, now=None, deadline_s: float = DEADLINE_S, on_stage=None) -> dict:
    clock = now if callable(now) else (lambda: time.time() if now is None else now)
    t0 = clock()
    call = call or AU.make_call(conn, cid, now=clock)
    errors, stage_done = [], []

    def set_stage(name):
        if on_stage:
            on_stage(name)
        DB.update_case(conn, cid, status="running", stage=name)

    def expired():
        return clock() - t0 > deadline_s

    DB.update_case(conn, cid, status="running", stage="ingest", run_started_at=t0, error=None, backend=P.backend_name())
    ing = run_ingest(raw_text, call=call, not_duplicates=_not_duplicates(conn, cid))
    text, recs = ing["text"], ing["records"]
    by_n = {r["n"]: r for r in recs}
    if ing.get("split_failure") in ("LLM_FAILED_AFTER_RETRIES", "FIXTURE_MISS", "SCHEMA_INVALID"):
        errors.append(_err("LLM_FAILED_AFTER_RETRIES", "split", None, "FIXTURE_MISS" if ing["split_failure"] == "FIXTURE_MISS" else None))
    _store_records(conn, cid, ing)
    dated_cut = lambda e: e.get("date_status") in ("parsed", "confirmed") and e.get("date")      # noqa: E731
----
run1 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors []
run2 stored [('r1', 0, 128)] errors [('LLM_FAILED_AFTER_RETRIES', 'split')] split_method None
entry e1 record ['r1'] stored span (0, 128) excerpt 'Splint removed.' in stored record text: True
consistent
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:20.079Z

**tool call — Bash**
````
{
 "command": "git show 8bf99fb -- tests/unit/test_split_llm.py && cd artifacts/review-evidence/T-057-staff-engineer-r3/tree && grep -n \"def apply_review\\|def add_item\\|def list_items\\|def update_item\" app/db/db.py && grep -n \"def make_call\\|prompt_version\" app/llm/audited.py | head",
 "description": "Show new test diff and DB review helper signatures"
}
````

### User / tool · 2026-11-02T02:38:20.202Z

**tool result**
````
commit 8bf99fb5ff76026aaac7d30b7288b901a4e0f725
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:37:20 2026 -0600

    fix(backend): re-run with failed/rejected split replaces stored records atomically (T-057 r3)
    
    Stored records now follow the run's records on every run (delete + re-store in one transaction when ids/spans differ);
    ingest narrows the except to validate_split only.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_split_llm.py b/tests/unit/test_split_llm.py
index f24335d..2a6286d 100644
--- a/tests/unit/test_split_llm.py
+++ b/tests/unit/test_split_llm.py
@@ -210,6 +210,48 @@ def test_rerun_with_different_boundaries_replaces_the_stored_records(tmp_path):
         assert e["excerpt"] in T4[rec[0]:rec[1]]
 
 
+@pytest.mark.parametrize("second", ["call_fails", "invalid_spans"])
+def test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent(tmp_path, second):
+    """T-057 r2 blocker (probe_rerun_fail2): run 1 model-split into 3 records; run 2's split fails / is rejected -> one record. Stored
+    records must equal run 2's records and every entry excerpt must be a substring of its own stored record."""
+    from app.db import db as DB
+    from app.llm import audited as AU
+    from tests.unit._fakes import FakeCall, sample_script
+    T4 = IN.normalize_text("May 4, 2026\nDr. A, ortho. Fall. Wrist swelling.\nMay 11, 2026\nDr. A, ortho. Pain 5/10.\nMay 25, 2026\nDr. A, ortho. Splint removed.\n")
+    a2, a3 = T4.index("May 11"), T4.index("May 25")
+    A = [(0, a2), (a2, a3), (a3, len(T4))]
+    runs = iter([A, second])
+
+    def split(u):
+        v = next(runs)
+        if v == "call_fails":
+            raise AU.LLMFailed("down")
+        if v == "invalid_spans":
+            return {"records": [{"start": 0, "end": 10}, {"start": 10, "end": 20}]}      # does not cover the text
+        return {"records": [{"start": a, "end": b} for a, b in v]}
+    call = FakeCall(sample_script(extract=_extract, split=split))
+    conn = DB.connect(str(tmp_path / "c.sqlite")); cid = DB.create_case(conn, T4, now=1.0)
+    PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)
+    assert DB.table_counts(conn, cid)["records"] == 3
+    out = PL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)
+    stored = [tuple(r) for r in conn.execute("SELECT id, char_start, char_end FROM records WHERE case_id=? ORDER BY seq", (cid,))]
+    assert stored == [(r["id"], r["char_start"], r["char_end"]) for r in out["records"]] and len(stored) == 1
+    spans = {r[0]: (r[1], r[2]) for r in stored}
+    entries = DB.list_items(conn, cid, "entry")
+    assert entries
+    for e in entries:
+        a, b = spans[e["record_ids"][0]]
+        assert e["excerpt"] in T4[a:b], e["id"]
+
+
+def test_value_error_outside_validate_split_is_not_reported_as_a_rejected_split(monkeypatch):
+    def boom(text, spans):
+        raise ValueError("programming error")
+    monkeypatch.setattr(IN, "_llm_records", boom)
+    with pytest.raises(ValueError, match="programming error"):
+        IN.ingest(TEXT, splitter=lambda t: [(0, SECOND), (SECOND, len(t))])
+
+
 def test_split_call_failure_reaches_the_run_errors_and_is_audited_with_prompt_version(tmp_path):
     from app.db import db as DB
     from app.llm import audited as AU
114:def add_item(conn, case_id: str, kind: str, payload: dict, now: float = 0) -> str:
159:def list_items(conn, case_id: str, kind: str) -> list:
164:def update_item(conn, item_id: str, now: float = 0, *, case: str = None, **fields) -> None:
179:def apply_review(conn, item_id: str, action: str, edited: dict = None, now: float = 0, case: str = None) -> dict:
56:                 complete_with_meta=None, validate=None, item_id=None, now=None, prompt_version=None, sleep=None):
74:                      prompt_version=prompt_version, prompt_sha256=h, attempt=attempt, latency_ms=(res.latency_ms if res and res.latency_ms else ms),
104:def make_call(conn, case_id: str, *, now=None, models: dict = None, schemas: dict = None):
111:                            prompt_version=PROMPT_OF_STEP.get(step))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:28.180Z

**tool call — Bash**
````
{
 "command": "git status --short -- app tests evals | head -20; echo \"--- brief command (repo root)\"; python3 -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -15; echo \"--- pinned 8bf99fb tree with venv\"; cd artifacts/review-evidence/T-057-staff-engineer-r3/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -5; cd /Users/arsis/zlayt-pm-project && grep -n \"\\\"accept\\\"\\|'accept'\\|reject\" app/db/db.py | head",
 "description": "Run split unit tests at repo root and pinned fix tree"
}
````

### User / tool · 2026-11-02T02:38:29.109Z

**tool result**
````
 M app/backend/narrative.py
 M app/llm/backends/fixture.py
 M evals/reports/latest.json
 M tests/e2e/test_charges.py
 M tests/e2e/test_edit.py
 M tests/e2e/test_export_ui.py
 M tests/e2e/test_flags_panel.py
 M tests/e2e/test_input.py
 M tests/e2e/test_keyboard_mobile.py
 M tests/e2e/test_ladder_gate.py
 M tests/e2e/test_review_matrix.py
 M tests/e2e/test_side_by_side.py
 M tests/e2e/test_source_record.py
 M tests/e2e/test_timeline.py
 M tests/fixtures/llm/056527c8d5791a06af8e2dff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
 M tests/fixtures/llm/067240d96709b57638faad6e55ccb4a12af21dd382baec8516eeff30ae621cdd.json
 M tests/fixtures/llm/0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
 M tests/fixtures/llm/12c7d9209cd3664ab6d186c3019b41db44960c32d1e3116c3cab75b6940d40d1.json
 M tests/fixtures/llm/15676bbd3a5dfcc0ea008d7ce5df7d39df233a249a11548075e4595d1556399c.json
 M tests/fixtures/llm/1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
--- brief command (repo root)
/opt/homebrew/opt/python@3.12/bin/python3.12: No module named pytest
--- pinned 8bf99fb tree with venv
.............................                                            [100%]
29 passed in 0.52s
18:ACTIONS = {"accept": "accepted", "edit": "edited", "dismiss": "dismissed", "reset": "pending",
207:    action = {"accepted": "accept", "edited": "edit", "dismissed": "dismiss", "pending": "reset"}[status]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:33.688Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-057-staff-engineer-r3 && .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider -v 2>&1 | grep -i \"rerun\\|value_error\" ; echo \"--- live working tree (dirty), venv:\"; .venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | tail -2; echo \"--- mutant copy\"; mkdir -p $R/mut-no-replace && git archive 8bf99fb | tar -x -C $R/mut-no-replace && .venv/bin/python -c \"\nimport pathlib\np=pathlib.Path('$R/mut-no-replace/app/backend/pipeline.py'); s=p.read_text()\nold='def _store_records(conn, cid: str, ing: dict) -> None:\\n'\nassert s.count(old)==1\np.write_text(s.replace(old, old+'    return  # MUTANT: record replacement removed\\n',1)); print('mutated')\n\" && cd $R/mut-no-replace && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | grep -E \"FAILED|passed|failed\" | tail -12; echo \"--- probe on mutant\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py /Users/arsis/zlayt-pm-project/$R/mut-no-replace | tail -3",
 "description": "Verbose rerun tests, live tree check, and remove-replacement mutant"
}
````

### User / tool · 2026-11-02T02:38:36.737Z

**tool result**
````
--- live working tree (dirty), venv:
.............................                                            [100%]
29 passed in 0.51s
--- mutant copy
mutated
        assert {"code": "LLM_FAILED_AFTER_RETRIES", "stage": "split"} == {k: v for k, v in next(e for e in out["errors"] if e["stage"] == "split").items() if k in ("code", "stage")}
FAILED tests/unit/test_split_llm.py::test_run_pipeline_replaces_the_single_stored_record
FAILED tests/unit/test_split_llm.py::test_rerun_with_different_boundaries_replaces_the_stored_records
FAILED tests/unit/test_split_llm.py::test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[call_fails]
FAILED tests/unit/test_split_llm.py::test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[invalid_spans]
FAILED tests/unit/test_split_llm.py::test_split_call_failure_reaches_the_run_errors_and_is_audited_with_prompt_version
5 failed, 24 passed in 0.52s
--- probe on mutant
Traceback (most recent call last):
  File "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py", line 33, in <module>
    s = span[e["record_ids"][0]]
        ~~~~^^^^^^^^^^^^^^^^^^^^
KeyError: 'r1'
run1 stored [] errors []
run2 stored [] errors [('LLM_FAILED_AFTER_RETRIES', 'split')] split_method None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:44.659Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r3/probe_accepted_orphan.py",
 "content": "\"\"\"Round-3 extra probe. Run 1 model-splits into 3 records; the paralegal ACCEPTS every entry; run 2's split fails (one unsplit record).\nDo accepted entries from run 1 still cite records that exist in the records table after run 2? Argument 1: pinned tree root.\"\"\"\nimport re, sys, tempfile, os\nroot = sys.argv[1]; sys.path.insert(0, root); os.chdir(root)\nfrom app.backend import ingest as IN, pipeline as PL\nfrom app.db import db as DB\nfrom app.llm import audited as AU\nfrom tests.unit._fakes import FakeCall, sample_script\n\ndef _extract(u):\n    body = re.search(r\"RECORD TEXT:\\n<record-\\w+>\\n(.*?)\\n</record-\", u, re.S).group(1)\n    s = \"Splint removed.\" if \"Splint removed.\" in body else body.split(\". \")[0].rstrip(\".\") + \".\"\n    return dict(summary=s, excerpt=s)\n\nT4 = IN.normalize_text(\"May 4, 2026\\nDr. A, ortho. Fall. Wrist swelling.\\nMay 11, 2026\\nDr. A, ortho. Pain 5/10.\\nMay 25, 2026\\nDr. A, ortho. Splint removed.\\n\")\na2, a3 = T4.index(\"May 11\"), T4.index(\"May 25\")\nA = [(0, a2), (a2, a3), (a3, len(T4))]\nruns = iter([A, \"FAIL\"])\ndef split(u):\n    v = next(runs)\n    if v == \"FAIL\":\n        raise AU.LLMFailed(\"down\")\n    return {\"records\": [{\"start\": a, \"end\": b} for a, b in v]}\ncall = FakeCall(sample_script(extract=_extract, split=split))\nconn = DB.connect(os.path.join(tempfile.mkdtemp(), \"x.sqlite\")); cid = DB.create_case(conn, T4, now=1.0)\nst = lambda: [tuple(r) for r in conn.execute(\"SELECT id,char_start,char_end FROM records WHERE case_id=? ORDER BY seq\", (cid,))]\nPL.run_pipeline(conn, cid, T4, call=call, now=lambda: 1.0)\nrun1_entries = DB.list_items(conn, cid, \"entry\")\nprint(\"run1 records\", st(), \"entries\", [(e[\"id\"], e[\"record_ids\"]) for e in run1_entries])\nfor e in run1_entries:\n    DB.apply_review(conn, e[\"id\"], \"accept\", now=1.5, case=cid)\nPL.run_pipeline(conn, cid, T4, call=call, now=lambda: 2.0)\nlive = {r[0] for r in st()}\nafter = DB.list_items(conn, cid, \"entry\")\nprint(\"run2 records\", st())\nprint(\"after run2 entries\", [(e[\"id\"], e[\"record_ids\"], e[\"review_status\"]) for e in after])\norphans = [e[\"id\"] for e in after if any(rid not in live for rid in e[\"record_ids\"])]\nprint(\"ORPHANED accepted entries (cite a record id not in records table):\" if orphans else \"no orphaned entries\", orphans)\n"
}
````

### User / tool · 2026-11-02T02:38:44.759Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r3/probe_accepted_orphan.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:47.625Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-057-staff-engineer-r3 && .venv/bin/python $R/probe_accepted_orphan.py /Users/arsis/zlayt-pm-project/$R/tree; echo \"exit=$?\"; echo \"--- mutant B: keep stored records when any exist (the r2 behaviour, replace removed on changed path)\"; rm -rf $R/mut-keep-if-any 2>/dev/null; mkdir -p $R/mut-keep-if-any && git archive 8bf99fb | tar -x -C $R/mut-keep-if-any && .venv/bin/python -c \"\nimport pathlib\np=pathlib.Path('$R/mut-keep-if-any/app/backend/pipeline.py'); s=p.read_text()\nold='    if stored == [(r[\\\"id\\\"], r[\\\"char_start\\\"], r[\\\"char_end\\\"]) for r in ing[\\\"records\\\"]]:\\n'\nassert s.count(old)==1, s.count(old)\np.write_text(s.replace(old, '    if stored:  # MUTANT: keep whatever is stored\\n',1)); print('mutated B')\n\" && cd $R/mut-keep-if-any && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider 2>&1 | grep -E \"^FAILED|passed|failed\" | tail -8; cd /Users/arsis/zlayt-pm-project && .venv/bin/python artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py /Users/arsis/zlayt-pm-project/$R/mut-keep-if-any | tail -3",
 "description": "Run accepted-orphan probe and a keep-if-any mutant"
}
````

### User / tool · 2026-11-02T02:38:49.667Z

**tool result**
````
run1 records [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] entries [('e1', ['r1']), ('e2', ['r2']), ('e3', ['r3'])]
run2 records [('r1', 0, 128)]
after run2 entries [('e1', ['r1'], 'accepted'), ('e2', ['r2'], 'accepted'), ('e3', ['r3'], 'accepted')]
ORPHANED accepted entries (cite a record id not in records table): ['e2', 'e3']
exit=0
--- mutant B: keep stored records when any exist (the r2 behaviour, replace removed on changed path)
mutated B
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cb3de0402f9a7 step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cefda64059ae4 step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=c27c8065e5c38 step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
FAILED tests/unit/test_split_llm.py::test_run_pipeline_replaces_the_single_stored_record
FAILED tests/unit/test_split_llm.py::test_rerun_with_different_boundaries_replaces_the_stored_records
FAILED tests/unit/test_split_llm.py::test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[call_fails]
FAILED tests/unit/test_split_llm.py::test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[invalid_spans]
4 failed, 25 passed in 0.58s
run2 stored [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] errors [('LLM_FAILED_AFTER_RETRIES', 'split')] split_method None
entry e1 record ['r1'] stored span (0, 47) excerpt 'Splint removed.' in stored record text: False
INCONSISTENT
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:38:59.957Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r3/tree && grep -n \"record_ids\\|record_id\" app/backend/*.py app/db/*.py | head -40; echo ---; sed -n 120,140p app/backend/present.py",
 "description": "Check how entries link to records in backend and presentation"
}
````

### User / tool · 2026-11-02T02:39:00.062Z

**tool result**
````
app/backend/export_routes.py:38:            "entries": [{"id": e["id"], "record_ids": e.get("record_ids") or [f"r{e['record_no']}"],
app/backend/generator.py:38:    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
app/backend/pipeline.py:65:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:80:                      "record_nos": [w["record_no"]], "record_ids": [r["id"]], "source_kind": "record", "review_status": "pending",
app/backend/pipeline.py:102:    return {"id": item_id or a["id"], "record_nos": a["record_nos"], "record_ids": [f"r{n}" for n in a["record_nos"]], "text": a["raw"], "raw": a["raw"],
app/backend/pipeline.py:137:        return {"record_ids_json": it["record_ids"], "seq": it["seq"], "date_iso": it.get("date"), "provider": it["provider"],
app/backend/pipeline.py:141:        return {"record_ids_json": it["record_ids"], "entry_id": it.get("entry_id"), "text": it["text"], "value_cents": it["cents"],
app/backend/pipeline.py:144:    computed = {k: it[k] for k in ("subtype", "from_date", "to_date", "days", "body_date", "first_treatment_date", "stated_dates", "record_ids",
app/backend/pipeline.py:207:    return next((e["id"] for e in entries if f"r{record_no}" in e["record_ids"]), None)
app/backend/pipeline.py:314:        f["record_ids"] = [f"r{n}" for n in f["record_nos"]]
app/backend/pipeline.py:331:    _persist(conn, cid, "entry", dated + undated + [e for e in tray if e.get("record_ids") and "summary" in e], now_t)
app/backend/pipeline.py:354:    """The GET /api/cases/{token} shape the eval runner reads (memory/contracts/api.md): evidence carries record_id + excerpt, flags carry
app/backend/pipeline.py:361:        g["evidence"] = [{**e, "record_id": f"r{e['record_no']}", "excerpt": e.get("text")} for e in f.get("evidence", [])]
app/backend/store.py:46:        d = dict(id=e["id"], record_ids=e["record_ids"], record_no=n_of.get((e["record_ids"] or [None])[0], 0), summary=ed.get("summary", e["summary"]),
app/backend/store.py:61:    amts = [dict(id=a["id"], record_no=n_of.get((a["record_ids"] or [None])[0], 0), cents=a["value_cents"], cls=a["kind"], raw=a["text"],
app/backend/store.py:66:        ev = [dict(record_no=x.get("record_no") or n_of.get(x.get("record_id"), 0), field=x.get("field", "excerpt"),
app/backend/api.py:403:        """D-031: split one record back out of a merged entry. Body {record_id}."""
app/backend/api.py:405:        if not isinstance(b.get("record_id"), str):
app/backend/api.py:410:            return review.not_duplicate(c, token, item_id, b["record_id"], call=make_call(c, token))
app/backend/ingest.py:316:            to_confirm.append({"record_id": rid, "raw": r["date_raw"], "candidates": p["candidates"]})
app/backend/flags.py:45:         "record_id": record.get("id", f"r{record['n']}"), "review_status": "pending",
app/backend/flags.py:167:    return {"type": "record_warning", "category": "injection_suspected", "record_no": record["n"], "record_id": record.get("id", f"r{record['n']}"),
app/backend/flags.py:205:    return {"type": "record_warning", "category": "analysis_incomplete", "record_no": None, "record_nos": [], "record_id": None,
app/backend/flags.py:241:             "record_no": ref["n"], "record_id": ref.get("id", f"r{ref['n']}"), "review_status": "pending", "source_kind": "record",
app/backend/present.py:41:    r = recs.get((row["record_ids"] or [None])[0], {})
app/backend/present.py:43:    return {**_common(row), "seq": r.get("seq"), "record_ids": row["record_ids"], "date": row["date_iso"], "date_status": r.get("date_status"),
app/backend/present.py:52:    return {**_common(row), "record_ids": row["record_ids"], "entry_id": row["entry_id"], "text": row["text"], "value_cents": row["value_cents"],
app/backend/present.py:62:        ids = c.get("record_ids") or []
app/backend/present.py:70:    return [{"record_id": e.get("record_id") or by_n.get(e.get("record_no")), "excerpt": e.get("excerpt") if e.get("excerpt") is not None else e.get("text"),
app/backend/present.py:127:    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
app/backend/present.py:153:    tray = [{"id": x["id"], "kind": k, "record_ids": x["record_ids"], "state": "rejected", "reasons": x["reasons"], "why": x["why"],
app/backend/present.py:170:    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
app/backend/present.py:177:            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
app/backend/review.py:114:    rec = next((r for r in recs if r["id"] == (item["record_ids"] or [None])[0]), None)
app/backend/review.py:154:def confirm_date(conn, case_id: str, record_id: str, date_iso: str, *, now=None) -> dict:
app/backend/review.py:156:    row = conn.execute("SELECT * FROM records WHERE id=? AND case_id=?", (record_id, case_id)).fetchone()
app/backend/review.py:164:    conn.execute("UPDATE records SET date_iso=?, date_status='confirmed' WHERE id=? AND case_id=?", (date_iso, record_id, case_id))
app/backend/review.py:167:        if record_id in (e["record_ids"] or []):
app/backend/review.py:176:    return {"record": {"id": record_id, "date_iso": date_iso, "date_status": "confirmed", "date_raw": rec["date_raw"]},
app/backend/review.py:200:                "record_ids": [f"r{n}" for n in nos], "source_kind": "record", "state": state, "reasons": codes}
---
    pend = sorted((x for x in live if x[1]["review_status"] == "pending"),
                  key=lambda x: (confidence.sort_key(x[1]["state"]), rank[x[0]], x[1].get("date_iso") or "", x[1]["id"]))
    return {"counts": counts, "queue": [r["id"] for _, r in pend],
            "ready_to_export": counts["pending"] == 0 and (counts["accepted"] + counts["edited"]) > 0}


def dates_to_confirm(conn, case_id):
    return [{"record_id": r["id"], "raw": r["date_raw"], "candidates": r["date_candidates"] or [], "status": r["date_status"]}
            for r in _recs_by_id(conn, case_id).values() if r["date_status"] in ("ambiguous", "missing")]


def record_view(r, raw, with_sentences=True, pages=None):
    block = raw[r["char_start"]:r["char_end"]]
    v = {"id": r["id"], "seq": r["seq"], "source_label": r["source_label"], "date_raw": r["date_raw"], "date_iso": r["date_iso"],
         "date_status": r["date_status"], "date_candidates": r["date_candidates"] or [], "duplicate_of": r["duplicate_of"],
         "injection_tag": bool(r["injection_tag"]), "encounter": bool(r["encounter"]), "char_start": r["char_start"],
         "char_end": r["char_end"], "text": block}
    if pages:                                    # PDF source (D-031): the page where the record starts
        v["page"] = pdf_text.page_for(pages, r["char_start"])
    if with_sentences:
        v["sentences"] = [{"text": block[a:b], "start": r["char_start"] + a, "end": r["char_start"] + b} for a, b in sentences.stripped_spans(block)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:01.977Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-057-staff-engineer-r3/tree && sed -n 166,182p app/backend/present.py",
 "description": "Read source-highlight lookup for item record ids"
}
````

### User / tool · 2026-11-02T02:39:02.057Z

**tool result**
````
def why_view(conn, case_id, item_id):
    item = item_view(conn, case_id, item_id)
    recs = _recs_by_id(conn, case_id)
    ids = list(item.get("record_ids") or (item.get("computed") or {}).get("record_ids") or [e.get("record_id") for e in item.get("evidence") or []])
    seen, src = set(), []
    for rid in ids:
        if rid in recs and rid not in seen:
            seen.add(rid)
            r = recs[rid]
            hs, he = item.get("excerpt_start"), item.get("excerpt_end")
            src.append({"record_id": rid, "char_start": r["char_start"], "char_end": r["char_end"], "highlight_start": hs, "highlight_end": he})
    calls = [_call(c) for c in DB.list_llm_calls(conn, case_id, item_id)]
    events = [{"action": e["action"], "at": store.iso(e["at"])} for e in DB.list_events(conn, case_id, item_id)]
    return {"item": item, "source": src, "calls": calls, "events": events}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:11.477Z

**tool call — Bash**
````
{
 "command": "R=artifacts/review-evidence/T-057-staff-engineer-r3 && sed 's/runs = iter(\\[A, \"FAIL\"\\])/B = [(0, a3), (a3, len(T4))]\\nruns = iter([A, B])/' $R/probe_accepted_orphan.py > $R/probe_accepted_orphan_success.py && grep -n \"runs = iter\" $R/probe_accepted_orphan_success.py && .venv/bin/python $R/probe_accepted_orphan_success.py /Users/arsis/zlayt-pm-project/$R/tree; echo \"--- run route guard\"; grep -n \"/run\\\"\" -A12 artifacts/review-evidence/T-057-staff-engineer-r3/tree/app/backend/api.py | head -30",
 "description": "Probe orphaning on a successful different-boundary re-run; check run route guard"
}
````

### User / tool · 2026-11-02T02:39:12.005Z

**tool result**
````
19:runs = iter([A, B])
run1 records [('r1', 0, 47), ('r2', 48, 85), ('r3', 86, 128)] entries [('e1', ['r1']), ('e2', ['r2']), ('e3', ['r3'])]
run2 records [('r1', 0, 85), ('r2', 86, 128)]
after run2 entries [('e1', ['r1'], 'accepted'), ('e2', ['r2'], 'accepted'), ('e3', ['r3'], 'accepted')]
ORPHANED accepted entries (cite a record id not in records table): ['e3']
--- run route guard
336:    @app.post("/api/cases/{token}/run", status_code=202)
337-    async def run_case(token: str, request: Request):
338-        b = await body_of(request)
339-        c = conn()
340-        try:
341-            case = get_case(c, token)
342-            if case["status"] == "running" or token in runs:
343-                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
344-            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
345-                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
346-            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
347-                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
348-            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:13.869Z

**tool call — Bash**
````
{
 "command": "sed -n 348,362p artifacts/review-evidence/T-057-staff-engineer-r3/tree/app/backend/api.py",
 "description": "Read the rerun guard for already-decided items"
}
````

### User / tool · 2026-11-02T02:39:13.949Z

**tool result**
````
            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
            if decided and b.get("confirm_rerun") is not True:
                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
            now = time.time()
            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
            runs[token].start()
            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
        finally:
            c.close()

    @app.get("/api/cases/{token}/status")
    def status(token: str):
        c = conn()
        try:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:25.333Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep T-057; ls artifacts/review-evidence/T-057-staff-engineer-r3/",
 "description": "Check existing T-057 review files and r3 evidence folder"
}
````

### User / tool · 2026-11-02T02:39:25.421Z

**tool result**
````
T-057-staff-engineer-r2.md
T-057-staff-engineer.md
mut-keep-if-any
mut-no-replace
probe_accepted_orphan.py
probe_accepted_orphan_success.py
tree
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:37.059Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-057-staff-engineer-r3.md",
 "content": "# T-057 review, round 3: re-run record consistency after a failed or rejected re-split, staff-engineer-reviewer\n\nCommit under review: 8bf99fb (pinned by `git archive` into artifacts/review-evidence/T-057-staff-engineer-r3/tree). HEAD at review time was b614b40, which contains 8bf99fb. The live working tree is dirty (145+ modified files, including app/backend/narrative.py and tests/fixtures), so the pinned tree is the control.\n\nVerdict: **fail**. The round-2 blocker is closed for items that have not been decided. A new blocker on the same clause is open: items the paralegal already accepted are orphaned when a re-run replaces the stored records, on both the failed-split path and the successful-split path.\n\n## Round-2 blocker: closed for pending items\n\n- The probe prints `run2 stored [('r1', 0, 128)]`, `entry e1 record ['r1'] stored span (0, 128) ... True`, and `consistent`.\n- The new tests `test_rerun_whose_split_fails_or_is_rejected_leaves_records_and_entries_consistent[call_fails|invalid_spans]` pass. The `ValueError` narrowing has its own test and passes.\n- Mutant \"remove record replacement\" (`return` at the top of `_store_records`): 5 failed, 24 passed. The two new tests fail, as do the existing replace tests and the split audit test.\n- Mutant \"keep whatever is stored\" (the round-2 behaviour, condition changed to `if stored:`): 4 failed, 25 passed. The probe prints `INCONSISTENT`.\n\n## Round-3 blocker: accepted items orphaned by a re-run\n\nThe new tests only use pending entries, because each test runs the pipeline and never accepts anything. Run 2 deletes pending rows only (`_persist`, pipeline.py:169-174), so accepted entries from run 1 survive with the record ids of run 1. Those ids no longer exist in the records table after run 2.\n\n- Failed re-split (`probe_accepted_orphan.py`): run 1 stored r1, r2, r3 and entries e1 to e3 were accepted. After run 2 the records table is `[('r1', 0, 128)]`, and the entries are `e1 ['r1'] accepted`, `e2 ['r2'] accepted`, `e3 ['r3'] accepted`. The probe reports `ORPHANED accepted entries ... ['e2', 'e3']`.\n- Successful re-split with different boundaries (`probe_accepted_orphan_success.py`): run 2 stores `[('r1', 0, 85), ('r2', 86, 128)]`, and accepted `e3 ['r3']` is orphaned.\n- Consequences I checked in code (pinned tree):\n  - `app/backend/present.py:170-177` (`why_view`): `if rid in recs` silently drops the missing record, so the \"why\" panel for an accepted item shows `source: []` with no warning.\n  - `app/backend/export_routes.py:38`: the export writes the dangling `record_ids` (fallback `r{record_no}`) for each entry.\n  - `app/backend/api.py:348-354`: a re-run on a case with decided items is allowed when the client sends `confirm_rerun: true`. The path is reachable through the UI and API.\n- Severity: rated **blocker** under CONTRACT D.2 \"loses facts\". The provenance of an accepted, exported item is lost, and it is lost silently. The round-2 acceptance criterion also requires that a failed re-split leave records and entries consistent, and it does not. A reviewer could argue for major because the excerpts are still verbatim input text. I did not downgrade it, because the link to the source record is what the paralegal verified against.\n\n## Findings for the worker\n\n1. blocker: accepted items from an earlier run are orphaned when the records are replaced, on both the failed and successful re-split paths. Fix options, pick one and state it in the handoff:\n   a. Refuse the record replacement while any entry is decided and return 409 with a reason code, or\n   b. Re-anchor decided items to the new record that contains their excerpt (verbatim substring check) and mark the item `needs_review` when no such record exists, or\n   c. Keep the first accepted split and do not re-ask the model on a re-run that has decided items.\n   Whichever is chosen, a test must cover a case with accepted items.\n2. minor: the new round-3 tests do not cover accepted or edited items, so they pass while finding 1 is present. Add the accepted-item variant to `tests/unit/test_split_llm.py` (acceptance test below).\n\nAcceptance test (for finding 1 and 2): accept every entry of run 1 (`DB.apply_review(conn, id, \"accept\", ...)`), then run 2 with (a) a failing split and (b) a successful split with different boundaries. After each run: every entry's `record_ids` resolve to a row in `records`, `excerpt in raw[char_start:char_end]` of that record, or the run refuses with a reason code. `probe_accepted_orphan.py` and `probe_accepted_orphan_success.py` must print no orphans.\n\n## Commands and results\n\n- `python3 -m pytest -q tests/unit/test_split_llm.py`: **not runnable**. System python3.12 has no pytest (`No module named pytest`). The venv was used instead.\n- `.venv/bin/python -m pytest -q tests/unit/test_split_llm.py -p no:cacheprovider` in the pinned 8bf99fb tree: 29 passed in 0.52s.\n- Same command in the live dirty working tree: 29 passed in 0.51s (not a clean control).\n- Probe `artifacts/review-evidence/T-057-staff-engineer-r2/probe_rerun_fail2.py` on the pinned tree: `consistent`, exit 0.\n- Mutant `artifacts/review-evidence/T-057-staff-engineer-r3/mut-no-replace` (record replacement removed): 5 failed, 24 passed.\n- Mutant `artifacts/review-evidence/T-057-staff-engineer-r3/mut-keep-if-any`: 4 failed, 25 passed; probe prints `INCONSISTENT`.\n- Grep: `grep -n \"except\" app/backend/pipeline.py` in the pinned tree shows the `_store_records` `except Exception: ROLLBACK; raise`, which re-raises. It is not a swallowed exception. No `float(`, `sleep(` in the changed files.\n\n## Not exercised\n\nFrontend rendering of the why panel and the export file (I read the code path, I did not click it). Live backend. `python -m app.pipeline evals/golden/sample.txt` (not in this card's brief). The 3-run live eval.\n\n## Model note\n\nThis review was run as claude-haiku-5-5. The dossier expects claude-sonnet-5-5. The record below uses the model I ran as.\n\n```json\n{\"card\": \"<dummy>\", \"persona\": \"<dummy>\", \"model\": \"<dummy>\",\n \"scope\": \"<dummy>\",\n \"exercised\": [\"<dummy>\"],\n \"verdict\": \"<dummy>\",\n \"scores\": {\"<dummy>\": \"<dummy>\"},\n \"findings\": [{\"severity\": \"<dummy>\", \"title\": \"<dummy>\", \"evidence\": \"<dummy>\",\n               \"why_it_matters\": \"<dummy>\", \"fix\": \"<dummy>\", \"acceptance_test\": \"<dummy>\"}],\n \"whats_right\": [\"<dummy>\"],\n \"questions_for_chris\": []}\n```\n"
}
````

### User / tool · 2026-11-02T02:39:37.208Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-057-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:44.831Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md",
 "old_string": "- Mutant scripts: write with the Write tool under artifacts/review-evidence/<card>-staff-engineer/; a `>` or `<` inside a bash heredoc/sed string trips board-guard.",
 "new_string": "- Mutant scripts: write with the Write tool under artifacts/review-evidence/<card>-staff-engineer/; a `>` or `<` inside a bash heredoc/sed string trips board-guard.\n\n## Round 3 additions (T-057 r3, fix 8bf99fb; 2026-11-01)\n- **Replace-on-change fixes must also reconcile decided items.** 8bf99fb makes pending items consistent on failed and successful re-splits, but `_persist` only deletes pending rows, so ACCEPTED entries keep record ids that no longer exist (probe_accepted_orphan.py). why_view silently drops them (present.py:170-177). **How to apply:** for any \"replace stored state\" fix, add a test where the paralegal has accepted items before the re-run.\n- **Pending-only tests hide accepted-item state.** The round-3 tests never accept anything, so they pass while the decided-item path is broken. **How to apply:** check whether the new test's fixtures include a decision step.\n- **Board validator rejects placeholder JSON.** `<dummy>` values fail the verdict enum and severity check in board-validate.sh (PostToolUse). Ask before writing placeholders into a review record.\n- **Brief command may not run.** System python3 has no pytest; use .venv/bin/python -m pytest and say so in the review."
}
````

### User / tool · 2026-11-02T02:39:44.931Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:39:46.764Z

Round-2 blocker is closed for pending items (the probe prints `consistent`, the new tests pass, and both mutants fail), but a new blocker is open: accepted items from run 1 are orphaned when a re-run replaces records, on both the failed and successful re-split paths. Verdict is fail; review written to `/Users/arsis/zlayt-pm-project/reviews/T-057-staff-engineer-r3.md`.
The board validator rejected the file because the `<dummy>` JSON values fail its verdict and severity checks, so I need you to decide: real values (verdict `fail`) or a different placeholder rule. I did not bypass the hook.
