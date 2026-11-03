# T-115 round 2 review: curated fixture set and e2e at HEAD (staff-engineer-reviewer)

Pinned: HEAD `08c921e878edfb8571e60972bbf5681e16d328fc` (parent `288affc`). Reviewed from `git archive HEAD` copy in scratch, not the working tree (which is dirty with other workers' edits).
Model: claude-haiku-5-5.

## Verdict: changes (0 blockers, 3 majors, 4 minors)

The brief's four checks all pass. The fixture change does what the card says: no judge answer is left in the curated set, all 19 new judge answers are real claude-cli recordings, and the guard test fails on both a shadow and a scripted judge file. The e2e suite is green at HEAD (172 passed, 1 skipped, 1 xfailed strict on T-117). What is still open:

- The round-1 e2e race is only half fixed (`test_stepper.py:204`).
- D-029 is now contradicted by the commit and has no amendment.
- The round-1 controls-red evidence for `judge_conflict_v5` is still unaddressed.

Commit 08c921e carries no unrelated content. Its 49 paths are the T-115 fixtures and the two T-115 files, but its commit message is a copy of the T-079 message (see F4).

## Brief checks

| Check | Result |
|---|---|
| 19 new claude-cli recordings | Confirmed: 19 `A` judge files under `tests/fixtures/llm/`, all `recorded_from` `claude-cli` / `claude-haiku-5-5`, `recorded_at` 2026-11-02T10:06:15Z to 10:07:27Z. |
| All 28 curated judge files removed | Confirmed: parent had 47 curated files (28 judge, 19 generator); commit deletes 28, all judge; curated now holds 19 generator files, 0 judge. |
| No curated judge shadows a recording | Confirmed: `classify.py` on the archive, curated = 19 `gen`, 0 `judge`. |
| Every judge answer the demo needs is a recording | Library replay (`evals/library_report.py` through `judge_demand.py`): 244 judge replays, all from top-level recordings, 0 from curated, 0 misses. The sample path passes `make_curated --check`. See F7 for the e2e-only misses. |
| `make_curated.py` no longer scripts judge answers | Build and check route `verdict` schemas to recorded replay. A dead scripted branch remains (F4). |
| `test_curated_fixtures.py` fails on a copied recording | Confirmed: shadow mutant (`0ec6b542...json` copied into curated) gives `1 failed, 5 passed`, `SHADOWS_RECORDING 0ec6b54252d8`. |
| `make_curated.py --check` passes | Confirmed: exit 0, `entries: 9 non-verified: []`, `letter equal: True | notes equal: True`. |
| Full tests/e2e on own server, except T-117 | Confirmed: `172 passed, 1 skipped, 1 xfailed in 230.06s`. Skip is `test_ladder_gate.py:37` ("no rejected item in the sample fixture run"). Server (PID 97679, port 7981) stopped; port confirmed closed. |

## Findings

**F1 (major, carried from r1 F2, half-fixed).** `tests/e2e/test_stepper.py:202` waits only for the `judge-summary` row, then `:204` reads `judge-summary-counts` with a one-shot `inner_text()`. Commit 6e880e6 converted `:257` to a retrying `to_have_text`, but `:204` was left as it was. A flaky race is still in the suite that the card says is green.

**F2 (major, D-029 contradicted and not amended).** `memory/ORCHESTRATOR_DECISIONS.md:37` (D-029) says the curated set holds "hand-checked generator/judge responses" and names the path `tests/fixtures/llm/recorded/`. That path does not exist; the recorded set is the top-level `tests/fixtures/llm/` (1089 files). The commit removes all curated judge answers, so the decision text is now false. `make_curated.py:1-8` and `test_curated_fixtures.py:1-9` cite D-029 for a judge rule that D-029 does not state. `grep -n -i curated memory/DECISIONS.md memory/ASSUMPTIONS.md memory/ORCHESTRATOR_DECISIONS.md` shows no amendment.

**F3 (major, carried from r1 F3, partly resolved).** The scripted J3/J4 answers are gone and the J3 key now replays its recorded `PLAN_VS_ACTUAL`. Still open: `evals/reports/controls-20261102T090925Z.md:3` reads `controls_ok: False` for `judge_conflict_v5` and `judge_flag_v3`, with J3 13/17 caught and false agrees `J3V1, J3V9, J3V13, H3V5` (line 8). That is the newest controls report (`ls evals/reports | grep controls`). Nothing in DECISIONS or ASSUMPTIONS records the red status, and no re-run is cited.

**F4 (minor, dead scripted branch).** `tests/fixtures/make_curated.py:55-60` still scripts `verdict` answers inside `answer()`. It is unreachable today because `fake()` at `:118-119` routes any `verdict` schema to `judge()` first. One routing edit would bring scripted judge answers back, and the unit guard only inspects files that land in the curated dir.

**F5 (minor, commit message does not describe the commit).** `git show -s --format='%h %s' 328428f` and `08c921e` have the identical subject "feat(evals): library packets lib08..lib15 ... (T-079)". 328428f is the real T-079 commit (313 files, 291 `tests/fixtures/llm` files, `evals/library/*`, `evals/library_report.py`). 08c921e's 49 paths contain no `evals/` or `expected.json` file, and its body's "291 claude-cli fixtures" is 328428f's count. The card note "swept into T-079's commit" points at the wrong commit. Nothing unrelated to T-079 or T-115 is in 08c921e's content; the problem is the audit record.

**F6 (minor, error visibility).** `app/backend/api.py:162` and `:184` log only `unhandled %s` with the class name. The e2e run logged 20 such lines (15 `TypeError`, 5 `AttributeError`) with no route and no traceback, so those requests cannot be identified from the run. Each returns an explicit 500 "Something went wrong.", so this is not a silent fallback. I did not trace which requests produced them.

**F7 (minor, e2e-only judge misses, pre-existing).** The e2e run logged 26 `llm call failed` lines naming 10 distinct `prompt_hash` values. None of the 10 is in the parent's curated or recorded set (`check_missing.py`), so 08c921e did not cause them. The library replay has zero judge misses. The demo can still issue judge calls with no recording outside the golden and library paths; I did not trace which e2e flows issue them or what the UI shows.

## Round-1 status

- r1 F1 (side-by-side focus test): fixed. `tests/e2e/test_side_by_side.py:61` focuses a row before `p`.
- r1 F2 (inner_text race): partly fixed, see F1.
- r1 F3 (regeneration disclosure and scripted J4/J3): scripted answers removed, see F3 for the open controls evidence.
- r1 F4 (staleness guard): fixed. `test_make_curated_check_is_current` fails when a judge prompt changes (scratch mutant of `app/llm/prompts/judge_flag_v3.md`: `1 failed, 5 passed`, JUDGE_NOT_RUN).

## What I exercised

- Read `personas/staff-engineer.md`, `board show T-115` (notes), `reviews/T-115-staff-engineer.md` (r1), D-029 at `memory/ORCHESTRATOR_DECISIONS.md:37`.
- `git show --stat --name-status 08c921e`, `git show -s 328428f`, `git merge-base --is-ancestor 328428f 08c921e`, `git log 328428f..08c921e`, `git ls-tree` counts of `evals/library`.
- `git archive HEAD` into scratch `T115_staff_r2/tree`.
- Classified the top-level recorded set (683 judge `claude-haiku-5-5`, 406 generator `claude-sonnet-5-5`) and the curated set (19 generator). `parent_judges.py`: parent curated 28 judge + 19 generator; deleted 28, all judge.
- `.venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q` on the archive: 6 passed.
- `.venv/bin/python tests/fixtures/make_curated.py --check` on the archive: exit 0.
- Mutants in scratch copies: shadow (`0ec6b54252d8...` copied into curated) gives 1 failed; scripted judge (key `ffff...`) gives 1 failed; judge prompt edit gives `test_make_curated_check_is_current` 1 failed.
- Fixture server from the archive on `127.0.0.1:7981` (`LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local ZLAYT_DB` in scratch). `E2E_BASE_URL=http://127.0.0.1:7981 ZLAYT_DB=<scratch> pytest tests/e2e -q`: 172 passed, 1 skipped, 1 xfailed in 230.06s. Server stopped by PID 97679; port closed.
- `evals/library_report.py` via `judge_demand.py` on the archive: 239 generator and 244 judge replays, 0 curated judge, 0 judge misses, 1 generator miss (`83bcee07...`, lib01 r3, pre-existing).
- Server log grep and `check_missing.py` for the 10 failed hashes.
- Read `app/backend/api.py:150-190`, `tests/e2e/test_stepper.py:202-204,256-257` and `tests/e2e/test_side_by_side.py:61` at HEAD.
- Not run: the full `tests/unit` suite (outside this brief's four checks).

Evidence copied to `artifacts/review-evidence/T-115-staff-engineer-r2/`: `e2e_r2_summary.txt`, `server_7981.log`, `library_report_head.md`, `judge_demand.py`, `classify.py`, `check_missing.py`, `parent_judges.py`, `added19.txt`, `deleted28.txt`.

```json
{"card": "T-115", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 08c921e878edfb8571e60972bbf5681e16d328fc (parent 288affc); git archive copy; own fixture server http://127.0.0.1:7981 (LLM_BACKEND=fixture FIXTURE_SET=curated ZLAYT_MODE=local, scratch ZLAYT_DB), stopped by PID 97679; sample golden case evals/golden/sample.txt; tests/e2e, tests/unit/test_curated_fixtures.py, tests/fixtures/make_curated.py, tests/fixtures/llm/ (recorded and curated)",
 "exercised": [
  "read personas/staff-engineer.md; board show T-115 notes; reviews/T-115-staff-engineer.md (r1); memory/ORCHESTRATOR_DECISIONS.md:37 (D-029)",
  "git show --stat/--name-status 08c921e (49 paths: 47 under tests/fixtures/llm, make_curated.py, test_curated_fixtures.py); git show -s 328428f; git merge-base --is-ancestor 328428f 08c921e (true); git log 328428f..08c921e",
  "git archive HEAD into scratch T115_staff_r2/tree",
  "classified recorded set (top-level: 683 judge claude-haiku-5-5, 406 generator claude-sonnet-5-5) and curated set (19 generator, 0 judge); 19 added files all judge, claude-cli, claude-haiku-5-5, recorded_at 2026-11-02T10:06-10:07Z",
  "parent curated set 08c921e^: 47 files, 28 judge, 19 generator; the 28 deleted files are all judge",
  ".venv/bin/python -m pytest tests/unit/test_curated_fixtures.py -q on archive: 6 passed",
  ".venv/bin/python tests/fixtures/make_curated.py --check on archive: exit 0, entries 9 non-verified [], letter equal True | notes equal True",
  "mutant shadow: 0ec6b54252d8 judge copied into curated; test_curated_fixtures.py: 1 failed, 5 passed (SHADOWS_RECORDING)",
  "mutant scripted: judge answer under key ffff...ff with no recording; test_curated_fixtures.py: 1 failed, 5 passed (SCRIPTED_JUDGE)",
  "mutant prompt: appended line to app/llm/prompts/judge_flag_v3.md in scratch; test_make_curated_check_is_current fails (JUDGE_NOT_RUN); 1 failed, 5 passed",
  "full pytest tests/e2e -q against 127.0.0.1:7981 (archive server), ZLAYT_DB in scratch: 172 passed, 1 skipped (test_ladder_gate.py:37), 1 xfailed (T-117 strict) in 230.06s; server stopped by PID 97679, port closed",
  "evals/library_report.py via judge_demand.py wrapper on archive: 239 generator and 244 judge replays from recordings, 0 curated judge, 0 judge misses, 1 generator miss 83bcee07 (lib01 r3, pre-existing)",
  "server_7981.log: 20 unhandled (15 TypeError, 5 AttributeError), 26 llm call failed over 10 distinct prompt_hash; check_missing.py: none of the 10 in parent curated or recorded set",
  "read app/backend/api.py:150-190; tests/e2e/test_stepper.py:202-204 and :256-257; tests/e2e/test_side_by_side.py:61 at HEAD archive; app/llm/backends/fixture.py call() fallback order",
  "grep of memory/DECISIONS.md, memory/ASSUMPTIONS.md, memory/ORCHESTRATOR_DECISIONS.md for curated/T-115: no amendment to D-029",
  "read evals/reports/controls-20261102T090925Z.md:3,8 (controls_ok False, J3 13/17); ls evals/reports controls files (newest is 090925Z)",
  "not run: full tests/unit suite (outside the brief's four checks)"
 ],
 "verdict": "changes",
 "scores": {"judge_answers_are_recordings": 5, "curated_has_no_judge_answers": 5, "guard_test_catches_shadow_and_scripted": 5, "make_curated_check_current": 5, "e2e_green_at_head": 4, "e2e_reproducibility": 3, "decision_record_consistency": 2, "commit_scope_and_message": 3, "error_visibility": 3, "scripted_code_removed": 3},
 "findings": [
  {"severity": "major",
   "title": "r1 F2 only half-fixed: judge-summary-counts still read with one-shot inner_text() at test_stepper.py:204",
   "evidence": "tests/e2e/test_stepper.py:202 waits only for the judge-summary row: jp.get_by_test_id('judge-summary').wait_for(); :204 asserts re.search(..., jp.get_by_test_id('judge-summary-counts').inner_text()). Commit 6e880e6 changed :257 to expect(...).to_have_text(...) but left :204. r1 pair runs at 400a8c0 gave 'loading' failures on 2 of 3 runs.",
   "why_it_matters": "The suite is the card's deliverable. A gate that passes one run and fails the next is not evidence (criterion 14), and the green result at HEAD cannot be trusted to hold on the next run.",
   "fix": "Replace the assert at test_stepper.py:204 with expect(jp.get_by_test_id('judge-summary-counts')).to_have_text(re.compile(r'\\d+ checked, \\d+ agreed with the draft, 3 questioned')). Keep :257 as it is.",
   "acceptance_test": "tests/e2e/test_stepper.py::test_judge_panel_collapsed_summary_and_labels and ::test_judge_panel_when_nothing_objected pass in 10 consecutive runs against a HEAD archive, each with a fresh ZLAYT_DB; grep shows no inner_text() read of judge-summary-counts in tests/e2e/test_stepper.py."},
  {"severity": "major",
   "title": "D-029 contradicted by the commit and not amended; recorded path in D-029 does not exist",
   "evidence": "memory/ORCHESTRATOR_DECISIONS.md:37 (D-029): 'tests/fixtures/llm/curated/ (hand-checked generator/judge responses ...)' and 'tests/fixtures/llm/recorded/'. In the HEAD archive, tests/fixtures/llm/recorded does not exist (ls: No such file); the recorded set is the top-level tests/fixtures/llm/ with 1089 files. Curated now has 19 generator and 0 judge files. make_curated.py:1-8 and tests/unit/test_curated_fixtures.py:1-9 cite D-029 for the judge rule. grep -n -i curated memory/DECISIONS.md memory/ASSUMPTIONS.md memory/ORCHESTRATOR_DECISIONS.md shows no amendment.",
   "why_it_matters": "D-029 is the binding fixture decision and CLAUDE.md non-negotiable 12 requires decisions to be recorded. The commit reverses half of what D-029 says the curated set contains, and the text a future reader sees says the opposite. A reader following the recorded path looks in a directory that does not exist.",
   "fix": "Orchestrator records a D-029 amendment in memory/ORCHESTRATOR_DECISIONS.md: judge answers are recordings only; curated holds generator and narrative answers; the recorded set is tests/fixtures/llm/. Correct the path in the D-029 row. Reviewers do not write memory/.",
   "acceptance_test": "memory/ORCHESTRATOR_DECISIONS.md has an amendment row citing 08c921e and T-115; the D-029 row names tests/fixtures/llm/ as the recorded set and contains no claim that curated holds judge responses."},
  {"severity": "major",
   "title": "Round-1 F3 still open: judge_conflict_v5 controls red and not recorded or re-run",
   "evidence": "evals/reports/controls-20261102T090925Z.md:3 reads 'controls_ok: False' (prompts judge_conflict_v5, judge_flag_v3); line 8 shows J3 13/17 caught with false agrees J3V1, J3V9, J3V13, H3V5. It is the newest controls report (ls evals/reports | grep controls: only 075238Z and 090925Z). grep in memory/ASSUMPTIONS.md and memory/DECISIONS.md finds no record of the red status.",
   "why_it_matters": "The curated set no longer scripts judges, so the e2e now depends on recorded judge_conflict_v5 answers from a judge whose live controls are red. D-046 makes J3 and J4 control sets part of ship-bar item 4. The card does not disclose this.",
   "fix": "Re-run the judge_conflict_v5 controls from a clean worktree and cite the new report, or record in memory/DECISIONS.md that v5 controls are red with the ship-bar consequence. The orchestrator owns the decision record.",
   "acceptance_test": "A controls report with controls_ok True for judge_conflict_v5 is cited in the T-115 handoff, or a DECISIONS row names the red report and its effect on ship-bar item 4."},
  {"severity": "minor",
   "title": "make_curated.py still contains a scripted verdict branch in answer()",
   "evidence": "tests/fixtures/make_curated.py:55-60: if 'verdict' in props: ... return dict(verdict=pick, reason_code='NONE'). Unreachable today because fake() at :118-119 routes any verdict schema to judge() first.",
   "why_it_matters": "The commit says make_curated no longer scripts judge answers. One routing edit re-enables scripted judge answers, and the guard test only inspects files that land in the curated dir.",
   "fix": "Delete the verdict branch from answer(); make answer() raise SystemExit for a schema with a verdict property.",
   "acceptance_test": "A unit test calls make_curated.answer() with a verdict schema and asserts SystemExit; grep for 'verdict' inside answer() returns nothing."},
  {"severity": "minor",
   "title": "08c921e carries a copied T-079 commit message; its content is T-115 only",
   "evidence": "git show -s --format='%h %s' 328428f and 08c921e: identical subject 'feat(evals): library packets lib08..lib15 with expected.json, recorded fixtures and a library report (T-079)'. 328428f is the T-079 commit (313 files, 291 tests/fixtures/llm, evals/library/*, evals/library_report.py). git show --name-status --format= 08c921e lists 49 paths, none under evals/ or any expected.json; the body's '291 claude-cli fixtures' is 328428f's count. Card note: 'swept into T-079's commit via shared index' names the wrong commit.",
   "why_it_matters": "Audit trail: git log attributes 19 judge recordings and 28 removals to T-079 and suggests the packets are in 08c921e. Nothing unrelated to T-079 or T-115 is in 08c921e's content.",
   "fix": "Do not rewrite history (destructive git is blocked). Correct the T-115 card note to say 08c921e is T-115 content under a copied T-079 message; add a LESSON that a commit message must be derived from its own diff.",
   "acceptance_test": "The T-115 card note names 08c921e as T-115 content; memory/LESSONS.md has the entry."},
  {"severity": "minor",
   "title": "Unhandled exceptions are logged by class name only, with no route or traceback",
   "evidence": "app/backend/api.py:162 and :184: log.error('unhandled %s', type(e).__name__). The e2e run logged 20 such lines (15 TypeError, 5 AttributeError) in artifacts/review-evidence/T-115-staff-engineer-r2/server_7981.log. Each returns 500 'Something went wrong.' (explicit, not a silent fallback). I did not trace which requests raised.",
   "why_it_matters": "TypeError and AttributeError are programming errors reached on some e2e flows while the suite stays green. An operator sees a class name and no path, so the 20 requests cannot be reproduced from the log (criterion 12: failures must be visible).",
   "fix": "Log the route, a request id and the traceback server-side (never in the response body). Re-run the e2e and triage each error class to a test or a product fix.",
   "acceptance_test": "A forced TypeError in a route produces a 500 with the route and traceback in the server log and no traceback in the response body; the next e2e log shows the route for each unhandled line."},
  {"severity": "minor",
   "title": "Judge re-check prompts outside the golden and library paths have no recording (pre-existing)",
   "evidence": "artifacts/review-evidence/T-115-staff-engineer-r2/server_7981.log: 26 'llm call failed ... prompt_hash=' lines, 10 distinct hashes. check_missing.py: none of the 10 is in the parent's curated or recorded set, so 08c921e did not cause them. Library replay (judge_demand.py): 244 judge replays, 0 misses, 0 curated.",
   "why_it_matters": "The demo can issue judge calls that have no recording, so those checks fail on the fixture backend. The failure is visible in the log and not silent, and it predates this commit. I did not confirm the UI outcome.",
   "fix": "Decide and record whether the cached demo needs recordings for re-checks after edits (see question_for_chris), or record the boundary in D-029.",
   "acceptance_test": "Either the 10 keys are recorded and the e2e log shows no FixtureMiss, or D-029 names the boundary and the e2e test asserts the visible failure state."}
 ],
 "whats_right": [
  "08c921e's content is T-115 only: 19 new recordings are all claude-cli judge answers, the 28 deletions are exactly the parent's 28 judge files, and the curated set keeps its 19 generator answers.",
  "The guard test fails on both a shadowed recording and a scripted judge file, and make_curated --check fails when a judge prompt changes, so the r1 staleness finding is closed.",
  "The T-117 xfail is strict and still the only xfail; the side-by-side focus fix at test_side_by_side.py:61 closes r1 F1."
 ],
 "questions_for_chris": [
  "Should the cached demo carry recordings for judge re-checks triggered by edits (F7), or is a visible failure acceptable offline?"
 ]}
```
