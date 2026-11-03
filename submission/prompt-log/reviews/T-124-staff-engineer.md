# T-124 review: staff-engineer-reviewer (round 1)

**Verdict: pass.** No blocker, no major. The three ids are declared, rendered and used, and the contract test is green on the pinned HEAD. Two minors on the contract test itself (one-directional check, substring match); neither affects T-124's three ids.

## What I ran

- Pinned to `git archive d56328a` (HEAD `d56328a2f6d37d0a09c4a9e14c66e726a417eb82` at review time). Extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-124-r1-head`.
- `pytest tests/unit/test_e2e_contract.py -v -p no:cacheprovider` on that archive: **3 passed**.
- Frontend render, at HEAD (`git grep`) and in the archive: `app/frontend/timeline.js:257` (`sort`, select in the Timeline toolbar); `app/frontend/export.js:37` (`copy-confirm`, role=alert); `app/frontend/export.js:38` (`btn-copy-anyway`); `export.js:40` (focus moves to it when the confirm opens).
- Spec use, at HEAD: `tests/e2e/test_polish_r3.py:99` (`sort`), `:140` and `:290` (`copy-confirm`), `:141` and `:291` (`btn-copy-anyway`).
- Parent `db7f6d0` archive, same test: **1 failed, 2 passed**; failure `AssertionError: ['copy-confirm', 'sort', 'btn-copy-anyway']`. The card's two added lines are what turn it green.
- Card diff: `git show d56328a --numstat` gives `2 0 tests/e2e/conftest.py` (2 insertions, 0 deletions, no id renamed or dropped).
- Mutation A (`artifacts/review-evidence/T-124-r1/mutA`): `export.js:37` renamed `copy-confirm` to `copy-confirm-gone`. Contract test: **3 passed**. The check never looks at the frontend.
- Mutation B (`artifacts/review-evidence/T-124-r1/mutB`): added `tests/e2e/test_probe_zz.py:3` with `get_by_test_id("btn-copy")`, an id not declared anywhere. Contract test: **3 passed** (`btn-copy` is a substring of the declared `btn-copy-letter`, `conftest.py:8`).
- `artifacts/review-evidence/T-124-r1/exact_token_check.py` on the HEAD archive: 162 spec ids, **0** that pass only as a substring of a declared id. The B hole is latent today.
- Working tree: `git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py` shows 8 modified frontend files (uncommitted, not part of this card). The three ids are still present in the working tree (`timeline.js:303`, `export.js:37-40`), but I reviewed HEAD only.
- Read-only: `curl http://localhost:7860/api/health` (fixture backend, live tree).

**Not run:** `tests/e2e/test_polish_r3.py` itself. It needs a fixture server on a pinned tree; the live server on 7860 serves the dirty working tree, and the brief asked for the three checks above only. Use of the ids is established by grep, not by a run.

## Findings

1. **minor, contract check is one-directional.** The contract test only asserts spec → contract. A declared id that the frontend stops rendering still passes (Mutation A). The T-124 drift came from the same gap in the other direction. The docstring's "all already rendered by the frontend" is true at HEAD but unenforced. Fix: add a unit test that every id named in the contract's test-id lists appears as a `data-testid` literal in `app/frontend`. Acceptance: Mutation A fails it; HEAD passes it.
2. **minor, the id check matches substrings.** `tests/unit/test_e2e_contract.py:22` uses `if pat not in c`. An undeclared id that is a substring of a declared one passes (Mutation B). Latent: no current spec relies on it (exact-token scan: 0 of 162). Fix: match whole tokens, e.g. `re.search(r"(?<![\w-])" + re.escape(pat) + r"(?![\w-])", c)`. Acceptance: Mutation B fails with `['btn-copy']`; HEAD still passes with 162 ids.

No blocker: no money, LLM, fallback, or network path is touched by this diff.

## Scores

| criterion | score |
|---|---|
| frontend renders each declared id | 5 |
| specs use each declared id | 5 |
| contract test green on pinned HEAD | 5 |
| contract test fails when an id is removed | 4 |
| contract test enforcement strength (both directions, whole tokens) | 3 |

## What's right

- All three ids are rendered at HEAD with the behaviour the contract text describes (`timeline.js:257`, `export.js:37-40`).
- The change is two docstring lines, no renames or drops. Parent `db7f6d0` fails with exactly these three ids and HEAD passes 3/3.
- The contract entry names the file and behaviour of each id, so the next reader can find the hook without grepping.

```json
{"card": "T-124", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d56328a (tests/e2e/conftest.py, +2 lines); pinned to git archive d56328a (HEAD d56328a2f6d37d0a09c4a9e14c66e726a417eb82); live app http://localhost:7860 read-only (/api/health) only; sample case not run",
 "exercised": [
   "read personas/staff-engineer.md, board show T-124, git show d56328a --numstat and diff",
   "git archive d56328a -> scratchpad T-124-r1-head; pytest tests/unit/test_e2e_contract.py -v -p no:cacheprovider: 3 passed",
   "git grep HEAD app/frontend for sort, copy-confirm, btn-copy-anyway: timeline.js:257, export.js:37, :38, :40",
   "grep HEAD tests/e2e/test_polish_r3.py for the three ids: lines 99, 140, 141, 290, 291",
   "git archive db7f6d0 (parent) contract test: 1 failed, missing ['copy-confirm','sort','btn-copy-anyway']",
   "Mutation A artifacts/review-evidence/T-124-r1/mutA: export.js:37 id renamed; contract test 3 passed",
   "Mutation B artifacts/review-evidence/T-124-r1/mutB: spec uses undeclared btn-copy; contract test 3 passed",
   "artifacts/review-evidence/T-124-r1/exact_token_check.py on HEAD archive: 162 ids, 0 substring-only",
   "git diff --stat HEAD -- app/frontend tests/e2e tests/unit/test_e2e_contract.py: working tree dirty (8 frontend files), HEAD reviewed",
   "curl GET http://localhost:7860/api/health: ok, backend fixture",
   "NOT run: tests/e2e/test_polish_r3.py (needs a fixture server on the pinned tree)"],
 "verdict": "pass",
 "scores": {"frontend_renders_declared_ids": 5, "specs_use_declared_ids": 5, "contract_test_green_on_pinned_head": 5, "contract_test_fails_when_id_removed": 4, "contract_enforcement_strength": 3},
 "findings": [
   {"severity": "minor", "title": "Contract check is one-directional: a declared id the frontend stops rendering still passes",
    "evidence": "artifacts/review-evidence/T-124-r1/mutA/app/frontend/export.js:37 renamed data-testid copy-confirm -> copy-confirm-gone; cd artifacts/review-evidence/T-124-r1/mutA && .venv/bin/python -m pytest tests/unit/test_e2e_contract.py -q -p no:cacheprovider -> 3 passed",
    "why_it_matters": "The conftest says every declared id is rendered; nothing checks it. T-124 was the same gap seen from the other side (spec ids missing from the contract).",
    "fix": "Add a unit test that every id listed in the tests/e2e/conftest.py contract appears as a data-testid literal in app/frontend (object-literal or attribute form).",
    "acceptance_test": "Mutation A fails the new test naming copy-confirm; HEAD d56328a passes it."},
   {"severity": "minor", "title": "Id check matches substrings: an undeclared id inside a declared one passes",
    "evidence": "tests/unit/test_e2e_contract.py:22 `if pat not in c`; artifacts/review-evidence/T-124-r1/mutB/tests/e2e/test_probe_zz.py:3 get_by_test_id(\"btn-copy\"); tests/e2e/conftest.py:8 declares btn-copy-letter; contract test 3 passed. Latent: artifacts/review-evidence/T-124-r1/exact_token_check.py finds 0 of 162 HEAD ids relying on a substring.",
    "why_it_matters": "R-ST-1 is the only enforcement that spec hooks are named in the contract; a substring match lets a typo or a truncated id through.",
    "fix": "Match whole tokens: re.search(r\"(?<![\\w-])\" + re.escape(pat) + r\"(?![\\w-])\", c) in test_every_test_id_is_declared.",
    "acceptance_test": "Mutation B fails with ['btn-copy']; HEAD d56328a still passes with all 162 ids."}
 ],
 "whats_right": [
   "All three ids are rendered at HEAD with the behaviour the contract describes (timeline.js:257; export.js:37-40).",
   "The change is two docstring lines with no renames or drops; parent db7f6d0 fails with exactly these three ids and HEAD passes 3/3.",
   "The contract entry names each id's file and behaviour, so the hook is findable without grep."],
 "questions_for_chris": []}
```
