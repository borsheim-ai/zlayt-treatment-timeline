# Subagent: T-115 r2 check (haiku staff) (T-115 r2 check (haiku staff))

Source: `agent-a1e513c8e10301423.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T10:13:13.009Z

Round-2 check of board card T-115 in /Users/arsis/zlayt-pm-project. The fixture change landed inside commit 08c921e, which was swept in by another worker's commit; see the card note via `python3 tools/board.py show T-115`. Read reviews/T-115-staff-engineer.md and D-029 in memory/ORCHESTRATOR_DECISIONS.md.

On a `git archive HEAD` copy in your scratchpad, confirm:
- no curated judge answer shadows a recording, and every judge answer the demo needs is a real recording. The worker reports 19 new claude-cli recordings, all 28 curated judge files removed, and make_curated.py no longer scripting judge answers;
- tests/unit/test_curated_fixtures.py fails when a recording is copied into the curated set (try it in a scratch copy);
- `tests/fixtures/make_curated.py --check` passes;
- the full tests/e2e passes with your own fixture server on a spare port (ZLAYT_MODE=local, ZLAYT_DB in your scratchpad), except the T-117 xfail. Stop the server by PID.

Also say whether commit 08c921e contains anything unrelated to T-079 and T-115 beyond these fixtures. Write reviews/T-115-staff-engineer-r2.md with a ```json block of real values: card, persona staff-engineer-reviewer, model claude-haiku-5-5, verdict, findings. Reply in 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:14.475Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T10:13:14.484Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:15.238Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-115; echo ---; cat reviews/T-115-staff-engineer.md; echo ---; grep -n \"D-029\" -A12 memory/ORCHESTRATOR_DECISIONS.md; echo ---; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ | head -50",
 "description": "Read T-115 card, prior review, D-029, and persona memory"
}
````

### User / tool · 2026-11-02T10:13:15.407Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:17.684Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-115 | sed -n '/## Notes/,$p'; echo ---REVIEW; cat reviews/T-115-staff-engineer.md; echo ---D029; grep -n \"D-029\" -A14 memory/ORCHESTRATOR_DECISIONS.md | head -60",
 "description": "Read T-115 notes, prior review, and D-029"
}
````

### User / tool · 2026-11-02T10:13:17.908Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:18.265Z

**tool call — Bash**
````
{
 "command": "git log --oneline -8 && echo --- && git show --stat 08c921e | head -80 && echo --- && git status --short | head -30; echo ---; ls -la .claude/agent-memory/staff-engineer-reviewer/ 2>/dev/null | head; ",
 "description": "Show recent git log and commit 08c921e stats"
}
````

### User / tool · 2026-11-02T10:13:18.428Z

**tool result**
````
08c921e feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
288affc test(backend): T-113 relabel H3V5 wrong -> correct by the D-046 second-agent ruling (reviews/T-093-staff-engineer-r4.md F1), before any run
6e880e6 test(e2e): T-060 follow-ups - letter keys from an item row, one-sentence tray flag lead, retrying judge-count assert
b89b9d9 docs: D-055 gaps warn on administrative endpoints instead of excluding
9fcae9b feat(frontend): layout polish: open-decisions strip, skip links and Start review, compact rows with captioned quotes and status chips, one-line charges rows, side-by-side flag evidence, processing state with progress, export focus and single primary, cases collapsed, T-096 minors (T-060)
eabe2b8 feat(frontend): one design-token system (tokens.css: palette light+dark, 7-step type scale, spacing, 2 radii, elevation) and every stylesheet rebuilt on it; one button and chip system with hover, active, focus and disabled states; sticky case header (T-060)
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
ea6ac71 fix(backend): gap exclusion fails safe toward treatment; label head + no treatment evidence required (T-116 r2)
---
commit 08c921e878edfb8571e60972bbf5681e16d328fc
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 04:12:32 2026 -0600

    feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
    
    Eight fully synthetic packets (second crash before MRI, Spanish interpreter note, UB-04/EOB/CMS-1500 OCR, priors and ledger with LOP,
    pre-suit records review with Waddell lines, cloned ROS, handwritten chiro scans with ambulance invoice, conclusory letter and 18.001
    affidavit), built by evals/library_build_v2.py. 291 claude-cli fixtures; lib09 r2, lib10 r6 and lib15 r7 stay honest
    LLM_FAILED_AFTER_RETRIES (no attempt-1 fixture). evals/library_report.py reports the packets, not gated. Denylist qa-side test.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 ...570d54c548a95e06668c89582af6b88e6c7daabb1e.json | 11 +++
 ...3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json | 11 +++
 ...e3919c5026fbe3d861980232f358270485a9f57243.json | 11 +++
 ...d57e7d5e1178adc854f1d757d5a54a266d0d0f8cef.json | 11 +++
 ...adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json | 11 +++
 ...f89a2dd162686e5fad03ab84d9002ab438849ebd4b.json | 11 +++
 ...43360478c22289d982857f3abc73377b804535ad59.json | 11 +++
 ...e1e6f1869abbbf083f6195a3441973e1074bd3f0f7.json | 11 +++
 ...d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd.json | 11 +++
 ...9bf3f9badf9c1b9309b76458a00213118b383ce266.json | 11 +++
 ...dec8e691ef3e4d43c35ee74fae0b2aa2be2fa4615c.json | 11 +++
 ...123a19a4e168e77bfef3ae9d74bc90ef232fc6e353.json | 11 +++
 ...d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2.json | 11 +++
 ...4647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json | 11 +++
 ...25a924ba1d5a4ce06b53da8f8feb7b9c7120e7f47c.json | 11 +++
 ...be7ce70971f30fa2a084cfdd39683e5f0b4dc3719d.json | 11 +++
 ...0870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json | 11 +++
 ...ff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json | 12 ---
 ...570d54c548a95e06668c89582af6b88e6c7daabb1e.json | 12 ---
 ...3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json | 12 ---
 ...e3919c5026fbe3d861980232f358270485a9f57243.json | 12 ---
 ...d57e7d5e1178adc854f1d757d5a54a266d0d0f8cef.json | 12 ---
 ...adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json | 12 ---
 ...f89a2dd162686e5fad03ab84d9002ab438849ebd4b.json | 12 ---
 ...ee311f3741eaff8b4b39498d8afefcb62580adb002.json | 12 ---
 ...43360478c22289d982857f3abc73377b804535ad59.json | 12 ---
 ...3904905e4e400ef4c6eb8499806d234f247dd75262.json | 12 ---
 ...e1e6f1869abbbf083f6195a3441973e1074bd3f0f7.json | 12 ---
 ...d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd.json | 12 ---
 ...9bf3f9badf9c1b9309b76458a00213118b383ce266.json | 12 ---
 ...f53c07e4809ea08d9727f280e2e72b226c9faa5aa7.json | 12 ---
 ...dec8e691ef3e4d43c35ee74fae0b2aa2be2fa4615c.json | 12 ---
 ...964771f61a25a922a5ac73859003d373d4c3536c06.json | 12 ---
 ...123a19a4e168e77bfef3ae9d74bc90ef232fc6e353.json | 12 ---
 ...d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2.json | 12 ---
 ...c7d7ccb6f8cbdf043cc018ab771440220878c84c96.json | 12 ---
 ...4647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json | 12 ---
 ...25a924ba1d5a4ce06b53da8f8feb7b9c7120e7f47c.json | 12 ---
 ...be7ce70971f30fa2a084cfdd39683e5f0b4dc3719d.json | 12 ---
 ...edb9e84de793ef1b3c6d8199cf65b07e65215991a9.json | 12 ---
 ...0870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json | 12 ---
 ...37297b943bf22d277951ff13184756fb659abb91ea.json | 12 ---
 ...6002a95c251a33a13b481a7052a943749f4d72e043.json | 12 ---
 ...c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c.json | 12 ---
 ...184cd405c56e7ebec814f8257f091fe60ffe2eda10.json | 12 ---
 ...6002a95c251a33a13b481a7052a943749f4d72e043.json | 11 +++
 ...184cd405c56e7ebec814f8257f091fe60ffe2eda10.json | 11 +++
 tests/fixtures/make_curated.py                     | 43 +++++++++-
 tests/unit/test_curated_fixtures.py                | 94 ++++++++++++++++++++++
 49 files changed, 345 insertions(+), 337 deletions(-)
---
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
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/paralegal-reviewer/reviewer-hook-constraints.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/conflicts.py
 M app/backend/flag_templates.py
 M app/backend/gaps.py
 M app/backend/pipeline.py
 M app/backend/present.py
 M app/backend/review.py
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
---
total 504
drwxr-xr-x@ 47 arsis  staff   1504 Nov  2 04:04 .
drwxr-xr-x@ 18 arsis  staff    576 Nov  2 03:02 ..
-rw-r--r--@  1 arsis  staff   8549 Nov  2 04:04 MEMORY.md
-rw-r--r--@  1 arsis  staff   1978 Nov  2 01:02 feedback_exact_count_vs_presence.md
-rw-r--r--@  1 arsis  staff   1670 Nov  1 22:52 feedback_review_write_once.md
-rw-r--r--@  1 arsis  staff   1132 Nov  1 20:37 feedback_severity_vs_brief.md
-rw-r--r--@  1 arsis  staff   1108 Nov  2 00:30 feedback_shared_scratchpad.md
-rw-r--r--@  1 arsis  staff   2587 Nov  1 19:58 project_backend_llm_review_patterns.md
-rw-r--r--@  1 arsis  staff   1928 Nov  1 19:49 project_db_review_patterns.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:22.284Z

**tool call — Bash**
````
{
 "command": "git rev-parse HEAD && echo --- && git show --stat --format= 08c921e | awk '{print $1}' | sed 's/^\\.\\.\\..*\\//.../' | head -80; echo ---; git show --name-status --format= 08c921e | awk '{print $1, $2}' | sort | uniq -c | sort -rn | head -5; echo; git show --name-only --format= 08c921e | grep -v 'tests/fixtures/llm/' ",
 "description": "Get HEAD sha and list files changed in 08c921e"
}
````

### User / tool · 2026-11-02T10:13:22.457Z

**tool result**
````
08c921e878edfb8571e60972bbf5681e16d328fc
---
...570d54c548a95e06668c89582af6b88e6c7daabb1e.json
...3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json
...e3919c5026fbe3d861980232f358270485a9f57243.json
...d57e7d5e1178adc854f1d757d5a54a266d0d0f8cef.json
...adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json
...f89a2dd162686e5fad03ab84d9002ab438849ebd4b.json
...43360478c22289d982857f3abc73377b804535ad59.json
...e1e6f1869abbbf083f6195a3441973e1074bd3f0f7.json
...d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd.json
...9bf3f9badf9c1b9309b76458a00213118b383ce266.json
...dec8e691ef3e4d43c35ee74fae0b2aa2be2fa4615c.json
...123a19a4e168e77bfef3ae9d74bc90ef232fc6e353.json
...d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2.json
...4647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json
...25a924ba1d5a4ce06b53da8f8feb7b9c7120e7f47c.json
...be7ce70971f30fa2a084cfdd39683e5f0b4dc3719d.json
...0870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json
...ff2af8134fcd3b2969bea747f1d00b18f2d191a36d.json
...570d54c548a95e06668c89582af6b88e6c7daabb1e.json
...3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json
...e3919c5026fbe3d861980232f358270485a9f57243.json
...d57e7d5e1178adc854f1d757d5a54a266d0d0f8cef.json
...adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json
...f89a2dd162686e5fad03ab84d9002ab438849ebd4b.json
...ee311f3741eaff8b4b39498d8afefcb62580adb002.json
...43360478c22289d982857f3abc73377b804535ad59.json
...3904905e4e400ef4c6eb8499806d234f247dd75262.json
...e1e6f1869abbbf083f6195a3441973e1074bd3f0f7.json
...d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd.json
...9bf3f9badf9c1b9309b76458a00213118b383ce266.json
...f53c07e4809ea08d9727f280e2e72b226c9faa5aa7.json
...dec8e691ef3e4d43c35ee74fae0b2aa2be2fa4615c.json
...964771f61a25a922a5ac73859003d373d4c3536c06.json
...123a19a4e168e77bfef3ae9d74bc90ef232fc6e353.json
...d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2.json
...c7d7ccb6f8cbdf043cc018ab771440220878c84c96.json
...4647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json
...25a924ba1d5a4ce06b53da8f8feb7b9c7120e7f47c.json
...be7ce70971f30fa2a084cfdd39683e5f0b4dc3719d.json
...edb9e84de793ef1b3c6d8199cf65b07e65215991a9.json
...0870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json
...37297b943bf22d277951ff13184756fb659abb91ea.json
...6002a95c251a33a13b481a7052a943749f4d72e043.json
...c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c.json
...184cd405c56e7ebec814f8257f091fe60ffe2eda10.json
...6002a95c251a33a13b481a7052a943749f4d72e043.json
...184cd405c56e7ebec814f8257f091fe60ffe2eda10.json
tests/fixtures/make_curated.py
tests/unit/test_curated_fixtures.py
49
---
   1 M tests/fixtures/make_curated.py
   1 D tests/fixtures/llm/curated/f5212e784cce54b0dd547f184cd405c56e7ebec814f8257f091fe60ffe2eda10.json
   1 D tests/fixtures/llm/curated/f2f207afab19f26f381d11c7f1b84064e3d14d1ae5bde696b04c52dd4d1d2a7c.json
   1 D tests/fixtures/llm/curated/e2f91427aeef98707788656002a95c251a33a13b481a7052a943749f4d72e043.json
   1 D tests/fixtures/llm/curated/d1e36f0196ae18855248ea37297b943bf22d277951ff13184756fb659abb91ea.json

tests/fixtures/make_curated.py
tests/unit/test_curated_fixtures.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:22.510Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-115-staff-engineer.md"
}
````

### User / tool · 2026-11-02T10:13:22.518Z

**tool result**
````
1	# T-115 review: E2E suite green on clean HEAD (staff-engineer-reviewer)
2	
3	Pinned: commit 400a8c06c96bafce4dd61f177f97d1fa2ab4d50f (parent c1b44be). Reviewed from `git archive 400a8c0` copy, not the working tree.
4	Model: claude-haiku-5-5.
5	
6	## Verdict: changes (0 blockers, 3 majors, 1 minor)
7	
8	The regeneration is narrower than the commit says and does not change any judge answer. T-117 is a real product bug and the strict xfail is the right way to record it. But the card's central claim, that the full e2e suite passes at HEAD with 172 passed, does not reproduce at 400a8c0. At HEAD I got 169 passed with 3 failed (run 2), or 156 passed with 1 failed and 16 skipped (run 1). The evidence in the handoff was taken at 36ceb38, three commits earlier.
9	
10	## What I ran and what I found
11	
12	**E2E at HEAD (own server, archive of 400a8c0, port 7971, fixture backend, curated set, ZLAYT_MODE=local).**
13	- Run 1, ZLAYT_DB not exported to pytest: `1 failed, 156 passed, 16 skipped, 1 xfailed in 223.67s`. The 16 skips are the ZLAYT_DB-dependent tests in test_code_check_refusal.py, which never ran.
14	- Run 2, fresh scratch DB, ZLAYT_DB exported to pytest: `3 failed, 169 passed, 1 skipped, 1 xfailed in 231.41s`. Only the T-117 xfail is strict and xfailed.
15	- Expected from the card: 172 passed, 1 skipped, 1 xfailed. Not reproduced.
16	
17	**Deterministic failure at HEAD.** `test_p_moves_focus_into_pane_and_escape_returns` fails (run 1 and run 2, and again alone twice): `tests/e2e/test_side_by_side.py:61`, `Locator expected to be focused ... Actual value: inactive`. The aria snapshot shows `Select an item, or press j, to see its source record here.` The same test run alone against a `git archive 36ceb38` copy on its own server (port 7972) gives `1 passed`. 3e3f3b7 (T-060, in the card's history but not in its evidence) changed the single-key handler so it acts only from an item row (`app/frontend/review.js:311-312`, `const row = RV.itemRowOf(t); if (!row) return;`). The test presses `j` from the page body (`test_side_by_side.py:60`). That is test drift from an intended product change. It is still red at the card's commit.
18	
19	**Flaky test.** `tests/e2e/test_stepper.py:204` and `:257` read `judge-summary-counts` with `inner_text()`, with no auto-wait, after waiting only for the container. The text is sometimes `loading…`. Run 2 failed both. Rerunning the pair alone three times at HEAD gave `1 failed, 1 passed`, `2 passed`, `1 failed, 1 passed`. Run 1 passed both, so the same HEAD is not reproducible.
20	
21	**Unit suite at HEAD.** `LLM_BACKEND=fixture pytest tests/unit`: `2556 passed, 4 skipped in 175.90s`.
22	
23	**Curated regeneration (400a8c0, 9 files).** `git show --stat 400a8c0` shows 5 renames (only `recorded_at` changed), 2 new files and 2 deleted files: 7 keys out, 7 keys in. I replayed the check at a9a27ed (last commit where the curated set was valid, `make_curated check: True`, 47 of 47 keys), at HEAD and at c1b44be, instrumenting `prompt_hash`:
24	- The 7 changed keys are 6 judge_flag `v2` to `v3` (J4) and 1 judge_conflict `v4` to `v5` (J3). The commit and handoff mention only judge_flag_v3.
25	- For all 7, the user text and JSON schema are identical. Only the system prompt text changed: J4 gained a missed_care definition and a scene-facts rule; J3 gained a CAN_BOTH_BE_TRUE rule for denials about different body parts. These are intended product prompt changes, not regen artefacts.
26	- Every new curated answer equals the old one (J4 `agree`/`NONE` ×6, J3 `conflict`/`NONE` ×1). No judge verdict changed.
27	- `make_curated.py --check` at HEAD: exit 0, `letter equal: True | notes equal: True`. At c1b44be: exit 1, `JUDGE_NOT_RUN` (7 keys missing). So the staleness was real.
28	
29	**Where the regeneration still papers over something.**
30	- Three of the six re-keyed J4 answers (`41e42a29…`, `5b05ba47…`, `e2f91427…`) have no recorded model output under judge_flag_v3 anywhere in `tests/fixtures/llm/`. Their only answer is the hand-scripted `agree` from `tests/fixtures/make_curated.py:49-52`, which picks `agree` for every J4 call.
31	- The J3 key `d1e36f01…` has a real claude-cli recording (`recorded_from` model claude-haiku-5-5, 2026-11-02T07:04:40Z) with `reason_code: PLAN_VS_ACTUAL`. Because `FIXTURE_SET=curated` is read first (`app/llm/backends/fixture.py:21-24`), the scripted answer with `reason_code: NONE` replaces it in the e2e run.
32	- The committed controls report that covers judge_conflict_v5 is red: `evals/reports/controls-20261102T090925Z.md:3` says `controls_ok: False`, and line 8 shows J3 13/17 caught with false agrees `J3V1, J3V9, J3V13, H3V5`. It was written 27 minutes before the regen commit. Neither the card nor the commit mentions it.
33	
34	**T-117 is a real product bug.** Confirmed, see finding list. Reproduced with `--runxfail`: the judge-row titles include `'f_r5_1'` with no `Record N` cue, while the other five rows carry cues. Root cause: `app/frontend/review.js:16-22` (`RV.find`) searches entries, undated entries, amounts and flags, but not `case.tray`. D-053 flags are only in `case.tray` (`app/backend/present.py:236-241`). `stepper.js:51-66` (`S.label`, `S.cue`) fall back to the raw id and an empty cue, and `judges.js:91` renders that label as the row title. The xfail is `strict=True` and names T-117.
35	
36	**No recurrence guard.** `grep -rln make_curated tests` finds only `tests/fixtures/make_curated.py`. No test runs `--check`, so the staleness was caught only by the e2e failures.
37	
38	## Findings
39	
40	Severity follows CONTRACT D.2. None of the §5 red flags apply: no silent fallback, no float money, no LLM date or total, no network in tests, no secrets.
41	
42	1. **major, the card's AC1 (HEAD green) is not met; the evidence is for 36ceb38.** See the deterministic failure and flaky-test paragraphs above. The handoff's "Verified: full tests/e2e on a clean HEAD worktree 172 pass" is not true for 400a8c0.
43	2. **major, flaky e2e race in judge-summary assertions** (`tests/e2e/test_stepper.py:204`, `:257`). Reproduce with the two test ids in a loop (three runs above).
44	3. **major, the regeneration re-keys judge answers without disclosing the J3 re-key, and leaves scripted answers standing for prompts whose live control is red.** See the three bullets above. No verdict changed, so this is not a silent product change, but the commit claim "12 e2e failures were fixture drift" is only true for keys.
45	4. **minor, no guard for curated-set staleness.** Add a unit test that runs `make_curated check()` against `tests/fixtures/llm/curated`. The handoff itself says a unit test would stop recurrence.
46	
47	## Fixes requested
48	
49	- F1: Rebase the test to focus an item row before `j` at `tests/e2e/test_side_by_side.py:60`. Re-run `git archive 400a8c0` with its own server and quote the full summary line. Only then cite 172.
50	- F2: Replace the one-shot `inner_text()` at `test_stepper.py:204` and `:257` with a web-first assertion (`expect(...).to_have_text(re.compile(...))`). Show 10 consecutive green runs of the two tests.
51	- F3: Correct the commit/handoff to say 6 J4 and 1 J3. Restore `reason_code: PLAN_VS_ACTUAL` for the J3 key or drop the curated override for it. Record in `memory/DECISIONS.md` or `ASSUMPTIONS.md` that three J4 v3 answers are scripted, and that judge_conflict_v5 controls were red at 090925Z. Re-run controls for v5 and cite the report.
52	- F4: Add the unit test in F4 above and show it fails if a prompt hash is changed.
53	
54	## What's right
55	
56	1. The regeneration changes only answer-file keys. Payload replay shows user text and schema unchanged for all 7 keys, and `make_curated --check` passes at HEAD with letter and notes equal to the golden.
57	2. The T-117 xfail is `strict=True`, names the card, and matches the traced root cause (`review.js:16-22` omits `case.tray`).
58	3. The 400a8c0 test diff is one marker line. No assertion was weakened. The unit suite is green at HEAD (2556 passed, 4 skipped).
59	
60	## Questions for Chris
61	
62	- Should curated answers override recorded claude-haiku-5-5 outputs, as they do for the J3 key (PLAN_VS_ACTUAL becomes NONE)? If yes, that needs a recorded decision.
63	- Is a curated J3 `conflict` answer acceptable for judge_conflict_v5 while its live controls are red?
64	
65	## Evidence
66	
67	- `artifacts/review-evidence/T-115-staff-engineer/e2e_run1_zlayt_db_unset.txt`
68	- `artifacts/review-evidence/T-115-staff-engineer/e2e_run2_zlayt_db_set.txt`
69	- `artifacts/review-evidence/T-115-staff-engineer/make_curated_check_c1b44be.txt`
70	- Scratch (not in repo): archive copies under the scratchpad `T115_staff_r1/` directory (HEAD `tree/`, `parent/`, `a9a/`, `base36/`); payload dumps `head_full.json`, `a9a/check.json`.
71	
72	```json
73	{"card": "T-115", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
74	 "scope": "commit 400a8c0 (parent c1b44be; 36ceb38 is the card's cited evidence commit); archive copy of 400a8c0; own fixture server http://127.0.0.1:7971 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), stopped by PID; tests/e2e, tests/unit, tests/fixtures/make_curated.py, tests/fixtures/llm/curated",
75	 "exercised": [
76	  "read personas/staff-engineer.md; board show T-115 and T-117",
77	  "git archive 400a8c06c96bafce4dd61f177f97d1fa2ab4d50f into scratchpad T115_staff_r1/tree; git show --stat and full diff of 400a8c0 for tests/e2e and tests/fixtures/llm/curated",
78	  "fixture server on 127.0.0.1:7971 from the archive; full pytest tests/e2e run 1 (ZLAYT_DB unset in pytest): 1 failed, 156 passed, 16 skipped, 1 xfailed",
79	  "full pytest tests/e2e run 2 (fresh DB, ZLAYT_DB set): 3 failed, 169 passed, 1 skipped, 1 xfailed",
80	  "test_p_moves_focus_into_pane_and_escape_returns alone x2 at 400a8c0 (fails) and alone on a git archive 36ceb38 copy at server 127.0.0.1:7972 (passes); server stopped by PID",
81	  "test_judge_panel_collapsed_summary_and_labels + test_judge_panel_when_nothing_objected x3 at 400a8c0 (mixed results)",
82	  "pytest tests/unit with LLM_BACKEND=fixture at 400a8c0: 2556 passed, 4 skipped",
83	  "make_curated.py --check at 400a8c0 (exit 0, letter/notes equal) and at c1b44be (exit 1, JudgeNotRun)",
84	  "instrumented replay (prompt_hash wrapper) at a9a27ed, c1b44be and 400a8c0: mapped the 7 changed keys to judge_flag v2->v3 (x6) and judge_conflict v4->v5 (x1); diffed system, user and schema per key",
85	  "provenance of tests/fixtures/llm/{d1e36f01,40edf164,6d5e6fe3,b362099f}*.json (recorded_from claude-cli, claude-haiku-5-5); absence of recorded files for 41e42a29, 5b05ba47, e2f91427",
86	  "tallied verdict/reason_code over curated judge answers at 400a8c0 and c1b44be (identical: supported/NONE 18, agree/NONE 9, conflict/NONE 1)",
87	  "T-117 repro: pytest --runxfail test_judge_panel_one_row_per_item_with_record_cue -> titles include 'f_r5_1' with no Record cue",
88	  "read app/frontend/review.js:15-22, 311-318; app/frontend/stepper.js:51-66; app/frontend/judges.js:91; app/backend/present.py:236-241; tests/fixtures/make_curated.py:38-52; app/llm/backends/fixture.py:20-26; evals/reports/controls-20261102T090925Z.md:3,8",
89	  "grep -rln make_curated tests (only tests/fixtures/make_curated.py)"
90	 ],
91	 "verdict": "changes",
92	 "scores": {"e2e_green_at_head": 2, "e2e_reproducibility": 2, "fixture_regen_faithfulness": 3, "xfail_discipline_T117": 5, "test_integrity_no_weakening": 4, "unit_suite_at_head": 4},
93	 "findings": [
94	  {"severity": "major",
95	   "title": "AC1 not met at HEAD: 172 passed does not reproduce at 400a8c0; the cited evidence is for 36ceb38, three commits earlier",
96	   "evidence": "Run 1 at 400a8c0: '1 failed, 156 passed, 16 skipped, 1 xfailed in 223.67s'. Run 2 (ZLAYT_DB set): '3 failed, 169 passed, 1 skipped, 1 xfailed in 231.41s'. Deterministic failure tests/e2e/test_side_by_side.py:61 (test_p_moves_focus_into_pane_and_escape_returns): 'Locator expected to be focused ... Actual value: inactive'; aria 'Select an item, or press j, to see its source record here.' Same test passes on git archive 36ceb38 (1 passed). Cause: 3e3f3b7 app/frontend/review.js:311-312 'const row = RV.itemRowOf(t); if (!row) return;' (j/k act only from an item row); test presses j from body at test_side_by_side.py:60. git merge-base --is-ancestor 36ceb38 400a8c0 succeeds; git log 36ceb38..400a8c0 lists 3e3f3b7, b5fb35c, c1b44be.",
97	   "why_it_matters": "The card's only deliverable is a green e2e suite at HEAD; the handoff ('Verified: full tests/e2e on a clean HEAD worktree 172 pass') is not true for the commit it is attached to. The milestone gate would inherit a red suite with a false green record.",
98	   "fix": "Test drift, not a product bug: focus an item row before pressing j at tests/e2e/test_side_by_side.py:60, then re-run on a fresh git archive of 400a8c0 and quote the full summary line. Correct the handoff to name the commit it was run on.",
99	   "acceptance_test": "git archive 400a8c0 -> own fixture server -> ZLAYT_DB=<scratch> E2E_BASE_URL=... pytest tests/e2e -q prints 0 failed and 172 passed, 1 skipped, 1 xfailed (strict, T-117)."},
100	  {"severity": "major",
101	   "title": "Flaky e2e race: judge-summary counts read with inner_text() before they render",
102	   "evidence": "tests/e2e/test_stepper.py:202-204 waits only for judge-summary, then assert re.search(..., jp.get_by_test_id('judge-summary-counts').inner_text()); the failure text is 'loading…' (line 204). Same pattern at :257. Pair run x3 at 400a8c0: '1 failed, 1 passed' / '2 passed' / '1 failed, 1 passed'. Run 1 passed both; run 2 failed both (AssertionError: judge-summary-counts inner_text 'loading…').",
103	   "why_it_matters": "A gate that passes on one run and fails on the next cannot be used as evidence, and it makes the AC1 result unreproducible (persona criterion 14: no timing dependence).",
104	   "fix": "Use a web-first assertion that auto-waits, e.g. expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\\d+ checked, \\d+ agreed with the draft, 3 questioned')), and the same for the 'checked \\d+, all agreed' case; do not read inner_text() once.",
105	   "acceptance_test": "Both tests pass in 10 consecutive runs of the pair at the HEAD archive, with a fresh ZLAYT_DB each time."},
106	  {"severity": "major",
107	   "title": "Regeneration re-keys 7 judge answers, one of them a J3 (judge_conflict v4->v5) not mentioned in the commit; 3 J4 v3 answers and the J3 answer are scripted, and the J3 recording is overridden",
108	   "evidence": "Replay of a9a27ed (check True, 47/47), c1b44be (JudgeNotRun) and 400a8c0 with prompt_hash instrumentation: the 7 changed keys are judge_flag v2->v3 x6 and judge_conflict v4->v5 x1; user text and schema identical, only system prompt text differs. Curated answers unchanged in content (agree/NONE x6, conflict/NONE x1). Recorded files: tests/fixtures/llm/d1e36f0196ae18855248ea37297b943bf22d277951ff13184756fb659abb91ea.json recorded_from claude-cli claude-haiku-5-5 with output {reason_code: PLAN_VS_ACTUAL, verdict: conflict}; the curated file for the same key has reason_code NONE, and FIXTURE_SET=curated is read first (app/llm/backends/fixture.py:21-24). Keys 41e42a29..., 5b05ba47..., e2f91427... have no file outside tests/fixtures/llm/curated. make_curated.py:49-52 picks 'agree' for every J4 call. evals/reports/controls-20261102T090925Z.md:3 'controls_ok: False' and :8 J3 judge_conflict_v5 13/17, false agrees J3V1, J3V9, J3V13, H3V5; that report predates the regen commit (09:36Z) by 27 minutes.",
109	   "why_it_matters": "No verdict changed, so this is not a silent product change, but the green curated e2e now rests on hand-scripted 'agree' answers for judge_flag_v3 (three keys have no model output under v3) and a J3 answer that drops the recorded reason. The judge_conflict_v5 live controls are red and the card does not say so. The commit message's 'fixture drift' label is true for keys, not for judge behaviour.",
110	   "fix": "Correct the commit/handoff to 6 J4 + 1 J3 re-keys. Restore reason_code PLAN_VS_ACTUAL for the J3 key (or stop the curated override for that key). Record in memory/DECISIONS.md or ASSUMPTIONS.md which curated judge answers are scripted and that judge_conflict_v5 controls were red at 20261102T090925Z. Re-run judge controls for v5 and cite the new report.",
111	   "acceptance_test": "A test asserts for each curated judge key that the reason_code equals the recorded one where a recording exists, and that every curated key maps to a judge prompt whose latest committed controls report is controls_ok True (or the exception is recorded in DECISIONS)."},
112	  {"severity": "minor",
113	   "title": "No guard against curated-set staleness; make_curated --check is run by nobody",
114	   "evidence": "grep -rln make_curated tests returns only tests/fixtures/make_curated.py. At c1b44be, 'python tests/fixtures/make_curated.py --check' exits 1 with JudgeNotRun (7 keys missing). The handoff says 'a unit test for that would stop recurrence' but none was added in 400a8c0 (git show --stat 400a8c0 lists only tests/e2e/test_stepper.py and tests/fixtures/llm/curated).",
115	   "why_it_matters": "Staleness was caught only indirectly, as 12 e2e failures. The next prompt bump will silently repeat it.",
116	   "fix": "Add a unit test that runs make_curated check() (or the equivalent key-coverage check) against tests/fixtures/llm/curated.",
117	   "acceptance_test": "Changing a judge prompt file without regenerating the curated set makes the new unit test fail; restoring the set makes it pass."}
118	 ],
119	 "whats_right": [
120	  "The regeneration changes only answer files; replay shows user text and schema identical for all 7 keys, and make_curated --check passes at HEAD with letter and notes equal to the golden.",
121	  "The T-117 xfail is strict=True, names the card, and matches the traced root cause (review.js:16-22 RV.find omits case.tray; present.py:236-241 puts D-053 flags there); --runxfail shows the 'f_r5_1' title with no Record cue.",
122	  "The 400a8c0 test diff is one marker line; no assertion was weakened. Unit suite at HEAD: 2556 passed, 4 skipped."
123	 ],
124	 "questions_for_chris": [
125	  "Should curated answers override recorded claude-haiku-5-5 outputs (the J3 key goes from PLAN_VS_ACTUAL to NONE)? If yes, record it as a decision.",
126	  "Is a scripted curated J3 'conflict' answer acceptable for judge_conflict_v5 while its committed live controls report is controls_ok False?"
127	 ]}
128	```
129	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:23.051Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-029\" memory/ORCHESTRATOR_DECISIONS.md | head; echo ---; awk '/D-029/{f=1} f{print; n++} n>25{exit}' memory/ORCHESTRATOR_DECISIONS.md",
 "description": "List 08c921e non-fixture files and read D-029"
}
````

### User / tool · 2026-11-02T10:13:23.106Z

**tool result (error)**
````
PreToolUse:Bash hook error: board-guard: reviewers may only write under reviews/ or artifacts/review-evidence/ (redirect to 25{exit})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:26.077Z

**tool call — Bash**
````
{
 "command": "grep -n \"D-029\" memory/ORCHESTRATOR_DECISIONS.md | head -5; L=$(grep -n \"D-029\" memory/ORCHESTRATOR_DECISIONS.md | head -1 | cut -d: -f1); sed -n \"${L},$((L+20))p\" memory/ORCHESTRATOR_DECISIONS.md",
 "description": "Locate and print the D-029 decision entry"
}
````

### User / tool · 2026-11-02T10:13:26.173Z

**tool result**
````
37:| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curated/` (hand-checked generator/judge responses that reproduce the golden summaries/excerpts exactly; labelled CURATED). E2E byte-equality (R-EX-6) and the public demo replay the curated set and the UI labels it 'cached demo (curated responses)'; the ship bar (§8.2) is measured on live runs and recorded fixtures only. | A live model may legitimately choose different whole-sentence excerpts (entry 2 adding the ER-charges sentence); byte-equality needs fixed responses; honesty needs the label. | T-040 handoff |
| D-030 | Flag evidence is the **verbatim phrase span** that triggered the flag (lexicon match or LLM-returned span), e.g. "Findings may represent degenerative change", "New onset pain" — not the whole sentence. Entry excerpts stay whole sentences (D-021). Internal notes quote flag spans; the golden notes block is the authority. | Precise flag quotes; matches the hand-written golden; entries keep context. | T-051/backend-4 |
| D-031 | **Scope reinstated (Chris, inbox 02:05Z):** build cut items that need no third-party integration, after the M3 core path (T-040..T-045) is green: multi-case with a case list (local/dev mode; public demo stays token-only per D-008) and a researched synthetic case library; PDF text-layer upload (no OCR); batch accept for *verified entries only* (never amounts or flags); manual entry for a rejected record (paralegal selects whole verbatim sentences, still grounded); LLM split fallback (flagged LLM_SPLIT); 'not a duplicate' split; full audit view (local mode); exhibit/Bates numbering as a per-case config; draft treatment paragraph in firm voice (stretch from spec; every sentence grounded + judged, internal until accepted). **Still cut, with reason:** charge reclassification (a rate must never become a charge — safety), auth/roles (needs an identity provider), per-user learning (needs its own evals), numeric confidence (unverifiable precision), non-English/handwriting, date-convention inference (silent-guess risk), OCR. | Chris asked; each reinstated item keeps the ladder and grounding rules. | Chris inbox 02:05Z |
| D-032 | Narrows D-018: normal/negative findings (`objective_negative`: 'negative for fracture', 'WNL', 'full ROM') are **context only, never flags**; `scene_facts` raise a causation flag only on specific adjuster phrases ('minimal damage', 'refused transport', 'ambulatory at scene', 'no airbag deployment'), never on a plain mechanism description ('Cyclist struck by a car'). | First eval: causation precision 0.5 from these two categories; golden case_05 must_not N2. | T-038 eval report 20261102T020824Z |
| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
| D-034 | Hardens D-006/R-RV-3: a number, date or $ figure in a summary, edit or manual entry that is not in that item's excerpt (or its source label/parsed date) is a **hard 422** — no 'keep my wording' override. The 409 confirm path remains only for non-numeric judge objections, and any override is listed in internal notes ('reviewer override: <reason code>'). | An override let 'Pain 9/10' into the letter against a 4/10 quote — an invented fact. | T-056 paralegal review |
| D-035 | Simplifies D-033: `patient_report` is attached only to a **clause** that begins with an explicit patient subject ('Patient', 'Pt', 'The patient') followed by a reporting verb (states, reports, notes, says, endorses, complains of, c/o, denies); the tag spans that clause only (to the next ';' or sentence end). Everything else — EMS, family, any other or unknown speaker, header labels — gets **no tag**. Default is no tag: a missing chip is safe, a wrong chip is not. | Speaker-list regexes kept missing new speakers (girlfriend, co-worker). | T-061 r2 |
| D-036 | Amends D-020 (2026-11-02): with `ZLAYT_MODE=local` (loopback-only), demo mode also admits the repo-shipped synthetic `evals/library/*.txt` packets by exact normalized hash. Arbitrary text is still rejected and not stored; the public build is unchanged (409). Local mode must refuse any non-loopback client by peer address, not just by the `HOST` env var. | Chris asked for multi-case demos from researched mock data (D-031); library texts are synthetic and fixed, so admitting them adds no new input surface. | T-053 security r2 F1/F2 |
| D-037 | Final rule for `patient_report` (supersedes the clause-splitting in D-035, 2026-11-02): the chip attaches only when the **whole excerpt** is a single patient-subject clause (`Patient`/`Pt`/`The patient` + reporting verb), with no further clause after `;`, `,`, `and`, or `(`. Any mixed excerpt gets no chip and stays a plain record excerpt, so no verb list decides it. Bare `C/O` gets no chip. A missing chip is safe; a wrong chip mislabels the source. | Three adjuster rounds kept finding clause-boundary holes; fail closed instead of patching verbs. | T-061 claims-adjuster r3 B1/B2 |
| D-038 | Narrows D-032 (2026-11-02): normal or negative objective findings stay context-only, but defense **credibility phrases** from the lexicon (e.g. 'Waddell signs', 'out of proportion', 'symptom magnification', 'non-physiologic', 'inconsistent effort') raise a flag so the paralegal sees them before the adjuster does. | These are what an adjuster quotes against the claimant; hiding them defeats the prep purpose. | T-063 staff r1 major 6 |
| D-039 | Re-run with decided items (2026-11-02): once any entry in a case is accepted, edited or dismissed, the case's records are frozen. A re-run reuses the stored records and never re-splits, so decided items keep their record ids and excerpts. Re-splitting is allowed only while every entry is still pending. | Provenance of an accepted item is what the paralegal verified against; it must never silently move. | T-057 staff r3 blocker |
| D-040 | **Cut the `patient_report` self-report chip** (supersedes D-033/D-035/D-037, 2026-11-02). Every excerpt is shown as a verbatim record excerpt with its source label. No code or model labels who is speaking. | Four adjuster rounds each found mixed excerpts that a closed rule still mislabeled. The verbatim excerpt already shows who spoke ('Patient states…', 'wife reports…'), so the label added risk without information. A missing chip is safe; a wrong one is a credibility error. | T-061 claims-adjuster r4 blocker; §7.4 |
| D-041 | An entry with no confirmed date cannot be accepted into the letter (2026-11-02). Accept returns 422 `DATE_UNCONFIRMED` until the paralegal confirms a date (Dates to confirm) or the entry is moved to the notes block. The UI disables Accept with the reason shown. 'Date not stated' never appears in the treatment section. | A demand letter treatment line without a date is unusable and invites an adjuster challenge. | T-068 paralegal r2 major |
| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
| D-044 | The export gate enforces the full ladder (2026-11-02): an LLM-made item whose judge never ran (JUDGE_UNAVAILABLE) blocks export even if the paralegal accepted it. The gate step says why, and its action is 'Run the second check again' (re-judges just those items). There is no override: the contract says nothing LLM-made reaches the export without code check + judge + human. | Found by T-080 r2: 12 accepted items with no judge passed the gate silently. | T-080 staff r2 major |
| D-045 | D-044 scope (2026-11-02): (a) pending items never reach the letter, so they do not block export (the AI disclosure line counts them); (b) a summary the paralegal wrote or edited is human-authored, so it is exempt from the judge but still passes the D-034 code checks; (c) rejudge is audited through llm_calls plus ladder.rejudge; a review_events row waits for a db CHECK change (minor, M3). | Keeps D-044 strict for model-made text without blocking human-authored edits. | T-080 r3 handoff |
| D-046 | Ship-bar item 4 also gates on the seeded J3 (conflict) and J4 (flag) judge control sets (2026-11-02): each must catch every seeded wrong item with 0 false agrees. Control labels are fixed before a run; an item may be relabelled only with a written reason reviewed by a second agent, never because it failed. | Judges J3/J4 now decide flags (T-075, T-094); a catch rate only on J1 would leave them unmeasured. | T-093 staff r1 major 2 |
| D-047 | Extends D-034 (2026-11-02): side (left/right), negation (no/not/without) and qualifier tokens that are missing from the excerpt are also a **hard 422** on edit and manual entry. The 409 'keep my wording' path is removed, so the gate (T-098) and the edit route agree and no item can be confirmed into an unexportable state. | A side or negation the record does not state is as dangerous as an invented number; a confirm path that leads to a blocked export is a dead end. | T-098 handoff |
| D-048 | Language routing fails safe (2026-11-02, after T-085 r2): a record or line runs as English only when it is **confidently English** (enough English function and clinical words, and no non-English evidence). Everything else is Spanish if confidently Spanish, otherwise LANGUAGE_UNCERTAIN: needs_review, labeled, and never passes on English token checks alone. On mixed lines, the English **and** Spanish token and qualifier checks both run (union), so a dropped 'posible' is caught whichever language leads. Routing gets a held-out measurement set. | Two rounds of heuristic detection let fresh Spanish and other-language lines through as unlabeled English. | T-085 legal-nurse r2 |
| D-049 | Billing completeness is decided by a code accounting pass (2026-11-02, after T-083 r3): every money-shaped token in a billing record ($-prefixed, a number with two decimals, or a no-cents figure in an amount column) must be accounted for as a parsed row, an unreconciled line, an excluded rate or an on-row 'unclear'. If any token is unaccounted for, the provider is complete: false and the record is listed. Repeated summary rows (e.g. two balance-forward lines) are all listed, never overwritten. On-row 'unclear' with complete: false is acceptable (nothing is lost). | Three rounds of per-format parsing still let bare figures vanish with complete: true; a token-level accounting pass makes silent loss impossible regardless of format. | T-083 staff r3 |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:28.622Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-115 > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_card_show.txt 2>/dev/null; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$S\" && ls -la \"$S\" | head; grep -n \"^- 2026-11-02T1[0-9]\" \"$S/T115_card_show.txt\" | cut -c1-600",
 "description": "Check scratchpad and print the latest T-115 card notes"
}
````

### User / tool · 2026-11-02T10:13:28.782Z

**tool result**
````
total 192552
drwx------@  936 arsis  wheel    29952 Nov  2 04:13 .
drwx------@    4 arsis  wheel      128 Nov  1 23:12 ..
drwx------@    2 arsis  wheel       64 Nov  2 00:28 .x
-rw-r--r--@    1 arsis  wheel      311 Nov  2 01:13 641ed.bak
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M1
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M1_nocombine
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M2
drwxr-xr-x@   22 arsis  wheel      704 Nov  2 00:43 M2_find0
drwxr-xr-x@   21 arsis  wheel      672 Nov  2 00:39 M3
29:- 2026-11-02T10:04:54Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-115-staff-engineer.md; round 1; findings:
34:- 2026-11-02T10:04:54Z qa: claimed
35:- 2026-11-02T10:12:58Z qa: AC 1 checked: r2 fixtures: 19 judge answers recorded live (claude-cli haiku-5-5, attempt 1 each), 28 curated judge files removed, none scripted; make_curated.py --check exit 0 letter+notes equal; tests/unit/test_curated_fixtures.py 6 passed (fails on shadow/scripted/stale, shown by mutation); tests/unit 2631 passed (4 transient failures from other workers' concurrent edits, pass on rerun); commit 08c921e (swept into T-079's commit via shared index)
36:- 2026-11-02T10:12:58Z qa: moved in_progress -> in_review
37:- 2026-11-02T10:13:08Z orchestrator: review dispatched: staff-engineer-reviewer
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:42.301Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; R=$S/T115_staff_r2; mkdir -p $R/tree && cd /Users/arsis/zlayt-pm-project && git archive HEAD | tar -x -C $R/tree && cd $R/tree && ls && echo --- && git -C /Users/arsis/zlayt-pm-project show --name-status --format= 08c921e | awk '{print $1}' | sort | uniq -c; echo --- ; git -C /Users/arsis/zlayt-pm-project show --name-status --format= 08c921e | grep -v '^[MD]\\s*tests/fixtures/llm/' ; echo --- ; git -C /Users/arsis/zlayt-pm-project show --name-only --format= 08c921e | awk -F/ '{print $1\"/\"$2\"/\"$3}' | sort | uniq -c",
 "description": "Archive HEAD into scratchpad and classify 08c921e files"
}
````

### User / tool · 2026-11-02T10:13:42.785Z

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
---
  20 A
  28 D
   1 M
---
A	tests/fixtures/llm/0ec6b54252d87fcd2eba19570d54c548a95e06668c89582af6b88e6c7daabb1e.json
A	tests/fixtures/llm/11b63311d0540b20ebda1d3792e15b80fae54f0cd9b31e41d1efd2605bab803a.json
A	tests/fixtures/llm/1fa7109353e0e9d1dac4dbe3919c5026fbe3d861980232f358270485a9f57243.json
A	tests/fixtures/llm/259cc181fd38601822c3ddd57e7d5e1178adc854f1d757d5a54a266d0d0f8cef.json
A	tests/fixtures/llm/381284dcc1b16c10482345adac4fbf4c7589f9296e20a71edcb346002a8d84e5.json
A	tests/fixtures/llm/3e93106cc39afac1ba942ff89a2dd162686e5fad03ab84d9002ab438849ebd4b.json
A	tests/fixtures/llm/41e42a2978854c340fcf3f43360478c22289d982857f3abc73377b804535ad59.json
A	tests/fixtures/llm/477dfa7a8c46a9f909373be1e6f1869abbbf083f6195a3441973e1074bd3f0f7.json
A	tests/fixtures/llm/527b0abaed8766e43da906d3ef72c1a1ca4feda281901b5b5169faa6f1ab8dbd.json
A	tests/fixtures/llm/5b05ba47abeb8a9571b0ac9bf3f9badf9c1b9309b76458a00213118b383ce266.json
A	tests/fixtures/llm/636239bec8cb1f0bedd4a1dec8e691ef3e4d43c35ee74fae0b2aa2be2fa4615c.json
A	tests/fixtures/llm/6faaefbcd81dd8f8b0c9bf123a19a4e168e77bfef3ae9d74bc90ef232fc6e353.json
A	tests/fixtures/llm/81b9613e80eb3b3c5ba7c3d9a8c75b61a8e28b3b08dc259854b7a2424eb3ecb2.json
A	tests/fixtures/llm/9477789eaee295aff7a0f64647f29266fe8fc7b275e2519b02d9d5a3dc5b59e7.json
A	tests/fixtures/llm/96ba249e456255a14a93dc25a924ba1d5a4ce06b53da8f8feb7b9c7120e7f47c.json
A	tests/fixtures/llm/a59ed88ad3e291bf206d9fbe7ce70971f30fa2a084cfdd39683e5f0b4dc3719d.json
A	tests/fixtures/llm/bc66f801341fe95dcff0620870e5237a7cf8ee1b1630413bf59f24a34b10f5fb.json
A	tests/fixtures/llm/e2f91427aeef98707788656002a95c251a33a13b481a7052a943749f4d72e043.json
A	tests/fixtures/llm/f5212e784cce54b0dd547f184cd405c56e7ebec814f8257f091fe60ffe2eda10.json
M	tests/fixtures/make_curated.py
A	tests/unit/test_curated_fixtures.py
---
  47 tests/fixtures/llm
   1 tests/fixtures/make_curated.py
   1 tests/unit/test_curated_fixtures.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:49.934Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; cd $R && ls tests/fixtures/llm | head -3; echo \"top-level json: $(ls tests/fixtures/llm/*.json | wc -l)\"; echo \"curated json: $(ls tests/fixtures/llm/curated/*.json | wc -l)\"; ls -d tests/fixtures/llm/recorded 2>&1; echo ---; cat app/llm/backends/fixture.py; echo ---; cat tests/fixtures/make_curated.py",
 "description": "Inspect fixture layout, fixture backend, and make_curated.py in archive"
}
````

### User / tool · 2026-11-02T10:13:50.078Z

**tool result**
````
00335ec113c1f7234011ea2005f91965f2cc9dcf64aa50c61a8a35672c2b4cf3.json
003bc1687297bb8de21ccbb56c7fb2f14002dadc0484b4d9762290c39acadade.json
00c97f20c9cf54c24c8b3275a7382a44877f7bd89ccb0a419716cb030e564104.json
top-level json:     1089
curated json:       19
ls: tests/fixtures/llm/recorded: No such file or directory
---
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p
---
"""Builds tests/fixtures/llm/curated/ (D-029, T-051): HAND-CHECKED generator/judge responses that reproduce the golden summaries and
excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a model.
Run:  .venv/bin/python tests/fixtures/make_curated.py [--check]
Judge answers (any schema with a "verdict") are NEVER scripted (T-115 r2, D-029): the build replays the real recorded model answer from
tests/fixtures/llm/<key>.json and, on a miss, records one live (ENABLE_LIVE=1 LLM_BACKEND=claude-cli, at most 3 attempts). No curated
judge file is written, so a curated answer can never shadow a recording; the check replays curated first, then the recorded set.
The script runs the real pipeline on evals/golden/sample.txt with the provider patched to these scripted answers, writes one
<sha256>.json per distinct prompt (key = provider.prompt_hash), each with a top-level "CURATED" header, then replays the set through the
real fixture backend and checks the export against evals/golden/sample.export.expected.txt.
"""
import json, os, pathlib, sys, tempfile, time
ROOT = pathlib.Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
os.environ.setdefault("LLM_BACKEND", "fixture")
OUT = ROOT / "tests" / "fixtures" / "llm" / "curated"
MAX_LIVE_ATTEMPTS = 3
import threading
_LIVE_LOCK = threading.Lock()
HEADER = ("CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from "
          "sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).")

from tests.unit import _golden as G
from app.backend import ingest
from tests.unit._fakes import golden_summaries, which_record
from app.llm import provider as P
from app.llm._types import LLMResult

SUMS = golden_summaries()
GOLD = G.expected("sample")
# per-record LLM flags (type, category, verbatim span) taken from sample.expected.json evidence
FLAGS = {
    3: [("pre_existing", "pre_existing", "Patient reports low back pain in 2023, resolved.")],
    6: [("causation", "missed_care", "Discharged from PT after two missed appointments.")],
    7: [("causation", "new_onset", "New onset pain")],
    8: [("pre_existing", "degenerative_language", "Findings may represent degenerative change"),
        ("causation", "speculative_language", "may represent degenerative change; correlate clinically")],
    9: [("causation", "patient_report", "Patient states symptoms began after the January collision.")],
}
CONFLICT = dict(type="conflict", category="treatment_plan_vs_actual", excerpt="Plan of care: 12 visits.",
                excerpt_b="Discharged from PT after two missed appointments.")

NARR_OVERRIDE = {6: "Discharged from PT after two missed appointments; pain 3/10."}

def answer(system, user, schema):
    props = set(schema.get("properties", {}))
    if "sentences" in props:                      # narrative paragraph (T-059): one firm-voice sentence per accepted entry, from the golden summary
        import re
        # entry 6: the golden summary says "physical therapy" while the quote says "PT", which the code check reads as new adverse wording
        sents = [dict(entry_id=m.group(1), text=f"On {m.group(3)}, {m.group(4)}: " + NARR_OVERRIDE.get(int(m.group(2)), SUMS[int(m.group(2))][0]))
                 for m in re.finditer(r"^ENTRY (e(\d+)) \| (.*?) \| (.*)$", user, re.M)]
        return dict(sentences=sents)
    if {"summary", "excerpt"} <= props:
        n = which_record(user)[0]
        return dict(summary=SUMS[n][0], excerpt=SUMS[n][1])
    if "verdict" in props:
        enum = schema["properties"]["verdict"].get("enum") or []
        v = {"supported": "supported", "agree": "agree", "conflict": "conflict"}
        pick = next((x for x in ("supported", "agree", "conflict") if x in enum), enum[0])
        return dict(verdict=pick, reason_code="NONE")
    if "flags" in props:
        recs = which_record(user)
        if len(recs) > 1:                     # cross-record conflicts pass
            return dict(flags=[CONFLICT])
        out = [dict(type=t, category=c, excerpt=x, excerpt_b=None) for t, c, x in FLAGS.get(recs[0], [])] if recs else []
        return dict(flags=out)
    raise SystemExit(f"unknown schema for curated answer: {sorted(props)}")

def accept_all(conn, cid, out, call):
    from app.backend import review
    for kind in ("entries", "amounts", "flags"):
        for it in out[kind]:
            if it.get("state") != "rejected":
                try:
                    review.apply_review(conn, cid, it["id"], {"action": "accept"}, call=call)
                except Exception as e:
                    print("accept failed", it["id"], getattr(e, "code", e))


def build():
    from app.db import db as DB
    from app.backend import pipeline as PL
    from app.llm import audited as AU
    OUT.mkdir(parents=True, exist_ok=True)
    for f in OUT.glob("*.json"):
        f.unlink()
    written = {}
    def judge(model, system, user, schema):
        """Real model answer for a judge prompt: recorded if present, else live (<= 3 attempts) and recorded to the default dir."""
        key = P.prompt_hash(model, system, user, schema)
        try:
            return P._fixture.call(model, system, user, schema, key=key)
        except P.FixtureMiss:
            pass
        if P.backend_name() == "fixture":
            raise SystemExit(f"no recorded judge answer for {key[:12]} and no live backend: rerun with ENABLE_LIVE=1 LLM_BACKEND=claude-cli")
        want = next((x for x in ("supported", "agree", "conflict") if x in (schema["properties"]["verdict"].get("enum") or [])), None)
        with _LIVE_LOCK:                                      # judges run in threads; record_context and the env flag are process-global
            try:
                return P._fixture.call(model, system, user, schema, key=key)     # another thread recorded it meanwhile
            except P.FixtureMiss:
                pass
            os.environ["RECORD_FIXTURES"] = "1"
            try:
                for attempt in range(1, MAX_LIVE_ATTEMPTS + 1):
                    try:
                        with P.record_context(G.raw("sample")):
                            res = real(model, system, user, schema)
                    except Exception as e:                   # backend error / invalid JSON: counts as an attempt
                        print(f"judge {key[:8]} attempt {attempt}: {type(e).__name__} {e}")
                        continue
                    print(f"judge {key[:8]} attempt {attempt}: {res.output['verdict']} {res.output.get('reason_code')} (golden path expects {want})")
                    if res.output["verdict"] == want:
                        return res
                raise SystemExit(f"judge {key[:8]}: no accepted answer in {MAX_LIVE_ATTEMPTS} attempts; last recorded answer stays in tests/fixtures/llm")
            finally:
                os.environ.pop("RECORD_FIXTURES", None)

    def fake(model, system, user, schema):
        if "verdict" in schema.get("properties", {}):
            return judge(model, system, user, schema)
        key = P.prompt_hash(model, system, user, schema)
        out = answer(system, user, schema)
        written[key] = dict(CURATED=HEADER, output=out,
                            recorded_from=dict(backend="curated", model="hand-checked (qa)", recorded_at=time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())))
        return LLMResult(output=out, backend="fixture", model_resolved=model, recorded_from=written[key]["recorded_from"])
    real = P.complete_with_meta
    P.complete_with_meta = fake
    try:
        tmp = tempfile.mkdtemp()
        conn = DB.connect(os.path.join(tmp, "c.sqlite")); cid = DB.create_case(conn, ingest.normalize_text(G.raw("sample")), now=1.0)   # the API stores normalised text; the narrative nonce hashes it
        call = AU.make_call(conn, cid)
        out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
        accept_all(conn, cid, out, call)
        from app.backend import narrative
        narrative.draft(conn, cid, call=call, now=1.0)
    finally:
        P.complete_with_meta = real
    for k, v in written.items():
        (OUT / f"{k}.json").write_text(json.dumps(v, indent=1, sort_keys=True))
    return len(written)

def check():
    """Replays through the REAL fixture backend; accepts everything; compares letter_text with the golden file."""
    os.environ.pop("LLM_FIXTURE_DIR", None)
    os.environ["FIXTURE_SET"] = "curated"        # curated first, then the recorded set (judge answers are recordings only)
    os.environ["LLM_BACKEND"] = "fixture"
    from app.db import db as DB
    from app.backend import pipeline as PL, store, export, review
    from app.llm import audited as AU
    tmp = tempfile.mkdtemp()
    conn = DB.connect(os.path.join(tmp, "r.sqlite")); cid = DB.create_case(conn, ingest.normalize_text(G.raw("sample")), now=1.0)
    call = AU.make_call(conn, cid)
    out = PL.run_pipeline(conn, cid, G.raw("sample"), call=call, now=lambda: 1.0)
    bad = [(e["id"], e["state"], e["reasons"]) for e in out["entries"] if e["state"] != "verified"]
    print("entries:", len(out["entries"]), "non-verified:", bad)
    from app.db import db as DB2
    for kind in ("entry", "amount", "flag"):
        for it in DB2.list_items(conn, cid, kind):
            if it["review_status"] == "pending" and it["state"] != "rejected":
                try:
                    review.apply_review(conn, cid, it["id"], {"action": "accept"}, call=call)
                except Exception as e:
                    print("accept failed", it["id"], it.get("text") or it.get("summary"), getattr(e, "code", e))
    ex = export.build_export(store.export_case(conn, cid))
    from app.backend import narrative
    nar = narrative.draft(conn, cid, call=call, now=1.0)
    print("narrative:", nar.get("error") or f"{len(nar['sentences'])} sentences, removed: {[(r['entry_id'], r['reason']) for r in nar['removed']]}")
    g = (G.G / "sample.export.expected.txt").read_text()
    gl = g.split("=== INTERNAL_NOTES_TEXT")[0].split("\n", 1)[1].rstrip("\n")
    gn = g.split("=== INTERNAL_NOTES_TEXT")[1].split("\n", 1)[1].rstrip("\n")
    print("letter equal:", ex["letter_text"] == gl, "| notes equal:", ex["internal_notes_text"] == gn)
    if ex["letter_text"] != gl:
        import difflib
        print("\n".join(list(difflib.unified_diff(gl.split("\n"), ex["letter_text"].split("\n"), "golden", "got", lineterm=""))[:30]))
    return ex["letter_text"] == gl

if __name__ == "__main__":
    if "--check" not in sys.argv:
        print("curated files written:", build())
    sys.exit(0 if check() else 1)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:13:56.894Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; cd $R && cat tests/unit/test_curated_fixtures.py; echo ---; ls tests/fixtures/llm/curated/; echo ---; for f in tests/fixtures/llm/curated/*.json; do python3 -I -c \"import json,sys; d=json.load(open(sys.argv[1])); print(sys.argv[1].split('/')[-1][:12], list(d.keys()), d.get('recorded_from',{}).get('backend'), str(d.get('output'))[:70])\" \"$f\"; done",
 "description": "Read curated fixture unit test and list curated files"
}
````

### User / tool · 2026-11-02T10:13:57.491Z

**tool result**
````
"""Integrity of the curated fixture set (D-029; T-115 round 2).

Rule: a CURATED answer may stand in for a generator/narrative response (it reproduces the golden letter byte for byte), but a JUDGE answer
(any output with a "verdict") must be a real recorded model answer. So in tests/fixtures/llm/curated/:
  1. no judge file may exist under the same key as a recording in tests/fixtures/llm/ (it would shadow what the model really said; the
     fixture backend reads curated first), and
  2. no judge file may exist without a recorded counterpart,
unless the key is on JUDGE_ALLOW_LIST below with a documented reason. The list is empty on purpose: every judge answer is recorded
(claude-cli, claude-haiku-5-5) and tests/fixtures/make_curated.py writes none. Adding an entry needs a card and a DECISIONS/ASSUMPTIONS note.
"""
import json
import pathlib
import subprocess
import sys

import pytest

ROOT = pathlib.Path(__file__).resolve().parents[2]
RECORDED = ROOT / "tests" / "fixtures" / "llm"
CURATED = RECORDED / "curated"

# key (full sha256) -> reason it may be a curated judge answer with no recorded counterpart. Keep empty.
JUDGE_ALLOW_LIST: dict = {}


def _is_judge(path: pathlib.Path) -> bool:
    out = json.loads(path.read_text()).get("output")
    return isinstance(out, dict) and "verdict" in out


def judge_problems(curated: pathlib.Path, recorded: pathlib.Path, allow: dict) -> list:
    """Human-readable problems for the curated dir: shadowed recordings, and curated judge answers with no recording (not allow-listed)."""
    problems = []
    for p in sorted(curated.glob("*.json")):
        if not _is_judge(p):
            continue
        key = p.stem
        if (recorded / p.name).is_file():
            problems.append(f"SHADOWS_RECORDING {key[:12]}: curated judge answer overrides the recorded model answer")
        elif key not in allow:
            problems.append(f"SCRIPTED_JUDGE {key[:12]}: curated judge answer with no recorded counterpart and not on the allow-list")
    return problems


def _write(d: pathlib.Path, key: str, output: dict):
    d.mkdir(parents=True, exist_ok=True)
    (d / f"{key}.json").write_text(json.dumps({"output": output, "recorded_from": {"backend": "x", "model": "m", "recorded_at": "t"}}))


JUDGE_OUT = {"verdict": "supported", "reason_code": "NONE"}


def test_shipped_curated_set_has_no_shadowing_or_scripted_judge_answers():
    assert CURATED.is_dir() and any(CURATED.glob("*.json"))
    assert judge_problems(CURATED, RECORDED, JUDGE_ALLOW_LIST) == []


def test_allow_list_entries_are_documented_and_still_needed():
    for key, reason in JUDGE_ALLOW_LIST.items():
        assert isinstance(reason, str) and len(reason) >= 20, f"{key[:12]}: the allow-list needs a written reason"
        p = CURATED / f"{key}.json"
        assert p.is_file() and _is_judge(p), f"{key[:12]}: allow-listed key is not a curated judge file; remove it"
        assert not (RECORDED / p.name).is_file(), f"{key[:12]}: now recorded; remove it from the allow-list and the curated file"


def test_detector_fails_when_curated_judge_shadows_a_recording(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(rec, "a" * 64, JUDGE_OUT)
    _write(cur, "a" * 64, {"verdict": "supported", "reason_code": "ADDS_CAUSATION"})
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SHADOWS_RECORDING"]
    assert [p.split()[0] for p in judge_problems(cur, rec, {"a" * 64: "allow-listing must not hide a shadow of a recording"})] == ["SHADOWS_RECORDING"]


def test_detector_fails_on_scripted_judge_without_recording_unless_allow_listed(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(cur, "b" * 64, JUDGE_OUT)
    assert [p.split()[0] for p in judge_problems(cur, rec, {})] == ["SCRIPTED_JUDGE"]
    assert judge_problems(cur, rec, {"b" * 64: "documented: no live model available for this prompt"}) == []


def test_detector_ignores_non_judge_curated_answers(tmp_path):
    cur, rec = tmp_path / "curated", tmp_path
    _write(cur, "c" * 64, {"summary": "s", "excerpt": "e"})
    _write(rec, "c" * 64, {"summary": "other", "excerpt": "e"})
    assert judge_problems(cur, rec, {}) == []


def test_make_curated_check_is_current():
    """The curated set must still replay to the golden letter and notes at this HEAD (a prompt change re-keys judge prompts and
    leaves the set stale; the failure then names the missing keys). Runs in a subprocess because the check edits os.environ."""
    r = subprocess.run([sys.executable, str(ROOT / "tests" / "fixtures" / "make_curated.py"), "--check"], cwd=ROOT, capture_output=True,
                       text=True, timeout=240, env={**__import__("os").environ, "LLM_BACKEND": "fixture", "ENABLE_LIVE": "0"})
    assert r.returncode == 0, (r.stdout[-1500:] + r.stderr[-1500:])
    assert "letter equal: True | notes equal: True" in r.stdout
---
0f653bdfe99e71b7c81505f7bc5d32aea9d5666c5b3445fbc41dbeeb04c1740c.json
1ae147d35880668764ee15dc7b6b20f68fa6a4e331e91013f1230944469cb5f5.json
228350fb06e4cf872348f390212b959eebee7313b76f0edf051977846aacbc56.json
37318d752543b06d4add14f3ab3aa71dc4e089522d392b500a6057b9fc790d1d.json
3e70853a6fadff0e4991350de156ea38d30b396597dbab5bc74601b2508eb6d7.json
4770363f6bf66fd6ea99a13cfb8010ae193143c79e531601e5f825415f593d24.json
4a4f531c922d869d060a0bf7b1d33b777c496b90570dd511f38559feded30334.json
4ed3d9961f3523183444f9fe85f8d460762306ec1bc8d89ddca81e621c7a6198.json
7f9e06e6e15e75756fa39c3aca5bb45dcaa75e29d727b0d9b3a4da164dc54519.json
85a544a335859c486aaa581be110146353bbe09d65a0b3946d121a72f463ad81.json
98b1735efe416a520c3489da333b1326b50420338d0e2f84d27d5fa1918058e7.json
a1f0777e7722b161b62e8d670366303c827a2daff336fa324944e50a38f01c85.json
a3f0e26ea728d289fec7de9c1a0de532e5a7b68efdbb86a20f8dd418c7d461d8.json
aacd477fd06e2a5bc1729568312bfa28e9de09dfb37d368d6a5bbc1c8c3d3bb3.json
b0511a4e8269eaffd9832fbd4d21b731b8a552b0d09aa0ba6294f427fbc83eca.json
b74b563d21aa33a19743ebfce89fd89e2e18307d627dd3310718364dbfd51aee.json
bde3b432c62b6dd09e7d4e18309d7d874292d52854fcd3d186de68b03933ce91.json
be8b230f82b33d2d1e8a9e1e0c6d1c4dc143e1e993d0117aabc60fc6202636ee.json
eadc16a0cec098ac5d852b835fd3b35cc09643704bcca5995cec606dcdc06afa.json
---
0f653bdfe99e ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'New onset pain radiating to right arm with numbness in fi
1ae147d35880 ['CURATED', 'output', 'recorded_from'] curated {'flags': []}
228350fb06e4 ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Cervical range of motion reduced approx. 40%. Plan of car
37318d752543 ['CURATED', 'output', 'recorded_from'] curated {'flags': [{'category': 'pre_existing', 'excerpt': 'Patient reports lo
3e70853a6fad ['CURATED', 'output', 'recorded_from'] curated {'sentences': [{'entry_id': 'e1', 'text': 'On January 9, 2026, Austin 
4770363f6bf6 ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'C5-C6 disc protrusion with mild right foraminal narrowing
4a4f531c922d ['CURATED', 'output', 'recorded_from'] curated {'flags': []}
4ed3d9961f35 ['CURATED', 'output', 'recorded_from'] curated {'flags': []}
7f9e06e6e15e ['CURATED', 'output', 'recorded_from'] curated {'flags': []}
85a544a33585 ['CURATED', 'output', 'recorded_from'] curated {'flags': [{'category': 'missed_care', 'excerpt': 'Discharged from PT 
98b1735efe41 ['CURATED', 'output', 'recorded_from'] curated {'excerpt': '41M restrained driver, rear-ended at approx. 35 mph. C/O 
a1f0777e7722 ['CURATED', 'output', 'recorded_from'] curated {'flags': [{'category': 'degenerative_language', 'excerpt': 'Findings 
a3f0e26ea728 ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Recommend cervical epidural steroid injection. Patient st
aacd477fd06e ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Persistent neck pain 6/10, daily headaches. Refer to phys
b0511a4e8269 ['CURATED', 'output', 'recorded_from'] curated {'flags': [{'category': 'new_onset', 'excerpt': 'New onset pain', 'exc
b74b563d21aa ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Dx: cervical strain; concussion without loss of conscious
bde3b432c62b ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Pain 4/10, improving.', 'summary': 'Pain 4/10, improving.
be8b230f82b3 ['CURATED', 'output', 'recorded_from'] curated {'excerpt': 'Discharged from PT after two missed appointments. Pain 3/
eadc16a0cec0 ['CURATED', 'output', 'recorded_from'] curated {'flags': [{'category': 'patient_report', 'excerpt': 'Patient states s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:06.985Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R/tree && cat > $R/classify.py <<'EOF'\nimport json, sys, pathlib, collections\nd = pathlib.Path(sys.argv[1])\nc = collections.Counter()\nfor p in sorted(d.glob(\"*.json\")):\n    j = json.loads(p.read_text())\n    out = j.get(\"output\")\n    kind = \"judge\" if isinstance(out, dict) and \"verdict\" in out else \"gen\"\n    rf = j.get(\"recorded_from\", {}) or {}\n    c[(kind, rf.get(\"backend\"), rf.get(\"model\"), \"CURATED\" in j)] += 1\nfor k, v in sorted(c.items(), key=str):\n    print(v, k)\nEOF\necho \"== top-level recorded set (HEAD archive)\"; python3 -I $R/classify.py tests/fixtures/llm\necho \"== curated set (HEAD archive)\"; python3 -I $R/classify.py tests/fixtures/llm/curated\necho \"== 19 files added by 08c921e\"; for f in $(git -C /Users/arsis/zlayt-pm-project show --name-status --format= 08c921e | awk '$1==\"A\" && $2 ~ /tests\\/fixtures\\/llm\\/[0-9a-f]+\\.json/ {print $2}'); do echo \"$f\"; done > $R/added19.txt; wc -l < $R/added19.txt\npython3 -I - \"$R\" <<'EOF'\nimport json, sys, pathlib, collections\nR = pathlib.Path(sys.argv[1]); tree = R/\"tree\"\nc = collections.Counter(); kinds = collections.Counter()\nfor line in (R/\"added19.txt\").read_text().split():\n    j = json.loads((tree/line).read_text())\n    rf = j.get(\"recorded_from\", {})\n    c[(rf.get(\"backend\"), rf.get(\"model\"))] += 1\n    out = j.get(\"output\", {})\n    kinds[(\"verdict\" in out and \"judge\") or \",\".join(sorted(out))] += 1\n    print(pathlib.Path(line).name[:12], rf.get(\"backend\"), rf.get(\"model\"), rf.get(\"recorded_at\"), json.dumps(out)[:110])\nprint(\"provenance:\", dict(c)); print(\"kinds:\", dict(kinds))\nEOF",
 "description": "Classify fixture sets and provenance of the 19 added recordings"
}
````

### User / tool · 2026-11-02T10:14:07.227Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:17.433Z

**tool call — Bash**
````
{
 "command": "ls -la .venv/bin/python 2>&1; .venv/bin/python --version; M=.claude/agent-memory/staff-engineer-reviewer; grep -il \"venv\\|ZLAYT_DB\\|archive\\|port\" $M/*.md | head; echo ---; grep -h -i \"gotcha\\|env\\|port\\|venv\\|PYTHON\" $M/project_harness_review_patterns.md $M/project_e2e_contract_review_patterns.md $M/project_eval_runner_review_patterns.md | head -30; echo ---; cat $M/feedback_shared_scratchpad.md | sed -n '1,30p'",
 "description": "Check venv and recall reviewer environment gotchas from memory"
}
````

### User / tool · 2026-11-02T10:14:17.547Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:22.774Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; cd $R && ls tests/e2e | head -40; echo ---; sed -n '1,60p' tests/e2e/conftest.py; echo ---; grep -n -i \"uvicorn\\|python -m app\\|serve\\|8000\\|7860\\|port\" docs/RUNBOOK.md | head -20; ls app | head -30",
 "description": "Inspect e2e conftest and how to start the app server"
}
````

### User / tool · 2026-11-02T10:14:22.886Z

**tool result**
````
__init__.py
conftest.py
test_adversarial.py
test_api.py
test_change_the_quote.py
test_charges.py
test_code_check_refusal.py
test_edit.py
test_export_ui.py
test_flags_panel.py
test_input.py
test_keyboard_mobile.py
test_ladder_gate.py
test_letter_isolation.py
test_local_mode.py
test_rerun_judge.py
test_review_matrix.py
test_side_by_side.py
test_source_record.py
test_stepper.py
test_suggestions.py
test_timeline.py
---
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
T-046 (R-ST-1 side-by-side): sbs-pane (aside beside the queue at >= 1024 px, not rendered below), sbs-body (scrollable record text, focus with p, Esc returns to the row), sbs-record (one per record shown, data-record-id), sbs-highlight (the excerpt mark; equals the item's excerpt), sbs-highlight-missing (role=alert when the offset cannot be found), sbs-title, sbs-empty, sbs-flags (line in the pane naming the flags on the shown record), sbs-show-flag (button in the pane that jumps to a flag on the record). Keys: p = focus the record pane. The Open record button and o still open the record-modal at every width.
T-096 (suggestions and confidence): btn-confirm-date (the explicit Confirm click of a date form: radios carry testid confirm-date + data-date, the suggested one is pre-checked and followed by date-suggested-tag 'Suggested · MM/DD'; date-suggestion-reason holds the backend reason under it; with no usable suggestion the readings stay one-click confirm-date buttons),
  dismissal-suggestions (box at the top of the flags panel) holding dismissal-suggestion (one per suggestion, data-key) with dismissal-message (the server's sentence verbatim), btn-hide-similar (the only call to POST .../dismissal_suggestions/apply), btn-keep-showing (client-side only) and dismissal-error (role=alert),
  calibration-line (section in the review view; data-status = ok|missing|invalid|error) holding calibration-verified and calibration-needs-review (the backend's sentences verbatim, never a percentage), calibration-stale (role=note, only when calibration.stale: 'These numbers come from an older version of the AI prompts.' plus stale_reason; the line also carries data-stale), calibration-small-sample (only when small_sample) or calibration-unavailable (plain words when the file is missing or invalid or the request fails),
  data-category = the flag category on flag containers (e.g. date_ambiguous); overlap-warning (section beside the accepted total in charges-panel) with overlap-item (data-statement-amount, data-covered-amount = amount ids), overlap-message (the fixed sentence from totals.possible_overlaps), overlap-in-total, btn-overlap-goto (jumps to an amount row), btn-overlap-record,
  tray-item (one per could-not-verify item, data-item-id) carries data-tray-kind = entry|flag; a flag tray item holds tray-flag-lead ('AI suggested a flag that the second check did not confirm; it is not in the letter.'), tray-why and tray-attempt; entry items keep tray-reason; manual-no-sentences (manual-entry form: 'This record has no sentences to pick from.' plus the record's sentences_reason).
T-060 (enterprise polish; keyboard, tokens, layout): SHORTCUTS ACT ONLY FROM AN ITEM ROW (WCAG 2.1.4): j, k, a, d, e, r, o, p, ? and Shift+A do nothing while focus is on Export, the header, a dialog, a text field or the page body; j and k walk ONE list in page order (dates to confirm, timeline rows, tray, flags, charges); a / d (and Enter on Accept / Dismiss) move focus to the next pending item, needs-review ones first, then to Export when none is left.
  Shift+A opens batch-confirm (dialog, title names the count; btn-batch-confirm, btn-batch-cancel; Cancel has focus; Esc cancels); the Accept all verified button (btn-accept-verified) is unchanged and still one step.
  New hooks: skip-nav (nav; the links are skip-dates, skip-suggest, skip-review, skip-flags, skip-charges, skip-export, only those with a target; the first Tab lands on the first of them), app-header (sticky), case-name, case-progress-bar (holds progress-text 'n of N decided' and a progress element), btn-export now lives in app-header (one element), btn-shortcuts and shortcuts-modal (btn-close-shortcuts), btn-theme (cycles auto / light / dark),
  todo-strip ('Open decisions', holds todo-list and one todo-<dates|review|flags|suggest|charges> button per open decision; 'Everything is decided' plus btn-todo-export when none), case-next-action (the case rail's 'What you need to do' line outside the collapsed checks, with btn-show-next-step), gap-change-note (T-114 gap_changes sentences after a date confirm; btn-dismiss-gap-note),
  run-state (while the analysis runs: progress element, plain stage name, skeleton rows; no raw stage names) and btn-retry-run in run-error, tray-notice (a sentence several unclear amounts share, shown once above the unclear table), keys-hint (the one-line keyboard hint in the flags panel).
  Wording: the row's 'Why?' button reads 'Why this status'; the charges 'Accept as noted' button reads 'Keep in notes'; the could-not-verify flag lead is the one sentence 'The AI suggested this flag. The checks did not support it, so it is left out of the letter.' for both reasons (tray-flag-lead), with tray-why inside a closed 'Why the checks left it out' disclosure.
Optional test hook: window.__debugInjectRecordHtml(str) renders str into the record modal through the normal text path (used to prove textContent).
"""
import json, os, urllib.request, urllib.error
import pytest

BASE = os.environ.get("E2E_BASE_URL", "http://localhost:7860")
SAMPLE_PATH = os.path.join(os.path.dirname(__file__), "..", "..", "evals", "golden")

def _up():
---
8:| App (tailnet) | https://<redacted-private>:7860 | live (dev build, cached demo from curated fixtures); restart with `./tools/serve_app.sh` |
9:| App (local) | http://localhost:7860 | `./tools/serve_app.sh` (tmux window `app`, fixture backend, curated set); `LLM_BACKEND=claude-cli ./tools/serve_app.sh` for live model calls |
11:Ports differ from the contract's 443/8443 on purpose: your tailnet already maps 443 → 127.0.0.1:4173 and 8443/10000 → 127.0.0.1:8787.
12:We restored those and gave the board and app their own ports so nothing of yours was clobbered.
26:2. Board server: `./tools/serve_board.sh` (also installs the native git pre-commit secret scan if missing) (tmux session `zlayt`, window `board`). Check: `curl -s localhost:7777/healthz`.
32:5. Tailnet exposure persists across restarts (`tailscale serve status`). If missing: `tailscale serve --bg --https=7777 http://127.0.0.1:7777`.
README-arch.md
__init__.py
backend
db
frontend
llm
main.py
pipeline.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:25.940Z

**tool call — Bash**
````
{
 "command": "cat tools/serve_app.sh; echo ---; R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; sed -n '60,90p' $R/tests/e2e/conftest.py; echo ---; grep -n \"ZLAYT_DB\\|ZLAYT_MODE\\|environ\" $R/app/config.py $R/app/main.py 2>/dev/null | head -20",
 "description": "Read app launch script and e2e conftest server checks"
}
````

### User / tool · 2026-11-02T10:14:26.043Z

**tool result**
````
#!/bin/sh
# Start (or restart) the prototype on :7860 in tmux (window "app"). Dev default: fixture backend, curated set (D-029).
cd "$(dirname "$0")/.." || exit 1
tmux has-session -t zlayt 2>/dev/null || tmux new-session -d -s zlayt -n shell
tmux kill-window -t zlayt:app 2>/dev/null
tmux new-window -d -t zlayt -n app "LLM_BACKEND=${LLM_BACKEND:-fixture} FIXTURE_SET=${FIXTURE_SET:-curated} ZLAYT_DB=${ZLAYT_DB:-artifacts/tmp/app.sqlite3} .venv/bin/python -m app.main >> artifacts/tmp/app.log 2>&1"
sleep 2
curl -fsS -o /dev/null -w "app http %{http_code} on :7860\n" http://127.0.0.1:7860/
---
def _up():
    try:
        urllib.request.urlopen(BASE + "/api/health", timeout=2).read()
        return True
    except Exception:
        return False

def pytest_collection_modifyitems(config, items):
    if _up():
        return
    skip = pytest.mark.skip(reason=f"app server not running at {BASE} (M3 UI/backend not built yet; start `make run` with LLM_BACKEND=fixture)")
    for it in items:
        if "tests/e2e" in str(it.fspath).replace("\\", "/"):
            it.add_marker(skip)

def api(method, path, body=None):
    req = urllib.request.Request(BASE + path, method=method, data=(json.dumps(body).encode() if body is not None else None), headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=60) as r:
            raw = r.read()
            return r.status, (json.loads(raw) if raw else None)
    except urllib.error.HTTPError as e:
        raw = e.read()
        return e.code, (json.loads(raw) if raw else None)

def golden_text(name):
    return open(os.path.join(SAMPLE_PATH, name)).read()

@pytest.fixture
def base_url():
    return BASE
---
14:    uvicorn.run(create(), host=os.environ.get("HOST", "127.0.0.1"), port=int(os.environ.get("PORT", "7860")), access_log=False, log_level="warning")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:33.333Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; cd $R && env -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=fixture ENABLE_LIVE=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q -p no:cacheprovider 2>&1 | tail -15; echo \"PYTEST_RC=${PIPESTATUS[0]}\"; echo ---; env -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=fixture ENABLE_LIVE=0 /Users/arsis/zlayt-pm-project/.venv/bin/python tests/fixtures/make_curated.py --check 2>&1 | tail -8; echo \"CHECK_RC=${PIPESTATUS[0]}\"",
 "description": "Run curated-fixture unit tests and make_curated --check on archive",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T10:14:34.728Z

**tool result**
````
......                                                                   [100%]
6 passed in 0.55s
PYTEST_RC=0
---
entries: 9 non-verified: []
narrative: 9 sentences, removed: []
letter equal: True | notes equal: True
CHECK_RC=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:46.347Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R && cp -R tree mut_shadow && cp tree/tests/fixtures/llm/0ec6b54252d87fcd2eba19570d54c548a95e06668c89582af6b88e6c7daabb1e.json mut_shadow/tests/fixtures/llm/curated/0ec6b54252d87fcd2eba19570d54c548a95e06668c89582af6b88e6c7daabb1e.json && cd mut_shadow && env -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=fixture ENABLE_LIVE=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q -p no:cacheprovider 2>&1 | grep -E \"passed|failed|SHADOWS|SCRIPTED|Error|assert\" | head -20; echo \"MUT_SHADOW_RC=${PIPESTATUS[0]}\"; echo ---; cd $R && cp -R tree mut_scripted && cp tree/tests/fixtures/llm/0ec6b54252d87fcd2eba19570d54c548a95e06668c89582af6b88e6c7daabb1e.json mut_scripted/tests/fixtures/llm/curated/ffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffffff.json && cd mut_scripted && env -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=fixture ENABLE_LIVE=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q -p no:cacheprovider 2>&1 | grep -E \"passed|failed|SHADOWS|SCRIPTED\" | head -20; echo \"MUT_SCRIPTED_RC=${PIPESTATUS[0]}\"",
 "description": "Mutate scratch copies: shadow a recording and add scripted judge, run guard test",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T10:14:49.841Z

**tool result**
````
        assert CURATED.is_dir() and any(CURATED.glob("*.json"))
>       assert judge_problems(CURATED, RECORDED, JUDGE_ALLOW_LIST) == []
E       AssertionError: assert ['SHADOWS_REC...model answer'] == []
E         Left contains one more item: 'SHADOWS_RECORDING 0ec6b54252d8: curated judge answer overrides the recorded model answer'
tests/unit/test_curated_fixtures.py:55: AssertionError
1 failed, 5 passed in 0.66s
MUT_SHADOW_RC=1
---
E       AssertionError: assert ['SCRIPTED_JU...e allow-list'] == []
E         Left contains one more item: 'SCRIPTED_JUDGE ffffffffffff: curated judge answer with no recorded counterpart and not on the allow-list'
1 failed, 5 passed in 0.63s
MUT_SCRIPTED_RC=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:14:59.163Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; lsof -nP -iTCP:7981 -sTCP:LISTEN; echo \"port check rc=$?\"; cd $R/tree && (env LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB=$R/zlayt_e2e.sqlite3 HOST=127.0.0.1 PORT=7981 /Users/arsis/zlayt-pm-project/.venv/bin/python -m app.main > $R/server_7981.log 2>&1 & echo $! > $R/server_7981.pid); sleep 4; cat $R/server_7981.pid; curl -s -o /dev/null -w \"health http %{http_code}\\n\" http://127.0.0.1:7981/api/health; lsof -nP -iTCP:7981 -sTCP:LISTEN",
 "description": "Start fixture server from archive on spare port 7981"
}
````

### User / tool · 2026-11-02T10:15:03.480Z

**tool result**
````
port check rc=1
97679
health http 200
COMMAND   PID  USER   FD   TYPE             DEVICE SIZE/OFF NODE NAME
Python  97679 arsis    9u  IPv4 0xf3ccae30ea73370c      0t0  TCP 127.0.0.1:7981 (LISTEN)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:15:08.856Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R/tree && env E2E_BASE_URL=http://127.0.0.1:7981 ZLAYT_DB=$R/zlayt_e2e.sqlite3 ZLAYT_MODE=local LLM_BACKEND=fixture FIXTURE_SET=curated /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/e2e -q -p no:cacheprovider -rxXs 2>&1 | tail -40 > $R/e2e_r2_summary.txt; cat $R/e2e_r2_summary.txt",
 "description": "Run full tests/e2e against scratch fixture server on 7981",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T10:18:59.257Z

**tool result**
````
........................................................................ [ 41%]
......s.............................................................x... [ 82%]
..............................                                           [100%]
=========================== short test summary info ============================
XFAIL tests/e2e/test_stepper.py::test_judge_panel_one_row_per_item_with_record_cue - T-117: judge row for a tray flag (f_r5_1) shows the raw id and no record cue
SKIPPED [1] tests/e2e/test_ladder_gate.py:37: no rejected item in the sample fixture run
172 passed, 1 skipped, 1 xfailed in 230.06s (0:03:50)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:06.350Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; echo \"server log lines: $(wc -l < $R/server_7981.log)\"; grep -i -c \"miss\\|error\\|traceback\\|JUDGE_\" $R/server_7981.log; grep -i \"miss\\|traceback\\|JUDGE_\" $R/server_7981.log | head -5; echo ---; ls $R/tree/evals/library | head -30; ls $R/tree/evals/library | wc -l; echo ---; grep -rn \"library\" $R/tree/evals/*.py 2>/dev/null | head -5; grep -rln \"FixtureMiss\" $R/tree/app | head",
 "description": "Check server log for fixture misses and list library packets"
}
````

### User / tool · 2026-11-02T10:19:06.474Z

**tool result**
````
server log lines:       46
20
---
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
case_lib08_second_crash_mri_after.expected.json
case_lib08_second_crash_mri_after.txt
case_lib09_spanish_interpreter_espalda.expected.json
case_lib09_spanish_interpreter_espalda.txt
case_lib10_eob_ub04_cms1500.expected.json
case_lib10_eob_ub04_cms1500.txt
case_lib11_priors_and_ledger.expected.json
case_lib11_priors_and_ledger.txt
case_lib12_records_review_credibility.expected.json
case_lib12_records_review_credibility.txt
case_lib13_cloned_notes_cross_provider.expected.json
case_lib13_cloned_notes_cross_provider.txt
case_lib14_handwritten_chiro_scans.expected.json
case_lib14_handwritten_chiro_scans.txt
case_lib15_conclusory_letter_mist.expected.json
case_lib15_conclusory_letter_mist.txt
      30
---
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/evals/library_report.py:2:"""Library report (T-079): scores every evals/library packet with evals.run's scoring functions. REPORTED, NOT GATED (D-031): no exit code
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/evals/library_report.py:5:Run:  .venv/bin/python -m evals.library_report [--out evals/reports/library-latest.md]     (fixture backend; no network)
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/evals/library_report.py:17:LIB = R.ROOT / "evals" / "library"
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/evals/library_report.py:46:    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/evals/library_report.py:47:    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/llm/_types.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/llm/backends/fixture.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/llm/audited.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/llm/provider.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/llm/record.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/backend/split_llm.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/backend/generator.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/backend/judge_guard.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/backend/rejudge.py
/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/app/backend/flags.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:13.808Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R/tree; grep -n \"JUDGE_\\|miss\\|Miss\\|Traceback\\|rror\" $R/server_7981.log | cut -c1-220 | head -20; echo ---; sed -n '1,12p' evals/library_report.py | cut -c1-240; echo ...; sed -n '40,70p' evals/library_report.py | cut -c1-200; echo ---; grep -n \"_fixture\\|def complete_with_meta\\|def prompt_hash\" app/llm/provider.py | head",
 "description": "Inspect server log matches and library report and provider hooks"
}
````

### User / tool · 2026-11-02T10:19:13.925Z

**tool result**
````
3:unhandled TypeError
4:unhandled TypeError
5:unhandled TypeError
10:unhandled TypeError
13:unhandled AttributeError
16:unhandled TypeError
18:unhandled TypeError
19:unhandled TypeError
20:unhandled TypeError
21:unhandled TypeError
35:unhandled TypeError
36:unhandled TypeError
37:unhandled AttributeError
38:unhandled AttributeError
39:unhandled TypeError
40:unhandled TypeError
41:unhandled TypeError
42:unhandled TypeError
43:unhandled AttributeError
46:unhandled AttributeError
---
#!/usr/bin/env python3
"""Library report (T-079): scores every evals/library packet with evals.run's scoring functions. REPORTED, NOT GATED (D-031): no exit code
depends on a score; the ship bar (evals.run) still measures only evals/golden. It only exits non-zero when a packet cannot be run at all.

Run:  .venv/bin/python -m evals.library_report [--out evals/reports/library-latest.md]     (fixture backend; no network)
Honest failures are shown, not hidden: a record whose extract call has no recorded fixture shows as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS),
the same rule as lib01.
"""
import argparse
import json
import pathlib
import subprocess
...
    sha = _git("rev-parse", "HEAD") or "unknown"
    dirty = [l for l in _git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
    return sha, ("clean" if not dirty and sha != "unknown" else f"DIRTY ({len(dirty)} tracked paths differ)" if dirty else "unknown")


def main(argv=None):
    ap = argparse.ArgumentParser(prog="python -m evals.library_report")
    ap.add_argument("--out", default=str(R.ROOT / "evals" / "reports" / "library-latest.md"))
    a = ap.parse_args(argv)
    pipeline = R.load_pipeline()
    rows = []
    for p in sorted(LIB.glob("case_*.txt")):
        rows.append(score(p.stem, p.read_text(), json.loads(p.with_name(p.stem + ".expected.json").read_text()), pipeline))
    sha, state = provenance()
    lines = ["# Library report (reported, not gated)", "", f"Source commit: {sha} (tree: {state}). Regenerate from a clean worktree of the commit you cite.", "",
             "Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.", "",
             "| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |",
             "|---|---|---|---|---|---|---|---|---|---|"]
    for r in rows:
        lines.append(f"| {r['case']} | {r['status']} | {r['entries']} | {r['amounts']} | {r['total_ok']} | {r['must_flags']} | {r['must_not_flag_hits']} | "
                     f"{', '.join(r['must_not_hits']) or '-'} | {r['gap_rows_wrong']} | {'; '.join(f'{c} r{n} {k}' for c, n, k in r['errors']) or '-'} |")
    lines += ["", "## Known honest failures (generated from the run above)", ""]
    fails = [(r["case"], c, n, k) for r in rows for c, n, k in r["errors"]]
    if fails:
        lines += ["| packet | record | code | cause |", "|---|---|---|---|"] + [f"| {p} | r{n} | {c} | {k or 'not captured'} |" for p, c, n, k in fails]
    else:
        lines += ["None at this commit: every record of every packet replays from a recorded fixture on the fixture backend."]
    lines += ["", "History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt "
              "in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract "
              "(T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call)."]
    pathlib.Path(a.out).write_text("\n".join(lines) + "\n")
---
16:from app.llm.backends import fixture as _fixture
33:def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
92:def complete_with_meta(model: str, system: str, user: str, json_schema: dict) -> LLMResult:
96:        res = _fixture.call(model, system, user, json_schema, key=key)
109:        _fixture.write(key, res, model)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:18.966Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cut -c1-260 $R/server_7981.log | head -30; echo ---; cd $R/tree && grep -rn \"unhandled\" app/*.py app/backend/*.py | head -5",
 "description": "View server log lines and the source of unhandled-error logging"
}
````

### User / tool · 2026-11-02T10:19:19.061Z

**tool result**
````
llm call failed call_id=c9fa24f987c72 step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
llm call failed call_id=cbfaf719a36b0 step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
unhandled TypeError
unhandled TypeError
unhandled TypeError
llm call failed call_id=caddf89f488bc step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
llm call failed call_id=c9019a52e7acd step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
llm call failed call_id=cd455156b40cf step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
llm call failed call_id=c3e5c68c7239a step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
unhandled TypeError
llm call failed call_id=cf3b82329912a step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
llm call failed call_id=cf92d8d8aba06 step=j1 attempt=1 prompt_hash=eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838
unhandled AttributeError
llm call failed call_id=c242a02ecf712 step=j1 attempt=1 prompt_hash=578fe6427cf41dd5f33cbb97b1ba07377ecdb4ad987799823b20541bb6aaff1f
llm call failed call_id=cbbb4e4beb08c step=j1 attempt=1 prompt_hash=f310eaa2fa506ae1570a3f90f84e5c0a31c4327897934196ca872813877bc76d
unhandled TypeError
llm call failed call_id=c9109e3755494 step=j1 attempt=1 prompt_hash=15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7
unhandled TypeError
unhandled TypeError
unhandled TypeError
unhandled TypeError
llm call failed call_id=c67f41da00896 step=j1 attempt=1 prompt_hash=0ca727803e287e0c04529fcd34aff4deecca32a7a4def2ad54fd40e60f631a07
llm call failed call_id=cf18c7cf0b54a step=j1 attempt=1 prompt_hash=6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6
llm call failed call_id=c2eccc100bfa3 step=j1 attempt=1 prompt_hash=b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845
llm call failed call_id=c9ff74cff61e5 step=j1 attempt=1 prompt_hash=6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6
llm call failed call_id=c5fdba7ec21fd step=j1 attempt=1 prompt_hash=b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845
llm call failed call_id=c4dafbfb0605b step=j1 attempt=1 prompt_hash=6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6
llm call failed call_id=c4a51833eb5f0 step=j1 attempt=1 prompt_hash=b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845
llm call failed call_id=cf9c8941085f7 step=j1 attempt=1 prompt_hash=6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6
llm call failed call_id=c676924da258c step=j1 attempt=1 prompt_hash=b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845
---
app/backend/api.py:162:        log.error("unhandled %s", type(e).__name__)
app/backend/api.py:184:            log.error("unhandled %s", type(e).__name__)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:25.432Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R/tree; for h in $(grep -o 'prompt_hash=[0-9a-f]*' $R/server_7981.log | sed 's/prompt_hash=//' | sort | uniq -c | sort -rn | awk '{print $2}'); do echo \"$h top=$(ls tests/fixtures/llm/$h.json 2>/dev/null | wc -l) curated=$(ls tests/fixtures/llm/curated/$h.json 2>/dev/null | wc -l) count=$(grep -c \"prompt_hash=$h\" $R/server_7981.log)\"; done; echo ---; grep -rn \"llm call failed\" app | head -3; echo ---; grep -rln \"FIXTURE_MISS\\|FixtureMiss\\|JUDGE_NOT_RUN\" tests/e2e tests/unit | head",
 "description": "Check whether server-log judge hashes resolve to recordings"
}
````

### User / tool · 2026-11-02T10:19:25.685Z

**tool result**
````
eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838 top=       0 curated=       0 count=8
b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845 top=       0 curated=       0 count=5
6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6 top=       0 curated=       0 count=5
83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557 top=       0 curated=       0 count=2
f310eaa2fa506ae1570a3f90f84e5c0a31c4327897934196ca872813877bc76d top=       0 curated=       0 count=1
dd1801ea53c2beb6e4eef91c31a58f9017fecb893fd495d69af97752907df01c top=       0 curated=       0 count=1
af66e649b0823c5c32e167709dddd1835bb0d641f39084a44d517d3995665fa8 top=       0 curated=       0 count=1
578fe6427cf41dd5f33cbb97b1ba07377ecdb4ad987799823b20541bb6aaff1f top=       0 curated=       0 count=1
15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7 top=       0 curated=       0 count=1
0ca727803e287e0c04529fcd34aff4deecca32a7a4def2ad54fd40e60f631a07 top=       0 curated=       0 count=1
---
app/llm/audited.py:110:        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
---
tests/e2e/conftest.py
tests/e2e/test_rerun_judge.py
tests/unit/test_generator.py
tests/unit/test_audited.py
tests/unit/test_judge_guard.py
tests/unit/test_provider.py
tests/unit/test_t037_backend.py
tests/unit/test_provider_backends.py
tests/unit/test_trace.py
tests/unit/test_lib09_t110.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:31.722Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; grep -n \"FIXTURE\\|FixtureMiss\\|JUDGE_NOT_RUN\\|FIXTURE_MISS\\|LLM_FIXTURE_DIR\\|unlink\\|remove\" tests/e2e/test_rerun_judge.py tests/e2e/conftest.py | cut -c1-230 | head -30",
 "description": "Find which e2e tests deliberately trigger judge fixture misses"
}
````

### User / tool · 2026-11-02T10:19:31.811Z

**tool result**
````
tests/e2e/test_rerun_judge.py:63:# ---- D-044: the rerun button wherever a JUDGE_NOT_RUN blocker or step appears
tests/e2e/test_rerun_judge.py:171:# ---- gate blockers: jump and update (moved here from test_stepper, now that only JUDGE_NOT_RUN items block)
tests/e2e/conftest.py:1:"""E2E harness (qa, T-039). Playwright from .venv against http://localhost:7860 with the FIXTURE backend (LLM_BACKEND=fixture; no key, no network).
tests/e2e/conftest.py:22:T-081/T-082 round 3 (D-044/D-045): btn-rerun-judge ('Run the second check again'; aria-busy and disabled while it runs; in the case rail gate and judges steps, each JUDGE_NOT_RUN gate-blocker row, the item
tests/e2e/conftest.py:25:  judge-rerun-group holds ONE btn-rerun-judge ('...for these N' / '...for this item') and its rerun-status, and the AI-check rows have no rerun button of their own; the panel's 'blocks export' wording foll
tests/e2e/conftest.py:189:    the real case right now (so dismissing one removes it, like the real gate). hold=True keeps the rejudge request open until release() so a test can see the busy state.
tests/e2e/conftest.py:217:        return [{"item_id": i, "kind": "entry", "reason_code": "JUDGE_NOT_RUN", "why": self.WHY, "next_action": self._na(i)} for i in self.active()]
tests/e2e/conftest.py:224:            g.update(status="fail", ready=False, reason_code="JUDGE_NOT_RUN", why=f"{n} accepted items have not been double-checked by the second AI check, so the export is blocked. Run the second check a
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:19:49.323Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cat > $R/judge_demand.py <<'EOF'\n\"\"\"Wrap the fixture backend call; count every replayed call by kind (judge = schema has verdict) and by the file that answered it.\"\"\"\nimport collections, json, os, pathlib, sys\nroot = pathlib.Path(sys.argv[1]); out = sys.argv[2]\nsys.path.insert(0, str(root))\nos.environ[\"LLM_BACKEND\"] = \"fixture\"; os.environ[\"FIXTURE_SET\"] = \"curated\"; os.environ.pop(\"LLM_FIXTURE_DIR\", None)\nfrom app.llm.backends import fixture as F\nseen = collections.Counter(); misses = []\norig = F.call\ndef wrapped(model, system, user, json_schema, *, key):\n    kind = \"judge\" if \"verdict\" in json_schema.get(\"properties\", {}) else \"gen\"\n    try:\n        r = orig(model, system, user, json_schema, key=key)\n    except Exception as e:\n        misses.append((kind, key[:12], type(e).__name__)); seen[(kind, \"MISS\")] += 1; raise\n    src = \"curated\" if (F.fixture_dir() / f\"{key}.json\").is_file() else \"recorded\"\n    seen[(kind, src)] += 1\n    if kind == \"judge\" and src == \"curated\":\n        print(\"CURATED_JUDGE_ANSWER\", key[:12])\n    return r\nF.call = wrapped\nimport evals.library_report as LR\nLR.main([\"--out\", out])\nprint(\"CALLS\", dict(seen))\nprint(\"MISSES\", len(misses), misses[:12])\nEOF\ncd $R/tree && /Users/arsis/zlayt-pm-project/.venv/bin/python -I $R/judge_demand.py $R/tree $R/library_report_head.md 2>&1 | tail -8; echo \"RC=${PIPESTATUS[0]}\"; echo ---; sed -n '1,30p' $R/library_report_head.md | cut -c1-200",
 "description": "Run library packets on fixture backend and count judge replays by source",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T10:19:50.750Z

**tool result**
````
| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |

History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt in the first recording pass failed (lib09 r2: INVALID_JSON twice; the other two: cause not captured). In round 2 the Spanish extract (T-085) re-recorded lib09 r2, and lib10 r6 / lib15 r7 were re-recorded with `--fill-missing` from a clean worktree (one pass, at most 3 attempts per call).
CALLS {('gen', 'MISS'): 1, ('gen', 'recorded'): 239, ('judge', 'recorded'): 244}
MISSES 1 [('gen', '83bcee077841', 'FixtureMissing')]
RC=0
---
# Library report (reported, not gated)

Source commit: unknown (tree: unknown). Regenerate from a clean worktree of the commit you cite.

Fixture backend. Scored with evals.run's matchers; packets are NOT part of the ship bar.

| packet | status | entries | amounts | total ok | must flags | must_not_flag hits | must_not hits | gap rows wrong | errors |
|---|---|---|---|---|---|---|---|---|---|
| case_lib01_er_only_then_gap | done_with_errors | 5/6 | 2/2 | True | 1/1 | 0 | - | 0 | LLM_FAILED_AFTER_RETRIES r3 FIXTURE_MISS |
| case_lib02_slip_fall_prior_knee | done | 6/7 | 3/3 | True | 4/4 | 0 | - | 0 | - |
| case_lib03_truck_rear_end_chiro | done | 7/7 | 3/3 | True | 3/3 | 0 | - | 0 | - |
| case_lib04_dog_bite_scar_revision | done | 6/6 | 2/3 | False | 2/2 | 0 | M4 | 0 | - |
| case_lib05_pedestrian_orif_hardware | done | 7/8 | 2/3 | False | 3/3 | 0 | - | 0 | - |
| case_lib06_lop_billed_vs_adjusted | done | 6/7 | 3/7 | False | 2/2 | 0 | M3 | 0 | - |
| case_lib07_parking_lot_fall_outside_records | done | 7/7 | 2/2 | True | 5/5 | 0 | - | 0 | - |
| case_lib08_second_crash_mri_after | done | 12/12 | 4/4 | True | 1/3 | 0 | - | 0 | - |
| case_lib09_spanish_interpreter_espalda | done | 4/7 | 3/5 | False | 1/2 | 0 | M5 | 0 | - |
| case_lib10_eob_ub04_cms1500 | done | 6/9 | 5/9 | False | 1/1 | 0 | M1 | 0 | - |
| case_lib11_priors_and_ledger | done | 4/9 | 4/8 | False | 3/4 | 0 | M1 | 0 | - |
| case_lib12_records_review_credibility | done | 8/10 | 5/5 | True | 6/6 | 0 | - | 0 | - |
| case_lib13_cloned_notes_cross_provider | done | 5/9 | 3/3 | True | 1/3 | 0 | - | 0 | - |
| case_lib14_handwritten_chiro_scans | done | 6/8 | 3/5 | False | 0/0 | 0 | M2 | 0 | - |
| case_lib15_conclusory_letter_mist | done | 4/8 | 4/7 | False | 1/3 | 0 | M4 | 0 | - |

## Known honest failures (generated from the run above)

| packet | record | code | cause |
|---|---|---|---|
| case_lib01_er_only_then_gap | r3 | LLM_FAILED_AFTER_RETRIES | FIXTURE_MISS |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:20:02.916Z

**tool call — Bash**
````
{
 "command": "git show --name-status --format= 08c921e | awk '$1==\"D\"{print $2}' > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/deleted28.txt; R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; wc -l < $R/deleted28.txt; for h in eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838 b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845 6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557 f310eaa2fa506ae1570a3f90f84e5c0a31c4327897934196ca872813877bc76d dd1801ea53c2beb6e4eef91c31a58f9017fecb893fd495d69af97752907df01c af66e649b0823c5c32e167709dddd1835bb0d641f39084a44d517d3995665fa8 578fe6427cf41dd5f33cbb97b1ba07377ecdb4ad987799823b20541bb6aaff1f 15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7 0ca727803e287e0c04529fcd34aff4deecca32a7a4def2ad54fd40e60f631a07; do in_parent=$(git -C /Users/arsis/zlayt-pm-project cat-file -e 08c921e^:tests/fixtures/llm/curated/$h.json 2>/dev/null && echo yes || echo no); in_del=$(grep -c \"$h\" $R/deleted28.txt); echo \"$h parent_curated=$in_parent deleted_by_commit=$in_del\"; done",
 "description": "Check whether the missing judge keys were in the curated set before the commit"
}
````

### User / tool · 2026-11-02T10:20:02.976Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: unresolved variable or substitution in command position ($h) | command: git show --name-status --format= 08c921e | awk '$1=="D"{print $2}' > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cf
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:20:09.866Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd /Users/arsis/zlayt-pm-project && git show --name-status --format= 08c921e | awk '$1==\"D\"{print $2}' > $R/deleted28.txt; cat > $R/check_missing.py <<'EOF'\nimport subprocess, sys, pathlib\nR = pathlib.Path(sys.argv[1])\nrepo = \"/Users/arsis/zlayt-pm-project\"\ndeleted = set(pathlib.Path(p).name for p in (R / \"deleted28.txt\").read_text().split())\nhashes = \"\"\"eadf559f6dfafc96821aa893eebe1af18c79e352d0e55d276c9e8d3aa39d5838 b51099f4ffa545e5609f3d2882ed0fc4c29ff77ca46267f2e92bcd15c28b5845\n6cf7877754461701e6af2807cb18e4c26e4f5f9231214d1f9584714d314bfbf6 83bcee077841d747f18a09ec211dca19fd26207433389d8e62ea61a4c97c7557\nf310eaa2fa506ae1570a3f90f84e5c0a31c4327897934196ca872813877bc76d dd1801ea53c2beb6e4eef91c31a58f9017fecb893fd495d69af97752907df01c\naf66e649b0823c5c32e167709dddd1835bb0d641f39084a44d517d3995665fa8 578fe6427cf41dd5f33cbb97b1ba07377ecdb4ad987799823b20541bb6aaff1f\n15ef7ce5fc7eb1c89da7d1964813037d2de6a50785f7e9035700c2d9d0ed9df7 0ca727803e287e0c04529fcd34aff4deecca32a7a4def2ad54fd40e60f631a07\"\"\".split()\nfor h in hashes:\n    name = h + \".json\"\n    r = subprocess.run([\"git\", \"-C\", repo, \"cat-file\", \"-e\", f\"08c921e^:tests/fixtures/llm/curated/{name}\"], capture_output=True)\n    parent_curated = r.returncode == 0\n    r2 = subprocess.run([\"git\", \"-C\", repo, \"cat-file\", \"-e\", f\"08c921e^:tests/fixtures/llm/{name}\"], capture_output=True)\n    print(h[:12], \"parent_curated=\" + str(parent_curated), \"parent_recorded=\" + str(r2.returncode == 0), \"deleted_by_commit=\" + str(name in deleted))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $R/check_missing.py $R",
 "description": "Check missing judge keys against parent commit curated and recorded sets"
}
````

### User / tool · 2026-11-02T10:20:10.377Z

**tool result**
````
eadf559f6dfa parent_curated=False parent_recorded=False deleted_by_commit=False
b51099f4ffa5 parent_curated=False parent_recorded=False deleted_by_commit=False
6cf787775446 parent_curated=False parent_recorded=False deleted_by_commit=False
83bcee077841 parent_curated=False parent_recorded=False deleted_by_commit=False
f310eaa2fa50 parent_curated=False parent_recorded=False deleted_by_commit=False
dd1801ea53c2 parent_curated=False parent_recorded=False deleted_by_commit=False
af66e649b082 parent_curated=False parent_recorded=False deleted_by_commit=False
578fe6427cf4 parent_curated=False parent_recorded=False deleted_by_commit=False
15ef7ce5fc7e parent_curated=False parent_recorded=False deleted_by_commit=False
0ca727803e28 parent_curated=False parent_recorded=False deleted_by_commit=False
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:20:27.574Z

**tool call — Bash**
````
{
 "command": "git show 08c921e -- tests/fixtures/make_curated.py | head -90 | cut -c1-210",
 "description": "Show make_curated.py diff in 08c921e"
}
````

### User / tool · 2026-11-02T10:20:27.680Z

**tool result**
````
commit 08c921e878edfb8571e60972bbf5681e16d328fc
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Mon Nov 2 04:12:32 2026 -0600

    feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
    
    Eight fully synthetic packets (second crash before MRI, Spanish interpreter note, UB-04/EOB/CMS-1500 OCR, priors and ledger with LOP,
    pre-suit records review with Waddell lines, cloned ROS, handwritten chiro scans with ambulance invoice, conclusory letter and 18.001
    affidavit), built by evals/library_build_v2.py. 291 claude-cli fixtures; lib09 r2, lib10 r6 and lib15 r7 stay honest
    LLM_FAILED_AFTER_RETRIES (no attempt-1 fixture). evals/library_report.py reports the packets, not gated. Denylist qa-side test.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/tests/fixtures/make_curated.py b/tests/fixtures/make_curated.py
index b2bbf66..a7bb1ae 100644
--- a/tests/fixtures/make_curated.py
+++ b/tests/fixtures/make_curated.py
@@ -1,6 +1,9 @@
 """Builds tests/fixtures/llm/curated/ (D-029, T-051): HAND-CHECKED generator/judge responses that reproduce the golden summaries and
 excerpts. Every answer below is derived from evals/golden (sample.export.expected.txt and sample.expected.json), never from a model.
 Run:  .venv/bin/python tests/fixtures/make_curated.py [--check]
+Judge answers (any schema with a "verdict") are NEVER scripted (T-115 r2, D-029): the build replays the real recorded model answer from
+tests/fixtures/llm/<key>.json and, on a miss, records one live (ENABLE_LIVE=1 LLM_BACKEND=claude-cli, at most 3 attempts). No curated
+judge file is written, so a curated answer can never shadow a recording; the check replays curated first, then the recorded set.
 The script runs the real pipeline on evals/golden/sample.txt with the provider patched to these scripted answers, writes one
 <sha256>.json per distinct prompt (key = provider.prompt_hash), each with a top-level "CURATED" header, then replays the set through the
 real fixture backend and checks the export against evals/golden/sample.export.expected.txt.
@@ -10,6 +13,9 @@ ROOT = pathlib.Path(__file__).resolve().parents[2]
 sys.path.insert(0, str(ROOT))
 os.environ.setdefault("LLM_BACKEND", "fixture")
 OUT = ROOT / "tests" / "fixtures" / "llm" / "curated"
+MAX_LIVE_ATTEMPTS = 3
+import threading
+_LIVE_LOCK = threading.Lock()
 HEADER = ("CURATED: hand-checked response written by qa from evals/golden (summary/quote from sample.export.expected.txt, flag spans from "
           "sample.expected.json). Not a model output. Cached demo only; ship-bar metrics use recorded/live runs (D-029).")
 
@@ -78,7 +84,40 @@ def build():
     for f in OUT.glob("*.json"):
         f.unlink()
     written = {}
+    def judge(model, system, user, schema):
+        """Real model answer for a judge prompt: recorded if present, else live (<= 3 attempts) and recorded to the default dir."""
+        key = P.prompt_hash(model, system, user, schema)
+        try:
+            return P._fixture.call(model, system, user, schema, key=key)
+        except P.FixtureMiss:
+            pass
+        if P.backend_name() == "fixture":
+            raise SystemExit(f"no recorded judge answer for {key[:12]} and no live backend: rerun with ENABLE_LIVE=1 LLM_BACKEND=claude-cli")
+        want = next((x for x in ("supported", "agree", "conflict") if x in (schema["properties"]["verdict"].get("enum") or [])), None)
+        with _LIVE_LOCK:                                      # judges run in threads; record_context and the env flag are process-global
+            try:
+                return P._fixture.call(model, system, user, schema, key=key)     # another thread recorded it meanwhile
+            except P.FixtureMiss:
+                pass
+            os.environ["RECORD_FIXTURES"] = "1"
+            try:
+                for attempt in range(1, MAX_LIVE_ATTEMPTS + 1):
+                    try:
+                        with P.record_context(G.raw("sample")):
+                            res = real(model, system, user, schema)
+                    except Exception as e:                   # backend error / invalid JSON: counts as an attempt
+                        print(f"judge {key[:8]} attempt {attempt}: {type(e).__name__} {e}")
+                        continue
+                    print(f"judge {key[:8]} attempt {attempt}: {res.output['verdict']} {res.output.get('reason_code')} (golden path expects {want})")
+                    if res.output["verdict"] == want:
+                        return res
+                raise SystemExit(f"judge {key[:8]}: no accepted answer in {MAX_LIVE_ATTEMPTS} attempts; last recorded answer stays in tests/fixtures/llm")
+            finally:
+                os.environ.pop("RECORD_FIXTURES", None)
+
     def fake(model, system, user, schema):
+        if "verdict" in schema.get("properties", {}):
+            return judge(model, system, user, schema)
         key = P.prompt_hash(model, system, user, schema)
         out = answer(system, user, schema)
         written[key] = dict(CURATED=HEADER, output=out,
@@ -102,7 +141,9 @@ def build():
 
 def check():
     """Replays through the REAL fixture backend; accepts everything; compares letter_text with the golden file."""
-    os.environ["LLM_FIXTURE_DIR"] = str(OUT)
+    os.environ.pop("LLM_FIXTURE_DIR", None)
+    os.environ["FIXTURE_SET"] = "curated"        # curated first, then the recorded set (judge answers are recordings only)
+    os.environ["LLM_BACKEND"] = "fixture"
     from app.db import db as DB
     from app.backend import pipeline as PL, store, export, review
     from app.llm import audited as AU
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:20:28.791Z

**tool call — Bash**
````
{
 "command": "git log --oneline --diff-filter=A -- evals/library/case_lib08_second_crash_mri_after.txt evals/library_build_v2.py evals/library_report.py | head; echo ---; git ls-tree -r --name-only 08c921e^ -- evals/library | wc -l; git ls-tree -r --name-only HEAD -- evals/library | wc -l; echo ---; git log --oneline -5 -- tests/fixtures/llm/curated | cat; echo ---; git ls-tree --name-only 08c921e^ tests/fixtures/llm/curated/ | wc -l; echo ---; grep -n -i \"curated\" memory/DECISIONS.md memory/ASSUMPTIONS.md memory/SCOPE_CUTS.md memory/LESSONS.md 2>/dev/null | cut -c1-260 | tail -15",
 "description": "Show make_curated diff, library file history, and curated-set decision notes"
}
````

### User / tool · 2026-11-02T10:20:29.094Z

**tool result**
````
328428f feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
---
      30
      30
---
08c921e feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
400a8c0 test(qa): T-115 curated judge fixtures regenerated for judge_flag_v3 (12 e2e failures were fixture drift), judge-row record cue xfail(strict) T-117
a9a27ed fix(backend): conflicts are code-proposed candidates classified by J3 v4; model-only flags the judge rejects are suppressed (T-094, R-CO-7)
3104213 fix(backend): stabilize live 3-run determinism (T-075, R-CO-7)
b9d3ead chore(backend): narrative fixtures for sample and case_01-09 (curated + recorded), make_curated drafts the narrative; A-109
---
      47
---
memory/ASSUMPTIONS.md:23:| A-109 | Library packet case_lib01 record 3 keeps its recorded extract failure (LLM_FAILED_AFTER_RETRIES: the live model answered with two JSON objects on every attempt); we do not harden the extract prompt to hide it. | A real model 
memory/SCOPE_CUTS.md:51:| debt | T-068 accepted with documented debt after 3 rounds (§7.4) | r3 major (confirmed entry still 'Needs review'/'date can be read two ways') is the server leaving DATE_AMBIGUOUS after confirm_date, fixed in T-076 r2. Minors (Edit e
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:20:37.480Z

**tool call — Bash**
````
{
 "command": "git show --stat --format='%h %s' 328428f | tail -3; git merge-base --is-ancestor 328428f 08c921e && echo \"328428f is ancestor of 08c921e\"; git show --name-only --format= 328428f | awk -F/ '{print $1\"/\"$2\"/\"$3}' | sort | uniq -c | sort -rn | head -8; echo ---; git log --oneline 328428f..08c921e | cat; echo ---; git show -s --format='%h %an %ad %s' 328428f | cut -c1-120; git show -s --format='%h %an %ad' 08c921e",
 "description": "Check T-079 commit 328428f contents and ancestry relative to 08c921e"
}
````

### User / tool · 2026-11-02T10:20:37.741Z

**tool result**
````
 ...fab707bc689388d2ffb35c27452986323792b3e0bb.json |  11 +
 tests/unit/test_library_denylist.py                |  54 ++
 313 files changed, 10166 insertions(+)
328428f is ancestor of 08c921e
 291 tests/fixtures/llm
   2 .claude/agent-memory/qa
   1 tests/unit/test_library_denylist.py
   1 evals/reports/library-latest.md
   1 evals/library_report.py/
   1 evals/library_build_v2.py/
   1 evals/library/case_lib15_conclusory_letter_mist.txt
   1 evals/library/case_lib15_conclusory_letter_mist.expected.json
---
08c921e feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)
288affc test(backend): T-113 relabel H3V5 wrong -> correct by the D-046 second-agent ruling (reviews/T-093-staff-engineer-r4.md F1), before any run
6e880e6 test(e2e): T-060 follow-ups - letter keys from an item row, one-sentence tray flag lead, retrying judge-count assert
b89b9d9 docs: D-055 gaps warn on administrative endpoints instead of excluding
9fcae9b feat(frontend): layout polish: open-decisions strip, skip links and Start review, compact rows with captioned quotes and status chips, one-line charges rows, side-by-side flag evidence, processing state with progress, export focus and single primary, cases collapsed, T-096 minors (T-060)
eabe2b8 feat(frontend): one design-token system (tokens.css: palette light+dark, 7-step type scale, spacing, 2 radii, elevation) and every stylesheet rebuilt on it; one button and chip system with hover, active, focus and disabled states; sticky case header (T-060)
78450f6 test(qa): lib11 expected: intake form is not a gap endpoint (T-118, applies T-116 five edits)
ea6ac71 fix(backend): gap exclusion fails safe toward treatment; label head + no treatment evidence required (T-116 r2)
400a8c0 test(qa): T-115 curated judge fixtures regenerated for judge_flag_v3 (12 e2e failures were fixture drift), judge-row record cue xfail(strict) T-117
c1b44be feat(backend): only treatment encounters start or end a gap; excluded records named in the gap's why (T-116)
3e3f3b7 fix(frontend): single-key shortcuts act only from an item row; Shift+A asks first with the count; one linear j/k queue across panels; focus to Accept after a date confirm; gap changes announced (T-060)
b5fb35c feat(backend): a rate is acknowledged, never a JUDGE_NOT_RUN blocker; lib09 rate judge fixtures; confirm_date reports gap_changes (T-114)
36ceb38 feat(frontend): T-096 pre-selected date suggestion, dismissal banner, measured precision (with stale note), overlap warning, flag tray wording
03206ca fix(qa): calibration staleness compares on-disk prompts; score_unsplit replays the whole case
3223e50 test(qa-eval): T-093 r4 live controls from a clean worktree of 822ff38: J4 12/12 incl J4W7 3/3, J3 13/17 (4 false agrees: J3V1, J3V9, J3V13, H3V5), 15/15 correct accepted
afcde06 feat(backend): code removes summary clauses the quote does not support before judging (T-112, D-054)
822ff38 fix(qa-eval): J3 controls rebuilt from pairs conflict_candidates.py proposes (4 real golden candidates plus crafted variants), labels locked with a rationale per item, reachability test (T-093 r4)
276991b feat(backend): GET /api/calibration reports stale when recorded prompt hashes differ from HEAD (T-102)
4bdf366 docs(architect): T-109 r2 LLM_VS_CODE rows 4, 7, 8, 11 and rule 7; ADR-020 (D-042, D-052 to D-054, T-110)
f187a30 docs: D-054 code removes summary clauses the quote does not support
62037fc test(backend): T-094 r2 evidence from a clean worktree of 789cb39: controls_ok True, live 3-run 083252Z and 085207Z ship_bar_met True (081339Z failed on a case_02 judge-unsupported summary)
789cb39 fix(qa-eval): git_source ignores evals/reports when deciding tree cleanliness, so a second run of one commit is not marked DIRTY (T-094 r2)
e8e6955 fix(backend): payment/balance/adjustment/copay wording beats any charge cue (EN+ES), estado de cuenta is context only, Spanish unclear note, recorded judge answer for lib09 consultas (T-110 r3)
d24ff07 fix(backend): Spanish charge/rate/balance cues in the shared cue function, overlap in internal notes, tray placeholder leaves after manual entry, UB-04 room total in other_figures (T-110 r2)
8b54d40 fix(backend): judge_conflict_v5: a denial naming one body part against a different named body part is benign (T-094 r2)
4a560d8 fix(backend): Waddell results flag in every word order; bare N/5 positive flags after a Waddell sentence (T-111 r2, D-043)
8a2b934 fix(backend): billing places tokens by position, not text; exact per-record count holds on 24000 generated records; other_figures filled (T-103 r4)
dda614d fix(backend): rejected model output goes to the could-not-verify tray, conflict candidate rules widened, judge_flag_v3 (T-094 r2, D-053)
3e936a0 feat(backend): failed-extract records are could-not-verify tray items; POSSIBLE_OVERLAP warns beside the charge total (T-110)
013f15b docs(architect): D-053 rows 11-12, tray replaces suppressed flags
99c2b32 fix(backend): single-clause 'Waddell testing not performed/done.' and 'Not tested.' stay silent (D-043, T-111)
8c190e8 docs: D-053 rejected model output goes to the tray, never dropped
a271014 fix(backend): every quote-picker unit saves alone: hedge-qualified sentences are combined units; label-only records offer no units with a reason (T-108 r2)
2ab7896 test(qa): controls evidence from a clean worktree of 9217f8a: J3 17/17, J4 11/12 (J4W7 unstable), controls_ok False (T-093 r3)
81aa55e fix(backend): credibility flag keeps the whole period-sentence excerpt through merge and hedge runs; allow-list is exactly D-043's forms (T-092)
bf0c748 docs(architect): LLM_VS_CODE row 11 code-proposed conflicts; D-047 to D-052 in rows and ADR-019 (T-109)
ce70bd2 chore(evals): regenerate library report from clean HEAD a74b727 (T-079 r2)
a74b727 fix(evals): lib09 counts the consult once (6,390), tolerated billed-without-note, lib10 r6 / lib15 r7 re-recorded, report provenance (T-079 r2)
9217f8a fix(qa): controls gate is every wrong item; arithmetic pairs move to code tests; J3C10 reason and changelog history; report names its source commit (T-093 r3)
a9a27ed fix(backend): conflicts are code-proposed candidates classified by J3 v4; model-only flags the judge rejects are suppressed (T-094, R-CO-7)
e3a62fa fix(backend): pdf_hidden and pdf_ocr allow-list is an AST audit (T-106 round 2)
1526a1f fix(backend): billing never merges lines across records or providers; row money tokens are fields, T-103 r3
9851a0d fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
d3e127c fix(backend): quote picker units come from the quotable body only (T-108)
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
3462ad0 fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
1335f21 fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
2dc5be2 feat(backend): billing ships as a cited line listing, no provider totals or complete flag (T-103, D-052)
841be23 docs: D-052 billing ships as cited line listing without totals (§7.4)
9f2811f fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)
fdc2506 fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)
ae76835 fix(backend): hidden-text scan runs in a child killed at the deadline; Widget/annotation covers, clip windows, low contrast and tiny text held back (T-087 r3)
288c1d3 fix(backend): D-047 r2: attribution, hedge and approximation words the quote lacks are a 422; one wide side/negation vocabulary shared by edit, manual entry, generator and gate (T-100 r2)
690a0e3 fix(backend): billing lists every repeated summary row, skipped records make totals incomplete, BALANCE DUE accepted with or without the forward (D-049, T-083 r5)
b10bff4 fix(backend): non-English is never auto-verified (D-050): AI_TRANSLATION in compose_state; English-dominant lines stay English; Portuguese suspeita/compressao not Spanish; 244-row routing set (T-085 r4)
dd84122 fix(backend): code checks bind accept for every entry, single and batch; gate and trace recompute them from the current text (D-051, T-098 r2)
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
f345bc8 fix(backend): calibration route rejects a hand-edited state total and checks the served labels (T-099 r2)
6bca71e fix(backend): final money-token accounting pass for billing; second balance-forward rows listed, bare figures never vanish (D-049, T-083 r4)
e63e564 docs: D-051 code checks bind accept for every item
a2d4b7c docs: D-050 non-English is never auto-verified (§7.4 after T-085 r3)
32f6c9d test(frontend): WordingFails route stub for the gate's code-check blocker (the edit route now refuses such wording, D-047); inline 422 cases (T-097 r2)
0a6ed4c docs: D-049 billing completeness by token accounting
f5ddec8 fix(frontend): remove the 409 keep-my-wording dialog and its copy now that T-100 landed; refused edits show the 422 reason inline (D-047, T-097 r2)
24c18a7 feat(backend): side/negation/qualifier tokens missing from the quote are a hard 422 on edit and manual entry; 409 keep-my-wording path removed (D-047, T-100)
e7a1987 fix(backend): language routing fails safe (D-048): English only when confidently English, mixed lines run the union of checks, Spanish cue words, 206-line routing set (T-085 r3)
21b6665 fix(frontend): AI-check summary and Why dialog read the gate and trace; failing edited wording is a named blocker with an Edit action; 422 edit reason inline (T-097 r2)
950d4a5 fix(backend): OCR_DERIVED survives edits; OCR render pixel caps and scrubbed tesseract env; hidden-text differential render, fail-closed scan, deadline that stops the worker (T-086 r2, T-087 r2)
db08276 fix(backend): billing lists every amount-bearing row or marks the provider incomplete; pins the prose charge gate (T-083 r3)
3703be4 docs: D-048 fail-safe language routing
196c985 harness: stale-index guard allows partial staging; blocks only re-staged older committed versions
3ecb8b1 feat(backend): GET /api/calibration serves the measured calibration read-only (T-099)
36a982b docs: D-047 side/negation tokens hard 422, drop 409 keep-my-wording path
e511778 fix(backend): export gate blocks human-edited items whose code checks fail (D-045b, T-098)
5b4ccb0 harness: pre-commit blocks stale-index reverts (staged blob matches neither HEAD nor worktree)
9c1af01 fix(backend): restore the T-085 r2 files that 57a08ba reverted by mistake (stale temp index); T-084 r3 change stays
57a08ba fix(backend): reclassify wording gate uses the classifier's rate verdict and the shared rate cues; class-only restore tested (T-084 r3)
1b1c711 fix(backend): language detection fails safe, French/Portuguese refused, CLI crash, 'no se descarta' keeps its meaning, Spanish cue words, Spanish eval pairs (T-085 r2)
172028c chore(evals): regenerate calibration.json from a clean worktree of b85fc1b (T-090 r3)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
8bc7f90 fix(backend): billing never totals per-visit rate rows, lists unparsed CMS-1500/ledger rows as unreconciled, verifier runs on the route, unreadable provider is not $0 (T-083 r2)
31b7ceb docs: revert audit for 328428f..bc12d44
0e30623 fix(frontend): scroll the rerun status line into view beside the pressed button (T-097)
c7ba1f1 fix: restore T-075/T-057 work reverted by 865b186 (prompt-version map: j3 judge_conflict_v2 and the conflicts step; T-085 commit had swept in an uncommitted audited.py edit)
d0b5fd8 test(e2e): declare sbs-flags and sbs-show-flag in the hook contract (T-097)
94edf56 fix(frontend): rerun answer shows beside the pressed button, AI-check panel follows the export gate, edited items shown as not AI-checked (T-097, D-045)
a850be0 fix: restore T-090 work reverted by 2fca530
6feb2ff fix: restore T-095 work reverted by 2fca530
bc12d44 fix(frontend): side-by-side pane floats over the right margin, flag button in the pane, Enter selects, one record heading (T-046 r2)
c8a9874 fix(backend): restore re-runs both checks after a rerun, rate cues decide the wording gate, audited_call retries provider errors only, LLMFailed class recorded (T-084 r2, T-073 r2)
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
d3130e3 harness: git-guard requires subagent commits to use a pathspec or temp index (stale shared index)
55300e9 fix(backend): date suggestion names the record each evidence date sits in; route-level demo-isolation and eligibility tests (T-088, T-089 round 2)
49c4600 memory: T-091 speaker attribution v2 fails fresh adversary; stays cut (D-040)
e2b4e3f fix: restore T-083 billing deleted by ec33bf0
865b186 feat(backend): Spanish-language records with verbatim Spanish quotes and a labelled, judged English translation (T-085, D-042)
02ff244 chore(evals): regenerate calibration.json from a clean worktree of 823b718 (fixture: verified 83/84, needs_review 10/10) (T-090 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
823b718 feat(evals): calibration sentences name backend and golden set, count unscored items, carry source commit and hashes, check-fresh covers calibration.json (T-090 r2)
031a708 feat(db): review_events actions reclassify and rejudge; in-place v3->v4 migration (T-095)
e92b6ed feat(frontend): Run the second check again button, refused export shown beside Export, pending items as a gate warning (T-081 r3, T-082 r3, D-044, D-045)
17cc9c7 feat(backend): speaker attribution v2 behind adversarial eval gate, disabled (T-091)
ec33bf0 feat(backend): guarded charge reclassification by the paralegal (T-084, D-042)
f218263 feat(backend): billing analysis on itemized ledgers, claim forms and EOBs (T-083)
7724412 fix(backend): review.py judge path catches only expected judge errors and keeps the error class (T-073)
e3fc01c harness: board-guard denies pkill/killall for subagents (shared dev servers)
5616dc3 feat(frontend): side-by-side source viewer at >= 1024 px (R-ST-1, T-046)
f667f08 feat(backend): date-convention suggestion (T-088) and dismissal-pattern suggestions (T-089)
---
328428f Chris Borsheim Sun Nov 1 22:21:07 2026 -0600 feat(evals): library packets lib08..lib15 with expected.json, recor
08c921e Chris Borsheim Mon Nov 2 04:12:32 2026 -0600
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:02.237Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R/tree && grep -n '\"verdict\" in props\\|\"verdict\" in schema\\|def answer\\|def fake\\|if \"verdict\"' tests/fixtures/make_curated.py | cut -c1-160; echo ---; cd /Users/arsis/zlayt-pm-project && sed -n '58,62p' tests/e2e/test_side_by_side.py | cut -c1-200; echo ---; grep -n \"inner_text\\|to_have_text\" tests/e2e/test_stepper.py | sed -n '1,12p' | cut -c1-200; echo ---; grep -rn \"judge_flag_v3\\|JUDGE_FLAG\" app/llm/*.py app/backend/*.py 2>/dev/null | head -4 | cut -c1-200",
 "description": "Locate dead verdict branch, check r1 e2e fixes, find judge prompt sources"
}
````

### User / tool · 2026-11-02T10:21:02.351Z

**tool result**
````
44:def answer(system, user, schema):
55:    if "verdict" in props:
118:    def fake(model, system, user, schema):
119:        if "verdict" in schema.get("properties", {}):
---
def test_p_moves_focus_into_pane_and_escape_returns(page, sample_case):
    """Keyboard access: p focuses the scrollable pane, Esc returns to the selected row."""
    open_case(page, sample_case)
    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()      # WCAG 2.1.4: letter keys act only from an item row (T-060)
    page.keyboard.press("p")
---
66:    kinds = {steps.nth(i).get_by_test_id("step-kind").inner_text() for i in range(steps.count())}
71:        assert s.get_by_test_id("step-why").inner_text().strip()
72:        assert s.get_by_test_id("step-status").inner_text().strip() in ("Passed", "Failed", "Skipped", "Not done yet", "Needs your decision", "Blocked")
73:        assert s.get_by_test_id("step-marker").inner_text().strip() in ("✓", "✕", "–", "○")   # glyph plus word, never colour alone
83:    assert "What you need to do" in human.get_by_test_id("step-action").inner_text()
84:    assert human.get_by_test_id("step-status").inner_text() == "Needs your decision"
119:    assert judge.get_by_test_id("step-kind").inner_text() == "AI check"
120:    assert "second ai check said" in judge.get_by_test_id("step-judge-reason").inner_text().lower()
121:    assert "What you need to do" in judge.get_by_test_id("step-action").inner_text()
132:    txt = cs.get_by_test_id("case-summary").inner_text().replace("\n", " ")
146:    assert re.fullmatch(r"\d+/10 checks passed", cs.get_by_test_id("case-summary-progress").inner_text())
149:    assert gate.get_by_test_id("step-status").inner_text() == "Blocked"
---
app/llm/audited.py:124:                  "j4": "judge_flag_v3", "flags": "flags_v1", "split": "split_v1", "narrative": "narrative_v1"}
app/backend/judges.py:64:    return _run("j4", "judge_flag_v3", schemas.Judge4, [excerpt],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:05.814Z

**tool call — Bash**
````
{
 "command": "grep -n \"judge-summary-counts\" tests/e2e/test_stepper.py | cut -c1-220; echo ---; find app -iname \"*judge*\" | grep -v __pycache__ | head; echo ---; sed -n '60,70p' app/backend/judges.py | cut -c1-200; echo ---; grep -n \"def prompt_hash\" -A8 app/llm/provider.py | cut -c1-200",
 "description": "Check judge-count assertions and judge prompt source files"
}
````

### User / tool · 2026-11-02T10:21:05.929Z

**tool result**
````
204:    assert re.search(r"\d+ checked, \d+ agreed with the draft, 3 questioned", jp.get_by_test_id("judge-summary-counts").inner_text())
257:    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"checked \d+, all agreed"))   # counts load after the panel (retrying assert, not a snapshot)
---
app/frontend/judges.js
app/backend/judge_guard.py
app/backend/rejudge.py
app/backend/judges.py
app/llm/prompts/judge_amount_class_v1.md
app/llm/prompts/judge_flag_v1.md
app/llm/prompts/judge_conflict_v6.md
app/llm/prompts/judge_conflict_v2.md
app/llm/prompts/judge_conflict_v4.md
app/llm/prompts/judge_conflict_v5.md
---
                call, nonce, item_id)


def run_j4_meta(excerpt: str, flag_type: str, category: str, *, call, nonce=None, item_id=None):
    return _run("j4", "judge_flag_v3", schemas.Judge4, [excerpt],
                [f"FLAG TYPE: {flag_type}", f"FLAG CATEGORY: {category}"], call, nonce, item_id)


def run_j1(summary, excerpt, label, *, call, nonce=None, item_id=None):
    return run_j1_meta(summary, excerpt, label, call=call, nonce=nonce, item_id=item_id)[0]

---
33:def prompt_hash(model: str, system: str, user: str, json_schema: dict) -> str:
34-    """sha256 over model+system+user+schema (canonical JSON). Any change to any part changes the key."""
35-    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
36-    return hashlib.sha256(blob.encode("utf-8")).hexdigest()
37-
38-
39-def _norm(s: str) -> str:
40-    return re.sub(r"\s+", " ", s).strip()
41-
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:12.777Z

**tool call — Bash**
````
{
 "command": "sed -n '196,206p' tests/e2e/test_stepper.py | cut -c1-230; echo ---; ls app/llm/prompts | grep -i \"judge_flag\"; echo ---; R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R && ls tree/app/llm/prompts | grep -i judge_flag",
 "description": "View judge-count wait context and locate judge_flag prompt file"
}
````

### User / tool · 2026-11-02T10:21:12.881Z

**tool result**
````
# ---- judge panel
def test_judge_panel_collapsed_summary_and_labels(page, judged_case):
    """T-082 r2: one summary row with the counts; closed by default; opening shows the label, models and totals; internals stay in Technical details."""
    open_case(page, judged_case)
    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
    assert jp.locator("details.zj-det").evaluate("d => d.open") is False and jp.bounding_box()["height"] < 120
    assert re.search(r"\d+ checked, \d+ agreed with the draft, 3 questioned", jp.get_by_test_id("judge-summary-counts").inner_text())
    jp = open_judges(page)
    label = jp.get_by_test_id("judge-label").inner_text()
---
judge_flag_v1.md
judge_flag_v2.md
judge_flag_v3.md
---
judge_flag_v1.md
judge_flag_v2.md
judge_flag_v3.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:21.213Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cd $R && cp -R tree mut_prompt && printf '\\nMUTANT: scratch-only prompt edit for the staleness guard check.\\n' >> mut_prompt/app/llm/prompts/judge_flag_v3.md && cd mut_prompt && env -u FIXTURE_SET -u LLM_FIXTURE_DIR LLM_BACKEND=fixture ENABLE_LIVE=0 /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q -p no:cacheprovider 2>&1 | grep -E \"passed|failed|^E .*(letter|check|assert|returncode|JUDGE|entries)\" | cut -c1-240 | head -12; echo \"RC=${PIPESTATUS[0]}\"",
 "description": "Mutate judge_flag_v3 prompt in scratch copy and run staleness unit test",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T10:21:23.071Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:31.217Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; grep -n \"inner_text())$\\|judge-summary-counts\\\").inner_text\" $R/tests/e2e/test_stepper.py | cut -c1-120; grep -n \"focus()      # WCAG\" $R/tests/e2e/test_side_by_side.py | cut -c1-80; echo ---; cd /Users/arsis/zlayt-pm-project && grep -n -i \"curated\\|T-115\" memory/ORCHESTRATOR_DECISIONS.md memory/DECISIONS.md memory/ASSUMPTIONS.md | cut -c1-200 | tail -12; echo ---; ls evals/reports | grep -i controls | tail -4",
 "description": "Verify r1 e2e fixes exist at HEAD and look for curated decision records"
}
````

### User / tool · 2026-11-02T10:21:31.336Z

**tool result**
````
146:    assert re.fullmatch(r"\d+/10 checks passed", cs.get_by_test_id("case-summary-progress").inner_text())
204:    assert re.search(r"\d+ checked, \d+ agreed with the draft, 3 questioned", jp.get_by_test_id("judge-summary-count
211:    assert re.search(r"claude-\S+", jp.get_by_test_id("judge-model-line").inner_text())
61:    page.get_by_test_id("queue").locator("[data-item-id]").first.focus()     
---
memory/ASSUMPTIONS.md:23:| A-109 | Library packet case_lib01 record 3 keeps its recorded extract failure (LLM_FAILED_AFTER_RETRIES: the live model answered with two JSON objects on every attempt); we 
memory/ORCHESTRATOR_DECISIONS.md:37:| D-029 | Two fixture sets: `tests/fixtures/llm/recorded/` (live claude-cli recordings, used by evals to replay real model behaviour) and `tests/fixtures/llm/curate
---
controls-20261102T075238Z.json
controls-20261102T075238Z.md
controls-20261102T090925Z.json
controls-20261102T090925Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:37.710Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cat > $R/parent_judges.py <<'EOF'\nimport json, subprocess, sys, pathlib\nrepo = \"/Users/arsis/zlayt-pm-project\"; R = pathlib.Path(sys.argv[1])\nnames = subprocess.run([\"git\", \"-C\", repo, \"ls-tree\", \"--name-only\", \"08c921e^\", \"tests/fixtures/llm/curated/\"], capture_output=True, text=True).stdout.split()\njudge = gen = deleted_judge = deleted_gen = 0\ndeleted = set(pathlib.Path(p).name for p in (R / \"deleted28.txt\").read_text().split())\nfor path in names:\n    blob = subprocess.run([\"git\", \"-C\", repo, \"show\", f\"08c921e^:{path}\"], capture_output=True, text=True).stdout\n    out = json.loads(blob).get(\"output\", {})\n    is_j = isinstance(out, dict) and \"verdict\" in out\n    name = pathlib.Path(path).name\n    if is_j: judge += 1\n    else: gen += 1\n    if name in deleted:\n        if is_j: deleted_judge += 1\n        else: deleted_gen += 1\nprint(\"parent curated files:\", len(names), \"judge:\", judge, \"gen:\", gen)\nprint(\"deleted by 08c921e:\", len(deleted), \"judge:\", deleted_judge, \"gen:\", deleted_gen)\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $R/parent_judges.py $R; grep -n \"controls_ok\" /Users/arsis/zlayt-pm-project/evals/reports/controls-20261102T090925Z.md | head -2 | cut -c1-160",
 "description": "Confirm the 28 deleted curated files were all judge answers"
}
````

### User / tool · 2026-11-02T10:21:38.674Z

**tool result**
````
parent curated files: 47 judge: 28 gen: 19
deleted by 08c921e: 28 judge: 28 gen: 0
3:**controls_ok: False**  backend `claude-cli`  prompts `judge_conflict_v5`, `judge_flag_v3` (hashes in the json)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:42.377Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; P=$(cat $R/server_7981.pid); ps -p $P -o pid,command | cut -c1-160; kill $P; sleep 2; ps -p $P -o pid= ; echo \"after kill ps rc=$?\"; lsof -nP -iTCP:7981 -sTCP:LISTEN; echo \"lsof rc=$?\"",
 "description": "Stop the scratch fixture server by PID and confirm port closed"
}
````

### User / tool · 2026-11-02T10:21:44.562Z

**tool result**
````
  PID COMMAND
97679 /opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/Resources/Python.app/Contents/MacOS/Python -m app.main
after kill ps rc=1
lsof rc=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:21:56.771Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; sed -n '150,190p' app/backend/api.py | cut -c1-170; echo ---; grep -rn \"500\" tests/e2e/*.py | head -5 | cut -c1-180",
 "description": "Read API unhandled-exception handler and any e2e tests expecting 500"
}
````

### User / tool · 2026-11-02T10:21:56.864Z

**tool result**
````
    @app.exception_handler(review.ReviewError)
    async def _review_error(_, e):
        return JSONResponse({"error": {"code": e.code, "message": e.message, "detail": e.detail}}, status_code=e.status)

    @app.exception_handler(StarletteHTTPException)
    async def _http_error(_, e):
        code = {404: "not_found", 405: "method_not_allowed"}.get(e.status_code, "bad_request")
        return JSONResponse({"error": {"code": code, "message": code.replace("_", " "), "detail": {}}}, status_code=e.status_code)

    @app.exception_handler(Exception)
    async def _unexpected(_, e):                                  # no traceback, no message text in the body or the log
        log.error("unhandled %s", type(e).__name__)
        return JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)

    @app.exception_handler(RequestValidationError)
    async def _validation(_, e):
        return JSONResponse({"error": {"code": "bad_request", "message": "Malformed request.", "detail": {}}}, status_code=400)

    @app.middleware("http")
    async def _headers(request, call_next):
        if request.url.path.startswith("/api") and time.time() - purged["at"] > 60:     # expired cases vanish even with no create
            purged["at"] = time.time()
            c = conn()
            try:
                DB.purge_expired(c, time.time())
            finally:
                c.close()
        try:
            if local_mode() and not is_loopback_peer(request):                          # D-036: local mode serves loopback peers only, however uvicorn was bound
                resp = JSONResponse({"error": {"code": "forbidden", "message": "Local mode accepts loopback clients only.", "detail": {}}}, status_code=403)
            else:
                resp = await call_next(request)
        except Exception as e:                                                          # last line of defence: standard JSON, no detail
            log.error("unhandled %s", type(e).__name__)
            resp = JSONResponse({"error": {"code": "internal", "message": "Something went wrong.", "detail": {}}}, status_code=500)
        resp.headers["Content-Security-Policy"] = CSP
        resp.headers["Referrer-Policy"] = "no-referrer"
        resp.headers["X-Content-Type-Options"] = "nosniff"
        resp.headers["Cache-Control"] = "no-store" if request.url.path.startswith("/api") else resp.headers.get("Cache-Control", "no-cache")
        return resp
---
tests/e2e/conftest.py:125:    page.get_by_test_id("timeline").wait_for(timeout=15000)
tests/e2e/test_adversarial.py:7:PDF_TEXT = "Page 1 of 3\nPATIENT CHART - CONFIDENTIAL\n\n2026-01-09 ER visit. Neck pain.\f\nPage 2 of 3\nPATIENT CHART - CONFIDENTIAL\nCharge: $500.
tests/e2e/test_suggestions.py:134:    page.route(re.compile(r"/api/cases/[^/]+/dismissal_suggestions/apply$"), lambda r: r.fulfill(status=500, json={"error": {"code": "internal", "
tests/e2e/test_suggestions.py:173:    page.route(re.compile(r"/api/calibration$"), lambda r: r.fulfill(status=500, json={"error": {"code": "internal", "message": "x"}}))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:22:05.518Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; echo \"unhandled: $(grep -c '^unhandled' $R/server_7981.log)\"; echo \"llm call failed: $(grep -c '^llm call failed' $R/server_7981.log)\"; echo \"distinct failed prompt_hash: $(grep -o 'prompt_hash=[0-9a-f]*' $R/server_7981.log | sort -u | wc -l)\"; grep '^unhandled' $R/server_7981.log | sort | uniq -c; echo ---; cat $R/e2e_r2_summary.txt | tail -2; ls $R",
 "description": "Count server-log error classes from the e2e run"
}
````

### User / tool · 2026-11-02T10:22:05.659Z

**tool result**
````
unhandled: 20
llm call failed: 26
distinct failed prompt_hash:       10
   5 unhandled AttributeError
  15 unhandled TypeError
---
SKIPPED [1] tests/e2e/test_ladder_gate.py:37: no rejected item in the sample fixture run
172 passed, 1 skipped, 1 xfailed in 230.06s (0:03:50)
added19.txt
check_missing.py
classify.py
deleted28.txt
e2e_r2_summary.txt
judge_demand.py
library_report_head.md
mut_prompt
mut_scripted
mut_shadow
parent_judges.py
server_7981.log
server_7981.pid
tree
zlayt_e2e.sqlite3
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:22:21.834Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree; grep -n 'judge-summary\").wait_for\\|judge-summary-counts' tests/e2e/test_stepper.py | cut -c1-150; A=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-115-staff-engineer-r2; mkdir -p $A && cp $R/e2e_r2_summary.txt $R/library_report_head.md $R/server_7981.log $R/judge_demand.py $R/check_missing.py $R/parent_judges.py $R/classify.py $R/added19.txt $R/deleted28.txt $A/ && ls $A",
 "description": "Confirm stepper line numbers and copy evidence into review-evidence"
}
````

### User / tool · 2026-11-02T10:22:21.930Z

**tool result (error)**
````
Exit code 1
42:    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
202:    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
204:    assert re.search(r"\d+ checked, \d+ agreed with the draft, 3 questioned", jp.get_by_test_id("judge-summary-counts").inner_text())
256:    jp = page.get_by_test_id("judge-panel"); jp.get_by_test_id("judge-summary").wait_for()
257:    expect(jp.get_by_test_id("judge-summary-counts")).to_have_text(re.compile(r"checked \d+, all agreed"))   # counts load after the panel (retryi
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/e2e_r2_summary.txt: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/library_report_head.md: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/server_7981.log: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/judge_demand.py: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/check_missing.py: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/parent_judges.py: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/classify.py: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/added19.txt: No such file or directory
cp: /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2/tree/deleted28.txt: No such file or directory
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:22:25.432Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; A=/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-115-staff-engineer-r2; mkdir -p $A && cp $R/e2e_r2_summary.txt $R/library_report_head.md $R/server_7981.log $R/judge_demand.py $R/check_missing.py $R/parent_judges.py $R/classify.py $R/added19.txt $R/deleted28.txt $A/ && ls $A",
 "description": "Copy round-2 evidence and check scripts into review-evidence"
}
````

### User / tool · 2026-11-02T10:22:25.568Z

**tool result**
````
added19.txt
check_missing.py
classify.py
deleted28.txt
e2e_r2_summary.txt
judge_demand.py
library_report_head.md
parent_judges.py
server_7981.log
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:23:41.598Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-115-staff-engineer-r2.md",
 "content": "# T-115 round 2 review: curated fixture set and e2e at HEAD (staff-engineer-reviewer)\n\nPinned: HEAD `08c921e878edfb8571e60972bbf5681e16d328fc` (parent `288affc`). Reviewed from `git archive HEAD` copy in scratch, not the working tree (which is dirty with other workers' edits).\nModel: claude-haiku-5-5.\n\n## Verdict: changes (0 blockers, 3 majors, 4 minors)\n\nThe brief's four checks all pass. The fixture change does what the card says: no judge answer is left in the curated set, all 19 new judge answers are real claude-cli recordings, and the guard test fails on both a shadow and a scripted judge file. The e2e suite is green at HEAD (172 passed, 1 skipped, 1 xfailed strict on T-117). What is still open:\n\n- The round-1 e2e race is only half fixed (`test_stepper.py:204`).\n- D-029 is now contradicted by the commit and has no amendment.\n- The round-1 controls-red evidence for `judge_conflict_v5` is still unaddressed.\n\nCommit 08c921e carries no unrelated content. Its 49 paths are the T-115 fixtures and the two T-115 files, but its commit message is a copy of the T-079 message (see F4).\n\n## Brief checks\n\n| Check | Result |\n|---|---|\n| 19 new claude-cli recordings | Confirmed: 19 `A` judge files under `tests/fixtures/llm/`, all `recorded_from` `claude-cli` / `claude-haiku-5-5`, `recorded_at` 2026-11-02T10:06:15Z to 10:07:27Z. |\n| All 28 curated judge files removed | Confirmed: parent had 47 curated files (28 judge, 19 generator); commit deletes 28, all judge; curated now holds 19 generator files, 0 judge. |\n| No curated judge shadows a recording | Confirmed: `classify.py` on the archive, curated = 19 `gen`, 0 `judge`. |\n| Every judge answer the demo needs is a recording | Library replay (`evals/library_report.py` through `judge_demand.py`): 244 judge replays, all from top-level recordings, 0 from curated, 0 misses. The sample path passes `make_curated --check`. See F7 for the e2e-only misses. |\n| `make_curated.py` no longer scripts judge answers | Build and check route `verdict` schemas to recorded replay. A dead scripted branch remains (F4). |\n| `test_curated_fixtures.py` fails on a copied recording | Confirmed: shadow mutant (`0ec6b542...json` copied into curated) gives `1 failed, 5 passed`, `SHADOWS_RECORDING 0ec6b54252d8`. |\n| `make_curated.py --check` passes | Confirmed: exit 0, `entries: 9 non-verified: []`, `letter equal: True | notes equal: True`. |\n| Full tests/e2e on own server, except T-117 | Confirmed: `172 passed, 1 skipped, 1 xfailed in 230.06s`. Skip is `test_ladder_gate.py:37` (\"no rejected item in the sample fixture run\"). Server (PID 97679, port 7981) stopped; port confirmed closed. |\n\n## Findings\n\n**F1 (major, carried from r1 F2, half-fixed).** `tests/e2e/test_stepper.py:202` waits only for the `judge-summary` row, then `:204` reads `judge-summary-counts` with a one-shot `inner_text()`. Commit 6e880e6 converted `:257` to a retrying `to_have_text`, but `:204` was left as it was. A flaky race is still in the suite that the card says is green.\n\n**F2 (major, D-029 contradicted and not amended).** `memory/ORCHESTRATOR_DECISIONS.md:37` (D-029) says the curated set holds \"hand-checked generator/judge responses\" and names the path `tests/fixtures/llm/recorded/`. That path does not exist; the recorded set is the top-level `tests/fixtures/llm/` (1089 files). The commit removes all curated judge answers, so the decision text is now false. `make_curated.py:1-8` and `test_curated_fixtures.py:1-9` cite D-029 for a judge rule that D-029 does not state. `grep -n -i curated memory/DECISIONS.md memory/ASSUMPTIONS.md memory/ORCHESTRATOR_DECISIONS.md` shows no amendment.\n\n**F3 (major, carried from r1 F3, partly resolved).** The scripted J3/J4 answers are gone and the J3 key now replays its recorded `PLAN_VS_ACTUAL`. Still open: `evals/reports/controls-20261102T090925Z.md:3` reads `controls_ok: False` for `judge_conflict_v5` and `judge_flag_v3`, with J3 13/17 caught and false agrees `J3V1, J3V9, J3V13, H3V5` (line 8). That is the newest controls report (`ls evals/reports | grep controls`). Nothing in DECISIONS or ASSUMPTIONS records the red status, and no re-run is cited.\n\n**F4 (minor, dead scripted branch).** `tests/fixtures/make_curated.py:55-60` still scripts `verdict` answers inside `answer()`. It is unreachable today because `fake()` at `:118-119` routes any `verdict` schema to `judge()` first. One routing edit would bring scripted judge answers back, and the unit guard only inspects files that land in the curated dir.\n\n**F5 (minor, commit message does not describe the commit).** `git show -s --format='%h %s' 328428f` and `08c921e` have the identical subject \"feat(evals): library packets lib08..lib15 ... (T-079)\". 328428f is the real T-079 commit (313 files, 291 `tests/fixtures/llm` files, `evals/library/*`, `evals/library_report.py`). 08c921e's 49 paths contain no `evals/` or `expected.json` file, and its body's \"291 claude-cli fixtures\" is 328428f's count. The card note \"swept into T-079's commit\" points at the wrong commit. Nothing unrelated to T-079 or T-115 is in 08c921e's content; the problem is the audit record.\n\n**F6 (minor, error visibility).** `app/backend/api.py:162` and `:184` log only `unhandled %s` with the class name. The e2e run logged 20 such lines (15 `TypeError`, 5 `AttributeError`) with no route and no traceback, so those requests cannot be identified from the run. Each returns an explicit 500 \"Something went wrong.\", so this is not a silent fallback. I did not trace which requests produced them.\n\n**F7 (minor, e2e-only judge misses, pre-existing).** The e2e run logged 26 `llm call failed` lines naming 10 distinct `prompt_hash` values. None of the 10 is in the parent's curated or recorded set (`check_missing.py`), so 08c921e did not cause them. The library replay has zero judge misses. The demo can still issue judge calls with no recording outside the golden and library paths; I did not trace which e2e flows issue them or what the UI shows.\n\n## Round-1 status\n\n- r1 F1 (side-by-side focus test): fixed. `tests/e2e/test_side_by_side.py:61` focuses a row before `p`.\n- r1 F2 (inner_text race): partly fixed, see F1.\n- r1 F3 (regeneration disclosure and scripted J4/J3): scripted answers removed, see F3 for the open controls evidence.\n- r1 F4 (staleness guard): fixed. `test_make_curated_check_is_current` fails when a judge prompt changes (scratch mutant of `app/llm/prompts/judge_flag_v3.md`: `1 failed, 5 passed`, JUDGE_NOT_RUN).\n\n## What I exercised\n\n- Read `personas/staff-engineer.md`, `board show T-115` (notes), `reviews/T-115-staff-engineer.md` (r1), D-029 at `memory/ORCHESTRATOR_DECISIONS.md:37`.\n- `git show --stat --name-status 08c921e`, `git show -s 328428f`, `git merge-base --is-ancestor 328428f 08c921e`, `git log 328428f..08c921e`, `git ls-tree` counts of `evals/library`.\n- `git archive HEAD` into scratch `T115_staff_r2/tree`.\n- Classified the top-level recorded set (683 judge `claude-haiku-5-5`, 406 generator `claude-sonnet-5-5`) and the curated set (19 generator). `parent_judges.py`: parent curated 28 judge + 19 generator; deleted 28, all judge.\n- `.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q` on the archive: 6 passed.\n- `.venv/bin/python tests/fixtures/make_curated.py --check` on the archive: exit 0.\n- Mutants in scratch copies: shadow (`0ec6b54252d8...` copied into curated) gives 1 failed; scripted judge (key `ffff...`) gives 1 failed; judge prompt edit gives `test_make_curated_check_is_current` 1 failed.\n- Fixture server from the archive on `127.0.0.1:7981` (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB` in scratch). `E2E_BASE_URL=http://127.0.0.1:7981 ZLAYT_DB=<scratch> pytest tests/e2e -q`: 172 passed, 1 skipped, 1 xfailed in 230.06s. Server stopped by PID 97679; port closed.\n- `evals/library_report.py` via `judge_demand.py` on the archive: 239 generator and 244 judge replays, 0 curated judge, 0 judge misses, 1 generator miss (`83bcee07...`, lib01 r3, pre-existing).\n- Server log grep and `check_missing.py` for the 10 failed hashes.\n- Read `app/backend/api.py:150-190`, `tests/e2e/test_stepper.py:202-204,256-257` and `tests/e2e/test_side_by_side.py:61` at HEAD.\n- Not run: the full `tests/unit` suite (outside this brief's four checks).\n\nEvidence copied to `artifacts/review-evidence/T-115-staff-engineer-r2/`: `e2e_r2_summary.txt`, `server_7981.log`, `library_report_head.md`, `judge_demand.py`, `classify.py`, `check_missing.py`, `parent_judges.py`, `added19.txt`, `deleted28.txt`.\n\n```json\n{\"card\": \"T-115\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"HEAD 08c921e878edfb8571e60972bbf5681e16d328fc (parent 288affc); git archive copy; own fixture server http://127.0.0.1:7981 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), stopped by PID 97679; sample golden case evals/golden/sample.txt; tests/e2e, tests/unit/test_curated_fixtures.py, tests/fixtures/make_curated.py, tests/fixtures/llm/ (recorded and curated)\",\n \"exercised\": [\n  \"read personas/staff-engineer.md; board show T-115 notes; reviews/T-115-staff-engineer.md (r1); memory/ORCHESTRATOR_DECISIONS.md:37 (D-029)\",\n  \"git show --stat/--name-status 08c921e (49 paths: 47 under tests/fixtures/llm, make_curated.py, test_curated_fixtures.py); git show -s 328428f; git merge-base --is-ancestor 328428f 08c921e (true); git log 328428f..08c921e\",\n  \"git archive HEAD into scratch T115_staff_r2/tree\",\n  \"classified recorded set (top-level: 683 judge claude-haiku-5-5, 406 generator claude-sonnet-5-5) and curated set (19 generator, 0 judge); 19 added files all judge, claude-cli, claude-haiku-5-5, recorded_at 2026-11-02T10:06-10:07Z\",\n  \"parent curated set 08c921e^: 47 files, 28 judge, 19 generator; the 28 deleted files are all judge\",\n  \".venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q on archive: 6 passed\",\n  \".venv/bin/python tests/fixtures/make_curated.py --check on archive: exit 0, entries 9 non-verified [], letter equal True | notes equal True\",\n  \"mutant shadow: 0ec6b54252d8 judge copied into curated; test_curated_fixtures.py: 1 failed, 5 passed (SHADOWS_RECORDING)\",\n  \"mutant scripted: judge answer under key ffff...ff with no recording; test_curated_fixtures.py: 1 failed, 5 passed (SCRIPTED_JUDGE)\",\n  \"mutant prompt: appended line to app/llm/prompts/judge_flag_v3.md in scratch; test_make_curated_check_is_current fails (JUDGE_NOT_RUN); 1 failed, 5 passed\",\n  \"full pytest tests/e2e -q against 127.0.0.1:7981 (archive server), ZLAYT_DB in scratch: 172 passed, 1 skipped (test_ladder_gate.py:37), 1 xfailed (T-117 strict) in 230.06s; server stopped by PID 97679, port closed\",\n  \"evals/library_report.py via judge_demand.py wrapper on archive: 239 generator and 244 judge replays from recordings, 0 curated judge, 0 judge misses, 1 generator miss 83bcee07 (lib01 r3, pre-existing)\",\n  \"server_7981.log: 20 unhandled (15 TypeError, 5 AttributeError), 26 llm call failed over 10 distinct prompt_hash; check_missing.py: none of the 10 in parent curated or recorded set\",\n  \"read app/backend/api.py:150-190; tests/e2e/test_stepper.py:202-204 and :256-257; tests/e2e/test_side_by_side.py:61 at HEAD archive; app/llm/backends/fixture.py call() fallback order\",\n  \"grep of memory/DECISIONS.md, memory/ASSUMPTIONS.md, memory/ORCHESTRATOR_DECISIONS.md for curated/T-115: no amendment to D-029\",\n  \"read evals/reports/controls-20261102T090925Z.md:3,8 (controls_ok False, J3 13/17); ls evals/reports controls files (newest is 090925Z)\",\n  \"not run: full tests/unit suite (outside the brief's four checks)\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"judge_answers_are_recordings\": 5, \"curated_has_no_judge_answers\": 5, \"guard_test_catches_shadow_and_scripted\": 5, \"make_curated_check_current\": 5, \"e2e_green_at_head\": 4, \"e2e_reproducibility\": 3, \"decision_record_consistency\": 2, \"commit_scope_and_message\": 3, \"error_visibility\": 3, \"scripted_code_removed\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"r1 F2 only half-fixed: judge-summary-counts still read with one-shot inner_text() at test_stepper.py:204\",\n   \"evidence\": \"tests/e2e/test_stepper.py:202 waits only for the judge-summary row: jp.get_by_test_id('judge-summary').wait_for(); :204 asserts re.search(..., jp.get_by_test_id('judge-summary-counts').inner_text()). Commit 6e880e6 changed :257 to expect(...).to_have_text(...) but left :204. r1 pair runs at 400a8c0 gave 'loading' failures on 2 of 3 runs.\",\n   \"why_it_matters\": \"The suite is the card's deliverable. A gate that passes one run and fails the next is not evidence (criterion 14), and the green result at HEAD cannot be trusted to hold on the next run.\",\n   \"fix\": \"Replace the assert at test_stepper.py:204 with expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\\\\d+ checked, \\\\d+ agreed with the draft, 3 questioned')). Keep :257 as it is.\",\n   \"acceptance_test\": \"tests/e2e/test_stepper.py::test_judge_panel_collapsed_summary_and_labels and ::test_judge_panel_when_nothing_objected pass in 10 consecutive runs against a HEAD archive, each with a fresh ZLAYT_DB; grep shows no inner_text() read of judge-summary-counts in tests/e2e/test_stepper.py.\"},\n  {\"severity\": \"major\",\n   \"title\": \"D-029 contradicted by the commit and not amended; recorded path in D-029 does not exist\",\n   \"evidence\": \"memory/ORCHESTRATOR_DECISIONS.md:37 (D-029): 'tests/fixtures/llm/curated/ (hand-checked generator/judge responses ...)' and 'tests/fixtures/llm/recorded/'. In the HEAD archive, tests/fixtures/llm/recorded does not exist (ls: No such file); the recorded set is the top-level tests/fixtures/llm/ with 1089 files. Curated now has 19 generator and 0 judge files. make_curated.py:1-8 and tests/unit/test_curated_fixtures.py:1-9 cite D-029 for the judge rule. grep -n -i curated memory/DECISIONS.md memory/ASSUMPTIONS.md memory/ORCHESTRATOR_DECISIONS.md shows no amendment.\",\n   \"why_it_matters\": \"D-029 is the binding fixture decision and CLAUDE.md non-negotiable 12 requires decisions to be recorded. The commit reverses half of what D-029 says the curated set contains, and the text a future reader sees says the opposite. A reader following the recorded path looks in a directory that does not exist.\",\n   \"fix\": \"Orchestrator records a D-029 amendment in memory/ORCHESTRATOR_DECISIONS.md: judge answers are recordings only; curated holds generator and narrative answers; the recorded set is tests/fixtures/llm/. Correct the path in the D-029 row. Reviewers do not write memory/.\",\n   \"acceptance_test\": \"memory/ORCHESTRATOR_DECISIONS.md has an amendment row citing 08c921e and T-115; the D-029 row names tests/fixtures/llm/ as the recorded set and contains no claim that curated holds judge responses.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Round-1 F3 still open: judge_conflict_v5 controls red and not recorded or re-run\",\n   \"evidence\": \"evals/reports/controls-20261102T090925Z.md:3 reads 'controls_ok: False' (prompts judge_conflict_v5, judge_flag_v3); line 8 shows J3 13/17 caught with false agrees J3V1, J3V9, J3V13, H3V5. It is the newest controls report (ls evals/reports | grep controls: only 075238Z and 090925Z). grep in memory/ASSUMPTIONS.md and memory/DECISIONS.md finds no record of the red status.\",\n   \"why_it_matters\": \"The curated set no longer scripts judges, so the e2e now depends on recorded judge_conflict_v5 answers from a judge whose live controls are red. D-046 makes J3 and J4 control sets part of ship-bar item 4. The card does not disclose this.\",\n   \"fix\": \"Re-run the judge_conflict_v5 controls from a clean worktree and cite the new report, or record in memory/DECISIONS.md that v5 controls are red with the ship-bar consequence. The orchestrator owns the decision record.\",\n   \"acceptance_test\": \"A controls report with controls_ok True for judge_conflict_v5 is cited in the T-115 handoff, or a DECISIONS row names the red report and its effect on ship-bar item 4.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"make_curated.py still contains a scripted verdict branch in answer()\",\n   \"evidence\": \"tests/fixtures/make_curated.py:55-60: if 'verdict' in props: ... return dict(verdict=pick, reason_code='NONE'). Unreachable today because fake() at :118-119 routes any verdict schema to judge() first.\",\n   \"why_it_matters\": \"The commit says make_curated no longer scripts judge answers. One routing edit re-enables scripted judge answers, and the guard test only inspects files that land in the curated dir.\",\n   \"fix\": \"Delete the verdict branch from answer(); make answer() raise SystemExit for a schema with a verdict property.\",\n   \"acceptance_test\": \"A unit test calls make_curated.answer() with a verdict schema and asserts SystemExit; grep for 'verdict' inside answer() returns nothing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"08c921e carries a copied T-079 commit message; its content is T-115 only\",\n   \"evidence\": \"git show -s --format='%h %s' 328428f and 08c921e: identical subject 'feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)'. 328428f is the T-079 commit (313 files, 291 tests/fixtures/llm, evals/library/*, evals/library_report.py). git show --name-status --format= 08c921e lists 49 paths, none under evals/ or any expected.json; the body's '291 claude-cli fixtures' is 328428f's count. Card note: 'swept into T-079's commit via shared index' names the wrong commit.\",\n   \"why_it_matters\": \"Audit trail: git log attributes 19 judge recordings and 28 removals to T-079 and suggests the packets are in 08c921e. Nothing unrelated to T-079 or T-115 is in 08c921e's content.\",\n   \"fix\": \"Do not rewrite history (destructive git is blocked). Correct the T-115 card note to say 08c921e is T-115 content under a copied T-079 message; add a LESSON that a commit message must be derived from its own diff.\",\n   \"acceptance_test\": \"The T-115 card note names 08c921e as T-115 content; memory/LESSONS.md has the entry.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Unhandled exceptions are logged by class name only, with no route or traceback\",\n   \"evidence\": \"app/backend/api.py:162 and :184: log.error('unhandled %s', type(e).__name__). The e2e run logged 20 such lines (15 TypeError, 5 AttributeError) in artifacts/review-evidence/T-115-staff-engineer-r2/server_7981.log. Each returns 500 'Something went wrong.' (explicit, not a silent fallback). I did not trace which requests raised.\",\n   \"why_it_matters\": \"TypeError and AttributeError are programming errors reached on some e2e flows while the suite stays green. An operator sees a class name and no path, so the 20 requests cannot be reproduced from the log (criterion 12: failures must be visible).\",\n   \"fix\": \"Log the route, a request id and the traceback server-side (never in the response body). Re-run the e2e and triage each error class to a test or a product fix.\",\n   \"acceptance_test\": \"A forced TypeError in a route produces a 500 with the route and traceback in the server log and no traceback in the response body; the next e2e log shows the route for each unhandled line.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Judge re-check prompts outside the golden and library paths have no recording (pre-existing)\",\n   \"evidence\": \"artifacts/review-evidence/T-115-staff-engineer-r2/server_7981.log: 26 'llm call failed ... prompt_hash=' lines, 10 distinct hashes. check_missing.py: none of the 10 is in the parent's curated or recorded set, so 08c921e did not cause them. Library replay (judge_demand.py): 244 judge replays, 0 misses, 0 curated.\",\n   \"why_it_matters\": \"The demo can issue judge calls that have no recording, so those checks fail on the fixture backend. The failure is visible in the log and not silent, and it predates this commit. I did not confirm the UI outcome.\",\n   \"fix\": \"Decide and record whether the cached demo needs recordings for re-checks after edits (see question_for_chris), or record the boundary in D-029.\",\n   \"acceptance_test\": \"Either the 10 keys are recorded and the e2e log shows no FixtureMiss, or D-029 names the boundary and the e2e test asserts the visible failure state.\"}\n ],\n \"whats_right\": [\n  \"08c921e's content is T-115 only: 19 new recordings are all claude-cli judge answers, the 28 deletions are exactly the parent's 28 judge files, and the curated set keeps its 19 generator answers.\",\n  \"The guard test fails on both a shadowed recording and a scripted judge file, and make_curated --check fails when a judge prompt changes, so the r1 staleness finding is closed.\",\n  \"The T-117 xfail is strict and still the only xfail; the side-by-side focus fix at test_side_by_side.py:61 closes r1 F1.\"\n ],\n \"questions_for_chris\": [\n  \"Should the cached demo carry recordings for judge re-checks triggered by edits (F7), or is a visible failure acceptable offline?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T10:23:41.777Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-115-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:23:49.596Z

**tool call — Bash**
````
{
 "command": "R=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T115_staff_r2; cat > $R/validate_r2.py <<'EOF'\nimport json, pathlib, re, sys\ntext = pathlib.Path(sys.argv[1]).read_text()\nblocks = re.findall(r\"```json\\n(.*?)\\n```\", text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"card\", d[\"card\"], \"persona\", d[\"persona\"], \"model\", d[\"model\"], \"verdict\", d[\"verdict\"])\nprint(\"severities\", sev)\nwant = \"fail\" if \"blocker\" in sev else (\"changes\" if \"major\" in sev else \"pass\")\nprint(\"rule verdict\", want, \"match\", want == d[\"verdict\"])\nprint(\"whats_right\", len(d[\"whats_right\"]), \"exercised\", len(d[\"exercised\"]))\nEOF\n/Users/arsis/zlayt-pm-project/.venv/bin/python -I $R/validate_r2.py /Users/arsis/zlayt-pm-project/reviews/T-115-staff-engineer-r2.md; cd /Users/arsis/zlayt-pm-project && python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate the review JSON block and verdict rule, run read-only board validate"
}
````

### User / tool · 2026-11-02T10:23:49.789Z

**tool result**
````
json blocks: 1
card T-115 persona staff-engineer-reviewer model claude-haiku-5-5 verdict changes
severities ['major', 'major', 'major', 'minor', 'minor', 'minor', 'minor']
rule verdict changes match True
whats_right 3 exercised 17
ok (119 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T10:23:53.604Z

T-115 r2 verdict is changes (0 blockers, 3 majors, 4 minors) in /Users/arsis/zlayt-pm-project/reviews/T-115-staff-engineer-r2.md: all four brief checks pass and 08c921e has no unrelated content (only a copied T-079 message), but the e2e race at test_stepper.py:204 is still there, D-029 is not amended, and the judge_conflict_v5 controls are still red.
