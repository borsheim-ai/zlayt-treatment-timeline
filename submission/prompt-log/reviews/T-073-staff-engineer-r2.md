# T-073 r2 review: narrow the broad except in the judge path (staff-engineer-reviewer, round 2)

Reviewer: staff-engineer-reviewer, model claude-haiku-5-5. Commit under review: c8a9874 (the T-073 r2 fix, committed together with the T-084 r2 changes), with e2b4e3f underneath. HEAD moved during the review from bc12d44 to a850be0 (6feb2ff and a850be0, both "restore ... reverted by 2fca530"). The T-073 files are unchanged from c8a9874 through a850be0, so the verdict is for HEAD a850be0. `git worktree add` was refused by board-guard for reviewers, so HEAD was pinned with `git archive a850be0` into the session scratchpad instead (same tree, no worktree).

## Summary

Both r1 findings are closed at HEAD. `audited_call` now retries only `LLMError`, `TimeoutError`, `ConnectionError`, and a `validate` `ValueError` (audited.py:21-22). Any other exception writes one `llm_calls` row with the class name only and is re-raised (audited.py:90-91, 106-108). The guard records `ladder.judge.error_class` for `LLMFailed`, `LLMFailedFixtureMiss`, `FixtureMissing` and `LLMError` on the two seams that use it (judge_guard.py:17-23; review.py:102, reclassify.py:167). Four scratch mutants of this code are each caught (5 to 8 failing tests each). No blocker, no major. Verdict: pass, with one minor (error_class is recorded only on the two guarded seams) and one minor record problem (the deferred judges.py change points at the wrong card).

## Exercised (what I actually ran or read)

- `python3 tools/board.py show T-073` and `show T-094` (T-094 is "Live ship-bar flap ...", not the judges.py card the handoff names).
- `git log --oneline -8`; `git rev-parse HEAD` (bc12d44 at start, a850be0 at the end); `git show --stat c8a9874`; `git show --stat e2b4e3f`.
- `git diff --stat c8a9874 bc12d44 -- app/backend/judge_guard.py app/llm/audited.py app/backend/judges.py tests/unit/test_audited.py tests/unit/test_judge_guard.py`: empty. `git diff --stat bc12d44 a850be0 -- <same files>`: empty.
- `.venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py`: working tree 120 passed (the working tree has uncommitted edits, not reviewed); pinned a850be0 120 passed; pinned c8a9874 9 failed, 111 passed (all 9 in test_reclassify.py, see T-084 r2).
- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_audited.py` at a850be0: 19 passed.
- `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit` at a850be0: 7 failed, 1392 passed, 2 skipped. None of the 7 is in test_audited.py or test_judge_guard.py (names in reviews/T-084-staff-engineer-r2.md).
- Read in full at a850be0: app/llm/audited.py, app/backend/judge_guard.py, app/backend/judges.py:24-39, tests/unit/test_audited.py, tests/unit/test_judge_guard.py, app/llm/_types.py:7-11.
- `grep -rn "judge_guard.guarded" app/` (review.py:102, reclassify.py:167 only) and `grep -rn "run_j[0-9]_meta(" app/` (judge call sites).
- Scratch mutants T73-1 to T73-4 with `artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py`, log `artifacts/review-evidence/T-073-T-084-r2/mutation-run-r2.txt`. Control on the pinned archive: 139 passed (the four files plus test_audited.py).
- The brief's selector `-k "review or reclass"` still does not collect test_judge_guard.py; I named the files explicitly, as r1 asked.

## Findings

### F1 (minor): error_class is recorded only on the two guarded seams

- `grep -rn "judge_guard.guarded" app/` returns review.py:102 and reclassify.py:167 only. Other judge call sites call `judges.run_*_meta` directly: rejudge.py:30-40, flags.py:291-294, narrative.py:108, generator.py:150, and the pipeline batch at judges.py:108. judges.py:33-34 still turns `LLMFailed` into `("unavailable", None, "NONE")`, so on those paths the ladder records reason NONE and no class.
- Why it matters: the card's AC is scoped to review.py, so the AC is met. The same expected failure on rejudge, flags or narrative still leaves the audit unable to say why the judge did not run. This is the same gap as r1 F2, now on the other seams.
- Fix: return the class from `judges._run` with the verdict (for example `(verdict, call_id, reason, error_class)`), or route each direct call through `judge_guard.guarded`. judges.py is outside this card's stated scope, so it needs its own card (see F2).
- Acceptance test: a fixture backend raising `AU.LLMFailed` through `rejudge` (rejudge.py:30) records `ladder.judge.error_class == "LLMFailed"`.

### F2 (minor): the deferred judges.py change has no card

- The handoff says "judges._run still returns reason NONE for LLMFailed ... (judges.py untouched, T-094)". `python3 tools/board.py show T-094` returns "Live ship-bar flap: case_02 golden must_not hit and entry recall 0.965 on a live run". The deferral points at an unrelated card, so it is effectively unrecorded.
- Fix: the orchestrator opens a backend card for the judges._run change (`board.py new` with the F1 acceptance test as its AC) and corrects the handoff reference.

### F3 (nit): retry delays are fixed, not jittered

- audited.py:17 `RETRY_DELAYS_S = (0.5, 1.5)`. The cap (audited.py:15, `MAX_ATTEMPTS = 3`, so two retries) and the per-attempt logging are right. The dossier (persona §9) asks for jitter on retries. This is optional for the fixture backend, which never sleeps.
- Fix (optional): add a small jitter to the live-backend sleep. Acceptance: a test that patches the sleep hook and asserts each delay lies within the jittered bounds.

## What is right

- audited.py:21-22 and :88-108: retries are limited to provider, transport and validation errors. Any other exception writes one `llm_calls` row (class name only) and is re-raised. test_audited.py:109-136 covers it; mutant T73-1 (broad retry) fails 8 tests and mutant T73-2 (bug not re-raised) fails 8 tests.
- judge_guard.py:17-23 notes the expected error's class on the way through judges._run, so review.py:102 and reclassify.py:167 record `ladder.judge.error_class`. test_judge_guard.py:94-113 covers LLMFailed, LLMFailedFixtureMiss, FixtureMissing and LLMError. Mutant T73-3 (class not noted) fails 5 tests.
- judge_guard.py:8 covers `FixtureMissing` through its base class (_types.py:11 `class FixtureMissing(LLMError)`). Mutant T73-4 (guard catches every exception) fails 7 tests.

Outside this card, not attributed to it: the full unit run at a850be0 has 7 failures, and the sample CLI crashes at pipeline.py:501. Details are in reviews/T-084-staff-engineer-r2.md.

## Scores

```
no_silent_fallback 4 (expected errors become unavailable with a class; no positive verdict; judges._run still hides the class on other seams, F1)
error_class_recorded 4 (both guarded seams; other judge call sites still NONE, F1)
propagation_on_real_path 5 (one row, re-raised, not retried; mutants T73-1 and T73-2 caught)
tests_kill_mutants 5 (4 of 4 seam mutants caught on the pinned HEAD)
ac_evidence_matches_code 4 (AC holds for review.py; the deferral is not recorded on a card, F2)
```

## Questions for Chris

None for this card.

```json
{"card": "T-073", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c8a9874 (T-073 r2, committed with T-084 r2) and e2b4e3f underneath; HEAD at review end a850be0 (bc12d44 at start), pinned by git archive; files app/llm/audited.py, app/backend/judge_guard.py, app/backend/judges.py (read), tests/unit/test_audited.py, tests/unit/test_judge_guard.py, app/llm/_types.py (read); no app URL; unit-level card, no sample-case run",
 "exercised": ["python3 tools/board.py show T-073 and show T-094", "git log --oneline -8; git rev-parse HEAD (bc12d44 then a850be0); git show --stat c8a9874 and e2b4e3f", "git diff --stat c8a9874 bc12d44 and bc12d44 a850be0 over the T-073 files (both empty)", ".venv/bin/python -m pytest -q tests/unit/test_reclassify.py tests/unit/test_judge_guard.py tests/unit/test_review_rules.py tests/unit/test_billing.py: working tree 120 passed; pinned a850be0 120 passed; pinned c8a9874 9 failed 111 passed", ".venv/bin/python -m pytest -q tests/unit/test_audited.py at a850be0: 19 passed", ".venv/bin/python -m pytest -q tests/unit at a850be0: 7 failed 1392 passed 2 skipped (none in the T-073 files)", "read audited.py, judge_guard.py, judges.py:24-39, test_audited.py, test_judge_guard.py, _types.py:7-11 at a850be0", "grep -rn judge_guard.guarded app/ and grep -rn run_j[0-9]_meta( app/", "scratch mutants T73-1..T73-4 via artifacts/review-evidence/T-073-T-084-r2/mutate_r2.py (log mutation-run-r2.txt): T73-1 8 failed, T73-2 8 failed, T73-3 5 failed, T73-4 7 failed; control 139 passed"],
 "verdict": "pass",
 "scores": {"no_silent_fallback": 4, "error_class_recorded": 4, "propagation_on_real_path": 5, "tests_kill_mutants": 5, "ac_evidence_matches_code": 4},
 "findings": [
  {"severity": "minor", "title": "error_class is recorded only on the two guarded seams; other judge call sites still turn LLMFailed into reason NONE with no class",
   "evidence": "grep -rn 'judge_guard.guarded' app/ -> review.py:102 and reclassify.py:167 only; judges.py:33-34 'except AU.LLMFailed: return unavailable, None, NONE' unchanged; direct callers rejudge.py:30-40, flags.py:291-294, narrative.py:108, generator.py:150, judges.py:108",
   "why_it_matters": "The card AC is scoped to review.py and is met. The same expected failure on rejudge, flags, narrative or the pipeline still leaves the audit without the reason the judge did not run (the r1 F2 gap on other seams).",
   "fix": "Return the class from judges._run with the verdict, or route each direct call through judge_guard.guarded. judges.py is outside this card, so it needs its own backend card (see F2).",
   "acceptance_test": "A fixture backend raising AU.LLMFailed through rejudge.py:30 records ladder.judge.error_class == 'LLMFailed' on the item."},
  {"severity": "minor", "title": "The deferred judges.py change has no card: the handoff cites T-094, which is an unrelated live ship-bar card",
   "evidence": "T-073 handoff text 'judges._run still returns reason NONE for LLMFailed ... (judges.py untouched, T-094)'; python3 tools/board.py show T-094 -> title 'Live ship-bar flap: case_02 golden must_not hit and entry recall 0.965 on a live run'",
   "why_it_matters": "A deferral that points at the wrong card is effectively unrecorded; the next reader will chase the wrong work.",
   "fix": "Orchestrator opens a backend card for the judges._run class capture (board.py new, AC = the F1 acceptance test) and corrects the handoff reference.",
   "acceptance_test": "board.py show <new card> lists the judges._run change in its AC; the T-073 handoff names that card."},
  {"severity": "nit", "title": "Retry delays are fixed, not jittered",
   "evidence": "app/llm/audited.py:17 RETRY_DELAYS_S = (0.5, 1.5); cap at audited.py:15 MAX_ATTEMPTS = 3 is correct",
   "why_it_matters": "The persona's retry guidance (AWS, persona §9) asks for jitter on retries. The fixture backend never sleeps, so this does not affect tests.",
   "fix": "Optional: add a small jitter to the live-backend sleep.",
   "acceptance_test": "A test that patches the sleep hook and asserts each delay lies within the jittered bounds."}
 ],
 "whats_right": [
  "audited.py:21-22 and :88-108: retries only provider, transport and validation errors; any other exception writes one llm_calls row (class name only) and re-raises; mutants T73-1 and T73-2 each fail 8 tests.",
  "judge_guard.py:17-23 notes the expected error's class on the way through judges._run, so review.py:102 and reclassify.py:167 record ladder.judge.error_class; test_judge_guard.py:94-113 covers it; mutant T73-3 fails 5 tests.",
  "judge_guard.py:8 covers FixtureMissing through its base class (_types.py:11), and mutant T73-4 (guard catches everything) fails 7 tests."
 ],
 "questions_for_chris": []}
```
