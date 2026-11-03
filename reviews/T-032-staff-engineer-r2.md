# T-032 review round 2, staff-engineer-reviewer

Verdict: **changes**. The round-1 blocker is fixed: preamble, trailing, between-block, between-separator and between-field text now becomes an `unsplit` record with `SPLIT_AMBIGUOUS` and `UNSPLIT_TEXT`. `03-17-98` is now `ambiguous` with candidates 1998 and 2098 (D-027). The limit boundaries are proven by tests. One silent-drop path is left: the SYNTHETIC banner exemption is too broad. Several new tests are weaker than their names say.

Exercised:
- `.venv/bin/python -m pytest tests/unit/test_dates.py tests/unit/test_ingest.py tests/unit/test_injection.py -q` gave 87 passed.
- `.venv/bin/python artifacts/review-evidence/T-032-ingest.py` gave 2 mismatches, both golden-vocabulary drift (carried minor).
- A probe script covering the cases in the brief:
  - preamble with and without headers, trailing text, text between `---` separators, text between fields, duplicate `Source:` and `Excerpt:` lines;
  - `03-17-98` and 7 other numeric dates;
  - empty, whitespace-only and None input;
  - exactly 60000 chars (accepted) and 60001 (`input_too_large`);
  - 40 records (accepted) and 41 (`input_too_large`);
  - determinism (identical across two runs);
  - a character-coverage check over sample.txt and case_01 to case_09.
- Mutation spot-check on a scratch copy under the scratchpad; the repo was untouched.
  - M1 leftovers loop off: 3 tests fail.
  - M2 max_records off: 1 fails.
  - M3 PIVOT_YY=99: 1 fails.
  - M4 oversize check off: 3 fail.
  - M6 empty check off: 1 fails.
  - M5 banner exemption widened: **87 pass, none fail**.
  - M7 dedupe key without source: **87 pass, none fail**.
- Read `ingest.py` and `dates.py` in full, and the new tests at `test_ingest.py:64-135`.
- Round-1 minors:
  - Source label is now scanned and tested.
  - `IngestError` replaces bare `ValueError` strings.
  - The golden vocabulary drift is not fixed; that is qa's file.
  - `scan('Disregard the above')` still returns `[]`; I left it deferred to security-reviewer.

```json
{"card": "T-032", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2: app/backend/{ingest,dates,injection,lexicon}.py; tests/unit/{test_dates,test_ingest,test_injection}.py; evals/golden; D-027; no app URL",
 "exercised": ["pytest tests/unit/test_dates.py tests/unit/test_ingest.py tests/unit/test_injection.py -q -> 87 passed", "artifacts/review-evidence/T-032-ingest.py -> TOTAL MISMATCHES: 2 (golden vocabulary only)", "probe scripts (scratchpad p2.py, p3.py): preamble/trailing/between-separator/between-field/duplicate-field text, 03-17-98 and 7 more numeric dates, empty/whitespace/None, 60000/60001 chars, 40/41 records, header-only paste, SYNTHETIC-banner abuse, determinism, char-coverage over sample + 9 cases", "mutation spot-check on scratch copy (mutate.py): M1-M7; M5 (banner exemption) and M7 (dedupe drops source) survive", "read ingest.py, dates.py, test_ingest.py:64-135"],
 "verdict": "changes",
 "scores": {"determinism_and_no_llm": 5, "date_parsing_no_silent_guess": 4, "split_fidelity_no_lost_text": 4, "limits_before_llm": 4, "dedupe": 4, "injection_scan": 4, "tests_prove_AC": 3},
 "findings": [
  {"severity": "major", "title": "SYNTHETIC banner exemption silently drops any first line that merely starts with 'SYNTHETIC'",
   "evidence": "ingest.py:106 exempts a single-line leading segment when text[s:e].upper().startswith('SYNTHETIC'). Repro (.venv/bin/python): ingest.ingest('SYNTHETIC patient had prior neck surgery in 2019\\n=== Record 1 ===\\nDate: 2026-01-01\\nSource: A\\nExcerpt: \"One.\"\\n') -> 1 record, split_method 'code', warnings []. Mutation M5 (exemption widened to any first line) leaves all 87 tests green; test_ingest.py:119-125 accepts any first line as the exempt remainder.",
   "why_it_matters": "D-027 says text outside recognised blocks is never dropped. The same silent-loss class as the round-1 blocker remains, behind a prefix check instead of an exact banner match. A clinical sentence is lost with no signal. I rate it major rather than blocker only because it needs the paste's first line to begin with the word SYNTHETIC.",
   "fix": "Exempt only the exact banner lines in evals/golden (match the full known banner text, or a regex like ^SYNTHETIC\\s*[—-]\\s*[^.]*(synthetic|not real)[^.]*$ documented in the docstring). Any other leading line becomes an unsplit record.",
   "acceptance_test": "test_ingest.py: the repro above yields an unsplit record and SPLIT_AMBIGUOUS; mutation M5 makes at least one test fail; the golden banners are still exempt."},
  {"severity": "minor", "title": "Dedupe provider-sensitivity is not proven (mutation M7 survives)",
   "evidence": "ingest.py:162 key (iso, _norm(source), _norm(excerpt)); deleting _norm(r['source']) keeps 87 passed. test_dedupe_requires_same_normalized_text_and_provider and test_same_day_different_provider_stays_separate do not use identical text with different providers.",
   "why_it_matters": "Checklist 19: the key must include the provider so two providers with identical wording on the same day are not merged and one charge dropped.",
   "fix": "Add a test with the same date and identical excerpt but different Source labels; assert two groups.",
   "acceptance_test": "M7 makes the new test fail."},
  {"severity": "minor", "title": "test_limits_no_llm cannot fail: ingest never reaches the provider",
   "evidence": "test_ingest.py:71-79 monkeypatches provider.complete and asserts calls == [], but ingest.py does not import app.llm and pipeline.py:4 is 'def run_ingest(raw_text: str): raise NotImplementedError'.",
   "why_it_matters": "The 'no LLM call before limits' claim is not enforced; it will pass whatever a future pipeline does. Ingest-level limit checks themselves are properly proven by test_limit_boundaries.",
   "fix": "Re-point the test at the pipeline entry point once wired (T-048); add a note in the test that it is a placeholder until then.",
   "acceptance_test": "Pipeline-level test: with the fixture backend counter, 60001 chars and 41 records raise with counter == 0; removing check_limits from the pipeline path fails it."},
  {"severity": "minor", "title": "Two-digit years 27-40 are read as 20yy and 'parsed', including future dates",
   "evidence": "dates.py:24 PIVOT_YY = 40; repro: parse_date('03-17-39') -> status 'parsed', iso '2039-03-17'.",
   "why_it_matters": "D-027 says two-digit years are never guessed. A fixed pivot is a documented guess and sample dates depend on 26, but a date 13 years in the future feeds gap math with no flag. test_two_digit_year_is_never_guessed covers only 98 and 26.",
   "fix": "Either pivot against an injected 'today' (anything after today is ambiguous), or say in the docstring and the product note that yy <= 40 is read as 20yy.",
   "acceptance_test": "test_dates.py: parse_date('03-17-39') is not 'parsed'; or a documented pivot test at 40/41."},
  {"severity": "minor", "title": "A paste of header lines only returns 0 records, split_method 'code', no warning",
   "evidence": ".venv/bin/python -c \"from app.backend import ingest; r=ingest.ingest('=== Record 1 ===\\n=== Record 2 ===\\n'); print(len(r['records']), r['split_method'], r['warnings'])\" -> 0 code []",
   "why_it_matters": "No facts are lost, but the UI would report 'found 0 records' as a confident split instead of an error or ambiguity.",
   "fix": "Zero records after a non-empty paste should raise IngestError('bad_request') or set SPLIT_AMBIGUOUS.",
   "acceptance_test": "The repro raises or warns SPLIT_AMBIGUOUS."},
  {"severity": "minor", "title": "Golden record_warnings still disagree with the pipeline (carried from round 1)",
   "evidence": "T-032-ingest.py: case_01 record_warnings got [('date_ambiguous', 8)] exp []; case_07 got injection_suspected exp instruction_like_text. TOTAL MISMATCHES: 2.",
   "why_it_matters": "A golden comparison would fail on correct behaviour. This is qa's file, not a code defect.",
   "fix": "qa updates expected.json (case_01 r8 date_ambiguous; case_07 type injection_suspected).",
   "acceptance_test": "T-032-ingest.py reports TOTAL MISMATCHES: 0."}
 ],
 "whats_right": ["Round-1 blocker closed: every probed outside-block text becomes an unsplit record with SPLIT_AMBIGUOUS + UNSPLIT_TEXT, and 3 mutation-sensitive tests plus a per-golden coverage test back it.", "03-17-98 -> ambiguous [1998-03-17, 2098-03-17] while 3/25/26 stays parsed; 60000 accepted, 60001 and 41 records refused with IngestError('input_too_large'); empty/whitespace/None -> bad_request.", "Still zero LLM/network/clock/float in ingest and dates; output identical across runs; IngestError replaces bare ValueError strings."],
 "questions_for_chris": []}
```
