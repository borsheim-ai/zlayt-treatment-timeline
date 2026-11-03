# T-036 LLM flag passes, round 4 (HEAD 5650eae): claims-adjuster review (Gary Pruitt)

Verdict: **changes** (0 blockers, 1 major, 1 minor, in scope).

Scope per the §7.4 split: the r3 blocker and the r3 majors on self-report labelling precision and the lexicon/DECISIONS narrowing moved to the new card T-061. They are not scored here and I did not downgrade them. They still reproduce at HEAD (probe in the exercised list): "S: neck pain 7/10." and "Self-reported neck pain 7/10." give has_self_report=False, and "Wife complains of neck pain." gives True. T-061 carries them.

Re-judged in scope, against HEAD 5650eae (extracted with `git archive HEAD`, because the live tree has uncommitted edits to flag_templates.py, why.py, confidence.py, pipeline.py, api.py, ingest.py, present.py, schemas.py and 44 fixture files):

- Per-record pass: **clean.** 9 flag prompts, one record block each; 9 extract calls; injected record 3 tagged and its flags need_review (probe section 3; test_flags_injection.py passes).
- Lexicon floor: **clean on the sample.** All 7 lexicon-only flags are needs_review LEXICON_ONLY; no lexicon-only flag is verified (probe section 6; test_flags_sample.py lexicon-floor and LEXICON_ONLY tests pass). I did not run case_06 directly; the 28-day near-miss rests on test_no_spurious_must_not_flags passing.
- Conflicts and J3/J4: **code path clean, committed replay not.** At HEAD the sample's judge calls miss their fixtures (finding 1). On the live tree the same CLI run shows the plan-vs-discharge conflict (f_cx1, "Plan of care: 12 visits.") as needs_review JUDGE_DISAGREES, which is the intended outcome. The accident-date conflict is one code flag, verified.
- Templates: **clean.** 0 own-voice hits and 0 double periods over 42 renders (probe section 5).
- D-030 spans: **clean.** 14 of 14 scripted evidence spans and 8 of 8 live excerpts are verbatim slices of evals/golden/sample.txt, and the live excerpts contain the golden must_contain text for records 7 and 8 (evals/golden/sample.expected.json:218, :574, :594).
- Conflict-pass warning: **clean on HEAD.** 81df4e0 is in HEAD. On both failure paths the run is status done_with_errors, with an error and a warning CONFLICT_PASS_INCOMPLETE; the case-level flag has record_no None, record_nos [], and the neutral why text (probe section 4). The r3 test test_pipeline_surfaces_conflict_pass_failure_as_run_warning passes at HEAD.

Findings:

1. **Major.** Committed fixtures do not replay the judge calls, so a clean checkout of HEAD shows JUDGE_UNAVAILABLE on every model-involved flag. `.venv/bin/python -m pytest tests/unit -q` in the extracted HEAD gives "3 failed, 789 passed": test_t037_backend.py::test_replay_has_no_fixture_miss[sample] ("sample: 20 failed calls, steps ['j1', 'j2', 'j3', 'j4']"), [case_01_date_formats] ("9 failed calls, steps ['j1', 'j2']") and test_sample_replay_shows_verified_entries ("assert (9 == 9 and 0 >= 7)"). `.venv/bin/python -m app.pipeline evals/golden/sample.txt --json` at HEAD writes 20 "llm call failed" lines to stderr (j1 9, j2 3, j3 1, j4 7) and every model-involved flag as lexicon+llm needs_review with reason JUDGE_UNAVAILABLE (artifacts/review-evidence/T-036-r4-cli-sample.json). The live tree has 44 modified tests/fixtures/llm/*.json files, and the same command there gives 0 failures, 3 verified and 5 needs_review JUDGE_DISAGREES (artifacts/review-evidence/T-036-r4-cli-sample-livetree.json). Visible, so not silent, but the committed artifact does not prove AC5. Owner: whoever is re-recording the D-028 judge fixtures (T-037 or T-035); the T-036 code is not the cause.
   Fix: commit the re-recorded fixtures with the prompts they replay, then rerun the three failing tests.
   Acceptance: on a clean checkout of the commit that closes this, `.venv/bin/python -m app.pipeline evals/golden/sample.txt --json 2>&1 | grep -c "llm call failed"` prints 0, and tests/unit/test_t037_backend.py passes.

2. **Minor.** A judge outage does not change the run status. On HEAD the CLI run reports status done with errors [] and warnings [] while 20 judge calls failed. The per-item reason JUDGE_UNAVAILABLE is visible, so this is not a silent pass, but the conflict pass is the only stage with a run-level signal.
   Fix: add a run warning (for example JUDGE_UNAVAILABLE, stage judges) and status done_with_errors when any judge call fails, or state in the handoff that judge outages are item-level only.
   Acceptance: a scripted run with j4 LLMFailed gives a warning with code JUDGE_UNAVAILABLE and status done_with_errors, with the item still needs_review.

What is right:
- The conflict-pass failure is visible at run level on HEAD: status done_with_errors, error and warning CONFLICT_PASS_INCOMPLETE, and a case-level flag with record_nos [] and no "no AI-made entry" wording.
- The live judge path works as specified: disagreeing judges leave the flag needs_review with JUDGE_DISAGREES, and the verified items carry "the second check agreed" wording.
- Every evidence span is verbatim and offset-correct, and every template renders without a double period.

Exercised (HEAD 5650eae unless noted):
- Read personas/claims-adjuster.md; read reviews/T-036-claims-adjuster-r3.md; read board card T-036 (`python3 tools/board.py show T-036`), including the orchestrator split note (T-061 "Self-report label precision ... split from T-036 per §7.4").
- `git rev-parse --short HEAD` -> 5650eae; `git status --short app tests evals memory spec` (dirty: confidence.py, flag_templates.py, why.py, pipeline.py, api.py, ingest.py, present.py, schemas.py, 44 fixture files); `git log --format='%h %s' 3f37141..HEAD -- app/backend app/llm tests/unit` (81df4e0 pipeline conflict-pass warning; 5216d06 D-032).
- `git archive HEAD | tar -x -C artifacts/review-evidence/T-036-r4-commit-5650eae`.
- `.venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q` -> 48 passed in 0.28s.
- `.venv/bin/python -m pytest tests/unit/test_flags_pass.py tests/unit/test_pipeline.py tests/unit/test_conflicts.py tests/unit/test_schemas.py -q` -> 78 passed in 1.27s.
- `.venv/bin/python -m pytest tests/unit -q` -> 3 failed, 789 passed (the three in test_t037_backend.py, finding 1).
- `.venv/bin/python -m pytest tests/unit/test_t037_backend.py -q` on the live tree -> 1 failed, 19 passed (case_02_gap_boundaries).
- `.venv/bin/python tests/fixtures/make_curated.py --check` (extracted HEAD) -> entries: 9 non-verified: []; letter equal: True | notes equal: True; exit 0.
- `artifacts/review-evidence/T-036-r4-probe.py <extracted HEAD>` -> artifacts/review-evidence/T-036-r4-probe.txt (sections 1-6: sample flags with origin and reasons; D-030 span check; per-record prompt count; conflict-pass failure on both paths; template sweep over 42 renders; origin/state counts).
- `.venv/bin/python -m app.pipeline evals/golden/sample.txt --json` at HEAD -> artifacts/review-evidence/T-036-r4-cli-sample.json and .err (20 judge failures).
- Same command on the live tree -> artifacts/review-evidence/T-036-r4-cli-sample-livetree.json and .err (0 failures; per-flag titles, excerpts and why read).
- Verbatim check of the live excerpts against evals/golden/sample.txt (8 of 8 substrings); golden spans read at evals/golden/sample.expected.json:218, :237, :574, :594.
- `grep -n` and read of tests/unit/test_flags_sample.py:45-56 (one-call-per-record assertion) and tests/unit/_fakes.py sample_script (scripted judges agree, no LLM flags; this is why section 1 of the probe shows lexicon-only flags).
- `.venv/bin/python -c` has_self_report checks on HEAD for the carried T-061 items (outputs above).
- Not run: the eval runner (evals.run), case_06 directly, the live app at :7860.

Outside my lens: the conflict and judge plumbing itself (J1/J2/J3/J4 prompts, judge thresholds) beyond what the sample run and test names show.

```json
{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 5650eae via git archive (per-record pass, lexicon floor, conflicts + J3/J4, templates, D-030 spans, conflict-pass warning); live tree compared for the judge fixtures only. r3 self-report blocker and majors are excluded per the T-061 split and carried there. Sample case sample.txt via the fixture pipeline (CLI and scripted FakeCall); no live app URL.",
 "exercised": [
  "Read personas/claims-adjuster.md; reviews/T-036-claims-adjuster-r3.md; board card T-036 and the T-061 split note",
  "git rev-parse --short HEAD; git status --short (dirty live tree listed); git log 3f37141..HEAD on app/backend, app/llm, tests/unit",
  "git archive HEAD | tar -x -C artifacts/review-evidence/T-036-r4-commit-5650eae",
  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q -> 48 passed",
  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py tests/unit/test_pipeline.py tests/unit/test_conflicts.py tests/unit/test_schemas.py -q -> 78 passed",
  ".venv/bin/python -m pytest tests/unit -q (HEAD) -> 3 failed, 789 passed (test_t037_backend.py sample and case_01 replay, sample replay shows verified entries)",
  ".venv/bin/python -m pytest tests/unit/test_t037_backend.py -q (live tree) -> 1 failed, 19 passed",
  ".venv/bin/python tests/fixtures/make_curated.py --check -> letter equal True, notes equal True",
  "artifacts/review-evidence/T-036-r4-probe.py <HEAD tree> -> T-036-r4-probe.txt (sample flags, D-030 spans 0 mismatches, 9 one-block flag prompts, conflict-pass failure both paths, template sweep 0 hits over 42 renders)",
  ".venv/bin/python -m app.pipeline evals/golden/sample.txt --json (HEAD) -> T-036-r4-cli-sample.json and .err (20 judge call failures, all flags JUDGE_UNAVAILABLE)",
  ".venv/bin/python -m app.pipeline evals/golden/sample.txt --json (live tree) -> T-036-r4-cli-sample-livetree.json and .err (0 failures; 3 verified, 5 JUDGE_DISAGREES)",
  "verbatim check of live excerpts in evals/golden/sample.txt (8 of 8); golden must_contain at evals/golden/sample.expected.json:218, :574, :594",
  "read tests/unit/test_flags_sample.py:45-56 and tests/unit/_fakes.py sample_script",
  ".venv/bin/python -c 'from app.backend import grounding as G; G.has_self_report(...)' on HEAD: 'S: neck pain 7/10.' False; 'Self-reported neck pain 7/10.' False; 'Wife complains of neck pain.' True (carried to T-061)"
 ],
 "verdict": "changes",
 "scores": {"surfaces_every_attack_item_on_sample": 5, "per_record_pass": 5, "lexicon_floor": 4, "conflicts_j3_j4": 3, "templates": 5, "d030_spans": 5, "conflict_pass_warning": 5, "test_honesty": 3},
 "findings": [
  {"severity": "major",
   "title": "Committed fixtures do not replay judge calls; the committed sample shows JUDGE_UNAVAILABLE on every model-involved flag",
   "evidence": "HEAD pytest tests/unit -q: '3 failed, 789 passed'; test_t037_backend.py::test_replay_has_no_fixture_miss[sample] 'sample: 20 failed calls, steps ['j1', 'j2', 'j3', 'j4']'; [case_01_date_formats] '9 failed calls, steps ['j1', 'j2']'; test_sample_replay_shows_verified_entries 'assert (9 == 9 and 0 >= 7)'. HEAD CLI: artifacts/review-evidence/T-036-r4-cli-sample.err has 20 'llm call failed' lines (j1 9, j2 3, j3 1, j4 7); T-036-r4-cli-sample.json all 9 model flags lexicon+llm needs_review reasons ['JUDGE_UNAVAILABLE']. Live tree: 44 modified tests/fixtures/llm/*.json; T-036-r4-cli-sample-livetree.json 0 failures, 3 verified, 5 JUDGE_DISAGREES.",
   "why_it_matters": "The flags are visible as needs_review, so nothing is silently lost. But the committed artifact cannot show the J3/J4 path on the sample, and AC5 cannot be proven from HEAD. The code path is right on the live tree, so the cause is uncommitted fixture re-recording, not T-036 logic.",
   "fix": "Commit the re-recorded D-028 judge fixtures together with the prompts they replay, then rerun the three failing tests on a clean checkout. Owner: whoever is re-recording (T-037 or T-035).",
   "acceptance_test": "On a clean checkout of the fixing commit: `.venv/bin/python -m app.pipeline evals/golden/sample.txt --json 2>&1 | grep -c 'llm call failed'` prints 0, and tests/unit/test_t037_backend.py passes in full."},
  {"severity": "minor",
   "title": "A judge outage leaves run status done with no run-level warning",
   "evidence": "HEAD CLI with 20 judge failures (T-036-r4-cli-sample.json): 'status': 'done', 'errors': [], 'warnings': []. The conflict pass is the only stage with a run-level signal (pipeline CONFLICT_PASS_INCOMPLETE, probe section 4).",
   "why_it_matters": "The item-level reason JUDGE_UNAVAILABLE is visible to the attorney, so this is not a silent pass. But a reader of the run status is told the run is clean while half its judge calls failed.",
   "fix": "Add a run warning JUDGE_UNAVAILABLE (stage judges) and set status done_with_errors when any judge call fails; or state in the handoff that judge outages are item-level only.",
   "acceptance_test": "Scripted run with j4 LLMFailed: out['warnings'] contains code JUDGE_UNAVAILABLE, out['status'] == 'done_with_errors', and the affected flag is needs_review with JUDGE_UNAVAILABLE."}
 ],
 "whats_right": [
  "The conflict-pass failure is visible at run level on HEAD: status done_with_errors, CONFLICT_PASS_INCOMPLETE as error and warning, and a case-level flag with record_nos [] and neutral why text (probe section 4).",
  "Every evidence span is verbatim at its offset (0 mismatches in probe section 2), and the live excerpts contain the golden must_contain text for records 7 and 8.",
  "Judge disagreement is handled as specified: the live run leaves five flags needs_review with JUDGE_DISAGREES, and the conflict flag for the 12-visit plan is surfaced, not dropped."
 ],
 "questions_for_chris": [
  "Should a judge outage set a run-level partial status the way the conflict pass now does (finding 2), or is item-level JUDGE_UNAVAILABLE the intended contract?",
  "Who commits the re-recorded D-028 judge fixtures, and in which card? The committed HEAD replay is red until they land (finding 1).",
  "T-061 carries the r3 self-report blocker and majors. Is any of them needed before the M2 gate, or can T-061 close after it?"
 ]}
```
