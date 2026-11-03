# T-090 round 2 review: calibrated confidence, provenance and majors (commits 823b718, 02ff244)

**Verdict: fail.** The file itself reproduces exactly from its source commit 823b718, and the r1 majors are mostly fixed in the commit. But a later commit, 2fca530 (T-087/T-086, sits between 823b718 and 02ff244), deleted the r2 code and its 11 tests, so HEAD (865b186) has neither. That re-opens the r1 blocker at HEAD. Two more majors and two minors remain.

Method notes. The brief named `git worktree add`, which board-guard blocks in the project tree, so I used a scratch clone of the project with `git checkout --detach 823b718` (same result: a clean tree at 823b718). Scratch evidence is in `artifacts/review-evidence/T-090-staff-r2/` (`mutation-and-command-log.txt`, regenerated `calibration.json` copies). Regeneration used `python -I` with the scratch clone on `sys.path`, fixture backend, `LLM_BACKEND` and `ENABLE_LIVE` unset.

## What reproduces

| Check | Result |
|---|---|
| Regenerate at 823b718, run 1 vs committed file (generated_at removed) | equal |
| Regenerate at 823b718, run 2 vs run 1 | byte-identical except generated_at |
| Counts | verified 83/84, needs_review 10/10 (same as committed) |
| Header | `source_commit` 823b718817cacf6d38cf179724fd374ad09dffdf, `source_tree_clean` true, `backend` fixture, 12 hashes (11 prompts + lexicon), `models` generator claude-sonnet-5-5 / judge claude-haiku-5-5 |
| Percent signs in calibration.json and in the sentence builder | 0 |
| `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` in the project tree | 84 passed, 1284 deselected, 0 skipped |
| Same selector at 823b718 code with the 02ff244 file (scratch clone) | 84 passed, 0 skipped |
| Same selector at 02ff244 (file commit, code as left by 2fca530) | 71 passed |

## Finding 1 (blocker): the r2 fix is not in HEAD

`git show 2fca530 -- evals/run.py` removes `git_source` and reverts the `unscored`/candidate-state changes. `git show 2fca530 -- tests/unit/test_eval_runner.py` removes 11 `^-def test_` lines, including `test_committed_calibration_regenerates_exactly_from_its_source_commit`. `git show 02ff244:evals/run.py | grep -c 'def git_source'` is 0. `git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py` exits 0, so HEAD carries the reverted code. The 84 passed in the project tree comes from uncommitted edits (`git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py`: 383 insertions, and the working-tree `evals/run.py` also differs from 823b718 at line 505). The card's AC evidence therefore cannot be reproduced from HEAD.

The consequence is the r1 blocker again. Running `python -m evals.run` at 02ff244 code overwrites calibration.json without `hashes`, `not_scored`, `source_commit` and `source_tree_clean`, and the sentences change (`artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json`). The committed header still names 823b718, and nothing in HEAD can check it.

Why blocker and not major: the shipped provenance guard (the traceability the card exists for) is absent from the committed code, so a rerun at HEAD does not produce the file it ships. I cannot downgrade this because the fix lives in another card's commit.

## Finding 2 (major): a forged source_commit passes by skipping

`tests/unit/test_eval_runner.py:635-638` skips the ancestor test when `cat-file -e <source_commit>^{commit}` fails, labelled "no git history here". `:642-647` skips the regeneration test with "source commit not available in this checkout". So a hand-edited header naming a commit that does not exist passes, with 2 skips. Mutant M-C (`source_commit` = `"1"*40`, 823b718 code, 02ff244 file): `82 passed, 2 skipped`. The brief asked that hand-edits fail the tests. This one does not.

## Finding 3 (major): the served field has no owner

Card AC 1 (board/cards/T-090.md) now reads "served field and UI line are carried by T-096 (frontend)". `python3 tools/board.py show T-096` shows its AC 1 covers only the "Verified items matched the record N/M times in testing" line "(T-090)". No backend route is in any AC. `grep -rln calibration app/` returns nothing (exit 1). The r1 fix asked that the served field be linked to a backend card; the narrowing removed the link rather than adding one.

## Finding 4 (minor): check-fresh passes an edited sentence

The card says check-fresh validates calibration.json. `evals/run.py:962` (`check_calibration`) checks only that by_state equals the sum of by_type and that hashes match the files. With the sentence changed from 83/84 to 84/84 and counts untouched, `R.check_fresh` returns 0 (log item 5). The regeneration test catches it, but only under pytest with git history.

## Finding 5 (minor): the clean flag is not checked by the regeneration test

`tests/unit/test_eval_runner.py:660` sets `fresh["source_tree_clean"] = c["source_tree_clean"]`, copying the file's own value into the comparison. Only the header test (`:629-633`) pins it to true. A file generated from a dirty tree that forges `true` passes both tests. This is minor because the committed file's commit is clean, but the header field is not verified.

## Majors from r1: status

- Blocker (not reproducible): fixed in 823b718/02ff244 (regeneration reproduces); reopened at HEAD by Finding 1.
- Major 2 (AC 1 closed with UI unbuilt): narrowed to the eval side; the UI is claimed by T-096, but the served field is not (Finding 3).
- Major 3 (amount class not tested): fixed. Mutant C1 (drop class term) turns `test_amount_class_is_part_of_the_match` red.
- Major 4 (sentences name no backend): fixed. Mutant C2 (drop backend from caveat) turns 3 parametrized sentence tests red. The fixture sentence reads "on the fixture backend (recorded replies, 10 golden cases, small sample)".
- Minors: 29/30 boundary (C3 killed), tolerated flag (C4 killed), not-scored disclosure (C5 killed), record_warning alignment (C6, candidate state dropped, killed broadly), check-fresh covers calibration.json (partly; Finding 4).

Hand-edit mutants on the 823b718 code with the 02ff244 file: count in by_state (killed, 2 tests), sentence text (killed), count in by_type only (killed, 2 tests), stale hash (killed), clean flag false (killed). Only the forged source_commit survives (Finding 2).

## Outside my lens

The ship bar is not met on the fixture run (`4_no_invented_facts`, determinism and judge controls not measured). Those are existing ship-bar items, not T-090. I did not judge the frontend wording.

```json
{"card": "T-090", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits 823b718 (evals/run.py, tests/unit/test_eval_runner.py) and 02ff244 (evals/reports/calibration.json); HEAD 865b186 checked for the code; scratch clone of the project at detached 823b718 and 02ff244 (git worktree blocked by board-guard); no app URL (no calibration route or UI exists: grep -rln calibration app/ returns nothing); sample case = fixture backend over the 10 golden cases",
 "exercised": [
  "read personas/staff-engineer.md, reviews/T-090-staff-engineer.md (r1), board/cards/T-090.md, board/cards/T-096.md via board.py show",
  "git show --stat 823b718, 02ff244, 2fca530; git show 823b718 -- evals/run.py and -- tests/unit/test_eval_runner.py; git show 2fca530 -- evals/run.py and -- tests/unit/test_eval_runner.py (11 removed test defs, git_source removed)",
  "git clone of the project into scratchpad t090r2/clone, git checkout --detach 823b718; regenerated twice: python -I -c runpy evals.run --out <scratch>/out1 and out2 (fixture); out1 and out2 equal to each other and to evals/reports/calibration.json ignoring generated_at (dict compare True, cmp of lines without generated_at byte-identical)",
  "header check on committed calibration.json: backend fixture, source_commit 823b718817cacf6d38cf179724fd374ad09dffdf, source_tree_clean true, 12 hashes, models; grep -c '%' calibration.json = 0; percent in build_calibration section of 823b718 = 0",
  ".venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' in the project tree: 84 passed, 1284 deselected, 0 skipped",
  "same selector at 823b718 code with the 02ff244 calibration.json in the scratch clone: 84 passed; at 02ff244 (clone detached): 71 passed; at 823b718 with its own pre-r2 file: 3 failed, 81 passed (stale file, not recorded further)",
  "regeneration at 02ff244 code (scratch clone): keys missing vs committed = hashes, not_scored, source_commit, source_tree_clean; by_state equal; sentences differ (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json)",
  "git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exit 0; git diff --stat HEAD -- evals/run.py tests/unit/test_eval_runner.py: 383 insertions; cmp working-tree evals/run.py vs 823b718: differ at line 505; cmp working-tree test_eval_runner.py vs 823b718: identical",
  "hand-edit mutants in scratch clone (823b718 code, 02ff244 file): by_state count +1 -> 2 failed; sentence text -> 1 failed; by_type count -> 2 failed; stale hash -> 1 failed; source_tree_clean false -> 1 failed; source_commit = 1*40 -> 82 passed, 2 skipped (test_eval_runner.py:638, :647)",
  "code mutants in scratch clone evals/run.py (restored from saved pristine copy): drop class term line 271 -> 1 failed; drop backend in caveat line 317 -> 4 failed; CAL_SMALL_N 30->5 line 243 -> 1 failed; drop tolerated term line 279 -> 1 failed; drop Not-scored sentence line 327 -> 1 failed; drop candidate state in to_candidates -> 35 failed, 5 errors",
  "check_fresh(latest.json) with edited sentence, python -I on scratch clone: returned 0",
  "board.py show T-096 (AC 1 text, status ready); grep -rln calibration app/ (no output, exit 1)",
  "full log: artifacts/review-evidence/T-090-staff-r2/mutation-and-command-log.txt"
 ],
 "verdict": "fail",
 "scores": {"counts_reproduce_from_commit": 5, "header_provenance_at_commit": 4, "provenance_guard_at_HEAD": 1, "hand_edit_detected": 3, "r1_majors_fixed": 3, "ac_closed_honestly": 2, "no_bare_percent": 5, "mutants_killed": 4},
 "findings": [
  {"severity": "blocker",
   "title": "The r2 provenance fix and its tests are reverted at HEAD by commit 2fca530; the card's test evidence is not reproducible from HEAD",
   "evidence": "git show 2fca530 -- tests/unit/test_eval_runner.py removes 11 test defs (grep -c '^-def test_' = 11), including test_committed_calibration_regenerates_exactly_from_its_source_commit; git show 2fca530 -- evals/run.py removes def git_source (git show 02ff244:evals/run.py | grep -c 'def git_source' = 0). git diff --quiet 02ff244 865b186 -- evals tests/unit/test_eval_runner.py exits 0, so HEAD has the reverted code. Selector at 02ff244: 71 passed (no r2 tests). Project-tree 84 passed comes from uncommitted edits (git diff --stat HEAD: evals/run.py and tests/unit/test_eval_runner.py, 383 insertions). Regeneration at 02ff244 code omits hashes, not_scored, source_commit, source_tree_clean (artifacts/review-evidence/T-090-staff-r2/regen-02ff244-code/calibration.json).",
   "why_it_matters": "This is the r1 blocker again. The served calibration.json names a source commit whose provenance guard is no longer in the shipped code, so a rerun of python -m evals.run at HEAD overwrites the file with one that has no provenance. The tests that were supposed to fail on a hand edit do not exist at HEAD, so the card's '84 passed' cannot be reproduced from the commits it lists. The 823b718 and 02ff244 commits themselves are correct; the loss happened after them.",
   "fix": "Restore the 823b718 versions of evals/run.py and tests/unit/test_eval_runner.py in a new commit that stages those two paths explicitly (git show 823b718:evals/run.py and :tests/unit/test_eval_runner.py are the reference). Do not hand-merge the uncommitted working-tree edits, which differ from 823b718 in evals/run.py (first difference at line 505). Ask the author of 2fca530 to stage by explicit path; the commit staged a stale evals/run.py and test file.",
   "acceptance_test": "git show HEAD:evals/run.py | grep -c 'def git_source' is at least 1; at the new HEAD, .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' reports 84 passed with 0 skipped from a clean tree; a regeneration at HEAD (fixture, --out) equals evals/reports/calibration.json ignoring generated_at."},
  {"severity": "major",
   "title": "A forged source_commit that names no existing commit passes the two provenance tests by skipping",
   "evidence": "tests/unit/test_eval_runner.py:635-638 (skip 'no git history here (shallow or exported tree)' when cat-file -e <source_commit>^{commit} fails) and :642-647 (skip 'source commit not available in this checkout'). Mutant on scratch clone (823b718 code, 02ff244 file, source_commit set to '1'*40): .venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' -> 82 passed, 2 skipped.",
   "why_it_matters": "The brief requires the tests to fail when the file is hand-edited. A header that cites a commit which does not exist is the provenance lie the card was opened to stop, and it is reported green. The skip conflates 'no git at all' (a legitimate export) with 'the cited commit is missing' (a fabricated header).",
   "fix": "Skip only when there is no git repository (git rev-parse --git-dir fails). When a repository exists and the cited commit is missing, or the commit is not an ancestor of HEAD, fail with the commit name.",
   "acceptance_test": "Set source_commit to '1'*40 in calibration.json; the selector reports at least one failed test and no skip for the provenance tests."},
  {"severity": "major",
   "title": "The served calibration field has no owner after AC 1 was narrowed",
   "evidence": "board/cards/T-090.md AC 1 evidence: 'served field and UI line are carried by T-096 (frontend)'. python3 tools/board.py show T-096 shows AC 1: 'Dates-to-confirm row ... Verified items matched the record N/M times in testing line with small-sample note (T-090); e2e tests', done false, status ready. No AC names a backend route or a read of evals/reports/calibration.json. grep -rln calibration app/ returns no files (exit 1).",
   "why_it_matters": "The r1 major asked for the served field to be linked to a backend card. The narrowing moved the UI line to T-096 but left the backend route with no card and no AC, so the sentence the paralegal reads has no path to the screen. The card's AC is narrower and honest about the UI, but the handoff to the backend is unowned.",
   "fix": "Add an explicit backend AC (route that returns the calibration.json fields, or null when the file is absent, read-only) to an existing backend card or a new one, and name it in T-090 AC 1 or the T-096 AC.",
   "acceptance_test": "board.py show <owning card> lists the route AC; grep -rn calibration app/backend finds the route; curl of the route returns the sentences.overall.verified string from evals/reports/calibration.json verbatim."},
  {"severity": "minor",
   "title": "check-fresh exits 0 for an edited sentence; it validates sums and hashes only",
   "evidence": "evals/run.py:962 check_calibration checks by_state vs sum of by_type and hashes vs files. Scratch-clone repro (python -I, R.check_fresh on a tmp dir with latest.json and the edited calibration.json, verified sentence changed to '84/84 ...'): returned 0.",
   "why_it_matters": "The card says check-fresh validates calibration.json. A hand-edited sentence, which the UI renders verbatim, passes the freshness command. Only the pytest regeneration test catches it, and that test needs git history.",
   "fix": "Add the calibration.json sentences and not_scored to check_calibration, or regenerate the sentences inside check_calibration from by_state and by_type and compare.",
   "acceptance_test": "Edit sentences.overall.verified in a copy of calibration.json; R.check_fresh returns 1."},
  {"severity": "minor",
   "title": "The regeneration test copies the file's source_tree_clean into the comparison, so a forged clean flag passes",
   "evidence": "tests/unit/test_eval_runner.py:660 fresh[\"source_tree_clean\"] = c[\"source_tree_clean\"] (823b718 numbering). Only the header test (:629-633) asserts the value is True.",
   "why_it_matters": "The clean flag is the only evidence the counts came from an unmodified tree. The regeneration test cannot check it, so a file produced from a dirty tree that says true is indistinguishable from a clean one.",
   "fix": "Record the tree state as a checked value at generation time (for example the tree hash of the tracked files) and compare it to git rev-parse at the source commit in the test, or drop the flag and rely on the commit.",
   "acceptance_test": "A calibration.json whose recorded tree hash differs from the source commit's tree fails the regeneration test."}
 ],
 "whats_right": [
  "calibration.json regenerates exactly from its source commit 823b718 (two runs identical except generated_at; counts 83/84 and 10/10), and the header records source_commit, source_tree_clean true, backend fixture and 12 prompt/lexicon hashes.",
  "Hand edits to by_state counts, by_type counts, the sentence text, the hashes and the clean flag each turn at least one test red at 823b718 (mutants M-A, M-B, M-D, M-E, M-G).",
  "Sentences name the backend and '(recorded replies, N golden cases)' for the fixture, no percent sign appears anywhere, and the r1 amount-class, tolerated, 29/30 boundary and not-scored mutants are each killed."
 ],
 "questions_for_chris": [
  "Which card should own the backend route that serves calibration.json: a new backend card, or an AC added to T-096?"
 ]}
```
