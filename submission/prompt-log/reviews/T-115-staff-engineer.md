# T-115 review: E2E suite green on clean HEAD (staff-engineer-reviewer)

Pinned: commit 400a8c06c96bafce4dd61f177f97d1fa2ab4d50f (parent c1b44be). Reviewed from `git archive 400a8c0` copy, not the working tree.
Model: claude-haiku-5-5.

## Verdict: changes (0 blockers, 3 majors, 1 minor)

The regeneration is narrower than the commit says and does not change any judge answer. T-117 is a real product bug and the strict xfail is the right way to record it. But the card's central claim, that the full e2e suite passes at HEAD with 172 passed, does not reproduce at 400a8c0. At HEAD I got 169 passed with 3 failed (run 2), or 156 passed with 1 failed and 16 skipped (run 1). The evidence in the handoff was taken at 36ceb38, three commits earlier.

## What I ran and what I found

**E2E at HEAD (own server, archive of 400a8c0, port 7971, fixture backend, curated set, ZLAYT_MODE=local).**
- Run 1, ZLAYT_DB not exported to pytest: `1 failed, 156 passed, 16 skipped, 1 xfailed in 223.67s`. The 16 skips are the ZLAYT_DB-dependent tests in test_code_check_refusal.py, which never ran.
- Run 2, fresh scratch DB, ZLAYT_DB exported to pytest: `3 failed, 169 passed, 1 skipped, 1 xfailed in 231.41s`. Only the T-117 xfail is strict and xfailed.
- Expected from the card: 172 passed, 1 skipped, 1 xfailed. Not reproduced.

**Deterministic failure at HEAD.** `test_p_moves_focus_into_pane_and_escape_returns` fails (run 1 and run 2, and again alone twice): `tests/e2e/test_side_by_side.py:61`, `Locator expected to be focused ... Actual value: inactive`. The aria snapshot shows `Select an item, or press j, to see its source record here.` The same test run alone against a `git archive 36ceb38` copy on its own server (port 7972) gives `1 passed`. 3e3f3b7 (T-060, in the card's history but not in its evidence) changed the single-key handler so it acts only from an item row (`app/frontend/review.js:311-312`, `const row = RV.itemRowOf(t); if (!row) return;`). The test presses `j` from the page body (`test_side_by_side.py:60`). That is test drift from an intended product change. It is still red at the card's commit.

**Flaky test.** `tests/e2e/test_stepper.py:204` and `:257` read `judge-summary-counts` with `inner_text()`, with no auto-wait, after waiting only for the container. The text is sometimes `loading…`. Run 2 failed both. Rerunning the pair alone three times at HEAD gave `1 failed, 1 passed`, `2 passed`, `1 failed, 1 passed`. Run 1 passed both, so the same HEAD is not reproducible.

**Unit suite at HEAD.** `LLM_BACKEND=fixture pytest tests/unit`: `2556 passed, 4 skipped in 175.90s`.

**Curated regeneration (400a8c0, 9 files).** `git show --stat 400a8c0` shows 5 renames (only `recorded_at` changed), 2 new files and 2 deleted files: 7 keys out, 7 keys in. I replayed the check at a9a27ed (last commit where the curated set was valid, `make_curated check: True`, 47 of 47 keys), at HEAD and at c1b44be, instrumenting `prompt_hash`:
- The 7 changed keys are 6 judge_flag `v2` to `v3` (J4) and 1 judge_conflict `v4` to `v5` (J3). The commit and handoff mention only judge_flag_v3.
- For all 7, the user text and JSON schema are identical. Only the system prompt text changed: J4 gained a missed_care definition and a scene-facts rule; J3 gained a CAN_BOTH_BE_TRUE rule for denials about different body parts. These are intended product prompt changes, not regen artefacts.
- Every new curated answer equals the old one (J4 `agree`/`NONE` ×6, J3 `conflict`/`NONE` ×1). No judge verdict changed.
- `make_curated.py --check` at HEAD: exit 0, `letter equal: True | notes equal: True`. At c1b44be: exit 1, `JUDGE_NOT_RUN` (7 keys missing). So the staleness was real.

**Where the regeneration still papers over something.**
- Three of the six re-keyed J4 answers (`41e42a29…`, `5b05ba47…`, `e2f91427…`) have no recorded model output under judge_flag_v3 anywhere in `tests/fixtures/llm/`. Their only answer is the hand-scripted `agree` from `tests/fixtures/make_curated.py:49-52`, which picks `agree` for every J4 call.
- The J3 key `d1e36f01…` has a real claude-cli recording (`recorded_from` model claude-haiku-5-5, 2026-11-02T07:04:40Z) with `reason_code: PLAN_VS_ACTUAL`. Because `FIXTURE_SET=curated` is read first (`app/llm/backends/fixture.py:21-24`), the scripted answer with `reason_code: NONE` replaces it in the e2e run.
- The committed controls report that covers judge_conflict_v5 is red: `evals/reports/controls-20261102T090925Z.md:3` says `controls_ok: False`, and line 8 shows J3 13/17 caught with false agrees `J3V1, J3V9, J3V13, H3V5`. It was written 27 minutes before the regen commit. Neither the card nor the commit mentions it.

**T-117 is a real product bug.** Confirmed, see finding list. Reproduced with `--runxfail`: the judge-row titles include `'f_r5_1'` with no `Record N` cue, while the other five rows carry cues. Root cause: `app/frontend/review.js:16-22` (`RV.find`) searches entries, undated entries, amounts and flags, but not `case.tray`. D-053 flags are only in `case.tray` (`app/backend/present.py:236-241`). `stepper.js:51-66` (`S.label`, `S.cue`) fall back to the raw id and an empty cue, and `judges.js:91` renders that label as the row title. The xfail is `strict=True` and names T-117.

**No recurrence guard.** `grep -rln make_curated tests` finds only `tests/fixtures/make_curated.py`. No test runs `--check`, so the staleness was caught only by the e2e failures.

## Findings

Severity follows CONTRACT D.2. None of the §5 red flags apply: no silent fallback, no float money, no LLM date or total, no network in tests, no secrets.

1. **major, the card's AC1 (HEAD green) is not met; the evidence is for 36ceb38.** See the deterministic failure and flaky-test paragraphs above. The handoff's "Verified: full tests/e2e on a clean HEAD worktree 172 pass" is not true for 400a8c0.
2. **major, flaky e2e race in judge-summary assertions** (`tests/e2e/test_stepper.py:204`, `:257`). Reproduce with the two test ids in a loop (three runs above).
3. **major, the regeneration re-keys judge answers without disclosing the J3 re-key, and leaves scripted answers standing for prompts whose live control is red.** See the three bullets above. No verdict changed, so this is not a silent product change, but the commit claim "12 e2e failures were fixture drift" is only true for keys.
4. **minor, no guard for curated-set staleness.** Add a unit test that runs `make_curated check()` against `tests/fixtures/llm/curated`. The handoff itself says a unit test would stop recurrence.

## Fixes requested

- F1: Rebase the test to focus an item row before `j` at `tests/e2e/test_side_by_side.py:60`. Re-run `git archive 400a8c0` with its own server and quote the full summary line. Only then cite 172.
- F2: Replace the one-shot `inner_text()` at `test_stepper.py:204` and `:257` with a web-first assertion (`expect(...).to_have_text(re.compile(...))`). Show 10 consecutive green runs of the two tests.
- F3: Correct the commit/handoff to say 6 J4 and 1 J3. Restore `reason_code: PLAN_VS_ACTUAL` for the J3 key or drop the curated override for it. Record in `memory/DECISIONS.md` or `ASSUMPTIONS.md` that three J4 v3 answers are scripted, and that judge_conflict_v5 controls were red at 090925Z. Re-run controls for v5 and cite the report.
- F4: Add the unit test in F4 above and show it fails if a prompt hash is changed.

## What's right

1. The regeneration changes only answer-file keys. Payload replay shows user text and schema unchanged for all 7 keys, and `make_curated --check` passes at HEAD with letter and notes equal to the golden.
2. The T-117 xfail is `strict=True`, names the card, and matches the traced root cause (`review.js:16-22` omits `case.tray`).
3. The 400a8c0 test diff is one marker line. No assertion was weakened. The unit suite is green at HEAD (2556 passed, 4 skipped).

## Questions for Chris

- Should curated answers override recorded claude-haiku-5-5 outputs, as they do for the J3 key (PLAN_VS_ACTUAL becomes NONE)? If yes, that needs a recorded decision.
- Is a curated J3 `conflict` answer acceptable for judge_conflict_v5 while its live controls are red?

## Evidence

- `artifacts/review-evidence/T-115-staff-engineer/e2e_run1_zlayt_db_unset.txt`
- `artifacts/review-evidence/T-115-staff-engineer/e2e_run2_zlayt_db_set.txt`
- `artifacts/review-evidence/T-115-staff-engineer/make_curated_check_c1b44be.txt`
- Scratch (not in repo): archive copies under the scratchpad `T115_staff_r1/` directory (HEAD `tree/`, `parent/`, `a9a/`, `base36/`); payload dumps `head_full.json`, `a9a/check.json`.

```json
{"card": "T-115", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 400a8c0 (parent c1b44be; 36ceb38 is the card's cited evidence commit); archive copy of 400a8c0; own fixture server http://127.0.0.1:7971 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), stopped by PID; tests/e2e, tests/unit, tests/fixtures/make_curated.py, tests/fixtures/llm/curated",
 "exercised": [
  "read personas/staff-engineer.md; board show T-115 and T-117",
  "git archive 400a8c06c96bafce4dd61f177f97d1fa2ab4d50f into scratchpad T115_staff_r1/tree; git show --stat and full diff of 400a8c0 for tests/e2e and tests/fixtures/llm/curated",
  "fixture server on 127.0.0.1:7971 from the archive; full pytest tests/e2e run 1 (ZLAYT_DB unset in pytest): 1 failed, 156 passed, 16 skipped, 1 xfailed",
  "full pytest tests/e2e run 2 (fresh DB, ZLAYT_DB set): 3 failed, 169 passed, 1 skipped, 1 xfailed",
  "test_p_moves_focus_into_pane_and_escape_returns alone x2 at 400a8c0 (fails) and alone on a git archive 36ceb38 copy at server 127.0.0.1:7972 (passes); server stopped by PID",
  "test_judge_panel_collapsed_summary_and_labels + test_judge_panel_when_nothing_objected x3 at 400a8c0 (mixed results)",
  "pytest tests/unit with LLM_BACKEND=fixture at 400a8c0: 2556 passed, 4 skipped",
  "make_curated.py --check at 400a8c0 (exit 0, letter/notes equal) and at c1b44be (exit 1, JudgeNotRun)",
  "instrumented replay (prompt_hash wrapper) at a9a27ed, c1b44be and 400a8c0: mapped the 7 changed keys to judge_flag v2->v3 (x6) and judge_conflict v4->v5 (x1); diffed system, user and schema per key",
  "provenance of tests/fixtures/llm/{d1e36f01,40edf164,6d5e6fe3,b362099f}*.json (recorded_from claude-cli, claude-haiku-5-5); absence of recorded files for 41e42a29, 5b05ba47, e2f91427",
  "tallied verdict/reason_code over curated judge answers at 400a8c0 and c1b44be (identical: supported/NONE 18, agree/NONE 9, conflict/NONE 1)",
  "T-117 repro: pytest --runxfail test_judge_panel_one_row_per_item_with_record_cue -> titles include 'f_r5_1' with no Record cue",
  "read app/frontend/review.js:15-22, 311-318; app/frontend/stepper.js:51-66; app/frontend/judges.js:91; app/backend/present.py:236-241; tests/fixtures/make_curated.py:38-52; app/llm/backends/fixture.py:20-26; evals/reports/controls-20261102T090925Z.md:3,8",
  "grep -rln make_curated tests (only tests/fixtures/make_curated.py)"
 ],
 "verdict": "changes",
 "scores": {"e2e_green_at_head": 2, "e2e_reproducibility": 2, "fixture_regen_faithfulness": 3, "xfail_discipline_T117": 5, "test_integrity_no_weakening": 4, "unit_suite_at_head": 4},
 "findings": [
  {"severity": "major",
   "title": "AC1 not met at HEAD: 172 passed does not reproduce at 400a8c0; the cited evidence is for 36ceb38, three commits earlier",
   "evidence": "Run 1 at 400a8c0: '1 failed, 156 passed, 16 skipped, 1 xfailed in 223.67s'. Run 2 (ZLAYT_DB set): '3 failed, 169 passed, 1 skipped, 1 xfailed in 231.41s'. Deterministic failure tests/e2e/test_side_by_side.py:61 (test_p_moves_focus_into_pane_and_escape_returns): 'Locator expected to be focused ... Actual value: inactive'; aria 'Select an item, or press j, to see its source record here.' Same test passes on git archive 36ceb38 (1 passed). Cause: 3e3f3b7 app/frontend/review.js:311-312 'const row = RV.itemRowOf(t); if (!row) return;' (j/k act only from an item row); test presses j from body at test_side_by_side.py:60. git merge-base --is-ancestor 36ceb38 400a8c0 succeeds; git log 36ceb38..400a8c0 lists 3e3f3b7, b5fb35c, c1b44be.",
   "why_it_matters": "The card's only deliverable is a green e2e suite at HEAD; the handoff ('Verified: full tests/e2e on a clean HEAD worktree 172 pass') is not true for the commit it is attached to. The milestone gate would inherit a red suite with a false green record.",
   "fix": "Test drift, not a product bug: focus an item row before pressing j at tests/e2e/test_side_by_side.py:60, then re-run on a fresh git archive of 400a8c0 and quote the full summary line. Correct the handoff to name the commit it was run on.",
   "acceptance_test": "git archive 400a8c0 -> own fixture server -> ZLAYT_DB=<scratch> E2E_BASE_URL=... pytest tests/e2e -q prints 0 failed and 172 passed, 1 skipped, 1 xfailed (strict, T-117)."},
  {"severity": "major",
   "title": "Flaky e2e race: judge-summary counts read with inner_text() before they render",
   "evidence": "tests/e2e/test_stepper.py:202-204 waits only for judge-summary, then assert re.search(..., jp.get_by_test_id('judge-summary-counts').inner_text()); the failure text is 'loading…' (line 204). Same pattern at :257. Pair run x3 at 400a8c0: '1 failed, 1 passed' / '2 passed' / '1 failed, 1 passed'. Run 1 passed both; run 2 failed both (AssertionError: judge-summary-counts inner_text 'loading…').",
   "why_it_matters": "A gate that passes on one run and fails on the next cannot be used as evidence, and it makes the AC1 result unreproducible (persona criterion 14: no timing dependence).",
   "fix": "Use a web-first assertion that auto-waits, e.g. expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\\d+ checked, \\d+ agreed with the draft, 3 questioned')), and the same for the 'checked \\d+, all agreed' case; do not read inner_text() once.",
   "acceptance_test": "Both tests pass in 10 consecutive runs of the pair at the HEAD archive, with a fresh ZLAYT_DB each time."},
  {"severity": "major",
   "title": "Regeneration re-keys 7 judge answers, one of them a J3 (judge_conflict v4->v5) not mentioned in the commit; 3 J4 v3 answers and the J3 answer are scripted, and the J3 recording is overridden",
   "evidence": "Replay of a9a27ed (check True, 47/47), c1b44be (JudgeNotRun) and 400a8c0 with prompt_hash instrumentation: the 7 changed keys are judge_flag v2->v3 x6 and judge_conflict v4->v5 x1; user text and schema identical, only system prompt text differs. Curated answers unchanged in content (agree/NONE x6, conflict/NONE x1). Recorded files: tests/fixtures/llm/d1e36f0196ae18855248ea37297b943bf22d277951ff13184756fb659abb91ea.json recorded_from claude-cli claude-haiku-5-5 with output {reason_code: PLAN_VS_ACTUAL, verdict: conflict}; the curated file for the same key has reason_code NONE, and FIXTURE_SET=curated is read first (app/llm/backends/fixture.py:21-24). Keys 41e42a29..., 5b05ba47..., e2f91427... have no file outside tests/fixtures/llm/curated. make_curated.py:49-52 picks 'agree' for every J4 call. evals/reports/controls-20261102T090925Z.md:3 'controls_ok: False' and :8 J3 judge_conflict_v5 13/17, false agrees J3V1, J3V9, J3V13, H3V5; that report predates the regen commit (09:36Z) by 27 minutes.",
   "why_it_matters": "No verdict changed, so this is not a silent product change, but the green curated e2e now rests on hand-scripted 'agree' answers for judge_flag_v3 (three keys have no model output under v3) and a J3 answer that drops the recorded reason. The judge_conflict_v5 live controls are red and the card does not say so. The commit message's 'fixture drift' label is true for keys, not for judge behaviour.",
   "fix": "Correct the commit/handoff to 6 J4 + 1 J3 re-keys. Restore reason_code PLAN_VS_ACTUAL for the J3 key (or stop the curated override for that key). Record in memory/DECISIONS.md or ASSUMPTIONS.md which curated judge answers are scripted and that judge_conflict_v5 controls were red at 20261102T090925Z. Re-run judge controls for v5 and cite the new report.",
   "acceptance_test": "A test asserts for each curated judge key that the reason_code equals the recorded one where a recording exists, and that every curated key maps to a judge prompt whose latest committed controls report is controls_ok True (or the exception is recorded in DECISIONS)."},
  {"severity": "minor",
   "title": "No guard against curated-set staleness; make_curated --check is run by nobody",
   "evidence": "grep -rln make_curated tests returns only tests/fixtures/make_curated.py. At c1b44be, 'python tests/fixtures/make_curated.py --check' exits 1 with JudgeNotRun (7 keys missing). The handoff says 'a unit test for that would stop recurrence' but none was added in 400a8c0 (git show --stat 400a8c0 lists only tests/e2e/test_stepper.py and tests/fixtures/llm/curated).",
   "why_it_matters": "Staleness was caught only indirectly, as 12 e2e failures. The next prompt bump will silently repeat it.",
   "fix": "Add a unit test that runs make_curated check() (or the equivalent key-coverage check) against tests/fixtures/llm/curated.",
   "acceptance_test": "Changing a judge prompt file without regenerating the curated set makes the new unit test fail; restoring the set makes it pass."}
 ],
 "whats_right": [
  "The regeneration changes only answer files; replay shows user text and schema identical for all 7 keys, and make_curated --check passes at HEAD with letter and notes equal to the golden.",
  "The T-117 xfail is strict=True, names the card, and matches the traced root cause (review.js:16-22 RV.find omits case.tray; present.py:236-241 puts D-053 flags there); --runxfail shows the 'f_r5_1' title with no Record cue.",
  "The 400a8c0 test diff is one marker line; no assertion was weakened. Unit suite at HEAD: 2556 passed, 4 skipped."
 ],
 "questions_for_chris": [
  "Should curated answers override recorded claude-haiku-5-5 outputs (the J3 key goes from PLAN_VS_ACTUAL to NONE)? If yes, record it as a decision.",
  "Is a scripted curated J3 'conflict' answer acceptable for judge_conflict_v5 while its committed live controls report is controls_ok False?"
 ]}
```
