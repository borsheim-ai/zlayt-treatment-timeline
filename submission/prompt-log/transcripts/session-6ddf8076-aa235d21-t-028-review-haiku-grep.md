# Subagent: T-028 review (haiku grep) (T-028 review (haiku grep))

Source: `agent-aa235d214ad4527f5.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:03:52.604Z

Working directory: /Users/arsis/zlayt-pm-project. Mechanical review of T-028 (`python3 tools/board.py show T-028`), a consistency pass on memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md. For each AC run greps and quote the output: SUMMARY_DROPS_QUALIFIER present in api.md, DECISIONS.md, LLM_VS_CODE.md; every category name in app/llm/lexicon.yaml (`grep -E "^  [a-z_]+:" -n` or python yaml load) appears in ADR-013 with a template; confirm_date example in api.md does not add a gap for the phone note; `date_invalid` is the only non-candidate code; "mg." treated as abbreviation consistently; README-arch cut line keeps the per-record flag pass; api.md export example references evals/golden/sample.export.expected.txt; DECISIONS.md AI line matches spec/REQUIREMENTS.md R-EX-4(1). Pass only if every AC is supported by output. Write reviews/T-028-staff-engineer.md (D.2 JSON, model = what you run as). Reply ≤ 4 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:03:53.753Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T01:03:53.760Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:03:54.117Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-028; echo \"EXIT=$?\"",
 "description": "Show T-028 card from board"
}
````

### User / tool · 2026-11-02T01:03:54.241Z

**tool result**
````
---
id: "T-028"
title: "ADR consistency pass: D-022, lexicon v2 categories, confirm_date example, mg., per-record pass (split from T-014)"
milestone: "M1"
role: "architect"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:02:15Z"
updated_at: "2026-11-02T01:03:53Z"
claimed_by: "architect"
claimed_at: "2026-11-02T01:02:37Z"
rounds: 0
commits: ["de749c2"]
reviews: []
ac:
  - {"n": 1, "text": "SUMMARY_DROPS_QUALIFIER (D-022) in api.md reason codes, ADR and LLM_VS_CODE", "done": true, "evidence": "grep -c SUMMARY_DROPS_QUALIFIER: api.md 1, DECISIONS.md 3, LLM_VS_CODE.md 1"}
  - {"n": 2, "text": "ADR-013 category list equals lexicon v2 categories (incl. prior_surgery), each with a flag template", "done": true, "evidence": "ADR-013 category list = lexicon v2 names (prior_surgery, alternative_cause, litigation_referral, objective_negative, recovery_context, accident_date_provenance); templates + lexicon-only stated; api.md list matches"}
  - {"n": 3, "text": "confirm_date example excludes the phone note from gap math (D-003, golden case_01); one error code; mg. treated as abbreviation everywhere (D-021); cut line keeps the per-record flag pass", "done": true, "evidence": "api.md confirm_date example gap_flags [] (phone note, D-003); date_invalid for non-candidate; mg. one unit [477,532); README-arch cut line drops per-record pass; check script 14/14 blocks, 17/17 offsets"}
  - {"n": 4, "text": "api.md export example references the golden file instead of copying it; D-001..D-024 citations current", "done": true, "evidence": "api.md export example abbreviates blocks and references golden file; D-001..D-024 in all three docs; AI line aligned to R-EX-4(1)"}
---
## Description
Debt from T-014 r3 (reviews/T-014-staff-engineer-r3.md M1-M5 + minors). Mechanical consistency only, no new design.

## Notes (append-only, newest last)
- 2026-11-02T01:02:18Z orchestrator: assigned: architect
- 2026-11-02T01:02:37Z architect: claimed
- 2026-11-02T01:03:40Z architect: AC 1 checked: grep -c SUMMARY_DROPS_QUALIFIER: api.md 1, DECISIONS.md 3, LLM_VS_CODE.md 1
- 2026-11-02T01:03:40Z architect: AC 2 checked: ADR-013 category list = lexicon v2 names (prior_surgery, alternative_cause, litigation_referral, objective_negative, recovery_context, accident_date_provenance); templates + lexicon-only stated; api.md list matches
- 2026-11-02T01:03:40Z architect: AC 3 checked: api.md confirm_date example gap_flags [] (phone note, D-003); date_invalid for non-candidate; mg. one unit [477,532); README-arch cut line drops per-record pass; check script 14/14 blocks, 17/17 offsets
- 2026-11-02T01:03:40Z architect: AC 4 checked: api.md export example abbreviates blocks and references golden file; D-001..D-024 in all three docs; AI line aligned to R-EX-4(1)
- 2026-11-02T01:03:40Z architect: moved in_progress -> in_review
- 2026-11-02T01:03:53Z orchestrator: review dispatched: staff-engineer (haiku)

## Handoff
M1 SUMMARY_DROPS_QUALIFIER + per-quote source_kind (ADR-012/005/017, api, LLM_VS_CODE); M2 ADR-013 union of lexicon categories; M3 confirm_date example gap_flags [] + encounter=false rule in ADR-010; M4 mg. is an abbreviation (D-021), sentences regenerated; M5 per-record pass off cut line; m1-m4, n1 done; AI line per R-EX-4(1). Left: qa golden export file still has the old AI line and needs the R-EX-4(1) text; golden variant E.

EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:03:54.632Z

**tool call — Bash**
````
{
 "command": "ls -la /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/ 2>/dev/null; echo \"---\"; cat /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md 2>/dev/null",
 "description": "List reviewer memory directory and index"
}
````

### User / tool · 2026-11-02T01:03:54.720Z

**tool result**
````
total 24
drwxr-xr-x@  5 arsis  staff   160 Nov  1 18:58 .
drwxr-xr-x@ 12 arsis  staff   384 Nov  1 19:03 ..
-rw-r--r--@  1 arsis  staff   287 Nov  1 18:48 MEMORY.md
-rw-r--r--@  1 arsis  staff  3100 Nov  1 19:01 project_design_review_patterns.md
-rw-r--r--@  1 arsis  staff  2646 Nov  1 18:58 project_harness_review_patterns.md
---
- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
- [Design review patterns](project_design_review_patterns.md) — T-014 r1+r2 defects: doc/REQ drift, amount-rule coverage, judge-failure path
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:03:58.053Z

**tool call — Bash**
````
{
 "command": "echo \"== AC1 grep -c ==\" && for f in memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md; do echo -n \"$f: \"; grep -c SUMMARY_DROPS_QUALIFIER \"$f\"; done; echo \"== AC1 grep -n ==\" && grep -n SUMMARY_DROPS_QUALIFIER memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md; echo \"== files exist ==\"; ls -la memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md app/README-arch.md app/llm/lexicon.yaml spec/REQUIREMENTS.md evals/golden/ 2>&1",
 "description": "Check SUMMARY_DROPS_QUALIFIER occurrences and file presence"
}
````

### User / tool · 2026-11-02T01:03:58.159Z

**tool result**
````
== AC1 grep -c ==
memory/contracts/api.md: 1
memory/DECISIONS.md: 3
docs/LLM_VS_CODE.md: 1
== AC1 grep -n ==
memory/contracts/api.md:439:| `SUMMARY_DROPS_QUALIFIER` | needs_review | the excerpt has a hedge, self-report marker, negation, laterality or "approx." that the summary leaves out (D-022) |
docs/LLM_VS_CODE.md:43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (or the record's source line / parsed date), and qualifiers in the excerpt must not be dropped from the summary (`SUMMARY_DROPS_QUALIFIER`). | The most likely invented fact is a changed number. A small judge model can miss it; code cannot. | Unit tests: "Pain 9/10" over "Pain 4/10" is flagged; an edit adding "$9,000" shows a warning before acceptance and needs "keep my wording". |
memory/DECISIONS.md:147:    - **needs_review**: any doubt, with reasons listed. Includes: judge verdict other than the positive one (partial, unsupported, disagrees, unsure) or judge unavailable (`JUDGE_UNAVAILABLE`, including a fixture miss on a re-check, `FIXTURE_MISS`); a summary token not in the excerpt or a qualifier of the excerpt missing from the summary (ADR-012, `SUMMARY_TOKEN_NOT_IN_EXCERPT`, `SUMMARY_DROPS_QUALIFIER`); a hedge sentence the excerpt omits or an excerpt that is not whole sentences; date ambiguous or missing; amount kind other than `charge`; lexicon and model disagree on a flag; the item's source record carries an injection tag, or it came from the cross-record pass in a case with any tagged record; a gap flag whose span could contain an unconfirmed date (`ENDPOINT_NOT_VERIFIED`); highlight offset not found; a failed run step.
memory/DECISIONS.md:244:- **Dropped qualifiers (D-022, round 4).** A second function `grounding.dropped_qualifiers(summary, excerpt)` finds qualifiers in the excerpt (lexicon hedge set, `self_report` entries, negation words such as "without", laterality, "approx.") and requires each to appear in the summary; a missing one gives `needs_review` with `SUMMARY_DROPS_QUALIFIER`. The judge checks additions, not omissions, so this is code. Self-report is tagged per quote: each entry carries `source_kind` (`patient_report` | `record`) for its excerpt sentences, set by code from the lexicon. In evals, `required_terms` are checked against the summary alone. R-TL-10 gains this check (ADR-017).
memory/DECISIONS.md:309:  12. **qa items.** Golden variant E (above); `required_terms` checked against the summary alone and R-TL-10 gains SUMMARY_DROPS_QUALIFIER (D-022).
== files exist ==
-rw-r--r--@ 1 arsis  staff   8454 Nov  1 19:03 app/README-arch.md
-rw-r--r--@ 1 arsis  staff  81847 Nov  1 18:51 app/llm/lexicon.yaml
-rw-r--r--@ 1 arsis  staff  21521 Nov  1 19:03 docs/LLM_VS_CODE.md
-rw-r--r--@ 1 arsis  staff  60577 Nov  1 19:03 memory/DECISIONS.md
-rw-r--r--@ 1 arsis  staff  34107 Nov  1 19:03 memory/contracts/api.md
-rw-r--r--@ 1 arsis  staff  57962 Nov  1 19:03 spec/REQUIREMENTS.md

evals/golden/:
total 560
drwxr-xr-x@ 27 arsis  staff    864 Nov  1 18:56 .
drwxr-xr-x@  4 arsis  staff    128 Nov  1 18:03 ..
-rw-r--r--@  1 arsis  staff  18038 Nov  1 18:56 README.md
-rw-r--r--@  1 arsis  staff  10494 Nov  1 18:56 case_01_date_formats.expected.json
-rw-r--r--@  1 arsis  staff   1210 Nov  1 18:56 case_01_date_formats.txt
-rw-r--r--@  1 arsis  staff  10639 Nov  1 18:56 case_02_gap_boundaries.expected.json
-rw-r--r--@  1 arsis  staff   1151 Nov  1 18:56 case_02_gap_boundaries.txt
-rw-r--r--@  1 arsis  staff  10324 Nov  1 18:56 case_03_rate_and_ocr.expected.json
-rw-r--r--@  1 arsis  staff    790 Nov  1 18:56 case_03_rate_and_ocr.txt
-rw-r--r--@  1 arsis  staff   7421 Nov  1 18:56 case_04_duplicates_no_amounts.expected.json
-rw-r--r--@  1 arsis  staff   1012 Nov  1 18:56 case_04_duplicates_no_amounts.txt
-rw-r--r--@  1 arsis  staff  10094 Nov  1 18:56 case_05_provider_conflict.expected.json
-rw-r--r--@  1 arsis  staff    860 Nov  1 18:56 case_05_provider_conflict.txt
-rw-r--r--@  1 arsis  staff  12960 Nov  1 18:56 case_06_subtle_pre_existing.expected.json
-rw-r--r--@  1 arsis  staff    902 Nov  1 18:56 case_06_subtle_pre_existing.txt
-rw-r--r--@  1 arsis  staff   9612 Nov  1 18:56 case_07_prompt_injection.expected.json
-rw-r--r--@  1 arsis  staff    735 Nov  1 18:56 case_07_prompt_injection.txt
-rw-r--r--@  1 arsis  staff  10372 Nov  1 18:56 case_08_diagnosis_temptation.expected.json
-rw-r--r--@  1 arsis  staff    715 Nov  1 18:56 case_08_diagnosis_temptation.txt
-rw-r--r--@  1 arsis  staff   8658 Nov  1 18:56 case_09_nonvisit_hides_gap.expected.json
-rw-r--r--@  1 arsis  staff    730 Nov  1 18:56 case_09_nonvisit_hides_gap.txt
-rw-r--r--@  1 arsis  staff  34272 Nov  1 18:56 check_golden.py
-rw-r--r--@  1 arsis  staff  19193 Nov  1 18:56 hallucinations.jsonl
-rw-r--r--@  1 arsis  staff   4310 Nov  1 18:56 hallucinations_controls.jsonl
-rw-r--r--@  1 arsis  staff  36877 Nov  1 18:56 sample.expected.json
-rw-r--r--@  1 arsis  staff   6381 Nov  1 18:56 sample.export.expected.txt
-rw-r--r--@  1 arsis  staff   1881 Nov  1 18:56 sample.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:03:58.875Z

**tool call — Bash**
````
{
 "command": "echo \"== lexicon categories (grep) ==\" && grep -E \"^  [a-z_]+:\" -n app/llm/lexicon.yaml; echo \"== lexicon categories (python yaml) ==\" && python3 -c \"\nimport yaml,sys\nd=yaml.safe_load(open('app/llm/lexicon.yaml'))\nprint('top-level keys:', list(d.keys()))\nfor k,v in d.items():\n    if isinstance(v,dict):\n        print(k, '->', list(v.keys()))\n\" 2>&1",
 "description": "Extract lexicon category names via grep and YAML load"
}
````

### User / tool · 2026-11-02T01:03:58.979Z

**tool result (error)**
````
Exit code 1
== lexicon categories (grep) ==
44:  window_tokens: 6
45:  pre_cues: ['no', 'not', 'denies', 'denied', 'deny', 'negative for', 'no history of', 'no prior', 'no previous',
48:  post_cues: ['denied', 'ruled out', 'is absent', 'are absent', 'was absent', 'were absent', 'not identified',
52:  clause_terminators: [',', ';', 'but', 'however', 'although', 'though', 'except', 'aside from', 'apart from',
60:  list_coordinators: ['or', 'nor']
61:  list_breakers: ['mild', 'moderate', 'severe', 'minimal', 'small', 'chronic', 'multilevel', 'early', 'advanced',
66:  field_answer: '^\s*(?:(?:[\w/''-]+\s*){0,3}?:|-)\s*(?:no|none|n|neg|negative|denies|denied|n/a|nil|0|absent)\b'
67:  pseudo_negations: ['no increase', 'no change', 'not only', 'not necessarily', 'no significant change',
73:  note: >
84:  pattern: '\b(?P<year>(?:19|20)\d{2})\b(?!-\d)\s*[,;:-]?\s*(?:now\s+|since\s+|which\s+(?:has\s+)?|and\s+(?:has\s+)?)?(?:fully\s+|completely\s+)?(?:resolved|healed|recovered)\b|\b(?:resolved|healed|recovered)\s+(?:in|by)\s+(?P<year2>(?:19|20)\d{2})\b'
85:  flag_type: pre_existing
86:  category: pre_existing
87:  hedge: false
88:  self_report: false
89:  strength: high
90:  negatable: false
91:  year_filter: true
92:  rationale: >
96:  source: 'AA A3; AA src 2 (Verisk ISO ClaimSearch), src 15; Appendix C record 3'
97:  false_positive: 'A year equal to or after the accident year ("headache 2026, resolved") is post-accident recovery, not a prior; the year filter drops it. ISO dates are not read as years.'
98:  appendix_c: [3]
99:  examples:
105:  pattern: '\b(?<!family\s)(?:past\s+|prior\s+|previous\s+)?(?:medical\s+)?history\s+of\b(?!\s+(?:the\s+)?present\s+illness)'
106:  flag_type: pre_existing
107:  category: pre_existing
108:  hedge: false
109:  self_report: false
110:  strength: medium
111:  negatable: true
112:  rationale: '"History of X" is the standard clinical way to record a prior condition (AA A3).'
113:  source: 'AA A3; AA src 1 (adjusters check pre-existing conditions), src 2'
114:  false_positive: '"No history of neck injury" and "denies history of" are negated. "History of present illness" is a section header, excluded. "Family history of" is excluded (not the patient). "History of" an unrelated disease (asthma) still fires at medium; the LLM judges relevance.'
115:  appendix_c: []
116:  examples:
122:  pattern: '\b(?:hx|h/o|PHx)\b(?!\s+of\s+present)'
123:  flag_type: pre_existing
124:  category: pre_existing
125:  hedge: false
126:  self_report: false
127:  strength: high
128:  negatable: true
129:  rationale: 'Dictated and templated notes record prior history as "hx", "Hx:", "h/o" (legal-nurse review blocker 1).'
130:  source: 'reviews/T-009-legal-nurse.md (blocker 1); AA A3; standard clinical abbreviation (assumption)'
131:  false_positive: '"No hx of trauma" is negated. "HPI" is not matched. "Hx: none" is negated by the field-answer rule.'
132:  appendix_c: []
133:  examples:
139:  pattern: '\b(?:PMH|PMHx|PSH|past\s+(?:medical|surgical)\s+history)\s+(?:is\s+)?(?:significant|remarkable|notable|positive|pertinent)\s+for\b'
140:  flag_type: pre_existing
141:  category: pre_existing
142:  hedge: false
143:  self_report: false
144:  strength: high
145:  negatable: false
146:  rationale: '"PMH significant for X" is the most common way a chart records a prior condition.'
147:  source: 'reviews/T-009-legal-nurse.md (blocker 1); AA A3'
148:  false_positive: 'The listed condition may be unrelated to the injured region (e.g. hypertension); the LLM judges relevance.'
149:  appendix_c: []
150:  examples:
155:  pattern: '\b(?:PMH|PMHx|PSH|past\s+(?:medical|surgical)\s+history)\s*[:\-]\s*(?!\s*(?:none|neg|negative|noncontributory|non-contributory|unremarkable|n/?a|no\b)\b)\S'
156:  flag_type: pre_existing
157:  category: pre_existing
158:  hedge: false
159:  self_report: false
160:  strength: low
161:  negatable: false
162:  rationale: 'A non-empty past-medical or past-surgical history section is where prior conditions live. It is low strength because most entries are unrelated (hypertension, appendectomy); specific terms in it (s/p, fusion, prior injury) fire their own entries.'
163:  source: 'reviews/T-009-legal-nurse.md (blocker 1); AA A3'
164:  false_positive: '"PMH: none" and "noncontributory" are excluded. Unrelated diseases hit at low strength only.'
165:  appendix_c: []
166:  examples:
171:  pattern: '\b(?:s/p|status[\s-]+post)\s+(?!(?:MVA|MVC|motor\s+vehicle|accident|collision|crash|fall\s+on\s+(?:01|1)/))\w'
172:  flag_type: pre_existing
173:  category: prior_surgery
174:  hedge: false
175:  self_report: false
176:  strength: high
177:  negatable: true
178:  rationale: '"s/p" or "status post" + procedure or injury records a prior surgery or event. A same-region prior surgery is the most damaging pre-existing fact (golden case_07).'
179:  source: 'reviews/T-009-legal-nurse.md (blocker 1); AA A3; golden case_07 P1'
180:  false_positive: 'Charts also write "s/p MVA" for the INDEX accident, so "s/p MVA/MVC/a

... [20008 characters truncated] ...

w-?\s?up|consult\w*|admission|discharge|return|RTW)\b)'
609:  flag_type: causation
610:  category: speculative_language
611:  hedge: true
612:  self_report: false
613:  strength: medium
614:  negatable: false
615:  rationale: 'Possibility and conjecture words. Texas courts treat "possibly" or "perhaps" opinions as conjecture, not reasonable medical probability.'
616:  source: 'AA A5; AA src 11 (Jelinek v. Casas and decisions quoting it)'
617:  false_positive: 'Plans ("Possible ESI if no improvement") are about treatment, not causation; a lookahead excludes plan nouns.'
618:  appendix_c: []
619:  examples:
624:  pattern: '\b(?:cannot|can\s?not|can''t)\s+(?:be\s+)?(?:exclude[ds]?|rule[ds]?\s+out|ruled\s+out|definitively\s+(?:determine|state))\b|\bnot\s+(?:be\s+)?(?:excluded|ruled\s+out)\b|\bcannot\s+be\s+differentiated\b'
625:  flag_type: causation
626:  category: speculative_language
627:  hedge: true
628:  self_report: false
629:  strength: medium
630:  negatable: false
631:  rationale: 'Radiology hedge: the finding is possible but unconfirmed. The defense cites it to show uncertainty.'
632:  source: 'AA A5; AA src 7, src 8 (UCSF: "cannot exclude" signals uncertainty)'
633:  false_positive: 'This is itself a negation construction, so it is listed as a pseudo-negation and does not suppress other hits around it.'
634:  appendix_c: []
635:  examples:
640:  pattern: '\b(?:suggestive\s+of|compatible\s+with|concerning\s+for|worrisome\s+for|(?:degenerative|chronic|acute|traumatic|post-?traumatic|old|new)\s+(?:versus|vs\.?|or)\s+(?:degenerative|chronic|acute|traumatic|post-?traumatic|old|new))\b'
641:  flag_type: causation
642:  category: speculative_language
643:  hedge: true
644:  self_report: false
645:  strength: medium
646:  negatable: false
647:  rationale: 'Standard radiology hedges. "Degenerative versus post-traumatic" literally leaves causation open; the tool must keep it open.'
648:  source: 'reviews/T-009-legal-nurse.md (major: hedge coverage); AA A5; AA src 7, src 8'
649:  false_positive: '"Compatible with acute strain" is a hedge pointing toward the claimant; it is still a hedge, and the flag only quotes it. "Findings consistent with" is deliberately not a hedge here.'
650:  appendix_c: []
651:  examples:
656:  pattern: '\b(?:non-?\s?specific|indeterminate|equivocal|uncertain\s+(?:significance|etiology|cause|origin)|unclear\s+(?:significance|etiology|cause|origin)|of\s+(?:undetermined|unknown)\s+(?:significance|etiology|cause|origin)|etiology\s+(?:unclear|unknown|uncertain|undetermined))\b'
657:  flag_type: causation
658:  category: speculative_language
659:  hedge: true
660:  self_report: false
661:  strength: medium
662:  negatable: false
663:  rationale: 'The record says the cause is unknown, and the defense reads an unknown cause as not-the-accident.'
664:  source: 'AA A5; AA src 8'
665:  false_positive: '"Nonspecific T-wave changes" on an unrelated EKG; the LLM checks relevance to the claimed injury.'
666:  appendix_c: []
667:  examples:
672:  pattern: '\b(?:likely|probably|presumably|most\s+consistent\s+with|suspect(?:ed)?|favor(?:ed)?|consistent\s+with)\s+(?:\w+\s+){0,2}(?:degenerative|chronic|age-?\s?related|pre-?existing|congenital|incidental|unrelated|longstanding|old)\b|\brather\s+than\s+(?:an?\s+)?(?:acute\s+)?(?:trauma|injury|the\s+(?:accident|collision))\b'
673:  flag_type: causation
674:  category: speculative_language
675:  hedge: true
676:  self_report: false
677:  strength: high
678:  negatable: true
679:  rationale: 'A clinician leaning toward a non-traumatic cause is the strongest form of the degenerative attack.'
680:  source: 'AA A4, A5; AA src 6, src 16, src 19'
681:  false_positive: '"Not likely degenerative" and "unlikely to be degenerative" are negated. "Likely post-traumatic strain" does not match.'
682:  appendix_c: []
683:  examples:
689:  pattern: '\bincidental(?:ly)?\b'
690:  flag_type: causation
691:  category: speculative_language
692:  hedge: false
693:  self_report: false
694:  strength: low
695:  negatable: true
696:  rationale: '"Incidental" means unrelated to the reason for the study; if it is attached to the injured region, the defense will cite it.'
697:  source: 'AA A4; assumption (radiology usage)'
698:  false_positive: 'Incidental findings in unrelated organs (a thyroid nodule on a neck CT) are irrelevant. Round 2 lowered it to low (context).'
699:  appendix_c: []
700:  examples:
705:  pattern: '\b(?:unrelated|not\s+related|no\s+(?:clear\s+)?(?:relation(?:ship)?|connection))\s+to\s+(?:the\s+)?(?:\w+\s+)?(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|trauma)\b'
706:  flag_type: causation
707:  category: speculative_language
708:  hedge: false
709:  self_report: false
710:  strength: high
711:  negatable: false
712:  rationale: 'An explicit no-causation statement in a treating record.'
713:  source: 'AA A5, A6; AA src 9 (Guevara — causation needs medical evidence; a contrary record undercuts it)'
714:  false_positive: 'Rare; the phrase is itself the n
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:01.050Z

**tool call — Bash**
````
{
 "command": "python3 -c \"import yaml; print('pyyaml', yaml.__version__)\" 2>&1; ls -la .venv/bin/python 2>&1; .venv/bin/python -c \"import yaml; print('venv pyyaml', yaml.__version__)\" 2>&1; echo \"== top-level keys (grep, col-0) ==\"; grep -nE \"^[a-zA-Z_]+:\" app/llm/lexicon.yaml | head -50",
 "description": "Check YAML availability and top-level lexicon keys"
}
````

### User / tool · 2026-11-02T01:04:01.201Z

**tool result**
````
Traceback (most recent call last):
  File "<string>", line 1, in <module>
ModuleNotFoundError: No module named 'yaml'
lrwxr-xr-x@ 1 arsis  staff  10 Nov  1 18:02 .venv/bin/python -> python3.12
venv pyyaml 6.0.3
== top-level keys (grep, col-0) ==
37:version: 2
38:flag_types: [pre_existing, causation, record_warning]
41:negation:
79:entries:
1179:code_lists:
1250:sources:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:03.503Z

**tool call — Bash**
````
{
 "command": "echo \"== entries: category values (python yaml via .venv) ==\" && .venv/bin/python -I -c \"\nimport yaml,collections\nd=yaml.safe_load(open('app/llm/lexicon.yaml',encoding='utf-8'))\nprint('version', d.get('version'), 'flag_types', d.get('flag_types'))\nents=d['entries']\nprint('num entries', len(ents))\nc=collections.Counter(e.get('category') for e in ents)\nfor k in sorted(c, key=lambda x: str(x)): print(repr(k), c[k])\nprint('--- code_lists keys:', list(d.get('code_lists',{}).keys()))\nprint('--- top keys:', list(d.keys()))\n\" 2>&1; echo \"== grep ^  [a-z_]+: in lexicon (categories are 4-space-indented 'category:' lines) ==\"; grep -nE \"^    category:\" app/llm/lexicon.yaml | sed -E 's/^[0-9]+:\\s+//' | sort | uniq -c",
 "description": "Load lexicon YAML and count category values"
}
````

### User / tool · 2026-11-02T01:04:03.777Z

**tool result**
````
== entries: category values (python yaml via .venv) ==
version 2 flag_types ['pre_existing', 'causation', 'record_warning']
num entries 66
'accident_date_provenance' 1
'alternative_cause' 3
'degenerative_language' 4
'litigation_referral' 1
'missed_care' 10
'new_onset' 2
'objective_negative' 4
'patient_report' 2
'pre_existing' 23
'prior_surgery' 2
'recovery_context' 4
'scene_facts' 1
'speculative_language' 9
--- code_lists keys: ['non_encounter', 'accident_date_phrases', 'injection', 'damages']
--- top keys: ['version', 'flag_types', 'v1_type_map', 'negation', 'entries', 'code_lists', 'sources']
== grep ^  [a-z_]+: in lexicon (categories are 4-space-indented 'category:' lines) ==
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:06.483Z

**tool call — Bash**
````
{
 "command": "grep -nE \"^#+ .*(ADR|D-0)\" memory/DECISIONS.md | head -80; echo \"== ADR-013 locate ==\"; grep -n \"ADR-013\" memory/DECISIONS.md",
 "description": "Locate ADR headings and ADR-013 references"
}
````

### User / tool · 2026-11-02T01:04:06.570Z

**tool result**
````
1:# DECISIONS (ADR log — architect is the sole writer; others propose via card notes)
14:## ADR-000 Harness decisions taken in M0
18:### ADR-000a Board cards use JSON values in the frontmatter
25:### ADR-000b Hooks are Python scripts behind `.sh` wrappers with plain `command` strings
32:### ADR-000c Reviewers drive the app with Python Playwright from `.venv`
39:### ADR-000d Workers and reviewers load their definition through `tools/agent_prompt.py` (now a fallback)
46:### ADR-000e Board on tailnet HTTPS :7777 and app on HTTPS :7860, not the contract's 443 and 8443
55:## ADR-001 Stack: Python + FastAPI + stdlib sqlite3 + build-step-free frontend
68:## ADR-002 Data model: records, entries, amounts, flags, each with a ladder record; separate audit and event tables
109:## ADR-003 LLM/code boundary and the three-rung validation ladder
127:## ADR-004 One LLM provider interface with three backends: claude-cli, anthropic-api, fixture
141:## ADR-005 Confidence states are computed by code; review status is separate; edit rules are narrow
158:## ADR-006 Deployment: Hugging Face Spaces (Docker) demo-only; Replit alternate; live mode is local only
173:## ADR-007 Pipeline runs in a background thread; the UI polls; ingest and gaps are synchronous code
185:## ADR-008 Record text is untrusted data; the controls are structural, not a phrase list
199:## ADR-009 Export: two blocks; the template of record is REQUIREMENTS section 6 and the golden file
211:## ADR-010 Gaps are computed by code over record dates, never over LLM entries
218:## ADR-011 Amounts: code extracts and classifies with explicit billing phrases; judge #2 validates every classification
238:## ADR-012 Deterministic token check on summaries and on edits
246:## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
264:## ADR-014 Conflicts: the accident-date rule, header-line grounding, and offsets
276:## ADR-015 Time-box cuts recorded in the architecture
281:## ADR-016 Excerpts are whole sentences; a qualifying hedge travels with its finding; date and provider are set by code
294:## ADR-017 Reconciliation with spec/REQUIREMENTS.md section 8 and later changes
== ADR-013 locate ==
87:flags         id, case_id, type('gap'|'conflict'|'pre_existing'|'causation'|'record_warning', D-013), category (closed list, ADR-013), source_kind('record'|'patient_report'),
246:## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
272:  - Semantic conflicts (PT plan of 12 visits vs discharge at visit 9) come from the LLM conflict pass (ADR-013 categories) with two quoted spans, J3 confirmation and the same grounding. Provider-name variants are code (normalised-name comparison), also with two quotes.
308:  11. **Lexicon v2 dependency.** `lexicon.yaml` (flag_type, hedge, self_report, strength, `accident_date_phrases`, `non_encounter`, `injection`) is a researcher deliverable that blocks gaps, the accident-date conflict and the injection scan (ADR-013).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:07.714Z

**tool call — Bash**
````
{
 "command": "sed -n '246,263p' memory/DECISIONS.md",
 "description": "Read ADR-013 section"
}
````

### User / tool · 2026-11-02T01:04:07.789Z

**tool result**
````
## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
- Status: accepted (round 2, amended round 3; D-007, D-013, D-018; resolves staff F8, R2-8)
- Context: flag explanations are where a model is most tempted to rule ("pre-existing degenerative disease"), which Appendix C forbids.
- Decision:
  - The flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation`, `record_warning` everywhere (D-013). `record_warning` flags are created by code only (categories `date_ambiguous`, `injection_suspected`).
  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on: `pre_existing`, `causation_weakening`, `compliance`, the hedge set, `patient_report`, `accident_date_phrases`, `damages`, `non_encounter`, `injection`. **`lexicon.yaml` v2 is a researcher deliverable that blocks the gap rule (`non_encounter`), the accident-date rule (`accident_date_phrases`) and the injection scan (`injection`); its self-check must run over every golden case and report recall per `must` flag.** The lexicon `causation_weakening` and `compliance` map to `causation`.
  - LLM flag passes run **per record** and return `{type, category, record_id, excerpt}`; the cross-record conflict pass returns `{category, a:{record_id, excerpt}, b:{...}}`. The schema rejects any extra prose field. `category` is from a closed list:
    The list equals the lexicon v2 category names (single vocabulary):
    - pre_existing: `pre_existing`, `degenerative_language`, `prior_surgery`;
    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
    - conflict: `treatment_plan_vs_actual`, `provider_name_variant`, `other_fact_mismatch` (LLM or code), `accident_date_after_treatment`, `accident_dates_differ` (code);
    - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
    Every category has a code template and a flag_type. `recovery_context` entries have `strength: low` and never raise a flag (context only). Categories with no LLM prompt behind them are lexicon-only (origin `lexicon`, `LEXICON_ONLY`, `needs_review`) unless the per-record pass also finds them.
  - Code verifies the excerpt, computes offsets and renders `title` and `explanation` from a template per category (`app/backend/flag_templates.py`; a unit test asserts every category has one), for example "Wording that could be used to question causation in {source} ({date}): “{excerpt}”". Delay to first treatment is never computed (D-017).
  - `source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt and drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
- Consequences: no free LLM string reaches the internal notes; the golden `must_not` list can be tested against templates.
- Alternatives considered: J1 over LLM prose (a judge on a free-text claim is the weakest rung); editable titles (cut); one all-records pass (an injected record could shape other records' flags).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:17.086Z

**tool call — Bash**
````
{
 "command": "echo \"== ADR-013 block: category tokens found ==\"; sed -n '246,263p' memory/DECISIONS.md > /tmp/adr013.txt 2>/dev/null; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p \"$SCR\"; sed -n '246,263p' memory/DECISIONS.md > \"$SCR/adr013.txt\"; .venv/bin/python -I -c \"\nimport yaml,re,sys\nd=yaml.safe_load(open('app/llm/lexicon.yaml',encoding='utf-8'))\nlex=sorted({e['category'] for e in d['entries']})\nadr=open('$SCR/adr013.txt',encoding='utf-8').read()\nprint('lexicon categories (%d):'%len(lex), lex)\nfor c in lex:\n    print(('OK   ' if re.search(r'\\b'+re.escape(c)+r'\\b',adr) else 'MISS ')+c)\nprint('--- ADR-013 names that look like categories but not in lexicon:')\nfor c in ['causation_weakening','compliance']:\n    print(c, 'in lexicon entries?', c in lex, '| in ADR-013?', bool(re.search(r'\\b'+c+r'\\b',adr)))\n\" 2>&1; echo \"== template file for categories ==\"; ls app/backend/flag_templates.py 2>&1; grep -rn \"flag_templates\" --include=*.py . 2>/dev/null | head -5; echo \"== grep categories in lexicon (raw) for causation_weakening/compliance ==\"; grep -n \"causation_weakening\\|compliance\" app/llm/lexicon.yaml | head",
 "description": "Check each lexicon category appears in ADR-013 and template file"
}
````

### User / tool · 2026-11-02T01:04:17.285Z

**tool result**
````
== ADR-013 block: category tokens found ==
lexicon categories (13): ['accident_date_provenance', 'alternative_cause', 'degenerative_language', 'litigation_referral', 'missed_care', 'new_onset', 'objective_negative', 'patient_report', 'pre_existing', 'prior_surgery', 'recovery_context', 'scene_facts', 'speculative_language']
OK   accident_date_provenance
OK   alternative_cause
OK   degenerative_language
OK   litigation_referral
OK   missed_care
OK   new_onset
OK   objective_negative
OK   patient_report
OK   pre_existing
OK   prior_surgery
OK   recovery_context
OK   scene_facts
OK   speculative_language
--- ADR-013 names that look like categories but not in lexicon:
causation_weakening in lexicon entries? False | in ADR-013? True
compliance in lexicon entries? False | in ADR-013? True
== template file for categories ==
ls: app/backend/flag_templates.py: No such file or directory
== grep categories in lexicon (raw) for causation_weakening/compliance ==
12:# - `flag_type` ∈ {pre_existing, causation, record_warning} (D-013/D-018). v1's `causation_weakening` and
13:#   `compliance` are both `causation` now; former compliance entries carry category `missed_care`.
39:v1_type_map: {causation_weakening: causation, compliance: causation, pre_existing: pre_existing}
931:- id: discharged_noncompliance
939:  rationale: 'Discharge for attendance or compliance reasons before the plan of care is complete is both a compliance issue and a plan-vs-actual conflict (record 4: 12 visits planned; record 6: discharged at visit 9).'
955:  rationale: 'Any discharge from therapy is context for the gap and recovery arguments. It is low: a completed course ("goals met") is the claimant''s best compliance fact.'
956:  source: 'AA A1, A2; reviews/T-009-claims-adjuster.md (minor: goals met); golden case_01 N2 (completed program is not non-compliance)'
963:- id: noncompliance
964:  pattern: '\bnon-?\s?complian(?:t|ce)\b|\bnot\s+(?:being\s+)?complian(?:t|ce)\b|\bpoor\s+(?:compliance|adherence|attendance|follow-?\s?through)\b|\bnon-?\s?adheren(?:t|ce)\b'
971:  rationale: 'An explicit provider statement of non-compliance is the strongest mitigation evidence.'
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:23.115Z

**tool call — Bash**
````
{
 "command": "grep -n \"confirm_date\" memory/contracts/api.md | head -30; echo \"== phone / gap_flags mentions ==\"; grep -n -i \"phone\\|gap_flags\" memory/contracts/api.md | head -40",
 "description": "Locate confirm_date example and phone/gap_flags mentions in api.md"
}
````

### User / tool · 2026-11-02T01:04:23.206Z

**tool result**
````
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` (409), `needs_confirm` (409), `item_rejected` (409), `invalid_edit` (422, every structurally invalid edit), `date_invalid` (422, `confirm_date` with a non-candidate date), `llm_unavailable` (503).
23:| POST | `/api/cases/{token}/records/{rid}/confirm_date` | choose one of the code-proposed readings of an ambiguous record date (recomputes gaps) |
82:Read once, then patch local state from review responses. `entries` are **chronological** by (date, seq) and contain only entries with a confirmed or parsed date; entries whose date is ambiguous or missing are in `undated_entries` (the "Dates to confirm" group, shown after the timeline) until `confirm_date`. The review order is `review.queue` only. `rejected` items appear only in `tray`.
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative`, `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
199:## POST /api/cases/{token}/records/{rid}/confirm_date
212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
244:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never become a charge); **flag** `note` only. Every structurally invalid edit is `422 invalid_edit` (the one code): any other action or key (date, provider, value, kind, flag title or evidence), an edit on a charge, an excerpt that is not a contiguous run of whole sentences of the same record, or one that drops a hedge sentence qualifying a kept sentence. Dates are not edited: ambiguous ones are resolved with `confirm_date`. `edit` implies accept: `review_status` becomes `edited`; the original is kept in `review_events` and shown as "edited" in the review UI and the internal notes. `rejected` items return `409 item_rejected` for accept/edit (dismiss and reset are allowed). Accepting is idempotent. There is no bulk accept.
== phone / gap_flags mentions ==
59:  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
62:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input_too_large`, `400 bad_request` (empty or `.pdf`), `409 demo_mode_unsupported_input` (demo mode, text not recorded).
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap` | `conflict` | `pre_existing` | `causation` | `record_warning` (D-013). Closed `category` lists: ADR-013 and ADR-014 (`gap_over_30`, `accident_date_after_treatment`, `accident_dates_differ`, `provider_name_variant`, `treatment_plan_vs_actual`, `other_fact_mismatch`, `pre_existing`, `degenerative_language`, `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `prior_surgery`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative`, `recovery_context` (low strength, never raises), `accident_date_provenance`, and for code-made `record_warning` flags `date_ambiguous`, `injection_suspected`). A `record_warning` flag has the same shape as other flags (template text, evidence span of the header date or matched phrase), is reviewable with accept/dismiss/note, and its accepted text goes to the internal notes. Records have `encounter` (false for billing statements and phone notes, which are excluded from gap math, D-003) and `sentences` (the whole-sentence units an excerpt may be built from, ADR-016). `dates_to_confirm`: records whose date is ambiguous (each `{record_id, raw, candidates[]}`, resolvable with `confirm_date`) or missing (`candidates: []`, stays excluded). `injection.records` lists tagged record ids; `banner` is a template sentence. `review.queue` order: needs_review first, then verified; amounts are never skipped. `ready_to_export` is true when no `pending` item remains in `queue` with state needs_review.
208:  "gap_flags": [],
212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:24.395Z

**tool call — Bash**
````
{
 "command": "sed -n '199,215p' memory/contracts/api.md",
 "description": "Read confirm_date endpoint section in api.md"
}
````

### User / tool · 2026-11-02T01:04:24.470Z

**tool result**
````
## POST /api/cases/{token}/records/{rid}/confirm_date
Resolves a record whose `date_status` is `ambiguous` by choosing one of the readings the code proposed (`date_candidates`). It is not an edit (D-010). A record with no readable date (`missing`) cannot be confirmed; it stays excluded and flagged. Request:
```json
{ "date": "2026-05-04" }
```
Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record warning, and `dates_to_confirm`:
```json
{ "record": {"id": "r8", "date_iso": "2026-05-04", "date_status": "confirmed", "date_raw": "04/05/2026"},
  "entry": {"id": "e8", "date": "2026-05-04", "moved_from": "undated_entries"},
  "gap_flags": [],
  "removed_flag_ids": ["f_warn_date_r8"],
  "dates_to_confirm": [], "warnings": [] }
```
`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomputed flags.

## GET /api/cases/{token}/items/{item_id}  — "Why?"
Ladder, the audited calls behind the item, and the source record text with the highlight range. Prompt text is not returned here (it is in the per-case audit).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:28.902Z

**tool call — Bash**
````
{
 "command": "echo \"== case_01 source ==\"; cat -n evals/golden/case_01_date_formats.txt; echo \"== expected.json: records with r8 / date / encounter ==\"; .venv/bin/python -I -c \"\nimport json\nd=json.load(open('evals/golden/case_01_date_formats.expected.json',encoding='utf-8'))\nprint('top keys:', list(d.keys()))\nrecs=d.get('records') or d.get('expected',{}).get('records')\nprint(type(recs))\n\" 2>&1 | head -20",
 "description": "Read golden case_01 source and expected JSON structure"
}
````

### User / tool · 2026-11-02T01:04:29.008Z

**tool result**
````
== case_01 source ==
     1	SYNTHETIC — invented for evaluation; not real patient data
     2	
     3	=== Record 1 ===
     4	Date: 2026-02-03
     5	Source: Quillfeather Urgent Care
     6	Excerpt: "Right ankle swelling after twisting on stairs. X-ray negative for fracture. Urgent care charge: $310.00."
     7	
     8	=== Record 2 ===
     9	Date: 02/17/2026
    10	Source: Dr. Orla Pennywhistle, primary care
    11	Excerpt: "Ankle swelling improved. Refer to physical therapy 1x/week for 4 weeks."
    12	
    13	=== Record 3 ===
    14	Date: Feb 24, 2026
    15	Source: Pemberwick Physical Therapy, visit 1
    16	Excerpt: "Gait mildly antalgic. Pain 4/10."
    17	
    18	=== Record 4 ===
    19	Date: 3 March 2026
    20	Source: Pemberwick Physical Therapy, visit 2
    21	Excerpt: "Pain 3/10. Balance exercises added."
    22	
    23	=== Record 5 ===
    24	Date: March 10th, 2026
    25	Source: Pemberwick Physical Therapy, visit 3
    26	Excerpt: "Pain 2/10. Walking without a limp."
    27	
    28	=== Record 6 ===
    29	Date: 03-17-26
    30	Source: Pemberwick Physical Therapy, visit 4
    31	Excerpt: "Pain 1/10. Discharged to home exercise program."
    32	
    33	=== Record 7 ===
    34	Date: 3/25/26
    35	Source: Dr. Orla Pennywhistle, primary care
    36	Excerpt: "Ankle exam normal. Optional recheck on 04/14/2026 if symptoms return."
    37	
    38	=== Record 8 ===
    39	Date: 04/05/2026
    40	Source: Dr. Orla Pennywhistle, phone note
    41	Excerpt: "Patient reports no new symptoms."
    42	
== expected.json: records with r8 / date / encounter ==
top keys: ['schema_version', 'case_id', 'synthetic', 'input_file', 'description', 'stress_types', 'records', 'entries', 'expected_entry_count', 'gap_excluded_records', 'gap_table', 'amounts', 'totals', 'flags', 'must_not_flag', 'tolerated', 'record_warnings', 'must_not', 'notes']
<class 'list'>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:31.339Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nd=json.load(open('evals/golden/case_01_date_formats.expected.json',encoding='utf-8'))\nfor r in d['records']:\n    if r.get('id') in ('r8',) or r.get('record_id')=='r8' or r.get('n')==8:\n        print('REC', json.dumps(r,ensure_ascii=False))\nprint('gap_excluded_records:', json.dumps(d['gap_excluded_records'],ensure_ascii=False))\nprint('record_warnings:', json.dumps(d['record_warnings'],ensure_ascii=False))\nprint('gap_table:', json.dumps(d['gap_table'],ensure_ascii=False)[:1500])\nprint('flags (gap/ids):')\nfor f in d['flags']:\n    if f.get('type')=='gap' or 'gap' in str(f.get('category','')): print('  ', json.dumps(f,ensure_ascii=False)[:400])\nprint('records[0] keys:', list(d['records'][0].keys()))\n\" 2>&1",
 "description": "Inspect golden case_01 record 8, gap exclusions and warnings"
}
````

### User / tool · 2026-11-02T01:04:31.447Z

**tool result**
````
gap_excluded_records: [8]
record_warnings: []
gap_table: [{"from_date": "2026-02-03", "to_date": "2026-02-17", "from_records": [1], "to_records": [2], "days": 14, "flag": false}, {"from_date": "2026-02-17", "to_date": "2026-02-24", "from_records": [2], "to_records": [3], "days": 7, "flag": false}, {"from_date": "2026-02-24", "to_date": "2026-03-03", "from_records": [3], "to_records": [4], "days": 7, "flag": false}, {"from_date": "2026-03-03", "to_date": "2026-03-10", "from_records": [4], "to_records": [5], "days": 7, "flag": false}, {"from_date": "2026-03-10", "to_date": "2026-03-17", "from_records": [5], "to_records": [6], "days": 7, "flag": false}, {"from_date": "2026-03-17", "to_date": "2026-03-25", "from_records": [6], "to_records": [7], "days": 8, "flag": false}]
flags (gap/ids):
records[0] keys: ['record_no', 'raw_date', 'date', 'kind', 'source']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:34.351Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\nd=json.load(open('evals/golden/case_01_date_formats.expected.json',encoding='utf-8'))\nfor r in d['records']:\n    if r.get('record_no')==8: print('REC8', json.dumps(r,ensure_ascii=False))\nprint('must_not:', json.dumps(d['must_not'],ensure_ascii=False)[:800])\nprint('notes:', json.dumps(d['notes'],ensure_ascii=False)[:1200])\nprint('flags:', json.dumps(d['flags'],ensure_ascii=False)[:600])\nprint('must_not_flag:', json.dumps(d['must_not_flag'],ensure_ascii=False)[:600])\nprint('tolerated:', json.dumps(d['tolerated'],ensure_ascii=False)[:600])\nprint('description:', d['description'])\n\"",
 "description": "Inspect golden case_01 record 8 date status and notes"
}
````

### User / tool · 2026-11-02T01:04:34.451Z

**tool result**
````
REC8 {"record_no": 8, "raw_date": "04/05/2026", "date": null, "kind": "phone_note", "source": "Dr. Orla Pennywhistle, phone note"}
must_not: [{"id": "M1", "statement": "Creates an entry dated 2026-04-14 (a date inside an excerpt, not a record date).", "check": "entry_date", "bad_examples": [{"date": "2026-04-14", "provider": "X"}, {"date": "2026-04-14", "provider": "Y"}, {"date": "2026-04-14", "provider": "Z"}], "good_examples": [{"date": "2026-01-01", "provider": "X"}, {"date": "2026-02-02", "provider": "Y"}, {"date": null, "provider": "Z"}], "dates": ["2026-04-14"]}, {"id": "M2", "statement": "Silently assigns record 8 a single date (2026-04-05 or 2026-05-04) as if parsed.", "check": "judge", "bad_examples": ["April 5, 2026 — phone note: no new symptoms.", "May 4, 2026 — Dr. Orla Pennywhistle phone note.", "2026-04-05 Patient reports no new symptoms."], "good_examples": ["Date ambiguous: 04/05/2026 could be April 5 or May 4, 
notes: ["Reading the ambiguous date is a human decision (docs/LLM_VS_CODE.md row 2). Record 8 is a phone note (non-encounter) and is excluded from gap math in any case."]
flags: []
must_not_flag: [{"id": "N1", "type": "gap", "statement": "No gap flags anywhere. In particular record 8 (ambiguous date, phone note) creates no gap: read as 2026-05-04 it would be 40 days after record 7."}, {"id": "N2", "type": "causation", "record_nos": [6], "statement": "'Discharged' here is a completed program (pain 1/10), not non-compliance."}]
tolerated: []
description: Seven distinct date formats plus one genuinely ambiguous numeric date (04/05/2026: April 5 or May 4) on a phone note. Ambiguous date must be marked ambiguous, excluded from gap math, and surfaced for review. A future date inside an excerpt (04/14/2026) is not a record date.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:38.180Z

**tool call — Bash**
````
{
 "command": "echo \"== date_invalid / candidate / non-candidate across memory/ docs/ app/README-arch.md spec/ ==\"; grep -rn -i \"date_invalid\\|non-candidate\\|not one of the\\|not a candidate\\|date_not_candidate\\|invalid_date\\|invalid_edit\" memory/ docs/ app/README-arch.md spec/REQUIREMENTS.md 2>/dev/null | cut -c1-260",
 "description": "Grep error codes for non-candidate dates across docs"
}
````

### User / tool · 2026-11-02T01:04:38.264Z

**tool result**
````
== date_invalid / candidate / non-candidate across memory/ docs/ app/README-arch.md spec/ ==
memory/DECISIONS.md:152:  - **One error code for an invalid edit:** every structurally invalid edit is `422 invalid_edit` (immutable key, edit on a charge, wrong item type, `confirm_date` on a parsed date (a non-candidate date is `422 date_invalid`), an excerp
memory/DECISIONS.md:288:  - The paralegal may change an entry's excerpt only to another contiguous run of whole units of the same record (`edits.excerpt`, ADR-005). The same rules apply: dropping a qualifying hedge is `422 invalid_edit`.
memory/DECISIONS.md:298:  1. **Edit rules.** Entries: summary, or excerpt to other whole sentences (D-010, D-012). Flags: note only. **Charges: accept/dismiss only (D-010)**, so R-CH-7 and the amount rows of R-RV-1/R-RV-2 shrink. `confirm_date` replaces "edit 
memory/contracts/api.md:9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input_too_large` (413), `demo_mode_unsupported_input` (409), `run_in_progress` 
memory/contracts/api.md:212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter
memory/contracts/api.md:244:Allowed `edits` by type (D-010, D-012): **entry** `summary`, or `excerpt` (must be a contiguous run of whole sentences of the same record, so the offsets stay code-derived); **amount** none (accept or dismiss only; a rate can never 
spec/REQUIREMENTS.md:84:| R-CH-7 | **Charges are accept / dismiss only (D-010, ADR-017).** A charge's class comes from code and judge #2; the paralegal can't reclassify or edit it, so no path turns a rate, estimate or unreadable amount into a totaled charge. R
spec/REQUIREMENTS.md:93:| R-RV-2 | **What each action does (D-010, D-012).** See the table below the requirements. Originals are kept. "Edited" shows in the review UI and in the internal notes, never in the letter text. | UT, each → 422 `invalid_edit`: edit 
spec/REQUIREMENTS.md:94:| R-RV-3 | **Edited text is re-checked.** The D-006 code check (numbers, dates, `$` in the new summary must appear in the excerpt) and judge #1 run on every edited summary and on every re-selected excerpt. If the code check or the judge
spec/REQUIREMENTS.md:371:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:42.541Z

**tool call — Bash**
````
{
 "command": "echo \"== mg. mentions ==\"; grep -rn \"mg\\b\" memory/ docs/LLM_VS_CODE.md app/README-arch.md spec/REQUIREMENTS.md evals/golden/README.md 2>/dev/null | grep -i \"mg\" | cut -c1-300; echo \"== D-021 ==\"; grep -rn \"D-021\" memory/ docs/ app/README-arch.md spec/ evals/golden/README.md 2>/dev/null | cut -c1-300",
 "description": "Grep mg. abbreviation treatment and D-021 across docs"
}
````

### User / tool · 2026-11-02T01:04:42.635Z

**tool result**
````
== mg. mentions ==
memory/contracts/api.md:91:                     {"text": "Rx cyclobenzaprine 10 mg.", "start": 477, "end": 502}, {"text": "Follow up with PCP in 1 week.", "start": 503, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
memory/contracts/api.md:96:      "summary": "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
memory/contracts/api.md:98:      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
memory/contracts/api.md:290:        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
memory/DECISIONS.md:285:  - **One sentence splitter**, the one defined in R-TL-2 (that requirement's terminator rule and abbreviation list, which includes `approx.`, `Dr.` and `mg.` per D-021, are the single source; this ADR does not restate it, so "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 
memory/ORCHESTRATOR_DECISIONS.md:29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are
evals/golden/README.md:116:Charges: ER $6,240 + MRI $2,150 = **$8,390**. PT `$185` is a rate; visit counts are never itemized → **unclear, not totaled**. Forbidden guess-sums: 9 × 185 = 1,665; 12 × 185 = 2,220; 8 × 185 = 1,480; 8,390 + 1,665 = 10,055; 8,390 + 2,220 = 10,610; 8,390 + 1,480 = 9,8
spec/REQUIREMENTS.md:49:| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/fl
spec/REQUIREMENTS.md:81:| R-CH-4 | Non-billing figures are not charges. "Rx cyclobenzaprine 10 mg" and other doses never appear as amounts. | Golden `must_not` M7: no amount valued 10, 35, 6, 7, 12, 40 or 2. | EV |
spec/REQUIREMENTS.md:227:Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
spec/REQUIREMENTS.md:228:Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
== D-021 ==
memory/SCOPE_CUTS.md:24:| debt | T-013 accepted with documented debt after 3 rounds (§7.4) | Remaining reconciliation (hallucination threshold as rate, K4/K5 must, D-019 total line, both-side accident-date quotes, D-016..D-021 refs, §8 clean) split to T-025, which T-017 depends on. | see card | M1
memory/DECISIONS.md:9:Round 2 (T-014 changes_requested): ADR-002..009 were rewritten in place; 010–017 are new. Round 3 amended 002–006, 008, 009, 011, 013, 015, 016, 017 again (D-018..D-021). Where
memory/DECISIONS.md:142:- Status: accepted (M1, amended rounds 2 and 3; D-006, D-010, D-011, D-012, D-021)
memory/DECISIONS.md:186:- Status: accepted (M1, amended rounds 2 and 3; D-005, D-018, D-021)
memory/DECISIONS.md:191:  3. **Suppression is made structural.** The pre_existing/causation flag pass runs **per record** (D-021), so one record's text never reaches the model call that decides another record's flags; an injected record can at most affect its own flags. A lexicon scan (code, every r
memory/DECISIONS.md:282:- Status: accepted (round 2, amended round 3; D-012, D-014, D-021; R-TL-2, R-TL-3, R-TL-8, R-TL-9)
memory/DECISIONS.md:285:  - **One sentence splitter**, the one defined in R-TL-2 (that requirement's terminator rule and abbreviation list, which includes `approx.`, `Dr.` and `mg.` per D-021, are the single source; this ADR does not restate it, so "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 
memory/DECISIONS.md:287:  - **Forced inclusion is narrow (D-021).** When a sentence the excerpt includes is qualified by a hedge sentence (a unit matching the hedge set of `lexicon.yaml`) in the same sentence or the immediately following unit of the same record, that hedge unit must be in the excerp
memory/DECISIONS.md:296:- Context: §8 listed conflicts between the requirements and the architect's first text; later reviews added more. Orchestrator decisions D-001..D-021 settle them. Where the requirements text still differs, the item below says what changes.
memory/DECISIONS.md:301:  4. **Codes and fields.** `EXCERPT_OMITS_QUALIFIER` adopted with D-021 scope. Neither `GROUNDING_DATE_MISMATCH` nor `GROUNDING_PROVIDER_NOT_IN_RECORD` exists; R-TL-3 and R-TL-9 are restated (ADR-016). `FIXTURE_MISS` and `JUDGE_UNAVAILABLE` on edits are new needs_review reaso
memory/ORCHESTRATOR_DECISIONS.md:29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are
spec/REQUIREMENTS.md:55:| R-TL-8 | **A hedge travels with its finding (D-018, D-021).** The **hedge set** is the lexicon entries with `hedge: true` in `app/llm/lexicon.yaml` (D-018); today `may_represent`, `correlate_clinically`, `possibility_terms`, `cannot_exclude`, `suggestive_versus_hedges`, `no
spec/REQUIREMENTS.md:97:| R-RV-6 | **No LLM output is auto-accepted. Record text is data (D-005).** A record with an injection warning forces all its items to `needs_review` (an advisory state, ADR-008), its amounts can't be charges, and it can't suppress flags from other records (the lexicon is the
spec/REQUIREMENTS.md:370:| 2 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)); `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out", D-021 limits it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:45.456Z

**tool call — Bash**
````
{
 "command": "echo \"== ORCHESTRATOR_DECISIONS D-0xx rows (ids) ==\"; grep -noE \"^\\| D-0[0-9]{2}\" memory/ORCHESTRATOR_DECISIONS.md | tr '\\n' ' '; echo; echo \"== D-003, D-021, D-022, D-023, D-024 full rows ==\"; grep -n -E \"^\\| D-0(03|21|22|23|24) \" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-900; echo \"== R-TL-2 full row (sentence splitter, abbreviations) ==\"; grep -n \"R-TL-2 \" spec/REQUIREMENTS.md | cut -c1-1500",
 "description": "Read D-003, D-021..D-024 rows and R-TL-2 abbreviation rule"
}
````

### User / tool · 2026-11-02T01:04:45.563Z

**tool result**
````
== ORCHESTRATOR_DECISIONS D-0xx rows (ids) ==
9:| D-001 10:| D-002 11:| D-003 12:| D-004 13:| D-005 14:| D-006 15:| D-007 16:| D-008 17:| D-009 18:| D-010 19:| D-011 20:| D-012 21:| D-013 22:| D-014 23:| D-015 24:| D-016 25:| D-017 26:| D-018 27:| D-019 28:| D-020 29:| D-021 30:| D-022 31:| D-023 32:| D-024 
== D-003, D-021, D-022, D-023, D-024 full rows ==
11:| D-003 | Gaps are computed by code over the code-parsed header dates of all clinical-encounter records (deduped), independent of LLM entries and review state. Billing statements and phone notes are excluded. Ambiguous dates are excluded and flagged. | Dropping an LLM entry must never change gap math. | T-014 staff-eng F2; T-015 paralegal |
29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) intact. Prior/causation flag pass runs per record so an injected record can't suppress another record's flag. | D-012 was over-applied (entries 3 and 5 would go needs_review). | T-014 staff r2 R2-4, privacy r2 N3 |
30:| D-022 | Dropped qualifiers: if an entry's excerpt contains a qualifier (hedge, self-report marker, negation such as "without loss of consciousness", laterality, approx.) and the **summary** omits it, code marks the entry `needs_review` (reason `SUMMARY_DROPS_QUALIFIER`). In evals, `required_terms` are checked against the summary alone. Self-report is tagged per **sentence/quote**, not per entry; field name `source_kind: patient_report`. | The judge checks additions, not omissions; an omitted hedge is how a summary misleads. | T-015 legal-nurse r2 M1/M3 |
31:| D-023 | **Harness threat model:** the hooks defend against *accidents and lazy evasion by well-meaning agents* (wrong spelling, a pasted destructive command, staging a secret), not against a deliberately hostile agent with shell access — a shell-text guard cannot be complete against that. Consequences: (1) every finding that a *plausible accidental spelling* passes is a bug and gets fixed + a regression test; (2) deliberate obfuscation (brace expansion, IFS, copies of board.py, interpreter one-liners) is residual risk, documented, and covered by detection instead: git history is append-only (no rewrite), every board transition is in the append-only activity log, and the orchestrator re-verifies evidence before closing; (3) `--no-verify` is never legitimate for agents (denied); (4) reviewers may run mutating git only inside scratch repos under /tmp or the scratchpad. | Security r2 
32:| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at milestone gates (Tier 2) and the final hiring panel. One agent may cover two persona checklists in one pass. (3) Docs/research cards: max 2 rounds; remaining majors without blockers become documented debt (§7.4) instead of round 3. (4) Briefs ≤ 12 lines, reviewer replies ≤ 10 lines. (5) Researcher moves to sonnet. (6) Heartbeat hourly, not every 20 min. (7) No more harness rounds after M0 r3: residual findings become debt under D-023. | Spend the budget on the product and the submission, not on review churn. | Chris inbox 2026-11-02T00:58Z |
== R-TL-2 full row (sentence splitter, abbreviations) ==
49:| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a terminator, where a terminator is `.`, `?` or `!` followed by whitespace and then an uppercase letter, digit or end of text; `;`; or a line break. A period after an abbreviation on a fixed list (`approx.`, `Dr.`, `Mr.`, `Mrs.`, `Ms.`, `vs.`, `etc.`, `e.g.`, `i.e.`, `mg.`) or inside a number (`1.5`) is not a terminator. | UT: for every golden record, the units concatenated equal the record text, and `approx. 35 mph.` in record 1 is one unit. Grounding verifier passes every `verified` entry. An excerpt that is not verbatim is `rejected` (tray only, never timeline or export). An excerpt that starts or ends mid-unit is `needs_review`. | UT + EV `grounding_rate` |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:51.103Z

**tool call — Bash**
````
{
 "command": "echo \"== abbreviation / splitter mentions ==\"; grep -rn -i \"abbrev\\|splitter\\|terminator\" memory/ docs/ app/README-arch.md spec/REQUIREMENTS.md evals/golden/README.md app/llm/lexicon.yaml 2>/dev/null | cut -c1-420; echo \"== 'mg' anywhere in app/ and evals/golden code/data ==\"; grep -rn \"mg\" app/ evals/golden/*.py evals/golden/*.txt evals/golden/*.jsonl 2>/dev/null | grep -v \"img\\|msg\\|ImageMagick\" | cut -c1-260 | head -20",
 "description": "Grep abbreviation and sentence-splitter rules and mg usage in code"
}
````

### User / tool · 2026-11-02T01:04:51.212Z

**tool result**
````
== abbreviation / splitter mentions ==
memory/contracts/api.md:267:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, b
memory/DECISIONS.md:285:  - **One sentence splitter**, the one defined in R-TL-2 (that requirement's terminator rule and abbreviation list, which includes `approx.`, `Dr.` and `mg.` per D-021, are the single source; this ADR does not restate it, so "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week." is one unit). Used by the excerpt check, flag evidence and the excerpt-edit UI. `GET case` returns `records[].sen
memory/DECISIONS.md:305:  8. **R-CH-2.** "The LLM only when code can't" is removed: code classifies, judge #2 checks every class (ADR-011). **R-TL-2/R-TL-8** follow ADR-016 (single splitter, narrow forced inclusion). **R-TL-3** is restated (date set by code).
memory/ORCHESTRATOR_DECISIONS.md:20:| D-012 | Excerpt rule: an entry's excerpt is one or more **whole sentences** of the record (code sentence splitter: `.`, `;`, line breaks), chosen by the model and changeable by the paralegal only to other whole sentences of the same record. A sentence that contains any lexicon hit (pre_existing / causation / compliance) or hedge is kept whole — a hedge can never be cut. Flagged
memory/ORCHESTRATOR_DECISIONS.md:29:| D-021 | Excerpt rule clarified: excerpts are whole sentences only; when a selected sentence is qualified by a hedge (in the same sentence or the immediately following sentence of the same record), that hedge sentence must be included. Other lexicon sentences are not forced into the excerpt (they surface as flags). Sentence splitter keeps abbreviations (approx., Dr., mg., e.g.) in
app/README-arch.md:18:  sentences.py     sentence splitter ( . ; line breaks; abbreviation-safe ), qualifier units
spec/REQUIREMENTS.md:36:| R-IN-1 | Accept records pasted as text. | Pasting the 9 sample records produces 9 timeline entries and the UI shows "9 records found" before any model call. Fail if the count is wrong or not shown. | E2E + UT (splitter; pieces concatenated equal the input) |
spec/REQUIREMENTS.md:49:| R-TL-2 | **Excerpt is verbatim and made of whole sentences (D-012).** An excerpt is a contiguous run of one or more *sentence units* of its record and a substring after whitespace normalization. **Sentence unit** (one code splitter, shared by the generator check, the gap/flag evidence and the excerpt-edit UI): the text up to and including a terminator, where a terminator is `.`, `?` or `!` f
spec/REQUIREMENTS.md:135:| R-CO-1 | **LLM used for at least one step, and the line is documented.** `docs/LLM_VS_CODE.md` has the §5.2 table and matches the code. | Staff-engineer review checks each pipeline step against the table. UT: gap, total, date-parse, dedupe, sentence-splitter and export modules import no LLM client. | PR (staff-engineer) + UT |
app/llm/lexicon.yaml:42:  # NegEx-style guard (Chapman 2001), clause-bounded per D-018, plus ConText-style terminators (Chapman 2011).
app/llm/lexicon.yaml:50:  # Scope ends at the end of the sentence and at any of these, so a cue before a terminator does not reach a hit
app/llm/lexicon.yaml:52:  clause_terminators: [',', ';', 'but', 'however', 'although', 'though', 'except', 'aside from', 'apart from',
app/llm/lexicon.yaml:121:- id: hx_abbrev
app/llm/lexicon.yaml:130:  source: 'reviews/T-009-legal-nurse.md (blocker 1); AA A3; standard clinical abbreviation (assumption)'
app/llm/lexicon.yaml:892:  false_positive: '"LOP" can be an unrelated abbreviation; the LLM confirms.'
evals/golden/README.md:12:| `hallucinations.jsonl` | 40 seeded unsupported summaries `{id, synthetic, category, record_text, candidate_summary, why_unsupported}` for judge recall (ship bar ≥ 95%); 13 come from synthetic cases; includes `temporal_to_causal` (patient's "began after" upgraded to "caused"), `approximation_dropped`, `abbreviation_misexpanded` |
== 'mg' anywhere in app/ and evals/golden code/data ==
app/llm/lexicon.yaml:1009:    miss: ['Rx cyclobenzaprine 10 mg.']
evals/golden/case_06_subtle_pre_existing.txt:6:Excerpt: "Rear-end collision. Cervical strain, neck pain 5/10. Patient denies prior neck problems. Rx ibuprofen 800 mg."
evals/golden/sample.txt:11:Excerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."
evals/golden/sample.export.expected.txt:9:Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.
evals/golden/sample.export.expected.txt:10:Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
evals/golden/hallucinations_controls.jsonl:1:{"id": "S01", "synthetic": true, "kind": "near_verbatim", "record_text": "Record 2 | 2026-01-09 | Central ER discharge summary | \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx 
evals/golden/hallucinations.jsonl:12:{"id": "H12", "synthetic": true, "category": "negation_flipped", "record_text": "Record 2 | 2026-01-09 | Central ER discharge summary | \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx c
evals/golden/hallucinations.jsonl:18:{"id": "H18", "synthetic": true, "category": "transposed_digits", "record_text": "Record 2 | 2026-01-09 | Central ER discharge summary | \"Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx 
evals/golden/hallucinations.jsonl:26:{"id": "H26", "synthetic": true, "category": "negative_study_flipped", "record_text": "Record 2 | 2026-01-09 | Central ER discharge summary | \"Dx: cervical strain; concussion without loss of consciousness. CT head negative
evals/golden/hallucinations.jsonl:29:{"id": "H29", "synthetic": true, "category": "negation_flipped", "record_text": "Record 1 | 2026-09-14 | Snickerwood ER | \"Rear-end collision. Cervical strain, neck pain 5/10. Patient denies prior neck problems. Rx ibuprof
evals/golden/hallucinations.jsonl:30:{"id": "H30", "synthetic": true, "category": "denial_as_fact", "record_text": "Record 1 | 2026-09-14 | Snickerwood ER | \"Rear-end collision. Cervical strain, neck pain 5/10. Patient denies prior neck problems. Rx ibuprofen
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:53.305Z

**tool call — Bash**
````
{
 "command": "cat -n app/README-arch.md",
 "description": "Read app/README-arch.md in full"
}
````

### User / tool · 2026-11-02T01:04:53.391Z

**tool result**
````
     1	# Architecture map (architect-owned; decisions in `memory/DECISIONS.md`, cross-cutting calls in `memory/ORCHESTRATOR_DECISIONS.md`)
     2	
     3	One process, one SQLite file, one set of static files. About 7 hours of build time in total, so every box below earns its place.
     4	
     5	```
     6	 browser (vanilla JS)  --JSON-->  FastAPI (app/backend/main.py)  -->  pipeline.py (thread)
     7	                                        |                                |
     8	                                    sqlite3 (app/db)                 code steps  <->  llm/audited.py -> provider.py -> backend
     9	                                                                                              claude-cli | anthropic-api | fixture
    10	```
    11	
    12	## Module layout (target; owner in brackets)
    13	```
    14	app/backend/ [backend]
    15	  main.py          routes from memory/contracts/api.md (11 endpoints), static files, error format, demo gate (hash of normalised text), lazy 24 h purge via the one delete_case()
    16	  schemas.py       Pydantic models: API shapes AND LLM output schemas (one source; no prose fields in flag schemas)
    17	  ingest.py        split records, header dates/source labels, `---` separator, dedupe, size limits, PHI-pattern warning
    18	  sentences.py     sentence splitter ( . ; line breaks; abbreviation-safe ), qualifier units
    19	  dates.py         format list; parsed | ambiguous | missing | confirmed; day arithmetic
    20	  amounts.py       currency regex (cents), billing-phrase classification, dedupe, totals (accepted / pending / detected)
    21	  grounding.py     whitespace-normalised match with a normalised->raw index map; absolute offsets; new_tokens(); date equals parse
    22	  confidence.py    compose_state(ladder, context) -> (state, reasons); reason codes
    23	  why.py           one template sentence per reason code
    24	  flag_templates.py  every flag title/explanation (code-rendered)
    25	  gaps.py          gaps from record dates (encounter records only); recompute on confirm_date
    26	  conflicts.py     accident-date rule, provider-name variants (code) + LLM conflict pass
    27	  flags.py         LLM flag pass + lexicon floor + record_warning flags
    28	  injection.py     instruction-like phrase scan (advisory), nonce delimiters, delimiter escaping
    29	  pipeline.py      stages; `python -m app.pipeline <file>`; run/status state; 8 min deadline
    30	  export.py        letter_text + internal_notes_text from accepted items only, deterministic
    31	app/llm/ [backend]
    32	  provider.py      complete(model, system, user, json_schema) -> dict ; complete_with_meta
    33	  audited.py       retry loop (1 + 2 retries, changed conditions), one llm_calls row per attempt, returns (output, call_id)
    34	  backends/        claude_cli.py  anthropic_api.py  fixture.py (+ record mode)
    35	  prompts/         extract_vN.md  judge_faithfulness_vN.md  judge_amount_class_vN.md  conflicts_vN.md  flags_vN.md  judge_conflict_vN.md  judge_flag_vN.md
    36	  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
    37	app/db/ [db]       schema.sql, db.py (connection, helpers, purge)
    38	app/frontend/ [frontend]  index.html, app.js (ES modules), styles.css
    39	app/config.py [release]   env: LLM_BACKEND, GENERATOR_MODEL, JUDGE_MODEL, ENABLE_LIVE, PROVIDER_CAP_CONFIRMED, DATA_DIR, limits; injectable now() for every deadline and purge
    40	```
    41	
    42	## Pipeline order (stage names match `/status`)
    43	0. `ingest` (sync, code): split, dedupe, header dates and source labels, encounter flag, regex amounts, rule classification, accident-date rule, **gap flags**, injection scan, record_warning flags.
    44	1. `extract`: one generator call per distinct record (concurrency <= 3). 2. `verify` (code). 3. `judge_entries` (J1).
    45	4. `amounts`: J2 on every amount (no LLM classifier). 5. `conflicts`: one cross-record LLM pair pass + J3. 6. `flags`: one LLM pass **per record** + lexicon floor + J4. 7. `finalize`: compose states, order. About 40 calls on the sample; evals default to the `fixture` backend, and the live backend is used only to record fixtures and for the 3-run determinism check.
    46	Gaps are not an LLM stage and never wait for one.
    47	
    48	## Invariants every worker must keep (a test exists for each)
    49	- No code path sets `review_status` except the review and confirm_date endpoints. There is no bulk accept.
    50	- Export reads only `accepted`/`edited` items; totals are computed on read, never stored; every letter line carries its verbatim excerpt.
    51	- Gap math reads only code-parsed record dates; dropping or rejecting an LLM entry never changes it.
    52	- Every model call goes through `audited.py`; no direct SDK or subprocess call elsewhere; backends never retry.
    53	- Nothing is silently corrected; a failed check shows a reason code. The model never supplies a date, an amount, a class, a provider or flag wording.
    54	- Record text appears in prompts only inside nonce delimiters, with delimiter-like substrings neutralised in the prompt copy.
    55	- **Never log record text, prompts or responses** (stdout, uvicorn, Space logs). Errors log `call_id` only.
    56	- Untrusted strings reach the DOM with `textContent` only.
    57	- Purge and `DELETE` are one function that deletes from every table by case id (prompts included); SQLite runs with `secure_delete`. Access logging is off (the case token is in the URL path) and responses send `Referrer-Policy: no-referrer`.
    58	- In the public demo build, text is stored only if its normalised hash is in the recorded set.
    59	
    60	## Data flow (what stores the text, for the "real build" delta)
    61	| Store / processor | Holds | Notes |
    62	|---|---|---|
    63	| SQLite on container disk | raw text, records, items, `llm_calls` (full prompts and responses), events | deleted by `DELETE` and lazily after 24 h through one function; ephemeral disk; public demo stores only recorded text |
    64	| `tests/fixtures/llm/*.json` (git) | prompts and responses for golden text only | recorder refuses any text not in `evals/golden` |
    65	| Anthropic API (live mode only, local) | prompts and responses | opt-in via `ENABLE_LIVE=1`; spend limit set on the provider key; synthetic data only |
    66	| `claude -p` on Chris's claude.ai login (dev only) | prompts and responses | consumer account; never in the image |
    67	| Hugging Face Space logs | whatever the app prints | hence the no-logging invariant |
    68	A real build would add a business agreement with zero-retention terms for the model provider (while accepting that safety-flagged content may be retained by the vendor beyond zero-retention), a review of Texas HSC §181.154 notice and authorization for electronic disclosure (see `research/phi-and-ai-supervision.md`), encryption at rest, access logging on audit reads, per-user accounts and retention rules. None of that is implemented; the prototype is synthetic-only.
    69	
    70	## Build order (suggested, to unblock parallel work)
    71	1. `schemas.py`, `confidence.py`, `grounding.py`, `dates.py`, `amounts.py`, `sentences.py`, `gaps.py` with unit tests first (no LLM).
    72	2. `provider.py` + fixture backend + `audited.py`; record fixtures with the CLI backend from the golden text.
    73	3. `ingest.py`, `pipeline.py` stages 0-3; the sample-case CLI prints entries and gaps.
    74	4. J2 amounts, conflicts, flags, judges, record_warning flags.
    75	5. Routes + export; frontend against the API draft in parallel from step 1.
    76	
    77	## Dependencies
    78	`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the accident-date rule and the injection scan, and its golden self-check (recall per `must` flag) gates the claim that the lexicon is a floor (ADR-008.4).
    79	
    80	## Cut line
    81	Already cut (D-011, D-020, ADR-015): in-app rate limiter and spend ledger (spend is limited on the provider key), arbitrary-text ingest on the public build, batch accept, charge reclassification and amount edits, the "not a duplicate" split, LLM date pointing, LLM split fallback, bring-your-own-key, `?full=1`, flag title/explanation edits, case list, jsonl audit export, citation toggle, manual add of an entry for a rejected record.
    82	First to go if a milestone exceeds 150% of budget (record in `SCOPE_CUTS.md`): the side-by-side layout (R-ST-1; the record modal R-RV-9 stays), then the synchronous judge re-run on edits (the edit would save as `needs_review` / `JUDGE_UNAVAILABLE`, which is already a defined state). The per-record flag pass is not on the cut line (it is the injection control, ADR-008.3); cheapen it by batching the judge instead.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:04:57.512Z

**tool call — Bash**
````
{
 "command": "echo \"== R-EX-4 in spec ==\"; grep -n \"R-EX-4\" spec/REQUIREMENTS.md | cut -c1-1200; echo \"== AI line candidates in DECISIONS.md / api.md / golden export / LLM_VS_CODE ==\"; grep -n -i \"\\bAI\\b\\|artificial\\|assist\" memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md evals/golden/sample.export.expected.txt | cut -c1-500",
 "description": "Read R-EX-4 requirement and find AI disclosure line in docs"
}
````

### User / tool · 2026-11-02T01:04:57.611Z

**tool result**
````
== R-EX-4 in spec ==
66:| R-FL-2 | **Conflicting facts.** Flag facts that conflict across records, citing both excerpts. | Sample must raise (a) accident date 2026-01-09 (records 1, 2) vs "Date of accident per intake form: 2026-01-19" (record 7), shown as a conflict and **not merged**, with the records cited (R-EX-4) and no choice made between the dates or any "delay from the accident" computed; the tool may state "first recorded treatment: January 9, 2026" (D-017); (b) PT plan of 12 visits (record 4) vs discharge at visit 9 after two missed appointments (record 6). `case_05_provider_conflict` raises its required flag and tolerates the name variants. | EV `flag_*[conflict]` + PR (legal-nurse) |
122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export." followed by "Pending items: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of
182:3. R-EX-4 sections 7 and 8 (future treatment, bills to request).
347:| A-101 | The paralegal builds the chronology; the attorney reviews the letter. | R-RV-*, R-EX-1, R-EX-4 |
352:| A-106 | The export cites each line by provider as written in the header + date of service with an `[Ex. __ / Bates __]` placeholder; the tool assigns no numbers; internal notes cite provider + date, not record numbers (matches `memory/ASSUMPTIONS.md`). | R-EX-2, R-EX-4, R-EX-6 |
360:- Providers with an entry in the letter but no stated charge are "bills to request" (R-EX-4).
361:- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).
371:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
376:Already aligned, checked at this commit: `memory/ASSUMPTIONS.md` A-106 matches R-EX-4 (provider + date; record numbers appear only in the internal notes) and R-EX-6; `memory/SCOPE_CUTS.md` rows 1–19 match §5 non-goals 1–19; the golden letter block has no parenthetical on the total line.
== AI line candidates in DECISIONS.md / api.md / golden export / LLM_VS_CODE ==
app/README-arch.md:66:| `claude -p` on Chris's claude.ai login (dev only) | prompts and responses | consumer account; never in the image |
app/README-arch.md:68:A real build would add a business agreement with zero-retention terms for the model provider (while accepting that safety-flagged content may be retained by the vendor beyond zero-retention), a review of Texas HSC §181.154 notice and authorization for electronic disclosure (see `research/phi-and-ai-supervision.md`), encryption at rest, access logging on audit reads, per-user accounts and retention rules. None of that is implemented; the prototype is synthetic-only.
memory/contracts/api.md:39:  "ai_banner": "Summaries and flags are drafted by AI and checked by code; you decide every item",
memory/contracts/api.md:414:Guarantees (tested): every entry and charge line in `letter_text` is followed by `Source [Ex. __ / Bates __]:` and its verbatim excerpt, with the provider as written and a long date; the total line is exactly `Billed charges stated in these records: $X.XX` for the accepted charges and nothing else; no record numbers, flag text, counts, AI statement or "edited" mark appear in `letter_text`; the same accepted set gives byte-identical output; `counts` is outside both blo
docs/LLM_VS_CODE.md:1:# Where the AI works and where plain code works
docs/LLM_VS_CODE.md:103:- **AI use is disclosed** on the review screen (a banner: summaries and flags are drafted by AI and checked by code, and she decides every item) and in the first line of the internal notes: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." It is not in the letter; whether a firm discloses there is the firm's decision.
memory/DECISIONS.md:203:  - Letter: entries as `<Month D, YYYY> — <provider as written>`, summary, then `Source [Ex. __ / Bates __]: "<verbatim excerpt>"`; `BILLED CHARGES` with `<provider as written>, <long date>: $X.XX` plus its source line; **the total line is exactly `Billed charges stated in these records: $X.XX`** where X is the sum of accepted charges (D-019). No parenthetical, no "excludes" clause, no dot leaders, no rate, no record numbers, no flag text, no counts, no "edited" mark, n
memory/DECISIONS.md:204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); includes "flagged language quoted in the letter" (D-012), "future treatment recommended (no cost stated)" (a code pattern on "recommend"), bills to request, records not in the treatment section, edited items with origi
memory/DECISIONS.md:207:  - UI disclosure (D-009): `/api/health` returns `ai_banner` ("Summaries and flags are drafted by AI and checked by code; you decide every item"), shown on the review view, and each entry carries `ai_drafted: true`.
memory/DECISIONS.md:209:- Alternatives considered: one blended document; short citations with an optional quote (fails ship bar 1); a parenthetical on the total built from non-charge amounts (leaks unaccepted and injected items into the carrier letter, privacy r2 N1); AI disclosure in the letter text (a firm decision, recorded for ASSUMPTIONS).
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:07.867Z

**tool call — Bash**
````
{
 "command": "echo \"== api.md export section ==\"; grep -n \"export\" memory/contracts/api.md | cut -c1-200 | head -30; echo; sed -n '265,285p' memory/contracts/api.md | cut -c1-900",
 "description": "Read api.md export endpoint section and example"
}
````

### User / tool · 2026-11-02T01:05:07.956Z

**tool result**
````
== api.md export section ==
11:- `warnings[]` appears on case, ingest, review and export responses. Shape: `{"code": "...", "message": "...", "item_id": null}`.
26:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items |
192:    "ready_to_export": false },
197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sam
261:              "queue": ["a3", "e4", "e2", "a1"], "ready_to_export": false },
266:## GET /api/cases/{token}/export
267:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.expo
272:  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled


## GET /api/cases/{token}/export
Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
```json
{
  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA",
  "generated_at": "2026-11-02T01:20:00Z",
  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges stated in these records: $8,390.00",
  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
  "items": {
    "entries": [
      {
        "id": "e1",
        "record_ids": [
          "r1"
        ],
        "edited": false,
        "excerpt": "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."
      },
      {
        "id": "e2",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:10.797Z

**tool call — Bash**
````
{
 "command": "grep -n \"LETTER_TEXT\\|INTERNAL_NOTES_TEXT\\|Billed charges\\|AI assistance\\|Pending items\\|Items not reviewed\" evals/golden/sample.export.expected.txt; echo \"== pytest referencing export golden ==\"; grep -rln \"sample.export.expected\" tests/ app/ tools/ 2>/dev/null; ls tests 2>/dev/null; echo \"== REQUIREMENTS section 6 export format markers ==\"; grep -n \"^## \\|^### \" spec/REQUIREMENTS.md | head -40",
 "description": "Check golden export blocks, total line, and pytest references"
}
````

### User / tool · 2026-11-02T01:05:10.901Z

**tool result**
````
1:=== LETTER_TEXT (block 1: paste into letter) ===
47:Billed charges stated in these records: $8,390.00
48:=== INTERNAL_NOTES_TEXT (block 2: do not send) ===
51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
== pytest referencing export golden ==
e2e
fixtures
unit
== REQUIREMENTS section 6 export format markers ==
30:## 1. Must-haves
32:### 1.1 Input
42:### 1.2 Timeline
59:### 1.3 Review flags
74:### 1.4 Billed charges
86:### 1.5 Review step
113:### 1.6 Export
131:## 2. Constraints
147:## 3. Part 1 submission items
159:## 4. Stretch pick: side-by-side source viewer
187:## 5. Non-goals
213:## 6. Export template and worked example (R-EX-6)
319:## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)
337:## 8. Assumptions and the hand-off list
339:### Assumptions this depends on
362:### Reconciliation status
377:## 9. Traceability pointers
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:13.668Z

**tool call — Bash**
````
{
 "command": "sed -n '122p' spec/REQUIREMENTS.md | fold -w 300 | head -20; echo \"== spec lines 213-318 AI / Pending / Items not reviewed ==\"; sed -n '213,318p' spec/REQUIREMENTS.md | grep -n -i \"AI \\|AI:\\|pending items\\|not reviewed\\|drafted\" | cut -c1-400; echo \"== exact string check ==\"; grep -c \"AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.\" spec/REQUIREMENTS.md; grep -c \"This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed\" memory/DECISIONS.md docs/LLM_VS_CODE.md evals/golden/sample.export.expected.txt spec/REQUIREMENTS.md",
 "description": "Compare AI disclosure line across spec and DECISIONS by exact text"
}
````

### User / tool · 2026-11-02T01:05:13.786Z

**tool result**
````
| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "AI assistance: this chronology was drafted with AI assistance and every item was revi
ewed by the paralegal before export." followed by "Pending items: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evid
ence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, wit
h excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first 
appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pe
nding items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sen
tence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "requ
est itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive patter
n `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
== spec lines 213-318 AI / Pending / Items not reviewed ==
61:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
99:PENDING ITEMS NOT INCLUDED
== exact string check ==
1
docs/LLM_VS_CODE.md:1
evals/golden/sample.export.expected.txt:1
memory/DECISIONS.md:1
spec/REQUIREMENTS.md:1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:21.356Z

**tool call — Bash**
````
{
 "command": "for f in memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md; do echo \"== $f: distinct D-ids cited ==\"; grep -oE \"D-0[0-9]{2}\" \"$f\" | sort -u | tr '\\n' ' '; echo; echo \"   max: $(grep -oE 'D-0[0-9]{2}' \"$f\" | sort -u | tail -1)  count-lines-with-D-ids: $(grep -cE 'D-0[0-9]{2}' \"$f\")\"; done; echo \"== D-ids cited in these docs but NOT defined in ORCHESTRATOR_DECISIONS ==\"; .venv/bin/python -I -c \"\nimport re\ndefined=set(re.findall(r'^\\| (D-0\\d{2}) \\|', open('memory/ORCHESTRATOR_DECISIONS.md',encoding='utf-8').read(), re.M))\ncited=set()\nfor f in ['memory/DECISIONS.md','memory/contracts/api.md','docs/LLM_VS_CODE.md','app/README-arch.md']:\n    cited|=set(re.findall(r'D-0\\d{2}', open(f,encoding='utf-8').read()))\nprint('defined:', len(defined), 'min', min(defined), 'max', max(defined))\nprint('cited but undefined:', sorted(cited-defined))\n\"",
 "description": "Check D-id citations across docs against ORCHESTRATOR_DECISIONS"
}
````

### User / tool · 2026-11-02T01:05:21.540Z

**tool result**
````
== memory/DECISIONS.md: distinct D-ids cited ==
D-001 D-002 D-003 D-004 D-005 D-006 D-007 D-008 D-009 D-010 D-011 D-012 D-013 D-014 D-015 D-017 D-018 D-019 D-020 D-021 D-022 D-024 
   max: D-024  count-lines-with-D-ids: 50
== memory/contracts/api.md: distinct D-ids cited ==
D-001 D-003 D-010 D-012 D-013 D-020 D-022 D-024 
   max: D-024  count-lines-with-D-ids: 7
== docs/LLM_VS_CODE.md: distinct D-ids cited ==
D-001 D-024 
   max: D-024  count-lines-with-D-ids: 1
== app/README-arch.md: distinct D-ids cited ==
D-011 D-020 
   max: D-020  count-lines-with-D-ids: 1
== D-ids cited in these docs but NOT defined in ORCHESTRATOR_DECISIONS ==
defined: 24 min D-001 max D-024
cited but undefined: []
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:26.748Z

**tool call — Bash**
````
{
 "command": "sed -n '362,376p' spec/REQUIREMENTS.md | cut -c1-900; echo \"== R-TL-10 ==\"; grep -n \"R-TL-10\" spec/REQUIREMENTS.md | cut -c1-900; echo \"== LLM_VS_CODE D-024 / D-001 context ==\"; grep -n \"D-024\\|D-001\" docs/LLM_VS_CODE.md | cut -c1-300",
 "description": "Read spec reconciliation rows and R-TL-10 for qualifier code"
}
````

### User / tool · 2026-11-02T01:05:26.849Z

**tool result**
````
### Reconciliation status

Everything above follows `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-024). **Authority rule:** `evals/golden/*` is the authority on expected outputs, and this file matches it. §6 block 2 equals the golden `INTERNAL_NOTES_TEXT` block and §6 block 1 equals `LETTER_TEXT`; the writer asks qa for no golden changes. `memory/contracts/api.md` and `memory/DECISIONS.md` are the authority for the API and are aligned to this file and the golden by the architect on **T-028**. Each row has a grep that shows the difference.

| # | File | Difference | Check | Owner |
|---|---|---|---|---|
| 1 | `memory/contracts/api.md` export example | `internal_notes_text` should equal the golden notes block (§6 block 2). | `diff` of the example against `evals/golden/sample.export.expected.txt` (expect none) | T-028 (architect) |
| 2 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)); `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out", D-021 limits it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS_QUALIFIER" memory/contracts/api.md` (expect 1 or more) | T-028 (architect) |
| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
| 5 | `.claude/agents/paralegal-reviewer.md` | `scores.verify_quickly` (D-015) is not in the paralegal brief. | `grep -c "verify_quickly" .claude/agents/paralegal-reviewer.md` (expect 1 or more) | T-016 (orchestrator) |
| 6 | `docs/CONTRACT.md` §5 M2 | "qa injects 20"; closed as permanent. The ship bar here is a rate over the file and the product note quotes the rate. CONTRACT is never edited. | none | closed |

Already aligned, checked at this commit: `memory/ASSUMPTIONS.md` A-106 matches R-EX-4 (provider + date; record numbers appear only in the internal notes) and R-EX-6; `memory/SCOPE_CUTS.md` rows 1–19 match §5 non-goals 1–19; the golden letter block has no parenthetical on the total line.

== R-TL-10 ==
57:| R-TL-10 | **Summaries keep the numbers and the qualifiers (D-006, D-022).** (a) A number, date, dollar figure or the word left, right, no, not or without in a summary must appear in the item's excerpt, the record's source label or its parsed date (token set: ADR-012 `grounding.new_tokens`) (so "visit 8" and a heading year don't trip it), or the entry is `needs_review` (`SUMMARY_TOKEN_NOT_IN_EXCERPT`). (b) If the excerpt contains a qualifier (a hedge, a self-report marker, a negation such as "without loss of consciousness", laterality, "approx.") and the **summary** omits it, the entry is `needs_review` (`SUMMARY_DROPS_QUALIFIER`). Both are code checks and don't rely on the judge. | UT: summary "pain 4/10" with excerpt "Pain 3/10." → `needs_review` (a). Summary "Diagnosed with concussion" for entry 2 → `needs_review` (b, drops "without loss of consciousness"). Sample entries pass
328:| 4 | **No invented facts** | 0 unsupported statements across 3 repeated runs on the sample case (judge + grounding). Judge recall on seeded hallucinations ≥ 95% of every item in `hallucinations.jsonl` (today 34, so at least 33). CONTRACT §5 M2 still says "qa injects 20"; the rate governs permanently and the product note quotes the rate. | `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run`, golden `must_not` | `python -m evals.run` | R-TL-4, R-TL-10, R-CH-2, R-CH-7, R-CO-3, R-CO-7 |
369:| 2 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)); `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out", D-021 limits it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS_QUALIFIER" memory/contracts/api.md` (expect 1 or more) | T-028 (architect) |
371:| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
== LLM_VS_CODE D-024 / D-001 context ==
3:*Treatment Timeline prototype. For the hiring panel, reviewers and the developers who maintain it. Decisions behind this page: `memory/DECISIONS.md` ADR-003, 004, 005, 008, 010 to 016; cross-cutting decisions D-001 to D-024 in `memory/ORCHESTRATOR_DECISIONS.md`. Requirements it serves: `spec/REQUI
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:42.042Z

**tool call — Bash**
````
{
 "command": "grep -n \"open(\\|write\\|__main__\\|argv\\|def main\\|14\\|17\" evals/golden/check_golden.py | head -40; echo \"== head ==\"; head -30 evals/golden/check_golden.py",
 "description": "Inspect check_golden.py for I/O and entry points"
}
````

### User / tool · 2026-11-02T01:05:42.130Z

**tool result**
````
8:  * entries: provider == the header source label of the lowest-numbered cited record, exactly as written (D-014, R-TL-9;
234:            err(cid, f"{e['id']}: provider_aliases are not allowed (D-014); provider is the header label")
424:    ("wrong gap dates do not match G1", [cand("gap", [(6, "x"), (7, "y")], from_date="2026-02-20", to_date="2026-03-06", days=14)], set()),
585:                errs.append(f"export notes: {f['id']} bullet computes a delay (D-017)")
== head ==
#!/usr/bin/env python3
"""Deterministic self-check of the golden set (no LLM, no network).

Run:  python3 evals/golden/check_golden.py        (exit 0 = golden set is internally consistent)

Verifies, for every <case>.expected.json:
  * the .txt starts with "SYNTHETIC" and parses into the records the JSON declares (raw date, kind, source);
  * entries: provider == the header source label of the lowest-numbered cited record, exactly as written (D-014, R-TL-9;
    no aliases); must_contain_excerpt (string or list) verbatim in the cited records; required_terms supported by the record;
  * seeded_edits (R-RV-3): an edit expected to go to needs_review really introduces a number absent from the excerpt,
    source label and parsed date; the control edit introduces none;
  * gap_table equals real calendar arithmetic over the parsed dates of *clinical-encounter* records only
    (billing statements, phone notes and ambiguous dates are excluded) and flag == (days > 30);
  * gap flags match flagged gap rows; totals equal the sum of in_total charges; all evidence is verbatim;
  * every must_not has >= 3 bad_examples and >= 3 good_examples; for regex / structural checks BOTH sets are TESTED
    (every bad example must fire, every good example must not); judge examples are counted and checked for overlap
    (the eval runner uses them to calibrate judge #1);
  * every regex must_not does not fire on the case input itself (unless input_exempt), nor on totals.display text;
  * the 10 stress types required by CONTRACT s5 M1 are covered by the synthetic cases;
  * sample.export.expected.txt: every quote is verbatim in the record it is cited to; headings equal the record header label +
    date; summaries satisfy required_terms (summary alone) and keep self-report attribution; numbers in summaries come from the
    excerpt/label/date; the total line is exactly totals.letter_line (D-019); no regex must_not fires on the letter; the
    "flagged language" and "bills to request" sections are re-derived from sample.expected.json and must match; every must flag's
    evidence appears in the notes;
  * flag-matching reference fixtures (overlapping evidence + one-to-one assignment; K4 vs K5);
  * hallucinations.jsonl / hallucinations_controls.jsonl: counts, labels, category coverage, verbatim record_text,
    >= 10 items from synthetic cases, >= 5 paraphrase controls with token overlap < 0.8.
This checks the *golden files*, not the product. The product runner (evals/run.py) consumes them.

Regex semantics (shared with the runner): text is first stripped of double-quoted spans (verbatim excerpts); each match of
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:46.596Z

**tool call — Bash**
````
{
 "command": "python3 evals/golden/check_golden.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_golden.out 2>&1; echo \"EXIT=$?\"; SCR=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; wc -l \"$SCR/check_golden.out\"; tail -40 \"$SCR/check_golden.out\"; echo \"== grep blocks/offsets lines ==\"; grep -n -i \"block\\|offset\" \"$SCR/check_golden.out\" | head -20",
 "description": "Run golden set self-check script and capture output"
}
````

### User / tool · 2026-11-02T01:05:46.736Z

**tool result**
````
EXIT=0
       1 /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_golden.out
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
== grep blocks/offsets lines ==
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:49.850Z

**tool call — Bash**
````
{
 "command": "grep -rn \"14/14\\|17/17\" memory/ docs/ app/ evals/ tools/ 2>/dev/null | cut -c1-200; echo \"== api.md 84-92 ==\"; sed -n '84,92p' memory/contracts/api.md | cut -c1-700",
 "description": "Search for 14/14 and 17/17 check evidence and view api.md sentence offsets"
}
````

### User / tool · 2026-11-02T01:05:49.939Z

**tool result**
````
== api.md 84-92 ==
{
  "token": "k3Jf9xQ2mP7vLw0aZ8tYhA", "name": "Rivera sample", "status": "ready", "demo_mode": true,
  "backend": "fixture", "models": {"generator": "claude-sonnet-5-5", "judge": "claude-haiku-5-5"},
  "records": [
    { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
      "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
      "sentences": [ {"text": "Dx: cervical strain;", "start": 396, "end": 416}, {"text": "concussion without loss of consciousness.", "start": 417, "end": 458}, {"text": "CT head negative.", "start": 459, "end": 476},
                     {"text": "Rx cyclobenzaprine 10 mg.", "start": 477, "end": 502}, {"text": "Follow up with PCP in 1 week.", "start": 503, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
  "undated_entries": [],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:05:53.496Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nt=open('evals/golden/sample.txt',encoding='utf-8').read()\ni=t.find('=== Record 2 ===')\nprint('record2 header idx in sample.txt:', i)\nrec_start=315\n# check whether sample offsets are absolute in sample.txt\nprint('char at 315:', repr(t[315:330]))\nprint('sample[396:416]', repr(t[396:416]))\nprint('sample[477:502]', repr(t[477:502]))\nprint('sample[503:532]', repr(t[503:532]))\nprint('sample[533:552]', repr(t[533:552]))\n\" ; echo \"== sample.txt first 420 chars ==\" ; .venv/bin/python -I -c \"\nt=open('evals/golden/sample.txt',encoding='utf-8').read()\nprint(repr(t[:600]))\nprint('len', len(t))\n\"",
 "description": "Verify api.md sentence offsets against golden sample text"
}
````

### User / tool · 2026-11-02T01:05:53.623Z

**tool result**
````
record2 header idx in sample.txt: 315
char at 315: '=== Record 2 =='
sample[396:416] 'Dx: cervical strain;'
sample[477:502] 'Rx cyclobenzaprine 10 mg.'
sample[503:532] 'Follow up with PCP in 1 week.'
sample[533:552] 'ER charges: $6,240.'
== sample.txt first 420 chars ==
'SYNTHETIC — Appendix A sample records (fictional case: Jordan Rivera, 41, Austin); not real patient data\n\n=== Record 1 ===\nDate: 2026-01-09\nSource: Austin EMS run report\nExcerpt: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER."\n\n=== Record 2 ===\nDate: 2026-01-09\nSource: Central ER discharge summary\nExcerpt: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240."\n\n=== Record 3 ===\nDate: 2026-01-16\nSource: Dr.'
len 1879
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:11.164Z

**tool call — Bash**
````
{
 "command": "ls app/ 2>&1; ls app/backend app/llm 2>&1 | head; echo \"== tests ==\"; ls tests/unit tests/e2e 2>&1 | head -30; echo \"== LLM_VS_CODE table rows (first col and LLM/code) ==\"; grep -n \"^| [0-9]* |\" docs/LLM_VS_CODE.md | cut -c1-180",
 "description": "Check app and tests layout and LLM_VS_CODE table rows"
}
````

### User / tool · 2026-11-02T01:06:11.257Z

**tool result**
````
README-arch.md
backend
db
frontend
llm
app/backend:

app/llm:
lexicon.yaml
prompts
== tests ==
tests/e2e:

tests/unit:
== LLM_VS_CODE table rows (first col and LLM/code) ==
29:| 1 | Split pasted text into records; merge exact duplicates | **Code**: `=== Record N ===` markers, dates, source labels, table rows, a `---` separator. Same date + provider + 
30:| 2 | Parse dates | **Code**: an explicit list of formats. `04/05/2026` fits two readings (April 5 or May 4): it is **ambiguous**, never guessed, and waits for the paralegal. | 
31:| 3 | Date of service and provider for an entry | **Code**: the record's own header date, and the record's `Source:` label exactly as written as the provider ("Capital PT, initi
32:| 4 | Per-record extraction: one-line summary and exact excerpt (a run of whole sentences) | **LLM (generator)**, structured output `{summary, excerpt}`, temperature 0 where the
33:| 5 | Clinical facts as a separate list | **Not built.** The summary and the verbatim excerpt carry the facts. | Every extra paraphrased field is another place to invent medical
34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses a
35:| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable
36:| 8 | Running total of charges | **Code**: sum of **accepted** amounts of class `charge`. The screen also shows "Pending review" separately and a "detected, not a total" figure.
37:| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes ar
38:| 10 | Conflicts that are structural: stated accident date later than the earliest treatment; two different stated accident dates; the same provider spelled two ways | **Code**:
39:| 11 | Conflicts that need meaning: a plan of 12 visits versus discharge at visit 9 | **LLM** proposes a pair as a category and two quoted spans, nothing else | Needs reading co
40:| 12 | Pre-existing conditions (flag type `pre_existing`) | **LLM** runs once **per record** and proposes a category and a quote; **and** a researched phrase list is scanned by 
41:| 13 | Language that weakens causation ("may represent degenerative change", "patient states", missed appointments, "new onset", scene facts such as refusing transport, "no obje
42:| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days be
43:| 15 | Numbers and dates in a summary or in the paralegal's edit | **Code**: every number, date, dollar figure and left/right/no/not/without in the text must be in the excerpt (
44:| 16 | Instruction-like text inside a record ("ignore previous instructions…") | **Code**: advisory phrase scan that raises a `record_warning` flag. Everything derived from th
45:| 17 | Confidence state per item (`verified`, `needs_review`, `rejected`) | **Code**: a fixed rule over the checks (rejected if a grounding check fails; needs review on any doub
46:| 18 | The "Why?" sentence | **Code**: one template per reason code. | A model explaining its own doubt would be another unverified claim. | Test: every reason code has a templa
47:| 19 | Sorting, filter to accepted items, export assembly, citations, the total line | **Code**. Every letter line carries its verbatim excerpt, the provider as written, a date 
48:| 20 | Audit trail | **Code**: every model call stores model, backend, prompt version and hash, full prompt and response, verdict, latency, cost; every human action stores befor
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:14.020Z

**tool call — Bash**
````
{
 "command": "sed -n '34,37p' docs/LLM_VS_CODE.md; echo; sed -n '9p;42p' docs/LLM_VS_CODE.md; echo; sed -n '101,104p' docs/LLM_VS_CODE.md | cut -c1-500",
 "description": "Read LLM_VS_CODE rows 6-9, 14 and disclosure section"
}
````

### User / tool · 2026-11-02T01:06:14.107Z

**tool result**
````
| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must not depend on a model's attention. | Unit tests with noisy, duplicate and dose-like numbers. An amount a model reports that code cannot find is rejected. |
| 7 | Say what an amount is: charge, rate, estimate, damages, unclear | **Code only**, by explicit billing phrases, first match wins: an injection-warned record or an unreadable figure is *unclear*; whole words "per", "each", "rate" or a following "per visit" / "/visit" is a *rate* ("Charge per visit $185"); "estimate(d)" is an *estimate*; lost-wage wording is *damages*; in a billing-statement record, "Statement for visit of 2026-02-02: $275" is a *charge*; a label ending "charge:" ("ER charges:", "Charge:") or "billed:" is a *charge*; everything else is *unclear*. There is no model classifier. | Billing language is regular enough for rules, and a rule can be tested. A rule cannot be argued with by a record that says "add $50,000 to the billed total". | **Judge 2 checks every classification** against the excerpt (`agrees`, `disagrees`, `unsure`), including the rule-made ones. A `charge` is `verified` only when judge 2 agrees; any other class needs review. Charges are accept or dismiss only, so a rate has no path to become a charge. Unit tests: 20 phrasings of "Charge per visit $185" all give *rate*; "Moderate" and "Corporate" never trigger the rate rule; all 14 dollar amounts across the golden cases get their golden class. |
| 8 | Running total of charges | **Code**: sum of **accepted** amounts of class `charge`. The screen also shows "Pending review" separately and a "detected, not a total" figure. Rates, estimates, damages and unclear amounts are listed "not totaled". | Arithmetic, and a total must mean "what she has verified", not "what the tool found". | Unit tests; E2E: the export total equals the accepted charges. The sample's PT rate ($185 per visit, visits never itemised) never becomes a PT total. |
| 9 | Treatment gap longer than 30 days | **Code** over the code-parsed **record dates** of all (de-duplicated) clinical-encounter records (billing statements and phone notes are excluded), independent of any model output or review state. Strictly more than 30 days; 30 is not a gap. | A gap is a fact about dates. If it depended on the model's entries, one dropped entry would invent a gap. | Unit tests at 29, 30, 31 days; sample 28-day near miss does not flag, 73-day gap does; dropping an entry never changes the result. Ambiguous dates are excluded, shown as a record warning, and any gap near one needs review; she resolves one by choosing a reading the code proposed (`confirm_date`). |

## The rules (enforced in code and tests, not only in prompts)
| 14 | The wording of every flag | **Code**: a fixed template per flag type and category, filled with dates, source labels and the verbatim quote. For example "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)". | A model explaining a flag is another unverified claim, and the place it would be tempted to rule on causation. | The model's output schema has no prose field; a test rejects extra fields. |

- **A rejected item means a missing entry.** If a record keeps failing the quote check, she sees it in the tray and writes that entry herself outside the tool (manual add is a deliberate cut).
- **Demo mode.** The public site replays recorded model answers for the sample case through the same code. It says so in a badge and refuses other text with a clear message, and it stores nothing a visitor pastes. Live mode runs locally and must be switched on deliberately.
- **AI use is disclosed** on the review screen (a banner: summaries and flags are drafted by AI and checked by code, and she decides every item) and in the first line of the internal notes: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." It is not in the letter; whether a firm discloses there is the firm's decision.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:19.012Z

**tool call — Bash**
````
{
 "command": "grep -rn \"date_ambiguous\\|DATE_EXCLUDED_FROM_GAPS\\|f_warn_date\" evals/golden/*.json evals/golden/*.md memory/contracts/api.md memory/DECISIONS.md 2>/dev/null | cut -c1-260 | head -20; echo \"== case_01 record_warnings schema hint in README ==\"; grep -n -i \"record_warnings\" evals/golden/README.md | cut -c1-300 | head",
 "description": "Trace date_ambiguous warning representation across golden and contract"
}
````

### User / tool · 2026-11-02T01:06:19.111Z

**tool result**
````
memory/DECISIONS.md:214:- Decision: at ingest, code takes the header date of every non-duplicate **clinical-encounter** record (billing statements, ledgers, phone notes and similar are excluded by a `non_encounter` source-label lexicon, D-003; they still becom
memory/DECISIONS.md:250:  - The flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation`, `record_warning` everywhere (D-013). `record_warning` flags are created by code only (categories `date_ambiguous`, `injection_suspected`).
memory/DECISIONS.md:257:    - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
memory/contracts/api.md:62:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`. Errors: `413 input
memory/contracts/api.md:197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.) Flag `type`: `gap`
memory/contracts/api.md:204:Response 200: the record with `date_status: "confirmed"`, its entry's date, the **recomputed gap flags** (a changed or new flag keeps no review status; an unchanged record pair keeps its status), the cleared `date_ambiguous` record 
memory/contracts/api.md:209:  "removed_flag_ids": ["f_warn_date_r8"],
== case_01 record_warnings schema hint in README ==
61:  "record_warnings": [{"type":"instruction_like_text","record_no","excerpt","level","expected_state"}],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:25.556Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"cents\\|float\\|Decimal\" memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md | cut -c1-260 | head -20; echo \"== api amount example ==\"; grep -n \"\\\"amount\\|value_cents\\|\\\"cents\\|\\\"kind\\\"\" memory/contracts/api.md | cut -c1-260 | head -12",
 "description": "Check money representation (cents, Decimal) in docs and API examples"
}
````

### User / tool · 2026-11-02T01:06:25.647Z

**tool result**
````
app/README-arch.md:20:  amounts.py       currency regex (cents), billing-phrase classification, dedupe, totals (accepted / pending / detected)
docs/LLM_VS_CODE.md:34:| 6 | Find every dollar amount | **Code**: a currency pattern over every record; money as whole cents. `$1,2OO` is listed as *unclear* with no value and never corrected. Doses and pain scores are never amounts. | Recall of numbers must n
memory/contracts/api.md:6:- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
memory/contracts/api.md:115:    { "id": "a1", "record_ids": ["r2"], "entry_id": "e2", "text": "$6,240", "value_cents": 624000, "kind": "charge",
memory/contracts/api.md:124:    { "id": "a3", "record_ids": ["r4"], "entry_id": "e4", "text": "$185", "value_cents": 18500, "kind": "rate",
memory/contracts/api.md:134:    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
memory/contracts/api.md:135:    "pending": {"cents": 839000, "count": 2, "label": "Pending review"},
memory/contracts/api.md:136:    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
memory/contracts/api.md:259:  "totals": { "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"}, "pending": {"cents": 839000, "count": 2, "label": "Pending review"} },
memory/contracts/api.md:381:    "charges_cents": 839000,
memory/DECISIONS.md:84:amounts       id, case_id, record_ids_json, entry_id, text ("$6,240" verbatim), value_cents (NULL if unreadable),
memory/DECISIONS.md:103:  - Money is integer cents. An unreadable amount (OCR noise `$1,2OO`) keeps its verbatim `text`, `value_cents = NULL`, kind `unclear`; code never repairs it.
memory/DECISIONS.md:222:  - Extraction (code): a currency pattern over every record; money as cents; OCR-noisy figures (`$1,2OO`, `$9S.00`) are kept verbatim with value NULL and kind `unclear`. Non-money figures (doses, pain scores) are never amounts. Dedupe: 
== api amount example ==
6:- Base path `/api`; JSON in and out; UTF-8; ISO dates `YYYY-MM-DD`; timestamps ISO-8601 UTC. Money is integer cents in `value_cents` plus the verbatim `text`.
74:  "stages": ["ingest","extract","verify","judge_entries","amounts","conflicts","flags","finalize"],
76:  "counts": {"entries": 9, "amounts": 3, "flags": 1},
114:  "amounts": [
115:    { "id": "a1", "record_ids": ["r2"], "entry_id": "e2", "text": "$6,240", "value_cents": 624000, "kind": "charge",
121:        "code_checks": {"amount_in_text": true, "classified_by": "rule:charge_label", "injection_tag": false, "highlight_found": true},
124:    { "id": "a3", "record_ids": ["r4"], "entry_id": "e4", "text": "$185", "value_cents": 18500, "kind": "rate",
130:        "code_checks": {"amount_in_text": true, "classified_by": "rule:per_unit", "injection_tag": false, "highlight_found": true},
134:    "accepted": {"cents": 0, "count": 0, "label": "Accepted charges"},
135:    "pending": {"cents": 839000, "count": 2, "label": "Pending review"},
136:    "detected_not_a_total": {"cents": 839000, "count": 2, "label": "Detected (not a total)"},
137:    "not_totaled": [{"id": "a3", "kind": "rate", "text": "$185"}]
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:29.414Z

**tool call — Bash**
````
{
 "command": "echo \"\\$ grep -n \\\"date_invalid\\\" memory/contracts/api.md\"; grep -n \"date_invalid\" memory/contracts/api.md | cut -c1-160; echo; echo \"\\$ grep -n \\\"AI assistance\\\" memory/DECISIONS.md\"; grep -n \"AI assistance\" memory/DECISIONS.md | cut -c1-400; echo; echo \"\\$ grep -n \\\"AI assistance\\\" spec/REQUIREMENTS.md\"; grep -n -o \"AI assistance[^|]\\{0,140\\}\" spec/REQUIREMENTS.md; echo; echo \"\\$ grep -n \\\"phone\\\" memory/contracts/api.md memory/DECISIONS.md\"; grep -n -o \".\\{0,60\\}phone.\\{0,80\\}\" memory/contracts/api.md memory/DECISIONS.md | cut -c1-260",
 "description": "Run spec-mandated greps for date_invalid, AI line and phone note"
}
````

### User / tool · 2026-11-02T01:06:30.508Z

**tool result**
````
$ grep -n "date_invalid" memory/contracts/api.md
9:- Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `inp
212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_dat

$ grep -n "AI assistance" memory/DECISIONS.md
204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); includes "flagged language quoted in the letter" (D-012), "future treatment recommended (no cost stated)" (a code pattern on "recommend"),

$ grep -n "AI assistance" spec/REQUIREMENTS.md
119:AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose
122:AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export." followed by "Pending items: N.
273:AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
370:AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` 

$ grep -n "phone" memory/contracts/api.md memory/DECISIONS.md
ugrep: error: error at position 81
f][\x80-\xbf]*){0,80}
                     \___exceeds complexity limits
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:32.248Z

**tool call — Bash**
````
{
 "command": "grep -n \"phone\" memory/contracts/api.md memory/DECISIONS.md | cut -c1-240; echo \"---- ADR-010 encounter rule ----\"; grep -n \"encounter\" memory/DECISIONS.md | cut -c1-200 | head -8",
 "description": "Grep phone-note references in api.md and DECISIONS.md"
}
````

### User / tool · 2026-11-02T01:06:32.340Z

**tool result**
````
memory/DECISIONS.md:50:- Consequences: the phone reaches `https://<node>.<tailnet>:7777` and `:7860` with TLS terminated by serve (use https, not http); `docs/RUNBOOK.md` carries the URLs; Chris's own services keep working. Cost: two extra 
memory/DECISIONS.md:80:              encounter (1 = clinical encounter; 0 = billing statement, phone note and similar, D-003)
memory/DECISIONS.md:214:- Decision: at ingest, code takes the header date of every non-duplicate **clinical-encounter** record (billing statements, ledgers, phone notes and similar are excluded by a `non_encounter` source-label lexicon, D-0
memory/contracts/api.md:62:(The real response lists all 9 records; the example shows one.) `warnings[]` codes: `SPLIT_AMBIGUOUS`, `DATE_EXCLUDED_FROM_GAPS`, `PHI_PATTERN` (SSN/phone/MRN-shaped text found; does not block), `DUPLICATE_MERGED`
memory/contracts/api.md:197:(The real response lists every entry, amount and flag; the example shows representative ones. `ladder` for items not shown follows the same shape. The `tray` example is a seeded failure, not a sample-case result.
memory/contracts/api.md:212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a ph
---- ADR-010 encounter rule ----
80:              encounter (1 = clinical encounter; 0 = billing statement, phone note and similar, D-003)
214:- Decision: at ingest, code takes the header date of every non-duplicate **clinical-encounter** record (billing statements, ledgers, phone notes and similar are excluded by a `non_encounter` sourc
229:    6. **billing statement**: the record's source label matches the billing-statement entries of the `non_encounter` lexicon and the label contains `statement`, `balance`, `amount due`, `total` or
251:  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`med
303:  6. **Gap scope.** Clinical-encounter records only (D-003); R-FL-1 and R-IN-5 gain that sentence. Ambiguous-date entries appear in a "Dates to confirm" group after the timeline (`undated_entries`
308:  11. **Lexicon v2 dependency.** `lexicon.yaml` (flag_type, hedge, self_report, strength, `accident_date_phrases`, `non_encounter`, `injection`) is a researcher deliverable that blocks gaps, the a
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:36.426Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport yaml\nd=yaml.safe_load(open('app/llm/lexicon.yaml',encoding='utf-8'))\nprint('non_encounter:', d['code_lists']['non_encounter'])\nprint('accident_date_phrases keys:', list(d['code_lists']['accident_date_phrases'].keys()) if isinstance(d['code_lists']['accident_date_phrases'],dict) else d['code_lists']['accident_date_phrases'])\nprint('injection keys:', list(d['code_lists']['injection'].keys()) if isinstance(d['code_lists']['injection'],dict) else 'list')\nprint('damages keys:', list(d['code_lists']['damages'].keys()) if isinstance(d['code_lists']['damages'],dict) else 'list')\nne=d['code_lists']['non_encounter']\nprint('phone matched by non_encounter?', any('phone' in str(x).lower() for x in (ne if isinstance(ne,list) else ne.values())))\n\"; echo \"== ADR-010 block ==\"; sed -n '211,217p' memory/DECISIONS.md | cut -c1-400",
 "description": "Check non_encounter lexicon covers phone notes and read ADR-010"
}
````

### User / tool · 2026-11-02T01:06:36.597Z

**tool result**
````
non_encounter: {'applies_to': 'source_label', 'consumer': 'ADR-010 / D-003: records whose source label matches are excluded from gap arithmetic. They still become entries.', 'rationale': 'Billing statements, ledgers, phone notes, records requests and correspondence carry dates that are not dates of care. Counting them hides real gaps (golden case_09: a billing statement 27 days after a visit would break a real gap).', 'source': 'D-003; ADR-010; golden case_01 (phone note), case_09 (billing statement, phone note)', 'false_positive': 'A phone note can document clinical advice. It is still excluded from gaps (D-003) but remains an entry. "Telehealth visit" and "video visit" are encounters and are deliberately NOT listed.', 'entries': [{'id': 'billing_document', 'pattern': '\\b(?:billing\\s+statement|itemi[sz]ed\\s+(?:bill|statement|charges)|statement\\s+of\\s+account|account\\s+statement|ledger|invoice|explanation\\s+of\\s+benefits|EOB|UB-?04|HCFA|CMS-?1500|payment\\s+(?:history|record)|balance\\s+due\\s+notice)\\b'}, {'id': 'phone_or_message', 'pattern': '\\b(?:phone|telephone|tel\\.?)\\s+(?:note|call|encounter|message|contact)\\b|\\bportal\\s+message\\b|\\bvoicemail\\b|\\bmessage\\s+(?:note|log)\\b'}, {'id': 'records_admin', 'pattern': '\\b(?:records?\\s+request|request\\s+for\\s+records|medical\\s+records\\s+(?:request|certification|affidavit)|business\\s+records\\s+affidavit|custodian\\s+(?:of\\s+records\\s+)?affidavit|18\\.001\\s+affidavit|authorization\\s+form|HIPAA\\s+authorization|correspondence|cover\\s+letter|fax\\s+cover|referral\\s+(?:form|letter)|prior\\s+authori[sz]ation|no-?\\s?show\\s+(?:notice|letter))\\b'}], 'examples': {'hit': ['Hobbleton Family Clinic, billing statement', 'Gloamwood Chiropractic, billing statement', 'Dr. Orla Pennywhistle, phone note', 'Hobbleton Family Clinic, phone note', 'Austin Imaging, itemized bill', 'Capital PT, records request'], 'miss': ['Capital PT, visit 9', 'Central ER discharge summary', 'Austin EMS run report', 'Hill Country Pain Management, follow-up', 'Austin Imaging, cervical MRI', 'Dr. Lysander Quibble, telehealth visit']}}
accident_date_phrases keys: ['applies_to', 'consumer', 'rationale', 'source', 'false_positive', 'entries', 'examples']
injection keys: ['applies_to', 'consumer', 'rationale', 'source', 'false_positive', 'entries', 'examples']
damages keys: ['applies_to', 'consumer', 'rationale', 'source', 'false_positive', 'entries', 'examples']
phone matched by non_encounter? True
== ADR-010 block ==
## ADR-010 Gaps are computed by code over record dates, never over LLM entries
- Status: accepted (round 2; resolves staff-engineer F2 and F7, requirement R-FL-1, R-IN-5; D-003)
- Context: a gap is a fact about dates in the records. If it were computed over LLM entries, one rejected or failed entry would invent a false gap (r5 missing makes r4→r6 42 days; r6 missing makes 87) and it would be labelled `verified`.
- Decision: at ingest, code takes the header date of every non-duplicate **clinical-encounter** record (billing statements, ledgers, phone notes and similar are excluded by a `non_encounter` source-label lexicon, D-003; they still become entries), parses it (explicit format list, never guessed), sorts by (date, seq) and emits a gap flag for each consecutive pair more than 30 calendar days apart (3
- Consequences: dropping, rejecting or editing an LLM entry can never change gap math; unit tests (29/30/31; r5 or r6 removed) need no LLM.
- Alternatives considered: gaps over verified entries (couples a fact to model success); gaps over all entries with `ENDPOINT_NOT_VERIFIED` (still produces a wrong number).
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:40.963Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md; echo \"==========\"; cat .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md | head -60; echo \"==========\"; ls reviews/ 2>&1 | head -40",
 "description": "Read existing reviewer memory notes and list reviews directory"
}
````

### User / tool · 2026-11-02T01:06:41.055Z

**tool result**
````
---
name: design-review-patterns
description: Recurring design-level defects found reviewing the Zlayt treatment-timeline architecture (T-014 rounds 1-2); check these first on later cards
metadata:
  type: project
---

Round 1 (2026-11-01, fail): defects, all resolved in round 2 but re-check them in M2 code reviews.
- Flag/gap logic keyed on LLM entries instead of code-parsed record dates (r5 dropped -> false 42-day gap). In M2 test that gaps use `records.date_iso`.
- Export default omitted verbatim excerpt (cite=short) vs ship bar 1 / R-EX-2.
- Judge #2 skipped on code-classified amounts; summary numerals not code-checked; retry count wording inconsistent.
- Illustrative JSON in api.md had wrong offsets and a `{...}` block. Re-run `artifacts/review-evidence/T-014-json-check.py` and `T-014-r2-offset-check.py` after any api.md edit.

Round 2 (changes, 4 majors) - new pattern: the architect's docs drift from REQUIREMENTS revision N because writer and architect edit in parallel.
- Export format restated in ADR-009, api.md and the golden file differ from REQUIREMENTS sec 6 (dot leaders, Source line, total-line parenthetical). Check byte-equality test target first.
- ADR-011 amount rules: simulate them on all `evals/golden/*.txt` (`T-014-r2-amount-sim.py`); case_09 `$275` billing-statement amount fell to `unclear`. Charges are accept/dismiss only, so a missed rule is unrecoverable for the user.
- Anything that calls a judge at request time (edit re-check) needs a stated judge-failure / FixtureMiss path; demo mode makes every edit a fixture miss.
- ADR-016 over-applied D-012 (forced inclusion of lexicon sentences; `mg.` abbreviation) vs R-TL-8 hedge-only.
- D-018 landed after the architect started; always check the newest D-xx against ADR category lists.

**Why:** these made T-014 fail round 1 (2026-11-01) and require changes in round 2.
**How to apply:** on M2 backend review, run the golden amount simulation against the real `amounts.py`, check export equals golden file, and grep for a defined judge-unavailable path.

Round 3 (2026-11-01, changes, 5 majors): same parallel-edit drift, now against lexicon v2, D-021/D-022 and the golden file.
- Check ADR category lists against the real `app/llm/lexicon.yaml` category values (6 lexicon categories were missing from ADR-013; P1 floor flag had no template).
- A binding D-xx can land during the architect's round (D-022 SUMMARY_DROPS_QUALIFIER was missed); grep new reason codes in api.md appendix.
- Embedded copies of files others own (api.md export vs golden) drift within the hour; recommend pointer + test, not a copy. Working tree can hold other agents' uncommitted edits: compare with `git show <rev>:path`.
- api.md examples that claim golden provenance: verify against the golden `gap_excluded_records` (confirm_date example put a phone note into gap math).
- Cut-line items can silently undo a structural control (per-record flag pass): read the cut line against ADR-008.
- Evidence: `artifacts/review-evidence/T-014-r3-amount-sim.py` / `-amount-demo.py` (real lexicon, ADR-011 r3 rules; 14/14 dollar amounts).
==========
---
name: harness-review-patterns
description: Recurring defects in the board CLI / board server / hook guards seen in M0 reviews (rounds 1-2), plus reviewer-environment gotchas
metadata:
  type: project
---

Recurring patterns (M0 round 2, HEAD f413e84):
- Hook guards are token/regex denylists: `board_guard.py` treats ANY token ending in `board.py` as an invocation (false-positives on `test_board.py`, `git diff -- tools/board.py x`); evaded by `bash -c`, `sh -c`, `eval`, globs, `python -c`. Always probe wrappers.
- Hook entry scripts `exec python3`; on system Python 3.9 the `X | None` annotations crash at import (outside try) -> rc 1 -> fail-open. Check `.claude/hooks/*.py` for `from __future__ import annotations` and import-time errors.
- Fixes tend to cover the implemented attack and skip the sibling (CSRF fixed via Origin==Host but no Host allowlist -> DNS rebinding passes). Test the round-1 acceptance line literally.
- Tests mirror the implementation (no Host test, no agent-sync test, no wrong-card/persona test). Agent files drifted from dossiers once between commits; no test.
- Free-text note markers (`assigned:`) used as machine state can be forged by any `note`.

Round 3 (e3fbb08) additions:
- board_guard checks `ba[2] == "done"` positionally; `move T-1 --agent x done` (valid argparse) bypasses it. Always probe flag order, not just wrappers.
- Sentinel-in-review-list pattern (`orchestrator-§7.4` debt entry) short-circuits `_reviews_pass` forever; test "accept -> reopen -> later fail" for any bypass flag.
- Reviewer-guard false positives: `git tag -l`, `branch --show-current`, `stash list`, `reflog`, `chmod +x`; Write tool denies scratchpad while Bash allows it.
- Working tree gets uncommitted orchestrator edits mid-review (D-024); say which tree was tested.
- D-023 threat model (memory/ORCHESTRATOR_DECISIONS.md): plausible accidental spelling = finding; deliberate obfuscation = residual/nit.

**Why:** these recurred across T-001/T-002/T-004 round 1 and 2.
**How to apply:** when re-reviewing harness code, re-run each round-1 acceptance test verbatim, then try the wrapper/sibling variant.

Reviewer-environment gotchas:
- As a native `*-reviewer`, board-guard denies all non-read-only `board.py` subcommands even with a temp BOARD_ROOT; write-path repros cannot be run by reviewers (do not route around with python wrappers; ask the orchestrator). Read-only (`validate/show/list/status/next/inbox`) work with BOARD_ROOT set.
- Bash redirects are checked against the initial cwd and unexpanded `$VAR` paths: use literal absolute scratchpad paths, or put the work in a script file in the scratchpad. `... | tee path` followed by another command on the next line was also falsely denied.
- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.
- A chained shell mutation check in a scratch copy (`rm -rf` + `rsync` + `sed -i` + regenerate) was denied by the permission guard on T-016 (2026-11-01). Do not split the chain to get around it; reason from code and label the finding "not reproduced".
- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).
==========
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:06:46.719Z

**tool call — Bash**
````
{
 "command": "ls artifacts/review-evidence/ 2>&1 | head -30; echo \"== T-014 r3 review head ==\"; sed -n '1,25p' reviews/T-014-staff-engineer-r3.md | cut -c1-300; echo \"== last JSON block of T-014 r3 ==\"; awk '/```json/{f=1} f' reviews/T-014-staff-engineer-r3.md | head -12 | cut -c1-300",
 "description": "List review evidence scripts and view prior review format"
}
````

### User / tool · 2026-11-02T01:06:46.816Z

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
== T-014 r3 review head ==
# Review T-014 round 3 (staff-engineer-reviewer): ADRs, LLM_VS_CODE.md, API contract

Verdict: **changes** (0 blockers, 5 majors, 4 minors, 1 nit). Of the 10 staff r2 findings, 7 are fully resolved, 3 are partly resolved (each leaves one of the new majors below). Of the privacy r2 findings, the blocker (N1) and the demo-storage major (N2) are resolved; N3 is mostly resolved with two 

What I re-ran (details in the JSON): the 14 api.md JSON blocks parse; 19 of 19 `raw[start:end]` offsets equal their quotes on `evals/golden/sample.txt`; the ADR-011 rules, applied literally with the real lexicon v2, classify all 14 golden dollar amounts as the golden file expects (including case_09 

What is left is drift between the architect's text and artifacts that moved in parallel (lexicon v2, D-021, D-022, the golden file, REQUIREMENTS at 2e92535). Each fix is small, but each one would make a backend worker build the wrong thing, so they stay majors.

## Majors
- **M1 D-022 is not in the design.** `SUMMARY_DROPS_QUALIFIER` and per-sentence `source_kind` appear in no ADR, no LLM_VS_CODE row, no reason code (`grep -c SUMMARY_DROPS_QUALIFIER` on api.md, DECISIONS.md, LLM_VS_CODE.md = 0, 0, 0). The writer's REQUIREMENTS section 8 row 5 lists it as an open T-01
- **M2 ADR-013's closed category list does not match lexicon v2.** The lexicon uses `prior_surgery`, `alternative_cause`, `objective_negative`, `litigation_referral`, `recovery_context`, `accident_date_provenance` (none in ADR-013; 0 mentions in the three architect docs) and not `no_objective_findin
- **M3 The `confirm_date` example puts a phone note into gap math.** api.md:206-210 recomputes `f_gap_r7_r8` (40 days) after confirming record 8 of case_01. Record 8 is a phone note; D-003, ADR-010 and golden case_01 (`gap_excluded_records: [8]`) exclude it. The example claims its numbers "come from
- **M4 `mg.` abbreviation.** ADR-016 says `mg.` is not an abbreviation and api.md:90-91 splits "Rx cyclobenzaprine 10 mg." from "Follow up with PCP in 1 week."; D-021 (binding) says the splitter keeps `mg.` intact, and R-TL-2 at HEAD lists it.
- **M5 Cut line undoes the injection control.** README-arch.md:82 lists "the per-record flag pass folded into one pass" as a cut. D-021 and ADR-008.3 make the per-record pass the structural control against one record suppressing another's flags.

## Minors and nit
m1 the api.md export example is a second copy of the golden file and already differs from it at HEAD; m2 `422 date_invalid` (R-RV-2) vs `invalid_edit` (api.md); m3 "golden variant E" is cited as evidence but does not exist and no card owns it; m4 normalisation says "trimmed" in api.md and ADR-006 bu

## Buildability in about 7 hours
Plausible with the ordered cut line, once M5 is fixed. Cuts taken in round 3 (limiter, ledger, arbitrary-text ingest, LLM classifier) remove the least valuable code. Remaining weight: 17 backend modules, 7 prompts, about 40 calls per case, fixtures to record for every golden case the demo accepts (a

## What I would not change
Gaps from code-parsed record dates; code-only amount classification with a judge on every class; the total line fixed by D-019; the edit re-check order with an explicit judge-unavailable state.

```json
== last JSON block of T-014 r3 ==
```json
{
  "card": "T-014",
  "persona": "staff-engineer-reviewer",
  "model": "claude-sonnet-5-5",
  "scope": "Round 3. git diff e442626..388d5b2 (memory/DECISIONS.md ADR-002..017, docs/LLM_VS_CODE.md, memory/contracts/api.md, app/README-arch.md), read at HEAD 8106024 (those four files unchanged since 388d5b2; spec/REQUIREMENTS.md and evals/golden updated at 2e92535/f8c1948 and compared); against
  "exercised": [
    "python3 tools/board.py show T-014 (AC and round-3 handoff read; claims not trusted)",
    "read reviews/T-014-staff-engineer-r2.md and reviews/T-014-privacy-compliance-r2.md in full",
    "read memory/DECISIONS.md lines 1-307, docs/LLM_VS_CODE.md, memory/contracts/api.md (453 lines), app/README-arch.md, memory/ORCHESTRATOR_DECISIONS.md D-001..D-023, REQUIREMENTS R-TL-2/R-TL-8/R-EX-8/R-RV-2 and section 8 at HEAD",
    "python3 -I artifacts/review-evidence/T-014-json-check.py: total 14 blocks, 0 fail",
    "python3 -I artifacts/review-evidence/T-014-r2-offset-check.py: chars 1879, 19 19 (all offsets equal quoted strings)",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:11.308Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-028 mechanical checks (staff-engineer-reviewer). Read-only; no network.\n\nRun from repo root:  .venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py\nPrints one PASS/FAIL line per check with the evidence it compared.\n\"\"\"\nimport re\nimport sys\nfrom pathlib import Path\n\nimport yaml\n\nROOT = Path(__file__).resolve().parents[2]\nresults = []\n\n\ndef check(name, ok, evidence):\n    results.append(ok)\n    print((\"PASS \" if ok else \"FAIL \") + name)\n    for line in evidence:\n        print(\"    \" + line)\n\n\ndef read(rel):\n    return (ROOT / rel).read_text(encoding=\"utf-8\")\n\n\n# 1. SUMMARY_DROPS_QUALIFIER presence (AC1)\ncounts = {f: read(f).count(\"SUMMARY_DROPS_QUALIFIER\")\n          for f in [\"memory/contracts/api.md\", \"memory/DECISIONS.md\", \"docs/LLM_VS_CODE.md\"]}\ncheck(\"AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md\",\n      all(v >= 1 for v in counts.values()), [f\"{k}: {v}\" for k, v in counts.items()])\n\n# 2. Lexicon v2 categories all named in ADR-013 (AC2, names only)\nlex = yaml.safe_load(read(\"app/llm/lexicon.yaml\"))\nlex_cats = sorted({e[\"category\"] for e in lex[\"entries\"]})\ndec = read(\"memory/DECISIONS.md\")\nm = re.search(r\"^## ADR-013.*?(?=^## ADR-014)\", dec, re.S | re.M)\nadr13 = m.group(0) if m else \"\"\nmissing = [c for c in lex_cats if not re.search(r\"\\b\" + re.escape(c) + r\"\\b\", adr13)]\ncheck(\"AC2 every lexicon v2 category name appears in ADR-013\",\n      bool(adr13) and not missing,\n      [f\"lexicon categories ({len(lex_cats)}): {lex_cats}\", f\"missing from ADR-013: {missing}\"])\n\n# 2b. Per-category flag template text in ADR-013 (AC2 'with a template')\ntmpl_mentions = {c: len(re.findall(r\"template\", adr13)) for c in lex_cats[:1]}\ncheck(\"AC2 each category has a flag template stated in ADR-013\",\n      False,\n      [\"ADR-013 contains the word 'template' %d times and one example wording; no per-category template text\"\n       % len(re.findall(r\"template\", adr13)),\n       \"app/backend/flag_templates.py exists: %s\" % (ROOT / \"app/backend/flag_templates.py\").exists()])\n\n# 3. Phone note (record 8) not in gap math in the confirm_date example (AC3a)\napi = read(\"memory/contracts/api.md\")\nsect = re.search(r\"^## POST /api/cases/\\{token\\}/records/\\{rid\\}/confirm_date.*?(?=^## )\", api, re.S | re.M)\nsect = sect.group(0) if sect else \"\"\ngap_empty = '\"gap_flags\": []' in sect\ngolden = yaml.safe_load(open(ROOT / \"evals/golden/case_01_date_formats.expected.json\", encoding=\"utf-8\")) \\\n    if False else None\ncheck(\"AC3a confirm_date example gap_flags empty for phone note r8\",\n      gap_empty and \"encounter\\\": false\" not in sect,\n      ['api.md confirm_date example contains \"gap_flags\": [] : %s' % gap_empty])\n\n# 4. date_invalid only non-candidate code (AC3b)\nnoncand = [l for l in api.splitlines() if re.search(r\"non-candidate|not one of the record\", l)]\ncheck(\"AC3b date_invalid is the only code for a non-candidate date\",\n      all(\"date_invalid\" in l for l in noncand) and len(noncand) >= 1,\n      [\"lines naming non-candidate dates: %d\" % len(noncand)] + [l[:160] for l in noncand])\n\n# 5. mg. treated as abbreviation: apply R-TL-2 splitter to sample record 2 and compare api.md units\nsample = read(\"evals/golden/sample.txt\")\nhdr = sample.index(\"=== Record 2 ===\")\nq0 = sample.index('Excerpt: \"', hdr) + len('Excerpt: \"')\nq1 = sample.index('\"', q0)\nbody = sample[q0:q1]\nABBR = {\"approx\", \"Dr\", \"Mr\", \"Mrs\", \"Ms\", \"vs\", \"etc\", \"e.g\", \"i.e\", \"mg\"}\n\n\ndef split_units(text, base):\n    units, start, i, n = [], 0, 0, len(text)\n    while i < n:\n        ch = text[i]\n        term = False\n        if ch in \".?!\":\n            tok = re.search(r\"([A-Za-z.]+)$\", text[:i + 1])\n            word = tok.group(1).rstrip(\".\") if tok else \"\"\n            is_abbr = ch == \".\" and word in ABBR\n            in_number = i > 0 and text[i - 1].isdigit() and i + 1 < n and text[i + 1].isdigit()\n            if not is_abbr and not in_number:\n                if i + 1 >= n:\n                    term = True\n                elif text[i + 1].isspace():\n                    rest = text[i + 1:].lstrip()\n                    term = (not rest) or rest[0].isupper() or rest[0].isdigit()\n        elif ch == \";\":\n            term = True\n        if term:\n            units.append((base + start, base + i + 1))\n            start = i + 1\n        i += 1\n    if start < n and text[start:].strip():\n        units.append((base + start, base + n))\n    # trim leading whitespace from each unit\n    fixed = []\n    for s, e in units:\n        while s < e and sample[s].isspace():\n            s += 1\n        fixed.append((s, e))\n    return fixed\n\n\nmine = split_units(body, q0)\napi_units = [(477, 502), (503, 532)]\nsent_block = re.search(r'\"sentences\": \\[(.*?)\\] \\}', api, re.S)\napi_list = re.findall(r'\"start\": (\\d+), \"end\": (\\d+)', sent_block.group(1)) if sent_block else []\napi_list = [(int(a), int(b)) for a, b in api_list]\nspan_mine = [u for u in mine if 470 <= u[0] <= 540]\nmg_unit_ok = (477, 532) in mine or any(u[0] == 477 and u[1] >= 532 for u in mine)\ncheck(\"AC4 'mg.' is not a terminator: R-TL-2 splitter yields one unit covering 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'\",\n      mg_unit_ok,\n      [\"R-TL-2 splitter on sample record 2 (absolute offsets): %s\" % mine,\n       \"api.md:91 sentences for the same span: %s\" % api_list,\n       \"units in span per splitter: %s\" % span_mine])\n\n# 6. AI line: R-EX-4(1) fixed text vs DECISIONS vs golden (AC5)\nspec = read(\"spec/REQUIREMENTS.md\")\nr_ex4_1 = \"AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.\"\nline_dec = [l for l in dec.splitlines() if \"AI assistance\" in l]\ngolden_ai = [l for l in read(\"evals/golden/sample.export.expected.txt\").splitlines() if \"AI assistance\" in l]\ncheck(\"AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text\",\n      r_ex4_1 in dec,\n      [\"R-EX-4(1) text present in DECISIONS.md: %s\" % (r_ex4_1 in dec),\n       \"R-EX-4(1) text present in spec §6 worked example: %s\" % (r_ex4_1 in spec),\n       \"golden INTERNAL_NOTES line: %s\" % (golden_ai[0][:140] if golden_ai else \"none\"),\n       \"DECISIONS.md:204 quotes: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.'\"])\n\n# 7. api.md export example references the golden file (AC6)\ncheck(\"AC6 api.md export example references evals/golden/sample.export.expected.txt\",\n      \"evals/golden/sample.export.expected.txt\" in api,\n      [\"count in api.md: %d\" % api.count(\"evals/golden/sample.export.expected.txt\")])\n\n# 8. Spec §8 row 1 check: diff of export example against golden expects none\ncheck(\"SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')\",\n      False,\n      [\"api.md export example abbreviates both text blocks ('[... full text is ... ...]') so a diff cannot be empty\"])\n\n# 9. Cut line keeps per-record flag pass (AC7)\nreadme = read(\"app/README-arch.md\")\ncut = readme.split(\"## Cut line\", 1)[1]\ncheck(\"AC7 README-arch cut line does not list the per-record flag pass as cut\",\n      \"per-record flag pass is not on the cut line\" in cut and \"per-record flag pass folded\" not in cut,\n      [\"cut-line sentence present: %s\" % (\"per-record flag pass is not on the cut line\" in cut)])\n\n# 10. D-ids cited resolve to ORCHESTRATOR_DECISIONS rows (AC8)\norch = read(\"memory/ORCHESTRATOR_DECISIONS.md\")\ndefined = set(re.findall(r\"^\\| (D-0\\d{2}) \\|\", orch, re.M))\ncited = set()\nfor f in [\"memory/DECISIONS.md\", \"memory/contracts/api.md\", \"docs/LLM_VS_CODE.md\", \"app/README-arch.md\"]:\n    cited |= set(re.findall(r\"D-0\\d{2}\", read(f)))\ncheck(\"AC8 every D-id cited in the four docs is defined (D-001..D-024)\",\n      cited <= defined,\n      [\"defined: %d (%s..%s)\" % (len(defined), min(defined), max(defined)),\n       \"cited but undefined: %s\" % sorted(cited - defined),\n       \"D-ids cited in DECISIONS.md: %s\" % sorted(set(re.findall(r\"D-0\\d{2}\", dec)))])\n\nprint()\nprint(\"SUMMARY: %d/%d checks passed\" % (sum(results), len(results)))\nsys.exit(0 if all(results) else 1)\n"
}
````

### User / tool · 2026-11-02T01:07:11.407Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:15.984Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py",
 "old_string": "# 2b. Per-category flag template text in ADR-013 (AC2 'with a template')\ntmpl_mentions = {c: len(re.findall(r\"template\", adr13)) for c in lex_cats[:1]}\ncheck(\"AC2 each category has a flag template stated in ADR-013\",\n      False,\n      [\"ADR-013 contains the word 'template' %d times and one example wording; no per-category template text\"\n       % len(re.findall(r\"template\", adr13)),\n       \"app/backend/flag_templates.py exists: %s\" % (ROOT / \"app/backend/flag_templates.py\").exists()])",
 "new_string": "# 2b. Per-category flag template text in ADR-013 (AC2 'with a template')\nper_cat = {c: bool(re.search(r\"\\b\" + re.escape(c) + r\"\\b[^\\n]{0,120}template|template[^\\n]{0,120}\\b\" + re.escape(c) + r\"\\b\", adr13))\n           for c in lex_cats}\ncheck(\"AC2 each lexicon category has a flag template stated in ADR-013\",\n      all(per_cat.values()),\n      [\"categories with a template named beside them: %s\" % sorted(c for c, ok in per_cat.items() if ok),\n       \"ADR-013 'template' mentions: %d\" % len(re.findall(r\"template\", adr13)),\n       \"app/backend/flag_templates.py exists: %s\" % (ROOT / \"app/backend/flag_templates.py\").exists()])"
}
````

### User / tool · 2026-11-02T01:07:16.087Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:19.150Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py'\ns=open(p,encoding='utf-8').read()\ns=s.replace('''golden = yaml.safe_load(open(ROOT / \"evals/golden/case_01_date_formats.expected.json\", encoding=\"utf-8\")) \\\\\n    if False else None\n''','')\ns=s.replace('''check(\"SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')\",\n      False,\n      [\"api.md export example abbreviates both text blocks ('[... full text is ... ...]') so a diff cannot be empty\"])''','''abbreviated = \"full text is the INTERNAL_NOTES_TEXT block\" in api\ncheck(\"SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')\",\n      not abbreviated,\n      [\"api.md export example abbreviates the notes block: %s\" % abbreviated,\n       \"so 'diff against golden' cannot be empty as spec §8 row 1 requires\"])''')\nopen(p,'w',encoding='utf-8').write(s)\nprint('ok', 'if False' not in s)\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py; echo \"EXIT=$?\"",
 "description": "Patch evidence script and run T-028 mechanical checks"
}
````

### User / tool · 2026-11-02T01:07:19.345Z

**tool result**
````
ok True
PASS AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md
    memory/contracts/api.md: 1
    memory/DECISIONS.md: 3
    docs/LLM_VS_CODE.md: 1
PASS AC2 every lexicon v2 category name appears in ADR-013
    lexicon categories (13): ['accident_date_provenance', 'alternative_cause', 'degenerative_language', 'litigation_referral', 'missed_care', 'new_onset', 'objective_negative', 'patient_report', 'pre_existing', 'prior_surgery', 'recovery_context', 'scene_facts', 'speculative_language']
    missing from ADR-013: []
FAIL AC2 each lexicon category has a flag template stated in ADR-013
    categories with a template named beside them: ['recovery_context']
    ADR-013 'template' mentions: 4
    app/backend/flag_templates.py exists: False
PASS AC3a confirm_date example gap_flags empty for phone note r8
    api.md confirm_date example contains "gap_flags": [] : True
PASS AC3b date_invalid is the only code for a non-candidate date
    lines naming non-candidate dates: 2
    - Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input
    `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` e
PASS AC4 'mg.' is not a terminator: R-TL-2 splitter yields one unit covering 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'
    R-TL-2 splitter on sample record 2 (absolute offsets): [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
    api.md:91 sentences for the same span: [(396, 416), (417, 458), (459, 476), (477, 502), (503, 532), (533, 552)]
    units in span per splitter: [(477, 532), (533, 552)]
FAIL AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text
    R-EX-4(1) text present in DECISIONS.md: False
    R-EX-4(1) text present in spec §6 worked example: True
    golden INTERNAL_NOTES line: This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
    DECISIONS.md:204 quotes: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.'
PASS AC6 api.md export example references evals/golden/sample.export.expected.txt
    count in api.md: 2
FAIL SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')
    api.md export example abbreviates the notes block: True
    so 'diff against golden' cannot be empty as spec §8 row 1 requires
PASS AC7 README-arch cut line does not list the per-record flag pass as cut
    cut-line sentence present: True
PASS AC8 every D-id cited in the four docs is defined (D-001..D-024)
    defined: 24 (D-001..D-024)
    cited but undefined: []
    D-ids cited in DECISIONS.md: ['D-001', 'D-002', 'D-003', 'D-004', 'D-005', 'D-006', 'D-007', 'D-008', 'D-009', 'D-010', 'D-011', 'D-012', 'D-013', 'D-014', 'D-015', 'D-017', 'D-018', 'D-019', 'D-020', 'D-021', 'D-022', 'D-024']

SUMMARY: 8/11 checks passed
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:28.218Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py'\ns=open(p,encoding='utf-8').read()\nold=s[s.index('span_mine = [u for u in mine'):s.index('# 6. AI line')]\nnew='''span_mine = [u for u in mine if 470 <= u[0] <= 540]\nmg_rule_ok = (477, 532) in mine\ncheck(\"AC4a splitter rule: 'mg.' is not a terminator (R-TL-2, D-021), one unit for record 2 span 477-532\",\n      mg_rule_ok,\n      [\"R-TL-2 splitter on sample record 2 (absolute offsets): %s\" % mine,\n       \"units in span per splitter: %s\" % span_mine])\napi_span = [u for u in api_list if 470 <= u[0] <= 540]\ncheck(\"AC4b api.md example treats 'mg.' as abbreviation (sentences list agrees with splitter)\",\n      api_span == [(477, 532)],\n      [\"api.md:91 sentences for the same span: %s\" % api_span,\n       \"splitter units for the same span:     %s\" % span_mine])\n\n'''\ns=s.replace(old,new)\nopen(p,'w',encoding='utf-8').write(s)\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t028.out 2>&1; echo \"EXIT=$?\"; grep -E \"^(PASS|FAIL)|SUMMARY\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t028.out; grep -A3 \"AC4b\" /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t028.out",
 "description": "Split mg. check into rule and api.md example, rerun"
}
````

### User / tool · 2026-11-02T01:07:28.436Z

**tool result**
````
EXIT=1
PASS AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md
PASS AC2 every lexicon v2 category name appears in ADR-013
FAIL AC2 each lexicon category has a flag template stated in ADR-013
PASS AC3a confirm_date example gap_flags empty for phone note r8
PASS AC3b date_invalid is the only code for a non-candidate date
PASS AC4a splitter rule: 'mg.' is not a terminator (R-TL-2, D-021), one unit for record 2 span 477-532
FAIL AC4b api.md example treats 'mg.' as abbreviation (sentences list agrees with splitter)
FAIL AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text
PASS AC6 api.md export example references evals/golden/sample.export.expected.txt
FAIL SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')
PASS AC7 README-arch cut line does not list the per-record flag pass as cut
PASS AC8 every D-id cited in the four docs is defined (D-001..D-024)
SUMMARY: 8/12 checks passed
FAIL AC4b api.md example treats 'mg.' as abbreviation (sentences list agrees with splitter)
    api.md:91 sentences for the same span: [(477, 502), (503, 532), (533, 552)]
    splitter units for the same span:     [(477, 532), (533, 552)]
FAIL AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:33.210Z

**tool call — Bash**
````
{
 "command": "ls app/pipeline.py app/__init__.py 2>&1; echo \"--- pytest ---\"; .venv/bin/python -m pytest tests/unit -q 2>&1 | tail -3; echo \"pytest_exit=${PIPESTATUS[0]}\"; echo \"--- CLI ---\"; .venv/bin/python -m app.pipeline evals/golden/sample.txt 2>&1 | tail -2; echo \"cli_exit=${PIPESTATUS[0]}\"; echo \"--- git ---\"; git rev-parse --is-inside-work-tree 2>&1; git log --oneline -1 2>&1 | head -2; echo \"--- golden self-check exit ---\"; python3 evals/golden/check_golden.py >/dev/null 2>&1; echo \"check_golden_exit=$?\"; echo \"--- board validate ---\"; python3 tools/board.py validate 2>&1 | tail -3; echo \"validate_exit=${PIPESTATUS[0]}\"",
 "description": "Run unit tests, pipeline CLI, git and board validation checks"
}
````

### User / tool · 2026-11-02T01:07:33.696Z

**tool result**
````
ls: app/__init__.py: No such file or directory
ls: app/pipeline.py: No such file or directory
--- pytest ---

no tests ran in 0.00s
pytest_exit=5
--- CLI ---
/Users/arsis/zlayt-pm-project/.venv/bin/python: No module named app.pipeline
cli_exit=1
--- git ---
true
f454c41 docs(spec): T-025 closed; §6 notes block synced to golden; R-FL-4 references all golden must_nots
--- golden self-check exit ---
check_golden_exit=0
--- board validate ---
ok (28 file(s))
validate_exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:36.725Z

**tool call — Bash**
````
{
 "command": "git cat-file -t de749c2 2>&1; git show --stat --format='%h %s' de749c2 2>&1 | head -12; echo \"--- status (in-scope files) ---\"; git status --short -- memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md app/llm/lexicon.yaml spec/REQUIREMENTS.md evals/golden 2>&1 | head; echo \"--- diff HEAD vs de749c2 in-scope (names) ---\"; git diff --stat de749c2 HEAD -- memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md 2>&1 | tail -3",
 "description": "Check card commit de749c2 and working-tree status of in-scope files"
}
````

### User / tool · 2026-11-02T01:07:36.877Z

**tool result**
````
commit
de749c2 docs(architect): T-028 consistency pass (D-022, lexicon v2 categories, mg., confirm_date)

 app/README-arch.md      |  2 +-
 docs/LLM_VS_CODE.md     | 10 +++++-----
 memory/DECISIONS.md     | 17 +++++++++--------
 memory/contracts/api.md |  6 +++---
 4 files changed, 18 insertions(+), 17 deletions(-)
--- status (in-scope files) ---
--- diff HEAD vs de749c2 in-scope (names) ---
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:07:40.658Z

**tool call — Bash**
````
{
 "command": "git show de749c2 -- memory/DECISIONS.md | grep -n \"^[-+].*AI assistance\" | cut -c1-260; echo \"--- spec R-EX-4(1) last changed ---\"; git log --oneline -3 -- spec/REQUIREMENTS.md | cat; echo \"--- api.md sentences line in de749c2 vs before ---\"; git show de749c2 -- memory/contracts/api.md | grep -n \"^[-+].*mg\\.\\|^[-+].*sentences\" | cut -c1-200",
 "description": "Trace architect edits to AI line and api.md mg. sentence units"
}
````

### User / tool · 2026-11-02T01:07:40.871Z

**tool result**
````
53:-  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line `AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.` and the pending count; includes "flagged lang
54:+  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`)
--- spec R-EX-4(1) last changed ---
f454c41 docs(spec): T-025 closed; §6 notes block synced to golden; R-FL-4 references all golden must_nots
65537a4 fix(harness): debt entry no longer masks later fails; board-guard catches move-done in any arg order; M0 r3 closures
4cc0f81 docs(spec): golden is authority for exports; section 8 owners updated
--- api.md sentences line in de749c2 vs before ---
23:-  "letter_text": "TREATMENT CHRONOLOGY\n\nJanuary 9, 2026 — Austin EMS run report\nRestrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; alert and oriented; transported to
24:-  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\nAI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.\nPendin
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:07.736Z

**tool call — Bash**
````
{
 "command": "grep -n \"template\" memory/DECISIONS.md | sed -n '1,12p' | cut -c1-220; echo \"---\"; grep -n \"recovery_context\" memory/DECISIONS.md | cut -c1-120",
 "description": "Show every template mention in DECISIONS.md to judge ADR-013 coverage"
}
````

### User / tool · 2026-11-02T01:08:07.829Z

**tool result**
````
7:012 token check on summaries and edits · 013 flag text is templated · 014 conflicts and the accident-date rule, offsets and grounding ·
88:              title, explanation (both rendered from code templates), computed_json (days, from, to, stated dates),
123:  - **Deviations from contract §5.2, recorded:** (i) no separate "clinical facts" field (extra paraphrase is extra room to invent); (ii) added J4 and the instruction-like-text row; (iii) amounts are classified by co
154:  - Every reason is a code from a closed list (appendix of `api.md`); the "Why?" sentence is a fixed template per code, never LLM text.
199:## ADR-009 Export: two blocks; the template of record is REQUIREMENTS section 6 and the golden file
243:- Alternatives considered: rejecting instead of `needs_review` (the orchestrator chose to keep the item visible for repair); excerpt-only allowed text (would flag the template's own "Visit 8" summary).
258:    Every category has a code template and a flag_type. `recovery_context` entries have `strength: low` and never raise a flag (context only). Categories with no LLM prompt behind them are lexicon-only (origin `lexic
259:  - Code verifies the excerpt, computes offsets and renders `title` and `explanation` from a template per category (`app/backend/flag_templates.py`; a unit test asserts every category has one), for example "Wording t
261:- Consequences: no free LLM string reaches the internal notes; the golden `must_not` list can be tested against templates.
---
255:    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_c
258:    Every category has a code template and a flag_type. `recovery_context` entries have `strength: low` and never ra
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:08:15.618Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py'\ns=open(p,encoding='utf-8').read()\nold='''per_cat = {c: bool(re.search(r\"\\\\b\" + re.escape(c) + r\"\\\\b[^\\\\n]{0,120}template|template[^\\\\n]{0,120}\\\\b\" + re.escape(c) + r\"\\\\b\", adr13))\n           for c in lex_cats}\ncheck(\"AC2 each lexicon category has a flag template stated in ADR-013\",\n      all(per_cat.values()),\n      [\"categories with a template named beside them: %s\" % sorted(c for c, ok in per_cat.items() if ok),\n       \"ADR-013 'template' mentions: %d\" % len(re.findall(r\"template\", adr13)),'''\nnew='''# the generic sentence \"Every category has a code template\" is an assertion, not a per-category template\nadr13_specific = \"\\\\n\".join(l for l in adr13.splitlines() if \"Every category has a code template\" not in l)\nper_cat = {c: bool(re.search(r\"\\\\b\" + re.escape(c) + r\"\\\\b[^\\\\n]{0,120}template|template[^\\\\n]{0,120}\\\\b\" + re.escape(c) + r\"\\\\b\", adr13_specific))\n           for c in lex_cats}\ncheck(\"AC2 each lexicon category has a flag template stated in ADR-013\",\n      all(per_cat.values()),\n      [\"categories with a per-category template in ADR-013: %d of %d %s\" % (sum(per_cat.values()), len(lex_cats), sorted(c for c, ok in per_cat.items() if ok)),\n       \"only template statements are generic: DECISIONS.md lines containing 'template': %s\" % [i + 1 for i, l in enumerate(dec.splitlines()) if 'template' in l and 'ADR-013' not in l and 240 < i + 1 < 262],'''\nassert old in s, \"pattern not found\"\ns=s.replace(old,new)\nopen(p,'w',encoding='utf-8').write(s)\nprint(\"patched\")\nEOF\n.venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py > /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t028.out 2>&1; echo \"EXIT=$?\"; cat /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t028.out | cut -c1-260",
 "description": "Fix per-category template check and rerun full evidence script"
}
````

### User / tool · 2026-11-02T01:08:15.824Z

**tool result**
````
patched
EXIT=1
PASS AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md
    memory/contracts/api.md: 1
    memory/DECISIONS.md: 3
    docs/LLM_VS_CODE.md: 1
PASS AC2 every lexicon v2 category name appears in ADR-013
    lexicon categories (13): ['accident_date_provenance', 'alternative_cause', 'degenerative_language', 'litigation_referral', 'missed_care', 'new_onset', 'objective_negative', 'patient_report', 'pre_existing', 'prior_surgery', 'recovery_context', 'scene_facts
    missing from ADR-013: []
FAIL AC2 each lexicon category has a flag template stated in ADR-013
    categories with a per-category template in ADR-013: 0 of 13 []
    only template statements are generic: DECISIONS.md lines containing 'template': [243, 258, 259, 261]
    app/backend/flag_templates.py exists: False
PASS AC3a confirm_date example gap_flags empty for phone note r8
    api.md confirm_date example contains "gap_flags": [] : True
PASS AC3b date_invalid is the only code for a non-candidate date
    lines naming non-candidate dates: 2
    - Errors: HTTP status plus `{"error": {"code": "snake_case", "message": "plain sentence", "detail": {}}}`. Codes: `bad_request` (400), `not_found` (404), `input
    `422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` e
PASS AC4a splitter rule: 'mg.' is not a terminator (R-TL-2, D-021), one unit for record 2 span 477-532
    R-TL-2 splitter on sample record 2 (absolute offsets): [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
    units in span per splitter: [(477, 532), (533, 552)]
FAIL AC4b api.md example treats 'mg.' as abbreviation (sentences list agrees with splitter)
    api.md:91 sentences for the same span: [(477, 502), (503, 532), (533, 552)]
    splitter units for the same span:     [(477, 532), (533, 552)]
FAIL AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text
    R-EX-4(1) text present in DECISIONS.md: False
    R-EX-4(1) text present in spec §6 worked example: True
    golden INTERNAL_NOTES line: This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
    DECISIONS.md:204 quotes: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.'
PASS AC6 api.md export example references evals/golden/sample.export.expected.txt
    count in api.md: 2
FAIL SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')
    api.md export example abbreviates the notes block: True
    so 'diff against golden' cannot be empty as spec §8 row 1 requires
PASS AC7 README-arch cut line does not list the per-record flag pass as cut
    cut-line sentence present: True
PASS AC8 every D-id cited in the four docs is defined (D-001..D-024)
    defined: 24 (D-001..D-024)
    cited but undefined: []
    D-ids cited in DECISIONS.md: ['D-001', 'D-002', 'D-003', 'D-004', 'D-005', 'D-006', 'D-007', 'D-008', 'D-009', 'D-010', 'D-011', 'D-012', 'D-013', 'D-014', 'D-015', 'D-017', 'D-018', 'D-019', 'D-020', 'D-021', 'D-022', 'D-024']

SUMMARY: 8/12 checks passed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:27.580Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md",
 "content": "# Review T-028 (staff-engineer-reviewer): ADR consistency pass\n\nVerdict: **fail** (1 blocker, 2 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).\n\nFour of eight AC items are supported by output. The blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris). The mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit.\n\nMechanical results (artifacts/review-evidence/T-028-review-checks.py): 8 of 12 checks pass. Failing: AC2 per-category templates, AC4b api.md mg. units, AC5 AI line, SPEC-8.1 export diff.\n\n```json\n{\"card\": \"T-028\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git de749c2 (= HEAD for memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; no uncommitted edits to them); spec/REQUIREMENTS.md and evals/golden at HEAD f454c41; no app URL (app/backend and app/pipeline.py do not exist); sample case evals/golden/sample.txt\",\n \"exercised\": [\n   \"python3 tools/board.py show T-028 -> EXIT=0, status in_review, 4 ACs read (claims not trusted)\",\n   \"read personas/staff-engineer.md in full\",\n   \"grep -c SUMMARY_DROPS_QUALIFIER memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md -> 1 / 3 / 1; grep -n shows api.md:439, DECISIONS.md:147,244,309, LLM_VS_CODE.md:43\",\n   \".venv/bin/python -I yaml load app/llm/lexicon.yaml -> version 2, 66 entries, 13 distinct categories: accident_date_provenance, alternative_cause, degenerative_language, litigation_referral, missed_care, new_onset, objective_negative, patient_report, pre_existing, prior_surgery, recovery_context, scene_facts, speculative_language\",\n   \"read memory/DECISIONS.md ADR-013 (lines 246-263): all 13 lexicon names present in the closed list; per-category template text: 0 of 13; only generic template statements at lines 258-259; grep template -> lines 243, 258, 259, 261\",\n   \"ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty\",\n   \"read memory/contracts/api.md error codes (line 9) and confirm_date section (lines 199-212); grep date_invalid / non-candidate -> date_invalid is the only non-candidate code\",\n   \"api.md:209-210 gap_flags [] checked against evals/golden/case_01_date_formats.expected.json: gap_excluded_records [8], record 8 kind phone_note, date null, flags [], record_warnings []\",\n   \"read app/llm/lexicon.yaml code_lists.non_encounter: phone_or_message pattern matches 'Dr. Orla Pennywhistle, phone note' (golden case_01 record 8)\",\n   \"verified api.md:86-92 sentence offsets against evals/golden/sample.txt absolute positions: sample[396:416]='Dx: cervical strain;', sample[477:502]='Rx cyclobenzaprine 10 mg.', sample[503:532]='Follow up with PCP in 1 week.', sample[533:552]='ER charges: $6,240.'\",\n   \"applied R-TL-2 splitter (abbreviation list incl. mg., D-021) to sample record 2 excerpt via artifacts/review-evidence/T-028-review-checks.py: units [(396,416),(417,458),(459,476),(477,532),(533,552)]; api.md:91 gives (477,502),(503,532) -> mismatch\",\n   \"grep -n 'AI assistance' memory/DECISIONS.md spec/REQUIREMENTS.md; exact-string counts: R-EX-4(1) sentence in spec 1, in DECISIONS 0; golden-variant sentence in DECISIONS 1, spec 1, LLM_VS_CODE 1, golden 1\",\n   \"git show de749c2 -- memory/DECISIONS.md: ADR-009 internal-notes bullet changed from the R-EX-4(1) text ('AI assistance: this chronology ... before export.' + 'Pending items') to the golden text, label kept as 'the fixed text of R-EX-4(1)'\",\n   \"read spec/REQUIREMENTS.md R-EX-4 (line 122), spec section 8 reconciliation rows 1-3 (lines 362-371), R-TL-2 (line 49), R-TL-10 (line 57), R-CH-4 (line 81)\",\n   \"read memory/ORCHESTRATOR_DECISIONS.md D-003, D-021, D-022, D-023, D-024; D-021 contains the mg. abbreviation rule; ids cited in the four docs all resolve (AC8 PASS)\",\n   \"read app/README-arch.md in full; cut line (lines 80-82) keeps the per-record flag pass; line 36 lists v1 lexicon category names\",\n   \"python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered'; exit 0\",\n   \"grep -rn '14/14\\\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches (the AC3 evidence count is not reproducible from the repo)\",\n   \".venv/bin/python -m pytest tests/unit -q -> 'no tests ran in 0.00s', exit 5 (tests/unit is empty)\",\n   \".venv/bin/python -m app.pipeline evals/golden/sample.txt -> 'No module named app.pipeline', exit 1 (CLI not built; not runnable at this commit)\",\n   \"python3 tools/board.py validate -> 'ok (28 file(s))', exit 0\",\n   \"python3 -I artifacts/review-evidence/T-028-review-checks.py -> SUMMARY: 8/12 checks passed, exit 1\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"AC1_summary_drops_qualifier\": 5, \"AC2_lexicon_names_in_adr013\": 4, \"AC2_flag_template_per_category\": 1, \"AC3_confirm_date_phone_gap\": 5, \"AC3_date_invalid_only_noncandidate\": 5, \"AC3_mg_abbreviation_consistency\": 2, \"AC3_cut_line_per_record_pass\": 5, \"AC4_export_golden_reference\": 3, \"AC4_ai_line_matches_R-EX-4_1\": 1, \"AC4_d_ids_resolve\": 5, \"evidence_honesty\": 2},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"DECISIONS AI line is not the R-EX-4(1) fixed text, and ADR-009 says it is\",\n   \"evidence\": \"memory/DECISIONS.md:204: 'beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`)'. spec/REQUIREMENTS.md:122 (R-EX-4(1)): 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' followed by 'Pending items: N.'. Repro: grep -c of the R-EX-4(1) sentence in memory/DECISIONS.md = 0. git show de749c2 -- memory/DECISIONS.md replaces the R-EX-4(1) text with the golden text (sample.export.expected.txt:51) and keeps the label 'fixed text of R-EX-4(1)'. Card AC4 evidence says 'AI line aligned to R-EX-4(1)'; that is false.\",\n   \"why_it_matters\": \"The disclosure text is a fixed string the spec names as fixed. DECISIONS says it matches the spec when it does not, so the golden test and the spec will disagree on the first export pytest. The spec is also internally inconsistent: R-EX-4(1) (spec:122) differs from the spec section 6 worked example (spec:273) and the golden file, which section 8's authority rule prefers. The architect followed the authority rule silently and mislabelled the source. Recorded as blocker because the card's stated spec alignment is false and the spec row check (section 8 row 3) fails as written; severity drops to major if Chris rules the golden text canonical and the spec row is amended.\",\n   \"fix\": \"Get Chris's ruling (questions_for_chris[0]). Then keep one string. If R-EX-4(1) wins: change DECISIONS.md:204, the ADR-009 text, LLM_VS_CODE.md:103, spec/REQUIREMENTS.md:273 and golden sample.export.expected.txt:51 (qa owns the golden). If the section 6 / golden text wins: amend R-EX-4(1) at spec/REQUIREMENTS.md:122 and remove 'the fixed text of R-EX-4(1)' from DECISIONS.md:204. Do not keep the label unless the strings are equal.\",\n   \"acceptance_test\": \"artifacts/review-evidence/T-028-review-checks.py AC5 PASS; the chosen sentence appears identically in spec, DECISIONS, LLM_VS_CODE and the golden file (grep -c equal in each); an export test compares the internal-notes block to the golden block byte for byte.\"},\n  {\"severity\": \"major\",\n   \"title\": \"api.md sentence array splits 'Rx cyclobenzaprine 10 mg.' at the abbreviation, contradicting R-TL-2, D-021 and ADR-016\",\n   \"evidence\": \"memory/contracts/api.md:91: '{\\\"text\\\": \\\"Rx cyclobenzaprine 10 mg.\\\", \\\"start\\\": 477, \\\"end\\\": 502}, {\\\"text\\\": \\\"Follow up with PCP in 1 week.\\\", \\\"start\\\": 503, \\\"end\\\": 532}'. memory/DECISIONS.md:285 says this exact sentence is one unit. Repro: artifacts/review-evidence/T-028-review-checks.py AC4b: api.md span [(477,502),(503,532)] vs R-TL-2 splitter span [(477,532)] on evals/golden/sample.txt record 2. This is the T-014 r3 M4 finding, which the card closes but the file still contradicts.\",\n   \"why_it_matters\": \"api.md records[].sentences is the unit list the excerpt editor builds on (ADR-016). An implementer who copies this array lets an excerpt end at 'mg.', a fragment, which breaks the whole-sentence rule (R-TL-2) and the 'hedge travels with its finding' rule. The card AC3 evidence 'mg. one unit [477,532)' is contradicted by the file it cites.\",\n   \"fix\": \"Replace api.md:91 with one unit: {\\\"text\\\": \\\"Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.\\\", \\\"start\\\": 477, \\\"end\\\": 532}; keep the 533-552 unit. Generate the example from the splitter output rather than by hand.\",\n   \"acceptance_test\": \"AC4b in T-028-review-checks.py passes; a unit test runs the real sentence splitter on evals/golden/sample.txt record 2 and asserts equality with the sentences array in api.md (the test reads the array from api.md, so the example cannot drift).\"},\n  {\"severity\": \"major\",\n   \"title\": \"'Each with a flag template' is asserted, not shown: ADR-013 has no per-category template and the template module does not exist\",\n   \"evidence\": \"memory/DECISIONS.md:258: 'Every category has a code template and a flag_type.' memory/DECISIONS.md:259: 'renders title and explanation from a template per category (app/backend/flag_templates.py; a unit test asserts every category has one), for example \\\"Wording that could be used to question causation...\\\"'. Only one template is worded. Repro: T-028-review-checks.py AC2b: 0 of 13 lexicon categories have template text in ADR-013. ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty.\",\n   \"why_it_matters\": \"The 'every flag is code-rendered from a fixed template' rule (docs/LLM_VS_CODE.md row 14) is the control that stops the model writing causation wording. Categories such as recovery_context (strength low, never raises) and the lexicon-only categories have no wording anywhere in the design, so the backend would invent it. A generic sentence is not a template, and the card's 'each with a flag template' is not supported by the ADR.\",\n   \"fix\": \"Add a table to ADR-013 with one template per category: the 13 lexicon categories plus the conflict, gap and record_warning codes it lists. Or check in app/backend/flag_templates.py as a key list equal to the closed category list and cite that file.\",\n   \"acceptance_test\": \"T-028-review-checks.py AC2b reports 13 of 13 lexicon categories with explicit template text (or the template file's key set equals the closed list); a unit test asserts it.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Spec section 8 row 1 check cannot pass: the api.md export example abbreviates the notes block\",\n   \"evidence\": \"spec/REQUIREMENTS.md:362-371 section 8 row 1: 'internal_notes_text should equal the golden notes block' with check 'diff of the example against evals/golden/sample.export.expected.txt (expect none)'. memory/contracts/api.md:272: '\\\"internal_notes_text\\\": \\\"INTERNAL REVIEW NOTES — DO NOT SEND\\\\n\\\\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]\\\"'. Repro: T-028-review-checks.py SPEC-8.1 FAIL.\",\n   \"why_it_matters\": \"Replacing the copy with a pointer (card AC4) is the right call, and T-014 r3 m1 recommended it. But the spec row still demands an empty diff, so the spec and the card now disagree on how this is verified, and a reviewer following the spec will fail the doc. The choice has not been recorded in an ADR.\",\n   \"fix\": \"Either amend spec section 8 row 1 to 'the example names the golden file; a pytest compares real export output with it' and record that in ADR-009, or embed the full block. Make the spec row and the example agree.\",\n   \"acceptance_test\": \"The spec row's check command and the api.md example describe the same verification; a pytest asserts real export output equals evals/golden/sample.export.expected.txt.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"README-arch lexicon line lists v1 category names that lexicon v2 does not contain\",\n   \"evidence\": \"app/README-arch.md:36: 'lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection'. Lexicon v2 entries[].category (13 names, yaml load) contains none of causation_weakening, compliance or hedge; accident_date_phrases, damages, non_encounter and injection are code_lists keys.\",\n   \"why_it_matters\": \"A backend worker reading the architecture map would look for categories that do not exist. ADR-013 maps causation_weakening and compliance to causation; the README does not say so.\",\n   \"fix\": \"Rewrite README-arch.md:36 as the 13 v2 category names plus the 4 code_lists keys, with a pointer to ADR-013.\",\n   \"acceptance_test\": \"A grep or unit test: every name on README-arch.md:36 is in lexicon v2 categories or code_lists keys.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"confirm_date example clears a date_ambiguous warning that the golden case does not expect\",\n   \"evidence\": \"memory/contracts/api.md:209: '\\\"removed_flag_ids\\\": [\\\"f_warn_date_r8\\\"]'. evals/golden/case_01_date_formats.expected.json: \\\"record_warnings\\\": [], \\\"flags\\\": [], \\\"gap_excluded_records\\\": [8]. Golden description: 'Ambiguous date must be marked ambiguous and surfaced for review.' evals/golden/README.md:61 record_warnings schema lists only instruction_like_text.\",\n   \"why_it_matters\": \"The gap example is correct (gap_flags [] matches D-003 and golden). But the example refers to a warning the golden never expects, so either the golden is missing the date_ambiguous expectation or the example names a flag the pipeline is not required to create. Golden is the stated authority for expected outputs (spec section 8).\",\n   \"fix\": \"qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden, or the architect rewrites the example to 'removed_flag_ids: [] (no warning in golden)' and records which one wins.\",\n   \"acceptance_test\": \"check_golden.py asserts a date_ambiguous warning for case_01 record 8 (or the api example has no removed id not present in the golden).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"AC3 evidence cites a count that no checked-in script produces\",\n   \"evidence\": \"Card T-028 AC3 evidence: 'check script 14/14 blocks, 17/17 offsets'. Repro: grep -rn '14/14\\\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches. The offsets themselves verify (sample.txt positions 396, 477, 503, 533 match api.md), but nothing prints the counts.\",\n   \"why_it_matters\": \"A count with no script cannot be re-run by the next reviewer. The same claim covers the mg. offsets, which are wrong (finding 2).\",\n   \"fix\": \"Check the offset and block script into artifacts/review-evidence/ and quote its output in the card; use the output, not a hand count.\",\n   \"acceptance_test\": \"python3 -I artifacts/review-evidence/<script>.py exits 0 and prints the counts quoted in the card.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Gap-math claim: confirm_date example is correct, but the golden and API must agree on record 8 date handling\",\n   \"evidence\": \"memory/contracts/api.md:212 says 'The example is golden case_01 record 8, a phone note (encounter: false)'. golden case_01 record 8: kind phone_note, date null, raw_date 04/05/2026, gap_excluded_records [8]. The example's date 2026-05-04 is one of the two readings; golden must_not M2 forbids silently assigning a date.\",\n   \"why_it_matters\": \"The example shows a human choice (confirm_date) and is labelled as such, so it does not break M2. It is listed here only so the golden and the example are checked together after the finding 6 fix.\",\n   \"fix\": \"No change required beyond finding 6; make the example's text say 'a paralegal chooses 2026-05-04'.\",\n   \"acceptance_test\": \"Covered by finding 6 acceptance.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"AC4 evidence 'D-001..D-024 in all three docs' overstates the citations\",\n   \"evidence\": \"Distinct D-ids: memory/DECISIONS.md 22 (no D-016, no D-023); memory/contracts/api.md 8 (D-001 D-003 D-010 D-012 D-013 D-020 D-022 D-024); docs/LLM_VS_CODE.md 2 (D-001, D-024). Every cited id resolves (T-028-review-checks.py AC8 PASS).\",\n   \"why_it_matters\": \"The substance passes; the evidence sentence does not describe the files.\",\n   \"fix\": \"Restate the evidence as 'every cited D-id resolves to a row in ORCHESTRATOR_DECISIONS (D-001..D-024)'.\",\n   \"acceptance_test\": \"T-028-review-checks.py AC8 PASS (already true).\"}\n ],\n \"whats_right\": [\n   \"SUMMARY_DROPS_QUALIFIER is present and consistent: api.md 1, DECISIONS.md 3, LLM_VS_CODE.md 1, matching R-TL-10(b) and D-022.\",\n   \"ADR-013 names all 13 lexicon v2 categories, and the confirm_date example's gap_flags [] matches golden gap_excluded_records [8] and D-003 (phone note, not in gap math).\",\n   \"The README-arch cut line keeps the per-record flag pass (README-arch.md:82), and money stays integer cents with the $185 rate outside the 839000 total (api.md:6, 124, 135).\"\n ],\n \"questions_for_chris\": [\n   \"Which AI disclosure line is canonical: R-EX-4(1) ('AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' + 'Pending items: N.') or the section 6 / golden line ('This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.')? The spec currently has both.\",\n   \"Should api.md embed the notes block (spec section 8 row 1 says diff expect none) or point to the golden file (card AC4 chose a pointer)?\",\n   \"D-024 puts Tier-1 card reviews on sonnet. This review ran as claude-haiku-5-5. Accept it for mechanical doc passes, or re-run on sonnet?\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T01:09:27.813Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:34.692Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md",
 "offset": 1,
 "limit": 12
}
````

### User / tool · 2026-11-02T01:09:34.702Z

**tool result**
````
1	# Review T-028 (staff-engineer-reviewer): ADR consistency pass
2	
3	Verdict: **fail** (1 blocker, 2 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).
4	
5	Four of eight AC items are supported by output. The blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris). The mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit.
6	
7	Mechanical results (artifacts/review-evidence/T-028-review-checks.py): 8 of 12 checks pass. Failing: AC2 per-category templates, AC4b api.md mg. units, AC5 AI line, SPEC-8.1 export diff.
8	
9	```json
10	{"card": "T-028", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
11	 "scope": "git de749c2 (= HEAD for memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; no uncommitted edits to them); spec/REQUIREMENTS.md and evals/golden at HEAD f454c41; no app URL (app/backend and app/pipeline.py do not exist); sample case evals/golden/sample.txt",
12	 "exercised": [
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:37.468Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md",
 "old_string": "Verdict: **fail** (1 blocker, 2 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).\n\nFour of eight AC items are supported by output. The blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris). The mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit.",
 "new_string": "Verdict: **fail** (1 blocker, 3 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).\n\nCard ACs against the output: AC1 supported. AC2 category names supported, per-category templates not. AC3 confirm_date gap, date_invalid and cut line supported; the mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit. AC4 golden reference supported; the AI line claim is false; the D-id wording overstates the citations.\n\nThe blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris)."
}
````

### User / tool · 2026-11-02T01:09:37.640Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:38.648Z

Now I'll remove the padding finding (the one that says "no change required") and fix the minor count.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:39.914Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md",
 "old_string": "  {\"severity\": \"minor\",\n   \"title\": \"Gap-math claim: confirm_date example is correct, but the golden and API must agree on record 8 date handling\",\n   \"evidence\": \"memory/contracts/api.md:212 says 'The example is golden case_01 record 8, a phone note (encounter: false)'. golden case_01 record 8: kind phone_note, date null, raw_date 04/05/2026, gap_excluded_records [8]. The example's date 2026-05-04 is one of the two readings; golden must_not M2 forbids silently assigning a date.\",\n   \"why_it_matters\": \"The example shows a human choice (confirm_date) and is labelled as such, so it does not break M2. It is listed here only so the golden and the example are checked together after the finding 6 fix.\",\n   \"fix\": \"No change required beyond finding 6; make the example's text say 'a paralegal chooses 2026-05-04'.\",\n   \"acceptance_test\": \"Covered by finding 6 acceptance.\"},\n  {\"severity\": \"nit\",",
 "new_string": "  {\"severity\": \"nit\","
}
````

### User / tool · 2026-11-02T01:09:40.097Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:43.640Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt=open('reviews/T-028-staff-engineer.md',encoding='utf-8').read()\nblocks=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd=json.loads(blocks[0])\nprint('keys:', sorted(d.keys()))\nprint('verdict:', d['verdict'], '| model:', d['model'])\nfrom collections import Counter\nc=Counter(f['severity'] for f in d['findings']); print('severity counts:', dict(c))\nexp='fail' if c.get('blocker',0) else ('changes' if c.get('major',0) else 'pass')\nprint('verdict rule expects:', exp, 'match:', exp==d['verdict'])\n\"; echo \"--- board validate ---\"; python3 tools/board.py validate 2>&1 | tail -5; echo \"validate_exit=${PIPESTATUS[0]}\"",
 "description": "Parse review JSON, check verdict rule and run board validator"
}
````

### User / tool · 2026-11-02T01:09:43.700Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:47.840Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_review_json.py",
 "content": "import json\nimport re\nfrom collections import Counter\n\npath = \"/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md\"\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"keys:\", sorted(d.keys()))\nprint(\"verdict:\", d[\"verdict\"], \"| model:\", d[\"model\"], \"| card:\", d[\"card\"], \"| persona:\", d[\"persona\"])\nc = Counter(f[\"severity\"] for f in d[\"findings\"])\nprint(\"severity counts:\", dict(c))\nexpected = \"fail\" if c.get(\"blocker\", 0) else (\"changes\" if c.get(\"major\", 0) else \"pass\")\nprint(\"verdict rule expects:\", expected, \"| matches file:\", expected == d[\"verdict\"])\nprint(\"whats_right count:\", len(d[\"whats_right\"]), \"| questions:\", len(d[\"questions_for_chris\"]))\n"
}
````

### User / tool · 2026-11-02T01:09:47.900Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_review_json.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:48.295Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py validate 2>&1 | tail -5; echo \"validate_exit=${PIPESTATUS[0]}\"",
 "description": "Run board validator on the repository (read-only)"
}
````

### User / tool · 2026-11-02T01:09:48.438Z

**tool result**
````
ok (28 file(s))
validate_exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:51.455Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-json-check.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Parse the single JSON block of reviews/T-028-staff-engineer.md and check the D.2 verdict rule.\n\nRun:  .venv/bin/python -I artifacts/review-evidence/T-028-review-json-check.py\n\"\"\"\nimport json\nimport re\nfrom collections import Counter\nfrom pathlib import Path\n\npath = Path(__file__).resolve().parents[2] / \"reviews\" / \"T-028-staff-engineer.md\"\ntext = path.read_text(encoding=\"utf-8\")\nfence = \"`\" * 3\nblocks = re.findall(re.escape(fence) + r\"json\\n(.*?)\\n\" + re.escape(fence), text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nprint(\"keys:\", sorted(d.keys()))\nprint(\"verdict:\", d[\"verdict\"], \"| model:\", d[\"model\"], \"| card:\", d[\"card\"], \"| persona:\", d[\"persona\"])\nc = Counter(f[\"severity\"] for f in d[\"findings\"])\nprint(\"severity counts:\", dict(c))\nexpected = \"fail\" if c.get(\"blocker\", 0) else (\"changes\" if c.get(\"major\", 0) else \"pass\")\nprint(\"verdict rule expects:\", expected, \"| matches file:\", expected == d[\"verdict\"])\nprint(\"whats_right:\", len(d[\"whats_right\"]), \"| questions_for_chris:\", len(d[\"questions_for_chris\"]))\n"
}
````

### User / tool · 2026-11-02T01:09:51.573Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-json-check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:52.882Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-028-review-json-check.py; echo \"exit=$?\"",
 "description": "Run JSON block parse and verdict-rule check on the review"
}
````

### User / tool · 2026-11-02T01:09:52.995Z

**tool result**
````
json blocks: 1
keys: ['card', 'exercised', 'findings', 'model', 'persona', 'questions_for_chris', 'scope', 'scores', 'verdict', 'whats_right']
verdict: fail | model: claude-haiku-5-5 | card: T-028 | persona: staff-engineer-reviewer
severity counts: {'blocker': 1, 'major': 3, 'minor': 3, 'nit': 1}
verdict rule expects: fail | matches file: True
whats_right: 3 | questions_for_chris: 3
exit=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:56.403Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md"
}
````

### User / tool · 2026-11-02T01:09:56.412Z

**tool result**
````
1	---
2	name: design-review-patterns
3	description: Recurring design-level defects found reviewing the Zlayt treatment-timeline architecture (T-014 rounds 1-2); check these first on later cards
4	metadata:
5	  type: project
6	---
7	
8	Round 1 (2026-11-01, fail): defects, all resolved in round 2 but re-check them in M2 code reviews.
9	- Flag/gap logic keyed on LLM entries instead of code-parsed record dates (r5 dropped -> false 42-day gap). In M2 test that gaps use `records.date_iso`.
10	- Export default omitted verbatim excerpt (cite=short) vs ship bar 1 / R-EX-2.
11	- Judge #2 skipped on code-classified amounts; summary numerals not code-checked; retry count wording inconsistent.
12	- Illustrative JSON in api.md had wrong offsets and a `{...}` block. Re-run `artifacts/review-evidence/T-014-json-check.py` and `T-014-r2-offset-check.py` after any api.md edit.
13	
14	Round 2 (changes, 4 majors) - new pattern: the architect's docs drift from REQUIREMENTS revision N because writer and architect edit in parallel.
15	- Export format restated in ADR-009, api.md and the golden file differ from REQUIREMENTS sec 6 (dot leaders, Source line, total-line parenthetical). Check byte-equality test target first.
16	- ADR-011 amount rules: simulate them on all `evals/golden/*.txt` (`T-014-r2-amount-sim.py`); case_09 `$275` billing-statement amount fell to `unclear`. Charges are accept/dismiss only, so a missed rule is unrecoverable for the user.
17	- Anything that calls a judge at request time (edit re-check) needs a stated judge-failure / FixtureMiss path; demo mode makes every edit a fixture miss.
18	- ADR-016 over-applied D-012 (forced inclusion of lexicon sentences; `mg.` abbreviation) vs R-TL-8 hedge-only.
19	- D-018 landed after the architect started; always check the newest D-xx against ADR category lists.
20	
21	**Why:** these made T-014 fail round 1 (2026-11-01) and require changes in round 2.
22	**How to apply:** on M2 backend review, run the golden amount simulation against the real `amounts.py`, check export equals golden file, and grep for a defined judge-unavailable path.
23	
24	Round 3 (2026-11-01, changes, 5 majors): same parallel-edit drift, now against lexicon v2, D-021/D-022 and the golden file.
25	- Check ADR category lists against the real `app/llm/lexicon.yaml` category values (6 lexicon categories were missing from ADR-013; P1 floor flag had no template).
26	- A binding D-xx can land during the architect's round (D-022 SUMMARY_DROPS_QUALIFIER was missed); grep new reason codes in api.md appendix.
27	- Embedded copies of files others own (api.md export vs golden) drift within the hour; recommend pointer + test, not a copy. Working tree can hold other agents' uncommitted edits: compare with `git show <rev>:path`.
28	- api.md examples that claim golden provenance: verify against the golden `gap_excluded_records` (confirm_date example put a phone note into gap math).
29	- Cut-line items can silently undo a structural control (per-record flag pass): read the cut line against ADR-008.
30	- Evidence: `artifacts/review-evidence/T-014-r3-amount-sim.py` / `-amount-demo.py` (real lexicon, ADR-011 r3 rules; 14/14 dollar amounts).
31	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:09:56.605Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T01:09:56.615Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1+r2 defects: doc/REQ drift, amount-rule coverage, judge-failure path
3	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:10:01.014Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md",
 "old_string": "- Evidence: `artifacts/review-evidence/T-014-r3-amount-sim.py` / `-amount-demo.py` (real lexicon, ADR-011 r3 rules; 14/14 dollar amounts).\n",
 "new_string": "- Evidence: `artifacts/review-evidence/T-014-r3-amount-sim.py` / `-amount-demo.py` (real lexicon, ADR-011 r3 rules; 14/14 dollar amounts).\n\nRound 4 = T-028 consistency pass (2026-11-01, fail: 1 blocker, 3 majors). Evidence: `artifacts/review-evidence/T-028-review-checks.py`.\n- Fix claims drift from the file: the architect's \"mg. one unit\" evidence is contradicted by api.md:91 (two units). T-014 r3 M4 came back after DECISIONS was fixed; ADR text and illustrative JSON are separate places to fix. Re-run the R-TL-2 splitter on sample record 2 after any api.md sentence edit.\n- \"Fixed text of R-EX-4(1)\" label on a string that is not R-EX-4(1). The spec itself had two AI lines (R-EX-4(1) vs section 6 / golden). Architect followed the golden-authority rule silently. When the spec disagrees with itself, the card must say so, not claim alignment.\n- A spec reconciliation check (\"diff of the example against golden, expect none\") cannot pass once the example is a pointer. Amend the check row or the example; never leave them disagreeing.\n- \"Each with a template\" in an ADR is a generic assertion; count per-category template text, not the word \"template\".\n- Evidence counts with no script in the repo (\"14/14 blocks, 17/17 offsets\") are not reproducible; ask for the script in artifacts/review-evidence.\n\n**Why:** these were the open T-014 r3 items closed by T-028; closure claims were partly false.\n**How to apply:** on any ADR or api.md consistency card, grep the claimed string in every file it names and run the splitter/offset check before accepting \"aligned\".\n"
}
````

### User / tool · 2026-11-02T01:10:01.118Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:10:01.853Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Design review patterns](project_design_review_patterns.md) — T-014 r1+r2 defects: doc/REQ drift, amount-rule coverage, judge-failure path\n",
 "new_string": "- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r3 and T-028 defects: doc/REQ drift, mg. splitter, AI line, template coverage\n"
}
````

### User / tool · 2026-11-02T01:10:01.960Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:10:04.348Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "offset": 24
}
````

### User / tool · 2026-11-02T01:10:04.355Z

**tool result**
````
24	
25	Reviewer-environment gotchas:
26	- As a native `*-reviewer`, board-guard denies all non-read-only `board.py` subcommands even with a temp BOARD_ROOT; write-path repros cannot be run by reviewers (do not route around with python wrappers; ask the orchestrator). Read-only (`validate/show/list/status/next/inbox`) work with BOARD_ROOT set.
27	- Bash redirects are checked against the initial cwd and unexpanded `$VAR` paths: use literal absolute scratchpad paths, or put the work in a script file in the scratchpad. `... | tee path` followed by another command on the next line was also falsely denied.
28	- Agent definitions are a session-start snapshot (my prompt was PROVISIONAL while files were COMPILED); HEAD can move mid-review (orchestrator commits) so re-check `git log -1` before claiming file state.
29	- A chained shell mutation check in a scratch copy (`rm -rf` + `rsync` + `sed -i` + regenerate) was denied by the permission guard on T-016 (2026-11-01). Do not split the chain to get around it; reason from code and label the finding "not reproduced".
30	- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).
31	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:10:07.555Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md",
 "old_string": "- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).\n",
 "new_string": "- Generator `--check` compares generated output to files, so regenerating after a generator change passes it. Content invariants (rules present, D.2 keys, 13 files) need explicit asserts (T-016 r1 minor).\n- (T-028, 2026-11-01) board-guard fails closed on any Bash command it cannot tokenise (\"could not parse command safely (No escaped character)\") when a `python3 -c` one-liner contains backslash-escaped backticks or quotes. Put such logic in a script file under artifacts/review-evidence/ and run that file.\n- (T-028) reviewer-write-guard denies the Write tool outside reviews/ and artifacts/review-evidence/, including the session scratchpad. Bash redirects to the scratchpad are allowed.\n- (T-028) the session header said \"not a git repository\" but `git rev-parse --is-inside-work-tree` returned true at the repo root. Verify with git, quote the output, do not trust the header.\n- (T-028) at f454c41 `app/backend/`, `app/pipeline.py` and `tests/unit/` are empty: `pytest tests/unit -q` exits 5 (no tests), `python -m app.pipeline` exits 1. Doc-stage cards cannot exercise the CLI; say so in `exercised`.\n"
}
````

### User / tool · 2026-11-02T01:10:07.664Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:10:12.473Z

Verdict: **fail**. Review at `/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md` (one JSON block, parses, verdict rule holds, model `claude-haiku-5-5`).
Blocker: DECISIONS.md:204 uses the golden AI line but calls it "the fixed text of R-EX-4(1)", which is spec/REQUIREMENTS.md:122. The spec has two different AI lines, so Chris needs to rule which is canonical.
Majors: api.md:91 still splits "Rx cyclobenzaprine 10 mg." (the T-014 r3 M4 regression); ADR-013 has no per-category flag templates and `app/backend/flag_templates.py` does not exist; spec §8 row 1's "diff expect none" cannot pass against the pointer.
Passed: SUMMARY_DROPS_QUALIFIER (1/3/1), 13/13 lexicon names in ADR-013, gap_flags [], date_invalid, per-record cut line. Checks: 8 of 12 (`artifacts/review-evidence/T-028-review-checks.py`). Note: D-024 specifies sonnet for Tier-1 reviews; this run was haiku.
