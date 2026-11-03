# T-030 round 3 review: staff-engineer-reviewer (Marcus Lee), re-scoped by orchestrator triage

Verdict: **pass** on T-030's own modules (`sentences.py`, `grounding.py`, `confidence.py`, `why.py`) and AC. No blocker, no major. Three minors and one nit.

Scope decision recorded, not a resolution. The orchestrator moved the r2 blocker (gap flags from `gaps.py:37/58` never reach `compose_state`) to T-037 AC 8. I checked that the AC is on the card: `python3 tools/board.py show T-037` lists `{"n": 8, "text": "From T-030 r2 review: gap flags emitted by gaps.py with ENDPOINT_NOT_VERIFIED get a state via compose_state in finalize; test_pipeline asserts every flag has a state", "done": false}`. I have not dropped the finding. Its severity stays **blocker** for T-037 and it is not counted in this T-030 verdict. T-030's round-1 major is closed at the `compose_state` table level only; the product-level closure is open under T-037 AC 8.

Brief run: `.venv/bin/python -m pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q` -> `209 passed in 0.30s`.

## Exercised this round
- `pytest` on the four files: `209 passed in 0.30s`.
- `python3 tools/board.py show T-030` and `show T-037` (read-only); T-037 AC 8 quoted above.
- `grep -n "def test_\(summary_tokens\|offsets_golden\|offset_lookup_failure\|no_silent_fix\)"` over the four files -> no output. Names present instead: `test_offset_round_trip_for_every_unit_run` (test_grounding.py:61), `test_locate_mutated_record_returns_none` (:79), `test_changed_pain_score_flags` (:91).
- `grep -rn sort_key --include=*.py .` -> `app/backend/confidence.py:23` is the only definition; no caller and no test.
- Re-read `app/backend/grounding.py:110-120` (`check_amount`) and `tests/unit/test_confidence.py` for the reason-code table.
- Carried from r2 without rerunning: the gap-flag repro (`gaps.gap_flags` yields `reasons` with no `state`), the `check_amount` probes, and the scratch mutations (M1 4 red, M2 1 red).

## AC status (T-030 card)
- AC1 (sentences + grounding green, verbatim, whole-sentence, mid-unit, hedge via lexicon): met. Suite green; hedge set comes from `hedge_ids` over lexicon entries (`grounding.py:78-79`).
- AC2 (summary tokens, qualifier, "Visit 8"): met on behaviour. The AC names `test_grounding::test_summary_tokens`, which does not exist; behaviour is covered by `test_changed_pain_score_flags`. See minor 2.
- AC3 (offsets golden, lookup failure): met on behaviour via `test_offset_round_trip_for_every_unit_run` and `test_locate_mutated_record_returns_none`. The AC-named tests `test_offsets_golden` and `test_offset_lookup_failure` do not exist. See minor 2.
- AC4 (compose_state table, needs_review sorts first, why template per code): table met; every REASON_CODE is reachable through a ladder/context row and tested (`test_needs_review_cases`, 22 rows, plus rejected and why-template tests). "Sorts first" is implemented by `sort_key` (`confidence.py:23`) but has no caller and no test. See minor 3.
- AC5 (no silent repair, `test_no_silent_fix`): behaviour correct (`check_excerpt` returns codes only and never mutates its input; the r1 exercise and the round-2 read confirm this). The AC-named test does not exist; the handoff says so ("Not done: AC-named no-silent-repair test"). See minor 2.

```json
{"card": "T-030", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "T-030's own modules at round 3: app/backend/{sentences,grounding,confidence,why}.py at HEAD a2fc95a (round-2 fix commit 1365926); tests/unit/test_{sentences,grounding,confidence,boundaries}.py; T-030 card AC1-AC5; T-037 AC 8 as the re-homed endpoint item (not scored here); no app URL, no pipeline CLI (pipeline.py is a stub)",
 "exercised": [
  "pytest tests/unit/test_sentences.py tests/unit/test_grounding.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -q -> 209 passed in 0.30s",
  "python3 tools/board.py show T-030 (AC1-AC5 read)",
  "python3 tools/board.py show T-037 (AC 8 confirmed)",
  "grep -n def test_(summary_tokens|offsets_golden|offset_lookup_failure|no_silent_fix) over the four test files -> no matches",
  "grep -rn sort_key --include=*.py . -> only app/backend/confidence.py:23",
  "read app/backend/grounding.py:110-120 and tests/unit/test_confidence.py (reason-code table)"],
 "verdict": "pass",
 "scores": {"excerpt_verification": 4, "summary_checks": 4, "splitter": 4, "compose_state_fail_closed": 4, "test_coverage": 3, "amount_grounding": 3, "no_llm_boundary": 5},
 "findings": [
  {"severity": "minor", "title": "check_amount accepts a bare figure inside a comma-grouped figure",
   "evidence": "app/backend/grounding.py:112 docstring: \"A longer figure does not vouch for a shorter one ('$185' vs '$1,850').\" Lines 116-118: `before = record_text[m.start() - 1] ...` and `if not before.isdigit() and not re.match(r\"\\d|[,.]\\d\", tail)`. Repro: check_amount('Charge: $6,240.', '240') -> []; check_amount('Charge: $1,850.', '850') -> [] (r2 probe).",
   "why_it_matters": "The function's own stated contract is false for comma-grouped figures, so the gate would vouch for a wrong figure if a caller ever passes a non-extracted amount. Not reachable from today's extraction path (amounts.find_amounts returns '$'-prefixed record text), so minor.",
   "fix": "In check_amount, also reject a match whose preceding character is ',' or '.' when the character before that is a digit.",
   "acceptance_test": "tests/unit/test_grounding.py: assert check_amount('Charge: $6,240.', '240') == ['GROUNDING_AMOUNT_NOT_IN_TEXT'] and check_amount('Charge: $1,850.', '850') == ['GROUNDING_AMOUNT_NOT_IN_TEXT']; existing $6,240 and $1,2OO cases stay green."},
  {"severity": "minor", "title": "T-030 card AC names four tests that do not exist, while marking the ACs done",
   "evidence": "grep -n 'def test_\\(summary_tokens\\|offsets_golden\\|offset_lookup_failure\\|no_silent_fix\\)' tests/unit/test_grounding.py tests/unit/test_sentences.py tests/unit/test_confidence.py tests/unit/test_boundaries.py -> no output. T-030 card AC2/AC3/AC5 each name one of these and carry \"done\": true. Handoff: \"Not done: AC-named no-silent-repair test\".",
   "why_it_matters": "AC5's invariant (a failing quote is never repaired) is correct in behaviour but its named proof does not exist, so a future change that returned corrected text with the code would not be caught by the test the card cites.",
   "fix": "Add a test that check_excerpt on a near-miss returns a list of str codes equal to the input's reason set and leaves the input unchanged, and either name it test_no_silent_fix or update the AC text to the real test names.",
   "acceptance_test": "pytest tests/unit/test_grounding.py -k 'silent or repair' passes; a mutant check_excerpt that also returns corrected text fails it."},
  {"severity": "minor", "title": "AC4 'needs_review sorts first' has no caller and no test",
   "evidence": "app/backend/confidence.py:23-25 `def sort_key(state: str) -> int: return STATE_ORDER[state]`. grep -rn sort_key --include=*.py . -> no caller and no test. T-030 AC4 names this behaviour.",
   "why_it_matters": "The ordering the queue relies on is defined but neither used nor asserted, so a regression to the order would pass the suite.",
   "fix": "Add a test asserting sorted(['verified','needs_review','rejected'], key=sort_key) == ['needs_review','verified','rejected'], and leave the caller to the review-queue card.",
   "acceptance_test": "pytest tests/unit/test_confidence.py -k sort green."},
  {"severity": "nit", "title": "Card evidence strings are stale",
   "evidence": "T-030 AC1-AC5 evidence reads \"200 pass, 1 test_sentences hedge-split test wrong\". Current run: 209 passed, 0 failed; test_sentences.py:46 test_hedge_sentence_splits_at_semicolon passes.",
   "why_it_matters": "A reader trusts a count and a failure note that no longer hold.",
   "fix": "Update the AC evidence to the 209-pass line quoted above.",
   "acceptance_test": "pytest on the four files prints '209 passed' or the current count, with no failures."}
 ],
 "whats_right": [
  "compose_state covers every REASON_CODE reachable through a ladder or context row, rejects unknown keys (confidence.py:49-51), and is tested row by row (test_needs_review_cases, 22 rows).",
  "check_excerpt returns only reason codes and never rewrites the quote; '$1,2OO' is found as written and the corrected '$1,200' is rejected (test_grounding.py:165-168).",
  "The lexicon loader raises on a hedge or self_report entry with no pattern (grounding.py:67-69), so the hedge set cannot silently shrink."],
 "questions_for_chris": ["The check_amount caller gap (no production call site; amounts are code-extracted, the edit path is ungated) is outside T-030's modules and is not on the T-033 card. Should it go on T-033's AC?"]}
```
