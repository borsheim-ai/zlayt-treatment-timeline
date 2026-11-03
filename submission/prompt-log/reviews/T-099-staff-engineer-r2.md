# T-099 staff-engineer-reviewer, round 2: GET /api/calibration (commit f345bc8)

Verdict: **pass** (0 blockers, 0 majors, 3 minors). The r1 major is closed: the "state totals equal type totals" rule now has its own test, and that test is the only one that goes red when the rule is removed. Four of the five r1 minors are fixed with tests. Three items remain open and are minors: the deferred F2, one new test gap in the `case_count` rule, and the card's AC 1 evidence line, which still does not reproduce at the pinned commit.

Model field: claude-haiku-5-5, the model I am running as (per the brief). The persona file's "expected" id differs; I used the actual one.

Pinning: reviewed `git archive f345bc8` into a scratch copy. Live HEAD moved to 4c5f9bf (T-101, qa: `evals.run` no longer overwrites calibration.json). `git diff --stat f345bc8 HEAD -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json app/backend/api.py` printed nothing, so every reviewed file is unchanged at live HEAD.

## r1 items

- **F1 (major): closed.** Mutant M_state_total_off (check at `calibration_route.py:85` replaced by `if False and ...`), scratch copy of f345bc8: `1 failed, 29 passed`, and the failing test is `test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total`. Control with the pre-r2 test file from 3ecb8b1: `C_state_total_off_r1_tests: 23 passed`, so the gap is gone only because of the new test.
- **F2 (minor): deferred by the author, still open.** See finding 1 and my answer on debt below.
- **F3 (minor): mostly closed.** by_case sum (`M_by_case_sum_off`: 1 failed), by_case bound (`M_by_case_le_off`: 1 failed), by_case call (`M_by_case_call_off`: 2 failed), small_sample (`M_small_sample_off`: 1 failed), backend in statements (`M_backend_stmt_off`: 1 failed), case count in statements (`M_case_stmt_off`: 1 failed). The small_sample rule matches the producer (`evals/run.py:338`, `:350`, `CAL_SMALL_N = 30` at `:244`). The `case_count == len(cases)` clause is fixed in code but not tested in isolation: finding 2.
- **F4 (minor): still does not reproduce.** Finding 3.

## Findings still open

1. **F2 (minor, deferred).** The route still requires only the substrings "on the N backend" and "N/M times" (`calibration_route.py:46-53`), and it never compares hashes. Probe B (verified-overall sentence with ' The letter is safe to send.' appended) returns `ok`. Probe C (a `hashes` entry that differs from disk) returns `ok`. The producer rejects both (`evals/run.py:1041` requires exact sentences; `:1045` compares hashes). `memory/SCOPE_CUTS.md` has no row for this; `grep -n -i calibration memory/SCOPE_CUTS.md` finds only the T-090 debt row. The only record is the T-099 handoff.

   **My answer on debt.** I accept the exact-sentence half as debt, but only once it is a SCOPE_CUTS row with an owner (the move of `calibration_sentences` is qa's file). Blast radius is low: the file is committed from a clean HEAD, and a hand edit that adds a claim is a visible repo diff. I do not accept the staleness half as open debt past the M3 gate. It is the one path where the served accuracy line can be false with no signal, and the producer already has the check. Fix that half before the gate.

2. **`case_count == len(cases)` is not isolated by any test (minor, new at r2).** Mutant M_case_count_off (clause at `calibration_route.py:97` replaced by `and True`): `30 passed`. The test that names the rule, `INVALID_CASES['case_count_not_the_case_list']` (`tests/unit/test_calibration_route.py:115`), is rejected by the statement clause instead, because the sentences still say "10 golden cases". Probe A (case_count 500, both sentences rewritten to "500 golden cases", consistent edit): pinned f345bc8 returns `invalid | ['case_count is not the number of cases']`; M_case_count_off returns `ok`. The handoff says "Each minor check disabled -> its test fails"; that is not true for this clause. I considered rating this major (same class as F1), and did not: the rule is enforced, the number is a sample label, and the other three r1 minors are fixed. The fix is one case whose sentences are rebuilt, so only the length check can reject it.

3. **Card AC 1 evidence still does not reproduce (minor, residual of r1 F4).** The card says `pytest -q tests/unit -k calibration: 39 passed, 2 failed in tests/unit/test_eval_runner.py` and blames an uncommitted worktree calibration.json (claude-cli). At f345bc8 the exported tree prints `39 passed, 2 skipped, 1807 deselected` (`SKIPPED [2] tests/unit/test_eval_runner.py:636`). A git checkout of f345bc8 with the worktree calibration.json copied in prints `41 passed, 1807 deselected`. The worktree file now has the same sha as the committed one (`49d383b58340ca18`), so the dirty state the card cites is gone. I could not reproduce the 2 failures in any tree.

## What I exercised

- Read `personas/staff-engineer.md` in full, `reviews/T-099-staff-engineer.md` (r1), and my T-098/T-099 memory file.
- `git rev-parse --short HEAD` gave f345bc8 at start and 4c5f9bf at the end; `git log --oneline f345bc8..HEAD` shows only the T-101 commit.
- `git show --stat f345bc8` and `git show f345bc8 -- app/backend/calibration_route.py` (full diff read).
- `git archive f345bc8 | tar -x` into a scratch copy. `git show f345bc8:app/backend/calibration_route.py | shasum -a 256` and the test file hash both match the archive (`cab48fdc...`, `c8617169...`).
- `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs` in the archive: `39 passed, 2 skipped, 1807 deselected`. `tests/unit/test_calibration_route.py` alone: `30 passed`. Repeated once more: same result (determinism).
- Git clone of the repo, checkout f345bc8, worktree calibration.json copied in, same `-k calibration` command: `41 passed, 1807 deselected`.
- `python3 -I artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py <archive> <venv python> <repo>`: output in `artifacts/review-evidence/T-099-staff-engineer-r2-results.txt` (mutants M_state_total_off, M_case_count_off, M_small_sample_off, M_by_case_sum_off, M_by_case_le_off, M_by_case_call_off, M_backend_stmt_off, M_case_stmt_off, two controls; probes A to D). All mutants ran on scratch copies, never the product tree.
- `grep -n "except\|float(\|sleep\|retry"` on the route and its test at f345bc8: only `except` clauses at lines 122, 124, 129; no float, sleep, retry or network. `load()` at lines 116-135 read.
- Producer validator read at f345bc8: `evals/run.py:244`, `:338`, `:350`, `:1029-1046`.
- `python3 tools/board.py show T-099`, `python3 tools/board.py list`, `python3 tools/board.py validate` (output: `ok (101 file(s))`).

Not exercised: the review screen (T-096 is not built), and the HTTP demo-mode probe again (the r1 probe covered it and this round did not touch the hook in `api.py`; `test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode` passes).

```json
{"card": "T-099", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit f345bc8 (app/backend/calibration_route.py, tests/unit/test_calibration_route.py) via git archive f345bc8 into a scratch copy; live HEAD 4c5f9bf (T-101) checked: no change to the reviewed files; no app URL (FastAPI TestClient, default demo mode); committed evals/reports/calibration.json (sample: 10 golden cases, fixture backend)",
 "exercised": [
  "git rev-parse --short HEAD (f345bc8, later 4c5f9bf); git log --oneline f345bc8..HEAD (T-101 only); git diff --stat f345bc8 HEAD over the reviewed files (empty)",
  "git show --stat f345bc8; git show f345bc8 -- app/backend/calibration_route.py (full); shasum -a 256 of the archive files matches git show f345bc8",
  "git archive f345bc8 | tar -x into scratch t099-f345bc8-r2; .venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs -> 39 passed, 2 skipped (test_eval_runner.py:636); tests/unit/test_calibration_route.py -> 30 passed; repeated -> identical",
  "git clone + checkout f345bc8 + worktree calibration.json copied in; -k calibration -> 41 passed, 1807 deselected",
  "artifacts/review-evidence/T-099-staff-engineer-r2-mutants.py (run with python3 -I) -> artifacts/review-evidence/T-099-staff-engineer-r2-results.txt: M_state_total_off 1 failed (new test); M_case_count_off 30 passed; M_small_sample_off 1 failed; M_by_case_sum_off 1 failed; M_by_case_le_off 1 failed; M_by_case_call_off 2 failed; M_backend_stmt_off 1 failed; M_case_stmt_off 1 failed; control pre-r2 tests + state mutant 23 passed; probes A to D",
  "grep -n except/float(/sleep/retry in the route and its tests at f345bc8 (only except lines 122, 124, 129); read calibration_route.py load() lines 116-135",
  "evals/run.py at f345bc8: lines 244, 338, 350, 1029-1046 (check_calibration) read; grep -n -i calibration memory/SCOPE_CUTS.md",
  "python3 tools/board.py show T-099; python3 tools/board.py list; python3 tools/board.py validate -> ok (101 file(s))"],
 "verdict": "pass",
 "scores": {"contract_shape": 4, "never_invents_numbers": 4, "demo_safety": 5, "validation_strength": 4, "test_pins_behaviour": 4},
 "findings": [
  {"severity": "minor", "title": "F2 still open and deferred with no scope-cut row: route checks sentences by substring only and never compares prompt/lexicon hashes",
   "evidence": "app/backend/calibration_route.py:46-53 (_statement_ok: substring checks only). Probe B (verified-overall sentence plus ' The letter is safe to send.') -> ok; probe C (hashes entry differing from disk) -> ok; artifacts/review-evidence/T-099-staff-engineer-r2-results.txt. Producer: evals/run.py:1041 (sentences must equal calibration_sentences) and :1045 (hash compare). memory/SCOPE_CUTS.md has no calibration row; the only record is the T-099 handoff.",
   "why_it_matters": "The served accuracy line can carry a hand-added claim, and a measurement taken against other prompts is served with no signal. The server accepts what the producer rejects. Latent today: the hashes match disk. Accepting the exact-sentence half as debt is reasonable once it is a SCOPE_CUTS row with an owner; the staleness half should not stay open past the M3 gate because it is the only path where the served accuracy can be false without a signal.",
   "fix": "Record the exact-sentence half in memory/SCOPE_CUTS.md with an owner. Before the M3 gate, compare the hashes in the route (same hashes() as evals/run.py) and return the INVALID envelope on mismatch; a stale flag only if T-096 renders it.",
   "acceptance_test": "A calibration whose verified-overall sentence has an added claim returns status invalid; a file whose hashes entry differs from disk returns status invalid; both are in INVALID_CASES."},
  {"severity": "minor", "title": "The case_count == len(cases) rule has no isolating test; the handoff claim that every minor's test fails is wrong for this rule",
   "evidence": "app/backend/calibration_route.py:97 (len(cases) == c['case_count']). Mutant M_case_count_off with that clause replaced by 'and True': tests/unit/test_calibration_route.py -> 30 passed (artifacts/review-evidence/T-099-staff-engineer-r2-results.txt). The test that names it, INVALID_CASES 'case_count_not_the_case_list' (tests/unit/test_calibration_route.py:115), is rejected by the statement clause, not this one. Probe A (case_count 500 and both sentences rewritten to '500 golden cases'): pinned f345bc8 -> invalid ['case_count is not the number of cases']; M_case_count_off -> ok. Card handoff: 'Each minor check disabled -> its test fails.'",
   "why_it_matters": "This is the r1 F1 pattern: a rule that another clause catches in the test is untested. A consistent hand edit of the sample size is served, and the small-sample caveat is computed from the same number. Rated minor, not major: it is a label and a sample count in a committed file, and the other r1 minors are fixed and tested. Reviewer considered major and did not.",
   "fix": "Add an INVALID_CASES case that sets case_count to 500 and rewrites both sentences to '500 golden cases', so only the length check can reject it; assert the problem 'case_count is not the number of cases'. Correct the handoff claim.",
   "acceptance_test": "With the len(cases) clause disabled the new case fails; enabled, the route returns status invalid."},
  {"severity": "minor", "title": "Card AC 1 evidence still does not reproduce at f345bc8; the dirty state it blames no longer exists",
   "evidence": "Card T-099 AC 1 (python3 tools/board.py show T-099): 'pytest -q tests/unit -k calibration: 39 passed, 2 failed in tests/unit/test_eval_runner.py ... the uncommitted worktree evals/reports/calibration.json is claude-cli'. At f345bc8 (git archive): '39 passed, 2 skipped, 1807 deselected', SKIPPED [2] tests/unit/test_eval_runner.py:636. Git checkout of f345bc8 with the worktree calibration.json copied in: '41 passed, 1807 deselected'. Worktree evals/reports/calibration.json sha 49d383b58340ca18 equals the committed file.",
   "why_it_matters": "'Done' evidence is what the orchestrator checks. The counts on the card are not the counts the cited command prints at the pinned commit, and the cause it names is gone. The feature itself is unaffected.",
   "fix": "Replace AC 1 evidence with the counts printed at f345bc8: route file 30 passed; -k calibration 39 passed, 2 skipped in an exported tree, 41 passed in a git checkout. Drop the claude-cli note.",
   "acceptance_test": "The cited command, run at the cited commit, prints the cited counts."}
 ],
 "whats_right": [
  "F1 closed: the state-total rule has its own test; with the check disabled that test is the only one that fails (1 failed), and the pre-r2 test file passes 23 with the mutant, so the gap is closed by the new test alone.",
  "Four of five r1 minors are fixed, and each new check's test goes red when the check is removed: by_case sum, by_case bound, by_case call, small_sample (rule matches evals/run.py:338, :350), statements naming backend and case count.",
  "load() keeps explicit statuses on every error path (calibration_route.py:116-135), logs rule names not file contents, and no new network, sleep, float or retry appears in the route or its tests."],
 "questions_for_chris": [
  "F2 product call: when a calibration fails the exact-sentence or hash check, should the route refuse (invalid envelope with the existing message; my recommendation, since no T-096 screen code exists to render a stale flag) or serve it with a stale flag?"]}
```
