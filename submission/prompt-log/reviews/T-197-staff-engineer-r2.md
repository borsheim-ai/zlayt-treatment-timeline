# T-197 r2 review (staff-engineer): guided UI reads health.local_mode

**Verdict: pass** (0 blockers, 0 majors, 3 minors, 1 nit).

**Reviewed sha: 9ab8cae**, the commit the brief names. HEAD was 9ab8cae at my first `git rev-parse HEAD` and moved to e425534 during the review (`fix(backend): T-177 r5 ...`). e425534 changes only `app/backend/review.py`, `app/backend/why.py` and `tests/unit/test_prepared_property.py`, so every finding below holds at both. I re-ran the first-paint tests at e425534 as well. The working tree is dirty and was not reviewed, except for the index state named in finding 2. Model recorded is claude-haiku-5-5, the model I ran as; the dossier expected claude-sonnet-5-5.

## Brief checks
1. **The guided frontend reads `health.local_mode`: met.** `grep -rn local_mode app/frontend` in the 9ab8cae archive prints `core.js:84` (a comment), `home.js:119` and `step1.js:28`. Both reads are `hl.local_mode !== false`, on the object returned by `G.healthNow` (core.js:86).
2. **The named test is committed, has no xfail, and passes with E2E_REQUIRE_DB=1: met.** `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py` succeeds. `git grep -n -E "xfail|skip" 9ab8cae -- tests/e2e/guided/test_round2.py` prints nothing (exit 1). In the archive, `E2E_REQUIRE_DB=1 ... -k "first_paint or health_says_local_mode_is_false"` gives 3 passed.

## Does the named test catch a regression?
Yes. I made scratch copies of the archive with each gate forced to `true` (exact-count replacement, count 1 each). Each mutant was run against the named test:
- control (unmutated): 1 passed.
- step1.js:28 forced: 1 failed, with `http 404: .../api/library` in the seen list.
- home.js:119 forced: 1 failed, with `http 404: .../api/cases`.
- both forced: 1 failed, with four entries.

## r1 findings at 9ab8cae
- major, card AC1 e2e half not met: **closed.** The test is committed and passes, and both frontend reads exist.
- minor, api.md:57 stated present-tense UI behaviour that was false: **closed.** Both readers now exist, so the sentence is true at 9ab8cae.
- nit, api.md:17 row omits local_mode: **open**, see finding 4.

## Findings

**minor 1: when `/api/health` fails, the page still probes the two routes it should not.**
- Evidence: `core.js:89` is `catch (e) { if (e && e.name === "AbortError") throw e; return {}; }`. With `{}`, `hl.local_mode` is undefined, so `!== false` is true and the page takes the probe branch (`home.js:119`, `step1.js:28`). Repro: in the 9ab8cae archive, a public server (ZLAYT_MODE unset) with `**/api/health` aborted in the browser. `.venv/bin/python <scratch>/T197_r2_scripts/health_fail_probe.py <archive> 7881` printed `/ api requests: ['/api/health', '/api/cases']` and `/new api requests: ['/api/health', '/api/library']`. The named test does not run this path (`test_round2.py:124-133` needs a reachable health).
- Why it matters: the card title says the guided UI never probes these routes in public mode. When the mode is unknown the page guesses local, and the error from health is turned into a default (checklist item 12: errors should reach an explicit status). The probes are caught (`home.js:122-124` falls through to this browser's tokens on 404; `step1.js:28` sets `lib = null`), so no wrong data appears and nothing is exposed. The cost is two 404s on first paint, the failure the card names, with no test guarding this cause. I rate it minor because the AC's literal scope is the health field, not a failed health call. If Chris reads the AC as covering a failed health call, it becomes major.
- Fix: choose the unknown-mode behaviour explicitly. Either (a) probe only on `hl.local_mode === true`, and show a plain "could not reach the server" state when health fails, or (b) keep probing and write that as the accepted degraded path in `memory/contracts/api.md`. Either way, add the test below.
- Acceptance test: in a public server fixture, abort `**/api/health`, load `/` and `/new`, and assert no request matching `/api/(cases|library)$` (the regex the test at `test_round2.py:140` uses). Under option (a), also assert the visible state.

**minor 2: the index has the named test staged for deletion, and an untracked copy in the working tree.**
- Evidence: `git status --short -- tests/e2e/guided` prints `D  tests/e2e/guided/test_round2.py` and `?? tests/e2e/guided/test_round2.py`, with `MM` on `_helpers.py`, `test_step1.py` and `test_step3.py`. The file is committed at 9ab8cae, so the committed state is right.
- Why it matters: CLAUDE.md requires a pathspec commit because the index is shared. A plain `git commit` by anyone would commit the staged deletion and remove the AC's named test. This does not change the verdict, which is about the commit.
- Fix: the owner unstages the deletion (`git restore --staged tests/e2e/guided/test_round2.py`) and commits by pathspec. I did not run this.
- Acceptance test: `git diff --cached --name-only | grep -c test_round2` prints 0, and `git status --short -- tests/e2e/guided/test_round2.py` has no `D` in the first column.

**minor 3: the card's closing commit is not on the card.**
- Evidence: `python3 tools/board.py show T-197` shows `status: "in_review"` and `commits: ["612dc2c"]`. `git log --oneline -i --grep=T-197` lists only `612dc2c feat(backend): GET /api/health reports local_mode (T-197)`. `git log -1 --format=%B 9ab8cae | grep -c T-197` prints 0. The subject of 9ab8cae is `fix(frontend): T-181 r2 guided UI: ... no first-paint 404 via health.local_mode ...`.
- Why it matters: AC1's e2e half is evidenced by 9ab8cae, but the board does not list that commit and the subject does not cite T-197. A reader who searches by card finds only the backend commit.
- Fix: record 9ab8cae against T-197 on the board (through the backend worker or the orchestrator, using `board.py`), and cite T-197 in the next commit that touches this area.
- Acceptance test: `python3 tools/board.py show T-197` lists `9ab8cae` in `commits`.

**nit 4: `memory/contracts/api.md:17` still omits local_mode.**
- Evidence: `git show 9ab8cae:memory/contracts/api.md | sed -n 17p` prints `| GET | \`/api/health\` | backend, demo mode, models, limits, banner text |`. The full shape at `:50` and the prose at `:57` are correct.
- Fix: add "local mode flag" to the row.
- Acceptance test: `git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode` prints 1.

## Exercised
- `python3 tools/board.py show T-197`: `in_review`, commits `["612dc2c"]`.
- `git rev-parse HEAD`: 9ab8cae at the first call; e425534 at the last call.
- `git archive 9ab8cae | tar -x` into a unique scratch directory. The archive has no `.venv`, so I used the project `.venv/bin/python`. `python -I -c` with `sys.path.insert(0, '.')` confirmed that `import app` resolves to the archive.
- `grep -rn local_mode app/frontend` in the archive: core.js:84, home.js:119, step1.js:28. `diff -q` of the archive's `step1.js` and `home.js` against `git show 9ab8cae:...`: identical.
- `git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py`: present. `git grep -n -E "xfail|skip" 9ab8cae -- tests/e2e/guided/test_round2.py`: no output.
- Archive: `E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider "tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server" -v -rs`: 1 passed in 1.96s.
- Archive: `E2E_REQUIRE_DB=1 ... -k "first_paint or health_says_local_mode_is_false" -v`: 3 passed (local first paint, public first paint, health false).
- Mutant copies of the archive (`mutate_fe.py`, run with `-I`): none, step1, home, both, as in the section above.
- `health_fail_probe.py` (aborted `/api/health`, public server on port 7881): output quoted in finding 1. The server was stopped; `lsof -nP -iTCP:7881 -sTCP:LISTEN` is empty afterwards.
- Archive at 9ab8cae: `.venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q`: 3 passed. `tests/unit -q`: 5856 passed, 11 skipped in 383.60s.
- `git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md`: empty, so the backend and the unit tests are unchanged since r1.
- Archive at e425534 (`git archive e425534`): the same 3-test `-k` subset with `E2E_REQUIRE_DB=1`: 3 passed.
- `git status --short -- tests/e2e/guided`: the index state quoted in finding 2.
- Read `app/frontend/guided/home.js:117-124`, `step1.js:27-29`, `core.js:86-90`, `tests/e2e/guided/test_round2.py:83-137`, `tests/e2e/guided/test_shell_smoke.py:20-26` (watch), `app/backend/api.py:266`, `memory/contracts/api.md:17, 50, 57`.

**Not exercised:** the dirty working tree; a live server on :7860; the full `test_round2.py` file (only the named test and the 3-test subset); a browser first paint on the local server beyond that subset.

## What is right
- The frontend reads are gated on the server's field, and removing either gate fails the named test with the exact 404 URL (see above). The test catches the regression.
- The named test has no xfail or skip at 9ab8cae. It asserts the server precondition `health.get("local_mode") is False` (`test_round2.py:132`) before the first-paint check, so it cannot pass on a server that dropped the field.
- r1's minor is closed: api.md:57 is true at 9ab8cae because the frontend reads the field.

## Questions for Chris
- When `/api/health` fails, should the guided UI keep probing (today) or show an explicit "could not reach the server" state? Finding 1 needs that choice.

```json
{"card": "T-197", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "Commit 9ab8cae (fix(frontend) T-181 r2, carries the T-197 frontend half): app/frontend/guided/{core,home,step1}.js, tests/e2e/guided/test_round2.py, memory/contracts/api.md; app/backend/api.py unchanged since 612dc2c. HEAD moved 9ab8cae -> e425534 during the review (e425534 touches app/backend/review.py, why.py, tests/unit/test_prepared_property.py only); the named test was re-run at e425534. No app URL on :7860; sample case not run (outside the AC). Working tree dirty, not reviewed except the index state in finding 2.",
 "exercised": [
  "python3 tools/board.py show T-197 -> status in_review, commits [\"612dc2c\"]",
  "git rev-parse HEAD -> 9ab8cae at first call, e425534 at last call; git log --oneline -4",
  "git archive 9ab8cae | tar -x into a unique scratch dir; project .venv/bin/python -I -c confirms import app resolves to the archive",
  "grep -rn local_mode app/frontend (archive) -> core.js:84, home.js:119, step1.js:28; diff -q of step1.js and home.js against git show 9ab8cae -> identical",
  "git cat-file -e 9ab8cae:tests/e2e/guided/test_round2.py -> present; git grep -n -E 'xfail|skip' 9ab8cae -- tests/e2e/guided/test_round2.py -> no output",
  "archive: E2E_REQUIRE_DB=1 .venv/bin/python -m pytest -p no:cacheprovider tests/e2e/guided/test_round2.py::test_no_failed_request_on_first_paint_in_a_public_server -v -rs -> 1 passed in 1.96s",
  "archive: E2E_REQUIRE_DB=1 ... -k 'first_paint or health_says_local_mode_is_false' -v -> 3 passed",
  "mutants (scratch copies via mutate_fe.py under python -I, count-asserted): control 1 passed; step1 gate forced 1 failed (http 404 /api/library); home gate forced 1 failed (http 404 /api/cases); both forced 1 failed",
  "health_fail_probe.py under the venv on the archive, port 7881, /api/health aborted in the browser: / requests ['/api/health','/api/cases']; /new requests ['/api/health','/api/library']; server stopped, port empty afterwards",
  "archive: .venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_api_routes.py -k health -q -> 3 passed; tests/unit -q -> 5856 passed, 11 skipped in 383.60s",
  "git diff --stat 612dc2c 9ab8cae -- app/backend tests/unit memory/contracts/api.md -> empty",
  "archive at e425534: E2E_REQUIRE_DB=1 -k 'first_paint or health_says_local_mode_is_false' -> 3 passed",
  "git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'",
  "git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0",
  "git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> row without local_mode",
  "read app/frontend/guided/home.js:117-124, step1.js:27-29, core.js:86-90, tests/e2e/guided/test_round2.py:83-137, tests/e2e/guided/test_shell_smoke.py:20-26, app/backend/api.py:266, memory/contracts/api.md:17,50,57",
  "not exercised: dirty working tree; live server on :7860; full test_round2.py file; browser first paint on the local server beyond the 3-test subset"
 ],
 "verdict": "pass",
 "scores": {"ac1_named_e2e_committed_and_passing": 5, "frontend_reads_local_mode": 5, "test_catches_removed_gate": 5, "failure_visible_when_health_fails": 2, "index_and_board_hygiene": 3, "api_md_documents_field": 4, "unit_suite_green": 5},
 "findings": [
  {"severity": "minor",
   "title": "When /api/health fails, the guided UI still probes /api/cases and /api/library",
   "evidence": "app/frontend/guided/core.js:89 'catch (e) { if (e && e.name === \"AbortError\") throw e; return {}; }'; home.js:119 and step1.js:28 'if (hl.local_mode !== false)'. Repro: public server, /api/health aborted in browser; health_fail_probe.py printed \"/ api requests: ['/api/health', '/api/cases']\" and \"/new api requests: ['/api/health', '/api/library']\".",
   "why_it_matters": "Fail-open default: with an unknown mode the page guesses local and probes the routes the card says it never probes in public mode. The 404s are caught (home.js:122-124, step1.js:28), so no wrong data or exposure. Cost is two visible 404s on first paint and no test for this cause. Checklist item 12 expects an explicit status, not a default. Minor because the AC covers the health field, not a failed health call; major if Chris reads the AC that way.",
   "fix": "Choose explicitly: (a) probe only when hl.local_mode === true and show a plain 'could not reach the server' state on failure, or (b) keep probing and record that as the accepted degraded path in memory/contracts/api.md. Add the test either way.",
   "acceptance_test": "Public server fixture with **/api/health aborted: load / and /new; assert no request matching /api/(cases|library)$; under option (a) assert the visible state."},
  {"severity": "minor",
   "title": "Index has tests/e2e/guided/test_round2.py staged for deletion, with an untracked copy in the worktree",
   "evidence": "git status --short -- tests/e2e/guided -> 'D  tests/e2e/guided/test_round2.py' and '?? tests/e2e/guided/test_round2.py'. The file is committed at 9ab8cae (git cat-file -e succeeds).",
   "why_it_matters": "CLAUDE.md requires pathspec commits because the index is shared. A plain git commit would commit the staged deletion and remove the AC's named test. The committed state is correct, so the verdict does not change.",
   "fix": "The owner runs git restore --staged tests/e2e/guided/test_round2.py and commits by pathspec. Not run by this reviewer.",
   "acceptance_test": "git diff --cached --name-only | grep -c test_round2 prints 0; git status --short -- tests/e2e/guided/test_round2.py shows no D in the first column."},
  {"severity": "minor",
   "title": "The closing commit 9ab8cae is not recorded on T-197",
   "evidence": "python3 tools/board.py show T-197 -> status in_review, commits [\"612dc2c\"]; git log --oneline -i --grep=T-197 -> 612dc2c only; git log -1 --format=%B 9ab8cae | grep -c T-197 -> 0.",
   "why_it_matters": "AC1's e2e half is evidenced by 9ab8cae, which the board does not list and whose subject (T-181 r2) does not cite T-197. A search by card finds only the backend commit.",
   "fix": "Record 9ab8cae against T-197 on the board through the backend worker or the orchestrator, using board.py. Cite T-197 in the next commit in this area.",
   "acceptance_test": "python3 tools/board.py show T-197 lists 9ab8cae under commits."},
  {"severity": "nit",
   "title": "memory/contracts/api.md:17 health row still omits local_mode",
   "evidence": "git show 9ab8cae:memory/contracts/api.md | sed -n 17p -> '| GET | `/api/health` | backend, demo mode, models, limits, banner text |'. The full shape at :50 and prose at :57 are correct.",
   "why_it_matters": "Discoverability in the summary table only. Carried from r1 and not yet fixed.",
   "fix": "Add 'local mode flag' to the row.",
   "acceptance_test": "git show <sha>:memory/contracts/api.md | sed -n 17p | grep -c local_mode prints 1."}
 ],
 "whats_right": [
  "Both frontend reads are gated on the server's local_mode field (home.js:119, step1.js:28), and removing either gate fails the named test with the exact 404 URL, so the test catches the regression.",
  "The named test has no xfail or skip at 9ab8cae and asserts health.get('local_mode') is False (test_round2.py:132) before the first-paint check, so it cannot pass on a server that dropped the field.",
  "The r1 minor is closed: api.md:57 is true at 9ab8cae because the frontend now reads the field."
 ],
 "questions_for_chris": ["When /api/health fails, should the guided UI keep probing (today) or show an explicit 'could not reach the server' state? Finding 1 needs that choice."]}
```
