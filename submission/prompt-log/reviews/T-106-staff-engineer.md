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
