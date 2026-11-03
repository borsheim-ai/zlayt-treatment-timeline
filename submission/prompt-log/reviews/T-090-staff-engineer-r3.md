# T-090 round 3 review: forged-header skip, source_tree, sentence check, served field (commits b85fc1b, 172028c)

**Verdict: changes.** No blocker. The r2 blocker is closed at HEAD: the r2 provenance code and its tests are back (a850be0), and `evals/reports/calibration.json` regenerates exactly from `git archive b85fc1b`. The r2 forged-header skip and the check-fresh sentence gap are fixed, and each mutant I ran is killed in a git checkout. One major stays open, the same as r2 finding 3: the served calibration field has no backend route in any acceptance criterion. T-090 AC 1 says the field is "carried by T-096", but T-096 does not carry it.

Method: the project-tree selector gives 86 passed, 0 skipped. The three files equal HEAD (`git diff --stat HEAD -- ...` empty), so that count is HEAD's. Mutants ran in a `git clone` detached at 172028c, which has `.git`, so the provenance tests run. The regeneration ran from `git archive b85fc1b`, which has no `.git`, as the brief asked. Full log: `artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt`.

## r2 status

| r2 finding | r3 status |
|---|---|
| 1 blocker: r2 fix reverted at HEAD by 2fca530 | Closed. a850be0 restores it; `git show HEAD:evals/run.py \| grep -c "def git_source"` = 1; every r2 test def is at HEAD except one rename |
| 2 major: forged source_commit passes by skipping | Closed in a git checkout (M1: 2 failed, 0 skipped). Residual in a git-less copy: finding 2 |
| 3 major: served field has no owner | Open: finding 1 |
| 4 minor: check-fresh passes an edited sentence | Closed: M5 kills the new test; M5b makes check_fresh return 1 |
| 5 minor: clean flag copied into the comparison | Closed: the flag is no longer copied. `source_tree` is checked against git (test_eval_runner.py:651) and `source_tree_clean` is pinned True |

## Mutants (scratch clone at 172028c, pristine files restored after each)

| Mutant | Result |
|---|---|
| M1: `source_commit` = "1"*40 | 2 failed, 84 passed, 0 skipped (ancestor test and regeneration test) |
| M2: `source_commit` = unreferenced commit, not an ancestor of HEAD | 1 failed (ancestor test) |
| M3: `source_tree` = "0"*40 | 1 failed (ancestor test) |
| M5: sentence rebuild removed from `check_calibration` (evals/run.py:1041-1042) | 1 failed: `test_check_fresh_fails_on_an_edited_calibration_sentence` |
| M5b: `sentences.overall.verified` 83/84 changed to 84/84, pristine code | `check_fresh` returns 1; stderr "calibration.json sentences do not match the counts they are built from" |
| M8: r2 skip-on-missing logic restored in `_require_source_commit`, header = "1"*40 | 83 passed, 3 skipped, 0 failed: a silent green, which is what r3 is meant to stop |

## Findings

### 1. major: the served calibration field still has no backend AC (r2 finding 3, open)

Evidence: `board/cards/T-090.md:20` AC 1 is `done: true` and says "served field and UI line are carried by T-096 (frontend)". `board/cards/T-096.md:18` AC 1 (`done: false`, status ready) contains no route, backend or serve term: `sed -n 18p board/cards/T-096.md | grep -o -i "route\|backend\|serve\|calibration"` prints nothing. `board/cards/T-096.md:26` is a note that says "Backend AC needed: route returns those fields, null if file absent, no write path; test it." No card holds that AC. `grep -rln calibration app/` prints nothing and exits 1.

Why it matters: the served sentence is the only path from the measured counts to the paralegal's screen. A note that says "Backend AC needed" is a request, not a criterion, so the route can ship absent while T-090 AC 1 stays done. The r3 change moved the UI line and the field shape to T-096 but left the backend route with no AC. This is not a blocker: no UI renders the number today. It must be fixed before the milestone gate.

Fix: add an AC to T-096, or to a named backend card, for a read-only route that returns the `calibration.json` fields listed in the T-096 note (schema `evals.calibration/1`). It returns null when `evals/reports/calibration.json` is absent and has no write path. Name that card id in T-090 AC 1.

Acceptance test: `python3 tools/board.py show <owner>` lists the route AC; `grep -rn calibration app/backend` finds the handler; a test reads the route against a temp file and asserts the response equals `sentences.overall.verified` verbatim, and returns null when the file is absent.

### 2. minor: a copy without `.git` skips both provenance tests, so a forged header passes with 3 skips

Evidence: `tests/unit/test_eval_runner.py:636` `pytest.skip("no git repository here (exported tree)")` and `:661` `pytest.skip("no git repository here")`. Repro: `git -C /Users/arsis/zlayt-pm-project archive 172028c | tar -x -C <scratch>/archive-head`, then set that copy's `source_commit` to "1"*40 and run `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"`. Result: `83 passed, 3 skipped` (SKIPPED [2] at :636, SKIPPED [1] at :661). The unforged copy gives the same `83 passed, 3 skipped`.

Why it matters: the r2 fix as specified (skip only when there is no repository) is implemented, and in a git checkout a forged header now fails. But a shipped copy without `.git` reports green with the provenance guard off, and the skip shows only as a count. Minor because the skip is explicit and the normal submission has history. The open question is whether a `.git`-less copy is ever what gets graded (see questions).

Fix: when there is no repository, fail unless an explicit opt-out variable is set by the export step (for example `CALIBRATION_EXPORT_NO_GIT=1`).

Acceptance test: in a git-less copy with `source_commit` = "1"*40 and no opt-out variable, the selector reports at least one failed test and no skipped provenance tests.

### 3. nit: `git_source` catch-all discards the reason git failed

Evidence: `evals/run.py:76-77` `except Exception:` / `return {"commit": None, "clean": None, "tree": None}`. The except line predates r3; r3 added the `tree` key to the same return. The None state is explicit, and the header test fails on it, so this is not silent.

Why it matters: a missing git binary, a timeout and a non-repository all look the same in the header. Not a blocker.

Fix: catch `subprocess.CalledProcessError`, `FileNotFoundError` and `subprocess.TimeoutExpired`, and print the reason to stderr.

### 4. nit: the served shape in the T-096 note omits the provenance keys

Evidence: `board/cards/T-096.md:26` lists by_state, by_type, not_scored, sentences, case_count, small_sample, backend and source_commit. `evals/reports/calibration.json` also carries `source_tree_clean`, `source_tree`, `hashes`, `generated_at`, `cases`, `models`, `source` and `match_rule` (key dump in the evidence log, section 7).

Why it matters: the UI cannot show that the counts came from a clean tree of the named commit. Not a spec requirement; noted so the frontend does not assume the field carries it.

Fix: if the UI should show provenance, add `source_tree_clean` to the served field and to the note. Otherwise say in the note that the served field is a subset.

## Reproduced

- `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` in the project tree: 86 passed, 1372 deselected, 0 skipped. In the scratch clone at 172028c: 86 passed, 1346 deselected.
- Regeneration from `git archive b85fc1b` with `python -I`, `env -i`, fixture backend, run twice: run1 and run2 are identical except `generated_at`. The committed file and the regeneration are identical except the four git-derived fields (`generated_at`, `source_commit`, `source_tree`, `source_tree_clean`). Copy at `artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json`.
- `git rev-parse b85fc1b^{tree}` = 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f, equal to the header `source_tree`.
- `grep -c "%" evals/reports/calibration.json` = 0.
- `python3 tools/board.py validate`: ok (97 files).

## Outside my lens

The ship bar on the fixture run is still unmet (`4_no_invented_facts`, determinism and judge controls not measured); `evals.run` exits 1 for that reason in each regeneration. Those are not T-090 AC items. I did not judge frontend wording.

```json
{"card": "T-090", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits b85fc1b (evals/run.py, tests/unit/test_eval_runner.py: r3 code), 172028c (evals/reports/calibration.json: regenerated), a850be0 (restores r2 code reverted by 2fca530); HEAD 172028c. No app URL (no calibration route exists: grep -rln calibration app/ returns nothing). Sample case = fixture backend over the 10 golden cases.",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-090-staff-engineer-r2.md, memory project_t090_calibration_review_patterns.md, board/cards/T-090.md and T-096.md via tools/board.py show, python3 tools/board.py validate (ok, 97 files)",
  "git show b85fc1b (full diff of evals/run.py and tests/unit/test_eval_runner.py) and git show 172028c (calibration.json diff); git show --stat a850be0, 2fca530",
  "git merge-base --is-ancestor for 823b718, 02ff244, 2fca530, 865b186, b85fc1b, 172028c: all yes; git rev-parse b85fc1b^{tree} = 3f014d4b5d84f8731ff464d4548e18dfce3fbd4f (equals header source_tree)",
  "git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py evals/reports/calibration.json: empty; git show HEAD:evals/run.py | grep -c 'def git_source' = 1; test def list of 823b718 vs HEAD: all present except one rename (test_committed_calibration_source_commit_is_an_ancestor_of_head)",
  "project tree: .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 86 passed, 1372 deselected, 0 skipped",
  "scratch clone (git clone --no-hardlinks, detached 172028c): same selector -> 86 passed, 1346 deselected, 0 skipped; R.ROOT confirmed inside the clone",
  "git archive b85fc1b into scratchpad (no .git); regenerated twice with python -I, env -i, fixture (python -I -c runpy evals.run --out); run1 vs run2 identical except generated_at; committed vs regenerated identical except generated_at, source_commit, source_tree, source_tree_clean; by_state, by_type, sentences, hashes, not_scored equal. Copy at artifacts/review-evidence/T-090-staff-r3/regen-b85fc1b-run1-calibration.json",
  "mutants in the scratch clone (pristine copies restored after each): M1 source_commit 1*40 -> 2 failed, 0 skipped; M2 unreferenced non-ancestor commit -> 1 failed; M3 source_tree 0*40 -> 1 failed; M4 source_commit 2*40 -> 2 failed; M5 sentence rebuild removed from check_calibration -> 1 failed (test_check_fresh_fails_on_an_edited_calibration_sentence); M5b edited sentence 83/84->84/84, check_fresh returns 1; M8 r2 skip logic restored + forged 1*40 -> 83 passed, 3 skipped, 0 failed",
  "git archive 172028c into scratchpad (no .git): selector unmodified -> 83 passed, 3 skipped; with source_commit 1*40 -> 83 passed, 3 skipped (forged header passes with skips)",
  "grep -rln calibration app/ (no output, exit 1); sed -n 18p board/cards/T-096.md | grep route/backend/serve/calibration (no output); grep -c '%' evals/reports/calibration.json = 0; python dump of calibration.json keys against the served shape in the T-096 note",
  "full log: artifacts/review-evidence/T-090-staff-r3/mutation-and-command-log.txt"
 ],
 "verdict": "changes",
 "scores": {"r2_blocker_closed_at_head": 5, "forged_header_fails_in_git_checkout": 5, "forged_header_fails_without_git": 2, "regeneration_from_source_commit": 5, "source_tree_checked_against_git": 5, "check_fresh_catches_sentence_edit": 5, "served_field_owned_with_ac": 2, "no_silent_skip_or_fallback": 3, "mutants_killed": 5},
 "findings": [
  {"severity": "major",
   "title": "The served calibration field still has no backend route in any acceptance criterion; T-090 AC 1 closes on an owner that does not carry it",
   "evidence": "board/cards/T-090.md:20 AC 1 done:true, text 'served field and UI line are carried by T-096 (frontend)'. board/cards/T-096.md:18 AC 1 (done:false, status ready) names no route, backend or serve term: sed -n 18p board/cards/T-096.md | grep -o -i 'route|backend|serve|calibration' prints nothing. board/cards/T-096.md:26 note 2026-11-02T04:48:59Z: 'Backend AC needed: route returns those fields, null if file absent, no write path; test it.' No card holds that AC. grep -rln calibration app/ prints nothing, exit 1.",
   "why_it_matters": "The served sentence is the only path from the measured counts to the paralegal's screen. A note that says 'Backend AC needed' is a request, not a criterion, so the route can ship absent while the T-090 AC stays done. This is r2 finding 3 unchanged: r3 moved the UI line and the shape to T-096 but left the backend route with no AC. Not a blocker because no UI renders an unsupported number today; it must be fixed before the milestone gate.",
   "fix": "Add an AC to T-096 (or to a named backend card) for a read-only route that returns the calibration.json fields in the T-096 note (schema evals.calibration/1), with null when evals/reports/calibration.json is absent and no write path; name that card id in T-090 AC 1.",
   "acceptance_test": "python3 tools/board.py show <owner> lists the route AC; grep -rn calibration app/backend finds the route handler; a test reads the route against a temp calibration.json and asserts the response equals the file's sentences.overall.verified verbatim, and returns null when the file is absent."},
  {"severity": "minor",
   "title": "A copy without .git skips both provenance tests, so a forged source_commit passes with 3 skips",
   "evidence": "tests/unit/test_eval_runner.py:636 pytest.skip('no git repository here (exported tree)') and :661 pytest.skip('no git repository here'). Repro: git -C /Users/arsis/zlayt-pm-project archive 172028c | tar -x -C <scratch>/archive-head; set that copy's source_commit to '1'*40; .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 83 passed, 3 skipped (SKIPPED [2] at :636, SKIPPED [1] at :661). The unforged copy gives the same 83 passed, 3 skipped.",
   "why_it_matters": "The r2 fix as specified (skip only when there is no repository) is implemented, and in a git checkout a forged header now fails (M1: 2 failed, 0 skipped). But a shipped copy without .git reports green with the provenance guard off, and the skip shows only as a count. Minor because the skip is explicit and the normal submission has history; the open question is whether a .git-less copy is ever what gets graded.",
   "fix": "When there is no repository, fail unless an explicit opt-out variable is set by the export step (for example CALIBRATION_EXPORT_NO_GIT=1), so an export that is meant to be checked cannot skip the guard silently.",
   "acceptance_test": "In a git-less copy with source_commit = '1'*40 and no opt-out variable, the selector reports at least one failed test and no skipped provenance tests."},
  {"severity": "nit",
   "title": "git_source's catch-all discards the reason git failed",
   "evidence": "evals/run.py:76-77 'except Exception: return {\"commit\": None, \"clean\": None, \"tree\": None}' (the except line predates r3; r3 added the tree key to the same return). The None state is explicit and the header test fails on it, so this is not silent.",
   "why_it_matters": "A missing git binary, a timeout and a non-repository all look the same in the header. Not a blocker; it hides the cause when the header comes out None.",
   "fix": "Catch subprocess.CalledProcessError, FileNotFoundError and subprocess.TimeoutExpired, and print the reason to stderr.",
   "acceptance_test": "git_source on a directory with no repository prints a reason to stderr and still returns the None state."},
  {"severity": "nit",
   "title": "The served shape in the T-096 note omits the provenance keys",
   "evidence": "board/cards/T-096.md:26 note lists by_state, by_type, not_scored, sentences, case_count, small_sample, backend and source_commit. evals/reports/calibration.json also carries source_tree_clean, source_tree, hashes, generated_at, cases, models, source and match_rule (key dump in the evidence log, section 7).",
   "why_it_matters": "The UI cannot show that the counts came from a clean tree of the named commit. Not a spec requirement; noted so the frontend does not assume the field carries it.",
   "fix": "If the UI should show provenance, add source_tree_clean to the served field and to the T-096 note. Otherwise say in the note that the served field is a subset.",
   "acceptance_test": "The served route's response includes or explicitly excludes source_tree_clean, and the T-096 note matches the route's keys."}
 ],
 "whats_right": [
  "The r2 provenance code and its tests are back in HEAD (a850be0): git show HEAD:evals/run.py has def git_source, and every test def of 823b718 is present at HEAD except one rename.",
  "A forged or unreferenced source_commit now fails in a git checkout (M1 2 failed, M2 1 failed, 0 skipped), a forged source_tree fails (M3), and an edited served sentence makes check-fresh return 1 (M5b).",
  "calibration.json regenerates from git archive b85fc1b: two runs identical except generated_at, and the committed file equals the regeneration except the four git-derived fields; source_tree 3f014d4b... equals git rev-parse b85fc1b^{tree}."
 ],
 "questions_for_chris": [
  "Which card owns the backend route that serves calibration.json: an AC added to T-096, or a new backend card? The T-096 note asks for a backend AC that no card holds; this is the same question as r2.",
  "Is a copy without .git ever what gets graded or shipped? If yes, the provenance guard skips there (finding 2) and needs another check.",
  "Model record: I am running as claude-haiku-5-5 and recorded that id as the brief asked. CLAUDE.md section 6 and the persona expect Sonnet for engineering reviewers. Should reviewer records show the id actually run, or the expected one?"
 ]}
```
