# Subagent: Staff re-check: T-197 (Staff re-check: T-197)

Source: `agent-aabc04a82f2753fcf.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T22:51:39.721Z

Re-check T-197 in /Users/arsis/zlayt-pm-project as the staff engineer, starting from a fresh context. Read reviews/T-197-staff-engineer.md. Your one major was that the first-paint e2e was untracked and no frontend read `local_mode`; commit 9ab8cae should fix it.

Verify against a `git archive HEAD` copy:
- the guided frontend reads `health.local_mode`;
- tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server is committed with no xfail, and passes when run with E2E_REQUIRE_DB=1.

Write reviews/T-197-staff-engineer-r2.md in D.2 format, applying the verdict rule. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:42.127Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T22:51:42.136Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:42.327Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer.md"
}
````

### User / tool · 2026-11-02T22:51:42.334Z

**tool result**
````
1	# T-197 review (staff-engineer): GET /api/health reports local_mode
2	
3	**Verdict: changes** (0 blockers, 1 major, 1 minor, 1 nit).
4	
5	**Reviewed sha: 612dc2c.** HEAD was dfd9b11 at my first rev-parse and moved to 612dc2c during the review. Every finding is for 612dc2c. The working tree is dirty and was not reviewed. Model recorded is claude-haiku-5-5, the model I ran as; the dossier expected claude-sonnet-5-5.
6	
7	## What holds at 612dc2c
8	- The field is `"local_mode": local_mode()` at `app/backend/api.py:266`, the same function that gates `/api/cases` (api.py:272) and `/api/library` (api.py:282). It is read per request.
9	- In five 200 cases (ZLAYT_MODE unset, `public`, `local`, `LOCAL`, and unset from 192.168.1.5) the body's `local_mode` equals `local_mode()` and is a bool. In local mode a non-loopback peer gets 403 from the middleware at api.py:221 before the body is built.
10	- The body adds no sensitive value. `local_mode` is a bool, and the ZLAYT_MODE value is not echoed.
11	- `tests/unit/test_api_routes.py:396-403` asserts True for `local`, False for unset, and False for `public`. Five mutants (hardcoded False, hardcoded True, field removed, public counted as local, string instead of bool) each fail it. The control passes.
12	- `memory/contracts/api.md:50` shows the field in the example and `:57` documents it.
13	
14	## Findings
15	- **major: the card's e2e AC is not met at 612dc2c.** `tests/e2e/guided/test_round2.py` is untracked (`git status` shows `??`) and absent at 612dc2c. No file under `app/frontend` reads `local_mode` at 612dc2c. `app/frontend/guided/step1.js:28` still calls `GET /library` on `/new`, and `home.js:118` still calls `G.api.cases` with no gate. The T-181 r2 first-paint request is still there. The working tree already has the frontend gate uncommitted. Not a blocker: the backend field is correct, the failure is caught, and nothing regressed.
16	- **minor: `api.md:57` describes UI behaviour in the present tense that does not exist at 612dc2c.** It should read "will" until the frontend lands.
17	- **nit: `api.md:17`** endpoint summary row omits local_mode.
18	
19	## Exercised
20	- `python3 tools/board.py show T-197`: in_progress, claimed by backend, AC1 done false, commits empty.
21	- `git rev-parse HEAD`, `git log --oneline -i --grep=T-197`, `git show --stat 612dc2c`.
22	- `git archive 612dc2c` extracted to the session scratchpad. `git show 612dc2c:app/backend/api.py | diff -q` against the archive copy: identical.
23	- In the archive, with the project venv: `python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -q` gave 35 passed; `-k health` gave 3 passed; `-k health_reports_local_mode -v` gave 1 passed.
24	- `artifacts/review-evidence/T-197-staff-engineer/health_probe.py` with `python -I` on the archive. Output is in the transcript.
25	- `artifacts/review-evidence/T-197-staff-engineer/mutants.py` with `python -I` on scratch copies. M0 control 1 passed; M1 to M5 each 1 failed.
26	- Read `app/backend/api.py` at 83, 221, 263-266, 270-292; `memory/contracts/api.md` at 17, 50, 57; `app/frontend/guided/step1.js:28`; `app/frontend/guided/home.js:118`.
27	- `grep -rln local_mode app/frontend` in the archive: 0 files.
28	- Not exercised: a live server on :7860, the public-mode browser first paint, the named e2e test (absent at the sha), the full unit suite.
29	
30	```json
31	{"card": "T-197", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
32	 "scope": "Reviewed commit 612dc2c (feat(backend): GET /api/health reports local_mode (T-197)): app/backend/api.py, memory/contracts/api.md, tests/unit/test_api_routes.py. HEAD was dfd9b11 at the first rev-parse and moved to 612dc2c during the review; all findings are for 612dc2c. The working tree is dirty (uncommitted frontend, e2e and api.py edits) and was not reviewed. No app URL (in-process TestClient only). No sample case run (outside the card AC).",
33	 "exercised": [
34	  "python3 tools/board.py show T-197 -> status in_progress, claimed_by backend, AC1 done false, commits []",
35	  "git rev-parse HEAD -> dfd9b11 at first call, then 612dc2cca3fed1b5f58728042593585056426aca; git log --oneline -i --grep=T-197 -> 612dc2c only",
36	  "git show --stat 612dc2c -> 3 files, 14 insertions, 2 deletions (app/backend/api.py, memory/contracts/api.md, tests/unit/test_api_routes.py)",
37	  "git archive 612dc2c | tar -x into scratchpad/T-197-612dc2c; git show 612dc2c:app/backend/api.py | diff -q against the archive copy -> identical",
38	  "cd archive && .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -q -> 35 passed in 6.94s; -k health -> 3 passed; -k health_reports_local_mode -v -> 1 passed",
39	  "artifacts/review-evidence/T-197-staff-engineer/health_probe.py run with python -I against the archive: ZLAYT_MODE unset, public, local, LOCAL (case), unset from 192.168.1.5, local from 192.168.1.5. Body.local_mode equals local_mode() and is a bool in each of the five 200 cases; local from a non-loopback peer returns 403 with no health body (middleware at api.py:221)",
40	  "artifacts/review-evidence/T-197-staff-engineer/mutants.py run with python -I on scratch copies of the archive (exact-count replacement asserted): M0 control 1 passed; M1 hardcoded False, M2 hardcoded True, M3 field removed, M4 public counted as local, M5 string instead of bool: each 1 failed",
41	  "Read app/backend/api.py:83 (local_mode), 221 (loopback gate applies to every path), 263-266 (health route returns local_mode: local_mode()), 270-282 and 292 (/api/cases and /api/library 404 when not local_mode())",
42	  "Read memory/contracts/api.md:50 (example shape with local_mode) and :57 (prose that says the guided UI reads it on first paint)",
43	  "grep -rln local_mode app/frontend in the 612dc2c archive -> 0 files; app/frontend/guided/step1.js:28 calls GET /library unconditionally on /new; app/frontend/guided/home.js:118 calls G.api.cases with no local_mode check",
44	  "git cat-file -e 612dc2c:tests/e2e/guided/test_round2.py -> absent; git status --short tests/e2e/guided -> '?? tests/e2e/guided/test_round2.py' (untracked). The named e2e test was not run because it does not exist at the reviewed sha. No browser run",
45	  "Not exercised: a live server on :7860 (not started), the public-mode browser first paint, the full unit suite (outside the brief)"
46	 ],
47	 "verdict": "changes",
48	 "scores": {"field_equals_local_mode_in_every_mode": 5, "leaks_nothing_sensitive": 5, "api_md_documents_field": 4, "unit_test_asserts_both_values": 5, "mutants_killed_by_unit_test": 5, "card_ac_first_paint_e2e_met_at_sha": 1},
49	 "findings": [
50	  {"severity": "major",
51	   "title": "Card AC1 e2e half is not met at 612dc2c: the named test is untracked, no frontend reads local_mode, and public first paint still requests /library and /api/cases",
52	   "evidence": "git cat-file -e 612dc2c:tests/e2e/guided/test_round2.py -> absent; git status --short tests/e2e/guided -> '?? tests/e2e/guided/test_round2.py'; grep -rln local_mode app/frontend (612dc2c archive) -> 0 files; app/frontend/guided/step1.js:28 'G.api.call(\"GET\", \"/library\", ...)' runs on /new with no gate; app/frontend/guided/home.js:118 'G.api.cases(signal)' runs with no gate. Card AC1 text: 'tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server passes (no xfail)'.",
53	   "why_it_matters": "The card title says the guided UI must never probe /api/cases or /api/library in public mode (T-181 r2 first-paint 404). At the reviewed commit the field exists but nothing reads it, so the first-paint request still happens. Not a blocker: the backend field is correct, the probe failure is caught (step1.js:28 sets lib = null), and nothing regressed. It is a must-fix before the card can close, because AC1 is not satisfied.",
54	   "fix": "Land the frontend half on the same card: gate the /library call in step1.js:28 and the G.api.cases call in home.js:118 on health.local_mode !== false, and commit tests/e2e/guided/test_round2.py without an xfail marker. The working tree already has this change uncommitted (grep shows local_mode in app/frontend/guided/step1.js:28 and home.js:119 there, context only). Then move to in_review at the new sha.",
55	   "acceptance_test": "At the committed sha: tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server passes; git grep -n xfail <sha> -- tests/e2e/guided/test_round2.py prints nothing; git grep -n local_mode <sha> -- app/frontend is non-empty."},
56	  {"severity": "minor",
57	   "title": "api.md states present-tense UI behaviour that is false at 612dc2c",
58	   "evidence": "memory/contracts/api.md:57: 'The guided UI reads it on first paint and never probes those routes when it is `false`, so a public server sees no 404.' versus grep -rln local_mode app/frontend -> 0 files at 612dc2c, and step1.js:28 / home.js:118 unconditional.",
59	   "why_it_matters": "A reader of the contract, including the frontend worker writing the missing half, would assume the gate exists. The field itself is documented correctly at api.md:50 and :57 (name, type, meaning, route gating). Minor because the claim describes the intended consumer behaviour, not the backend output; it becomes true only when finding 1 lands.",
60	   "fix": "Until the frontend lands, reword line 57 to 'The guided UI will read it ...' or land the frontend change in the same commit as the doc.",
61	   "acceptance_test": "After the frontend commit: git grep -n local_mode <sha> -- app/frontend is non-empty and api.md:57 matches that sha; before it, api.md:57 uses future tense."},
62	  {"severity": "nit",
63	   "title": "api.md endpoint summary row does not list local_mode",
64	   "evidence": "memory/contracts/api.md:17: '| GET | `/api/health` | backend, demo mode, models, limits, banner text |'",
65	   "why_it_matters": "Minor discoverability gap in the summary table; the full shape at :50 is correct.",
66	   "fix": "Add 'local mode flag' to the row.",
67	   "acceptance_test": "grep -n 'local mode' memory/contracts/api.md shows the row at line 17."}
68	 ],
69	 "whats_right": [
70	  "The field is the same local_mode() call that gates /api/cases and /api/library, read per request at api.py:266, so it cannot drift from the gate.",
71	  "The new unit test asserts True and False, plus a 'public' value that must read False; five mutants (hardcoded False, hardcoded True, field removed, public counted as local, string not bool) each fail it, and the unmutated control passes.",
72	  "In local mode a non-loopback client gets 403 from the middleware at api.py:221 before the health body is built, so a public client only ever sees local_mode false; the field discloses nothing beyond the existing demo_mode and backend fields."
73	 ],
74	 "questions_for_chris": ["Should T-197 close on the backend half alone with the frontend and e2e split into a new card, or stay open until the first-paint e2e passes? The card AC currently requires the e2e."]}
75	```
76	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:42.677Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 && git show --stat 9ab8cae | head -40",
 "description": "Show recent commits and the fix commit stats"
}
````

### User / tool · 2026-11-02T22:51:42.799Z

**tool result**
````
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
dfd9b11 docs(submission): NEEDS_CHRIS publish-from-snapshot item, T-193, row 8 to P2
3feb096 test(backend): T-177 r4 e2e: golden notes normalize the prepared disclosure line; classic tag tooltip stays exempt until the frontend card
commit 9ab8caeb27d6e7a35a533327fa38737fc6a38050
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 16:50:49 2026 -0600

    fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 .claude/agent-memory/frontend/MEMORY.md            |   5 +
 .../agent-memory/frontend/project_t181_round2.md   |  14 +
 app/frontend/guided/app.js                         |  17 +-
 app/frontend/guided/core.js                        |   9 +-
 app/frontend/guided/home.js                        |   3 +-
 app/frontend/guided/review.css                     |  14 +-
 app/frontend/guided/review.js                      |  74 +++-
 app/frontend/guided/step1.js                       |  13 +-
 app/frontend/guided/step2.js                       |  55 ++-
 app/frontend/guided/step3.css                      |  12 +
 app/frontend/guided/step3.js                       |  14 +-
 app/frontend/guided/step4.css                      |   3 +-
 app/frontend/guided/step4.js                       |  18 +-
 app/frontend/timeline.js                           |   2 +-
 tests/e2e/guided/test_round2.py                    | 389 +++++++++++++++++++++
 tests/e2e/guided/test_step1.py                     |   2 +-
 tests/e2e/guided/test_step3.py                     |   2 +-
 tests/e2e/test_demo_provenance.py                  |   2 +-
 18 files changed, 600 insertions(+), 48 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:43.256Z

**tool call — Bash**
````
{
 "command": "ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ | head -5; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t197_health_local_mode_patterns.md",
 "description": "Check memory dir and the prior T-197 pattern note"
}
````

### User / tool · 2026-11-02T22:51:43.345Z

**tool result**
````
MEMORY.md
feedback_bind_to_named_reference.md
feedback_consistent_forgery_probe.md
feedback_differential_probe_prior_build.md
feedback_evidence_sha_vs_commit.md
---
name: t197-health-local-mode-patterns
description: T-197 health local_mode review r1 - HEAD moved mid-review, backend-only commit left the card's e2e AC open, api.md described unbuilt UI behaviour in the present tense
metadata:
  type: project
---

T-197 (GET /api/health reports local_mode, so the guided UI skips /api/cases and /api/library in public mode) was reviewed at 612dc2c, verdict changes (1 major, 1 minor, 1 nit).

- **Field correct, test sound.** `"local_mode": local_mode()` at app/backend/api.py:266, same function that gates the two routes. Unit test test_api_routes.py:396-403 asserts True, False and public=False; five mutants all killed. The TestClient in the `env` fixture uses a loopback peer, so the local-mode middleware (api.py:221) does not 403 the probe.
- **Card AC half missing.** The card's AC names tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server. At the reviewed sha that file was untracked and no frontend file read local_mode; step1.js:28 and home.js:118 still probe unconditionally. The working tree had the fix uncommitted.
- **Doc overstated.** memory/contracts/api.md:57 said "the guided UI reads it on first paint" in the present tense.

**Why:** the card closed its backend half and the doc claimed the frontend half. Reviewing only the commit exposes the gap; reading the card AC alone would not.

**How to apply:** when a card's AC names an e2e test, grep the test path at the reviewed sha (`git cat-file -e <sha>:<path>`) and grep the consumer (`grep -rln <field> app/frontend`) before accepting an AC as met. Check that contract-doc prose about consumers is true at the sha, not only in the working tree. Related: [[feedback_evidence_sha_vs_commit]], [[project_t175_r2_patterns]], [[project_t196_doc_claim_patterns]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:46.784Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && git status --short | head -30 && python3 tools/board.py show T-197 2>&1 | head -40",
 "description": "Confirm HEAD, working tree state, and T-197 card"
}
````

### User / tool · 2026-11-02T22:51:46.985Z

**tool result**
````
9ab8caeb27d6e7a35a533327fa38737fc6a38050
 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/backend/project_t139_charge_text.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
MM .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_multicase.md
D  .claude/agent-memory/frontend/project_t181_round2.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_e2e_contract_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
MM app/backend/api.py
MM app/backend/export.py
MM app/backend/export_routes.py
MM app/backend/flag_templates.py
---
id: "T-197"
title: "GET /api/health reports local_mode so the guided UI never probes /api/cases or /api/library in public mode (T-181 r2 first-paint 404)"
milestone: "M3"
role: "backend"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T22:40:40Z"
updated_at: "2026-11-02T22:51:29Z"
claimed_by: "backend"
claimed_at: "2026-11-02T22:40:47Z"
rounds: 1
commits: ["612dc2c"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-197-staff-engineer.md", "at": "2026-11-02T22:46:29Z"}
ac:
  - {"n": 1, "text": "health includes local_mode (bool, = local_mode()); api.md documents it; unit test; tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server passes (no xfail)", "done": true, "evidence": "tests/unit/test_api_routes.py::test_health_reports_local_mode_as_a_bool; git-archive copy: 79 passed (test_api_routes+test_case_list); tests/e2e/guided/test_round2.py -k first_paint: 2 passed, no xfail; api.md documents local_mode"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T22:40:47Z backend: claimed
- 2026-11-02T22:42:07Z backend: AC 1 checked: tests/unit/test_api_routes.py::test_health_reports_local_mode_as_a_bool; git-archive copy: 79 passed (test_api_routes+test_case_list); tests/e2e/guided/test_round2.py -k first_paint: 2 passed, no xfail; api.md documents local_mode
- 2026-11-02T22:42:08Z backend: moved in_progress -> in_review
- 2026-11-02T22:42:17Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T22:46:29Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-197-staff-engineer.md; round 1; findings:
    - [major] Card AC1 e2e half is not met at 612dc2c: the named test is untracked, no frontend reads local_mode, and public first paint still requests /library and /api/cases — fix: Land the frontend half on the same card: gate the /library call in step1.js:28 and the G.api.cases call in home.js:118 on health.local_mode !== false, and commit tests/e2e/guided/test_round2.py without an xfail marker
    - [minor] api.md states present-tense UI behaviour that is false at 612dc2c — fix: Until the frontend lands, reword line 57 to 'The guided UI will read it ...' or land the frontend change in the same commit as the doc.
- 2026-11-02T22:46:30Z orchestrator: Backend half correct. The remaining AC (first-paint e2e) lands with the T-181 r2 commit (frontend reads local_mode; test un-xfailed). Re-check after T-181 r2 commits; no backend work left.
- 2026-11-02T22:46:31Z orchestrator: moved changes_requested -> blocked: waits on the T-181 r2 commit (frontend reads local_mode, first-paint e2e committed)
- 2026-11-02T22:51:29Z backend: moved blocked -> in_progress
- 2026-11-02T22:51:29Z backend: moved in_progress -> in_review: first-paint e2e now committed in 9ab8cae (hard assertion)
- 2026-11-02T22:51:29Z orchestrator: review dispatched: staff-engineer-reviewer

## Handoff
What changed: health adds local_mode (= local_mode()); api.md example + note; unit test. How verified: git archive of the commit tree, unit api/case_list 79 passed; e2e first_paint test passes (not xfail). Left: nothing. Surprised: .venv needed for pytest.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:47.622Z

**tool call — Bash**
````
{
 "command": "cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_review_write_once.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_evidence_sha_vs_commit.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_scratchpad.md /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_playwright_render_probe.md",
 "description": "Read relevant reviewer memory feedback notes"
}
````

### User / tool · 2026-11-02T22:51:47.707Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:51.991Z

**tool call — Bash**
````
{
 "command": "ls reviews/ | grep -i T-197; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -la \"$S\" 2>&1 | head -30; echo \"---\"; git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py && echo PRESENT_AT_HEAD; git status --short tests/e2e/guided app/frontend/guided | head; echo \"--- xfail at HEAD for test file:\"; git grep -n xfail 9ab8cae -- tests/e2e/guided/test_round2.py; echo \"rc=$?\"",
 "description": "Check review file absence, scratchpad, and test file at HEAD"
}
````

### User / tool · 2026-11-02T22:51:52.413Z

**tool result**
````
T-197-staff-engineer.md
total 514848
drwx------@ 1929 arsis  wheel    61728 Nov  2 16:50 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwxr-xr-x@    7 arsis  wheel      224 Nov  2 07:36 .claude
-rw-r--r--@    1 arsis  wheel      403 Nov  2 07:36 .gitignore
drwxr-xr-x@    6 arsis  wheel      192 Nov  2 08:00 .pytest_cache
-rw-r--r--@    1 arsis  wheel      247 Nov  2 10:21 .t165dir
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
-rw-r--r--@    1 arsis  wheel     6786 Nov  2 07:36 CLAUDE.md
drwxr-xr-x@   12 arsis  wheel      384 Nov  2 14:08 GATEM3_se
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
---
PRESENT_AT_HEAD
MM app/frontend/guided/app.js
MM app/frontend/guided/core.js
MM app/frontend/guided/home.js
MM app/frontend/guided/review.css
MM app/frontend/guided/review.js
MM app/frontend/guided/step1.js
MM app/frontend/guided/step2.js
MM app/frontend/guided/step3.css
MM app/frontend/guided/step3.js
MM app/frontend/guided/step4.css
--- xfail at HEAD for test file:
rc=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:51:55.829Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -d \"$S/T197_r2_9ab8cae\" 2>/dev/null && echo EXISTS || echo FREE; mkdir -p \"$S/T197_r2_9ab8cae\" && cd /Users/arsis/zlayt-pm-project && git archive 9ab8cae | tar -x -C \"$S/T197_r2_9ab8cae\" && ls \"$S/T197_r2_9ab8cae\" | head -50 && ls -la \"$S/T197_r2_9ab8cae/.venv\" 2>&1 | head -3",
 "description": "Extract git archive of HEAD 9ab8cae into unique scratch dir"
}
````

### User / tool · 2026-11-02T22:51:57.026Z

**tool result**
````
FREE
CLAUDE.md
Dockerfile
MASTER_PROMPT.md
Makefile
README.md
app
artifacts
board
deploy
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
run.sh
spec
submission
tests
tools
ls: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae/.venv: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:00.968Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && echo \"== grep local_mode app/frontend (archive)\"; grep -rn local_mode app/frontend; echo \"rc=$?\"; echo \"== grep local_mode in api.py / tests (archive)\"; grep -rn \"local_mode\" app/backend/api.py | head; echo \"== verify archive matches HEAD for frontend guided\"; cd /Users/arsis/zlayt-pm-project && for f in app/frontend/guided/step1.js app/frontend/guided/home.js; do git show 9ab8cae:$f | diff -q - \"$S/$f\" && echo \"identical $f\"; done; echo \"== git show HEAD:step1.js line 28 and home.js\"; git show 9ab8cae:app/frontend/guided/step1.js | sed -n 20,40p; echo ---; git show 9ab8cae:app/frontend/guided/home.js | sed -n 1,20p",
 "description": "Grep archive frontend for local_mode and inspect step1/home at HEAD"
}
````

### User / tool · 2026-11-02T22:52:01.159Z

**tool result**
````
== grep local_mode app/frontend (archive)
app/frontend/guided/core.js:84:  /* The server's health, once (shared with the shell's own request). `local_mode` (T-181 r2) says whether the list of cases and the test-case library exist: when it is false the page never asks for them,
app/frontend/guided/home.js:119:    if (hl.local_mode !== false) try { return { mode: "local", views: ((await G.api.cases(signal)).cases || []).map(fromRow) }; }
app/frontend/guided/step1.js:28:    if (hl.local_mode !== false) try { lib = ((await G.api.call("GET", "/library", null, ctx.signal)).cases || []).map((x) => ({ id: x.id, name: nice(x.name) })); } catch (e) { if (e.name === "AbortError") return; lib = null; }
rc=0
== grep local_mode in api.py / tests (archive)
app/backend/api.py:83:def local_mode() -> bool:
app/backend/api.py:105:        return app.state.recorded | ({digest(x["path"].read_text()) for x in library_cases()} if local_mode() else set())
app/backend/api.py:115:    if local_mode() and os.environ.get("HOST", "127.0.0.1") not in ("127.0.0.1", "::1", "localhost"):
app/backend/api.py:221:            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
app/backend/api.py:266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
app/backend/api.py:272:        if not local_mode():                                     # public/demo stays token-only: the route does not exist (D-008)
app/backend/api.py:282:        if not local_mode():
app/backend/api.py:292:            if not local_mode():
app/backend/api.py:358:            if (full := limits.case_full(c, local_mode())):          # T-183 r2: public demo stores at most DEMO_MAX_CASES
app/backend/api.py:451:            if (busy := limits.runs_busy(len(runs), local_mode())):  # T-183 r2: public demo runs at most DEMO_MAX_RUNS at once
== verify archive matches HEAD for frontend guided
identical app/frontend/guided/step1.js
identical app/frontend/guided/home.js
== git show HEAD:step1.js line 28 and home.js
  G.longDate = longDate;

  /* ---------------------------------------------------------------- /new */
  G.pages.new = async function (ctx) {
    let hl;
    try { hl = await G.healthNow(ctx.signal); } catch (e) { if (e.name === "AbortError") return; hl = {}; }
    const demo = !!hl.demo_mode, lim = hl.limits || { max_chars: 60000, max_records: 40 }, sampleOk = hl.sample_available !== false;
    let lib = null;
    if (hl.local_mode !== false) try { lib = ((await G.api.call("GET", "/library", null, ctx.signal)).cases || []).map((x) => ({ id: x.id, name: nice(x.name) })); } catch (e) { if (e.name === "AbortError") return; lib = null; }
    if (lib && !lib.length) lib = null;
    const ONLY = () => (lib ? "This demo can only read the sample case and our test cases." : "This demo can only read the sample case.");
    const st = { how: demo ? (sampleOk ? "sample" : lib ? "library" : "sample") : "paste", text: "", file: null, lib: null, reading: false, again: null };

    /* name */
    const nameInput = h("input", { id: "case-name", type: "text", maxlength: "120", autocomplete: "off", "data-testid": "input-name", "aria-describedby": "name-hint name-error" });
    const nameErr = h("span", { class: "hint bad", id: "name-error", role: "alert", "data-testid": "name-error" });
    nameInput.addEventListener("input", () => { nameErr.textContent = ""; });

    /* tiles */
    const tiles = [
      { key: "paste", head: "Paste text", sub: "Copy the records and paste them here.", off: demo },
---
/* Your cases (/). T-181, D-068, spec section 3. Builder A.
   Local mode: GET /api/cases lists every case. Public/demo mode: that route is 404 by design, so the list is the cases THIS BROWSER started (tokens kept in localStorage by G.cases,
   try/catch), each read with GET /api/cases/{token}. One definition of the Next line and the Continue target (spec 3.2) for both sources.
   Test ids: btn-new-case, btn-sample-case, cases-list, cases-finished, cases-empty, case-card (data-token, data-title), case-next, btn-continue, btn-rename, btn-delete, btn-delete-yes, btn-delete-keep,
   rename-input, btn-rename-save, btn-rename-cancel, btn-remove-gone, find-case, cases-mode, page-error, btn-retry. Text only (textContent); no inline style attributes. */
(function () {
  const G = window.G, { h } = G;

  /* ---- the cases this browser started (public mode). Shared with step1.js. Never throws: storage can be blocked. ---- */
  const KEY = "zl.guided.cases";
  G.cases = {
    list() { try { const v = JSON.parse(localStorage.getItem(KEY) || "[]"); return Array.isArray(v) ? v.filter((t) => typeof t === "string") : []; } catch (_) { return []; } },
    add(token) { try { const l = G.cases.list().filter((t) => t !== token); l.unshift(token); localStorage.setItem(KEY, JSON.stringify(l.slice(0, 100))); } catch (_) { /* not remembered */ } },
    remove(token) { try { localStorage.setItem(KEY, JSON.stringify(G.cases.list().filter((t) => t !== token))); } catch (_) { /* not remembered */ } },
  };

  const fill = (el, ...kids) => el.replaceChildren(...kids.flat(Infinity).filter((k) => k != null && k !== false));    // replaceChildren turns null into the text "null"
  const plural = (n, one, many) => `${n} ${n === 1 ? one : many || one + "s"}`;
  const day = (iso) => { const d = new Date(iso); return isNaN(d) ? "" : d.toLocaleDateString("en-US", { month: "short", day: "numeric" }); };
  const track = ["Add records", "Timeline", "Bills", "Letter"];
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:07.044Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && grep -n \"first_paint\\|xfail\\|E2E_REQUIRE_DB\\|def test_\\|skip\" tests/e2e/guided/test_round2.py | head -80; echo \"== def body\"; n=$(grep -n \"def test_no_failed_request_on_first_paint_in_a_public_server\" tests/e2e/guided/test_round2.py | cut -d: -f1); sed -n \"$((n-12)),$((n+45))p\" tests/e2e/guided/test_round2.py",
 "description": "Inspect the named e2e test and its markers in archive"
}
````

### User / tool · 2026-11-02T22:52:07.159Z

**tool result**
````
42:def test_the_grey_box_does_not_say_a_borrowed_sentence_is_in_no_line_and_the_outside_words_are_underlined(pw, make):
62:def test_the_bates_panel_says_one_number_per_record_and_previews_before_save(pw, make):
83:def test_no_failed_request_on_first_paint_in_a_local_server(pw):
124:def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
140:def test_when_health_says_local_mode_is_false_the_page_never_asks_for_the_list_or_the_library(pw, public_server):
161:def test_a_refused_edit_names_the_words_she_dropped_in_plain_grammar(pw, make):
177:def test_plain_words_for_every_qualifier_sentence_the_server_has(pw):
194:def test_tapping_the_step_toggle_again_closes_the_list_and_stays_on_the_page(pw, make, w):
209:def test_a_disputed_line_and_its_tick_box_are_on_screen_together_at_390(pw, make):
225:def test_an_edited_line_and_its_tick_box_are_on_screen_together_at_390(pw, make):
243:def test_step3_done_fits_a_phone_and_every_change_button_is_on_screen(pw, make, w, h):
263:def test_no_guided_screen_scrolls_sideways_on_a_phone(pw, make, w, h):
286:def test_a_refused_yes_keeps_focus_off_the_answer_buttons_and_sends_nothing(pw, make):
304:def test_the_ledger_line_reason_points_to_step_3_and_reads_in_plain_words(pw, make):
316:def test_an_amount_the_second_check_disputed_says_which_way_it_disagreed(pw, make):
326:def test_a_counted_ledger_line_with_no_date_of_service_shows_the_statement_date(pw, make):
340:def test_the_title_row_does_not_say_not_written_by_an_ai_while_a_tag_says_ai_draft(pw, make):
354:def test_pressing_e_clears_the_previous_saved_message_and_its_undo(pw, make):
365:def test_every_highlight_of_a_multi_record_warning_is_in_view_at_1440(pw, make):
381:def test_step_3_keys_hint_does_not_offer_a_key_for_an_action_that_is_not_there(pw, make):
== def body
        else:
            pytest.fail("the public test server did not answer /api/health")
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        log.close()


def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
    """Home and /new in public mode: no 404 on /api/cases or /api/library. Needs `local_mode` in GET /api/health (T-197): without it the page cannot know."""
    health = __import__("json").loads(urllib.request.urlopen(public_server + "/api/health").read())
    b, page = desktop(pw)
    try:
        seen = watch(page)
        for path in ("/", "/new"):
            page.goto(public_server + path); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000); page.wait_for_timeout(300)
        assert health.get("local_mode") is False, health          # T-197: health says whether the list of cases and the library exist
        assert seen == [], seen
        page.goto(public_server + "/new"); page.locator("[data-testid=view][data-ready]").wait_for(state="attached")
        assert "test cases" not in page.get_by_test_id("demo-note").inner_text()      # nothing in a public demo offers the test cases
    finally:
        b.close()


def test_when_health_says_local_mode_is_false_the_page_never_asks_for_the_list_or_the_library(pw, public_server):
    """The frontend half of the 404 fix, proven now: the public server's health gets `local_mode: false` injected (what backend adds), and / and /new make no request that fails."""
    import json as _json
    b, page = desktop(pw)
    try:
        def health(route):
            r = route.fetch(); body = r.json(); body["local_mode"] = False
            route.fulfill(response=r, body=_json.dumps(body))
        page.route("**/api/health", health)
        seen = watch(page); asked = []
        page.on("request", lambda r: asked.append(r.url) if re.search(r"/api/(cases|library)$", r.url) and r.method == "GET" else None)
        for path in ("/", "/new"):
            page.goto(public_server + path); page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000); page.wait_for_timeout(300)
        assert seen == [] and asked == [], (seen, asked)
        assert "test cases" not in page.get_by_test_id("demo-note").inner_text()
    finally:
        b.close()


# ------------------------------------------------------------------------------------ UX major 3: the refusal names the words

def test_a_refused_edit_names_the_words_she_dropped_in_plain_grammar(pw, make):
    tok = make(); e1 = item(tok, "e1"); b, page = desktop(pw)
    try:
        open_item(page, tok, "e1")
        page.get_by_test_id("btn-third").click()
        ta = page.get_by_test_id("edit-summary"); ta.fill(e1["summary"].replace("complained of ", ""))
        page.get_by_test_id("answer-yes").click()
        foot = page.get_by_test_id("card-foot"); expect(foot).to_contain_text("Not saved.")
        t = foot.inner_text()
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:11.432Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && sed -n 1,124p tests/e2e/guided/test_round2.py",
 "description": "Read test_round2.py helpers and public_server fixture"
}
````

### User / tool · 2026-11-02T22:52:11.530Z

**tool result**
````
"""T-181 round 2 (D-068): the paralegal and UX-designer findings of round 1, each with its own guard.
Real browser, the fixture backend (curated set), the real API. Cases are made over the API and deleted afterwards.
What is guarded: the borrowed-sentence label and the underlined words (paralegal major 1); the Bates rule and its preview (paralegal major 2); no failed request on first paint, in a local and in a
PUBLIC server (T-182 r3); a refused edit names the dropped words (UX major 3); the step list closes when its toggle is tapped again (UX major 4); a disputed line and its tick box are on screen together
at 390 (UX major 2); Step 3's done lists fit a phone (UX major 1); no sideways scrolling on any guided screen at 390 and 320; a refused Yes never moves focus onto a button that answers; the second
check's direction on an amount; ledger lines with no date of service; the title-row provenance follows the case; every highlight of a multi-record warning is in view at 1440x900."""
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.request

import pytest
from playwright.sync_api import expect

import tests.e2e.conftest as C
from tests.e2e.guided._helpers import decide_all
from tests.e2e.guided.test_shell_smoke import go, watch
from tests.e2e.guided.test_step2 import LIB10, item, make, open_item, case   # noqa: F401  (make is a fixture)

LIB11 = "case_lib11_priors_and_ledger"


def no_h_scroll(page):
    return page.evaluate("document.documentElement.scrollWidth <= document.documentElement.clientWidth + 1")


def phone(pw, w=390, h=844):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, is_mobile=True, has_touch=True)
    return b, ctx.new_page()


def desktop(pw, w=1440, h=900):
    b = pw.chromium.launch(); ctx = b.new_context(viewport={"width": w, "height": h}, permissions=["clipboard-read", "clipboard-write"], accept_downloads=True)
    return b, ctx.new_page()


# ------------------------------------------------------------------------------------ paralegal major 1: the borrowed sentence

def test_the_grey_box_does_not_say_a_borrowed_sentence_is_in_no_line_and_the_outside_words_are_underlined(pw, make):
    tok = make(LIB11); b, page = desktop(pw)
    try:
        for iid, words in (("e1", {"Annual", "visit"}), ("e2", {"struck", "behind"})):
            open_item(page, tok, iid)
            box = page.get_by_test_id("uncovered")
            expect(box).to_contain_text("outside the highlighted words")
            assert "not in any line" not in box.inner_text()
            out = set(page.get_by_test_id("outside-word").all_inner_texts())
            assert words <= out, (iid, out)
            expect(page.get_by_test_id("outside-note")).to_contain_text("Underlined words are not in the highlighted words")
        # an item that is not disputed carries no underline
        open_item(page, tok, "e3")
        assert page.get_by_test_id("outside-word").count() == 0
    finally:
        b.close()


# ------------------------------------------------------------------------------------ paralegal major 2: Bates

def test_the_bates_panel_says_one_number_per_record_and_previews_before_save(pw, make):
    tok = make(); decide_all(tok); b, page = desktop(pw)
    try:
        go(page, f"/case/{tok}/letter")
        rule = page.get_by_test_id("cfg-rule").inner_text()
        assert "One Bates number per record" in rule and "not per page" in rule and "9 records" in rule, rule
        expect(page.get_by_test_id("cfg-panel")).to_contain_text("fill in the page numbers in Word")
        expect(page.get_by_test_id("cfg-preview")).to_contain_text("Nothing filled in")
        page.get_by_test_id("cfg-exhibit").fill("3"); page.get_by_test_id("cfg-bates-prefix").fill("RIVERA"); page.get_by_test_id("cfg-bates-start").fill("1")
        pv = page.get_by_test_id("cfg-preview")
        expect(pv).to_contain_text("record 1 reads [Ex. 3 / Bates RIVERA0001]")
        expect(pv).to_contain_text("record 9 reads [Ex. 3 / Bates RIVERA0009]")
        assert C.api("GET", f"/api/cases/{tok}/export_config")[1]["bates_prefix"] is None, "a preview saves nothing"
        page.get_by_test_id("cfg-bates-start").fill("100")
        expect(pv).to_contain_text("record 9 reads [Ex. 3 / Bates RIVERA0108]")
    finally:
        b.close()


# ------------------------------------------------------------------------------------ T-182 r3: no failed request on first paint

def test_no_failed_request_on_first_paint_in_a_local_server(pw):
    b, page = desktop(pw)
    try:
        seen = watch(page)
        for path in ("/", "/new"):
            go(page, path); page.wait_for_timeout(300)
        assert seen == [], seen
    finally:
        b.close()


@pytest.fixture(scope="module")
def public_server():
    """A second private server in PUBLIC mode (ZLAYT_MODE unset): GET /api/cases and /api/library answer 404 there by design."""
    s = __import__("socket").socket(); s.bind(("127.0.0.1", 0)); port = s.getsockname()[1]; s.close()
    tmp = tempfile.mkdtemp(prefix="zlayt-e2e-public-")
    env = dict(os.environ, PORT=str(port), HOST="127.0.0.1", LLM_BACKEND="fixture", FIXTURE_SET="curated", ZLAYT_DB=os.path.join(tmp, "p.sqlite3"))
    env.pop("ANTHROPIC_API_KEY", None); env.pop("ZLAYT_MODE", None)
    log = open(os.path.join(tmp, "server.log"), "w")
    proc = subprocess.Popen([sys.executable, "-m", "app.main"], cwd=C.ROOT, env=env, stdout=log, stderr=subprocess.STDOUT)
    base = f"http://127.0.0.1:{port}"
    try:
        for _ in range(80):
            try:
                urllib.request.urlopen(base + "/api/health", timeout=1).read(); break
            except Exception:
                if proc.poll() is not None:
                    pytest.fail("the public test server exited: " + open(os.path.join(tmp, "server.log")).read()[-1500:])
                time.sleep(0.5)
        else:
            pytest.fail("the public test server did not answer /api/health")
        yield base
    finally:
        proc.terminate()
        try:
            proc.wait(timeout=10)
        except Exception:
            proc.kill()
        log.close()


def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:16.037Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && grep -rn \"E2E_REQUIRE_DB\" tests/ tools/ Makefile run.sh 2>/dev/null | head -20; echo \"== watch\"; grep -n \"def watch\" -A 22 tests/e2e/guided/test_shell_smoke.py; echo \"== conftest head\"; sed -n 1,60p tests/e2e/conftest.py",
 "description": "Find E2E_REQUIRE_DB usage, watch helper, and e2e conftest"
}
````

### User / tool · 2026-11-02T22:52:16.214Z

**tool result**
````
tests/e2e/conftest.py:120:    set ZLAYT_DB to that server's file, or those specs skip with a reason). Set E2E_REQUIRE_DB=1 to make a skipped DB spec a failure (see `needs_db`)."""
tests/e2e/conftest.py:166:    """The SQLite file of the server under test, for specs that put an item into a state the fixture backend never produces. A plain run has one (pytest_configure). With E2E_REQUIRE_DB=1 a missing
tests/e2e/conftest.py:171:        if os.environ.get("E2E_REQUIRE_DB") == "1":
tests/e2e/test_ladder_gate.py:36:    with E2E_REQUIRE_DB=1 a missing file fails, it does not skip). Dismiss and reset still work on it."""
tests/e2e/test_no_console_errors.py:44:        if os.environ.get("E2E_REQUIRE_DB") == "1":
tests/e2e/test_rerun_note.py:20:        if os.environ.get("E2E_REQUIRE_DB") == "1":
tests/e2e/test_adversarial_ui.py:6:Needs ZLAYT_DB (the private server a plain run starts) to read the counters; E2E_REQUIRE_DB=1 makes a missing one a failure."""
tools/check_index_imports.py:57:                               cwd=tmp, capture_output=True, text=True, env={**env, "E2E_REQUIRE_DB": "1"})
== watch
20:def watch(page, allow_404=()):
21-    """pageerror, console.error, failed requests (an asset 404 counts) and window.onerror / unhandledrejection (a hook that runs before any page script). Returns the list to assert empty."""
22-    seen = []
23-    page.add_init_script(HOOK)
24-    page.on("pageerror", lambda e: seen.append("pageerror: " + str(e)))
25-    page.on("console", lambda m: seen.append("console." + m.type + ": " + m.text) if m.type == "error" and not any(a in m.text for a in allow_404) else None)
26-    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url for a in allow_404) else None)
27-    page.on("requestfailed", lambda r: seen.append("requestfailed: " + r.url) if "ERR_ABORTED" not in (r.failure or "") else None)      # a fetch the app aborted on purpose when she moved on is not a failure
28-    return seen
29-
30-
31-def go(page, path="/"):
32-    page.goto(C.SERVER + path)
33-    page.locator("[data-testid=view][data-ready]").wait_for(state="attached", timeout=15000)
34-
35-
36-def rect(page, sel):
37-    return page.evaluate("(s) => { const r = document.querySelector(s).getBoundingClientRect(); return [r.x, r.y, r.width, r.height].map(Math.round); }", sel)
38-
39-
40-def chrome(page):
41-    return {s: rect(page, s) for s in CHROME}
42-
== conftest head
"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
Every spec is skipped with a clear reason when the server is not up (M3 not built yet).

DATA-TESTID CONTRACT for the frontend (T-040..T-046). A unit test (tests/unit/test_e2e_contract.py) asserts every hook used by a spec is named here.
Test ids: banner-synthetic, input-text, file-input, btn-sample, btn-analyze, record-count, timeline, entry-<seq>, entry-state, entry-date, entry-provider,
  entry-summary, entry-excerpt, entry-why, why-text, btn-accept, btn-accept-verified, btn-undo-batch, btn-dismiss, btn-edit, btn-reset, btn-source, edit-summary, btn-save-edit, btn-keep-wording,
  warning-list, queue, record-modal, record-highlight, dates-to-confirm, rejected-tray, flags-panel, flag-note, charges-panel, amount-<raw>, accepted-total,
  pending-total, unclear-tray, btn-export, export-letter, export-notes, btn-copy-letter, count-line.
  T-068 (undated-entry and orphan-date branches): date-to-confirm-item (one row per undated record in dates-to-confirm, carries data-record-id), date-to-confirm-excerpt (its verbatim excerpt),
  confirm-date (one per reading, carries data-date = YYYY-MM-DD), missing-entry (a record with no entry, carries data-record-id), missing-date-confirmed (the confirmed date shown on a missing-entry row), btn-manual-entry (by-hand entry control on a missing-entry row).
  T-068 r3 (D-041, undated entries): accept-blocked-reason (visible 'Confirm the date first' beside a disabled btn-accept), link-confirm-date (button that moves focus to the entry's date choices), batch-skipped-note (batch bar: how many undated entries it skips), missing-entry-excerpt (verbatim quote kept on a missing-entry card after its date is confirmed).
Attributes (data-item-id = the item id on every entry/amount/flag row, used by the keyboard flow; and on every entry-<seq>, amount-<raw>, flag container): data-review = pending|accepted|edited|dismissed; data-state = verified|needs_review|rejected
  (also on the rows inside `queue`); data-flag-type = gap|conflict|pre_existing|causation|record_warning on flag containers (btn-source lives inside each flag).
  data-testid = the hook attribute carrying every test id above (specs select it as [data-testid="..."]); data-record-id = the record id (e.g. r8) on date-to-confirm-item and missing-entry rows; data-date = YYYY-MM-DD on confirm-date buttons.
Roles: refusals (pdf upload, empty input) render role=alert. Queue rows carry tabindex. Edit forms have NO input named date or provider (absent by design).
Keyboard (when a queue row is focused): a = accept, d = dismiss, Enter = open source record, j = next item (side-by-side stretch).
  T-081/T-082 (D-042, steppers and AI-check panel): item-stepper (in the Why panel, with data-verdict), item-verdict, item-progress, step (one per step: data-step-id, data-status = pass|fail|skipped|pending, data-kind = code|llm|human; aria-current=step on the one the human must act on),
  step-marker (glyph), step-kind (Code | AI draft | AI check | You), step-status (word), step-why, step-evidence, step-values, step-judge-reason, step-tech, step-counts, step-action ('What you need to do' line), btn-step-action (data-action-code), btn-trace (How it was checked; on flag and charge cards and tray items; data-trace-for = item id),
  case-stepper (details, collapsed by default; auto-opens when Export is clicked while the gate is blocked), case-summary (one-line summary row), case-summary-progress ('x/10 checks passed'), case-summary-need ('n need you'), case-summary-gate ('Export blocked by n' | 'Ready to export'), item-active (T-081 r2: the step that needs you, under the verdict, with btn-jump-active 'Show this step'), case-verdict, case-progress, case-step (same attributes as step; ids ingest..export_gate), gate-blockers, gate-blocker (data-jump-item = item id), btn-gate-jump, btn-to-judges,
  judge-panel (details, collapsed by default), judge-summary (one-line summary row), judge-summary-counts ('16 checked, 13 agreed with the draft, 3 questioned'), judge-row-title ('Attorney referral · Record 3'), judge-row-tech and judge-tech (closed Technical details), judge-label, judge-model-line, judge-prompts, judge-totals, judge-by-check, judge-rejections, judge-rejection, judge-unresolved-list, judge-unresolved, judge-disagreements, judge-disagreement (rows carry data-target-item, never data-item-id), btn-judge-steps, btn-judge-goto.
  T-081 r2 additions: narrative-panel and narrative-sentence (each sentence carries a btn-trace 'How this sentence was checked'); data-panel = the panel name on side-panel sections (judges, charges, flags, narrative), used to assert where a jump landed; data-open-on-jump on the collapsed judge details.
T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item stepper's skipped judge step, the message beside Export, and the AI-check panel rows and group), rerun-status (role=status sentence: running / result in plain words),
  export-blocked (section right under the Export toolbar; focused and scrolled into view when GET /export is refused 422; holds export-blocked-msg, a gate-blockers list and btn-export-blocked-close), gate-warnings and gate-warning (data-warning-code = ITEMS_NOT_REVIEWED; pending items warn, they do not block) with btn-gate-warning-jump, judge-rerun-group (group-level rerun in the AI-check panel), judge-more ('Show the other N' beyond 5 rows per group).
T-097 (r3 majors): no new test ids. rerun-status inside export-blocked must sit directly under the lead sentence beside the single btn-rerun-judge there (rows in that message only offer btn-gate-jump);
  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording follows the export gate's JUDGE_NOT_RUN blockers only
  (an edited item is 'Edited by you, not AI-checked', no rerun).
T-097 round 2 (D-045 b, T-098, D-047): judge-wording-list (AI-check panel group 'Where your wording does not match the quote') with one judge-wording row per gate code-check blocker (data-target-item) holding btn-judge-edit ('Edit your wording', opens the item's edit box),
  item-wording-fail (alert at the top of the item Why dialog: "Your wording doesn't match the quote: <reason>") with btn-wording-edit, btn-gate-edit (same action on a rail/export-message gate-blocker row for a code-check blocker). An edited item that passes shows 'Edited by you, not AI-checked' (panel row, Why verdict, judge step 'Not needed', no btn-rerun-judge).
  The 409 'keep my wording' confirm is gone (D-047, T-100): btn-keep-wording, warning-list and btn-cancel-confirm no longer exist in the UI; a refused edit is a 422 shown in the rv-error line under the edit box (specs only assert their absence).
T-097 round 3 (D-051, T-098 r2): accept-refused (role=alert box right under an item's review buttons when Accept is refused 422 CODE_CHECK_FAILED; holds accept-refused-msg = 'Not accepted. <the server's reason>' and btn-accept-refused-edit 'Edit the summary', which opens the edit box),
  batch-refused (inside batch-bar when 'Accept all verified entries' is refused: batch-refused-msg 'Nothing was accepted. <reason>', one batch-refused-item per refused item (data-refused-id) with btn-batch-refused-edit 'Edit the summary'; an item leaves the list once it is no longer pending),
  judge-case-verdict (the backend's case verdict label, verbatim, e.g. '1 summary fails a check', in the AI-check panel's 'Where a summary does not match its quote' group; the same words as case-verdict in the rail).
  The case-rail gate blocker rows carry no btn-rerun-judge any more: one POST reruns every item, so the gate step, the judges step, the refused-export message and the panel group each have ONE button whose label says 'for these N' / 'for this item'.
  T-104: when the refusal's next_action is EDIT_QUOTE the accept-refused box holds btn-accept-refused-quote 'Change the quote' instead of btn-accept-refused-edit, and each batch-refused-item holds btn-batch-refused-quote (the batch message then says 'entries', not 'summaries');
  both open the item's quote picker (excerpt-editor, excerpt-unit, btn-save-excerpt; ZL.openQuoteEditor). CODE_CHECK_FAILED returned by an EDIT renders edit-refused-msg (the server's sentence, inside the item's role=alert rv-error line under the edit box, box open, typed text kept)
  with btn-edit-refused-quote 'Change the quote' only for EDIT_QUOTE. The Why dialog's item-wording-fail lead follows the verdict string as sent ('...this summary...' -> 'This summary doesn't match the quote:', '...your wording...' -> 'Your wording doesn't match the quote:') and its btn-wording-edit
  (also btn-gate-edit, btn-judge-edit) reads 'Change the quote' for EDIT_QUOTE.
  A code-check blocker on an AI draft reads 'This summary doesn't match the quote:' with 'Edit the summary'; on wording the paralegal wrote or edited it reads 'Your wording doesn't match the quote:' with 'Edit your wording'.
T-108 (quote picker units carry no `Excerpt: \"` wrapper, quote marks or header lines): no new frontend hooks; test_change_the_quote.py also reads excerpt-error (role=alert line inside excerpt-editor, hidden unless the server refuses the quote), already rendered by excerpt.js.
T-060 r3 / T-124 (hooks the polish_r3 specs use, all already rendered by the frontend; they were missing from this contract, not dropped): sort (select in the timeline toolbar that orders entries; timeline.js),
  copy-confirm (role=alert box shown when Copy letter is pressed while items are still pending; export.js) and btn-copy-anyway ('Copy anyway'; takes focus when the confirm opens, so Enter goes through it; export.js).
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('The AI suggested this flag. The checks did not support it, so it is left out of the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
T-060 round 3 (compact rows, decided rows, shortcut sheet, export): shortcuts-list (the <dl> in shortcuts-modal: one dt/kbd + dd per key, 9 keys), entry-toggle (the row's More / Less control, aria-expanded; collapsed rows clamp the summary to 3 lines and the excerpt to 2),
  btn-start-review (primary button in todo-strip; Enter moves focus to the first item that needs a decision), checks-card (one card holding case-stepper, judge-panel and the next-action line), btn-download-letter / btn-download-notes (a .txt of the server text, verbatim).
  Wording: btn-accept on an accepted row reads 'Accepted' (edited: 'Edited', charges 'Kept in notes') with no btn--primary and stays clickable (a no-op that says so); a dismissed row's btn-dismiss reads 'Dismissed'; btn-reset reads 'Undo'; the machine-state chip 'Verified' reads 'Quote matches'.
  The calibration-line section moved below the queue (still plain, never collapsed); the batch bar (btn-accept-verified) is in the Timeline toolbar.
T-060 round 4 (+ T-114 r3): gap-change-card (a <p> inside a gap flag card: the server's sentence 'now 40 days (was 42)' plus 'Before / Now' lines with the dates; kept per case in the browser, survives Got it and a reload; a flag with a gap_change field wins) and gap-change-removed (a gap that no longer applies, under Treatment gaps),
  dismissed-group (a <details> right under the queue: dismissed entries leave the queue testid and wait here; collapsed after a reload, open for the entry just dismissed), dismissed-summary ('Dismissed (n)') and dismissed-queue (the rows inside), edit-recheck-hint (under the edit box: the code checks numbers, dates and negations, then the second AI check) and
  edit-recheck-note (kept on an edited row until the next decision: 'Saved and re-checked ...'). data-amount-kind (charge, rate, estimate, damages or unclear) is on every amount row; data-chip marks the state / review chips inside a charge row; an accepted rate / estimate / unclear amount shows only the review chip.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:22.210Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; ls /Users/arsis/zlayt-pm-project/.venv/bin/python && cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -c \"import sys; sys.path.insert(0, '.'); import app, os; print(app.__file__)\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"import playwright, pytest; print('playwright ok', pytest.__version__)\"; ls ~/Library/Caches/ms-playwright 2>&1 | head",
 "description": "Confirm venv imports archive app and Playwright is available"
}
````

### User / tool · 2026-11-02T22:52:22.458Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:26.484Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && E2E_REQUIRE_DB=1 timeout 400 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server\" -v -rs 2>&1 | tail -40",
 "description": "Run named public first-paint e2e test in archive with E2E_REQUIRE_DB=1",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T22:52:26.584Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:29.505Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server\" -v -rs 2>&1 | tail -40",
 "description": "Run named public first-paint e2e test in archive with E2E_REQUIRE_DB=1",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T22:52:32.504Z

**tool result**
````
============================= test session starts ==============================
platform darwin -- Python 3.12.2, pytest-9.2.0, pluggy-1.7.0 -- /Users/arsis/zlayt-pm-project/.venv/bin/python
rootdir: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 1 item

tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server PASSED [100%]

============================== 1 passed in 1.96s ===============================
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:42.111Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S/T197_r2_scripts\" && cat > \"$S/T197_r2_scripts/mutate_fe.py\" <<'EOF'\n# usage: mutate_fe.py <src_archive> <dst_copy> <which: none|step1|home|both>\nimport shutil, sys, pathlib\nsrc, dst, which = pathlib.Path(sys.argv[1]), pathlib.Path(sys.argv[2]), sys.argv[3]\nif dst.exists():\n    shutil.rmtree(dst)\nshutil.copytree(src, dst, ignore=shutil.ignore_patterns(\".pytest_cache\", \"__pycache__\"))\ntargets = {\"step1\": [\"app/frontend/guided/step1.js\"], \"home\": [\"app/frontend/guided/home.js\"], \"both\": [\"app/frontend/guided/step1.js\", \"app/frontend/guided/home.js\"], \"none\": []}[which]\nfor rel in targets:\n    p = dst / rel\n    s = p.read_text()\n    n = s.count(\"hl.local_mode !== false\")\n    assert n == 1, (rel, n)\n    p.write_text(s.replace(\"hl.local_mode !== false\", \"true\"))\n    print(\"mutated\", rel, \"count\", n)\nprint(\"ok\", which, dst)\nEOF\ncd \"$S\" && for w in none step1 home both; do /Users/arsis/zlayt-pm-project/.venv/bin/python -I \"$S/T197_r2_scripts/mutate_fe.py\" \"$S/T197_r2_9ab8cae\" \"$S/T197_r2_mut_$w\" $w; done",
 "description": "Create frontend-gate mutant copies of the archive in scratch"
}
````

### User / tool · 2026-11-02T22:52:45.927Z

**tool result**
````
ok none /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_mut_none
mutated app/frontend/guided/step1.js count 1
ok step1 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_mut_step1
mutated app/frontend/guided/home.js count 1
ok home /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_mut_home
mutated app/frontend/guided/step1.js count 1
mutated app/frontend/guided/home.js count 1
ok both /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_mut_both
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:52:48.920Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; for w in none step1 home both; do echo \"===== mutant: $w\"; cd \"$S/T197_r2_mut_$w\" && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server\" -q 2>&1 | grep -E \"passed|failed|AssertionError|http [0-9]+\" | head -8; done",
 "description": "Run named e2e test against each frontend-gate mutant",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T22:53:00.676Z

**tool result**
````
===== mutant: none
1 passed in 1.91s
===== mutant: step1
___________ test_no_failed_request_on_first_paint_in_a_public_server ___________
    def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
E           AssertionError: ['http 404: http://127.0.0.1:50264/api/library', 'console.error: Failed to load resource: the server responded with a status of 404 (Not Found)']
E           assert ['http 404: h... (Not Found)'] == []
E             Left contains 2 more items, first extra item: 'http 404: http://127.0.0.1:50264/api/library'
tests/e2e/guided/test_round2.py:133: AssertionError
FAILED tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server
1 failed in 1.95s
===== mutant: home
___________ test_no_failed_request_on_first_paint_in_a_public_server ___________
    def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
E           AssertionError: ['http 404: http://127.0.0.1:50329/api/cases', 'console.error: Failed to load resource: the server responded with a status of 404 (Not Found)']
E           assert ['http 404: h... (Not Found)'] == []
E             Left contains 2 more items, first extra item: 'http 404: http://127.0.0.1:50329/api/cases'
tests/e2e/guided/test_round2.py:133: AssertionError
FAILED tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server
1 failed in 1.98s
===== mutant: both
___________ test_no_failed_request_on_first_paint_in_a_public_server ___________
    def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
E           AssertionError: ['http 404: http://127.0.0.1:50367/api/cases', 'console.error: Failed to load resource: the server responded with a st....1:50367/api/library', 'console.error: Failed to load resource: the server responded with a status of 404 (Not Found)']
E           assert ['http 404: h... (Not Found)'] == []
E             Left contains 4 more items, first extra item: 'http 404: http://127.0.0.1:50367/api/cases'
tests/e2e/guided/test_round2.py:133: AssertionError
FAILED tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server
1 failed in 1.97s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:53:10.157Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && echo \"== core.js healthNow\"; grep -n \"healthNow\" -A4 app/frontend/guided/core.js | head -20; echo \"== home.js 112-124\"; sed -n 112,124p app/frontend/guided/home.js; echo \"== api.md 15-18, 48-58 at HEAD\"; sed -n '17p;50p;57p' memory/contracts/api.md; echo \"== backend health route\"; sed -n 263,267p app/backend/api.py | cut -c1-260",
 "description": "Inspect healthNow fallback, home probe, api.md and health route at HEAD"
}
````

### User / tool · 2026-11-02T22:53:10.266Z

**tool result**
````
== core.js healthNow
86:  G.healthNow = async function (signal) {
87-    if (G.store.health) return G.store.health;
88-    try { const hl = await (G.store.healthP || G.api.health(signal)); G.store.health = G.store.health || hl; return hl || {}; }
89-    catch (e) { if (e && e.name === "AbortError") throw e; return {}; }
90-  };
== home.js 112-124
      h("div", { class: "cc-meta" }, ""), h("p", { class: "next warn", "data-testid": "case-next" }, "This case is no longer here." + (hrs ? ` Cases are kept for ${hrs} hours.` : "")), h("span", {}), h("div", { class: "cc-bottom" }, rm));
  }
  const skeleton = () => h("article", { class: "ccard skeleton", "aria-hidden": "true" }, h("div", { class: "skel sk-title" }), h("div", { class: "skel sk-meta" }), h("div", { class: "skel sk-track" }), h("div", { class: "skel sk-next" }), h("div", { class: "skel sk-btn" }));

  /* ---- data: local list, or this browser's tokens ---- */
  async function load(signal) {
    const hl = await G.healthNow(signal);
    if (hl.local_mode !== false) try { return { mode: "local", views: ((await G.api.cases(signal)).cases || []).map(fromRow) }; }
    catch (e) {
      if (e.name === "AbortError") throw e;
      if (e.status !== 404) throw e;
    }
    const tokens = G.cases.list();
== api.md 15-18, 48-58 at HEAD
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
  "backend": "fixture", "demo_mode": true, "local_mode": false, "answers": "prepared", "live_enabled": false,
`local_mode` (T-197, additive): `true` only on the private local server (`ZLAYT_MODE=local`, same value that gates `GET /api/cases` and `GET /api/library`, which do not exist in public mode, D-008). The guided UI reads it on first paint and never probes those routes when it is `false`, so a public server sees no 404.
== backend health route
    @app.get("/api/health")
    def health():
        ans = answers()
        return {"ok": True, "version": VERSION, "synthetic_only": True, "banner": BANNER, "backend": backend(), "demo_mode": demo_mode(), "local_mode": local_mode(), "answers": ans,
                "live_enabled": live_enabled(), "models": models(), "limits": {"max_chars": ingest.MAX_CHARS, "max_records": ingest.MAX_RECORDS},
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:53:20.857Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T197_r2_scripts/health_fail_probe.py\" <<'EOF'\n# usage: health_fail_probe.py <archive_dir> <port>\n# Public server (ZLAYT_MODE unset). /api/health is aborted in the browser; record which list routes the page still requests.\nimport os, socket, subprocess, sys, tempfile, time, urllib.request, pathlib\nfrom playwright.sync_api import sync_playwright\narch, port = pathlib.Path(sys.argv[1]), int(sys.argv[2])\ntmp = tempfile.mkdtemp(prefix=\"zlayt-t197r2-\")\nenv = dict(os.environ, PORT=str(port), HOST=\"127.0.0.1\", LLM_BACKEND=\"fixture\", FIXTURE_SET=\"curated\", ZLAYT_DB=os.path.join(tmp, \"p.sqlite3\"))\nenv.pop(\"ANTHROPIC_API_KEY\", None); env.pop(\"ZLAYT_MODE\", None)\nlog = open(os.path.join(tmp, \"server.log\"), \"w\")\nproc = subprocess.Popen([sys.executable, \"-m\", \"app.main\"], cwd=str(arch), env=env, stdout=log, stderr=subprocess.STDOUT)\nbase = f\"http://127.0.0.1:{port}\"\ntry:\n    for _ in range(80):\n        try:\n            print(\"server health (direct):\", urllib.request.urlopen(base + \"/api/health\", timeout=1).read()[:120]); break\n        except Exception:\n            time.sleep(0.5)\n    with sync_playwright() as pw:\n        b = pw.chromium.launch(); page = b.new_context(viewport={\"width\": 1440, \"height\": 900}).new_page()\n        reqs = []\n        page.on(\"request\", lambda r: reqs.append(r.url.replace(base, \"\")) if \"/api/\" in r.url else None)\n        page.route(\"**/api/health\", lambda route: route.abort())\n        for path in (\"/\", \"/new\"):\n            reqs.clear()\n            page.goto(base + path); page.wait_for_timeout(1500)\n            print(path, \"api requests:\", reqs)\n        b.close()\nfinally:\n    proc.terminate(); proc.wait(timeout=10); log.close()\n    print(\"server log tail:\", open(os.path.join(tmp, \"server.log\")).read()[-300:])\nEOF\ncd \"$S/T197_r2_9ab8cae\" && /Users/arsis/zlayt-pm-project/.venv/bin/python \"$S/T197_r2_scripts/health_fail_probe.py\" \"$S/T197_r2_9ab8cae\" 7881 2>&1 | tail -20",
 "description": "Probe public first paint with /api/health aborted in the browser",
 "timeout": 200000
}
````

### User / tool · 2026-11-02T22:53:25.255Z

**tool result**
````
server health (direct): b'{"ok":true,"version":"0.1.0","synthetic_only":true,"banner":"Synthetic data only \xe2\x80\x94 never paste real records","backend"'
/ api requests: ['/api/health', '/api/cases']
/new api requests: ['/api/health', '/api/library']
server log tail: Serving on http://127.0.0.1:7881  (Ctrl-C to stop)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:53:33.601Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && echo \"== e2e -k first_paint or health_says\" && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/e2e/guided/test_round2.py -k \"first_paint or health_says_local_mode_is_false\" -v -rs 2>&1 | tail -8; echo \"== unit health\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q 2>&1 | tail -3; echo \"== xfail/skip markers on named test at HEAD\"; cd /Users/arsis/zlayt-pm-project && git grep -n -E \"xfail|skip\" 9ab8cae -- tests/e2e/guided/test_round2.py; echo \"rc=$?\"; git show 9ab8cae:tests/e2e/guided/test_round2.py | sed -n 121,124p",
 "description": "Run first-paint e2e subset and health unit tests in archive; check markers",
 "timeout": 420000
}
````

### User / tool · 2026-11-02T22:53:42.241Z

**tool result**
````
== e2e -k first_paint or health_says
plugins: platformdirs-4.14.3, anyio-4.16.0
collecting ... collected 23 items / 20 deselected / 3 selected

tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_local_server PASSED [ 33%]
tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server PASSED [ 66%]
tests/e2e/guided/test_round2.py::test_when_health_says_local_mode_is_false_the_page_never_asks_for_the_list_or_the_library PASSED [100%]

======================= 3 passed, 20 deselected in 3.75s =======================
== unit health
...                                                                      [100%]
3 passed, 32 deselected in 3.61s
== xfail/skip markers on named test at HEAD
rc=1
        log.close()


def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:53:49.920Z

**tool call — Bash**
````
{
 "command": "echo \"HEAD now: $(git rev-parse HEAD)\"; echo \"== commits mentioning T-197\"; git log --oneline -i --grep=T-197; echo \"== 9ab8cae subject+body T-197 mention?\"; git log -1 --format=%B 9ab8cae | grep -c \"T-197\"; echo \"== card commits field\"; python3 tools/board.py show T-197 | grep -E \"^commits|^status\"; echo \"== working tree vs HEAD for frontend guided + e2e test\"; git diff --stat 9ab8cae -- app/frontend/guided tests/e2e/guided | tail -3; echo \"== api.md 17/57 at HEAD vs worktree\"; git diff 9ab8cae -- memory/contracts/api.md | head -5; echo \"(end diff)\"",
 "description": "Recheck HEAD, T-197 commit traceability and working tree delta"
}
````

### User / tool · 2026-11-02T22:53:50.179Z

**tool result**
````
HEAD now: 9ab8caeb27d6e7a35a533327fa38737fc6a38050
== commits mentioning T-197
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
== 9ab8cae subject+body T-197 mention?
0
== card commits field
status: "in_review"
commits: ["612dc2c"]
== working tree vs HEAD for frontend guided + e2e test
 tests/e2e/guided/test_round2.py | 389 ----------------------------------------
 1 file changed, 389 deletions(-)
== api.md 17/57 at HEAD vs worktree
(end diff)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:53:53.305Z

**tool call — Bash**
````
{
 "command": "ls -la tests/e2e/guided/test_round2.py 2>&1; git status --short -- tests/e2e/guided; git log --oneline -2 -- tests/e2e/guided/test_round2.py; echo \"== api.md row 17 at HEAD\"; git show 9ab8cae:memory/contracts/api.md | sed -n 17p",
 "description": "Check working-tree status of the e2e test file and api.md row"
}
````

### User / tool · 2026-11-02T22:53:53.480Z

**tool result**
````
-rw-r--r--@ 1 arsis  staff  21200 Nov  2 16:42 tests/e2e/guided/test_round2.py
MM tests/e2e/guided/_helpers.py
D  tests/e2e/guided/test_round2.py
MM tests/e2e/guided/test_step1.py
MM tests/e2e/guided/test_step3.py
?? tests/e2e/guided/test_round2.py
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
== api.md row 17 at HEAD
| GET | `/api/health` | backend, demo mode, models, limits, banner text |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T22:54:06.701Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider tests/unit -q 2>&1 | tail -4; echo \"== port 7881 listeners\"; lsof -nP -iTCP:7881 -sTCP:LISTEN 2>&1 | head -3; echo \"(end)\"",
 "description": "Run unit suite in archive and confirm probe server exited",
 "timeout": 400000
}
````

### User / tool · 2026-11-02T23:00:32.108Z

**tool result**
````
........................................................................ [ 98%]
........................................................................ [ 99%]
...................................                                      [100%]
5856 passed, 11 skipped in 383.60s (0:06:23)
== port 7881 listeners
(end)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:00:44.018Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; cd \"$S\" && grep -n \"local_mode\" app/frontend/guided/home.js app/frontend/guided/step1.js app/frontend/guided/core.js | cut -c1-120; grep -n \"healthNow = \\|return {};\\|async function load\" app/frontend/guided/core.js app/frontend/guided/home.js; echo \"--- tests\"; grep -n \"def public_server\\|def test_no_failed_request_on_first_paint_in_a_public_server\\|assert health.get\\|assert seen == \\[\\], seen\\|def test_no_failed_request_on_first_paint_in_a_local\" tests/e2e/guided/test_round2.py; grep -n \"def watch\\|r.status >= 400\" tests/e2e/guided/test_shell_smoke.py | cut -c1-120; echo \"--- api\"; grep -n '\"local_mode\": local_mode()' app/backend/api.py | cut -c1-80; grep -n \"local_mode\" memory/contracts/api.md | cut -c1-60; echo \"--- board state\"; cd /Users/arsis/zlayt-pm-project && git grep -n \"local_mode\" 9ab8cae -- app/frontend | cut -c1-80",
 "description": "Get exact line numbers for every citation before writing the review"
}
````

### User / tool · 2026-11-02T23:00:44.187Z

**tool result**
````
app/frontend/guided/home.js:119:    if (hl.local_mode !== false) try { return { mode: "local", views: ((await G.api.case
app/frontend/guided/core.js:84:  /* The server's health, once (shared with the shell's own request). `local_mode` (T-181
app/frontend/guided/step1.js:28:    if (hl.local_mode !== false) try { lib = ((await G.api.call("GET", "/library", null,
app/frontend/guided/home.js:117:  async function load(signal) {
app/frontend/guided/core.js:86:  G.healthNow = async function (signal) {
app/frontend/guided/core.js:89:    catch (e) { if (e && e.name === "AbortError") throw e; return {}; }
--- tests
83:def test_no_failed_request_on_first_paint_in_a_local_server(pw):
89:        assert seen == [], seen
95:def public_server():
124:def test_no_failed_request_on_first_paint_in_a_public_server(pw, public_server):
132:        assert health.get("local_mode") is False, health          # T-197: health says whether the list of cases and the library exist
133:        assert seen == [], seen
20:def watch(page, allow_404=()):
26:    page.on("response", lambda r: seen.append(f"http {r.status}: {r.url}") if r.status >= 400 and not any(a in r.url 
--- api
266:        return {"ok": True, "version": VERSION, "synthetic_only": True, "ban
50:  "backend": "fixture", "demo_mode": true, "local_mode": 
57:`local_mode` (T-197, additive): `true` only on the privat
--- board state
9ab8cae:app/frontend/guided/core.js:84:  /* The server's health, once (shared wi
9ab8cae:app/frontend/guided/home.js:119:    if (hl.local_mode !== false) try { r
9ab8cae:app/frontend/guided/step1.js:28:    if (hl.local_mode !== false) try { l
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:01:20.530Z

**tool call — Bash**
````
{
 "command": "echo \"== backend/unit/contract diff 612dc2c..9ab8cae (empty = unchanged):\"; git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md; echo \"(end)\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T197_r2_9ab8cae; grep -n \"e.status !== 404\\|const tokens = G.cases.list\" \"$S/app/frontend/guided/home.js\"; grep -n \"lib = null\" \"$S/app/frontend/guided/step1.js\" | cut -c1-40; grep -n \"local_mode\" \"$S/app/frontend/guided/core.js\" | cut -c1-20; echo \"HEAD at end: $(git rev-parse HEAD)\"; ls /Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer-r2.md 2>&1",
 "description": "Confirm backend unchanged since r1 and pin home.js fallthrough lines"
}
````

### User / tool · 2026-11-02T23:01:20.695Z

**tool result (error)**
````
Exit code 1
== backend/unit/contract diff 612dc2c..9ab8cae (empty = unchanged):
(end)
122:      if (e.status !== 404) throw e;
124:    const tokens = G.cases.list();
27:    let lib = null;
28:    if (hl.local_mode !== false) try 
29:    if (lib && !lib.length) lib = nul
84:  /* The server's
HEAD at end: e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
ls: /Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer-r2.md: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:01:24.760Z

**tool call — Bash**
````
{
 "command": "git log --oneline -4 && echo \"== files changed 9ab8cae..HEAD\" && git diff --stat 9ab8cae HEAD | tail -15 && echo \"== does HEAD touch guided frontend, the e2e test, api.py, api.md?\" && git diff --name-only 9ab8cae HEAD -- app/frontend tests/e2e app/backend memory/contracts; echo \"(end)\"; git show --format='%H %s' -s e425534 | cut -c1-200",
 "description": "Inspect the new HEAD commit and whether it touches reviewed files"
}
````

### User / tool · 2026-11-02T23:01:24.909Z

**tool result**
````
e425534 fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/hand-entry pass and static twin-completeness test
9ab8cae fix(frontend): T-181 r2 guided UI: borrowed-sentence label and underlined outside words, Bates rule and preview, no first-paint 404 via health.local_mode, refused edit names dropped words, phone fixes (step toggle, disputed line with tick box, Step 3 cards), classic tooltip per D-065
f5f1be9 feat(qa): T-198 prompt log redacts the outside project name by default (one switch, REDACT_OUTSIDE_PROJECT_NAME); README edit 7
612dc2c feat(backend): GET /api/health reports local_mode (T-197)
== files changed 9ab8cae..HEAD
 app/backend/review.py                |   9 +--
 app/backend/why.py                   |   1 +
 tests/unit/test_prepared_property.py | 104 +++++++++++++++++++++++++++++++++--
 3 files changed, 104 insertions(+), 10 deletions(-)
== does HEAD touch guided frontend, the e2e test, api.py, api.md?
app/backend/review.py
app/backend/why.py
(end)
e425534ec1af6f2bb1dadbc6c59353a13af6b5ca fix(backend): T-177 r5 edit/hand-entry second-check warning follows provenance; INJECTION_SUSPECTED twin; property test adds unsupported fault, edit/accept/han
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:01:30.312Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -d \"$S/T197_r2_e425534\" 2>/dev/null && echo EXISTS || { mkdir -p \"$S/T197_r2_e425534\" && cd /Users/arsis/zlayt-pm-project && git archive e425534 | tar -x -C \"$S/T197_r2_e425534\" && cd \"$S/T197_r2_e425534\" && E2E_REQUIRE_DB=1 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py\" -k \"first_paint or health_says_local_mode_is_false\" -v 2>&1 | tail -6; }; cd /Users/arsis/zlayt-pm-project && echo \"HEAD at end: $(git rev-parse HEAD)\"",
 "description": "Archive new HEAD e425534 and rerun first-paint e2e subset",
 "timeout": 300000
}
````

### User / tool · 2026-11-02T23:01:36.120Z

**tool result**
````
tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_local_server PASSED [ 33%]
tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server PASSED [ 66%]
tests/e2e/guided/test_round2.py::test_when_health_says_local_mode_is_false_the_page_never_asks_for_the_list_or_the_library PASSED [100%]

======================= 3 passed, 20 deselected in 3.68s =======================
HEAD at end: e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:13.567Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; cat > \"$S/T197_r2_scripts/draft_r2.md\" <<'EOF'\n# T-197 r2 review (staff-engineer): guided UI reads health.local_mode\n\n**Verdict: pass** (0 blockers, 0 majors, 3 minors, 1 nit).\n\n**Reviewed sha: 9ab8cae**, the commit the brief names. HEAD was 9ab8cae at my first `git rev-parse HEAD` and moved to e425534 during the review (`fix(backend): T-177 r5 ...`). e425534 changes only `app/backend/review.py`, `app/backend/why.py` and `tests/unit/test_prepared_property.py`, so every finding below holds at both. I re-ran the first-paint tests at e425534 as well. The working tree is dirty and was not reviewed, except for the index state named in finding 2. Model recorded is claude-haiku-5-5, the model I ran as; the dossier expected claude-sonnet-5-5.\n\n## Brief checks\n1. **The guided frontend reads `health.local_mode`: met.** `grep -rn local_mode app/frontend` in the 9ab8cae archive prints `core.js:84` (a comment), `home.js:119` and `step1.js:28`. Both reads are `hl.local_mode !== false`, on the object returned by `G.healthNow` (core.js:86).\n2. **The named test is committed, has no xfail, and passes with E2E_REQUIRE_DB=1: met.** `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py` succeeds. `git grep -n -E \"xfail|skip\" 9ab8cae -- tests/e2e/guided/test_round2.py` prints nothing (exit 1). In the archive, `E2E_REQUIRE_DB=1 ... -k \"first_paint or health_says_local_mode_is_false\"` gives 3 passed.\n\n## Does the named test catch a regression?\nYes. I made scratch copies of the archive with each gate forced to `true` (exact-count replacement, count 1 each). Each mutant was run against the named test:\n- control (unmutated): 1 passed.\n- step1.js:28 forced: 1 failed, with `http 404: .../api/library` in the seen list.\n- home.js:119 forced: 1 failed, with `http 404: .../api/cases`.\n- both forced: 1 failed, with four entries.\n\n## r1 findings at 9ab8cae\n- major, card AC1 e2e half not met: **closed.** The test is committed and passes, and both frontend reads exist.\n- minor, api.md:57 stated present-tense UI behaviour that was false: **closed.** Both readers now exist, so the sentence is true at 9ab8cae.\n- nit, api.md:17 row omits local_mode: **open**, see finding 4.\n\n## Findings\n\n**minor 1: when `/api/health` fails, the page still probes the two routes it should not.**\n- Evidence: `core.js:89` is `catch (e) { if (e && e.name === \"AbortError\") throw e; return {}; }`. With `{}`, `hl.local_mode` is undefined, so `!== false` is true and the page takes the probe branch (`home.js:119`, `step1.js:28`). Repro: in the 9ab8cae archive, a public server (ZLAYT_MODE unset) with `**/api/health` aborted in the browser. `.venv/bin/python <scratch>/T197_r2_scripts/health_fail_probe.py <archive> 7881` printed `/ api requests: ['/api/health', '/api/cases']` and `/new api requests: ['/api/health', '/api/library']`. The named test does not run this path (`test_round2.py:124-133` needs a reachable health).\n- Why it matters: the card title says the guided UI never probes these routes in public mode. When the mode is unknown the page guesses local, and the error from health is turned into a default (checklist item 12: errors should reach an explicit status). The probes are caught (`home.js:122` falls through to this browser's tokens on 404; `step1.js:28` sets `lib = null`), so no wrong data appears and nothing is exposed. The cost is two 404s on first paint, the failure the card names, with no test guarding this cause. I rate it minor because the AC's literal scope is the health field, not a failed health call. If Chris reads the AC as covering a failed health call, it becomes major.\n- Fix: choose the unknown-mode behaviour explicitly. Either (a) probe only on `hl.local_mode === true`, and show a plain \"could not reach the server\" state when health fails, or (b) keep probing and write that as the accepted degraded path in `memory/contracts/api.md`. Either way, add the test below.\n- Acceptance test: in a public server fixture, abort `**/api/health`, load `/` and `/new`, and assert no request matching `/api/(cases|library)$` (the regex the test at `test_round2.py:140` uses). Under option (a), also assert the visible state.\n\n**minor 2: the index has the named test staged for deletion, and an untracked copy in the working tree.**\n- Evidence: `git status --short -- tests/e2e/guided` prints `D  tests/e2e/guided/test_round2.py` and `?? tests/e2e/guided/test_round2.py`, with `MM` on `_helpers.py`, `test_step1.py` and `test_step3.py`. The file is committed at 9ab8cae, so the committed state is right.\n- Why it matters: CLAUDE.md requires a pathspec commit because the index is shared. A plain `git commit` by anyone would commit the staged deletion and remove the AC's named test. This does not change the verdict, which is about the commit.\n- Fix: the owner unstages the deletion (`git restore --staged tests/e2e/guided/test_round2.py`) and commits by pathspec. I did not run this.\n- Acceptance test: `git diff --cached --name-only | grep -c test_round2` prints 0, and `git status --short -- tests/e2e/guided/test_round2.py` has no `D` in the first column.\n\n**minor 3: the card's closing commit is not on the card.**\n- Evidence: `python3 tools/board.py show T-197` shows `status: \"in_review\"` and `commits: [\"612dc2c\"]`. `git log --oneline -i --grep=T-197` lists only `612dc2c feat(backend): GET /api/health reports local_mode (T-197)`. `git log -1 --format=%B 9ab8cae | grep -c T-197` prints 0. The subject of 9ab8cae is `fix(frontend): T-181 r2 guided UI: ... no first-paint 404 via health.local_mode ...`.\n- Why it matters: AC1's e2e half is evidenced by 9ab8cae, but the board does not list that commit and the subject does not cite T-197. A reader who searches by card finds only the backend commit.\n- Fix: record 9ab8cae against T-197 on the board (through the backend worker or the orchestrator, using `board.py`), and cite T-197 in the next commit that touches this area.\n- Acceptance test: `python3 tools/board.py show T-197` lists `9ab8cae` in `commits`.\n\n**nit 4: `memory/contracts/api.md:17` still omits local_mode.**\n- Evidence: `git show 9ab8cae:memory/contracts/api.md | sed -n 17p` prints `| GET | \\`/api/health\\` | backend, demo mode, models, limits, banner text |`. The full shape at `:50` and the prose at `:57` are correct.\n- Fix: add \"local mode flag\" to the row.\n- Acceptance test: `git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode` prints 1.\n\n## Exercised\n- `python3 tools/board.py show T-197`: `in_review`, commits `[\"612dc2c\"]`.\n- `git rev-parse HEAD`: 9ab8cae at the first call; e425534 at the last call.\n- `git archive 9ab8cae | tar -x` into a unique scratch directory. The archive has no `.venv`, so I used the project `.venv/bin/python`. `python -I -c` with `sys.path.insert(0, '.')` confirmed that `import app` resolves to the archive.\n- `grep -rn local_mode app/frontend` in the archive: core.js:84, home.js:119, step1.js:28. `diff -q` of the archive's `step1.js` and `home.js` against `git show 9ab8cae:...`: identical.\n- `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py`: present. `git grep -n -E \"xfail|skip\" 9ab8cae -- tests/e2e/guided/test_round2.py`: no output.\n- Archive: `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server\" -v -rs`: 1 passed in 1.96s.\n- Archive: `E2E_REQUIRE_DB=1 ... -k \"first_paint or health_says_local_mode_is_false\" -v`: 3 passed (local first paint, public first paint, health false).\n- Mutant copies of the archive (`mutate_fe.py`, run with `-I`): none, step1, home, both, as in the section above.\n- `health_fail_probe.py` (aborted `/api/health`, public server on port 7881): output quoted in finding 1. The server was stopped; `lsof -nP -iTCP:7881 -sTCP:LISTEN` is empty afterwards.\n- Archive at 9ab8cae: `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q`: 3 passed. `tests/unit -q`: 5856 passed, 11 skipped in 383.60s.\n- `git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md`: empty, so the backend and the unit tests are unchanged since r1.\n- Archive at e425534 (`git archive e425534`): the same 3-test `-k` subset with `E2E_REQUIRE_DB=1`: 3 passed.\n- `git status --short -- tests/e2e/guided`: the index state quoted in finding 2.\n- Read `app/frontend/guided/home.js:117-124`, `step1.js:27-29`, `core.js:86-90`, `tests/e2e/guided/test_round2.py:83-137`, `tests/e2e/guided/test_shell_smoke.py:20-26` (watch), `app/backend/api.py:266`, `memory/contracts/api.md:17, 50, 57`.\n\n**Not exercised:** the dirty working tree; a live server on :7860; the full `test_round2.py` file (only the named test and the 3-test subset); a browser first paint on the local server beyond that subset.\n\n## What is right\n- The frontend reads are gated on the server's field, and removing either gate fails the named test with the exact 404 URL (see above). The test catches the regression.\n- The named test has no xfail or skip at 9ab8cae. It asserts the server precondition `health.get(\"local_mode\") is False` (`test_round2.py:132`) before the first-paint check, so it cannot pass on a server that dropped the field.\n- r1's minor is closed: api.md:57 is true at 9ab8cae because the frontend reads the field.\n\n## Questions for Chris\n- When `/api/health` fails, should the guided UI keep probing (today) or show an explicit \"could not reach the server\" state? Finding 1 needs that choice.\n\n```json\n{\"card\": \"T-197\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Commit 9ab8cae (fix(frontend) T-181 r2, carries the T-197 frontend half): app/frontend/guided/{core,home,step1}.js, tests/e2e/guided/test_round2.py, memory/contracts/api.md; app/backend/api.py unchanged since 612dc2c. HEAD moved 9ab8cae -> e425534 during the review (e425534 touches app/backend/review.py, why.py, tests/unit/test_prepared_property.py only); the named test was re-run at e425534. No app URL on :7860; sample case not run (outside the AC). Working tree dirty, not reviewed except the index state in finding 2.\",\n \"exercised\": [\n  \"python3 tools/board.py show T-197 -> status in_review, commits [\\\"612dc2c\\\"]\",\n  \"git rev-parse HEAD -> 9ab8cae at first call, e425534 at last call; git log --oneline -4\",\n  \"git archive 9ab8cae | tar -x into a unique scratch dir; project .venv/bin/python -I -c confirms import app resolves to the archive\",\n  \"grep -rn local_mode app/frontend (archive) -> core.js:84, home.js:119, step1.js:28; diff -q of step1.js and home.js against git show 9ab8cae -> identical\",\n  \"git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py -> present; git grep -n -E 'xfail|skip' 9ab8cae -- tests/e2e/guided/test_round2.py -> no output\",\n  \"archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server -v -rs -> 1 passed in 1.96s\",\n  \"archive: E2E_REQUIRE_DB=1 ... -k 'first_paint or health_says_local_mode_is_false' -v -> 3 passed\",\n  \"mutants (scratch copies via mutate_fe.py under python -I, count-asserted): control 1 passed; step1 gate forced 1 failed (http 404 /api/library); home gate forced 1 failed (http 404 /api/cases); both forced 1 failed\",\n  \"health_fail_probe.py under the venv on the archive, port 7881, /api/health aborted in the browser: / requests ['/api/health','/api/cases']; /new requests ['/api/health','/api/library']; server stopped, port empty afterwards\",\n  \"archive: .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q -> 3 passed; tests/unit -q -> 5856 passed, 11 skipped in 383.60s\",\n  \"git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md -> empty\",\n  \"archive at e425534: E2E_REQUIRE_DB=1 -k 'first_paint or health_says_local_mode_is_false' -> 3 passed\",\n  \"git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'\",\n  \"git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0\",\n  \"git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> row without local_mode\",\n  \"read app/frontend/guided/home.js:117-124, step1.js:27-29, core.js:86-90, tests/e2e/guided/test_round2.py:83-137, tests/e2e/guided/test_shell_smoke.py:20-26, app/backend/api.py:266, memory/contracts/api.md:17,50,57\",\n  \"not exercised: dirty working tree; live server on :7860; full test_round2.py file; browser first paint on the local server beyond the 3-test subset\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"ac1_named_e2e_committed_and_passing\": 5, \"frontend_reads_local_mode\": 5, \"test_catches_removed_gate\": 5, \"failure_visible_when_health_fails\": 2, \"index_and_board_hygiene\": 3, \"api_md_documents_field\": 4, \"unit_suite_green\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"When /api/health fails, the guided UI still probes /api/cases and /api/library\",\n   \"evidence\": \"app/frontend/guided/core.js:89 'catch (e) { if (e && e.name === \\\"AbortError\\\") throw e; return {}; }'; home.js:119 and step1.js:28 'if (hl.local_mode !== false)'. Repro: public server, /api/health aborted in browser; health_fail_probe.py printed \\\"/ api requests: ['/api/health', '/api/cases']\\\" and \\\"/new api requests: ['/api/health', '/api/library']\\\".\",\n   \"why_it_matters\": \"Fail-open default: with an unknown mode the page guesses local and probes the routes the card says it never probes in public mode. The 404s are caught (home.js:122, step1.js:28), so no wrong data or exposure. Cost is two visible 404s on first paint and no test for this cause. Checklist item 12 expects an explicit status, not a default. Minor because the AC covers the health field, not a failed health call; major if Chris reads the AC that way.\",\n   \"fix\": \"Choose explicitly: (a) probe only when hl.local_mode === true and show a plain 'could not reach the server' state on failure, or (b) keep probing and record that as the accepted degraded path in memory/contracts/api.md. Add the test either way.\",\n   \"acceptance_test\": \"Public server fixture with **/api/health aborted: load / and /new; assert no request matching /api/(cases|library)$; under option (a) assert the visible state.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Index has tests/e2e/guided/test_round2.py staged for deletion, with an untracked copy in the worktree\",\n   \"evidence\": \"git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'. The file is committed at 9ab8cae (git cat-file -e succeeds).\",\n   \"why_it_matters\": \"CLAUDE.md requires pathspec commits because the index is shared. A plain git commit would commit the staged deletion and remove the AC's named test. The committed state is correct, so the verdict does not change.\",\n   \"fix\": \"The owner runs git restore --staged tests/e2e/guided/test_round2.py and commits by pathspec. Not run by this reviewer.\",\n   \"acceptance_test\": \"git diff --cached --name-only | grep -c test_round2 prints 0; git status --short -- tests/e2e/guided/test_round2.py shows no D in the first column.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The closing commit 9ab8cae is not recorded on T-197\",\n   \"evidence\": \"python3 tools/board.py show T-197 -> status in_review, commits [\\\"612dc2c\\\"]; git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0.\",\n   \"why_it_matters\": \"AC1's e2e half is evidenced by 9ab8cae, which the board does not list and whose subject (T-181 r2) does not cite T-197. A search by card finds only the backend commit.\",\n   \"fix\": \"Record 9ab8cae against T-197 on the board through the backend worker or the orchestrator, using board.py. Cite T-197 in the next commit in this area.\",\n   \"acceptance_test\": \"python3 tools/board.py show T-197 lists 9ab8cae under commits.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"memory/contracts/api.md:17 health row still omits local_mode\",\n   \"evidence\": \"git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> '| GET | `/api/health` | backend, demo mode, models, limits, banner text |'. The full shape at :50 and prose at :57 are correct.\",\n   \"why_it_matters\": \"Discoverability in the summary table only. Carried from r1 and not yet fixed.\",\n   \"fix\": \"Add 'local mode flag' to the row.\",\n   \"acceptance_test\": \"git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode prints 1.\"}\n ],\n \"whats_right\": [\n  \"Both frontend reads are gated on the server's local_mode field (home.js:119, step1.js:28), and removing either gate fails the named test with the exact 404 URL, so the test catches the regression.\",\n  \"The named test has no xfail or skip at 9ab8cae and asserts health.get('local_mode') is False (test_round2.py:132) before the first-paint check, so it cannot pass on a server that dropped the field.\",\n  \"The r1 minor is closed: api.md:57 is true at 9ab8cae because the frontend now reads the field.\"\n ],\n \"questions_for_chris\": [\"When /api/health fails, should the guided UI keep probing (today) or show an explicit 'could not reach the server' state? Finding 1 needs that choice.\"]}\n```\nEOF\npython3 - \"$S/T197_r2_scripts/draft_r2.md\" <<'EOF'\nimport json, sys, re\ntxt = open(sys.argv[1], encoding=\"utf-8\").read()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", txt, re.S)\nfences = txt.count(\"```json\")\nprint(\"json fences:\", fences, \"blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"keys ok:\", all(k in d for k in [\"card\",\"persona\",\"model\",\"scope\",\"exercised\",\"verdict\",\"scores\",\"findings\",\"whats_right\",\"questions_for_chris\"]))\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nblockers = sev.count(\"blocker\"); majors = sev.count(\"major\")\nexpect = \"fail\" if blockers else (\"changes\" if majors else \"pass\")\nprint(\"sev\", sev, \"verdict\", d[\"verdict\"], \"rule says\", expect, \"OK\" if expect == d[\"verdict\"] else \"MISMATCH\")\nprint(\"whats_right count\", len(d[\"whats_right\"]), \"model\", d[\"model\"])\nEOF",
 "description": "Draft the review in scratch and validate its JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T23:02:13.680Z

**tool result**
````
json fences: 1 blocks: 1
keys ok: True
sev ['minor', 'minor', 'minor', 'nit'] verdict pass rule says pass OK
whats_right count 3 model claude-haiku-5-5
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:38.606Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer-r2.md",
 "content": "# T-197 r2 review (staff-engineer): guided UI reads health.local_mode\n\n**Verdict: pass** (0 blockers, 0 majors, 3 minors, 1 nit).\n\n**Reviewed sha: 9ab8cae**, the commit the brief names. HEAD was 9ab8cae at my first `git rev-parse HEAD` and moved to e425534 during the review (`fix(backend): T-177 r5 ...`). e425534 changes only `app/backend/review.py`, `app/backend/why.py` and `tests/unit/test_prepared_property.py`, so every finding below holds at both. I re-ran the first-paint tests at e425534 as well. The working tree is dirty and was not reviewed, except for the index state named in finding 2. Model recorded is claude-haiku-5-5, the model I ran as; the dossier expected claude-sonnet-5-5.\n\n## Brief checks\n1. **The guided frontend reads `health.local_mode`: met.** `grep -rn local_mode app/frontend` in the 9ab8cae archive prints `core.js:84` (a comment), `home.js:119` and `step1.js:28`. Both reads are `hl.local_mode !== false`, on the object returned by `G.healthNow` (core.js:86).\n2. **The named test is committed, has no xfail, and passes with E2E_REQUIRE_DB=1: met.** `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py` succeeds. `git grep -n -E \"xfail|skip\" 9ab8cae -- tests/e2e/guided/test_round2.py` prints nothing (exit 1). In the archive, `E2E_REQUIRE_DB=1 ... -k \"first_paint or health_says_local_mode_is_false\"` gives 3 passed.\n\n## Does the named test catch a regression?\nYes. I made scratch copies of the archive with each gate forced to `true` (exact-count replacement, count 1 each). Each mutant was run against the named test:\n- control (unmutated): 1 passed.\n- step1.js:28 forced: 1 failed, with `http 404: .../api/library` in the seen list.\n- home.js:119 forced: 1 failed, with `http 404: .../api/cases`.\n- both forced: 1 failed, with four entries.\n\n## r1 findings at 9ab8cae\n- major, card AC1 e2e half not met: **closed.** The test is committed and passes, and both frontend reads exist.\n- minor, api.md:57 stated present-tense UI behaviour that was false: **closed.** Both readers now exist, so the sentence is true at 9ab8cae.\n- nit, api.md:17 row omits local_mode: **open**, see finding 4.\n\n## Findings\n\n**minor 1: when `/api/health` fails, the page still probes the two routes it should not.**\n- Evidence: `core.js:89` is `catch (e) { if (e && e.name === \"AbortError\") throw e; return {}; }`. With `{}`, `hl.local_mode` is undefined, so `!== false` is true and the page takes the probe branch (`home.js:119`, `step1.js:28`). Repro: in the 9ab8cae archive, a public server (ZLAYT_MODE unset) with `**/api/health` aborted in the browser. `.venv/bin/python <scratch>/T197_r2_scripts/health_fail_probe.py <archive> 7881` printed `/ api requests: ['/api/health', '/api/cases']` and `/new api requests: ['/api/health', '/api/library']`. The named test does not run this path (`test_round2.py:124-133` needs a reachable health).\n- Why it matters: the card title says the guided UI never probes these routes in public mode. When the mode is unknown the page guesses local, and the error from health is turned into a default (checklist item 12: errors should reach an explicit status). The probes are caught (`home.js:122-124` falls through to this browser's tokens on 404; `step1.js:28` sets `lib = null`), so no wrong data appears and nothing is exposed. The cost is two 404s on first paint, the failure the card names, with no test guarding this cause. I rate it minor because the AC's literal scope is the health field, not a failed health call. If Chris reads the AC as covering a failed health call, it becomes major.\n- Fix: choose the unknown-mode behaviour explicitly. Either (a) probe only on `hl.local_mode === true`, and show a plain \"could not reach the server\" state when health fails, or (b) keep probing and write that as the accepted degraded path in `memory/contracts/api.md`. Either way, add the test below.\n- Acceptance test: in a public server fixture, abort `**/api/health`, load `/` and `/new`, and assert no request matching `/api/(cases|library)$` (the regex the test at `test_round2.py:140` uses). Under option (a), also assert the visible state.\n\n**minor 2: the index has the named test staged for deletion, and an untracked copy in the working tree.**\n- Evidence: `git status --short -- tests/e2e/guided` prints `D  tests/e2e/guided/test_round2.py` and `?? tests/e2e/guided/test_round2.py`, with `MM` on `_helpers.py`, `test_step1.py` and `test_step3.py`. The file is committed at 9ab8cae, so the committed state is right.\n- Why it matters: CLAUDE.md requires a pathspec commit because the index is shared. A plain `git commit` by anyone would commit the staged deletion and remove the AC's named test. This does not change the verdict, which is about the commit.\n- Fix: the owner unstages the deletion (`git restore --staged tests/e2e/guided/test_round2.py`) and commits by pathspec. I did not run this.\n- Acceptance test: `git diff --cached --name-only | grep -c test_round2` prints 0, and `git status --short -- tests/e2e/guided/test_round2.py` has no `D` in the first column.\n\n**minor 3: the card's closing commit is not on the card.**\n- Evidence: `python3 tools/board.py show T-197` shows `status: \"in_review\"` and `commits: [\"612dc2c\"]`. `git log --oneline -i --grep=T-197` lists only `612dc2c feat(backend): GET /api/health reports local_mode (T-197)`. `git log -1 --format=%B 9ab8cae | grep -c T-197` prints 0. The subject of 9ab8cae is `fix(frontend): T-181 r2 guided UI: ... no first-paint 404 via health.local_mode ...`.\n- Why it matters: AC1's e2e half is evidenced by 9ab8cae, but the board does not list that commit and the subject does not cite T-197. A reader who searches by card finds only the backend commit.\n- Fix: record 9ab8cae against T-197 on the board (through the backend worker or the orchestrator, using `board.py`), and cite T-197 in the next commit that touches this area.\n- Acceptance test: `python3 tools/board.py show T-197` lists `9ab8cae` in `commits`.\n\n**nit 4: `memory/contracts/api.md:17` still omits local_mode.**\n- Evidence: `git show 9ab8cae:memory/contracts/api.md | sed -n 17p` prints `| GET | \\`/api/health\\` | backend, demo mode, models, limits, banner text |`. The full shape at `:50` and the prose at `:57` are correct.\n- Fix: add \"local mode flag\" to the row.\n- Acceptance test: `git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode` prints 1.\n\n## Exercised\n- `python3 tools/board.py show T-197`: `in_review`, commits `[\"612dc2c\"]`.\n- `git rev-parse HEAD`: 9ab8cae at the first call; e425534 at the last call.\n- `git archive 9ab8cae | tar -x` into a unique scratch directory. The archive has no `.venv`, so I used the project `.venv/bin/python`. `python -I -c` with `sys.path.insert(0, '.')` confirmed that `import app` resolves to the archive.\n- `grep -rn local_mode app/frontend` in the archive: core.js:84, home.js:119, step1.js:28. `diff -q` of the archive's `step1.js` and `home.js` against `git show 9ab8cae:...`: identical.\n- `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py`: present. `git grep -n -E \"xfail|skip\" 9ab8cae -- tests/e2e/guided/test_round2.py`: no output.\n- Archive: `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider \"tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server\" -v -rs`: 1 passed in 1.96s.\n- Archive: `E2E_REQUIRE_DB=1 ... -k \"first_paint or health_says_local_mode_is_false\" -v`: 3 passed (local first paint, public first paint, health false).\n- Mutant copies of the archive (`mutate_fe.py`, run with `-I`): none, step1, home, both, as in the section above.\n- `health_fail_probe.py` (aborted `/api/health`, public server on port 7881): output quoted in finding 1. The server was stopped; `lsof -nP -iTCP:7881 -sTCP:LISTEN` is empty afterwards.\n- Archive at 9ab8cae: `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q`: 3 passed. `tests/unit -q`: 5856 passed, 11 skipped in 383.60s.\n- `git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md`: empty, so the backend and the unit tests are unchanged since r1.\n- Archive at e425534 (`git archive e425534`): the same 3-test `-k` subset with `E2E_REQUIRE_DB=1`: 3 passed.\n- `git status --short -- tests/e2e/guided`: the index state quoted in finding 2.\n- Read `app/frontend/guided/home.js:117-124`, `step1.js:27-29`, `core.js:86-90`, `tests/e2e/guided/test_round2.py:83-137`, `tests/e2e/guided/test_shell_smoke.py:20-26` (watch), `app/backend/api.py:266`, `memory/contracts/api.md:17, 50, 57`.\n\n**Not exercised:** the dirty working tree; a live server on :7860; the full `test_round2.py` file (only the named test and the 3-test subset); a browser first paint on the local server beyond that subset.\n\n## What is right\n- The frontend reads are gated on the server's field, and removing either gate fails the named test with the exact 404 URL (see above). The test catches the regression.\n- The named test has no xfail or skip at 9ab8cae. It asserts the server precondition `health.get(\"local_mode\") is False` (`test_round2.py:132`) before the first-paint check, so it cannot pass on a server that dropped the field.\n- r1's minor is closed: api.md:57 is true at 9ab8cae because the frontend reads the field.\n\n## Questions for Chris\n- When `/api/health` fails, should the guided UI keep probing (today) or show an explicit \"could not reach the server\" state? Finding 1 needs that choice.\n\n```json\n{\"card\": \"T-197\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"Commit 9ab8cae (fix(frontend) T-181 r2, carries the T-197 frontend half): app/frontend/guided/{core,home,step1}.js, tests/e2e/guided/test_round2.py, memory/contracts/api.md; app/backend/api.py unchanged since 612dc2c. HEAD moved 9ab8cae -> e425534 during the review (e425534 touches app/backend/review.py, why.py, tests/unit/test_prepared_property.py only); the named test was re-run at e425534. No app URL on :7860; sample case not run (outside the AC). Working tree dirty, not reviewed except the index state in finding 2.\",\n \"exercised\": [\n  \"python3 tools/board.py show T-197 -> status in_review, commits [\\\"612dc2c\\\"]\",\n  \"git rev-parse HEAD -> 9ab8cae at first call, e425534 at last call; git log --oneline -4\",\n  \"git archive 9ab8cae | tar -x into a unique scratch dir; project .venv/bin/python -I -c confirms import app resolves to the archive\",\n  \"grep -rn local_mode app/frontend (archive) -> core.js:84, home.js:119, step1.js:28; diff -q of step1.js and home.js against git show 9ab8cae -> identical\",\n  \"git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py -> present; git grep -n -E 'xfail|skip' 9ab8cae -- tests/e2e/guided/test_round2.py -> no output\",\n  \"archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server -v -rs -> 1 passed in 1.96s\",\n  \"archive: E2E_REQUIRE_DB=1 ... -k 'first_paint or health_says_local_mode_is_false' -v -> 3 passed\",\n  \"mutants (scratch copies via mutate_fe.py under python -I, count-asserted): control 1 passed; step1 gate forced 1 failed (http 404 /api/library); home gate forced 1 failed (http 404 /api/cases); both forced 1 failed\",\n  \"health_fail_probe.py under the venv on the archive, port 7881, /api/health aborted in the browser: / requests ['/api/health','/api/cases']; /new requests ['/api/health','/api/library']; server stopped, port empty afterwards\",\n  \"archive: .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q -> 3 passed; tests/unit -q -> 5856 passed, 11 skipped in 383.60s\",\n  \"git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md -> empty\",\n  \"archive at e425534: E2E_REQUIRE_DB=1 -k 'first_paint or health_says_local_mode_is_false' -> 3 passed\",\n  \"git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'\",\n  \"git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0\",\n  \"git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> row without local_mode\",\n  \"read app/frontend/guided/home.js:117-124, step1.js:27-29, core.js:86-90, tests/e2e/guided/test_round2.py:83-137, tests/e2e/guided/test_shell_smoke.py:20-26, app/backend/api.py:266, memory/contracts/api.md:17,50,57\",\n  \"not exercised: dirty working tree; live server on :7860; full test_round2.py file; browser first paint on the local server beyond the 3-test subset\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"ac1_named_e2e_committed_and_passing\": 5, \"frontend_reads_local_mode\": 5, \"test_catches_removed_gate\": 5, \"failure_visible_when_health_fails\": 2, \"index_and_board_hygiene\": 3, \"api_md_documents_field\": 4, \"unit_suite_green\": 5},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"When /api/health fails, the guided UI still probes /api/cases and /api/library\",\n   \"evidence\": \"app/frontend/guided/core.js:89 'catch (e) { if (e && e.name === \\\"AbortError\\\") throw e; return {}; }'; home.js:119 and step1.js:28 'if (hl.local_mode !== false)'. Repro: public server, /api/health aborted in browser; health_fail_probe.py printed \\\"/ api requests: ['/api/health', '/api/cases']\\\" and \\\"/new api requests: ['/api/health', '/api/library']\\\".\",\n   \"why_it_matters\": \"Fail-open default: with an unknown mode the page guesses local and probes the routes the card says it never probes in public mode. The 404s are caught (home.js:122-124, step1.js:28), so no wrong data or exposure. Cost is two visible 404s on first paint and no test for this cause. Checklist item 12 expects an explicit status, not a default. Minor because the AC covers the health field, not a failed health call; major if Chris reads the AC that way.\",\n   \"fix\": \"Choose explicitly: (a) probe only when hl.local_mode === true and show a plain 'could not reach the server' state on failure, or (b) keep probing and record that as the accepted degraded path in memory/contracts/api.md. Add the test either way.\",\n   \"acceptance_test\": \"Public server fixture with **/api/health aborted: load / and /new; assert no request matching /api/(cases|library)$; under option (a) assert the visible state.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Index has tests/e2e/guided/test_round2.py staged for deletion, with an untracked copy in the worktree\",\n   \"evidence\": \"git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'. The file is committed at 9ab8cae (git cat-file -e succeeds).\",\n   \"why_it_matters\": \"CLAUDE.md requires pathspec commits because the index is shared. A plain git commit would commit the staged deletion and remove the AC's named test. The committed state is correct, so the verdict does not change.\",\n   \"fix\": \"The owner runs git restore --staged tests/e2e/guided/test_round2.py and commits by pathspec. Not run by this reviewer.\",\n   \"acceptance_test\": \"git diff --cached --name-only | grep -c test_round2 prints 0; git status --short -- tests/e2e/guided/test_round2.py shows no D in the first column.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"The closing commit 9ab8cae is not recorded on T-197\",\n   \"evidence\": \"python3 tools/board.py show T-197 -> status in_review, commits [\\\"612dc2c\\\"]; git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0.\",\n   \"why_it_matters\": \"AC1's e2e half is evidenced by 9ab8cae, which the board does not list and whose subject (T-181 r2) does not cite T-197. A search by card finds only the backend commit.\",\n   \"fix\": \"Record 9ab8cae against T-197 on the board through the backend worker or the orchestrator, using board.py. Cite T-197 in the next commit in this area.\",\n   \"acceptance_test\": \"python3 tools/board.py show T-197 lists 9ab8cae under commits.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"memory/contracts/api.md:17 health row still omits local_mode\",\n   \"evidence\": \"git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> '| GET | `/api/health` | backend, demo mode, models, limits, banner text |'. The full shape at :50 and prose at :57 are correct.\",\n   \"why_it_matters\": \"Discoverability in the summary table only. Carried from r1 and not yet fixed.\",\n   \"fix\": \"Add 'local mode flag' to the row.\",\n   \"acceptance_test\": \"git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode prints 1.\"}\n ],\n \"whats_right\": [\n  \"Both frontend reads are gated on the server's local_mode field (home.js:119, step1.js:28), and removing either gate fails the named test with the exact 404 URL, so the test catches the regression.\",\n  \"The named test has no xfail or skip at 9ab8cae and asserts health.get('local_mode') is False (test_round2.py:132) before the first-paint check, so it cannot pass on a server that dropped the field.\",\n  \"The r1 minor is closed: api.md:57 is true at 9ab8cae because the frontend now reads the field.\"\n ],\n \"questions_for_chris\": [\"When /api/health fails, should the guided UI keep probing (today) or show an explicit 'could not reach the server' state? Finding 1 needs that choice.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T23:02:38.787Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:41.253Z

**tool call — Bash**
````
{
 "command": "python3 -I - reviews/T-197-staff-engineer-r2.md <<'EOF'\nimport json, sys, re\ntxt = open(sys.argv[1], encoding=\"utf-8\").read()\nprint(\"json fences:\", txt.count(\"```json\"), \"blocks:\", len(re.findall(r\"```json\\n(.*?)\\n```\", txt, re.S)))\nd = json.loads(re.findall(r\"```json\\n(.*?)\\n```\", txt, re.S)[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nexp = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"verdict\", d[\"verdict\"], \"rule\", exp, \"OK\" if exp == d[\"verdict\"] else \"MISMATCH\", \"model\", d[\"model\"], \"whats_right\", len(d[\"whats_right\"]))\nEOF\necho \"HEAD at end: $(git rev-parse HEAD)\"",
 "description": "Validate the written review's JSON block and verdict rule"
}
````

### User / tool · 2026-11-02T23:02:41.398Z

**tool result**
````
json fences: 1 blocks: 1
verdict pass rule pass OK model claude-haiku-5-5 whats_right 3
HEAD at end: e425534ec1af6f2bb1dadbc6c59353a13af6b5ca
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:45.264Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t197_health_local_mode_patterns.md"
}
````

### User / tool · 2026-11-02T23:02:45.272Z

**tool result**
````
1	---
2	name: t197-health-local-mode-patterns
3	description: T-197 health local_mode review r1 - HEAD moved mid-review, backend-only commit left the card's e2e AC open, api.md described unbuilt UI behaviour in the present tense
4	metadata:
5	  type: project
6	---
7	
8	T-197 (GET /api/health reports local_mode, so the guided UI skips /api/cases and /api/library in public mode) was reviewed at 612dc2c, verdict changes (1 major, 1 minor, 1 nit).
9	
10	- **Field correct, test sound.** `"local_mode": local_mode()` at app/backend/api.py:266, same function that gates the two routes. Unit test test_api_routes.py:396-403 asserts True, False and public=False; five mutants all killed. The TestClient in the `env` fixture uses a loopback peer, so the local-mode middleware (api.py:221) does not 403 the probe.
11	- **Card AC half missing.** The card's AC names tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server. At the reviewed sha that file was untracked and no frontend file read local_mode; step1.js:28 and home.js:118 still probe unconditionally. The working tree had the fix uncommitted.
12	- **Doc overstated.** memory/contracts/api.md:57 said "the guided UI reads it on first paint" in the present tense.
13	
14	**Why:** the card closed its backend half and the doc claimed the frontend half. Reviewing only the commit exposes the gap; reading the card AC alone would not.
15	
16	**How to apply:** when a card's AC names an e2e test, grep the test path at the reviewed sha (`git cat-file -e <sha>:<path>`) and grep the consumer (`grep -rln <field> app/frontend`) before accepting an AC as met. Check that contract-doc prose about consumers is true at the sha, not only in the working tree. Related: [[feedback_evidence_sha_vs_commit]], [[project_t175_r2_patterns]], [[project_t196_doc_claim_patterns]].
17	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:45.469Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T23:02:45.494Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014/T-028: doc/REQ drift, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031: partial re-fixes, regex guard blind spots, scratch-copy mutation
4	- [LLM-stage review patterns](project_llm_stage_review_patterns.md) — T-048: verify no-op, skipif on untracked fixtures, pin HEAD by sha
5	- [Wiring review patterns](project_wiring_review_patterns.md) — T-030: green unit tests, no production caller; grep callers
6	- [Backend LLM review patterns](project_backend_llm_review_patterns.md) — T-035/T-033: untested wiring, label-window bleed
7	- [E2E contract review patterns](project_e2e_contract_review_patterns.md) — T-039/T-124: hook contract vs specs, stub-server E2E
8	- [T-050 namespacing patterns](project_t050_namespacing_review_patterns.md) — T-050: producer fix, delete-on-upgrade loss, pin by archive
9	- [Eval runner review patterns](project_eval_runner_review_patterns.md) — T-038: fake hides real keys, git-archive pinning
10	- [Split LLM review patterns](project_split_llm_review_patterns.md) — T-057: stale-on-failed-rerun, orphan probe needs control
11	- [Round-2 snapshot review patterns](project_round2_snapshot_review_patterns.md) — T-040/T-043: HEAD moves, archive needs fixtures, overwrite hazard
12	- [T-063 doc-vs-code patterns](project_t063_doc_vs_code_review_patterns.md) — "code only" docs that call models, stale "no card", HEAD moves
13	- [Severity vs brief](feedback_severity_vs_brief.md) — rate per CONTRACT D.2 when a brief's default severity conflicts
14	- [T-065 fallback-removal patterns](project_t065_batch_fallback_review_patterns.md) — mock fan-out, undo test, mock contract drift
15	- [T-066 NO_MODEL patterns](project_t066_no_model_reason_patterns.md) — elif reason wider than its message; assert reason absence
16	- [R2 fix-verification patterns](project_r2_fix_verification_patterns.md) — T-058/T-055/T-059: fix in another card's commit, overstated counts
17	- [T-070/T-067 patterns](project_t070_t067_review_patterns.md) — exact-string guard vs strip, normalizer+consumer mutation, persona mismatch
18	- [T-080 trace API patterns](project_t080_trace_review_patterns.md) — judge-never-ran summaries, gate vs export agreement, 422 vs 409
19	- [Review write-once](feedback_review_write_once.md) — reviews/*.md is append-only under the guard; proof-read before first Write
20	- [T-067 r6 D-043 patterns](project_t067_r6_d043_patterns.md) — later decision supersedes old clause, allow-list comment drift
21	- [T-075 determinism patterns](project_t075_determinism_review_patterns.md) — signature narrower than R-CO-7, vacuous order test
22	- [T-093 signature and controls patterns](project_t093_signature_controls_patterns.md) — H3V5 label vs judge rule 1, reachability mutants
23	- [T-083 billing patterns](project_t083_billing_review_patterns.md) — r1-r3: bare figures vanish, second balance-forward overwrites
24	- [T-083 r4 accounting patterns](project_t083_r4_accounting_patterns.md) — r4: repeated totals overwritten while counted as placed
25	- [T-090 calibration patterns](project_t090_calibration_review_patterns.md) — r1-r3: git-less copy skips provenance, unowned route
26	- [T-088/T-089 suggestion patterns](project_t088_t089_review_patterns.md) — reason scope, AC done with UI unbuilt, conjunction gaps
27	- [T-095 HEAD-revert patterns](project_t095_head_revert_patterns.md) — r1 HEAD revert fail; r2 partial restore, later-card hunks
28	- [T-073/T-084 patterns](project_t073_t084_review_patterns.md) — seam-only proof, restore bypass, redundant gate arms
29	- [T-100 D-047 patterns](project_t100_d047_review_patterns.md) — one-way qualifier check, gate reads stored reasons only
30	- [T-098/T-099 patterns](project_t098_t099_review_patterns.md) — AI-draft invented number accepted, state-sum untested
31	- [T-083 r5 cross-family patterns](project_t083_r5_cross_family_patterns.md) — ledger and CMS totals share a slot, bare charge dropped
32	- [T-101 calibration guard patterns](project_t101_calibration_guard_patterns.md) — guard tested for golden only, run-then-write
33	- [T-098 r2 patterns](project_t098_r2_review_patterns.md) — summary-only edit bypasses accept guard, gate recomputes 2 of 5
34	- [T-103 listing patterns](project_t103_listing_review_patterns.md) — UB-04 room total vs other_figures, offset comparisons
35	- [Exact count vs presence](feedback_exact_count_vs_presence.md) — presence oracles miss a dropped second copy
36	- [T-100 r2 patterns](project_t100_r2_patterns.md) — shared new_tokens, vocabulary narrower than lists, unpinned Spanish branches
37	- [T-098 r3 patterns](project_t098_r3_review_patterns.md) — choke point by grep+probe; removed narrative text still printed
38	- [T-106 patterns](project_t106_review_patterns.md) — pdf_hidden regex bypass via from-subprocess-import, loose fixture filter
39	- [T-108 quote-units patterns](project_t108_quote_units_patterns.md) — masked route checks, sentences_reason unrendered, broad except
40	- [Shared scratchpad](feedback_shared_scratchpad.md) — unique card-round subdirs, diff -rq archive checks, no backgrounded chains
41	- [T-109 doc-vs-code patterns](project_t109_doc_vs_code_patterns.md) — cite range off by blank lines, scan a-side keys
42	- [T-106 r2 audit patterns](project_t106_r2_audit_patterns.md) — AST audit misses os alias/ctypes/asyncio, ps argv unpinned
43	- [T-102 stale-calibration patterns](project_t102_stale_calibration_patterns.md) — stale fix verified via clone, wrong-dir literal pin
44	- [T-115 e2e/curated patterns](project_t115_e2e_curated_patterns.md) — evidence cites older commit, regen re-keys prompts, inner_text race
45	- [T-112 trim patterns](project_t112_trim_patterns.md) — stems then abbreviations over-trim, unpinned counter
46	- [T-119 keyboard coverage patterns](project_t119_keyboard_coverage_patterns.md) — vis() first-frame poll, count artifact without sha
47	- [Verify PID before kill](feedback_verify_pid_before_kill.md) — $! can be a wrapper; check ps and lsof before killing
48	- [T-120/T-121/T-105 patterns](project_t120_t121_t105_patterns.md) — negative-proxy guard, one-direction single-source refactor
49	- [T-128/T-129/T-127 patterns](project_t128_t129_t127_patterns.md) — closed-list fragment guard, preamble flag never served
50	- [T-120 r3 patterns](project_t120_r3_patterns.md) — strip-then-scan, honorific collision, unpinned gate mutant
51	- [T-128/T-129 r2 patterns](project_t128_t129_r2_patterns.md) — structural rule leaves tail clauses, relative sweep path
52	- [T-133 lexicon patterns](project_t133_lexicon_review_patterns.md) — bare 'History:' over-flag, attribution deny untested
53	- [T-113/T-122 patterns](project_t113_t122_patterns.md) — held-out control naming its noun, closed-list word mutants
54	- [T-132 r2 / T-128 r3 patterns](project_t132_t128_r2r3_patterns.md) — wrap inside chained clause, prefix-oracle fuzz
55	- [T-133 r3 patterns](project_t133_r3_patterns.md) — header guard dropped history flags, ';' suppression recall gap
56	- [T-133 r4 patterns](project_t133_r4_patterns.md) — \s matches newline: line-start bare History: flags
57	- [T-133 r5 patterns](project_t133_r5_patterns.md) — CR-only kills \s, eval grep must read header line
58	- [Regex multiline probe](feedback_regex_multiline_probe.md) — probe \s and line-break variants of "line start" guards
59	- [Differential probe vs prior build](feedback_differential_probe_prior_build.md) — run probes on pre-fix and HEAD archives
60	- [T-134 unconfirmed-edit patterns](project_t134_unconfirmed_edit_patterns.md) — judge counts open edit, N3/N5 mutants survive
61	- [GATE-M2 patterns](project_gate_m2_patterns.md) — deadline skips judge_entries, timed-out rerun deletes pending
62	- [T-113 r2 patterns](project_t113_r2_patterns.md) — git-derived audit with throwaway repos, unpinned count mutants
63	- [T-132 r4 patterns](project_t132_r4_patterns.md) — 'Label:' regex drops condition lines, subdir archive exports empty
64	- [T-132 r5 patterns](project_t132_r5_patterns.md) — closed-list stop drops ALL-CAPS lines, control-first probe expectations
65	- [T-134 r3 / T-138 patterns](project_t134_r3_t138_patterns.md) — text fix missed review step, snapshot aliases mutated dict
66	- [T-145/T-146 patterns](project_t145_t146_patterns.md) — shared JUDGE_NOT_RUN mislabels, failed re-run wipes accepted
67	- [T-141 r2 patterns](project_t141_r2_patterns.md) — word list loses conflicts, stored run summary stale after confirm
68	- [T-134 r4 / T-138 r2 patterns](project_t134_r4_t138_r2_patterns.md) — backend wording fixed but UI regex keeps old sentence
69	- [Frontend text coupling](feedback_frontend_text_coupling.md) — grep app/frontend for old phrase when a backend sentence changes
70	- [T-136 r2 patterns](project_t136_r2_patterns.md) — private-server fallback to :7860, red e2e predating the card
71	- [T-146 r2 patterns](project_t146_r2_patterns.md) — keep-whole rule keyed on judge/stub only, SUMMARY_NOT_IN_QUOTE overwrites
72	- [T-140 r2 patterns](project_t140_r2_patterns.md) — tests read untracked reviewer file, after-figure position gap
73	- [T-141 r3 patterns](project_t141_r3_patterns.md) — negator/history windows hide collisions, 31/31 mutants killed
74	- [T-141 r4 patterns](project_t141_r4_patterns.md) — month-year cut-off hides 'Rear-ended in October 2025'
75	- [T-152 golden-claim patterns](project_t152_golden_claim_patterns.md) — untracked ledger breaks collection, golden-named test
76	- [T-146 r3 patterns](project_t146_r3_patterns.md) — equal-rank check replaces decided item silently, rerun_note unused
77	- [T-146 r4 patterns](project_t146_r4_patterns.md) — identical re-run rewrites decided rows, dead 'conflicts' key
78	- [Fake script keys](feedback_fake_script_keys.md) — FakeCall returns {} for unknown keys; run a wrong-key control
79	- [T-141 r5 patterns](project_t141_r5_patterns.md) — verb-only mechanism gate, noun forms stay in-window, gate mutant pinned
80	- [T-155 e2e triage patterns](project_t155_e2e_triage_patterns.md) — green on older sha, hidden list 0 px, refusal box offset
81	- [Evidence sha vs commit](feedback_evidence_sha_vs_commit.md) — run cited test at evidence sha and reviewed commit
82	- [T-157 title/next_action patterns](project_t157_case_title_next_action_patterns.md) — edit-class survivor, identity-only demo test
83	- [T-140 r3 / T-152 r2 patterns](project_t140_r3_t152_r2_patterns.md) — per-line not per-figure default-deny, undated promote unflagged
84	- [T-141 r6 patterns](project_t141_r6_patterns.md) — closed exemption leaks across and/or/with, bare hit/impact missing
85	- [T-141 r7 patterns](project_t141_r7_patterns.md) — two-digit-year dates escape the guard, conftest SyntaxError looks red
86	- [T-141 r8 patterns](project_t141_r8_patterns.md) — HEAD moved past card, sentence-scope residual, 10-pin mutant
87	- [T-162 rerun-note patterns](project_t162_rerun_note_patterns.md) — dead-panel throws now red, swallow in wrapper passes
88	- [Swallow needs render marker](feedback_swallow_needs_render_marker.md) — assert a render marker for every panel
89	- [Watcher blind to render errors](feedback_watcher_blind_to_render_errors.md) — pageerror watchers empty when a render hook throws
90	- [T-159/T-161 r2 patterns](project_t159_t161_r2_patterns.md) — compensation fails under double fault, undated-boundary mutant
91	- [T-158 settle patterns](project_t158_settle_patterns.md) — r3: one-shot scroll passes same probe, sha-less AC still red at 0b2ce9c
92	- [T-160 budget/placement patterns](project_t160_budget_placement_patterns.md) — sample-only budget test, "never own line" false at 320 px
93	- [T-155 r2 / T-164 patterns](project_t155_r2_t164_patterns.md) — totals match but skip sets differ, [hidden] !important no-op
94	- [T-167 plain-wording patterns](project_t167_plain_wording_patterns.md) — AC universal grep overclaimed, fallback doubles phrase
95	- [Reviewer scratch writes](feedback_reviewer_scratch_writes.md) — Write blocked in scratchpad; evidence under artifacts/review-evidence
96	- [T-165 r2 patterns](project_t165_r2_patterns.md) — hand entry kept with rerun_note, e2e red out of scope
97	- [T-168 parser patterns](project_t168_parser_patterns.md) — closing-object parser is global, truncated sub-object accepted
98	- [GATE-M2 r2 patterns](project_gate_m2_r2_patterns.md) — suite red across fixture guards, run suite in a git clone
99	- [T-169 r2 binding patterns](project_t169_r2_binding_patterns.md) — newest-by-name run link picks decoy, r1 F4 missing
100	- [Bind to named reference](feedback_bind_to_named_reference.md) — binding test must read the reference the artifact names
101	- [T-173 seed-fidelity patterns](project_t173_seed_fidelity_patterns.md) — r1/r2: seeded row raw-equal to placeholder; browser attempt rule unguarded (M6 3/3)
102	- [Guard blocks shell expansions](feedback_guard_blocks_shell_expansions.md) — git-guard refuses ${var%%}; board-guard refuses 2>; use python -I script
103	- [T-175 r2 patterns](project_t175_r2_patterns.md) — 9/9 backend mutants red, UI renders null progress as "None"
104	- [Playwright render probe](feedback_playwright_render_probe.md) — render the real list from an archive; screenshot beats inner_text
105	- [GATE-M3 / T-045 patterns](project_gate_m3_t045_patterns.md) — is_mobile scroll check vacuous, "unit-covered" claim false, no-op mutants
106	- [T-045 r2 record-latest patterns](project_t045_r2_record_latest_patterns.md) — header value copied not recomputed; flipped fixture report records ship bar True
107	- [Mutant apply verify](feedback_mutant_apply_verify.md) — BSD sed 0,/re/ no-ops silently; grep the mutant; restore via git show HEAD
108	- [T-177 provenance patterns](project_t177_provenance_patterns.md) — r1: payload model names; r2: flag items "AI found it", FAIL branches say "AI drafted", missing-key PASS
109	- [Playwright route hold](feedback_playwright_route_hold.md) — blocking sleep in a route handler freezes the page; park the route, release from the loop
110	- [T-045 r3 record-latest patterns](project_t045_r3_record_latest_patterns.md) — header flips refused; consistent body+header forgery records live (minor); parser coverage gaps
111	- [Consistent forgery probe](feedback_consistent_forgery_probe.md) — recompute-from-document checks: probe header+body+pointer together, not only header flips
112	- [T-179 D-066/D-067 patterns](project_t179_d066_d067_patterns.md) — conditional-branch test never runs, regex misses heading, stamp outside txn
113	- [T-177 r3 patterns](project_t177_r3_patterns.md) — closed swap table leaks on failure paths; schema-invalid row flips case models; F-D untested
114	- [T-196 doc-claim patterns](project_t196_doc_claim_patterns.md) — take-back map lacks accepted; append-only file kept a wrong cite range
115	- [T-197 local_mode patterns](project_t197_health_local_mode_patterns.md) — HEAD moved mid-review, e2e AC untracked, api.md claims unbuilt UI
116	- [T-177 r4 patterns](project_t177_r4_patterns.md) — property guard misses ungrounded/edit/accept faults; twin-or-AI fallback; shape exemptions
117	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:49.749Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t197_health_local_mode_patterns.md",
 "old_string": "**How to apply:** when a card's AC names an e2e test, grep the test path at the reviewed sha (`git cat-file -e <sha>:<path>`) and grep the consumer (`grep -rln <field> app/frontend`) before accepting an AC as met. Check that contract-doc prose about consumers is true at the sha, not only in the working tree. Related: [[feedback_evidence_sha_vs_commit]], [[project_t175_r2_patterns]], [[project_t196_doc_claim_patterns]].",
 "new_string": "**How to apply:** when a card's AC names an e2e test, grep the test path at the reviewed sha (`git cat-file -e <sha>:<path>`) and grep the consumer (`grep -rln <field> app/frontend`) before accepting an AC as met. Check that contract-doc prose about consumers is true at the sha, not only in the working tree. Related: [[feedback_evidence_sha_vs_commit]], [[project_t175_r2_patterns]], [[project_t196_doc_claim_patterns]].\n\n**r2 (9ab8cae, verdict pass; file reviews/T-197-staff-engineer-r2.md):** r1 major closed. The frontend reads `hl.local_mode !== false` at home.js:119 and step1.js:28, and the named e2e test is committed with no xfail and passes under E2E_REQUIRE_DB=1. Forcing either gate to `true` in an archive copy fails the test with the 404 URL.\n- New minor: `G.healthNow` returns `{}` when /api/health fails (core.js:89), so the page takes the probe branch. Probed with the route aborted: `/` requests /api/cases and `/new` requests /api/library. See [[feedback_fail_open_unknown_flag]].\n- New minor: `git status` showed `D ` (staged) for tests/e2e/guided/test_round2.py plus `??` in the worktree. The committed file is fine; a plain commit would drop the AC test. See [[feedback_shared_index_staged_deletes]].\n- New minor: the board lists only 612dc2c for T-197. 9ab8cae (T-181 r2 subject) carries the e2e half with no T-197 cite.\n- HEAD moved 9ab8cae -> e425534 mid-review (backend-only change). I re-ran the subset at e425534 and it passed."
}
````

### User / tool · 2026-11-02T23:02:49.859Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_t197_health_local_mode_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:54.254Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_fail_open_unknown_flag.md",
 "content": "---\nname: feedback_fail_open_unknown_flag\ndescription: a feature gate written as `flag !== false` takes the permissive branch when the flag fetch fails (helper returns {}); probe the gate with the flag request aborted, not only with the flag present\nmetadata:\n  type: feedback\n---\n\nWhen a frontend gate reads a server flag, check what the helper returns on failure. In T-197 r2 `G.healthNow` returned `{}` on any non-abort error (app/frontend/guided/core.js:89), so `hl.local_mode !== false` was true and the page probed the routes the flag exists to hide (`/api/cases`, `/api/library` in public mode). Both 404s were caught, so the failure was quiet, not wrong.\n\n**Why:** the e2e test only covered the healthy path (flag present, `false`). A reviewer who checks \"does the test pass\" misses the branch the flag is supposed to protect.\n\n**How to apply:** for any `flag !== false` or `flag === undefined` default, write the probe: in an archive copy, abort the flag request (`page.route(\"**/api/health\", lambda r: r.abort())`), load the pages, and list the `/api/` requests. Report the default as a finding, and propose the explicit state or the safer default with a test. Related: [[project_t197_health_local_mode_patterns]], [[feedback_playwright_render_probe]].\n"
}
````

### User / tool · 2026-11-02T23:02:54.395Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_fail_open_unknown_flag.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:56.624Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_index_staged_deletes.md",
 "content": "---\nname: feedback_shared_index_staged_deletes\ndescription: a review's committed-sha check can pass while the shared index stages a deletion of the same test; check `git status --short -- <test path>` for D in column one, and report it as a hazard\nmetadata:\n  type: feedback\n---\n\nAt T-197 r2, `git cat-file -e <sha>:tests/e2e/guided/test_round2.py` succeeded, but `git status --short -- tests/e2e/guided` showed `D  tests/e2e/guided/test_round2.py` (staged) with `??` on the same path in the worktree. The committed state was right. A plain `git commit` by any agent would have committed the deletion and removed the AC's named test.\n\n**Why:** the index is shared (CLAUDE.md requires pathspec commits for this reason). A reviewer who only reads the sha misses that the next commit can undo it.\n\n**How to apply:** when a card's AC names a test file, run `git status --short -- <path>` as well as `git cat-file -e <sha>:<path>`. Report a staged `D` as a minor hazard, and say the verdict is about the committed sha. Suggest `git restore --staged <path>` for the owner and a pathspec commit. Do not run the restore yourself. Related: [[project_t197_health_local_mode_patterns]], [[feedback_evidence_sha_vs_commit]].\n"
}
````

### User / tool · 2026-11-02T23:02:56.728Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/feedback_shared_index_staged_deletes.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:02:59.922Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [T-197 local_mode patterns](project_t197_health_local_mode_patterns.md) — HEAD moved mid-review, e2e AC untracked, api.md claims unbuilt UI\n- [T-177 r4 patterns](project_t177_r4_patterns.md) — property guard misses ungrounded/edit/accept faults; twin-or-AI fallback; shape exemptions",
 "new_string": "- [T-197 local_mode patterns](project_t197_health_local_mode_patterns.md) — r1 e2e AC untracked; r2 pass: health-fail probe, staged deletion, board sha\n- [T-177 r4 patterns](project_t177_r4_patterns.md) — property guard misses ungrounded/edit/accept faults; twin-or-AI fallback; shape exemptions\n- [Fail-open unknown flag](feedback_fail_open_unknown_flag.md) — `flag !== false` takes the permissive branch when the flag fetch fails\n- [Shared index staged deletes](feedback_shared_index_staged_deletes.md) — sha check passes while index stages a D on the AC test; run git status too"
}
````

### User / tool · 2026-11-02T23:03:00.048Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T23:03:01.926Z

T-197 r2 at 9ab8cae: pass (0 blockers, 0 majors, 3 minors, 1 nit). Review: /Users/arsis/zlayt-pm-project/reviews/T-197-staff-engineer-r2.md. HEAD moved to e425534 mid-review; the named test also passes there.
