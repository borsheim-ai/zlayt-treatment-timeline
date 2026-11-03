# T-102 round 2 review (staff-engineer-reviewer), commit 03206ca

Verdict: **changes**. 0 blockers, 1 major (r1 F2, still open), 2 minors, 2 nits. Model id is claude-haiku-5-5 (the id this session runs as).

Round-1 status, checked against 03206ca:
- F1 (blocker, stale compares HEAD, uncommitted edit reads stale false): **closed**. An uncommitted edit to app/llm/prompts/extract_v1.md gives stale true through the module and over HTTP, with the reason naming the file. Reverting it gives stale false. The same edit on the 276991b code still gives stale false, so the regression is real and fixed (artifacts/review-evidence/T-102-staff-engineer-r2/stale_probe_r2.txt, scenarios 5-7).
- F2 (major, AC 1 done:true with its UI clause unowned): **open**. T-096 acceptance text still has no stale line.
- F3 (major, score_unsplit row green with 6 of 7 calls unreplayed): **closed**. On the archive HEAD the row is value true, misses [], 10 calls replayed (1 split, 9 default, 0 MISS). A residual wrong-dir / empty-dir weakness is finding 2.
- F4 (major, UNCHECKED fail-open branch untested): **closed**. The fail-open mutant is now killed by test_an_unreadable_current_prompt_set_is_stale_with_the_unchecked_reason_never_current.
- F5 (minor, handoff misattributes 4_no_invented_facts): **closed in the handoff** (the card's handoff now names the live-only clauses). The explicit "judge_unavailable_count 0" display is finding 4.
- F6 (nit, empty-hashes branch unpinned): **closed**. Mutant killed by test_a_file_that_records_no_hashes_is_stale.
- Per-GET git subprocess nit: **closed by removal**. calibration_route.py at HEAD has no subprocess or git call.

Checks from the brief:
- **Uncommitted prompt edit reads stale true (archive HEAD copy):** the git archive copy has no .git, so it takes the disk path and reads stale true (stale_probe_r2.txt, scenario 2). An archive cannot tell HEAD from disk, so I also ran the same edit on a git clone pinned at 03206ca (scenario 5, stale true) and on the 276991b clone (scenario 7, stale false).
- **score_unsplit runs against the right dir and a test fails when the dir is wrong or empty:** yes, with the caveats in finding 2. A wrong FIXTURE_SET name fails test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir. An emptied split dir fails test_score_unsplit_on_the_real_pipeline_replays_every_call_with_no_fixture_miss. But the row stays true on the wrong name.
- **Real unsplit_paste result (archive HEAD):** value true, misses [], records 3, 10 LLM calls, 0 MISS (unsplit_row_r2.txt).
- **Brief pytest command:** project tree 152 passed, 2342 deselected (pytest_project_tree_r2.txt). Archive HEAD 149 passed, 3 skipped (pytest_archive_head_r2.txt). The 3 skips are the git-dependent tests at tests/unit/test_eval_runner.py:794 and :819 ("no git repository here (exported tree)"). The project tree count moved from 2474 to 2494 collected during this review, so the project tree is not a fixed reference; the archive HEAD run is the one to cite.

Mutation set on archive HEAD copies (mutants_r2.txt): 9 of 9 killed, including the F4 and F6 mutants that survived in round 1. Test-only failures are listed in the mutants file.

Evidence folder: artifacts/review-evidence/T-102-staff-engineer-r2/ (probe_stale.py, run_stale.sh, run_unsplit.py, mutate_r2.py, run_r2_checks.sh, capture_r2.sh and the outputs cited above).

```json
{"card": "T-102", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 03206ca (HEAD; card commits 276991b and 03206ca): app/backend/calibration_route.py, evals/run.py score_unsplit, tests/unit/test_calibration_route.py, tests/unit/test_eval_runner.py, app/llm/backends/fixture.py; served GET /api/calibration via create_app TestClient on scratch copies (no live app URL); fixture backend only; sample = calibration golden set plus unsplit_paste",
 "exercised": [
  "read personas/staff-engineer.md in full; tools/board.py show T-102 (latest commit 03206ca); reviews/T-102-staff-engineer.md (r1); T-096 card; reviewer memory project_t102_stale_calibration_patterns.md",
  "git archive HEAD (03206ca) into scratchpad T102_staff_r2/archive_HEAD (no .git); git clone --no-hardlinks pinned at 03206ca (clone_HEAD) and at 276991b (clone_276991b); diff -rq archive vs clone_HEAD identical apart from .git",
  "brief pytest in project tree: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 152 passed, 2342 deselected (pytest_project_tree_r2.txt)",
  "same pytest on archive HEAD with -rs = 149 passed, 3 skipped (no git repository, test_eval_runner.py:794, :819) (pytest_archive_head_r2.txt)",
  "stale probe, 7 scenarios through module load() and through create_app GET /api/calibration (probe_stale.py via run_stale.sh): archive clean false; archive uncommitted edit true with reason naming extract_v1.md; archive reverted false; clone_HEAD clean false; clone_HEAD uncommitted edit true; clone_HEAD reverted false; clone_276991b uncommitted edit false (old code) (stale_probe_r2.txt)",
  "score_unsplit on archive HEAD via a fixture-call spy (run_unsplit.py): value true, misses [], records 3, 10 calls = 1 split + 9 default + 0 MISS; repeated on mutant copies (unsplit_row_r2.txt)",
  "9 mutants on archive HEAD copies, each run with pytest -k 'calibration or eval_runner' (mutate_r2.py, mutants_r2.txt): wrong FIXTURE_SET name KILLED (1 test); split dir emptied KILLED (1 test); pre-fix LLM_FIXTURE_DIR KILLED (2); no empty-dir message KILLED (2); no miss recording KILLED (1); UNCHECKED fail-open KILLED (1); empty-hashes stale reason KILLED (1); route stale forced off KILLED (10)",
  "cmp and json compare of the two split-reply copies (tests/fixtures/llm/<d143a9...>.json vs tests/fixtures/llm/split/): outputs equal, recorded_at differs",
  "grep: grep -n 'older version' board/cards/T-096.md (only line 29, a Notes entry); grep -rn 'older version' app/frontend on archive HEAD (no hits); grep subprocess/git in calibration_route.py at HEAD (no hits); grep 'not measured|judge_unavailable_count' tests/unit and evals/run.py (lines 917, 920)",
  "read app/backend/calibration_route.py (203 lines), evals/run.py score_unsplit (445-503), ship-bar clause text, app/llm/backends/fixture.py, app/llm/provider.py dispatch (attribute call, so the spy intercepts), tests/unit/test_eval_runner.py 1006-1060",
  "board validate (read-only): ok (115 files) before this file was written",
  "no live network, no API key, fixture backend only; no product file edited; the probe copies and mutants live in the scratchpad"
 ],
 "verdict": "changes",
 "scores": {"ac1_stale_semantics": 5, "test_strength_mutants": 4, "failure_visibility": 5, "ac_closure_honesty": 2, "eval_integrity_side_path": 4},
 "findings": [
  {"severity": "major",
   "title": "AC 1 still closed done:true with its UI clause unowned: T-096 acceptance text has no stale line (r1 F2 open)",
   "evidence": "board/cards/T-102.md AC 1 is \"done\": true and its text says UI (T-096) shows 'numbers from an older version'. Repro: grep -n \"older version\" board/cards/T-096.md prints only line 29, a Notes entry (2026-11-02T09:07:33Z qa: ... Show the 'numbers from an older version' line when stale is true ...). The T-096 acceptance block has no such line. grep -rn \"older version\" app/frontend on the archive HEAD copy prints nothing.",
   "why_it_matters": "The user-visible half of the stale requirement has no acceptance criterion in its owning card. Until T-096 lands from its current AC, a stale calibration is served and nothing shows it. This is the AC-closed-with-unbuilt-clause pattern from r1 and from T-090 r1.",
   "fix": "Put the stale line into T-096 acceptance text (not a note). Then either reword T-102 AC 1 as backend-only, or reopen it until the line exists. The handoff's 'this AC is backend-only' does not change the AC text on the card.",
   "acceptance_test": "grep -n 'older version' board/cards/T-096.md shows a line above the Notes heading. T-102 AC 1 no longer claims a UI clause as done. Grep check on app/frontend once T-096 lands."},
  {"severity": "minor",
   "title": "score_unsplit: a wrong FIXTURE_SET name leaves the row green; the wrong-dir guard is a literal pin; an empty split dir is caught by a path check, not by a replay miss",
   "evidence": "evals/run.py:459 sets os.environ[\"FIXTURE_SET\"] = \"split\" and evals/run.py:460 checks (FX.DEFAULT_DIR / \"split\").glob(...), both hard-coded. Mutant with \"splt\" (mutants_r2.txt, F3_wrong_fixture_set_name): unsplit_row_r2.txt shows value true, misses [], 10 calls = 1 split + 9 default + 0 MISS, because the split reply also exists in tests/fixtures/llm/ (default dir). The only test that fails is test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir, which asserts the literal set == \"split\" (tests/unit/test_eval_runner.py:1059). Mutant with the split dir emptied (F3_split_dir_emptied): row value false with misses [\"the recorded split fixture dir is missing or empty\"] while all 10 calls replayed from default (default 10, MISS 0).",
   "why_it_matters": "The row is not false because of the wrong dir; it is false or true for reasons that do not match the replay. The only guard for a wrong name is a test that pins a string (checklist item 13: assert behaviour, not implementation). The residual is not a silent wrong green value: every mutant still replays all calls, so this is minor.",
   "fix": "Have the scorer record which directory served the split call (the spy already sees the key) and fail the row when that key is not served from the split dir. Derive the emptiness check from the same constant as the env value so the two cannot drift. Optionally drop the duplicate split reply (finding 3).",
   "acceptance_test": "Mutant FIXTURE_SET=\"splt\": score_unsplit returns value false or a miss naming the split key, asserted by behaviour. Mutant with split dir emptied: the miss names the split reply, not only the path check. Both red in tests/unit/test_eval_runner.py."},
  {"severity": "nit",
   "title": "The split reply is stored twice with identical output and different recorded_at",
   "evidence": "cmp tests/fixtures/llm/d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json tests/fixtures/llm/split/d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json -> differ at line 21. Parsed: outputs equal True; recorded_from.recorded_at 2026-11-02T06:47:48Z (default) and 2026-11-02T02:26:20Z (split/).",
   "why_it_matters": "Two recordings of one key make it unclear which is the provenance of the split reply. No score changes, so this is a nit.",
   "fix": "Keep one recording and say in the scorer docstring where it lives, or record why both exist.",
   "acceptance_test": "Only one file per key under tests/fixtures/llm/ (or a note in the fixture README) and the unsplit row still true."},
  {"severity": "nit",
   "title": "Judge-unavailable count is shown only when non-zero; the fixture report does not print judge_unavailable_count 0 (r1 F5 follow-up)",
   "evidence": "evals/run.py:920 is an if on m[\"hallucination_catch_rate\"].get(\"judge_unavailable_count\", 0), so the line only appears when the count is non-zero. The card handoff now says the 4_no_invented_facts blocker comes from the live-only clauses, not judge_unavailable. The live-only reason text is at evals/run.py:917 (not measured over exactly 3 live runs).",
   "why_it_matters": "The correction is in the handoff, but the report itself does not show that the judge-unavailable count is 0, which is what the r1 acceptance test asked for.",
   "fix": "Print judge_unavailable_count explicitly in the ship report, including when it is 0.",
   "acceptance_test": "Fixture ship report contains the text judge_unavailable_count 0 and lists 4_no_invented_facts with the live-only clauses as the reason."}
 ],
 "whats_right": [
  "Stale is now computed from the prompt and lexicon files on disk, which is what the app loads; an uncommitted edit is stale true with the file named, and the 276991b code gives stale false on the same edit (stale_probe_r2.txt).",
  "The fail-closed UNCHECKED branch and the empty-hashes branch are now pinned: both mutants turn tests red, and the route no longer runs git (mutants_r2.txt).",
  "score_unsplit replays all 10 LLM calls of the case with zero misses on HEAD (unsplit_row_r2.txt), so the unsplit row cannot be green on an unreplayed case."
 ],
 "questions_for_chris": [
  "Outside my lens (UX copy): when the calibration cannot be checked (UNCHECKED), should the UI show 'numbers from an older version' or a different sentence? Carried from r1; the reason and the static line disagree."
 ]}
```
