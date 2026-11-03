# Subagent: T-030 r2 check (haiku) (T-030 r2 check (haiku))

Source: `agent-a13aadf03abd5bf69.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:50:24.150Z

Working directory: /Users/arsis/zlayt-pm-project. Round 2 of T-030 against reviews/T-030-staff-engineer.md (majors: grounding.check_amount missing; compose_state ignores endpoint_unverified). Run `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` and quote the summary line; pass if 0 failures and both majors are resolved. Write reviews/T-030-staff-engineer-r2.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:25.772Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T01:50:25.785Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:25.978Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer.md"
}
````

### User / tool · 2026-11-02T01:50:25.985Z

**tool result**
````
1	# T-030 review: staff-engineer-reviewer (Marcus Lee)
2	
3	Verdict: **changes**. No blockers. Two majors: `check_amount` is not implemented (checklist #4), and `compose_state` has no code path for `endpoint_unverified`, so it fails open to `verified`. Both are red in the shipped suite.
4	
5	Core behaviour is right. Exercised with `artifacts/review-evidence/T-030-exercise.py`:
6	- All 68 golden excerpts verify clean against their own record text.
7	- Non-verbatim quotes (changed words, lower-cased, truncated) return exactly `GROUNDING_EXCERPT_NOT_VERBATIM`.
8	- Dropping "may represent degenerative change; correlate clinically." from record 8 returns `EXCERPT_OMITS_QUALIFIER`. A half hedge also returns it. The hedge alone is clean.
9	- A mid-unit excerpt returns `EXCERPT_NOT_WHOLE_SENTENCE`, which maps to needs_review.
10	- A summary "Pain 4/10." over "Pain 3/10." returns `SUMMARY_TOKEN_NOT_IN_EXCERPT`. A summary dropping "without loss of consciousness" returns `SUMMARY_DROPS_QUALIFIER`. `compose_state` makes both `needs_review`. "Visit 8" as a label passes.
11	- "approx. 35 mph." is one unit. "10 mg. in the morning" is one unit. "10 mg. Follow" splits in two. That matches the revised test and conflicts with the REQ abbreviation list, as the backend handoff says.
12	- Units tile every golden excerpt.
13	- `check_excerpt` never mutates its input and returns only codes.
14	- The output is byte-identical across two runs.
15	- The four modules import no LLM client (`re`, `yaml`, `functools`, `pathlib`, `app.backend.grounding` only).
16	- Mutation: replacing the hedge test with `if False:` in a scratch copy turned `test_entry8_without_hedge_needs_review` and `test_entry8_with_half_the_hedge_still_omits` red.
17	
18	Run: `pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `6 failed, 203 passed`. The 6 are the T-029 r2 tests added in b366b75 after T-030's commit 217e243. The card evidence says "200 pass", which is stale.
19	
20	```json
21	{"card": "T-030", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
22	 "scope": "app/backend/{sentences,grounding,confidence,why}.py at commit 217e243 (working tree at b366b75); tests/unit/test_{sentences,grounding,confidence,boundaries}.py; evals/golden",
23	 "exercised": [
24	  "python3 tools/board.py show T-030",
25	  ".venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q (6 failed, 203 passed)",
26	  ".venv/bin/python artifacts/review-evidence/T-030-exercise.py (golden excerpts, non-verbatim, hedge drop, summary tokens, splitter, no-repair, imports, determinism; 2 FAIL lines = the two majors); run twice, identical md5",
27	  "read grounding.py, sentences.py, confidence.py in full; grep except/continue",
28	  "mutation in scratch copy (is_hedge_unit gate -> False): 2 hedge tests red",
29	  "compose_state with a misspelled context key -> ('verified', [])",
30	  "python3 tools/board.py validate -> ok (49 file(s))"],
31	 "verdict": "changes",
32	 "scores": {"excerpt_verification": 4, "summary_checks": 4, "splitter": 4, "compose_state_fail_closed": 2, "test_coverage": 3, "no_llm_boundary": 5},
33	 "findings": [
34	  {"severity": "major", "title": "Amount-in-text grounding check (check_amount) not implemented",
35	   "evidence": "grounding.py has no check_amount (exercise script: 'FAIL check_amount exists'). pytest: tests/unit/test_grounding.py::test_amount_present_in_record_passes, ::test_amount_absent_from_record_is_rejected[$6,420|$9,000|$62,400] and ::test_noisy_amount_not_autocorrected fail with AttributeError: module 'app.backend.grounding' has no attribute 'check_amount' (test_grounding.py:158-168).",
36	   "why_it_matters": "Checklist #4 requires each amount to appear in its record's text, or an amount the model invented or 'corrected' ($1,2OO -> $1,200) reaches the total with no code gate. GROUNDING_AMOUNT_NOT_IN_TEXT is in REJECTED_CODES but nothing produces it.",
37	   "fix": "Add check_amount(record_text, raw_amount) -> [] or ['GROUNDING_AMOUNT_NOT_IN_TEXT'] using the same whitespace normalization as locate; no digit repair.",
38	   "acceptance_test": "pytest tests/unit/test_grounding.py -k amount green; stubbing check_amount to return [] makes test_amount_absent_from_record_is_rejected red"},
39	  {"severity": "major", "title": "compose_state ignores endpoint_unverified and fails open to verified",
40	   "evidence": "confidence.py:42-60 never reads ctx['endpoint_unverified']. Repro: C.compose_state({'grounding_failures':[],'schema_valid':True,'code_reasons':[],'judge':'supported'},{'endpoint_unverified':True}) -> ('verified', []). pytest tests/unit/test_confidence.py::test_needs_review_cases[ladder21-ctx21-ENDPOINT_NOT_VERIFIED] fails (test_confidence.py:66).",
41	   "why_it_matters": "A gap flag whose span could contain an unconfirmed date is the case where a false 73-day flag would show as verified. ENDPOINT_NOT_VERIFIED is in REASON_CODES but can never be produced (api.md:448).",
42	   "fix": "Add ('endpoint_unverified', 'ENDPOINT_NOT_VERIFIED') to the boolean table at confidence.py:55.",
43	   "acceptance_test": "pytest tests/unit/test_confidence.py green"},
44	  {"severity": "minor", "title": "compose_state silently ignores unknown or misspelled ladder and context keys",
45	   "evidence": "compose_state({...ok...}, {'injecton': True}) -> ('verified', []). Booleans read with ctx.get(key); date_status/amount_class/agreement default to 'no doubt' when absent (confidence.py:52-57). This is how the endpoint_unverified gap above went unnoticed.",
46	   "why_it_matters": "A typo in the pipeline caller produces verified with no error: a silent fallback by omission. 'Unknown value' already raises ValueError, but unknown keys do not.",
47	   "fix": "Raise ValueError on keys outside the documented ladder/context sets (or require all keys). Keep judge=None as the documented 'no judge needed' case.",
48	   "acceptance_test": "new test: compose_state(L(), {'injecton': True}) raises ValueError"},
49	  {"severity": "minor", "title": "Lexicon loader silently skips malformed entries, including hedge: true entries",
50	   "evidence": "grounding.py:66 `if not isinstance(e, dict) or 'pattern' not in e: continue`; _lexicon is lru_cached (line 62).",
51	   "why_it_matters": "A hedge: true entry with a typo'd key is dropped from the hedge set and EXCERPT_OMITS_QUALIFIER stops firing for it, with no error.",
52	   "fix": "Raise on an entry with hedge: true or self_report: true and no valid pattern; keep skipping only comment/metadata rows explicitly.",
53	   "acceptance_test": "test with a tmp lexicon that has hedge: true and no pattern raises"},
54	  {"severity": "minor", "title": "Summary-side hedge/negation/self-report detection uses hardcoded word lists, not the lexicon",
55	   "evidence": "grounding.py:152 _HEDGE_WORDS, _SELF, _NEG, _LATERAL, _APPROX regexes are in code; line 163 accepts `hedge_ids(summary) or _HEDGE_WORDS.search(summary)`. AC1 says the hedge set is read from lexicon.yaml `hedge: true` (R-TL-8).",
56	   "why_it_matters": "Two hedge vocabularies can drift: a lexicon edit changes the excerpt check but not the summary check, and the summary check passes on any of 'may|likely|appears|...' even when the lexicon hedge in the excerpt is a different concept.",
57	   "fix": "Use hedge_ids(summary) only (or document _HEDGE_WORDS as the intentional looser summary-side set in the module docstring and test its boundary).",
58	   "acceptance_test": "test: excerpt hedge 'cannot be excluded' with summary 'may be present' -> decided and asserted either way"},
59	  {"severity": "minor", "title": "AC-named tests do not exist; the no-silent-repair claim has no direct test",
60	   "evidence": "AC cites test_grounding::test_no_silent_fix, ::test_summary_tokens, ::test_offsets_golden, ::test_offset_lookup_failure. grep 'silent|unchanged' tests/unit/test_grounding.py -> nothing. Tests have different names (test_changed_pain_score_flags, test_locate_mutated_record_returns_none). Handoff itself notes this.",
61	   "why_it_matters": "AC5 'a failing quote is never repaired' rests on test_not_verbatim_is_rejected only. A function that returned the corrected text alongside the code would still pass.",
62	   "fix": "Add a test that check_excerpt on a near-miss returns only reason codes (list of str) and leaves the input unchanged, and align AC text with the real test names.",
63	   "acceptance_test": "pytest tests/unit/test_grounding.py -k 'repair or silent'"},
64	  {"severity": "nit", "title": "Card evidence is stale",
65	   "evidence": "T-030 AC evidence says '200 pass, 1 test_sentences hedge-split test wrong'. Today: 6 failed, 203 passed (the 6 are the two majors above). test_sentences passes now.",
66	   "why_it_matters": "A reader trusts a green claim that no longer holds.",
67	   "fix": "Re-run and update the evidence after fixing the majors.",
68	   "acceptance_test": "pytest ... -q prints 'passed' with no failures"}
69	 ],
70	 "whats_right": [
71	  "check_excerpt is a pure function of (record, excerpt): verbatim after whitespace normalization, offsets mapped back to raw text, returns codes only and never rewrites the quote.",
72	  "Hedge omission and summary qualifier/token checks behave as the AC states on the real record 8, record 2 and 'Pain 3/10.' cases, and fail when the hedge gate is removed.",
73	  "compose_state raises on unknown reason codes and unknown judge/date/amount values, and the four modules import no LLM client, network or app.llm code."
74	 ],
75	 "questions_for_chris": []}
76	```
77	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:26.202Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T01:50:26.217Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks
3	- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method
4	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:28.595Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q 2>&1 | tail -n 30",
 "description": "Run the four T-030 unit test files and capture summary"
}
````

### User / tool · 2026-11-02T01:50:29.244Z

**tool result**
````
........................................................................ [ 34%]
........................................................................ [ 68%]
.................................................................        [100%]
209 passed in 0.29s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:29.258Z

**tool call — Bash**
````
{
 "command": "grep -n \"check_amount\\|GROUNDING_AMOUNT_NOT_IN_TEXT\" -r app tests evals 2>/dev/null; echo \"---\"; grep -n \"endpoint_unverified\\|ENDPOINT_NOT_VERIFIED\" -r app tests 2>/dev/null; echo \"---\"; ls -la app/backend/ 2>/dev/null",
 "description": "Grep for check_amount and endpoint_unverified references"
}
````

### User / tool · 2026-11-02T01:50:29.354Z

**tool result**
````
app/backend/confidence.py:6:    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
app/backend/confidence.py:13:REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
app/backend/why.py:4:    "GROUNDING_AMOUNT_NOT_IN_TEXT": "The amount shown does not appear in the record text, so this item was rejected and cannot be used.",
app/backend/grounding.py:110:def check_amount(record_text: str, raw_amount: str) -> list:
app/backend/grounding.py:120:    return ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_grounding.py:155:# ---------- amount grounding (checklist 4, api.md GROUNDING_AMOUNT_NOT_IN_TEXT)
tests/unit/test_grounding.py:158:    assert GR.check_amount(G.record("sample", 2)["excerpt"], "$6,240") == []
tests/unit/test_grounding.py:162:    """R-CH-1 / row 6: an amount the record does not contain -> GROUNDING_AMOUNT_NOT_IN_TEXT (rejected)."""
tests/unit/test_grounding.py:163:    assert GR.check_amount(G.record("sample", 2)["excerpt"], raw) == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_grounding.py:168:    assert GR.check_amount(t, "$1,2OO") == [] and GR.check_amount(t, "$1,200") == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_confidence.py:36:    (L(grounding_failures=["GROUNDING_AMOUNT_NOT_IN_TEXT"]), "GROUNDING_AMOUNT_NOT_IN_TEXT"),
---
app/backend/why.py:19:    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:44:             "endpoint_unverified"}
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/gaps.py:37:            reasons.append("ENDPOINT_NOT_VERIFIED")
tests/unit/test_confidence.py:7:          "split_ambiguous": bool, "llm_failed": bool, "endpoint_unverified": bool}
tests/unit/test_confidence.py:15:CTX = dict(injection=False, date_status="parsed", amount_class=None, agreement=None, fixture_miss=False, split_ambiguous=False, llm_failed=False, endpoint_unverified=False)
tests/unit/test_confidence.py:66:    (L(), X(endpoint_unverified=True), "ENDPOINT_NOT_VERIFIED"),   # R-FL-1: a gap whose span could contain an unconfirmed date
---
total 240
drwxr-xr-x@ 23 arsis  staff    736 Nov  1 19:49 .
drwxr-xr-x@  8 arsis  staff    256 Nov  1 19:40 ..
-rw-r--r--@  1 arsis  staff      0 Nov  1 19:40 __init__.py
-rw-r--r--@  1 arsis  staff    338 Nov  1 19:41 amounts.py
-rw-r--r--@  1 arsis  staff   3682 Nov  1 19:50 confidence.py
-rw-r--r--@  1 arsis  staff   6119 Nov  1 19:50 conflicts.py
-rw-r--r--@  1 arsis  staff   4623 Nov  1 19:49 dates.py
-rw-r--r--@  1 arsis  staff    258 Nov  1 19:47 export.py
-rw-r--r--@  1 arsis  staff   7846 Nov  1 19:48 flag_templates.py
-rw-r--r--@  1 arsis  staff    488 Nov  1 19:44 flags.py
-rw-r--r--@  1 arsis  staff   3601 Nov  1 19:48 gaps.py
-rw-r--r--@  1 arsis  staff   8676 Nov  1 19:49 generator.py
-rw-r--r--@  1 arsis  staff   9238 Nov  1 19:50 grounding.py
-rw-r--r--@  1 arsis  staff  11567 Nov  1 19:49 ingest.py
-rw-r--r--@  1 arsis  staff   1240 Nov  1 19:45 injection.py
-rw-r--r--@  1 arsis  staff   5205 Nov  1 19:49 judges.py
-rw-r--r--@  1 arsis  staff    761 Nov  1 19:45 lexicon.py
-rw-r--r--@  1 arsis  staff    354 Nov  1 19:44 pipeline.py
-rw-r--r--@  1 arsis  staff    548 Nov  1 19:47 review.py
-rw-r--r--@  1 arsis  staff   1397 Nov  1 19:48 schemas.py
-rw-r--r--@  1 arsis  staff   3284 Nov  1 19:46 sentences.py
-rw-r--r--@  1 arsis  staff    155 Nov  1 19:41 totals.py
-rw-r--r--@  1 arsis  staff   3174 Nov  1 19:46 why.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:30.743Z

Suite is green at 209 passed. Next I'll read the two changed modules and the tests that cover the majors to confirm the fixes are real.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:30.928Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/grounding.py"
}
````

### User / tool · 2026-11-02T01:50:30.937Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:31.113Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/confidence.py"
}
````

### User / tool · 2026-11-02T01:50:31.128Z

**tool result**
````
1	"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.
2	
3	Precedence: rejected > needs_review > verified. Reason codes are a closed list (api.md appendix); an unknown code is a bug.
4	"""
5	REASON_CODES = (
6	    "GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID",
7	    "SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE",
8	    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
9	    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
10	    "AMOUNT_ESTIMATE", "AMOUNT_DAMAGES", "AMOUNT_UNCLEAR", "LEXICON_ONLY", "LLM_ONLY", "SPLIT_AMBIGUOUS",
11	    "INJECTION_SUSPECTED", "LLM_FAILED_AFTER_RETRIES",
12	)
13	REJECTED_CODES = frozenset({"GROUNDING_EXCERPT_NOT_VERBATIM", "GROUNDING_AMOUNT_NOT_IN_TEXT", "SCHEMA_INVALID"})
14	STATE_ORDER = {"needs_review": 0, "verified": 1, "rejected": 2}
15	
16	_JUDGE = {"partially": "JUDGE_PARTIAL", "unsupported": "JUDGE_UNSUPPORTED", "disagrees": "JUDGE_DISAGREES",
17	          "unsure": "JUDGE_UNSURE", "unavailable": "JUDGE_UNAVAILABLE"}
18	_AMOUNT = {"rate": "AMOUNT_RATE_NOT_TOTALED", "estimate": "AMOUNT_ESTIMATE", "damages": "AMOUNT_DAMAGES", "unclear": "AMOUNT_UNCLEAR"}
19	_AGREE = {"lexicon_only": "LEXICON_ONLY", "llm_only": "LLM_ONLY"}
20	_DATE = {"ambiguous": "DATE_AMBIGUOUS", "missing": "DATE_MISSING"}
21	
22	
23	def sort_key(state: str) -> int:
24	    """needs_review first, then verified, then rejected."""
25	    return STATE_ORDER[state]
26	
27	
28	def _known(code: str) -> str:
29	    if code not in REASON_CODES:
30	        raise ValueError(f"unknown reason code: {code}")
31	    return code
32	
33	
34	def _lookup(table: dict, value, none_ok=()):
35	    if value is None or value in none_ok:
36	        return None
37	    if value not in table:
38	        raise ValueError(f"unknown value: {value}")
39	    return table[value]
40	
41	
42	_LADDER_KEYS = {"grounding_failures", "schema_valid", "code_reasons", "judge"}
43	_CTX_KEYS = {"injection", "date_status", "amount_class", "agreement", "fixture_miss", "split_ambiguous", "llm_failed",
44	             "endpoint_unverified"}
45	
46	
47	def compose_state(ladder: dict, context: dict = None):
48	    ctx = context or {}
49	    bad = (set(ladder) - _LADDER_KEYS) | (set(ctx) - _CTX_KEYS)
50	    if bad:      # a misspelled key must not fail open to 'verified'
51	        raise ValueError(f"unknown ladder/context keys: {sorted(bad)}")
52	    rejected, doubts = [], []
53	    for c in ladder.get("grounding_failures", []) or []:
54	        rejected.append(_known(c))
55	    if ladder.get("schema_valid", True) is False:
56	        rejected.append("SCHEMA_INVALID")
57	    for c in ladder.get("code_reasons", []) or []:
58	        (rejected if _known(c) in REJECTED_CODES else doubts).append(c)
59	    doubts.append(_lookup(_JUDGE, ladder.get("judge"), none_ok=("supported",)))
60	    doubts.append(_lookup(_DATE, ctx.get("date_status"), none_ok=("parsed", "confirmed")))
61	    doubts.append(_lookup(_AMOUNT, ctx.get("amount_class"), none_ok=("charge",)))
62	    doubts.append(_lookup(_AGREE, ctx.get("agreement"), none_ok=("both",)))
63	    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"),
64	                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
65	        if ctx.get(key):
66	            doubts.append(code)
67	    rejected = list(dict.fromkeys(rejected))
68	    if rejected:
69	        return "rejected", rejected
70	    doubts = list(dict.fromkeys(d for d in doubts if d))
71	    return ("needs_review", doubts) if doubts else ("verified", [])
72	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:31.438Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_grounding.py",
 "offset": 150,
 "limit": 30
}
````

### User / tool · 2026-11-02T01:50:31.450Z

**tool result**
````
150	            assert "SUMMARY_TOKEN_NOT_IN_EXCERPT" in out, se["id"]
151	        if se["kind"] == "control":
152	            assert out == [], se["id"]
153	
154	
155	# ---------- amount grounding (checklist 4, api.md GROUNDING_AMOUNT_NOT_IN_TEXT)
156	def test_amount_present_in_record_passes():
157	    """R-CH-1: '$6,240' is in sample record 2 -> no reason."""
158	    assert GR.check_amount(G.record("sample", 2)["excerpt"], "$6,240") == []
159	
160	@pytest.mark.parametrize("raw", ["$6,420", "$9,000", "$62,400"])
161	def test_amount_absent_from_record_is_rejected(raw):
162	    """R-CH-1 / row 6: an amount the record does not contain -> GROUNDING_AMOUNT_NOT_IN_TEXT (rejected)."""
163	    assert GR.check_amount(G.record("sample", 2)["excerpt"], raw) == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
164	
165	def test_noisy_amount_not_autocorrected():
166	    """R-CH-1: '$1,2OO' (case_03) is found as written; the corrected '$1,200' is NOT in the text and is rejected."""
167	    t = G.record("case_03_rate_and_ocr", 2)["excerpt"]
168	    assert GR.check_amount(t, "$1,2OO") == [] and GR.check_amount(t, "$1,200") == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
169	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:31.599Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/test_confidence.py"
}
````

### User / tool · 2026-11-02T01:50:31.610Z

**tool result**
````
1	"""compose_state table + why templates. R-TL-5, ADR-005, LLM_VS_CODE rows 17 and 18.
2	
3	Ladder:  {"grounding_failures": [codes], "schema_valid": bool, "code_reasons": [codes], "judge": None|"supported"|"partially"|
4	          "unsupported"|"disagrees"|"unsure"|"unavailable"}
5	Context: {"injection": bool, "date_status": "parsed"|"confirmed"|"ambiguous"|"missing", "amount_class": None|"charge"|"rate"|
6	          "estimate"|"damages"|"unclear", "agreement": None|"both"|"lexicon_only"|"llm_only", "fixture_miss": bool,
7	          "split_ambiguous": bool, "llm_failed": bool, "endpoint_unverified": bool}
8	Returns (state, reasons). Precedence rejected > needs_review > verified.
9	"""
10	import pathlib, re
11	import pytest
12	from app.backend import confidence as C, why as W
13	
14	OK = dict(grounding_failures=[], schema_valid=True, code_reasons=[], judge="supported")
15	CTX = dict(injection=False, date_status="parsed", amount_class=None, agreement=None, fixture_miss=False, split_ambiguous=False, llm_failed=False, endpoint_unverified=False)
16	
17	def L(**kw):
18	    return {**OK, **kw}
19	def X(**kw):
20	    return {**CTX, **kw}
21	
22	def test_all_clear_is_verified():
23	    """R-TL-5: every code check passed, judge positive, no context doubt -> verified with no reasons."""
24	    assert C.compose_state(L(), X()) == ("verified", [])
25	
26	def test_no_judge_required_item_is_verified():
27	    """R-TL-5 / row 17: items without a judge (judge None) with clean checks are verified."""
28	    assert C.compose_state(L(judge=None), X()) == ("verified", [])
29	
30	def test_confirmed_date_is_verified():
31	    """R-IN-5: a date the paralegal confirmed no longer needs review."""
32	    assert C.compose_state(L(), X(date_status="confirmed")) == ("verified", [])
33	
34	@pytest.mark.parametrize("ladder,code", [
35	    (L(grounding_failures=["GROUNDING_EXCERPT_NOT_VERBATIM"]), "GROUNDING_EXCERPT_NOT_VERBATIM"),
36	    (L(grounding_failures=["GROUNDING_AMOUNT_NOT_IN_TEXT"]), "GROUNDING_AMOUNT_NOT_IN_TEXT"),
37	    (L(schema_valid=False), "SCHEMA_INVALID"),
38	])
39	def test_rejected_cases(ladder, code):
40	    """ADR-005: grounding failure or schema-invalid output -> rejected, reason listed."""
41	    st, rs = C.compose_state(ladder, X())
42	    assert st == "rejected" and code in rs
43	
44	@pytest.mark.parametrize("ladder,ctx,code", [
45	    (L(code_reasons=["SUMMARY_TOKEN_NOT_IN_EXCERPT"]), X(), "SUMMARY_TOKEN_NOT_IN_EXCERPT"),
46	    (L(code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(), "SUMMARY_DROPS_QUALIFIER"),
47	    (L(code_reasons=["EXCERPT_OMITS_QUALIFIER"]), X(), "EXCERPT_OMITS_QUALIFIER"),
48	    (L(code_reasons=["EXCERPT_NOT_WHOLE_SENTENCE"]), X(), "EXCERPT_NOT_WHOLE_SENTENCE"),
49	    (L(code_reasons=["HIGHLIGHT_NOT_FOUND"]), X(), "HIGHLIGHT_NOT_FOUND"),
50	    (L(judge="partially"), X(), "JUDGE_PARTIAL"),
51	    (L(judge="unsupported"), X(), "JUDGE_UNSUPPORTED"),
52	    (L(judge="disagrees"), X(), "JUDGE_DISAGREES"),
53	    (L(judge="unsure"), X(), "JUDGE_UNSURE"),
54	    (L(judge="unavailable"), X(), "JUDGE_UNAVAILABLE"),
55	    (L(), X(fixture_miss=True), "FIXTURE_MISS"),
56	    (L(), X(date_status="ambiguous"), "DATE_AMBIGUOUS"),
57	    (L(), X(date_status="missing"), "DATE_MISSING"),
58	    (L(), X(amount_class="rate"), "AMOUNT_RATE_NOT_TOTALED"),
59	    (L(), X(amount_class="estimate"), "AMOUNT_ESTIMATE"),
60	    (L(), X(amount_class="damages"), "AMOUNT_DAMAGES"),
61	    (L(), X(amount_class="unclear"), "AMOUNT_UNCLEAR"),
62	    (L(), X(agreement="lexicon_only"), "LEXICON_ONLY"),
63	    (L(), X(agreement="llm_only"), "LLM_ONLY"),
64	    (L(), X(split_ambiguous=True), "SPLIT_AMBIGUOUS"),
65	    (L(), X(injection=True), "INJECTION_SUSPECTED"),
66	    (L(), X(endpoint_unverified=True), "ENDPOINT_NOT_VERIFIED"),   # R-FL-1: a gap whose span could contain an unconfirmed date
67	    (L(), X(llm_failed=True), "LLM_FAILED_AFTER_RETRIES"),
68	])
69	def test_needs_review_cases(ladder, ctx, code):
70	    """ADR-005 / R-TL-5: each doubt yields needs_review with its reason code."""
71	    st, rs = C.compose_state(ladder, ctx)
72	    assert st == "needs_review" and code in rs
73	
74	def test_charge_amount_class_is_not_a_doubt():
75	    """R-CH-2: amount_class 'charge' adds no reason."""
76	    assert C.compose_state(L(), X(amount_class="charge")) == ("verified", [])
77	
78	def test_agreement_both_is_not_a_doubt():
79	    """ADR-008.4: lexicon and model agree -> no LEXICON_ONLY / LLM_ONLY."""
80	    assert C.compose_state(L(), X(agreement="both")) == ("verified", [])
81	
82	def test_rejected_beats_needs_review():
83	    """ADR-005 precedence: rejected > needs_review; the rejecting reason is kept."""
84	    st, rs = C.compose_state(L(grounding_failures=["GROUNDING_EXCERPT_NOT_VERBATIM"], judge="unsupported"), X(injection=True))
85	    assert st == "rejected" and "GROUNDING_EXCERPT_NOT_VERBATIM" in rs
86	
87	def test_multiple_doubts_all_listed_once_each():
88	    """R-TL-5: several doubts -> needs_review with each reason exactly once."""
89	    st, rs = C.compose_state(L(judge="partially", code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(injection=True, date_status="ambiguous"))
90	    assert st == "needs_review"
91	    assert sorted(rs) == sorted(["JUDGE_PARTIAL", "SUMMARY_DROPS_QUALIFIER", "INJECTION_SUSPECTED", "DATE_AMBIGUOUS"])
92	
93	def test_deterministic_and_pure():
94	    """Row 17: same ladder -> same state; inputs are not mutated."""
95	    l, c = L(judge="partially"), X(injection=True)
96	    l0, c0 = dict(l), dict(c)
97	    assert C.compose_state(l, c) == C.compose_state(l, c)
98	    assert l == l0 and c == c0
99	
100	def test_context_optional():
101	    """Row 17: context may be omitted (treated as no doubt)."""
102	    assert C.compose_state(L()) == ("verified", [])
103	
104	def test_unknown_code_is_a_bug():
105	    """Closed list: an unknown reason code raises instead of passing silently."""
106	    with pytest.raises((ValueError, KeyError)):
107	        C.compose_state(L(code_reasons=["MADE_UP_CODE"]), X())
108	
109	# ---------- reason-code list and why templates (row 18)
110	def api_codes():
111	    t = (pathlib.Path(__file__).resolve().parents[2] / "memory/contracts/api.md").read_text()
112	    app = t.split("## Appendix: reason codes")[1]
113	    codes = set()
114	    for line in app.splitlines():
115	        if line.startswith("| `"):
116	            codes |= set(re.findall(r"`([A-Z][A-Z_]+)`", line.split("|")[1]))
117	    return codes
118	
119	def test_reason_codes_match_api_appendix():
120	    """Row 18 / api.md appendix: confidence.REASON_CODES equals the closed list (22+ codes)."""
121	    assert set(C.REASON_CODES) == api_codes()
122	    assert len(api_codes()) >= 22
123	
124	@pytest.mark.parametrize("code", sorted(api_codes()))
125	def test_every_reason_code_has_a_why_template(code):
126	    """Row 18: every reason code has a fixed, non-empty, plain-language template (no braces left over, no model text)."""
127	    s = W.why(code)
128	    assert isinstance(s, str) and 15 < len(s) < 300 and "{" not in s and "}" not in s
129	
130	def test_why_unknown_code_raises():
131	    """Row 18: unknown code -> KeyError (templates are a closed list)."""
132	    with pytest.raises(KeyError):
133	        W.why("NOT_A_CODE")
134	
135	def test_why_is_deterministic():
136	    """Row 18: same code -> byte-identical sentence."""
137	    assert W.why("JUDGE_PARTIAL") == W.why("JUDGE_PARTIAL")
138	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:42.579Z

Both fixes are present in code and tests. Before I accept them, I need to check that `check_amount` and the `endpoint_unverified` key are actually reached from the pipeline, not just from the unit tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:43.663Z

**tool call — Bash**
````
{
 "command": "echo \"== callers of check_amount / compose_state / endpoint_unverified (app/ and evals/ and scripts) ==\" && grep -rn \"check_amount\\|compose_state\\|endpoint_unverified\\|check_excerpt\\|check_summary\" --include=*.py . 2>/dev/null | grep -v \"^./.venv\" | grep -v \"^./tests/\" ; echo \"== gaps.py ==\" && sed -n 1,60p app/backend/gaps.py; echo \"== pipeline.py ==\" && cat app/backend/pipeline.py",
 "description": "Find production call sites for the new grounding and state functions"
}
````

### User / tool · 2026-11-02T01:50:43.768Z

**tool result**
````
== callers of check_amount / compose_state / endpoint_unverified (app/ and evals/ and scripts) ==
artifacts/review-evidence/T-030-exercise.py:19:        res = GR.check_excerpt(r["excerpt"], r["excerpt"])
artifacts/review-evidence/T-030-exercise.py:20:        res2 = GR.check_excerpt(raw, r["excerpt"])
artifacts/review-evidence/T-030-exercise.py:27:    chk(f"non-verbatim rejected: {ex!r}", GR.check_excerpt(rec2, ex) == ["GROUNDING_EXCERPT_NOT_VERBATIM"], GR.check_excerpt(rec2, ex))
artifacts/review-evidence/T-030-exercise.py:29:chk("case change rejected", GR.check_excerpt(rec2, rec2.lower()) == ["GROUNDING_EXCERPT_NOT_VERBATIM"])
artifacts/review-evidence/T-030-exercise.py:32:chk("hedge omitted -> EXCERPT_OMITS_QUALIFIER", GR.check_excerpt(rec8, dropped) == ["EXCERPT_OMITS_QUALIFIER"], GR.check_excerpt(rec8, dropped))
artifacts/review-evidence/T-030-exercise.py:34:chk("hedge sentence alone is clean", GR.check_excerpt(rec8, full) == [], GR.check_excerpt(rec8, full))
artifacts/review-evidence/T-030-exercise.py:35:chk("full excerpt clean", GR.check_excerpt(rec8, rec8) == [])
artifacts/review-evidence/T-030-exercise.py:38:print("   half-hedge:", GR.check_excerpt(rec8, half))
artifacts/review-evidence/T-030-exercise.py:40:print("   charge-only excerpt:", GR.check_excerpt(rec8, "Charge: $2,150."))
artifacts/review-evidence/T-030-exercise.py:42:print("   mid-unit:", GR.check_excerpt(rec1, "rear-ended at approx. 35 mph"))
artifacts/review-evidence/T-030-exercise.py:45:chk("'pain 4/10' over 'Pain 3/10.' -> needs_review path", "SUMMARY_TOKEN_NOT_IN_EXCERPT" in GR.check_summary("Pain 4/10.", pain), GR.check_summary("Pain 4/10.", pain))
artifacts/review-evidence/T-030-exercise.py:46:chk("'Visit 8' label passes", GR.check_summary("Visit 8: pain 3/10.", pain, label="Visit 8") == [], GR.check_summary("Visit 8: pain 3/10.", pain, label="Visit 8"))
artifacts/review-evidence/T-030-exercise.py:47:chk("drop 'without loss of consciousness' -> SUMMARY_DROPS_QUALIFIER", "SUMMARY_DROPS_QUALIFIER" in GR.check_summary("Cervical strain and concussion diagnosed.", rec2), GR.check_summary("Cervical strain and concussion diagnosed.", rec2))
artifacts/review-evidence/T-030-exercise.py:49:    st, rs = C.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": GR.check_summary(summ, exc), "judge": "supported"}, {})
artifacts/review-evidence/T-030-exercise.py:50:    chk(f"compose_state -> needs_review for {summ!r}", st == "needs_review", (st, rs))
artifacts/review-evidence/T-030-exercise.py:62:a = copy.copy(rec2); GR.check_excerpt(a, "Dx cervical strain"); chk("input unmodified", a == rec2)
artifacts/review-evidence/T-030-exercise.py:64:chk("check_amount exists (checklist #4 amount in text)", hasattr(GR, "check_amount"))
artifacts/review-evidence/T-030-exercise.py:65:chk("compose_state handles endpoint_unverified", C.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": "supported"}, {"endpoint_unverified": True})[0] == "needs_review", C.compose_state({"grounding_failures": [], "schema_valid": True, "code_reasons": [], "judge": "supported"}, {"endpoint_unverified": True}))
artifacts/review-evidence/T-030-exercise.py:74:chk("deterministic", GR.check_excerpt(rec8, dropped) == GR.check_excerpt(rec8, dropped))
app/backend/confidence.py:1:"""compose_state(ladder, context) -> (state, reasons)  (ADR-005, R-TL-5, LLM_VS_CODE row 17). Pure and deterministic.
app/backend/confidence.py:44:             "endpoint_unverified"}
app/backend/confidence.py:47:def compose_state(ladder: dict, context: dict = None):
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
app/backend/judges.py:90:    """Map a judge's own enum to the compose_state vocabulary. Only the positive verdict becomes 'supported';
app/backend/generator.py:3:state is composed by code (confidence.compose_state). A failing quote is never repaired: it is rejected and stays out of the timeline.
app/backend/generator.py:69:    exc_reasons = grounding.check_excerpt(body, excerpt)
app/backend/generator.py:74:        code_reasons += grounding.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
app/backend/generator.py:104:    state, reasons = confidence.compose_state(
app/backend/grounding.py:4:check_excerpt: reason codes for a model/user excerpt against its record. check_summary: token and dropped-qualifier checks.
app/backend/grounding.py:87:def check_excerpt(record_text: str, excerpt: str) -> list:
app/backend/grounding.py:110:def check_amount(record_text: str, raw_amount: str) -> list:
app/backend/grounding.py:196:def check_summary(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
tests/unit/test_grounding.py:15:    assert GR.check_excerpt(r, "Discharged from PT after two missed appointments. Pain 3/10.") == []
tests/unit/test_grounding.py:19:    assert GR.check_excerpt(R8, "C5-C6 disc herniation with mild right foraminal narrowing.") == ["GROUNDING_EXCERPT_NOT_VERBATIM"]
tests/unit/test_grounding.py:24:    assert GR.check_excerpt(r, "Fracture alignment satisfactory. Continue splint 3 weeks. No driving.") == []
tests/unit/test_grounding.py:28:    assert "EXCERPT_NOT_WHOLE_SENTENCE" in GR.check_excerpt(R8, "disc protrusion with mild right foraminal narrowing")
tests/unit/test_grounding.py:32:    assert GR.check_excerpt(R8, FINDING) == ["EXCERPT_OMITS_QUALIFIER"]
tests/unit/test_grounding.py:36:    assert GR.check_excerpt(R8, FINDING + " " + HEDGE_UNITS) == []
tests/unit/test_grounding.py:40:    assert GR.check_excerpt(R8, FINDING + " Findings may represent degenerative change;") == ["EXCERPT_OMITS_QUALIFIER"]
tests/unit/test_grounding.py:44:    assert GR.check_excerpt(G.record("sample", 3)["excerpt"], "Persistent neck pain 6/10, daily headaches.") == []
tests/unit/test_grounding.py:45:    assert GR.check_excerpt(G.record("sample", 5)["excerpt"], "Pain 4/10, improving.") == []
tests/unit/test_grounding.py:49:    assert GR.check_excerpt(G.record("sample", 6)["excerpt"], "Discharged from PT after two missed appointments.") == []
tests/unit/test_grounding.py:85:    return GR.check_summary(summary, excerpt, label, date)
tests/unit/test_grounding.py:128:    """R-TL-10 / R-EX-6: all 9 summaries in sample.export.expected.txt pass check_summary against their own quote, label and date."""
tests/unit/test_grounding.py:138:        assert GR.check_summary(summ, quote, m.group(2), iso) == [], summ
tests/unit/test_grounding.py:148:        out = GR.check_summary(se["new_summary"], "Pain 4/10, improving." if se["record_no"] == 5 else r["excerpt"], row["source"], row["date"])
tests/unit/test_grounding.py:158:    assert GR.check_amount(G.record("sample", 2)["excerpt"], "$6,240") == []
tests/unit/test_grounding.py:163:    assert GR.check_amount(G.record("sample", 2)["excerpt"], raw) == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_grounding.py:168:    assert GR.check_amount(t, "$1,2OO") == [] and GR.check_amount(t, "$1,200") == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_confidence.py:1:"""compose_state table + why templates. R-TL-5, ADR-005, LLM_VS_CODE rows 17 and 18.
tests/unit/test_confidence.py:7:          "split_ambiguous": bool, "llm_failed": bool, "endpoint_unverified": bool}
tests/unit/test_confidence.py:15:CTX = dict(injection=False, date_status="parsed", amount_class=None, agreement=None, fixture_miss=False, split_ambiguous=False, llm_failed=False, endpoint_unverified=False)
tests/unit/test_confidence.py:24:    assert C.compose_state(L(), X()) == ("verified", [])
tests/unit/test_confidence.py:28:    assert C.compose_state(L(judge=None), X()) == ("verified", [])
tests/unit/test_confidence.py:32:    assert C.compose_state(L(), X(date_status="confirmed")) == ("verified", [])
tests/unit/test_confidence.py:41:    st, rs = C.compose_state(ladder, X())
tests/unit/test_confidence.py:66:    (L(), X(endpoint_unverified=True), "ENDPOINT_NOT_VERIFIED"),   # R-FL-1: a gap whose span could contain an unconfirmed date
tests/unit/test_confidence.py:71:    st, rs = C.compose_state(ladder, ctx)
tests/unit/test_confidence.py:76:    assert C.compose_state(L(), X(amount_class="charge")) == ("verified", [])
tests/unit/test_confidence.py:80:    assert C.compose_state(L(), X(agreement="both")) == ("verified", [])
tests/unit/test_confidence.py:84:    st, rs = C.compose_state(L(grounding_failures=["GROUNDING_EXCERPT_NOT_VERBATIM"], judge="unsupported"), X(injection=True))
tests/unit/test_confidence.py:89:    st, rs = C.compose_state(L(judge="partially", code_reasons=["SUMMARY_DROPS_QUALIFIER"]), X(injection=True, date_status="ambiguous"))
tests/unit/test_confidence.py:97:    assert C.compose_state(l, c) == C.compose_state(l, c)
tests/unit/test_confidence.py:102:    assert C.compose_state(L()) == ("verified", [])
tests/unit/test_confidence.py:107:        C.compose_state(L(code_reasons=["MADE_UP_CODE"]), X())
== gaps.py ==
"""Treatment gaps, computed by code over code-parsed header dates of clinical-encounter records (ADR-010, D-003, R-FL-1, row 9).
Entry state, review status and LLM output have no influence. Strictly more than 30 calendar days flags (30 is not a gap, 31 is).
Ambiguous or missing dates and non-encounter records (billing statements, phone notes) are never endpoints."""
from app.backend import dates, flag_templates
from app.backend.ingest import evidence_span

THRESHOLD_DAYS = 30


def is_gap(days: int) -> bool:
    return days > THRESHOLD_DAYS


def compute_gaps(records: list) -> list:
    """[{from_date, to_date, from_records, to_records, days, flag}] between consecutive DISTINCT encounter dates."""
    by_date = {}
    for r in records:
        if r.get("kind", "encounter") == "encounter" and r.get("date_iso"):
            by_date.setdefault(r["date_iso"], []).append(r["n"])
    ds = sorted(by_date)
    out = []
    for a, b in zip(ds, ds[1:]):
        n = dates.days_between(a, b)
        out.append({"from_date": a, "to_date": b, "from_records": sorted(by_date[a]), "to_records": sorted(by_date[b]),
                    "days": n, "flag": is_gap(n)})
    return out


def _reasons(gap: dict, records: list) -> list:
    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
    reasons = []
    for r in records:
        if r.get("kind", "encounter") != "encounter" or r.get("date_iso"):
            continue
        cands = r.get("date_candidates") or []
        if not cands or any(gap["from_date"] <= c <= gap["to_date"] for c in cands):
            reasons.append("ENDPOINT_NOT_VERIFIED")
            break
    ends = set(gap["from_records"]) | set(gap["to_records"])
    if any(r.get("injection_tag") for r in records if r["n"] in ends):
        reasons.append("INJECTION_SUSPECTED")
    return reasons


def gap_flags(records: list) -> list:
    """One flag per gap over 30 days, id keyed by the bounding record pair; text from flag_templates only."""
    by_n = {r["n"]: r for r in records}
    flags = []
    for g in compute_gaps(records):
        if not g["flag"]:
            continue
        a, b = g["from_records"][-1], g["to_records"][0]
        title, expl = flag_templates.render("gap", "gap_over_30", days=g["days"], from_date=g["from_date"], to_date=g["to_date"],
                                            provider_a=by_n[a].get("source"), provider_b=by_n[b].get("source"))
        ev = [evidence_span(by_n[n], f) for n in (a, b) for f in ("date", "source")]
        flags.append({"id": f"f_gap_r{a}_r{b}", "type": "gap", "category": "gap_over_30", "origin": "code", "title": title,
                      "explanation": expl, "from_date": g["from_date"], "to_date": g["to_date"], "days": g["days"],
                      "record_nos": sorted(set(g["from_records"]) | set(g["to_records"])), "evidence": ev, "reasons": _reasons(g, records)})
    return flags

== pipeline.py ==
"""STUB (qa, T-048): backend replaces. Pipeline stages per app/README-arch.md; see tests/unit/test_pipeline.py."""
def __getattr__(name):
    raise NotImplementedError(name)
def run_ingest(raw_text: str): raise NotImplementedError
def run_pipeline(conn, case_id: str, raw_text: str, *, call, now=None, deadline_s: float = 480): raise NotImplementedError
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:44.415Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ 2>/dev/null; echo \"---\"; ls app/ ; echo \"---\"; ls memory/contracts 2>/dev/null | head; echo \"--- git?\"; git rev-parse --is-inside-work-tree 2>&1 | head -1; git log --oneline -5 2>&1 | head -5",
 "description": "Check app layout, evidence dir and git state"
}
````

### User / tool · 2026-11-02T01:50:44.546Z

**tool result**
````
M0-r2-staff-resolution.md
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-001-r2-readonly-repros.txt
T-001-r3-repro.out.txt
T-001-r3-repro.sh
T-002-curl.txt
T-002-r2-activity-390.png
T-002-r2-board-390.png
T-002-r2-csrf-curl.txt
T-002-r2-inbox-390.png
T-002-r2-milestones-390.png
T-002-r2-personas-390.png
T-002-r2-state-390.png
T-002-r2-xss.json
T-002-r3-404.py
T-002-r3-activity-390.png
T-002-r3-board-390.png
T-002-r3-inbox-390.png
T-002-r3-milestones-390.png
T-002-r3-personas-390.png
T-002-r3-probe.out.txt
T-002-r3-probe.py
T-002-r3-state-390.png
T-002-r3-ui.out.txt
T-002-r3-ui.py
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-r2-commit-secret-probe.out.txt
T-003-r2-commit-secret-probe.py
T-003-r2-git-guard-results.txt
T-003-r2-probe-board2.out.txt
T-003-r2-probe-board2.py
T-003-r2-probe-corpus.txt
T-003-r2-probe-direct.out.txt
T-003-r2-probe-direct.out2.txt
T-003-r2-probe-direct.py
T-003-r3-probe-board2.out.txt
T-003-r3-probe-corpus.out.txt
T-003-r3-probe-corpus.py
T-003-r3-probe-direct.out.txt
T-003-r3-probe-legit.out.txt
T-003-r3-probe-legit.py
T-003-r3-probe-pwd.out.txt
T-003-r3-probe-pwd.py
T-003-r3-probe-rwg.out.txt
T-003-r3-probe-rwg.py
T-003-r3-probe-targeted.out.txt
T-003-r3-probe-targeted.py
T-003-r3-probe-targeted2.out.txt
T-003-r3-probe-targeted2.py
T-003-reviewer-write-guard-probe.txt
T-004-agent-check.txt
T-004-r2-agent-sync.txt
T-004-r2-board-guard-probe.py
T-004-r2-board-guard-probe.txt
T-004-r2-shell-write-probe.txt
T-004-r3-board-guard-probe.out.txt
T-004-r3-board-guard-probe.py
T-005-r2-pathcheck.py
T-006-check-secrets-probe.txt
T-006-r2-chain-probe.out.txt
T-006-r2-chain-probe.py
T-006-r2-fp-probe.out.txt
T-006-r2-fp-probe.py
T-006-r2-probe.out.txt
T-006-r2-probe.py
T-006-r3-chain-probe.out.txt
T-006-r3-commit-paths-probe.out.txt
T-006-r3-commit-paths-probe.py
T-006-r3-fp-probe.out.txt
T-006-r3-probe.out.txt
T-006-rename-probe.txt
T-008-adjuster-source-checks.txt
T-008-r2-adjuster.md
T-008-r2-src
T-008-r3-adjuster-greps.txt
T-008-r3-adjuster-hits.md
T-008-r3-insurancejournal-854959.html
T-008-r3-insurancejournal-checks.txt
T-009-adjuster-probes.py
T-009-adjuster-probes.txt
T-009-nurse-golden-scan.txt
T-009-nurse-probe-output.txt
T-009-nurse-probe.py
T-009-nurse-probes.txt
T-009-r2-nurse-probe-output.txt
T-009-r2-nurse-probe.py
T-009-r2-nurse-variants-output.txt
T-009-r2-nurse-variants.py
T-009-r2-resolution.md
T-010-011-sections.txt
T-010-011-source-check.md
T-010-litlead-source-check.md
T-010-r2-count.py
T-010-r2-resolution.md
T-010-r2-srch.py
T-010-r3-check.py
T-010-r3-resolution.md
T-011-r2-check.py
T-012-h2t.py
T-012-r2-fetch.py
T-012-r2-resolution.md
T-012-source-check.md
T-013-paralegal-walkthrough.md
T-013-r2-paralegal-jsoncheck.py
T-013-r2-paralegal-walk.out.txt
T-013-r2-paralegal-walk.py
T-013-r2-resolution.md
T-013-r3-paralegal-golden-cmp.out.txt
T-013-r3-paralegal-golden-cmp.py
T-013-r3-paralegal-jsoncheck.py
T-013-r3-paralegal-walk.out.txt
T-013-r3-paralegal-walk.py
T-013-r3-resolution.md
T-013-r3check.py
T-013-trace.md
T-014-amount-cue-demo.py
T-014-injection-trace.md
T-014-json-check.out
T-014-json-check.py
T-014-r2-amount-demo.py
T-014-r2-amount-sim.out
T-014-r2-amount-sim.py
T-014-r2-json-check.out
T-014-r2-offset-check.out
T-014-r2-offset-check.py
T-014-r2-privacy-resolution.md
T-014-r2-staff-resolution.md
T-014-r3-amount-demo.out
T-014-r3-amount-demo.py
T-014-r3-amount-sim.out
T-014-r3-amount-sim.py
T-014-r3-resolution.md
T-014-walkthrough.md
T-015-legal-nurse-items.md
T-015-paralegal-blind.md
T-015-paralegal-regex-probe.out.txt
T-015-paralegal-regex-probe.py
T-015-r2-nurse-probe.out.txt
T-015-r2-nurse-probe.py
T-015-r2-nurse.md
T-015-r2-paralegal-jsoncheck.py
T-015-r2-paralegal-probe.out.txt
T-015-r2-paralegal-probe.py
T-015-r2-paralegal.md
T-015-r3-paralegal-entries.out.txt
T-015-r3-paralegal-entries.py
T-015-r3-paralegal-jsoncheck.py
T-015-r3-paralegal-mutation.out.txt
T-015-r3-paralegal-mutation.py
T-015-r3-paralegal-probe.out.txt
T-015-r3-paralegal-probe.py
T-015-r3-paralegal-rerun-of-r2-probe.out.txt
T-015-r3-paralegal-s6diff.out.txt
T-015-r3-paralegal-s6diff.py
T-015-r3-rerun-of-r2-nurse-probe.out.txt
T-015-r4-paralegal-jsoncheck.out.txt
T-015-r4-paralegal-jsoncheck.py
T-015-r4-paralegal-recheck.out.txt
T-015-r4-paralegal-recheck.py
T-017-r3-owner-probe.out.txt
T-017-r3-owner-probe.py
T-018-contract-probe.out.txt
T-018-contract-probe.py
T-018-r2-applied-check.out.txt
T-018-r2-applied-check.py
T-018-r3-applied-check.out.txt
T-025-pm-probe.out.txt
T-025-pm-probe.py
T-025-pm-r2-probe.out.txt
T-025-pm-r2-probe.py
T-026-desktop-dialog.png
T-026-desktop-office.png
T-026-mobile-dialog.png
T-026-mobile-office.png
T-026-ux-designer-office.py
T-027-nurse-fresh-probe.py
T-027-nurse-fresh.txt
T-028-r2-checks.py
T-028-r2-json-check.py
T-028-review-checks.py
T-028-review-json-check.py
T-030-exercise.py
T-031-ac_check.out
T-031-ac_check.py
T-031-mutation.out
T-031-mutation.py
T-031-r2-check.out
T-031-r2-check.py
T-031-r2-verdict-check.py
T-032-ingest.py
T-047-desktop-1440-dialog.png
T-047-desktop-1440-forced-reviewing.png
T-047-desktop-1440.png
T-047-mobile-390-dialog.png
T-047-mobile-390-full.png
T-047-mobile-390-nav-onload.png
T-047-mobile-390.png
T-047-ux-designer-ac2-forced.py
T-047-ux-designer-check.py
T-047-ux-designer-nav-keyboard.py
T-049-served-index.html
T-049-ux-designer-01-board-390.png
T-049-ux-designer-02-office-390.png
T-049-ux-designer-03-fullscreen-390.png
T-049-ux-designer-04-view-office-390.png
T-049-ux-designer-check.out.json
T-049-ux-designer-check.py
__pycache__
---
README-arch.md
__init__.py
backend
db
frontend
llm
---
api.md
--- git?
true
a2fc95a feat(backend): generator, judges J1-J4, schemas, versioned prompts (T-035)
810fec1 fix(db): add_item rejects edits, AST guard for review_status/edited_json writers (T-031 r2 majors)
1365926 fix(backend): check_amount, endpoint_unverified, strict keys (T-030 r2)
a3d8df9 fix(backend): ingest keeps unsplit text, 2-digit years ambiguous, proof tests (T-032 r2)
958c353 feat(backend): LLM provider, claude-cli/anthropic-api/fixture backends, audited retries, recorder (T-034)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:49.201Z

Git is available here and the log shows `1365926 fix(backend): check_amount, endpoint_unverified, strict keys (T-030 r2)`. Next I'll read the generator's call sites and the gap-flag state path to see whether either fix reaches a real output.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:49.971Z

**tool call — Bash**
````
{
 "command": "sed -n 55,120p app/backend/generator.py; echo \"== grep flag state consumers ==\"; grep -rn \"gap_flags\\|compute_gaps\\|\\\"reasons\\\"\\|'reasons'\\|needs_review\" app/backend/*.py | grep -v \"^app/backend/confidence.py\" | head -40",
 "description": "Read generator compose path and gap flag consumers"
}
````

### User / tool · 2026-11-02T01:50:50.068Z

**tool result**
````
    e["ladder"] = {"item_id": e["id"], "generator": {"model": judges.generator_model(), "prompt_version": prompt.name,
                                                      "call_id": call_id, "output": out if isinstance(out, dict) else None},
                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
    try:
        o = schemas.ExtractOutput.model_validate(out)
    except (ValidationError, TypeError, ValueError):
        e.update(summary="", excerpt="", excerpt_start=None, excerpt_end=None, source_kind="record")
        return compose(e, record, grounding_failures=["SCHEMA_INVALID"], schema_valid=False)
    return verify(e, record, o.summary, o.excerpt)


def verify(e: dict, record: dict, summary: str, excerpt: str) -> dict:
    """Stage 2 (code): grounding of the excerpt, summary token/qualifier checks, offsets. Never edits the model's text."""
    body = record["excerpt"]
    exc_reasons = grounding.check_excerpt(body, excerpt)
    failures = [c for c in exc_reasons if c in confidence.REJECTED_CODES]
    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
    span = grounding.locate(body, excerpt)
    if not failures:
        code_reasons += grounding.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
        if span is None:
            code_reasons.append("HIGHLIGHT_NOT_FOUND")
    base = body_offset(record)
    e.update(summary=summary, excerpt=excerpt,
             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
             source_kind="patient_report" if grounding.has_self_report(excerpt) else "record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
              date_provider_from_header=True,
              summary_tokens_not_in_excerpt=grounding.new_tokens(summary, excerpt, record["source"], record.get("date_iso") or "") if not failures else [],
              highlight_found=span is not None)
    return compose(e, record, grounding_failures=failures, code_reasons=list(dict.fromkeys(code_reasons)))


def compose(e: dict, record: dict, *, grounding_failures=None, code_reasons=None, schema_valid=True, judge="__keep__", fixture_miss=False) -> dict:
    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
    lad = e["ladder"]
    st = e.setdefault("_stage", {})
    if grounding_failures is not None:
        st["grounding_failures"] = grounding_failures
    if code_reasons is not None:
        st["code_reasons"] = code_reasons
    st.setdefault("code_reasons", [])
    st.setdefault("grounding_failures", [])
    st["schema_valid"] = schema_valid and st.get("schema_valid", True)
    if judge != "__keep__":
        st["judge"] = judge
    st["fixture_miss"] = fixture_miss or st.get("fixture_miss", False)
    state, reasons = confidence.compose_state(
        {"grounding_failures": st["grounding_failures"], "schema_valid": st["schema_valid"], "code_reasons": st["code_reasons"],
         "judge": st.get("judge")}, _ctx(record, fixture_miss=st["fixture_miss"]))
    e["state"], e["reasons"] = state, reasons
    e["why"] = " ".join(why.why(c) for c in reasons) if reasons else "Quote found word for word, every number in the summary is in the quote, and the second check agreed."
    lad["state"] = state
    return e


def _one(args):
    record, group, call, case_text = args
    return extract_one(record, group, call=call, case_text=case_text)


def extract_entries(records: list, groups: list, *, call, case_text: str = "", workers: int = CONCURRENCY):
    """Stages 1-2 over distinct records (only the first record of each duplicate group is sent). Returns
    (entries, rejected, failures). `entries` are chronological by (date, seq) and never contain a rejected item; `rejected` goes to the
== grep flag state consumers ==
app/backend/generator.py:91:    """Set e['state'], e['reasons'], e['why'] from e['_stage'] (private inputs; callers drop '_' keys when storing). Re-run after the judge."""
app/backend/generator.py:107:    e["state"], e["reasons"] = state, reasons
app/backend/gaps.py:14:def compute_gaps(records: list) -> list:
app/backend/gaps.py:30:    """needs_review reasons: an undated/ambiguous encounter record whose date could fall inside the span (ADR-010), or an injection-tagged endpoint."""
app/backend/gaps.py:45:def gap_flags(records: list) -> list:
app/backend/gaps.py:49:    for g in compute_gaps(records):
app/backend/gaps.py:58:                      "record_nos": sorted(set(g["from_records"]) | set(g["to_records"])), "evidence": ev, "reasons": _reasons(g, records)})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:50:53.494Z

**tool call — Bash**
````
{
 "command": "echo \"== _ctx ==\" && grep -n \"def _ctx\" -A 12 app/backend/generator.py; echo \"== reasons/state readers in backend ==\" && grep -rn \"\\[\\\"reasons\\\"\\]\\|\\.get(\\\"reasons\\\"\\|\\\"state\\\"\\]\\|get(\\\"state\\\"\" app/backend/*.py | head -30; echo \"== check_amount call sites in whole repo excluding tests and evidence ==\"; grep -rn \"check_amount\" --include=*.py --include=*.md . | grep -v \"^./.venv\" | grep -v \"^./tests/\" | grep -v \"^./artifacts/\"; echo \"== dedupe: api/frontend mention of endpoint ==\"; grep -rn \"ENDPOINT_NOT_VERIFIED\" --include=*.py --include=*.md --include=*.js --include=*.html . | grep -v \"^./.venv\" | head",
 "description": "Inspect context builder and reason/state readers"
}
````

### User / tool · 2026-11-02T01:50:53.617Z

**tool result**
````
== _ctx ==
33:def _ctx(record: dict, **extra) -> dict:
34-    return {"injection": bool(record.get("injection_tag")), "date_status": record.get("date_status", "parsed"), **extra}
35-
36-
37-def _entry_base(record: dict, group: list, case_text: str) -> dict:
38-    return {"id": f"e{record['n']}", "seq": record["n"], "record_id": record["id"], "record_ids": [f"r{n}" for n in group],
39-            "date": record.get("date_iso"), "date_status": record.get("date_status", "parsed"),
40-            "provider": record["source"], "ai_drafted": True, "review_status": "pending"}
41-
42-
43-def extract_one(record: dict, group: list, *, call, case_text: str = "") -> dict:
44-    """One generator call. Returns an entry dict (pre-judge) or {'failure': code, 'record_no': n} when no output exists."""
45-    step, item = "extract", f"e{record['n']}"
== reasons/state readers in backend ==
app/backend/generator.py:107:    e["state"], e["reasons"] = state, reasons
app/backend/generator.py:109:    lad["state"] = state
app/backend/generator.py:128:    entries = sorted((e for e in made if e["state"] != "rejected"), key=lambda e: (e["date"] or "9999-99-99", e["seq"]))
app/backend/generator.py:129:    rejected = [e for e in made if e["state"] == "rejected"]
app/backend/generator.py:136:        if e["state"] == "rejected":
== check_amount call sites in whole repo excluding tests and evidence ==
artifacts/review-evidence/T-030-exercise.py:64:chk("check_amount exists (checklist #4 amount in text)", hasattr(GR, "check_amount"))
app/backend/grounding.py:110:def check_amount(record_text: str, raw_amount: str) -> list:
board/cards/T-030.md:46:    - [major] Amount-in-text grounding check (check_amount) not implemented — fix: Add check_amount(record_text, raw_amount) -> [] or ['GROUNDING_AMOUNT_NOT_IN_TEXT'] using the same whitespace normalization as locate; no digit repair.
board/cards/T-030.md:58:Round 2: added grounding.check_amount (5 tests green), compose_state honours endpoint_unverified (1 test green) and raises on unknown ladder/context keys, lexicon loader raises on pattern-less hedge/self_report entries, summary-side hedge words documented as intentionally looser. 250 pass across grounding/confidence/sentences/boundaries/judges/schemas. Not done: AC-named no-silent-repair test (tests are qa-owned; check_excerpt returns only code lists, never mutates).
board/cards/T-035.md:39:- 2026-11-02T01:50:00Z backend: Built against stubs of audited/provider (call(step,system,user,schema,*,item_id)->(out,call_id)); T-034 not needed to unit-test. Also implemented J3/J4 + prompts judge_conflict_v1/judge_flag_v1 and schemas.FlagPass for T-036 (backend-2: reuse, don't re-add). Added grounding.check_amount + confidence endpoint_unverified (new T-029 tests).
board/cards/T-029.md:52:    - [major] No test for the amount-in-text grounding check (GROUNDING_AMOUNT_NOT_IN_TEXT) — fix: Add to test_grounding.py a check_amount(record_text, raw/cents) suite: $6,240 in sample record 2 passes; '$6,420' or '$9,000' absent from text returns ['GROUNDING_AMOUNT_NOT_IN_TEXT']; '$1,2OO' is not auto-corrected to $1,200.
board/cards/T-029.md:67:Review fixes: check_amount tests (3 absent, noisy not auto-corrected), duplicate-record-2 paste counts ER charge once (date+provider+text key) + date+provider-only key must not merge, ENDPOINT_NOT_VERIFIED row (ctx key endpoint_unverified), boundary scan adds urllib.request/importlib/ctypes, __init__ chains, dynamic-import calls; sentence tests aligned to backend (4th unit; mg. per D-021). grounding.check_amount is not yet in backend grounding.py (red AttributeError until added).
tests/unit/test_grounding.py:158:    assert GR.check_amount(G.record("sample", 2)["excerpt"], "$6,240") == []
tests/unit/test_grounding.py:163:    assert GR.check_amount(G.record("sample", 2)["excerpt"], raw) == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
tests/unit/test_grounding.py:168:    assert GR.check_amount(t, "$1,2OO") == [] and GR.check_amount(t, "$1,200") == ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
reviews/T-030-staff-engineer.md:3:Verdict: **changes**. No blockers. Two majors: `check_amount` is not implemented (checklist #4), and `compose_state` has no code path for `endpoint_unverified`, so it fails open to `verified`. Both are red in the shipped suite.
reviews/T-030-staff-engineer.md:34:  {"severity": "major", "title": "Amount-in-text grounding check (check_amount) not implemented",
reviews/T-030-staff-engineer.md:35:   "evidence": "grounding.py has no check_amount (exercise script: 'FAIL check_amount exists'). pytest: tests/unit/test_grounding.py::test_amount_present_in_record_passes, ::test_amount_absent_from_record_is_rejected[$6,420|$9,000|$62,400] and ::test_noisy_amount_not_autocorrected fail with AttributeError: module 'app.backend.grounding' has no attribute 'check_amount' (test_grounding.py:158-168).",
reviews/T-030-staff-engineer.md:37:   "fix": "Add check_amount(record_text, raw_amount) -> [] or ['GROUNDING_AMOUNT_NOT_IN_TEXT'] using the same whitespace normalization as locate; no digit repair.",
reviews/T-030-staff-engineer.md:38:   "acceptance_test": "pytest tests/unit/test_grounding.py -k amount green; stubbing check_amount to return [] makes test_amount_absent_from_record_is_rejected red"},
reviews/T-029-staff-engineer.md:36:   "evidence": "grep -n 'amount\\|check_amount' tests/unit/test_grounding.py returns only case_04 lines (23, 75); GROUNDING_AMOUNT_NOT_IN_TEXT appears only as a string in test_confidence.py rejected-cases. Checklist #4 requires each amount to appear in the record text.",
reviews/T-029-staff-engineer.md:38:   "fix": "Add to test_grounding.py a check_amount(record_text, raw/cents) suite: $6,240 in sample record 2 passes; '$6,420' or '$9,000' absent from text returns ['GROUNDING_AMOUNT_NOT_IN_TEXT']; '$1,2OO' is not auto-corrected to $1,200.",
reviews/T-029-staff-engineer-r2.md:5:Run: `.venv/bin/python -m pytest tests/unit -q` -> `215 failed, 284 passed, 4 errors`. T-030 and T-032 have since landed, so the failures are no longer all NotImplementedError. The 6 failures in test_boundaries, test_confidence, test_grounding and test_sentences are the new r2 tests (see the T-030 review): 5 are `AttributeError: ... no attribute 'check_amount'` and 1 is ENDPOINT_NOT_VERIFIED.
reviews/T-029-staff-engineer-r2.md:19:  "grep -n 'GROUNDING_AMOUNT_NOT_IN_TEXT\\|check_amount' tests/unit/*.py -> test_grounding.py:155-168, test_confidence.py:36",
== dedupe: api/frontend mention of endpoint ==
artifacts/review-evidence/T-014-walkthrough.md:10:| 73-day gap (r6 2026-03-06 -> r7 2026-05-18) | stage `gaps`, row 9, `gaps.py` | C (date arithmetic) | unit tests 29/30/31; state `verified` if both endpoints verified | Row 9 / api f1 compute over "consecutive dated **entries**", not over code-parsed **record** dates. If an entry is rejected or fails (LLM_FAILED_AFTER_RETRIES), it is not in the sequence. Recomputed: with r5 absent, r4 (01-23) -> r6 (03-06) = **42 days**, a false >30 gap whose endpoints r4 and r6 are both `verified`. With r6 absent, the true 73-day gap becomes r5 -> r7 = **87 days**. ENDPOINT_NOT_VERIFIED only covers the two endpoints, not an intervening missing entry. See finding F2. |
app/backend/why.py:19:    "ENDPOINT_NOT_VERIFIED": "One end of this gap could involve a date that has not been confirmed.",
app/backend/confidence.py:9:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:64:                      ("injection", "INJECTION_SUSPECTED"), ("endpoint_unverified", "ENDPOINT_NOT_VERIFIED"), ("llm_failed", "LLM_FAILED_AFTER_RETRIES")):
memory/DECISIONS.md:147:    - **needs_review**: any doubt, with reasons listed. Includes: judge verdict other than the positive one (partial, unsupported, disagrees, unsure) or judge unavailable (`JUDGE_UNAVAILABLE`, including a fixture miss on a re-check, `FIXTURE_MISS`); a summary token not in the excerpt or a qualifier of the excerpt missing from the summary (ADR-012, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`); a hedge sentence the excerpt omits or an excerpt that is not whole sentences; date ambiguous or missing; amount kind other than `charge`; lexicon and model disagree on a flag; the item's source record carries an injection tag, or it came from the cross-record pass in a case with any tagged record; a gap flag whose span could contain an unconfirmed date (`ENDPOINT_NOT_VERIFIED`); highlight offset not found; a failed run step.
memory/DECISIONS.md:214:- Decision: at ingest, code takes the header date of every non-duplicate **clinical-encounter** record (billing statements, ledgers, phone notes and similar are excluded by a `non_encounter` source-label lexicon, D-003; they still become entries), parses it (explicit format list, never guessed), sorts by (date, seq) and emits a gap flag for each consecutive pair more than 30 calendar days apart (30 is not a gap, 31 is). Entry state, review status and LLM output have no influence. A record whose date is ambiguous or missing is excluded from the arithmetic, listed in `dates_to_confirm`, and gets a `record_warning` flag (category `date_ambiguous`; D-013) plus case warning `DATE_EXCLUDED_FROM_GAPS`; any gap flag whose span could contain one of its candidate dates (or, for a missing date, every gap flag) is `needs_review` with `ENDPOINT_NOT_VERIFIED`. Confirming an ambiguous date (`confirm_date`, ADR-005) recomputes gap flags (ADR-002). Template wording: "Gap of {days} days between {date A} ({source A}) and {date B} ({source B})". Evidence is the header `Date:` and `Source:` spans of the two bounding records, plus their entry excerpts when an entry exists and is not rejected. A record with `encounter=false` never causes `ENDPOINT_NOT_VERIFIED` and never changes gap math when its date is confirmed. A bounding record carrying an injection tag makes the flag `needs_review`; its date still counts, because the date is parsed by code.
memory/DECISIONS.md:216:- Alternatives considered: gaps over verified entries (couples a fact to model success); gaps over all entries with `ENDPOINT_NOT_VERIFIED` (still produces a wrong number).
board/cards/T-014.md:82:    - [major] M3 The confirm_date example adds a phone note to gap math, contradicting D-003, ADR-010 and golden case_01 — fix: Change the example to a case where an encounter record's date is ambiguous (or show gap_flags: [] and removed_flag_ids for case_01 r8), delete the 'come from golden case_01' sentence, and add to ADR-010: a record with encounter=false never causes ENDPOINT_NOT_VERIFIED and
board/cards/T-030.md:47:    - [major] compose_state ignores endpoint_unverified and fails open to verified — fix: Add ('endpoint_unverified', 'ENDPOINT_NOT_VERIFIED') to the boolean table at confidence.py:55.
app/backend/gaps.py:37:            reasons.append("ENDPOINT_NOT_VERIFIED")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:11.884Z

Both fixes are reachable from the unit tests. I still need to check whether the amount gate and the endpoint reason reach any production output. I'll probe `check_amount` at its boundaries and check the schema and gap tests.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:14.464Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I - <<'EOF'\nimport sys; sys.path.insert(0, \"/Users/arsis/zlayt-pm-project\")\nfrom app.backend import grounding as GR\nfrom app.backend import confidence as C\ncases = [\n (\"Charge: $6,240.\", \"$6,240\"),\n (\"Charge: $6,240.\", \"240\"),\n (\"Charge: $1,850.\", \"850\"),\n (\"Charge per visit $185.\", \"$185\"),\n (\"Charge: $1,850.\", \"$185\"),\n (\"Charge: $1,850.\", \"1,850\"),\n (\"Charge: $1,2OO.\", \"$1,200\"),\n (\"Charge: $1,2OO.\", \"$1,2OO\"),\n (\"Paid 1850 dollars.\", \"850\"),\n (\"Visit 2026-01-09 $185.\", \"09\"),\n (\"Total $62,400.\", \"$6,240\"),\n (\"Total $6,240.\", \"\"),\n]\nfor t, a in cases:\n    print(repr(t), repr(a), \"->\", GR.check_amount(t, a))\nprint(\"compose endpoint:\", C.compose_state({\"grounding_failures\": [], \"schema_valid\": True, \"code_reasons\": [], \"judge\": \"supported\"}, {\"endpoint_unverified\": True}))\nprint(\"compose unknown key:\", end=\" \")\ntry:\n    C.compose_state({\"grounding_failures\": [], \"schema_valid\": True, \"code_reasons\": [], \"judge\": \"supported\"}, {\"injecton\": True}); print(\"NO RAISE\")\nexcept ValueError as e: print(\"ValueError:\", e)\nEOF\necho \"== schemas amount fields ==\"; grep -n \"amount\\|class \" app/backend/schemas.py | head -30; echo \"== totals.py ==\"; cat app/backend/totals.py; echo \"== gap tests ==\"; ls tests/unit/ | head -50; grep -rln \"gap_flags\\|compute_gaps\" tests/unit/ ",
 "description": "Probe check_amount boundaries and compose_state with -I isolated Python"
}
````

### User / tool · 2026-11-02T01:51:14.608Z

**tool result**
````
'Charge: $6,240.' '$6,240' -> []
'Charge: $6,240.' '240' -> []
'Charge: $1,850.' '850' -> []
'Charge per visit $185.' '$185' -> []
'Charge: $1,850.' '$185' -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']
'Charge: $1,850.' '1,850' -> []
'Charge: $1,2OO.' '$1,200' -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']
'Charge: $1,2OO.' '$1,2OO' -> []
'Paid 1850 dollars.' '850' -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']
'Visit 2026-01-09 $185.' '09' -> []
'Total $62,400.' '$6,240' -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']
'Total $6,240.' '' -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']
compose endpoint: ('needs_review', ['ENDPOINT_NOT_VERIFIED'])
compose unknown key: ValueError: unknown ladder/context keys: ['injecton']
== schemas amount fields ==
2:The generator returns {summary, excerpt} only: no provider, date, amount or clinical-facts field (code supplies those).
9:class _Closed(BaseModel):
13:class ExtractOutput(_Closed):
18:class Judge1(_Closed):
23:class Judge2(_Closed):
28:class Judge3(_Closed):
33:class Judge4(_Closed):
38:class FlagOutput(_Closed):
46:class FlagPass(_Closed):
== totals.py ==
"""Running total of ACCEPTED charges, computed on read and never stored (R-CH-3, D-004, D-019, ADR-011). Integer cents only.
Only class `charge` with review_status accepted/edited adds. Pending charges are 'detected, not a total'. No PT total is ever derived from a rate."""

COUNTED = ("accepted", "edited")
LETTER_PREFIX = "Billed charges stated in these records: "
UI_PREFIX = "Accepted charges: "
DETECTED_LABEL = "Detected, not yet accepted (not a total)"


def usd(cents: int) -> str:
    return f"${cents // 100:,}.{cents % 100:02d}"


def totals(amounts: list) -> dict:
    accepted = pending = 0
    unclear, found = [], 0
    for a in amounts:
        cls, cents, st = a.get("cls"), a.get("cents"), a.get("review_status", "pending")
        if cls != "damages":
            found += 1
        if cls == "charge" and cents is not None:
            if st in COUNTED:
                accepted += cents
            elif st == "pending":
                pending += cents
        elif st != "dismissed" and cls != "damages":
            unclear.append(a)
    status = "none_found" if not found else ("partial_unclear" if unclear else "complete")
    return {"accepted_cents": accepted, "detected_pending_cents": pending, "detected_label": DETECTED_LABEL,
            "unclear_items": unclear, "amounts_found": found, "status": status,
            "letter_line": LETTER_PREFIX + usd(accepted) if accepted else None,
            "ui_line": UI_PREFIX + usd(accepted) if accepted else "No accepted charges yet."}
== gap tests ==
__init__.py
_fakes.py
_golden.py
test_amounts.py
test_audited.py
test_boundaries.py
test_confidence.py
test_conflicts.py
test_dates.py
test_db.py
test_eval_matching.py
test_export.py
test_flag_templates.py
test_flags_injection.py
test_flags_sample.py
test_gaps.py
test_grounding.py
test_ingest.py
test_injection.py
test_judges.py
test_pipeline.py
test_provider.py
test_provider_backends.py
test_review_rules.py
test_schemas.py
test_sentences.py
test_totals.py
tests/unit/test_gaps.py
tests/unit/test_pipeline.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:21.145Z

The `compose_state` key fix holds and unknown keys now raise. `check_amount` has a boundary hole: a bare `240` or `850` is accepted when the record says `$6,240` or `$1,850`, because `,` counts as a boundary in the digit guard. Next I'll check whether amounts or gap flags reach any production state path.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:22.468Z

**tool call — Bash**
````
{
 "command": "echo \"== amounts.py ==\" && cat app/backend/amounts.py; echo \"== test_gaps state asserts ==\" && grep -n \"state\\|reasons\\|ENDPOINT\" tests/unit/test_gaps.py | head -20; echo \"== gap flag state key anywhere? ==\" && grep -rn \"\\\"state\\\"\" app/backend/gaps.py app/backend/flags.py app/backend/flag_templates.py app/backend/export.py app/backend/review.py 2>/dev/null; echo \"== edited amounts in totals path / check_amount callers ==\"; grep -rn \"COUNTED\\|edited\" app/backend/*.py | head; echo \"== R-CH-1 spec text ==\"; grep -rn \"R-CH-1\\b\" memory/ docs/ 2>/dev/null | head -5",
 "description": "Check amount extraction, gap state assertions and spec R-CH-1"
}
````

### User / tool · 2026-11-02T01:51:22.586Z

**tool result**
````
== amounts.py ==
"""Dollar amounts: find, classify, dedupe (all code; ADR-011, R-CH-1/2/4/6, D-004/D-005, LLM_VS_CODE rows 6 and 7).
Money is whole cents (int). Noisy OCR figures keep their verbatim text with cents None and class unclear, never corrected.
There is no LLM classifier. A rate can never become a charge: classes are decided here and the paralegal can only accept or dismiss."""
import re

from app.backend import injection, lexicon

# '$' + a figure. Letters that OCR confuses with digits (O o l I S B) are tolerated so noise is LISTED (unclear), not silently skipped.
_AMT = re.compile(r"\$\s?([0-9OolISB](?:[0-9OolISB,]*[0-9OolISB])?(?:\.[0-9OolISB]{1,2})?)")
_VALID = re.compile(r"(?:\d{1,3}(?:,\d{3})+|\d+)(?:\.(\d{1,2}))?$")
_BOUNDARY = re.compile(r"(?<=[.;!?])\s+|\n")
_RATE_WORD = re.compile(r"\b(?:per|each|rate)\b", re.IGNORECASE)
_RATE_AFTER = re.compile(r"^\s*(?:per\s+\w+|/\s*\w+|each\b|an?\s+(?:visit|session|hour|day|unit|treatment|procedure|adjustment|appointment)\b)", re.IGNORECASE)
_ESTIMATE = re.compile(r"\bestimat(?:e|ed|es)\b", re.IGNORECASE)
_STATEMENT = re.compile(r"\b(?:statement|balance|amount\s+due|total|billed)\b", re.IGNORECASE)
_CHARGE_END = re.compile(r"(?:\b[\w-]+\s+)?\b(?:charges?|billed)\s*:?\s*$", re.IGNORECASE)
_WORK_TAIL = re.compile(r"\s+(?:of|from|off)\s+work\b", re.IGNORECASE)


def to_cents(figure: str):
    """'6,240' -> 624000, '95.5' -> 9550; None when the figure is not a clean number. Integer arithmetic only."""
    m = _VALID.match(figure)
    if not m:
        return None
    whole = figure.split(".")[0].replace(",", "")
    return int(whole) * 100 + int((m.group(1) or "").ljust(2, "0") or 0)


def find_amounts(excerpt: str) -> list:
    """[{raw, cents, start, end}] for every '$' figure, in text order. Doses, speeds, scores and day counts have no '$' and are never found."""
    out = []
    spans = [(h["start"], h["end"]) for h in injection.scan(excerpt or "")]
    for m in _AMT.finditer(excerpt or ""):
        figure = m.group(1)
        if not any(c.isdigit() for c in figure):
            continue
        injected = any(s <= m.start() and m.end() <= e for s, e in spans)   # a figure inside instruction-like text has no trusted value (D-005)
        out.append({"raw": m.group(0), "cents": None if injected else to_cents(figure), "start": m.start(), "end": m.end()})
    return out


def _label(excerpt: str, start: int) -> str:
    before = _BOUNDARY.split(excerpt[:start])[-1]
    return " ".join(before.split()[-6:])


def classify(excerpt: str, amount: dict, injection: bool = False, source: str = None) -> str:
    """charge | rate | estimate | damages | unclear. First match wins (ADR-011): injection, unreadable, rate, estimate, damages,
    billing statement, charge label, else unclear. `source` (the record's header label) is optional; when given, the statement rule
    needs it to be a billing document."""
    if injection or amount.get("cents") is None:
        return "unclear"
    label = _label(excerpt, amount["start"])
    after = excerpt[amount["end"]:amount["end"] + 30]
    if _RATE_WORD.search(label) or _RATE_AFTER.match(after):
        return "rate"
    if _ESTIMATE.search(label):
        return "estimate"
    if any(e["regex"].search(label) for e in lexicon.code_list("damages")):
        return "damages"
    if _STATEMENT.search(label) and (source is None or _is_billing_source(source)):
        return "charge"
    if _CHARGE_END.search(label):
        return "charge"
    return "unclear"


def _is_billing_source(source: str) -> bool:
    return any(e["id"] == "billing_document" and e["regex"].search(source or "") for e in lexicon.code_list("non_encounter"))


def damages_mentions(excerpt: str) -> list:
    """Work-loss and similar mentions with no dollar value (lexicon `damages`): [{raw, cents: None, cls: 'damages', start, end}]."""
    out = []
    for e in lexicon.code_list("damages"):
        for m in e["regex"].finditer(excerpt or ""):
            end = m.end()
            t = _WORK_TAIL.match(excerpt, end)
            if t:
                end = t.end()
            if not any(o["start"] < end and m.start() < o["end"] for o in out):
                out.append({"raw": excerpt[m.start():end], "cents": None, "cls": "damages", "start": m.start(), "end": end})
    return sorted(out, key=lambda o: o["start"])


def _norm(s):
    return " ".join((s or "").split()).casefold()


def dedupe_amounts(amounts: list) -> list:
    """Same date + normalised provider + record text (when given) + class + value merges into one amount citing every record (R-CH-6). Unreadable values never merge."""
    out, index = [], {}
    for a in amounts:
        nos = sorted(a.get("record_nos") or [a["record_no"]])
        key = (a.get("date"), _norm(a.get("provider")), _norm(a.get("text")), a.get("cls"), a.get("cents")) if a.get("cents") is not None else None
        if key in index:
            m = out[index[key]]
            m["record_nos"] = sorted(set(m["record_nos"]) | set(nos))
            m["duplicate_note"] = "Same amount, date and provider appears in records " + ", ".join(str(n) for n in m["record_nos"]) + "."
            continue
        row = {**a, "record_nos": nos, "duplicate_note": None}
        if key is not None:
            index[key] = len(out)
        out.append(row)
    return out


def extract_amounts(records: list) -> list:
    """All amounts of a case from ingested records (needs n, excerpt; uses date_iso, source, injection_tag, text, char_start when present).
    Injection-tagged records yield class unclear for every amount (D-005). Duplicate records contribute once (the dedupe is per record)."""
    rows = []
    for r in records:
        if r.get("duplicate_of"):
            continue
        base = (r.get("char_start") or 0) + (r["text"].find(r["excerpt"]) if r.get("text") and r["excerpt"] in r["text"] else 0)
        found = [{**a, "cls": classify(r["excerpt"], a, injection=bool(r.get("injection_tag")), source=r.get("source"))}
                 for a in find_amounts(r["excerpt"])] + damages_mentions(r["excerpt"])
        for a in sorted(found, key=lambda x: x["start"]):
            rows.append({"record_no": r["n"], "text": r["excerpt"], "date": r.get("date_iso"), "provider": r.get("source"), "raw": a["raw"], "cents": a["cents"],
                         "cls": a["cls"], "start": base + a["start"], "end": base + a["end"], "injection": bool(r.get("injection_tag"))})
    out = dedupe_amounts(rows)
    for i, a in enumerate(out, 1):
        a["id"] = f"a{i}"
    return out


_PLAN = re.compile(r"plan\s+of\s+care\s*:\s*(\d+)\s+visits?", re.IGNORECASE)
_VISIT = re.compile(r"\bvisit\s+(\d+)\b", re.IGNORECASE)


def _prefix(source):
    return _norm((source or "").split(",")[0])


def rate_note(records: list, record_no: int) -> dict:
    """Numbers for the rate note, code-derived (T-033 AC7): planned N from 'Plan of care: N visits' in a record with the same provider
    prefix (header label before the first comma); last_visit M = highest 'visit M' in such a header label. None when not found."""
    me = next(r for r in records if r["n"] == record_no)
    same = [r for r in records if _prefix(r.get("source")) == _prefix(me.get("source"))]
    planned = next((int(m.group(1)) for r in same for m in [_PLAN.search(r.get("excerpt") or "")] if m), None)
    visits = [int(m.group(1)) for r in same for m in [_VISIT.search(r.get("source") or "")] if m]
    return {"planned": planned, "last_visit": max(visits) if visits else None}
== test_gaps state asserts ==
33:    """R-FL-1 (D-003): case_09 billing statement + phone note do not split the 56-day gap."""
== gap flag state key anywhere? ==
== edited amounts in totals path / check_amount callers ==
app/backend/export.py:11:review_status in (accepted, edited) is "in"; dismissed/rejected is "out"; anything else is pending.
app/backend/export.py:31:IN = ("accepted", "edited")
app/backend/export.py:389:def _edited(v):
app/backend/export.py:392:        if e.get("review_status") != "edited":
app/backend/export.py:401:        out.append(f"- {_cap(v.cite(e['record_no']))}: " + "; ".join(bits or ["edited"]) + ".")
app/backend/export.py:435:        "EDITED ITEMS", *_edited(v), "",
app/backend/generator.py:57:                   "judge": None, "code_checks": {}, "human": {"action": None, "edited_text": None, "at": None}}
app/backend/totals.py:2:Only class `charge` with review_status accepted/edited adds. Pending charges are 'detected, not a total'. No PT total is ever derived from a rate."""
app/backend/totals.py:4:COUNTED = ("accepted", "edited")
app/backend/totals.py:22:            if st in COUNTED:
== R-CH-1 spec text ==
docs/M2M3_COVERAGE.md:49:| R-CH-1 | T-033 (m2-be-amounts-gaps), T-038 (m2-qa-eval-runner) |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:35.905Z

**tool call — Bash**
````
{
 "command": "echo \"== who owns gaps.py / check_amount wiring on the board ==\"; grep -ln \"gaps.py\\|check_amount\" board/cards/*.md; echo \"== any amount-edit path that sets cents? ==\"; grep -rln \"cents\" app/db app/backend 2>/dev/null; grep -rn \"edited_json\\|amount\" app/db/*.py 2>/dev/null | head -8; echo \"== api.md R-CH-1 / gap state wording ==\"; grep -n \"ENDPOINT_NOT_VERIFIED\\|GROUNDING_AMOUNT_NOT_IN_TEXT\" memory/contracts/api.md | head; echo \"== pytest config ==\"; ls pytest.ini setup.cfg pyproject.toml conftest.py tests/conftest.py 2>/dev/null; echo \"== scratch mutation copy ==\"; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t030r2mut; rm -rf \"$S\"; mkdir -p \"$S\" && rsync -a --exclude .venv --exclude artifacts --exclude board --exclude .git --exclude __pycache__ ./app ./tests ./memory ./evals \"$S\"/ 2>&1 | tail -3; ls \"$S\"",
 "description": "Check ownership, edit paths, and set up scratch mutation copy"
}
````

### User / tool · 2026-11-02T01:51:36.083Z

**tool result**
````
== who owns gaps.py / check_amount wiring on the board ==
board/cards/T-030.md
board/cards/T-029.md
board/cards/T-033.md
board/cards/T-035.md
== any amount-edit path that sets cents? ==
app/db/schema.sql
app/backend/totals.py
app/backend/export.py
app/backend/export_routes.py
app/backend/amounts.py
app/db/db.py:4:- get_item() returns columns with `_json` decoded under the stripped name (ladder_json -> "ladder", edited_json -> "edited").
app/db/db.py:18:_ITEM_TABLES = {"entry": ("entries", "e"), "amount": ("amounts", "a"), "flag": ("flags", "f")}
app/db/db.py:19:_PREFIX_KIND = {"e": "entry", "a": "amount", "f": "flag"}
app/db/db.py:20:_CASE_TABLES = ("records", "entries", "amounts", "flags", "llm_calls", "review_events", "cases")
app/db/db.py:91:    """Insert an entry/amount/flag. payload keys must be column names (dicts/lists JSON-encoded). New items are pending."""
app/db/db.py:96:    if {"review_status", "edited_json", "edited"} & set(p):
app/db/db.py:137:    locked = {"review_status", "edited_json", "edited", "id", "case_id", "updated_at"}
app/db/db.py:151:    item's own columns; an edit goes to edited_json, so the original is never lost (R-RV-2)."""
== api.md R-CH-1 / gap state wording ==
436:| `GROUNDING_AMOUNT_NOT_IN_TEXT` | rejected | model reported an amount the record does not contain |
448:| `ENDPOINT_NOT_VERIFIED` | needs_review | a gap's span could contain an unconfirmed date |
== pytest config ==
tests/conftest.py
== scratch mutation copy ==
app
evals
memory
tests
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:41.757Z

The scratch copy is ready. I'll apply each fix's mutation there, not in the product tree, and confirm the tests go red.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:45.742Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t030r2mut\nPY=/Users/arsis/zlayt-pm-project/.venv/bin/python\ncd \"$S\" && echo \"== baseline (scratch copy, unmutated) ==\" && $PY -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q 2>&1 | tail -n 1\n# M1: check_amount stubbed to accept everything\ncp app/backend/grounding.py /tmp/_unused 2>/dev/null; cp \"$S/app/backend/grounding.py\" \"$S/grounding.orig\"\n$PY - \"$S\" <<'EOF'\nimport sys, pathlib\np = pathlib.Path(sys.argv[1]) / \"app/backend/grounding.py\"\ns = p.read_text()\nold = '    return [\"GROUNDING_AMOUNT_NOT_IN_TEXT\"]\\n'\nassert s.count(old) == 1\np.write_text(s.replace(old, '    return []  # MUTANT: amount gate removed\\n'))\nEOF\necho \"== M1 check_amount -> [] ==\" && $PY -m pytest tests/unit/test_grounding.py -q 2>&1 | grep -E \"^FAILED|passed|failed\" | tail -n 8\ncp \"$S/grounding.orig\" \"$S/app/backend/grounding.py\"\n# M2: drop the endpoint_unverified row from compose_state\ncp \"$S/app/backend/confidence.py\" \"$S/confidence.orig\"\n$PY - \"$S\" <<'EOF'\nimport sys, pathlib\np = pathlib.Path(sys.argv[1]) / \"app/backend/confidence.py\"\ns = p.read_text()\nold = '(\"endpoint_unverified\", \"ENDPOINT_NOT_VERIFIED\"), '\nassert s.count(old) == 1\np.write_text(s.replace(old, ''))\nEOF\necho \"== M2 endpoint_unverified row removed ==\" && $PY -m pytest tests/unit/test_confidence.py -q 2>&1 | grep -E \"^FAILED|passed|failed\" | tail -n 5\ncp \"$S/confidence.orig\" \"$S/app/backend/confidence.py\"\necho \"== restored ==\" && $PY -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q 2>&1 | tail -n 1",
 "description": "Run baseline and two mutations in the scratch copy only"
}
````

### User / tool · 2026-11-02T01:51:47.759Z

**tool result**
````
== baseline (scratch copy, unmutated) ==
209 passed in 0.31s
== M1 check_amount -> [] ==
FAILED tests/unit/test_grounding.py::test_amount_absent_from_record_is_rejected[$6,420]
FAILED tests/unit/test_grounding.py::test_amount_absent_from_record_is_rejected[$9,000]
FAILED tests/unit/test_grounding.py::test_amount_absent_from_record_is_rejected[$62,400]
FAILED tests/unit/test_grounding.py::test_noisy_amount_not_autocorrected - As...
4 failed, 41 passed in 0.19s
== M2 endpoint_unverified row removed ==
        (L(), X(llm_failed=True), "LLM_FAILED_AFTER_RETRIES"),
FAILED tests/unit/test_confidence.py::test_needs_review_cases[ladder21-ctx21-ENDPOINT_NOT_VERIFIED]
1 failed, 64 passed in 0.05s
== restored ==
209 passed in 0.30s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:50.297Z

Both mutations turn the right tests red and the restored tree is green again. Last checks: rerun the prior evidence script to confirm the two FAIL lines are gone, and see what the API spec says a gap flag must carry.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:51:52.388Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-030-exercise.py 2>&1 | grep -c \"^FAIL\" ; .venv/bin/python artifacts/review-evidence/T-030-exercise.py 2>&1 | grep -E \"^FAIL|check_amount exists|endpoint_unverified|compose_state handles\" ; echo \"== api.md flag state / gap flag shape ==\"; grep -n \"flag\" memory/contracts/api.md | grep -i \"state\\|gap\\|needs_review\" | head -12; echo \"== test_gaps ENDPOINT coverage ==\"; grep -c \"ENDPOINT_NOT_VERIFIED\" tests/unit/test_gaps.py; echo \"== gap flags carry no state: ==\"; .venv/bin/python -I -c \"\nimport sys; sys.path.insert(0,'/Users/arsis/zlayt-pm-project')\nfrom app.backend import gaps\nrecs=[{'n':1,'kind':'encounter','date_iso':'2026-01-01','source':'A'},{'n':2,'kind':'encounter','date_iso':'2026-03-15','source':'B','date_status':'parsed'},{'n':3,'kind':'encounter','date_iso':None,'date_candidates':['2026-02-10'],'source':'C'}]\nfor f in gaps.gap_flags(recs): print(sorted(f.keys())); print('state' in f, f['reasons'])\n\"",
 "description": "Rerun evidence script and inspect gap flag shape"
}
````

### User / tool · 2026-11-02T01:51:52.879Z

**tool result**
````
1
PASS check_amount exists (checklist #4 amount in text)
PASS compose_state handles endpoint_unverified :: ('needs_review', ['ENDPOINT_NOT_VERIFIED'])
FAILS: 0
== api.md flag state / gap flag shape ==
8:- Item ids: entries `e…`, amounts `a…`, flags `f…`, records `r…`. Gap flags use `f_gap_<recA>_<recB>`. Opaque to the frontend.
49:Request text is normalised first (CRLF and CR become LF; leading/trailing whitespace trimmed). **In demo mode the text is accepted only if its sha256 is in the recorded set (the sample and the golden cases); otherwise `409 demo_mode_unsupported_input` is returned before anything is stored** (D-020). Response 201 (all code: records, dates, duplicates, amounts, gap flags exist before any model call):
59:  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
178:        "generator": {"model": "claude-sonnet-5-5", "prompt_version": "flags_v1", "call_id": "c40", "output": {"type": "causation", "category": "patient_report", "record_id": "r9", "excerpt": "Patient states symptoms began after the January collision."}},
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative`, `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
204:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
208:  "gap_flags": [],
212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
230:For multi-record items (a gap flag, a conflict, a merged duplicate) `source` has one element per record so the UI can open all of them. `404 not_found` for an unknown id.
414:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blocks (R-EX-5); flagged language that is quoted inside an accepted excerpt is listed in the internal notes (D-012); on the `fixture` backend the sample output equals the golden file byte for byte.
451:| `LEXICON_ONLY` / `LLM_ONLY` | needs_review | phrase list and model disagree on a flag |
== test_gaps ENDPOINT coverage ==
0
== gap flags carry no state: ==
['category', 'days', 'evidence', 'explanation', 'from_date', 'id', 'origin', 'reasons', 'record_nos', 'title', 'to_date', 'type']
False ['ENDPOINT_NOT_VERIFIED']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:52:14.554Z

**tool call — Bash**
````
{
 "command": "echo \"== flags table ==\"; grep -n \"CREATE TABLE.*flags\" -A 12 app/db/schema.sql; echo \"== who inserts flags ==\"; grep -rn \"insert_item\\|\\\"flag\\\"\" app/backend/*.py app/db/*.py | grep -v \"^app/db/db.py:1[0-9]:\" | head -8; echo \"== api.md gap flag / ladder on flags ==\"; sed -n 170,176p memory/contracts/api.md | cut -c1-400; echo \"== commit 1365926 stat ==\"; git show --stat --format='%h %s' 1365926 | head -12",
 "description": "Check flags persistence, insert path, and round-2 commit scope"
}
````

### User / tool · 2026-11-02T01:52:14.682Z

**tool result**
````
== flags table ==
32:CREATE TABLE IF NOT EXISTS flags (
33-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id),
34-  type TEXT CHECK (type IN ('gap','conflict','pre_existing','causation','record_warning')),
35-  category TEXT, source_kind TEXT CHECK (source_kind IN ('record','patient_report')),
36-  title TEXT, explanation TEXT, computed_json TEXT, evidence_json TEXT,
37-  origin TEXT CHECK (origin IN ('code','lexicon','llm','lexicon+llm')), reviewer_note TEXT,
38-  state TEXT, state_reasons_json TEXT,
39-  review_status TEXT NOT NULL DEFAULT 'pending' CHECK (review_status IN ('pending','accepted','edited','dismissed')),
40-  edited_json TEXT, ladder_json TEXT, updated_at REAL
41-);
42--- Audit: one row per attempt (ADR-003.7); holds full prompts, so delete_case must cover it (ADR-006).
43-CREATE TABLE IF NOT EXISTS llm_calls (
44-  id TEXT PRIMARY KEY, case_id TEXT NOT NULL REFERENCES cases(id), item_id TEXT,
== who inserts flags ==
app/backend/export.py:194:    return _cap((t or "flag").replace("_", " "))
app/backend/gaps.py:25:                    "days": n, "flag": is_gap(n)})
app/backend/gaps.py:50:        if not g["flag"]:
== api.md gap flag / ladder on flags ==
      "title": "Patient self-report",
      "explanation": "Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): “Patient states symptoms began after the January collision.”",
      "computed": {},
      "evidence": [ {"record_id": "r9", "excerpt": "Patient states symptoms began after the January collision.", "start": 1818, "end": 1876} ],
      "origin": "lexicon+llm", "reviewer_note": null,
      "state": "verified", "reasons": [], "why": "Quote found word for word; the phrase list and the model agree, and the second check agreed.",
      "review_status": "pending", "edited": null,
== commit 1365926 stat ==
1365926 fix(backend): check_amount, endpoint_unverified, strict keys (T-030 r2)

 app/backend/confidence.py | 10 +++++++++-
 app/backend/grounding.py  | 25 ++++++++++++++++++++++++-
 2 files changed, 33 insertions(+), 2 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:52:25.574Z

**tool call — Bash**
````
{
 "command": "for f in app/backend/sentences.py app/backend/grounding.py app/backend/confidence.py app/backend/why.py; do echo \"== $f\"; grep -n \"^import\\|^from\\|    import\\|    from\" \"$f\"; done; echo \"== bare except / except Exception in four modules\"; grep -n \"except\" app/backend/sentences.py app/backend/grounding.py app/backend/confidence.py app/backend/why.py; echo \"(end)\"; echo \"== gaps.py lines 33-38 for citation\"; sed -n 33,38p app/backend/gaps.py; date -u +%Y-%m-%dT%H:%M:%SZ",
 "description": "Confirm no LLM imports and no bare excepts in the four modules"
}
````

### User / tool · 2026-11-02T01:52:25.685Z

**tool result**
````
== app/backend/sentences.py
7:import re
82:    from app.backend.grounding import locate_all
== app/backend/grounding.py
6:import functools
7:import pathlib
8:import re
10:import yaml
89:    from app.backend import sentences as S
== app/backend/confidence.py
== app/backend/why.py
== bare except / except Exception in four modules
(end)
== gaps.py lines 33-38 for citation
        if r.get("kind", "encounter") != "encounter" or r.get("date_iso"):
            continue
        cands = r.get("date_candidates") or []
        if not cands or any(gap["from_date"] <= c <= gap["to_date"] for c in cands):
            reasons.append("ENDPOINT_NOT_VERIFIED")
            break
2026-11-02T01:52:25Z
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:52:44.593Z

Evidence is complete. I'm writing the round-2 review now. The verdict is `fail` on one new blocker, because the fix for the endpoint major sits in the table but the only producer of that reason never calls it.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:03.132Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r2.md",
 "content": "# T-030 round 2 review: staff-engineer-reviewer (Marcus Lee)\n\nVerdict: **fail**. Scope: round-2 commit 1365926 (`check_amount`, `endpoint_unverified`, strict keys).\n\nBrief check: `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.29s` (0 failures). Both round-1 majors are resolved at the function and table level: `check_amount` exists and is tested, and `compose_state` maps `endpoint_unverified` to `ENDPOINT_NOT_VERIFIED`. The brief's pass condition is therefore met on its literal wording. The verdict is `fail` because the endpoint major's own risk is not closed in production: the only producer of `ENDPOINT_NOT_VERIFIED` (gaps.py:37) never calls `compose_state`, and the gap flag it builds carries no state at all. That is a blocker under D.2 (spec constraint, api.md:448).\n\nKey evidence:\n- `reasons` on a gap flag with an unconfirmed endpoint: `['ENDPOINT_NOT_VERIFIED']`, and `'state' in flag` is `False` (repro below).\n- The entry path (`generator.py:33-34`, `_ctx`) never sets `endpoint_unverified`, and gap flags do not pass through `generator.compose`.\n- `check_amount` has no production caller. A bare `240` is accepted against `$6,240` (minor, below).\n\n## Exercised\n- `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.29s` (rerun: `209 passed in 0.31s`, unmutated scratch copy).\n- `grep -rn \"check_amount\\|compose_state\\|endpoint_unverified\" --include=*.py . | grep -v tests/` -> call sites listed in findings; `check_amount` only defined at `app/backend/grounding.py:110`, never called outside tests.\n- `git show --stat 1365926` -> `app/backend/confidence.py | 10`, `app/backend/grounding.py | 25`.\n- Read in full: `app/backend/grounding.py`, `app/backend/confidence.py`, `app/backend/gaps.py`, `app/backend/generator.py:55-110`, `app/backend/amounts.py`, `app/backend/totals.py`, `app/backend/schemas.py`, `app/db/schema.sql` (flags table), `tests/unit/test_grounding.py:150-168`, `tests/unit/test_confidence.py`.\n- `.venv/bin/python -I` probe of `check_amount`: `('Charge: $6,240.', '$6,240') -> []`, `('Charge: $6,240.', '240') -> []`, `('Charge: $1,850.', '850') -> []`, `('Charge: $1,850.', '$185') -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']`, `('Charge: $1,2OO.', '$1,200') -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']`, `('Charge: $1,2OO.', '$1,2OO') -> []`.\n- `.venv/bin/python -I` probe of `compose_state({...ok...}, {'endpoint_unverified': True})` -> `('needs_review', ['ENDPOINT_NOT_VERIFIED'])`; with `{'injecton': True}` -> `ValueError: unknown ladder/context keys: ['injecton']`.\n- Gap flag repro: three synthetic records (2026-01-01 encounter, 2026-03-15 encounter, undated with candidate 2026-02-10) passed to `gaps.gap_flags` -> keys `['category','days','evidence','explanation','from_date','id','origin','reasons','record_nos','title','to_date','type']`; `'state' in f` -> `False`; `reasons` -> `['ENDPOINT_NOT_VERIFIED']`.\n- `artifacts/review-evidence/T-030-exercise.py` -> `FAILS: 0` (round 1: 2 FAIL lines, the two majors). Its `check_amount exists` and `compose_state handles endpoint_unverified` lines now PASS.\n- Mutation in a scratch copy (product tree not touched): M1 `check_amount` body -> `return []` -> `4 failed, 41 passed` (3x `test_amount_absent_from_record_is_rejected`, `test_noisy_amount_not_autocorrected`). M2 remove the `endpoint_unverified` row from `confidence.py` -> `1 failed, 64 passed` (`test_needs_review_cases[ladder21-ctx21-ENDPOINT_NOT_VERIFIED]`). Restored copy -> `209 passed`.\n- `grep -n \"^import\\|^from\\|    import\\|    from\"` on `sentences.py`, `grounding.py`, `confidence.py`, `why.py` -> stdlib (`re`, `functools`, `pathlib`) and `yaml` only, plus local `app.backend` imports. No LLM client. `grep -n except` on the four -> no hits.\n- Not run: the pipeline CLI (`app/backend/pipeline.py` is a stub that raises `NotImplementedError`); `pytest tests/unit -q` as a whole (outside the brief's four files).\n\n```json\n{\"card\": \"T-030\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"round-2 commit 1365926 (app/backend/confidence.py, app/backend/grounding.py); working tree at a2fc95a; read-through of app/backend/{gaps,generator,amounts,totals,schemas}.py and app/db/schema.sql for production callers; tests/unit/test_{sentences,grounding,confidence,boundaries}.py; artifacts/review-evidence/T-030-exercise.py; no app URL (backend only), no sample CLI run (pipeline.py is a stub)\",\n \"exercised\": [\n  \"pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q -> 209 passed in 0.29s\",\n  \"grep -rn check_amount|compose_state|endpoint_unverified --include=*.py . (non-test call sites)\",\n  \"git show --stat 1365926\",\n  \"read grounding.py, confidence.py, gaps.py, generator.py:55-110, amounts.py, totals.py, schemas.py, schema.sql flags table, test_grounding.py:150-168, test_confidence.py\",\n  \".venv/bin/python -I probes: check_amount boundary cases; compose_state endpoint_unverified and unknown-key cases\",\n  \"gaps.gap_flags on 3 synthetic records -> flag keys, 'state' absent, reasons ['ENDPOINT_NOT_VERIFIED']\",\n  \"artifacts/review-evidence/T-030-exercise.py -> FAILS: 0\",\n  \"scratch-copy mutation M1 (check_amount -> []): 4 failed; M2 (endpoint row removed): 1 failed; restored: 209 passed\",\n  \"import and except grep on sentences.py, grounding.py, confidence.py, why.py\"],\n \"verdict\": \"fail\",\n \"scores\": {\"excerpt_verification\": 4, \"summary_checks\": 4, \"splitter\": 4, \"compose_state_fail_closed\": 4, \"gap_flag_state\": 1, \"amount_grounding\": 3, \"test_coverage\": 4, \"no_llm_boundary\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\", \"title\": \"Gap flags are emitted with no state; ENDPOINT_NOT_VERIFIED never reaches compose_state\",\n   \"evidence\": \"app/backend/gaps.py:37 `reasons.append(\\\"ENDPOINT_NOT_VERIFIED\\\")`; app/backend/gaps.py:58 `\\\"evidence\\\": ev, \\\"reasons\\\": _reasons(g, records)})` (flag dict has no 'state' key). Repro: `.venv/bin/python -I -c \\\"...gaps.gap_flags(recs)...\\\"` -> keys [... 'reasons', ...] with no 'state'; `'state' in f` -> False; `reasons` -> ['ENDPOINT_NOT_VERIFIED']. Only compose_state caller on the entry path: app/backend/generator.py:104-106, whose `_ctx` (generator.py:33-34) never sets endpoint_unverified. memory/contracts/api.md:448 `| ENDPOINT_NOT_VERIFIED | needs_review | a gap's span could contain an unconfirmed date |`. api.md flag example: `\\\"state\\\": \\\"verified\\\", \\\"reasons\\\": []`. app/db/schema.sql:38 `state TEXT, state_reasons_json TEXT,` on flags.\",\n   \"why_it_matters\": \"Round 1's major was that a gap flag whose span could hide an unconfirmed date would not come out needs_review. The round-2 fix made compose_state correct, but the only code that produces ENDPOINT_NOT_VERIFIED for gap flags does not call compose_state and attaches no state. So the spec's needs_review for that case is not produced, and anything that gates on flag state (review queue, ready_to_export per api.md) cannot see an unconfirmed-endpoint gap. A false 73-day flag can therefore reach export review without a state. This is a spec violation (api.md:448 and the flag shape), not a style point. Scope note: gaps.py is T-029/T-033 code, but it is the path the round-1 major named, so the major is not closed until this is fixed.\",\n   \"fix\": \"In gaps.gap_flags, set state and state_reasons on every flag. Simplest: call confidence.compose_state({'grounding_failures': [], 'schema_valid': True, 'code_reasons': [], 'judge': None}, {'endpoint_unverified': 'ENDPOINT_NOT_VERIFIED' in reasons, 'injection': 'INJECTION_SUSPECTED' in reasons}) and write the returned state and reasons onto the flag (needs_review iff reasons, else verified).\",\n   \"acceptance_test\": \"New test in tests/unit/test_gaps.py: a gap whose endpoint record has date_candidates spanning the gap -> flag['state'] == 'needs_review' and 'ENDPOINT_NOT_VERIFIED' in flag['reasons']; a clean >30-day gap -> flag['state'] == 'verified' and reasons == []. Mutation check: removing the endpoint row from confidence.py (M2 above) turns it red.\"},\n  {\"severity\": \"minor\", \"title\": \"check_amount accepts a bare figure that sits inside a comma-grouped figure\",\n   \"evidence\": \"app/backend/grounding.py:112 docstring: \\\"A longer figure does not vouch for a shorter one ('$185' vs '$1,850').\\\" Lines 116-118: `before = record_text[m.start() - 1] ...` / `if not before.isdigit() and not re.match(r\\\"\\\\d|[,.]\\\\d\\\", tail)`. Repro: check_amount('Charge: $6,240.', '240') -> []; check_amount('Charge: $1,850.', '850') -> [].\",\n   \"why_it_matters\": \"The function's own contract is false for comma-grouped figures: the ',' before the match is not a digit, so the digit-run guard passes and a wrong figure is vouched for. It is not reachable from today's production path: amounts.find_amounts (app/backend/amounts.py) only returns '$'-prefixed text from the record, and app/backend/schemas.py states the generator returns no amount field. It becomes live the moment a caller passes a figure that was not extracted (e.g. an edited amount).\",\n   \"fix\": \"Also reject a match where the character before is ',' or '.' and the character before that is a digit (i.e. the match is the tail of a grouped number). Keep the existing tail check.\",\n   \"acceptance_test\": \"assert GR.check_amount('Charge: $6,240.', '240') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] and GR.check_amount('Charge: $1,850.', '850') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] added to tests/unit/test_grounding.py; existing $6,240 and $1,2OO cases stay green.\"},\n  {\"severity\": \"minor\", \"title\": \"check_amount has no production caller\",\n   \"evidence\": \"grep -rn check_amount --include=*.py . (excluding tests) -> only app/backend/grounding.py:110 (definition). amounts.find_amounts (app/backend/amounts.py) and totals.py (COUNTED includes 'edited', totals.py:4) do not call it.\",\n   \"why_it_matters\": \"Checklist #4 needs each amount in the text. Amounts are extracted by code from the record text, so today they pass by construction and the gate is defense-in-depth. But any path that writes a non-extracted amount into totals (e.g. an edited amount counted via COUNTED) has no gate, which is the risk round 1 named.\",\n   \"fix\": \"Call check_amount on every amount that did not come from amounts.find_amounts, at the point it is written (edit or consolidation path), and reject with GROUNDING_AMOUNT_NOT_IN_TEXT. Owner: T-033 or the edit path card.\",\n   \"acceptance_test\": \"A unit test that writes an edited amount whose raw text is not in the record and asserts it is rejected, not counted in totals().\"}\n ],\n \"whats_right\": [\n  \"compose_state now raises on unknown ladder and context keys (app/backend/confidence.py:49-51; probe {'injecton': True} -> ValueError), and ENDPOINT_NOT_VERIFIED is a table row (confidence.py:64); removing that row turns test_needs_review_cases[ENDPOINT_NOT_VERIFIED] red.\",\n  \"check_amount never repairs: '$1,2OO' is found as written and the corrected '$1,200' is rejected (test_grounding.py:165-168); stubbing check_amount to [] turns 4 tests red.\",\n  \"The lexicon loader now raises on hedge or self_report entries with no pattern (app/backend/grounding.py:67-69), closing the round-1 silent-skip minor.\"\n ],\n \"questions_for_chris\": [\"Which card owns the gap-flag state composition (gaps.py), T-029 or T-033? I have filed it against T-030 because it is the path the round-1 major named; re-home it if you prefer.\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:53:03.280Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:04.908Z

The review is written. I'll run the read-only board validator against it, since the verdict rule is enforced there.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:05.479Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -n 8; echo \"exit=$?\"; grep -n \"T-030-staff-engineer-r2\\|r2\" tools/board.py 2>/dev/null | head -3",
 "description": "Run read-only board validator on the repo"
}
````

### User / tool · 2026-11-02T01:53:05.634Z

**tool result**
````
ok (49 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:09.675Z

Validator passes. Before I finish, I'll save the recurring pattern to my memory directory: a round fix that is only verified at the function level and never reached from the producer.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:12.928Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_wiring_review_patterns.md",
 "content": "---\nname: wiring-review-patterns\ndescription: T-030 r2 pattern: a round fix passes its unit tests at the function/table level but the producer path never calls it. Check callers and run the producer, not just pytest.\nmetadata:\n  type: project\n---\n\nRecurring pattern (T-030 r2, 2026-11-01): the round-1 major \"compose_state ignores endpoint_unverified\" was fixed in the\nboolean table (confidence.py:64) and tested there, and `check_amount` was added with tests. But the only producer of\nENDPOINT_NOT_VERIFIED (app/backend/gaps.py:37) never calls compose_state, and gap flags carry reasons with no `state` key.\n`check_amount` had no production caller at all. Pytest was green on both, so the green summary hid the gap.\n\n**Why:** a fix that is green only in its own unit test does not close the risk the original finding named (the gap flag\npath). Same family as T-031 partial re-fixes (sibling writers), see [[project_db_review_patterns]].\n\n**How to apply:**\n- For every function or table row a round adds or changes, grep non-test callers (`grep -rn name --include=*.py . | grep -v tests/`).\n  Zero production hits = not wired, regardless of pytest.\n- Run the producer on a repro (e.g. gaps.gap_flags on synthetic records) and check the output shape, not only the unit tests.\n- Scratch-copy mutation of the function (return []) and of the table row shows whether the tests are load-bearing; it does not\n  show whether production reaches them.\n\nAlso: the dossier names claude-sonnet-5-5 as the expected model id, but the r2 run was executing as claude-haiku-5-5. Record\nthe model that actually ran in the JSON, and note the mismatch in the reply.\n"
}
````

### User / tool · 2026-11-02T01:53:13.102Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_wiring_review_patterns.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:13.978Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method\n",
 "new_string": "- [DB review patterns](project_db_review_patterns.md) — T-031 r1-r2: partial re-fixes (sibling writers), regex guard blind spots, scratch-copy mutation method\n- [Wiring review patterns](project_wiring_review_patterns.md) — T-030 r2: fix green in unit tests but no production caller; grep callers and run the producer\n"
}
````

### User / tool · 2026-11-02T01:53:14.074Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (note: the file had been modified on disk since you last read it — the edit applied cleanly, but the file contains other changes not in your context. Read it before edits that depend on surrounding content.)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:15.887Z

T-030 r2: pytest `209 passed in 0.29s`, both majors resolved at function/table level, verdict **fail** on a new blocker (gap flags from gaps.py:37/58 emit ENDPOINT_NOT_VERIFIED with no state and never reach compose_state); review at /Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r2.md (model claude-haiku-5-5, not the dossier's expected sonnet id).

### User / tool · 2026-11-02T01:53:26.638Z

The coordinator sent a message while you were working:
Orchestrator triage: your T-030 r2 blocker (gap flags from gaps.py never reach compose_state) is pipeline wiring owned by T-037 finalize; I've added it to T-037's AC. Please re-judge T-030 strictly on its own modules (sentences, grounding, confidence, why) and AC, and write reviews/T-030-staff-engineer-r3.md (D.2 JSON). Reply 1 line.

Address this before completing your current task.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:37.374Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-030 2>&1 | head -80; echo \"=== T-037 ===\"; python3 tools/board.py show T-037 2>&1 | grep -n -i \"endpoint\\|gap\\|ENDPOINT\\|state\" | head -20",
 "description": "Read T-030 card AC and check T-037 carries the gap-flag item"
}
````

### User / tool · 2026-11-02T01:53:37.553Z

**tool result**
````
---
id: "T-030"
title: "Grounding verifier first: sentences.py, grounding.py, confidence.py, why.py"
milestone: "M2"
role: "backend"
status: "changes_requested"
priority: "P0"
depends_on: ["T-029"]
created_by: "orchestrator"
created_at: "2026-11-02T01:14:09Z"
updated_at: "2026-11-02T01:53:32Z"
claimed_by: "backend"
claimed_at: "2026-11-02T01:50:18Z"
rounds: 2
commits: ["217e243", "1365926"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5", "verdict": "changes", "file": "reviews/T-030-staff-engineer.md", "at": "2026-11-02T01:50:00Z"}
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-030-staff-engineer-r2.md", "at": "2026-11-02T01:53:24Z"}
ac:
  - {"n": 1, "text": "`pytest tests/unit/test_sentences.py tests/unit/test_grounding.py` green: excerpt is a verbatim, whole-sentence, contiguous run; non-verbatim -> rejected, mid-unit -> needs_review (R-TL-2); hedge omitted -> EXCERPT_OMITS_QUALIFIER, hedge set read from lexicon.yaml `hedge: true` (R-TL-8)", "done": true, "evidence": "pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries"}
  - {"n": 2, "text": "new_tokens() and qualifier check: 'pain 4/10' over 'Pain 3/10.' and a summary dropping 'without loss of consciousness' -> needs_review; 'Visit 8' label passes (R-TL-10, row 15); proved by test_grounding::test_summary_tokens", "done": true, "evidence": "pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries"}
  - {"n": 3, "text": "offsets: for every golden excerpt raw_text[start:end] equals the quote; a mutated record makes lookup fail -> needs_review (R-RV-9, R-FL-5); proved by test_grounding::test_offsets_golden and test_offset_lookup_failure", "done": true, "evidence": "pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries"}
  - {"n": 4, "text": "`pytest tests/unit/test_confidence.py` green: full compose_state table, needs_review sorts first, every reason code has a why template (R-TL-5, rows 17, 18)", "done": true, "evidence": "pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries"}
  - {"n": 5, "text": "`pytest tests/unit/test_boundaries.py` green for these modules and a failing quote is never repaired (test_grounding::test_no_silent_fix, row 4 rung 1)", "done": true, "evidence": "pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries"}
---
## Description
Implements the grounding verifier before any LLM stage exists, per CONTRACT M2 'write it first'. Covers R-TL-2, R-TL-8, R-TL-10, R-FL-5, R-RV-9 offsets and the confidence/why modules (LLM_VS_CODE rows 4 rung 1, 15, 17, 18). All code, no LLM import.

Plan key: m2-be-grounding (artifacts/tmp/m2m3_cards.json; coverage in docs/M2M3_COVERAGE.md).

Estimate: 45 min.

## Notes (append-only, newest last)
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-030.md
- 2026-11-02T01:44:07Z backend: claimed
- 2026-11-02T01:44:07Z backend: started against committed T-029 tests
- 2026-11-02T01:44:12Z orchestrator: assigned: backend-1
- 2026-11-02T01:46:37Z backend: tests/unit/test_sentences.py::test_hedge_sentence_splits_at_semicolon is wrong: record 8 excerpt in evals/golden/sample.txt ends with 'Charge: $2,150.' (a 4th unit per R-TL-2), test lists 3. Splitter correct; qa should append 'Charge: $2,150.'. Also: test_abbreviations expects 'mg. Follow' to split (REQ lists mg. as abbreviation, ADR-016 says one unit); implemented mg./etc. as sentence-final before uppercase. All else green (200/201).
- 2026-11-02T01:46:44Z backend: AC 1 checked: pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries
- 2026-11-02T01:46:44Z backend: AC 2 checked: pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries
- 2026-11-02T01:46:44Z backend: AC 3 checked: pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries
- 2026-11-02T01:46:44Z backend: AC 4 checked: pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries
- 2026-11-02T01:46:44Z backend: AC 5 checked: pytest tests/unit/test_sentences.py test_grounding.py test_confidence.py test_boundaries.py: 200 pass, 1 test_sentences hedge-split test wrong (record 8 has 4th unit; noted); nearest tests: test_grounding (excerpt/summary/offsets), test_confidence, test_boundaries
- 2026-11-02T01:46:44Z backend: moved in_progress -> in_review
- 2026-11-02T01:47:27Z orchestrator: review dispatched: staff (sonnet)
- 2026-11-02T01:50:00Z orchestrator: review staff-engineer-reviewer (claude-sonnet-5-5): changes — reviews/T-030-staff-engineer.md; round 1; findings:
    - [major] Amount-in-text grounding check (check_amount) not implemented — fix: Add check_amount(record_text, raw_amount) -> [] or ['GROUNDING_AMOUNT_NOT_IN_TEXT'] using the same whitespace normalization as locate; no digit repair.
    - [major] compose_state ignores endpoint_unverified and fails open to verified — fix: Add ('endpoint_unverified', 'ENDPOINT_NOT_VERIFIED') to the boolean table at confidence.py:55.
    - [minor] compose_state silently ignores unknown or misspelled ladder and context keys — fix: Raise ValueError on keys outside the documented ladder/context sets (or require all keys). Keep judge=None as the documented 'no judge needed' case.
    - [minor] Lexicon loader silently skips malformed entries, including hedge: true entries — fix: Raise on an entry with hedge: true or self_report: true and no valid pattern; keep skipping only comment/metadata rows explicitly.
    - [minor] Summary-side hedge/negation/self-report detection uses hardcoded word lists, not the lexicon — fix: Use hedge_ids(summary) only (or document _HEDGE_WORDS as the intentional looser summary-side set in the module docstring and test its boundary).
    - [minor] AC-named tests do not exist; the no-silent-repair claim has no direct test — fix: Add a test that check_excerpt on a near-miss returns only reason codes (list of str) and leaves the input unchanged, and align AC text with the real test names.
- 2026-11-02T01:50:00Z orchestrator: assigned: backend-1
- 2026-11-02T01:50:18Z backend: claimed
- 2026-11-02T01:50:18Z backend: moved in_progress -> in_review
- 2026-11-02T01:50:25Z orchestrator: review dispatched: haiku r2
- 2026-11-02T01:53:24Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-030-staff-engineer-r2.md; round 2; findings:
    - [blocker] Gap flags are emitted with no state; ENDPOINT_NOT_VERIFIED never reaches compose_state — fix: In gaps.gap_flags, set state and state_reasons on every flag. Simplest: call confidence.compose_state({'grounding_failures': [], 'schema_valid': True, 'code_reasons': [], 'judge': None}, {'endpoint_unverified': 'ENDPOINT_NOT_VERIFIED' in reasons, 'injection': 'INJECTION_SUSPECTED' in reaso
    - [minor] check_amount accepts a bare figure that sits inside a comma-grouped figure — fix: Also reject a match where the character before is ',' or '.' and the character before that is a digit (i.e. the match is the tail of a grouped number). Keep the existing tail check.
    - [minor] check_amount has no production caller — fix: Call check_amount on every amount that did not come from amounts.find_amounts, at the point it is written (edit or consolidation path), and reject with GROUNDING_AMOUNT_NOT_IN_TEXT. Owner: T-033 or the edit path card.
- 2026-11-02T01:53:25Z orchestrator: Triage: r2 'blocker' (gap flags never reach compose_state) is pipeline wiring in T-037 finalize, not T-030's modules; moved to T-037 AC. Asked reviewer to re-scope.
- 2026-11-02T01:53:32Z orchestrator: assigned: orchestrator (awaiting re-scoped r3 verdict)

## Handoff
Round 2: added grounding.check_amount (5 tests green), compose_state honours endpoint_unverified (1 test green) and raises on unknown ladder/context keys, lexicon loader raises on pattern-less hedge/self_report entries, summary-side hedge words documented as intentionally looser. 250 pass across grounding/confidence/sentences/boundaries/judges/schemas. Not done: AC-named no-silent-repair test (tests are qa-owned; check_excerpt returns only code lists, never mutates).

=== T-037 ===
18:  - {"n": 1, "text": "`python -m app.pipeline evals/golden/sample.txt` (fixture backend) prints 9 entries, the 73-day gap flag, charges $8,390 total, all flag groups, exit 0 in under 60 s (CONTRACT M2 CLI)", "done": false, "evidence": null}
21:  - {"n": 4, "text": "gap flags and ingest results exist when every LLM call raises (stub backend); dropping an entry leaves gaps unchanged (D-003, row 9); proved by test_pipeline::test_code_stages_without_llm", "done": false, "evidence": null}
25:  - {"n": 8, "text": "From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state", "done": false, "evidence": null}
28:Ties stages 0 to 7 together and records fixtures so evals run with no key (A-001/A-002, R-CO-2, R-CO-6, R-RV-6). Delivers the CONTRACT M2 CLI and finalize/state composition (rows 17, 20).
42:- 2026-11-02T01:53:24Z orchestrator: AC 8 added: From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:51.815Z

T-037 AC 8 is in place, which I verified from the card. Now I'll check the T-030 AC evidence directly: whether the AC-named tests exist, whether `sort_key` is tested, and whether the T-033 card carries the amount-caller item.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:53:53.998Z

**tool call — Bash**
````
{
 "command": "for n in test_summary_tokens test_offsets_golden test_offset_lookup_failure test_no_silent_fix test_hedge_sentence_splits_at_semicolon test_abbreviations; do printf \"%-36s \" $n; grep -rln \"def $n\" tests/unit/ | tr '\\n' ' '; echo; done; echo \"== sort_key tests ==\"; grep -rn \"sort_key\" tests/unit/ | head -3; echo \"== needs_review sort test? ==\"; grep -rn \"needs_review.*verified\\|sort\" tests/unit/test_confidence.py | head -3; echo \"== boundary/why tests exist ==\"; grep -c \"def test_\" tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py; echo \"== T-033 mentions check_amount ==\"; grep -n \"check_amount\" board/cards/T-033.md | cut -c1-200; echo \"== hedge-split test (sentences) ==\"; grep -n \"semicolon\\|Charge: \\$2,150\\|mg\\.\" tests/unit/test_sentences.py | head -6; echo \"== evidence strings ==\"; .venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q 2>&1 | tail -n1",
 "description": "Verify AC-named tests, sort_key coverage and T-033 caller item"
}
````

### User / tool · 2026-11-02T01:53:54.700Z

**tool result**
````
test_summary_tokens                  
test_offsets_golden                  
test_offset_lookup_failure           
test_no_silent_fix                   
test_hedge_sentence_splits_at_semicolon tests/unit/test_sentences.py 
test_abbreviations                   tests/unit/test_sentences.py 
== sort_key tests ==
== needs_review sort test? ==
tests/unit/test_confidence.py:8:Returns (state, reasons). Precedence rejected > needs_review > verified.
tests/unit/test_confidence.py:91:    assert sorted(rs) == sorted(["JUDGE_PARTIAL", "SUMMARY_DROPS_QUALIFIER", "INJECTION_SUSPECTED", "DATE_AMBIGUOUS"])
tests/unit/test_confidence.py:124:@pytest.mark.parametrize("code", sorted(api_codes()))
== boundary/why tests exist ==
tests/unit/test_sentences.py:9
tests/unit/test_boundaries.py:4
tests/unit/test_grounding.py:26
tests/unit/test_confidence.py:16
== T-033 mentions check_amount ==
== hedge-split test (sentences) ==
31:    ("Rx cyclobenzaprine 10 mg. Follow up in 1 week.", "Rx cyclobenzaprine 10 mg."),   # 'mg.' before a capitalised sentence IS a terminator (backend splitter; REQ R-TL-2 abbreviation list to be corrected)
37:    """R-TL-2 / D-021: abbreviations (approx., Dr., mg., e.g., vs.) and decimals are not terminators."""
40:def test_semicolon_and_line_break_terminate():
46:def test_hedge_sentence_splits_at_semicolon():
== evidence strings ==
209 passed in 0.30s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:10.736Z

Most T-030 AC evidence checks out. Four AC-named tests are absent and `sort_key` has no test. I'll confirm the remaining names and the `sort_key` callers before I write the file.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:11.904Z

**tool call — Bash**
````
{
 "command": "echo \"== sort_key anywhere ==\"; grep -rn \"sort_key\" --include=*.py . | grep -v \"^./.venv\"; echo \"== offset / repair / summary-named tests present in the four files ==\"; grep -n \"def test_.*\\(offset\\|repair\\|silent\\|summary_token\\|changed_pain\\|mutated\\)\" tests/unit/test_grounding.py tests/unit/test_sentences.py tests/unit/test_confidence.py tests/unit/test_boundaries.py; echo \"== grounding.py line refs ==\"; grep -n \"before = \\|isdigit\\|def check_amount\" app/backend/grounding.py",
 "description": "Confirm sort_key callers and AC-named test presence"
}
````

### User / tool · 2026-11-02T01:54:12.013Z

**tool result**
````
== sort_key anywhere ==
evals/run.py:346:    return json.dumps([ents, ams, fl, (out.get("totals") or {}).get("detected_not_a_total")], sort_keys=True, default=str)
evals/run.py:554:    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
evals/run.py:596:        latest.write_text(json.dumps(data, indent=1, sort_keys=True) + "\n")
tools/board.py:253:        atomic_write(SHADOW, json.dumps(shadow, indent=0, sort_keys=True))
app/llm/audited.py:93:    return json.dumps(o, sort_keys=True)
app/llm/provider.py:28:    blob = json.dumps([model, system, user, json_schema], sort_keys=True, ensure_ascii=False, separators=(",", ":"))
app/llm/backends/claude_cli.py:32:            f"that satisfies this JSON Schema:\n{json.dumps(json_schema, sort_keys=True)}")
app/llm/backends/fixture.py:38:    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
app/backend/confidence.py:23:def sort_key(state: str) -> int:
app/db/db.py:43:    return json.dumps(v, ensure_ascii=False, sort_keys=True) if isinstance(v, (dict, list)) else v
== offset / repair / summary-named tests present in the four files ==
tests/unit/test_grounding.py:61:def test_offset_round_trip_for_every_unit_run(case):
tests/unit/test_grounding.py:79:def test_locate_mutated_record_returns_none():
tests/unit/test_grounding.py:91:def test_changed_pain_score_flags():
== grounding.py line refs ==
110:def check_amount(record_text: str, raw_amount: str) -> list:
116:            before = record_text[m.start() - 1] if m.start() else ""
118:            if not before.isdigit() and not re.match(r"\d|[,.]\d", tail):
135:        out.append(str(int(t)) if t.isdigit() else t)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:16.179Z

The re-scoped T-030 verdict is `pass`. The endpoint blocker is out of T-030's modules, and the remaining findings are minor or nit. Writing r3 now.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:30.357Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r3.md",
 "content": "# T-030 round 3 review: staff-engineer-reviewer (Marcus Lee), re-scoped by orchestrator triage\n\nVerdict: **pass** on T-030's own modules (`sentences.py`, `grounding.py`, `confidence.py`, `why.py`) and AC. No blocker, no major. Three minors and one nit.\n\nScope decision recorded, not a resolution. The orchestrator moved the r2 blocker (gap flags from `gaps.py:37/58` never reach `compose_state`) to T-037 AC 8. I checked that the AC is on the card: `python3 tools/board.py show T-037` lists `{\"n\": 8, \"text\": \"From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state\", \"done\": false}`. I have not dropped the finding. Its severity stays **blocker** for T-037 and it is not counted in this T-030 verdict. T-030's round-1 major is closed at the `compose_state` table level only; the product-level closure is open under T-037 AC 8.\n\nBrief run: `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.30s`.\n\n## Exercised this round\n- `pytest` on the four files: `209 passed in 0.30s`.\n- `python3 tools/board.py show T-030` and `show T-037` (read-only); T-037 AC 8 quoted above.\n- `grep -n \"def test_\\(summary_tokens\\|offsets_golden\\|offset_lookup_failure\\|no_silent_fix\\)\"` over the four files -> no output. Names present instead: `test_offset_round_trip_for_every_unit_run` (test_grounding.py:61), `test_locate_mutated_record_returns_none` (:79), `test_changed_pain_score_flags` (:91).\n- `grep -rn sort_key --include=*.py .` -> `app/backend/confidence.py:23` is the only definition; no caller and no test.\n- Re-read `app/backend/grounding.py:110-120` (`check_amount`) and `tests/unit/test_confidence.py` for the reason-code table.\n- Carried from r2 without rerunning: the gap-flag repro (`gaps.gap_flags` yields `reasons` with no `state`), the `check_amount` probes, and the scratch mutations (M1 4 red, M2 1 red).\n\n## AC status (T-030 card)\n- AC1 (sentences + grounding green, verbatim, whole-sentence, mid-unit, hedge via lexicon): met. Suite green; hedge set comes from `hedge_ids` over lexicon entries (`grounding.py:78-79`).\n- AC2 (summary tokens, qualifier, \"Visit 8\"): met on behaviour. The AC names `test_grounding::test_summary_tokens`, which does not exist; behaviour is covered by `test_changed_pain_score_flags`. See minor 2.\n- AC3 (offsets golden, lookup failure): met on behaviour via `test_offset_round_trip_for_every_unit_run` and `test_locate_mutated_record_returns_none`. The AC-named tests `test_offsets_golden` and `test_offset_lookup_failure` do not exist. See minor 2.\n- AC4 (compose_state table, needs_review sorts first, why template per code): table met; every REASON_CODE is reachable through a ladder/context row and tested (`test_needs_review_cases`, 22 rows, plus rejected and why-template tests). \"Sorts first\" is implemented by `sort_key` (`confidence.py:23`) but has no caller and no test. See minor 3.\n- AC5 (no silent repair, `test_no_silent_fix`): behaviour correct (`check_excerpt` returns codes only and never mutates its input; the r1 exercise and the round-2 read confirm this). The AC-named test does not exist; the handoff says so (\"Not done: AC-named no-silent-repair test\"). See minor 2.\n\n```json\n{\"card\": \"T-030\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"T-030's own modules at round 3: app/backend/{sentences,grounding,confidence,why}.py at HEAD a2fc95a (round-2 fix commit 1365926); tests/unit/test_{sentences,grounding,confidence,boundaries}.py; T-030 card AC1-AC5; T-037 AC 8 as the re-homed endpoint item (not scored here); no app URL, no pipeline CLI (pipeline.py is a stub)\",\n \"exercised\": [\n  \"pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q -> 209 passed in 0.30s\",\n  \"python3 tools/board.py show T-030 (AC1-AC5 read)\",\n  \"python3 tools/board.py show T-037 (AC 8 confirmed)\",\n  \"grep -n def test_(summary_tokens|offsets_golden|offset_lookup_failure|no_silent_fix) over the four test files -> no matches\",\n  \"grep -rn sort_key --include=*.py . -> only app/backend/confidence.py:23\",\n  \"read app/backend/grounding.py:110-120 and tests/unit/test_confidence.py (reason-code table)\"],\n \"verdict\": \"pass\",\n \"scores\": {\"excerpt_verification\": 4, \"summary_checks\": 4, \"splitter\": 4, \"compose_state_fail_closed\": 4, \"test_coverage\": 3, \"amount_grounding\": 3, \"no_llm_boundary\": 5},\n \"findings\": [\n  {\"severity\": \"minor\", \"title\": \"check_amount accepts a bare figure inside a comma-grouped figure\",\n   \"evidence\": \"app/backend/grounding.py:112 docstring: \\\"A longer figure does not vouch for a shorter one ('$185' vs '$1,850').\\\" Lines 116-118: `before = record_text[m.start() - 1] ...` and `if not before.isdigit() and not re.match(r\\\"\\\\d|[,.]\\\\d\\\", tail)`. Repro: check_amount('Charge: $6,240.', '240') -> []; check_amount('Charge: $1,850.', '850') -> [] (r2 probe).\",\n   \"why_it_matters\": \"The function's own stated contract is false for comma-grouped figures, so the gate would vouch for a wrong figure if a caller ever passes a non-extracted amount. Not reachable from today's extraction path (amounts.find_amounts returns '$'-prefixed record text), so minor.\",\n   \"fix\": \"In check_amount, also reject a match whose preceding character is ',' or '.' when the character before that is a digit.\",\n   \"acceptance_test\": \"tests/unit/test_grounding.py: assert check_amount('Charge: $6,240.', '240') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] and check_amount('Charge: $1,850.', '850') == ['GROUNDING_AMOUNT_NOT_IN_TEXT']; existing $6,240 and $1,2OO cases stay green.\"},\n  {\"severity\": \"minor\", \"title\": \"T-030 card AC names four tests that do not exist, while marking the ACs done\",\n   \"evidence\": \"grep -n 'def test_\\\\(summary_tokens\\\\|offsets_golden\\\\|offset_lookup_failure\\\\|no_silent_fix\\\\)' tests/unit/test_grounding.py tests/unit/test_sentences.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -> no output. T-030 card AC2/AC3/AC5 each name one of these and carry \\\"done\\\": true. Handoff: \\\"Not done: AC-named no-silent-repair test\\\".\",\n   \"why_it_matters\": \"AC5's invariant (a failing quote is never repaired) is correct in behaviour but its named proof does not exist, so a future change that returned corrected text with the code would not be caught by the test the card cites.\",\n   \"fix\": \"Add a test that check_excerpt on a near-miss returns a list of str codes equal to the input's reason set and leaves the input unchanged, and either name it test_no_silent_fix or update the AC text to the real test names.\",\n   \"acceptance_test\": \"pytest tests/unit/test_grounding.py -k 'silent or repair' passes; a mutant check_excerpt that also returns corrected text fails it.\"},\n  {\"severity\": \"minor\", \"title\": \"AC4 'needs_review sorts first' has no caller and no test\",\n   \"evidence\": \"app/backend/confidence.py:23-25 `def sort_key(state: str) -> int: return STATE_ORDER[state]`. grep -rn sort_key --include=*.py . -> no caller and no test. T-030 AC4 names this behaviour.\",\n   \"why_it_matters\": \"The ordering the queue relies on is defined but neither used nor asserted, so a regression to the order would pass the suite.\",\n   \"fix\": \"Add a test asserting sorted(['verified','needs_review','rejected'], key=sort_key) == ['needs_review','verified','rejected'], and leave the caller to the review-queue card.\",\n   \"acceptance_test\": \"pytest tests/unit/test_confidence.py -k sort green.\"},\n  {\"severity\": \"nit\", \"title\": \"Card evidence strings are stale\",\n   \"evidence\": \"T-030 AC1-AC5 evidence reads \\\"200 pass, 1 test_sentences hedge-split test wrong\\\". Current run: 209 passed, 0 failed; test_sentences.py:46 test_hedge_sentence_splits_at_semicolon passes.\",\n   \"why_it_matters\": \"A reader trusts a count and a failure note that no longer hold.\",\n   \"fix\": \"Update the AC evidence to the 209-pass line quoted above.\",\n   \"acceptance_test\": \"pytest on the four files prints '209 passed' or the current count, with no failures.\"}\n ],\n \"whats_right\": [\n  \"compose_state covers every REASON_CODE reachable through a ladder or context row, rejects unknown keys (confidence.py:49-51), and is tested row by row (test_needs_review_cases, 22 rows).\",\n  \"check_excerpt returns only reason codes and never rewrites the quote; '$1,2OO' is found as written and the corrected '$1,200' is rejected (test_grounding.py:165-168).\",\n  \"The lexicon loader raises on a hedge or self_report entry with no pattern (grounding.py:67-69), so the hedge set cannot silently shrink.\"],\n \"questions_for_chris\": [\"The check_amount caller gap (no production call site; amounts are code-extracted, the edit path is ungated) is outside T-030's modules and is not on the T-033 card. Should it go on T-033's AC?\"]}\n```\n"
}
````

### User / tool · 2026-11-02T01:54:30.583Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r3.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:31.821Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -n 3; echo \"exit=$?\"",
 "description": "Run read-only board validator after writing r3"
}
````

### User / tool · 2026-11-02T01:54:31.954Z

**tool result**
````
ok (49 file(s))
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:54:33.521Z

T-030 r3: **pass** on its own modules (209 passed in 0.30s, no blockers or majors; 3 minors, 1 nit), with the endpoint blocker held at T-037 AC 8 and not counted here; review at /Users/arsis/zlayt-pm-project/reviews/T-030-staff-engineer-r3.md.
