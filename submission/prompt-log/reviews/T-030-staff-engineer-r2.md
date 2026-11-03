# T-030 round 2 review: staff-engineer-reviewer (Marcus Lee)

Verdict: **fail**. Scope: round-2 commit 1365926 (`check_amount`, `endpoint_unverified`, strict keys).

Brief check: `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.29s` (0 failures). Both round-1 majors are resolved at the function and table level: `check_amount` exists and is tested, and `compose_state` maps `endpoint_unverified` to `ENDPOINT_NOT_VERIFIED`. The brief's pass condition is therefore met on its literal wording. The verdict is `fail` because the endpoint major's own risk is not closed in production: the only producer of `ENDPOINT_NOT_VERIFIED` (gaps.py:37) never calls `compose_state`, and the gap flag it builds carries no state at all. That is a blocker under D.2 (spec constraint, api.md:448).

Key evidence:
- `reasons` on a gap flag with an unconfirmed endpoint: `['ENDPOINT_NOT_VERIFIED']`, and `'state' in flag` is `False` (repro below).
- The entry path (`generator.py:33-34`, `_ctx`) never sets `endpoint_unverified`, and gap flags do not pass through `generator.compose`.
- `check_amount` has no production caller. A bare `240` is accepted against `$6,240` (minor, below).

## Exercised
- `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.29s` (rerun: `209 passed in 0.31s`, unmutated scratch copy).
- `grep -rn "check_amount\|compose_state\|endpoint_unverified" --include=*.py . | grep -v tests/` -> call sites listed in findings; `check_amount` only defined at `app/backend/grounding.py:110`, never called outside tests.
- `git show --stat 1365926` -> `app/backend/confidence.py | 10`, `app/backend/grounding.py | 25`.
- Read in full: `app/backend/grounding.py`, `app/backend/confidence.py`, `app/backend/gaps.py`, `app/backend/generator.py:55-110`, `app/backend/amounts.py`, `app/backend/totals.py`, `app/backend/schemas.py`, `app/db/schema.sql` (flags table), `tests/unit/test_grounding.py:150-168`, `tests/unit/test_confidence.py`.
- `.venv/bin/python -I` probe of `check_amount`: `('Charge: $6,240.', '$6,240') -> []`, `('Charge: $6,240.', '240') -> []`, `('Charge: $1,850.', '850') -> []`, `('Charge: $1,850.', '$185') -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']`, `('Charge: $1,2OO.', '$1,200') -> ['GROUNDING_AMOUNT_NOT_IN_TEXT']`, `('Charge: $1,2OO.', '$1,2OO') -> []`.
- `.venv/bin/python -I` probe of `compose_state({...ok...}, {'endpoint_unverified': True})` -> `('needs_review', ['ENDPOINT_NOT_VERIFIED'])`; with `{'injecton': True}` -> `ValueError: unknown ladder/context keys: ['injecton']`.
- Gap flag repro: three synthetic records (2026-01-01 encounter, 2026-03-15 encounter, undated with candidate 2026-02-10) passed to `gaps.gap_flags` -> keys `['category','days','evidence','explanation','from_date','id','origin','reasons','record_nos','title','to_date','type']`; `'state' in f` -> `False`; `reasons` -> `['ENDPOINT_NOT_VERIFIED']`.
- `artifacts/review-evidence/T-030-exercise.py` -> `FAILS: 0` (round 1: 2 FAIL lines, the two majors). Its `check_amount exists` and `compose_state handles endpoint_unverified` lines now PASS.
- Mutation in a scratch copy (product tree not touched): M1 `check_amount` body -> `return []` -> `4 failed, 41 passed` (3x `test_amount_absent_from_record_is_rejected`, `test_noisy_amount_not_autocorrected`). M2 remove the `endpoint_unverified` row from `confidence.py` -> `1 failed, 64 passed` (`test_needs_review_cases[ladder21-ctx21-ENDPOINT_NOT_VERIFIED]`). Restored copy -> `209 passed`.
- `grep -n "^import\|^from\|    import\|    from"` on `sentences.py`, `grounding.py`, `confidence.py`, `why.py` -> stdlib (`re`, `functools`, `pathlib`) and `yaml` only, plus local `app.backend` imports. No LLM client. `grep -n except` on the four -> no hits.
- Not run: the pipeline CLI (`app/backend/pipeline.py` is a stub that raises `NotImplementedError`); `pytest tests/unit -q` as a whole (outside the brief's four files).

```json
{"card": "T-030", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round-2 commit 1365926 (app/backend/confidence.py, app/backend/grounding.py); working tree at a2fc95a; read-through of app/backend/{gaps,generator,amounts,totals,schemas}.py and app/db/schema.sql for production callers; tests/unit/test_{sentences,grounding,confidence,boundaries}.py; artifacts/review-evidence/T-030-exercise.py; no app URL (backend only), no sample CLI run (pipeline.py is a stub)",
 "exercised": [
  "pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q -> 209 passed in 0.29s",
  "grep -rn check_amount|compose_state|endpoint_unverified --include=*.py . (non-test call sites)",
  "git show --stat 1365926",
  "read grounding.py, confidence.py, gaps.py, generator.py:55-110, amounts.py, totals.py, schemas.py, schema.sql flags table, test_grounding.py:150-168, test_confidence.py",
  ".venv/bin/python -I probes: check_amount boundary cases; compose_state endpoint_unverified and unknown-key cases",
  "gaps.gap_flags on 3 synthetic records -> flag keys, 'state' absent, reasons ['ENDPOINT_NOT_VERIFIED']",
  "artifacts/review-evidence/T-030-exercise.py -> FAILS: 0",
  "scratch-copy mutation M1 (check_amount -> []): 4 failed; M2 (endpoint row removed): 1 failed; restored: 209 passed",
  "import and except grep on sentences.py, grounding.py, confidence.py, why.py"],
 "verdict": "fail",
 "scores": {"excerpt_verification": 4, "summary_checks": 4, "splitter": 4, "compose_state_fail_closed": 4, "gap_flag_state": 1, "amount_grounding": 3, "test_coverage": 4, "no_llm_boundary": 5},
 "findings": [
  {"severity": "blocker", "title": "Gap flags are emitted with no state; ENDPOINT_NOT_VERIFIED never reaches compose_state",
   "evidence": "app/backend/gaps.py:37 `reasons.append(\"ENDPOINT_NOT_VERIFIED\")`; app/backend/gaps.py:58 `\"evidence\": ev, \"reasons\": _reasons(g, records)})` (flag dict has no 'state' key). Repro: `.venv/bin/python -I -c \"...gaps.gap_flags(recs)...\"` -> keys [... 'reasons', ...] with no 'state'; `'state' in f` -> False; `reasons` -> ['ENDPOINT_NOT_VERIFIED']. Only compose_state caller on the entry path: app/backend/generator.py:104-106, whose `_ctx` (generator.py:33-34) never sets endpoint_unverified. memory/contracts/api.md:448 `| ENDPOINT_NOT_VERIFIED | needs_review | a gap's span could contain an unconfirmed date |`. api.md flag example: `\"state\": \"verified\", \"reasons\": []`. app/db/schema.sql:38 `state TEXT, state_reasons_json TEXT,` on flags.",
   "why_it_matters": "Round 1's major was that a gap flag whose span could hide an unconfirmed date would not come out needs_review. The round-2 fix made compose_state correct, but the only code that produces ENDPOINT_NOT_VERIFIED for gap flags does not call compose_state and attaches no state. So the spec's needs_review for that case is not produced, and anything that gates on flag state (review queue, ready_to_export per api.md) cannot see an unconfirmed-endpoint gap. A false 73-day flag can therefore reach export review without a state. This is a spec violation (api.md:448 and the flag shape), not a style point. Scope note: gaps.py is T-029/T-033 code, but it is the path the round-1 major named, so the major is not closed until this is fixed.",
   "fix": "In gaps.gap_flags, set state and state_reasons on every flag. Simplest: call confidence.compose_state({'grounding_failures': [], 'schema_valid': True, 'code_reasons': [], 'judge': None}, {'endpoint_unverified': 'ENDPOINT_NOT_VERIFIED' in reasons, 'injection': 'INJECTION_SUSPECTED' in reasons}) and write the returned state and reasons onto the flag (needs_review iff reasons, else verified).",
   "acceptance_test": "New test in tests/unit/test_gaps.py: a gap whose endpoint record has date_candidates spanning the gap -> flag['state'] == 'needs_review' and 'ENDPOINT_NOT_VERIFIED' in flag['reasons']; a clean >30-day gap -> flag['state'] == 'verified' and reasons == []. Mutation check: removing the endpoint row from confidence.py (M2 above) turns it red."},
  {"severity": "minor", "title": "check_amount accepts a bare figure that sits inside a comma-grouped figure",
   "evidence": "app/backend/grounding.py:112 docstring: \"A longer figure does not vouch for a shorter one ('$185' vs '$1,850').\" Lines 116-118: `before = record_text[m.start() - 1] ...` / `if not before.isdigit() and not re.match(r\"\\d|[,.]\\d\", tail)`. Repro: check_amount('Charge: $6,240.', '240') -> []; check_amount('Charge: $1,850.', '850') -> [].",
   "why_it_matters": "The function's own contract is false for comma-grouped figures: the ',' before the match is not a digit, so the digit-run guard passes and a wrong figure is vouched for. It is not reachable from today's production path: amounts.find_amounts (app/backend/amounts.py) only returns '$'-prefixed text from the record, and app/backend/schemas.py states the generator returns no amount field. It becomes live the moment a caller passes a figure that was not extracted (e.g. an edited amount).",
   "fix": "Also reject a match where the character before is ',' or '.' and the character before that is a digit (i.e. the match is the tail of a grouped number). Keep the existing tail check.",
   "acceptance_test": "assert GR.check_amount('Charge: $6,240.', '240') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] and GR.check_amount('Charge: $1,850.', '850') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] added to tests/unit/test_grounding.py; existing $6,240 and $1,2OO cases stay green."},
  {"severity": "minor", "title": "check_amount has no production caller",
   "evidence": "grep -rn check_amount --include=*.py . (excluding tests) -> only app/backend/grounding.py:110 (definition). amounts.find_amounts (app/backend/amounts.py) and totals.py (COUNTED includes 'edited', totals.py:4) do not call it.",
   "why_it_matters": "Checklist #4 needs each amount in the text. Amounts are extracted by code from the record text, so today they pass by construction and the gate is defense-in-depth. But any path that writes a non-extracted amount into totals (e.g. an edited amount counted via COUNTED) has no gate, which is the risk round 1 named.",
   "fix": "Call check_amount on every amount that did not come from amounts.find_amounts, at the point it is written (edit or consolidation path), and reject with GROUNDING_AMOUNT_NOT_IN_TEXT. Owner: T-033 or the edit path card.",
   "acceptance_test": "A unit test that writes an edited amount whose raw text is not in the record and asserts it is rejected, not counted in totals()."}
 ],
 "whats_right": [
  "compose_state now raises on unknown ladder and context keys (app/backend/confidence.py:49-51; probe {'injecton': True} -> ValueError), and ENDPOINT_NOT_VERIFIED is a table row (confidence.py:64); removing that row turns test_needs_review_cases[ENDPOINT_NOT_VERIFIED] red.",
  "check_amount never repairs: '$1,2OO' is found as written and the corrected '$1,200' is rejected (test_grounding.py:165-168); stubbing check_amount to [] turns 4 tests red.",
  "The lexicon loader now raises on hedge or self_report entries with no pattern (app/backend/grounding.py:67-69), closing the round-1 silent-skip minor."
 ],
 "questions_for_chris": ["Which card owns the gap-flag state composition (gaps.py), T-029 or T-033? I have filed it against T-030 because it is the path the round-1 major named; re-home it if you prefer."]}
```
