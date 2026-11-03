# T-073 review: narrow the broad except in the review.py judge path (staff-engineer)

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit reviewed: 7724412 (T-073). HEAD at review time was ec33bf0 (T-084); the T-073 files are unchanged between 7724412 and ec33bf0 (`git diff --stat 7724412 ec33bf0 -- app/backend/review.py app/backend/judge_guard.py app/backend/judges.py app/llm/audited.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py` prints nothing). The working tree moved during the review (other workers' uncommitted changes, including app/backend/reclassify.py and tests/unit/test_reclassify.py), so I pinned HEAD with `git archive ec33bf0` into the session scratchpad.

## Summary

The guard itself is narrow and does what the card says at the seam it is tested at: `judge_guard.guarded` (judge_guard.py:15-16) returns `unavailable` with the class name for `LLMFailed`, `LLMError` and `FixtureMissing`, and lets everything else raise. Four deliberate mutations of the guard are all caught (4/4).

The acceptance criterion does not hold on the real call path, though. Two gaps:
1. A programmer bug raised inside the real judge call is not propagated. `app/llm/audited.py:70` has its own `except Exception`, which retries the call three times and reports it as a judge that did not answer. The unit test that claims propagation fakes the call one layer above, so it never reaches that code.
2. `LLMFailed`, the error the card's AC names as recorded with `ladder.judge.error_class`, never reaches the guard. `judges._run` turns it into `unavailable` with reason `NONE` and no class.

Neither gap lets an unverified item through as verified (the state is `needs_review`), so both are major, not blocker. Verdict: changes.

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-073` (card AC, handoff, note "Left: LLMFailed is already swallowed inside judges._run").
- `git show --stat 7724412`; `git show 7724412 -- app/backend/judge_guard.py app/backend/review.py tests/unit/test_review_rules.py`; `cat -n tests/unit/test_judge_guard.py`; `cat -n app/backend/judge_guard.py`.
- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` in the working tree: `109 passed, 1173 deselected`.
- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass" --collect-only -q | grep -c judge_guard`: `0`. The brief's `-k` selector does not collect `tests/unit/test_judge_guard.py` at all, so I also ran that file on its own: `.venv/bin/python -m pytest -q tests/unit/test_judge_guard.py` gives `10 passed`.
- HEAD archive (`git archive ec33bf0` into the scratchpad, `head-ec33bf0`): `-k "review or reclass"` gives `107 passed, 1068 deselected`; `test_judge_guard.py` gives `10 passed`.
- Scratch mutants (`artifacts/review-evidence/T-073-T-084/mutate.py`, log in `artifacts/review-evidence/T-073-T-084/mutation-run.txt`), run on the HEAD archive with `test_judge_guard.py` and `test_review_rules.py`. Control: `55 passed`.
  - A, `judge_guard.py` `except EXPECTED_JUDGE_ERRORS` changed to `except Exception`: `4 failed` (the three unexpected-error cases and the edit-propagates case).
  - B, `review.py:100` guard call replaced by a direct `judges.run_j1_meta` call: `3 failed`.
  - C, expected errors return `supported` instead of `unavailable`: `6 failed`.
  - D, error class dropped (`None` instead of `type(e).__name__`): `4 failed`.
- Probes on the HEAD archive (`artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py`, `probe_t073_adapter_bug_through_audited.py`; output in `artifacts/review-evidence/T-073-T-084/probe-run.txt`).
- `grep -n "except" app/backend/review.py app/backend/judge_guard.py app/backend/judges.py app/llm/audited.py` and `git show 7724412:app/llm/audited.py | grep -n "except Exception as e:"` (line 70).

## Findings

### F1 (major): a programmer bug in the real judge call is retried and hidden as JUDGE_UNAVAILABLE

- `app/llm/audited.py:70`: `        except Exception as e:                         # only our own error codes are stored, never model- or record-derived text`. Any exception from the provider call or `validate` is caught here, recorded as `_error_code(e)`, and retried (`MAX_ATTEMPTS = 3` at audited.py:15, `raise LLMFailed(...)` at audited.py:92).
- `app/backend/judges.py:33-34`: `except AU.LLMFailed:` then `return "unavailable", None, "NONE"`. The reason is `NONE` and the class is not kept on the ladder.
- Reproduction: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py` run against the HEAD archive. A provider adapter raising `RuntimeError("programmer bug in provider adapter")`, called through the real `AU.audited_call`, gives:
  - `llm_calls: [{'step': 'j1', 'attempt': 1, 'error': 'RuntimeError'}, {'step': 'j1', 'attempt': 2, 'error': 'RuntimeError'}, {'step': 'j1', 'attempt': 3, 'error': 'RuntimeError'}]`
  - `warnings: ['JUDGE_UNAVAILABLE'] state: needs_review judge: {'verdict': 'unavailable', 'reason_code': 'NONE'} error_class in ladder: False`
- The propagation test in the card (`tests/unit/test_judge_guard.py:45-52`) raises `RuntimeError` from a raw fake call that is passed straight to `apply_review`. It never enters `audited_call`, so the mutation that matters here is invisible to it.
- Why it matters: the AC says "others propagate". On the production path they are retried three times and shown to the paralegal as a judge that did not answer, with the reason `NONE`. The class survives only in the `llm_calls` rows. This is the "swallowed exception" pattern from the dossier (§3, checklist item 12). It is not a verified-item leak, so it is major.
- Fix: narrow `audited.py:70` to provider and LLM errors (`P.LLMError` and our own codes). Let every other exception propagate out of `audited_call` without a retry. The owner is backend, but `app/llm/**` and `judges.py` are outside this card's stated scope (handoff: "judges.py off limits"), so this needs its own card.
- Acceptance test: `audited_call` with a `complete_with_meta` that raises `RuntimeError` raises `RuntimeError` to the caller and writes exactly one `llm_calls` row. The same provider through `apply_review` raises and saves nothing (the card's own propagation assertion, now on the real path).

### F2 (major): error_class is not recorded for LLMFailed, which the AC names

- Card AC (`board.py show T-073`, ac[0].text): "LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class". The AC evidence says the same.
- `app/backend/judges.py:33-34` returns before the guard sees the exception, so `judge_guard.py:15` never handles `LLMFailed` on the production path.
- Reproduction: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py`. With `FakeCall({"j1": AU.LLMFailed("down")})`: `LLMFailed path judge ladder: {'reason_code': 'NONE', 'verdict': 'unavailable'} warnings: ['JUDGE_UNAVAILABLE'] state: needs_review`. There is no `error_class`. The same probe with `P.LLMError("TIMEOUT")` does record `'error_class': 'LLMError'`, because that one escapes `_run`.
- Tests do not catch it. `tests/unit/test_judge_guard.py:15-16` asserts only the reason code `NONE` for `LLMFailed`. `tests/unit/test_review_rules.py:148-156` (the parametrized `AU.LLMFailed` case) asserts state, reasons and verdict, not `error_class`.
- The handoff's "Left" note admits this, but the AC evidence still lists `LLMFailed` as recorded with its class. The evidence overstates what the code does.
- Fix: have `judges._run` return the class (for example `"LLMFailed"`) or re-raise `LLMFailed` to the guard, so the ladder carries `error_class` for every expected failure. If that stays out of scope, correct the AC evidence now.
- Acceptance test: add `assert it["ladder"]["judge"]["error_class"] == "LLMFailed"` to the `AU.LLMFailed` case in `tests/unit/test_review_rules.py:148`. It fails on HEAD today.

### F3 (minor): the brief's test selector drops the T-073 guard tests

- `.venv/bin/python -m pytest -q tests/unit -k "review or reclass"` collects 0 tests from `tests/unit/test_judge_guard.py` (see Exercised). The guard's 10 tests run only when the file is named explicitly.
- Fix: add `or guard` to the selector (or name `test_judge_guard.py` in the brief). Not a product defect; it is a verification gap in how the card was checked.

## What is right

- `app/backend/judge_guard.py:15-16` maps expected errors to `unavailable` with the class name, never to a positive verdict. Mutant C (expected becomes `supported`) is caught by 6 tests.
- Unexpected errors at the guard seam propagate and save nothing: `tests/unit/test_judge_guard.py:31-33` and `:45-52`. Mutant A (broad catch) is caught by 4 tests.
- Mutants B (guard removed from `review.py:100`) and D (class dropped) are both caught, so the wiring at `review.py:100` and the ladder write are tested, not just the helper.

## Scores

```
no_silent_fallback 3 (expected errors visible as needs_review; the unexpected path is not)
error_class_recorded 2 (only when the error escapes judges._run)
propagation_on_real_path 2 (audited.py:70 retries bugs)
tests_kill_mutants 4 (4/4 seam mutants caught; real-path mutant not covered)
ac_evidence_matches_code 2 (LLMFailed class claim)
```

## Questions for Chris

- Should a judge that hits a programmer bug show `JUDGE_UNAVAILABLE` (ADR-005 wording, the paralegal can retry) or a visible error state (a bug, not a judge outcome)? The answer decides where F1 is fixed.

<!-- Verdict rule: 0 blockers, 2 majors -> changes. -->

```json
{"card": "T-073", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 7724412 (T-073), pinned HEAD ec33bf0 via git archive; files app/backend/judge_guard.py, app/backend/review.py, tests/unit/test_judge_guard.py, tests/unit/test_review_rules.py; app/llm/audited.py and app/backend/judges.py read for the real path; no app URL; no sample case (unit-level card)",
 "exercised": ["python3 tools/board.py show T-073", "git show --stat 7724412; git show 7724412 -- app/backend/judge_guard.py app/backend/review.py tests/unit/test_review_rules.py", "cat -n app/backend/judge_guard.py tests/unit/test_judge_guard.py", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' (working tree: 109 passed, 1173 deselected)", ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' --collect-only -q | grep -c judge_guard (0)", ".venv/bin/python -m pytest -q tests/unit/test_judge_guard.py (10 passed)", "git archive ec33bf0 into scratchpad head-ec33bf0: -k 'review or reclass' 107 passed; test_judge_guard.py 10 passed", "scratch mutants A-D via artifacts/review-evidence/T-073-T-084/mutate.py: A 4 failed, B 3 failed, C 6 failed, D 4 failed; control 55 passed", "probes: artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py (3x RuntimeError in llm_calls, JUDGE_UNAVAILABLE, no class), probe_t073_llmfailed_class.py (LLMFailed: no error_class)", "grep -n except on review.py, judge_guard.py, judges.py, audited.py; git show 7724412:app/llm/audited.py line 70"],
 "verdict": "changes",
 "scores": {"no_silent_fallback": 3, "error_class_recorded": 2, "propagation_on_real_path": 2, "tests_kill_mutants": 4, "ac_evidence_matches_code": 2},
 "findings": [
  {"severity": "major", "title": "A programmer bug in the real judge call is retried 3x and hidden as JUDGE_UNAVAILABLE (broad except one layer down)",
   "evidence": "app/llm/audited.py:70 `except Exception as e:` (then retry, MAX_ATTEMPTS=3 at audited.py:15, raise LLMFailed at audited.py:92); app/backend/judges.py:33-34 `except AU.LLMFailed:` -> return unavailable/NONE; repro artifacts/review-evidence/T-073-T-084/probe_t073_adapter_bug_through_audited.py -> llm_calls error RuntimeError x3, warnings ['JUDGE_UNAVAILABLE'], state needs_review, error_class absent; tests/unit/test_judge_guard.py:45-52 raises from a raw fake call that bypasses audited_call",
   "why_it_matters": "The AC says anything other than an expected judge error propagates. On the production path a bug is retried and reported to the paralegal as a judge that did not answer, with reason NONE. The class survives only in llm_calls. Not a verified-item leak (state is needs_review), so major, not blocker.",
   "fix": "Narrow audited.py:70 to provider/LLM errors (P.LLMError and our own codes); let other exceptions propagate without retry. app/llm and judges.py are outside this card's stated scope, so raise it as its own backend card.",
   "acceptance_test": "audited_call with complete_with_meta raising RuntimeError raises RuntimeError to the caller and writes one llm_calls row; the same provider through apply_review raises and saves nothing."},
  {"severity": "major", "title": "error_class is not recorded for LLMFailed, which the AC names explicitly",
   "evidence": "card T-073 ac[0].text: 'LLMFailed/FixtureMissing/LLMError -> JUDGE_UNAVAILABLE with ladder.judge.error_class'; app/backend/judges.py:33-34 returns before the guard sees the exception; repro artifacts/review-evidence/T-073-T-084/probe_t073_llmfailed_class.py -> 'LLMFailed path judge ladder: {'reason_code': 'NONE', 'verdict': 'unavailable'} ... state: needs_review'; tests/unit/test_judge_guard.py:15-16 asserts only code NONE; tests/unit/test_review_rules.py:148-156 does not assert error_class",
   "why_it_matters": "The class is the audit's answer to 'why did the judge not run'. For the most common expected failure (LLMFailed after retries) the ladder records NONE. The AC evidence claims otherwise.",
   "fix": "Make judges._run return the class (e.g. 'LLMFailed') or re-raise LLMFailed to the guard, so every expected failure lands in ladder.judge.error_class. If deferred, correct the AC evidence now.",
   "acceptance_test": "In tests/unit/test_review_rules.py:148 (the AU.LLMFailed case) assert it['ladder']['judge']['error_class'] == 'LLMFailed'; fails on HEAD today."},
  {"severity": "minor", "title": "The brief's -k selector collects zero tests from test_judge_guard.py",
   "evidence": ".venv/bin/python -m pytest -q tests/unit -k 'review or reclass' --collect-only -q | grep -c judge_guard -> 0; .venv/bin/python -m pytest -q tests/unit/test_judge_guard.py -> 10 passed",
   "why_it_matters": "The guard file that holds the T-073 behaviour tests is skipped by the standard selection for this card, so a regression there does not show in the card's selector run.",
   "fix": "Add 'or guard' to the -k expression, or list tests/unit/test_judge_guard.py explicitly.",
   "acceptance_test": "The selector collects at least the 10 test_judge_guard.py tests (--collect-only shows them)."}
 ],
 "whats_right": [
  "app/backend/judge_guard.py:15-16 maps expected errors to unavailable with the class name and never to a positive verdict (mutant C caught by 6 tests).",
  "Unexpected errors at the guard seam propagate and save nothing (tests/unit/test_judge_guard.py:31-33 and :45-52); mutant A (broad catch) caught by 4 tests.",
  "Mutants B (guard removed at review.py:100) and D (class dropped) are both caught, so the wiring and the ladder write are tested, not only the helper."
 ],
 "questions_for_chris": ["For a judge that hits a programmer bug, should the paralegal see JUDGE_UNAVAILABLE (retryable, ADR-005 wording) or a visible error state (a bug, not a judge outcome)? The answer decides where F1 is fixed."]}
```
