# Subagent: T-070 r2 check (haiku staff) (T-070 r2 check (haiku staff))

Source: `agent-a173adbd7f1ed8249.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:03:28.001Z

Round-2 check of board card T-070 in /Users/arsis/zlayt-pm-project (commit 20471a7, evals/run.py). Using reviews/T-070-staff-engineer.md, confirm:
- " claude-cli " and "Claude-CLI" without ENABLE_LIVE exit 2 and never run on fixtures;
- unknown names exit 2;
- the tests fail when the normalization is mutated out.

Run `.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py`. Write reviews/T-070-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:31.023Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T03:03:31.031Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:31.203Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-070-staff-engineer.md"
}
````

### User / tool · 2026-11-02T03:03:31.210Z

**tool result**
````
1	# T-070 review: staff-engineer-reviewer (commit 815d616)
2	
3	**Verdict: changes.** One major, one minor, no blockers. Pinned to 815d616 with `git archive` (HEAD moved to b9d3ead during the review; the commit touches only `evals/run.py`, `tests/unit/test_eval_runner.py` and one report file).
4	
5	**AC check: met as written.** The AC asks that `LLM_BACKEND=claude-cli ENABLE_LIVE=1 ... --runs 3` reports `backend=claude-cli`, measures determinism and unsupported counts, and notes the report path. The committed report `evals/reports/20261102T025219Z.md` does that. Its determinism is 0.0 against a bar of 1.0. The AC does not require the bar, so I did not count it as a finding. T-075 tracks it.
6	
7	**Refusal: exact string only.** With `ENABLE_LIVE` unset, `LLM_BACKEND=claude-cli` exits 2 as intended. A padded or mixed-case value (`" claude-cli "`, `Claude-CLI`) still runs the fixture pipeline and writes a report labelled `backend=fixture`. The label is honest, so nothing is misreported, but the refusal does not cover the case its title describes.
8	
9	Probes: the guard test fails when the check is disabled (mutant), so the test is not vacuous.
10	
11	```json
12	{"card": "T-070", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
13	 "scope": "commit 815d616 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/20261102T025219Z.md); pinned via git archive; HEAD during review b9d3ead; no app URL; eval runner only (no product code in scope)",
14	 "exercised": [
15	   "git show 815d616 --stat and git show 815d616 -- evals/run.py tests/unit/test_eval_runner.py (full diff read)",
16	   "git archive 815d616 | tar -x -C <scratchpad>/t070",
17	   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit/test_eval_runner.py -q -k live_backend at 815d616: 2 passed, 36 deselected",
18	   "PYTHONPATH=. .venv/bin/python -m pytest tests/unit -q at 815d616: 2 failed (tests/unit/test_e2e_contract.py::test_every_test_id_is_declared, ::test_data_attributes_declared), 943 passed; both files are untouched by 815d616",
19	   "Mutant in scratch copy: evals/run.py:680 condition replaced with `if False:`; pytest -k live_backend -> 1 failed (test_live_backend_without_enable_live_is_refused), 1 passed; scratch file restored and cmp-identical to git show 815d616:evals/run.py",
20	   "Control: LLM_BACKEND=claude-cli .venv/bin/python -m evals.run --out <scratch>/probeC (ENABLE_LIVE unset) -> rc=2 with message 'requested but ENABLE_LIVE=1 is not set'",
21	   "Probe A: env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' .venv/bin/python -m evals.run --out <scratch>/probeA -> rc=1, stdout 'ship_bar_met=False backend=fixture report=.../probeA/20261102T025742Z.md'; report backend=fixture, backend_requested=' claude-cli '",
22	   "Probe B: env -u ENABLE_LIVE LLM_BACKEND='Claude-CLI' ... --out <scratch>/probeB -> rc=1, backend=fixture (same bypass)",
23	   "Read evals/run.py:32, 567, 679-680 and app/llm/provider.py:23-30, 27 at 815d616 (LIVE_BACKENDS exact match; report label from pipeline-served backend; provider strips LLM_BACKEND)",
24	   "git show 815d616:evals/reports/20261102T025219Z.md cmp-identical to working tree; header '**ship_bar_met: False**  backend `claude-cli`'; metrics table read (determinism_3run 0.0 vs 1.0, unsupported_count_3run 0, blocker 4_no_invented_facts)",
25	   ".venv/bin/python tools/board.py show T-070 and show T-075 (read-only)"
26	 ],
27	 "verdict": "changes",
28	 "scores": {"ac_met_as_written": 5, "refusal_covers_requested_forms": 3, "test_non_vacuous": 5, "report_label_honesty": 5, "no_silent_fallback": 4, "scope_discipline": 5},
29	 "findings": [
30	   {"severity": "major",
31	    "title": "Guard matches the raw LLM_BACKEND string, so padded or mixed-case live names still run as fixture",
32	    "evidence": "evals/run.py:679-680 at 815d616: `backend = a.backend or os.environ.get(\"LLM_BACKEND\", \"fixture\")` then `if pipeline is None and backend in LIVE_BACKENDS and os.environ.get(\"ENABLE_LIVE\") != \"1\":`; LIVE_BACKENDS (evals/run.py:32) is an exact tuple match. app/llm/provider.py:27 strips the same variable, so the provider and the guard disagree. Repro: git archive 815d616 | tar -x -C <dir>; cd <dir>; env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out <dir>/out -> rc=1, 'ship_bar_met=False backend=fixture'; report JSON backend='fixture', backend_requested=' claude-cli '. Same with LLM_BACKEND=Claude-CLI.",
33	    "why_it_matters": "T-070 exists because a requested live run silently ran as fixture. The exact-string guard fixes only the spelling the test uses. A trailing space from a quoted or hand-edited .env, or a capitalised name, still runs the fixture pipeline and writes an eval report that looks like a finished run. The report label is honest (backend=fixture) and the ship bar blocks it, so this is not a false label and not a silent pass. It is a major because the refusal does not hold for the request the card names.",
34	    "fix": "Normalise and validate the name before the check: backend = (a.backend or os.environ.get(\"LLM_BACKEND\", \"fixture\")).strip(); refuse (rc 2, same message, no report written) any value not in (\"fixture\",) + LIVE_BACKENDS, since an unknown name is an error, not a fixture run. Keep the ENABLE_LIVE check for live names. Optionally also refuse after the run if the requested backend is live and report['backend'] == 'fixture'.",
35	    "acceptance_test": "Parametrised unit test in tests/unit/test_eval_runner.py with ENABLE_LIVE unset and LLM_BACKEND in [' claude-cli ', 'Claude-CLI', 'claude-cli\\n', 'anthropic-api ']: main([...]) == 2, stderr contains 'ENABLE_LIVE=1' (or 'unknown backend'), and no *.json written to tmp_path. Positive control: LLM_BACKEND='fixture' returns 0 and the report says backend fixture."},
36	   {"severity": "minor",
37	    "title": "No unit assertion that a correctly configured live run reaches the pipeline",
38	    "evidence": "tests/unit/test_eval_runner.py:362-368 (test_live_backend_without_enable_live_is_refused) asserts only rc 2 for the unset case. The 815d616 diff adds no test with ENABLE_LIVE=1. The live path is evidenced only by the committed manual report.",
39	    "why_it_matters": "A later edit that refuses a correctly configured live run (for example a wrong comparison) would pass the suite and surface only at the next manual eval.",
40	    "fix": "Add a test with ENABLE_LIVE=1 and LLM_BACKEND=claude-cli, monkeypatching load_pipeline (or passing a fake pipeline is not enough, since the guard skips injected pipelines) to a recorder, and assert the run proceeds past the guard (rc != 2).",
41	    "acceptance_test": "The new test fails when the guard condition is inverted (ENABLE_LIVE != '1' changed to == '1') and passes at HEAD."}
42	 ],
43	 "whats_right": [
44	   "The guard is non-vacuous: with the condition disabled in the pinned copy, test_live_backend_without_enable_live_is_refused fails (1 failed, 1 passed).",
45	   "The report label is what the pipeline served (evals/run.py:567 sample_out.get('backend'), request kept in backend_requested), so the probes show backend=fixture and not a false claude-cli label.",
46	   "The refusal returns 2 before build_report, so a refused request writes no report file (asserted by the test's `not list(tmp_path.glob('*.json'))`)."
47	 ],
48	 "questions_for_chris": []}
49	```
50	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:31.405Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t070_t067_review_patterns.md"
}
````

### User / tool · 2026-11-02T03:03:31.411Z

**tool result**
````
1	---
2	name: t070-t067-review-patterns
3	description: T-070 r1 (815d616 eval guard) and T-067 r2 (f6fa2dd credibility family): exact-match guard vs provider strip, clause-prefix negation drops mixed results, post-term negation gap, persona-mismatch handling
4	metadata:
5	  type: project
6	---
7	
8	Reviewed 2026-11-02. T-070 r1 pinned at 815d616; T-067 r2 pinned at f6fa2dd; HEAD moved to b9d3ead during both.
9	
10	- **Exact-string guard vs a normalising provider.** evals/run.py:679-680 checked the raw LLM_BACKEND against LIVE_BACKENDS (exact tuple); app/llm/provider.py:27 strips the same variable. A padded (" claude-cli ") or mixed-case ("Claude-CLI") value skips the refusal and runs fixture. The report label stayed honest (backend=fixture), so this is a coverage gap, not a false label.
11	  **Why:** the test used the exact string, so it passed while the class of input stayed open.
12	  **How to apply:** for any "refuse X" guard that duplicates parsing done upstream, grep the reader for strip/lower and probe the variants it accepts, not only the literal the test uses.
13	
14	- **Clause-prefix negation drops mixed results.** credibility.py:35-36 takes the first clause and tests only its leading words with `_NEG_RESULT.match`. "Waddell signs negative on the left, positive on the right." is silent, and the reversed order flags. The same facts give different output depending on word order.
15	  **How to apply:** for any negation-by-prefix rule, probe a two-result sentence in both orders and check the positive side survives.
16	
17	- **Negation after the term is not covered.** "Waddell testing was not done." and "Malingering was not suspected." still flag. The r1 negation list covered before-term and result-word forms only.
18	  **How to apply:** probe post-term negation with the verbs a record would use (done, performed, suspected, elicited).
19	
20	- **Severity deviation on residuals.** r1 rated "negated wording raises a flag" a blocker because the template stated the opposite of the record. In r2 the template is neutral, so the post-term residual was rated major, and the deviation was stated in the review. See [[feedback_severity_vs_brief]].
21	
22	- **Persona mismatch.** The orchestrator asked me to write a claims-adjuster-reviewer file. I am staff-engineer-reviewer. I wrote the requested path, set the JSON persona to my own persona, named the gap in the first paragraph, and left the adjuster-lens judgment for a fresh dispatch. Reason: writing as another persona breaks the fresh-context rule.
23	  **How to apply:** if asked for a persona that is not mine, keep the honest persona field, put the gap in the first paragraph and the reply, and do the engineering probes that are in my lens.
24	
25	- **Pass counts depend on the selection.** `pytest tests/unit/test_flags*.py` = 48; adding tests/unit/test_flag_templates.py = 74 (the card's figure). `-k flag` = 122. Check the selection before disputing a card's count.
26	
27	- **Environment gotcha.** macOS has no `timeout(1)`; `timeout 600 pytest ...` fails with "command not found". Use the Bash tool's timeout parameter instead.
28	
29	- **Full-suite baseline at these commits:** 943 passed / 2 failed at 815d616; 947 passed / 2 failed at f6fa2dd. The failures are tests/unit/test_e2e_contract.py::test_every_test_id_is_declared and ::test_data_attributes_declared, untouched by either commit.
30	
31	See also [[project_eval_runner_review_patterns]] (fake hides real shape; scratch-copy mutation method) and [[project_r2_fix_verification_patterns]] (pin the card's fix commit).
32	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:31.900Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git show --stat 20471a7 | head -40 && echo '---' && cat evals/run.py",
 "description": "Show recent commits, commit 20471a7 stats, and evals/run.py"
}
````

### User / tool · 2026-11-02T03:03:32.031Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:34.664Z

**tool call — Bash**
````
{
 "command": "git rev-parse --short HEAD && git show 20471a7 -- evals/run.py && echo '=== TEST DIFF (first 80 lines) ===' && git show 20471a7 -- tests/unit/test_eval_runner.py | head -90",
 "description": "Show HEAD and the 20471a7 diff for run.py and tests"
}
````

### User / tool · 2026-11-02T03:03:34.791Z

**tool result**
````
20471a7
commit 20471a753037e25c4931de9aec68422e939453ff
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 21:03:14 2026 -0600

    fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)
    
    Strip and lower-case the requested backend so ' Claude-CLI ' is guarded like claude-cli; any unknown value exits 2 instead of running fixtures. Adds parametrized tests.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/evals/run.py b/evals/run.py
index eb3b0e2..0b5059f 100644
--- a/evals/run.py
+++ b/evals/run.py
@@ -30,6 +30,7 @@ GOLD = ROOT / "evals" / "golden"
 REPORTS = ROOT / "evals" / "reports"
 REQUIREMENTS = ROOT / "spec" / "REQUIREMENTS.md"
 LIVE_BACKENDS = ("claude-cli", "anthropic-api")
+KNOWN_BACKENDS = ("fixture",) + LIVE_BACKENDS
 NOT_MEASURED = {"value": None, "status": "not_measured"}
 
 THRESHOLDS = {"grounding_rate": 1.0, "entry_recall": 0.95, "amount_recall": 0.95, "flag_precision": 0.9, "flag_recall": 0.9,
@@ -649,6 +650,14 @@ def refuse_curated(env=None):
                               "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")
 
 
+def normalize_backend(raw):
+    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
+    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
+    the caller must exit 2 rather than fall back to fixtures."""
+    name = (raw or "").strip().lower() or "fixture"
+    return name if name in KNOWN_BACKENDS else None
+
+
 def main(argv=None, pipeline=None):
     ap = argparse.ArgumentParser(prog="python -m evals.run")
     ap.add_argument("--check-fresh", action="store_true")
@@ -676,7 +685,13 @@ def main(argv=None, pipeline=None):
     except CuratedFixtures as e:
         print(f"evals.run: {e}", file=sys.stderr)
         return 2
-    backend = a.backend or os.environ.get("LLM_BACKEND", "fixture")
+    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
+    backend = normalize_backend(raw)
+    if backend is None:
+        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
+        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
+              f"Nothing was run.", file=sys.stderr)
+        return 2
     if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
         # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
         # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
=== TEST DIFF (first 80 lines) ===
commit 20471a753037e25c4931de9aec68422e939453ff
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 21:03:14 2026 -0600

    fix(evals): normalise and validate LLM_BACKEND before the live guard (T-070 r2)
    
    Strip and lower-case the requested backend so ' Claude-CLI ' is guarded like claude-cli; any unknown value exits 2 instead of running fixtures. Adds parametrized tests.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/unit/test_eval_runner.py b/tests/unit/test_eval_runner.py
index 735f8cc..1e47cfb 100644
--- a/tests/unit/test_eval_runner.py
+++ b/tests/unit/test_eval_runner.py
@@ -366,3 +366,62 @@ def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, caps
     assert R.main(["--out", str(tmp_path)]) == 2
     assert "ENABLE_LIVE=1" in capsys.readouterr().err
     assert not list(tmp_path.glob("*.json"))
+
+
+@pytest.mark.parametrize("raw", [" claude-cli ", "Claude-CLI", "CLAUDE-CLI\n", "\tanthropic-api  ", "Anthropic-API"])
+def test_padded_or_mixed_case_live_backend_without_enable_live_is_refused(raw, monkeypatch, tmp_path, capsys):
+    """T-070 r2 (staff-engineer major): the guard must see the normalized name, or ' claude-cli ' runs on fixtures and writes backend=fixture."""
+    monkeypatch.setenv("LLM_BACKEND", raw)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    assert R.main(["--out", str(tmp_path)]) == 2
+    assert "ENABLE_LIVE=1" in capsys.readouterr().err
+    assert not list(tmp_path.glob("*.json"))
+
+
+@pytest.mark.parametrize("raw", ["openai", "claude", "claude-cli-x", "anthropic", "fixtures", "lol"])
+def test_unknown_backend_name_exits_2_with_a_clear_message(raw, monkeypatch, tmp_path, capsys):
+    """T-070 r2: a value that is not a known backend is an error, never a silent fixture run."""
+    monkeypatch.setenv("LLM_BACKEND", raw)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    assert R.main(["--out", str(tmp_path)]) == 2
+    err = capsys.readouterr().err
+    assert "unknown LLM_BACKEND" in err and "Nothing was run" in err
+    assert not list(tmp_path.glob("*.json"))
+
+
+@pytest.mark.parametrize("flag", ["openai", " Claude-Cli  ", "Fixture!"])
+def test_backend_flag_is_validated_like_the_env_var(flag, monkeypatch, tmp_path, capsys):
+    monkeypatch.delenv("LLM_BACKEND", raising=False)
+    monkeypatch.delenv("ENABLE_LIVE", raising=False)
+    rc = R.main(["--backend", flag, "--out", str(tmp_path)])
+    assert rc == 2
+    assert not list(tmp_path.glob("*.json"))
+    if flag.strip().lower() == "claude-cli":                # a known backend in odd case is refused by the ENABLE_LIVE guard, not 'unknown'
+        assert "ENABLE_LIVE=1" in capsys.readouterr().err
+    else:
+        assert "unknown LLM_BACKEND" in capsys.readouterr().err
+
+
+@pytest.mark.parametrize("raw,expected", [
+    (None, "fixture"), ("", "fixture"), ("   ", "fixture"), ("fixture", "fixture"), ("FIXTURE ", "fixture"),
+    (" claude-cli ", "claude-cli"), ("Claude-CLI", "claude-cli"), ("\tANTHROPIC-API\n", "anthropic-api"),
+    ("openai", None), ("claude", None), ("claude-cli ok", None),
+])
+def test_normalize_backend_strips_lowercases_and_rejects_unknown(raw, expected):
+    assert R.normalize_backend(raw) == expected
+
+
+def test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name(monkeypatch, tmp_path):
+    """T-070 r2 minor: with ENABLE_LIVE=1 a padded, mixed-case live name passes the guard and the run is built with the normalized backend."""
+    seen = []
+    def fake_build(pipeline, backend, runs=3, **kw):
+        seen.append((backend, runs))
+        return {"ship_bar_met": False, "backend": backend, "blockers": []}
+    monkeypatch.setattr(R, "build_report", fake_build)
+    monkeypatch.setattr(R, "load_pipeline", lambda: object())
+    monkeypatch.setattr(R, "write_report", lambda r, outdir=None: tmp_path / "x.json")
+    monkeypatch.setenv("LLM_BACKEND", " Claude-CLI ")
+    monkeypatch.setenv("ENABLE_LIVE", "1")
+    rc = R.main(["--out", str(tmp_path)])
+    assert rc == 1                                           # ship bar not met by the stub, but the run proceeded past the guard
+    assert seen == [("claude-cli", 3)]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:35.030Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit/test_eval_runner.py 2>&1 | tail -25",
 "description": "Run eval runner unit tests in the working tree"
}
````

### User / tool · 2026-11-02T03:03:37.217Z

**tool result**
````
................................................................         [100%]
64 passed in 1.86s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:43.400Z

**tool call — Bash**
````
{
 "command": "grep -n \"def main\" -A 75 evals/run.py | sed -n '1,95p'; echo '=== load_pipeline / run_case ==='; grep -n \"def load_pipeline\" -A 12 evals/run.py; grep -n \"run_case\\|backend\" evals/run.py | head -60",
 "description": "Read main() guard flow and pipeline backend plumbing in evals/run.py"
}
````

### User / tool · 2026-11-02T03:03:43.505Z

**tool result**
````
661:def main(argv=None, pipeline=None):
662-    ap = argparse.ArgumentParser(prog="python -m evals.run")
663-    ap.add_argument("--check-fresh", action="store_true")
664-    ap.add_argument("--check-spec", action="store_true")
665-    ap.add_argument("--backend", default=None)
666-    ap.add_argument("--runs", type=int, default=3, help="live runs on the sample; anything but 3 leaves determinism/unsupported not_measured")
667-    ap.add_argument("--out", default=str(REPORTS))
668-    a = ap.parse_args(argv)
669-    out = pathlib.Path(a.out)
670-    if a.check_fresh:
671-        return check_fresh(out / "latest.json")
672-    if a.check_spec:
673-        s = check_spec()
674-        latest = out / "latest.json"
675-        data = json.loads(latest.read_text()) if latest.exists() else {"schema": "evals.run/1"}
676-        data.update(s)
677-        if "metrics" in data:                       # a full report: never leave a stale ship_bar_met next to a changed spec result
678-            data["ship_bar_met"], data["bars"], data["blockers"] = evaluate_report(data)
679-        out.mkdir(parents=True, exist_ok=True)
680-        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
681-        print(json.dumps(s))
682-        return 0 if s["spec_matches_golden"] else 1
683-    try:
684-        refuse_curated()
685-    except CuratedFixtures as e:
686-        print(f"evals.run: {e}", file=sys.stderr)
687-        return 2
688-    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
689-    backend = normalize_backend(raw)
690-    if backend is None:
691-        # T-070 r2: an unknown name is an error, not a fixture run (app.llm.provider would silently serve fixtures without ENABLE_LIVE=1).
692-        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
693-              f"Nothing was run.", file=sys.stderr)
694-        return 2
695-    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
696-        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
697-        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
698-        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
699-              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
700-        return 2
701-    report = build_report(pipeline or load_pipeline(), backend, a.runs)
702-    path = write_report(report, out)
703-    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
704-    for b in report["blockers"]:
705-        print("  blocker:", b)
706-    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)
707-
708-
709-if __name__ == "__main__":
710-    sys.exit(main())
=== load_pipeline / run_case ===
631:def load_pipeline():
632-    from app import pipeline
633-    return pipeline
634-
635-
636-class CuratedFixtures(Exception):
637-    pass
638-
639-
640-def refuse_curated(env=None):
641-    """D-029: the ship bar is measured on live runs and recorded fixtures only. Curated (hand-checked) responses reproduce the golden
642-    answers by construction, so scoring them would be circular. Refuse to compute ship-bar metrics when the curated set is selected."""
643-    env = os.environ if env is None else env
4:    python -m evals.run                  full run (backend from LLM_BACKEND, default fixture)
8:Pipeline contract consumed (backend T-037 provides; the runner is unit-tested against a fake):
9:    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
10:        records, entries, undated_entries, amounts, totals, flags, tray, warnings, backend, models{generator,judge}
13:    app.pipeline.judge_summary(summary, excerpt, label, backend) -> "supported" | "partially" | "unsupported" | "unavailable"
14:Metrics that need a live model (determinism_3run, unsupported_count_3run) are `not_measured` on the fixture backend, and
272:    recs = {rn(r.get("id", r.get("seq"))): r for r in out.get("records") or []}   # run_case record keys: id, seq, n, source, date_iso, date_status
296:def score_unsplit(pipeline, backend):
299:    On the fixture backend the recorded split reply lives in tests/fixtures/llm/split."""
303:    if backend == "fixture":
306:        out = pipeline.run_case(text, backend)
335:def run_cases(pipeline, backend, cases=None):
339:        out = pipeline.run_case(text, backend)
393:def live_metrics(pipeline, backend, text, runs=3):
399:    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
501:def ship_bar(m, a, backend, spec_ok):
519:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
521:    if backend not in LIVE_BACKENDS:
522:        blockers.append(f"backend={backend}: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)")
538:    b, blockers = ship_bar(report["metrics"], report["assertions"], report["backend"], report["spec_matches_golden"])
542:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
544:    results, outs = run_cases(pipeline, backend, cases)
548:        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
551:    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
553:    m["unsplit_paste"] = score_unsplit(pipeline, backend)
555:    if backend in LIVE_BACKENDS:
556:        m.update(live_metrics(pipeline, backend, sample, runs))
561:        from app.backend import flags as FL              # reported, not gated (D-026), but a crash still fails loudly
568:              "backend": sample_out.get("backend", backend), "backend_requested": backend, "models": sample_out.get("models", {}),
583:    L = [f"# Eval report {r['generated_at']}", "", f"**ship_bar_met: {r['ship_bar_met']}**  backend `{r['backend']}`  models `{json.dumps(r['models'])}`", ""]
650:                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")
653:def normalize_backend(raw):
654:    """T-070 r2: strip and lower-case the requested backend name before any guard looks at it, so ' Claude-CLI ' is the claude-cli
655:    backend and is refused like it. Empty means the default fixture backend. Returns None for a value that is not a known backend;
665:    ap.add_argument("--backend", default=None)
688:    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
689:    backend = normalize_backend(raw)
690:    if backend is None:
692:        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
695:    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
696:        # T-070: app.llm.provider.backend_name() silently serves 'fixture' for a live backend without ENABLE_LIVE=1 (D-008/D-020, by design).
698:        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
699:              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
701:    report = build_report(pipeline or load_pipeline(), backend, a.runs)
703:    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:03:56.360Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf \"$SCR/t070r2\" && mkdir -p \"$SCR/t070r2\" && git archive 20471a7 | tar -x -C \"$SCR/t070r2\" && cd \"$SCR/t070r2\" && git -C /Users/arsis/zlayt-pm-project status --short | head -5; echo \"status-exit=$?\"; echo \"--- archive HEAD sha check\"; git -C /Users/arsis/zlayt-pm-project rev-parse 20471a7; echo \"--- LLM_BACKEND reads in app/\"; grep -rn \"LLM_BACKEND\\|ENABLE_LIVE\" app/ --include=*.py | head -20; echo \"--- run_case in app/pipeline.py\"; grep -n \"def run_case\" -A 12 app/pipeline.py | head -30",
 "description": "Pin commit 20471a7 into scratch via git archive and grep backend plumbing"
}
````

### User / tool · 2026-11-02T03:03:56.451Z

**tool result (error)**
````
Permission to use Bash with command SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && rm -rf "$SCR/t070r2" && mkdir -p "$SCR/t070r2" && git archive 20471a7 has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:01.268Z

**tool call — Bash**
````
{
 "command": "mkdir -p /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && git -C /Users/arsis/zlayt-pm-project archive 20471a7 | tar -x -C /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && ls /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b | head -30 && echo '--- git status (working tree)' && git -C /Users/arsis/zlayt-pm-project status --short | head -5 && echo '--- backend plumbing in app/' && grep -rn \"LLM_BACKEND\\|ENABLE_LIVE\" /Users/arsis/zlayt-pm-project/app --include=*.py | head -20 && echo '--- run_case' && grep -n \"def run_case\" -A 8 /Users/arsis/zlayt-pm-project/app/pipeline.py | head -24",
 "description": "Extract commit 20471a7 into a scratch dir and grep backend plumbing"
}
````

### User / tool · 2026-11-02T03:04:01.695Z

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
--- git status (working tree)
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
--- backend plumbing in app/
/Users/arsis/zlayt-pm-project/app/llm/provider.py:3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
/Users/arsis/zlayt-pm-project/app/llm/provider.py:24:    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
/Users/arsis/zlayt-pm-project/app/llm/provider.py:25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
/Users/arsis/zlayt-pm-project/app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
/Users/arsis/zlayt-pm-project/app/llm/provider.py:28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
/Users/arsis/zlayt-pm-project/app/llm/record.py:1:"""Fixture recorder: LLM_BACKEND=claude-cli RECORD_FIXTURES=1 python -m app.llm.record evals/golden/<case>.txt
/Users/arsis/zlayt-pm-project/app/llm/record.py:22:        raise ValueError("record mode needs a live LLM_BACKEND (claude-cli or anthropic-api)")
/Users/arsis/zlayt-pm-project/app/llm/record.py:82:            print("refused: needs a live LLM_BACKEND and RECORD_FIXTURES=1", file=sys.stderr)
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:413:        self.old = os.environ.get("LLM_BACKEND")
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:415:            os.environ["LLM_BACKEND"] = self.name
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:420:            os.environ.pop("LLM_BACKEND", None)
/Users/arsis/zlayt-pm-project/app/backend/pipeline.py:422:            os.environ["LLM_BACKEND"] = self.old
/Users/arsis/zlayt-pm-project/app/backend/api.py:102:    if os.environ.get("LLM_BACKEND") == "anthropic-api" and os.environ.get("ENABLE_LIVE") == "1" and os.environ.get("PROVIDER_CAP_CONFIRMED") != "1":
/Users/arsis/zlayt-pm-project/app/backend/api.py:111:        return provider.backend_name()                          # 'fixture' in demo mode whatever LLM_BACKEND says
/Users/arsis/zlayt-pm-project/app/backend/api.py:114:        return os.environ.get("ENABLE_LIVE") == "1" and (backend() == "claude-cli" or bool(os.environ.get("ANTHROPIC_API_KEY")))
--- run_case
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:05.168Z

**tool call — Bash**
````
{
 "command": "ls app/pipeline.py app/pipeline/ 2>&1 | head; echo '--- app/backend/pipeline.py 405-425'; sed -n 405,425p app/backend/pipeline.py; echo '--- def run_case anywhere'; grep -rn \"def run_case\\|def judge_summary\" app/ --include=*.py; echo '--- provider.py 20-35'; sed -n 20,40p app/llm/provider.py",
 "description": "Locate run_case definition and provider backend resolution"
}
````

### User / tool · 2026-11-02T03:04:05.285Z

**tool result**
````
ls: app/pipeline/: No such file or directory
app/pipeline.py
--- app/backend/pipeline.py 405-425
class _Backend:
    """Temporarily select the LLM backend for one call (eval runner passes it explicitly)."""

    def __init__(self, name):
        self.name, self.old = name, None

    def __enter__(self):
        import os
        self.old = os.environ.get("LLM_BACKEND")
        if self.name:
            os.environ["LLM_BACKEND"] = self.name

    def __exit__(self, *a):
        import os
        if self.old is None:
            os.environ.pop("LLM_BACKEND", None)
        else:
            os.environ["LLM_BACKEND"] = self.old


def _scratch_call(tmp, text):
--- def run_case anywhere
app/backend/api.py:337:    async def run_case(token: str, request: Request):
app/backend/pipeline.py:432:def run_case(text: str, backend: str = None) -> dict:
app/backend/pipeline.py:445:def judge_summary(summary: str, excerpt: str, label: str, backend: str = None) -> str:
--- provider.py 20-35
_record_ok = False


def backend_name() -> str:
    """The backend actually used. A live backend (claude-cli, anthropic-api) needs ENABLE_LIVE=1, or an explicit record_context()
    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
    (D-008/D-020, T-053 security r1): no code path sends a model call from a demo."""
    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
        return "fixture"
    return name


def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
    return hashlib.sha256(blob.encode("utf-8")).hexdigest()


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:14.120Z

**tool call — Bash**
````
{
 "command": "SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b; cd $SCR && echo \"FIXTURE_SET=${FIXTURE_SET:-<unset>} LLM_FIXTURE_DIR=${LLM_FIXTURE_DIR:-<unset>}\" && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python && i=0 && for v in \" claude-cli \" \"Claude-CLI\" \"claude-cli\" \"anthropic-api\" \"openai\" \"claude\" \"fixture\" \"\"; do i=$((i+1)); out=$SCR/probe_$i; env -u ENABLE_LIVE -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=\"$v\" $PY -m evals.run --out $out >$SCR/p$i.stdout 2>$SCR/p$i.stderr; rc=$?; echo \"[$i] LLM_BACKEND=$(printf %q \"$v\") rc=$rc stdout_bytes=$(wc -c <$SCR/p$i.stdout | tr -d ' ') json_files=$(ls $out 2>/dev/null | grep -c '\\.json$') stderr: $(head -c 160 $SCR/p$i.stderr)\"; done; echo '--- --backend flag, no LLM_BACKEND'; for f in \" claude-cli \" \"Claude-CLI\" \"openai\"; do env -u ENABLE_LIVE -u LLM_BACKEND $PY -m evals.run --backend \"$f\" --out $SCR/probe_flag >$SCR/pf.stdout 2>$SCR/pf.stderr; echo \"[--backend $(printf %q \"$f\")] rc=$? stdout_bytes=$(wc -c <$SCR/pf.stdout | tr -d ' ') stderr: $(head -c 140 $SCR/pf.stderr)\"; done; echo '--- control: ENABLE_LIVE=1 path not exercised (no live calls made)'",
 "description": "Probe CLI refusal and unknown-name exit codes in the pinned copy"
}
````

### User / tool · 2026-11-02T03:04:14.182Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to })
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:19.596Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out ./probe_1 2>&1; echo \"rc=$?\"; ls ./probe_1 2>&1 | head -3",
 "description": "Probe padded claude-cli refusal in the pinned copy"
}
````

### User / tool · 2026-11-02T03:04:19.744Z

**tool result**
````
evals.run: backend=claude-cli requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). Re-run with: LLM_BACKEND=claude-cli ENABLE_LIVE=1 python3 -m evals.run --runs 3
rc=2
ls: ./probe_1: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:23.868Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && PY=/Users/arsis/zlayt-pm-project/.venv/bin/python; for v in \" claude-cli \" \"Claude-CLI\" \"claude-cli\" \"anthropic-api\" \"openai\" \"claude\" \"fixture\" \"\"; do rm_out=probe_env; res=$(env -u ENABLE_LIVE LLM_BACKEND=\"$v\" $PY -m evals.run --out ./$rm_out 2>&1; echo \"rc=$?\"); n=$(ls ./$rm_out 2>/dev/null | grep -c '\\.json$'); echo \"LLM_BACKEND=$(printf %q \"$v\") | $(echo \"$res\" | tail -1) | json_written=$n | $(echo \"$res\" | head -1 | cut -c1-150)\"; done; echo '--- --backend flag, LLM_BACKEND unset'; for f in \" claude-cli \" \"Claude-CLI\" \"openai\"; do res=$(env -u ENABLE_LIVE -u LLM_BACKEND $PY -m evals.run --backend \"$f\" --out ./probe_flag 2>&1; echo \"rc=$?\"); echo \"--backend $(printf %q \"$f\") | $(echo \"$res\" | tail -1) | $(echo \"$res\" | head -1 | cut -c1-150)\"; done",
 "description": "Run refusal and unknown-name probe matrix against pinned copy"
}
````

### User / tool · 2026-11-02T03:04:23.932Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No closing quotation) | command: cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf80
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:27.210Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE LLM_BACKEND=\"Claude-CLI\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out ./probe_2 2>&1; echo \"rc=$?\"; ls ./probe_2 2>&1 | head -2",
 "description": "Probe mixed-case Claude-CLI refusal in pinned copy"
}
````

### User / tool · 2026-11-02T03:04:27.351Z

**tool result**
````
evals.run: backend=claude-cli requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). Re-run with: LLM_BACKEND=claude-cli ENABLE_LIVE=1 python3 -m evals.run --runs 3
rc=2
ls: ./probe_2: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:28.636Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE LLM_BACKEND=\"openai\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out ./probe_3 2>&1; echo \"rc=$?\"; ls ./probe_3 2>&1 | head -2",
 "description": "Probe unknown backend name openai in pinned copy"
}
````

### User / tool · 2026-11-02T03:04:28.775Z

**tool result**
````
evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.
rc=2
ls: ./probe_3: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:30.109Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE LLM_BACKEND=\"anthropic-api\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out ./probe_4 2>&1; echo \"rc=$?\"; ls ./probe_4 2>&1 | head -2",
 "description": "Probe anthropic-api refusal without ENABLE_LIVE in pinned copy"
}
````

### User / tool · 2026-11-02T03:04:30.258Z

**tool result**
````
evals.run: backend=anthropic-api requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). Re-run with: LLM_BACKEND=anthropic-api ENABLE_LIVE=1 python3 -m evals.run --runs 3
rc=2
ls: ./probe_4: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:31.625Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE -u LLM_BACKEND /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend \" claude-cli \" --out ./probe_5 2>&1; echo \"rc=$?\"; ls ./probe_5 2>&1 | head -2",
 "description": "Probe padded claude-cli via --backend flag without env"
}
````

### User / tool · 2026-11-02T03:04:31.768Z

**tool result**
````
evals.run: backend=claude-cli requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). Re-run with: LLM_BACKEND=claude-cli ENABLE_LIVE=1 python3 -m evals.run --runs 3
rc=2
ls: ./probe_5: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:33.053Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE -u LLM_BACKEND /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --backend \"openai\" --out ./probe_6 2>&1; echo \"rc=$?\"; ls ./probe_6 2>&1 | head -2",
 "description": "Probe unknown backend via --backend flag openai"
}
````

### User / tool · 2026-11-02T03:04:33.229Z

**tool result**
````
evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.
rc=2
ls: ./probe_6: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:34.586Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t070r2b && env -u ENABLE_LIVE LLM_BACKEND=\"fixture\" /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --out ./probe_7 2>&1 | tail -3; echo \"rc=${PIPESTATUS[0]}\"; ls ./probe_7 2>&1 | head -4",
 "description": "Positive control: fixture backend runs and writes a labelled report"
}
````

### User / tool · 2026-11-02T03:04:35.830Z

**tool result**
````
ship_bar_met=False backend=fixture report=probe_7/20261102T030435Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
rc=1
20261102T030435Z.md
latest.json
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:46.997Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp -R t070r2b m1 && cp -R t070r2b m2 && cp -R t070r2b m3 && cp -R t070r2b m4 && cp -R t070r2b base && /usr/bin/python3 -c \"import pathlib,sys; print('py ok')\" && echo copies-ok",
 "description": "Create baseline and mutant copies of the pinned tree"
}
````

### User / tool · 2026-11-02T03:04:49.180Z

**tool result**
````
py ok
copies-ok
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:04:53.297Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && /usr/bin/python3 -c \"\nimport pathlib\nmuts = {\n 'm1': ('name = (raw or \\\"\\\").strip().lower() or \\\"fixture\\\"', 'name = (raw or \\\"\\\") or \\\"fixture\\\"'),\n 'm2': ('return name if name in KNOWN_BACKENDS else None', 'return name'),\n 'm3': ('backend = normalize_backend(raw)', 'backend = raw or \\\"fixture\\\"'),\n 'm4': ('if pipeline is None and backend in LIVE_BACKENDS and', 'if pipeline is None and raw in LIVE_BACKENDS and'),\n}\nfor k,(old,new) in muts.items():\n    p = pathlib.Path(k)/'evals'/'run.py'\n    s = p.read_text()\n    n = s.count(old)\n    assert n == 1, (k, n)\n    p.write_text(s.replace(old,new))\n    print(k, 'applied', n)\n\"; for k in base m1 m2 m3 m4; do echo \"== $k\"; cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/$k && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py 2>&1 | tail -12; done",
 "description": "Apply four normalization mutants to scratch copies and run eval runner tests"
}
````

### User / tool · 2026-11-02T03:05:29.168Z

**tool result**
````
m1 applied 1
m2 applied 1
m3 applied 1
m4 applied 1
== base
................................................................         [100%]
64 passed in 1.97s
== m1
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Claude-CLI]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[CLAUDE-CLI\n]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[\tanthropic-api  ]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Anthropic-API]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[ Claude-Cli  ]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[   -fixture]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[FIXTURE -fixture]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[ claude-cli -claude-cli]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[Claude-CLI-claude-cli]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[\tANTHROPIC-API\n-anthropic-api]
FAILED tests/unit/test_eval_runner.py::test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name
12 failed, 52 passed in 2.13s
== m2
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[openai]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[claude]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[claude-cli-x]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[anthropic]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[fixtures]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[lol]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[openai]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[Fixture!]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[openai-None]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[claude-None]
FAILED tests/unit/test_eval_runner.py::test_normalize_backend_strips_lowercases_and_rejects_unknown[claude-cli ok-None]
11 failed, 53 passed in 7.86s
== m3
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Anthropic-API]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[openai]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[claude]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[claude-cli-x]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[anthropic]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[fixtures]
FAILED tests/unit/test_eval_runner.py::test_unknown_backend_name_exits_2_with_a_clear_message[lol]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[openai]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[ Claude-Cli  ]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[Fixture!]
FAILED tests/unit/test_eval_runner.py::test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name
15 failed, 49 passed in 12.56s
== m4
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cc45820e9c1c3 step=split attempt=1 prompt_hash=d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=ce404ff28446c step=extract attempt=1 prompt_hash=a149da472e6d93e42cf7c4944b30a878d18768e926fa8c94524821e5f60fc265
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cc60fda089a91 step=conflicts attempt=1 prompt_hash=09ad5afa7266922e9d80691655f729f6bbc6da907db9053b4e9b51c753b37915
WARNING  zlayt.llm:audited.py:87 llm call failed call_id=cd92eb80726d2 step=flags attempt=1 prompt_hash=4b50862f7e4e667cf8acc5d401e59db51d260422949aff262bb517ac450730f0
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[ claude-cli ]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Claude-CLI]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[CLAUDE-CLI\n]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[\tanthropic-api  ]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Anthropic-API]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[ Claude-Cli  ]
6 failed, 58 passed in 9.85s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:05:46.964Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad && cp -R t070r2b m5 && /usr/bin/python3 -c \"\nimport pathlib\np = pathlib.Path('m5')/'evals'/'run.py'\ns = p.read_text()\nold = 'and os.environ.get(\\\"ENABLE_LIVE\\\") != \\\"1\\\":'\nassert s.count(old) == 1, s.count(old)\np.write_text(s.replace(old, 'and os.environ.get(\\\"ENABLE_LIVE\\\") == \\\"1\\\":'))\nprint('m5 applied')\n\" && cd m5 && PYTHONPATH=. /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py 2>&1 | grep -E \"FAILED|passed|failed\" | tail -8; echo '--- provider dispatch for unknown names (app, outside 20471a7 scope)'; grep -n \"def complete\\|name ==\\|name in\\|backend_name()\" /Users/arsis/zlayt-pm-project/app/llm/provider.py | head -20",
 "description": "Run ENABLE_LIVE guard inversion mutant and inspect provider dispatch"
}
````

### User / tool · 2026-11-02T03:05:55.243Z

**tool result**
````
m5 applied
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[ claude-cli ]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Claude-CLI]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[CLAUDE-CLI\n]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[\tanthropic-api  ]
FAILED tests/unit/test_eval_runner.py::test_padded_or_mixed_case_live_backend_without_enable_live_is_refused[Anthropic-API]
FAILED tests/unit/test_eval_runner.py::test_backend_flag_is_validated_like_the_env_var[ Claude-Cli  ]
FAILED tests/unit/test_eval_runner.py::test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name
8 failed, 56 passed in 7.54s
--- provider dispatch for unknown names (app, outside 20471a7 scope)
23:def backend_name() -> str:
92:def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
93:    name = backend_name()
95:    if name == "fixture":
97:    elif name in ("claude-cli", "anthropic-api"):
100:        if name == "claude-cli":
113:def complete(model: str, system: str, user: str, json_schema: dict) -> dict:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:05:56.626Z

**tool call — Bash**
````
{
 "command": "sed -n 92,112p /Users/arsis/zlayt-pm-project/app/llm/provider.py",
 "description": "Read provider dispatch for live and unknown backend names"
}
````

### User / tool · 2026-11-02T03:05:56.712Z

**tool result**
````
def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
    name = backend_name()
    key = prompt_hash(model, system, user, json_schema)
    if name == "fixture":
        res = _fixture.call(model, system, user, json_schema, key=key)
    elif name in ("claude-cli", "anthropic-api"):
        if _recording() and not _record_ok:
            raise ValueError("record mode needs record_context() over text from evals/golden")
        if name == "claude-cli":
            from app.llm.backends import claude_cli as be
        else:
            from app.llm.backends import anthropic_api as be
        res = be.call(model, system, user, json_schema, key=key)
    else:
        raise LLMError(f"UNKNOWN_BACKEND {name}")
    validate_schema(res.output, json_schema)
    if name != "fixture" and _recording():
        _fixture.write(key, res, model)
    return res
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:18.919Z

**tool call — Bash**
````
{
 "command": "grep -n \"def normalize_backend\\|raw = a.backend\\|backend = normalize_backend\\|unknown LLM_BACKEND\\|ENABLE_LIVE\\\") != \\\"1\\\"\\|build_report(pipeline\" evals/run.py && grep -n \"def test_\" tests/unit/test_eval_runner.py | tail -6 && git -C /Users/arsis/zlayt-pm-project show 20471a7:evals/run.py | grep -c \"unknown LLM_BACKEND\"",
 "description": "Get exact line numbers for guard, normalizer and new tests at HEAD"
}
````

### User / tool · 2026-11-02T03:06:19.044Z

**tool result**
````
542:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None):
653:def normalize_backend(raw):
688:    raw = a.backend if a.backend is not None else os.environ.get("LLM_BACKEND", "")
689:    backend = normalize_backend(raw)
692:        print(f"evals.run: unknown LLM_BACKEND {raw!r}; known backends are {', '.join(KNOWN_BACKENDS)} (after strip and lower-case). "
695:    if pipeline is None and backend in LIVE_BACKENDS and os.environ.get("ENABLE_LIVE") != "1":   # an injected (fake) pipeline never reaches the provider
701:    report = build_report(pipeline or load_pipeline(), backend, a.runs)
362:def test_live_backend_without_enable_live_is_refused(monkeypatch, tmp_path, capsys):
372:def test_padded_or_mixed_case_live_backend_without_enable_live_is_refused(raw, monkeypatch, tmp_path, capsys):
382:def test_unknown_backend_name_exits_2_with_a_clear_message(raw, monkeypatch, tmp_path, capsys):
393:def test_backend_flag_is_validated_like_the_env_var(flag, monkeypatch, tmp_path, capsys):
410:def test_normalize_backend_strips_lowercases_and_rejects_unknown(raw, expected):
414:def test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name(monkeypatch, tmp_path):
1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:37.346Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-070-staff-engineer-r2.md",
 "content": "# T-070 round 2 review: staff-engineer-reviewer (commit 20471a7)\n\n**Verdict: pass.** No blockers, no majors. The r1 major is closed: a padded or mixed-case live name without `ENABLE_LIVE` now exits 2, an unknown name exits 2, and a test fails when the normalization is mutated out. One nit (wording of the error message when the value came from `--backend`).\n\nPinned to 20471a7 with `git archive` (HEAD at review time is 20471a7; the working tree has unrelated uncommitted changes under `.claude/agent-memory/`, which I did not touch). Scope is `evals/run.py` and `tests/unit/test_eval_runner.py` only.\n\n**Checks against the three asks**\n\n1. `\" claude-cli \"` and `\"Claude-CLI\"` without `ENABLE_LIVE`: exit 2, no stdout, no report directory written, and the refusal is at `evals/run.py:695`, before `build_report` at `:701`, so no fixture run happens. Probes below show rc=2 for both, and `ls` of the `--out` directory fails (nothing written).\n2. Unknown names: `openai`, `claude`, `claude-cli-x`, `anthropic`, `fixtures`, `lol` (env and `--backend`) exit 2 with \"Nothing was run.\" and no report. Covered by `tests/unit/test_eval_runner.py:382-391` and `:393-404`.\n3. Normalization mutated out: four mutants in scratch copies of the pinned tree each fail the unit file (see table). The guard-inversion mutant (`ENABLE_LIVE != \"1\"` changed to `== \"1\"`) also fails 8 tests, including the new `test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name`, so the r1 minor is closed too.\n\n**Deterministic results**\n\n- `.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py` (working tree, HEAD 20471a7): `64 passed in 1.86s`.\n- Same file in the pinned copy with `PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py`: `64 passed in 1.97s`.\n\n**Mutants (scratch copies, not committed)**\n\n| Mutant | Change | Result |\n|---|---|---|\n| m1 | `normalize_backend` drops `.strip().lower()` | 12 failed, 52 passed |\n| m2 | `normalize_backend` returns any name (no unknown check) | 11 failed, 53 passed |\n| m3 | `main` uses `raw or \"fixture\"` instead of `normalize_backend(raw)` | 15 failed, 49 passed |\n| m4 | guard tests `raw in LIVE_BACKENDS` instead of normalized `backend` | 6 failed, 58 passed |\n| m5 | `ENABLE_LIVE != \"1\"` inverted to `== \"1\"` | 8 failed, 56 passed |\n\n**CLI probes (pinned copy, `python -m evals.run`, ENABLE_LIVE unset, no live call made)**\n\n- `LLM_BACKEND=\" claude-cli \"`: rc=2, stderr `evals.run: backend=claude-cli requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend (D-008/D-020). ...`, no output dir.\n- `LLM_BACKEND=\"Claude-CLI\"`: rc=2, same message, no output dir.\n- `LLM_BACKEND=\"anthropic-api\"`: rc=2, ENABLE_LIVE message, no output dir.\n- `LLM_BACKEND=\"openai\"`: rc=2, `evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.`, no output dir.\n- `--backend \" claude-cli \"` with LLM_BACKEND unset: rc=2, ENABLE_LIVE message.\n- `--backend \"openai\"`: rc=2, `unknown LLM_BACKEND 'openai'...` (see nit).\n- Positive control `LLM_BACKEND=\"fixture\"`: rc=1, `ship_bar_met=False backend=fixture report=probe_7/20261102T030435Z.md`, blockers `4_no_invented_facts` and `backend=fixture: determinism_3run and unsupported_count_3run need a live backend`. The fixture path still runs and labels itself honestly.\n\n**Read-only checks**\n\n- `evals/run.py:688-694` normalizes once and feeds the normalized name to the guard and to `build_report`. The pipeline gets the same normalized name: `app/backend/pipeline.py:413-422` (`_Backend`) sets `LLM_BACKEND` to it for the call, so the live path and the guard agree.\n- `app/llm/provider.py:27` strips the same variable, and `:92-111` raises `LLMError(\"UNKNOWN_BACKEND ...\")` for an unrecognised live-looking name, so the app side does not fall through silently either.\n\n## Finding\n\n**nit: the unknown-name message says `LLM_BACKEND` even when the value came from `--backend`.**\n- Evidence: `evals/run.py:692` prints `unknown LLM_BACKEND {raw!r}` for both sources. Repro: `env -u ENABLE_LIVE -u LLM_BACKEND .venv/bin/python -m evals.run --backend \"openai\" --out <dir>` prints `evals.run: unknown LLM_BACKEND 'openai'; ...`. The test `tests/unit/test_eval_runner.py:393-404` asserts the same wording for the flag path, so the test locks it in.\n- Why it matters: the operator reads the wrong variable name. Nothing is run and the exit code is correct, so this is cosmetic.\n- Fix: name the source, for example `unknown backend {raw!r} from {source}` where `source` is `--backend` or `LLM_BACKEND`. Update the flag-path assertion to match.\n- Acceptance test: `--backend openai` prints a message containing `--backend` and not `LLM_BACKEND`; `LLM_BACKEND=openai` still prints `LLM_BACKEND`; both exit 2 and write no `*.json`.\n\n## Out of scope for this card (noted, not a finding)\n\n- `app/llm/provider.py:27-29` serves `fixture` silently for any non-fixture `LLM_BACKEND` when `ENABLE_LIVE` is unset (by design, D-008/D-020). The eval runner now refuses these names; the app does not. This is outside 20471a7's diff, so I did not count it against T-070.\n\n```json\n{\"card\": \"T-070\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit 20471a7 (evals/run.py, tests/unit/test_eval_runner.py); pinned via git archive 20471a7; HEAD 20471a7 at review time; no app URL; eval runner only\",\n \"exercised\": [\n   \"git show 20471a7 -- evals/run.py and -- tests/unit/test_eval_runner.py (full diff read)\",\n   \"sed/grep read of evals/run.py main() at HEAD (lines 661-706) and normalize_backend (653-658), load_pipeline (631), refuse_curated (640)\",\n   \"app/llm/provider.py:20-30 and :92-111; app/backend/pipeline.py:405-432 (_Backend, run_case)\",\n   \".venv/bin/python -m pytest -q tests/unit/test_eval_runner.py (working tree): 64 passed in 1.86s\",\n   \"git archive 20471a7 | tar -x into scratch t070r2b; PYTHONPATH=. .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_eval_runner.py: 64 passed in 1.97s\",\n   \"CLI probe env -u ENABLE_LIVE LLM_BACKEND=' claude-cli ' python -m evals.run --out ./probe_1: rc=2, ENABLE_LIVE message, no output dir\",\n   \"CLI probe LLM_BACKEND=Claude-CLI (ENABLE_LIVE unset): rc=2, ENABLE_LIVE message, no output dir\",\n   \"CLI probe LLM_BACKEND=anthropic-api (ENABLE_LIVE unset): rc=2, ENABLE_LIVE message, no output dir\",\n   \"CLI probe LLM_BACKEND=openai: rc=2, 'unknown LLM_BACKEND ... Nothing was run.', no output dir\",\n   \"CLI probe --backend ' claude-cli ' with LLM_BACKEND unset: rc=2, ENABLE_LIVE message\",\n   \"CLI probe --backend openai: rc=2, unknown-name message (wording nit)\",\n   \"CLI control LLM_BACKEND=fixture (ENABLE_LIVE unset): rc=1, 'ship_bar_met=False backend=fixture', report written to scratch\",\n   \"Mutant m1 (normalize drops strip/lower): pytest tests/unit/test_eval_runner.py -> 12 failed, 52 passed\",\n   \"Mutant m2 (normalize accepts any name): pytest -> 11 failed, 53 passed\",\n   \"Mutant m3 (main uses raw or 'fixture' instead of normalize_backend): pytest -> 15 failed, 49 passed\",\n   \"Mutant m4 (guard tests raw instead of normalized name): pytest -> 6 failed, 58 passed\",\n   \"Mutant m5 (ENABLE_LIVE guard inverted to == '1'): pytest -> 8 failed, 56 passed, including test_correctly_configured_padded_live_run_reaches_the_pipeline_with_the_normalized_name\",\n   \"Mutants were applied only in scratch copies (m1-m5 under the scratchpad); no product file changed; no live backend was invoked (ENABLE_LIVE never set to 1 outside monkeypatched tests)\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"ac_met_as_written\": 5, \"padded_and_mixed_case_refused\": 5, \"unknown_names_exit_2\": 5, \"tests_non_vacuous_under_mutation\": 5, \"no_silent_fallback\": 5, \"error_message_accuracy\": 3, \"scope_discipline\": 5},\n \"findings\": [\n   {\"severity\": \"nit\",\n    \"title\": \"Unknown-name message says LLM_BACKEND even when the value came from --backend\",\n    \"evidence\": \"evals/run.py:692: print(f\\\"evals.run: unknown LLM_BACKEND {raw!r}; known backends are ...\\\"). Repro: env -u ENABLE_LIVE -u LLM_BACKEND .venv/bin/python -m evals.run --backend \\\"openai\\\" --out <dir> -> stderr \\\"evals.run: unknown LLM_BACKEND 'openai'; known backends are fixture, claude-cli, anthropic-api (after strip and lower-case). Nothing was run.\\\" rc=2. tests/unit/test_eval_runner.py:393-404 asserts the same wording for the flag path.\",\n    \"why_it_matters\": \"The operator is told to look at the wrong variable. The run is still refused with rc 2 and no report, so this is cosmetic, but it costs time when debugging a command line.\",\n    \"fix\": \"Name the source in the message: 'unknown backend {raw!r} from {source}' where source is '--backend' or 'LLM_BACKEND'. Update the flag-path assertion in test_backend_flag_is_validated_like_the_env_var to match.\",\n    \"acceptance_test\": \"--backend openai prints a message containing '--backend' and not 'LLM_BACKEND'; LLM_BACKEND=openai still prints 'LLM_BACKEND'; both exit 2 and write no *.json under --out.\"}\n ],\n \"whats_right\": [\n   \"Normalization happens once (evals/run.py:688-689), and the guard, build_report and _Backend (app/backend/pipeline.py:413-422) all see the same normalized name, so the refusal and the live path cannot disagree.\",\n   \"Refusals return 2 before build_report (evals/run.py:695-700 vs 701), so a refused request runs no fixture and writes no report; the probes confirm no output directory is created.\",\n   \"The new tests are non-vacuous: all four normalization and guard mutants and the guard inversion each fail between 6 and 15 tests, and the reach-the-pipeline test closes the r1 minor.\"\n ],\n \"questions_for_chris\": [\"Should app/llm/provider.py backend_name() (lines 27-29) also refuse unknown LLM_BACKEND names when ENABLE_LIVE is unset, the way the eval runner now does? Today it silently serves fixture, which is the by-design demo behaviour (D-008/D-020); I did not count it against T-070.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T03:06:37.518Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-070-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:39.018Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python tools/board.py validate 2>&1 | tail -15; echo \"rc=$?\"",
 "description": "Run read-only board validator over review files"
}
````

### User / tool · 2026-11-02T03:06:39.177Z

**tool result**
````
ok (76 file(s))
rc=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:42.620Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && tail -5 project_harness_review_patterns.md && echo '---' && grep -n \"T-070\" MEMORY.md",
 "description": "Check memory index and harness pattern file tail before updating"
}
````

### User / tool · 2026-11-02T03:06:42.718Z

**tool result**
````
- (T-028) at f454c41 `app/backend/`, `app/pipeline.py` and `tests/unit/` are empty: `pytest tests/unit -q` exits 5 (no tests), `python -m app.pipeline` exits 1. Doc-stage cards cannot exercise the CLI; say so in `exercised`.
- (T-065/T-066 r2, 2026-11-01) reviewer-write-guard makes existing review files append-only: an Edit to `reviews/<card>-<persona>.md` is denied. Write a new `-r2.md` file instead, and fix small wording slips in the next round, not in place.
- (T-065/T-066 r2) `rm -rf` in a Bash chain with `git archive` was denied by the permission guard. `mkdir -p` + `git archive | tar -x -C <dir>` works, and `cp -R` for mutant copies works. Pass `/usr/bin/python3 -I script.py` for file-based edits to scratch copies (anchor-count asserts, then write).
- (T-065/T-066 r2) board-guard denies `python3 -c` (and a `tee` chain) containing backslash escapes or backticks, including `\n` in a string. Put JSON checks in a script file under the scratchpad and run that.
- (T-065/T-066 r2) `board.py validate <path>` is read-only and works on a review file; use it to confirm the D.2 shape before replying.
---
17:- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-067 r2 mixed-result drop and post-term negation, persona mismatch
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:47.049Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && cat >> project_harness_review_patterns.md <<'EOF'\n- (T-070 r2, 2026-11-01) A shell `>` redirect into the scratchpad is denied by board-guard (\"reviewers may only write under reviews/...\"), even though `tar -x -C` and `cp -R` into the same dir pass. Capture output with `2>&1; echo rc=$?` inside the command instead of redirecting. Chained `$(...)` loops with nested quotes trip git-guard's parser; use one probe per Bash call.\nEOF\ncat >> project_t070_t067_review_patterns.md <<'EOF'\n\n## T-070 r2 (20471a7) — closed\n- The fix normalizes once (`normalize_backend`, evals/run.py:688-689) and the guard, `build_report` and `_Backend` (app/backend/pipeline.py:413-422) all see the same name. Padded, mixed-case and unknown names exit 2 with no report. Four normalization mutants and a guard inversion each fail 6-15 tests in `tests/unit/test_eval_runner.py`.\n- Residual nit: the unknown-name message says `LLM_BACKEND` even when the value came from `--backend` (evals/run.py:692).\n- The app side (`app/llm/provider.py:27-29`) still serves fixture silently for unknown names when ENABLE_LIVE is unset (by design, D-008/D-020). Out of the eval card's scope; raised as a question for Chris.\n- **Why:** a fix that normalizes in the guard can still disagree with the consumer. Check that the guard and the consumer use the same variable, not just that the tests pass.\n- **How to apply:** for any refuse-on-name guard, mutate the normalizer, the guard and the consumer separately; a passing suite with only the guard mutated proves little.\nEOF\ncd /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer && python3 -c \"print('ok')\" >/dev/null; echo done",
 "description": "Append T-070 r2 patterns and harness gotchas to reviewer memory"
}
````

### User / tool · 2026-11-02T03:06:47.171Z

**tool result**
````
done
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:49.422Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T03:06:49.431Z

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
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-067 r2 mixed-result drop and post-term negation, persona mismatch
18	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:51.150Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-067 r2 mixed-result drop and post-term negation, persona mismatch",
 "new_string": "- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — T-070 r1 exact-string guard vs strip, T-070 r2 normalizer+guard+consumer mutation (pass), T-067 r2 mixed-result drop, persona mismatch"
}
````

### User / tool · 2026-11-02T03:06:51.252Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T03:06:52.793Z

T-070 r2 passes (0 blockers, 0 majors, 1 nit): padded/mixed-case and unknown LLM_BACKEND names exit 2 with no report, the 64 eval-runner tests pass, and four normalization mutants plus a guard inversion each fail 6–15 tests. Review: /Users/arsis/zlayt-pm-project/reviews/T-070-staff-engineer-r2.md (board validate: ok, 76 files).
