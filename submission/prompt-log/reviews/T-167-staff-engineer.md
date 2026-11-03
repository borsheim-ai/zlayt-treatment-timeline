# T-167 review (staff-engineer-reviewer): plain wording, no codes or test jargon in paralegal text or notes

Commit under review: `da6afb2` (HEAD = da6afb2, parent f7a8f2a). Checked on a `git archive da6afb2` copy.

## Summary

The backend change does what it claims for what it owns. Across the sample and 15 library cases, the letter and the internal notes export contain no reason codes and no test wording. The demo edit message says the AI second check is not available in this demo and tells the paralegal to compare and accept. Reason codes stay in the API fields (`reasons`, `warnings[].code`). The four older tests were updated to the new sentences without weakening them, and four local mutants each turn the new test file red.

Two things block a clean pass:

1. The unit suite is red at this commit: `tests/unit/test_e2e_contract.py::test_every_test_id_is_declared` fails. The cause is the sibling commit f7a8f2a (T-149 r3), not this diff. The card's "5266 passed" evidence does not reproduce.
2. AC1 says "grep of every user-facing string ... finds none", and the card is marked done. That is false for strings the backend serves (`GET /api/calibration`, evals-authored sentences with "recorded replies" and "golden cases"). The handoff lists them as "not mine", so AC1 cannot be closed as written.

Verdict rule applied: no blocker, two majors, so `changes`.

## Findings

### F1 (major): unit suite is red at da6afb2, so the card's AC1 evidence does not reproduce

- Command: `cd <archive da6afb2> && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider`
- Output tail: `1 failed, 5276 passed, 8 skipped`. The failure: `FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared` with `AssertionError: ['cases-keys', 'do-first-item', 'btn-new-case']`.
- Rerun alone: `pytest tests/unit/test_e2e_contract.py -q` gives `1 failed, 2 passed`.
- The ids are used in `app/frontend/overview.js:147,149,353,356` and `tests/e2e/test_multicase.py:563,581,609`. They are not declared in the contract docstring of `tests/e2e/conftest.py`. `git log` shows f7a8f2a added them; T-167's diff does not touch these files.
- Why it matters: the brief requires the unit suite to pass, and AC1 cites a green run. A red suite at the reviewed HEAD means the card's evidence is stale or wrong.
- Fix: the owning card adds the three ids to the conftest contract (or renames them to declared ids), then the suite is re-run at the commit that closes T-167. Not a T-167 code defect, but T-167 cannot close on evidence that does not reproduce.
- Acceptance test: `.venv/bin/python -I -m pytest tests/unit -q` exits 0 at the closing commit, and AC1 cites that run.

### F2 (major): AC1 "every user-facing string finds none" is false for backend-served calibration text

- Evidence: `artifacts/review-evidence/T-167-r1/sweep_local_hits.json` and `sweep_demo_hits.json`. Same result in demo mode (sample only) and local mode. Verbatim from `GET /api/calibration`, path `calibration/sentences/overall/verified`:
  `Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).`
  Eight such sentences (amount, entry, flag, overall; needs_review and verified) carry "fixture", "recorded replies" and "golden".
- Producer: `evals/run.py:314` builds `parts = (["recorded replies"] if backend == "fixture" else []) + [f"{case_count} golden cases"]`. Its docstring says these are "the statements the UI renders verbatim". The backend serves them: `app/backend/calibration_route.py:31` lists `"sentences"` in `SERVED`, and `calibration_route.py:87-115` rebuilds and checks them, so a builder fix must also update that check.
- The same surfaces still carry test wording at da6afb2 (T-166 and qa own them; I do not count them against T-167's diff, but AC1 as written covers them): `app/frontend/app.js:11` `"cached demo (recorded responses)"` / `"cached demo (curated responses)"`; `app/frontend/api.js:10` `"Request failed"`.
- Why it matters: the audit's F7 is a P0. The card claims the whole surface is clean, and the handoff says the strings are "not mine". The card cannot be closed on AC1 as written.
- Fix: either (a) narrow AC1 to backend-authored strings and log the rest as a SCOPE_CUT with cards (qa for the `evals/run.py:314` caveat builder and its rebuild check; T-166 for the chip and `api.js`), or (b) bring the builder into scope. Do not mark AC1 "done" with the universal claim.
- Acceptance test: rendered overview and case text, `GET /api/calibration`, and both exports contain none of: `fixture`, `golden`, `recorded replies`, `curated`, `Request failed`, `server answered`.

### F3 (minor): a prose field embeds a reason code in parentheses

- Evidence: `app/backend/trace.py:959` `"judge_says": f"{says} ({r['reason_code']})"`. Live API output for `case_lib04_dog_bite_scar_revision`, `GET /api/cases/{tok}/judges`, path `judges/disagreements/0/judge_says`: `charge (SHOULD_BE_CHARGE)`. There are 28 such strings in the library sweep (also SHOULD_BE_DAMAGES, SHOULD_BE_ESTIMATE).
- The UI hides it only by the regex at `app/frontend/judges.js:58` (`noCode`), which strips a trailing "(CODE)". Any other consumer prints the code.
- Why it matters: the card's rule is codes in API machine fields only. Here a human-readable field carries the code, and the frontend has to repair it.
- Fix: add a `reason_code` key carrying the code, and set `judge_says` to the plain sentence only.
- Acceptance test: for every item in the library sweep, no SHOUTING code appears in any string value except under the keys `reasons`, `reason_code`, `code`, `state_reason`, `error_class`.

### F4 (minor): `_removed_why` fallback doubles a phrase in the notes

- Evidence: `app/backend/export.py:697-700` and `:719`. Probe, run on the archive:
  `export._removed_why({'message':'JUDGE_UNSUPPORTED: x'})` returns `'it failed a check'`, and `_draft_paragraph` on a removed sentence with a code-bearing message prints `- AI wording removed (failed a check: it failed a check) (e9).`
- Latent: no current `narrative.REASONS` message contains a code (the new test asserts this). The `Removed:` branch at `export.py:723` also drops the final period when the fallback fires.
- Fix: give each branch its own fallback phrase ("AI wording removed (failed a check)" in the first branch, a full sentence with a period in the second).
- Acceptance test: a unit test with a code-bearing message asserts the output contains neither `failed a check: it failed a check` nor a SHOUTING token, and that the Removed line ends with ".".

### F5 (minor): the FIXTURE_MISS sentence is replay wording with no next step

- Evidence: `app/backend/why.py:17` `"The demo has no recorded AI answer for this step, so this item has not been checked."` Shown as the `why` of the tray item in `case_lib01_er_only_then_gap` (`artifacts/review-evidence/T-167-r1/sweep_local_distinct_strings.tsv`, key `why`).
- AC1's banned list does not name "recorded AI answer", so the literal AC passes. But "recorded answer" describes the fixture replay mechanism, and the sentence gives no instruction, unlike the demo second-check sentence.
- Fix: reuse the demo second-check wording (`JUDGE_DEMO`) for FIXTURE_MISS items.
- Acceptance test: `why.why("FIXTURE_MISS")` contains "not available in this demo" and "compare", and does not contain "recorded".

## Scores

| criterion | score (1-5) | note |
|---|---|---|
| plain_wording_backend_sentences | 4 | every why/reason/notes sentence clean; F5 is a minor replay phrase |
| plain_wording_all_served_strings | 2 | F2: calibration sentences and T-166 strings still carry test wording |
| codes_kept_in_api_fields | 4 | codes present where designed; F3 puts one in a prose field |
| demo_edit_message | 5 | plain, says not available in this demo, says what to do |
| notes_export_plain | 4 | 0 hits in letter or notes; F4 latent doubled phrase |
| unit_suite_green_at_head | 2 | F1: one red test from f7a8f2a |
| test_sensitivity | 5 | 4 mutants each red |
| golden_unchanged | 5 | no diff under evals/; check_golden exit 0 |
| determinism_cli | 5 | sample CLI twice, identical stdout |

## Exercised

- Read `personas/staff-engineer.md`; `python3 tools/board.py show T-167` and `show T-166`; `reviews/MVP-ux-audit.md` F4 and F7; `git show da6afb2` (10 files, backend diff read in full); `git rev-parse` confirmed HEAD = da6afb2.
- Extracted `git archive da6afb2` into a scratch copy (outside the repo). Read `tests/unit/test_t167_plain_wording.py` in full.
- Unit suite: `.venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider` on the archive: `1 failed, 5276 passed, 8 skipped` (F1). Single-file rerun of `tests/unit/test_e2e_contract.py`: `1 failed, 2 passed`.
- Sweep script `artifacts/review-evidence/T-167-r1/t167_sweep.py`:
  - Demo mode (public, sample only; the 15 library creates returned `409 demo_mode_unsupported_input`): 2,978 strings scanned, 0 hits in letter or notes.
  - Local mode (`T167_MODE=local`, sample plus 15 library cases): 42,142 strings scanned, 0 hits in `letter_text` or `internal_notes_text` across 16 cases. Hits are in machine fields plus F2, F3, F5 above. Output: `sweep_local_hits.json`, `sweep_local_distinct_strings.tsv`, `sweep_demo_hits.json`.
  - Reading the notes: `sample_internal_notes.txt` (edited item reads "(accepted by the paralegal after comparing it with the quote; second check not available)") and `case_lib02_internal_notes.txt`.
- Codes in API fields: the sweep shows `accept_resp/item/reasons/0 = JUDGE_UNAVAILABLE` and `edit_resp/warnings/0/code = JUDGE_UNAVAILABLE`, and the edit warning text is the demo sentence.
- Mutants (`artifacts/review-evidence/T-167-r1/mutate.py`, applied to a scratch copy, not committed): M1 restore `JUDGE_NOT_RUN:` prefix gives `4 failed, 215 passed`; M2 restore code in notes phrase gives `2 failed`; M3 drop "in this demo" gives `2 failed`; M4 restore "fixture backend ... recorded replies" in FIXTURE_MISS gives `6 failed`. All killed.
- `evals/golden/check_golden.py` (archive): exit 0, `golden OK: 10 cases (9 synthetic), 57 must_nots with tested examples ...`. `git diff --stat da6afb2^ da6afb2 -- evals/ tests/unit/_golden.py`: empty, so the sample golden is unchanged.
- CLI: `python -I -c "... runpy.run_module('app.pipeline', run_name='__main__')" evals/golden/sample.txt` twice on the archive: exit 0 both, stdout identical (45 lines). Saved as `cli_sample_run1.txt` and `cli_sample_run2.txt`. The status line `backend: fixture` is a developer CLI and is out of scope for paralegal text.
- Probes: `export._removed_why` and `_draft_paragraph` (F4); `git grep` at da6afb2 for `Request failed`, `cached demo`, `curated responses` (F2); `evals/run.py:314`; `trace.py:959`; `judges.js:58`.

Outside my lens: the phrasing "code check" and "phrase list" in notes and sentences, and the wording "compare the summary with the quote" versus "compare your wording". These are copy choices, and I did not judge them beyond "plain and actionable".

## whats_right

- Letter and internal notes are clean for sample and all 15 library cases (0 hits), and the demo edit message says what is not available and what to do.
- The new test file is sensitive: four local mutants, each turns it red, and the four older tests were updated to new behaviour assertions rather than loosened.
- Codes remain in API fields (`reasons`, `warnings[].code`), so the UI and support can still see the cause.

```json
{"card": "T-167", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit da6afb2 (HEAD = da6afb2; parent f7a8f2a), backend files in the diff plus tests/unit/test_t167_plain_wording.py; checked on git archive da6afb2 copy; no live app URL (FastAPI TestClient sweep); sample case plus 15 library cases (library only in ZLAYT_MODE=local)",
 "exercised": [
   "read personas/staff-engineer.md; board.py show T-167 and T-166; reviews/MVP-ux-audit.md F4 and F7; git show da6afb2 (backend diff, 10 files); git rev-parse HEAD",
   "git archive da6afb2 into a scratch copy; .venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider: 1 failed, 5276 passed, 8 skipped",
   "pytest tests/unit/test_e2e_contract.py -q: 1 failed, 2 passed (rerun)",
   "read tests/unit/test_t167_plain_wording.py in full and the four updated older tests",
   "artifacts/review-evidence/T-167-r1/t167_sweep.py demo mode (sample; 15 library creates refused with 409 demo_mode_unsupported_input): 2978 strings scanned, 0 hits in letter or notes",
   "t167_sweep.py local mode (T167_MODE=local, sample plus 15 library cases): 42142 strings scanned, 0 hits in letter_text or internal_notes_text across 16 cases; hits in artifacts/review-evidence/T-167-r1/sweep_local_hits.json and sweep_local_distinct_strings.tsv",
   "read sample_internal_notes.txt and case_lib02_internal_notes.txt; codes in API fields confirmed (accept_resp/item/reasons/0 JUDGE_UNAVAILABLE; edit_resp/warnings/0/code JUDGE_UNAVAILABLE)",
   "mutants mutate.py M1-M4 on a scratch copy: 4, 2, 2, 6 failures in test_t167_plain_wording.py (all killed)",
   "evals/golden/check_golden.py on archive: exit 0; git diff --stat da6afb2^ da6afb2 -- evals/ tests/unit/_golden.py: empty",
   "app.pipeline evals/golden/sample.txt run twice on archive: exit 0 both, stdout identical (artifacts/review-evidence/T-167-r1/cli_sample_run1.txt, cli_sample_run2.txt)",
   "probe export._removed_why and _draft_paragraph with a code-bearing message; git grep at da6afb2 for Request failed, cached demo, curated responses; evals/run.py:314; trace.py:959; judges.js:58"
 ],
 "verdict": "changes",
 "scores": {"plain_wording_backend_sentences": 4, "plain_wording_all_served_strings": 2, "codes_kept_in_api_fields": 4, "demo_edit_message": 5, "notes_export_plain": 4, "unit_suite_green_at_head": 2, "test_sensitivity": 5, "golden_unchanged": 5, "determinism_cli": 5},
 "findings": [
   {"severity": "major", "title": "Unit suite is red at da6afb2; the card's AC1 evidence (5266 passed) does not reproduce",
    "evidence": "pytest tests/unit -q on git archive da6afb2: '1 failed, 5276 passed, 8 skipped'; FAILED tests/unit/test_e2e_contract.py::test_every_test_id_is_declared: AssertionError ['cases-keys', 'do-first-item', 'btn-new-case']; ids used at app/frontend/overview.js:147,149,353,356 and tests/e2e/test_multicase.py:563,581,609, not declared in tests/e2e/conftest.py; added by f7a8f2a, not by da6afb2",
    "why_it_matters": "The brief requires the unit suite to pass and AC1 cites a green run; a red suite at the reviewed HEAD means the evidence is stale or wrong.",
    "fix": "The owning card (qa for tests/**, or frontend) adds the three ids to the conftest contract docstring or renames them to declared ids; re-run at the closing commit.",
    "acceptance_test": ".venv/bin/python -I -m pytest tests/unit -q exits 0 at the closing commit; AC1 cites that run"},
   {"severity": "major", "title": "AC1 'grep of every user-facing string finds none' is false: backend-served calibration sentences still carry test wording",
    "evidence": "artifacts/review-evidence/T-167-r1/sweep_local_hits.json and sweep_demo_hits.json; GET /api/calibration path calibration/sentences/overall/verified: 'Verified items matched the record 84/85 times in testing on the fixture backend (recorded replies, 10 golden cases, small sample).'; producer evals/run.py:314 parts = ([\"recorded replies\"] if backend == \"fixture\" else []) + [f\"{case_count} golden cases\"]; served by app/backend/calibration_route.py:31 and rebuilt/checked at :87-115; also app/frontend/app.js:11 'cached demo (recorded responses)' / '(curated responses)' and app/frontend/api.js:10 'Request failed' at da6afb2 (T-166/qa scope)",
    "why_it_matters": "The audit ranks F7 as P0. The card is marked done on a universal claim its own handoff contradicts ('not mine').",
    "fix": "Either narrow AC1 to backend-authored strings and record the rest as a SCOPE_CUT with cards (qa: evals/run.py:314 caveat builder and its rebuild check; T-166: chip and api.js), or bring the builder into scope. Do not close AC1 with the universal claim.",
    "acceptance_test": "Rendered overview and case text, GET /api/calibration, and both exports contain none of: fixture, golden, recorded replies, curated, Request failed, server answered"},
   {"severity": "minor", "title": "A prose field embeds a reason code in parentheses (judge_says)",
    "evidence": "app/backend/trace.py:959 \"judge_says\": f\"{says} ({r['reason_code']})\"; GET /api/cases/{tok}/judges for case_lib04_dog_bite_scar_revision, judges/disagreements/0/judge_says = 'charge (SHOULD_BE_CHARGE)'; 28 such strings in the library sweep; hidden only by the regex at app/frontend/judges.js:58",
    "why_it_matters": "The card's rule is codes in machine fields only. A human-readable field carries the code and the frontend has to strip it; any other consumer prints it.",
    "fix": "Add a reason_code key carrying the code; set judge_says to the plain sentence only.",
    "acceptance_test": "For every item in the library sweep, no SHOUTING code appears in any string value except under keys reasons, reason_code, code, state_reason, error_class"},
   {"severity": "minor", "title": "_removed_why fallback doubles a phrase in the notes export",
    "evidence": "app/backend/export.py:697-700 and :719. export._removed_why({'message':'JUDGE_UNSUPPORTED: x'}) returns 'it failed a check'; _draft_paragraph prints '- AI wording removed (failed a check: it failed a check) (e9).'; the Removed branch at :723 drops the final period when the fallback fires. Latent: no current narrative.REASONS message has a code.",
    "why_it_matters": "A future message that carries a code would print a doubled, wrong sentence in the paste-out notes.",
    "fix": "Give each branch its own fallback phrase; the Removed fallback ends with a period.",
    "acceptance_test": "Unit test with a code-bearing message: output has neither 'failed a check: it failed a check' nor a SHOUTING token; the Removed line ends with '.'"},
   {"severity": "minor", "title": "FIXTURE_MISS sentence is replay wording with no next step",
    "evidence": "app/backend/why.py:17 'The demo has no recorded AI answer for this step, so this item has not been checked.'; shown as the why of the tray item in case_lib01_er_only_then_gap (artifacts/review-evidence/T-167-r1/sweep_local_distinct_strings.tsv, key why)",
    "why_it_matters": "'Recorded answer' describes the fixture replay mechanism, and the sentence gives no instruction, unlike the demo second-check sentence. AC1's banned list does not name it, so the literal AC passes.",
    "fix": "Reuse the JUDGE_DEMO wording for FIXTURE_MISS items.",
    "acceptance_test": "why.why('FIXTURE_MISS') contains 'not available in this demo' and 'compare', and does not contain 'recorded'"}
 ],
 "whats_right": [
   "Letter and internal notes are clean for the sample and all 15 library cases (0 hits), and the demo edit message says what is unavailable and what to do",
   "The new test file is sensitive: four local mutants each turn it red, and the four older tests were updated to new behaviour assertions rather than loosened",
   "Codes remain in API fields (reasons, warnings[].code), so support can still see the cause"
 ],
 "questions_for_chris": ["Should AC1's 'every user-facing string' cover the calibration sentences that evals/run.py builds and the backend serves, or only backend-authored text?"]}
```
