# GATE-M3M4 staff-engineer review (pinned f6d5c19)

Verdict: **fail** by the verdict rule (2 blockers, both "a doc that states something false"; the code behaves correctly). Rules applied: D-075 (blockers only, everything else minor and goes to SCOPE_CUTS) and D-074.

Scope: a fresh `git archive f6d5c19` in `/tmp/gs/arc` (scratchpad `GATE_M3M4_staff/arc`), plus a `git clone` at f6d5c19 for the git-dependent tools tests. Cards T-202, T-207, T-213, T-214, then a broad pass. No full e2e run (QA owns it); targeted tests only.

## Card results
- **T-202 (all-blank date fallback): passes.** `export.charge_when` (`app/backend/export.py:210-215`) always prints `<source>, date of service [__________] (statement|record dated X)`, the bare blank when the record has no date. `service_date.resolve` (`service_date.py:406-413`) turns any date the reader finds into `not_read`, so Step 3 and the letter agree. `python -m evals.letter_check` gives `{"value": 0, "cases": 25 ...}`. Mutant 1 (letter prints the record date): letter_check lists violations in cases lib13, lib14, lib15 and others, and 6 tests in `test_t202_r7_all_blank.py` fail. Mutant 2 (`resolve` returns the raw read): 5 tests fail in `test_t202_r7_all_blank.py` and `test_t200_undated_charge_label.py` (the letter is not affected, because `charge_when` does not call `resolve`; only Step 3 is). So letter_check enforces the letter, and the unit tests enforce Step 3.
- **T-207 (rows 2-3): pass.** Row 2 and row 3 match the code row by row (blank form, "statement" vs "record" label, bare blank when undated, entry dates stay on the ambiguous-never-guessed rule, `letter_check.charge_date_violations` is an independent scanner: it imports nothing from `app` and reads only `encounter_types.json`). The false statements are in other rows (findings 1 and 2).
- **T-213 (Office tab removed): pass.** `grep -ci office tools/board_ui.html tools/board_server.py` gives 0 and 0. Server from the archive: `/` 200, `/api/office` 404. Playwright clicked all six tabs (Board, Milestones, Personas, Activity, Inbox, State); the only console error is `/favicon.ico` 404. `tools/tests`: 339 passed in the main repo at HEAD f6d5c19 (see minor 2 for the clone failures).
- **T-214 (code-only flags): pass.** `present.py:310-312`; `test_flag_origin_t214.py` 2 passed. Mutant (drop `prepared = False`): `test_code_only_flags_are_not_prepared_on_the_curated_sample` fails. On the curated sample only f_r7_1 (lexicon) and the three code-made flags get `prepared=false` and an origin label; the `lexicon+llm` flags stay prepared. The guided UI test `test_t214_...` passes and the how-checked panel shows "Not needed" for the judge on the gap flag.

## Broad pass (all judged blocker or not)
- LLM/code boundary: no `llm`, `provider` or `audited` import in dates, gaps, money, amounts, totals, export, service_date, grounding, sentences (grep). No `float(` on money, no bare `except:` or `except Exception: pass` in `app`. Gap/amount/ledger unit files: 190 passed. Not a blocker.
- Ladder: API probe on the curated and the recorded sample sets. Export with nothing accepted is 422 `export_blocked`. An edit with an invented number and date is 422 and the stored summary is unchanged. Batch accept of an amount is 422 `CHARGES_NOT_BATCHED`, of a flag is 422 `invalid_batch`, a mixed batch changes nothing (entry stays `pending`). After accepting everything and dismissing one entry: the dismissed excerpt is not in the letter or the notes, the total is `$8,390.00` (6,240 + 2,150, the $185 rate excluded). Rejected-item accept/edit/count refusal and the judge-not-run gate are pinned by 267 passing tests in the ladder/export files. No bypass found.
- Crash paths: 27 malformed or hostile requests (bad JSON, list body, null action, wrong types, unknown ids, 2 MB paste, bad style, bad export config, missing page image): zero 5xx. 2 MB paste is 413.
- Determinism: `python -m app.pipeline evals/golden/sample.txt` run twice with the fixture backend: byte-identical (`cmp` silent). `evals/golden/check_golden.py` OK; `tests/fixtures/make_curated.py --check` "letter equal: True | notes equal: True".
- Secrets: `tools/check_secrets.py` "ok (3824 file(s) scanned)"; only `.env.example` is tracked.

## Findings (same order as the JSON block)
1. **blocker** `docs/LLM_VS_CODE.md:47` (row 19) states the total line is "Billed charges stated in these records: $X" and that every letter line carries "a date of service". The code and golden print `Billed charges accepted from these records: ` (`app/backend/export.py:36`, `evals/golden/sample.export.expected.txt:47`), and since D-073 charge lines print the blank. This is the graded doc, so a false sentence in it is a blocker under the brief.
2. **blocker** `memory/contracts/api.md:574-575` still says charge lines carry "a long date" and that a charge line's date has "Exactly two sources" (bill-table cell, encounter record's own date). The code prints the blank on every charge line (`service_date.py:404-413`); api.md never mentions the r7 fallback.
3. **minor** (SCOPE_CUTS) A code-computed gap flag has `why` = "...and the second check agreed." with `ladder.judge = null`. Not shown in the guided UI (the panel says "Not needed"), so not a demo blocker.
4. **minor** (SCOPE_CUTS) `tools/tests` fails 6 (git clone) or 11 (plain archive) tests when the repo sits under `/tmp`; the guard intentionally allows writes under `/tmp`, so `test_board_guard`/`test_git_guard` expectations break. Passes 339/339 in the real repo. QA should run it there.

## What is right
- The blank is enforced twice: `charge_when` for the letter and an independent scanner (`letter_check`) that kills the record-date mutant over 25 cases.
- The ladder holds at the API: refused accepts and batches change nothing, edits with invented numbers are 422 with nothing saved, dismissed items never reach the letter.
- The hostile-request sweep produced zero 5xx; oversized paste fails fast with 413.

```json
{"card": "GATE-M3M4", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "git archive f6d5c19 (T-202, T-207, T-213, T-214 + broad pass); app via TestClient and board server from the archive; sample case, curated and recorded fixture sets",
 "exercised": [
  "git archive f6d5c19 to scratch dir; git clone at f6d5c19; git rev-parse HEAD = f6d5c1919a26b7e71f67dfd079b520d5aa82ec68",
  "pytest tests/unit/test_t202_r7_all_blank.py test_flag_origin_t214.py test_prepared_property.py: 47 passed, 3 skipped (valid has no scope)",
  "pytest ladder/export unit files (test_export, test_export_edge, test_grounding, test_judge_guard, test_judges, test_review_rules, test_t134_unconfirmed_edit, test_t145_judge_not_run, test_t168_strict_judge_parse): 267 passed",
  "pytest test_gaps, test_amounts, test_amounts_d059: 190 passed",
  "pytest tests/e2e/test_charge_confirm.py guided/test_t205.py guided/test_t206.py: 34 passed; guided/test_t211.py -k t214: 1 passed",
  "python -m evals.letter_check: value 0, 25 cases; evals.golden.check_golden OK; tests/fixtures/make_curated.py --check: letter equal True",
  "mutants: export.charge_when prints record date (letter_check lists violations, 6 tests fail); service_date.resolve returns raw read (5 tests fail, letter_check stays 0 because the letter does not call resolve); present.py drop prepared=False (1 test fails)",
  "tools/tests: 339 passed in main repo at HEAD; 11 failed in plain archive and 6 failed in a clone under /tmp (guard allows /tmp writes, environmental)",
  "board_server.py from the archive on 7791/7792: / 200, /api/office 404, Playwright over 6 tabs, only console error is favicon 404; servers stopped by verified PID",
  "ladder_probe.py, batch_probe.py, flag_probe.py (artifacts/review-evidence/GATE-M3M4-staff/): 27 hostile requests no 5xx; batch/edit/accept refusals; export after accept+dismiss; total 839000 cents",
  "test_gap_flag_text.py copied into archive tests/e2e/guided: guided UI shows 'Not needed' for the gap flag judge row, no 'second check agreed' text",
  "python -m app.pipeline evals/golden/sample.txt twice: cmp identical",
  "greps: llm imports in deterministic modules, bare except, float(, sleep(, secrets (check_secrets ok, 3824 files)",
  "read docs/LLM_VS_CODE.md rows 2, 3, 19, memory/contracts/api.md 574-575, service_date.py, export.py, store.py, letter_check.py, present.py, review.py, case_extras.py, frontend T-214 diff"],
 "verdict": "fail",
 "scores": {"llm_code_boundary": 5, "validation_ladder": 5, "determinism_and_tests": 4, "failure_visibility_no_crash": 5, "doc_accuracy": 2},
 "findings": [
  {"severity": "blocker", "title": "LLM_VS_CODE row 19 states the wrong total-line wording and a date of service on every letter line",
   "evidence": "docs/LLM_VS_CODE.md:47: 'The total line is always exactly \"Billed charges stated in these records: $X\"' and 'Every letter line carries its verbatim excerpt, the provider as written, a date of service'. Code: app/backend/export.py:36 TOTAL_PREFIX = \"Billed charges accepted from these records: \"; evals/golden/sample.export.expected.txt:47 'Billed charges accepted from these records: $8,390.00'; charge lines print 'date of service [__________] (record dated January 9, 2026)' (probe export). grep -n 'stated in these records' docs/LLM_VS_CODE.md finds only line 47.",
   "why_it_matters": "This is the graded doc; row 19 contradicts both the code and rows 2-3 that T-207 just fixed. A hiring reviewer comparing the doc with the letter finds a false sentence.",
   "fix": "Row 19: change the quoted total line to 'Billed charges accepted from these records: $X' and say each treatment line carries its date and each charge line carries the fillable 'date of service [__________]' blank (row 3).",
   "acceptance_test": "grep -c 'stated in these records' docs/LLM_VS_CODE.md returns 0, and row 19 mentions the fillable blank for charge lines; python -m evals.letter_check still value 0."},
  {"severity": "blocker", "title": "api.md still documents a printed charge-line date with two sources; the code prints the blank on every line",
   "evidence": "memory/contracts/api.md:574 'every entry and charge line in letter_text is followed by Source ... with the provider as written and a long date'; api.md:575 '**Where a charge line's date comes from (D-073 round 6, T-202 r6; code only).** Exactly two sources ...'. Code: app/backend/service_date.py:404-413 resolve() 'the letter and Step 3 NEVER carry a service date'; app/backend/export.py:210-215 charge_when always prints the blank. grep -n 'fallback' memory/contracts/api.md finds no mention of the r7 fallback.",
   "why_it_matters": "The API contract is the frontend/backend source of truth and part of the repo Chris hands over; it states behaviour the product no longer has (a doc that states something false is a blocker per the gate brief).",
   "fix": "Replace the line-575 paragraph with the r7 rule (every charge line prints 'date of service [__________] (statement|record dated X)', no service date extracted, reader kept as service_date.read, SCOPE_CUTS 28) and change 'a long date' in line 574 to 'a long date for entries; charge lines print the fillable date blank'.",
   "acceptance_test": "grep -n 'Exactly two sources' memory/contracts/api.md returns nothing; the replacement text names 'date of service [__________]'."},
  {"severity": "minor", "title": "Code-computed gap flag carries a stale 'second check agreed' why with no judge (SCOPE_CUTS, D-075)",
   "evidence": "flag_probe.py on curated sample: item f_gap_r6_r7 why='Quote found word for word, every number in the summary is in the quote, and the second check agreed.' with ladder.judge null; guided UI row how-ai-text='Not needed. This is arithmetic over dates in the record, which code does exactly.' and page text does not contain 'second check agreed'.",
   "why_it_matters": "The API field says a check ran that did not; any surface that prints item.why for a gap flag would mislead. The guided demo does not.",
   "fix": "Give code-computed flags a why that names only the code checks (present.py OK_WHY branch).",
   "acceptance_test": "A unit test asserts f_gap_* why does not contain 'second check'."},
  {"severity": "minor", "title": "tools/tests depend on the repo not living under /tmp (SCOPE_CUTS, D-075)",
   "evidence": "In a git clone under the scratchpad (/private/tmp/...): 'pytest tools/tests' -> 6 failed, 333 passed (test_board_guard::test_denied[...]); plain archive: 11 failed, 328 passed; main repo at HEAD: 339 passed. .claude/hooks/board_guard.py:38 treats /tmp and /private/tmp as writable.",
   "why_it_matters": "A QA run from a /tmp clone or archive shows red that is not a product defect.",
   "fix": "Run the tools suite from the real checkout, or have the tests set up the repo path outside /tmp.",
   "acceptance_test": "pytest tools/tests passes from a clone placed outside /tmp."}
 ],
 "whats_right": [
  "The fillable blank is enforced twice (export.charge_when plus the independent letter_check scanner); the record-date mutant fails letter_check over the corpus and 6 unit tests.",
  "The ladder holds at the API: refused accepts and batches change nothing, an edit with an invented number is 422 with nothing saved, dismissed items never reach the letter or the total.",
  "27 hostile requests produced zero 5xx, an oversized paste fails fast with 413, and the CLI is byte-identical across runs."],
 "questions_for_chris": []}
```
