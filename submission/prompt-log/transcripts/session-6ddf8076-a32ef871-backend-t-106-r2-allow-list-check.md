# Subagent: Backend: T-106 r2 allow-list check (Backend: T-106 r2 allow-list check)

Source: `agent-a32ef8718e1c15bda.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T06:20:49.275Z

You own board card T-106, round 2 (claimed by "backend") in /Users/arsis/zlayt-pm-project. Read reviews/T-106-staff-engineer.md and the orchestrator decision note on the card (`python3 tools/board.py show T-106`): the narrative-panel major is accepted as intended, because the UI is paralegal-only and labeled removed.

Fix the other major. The pdf_hidden allow-list check in test_single_call_path can be bypassed. Make it robust:
- check with the AST, not string matching, that pdf_hidden.py and pdf_ocr.py never import or call anything related to claude, anthropic or app.llm;
- check that any subprocess call's argv[0] is the Python interpreter running their own child module, or tesseract.
Use the reviewer's bypass examples as tests that must fail the check.

Run `.venv/bin/python -m pytest -q tests/unit`, and check it's green on a `git archive HEAD` copy. Commit with `git add <paths>` and then `git commit -m "..." -- <paths>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-106 in_review --agent backend`. Reply in 1 line.

### User / tool · 2026-11-02T06:20:49.283Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-haiku-5-5 · 2026-11-02T06:20:51.822Z

**tool call — mcp__ccd_turn__update_plan**
````
{
 "items": [
  {
   "content": "Read T-106 card, review, and test file",
   "status": "in_progress"
  },
  {
   "content": "Rewrite pdf_hidden allow-list check with AST",
   "status": "pending"
  },
  {
   "content": "Add bypass-example tests that must fail the check",
   "status": "pending"
  },
  {
   "content": "Run unit tests and check git archive HEAD copy",
   "status": "pending"
  },
  {
   "content": "Commit, ac, handoff, move in_review",
   "status": "pending"
  }
 ],
 "scope": "first_task"
}
````

### User / tool · 2026-11-02T06:20:51.825Z

**tool result (error)**
````
PreToolUse:mcp__ccd_turn__update_plan hook error: Not shown: you are a subagent, and the app shows only the main conversation's task list and wrap-up. Do not call update_plan or wrap_up again; carry on with your task and report your result as usual.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:20:52.282Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-106 && echo ---- && cat reviews/T-106-staff-engineer.md && echo ---- && grep -rn \"pdf_hidden\" tests/unit | head -50",
 "description": "Show card, review, and pdf_hidden test references"
}
````

### User / tool · 2026-11-02T06:20:52.433Z

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
updated_at: "2026-11-02T06:20:44Z"
claimed_by: "backend"
claimed_at: "2026-11-02T06:20:44Z"
rounds: 1
commits: ["c2a5d1f"]
reviews:
  - {"persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5", "verdict": "changes", "file": "reviews/T-106-staff-engineer.md", "at": "2026-11-02T06:20:44Z"}
ac:
  - {"n": 1, "text": "On a git-archive copy of HEAD (plus a git-init variant where needed) tests/unit is fully green; test_single_call_path allow-lists pdf_hidden (local, no LLM) with a check it never calls claude; test_fixture_runs_write_no_artifacts fixed at its cause; no-.git calibration test skips cleanly or works; internal notes never print a narrative sentence that was not code-checked (NOT_AN_ACCEPTED_ENTRY); a test pins the HIGHLIGHT_NOT_FOUND recompute or the dead code is removed", "done": true, "evidence": "c2a5d1f: pytest tests/unit on git archive of HEAD = 2064 passed 4 skipped 0 failed; on a git worktree of HEAD = 2067 passed 1 skipped 0 failed. New/changed tests: test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children, test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry, test_trace.py::test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106 (both mutants killed)"}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T06:01:47Z backend: claimed
- 2026-11-02T06:12:15Z backend: 5 fixes committed c2a5d1f; tests/unit green on git archive HEAD (2064 passed, 4 skipped) and git worktree HEAD (2067 passed, 1 skipped); worktree removed.
- 2026-11-02T06:12:15Z backend: AC 1 checked: c2a5d1f: pytest tests/unit on git archive of HEAD = 2064 passed 4 skipped 0 failed; on a git worktree of HEAD = 2067 passed 1 skipped 0 failed. New/changed tests: test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children, test_narrative.py::test_internal_notes_never_print_a_sentence_that_cites_a_non_accepted_entry, test_trace.py::test_highlight_not_found_is_recomputed_live_by_accept_gate_and_trace_t106 (both mutants killed)
- 2026-11-02T06:12:15Z backend: moved in_progress -> in_review
- 2026-11-02T06:12:23Z orchestrator: review dispatched: staff-engineer-reviewer
- 2026-11-02T06:20:44Z orchestrator: review staff-engineer-reviewer (claude-haiku-5-5): changes — reviews/T-106-staff-engineer.md; round 1; findings:
    - [major] pdf_hidden subprocess allow-list is not enforced as narrow; a from-subprocess-import spawn passes all three tests — fix: Replace the regex with an ast walk over app/backend/pdf_hidden.py: fail on `import subprocess as X` and on `from subprocess import ...`, collect every Call whose func is subprocess.run/Popen/call/check_output/check_call, and assert each argv[0] is the literal "ps" 
    - [major] The notes-only fix leaves unchecked removed-sentence wording on the paralegal panel and in the API — fix: Either (a) drop text for reason NOT_AN_ACCEPTED_ENTRY in narrative.py:159 and render the same phrase used at export.py:549 in narrative.js:63, or (b) record a scope cut in memory/SCOPE_CUTS.md saying the panel shows unchecked wording on purpose and why. Orchestrator decides; the 
    - [minor] Fixture-run artifact filter accepts calibration.json at any depth under runs/ and does not require exactly one scratch file — fix: scratch = [f for f in files if re.fullmatch(r"[^/]+/calibration\.json", f)]; assert len(scratch) == 1 and that no other file exists under runs/.
- 2026-11-02T06:20:44Z backend: claimed
- 2026-11-02T06:20:44Z orchestrator: Decision: the narrative panel (UI, paralegal-only, labeled removed) may show a removed sentence so the paralegal can see what was cut; only the export/notes must withhold it. Round 2 = make the pdf_hidden allow-list check non-bypassable.

## Handoff
What changed (c2a5d1f): (1) both test_single_call_path allow-list pdf_hidden.py (anthropic still banned); new test_pdf_hidden_only_starts_local_children: no claude/anthropic, only 2 subprocess calls (ps, own scan module), no shell. (2) test_fixture_runs_write_no_artifacts: the TEST was wrong, code right: T-101 deliberately writes a scratch calibration.json under runs/<ts>/ on every plain run; test now allows only that file and asserts no run*.json/case artifacts and no run_artifacts in latest.json. (3) no-.git calibration test: the CODE already refuses cleanly (exit 2, 'no git repository or HEAD commit is available', no traceback); the TEST crashed because it ran git archive HEAD inside the export; it now builds the tree with shutil and asserts the message and no traceback. (4) export._draft_paragraph: NOT_AN_ACCEPTED_ENTRY prints 'Sentence removed (cites an entry that is not accepted) (e99): NOT_AN_ACCEPTED_ENTRY.' not the text; test covers pending and accepted paragraph; mutant killed. (5) HIGHLIGHT_NOT_FOUND is unreachable with real grounding (locate and check_excerpt share one matcher) but kept as defence in depth; test patches grounding.locate to None under a stale stored pass: accept 422, gate blocker, export 422, trace highlight step fails; mutants M3c and M11b each fail it. How verified: tests/unit on git archive HEAD 2064 passed 4 skipped; on git worktree HEAD 2067 passed 1 skipped (skips differ on git-dependent tests); worktree removed. Left: no eval run needed (no prompt/model/lexicon/schema change). Surprised: a pre-existing unregistered dir at scratchpad/wt holds a .env; I left it untouched and used wt106.

----
# T-106 review: staff-engineer-reviewer (commit c2a5d1f)

**Verdict: changes** (0 blockers, 2 majors, 3 minors/nits). Deterministic checks pass: the unit suite on a clean `git archive` of HEAD is green on two runs (2064 passed, 4 skipped, 0 failed). The problems are in the fixes themselves. The pdf_hidden allow-list is narrower on paper than in the test, and the "notes never print unchecked wording" fix stops at the notes while the paralegal panel and the API still print the same sentence text.

## Deterministic checks

- Clean-HEAD suite: `git archive c2a5d1f` extracted to a scratch dir with no `.git` (`git rev-parse --git-dir` returned "fatal: not a git repository"). `.venv/bin/python -m pytest -q tests/unit` gave `2064 passed, 4 skipped in 144.17s`, exit 0. A second run with `-rs` gave `2064 passed, 4 skipped in 141.44s`, exit 0, so it reproduces.
- Skips: `tests/unit/test_eval_runner.py:794` (x2, "no git repository here (exported tree)"), `:819` ("no git repository here"), and `tests/unit/test_spanish_failsafe.py:223` (env-gated live judge eval). None are failures.
- Mutants, in scratch copies only (the project tree was not edited):
  - trace highlight live term removed (`trace.py:370`): killed at `test_trace.py:1390`.
  - accept-gate recompute disabled (`review.py:98`): killed at `test_trace.py:1387`.
  - NOT_AN_ACCEPTED_ENTRY export branch disabled (`export.py:548`): killed at `test_narrative.py:288`.
  - plain run also writes the committed `calibration.json` (`evals/run.py:1051`): `test_fixture_runs_write_no_artifacts` survives, `test_plain_run_leaves_committed_calibration_json_untouched` kills it. The fixture test is not the guard for this invariant, and another test is.
  - pdf_hidden spawns via `from subprocess import run` (new call not in the test's regex): all three allow-list tests pass (F1).
  - pdf_hidden names `claude`: killed at `test_pdf_hidden.py` (the claude-name assertion).
- No-git CLI: `env -u LLM_BACKEND -u ENABLE_LIVE .venv/bin/python -m evals.run --write-calibration --out <dir>` in the archive gave exit 2 and stderr `evals.run: --write-calibration refused, nothing was run or written: no git repository or HEAD commit is available to name as the source.` Nothing was written.
- Added lines in the commit grepped for `except`, `float(`, `sleep(`, `retry`, model ids and `.env`: no matches.
- No eval re-run: the commit touches no prompt, model, lexicon or schema.

## Findings

**F1 (major): the pdf_hidden allow-list is not narrow in what it enforces.** `test_provider.py:123` exempts the whole file from the subprocess rule. `test_pdf_hidden.py:107-109` only counts literal `subprocess.<fn>([...` calls. A `from subprocess import run` call is invisible to that count, so the "every call starts ps or sys.executable" docstring (`test_pdf_hidden.py:100-103`) is not enforced. The probe mutant passed all three allow-list tests. The claude-name check is a word grep and does work.

**F2 (major): unchecked wording is still printed on the paralegal's screen.** `app/frontend/narrative.js:63` renders `"“" + r.text + "” — "` for every removed item, including NOT_AN_ACCEPTED_ENTRY. `app/backend/narrative.py:159` returns `text` for every reason. T-098 r3 recorded this same leftover class. The commit fixes only the notes (`export.py:548-549`). The AC wording ("internal notes") is met, but the rationale is not. The text is labelled "removed" and stays out of the letter, so I rate this major, not blocker. The UI was not run (no app URL in scope); this is from code reading.

**F3 (minor): the fixture-run filter is looser than the AC.** `test_t093_eval_signature.py:171` allows any file whose path ends in `/calibration.json`, at any depth under `runs/`. The AC says only the scratch file directly under `runs/<ts>/`. Not mutated; read from the code.

**F4 (nit): the NOT_AN_ACCEPTED_ENTRY note is false for translated entries.** `narrative.py:78` drops translated entries from `by_id`, so `narrative.py:99-100` labels a citation of an accepted translated entry as "not accepted". Reachable only if the model cites an id outside the prompt.

**F5 (nit): judge-failed wording is still printed in the notes.** `export.py:551` prints `Removed: "<text>"` for JUDGE_* reasons (`narrative.py:113`). Those sentences passed the code checks, so D-051 and the AC do not cover them. I would still treat them like F2 for consistency.

**F6 (nit): "fully green" on an archive skips two provenance tests.** `test_eval_runner.py:794` and `:819` do not run without `.git`. The card's worktree run covers them, so the AC holds.

## Right

- The archive suite reproduces: 2064 passed, 4 skipped, 0 failed, twice.
- The no-git refusal is explicit: exit 2, a clear message, nothing written, and the test checks the message and the absence of a traceback.
- The HIGHLIGHT_NOT_FOUND test has a control assertion and kills both live-recompute mutants.

## Not exercised

No app URL in scope, so the UI was not run. The project working tree is dirty (`git status --short` lists uncommitted edits, e.g. `app/backend/api.py`, `flags.py`, `judges.py`, `pdf_checks.py`), so no project-tree result is cited here.

```json
{"card": "T-106", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit c2a5d1f (HEAD); git archive copy with no .git (scratchpad T106_head_archive); files app/backend/export.py and tests/unit/test_eval_runner.py, test_narrative.py, test_pdf_hidden.py, test_provider.py, test_provider_backends.py, test_t093_eval_signature.py, test_trace.py; no app URL; no sample-case run (no prompt, model, lexicon or schema change)",
 "exercised": [
   "read personas/staff-engineer.md and board show T-106 (status in_review, AC 1 done)",
   "git show --stat and full git show c2a5d1f -- app tests/unit (8 files, +70/-11)",
   "git archive c2a5d1f | tar -x into scratchpad T106_head_archive; git rev-parse --git-dir -> fatal: not a git repository",
   ".venv/bin/python -m pytest -q tests/unit in the archive, two runs: 2064 passed, 4 skipped, 0 failed (second run with -rs; skips test_eval_runner.py:794 x2, :819, test_spanish_failsafe.py:223)",
   "read narrative.py draft (75-119), export.py _draft_paragraph (540-552), review.py code_check_failures (81-103) and accept guard (245-257), trace.py highlight steps (369-370, 611-612), evals/run.py git_source (75-96), write_calibration_refusal (1020-1029), write_report (1034-1057), CLI refusal (1186-1192), pdf_hidden.py subprocess calls (513, 558), app/frontend/narrative.js (61-63), narrative.py:159",
   "mutants in scratch copies, one per check: trace.py:370 live term (killed test_trace.py:1390); review.py:98 recompute (killed test_trace.py:1387); export.py:548 branch (killed test_narrative.py:288); evals/run.py:1051 root calibration write (fixture test survives, calibration-untouched test kills); pdf_hidden from-subprocess-import probe (3 allow-list tests pass); pdf_hidden claude-name probe (killed)",
   "no-git CLI: .venv/bin/python -m evals.run --write-calibration --out <dir> in the archive -> exit 2, 'no git repository or HEAD commit is available to name as the source', nothing written",
   "grep of added lines in c2a5d1f for except, float(, sleep(, retry, model ids, .env -> no matches",
   "git status --short in the project tree (dirty; no project-tree results cited)"
 ],
 "verdict": "changes",
 "scores": {"clean_head_suite_green": 5, "fixes_not_weakened": 3, "allow_list_narrowness": 2, "no_silent_fallback_or_swallowed_error": 5, "notes_never_print_unchecked_wording": 3, "highlight_safety_net_pinned": 5},
 "findings": [
   {"severity": "major", "title": "pdf_hidden subprocess allow-list is not enforced as narrow; a from-subprocess-import spawn passes all three tests",
    "evidence": "tests/unit/test_provider.py:123 allow_subprocess = {\"backend/pdf_ocr.py\", \"backend/pdf_hidden.py\"} exempts the whole file; tests/unit/test_pdf_hidden.py:107-109 counts only literal subprocess.<fn>([ calls (len(calls) == 2) and checks argv[0]. Repro: scratch copy with `from subprocess import run as _sp_run` and an uncalled `_sp_run([\"/usr/bin/curl\", \"-s\", \"https://example.invalid/x\"], capture_output=True)` appended to app/backend/pdf_hidden.py; .venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children tests/unit/test_provider.py::test_single_call_path tests/unit/test_provider_backends.py::test_single_call_path -> 3 passed. The claude-name assertion (test_pdf_hidden.py:~111) does fail on a probe `_CMD_PROBE = [\"claude\", \"-p\"]`.",
    "why_it_matters": "AC 1 asks for a narrow allow-list. The file-level exemption lets pdf_hidden.py start processes, and the only narrowing is a regex. Any spawn written without the literal form passes, so the docstring claim (every subprocess call is ps or this interpreter) is false assurance.",
    "fix": "Replace the regex with an ast walk over app/backend/pdf_hidden.py: fail on `import subprocess as X` and on `from subprocess import ...`, collect every Call whose func is subprocess.run/Popen/call/check_output/check_call, and assert each argv[0] is the literal \"ps\" or sys.executable. Keep the claude/anthropic word check and add an assertion that the file imports nothing from app.llm.",
    "acceptance_test": "Apply the probe above to a scratch copy: tests/unit/test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children must fail there and pass on HEAD."},
   {"severity": "major", "title": "The notes-only fix leaves unchecked removed-sentence wording on the paralegal panel and in the API",
    "evidence": "app/frontend/narrative.js:63: el(\"li\", {}, \"“\" + r.text + \"” — \" + (r.message || r.reason), ...) renders every removed item, including NOT_AN_ACCEPTED_ENTRY. app/backend/narrative.py:159: \"removed\": [{\"text\": r[\"text\"], ...} for r in nar.get(\"removed\", [])] returns the text for every reason. The commit changes only app/backend/export.py:548-549. Recorded leftover class: memory project_t098_r3_review_patterns (T-098 r3, unchecked removed narrative text still printed).",
    "why_it_matters": "The card's rationale is that a sentence citing a non-accepted entry was never code-checked, so its wording must not be printed. The panel the paralegal reads prints exactly that wording. The AC is literally met (it says internal notes), so this is a partial fix of a recorded finding. Not a blocker: the text is labelled removed and export tests show it stays out of letter_text and the notes.",
    "fix": "Either (a) drop text for reason NOT_AN_ACCEPTED_ENTRY in narrative.py:159 and render the same phrase used at export.py:549 in narrative.js:63, or (b) record a scope cut in memory/SCOPE_CUTS.md saying the panel shows unchecked wording on purpose and why. Orchestrator decides; the gap is rated either way.",
    "acceptance_test": "Unit test on the narrative route after a draft that cites e99: the NOT_AN_ACCEPTED_ENTRY removed item carries no wording text. A DOM or E2E check that the narrative panel does not contain \"9/10 on the left\" for that case."},
   {"severity": "minor", "title": "Fixture-run artifact filter accepts calibration.json at any depth under runs/ and does not require exactly one scratch file",
    "evidence": "tests/unit/test_t093_eval_signature.py:171: assert [f for f in files if not f.endswith(\"/calibration.json\")] == []. A file runs/<ts>/case1/calibration.json passes. Read from code; not mutated.",
    "why_it_matters": "AC 1 says the test allows only the scratch calibration.json directly under runs/<ts>/. The current filter is looser than the AC states.",
    "fix": "scratch = [f for f in files if re.fullmatch(r\"[^/]+/calibration\\.json\", f)]; assert len(scratch) == 1 and that no other file exists under runs/.",
    "acceptance_test": "Scratch mutant writing runs/<ts>/x/calibration.json makes test_fixture_runs_write_no_artifacts fail."},
   {"severity": "nit", "title": "NOT_AN_ACCEPTED_ENTRY note text is false for an accepted entry filtered out as translated",
    "evidence": "app/backend/narrative.py:78 drops entries with translation_label from by_id; narrative.py:99-100 records a citation of such an entry as NOT_AN_ACCEPTED_ENTRY; app/backend/export.py:549 prints \"cites an entry that is not accepted\".",
    "why_it_matters": "The note says the entry is not accepted when it is accepted but outside the English draft. Reachable only if the model cites an id outside the prompt list (prompt_user, narrative.py:47-52).",
    "fix": "Use a separate reason or message for the translated case, or rephrase the note to 'cites an entry that is not in the English draft'.",
    "acceptance_test": "Draft with a sentence citing an accepted translated entry: the note text is true for that case."},
   {"severity": "nit", "title": "Judge-failed wording is still printed in the internal notes",
    "evidence": "app/backend/export.py:551: lines.append(f'- Removed: \"{r[\"text\"]}\" ({r[\"entry_id\"]}): {r[\"reason\"]}.') handles JUDGE_PARTIAL, JUDGE_UNSUPPORTED and JUDGE_UNAVAILABLE (app/backend/narrative.py:113). Those sentences passed the code checks, so D-051 and this AC do not cover them.",
    "why_it_matters": "Outside the AC. The same reasoning as F2 would apply for consistency. I would have done this differently; it is not a spec violation.",
    "fix": "Optional: print the phrase form for judge reasons too, matching F2's fix.",
    "acceptance_test": "Optional: export notes contain no removed-sentence wording for any removed reason."},
   {"severity": "nit", "title": "The archive's fully green run skips two provenance tests",
    "evidence": "pytest -rs in the archive: SKIPPED [2] tests/unit/test_eval_runner.py:794 (no git repository here (exported tree)) and SKIPPED [1] tests/unit/test_eval_runner.py:819 (no git repository here).",
    "why_it_matters": "Skips are not failures and the card's worktree run (2067 passed, 1 skipped) covers them, so the AC holds. Noting that an export alone does not exercise the committed calibration's provenance.",
    "fix": "None required. Keep the worktree run in the card evidence.",
    "acceptance_test": "Worktree of HEAD: pytest -q tests/unit/test_eval_runner.py runs the two tests and passes."}
 ],
 "whats_right": [
   "Clean-archive suite reproduces: 2064 passed, 4 skipped, 0 failed on two runs.",
   "The no-git CLI refusal is explicit: exit 2, a clear message, nothing written; the test checks the message and the absence of a traceback.",
   "The HIGHLIGHT_NOT_FOUND test has a control assertion and kills both live-recompute mutants (trace.py:370 and review.py:98)."
 ],
 "questions_for_chris": [
   "Is the paralegal narrative panel (app/frontend/narrative.js:63) inside the 'notes never print unchecked wording' rule? If not, it should be a recorded scope cut; the answer decides F2."
 ]}
```
----
tests/unit/test_pdf_checks_api.py:15:from tests.unit.test_pdf_hidden import HIDDEN, VISIBLE, pdf_with
tests/unit/test_pdf_hidden.py:5:from app.backend import pdf_checks, pdf_hidden, pdf_text
tests/unit/test_pdf_hidden.py:28:    scanned = pdf_hidden.scan(pdf_with(key))
tests/unit/test_pdf_hidden.py:35:    scanned = pdf_hidden.scan(build(text_page([VISIBLE, "Second visible line: ROM limited."])))
tests/unit/test_pdf_hidden.py:41:    assert pdf_hidden.scan(build(c))["pages"][1]["hidden"] == []
tests/unit/test_pdf_hidden.py:46:    assert pdf_hidden.scan(build(c))["pages"][1]["hidden"] == []
tests/unit/test_pdf_hidden.py:81:    out = pdf_hidden.remove_from_text("Visible A\nsomething the extractor spelled differently",
tests/unit/test_pdf_hidden.py:87:    assert pdf_hidden.remove_from_text("line one\nHIDDEN words\nline three", [{"text": "HIDDEN words", "reasons": []}], "") == "line one\nline three"
tests/unit/test_pdf_hidden.py:100:def test_pdf_hidden_only_starts_local_children():
tests/unit/test_pdf_hidden.py:101:    """The subprocess allow-list in test_provider.py covers pdf_hidden.py because it only starts local children and makes no LLM call: it never
tests/unit/test_pdf_hidden.py:105:    code = "\n".join(l for l in pathlib.Path(pdf_hidden.__file__).read_text().splitlines() if not l.lstrip().startswith(("#", '"""')))
tests/unit/test_pdf_hidden.py:109:    assert all(c.startswith('"ps"') or c.startswith('sys.executable, "-m", "app.backend.pdf_hidden"') for c in calls), calls
tests/unit/test_pdf_hidden_r3.py:13:from app.backend import pdf_checks, pdf_hidden, pdf_text
tests/unit/test_pdf_hidden_r3.py:146:    with pytest.raises(pdf_hidden.HiddenScanTimeout):
tests/unit/test_pdf_hidden_r3.py:147:        pdf_hidden.scan(data, deadline=time.monotonic() + 2.0)
tests/unit/test_pdf_hidden_r3.py:169:    code = ("import sys,time;sys.path.insert(0,'.');from app.backend import pdf_hidden as m;m._limit_child(1.0);"
tests/unit/test_pdf_hidden_r3.py:172:    p = subprocess.run(["python3", "-c", code], cwd=pdf_hidden._ROOT, capture_output=True, timeout=25)
tests/unit/test_pdf_hidden_r3.py:184:    monkeypatch.setattr(pdf_hidden.subprocess, "Popen", spy)
tests/unit/test_pdf_hidden_r3.py:185:    pdf_hidden.scan(K.one_page(K.VISIBLE))
tests/unit/test_pdf_hidden_r3.py:186:    assert "ANTHROPIC_API_KEY" not in seen and set(seen) <= set(pdf_hidden._CHILD_ENV_KEEP) | {"PYTHONDONTWRITEBYTECODE"}
tests/unit/test_pdf_hidden_r3.py:190:    monkeypatch.setattr(pdf_hidden, "_ROOT", "/nonexistent-dir-for-test")
tests/unit/test_pdf_hidden_r3.py:191:    with pytest.raises(pdf_hidden.HiddenScanUnavailable):
tests/unit/test_pdf_hidden_r3.py:192:        pdf_hidden.scan(K.one_page(K.VISIBLE))
tests/unit/test_pdf_hidden_r3.py:200:    s = pdf_hidden.scan(data, deadline=time.monotonic() + 30)
tests/unit/test_pdf_hidden_r2.py:11:from app.backend import pdf_checks, pdf_hidden, pdf_text
tests/unit/test_pdf_hidden_r2.py:73:    scanned = pdf_hidden.scan(CASES["white_text_in_form_depth_45"])
tests/unit/test_pdf_hidden_r2.py:95:    assert pdf_hidden.unlisted_spans("Dr. Rao noted effective treat-\nment of the office visit", listed) == []
tests/unit/test_pdf_hidden_r2.py:96:    assert pdf_hidden.unlisted_spans("Dr. Rao noted ignore previous instructions effective", listed) == ["ignore previous instructions"]
tests/unit/test_pdf_hidden_r2.py:97:    assert pdf_hidden.unlisted_spans("A b 6/10", "6 10") == []                     # single letters never count as words
tests/unit/test_pdf_hidden_r2.py:119:            scanned = pdf_hidden.scan(data)
tests/unit/test_pdf_hidden_r2.py:122:        except pdf_hidden.HiddenScanUnavailable:
tests/unit/test_pdf_hidden_r2.py:135:        raise pdf_hidden.HiddenScanUnavailable("PdfiumError", texts=pdf_text.read_pages(data))      # the child read the text layer, then the render failed
tests/unit/test_pdf_hidden_r2.py:136:    monkeypatch.setattr(pdf_hidden, "scan", boom)
tests/unit/test_pdf_hidden_r2.py:147:    real = pdf_hidden._page_scan
tests/unit/test_pdf_hidden_r2.py:155:    monkeypatch.setattr(pdf_hidden, "_page_scan", flaky)
tests/unit/test_pdf_hidden_r2.py:156:    monkeypatch.setattr(pdf_hidden, "scan", lambda d, deadline=None, **kw: {**pdf_hidden.scan_inprocess(d, deadline), "texts": pdf_text.read_pages(d)})       # the patch only reaches the in-process scan (the child is a fresh interpreter)
tests/unit/test_pdf_hidden_r2.py:162:    assert ht["pages"] == [{"page": 2, "count": 0, "items": [], "unchecked": True, "why": pdf_hidden.UNCHECKED_PLAIN["page_not_rendered"],
tests/unit/test_pdf_hidden_r2.py:168:    monkeypatch.setattr(pdf_hidden, "MAX_TEXT_OBJECTS", 50)
tests/unit/test_pdf_hidden_r2.py:169:    monkeypatch.setattr(pdf_hidden, "scan", lambda d, deadline=None, **kw: {**pdf_hidden.scan_inprocess(d, deadline), "texts": pdf_text.read_pages(d)})       # the patch only reaches the in-process scan
tests/unit/test_pdf_hidden_r2.py:171:    s = pdf_hidden.scan(data)
tests/unit/test_pdf_hidden_r2.py:179:    real = pdf_hidden.scan
tests/unit/test_pdf_hidden_r2.py:185:    monkeypatch.setattr(pdf_hidden, "scan", short)
tests/unit/test_pdf_hidden_r2.py:194:    with pytest.raises(pdf_hidden.HiddenScanTimeout):
tests/unit/test_pdf_hidden_r2.py:195:        pdf_hidden.scan(data, deadline=time.monotonic() + 0.5)
tests/unit/test_pdf_hidden_r2.py:197:    with pytest.raises(pdf_hidden.HiddenScanTimeout):
tests/unit/test_pdf_hidden_r2.py:198:        pdf_hidden.scan(data, deadline=time.monotonic() - 1)
tests/unit/test_pdf_hidden_r2.py:232:        raise pdf_hidden.HiddenScanUnavailable("PdfiumError", texts=pdf_text.read_pages(data))
tests/unit/test_pdf_hidden_r2.py:233:    monkeypatch.setattr(pdf_hidden, "scan", boom)
tests/unit/test_provider.py:121:    # And app/backend/pdf_hidden.py (T-087): it starts a local child process (this interpreter running its own scan module, plus a `ps` RSS probe)
tests/unit/test_provider.py:122:    # so a hung PDF renderer can be killed; no LLM. test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children checks it never names `claude`.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:20:54.313Z

**tool call — Bash**
````
{
 "command": "sed -n 90,130p tests/unit/test_pdf_hidden.py && echo ---- && sed -n 105,135p tests/unit/test_provider.py && echo ---- && grep -n \"subprocess\\|^import\\|^from\\|claude\\|anthropic\\|app.llm\" app/backend/pdf_hidden.py | head -60 && echo ---- && grep -n \"subprocess\\|^import\\|^from\" app/backend/pdf_ocr.py | head -30 && echo ---- && ls tests/unit | grep -i \"provider\" ",
 "description": "Inspect pdf_hidden test, provider test, and module imports"
}
````

### User / tool · 2026-11-02T06:20:54.435Z

**tool result**
````
def test_two_page_pdf_reports_only_the_page_with_hidden_text():
    two = build_pages([text_page([VISIBLE]), text_page(["Page two visible line."]) + b"\n" + HIDDEN["white"][0]])
    got = pdf_checks.extract(two)
    assert [p["page"] for p in got["pdf_checks"]["hidden_text"]["pages"]] == [2]
    assert "Page two visible line." in got["text"] and "PLANTED" not in got["text"]
    assert "PLANTED" not in pdf_checks.extract(two, include_hidden="1")["text"]       # confirming page 1 does not include page 2
    assert "PLANTED" in pdf_checks.extract(two, include_hidden="1,2")["text"]
    assert "PLANTED" in pdf_checks.extract(two, include_hidden="all")["text"]


def test_pdf_hidden_only_starts_local_children():
    """The subprocess allow-list in test_provider.py covers pdf_hidden.py because it only starts local children and makes no LLM call: it never
    names `claude` or the anthropic SDK, and every subprocess call starts either `ps` (RSS probe) or this interpreter running its own scan module."""
    import pathlib
    import re
    code = "\n".join(l for l in pathlib.Path(pdf_hidden.__file__).read_text().splitlines() if not l.lstrip().startswith(("#", '"""')))
    assert not re.search(r"claude|anthropic", code, re.I)
    calls = re.findall(r"subprocess\.(?:run|Popen|call|check_output|check_call)\(\[([^\]]+)\]", code)
    assert len(calls) == 2
    assert all(c.startswith('"ps"') or c.startswith('sys.executable, "-m", "app.backend.pdf_hidden"') for c in calls), calls
    assert not re.search(r"os\.system|shell\s*=\s*True|os\.exec|os\.spawn", code)
----
    def fake_run(argv, **kw):
        seen.update(kw)
        return subprocess.CompletedProcess(argv, 0, stdout='{"result": "{\\"summary\\": \\"ok\\"}", "is_error": false}', stderr="")
    monkeypatch.setattr(C.subprocess, "run", fake_run)
    monkeypatch.setenv("ANTHROPIC_API_KEY", "not-a-real-key")
    r = C.call("m", "s", "u", SCHEMA, key="k")
    assert r.output == {"summary": "ok"} and r.backend == "claude-cli"
    assert root not in pathlib.Path(seen["cwd"]).resolve().parents and pathlib.Path(seen["cwd"]).resolve() != root
    assert 0 < seen["timeout"] <= 120 and "ANTHROPIC_API_KEY" not in seen["env"]

def test_single_call_path():
    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
    import re
    app = pathlib.Path(__file__).resolve().parents[2] / "app"
    # The one allowed exception: app/backend/pdf_ocr.py runs the local Tesseract binary (T-086). That is OCR, not an LLM call; it may import
    # subprocess but never the anthropic SDK, and test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract checks it never starts `claude`.
    # And app/backend/pdf_hidden.py (T-087): it starts a local child process (this interpreter running its own scan module, plus a `ps` RSS probe)
    # so a hung PDF renderer can be killed; no LLM. test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children checks it never names `claude`.
    allow_subprocess = {"backend/pdf_ocr.py", "backend/pdf_hidden.py"}
    bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
           if "llm/backends" not in p.as_posix()
           and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)
           and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r"^\s*(import|from)\s+anthropic\b", p.read_text(), re.M))]
    assert bad == []

def test_no_text_in_logs(monkeypatch, caplog, capsys):
    """T-034 AC5 / arch invariant: backend failures never put the prompt, reply or SDK message in errors or logs."""
    import logging
    caplog.set_level(logging.DEBUG)
    from app.llm.backends import claude_cli as C, anthropic_api as A
    monkeypatch.setattr(C.subprocess, "run", lambda argv, **kw: subprocess.CompletedProcess(argv, 1, stdout="SECRET REPLY", stderr="SECRET RECORD TEXT"))
----
38:import ctypes
39:import json
40:import math
41:import os
42:import re
43:import subprocess
44:import sys
45:import threading
46:import time
47:import unicodedata
513:        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
515:    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
558:            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode] + ([extra] if extra else []), cwd=_ROOT, env=env,
559:                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
586:            except subprocess.TimeoutExpired:
----
1:"""Local OCR for scanned PDF pages (T-086, D-042). The Tesseract binary runs as a subprocess on this machine; no page image or text
10:import base64
11:import csv
12:import io
13:import os
14:import re
15:import shutil
16:import struct
17:import subprocess
18:import tempfile
19:import time
20:import zlib
69:        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_env())
73:        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_env())
75:    except (OSError, subprocess.SubprocessError):
167:            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
169:        except subprocess.TimeoutExpired:
243:    Tesseract subprocess and the PNG bytes it reads are handled in this process."""
----
test_provider.py
test_provider_backends.py
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:21:17.522Z

**tool call — Bash**
````
{
 "command": "sed -n 55,80p app/backend/pdf_ocr.py && echo ---- && sed -n 160,170p app/backend/pdf_ocr.py && echo ---- && grep -n \"_which\\|def _env\" app/backend/pdf_ocr.py && echo ---- && sed -n 505,520p app/backend/pdf_hidden.py && echo ---- && sed -n 550,560p app/backend/pdf_hidden.py && echo ---- && grep -n -i \"llm\\|claude\\|anthropic\\|importlib\\|__import__\\|getattr\\|os\\.\\(system\\|popen\\|exec\\|spawn\\)\" app/backend/pdf_hidden.py app/backend/pdf_ocr.py; echo ----; grep -n \"def test_pdf_ocr_only_runs_tesseract\" -A12 tests/unit/test_pdf_ocr.py; echo ----; git -C /Users/arsis/zlayt-pm-project status --short | head -30; git -C /Users/arsis/zlayt-pm-project log --oneline -3",
 "description": "Inspect OCR and hidden-scan subprocess sites and related test"
}
````

### User / tool · 2026-11-02T06:21:17.716Z

**tool result**
````
        self.reason, self.page = reason, page


def _which() -> str:
    return shutil.which("tesseract") or ""


def ocr_status() -> dict:
    """{available, version, tested_version, languages, message}. Never raises."""
    exe = _which()
    if not exe:
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Scanned pages need Tesseract, which is not installed on this server. " + INSTALL_HINT}
    try:
        v = subprocess.run([exe, "--version"], capture_output=True, text=True, timeout=10, env=_env())
        first = ((v.stdout or v.stderr).splitlines() or [""])[0]
        m = re.search(r"(\d+)\.(\d+)(?:\.(\d+))?", first)
        version = m.group(0) if m else None
        langs = subprocess.run([exe, "--list-langs"], capture_output=True, text=True, timeout=10, env=_env())
        languages = [x.strip() for x in (langs.stdout or "").splitlines()[1:] if x.strip() and x.strip() not in ("osd", "snum")]
    except (OSError, subprocess.SubprocessError):
        return {"available": False, "version": None, "tested_version": TESTED_VERSION, "languages": [],
                "message": "Tesseract is installed but could not be run. " + INSTALL_HINT}
    if not m or int(m.group(1)) < MIN_MAJOR or "eng" not in languages:
        return {"available": False, "version": version, "tested_version": TESTED_VERSION, "languages": languages,
                "message": f"This server has Tesseract {version or '(unknown version)'} with English data "
----
        raise OcrUnavailable(st["message"])
    lang = "+".join(l for l in (languages or ["eng"]) if l in st["languages"]) or "eng"
    with tempfile.TemporaryDirectory(prefix="zlayt-ocr-") as d:
        src = os.path.join(d, "page.png")
        with open(src, "wb") as f:
            f.write(png)
        try:
            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
                               timeout=timeout, env=_env(), cwd=d)
        except subprocess.TimeoutExpired:
            raise OcrFailed("timeout") from None
----
40:def _env() -> dict:
58:def _which() -> str:
64:    exe = _which()
167:            p = subprocess.run([_which(), src, "stdout", "-l", lang, "--psm", "3", "tsv"], capture_output=True, text=True,
----
_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
_SLOTS = threading.BoundedSemaphore(MAX_CHILDREN)
_CHILD_ENV_KEEP = ("PATH", "LANG", "LC_ALL", "LC_CTYPE", "TMPDIR")      # nothing else: no API key, token or HOME reaches the child


def _rss_bytes(pid: int) -> int:
    """Resident memory of a process we started, from ps (works on macOS and Linux); 0 when it cannot be read or has gone."""
    try:
        out = subprocess.run(["ps", "-o", "rss=", "-p", str(pid)], capture_output=True, text=True, timeout=2).stdout.strip()
        return int(out.split()[0]) * 1024 if out else 0
    except (OSError, ValueError, IndexError, subprocess.SubprocessError):
        return 0


def _messages(out: bytes) -> list:
    """The JSON lines a child wrote (a killed child leaves a partial last line, which is ignored)."""
----
    proc = None
    try:
        remaining = deadline - time.monotonic()
        if remaining <= 0:
            raise HiddenScanTimeout("deadline")
        env = {k: os.environ[k] for k in _CHILD_ENV_KEEP if k in os.environ}
        env["PYTHONDONTWRITEBYTECODE"] = "1"
        try:
            proc = subprocess.Popen([sys.executable, "-m", "app.backend.pdf_hidden", "%.3f" % remaining, mode] + ([extra] if extra else []), cwd=_ROOT, env=env,
                                    stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL, close_fds=True)
        except OSError as e:
----
app/backend/pdf_hidden.py:597:        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
app/backend/pdf_hidden.py:671:                             (getattr(resource, "RLIMIT_AS", None), CHILD_MEM_BYTES, CHILD_MEM_BYTES)):
----
128:def test_pdf_ocr_only_runs_tesseract():
129-    """The subprocess allow-list in test_provider.py covers pdf_ocr.py because it runs a local OCR binary, not an LLM: it never names
130-    `claude` or the anthropic SDK, and every subprocess.run starts with the tesseract executable (or its --version / --list-langs probes)."""
131-    import pathlib
132-    import re
133-    src = pathlib.Path(pdf_ocr.__file__).read_text()
134-    code = "\n".join(l for l in src.splitlines() if not l.lstrip().startswith(("#", '"""')))
135-    assert not re.search(r"claude|anthropic", code, re.I)
136-    calls = re.findall(r"subprocess\.run\(\[([^,\]]+)", src)
137-    assert calls and all(c.strip() in ("exe", "_which()") for c in calls)
138-
139-
140-def test_an_ocr_item_trace_has_the_ocr_source_step(tmp_path):
----
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
 M app/backend/billing.py
 M app/backend/flags.py
 M app/backend/judges.py
 M app/backend/pipeline.py
 M app/llm/audited.py
 D app/llm/prompts/conflicts_v1.md
 M board/activity.jsonl
 M board/cards/T-045.md
 M board/cards/T-046.md
 M board/cards/T-053.md
 M board/cards/T-055.md
 M board/cards/T-057.md
 M board/cards/T-058.md
9851a0d fix(backend): OCR page rendering runs in the killed scan child; a killed or failed child is a 400 with no in-process fallback (T-107)
d3e127c fix(backend): quote picker units come from the quotable body only (T-108)
c2a5d1f fix(backend): unit suite green on a clean HEAD; notes never print an unchecked narrative sentence (T-106)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:15.489Z

**tool call — Bash**
````
{
 "command": "grep -n \"signal\" app/backend/pdf_hidden.py | head; sed -n 590,600p app/backend/pdf_hidden.py; ls tests/unit/__init__.py tests/__init__.py 2>&1; .venv/bin/python -V; sed -n 1,12p tests/unit/test_pdf_ocr.py; grep -n \"^import\\|^from\" tests/unit/test_provider.py tests/unit/test_pdf_hidden.py; .venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py tests/unit/test_provider.py tests/unit/test_pdf_ocr.py 2>&1 | tail -3",
 "description": "Check signal usage, package layout, python version, baseline tests"
}
````

### User / tool · 2026-11-02T06:22:20.234Z

**tool result**
````
597:        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
                proc.communicate()
                raise HiddenScanUnavailable("child_died") from None
            if _rss_bytes(proc.pid) > CHILD_RSS_BYTES:
                proc.kill()
                partial, _ = proc.communicate()
                raise HiddenScanUnavailable("memory", _texts_of(_messages(partial)))
        msgs = _messages(out)
        if proc.returncode == -getattr(__import__("signal"), "SIGXCPU", 24):
            raise HiddenScanTimeout("cpu_limit")
        if proc.returncode != 0 or not msgs:
            raise HiddenScanUnavailable("child_failed", _texts_of(msgs))
tests/__init__.py
tests/unit/__init__.py
Python 3.12.2
"""T-086: local OCR of scanned PDF pages. Tests that need the Tesseract binary skip cleanly when it is not installed; the rest
(missing-binary message, TSV parsing, low-confidence rule, needs_review marking) run everywhere. All text is SYNTHETIC."""
import shutil

import pytest

from app.backend import pdf_checks, pdf_ocr, pdf_text
from tests.unit._pdf_raw import build, scanned_copy, text_page

pytest.importorskip("pypdfium2")
needs_tesseract = pytest.mark.skipif(not shutil.which("tesseract"), reason="tesseract is not installed")

tests/unit/test_provider.py:2:import json
tests/unit/test_provider.py:3:import pytest
tests/unit/test_provider.py:4:from app.llm import provider as P
tests/unit/test_provider.py:78:import pathlib, subprocess, sys, types
tests/unit/test_pdf_hidden.py:3:import pytest
tests/unit/test_pdf_hidden.py:5:from app.backend import pdf_checks, pdf_hidden, pdf_text
tests/unit/test_pdf_hidden.py:6:from tests.unit._pdf_raw import build, build_pages, text_page
.............................................                            [100%]
45 passed in 4.40s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:31.412Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/tests/unit/spawn_audit.py",
 "content": "\"\"\"AST audit for the two backend modules that start local processes (T-106 round 2; T-086 pdf_ocr, T-087 pdf_hidden).\n\nNeither module may import, name or call anything related to Claude, Anthropic or app.llm, and every subprocess spawn\nmust start an allow-listed program: the interpreter running its own child module, the `ps` RSS probe (pdf_hidden only),\nor the Tesseract binary found by `_which()` (pdf_ocr only). A string regex can be bypassed by an alias, a from-import,\nan uncalled attribute, a lookup through getattr, an argv held in a variable or a `-c` payload, so every check here walks\nthe parsed tree. `audit` returns one message per violation; an empty list means the module passes.\n\"\"\"\nimport ast\nimport re\n\nSPAWN_FUNCS = {\"run\", \"Popen\", \"call\", \"check_output\", \"check_call\", \"getoutput\", \"getstatusoutput\"}\nSUBPROCESS_DATA = {\"PIPE\", \"DEVNULL\", \"STDOUT\", \"SubprocessError\", \"TimeoutExpired\", \"CalledProcessError\", \"CompletedProcess\"}\nBANNED_MODULES = (\"anthropic\", \"importlib\", \"runpy\", \"pty\", \"commands\", \"multiprocessing\")\nBANNED_CALLS = {\"__import__\", \"eval\", \"exec\"}\nBANNED_OS_ATTR = re.compile(r\"^(system|popen|exec|spawn|posix_spawn|fork|startfile)\")\nRELATED = re.compile(r\"claude|anthropic|llm\", re.I)\n\n# argv[0] keys: \"lit:<text>\" for a string literal, \"expr:<source>\" for any other expression.\nPOLICY = {\n    \"pdf_hidden\": {\"argv0\": {\"lit:ps\", \"expr:sys.executable\"}},\n    \"pdf_ocr\": {\"argv0\": {\"expr:exe\", \"expr:_which()\"}},\n}\n\n\ndef _is_str_expr(node):\n    return isinstance(node, ast.Expr) and isinstance(node.value, ast.Constant) and isinstance(node.value.value, str)\n\n\ndef _key(node):\n    if isinstance(node, ast.Constant) and isinstance(node.value, str):\n        return \"lit:\" + node.value\n    return \"expr:\" + ast.unparse(node)\n\n\ndef _lit(node):\n    return node.value if isinstance(node, ast.Constant) and isinstance(node.value, str) else None\n\n\ndef _spawn_calls(tree):\n    for node in ast.walk(tree):\n        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr in SPAWN_FUNCS \\\n                and isinstance(node.func.value, ast.Name) and node.func.value.id == \"subprocess\":\n            yield node\n\n\ndef spawn_keys(source: str) -> list:\n    \"\"\"argv[0] key of every subprocess spawn in the module, in source order (empty when none or unreadable).\"\"\"\n    tree = ast.parse(source)\n    keys = []\n    for call in sorted(_spawn_calls(tree), key=lambda c: (c.lineno, c.col_offset)):\n        argv = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == \"args\"), None)\n        if isinstance(argv, (ast.List, ast.Tuple)) and argv.elts:\n            keys.append(_key(argv.elts[0]))\n    return keys\n\n\ndef audit(source: str, module: str) -> list:\n    \"\"\"Violations for one backend module. `module` is its file stem: pdf_hidden or pdf_ocr.\"\"\"\n    policy = POLICY[module]\n    tree = ast.parse(source)\n    out = []\n    docstring_ids = set()\n    attr_base_ids = set()\n    spawn_attr_ids = set()\n    for node in ast.walk(tree):\n        if isinstance(node, (ast.Module, ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)) and node.body and _is_str_expr(node.body[0]):\n            docstring_ids.add(id(node.body[0].value))\n        if isinstance(node, ast.Attribute):\n            attr_base_ids.add(id(node.value))\n        if isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute):\n            spawn_attr_ids.add(id(node.func))\n\n    def bad(node, msg):\n        out.append(f\"line {getattr(node, 'lineno', '?')}: {msg}\")\n\n    for node in ast.walk(tree):\n        if isinstance(node, ast.Import):\n            for a in node.names:\n                if a.name == \"subprocess\" and a.asname is not None:\n                    bad(node, \"subprocess imported under an alias\")\n                if a.name != \"subprocess\" and (a.name.split(\".\")[0] in BANNED_MODULES or RELATED.search(a.name)):\n                    bad(node, f\"imports {a.name}\")\n        elif isinstance(node, ast.ImportFrom):\n            mod = node.module or \"\"\n            if mod == \"subprocess\" or mod.startswith(\"subprocess.\") or mod.split(\".\")[0] in BANNED_MODULES or RELATED.search(mod):\n                bad(node, f\"from {'.' * node.level}{mod} import ...\")\n            for a in node.names:\n                if a.name == \"subprocess\" or RELATED.search(a.name):\n                    bad(node, f\"imports name {a.name}\")\n        elif isinstance(node, ast.Name):\n            if node.id in BANNED_CALLS:\n                bad(node, f\"uses {node.id}\")\n            if RELATED.search(node.id):\n                bad(node, f\"names {node.id}\")\n            if node.id == \"subprocess\" and id(node) not in attr_base_ids:\n                bad(node, \"uses the subprocess module other than as subprocess.<name>(...)\")\n        elif isinstance(node, ast.Attribute):\n            if RELATED.search(node.attr):\n                bad(node, f\"names attribute {node.attr}\")\n            if isinstance(node.value, ast.Name):\n                base, attr = node.value.id, node.attr\n                if base == \"subprocess\" and attr in SPAWN_FUNCS and id(node) not in spawn_attr_ids:\n                    bad(node, f\"subprocess.{attr} is used without being called\")\n                if base == \"subprocess\" and attr not in SPAWN_FUNCS | SUBPROCESS_DATA:\n                    bad(node, f\"subprocess.{attr} is not on the allow-list\")\n                if base == \"os\" and BANNED_OS_ATTR.match(attr):\n                    bad(node, f\"os.{attr} starts a process\")\n        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef, ast.arg)):\n            name = node.arg if isinstance(node, ast.arg) else node.name\n            if RELATED.search(name):\n                bad(node, f\"names {name}\")\n        elif isinstance(node, ast.Constant) and isinstance(node.value, str) and id(node) not in docstring_ids:\n            if RELATED.search(node.value):\n                bad(node, f\"string mentions {node.value[:40]!r}\")\n\n    for call in _spawn_calls(tree):\n        if any(k.arg == \"shell\" and isinstance(k.value, ast.Constant) and k.value.value for k in call.keywords):\n            bad(call, \"shell=True\")\n        argv = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == \"args\"), None)\n        if not isinstance(argv, (ast.List, ast.Tuple)) or not argv.elts:\n            bad(call, \"argv is not a literal list\")\n            continue\n        key = _key(argv.elts[0])\n        if key not in policy[\"argv0\"]:\n            bad(call, f\"starts {key[4:]!r}, which is not an allowed program\")\n        elif key == \"expr:sys.executable\" and [_lit(e) for e in argv.elts[1:3]] != [\"-m\", f\"app.backend.{module}\"]:\n            bad(call, f\"sys.executable must run only app.backend.{module} as a module (-m)\")\n\n    if \"expr:exe\" in policy[\"argv0\"]:\n        assigns = [n for n in ast.walk(tree) if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == \"exe\" for t in n.targets)]\n        stores = [n for n in ast.walk(tree) if isinstance(n, ast.Name) and n.id == \"exe\" and isinstance(n.ctx, ast.Store)]\n        if len(assigns) != len(stores) or any(ast.unparse(a.value) != \"_which()\" for a in assigns):\n            out.append(\"exe is bound to something other than _which()\")\n    if \"expr:_which()\" in policy[\"argv0\"]:\n        defs = [n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == \"_which\"]\n        if not any(isinstance(c, ast.Constant) and c.value == \"tesseract\" for d in defs for c in ast.walk(d)):\n            out.append(\"_which() does not resolve the tesseract binary\")\n    return out\n"
}
````

### User / tool · 2026-11-02T06:22:31.471Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/tests/unit/spawn_audit.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:34.322Z

**tool call — Bash**
````
{
 "command": "sed -n 36,48p app/backend/pdf_hidden.py",
 "description": "Show pdf_hidden import block"
}
````

### User / tool · 2026-11-02T06:22:34.407Z

**tool result**
````
text clipped to under CLIP_VISIBLE_MIN of its box are all held back as suspected (a faint but real footnote costs the paralegal one click).
Text a reader can read only by changing the contrast or the zoom is not text they would quote."""
import ctypes
import json
import math
import os
import re
import subprocess
import sys
import threading
import time
import unicodedata
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:35.759Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py",
 "old_string": "import re\nimport subprocess\nimport sys\nimport threading\nimport time\nimport unicodedata",
 "new_string": "import re\nimport signal\nimport subprocess\nimport sys\nimport threading\nimport time\nimport unicodedata"
}
````

### User / tool · 2026-11-02T06:22:35.813Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:37.108Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py",
 "old_string": "        if proc.returncode == -getattr(__import__(\"signal\"), \"SIGXCPU\", 24):",
 "new_string": "        if proc.returncode == -getattr(signal, \"SIGXCPU\", 24):"
}
````

### User / tool · 2026-11-02T06:22:37.188Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/app/backend/pdf_hidden.py has been updated successfully.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:38.860Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport pathlib,sys\nsys.path.insert(0,'.')\nfrom tests.unit.spawn_audit import audit, spawn_keys\nfor m in ['pdf_hidden','pdf_ocr']:\n    s=pathlib.Path(f'app/backend/{m}.py').read_text()\n    print(m, audit(s,m), spawn_keys(s))\n\"",
 "description": "Run the audit against the real pdf_hidden and pdf_ocr modules"
}
````

### User / tool · 2026-11-02T06:22:39.012Z

**tool result**
````
pdf_hidden ['line 559: argv is not a literal list'] ['lit:ps']
pdf_ocr [] ['expr:exe', 'expr:exe', 'expr:_which()']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:44.456Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport re,pathlib\np=pathlib.Path('tests/unit/spawn_audit.py')\ns=p.read_text()\nhelper='''def _argv_list(call):\n    \"\"\"The literal argv list of a spawn call: `[...]`, or `[...] + tail` where the head is the literal (pdf_hidden Popen).\"\"\"\n    node = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == \"args\"), None)\n    while isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):\n        node = node.left\n    return node if isinstance(node, (ast.List, ast.Tuple)) and node.elts else None\n\n\ndef spawn_keys(source: str) -> list:\n    \"\"\"argv[0] key of every subprocess spawn in the module, in source order (empty when none or unreadable).\"\"\"\n    tree = ast.parse(source)\n    keys = []\n    for call in sorted(_spawn_calls(tree), key=lambda c: (c.lineno, c.col_offset)):\n        argv = _argv_list(call)\n        if argv is not None:\n            keys.append(_key(argv.elts[0]))\n    return keys\n'''\nstart=s.index('def spawn_keys'); end=s.index('def audit(')\ns=s[:start]+helper+'\\n\\n'+s[end:]\nold='''        argv = call.args[0] if call.args else next((k.value for k in call.keywords if k.arg == \"args\"), None)\n        if not isinstance(argv, (ast.List, ast.Tuple)) or not argv.elts:'''\nnew='''        argv = _argv_list(call)\n        if argv is None:'''\nassert s.count(old)==1\ns=s.replace(old,new)\np.write_text(s)\nEOF\n.venv/bin/python -c \"\nimport pathlib,sys\nsys.path.insert(0,'.')\nfrom tests.unit.spawn_audit import audit, spawn_keys\nfor m in ['pdf_hidden','pdf_ocr']:\n    s=pathlib.Path(f'app/backend/{m}.py').read_text()\n    print(m, audit(s,m), spawn_keys(s))\n\"",
 "description": "Handle argv list concatenation in the audit and recheck"
}
````

### User / tool · 2026-11-02T06:22:44.631Z

**tool result**
````
pdf_hidden [] ['lit:ps', 'expr:sys.executable']
pdf_ocr [] ['expr:exe', 'expr:exe', 'expr:_which()']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:51.757Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport pathlib\np=pathlib.Path('tests/unit/test_pdf_hidden.py')\ns=p.read_text()\nstart=s.index('def test_pdf_hidden_only_starts_local_children():')\nend=s.index('    assert not re.search(r\"os\\\\.system|shell\\\\s*=\\\\s*True|os\\\\.exec|os\\\\.spawn\", code)\\n')+len('    assert not re.search(r\"os\\\\.system|shell\\\\s*=\\\\s*True|os\\\\.exec|os\\\\.spawn\", code)\\n')\nnew='''def test_pdf_hidden_only_starts_local_children():\n    \"\"\"pdf_hidden.py starts local children and never an LLM (T-087). The AST audit in spawn_audit.py enforces it: no claude,\n    anthropic or app.llm import, name or string; every spawn starts `ps` (RSS probe) or this interpreter running its own module.\"\"\"\n    src = pathlib.Path(pdf_hidden.__file__).read_text()\n    assert audit(src, \"pdf_hidden\") == []\n    assert spawn_keys(src) == [\"lit:ps\", \"expr:sys.executable\"]\n\n\n# Each snippet is appended to the real module; the audit must report it. Every one of these passed the old regex allow-list.\nBYPASSES = {\n    \"from_import_alias\": \"from subprocess import run as _sp_run\\\\n_sp_run(['/usr/bin/curl', 'https://example.invalid'])\\\\n\",\n    \"module_alias\": \"import subprocess as sp\\\\nsp.run(['/usr/bin/curl', 'https://example.invalid'])\\\\n\",\n    \"uncalled_attribute\": \"import subprocess\\\\n_f = subprocess.run\\\\n_f(['/usr/bin/curl', 'x'])\\\\n\",\n    \"getattr_lookup\": \"import subprocess\\\\ngetattr(subprocess, 'run')(['/usr/bin/curl', 'x'])\\\\n\",\n    \"argv_in_variable\": \"import subprocess\\\\n_argv = ['/usr/bin/curl', 'x']\\\\nsubprocess.run(_argv)\\\\n\",\n    \"starred_argv\": \"import subprocess\\\\nsubprocess.run(*[['/usr/bin/curl', 'x']])\\\\n\",\n    \"shell_true\": \"import subprocess\\\\nsubprocess.run(['ps'], shell=True)\\\\n\",\n    \"rebind_subprocess\": \"subprocess = None\\\\n\",\n    \"claude_program\": \"import subprocess\\\\nsubprocess.run(['claude', '-p', 'hi'], capture_output=True)\\\\n\",\n    \"claude_absolute_path\": \"import subprocess\\\\nsubprocess.run(['/usr/local/bin/claude', '-p'])\\\\n\",\n    \"interpreter_runs_code\": \"import subprocess, sys\\\\nsubprocess.run([sys.executable, '-c', 'import os; os.system(\\\\\"curl x\\\\\")'])\\\\n\",\n    \"interpreter_other_module\": \"import subprocess, sys\\\\nsubprocess.run([sys.executable, '-m', 'app.llm.backends.claude_cli'])\\\\n\",\n    \"dunder_import\": \"__import__('subprocess').run(['/usr/bin/curl', 'x'])\\\\n\",\n    \"exec_string\": \"exec('import anthropic')\\\\n\",\n    \"os_system\": \"import os\\\\nos.system('curl https://example.invalid')\\\\n\",\n    \"os_popen\": \"import os\\\\nos.popen('curl https://example.invalid')\\\\n\",\n    \"anthropic_import\": \"import anthropic\\\\n\",\n    \"llm_package_import\": \"from app import llm\\\\n\",\n    \"llm_relative_import\": \"from ..llm import backends\\\\n\",\n    \"claude_string\": \"_NAME = 'claude'\\\\n\",\n    \"claude_identifier\": \"def _call_claude():\\\\n    return None\\\\n\",\n}\n\n\n@pytest.mark.parametrize(\"snippet\", list(BYPASSES.values()), ids=list(BYPASSES))\ndef test_pdf_hidden_audit_rejects_bypass(snippet):\n    src = pathlib.Path(pdf_hidden.__file__).read_text() + \"\\\\n\" + snippet\n    assert audit(src, \"pdf_hidden\"), \"the audit let this through\"\n\n\ndef test_pdf_hidden_audit_rejects_a_spawn_that_is_not_the_probe_or_interpreter_module():\n    src = pathlib.Path(pdf_hidden.__file__).read_text() + \"\\\\nimport subprocess\\\\nsubprocess.run(['/usr/bin/curl', 'x'])\\\\n\"\n    assert any(\"curl\" in v for v in audit(src, \"pdf_hidden\"))\n'''\ns=s[:start]+new+s[end:]\ns=s.replace(\"from tests.unit._pdf_raw import build, build_pages, text_page\\n\",\"from tests.unit._pdf_raw import build, build_pages, text_page\\nfrom tests.unit.spawn_audit import audit, spawn_keys\\n\",1)\nif \"import pathlib\" not in s.split(\"\\n\\n\")[0]:\n    s=\"import pathlib\\n\"+s\np.write_text(s)\nEOF\nsed -n 1,10p tests/unit/test_pdf_hidden.py",
 "description": "Replace pdf_hidden allow-list test with AST audit and bypass tests"
}
````

### User / tool · 2026-11-02T06:22:51.873Z

**tool result**
````
import pathlib
"""T-087: text in the text layer that is not visible when the page is rendered is flagged per page and kept out of the case text
until the paralegal confirms it. Synthetic PDFs are generated here (tests/unit/_pdf_raw.py)."""
import pytest

from app.backend import pdf_checks, pdf_hidden, pdf_text
from tests.unit._pdf_raw import build, build_pages, text_page
from tests.unit.spawn_audit import audit, spawn_keys

pytest.importorskip("pypdfium2")
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:53.937Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport pathlib\np=pathlib.Path('tests/unit/test_pdf_hidden.py')\ns=p.read_text()\ns=s.replace(\"import pathlib\\n\",\"\",1)\ns=s.replace(\"import pytest\\n\\nfrom app.backend import pdf_checks\",\"import pathlib\\n\\nimport pytest\\n\\nfrom app.backend import pdf_checks\",1)\np.write_text(s)\nEOF\nsed -n 1,10p tests/unit/test_pdf_hidden.py; grep -n \"pdf_hidden\\|test_single_call_path\" -n tests/unit/test_provider_backends.py | head -5",
 "description": "Fix import order so module docstring stays first"
}
````

### User / tool · 2026-11-02T06:22:54.055Z

**tool result**
````
"""T-087: text in the text layer that is not visible when the page is rendered is flagged per page and kept out of the case text
until the paralegal confirms it. Synthetic PDFs are generated here (tests/unit/_pdf_raw.py)."""
import pathlib

import pytest

from app.backend import pdf_checks, pdf_hidden, pdf_text
from tests.unit._pdf_raw import build, build_pages, text_page
from tests.unit.spawn_audit import audit, spawn_keys

153:def test_single_call_path():
159:        if p.name in ("pdf_ocr.py", "pdf_hidden.py") and "backend" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls; anthropic stays banned
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:22:56.689Z

**tool call — Bash**
````
{
 "command": "sed -n 150,170p tests/unit/test_provider_backends.py; echo ----; grep -n \"def test_single_call_path\" -A16 tests/unit/test_provider.py; echo ----; sed -n 1,12p tests/unit/test_provider_backends.py | grep -n \"import\"",
 "description": "Read both test_single_call_path definitions"
}
````

### User / tool · 2026-11-02T06:22:56.785Z

**tool result**
````
    assert out == {"summary": "ok"} and row["backend"] == "fixture" and row["role"] == "judge" and row["parsed_ok"] == 1
    assert json.loads(row["recorded_from_json"] if "recorded_from_json" in row else json.dumps(row["recorded_from"]))["backend"] == "claude-cli"

def test_single_call_path():
    """T-034 AC5: no SDK or subprocess use outside app/llm/backends."""
    for p in (ROOT / "app").rglob("*.py"):
        if "backends" in p.parts and "llm" in p.parts:
            continue
        src = p.read_text()
        if p.name in ("pdf_ocr.py", "pdf_hidden.py") and "backend" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls; anthropic stays banned
            assert not re.search(r"^\s*(import|from)\s+anthropic\b", src, re.M), p
            continue
        assert not re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", src, re.M), p

def test_no_text_in_logs(tmp_path, monkeypatch, caplog, capsys):
    """T-034 AC5: a failing live call logs neither prompt nor error text."""
    caplog.set_level("DEBUG")
    monkeypatch.setenv("LLM_BACKEND", "claude-cli")
    def fake_run(a, **k): raise subprocess.TimeoutExpired("claude", 120)
    monkeypatch.setattr(CLI.subprocess, "run", fake_run)
    conn = DB.connect(str(tmp_path / "a.sqlite")); cid = DB.create_case(conn, "SYNTHETIC", now=1.0)
----
115:def test_single_call_path():
116-    """T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends."""
117-    import re
118-    app = pathlib.Path(__file__).resolve().parents[2] / "app"
119-    # The one allowed exception: app/backend/pdf_ocr.py runs the local Tesseract binary (T-086). That is OCR, not an LLM call; it may import
120-    # subprocess but never the anthropic SDK, and test_pdf_ocr.py::test_pdf_ocr_only_runs_tesseract checks it never starts `claude`.
121-    # And app/backend/pdf_hidden.py (T-087): it starts a local child process (this interpreter running its own scan module, plus a `ps` RSS probe)
122-    # so a hung PDF renderer can be killed; no LLM. test_pdf_hidden.py::test_pdf_hidden_only_starts_local_children checks it never names `claude`.
123-    allow_subprocess = {"backend/pdf_ocr.py", "backend/pdf_hidden.py"}
124-    bad = [str(p.relative_to(app)) for p in app.rglob("*.py")
125-           if "llm/backends" not in p.as_posix()
126-           and re.search(r"^\s*(import|from)\s+(anthropic|subprocess)\b", p.read_text(), re.M)
127-           and not (str(p.relative_to(app)) in allow_subprocess and not re.search(r"^\s*(import|from)\s+anthropic\b", p.read_text(), re.M))]
128-    assert bad == []
129-
130-def test_no_text_in_logs(monkeypatch, caplog, capsys):
131-    """T-034 AC5 / arch invariant: backend failures never put the prompt, reply or SDK message in errors or logs."""
----
2:import json, pathlib, re, subprocess, threading, time, types
3:import pytest
4:from app.llm import provider as P, audited as AU, record as R
5:from app.llm.backends import claude_cli as CLI, anthropic_api as API
6:from app.db import db as DB
7:from tests.unit import _golden as G
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:23:08.029Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport pathlib\n# test_provider.py\np=pathlib.Path('tests/unit/test_provider.py'); s=p.read_text()\nstart=s.index('def test_single_call_path():'); end=s.index('def test_no_text_in_logs(monkeypatch, caplog, capsys):')\nnew='''def test_single_call_path():\n    \"\"\"T-034 AC5 / arch invariant: no anthropic SDK or subprocess import outside app/llm/backends.\"\"\"\n    import re\n    from tests.unit.spawn_audit import audit\n    app = pathlib.Path(__file__).resolve().parents[2] / \"app\"\n    # Two local-process modules may import subprocess: app/backend/pdf_ocr.py (Tesseract, T-086) and app/backend/pdf_hidden.py (its own scan\n    # child plus a `ps` RSS probe, T-087). They are not allowed to call the LLM, and they are not checked with a regex: the AST audit in\n    # tests/unit/spawn_audit.py rejects any claude/anthropic/app.llm name, any spawn outside its argv allow-list, and any alias or lookup trick.\n    allow_subprocess = {\"backend/pdf_ocr.py\": \"pdf_ocr\", \"backend/pdf_hidden.py\": \"pdf_hidden\"}\n    bad = []\n    for p in app.rglob(\"*.py\"):\n        rel = str(p.relative_to(app))\n        if \"llm/backends\" in p.as_posix():\n            continue\n        src = p.read_text()\n        if rel in allow_subprocess:\n            bad += [f\"{rel}: {v}\" for v in audit(src, allow_subprocess[rel])]\n        elif re.search(r\"^\\\\s*(import|from)\\\\s+(anthropic|subprocess)\\\\b\", src, re.M):\n            bad.append(rel)\n    assert bad == []\n\n'''\ns=s[:start]+new+s[end:]\np.write_text(s)\n\n# test_provider_backends.py\np=pathlib.Path('tests/unit/test_provider_backends.py'); s=p.read_text()\nold='''        if p.name in (\"pdf_ocr.py\", \"pdf_hidden.py\") and \"backend\" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls; anthropic stays banned\n            assert not re.search(r\"^\\\\s*(import|from)\\\\s+anthropic\\\\b\", src, re.M), p\n            continue'''\nassert s.count(old)==1, s.count(old)\ns=s.replace(old,'''        if p.name in (\"pdf_ocr.py\", \"pdf_hidden.py\") and \"backend\" in p.parts:      # local Tesseract binary (T-086) / local scan child process (T-087), not LLM calls\n            assert audit(src, p.stem) == [], p                                       # AST audit: no claude/anthropic/app.llm, argv allow-list only\n            continue''')\ns=s.replace(\"from tests.unit import _golden as G\\n\",\"from tests.unit import _golden as G\\nfrom tests.unit.spawn_audit import audit\\n\",1)\np.write_text(s)\n\n# test_pdf_ocr.py\np=pathlib.Path('tests/unit/test_pdf_ocr.py'); s=p.read_text()\nstart=s.index('def test_pdf_ocr_only_runs_tesseract():'); end=s.index('def test_an_ocr_item_trace_has_the_ocr_source_step')\nnew='''def test_pdf_ocr_only_runs_tesseract():\n    \"\"\"pdf_ocr.py runs a local OCR binary, never an LLM (T-086). The AST audit in spawn_audit.py enforces it: no claude, anthropic or\n    app.llm reference; every spawn starts the Tesseract path from _which(), and `exe` is only ever bound to _which().\"\"\"\n    src = pathlib.Path(pdf_ocr.__file__).read_text()\n    assert audit(src, \"pdf_ocr\") == []\n    assert spawn_keys(src) == [\"expr:exe\", \"expr:exe\", \"expr:_which()\"]\n\n\nOCR_BYPASSES = {\n    \"exe_rebound\": \"exe = 'curl'\\\\n\",\n    \"ps_probe\": \"import subprocess\\\\nsubprocess.run(['ps', '-A'])\\\\n\",\n    \"interpreter_probe\": \"import subprocess, sys\\\\nsubprocess.run([sys.executable, '-m', 'app.backend.pdf_ocr'])\\\\n\",\n    \"claude_program\": \"import subprocess\\\\nsubprocess.run(['claude', '-p', 'x'])\\\\n\",\n    \"from_import_alias\": \"from subprocess import check_output as co\\\\nco(['/usr/bin/curl', 'x'])\\\\n\",\n    \"llm_import\": \"from app.llm import provider\\\\n\",\n}\n\n\n@pytest.mark.parametrize(\"snippet\", list(OCR_BYPASSES.values()), ids=list(OCR_BYPASSES))\ndef test_pdf_ocr_audit_rejects_bypass(snippet):\n    src = pathlib.Path(pdf_ocr.__file__).read_text() + \"\\\\n\" + snippet\n    assert audit(src, \"pdf_ocr\"), \"the audit let this through\"\n\n\n'''\ns=s[:start]+new+s[end:]\ns=s.replace(\"import shutil\\n\\nimport pytest\\n\",\"import pathlib\\nimport shutil\\n\\nimport pytest\\n\",1)\ns=s.replace(\"from tests.unit._pdf_raw import build, scanned_copy, text_page\\n\",\"from tests.unit._pdf_raw import build, scanned_copy, text_page\\nfrom tests.unit.spawn_audit import audit, spawn_keys\\n\",1)\np.write_text(s)\nEOF\n.venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_ocr.py 2>&1 | tail -15",
 "description": "Wire AST audit into single-call and OCR tests, then run them"
}
````

### User / tool · 2026-11-02T06:23:15.099Z

**tool result**
````
........................................................................ [ 78%]
....................                                                     [100%]
92 passed in 6.57s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:23:18.275Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport pathlib,sys\nsys.path.insert(0,'.')\nfrom tests.unit.test_pdf_hidden import BYPASSES\nfrom tests.unit.test_pdf_ocr import OCR_BYPASSES\nfrom tests.unit.spawn_audit import audit\nh=pathlib.Path('app/backend/pdf_hidden.py').read_text()\no=pathlib.Path('app/backend/pdf_ocr.py').read_text()\nfor k,v in BYPASSES.items(): print('H',k, audit(h+'\\n'+v,'pdf_hidden')[:1])\nfor k,v in OCR_BYPASSES.items(): print('O',k, audit(o+'\\n'+v,'pdf_ocr')[:1])\n\" 2>&1 | tail -50",
 "description": "Print the violation each bypass snippet triggers"
}
````

### User / tool · 2026-11-02T06:23:18.870Z

**tool result**
````
H from_import_alias ['line 798: from subprocess import ...']
H module_alias ['line 798: subprocess imported under an alias']
H uncalled_attribute ['line 799: subprocess.run is used without being called']
H getattr_lookup ['line 799: uses the subprocess module other than as subprocess.<name>(...)']
H argv_in_variable ['line 800: argv is not a literal list']
H starred_argv ['line 799: argv is not a literal list']
H shell_true ['line 799: shell=True']
H rebind_subprocess ['line 798: uses the subprocess module other than as subprocess.<name>(...)']
H claude_program ["line 799: string mentions 'claude'"]
H claude_absolute_path ["line 799: string mentions '/usr/local/bin/claude'"]
H interpreter_runs_code ['line 799: sys.executable must run only app.backend.pdf_hidden as a module (-m)']
H interpreter_other_module ["line 799: string mentions 'app.llm.backends.claude_cli'"]
H dunder_import ['line 798: uses __import__']
H exec_string ['line 798: uses exec']
H os_system ['line 799: os.system starts a process']
H os_popen ['line 799: os.popen starts a process']
H anthropic_import ['line 798: imports anthropic']
H llm_package_import ['line 798: imports name llm']
H llm_relative_import ['line 798: from ..llm import ...']
H claude_string ["line 798: string mentions 'claude'"]
H claude_identifier ['line 798: names _call_claude']
O exe_rebound ['exe is bound to something other than _which()']
O ps_probe ["line 266: starts 'ps', which is not an allowed program"]
O interpreter_probe ["line 266: starts ':sys.executable', which is not an allowed program"]
O claude_program ["line 266: string mentions 'claude'"]
O from_import_alias ['line 265: from subprocess import ...']
O llm_import ['line 265: from app.llm import ...']
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:23:21.522Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'EOF'\nimport pathlib\np=pathlib.Path('tests/unit/spawn_audit.py'); s=p.read_text()\nold='bad(call, f\"starts {key[4:]!r}, which is not an allowed program\")'\nassert s.count(old)==1\ns=s.replace(old,'bad(call, f\"starts {key.split(\\':\\', 1)[1]!r}, which is not an allowed program\")')\np.write_text(s)\nEOF\ngrep -n \"allowed program\" tests/unit/spawn_audit.py; .venv/bin/python -m pytest -q tests/unit/test_pdf_hidden.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_ocr.py 2>&1 | tail -2",
 "description": "Fix violation message text and rerun the four test files"
}
````

### User / tool · 2026-11-02T06:23:27.818Z

**tool result**
````
134:            bad(call, f"starts {key.split(':', 1)[1]!r}, which is not an allowed program")
....................                                                     [100%]
92 passed in 5.77s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:23:32.358Z

**tool call — Bash**
````
{
 "command": "timeout 580 .venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15",
 "description": "Run full unit suite in the project tree",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:23:32.449Z

**tool result**
````
/bin/bash: timeout: command not found
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:23:33.614Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest -q tests/unit 2>&1 | tail -15",
 "description": "Run full unit suite in the project tree",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:26:18.398Z

**tool result**
````
........................................................................ [ 58%]
........................................................................ [ 62%]
........................................................................ [ 65%]
........................................................................ [ 68%]
........................................................................ [ 71%]
........................................................................ [ 75%]
........................................................................ [ 78%]
........................................................................ [ 81%]
........................................................................ [ 84%]
.....................s.................................................. [ 88%]
........................................................................ [ 91%]
........................................................................ [ 94%]
........................................................................ [ 97%]
..............................................                           [100%]
2205 passed, 1 skipped in 163.36s (0:02:43)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:20.825Z

**tool call — Bash**
````
{
 "command": "git diff --stat -- app/backend/pdf_hidden.py tests/unit/spawn_audit.py tests/unit/test_pdf_hidden.py tests/unit/test_provider.py tests/unit/test_provider_backends.py tests/unit/test_pdf_ocr.py; git status --short -- app/backend/pdf_hidden.py tests/unit/ | head -20; git log --oneline -1 -- tests/unit/test_pdf_ocr.py",
 "description": "Confirm only my changes sit in the paths to commit"
}
````

### User / tool · 2026-11-02T06:26:20.999Z

**tool result**
````
 app/backend/pdf_hidden.py            |  3 +-
 tests/unit/test_pdf_hidden.py        | 55 +++++++++++++++++++++++++++++-------
 tests/unit/test_pdf_ocr.py           | 30 ++++++++++++++------
 tests/unit/test_provider.py          | 24 ++++++++++------
 tests/unit/test_provider_backends.py |  5 ++--
 5 files changed, 87 insertions(+), 30 deletions(-)
 M app/backend/pdf_hidden.py
 M tests/unit/test_flags_injection.py
 M tests/unit/test_flags_pass.py
 M tests/unit/test_pdf_hidden.py
 M tests/unit/test_pdf_ocr.py
 M tests/unit/test_pipeline.py
 M tests/unit/test_provider.py
 M tests/unit/test_provider_backends.py
 M tests/unit/test_t075_determinism.py
?? tests/unit/spawn_audit.py
?? tests/unit/test_conflict_candidates.py
2fca530 feat(backend): PDF hidden-text detection and local Tesseract OCR (T-087, T-086)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:24.660Z

**tool call — Bash**
````
{
 "command": "git add app/backend/pdf_hidden.py tests/unit/spawn_audit.py tests/unit/test_pdf_hidden.py tests/unit/test_pdf_ocr.py tests/unit/test_provider.py tests/unit/test_provider_backends.py && git diff --cached --stat",
 "description": "Stage the six T-106 round-2 paths explicitly"
}
````

### User / tool · 2026-11-02T06:26:24.801Z

**tool result**
````
 app/backend/pdf_hidden.py            |   3 +-
 tests/unit/spawn_audit.py            | 147 +++++++++++++++++++++++++++++++++++
 tests/unit/test_pdf_hidden.py        |  55 ++++++++++---
 tests/unit/test_pdf_ocr.py           |  30 +++++--
 tests/unit/test_provider.py          |  24 +++---
 tests/unit/test_provider_backends.py |   5 +-
 6 files changed, 234 insertions(+), 30 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:26.323Z

**tool call — Bash**
````
{
 "command": "git commit -m \"fix(backend): pdf_hidden and pdf_ocr allow-list is an AST audit (T-106 round 2)\n\nReplace the string-regex subprocess allow-list with tests/unit/spawn_audit.py. It rejects any claude, anthropic or app.llm import,\nname or string; any subprocess alias, from-import, uncalled attribute, getattr lookup or non-literal argv; shell=True; os.system and\nfriends; __import__, eval and exec; and any spawn whose argv[0] is not the interpreter running its own module (-m), the ps probe\n(pdf_hidden), or the Tesseract path from _which() (pdf_ocr). pdf_hidden's signal lookup is now a plain import. The reviewer's bypass\nexamples are parametrized tests that must fail the audit.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- app/backend/pdf_hidden.py tests/unit/spawn_audit.py tests/unit/test_pdf_hidden.py tests/unit/test_pdf_ocr.py tests/unit/test_provider.py tests/unit/test_provider_backends.py && git log --oneline -1",
 "description": "Commit the T-106 round-2 paths with trailer"
}
````

### User / tool · 2026-11-02T06:26:26.888Z

**tool result**
````
check_secrets: ok (6 file(s) scanned staged)
[main e3a62fa] fix(backend): pdf_hidden and pdf_ocr allow-list is an AST audit (T-106 round 2)
 6 files changed, 234 insertions(+), 30 deletions(-)
 create mode 100644 tests/unit/spawn_audit.py
e3a62fa fix(backend): pdf_hidden and pdf_ocr allow-list is an AST audit (T-106 round 2)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:31.659Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t106_r2_head && rm -rf \"$S\" && mkdir -p \"$S\" && git archive HEAD | tar -x -C \"$S\" && cd \"$S\" && ls -a | head -3 && test ! -e .git && echo \"no .git in archive\" && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3",
 "description": "Extract HEAD archive to scratch and run unit suite",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:26:31.730Z

**tool result (error)**
````
Permission to use Bash with command S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t106_r2_head && rm -rf "$S" && mkdir -p "$S" && git archive HEAD has been denied.
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:34.591Z

**tool call — Bash**
````
{
 "command": "S=/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t106_r2_archive && mkdir -p \"$S\" && git archive HEAD | tar -x -C \"$S\" && ls -a \"$S\" | head -5 && test ! -e \"$S/.git\" && echo \"no .git in archive\"",
 "description": "Extract HEAD archive into a fresh scratch directory"
}
````

### User / tool · 2026-11-02T06:26:35.082Z

**tool result**
````
.
..
.claude
.gitignore
CLAUDE.md
no .git in archive
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:26:37.170Z

**tool call — Bash**
````
{
 "command": "cd /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/t106_r2_archive && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest -q tests/unit 2>&1 | tail -3",
 "description": "Run unit suite on the HEAD archive copy",
 "timeout": 600000
}
````

### User / tool · 2026-11-02T06:29:16.187Z

**tool result**
````
........................................................................ [ 98%]
............................                                             [100%]
2184 passed, 4 skipped in 157.67s (0:02:37)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:29:22.377Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\" && $B ac T-106 --check 1 --agent backend --evidence \"e3a62fa: pdf_hidden/pdf_ocr allow-list is an AST audit (tests/unit/spawn_audit.py). Reviewer bypasses (from-import alias, module alias, uncalled attribute, getattr, argv variable, claude argv, -c payload, os.system, __import__) fail it: test_pdf_hidden.py::test_pdf_hidden_audit_rejects_bypass[*] and test_pdf_ocr.py::test_pdf_ocr_audit_rejects_bypass[*]. tests/unit on git archive of HEAD: 2184 passed 4 skipped 0 failed; project tree 2205 passed 1 skipped\" && $B handoff T-106 --agent backend --text \"Round 2 (e3a62fa): the pdf_hidden allow-list is now an AST audit, not a regex. What changed: tests/unit/spawn_audit.py (new) walks the tree of pdf_hidden.py and pdf_ocr.py. It rejects any claude/anthropic/llm import, name or string; subprocess aliases, from-imports, uncalled attributes, getattr lookups and non-literal argv; shell=True; os.system/popen; __import__/eval/exec; and any spawn whose argv[0] is not the allowed program. pdf_hidden's __import__('signal') became a plain import. The reviewer's from-import probe and 21 other bypass snippets are parametrized tests that must fail. How verified: .venv/bin/python -m pytest -q tests/unit = 2205 passed 1 skipped in the project tree; on git archive HEAD (no .git) = 2184 passed 4 skipped 0 failed. Left: a deviation from the brief. The brief allows only the interpreter or tesseract, but pdf_hidden's RSS probe runs ps, so ps is a third allowed argv[0] for pdf_hidden only (the reviewer's proposal; the code is real). Say if you want the probe removed instead. Left also: F3 (fixture filter depth) not touched. Surprised: the shared working tree has other agents' uncommitted edits, so I staged and committed my six paths only.\" && $B move T-106 in_review --agent backend && $B show T-106 | head -12",
 "description": "Record AC evidence, handoff, and move card to in_review"
}
````

### User / tool · 2026-11-02T06:29:22.709Z

**tool result**
````
AC 1 checked: e3a62fa: pdf_hidden/pdf_ocr allow-list is an AST audit (tests/unit/spawn_audit.py). Reviewer bypasses (from-import alias, module alias, uncalled attribute, getattr, argv variable, claude argv, -c payload, os.system, __import__) fail it: test_pdf_hidden.py::test_pdf_hidden_audit_rejects_bypass[*] and test_pdf_ocr.py::test_pdf_ocr_audit_rejects_bypass[*]. tests/unit on git archive of HEAD: 2184 passed 4 skipped 0 failed; project tree 2205 passed 1 skipped
handoff written on T-106
T-106: in_progress -> in_review
---
id: "T-106"
title: "Unit suite back to green on clean HEAD: pdf_hidden subprocess allow-list, fixture-run artifacts test, no-.git calibration test; notes withhold unchecked narrative text; HIGHLIGHT_NOT_FOUND test"
milestone: "M2"
role: "backend"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T06:01:45Z"
updated_at: "2026-11-02T06:29:22Z"
claimed_by: "backend"
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:29:24.184Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py commit T-106 --sha e3a62fa --agent backend",
 "description": "Record the round-2 commit on the card"
}
````

### User / tool · 2026-11-02T06:29:24.313Z

**tool result**
````
T-106: commit e3a62fa recorded
````

### Assistant · claude-haiku-5-5 · 2026-11-02T06:29:25.716Z

T-106 round 2 is in_review at e3a62fa: the pdf_hidden/pdf_ocr allow-list is now an AST audit that rejects all the reviewer's bypasses, and the unit suite is green on both the project tree (2205 passed) and a `git archive HEAD` copy (2184 passed, 4 skipped). One deviation to confirm: pdf_hidden's `ps` RSS probe is a third allowed argv[0] for that module only, since removing it would change the product code.
