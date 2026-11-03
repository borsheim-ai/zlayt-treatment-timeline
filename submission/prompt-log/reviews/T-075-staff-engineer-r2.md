# T-075 review round 2: staff-engineer-reviewer (commit b5b9b34)

Verdict: **pass**. No blocker, no major. Two nits.

All three confirmations hold:
- Removing the model-flag sort (`app/backend/flags.py:125`) makes `test_model_flag_order_does_not_change_the_flag_list` fail.
- Reverting J3 (`judges.py:59`) or J4 (`judges.py:64`) to `_v1` makes `test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names` fail.
- The card and `evals/reports/determinism-diagnosis.md` now say the cause of the 0.0 is unconfirmed and the changes are mitigations.

Round-1 findings 1, 2 and 4 are moved to T-093 and T-094 and are not re-scored. Round-1 minor 6 (no negative control for J3/J4) is covered by T-093 AC 2 and is not re-scored either. The main working tree is dirty with other agents' edits, so every check was run on a `git archive b5b9b34` copy in the scratchpad, not on the live tree.

Mutation results (scratch copies, one change each):
- `m_sort`: `uniq.sort(key=` replaced by a no-op call. `pytest tests/unit/test_t075_determinism.py` gives `1 failed, 4 passed`; the failure is `test_model_flag_order_does_not_change_the_flag_list`.
- `m_j3`: `_run("j3", "judge_conflict_v2"` changed to `judge_conflict_v1` (judges.py:59). `1 failed, 4 passed`; the failure is `test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names`.
- `m_j4`: `_run("j4", "judge_flag_v2"` changed to `judge_flag_v1` (judges.py:64). `1 failed, 4 passed`; same failing test.
- Baseline on the unmodified archive: `5 passed`. Each scratch copy imported its own `app` package (checked with `import app.backend.flags as f; print(f.__file__)`).

Other checks:
- `.venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py`: `5 passed`, repeated three times with `5 passed` each.
- `.venv/bin/python -m pytest tests/unit -q`: `1043 passed`, matching the card.
- The T-075 test file has no `sleep`, `time`, `random`, `except` or `float(` in its own code. The only `sleep` is a `lambda` keyword argument that the test replaces with a test double.
- The new sort test has a control: `assert len(model_only) == 3` before it loops over all six permutations with a duplicate.
- The new prompt test checks in both directions. The text the judge sent must equal `promptlib.load(pv).text`, where `pv` is the version the audit record names. A v1 revert in `judges.py` fails it, and so does a wrong version in `flags.py:292,295,300`.
- Card T-075 AC 2 evidence and note, and `determinism-diagnosis.md` line 3, say the cause is unconfirmed and that the 1.0 cannot tell changed code from unchanged code.

Nits (optional, not verdict-affecting):
1. Card T-075 AC 2 text still reads "Fix lands so ... gives determinism_3run 1.0". The evidence line now says the 1.0 does not show the fix. The wording is honest, but the AC text itself still frames the 1.0 as the fix's result.
2. The retry test (`tests/unit/test_t075_determinism.py:60-69`) asserts only `callable(seen[1])`. The values `RETRY_DELAYS_S = (0.5, 1.5)` are not asserted. This was round-1 minor 7's optional item.

```json
{"card": "T-075", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit b5b9b34 (tests/unit/test_t075_determinism.py, evals/reports/determinism-diagnosis.md) and the T-075 card notes; pinned via git archive b5b9b34 in the scratchpad; no app URL; no live eval run this round",
 "exercised": [
   "git rev-parse --short HEAD -> b5b9b34; git show --stat b5b9b34 (2 files, 44 insertions, 16 deletions); git show b5b9b34 -- tests/unit/test_t075_determinism.py evals/reports/determinism-diagnosis.md (full diff read)",
   "cat -n tests/unit/test_t075_determinism.py (full file, 88 lines)",
   ".venv/bin/python tools/board.py show T-075; show T-093; show T-094",
   ".venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py -> 5 passed (run 3 times, 5 passed each)",
   ".venv/bin/python -m pytest tests/unit -q -p no:cacheprovider -> 1043 passed",
   "git archive b5b9b34 | tar -x -C <scratchpad>/t075r2/base; baseline pytest there -> 5 passed",
   "scratch mutants (copies of base): m_sort: app/backend/flags.py:125 uniq.sort(key= -> (lambda **k: None)(key= ; pytest -> 1 failed, 4 passed, failing test test_model_flag_order_does_not_change_the_flag_list",
   "m_j3: app/backend/judges.py:59 judge_conflict_v2 -> judge_conflict_v1; pytest -> 1 failed, 4 passed, failing test test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names",
   "m_j4: app/backend/judges.py:64 judge_flag_v2 -> judge_flag_v1; pytest -> 1 failed, 4 passed, same failing test",
   "import check in each scratch copy: app.backend.flags resolves to the scratch copy's app/ directory",
   "grep -n 'sleep|except|float(|time|random' tests/unit/test_t075_determinism.py (only a monkeypatch lambda kwarg); git show b5b9b34 | grep '^+' for except/float(/sleep( -> none added",
   "grep -n 'fix|caus|stabil' evals/reports/determinism-diagnosis.md (line 3 status: cause unconfirmed, changes are mitigations; section 4 labelled inference)",
   "flags.py:292,295,300 read for the audit pv wiring; judges.py _run loads prompt by name (judges.py:24-27)"
 ],
 "verdict": "pass",
 "scores": {"sort_test_kills_sort_mutant": 5, "judge_prompt_test_kills_v1_revert": 5, "cause_wording_honest": 4, "test_reproducibility": 5, "full_unit_suite_green": 5},
 "findings": [
   {"severity": "nit", "title": "Card AC 2 text still frames the 1.0 as the fix's result",
    "evidence": "python3 tools/board.py show T-075: ac n=2 text 'Fix lands so LLM_BACKEND=claude-cli ENABLE_LIVE=1 evals.run --runs 3 gives determinism_3run 1.0 ...'; its evidence line now begins 'Corrected: pre-change baseline was already determinism 1.0 in 12/12 runs'",
    "why_it_matters": "The evidence is now honest. The AC text still reads as though the fix produces the 1.0, which is the reading the diagnosis doc was rewritten to rule out.",
    "fix": "Optional: when the orchestrator next edits the card, reword AC 2 to 'eval gives determinism 1.0 and unsupported 0 after the changes (non-discriminating, see diagnosis)'. The current evidence line is adequate.",
    "acceptance_test": "Card AC 2 text no longer says 'Fix lands so'; evidence line unchanged."},
   {"severity": "nit", "title": "Retry-pause test checks only that a sleep is callable, not the (0.5, 1.5) delays",
    "evidence": "tests/unit/test_t075_determinism.py:60-69: `assert seen[0] is None and callable(seen[1])`; app/llm/audited.py RETRY_DELAYS_S = (0.5, 1.5) (round-1 review cited audited.py:17)",
    "why_it_matters": "The test proves the live backend pauses and the fixture does not, but not the pause length. This was round-1 minor 7's optional item and is not part of the r2 changes.",
    "fix": "Assert that the live sleep for attempt 2 is the value in RETRY_DELAYS_S (for example, call the sleep with 0 and check the recorded duration) instead of only checking callable.",
    "acceptance_test": "Changing RETRY_DELAYS_S to (0, 0) or removing the pause fails the test."}
 ],
 "whats_right": [
   "The sort test has a control (asserts three model-only flags) and checks all six permutations with a duplicate; the removed-sort mutant fails it.",
   "The prompt test compares the text the judge sent with the version the audit record names, so a v1 revert in either judges.py call fails it.",
   "The card and determinism-diagnosis.md now state the 0.0 cause is unconfirmed and that the 1.0 cannot discriminate fixed from unfixed code."
 ],
 "questions_for_chris": []}
```
