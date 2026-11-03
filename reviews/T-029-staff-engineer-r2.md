# T-029 round 2: staff-engineer-reviewer (Marcus Lee)

Verdict: **pass**. The three round-1 majors are now encoded in tests (commit b366b75). Two minors remain. No blockers.

Run: `.venv/bin/python -m pytest tests/unit -q` -> `215 failed, 284 passed, 4 errors`. T-030 and T-032 have since landed, so the failures are no longer all NotImplementedError. The 6 failures in test_boundaries, test_confidence, test_grounding and test_sentences are the new r2 tests (see the T-030 review): 5 are `AttributeError: ... no attribute 'check_amount'` and 1 is ENDPOINT_NOT_VERIFIED.

Round-1 majors:
1. **Amount grounding: covered.** `tests/unit/test_grounding.py:156-168` has `test_amount_present_in_record_passes` ($6,240 in record 2), `test_amount_absent_from_record_is_rejected` ($6,420, $9,000, $62,400 -> `["GROUNDING_AMOUNT_NOT_IN_TEXT"]`) and `test_noisy_amount_not_autocorrected` ($1,2OO passes as written, $1,200 is rejected). These tests fail if the check is stubbed or removed (today: AttributeError).
2. **Dedupe: mostly covered.** `test_amounts.py:75` `test_pasting_record_2_twice_counts_the_er_charge_once` appends a record 10 copy of record 2 and asserts `[2, 10] in I.dedupe(recs)`, then `dedupe_amounts` gives one row citing [2, 10], then `totals` gives `accepted_cents == 624000`. `test_amounts.py:90` `test_date_provider_only_key_would_wrongly_merge` (same date and provider, different text -> 2) kills a date+provider key. The missing case is the provider leg (see the first minor).
3. **ENDPOINT_NOT_VERIFIED: covered.** `test_confidence.py:7,15` add `endpoint_unverified` to the context, and `test_confidence.py:66` adds `(L(), X(endpoint_unverified=True), "ENDPOINT_NOT_VERIFIED")` to the needs_review table. It currently fails, which is correct: compose_state ignores the key.
4. **Boundary scan: extended.** `test_boundaries.py:10-12` now forbids `importlib`, `http`, `ctypes` and `urllib.request`. `transitive()` (lines 38-50) adds the `app.__init__` and `app.backend.__init__` chain. `test_dynamic_import_calls_are_forbidden` (line 72) flags `__import__`, `import_module`, `exec` and `eval` calls. All 13 boundary scans pass. I read this code and did not re-run my round-1 scratch fixture tree, so this is not mutation-verified.

```json
{"card": "T-029", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2: commit b366b75 (tests/unit/test_grounding.py, test_amounts.py, test_confidence.py, test_boundaries.py); r1 file reviews/T-029-staff-engineer.md",
 "exercised": [
  ".venv/bin/python -m pytest tests/unit -q (215 failed, 284 passed, 4 errors)",
  ".venv/bin/python -m pytest tests/unit/test_boundaries.py test_confidence.py test_grounding.py test_sentences.py -q (6 failed, 203 passed)",
  "grep -n 'GROUNDING_AMOUNT_NOT_IN_TEXT\\|check_amount' tests/unit/*.py -> test_grounding.py:155-168, test_confidence.py:36",
  "grep -n 'ENDPOINT_NOT_VERIFIED\\|endpoint_unverified' tests/unit/*.py -> test_confidence.py:7,15,66",
  "grep for twice/duplicate/paste in test_ingest/test_totals/test_amounts; pytest -k 'twice or dedupe or duplicate or key' (4 failed on NotImplementedError)",
  "read test_boundaries.py in full",
  "read test_ingest.py dedupe tests"],
 "verdict": "pass",
 "scores": {"golden_fidelity": 4, "ac_coverage": 4, "mutation_resistance": 4, "determinism": 5, "design_freedom": 4, "boundary_scan": 4},
 "findings": [
  {"severity": "minor", "title": "Dedupe provider isolation still unproven (same date + same text, different provider)",
   "evidence": "tests/unit/test_amounts.py:75-93 and test_ingest.py:28-37: no case has identical date and text with different providers. test_same_day_different_provider_stays_separate (test_ingest.py:26) uses sample records 1 and 2, whose texts differ, so a date+text key without provider passes every dedupe test. test_dedupe_requires_same_normalized_text_and_provider docstring still says 'same date+provider but different text', yet case_04 records 5 and 6 differ in date too.",
   "why_it_matters": "R-TL-7 key is date + provider + normalized text. Two providers who each wrote the same boilerplate on the same day would merge and a charge would be lost.",
   "fix": "Add a case with two rows (or records) with the same date and same text but different provider -> 2 groups. Fix the stale docstring.",
   "acceptance_test": "pytest tests/unit -k 'provider' ; mutate the key to (date, text) and see red"},
  {"severity": "minor", "title": "test_init_chain_is_scanned asserts nothing about the scan",
   "evidence": "tests/unit/test_boundaries.py:62-65: computes `owners` (unused) then asserts only that module_path('app.backend') is not None.",
   "why_it_matters": "Round-1 asked for package __init__ chains to be scanned; the code does it (lines 46-49) but no test fails if that loop is deleted.",
   "fix": "Assert ('app.backend.gaps', 'app.backend.__init__') or ('app.backend.__init__', <its import>) appears in transitive('app.backend.gaps'), or run transitive against a scratch tree whose __init__ imports anthropic and assert it is reported.",
   "acceptance_test": "delete lines 46-49 of test_boundaries.py and the test goes red"}
 ],
 "whats_right": [
  "Amount-grounding tests assert both the pass and the exact rejected code, and pin the no-auto-correct behavior ($1,2OO is found as written, $1,200 is rejected).",
  "Paste-twice test runs the whole chain (split -> dedupe -> dedupe_amounts -> totals) and asserts 624000, not 1248000.",
  "ENDPOINT_NOT_VERIFIED is a first-class compose_state input, so the red test forces the backend to implement it."
 ],
 "questions_for_chris": []}
```
