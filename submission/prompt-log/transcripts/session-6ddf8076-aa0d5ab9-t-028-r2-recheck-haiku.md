# Subagent: T-028 r2 recheck (haiku) (T-028 r2 recheck (haiku))

Source: `agent-aa0d5ab9da59d4fbc.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:11:21.949Z

Working directory: /Users/arsis/zlayt-pm-project. Re-check T-028 round 2 (commit 10cffcd) against reviews/T-028-staff-engineer.md. Its blocker was stale (verify with `grep -n "drafted with AI assistance" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt` — all must carry the same sentence). Check: ADR-013 has one title+explanation template per lexicon category (compare to category names in app/llm/lexicon.yaml); api.md no longer splits after "10 mg."; `grep -n "sample.export.expected.txt" memory/contracts/api.md`. Quote outputs. Write reviews/T-028-staff-engineer-r2.md (D.2 JSON, model = what you run as). Reply ≤ 3 lines.

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:23.049Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/staff-engineer.md"
}
````

### User / tool · 2026-11-02T01:11:23.059Z

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

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:23.294Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T01:11:23.302Z

**tool result**
````
1	- [Harness review patterns](project_harness_review_patterns.md) — board-guard false positives/bypasses, fail-open py3.9, reviewer env gotchas
2	- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r3 and T-028 defects: doc/REQ drift, mg. splitter, AI line, template coverage
3	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:23.474Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer.md"
}
````

### User / tool · 2026-11-02T01:11:23.484Z

**tool result**
````
1	# Review T-028 (staff-engineer-reviewer): ADR consistency pass
2	
3	Verdict: **fail** (1 blocker, 3 majors, 3 minors, 1 nit). Commit reviewed: de749c2 (identical to HEAD for the four in-scope docs at review time; working tree clean for them).
4	
5	Card ACs against the output: AC1 supported. AC2 category names supported, per-category templates not. AC3 confirm_date gap, date_invalid and cut line supported; the mg. claim is contradicted by api.md:91, which splits the sentence the card says is one unit. AC4 golden reference supported; the AI line claim is false; the D-id wording overstates the citations.
6	
7	The blocker is the AI disclosure line: the card says DECISIONS.md matches R-EX-4(1), and it does not. The spec itself carries two different AI lines, so this needs Chris's ruling (see questions_for_chris).
8	
9	Mechanical results (artifacts/review-evidence/T-028-review-checks.py): 8 of 12 checks pass. Failing: AC2 per-category templates, AC4b api.md mg. units, AC5 AI line, SPEC-8.1 export diff.
10	
11	```json
12	{"card": "T-028", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
13	 "scope": "git de749c2 (= HEAD for memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; no uncommitted edits to them); spec/REQUIREMENTS.md and evals/golden at HEAD f454c41; no app URL (app/backend and app/pipeline.py do not exist); sample case evals/golden/sample.txt",
14	 "exercised": [
15	   "python3 tools/board.py show T-028 -> EXIT=0, status in_review, 4 ACs read (claims not trusted)",
16	   "read personas/staff-engineer.md in full",
17	   "grep -c SUMMARY_DROPS_QUALIFIER memory/contracts/api.md memory/DECISIONS.md docs/LLM_VS_CODE.md -> 1 / 3 / 1; grep -n shows api.md:439, DECISIONS.md:147,244,309, LLM_VS_CODE.md:43",
18	   ".venv/bin/python -I yaml load app/llm/lexicon.yaml -> version 2, 66 entries, 13 distinct categories: accident_date_provenance, alternative_cause, degenerative_language, litigation_referral, missed_care, new_onset, objective_negative, patient_report, pre_existing, prior_surgery, recovery_context, scene_facts, speculative_language",
19	   "read memory/DECISIONS.md ADR-013 (lines 246-263): all 13 lexicon names present in the closed list; per-category template text: 0 of 13; only generic template statements at lines 258-259; grep template -> lines 243, 258, 259, 261",
20	   "ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty",
21	   "read memory/contracts/api.md error codes (line 9) and confirm_date section (lines 199-212); grep date_invalid / non-candidate -> date_invalid is the only non-candidate code",
22	   "api.md:209-210 gap_flags [] checked against evals/golden/case_01_date_formats.expected.json: gap_excluded_records [8], record 8 kind phone_note, date null, flags [], record_warnings []",
23	   "read app/llm/lexicon.yaml code_lists.non_encounter: phone_or_message pattern matches 'Dr. Orla Pennywhistle, phone note' (golden case_01 record 8)",
24	   "verified api.md:86-92 sentence offsets against evals/golden/sample.txt absolute positions: sample[396:416]='Dx: cervical strain;', sample[477:502]='Rx cyclobenzaprine 10 mg.', sample[503:532]='Follow up with PCP in 1 week.', sample[533:552]='ER charges: $6,240.'",
25	   "applied R-TL-2 splitter (abbreviation list incl. mg., D-021) to sample record 2 excerpt via artifacts/review-evidence/T-028-review-checks.py: units [(396,416),(417,458),(459,476),(477,532),(533,552)]; api.md:91 gives (477,502),(503,532) -> mismatch",
26	   "grep -n 'AI assistance' memory/DECISIONS.md spec/REQUIREMENTS.md; exact-string counts: R-EX-4(1) sentence in spec 1, in DECISIONS 0; golden-variant sentence in DECISIONS 1, spec 1, LLM_VS_CODE 1, golden 1",
27	   "git show de749c2 -- memory/DECISIONS.md: ADR-009 internal-notes bullet changed from the R-EX-4(1) text ('AI assistance: this chronology ... before export.' + 'Pending items') to the golden text, label kept as 'the fixed text of R-EX-4(1)'",
28	   "read spec/REQUIREMENTS.md R-EX-4 (line 122), spec section 8 reconciliation rows 1-3 (lines 362-371), R-TL-2 (line 49), R-TL-10 (line 57), R-CH-4 (line 81)",
29	   "read memory/ORCHESTRATOR_DECISIONS.md D-003, D-021, D-022, D-023, D-024; D-021 contains the mg. abbreviation rule; ids cited in the four docs all resolve (AC8 PASS)",
30	   "read app/README-arch.md in full; cut line (lines 80-82) keeps the per-record flag pass; line 36 lists v1 lexicon category names",
31	   "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered'; exit 0",
32	   "grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches (the AC3 evidence count is not reproducible from the repo)",
33	   ".venv/bin/python -m pytest tests/unit -q -> 'no tests ran in 0.00s', exit 5 (tests/unit is empty)",
34	   ".venv/bin/python -m app.pipeline evals/golden/sample.txt -> 'No module named app.pipeline', exit 1 (CLI not built; not runnable at this commit)",
35	   "python3 tools/board.py validate -> 'ok (28 file(s))', exit 0",
36	   "python3 -I artifacts/review-evidence/T-028-review-checks.py -> SUMMARY: 8/12 checks passed, exit 1"
37	 ],
38	 "verdict": "fail",
39	 "scores": {"AC1_summary_drops_qualifier": 5, "AC2_lexicon_names_in_adr013": 4, "AC2_flag_template_per_category": 1, "AC3_confirm_date_phone_gap": 5, "AC3_date_invalid_only_noncandidate": 5, "AC3_mg_abbreviation_consistency": 2, "AC3_cut_line_per_record_pass": 5, "AC4_export_golden_reference": 3, "AC4_ai_line_matches_R-EX-4_1": 1, "AC4_d_ids_resolve": 5, "evidence_honesty": 2},
40	 "findings": [
41	  {"severity": "blocker",
42	   "title": "DECISIONS AI line is not the R-EX-4(1) fixed text, and ADR-009 says it is",
43	   "evidence": "memory/DECISIONS.md:204: 'beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`)'. spec/REQUIREMENTS.md:122 (R-EX-4(1)): 'AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' followed by 'Pending items: N.'. Repro: grep -c of the R-EX-4(1) sentence in memory/DECISIONS.md = 0. git show de749c2 -- memory/DECISIONS.md replaces the R-EX-4(1) text with the golden text (sample.export.expected.txt:51) and keeps the label 'fixed text of R-EX-4(1)'. Card AC4 evidence says 'AI line aligned to R-EX-4(1)'; that is false.",
44	   "why_it_matters": "The disclosure text is a fixed string the spec names as fixed. DECISIONS says it matches the spec when it does not, so the golden test and the spec will disagree on the first export pytest. The spec is also internally inconsistent: R-EX-4(1) (spec:122) differs from the spec section 6 worked example (spec:273) and the golden file, which section 8's authority rule prefers. The architect followed the authority rule silently and mislabelled the source. Recorded as blocker because the card's stated spec alignment is false and the spec row check (section 8 row 3) fails as written; severity drops to major if Chris rules the golden text canonical and the spec row is amended.",
45	   "fix": "Get Chris's ruling (questions_for_chris[0]). Then keep one string. If R-EX-4(1) wins: change DECISIONS.md:204, the ADR-009 text, LLM_VS_CODE.md:103, spec/REQUIREMENTS.md:273 and golden sample.export.expected.txt:51 (qa owns the golden). If the section 6 / golden text wins: amend R-EX-4(1) at spec/REQUIREMENTS.md:122 and remove 'the fixed text of R-EX-4(1)' from DECISIONS.md:204. Do not keep the label unless the strings are equal.",
46	   "acceptance_test": "artifacts/review-evidence/T-028-review-checks.py AC5 PASS; the chosen sentence appears identically in spec, DECISIONS, LLM_VS_CODE and the golden file (grep -c equal in each); an export test compares the internal-notes block to the golden block byte for byte."},
47	  {"severity": "major",
48	   "title": "api.md sentence array splits 'Rx cyclobenzaprine 10 mg.' at the abbreviation, contradicting R-TL-2, D-021 and ADR-016",
49	   "evidence": "memory/contracts/api.md:91: '{\"text\": \"Rx cyclobenzaprine 10 mg.\", \"start\": 477, \"end\": 502}, {\"text\": \"Follow up with PCP in 1 week.\", \"start\": 503, \"end\": 532}'. memory/DECISIONS.md:285 says this exact sentence is one unit. Repro: artifacts/review-evidence/T-028-review-checks.py AC4b: api.md span [(477,502),(503,532)] vs R-TL-2 splitter span [(477,532)] on evals/golden/sample.txt record 2. This is the T-014 r3 M4 finding, which the card closes but the file still contradicts.",
50	   "why_it_matters": "api.md records[].sentences is the unit list the excerpt editor builds on (ADR-016). An implementer who copies this array lets an excerpt end at 'mg.', a fragment, which breaks the whole-sentence rule (R-TL-2) and the 'hedge travels with its finding' rule. The card AC3 evidence 'mg. one unit [477,532)' is contradicted by the file it cites.",
51	   "fix": "Replace api.md:91 with one unit: {\"text\": \"Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.\", \"start\": 477, \"end\": 532}; keep the 533-552 unit. Generate the example from the splitter output rather than by hand.",
52	   "acceptance_test": "AC4b in T-028-review-checks.py passes; a unit test runs the real sentence splitter on evals/golden/sample.txt record 2 and asserts equality with the sentences array in api.md (the test reads the array from api.md, so the example cannot drift)."},
53	  {"severity": "major",
54	   "title": "'Each with a flag template' is asserted, not shown: ADR-013 has no per-category template and the template module does not exist",
55	   "evidence": "memory/DECISIONS.md:258: 'Every category has a code template and a flag_type.' memory/DECISIONS.md:259: 'renders title and explanation from a template per category (app/backend/flag_templates.py; a unit test asserts every category has one), for example \"Wording that could be used to question causation...\"'. Only one template is worded. Repro: T-028-review-checks.py AC2b: 0 of 13 lexicon categories have template text in ADR-013. ls app/backend/flag_templates.py -> No such file or directory; ls app/backend -> empty.",
56	   "why_it_matters": "The 'every flag is code-rendered from a fixed template' rule (docs/LLM_VS_CODE.md row 14) is the control that stops the model writing causation wording. Categories such as recovery_context (strength low, never raises) and the lexicon-only categories have no wording anywhere in the design, so the backend would invent it. A generic sentence is not a template, and the card's 'each with a flag template' is not supported by the ADR.",
57	   "fix": "Add a table to ADR-013 with one template per category: the 13 lexicon categories plus the conflict, gap and record_warning codes it lists. Or check in app/backend/flag_templates.py as a key list equal to the closed category list and cite that file.",
58	   "acceptance_test": "T-028-review-checks.py AC2b reports 13 of 13 lexicon categories with explicit template text (or the template file's key set equals the closed list); a unit test asserts it."},
59	  {"severity": "major",
60	   "title": "Spec section 8 row 1 check cannot pass: the api.md export example abbreviates the notes block",
61	   "evidence": "spec/REQUIREMENTS.md:362-371 section 8 row 1: 'internal_notes_text should equal the golden notes block' with check 'diff of the example against evals/golden/sample.export.expected.txt (expect none)'. memory/contracts/api.md:272: '\"internal_notes_text\": \"INTERNAL REVIEW NOTES — DO NOT SEND\\n\\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]\"'. Repro: T-028-review-checks.py SPEC-8.1 FAIL.",
62	   "why_it_matters": "Replacing the copy with a pointer (card AC4) is the right call, and T-014 r3 m1 recommended it. But the spec row still demands an empty diff, so the spec and the card now disagree on how this is verified, and a reviewer following the spec will fail the doc. The choice has not been recorded in an ADR.",
63	   "fix": "Either amend spec section 8 row 1 to 'the example names the golden file; a pytest compares real export output with it' and record that in ADR-009, or embed the full block. Make the spec row and the example agree.",
64	   "acceptance_test": "The spec row's check command and the api.md example describe the same verification; a pytest asserts real export output equals evals/golden/sample.export.expected.txt."},
65	  {"severity": "minor",
66	   "title": "README-arch lexicon line lists v1 category names that lexicon v2 does not contain",
67	   "evidence": "app/README-arch.md:36: 'lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection'. Lexicon v2 entries[].category (13 names, yaml load) contains none of causation_weakening, compliance or hedge; accident_date_phrases, damages, non_encounter and injection are code_lists keys.",
68	   "why_it_matters": "A backend worker reading the architecture map would look for categories that do not exist. ADR-013 maps causation_weakening and compliance to causation; the README does not say so.",
69	   "fix": "Rewrite README-arch.md:36 as the 13 v2 category names plus the 4 code_lists keys, with a pointer to ADR-013.",
70	   "acceptance_test": "A grep or unit test: every name on README-arch.md:36 is in lexicon v2 categories or code_lists keys."},
71	  {"severity": "minor",
72	   "title": "confirm_date example clears a date_ambiguous warning that the golden case does not expect",
73	   "evidence": "memory/contracts/api.md:209: '\"removed_flag_ids\": [\"f_warn_date_r8\"]'. evals/golden/case_01_date_formats.expected.json: \"record_warnings\": [], \"flags\": [], \"gap_excluded_records\": [8]. Golden description: 'Ambiguous date must be marked ambiguous and surfaced for review.' evals/golden/README.md:61 record_warnings schema lists only instruction_like_text.",
74	   "why_it_matters": "The gap example is correct (gap_flags [] matches D-003 and golden). But the example refers to a warning the golden never expects, so either the golden is missing the date_ambiguous expectation or the example names a flag the pipeline is not required to create. Golden is the stated authority for expected outputs (spec section 8).",
75	   "fix": "qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden, or the architect rewrites the example to 'removed_flag_ids: [] (no warning in golden)' and records which one wins.",
76	   "acceptance_test": "check_golden.py asserts a date_ambiguous warning for case_01 record 8 (or the api example has no removed id not present in the golden)."},
77	  {"severity": "minor",
78	   "title": "AC3 evidence cites a count that no checked-in script produces",
79	   "evidence": "Card T-028 AC3 evidence: 'check script 14/14 blocks, 17/17 offsets'. Repro: grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches. The offsets themselves verify (sample.txt positions 396, 477, 503, 533 match api.md), but nothing prints the counts.",
80	   "why_it_matters": "A count with no script cannot be re-run by the next reviewer. The same claim covers the mg. offsets, which are wrong (finding 2).",
81	   "fix": "Check the offset and block script into artifacts/review-evidence/ and quote its output in the card; use the output, not a hand count.",
82	   "acceptance_test": "python3 -I artifacts/review-evidence/<script>.py exits 0 and prints the counts quoted in the card."},
83	  {"severity": "nit",
84	   "title": "AC4 evidence 'D-001..D-024 in all three docs' overstates the citations",
85	   "evidence": "Distinct D-ids: memory/DECISIONS.md 22 (no D-016, no D-023); memory/contracts/api.md 8 (D-001 D-003 D-010 D-012 D-013 D-020 D-022 D-024); docs/LLM_VS_CODE.md 2 (D-001, D-024). Every cited id resolves (T-028-review-checks.py AC8 PASS).",
86	   "why_it_matters": "The substance passes; the evidence sentence does not describe the files.",
87	   "fix": "Restate the evidence as 'every cited D-id resolves to a row in ORCHESTRATOR_DECISIONS (D-001..D-024)'.",
88	   "acceptance_test": "T-028-review-checks.py AC8 PASS (already true)."}
89	 ],
90	 "whats_right": [
91	   "SUMMARY_DROPS_QUALIFIER is present and consistent: api.md 1, DECISIONS.md 3, LLM_VS_CODE.md 1, matching R-TL-10(b) and D-022.",
92	   "ADR-013 names all 13 lexicon v2 categories, and the confirm_date example's gap_flags [] matches golden gap_excluded_records [8] and D-003 (phone note, not in gap math).",
93	   "The README-arch cut line keeps the per-record flag pass (README-arch.md:82), and money stays integer cents with the $185 rate outside the 839000 total (api.md:6, 124, 135)."
94	 ],
95	 "questions_for_chris": [
96	   "Which AI disclosure line is canonical: R-EX-4(1) ('AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export.' + 'Pending items: N.') or the section 6 / golden line ('This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.')? The spec currently has both.",
97	   "Should api.md embed the notes block (spec section 8 row 1 says diff expect none) or point to the golden file (card AC4 chose a pointer)?",
98	   "D-024 puts Tier-1 card reviews on sonnet. This review ran as claude-haiku-5-5. Accept it for mechanical doc passes, or re-run on sonnet?"
99	 ]}
100	```
101	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:26.543Z

**tool call — Bash**
````
{
 "command": "git log --oneline -5 2>&1; echo \"---\"; git show --stat 10cffcd 2>&1 | head -40; echo \"---\"; git status --short 2>&1 | head -20",
 "description": "Show recent commits, commit 10cffcd stats, and working tree status"
}
````

### User / tool · 2026-11-02T01:11:26.684Z

**tool result**
````
1e675ea chore(gate): M0 gate pass — harness complete (318 tests); T-003/T-006 closed
10cffcd docs(architect): T-028 r2 template table, mg. sentence unit
3ff15cd docs(spec): R-EX-4(1) AI line matches golden; T-015 closed
f454c41 docs(spec): T-025 closed; §6 notes block synced to golden; R-FL-4 references all golden must_nots
65537a4 fix(harness): debt entry no longer masks later fails; board-guard catches move-done in any arg order; M0 r3 closures
---
commit 10cffcd32259e7627f73602798c126043b562651
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:11:09 2026 -0600

    docs(architect): T-028 r2 template table, mg. sentence unit
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

 memory/DECISIONS.md     | 26 ++++++++++++++++++++++++++
 memory/contracts/api.md |  2 +-
 2 files changed, 27 insertions(+), 1 deletion(-)
---
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M board/activity.jsonl
 M board/cards/T-028.md
?? artifacts/review-evidence/
?? board/inbox/archive/20261102T005853430609Z.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:27.311Z

**tool call — Bash**
````
{
 "command": "grep -n \"drafted with AI assistance\" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt; echo \"EXIT=$?\"; echo \"---\"; grep -n \"AI assistance\" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt docs/LLM_VS_CODE.md memory/contracts/api.md; echo \"EXIT=$?\"",
 "description": "Check AI disclosure sentence consistency across the four files"
}
````

### User / tool · 2026-11-02T01:11:27.404Z

**tool result**
````
spec/REQUIREMENTS.md:122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
spec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
memory/DECISIONS.md:204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); includes "flagged language quoted in the letter" (D-012), "future treatment recommended (no cost stated)" (a code pattern on "recommend"), bills to request, records not in the treatment section, edited items with original and new text and any "keep my wording" confirmation.
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
EXIT=0
---
memory/DECISIONS.md:204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); includes "flagged language quoted in the letter" (D-012), "future treatment recommended (no cost stated)" (a code pattern on "recommend"), bills to request, records not in the treatment section, edited items with original and new text and any "keep my wording" confirmation.
evals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
spec/REQUIREMENTS.md:119:| R-EX-1 | **Treatment section (paste into letter)** contains accepted entries and accepted `charge` amounts only. It holds no tool-authored flag content: no flag note, type label, title, explanation, day count, count line or AI-assistance line. Record words appear only inside an accepted entry's excerpt or summary. | E2E: accept all 9 entries, both charges and all flags, add a reviewer note to the gap flag. Assert `letter_text` contains none of: the reviewer note text, "REVIEWER NOTE", any flag type label, any flag title or explanation string produced from `sample.expected.json`'s flags, "73 days", "AI assistance", or any count line. UT: every line of `letter_text` is a fixed heading, a date + provider heading, an entry summary, a `Source` line whose quote is a substring of the accepted excerpt, an amount line or the total line; the letter builder takes no flags argument. Set equality: with a chosen subset accepted, the item IDs in `letter_text` equal that subset. | E2E + UT |
spec/REQUIREMENTS.md:122:| R-EX-4 | **Internal review notes — do not send** contain these sections, in this order. Every record citation reads `record N (<provider as written>, <Month D, YYYY>)`. (1) AI-assistance line (D-009), fixed text: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." (matches the golden notes block; DECISIONS aligned on T-028) (2) Flags accepted, with evidence. (3) Flags dismissed, with any reason. (4) **Flagged language quoted in the letter**: each letter entry whose excerpt contains the evidence of a flag that is not dismissed, naming the flag type, so the attorney decides whether it goes out (D-012). (5) Amounts not totaled (accepted rate, estimate, unclear), worded as an action ("request itemized PT ledger"; "request clean copy of bill"). (6) Damages mentions that aren't charges, with excerpt. (7) **Future treatment recommended (no cost stated)**, from sentences matching a small code pattern list (it starts with "recommend"; extend by card), worded "request cost estimate". (8) **Bills to request**: one line, providers named by the label up to its first comma, in order of first appearance in the chronology, omitting any provider with an accepted charge, with " (itemized ledger)" appended when the provider has a non-dismissed rate. (9) Records not in the treatment section (R-EX-7). (10) Edited items, with original and new text and any "keep my wording" confirmation. (11) Pending items not included. | Sample, everything accepted (full text in §6): the notes list the gap, both conflicts, both prior mentions and the causation flags; entries 1, 4, 6, 7, 8, 9 under "flagged language quoted in the letter" (entry 1 because the accident-date conflict cites its "rear-ended" sentence) (record 3's 2023 low back sentence and record 7's intake-form sentence are not in the letter); the accident-date conflict citing records 1 and 2 (header date, no choice between dates, D-017) and record 7's intake line; the K5 causation item for record 7's intake line; the $185 rate with "request itemized PT ledger"; the record 5 damages mention; "Recommend cervical epidural steroid injection." from record 9; the bills-to-request line is exactly "Austin EMS run report; Dr. Alvarez; Capital PT (itemized ledger); Hill Country Pain Management." UT: every match of the case-insensitive pattern `record \d+` in `internal_notes_text` is followed by a parenthesis with a provider and a date. | UT + E2E |
spec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.
spec/REQUIREMENTS.md:370:| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
docs/LLM_VS_CODE.md:103:- **AI use is disclosed** on the review screen (a banner: summaries and flags are drafted by AI and checked by code, and she decides every item) and in the first line of the internal notes: "This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N." It is not in the letter; whether a firm discloses there is the firm's decision.
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:32.781Z

**tool call — Bash**
````
{
 "command": "git show 10cffcd -- memory/DECISIONS.md memory/contracts/api.md 2>&1",
 "description": "Show full diff of commit 10cffcd for DECISIONS and api.md"
}
````

### User / tool · 2026-11-02T01:11:32.877Z

**tool result**
````
commit 10cffcd32259e7627f73602798c126043b562651
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 19:11:09 2026 -0600

    docs(architect): T-028 r2 template table, mg. sentence unit
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>

diff --git a/memory/DECISIONS.md b/memory/DECISIONS.md
index f712fcb..de73117 100644
--- a/memory/DECISIONS.md
+++ b/memory/DECISIONS.md
@@ -255,6 +255,32 @@ review_events id, case_id, item_id, action('accept'|'edit'|'dismiss'|'reset'|'co
     - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
     - conflict: `treatment_plan_vs_actual`, `provider_name_variant`, `other_fact_mismatch` (LLM or code), `accident_date_after_treatment`, `accident_dates_differ` (code);
     - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
+    **Template table (design text; slots `{date}` long date, `{provider}` header label as written, `{quote}` verbatim excerpt, `{days}`, `{a}`/`{b}` for two sources):**
+
+    | Category | Title template | Explanation template |
+    |---|---|---|
+    | gap_over_30 | Gap of {days} days | Gap of {days} days between {date A} ({provider A}) and {date B} ({provider B}). |
+    | accident_date_after_treatment | Stated accident date is later than recorded treatment | Stated accident date {stated} (“{quote}”) is later than the first recorded treatment, {date} ({provider A}; {provider B}). The records disagree; the tool does not choose between them. |
+    | accident_dates_differ | Two different stated accident dates | {provider A} states {date A} (“{quote A}”); {provider B} states {date B} (“{quote B}”). The tool does not choose between them. |
+    | provider_name_variant | Provider name differs between records | {provider A} (“{quote A}”) and {provider B} (“{quote B}”) may name the same provider. |
+    | treatment_plan_vs_actual | Treatment plan and what followed differ | {provider A} ({date A}): “{quote A}”. {provider B} ({date B}): “{quote B}”. |
+    | other_fact_mismatch | Records differ on a fact | {provider A} ({date A}): “{quote A}”. {provider B} ({date B}): “{quote B}”. |
+    | pre_existing | Mention of a prior or pre-existing condition | {provider} ({date}) mentions a prior or pre-existing condition: “{quote}”. |
+    | degenerative_language | Degenerative wording | {provider} ({date}) uses degenerative wording: “{quote}”. |
+    | prior_surgery | Mention of prior surgery or repair | {provider} ({date}) mentions prior surgery or repair: “{quote}”. |
+    | speculative_language | Hedged wording | Wording that could be used to question causation in {provider} ({date}): “{quote}”. |
+    | patient_report | Patient self-report | Patient self-report (not a physician's opinion) in {provider} ({date}): “{quote}”. |
+    | missed_care | Missed or ended care | Wording about missed appointments or ending care in {provider} ({date}): “{quote}”. |
+    | new_onset | New-onset wording | New-onset wording in {provider} ({date}): “{quote}”. |
+    | scene_facts | Scene facts | Scene facts recorded by {provider} ({date}): “{quote}”. |
+    | alternative_cause | Possible other cause | Wording suggesting another cause in {provider} ({date}): “{quote}”. |
+    | litigation_referral | Attorney referral | Referral wording in {provider} ({date}): “{quote}”. |
+    | objective_negative | No objective findings noted | Wording about absent or normal findings in {provider} ({date}): “{quote}”. |
+    | recovery_context | (context only, never raises a flag) | n/a |
+    | accident_date_provenance | Accident date source | Accident date as stated in {provider} ({date}): “{quote}”. |
+    | date_ambiguous | Date to confirm | The date “{raw}” in {provider} can be read more than one way; choose one reading. |
+    | injection_suspected | Instruction-like text in a record | {provider} ({date}) contains instruction-like text: “{quote}”. It is shown unchanged and everything from this record needs review. |
+
     Every category has a code template and a flag_type. `recovery_context` entries have `strength: low` and never raise a flag (context only). Categories with no LLM prompt behind them are lexicon-only (origin `lexicon`, `LEXICON_ONLY`, `needs_review`) unless the per-record pass also finds them.
   - Code verifies the excerpt, computes offsets and renders `title` and `explanation` from a template per category (`app/backend/flag_templates.py`; a unit test asserts every category has one), for example "Wording that could be used to question causation in {source} ({date}): “{excerpt}”". Delay to first treatment is never computed (D-017).
   - `source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt and drives the "Patient self-report" label. Origin is `lexicon`, `llm` or `lexicon+llm`; one-sided hits are `needs_review` (`LEXICON_ONLY`, `LLM_ONLY`). Flags are not editable except a reviewer note.
diff --git a/memory/contracts/api.md b/memory/contracts/api.md
index be00c6a..8388d81 100644
--- a/memory/contracts/api.md
+++ b/memory/contracts/api.md
@@ -88,7 +88,7 @@ Read once, then patch local state from review responses. `entries` are **chronol
     { "id": "r2", "seq": 2, "source_label": "Central ER discharge summary", "date_iso": "2026-01-09", "date_status": "parsed",
       "date_candidates": [], "duplicate_of": null, "injection_tag": false, "encounter": true, "char_start": 315, "char_end": 553, "text": "=== Record 2 ===\n...",
       "sentences": [ {"text": "Dx: cervical strain;", "start": 396, "end": 416}, {"text": "concussion without loss of consciousness.", "start": 417, "end": 458}, {"text": "CT head negative.", "start": 459, "end": 476},
-                     {"text": "Rx cyclobenzaprine 10 mg.", "start": 477, "end": 502}, {"text": "Follow up with PCP in 1 week.", "start": 503, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
+                     {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
   "undated_entries": [],
   "entries": [
     { "id": "e2", "seq": 2, "record_ids": ["r2"], "date": "2026-01-09", "date_status": "parsed",
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:33.627Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport yaml\nd = yaml.safe_load(open('app/llm/lexicon.yaml'))\ncats = sorted({e['category'] for e in d['entries']})\nprint('version', d.get('version'), 'entries', len(d['entries']), 'distinct', len(cats))\nfor c in cats: print(c)\nprint('code_lists keys:', sorted(d.get('code_lists', {}).keys()))\n\" 2>&1; echo \"EXIT=$?\"",
 "description": "List lexicon v2 category names and code_lists keys"
}
````

### User / tool · 2026-11-02T01:11:33.802Z

**tool result**
````
version 2 entries 66 distinct 13
accident_date_provenance
alternative_cause
degenerative_language
litigation_referral
missed_care
new_onset
objective_negative
patient_report
pre_existing
prior_surgery
recovery_context
scene_facts
speculative_language
code_lists keys: ['accident_date_phrases', 'damages', 'injection', 'non_encounter']
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:47.689Z

**tool call — Bash**
````
{
 "command": "grep -n \"sample.export.expected.txt\" memory/contracts/api.md; echo \"EXIT=$?\"; echo \"---\"; grep -n \"internal_notes_text\" memory/contracts/api.md; echo \"---\"; sed -n '246,263p' memory/DECISIONS.md | cut -c1-400",
 "description": "Grep api.md for golden export reference and read ADR-013 closed list"
}
````

### User / tool · 2026-11-02T01:11:47.788Z

**tool result**
````
267:Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both charges and the flags accepted and nothing edited:
272:  "letter_text": "TREATMENT CHRONOLOGY\n\n[... nine entries with their Source lines and BILLED CHARGES: full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\n\nBilled charges stated in these records: $8,390.00",
EXIT=0
---
26:| GET | `/api/cases/{token}/export` | `letter_text` + `internal_notes_text` from accepted items |
273:  "internal_notes_text": "INTERNAL REVIEW NOTES — DO NOT SEND\n\n[... sections in R-EX-4 order: full text is the INTERNAL_NOTES_TEXT block of the golden file ...]",
---
## ADR-013 Flag text is rendered by code; the LLM returns a category and quoted spans only
- Status: accepted (round 2, amended round 3; D-007, D-013, D-018; resolves staff F8, R2-8)
- Context: flag explanations are where a model is most tempted to rule ("pre-existing degenerative disease"), which Appendix C forbids.
- Decision:
  - The flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation`, `record_warning` everywhere (D-013). `record_warning` flags are created by code only (categories `date_ambiguous`, `injection_suspected`).
  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on:
  - LLM flag passes run **per record** and return `{type, category, record_id, excerpt}`; the cross-record conflict pass returns `{category, a:{record_id, excerpt}, b:{...}}`. The schema rejects any extra prose field. `category` is from a closed list:
    The list equals the lexicon v2 category names (single vocabulary):
    - pre_existing: `pre_existing`, `degenerative_language`, `prior_surgery`;
    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
    - conflict: `treatment_plan_vs_actual`, `provider_name_variant`, `other_fact_mismatch` (LLM or code), `accident_date_after_treatment`, `accident_dates_differ` (code);
    - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
    **Template table (design text; slots `{date}` long date, `{provider}` header label as written, `{quote}` verbatim excerpt, `{days}`, `{a}`/`{b}` for two sources):**

    | Category | Title template | Explanation template |
    |---|---|---|
    | gap_over_30 | Gap of {days} days | Gap of {days} days between {date A} ({provider A}) and {date B} ({provider B}). |
    | accident_date_after_treatment | Stated accident date is later than recorded treatment | Stated accident date {stated} (“{quote}”) is later than the first recorded treatment, {date} ({provider A}; {provider B}). The records disagree; the tool does not choose between them. |
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:49.193Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\ns = open('evals/golden/sample.txt', encoding='utf-8').read()\nprint('len', len(s))\nprint('sample[477:532] =', repr(s[477:532]))\nprint('sample[477:502] =', repr(s[477:502]))\nprint('sample[502] =', repr(s[502]))\nprint('sample[503:532] =', repr(s[503:532]))\napi = open('memory/contracts/api.md', encoding='utf-8').read()\nunit = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'\nprint('api unit text present:', unit in api, '| sample span equals unit:', s[477:532] == unit)\nprint('old split present in api.md:', '\\\"Rx cyclobenzaprine 10 mg.\\\", \\\"start\\\": 477' in api)\n\" 2>&1; echo \"EXIT=$?\"; echo \"---\"; grep -n \"10 mg\" memory/contracts/api.md | cut -c1-300",
 "description": "Verify sample offsets and api.md mg. sentence unit against sample.txt"
}
````

### User / tool · 2026-11-02T01:11:49.304Z

**tool result**
````
len 1879
sample[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'
sample[477:502] = 'Rx cyclobenzaprine 10 mg.'
sample[502] = ' '
sample[503:532] = 'Follow up with PCP in 1 week.'
api unit text present: True | sample span equals unit: True
old split present in api.md: False
EXIT=0
---
91:                     {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER charges: $6,240.", "start": 533, "end": 552} ] } ],
96:      "summary": "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed; follow up with PCP in 1 week.",
98:      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.",
290:        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week."
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:52.969Z

**tool call — Bash**
````
{
 "command": "ls -la artifacts/review-evidence/ 2>&1; echo \"---\"; wc -l artifacts/review-evidence/T-028-review-checks.py 2>&1; echo \"---\"; .venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py 2>&1; echo \"EXIT=$?\"",
 "description": "Run round-1 mechanical check script against current files"
}
````

### User / tool · 2026-11-02T01:11:53.158Z

**tool result**
````
total 6552
drwxr-xr-x@ 177 arsis  staff    5664 Nov  1 19:09 .
drwxr-xr-x@   6 arsis  staff     192 Nov  1 18:20 ..
-rw-r--r--@   1 arsis  staff    5624 Nov  1 18:41 M0-r2-staff-resolution.md
-rw-r--r--@   1 arsis  staff    3998 Nov  1 18:17 T-001-exercise-1.txt
-rw-r--r--@   1 arsis  staff    4574 Nov  1 18:17 T-001-exercise-2.txt
-rw-r--r--@   1 arsis  staff    2738 Nov  1 18:23 T-001-exercise-3.txt
-rw-r--r--@   1 arsis  staff    3536 Nov  1 18:37 T-001-r2-readonly-repros.txt
-rw-r--r--@   1 arsis  staff    5099 Nov  1 18:59 T-001-r3-repro.out.txt
-rw-r--r--@   1 arsis  staff    4156 Nov  1 18:59 T-001-r3-repro.sh
-rw-r--r--@   1 arsis  staff   13729 Nov  1 18:22 T-002-curl.txt
-rw-r--r--@   1 arsis  staff  118831 Nov  1 18:42 T-002-r2-activity-390.png
-rw-r--r--@   1 arsis  staff   82140 Nov  1 18:42 T-002-r2-board-390.png
-rw-r--r--@   1 arsis  staff    1300 Nov  1 18:42 T-002-r2-csrf-curl.txt
-rw-r--r--@   1 arsis  staff   73730 Nov  1 18:42 T-002-r2-inbox-390.png
-rw-r--r--@   1 arsis  staff   80417 Nov  1 18:42 T-002-r2-milestones-390.png
-rw-r--r--@   1 arsis  staff   92057 Nov  1 18:42 T-002-r2-personas-390.png
-rw-r--r--@   1 arsis  staff   40406 Nov  1 18:42 T-002-r2-state-390.png
-rw-r--r--@   1 arsis  staff    1126 Nov  1 18:42 T-002-r2-xss.json
-rw-r--r--@   1 arsis  staff     488 Nov  1 19:00 T-002-r3-404.py
-rw-r--r--@   1 arsis  staff  116259 Nov  1 19:00 T-002-r3-activity-390.png
-rw-r--r--@   1 arsis  staff   80919 Nov  1 19:00 T-002-r3-board-390.png
-rw-r--r--@   1 arsis  staff   72782 Nov  1 19:00 T-002-r3-inbox-390.png
-rw-r--r--@   1 arsis  staff   80730 Nov  1 19:00 T-002-r3-milestones-390.png
-rw-r--r--@   1 arsis  staff   89842 Nov  1 19:00 T-002-r3-personas-390.png
-rw-r--r--@   1 arsis  staff    2910 Nov  1 19:00 T-002-r3-probe.out.txt
-rw-r--r--@   1 arsis  staff    3551 Nov  1 19:00 T-002-r3-probe.py
-rw-r--r--@   1 arsis  staff   97954 Nov  1 19:00 T-002-r3-state-390.png
-rw-r--r--@   1 arsis  staff    2132 Nov  1 19:00 T-002-r3-ui.out.txt
-rw-r--r--@   1 arsis  staff    1940 Nov  1 19:00 T-002-r3-ui.py
-rw-r--r--@   1 arsis  staff    1353 Nov  1 18:20 T-003-git-guard-commit-secret-probe.txt
-rw-r--r--@   1 arsis  staff   11736 Nov  1 18:17 T-003-git-guard-probe.txt
-rw-r--r--@   1 arsis  staff    5500 Nov  1 18:20 T-003-other-hooks-probe.txt
-rw-r--r--@   1 arsis  staff    1282 Nov  1 18:49 T-003-r2-commit-secret-probe.out.txt
-rw-r--r--@   1 arsis  staff    1792 Nov  1 18:49 T-003-r2-commit-secret-probe.py
-rw-r--r--@   1 arsis  staff   40696 Nov  1 18:39 T-003-r2-git-guard-results.txt
-rw-r--r--@   1 arsis  staff    8293 Nov  1 18:46 T-003-r2-probe-board2.out.txt
-rw-r--r--@   1 arsis  staff    6606 Nov  1 18:46 T-003-r2-probe-board2.py
-rw-r--r--@   1 arsis  staff   11627 Nov  1 18:39 T-003-r2-probe-corpus.txt
-rw-r--r--@   1 arsis  staff   24234 Nov  1 18:41 T-003-r2-probe-direct.out.txt
-rw-r--r--@   1 arsis  staff   24508 Nov  1 18:45 T-003-r2-probe-direct.out2.txt
-rw-r--r--@   1 arsis  staff   15783 Nov  1 18:41 T-003-r2-probe-direct.py
-rw-r--r--@   1 arsis  staff    8293 Nov  1 18:57 T-003-r3-probe-board2.out.txt
-rw-r--r--@   1 arsis  staff    9820 Nov  1 19:05 T-003-r3-probe-corpus.out.txt
-rw-r--r--@   1 arsis  staff    2129 Nov  1 18:56 T-003-r3-probe-corpus.py
-rw-r--r--@   1 arsis  staff   26955 Nov  1 19:06 T-003-r3-probe-direct.out.txt
-rw-r--r--@   1 arsis  staff     769 Nov  1 19:02 T-003-r3-probe-legit.out.txt
-rw-r--r--@   1 arsis  staff    3257 Nov  1 19:02 T-003-r3-probe-legit.py
-rw-r--r--@   1 arsis  staff     437 Nov  1 19:08 T-003-r3-probe-pwd.out.txt
-rw-r--r--@   1 arsis  staff     737 Nov  1 19:08 T-003-r3-probe-pwd.py
-rw-r--r--@   1 arsis  staff    5004 Nov  1 19:01 T-003-r3-probe-rwg.out.txt
-rw-r--r--@   1 arsis  staff    4720 Nov  1 19:01 T-003-r3-probe-rwg.py
-rw-r--r--@   1 arsis  staff   32357 Nov  1 19:06 T-003-r3-probe-targeted.out.txt
-rw-r--r--@   1 arsis  staff   17211 Nov  1 18:58 T-003-r3-probe-targeted.py
-rw-r--r--@   1 arsis  staff   22381 Nov  1 19:06 T-003-r3-probe-targeted2.out.txt
-rw-r--r--@   1 arsis  staff   13423 Nov  1 19:00 T-003-r3-probe-targeted2.py
-rw-r--r--@   1 arsis  staff     783 Nov  1 18:18 T-003-reviewer-write-guard-probe.txt
-rw-r--r--@   1 arsis  staff    3252 Nov  1 18:21 T-004-agent-check.txt
-rw-r--r--@   1 arsis  staff    1296 Nov  1 18:38 T-004-r2-agent-sync.txt
-rw-r--r--@   1 arsis  staff    2556 Nov  1 18:37 T-004-r2-board-guard-probe.py
-rw-r--r--@   1 arsis  staff    1985 Nov  1 18:37 T-004-r2-board-guard-probe.txt
-rw-r--r--@   1 arsis  staff     400 Nov  1 18:40 T-004-r2-shell-write-probe.txt
-rw-r--r--@   1 arsis  staff    4166 Nov  1 19:02 T-004-r3-board-guard-probe.out.txt
-rw-r--r--@   1 arsis  staff    4705 Nov  1 19:02 T-004-r3-board-guard-probe.py
-rw-r--r--@   1 arsis  staff    1269 Nov  1 18:36 T-005-r2-pathcheck.py
-rw-r--r--@   1 arsis  staff    3479 Nov  1 18:19 T-006-check-secrets-probe.txt
-rw-r--r--@   1 arsis  staff     457 Nov  1 18:46 T-006-r2-chain-probe.out.txt
-rw-r--r--@   1 arsis  staff    1299 Nov  1 18:46 T-006-r2-chain-probe.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 18:47 T-006-r2-fp-probe.out.txt
-rw-r--r--@   1 arsis  staff    1679 Nov  1 18:47 T-006-r2-fp-probe.py
-rw-r--r--@   1 arsis  staff   14186 Nov  1 18:44 T-006-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff   12661 Nov  1 18:44 T-006-r2-probe.py
-rw-r--r--@   1 arsis  staff     652 Nov  1 19:02 T-006-r3-chain-probe.out.txt
-rw-r--r--@   1 arsis  staff     323 Nov  1 19:03 T-006-r3-commit-paths-probe.out.txt
-rw-r--r--@   1 arsis  staff    2170 Nov  1 19:03 T-006-r3-commit-paths-probe.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 19:02 T-006-r3-fp-probe.out.txt
-rw-r--r--@   1 arsis  staff   14411 Nov  1 19:02 T-006-r3-probe.out.txt
-rw-r--r--@   1 arsis  staff     266 Nov  1 18:21 T-006-rename-probe.txt
-rw-r--r--@   1 arsis  staff    3095 Nov  1 18:36 T-008-adjuster-source-checks.txt
-rw-r--r--@   1 arsis  staff    5000 Nov  1 18:53 T-008-r2-adjuster.md
drwxr-xr-x@   6 arsis  staff     192 Nov  1 18:52 T-008-r2-src
-rw-r--r--@   1 arsis  staff    4018 Nov  1 18:58 T-008-r3-adjuster-greps.txt
-rw-r--r--@   1 arsis  staff    4470 Nov  1 18:59 T-008-r3-adjuster-hits.md
-rw-r--r--@   1 arsis  staff  103085 Nov  1 18:58 T-008-r3-insurancejournal-854959.html
-rw-r--r--@   1 arsis  staff    5686 Nov  1 18:58 T-008-r3-insurancejournal-checks.txt
-rw-r--r--@   1 arsis  staff    7118 Nov  1 18:33 T-009-adjuster-probes.py
-rw-r--r--@   1 arsis  staff    7919 Nov  1 18:33 T-009-adjuster-probes.txt
-rw-r--r--@   1 arsis  staff    3506 Nov  1 18:34 T-009-nurse-golden-scan.txt
-rw-r--r--@   1 arsis  staff   10773 Nov  1 18:34 T-009-nurse-probe-output.txt
-rw-r--r--@   1 arsis  staff    1912 Nov  1 18:34 T-009-nurse-probe.py
-rw-r--r--@   1 arsis  staff    5508 Nov  1 18:34 T-009-nurse-probes.txt
-rw-r--r--@   1 arsis  staff   27892 Nov  1 18:55 T-009-r2-nurse-probe-output.txt
-rw-r--r--@   1 arsis  staff    9224 Nov  1 18:55 T-009-r2-nurse-probe.py
-rw-r--r--@   1 arsis  staff    2111 Nov  1 18:56 T-009-r2-nurse-variants-output.txt
-rw-r--r--@   1 arsis  staff    2729 Nov  1 18:56 T-009-r2-nurse-variants.py
-rw-r--r--@   1 arsis  staff    8083 Nov  1 18:58 T-009-r2-resolution.md
-rw-r--r--@   1 arsis  staff   17929 Nov  1 18:32 T-010-011-sections.txt
-rw-r--r--@   1 arsis  staff   11927 Nov  1 18:41 T-010-011-source-check.md
-rw-r--r--@   1 arsis  staff   10370 Nov  1 18:36 T-010-litlead-source-check.md
-rw-r--r--@   1 arsis  staff    1134 Nov  1 18:45 T-010-r2-count.py
-rw-r--r--@   1 arsis  staff    9595 Nov  1 18:46 T-010-r2-resolution.md
-rw-r--r--@   1 arsis  staff     601 Nov  1 18:43 T-010-r2-srch.py
-rw-r--r--@   1 arsis  staff    2065 Nov  1 18:52 T-010-r3-check.py
-rw-r--r--@   1 arsis  staff    4370 Nov  1 18:53 T-010-r3-resolution.md
-rw-r--r--@   1 arsis  staff    1898 Nov  1 18:38 T-011-r2-check.py
-rw-r--r--@   1 arsis  staff     958 Nov  1 18:32 T-012-h2t.py
-rw-r--r--@   1 arsis  staff    1886 Nov  1 18:52 T-012-r2-fetch.py
-rw-r--r--@   1 arsis  staff    4598 Nov  1 18:55 T-012-r2-resolution.md
-rw-r--r--@   1 arsis  staff    7818 Nov  1 18:35 T-012-source-check.md
-rw-r--r--@   1 arsis  staff   12757 Nov  1 18:23 T-013-paralegal-walkthrough.md
-rw-r--r--@   1 arsis  staff     710 Nov  1 18:34 T-013-r2-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    4411 Nov  1 18:31 T-013-r2-paralegal-walk.out.txt
-rw-r--r--@   1 arsis  staff    4557 Nov  1 18:31 T-013-r2-paralegal-walk.py
-rw-r--r--@   1 arsis  staff    6010 Nov  1 18:33 T-013-r2-resolution.md
-rw-r--r--@   1 arsis  staff     667 Nov  1 18:44 T-013-r3-paralegal-golden-cmp.out.txt
-rw-r--r--@   1 arsis  staff    1583 Nov  1 18:44 T-013-r3-paralegal-golden-cmp.py
-rw-r--r--@   1 arsis  staff     824 Nov  1 18:46 T-013-r3-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    4221 Nov  1 18:44 T-013-r3-paralegal-walk.out.txt
-rw-r--r--@   1 arsis  staff    8007 Nov  1 18:44 T-013-r3-paralegal-walk.py
-rw-r--r--@   1 arsis  staff    2857 Nov  1 18:45 T-013-r3-resolution.md
-rw-r--r--@   1 arsis  staff    2868 Nov  1 18:44 T-013-r3check.py
-rw-r--r--@   1 arsis  staff   23496 Nov  1 18:46 T-013-trace.md
-rw-r--r--@   1 arsis  staff    1235 Nov  1 18:27 T-014-amount-cue-demo.py
-rw-r--r--@   1 arsis  staff    6372 Nov  1 18:28 T-014-injection-trace.md
-rw-r--r--@   1 arsis  staff     376 Nov  1 18:23 T-014-json-check.out
-rw-r--r--@   1 arsis  staff     793 Nov  1 18:23 T-014-json-check.py
-rw-r--r--@   1 arsis  staff    7761 Nov  1 18:43 T-014-r2-amount-demo.py
-rw-r--r--@   1 arsis  staff    1371 Nov  1 18:46 T-014-r2-amount-sim.out
-rw-r--r--@   1 arsis  staff    1738 Nov  1 18:46 T-014-r2-amount-sim.py
-rw-r--r--@   1 arsis  staff     317 Nov  1 18:46 T-014-r2-json-check.out
-rw-r--r--@   1 arsis  staff    1522 Nov  1 18:46 T-014-r2-offset-check.out
-rw-r--r--@   1 arsis  staff    1351 Nov  1 18:46 T-014-r2-offset-check.py
-rw-r--r--@   1 arsis  staff   10089 Nov  1 18:45 T-014-r2-privacy-resolution.md
-rw-r--r--@   1 arsis  staff    6747 Nov  1 18:47 T-014-r2-staff-resolution.md
-rw-r--r--@   1 arsis  staff    3549 Nov  1 18:56 T-014-r3-amount-demo.out
-rw-r--r--@   1 arsis  staff    5551 Nov  1 18:56 T-014-r3-amount-demo.py
-rw-r--r--@   1 arsis  staff    1313 Nov  1 18:56 T-014-r3-amount-sim.out
-rw-r--r--@   1 arsis  staff    3719 Nov  1 18:56 T-014-r3-amount-sim.py
-rw-r--r--@   1 arsis  staff    9266 Nov  1 18:59 T-014-r3-resolution.md
-rw-r--r--@   1 arsis  staff    6710 Nov  1 18:26 T-014-walkthrough.md
-rw-r--r--@   1 arsis  staff   10226 Nov  1 18:29 T-015-legal-nurse-items.md
-rw-r--r--@   1 arsis  staff    7988 Nov  1 18:27 T-015-paralegal-blind.md
-rw-r--r--@   1 arsis  staff    1484 Nov  1 18:30 T-015-paralegal-regex-probe.out.txt
-rw-r--r--@   1 arsis  staff    2319 Nov  1 18:30 T-015-paralegal-regex-probe.py
-rw-r--r--@   1 arsis  staff    8869 Nov  1 18:47 T-015-r2-nurse-probe.out.txt
-rw-r--r--@   1 arsis  staff   10444 Nov  1 18:47 T-015-r2-nurse-probe.py
-rw-r--r--@   1 arsis  staff   10177 Nov  1 18:49 T-015-r2-nurse.md
-rw-r--r--@   1 arsis  staff     632 Nov  1 18:48 T-015-r2-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff   13119 Nov  1 18:45 T-015-r2-paralegal-probe.out.txt
-rw-r--r--@   1 arsis  staff    8982 Nov  1 18:45 T-015-r2-paralegal-probe.py
-rw-r--r--@   1 arsis  staff    3370 Nov  1 18:47 T-015-r2-paralegal.md
-rw-r--r--@   1 arsis  staff    3417 Nov  1 18:58 T-015-r3-paralegal-entries.out.txt
-rw-r--r--@   1 arsis  staff    1547 Nov  1 18:58 T-015-r3-paralegal-entries.py
-rw-r--r--@   1 arsis  staff     789 Nov  1 19:03 T-015-r3-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff     649 Nov  1 19:00 T-015-r3-paralegal-mutation.out.txt
-rw-r--r--@   1 arsis  staff    1145 Nov  1 19:00 T-015-r3-paralegal-mutation.py
-rw-r--r--@   1 arsis  staff    8956 Nov  1 19:00 T-015-r3-paralegal-probe.out.txt
-rw-r--r--@   1 arsis  staff    8196 Nov  1 19:00 T-015-r3-paralegal-probe.py
-rw-r--r--@   1 arsis  staff    9429 Nov  1 18:57 T-015-r3-paralegal-rerun-of-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff    2288 Nov  1 18:58 T-015-r3-paralegal-s6diff.out.txt
-rw-r--r--@   1 arsis  staff     772 Nov  1 18:58 T-015-r3-paralegal-s6diff.py
-rw-r--r--@   1 arsis  staff    9710 Nov  1 18:59 T-015-r3-rerun-of-r2-nurse-probe.out.txt
-rw-r--r--@   1 arsis  staff     194 Nov  1 19:08 T-015-r4-paralegal-jsoncheck.out.txt
-rw-r--r--@   1 arsis  staff    1125 Nov  1 19:08 T-015-r4-paralegal-jsoncheck.py
-rw-r--r--@   1 arsis  staff    2130 Nov  1 19:07 T-015-r4-paralegal-recheck.out.txt
-rw-r--r--@   1 arsis  staff    5440 Nov  1 19:07 T-015-r4-paralegal-recheck.py
-rw-r--r--@   1 arsis  staff    1217 Nov  1 18:58 T-025-pm-probe.out.txt
-rw-r--r--@   1 arsis  staff    1581 Nov  1 18:58 T-025-pm-probe.py
-rw-r--r--@   1 arsis  staff    1691 Nov  1 19:04 T-025-pm-r2-probe.out.txt
-rw-r--r--@   1 arsis  staff    1120 Nov  1 19:04 T-025-pm-r2-probe.py
-rw-r--r--@   1 arsis  staff  271072 Nov  1 19:03 T-026-desktop-dialog.png
-rw-r--r--@   1 arsis  staff  265680 Nov  1 19:03 T-026-desktop-office.png
-rw-r--r--@   1 arsis  staff  112324 Nov  1 19:03 T-026-mobile-dialog.png
-rw-r--r--@   1 arsis  staff  265502 Nov  1 19:03 T-026-mobile-office.png
-rw-r--r--@   1 arsis  staff    3151 Nov  1 19:03 T-026-ux-designer-office.py
-rw-r--r--@   1 arsis  staff    8723 Nov  1 19:08 T-028-review-checks.py
-rw-r--r--@   1 arsis  staff    1076 Nov  1 19:09 T-028-review-json-check.py
drwxr-xr-x@   3 arsis  staff      96 Nov  1 18:56 __pycache__
---
     175 artifacts/review-evidence/T-028-review-checks.py
---
PASS AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md
    memory/contracts/api.md: 1
    memory/DECISIONS.md: 3
    docs/LLM_VS_CODE.md: 1
PASS AC2 every lexicon v2 category name appears in ADR-013
    lexicon categories (13): ['accident_date_provenance', 'alternative_cause', 'degenerative_language', 'litigation_referral', 'missed_care', 'new_onset', 'objective_negative', 'patient_report', 'pre_existing', 'prior_surgery', 'recovery_context', 'scene_facts', 'speculative_language']
    missing from ADR-013: []
FAIL AC2 each lexicon category has a flag template stated in ADR-013
    categories with a per-category template in ADR-013: 0 of 13 []
    only template statements are generic: DECISIONS.md lines containing 'template': [243, 260]
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
    api.md:91 sentences for the same span: [(477, 532), (533, 552)]
    splitter units for the same span:     [(477, 532), (533, 552)]
FAIL AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text
    R-EX-4(1) text present in DECISIONS.md: False
    R-EX-4(1) text present in spec §6 worked example: False
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
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:11:56.991Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-review-checks.py"
}
````

### User / tool · 2026-11-02T01:11:57.000Z

**tool result**
````
1	#!/usr/bin/env python3
2	"""T-028 mechanical checks (staff-engineer-reviewer). Read-only; no network.
3	
4	Run from repo root:  .venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py
5	Prints one PASS/FAIL line per check with the evidence it compared.
6	"""
7	import re
8	import sys
9	from pathlib import Path
10	
11	import yaml
12	
13	ROOT = Path(__file__).resolve().parents[2]
14	results = []
15	
16	
17	def check(name, ok, evidence):
18	    results.append(ok)
19	    print(("PASS " if ok else "FAIL ") + name)
20	    for line in evidence:
21	        print("    " + line)
22	
23	
24	def read(rel):
25	    return (ROOT / rel).read_text(encoding="utf-8")
26	
27	
28	# 1. SUMMARY_DROPS_QUALIFIER presence (AC1)
29	counts = {f: read(f).count("SUMMARY_DROPS_QUALIFIER")
30	          for f in ["memory/contracts/api.md", "memory/DECISIONS.md", "docs/LLM_VS_CODE.md"]}
31	check("AC1 SUMMARY_DROPS_QUALIFIER in api.md, DECISIONS.md, LLM_VS_CODE.md",
32	      all(v >= 1 for v in counts.values()), [f"{k}: {v}" for k, v in counts.items()])
33	
34	# 2. Lexicon v2 categories all named in ADR-013 (AC2, names only)
35	lex = yaml.safe_load(read("app/llm/lexicon.yaml"))
36	lex_cats = sorted({e["category"] for e in lex["entries"]})
37	dec = read("memory/DECISIONS.md")
38	m = re.search(r"^## ADR-013.*?(?=^## ADR-014)", dec, re.S | re.M)
39	adr13 = m.group(0) if m else ""
40	missing = [c for c in lex_cats if not re.search(r"\b" + re.escape(c) + r"\b", adr13)]
41	check("AC2 every lexicon v2 category name appears in ADR-013",
42	      bool(adr13) and not missing,
43	      [f"lexicon categories ({len(lex_cats)}): {lex_cats}", f"missing from ADR-013: {missing}"])
44	
45	# 2b. Per-category flag template text in ADR-013 (AC2 'with a template')
46	# the generic sentence "Every category has a code template" is an assertion, not a per-category template
47	adr13_specific = "\n".join(l for l in adr13.splitlines() if "Every category has a code template" not in l)
48	per_cat = {c: bool(re.search(r"\b" + re.escape(c) + r"\b[^\n]{0,120}template|template[^\n]{0,120}\b" + re.escape(c) + r"\b", adr13_specific))
49	           for c in lex_cats}
50	check("AC2 each lexicon category has a flag template stated in ADR-013",
51	      all(per_cat.values()),
52	      ["categories with a per-category template in ADR-013: %d of %d %s" % (sum(per_cat.values()), len(lex_cats), sorted(c for c, ok in per_cat.items() if ok)),
53	       "only template statements are generic: DECISIONS.md lines containing 'template': %s" % [i + 1 for i, l in enumerate(dec.splitlines()) if 'template' in l and 'ADR-013' not in l and 240 < i + 1 < 262],
54	       "app/backend/flag_templates.py exists: %s" % (ROOT / "app/backend/flag_templates.py").exists()])
55	
56	# 3. Phone note (record 8) not in gap math in the confirm_date example (AC3a)
57	api = read("memory/contracts/api.md")
58	sect = re.search(r"^## POST /api/cases/\{token\}/records/\{rid\}/confirm_date.*?(?=^## )", api, re.S | re.M)
59	sect = sect.group(0) if sect else ""
60	gap_empty = '"gap_flags": []' in sect
61	check("AC3a confirm_date example gap_flags empty for phone note r8",
62	      gap_empty and "encounter\": false" not in sect,
63	      ['api.md confirm_date example contains "gap_flags": [] : %s' % gap_empty])
64	
65	# 4. date_invalid only non-candidate code (AC3b)
66	noncand = [l for l in api.splitlines() if re.search(r"non-candidate|not one of the record", l)]
67	check("AC3b date_invalid is the only code for a non-candidate date",
68	      all("date_invalid" in l for l in noncand) and len(noncand) >= 1,
69	      ["lines naming non-candidate dates: %d" % len(noncand)] + [l[:160] for l in noncand])
70	
71	# 5. mg. treated as abbreviation: apply R-TL-2 splitter to sample record 2 and compare api.md units
72	sample = read("evals/golden/sample.txt")
73	hdr = sample.index("=== Record 2 ===")
74	q0 = sample.index('Excerpt: "', hdr) + len('Excerpt: "')
75	q1 = sample.index('"', q0)
76	body = sample[q0:q1]
77	ABBR = {"approx", "Dr", "Mr", "Mrs", "Ms", "vs", "etc", "e.g", "i.e", "mg"}
78	
79	
80	def split_units(text, base):
81	    units, start, i, n = [], 0, 0, len(text)
82	    while i < n:
83	        ch = text[i]
84	        term = False
85	        if ch in ".?!":
86	            tok = re.search(r"([A-Za-z.]+)$", text[:i + 1])
87	            word = tok.group(1).rstrip(".") if tok else ""
88	            is_abbr = ch == "." and word in ABBR
89	            in_number = i > 0 and text[i - 1].isdigit() and i + 1 < n and text[i + 1].isdigit()
90	            if not is_abbr and not in_number:
91	                if i + 1 >= n:
92	                    term = True
93	                elif text[i + 1].isspace():
94	                    rest = text[i + 1:].lstrip()
95	                    term = (not rest) or rest[0].isupper() or rest[0].isdigit()
96	        elif ch == ";":
97	            term = True
98	        if term:
99	            units.append((base + start, base + i + 1))
100	            start = i + 1
101	        i += 1
102	    if start < n and text[start:].strip():
103	        units.append((base + start, base + n))
104	    # trim leading whitespace from each unit
105	    fixed = []
106	    for s, e in units:
107	        while s < e and sample[s].isspace():
108	            s += 1
109	        fixed.append((s, e))
110	    return fixed
111	
112	
113	mine = split_units(body, q0)
114	api_units = [(477, 502), (503, 532)]
115	sent_block = re.search(r'"sentences": \[(.*?)\] \}', api, re.S)
116	api_list = re.findall(r'"start": (\d+), "end": (\d+)', sent_block.group(1)) if sent_block else []
117	api_list = [(int(a), int(b)) for a, b in api_list]
118	span_mine = [u for u in mine if 470 <= u[0] <= 540]
119	mg_rule_ok = (477, 532) in mine
120	check("AC4a splitter rule: 'mg.' is not a terminator (R-TL-2, D-021), one unit for record 2 span 477-532",
121	      mg_rule_ok,
122	      ["R-TL-2 splitter on sample record 2 (absolute offsets): %s" % mine,
123	       "units in span per splitter: %s" % span_mine])
124	api_span = [u for u in api_list if 470 <= u[0] <= 540]
125	check("AC4b api.md example treats 'mg.' as abbreviation (sentences list agrees with splitter)",
126	      api_span == [(477, 532)],
127	      ["api.md:91 sentences for the same span: %s" % api_span,
128	       "splitter units for the same span:     %s" % span_mine])
129	
130	# 6. AI line: R-EX-4(1) fixed text vs DECISIONS vs golden (AC5)
131	spec = read("spec/REQUIREMENTS.md")
132	r_ex4_1 = "AI assistance: this chronology was drafted with AI assistance and every item was reviewed by the paralegal before export."
133	line_dec = [l for l in dec.splitlines() if "AI assistance" in l]
134	golden_ai = [l for l in read("evals/golden/sample.export.expected.txt").splitlines() if "AI assistance" in l]
135	check("AC5 DECISIONS.md AI line equals R-EX-4(1) fixed text",
136	      r_ex4_1 in dec,
137	      ["R-EX-4(1) text present in DECISIONS.md: %s" % (r_ex4_1 in dec),
138	       "R-EX-4(1) text present in spec §6 worked example: %s" % (r_ex4_1 in spec),
139	       "golden INTERNAL_NOTES line: %s" % (golden_ai[0][:140] if golden_ai else "none"),
140	       "DECISIONS.md:204 quotes: 'This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.'"])
141	
142	# 7. api.md export example references the golden file (AC6)
143	check("AC6 api.md export example references evals/golden/sample.export.expected.txt",
144	      "evals/golden/sample.export.expected.txt" in api,
145	      ["count in api.md: %d" % api.count("evals/golden/sample.export.expected.txt")])
146	
147	# 8. Spec §8 row 1 check: diff of export example against golden expects none
148	abbreviated = "full text is the INTERNAL_NOTES_TEXT block" in api
149	check("SPEC-8.1 api.md export example equals golden notes block (spec §8 row 1 check: 'expect none')",
150	      not abbreviated,
151	      ["api.md export example abbreviates the notes block: %s" % abbreviated,
152	       "so 'diff against golden' cannot be empty as spec §8 row 1 requires"])
153	
154	# 9. Cut line keeps per-record flag pass (AC7)
155	readme = read("app/README-arch.md")
156	cut = readme.split("## Cut line", 1)[1]
157	check("AC7 README-arch cut line does not list the per-record flag pass as cut",
158	      "per-record flag pass is not on the cut line" in cut and "per-record flag pass folded" not in cut,
159	      ["cut-line sentence present: %s" % ("per-record flag pass is not on the cut line" in cut)])
160	
161	# 10. D-ids cited resolve to ORCHESTRATOR_DECISIONS rows (AC8)
162	orch = read("memory/ORCHESTRATOR_DECISIONS.md")
163	defined = set(re.findall(r"^\| (D-0\d{2}) \|", orch, re.M))
164	cited = set()
165	for f in ["memory/DECISIONS.md", "memory/contracts/api.md", "docs/LLM_VS_CODE.md", "app/README-arch.md"]:
166	    cited |= set(re.findall(r"D-0\d{2}", read(f)))
167	check("AC8 every D-id cited in the four docs is defined (D-001..D-024)",
168	      cited <= defined,
169	      ["defined: %d (%s..%s)" % (len(defined), min(defined), max(defined)),
170	       "cited but undefined: %s" % sorted(cited - defined),
171	       "D-ids cited in DECISIONS.md: %s" % sorted(set(re.findall(r"D-0\d{2}", dec)))])
172	
173	print()
174	print("SUMMARY: %d/%d checks passed" % (sum(results), len(results)))
175	sys.exit(0 if all(results) else 1)
176	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:08.310Z

**tool call — Bash**
````
{
 "command": "sed -n '360,366p' spec/REQUIREMENTS.md | cut -c1-500; echo \"--- README-arch:36\"; sed -n '36p' app/README-arch.md; echo \"--- api.md confirm_date\"; grep -n \"removed_flag_ids\\|gap_flags\" memory/contracts/api.md | cut -c1-250; echo \"--- counts\"; grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/ 2>&1 | head -5; echo \"grep EXIT=$?\"; echo \"--- commits touching the four docs since de749c2\"; git log --oneline de749c2..HEAD -- memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md app/README-arch.md spec/REQUIREMENTS.md evals/golden/ 2>&1",
 "description": "Check spec section 8 row 1, README-arch, api.md confirm_date, and commit history"
}
````

### User / tool · 2026-11-02T01:12:08.448Z

**tool result**
````
- Recommended future treatment is a specials item the firm will want costed; the notes surface it (R-EX-4).

### Reconciliation status

Everything above follows `memory/ORCHESTRATOR_DECISIONS.md` (D-001 to D-024). **Authority rule:** `evals/golden/*` is the authority on expected outputs, and this file matches it. §6 block 2 equals the golden `INTERNAL_NOTES_TEXT` block and §6 block 1 equals `LETTER_TEXT`; the writer asks qa for no golden changes. `memory/contracts/api.md` and `memory/DECISIONS.md` are the authority for the API and are aligned to this file and the golden by the architect on **T-028**. Each row has a grep that s

| # | File | Difference | Check | Owner |
--- README-arch:36
  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
--- api.md confirm_date
59:  "gap_flags": ["f_gap_r6_r7"], "record_warning_flags": [],
208:  "gap_flags": [],
209:  "removed_flag_ids": ["f_warn_date_r8"],
212:`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): con
--- counts
grep EXIT=0
--- commits touching the four docs since de749c2
1e675ea chore(gate): M0 gate pass — harness complete (318 tests); T-003/T-006 closed
10cffcd docs(architect): T-028 r2 template table, mg. sentence unit
3ff15cd docs(spec): R-EX-4(1) AI line matches golden; T-015 closed
f454c41 docs(spec): T-025 closed; §6 notes block synced to golden; R-FL-4 references all golden must_nots
65537a4 fix(harness): debt entry no longer masks later fails; board-guard catches move-done in any arg order; M0 r3 closures
0c03c4f fix(evals): golden r3 fixes - both-sides accident conflict, self_report_spans key, R-EX-4 AI line, tighter flag matching
4cc0f81 docs(spec): golden is authority for exports; section 8 owners updated
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:08.842Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-028 2>&1 | head -80; echo \"EXIT=${PIPESTATUS[0]}\"",
 "description": "Show board card T-028 with acceptance criteria"
}
````

### User / tool · 2026-11-02T01:12:08.973Z

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
updated_at: "2026-11-02T01:11:23Z"
claimed_by: "architect"
claimed_at: "2026-11-02T01:10:57Z"
rounds: 1
commits: ["de749c2", "10cffcd"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-028-staff-engineer.md", "at": "2026-11-02T01:10:46Z"}
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
- 2026-11-02T01:10:46Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-028-staff-engineer.md; round 1; findings:
    - [blocker] DECISIONS AI line is not the R-EX-4(1) fixed text, and ADR-009 says it is — fix: Get Chris's ruling (questions_for_chris[0]). Then keep one string. If R-EX-4(1) wins: change DECISIONS.md:204, the ADR-009 text, LLM_VS_CODE.md:103, spec/REQUIREMENTS.md:273 and golden sample.export.expected.txt:51 (qa owns the golden). If the section 6 / golden text wins: amend R-EX-4(1) at spec/REQUI
    - [major] api.md sentence array splits 'Rx cyclobenzaprine 10 mg.' at the abbreviation, contradicting R-TL-2, D-021 and ADR-016 — fix: Replace api.md:91 with one unit: {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}; keep the 533-552 unit. Generate the example from the splitter output rather than by hand.
    - [major] 'Each with a flag template' is asserted, not shown: ADR-013 has no per-category template and the template module does not exist — fix: Add a table to ADR-013 with one template per category: the 13 lexicon categories plus the conflict, gap and record_warning codes it lists. Or check in app/backend/flag_templates.py as a key list equal to the closed category list and cite that file.
    - [major] Spec section 8 row 1 check cannot pass: the api.md export example abbreviates the notes block — fix: Either amend spec section 8 row 1 to 'the example names the golden file; a pytest compares real export output with it' and record that in ADR-009, or embed the full block. Make the spec row and the example agree.
    - [minor] README-arch lexicon line lists v1 category names that lexicon v2 does not contain — fix: Rewrite README-arch.md:36 as the 13 v2 category names plus the 4 code_lists keys, with a pointer to ADR-013.
    - [minor] confirm_date example clears a date_ambiguous warning that the golden case does not expect — fix: qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden, or the architect rewrites the example to 'removed_flag_ids: [] (no warning in golden)' and records which one wins.
    - [minor] AC3 evidence cites a count that no checked-in script produces — fix: Check the offset and block script into artifacts/review-evidence/ and quote its output in the card; use the output, not a hand count.
- 2026-11-02T01:10:46Z orchestrator: Triage: the 'blocker' (two AI lines) is stale; grep shows REQUIREMENTS:273, DECISIONS:204 and golden:51 carry the same line after 3ff15cd. Real items: ADR-013 per-category flag templates; api.md:91 mg. split vs D-021. §8 row 1 check rewritten by orchestrator.
- 2026-11-02T01:10:47Z orchestrator: assigned: architect
- 2026-11-02T01:10:57Z architect: claimed
- 2026-11-02T01:11:07Z architect: moved in_progress -> in_review
- 2026-11-02T01:11:23Z orchestrator: review dispatched: haiku r2

## Handoff
Round 2: ADR-013 template table (one title/explanation per category, slots {date}/{provider}/{quote}); api.md record-2 sentences regenerated (mg. abbreviation, one unit [477,532)); check script 14/14 blocks, 17/17 offsets.

EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:12.479Z

**tool call — Bash**
````
{
 "command": "sed -n '366,372p' spec/REQUIREMENTS.md | cut -c1-700; echo \"--- ADR-009 / LLM_VS_CODE golden line\"; grep -n \"SUMMARY_DROPS_QUALIFIER\" memory/DECISIONS.md | cut -c1-120; echo \"--- api.md:209-212 confirm_date\"; sed -n '199,212p' memory/contracts/api.md | cut -c1-400; echo \"--- golden remaining\"; grep -n \"date_ambiguous\\|record_warnings\" evals/golden/case_01_date_formats.expected.json | head; echo \"--- ADR-013 template-table rows count\"; awk '/^## ADR-013/,/^## ADR-014/' memory/DECISIONS.md | grep -c '^    | [a-z_]* |'",
 "description": "Read spec section 8 rows, golden warnings, and count ADR-013 template rows"
}
````

### User / tool · 2026-11-02T01:12:12.606Z

**tool result**
````
| # | File | Difference | Check | Owner |
|---|---|---|---|---|
| 1 | `memory/contracts/api.md` export example | The example references `evals/golden/sample.export.expected.txt` instead of copying it (one source of truth). | `grep -n "sample.export.expected.txt" memory/contracts/api.md` (expect ≥ 1) | T-028 | resolved |
| 2 | `memory/contracts/api.md` reason codes | No `SUMMARY_DROPS_QUALIFIER` (D-022, R-TL-10(b)); `EXCERPT_OMITS_QUALIFIER` reads "the record has a hedge sentence the excerpt leaves out", D-021 limits it to a hedge that qualifies a selected sentence. | `grep -c "SUMMARY_DROPS_QUALIFIER" memory/contracts/api.md` (expect 1 or more) | T-028 (architect) |
| 3 | `memory/contracts/api.md` / `memory/DECISIONS.md` | `confirm_date` with a non-candidate date must be `422 date_invalid`; the AI line in DECISIONS must match R-EX-4(1); the gap example for a phone note must follow D-003 (excluded from gap math). | `grep -n "date_invalid" memory/contracts/api.md`; `grep -n "AI assistance" memory/DECISIONS.md`; `grep -n "phone" memory/contracts/api.md memory/DECISIONS.md` | T-028 (architect) |
| 4 | `evals/golden/README.md`, `sample.expected.json` | Golden uses `source_kind: patient_self_report` and checks `required_terms` on summary+excerpt; D-022 and R-FL-7/R-TL-10 say `patient_report` and summary alone. Not a request to qa: the orchestrator records which wins, and the loser is edited by its owner. | `grep -n "patient_self_report\|summary+excerpt" evals/golden/README.md` | orchestrator (D-entry) |
| 5 | M3 paralegal review brief (orchestrator, T-018/M3 gate) | `scores.verify_quickly` (D-015) must be requested in the brief. | `grep -c "verify_quickly" .claude/agents/paralegal-reviewer.md` (expect 1 or more) | T-016 (orchestrator) |
--- ADR-009 / LLM_VS_CODE golden line
147:    - **needs_review**: any doubt, with reasons listed. Includes: judge verdict other than the positive one (partial
244:- **Dropped qualifiers (D-022, round 4).** A second function `grounding.dropped_qualifiers(summary, excerpt)` finds 
335:  12. **qa items.** Golden variant E (above); `required_terms` checked against the summary alone and R-TL-10 gains S
--- api.md:209-212 confirm_date
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
`422 date_invalid` when the date is not one of the record's candidates; `422 invalid_edit` when the record's date is not ambiguous. Logged as a `confirm_date` event. The example is golden `case_01` record 8, a phone note (`encounter: false`): confirming its date moves the entry onto the timeline but changes no gap math, so `gap_flags` is empty. For an encounter record, `gap_flags` lists the recomp
--- golden remaining
315:  "record_warnings": [],
--- ADR-013 template-table rows count
20
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:51.716Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-checks.py",
 "content": "#!/usr/bin/env python3\n\"\"\"T-028 round-2 mechanical checks (staff-engineer-reviewer). Read-only; no network.\n\nRun from repo root:  .venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py\nReplaces the round-1 script for the round-2 review. The round-1 script\n(T-028-review-checks.py) had two defects that this script corrects:\n  - AC4b compared api.md against the constant [(477,532)] but its span filter\n    (470..540) also catches the 533-552 unit, so it could never pass.\n  - AC5 searched for the pre-3ff15cd R-EX-4(1) wording, which no longer exists.\nPrints one PASS/FAIL line per check with the evidence it compared.\n\"\"\"\nimport re\nimport sys\nfrom pathlib import Path\n\nimport yaml\n\nROOT = Path(__file__).resolve().parents[2]\nresults = []\n\n\ndef check(name, ok, evidence):\n    results.append(bool(ok))\n    print((\"PASS \" if ok else \"FAIL \") + name)\n    for line in evidence:\n        print(\"    \" + line)\n\n\ndef read(rel):\n    return (ROOT / rel).read_text(encoding=\"utf-8\")\n\n\ndec = read(\"memory/DECISIONS.md\")\napi = read(\"memory/contracts/api.md\")\nspec = read(\"spec/REQUIREMENTS.md\")\nllm = read(\"docs/LLM_VS_CODE.md\")\ngolden_export = read(\"evals/golden/sample.export.expected.txt\")\nsample = read(\"evals/golden/sample.txt\")\n\n# ---- C1. AI disclosure sentence: one canonical wording in all four places ----\nAI_RE = (r\"This chronology was drafted with AI assistance; every item in the treatment section \"\n         r\"was accepted by the paralegal\\. Items not reviewed: (?:N|\\d+)\\.\")\nhits = {\n    \"spec/REQUIREMENTS.md\": len(re.findall(AI_RE, spec)),\n    \"memory/DECISIONS.md\": len(re.findall(AI_RE, dec)),\n    \"docs/LLM_VS_CODE.md\": len(re.findall(AI_RE, llm)),\n    \"evals/golden/sample.export.expected.txt\": len(re.findall(AI_RE, golden_export)),\n}\nold_variant = \"AI assistance: this chronology was drafted with AI assistance and every item was reviewed\"\nstale = {f: read(f).count(old_variant) for f in [\"spec/REQUIREMENTS.md\", \"memory/DECISIONS.md\",\n                                                  \"docs/LLM_VS_CODE.md\", \"evals/golden/sample.export.expected.txt\"]}\ncheck(\"C1 AI line: same canonical sentence in spec, DECISIONS, LLM_VS_CODE and golden; no old variant\",\n      all(v >= 1 for v in hits.values()) and not any(stale.values()),\n      [\"canonical sentence matches per file: %s\" % hits,\n       \"old R-EX-4(1) variant matches per file: %s\" % stale])\n\n# ---- C2. ADR-013 template table vs lexicon v2 categories ----\nlex = yaml.safe_load(read(\"app/llm/lexicon.yaml\"))\nlex_cats = sorted({e[\"category\"] for e in lex[\"entries\"]})\nm = re.search(r\"^## ADR-013.*?(?=^## ADR-014)\", dec, re.S | re.M)\nadr13 = m.group(0) if m else \"\"\nrows = {}\nfor line in adr13.splitlines():\n    if not re.match(r\"^\\s*\\|\", line):\n        continue\n    cells = [c.strip() for c in line.strip().strip(\"|\").split(\"|\")]\n    if len(cells) == 3 and cells[0] not in (\"Category\",) and not set(cells[0]) <= set(\"-\"):\n        rows[cells[0]] = cells[1:]\nno_row = [c for c in lex_cats if c not in rows]\nblank = [c for c in lex_cats if c in rows and (not rows[c][1] or rows[c][1] == \"n/a\")]\ncheck(\"C2a every lexicon v2 category has a template-table row in ADR-013\",\n      not no_row,\n      [\"lexicon categories: %d; rows in table: %d\" % (len(lex_cats), len(rows)),\n       \"lexicon categories with no row: %s\" % no_row,\n       \"lexicon categories whose explanation is blank or n/a: %s\" % blank])\n\nADR_CODES = [\"treatment_plan_vs_actual\", \"other_fact_mismatch\", \"accident_date_after_treatment\",\n             \"accident_dates_differ\", \"provider_name_variant\", \"gap_over_30\", \"date_ambiguous\",\n             \"injection_suspected\"]\nmissing_codes = [c for c in ADR_CODES if c not in rows]\ncheck(\"C2b every conflict, gap and record_warning code named in ADR-013 has a row\",\n      not missing_codes,\n      [\"codes with no row: %s\" % missing_codes])\n\n# placeholders used in the table vs the legend stated above it\nlegend_line = [l for l in adr13.splitlines() if \"slots\" in l]\nlegend = set(re.findall(r\"`\\{(\\w+)\\}`\", legend_line[0])) if legend_line else set()\nlegend |= {\"a\", \"b\"} if \"{a}\" in \" \".join(legend_line) else set()\nused = set()\nfor cells in rows.values():\n    for cell in cells:\n        used |= set(re.findall(r\"\\{([^}]+)\\}\", cell))\ndeclared = {\"date\", \"provider\", \"quote\", \"days\", \"a\", \"b\"}\nundeclared = sorted(used - declared)\ncheck(\"C2c every placeholder in the template table is declared in the slot legend\",\n      not undeclared,\n      [\"slot legend (as written): %s\" % sorted(legend),\n       \"placeholders used in table: %s\" % sorted(used),\n       \"used but not declared: %s\" % undeclared])\n\n# the example sentence below the table uses different slot names\nexample = re.search(r\"for example \\\"(Wording that could be used[^\\\"]*)\\\"\", adr13)\nex_slots = sorted(set(re.findall(r\"\\{(\\w+)\\}\", example.group(1)))) if example else []\ncheck(\"C2d the example template under the table uses the same slot names as the table\",\n      ex_slots and set(ex_slots) <= declared,\n      [\"example slots: %s\" % ex_slots,\n       \"example text: %s\" % (example.group(1)[:120] if example else \"not found\")])\n\n# ---- C3. api.md record 2 sentences vs R-TL-2 splitter (mg. is not a terminator) ----\nhdr = sample.index(\"=== Record 2 ===\")\nq0 = sample.index('Excerpt: \"', hdr) + len('Excerpt: \"')\nq1 = sample.index('\"', q0)\nbody = sample[q0:q1]\nABBR = {\"approx\", \"Dr\", \"Mr\", \"Mrs\", \"Ms\", \"vs\", \"etc\", \"e.g\", \"i.e\", \"mg\"}\n\n\ndef split_units(text, base):\n    units, start, i, n = [], 0, 0, len(text)\n    while i < n:\n        ch = text[i]\n        term = False\n        if ch in \".?!\":\n            tok = re.search(r\"([A-Za-z.]+)$\", text[:i + 1])\n            word = tok.group(1).rstrip(\".\") if tok else \"\"\n            is_abbr = ch == \".\" and word in ABBR\n            in_number = i > 0 and text[i - 1].isdigit() and i + 1 < n and text[i + 1].isdigit()\n            if not is_abbr and not in_number:\n                if i + 1 >= n:\n                    term = True\n                elif text[i + 1].isspace():\n                    rest = text[i + 1:].lstrip()\n                    term = (not rest) or rest[0].isupper() or rest[0].isdigit()\n        elif ch == \";\":\n            term = True\n        if term:\n            units.append((base + start, base + i + 1))\n            start = i + 1\n        i += 1\n    if start < n and text[start:].strip():\n        units.append((base + start, base + n))\n    fixed = []\n    for s, e in units:\n        while s < e and sample[s].isspace():\n            s += 1\n        fixed.append((s, e))\n    return fixed\n\n\nmine = split_units(body, q0)\nsent_block = re.search(r'\"id\": \"r2\".*?\"sentences\": \\[(.*?)\\] \\} \\]', api, re.S)\napi_pairs = re.findall(r'\"text\": \"((?:[^\"\\\\]|\\\\.)*)\", \"start\": (\\d+), \"end\": (\\d+)', sent_block.group(1)) if sent_block else []\napi_list = [(int(s), int(e)) for _, s, e in api_pairs]\napi_text_ok = all(sample[int(s):int(e)] == t for t, s, e in api_pairs)\ncheck(\"C3a api.md record 2 sentences equal the R-TL-2 splitter output on sample record 2\",\n      api_list == mine,\n      [\"splitter units (absolute): %s\" % mine,\n       \"api.md units (absolute):    %s\" % api_list])\ncheck(\"C3b each api.md sentence text equals sample.txt[start:end] exactly\",\n      api_text_ok and len(api_pairs) > 0,\n      [\"api.md sentence count for record 2: %d\" % len(api_pairs),\n       \"sample[477:532] = %r\" % sample[477:532]])\n\n# ---- C4. golden reference from api.md (architect's r2 grep) ----\ng = api.count(\"sample.export.expected.txt\")\ncheck(\"C4 api.md references evals/golden/sample.export.expected.txt (grep count >= 1)\",\n      g >= 1,\n      [\"count: %d\" % g])\n\n# ---- C5. spec section 8 row 1 check now matches the api.md example ----\nrow1 = [l for l in spec.splitlines() if l.startswith(\"| 1 | `memory/contracts/api.md` export example\")]\ncheck(\"C5 spec section 8 row 1 check is 'expect >= 1' (not 'expect none') and api.md satisfies it\",\n      bool(row1) and \"expect ≥ 1\" in row1[0] and g >= 1,\n      [\"row 1: %s\" % (row1[0][:260] if row1 else \"not found\")])\n\n# ---- C6. README-arch lexicon line uses lexicon v2 names ----\nreadme = read(\"app/README-arch.md\")\nv1_names = [n for n in [\"causation_weakening\", \"compliance\", \"hedge\", \"accident_date_phrases\", \"damages\", \"non_encounter\", \"injection\"]\n            if re.search(r\"\\b\" + n + r\"\\b\", readme.split(\"lexicon.yaml\")[1].split(\"\\n\")[0])] if \"lexicon.yaml\" in readme else []\ncheck(\"C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys\",\n      not v1_names,\n      [\"v1-only names still on the lexicon line: %s\" % v1_names])\n\n# ---- C7. confirm_date example removes a date_ambiguous warning the golden does not expect ----\nimport json\ngold = json.loads(read(\"evals/golden/case_01_date_formats.expected.json\"))\nrec8_warn = [w for w in gold.get(\"record_warnings\", []) if str(w.get(\"record_id\", \"\")) in (\"8\", \"r8\")]\ncheck(\"C7 api.md confirm_date removed_flag_ids (f_warn_date_r8) has a matching golden expectation\",\n      bool(rec8_warn),\n      [\"golden case_01 record_warnings for record 8: %s\" % rec8_warn,\n       \"golden record_warnings total: %d\" % len(gold.get(\"record_warnings\", []))])\n\n# ---- C8. AC3 evidence count reproducible from a checked-in script ----\nhits_count = sum(len(re.findall(r\"14/14|17/17\", read(f))) for f in\n                 [\"memory/DECISIONS.md\", \"memory/contracts/api.md\", \"docs/LLM_VS_CODE.md\", \"app/README-arch.md\"])\ncheck(\"C8 card AC3 evidence '14/14 blocks, 17/17 offsets' appears in a checked-in script or doc\",\n      hits_count > 0,\n      [\"matches for 14/14 or 17/17 in the four docs: %d\" % hits_count])\n\nprint()\nprint(\"SUMMARY: %d/%d checks passed\" % (sum(results), len(results)))\nsys.exit(0 if all(results) else 1)\n"
}
````

### User / tool · 2026-11-02T01:12:51.837Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-checks.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:53.883Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py 2>&1; echo \"EXIT=$?\"",
 "description": "Run round-2 mechanical check script"
}
````

### User / tool · 2026-11-02T01:12:54.060Z

**tool result**
````
PASS C1 AI line: same canonical sentence in spec, DECISIONS, LLM_VS_CODE and golden; no old variant
    canonical sentence matches per file: {'spec/REQUIREMENTS.md': 2, 'memory/DECISIONS.md': 1, 'docs/LLM_VS_CODE.md': 1, 'evals/golden/sample.export.expected.txt': 1}
    old R-EX-4(1) variant matches per file: {'spec/REQUIREMENTS.md': 0, 'memory/DECISIONS.md': 0, 'docs/LLM_VS_CODE.md': 0, 'evals/golden/sample.export.expected.txt': 0}
PASS C2a every lexicon v2 category has a template-table row in ADR-013
    lexicon categories: 13; rows in table: 21
    lexicon categories with no row: []
    lexicon categories whose explanation is blank or n/a: ['recovery_context']
PASS C2b every conflict, gap and record_warning code named in ADR-013 has a row
    codes with no row: []
FAIL C2c every placeholder in the template table is declared in the slot legend
    slot legend (as written): ['a', 'b', 'date', 'days', 'provider', 'quote']
    placeholders used in table: ['date', 'date A', 'date B', 'days', 'provider', 'provider A', 'provider B', 'quote', 'quote A', 'quote B', 'raw', 'stated']
    used but not declared: ['date A', 'date B', 'provider A', 'provider B', 'quote A', 'quote B', 'raw', 'stated']
FAIL C2d the example template under the table uses the same slot names as the table
    example slots: ['date', 'excerpt', 'source']
    example text: Wording that could be used to question causation in {source} ({date}): “{excerpt}”
PASS C3a api.md record 2 sentences equal the R-TL-2 splitter output on sample record 2
    splitter units (absolute): [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
    api.md units (absolute):    [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
PASS C3b each api.md sentence text equals sample.txt[start:end] exactly
    api.md sentence count for record 2: 5
    sample[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'
PASS C4 api.md references evals/golden/sample.export.expected.txt (grep count >= 1)
    count: 2
PASS C5 spec section 8 row 1 check is 'expect >= 1' (not 'expect none') and api.md satisfies it
    row 1: | 1 | `memory/contracts/api.md` export example | The example references `evals/golden/sample.export.expected.txt` instead of copying it (one source of truth). | `grep -n "sample.export.expected.txt" memory/contracts/api.md` (expect ≥ 1) | T-028 | resolved |
FAIL C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys
    v1-only names still on the lexicon line: ['causation_weakening', 'compliance', 'hedge', 'accident_date_phrases', 'damages', 'non_encounter', 'injection']
FAIL C7 api.md confirm_date removed_flag_ids (f_warn_date_r8) has a matching golden expectation
    golden case_01 record_warnings for record 8: []
    golden record_warnings total: 0
FAIL C8 card AC3 evidence '14/14 blocks, 17/17 offsets' appears in a checked-in script or doc
    matches for 14/14 or 17/17 in the four docs: 0

SUMMARY: 7/12 checks passed
EXIT=1
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:12:58.939Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\ng = json.load(open('evals/golden/case_01_date_formats.expected.json'))\nprint('top-level keys:', sorted(g.keys()))\nfor k in g:\n    if 'record' in k and k != 'record_warnings':\n        v = g[k]\n        print(k, type(v).__name__, (len(v) if hasattr(v,'__len__') else v))\n\" 2>&1; echo \"EXIT=$?\"; echo \"---\"; grep -n '\"date_ambiguous\"\\|date_ambiguous' evals/golden/case_01_date_formats.expected.json evals/golden/README.md | head -5; echo \"grep EXIT=$?\"; echo \"--- README-arch lexicon line tokens\"; grep -n \"lexicon.yaml\" app/README-arch.md | cut -c1-200; echo \"--- mg. occurrences in the four docs + spec\"; grep -n \"10 mg\\.\" memory/DECISIONS.md memory/contracts/api.md docs/LLM_VS_CODE.md spec/REQUIREMENTS.md | cut -c1-160",
 "description": "Inspect golden case_01 warnings and remaining mg. occurrences"
}
````

### User / tool · 2026-11-02T01:12:59.087Z

**tool result**
````
top-level keys: ['amounts', 'case_id', 'description', 'entries', 'expected_entry_count', 'flags', 'gap_excluded_records', 'gap_table', 'input_file', 'must_not', 'must_not_flag', 'notes', 'record_warnings', 'records', 'schema_version', 'stress_types', 'synthetic', 'tolerated', 'totals']
records list 8
gap_excluded_records list 1
EXIT=0
---
grep EXIT=0
--- README-arch lexicon line tokens
36:  lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
78:`app/llm/lexicon.yaml` v2 (researcher): `flag_type`, `hedge`, `self_report`, `strength`, plus the `accident_date_phrases`, `non_encounter` and `injection` categories. It blocks the gap rule, the ac
--- mg. occurrences in the four docs + spec
spec/REQUIREMENTS.md:228:Source [Ex. __ / Bates __]: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg.
memory/contracts/api.md:91:                     {"text": "Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.", "start": 477, "end": 532}, {"text": "ER char
memory/contracts/api.md:98:      "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow u
memory/contracts/api.md:290:        "excerpt": "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follo
memory/DECISIONS.md:311:  - **One sentence splitter**, the one defined in R-TL-2 (that requirement's terminator rule and abbreviation list, which includes `appr
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:02.406Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\ng = json.load(open('evals/golden/case_01_date_formats.expected.json'))\nfor r in g['records']:\n    if str(r.get('seq', r.get('id'))) in ('8',) or r.get('id') in ('8','r8') or r.get('seq')==8:\n        print(json.dumps(r)[:600])\nprint('gap_excluded_records', g['gap_excluded_records'])\nprint('description', g['description'][:300])\n\" 2>&1; echo \"EXIT=$?\"",
 "description": "Show golden case_01 record 8 fields"
}
````

### User / tool · 2026-11-02T01:13:02.513Z

**tool result**
````
gap_excluded_records [8]
description Seven distinct date formats plus one genuinely ambiguous numeric date (04/05/2026: April 5 or May 4) on a phone note. Ambiguous date must be marked ambiguous, excluded from gap math, and surfaced for review. A future date inside an excerpt (04/14/2026) is not a record date.
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:04.274Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json\ng = json.load(open('evals/golden/case_01_date_formats.expected.json'))\nr = g['records']\nprint(type(r[0]).__name__, json.dumps(r[-1])[:700])\nprint('flags:', json.dumps(g['flags'])[:300])\n\" 2>&1; echo \"EXIT=$?\"; echo \"--- golden checker\"; .venv/bin/python -I evals/golden/check_golden.py 2>&1 | tail -3; echo \"EXIT=$?\"",
 "description": "Show golden record 8 structure and run golden checker"
}
````

### User / tool · 2026-11-02T01:13:04.431Z

**tool result**
````
dict {"record_no": 8, "raw_date": "04/05/2026", "date": null, "kind": "phone_note", "source": "Dr. Orla Pennywhistle, phone note"}
flags: []
EXIT=0
--- golden checker
golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:08.450Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-checks.py",
 "old_string": "readme = read(\"app/README-arch.md\")\nv1_names = [n for n in [\"causation_weakening\", \"compliance\", \"hedge\", \"accident_date_phrases\", \"damages\", \"non_encounter\", \"injection\"]\n            if re.search(r\"\\b\" + n + r\"\\b\", readme.split(\"lexicon.yaml\")[1].split(\"\\n\")[0])] if \"lexicon.yaml\" in readme else []\ncheck(\"C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys\",\n      not v1_names,\n      [\"v1-only names still on the lexicon line: %s\" % v1_names])",
 "new_string": "readme = read(\"app/README-arch.md\")\nallowed = set(lex_cats) | set(lex.get(\"code_lists\", {}).keys()) | {\"hedge_flag_booleans\"}\nlex_line = [l for l in readme.splitlines() if \"categories:\" in l and \"lexicon.yaml\" in l]\nlisted = re.findall(r\"[a-z_]+\", lex_line[0].split(\"categories:\", 1)[1]) if lex_line else []\nv1_names = sorted({n for n in listed if n not in allowed})\ncheck(\"C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys\",\n      bool(lex_line) and not v1_names,\n      [\"README-arch lexicon line: %s\" % (lex_line[0].strip()[:200] if lex_line else \"not found\"),\n       \"names on that line not in lexicon v2 categories or code_lists keys: %s\" % v1_names])"
}
````

### User / tool · 2026-11-02T01:13:08.552Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-checks.py has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:10.268Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py 2>&1; echo \"EXIT=$?\"; echo \"--- r1 script (for the record)\"; .venv/bin/python -I artifacts/review-evidence/T-028-review-checks.py 2>&1 | grep -E \"^(PASS|FAIL)|SUMMARY\"; echo \"--- board validate\"; python3 tools/board.py validate 2>&1 | tail -2; echo \"EXIT=${PIPESTATUS[0]}\"",
 "description": "Rerun round-2 checks, round-1 checks summary, and board validate"
}
````

### User / tool · 2026-11-02T01:13:10.599Z

**tool result**
````
PASS C1 AI line: same canonical sentence in spec, DECISIONS, LLM_VS_CODE and golden; no old variant
    canonical sentence matches per file: {'spec/REQUIREMENTS.md': 2, 'memory/DECISIONS.md': 1, 'docs/LLM_VS_CODE.md': 1, 'evals/golden/sample.export.expected.txt': 1}
    old R-EX-4(1) variant matches per file: {'spec/REQUIREMENTS.md': 0, 'memory/DECISIONS.md': 0, 'docs/LLM_VS_CODE.md': 0, 'evals/golden/sample.export.expected.txt': 0}
PASS C2a every lexicon v2 category has a template-table row in ADR-013
    lexicon categories: 13; rows in table: 21
    lexicon categories with no row: []
    lexicon categories whose explanation is blank or n/a: ['recovery_context']
PASS C2b every conflict, gap and record_warning code named in ADR-013 has a row
    codes with no row: []
FAIL C2c every placeholder in the template table is declared in the slot legend
    slot legend (as written): ['a', 'b', 'date', 'days', 'provider', 'quote']
    placeholders used in table: ['date', 'date A', 'date B', 'days', 'provider', 'provider A', 'provider B', 'quote', 'quote A', 'quote B', 'raw', 'stated']
    used but not declared: ['date A', 'date B', 'provider A', 'provider B', 'quote A', 'quote B', 'raw', 'stated']
FAIL C2d the example template under the table uses the same slot names as the table
    example slots: ['date', 'excerpt', 'source']
    example text: Wording that could be used to question causation in {source} ({date}): “{excerpt}”
PASS C3a api.md record 2 sentences equal the R-TL-2 splitter output on sample record 2
    splitter units (absolute): [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
    api.md units (absolute):    [(396, 416), (417, 458), (459, 476), (477, 532), (533, 552)]
PASS C3b each api.md sentence text equals sample.txt[start:end] exactly
    api.md sentence count for record 2: 5
    sample[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'
PASS C4 api.md references evals/golden/sample.export.expected.txt (grep count >= 1)
    count: 2
PASS C5 spec section 8 row 1 check is 'expect >= 1' (not 'expect none') and api.md satisfies it
    row 1: | 1 | `memory/contracts/api.md` export example | The example references `evals/golden/sample.export.expected.txt` instead of copying it (one source of truth). | `grep -n "sample.export.expected.txt" memory/contracts/api.md` (expect ≥ 1) | T-028 | resolved |
FAIL C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys
    README-arch lexicon line: lexicon.yaml     [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection
    names on that line not in lexicon v2 categories or code_lists keys: ['causation_weakening', 'compliance', 'hedge']
FAIL C7 api.md confirm_date removed_flag_ids (f_warn_date_r8) has a matching golden expectation
    golden case_01 record_warnings for record 8: []
    golden record_warnings total: 0
FAIL C8 card AC3 evidence '14/14 blocks, 17/17 offsets' appears in a checked-in script or doc
    matches for 14/14 or 17/17 in the four docs: 0

SUMMARY: 7/12 checks passed
EXIT=1
--- r1 script (for the record)
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
--- board validate
ok (28 file(s))
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:24.141Z

**tool call — Bash**
````
{
 "command": "ls tests/unit 2>&1 | head -3; echo \"---\"; grep -rln \"sample.export.expected\" tests/ app/ 2>&1 | head -3; echo \"grep EXIT=$?\"; echo \"--- ADR-009 mentions of golden/pytest\"; awk '/^## ADR-009/,/^## ADR-010/' memory/DECISIONS.md | grep -n \"golden\\|pytest\\|export\" | cut -c1-220; echo \"--- api.md 267 and 272 full\"; sed -n '267p' memory/contracts/api.md | cut -c1-400; echo \"--- spec row 1 cell count\"; sed -n '363p' spec/REQUIREMENTS.md | awk -F'|' '{print NF-2\" cells\"}'; sed -n '362p' spec/REQUIREMENTS.md | awk -F'|' '{print NF-2\" header cells\"}'",
 "description": "Check for export golden test, ADR-009 recording, and spec table shape"
}
````

### User / tool · 2026-11-02T01:13:24.267Z

**tool result**
````
---
grep EXIT=0
--- ADR-009 mentions of golden/pytest
1:## ADR-009 Export: two blocks; the template of record is REQUIREMENTS section 6 and the golden file
3:- Context: the flags (gaps, conflicts, pre-existing conditions, causation wording) are what an adjuster would use against the client, so they are for the paralegal and attorney, not the letter. Ship bar 1 requires ever
4:- Decision: `GET /api/cases/{token}/export` returns code-assembled `letter_text` and `internal_notes_text` from items with `review_status in (accepted, edited)` only. **The exact format is `spec/REQUIREMENTS.md` §6 (R
5:  - Letter: entries as `<Month D, YYYY> — <provider as written>`, summary, then `Source [Ex. __ / Bates __]: "<verbatim excerpt>"`; `BILLED CHARGES` with `<provider as written>, <long date>: $X.XX` plus its source li
8:  - There is no citation toggle. Output is byte-deterministic for the same accepted set. The sample equals the golden file only on the `fixture` backend, whose recorded summaries are the golden summaries (qa and backen
--- api.md 267 and 272 full
Built by code from items with `review_status` in (`accepted`, `edited`) only (ADR-009). No parameters. **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** The example is the sample case with all 9 entries, both char
--- spec row 1 cell count
-2 cells
-1 header cells
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:28.966Z

**tool call — Bash**
````
{
 "command": "echo \"--- pytest\"; .venv/bin/python -m pytest tests/unit -q 2>&1 | tail -3; echo \"PYTEST_EXIT=${PIPESTATUS[0]}\"; echo \"--- CLI\"; .venv/bin/python -m app.pipeline evals/golden/sample.txt 2>&1 | tail -2; echo \"CLI_EXIT=${PIPESTATUS[0]}\"; echo \"--- golden export refs in tests/app (count)\"; grep -rl \"sample.export.expected\" tests app 2>/dev/null | wc -l; echo \"--- tests dir listing\"; find tests -type f 2>/dev/null | head -5; echo \"find_count=$(find tests -type f 2>/dev/null | wc -l)\"; echo \"--- app/backend listing\"; ls -A app/backend 2>&1",
 "description": "Run unit tests, pipeline CLI, and check for export golden references in code"
}
````

### User / tool · 2026-11-02T01:13:29.401Z

**tool result**
````
--- pytest

no tests ran in 0.00s
PYTEST_EXIT=5
--- CLI
/Users/arsis/zlayt-pm-project/.venv/bin/python: No module named app.pipeline
CLI_EXIT=1
--- golden export refs in tests/app (count)
       0
--- tests dir listing
find_count=       0
--- app/backend listing
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:42.224Z

**tool call — Bash**
````
{
 "command": "grep -n \"^## ADR-009\" memory/DECISIONS.md; awk '/^## ADR-009/,/^## ADR-010/' memory/DECISIONS.md | sed -n '4p' | cut -c1-900; echo \"--- spec row 1 line\"; grep -n '^| 1 | `memory/contracts/api.md` export example' spec/REQUIREMENTS.md | cut -c1-20; echo \"--- ADR-013 template-table location and nominal line numbers\"; grep -n \"Template table (design text\\|^    | recovery_context\\|^    | gap_over_30\\|^    | injection_suspected\\|Every category has a code template\" memory/DECISIONS.md | cut -c1-80; echo \"--- D-024 text\"; grep -n \"^| D-024 \" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-300",
 "description": "Locate ADR-009 decision line, spec row 1, ADR-013 table rows, and D-024"
}
````

### User / tool · 2026-11-02T01:13:42.421Z

**tool result**
````
199:## ADR-009 Export: two blocks; the template of record is REQUIREMENTS section 6 and the golden file
- Decision: `GET /api/cases/{token}/export` returns code-assembled `letter_text` and `internal_notes_text` from items with `review_status in (accepted, edited)` only. **The exact format is `spec/REQUIREMENTS.md` §6 (R-EX-4, R-EX-6) and is checked in as `evals/golden/sample.export.expected.txt`; the golden file is authoritative and this ADR does not restate it.** What this ADR fixes:
--- spec row 1 line
368:| 1 | `memory/co
--- ADR-013 template-table location and nominal line numbers
258:    **Template table (design text; slots `{date}` long date, `{provider}` he
262:    | gap_over_30 | Gap of {days} days | Gap of {days} days between {date A}
279:    | recovery_context | (context only, never raises a flag) | n/a |
282:    | injection_suspected | Instruction-like text in a record | {provider} (
284:    Every category has a code template and a flag_type. `recovery_context` e
--- D-024 text
32:| D-024 | **Token budget (Chris, 00:58Z):** keep ≥ 40% of the weekly plan in reserve. (1) Chat updates: one or two lines, only on milestone events; details live on the board. (2) Tier-1 card reviews: **one** reviewer per card, on **sonnet** (persona prompt unchanged); opus reviewers only at mil
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:13:46.593Z

**tool call — Bash**
````
{
 "command": "grep -n \"{raw}\\|{stated}\\|{a}\\|a unit test asserts every category\\|for example \\\"Wording\" memory/DECISIONS.md | cut -c1-90; echo \"---\"; grep -n '\"removed_flag_ids\"' memory/contracts/api.md | cut -c1-80; echo \"--- golden record 8 line\"; grep -n '\"record_no\": 8' evals/golden/case_01_date_formats.expected.json | cut -c1-80; grep -n '\"record_warnings\"' evals/golden/case_01_date_formats.expected.json | cut -c1-60",
 "description": "Get exact line numbers for placeholder and warning findings"
}
````

### User / tool · 2026-11-02T01:13:46.708Z

**tool result**
````
258:    **Template table (design text; slots `{date}` long date, `{provider}` header label
263:    | accident_date_after_treatment | Stated accident date is later than recorded trea
281:    | date_ambiguous | Date to confirm | The date “{raw}” in {provider} can be rea
285:  - Code verifies the excerpt, computes offsets and renders `title` and `explanation` 
296:  - Evidence has at least two items: the stated-date phrase span, and the `Date:` head
---
209:  "removed_flag_ids": ["f_warn_date_r8"],
--- golden record 8 line
65:      "record_no": 8,
315:  "record_warnings": [],
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:14:49.940Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer-r2.md",
 "content": "# Review T-028 round 2 (staff-engineer-reviewer): ADR consistency pass\n\nVerdict: **changes** (0 blockers, 1 major, 3 minors carried or new, 2 nits). Commit reviewed: 10cffcd (architect r2), on top of 3ff15cd (spec R-EX-4(1) AI line) and HEAD 1e675ea. The four in-scope docs are clean in git status (only the agent-memory and board files show as modified).\n\nRound 1 status:\n- **Blocker (AI line) is closed.** The three places that carried the disputed line now carry the golden wording, byte for byte, as C1 shows. The spec change came in 3ff15cd; DECISIONS:204 already carried the golden text in de749c2. My round-1 blocker is stale, as the orchestrator triage said.\n- **Major (api.md mg. split) is closed.** api.md:91 is one unit [477,532) and matches the R-TL-2 splitter and sample.txt offsets exactly.\n- **Major (per-category templates) is closed at design level.** ADR-013 has a template row for all 13 lexicon v2 categories, plus the conflict, gap and record_warning codes. Two new minors come out of the table itself (F2, F3).\n- **Major (spec §8 row 1 vs the export example) is re-filed as F1.** The row was rewritten to a filename grep; the content check it now relies on does not exist.\n- **Minors carried, still open:** F4 (README-arch v1 names), F5 (confirm_date warning vs golden), F6 (unreproducible \"14/14, 17/17\" count). Nit F7 (D-id wording) was not re-checked this round.\n\nCorrection to my round-1 evidence: `artifacts/review-evidence/T-028-review-checks.py` had two defects. AC4b compared api.md against a hand-typed constant `[(477,532)]` while its span filter also caught the 533-552 unit, so it could not pass; the splitter and api.md agreed. AC5 searched for the pre-3ff15cd R-EX-4(1) wording. I retract those two FAIL lines. The corrected checks are in `artifacts/review-evidence/T-028-r2-checks.py`.\n\nMechanical results: `artifacts/review-evidence/T-028-r2-checks.py` prints 7/12 PASS. The five FAILs are F2 (C2c, C2d), F4 (C6), F5 (C7), F6 (C8). F1 is not a script FAIL because the spec row passes its own weakened check (C5); that is the problem.\n\nEvidence excerpts:\n\n```\n$ grep -n \"drafted with AI assistance\" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt\nspec/REQUIREMENTS.md:122:... (1) AI-assistance line (D-009), fixed text: \"This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.\" ...\nspec/REQUIREMENTS.md:273:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.\nmemory/DECISIONS.md:204:  - Internal notes: sections in R-EX-4 order, beginning with the single agreed AI line the fixed text of R-EX-4(1) (`This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: N.`); ...\nevals/golden/sample.export.expected.txt:51:This chronology was drafted with AI assistance; every item in the treatment section was accepted by the paralegal. Items not reviewed: 0.\nEXIT=0\n\n$ grep -n \"sample.export.expected.txt\" memory/contracts/api.md\n267:Built by code from items ... **The exact format of both blocks is `spec/REQUIREMENTS.md` §6 and `evals/golden/sample.export.expected.txt` (authoritative; the example abbreviates the two text blocks and references the file; a pytest compares real output with it).** ...\n272:  \"letter_text\": \"TREATMENT CHRONOLOGY\\n\\n[... nine entries ... full text is the LETTER_TEXT block of evals/golden/sample.export.expected.txt ...]\\n\\nBilled charges stated in these records: $8,390.00\",\nEXIT=0\n\n$ .venv/bin/python -I -c \"...sample[477:532]...\" (run on evals/golden/sample.txt)\nsample[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.'\napi unit text present: True | sample span equals unit: True | old split present in api.md: False\n\n$ .venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py\nPASS C1 AI line: same canonical sentence in spec, DECISIONS, LLM_VS_CODE and golden; no old variant\nPASS C2a every lexicon v2 category has a template-table row in ADR-013\n    lexicon categories: 13; rows in table: 21\n    lexicon categories whose explanation is blank or n/a: ['recovery_context']\nPASS C2b every conflict, gap and record_warning code named in ADR-013 has a row\nFAIL C2c every placeholder in the template table is declared in the slot legend\n    used but not declared: ['date A', 'date B', 'provider A', 'provider B', 'quote A', 'quote B', 'raw', 'stated']\nFAIL C2d the example template under the table uses the same slot names as the table\n    example slots: ['date', 'excerpt', 'source']\nPASS C3a api.md record 2 sentences equal the R-TL-2 splitter output on sample record 2\nPASS C3b each api.md sentence text equals sample.txt[start:end] exactly\nPASS C4 api.md references evals/golden/sample.export.expected.txt (grep count >= 1)\nPASS C5 spec section 8 row 1 check is 'expect >= 1' (not 'expect none') and api.md satisfies it\nFAIL C6 README-arch lexicon line lists only lexicon v2 names or code_lists keys\n    names on that line not in lexicon v2 categories or code_lists keys: ['causation_weakening', 'compliance', 'hedge']\nFAIL C7 api.md confirm_date removed_flag_ids (f_warn_date_r8) has a matching golden expectation\n    golden case_01 record_warnings for record 8: []\nFAIL C8 card AC3 evidence '14/14 blocks, 17/17 offsets' appears in a checked-in script or doc\n    matches for 14/14 or 17/17 in the four docs: 0\nSUMMARY: 7/12 checks passed\nEXIT=1\n```\n\n## Findings\n\n**F1 (major, new this round): the spec §8 row 1 check is a filename grep, and the content test it now relies on does not exist.** The orchestrator rewrote row 1 from \"diff against golden, expect none\" to a grep (`grep -n \"sample.export.expected.txt\" memory/contracts/api.md`, expect ≥ 1). That makes the row pass whether or not the export's notes block equals the golden block. The api.md:267 sentence says \"a pytest compares real output with it\", but no such pytest exists: `.venv/bin/python -m pytest tests/unit -q` prints \"no tests ran in 0.00s\" and exits 5, and `grep -rl \"sample.export.expected\" tests app | wc -l` prints 0. Round-1 fix option A asked for the row to name the test; the row names a grep instead. The golden is the authority (spec §8), and nothing checks it.\n\n**F2 (minor, new): slot names in the ADR-013 template table do not match the slot legend or the example.** DECISIONS.md:258 declares `{date}`, `{provider}`, `{quote}`, `{days}`, `{a}`/`{b}`. The rows use `{date A}`, `{provider A}`, `{quote A}`, `{date B}`, `{provider B}`, `{quote B}` (lines 262 onward), `{stated}` (263) and `{raw}` (281). The example at DECISIONS.md:285 uses `{source}`, `{date}`, `{excerpt}`. A renderer built from the legend would raise on the table's keys, or the implementer would pick one set and the other would drift. Design text only, nothing built yet, so minor.\n\n**F3 (minor, new): recovery_context has no explanation template, but the text says every category has one.** DECISIONS.md:279 `| recovery_context | (context only, never raises a flag) | n/a |`, against DECISIONS.md:285 \"a unit test asserts every category has one\". As written, the test either fails on recovery_context or needs an unstated exception. State the exception: categories with strength `low` are never rendered and have no explanation template; the test asserts a template for every other category.\n\n**F4 (minor, carried from r1, open): README-arch lexicon line lists v1 names.** app/README-arch.md:36 reads `lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection`. Lexicon v2 has none of `causation_weakening`, `compliance` or `hedge` as categories (C6 output above). Fix: rewrite the line as the 13 v2 names plus the 4 code_lists keys, with a pointer to ADR-013.\n\n**F5 (minor, carried from r1, open): confirm_date example removes a warning the golden does not expect.** api.md:209 `\"removed_flag_ids\": [\"f_warn_date_r8\"]`. Golden case_01 record 8 (`{\"record_no\": 8, \"raw_date\": \"04/05/2026\", \"date\": null, \"kind\": \"phone_note\", ...}` at line 65) has `\"record_warnings\": []` at line 315, and the golden description says the ambiguous date \"must be marked ambiguous ... and surfaced for review\", which no expected value checks. Either the golden lacks the expectation or the example names a flag the pipeline is not required to create. The gap example itself (`gap_flags: []`) is correct. Fix as r1: qa adds the date_ambiguous expectation, or the architect writes `removed_flag_ids: []` and records which wins.\n\n**F6 (minor, carried from r1, open): the AC3 evidence count is not reproducible.** Card T-028 AC3 evidence and the Handoff both say \"check script 14/14 blocks, 17/17 offsets\". `grep -rn '14/14\\|17/17' memory/ docs/ app/ evals/ tools/` returns nothing (C8: 0). Check the script into artifacts/review-evidence/ and quote its output.\n\n**F7 (nit, carried from r1, not re-checked): card AC4 \"D-001..D-024 in all three docs\" overstates the citations.** The r1 counts stand; every cited id resolves.\n\n**F8 (nit, new): spec §8 row 1 has six cells under a five-column header.** spec/REQUIREMENTS.md row 1 ends `| T-028 | resolved |` after the Owner column. Move the status into the Difference cell or add a column.\n\n## Exercised\n\n- `personas/staff-engineer.md` read in full; `reviews/T-028-staff-engineer.md` (r1) read in full; `.claude/agent-memory/staff-engineer-reviewer/MEMORY.md` read.\n- `git log --oneline -5`; `git show --stat 10cffcd`; `git show 10cffcd -- memory/DECISIONS.md memory/contracts/api.md` (full diff read); `git log --oneline de749c2..HEAD -- <four docs, spec, golden>`.\n- `grep -n \"drafted with AI assistance\" ...` and `grep -n \"AI assistance\" ...` over spec, DECISIONS, LLM_VS_CODE, api.md, golden (outputs quoted above).\n- `.venv/bin/python -I` lexicon load: version 2, 66 entries, 13 distinct categories; code_lists keys `accident_date_phrases, damages, injection, non_encounter`.\n- DECISIONS.md ADR-013 lines 246-296 read; template table counted: 21 rows; 13 of 13 lexicon categories have a row.\n- api.md:86-92 record 2 sentences; `sample.txt[477:532]` literal check; `grep -n \"sample.export.expected.txt\" memory/contracts/api.md` (lines 267, 272); `grep -n \"removed_flag_ids\"` (209); `grep -n \"internal_notes_text\"` (273).\n- spec/REQUIREMENTS.md section 8 rows 1-5 (current text).\n- `artifacts/review-evidence/T-028-review-checks.py` (round 1, now with two known defects) and `artifacts/review-evidence/T-028-r2-checks.py` (new, 12 checks, 7/12).\n- `evals/golden/check_golden.py` → \"golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples, 40 hallucination items (13 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered\", exit 0.\n- `evals/golden/case_01_date_formats.expected.json`: top-level keys, record 8 (line 65), `record_warnings` (line 315).\n- `.venv/bin/python -m pytest tests/unit -q` → \"no tests ran in 0.00s\", exit 5. `grep -rl sample.export.expected tests app` → 0 files.\n- `.venv/bin/python -m app.pipeline evals/golden/sample.txt` → \"No module named app.pipeline\", exit 1. Not runnable at this commit; no app URL exists (`ls -A app/backend` empty).\n- `python3 tools/board.py show T-028` (in_review, 4 ACs, notes, handoff) and `python3 tools/board.py validate` → \"ok (28 file(s))\", exit 0 (before this file was written).\n- `app/README-arch.md:36` read.\n\n## What is right\n\n- The mg. sentence is one unit in api.md:91 (477-532), equal to the R-TL-2 splitter output and to sample.txt[477:532] (C3a, C3b).\n- ADR-013 has one template row per lexicon v2 category plus each conflict, gap and record_warning code, and the text is code-rendered with no model text in it (C2a, C2b).\n- The AI disclosure sentence is identical in spec R-EX-4(1) and §6, DECISIONS:204, LLM_VS_CODE:103 and the golden file (C1); the round-1 blocker is closed.\n\n```json\n{\"card\": \"T-028\", \"persona\": \"staff-engineer-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"git 10cffcd (architect r2) on HEAD 1e675ea; four docs memory/DECISIONS.md, memory/contracts/api.md, docs/LLM_VS_CODE.md, app/README-arch.md; spec/REQUIREMENTS.md (3ff15cd, section 8 row 1 rewritten by orchestrator) and evals/golden at HEAD; no app URL (app/backend empty, no app.pipeline); sample case evals/golden/sample.txt\",\n \"exercised\": [\n   \"read personas/staff-engineer.md in full; read reviews/T-028-staff-engineer.md (round 1) and the agent memory index\",\n   \"git show --stat 10cffcd; git show 10cffcd -- memory/DECISIONS.md memory/contracts/api.md (full diff); git log --oneline de749c2..HEAD over the in-scope files\",\n   \"grep -n \\\"drafted with AI assistance\\\" spec/REQUIREMENTS.md memory/DECISIONS.md evals/golden/sample.export.expected.txt -> spec:122, spec:273, DECISIONS:204, golden:51, all the same sentence (N or 0 for the count), EXIT=0\",\n   \"grep -n \\\"AI assistance\\\" across spec, DECISIONS, LLM_VS_CODE, api.md, golden -> one canonical line each; no R-EX-4(1) old variant anywhere\",\n   \".venv/bin/python -I lexicon load: version 2, 66 entries, 13 distinct categories; code_lists keys accident_date_phrases, damages, injection, non_encounter\",\n   \"read memory/DECISIONS.md ADR-013 (lines 246-296): template table has 21 rows; all 13 lexicon categories have a row; recovery_context explanation is n/a\",\n   \"api.md:86-92 record 2 sentences vs sample.txt[477:532] = 'Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week.' ; artifacts/review-evidence/T-028-r2-checks.py C3a/C3b PASS\",\n   \"grep -n \\\"sample.export.expected.txt\\\" memory/contracts/api.md -> lines 267, 272\",\n   \"read spec/REQUIREMENTS.md section 8 rows 1-5 (row 1 now 'grep ... expect >= 1')\",\n   \"artifacts/review-evidence/T-028-review-checks.py (round 1) rerun: 8/12; two round-1 defects identified and retracted (AC4b constant, AC5 stale wording)\",\n   \"artifacts/review-evidence/T-028-r2-checks.py (new): 7/12 PASS; FAILs C2c, C2d, C6, C7, C8\",\n   \"evals/golden/check_golden.py -> golden OK, exit 0\",\n   \"evals/golden/case_01_date_formats.expected.json: record 8 (line 65, raw_date 04/05/2026, date null, phone_note), record_warnings [] (line 315), gap_excluded_records [8]\",\n   \".venv/bin/python -m pytest tests/unit -q -> 'no tests ran in 0.00s', exit 5; grep -rl sample.export.expected tests app -> 0 files\",\n   \".venv/bin/python -m app.pipeline evals/golden/sample.txt -> 'No module named app.pipeline', exit 1; ls -A app/backend -> empty\",\n   \"grep -rn '14/14\\\\|17/17' memory/ docs/ app/ evals/ tools/ -> no matches (C8: 0)\",\n   \"app/README-arch.md:36 read; lexicon v2 names compared (causation_weakening, compliance, hedge not categories)\",\n   \"python3 tools/board.py show T-028 -> in_review, 4 ACs, notes and handoff read (claims not trusted)\",\n   \"python3 tools/board.py validate -> ok (28 file(s)), exit 0\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"AI_line_matches_R-EX-4_1\": 5, \"mg_unit_matches_splitter_and_D-021\": 5, \"ADR013_template_per_lexicon_category\": 4, \"ADR013_slot_keys_consistent\": 2, \"spec_section8_row1_testable\": 2, \"golden_vs_confirm_date_example\": 2, \"evidence_reproducible\": 2, \"evidence_honesty\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"spec section 8 row 1 is checked by a filename grep; the golden-equality test it depends on does not exist\",\n   \"evidence\": \"spec/REQUIREMENTS.md section 8 row 1: `grep -n \\\"sample.export.expected.txt\\\" memory/contracts/api.md` (expect ≥ 1). memory/contracts/api.md:267: 'a pytest compares real output with it'. Repro: `.venv/bin/python -m pytest tests/unit -q` -> 'no tests ran in 0.00s', exit 5; `grep -rl sample.export.expected tests app | wc -l` -> 0.\",\n   \"why_it_matters\": \"The golden notes and letter blocks are the authority (spec section 8). With this row, the spec check passes whether or not the export's internal_notes_text equals the golden block, so the disclosure text and the flag lists in the notes could drift from the golden with no failing check. The round-1 fix asked for the row to name a test; the row now names a grep.\",\n   \"fix\": \"Build the export golden test on the export card (the one that assembles letter_text and internal_notes_text). Point spec section 8 row 1 at that test id, not at a grep for a filename. Keep the api.md pointer.\",\n   \"acceptance_test\": \"A pytest (proposed id tests/unit/test_export_golden.py::test_blocks_equal_golden) builds the export from the sample accepted set and asserts both blocks equal evals/golden/sample.export.expected.txt byte for byte; spec row 1 check names that id; mutating one line of the notes block in the export code makes the test fail.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"ADR-013 template table uses slot names that the slot legend and the example do not declare\",\n   \"evidence\": \"memory/DECISIONS.md:258 legend: `{date}`, `{provider}`, `{quote}`, `{days}`, `{a}`/`{b}`. Rows use {date A}, {provider A}, {quote A}, {date B}, {provider B}, {quote B} (from line 262), {stated} (line 263), {raw} (line 281). Example at memory/DECISIONS.md:285 uses {source}, {date}, {excerpt}. Repro: `.venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py` -> C2c FAIL, C2d FAIL.\",\n   \"why_it_matters\": \"The table is the code-rendered template set the flag rule depends on (LLM_VS_CODE row 14). If the legend and the rows disagree, the renderer and its unit test will disagree on keys, and a template could emit literal braces in a flag the paralegal reads.\",\n   \"fix\": \"Pick one slot set. Declare every slot used in the table, including stated and raw, in the legend; rename the example's slots to match. Add the slot list as a column or a line per row.\",\n   \"acceptance_test\": \"The unit test that asserts one template per category also asserts every placeholder in each template is in the declared slot set; the r2 script C2c and C2d PASS.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"recovery_context has no explanation template, but the ADR says every category has one and a unit test asserts it\",\n   \"evidence\": \"memory/DECISIONS.md:279: `| recovery_context | (context only, never raises a flag) | n/a |`. memory/DECISIONS.md:285: 'a unit test asserts every category has one'.\",\n   \"why_it_matters\": \"As written, the stated test either fails on recovery_context or needs an exception nobody has written down. An implementer will pick one of these silently.\",\n   \"fix\": \"State the exception in ADR-013: categories with strength low are never rendered and have no explanation template; the unit test asserts a template for every other category.\",\n   \"acceptance_test\": \"The unit test lists the strength-low categories explicitly and asserts a template for every other category in the lexicon v2 list.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"README-arch lexicon line lists category names that lexicon v2 does not contain (carried from r1)\",\n   \"evidence\": \"app/README-arch.md:36: 'lexicon.yaml [researcher] categories: pre_existing, causation_weakening, compliance, hedge, patient_report, accident_date_phrases, damages, non_encounter, injection'. Repro: `.venv/bin/python -I artifacts/review-evidence/T-028-r2-checks.py` -> C6 FAIL: causation_weakening, compliance, hedge.\",\n   \"why_it_matters\": \"A backend worker reading the architecture map would look for categories that do not exist in app/llm/lexicon.yaml.\",\n   \"fix\": \"Rewrite README-arch.md:36 as the 13 lexicon v2 category names and the 4 code_lists keys, with a pointer to ADR-013.\",\n   \"acceptance_test\": \"C6 PASS: every name on the README-arch lexicon line is a lexicon v2 category or a code_lists key.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"confirm_date example removes a date_ambiguous warning the golden does not expect (carried from r1)\",\n   \"evidence\": \"memory/contracts/api.md:209: `\\\"removed_flag_ids\\\": [\\\"f_warn_date_r8\\\"]`. evals/golden/case_01_date_formats.expected.json:315 `\\\"record_warnings\\\": []`; record 8 at line 65 (`\\\"raw_date\\\": \\\"04/05/2026\\\", \\\"date\\\": null`). Golden description: 'Ambiguous date must be marked ambiguous, excluded from gap math, and surfaced for review'; only the exclusion is expected. Repro: C7 FAIL.\",\n   \"why_it_matters\": \"The golden is the stated authority for expected outputs. Either the golden is missing the date_ambiguous expectation the description states, or the example names a warning the pipeline is not required to create. The gap example is correct; this one id is the problem.\",\n   \"fix\": \"qa adds a date_ambiguous record_warning expectation for case_01 record 8 to the golden; or the architect writes `removed_flag_ids: []` and records which of the two wins.\",\n   \"acceptance_test\": \"check_golden.py asserts the record 8 warning if qa adds it, or the api example removes the id and C7 is retired.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"the AC3 evidence count '14/14 blocks, 17/17 offsets' is not produced by any checked-in script (carried from r1)\",\n   \"evidence\": \"Card T-028 AC3 evidence and Handoff: 'check script 14/14 blocks, 17/17 offsets'. Repro: `grep -rn '14/14\\\\|17/17' memory/ docs/ app/ evals/ tools/` -> no matches (C8: 0 matches in the four docs).\",\n   \"why_it_matters\": \"The card's evidence cannot be re-run by the next reviewer, so the claim rests on a hand count.\",\n   \"fix\": \"Check the offset and block script into artifacts/review-evidence/ and quote its output in the card.\",\n   \"acceptance_test\": \"`.venv/bin/python -I artifacts/review-evidence/<script>.py` exits 0 and prints the counts quoted in the card.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"spec section 8 row 1 has six cells under a five-column header (new)\",\n   \"evidence\": \"spec/REQUIREMENTS.md section 8, row 1: `| 1 | ... | T-028 | resolved |` after the Owner column.\",\n   \"why_it_matters\": \"Markdown renders the status as a stray cell; the next editor may read it as an owner.\",\n   \"fix\": \"Move 'resolved' into the Difference cell or add a Status column to the table.\",\n   \"acceptance_test\": \"Each row of the section 8 table has five cells.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"card AC4 evidence 'D-001..D-024 in all three docs' overstates the citations (carried from r1, not re-checked this round)\",\n   \"evidence\": \"Card T-028 AC4 evidence. Round-1 count: DECISIONS.md 22 distinct D-ids, api.md 8, LLM_VS_CODE.md 2; every cited id resolves.\",\n   \"why_it_matters\": \"The substance passes; the evidence sentence does not describe the files.\",\n   \"fix\": \"Restate as 'every D-id cited in the four docs resolves to a row in ORCHESTRATOR_DECISIONS (D-001..D-024)'.\",\n   \"acceptance_test\": \"The r1 AC8 check (every cited D-id defined) continues to pass.\"}\n ],\n \"whats_right\": [\n   \"The mg. sentence is one unit in api.md:91 (477-532), equal to the R-TL-2 splitter output and to sample.txt[477:532] (C3a, C3b).\",\n   \"ADR-013 has one template row for each of the 13 lexicon v2 categories and for each conflict, gap and record_warning code; the text is code-rendered.\",\n   \"The AI disclosure sentence is identical in spec R-EX-4(1), spec section 6, DECISIONS.md:204, LLM_VS_CODE.md:103 and the golden file (C1); the round-1 blocker is closed.\"\n ],\n \"questions_for_chris\": [\n   \"Is the golden wording the canonical AI line? After 3ff15cd, spec R-EX-4(1), section 6, DECISIONS:204, LLM_VS_CODE:103 and golden:51 all carry it, which closes the round-1 blocker on that reading. Confirm, or name the other wording.\",\n   \"D-024 puts Tier-1 card reviews on sonnet. This review ran as claude-haiku-5-5, as in round 1. Accept haiku for doc-only consistency passes, or re-run on sonnet before the gate?\",\n   \"Should the golden export test (F1) be assigned to a card now? tests/unit is empty at M1, so the spec row has nothing to point at until one exists.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T01:14:50.095Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer-r2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:14:52.689Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I -c \"\nimport json,re\nt = open('reviews/T-028-staff-engineer-r2.md', encoding='utf-8').read()\nblocks = re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', t, re.S)\nprint('json blocks:', len(blocks))\nd = json.loads(blocks[0])\nsev = [f['severity'] for f in d['findings']]\nprint('verdict', d['verdict'], 'severities', sev)\nprint('blockers', sev.count('blocker'), 'majors', sev.count('major'))\nprint('model', d['model'], 'whats_right', len(d['whats_right']))\n\" 2>&1; echo \"EXIT=$?\"; python3 tools/board.py validate 2>&1 | tail -3; echo \"VALIDATE_EXIT=${PIPESTATUS[0]}\"",
 "description": "Parse the review JSON block and run board validate"
}
````

### User / tool · 2026-11-02T01:14:52.746Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:14:56.233Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_r2_json.py",
 "content": "import json\nimport re\nimport sys\n\npath = \"/Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer-r2.md\"\ntext = open(path, encoding=\"utf-8\").read()\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"verdict\", d[\"verdict\"], \"severities\", sev)\nprint(\"blockers\", sev.count(\"blocker\"), \"majors\", sev.count(\"major\"))\nprint(\"model\", d[\"model\"], \"whats_right\", len(d[\"whats_right\"]))\nexpected = \"fail\" if sev.count(\"blocker\") else (\"changes\" if sev.count(\"major\") else \"pass\")\nprint(\"verdict rule expects\", expected, \"ok\" if expected == d[\"verdict\"] else \"MISMATCH\")\nsys.exit(0 if expected == d[\"verdict\"] else 1)\n"
}
````

### User / tool · 2026-11-02T01:14:56.290Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/check_r2_json.py). Reviewers critique; they do not fix.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:14:59.269Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-json-check.py",
 "content": "#!/usr/bin/env python3\n\"\"\"Parse the single JSON block in reviews/T-028-staff-engineer-r2.md and apply the verdict rule (CONTRACT 7.4).\n\nRun from repo root:  .venv/bin/python -I artifacts/review-evidence/T-028-r2-json-check.py\n\"\"\"\nimport json\nimport re\nimport sys\nfrom pathlib import Path\n\npath = Path(__file__).resolve().parents[2] / \"reviews\" / \"T-028-staff-engineer-r2.md\"\ntext = path.read_text(encoding=\"utf-8\")\nfence = \"`\" * 3\nblocks = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, text, re.S)\nprint(\"json blocks:\", len(blocks))\nd = json.loads(blocks[0])\nsev = [f[\"severity\"] for f in d[\"findings\"]]\nprint(\"verdict\", d[\"verdict\"], \"severities\", sev)\nprint(\"blockers\", sev.count(\"blocker\"), \"majors\", sev.count(\"major\"))\nprint(\"model\", d[\"model\"], \"whats_right\", len(d[\"whats_right\"]))\nexpected = \"fail\" if sev.count(\"blocker\") else (\"changes\" if sev.count(\"major\") else \"pass\")\nprint(\"verdict rule expects\", expected, \"ok\" if expected == d[\"verdict\"] else \"MISMATCH\")\nsys.exit(0 if expected == d[\"verdict\"] else 1)\n"
}
````

### User / tool · 2026-11-02T01:14:59.369Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-028-r2-json-check.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:15:00.685Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -I artifacts/review-evidence/T-028-r2-json-check.py 2>&1; echo \"JSON_CHECK_EXIT=$?\"; python3 tools/board.py validate 2>&1 | tail -3; echo \"VALIDATE_EXIT=${PIPESTATUS[0]}\"",
 "description": "Parse review JSON, apply verdict rule, and run board validate"
}
````

### User / tool · 2026-11-02T01:15:00.872Z

**tool result**
````
json blocks: 1
verdict changes severities ['major', 'minor', 'minor', 'minor', 'minor', 'minor', 'nit', 'nit']
blockers 0 majors 1
model claude-haiku-5-5 whats_right 3
verdict rule expects changes ok
JSON_CHECK_EXIT=0
ok (47 file(s))
VALIDATE_EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:15:02.279Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md"
}
````

### User / tool · 2026-11-02T01:15:02.299Z

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
32	Round 4 = T-028 consistency pass (2026-11-01, fail: 1 blocker, 3 majors). Evidence: `artifacts/review-evidence/T-028-review-checks.py`.
33	- Fix claims drift from the file: the architect's "mg. one unit" evidence is contradicted by api.md:91 (two units). T-014 r3 M4 came back after DECISIONS was fixed; ADR text and illustrative JSON are separate places to fix. Re-run the R-TL-2 splitter on sample record 2 after any api.md sentence edit.
34	- "Fixed text of R-EX-4(1)" label on a string that is not R-EX-4(1). The spec itself had two AI lines (R-EX-4(1) vs section 6 / golden). Architect followed the golden-authority rule silently. When the spec disagrees with itself, the card must say so, not claim alignment.
35	- A spec reconciliation check ("diff of the example against golden, expect none") cannot pass once the example is a pointer. Amend the check row or the example; never leave them disagreeing.
36	- "Each with a template" in an ADR is a generic assertion; count per-category template text, not the word "template".
37	- Evidence counts with no script in the repo ("14/14 blocks, 17/17 offsets") are not reproducible; ask for the script in artifacts/review-evidence.
38	
39	**Why:** these were the open T-014 r3 items closed by T-028; closure claims were partly false.
40	**How to apply:** on any ADR or api.md consistency card, grep the claimed string in every file it names and run the splitter/offset check before accepting "aligned".
41	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:15:06.871Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md",
 "old_string": "**Why:** these were the open T-014 r3 items closed by T-028; closure claims were partly false.\n**How to apply:** on any ADR or api.md consistency card, grep the claimed string in every file it names and run the splitter/offset check before accepting \"aligned\".",
 "new_string": "Round 2 of T-028 (2026-11-01, changes: 1 major, 3 minors carried or new, 2 nits; 0 blockers). Evidence: `artifacts/review-evidence/T-028-r2-checks.py`.\n- Stale blockers: the round-1 AI-line blocker was closed by a spec-side commit (3ff15cd) while the review still quoted the old wording. Re-grep every disputed string before re-filing.\n- Check weakened to pass: the spec row 1 diff check was rewritten to a grep for a filename (\"expect >= 1\"), and the golden equality it implied has no test (tests/unit is empty). A check that passes without the content it is meant to verify is a finding even when the doc now agrees.\n- Template tables: 21 rows cover 13 of 13 lexicon categories, but slot names differ between legend, rows and example (`{a}` vs `{date A}`, `{source}` vs `{provider}`), and recovery_context is `n/a` while the text says every category has one.\n- My own round-1 script had a hand-typed constant in AC4b (span filter caught a second unit) and searched for stale wording in AC5. Compare computed to computed, never to a literal, and retire checks whose target text moved.\n- Carried, still open: README-arch lexicon line (v1 names), confirm_date `f_warn_date_r8` vs golden (no record 8 warning), \"14/14, 17/17\" count with no script.\n\n**Why:** these were the open T-014 r3 items closed by T-028; closure claims were partly false, and round 2 showed the fixes can also weaken the checks.\n**How to apply:** on any ADR or api.md consistency card, grep the claimed string in every file it names, run the splitter/offset check and compare computed values, and check that any spec check row still tests content, not a filename, before accepting \"aligned\"."
}
````

### User / tool · 2026-11-02T01:15:06.975Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:15:08.902Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md",
 "old_string": "- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r3 and T-028 defects: doc/REQ drift, mg. splitter, AI line, template coverage",
 "new_string": "- [Design review patterns](project_design_review_patterns.md) — T-014 r1-r4 and T-028 r1-r2: doc/REQ drift, mg. splitter, AI line, template slots, weakened spec checks"
}
````

### User / tool · 2026-11-02T01:15:09.012Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/staff-engineer-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T01:15:11.475Z

Verdict **changes**, 0 blockers. The round-1 AI-line blocker is closed (the same sentence now sits in spec:122/273, DECISIONS:204 and golden:51), and the mg. split at api.md:91 is fixed.
One major open: spec §8 row 1 is now a filename grep, and the golden export test it implies does not exist (tests/unit is empty). Minors still open: README-arch v1 names, the confirm_date warning, and the unreproducible 14/14 count.
Review: /Users/arsis/zlayt-pm-project/reviews/T-028-staff-engineer-r2.md (JSON parses, verdict rule ok, board validate ok). My round-1 script had two defects, which I retracted in the review.
