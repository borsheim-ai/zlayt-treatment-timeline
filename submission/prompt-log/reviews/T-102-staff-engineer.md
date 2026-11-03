# T-102 review (staff-engineer-reviewer), commit 276991b

Verdict: **fail**. 1 blocker, 3 majors, 1 minor, 2 nits. Model id is claude-haiku-5-5 (the id this session runs as). The dossier's "expected" id differs; the actual id is recorded.

Checks from the brief:
- **stale true with a reason when committed hashes differ:** yes. Through `create_app` over HTTP, a prompt edit committed in a scratch repo gives `stale: true` and "extract_v1.md changed" (artifacts/review-evidence/T-102-staff-engineer/e2e_http.txt, state 3).
- **stale false otherwise:** yes for committed state (state 1). **No** when the prompt differs on disk but is not committed: `stale: false` (state 2, same file). That is F1, the blocker.
- **calibration.json reproduces from f187a30:** yes. A clean clone detached at f187a30, regenerated with `--write-calibration --backend fixture`, equals the 276991b copy on every key except `generated_at` (regen_f187_compare.txt). The run exits 1 because the ship bar is not met on the fixture backend; the file is still written.
- **tests cover both states and fail under mutation:** both states are covered. 8 of 10 mutants of the comparison and route fail a test. The fail-closed UNCHECKED branch is unguarded (M10 survives, F4). M5 survives (F6, nit).
- **score_unsplit fixture-dir bug:** real (F3). Severity major. It does not touch the served calibration: the calibration case list is golden-only.
- **Handoff claim about the 4_no_invented_facts blocker:** not reproduced. Its stated cause, judge_unavailable, is 0 in my run (F5).

Exercised (details in the json `exercised` list and in the evidence folder): git archive and detached clone of 276991b; clean clone at f187a30 with the regeneration; `.venv/bin/python -m pytest -q tests/unit -k calibration` in the project tree (63 passed) and in the pinned clone (63 passed); the route over HTTP in three states; committed-hash probe; 10 hash-comparison mutants; unreadable-prompts probe; score_unsplit with a fixture spy; grep of app/frontend for the stale copy; reading the card AC, T-096 AC, calibration_route.py, the test file, evals/run.py, fixture.py and promptlib.py.

Evidence folder: artifacts/review-evidence/T-102-staff-engineer/ (scripts and outputs cited below).

```json
{"card": "T-102", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 276991b (app/backend/calibration_route.py, tests/unit/test_calibration_route.py, evals/reports/calibration.json); calibration.json source_commit f187a30; GET /api/calibration exercised through create_app TestClient on a scratch tree (no live app URL); calibration set = 10 golden cases on the fixture backend",
 "exercised": [
  "read personas/staff-engineer.md in full; tools/board.py show T-102 and T-096; reviewer memory notes on calibration patterns",
  "git archive 276991b into scratch T102_staff_r1/archive_276991b; git clone --no-hardlinks + checkout --detach 276991b (T102_staff_r1/clone); diff -rq against the archive equal",
  "clean clone detached at f187a30 (T102_staff_r1/clone_f187): python -m evals.run --write-calibration --backend fixture (exit 1, ship_bar_met False, calibration.json written); compared with the 276991b copy: only generated_at differs (regen_f187_compare.txt)",
  "project tree: .venv/bin/python -m pytest -q tests/unit -k calibration = 63 passed, 2405 deselected (pytest_project_tree_calibration.txt); pinned clone, same selection = 63 passed, 2368 deselected (pytest_pinned_clone_calibration.txt)",
  "read app/backend/calibration_route.py, tests/unit/test_calibration_route.py (42 tests), evals/run.py (hashes, git_source, score_unsplit, ship-bar gate at 886), app/llm/backends/fixture.py, app/llm/promptlib.py, app/backend/api.py:517",
  "GET /api/calibration via create_app TestClient in a scratch tree at 276991b, three states: committed prompts match (stale false); same prompt edited on disk, uncommitted (stale false); same edit committed (stale true, reason names extract_v1.md) (e2e_http.py, e2e_http.txt)",
  "recorded vs disk vs HEAD hash probe at 276991b, with and without an uncommitted prompt edit (probe_route.py, stale_probe_B_uncommitted.txt)",
  "10 mutants of the hash comparison and route in a scratch copy, each run against tests/unit/test_calibration_route.py (mutate.py, mutants.txt): M1-M4, M6-M9 killed; M5 and M10 survived",
  "unreadable-prompts branch: removed a prompt blob from a throwaway repo and cleared _HEAD_CACHE; route returned stale true with the UNCHECKED reason (unchecked_probe.py, unchecked_branch.txt)",
  "score_unsplit on the fixture backend with a spy on fixture.call, and the default recorded set (probe2.py, unsplit_score_fixture_misses.txt); checked that the six missing keys exist in tests/fixtures/llm/",
  "grep -rn 'older version' app/frontend = 0 hits; T-096 card AC text (line 18) has no stale line; only a note (line 29) carries it",
  "no live network, no API key, fixture backend only; no product file edited"
 ],
 "verdict": "fail",
 "scores": {"ac1_stale_semantics": 2, "provenance_reproducible": 5, "test_strength_mutants": 3, "failure_visibility": 3, "ac_closure_honesty": 2, "eval_integrity_side_path": 2, "no_live_or_wallclock_in_tests": 5},
 "findings": [
  {"severity": "blocker",
   "title": "Stale check compares against HEAD, not the prompts the pipeline loads: an uncommitted prompt edit reports stale false",
   "evidence": "app/backend/calibration_route.py:163-166 (current_prompt_hashes returns the HEAD hashes whenever a checkout exists); tests/unit/test_calibration_route.py:247-253 pins stale False for a prompt edited on disk; app/llm/promptlib.py:8,19-21 loads the prompt files from disk (lru_cache per process). Repro: artifacts/review-evidence/T-102-staff-engineer/stale_probe_B_uncommitted.txt shows recorded_vs_disk_differ ['app/llm/prompts/extract_v1.md'] with 'status ok | stale False'. e2e_http.txt state 2: same edit, HTTP 200, stale False; state 3 (same edit committed): stale True.",
   "why_it_matters": "AC 1 says stale is true 'when the recorded prompt hashes differ from the current prompts'. The running pipeline reads the working-tree prompt files, so in any checkout with an uncommitted prompt edit the served calibration is reported current while the prompts that would run differ from the ones measured. That is the silent false-current case the card exists to prevent. The deployed copy without .git falls back to disk and is correct; the gap is in development checkouts, where prompts are edited.",
   "fix": "Compare the recorded hashes with disk_prompt_hashes(root), the files the pipeline loads. If HEAD is also wanted, report uncommitted prompt changes as a separate reason instead of hiding them. If Chris rules that HEAD was the intended meaning (see questions_for_chris), amend AC 1 and record the scope cut in memory/SCOPE_CUTS.md; the severity then becomes major.",
   "acceptance_test": "On a git checkout whose recorded hashes match HEAD: edit app/llm/prompts/extract_v1.md without committing; GET /api/calibration returns stale true with a reason that names extract_v1.md changed; revert the edit; stale false. Replace test_uncommitted_prompt_edit_is_judged_at_head_not_on_disk (tests/unit/test_calibration_route.py:247-253) with this test."},
  {"severity": "major",
   "title": "AC 1 is done:true with its UI clause unbuilt, and T-096 does not carry the line in its acceptance text",
   "evidence": "board/cards/T-102.md:18 AC 1 text \"...UI (T-096) shows 'numbers from an older version'; test\" with \"done\": true. grep -rn 'older version' app/frontend returns 0 hits at 276991b. board/cards/T-096.md:18 (AC 1, done: false, status in_progress) lists the accuracy line and small-sample note but no stale line; the only mention is the note at board/cards/T-096.md:29.",
   "why_it_matters": "The user-visible half of the requirement has no acceptance criterion in its owning card. Until T-096 lands the flag is served and nothing shows it. When T-096 lands from its current AC, the accuracy sentence can be shown as current with no stale line. This is the AC-closed-with-unbuilt-clause pattern recorded in the reviewer memory for T-090.",
   "fix": "Put the stale line into T-096 acceptance text (not a note). Either set T-102 AC 1 to backend-only with the UI clause moved to T-096, or reopen T-102 AC 1 until the line exists.",
   "acceptance_test": "T-096 e2e: with a stale calibration (stale true) the page shows 'numbers from an older version' next to the accuracy sentence; with stale false it shows no such line. Grep check: the phrase appears in the frontend and in T-096 AC text."},
  {"severity": "major",
   "title": "score_unsplit fixture-dir bug is real: the unsplit_paste row passes with 6 of 7 LLM calls unreplayed",
   "evidence": "evals/run.py:451-453 sets LLM_FIXTURE_DIR to tests/fixtures/llm/split for the unsplit case; app/llm/backends/fixture.py:23 skips the default-dir fallback whenever LLM_FIXTURE_DIR is set. Repro: artifacts/review-evidence/T-102-staff-engineer/unsplit_score_fixture_misses.txt shows 'SCORE True []' with six 'MISS ... tests/fixtures/llm/split FixtureMissing' lines (three step=extract, three step=flags). All six keys exist in tests/fixtures/llm/ and not in tests/fixtures/llm/split/. The default-dir run has 10 HITs and 0 misses. Regenerated report row (clone_f187 evals/reports/20261102T090943Z.md line 23): 'unsplit_paste (LLM split, D-031) | True [] | true | R-IN-1'.",
   "why_it_matters": "Severity major, not blocker: the product path is untouched, and the served calibration is unaffected (calibration.json lists only the 10 golden cases; unsplit_paste is not among them). But the gate row cannot see missing extraction or flags, so a regression in those stages for this case would leave the row green. The row proves only the code-derived date, source and split warning. The row also feeds the 4_no_invented_facts clause (evals/run.py:886).",
   "fix": "Fix fixture.py:23 so an override dir falls back to the recorded set for keys it lacks, or give score_unsplit an explicit dir that holds every key it needs. Make the unsplit row false when its run records any FIXTURE_MISS or llm call failure.",
   "acceptance_test": "Unit test: score_unsplit with a split dir missing one extract key returns value False (or raises), not True. Second assertion: the row reports a miss count of 0 on the committed recorded set."},
  {"severity": "major",
   "title": "The fail-closed UNCHECKED branch has no test; a fail-open mutant survives all 42 tests",
   "evidence": "app/backend/calibration_route.py:217-219 (except OSError/SubprocessError -> why = UNCHECKED). Mutant M10 (why = UNCHECKED -> why = None) leaves '42 passed' (artifacts/review-evidence/T-102-staff-engineer/mutants.txt, line M10). The branch is reachable: unchecked_branch.txt shows that after deleting a prompt blob and clearing _HEAD_CACHE (calibration_route.py:38) the route returns 'ok True | The current prompts could not be read...'. Without the cache clear the second read is served from cache, so the failure is seen once per process per commit. The UNCHECKED copy is also shown with the static 'numbers from an older version' line, so the wording mismatches the reason.",
   "why_it_matters": "The card's honesty property is that an unknown state is never shown as current. The branch that enforces it is unguarded, so a change to fail-open passes CI. This is the silent-fallback pattern in the red-flag list, guarded by nothing.",
   "fix": "Add a test that makes the head read raise (monkeypatch head_prompt_hashes to raise subprocess.CalledProcessError, or remove a blob in a throwaway repo after clearing _HEAD_CACHE) and asserts stale true with stale_reason == CR.UNCHECKED. Decide whether the UI should show a different line for an unreadable check.",
   "acceptance_test": "Mutant M10 (why = UNCHECKED -> why = None) turns a test red. Repro: the mutate.py harness in artifacts/review-evidence/T-102-staff-engineer/."},
  {"severity": "minor",
   "title": "Handoff misattributes the worktree blocker 4_no_invented_facts to judge_unavailable",
   "evidence": "Handoff text: 'the worktree report's blocker 4_no_invented_facts comes from judge_unavailable'. In a clean clone at f187a30 (regen_f187_compare.txt): judge_unavailable_count 0 and judge_unavailable_in_cases 0. The blockers are 4_no_invented_facts plus 'determinism_3run and unsupported_count_3run need a live backend' and 'judge_controls: not measured'. The clause list at evals/run.py:886 requires determinism_3run and unsupported_count_3run to be 1.0 and 3-run measured, so the clause is false on the fixture backend by construction.",
   "why_it_matters": "A wrong root cause in a handoff sends the next fixer to the wrong place. On the fixture backend the 4_no_invented_facts bar cannot pass at all, which the calibration number does not show.",
   "fix": "Correct the handoff note. Qa follow-up: separate the live-only clauses from the fixture bar, or label the fixture result as not measured for that bar.",
   "acceptance_test": "A fixture ship report lists the 4_no_invented_facts reason as the not-measured live clauses and judge_controls, with judge_unavailable_count 0 shown explicitly."},
  {"severity": "nit",
   "title": "Empty recorded hashes ({}) branch is not pinned by a test",
   "evidence": "app/backend/calibration_route.py:173 'if not isinstance(recorded, dict) or not recorded:'. tests/unit/test_calibration_route.py:268-273 removes the key (None) rather than setting {}. Mutant M5 (drop 'or not recorded') survives. By code reading, not run: with recorded {} and prompts at HEAD, the mutant's reason text changes from 'does not record which prompts' to '<name> is new'.",
   "why_it_matters": "A file that records an empty hash map should be stale with the 'does not record' sentence; that sentence is what the UI would quote.",
   "fix": "Add a case with doc['hashes'] = {} next to the missing-key test.",
   "acceptance_test": "Mutant M5 turns a test red."},
  {"severity": "nit",
   "title": "Each GET runs two git subprocesses before the cache is consulted",
   "evidence": "app/backend/calibration_route.py:148 (rev-parse --show-toplevel) and :151 (rev-parse HEAD) run on every call to head_prompt_hashes; the cache at :38 is only checked after them. The comment at :38 says 'not per request'. Read, not timed.",
   "why_it_matters": "Small cost, and the comment misstates the behaviour.",
   "fix": "Cache the HEAD sha with a short TTL, or correct the comment.",
   "acceptance_test": "A test that counts subprocess calls per GET, or a corrected comment."}
 ],
 "whats_right": [
  "The committed evals/reports/calibration.json reproduces from f187a30: a clean-clone regeneration equals the 276991b copy on every key except generated_at (regen_f187_compare.txt).",
  "The comparison is per name and covers edited, added, removed and lexicon changes; 8 of 10 mutants of the comparison and route fail a test (mutants.txt).",
  "Missing and invalid states stay fail-closed: calibration is null and file contents are never echoed (tests/unit/test_calibration_route.py:89-147)."
 ],
 "questions_for_chris": [
  "AC 1 says 'current prompts'. Is that HEAD (as built and pinned at tests/unit/test_calibration_route.py:247-253) or the working-tree prompt files the pipeline loads (app/llm/promptlib.py:21)? My rating of F1 assumes the working tree."
 ]}
```
