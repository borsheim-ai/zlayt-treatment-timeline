# Subagent: T-101 review (haiku staff) (T-101 review (haiku staff))

Source: `agent-a558eba01dae286fc.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T05:25:09.009Z

Review board card T-101 in /Users/arsis/zlayt-pm-project (commit 4c5f9bf, evals/run.py). Confirm:
- a plain `python -m evals.run` leaves evals/reports/calibration.json byte-identical;
- `--write-calibration` refuses on a dirty tracked tree and writes the provenance header on a clean one;
- the tests fail if the guard is mutated in a scratch copy.

Test a `git archive HEAD` copy in your scratchpad; you'll need `git init` there to test the clean and dirty logic. Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Write reviews/T-101-staff-engineer.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:10.054Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T05:25:10.063Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:10.278Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T05:25:10.285Z

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
24	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1 d0aee83; r2 fix reverted at HEAD; r3 172028c: git-less copy skips provenance (forged header passes), served route still unowned
25	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — r1 f667f08: reason scope, AC done with UI unbuilt, index deletions; r2 55300e9: done flag left true, conjunction without pending match, `x*8 or [None]` seeds 1 row
26	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 031a708 fail (HEAD revert); r2 31b7ceb pass: partial restore, later-card hunks, CLI crash out of scope
27	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — T-073 r1 seam-only proof; T-084 r1 restore bypass; r2 c8a9874 fails own tree; r4 9c1af01 pass: redundant gate arms, fix commit lacks the change
28	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted, D-047 409 closed by T-100; T-099 3ecb8b1 changes: state-sum rule untested, route weaker than evals check
29	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:10.753Z

**tool call — Bash**
````
{
 "command": "git show --stat 4c5f9bf && git -C /Users/arsis/zlayt-pm-project status --short | head -30 && python3 tools/board.py show T-101",
 "description": "Show commit, working tree status, and T-101 card"
}
````

### User / tool · 2026-11-02T05:25:10.945Z

**tool result**
````
commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:24:43 2026 -0600

    fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
    
    A plain run now writes a scratch copy under evals/reports/runs/<ts>/calibration.json and never touches the committed file the app serves. --write-calibration writes evals/reports/calibration.json with the T-090 provenance header (source_commit, source_tree_clean, source_tree, hashes, backend), and is refused before any run unless the tracked tree is clean at HEAD; the header is re-checked after the run. Tests cover both behaviours, the real-git cleanliness rule, the no-git export, and the regeneration test (accepts the cited commit's own output location).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 evals/run.py                   |  45 +++++++++++--
 tests/unit/test_eval_runner.py | 141 +++++++++++++++++++++++++++++++++++++++--
 2 files changed, 175 insertions(+), 11 deletions(-)
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
MM app/backend/api.py
MM app/backend/billing.py
 M app/backend/case_extras.py
 M app/backend/confidence.py
 M app/backend/flags.py
 M app/backend/generator.py
MM app/backend/grounding.py
 M app/backend/judges.py
 M app/backend/language.py
 M app/backend/pdf_hidden.py
 M app/backend/pipeline.py
 M app/backend/reclassify.py
 M app/backend/rejudge.py
 M app/backend/review.py
---
id: "T-101"
title: "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD)"
milestone: "M3"
role: "qa"
status: "in_review"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:21:08Z"
updated_at: "2026-11-02T05:25:05Z"
claimed_by: "qa"
claimed_at: "2026-11-02T05:21:14Z"
rounds: 0
commits: ["4c5f9bf"]
reviews: []
ac:
  - {"n": 1, "text": "Plain 'python -m evals.run' leaves evals/reports/calibration.json untouched; --write-calibration refuses on a dirty tree; test", "done": true, "evidence": "tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T05:21:14Z qa: claimed
- 2026-11-02T05:24:59Z qa: AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibration_json, ::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head, ::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header, ::test_write_calibration_rechecks_the_header_after_the_run, ::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed
- 2026-11-02T05:25:00Z qa: moved in_progress -> in_review
- 2026-11-02T05:25:05Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json with the T-090 header (source_commit, source_tree_clean, source_tree, hashes, backend), refused (exit 2, nothing run) unless the tracked tree is clean at HEAD, re-checked after the run. Tests: tests/unit/test_eval_runner.py (+6 new, 4 updated for the new location). How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed, 0 skipped; committed calibration.json is byte-identical to HEAD (restored and still identical after the run); real CLI plain run to a scratch --out rc=1 (fixture ship bar, expected) with calibration untouched; --write-calibration on this dirty tree rc=2, nothing written. Left: latest.json and the .md are still written by every run as before (not in scope). Other agents' uncommitted changes in the shared tree were left alone; the commit used --only paths. Surprise: the regeneration test replays the cited commit's own code, so it accepts the old out/calibration.json location as well as the new runs/ scratch copy. Note for orchestrator: --write-calibration does not restrict backend; the committed-header test pins backend=fixture, so a live write would fail that test by design.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:13.495Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat project_t090_calibration_review_patterns.md project_eval_runner_review_patterns.md feedback_review_write_once.md feedback_severity_vs_brief.md project_harness_review_patterns.md 2>&1 | head -250",
 "description": "Read recurring calibration and eval-runner memory notes"
}
````

### User / tool · 2026-11-02T05:25:13.600Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:14.250Z

**tool call — Bash**
````
{
 "command": "git show 4c5f9bf -- evals/run.py && git show 4c5f9bf:evals/run.py | wc -l && ls -la evals/reports/ && git status --short evals/ tests/unit/test_eval_runner.py && git log --oneline -5 -- evals/run.py",
 "description": "Show T-101 diff for evals/run.py and eval report state"
}
````

### User / tool · 2026-11-02T05:25:14.435Z

**tool result**
````
commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:24:43 2026 -0600

    fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
    
    A plain run now writes a scratch copy under evals/reports/runs/<ts>/calibration.json and never touches the committed file the app serves. --write-calibration writes evals/reports/calibration.json with the T-090 provenance header (source_commit, source_tree_clean, source_tree, hashes, backend), and is refused before any run unless the tracked tree is clean at HEAD; the header is re-checked after the run. Tests cover both behaviours, the real-git cleanliness rule, the no-git export, and the regeneration test (accepts the cited commit's own output location).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index 47b0807..9fbb834 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -1,7 +1,11 @@
 """Eval runner: `python -m evals.run` scores the product against the golden set and writes
 evals/reports/<UTC timestamp>.md + evals/reports/latest.json (CONTRACT 8.2 ship bar, REQUIREMENTS 7; D-024/D-026).
 
-    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
+    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture); the committed calibration.json is NOT touched,
+                                         its scratch copy goes to evals/reports/runs/<ts>/calibration.json (T-101)
+    python -m evals.run --write-calibration
+                                         full run that also writes the committed evals/reports/calibration.json (the file the app serves).
+                                         Refused (exit 2, nothing run) unless the tracked tree is clean and HEAD is a commit (T-101)
     python -m evals.run --check-spec     REQUIREMENTS section 6 blocks vs golden export (byte-equal); writes spec_matches_golden
     python -m evals.run --check-fresh    exit 1 when latest.json prompt/lexicon hashes differ from the files on disk
 
@@ -999,14 +1003,32 @@ def render_md(r):
     return "\n".join(L) + "\n"
 
 
-def write_report(r, outdir=REPORTS):
+def write_calibration_refusal(src):
+    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tracked tree at a commit
+    (T-090 r2: the header must name the code that produced the counts). Untracked files do not count, matching git_source()."""
+    if src.get("commit") is None or src.get("clean") is None:
+        return "no git repository or HEAD commit is available to name as the source"
+    if not src["clean"]:
+        return "the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD"
+    return None
+
+
+def write_report(r, outdir=REPORTS, write_calibration=False):
+    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
+    copy under outdir/runs/<ts>/ so a plain run never touches the file the app serves (T-101)."""
     outdir = pathlib.Path(outdir)
     outdir.mkdir(parents=True, exist_ok=True)
     ts = r["generated_at"].replace(":", "").replace("-", "")
     (outdir / f"{ts}.md").write_text(render_md(r))
     (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
-    if r.get("calibration"):                      # small file the app serves (T-090); regenerated by every full run
-        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
+    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
+        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
+        if write_calibration:
+            (outdir / "calibration.json").write_text(body)
+        else:
+            scratch = outdir / "runs" / ts
+            scratch.mkdir(parents=True, exist_ok=True)
+            (scratch / "calibration.json").write_text(body)
     return outdir / f"{ts}.md"
 
 
@@ -1099,6 +1121,8 @@ def main(argv=None, pipeline=None):
     ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
     ap.add_argument("--out", default=str(REPORTS))
     ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
+    ap.add_argument("--write-calibration", action="store_true",
+                    help="also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)")
     a = ap.parse_args(argv)
     out = pathlib.Path(a.out)
     if a.check_fresh:
@@ -1132,13 +1156,24 @@ def main(argv=None, pipeline=None):
         print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
               f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
         return 2
+    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
+        why = write_calibration_refusal(git_source())
+        if why:
+            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
+            return 2
     ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
     if a.controls:
         return run_controls_only(backend, out, ts)
     real = pipeline is None
     report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                           judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
-    path = write_report(report, out)
+    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
+        cal = report.get("calibration") or {}
+        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
+        if why:
+            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
+            return 2
+    path = write_report(report, out, write_calibration=a.write_calibration)
     print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
     for b in report["blockers"]:
         print("  blocker:", b)
    1184
total 728
drwxr-xr-x@ 46 arsis  staff   1472 Nov  1 23:11 .
drwxr-xr-x@ 12 arsis  staff    384 Nov  1 23:24 ..
-rw-r--r--@  1 arsis  staff   2694 Nov  1 20:08 20261102T020824Z.md
-rw-r--r--@  1 arsis  staff   2791 Nov  1 20:09 20261102T020933Z.md
-rw-r--r--@  1 arsis  staff   2605 Nov  1 20:10 20261102T021029Z.md
-rw-r--r--@  1 arsis  staff   2732 Nov  1 20:10 20261102T021046Z.md
-rw-r--r--@  1 arsis  staff   2737 Nov  1 20:27 20261102T022701Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:29 20261102T022927Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:30 20261102T023039Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:31 20261102T023155Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023203Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023204Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:32 20261102T023208Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:36 20261102T023603Z.md
-rw-r--r--@  1 arsis  staff   2883 Nov  1 20:39 20261102T023911Z.md
-rw-r--r--@  1 arsis  staff   2966 Nov  1 20:39 20261102T023916Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:43 20261102T024348Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:43 20261102T024355Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:46 20261102T024653Z.md
-rw-r--r--@  1 arsis  staff   2831 Nov  1 20:48 20261102T024822Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:50 20261102T025055Z.md
-rw-r--r--@  1 arsis  staff   2708 Nov  1 20:52 20261102T025219Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:55 20261102T025526Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 20:57 20261102T025715Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 21:04 20261102T030405Z.md
-rw-r--r--@  1 arsis  staff   2800 Nov  1 21:12 20261102T031209Z.md
-rw-r--r--@  1 arsis  staff   3008 Nov  1 21:20 20261102T032024Z.md
-rw-r--r--@  1 arsis  staff   2884 Nov  1 21:28 20261102T032823Z.md
-rw-r--r--@  1 arsis  staff   3407 Nov  1 21:57 20261102T035750Z.md
-rw-r--r--@  1 arsis  staff   3559 Nov  1 22:09 20261102T040933Z.md
-rw-r--r--@  1 arsis  staff  10094 Nov  1 22:38 20261102T043845Z.md
-rw-r--r--@  1 arsis  staff  10022 Nov  1 23:11 20261102T051136Z.md
-rw-r--r--@  1 arsis  staff   7029 Nov  1 23:23 calibration.json
-rw-r--r--@  1 arsis  staff  26485 Nov  1 22:25 controls-20261102T042306Z.json
-rw-r--r--@  1 arsis  staff   6556 Nov  1 22:25 controls-20261102T042306Z.md
-rw-r--r--@  1 arsis  staff  26497 Nov  1 22:41 controls-20261102T043911Z.json
-rw-r--r--@  1 arsis  staff   6557 Nov  1 22:41 controls-20261102T043911Z.md
-rw-r--r--@  1 arsis  staff  26483 Nov  1 22:52 controls-20261102T044933Z.json
-rw-r--r--@  1 arsis  staff   6557 Nov  1 22:52 controls-20261102T044933Z.md
-rw-r--r--@  1 arsis  staff  26403 Nov  1 22:54 controls-20261102T045207Z.json
-rw-r--r--@  1 arsis  staff   6543 Nov  1 22:54 controls-20261102T045207Z.md
-rw-r--r--@  1 arsis  staff   8669 Nov  1 21:44 determinism-diagnosis.md
-rw-r--r--@  1 arsis  staff  53668 Nov  1 23:11 latest.json
-rw-r--r--@  1 arsis  staff   1817 Nov  1 22:20 library-latest.md
-rw-r--r--@  1 arsis  staff   2105 Nov  1 20:39 m3-sensors.md
drwxr-xr-x@  7 arsis  staff    224 Nov  1 23:12 runs
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
?? evals/reports/20261102T024653Z.md
?? evals/reports/20261102T024822Z.md
?? evals/reports/20261102T025055Z.md
?? evals/reports/20261102T025526Z.md
?? evals/reports/20261102T030405Z.md
?? evals/reports/20261102T031209Z.md
?? evals/reports/20261102T032024Z.md
?? evals/reports/20261102T043845Z.md
?? evals/reports/20261102T051136Z.md
?? evals/reports/controls-20261102T043911Z.json
?? evals/reports/controls-20261102T043911Z.md
?? evals/reports/controls-20261102T044933Z.json
?? evals/reports/controls-20261102T044933Z.md
?? evals/reports/controls-20261102T045207Z.json
?? evals/reports/controls-20261102T045207Z.md
?? evals/reports/runs/20261102T042232Z/
?? evals/reports/runs/20261102T045543Z/
?? evals/reports/runs/20261102T051136Z/
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
a850be0 fix: restore T-090 work reverted by 2fca530
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:20.169Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git log --oneline -3 && echo \"--- tracked dirty count:\" && git status --porcelain --untracked-files=no | wc -l && echo \"--- calibration.json tracked?\" && git ls-files evals/reports/calibration.json && git diff --quiet HEAD -- evals/reports/calibration.json; echo \"calib_diff_rc=$?\" && git show HEAD:evals/reports/calibration.json | shasum -a 256 && shasum -a 256 evals/reports/calibration.json && cat evals/reports/calibration.json && echo \"--- evals/run.py at HEAD vs worktree:\" && git diff --quiet HEAD -- evals/run.py tests/unit/test_eval_runner.py; echo \"run_py_diff_rc=$?\"",
 "description": "Pin HEAD and check calibration.json tracked state"
}
````

### User / tool · 2026-11-02T05:25:20.408Z

**tool result**
````
4c5f9bf909253bfffa55cb41b1350c412c56e6da
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
--- tracked dirty count:
      68
--- calibration.json tracked?
evals/reports/calibration.json
calib_diff_rc=0
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  -
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,
   "total": 10
  },
  "verified": {
   "cases": [
    "case_01_date_formats",
    "case_02_gap_boundaries",
    "case_03_rate_and_ocr",
    "case_04_duplicates_no_amounts",
    "case_05_provider_conflict",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "case_08_diagnosis_temptation",
    "case_09_nonvisit_hides_gap",
    "sample"
   ],
   "matched": 83,
   "total": 84
  }
 },
 "by_type": {
  "amount": {
   "needs_review": {
    "by_case": {
     "case_03_rate_and_ocr": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 6,
    "total": 6
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_03_rate_and_ocr": [
      2,
      2
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      2,
      2
     ]
    },
    "matched": 9,
    "total": 9
   }
  },
  "entry": {
   "needs_review": {
    "by_case": {
     "case_01_date_formats": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 2,
    "total": 2
   },
   "verified": {
    "by_case": {
     "case_01_date_formats": [
      7,
      7
     ],
     "case_02_gap_boundaries": [
      8,
      8
     ],
     "case_03_rate_and_ocr": [
      5,
      5
     ],
     "case_04_duplicates_no_amounts": [
      4,
      4
     ],
     "case_05_provider_conflict": [
      5,
      5
     ],
     "case_06_subtle_pre_existing": [
      4,
      5
     ],
     "case_07_prompt_injection": [
      3,
      3
     ],
     "case_08_diagnosis_temptation": [
      4,
      4
     ],
     "case_09_nonvisit_hides_gap": [
      5,
      5
     ],
     "sample": [
      9,
      9
     ]
    },
    "matched": 54,
    "total": 55
   }
  },
  "flag": {
   "needs_review": {
    "by_case": {
     "case_06_subtle_pre_existing": [
      1,
      1
     ],
     "case_07_prompt_injection": [
      1,
      1
     ]
    },
    "matched": 2,
    "total": 2
   },
   "verified": {
    "by_case": {
     "case_02_gap_boundaries": [
      3,
      3
     ],
     "case_05_provider_conflict": [
      1,
      1
     ],
     "case_06_subtle_pre_existing": [
      3,
      3
     ],
     "case_07_prompt_injection": [
      1,
      1
     ],
     "case_08_diagnosis_temptation": [
      1,
      1
     ],
     "case_09_nonvisit_hides_gap": [
      1,
      1
     ],
     "sample": [
      10,
      10
     ]
    },
    "matched": 20,
    "total": 20
   }
  }
 },
 "case_count": 10,
 "cases": [
  "sample",
  "case_01_date_formats",
  "case_02_gap_boundaries",
  "case_03_rate_and_ocr",
  "case_04_duplicates_no_amounts",
  "case_05_provider_conflict",
  "case_06_subtle_pre_existing",
  "case_07_prompt_injection",
  "case_08_diagnosis_temptation",
  "case_09_nonvisit_hides_gap"
 ],
 "generated_at": "2026-11-02T04:48:31Z",
 "hashes": {
  "app/llm/lexicon.yaml": "a2518d8f098de26bf66777a51586da09d02f47cb50a542920498b5d38c089263",
  "app/llm/prompts/conflicts_v1.md": "16c18d05e68a5cfa0fa6496497b377dfbcda3c19fbf04dfaa9c9cf36139932ca",
  "app/llm/prompts/extract_es_v1.md": "985832562d871160eefe9f98eb9977e41fba6bf8fe672604b3f6043d337c93fb",
  "app/llm/prompts/extract_v1.md": "11a948d70400e97f958132495632d924bb07417dfa749ba6a992afcc11b989e2",
  "app/llm/prompts/flags_v1.md": "d5c3bf51cb2da188ddd5080e94cf37eff1d9b37afc21f29219e5480e01d18725",
  "app/llm/prompts/judge_amount_class_v1.md": "e7a7695ff9e73c0954a995534a3cfca33167b3d775b40bd5644d716196e869a8",
  "app/llm/prompts/judge_conflict_v1.md": "10c7cfddbd32d78cbdb005a14731abcb40ef55c83265b87abb88f74c48551daa",
  "app/llm/prompts/judge_conflict_v2.md": "6eac7a227ea9292e89350c3f10c11bc94d057b446cd3bf8cfde1a4684843cbc6",
  "app/llm/prompts/judge_faithfulness_es_v1.md": "d51be0b39c9d2ba0725f81b402e82e80696282bd0ea98e9ce789f575fa21f898",
  "app/llm/prompts/judge_faithfulness_v1.md": "636bd46d728af66608aba566efe431371e49e32a066fca71b2046534adbd002b",
  "app/llm/prompts/judge_flag_v1.md": "97dd90e3d9546a836d327e12953c9c30ba574ebdcc6073ada9162cd480d2e432",
  "app/llm/prompts/judge_flag_v2.md": "7b6b34712531643b0d79f3ccdd92932d8abb86bfdeeb756d7c39314e29ed39fe",
  "app/llm/prompts/narrative_v1.md": "3d75a823c717359208322d17ba8b77fd58893a4aa15bc92a18c48c78e94e12ac",
  "app/llm/prompts/split_v1.md": "9a2d0cffafa37f318e18a9c076c82f9f5c404ecb53781956813fafe7bf66197b"
 },
 "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
 "models": {
  "generator": "claude-sonnet-5-5",
  "judge": "claude-haiku-5-5"
 },
 "not_scored": {
  "amount": 0,
  "entry": 0,
  "flag": 0,
  "total": 0
 },
 "schema": "evals.calibration/1",
 "sentences": {
  "by_type": {
   "amount": {
    "needs_review": "Needs-review amounts matched the record 6/6 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified amounts matched the record 9/9 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "entry": {
    "needs_review": "Needs-review entries matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified entries matched the record 54/55 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   },
   "flag": {
    "needs_review": "Needs-review flags matched the record 2/2 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
    "verified": "Verified flags matched the record 20/20 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
   }
  },
  "overall": {
   "needs_review": "Items marked needs review matched the record 10/10 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).",
   "verified": "Verified items matched the record 83/84 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample)."
  }
 },
 "small_sample": true,
 "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
 "source_commit": "b85fc1b56386aa0d37460186b5840eec0e578642",
 "source_tree": "3f014d4b5d84f8731ff464d4548e18dfce3fbd4f",
 "source_tree_clean": true
}
--- evals/run.py at HEAD vs worktree:
run_py_diff_rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:22.949Z

**tool call — Bash**
````
{
 "command": "grep -n \"def git_source\\|def calibration\\|source_tree\\|source_commit\\|REPORTS\\s*=\\|write_calibration\\|def main\\|def build_report\\|def run_controls_only\\|def check_fresh\\|generated_at\" evals/run.py | head -80",
 "description": "Locate calibration and git_source functions in evals/run.py"
}
````

### User / tool · 2026-11-02T05:25:23.042Z

**tool result**
````
34:REPORTS = ROOT / "evals" / "reports"
71:def git_source(root=ROOT):
291:def calibration_sentences(by_state, cells, backend, case_count, not_scored, small_cases):
322:def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
347:    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
349:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
887:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None):
917:    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
921:    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
964:    L = ["", f"## Calibrated confidence (measured counts, backend `{c['backend']}`, {c['case_count']} golden cases, source commit `{(c.get('source_commit') or 'unknown')[:10]}`)", ""]
975:    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
1006:def write_calibration_refusal(src):
1016:def write_report(r, outdir=REPORTS, write_calibration=False):
1017:    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
1021:    ts = r["generated_at"].replace(":", "").replace("-", "")
1026:        if write_calibration:
1035:def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
1101:def run_controls_only(backend, out, ts):
1110:    (out / f"controls-{ts}.json").write_text(json.dumps({"schema": "evals.controls/1", "generated_at": ts, "backend": backend, "controls_ok": ok,
1116:def main(argv=None, pipeline=None):
1159:    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
1160:        why = write_calibration_refusal(git_source())
1170:    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
1172:        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
1176:    path = write_report(report, out, write_calibration=a.write_calibration)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:24.273Z

**tool call — Bash**
````
{
 "command": "sed -n 60,100p evals/run.py && echo ----- && sed -n 318,352p evals/run.py && echo ----- && sed -n 887,930p evals/run.py",
 "description": "Read git_source, build_calibration, build_report"
}
````

### User / tool · 2026-11-02T05:25:24.370Z

**tool result**
````
def ratio(num, den):
    return None if den == 0 else num / den


def golden_cases():
    names = ["sample"] + sorted(p.name[:-len(".expected.json")] for p in GOLD.glob("case_*.expected.json"))
    return [(n, (GOLD / f"{n}.txt").read_text(), json.loads((GOLD / f"{n}.expected.json").read_text())) for n in names]


def git_source(root=ROOT):
    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD} of the tree the numbers were produced from; Nones when git is unavailable.
    A calibration file is only traceable when it was produced from a clean tree (T-090 r2: generate in a clean worktree of HEAD)."""
    import subprocess
    try:
        head = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        tree = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD^{tree}"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
        return {"commit": head, "clean": not dirty, "tree": tree}
    except Exception:
        return {"commit": None, "clean": None, "tree": None}


def sha256_file(p):
    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()


def hashes(root=ROOT):
    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
    out = {}
    for p in sorted((root / "app" / "llm" / "prompts").glob("*.md")):
        out[p.relative_to(root).as_posix()] = sha256_file(p)
    lex = root / "app" / "llm" / "lexicon.yaml"
    if lex.exists():
        out[lex.relative_to(root).as_posix()] = sha256_file(lex)
    return out


def split_regex_text(s):
    return re.sub(r'"[^"]*"', " ", s or "")
-----
                                          f"No {s.replace('_', ' ')} {noun[t]} were seen in testing on the {backend} backend.")
    return sentences


def build_calibration(results, backend, models=None, generated_at=None, source=None, hashes_=None):
    """Pool score_calibration over the golden cases.  Only measured counts: N matched of M seen, with the cases they came from.
    Statements are generated here so the UI never composes a number of its own (and never shows a bare percentage)."""
    names = list(results)
    cells = {t: {s: {"matched": 0, "total": 0, "by_case": {}} for s in CAL_STATES} for t in CAL_TYPES}
    for n, r in results.items():
        for t in CAL_TYPES:
            for s in CAL_STATES:
                m, tot = r.get("calibration", {}).get(t, {}).get(s, [0, 0])
                c = cells[t][s]
                c["matched"] += m
                c["total"] += tot
                if tot:
                    c["by_case"][n] = [m, tot]
    by_state = {}
    for s in CAL_STATES:
        m = sum(cells[t][s]["matched"] for t in CAL_TYPES)
        tot = sum(cells[t][s]["total"] for t in CAL_TYPES)
        cs = sorted({n for t in CAL_TYPES for n in cells[t][s]["by_case"]})
        by_state[s] = {"matched": m, "total": tot, "cases": cs}
    small_cases = len(names) < CAL_SMALL_N
    not_scored = {t: sum(r.get("calibration_unscored", {}).get(t, 0) for r in results.values()) for t in CAL_TYPES}
    not_scored["total"] = sum(not_scored[t] for t in CAL_TYPES)

    sentences = calibration_sentences(by_state, cells, backend, len(names), not_scored, small_cases)
    return {"schema": "evals.calibration/1", "generated_at": generated_at, "backend": backend, "models": models or {},
            "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
            "match_rule": "entry: a golden entry is found in it; amount: same record, text, class and value as a golden amount; "
                          "flag: counted as correct by flag_precision. Rejected items and record warnings are not scored on purpose; "
                          "produced items with no usable state, and duplicate flags, are counted under not_scored. Records with no output are outside the count.",
-----
def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None):
    cases = cases or golden_cases()
    results, outs = run_cases(pipeline, backend, cases, runs_dir)
    m = aggregate(results)
    items, controls = load_jsonl(GOLD / "hallucinations.jsonl"), load_jsonl(GOLD / "hallucinations_controls.jsonl")
    if check_summary is None:
        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
        check_summary = GR.check_summary
    check = check_summary
    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
    m["case_07_total_420"] = case_07_total(results, outs)
    m["unsplit_paste"] = score_unsplit(pipeline, backend)
    sample = next(t for n, t, _ in cases if n == "sample")
    if backend in LIVE_BACKENDS:
        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
    else:
        m["determinism_3run"] = dict(NOT_MEASURED, r_ids=RIDS["determinism_3run"])
        m["unsupported_count_3run"] = dict(NOT_MEASURED, r_ids=RIDS["unsupported_count_3run"])
    if lexicon_flags is None:
        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
        lexicon_flags = FL.lexicon_flags
    m["lexicon_recall_must_flags"] = lexicon_recall(lexicon_flags, cases)
    if judge_control is None:
        m["judge_controls"] = {"status": "not_measured", "value": None, "reason": "no judge_control supplied", "r_ids": ["R-CO-2", "R-CO-3"]}
    else:
        m["judge_controls"] = judge_controls_metrics(load_controls(), judge_control, repeats=CONTROL_REPEATS if backend in LIVE_BACKENDS else 1)
    a = assertions(results)
    spec = check_spec(req_path)
    sample_out = outs.get("sample", {})
    source = git_source()
    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
              "hashes": hashes(), "metrics": m, "assertions": a, **spec, "per_case": results,
              "thresholds": THRESHOLDS, "cases": list(results)}
    report["calibration"] = build_calibration(results, report["backend"], report["models"], report["generated_at"], source, report["hashes"])
    if runs_dir is not None:
        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
    met, bars, blockers = evaluate_report(report)
    report.update(ship_bar_met=met, bars=bars, blockers=blockers)
    return report


# ---------------------------------------------------------------- output
def pct(x):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:24.723Z

**tool call — Bash**
````
{
 "command": "sed -n 1116,1184p evals/run.py && echo ----- && sed -n 1035,1100p evals/run.py",
 "description": "Read main() and check_fresh in evals/run.py"
}
````

### User / tool · 2026-11-02T05:25:24.821Z

**tool result**
````
def main(argv=None, pipeline=None):
    ap = argparse.ArgumentParser(prog="python -m evals.run")
    ap.add_argument("--check-fresh", action="store_true")
    ap.add_argument("--check-spec", action="store_true")
    ap.add_argument("--backend", default=None)
    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
    ap.add_argument("--out", default=str(REPORTS))
    ap.add_argument("--controls", action="store_true", help="run only the J3/J4 seeded controls (CONTROL_REPEATS repeats per item) and write controls-<ts>.md/.json")
    ap.add_argument("--write-calibration", action="store_true",
                    help="also write the committed calibration.json (out/calibration.json); refused unless the tracked tree is clean at HEAD (T-101)")
    a = ap.parse_args(argv)
    out = pathlib.Path(a.out)
    if a.check_fresh:
        return check_fresh(out / "latest.json")
    if a.check_spec:
        s = check_spec()
        latest = out / "latest.json"
        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
        data.update(s)
        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
        out.mkdir(parents=True, exist_ok=True)
        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
        print(json.dumps(s))
        return 0 if s["spec_matches_golden"] else 1
    try:
        refuse_curated()
    except CuratedFixtures as e:
        print(f"evals.run: {e}", file=sys.stderr)
        return 2
    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
    backend = normalize_backend(raw)
    if backend is None:
        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
              f"Nothing was run.", file=sys.stderr)
        return 2
    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
        if why:
            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
            return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
        cal = report.get("calibration") or {}
        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean")})
        if why:
            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
            return 2
    path = write_report(report, out, write_calibration=a.write_calibration)
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)


if __name__ == "__main__":
    sys.exit(main())
-----
def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
    p = pathlib.Path(latest_path)
    if not p.exists():
        print("check-fresh: no latest.json", file=sys.stderr)
        return 1
    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
    for k in diff:
        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
    bad = check_calibration(p.parent / "calibration.json", root)
    for m in bad:
        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
    return 1 if diff or bad else 0


def check_calibration(path, root=ROOT):
    """Problems with the served calibration.json (T-090 r2): totals that do not add up (a hand-edited count), or prompt/lexicon hashes that differ from the
    files on disk (the counts were measured against other prompts). Empty list when the file is absent or fine."""
    p = pathlib.Path(path)
    if not p.exists():
        return []
    c = json.loads(p.read_text())
    bad = []
    for s in CAL_STATES:
        for k in ("matched", "total"):
            if c["by_state"][s][k] != sum(c["by_type"][t][s][k] for t in CAL_TYPES):
                bad.append(f"by_state.{s}.{k} is not the sum of by_type")
    if c.get("sentences") != calibration_sentences(c["by_state"], c["by_type"], c["backend"], c["case_count"], c.get("not_scored") or {"total": 0}, c["case_count"] < CAL_SMALL_N):
        bad.append("sentences do not match the counts they are built from")
    old = c.get("hashes") or {}
    now = hashes(root)
    bad += [f"was measured against a different {k}" for k in sorted(set(old) | set(now)) if old and old.get(k) != now.get(k)]
    return bad


def load_pipeline():
    from app import pipeline
    return pipeline


class CuratedFixtures(Exception):
    pass


def refuse_curated(env=None):
    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
    env = os.environ if env is None else env
    d = env.get("LLM_FIXTURE_DIR", "").strip()
    curated_dir = ROOT / "tests" / "fixtures" / "llm" / "curated"
    in_curated = bool(d) and (pathlib.Path(d).resolve() == curated_dir.resolve() or curated_dir.resolve() in pathlib.Path(d).resolve().parents)
    if env.get("FIXTURE_SET", "").strip() == "curated" or in_curated:
        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under "
                              "tests/fixtures/llm/curated): curated responses reproduce the golden answers by construction (D-029). "
                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")


def normalize_backend(raw):
    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
    the caller must exit 2 rather than fall back to fixtures."""
    name = (raw or "").strip().lower() or "fixture"
    return name if name in KNOWN_BACKENDS else None
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:25:49.631Z

**tool call — Bash**
````
{
 "command": "git show 4c5f9bf -- tests/unit/test_eval_runner.py | head -260",
 "description": "Show T-101 test diff"
}
````

### User / tool · 2026-11-02T05:25:49.730Z

**tool result**
````
commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 23:24:43 2026 -0600

    fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
    
    A plain run now writes a scratch copy under evals/reports/runs/<ts>/calibration.json and never touches the committed file the app serves. --write-calibration writes evals/reports/calibration.json with the T-090 provenance header (source_commit, source_tree_clean, source_tree, hashes, backend), and is refused before any run unless the tracked tree is clean at HEAD; the header is re-checked after the run. Tests cover both behaviours, the real-git cleanliness rule, the no-git export, and the regeneration test (accepts the cited commit's own output location).
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index d21a423..d75b64c 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -424,7 +424,7 @@ def test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_norm
         return {"ship_bar_met": False, "backend": backend, "blockers": []}
     monkeypatch.setattr(R, "build_report", fake_build)
     monkeypatch.setattr(R, "load_pipeline", lambda: object())
-    monkeypatch.setattr(R, "write_report", lambda r, outdir=None: tmp_path / "x.json")
+    monkeypatch.setattr(R, "write_report", lambda r, outdir=None, **kw: tmp_path / "x.json")
     monkeypatch.setenv("LLM_BACKEND", " Claude-CLI ")
     monkeypatch.setenv("ENABLE_LIVE", "1")
     rc = R.main(["--out", str(tmp_path)])
@@ -608,9 +608,118 @@ def test_full_report_carries_calibration_and_write_report_emits_calibration_json
     c = rep["calibration"]
     assert c["backend"] == rep["backend"] and c["cases"] == rep["cases"]
     assert c["by_state"]["verified"]["total"] == sum(rep["per_case"][n]["calibration"][t]["verified"][1] for n in rep["per_case"] for t in R.CAL_TYPES)
-    R.write_report(rep, tmp_path)
-    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
-    assert "Calibrated confidence" in next(tmp_path.glob("2*.md")).read_text()
+    R.write_report(rep, tmp_path / "plain")
+    assert "Calibrated confidence" in next((tmp_path / "plain").glob("2*.md")).read_text()
+    assert json.loads(next((tmp_path / "plain" / "runs").glob("*/calibration.json")).read_text()) == json.loads(json.dumps(c))
+    R.write_report(rep, tmp_path / "committed", write_calibration=True)
+    assert json.loads((tmp_path / "committed" / "calibration.json").read_text()) == json.loads(json.dumps(c))
+
+
+# ---------------------------------------------------------------- T-101: a plain run never touches the committed calibration.json
+def _fake_report(monkeypatch, rep):
+    monkeypatch.setattr(R, "build_report", lambda *a, **k: copy.deepcopy(rep))
+    monkeypatch.setattr(R, "load_pipeline", lambda: object())
+    monkeypatch.delenv("LLM_BACKEND", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+
+
+def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
+    """T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy."""
+    committed = tmp_path / "calibration.json"
+    committed.write_text('{"sentinel": "committed file, must not change"}\n')
+    monkeypatch.setattr(R, "REPORTS", tmp_path)
+    _fake_report(monkeypatch, good)
+    before = committed.read_bytes()
+    assert R.main([]) == 0
+    assert committed.read_bytes() == before
+    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
+    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good["calibration"]))
+    assert list(tmp_path.glob("2*.md")) and (tmp_path / "latest.json").exists()
+
+
+def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
+    """T-101 AC1: a plain run is independent of git state; a dirty tree neither blocks it nor changes the committed file."""
+    monkeypatch.setattr(R, "REPORTS", tmp_path)
+    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": False, "tree": "b" * 40})
+    _fake_report(monkeypatch, good)
+    assert R.main([]) == 0
+    assert not (tmp_path / "calibration.json").exists()
+
+
+def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
+    """T-101: a tree dirtied during a long run must not produce a committed header that claims clean; nothing is written."""
+    monkeypatch.setattr(R, "git_source", lambda root=None: {"commit": "a" * 40, "clean": True, "tree": "b" * 40})   # clean at the start
+    def dirtied_during_run(*a, **k):
+        rep = copy.deepcopy(good)
+        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"],
+                                                 {"commit": "a" * 40, "clean": False, "tree": "b" * 40}, rep["hashes"])
+        return rep
+    monkeypatch.setattr(R, "build_report", dirtied_during_run)
+    monkeypatch.setattr(R, "load_pipeline", lambda: object())
+    monkeypatch.delenv("LLM_BACKEND", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
+    assert not (tmp_path / "calibration.json").exists() and not (tmp_path / "latest.json").exists()
+
+
+@pytest.mark.parametrize("src", [
+    {"commit": "a" * 40, "clean": False, "tree": "b" * 40},          # tracked edits or staged changes
+    {"commit": None, "clean": None, "tree": None},                    # no git at all (exported tree)
+])
+def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
+    """T-101 AC2: --write-calibration exits 2 before the pipeline runs and writes nothing."""
+    monkeypatch.setattr(R, "git_source", lambda root=None: src)
+    def must_not_run(*a, **k):
+        raise AssertionError("the pipeline ran although --write-calibration was refused")
+    monkeypatch.setattr(R, "build_report", must_not_run)
+    monkeypatch.setattr(R, "load_pipeline", lambda: object())
+    monkeypatch.delenv("LLM_BACKEND", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    assert R.main(["--write-calibration", "--out", str(tmp_path)]) == 2
+    assert list(tmp_path.iterdir()) == []
+
+
+def test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():
+    assert R.write_calibration_refusal({"commit": "a" * 40, "clean": True, "tree": "b" * 40}) is None
+    assert "uncommitted" in R.write_calibration_refusal({"commit": "a" * 40, "clean": False, "tree": "b" * 40})
+    assert R.write_calibration_refusal({"commit": None, "clean": None, "tree": None}) is not None
+
+
+def test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):
+    """T-101 AC2/AC3 on a real repository: allowed on a clean tracked tree (untracked files do not count), refused after a tracked edit and
+    leaves the file absent; the written header names HEAD, the clean flag, the tree and the prompt/lexicon hashes as T-090 defined them."""
+    if shutil.which("git") is None:
+        pytest.skip("git missing")
+    repo = tmp_path / "repo"
+    repo.mkdir()
+    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
+    subprocess.run(["git", "init", "-q", str(repo)], check=True)
+    (repo / "f").write_text("a")
+    subprocess.run(["git", "-C", str(repo), "add", "f"], check=True)
+    subprocess.run(["git", "-C", str(repo), "commit", "-qm", "x"], check=True, env=env)
+    head = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"], capture_output=True, text=True, check=True).stdout.strip()
+    real = R.git_source
+    monkeypatch.setattr(R, "git_source", lambda root=None: real(repo))
+    def fake_report(*a, **k):
+        rep = copy.deepcopy(good)
+        rep["calibration"] = R.build_calibration(rep["per_case"], rep["backend"], rep["models"], rep["generated_at"], R.git_source(), rep["hashes"])
+        return rep
+    monkeypatch.setattr(R, "build_report", fake_report)
+    monkeypatch.setattr(R, "load_pipeline", lambda: object())
+    monkeypatch.delenv("LLM_BACKEND", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    out = tmp_path / "out"
+    (repo / "untracked.txt").write_text("not tracked")
+    assert R.main(["--write-calibration", "--out", str(out)]) == 0
+    c = json.loads((out / "calibration.json").read_text())
+    assert c["schema"] == "evals.calibration/1" and c["source_commit"] == head and c["source_tree_clean"] is True
+    assert re.fullmatch(r"[0-9a-f]{40}", c["source_tree"]) and c["hashes"] == good["hashes"] and c["backend"] == good["backend"]
+    (out / "calibration.json").unlink()
+    (repo / "f").write_text("edited, not committed")
+    before = sorted(p.name for p in out.iterdir())
+    assert R.main(["--write-calibration", "--out", str(out)]) == 2
+    assert not (out / "calibration.json").exists()
+    assert sorted(p.name for p in out.iterdir()) == before          # the refused run wrote nothing new
 
 
 # ---------------------------------------------------------------- T-090 r2: the committed calibration.json is traceable and reproducible
@@ -677,14 +786,34 @@ def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_pa
     env["PYTHONPATH"] = str(src)
     out = tmp_path / "out"
     r = subprocess.run([sys.executable, "-m", "evals.run", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=600)
-    assert (out / "calibration.json").exists(), r.stdout[-400:] + r.stderr[-800:]
-    fresh = json.loads((out / "calibration.json").read_text())
+    # The cited commit's own code decides where the file lands: commits before T-101 write out/calibration.json, later ones only a
+    # scratch copy under out/runs/<ts>/ (T-101). Exactly one must exist either way.
+    found = [p for p in [out / "calibration.json", *sorted((out / "runs").glob("*/calibration.json"))] if p.exists()]
+    assert len(found) == 1, r.stdout[-400:] + r.stderr[-800:]
+    fresh = json.loads(found[0].read_text())
     git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
     assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
     assert {k: v for k, v in fresh.items() if k not in git_fields} == {k: v for k, v in c.items() if k not in git_fields}
     assert c["source_tree_clean"] is True
 
 
+def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
+    """T-101 AC2 end to end: an export of HEAD with no .git exits 2 before any run and writes nothing."""
+    if shutil.which("git") is None:
+        pytest.skip("git missing")
+    src = tmp_path / "src"
+    src.mkdir()
+    tar = subprocess.run(["git", "archive", "HEAD"], cwd=R.ROOT, capture_output=True, check=True).stdout
+    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
+    shutil.copy(R.ROOT / "evals" / "run.py", src / "evals" / "run.py")      # the working-tree runner (T-101 is not committed yet)
+    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
+    env["PYTHONPATH"] = str(src)
+    out = tmp_path / "out"
+    r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
+    assert r.returncode == 2 and "--write-calibration refused" in r.stderr, r.stderr[-800:]
+    assert not out.exists() or not any(out.iterdir())
+
+
 def test_git_source_reports_commit_and_dirtiness(tmp_path):
     if shutil.which("git") is None:
         pytest.skip("git missing")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:23.597Z

**tool call — Bash**
````
{
 "command": "sed -n 25,40p evals/run.py && echo ----- && grep -rn \"calibration.json\\|write-calibration\\|write_calibration\" --include=* -I . 2>/dev/null | grep -v \"^./evals/reports/\\|^./.git/\\|^./.venv/\\|agent-memory\\|^./tests/unit/test_eval_runner.py\" | head -40 && echo ----- && cat .gitignore | head -60 && echo ----- && grep -rn \"source_tree_clean\\|untracked\" memory/ spec/ docs/ board/cards/T-090.md board/cards/T-101.md 2>/dev/null | head -20",
 "description": "Find calibration.json consumers, gitignore rules, spec wording"
}
````

### User / tool · 2026-11-02T05:26:30.699Z

**tool result**
````
import os
import pathlib
import re
import sys

from evals.matching import assign_detail, norm

ROOT = pathlib.Path(__file__).resolve().parents[1]
GOLD = ROOT / "evals" / "golden"
REPORTS = ROOT / "evals" / "reports"
REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
LIVE_BACKENDS = ("claude-cli", "anthropic-api")
KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
NOT_MEASURED = {"value": None, "status": "not_measured"}

THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
-----
artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py:4:doc = json.loads((pathlib.Path(os.getcwd()) / "evals/reports/calibration.json").read_text())
artifacts/review-evidence/T-099-staff-engineer-r2-results.txt:23:== probes (serve verdict for a hand-edited copy of evals/reports/calibration.json at f345bc8)
artifacts/review-evidence/T-099-staff-engineer-probe-states.py:10:REAL = pathlib.Path(os.getcwd()) / "evals" / "reports" / "calibration.json"
artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py:96:print("== probes (serve verdict for a hand-edited copy of evals/reports/calibration.json at f345bc8)")
artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py:97:doc = json.loads((ARCH / "evals/reports/calibration.json").read_text())
artifacts/review-evidence/T-093-r2-HEAD/evals/run.py:971:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-093-r2-HEAD/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt:8:   run1 and run2 calibration.json are identical except generated_at (cmp of grep -v generated_at: byte-identical).
artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt:9:   Committed evals/reports/calibration.json vs run1 (generated_at removed, dict compare): True; vs run2: True.
artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt:13:2. Selector at 823b718 code + 02ff244 calibration.json (scratch clone):
artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt:24:   Copy: regen-02ff244-code/calibration.json.
artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt:26:5. Hand-edit mutants on the scratch clone (823b718 code, 02ff244 calibration.json). Selector result:
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:6:   $ git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:26:   copy: artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:27:   $ grep -c "%" evals/reports/calibration.json -> 0
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:39:   M5b calibration.json sentences.overall.verified 83/84 -> 84/84, check_fresh (clone, pristine code)
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:40:        -> returns 1; stderr "check-fresh: calibration.json sentences do not match the counts they are built from"
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:45:   unmodified calibration.json : 83 passed, 3 skipped (SKIPPED [2] test_eval_runner.py:636; SKIPPED [1] :661)
artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt:53:   T-096 shape (note) vs calibration.json keys: by_state, by_type, not_scored, sentences, case_count, small_sample,
artifacts/review-evidence/T-079-tree/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mutation-results.txt:7:M7 pooled total overwrites instead of sums: KILLED | 2 failed, 69 passed, 1046 deselected in 3.40s | tests/unit/test_eval_runner.py::test_build_calibration_pools_counts_names_cases_and_flags_small_samples; tests/unit/test_eval_runner.py::test_full_report_carries_calibration_and_write_report_emits_calibration_json
artifacts/review-evidence/T-090-staff/mutation-results.txt:8:M8 overall sentence shows a percentage: KILLED | 2 failed, 69 passed, 1046 deselected in 3.28s | tests/unit/test_eval_runner.py::test_build_calibration_pools_counts_names_cases_and_flags_small_samples; tests/unit/test_eval_runner.py::test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts
artifacts/review-evidence/T-090-staff/mut-M10/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M10/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M11/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M11/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M3/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M3/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M3/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M3/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
artifacts/review-evidence/T-090-staff/mut-M4/evals/run.py:911:        (outdir / "calibration.json").write_text(json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n")
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:494:def test_calibration_json_has_no_percentages_and_no_numbers_beyond_counts():
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:524:def test_full_report_carries_calibration_and_write_report_emits_calibration_json(good, tmp_path):
artifacts/review-evidence/T-090-staff/mut-M4/tests/unit/test_eval_runner.py:530:    assert json.loads((tmp_path / "calibration.json").read_text()) == json.loads(json.dumps(c))
-----
.env
.env.*
!.env.example
.venv/
__pycache__/
*.pyc
.pytest_cache/
node_modules/
.claude/agent-memory-local/
.claude/settings.local.json
artifacts/tmp/
board/.locks/
board/.stop_guard_state
board/.hook_debug.log
board/.server.log
app/db/*.sqlite3
*.sqlite3
.DS_Store
board/.hook_input_keys.log
board/.state.json
*.pem
*.key
id_rsa*
.envrc
*.env
.ruff_cache/
.coverage
*.log
.claude/scheduled_tasks.lock
-----
memory/LESSONS.md:26:- 2026-11-02T02:22:38Z **orchestrator**: Shared worktree + a shared file (api.py) edited by 3 backends: one commit swept others' uncommitted edits that import untracked files, breaking HEAD. Mitigation: commit new modules immediately (even as stubs) before wiring them into shared files; orchestrator checks HEAD importability at gates (git stash-free: 'git worktree add /tmp/headcheck HEAD && pytest -q').
board/cards/T-090.md:22:  - {"n": 1, "text": "evals report matched/seen counts for verified / needs_review items vs golden, in code-built sentences that name the backend and golden set, with no % and no invented numbers; served field and UI line are carried by T-096 (frontend)", "done": true, "evidence": "calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)"}
board/cards/T-090.md:44:- 2026-11-02T04:31:37Z qa: AC 1 checked: evals/reports/calibration.json generated from a clean worktree of 823b718 (source_commit, source_tree_clean=true, backend=fixture in header): verified 83/84, needs_review 10/10; tests/unit/test_eval_runner.py regenerates it from git archive of source_commit and compares; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 84 passed
board/cards/T-090.md:45:- 2026-11-02T04:31:37Z qa: r2: commits 823b718 (code, tests) and 02ff244 (calibration.json from clean worktree 823b718, worktree removed). Blocker: header has source_commit, source_tree_clean, backend, hashes; tests: ancestor-of-HEAD, regenerate-from-source-commit equality, check-fresh fails on edited count/changed hashes. Major 2: AC 1 narrowed to the eval side, served field + UI line is T-096. Major 3: amount class test. Major 4: sentences name backend + golden set (+ 'recorded replies' for fixture). Minors: 29/30 boundary, tolerated flag, record_warning alignment (state now travels with the candidate, no zip), not_scored counts, check-fresh covers calibration.json. Nit: 7 tests originally, not 6; selector now gives 84. generated_at kept in file (test ignores it). Not done: latest.json/.md not regenerated (latest.json is the live claude-cli report). FOR FRONTEND T-096: sentences now end with backend+basis already, render verbatim.
board/cards/T-090.md:53:    - [minor] The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes — fix: Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.
board/cards/T-090.md:58:- 2026-11-02T04:48:59Z qa: AC 1 checked: calibration.json regenerated from a clean worktree of b85fc1b (source_commit, source_tree_clean=true, source_tree, backend=fixture): verified 83/84, needs_review 10/10; test_eval_runner: forged source_commit fails (no skip) when a repo exists, regenerates from git archive of source_commit and compares, source_tree checked against git; check-fresh rebuilds sentences; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 86 passed, 0 skipped; served field+UI moved to T-096 (note posted with field shape)
board/cards/T-101.md:30:What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-calibration writes out/calibration.json with the T-090 header (source_commit, source_tree_clean, source_tree, hashes, backend), refused (exit 2, nothing run) unless the tracked tree is clean at HEAD, re-checked after the run. Tests: tests/unit/test_eval_runner.py (+6 new, 4 updated for the new location). How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 124 passed, 0 skipped; committed calibration.json is byte-identical to HEAD (restored and still identical after the run); real CLI plain run to a scratch --out rc=1 (fixture ship bar, expected) with calibration untouched; --write-calibration on this dirty tree rc=2, nothing written. Left: latest.json and the .md are still written by every run as before (not in scope). Other agents' uncommitted changes in the shared tree were left alone; the commit used --only paths. Surprise: the regeneration test replays the cited commit's own code, so it accepts the old out/calibration.json location as well as the new runs/ scratch copy. Note for orchestrator: --write-calibration does not restrict backend; the committed-header test pins backend=fixture, so a live write would fail that test by design.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:36.483Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/t101/archive\" && cd /Users/arsis/zlayt-pm-project && git archive 4c5f9bf | tar -x -C \"$S/t101/archive\" && echo \"archive_rc=$?\" && cd \"$S/t101/archive\" && ls && /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import evals.run as R, app; print(R.ROOT); print(app.__file__)\" && cmp evals/reports/calibration.json /Users/arsis/zlayt-pm-project/evals/reports/calibration.json && echo \"archive calib identical to project working copy\" && git -C /Users/arsis/zlayt-pm-project rev-parse 4c5f9bf^{tree}",
 "description": "Extract git archive of 4c5f9bf into scratchpad and verify imports"
}
````

### User / tool · 2026-11-02T05:26:36.965Z

**tool result**
````
archive_rc=0
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
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/archive
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/archive/app/__init__.py
archive calib identical to project working copy
4b4960da2d9e52141982b125dc986f0b22344360
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:40.379Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/t101/archive\"; cd \"$A\" && echo \"before: $(shasum -a 256 evals/reports/calibration.json)\" && env -u LLM_BACKEND -u ENABLE_LIVE -u LLM_FIXTURE_DIR -u FIXTURE_SET /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run; echo \"plain_rc=$?\"; echo \"after:  $(shasum -a 256 evals/reports/calibration.json)\"; cmp evals/reports/calibration.json /Users/arsis/zlayt-pm-project/evals/reports/calibration.json && echo \"still identical to HEAD copy\"; ls -la evals/reports/runs/ && find evals/reports/runs -name calibration.json -newer evals/run.py -print",
 "description": "Plain evals.run in archive copy; compare calibration.json hash before and after"
}
````

### User / tool · 2026-11-02T05:26:41.785Z

**tool result**
````
before: 49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
llm call failed call_id=c848dcb7b682e step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c4b3ac835c0dd step=extract attempt=1 prompt_hash=4b3235bcc27fc57d8df381ddb636080623de75ee126ef90ad5acc8fb69609bfb
llm call failed call_id=c8159d87c2946 step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
llm call failed call_id=c49a0c5eb5545 step=conflicts attempt=1 prompt_hash=72f2b8a330ffbf0fe899b1558f048a20e812d19112dca07a3b4e2469aba19140
llm call failed call_id=c903d546f65ac step=flags attempt=1 prompt_hash=aba7985fd2cf66130a268227a931481f6fd49a86d8fc7dc85134687ef05737ef
llm call failed call_id=c69669e3cf04f step=flags attempt=1 prompt_hash=6492c1869040382bbd047206c9f36c4c49e8a71b2c3d09c8de75be6be2747427
llm call failed call_id=c9993209f0f44 step=flags attempt=1 prompt_hash=8ef7ba54619423c4d84c9bc0e224a30770fe63001b5b91d7bb0db899efbdffef
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/archive/evals/reports/20261102T052641Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
plain_rc=1
after:  49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
still identical to HEAD copy
total 0
drwxr-xr-x@  5 arsis  wheel  160 Nov  1 23:26 .
drwxr-xr-x@ 23 arsis  wheel  736 Nov  1 23:26 ..
drwxr-xr-x@ 15 arsis  wheel  480 Nov  1 23:24 20261102T034706Z
drwxr-xr-x@ 15 arsis  wheel  480 Nov  1 23:24 20261102T035806Z
drwxr-xr-x@  3 arsis  wheel   96 Nov  1 23:26 20261102T052641Z
evals/reports/runs/20261102T052641Z/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:46.994Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; A=\"$S/t101/archive\"; cd \"$A\" && ls -la --time-style=+%T evals/reports/latest.json | cat; env -u LLM_BACKEND -u ENABLE_LIVE -u LLM_FIXTURE_DIR -u FIXTURE_SET /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration --out \"$S/t101/out-nogit\" ; echo \"wc_nogit_rc=$?\"; ls -la \"$S/t101/out-nogit\" 2>&1 | head; echo \"--- evals/reports/calibration.json still:\"; shasum -a 256 evals/reports/calibration.json; echo \"--- in-tree default out (--write-calibration, no --out) without git:\"; env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration; echo \"rc=$?\"; shasum -a 256 evals/reports/calibration.json",
 "description": "Run --write-calibration in git-less archive copy; expect refusal"
}
````

### User / tool · 2026-11-02T05:26:47.272Z

**tool result**
````
ls: unrecognized option `--time-style=+%T'
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
evals.run: --write-calibration refused, nothing was run or written: no git repository or HEAD commit is available to name as the source.
wc_nogit_rc=2
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/out-nogit: No such file or directory
--- evals/reports/calibration.json still:
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
--- in-tree default out (--write-calibration, no --out) without git:
evals.run: --write-calibration refused, nothing was run or written: no git repository or HEAD commit is available to name as the source.
rc=2
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:51.617Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101\" && git clone -q --no-hardlinks /Users/arsis/zlayt-pm-project clone && cd clone && git checkout -q --detach 4c5f9bf && git rev-parse HEAD && git rev-parse HEAD^{tree} && echo \"tracked-dirty lines: $(git status --porcelain --untracked-files=no | wc -l)\" && git log --oneline -1 b85fc1b && cp evals/reports/calibration.json \"$S/t101/calibration.HEAD.json\" && shasum -a 256 evals/reports/calibration.json && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration 2>&1 | tail -4; echo \"wc_clean_rc=${PIPESTATUS[0]}\"; shasum -a 256 evals/reports/calibration.json",
 "description": "Clone project at 4c5f9bf and run --write-calibration on clean tree"
}
````

### User / tool · 2026-11-02T05:26:54.863Z

**tool result**
````
4c5f9bf909253bfffa55cb41b1350c412c56e6da
4b4960da2d9e52141982b125dc986f0b22344360
tracked-dirty lines:        0
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
ship_bar_met=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/clone/evals/reports/20261102T052654Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
wc_clean_rc=1
2adb49d1465200bacbd06096c07ecae3c4870ae3b619bd4a6c0e6698f9f297a4  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:26:59.088Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json,sys\nnew=json.load(open('evals/reports/calibration.json')); old=json.load(open(sys.argv[1]))\nfor k in ('generated_at','source_commit','source_tree_clean','source_tree','backend','schema'):\n    print(k, '| old:', old.get(k), '| new:', new.get(k))\ng=('generated_at','source_commit','source_tree_clean','source_tree')\nprint('non-git fields identical:', {k:v for k,v in new.items() if k not in g}=={k:v for k,v in old.items() if k not in g})\nprint('by_state new:', new['by_state']['verified']['matched'], new['by_state']['verified']['total'], new['by_state']['needs_review']['matched'], new['by_state']['needs_review']['total'])\n\" \"$S/t101/calibration.HEAD.json\"; grep -c \"\" evals/reports/calibration.json; head -c 300 evals/reports/calibration.json; echo; cat evals/reports/calibration.json | tail -6",
 "description": "Verify written calibration header fields against HEAD copy"
}
````

### User / tool · 2026-11-02T05:26:59.231Z

**tool result**
````
generated_at | old: 2026-11-02T04:48:31Z | new: 2026-11-02T05:26:54Z
source_commit | old: b85fc1b56386aa0d37460186b5840eec0e578642 | new: 4c5f9bf909253bfffa55cb41b1350c412c56e6da
source_tree_clean | old: True | new: True
source_tree | old: 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f | new: 4b4960da2d9e52141982b125dc986f0b22344360
backend | old: fixture | new: fixture
schema | old: evals.calibration/1 | new: evals.calibration/1
non-git fields identical: True
by_state new: 83 84 10 10
267
{
 "backend": "fixture",
 "by_state": {
  "needs_review": {
   "cases": [
    "case_01_date_formats",
    "case_03_rate_and_ocr",
    "case_06_subtle_pre_existing",
    "case_07_prompt_injection",
    "sample"
   ],
   "matched": 10,
   "total": 10
  },
  "verified": {
   "cases": [
    "case_01_dat
 "small_sample": true,
 "source": "evals.run over the golden cases; measured counts only (D-042, scope cut 10)",
 "source_commit": "4c5f9bf909253bfffa55cb41b1350c412c56e6da",
 "source_tree": "4b4960da2d9e52141982b125dc986f0b22344360",
 "source_tree_clean": true
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:04.073Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && echo \"# reviewer dirty probe\" >> README.md && git status --porcelain --untracked-files=no && shasum -a 256 evals/reports/calibration.json && ls evals/reports/runs | wc -l && ls evals/reports/*.md | wc -l && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration; echo \"wc_dirty_rc=$?\"; shasum -a 256 evals/reports/calibration.json && ls evals/reports/runs | wc -l && ls evals/reports/*.md | wc -l && echo \"--- plain run on dirty tree:\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run >/dev/null 2>&1; echo \"plain_dirty_rc=$?\"; shasum -a 256 evals/reports/calibration.json; ls evals/reports/runs | wc -l; git checkout -q -- README.md && git status --porcelain --untracked-files=no | wc -l",
 "description": "Dirty-tree probe: refused --write-calibration, plain run leaves file alone"
}
````

### User / tool · 2026-11-02T05:27:05.575Z

**tool result (error)**
````
Exit code 1
 M evals/reports/calibration.json
 M evals/reports/latest.json
2adb49d1465200bacbd06096c07ecae3c4870ae3b619bd4a6c0e6698f9f297a4  evals/reports/calibration.json
       2
      17
evals.run: --write-calibration refused, nothing was run or written: the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD.
wc_dirty_rc=2
2adb49d1465200bacbd06096c07ecae3c4870ae3b619bd4a6c0e6698f9f297a4  evals/reports/calibration.json
       2
      17
--- plain run on dirty tree:
plain_dirty_rc=1
2adb49d1465200bacbd06096c07ecae3c4870ae3b619bd4a6c0e6698f9f297a4  evals/reports/calibration.json
       3
error: pathspec 'README.md' did not match any file(s) known to git
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:20.989Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && git checkout -q -- evals/reports/calibration.json evals/reports/latest.json && rm -f README.md && git status --porcelain --untracked-files=no | wc -l && git ls-files | grep -n \"CLAUDE.md\\|RUNBOOK\\|requirements.txt\" | head -5; git ls-files | wc -l; shasum -a 256 evals/reports/calibration.json",
 "description": "Reset scratch clone's tracked report files and remove stray probe file"
}
````

### User / tool · 2026-11-02T05:27:21.302Z

**tool result**
````
       0
102:CLAUDE.md
350:docs/RUNBOOK.md
488:requirements.txt
    1806
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:25.616Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && echo \"<!-- reviewer dirty probe -->\" >> docs/RUNBOOK.md && git status --porcelain --untracked-files=no && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration; echo \"wc_dirty_rc=$?\"; shasum -a 256 evals/reports/calibration.json; ls evals/reports/runs | wc -l; git checkout -q -- docs/RUNBOOK.md && git status --porcelain --untracked-files=no | wc -l",
 "description": "Clean-HEAD dirty probe: edit tracked doc, expect --write-calibration refusal"
}
````

### User / tool · 2026-11-02T05:27:25.890Z

**tool result**
````
 M docs/RUNBOOK.md
evals.run: --write-calibration refused, nothing was run or written: the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD.
wc_dirty_rc=2
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
       3
       0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:29.649Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && cp evals/golden/case_01_date_formats.txt evals/golden/case_zz_untracked.txt && cp evals/golden/case_01_date_formats.expected.json evals/golden/case_zz_untracked.expected.json && git status --porcelain --untracked-files=no | wc -l && git status --porcelain | head -3 && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration 2>&1 | head -2; echo \"wc_untracked_rc=${PIPESTATUS[0]}\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nc=json.load(open('evals/reports/calibration.json'))\nprint('source_commit', c['source_commit']); print('source_tree', c['source_tree']); print('source_tree_clean', c['source_tree_clean'])\nprint('case_count', c['case_count']); print('cases includes case_zz:', 'case_zz_untracked' in c['cases'])\nprint('hashes keys', len(c['hashes']))\nprint('by_state verified', c['by_state']['verified']['matched'], c['by_state']['verified']['total'])\n\"; git ls-tree -r --name-only 4b4960da | grep -c \"case_zz\" ; git ls-files --others --exclude-standard | grep -c \"case_zz\"",
 "description": "Untracked golden case probe: header still claims clean HEAD tree"
}
````

### User / tool · 2026-11-02T05:27:31.501Z

**tool result**
````
       0
?? evals/golden/case_zz_untracked.expected.json
?? evals/golden/case_zz_untracked.txt
?? evals/reports/20261102T052654Z.md
llm call failed call_id=c596fd06aeb47 step=extract attempt=1 prompt_hash=e02650eaff3b56a59664e6c6efe611cfde00a438a6671ac91403a65ebcdb3431
llm call failed call_id=c25554461312d step=extract attempt=1 prompt_hash=dd11310acca4a716f8a2e2bd69d7bac58b0fb9eb95ccb23835d4e980bdde1011
wc_untracked_rc=120
source_commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da
source_tree 4b4960da2d9e52141982b125dc986f0b22344360
source_tree_clean True
case_count 11
cases includes case_zz: True
hashes keys 14
by_state verified 91 92
0
2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:37.064Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration > \"$S/t101/untracked-run.log\" 2>&1; echo \"wc_untracked_rc=$?\"; tail -3 \"$S/t101/untracked-run.log\"; grep -o '\"generated_at\": \"[^\"]*\"\\|\"source_tree_clean\": [a-z]*' evals/reports/calibration.json; git status --porcelain --untracked-files=no | wc -l",
 "description": "Re-run --write-calibration with untracked golden case, capture rc and header"
}
````

### User / tool · 2026-11-02T05:27:37.313Z

**tool result**
````
wc_untracked_rc=2
evals.run: --write-calibration refused, nothing was run or written: the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files); commit or stash, or run from a clean worktree of HEAD.
"generated_at": "2026-11-02T05:27:31Z"
"source_tree_clean": true
       2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:40.550Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && git checkout -q -- evals/reports/calibration.json evals/reports/latest.json && git status --porcelain --untracked-files=no | wc -l && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration > \"$S/t101/untracked-run.log\" 2>&1; echo \"wc_untracked_rc=$?\"; tail -2 \"$S/t101/untracked-run.log\" | cut -c1-200; grep -o '\"generated_at\": \"[^\"]*\"\\|\"source_tree_clean\": [a-z]*\\|\"source_tree\": \"[^\"]*\"\\|\"source_commit\": \"[^\"]*\"\\|\"case_count\": [0-9]*' evals/reports/calibration.json; git ls-tree -r --name-only 4b4960da | grep -c \"case_zz\"",
 "description": "Restore tracked outputs and rerun untracked golden case probe cleanly"
}
````

### User / tool · 2026-11-02T05:27:42.007Z

**tool result**
````
       0
wc_untracked_rc=1
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
"case_count": 11
"generated_at": "2026-11-02T05:27:41Z"
"source_commit": "4c5f9bf909253bfffa55cb41b1350c412c56e6da"
"source_tree": "4b4960da2d9e52141982b125dc986f0b22344360"
"source_tree_clean": true
0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:27:54.610Z

**tool call — Bash**
````
{
 "command": "shasum -a 256 evals/reports/calibration.json evals/reports/latest.json > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/proj-before.sha 2>/dev/null; ls -la /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/ | head -3; shasum -a 256 evals/reports/calibration.json evals/reports/latest.json; .venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -15; echo \"pytest_rc=${PIPESTATUS[0]}\"; shasum -a 256 evals/reports/calibration.json evals/reports/latest.json",
 "description": "Run T-101 pytest selection in project tree and check report files unchanged",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:28:04.092Z

**tool result**
````
total 40
drwxr-xr-x@   9 arsis  wheel    288 Nov  1 23:27 .
drwx------@ 655 arsis  wheel  20960 Nov  1 23:27 ..
3815c6ce652831ac5296b043e538144981edb14018bb9ec9e0821a3415cd70d0  evals/reports/calibration.json
4fe3b264e77c5b05557498100faf91492d288b7405a0781fbe488e01f303d6e9  evals/reports/latest.json
        git_fields = ("generated_at", "source_commit", "source_tree_clean", "source_tree")
>       assert fresh["by_state"] == c["by_state"] and fresh["by_type"] == c["by_type"] and fresh["sentences"] == c["sentences"]
E       AssertionError: assert ({'needs_revie... 'total': 84}} == {'needs_revie... 'total': 85}}
E         
E         Differing items:
E         {'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', ...], 'matched': 83, 'total': 84}} != {'verified': {'cases': ['case_01_date_formats', 'case_02_gap_boundaries', 'case_03_rate_and_ocr', 'case_04_duplicates_no_amounts', 'case_05_provider_conflict', 'case_06_subtle_pre_existing', ...], 'matched': 83, 'total': 85}}
E         {'needs_review': {'cases': ['case_01_date_formats', 'case_03_rate_and_ocr', 'case_06_subtle_pre_existing',...
E         
E         ...Full output truncated, use '-vv' to show)

tests/unit/test_eval_runner.py:795: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_header_names_backend_and_a_clean_source_commit
FAILED tests/unit/test_eval_runner.py::test_committed_calibration_regenerates_exactly_from_its_source_commit
2 failed, 122 passed, 1825 deselected in 9.01s
pytest_rc=1
3815c6ce652831ac5296b043e538144981edb14018bb9ec9e0821a3415cd70d0  evals/reports/calibration.json
4fe3b264e77c5b05557498100faf91492d288b7405a0781fbe488e01f303d6e9  evals/reports/latest.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:28:12.346Z

**tool call — Bash**
````
{
 "command": "stat -f '%Sm %N' -t '%Y-%m-%dT%H:%M:%S' evals/reports/calibration.json evals/reports/latest.json && date -u +%Y-%m-%dT%H:%M:%SZ && git status --porcelain -- evals/reports/calibration.json && git rev-parse HEAD && git log --oneline -3 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nc=json.load(open('evals/reports/calibration.json'))\nprint('generated_at', c.get('generated_at'), 'source_commit', c.get('source_commit'), 'clean', c.get('source_tree_clean'), 'tree', c.get('source_tree'), 'case_count', c.get('case_count'), 'cases', c.get('cases')[-2:])\nprint('verified total', c['by_state']['verified']['total'], 'matched', c['by_state']['verified']['matched'])\n\" && cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t101/proj-before.sha; ls -la evals/golden/ | grep -i \"case_\" | wc -l; ls evals/golden | grep -v \"^case_0[0-9]\\|sample\" | head -20",
 "description": "Investigate who changed the project calibration.json since review start"
}
````

### User / tool · 2026-11-02T05:28:12.569Z

**tool result**
````
2026-11-01T23:27:16 evals/reports/calibration.json
2026-11-01T23:27:16 evals/reports/latest.json
2026-11-02T05:28:12Z
 M evals/reports/calibration.json
4c5f9bf909253bfffa55cb41b1350c412c56e6da
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
generated_at 2026-11-02T05:27:16Z source_commit 4c5f9bf909253bfffa55cb41b1350c412c56e6da clean False tree 4b4960da2d9e52141982b125dc986f0b22344360 case_count 10 cases ['case_08_diagnosis_temptation', 'case_09_nonvisit_hides_gap']
verified total 85 matched 83
3815c6ce652831ac5296b043e538144981edb14018bb9ec9e0821a3415cd70d0  evals/reports/calibration.json
4fe3b264e77c5b05557498100faf91492d288b7405a0781fbe488e01f303d6e9  evals/reports/latest.json
      18
README.md
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
judge_controls.CHANGELOG.md
judge_controls.jsonl
judge_controls_heldout.jsonl
unsplit_paste.split.json
unsplit_paste.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:28:44.358Z

**tool call — Bash**
````
{
 "command": "grep -n '2026-11-02T05:2[4-9]' board/activity.jsonl | cut -c1-260; echo ---; ls -la --time-style=long-iso evals/reports/runs | tail -5; ls evals/reports | grep \"20261102T0527\\|20261102T0526\" ; echo ---; /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nl=json.load(open('evals/reports/latest.json'))\nprint('latest generated_at', l.get('generated_at'), 'backend', l.get('backend'), 'source_tree_clean' , l.get('calibration',{}).get('source_tree_clean'), 'cases', len(l.get('cases',[])))\n\"",
 "description": "Check board activity and report files around the 05:27 write"
}
````

### User / tool · 2026-11-02T05:28:44.494Z

**tool result**
````
2399:{"ts": "2026-11-02T05:24:59Z", "event": "ac", "agent": "qa", "card": "T-101", "text": "AC 1 checked: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched, ::test_plain_run_with_dirty_tree_still_never_writes_calibratio
2400:{"ts": "2026-11-02T05:24:59Z", "event": "commit", "agent": "qa", "card": "T-101", "text": "4c5f9bf"}
2401:{"ts": "2026-11-02T05:24:59Z", "event": "handoff", "agent": "qa", "card": "T-101", "text": "What changed: evals/run.py - a plain run writes a scratch copy to evals/reports/runs/<ts>/calibration.json and never the committed calibration.json; new --write-ca
2402:{"ts": "2026-11-02T05:25:00Z", "event": "move", "agent": "qa", "card": "T-101", "text": "in_progress -> in_review", "status": "in_review"}
2403:{"ts": "2026-11-02T05:25:05Z", "event": "dispatch", "agent": "orchestrator", "card": "T-101", "text": "review dispatched: staff-engineer-reviewer"}
2404:{"ts": "2026-11-02T05:25:41Z", "event": "review", "agent": "orchestrator", "card": "T-097", "text": "review ux-designer-reviewer (claude-haiku-5-5): fail — reviews/T-097-ux-designer-r2.md", "persona": "ux-designer-reviewer", "verdict": "fail", "file": "
2405:{"ts": "2026-11-02T05:25:41Z", "event": "claim", "agent": "frontend", "card": "T-097", "text": "Rerun-check feedback and judge-panel/gate agreement (T-081/T-082 r3 majors)"}
2406:{"ts": "2026-11-02T05:25:41Z", "event": "note", "agent": "orchestrator", "card": "T-097", "text": "r2 blocker is backend (gate trusted stored check results): routed to T-098 r2 (recompute at gate time). Round 3 here re-verifies the UI once T-098 lands; fi
2407:{"ts": "2026-11-02T05:25:41Z", "event": "assign", "agent": "orchestrator", "card": "T-097", "text": "assigned to frontend"}
2408:{"ts": "2026-11-02T05:25:48Z", "event": "review", "agent": "orchestrator", "card": "T-100", "text": "review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-100-staff-engineer.md", "persona": "staff-engineer-reviewer", "verdict": "fail", "fi
2409:{"ts": "2026-11-02T05:25:48Z", "event": "claim", "agent": "backend", "card": "T-100", "text": "Implement D-047: side/negation/qualifier tokens missing from the excerpt are a hard 422 on edit and manual entry; remove the 409 keep-my-wording path"}
2410:{"ts": "2026-11-02T05:26:30Z", "event": "review", "agent": "orchestrator", "card": "T-099", "text": "review staff-engineer-reviewer (claude-haiku-5-5): pass — reviews/T-099-staff-engineer-r2.md", "persona": "staff-engineer-reviewer", "verdict": "pass", 
2411:{"ts": "2026-11-02T05:26:30Z", "event": "move", "agent": "orchestrator", "card": "T-099", "text": "in_review -> done", "status": "done"}
2412:{"ts": "2026-11-02T05:26:30Z", "event": "new", "agent": "orchestrator", "card": "T-102", "text": "Calibration staleness: served calibration.json must flag when its prompt hashes no longer match HEAD (before M3 gate)", "milestone": "M3", "role": "qa"}
---
ls: unrecognized option `--time-style=long-iso'
usage: ls [-@ABCFGHILOPRSTUWXabcdefghiklmnopqrstuvwxy1%,] [--color=when] [-D format] [file ...]
20261102T052638Z.md
20261102T052716Z.md
---
latest generated_at 2026-11-02T05:27:16Z backend claude-cli source_tree_clean False cases 10
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:28:51.847Z

**tool call — Bash**
````
{
 "command": "ls evals/reports/runs/ && echo --- && ps -axo pid,lstart,command | grep -i \"evals.run\\|evals/run\" | grep -v grep | head -10; echo --- && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"\nimport json\nc=json.load(open('evals/reports/calibration.json'))\nprint('header backend', c['backend'], 'models', c.get('models'), 'generated_at', c['generated_at'])\n\" && grep -n \"05:2[0-3]\" board/activity.jsonl | grep -i \"eval\\|calib\\|live\\|claude-cli\" | cut -c1-220 | tail -8",
 "description": "Check running eval processes, run dirs, and the header backend"
}
````

### User / tool · 2026-11-02T05:28:52.029Z

**tool result**
````
20261102T034706Z
20261102T035806Z
20261102T042232Z
20261102T045543Z
20261102T051136Z
20261102T052638Z
---
---
header backend claude-cli models {'generator': 'claude-sonnet-5-5', 'judge': 'claude-haiku-5-5'} generated_at 2026-11-02T05:27:16Z
2391:{"ts": "2026-11-02T05:20:58Z", "event": "ac", "agent": "backend", "card": "T-099", "text": "AC 1 checked: tests/unit/test_calibration_route.py: 30 passed (route file alone; includes state-total hand-edit test, mutan
2392:{"ts": "2026-11-02T05:20:58Z", "event": "handoff", "agent": "backend", "card": "T-099", "text": "r2 fixes (commit f345bc8, app/backend/calibration_route.py + tests/unit/test_calibration_route.py only)."}
2396:{"ts": "2026-11-02T05:21:08Z", "event": "new", "agent": "orchestrator", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a cl
2398:{"ts": "2026-11-02T05:21:14Z", "event": "claim", "agent": "qa", "card": "T-101", "text": "evals.run must not overwrite the committed calibration.json by default (write only with --write-calibration from a clean HEAD
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:29:32.302Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && rm -f evals/golden/case_zz_untracked.txt evals/golden/case_zz_untracked.expected.json && git checkout -q -- evals/reports/calibration.json evals/reports/latest.json && git status --porcelain --untracked-files=no | wc -l && git rev-parse HEAD && shasum -a 256 evals/reports/calibration.json && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" -p no:cacheprovider 2>&1 | tail -4; echo \"clone_pytest_rc=${PIPESTATUS[0]}\"; git status --porcelain --untracked-files=no | wc -l; shasum -a 256 evals/reports/calibration.json",
 "description": "Restore clone to HEAD state and run T-101 pytest selection at 4c5f9bf",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T05:29:41.403Z

**tool result**
````
       0
4c5f9bf909253bfffa55cb41b1350c412c56e6da
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
........................................................................ [ 58%]
....................................................                     [100%]
124 passed, 1732 deselected in 8.60s
clone_pytest_rc=0
       0
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:29:57.682Z

**tool call — Bash**
````
{
 "command": "mkdir -p artifacts/review-evidence/T-101-staff-engineer && cat > artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py <<'EOF'\n\"\"\"T-101 mutation driver (staff-engineer-reviewer). Run with: <venv>/bin/python -I mutate_guard.py <clone_dir> <evidence_dir>.\nEach mutant is one exact-anchor edit to evals/run.py in a scratch clone at 4c5f9bf; the anchor must occur exactly once.\nRuns the T-101 selection, records the summary line and failing test names, then restores the pristine file byte for byte.\"\"\"\nimport os\nimport pathlib\nimport subprocess\nimport sys\n\nclone = pathlib.Path(sys.argv[1])\nevid = pathlib.Path(sys.argv[2])\nrun_py = clone / \"evals\" / \"run.py\"\npristine = run_py.read_bytes()\n(evid / \"run.py.pristine\").write_bytes(pristine)\nenv = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\", \"LLM_FIXTURE_DIR\", \"FIXTURE_SET\")}\nPY = \"/Users/arsis/zlayt-pm-project/.venv/bin/python\"\n\nMUTANTS = [\n    (\"M1 plain run writes the committed calibration.json\",\n     \"        if write_calibration:\\n\", \"        if True:\\n\"),\n    (\"M2 pre-run refusal removed (pipeline runs before the guard)\",\n     \"    if a.write_calibration:                          # T-101: refuse before any run is paid for\",\n     \"    if False:                                        # T-101: refuse before any run is paid for\"),\n    (\"M3 post-run header recheck removed\",\n     \"    if a.write_calibration:                          # the tree can be dirtied during a long run\",\n     \"    if False:                                        # the tree can be dirtied during a long run\"),\n    (\"M4 refusal rule ignores a dirty tree\",\n     '    if not src[\"clean\"]:', \"    if False:\"),\n    (\"M5 dirty check counts untracked files\",\n     '\"status\", \"--porcelain\", \"--untracked-files=no\"', '\"status\", \"--porcelain\"'),\n    (\"M6 --write-calibration flag not passed to write_report\",\n     \"write_report(report, out, write_calibration=a.write_calibration)\", \"write_report(report, out)\"),\n    (\"M7 header source_tree_clean hard-coded True\",\n     '\"source_tree_clean\": (source or {}).get(\"clean\")', '\"source_tree_clean\": True'),\n    (\"M8 no-git clause dropped from refusal (message becomes 'uncommitted changes')\",\n     '    if src.get(\"commit\") is None or src.get(\"clean\") is None:', '    if src.get(\"commit\") is None:'),\n]\n\ndef run_tests():\n    r = subprocess.run([PY, \"-m\", \"pytest\", \"-q\", \"tests/unit\", \"-k\", \"calibration or eval_runner\", \"-p\", \"no:cacheprovider\", \"-rfE\"],\n                       cwd=clone, env=env, capture_output=True, text=True, timeout=900)\n    lines = r.stdout.strip().splitlines()\n    summary = lines[-1] if lines else \"(no output)\"\n    fails = [l.split(\" - \")[0].replace(\"FAILED \", \"\").replace(\"ERROR \", \"\") for l in lines if l.startswith((\"FAILED\", \"ERROR\"))]\n    return r.returncode, summary, fails\n\nrc, summary, _ = run_tests()\nprint(f\"BASELINE rc={rc} | {summary}\")\nassert rc == 0, \"baseline must be green before mutating\"\nfor name, old, new in MUTANTS:\n    text = pristine.decode()\n    n = text.count(old)\n    if n != 1:\n        print(f\"{name}: ANCHOR COUNT {n} != 1, not run\")\n        continue\n    run_py.write_text(text.replace(old, new))\n    try:\n        rc, summary, fails = run_tests()\n    finally:\n        run_py.write_bytes(pristine)\n    verdict = \"KILLED\" if rc != 0 else \"SURVIVED\"\n    print(f\"{name}: {verdict} | rc={rc} | {summary}\")\n    for f in fails:\n        print(f\"    failed: {f}\")\nrestored = run_py.read_bytes() == pristine\nprint(f\"restored_pristine={restored}\")\nEOF\necho written; ls -la artifacts/review-evidence/T-101-staff-engineer/",
 "description": "Write mutation driver script into review evidence folder"
}
````

### User / tool · 2026-11-02T05:29:57.770Z

**tool result**
````
written
total 8
drwxr-xr-x@   3 arsis  staff     96 Nov  1 23:29 .
drwxr-xr-x@ 914 arsis  staff  29248 Nov  1 23:29 ..
-rw-r--r--@   1 arsis  staff   3367 Nov  1 23:29 mutate_guard.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:30:00.874Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd /Users/arsis/zlayt-pm-project && /Users/arsis/zlayt-pm-project/.venv/bin/python -I artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py \"$S/t101/clone\" /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-101-staff-engineer 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-101-staff-engineer/mutation-log.txt; cd \"$S/t101/clone\" && git status --porcelain --untracked-files=no | wc -l",
 "description": "Run T-101 guard mutants in scratch clone and log results",
 "timeout": 900000
}
````

### User / tool · 2026-11-02T05:31:19.391Z

**tool result**
````
BASELINE rc=0 | 124 passed, 1732 deselected in 8.02s
M1 plain run writes the committed calibration.json: KILLED | rc=1 | 3 failed, 121 passed, 1732 deselected in 8.28s
    failed: tests/unit/test_eval_runner.py::test_full_report_carries_calibration_and_write_report_emits_calibration_json
    failed: tests/unit/test_eval_runner.py::test_plain_run_leaves_committed_calibration_json_untouched
    failed: tests/unit/test_eval_runner.py::test_plain_run_with_dirty_tree_still_never_writes_calibration_json
M2 pre-run refusal removed (pipeline runs before the guard): KILLED | rc=1 | 2 failed, 122 passed, 1732 deselected in 9.28s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src0]
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src1]
M3 post-run header recheck removed: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.27s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
M4 refusal rule ignores a dirty tree: KILLED | rc=1 | 4 failed, 120 passed, 1732 deselected in 8.23s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head[src0]
    failed: tests/unit/test_eval_runner.py::test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M5 dirty check counts untracked files: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.51s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M6 --write-calibration flag not passed to write_report: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.24s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header
M7 header source_tree_clean hard-coded True: KILLED | rc=1 | 1 failed, 123 passed, 1732 deselected in 8.36s
    failed: tests/unit/test_eval_runner.py::test_write_calibration_rechecks_the_header_after_the_run
M8 no-git clause dropped from refusal (message becomes 'uncommitted changes'): SURVIVED | rc=0 | 124 passed, 1732 deselected in 8.44s
restored_pristine=True
       0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:31:27.633Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cd \"$S/t101/clone\" && shasum -a 256 evals/reports/calibration.json && env -u LLM_BACKEND -u ENABLE_LIVE /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration --controls > \"$S/t101/controls.log\" 2>&1; echo \"controls_wc_rc=$?\"; tail -2 \"$S/t101/controls.log\" | cut -c1-240; shasum -a 256 evals/reports/calibration.json; git status --porcelain --untracked-files=no; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit -k \"test_committed_calibration_header_names_backend_and_a_clean_source_commit\" 2>&1 | grep -E \"^E  |passed|failed\" | head -6; shasum -a 256 evals/reports/calibration.json",
 "description": "Probe --write-calibration with --controls; capture project header test failure",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:31:30.558Z

**tool result**
````
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
controls_wc_rc=1
llm call failed call_id=c72dd2001004b step=j4 attempt=1 prompt_hash=3046362cb963a786c075c4b947c12a6b7d4e224a9b268bfb2fe4d3f49a1b1a97
controls_ok=False backend=fixture report=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076
49d383b58340ca186e5ffceac3539e6ea5f94e582cee767d6c8f28c7ea1fd66c  evals/reports/calibration.json
E       AssertionError: assert ('claude-cli' == 'fixture'
E         
E         - fixture
E         + claude-cli)
1 failed, 2003 deselected in 1.74s
3815c6ce652831ac5296b043e538144981edb14018bb9ec9e0821a3415cd70d0  evals/reports/calibration.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:31:38.804Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-101-staff-engineer && cat > untracked-provenance-probe.sh <<'EOF'\n#!/usr/bin/env bash\n# T-101 provenance probe (staff-engineer-reviewer). Usage: bash untracked-provenance-probe.sh <clone_at_4c5f9bf> <venv_python>\n# Adds one UNTRACKED golden case (a copy of case_01) to a clean clone of 4c5f9bf, runs --write-calibration, and prints the header.\nset -u\nCLONE=\"$1\"; PY=\"$2\"\ncd \"$CLONE\" || exit 1\ngit checkout -q -- evals/reports/calibration.json evals/reports/latest.json\ncp evals/golden/case_01_date_formats.txt evals/golden/case_zz_untracked.txt\ncp evals/golden/case_01_date_formats.expected.json evals/golden/case_zz_untracked.expected.json\necho \"tracked dirty lines: $(git status --porcelain --untracked-files=no | wc -l)\"\necho \"untracked: $(git ls-files --others --exclude-standard | tr '\\n' ' ')\"\nenv -u LLM_BACKEND -u ENABLE_LIVE \"$PY\" -m evals.run --write-calibration > /dev/null 2>&1\necho \"write_calibration_rc=$? (1 = ship bar not met, write still happens)\"\n\"$PY\" -I -c \"import json; c=json.load(open('evals/reports/calibration.json')); print({k: c[k] for k in ('source_commit','source_tree_clean','source_tree','case_count')}); print('verified', c['by_state']['verified']['matched'], '/', c['by_state']['verified']['total'], ' case_zz in cases:', 'case_zz_untracked' in c['cases'])\"\necho \"case_zz files in source_tree 4b4960da: $(git ls-tree -r --name-only 4b4960da | grep -c case_zz)\"\ngit checkout -q -- evals/reports/calibration.json evals/reports/latest.json\nrm -f evals/golden/case_zz_untracked.txt evals/golden/case_zz_untracked.expected.json\necho \"restored: tracked dirty lines $(git status --porcelain --untracked-files=no | wc -l)\"\nEOF\nS=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; bash /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh \"$S/t101/clone\" /Users/arsis/zlayt-pm-project/.venv/bin/python 2>&1 | tee /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.log",
 "description": "Save and run untracked-golden-case provenance probe in scratch clone",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T05:31:40.365Z

**tool result**
````
tracked dirty lines:        0
untracked: evals/golden/case_zz_untracked.expected.json evals/golden/case_zz_untracked.txt evals/reports/20261102T052654Z.md evals/reports/20261102T052705Z.md evals/reports/20261102T052731Z.md evals/reports/20261102T052741Z.md evals/reports/controls-20261102T053127Z.json evals/reports/controls-20261102T053127Z.md evals/reports/runs/20261102T052705Z/calibration.json 
write_calibration_rc=1 (1 = ship bar not met, write still happens)
{'source_commit': '4c5f9bf909253bfffa55cb41b1350c412c56e6da', 'source_tree_clean': True, 'source_tree': '4b4960da2d9e52141982b125dc986f0b22344360', 'case_count': 11}
verified 91 / 92  case_zz in cases: True
case_zz files in source_tree 4b4960da: 0
restored: tracked dirty lines        0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:31:45.998Z

**tool call — Bash**
````
{
 "command": "git show HEAD:evals/run.py | grep -n 'def git_source\\|\"--untracked-files=no\"\\|def write_calibration_refusal\\|if not src\\[\"clean\"\\]\\|if src.get(\"commit\") is None or\\|def write_report\\|if write_calibration:\\|scratch = outdir\\|ts = r\\[\"generated_at\"\\]\\|source = git_source()\\|\"generated_at\": dt\\|run_cases(pipeline\\|if a.controls:\\|if a.write_calibration:\\|write_report(report, out\\|ts = dt.datetime.now\\|\"source_tree_clean\": (source\\|run_artifacts\\|except Exception:\\|if a.write_calibration:  ' ; git show HEAD:tests/unit/test_eval_runner.py | grep -n \"def test_write_calibration\\|def test_plain_run\\|def test_committed_calibration\\|def test_git_source\" ",
 "description": "Get exact HEAD line numbers for review citations"
}
````

### User / tool · 2026-11-02T05:31:46.120Z

**tool result**
````
71:def git_source(root=ROOT):
77:        dirty = subprocess.run(["git", "-C", str(root), "status", "--porcelain", "--untracked-files=no"], capture_output=True, text=True, timeout=20, check=True).stdout.strip()
80:    except Exception:
349:            "source_commit": (source or {}).get("commit"), "source_tree_clean": (source or {}).get("clean"), "source_tree": (source or {}).get("tree"), "hashes": hashes_ or {},
465:def run_cases(pipeline, backend, cases=None, runs_dir=None):
889:    results, outs = run_cases(pipeline, backend, cases, runs_dir)
916:    source = git_source()
917:    report = {"schema": "evals.run/1", "generated_at": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
923:        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
1000:          *( [f"- per-run artifacts: `{r['run_artifacts']}`"] if r.get("run_artifacts") else [] ),
1006:def write_calibration_refusal(src):
1009:    if src.get("commit") is None or src.get("clean") is None:
1011:    if not src["clean"]:
1016:def write_report(r, outdir=REPORTS, write_calibration=False):
1021:    ts = r["generated_at"].replace(":", "").replace("-", "")
1026:        if write_calibration:
1029:            scratch = outdir / "runs" / ts
1159:    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
1164:    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
1165:    if a.controls:
1170:    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
1176:    path = write_report(report, out, write_calibration=a.write_calibration)
626:def test_plain_run_leaves_committed_calibration_json_untouched(monkeypatch, tmp_path, good):
640:def test_plain_run_with_dirty_tree_still_never_writes_calibration_json(monkeypatch, tmp_path, good):
649:def test_write_calibration_rechecks_the_header_after_the_run(monkeypatch, tmp_path, good):
669:def test_write_calibration_refuses_before_running_when_tree_is_not_clean_at_head(monkeypatch, tmp_path, src):
682:def test_write_calibration_refusal_rule_is_clean_tracked_tree_at_a_commit():
688:def test_write_calibration_follows_real_git_cleanliness_and_records_the_t090_header(monkeypatch, tmp_path, good):
750:def test_committed_calibration_header_names_backend_and_a_clean_source_commit():
756:def test_committed_calibration_source_commit_exists_and_is_an_ancestor_of_head():
775:def test_committed_calibration_regenerates_exactly_from_its_source_commit(tmp_path):
800:def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
817:def test_git_source_reports_commit_and_dirtiness(tmp_path):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:32:52.785Z

**tool call — Bash**
````
{
 "command": "git show 4c5f9bf | grep -n '^+' | grep -E 'except|float\\(|sleep\\(|retry' ; echo \"grep_rc=$? (1 = no added except/float/sleep/retry lines)\"; ls -la reviews/T-101-staff-engineer.md 2>&1 | head -1; ls artifacts/review-evidence/T-101-staff-engineer/",
 "description": "Grep T-101 diff for except, float, sleep, retry; confirm review file absent"
}
````

### User / tool · 2026-11-02T05:32:52.901Z

**tool result**
````
grep_rc=1 (1 = no added except/float/sleep/retry lines)
ls: reviews/T-101-staff-engineer.md: No such file or directory
mutate_guard.py
mutation-log.txt
run.py.pristine
untracked-provenance-probe.log
untracked-provenance-probe.sh
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:22.097Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-101-staff-engineer.md",
 "content": "# T-101 review: evals.run leaves calibration.json alone; --write-calibration only from a clean HEAD (commit 4c5f9bf)\n\nReviewer: staff-engineer-reviewer (model claude-haiku-5-5). Verdict: **changes** (0 blockers, 2 majors, 5 minors, 1 nit).\n\nThe three confirmations the brief asked for, all run at 4c5f9bf in a clone and in a git archive copy:\n\n1. A plain `python -m evals.run` leaves evals/reports/calibration.json byte-identical. Confirmed (sha256 49d383b5... before and after, archive copy and clone, including a plain run on a dirty tree).\n2. `--write-calibration` refuses on a dirty tracked tree and writes the T-090 header on a clean one. Confirmed (rc 2 with nothing run and nothing written on a dirty tree; on a clean clone the header is source_commit 4c5f9bf, source_tree_clean true, source_tree 4b4960da, equal to `git rev-parse 4c5f9bf^{tree}`). Its refusal is also literal to the AC: untracked files do not block it, which lets the header claim a clean tree for inputs the tree does not contain (F1).\n3. Mutating the guard fails tests. Confirmed for 7 of 8 mutants (M1 to M7 killed; M8, the no-git clause, survives; F6).\n\nDeviation from the brief, stated up front: I used `git clone --no-hardlinks` plus `checkout --detach 4c5f9bf` instead of `git archive` plus `git init`, so that the cited commit b85fc1b exists for the regeneration test. The archive copy (no .git) was used for the plain-run and no-git checks.\n\nTwo findings were judged against D.2 and not rated blocker, with the reason. F1: the card's AC is met as written and no section 5 red flag is hit, but the header's clean claim is false for untracked golden inputs. F2: the served file in the shared working tree is not HEAD's, but HEAD code cannot produce it, so the commit is not its cause. If F2 is still in place at the M3 gate, it becomes a blocker, because the served file would violate the T-090 AC.\n\nWorking-tree state at review time (not the commit): `git status --porcelain -- evals/reports/calibration.json` gives ` M evals/reports/calibration.json`. The file was rewritten at 2026-11-02T05:27:16Z by a live claude-cli run (header backend claude-cli, source_tree_clean false). In the project tree, `pytest -q tests/unit -k \"calibration or eval_runner\"` gives 2 failed, 122 passed. At 4c5f9bf in the clone it gives 124 passed. Who ran that writer is not determinable from the files; see the orchestrator note in the JSON.\n\n## Findings\n\n- **F1 (major) Untracked inputs are invisible to the clean check, so the header can claim a clean HEAD for numbers HEAD cannot reproduce.** evals/run.py:77 uses `git status --porcelain --untracked-files=no`. Repro: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh and its log. With an untracked evals/golden/case_zz_untracked pair, `--write-calibration` writes source_tree_clean true, source_tree 4b4960da, case_count 11, verified 91/92 (was 83/84), and `git ls-tree -r --name-only 4b4960da | grep -c case_zz` is 0.\n- **F2 (major) Working-tree served calibration.json was overwritten after the commit by a run that HEAD code cannot produce.** Repro: `git status --porcelain -- evals/reports/calibration.json`; header read with python -I (generated_at 05:27:16Z, backend claude-cli, source_tree_clean false); `ls evals/reports/runs` shows 20261102T052638Z. Code path: the write needs --write-calibration past evals/run.py:1159 and 1170 to 1174, which refuse clean=False; plain runs write only runs/<ts>/ (evals/run.py:1026 to 1032).\n- **F3 (minor) --write-calibration with --controls silently writes nothing.** evals/run.py:1165 returns before the write at 1176, with no message.\n- **F4 (minor) Live runs: the calibration scratch copy and the run artifacts land in different directories.** evals/run.py:1164 sets the run ts before the run; :917 sets generated_at after run_cases (:889); :1021 names the scratch dir from generated_at; :923 points run_artifacts at the main ts dir. Observed: runs/20261102T052638Z versus report 20261102T052716Z.md, 38 s apart. Reasoned from code and observed dir names; no live backend was run.\n- **F5 (minor) Refusal names no dirty file, and the normal sequence trips it.** Clone: after a successful --write-calibration, `git status --porcelain --untracked-files=no` lists M evals/reports/calibration.json and M evals/reports/latest.json, so the next --write-calibration returns rc 2 with a generic message (evals/run.py:1011 to 1012).\n- **F6 (minor) Test gap: the no-git refusal reason is not asserted.** tests/unit/test_eval_runner.py:682 to 685 asserts only `is not None`. Mutant M8 (drop `or src.get(\"clean\") is None` at evals/run.py:1009) survives; with it gone a no-git tree is refused with the wrong reason \"uncommitted changes\" (`not None` is True at :1011).\n- **F7 (nit) Broad except in git_source.** evals/run.py:80 `except Exception:` turns a missing git binary, a timeout and a corrupt repo into the same \"no git repository\" state. Still fail-closed, so not a blocker.\n\n## What is right\n\n- Plain runs never touch the committed file: M1 is killed by three tests, and the archive and clone sha checks held.\n- The pre-run refusal happens before the pipeline runs: M2 is killed by both parametrized cases.\n- The post-run header recheck covers a tree dirtied during a run: M3 and M7 are killed by test_write_calibration_rechecks_the_header_after_the_run.\n\n## Exercised (commands and results)\n\n- `git show --stat 4c5f9bf`; `git show 4c5f9bf -- evals/run.py tests/unit/test_eval_runner.py`; read evals/run.py (HEAD lines 71 to 80, 318 to 352, 887 to 930, 1006 to 1184) and the T-101 test hunks; `python3 tools/board.py show T-101`; `git show 4c5f9bf | grep '^+' | grep -E 'except|float\\(|sleep\\(|retry'` returned no lines.\n- Archive copy: `git archive 4c5f9bf | tar -x -C <scratchpad>/t101/archive`; import check printed the archive path. Plain `python -m evals.run` with LLM_BACKEND, ENABLE_LIVE, LLM_FIXTURE_DIR and FIXTURE_SET unset: rc 1 (fixture ship bar not met, expected), calibration.json sha256 49d383b5... before and after, scratch copy runs/20261102T052641Z/calibration.json created. `--write-calibration` on the git-less archive: rc 2, \"refused, nothing was run or written: no git repository...\", output dir not created.\n- Clone: `git clone --no-hardlinks /Users/arsis/zlayt-pm-project <scratch>/t101/clone` then `git checkout --detach 4c5f9bf`; HEAD 4c5f9bf909253bfffa55cb41b1350c412c56e6da, `git rev-parse HEAD^{tree}` 4b4960da2d9e52141982b125dc986f0b22344360, tracked dirty 0. `--write-calibration` on the clean clone: header as above; non-git fields identical to the b85fc1b file (python -I comparison).\n- Dirty probe: appended a line to docs/RUNBOOK.md: rc 2 \"the tracked tree has uncommitted changes\", run-dir count unchanged, calibration sha unchanged; restored.\n- Untracked probe: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh, log beside it.\n- `--write-calibration --controls` on the clean clone: no calibration write, sha unchanged, controls output only.\n- `.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\"` at 4c5f9bf (clone): 124 passed, 0 skipped, rc 0; sha unchanged.\n- Same command in the project working tree: 2 failed, 122 passed (test_committed_calibration_header_names_backend_and_a_clean_source_commit: `assert ('claude-cli' == 'fixture')`; test_committed_calibration_regenerates_exactly_from_its_source_commit: verified total 85 against 84). Project calibration.json sha256 3815c6ce... before and after the run.\n- Mutation: artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py, log mutation-log.txt. Baseline 124 passed; M1 to M7 KILLED; M8 SURVIVED; restored_pristine=True.\n- Read-only project checks: `git status`, `shasum -a 256`, `stat`, `ps` (no evals.run process running), grep of board/activity.jsonl for 2026-11-02T05:2x events.\n- Not run: any live backend, any network call.\n\n```json\n{\"card\": \"T-101\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 4c5f9bf (evals/run.py, tests/unit/test_eval_runner.py) at HEAD 4c5f9bf; CLI only, no app URL; sample case evals/golden/sample.txt via the fixture backend; shared project working tree also observed (F2)\",\n \"exercised\": [\"git show --stat and git show of 4c5f9bf (evals/run.py, test_eval_runner.py); board show T-101\",\n  \"read evals/run.py HEAD lines 71-80, 318-352, 887-930, 1006-1184 and the T-101 test hunks; grep of the diff for except, float(, sleep(, retry: no added lines\",\n  \"archive copy of 4c5f9bf (no .git): plain evals.run rc 1 (fixture ship bar), calibration.json sha256 unchanged, scratch runs/<ts>/calibration.json written; --write-calibration rc 2 with 'no git repository' reason and nothing written\",\n  \"clone at 4c5f9bf (tree 4b4960da): --write-calibration on clean tree writes header source_commit 4c5f9bf, source_tree_clean true, source_tree 4b4960da, non-git fields equal to b85fc1b file\",\n  \"clone dirty probe (docs/RUNBOOK.md edit): --write-calibration rc 2, nothing run or written; plain run leaves calibration sha unchanged\",\n  \"untracked golden-case probe (artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh + .log): header clean true, counts 91/92 with case not in source_tree\",\n  \"--write-calibration --controls on clean clone: no calibration write\",\n  \"pytest -q tests/unit -k 'calibration or eval_runner' at 4c5f9bf in clone: 124 passed, 0 skipped; in project working tree: 2 failed, 122 passed\",\n  \"mutation driver artifacts/review-evidence/T-101-staff-engineer/mutate_guard.py, log mutation-log.txt: baseline 124 passed; M1-M7 killed; M8 survived; run.py restored byte-identical\",\n  \"read-only project checks: git status, shasum, stat, ps, board/activity.jsonl grep for 05:2x events; no live backend, no network\"],\n \"verdict\": \"changes\",\n \"scores\": {\"plain_run_isolation\": 5, \"write_guard_refusal\": 4, \"provenance_header\": 2, \"test_strength\": 4, \"cli_surface\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Untracked inputs are invisible to the clean check, so the header can claim a clean HEAD for numbers HEAD cannot reproduce\",\n   \"evidence\": \"evals/run.py:77 `git status --porcelain --untracked-files=no`; repro artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh and .log: with untracked evals/golden/case_zz_untracked.{txt,expected.json} in a clean clone of 4c5f9bf, --write-calibration writes source_tree_clean true, source_tree 4b4960da..., case_count 11, verified 91/92 (clean run 83/84), and `git ls-tree -r --name-only 4b4960da | grep -c case_zz` prints 0\",\n   \"why_it_matters\": \"T-090 requires the served calibration.json to be regenerable from the header's clean source. Here the header names a clean HEAD tree for counts produced from a golden case that tree does not contain. The AC is met as written (dirty tracked tree refused), so this is not a literal AC failure; it is a false provenance claim in the file the app serves. The project has a recorded incident of untracked files breaking HEAD (memory/LESSONS.md:26). Rated major, not blocker: no section 5 red flag, and the trigger needs a human to add untracked golden inputs.\",\n   \"fix\": \"Treat any untracked path outside evals/reports/ as dirty (for example `git ls-files --others --exclude-standard -- app tests evals/golden spec docs`) and refuse. Exclude evals/reports/ because plain runs write untracked reports there (observed). Alternatively record an untracked_inputs list in the header and refuse when it is non-empty. The existing test 'untracked files do not count' (repo-root untracked.txt) must change with the rule.\",\n   \"acceptance_test\": \"Probe script exits 2 with nothing written when an untracked file exists under evals/golden or app; still writes when only evals/reports/* is untracked; the untracked-file test in test_write_calibration_follows_real_git_cleanliness is updated to these cases.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Working-tree served calibration.json was overwritten after the commit by a run that HEAD code cannot produce\",\n   \"evidence\": \"`git status --porcelain -- evals/reports/calibration.json` -> ' M evals/reports/calibration.json'; python -I read of the file: generated_at 2026-11-02T05:27:16Z, backend claude-cli, source_tree_clean false; evals/reports/latest.json generated_at 05:27:16Z backend claude-cli; evals/reports/runs/20261102T052638Z exists. Project pytest -k calibration: 'assert (claude-cli == fixture)' in test_committed_calibration_header_names_backend_and_a_clean_source_commit; clone at 4c5f9bf: 124 passed. HEAD write path is guarded at evals/run.py:1159 and 1170-1174 (refuse clean=False); plain runs write only runs/<ts>/ (evals/run.py:1026-1032).\",\n   \"why_it_matters\": \"This is the incident T-101 exists to stop: a dirty live run replaced the served file with a claude-cli header that is not reproducible from a clean commit. Two T-090/T-101 tests are red in the tree the team works from. The commit is not the cause (HEAD code refuses this write), so the writer ran other code or bypassed the guard; the files do not say which. Rated major: the commit is correct and the file sits outside it. Upgrade to blocker if it is still in place at the M3 gate, because the served file would then violate the T-090 AC.\",\n   \"fix\": \"Confirm no evals.run process is running (ps showed none at review time), restore the HEAD copy with git checkout -- evals/reports/calibration.json, and identify the writer from runs/20261102T052638Z and its log. Add a check that refuses to serve a calibration.json whose header backend or source_tree_clean is not the pinned one.\",\n   \"acceptance_test\": \"`git status --porcelain -- evals/reports/calibration.json` is empty; sha256 equals HEAD's 49d383b5...; `.venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner'` run in the project working tree passes with 0 failed.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"--write-calibration combined with --controls silently writes nothing\",\n   \"evidence\": \"evals/run.py:1159-1163 guard, then :1165 `if a.controls: return run_controls_only(...)` precedes the write at :1176; clone repro: `evals.run --write-calibration --controls` on a clean clone exits with the controls result and prints no calibration message; calibration.json sha unchanged\",\n   \"why_it_matters\": \"A user who asks for a calibration write gets an exit code and no file, with no message that the flag was ignored.\",\n   \"fix\": \"Refuse the combination before any run with exit 2 and a message, or write the calibration in controls mode.\",\n   \"acceptance_test\": \"`evals.run --write-calibration --controls` exits 2, runs nothing, and writes nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Live runs: calibration scratch copy and run artifacts land in different run directories\",\n   \"evidence\": \"evals/run.py:1164 sets the main ts before the run and passes it as runs_dir (:1167 onward); :917 sets generated_at after run_cases (:889); :1021 names the scratch dir from generated_at; :923 points run_artifacts at the main ts dir. Observed: runs/20261102T052638Z (live artifacts) against report 20261102T052716Z.md, 38 s apart.\",\n   \"why_it_matters\": \"A reader following run_artifacts in the report will not find the calibration copy written for the same live run.\",\n   \"fix\": \"Compute one ts in main and pass it to build_report and write_report, or write the calibration scratch copy into runs_dir.\",\n   \"acceptance_test\": \"A live-backend test with a faked provider asserts that the report's run_artifacts directory contains calibration.json.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Refusal names no dirty file, and the normal sequence trips it\",\n   \"evidence\": \"clone: after a successful --write-calibration, `git status --porcelain --untracked-files=no` lists ' M evals/reports/calibration.json' and ' M evals/reports/latest.json'; the next --write-calibration returns rc 2 with 'the tracked tree has uncommitted changes (git status --porcelain is not empty for tracked files)' (evals/run.py:1011-1012). Every run also rewrites tracked latest.json (write_report).\",\n   \"why_it_matters\": \"The operator cannot tell which file blocked the write, and a plain run followed by --write-calibration is refused by default.\",\n   \"fix\": \"List the dirty paths in the refusal text; decide explicitly whether the run-rewritten latest.json should count toward dirtiness.\",\n   \"acceptance_test\": \"The refusal text contains each dirty tracked path; a test asserts a path name appears in the message.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Test gap: the no-git refusal reason is not asserted\",\n   \"evidence\": \"tests/unit/test_eval_runner.py:682-685 asserts only `is not None` for the no-git case. Mutant M8 (drop `or src.get(\\\"clean\\\") is None` at evals/run.py:1009) SURVIVED in artifacts/review-evidence/T-101-staff-engineer/mutation-log.txt; without the clause a no-git tree is refused with the reason 'uncommitted changes' because `not None` is True at evals/run.py:1011.\",\n   \"why_it_matters\": \"The wrong reason is shown to the operator and nothing catches it.\",\n   \"fix\": \"Assert the reason text: 'no git repository' in the no-git case.\",\n   \"acceptance_test\": \"Mutant M8 is killed by the T-101 selection.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Broad except in git_source collapses every failure into the no-git state\",\n   \"evidence\": \"evals/run.py:80 `except Exception:` returns {'commit': None, ...}; a missing git binary, a timeout and a corrupt repo look the same.\",\n   \"why_it_matters\": \"The refusal stays fail-closed, so this is not a blocker, but the message can point at the wrong cause.\",\n   \"fix\": \"Catch OSError and subprocess.SubprocessError only.\",\n   \"acceptance_test\": \"A test with git replaced by a missing binary reports the OS error reason.\"}\n ],\n \"whats_right\": [\"Plain runs never write the committed calibration.json: sha256 unchanged in the archive copy and the dirty clone; mutant M1 is killed by three tests\",\n  \"The pre-run refusal happens before the pipeline runs: mutant M2 is killed by both parametrized cases, and the dirty probe ran nothing\",\n  \"The post-run header recheck closes the dirtied-during-run gap: mutants M3 and M7 are killed by test_write_calibration_rechecks_the_header_after_the_run\"],\n \"questions_for_chris\": [\"Should --write-calibration be limited to the recorded fixture backend? Today any backend that passes the tree check can overwrite the served calibration.json (evals/run.py:1176); the T-101 handoff notes the tests pin fixture but the code does not.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T05:33:22.242Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-101-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:25.273Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate reviews/T-101-staff-engineer.md; echo \"validate_rc=$?\"; grep -c '^```' reviews/T-101-staff-engineer.md",
 "description": "Validate the T-101 review file with the board validator"
}
````

### User / tool · 2026-11-02T05:33:25.411Z

**tool result**
````
ok (1 file(s))
validate_rc=0
2
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:33.488Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat > project_t101_calibration_guard_patterns.md <<'EOF'\n---\nname: t101-calibration-guard-patterns\ndescription: T-101 r1 (commit 4c5f9bf, evals.run plain vs --write-calibration guard): untracked golden input under a clean header, live run overwrote the served file in the shared tree, --controls silent no-op, refusal reason untested\nmetadata:\n  type: project\n---\n\nT-101 r1 (commit 4c5f9bf; review reviews/T-101-staff-engineer.md): changes, 0 blockers, 2 majors, 5 minors, 1 nit. Mutants M1-M7 killed, M8 (no-git clause) survived.\n\n- **Clean check ignores untracked inputs, so the header lies.** `git status --porcelain --untracked-files=no` lets an untracked golden case change the counts while the header says source_tree_clean true at the HEAD tree (which does not contain the case). Repro script: artifacts/review-evidence/T-101-staff-engineer/untracked-provenance-probe.sh. Plain runs also leave untracked reports under evals/reports, so the fix must exclude that dir, not all untracked files.\n- **Shared tree is not HEAD.** After 4c5f9bf, the project working-tree evals/reports/calibration.json was rewritten by a claude-cli run (header backend claude-cli, clean false). Project pytest then showed 2 failed; the same selection at HEAD in a clone showed 124 passed. HEAD code cannot write a clean=false header (both guards refuse), so the writer ran other code. Check `git status -- <served file>` and the header before citing project-tree test results.\n- **Flag combinations.** `--write-calibration --controls` returns before the write and says nothing.\n- **Scratch dir mismatch.** The calibration scratch dir is named from generated_at, the run artifacts from the main ts; for live runs they differ by the run length (observed 38 s).\n- **Refusal text.** It does not name the dirty files; a plain run rewrites tracked latest.json, so a write right after a run is refused.\n- **Survivor pattern.** Dropping the `or ... clean is None` clause keeps rc 2 (the `not None` branch refuses too) but gives the wrong reason; the test only asserts `is not None`. Assert the reason text.\n\n**Why:** the card's AC was met literally, so the findings are about what the header claims and what the served file contains, not the AC wording.\n**How to apply:** for any \"write only from clean\" guard, (1) add an untracked input and check the header, (2) check the served file in the working tree against HEAD before trusting project-tree test output, (3) mutate the refusal and assert its reason text.\n\nRelated: [[project_t090_calibration_review_patterns]] (provenance header history), [[project_eval_runner_review_patterns]] (scratch-copy method, git archive pinning).\nEOF\ncd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && grep -n \"t101\" MEMORY.md; echo \"---\"; tail -c 200 MEMORY.md | od -c | tail -2 >/dev/null; echo ok",
 "description": "Save T-101 recurring patterns to reviewer memory"
}
````

### User / tool · 2026-11-02T05:33:33.590Z

**tool result**
````
---
ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:35.962Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted, D-047 409 closed by T-100; T-099 3ecb8b1 changes: state-sum rule untested, route weaker than evals check",
 "new_string": "- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted, D-047 409 closed by T-100; T-099 3ecb8b1 changes: state-sum rule untested, route weaker than evals check\n- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — T-101 4c5f9bf changes: untracked input under clean header, shared-tree served file not HEAD, --controls no-op, refusal reason untested"
}
````

### User / tool · 2026-11-02T05:33:35.964Z

**tool result (error)**
````
<tool_use_error>File has been modified since read, either by the user or by a linter. Read it again before attempting to write it.</tool_use_error>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:37.621Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && printf '%s\\n' '- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — T-101 4c5f9bf changes: untracked input under clean header, shared-tree served file not HEAD, --controls no-op, refusal reason untested' >> MEMORY.md && tail -3 MEMORY.md | cut -c1-160",
 "description": "Append T-101 pointer line to reviewer memory index"
}
````

### User / tool · 2026-11-02T05:33:37.706Z

**tool result**
````
- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — r1 24c18a7 fail: one-way qualifier check, gate reads stored reasons only, narrow negation lis
- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — T-098 e511778 fail: AI-draft invented number accepted; T-099 3ecb8b1 changes (state-sum untes
- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — T-101 4c5f9bf changes: untracked input under clean header, shared-tree serv
````

### Assistant · claude-haiku-5-5 · 2026-11-02T05:33:39.944Z

T-101 verdict is changes (0 blockers, 2 majors, 5 minors, 1 nit) in `/Users/arsis/zlayt-pm-project/reviews/T-101-staff-engineer.md`: the plain run and the dirty-tree refusal hold at 4c5f9bf (124 passed), but the clean check ignores untracked inputs, and the shared-tree calibration.json was overwritten by a claude-cli run at 05:27:16Z.
