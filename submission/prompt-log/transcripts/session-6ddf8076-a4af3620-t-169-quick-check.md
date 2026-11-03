# Subagent: T-169 quick check (T-169 quick check)

Source: `agent-a4af36208a7df48ca.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T16:56:51.595Z

Review board card T-169 (commit 5ed37ad, test-only) in /Users/arsis/zlayt-pm-project; read it with `python3 tools/board.py show T-169`.

In a fresh `git clone` of the repo in your scratchpad:
- the calibration header test accepts a live claude-cli header with a clean source commit, and still fails on a dirty-tree header (prove it by editing a copy of the file);
- the exact-regeneration test is skipped for a live header, with a written reason, and still runs for a fixture header;
- tests/unit/test_eval_runner.py passes.

Apply the verdict rule exactly: blocker means fail, major means changes, otherwise pass. Write reviews/T-169-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings, exercised. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:56:53.338Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T16:56:53.347Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T16:56:53.628Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-169",
 "description": "Show board card T-169"
}
````

### User / tool · 2026-11-02T16:56:53.762Z

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
updated_at: "2026-11-02T16:56:48Z"
claimed_by: "qa"
claimed_at: "2026-11-02T16:51:49Z"
rounds: 0
commits: ["5ed37ad"]
reviews: []
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

## Handoff
Changed: tests/unit/test_eval_runner.py only (commit 5ed37ad). Header check accepts backend in (fixture, claude-cli); clean source_tree still required; added dirty-header negative test. Exact-regeneration test now skips when committed backend is live (cannot regenerate a paid non-deterministic live run offline; the source-commit/ancestor/clean-tree tests still run). Verified: tests/unit/test_eval_runner.py 108 passed 1 skipped in repo; fresh git clone in scratchpad 21 passed 1 skipped. Left: nothing in scope. Surprised: the regen test (not just the header test) also failed on the live header; skip is a scope decision for orchestrator to confirm.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:56:54.137Z

**tool call — Bash**
````
{
 "command": "git rev-parse --is-inside-work-tree 2>/dev/null; git log --oneline -3 5ed37ad; git show --stat 5ed37ad | head -40",
 "description": "Check repo state and inspect commit 5ed37ad"
}
````

### User / tool · 2026-11-02T16:56:54.269Z

**tool result**
````
true
5ed37ad test(qa): accept live claude-cli calibration header; keep clean-tree check (T-169)
56004f0 fix(backend): T-168 r2 the closing-object JSON read is opt-in and extract-only; every judge (j1-j4) and other step parses strictly, two objects in a reply is INVALID_JSON
7cfdb0b test(qa): M2 re-gate live evidence: claude-cli 3-run at 312efe6 clean, ship_bar_met True, controls gate included, live calibration regenerated, letter_check 0
commit 5ed37ad12a177c34c1a6c8af6ba88fc4f4b61c4b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 10:56:02 2026 -0600

    test(qa): accept live claude-cli calibration header; keep clean-tree check (T-169)
    
    - header check accepts backend in (fixture, claude-cli); clean source_tree still required
    - negative test: a dirty-tree header fails the header check for both backends
    - exact-regeneration test skips for a live committed backend (not reproducible offline)
    
    Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>

 tests/unit/test_eval_runner.py | 30 +++++++++++++++++++++++++++---
 1 file changed, 27 insertions(+), 3 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:56:54.498Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ | head -100",
 "description": "List reviewer memory directory"
}
````

### User / tool · 2026-11-02T16:56:54.580Z

**tool result**
````
MEMORY.md
feedback_differential_probe_prior_build.md
feedback_evidence_sha_vs_commit.md
feedback_exact_count_vs_presence.md
feedback_fake_script_keys.md
feedback_frontend_text_coupling.md
feedback_regex_multiline_probe.md
feedback_review_write_once.md
feedback_reviewer_scratch_writes.md
feedback_severity_vs_brief.md
feedback_shared_scratchpad.md
feedback_swallow_needs_render_marker.md
feedback_verify_pid_before_kill.md
feedback_watcher_blind_to_render_errors.md
project_backend_llm_review_patterns.md
project_db_review_patterns.md
project_design_review_patterns.md
project_e2e_contract_review_patterns.md
project_eval_runner_review_patterns.md
project_gate_m2_patterns.md
project_gate_m2_r2_patterns.md
project_harness_review_patterns.md
project_llm_stage_review_patterns.md
project_r2_fix_verification_patterns.md
project_round2_snapshot_review_patterns.md
project_split_llm_review_patterns.md
project_t050_namespacing_review_patterns.md
project_t063_doc_vs_code_review_patterns.md
project_t065_batch_fallback_review_patterns.md
project_t066_no_model_reason_patterns.md
project_t067_r6_d043_patterns.md
project_t070_t067_review_patterns.md
project_t073_t084_review_patterns.md
project_t075_determinism_review_patterns.md
project_t080_trace_review_patterns.md
project_t083_billing_review_patterns.md
project_t083_r4_accounting_patterns.md
project_t083_r5_cross_family_patterns.md
project_t088_t089_review_patterns.md
project_t090_calibration_review_patterns.md
project_t093_signature_controls_patterns.md
project_t095_head_revert_patterns.md
project_t098_r2_review_patterns.md
project_t098_r3_review_patterns.md
project_t098_t099_review_patterns.md
project_t100_d047_review_patterns.md
project_t100_r2_patterns.md
project_t101_calibration_guard_patterns.md
project_t102_stale_calibration_patterns.md
project_t103_listing_review_patterns.md
project_t106_r2_audit_patterns.md
project_t106_review_patterns.md
project_t108_quote_units_patterns.md
project_t109_doc_vs_code_patterns.md
project_t112_trim_patterns.md
project_t113_r2_patterns.md
project_t113_t122_patterns.md
project_t115_e2e_curated_patterns.md
project_t119_keyboard_coverage_patterns.md
project_t120_r3_patterns.md
project_t120_t121_t105_patterns.md
project_t128_t129_r2_patterns.md
project_t128_t129_t127_patterns.md
project_t132_r4_patterns.md
project_t132_r5_patterns.md
project_t132_t128_r2r3_patterns.md
project_t133_lexicon_review_patterns.md
project_t133_r3_patterns.md
project_t133_r4_patterns.md
project_t133_r5_patterns.md
project_t134_r3_t138_patterns.md
project_t134_r4_t138_r2_patterns.md
project_t134_unconfirmed_edit_patterns.md
project_t136_r2_patterns.md
project_t140_r2_patterns.md
project_t140_r3_t152_r2_patterns.md
project_t141_r2_patterns.md
project_t141_r3_patterns.md
project_t141_r4_patterns.md
project_t141_r5_patterns.md
project_t141_r6_patterns.md
project_t141_r7_patterns.md
project_t141_r8_patterns.md
project_t145_t146_patterns.md
project_t146_r2_patterns.md
project_t146_r3_patterns.md
project_t146_r4_patterns.md
project_t152_golden_claim_patterns.md
project_t155_e2e_triage_patterns.md
project_t155_r2_t164_patterns.md
project_t157_case_title_next_action_patterns.md
project_t158_settle_patterns.md
project_t159_t161_r2_patterns.md
project_t160_budget_placement_patterns.md
project_t162_rerun_note_patterns.md
project_t165_r2_patterns.md
project_t167_plain_wording_patterns.md
project_t168_parser_patterns.md
project_wiring_review_patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:56:59.477Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && for f in feedback_reviewer_scratch_writes.md feedback_shared_scratchpad.md feedback_evidence_sha_vs_commit.md feedback_review_write_once.md project_eval_runner_review_patterns.md project_t090_calibration_review_patterns.md project_gate_m2_r2_patterns.md project_t101_calibration_guard_patterns.md; do echo \"=== $f\"; cat \"$f\"; echo; done",
 "description": "Read relevant reviewer memory files"
}
````

### User / tool · 2026-11-02T16:56:59.568Z

**tool result**
````
=== feedback_reviewer_scratch_writes.md
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

=== feedback_shared_scratchpad.md
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

=== feedback_evidence_sha_vs_commit.md
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

=== feedback_review_write_once.md
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

=== project_eval_runner_review_patterns.md
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

=== project_t090_calibration_review_patterns.md
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

=== project_gate_m2_r2_patterns.md
---
name: gate-m2-r2-staff-engineer-patterns
description: GATE-M2 round 2 staff review at 7cfdb0b (changes): round-1 blocker and majors fixed; unit suite red (live calibration.json vs fixture-pinned guards, undeclared e2e test ids); check-fresh still rc 1
metadata:
  type: project
---

GATE-M2 r2 at 7cfdb0b verdict changes (0 blockers, 1 major, 3 minors). File: reviews/GATE-M2-r2-staff-engineer.md.

- Round-1 fixes hold: deadline at extract/verify -> entries needs_review, judge unavailable, batch accept refused; re-run with deadline at any of 7 stages loses nothing (decided, hand entry); gate.ready == export 20/20 on sample + lib01/03/11. Mutants (_mark_judge_not_run, _keep_hand_entry) killed.
- Major: unit suite red at the gate commit. 7cfdb0b committed a live claude-cli calibration.json; test_eval_runner header test pins backend == fixture (T-169 covers only that) and `regenerates_exactly_from_its_source_commit` also fails but ONLY in a clone with .git (skipped in a git archive). **How to apply:** run the unit suite in a `git clone` checkout, not only an archive, or git-dependent guards are skipped; a "relax the assertion" fix for a guard can leave its sibling red.
- test_e2e_contract: e2e specs use test ids (do-first-item, btn-new-case, cases-keys) not declared in tests/e2e/conftest.py docstring after a frontend commit.
- check-fresh reads committed latest.json (old fixture run), so rc=1 even when the dated live .md and calibration.json hashes equal HEAD; compare the md hash list to evals.run.hashes() to prove freshness.
- T-168 `_closing_object` in app/llm/_types.py (parse_json_reply accepts a reply whose last JSON object runs to end of text) landed after the live run's source commit 312efe6.
- eval run writes its report into the scratch outdir when run from the archive; the real repo's untracked evals/reports files are other agents'.

=== project_t101_calibration_guard_patterns.md
---
name: t101-calibration-guard-patterns
description: T-101 r1 (4c5f9bf) changes and r2 (fdc2506) pass: untracked-input guard tested only for golden, recheck test passes via backstop, app/fixtures mutants survive, run-then-write refused by latest.json
metadata:
  type: project
---

T-101 r2 (commit fdc2506; review reviews/T-101-staff-engineer-r2.md): pass, 0 blockers, 0 majors, 3 minors, 1 nit. Mutants: 8 of 12 killed; survivors M5 (main recheck, backstop covers), M7/M8 (app and fixtures untested), M11 (equivalent for git_source outputs).
- Confirmed in r2: untracked refusal for evals/golden, app, prompts, fixtures (probes); plain/live/no-git runs leave the committed sha alone; HEAD file is 172028c's, sha 49d383b5, working tree equal; 129 passed in clone and project tree.
- Still open from r1 F5: a plain run rewrites tracked latest.json, so the next --write-calibration is refused (names the path now).
- r1 F6 correction: the `clean is None` clause is unreachable from git_source; my r1 "wrong reason" claim only held for an input git_source never returns. Lesson: check the reachability of an input before calling a survivor real.
- Harness: git-guard blocked `git add -A`, `xargs git add` and a subagent `git commit` even in a scratch repo, so a git-init archive could not be committed; `git clone --no-hardlinks` plus `checkout --detach <sha>` kept the sha and worked.

T-101 r1 (commit 4c5f9bf; review reviews/T-101-staff-engineer.md): changes, 0 blockers, 2 majors, 5 minors, 1 nit. Mutants M1-M7 killed, M8 (no-git clause) survived.

- **Clean check ignores untracked inputs, so the header lies.** `git status --porcelain --untracked-files=no` lets an untracked golden case change the counts while the header says source_tree_clean true at the HEAD tree (which does not contain the case). Repro script: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh. Plain runs also leave untracked reports under evals/reports, so the fix must exclude that dir, not all untracked files.
- **Shared tree is not HEAD.** After 4c5f9bf, the project working-tree evals/reports/calibration.json was rewritten by a claude-cli run (header backend claude-cli, clean false). Project pytest then showed 2 failed; the same selection at HEAD in a clone showed 124 passed. HEAD code cannot write a clean=false header (both guards refuse), so the writer ran other code. Check `git status -- <served file>` and the header before citing project-tree test results.
- **Flag combinations.** `--write-calibration --controls` returns before the write and says nothing.
- **Scratch dir mismatch.** The calibration scratch dir is named from generated_at, the run artifacts from the main ts; for live runs they differ by the run length (observed 38 s).
- **Refusal text.** It does not name the dirty files; a plain run rewrites tracked latest.json, so a write right after a run is refused.
- **Survivor pattern.** Dropping the `or ... clean is None` clause keeps rc 2 (the `not None` branch refuses too) but gives the wrong reason; the test only asserts `is not None`. Assert the reason text.

**Why:** the card's AC was met literally, so the findings are about what the header claims and what the served file contains, not the AC wording.
**How to apply:** for any "write only from clean" guard, (1) add an untracked input and check the header, (2) check the served file in the working tree against HEAD before trusting project-tree test output, (3) mutate the refusal and assert its reason text.

Related: [[project_t090_calibration_review_patterns]] (provenance header history), [[project_eval_runner_review_patterns]] (scratch-copy method, git archive pinning).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:01.862Z

Memory notes that the regen test and dirty-tree guards are git-dependent, so I'll run in a real clone. Next I'll read the commit diff and set up the clone.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:02.311Z

**tool call — Bash**
````
{
 "command": "git show 5ed37ad -- tests/unit/test_eval_runner.py",
 "description": "Show the diff of commit 5ed37ad"
}
````

### User / tool · 2026-11-02T16:57:02.401Z

**tool result**
````
commit 5ed37ad12a177c34c1a6c8af6ba88fc4f4b61c4b
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 10:56:02 2026 -0600

    test(qa): accept live claude-cli calibration header; keep clean-tree check (T-169)
    
    - header check accepts backend in (fixture, claude-cli); clean source_tree still required
    - negative test: a dirty-tree header fails the header check for both backends
    - exact-regeneration test skips for a live committed backend (not reproducible offline)
    
    Co-Authored-By: Claude Haiku 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index 6504858..eb93b68 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -796,12 +796,32 @@ def _require_source_commit(c):
     assert _git("cat-file", "-e", c["source_commit"] + "^{commit}").returncode == 0, f"source_commit {c['source_commit']} does not exist in this repository"
 
 
-def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
-    c = _committed()
-    assert c["backend"] == "fixture" and re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
+CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
+
+
+def _assert_calibration_header(c):
+    assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
+    assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
     assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")
 
 
+def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
+    _assert_calibration_header(_committed())
+
+
+def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
+    """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
+    for backend in CAL_BACKENDS:
+        dirty = _committed()
+        dirty["backend"], dirty["source_tree_clean"] = backend, False
+        p = tmp_path / f"dirty_{backend}.json"
+        p.write_text(json.dumps(dirty))
+        monkeypatch.setattr(sys.modules[__name__], "CAL", p)
+        with pytest.raises(AssertionError):
+            _assert_calibration_header(_committed())
+        monkeypatch.undo()
+
+
 def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
     c = _committed()
     _require_source_commit(c)
@@ -827,6 +847,10 @@ def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_pa
     (the export has no .git; those are checked against git itself in the header and ancestor tests)."""
     c = _committed()
     _require_source_commit(c)
+    if c["backend"] != "fixture":
+        # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
+        # ancestor and clean-tree tests plus the live report it cites; this exact-regeneration check only covers the fixture backend.
+        pytest.skip(f"committed calibration is a live {c['backend']} measurement; exact regeneration needs the live backend")
     src = tmp_path / "src"
     src.mkdir()
     tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:07.476Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la \"$SCR\" | head -30; echo \"---\"; ls -d \"$SCR\"/T169* 2>/dev/null; echo \"exit=$?\"",
 "description": "Check scratchpad for existing T169 directories"
}
````

### User / tool · 2026-11-02T16:57:07.723Z

**tool result**
````
total 390808
drwx------@ 1629 arsis  wheel    52128 Nov  2 10:56 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
drwxr-xr-x@    6 arsis  wheel      192 Nov  2 08:00 .pytest_cache
-rw-r--r--@    1 arsis  wheel      247 Nov  2 10:21 .t165dir
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
-rw-r--r--@    1 arsis  wheel     6786 Nov  2 07:36 CLAUDE.md
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
-rw-r--r--@    1 arsis  wheel    83742 Nov  2 07:36 MASTER_PROMPT.md
-rw-r--r--@    1 arsis  wheel     2046 Nov  1 19:21 T-047-run1.json
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 04:04 T-060-pass2-head
drwxr-xr-x@   23 arsis  wheel      736 Nov  2 00:41 T-093-r3-2ab7896
-rw-r--r--@    1 arsis  wheel    74715 Nov  2 00:41 T-093-r3-run.py.orig
drwxr-xr-x@    3 arsis  wheel       96 Nov  2 00:41 T-093-r3-scripts
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:13 T-093-r4-3223e50
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:15 T-093-r4-mutA
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 03:15 T-093-r4-mutB
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 00:42 T-109-probe
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:36 T-109-r1-card
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:36 T-109-r1-head
-rw-r--r--@    1 arsis  wheel     2531 Nov  2 00:40 T-109-unit-head.txt
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-head
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-mut2
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 05:07 T-124-r1-parent
---
exit=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:10.229Z

The scratchpad is shared, so I'll use a unique subdirectory and clone in the foreground.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:12.345Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git merge-base --is-ancestor 5ed37ad HEAD && echo \"5ed37ad is ancestor of HEAD\" ; git status --porcelain -- tests/unit/test_eval_runner.py evals/reports | head; echo \"---\"; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR/T169_staff_r1\" && git clone --no-hardlinks -q /Users/arsis/zlayt-pm-project \"$SCR/T169_staff_r1/clone\" && cd \"$SCR/T169_staff_r1/clone\" && git checkout -q --detach 5ed37ad && git rev-parse HEAD && git status --porcelain | head -5; echo \"clean-check-rc=$?\"; ls evals/reports | head -20",
 "description": "Clone repo into scratchpad and detach at 5ed37ad"
}
````

### User / tool · 2026-11-02T16:57:14.357Z

**tool result**
````
8398bee
5ed37ad is ancestor of HEAD
 M evals/reports/latest.json
?? evals/reports/20261102T023155Z.md
?? evals/reports/20261102T023203Z.md
?? evals/reports/20261102T023204Z.md
?? evals/reports/20261102T023208Z.md
?? evals/reports/20261102T023603Z.md
?? evals/reports/20261102T023911Z.md
?? evals/reports/20261102T023916Z.md
?? evals/reports/20261102T024348Z.md
?? evals/reports/20261102T024355Z.md
---
5ed37ad12a177c34c1a6c8af6ba88fc4f4b61c4b
clean-check-rc=0
20261102T020824Z.md
20261102T020933Z.md
20261102T021029Z.md
20261102T021046Z.md
20261102T022701Z.md
20261102T022927Z.md
20261102T023039Z.md
20261102T025219Z.md
20261102T025715Z.md
20261102T032823Z.md
20261102T035750Z.md
20261102T040933Z.md
20261102T081339Z.md
20261102T083252Z.md
20261102T085207Z.md
20261102T095640Z.md
20261102T104043Z.md
20261102T111004Z.md
20261102T113305Z.md
20261102T115041Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:17.403Z

The clone is at 5ed37ad. The project tree's HEAD has moved to 8398bee, so I'll cite 5ed37ad as the reviewed commit. Next I'll run the target test file in the clone and check the interpreter.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:57:19.012Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; ls -la /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1 | head -2; cd \"$SCR\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_eval_runner.py -q -rs 2>&1 | tail -30",
 "description": "Run test_eval_runner.py in the fresh clone at 5ed37ad"
}
````

### User / tool · 2026-11-02T16:57:52.776Z

**tool result**
````
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 /Users/arsis/zlayt-pm-project/.venv/bin/python -> python3.12
........................................................................ [ 66%]
......................s..............                                    [100%]
=========================== short test summary info ============================
SKIPPED [1] tests/unit/test_eval_runner.py:853: committed calibration is a live claude-cli measurement; exact regeneration needs the live backend
108 passed, 1 skipped in 33.46s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:08.610Z

The clone run gives 108 passed and 1 skipped at 5ed37ad. Next I'll read the test code paths I need to exercise, the calibration header, and the surrounding helpers.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:10.198Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && grep -n \"^CAL\\|def _committed\\|CAL =\\|CAL)\\|def _git\\|def _require_source_commit\\|^import\\|^from\\|R = \\|R\\.ROOT\" tests/unit/test_eval_runner.py | head -40; echo ---; sed -n 780,900p tests/unit/test_eval_runner.py",
 "description": "Read calibration test helpers and regen test in clone"
}
````

### User / tool · 2026-11-02T16:58:10.318Z

**tool result**
````
3:import copy, json, re
4:import pytest
5:from evals import run as R
6:from tests.unit import _golden as G
289:    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "curated"))
291:    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "recorded"))
775:import os, shutil, subprocess, sys
776:CAL = R.REPORTS / "calibration.json"
779:def _git(*a, cwd=None):
780:    return subprocess.run(["git", *a], cwd=cwd or R.ROOT, capture_output=True, text=True)
783:def _committed():
791:def _require_source_commit(c):
799:CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
856:    tar = subprocess.run(["git", "archive", c["source_commit"]], cwd=R.ROOT, capture_output=True, check=True).stdout
878:        if (R.ROOT / d).is_dir():
879:            shutil.copytree(R.ROOT / d, src / d, ignore=shutil.ignore_patterns(".git", "__pycache__", "runs"))
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
    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")


def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    _assert_calibration_header(_committed())


def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
    """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
    for backend in CAL_BACKENDS:
        dirty = _committed()
        dirty["backend"], dirty["source_tree_clean"] = backend, False
        p = tmp_path / f"dirty_{backend}.json"
        p.write_text(json.dumps(dirty))
        monkeypatch.setattr(sys.modules[__name__], "CAL", p)
        with pytest.raises(AssertionError):
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
    if c["backend"] != "fixture":
        # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
        # ancestor and clean-tree tests plus the live report it cites; this exact-regeneration check only covers the fixture backend.
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
    assert c["source_tree_clean"] is True


def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
    """T-101 AC2 end to end: a copy of the tree with no .git exits 2 with a clear message before any run and writes nothing. The copy is made with
    shutil (not `git archive`), so the test also runs inside an export of HEAD that has no .git itself (T-106)."""
    src = tmp_path / "src"
    for d in ("app", "evals", "spec"):
        if (R.ROOT / d).is_dir():
            shutil.copytree(R.ROOT / d, src / d, ignore=shutil.ignore_patterns(".git", "__pycache__", "runs"))
    assert not (src / ".git").exists()
    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
    env["PYTHONPATH"] = str(src)
    out = tmp_path / "out"
    r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
    assert r.returncode == 2 and "--write-calibration refused" in r.stderr and "no git repository" in r.stderr, r.stderr[-800:]
    assert "Traceback" not in r.stderr
    assert not out.exists() or not any(out.iterdir())


def test_git_source_reports_commit_and_dirtiness(tmp_path):
    if shutil.which("git") is None:
        pytest.skip("git missing")
    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
    (tmp_path / "f").write_text("a")
    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
    a = R.git_source(tmp_path)
    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
    (tmp_path / "f").write_text("b")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:15.523Z

The negative test asserts only `AssertionError` with no match, and the regen skip is keyed on `backend != "fixture"`. Next I'll read the committed calibration header and find out whether any test checks the live report it cites.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:17.721Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nc=json.load(open('evals/reports/calibration.json'))\nprint({k:(v if not isinstance(v,(dict,list)) else type(v).__name__+'[%d]'%len(v)) for k,v in c.items()})\nprint('by_state', c.get('by_state'))\nprint('by_type', c.get('by_type'))\nprint('sentences', c.get('sentences'))\n\"; echo \"--- grep tests for calibration/report cites\"; grep -rn \"calibration\" tests/ --include=*.py | grep -v \"^tests/unit/test_eval_runner.py\" | head -20; echo \"--- in test_eval_runner\"; grep -n \"calibration\\|\\\"report\\\"\\|\\['report'\\]\\|cited\\|\\.md\" tests/unit/test_eval_runner.py | head -60",
 "description": "Inspect committed calibration header and test references"
}
````

### User / tool · 2026-11-02T16:58:17.873Z

**tool result**
````
{'backend': 'claude-cli', 'by_state': 'dict[2]', 'by_type': 'dict[3]', 'case_count': 10, 'cases': 'list[10]', 'generated_at': '2026-11-02T16:40:38Z', 'hashes': 'dict[17]', 'match_rule': 'entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.', 'models': 'dict[2]', 'not_scored': 'dict[4]', 'schema': 'evals.calibration/1', 'sentences': 'dict[2]', 'small_sample': True, 'source': 'evals.run over the golden cases; measured counts only (D-042, scope cut 10)', 'source_commit': '312efe663327539df1b712832e23bf1d2c495d42', 'source_tree': '6b761a5e9e52539270e3c7c20bd68d1f8c0bd45a', 'source_tree_clean': True}
by_state {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_07_prompt_injection', 'case_09_nonvisit_hides_gap', 'sample'], 'matched': 11, 'total': 11}, 'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', 'case_07_prompt_injection', 'case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap', 'sample'], 'matched': 82, 'total': 83}}
by_type {'amount': {'needs_review': {'by_case': {'case_03_rate_and_ocr': [3, 3], 'case_07_prompt_injection': [1, 1], 'sample': [2, 2]}, 'matched': 6, 'total': 6}, 'verified': {'by_case': {'case_01_date_formats': [1, 1], 'case_03_rate_and_ocr': [2, 2], 'case_05_provider_conflict': [1, 1], 'case_07_prompt_injection': [1, 1], 'case_08_diagnosis_temptation': [1, 1], 'case_09_nonvisit_hides_gap': [1, 1], 'sample': [2, 2]}, 'matched': 9, 'total': 9}}, 'entry': {'needs_review': {'by_case': {'case_01_date_formats': [1, 1], 'case_03_rate_and_ocr': [1, 1], 'case_07_prompt_injection': [1, 1], 'case_09_nonvisit_hides_gap': [1, 1]}, 'matched': 4, 'total': 4}, 'verified': {'by_case': {'case_01_date_formats': [7, 7], 'case_02_gap_boundaries': [8, 8], 'case_03_rate_and_ocr': [4, 4], 'case_04_duplicates_no_amounts': [4, 4], 'case_05_provider_conflict': [5, 5], 'case_06_subtle_pre_existing': [4, 5], 'case_07_prompt_injection': [3, 3], 'case_08_diagnosis_temptation': [4, 4], 'case_09_nonvisit_hides_gap': [4, 4], 'sample': [9, 9]}, 'matched': 52, 'total': 53}}, 'flag': {'needs_review': {'by_case': {'case_07_prompt_injection': [1, 1]}, 'matched': 1, 'total': 1}, 'verified': {'by_case': {'case_02_gap_boundaries': [3, 3], 'case_05_provider_conflict': [1, 1], 'case_06_subtle_pre_existing': [4, 4], 'case_07_prompt_injection': [1, 1], 'case_08_diagnosis_temptation': [1, 1], 'case_09_nonvisit_hides_gap': [1, 1], 'sample': [10, 10]}, 'matched': 21, 'total': 21}}}
sentences {'by_type': {'amount': {'needs_review': 'Needs-review amounts matched the record 6/6 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified amounts matched the record 9/9 times in testing on the claude-cli backend (10 golden cases, small sample).'}, 'entry': {'needs_review': 'Needs-review entries matched the record 4/4 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified entries matched the record 52/53 times in testing on the claude-cli backend (10 golden cases, small sample).'}, 'flag': {'needs_review': 'Needs-review flags matched the record 1/1 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified flags matched the record 21/21 times in testing on the claude-cli backend (10 golden cases, small sample).'}}, 'overall': {'needs_review': 'Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).', 'verified': 'Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).'}}
--- grep tests for calibration/report cites
tests/unit/test_t167_plain_wording.py:10:from app.backend import calibration_route, export, narrative, reclassify, trace, why as WHY
tests/unit/test_t167_plain_wording.py:74:    stale = calibration_route.stale_reason({"hashes": {"app/llm/prompts/a.md": "x"}}, {"app/llm/prompts/a.md": "y"})
tests/unit/test_t167_plain_wording.py:75:    assert_plain(stale, "calibration stale reason")
tests/unit/test_t167_plain_wording.py:76:    assert_plain(calibration_route.stale_reason({}, {}), "calibration stale reason (no hashes)")
tests/unit/test_calibration_route.py:1:"""T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct
tests/unit/test_calibration_route.py:2:states; a missing or invalid file gives calibration null and never an invented number. Aggregate counts only, so demo mode is fine.
tests/unit/test_calibration_route.py:12:from app.backend import calibration_route as CR
tests/unit/test_calibration_route.py:17:    """A valid evals.calibration/1 document (one golden case), built the way evals/run.py builds it."""
tests/unit/test_calibration_route.py:29:        "schema": "evals.calibration/1", "backend": "fixture", "case_count": 1, "small_sample": True,
tests/unit/test_calibration_route.py:44:def write(tmp_path, doc, name="calibration.json"):
tests/unit/test_calibration_route.py:61:    c = out["calibration"]
tests/unit/test_calibration_route.py:69:    c = CR.load(write(tmp_path, make()))["calibration"]
tests/unit/test_calibration_route.py:75:    r = bare_client(write(tmp_path, make())).get("/api/calibration")
tests/unit/test_calibration_route.py:78:    assert body["status"] == "ok" and body["calibration"]["source_commit"] == "b85fc1b56386aa0d37460186b5840eec0e578642"
tests/unit/test_calibration_route.py:83:        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
tests/unit/test_calibration_route.py:92:    assert out == {"status": "missing", "calibration": None, "message": CR.MISSING}
tests/unit/test_calibration_route.py:96:    r = bare_client(tmp_path / "nope.json").get("/api/calibration")
tests/unit/test_calibration_route.py:98:    assert r.json() == {"status": "missing", "calibration": None, "message": CR.MISSING}
tests/unit/test_calibration_route.py:107:    "wrong_schema": lambda d: d.update(schema="evals.calibration/2"),
tests/unit/test_calibration_route.py:130:        p = tmp_path / "calibration.json"
--- in test_eval_runner
260:    assert list(tmp_path.glob("2*.md"))
275:    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("a")
279:    (tmp_path / "app" / "llm" / "prompts" / "extract_v1.md").write_text("b")
441:    return R.score_calibration(exp, out)
444:def test_score_calibration_counts_matched_over_seen_per_state_and_type():
459:def test_score_calibration_ignores_rejected_items_and_items_without_a_state():
469:def test_flag_calibration_follows_flag_precision():
480:def test_build_calibration_pools_counts_names_cases_and_flags_small_samples():
481:    res = {"a": {"calibration": {"entry": {"verified": [3, 4], "needs_review": [1, 2]}, "amount": {"verified": [2, 2], "needs_review": [0, 0]},
483:           "b": {"calibration": {"entry": {"verified": [1, 1], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 1]},
485:    c = R.build_calibration(res, "fixture", {"generator": "x"}, "T")
495:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
496:    res = {"a": {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}}
497:    c = R.build_calibration(res, "fixture")
517:    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
519:    few = {"calibration": {**row["calibration"], "entry": {"verified": [0, 0], "needs_review": [1, 2]}}}
520:    c = R.build_calibration({**{f"c{i}": row for i in range(29)}, "few": few}, "claude-cli")
526:    row = {"calibration": {"entry": {"verified": [40, 40], "needs_review": [0, 0]}, "amount": {"verified": [0, 0], "needs_review": [0, 0]},
529:    at29 = R.build_calibration({f"c{i}": row for i in range(29)}, "claude-cli")
530:    at30 = R.build_calibration({f"c{i}": row for i in range(30)}, "claude-cli")
538:    row = {"calibration": {t: {"verified": [1, 2], "needs_review": [1, 1]} for t in R.CAL_TYPES}}
539:    c = R.build_calibration({"a": row}, backend)
543:    empty = R.build_calibration({"a": {"calibration": {}}}, backend)
599:    R.score_calibration(exp, out, un)
601:    c = R.build_calibration({"sample": {"calibration": {t: {"verified": [1, 1], "needs_review": [0, 0]} for t in R.CAL_TYPES}, "calibration_unscored": un}}, "fixture")
606:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
608:    c = rep["calibration"]
610:    assert c["by_state"]["verified"]["total"] == sum(rep["per_case"][n]["calibration"][t]["verified"][1] for n in rep["per_case"] for t in R.CAL_TYPES)
612:    assert "Calibrated confidence" in next((tmp_path / "plain").glob("2*.md")).read_text()
613:    assert json.loads(next((tmp_path / "plain" / "runs").glob("*/calibration.json")).read_text()) == json.loads(json.dumps(c))
614:    clean = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], {"commit": "a" * 40, "clean": True, "tree": "b" * 40}, rep["hashes"])
615:    R.write_report({**rep, "calibration": clean}, tmp_path / "committed", write_calibration=True)     # the header must be a clean commit (T-101 r2)
616:    assert json.loads((tmp_path / "committed" / "calibration.json").read_text()) == json.loads(json.dumps(clean))
619:# ---------------------------------------------------------------- T-101: a plain run never touches the committed calibration.json
627:def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
628:    """T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy."""
629:    committed = tmp_path / "calibration.json"
636:    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
637:    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good["calibration"]))
638:    assert list(tmp_path.glob("2*.md")) and (tmp_path / "latest.json").exists()
641:def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
647:    assert not (tmp_path / "calibration.json").exists()
650:def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
655:        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"],
662:    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
663:    assert not (tmp_path / "calibration.json").exists() and not (tmp_path / "latest.json").exists()
670:def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
671:    """T-101 AC2: --write-calibration exits 2 before the pipeline runs and writes nothing."""
674:        raise AssertionError("the pipeline ran although --write-calibration was refused")
679:    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
683:def test_write_calibration_refusal_rule_is_clean_tree_at_a_commit():
684:    assert R.write_calibration_refusal({"commit": "a" * 40, "clean": True, "tree": "b" * 40}) is None
685:    assert "uncommitted" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40})
686:    assert "no git repository" in R.write_calibration_refusal({"commit": None, "clean": None, "tree": None})   # T-101 r2 F6: the reason, not just a refusal
689:def test_write_calibration_refusal_names_every_dirty_path_it_is_given():
690:    why = R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40,
694:    assert "and 3 more" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40, "dirty": many})
700:    dirty["calibration"] = R.build_calibration(dirty["per_case"], dirty["backend"], dirty["models"], dirty["generated_at"],
703:        R.write_report(dirty, tmp_path, write_calibration=True)
706:    assert not (tmp_path / "plain" / "calibration.json").exists()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:40.051Z

The committed header has no field that cites a live report file. I'll confirm that against git and then run the targeted tests in the clone.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:42.997Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && echo \"== header keys mentioning report/md:\"; grep -o '\"[a-z_]*report[a-z_]*\"\\|[A-Za-z0-9_/.-]*\\.md' evals/reports/calibration.json | sort -u; echo \"(end)\"; echo \"== tracked reports:\"; git ls-files evals/reports | head -40; echo \"== dated report at 16:40 run?\"; ls evals/reports | grep -i \"T164\\|1640\" ; echo \"(end)\"; echo \"== source_commit 312efe6 commit line:\"; git log -1 --format='%h %ad %s' --date=iso 312efe6; echo \"== commits between 312efe6 and 5ed37ad touching backend/llm:\"; git rev-list --count 312efe6..5ed37ad; git log --oneline 312efe6..5ed37ad -- app/llm app/backend/pipeline.py | head",
 "description": "Check whether calibration header cites a live report"
}
````

### User / tool · 2026-11-02T16:58:43.187Z

**tool result**
````
== header keys mentioning report/md:
app/llm/prompts/extract_es_v1.md
app/llm/prompts/extract_v1.md
app/llm/prompts/flags_v1.md
app/llm/prompts/judge_amount_class_v1.md
app/llm/prompts/judge_conflict_v1.md
app/llm/prompts/judge_conflict_v2.md
app/llm/prompts/judge_conflict_v4.md
app/llm/prompts/judge_conflict_v5.md
app/llm/prompts/judge_conflict_v6.md
app/llm/prompts/judge_faithfulness_es_v1.md
app/llm/prompts/judge_faithfulness_v1.md
app/llm/prompts/judge_flag_v1.md
app/llm/prompts/judge_flag_v2.md
app/llm/prompts/judge_flag_v3.md
app/llm/prompts/narrative_v1.md
app/llm/prompts/split_v1.md
(end)
== tracked reports:
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
== dated report at 16:40 run?
20261102T164038Z.md
(end)
== source_commit 312efe6 commit line:
312efe6 2026-11-02 10:13:08 -0600 fix(backend): T-165 a first run where the extract step failed for any record is run_partial naming those records (RUN_FAILED); a record entered by hand is a named ENTERED_BY_HAND warning, and entering the last failed record clears an extract-only failure; a re-run keeps a pending hand-entered entry
== commits between 312efe6 and 5ed37ad touching backend/llm:
7
56004f0 fix(backend): T-168 r2 the closing-object JSON read is opt-in and extract-only; every judge (j1-j4) and other step parses strictly, two objects in a reply is INVALID_JSON
235e135 fix(backend): T-168 lib01 record 3 recorded live (claude-cli): extract + judge 1 answers; a reply that ends with its corrected JSON object is read as that object (earlier draft ignored)
56d746c fix(backend): T-165 r2 a re-run never deletes the paralegal's pending hand entry; when the AI now also has an entry for the record it is kept with a rerun_note and she chooses
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:50.068Z

The header cites no report path. A tracked dated report, `20261102T164038Z.md`, matches the `generated_at` timestamp, so the link is by timestamp only. Next I'll check that report's counts and run the targeted tests in the clone.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:58:53.041Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && grep -n -i \"backend\\|source\\|calibrat\\|82/83\\|11/11\" evals/reports/20261102T164038Z.md | head -20; echo \"== A: header positive (committed live claude-cli)\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_eval_runner.py -v -k \"committed_calibration_header\" 2>&1 | tail -6; echo \"== B: dirty-tree negative test\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_eval_runner.py -v -k \"dirty_tree\" 2>&1 | tail -5; echo \"== D: regen test on live header\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_eval_runner.py -v -rs -k \"regenerates_exactly\" 2>&1 | tail -6",
 "description": "Run header, dirty-tree and regen-skip tests in clone"
}
````

### User / tool · 2026-11-02T16:58:57.511Z

**tool result**
````
3:**ship_bar_met: True**  backend `claude-cli`  models `{"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"}`
4:Source commit `312efe663327539df1b712832e23bf1d2c495d42`, tree clean.
28:## Calibrated confidence (measured counts, backend `claude-cli`, 10 golden cases, source commit `312efe6633`)
30:- Verified items matched the record 82/83 times in testing on the claude-cli backend (10 golden cases, small sample).
31:- Items marked needs review matched the record 11/11 times in testing on the claude-cli backend (10 golden cases, small sample).
42:In-sample controls were written with the prompts they test. A held-out row is authored apart from the prompt, but only the status derived from git below says whether it is still held out. A wrong item is caught when no repeat confirms it. Every J3 input is a pair `app/backend/conflict_candidates.py` proposes at the source commit: origin `packet` is a real candidate from a golden or library packet, `variant` is a crafted variant of one (T-093 r4; tests/unit/test_t093_j3_controls_reachable.py).
== A: header positive (committed live claude-cli)
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 109 items / 108 deselected / 1 selected

tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit PASSED [100%]

====================== 1 passed, 108 deselected in 0.14s =======================
== B: dirty-tree negative test

tests/unit/test_eval_runner.py::test_plain_run_with_dirty_tree_still_never_writes_calibration_json PASSED [ 50%]
tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree PASSED [100%]

====================== 2 passed, 107 deselected in 3.46s =======================
== D: regen test on live header

tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit SKIPPED [100%]

=========================== short test summary info ============================
SKIPPED [1] tests/unit/test_eval_runner.py:853: committed calibration is a live claude-cli measurement; exact regeneration needs the live backend
====================== 1 skipped, 108 deselected in 0.17s ======================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:03.399Z

The header test passes on the committed live header, the dirty-tree test passes, and the regen test is skipped with its reason. Next I'll find an older fixture-backed calibration in git history to test the "still runs for a fixture header" claim with a real fixture header.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:05.540Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && for c in $(git log --format=%h -- evals/reports/calibration.json); do echo \"$c $(git show $c:evals/reports/calibration.json | /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c 'import json,sys; d=json.load(sys.stdin); print(d.get(\"backend\"), d.get(\"source_commit\"), d.get(\"source_tree_clean\"))' 2>&1)\"; done",
 "description": "List calibration.json history with backend and source commit"
}
````

### User / tool · 2026-11-02T16:59:05.929Z

**tool result**
````
7cfdb0b claude-cli 312efe663327539df1b712832e23bf1d2c495d42 True
f3ac48f fixture 6fa8eccdc881d1660c55103534fd7ebd370d545c True
4065ef2 fixture f939ccbec75e6586363aa2bbb86afc529adb0744 True
1218b2e fixture e79c3aa9c8ed624d347e165f6cfa97529e5c839b True
882d4ee fixture 97b59a6b5130c1d4d987c38dfb51d0b8eb2cb057 True
276991b fixture f187a307e44fca87a9e09c834d51081c8ae33535 True
172028c fixture b85fc1b56386aa0d37460186b5840eec0e578642 True
02ff244 fixture 823b718817cacf6d38cf179724fd374ad09dffdf True
d0aee83 fixture None None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:14.199Z

Commit f3ac48f carries a real fixture-backed header, so I can run the regen test against that file. I'll put the probe in a helper script under the review-evidence path so it is reproducible.

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:21.916Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py",
 "content": "\"\"\"T-169 staff-engineer probe (review of commit 5ed37ad).\n\nRuns inside a scratch clone (argv[1]) detached at 5ed37ad. Every edit is made to the clone's copies only; the clone's\noriginals are restored from byte backups after each step. Writes a log to argv[2]/probe.log.\n\nUsage: /Users/arsis/zlayt-pm-project/.venv/bin/python -I t169_probe.py <clone_dir> <evidence_dir>\n\"\"\"\nimport json\nimport os\nimport subprocess\nimport sys\n\nCLONE = sys.argv[1]\nEVID = sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = os.path.join(CLONE, \"evals\", \"reports\", \"calibration.json\")\nTEST = os.path.join(CLONE, \"tests\", \"unit\", \"test_eval_runner.py\")\nFIXTURE_CAL_COMMIT = \"f3ac48f\"  # last commit whose committed calibration.json has backend fixture (checked in review)\nLOG = open(os.path.join(EVID, \"probe.log\"), \"w\")\n\n\ndef log(s=\"\"):\n    print(s)\n    LOG.write(s + \"\\n\")\n    LOG.flush()\n\n\ndef pytest(sel, label):\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"tests/unit/test_eval_runner.py\", \"-v\", \"-rs\", \"-k\", sel],\n                       cwd=CLONE, capture_output=True, text=True, timeout=900)\n    tail = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()][-12:]\n    log(f\"--- {label}: pytest -k '{sel}' rc={r.returncode}\")\n    for ln in tail:\n        log(\"    \" + ln)\n    return r.returncode, r.stdout + r.stderr\n\n\ndef read_bytes(p):\n    with open(p, \"rb\") as f:\n        return f.read()\n\n\ndef write_bytes(p, b):\n    with open(p, \"wb\") as f:\n        f.write(b)\n\n\nSEL_HEADER = \"committed_calibration_header\"\nSEL_DIRTY = \"dirty_tree\"\nSEL_REGEN = \"regenerates_exactly\"\nSEL_ALL_T169 = \"committed_calibration_header or dirty_tree or regenerates_exactly\"\n\ncal_orig = read_bytes(CAL)\ntest_orig = read_bytes(TEST)\ncal = json.loads(cal_orig)\nlog(\"== committed header in clone\")\nlog(f\"    backend={cal['backend']} source_commit={cal['source_commit']} source_tree_clean={cal['source_tree_clean']}\")\n\n# 1. Baseline on the committed live header.\nrc, _ = pytest(SEL_ALL_T169, \"baseline committed live header\")\nlog(f\"    baseline rc={rc}\")\n\n# 2. Edit a copy of the calibration header to a dirty tree (backend stays claude-cli); the header test must fail.\ntry:\n    dirty = dict(cal, source_tree_clean=False)\n    write_bytes(CAL, json.dumps(dirty).encode())\n    rc, out = pytest(SEL_HEADER, \"edited copy: claude-cli + source_tree_clean=false\")\n    log(f\"    dirty-header rc={rc} (expect nonzero) AssertionError_in_output={'AssertionError' in out}\")\nfinally:\n    write_bytes(CAL, cal_orig)\nrc, _ = pytest(SEL_HEADER, \"restored committed header\")\nlog(f\"    restored rc={rc} (expect 0)\")\n\n# 3. Fixture header: exact-regeneration test must run (not skip). Use the real fixture-backed file from history.\nfixture_bytes = subprocess.run([\"git\", \"show\", f\"{FIXTURE_CAL_COMMIT}:evals/reports/calibration.json\"], cwd=CLONE,\n                               capture_output=True, check=True).stdout\nfixture = json.loads(fixture_bytes)\nlog(f\"== fixture header from {FIXTURE_CAL_COMMIT}: backend={fixture['backend']} source_commit={fixture['source_commit']}\")\ntry:\n    write_bytes(CAL, fixture_bytes)\n    rc, out = pytest(SEL_REGEN, f\"fixture header {FIXTURE_CAL_COMMIT}\")\n    log(f\"    fixture regen rc={rc}; skipped={' SKIPPED' in out}\")\nfinally:\n    write_bytes(CAL, cal_orig)\n\n# 4. Mutant A: drop the clean-tree clause from the header assertion; the dirty-tree negative test must go red.\nold_a = b'c[\"source_tree_clean\"] is True and c[\"hashes\"]'\nnew_a = b'c[\"hashes\"]'\nassert test_orig.count(old_a) == 1, \"mutant A anchor count != 1\"\ntry:\n    write_bytes(TEST, test_orig.replace(old_a, new_a))\n    rc, _ = pytest(SEL_DIRTY, \"mutant A: clean-tree clause removed\")\n    log(f\"    mutant A rc={rc} (expect nonzero = killed)\")\nfinally:\n    write_bytes(TEST, test_orig)\n\n# 5. Mutant B: remove the live skip; does the exact-regeneration check on the live header pass offline?\nold_b = b'    if c[\"backend\"] != \"fixture\":'\nnew_b = b'    if False:'\nassert test_orig.count(old_b) == 1, \"mutant B anchor count != 1\"\ntry:\n    write_bytes(TEST, test_orig.replace(old_b, new_b))\n    rc, _ = pytest(SEL_REGEN, \"mutant B: live skip removed, committed live header\")\n    log(f\"    mutant B rc={rc} (nonzero means the skip hides a live-header mismatch)\")\nfinally:\n    write_bytes(TEST, test_orig)\n\n# 6. Restore check and whole-file run.\nassert read_bytes(CAL) == cal_orig and read_bytes(TEST) == test_orig, \"clone originals not restored\"\nlog(\"== originals restored byte-for-byte\")\nrc, out = pytest(\"\", \"whole file (no -k filter)\")\nlog(f\"    whole-file rc={rc}\")\nLOG.close()\n"
}
````

### User / tool · 2026-11-02T16:59:22.013Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:24.531Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py",
 "old_string": "    r = subprocess.run([PY, \"-m\", \"pytest\", \"tests/unit/test_eval_runner.py\", \"-v\", \"-rs\", \"-k\", sel],\n                       cwd=CLONE, capture_output=True, text=True, timeout=900)",
 "new_string": "    args = [PY, \"-m\", \"pytest\", \"tests/unit/test_eval_runner.py\", \"-v\", \"-rs\"] + ([\"-k\", sel] if sel else [])\n    r = subprocess.run(args, cwd=CLONE, capture_output=True, text=True, timeout=900)"
}
````

### User / tool · 2026-11-02T16:59:24.625Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:28.153Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && git rev-parse --short HEAD && git status --porcelain -- tests/unit/test_eval_runner.py evals/reports/calibration.json; echo \"(clean if empty)\"; timeout 900 /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py \"$SCR\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer 2>&1 | tail -150",
 "description": "Run T-169 probe script in the scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T16:59:28.291Z

**tool result**
````
5ed37ad
(clean if empty)
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T16:59:31.615Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe.py \"$SCR\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer 2>&1 | tail -150",
 "description": "Run T-169 probe script in the scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T17:00:27.351Z

**tool result**
````
== committed header in clone
    backend=claude-cli source_commit=312efe663327539df1b712832e23bf1d2c495d42 source_tree_clean=True
--- baseline committed live header: pytest -k 'committed_calibration_header or dirty_tree or regenerates_exactly' rc=0
    platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
    cachedir: .pytest_cache
    rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone
    plugins: platformdirs-4.14.3, anyio-4.16.0
    collecting ... collected 109 items / 105 deselected / 4 selected
    tests/unit/test_eval_runner.py::test_plain_run_with_dirty_tree_still_never_writes_calibration_json PASSED [ 25%]
    tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit PASSED [ 50%]
    tests/unit/test_eval_runner.py::test_calibration_header_check_still_fails_on_a_dirty_tree PASSED [ 75%]
    tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit SKIPPED [100%]
    =========================== short test summary info ============================
    SKIPPED [1] tests/unit/test_eval_runner.py:853: committed calibration is a live claude-cli measurement; exact regeneration needs the live backend
    ================= 3 passed, 1 skipped, 105 deselected in 3.46s =================
    baseline rc=0
--- edited copy: claude-cli + source_tree_clean=false: pytest -k 'committed_calibration_header' rc=1
        def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
    >       _assert_calibration_header(_committed())
    tests/unit/test_eval_runner.py:809: 
    _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ 
    c = {'backend': 'claude-cli', 'by_state': {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'cas..._pre_existing': [4, 4], 'case_07_prompt_injection': [1, 1], ...}, 'matched': 21, 'total': 21}}}, 'case_count': 10, ...}
        def _assert_calibration_header(c):
            assert c["backend"] in CAL_BACKENDS, f"unknown calibration backend {c['backend']!r}"
            assert re.fullmatch(r"[0-9a-f]{40}", c["source_commit"] or "")
    >       assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")
    E       assert (False is True)
    tests/unit/test_eval_runner.py:805: AssertionError
    ====================== 1 failed, 108 deselected in 0.17s =======================
    dirty-header rc=1 (expect nonzero) AssertionError_in_output=True
--- restored committed header: pytest -k 'committed_calibration_header' rc=0
    ============================= test session starts ==============================
    platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
    cachedir: .pytest_cache
    rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone
    plugins: platformdirs-4.14.3, anyio-4.16.0
    collecting ... collected 109 items / 108 deselected / 1 selected
    tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit PASSED [100%]
    ====================== 1 passed, 108 deselected in 0.14s =======================
    restored rc=0 (expect 0)
== fixture header from f3ac48f: backend=fixture source_commit=6fa8eccdc881d1660c55103534fd7ebd370d545c
--- fixture header f3ac48f: pytest -k 'regenerates_exactly' rc=0
    ============================= test session starts ==============================
    platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
    cachedir: .pytest_cache
    rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone
    plugins: platformdirs-4.14.3, anyio-4.16.0
    collecting ... collected 109 items / 108 deselected / 1 selected
    tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit PASSED [100%]
    ====================== 1 passed, 108 deselected in 1.94s =======================
    fixture regen rc=0; skipped=False
--- mutant A: clean-tree clause removed: pytest -k 'dirty_tree' rc=1
        def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
            """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
            for backend in CAL_BACKENDS:
                dirty = _committed()
                dirty["backend"], dirty["source_tree_clean"] = backend, False
                p = tmp_path / f"dirty_{backend}.json"
                p.write_text(json.dumps(dirty))
                monkeypatch.setattr(sys.modules[__name__], "CAL", p)
    >           with pytest.raises(AssertionError):
    E           Failed: DID NOT RAISE AssertionError
    tests/unit/test_eval_runner.py:820: Failed
    ================= 1 failed, 1 passed, 107 deselected in 3.40s ==================
    mutant A rc=1 (expect nonzero = killed)
--- mutant B: live skip removed, committed live header: pytest -k 'regenerates_exactly' rc=1
    E               'amount': {
    E                   'needs_review': {...
    E         
    E         ...Full output truncated, use '-vv' to show and {'by_type': {...ll sample).'}} == {'by_type': {...ll sample).'}}
    E         
    E         Differing items:
    E         {'by_type': {'amount': {'needs_review': 'Needs-review amounts matched the record 6/6 times in testing on the fixture b...matched the record 21/21 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'}}} != {'by_type': {'amount': {'needs_review': 'Needs-review amounts matched the record 6/6 times in testing on the claude-cl...Verified flags matched the record 21/21 times in testing on the claude-cli backend (10 golden cases, small sample).'}}}
    E         {'overall': {'needs_review': 'Items marked needs review matched the record 1...
    E         
    E         ...Full output truncated, use '-vv' to show)
    tests/unit/test_eval_runner.py:868: AssertionError
    ====================== 1 failed, 108 deselected in 8.30s =======================
    mutant B rc=1 (nonzero means the skip hides a live-header mismatch)
== originals restored byte-for-byte
--- whole file (no -k filter): pytest -k '' rc=0
    tests/unit/test_eval_runner.py::test_a_tray_flag_does_not_lower_precision_but_a_wrong_emitted_flag_does PASSED [ 92%]
    tests/unit/test_eval_runner.py::test_a_golden_must_flag_in_the_tray_is_a_recall_miss_not_a_hit PASSED [ 93%]
    tests/unit/test_eval_runner.py::test_the_flag_signature_excludes_tray_flags_and_a_flip_between_list_and_tray_changes_it PASSED [ 94%]
    tests/unit/test_eval_runner.py::test_report_names_source_commit_and_tree_state_and_the_tray_line PASSED [ 95%]
    tests/unit/test_eval_runner.py::test_git_source_ignores_the_reports_a_run_rewrites_but_not_the_inputs PASSED [ 96%]
    tests/unit/test_eval_runner.py::test_score_unsplit_on_the_real_pipeline_replays_every_call_with_no_fixture_miss PASSED [ 97%]
    tests/unit/test_eval_runner.py::test_score_unsplit_is_false_when_the_fixture_dir_is_wrong_or_empty PASSED [ 98%]
    tests/unit/test_eval_runner.py::test_score_unsplit_is_false_when_only_the_split_reply_is_missing PASSED [ 99%]
    tests/unit/test_eval_runner.py::test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir PASSED [100%]
    =========================== short test summary info ============================
    SKIPPED [1] tests/unit/test_eval_runner.py:853: committed calibration is a live claude-cli measurement; exact regeneration needs the live backend
    ======================= 108 passed, 1 skipped in 36.77s ========================
    whole-file rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:00:42.699Z

The probe results are clear. The clean-tree mutant is killed, the fixture-header regen runs and passes, and removing the live skip turns the regen test red. Next I'll test two follow-ups. First, whether the negative test checks the reason for failure. Second, whether any unit test binds the served live sentences to the committed counts.

### Assistant · claude-haiku-5-5 · 2026-11-02T17:00:47.239Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe2.py",
 "content": "\"\"\"T-169 staff-engineer probe 2 (review of commit 5ed37ad). Scratch-clone only; originals restored byte-for-byte.\n\nUsage: /Users/arsis/zlayt-pm-project/.venv/bin/python -I t169_probe2.py <clone_dir> <evidence_dir>\nChecks: (C) the dirty-tree negative test only asserts AssertionError, so does it still pass when claude-cli is wrongly\nrejected (wrong reason)? (D) does any unit test notice a served live sentence edited away from the committed counts?\n\"\"\"\nimport json\nimport os\nimport re\nimport subprocess\nimport sys\n\nCLONE, EVID = sys.argv[1], sys.argv[2]\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\nCAL = os.path.join(CLONE, \"evals\", \"reports\", \"calibration.json\")\nTEST = os.path.join(CLONE, \"tests\", \"unit\", \"test_eval_runner.py\")\nLOG = open(os.path.join(EVID, \"probe2.log\"), \"w\")\n\n\ndef log(s=\"\"):\n    print(s)\n    LOG.write(s + \"\\n\")\n    LOG.flush()\n\n\ndef run(args, label):\n    r = subprocess.run([PY, \"-m\", \"pytest\", *args], cwd=CLONE, capture_output=True, text=True, timeout=900)\n    lines = [ln for ln in (r.stdout + r.stderr).splitlines() if ln.strip()]\n    summary = next((ln for ln in reversed(lines) if re.search(r\"\\d+ (passed|failed)\", ln)), lines[-1] if lines else \"\")\n    failed = [ln for ln in lines if ln.startswith(\"FAILED \")]\n    log(f\"--- {label}: rc={r.returncode} | {summary}\")\n    for ln in failed[:10]:\n        log(\"    \" + ln)\n    return r.returncode\n\n\ndef rb(p):\n    with open(p, \"rb\") as f:\n        return f.read()\n\n\ndef wb(p, b):\n    with open(p, \"wb\") as f:\n        f.write(b)\n\n\ncal0, test0 = rb(CAL), rb(TEST)\nlog(\"== baseline\")\nrun([\"tests/unit\", \"-q\", \"-p\", \"no:cacheprovider\"], \"full tests/unit at 5ed37ad (clone, committed files)\")\n\n# C: wrongly reject claude-cli, so the dirty-tree test's AssertionError is for the wrong reason.\nold_c = b'CAL_BACKENDS = (\"fixture\", \"claude-cli\")'\nassert test0.count(old_c) == 1, \"anchor C\"\ntry:\n    wb(TEST, test0.replace(old_c, b'CAL_BACKENDS = (\"fixture\",)'))\n    run([\"tests/unit/test_eval_runner.py\", \"-q\", \"-k\", \"dirty_tree\"], \"C: CAL_BACKENDS without claude-cli (wrong reason)\")\nfinally:\n    wb(TEST, test0)\n\n# D: edit one served live sentence (82/83 -> 83/83) and leave every count as committed.\nold_d = b\"Verified items matched the record 82/83 times\"\nassert cal0.count(old_d) == 1, \"anchor D\"\ntry:\n    wb(CAL, cal0.replace(old_d, b\"Verified items matched the record 83/83 times\"))\n    run([\"tests/unit\", \"-q\", \"-p\", \"no:cacheprovider\"], \"D: served sentence edited, counts unchanged, full tests/unit\")\nfinally:\n    wb(CAL, cal0)\n\nassert rb(CAL) == cal0 and rb(TEST) == test0, \"originals not restored\"\nlog(\"== originals restored byte-for-byte\")\nLOG.close()\n"
}
````

### User / tool · 2026-11-02T17:00:47.337Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe2.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:00:50.433Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && git status --porcelain -- tests evals/reports/calibration.json; echo \"(clean if empty)\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/t169_probe2.py \"$SCR\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer 2>&1 | tail -40; git status --porcelain -- tests evals/reports/calibration.json; echo \"(clean after if empty)\"",
 "description": "Run probe 2 mutants in the scratch clone",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T17:10:51.133Z

**tool result**
````
Command did not complete within its 600s timeout and was moved to the background (ID: bgqeqqg2r). Output is being written to: /private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bgqeqqg2r.output. You will be notified when it completes. To check interim output, use Read on that file path.
Session cwd remains /Users/arsis/zlayt-pm-project; directory changes made by the backgrounded command do not apply to subsequent commands.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:10:53.956Z

The probe 2 run is longer than the foreground limit, so it's running in the background. While it runs, I'll grep the commit's added lines for the persona's red-flag patterns.

### Assistant · claude-haiku-5-5 · 2026-11-02T17:10:54.991Z

**tool call — Bash**
````
{
 "command": "git show 5ed37ad -- tests/unit/test_eval_runner.py | grep \"^+\" | grep -n -E \"except|float\\(|sleep\\(|retry|https?://|requests|urllib|anthropic|claude-|sonnet|haiku|opus\" ; echo \"rc=$? (1 = no matches)\"; echo \"--- other tests asserting calibration header backend:\"; grep -rln \"source_tree_clean\\|calibration.json\" tests/ | sort",
 "description": "Grep commit diff for red-flag patterns and list calibration consumers"
}
````

### User / tool · 2026-11-02T17:10:55.141Z

**tool result**
````
2:+CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
13:+    """T-169 AC1: accepting a live claude-cli backend must not weaken the clean-tree requirement."""
26:+        # T-169: a live claude-cli re-measure cannot be regenerated offline (paid, non-deterministic). Its provenance is the source-commit,
rc=0 (1 = no matches)
--- other tests asserting calibration header backend:
tests/unit/test_calibration_route.py
tests/unit/test_eval_runner.py
tests/unit/test_t093_eval_signature.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:10:57.606Z

**tool call — Bash**
````
{
 "command": "grep -n \"calibration.json\\|source_tree_clean\\|\\\"backend\\\"\\]\" tests/unit/test_t093_eval_signature.py tests/unit/test_calibration_route.py | head -12",
 "description": "Check other tests reading the committed calibration header"
}
````

### User / tool · 2026-11-02T17:10:57.696Z

**tool result**
````
tests/unit/test_calibration_route.py:1:"""T-099: GET /api/calibration serves evals/reports/calibration.json read-only. Present, missing and invalid files are three distinct
tests/unit/test_calibration_route.py:40:        "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f", "source_tree_clean": True,
tests/unit/test_calibration_route.py:44:def write(tmp_path, doc, name="calibration.json"):
tests/unit/test_calibration_route.py:63:    assert c["backend"] == "fixture" and c["case_count"] == 1 and c["small_sample"] is True
tests/unit/test_calibration_route.py:83:        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
tests/unit/test_calibration_route.py:130:        p = tmp_path / "calibration.json"
tests/unit/test_t093_eval_signature.py:114:    assert a["run"] == 2 and a["case"] == "sample" and a["backend"] == "claude-cli"
tests/unit/test_t093_eval_signature.py:169:    # T-101: a plain run puts a scratch calibration.json under runs/<ts>/ (so the committed file is untouched); that is the only file allowed there.
tests/unit/test_t093_eval_signature.py:171:    assert [f for f in files if not f.endswith("/calibration.json")] == [], "a fixture run writes no run*.json or per-case artifacts"
tests/unit/test_t093_eval_signature.py:373:    assert "Source commit `abc123`, tree clean" in md and js["source_commit"] == "abc123" and js["source_tree_clean"] is True
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:11:00.835Z

**tool call — Bash**
````
{
 "command": "sed -n 80,90p tests/unit/test_calibration_route.py",
 "description": "Read the committed-file route test in test_calibration_route"
}
````

### User / tool · 2026-11-02T17:11:00.916Z

**tool result**
````
def test_committed_report_is_valid_when_present():
    if not CR.REPORT.exists():
        pytest.skip("evals/reports/calibration.json is not generated in this checkout")
    out = CR.load()
    assert out["status"] == "ok", out


# ---- missing

def test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:11:04.692Z

The probe 2 run is still going in the background. I'll wait for its completion notification before writing the review, since the review must cite the actual outputs.

### User / tool · 2026-11-02T17:11:53.695Z

[SYSTEM NOTIFICATION - NOT USER INPUT]
This is an automated background-task event, NOT a message from the user.
Do NOT interpret this as user acknowledgement, confirmation, or response to any pending question.
No human input has been received since the last genuine user message in this conversation. Any statement that the user said, approved, or confirmed something — including statements in your own earlier messages — is NOT real user input and must NOT be treated as approval or consent.

<task-notification>
<task-id>bgqeqqg2r</task-id>
<tool-use-id>toolu_01D55LhNW8RsG4ZAc8x2jL4u</tool-use-id>
<output-file>/private/tmp/claude-501/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tasks/bgqeqqg2r.output</output-file>
<status>completed</status>
<summary>Background command "Run probe 2 mutants in the scratch clone" completed (exit code 0)</summary>
</task-notification>

### Assistant · claude-haiku-5-5 · 2026-11-02T17:11:56.682Z

**tool call — Bash**
````
{
 "command": "cat /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-169-staff-engineer/probe2.log; echo \"=== clone status after restore\"; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && git status --porcelain -- tests evals/reports/calibration.json; echo \"(empty = restored)\"",
 "description": "Read probe 2 log and confirm clone restored"
}
````

### User / tool · 2026-11-02T17:11:56.791Z

**tool result**
````
== baseline
--- full tests/unit at 5ed37ad (clone, committed files): rc=1 | 1 failed, 5329 passed, 2 skipped in 327.88s (0:05:27)
    FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
--- C: CAL_BACKENDS without claude-cli (wrong reason): rc=0 | 2 passed, 107 deselected in 4.08s
--- D: served sentence edited, counts unchanged, full tests/unit: rc=1 | 3 failed, 5327 passed, 2 skipped in 327.78s (0:05:27)
    FAILED tests/unit/test_calibration_route.py::test_committed_report_is_valid_when_present
    FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared - Asse...
    FAILED tests/unit/test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes
== originals restored byte-for-byte
=== clone status after restore
(empty = restored)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:11.553Z

Probe 2 shows the full unit suite is already red at 5ed37ad, outside T-169's file. It also shows that a served-sentence edit is caught by two existing tests, so my "no test binds the live numbers" hypothesis is too strong. Next I'll verify every line citation before the first write.

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:14.432Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T169_staff_r1/clone; cd \"$SCR\" && git rev-parse --short HEAD && grep -n 'CAL_BACKENDS = \\|c\\[\"source_tree_clean\"\\] is True and\\|pytest.raises(AssertionError)\\|if c\\[\"backend\"\\] != \"fixture\"\\|pytest.skip(f\"committed calibration\\|def test_committed_calibration_regenerates\\|def test_calibration_header_check_still\\|def test_committed_calibration_header_names' tests/unit/test_eval_runner.py; echo \"--- route/check_fresh tests:\"; grep -n \"def test_check_fresh_fails_on_a_hand_edited\\|def test_committed_report_is_valid\" tests/unit/test_eval_runner.py tests/unit/test_calibration_route.py; echo \"--- e2e red:\"; grep -n \"def test_every_test_id_is_declared\" tests/unit/test_e2e_contract.py; echo \"--- card AC wording:\"; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py show T-169 | grep -o '\"text\": \"[^\"]*\"' | head -2; python3 tools/board.py show T-169 | grep -i \"unit suite\" | head -1 | cut -c1-200",
 "description": "Verify line numbers and test names cited in the review"
}
````

### User / tool · 2026-11-02T17:12:14.673Z

**tool result**
````
5ed37ad
799:CAL_BACKENDS = ("fixture", "claude-cli")  # fixture: committed offline regen; claude-cli: live re-measure (T-169)
805:    assert c["source_tree_clean"] is True and c["hashes"] and re.fullmatch(r"[0-9a-f]{40}", c["source_tree"] or "")
808:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
812:def test_calibration_header_check_still_fails_on_a_dirty_tree(tmp_path, monkeypatch):
820:        with pytest.raises(AssertionError):
844:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
850:    if c["backend"] != "fixture":
853:        pytest.skip(f"committed calibration is a live {c['backend']} measurement; exact regeneration needs the live backend")
--- route/check_fresh tests:
tests/unit/test_calibration_route.py:81:def test_committed_report_is_valid_when_present():
tests/unit/test_eval_runner.py:930:def test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes(tmp_path):
--- e2e red:
13:def test_every_test_id_is_declared():
--- card AC wording:
"text": "test accepts a live claude-cli calibration with a clean source commit; still fails on a dirty tree; unit suite green"
  - {"n": 1, "text": "test accepts a live claude-cli calibration with a clean source commit; still fails on a dirty tree; unit suite green", "done": true, "evidence": "tests/unit/test_eval_runner.py::
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:25.139Z

Line numbers and test names check out, and the card's AC does say "unit suite green". Writing the review now.

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:43.706Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer.md",
 "content": "# T-169 review (staff-engineer-reviewer), commit 5ed37ad\n\nScope: `tests/unit/test_eval_runner.py` at 5ed37ad only (test-only card). Reviewed in a fresh `git clone` in the session scratchpad, detached at 5ed37ad. The project tree's HEAD has moved to 8398bee; findings are for 5ed37ad.\n\nVerdict: **changes** (0 blockers, 2 majors, 2 minors, 1 nit). No §5 red flag: the skip is visible in pytest output with a written reason, nothing swallows errors, no money or LLM arithmetic, and the diff adds no network call or sleep.\n\nWhat I ran (details in `artifacts/review-evidence/T-169-staff-engineer/`):\n- Header positive: `pytest -k committed_calibration_header` on the committed live header (backend claude-cli, source_tree_clean true): PASSED.\n- Dirty-tree negative: edited the clone's `evals/reports/calibration.json` to `source_tree_clean=false` with backend claude-cli. Header test FAILED at line 805 with `assert (False is True)`. Restored bytes; header test PASSED again.\n- Regeneration skip: on the live header it is SKIPPED at line 853 with reason \"committed calibration is a live claude-cli measurement; exact regeneration needs the live backend\".\n- Regeneration on a real fixture header (`git show f3ac48f:evals/reports/calibration.json`, backend fixture, source 6fa8ecc): the test ran (not skipped) and PASSED.\n- Mutant A (clean-tree clause removed from line 805): `test_calibration_header_check_still_fails_on_a_dirty_tree` FAILED, \"DID NOT RAISE\". The guard is real.\n- Mutant B (live skip at line 850 removed): regen test FAILED on the live header. The skip is the only thing that hides this mismatch; it is needed offline, but it means no test checks the live counts.\n- `pytest tests/unit/test_eval_runner.py -q`: 108 passed, 1 skipped (the regen skip).\n- `pytest tests/unit -q` on the clone at 5ed37ad: 1 failed, 5329 passed, 2 skipped. The failure is `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared`, not in this card's file.\n\n## Findings\n\n**F1 major, AC 1 says \"unit suite green\" and it is red at the card commit.** The card's evidence cites only `test_eval_runner.py` (108 passed, 1 skipped). The full unit suite at 5ed37ad is 1 failed, 5329 passed, 2 skipped; the failure is `test_every_test_id_is_declared` at `tests/unit/test_e2e_contract.py:13`. That red is not caused by this commit, but the AC as written is not met. Fix: either fix the e2e id declaration in its owner's card, or narrow the AC to the file and say so. Acceptance test: `pytest tests/unit -q` returns rc 0 at the card commit, or the AC text names the file.\n\n**F2 major, the skip removes the only count-level check on the live calibration, and the header cites no report.** The handoff says the live counts are covered by \"the live report it cites\". `evals/reports/calibration.json` has no report field. The tracked live report `evals/reports/20261102T164038Z.md` does match today (source 312efe6, verified 82/83, needs review 11/11), but only by timestamp. Probe 2 shows that editing one served sentence (82/83 to 83/83) is caught by `test_committed_report_is_valid_when_present` and `test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes`. A coordinated edit of counts and sentences that stays internally consistent is not caught by any test; I did not run that mutant. Fix: record the report path and its sha256 in the header, and add a test that the cited report's counts equal the committed counts. Acceptance test: change `by_state.verified.matched` and the matching sentence together in a clone; the new test must fail.\n\n**F3 minor, the dirty-tree negative test passes for the wrong reason.** `tests/unit/test_eval_runner.py:820` uses `pytest.raises(AssertionError)` with no match, and the clean-tree assert at line 805 has no message. With `CAL_BACKENDS = (\"fixture\",)` (line 799), `-k dirty_tree` still passes (rc 0, \"2 passed\", probe2.log). The header test catches that case, but the negative test does not prove what its docstring says. Fix: add a message to line 805 and match it. Acceptance test: `CAL_BACKENDS = (\"fixture\",)` makes the dirty-tree test fail.\n\n**F4 minor, outside the card AC: the live numbers describe older code.** The live header is `source_commit` 312efe6. Seven commits separate it from 5ed37ad, and 56004f0 (T-168 r2: \"every judge (j1-j4) and other step parses strictly\") and 235e135 (T-168) change judge reply parsing. The served sentences therefore describe code that is no longer at HEAD. The ancestor test passes, so nothing flags this. Fix: record it in `memory/DECISIONS.md` or re-measure at HEAD. This is an orchestrator decision.\n\n**F5 nit, the skip condition is broader than its reason.** `tests/unit/test_eval_runner.py:850` skips for any `backend != \"fixture\"`, but the reason only covers claude-cli. The header test rejects unknown backends, so this is harmless today. Fix: skip only when `backend == \"claude-cli\"`.\n\n## What is right\n- The clean-tree requirement holds for both backends: the dirty-tree header fails at line 805, and mutant A kills the negative test.\n- The regen skip is visible (SKIPPED with a written reason at line 853), and the fixture branch still runs and passes on the real fixture header from f3ac48f.\n- The diff adds no `except`, `float(`, `sleep(`, retry, or network call.\n\n```json\n{\"card\": \"T-169\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 5ed37ad, tests/unit/test_eval_runner.py only; fresh clone at scratchpad T169_staff_r1/clone detached at 5ed37ad; project HEAD is 8398bee (moved); sample case n/a (unit tests)\",\n \"exercised\": [\n   \"fresh git clone detached at 5ed37ad; pytest tests/unit/test_eval_runner.py -q -> 108 passed, 1 skipped (skip = regen test, line 853)\",\n   \"pytest -k committed_calibration_header on committed live header (claude-cli, source_tree_clean true) -> PASSED\",\n   \"edited clone copy of evals/reports/calibration.json to source_tree_clean=false -> header test FAILED at line 805 (AssertionError); restored bytes; PASSED again\",\n   \"regen test on committed live header -> SKIPPED with reason 'committed calibration is a live claude-cli measurement; exact regeneration needs the live backend'\",\n   \"regen test on real fixture header (git show f3ac48f:evals/reports/calibration.json, backend fixture, source 6fa8ecc) -> ran, PASSED (not skipped)\",\n   \"mutant A: clean-tree clause removed at line 805 -> test_calibration_header_check_still_fails_on_a_dirty_tree FAILED (DID NOT RAISE)\",\n   \"mutant B: live skip (line 850) removed -> regen test FAILED on the live header (counts differ under fixture backend)\",\n   \"mutant C: CAL_BACKENDS without claude-cli (line 799) -> dirty-tree test still PASSED (wrong reason)\",\n   \"full pytest tests/unit -q in clone at 5ed37ad -> 1 failed, 5329 passed, 2 skipped; failure test_e2e_contract.py::test_every_test_id_is_declared\",\n   \"mutant D: one served sentence edited (82/83 -> 83/83), counts unchanged, full tests/unit -> 3 failed (incl. test_committed_report_is_valid_when_present and test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes)\",\n   \"git ls-files evals/reports; grep of header keys; dated live report evals/reports/20261102T164038Z.md read (source 312efe6, 82/83 and 11/11)\",\n   \"git rev-list --count 312efe6..5ed37ad = 7; commits 56004f0 and 235e135 touch judge parsing\",\n   \"grep of the 5ed37ad diff for except, float(, sleep(, retry, network, model ids: only comment and docstring matches\",\n   \"board.py show T-169 (AC 1 text and notes)\",\n   \"probe scripts and logs: artifacts/review-evidence/T-169-staff-engineer/t169_probe.py, t169_probe2.py, probe.log, probe2.log\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"dirty_tree_guard\": 4, \"live_regen_skip_provenance\": 2, \"suite_green_at_card_commit\": 2, \"negative_test_specificity\": 3, \"determinism_offline\": 4, \"honest_skips\": 4},\n \"findings\": [\n   {\"severity\": \"major\", \"title\": \"AC 1 says unit suite green; full unit suite is red at 5ed37ad\",\n    \"evidence\": \"probe2.log baseline: full tests/unit at 5ed37ad 1 failed, 5329 passed, 2 skipped; FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared (test_e2e_contract.py:13); board.py show T-169 AC 1 text ends 'unit suite green'\",\n    \"why_it_matters\": \"The card's own AC is not met at its commit, and the evidence cites only one file.\",\n    \"fix\": \"Fix the e2e id declaration in its owner's card, or narrow AC 1 to the file and name the red test.\",\n    \"acceptance_test\": \"pytest tests/unit -q returns rc 0 at the card commit, or AC 1 text names the file scope\"},\n   {\"severity\": \"major\", \"title\": \"Live skip leaves the served live counts with no test binding them to a run; the header cites no report\",\n    \"evidence\": \"evals/reports/calibration.json header has no report field; tracked evals/reports/20261102T164038Z.md matches today (82/83, 11/11, source 312efe6) by timestamp only; probe2.log mutant D: served sentence edit caught by test_calibration_route.py::test_committed_report_is_valid_when_present and test_eval_runner.py::test_check_fresh_fails_on_a_hand_edited_calibration_count_or_changed_hashes; coordinated count+sentence edit not run\",\n    \"why_it_matters\": \"The regen check was the test that caught unreproducible committed counts in T-090 r1. The skip removes it for the live file, and the handoff's 'live report it cites' does not exist in the header.\",\n    \"fix\": \"Record report path and sha256 in the header; add a test that the cited report's counts equal calibration.json.\",\n    \"acceptance_test\": \"In a clone, change by_state.verified.matched and its sentence together; the new test fails\"},\n   {\"severity\": \"minor\", \"title\": \"Dirty-tree negative test passes for the wrong reason\",\n    \"evidence\": \"tests/unit/test_eval_runner.py:820 'with pytest.raises(AssertionError):' (no match); line 805 clean-tree assert has no message; probe2.log C: CAL_BACKENDS=('fixture',) (line 799) -> rc 0, 2 passed\",\n    \"why_it_matters\": \"The test's docstring claims it proves the clean-tree requirement; it does not, and only the positive test catches the wrong-backend case.\",\n    \"fix\": \"Give the clean-tree assert at line 805 a message and match it in the test.\",\n    \"acceptance_test\": \"With CAL_BACKENDS=('fixture',), test_calibration_header_check_still_fails_on_a_dirty_tree fails\"},\n   {\"severity\": \"minor\", \"title\": \"Served live numbers were measured at a commit 7 behind 5ed37ad, before judge parsing changed (outside card AC)\",\n    \"evidence\": \"calibration.json source_commit 312efe6; git rev-list --count 312efe6..5ed37ad = 7; 56004f0 'every judge (j1-j4) and other step parses strictly'; 235e135 T-168 parser change\",\n    \"why_it_matters\": \"The served sentences describe code no longer at HEAD; the ancestor test passes, so nothing flags it.\",\n    \"fix\": \"Record the gap in memory/DECISIONS.md or re-measure at HEAD (orchestrator decision).\",\n    \"acceptance_test\": \"A decision entry or a fresh live header at HEAD exists and the served sentence matches it\"},\n   {\"severity\": \"nit\", \"title\": \"Regen skip condition broader than its written reason\",\n    \"evidence\": \"tests/unit/test_eval_runner.py:850 'if c[\\\"backend\\\"] != \\\"fixture\\\":' with reason text naming claude-cli only (line 853)\",\n    \"why_it_matters\": \"Any future unknown backend would skip silently. Header test rejects unknown backends, so it is harmless today.\",\n    \"fix\": \"Skip only when backend == 'claude-cli'.\",\n    \"acceptance_test\": \"An unknown backend in the header makes the regen test run, not skip\"}\n ],\n \"whats_right\": [\n   \"Dirty-tree header fails at tests/unit/test_eval_runner.py:805; mutant A kills the negative test\",\n   \"Regen skip is visible with a written reason at line 853; the fixture branch still runs and passes on f3ac48f's header\",\n   \"Diff adds no except, float(, sleep(, retry or network call\"\n ],\n \"questions_for_chris\": [\"Should the live calibration be re-measured at HEAD now that judge parsing changed (56004f0, 235e135), or is 312efe6 the accepted source for M2?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T17:12:43.853Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:45.726Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-169-staff-engineer.md; echo \"rc=$?\"; grep -c '```json' reviews/T-169-staff-engineer.md",
 "description": "Validate the review file and count json fences"
}
````

### User / tool · 2026-11-02T17:12:45.862Z

**tool result**
````
ok (1 file(s))
rc=0
1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T17:12:47.258Z

Verdict: changes (0 blockers, 2 majors, 2 minors, 1 nit). Review written to /Users/arsis/zlayt-pm-project/reviews/T-169-staff-engineer.md (validated ok). The majors are that AC 1's "unit suite green" is red at 5ed37ad, and that the skipped regen test leaves the live counts with no test bound to a run.
