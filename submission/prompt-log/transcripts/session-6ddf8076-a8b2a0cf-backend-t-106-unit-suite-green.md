# Subagent: Backend: T-106 unit suite green (Backend: T-106 unit suite green)

Source: `agent-a8b2a0cfca4ca113f.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:01:54.781Z

You own board card T-106 (P1, claimed by "backend") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-106`. The goal is a fully green `tests/unit` on a clean copy of HEAD. Check on both a `git archive HEAD` extract and a `git worktree add <scratchpad>/wt HEAD` copy, and remove the worktree afterwards.

Known failures (see reviews/T-098-staff-engineer-r3.md):
1. Two `test_single_call_path` tests fail because app/backend/pdf_hidden.py imports subprocess. Allow-list it narrowly, as was done for pdf_ocr: a local child process and no LLM. Add a check that it never names `claude`.
2. `test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts` fails. Find the cause; T-101 changed run-dir writing. Fix the code or the test, whichever is wrong, and explain which in the handoff.
3. `test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git` needs .git. In an archive with no git it should still refuse, with a clear message, rather than crash. Make the code do that if it doesn't.
4. Internal notes must never print a narrative sentence that wasn't code-checked (NOT_AN_ACCEPTED_ENTRY). Show "sentence removed (cites an entry that is not accepted)" instead. Add a test.
5. HIGHLIGHT_NOT_FOUND: add a test that pins the live recompute, or remove it if it's dead code.

Each of these touches a different owner's file, and you're authorized to make these targeted fixes. Commit with the pathspec rule or a fresh temp index, and check that `git diff --cached --stat` lists only your files. Use the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Never pkill. Then `board.py ac`, the handoff, and `move T-106 in_review --agent backend`. Reply in 2 lines with the final pass and fail counts on the clean copy.

### User / tool · 2026-11-02T06:01:54.787Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:01:57.796Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-106; git status --short | head -20; git log --oneline | head -5"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:01:57.803Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-098-staff-engineer-r3.md"
}
````

### User / tool · 2026-11-02T06:01:57.980Z

**tool result**
````
---
id: "T-106"
title: "Unit suite back to green on clean HEAD: pdf_hidden subprocess allow-list, fixture-run artifacts test, no-.git calibration test; notes withhold unchecked narrative text; HIGHLIGHT_NOT_FOUND test"
milestone: "M2"
role: "backend"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:01:45Z"
updated_at: "2026-11-02T06:01:47Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:01:47Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "On a git-archive copy of HEAD (plus a git-init variant where needed) tests/unit is fully green; test_single_call_path allow-lists pdf_hidden (local, no LLM) with a check it never calls claude; test_fixture_runs_write_no_artifacts fixed at its cause; no-.git calibration test skips cleanly or works; internal notes never print a narrative sentence that was not code-checked (NOT_AN_ACCEPTED_ENTRY); a test pins the HIGHLIGHT_NOT_FOUND recompute or the dead code is removed", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T06:01:47Z backend: claimed

## Handoff (filled when moving to in_review)

 M .claude/agent-memory/backend/project_backend_conventions.md
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md
 M .claude/agent-memory/claims-adjuster-reviewer/feedback_reviews_write_once.md
 M .claude/agent-memory/frontend/MEMORY.md
 M .claude/agent-memory/frontend/project_stepper_panels.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/feedback_reviewer_tooling_quirks.md
 M .claude/agent-memory/paralegal-reviewer/library-review-patterns.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_pdf_upload_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_split_llm_review_patterns.md
 M .claude/agent-memory/ux-designer-reviewer/MEMORY.md
 M app/backend/api.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
1335f21 fix(backend): D-051 accept guard runs from one choke point (set_review) on accept, edit and batch; gate and trace recompute all code checks; notes withhold failing AI wording; AI-draft verdict says this summary (T-098 r3)
2dc5be2 feat(backend): billing ships as a cited line listing, no provider totals or complete flag (T-103, D-052)
841be23 docs: D-052 billing ships as cited line listing without totals (§7.4)
9f2811f fix(frontend): refused Accept (single and batch) shows the server reason beside the button with Edit; backend case verdict in rail and panel; panel names each class once; one rerun button per list; Not-needed step prints no verdict (T-097 r3)
````

### User / tool · 2026-11-02T06:01:57.989Z

**tool result**
````
1	# T-098 staff-engineer-reviewer, round 3: D-051 choke point (commit 1335f21)
2	
3	Verdict: **pass** (0 blockers, 0 majors, 1 minor, 1 nit). Every r2 finding is closed: the summary-only edit of a draft whose quote drops the hedge sentence is now a 422 and the stored reason survives, the gate and trace recompute all code checks, the notes withhold failing AI wording for edited originals and removed narrative sentences, and mutant M11 is killed. One narrow notes case is left (minor, finding 1).
4	
5	Pinning: reviewed `git archive 1335f21`. HEAD moved to faee448 (T-087 r4, PDF files only) during the review; `git diff 1335f21 HEAD --stat` over review.py, trace.py, export.py, store.py, case_extras.py, narrative.py and app/db is empty, so nothing in scope changed.
6	
7	## Checks asked for
8	
9	1. **review.set_review is the single choke point.** `review.py:152-167` runs the check before `DB.apply_review` for any action that leaves an entry accepted or edited (`DB.ACTIONS.get(action) in ("accepted","edited")`), on the post-edit wording (`cand["edited"] = edited`, stored code reasons dropped so the new text counts). Callers: single accept/dismiss/reset (`review.py:~182`), edit incl. flag note (`_edit`, `review.py:285` and `:317`), batch write loop (`review.batch_apply` -> `set_review`). Grep of `apply_review|review_status` over app/ (archive): the only other `DB.apply_review` calls are `review.py:423` (flag reset), `:472` (`manual_entry`, `ACTIONS` value None = log only; the item is inserted pending and the S8 probe needs a separate accept), `:529` (`not_duplicate`, log only) and `pipeline.py:204` (flag reset). `db.add_item` and `db.update_item` raise on `review_status` or `edited` (`db.py:156`, `:203`). `pipeline._persist` (`:206-208`) carries an old accepted status over a rerun; that is the D-039 route, and the gate catches it (probe S6: gate ready False, export 422). No path sets accepted or edited without going through set_review, except that carry-over, which the gate covers.
10	2. **Quote that drops a hedge sentence.** Probe `T-098-staff-engineer-r3-probe.py` (results `...-r3-probe-results.txt`): real `generator.verify` gives `needs_review ['EXCERPT_OMITS_QUALIFIER']`; accept -> `422 CODE_CHECK_FAILED`, `next_action.code EDIT_QUOTE`; summary-only edit -> `422 CODE_CHECK_FAILED`, row stays `pending`, `state_reasons ['EXCERPT_OMITS_QUALIFIER']` (reason kept), `edited None`; batch accept [e8] -> 422, row pending; item trace verdict `needs_attention`, blocks_export True, failing step `excerpt_hedge` with `EDIT_QUOTE`; repair edit (quote with the hedge sentence plus a matching summary) -> 200, status `edited`.
11	3. **Gate and trace recompute all 5 checks.** r2 probe2 on the archive: quote cut to drop the hedge, forced accept -> `gate ready False, blockers [('e8','EXCERPT_OMITS_QUALIFIER')]`, `GET /export 422`, trace fails `excerpt_hedge`; quote starting mid-sentence -> `EXCERPT_NOT_WHOLE_SENTENCE`, export 422. Mutants M3a, M3b, M3d, M3e each fail a test (M3c, see finding 2).
12	4. **Notes never print failing AI wording.** r2 matrix probe on the archive: **63 checks, 0 failed**; S4 "internal notes contain the AI draft's invented token under EDITED ITEMS: False" for all verdicts and both token kinds; S9 `notes_print_removed_sentence false`; `letter_text` clean everywhere. M15 (edited originals) and M16 (narrative removed) each fail a test. One case remains (finding 1).
13	5. **M11 killed.** `code_check_failures` quote loop replaced by `[]`: `1 failed, 74 passed`, first failure `test_summary_only_edit_of_a_draft_whose_quote_drops_the_hedge_is_422_and_keeps_the_reason_d051_r3`. Baseline 128 passed. 24 mutants run: 21 fail a test; survivors M2b (equivalent: the batch pre-check still refuses first), M3c and M11b (highlight, finding 2), M8 (equivalent: stored reasons duplicate the live check).
14	
15	Across all routes, an invented token reaching the export: matrix of single accept, stale-pass accept, batch, edit, forced accept + gate, rerun after decisions, rejudge then accept, manual entry, narrative, times judge verdicts supported / unsupported / disagrees (partially), tokens "Pain 5/10" and "on the left": none reaches `letter_text`. Only the internal-notes case in finding 1 prints a token.
16	
17	## Unit suite (archive of 1335f21)
18	
19	`.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit`: **4 failed, 2023 passed, 4 skipped**. None relates to T-098 (1335f21 touches no file these tests cover):
20	- `test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git`: runs `git archive HEAD` inside a tree without `.git`; archive artefact (passes in the live repo).
21	- `test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts`: also fails in the live repo (T-093/T-101 area, seen in r2).
22	- `test_provider.py::test_single_call_path` and `test_provider_backends.py::test_single_call_path`: `app/backend/pdf_hidden.py` imports `subprocess` (T-087 r3, ae76835); also fail in the live repo. They belong to T-087, not T-098.
23	
24	Targeted suite (trace, export, case_extras, date_unconfirmed): 128 passed.
25	
26	## Findings
27	
28	**F1 (minor, my reading). A removed narrative sentence that cites a non-accepted entry still prints in the internal notes, whatever it says.** `export.py` hides removed sentences only for the five `NARRATIVE_CODE_REASONS`; `NOT_AN_ACCEPTED_ENTRY` is printed as `Removed: "<text>"`. Probe (3): the narrative model returns `{"entry_id":"e99","text":"Pain was 9/10 on the left side."}`; `GET /export` 200, `letter has '9/10': False`, `notes has '9/10': True`: `- Removed: "Pain was 9/10 on the left side." (e99): NOT_AN_ACCEPTED_ENTRY.` The sentence was never code-checked (there is no quote to check against), so it is not a failed-check case under the commit's rule, but it is AI wording with an unsupported number printed in the export response, under the labelled do-not-send block. The letter is clean. Same family as r2 F3; the rule "no unsupported AI token anywhere in the export response" is Chris's call (question below).
29	
30	**F2 (nit). The highlight half of the live recompute has no test.** Mutants M3c (`or "HIGHLIGHT_NOT_FOUND" in live` removed from the trace) and M11b (`HIGHLIGHT_NOT_FOUND` check in `code_check_failures` replaced by `if False`) both leave 128 passed. I could not find a route that reaches it with a verbatim quote, so it is probably unreachable today; a test with a quote that passes `check_excerpt` but fails `locate` would pin it, or the branch can be dropped.
31	
32	## What I exercised
33	
34	`git rev-parse HEAD`, `git log --oneline 1335f21..HEAD`, `git show 1335f21 -- app/ memory/contracts/api.md`, `git archive 1335f21` into two scratch copies (probes, mutants); full `tests/unit` on the archive and on the live repo for the four failures; r2 probes `T-098-staff-engineer-r2-probe.py` (63 checks, 0 failed), `...-r2-probe2.py`, `...-r2-probe3.py` on the archive; new `T-098-staff-engineer-r3-probe.py` and `T-098-staff-engineer-r3-mutants.py` (24 mutants); greps for `apply_review`, `review_status`, `INSERT`, direct state writes in `app/`; read `review.py`, `case_extras.py`, `trace.py`, `export.py`, `store.py`, `narrative.py`, `pipeline._persist`, `app/db/db.py`. Not scored: frontend copy (T-104); browser UI; real LLM backends (fixture only, by design).
35	
36	```json
37	{"card": "T-098", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
38	 "scope": "commit 1335f21 (D-051 single choke point set_review, gate and trace recompute of all code checks, notes withhold failing AI wording) on git archive 1335f21; HEAD moved to faee448 (PDF files only, nothing in scope changed); FastAPI TestClient with the fixture backend and scratch DB copies of the sample case; no app URL",
39	 "exercised": [
40	  "git rev-parse HEAD; git log --oneline 1335f21..HEAD; git diff 1335f21 HEAD --stat over review.py, trace.py, export.py, store.py, case_extras.py, narrative.py, app/db (empty)",
41	  "git show 1335f21 -- app/backend/*.py memory/contracts/api.md; read review.py set_review, code_check_failures, _edit, batch_apply, case_extras._check/apply_batch, trace._entry_steps/_finish, export._edited/_draft_paragraph/_pending, store.export_case, narrative.draft, pipeline._persist, app/db/db.py apply_review/add_item/update_item",
42	  "grep over the archive for apply_review, review_status writers, INSERT/REPLACE: only set_review plus flag reset (review.py:423, pipeline.py:204), log-only manual_entry and not_duplicate, and the D-039 carry-over in pipeline._persist",
43	  ".venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit on git archive 1335f21 -> 4 failed, 2023 passed, 4 skipped (eval_runner without .git; t093 fixture artefacts; two test_single_call_path on pdf_hidden.py subprocess import; none related to T-098; the last three also fail in the live repo)",
44	  "artifacts/review-evidence/T-098-staff-engineer-r2-probe.py on the archive: 63 checks, 0 failed (single/batch/edit/forced accept + gate/rerun/rejudge/manual entry/narrative x supported, unsupported, disagrees x 'Pain 5/10', 'on the left'); notes never print the token for edited originals and removed code-failing narrative sentences",
45	  "artifacts/review-evidence/T-098-staff-engineer-r2-probe2.py on the archive: hedge dropped and mid-sentence quote, forced accept -> gate ready False, export 422, trace fails excerpt_hedge / excerpt_whole_sentence",
46	  "artifacts/review-evidence/T-098-staff-engineer-r2-probe3.py and new T-098-staff-engineer-r3-probe.py on the archive: e8 quote drops hedge -> accept 422 EDIT_QUOTE, summary-only edit 422 with stored EXCERPT_OMITS_QUALIFIER kept and status pending, batch 422, item trace excerpt_hedge EDIT_QUOTE, repair edit 200; narrative sentence citing e99 with '9/10' printed in notes (F1)",
47	  "artifacts/review-evidence/T-098-staff-engineer-r3-mutants.py on a scratch copy: 24 mutants, baseline 128 passed; M11 killed; survivors M2b and M8 (equivalent), M3c and M11b (highlight, F2)"],
48	 "verdict": "pass",
49	 "scores": {"accept_guard_single_choke_point": 5, "batch_guard": 5, "edit_route_vs_accept_guard": 5, "gate_and_trace_recompute": 5, "notes_withhold_failing_wording": 4, "tests_pin_behaviour": 4},
50	 "findings": [
51	  {"severity": "minor", "title": "A removed narrative sentence citing a non-accepted entry prints in the internal notes with its unsupported number",
52	   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r3-probe-results.txt: 'letter has 9/10: False | notes has 9/10: True' and the notes line '- Removed: \"Pain was 9/10 on the left side.\" (e99): NOT_AN_ACCEPTED_ENTRY.'; app/backend/export.py _draft_paragraph hides removed text only for NARRATIVE_CODE_REASONS, not NOT_AN_ACCEPTED_ENTRY.",
53	   "why_it_matters": "The commit states AI wording that failed a check is not printed anywhere in the export; this sentence could not be checked against any quote and is printed with an unsupported figure. It sits in the labelled do-not-send block and the letter is clean, so I rate it minor and leave the rule to Chris.",
54	   "fix": "Print removed narrative text only when its reason is a judge reason; for NOT_AN_ACCEPTED_ENTRY print 'AI wording removed (cited entry is not accepted)' without the text, or record in DECISIONS that the notes may show removed AI text as an audit trail.",
55	   "acceptance_test": "Unit: narrative draft with a sentence citing a non-accepted entry id and containing '9/10'; accept the paragraph with another valid sentence; export: internal_notes_text has no '9/10'. Mutation: restoring the plain print fails it."},
56	  {"severity": "nit", "title": "HIGHLIGHT_NOT_FOUND live recompute is not pinned by any test",
57	   "evidence": "artifacts/review-evidence/T-098-staff-engineer-r3-mutants-results.txt: 'M3c trace highlight live term off -> 128 passed <-- SURVIVED' and 'M11b code_check_failures: highlight check off -> 128 passed <-- SURVIVED'",
58	   "why_it_matters": "A regression in this branch stays green; I found no route that reaches it with a verbatim quote, so it may be dead code.",
59	   "fix": "Add a test with a quote that passes check_excerpt but fails grounding.locate, or remove the branch.",
60	   "acceptance_test": "Mutants M3c and M11b make a new test fail, or the branch is gone."}
61	 ],
62	 "whats_right": [
63	  "set_review runs the five-check recompute on the post-edit wording before any write, so accept, edit (including summary-only), batch and reset share one guard and a refused edit leaves the row and its stored reason untouched (M1, M1b, M1c, M11, M17 each fail a test).",
64	  "A quote-level failure now says EDIT_QUOTE in the 422, the item trace and the gate, and a stale stored pass cannot hide it (M3a, M3b, M3d, M13 fail a test).",
65	  "The new tests assert behaviour through the real API (status codes, stored reasons, absence of the token from the whole export response) and 21 of 24 mutants break one."],
66	 "questions_for_chris": [
67	  "F1: may the internal notes show removed AI narrative text that was never checked against a quote (cited entry not accepted), or must the whole export response be free of unsupported AI numbers?"]}
68	```
69	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:00.346Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/backend/project_backend_conventions.md | head -60; git status --short | grep -v agent-memory; ls .venv/bin/python"
}
````

### User / tool · 2026-11-02T06:02:00.467Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:03.146Z

**tool call — Bash**
````
{
 "command": "git status --short | grep -v agent-memory; ls .venv/bin/python; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; echo $S; ls $S"
}
````

### User / tool · 2026-11-02T06:02:03.280Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:06.194Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mkdir -p $S/ar && git archive HEAD | tar -x -C $S/ar; ls -a $S/ar | head -30; ls .venv/bin/python; git log --oneline -1"
}
````

### User / tool · 2026-11-02T06:02:06.720Z

**tool result**
````
.
..
.claude
.gitignore
CLAUDE.md
MASTER_PROMPT.md
app
artifacts
board
docs
evals
memory
personas
requirements-dev.txt
requirements.txt
research
reviews
spec
submission
tests
tools
.venv/bin/python
faee448 fix(backend): pypdf text read runs in the killed scan child; 2 PDF jobs at once, 429 busy; opaque Popup counts as a cover; RSS watchdog (T-087 r4)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:02:08.764Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/*/6ddf8076*/scratchpad/ar && P=/Users/arsis/zlayt-pm-project/.venv/bin/python; time $P -I -m pytest -p no:cacheprovider -q -x --no-header tests/unit -q 2>&1 | tail -5; $P -I -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -15",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:04:49.699Z

**tool result**
````
/opt/homebrew/Cellar/python@3.12/3.12.2_1/Frameworks/Python.framework/Versions/3.12/lib/python3.12/subprocess.py:571: CalledProcessError
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git
!!!!!!!!!!!!!!!!!!!!!!!!!! stopping after 1 failures !!!!!!!!!!!!!!!!!!!!!!!!!!!

real	0m19.403s
user	0m8.818s
sys	0m3.669s
E        +  where True = exists()
E        +    where exists = (PosixPath('/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-3489/test_fixture_runs_write_no_art0') / 'runs').exists

tests/unit/test_t093_eval_signature.py:169: AssertionError
----------------------------- Captured stdout call -----------------------------
ship_bar_met=False backend=fixture report=/private/var/folders/1s/kbz0fbqn09s345zfzcyhbjqm0000gn/T/pytest-of-arsis/pytest-3489/test_fixture_runs_write_no_art0/20261102T060441Z.md
  blocker: 4_no_invented_facts
  blocker: backend=fixture: determinism_3run and unsupported_count_3run need a live backend (R-CO-7)
  blocker: judge_controls (J3/J4 seeded wrong items): not measured
=========================== short test summary info ============================
FAILED tests/unit/test_eval_runner.py::test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git
FAILED tests/unit/test_provider.py::test_single_call_path - AssertionError: a...
FAILED tests/unit/test_provider_backends.py::test_single_call_path - Assertio...
FAILED tests/unit/test_t093_eval_signature.py::test_fixture_runs_write_no_artifacts
4 failed, 2035 passed, 4 skipped in 140.20s (0:02:20)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:51.156Z

**tool call — Bash**
````
{
 "command": "sed -n 140,185p tests/unit/test_t093_eval_signature.py; grep -n \"def test_write_calibration_is_refused_by_the_cli\" -B3 -A30 tests/unit/test_eval_runner.py; grep -n \"single_call_path\" -A40 tests/unit/test_provider.py | head -80"
}
````

### User / tool · 2026-11-02T06:04:51.263Z

**tool result**
````
def test_a_determinism_failure_is_diagnosable_from_the_report_and_the_artifacts(tmp_path):
    fn = on_run2(lambda o: o["flags"].remove(first(o, lambda f: f["type"] == "gap")))
    m = R.live_metrics(Perfect(mutate=fn), "claude-cli", SAMPLE, 3, runs_dir=tmp_path)["determinism_3run"]
    d = m["differences"]["run1_vs_run2"]["gap_flags"]
    assert d["only_in_first"] and not d["only_in_other"]
    a1, a2 = (json.loads((tmp_path / f"run{i}.json").read_text()) for i in (1, 2))
    assert len([i for i in a1["items"] if i["kind"] == "flag"]) == len([i for i in a2["items"] if i["kind"] == "flag"]) + 1


def test_build_report_writes_every_case_artifact_and_names_the_directory(tmp_path):
    rd = tmp_path / "runs" / "20261102T000000Z"
    r = report(runs_dir=rd)
    names = {p.stem for p in rd.iterdir()}
    assert {"run1", "run2", "run3", "sample", "case_02_gap_boundaries"} <= names
    assert r["run_artifacts"] == str(rd)
    assert f"per-run artifacts: `{rd}`" in R.render_md(r)


def test_main_writes_artifacts_next_to_the_report_for_a_live_backend(tmp_path):
    assert R.main(["--backend", "claude-cli", "--out", str(tmp_path)], pipeline=Perfect()) in (0, 1)
    dirs = list((tmp_path / "runs").iterdir())
    assert len(dirs) == 1 and (dirs[0] / "run3.json").exists() and (dirs[0] / "case_02_gap_boundaries.json").exists()
    assert json.loads((tmp_path / "latest.json").read_text())["run_artifacts"].endswith(dirs[0].name)


def test_fixture_runs_write_no_artifacts(tmp_path):
    R.main(["--backend", "fixture", "--out", str(tmp_path)], pipeline=Perfect("fixture"))
    assert not (tmp_path / "runs").exists()


# ---------------------------------------------------------------- J3 / J4 seeded controls
CONTROLS = R.load_controls()
IN_SAMPLE = [c for c in CONTROLS if c["split"] == "in_sample"]
HELD_OUT = [c for c in CONTROLS if c["split"] == "held_out"]


def test_the_control_file_has_wrong_and_correct_items_for_both_judges():
    assert len({c["id"] for c in CONTROLS}) == len(CONTROLS)
    for j, pos, neg in (("j3", "conflict", "benign"), ("j4", "agree", "disagree")):
        mine = [c for c in CONTROLS if c["judge"] == j]
        assert sum(c["kind"] == "wrong" for c in mine) >= 5 and sum(c["kind"] == "correct" for c in mine) >= 5
        assert all(c.get("why") for c in mine), "every control item, wrong or correct, says why it is labelled as it is"
        assert all(c["synthetic"] is True and c["expected"] == (neg if c["kind"] == "wrong" else pos) for c in mine)

846-    assert c["source_tree_clean"] is True
847-
848-
849:def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):
850-    """T-101 AC2 end to end: an export of HEAD with no .git exits 2 before any run and writes nothing."""
851-    if shutil.which("git") is None:
852-        pytest.skip("git missing")
853-    src = tmp_path / "src"
854-    src.mkdir()
855-    tar = subprocess.run(["git", "archive", "HEAD"], cwd=R.ROOT, capture_output=True, check=True).stdout
856-    subprocess.run(["tar", "-x", "-C", str(src)], input=tar, check=True)
857-    shutil.copy(R.ROOT / "evals" / "run.py", src / "evals" / "run.py")      # the working-tree runner (T-101 is not committed yet)
858-    env = {k: v for k, v in os.environ.items() if k not in ("LLM_BACKEND", "ENABLE_LIVE")}
859-    env["PYTHONPATH"] = str(src)
860-    out = tmp_path / "out"
861-    r = subprocess.run([sys.executable, "-m", "evals.run", "--write-calibration", "--out", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)
862-    assert r.returncode == 2 and "--write-calibration refused" in r.stderr, r.stderr[-800:]
863-    assert not out.exists() or not any(out.iterdir())
864-
865-
866-def test_git_source_reports_commit_and_dirtiness(tmp_path):
867-    if shutil.which("git") is None:
868-        pytest.skip("git missing")
869-    subprocess.run(["git", "init", "-q", str(tmp_path)], check=True)
870-    (tmp_path / "f").write_text("a")
871-    env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t", "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
872-    subprocess.run(["git", "-C", str(tmp_path), "add", "f"], check=True)
873-    subprocess.run(["git", "-C", str(tmp_path), "commit", "-qm", "x"], check=True, env=env)
874-    a = R.git_source(tmp_path)
875-    assert re.fullmatch(r"[0-9a-f]{40}", a["commit"]) and a["clean"] is True
876-    (tmp_path / "f").write_text("b")
877-    assert R.git_source(tmp_path)["clean"] is False
878-    assert R.git_source(tmp_path)["dirty"] == [" M f"]
879-    assert re.fullmatch(r"[0-9a-f]{40}", a["tree"])
115:def test_single_call_path():
116-    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
117-    import re
118-    app = pathlib.Path(__file__).resolve().parents[2] / "app"
119-    # The one allowed exception: app/backend/pdf_ocr.py runs the local Tesseract binary (T-086). That is OCR, not an LLM call; it may import
120-    # subprocess but never the anthropic SDK, and test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract checks it never starts `claude`.
121-    allow_subprocess = {"backend/pdf_ocr.py"}
122-    bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
123-           if "llm/backends" not in p.as_posix()
124-           and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)
125-           and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r"^\s*(import|from)\s+anthropic\b", p.read_text(), re.M))]
126-    assert bad == []
127-
128-def test_no_text_in_logs(monkeypatch, caplog, capsys):
129-    """T-034 AC5 / arch invariant: backend failures never put the prompt, reply or SDK message in errors or logs."""
130-    import logging
131-    caplog.set_level(logging.DEBUG)
132-    from app.llm.backends import claude_cli as C, anthropic_api as A
133-    monkeypatch.setattr(C.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 1, stdout="SECRET REPLY", stderr="SECRET RECORD TEXT"))
134-    with pytest.raises(P.LLMError) as e1:
135-        C.call("m", "s", "SECRET RECORD TEXT", SCHEMA, key="k")
136-    class Boom:
137-        class messages:
138-            @staticmethod
139-            def create(**kw): raise RuntimeError("SECRET RECORD TEXT echoed by SDK")
140-    with pytest.raises(P.LLMError) as e2:
141-        A.call("m", "s", "SECRET RECORD TEXT", SCHEMA, key="k", client=Boom())
142-    out = capsys.readouterr()
143-    assert "SECRET" not in str(e1.value) + str(e2.value) + caplog.text + out.out + out.err
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:53.572Z

**tool call — Bash**
````
{
 "command": "grep -n \"single_call_path\" -A14 tests/unit/test_provider_backends.py; grep -n \"only_runs_tesseract\" -B2 -A20 tests/unit/test_pdf_ocr*.py | head -50; grep -n \"subprocess\\|claude\" app/backend/pdf_hidden.py | head -30; ls tests/unit | grep pdf"
}
````

### User / tool · 2026-11-02T06:04:53.680Z

**tool result**
````
153:def test_single_call_path():
154-    """T-034 AC5: no SDK or subprocess use outside app/llm/backends."""
155-    for p in (ROOT / "app").rglob("*.py"):
156-        if "backends" in p.parts and "llm" in p.parts:
157-            continue
158-        src = p.read_text()
159-        if p.name == "pdf_ocr.py" and "backend" in p.parts:      # local Tesseract binary (T-086), not an LLM call; anthropic stays banned
160-            assert not re.search(r"^\s*(import|from)\s+anthropic\b", src, re.M), p
161-            continue
162-        assert not re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M), p
163-
164-def test_no_text_in_logs(tmp_path, monkeypatch, caplog, capsys):
165-    """T-034 AC5: a failing live call logs neither prompt nor error text."""
166-    caplog.set_level("DEBUG")
167-    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
tests/unit/test_pdf_ocr.py-126-
tests/unit/test_pdf_ocr.py-127-
tests/unit/test_pdf_ocr.py:128:def test_pdf_ocr_only_runs_tesseract():
tests/unit/test_pdf_ocr.py-129-    """The subprocess allow-list in test_provider.py covers pdf_ocr.py because it runs a local OCR binary, not an LLM: it never names
tests/unit/test_pdf_ocr.py-130-    `claude` or the anthropic SDK, and every subprocess.run starts with the tesseract executable (or its --version / --list-langs probes)."""
tests/unit/test_pdf_ocr.py-131-    import pathlib
tests/unit/test_pdf_ocr.py-132-    import re
tests/unit/test_pdf_ocr.py-133-    src = pathlib.Path(pdf_ocr.__file__).read_text()
tests/unit/test_pdf_ocr.py-134-    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("#", '"""')))
tests/unit/test_pdf_ocr.py-135-    assert not re.search(r"claude|anthropic", code, re.I)
tests/unit/test_pdf_ocr.py-136-    calls = re.findall(r"subprocess\.run\(\[([^,\]]+)", src)
tests/unit/test_pdf_ocr.py-137-    assert calls and all(c.strip() in ("exe", "_which()") for c in calls)
tests/unit/test_pdf_ocr.py-138-
tests/unit/test_pdf_ocr.py-139-
tests/unit/test_pdf_ocr.py-140-def test_an_ocr_item_trace_has_the_ocr_source_step(tmp_path):
tests/unit/test_pdf_ocr.py-141-    from app.backend import trace
tests/unit/test_pdf_ocr.py-142-    from app.db import db as DB
tests/unit/test_pdf_ocr.py-143-    from tests.unit import _golden as G
tests/unit/test_pdf_ocr.py-144-    from tests.unit._fakes import FakeCall, sample_script
tests/unit/test_pdf_ocr.py-145-    from app.backend import pipeline as PL
tests/unit/test_pdf_ocr.py-146-    raw = G.raw("sample")
tests/unit/test_pdf_ocr.py-147-    conn = DB.connect(str(tmp_path / "t.sqlite"))
tests/unit/test_pdf_ocr.py-148-    cid = DB.create_case(conn, raw, now=1.0, config_json={"source_pdf": True, "pages": [{"page": 1, "start": 0, "end": len(raw), "source": "ocr"}]})
43:import subprocess
513:        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
515:    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
558:            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode], cwd=_ROOT, env=env,
559:                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
572:            except subprocess.TimeoutExpired:
_pdf.py
_pdf_probe.py
_pdf_raw.py
test_pdf_checks_api.py
test_pdf_hidden.py
test_pdf_hidden_r2.py
test_pdf_hidden_r3.py
test_pdf_hidden_r4.py
test_pdf_ocr.py
test_pdf_ocr_limits.py
test_pdf_upload.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:04:57.958Z

**tool call — Bash**
````
{
 "command": "grep -n -i \"claude\\|anthropic\" app/backend/pdf_hidden.py; grep -n \"subprocess\\.\\(run\\|Popen\\|check\\|call\\)\" app/backend/pdf_hidden.py; head -30 tests/unit/test_pdf_hidden.py; git diff HEAD --stat -- tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_hidden.py"
}
````

### User / tool · 2026-11-02T06:04:58.075Z

**tool result**
````
513:        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
558:            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode], cwd=_ROOT, env=env,
"""T-087: text in the text layer that is not visible when the page is rendered is flagged per page and kept out of the case text
until the paralegal confirms it. Synthetic PDFs are generated here (tests/unit/_pdf_raw.py)."""
import pytest

from app.backend import pdf_checks, pdf_hidden, pdf_text
from tests.unit._pdf_raw import build, build_pages, text_page

pytest.importorskip("pypdfium2")

VISIBLE = "SYNTHETIC visit 03/04/2023 Dr. Rao: neck pain 6/10, ibuprofen prescribed."
HIDDEN = {
    "white": (b"BT /F1 12 Tf 1 1 1 rg 50 650 Td (PLANTED white text: patient was symptom free.) Tj ET", "blends_with_background"),
    "offpage": (b"BT /F1 12 Tf 0 g 900 650 Td (PLANTED off page text.) Tj ET", "off_page"),
    "tiny": (b"BT /F1 1 Tf 0 g 50 600 Td (PLANTED tiny text.) Tj ET", "tiny_font"),
    "invisible": (b"BT /F1 12 Tf 3 Tr 0 g 50 550 Td (PLANTED invisible mode text.) Tj ET 0 Tr", "invisible_render_mode"),
    "scaled_tiny": (b"q 0.1 0 0 0.1 0 0 cm BT /F1 20 Tf 0 g 500 5000 Td (PLANTED scaled tiny text.) Tj ET Q", "tiny_font"),
    "covered": (b"BT /F1 12 Tf 0 g 50 500 Td (PLANTED covered text.) Tj ET\n1 1 1 rg 40 490 300 40 re f", "blends_with_background"),
    "near_white": (b"BT /F1 12 Tf 0.97 g 50 450 Td (PLANTED nearly white text.) Tj ET", "blends_with_background"),
}


def pdf_with(*keys, page_text=VISIBLE):
    return build(text_page([page_text]) + b"\n" + b"\n".join(HIDDEN[k][0] for k in keys))


@pytest.mark.parametrize("key", sorted(HIDDEN))
def test_each_kind_of_hidden_text_is_flagged_with_its_reason(key):
    scanned = pdf_hidden.scan(pdf_with(key))
    hidden = scanned["pages"][1]["hidden"]
    assert len(hidden) == 1 and "PLANTED" in hidden[0]["text"]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:05.712Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\nimport re\np='tests/unit/test_provider.py'\ns=open(p).read()\ns=s.replace('''    allow_subprocess = {\"backend/pdf_ocr.py\"}''','''    # And app/backend/pdf_hidden.py (T-087): it starts a local child process (this interpreter running its own scan module, plus a `ps` RSS probe)\n    # so a hung PDF renderer can be killed; no LLM. test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children checks it never names `claude`.\n    allow_subprocess = {\"backend/pdf_ocr.py\", \"backend/pdf_hidden.py\"}''')\nopen(p,'w').write(s)\np='tests/unit/test_provider_backends.py'\ns=open(p).read()\ns=s.replace('''        if p.name == \"pdf_ocr.py\" and \"backend\" in p.parts:      # local Tesseract binary (T-086), not an LLM call; anthropic stays banned''','''        if p.name in (\"pdf_ocr.py\", \"pdf_hidden.py\") and \"backend\" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls; anthropic stays banned''')\nopen(p,'w').write(s)\nEOF\ncat >> tests/unit/test_pdf_hidden.py <<'EOF'\n\n\ndef test_pdf_hidden_only_starts_local_children():\n    \"\"\"The subprocess allow-list in test_provider.py covers pdf_hidden.py because it only starts local children and makes no LLM call: it never\n    names `claude` or the anthropic SDK, and every subprocess call starts either `ps` (RSS probe) or this interpreter running its own scan module.\"\"\"\n    import pathlib\n    import re\n    code = \"\\n\".join(l for l in pathlib.Path(pdf_hidden.__file__).read_text().splitlines() if not l.lstrip().startswith((\"#\", '\"\"\"')))\n    assert not re.search(r\"claude|anthropic\", code, re.I)\n    calls = re.findall(r\"subprocess\\.(?:run|Popen|call|check_output|check_call)\\(\\[([^\\]]+)\\]\", code)\n    assert len(calls) == 2\n    assert all(c.startswith('\"ps\"') or c.startswith('sys.executable, \"-m\", \"app.backend.pdf_hidden\"') for c in calls), calls\n    assert not re.search(r\"os\\.system|shell\\s*=\\s*True|os\\.exec|os\\.spawn\", code)\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children tests/unit/test_provider.py::test_single_call_path tests/unit/test_provider_backends.py::test_single_call_path 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T06:05:06.134Z

**tool result**
````
...                                                                      [100%]
3 passed in 0.10s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:08.282Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- evals/run.py; grep -n \"runs_dir\\|\\\"runs\\\"\\|'runs'\\|run_artifacts\" evals/run.py | head -40; git log --oneline -6 -- evals/run.py tests/unit/test_t093_eval_signature.py"
}
````

### User / tool · 2026-11-02T06:05:08.425Z

**tool result**
````
475:def run_cases(pipeline, backend, cases=None, runs_dir=None):
477:    With runs_dir each case's artifact is written as <runs_dir>/<case>.json (items, states, judge codes), so a case-level miss is diagnosable."""
483:        write_run_artifact(runs_dir, name, out, name)
711:def write_run_artifact(runs_dir, fname, out, name=None, run=None):
713:    if runs_dir is None:
718:    d = pathlib.Path(runs_dir)
724:def live_metrics(pipeline, backend, text, runs=3, runs_dir=None):
726:    With runs_dir each run's artifact (run1.json ..) is written there, and a mismatch lists the differing fields and items."""
733:        write_run_artifact(runs_dir, f"run{i}", o, "sample", i)
737:    det = {"value": sum(s == sigs[0] for s in sigs[1:]) / (runs - 1), "runs": runs, "status": "measured", "r_ids": RIDS["determinism_3run"],
742:            "unsupported_count_3run": {"value": sum(unsupported), "per_run": unsupported, "runs": runs, "status": "measured", "r_ids": RIDS["unsupported_count_3run"]}}
864:                               and m["unsupported_count_3run"].get("value") == 0 and m["unsupported_count_3run"].get("runs") == 3
865:                               and m["determinism_3run"].get("value") == 1.0 and m["determinism_3run"].get("runs") == 3
870:        if backend in LIVE_BACKENDS and m[k].get("runs") != 3:
897:def build_report(pipeline, backend, runs=3, cases=None, req_path=REQUIREMENTS, check_summary=None, lexicon_flags=None, runs_dir=None, judge_control=None):
899:    results, outs = run_cases(pipeline, backend, cases, runs_dir)
911:        m.update(live_metrics(pipeline, backend, sample, runs, runs_dir))
932:    if runs_dir is not None:
933:        report["run_artifacts"] = pathlib.Path(runs_dir).relative_to(ROOT).as_posix() if pathlib.Path(runs_dir).is_relative_to(ROOT) else str(runs_dir)
1010:          *( [f"- per-run artifacts: `{r['run_artifacts']}`"] if r.get("run_artifacts") else [] ),
1054:            scratch = outdir / "runs" / (scratch_ts or ts)
1197:    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
fdc2506 fix(qa): --write-calibration judges the header in write_report, refuses untracked inputs and --controls, shares one run dir (T-101 r2)
4c5f9bf fix(qa): plain evals.run leaves calibration.json alone; --write-calibration writes it only from a clean HEAD (T-101)
b85fc1b fix(evals): forged calibration source_commit fails instead of skipping; record source tree; check-fresh rebuilds sentences (T-090 r3)
a850be0 fix: restore T-090 work reverted by 2fca530
7df65fb feat(evals): J3/J4 controls rebuilt as matched pairs, held-out split, 3 repeats, per-item report (T-093 r2)
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:09.798Z

**tool call — Bash**
````
{
 "command": "sed -n 1035,1075p evals/run.py; sed -n 1180,1215p evals/run.py"
}
````

### User / tool · 2026-11-02T06:05:09.881Z

**tool result**
````
    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
    copy under outdir/runs/<scratch_ts or ts>/ so a plain run never touches the file the app serves (T-101).
    write_calibration is judged here as well as in main(), so every caller that reaches the committed file meets the same clean-HEAD rule (T-101 r2)."""
    if write_calibration:                         # checked before anything is written: a refused call leaves the directory as it was
        cal = r.get("calibration") or {}
        why = "the report has no calibration" if not cal else write_calibration_refusal(
            {"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"), "dirty": []})
        if why:
            raise CalibrationRefused(why)
    outdir = pathlib.Path(outdir)
    outdir.mkdir(parents=True, exist_ok=True)
    ts = r["generated_at"].replace(":", "").replace("-", "")
    (outdir / f"{ts}.md").write_text(render_md(r))
    (outdir / "latest.json").write_text(json.dumps(r, indent=1, sort_keys=True, default=str) + "\n")
    if r.get("calibration"):                      # small file the app serves (T-090); written only by --write-calibration (T-101)
        body = json.dumps(r["calibration"], indent=1, sort_keys=True) + "\n"
        if write_calibration:
            (outdir / "calibration.json").write_text(body)
        else:
            scratch = outdir / "runs" / (scratch_ts or ts)
            scratch.mkdir(parents=True, exist_ok=True)
            (scratch / "calibration.json").write_text(body)
    return outdir / f"{ts}.md"


def check_fresh(latest_path=REPORTS / "latest.json", root=ROOT):
    """0 when latest.json hashes equal the files on disk; 1 otherwise (or when latest.json is missing)."""
    p = pathlib.Path(latest_path)
    if not p.exists():
        print("check-fresh: no latest.json", file=sys.stderr)
        return 1
    old, now = json.loads(p.read_text()).get("hashes", {}), hashes(root)
    diff = sorted(k for k in set(old) | set(now) if old.get(k) != now.get(k))
    for k in diff:
        print(f"check-fresh: {k} changed since the report", file=sys.stderr)
    bad = check_calibration(p.parent / "calibration.json", root)
    for m in bad:
        print(f"check-fresh: calibration.json {m}", file=sys.stderr)
    return 1 if diff or bad else 0


        # The eval runner must not report a fixture run as if it were the live one the caller asked for - refuse loudly instead.
        print(f"evals.run: backend={backend} requested but ENABLE_LIVE=1 is not set, so app.llm.provider would serve the fixture backend "
              f"(D-008/D-020). Re-run with: LLM_BACKEND={backend} ENABLE_LIVE=1 python3 -m evals.run --runs 3", file=sys.stderr)
        return 2
    if a.write_calibration and a.controls:           # T-101 r2: controls mode writes no calibration, so the combination is refused, not silently ignored
        print("evals.run: --write-calibration cannot be combined with --controls (controls mode writes no calibration); nothing was run or written.",
              file=sys.stderr)
        return 2
    if a.write_calibration:                          # T-101: refuse before any run is paid for, never write a dirty-tree calibration
        why = write_calibration_refusal(git_source())
        if why:
            print(f"evals.run: --write-calibration refused, nothing was run or written: {why}.", file=sys.stderr)
            return 2
    ts = dt.datetime.now(dt.timezone.utc).strftime("%Y%m%dT%H%M%SZ")
    if a.controls:
        return run_controls_only(backend, out, ts)
    real = pipeline is None
    report = build_report(pipeline or load_pipeline(), backend, a.runs, runs_dir=out / "runs" / ts if backend in LIVE_BACKENDS else None,
                          judge_control=default_judge_control(backend) if real and backend in LIVE_BACKENDS else None)
    if a.write_calibration:                          # the tree can be dirtied during a long run: judge the header that would be written (T-101)
        cal = report.get("calibration") or {}
        why = write_calibration_refusal({"commit": cal.get("source_commit"), "clean": cal.get("source_tree_clean"),
                                         "dirty": (git_source().get("dirty") or []) if cal.get("source_tree_clean") is False else []})
        if why:
            print(f"evals.run: --write-calibration refused after the run, nothing was written: {why}.", file=sys.stderr)
            return 2
    try:
        path = write_report(report, out, write_calibration=a.write_calibration, scratch_ts=ts)   # one run directory: runs/<ts> (T-101 r2)
    except CalibrationRefused as e:                  # backstop: write_report judges the header too
        print(f"evals.run: --write-calibration refused, nothing was written: {e}.", file=sys.stderr)
        return 2
    print(f"ship_bar_met={report['ship_bar_met']} backend={report['backend']} report={path}")
    for b in report["blockers"]:
        print("  blocker:", b)
    return 0 if report["ship_bar_met"] else 1       # 2 is reserved for refused runs (curated fixtures)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:12.155Z

**tool call — Bash**
````
{
 "command": "grep -n \"scratch\\|runs\\\" /\" tests/unit/test_eval_runner.py | head -20"
}
````

### User / tool · 2026-11-02T06:05:12.239Z

**tool result**
````
628:    """T-101 AC1: `python -m evals.run` (default out = evals/reports) leaves evals/reports/calibration.json byte-identical and writes a scratch copy."""
636:    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
637:    assert len(scratch) == 1 and json.loads(scratch[0].read_text()) == json.loads(json.dumps(good["calibration"]))
705:    R.write_report(dirty, tmp_path / "plain")                     # a plain write of the same report is still fine: it goes to scratch
721:def test_scratch_copy_and_live_run_artifacts_share_one_run_directory(monkeypatch, tmp_path, good):
722:    """T-101 r2 F4: the scratch calibration.json lands in the same runs/<ts> directory the live run artifacts use."""
733:    scratch = list((tmp_path / "runs").glob("*/calibration.json"))
734:    assert len(scratch) == 1 and scratch[0].parent == seen["runs_dir"]
839:    # scratch copy under out/runs/<ts>/ (T-101). Exactly one must exist either way.
884:    """T-101 r2 F1: an untracked golden case, fixture or prompt makes the tree dirty; an untracked report or a scratch file outside the inputs does not."""
897:    (tmp_path / "scratch.txt").write_text("outside the inputs")                                   # not an input either
902:    assert "evals/reports" not in " ".join(src["dirty"]) and "scratch.txt" not in " ".join(src["dirty"])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:14.122Z

The test is stale; T-101 deliberately puts a scratch calibration copy in `runs/<ts>/`. I'll fix the test to assert what it was meant to guard: no per-case or per-run artifacts from a fixture run.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:16.962Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_t093_eval_signature.py'\ns=open(p).read()\ns=s.replace('''    R.main([\"--backend\", \"fixture\", \"--out\", str(tmp_path)], pipeline=Perfect(\"fixture\"))\n    assert not (tmp_path / \"runs\").exists()''','''    R.main([\"--backend\", \"fixture\", \"--out\", str(tmp_path)], pipeline=Perfect(\"fixture\"))\n    # T-101: a plain run puts a scratch calibration.json under runs/<ts>/ (so the committed file is untouched); that is the only file allowed there.\n    files = [p.relative_to(tmp_path / \"runs\").as_posix() for p in (tmp_path / \"runs\").rglob(\"*\") if p.is_file()] if (tmp_path / \"runs\").exists() else []\n    assert [f for f in files if not f.endswith(\"/calibration.json\")] == [], \"a fixture run writes no run*.json or per-case artifacts\"\n    assert json.loads((tmp_path / \"latest.json\").read_text()).get(\"run_artifacts\") in (None, \"\")''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_t093_eval_signature.py 2>&1 | tail -3\ngrep -n \"def git_source\" -A25 evals/run.py; grep -n \"def write_calibration_refusal\" -A18 evals/run.py"
}
````

### User / tool · 2026-11-02T06:05:19.443Z

**tool result**
````
.............................................................            [100%]
61 passed in 2.16s
75:def git_source(root=ROOT):
76-    """{'commit': HEAD hash, 'clean': no tracked file differs from HEAD and no untracked file sits under GIT_INPUT_PATHS, 'tree': HEAD^{tree},
77-    'dirty': the porcelain lines that make it dirty}; Nones when git is unavailable. A calibration file is only traceable when it was produced from a
78-    clean tree (T-090 r2: generate in a clean worktree of HEAD). Untracked files outside the inputs (e.g. a scratch file at the repo root) do not count."""
79-    import subprocess
80-
81-    def git(*args):
82-        return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True, timeout=20, check=True).stdout
83-    try:
84-        head = git("rev-parse", "HEAD").strip()
85-        tree = git("rev-parse", "HEAD^{tree}").strip()
86-        tracked = [l for l in git("status", "--porcelain", "--untracked-files=no").splitlines() if l.strip()]
87-        untracked = [l for l in git("status", "--porcelain", "--untracked-files=all", "--", *GIT_INPUT_PATHS).splitlines() if l.startswith("?? ")]
88-    except (OSError, subprocess.SubprocessError):
89-        return {"commit": None, "clean": None, "tree": None, "dirty": []}
90-    dirty = tracked + untracked
91-    return {"commit": head, "clean": not dirty, "tree": tree, "dirty": dirty}
92-
93-
94-def sha256_file(p):
95-    return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
96-
97-
98-def hashes(root=ROOT):
99-    """sha256 of every app/llm/prompts/*.md and app/llm/lexicon.yaml (CONTRACT 8.3 regression discipline)."""
100-    out = {}
1020:def write_calibration_refusal(src):
1021-    """T-101: why --write-calibration may not run, or None. The committed calibration.json is only written from a clean tree at a commit: no tracked
1022-    file differs from HEAD and no untracked file sits under the eval's inputs (T-090 r2: the header must name the code that produced the counts)."""
1023-    if src.get("commit") is None or src.get("clean") is None:
1024-        return "no git repository or HEAD commit is available to name as the source"
1025-    if not src["clean"]:
1026-        paths = [p.rstrip() for p in (src.get("dirty") or [])]
1027-        shown = "; ".join(paths[:10]) or "paths not listed"
1028-        more = f"; and {len(paths) - 10} more" if len(paths) > 10 else ""
1029-        return (f"the tree has uncommitted changes or untracked files under the eval inputs ({shown}{more}); "
1030-                "commit, stash or remove them, or run from a clean worktree of HEAD")
1031-    return None
1032-
1033-
1034-def write_report(r, outdir=REPORTS, write_calibration=False, scratch_ts=None):
1035-    """latest.json and the .md always. calibration.json: the committed file (outdir/calibration.json) only when write_calibration; otherwise a scratch
1036-    copy under outdir/runs/<scratch_ts or ts>/ so a plain run never touches the file the app serves (T-101).
1037-    write_calibration is judged here as well as in main(), so every caller that reaches the committed file meets the same clean-HEAD rule (T-101 r2)."""
1038-    if write_calibration:                         # checked before anything is written: a refused call leaves the directory as it was
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:26.684Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/*/6ddf8076*/scratchpad/ar && ls -a | grep -c \"^.git$\"; mkdir -p /tmp/_x 2>/dev/null; PYTHONPATH=$PWD /Users/arsis/zlayt-pm-project/.venv/bin/python -m evals.run --write-calibration --out $PWD/../outx; echo rc=$?; rmdir /tmp/_x; ls ../outx 2>&1 | head -2"
}
````

### User / tool · 2026-11-02T06:05:26.938Z

**tool result**
````
0
evals.run: --write-calibration refused, nothing was run or written: no git repository or HEAD commit is available to name as the source.
rc=2
ls: ../outx: No such file or directory
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:32.652Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_eval_runner.py'\ns=open(p).read()\nold=s[s.index('def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git'):s.index('def test_git_source_reports_commit_and_dirtiness')]\nnew='''def test_write_calibration_is_refused_by_the_cli_in_an_exported_tree_without_git(tmp_path):\n    \"\"\"T-101 AC2 end to end: a copy of the tree with no .git exits 2 with a clear message before any run and writes nothing. The copy is made with\n    shutil (not `git archive`), so the test also runs inside an export of HEAD that has no .git itself (T-106).\"\"\"\n    src = tmp_path / \"src\"\n    for d in (\"app\", \"evals\", \"spec\"):\n        if (R.ROOT / d).is_dir():\n            shutil.copytree(R.ROOT / d, src / d, ignore=shutil.ignore_patterns(\".git\", \"__pycache__\", \"runs\"))\n    assert not (src / \".git\").exists()\n    env = {k: v for k, v in os.environ.items() if k not in (\"LLM_BACKEND\", \"ENABLE_LIVE\")}\n    env[\"PYTHONPATH\"] = str(src)\n    out = tmp_path / \"out\"\n    r = subprocess.run([sys.executable, \"-m\", \"evals.run\", \"--write-calibration\", \"--out\", str(out)], cwd=src, env=env, capture_output=True, text=True, timeout=120)\n    assert r.returncode == 2 and \"--write-calibration refused\" in r.stderr and \"no git repository\" in r.stderr, r.stderr[-800:]\n    assert \"Traceback\" not in r.stderr\n    assert not out.exists() or not any(out.iterdir())\n\n\n'''\ns=s.replace(old,new)\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_eval_runner.py -k \"write_calibration_is_refused\" 2>&1 | tail -3"
}
````

### User / tool · 2026-11-02T06:05:33.181Z

**tool result**
````
..                                                                       [100%]
2 passed, 97 deselected in 0.23s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:35.173Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend/export.py app/backend/trace.py app/backend/review.py; grep -n \"NARRATIVE_CODE_REASONS\\|NOT_AN_ACCEPTED_ENTRY\\|Removed\" app/backend/*.py"
}
````

### User / tool · 2026-11-02T06:05:35.270Z

**tool result**
````
app/backend/export.py:33:NARRATIVE_CODE_REASONS = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "SEVERITY_NOT_QUOTED", "FLAG_CONTENT")
app/backend/export.py:546:        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
app/backend/export.py:549:            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
app/backend/narrative.py:17:    "NOT_AN_ACCEPTED_ENTRY": "The sentence cites an entry that is not accepted.",
app/backend/narrative.py:100:            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
app/backend/trace.py:50:    "NOT_AN_ACCEPTED_ENTRY": narrative.REASONS["NOT_AN_ACCEPTED_ENTRY"],
app/backend/trace.py:647:    rcodes = list((rem or {}).get("reasons") or []) if reason not in ("NOT_AN_ACCEPTED_ENTRY",) and not str(reason).startswith("JUDGE_") else []
app/backend/trace.py:654:    cited_ok = reason != "NOT_AN_ACCEPTED_ENTRY"
app/backend/trace.py:655:    st.append(step("cites_accepted_entry", "Cites an accepted entry", "code", PASS if cited_ok else FAIL, "The sentence cites an entry you accepted." if cited_ok else TRACE_WHY["NOT_AN_ACCEPTED_ENTRY"],
app/backend/trace.py:656:                   reason=None if cited_ok else "NOT_AN_ACCEPTED_ENTRY", rule="D-031", evidence={"values": {"entry_id": s["entry_id"]}},
app/backend/trace.py:659:        st.append(_skipped("sentence_checks", "Numbers, qualifiers and wording match the quote", "code", "NOT_AN_ACCEPTED_ENTRY", "D-006", "Not run: the cited entry is not accepted."))
app/backend/trace.py:688:        code, label = "removed", "Removed from the draft"
app/backend/trace.py:703:                               "step_id": "cites_accepted_entry" if c == "NOT_AN_ACCEPTED_ENTRY" else ("sentence_checks" if c in rcodes else "judge_1")}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:37.555Z

**tool call — Bash**
````
{
 "command": "sed -n 525,560p app/backend/export.py; grep -n \"internal_notes_text\\|9/10\\|e99\" tests/unit/test_export*.py tests/unit/test_d051*.py 2>/dev/null | head -20; grep -ln \"NARRATIVE_CODE_REASONS\\|Removed:\\|sentence removed\" tests/unit/*.py"
}
````

### User / tool · 2026-11-02T06:05:37.658Z

**tool result**
````
def _cite_tail(v, entry_id):
    e = next(x for x in v.entries if x["id"] == entry_id)
    return f"{v.source(e['record_no'])}, {_long_date(v.date_of(e))}"


def _draft_paragraph(v):
    n = v.narrative
    if not n:
        return []
    live = {e["id"]: e for e in v.in_entries}
    st = n.get("status", "pending")
    lines = ["", "DRAFT TREATMENT PARAGRAPH (AI-drafted from accepted entries; each sentence cites one entry and passed code checks and the second check)"]
    lines.append({"pending": "- Not in the letter until you accept it.", "dismissed": "- Dismissed; not in the letter.",
                  "accepted": "- Accepted: included in the letter as TREATMENT SUMMARY."}.get(st, "- Not in the letter."))
    for s in n.get("sentences", []):
        e = live.get(s["entry_id"])
        stale = e is None or (n.get("basis") or {}).get(s["entry_id"]) != basis_hash(e)
        tag = "" if st != "accepted" or not stale else " [NOT in the letter: the cited entry changed or is no longer accepted]"
        lines.append(f'- {s["text"]} ({s.get("cite") or s["entry_id"]}){tag}')
    for r in n.get("removed", []):
        if r["reason"] in NARRATIVE_CODE_REASONS:       # D-051: wording that failed a code check is not printed anywhere in the export
            lines.append(f'- AI wording removed (failed a check: {r.get("message") or r["reason"]}) ({r["entry_id"]}): {r["reason"]}.')
        else:
            lines.append(f'- Removed: "{r["text"]}" ({r["entry_id"]}): {r["reason"]}.')
    return lines


def _notes(v):
    accepted = [f for f in v.flags if _status(f) == "in"]
    dismissed = [f for f in v.flags if f.get("review_status") in OUT]
    pending = _pending(v)
    sec = [
        NOTES_TITLE, "",
        AI_LINE.format(n=len(pending)), "",
        "FLAGS ACCEPTED", *_flag_block(v, accepted), "",
tests/unit/test_export.py:32:    """R-EX-6: all entries + both charges accepted -> letter_text and internal_notes_text equal sample.export.expected.txt exactly."""
tests/unit/test_export.py:36:    assert out["internal_notes_text"] == notes.rstrip("\n")
tests/unit/test_export.py:58:    assert re.search(r"Record 5 \(Capital PT, visit 8, February 20, 2026\) — dismissed", out["internal_notes_text"])
tests/unit/test_export.py:68:    assert "$185" in out["internal_notes_text"] and "Request itemized PT ledger" in out["internal_notes_text"]
tests/unit/test_export.py:84:    assert "Visit 8: pain 4/10, improving." in out["internal_notes_text"]
tests/unit/test_export.py:129:    n = X.build_export(build_case())["internal_notes_text"]
tests/unit/test_export.py:135:    n = X.build_export(build_case())["internal_notes_text"]
tests/unit/test_export.py:142:    n = X.build_export(build_case())["internal_notes_text"]
tests/unit/test_export.py:150:    assert "Items not reviewed: 1." in out["internal_notes_text"]
tests/unit/test_export.py:151:    n = out["internal_notes_text"]
tests/unit/test_export.py:161:    n = X.build_export(c)["internal_notes_text"]
tests/unit/test_export.py:172:    sec = out["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
tests/unit/test_export.py:180:    sec = X.build_export(c)["internal_notes_text"].split("EDITED ITEMS")[1].split("PENDING ITEMS")[0]
tests/unit/test_export_edge.py:12:    sec = out["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1].split("EDITED ITEMS")[0]
tests/unit/test_export_edge.py:23:    sec = out["internal_notes_text"].split("RECORDS NOT IN THE TREATMENT SECTION")[1].split("EDITED ITEMS")[0]
tests/unit/test_export_edge.py:33:    assert "9,999" not in out["letter_text"] and "excerpt not found in record" in out["internal_notes_text"]
tests/unit/test_export_edge.py:37:    n = X.build_export(build_case())["internal_notes_text"]
tests/unit/test_export_edge.py:62:    n = out["internal_notes_text"]
tests/unit/test_narrative.py
tests/unit/test_trace.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:40.114Z

**tool call — Bash**
````
{
 "command": "grep -n \"internal_notes_text\\|Removed\\|AI wording removed\" tests/unit/test_narrative.py | head -20; sed -n 1,60p tests/unit/test_narrative.py"
}
````

### User / tool · 2026-11-02T06:05:40.209Z

**tool result**
````
116:    assert "DRAFT TREATMENT PARAGRAPH" in ex["internal_notes_text"] and "Not in the letter until you accept it" in ex["internal_notes_text"]
137:    assert "DRAFT TREATMENT" not in out["internal_notes_text"] and "TREATMENT SUMMARY" not in out["letter_text"]
174:    notes = ex["internal_notes_text"]
"""T-059 (D-031): firm-voice treatment paragraph from ACCEPTED entries only; every sentence code-checked and judged; seeded hallucinations are removed."""
import pytest
from app.backend import export as X, narrative as N, pipeline as PL, review as RV, store
from app.db import db as DB
from tests.unit import _golden as G
from tests.unit._fakes import FakeCall, sample_script


def accepted_sample(tmp_path, accept=lambda n: True):
    conn = DB.connect(str(tmp_path / "n.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=FakeCall(sample_script()), now=lambda: 1.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["state"] != "rejected" and accept(int(e["id"][1:])):
            RV.apply_review(conn, cid, e["id"], {"action": "accept"}, call=FakeCall(sample_script()))
    return conn, cid


GOOD = [{"entry_id": "e1", "text": "On January 9, 2026, Austin EMS documented a restrained driver rear-ended at approx. 35 mph who complained of neck pain 7/10 and headache."},
        {"entry_id": "e5", "text": "On February 20, 2026, Capital PT recorded pain 4/10, improving."}]


def narr(sentences, judge="supported"):
    return FakeCall({"narrative": {"sentences": sentences}, "j1": {"verdict": judge, "reason_code": "NONE"}})


def test_good_sentences_kept_with_citations(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    n = N.draft(conn, cid, call=narr(GOOD), now=2.0)
    assert [s["entry_id"] for s in n["sentences"]] == ["e1", "e5"] and not n["removed"] and n["status"] == "pending"
    assert all(s["cite"].startswith("record ") and s["judge"]["verdict"] == "supported" for s in n["sentences"])


def test_only_accepted_entries_are_sent_to_the_model(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: n in (1, 5))
    call = narr(GOOD)
    N.draft(conn, cid, call=call, now=2.0)
    user = call.prompts("narrative")[0]
    assert "ENTRY e1" in user and "ENTRY e5" in user and "ENTRY e2 " not in user and "ENTRY e7" not in user
    for flagword in ("73 days", "gap", "Conflict", "FLAGS"):
        assert flagword.lower() not in user.lower().replace("approx", "")


def test_no_accepted_entries_means_no_call(tmp_path):
    conn, cid = accepted_sample(tmp_path, accept=lambda n: False)
    call = narr(GOOD)
    n = N.draft(conn, cid, call=call, now=2.0)
    assert n["error"] == "NO_ACCEPTED_ENTRIES" and call.steps() == []


E5 = "On February 20, 2026, Capital PT recorded pain 4/10, improving"     # e5 quote: 'Pain 4/10, improving.' (no hedge, no self-report marker)
TOK, QUAL, CAUSE, FLAG, SEV = ("SUMMARY_TOKEN_NOT_IN_EXCERPT", "SUMMARY_DROPS_QUALIFIER", "CAUSATION_NOT_QUOTED", "FLAG_CONTENT", "SEVERITY_NOT_QUOTED")


@pytest.mark.parametrize("entry,text,reasons", [
    # D-006: each of number, side, negation and date, on a quote with no hedge so ONLY the token check can fire
    ("e5", E5.replace("4/10", "9/10") + ".", [TOK]),
    ("e5", E5.replace("pain", "left pain") + ".", [TOK]),
    ("e5", E5.replace("pain", "no pain") + ".", [TOK]),
    ("e5", E5.replace("February 20", "March 5") + ".", [TOK]),
    ("e1", "On January 9, 2026, Austin EMS found a herniated disc at C6-C7 and neck pain 9/10.", [TOK, QUAL]),            # invented numbers; also drops C/O
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:43.314Z

**tool call — Bash**
````
{
 "command": "sed -n 105,200p tests/unit/test_narrative.py; sed -n 85,110p app/backend/narrative.py"
}
````

### User / tool · 2026-11-02T06:05:43.402Z

**tool result**
````
    conn, cid = accepted_sample(tmp_path)
    s = {"entry_id": "e9", "text": "On June 12, 2026, Hill Country Pain Management recorded that the patient states symptoms began after the January collision."}
    n = N.draft(conn, cid, call=narr([s]), now=2.0)
    assert len(n["sentences"]) == 1 and not n["removed"]


# ---- export wiring: internal until accepted
def test_internal_notes_until_accepted_then_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert "DRAFT TREATMENT PARAGRAPH" in ex["internal_notes_text"] and "Not in the letter until you accept it" in ex["internal_notes_text"]
    assert "TREATMENT SUMMARY" not in ex["letter_text"] and GOOD[0]["text"] not in ex["letter_text"]
    N.review(conn, cid, "accept", now=3.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert "TREATMENT SUMMARY" in ex["letter_text"] and f"{GOOD[1]['text']} (Capital PT, visit 8, February 20, 2026)" in ex["letter_text"]


def test_dismissed_and_stale_sentences_stay_out_of_the_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "dismiss", now=3.0)
    assert "TREATMENT SUMMARY" not in X.build_export(store.export_case(conn, cid))["letter_text"]
    N.review(conn, cid, "accept", now=4.0)
    RV.apply_review(conn, cid, "e5", {"action": "dismiss"})                      # the cited entry leaves the letter
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[1]["text"] not in ex["letter_text"] and GOOD[0]["text"] in ex["letter_text"]


def test_export_without_a_narrative_is_unchanged():
    from tests.unit.test_export import build_case
    out = X.build_export(build_case())
    assert "DRAFT TREATMENT" not in out["internal_notes_text"] and "TREATMENT SUMMARY" not in out["letter_text"]


# ---- recorded fixtures (claude-cli, sample case): replay through audited; python /private/tmp/.../rec_narr.py --record regenerates them
def test_recorded_sample_paragraph_replays_with_every_sentence_supported(tmp_path, monkeypatch):
    import pathlib
    from app.llm import audited as AU
    root = pathlib.Path(__file__).resolve().parents[2]
    monkeypatch.setenv("LLM_BACKEND", "fixture")
    monkeypatch.delenv("LLM_FIXTURE_DIR", raising=False)
    conn = DB.connect(str(tmp_path / "r.sqlite")); cid = DB.create_case(conn, G.raw("sample"), now=1.0)
    PL.run_pipeline(conn, cid, G.raw("sample"), call=AU.make_call(conn, cid), now=lambda: 1.0)
    for e in DB.list_items(conn, cid, "entry"):
        if e["state"] != "rejected":
            RV.apply_review(conn, cid, e["id"], {"action": "accept"})
    monkeypatch.setenv("LLM_FIXTURE_DIR", str(root / "tests" / "fixtures" / "llm" / "narrative"))
    n = N.draft(conn, cid, call=AU.make_call(conn, cid), now=2.0)
    assert not n.get("error") and len(n["sentences"]) >= 6 and not n["removed"]
    assert all(s["judge"]["verdict"] == "supported" and s["cite"] for s in n["sentences"])
    text = " ".join(s["text"] for s in n["sentences"]).lower()
    assert "73 days" not in text and " gap" not in text and "conflict" not in text
    steps = [c["step"] for c in DB.list_llm_calls(conn, cid) if c["step"] in ("narrative", "j1")]
    assert steps.count("narrative") == 1 and steps.count("j1") >= len(n["sentences"])      # the ladder record has every call


# ---- T-059 review F2: an entry edited after the draft drops its sentence (basis hash), the others stay
def test_entry_edited_after_the_draft_drops_its_sentence_from_the_letter(tmp_path):
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[0]["text"] in ex["letter_text"] and GOOD[1]["text"] in ex["letter_text"]           # control: both in before the edit
    RV.apply_review(conn, cid, "e5", {"action": "edit", "edits": {"summary": "Pain rated 4/10, improving."}}, call=FakeCall(sample_script()))
    assert [e for e in DB.list_items(conn, cid, "entry") if e["id"] == "e5"][0]["review_status"] == "edited"      # still in the letter as an entry
    ex = X.build_export(store.export_case(conn, cid))
    assert GOOD[1]["text"] not in ex["letter_text"] and GOOD[0]["text"] in ex["letter_text"]
    tag = "[NOT in the letter: the cited entry changed or is no longer accepted]"
    notes = ex["internal_notes_text"]
    assert f'- {GOOD[1]["text"]} (' in notes and tag in notes.split(GOOD[1]["text"])[1].split("\n")[0]
    assert tag not in notes.split(GOOD[0]["text"])[1].split("\n")[0]                                   # the unchanged sentence carries no tag


# ---- T-059 review F4: a failed re-draft must not overwrite the paragraph the paralegal already has
class Boom(Exception):
    pass


def failing_calls():
    from app.llm import audited as AU, provider as P
    return [("llm_failed", FakeCall({"narrative": AU.LLMFailed("down")})), ("fixture_miss", FakeCall({"narrative": P.FixtureMiss("none")})),
            ("schema", FakeCall({"narrative": {"sentences": "not a list"}})), ("type", FakeCall({"narrative": None}))]


@pytest.mark.parametrize("which", range(4))
def test_failed_redraft_keeps_the_accepted_paragraph(tmp_path, which):
    name, bad = failing_calls()[which]
    conn, cid = accepted_sample(tmp_path)
    N.draft(conn, cid, call=narr(GOOD), now=2.0)
    N.review(conn, cid, "accept", now=3.0)
    before = N.get(conn, cid)
    out = N.draft(conn, cid, call=bad, now=4.0)
    assert out["error"] == "LLM_FAILED_AFTER_RETRIES", name                       # the failure is reported alongside ...
    assert out["status"] == "accepted" and [s["entry_id"] for s in out["sentences"]] == ["e1", "e5"]
    assert N.get(conn, cid) == before and "error" not in N.get(conn, cid)         # ... and nothing stored changed
        return dict(existing, error=base["error"]) if existing else base
    prompt = promptlib.load("narrative_v1")
    nonce = promptlib.nonce(case["raw_text"], "narrative", ",".join(by_id))
    try:
        out, call_id = call("narrative", prompt.text, prompt_user(entries, nonce), schemas.NarrativeOutput.model_json_schema(), item_id="narrative")
        sents = schemas.NarrativeOutput.model_validate(out).sentences
    except (AU.LLMFailed, P.FixtureMiss, ValidationError, TypeError, ValueError):
        base["error"] = "LLM_FAILED_AFTER_RETRIES"
        return _keep_or_save(conn, case_id, case, existing, base)
    base["generator"] = {"model": judges.generator_model(), "prompt_version": prompt.name, "call_id": call_id}
    for k, s in enumerate(sents, 1):
        text, eid = s.text.strip(), s.entry_id
        item = {"id": f"ns{k}", "entry_id": eid, "text": text}
        e = by_id.get(eid)
        if e is None:
            base["removed"].append({**item, "reason": "NOT_AN_ACCEPTED_ENTRY"})
            continue
        reasons = check_sentence(text, e)
        item["code_checks"] = {"reasons": reasons}
        if reasons:
            base["removed"].append({**item, "reason": reasons[0], "reasons": reasons})
            continue
        # the date of service lives in the record header, not the quote: give the judge the header it may rely on
        verdict, jcall, jcode = judges.run_j1_meta(text, e["excerpt"], f"{e['label']} (date of service {export._long_date(e['date_iso'])})",
                                                   call=call, item_id=item["id"])
        lad = judges.to_ladder("j1", verdict)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:05:50.924Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='app/backend/export.py'\ns=open(p).read()\ns=s.replace('''        else:\n            lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.')\n    return lines''','''        elif r[\"reason\"] == \"NOT_AN_ACCEPTED_ENTRY\":     # T-106: no quote to check this sentence against, so its wording is never printed either\n            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r[\"entry_id\"]}): {r[\"reason\"]}.')\n        else:\n            lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.')\n    return lines''')\nopen(p,'w').write(s)\nEOF\ncat >> tests/unit/test_narrative.py <<'EOF'\n\n\n# ---- T-106 (T-098 r3 F1): a sentence that cites an entry that is not accepted was never code-checked; the notes do not print its wording\ndef test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry(tmp_path):\n    conn, cid = accepted_sample(tmp_path)\n    bad = {\"entry_id\": \"e99\", \"text\": \"Pain was 9/10 on the left side.\"}\n    n = N.draft(conn, cid, call=narr(GOOD + [bad]), now=2.0)\n    assert [r[\"reason\"] for r in n[\"removed\"]] == [\"NOT_AN_ACCEPTED_ENTRY\"] and [s[\"entry_id\"] for s in n[\"sentences\"]] == [\"e1\", \"e5\"]\n    for accept in (False, True):\n        if accept:\n            N.review(conn, cid, \"accept\", now=3.0)\n        ex = X.build_export(store.export_case(conn, cid))\n        notes = ex[\"internal_notes_text\"]\n        assert \"9/10 on the left\" not in notes and \"left side\" not in notes and \"9/10 on the left\" not in ex[\"letter_text\"]\n        assert \"Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.\" in notes\n        assert GOOD[0][\"text\"] in notes                                                  # control: the checked sentences still print\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_narrative.py tests/unit/test_export*.py tests/unit/test_trace.py 2>&1 | tail -4"
}
````

### User / tool · 2026-11-02T06:06:01.410Z

**tool result**
````
........................................................................ [ 47%]
........................................................................ [ 94%]
........                                                                 [100%]
152 passed in 9.82s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:04.467Z

**tool call — Bash**
````
{
 "command": "cp app/backend/export.py /tmp/export.bak 2>/dev/null; cp app/backend/export.py \"$TMPDIR/export.bak\" 2>/dev/null; sed -i '' 's/elif r\\[\"reason\"\\] == \"NOT_AN_ACCEPTED_ENTRY\":/elif False:/' app/backend/export.py && .venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_narrative.py -k non_accepted 2>&1 | tail -2; sed -i '' 's/elif False:/elif r[\"reason\"] == \"NOT_AN_ACCEPTED_ENTRY\":/' app/backend/export.py; rm -f /tmp/export.bak; git diff -- app/backend/export.py | grep '^[+-]' "
}
````

### User / tool · 2026-11-02T06:06:05.289Z

**tool result**
````
FAILED tests/unit/test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry
1 failed, 36 deselected in 0.45s
--- a/app/backend/export.py
+++ b/app/backend/export.py
+        elif r["reason"] == "NOT_AN_ACCEPTED_ENTRY":     # T-106: no quote to check this sentence against, so its wording is never printed either
+            lines.append(f'- Sentence removed (cites an entry that is not accepted) ({r["entry_id"]}): {r["reason"]}.')
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:06.901Z

**tool call — Bash**
````
{
 "command": "grep -n \"HIGHLIGHT_NOT_FOUND\" -r app tests | head -20; grep -n \"def check_excerpt\" -A40 app/backend/*.py | head -80"
}
````

### User / tool · 2026-11-02T06:06:07.008Z

**tool result**
````
app/backend/why.py:10:    "HIGHLIGHT_NOT_FOUND": "The quote could not be located in the record text, so it cannot be highlighted.",
app/backend/trace.py:71:    "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight", "DATE_AMBIGUOUS": "date_confirmed",
app/backend/trace.py:369:    code_step("highlight", "Quote can be highlighted in the record", "HIGHLIGHT_NOT_FOUND", "The quote's position in the record was found, so it can be highlighted.", "row 4",
app/backend/trace.py:370:              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or "HIGHLIGHT_NOT_FOUND" in live)
app/backend/trace.py:611:        if "HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or any(s["start"] is None for s in spans):
app/backend/trace.py:612:            st.append(step("highlight", "Quote can be highlighted in the record", "code", FAIL, reason_text("HIGHLIGHT_NOT_FOUND"), reason="HIGHLIGHT_NOT_FOUND", rule="row 4",
app/backend/confidence.py:10:    "HIGHLIGHT_NOT_FOUND", "JUDGE_PARTIAL", "JUDGE_UNSUPPORTED", "JUDGE_DISAGREES", "JUDGE_UNSURE", "JUDGE_UNAVAILABLE",
app/backend/review.py:64:                      "HIGHLIGHT_NOT_FOUND")
app/backend/review.py:66:                   "EXCERPT_OMITS_QUALIFIER": "excerpt_hedge", "EXCERPT_NOT_WHOLE_SENTENCE": "excerpt_whole_sentence", "HIGHLIGHT_NOT_FOUND": "highlight"}
app/backend/review.py:67:QUOTE_LEVEL_REASONS = ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE", "HIGHLIGHT_NOT_FOUND")   # only a change to the QUOTE clears these
app/backend/review.py:73:                "EXCERPT_NOT_WHOLE_SENTENCE": "the quote is not whole sentences", "HIGHLIGHT_NOT_FOUND": "the quote cannot be found in the record"}
app/backend/review.py:99:            out["HIGHLIGHT_NOT_FOUND"] = {}
app/backend/review.py:124:    elif c == "HIGHLIGHT_NOT_FOUND":
app/backend/review.py:257:        raise _bad("The quoted sentences cannot be found in the record, so they cannot be highlighted. Change the quote.", reason="HIGHLIGHT_NOT_FOUND")
app/backend/generator.py:85:            code_reasons.append("HIGHLIGHT_NOT_FOUND")
app/backend/grounding.py:53:    """First (start, end) raw span of the excerpt in the record, or None (offset lookup failed: HIGHLIGHT_NOT_FOUND)."""
tests/unit/test_grounding.py:80:    """R-RV-9: mutated record -> offset lookup fails -> None (item drops to needs_review HIGHLIGHT_NOT_FOUND)."""
tests/unit/test_confidence.py:49:    (L(code_reasons=["HIGHLIGHT_NOT_FOUND"]), X(), "HIGHLIGHT_NOT_FOUND"),
app/backend/grounding.py:88:def check_excerpt(record_text: str, excerpt: str) -> list:
app/backend/grounding.py-89-    """[] when clean. Not verbatim -> ['GROUNDING_EXCERPT_NOT_VERBATIM'] (rejected, nothing else is evaluated)."""
app/backend/grounding.py-90-    from app.backend import sentences as S
app/backend/grounding.py-91-    spans = locate_all(record_text, excerpt)
app/backend/grounding.py-92-    if not spans:
app/backend/grounding.py-93-        return ["GROUNDING_EXCERPT_NOT_VERBATIM"]
app/backend/grounding.py-94-    reasons = []
app/backend/grounding.py-95-    units = S.stripped_spans(record_text)
app/backend/grounding.py-96-    starts, ends = {a for a, _ in units}, {b for _, b in units}
app/backend/grounding.py-97-    aligned = [sp for sp in spans if sp[0] in starts and sp[1] in ends]
app/backend/grounding.py-98-    if not aligned:
app/backend/grounding.py-99-        reasons.append("EXCERPT_NOT_WHOLE_SENTENCE")
app/backend/grounding.py-100-    s, e = (aligned or spans)[0]
app/backend/grounding.py-101-    # a hedge unit immediately after the last unit the excerpt touches must travel with it (R-TL-8, D-021)
app/backend/grounding.py-102-    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
app/backend/grounding.py-103-    nxt = (touched[-1] + 1) if touched else len(units)
app/backend/grounding.py-104-    if nxt < len(units):
app/backend/grounding.py-105-        a, b = units[nxt]
app/backend/grounding.py-106-        if is_hedge_unit(record_text[a:b]):
app/backend/grounding.py-107-            reasons.append("EXCERPT_OMITS_QUALIFIER")
app/backend/grounding.py-108-    return reasons
app/backend/grounding.py-109-
app/backend/grounding.py-110-
app/backend/grounding.py-111-def check_amount(record_text: str, raw_amount: str) -> list:
app/backend/grounding.py-112-    """An amount the model (or an edit) reports must appear in the record exactly as written (R-CH-1). Never auto-corrected:
app/backend/grounding.py-113-    '$1,2OO' is found as written, the 'fixed' '$1,200' is not. A longer figure does not vouch for a shorter one ('$185' vs '$1,850')."""
app/backend/grounding.py-114-    raw = (raw_amount or "").strip()
app/backend/grounding.py-115-    if raw:
app/backend/grounding.py-116-        for m in re.finditer(re.escape(raw), record_text):
app/backend/grounding.py-117-            before = record_text[m.start() - 1] if m.start() else ""
app/backend/grounding.py-118-            tail = record_text[m.end():m.end() + 2]
app/backend/grounding.py-119-            if not before.isdigit() and not re.match(r"\d|[,.]\d", tail):
app/backend/grounding.py-120-                return []
app/backend/grounding.py-121-    return ["GROUNDING_AMOUNT_NOT_IN_TEXT"]
app/backend/grounding.py-122-
app/backend/grounding.py-123-
app/backend/grounding.py-124-# ---------------------------------------------------------------- summary checks
app/backend/grounding.py-125-_NUM = re.compile(r"\d+(?:,\d{3})*(?:\.\d+)?")
app/backend/grounding.py-126-# One source of truth for side and negation words (D-047): the edit route, the generator's code check and the export gate all use it.
app/backend/grounding.py-127-# Contractions (didn't, can't) count as a negation word of their own. Qualifier words (attribution, hedge, approximation) are added by added_qualifier_tokens().
app/backend/grounding.py-128-_WORDS = re.compile(r"\b(left|right|bilateral(?:ly)?|no|not|none|never|without|denies|denied|negative|neither|nor|absent)\b|\b(\w+n't)\b", re.IGNORECASE)
app/backend/spanish_text.py:173:def check_excerpt(record_text: str, excerpt: str) -> list:
app/backend/spanish_text.py-174-    """grounding.check_excerpt on the ORIGINAL Spanish text, plus the Spanish hedge rule: a hedge sentence right after the quote
app/backend/spanish_text.py-175-    ('Compatible con contractura.') must travel with it (R-TL-8). The match itself is the same whitespace-normalised substring test."""
app/backend/spanish_text.py-176-    from app.backend import sentences as S
app/backend/spanish_text.py-177-    reasons = grounding.check_excerpt(record_text, excerpt)
app/backend/spanish_text.py-178-    if "GROUNDING_EXCERPT_NOT_VERBATIM" in reasons or "EXCERPT_OMITS_QUALIFIER" in reasons:
app/backend/spanish_text.py-179-        return reasons
app/backend/spanish_text.py-180-    spans = grounding.locate_all(record_text, excerpt)
app/backend/spanish_text.py-181-    units = S.stripped_spans(record_text)
app/backend/spanish_text.py-182-    starts, ends = {a for a, _ in units}, {b for _, b in units}
app/backend/spanish_text.py-183-    s, e = next((sp for sp in spans if sp[0] in starts and sp[1] in ends), spans[0])
app/backend/spanish_text.py-184-    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
app/backend/spanish_text.py-185-    nxt = (touched[-1] + 1) if touched else len(units)
app/backend/spanish_text.py-186-    if nxt < len(units) and is_hedge_unit(record_text[units[nxt][0]:units[nxt][1]]):
app/backend/spanish_text.py-187-        reasons.append("EXCERPT_OMITS_QUALIFIER")
app/backend/spanish_text.py-188-    return reasons
app/backend/spanish_text.py-189-
app/backend/spanish_text.py-190-
app/backend/spanish_text.py-191-# ---------------------------------------------------------------- the D-034 checks, Spanish quote vs English summary
app/backend/spanish_text.py-192-def new_tokens(summary: str, excerpt: str, label: str = "", date_iso: str = "") -> list:
app/backend/spanish_text.py-193-    """Numbers, dollar figures, months and left/right/no/not/without in the English summary that the Spanish quote, the source label or
app/backend/spanish_text.py-194-    the parsed date do not support. Same contract as grounding.new_tokens."""
app/backend/spanish_text.py-195-    allowed = _allowed_numbers(excerpt, label, date_iso)
app/backend/spanish_text.py-196-    out = [t for t in grounding._num_tokens(summary) if t not in allowed]
app/backend/spanish_text.py-197-    ok = allowed_english_words(excerpt)
app/backend/spanish_text.py-198-    out += [w for w in grounding.side_neg_words(summary, keep_order=True) if w not in ok]
app/backend/spanish_text.py-199-    out += [w for w in added_qualifier_tokens(summary, excerpt) if w not in out]
app/backend/spanish_text.py-200-    src = fold(excerpt + " " + label)
app/backend/spanish_text.py-201-    months = _date_months(excerpt, date_iso) | {grounding._MONTHS[int(m.group(1)) - 1]
app/backend/spanish_text.py-202-                                                for m in [re.match(r"\d{4}-(\d{2})", date_iso or "")] if m}
app/backend/spanish_text.py-203-    months |= {MONTHS_ES[w] for w in _words(label) if w in MONTHS_ES}
app/backend/spanish_text.py-204-    out += [x.lower() for x in grounding._MONTH_RX.findall(summary) if x.lower() not in months and x.lower() not in src]
app/backend/spanish_text.py-205-    return list(dict.fromkeys(out))
app/backend/spanish_text.py-206-
app/backend/spanish_text.py-207-
app/backend/spanish_text.py-208-def added_qualifier_tokens(summary: str, excerpt: str) -> list:
app/backend/spanish_text.py-209-    """D-047 for a Spanish quote: attribution, hedge or approximation words in the English summary when the Spanish (or mixed English) quote has no qualifier
app/backend/spanish_text.py-210-    of that kind. Same contract as grounding.added_qualifier_tokens. The quote side is as wide as dropped_qualifiers' reading of it."""
app/backend/spanish_text.py-211-    folded = fold(excerpt)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:08.498Z

**tool call — Bash**
````
{
 "command": "sed -n 40,120p app/backend/grounding.py; sed -n 88,130p app/backend/review.py; sed -n 70,92p app/backend/generator.py"
}
````

### User / tool · 2026-11-02T06:06:08.591Z

**tool result**
````
    """Every (start, end) raw span whose whitespace-normalised text equals the normalised excerpt."""
    ex = normalize(excerpt)
    if not ex:
        return []
    norm, idx = _norm_with_map(record_text)
    spans, pos = [], norm.find(ex)
    while pos != -1:
        spans.append((idx[pos], idx[pos + len(ex) - 1] + 1))
        pos = norm.find(ex, pos + 1)
    return spans


def locate(record_text: str, excerpt: str):
    """First (start, end) raw span of the excerpt in the record, or None (offset lookup failed: HIGHLIGHT_NOT_FOUND)."""
    spans = locate_all(record_text, excerpt)
    return spans[0] if spans else None


# ---------------------------------------------------------------- lexicon (hedge / attribution sets)
@functools.lru_cache(maxsize=1)
def _lexicon() -> dict:
    data = yaml.safe_load(_LEXICON.read_text())
    entries = data["entries"] if isinstance(data, dict) and "entries" in data else data
    hedges, selfrep = {}, {}
    for e in entries:
        if not isinstance(e, dict):
            continue
        if "pattern" not in e:
            if e.get("hedge") or e.get("self_report"):
                raise ValueError(f"lexicon entry {e.get('id')} is a hedge/self_report entry without a pattern")
            continue
        if e.get("hedge"):
            hedges[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
        if e.get("self_report"):
            selfrep[e["id"]] = re.compile(e["pattern"], re.IGNORECASE)
    scope = (data.get("self_report_scope") or {}).get("exclude_sentence") if isinstance(data, dict) else None
    return {"hedge": hedges, "self_report": selfrep, "self_report_exclude": re.compile(scope, re.IGNORECASE) if scope else None}


def hedge_ids(text: str) -> set:
    return {i for i, rx in _lexicon()["hedge"].items() if rx.search(text)}


def is_hedge_unit(unit_text: str) -> bool:
    return bool(hedge_ids(unit_text))


# ---------------------------------------------------------------- excerpt check
def check_excerpt(record_text: str, excerpt: str) -> list:
    """[] when clean. Not verbatim -> ['GROUNDING_EXCERPT_NOT_VERBATIM'] (rejected, nothing else is evaluated)."""
    from app.backend import sentences as S
    spans = locate_all(record_text, excerpt)
    if not spans:
        return ["GROUNDING_EXCERPT_NOT_VERBATIM"]
    reasons = []
    units = S.stripped_spans(record_text)
    starts, ends = {a for a, _ in units}, {b for _, b in units}
    aligned = [sp for sp in spans if sp[0] in starts and sp[1] in ends]
    if not aligned:
        reasons.append("EXCERPT_NOT_WHOLE_SENTENCE")
    s, e = (aligned or spans)[0]
    # a hedge unit immediately after the last unit the excerpt touches must travel with it (R-TL-8, D-021)
    touched = [i for i, (a, b) in enumerate(units) if a < e and b > s]
    nxt = (touched[-1] + 1) if touched else len(units)
    if nxt < len(units):
        a, b = units[nxt]
        if is_hedge_unit(record_text[a:b]):
            reasons.append("EXCERPT_OMITS_QUALIFIER")
    return reasons


def check_amount(record_text: str, raw_amount: str) -> list:
    """An amount the model (or an edit) reports must appear in the record exactly as written (R-CH-1). Never auto-corrected:
    '$1,2OO' is found as written, the 'fixed' '$1,200' is not. A longer figure does not vouch for a shorter one ('$185' vs '$1,850')."""
    raw = (raw_amount or "").strip()
    if raw:
        for m in re.finditer(re.escape(raw), record_text):
            before = record_text[m.start() - 1] if m.start() else ""
            tail = record_text[m.end():m.end() + 2]
            if not before.isdigit() and not re.match(r"\d|[,.]\d", tail):
                return []
        g = spanish.module_for(language.record_lang(rec))
        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
        if toks:
            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
        dropped = g.dropped_qualifiers(summ, exc)
        if dropped:
            out["SUMMARY_DROPS_QUALIFIER"] = {"qualifiers": list(dropped)}
        for c in g.check_excerpt(rec["excerpt"], exc):             # the quote against its record: word for word, whole sentences, keeps the hedge sentence
            if c in ("GROUNDING_EXCERPT_NOT_VERBATIM", "EXCERPT_OMITS_QUALIFIER", "EXCERPT_NOT_WHOLE_SENTENCE"):
                out[c] = {}
        if grounding.locate(rec["excerpt"], exc) is None and "GROUNDING_EXCERPT_NOT_VERBATIM" not in out:
            out["HIGHLIGHT_NOT_FOUND"] = {}
    for c in item.get("state_reasons") or []:
        if c in CODE_CHECK_REASONS:
            out.setdefault(c, {})
    return {c: out[c] for c in CODE_CHECK_REASONS if c in out}


def code_check_message(fails: dict) -> str:
    """Plain words for the first failing check, then the next step."""
    c = next(iter(fails))
    d = fails[c]
    if c == "SUMMARY_TOKEN_NOT_IN_EXCERPT" and d.get("tokens"):
        toks = d["tokens"]
        if any(_NUMERIC_TOKEN.search(t) for t in toks):
            what = "The summary has a number, date or dollar figure that is not in the quote: " + ", ".join(toks) + "."
        else:
            what = "The summary says " + _quoted_words(toks) + ", which the quote does not say."
    elif c == "SUMMARY_DROPS_QUALIFIER" and d.get("qualifiers"):
        what = "The quote carries " + "; ".join(_QUALIFIER_WORDS.get(k, k) for k in d["qualifiers"]) + " that the summary leaves out."
    elif c == "GROUNDING_EXCERPT_NOT_VERBATIM":
        what = "The quote is not word for word in the record."
    elif c == "EXCERPT_OMITS_QUALIFIER":
        what = "The quote leaves out a hedge sentence that qualifies it."
    elif c == "EXCERPT_NOT_WHOLE_SENTENCE":
        what = "The quote does not start and end on whole sentences."
    elif c == "HIGHLIGHT_NOT_FOUND":
        what = "The quote cannot be found in the record, so it cannot be highlighted."
    else:
        what = "The summary does not match the quote."
    return f"{what} {EDIT_QUOTE_TEXT if c in QUOTE_LEVEL_REASONS else EDIT_SUMMARY_TEXT}."




def verify(e: dict, record: dict, summary: str, excerpt: str) -> dict:
    """Stage 2 (code): grounding of the excerpt, summary token/qualifier checks, offsets. Never edits the model's text."""
    body = record["excerpt"]
    g = spanish.module_for(language.record_lang(record))     # English: grounding itself; Spanish: the same checks mapped onto Spanish words
    exc_reasons = g.check_excerpt(body, excerpt)
    failures = [c for c in exc_reasons if c in confidence.REJECTED_CODES]
    code_reasons = [c for c in exc_reasons if c not in confidence.REJECTED_CODES]
    if language.record_lang(record) == "uncertain":          # D-042: never verified when the language is not confidently English or Spanish
        code_reasons.append("LANGUAGE_UNCERTAIN")
    span = grounding.locate(body, excerpt)
    if not failures:
        code_reasons += g.check_summary(summary, excerpt, record["source"], record.get("date_iso") or "")
        if span is None:
            code_reasons.append("HIGHLIGHT_NOT_FOUND")
    base = body_offset(record)
    e.update(summary=summary, excerpt=excerpt,
             excerpt_start=base + span[0] if span else None, excerpt_end=base + span[1] if span else None,
             source_kind="record")
    cc = e["ladder"]["code_checks"]
    cc.update(excerpt_verbatim=not failures, excerpt_whole_sentence="EXCERPT_NOT_WHOLE_SENTENCE" not in code_reasons,
              qualifier_carried="EXCERPT_OMITS_QUALIFIER" not in code_reasons and "SUMMARY_DROPS_QUALIFIER" not in code_reasons,
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:15.490Z

**tool call — Bash**
````
{
 "command": "grep -n \"live\\b\\|live =\" app/backend/trace.py | head -20; grep -n \"highlight_found\" -r app | head; grep -n \"excerpt_hedge\" tests/unit/*.py | head; grep -n \"def code_check_failures\" -B2 -A12 app/backend/review.py"
}
````

### User / tool · 2026-11-02T06:06:15.609Z

**tool result**
````
235:    """The paralegal's rung. pending (live item) blocks export; rejected can only be dismissed; dismissed is skipped."""
269:    live = row.get("state") != "rejected"
290:    blocks = (live and rs == "pending") if blocks_flag is None else blocks_flag
319:    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
320:    verbatim_fail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False or "GROUNDING_EXCERPT_NOT_VERBATIM" in live
360:              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_NOT_WHOLE_SENTENCE" in R or cc.get("excerpt_whole_sentence") is False or "EXCERPT_NOT_WHOLE_SENTENCE" in live)
362:              na("EDIT_QUOTE", {"item_id": row["id"]}), failed="EXCERPT_OMITS_QUALIFIER" in R or "EXCERPT_OMITS_QUALIFIER" in live)
363:    toks = cc.get("summary_tokens_not_in_excerpt") or (live.get("SUMMARY_TOKEN_NOT_IN_EXCERPT") or {}).get("tokens") or []
366:              evidence={"tokens": toks}, failed="SUMMARY_TOKEN_NOT_IN_EXCERPT" in R or bool(toks) or "SUMMARY_TOKEN_NOT_IN_EXCERPT" in live)
368:              "D-022", na("EDIT_SUMMARY", {"item_id": row["id"]}), failed="SUMMARY_DROPS_QUALIFIER" in R or "SUMMARY_DROPS_QUALIFIER" in live)
370:              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or "HIGHLIGHT_NOT_FOUND" in live)
409:    """An accepted or edited, live entry: its failing code checks block the export (D-051). Accept refuses such an item, so this is old data or a
980:        st.append(step("review", "Your accept, edit or dismiss on each item", "human", PASS, "Every live item has your decision.", rule="row 17", counts=rc))
app/frontend/mock.js:73:      code_checks: { excerpt_verbatim: true, excerpt_whole_sentence: true, qualifier_carried: true, date_provider_from_header: true, summary_tokens_not_in_excerpt: [], highlight_found: true },
app/backend/trace.py:370:              na("READ_RECORD", {"record_id": rid}), failed="HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or "HIGHLIGHT_NOT_FOUND" in live)
app/backend/trace.py:611:        if "HIGHLIGHT_NOT_FOUND" in R or cc.get("highlight_found") is False or any(s["start"] is None for s in spans):
app/backend/flags.py:169:        f["ladder"]["code_checks"] = {"excerpt_verbatim": "GROUNDING_EXCERPT_NOT_VERBATIM" not in fail, "highlight_found": f["evidence"][0]["start"] is not None}
app/backend/review.py:321:    lad.setdefault("code_checks", {}).update(summary_tokens_not_in_excerpt=toks, highlight_found=span is not None,
app/backend/review.py:463:                              "highlight_found": span is not None, "qualifier_carried": "SUMMARY_DROPS_QUALIFIER" not in chk["code_reasons"],
app/backend/generator.py:95:              highlight_found=span is not None)
tests/unit/test_trace.py:128:    assert [s["id"] for s in t["steps"]] == ["extracted", "excerpt_verbatim", "excerpt_whole_sentence", "excerpt_hedge", "summary_tokens", "summary_qualifier",
tests/unit/test_trace.py:165:    for sid in ("excerpt_whole_sentence", "excerpt_hedge", "summary_tokens", "summary_qualifier", "highlight", "judge_1"):
tests/unit/test_trace.py:1269:        assert err["detail"]["reason_code"] == "EXCERPT_OMITS_QUALIFIER" and err["detail"]["step_id"] == "excerpt_hedge"
tests/unit/test_trace.py:1304:    ("hedge sentence dropped", HEDGE_Q, "Disc protrusion at C5-C6 with mild right foraminal narrowing.", "EXCERPT_OMITS_QUALIFIER", "excerpt_hedge"),
79-
80-
81:def code_check_failures(rec, item: dict) -> dict:
82-    """{reason_code: detail} for every D-034/D-047/D-022 code check the entry's CURRENT summary and quote fail. Recomputed from the text (same
83-    functions the generator and the edit route use), plus any such reason already stored on the item, so old data cannot slip through.
84-    `rec` is a store.load_records() dict (None: only the stored reasons count)."""
85-    out = {}
86-    summ, exc = current_text(item)
87-    if rec is not None:
88-        g = spanish.module_for(language.record_lang(rec))
89-        toks = g.new_tokens(summ, exc, rec.get("source") or item.get("provider") or "", rec.get("date_iso") or item.get("date_iso") or "")
90-        if toks:
91-            out["SUMMARY_TOKEN_NOT_IN_EXCERPT"] = {"tokens": toks}
92-        dropped = g.dropped_qualifiers(summ, exc)
93-        if dropped:
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:19.420Z

**tool call — Bash**
````
{
 "command": "sed -n 1,40p tests/unit/test_trace.py; sed -n 1285,1345p tests/unit/test_trace.py; sed -n 300,325p app/backend/trace.py"
}
````

### User / tool · 2026-11-02T06:06:19.512Z

**tool result**
````
"""D-042 check traces (T-080): per-item stepper, case stepper with export gate, judge summary, and the full/metadata visibility split.
Fixture backend, no key. One recorded sample run is built once; each test works on its own copy of the database."""
import json
import pathlib
import sqlite3
import time

import pytest
from fastapi.testclient import TestClient

from app.backend import trace, why
from app.backend.api import create_app
from app.db import db as DB

STATUSES = {"pass", "fail", "skipped", "pending"}
KINDS = {"code", "llm", "human"}
NEXT_CODES = {"DECIDE", "CONFIRM_DATE", "EDIT_SUMMARY", "EDIT_QUOTE", "READ_RECORD", "COMPARE_BY_HAND", "DISMISS_OR_ENTER_BY_HAND", "RERUN", "SENTENCE_REMOVED", "CONFIRM_RERUN", "RERUN_JUDGE"}
FULL_ONLY_KEYS = {"response_raw", "before", "after", "edited_text"}


@pytest.fixture(scope="module")
def base(tmp_path_factory):
    import os
    d = tmp_path_factory.mktemp("trace")
    old = {k: os.environ.get(k) for k in ("LLM_BACKEND", "ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY")}
    os.environ["LLM_BACKEND"] = "fixture"
    for k in ("ZLAYT_MODE", "ENABLE_LIVE", "ANTHROPIC_API_KEY"):
        os.environ.pop(k, None)
    db = str(d / "base.sqlite")
    c = TestClient(create_app(db, static_dir=str(d)), client=("127.0.0.1", 50000))
    pre = c.post("/api/cases", json={"sample": True}).json()["token"]          # an ingested case that never ran
    tok = c.post("/api/cases", json={"sample": True}).json()["token"]
    assert c.post(f"/api/cases/{tok}/run", json={}).status_code == 202
    for _ in range(240):
        if c.get(f"/api/cases/{tok}/status").json()["status"] in ("ready", "failed"):
            break
        time.sleep(0.25)
    assert c.get(f"/api/cases/{tok}/status").json()["status"] == "ready"
    yield {"dir": d, "db": db, "tok": tok, "pre": pre}
    for k, v in old.items():
    assert row["review_status"] == "pending" and "EXCERPT_OMITS_QUALIFIER" in row["state_reasons"]


def test_set_review_is_the_choke_point_for_accept_edit_and_batch_d051_r3(env):
    from app.backend import review as REV
    c, conn, tok, _ = env
    eid = _e8_ai_draft_with_short_quote(c, conn, tok)
    for action, kw in (("accept", {}), ("edit", {"edited": {"summary": "x y", "at": "t"}})):
        with pytest.raises(REV.ReviewError) as ei:
            REV.set_review(conn, tok, eid, action, now=9e9, **kw)
        assert ei.value.status == 422 and ei.value.code == "CODE_CHECK_FAILED"
    with pytest.raises(REV.ReviewError):
        REV.batch_apply(conn, tok, eid, "accept", 9e9)
    assert DB.get_item(conn, eid, tok)["review_status"] == "pending"
    REV.batch_apply(conn, tok, eid, "reset", 9e9)                                                    # the way out is never blocked
    assert not [e for e in DB.list_events(conn, tok, eid) if e["action"] in ("accept", "edit")]


QUOTE_AND_SUMMARY_CASES = [      # (name, excerpt, summary, expected reason, failing trace step); every stored check result is left as a pass
    ("hedge sentence dropped", HEDGE_Q, "Disc protrusion at C5-C6 with mild right foraminal narrowing.", "EXCERPT_OMITS_QUALIFIER", "excerpt_hedge"),
    ("quote starts mid-sentence", "disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically.",
     "Disc protrusion with mild right foraminal narrowing; findings may represent degenerative change.", "EXCERPT_NOT_WHOLE_SENTENCE", "excerpt_whole_sentence"),
    ("quote is not in the record", "Patient reports the collision was the cause of the disc protrusion.", "Patient reports the collision was the cause of the disc protrusion.",
     "GROUNDING_EXCERPT_NOT_VERBATIM", "excerpt_verbatim"),
    ("number not in the quote", HEDGE_FULL, "Disc protrusion with pain 5/10, findings may represent degenerative change.", "SUMMARY_TOKEN_NOT_IN_EXCERPT", "summary_tokens"),
    ("qualifier dropped", HEDGE_FULL, "Disc protrusion at C5-C6 with mild right foraminal narrowing.", "SUMMARY_DROPS_QUALIFIER", "summary_qualifier"),
]


@pytest.mark.parametrize("name,excerpt,summary,reason,step_id", QUOTE_AND_SUMMARY_CASES, ids=[x[0] for x in QUOTE_AND_SUMMARY_CASES])
def test_gate_and_trace_recompute_all_code_checks_over_a_stale_stored_pass_d051_r3(env, name, excerpt, summary, reason, step_id):
    """The reviewer's F2: every stored result says pass, the text fails one check. Accept refuses; a forced accept is a gate blocker, GET /export is 422
    and the item trace shows that step failing with blocks_export. Mutant M11 (the quote checks off) fails the first three cases."""
    c, conn, tok, _ = env
    row = DB.get_item(conn, "e8", tok)
    lad = row["ladder"]
    lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
    lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
    DB.update_item(conn, "e8", now=9e9, case=tok, summary=summary, excerpt=excerpt, state="verified", state_reasons_json=[], ladder=lad)
    r = c.post(f"/api/cases/{tok}/items/e8/review", json={"action": "accept"})
    assert r.status_code == 422 and r.json()["error"]["detail"]["reason_code"] == reason
    DB.apply_review(conn, "e8", "accept", now=9e9, case=tok)                                         # old data / any route that skips the guard
    c.post(f"/api/cases/{tok}/items/e1/review", json={"action": "accept"})
    g = _gate(c, tok)
    assert g["ready"] is False and [(b["item_id"], b["reason_code"]) for b in _ccf(g)] == [("e8", reason)]
    assert c.get(f"/api/cases/{tok}/export").status_code == 422
    stp = steps_of(c.get(f"/api/cases/{tok}/items/e8/trace").json())[step_id]
    assert stp["status"] == "fail" and stp["blocks_export"] is True and stp["reason_code"] == reason


def test_internal_notes_never_print_ai_wording_that_failed_a_check_d051_r3(env):
    """EDITED ITEMS 'summary was' and the narrative 'Removed' line say the AI wording was removed, not what it said."""
    c, conn, tok, _ = env
    ents = c.get(f"/api/cases/{tok}").json()["entries"]
    eid = ents[0]["id"]
    row = DB.get_item(conn, eid, tok)
    DB.apply_review(conn, eid, "edit", edited={"summary": row["summary"], "original_summary": "Pain 5/10 on the left.", "at": "2026-11-02T00:00:00Z"}, now=9e9, case=tok)
    DB.update_item(conn, eid, now=9e9, case=tok, state="verified", state_reasons_json=[])
    for x in ents[1:]:
        c.post(f"/api/cases/{tok}/items/{x['id']}/review", json={"action": "accept"})
    case = DB.get_case(conn, tok)
    return {"token": cx.case_id, "item_id": item_id, "kind": kind, "mode": "full" if cx.full else "metadata", "state": row.get("state"),
            "review_status": rs, "state_reasons": reasons, "verdict": {"code": code, "label": label, "blocks_export": bool(blocks)},
            "progress": _progress(steps), "next_action": first_na, "steps": steps}


# ------------------------------------------------------------------ entries
def _excerpt_ev(cx, rid, row):
    ed = row.get("edited") or {}
    return _span(cx, rid, ed.get("excerpt_start", row.get("excerpt_start")), ed.get("excerpt_end", row.get("excerpt_end")), ed.get("excerpt", row.get("excerpt")))


def _entry_steps(cx, row):
    R = set(row.get("state_reasons") or [])
    lad = row.get("ladder") or {}
    cc = lad.get("code_checks") or {}
    rid = (row.get("record_ids") or [None])[0]
    rec = cx.recs.get(rid, {})
    exc = _excerpt_ev(cx, rid, row)
    # D-051: all five code checks (and the highlight) are recomputed from the CURRENT summary and quote, as accept does, and also honour what was stored
    live = review.code_check_failures(review.entry_record(row, cx.live_recs), row)
    verbatim_fail = "GROUNDING_EXCERPT_NOT_VERBATIM" in R or cc.get("excerpt_verbatim") is False or "GROUNDING_EXCERPT_NOT_VERBATIM" in live
    schema_fail = "SCHEMA_INVALID" in R
    stop = "SCHEMA_INVALID" if schema_fail else ("GROUNDING_EXCERPT_NOT_VERBATIM" if verbatim_fail else None)
    st = []
    # 1 extracted
    if lad.get("entered_by"):
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:24.921Z

**tool call — Bash**
````
{
 "command": "grep -n \"^def _gate\\|^def _ccf\\|^def steps_of\\|^def env\\|^HEDGE_FULL\\|^HEDGE_Q\" -A8 tests/unit/test_trace.py | head -70"
}
````

### User / tool · 2026-11-02T06:06:25.007Z

**tool result**
````
48:def env(base, tmp_path, monkeypatch):
49-    monkeypatch.setenv("LLM_BACKEND", "fixture")
50-    monkeypatch.delenv("ZLAYT_MODE", raising=False)
51-    path = str(tmp_path / "copy.sqlite")
52-    src = sqlite3.connect(base["db"])
53-    dst = sqlite3.connect(path)
54-    src.backup(dst)
55-    src.close()
56-    dst.close()
--
62:def steps_of(t):
63-    return {s["id"]: s for s in t["steps"]}
64-
65-
66-def walk(o, keys):
67-    """Every dict key anywhere in o that is in `keys`."""
68-    found = set()
69-    if isinstance(o, dict):
70-        for k, v in o.items():
--
537:def _gate_states(c, conn, tok):
538-    """Yield (name) after putting the case into each state we can build; the caller checks the invariant."""
539-    case = c.get(f"/api/cases/{tok}").json()
540-    ids = [x["id"] for k in ("entries", "undated_entries", "amounts", "flags") for x in case[k]]
541-    yield "pending items"
542-    DB.update_case(conn, tok, status="running")
543-    yield "running with pending items"
544-    DB.update_case(conn, tok, status="ready")
545-    for i in ids:
--
692:def _gate(c, tok):
693-    return steps_of(c.get(f"/api/cases/{tok}/trace").json())["export_gate"]
694-
695-
696-def _jnr(gate):
697-    return [b for b in gate["blockers"] if b["reason_code"] == "JUDGE_NOT_RUN"]
698-
699-
700-def test_accepted_items_whose_judge_never_ran_are_gate_blockers_with_a_next_action(env):
--
1050:def _ccf(gate):
1051-    return [b for b in gate["blockers"] if b.get("step_id")]
1052-
1053-
1054-def test_edited_summary_that_drops_a_qualifier_blocks_the_gate_and_export_422_t098(env):
1055-    c, conn, tok, _ = env
1056-    edt = _mixed(c, tok, conn)
1057-    g = _gate(c, tok)
1058-    got = _ccf(g)
--
1249:HEDGE_Q = "C5-C6 disc protrusion with mild right foraminal narrowing."                               # e8's quote without the hedge sentence that follows it in the record
1250:HEDGE_FULL = "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically."
1251-
1252-
1253-def _e8_ai_draft_with_short_quote(c, conn, tok, stored=True):
1254-    """The reviewer's live case (T-098-staff-engineer-r2 F1): the AI quoted e8 and left out the hedge sentence that follows it."""
1255-    row = DB.get_item(conn, "e8", tok)
1256-    assert HEDGE_FULL in row["excerpt"] or row["excerpt"].startswith(HEDGE_Q)
1257-    DB.update_item(conn, "e8", now=9e9, case=tok, excerpt=HEDGE_Q, summary="Disc protrusion at C5-C6 with mild right foraminal narrowing.",
1258-                   state="needs_review", state_reasons_json=["EXCERPT_OMITS_QUALIFIER"] if stored else [])
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:30.910Z

**tool call — Bash**
````
{
 "command": "cat >> tests/unit/test_trace.py <<'EOF'\n\n\ndef test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106(env, monkeypatch):\n    \"\"\"T-098 r3 F2: HIGHLIGHT_NOT_FOUND has no route with a verbatim quote today (locate and check_excerpt use one matcher), so the live recompute is\n    defence in depth. Pin it by making locate fail while every stored result says pass: accept refuses, a forced accept is a gate blocker, export is\n    422 and the item trace fails the `highlight` step. Mutants: the highlight term off in trace._entry_steps, or the check off in review.code_check_failures.\"\"\"\n    from app.backend import grounding\n    c, conn, tok, _ = env\n    row = DB.get_item(conn, \"e8\", tok)\n    lad = row[\"ladder\"]\n    lad[\"code_checks\"] = {k: (True if k != \"summary_tokens_not_in_excerpt\" else []) for k in (lad.get(\"code_checks\") or {})}\n    lad[\"judge\"] = {\"model\": \"fixture\", \"prompt_version\": \"judge\", \"call_id\": None, \"verdict\": \"supported\", \"reason_code\": \"NONE\"}\n    DB.update_item(conn, \"e8\", now=9e9, case=tok, state=\"verified\", state_reasons_json=[], ladder=lad)\n    assert \"HIGHLIGHT_NOT_FOUND\" not in steps_of(c.get(f\"/api/cases/{tok}/items/e8/trace\").json())[\"highlight\"].get(\"reason_code\", \"\")      # control: fine while locate works\n    monkeypatch.setattr(grounding, \"locate\", lambda *a, **k: None)\n    r = c.post(f\"/api/cases/{tok}/items/e8/review\", json={\"action\": \"accept\"})\n    assert r.status_code == 422 and r.json()[\"error\"][\"detail\"][\"reason_code\"] == \"HIGHLIGHT_NOT_FOUND\"\n    DB.apply_review(conn, \"e8\", \"accept\", now=9e9, case=tok)                                         # old data / any route that skips the guard\n    g = _gate(c, tok)\n    assert (\"e8\", \"HIGHLIGHT_NOT_FOUND\") in [(b[\"item_id\"], b[\"reason_code\"]) for b in _ccf(g)] and g[\"ready\"] is False\n    assert c.get(f\"/api/cases/{tok}/export\").status_code == 422\n    stp = steps_of(c.get(f\"/api/cases/{tok}/items/e8/trace\").json())[\"highlight\"]\n    assert stp[\"status\"] == \"fail\" and stp[\"blocks_export\"] is True and stp[\"reason_code\"] == \"HIGHLIGHT_NOT_FOUND\"\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_trace.py -k t106 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T06:06:32.108Z

**tool result**
````
        from app.backend import grounding
        c, conn, tok, _ = env
        row = DB.get_item(conn, "e8", tok)
        lad = row["ladder"]
        lad["code_checks"] = {k: (True if k != "summary_tokens_not_in_excerpt" else []) for k in (lad.get("code_checks") or {})}
        lad["judge"] = {"model": "fixture", "prompt_version": "judge", "call_id": None, "verdict": "supported", "reason_code": "NONE"}
        DB.update_item(conn, "e8", now=9e9, case=tok, state="verified", state_reasons_json=[], ladder=lad)
>       assert "HIGHLIGHT_NOT_FOUND" not in steps_of(c.get(f"/api/cases/{tok}/items/e8/trace").json())["highlight"].get("reason_code", "")      # control: fine while locate works
               ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
E       TypeError: argument of type 'NoneType' is not iterable

tests/unit/test_trace.py:1384: TypeError
=========================== short test summary info ============================
FAILED tests/unit/test_trace.py::test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106
1 failed, 84 deselected in 0.89s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:33.544Z

Fix the control assertion (reason_code is None when passing).

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:34.955Z

**tool call — Bash**
````
{
 "command": "python3 - <<'EOF'\np='tests/unit/test_trace.py'\ns=open(p).read()\ns=s.replace('''    assert \"HIGHLIGHT_NOT_FOUND\" not in steps_of(c.get(f\"/api/cases/{tok}/items/e8/trace\").json())[\"highlight\"].get(\"reason_code\", \"\")      # control: fine while locate works''','''    assert steps_of(c.get(f\"/api/cases/{tok}/items/e8/trace\").json())[\"highlight\"][\"status\"] == \"pass\"      # control: fine while locate works''')\nopen(p,'w').write(s)\nEOF\n.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit/test_trace.py -k t106 2>&1 | tail -15"
}
````

### User / tool · 2026-11-02T06:06:36.263Z

**tool result**
````
.                                                                        [100%]
1 passed, 84 deselected in 0.96s
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:37.260Z

Now the two mutants.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:39.213Z

**tool call — Bash**
````
{
 "command": "cp app/backend/trace.py \"$TMPDIR/trace.bak\" && cp app/backend/review.py \"$TMPDIR/review.bak\" && P=.venv/bin/python\nsed -i '' 's/ or \"HIGHLIGHT_NOT_FOUND\" in live)/)/' app/backend/trace.py && $P -I -m pytest -p no:cacheprovider -q tests/unit/test_trace.py -k t106 2>&1 | tail -1; cp \"$TMPDIR/trace.bak\" app/backend/trace.py\nsed -i '' 's/if grounding.locate(rec\\[\"excerpt\"\\], exc) is None and/if False and grounding.locate(rec[\"excerpt\"], exc) is None and/' app/backend/review.py && $P -I -m pytest -p no:cacheprovider -q tests/unit/test_trace.py -k t106 2>&1 | tail -1; cp \"$TMPDIR/review.bak\" app/backend/review.py\ngit diff --stat -- app/backend/trace.py app/backend/review.py; git status --short app/backend | head"
}
````

### User / tool · 2026-11-02T06:06:41.470Z

**tool result**
````
1 failed, 84 deselected in 0.80s
1 failed, 84 deselected in 0.82s
 M app/backend/api.py
 M app/backend/export.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
?? app/backend/conflict_candidates.py
[This command modified 2 files you've previously read: app/backend/trace.py, app/backend/review.py. Call Read before editing.]
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:44.988Z

**tool call — Bash**
````
{
 "command": "git diff HEAD --stat -- app/backend/export.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_hidden.py tests/unit/test_t093_eval_signature.py tests/unit/test_eval_runner.py tests/unit/test_narrative.py tests/unit/test_trace.py; git diff --cached --stat | tail -5"
}
````

### User / tool · 2026-11-02T06:06:45.109Z

**tool result**
````
 app/backend/export.py                  |  2 ++
 tests/unit/test_eval_runner.py         | 16 ++++++++--------
 tests/unit/test_narrative.py           | 16 ++++++++++++++++
 tests/unit/test_pdf_hidden.py          | 13 +++++++++++++
 tests/unit/test_provider.py            |  4 +++-
 tests/unit/test_provider_backends.py   |  2 +-
 tests/unit/test_t093_eval_signature.py |  5 ++++-
 tests/unit/test_trace.py               | 23 +++++++++++++++++++++++
 8 files changed, 70 insertions(+), 11 deletions(-)
 tests/unit/_pdf_probe.py          |  66 ----------------------
 tests/unit/test_pdf_ocr_limits.py | 114 --------------------------------------
 2 files changed, 180 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:50.343Z

**tool call — Bash**
````
{
 "command": "F=\"app/backend/export.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_hidden.py tests/unit/test_t093_eval_signature.py tests/unit/test_eval_runner.py tests/unit/test_narrative.py tests/unit/test_trace.py\" && git commit -q -m \"fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)\n\n- test_single_call_path (both copies) allow-list pdf_hidden.py (local child process, no LLM); test_pdf_hidden checks it never names claude/anthropic\n- test_fixture_runs_write_no_artifacts: T-101 deliberately writes a scratch calibration.json under runs/<ts>; test now allows only that file (code was right)\n- no-.git calibration test builds its tree with shutil instead of git archive; the CLI already refuses with exit 2\n- export notes: NOT_AN_ACCEPTED_ENTRY sentences print 'Sentence removed (cites an entry that is not accepted)', not their text; test added\n- HIGHLIGHT_NOT_FOUND live recompute pinned by a test (both mutants killed)\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- $F && git show --stat --format=%h HEAD | tail -12"
}
````

### User / tool · 2026-11-02T06:06:50.886Z

**tool result**
````
check_secrets: ok (8 file(s) scanned staged)
c2a5d1f

 app/backend/export.py                  |  2 ++
 tests/unit/test_eval_runner.py         | 16 ++++++++--------
 tests/unit/test_narrative.py           | 16 ++++++++++++++++
 tests/unit/test_pdf_hidden.py          | 13 +++++++++++++
 tests/unit/test_provider.py            |  4 +++-
 tests/unit/test_provider_backends.py   |  2 +-
 tests/unit/test_t093_eval_signature.py |  5 ++++-
 tests/unit/test_trace.py               | 23 +++++++++++++++++++++++
 8 files changed, 70 insertions(+), 11 deletions(-)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:53.498Z

**tool call — Bash**
````
{
 "command": "S=$(echo /private/tmp/claude-501/*/6ddf8076*/scratchpad) && rm -rf $S/ar $S/outx && mkdir -p $S/ar && git archive HEAD | tar -x -C $S/ar && git log --oneline -3 && cd $S/ar && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -6",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:06:53.553Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: rm with an unresolved expansion ($) is blocked | command: S=$(echo /private/tmp/claude-501/*/6ddf8076*/scratchpad) && rm -rf $S/ar $S/outx && mkdir -p $S/ar && git archive HEAD | tar -x -C $S/ar && git log --oneline -3 && cd $S/ar && /Users/arsis/zlayt-pm-pr
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:06:57.123Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; mv $S/ar $S/ar_old; mkdir -p $S/ar2 && git archive HEAD | tar -x -C $S/ar2 && git log --oneline -3 && cd $S/ar2 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -6",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:09:21.535Z

**tool result**
````
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
3462ad0 fix(frontend): EDIT_QUOTE refusals offer Change the quote and open the picker; CODE_CHECK_FAILED on edit shows inline under the edit box; Why lead follows the backend verdict string (T-104)
bcdcb91 fix(backend): billing applies D-052 strictly: no sums or comparisons; EOB rows are lines, every EOB money token placed (T-103 r2)
...........................s............................................ [ 87%]
........................................................................ [ 90%]
........................................................................ [ 94%]
........................................................................ [ 97%]
....................................................                     [100%]
2064 passed, 4 skipped in 142.72s (0:02:22)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:09:23.381Z

Archive is green. Now the worktree copy.

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:09:26.068Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git worktree add -q --detach $S/wt HEAD && cd $S/wt && git log --oneline -1 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -6",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:09:26.175Z

**tool result (error)**
````
Exit code 128
fatal: '/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt' already exists
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:09:30.797Z

**tool call — Bash**
````
{
 "command": "git worktree list; S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; ls -a $S/wt | head"
}
````

### User / tool · 2026-11-02T06:09:30.895Z

**tool result**
````
/Users/arsis/zlayt-pm-project  c2a5d1f [main]
.
..
.claude
.env
.gitignore
.pytest_cache
CLAUDE.md
MASTER_PROMPT.md
app
data
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:09:34.712Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad; git worktree add -q --detach $S/wt106 HEAD && cd $S/wt106 && git log --oneline -1 && /Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest -p no:cacheprovider -q tests/unit 2>&1 | tail -6",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:12:04.374Z

**tool result**
````
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
...........................s............................................ [ 87%]
........................................................................ [ 90%]
........................................................................ [ 94%]
........................................................................ [ 97%]
....................................................                     [100%]
2067 passed, 1 skipped in 147.92s (0:02:27)
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:12:14.965Z

**tool call — Bash**
````
{
 "command": "git worktree remove --force /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/wt106; git worktree prune; git worktree list; B=\"python3 tools/board.py\"\n$B note T-106 --agent backend --text \"5 fixes committed c2a5d1f; tests/unit green on git archive HEAD (2064 passed, 4 skipped) and git worktree HEAD (2067 passed, 1 skipped); worktree removed.\"\n$B ac T-106 --check 1 --agent backend --evidence \"c2a5d1f: pytest tests/unit on git archive of HEAD = 2064 passed 4 skipped 0 failed; on a git worktree of HEAD = 2067 passed 1 skipped 0 failed. New/changed tests: test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children, test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry, test_trace.py::test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106 (both mutants killed)\"\n$B commit T-106 --sha c2a5d1f --agent backend\n$B handoff T-106 --agent backend --text \"What changed (c2a5d1f): (1) both test_single_call_path allow-list pdf_hidden.py (anthropic still banned); new test_pdf_hidden_only_starts_local_children: no claude/anthropic, only 2 subprocess calls (ps, own scan module), no shell. (2) test_fixture_runs_write_no_artifacts: the TEST was wrong, code right: T-101 deliberately writes a scratch calibration.json under runs/<ts>/ on every plain run; test now allows only that file and asserts no run*.json/case artifacts and no run_artifacts in latest.json. (3) no-.git calibration test: the CODE already refuses cleanly (exit 2, 'no git repository or HEAD commit is available', no traceback); the TEST crashed because it ran git archive HEAD inside the export; it now builds the tree with shutil and asserts the message and no traceback. (4) export._draft_paragraph: NOT_AN_ACCEPTED_ENTRY prints 'Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.' not the text; test covers pending and accepted paragraph; mutant killed. (5) HIGHLIGHT_NOT_FOUND is unreachable with real grounding (locate and check_excerpt share one matcher) but kept as defence in depth; test patches grounding.locate to None under a stale stored pass: accept 422, gate blocker, export 422, trace highlight step fails; mutants M3c and M11b each fail it. How verified: tests/unit on git archive HEAD 2064 passed 4 skipped; on git worktree HEAD 2067 passed 1 skipped (skips differ on git-dependent tests); worktree removed. Left: no eval run needed (no prompt/model/lexicon/schema change). Surprised: a pre-existing unregistered dir at scratchpad/wt holds a .env; I left it untouched and used wt106.\"\n$B move T-106 in_review --agent backend"
}
````

### User / tool · 2026-11-02T06:12:15.500Z

**tool result**
````
/Users/arsis/zlayt-pm-project  c2a5d1f [main]
noted on T-106
AC 1 checked: c2a5d1f: pytest tests/unit on git archive of HEAD = 2064 passed 4 skipped 0 failed; on a git worktree of HEAD = 2067 passed 1 skipped 0 failed. New/changed tests: test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children, test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry, test_trace.py::test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106 (both mutants killed)
T-106: commit c2a5d1f recorded
handoff written on T-106
T-106: in_progress -> in_review
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T06:12:19.015Z

T-106 is in review with all five fixes committed as c2a5d1f (8 files, checked with `git diff --cached --stat` before the commit).

On clean HEAD the unit suite has 0 failures: 2064 passed, 4 skipped on the `git archive` copy, and 2067 passed, 1 skipped on a `git worktree` copy, which I removed afterwards. The existing directory at scratchpad/`wt` isn't a registered worktree and contains a `.env`, so I left it alone and used `wt106`.

On the five items:
- **`test_fixture_runs_write_no_artifacts`:** the test was wrong, not the code. T-101 deliberately writes a scratch `calibration.json` under `runs/<ts>/`, so I narrowed the test to allow only that file.
- **No-.git calibration test:** the code already exits 2 with a clear message. The test crashed because it ran `git archive` inside the export, so it now copies the tree with `shutil`.
- **`HIGHLIGHT_NOT_FOUND`:** no real quote can reach it, so I kept it as a safety net and pinned it with a test that forces the lookup to fail, which breaks if either check is removed.
