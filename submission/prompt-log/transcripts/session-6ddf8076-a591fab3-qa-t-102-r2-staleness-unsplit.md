# Subagent: QA: T-102 r2 staleness + unsplit (QA: T-102 r2 staleness + unsplit)

Source: `agent-a591fab36d58b5b76.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T09:18:19.739Z

You own board card T-102, round 2 (claimed by "qa") in /Users/arsis/zlayt-pm-project. Read reviews/T-102-staff-engineer.md.

1. **Blocker:** staleness must compare the recorded prompt hashes against the prompt files the running app actually loads, on disk, not against HEAD. An uncommitted prompt edit must read as stale. Add a test that edits a prompt file in a temp copy and expects stale: true.
2. **Major:** the score_unsplit fixture-dir bug makes that eval vacuously green. Fix it so the scorer actually runs against the right fixture dir, and add a test that fails when the fixture dir is wrong or empty. Report the real unsplit_paste result after the fix.

Run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Commit with `git add <paths>` then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-102 in_review --agent qa`. Reply in 1 line.

### User / tool · 2026-11-02T09:18:19.745Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:22.204Z

**tool call — Bash**
````
{
 "command": "cat reviews/T-102-staff-engineer.md | head -120; python3 tools/board.py show T-102 | head -60; git status --short | head -20"
}
````

### User / tool · 2026-11-02T09:18:22.395Z

**tool result**
````
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
---
id: "T-102"
title: "Calibration staleness: served calibration.json must flag when its prompt hashes no longer match HEAD (before M3 gate)"
milestone: "M3"
role: "qa"
status: "in_progress"
priority: "P2"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T05:26:30Z"
updated_at: "2026-11-02T09:18:15Z"
claimed_by: "qa"
claimed_at: "2026-11-02T09:18:15Z"
rounds: 1
commits: ["276991b1e68a4ea998332454523b5419982e682b"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "fail", "file": "reviews/T-102-staff-engineer.md", "at": "2026-11-02T09:18:15Z"}
ac:
  - {"n": 1, "text": "GET /api/calibration reports stale: true with a reason when the recorded prompt hashes differ from the current prompts; UI (T-096) shows 'numbers from an older version'; test", "done": true, "evidence": "tests/unit/test_calibration_route.py: 12 new stale/current tests (edited, added, removed, lexicon, uncommitted-not-flagged, no-git disk fallback, no recorded hashes, reason cap, route over HTTP, HEAD hashes == evals.run.hashes); file 42 passed; .venv/bin/python -m pytest -q tests/unit -k calibration = 63 passed. calibration.json regenerated from clean worktree of f187a30 and committed in 276991b1e68a4ea998332454523b5419982e682b. UI line 'numbers from an older version' is T-096's; field noted there."}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T09:01:46Z qa: claimed
- 2026-11-02T09:03:01Z qa: Plan: calibration_route computes current prompt+lexicon hashes from HEAD (git cat-file; disk fallback without a repo), reports calibration.stale + stale_reason; tests for stale (committed prompt change, new/removed file) and current; then regenerate calibration.json from a clean worktree of HEAD with --write-calibration --backend fixture; note T-096 field shape.
- 2026-11-02T09:07:33Z qa: AC 1 checked: tests/unit/test_calibration_route.py: 12 new stale/current tests (edited, added, removed, lexicon, uncommitted-not-flagged, no-git disk fallback, no recorded hashes, reason cap, route over HTTP, HEAD hashes == evals.run.hashes); file 42 passed; .venv/bin/python -m pytest -q tests/unit -k calibration = 63 passed. calibration.json regenerated from clean worktree of f187a30 and committed in 276991b1e68a4ea998332454523b5419982e682b. UI line 'numbers from an older version' is T-096's; field noted there.
- 2026-11-02T09:07:40Z qa: moved in_progress -> in_review
- 2026-11-02T09:07:53Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T09:18:15Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): fail — reviews/T-102-staff-engineer.md; round 1; findings:
    - [blocker] Stale check compares against HEAD, not the prompts the pipeline loads: an uncommitted prompt edit reports stale false — fix: Compare the recorded hashes with disk_prompt_hashes(root), the files the pipeline loads. If HEAD is also wanted, report uncommitted prompt changes as a separate reason instead of hiding them. If Chris rules that HEAD was the intended meaning (see questions_fo
    - [major] AC 1 is done:true with its UI clause unbuilt, and T-096 does not carry the line in its acceptance text — fix: Put the stale line into T-096 acceptance text (not a note). Either set T-102 AC 1 to backend-only with the UI clause moved to T-096, or reopen T-102 AC 1 until the line exists.
    - [major] score_unsplit fixture-dir bug is real: the unsplit_paste row passes with 6 of 7 LLM calls unreplayed — fix: Fix fixture.py:23 so an override dir falls back to the recorded set for keys it lacks, or give score_unsplit an explicit dir that holds every key it needs. Make the unsplit row false when its run records any FIXTURE_MISS or llm call failure.
    - [major] The fail-closed UNCHECKED branch has no test; a fail-open mutant survives all 42 tests — fix: Add a test that makes the head read raise (monkeypatch head_prompt_hashes to raise subprocess.CalledProcessError, or remove a blob in a throwaway repo after clearing _HEAD_CACHE) and asserts stale true with stale_reason == CR.UNCHECKED. Decide whether the UI should show a different line for 
    - [minor] Handoff misattributes the worktree blocker 4_no_invented_facts to judge_unavailable — fix: Correct the handoff note. Qa follow-up: separate the live-only clauses from the fixture bar, or label the fixture result as not measured for that bar.
- 2026-11-02T09:18:15Z qa: claimed

## Handoff
What changed: app/backend/calibration_route.py: calibration.stale (bool) and calibration.stale_reason (plain sentence naming new/removed/changed prompt or lexicon files, or null) compare the recorded hashes with the same files at HEAD (git cat-file; disk when no checkout). Hashes not served. tests/unit/test_calibration_route.py: 12 new stale/current tests. evals/reports/calibration.json regenerated: python -m evals.run --write-calibration --backend fixture in a clean worktree of f187a30, copied in unchanged (cmp), commit 276991b. How verified: pytest -q tests/unit/test_calibration_route.py 42 passed; pytest -q tests/unit -k calibration 63 passed; live route on HEAD: ok, stale false; the old committed file was stale (judge_flag_v3 and judge_conflict_v4/v5 new, conflicts_v1 removed). What's left: UI line on T-096 (note posted with field shape). Surprised: (1) evals/run.py score_unsplit sets LLM_FIXTURE_DIR to tests/fixtures/llm/split, and fixture.call does not fall back when it is set, so 6 other LLM calls in that case miss; the worktree report's blocker 4_no_invented_facts comes from judge_unavailable. Calibration counts are golden-case only and show no misses. Needs a qa follow-up card (evals/** is mine). (2) The trailer is Haiku 5.5 per the harness attribution, not Opus 5.5 as the brief asked. (3) The stale check reads HEAD as asked, so an uncommitted prompt edit is not flagged until committed.

 M .claude/agent-memory/backend/MEMORY.md
 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/backend/project_t110_overlap_tray.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/qa/MEMORY.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:22.727Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/memory/MEMORY.md"
}
````

### User / tool · 2026-11-02T09:18:22.742Z

**tool result (error)**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:24.437Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/qa/project_calibration_route.md; sed -n 1,260p app/backend/calibration_route.py; sed -n 1,60p app/llm/backends/fixture.py; sed -n 425,500p evals/run.py"
}
````

### User / tool · 2026-11-02T09:18:24.529Z

**tool result**
````
---
name: calibration-route-and-regen
description: How GET /api/calibration decides stale, how calibration.json is regenerated from a clean worktree, and the fixture-dir pitfall in score_unsplit
metadata:
  type: project
---

GET /api/calibration lives in app/backend/calibration_route.py (T-099, stale flag T-102). It serves evals/reports/calibration.json read-only.
`calibration.stale` / `stale_reason` compare the file's recorded `hashes` (prompts + lexicon, sha256) with the same files at HEAD
(`git cat-file blob HEAD:path`, cached per HEAD sha); a checkout-less copy falls back to disk. Hashes are never served.

**Why:** the served numbers must say when they describe older prompts (T-096 shows "numbers from an older version").
**How to apply:** when prompts change, regenerate before the gate. Do it in a clean worktree, not the shared tree:
`git worktree add <scratchpad>/<unique-name> HEAD`, then `.venv/bin/python -m evals.run --write-calibration --backend fixture` from
inside it (the committed file is refused from a dirty tree), copy the file back (`cmp` it), commit it, then `git worktree remove --force`.
Pick a unique worktree name: a `wt` folder already existed in the scratchpad (an old copy of the project with a .env) and was not touched.

Pitfalls:
- evals/run.py `score_unsplit` sets LLM_FIXTURE_DIR to tests/fixtures/llm/split for the unsplit case, and fixture.call does not fall back
  to the default dir when LLM_FIXTURE_DIR is set. The other LLM calls in that case miss (FIXTURE_MISS), judge_unavailable_count > 0, and
  the report shows blocker 4_no_invented_facts. Golden-case calibration counts are unaffected. Open follow-up for qa.
- The count changes between regenerations come from code as well as prompts (T-110 and others), so 83/84 became 84/85 at HEAD.
- git-guard rejects `git add ... && git commit ...` in one Bash call: stage in one call, commit in the next.
- `timeout` is not installed on this Mac; use the Bash tool's timeout parameter.
- The git-guard hook and `git commit -- <paths>` only commit the listed paths; the shared index often holds other workers' staged deletions.
"""GET /api/calibration (T-099): the measured calibration the review screen quotes (T-090 writes it, T-096 shows it).

Read-only. Serves evals/reports/calibration.json, which evals.run writes from the golden cases: aggregate counts, the statements built
from those counts, the source commit and the backend. It holds no record text and no case token, so it is safe in demo mode and has no gate.

Three states, always HTTP 200 with the same envelope {"status", "calibration", "message"}:
- "ok": the file is the evals.calibration/1 shape, its totals add up, and every statement quotes its own counts. `calibration` is the
  served subset (SERVED below) plus two flags (T-102):
    stale        true when the prompt or lexicon hashes recorded in the file differ from the same files at HEAD (added, removed or
                 edited since the run); the counts then describe older prompts. A file that records no hashes is stale too.
    stale_reason a plain sentence naming the files that differ, or null when `stale` is false.
  The hashes themselves are not served.
- "missing": no file. `calibration` is null. Nothing is invented.
- "invalid": the file cannot be read as a valid measurement (bad JSON, wrong schema, a hand-edited count, a statement that quotes other
  counts). `calibration` is null and the file's contents are never echoed; the reasons go to the log.
The UI hides the accuracy line when `calibration` is null (T-096) and shows "numbers from an older version" when `stale` is true.
This module reads one fixed path and the prompt files at HEAD (or on disk when there is no git checkout); it never writes.
"""
import hashlib
import json
import logging
import pathlib
import subprocess

ROOT = pathlib.Path(__file__).resolve().parents[2]
REPORT = ROOT / "evals" / "reports" / "calibration.json"
SCHEMA = "evals.calibration/1"
TYPES = ("entry", "amount", "flag")
STATES = ("verified", "needs_review")
SMALL_N = 30  # evals/run.py CAL_SMALL_N: fewer cases, or items in a state, than this is a small sample
SERVED = ("schema", "backend", "case_count", "small_sample", "source_commit", "generated_at", "by_state", "by_type", "not_scored", "sentences")
PROMPT_DIR = "app/llm/prompts"  # the same inputs evals/run.py hashes(): every prompt *.md and the lexicon
LEXICON = "app/llm/lexicon.yaml"
MISSING = "No calibration has been measured yet, so no accuracy line is shown."
INVALID = "The calibration file is not a valid measurement, so no accuracy line is shown. Regenerate it with python -m evals.run."
UNCHECKED = "The current prompts could not be read, so these numbers cannot be checked against them."
log = logging.getLogger("zlayt.calibration")
_HEAD_CACHE = {}  # (repo, HEAD sha) -> hashes at that commit; one git read per new commit, not per request


def _count(x) -> bool:
    return isinstance(x, int) and not isinstance(x, bool) and x >= 0


def _cell_ok(c) -> bool:
    return isinstance(c, dict) and _count(c.get("matched")) and _count(c.get("total")) and c["matched"] <= c["total"]


def _by_case_ok(cell) -> bool:
    """Each case's [matched, total] has matched <= total, and the cases add up to the cell's own counts."""
    bc = cell["by_case"]
    if not all(isinstance(v, list) and len(v) == 2 and _count(v[0]) and _count(v[1]) and v[0] <= v[1] for v in bc.values()):
        return False
    return sum(v[0] for v in bc.values()) == cell["matched"] and sum(v[1] for v in bc.values()) == cell["total"]


def _statement_ok(text, cell, backend, case_count) -> bool:
    """A statement is a non-empty string that names the backend. When its cell has items it must also quote that cell's own m/t and the
    case count, as calibration_sentences in evals/run.py builds them. A hand-edited number or label fails here."""
    if not isinstance(text, str) or not text or f" on the {backend} backend" not in text:
        return False
    if cell["total"] == 0:
        return True
    return f"{cell['matched']}/{cell['total']} times" in text and f"{case_count} golden cases" in text


def problems(c) -> list:
    """Why `c` is not a valid calibration document. Empty list when it is. Checks the shape, the count ranges, that the state totals add up
    to the type totals, and that each statement quotes its own counts."""
    if not isinstance(c, dict):
        return ["not an object"]
    bad = []
    if c.get("schema") != SCHEMA:
        bad.append("schema")
    if not (isinstance(c.get("backend"), str) and c["backend"]):
        bad.append("backend")
    if not _count(c.get("case_count")):
        bad.append("case_count")
    if not isinstance(c.get("small_sample"), bool):
        bad.append("small_sample")
    if not (isinstance(c.get("source_commit"), str) and c["source_commit"]):
        bad.append("source_commit")
    if not isinstance(c.get("generated_at"), str):
        bad.append("generated_at")
    ns = c.get("not_scored")
    if not (isinstance(ns, dict) and all(_count(ns.get(k)) for k in TYPES + ("total",)) and ns["total"] == sum(ns[t] for t in TYPES)):
        bad.append("not_scored")
    bs, bt, se = c.get("by_state"), c.get("by_type"), c.get("sentences")
    if not (isinstance(bs, dict) and isinstance(bt, dict) and all(isinstance(bt.get(t), dict) for t in TYPES)):
        return bad + ["by_state or by_type"]
    for s in STATES:
        if not (_cell_ok(bs.get(s)) and isinstance(bs[s].get("cases"), list) and all(isinstance(x, str) for x in bs[s]["cases"])):
            bad.append(f"by_state.{s}")
            continue
        for k in ("matched", "total"):
            if bs[s][k] != sum(bt[t][s][k] for t in TYPES if isinstance(bt[t].get(s), dict) and _cell_ok(bt[t][s])):
                bad.append(f"by_state.{s}.{k} is not the sum over by_type (hand-edited count)")
    for t in TYPES:
        for s in STATES:
            cell = (bt.get(t) or {}).get(s)
            if not (_cell_ok(cell) and isinstance(cell.get("by_case"), dict)):
                bad.append(f"by_type.{t}.{s}")
            elif not _by_case_ok(cell):
                bad.append(f"by_type.{t}.{s}.by_case does not add up to its cell")
    if bad:
        return bad
    cases = c.get("cases")
    if not (isinstance(cases, list) and all(isinstance(x, str) for x in cases) and len(cases) == c["case_count"]):
        bad.append("case_count is not the number of cases")
    if c["small_sample"] != (c["case_count"] < SMALL_N or any(bs[s]["total"] < SMALL_N for s in STATES)):
        bad.append("small_sample is not the sample-size rule")
    if not (isinstance(se, dict) and isinstance(se.get("overall"), dict) and isinstance(se.get("by_type"), dict)):
        return bad + ["sentences"]
    for s in STATES:
        if not _statement_ok(se["overall"].get(s), bs[s], c["backend"], c["case_count"]):
            bad.append(f"sentences.overall.{s} does not quote its counts")
    for t in TYPES:
        for s in STATES:
            if not _statement_ok((se["by_type"].get(t) or {}).get(s), bt[t][s], c["backend"], c["case_count"]):
                bad.append(f"sentences.by_type.{t}.{s} does not quote its counts")
    return bad


def _sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def disk_prompt_hashes(root=ROOT) -> dict:
    """The prompt and lexicon hashes read from the working tree: the set evals/run.py hashes() records. Used when there is no git checkout."""
    root = pathlib.Path(root)
    out = {}
    for p in sorted((root / PROMPT_DIR).glob("*.md")):
        out[p.relative_to(root).as_posix()] = _sha256(p.read_bytes())
    if (root / LEXICON).exists():
        out[LEXICON] = _sha256((root / LEXICON).read_bytes())
    return out


def _git(root, *args) -> bytes:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, timeout=10, check=True).stdout


def head_prompt_hashes(root=ROOT):
    """The same hashes as the prompt and lexicon files committed at HEAD of the checkout at `root`. None when `root` is not the top of a git
    checkout that has a commit (a deployed copy has no .git, and git may be absent): the caller then reads the files on disk.
    A failure reading a committed blob raises (OSError or SubprocessError); load() turns that into an unchecked state."""
    try:
        top = _git(root, "rev-parse", "--show-toplevel").decode().strip()
        if pathlib.Path(top).resolve() != pathlib.Path(root).resolve():
            return None
        head = _git(root, "rev-parse", "HEAD").decode().strip()
    except (OSError, subprocess.SubprocessError):
        return None
    key = (str(pathlib.Path(root).resolve()), head)
    if key not in _HEAD_CACHE:
        _HEAD_CACHE.clear()
        names = _git(root, "ls-tree", "--name-only", head, PROMPT_DIR + "/", LEXICON).decode().splitlines()
        wanted = [n for n in names if n == LEXICON or (n.startswith(PROMPT_DIR + "/") and n.endswith(".md") and "/" not in n[len(PROMPT_DIR) + 1:])]
        _HEAD_CACHE[key] = {n: _sha256(_git(root, "cat-file", "blob", f"{head}:{n}")) for n in sorted(wanted)}
    return dict(_HEAD_CACHE[key])


def current_prompt_hashes(root=ROOT) -> dict:
    """What the prompts are now: at HEAD when `root` is a git checkout, otherwise on disk."""
    head = head_prompt_hashes(root)
    return head if head is not None else disk_prompt_hashes(root)


def stale_reason(doc, current):
    """Why the measurement in `doc` no longer matches the prompts in `current`, or None. Compared name by name: a prompt added, removed or
    edited since the run means the counts describe other prompts. A file that records no hashes cannot be shown current."""
    recorded = doc.get("hashes")
    if not isinstance(recorded, dict) or not recorded:
        return "This measurement does not record which prompts it used, so it cannot be checked against the current prompts."
    changed = sorted(k for k in set(recorded) | set(current) if recorded.get(k) != current.get(k))
    if not changed:
        return None

    def describe(k):
        name = pathlib.PurePosixPath(k).name
        if k not in recorded:
            return f"{name} is new"
        if k not in current:
            return f"{name} was removed"
        return f"{name} changed"
    shown = "; ".join(describe(k) for k in changed[:8])
    more = f"; and {len(changed) - 8} more" if len(changed) > 8 else ""
    return f"The prompts have changed since these numbers were measured: {shown}{more}. The numbers describe an older version of the prompts."


def _envelope(status, calibration=None, message=None) -> dict:
    return {"status": status, "calibration": calibration, "message": message}


def load(path=REPORT, root=ROOT) -> dict:
    """The envelope for the file at `path`: ok with the served subset and the stale flags, missing, or invalid. Read-only; never raises.
    `root` is the checkout whose prompts the file is compared with (HEAD)."""
    p = pathlib.Path(path)
    try:
        raw = p.read_text(encoding="utf-8")
    except FileNotFoundError:
        return _envelope("missing", message=MISSING)
    except (OSError, UnicodeDecodeError):
        log.warning("calibration file could not be read: %s", p.name)
        return _envelope("invalid", message=INVALID)
    try:
        doc = json.loads(raw)
    except ValueError:
        log.warning("calibration file is not JSON: %s", p.name)
        return _envelope("invalid", message=INVALID)
    bad = problems(doc)
    if bad:
        log.warning("calibration file rejected: %s", "; ".join(bad))
        return _envelope("invalid", message=INVALID)
    try:
        why = stale_reason(doc, current_prompt_hashes(root))
    except (OSError, subprocess.SubprocessError):
        log.warning("current prompt files could not be read under %s", pathlib.Path(root).name)
        why = UNCHECKED
    served = {k: doc[k] for k in SERVED}
    served.update(stale=why is not None, stale_reason=why)
    return _envelope("ok", served)


def add_routes(app, *, path=REPORT, root=ROOT):
    @app.get("/api/calibration")
    def calibration():
        return load(path, root)
"""fixture backend: replay tests/fixtures/llm/<sha256>.json; a miss raises FixtureMiss. ADR-004. No key, no network."""
import json
import os
import pathlib
import time

from app.llm._types import FixtureMiss, LLMError, LLMResult

DEFAULT_DIR = pathlib.Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "llm"


def fixture_dir() -> pathlib.Path:
    """LLM_FIXTURE_DIR wins; else FIXTURE_SET=<name> maps to tests/fixtures/llm/<name>/ (e.g. curated); else the default dir."""
    if os.environ.get("LLM_FIXTURE_DIR"):
        return pathlib.Path(os.environ["LLM_FIXTURE_DIR"])
    name = os.environ.get("FIXTURE_SET", "").strip()
    return DEFAULT_DIR / name if name and name.isidentifier() else DEFAULT_DIR


def call(model: str, system: str, user: str, json_schema: dict, *, key: str) -> LLMResult:
    p = fixture_dir() / f"{key}.json"
    t0 = time.monotonic()
    if not p.is_file() and not os.environ.get("LLM_FIXTURE_DIR") and fixture_dir() != DEFAULT_DIR:
        p = DEFAULT_DIR / f"{key}.json"        # FIXTURE_SET (e.g. curated) first, then the recorded claude-cli set
    if not p.is_file():
        raise FixtureMiss(key)
    try:
        d = json.loads(p.read_text())
        out = d["output"]
    except (ValueError, KeyError, OSError):
        raise LLMError(f"FIXTURE_CORRUPT {key}") from None
    return LLMResult(output=out, backend="fixture", model_resolved=model, latency_ms=int((time.monotonic() - t0) * 1000),
                     raw=json.dumps(out), recorded_from=d.get("recorded_from") or {})


def write(key: str, result: LLMResult, model: str) -> pathlib.Path:
    """Record mode: store a live result keyed by the prompt hash, with provenance."""
    d = fixture_dir()
    d.mkdir(parents=True, exist_ok=True)
    p = d / f"{key}.json"
    rec = {"output": result.output,
           "recorded_from": {"backend": result.backend, "model": result.model_resolved or model,
                             "recorded_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}}
    p.write_text(json.dumps(rec, indent=1, sort_keys=True))
    return p
        nonlocal checked
        checked += 1
        if not ok:
            bad.append(label)

    for e in product_entries(out):
        chk(f"entry {e.get('id')} excerpt", norm(e.get("excerpt")) in ntext)
        first = recs.get(min((rn(r) for r in e.get("record_ids", [])), default=None))
        if first is not None:
            chk(f"entry {e.get('id')} provider", norm(e.get("provider")) == norm(first["source"]))
            if first.get("date_status") == "parsed":
                chk(f"entry {e.get('id')} date", e.get("date") == first.get("date_iso"))
    for a in out.get("amounts") or []:
        chk(f"amount {a.get('id')}", norm(a.get("text")) in ntext and norm(a.get("excerpt")) in ntext)
    for f in out.get("flags") or []:
        for ev in f.get("evidence", []):
            chk(f"flag {f.get('id')} evidence", norm(ev.get("excerpt")) in ntext)
    return {"checked": checked, "failures": bad}


def score_unsplit(pipeline, backend):
    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
    them and parses every field. Expected: 3 records with the golden date and source (from code), each carrying exactly one LLM_SPLIT record_warning.
    On the fixture backend the recorded split reply lives in tests/fixtures/llm/split."""
    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
    text = (GOLD / "unsplit_paste.txt").read_text()
    saved = os.environ.get("LLM_FIXTURE_DIR")
    if backend == "fixture":
        os.environ["LLM_FIXTURE_DIR"] = str(ROOT / "tests" / "fixtures" / "llm" / "split")
    try:
        out = pipeline.run_case(text, backend)
    finally:
        if saved is None:
            os.environ.pop("LLM_FIXTURE_DIR", None)
        else:
            os.environ["LLM_FIXTURE_DIR"] = saved
    recs = {rn(r.get("n", r.get("id"))): r for r in out.get("records") or []}
    misses = []
    if len(recs) != len(exp["records"]):
        misses.append(f"record count {len(recs)} != {len(exp['records'])}")
    warn = {}
    for f in out.get("flags") or []:
        if f.get("type") == "record_warning" and f.get("category") == "llm_split":
            for e in f.get("evidence", [])[:1]:
                warn[rn(e.get("record_id", e.get("record_no")))] = warn.get(rn(e.get("record_id", e.get("record_no"))), 0) + 1
    for g in exp["records"]:
        r = recs.get(g["record_no"])
        if r is None:
            misses.append(f"record {g['record_no']} missing")
            continue
        if r.get("date_iso") != g["date"]:
            misses.append(f"record {g['record_no']} date {r.get('date_iso')} != {g['date']}")
        if norm(r.get("source")) != norm(g["source"]):
            misses.append(f"record {g['record_no']} source differs")
        if warn.get(g["record_no"], 0) != 1:
            misses.append(f"record {g['record_no']} has {warn.get(g['record_no'], 0)} LLM_SPLIT warnings, want 1")
    return {"value": not misses, "misses": misses, "records": len(recs), "r_ids": ["R-IN-1", "R-RV-6"]}


def run_cases(pipeline, backend, cases=None, runs_dir=None):
    """Score every golden case. Returns per-case dicts plus the raw outputs for the live-only checks.
    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
    results, outs = {}, {}
    for name, text, exp in (cases or golden_cases()):
        out = pipeline.run_case(text, backend)
        unscored = {}
        outs[name] = out
        write_run_artifact(runs_dir, name, out, name)
        results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
                         "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
                         "unsupported_summaries": unsupported_summaries(out), "judge_unavailable": judge_unavailable_in(out), "grounding": grounding(text, out),
                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
    return results, outs


# ---------------------------------------------------------------- hallucinations (rung 1 code + rung 2 judge)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:30.065Z

**tool call — Bash**
````
{
 "command": "grep -n \"unsplit\\|FIXTURE_SET\\|LLM_FIXTURE_DIR\" evals/*.py tests/unit/*.py | head -40; grep -n \"def run_case\" -A30 evals/pipeline.py | head -60; ls tests/fixtures/llm/split | head; grep -n \"def test_\\|head_prompt\\|_HEAD_CACHE\\|current_prompt\" tests/unit/test_calibration_route.py | sed -n 1,120p; ls tests/unit | grep -i eval"
}
````

### User / tool · 2026-11-02T09:18:30.191Z

**tool result**
````
evals/run.py:445:def score_unsplit(pipeline, backend):
evals/run.py:446:    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
evals/run.py:449:    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
evals/run.py:450:    text = (GOLD / "unsplit_paste.txt").read_text()
evals/run.py:451:    saved = os.environ.get("LLM_FIXTURE_DIR")
evals/run.py:453:        os.environ["LLM_FIXTURE_DIR"] = str(ROOT / "tests" / "fixtures" / "llm" / "split")
evals/run.py:458:            os.environ.pop("LLM_FIXTURE_DIR", None)
evals/run.py:460:            os.environ["LLM_FIXTURE_DIR"] = saved
evals/run.py:888:                               and m["golden_must_not_hits"]["value"] == 0 and m["unsplit_paste"]["value"] is True and m["case_07_total_420"]["value"] is True
evals/run.py:933:    m["unsplit_paste"] = score_unsplit(pipeline, backend)
evals/run.py:1030:          f"| unsplit_paste (LLM split, D-031) | {m['unsplit_paste']['value']} {m['unsplit_paste']['misses']} | true | R-IN-1 |",
evals/run.py:1139:    d = env.get("LLM_FIXTURE_DIR", "").strip()
evals/run.py:1142:    if env.get("FIXTURE_SET", "").strip() == "curated" or in_curated:
evals/run.py:1143:        raise CuratedFixtures("evals.run refuses to compute ship-bar metrics on the CURATED fixture set (FIXTURE_SET=curated or LLM_FIXTURE_DIR under "
evals/run.py:1145:                              "Unset FIXTURE_SET/LLM_FIXTURE_DIR to use the recorded set, or use a live backend.")
tests/unit/test_eval_runner.py:14:UNSPLIT = (R.GOLD / "unsplit_paste.txt").read_text()
tests/unit/test_eval_runner.py:15:USPLIT = json.loads((R.GOLD / "unsplit_paste.split.json").read_text())
tests/unit/test_eval_runner.py:23:            return self.unsplit(backend)
tests/unit/test_eval_runner.py:58:    def unsplit(self, backend):
tests/unit/test_eval_runner.py:63:            self.mutate("unsplit_paste", out, self)
tests/unit/test_eval_runner.py:284:    """D-029 / T-051: with FIXTURE_SET=curated or LLM_FIXTURE_DIR under tests/fixtures/llm/curated, the full run exits 2 with a clear message and writes no report; recorded/default sets are accepted."""
tests/unit/test_eval_runner.py:285:    monkeypatch.setenv("FIXTURE_SET", "curated")
tests/unit/test_eval_runner.py:288:    monkeypatch.delenv("FIXTURE_SET")
tests/unit/test_eval_runner.py:289:    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "curated"))
tests/unit/test_eval_runner.py:291:    monkeypatch.setenv("LLM_FIXTURE_DIR", str(R.ROOT / "tests" / "fixtures" / "llm" / "recorded"))
tests/unit/test_eval_runner.py:293:    monkeypatch.delenv("LLM_FIXTURE_DIR")
tests/unit/test_eval_runner.py:294:    monkeypatch.setenv("FIXTURE_SET", "recorded")
tests/unit/test_eval_runner.py:343:def test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4():
tests/unit/test_eval_runner.py:344:    """T-057 minor / D-031: unsplit_paste is part of the scored set: 3 code-parsed records, one LLM_SPLIT record_warning each; dropping one fails bar 4."""
tests/unit/test_eval_runner.py:346:    assert ok["metrics"]["unsplit_paste"]["value"] is True and ok["ship_bar_met"] is True
tests/unit/test_eval_runner.py:348:        if n == "unsplit_paste":
tests/unit/test_eval_runner.py:351:    assert bad["metrics"]["unsplit_paste"]["value"] is False and "record 1 has 0 LLM_SPLIT warnings, want 1" in bad["metrics"]["unsplit_paste"]["misses"]
tests/unit/test_eval_runner.py:354:def test_unsplit_paste_wrong_date_or_one_record_fails():
tests/unit/test_eval_runner.py:357:        if n == "unsplit_paste":
tests/unit/test_eval_runner.py:360:    assert r["metrics"]["unsplit_paste"]["value"] is False and r["bars"]["4_no_invented_facts"] is False
tests/unit/test_eval_runner.py:362:        if n == "unsplit_paste":
tests/unit/test_eval_runner.py:364:    assert report(Perfect(mutate=bad_date))["metrics"]["unsplit_paste"]["value"] is False
tests/unit/test_export_edge.py:43:    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
tests/unit/test_export_edge.py:44:    monkeypatch.setenv("FIXTURE_SET", "curated")
tests/unit/test_export_edge.py:46:    monkeypatch.setenv("LLM_FIXTURE_DIR", "/x")
ugrep: warning: evals/pipeline.py: No such file or directory
d143a9a09567aebd99b1547f304b0b8cb572efa4905bdcdea6eab9042863934a.json
57:def test_present_file_is_served_with_source_commit_backend_and_sample_size(tmp_path):
67:def test_served_object_is_exactly_the_t096_shape_without_hashes_models_or_paths(tmp_path):
73:def test_route_serves_present_file_over_http(tmp_path):
80:def test_committed_report_is_valid_when_present():
89:def test_missing_file_is_an_empty_state_with_no_numbers(tmp_path):
94:def test_route_missing_file_returns_200_empty_state_not_an_error(tmp_path):
126:def test_invalid_file_is_an_empty_state_and_is_never_served(tmp_path, name):
142:def test_invalid_route_response_does_not_echo_file_contents(tmp_path):
150:def test_problems_is_empty_for_a_valid_document_and_lists_faults_otherwise():
157:def test_state_total_check_rejects_a_consistent_hand_edit_of_a_state_total(tmp_path):
201:def test_current_when_recorded_hashes_match_the_prompts_at_head(tmp_path):
207:def test_edited_and_committed_prompt_is_stale_and_the_reason_names_it(tmp_path):
220:def test_prompt_added_since_the_run_is_stale(tmp_path):
229:def test_prompt_removed_since_the_run_is_stale(tmp_path):
238:def test_lexicon_change_is_stale_too(tmp_path):
247:def test_uncommitted_prompt_edit_is_judged_at_head_not_on_disk(tmp_path):
256:def test_without_a_git_checkout_the_files_on_disk_are_compared(tmp_path):
268:def test_a_file_that_records_no_hashes_is_stale(tmp_path):
276:def test_stale_reason_names_at_most_eight_files_and_counts_the_rest():
284:def test_head_hashes_are_the_hashes_evals_run_records(tmp_path):
288:    assert CR.head_prompt_hashes(repo) == run_hashes(repo) == CR.disk_prompt_hashes(repo)
291:def test_head_is_not_used_when_root_is_only_inside_another_repository(tmp_path):
294:    assert CR.head_prompt_hashes(sub) is None
295:    assert CR.current_prompt_hashes(sub) == CR.disk_prompt_hashes(sub)
298:def test_route_serves_the_stale_flag_over_http(tmp_path):
321:def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
329:def test_route_carries_no_case_tokens_or_record_text(app_client):
335:def test_route_is_read_only(app_client):
test_eval_matching.py
test_eval_runner.py
test_eval_spec_check.py
test_t093_eval_signature.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:32.030Z

**tool call — Bash**
````
{
 "command": "sed -n 165,325p tests/unit/test_calibration_route.py; sed -n 1,80p tests/unit/test_eval_runner.py; grep -n \"def run_case\" -B3 -A30 evals/*.py app/*/*.py | head -70; ls tests/fixtures/llm | wc -l"
}
````

### User / tool · 2026-11-02T09:18:32.138Z

**tool result**
````
# ---- stale (T-102): the recorded prompt hashes against the prompts at HEAD. Each test builds its own throwaway git repo.

GIT = ["git", "-c", "commit.gpgsign=false", "-c", "core.hooksPath=/dev/null", "-c", "user.name=qa", "-c", "user.email=qa@example.invalid"]


def git(repo, *args):
    subprocess.run([*GIT, "-C", str(repo), *args], check=True, capture_output=True)


def make_repo(tmp_path, prompts=None):
    """A git checkout with two prompts and a lexicon, committed. Hermetic: never touches the project's own repository."""
    repo = tmp_path / "repo"
    (repo / "app" / "llm" / "prompts").mkdir(parents=True)
    for name, text in (prompts or {"extract_v1.md": "extract\n", "judge_flag_v2.md": "flag v2\n"}).items():
        (repo / "app" / "llm" / "prompts" / name).write_text(text)
    (repo / "app" / "llm" / "lexicon.yaml").write_text("terms: []\n")
    git(repo, "init", "-q")
    git(repo, "add", "app")
    git(repo, "commit", "-q", "-m", "prompts")
    return repo


def recorded_for(root):
    """A valid document whose recorded hashes are the prompts under `root`, as a run from that checkout would record them."""
    d = make()
    d["hashes"] = CR.disk_prompt_hashes(root)
    return d


def commit_all_under_app(repo, message):
    git(repo, "add", "-A", "app")
    git(repo, "commit", "-q", "-m", message)


def test_current_when_recorded_hashes_match_the_prompts_at_head(tmp_path):
    repo = make_repo(tmp_path)
    c = CR.load(write(tmp_path, recorded_for(repo)), root=repo)["calibration"]
    assert c["stale"] is False and c["stale_reason"] is None


def test_edited_and_committed_prompt_is_stale_and_the_reason_names_it(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v2.md").write_text("flag v2, tightened\n")
    commit_all_under_app(repo, "tighten flag prompt")
    out = CR.load(write(tmp_path, doc), root=repo)
    assert out["status"] == "ok"
    c = out["calibration"]
    assert c["stale"] is True
    assert c["stale_reason"] == ("The prompts have changed since these numbers were measured: judge_flag_v2.md changed. "
                                 "The numbers describe an older version of the prompts.")


def test_prompt_added_since_the_run_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v3.md").write_text("flag v3\n")
    commit_all_under_app(repo, "add flag v3")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "judge_flag_v3.md is new" in c["stale_reason"]


def test_prompt_removed_since_the_run_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    git(repo, "rm", "-q", "app/llm/prompts/extract_v1.md")
    git(repo, "commit", "-q", "-m", "retire extract v1")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "extract_v1.md was removed" in c["stale_reason"]


def test_lexicon_change_is_stale_too(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/lexicon.yaml").write_text("terms: [x]\n")
    commit_all_under_app(repo, "lexicon")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "lexicon.yaml changed" in c["stale_reason"]


def test_uncommitted_prompt_edit_is_judged_at_head_not_on_disk(tmp_path):
    """The card asks for the prompts at HEAD. A prompt edited but not committed is not yet a change HEAD has, so it does not flag here."""
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v2.md").write_text("edited, not committed\n")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is False


def test_without_a_git_checkout_the_files_on_disk_are_compared(tmp_path):
    root = tmp_path / "copy"
    (root / "app" / "llm" / "prompts").mkdir(parents=True)
    (root / "app" / "llm" / "prompts" / "extract_v1.md").write_text("extract\n")
    (root / "app" / "llm" / "lexicon.yaml").write_text("terms: []\n")
    doc = recorded_for(root)
    assert CR.load(write(tmp_path, doc), root=root)["calibration"]["stale"] is False
    (root / "app" / "llm" / "prompts" / "extract_v1.md").write_text("extract, edited on disk\n")
    c = CR.load(write(tmp_path, doc), root=root)["calibration"]
    assert c["stale"] is True and "extract_v1.md changed" in c["stale_reason"]


def test_a_file_that_records_no_hashes_is_stale(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    doc.pop("hashes")
    c = CR.load(write(tmp_path, doc), root=repo)["calibration"]
    assert c["stale"] is True and "does not record which prompts" in c["stale_reason"]


def test_stale_reason_names_at_most_eight_files_and_counts_the_rest():
    recorded = {"old.md": "00"}
    current = {f"judge_{i:02d}.md": "11" for i in range(10)}
    reason = CR.stale_reason({"hashes": recorded}, current)
    assert reason.count(" is new") == 8 and "old.md was removed" not in reason
    assert reason.endswith("; and 3 more. The numbers describe an older version of the prompts.")


def test_head_hashes_are_the_hashes_evals_run_records(tmp_path):
    """The route and the producer (evals/run.py hashes()) must agree on the same files, or every fresh file would read as stale."""
    from evals.run import hashes as run_hashes
    repo = make_repo(tmp_path)
    assert CR.head_prompt_hashes(repo) == run_hashes(repo) == CR.disk_prompt_hashes(repo)


def test_head_is_not_used_when_root_is_only_inside_another_repository(tmp_path):
    repo = make_repo(tmp_path)
    sub = repo / "app"
    assert CR.head_prompt_hashes(sub) is None
    assert CR.current_prompt_hashes(sub) == CR.disk_prompt_hashes(sub)


def test_route_serves_the_stale_flag_over_http(tmp_path):
    repo = make_repo(tmp_path)
    doc = recorded_for(repo)
    (repo / "app/llm/prompts/judge_flag_v2.md").write_text("flag v2, tightened\n")
    commit_all_under_app(repo, "tighten flag prompt")
    app = FastAPI()
    CR.add_routes(app, path=write(tmp_path, doc), root=repo)
    body = TestClient(app).get("/api/calibration").json()
    assert body["status"] == "ok" and body["calibration"]["stale"] is True
    assert "judge_flag_v2.md changed" in body["calibration"]["stale_reason"]
    assert "hashes" not in body["calibration"]


# ---- the route on the real app, demo mode, read-only

@pytest.fixture
def app_client(tmp_path, monkeypatch):
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("ENABLE_LIVE", raising=False)
    monkeypatch.delenv("ANTHROPIC_API_KEY", raising=False)
    return TestClient(create_app(str(tmp_path / "cal.sqlite"), static_dir=str(tmp_path)))


def test_route_is_on_the_real_app_and_needs_no_gate_in_demo_mode(app_client):
    r = app_client.get("/api/calibration")
    assert r.status_code == 200
    body = r.json()
    assert body["status"] in ("ok", "missing", "invalid")
"""evals.run scoring, ship bar, freshness and lexicon recall against a FAKE pipeline built from the golden answers (no model, no network).
T-038 AC1-AC7, AC9; R-CO-3, R-CO-7, R-TL-4, R-RV-6, D-026."""
import copy, json, re
import pytest
from evals import run as R
from tests.unit import _golden as G

ITEMS = R.load_jsonl(G.G / "hallucinations.jsonl")
CONTROLS = R.load_jsonl(G.G / "hallucinations_controls.jsonl")
BAD = {i["candidate_summary"] for i in ITEMS}
SAMPLE = next(t for n, t, _ in R.golden_cases() if n == "sample")
REC = re.compile(r'=== Record (\d+) ===\nDate: (.*)\nSource: (.*)\nExcerpt: "(.*)"\n')

UNSPLIT = (R.GOLD / "unsplit_paste.txt").read_text()
USPLIT = json.loads((R.GOLD / "unsplit_paste.split.json").read_text())

class Perfect:
    """Pipeline whose output is derived from the golden expected files, so every bar is met unless a test perturbs it."""
    def __init__(self, backend="claude-cli", mutate=None, flip=False):
        self.mutate, self.flip, self.sample_runs = mutate, flip, 0
    def run_case(self, text, backend):
        if text == UNSPLIT:
            return self.unsplit(backend)
        name = next(n for n, t, _ in R.golden_cases() if t == text)
        exp = G.expected(name)
        recs = {r["record_no"]: r for r in exp["records"]}
        parsed = {int(m.group(1)): m.group(4) for m in REC.finditer(text)}
        ents = []
        for e in exp["entries"]:
            terms = [t if isinstance(t, str) else t[0] for t in e.get("required_terms", [])]
            attrib = [sp["attribution_any"][0] for sp in e.get("self_report_spans", [])]
            ents.append(dict(id="e" + e["id"], record_ids=[f"r{n}" for n in e["record_nos"]], date=e["date"], date_status=e["date_status"],
                             provider=e["provider"], summary="; ".join(terms + attrib), excerpt=parsed[e["record_nos"][0]], state="verified", reasons=[],
                             ladder={"judge": {"verdict": "supported"}}))
        ams = [dict(id="a" + a["id"], record_ids=[f"r{a['record_no']}"], text=a["raw"], excerpt=a["raw"], kind=a["class"],
                    value_cents=None if a["value"] is None else round(a["value"] * 100)) for a in exp["amounts"]]
        flags = []
        for f in exp["flags"]:
            if f["level"] != "must":
                continue
            ev = [dict(record_id=f"r{e['record_no']}", excerpt=e["excerpt"]) for e in f["evidence"] if e.get("field", "excerpt") != "date"] or \
                 [dict(record_id=f"r{n}", excerpt=f"Date: {recs[n]['raw_date']}") for n in f["cite"]["all"]]
            flags.append(dict(id=f["id"], type=f["type"], evidence=ev, computed={"from": f.get("from_date"), "to": f.get("to_date"), "days": f.get("days")}, review_status="pending"))
        for w in exp.get("record_warnings", []):
            flags.append(dict(id="w" + w["id"], type="record_warning", evidence=[dict(record_id=f"r{w['record_no']}", excerpt=w["excerpt"])]))
            for e in ents:
                if f"r{w['record_no']}" in e["record_ids"]:
                    e["state"] = "needs_review"
        total = round(exp["totals"]["explicit_charges_total"] * 100)
        out = dict(records=[dict(id=f"r{n}", seq=n, source=r["source"], date_iso=r["date"], date_status="parsed" if r["date"] else "ambiguous") for n, r in recs.items()],
                   entries=ents, undated_entries=[], amounts=ams, flags=flags, tray=[], backend=backend, models={"generator": "g", "judge": "j"},
                   totals={"detected_not_a_total": {"cents": total}}, letter_text="")
        if name == "sample":
            self.sample_runs += 1
        if self.mutate:
            self.mutate(name, out, self)
        return out
    def unsplit(self, backend):
        out = dict(records=[dict(id=f"r{g['record_no']}", n=g["record_no"], date_iso=g["date"], source=g["source"], date_status="parsed") for g in USPLIT["records"]],
                   entries=[], undated_entries=[], amounts=[], tray=[], backend=backend, models={}, totals={},
                   flags=[dict(id=f"w{g['record_no']}", type="record_warning", category="llm_split", evidence=[dict(record_id=f"r{g['record_no']}", excerpt="x")]) for g in USPLIT["records"]])
        if self.mutate:
            self.mutate("unsplit_paste", out, self)
        return out
    def judge_summary(self, summary, excerpt, label, backend):
        return "unsupported" if (summary in BAD) != self.flip else "supported"

def gold_floor(rec):
    """Perfect lexicon floor: the golden must pre_existing/causation flags for this record (injected; the real one is backend's)."""
    out = []
    for name, _, exp in R.golden_cases():
        if rec.get("case") not in (None, name):
            continue
        out += [dict(type=e["type"], excerpt=e["evidence"][0]["excerpt"]) for e in exp["flags"]
                if e["type"] in ("pre_existing", "causation") and e["level"] == "must" and rec["n"] in e["cite"]["all"]]
    return out

def perfect_control(item):
    """A judge that answers every seeded J3/J4 control as the golden file expects."""
    return item["expected"], "NONE"
app/backend/api.py-347-            runs.pop(token, None)
app/backend/api.py-348-
app/backend/api.py-349-    @app.post("/api/cases/{token}/run", status_code=202)
app/backend/api.py:350:    async def run_case(token: str, request: Request):
app/backend/api.py-351-        b = await body_of(request)
app/backend/api.py-352-        c = conn()
app/backend/api.py-353-        try:
app/backend/api.py-354-            case = get_case(c, token)
app/backend/api.py-355-            if case["status"] == "running" or token in runs:
app/backend/api.py-356-                raise ApiError(409, "run_in_progress", "A run is already in progress for this case.")
app/backend/api.py-357-            if demo_mode() and digest(case["raw_text"]) not in allowed_hashes():
app/backend/api.py-358-                raise ApiError(409, "demo_mode_unsupported_input", "This demo only runs the recorded sample cases.")
app/backend/api.py-359-            if backend() == "anthropic-api" and not os.environ.get("ANTHROPIC_API_KEY") and not demo_mode():
app/backend/api.py-360-                raise ApiError(503, "llm_unavailable", "The AI service is not available.")
app/backend/api.py-361-            decided = any(r["review_status"] != "pending" for k in ("entry", "amount", "flag") for r in DB.list_items(c, token, k))
app/backend/api.py-362-            if decided and b.get("confirm_rerun") is not True:
app/backend/api.py-363-                raise ApiError(409, "needs_confirm", "Items already have decisions; confirm to run again.")
app/backend/api.py-364-            now = time.time()
app/backend/api.py-365-            DB.update_case(c, token, status="running", stage="extract", error=None, run_started_at=now, run_finished_at=None)
app/backend/api.py-366-            runs[token] = threading.Thread(target=_run_thread, args=(token, case["raw_text"]), daemon=True)
app/backend/api.py-367-            runs[token].start()
app/backend/api.py-368-            return {"token": token, "status": "running", "stage": "extract", "started_at": store.iso(now)}
app/backend/api.py-369-        finally:
app/backend/api.py-370-            c.close()
app/backend/api.py-371-
app/backend/api.py-372-    @app.post("/api/cases/{token}/rejudge")
app/backend/api.py-373-    async def rejudge_case(token: str):
app/backend/api.py-374-        """D-044: run the second check again for AI-made items whose judge never answered. Same demo-mode and ENABLE_LIVE rules as /run:
app/backend/api.py-375-        demo mode replays recorded answers only (a miss stays unavailable), live calls need ENABLE_LIVE=1. Each call is audited. The result carries the new export gate."""
app/backend/api.py-376-        from app.backend import rejudge as RJ
app/backend/api.py-377-        c = conn()
app/backend/api.py-378-        try:
app/backend/api.py-379-            case = get_case(c, token)
app/backend/api.py-380-            if case["status"] == "running" or token in runs or token in rejudging:
evals/run.py-481-    return {"value": not misses, "misses": misses, "records": len(recs), "r_ids": ["R-IN-1", "R-RV-6"]}
evals/run.py-482-
evals/run.py-483-
evals/run.py:484:def run_cases(pipeline, backend, cases=None, runs_dir=None):
evals/run.py-485-    """Score every golden case. Returns per-case dicts plus the raw outputs for the live-only checks.
evals/run.py-486-    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
evals/run.py-487-    results, outs = {}, {}
evals/run.py-488-    for name, text, exp in (cases or golden_cases()):
evals/run.py-489-        out = pipeline.run_case(text, backend)
evals/run.py-490-        unscored = {}
evals/run.py-491-        outs[name] = out
evals/run.py-492-        write_run_artifact(runs_dir, name, out, name)
evals/run.py-493-        results[name] = {"entries": score_entries(exp, out), "amounts": score_amounts(exp, out), "flags": score_flags(exp, out),
evals/run.py-494-                         "record_warning_misses": score_record_warnings(exp, out), "must_not_hits": check_must_not(exp, out),
evals/run.py-495-                         "unsupported_summaries": unsupported_summaries(out), "judge_unavailable": judge_unavailable_in(out), "grounding": grounding(text, out),
evals/run.py-496-                         "calibration": score_calibration(exp, out, unscored), "calibration_unscored": unscored}
evals/run.py-497-    return results, outs
evals/run.py-498-
evals/run.py-499-
evals/run.py-500-# ---------------------------------------------------------------- hallucinations (rung 1 code + rung 2 judge)
evals/run.py-501-def parse_record_text(rt):
evals/run.py-502-    """'Record 8 | 2026-05-29 | Austin Imaging, cervical MRI | "excerpt"' -> (label, date, excerpt)."""
evals/run.py-503-    m = re.match(r'Record \d+ \| ([^|]*) \| (.*?) \| "(.*)"\s*$', rt, re.S)
evals/run.py-504-    if not m:
evals/run.py-505-        return "", "", rt
evals/run.py-506-    return m.group(2).strip(), m.group(1).strip(), m.group(3)
evals/run.py-507-
evals/run.py-508-
evals/run.py-509-def judge_item(item, judge, check_summary):
evals/run.py-510-    label, date, excerpt = parse_record_text(item["record_text"])
evals/run.py-511-    code = list(check_summary(item["candidate_summary"], excerpt, label, date)) if check_summary else []   # a crash propagates: no silent code-rung loss
evals/run.py-512-    verdict = judge(item["candidate_summary"], excerpt, label)
evals/run.py-513-    return {"id": item["id"], "code_reasons": code, "verdict": verdict}
evals/run.py-514-
app/backend/pipeline.py-437-    return conn, cid, AU.make_call(conn, cid)
app/backend/pipeline.py-438-
    1109
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:37.103Z

**tool call — Bash**
````
{
 "command": "grep -n \"fixture\" app/llm/*.py | head -30; grep -n \"class .*Pipeline\\|def run_case\\|FIXTURE_MISS\\|FixtureMiss\" evals/*.py app/llm/*.py app/backend/*.py | head -30; sed -n 925,940p evals/run.py"
}
````

### User / tool · 2026-11-02T09:18:37.205Z

**tool result**
````
app/llm/promptlib.py:28:    """First 12 hex of sha256 over the parts (ADR-008.5: case text + step + item id). Deterministic so fixtures match."""
app/llm/_types.py:25:    backend: str = "fixture"
app/llm/audited.py:4:attempt (prompt hash = sha256 of model+system+user+schema); a fixture miss is final. Never logs prompts, responses or error text.
app/llm/audited.py:33:    """The LLM layer gave up (every attempt failed, or a fixture was missing). `last_error` is the last attempt's failure code
app/llm/audited.py:45:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:78:        res, err, fixture_miss, bug = None, None, False, None
app/llm/audited.py:87:            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
app/llm/audited.py:110:        log.warning("llm call failed call_id=%s step=%s attempt=%d%s", call_id, step, attempt, f" prompt_hash={h}" if fixture_miss else "")
app/llm/audited.py:111:        if fixture_miss:
app/llm/audited.py:134:        # a live backend that just failed (rate limit, timeout) is retried after a short pause, not at once (T-075); the fixture backend never sleeps
app/llm/audited.py:136:                            prompt_version=PROMPT_OF_STEP.get(step), sleep=None if P.backend_name() == "fixture" else time.sleep)
app/llm/provider.py:3:LLM_BACKEND = fixture (default; no key, no network) | claude-cli (dev) | anthropic-api (live).
app/llm/provider.py:5:Record mode (RECORD_FIXTURES=1 or LLM_FIXTURE_RECORD=1, live backend only) writes tests/fixtures/llm/<hash>.json and is
app/llm/provider.py:16:from app.llm.backends import fixture as _fixture
app/llm/provider.py:25:    (dev recording). Otherwise - demo mode, tests, the public build - this is ALWAYS 'fixture', whatever LLM_BACKEND or a key say
app/llm/provider.py:27:    name = os.environ.get("LLM_BACKEND", "fixture").strip() or "fixture"
app/llm/provider.py:28:    if name != "fixture" and os.environ.get("ENABLE_LIVE") != "1" and not _record_ok:
app/llm/provider.py:29:        return "fixture"
app/llm/provider.py:95:    if name == "fixture":
app/llm/provider.py:96:        res = _fixture.call(model, system, user, json_schema, key=key)
app/llm/provider.py:108:    if name != "fixture" and _recording():
app/llm/provider.py:109:        _fixture.write(key, res, model)
app/llm/record.py:3:Runs the pipeline over one golden input with a live backend; provider.py writes tests/fixtures/llm/<hash>.json for
app/llm/record.py:14:    """complete_with_meta that replays an existing fixture and goes live only on a miss (never overwrites a recorded answer)."""
app/llm/record.py:18:            res = P._fixture.call(model, system, user, json_schema, key=key)
app/llm/record.py:27:    """Return the number of fixture files present after the run. `run(conn, case_id, raw, call)` defaults to the pipeline.
app/llm/record.py:28:    fill_missing: replay recorded answers and call the live backend only for prompts with no fixture (T-085: new prompts for one record type)."""
app/llm/record.py:35:    if P.backend_name() == "fixture":
app/llm/record.py:56:    return len(list(P._fixture.fixture_dir().glob("*.json")))
app/llm/record.py:101:        if P.backend_name() == "fixture" or not P._recording():
evals/library_report.py:6:Honest failures are shown, not hidden: a record whose extract call has no recorded fixture shows as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS),
evals/library_report.py:67:    lines += ["", "History (T-079): at 328428f lib09 r2, lib10 r6 and lib15 r7 replayed as LLM_FAILED_AFTER_RETRIES (FIXTURE_MISS) because every live attempt "
evals/run.py:484:def run_cases(pipeline, backend, cases=None, runs_dir=None):
evals/run.py:621:            except P.FixtureMiss:
app/llm/audited.py:34:    (TIMEOUT, SCHEMA_INVALID, FIXTURE_MISS ...), so a caller can record why without keeping any record text."""
app/llm/audited.py:44:class LLMFailedFixtureMiss(LLMFailed, P.FixtureMissing):
app/llm/audited.py:45:    """A fixture miss, surfaced as LLM_FAILED_AFTER_RETRIES and still catchable as FixtureMiss (never a default answer)."""
app/llm/audited.py:47:    last_error = "FIXTURE_MISS"
app/llm/audited.py:50:        P.FixtureMissing.__init__(self, prompt_hash)
app/llm/audited.py:86:        except P.FixtureMissing as e:
app/llm/audited.py:87:            err, fixture_miss = f"FIXTURE_MISS {e.prompt_hash or h}", True
app/llm/audited.py:112:            raise LLMFailedFixtureMiss(h)
app/llm/_types.py:11:class FixtureMissing(LLMError):
app/llm/_types.py:15:        super().__init__(f"FIXTURE_MISS {prompt_hash}")
app/llm/_types.py:19:FixtureMiss = FixtureMissing   # old spelling, kept as an alias
app/llm/record.py:21:        except P.FixtureMiss:
app/llm/provider.py:15:from app.llm._types import FixtureMiss, FixtureMissing, LLMError, LLMResult, validate_schema  # noqa: F401  (re-exported API)
app/backend/api.py:350:    async def run_case(token: str, request: Request):
app/backend/confidence.py:11:    "FIXTURE_MISS", "DATE_AMBIGUOUS", "DATE_MISSING", "ENDPOINT_NOT_VERIFIED", "AMOUNT_RATE_NOT_TOTALED",
app/backend/confidence.py:66:    for key, code in (("fixture_miss", "FIXTURE_MISS"), ("split_ambiguous", "SPLIT_AMBIGUOUS"), ("llm_split", "LLM_SPLIT"),
app/backend/flags.py:205:    except P.FixtureMiss:
app/backend/flags.py:279:    except P.FixtureMiss:
app/backend/ingest.py:274:            if e.code == "FIXTURE_MISS":   # no recorded answer is the same user-facing state as no model; the detail stays for the run's error entry
app/backend/generator.py:54:    except P.FixtureMiss:
app/backend/generator.py:55:        return {"failure": "FIXTURE_MISS", "record_no": record["n"]}
app/backend/generator.py:141:    """A record the extract step produced NO usable output for (LLM_FAILED_AFTER_RETRIES, FIXTURE_MISS, UNSUPPORTED_LANGUAGE, SUMMARY_NOT_IN_QUOTE) as a could-not-verify tray
app/backend/generator.py:164:    tray only (R-TL-2). `failures` = [{'record_no', 'failure'}] for records with no output (LLM_FAILED_AFTER_RETRIES / FIXTURE_MISS)."""
app/backend/generator.py:185:        except P.FixtureMiss:
app/backend/judge_guard.py:5:on its way through; the class (LLMFailed, LLMError, FixtureMissing ...) is returned whichever layer swallowed the exception."""
app/backend/judges.py:102:    Returns {id: {'verdict', 'ladder', 'call_id', 'reason_code', 'fixture_miss', 'model', 'prompt_version'}}. FixtureMiss -> ladder 'unavailable' + fixture_miss True."""
    m = aggregate(results)
    items, controls = load_jsonl(GOLD / "hallucinations.jsonl"), load_jsonl(GOLD / "hallucinations_controls.jsonl")
    if check_summary is None:
        from app.backend import grounding as GR          # no fallback: a missing code rung must fail the run
        check_summary = GR.check_summary
    check = check_summary
    m["hallucination_catch_rate"] = {**hallucination_metrics(items, controls, lambda s, e, l: pipeline.judge_summary(s, e, l, backend), check), "r_ids": RIDS["hallucination_catch_rate"]}
    m["case_07_total_420"] = case_07_total(results, outs)
    m["unsplit_paste"] = score_unsplit(pipeline, backend)
    sample = next(t for n, t, _ in cases if n == "sample")
    if backend in LIVE_BACKENDS:
        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
    else:
        m["determinism_3run"] = dict(NOT_MEASURED, r_ids=RIDS["determinism_3run"])
        m["unsupported_count_3run"] = dict(NOT_MEASURED, r_ids=RIDS["unsupported_count_3run"])
    if lexicon_flags is None:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:40.801Z

**tool call — Bash**
````
{
 "command": "grep -n \"^class \\|^def .*pipeline\\|import_module\\|def real_pipeline\\|run_case\" evals/run.py | head -20; grep -rn \"def run_case\" evals app | head"
}
````

### User / tool · 2026-11-02T09:18:40.908Z

**tool result**
````
13:    app.pipeline.run_case(text: str, backend: str) -> dict          the GET /api/cases/{token} shape (memory/contracts/api.md):
421:    recs = {rn(r.get("id", r.get("seq"))): r for r in out.get("records") or []}   # run_case record keys: id, seq, n, source, date_iso, date_status
445:def score_unsplit(pipeline, backend):
455:        out = pipeline.run_case(text, backend)
484:def run_cases(pipeline, backend, cases=None, runs_dir=None):
489:        out = pipeline.run_case(text, backend)
736:def live_metrics(pipeline, backend, text, runs=3, runs_dir=None):
743:    outs = [pipeline.run_case(text, backend) for _ in range(runs)]
922:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None):
924:    results, outs = run_cases(pipeline, backend, cases, runs_dir)
1046:class CalibrationRefused(RuntimeError):
1126:def load_pipeline():
1131:class CuratedFixtures(Exception):
1173:def main(argv=None, pipeline=None):
evals/run.py:484:def run_cases(pipeline, backend, cases=None, runs_dir=None):
app/backend/api.py:350:    async def run_case(token: str, request: Request):
app/backend/pipeline.py:440:def run_case(text: str, backend: str = None) -> dict:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:50.871Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='evals/run.py'\ns=open(p).read()\nold=s[s.index('    saved = os.environ.get(\"LLM_FIXTURE_DIR\")\\n    if backend == \"fixture\":'):s.index('    recs = {rn(r.get(\"n\", r.get(\"id\"))): r for r in out.get(\"records\") or []}\\n    misses = []\\n    if len(recs) != len(exp[\"records\"])')]\nnew='''    saved = {k: os.environ.get(k) for k in (\"LLM_FIXTURE_DIR\", \"FIXTURE_SET\")}\n    misses, replay_misses, orig = [], [], None\n    if backend == \"fixture\":\n        # FIXTURE_SET=split looks in tests/fixtures/llm/split first and then in the recorded default dir. LLM_FIXTURE_DIR must NOT be set:\n        # fixture.call then skips the default-dir fallback and every other LLM call of this case (extract, flags) misses (T-102 review F3).\n        from app.llm.backends import fixture as FX\n        os.environ.pop(\"LLM_FIXTURE_DIR\", None)\n        os.environ[\"FIXTURE_SET\"] = \"split\"\n        if not any((FX.DEFAULT_DIR / \"split\").glob(\"*.json\")):\n            misses.append(\"the recorded split fixture dir is missing or empty\")\n        orig = FX.call\n\n        def spy(*a, **kw):\n            try:\n                return orig(*a, **kw)\n            except FX.FixtureMiss as e:\n                replay_misses.append(str(e))\n                raise\n        FX.call = spy\n    try:\n        out = pipeline.run_case(text, backend)\n    finally:\n        if orig is not None:\n            FX.call = orig\n        for k, v in saved.items():\n            if v is None:\n                os.environ.pop(k, None)\n            else:\n                os.environ[k] = v\n    if replay_misses:\n        misses.append(f\"{len(replay_misses)} LLM call(s) had no recorded fixture (the case was not fully replayed)\")\n'''\ns=s.replace(old,new)\ns=s.replace('''recs = {rn(r.get(\"n\", r.get(\"id\"))): r for r in out.get(\"records\") or []}\n    misses = []\n    if len(recs) != len(exp[\"records\"])''','''recs = {rn(r.get(\"n\", r.get(\"id\"))): r for r in out.get(\"records\") or []}\n    if len(recs) != len(exp[\"records\"])''')\ns=s.replace('On the fixture backend the recorded split reply lives in tests/fixtures/llm/split.\"\"\"','On the fixture backend the recorded split reply lives in tests/fixtures/llm/split and every other call replays from the default recorded dir;\\n    a missing split dir or any fixture miss makes the row false, so the row cannot be green on a case that was not replayed.\"\"\"')\nopen(p,'w').write(s)\nEOF\nsed -n 445,490p evals/run.py\n.venv/bin/python - <<'EOF'\nimport evals.run as R\np=R.load_pipeline()\nprint(R.score_unsplit(p,\"fixture\"))\nEOF"
}
````

### User / tool · 2026-11-02T09:18:51.380Z

**tool result**
````
def score_unsplit(pipeline, backend):
    """D-031 / T-057: evals/golden/unsplit_paste.{txt,split.json}. The code split sees one block; the model proposes boundaries; code validates
    them and parses every field. Expected: 3 records with the golden date and source (from code), each carrying exactly one LLM_SPLIT record_warning.
    On the fixture backend the recorded split reply lives in tests/fixtures/llm/split and every other call replays from the default recorded dir;
    a missing split dir or any fixture miss makes the row false, so the row cannot be green on a case that was not replayed."""
    exp = json.loads((GOLD / "unsplit_paste.split.json").read_text())
    text = (GOLD / "unsplit_paste.txt").read_text()
    saved = {k: os.environ.get(k) for k in ("LLM_FIXTURE_DIR", "FIXTURE_SET")}
    misses, replay_misses, orig = [], [], None
    if backend == "fixture":
        # FIXTURE_SET=split looks in tests/fixtures/llm/split first and then in the recorded default dir. LLM_FIXTURE_DIR must NOT be set:
        # fixture.call then skips the default-dir fallback and every other LLM call of this case (extract, flags) misses (T-102 review F3).
        from app.llm.backends import fixture as FX
        os.environ.pop("LLM_FIXTURE_DIR", None)
        os.environ["FIXTURE_SET"] = "split"
        if not any((FX.DEFAULT_DIR / "split").glob("*.json")):
            misses.append("the recorded split fixture dir is missing or empty")
        orig = FX.call

        def spy(*a, **kw):
            try:
                return orig(*a, **kw)
            except FX.FixtureMiss as e:
                replay_misses.append(str(e))
                raise
        FX.call = spy
    try:
        out = pipeline.run_case(text, backend)
    finally:
        if orig is not None:
            FX.call = orig
        for k, v in saved.items():
            if v is None:
                os.environ.pop(k, None)
            else:
                os.environ[k] = v
    if replay_misses:
        misses.append(f"{len(replay_misses)} LLM call(s) had no recorded fixture (the case was not fully replayed)")
    recs = {rn(r.get("n", r.get("id"))): r for r in out.get("records") or []}
    if len(recs) != len(exp["records"]):
        misses.append(f"record count {len(recs)} != {len(exp['records'])}")
    warn = {}
    for f in out.get("flags") or []:
        if f.get("type") == "record_warning" and f.get("category") == "llm_split":
            for e in f.get("evidence", [])[:1]:
                warn[rn(e.get("record_id", e.get("record_no")))] = warn.get(rn(e.get("record_id", e.get("record_no"))), 0) + 1
{'value': True, 'misses': [], 'records': 3, 'r_ids': ['R-IN-1', 'R-RV-6']}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:18:58.208Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/calibration_route.py'\ns=open(p).read()\na=s.index('def _git(root, *args)')\nb=s.index('def stale_reason(doc, current):')\ns=s[:a]+'''def current_prompt_hashes(root=ROOT) -> dict:\n    \"\"\"What the prompts are now: the files on disk under `root`, which are the files the running app loads (app/llm/promptlib.py reads them\n    from disk). Deliberately not HEAD: a prompt edited and not yet committed already changes what the pipeline runs, so it must read as stale.\"\"\"\n    return disk_prompt_hashes(root)\n\n\n'''+s[b:]\ns=s.replace('''import pathlib\nimport subprocess\n''','''import pathlib\n''')\ns=s.replace('_HEAD_CACHE = {}  # (repo, HEAD sha) -> hashes at that commit; one git read per new commit, not per request\\n','')\ns=s.replace('''    stale        true when the prompt or lexicon hashes recorded in the file differ from the same files at HEAD (added, removed or\n                 edited since the run); the counts then describe older prompts. A file that records no hashes is stale too.''','''    stale        true when the prompt or lexicon hashes recorded in the file differ from the files on disk that the running app loads\n                 (added, removed or edited since the run, committed or not); the counts then describe older prompts. A file that\n                 records no hashes is stale too, and so is a state where the current files cannot be read (never shown as current).''')\ns=s.replace('This module reads one fixed path and the prompt files at HEAD (or on disk when there is no git checkout); it never writes.','This module reads one fixed path and the prompt files on disk; it never writes.')\ns=s.replace(\"`root` is the checkout whose prompts the file is compared with (HEAD).\",\"`root` is the tree whose prompt files (on disk) the file is compared with.\")\ns=s.replace(\"except (OSError, subprocess.SubprocessError):\\n        log.warning(\\\"current\",\"except OSError:\\n        log.warning(\\\"current\")\nopen(p,'w').write(s)\nEOF\ngrep -n \"HEAD\\|git\\|subprocess\" app/backend/calibration_route.py; grep -n \"calibration_route\\|head_prompt\" -r app tests evals --include=*.py | grep -v \"^tests/unit/test_calibration_route\\|^app/backend/calibration_route\""
}
````

### User / tool · 2026-11-02T09:18:58.408Z

**tool result**
````
128:    """The prompt and lexicon hashes read from the working tree: the set evals/run.py hashes() records. Used when there is no git checkout."""
140:    from disk). Deliberately not HEAD: a prompt edited and not yet committed already changes what the pipeline runs, so it must read as stale."""
app/backend/api.py:516:    from app.backend import calibration_route
app/backend/api.py:517:    calibration_route.add_routes(app)       # T-099 read-only eval calibration counts; aggregate only, no gate (demo-safe)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:11.128Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/calibration_route.py'\ns=open(p).read()\ns=s.replace(\"read from the working tree: the set evals/run.py hashes() records. Used when there is no git checkout.\",\"read from the working tree: the set evals/run.py hashes() records. The route compares against these, not HEAD.\")\nopen(p,'w').write(s)\np='tests/unit/test_calibration_route.py'\ns=open(p).read()\ns=s.replace(\"# ---- stale (T-102): the recorded prompt hashes against the prompts at HEAD. Each test builds its own throwaway git repo.\",\"# ---- stale (T-102): the recorded prompt hashes against the prompt files on disk (the ones the app loads), committed or not. Each test builds its own throwaway tree.\")\ns=s.replace(\"test_current_when_recorded_hashes_match_the_prompts_at_head\",\"test_current_when_recorded_hashes_match_the_prompts_on_disk\")\na=s.index(\"def test_uncommitted_prompt_edit_is_judged_at_head_not_on_disk\")\nb=s.index(\"def test_without_a_git_checkout_the_files_on_disk_are_compared\")\ns=s[:a]+'''def test_uncommitted_prompt_edit_is_stale_and_reverting_it_is_current(tmp_path):\n    \"\"\"T-102 review F1: the app loads the prompt files from disk, so an edit that is not committed already changes what runs and must read stale.\"\"\"\n    repo = make_repo(tmp_path)\n    doc = recorded_for(repo)\n    path = repo / \"app/llm/prompts/judge_flag_v2.md\"\n    path.write_text(\"edited, not committed\\\\n\")\n    c = CR.load(write(tmp_path, doc), root=repo)[\"calibration\"]\n    assert c[\"stale\"] is True and \"judge_flag_v2.md changed\" in c[\"stale_reason\"]\n    path.write_text(\"flag v2\\\\n\")\n    assert CR.load(write(tmp_path, doc), root=repo)[\"calibration\"][\"stale\"] is False\n\n\ndef test_prompt_edited_in_a_temp_copy_of_the_real_prompts_is_stale(tmp_path):\n    \"\"\"The real prompt files and lexicon, copied: recorded from the copy as it is, then one real prompt is edited in the copy only.\"\"\"\n    real = CR.ROOT\n    copy = tmp_path / \"copy\"\n    shutil.copytree(real / \"app\" / \"llm\" / \"prompts\", copy / \"app\" / \"llm\" / \"prompts\")\n    shutil.copy(real / \"app\" / \"llm\" / \"lexicon.yaml\", copy / \"app\" / \"llm\" / \"lexicon.yaml\")\n    doc = recorded_for(copy)\n    assert CR.load(write(tmp_path, doc), root=copy)[\"calibration\"][\"stale\"] is False\n    target = sorted((copy / \"app\" / \"llm\" / \"prompts\").glob(\"extract_*.md\"))[0]\n    target.write_text(target.read_text() + \"\\\\nAn uncommitted edit.\\\\n\")\n    out = CR.load(write(tmp_path, doc), root=copy)\n    assert out[\"status\"] == \"ok\" and out[\"calibration\"][\"stale\"] is True\n    assert f\"{target.name} changed\" in out[\"calibration\"][\"stale_reason\"]\n\n\ndef test_route_over_http_reports_an_uncommitted_prompt_edit_as_stale(tmp_path):\n    repo = make_repo(tmp_path)\n    doc = recorded_for(repo)\n    (repo / \"app/llm/prompts/extract_v1.md\").write_text(\"extract, edited and not committed\\\\n\")\n    app = FastAPI()\n    CR.add_routes(app, path=write(tmp_path, doc), root=repo)\n    body = TestClient(app).get(\"/api/calibration\").json()\n    assert body[\"status\"] == \"ok\" and body[\"calibration\"][\"stale\"] is True\n    assert \"extract_v1.md changed\" in body[\"calibration\"][\"stale_reason\"]\n\n\ndef test_an_unreadable_current_prompt_set_is_stale_with_the_unchecked_reason_never_current(tmp_path, monkeypatch):\n    \"\"\"Fail closed: when the current prompts cannot be read the numbers are not shown as current (T-102 review F4, mutant: reason None).\"\"\"\n    repo = make_repo(tmp_path)\n    doc = recorded_for(repo)\n\n    def boom(root=None):\n        raise PermissionError(\"denied\")\n    monkeypatch.setattr(CR, \"disk_prompt_hashes\", boom)\n    out = CR.load(write(tmp_path, doc), root=repo)\n    assert out[\"status\"] == \"ok\"\n    assert out[\"calibration\"][\"stale\"] is True and out[\"calibration\"][\"stale_reason\"] == CR.UNCHECKED\n\n\n'''+s[b:]\ns=s.replace(\"def test_without_a_git_checkout_the_files_on_disk_are_compared\",\"def test_a_tree_without_git_is_compared_on_disk_too\")\na=s.index(\"def test_head_hashes_are_the_hashes_evals_run_records\")\nb=s.index(\"def test_route_serves_the_stale_flag_over_http\")\ns=s[:a]+'''def test_disk_hashes_are_the_hashes_evals_run_records(tmp_path):\n    \"\"\"The route and the producer (evals/run.py hashes()) must agree on the same files, or every fresh file would read as stale.\"\"\"\n    from evals.run import hashes as run_hashes\n    repo = make_repo(tmp_path)\n    assert CR.current_prompt_hashes(repo) == run_hashes(repo) == CR.disk_prompt_hashes(repo)\n\n\n'''+s[b:]\ns=s.replace('''    doc.pop(\"hashes\")\n    c = CR.load(write(tmp_path, doc), root=repo)[\"calibration\"]\n    assert c[\"stale\"] is True and \"does not record which prompts\" in c[\"stale_reason\"]\n''','''    doc.pop(\"hashes\")\n    c = CR.load(write(tmp_path, doc), root=repo)[\"calibration\"]\n    assert c[\"stale\"] is True and \"does not record which prompts\" in c[\"stale_reason\"]\n    doc[\"hashes\"] = {}\n    c = CR.load(write(tmp_path, doc), root=repo)[\"calibration\"]\n    assert c[\"stale\"] is True and \"does not record which prompts\" in c[\"stale_reason\"]\n''')\nopen(p,'w').write(s)\nEOF\nsed -n 1,20p tests/unit/test_calibration_route.py | grep -n import"
}
````

### User / tool · 2026-11-02T09:19:11.243Z

**tool result**
````
4:import json
5:import subprocess
7:import pytest
8:from fastapi import FastAPI
9:from fastapi.testclient import TestClient
11:from app.backend import calibration_route as CR
12:from app.backend.api import create_app
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:12.053Z

Now the eval_runner tests.

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:12.676Z

**tool call — Bash**
````
{
 "command": "sed -i 's/^import subprocess$/import shutil\\nimport subprocess/' tests/unit/test_calibration_route.py && sed -n 340,366p tests/unit/test_eval_runner.py"
}
````

### User / tool · 2026-11-02T09:19:12.768Z

**tool result (error)**
````
Exit code 1
sed: 2: "tests/unit/test_calibra ...": undefined label 'ests/unit/test_calibration_route.py'
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:14.184Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_calibration_route.py'\ns=open(p).read().replace(\"import subprocess\\n\",\"import shutil\\nimport subprocess\\n\",1)\nopen(p,'w').write(s)\nEOF\nsed -n 340,366p tests/unit/test_eval_runner.py"
}
````

### User / tool · 2026-11-02T09:19:14.293Z

**tool result**
````
    assert r["bars"]["4_no_invented_facts"] is False


def test_unsplit_paste_is_scored_and_a_missing_llm_split_warning_fails_bar_4():
    """T-057 minor / D-031: unsplit_paste is part of the scored set: 3 code-parsed records, one LLM_SPLIT record_warning each; dropping one fails bar 4."""
    ok = report()
    assert ok["metrics"]["unsplit_paste"]["value"] is True and ok["ship_bar_met"] is True
    def drop(n, o, p):
        if n == "unsplit_paste":
            o["flags"] = o["flags"][1:]
    bad = report(Perfect(mutate=drop))
    assert bad["metrics"]["unsplit_paste"]["value"] is False and "record 1 has 0 LLM_SPLIT warnings, want 1" in bad["metrics"]["unsplit_paste"]["misses"]
    assert bad["bars"]["4_no_invented_facts"] is False

def test_unsplit_paste_wrong_date_or_one_record_fails():
    """D-031 M1/M2: a wrong code-parsed date, or boundaries rejected (one record), is a miss."""
    def one(n, o, p):
        if n == "unsplit_paste":
            o["records"] = o["records"][:1]
    r = report(Perfect(mutate=one))
    assert r["metrics"]["unsplit_paste"]["value"] is False and r["bars"]["4_no_invented_facts"] is False
    def bad_date(n, o, p):
        if n == "unsplit_paste":
            o["records"][1]["date_iso"] = "2026-05-12"
    assert report(Perfect(mutate=bad_date))["metrics"]["unsplit_paste"]["value"] is False
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:22.715Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_eval_runner.py <<'EOF'\n\n\n# ---- score_unsplit replays the whole case (T-102 review F3): the row cannot be green while LLM calls go unreplayed\n\ndef test_score_unsplit_on_the_real_pipeline_replays_every_call_with_no_fixture_miss():\n    from app.llm.backends import fixture as FX\n    seen = []\n    orig = FX.call\n    def spy(*a, **kw):\n        seen.append(kw.get(\"key\"))\n        return orig(*a, **kw)\n    FX.call = spy\n    try:\n        r = R.score_unsplit(R.load_pipeline(), \"fixture\")\n    finally:\n        FX.call = orig\n    assert r[\"value\"] is True and r[\"misses\"] == [] and r[\"records\"] == 3\n    assert len(seen) >= 7, \"extract, flags and split calls must all be replayed, not just the split reply\"\n\n\ndef test_score_unsplit_is_false_when_the_fixture_dir_is_wrong_or_empty(tmp_path, monkeypatch):\n    from app.llm.backends import fixture as FX\n    empty = tmp_path / \"empty\"\n    empty.mkdir()\n    monkeypatch.setattr(FX, \"DEFAULT_DIR\", empty)\n    r = R.score_unsplit(R.load_pipeline(), \"fixture\")\n    assert r[\"value\"] is False\n    assert any(\"split fixture dir is missing or empty\" in m for m in r[\"misses\"])\n    assert any(\"no recorded fixture\" in m for m in r[\"misses\"])\n\n\ndef test_score_unsplit_is_false_when_only_the_split_reply_is_missing(tmp_path, monkeypatch):\n    \"\"\"The default recorded set is present but tests/fixtures/llm/split is not: the split call misses, so the row is false.\"\"\"\n    from app.llm.backends import fixture as FX\n    d = tmp_path / \"llm\"\n    d.mkdir()\n    for p in FX.DEFAULT_DIR.glob(\"*.json\"):\n        (d / p.name).symlink_to(p)\n    monkeypatch.setattr(FX, \"DEFAULT_DIR\", d)\n    r = R.score_unsplit(R.load_pipeline(), \"fixture\")\n    assert r[\"value\"] is False and any(\"split fixture dir is missing or empty\" in m for m in r[\"misses\"])\n\n\ndef test_score_unsplit_restores_the_fixture_env_and_never_sets_llm_fixture_dir(monkeypatch):\n    \"\"\"LLM_FIXTURE_DIR disables the default-dir fallback in fixture.call, so the scorer must not set it while the case runs.\"\"\"\n    monkeypatch.delenv(\"LLM_FIXTURE_DIR\", raising=False)\n    monkeypatch.setenv(\"FIXTURE_SET\", \"recorded\")\n    seen = {}\n    class Spy(Perfect):\n        def run_case(self, text, backend):\n            import os\n            seen.update(dir=os.environ.get(\"LLM_FIXTURE_DIR\"), set=os.environ.get(\"FIXTURE_SET\"))\n            return super().run_case(text, backend)\n    R.score_unsplit(Spy(), \"fixture\")\n    import os\n    assert seen == {\"dir\": None, \"set\": \"split\"}\n    assert os.environ.get(\"FIXTURE_SET\") == \"recorded\" and \"LLM_FIXTURE_DIR\" not in os.environ\nEOF\n.venv/bin/python -m pytest -q tests/unit -k \"calibration or eval_runner\" 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T09:19:34.594Z

**tool result**
````
........................................................................ [ 47%]
........................................................................ [ 94%]
........                                                                 [100%]
152 passed, 2322 deselected in 11.47s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:38.146Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nfrom app.backend import calibration_route as C\nc=C.load()['calibration']; print(c['stale'], c['stale_reason'])\"; git status --short app/backend/calibration_route.py tests/unit/test_calibration_route.py tests/unit/test_eval_runner.py evals/run.py"
}
````

### User / tool · 2026-11-02T09:19:38.286Z

**tool result**
````
False None
 M app/backend/calibration_route.py
 M evals/run.py
 M tests/unit/test_calibration_route.py
 M tests/unit/test_eval_runner.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:39.848Z

**tool call — Bash**
````
{
 "command": "git add app/backend/calibration_route.py evals/run.py tests/unit/test_calibration_route.py tests/unit/test_eval_runner.py"
}
````

### User / tool · 2026-11-02T09:19:39.954Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:42.491Z

**tool call — Bash**
````
{
 "command": "git commit -q -m \"fix(qa): calibration staleness compares on-disk prompts; score_unsplit replays the whole case\n\nStale now compares recorded hashes with the prompt files the app loads (disk), so an uncommitted edit reads stale. score_unsplit uses FIXTURE_SET=split (default-dir fallback kept), is false on any fixture miss or empty split dir. Adds tests incl. the unchecked fail-closed branch and empty recorded hashes.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/calibration_route.py evals/run.py tests/unit/test_calibration_route.py tests/unit/test_eval_runner.py && git rev-parse HEAD"
}
````

### User / tool · 2026-11-02T09:19:43.093Z

**tool result**
````
check_secrets: ok (4 file(s) scanned staged)
03206ca8c3bb8809b09204f513ae0e2080916183
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:49.863Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; SHA=03206ca8c3bb8809b09204f513ae0e2080916183\n$B commit T-102 --sha $SHA --agent qa\n$B ac T-102 --check 1 --agent qa --evidence \"tests/unit/test_calibration_route.py::test_uncommitted_prompt_edit_is_stale_and_reverting_it_is_current, ::test_prompt_edited_in_a_temp_copy_of_the_real_prompts_is_stale, ::test_route_over_http_reports_an_uncommitted_prompt_edit_as_stale (compare against disk, not HEAD); ::test_an_unreadable_current_prompt_set_is_stale_with_the_unchecked_reason_never_current (F4); empty-hashes case (F6). pytest -k 'calibration or eval_runner' = 152 passed. Backend clause only: the 'older version' UI line is a T-096 AC (orchestrator to carry it there per F2). Commit $SHA\"\n$B handoff T-102 --agent qa --text \"What changed: calibration_route.current_prompt_hashes now = disk_prompt_hashes (the files promptlib loads); HEAD/git code removed, so an uncommitted prompt edit is stale:true with the file named. evals/run.py score_unsplit uses FIXTURE_SET=split (default-dir fallback kept, LLM_FIXTURE_DIR never set), spies fixture.call, and the row is false on an empty/missing split dir or any fixture miss. How verified: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' = 152 passed (new: uncommitted edit stale + revert current, temp copy of real prompts, HTTP route, unchecked fail-closed, empty hashes {}, score_unsplit real pipeline 0 misses with >=7 replayed calls, wrong/empty fixture dir false, env restored). Real unsplit_paste after fix: value True, misses [], 3 records, all calls replayed (was True with 6 of 7 calls unreplayed). calibration.json unchanged and not stale (prompt hashes unchanged). What's left: F2 (UI stale line belongs in T-096 AC text; this AC is backend-only), F5 correction: the 4_no_invented_facts blocker on the fixture backend is the live-only clauses (determinism_3run, unsupported_count_3run, judge_controls not measured), not judge_unavailable (0); separating those clauses is a follow-up. Surprised: fixture.call already falls back to the default dir under FIXTURE_SET, so no backend change was needed. Commit $SHA\"\n$B move T-102 in_review --agent qa"
}
````

### User / tool · 2026-11-02T09:19:50.190Z

**tool result**
````
T-102: commit 03206ca8c3bb8809b09204f513ae0e2080916183 recorded
AC 1 checked: tests/unit/test_calibration_route.py::test_uncommitted_prompt_edit_is_stale_and_reverting_it_is_current, ::test_prompt_edited_in_a_temp_copy_of_the_real_prompts_is_stale, ::test_route_over_http_reports_an_uncommitted_prompt_edit_as_stale (compare against disk, not HEAD); ::test_an_unreadable_current_prompt_set_is_stale_with_the_unchecked_reason_never_current (F4); empty-hashes case (F6). pytest -k 'calibration or eval_runner' = 152 passed. Backend clause only: the 'older version' UI line is a T-096 AC (orchestrator to carry it there per F2). Commit 03206ca8c3bb8809b09204f513ae0e2080916183
handoff written on T-102
T-102: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T09:19:53.397Z

T-102 round 2 is in review (commit 03206ca): staleness now compares the recorded hashes with the prompt files on disk, so an uncommitted prompt edit reads `stale: true`. The test run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` gives 152 passed.

- **`score_unsplit`:** it no longer sets `LLM_FIXTURE_DIR`, which disabled the default-dir fallback. It now uses `FIXTURE_SET=split`, and the row is false on an empty or missing split dir or any fixture miss. The real `unsplit_paste` result after the fix is `value: True`, no misses, 3 records, with every LLM call replayed. Before, it was True with 6 of 7 calls unreplayed.
- **Tests added:** an uncommitted prompt edit in a temp copy, and wrong or empty fixture dirs. I also covered the unchecked branch and the `hashes: {}` case from the review.
- **For you (F2):** the "numbers from an older version" UI clause is not in T-096's acceptance text, so AC 1 here is backend-only. I did not touch T-096.

I also corrected the F5 misattribution in the handoff.
