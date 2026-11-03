# Revert audit: commits 328428f..bc12d44 (20 commits)

Method: for every commit, `git diff -U0 <parent> <commit>` per file; every deleted line was traced with `git blame <parent>` to the commit that
introduced it. A hit means the commit removed lines another card had committed. Each hit was then read to separate a legitimate edit from a revert.
A second pass ran the unit suite on a clean worktree and traced each failure (this found the audited.py row, whose lines predate 328428f).

| Commit (card) | File | What was lost | Card that lost it | Restored by |
|---|---|---|---|---|
| ec33bf0 (T-084) | app/backend/billing.py (642 lines), tests/unit/test_billing.py (330), 2 lines in api.py | whole T-083 billing module, its tests and the router lines | T-083 | e2b4e3f (earlier) |
| ec33bf0 (T-084) | memory/contracts/api.md | 37 lines: billing route row and `GET /billing` section | T-083 | 865b186 re-added them by accident; every f218263 line verified present in HEAD; no commit needed |
| 2fca530 (T-087/T-086) | app/db/db.py, app/db/schema.sql | SCHEMA_VERSION 4, AUDIT_ONLY_ACTIONS, `_migrate_v3_to_v4`, `log_event`, `reclassify`/`rejudge` in the CHECK | T-095 (031a708) | 6feb2ff |
| 2fca530 | app/backend/rejudge.py | `_log` helper and its 2 calls (audit row per re-judged item) | T-095 | 6feb2ff |
| 2fca530 | tests/unit/test_db.py (76 lines), tests/unit/test_trace.py (16 lines) | v3->v4 migration tests, rejudge/reclassify audit tests | T-095 | 6feb2ff |
| 2fca530 | app/backend/reclassify.py, tests/unit/test_reclassify.py (1 line each) | `AUDIT_ACTION = "reclassify"` and its assert | T-095 | already fixed by c8a9874 (T-084 r2); reverse-apply was a no-op |
| 2fca530 | evals/run.py (70 lines), tests/unit/test_eval_runner.py (167) | `git_source`, `score_calibration(unscored)`, backend-naming calibration sentences, `source_commit`/`hashes`, `not_scored`, `check_calibration` in check-fresh | T-090 r2 (823b718) | a850be0 |
| 865b186 (T-085) | app/llm/audited.py | `"conflicts": "conflicts_v1"` in PROMPT_OF_STEP and `j3: judge_conflict_v2` (replaced by `judge_conflict_v3`, a prompt file that was never committed): another worker's uncommitted edit was swept in. 4 test_trace tests and test_t075 failed on it | T-057 (b365af3) / T-075 (3104213) | c7ba1f1 |

Checked and fine (deleted lines are same-card or intended edits): f667f08, 5616dc3, 7724412, f218263, 17cc9c7, e92b6ed, 031a708 (reclassify one-liner edit), 55300e9 (own card), 865b186 other files (api.py, present.py, review.py edits are the Spanish path), 7df65fb, d3130e3, bc12d44, e3fc01c, 49c4600, 02ff244, c8a9874.
2fca530 additions kept as they are (T-086/T-087 scope): pdf_*.py, OCR_DERIVED in confidence/trace/why/present/pipeline, api.py PDF route, provider test allowance for pdf_ocr.py.

Unit suite on a clean worktree of c7ba1f1: 1400 passed, 1 failed. Baseline bc12d44: 1368 passed, 16 failed.
Remaining failure, not a revert: tests/unit/test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s. 865b186 (T-085) put the
`language.case_check(... IN.ingest(raw) ...)` block in app/backend/pipeline.py `main()` before `raw` is read (UnboundLocalError). It belongs after the file read; left for the T-085 owner.
Process note: an uncommitted audited.py edit for a conflict-judge change (judge_conflict_v4, conflict_candidates.py in the working tree) is still in progress; when committed it must carry its own PROMPT_OF_STEP and `conflicts` handling.
