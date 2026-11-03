# T-210 review (staff-engineer-reviewer), commit ad0d91a

Verdict: **pass**. No blocker, no major. One minor.

Model note: the brief expected `claude-sonnet-5-5`, but this session runs as `claude-haiku-5-5`, so the record uses `claude-haiku-5-5`.

Summary. All five declared ids are real: each is a literal `data-testid` in the guided shell that the backend serves at `/` (D-068). The docstring descriptions match the render sites. The commit touches one docstring line (`tests/e2e/conftest.py:102`), and no test, skip or assertion changed. The parent commit 0281189 reproduces the red with exactly these five ids missing. From a `git archive ad0d91a` copy, the contract test passes (3 passed) and the full unit suite passes (6267 passed, 12 skipped), matching the card's AC evidence.

Minor. The unit contract test is a text-presence check on the docstring (`tests/unit/test_e2e_contract.py:22`, `pat not in c`). A frontend that stops rendering one of these ids keeps the unit suite green; I proved this with a scratch mutant. For `btn-draft` and `draft-done`, the only check that ties them to the frontend is the E2E spec, which is not in the unit suite. This is not a D.2 spec violation, because R-ST-1 only requires spec hooks to be named in the contract, and that holds.

Exercised (all commands run from `/Users/arsis/zlayt-pm-project` unless noted; HEAD at review time = `ad0d91a`, confirmed by `git rev-parse HEAD`):
1. `git show ad0d91a --stat` and `git show ad0d91a -- tests/e2e/conftest.py`: one insertion, at `tests/e2e/conftest.py:102`.
2. `python3 tools/board.py show T-210`: status in_review, AC 1 done with the 6267/12 evidence.
3. `git archive ad0d91a | tar -x` into the session scratchpad (`T210-archive`); `git archive 0281189` into `T210-parent`.
4. Frontend presence, grep at ad0d91a: `brand` at `app/frontend/guided/app.js:63` (header link to `/`); `footer-note` at `guided/app.js:56`; `demo-badge` at `guided/app.js:66` (a header pill, rendered only when `p.label` is set; `G.provenance` at `guided/app.js:45-49` returns the neutral line while health is pending); `btn-draft` at `guided/step1.js:203` ("Draft the timeline", in `drawFound`); `draft-done` at `guided/step1.js:270` ("Records added", in `drawDone`).
5. Shipped at `/`: `app/backend/api.py:681-711` (the guided `index.html` is the front door; `GuidedFiles` mounted at `/` on line 711).
6. `/Users/arsis/zlayt-pm-project/.venv/bin/python -I -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider` in `T210-archive`: `3 passed in 0.03s`.
7. Same invocation on `tests/unit` in `T210-archive`: `6267 passed, 12 skipped in 405.55s`.
8. Same contract test in `T210-parent`: `1 failed, 2 passed`; `AssertionError: ['footer-note', 'draft-done', 'btn-draft', 'demo-badge', 'brand']`. Substring counts of the five ids in the parent docstring: all 0.
9. Mutant (scratch copy only): removed `"data-testid": "btn-draft", ` from `guided/step1.js:203` in `T210-archive`. The contract test still reported `3 passed`. I restored the file and confirmed with `cmp` against `git show ad0d91a:app/frontend/guided/step1.js`.
10. `grep` of the five ids under `tests/unit` at ad0d91a: no hits. `test_e2e_contract.py` reads only `tests/e2e` (lines 4-11), never `app/frontend`.

Not exercised: the E2E specs (`tests/e2e/test_prepared_first_paint.py:304` uses `demo-badge`, `:320` uses `btn-draft` and `draft-done`) were not run, because no server or browser was started. The pipeline CLI was not run, because it is outside the card's scope. The working tree has uncommitted changes from other agents; I did not review them, and this review covers the committed tree at ad0d91a.

Findings:
- Minor (should fix, not a spec violation): the contract test matches substrings of the docstring, so it cannot detect a frontend id that was removed. See item 9 above.

What is right:
- All five ids are literal `data-testid` attributes on the shipped guided shell, and each docstring description matches its render site.
- The fix is one docstring line; no test, skip or assertion was weakened, and the parent red reproduces with exactly these five ids.
- The unit suite from a git archive reproduces the card's numbers (6267 passed, 12 skipped).

```json
{"card": "T-210", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit ad0d91a (HEAD at review time; diff = tests/e2e/conftest.py:102 only); app URL: none started; sample case: n/a",
 "exercised": [
  "git show ad0d91a --stat; git show ad0d91a -- tests/e2e/conftest.py (1 insertion at conftest.py:102)",
  "python3 tools/board.py show T-210 (status in_review, AC 1 done with 6267/12 evidence)",
  "git archive ad0d91a | tar -x into scratchpad T210-archive; git archive 0281189 | tar -x into scratchpad T210-parent",
  "grep -rn of the five ids under app/ at ad0d91a: brand guided/app.js:63; footer-note guided/app.js:56; demo-badge guided/app.js:66; btn-draft guided/step1.js:203; draft-done guided/step1.js:270",
  "read G.provenance guided/app.js:45-49 (demo-badge gating) and app/backend/api.py:681-711 (guided shell served at /)",
  ".venv/bin/python -I -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider in T210-archive: 3 passed",
  ".venv/bin/python -I -m pytest tests/unit -q -p no:cacheprovider in T210-archive: 6267 passed, 12 skipped in 405.55s",
  "same contract test in T210-parent (0281189): 1 failed, 2 passed; missing ['footer-note', 'draft-done', 'btn-draft', 'demo-badge', 'brand']",
  "mutant in T210-archive scratch copy: removed the btn-draft data-testid at guided/step1.js:203; contract test still 3 passed; file restored and cmp-verified against git show ad0d91a",
  "grep of the five ids under tests/unit at ad0d91a: no hits; test_e2e_contract.py reads only tests/e2e (lines 4-11)"
 ],
 "verdict": "pass",
 "scores": {"declared_ids_exist_in_frontend": 5, "declarations_match_render_sites": 5, "no_test_weakening": 5, "unit_suite_reproducible_from_archive": 5, "contract_test_detects_frontend_removal": 2},
 "findings": [
  {"severity": "minor",
   "title": "Contract test is a docstring substring check; a removed frontend id keeps it green",
   "evidence": "tests/unit/test_e2e_contract.py:22 `if pat not in c and not (...)` with c = docstring (line 7); mutant run: removing the btn-draft data-testid at app/frontend/guided/step1.js:203 leaves `3 passed`",
   "why_it_matters": "A frontend that stops rendering one of these ids stays green in the unit suite. For btn-draft and draft-done the only check is the E2E spec tests/e2e/test_prepared_first_paint.py:320, which is not in tests/unit. Not a D.2 spec violation: R-ST-1 only requires spec hooks to be named in the contract, and that holds.",
   "fix": "In tests/unit/test_e2e_contract.py, match whole id tokens in the docstring rather than substrings; and for each declared id, assert that the literal id follows a data-testid key in app/frontend (source grep, so state-gated elements such as draft-done still pass).",
   "acceptance_test": "With the btn-draft data-testid removed from guided/step1.js:203, the unit contract test fails and names btn-draft; with the line restored it passes; full tests/unit still green from git archive."}
 ],
 "whats_right": [
  "All five ids are literal data-testid attributes on the shipped guided shell, and each docstring description matches its render site.",
  "The fix is one docstring line; no test, skip or assertion was weakened, and the parent red reproduces with exactly these five ids.",
  "The unit suite from a git archive reproduces the card's numbers (6267 passed, 12 skipped)."
 ],
 "questions_for_chris": ["Should R-ST-1 require each declared id to exist in app/frontend (the minor finding), or is the E2E spec meant to be the only frontend check?"]}
```
