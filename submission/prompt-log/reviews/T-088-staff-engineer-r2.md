# T-088 round-2 review: date-convention suggestion (staff-engineer-reviewer)

**Verdict: changes.** The round-1 blocker is closed: the reason now names the record each evidence date sits in, and both names match the golden source. Round-1 minors and the nit are closed. One major stays open: AC 1 is still `done: true` on the board, and its eval half has no card.

Scope: commit 55300e9 (round 2) on top of f667f08. HEAD moved during the review (d3130e3, then 7df65fb, a T-093 commit); I pinned the tree at 7df65fb. The card paths are byte-identical between 55300e9 and 7df65fb.

**Round-1 items**

| Round-1 item | Status | Evidence |
|---|---|---|
| Blocker: reason says "in this record" for dates in other records | Closed | `artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt`: REASON "4 other dates in this packet use month first (Record 2: 02/17/2026) and (Record 6: 03-17-26)"; both records checked against the golden source; mutants R2-88a and R2-88b (old wording) fail named tests |
| Major: AC 1 done while UI and eval are unbuilt | Open (partly corrected) | `board show T-088`: `"done": true`; AC text still names the UI and the eval case; no qa card (see F1) |
| Major: shared index stages deletion of card files | Closed for these four paths | `git diff --cached --name-status -- app/backend/date_convention.py app/backend/dismissal_patterns.py tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py` prints nothing |
| Minor: `and`/`or` precedence in the two-digit-year test | Closed | `tests/unit/test_date_convention.py:65` now `... and (s["iso"] is None or s["iso"] in ...)` |
| Nit: unused `dates` import | Closed | `app/backend/date_convention.py` imports only `re` (line 8) |

**Your checks**
1. Reason names the records (golden case_01 record 8): holds. The ambiguous record is r8 (04/05/2026). Evidence is r2 (02/17/2026) and r6 (03-17-26), and the reason names both. Both dates sit inside `=== Record 2 ===` and `=== Record 6 ===` in `evals/golden/case_01_date_formats.txt`. The packet case in the unit test names Record 1 (`Another date in this packet uses month first (Record 1: 03/14/2026)`).
2. Never auto-applied: holds. `auto_applied: False` (`date_convention.py:66`). The record stays `ambiguous`. A confirm with a non-candidate date returns 422 (probe). The UI pre-select is not built, so nothing reads the suggestion on the server path.
3. AC 1 correction posted, UI moved to T-096: the correction is in the T-088 notes (04:34:55Z) and the UI is on T-096 (`ready`, AC includes the pre-select). **Not done:** the eval half has no card. The T-088 note asks qa to add the case_01 expected.json entry, but `board list --role qa` shows no card for it, and the expected file still has 0 matches for suggestion or dismissal. The AC flag stays `true`, which is F1.

**Findings**
- **F1 (major, open).** AC 1 is `done: true`. The correction is honest, but the gate still reads done. The round-1 options were done=false or a split into cards, and only the UI was split. Fix: set done=false, or amend the AC to the backend half and open a qa card for the eval entry.
- **F2 (minor).** The handoff's "(160 pass)" does not reproduce at the commit. At 7df65fb the selector gives 140 passed. The 160 comes from the dirty main tree, which holds other workers' uncommitted tests. The card's own 30 tests pass in both trees.

**Exercised** (all run by me; exact outputs in the files named)
- `python3 tools/board.py show T-088`, `show T-096`, `list --role qa`.
- `git show 55300e9` for the three in-scope files (full diff read); `git diff 55300e9 7df65fb` for the card paths and their helpers (empty).
- `.venv/bin/python -m pytest -q tests/unit -k "date or dismiss or suggest"`: clean HEAD **140 passed, 1196 deselected**; dirty main tree **160 passed, 1238 deselected**.
- `pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py`: **30 passed** (clean HEAD).
- `pytest tests/unit` on clean HEAD: **6 failed, 1330 passed**. The same 6 fail at 55300e9 (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); none touches the card files. Outside these cards; see below.
- `probe_t088_r2.py` on clean HEAD (`probe_t088_r2_output.txt`).
- `mutate_r2.py` on a scratch copy (`mutation_run_r2.txt`): R2-88a to R2-88h all CAUGHT (singular and plural old wording, dropped and off-by-one record number, auto_applied true, mixed-order, swapped iso, auto-confirm).
- `grep -rn "other dates in this record\|this record"` over app, memory/contracts, tests, evals: no stale wording in the reason path.

**Process note.** `git worktree add` was refused by the board-guard (reviewers may not run `git worktree` in the project). I pinned the same tree with `git archive` into `artifacts/review-evidence/T-088-T-089-r2/clean`.

**Outside these cards (not findings on T-088 or T-089)**
- Clean HEAD has 6 failing unit tests (`test_trace.py` x4, `test_t075_determinism.py`, `test_t037_backend.py`); the same 6 fail at 55300e9. The dirty main tree has 21 failures from in-progress work.
- The shared index currently stages deletions of other cards' paths (`evals/reports/controls-20261102T042306Z.*`, `evals/golden/judge_controls_heldout.jsonl`, `.claude/agent-memory/qa/project_judge_controls.md`). That is the round-1 F3 hazard, for T-093's paths.

```json
{"card": "T-088", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "round 2, commit 55300e9 (app/backend/date_convention.py reason, memory/contracts/api.md, tests/unit/test_date_convention.py); pinned tree HEAD 7df65fb via git archive at artifacts/review-evidence/T-088-T-089-r2/clean (card paths unchanged 55300e9..7df65fb); golden evals/golden/case_01_date_formats.txt; no live app URL (TestClient in-process, LLM_BACKEND=fixture)",
 "exercised": ["python3 tools/board.py show T-088, show T-096, list --role qa", "git show 55300e9 for the three in-scope files (full diff read)", "git diff 55300e9 7df65fb for the card paths and their helpers (empty)", ".venv/bin/python -m pytest -q tests/unit -k 'date or dismiss or suggest' in clean HEAD: 140 passed, 1196 deselected; in the dirty main tree: 160 passed, 1238 deselected", "pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py in clean HEAD: 30 passed", "pytest tests/unit in clean HEAD: 6 failed, 1330 passed (none in card files; the same 6 fail at 55300e9)", "probe_t088_r2.py on clean HEAD (artifacts/review-evidence/T-088-T-089-r2/probe_t088_r2_output.txt): golden reason, each named record checked against the golden source text, confirm of a non-candidate, packet reason", "mutate_r2.py on a scratch copy: R2-88a to R2-88h (artifacts/review-evidence/T-088-T-089-r2/mutation_run_r2.txt), all caught", "git diff --cached --name-status -- the four card paths (empty); grep 'this record' and 'other dates in this record' over app, memory/contracts, tests and evals (only the contract's 'never described as' sentence and unrelated copy)", "grep -c 'suggestion|dismissal' on evals/golden/case_01_date_formats.expected.json (0); grep on app/frontend (0)"],
 "verdict": "changes",
 "scores": {"code_only_no_llm": 5, "never_auto_applied_d041": 5, "reason_grounded_in_packet": 5, "mixed_packet_handling": 4, "tests_fail_on_mutation": 5, "ac_integrity": 3},
 "findings": [
  {"severity": "major",
   "title": "AC 1 is still done=true, and its eval half has no card",
   "evidence": "python3 tools/board.py show T-088 → \"done\": true, \"evidence\": \"PARTIAL, corrected: backend half only. ...\"; the AC text still reads 'the UI pre-selects it' and 'eval case'. python3 tools/board.py list --role qa shows 11 cards (T-015 to T-093); none covers evals/golden/case_01_date_formats.expected.json. grep -c 'suggestion|dismissal' artifacts/review-evidence/T-088-T-089-r2/clean/evals/golden/case_01_date_formats.expected.json → 0.",
   "why_it_matters": "The correction note is honest and the UI is now on T-096, but the gate still reads done=true, and the eval entry exists only as a note addressed to qa. Round 1 asked for done=false or a split into cards; only the UI was split. Until one of those is done, the board says AC 1 is met while two of its parts are not. Kept at major, not downgraded, because it is the same open round-1 finding.",
   "fix": "Either set AC 1 done=false (the UI part stays on T-096, the eval part stays open), or amend the AC text to the backend half and open a qa card for the expected.json entry, using the assertion written in the T-088 note. Do not tick the eval part until expected.json contains it.",
   "acceptance_test": "board show T-088 shows AC 1 done=false, or its text names only the backend half and a qa card exists for the eval entry; grep -c 'MM/DD' evals/golden/case_01_date_formats.expected.json is at least 1 once qa closes that card."},
  {"severity": "minor",
   "title": "The handoff's '(160 pass)' does not reproduce at the commit",
   "evidence": "T-088 handoff: \"pytest -q tests/unit -k 'date or dismiss or suggest' (160 pass)\". Clean HEAD (artifacts/review-evidence/T-088-T-089-r2/clean): '140 passed, 1196 deselected'. Dirty main tree: '160 passed, 1238 deselected'; the 20 extra passes come from uncommitted tests (test_conflict_candidates.py, J3 tests in test_pipeline.py), not from this card. The card's own 30 tests pass in both trees.",
   "why_it_matters": "A reviewer or the Stop hook that reruns the handoff command in a clean checkout gets a different number, so the quoted evidence cannot be reproduced at the commit.",
   "fix": "Quote the card's own files in the handoff: pytest tests/unit/test_date_convention.py tests/unit/test_dismissal_patterns.py (30 passed), or the selector count taken from a clean checkout of the commit.",
   "acceptance_test": "Extract the commit with git archive, run the quoted command there, and check that the quoted number equals the output."}
 ],
 "whats_right": ["The reason names the record each example date sits in, and both names match the golden source: Record 2 holds 02/17/2026 and Record 6 holds 03-17-26 (probe_t088_r2_output.txt, checked against the '=== Record N ===' blocks in the golden text).", "Never auto-applied: auto_applied is false, the record stays ambiguous, and a non-candidate confirm is refused with 422.", "Every reason-wording mutant (singular and plural 'in this record', dropped or off-by-one record number) fails a named test, and the round-1 regression mutants (mixed order, swapped iso, auto-confirm) still fail."],
 "questions_for_chris": ["Round-1 question, still open: for a packet whose dates disagree on order, should the paralegal see a short 'mixed packet' note, or is silence (no suggestion) the intended behaviour?"]}
```
