# T-099 staff-engineer-reviewer: GET /api/calibration (commit 3ecb8b1)

Verdict: **changes** (0 blockers, 1 major, 3 minor). The route does what the card says: it serves the committed calibration in the contract shape, returns `calibration: null` for missing and invalid files, invents no numbers, and is read-only and safe in demo mode. The major is a test gap: the rule "state totals equal type totals" can be removed and every test stays green.

Pinning: I reviewed `git archive 3ecb8b1` (the card commit). The live HEAD during the review was f5ddec8; `git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json` printed nothing, so the reviewed files are unchanged at live HEAD.

Severity: the card's validation rules are the thing I check against D.2. A hand-edited statement or a wrong sub-count is not an invented number produced by the app (the route serves only what is in the file), so nothing rises to blocker. Those gaps are minors, with the reasons in each finding.

## Findings

**F1 (major). The "state totals equal type totals" rule is untested.** `app/backend/calibration_route.py:73` is the only check of `by_state` against `by_type`. Replacing it with `if False:` leaves `tests/unit/test_calibration_route.py` at 23 passed. The test that looks like it covers it (`sum_mismatch_hand_edit`, `tests/unit/test_calibration_route.py:106`) is rejected by the statement check, because it changes only the count. A consistent hand-edit (count and its sentence changed together) is served as `ok` on the mutant and rejected on the real code: `artifacts/review-evidence/T-099-staff-engineer-results.txt`, "consistent hand-edit" lines. The card lists this rule as validation; a regression would serve a wrong "matched N/M times" line with no failing test.

**F2 (minor). The route checks less than the producer.** `app/backend/calibration_route.py:37-41` (`_statement_ok`) only requires that the substring "N/M times" appear in a statement. `evals/run.py:1041` rebuilds all statements from the counts and requires equality, and `evals/run.py:1043-1045` compares prompt and lexicon hashes with disk. Probe `hand_edit_sentence_claim` rewrites the verified-overall sentence to end "so the letter is safe to send." and the route returns `ok`; the UI shows statements verbatim (`memory/contracts/api.md`, T-099 section). The hash comparison is absent from the route, so a measurement made on older prompts is served with no staleness signal. This is latent, not live: I checked three hashes (`app/llm/lexicon.yaml`, `app/llm/prompts/judge_faithfulness_v1.md`, `app/llm/prompts/extract_v1.md`) with `shasum -a 256` and they match the committed file.

**F3 (minor). Fields the route serves are not cross-checked.** `calibration_route.py:52-57` checks only the type of `backend`, `case_count` and `small_sample`; `:78` checks only that `by_case` is a dict. Probes, all `ok`: `case_count` 500 while the sentences say "10 golden cases" (`hand_edit_case_count`); `by_case` `[1, 9]` in a 55-item cell (`hand_edit_by_case_only`); `by_case` `[12, 9]` (`by_case_matched_gt_total`); `small_sample` false with 10 cases (`small_sample_flipped`, the threshold is `evals/run.py:244`, CAL_SMALL_N = 30); `backend` changed to `claude-sonnet-5-5` while the sentence names the fixture backend (`hand_edit_backend_label`). The counts the card cares about are checked; these labels and sub-counts are not.

**F4 (minor). The card's evidence does not reproduce.** The T-099 card AC 1 says `pytest -q tests/unit -k calibration gives 34 passed`. At 3ecb8b1 the command prints `32 passed, 2 skipped, 1570 deselected`, the skips are `tests/unit/test_eval_runner.py:636: no git repository here (exported tree)`, and `tests/unit/test_calibration_route.py` alone gives 23 passed. The feature is fine; the evidence line is wrong, and "done" rests on it.

## What I exercised

- `git show --stat 3ecb8b1`; `git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py` (read in full); `git archive 3ecb8b1` into the scratchpad.
- `.venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs` on the archive: 32 passed, 2 skipped. `tests/unit/test_calibration_route.py` alone: 23 passed.
- State probes on 22 scratch files (missing, not JSON, not UTF-8, list, wrong schema, state total, sentence, floats, bools, cell `matched > total`, not_scored, extra key, directory): `artifacts/review-evidence/T-099-staff-engineer-probe-states.py`. Results: `artifacts/review-evidence/T-099-staff-engineer-results.txt`.
- Consistent hand-edit probe: `artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py` (real code: invalid; mutant: ok).
- HTTP demo-mode probe on the real app: `artifacts/review-evidence/T-099-staff-engineer-probe-http.py`. GET `/api/calibration` returns 200, envelope keys `calibration, message, status`, status `ok`; POST, PUT, PATCH and DELETE return 405; `/api/health` reports `demo_mode: True`; the body contains none of `token`, `excerpt`, `Patient`, `summary`.
- Mutants on a scratch copy: `artifacts/review-evidence/T-099-staff-engineer-mutants.py` (M1 sentence check removed: 1 failed; M2 state-total check removed: 23 passed; M3 `problems()` ignored: 11 failed; M4 all methods accepted: 1 failed; restored: 23 passed).
- Read the committed `evals/reports/calibration.json` and checked its arithmetic: verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2; `source_commit` b85fc1b; `case_count` 10 and `small_sample` true agree with the sentences.
- Read `memory/contracts/api.md` (T-099 section), `evals/run.py:1029-1047` (`check_calibration`), `evals/run.py:6` (`--check-fresh`), and the cards via `python3 tools/board.py show T-099` and `show T-096`.
- Not exercised: the review screen (T-096 is not built); the Docker image (release lane).

```json
{"card": "T-099", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 3ecb8b1 (app/backend/api.py hook, app/backend/calibration_route.py, tests/unit/test_calibration_route.py) via git archive 3ecb8b1; live HEAD f5ddec8 checked: no change to the reviewed files; no app URL (FastAPI TestClient, real app, default demo mode); committed evals/reports/calibration.json (sample: 10 golden cases, fixture backend)",
 "exercised": [
  "git show --stat 3ecb8b1; git show 3ecb8b1 -- app/backend/api.py app/backend/calibration_route.py (full); git archive 3ecb8b1 into scratch t099-3ecb8b1",
  "git diff --stat 3ecb8b1 f5ddec8 -- app/backend/calibration_route.py tests/unit/test_calibration_route.py evals/reports/calibration.json -> empty",
  ".venv/bin/python -m pytest -p no:cacheprovider -q tests/unit -k calibration -rs -> 32 passed, 2 skipped (test_eval_runner.py:636); tests/unit/test_calibration_route.py -> 23 passed",
  "artifacts/review-evidence/T-099-staff-engineer-probe-states.py: 22 scratch files through calibration_route.load; statuses ok/missing/invalid as listed in artifacts/review-evidence/T-099-staff-engineer-results.txt",
  "artifacts/review-evidence/T-099-staff-engineer-probe-consistent-edit.py: state total and its sentence changed together -> invalid on 3ecb8b1; ok with calibration_route.py:73 disabled",
  "artifacts/review-evidence/T-099-staff-engineer-probe-http.py: GET /api/calibration -> 200 status ok, keys calibration/message/status; POST, PUT, PATCH, DELETE -> 405; /api/health demo_mode True; body has no token, excerpt, Patient or summary",
  "artifacts/review-evidence/T-099-staff-engineer-mutants.py on the scratch copy: M1 sentence m/t check removed -> 1 failed; M2 state-total check removed -> 23 passed; M3 problems() ignored -> 11 failed; M4 all methods accepted -> 1 failed; restored -> 23 passed",
  "read evals/reports/calibration.json (committed): arithmetic checked (verified 83/84 = 9+54+20 and 9+55+20; needs_review 10/10 = 6+2+2); shasum -a 256 of app/llm/lexicon.yaml, app/llm/prompts/judge_faithfulness_v1.md, app/llm/prompts/extract_v1.md matches the hashes in the file",
  "read memory/contracts/api.md T-099 section; evals/run.py 6, 244, 1029-1047; app/backend/calibration_route.py in full; tests/unit/test_calibration_route.py test names and INVALID_CASES (lines 56-177); python3 tools/board.py show T-099 and show T-096"],
 "verdict": "changes",
 "scores": {"contract_shape": 4, "never_invents_numbers": 3, "demo_safety": 5, "validation_strength": 2, "test_pins_behaviour": 2},
 "findings": [
  {"severity": "major", "title": "The 'state totals equal type totals' validation rule is untested: removing it keeps all 23 route tests green",
   "evidence": "app/backend/calibration_route.py:73 (if bs[s][k] != sum(bt[t][s][k] ...)). Mutant with the check replaced by 'if False:': .venv/bin/python -m pytest -q tests/unit/test_calibration_route.py -> 23 passed (artifacts/review-evidence/T-099-staff-engineer-mutants.py, M2). tests/unit/test_calibration_route.py:106 (sum_mismatch_hand_edit) is rejected by the statement check, not the sum check. Consistent hand-edit (by_state.verified 82/84 with its sentence rewritten): ok on the mutant, invalid on 3ecb8b1 (artifacts/review-evidence/T-099-staff-engineer-results.txt).",
   "why_it_matters": "The card lists this rule as a validation step. It is the only check that stops a headline total being edited together with its sentence. No test fails when it is removed, so a regression would serve a wrong 'matched N/M times' line with no failing test. Rated major (tests fail when the code breaks).",
   "fix": "Add an INVALID_CASES entry whose sentences are rebuilt to match the changed state total, so only the sum check can reject it, and assert the problem names by_state.verified.matched.",
   "acceptance_test": "New case returns status invalid; with calibration_route.py:73 disabled the new test fails."},
  {"severity": "minor", "title": "The route validates less than the producer's own check (sentences are not rebuilt; hashes are not compared)",
   "evidence": "app/backend/calibration_route.py:37-41 (_statement_ok: only the substring 'N/M times' is required), :85-90 (statement checks). evals/run.py:1041 rebuilds the statements from the counts and requires equality; evals/run.py:1043-1045 compares prompt and lexicon hashes with disk. Probe hand_edit_sentence_claim (artifacts/review-evidence/T-099-staff-engineer-results.txt): verified-overall sentence changed to end 'so the letter is safe to send.' -> status ok.",
   "why_it_matters": "The UI shows the statements verbatim (memory/contracts/api.md T-099 section), so a hand-edited statement that keeps the numbers is shown as measured. The same file fails check_calibration, so the server accepts what the producer rejects. A calibration measured on older prompts is also served with no staleness signal. Latent, not live: the three hashes I checked match the files on disk.",
   "fix": "Move calibration_sentences into a module both evals/run.py and calibration_route.py import; require exact equality with the file's sentences. Add the hash comparison (or a freshness field in SERVED) so a stale file is flagged.",
   "acceptance_test": "A calibration whose sentence adds a claim is invalid; a file whose prompt hash differs from disk is invalid or served with a stale flag."},
  {"severity": "minor", "title": "by_case, case_count, small_sample and backend are served without cross-checks",
   "evidence": "app/backend/calibration_route.py:52-57 (backend, case_count, small_sample: type checks only), :78 (by_case: dict check only). Probes, all status ok (artifacts/review-evidence/T-099-staff-engineer-results.txt): hand_edit_case_count (case_count 500, sentences still say '10 golden cases'); hand_edit_by_case_only (by_case [1, 9] in a 55-item cell); by_case_matched_gt_total ([12, 9]); small_sample_flipped (false with 10 cases; threshold evals/run.py:244 CAL_SMALL_N = 30); hand_edit_backend_label (backend 'claude-sonnet-5-5' while the sentence says fixture backend).",
   "why_it_matters": "The served envelope carries numbers and labels that the statements and the sample size contradict, and the UI can show them. The card's 'never invented numbers' holds for the headline counts, but these fields are not checked against each other or against the sentences.",
   "fix": "Check that by_case sums equal each cell total and that matched <= total per case; require case_count == len(cases); require small_sample == (case_count < 30); require backend to match the backend named in the sentences.",
   "acceptance_test": "Each probe above returns status invalid."},
  {"severity": "minor", "title": "The card's test evidence does not reproduce",
   "evidence": "T-099 card AC 1 evidence (python3 tools/board.py show T-099): 'pytest -q tests/unit -k calibration gives 34 passed'. At 3ecb8b1: '32 passed, 2 skipped, 1570 deselected' (artifacts/review-evidence/T-099-staff-engineer-results.txt); 'SKIPPED [2] tests/unit/test_eval_runner.py:636: no git repository here (exported tree)'. tests/unit/test_calibration_route.py alone: 23 passed.",
   "why_it_matters": "The 'done' evidence is what the orchestrator checks. The numbers do not match what the command prints, and the two skipped tests are from another file. The feature is unaffected.",
   "fix": "Correct the card's evidence line to the printed counts, or select the route file explicitly (tests/unit/test_calibration_route.py).",
   "acceptance_test": "The cited command prints the cited numbers."}
 ],
 "whats_right": [
  "Envelope and empty states are right: GET returns 200 with {status, calibration, message}; missing and invalid files give calibration null with a constant message; no default numbers appear in any state (state probes, HTTP probe).",
  "Invalid files never echo their contents: an extra key with record-like text is not served, and the logs name only the rule (state probes 'extra_key'; server log lines in the results file).",
  "Read-only and demo-safe: POST, PUT, PATCH and DELETE return 405, no case token or record text is served, and the route is not gated by demo mode (HTTP probe; test_route_is_read_only)."],
 "questions_for_chris": [
  "Should the route refuse a calibration whose prompt or lexicon hashes differ from disk, as evals/run.py check_calibration does, or serve it with a stale flag for the review screen to show?"]}
```
