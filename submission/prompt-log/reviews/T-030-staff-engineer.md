# T-030 review: staff-engineer-reviewer (Marcus Lee)

Verdict: **changes**. No blockers. Two majors: `check_amount` is not implemented (checklist #4), and `compose_state` has no code path for `endpoint_unverified`, so it fails open to `verified`. Both are red in the shipped suite.

Core behaviour is right. Exercised with `artifacts/review-evidence/T-030-exercise.py`:
- All 68 golden excerpts verify clean against their own record text.
- Non-verbatim quotes (changed words, lower-cased, truncated) return exactly `GROUNDING_EXCERPT_NOT_VERBATIM`.
- Dropping "may represent degenerative change; correlate clinically." from record 8 returns `EXCERPT_OMITS_QUALIFIER`. A half hedge also returns it. The hedge alone is clean.
- A mid-unit excerpt returns `EXCERPT_NOT_WHOLE_SENTENCE`, which maps to needs_review.
- A summary "Pain 4/10." over "Pain 3/10." returns `SUMMARY_TOKEN_NOT_IN_EXCERPT`. A summary dropping "without loss of consciousness" returns `SUMMARY_DROPS_QUALIFIER`. `compose_state` makes both `needs_review`. "Visit 8" as a label passes.
- "approx. 35 mph." is one unit. "10 mg. in the morning" is one unit. "10 mg. Follow" splits in two. That matches the revised test and conflicts with the REQ abbreviation list, as the backend handoff says.
- Units tile every golden excerpt.
- `check_excerpt` never mutates its input and returns only codes.
- The output is byte-identical across two runs.
- The four modules import no LLM client (`re`, `yaml`, `functools`, `pathlib`, `app.backend.grounding` only).
- Mutation: replacing the hedge test with `if False:` in a scratch copy turned `test_entry8_without_hedge_needs_review` and `test_entry8_with_half_the_hedge_still_omits` red.

Run: `pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `6 failed, 203 passed`. The 6 are the T-029 r2 tests added in b366b75 after T-030's commit 217e243. The card evidence says "200 pass", which is stale.

```json
{"card": "T-030", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/{sentences,grounding,confidence,why}.py at commit 217e243 (working tree at b366b75); tests/unit/test_{sentences,grounding,confidence,boundaries}.py; evals/golden",
 "exercised": [
  "python3 tools/board.py show T-030",
  ".venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q (6 failed, 203 passed)",
  ".venv/bin/python artifacts/review-evidence/T-030-exercise.py (golden excerpts, non-verbatim, hedge drop, summary tokens, splitter, no-repair, imports, determinism; 2 FAIL lines = the two majors); run twice, identical md5",
  "read grounding.py, sentences.py, confidence.py in full; grep except/continue",
  "mutation in scratch copy (is_hedge_unit gate -> False): 2 hedge tests red",
  "compose_state with a misspelled context key -> ('verified', [])",
  "python3 tools/board.py validate -> ok (49 file(s))"],
 "verdict": "changes",
 "scores": {"excerpt_verification": 4, "summary_checks": 4, "splitter": 4, "compose_state_fail_closed": 2, "test_coverage": 3, "no_llm_boundary": 5},
 "findings": [
  {"severity": "major", "title": "Amount-in-text grounding check (check_amount) not implemented",
   "evidence": "grounding.py has no check_amount (exercise script: 'FAIL check_amount exists'). pytest: tests/unit/test_grounding.py::test_amount_present_in_record_passes, ::test_amount_absent_from_record_is_rejected[$6,420|$9,000|$62,400] and ::test_noisy_amount_not_autocorrected fail with AttributeError: module 'app.backend.grounding' has no attribute 'check_amount' (test_grounding.py:158-168).",
   "why_it_matters": "Checklist #4 requires each amount to appear in its record's text, or an amount the model invented or 'corrected' ($1,2OO -> $1,200) reaches the total with no code gate. GROUNDING_AMOUNT_NOT_IN_TEXT is in REJECTED_CODES but nothing produces it.",
   "fix": "Add check_amount(record_text, raw_amount) -> [] or ['GROUNDING_AMOUNT_NOT_IN_TEXT'] using the same whitespace normalization as locate; no digit repair.",
   "acceptance_test": "pytest tests/unit/test_grounding.py -k amount green; stubbing check_amount to return [] makes test_amount_absent_from_record_is_rejected red"},
  {"severity": "major", "title": "compose_state ignores endpoint_unverified and fails open to verified",
   "evidence": "confidence.py:42-60 never reads ctx['endpoint_unverified']. Repro: C.compose_state({'grounding_failures':[],'schema_valid':True,'code_reasons':[],'judge':'supported'},{'endpoint_unverified':True}) -> ('verified', []). pytest tests/unit/test_confidence.py::test_needs_review_cases[ladder21-ctx21-ENDPOINT_NOT_VERIFIED] fails (test_confidence.py:66).",
   "why_it_matters": "A gap flag whose span could contain an unconfirmed date is the case where a false 73-day flag would show as verified. ENDPOINT_NOT_VERIFIED is in REASON_CODES but can never be produced (api.md:448).",
   "fix": "Add ('endpoint_unverified', 'ENDPOINT_NOT_VERIFIED') to the boolean table at confidence.py:55.",
   "acceptance_test": "pytest tests/unit/test_confidence.py green"},
  {"severity": "minor", "title": "compose_state silently ignores unknown or misspelled ladder and context keys",
   "evidence": "compose_state({...ok...}, {'injecton': True}) -> ('verified', []). Booleans read with ctx.get(key); date_status/amount_class/agreement default to 'no doubt' when absent (confidence.py:52-57). This is how the endpoint_unverified gap above went unnoticed.",
   "why_it_matters": "A typo in the pipeline caller produces verified with no error: a silent fallback by omission. 'Unknown value' already raises ValueError, but unknown keys do not.",
   "fix": "Raise ValueError on keys outside the documented ladder/context sets (or require all keys). Keep judge=None as the documented 'no judge needed' case.",
   "acceptance_test": "new test: compose_state(L(), {'injecton': True}) raises ValueError"},
  {"severity": "minor", "title": "Lexicon loader silently skips malformed entries, including hedge: true entries",
   "evidence": "grounding.py:66 `if not isinstance(e, dict) or 'pattern' not in e: continue`; _lexicon is lru_cached (line 62).",
   "why_it_matters": "A hedge: true entry with a typo'd key is dropped from the hedge set and EXCERPT_OMITS_QUALIFIER stops firing for it, with no error.",
   "fix": "Raise on an entry with hedge: true or self_report: true and no valid pattern; keep skipping only comment/metadata rows explicitly.",
   "acceptance_test": "test with a tmp lexicon that has hedge: true and no pattern raises"},
  {"severity": "minor", "title": "Summary-side hedge/negation/self-report detection uses hardcoded word lists, not the lexicon",
   "evidence": "grounding.py:152 _HEDGE_WORDS, _SELF, _NEG, _LATERAL, _APPROX regexes are in code; line 163 accepts `hedge_ids(summary) or _HEDGE_WORDS.search(summary)`. AC1 says the hedge set is read from lexicon.yaml `hedge: true` (R-TL-8).",
   "why_it_matters": "Two hedge vocabularies can drift: a lexicon edit changes the excerpt check but not the summary check, and the summary check passes on any of 'may|likely|appears|...' even when the lexicon hedge in the excerpt is a different concept.",
   "fix": "Use hedge_ids(summary) only (or document _HEDGE_WORDS as the intentional looser summary-side set in the module docstring and test its boundary).",
   "acceptance_test": "test: excerpt hedge 'cannot be excluded' with summary 'may be present' -> decided and asserted either way"},
  {"severity": "minor", "title": "AC-named tests do not exist; the no-silent-repair claim has no direct test",
   "evidence": "AC cites test_grounding::test_no_silent_fix, ::test_summary_tokens, ::test_offsets_golden, ::test_offset_lookup_failure. grep 'silent|unchanged' tests/unit/test_grounding.py -> nothing. Tests have different names (test_changed_pain_score_flags, test_locate_mutated_record_returns_none). Handoff itself notes this.",
   "why_it_matters": "AC5 'a failing quote is never repaired' rests on test_not_verbatim_is_rejected only. A function that returned the corrected text alongside the code would still pass.",
   "fix": "Add a test that check_excerpt on a near-miss returns only reason codes (list of str) and leaves the input unchanged, and align AC text with the real test names.",
   "acceptance_test": "pytest tests/unit/test_grounding.py -k 'repair or silent'"},
  {"severity": "nit", "title": "Card evidence is stale",
   "evidence": "T-030 AC evidence says '200 pass, 1 test_sentences hedge-split test wrong'. Today: 6 failed, 203 passed (the 6 are the two majors above). test_sentences passes now.",
   "why_it_matters": "A reader trusts a green claim that no longer holds.",
   "fix": "Re-run and update the evidence after fixing the majors.",
   "acceptance_test": "pytest ... -q prints 'passed' with no failures"}
 ],
 "whats_right": [
  "check_excerpt is a pure function of (record, excerpt): verbatim after whitespace normalization, offsets mapped back to raw text, returns codes only and never rewrites the quote.",
  "Hedge omission and summary qualifier/token checks behave as the AC states on the real record 8, record 2 and 'Pain 3/10.' cases, and fail when the hedge gate is removed.",
  "compose_state raises on unknown reason codes and unknown judge/date/amount values, and the four modules import no LLM client, network or app.llm code."
 ],
 "questions_for_chris": []}
```
