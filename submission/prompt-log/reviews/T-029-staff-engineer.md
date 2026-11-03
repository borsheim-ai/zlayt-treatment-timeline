# T-029 review: staff-engineer-reviewer (Marcus Lee)

Verdict: **changes**. No blockers. Three majors: checklist items the suites do not encode (amount-in-text grounding, dedupe key isolation / paste-twice, one reason code missing from the compose_state table).

Run: `.venv/bin/python -m pytest tests/unit -q` -> `366 failed, 30 passed, 9 errors in 0.92s` at review start. Every `E` line is `NotImplementedError` (374 plain, 1 `NotImplementedError: REASON_CODES`). No collection errors. The 30 passes are 13 `test_module_exists`, 13 boundary scans, 3 vacuous `test_cents_and_class_match_golden` cases (case_02/04/06 have no amounts) and the lexicon-yaml test. The suite is now 482 collected because T-048 files (test_audited/schemas/provider) landed since; `grep -L 'R-[A-Z]*-[0-9]' tests/unit/test_*.py` now prints `tests/unit/test_audited.py` (T-048's, not T-029's).

Golden spot-checks, all correct against `evals/golden/*.expected.json` and `spec/SAMPLE_CASE_TRUTHS.md`:
1. Gap 28 / 73 days with the 2026-03-06 -> 2026-05-18 flag.
2. Case_02 29/30/31 (3 flags, 4 near-misses, leap 2028) plus `is_gap` at 28/29/30/31/73.
3. $8,390 = 839000 cents, rate excluded.
4. $185 as rate, with 20 phrasings (I counted 20).
5. `$1,2OO` -> cents None, class unclear.
6. Sample record 7 header date 2026-05-18.
7. Case_04 6 records -> `[[1,2],[3,4],[5],[6]]`.
8. Ambiguous 04/05/2026 -> candidates 2026-04-05 and 2026-05-04.

Tests are deterministic. `now` is injected in the db tests, there is no network and no sleep. The API shapes are fixed by docstrings, which is acceptable. Reasonable designs are not blocked, with the exceptions in the findings.

```json
{"card": "T-029", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "tests/unit/* + app stubs, commits eb60295 and 50fbd90; golden cases + sample; no app URL",
 "exercised": [
  "python3 tools/board.py show T-029",
  ".venv/bin/python -m pytest tests/unit -q (366 failed, 30 passed, 9 errors; all E lines NotImplementedError)",
  "pytest --collect-only (482 now; 396 at card time)",
  "read every tests/unit/test_*.py in T-029 scope plus _golden.py",
  "diffed assertions against golden expected.json (records, gap_table, amounts, totals) and spec/SAMPLE_CASE_TRUTHS.md",
  "grep -L R-ID over test_*.py",
  "mutation on boundary scanner: ran test_boundaries.transitive against a scratch tree in the scratchpad (urllib.request, importlib.import_module, package __init__ importing anthropic, transitive helper->provider)",
  "checked golden letter for forbidden substrings used by test_letter_has_no_flag_content",
  "grep for amount grounding tests and ENDPOINT_NOT_VERIFIED coverage; board.py validate"],
 "verdict": "changes",
 "scores": {"golden_fidelity": 4, "ac_coverage": 3, "mutation_resistance": 3, "determinism": 5, "design_freedom": 4, "boundary_scan": 3},
 "findings": [
  {"severity": "major", "title": "No test for the amount-in-text grounding check (GROUNDING_AMOUNT_NOT_IN_TEXT)",
   "evidence": "grep -n 'amount\\|check_amount' tests/unit/test_grounding.py returns only case_04 lines (23, 75); GROUNDING_AMOUNT_NOT_IN_TEXT appears only as a string in test_confidence.py rejected-cases. Checklist #4 requires each amount to appear in the record text.",
   "why_it_matters": "An amount the model invented (or that was OCR-'corrected') could be accepted into the $ total; implementing the check is not forced by any test, and removing it breaks nothing.",
   "fix": "Add to test_grounding.py a check_amount(record_text, raw/cents) suite: $6,240 in sample record 2 passes; '$6,420' or '$9,000' absent from text returns ['GROUNDING_AMOUNT_NOT_IN_TEXT']; '$1,2OO' is not auto-corrected to $1,200.",
   "acceptance_test": "pytest tests/unit/test_grounding.py -k amount fails on NotImplementedError and, once implemented, fails if the check is stubbed to return []"},
  {"severity": "major", "title": "Dedupe key is not isolated, and no 'paste record 2 twice' test (checklist #19, R-TL-7)",
   "evidence": "tests/unit/test_ingest.py:34-37 test_dedupe_requires_same_normalized_text_and_provider: docstring says 'same date+provider but different text', but case_04 records 5 and 6 differ in date too (2026-05-25 vs 2026-05-26, evals/golden/case_04...txt:23-31). A dedupe keyed on (date, provider) alone, or (date, text) alone, passes every ingest test. tests/unit/test_amounts.py:68-72 test_duplicate_charge_merged_once uses hand-built rows, not a pasted duplicate of sample record 2.",
   "why_it_matters": "R-TL-7 key is date + provider + normalized text. A date-only or provider-less key silently merges distinct visits or leaves the ER $6,240 double counted. Nothing proves the ER charge is counted once end to end.",
   "fix": "Add three cases: same date + same provider + different text stays 2; same date + same text + different provider stays 2; sample with record 2 pasted twice -> split_records/dedupe gives one merged group [2,2'] and find_amounts -> dedupe_amounts -> totals returns accepted_cents 839000 (ER once).",
   "acceptance_test": "pytest tests/unit/test_ingest.py tests/unit/test_totals.py -k 'duplicate or twice' ; mutate dedupe key to date-only and see red"},
  {"severity": "major", "title": "compose_state table incomplete: ENDPOINT_NOT_VERIFIED has no row and no context key",
   "evidence": "api.md:448 lists ENDPOINT_NOT_VERIFIED (needs_review, 'a gap's span could contain an unconfirmed date'). Script over test_confidence.py: 'uncovered by compose_state tests: [ENDPOINT_NOT_VERIFIED]'. CTX dict (test_confidence.py:17) has no field for it. AC2 says 'full compose_state table (row 17)'.",
   "why_it_matters": "A gap flag whose endpoint date is unconfirmed is exactly the case where a false 73-day flag would present as verified; the table is the only place the state is composed.",
   "fix": "Add a context key (e.g. endpoint_unverified: bool) to CTX and a needs_review case expecting ENDPOINT_NOT_VERIFIED; if it is deliberately produced elsewhere, assert that in a test and say so in the docstring.",
   "acceptance_test": "pytest tests/unit/test_confidence.py -k ENDPOINT_NOT_VERIFIED collects and fails on NotImplementedError"},
  {"severity": "minor", "title": "Boundary scanner misses stdlib network, dynamic imports and package __init__",
   "evidence": "Scratch run of tests.unit.test_boundaries.transitive: a module with `import urllib.request` -> []; `importlib.import_module('anthropic')` -> []; app/backend/__init__.py importing anthropic -> totals [] (module_path('app.backend') is None, tests/unit/test_boundaries.py:30-32). FORBIDDEN_ROOTS has urllib3, not urllib. Transitive helper->provider and `from . import sub`->anthropic ARE caught.",
   "why_it_matters": "AC4/AC7 promise 'scan transitive imports'; package __init__ chains and urllib.request are real ways an LLM/network client reaches a deterministic module. Also FORBIDDEN_APP 'app.llm' prefix would block a legitimate app.llm.lexicon loader that grounding needs for the hedge set (R-TL-8).",
   "fix": "Resolve packages to <pkg>/__init__.py, add urllib/ssl/smtplib/websockets/openai-like roots, flag importlib/__import__ calls in the AST, and allow app.llm.lexicon (data loader) explicitly.",
   "acceptance_test": "a scratch fixture tree like the one used in this review makes test_no_llm_client_direct_or_transitive fail for each of the three cases"},
  {"severity": "minor", "title": "Totals suite is synthetic only; golden totals and float guard untested",
   "evidence": "tests/unit/test_totals.py builds dicts by hand (lines 6-37). Golden totals not asserted: case_03 explicit_charges_total 335 (cents 33500, $95 rate and two OCR items excluded), case_01 310, status values 'complete'/'partial_unclear'/'none_found', ui_line 'No dollar amounts found in these records.'. test_integer_cents_no_float_drift (line 33) passes ints and cannot detect a float implementation.",
   "why_it_matters": "Float money is a red flag; the case_03 mix of rate, OCR noise and charge is the best golden for 'sum charge only'.",
   "fix": "Parametrize over case_names(): build totals input from expected amounts and assert accepted_cents == totals.explicit_charges_total*100 and status; add a test that float cents (e.g. 10.5) raise TypeError/ValueError.",
   "acceptance_test": "pytest tests/unit/test_totals.py -k golden"},
  {"severity": "minor", "title": "Several tests are tautological or weaker than their docstrings",
   "evidence": "test_gaps.py:44-46 test_dropping_an_entry_never_changes_gaps calls compute_gaps on the same data twice. test_dates.py:30-32 test_dates_inside_body_are_not_the_record_date never calls anything on the body date. test_export.py test_only_accepted_or_edited_exported_subset_equality asserts len(heads)==3, not that they are records 1, 4, 9. test_amounts.py non-money list (line 51) omits 'approx. 40%' although sample.txt:21 contains it (checklist #17). test_ingest.py:49 pieces test only checks `in raw`.",
   "why_it_matters": "A test that cannot fail gives false confidence; the docstring promises more than the assertion.",
   "fix": "Replace with real assertions: drop a record and assert the other gaps are unchanged; parse record 7 body date and assert it is not the header iso; compare heads to the expected provider/date set; add 'approx. 40%' to the non-money cases.",
   "acceptance_test": "each rewritten test fails under a one-line mutation (e.g. gaps using body date)"},
  {"severity": "minor", "title": "Input-size boundary (R-IN-4) only tested at 2,000,000 chars",
   "evidence": "tests/unit/test_ingest.py:57-58 uses 'x' * 2_000_000; api.md:37 limits max_chars 60000, max_records 40. Empty input is not tested at the unit level.",
   "why_it_matters": "An off-by-one or a wrong limit (e.g. 2 MB) passes; R-IN-4 says empty and oversize both fail visibly before any LLM call.",
   "fix": "Test 60000 passes, 60001 raises input_too_large, '' raises bad_request-style error, 41 records handled per spec.",
   "acceptance_test": "pytest tests/unit/test_ingest.py -k 'size or empty'"},
  {"severity": "nit", "title": "AC5 grep is not clean today and three golden-amount cases pass vacuously",
   "evidence": "grep -L 'R-[A-Z]*-[0-9]' tests/unit/test_*.py prints tests/unit/test_audited.py (T-048 file added after the card was closed out). test_cents_and_class_match_golden[case_02|04|06] PASS with no implementation.",
   "why_it_matters": "'Red before backend code' is slightly muddied; AC5 will fail on the next verification run.",
   "fix": "Ask T-048 owner to add an R-ID to test_audited.py; add an explicit 'no amounts found' assertion (find_amounts == []) in those cases so they go red until implemented.",
   "acceptance_test": "grep -L prints nothing; those three params fail on NotImplementedError"}
 ],
 "whats_right": [
  "Gap suite encodes 29/30/31 at both the is_gap level and the leap-year golden gap_table, and proves non-encounter records never become endpoints.",
  "Boundary test genuinely walks transitive app.* imports (relative imports handled) and caught the helper->provider and __init__-less sub->anthropic chains in my scratch run.",
  "Golden-driven design (split, kind, find_amounts, gap_table, export byte-equality, flag templates) means tests track the eval truths, and compose_state tests include JUDGE_UNAVAILABLE -> needs_review, so no silent fallback."
 ],
 "questions_for_chris": []}
```
