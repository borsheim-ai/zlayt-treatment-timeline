# T-090 review: calibrated confidence as measured counts (D-042, scope cut 10)

**Verdict: fail.** One blocker: the committed `evals/reports/calibration.json` does not come from the code that committed it. Three majors, four minors, one nit.

Scope: commit d0aee83 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/calibration.json). Line numbers below are at d0aee83, pinned with `git archive` into `artifacts/review-evidence/T-090-staff/base/`. HEAD moved to ec33bf0 during the review; the archive of ec33bf0 gives the same counts, so the finding stands at HEAD too. The working-tree `evals/run.py` is modified by an uncommitted change, so working-tree numbers are not used as evidence. No app URL exists for this card: there is no calibration route or UI yet (`grep -rln calibration app/` returns nothing).

## What reproduces and what does not

| Source | verified | needs_review | Amount / flag cells |
|---|---|---|---|
| Committed `evals/reports/calibration.json` (card AC 1 cites it) | 82/83 | 11/13 | flags needs_review 3/5, flags verified 19/19 |
| Regenerated at d0aee83, run 1 and run 2 (`evals.run --out`, fixture) | 83/84 | 10/10 | flags needs_review 2/2, flags verified 20/20 |
| Regenerated at ec33bf0 (HEAD at write time) | 83/84 | 10/10 | same as above |
| Working tree (uncommitted evals/run.py and app changes) | 84/85 | 9/9 | not evidence for this commit |

Runs 1 and 2 at d0aee83 differ only in `generated_at` (`artifacts/review-evidence/T-090-staff/regen-1`, `regen-2`). The committed file's `generated_at` is 2026-11-02T04:18:47Z; no `evals/reports/*0418*.md` exists, and `evals/reports/latest.json` (04:09:33Z) has no `calibration` key.

Hand recompute from the raw fixture outputs (`artifacts/review-evidence/T-090-staff/dump-items-pinned.txt`, golden expectations beside each live item):
- Verified amounts, 9/9: sample r2 $6,240 and r8 $2,150 (charge, 624000 and 215000 cents), case_01 r1 $310.00, case_03 r3 $95.00 and r5 $240, case_05 r2 $4,380, case_07 r1 $420, case_08 r2 $1,875, case_09 r2 $275. Each matches a golden amount on record, raw text, class and value. Agrees with the file.
- Needs-review flags, 2/2: case_06 conflict (r1 and r2, cite C1) and case_07 gap 2026-03-16 to 2026-05-04, 49 days (cite G1). The file says 3/5. The dump has no sample needs-review flag and only one case_06 needs-review flag. Disagrees with the file.

## Other checks

- Percent: zero `%` or `percent` in the calibration code (evals/run.py:228-317 and the render function), in `calibration.json`, or in the rendered `## Calibrated confidence` section of the regenerated report. Passes.
- Backend and sample size: the file states `backend: fixture`, `case_count: 10`, `small_sample: true`. The sentences do not name the backend (see finding 4).
- Mutation: 13 mutants of the matching and pooling logic in a scratch copy of d0aee83 (`artifacts/review-evidence/T-090-staff/mutate_calibration.py`, results in `mutation-results.txt`). 9 killed, 4 survived (M2, M3, M9, M13).
- Tests: `.venv/bin/python -m pytest -q tests/unit -k "calibration or eval_runner"` gives 71 passed in the working tree and 71 passed in the d0aee83 archive. The card says 126 eval tests pass; the brief's selector does not reproduce that number.

## Findings

Each finding has its evidence in the JSON block. The blocker is the reason for the verdict.

1. **blocker**: committed calibration.json cannot be reproduced and has no traceable run (see table above).
2. **major**: AC 1 is marked done while its UI clause is unbuilt (card line 18).
3. **major**: the amount class check is not exercised; mutant M2 survives on tests and on the golden set.
4. **major**: the rendered sentence names no backend and no golden-set provenance.
5. **minor**: small-sample threshold boundary at 29 is untested; M9 survives.
6. **minor**: tolerated-flag and record_warning alignment mutants (M3, M13) survive.
7. **minor**: items are dropped from the denominator silently (stateless items, duplicate candidates, extraction failures).
8. **minor**: calibration.json is not in the freshness check, and it embeds a wall-clock timestamp.
9. **nit**: card says "6 new tests" and the diff adds 7.

## What is right

- Counts regenerate deterministically at a fixed tree; only `generated_at` moves.
- No percentage is rendered anywhere in this change; sentences are generated in code with N/M and a caveat.
- The matching reuses the existing golden rules (entry_found, amount raw/class/value, flag one-to-one), and hand-checked amount cells agree; 9 of 13 mutants die, including the denominator, pooling, percent and state-guard mutants.

## Outside my lens

The same fixture run reports `ship_bar_met=False` (blockers: 4_no_invented_facts, determinism and judge controls not measured). That is the existing ship bar, not T-090.

```json
{"card": "T-090", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit d0aee83 (evals/run.py, tests/unit/test_eval_runner.py, evals/reports/calibration.json), pinned by git archive to artifacts/review-evidence/T-090-staff/base; HEAD moved to ec33bf0 mid-review (same counts there); working-tree evals/run.py is uncommitted-modified and not used; sample case = fixture backend over the 10 golden cases (sample, case_01..case_09); no app URL (no calibration route or UI exists)",
 "exercised": [
  "read personas/staff-engineer.md, board/cards/T-090.md, memory/ORCHESTRATOR_DECISIONS.md D-042, memory/SCOPE_CUTS.md row 10",
  "git show d0aee83 --stat; git show d0aee83 -- evals/run.py; git show d0aee83 -- tests/unit/test_eval_runner.py",
  "git archive d0aee83 (app evals tests spec docs memory tools) into artifacts/review-evidence/T-090-staff/base; cmp: archive calibration.json identical to committed file",
  ".venv/bin/python -m pytest -q tests/unit -k 'calibration or eval_runner' in the working tree: 71 passed, 1102 deselected; same in the d0aee83 archive: 71 passed, 1046 deselected",
  "archive d0aee83: .venv/bin/python -m evals.run --out .../regen-1 and --out .../regen-2 (fixture, no --backend): identical except generated_at (diff line 213); both give verified 83/84, needs_review 10/10; diff against committed calibration.json shows different counts",
  "working tree: evals.run --out .../regen-wt: verified 84/85, needs_review 9/9; archive ec33bf0 (HEAD): regen-head: verified 83/84, needs_review 10/10",
  "dump_items.py (pinned, fixture, all 10 cases) to dump-items-pinned.txt; hand recompute of verified amounts (9/9, agrees) and needs_review flags (2/2, committed says 3/5, disagrees); verified flags 20/20 by the same dump (committed says 19/19)",
  "mutate_calibration.py: 13 scratch mutants on the d0aee83 copy, each run with the calibration and eval_runner selector: 9 killed, 4 survived (M2, M3, M9, M13); mutant counts regenerated for M2 and M13 (regen-mut-M2, regen-mut-M13) are identical to base",
  "grep for percent signs in evals/run.py calibration code, calibration.json, and the rendered calibration section of regen-pinned-b: 0 hits; grep -rln calibration app/: no hits",
  "ls evals/reports/*0418*: none; evals/reports/latest.json generated_at 2026-11-02T04:09:33Z, no calibration key",
  "git show d0aee83 -- tests/unit/test_eval_runner.py | grep -c '^+def test_': 7 new tests"
 ],
 "verdict": "fail",
 "scores": {"counts_reproduce_from_commit": 1, "hand_recompute_agrees": 2, "provenance_traceable": 1, "no_bare_percent": 5,
            "regeneration_deterministic": 4, "backend_and_sample_stated": 3, "mutants_killed": 3, "ac_closed_honestly": 2},
 "findings": [
  {"severity": "blocker",
   "title": "Committed calibration.json does not reproduce from the commit and has no traceable run",
   "evidence": "evals/reports/calibration.json:28-29 shows matched 82 total 83 (verified) and :12-13 shows matched 11 total 13 (needs_review); :240-241 carries the same sentences. Regenerating at d0aee83 with .venv/bin/python -m evals.run --out <dir> (fixture) gives verified 83/84 and needs_review 10/10, identical across two runs (artifacts/review-evidence/T-090-staff/regen-1 and regen-2; only line 213 generated_at differs). Regenerating at HEAD ec33bf0 gives the same (regen-head). Flag cells also differ: committed needs_review 3/5 at :165-166 and verified 19/19 at :199-200, regenerated 2/2 and 20/20. Provenance: committed generated_at 2026-11-02T04:18:47Z (:217) has no matching evals/reports/20261102T041847Z.md, and evals/reports/latest.json (04:09:33Z) has no calibration key.",
   "why_it_matters": "The served file is the number a paralegal will read ('matched the record 82/83 times in testing'). No run of the committed code produces it, so it is not measured from evals as D-042 requires, and the next reviewer cannot reproduce the card's evidence. A figure that cannot be traced to a run is an invented number even if the code is right.",
   "fix": "Regenerate calibration.json with a full python -m evals.run at the commit being shipped (fixture backend) and commit it with its report .md and latest.json in the same commit. Do not hand-place or copy the file. Update the card evidence to the regenerated counts (83/84 and 10/10 at d0aee83).",
   "acceptance_test": "At the shipped commit: python -m evals.run --out <tmp> then compare <tmp>/calibration.json with evals/reports/calibration.json ignoring generated_at (must be equal); and a unit test that builds calibration over the golden cases with the fixture backend and asserts by_state and by_type equal the committed file's values."},
  {"severity": "major",
   "title": "AC 1 is marked done while its UI clause is unbuilt",
   "evidence": "board/cards/T-090.md:18 has the AC text \"UI shows 'Verified items matched the record N/M times in testing' instead of a %\" with \"done\": true; the same line's evidence ends \"UI line pending frontend (note)\". grep -rln calibration app/ returns no files at d0aee83 or the working tree, so no endpoint serves calibration.json and no UI renders sentences.overall.",
   "why_it_matters": "A clause of the AC is not met and the AC is closed anyway. The D-042 requirement is that the displayed statement shows measured counts; the displayed statement does not exist yet, so the card's done state overstates what shipped.",
   "fix": "Set AC 1 to done: false, or split it: AC 1a (eval counts, done) and AC 1b (served read-only calibration field and UI line rendered verbatim, no percent), with 1b linked to the frontend and backend cards that will build it.",
   "acceptance_test": "board.py show T-090 shows AC 1b open until a running app returns the calibration sentence (curl the route) and the rendered UI text contains it verbatim with no percent sign."},
  {"severity": "major",
   "title": "Amount matching ignores class in no test; mutant survives and golden counts do not change",
   "evidence": "evals/run.py:253 `and a.get(\"kind\") == g[\"class\"] and a.get(\"value_cents\") == cents):` (d0aee83). Mutant M2 removes the class term: SURVIVED, 71 passed (artifacts/review-evidence/T-090-staff/mutation-results.txt, line for M2). Golden counts under M2 are identical to base (regen-mut-M2/calibration.json).",
   "why_it_matters": "The amount rule is the only place the calibration separates a rate from a charge. If a rate were classified as a charge with the same text and value, the calibrated amount precision would still count it as matched. That inflates the measured number in the exact area the spec treats as a blocker ($185 rate must never be totalled as a charge).",
   "fix": "Keep the class term and add a unit test in tests/unit/test_eval_runner.py: in the sample, change the kind of one verified amount (for example $6,240 charge to rate) and assert that the verified amount count falls from 2/2 to 1/2 for the sample.",
   "acceptance_test": "The new test fails under mutant M2 (remove the class term at evals/run.py:253) and passes at d0aee83."},
  {"severity": "major",
   "title": "The sentence the UI will render verbatim names no backend and no provenance",
   "evidence": "evals/run.py:300 builds sentences.overall from 'Verified items matched the record {m}/{t} times in testing' plus caveat; the string has no backend. evals/reports/calibration.json:241 reads \"Verified items matched the record 82/83 times in testing (small sample: 10 cases).\" The backend 'fixture' appears only in the top-level field (:2) and the report heading. The card note (board/cards/T-090.md:26) asks the frontend to show the backend beside the sentence, which no test enforces.",
   "why_it_matters": "The fixture backend replays recorded replies on the 10 golden cases; it is not live model output. A reader of 'matched the record 82/83 times in testing' will take it as live precision. The file says fixture; the statement a paralegal reads does not. D-042 requires the shown statement to be exactly what was measured.",
   "fix": "Put the backend and the golden-set basis into the sentence, for example 'Verified items matched the record 82/83 times in testing on the fixture backend (recorded replies, 10 golden cases).' Build it in build_calibration so the UI cannot drop it.",
   "acceptance_test": "A unit test asserts each sentence in sentences.overall contains the backend name (build_calibration(res, 'fixture') contains 'fixture'; build_calibration(res, 'claude-cli') contains 'claude-cli')."},
  {"severity": "minor",
   "title": "Small-sample threshold boundary at 29 cases is not tested; lowering CAL_SMALL_N to 5 survives",
   "evidence": "evals/run.py:231 `CAL_SMALL_N = 30`. Mutant M9 (CAL_SMALL_N = 5): SURVIVED, 71 passed. tests/unit/test_eval_runner.py:519 builds range(29) plus 'few' = 30 cases, so the test only checks the 30-case side.",
   "why_it_matters": "The caveat is the guard that keeps a 3-of-3 result from reading as a rate. The threshold is a code choice, not a spec number, and nothing pins it at 29 versus 30.",
   "fix": "Add the 29-case assertion beside the 30-case one: at 29 cases the overall sentence carries 'small sample'; at 30 it does not.",
   "acceptance_test": "The new 29-case test fails under M9 (CAL_SMALL_N = 5) and under a raised threshold of 31 (the 30-case assertion already covers that)."},
  {"severity": "minor",
   "title": "Tolerated-flag and record_warning alignment mutants survive",
   "evidence": "evals/run.py:264 `add(\"flag\", c[\"_state\"], i in owned or any(tolerated_match(...)))`: mutant M3 drops the tolerated term and SURVIVES. evals/run.py:257 filters record_warning out of flags, and zip(cands, flags) at evals/run.py:259 pairs them by position; mutant M13 drops the filter and SURVIVES. Golden counts under M13 are identical to base (regen-mut-M13).",
   "why_it_matters": "A tolerated (documented allowed) candidate would count as wrong, understating precision. A record_warning in the flags list would shift every later flag's state by one position, silently assigning needs_review where verified belongs. Neither is covered, and the golden numbers would not show it.",
   "fix": "Add a test with one tolerated candidate (expect it counted as matched) and one case with a record_warning placed before a flag (expect the states to stay aligned). Prefer matching by candidate identity over zip position.",
   "acceptance_test": "M3 and M13 each turn at least one test red."},
  {"severity": "minor",
   "title": "Items are dropped from the denominator silently",
   "evidence": "evals/run.py:242 `if state in CAL_STATES:` drops items with a missing or other state; tests/unit/test_eval_runner.py:459 asserts that exclusion as intended. evals/matching.py:37-42 (assign_detail) keeps the first of duplicate candidates and drops later ones, so a duplicate's state never counts. app/backend/generator.py:51 returns {'failure': 'FIXTURE_MISS'} for a record with no extraction, so that record never becomes an item and never reaches M.",
   "why_it_matters": "The sentence reads as the share of produced items that were right; it does not say how many produced items were not scored, or that records with no output are outside the count. Precision of produced items is the stated D-042 measure, so this is a disclosure gap rather than a wrong number, but it hides output-schema bugs (a missing state looks like 'not an item').",
   "fix": "Count the excluded items per cell and print them beside the sentence ('N items not scored'); or state in the sentence that the count covers produced items only.",
   "acceptance_test": "A build_calibration test with one stateless item reports 'not scored: 1' beside the sentence; the sentence no longer reads as complete."},
  {"severity": "minor",
   "title": "calibration.json is outside the freshness check and embeds a wall-clock timestamp",
   "evidence": "evals/reports/calibration.json:217 \"generated_at\" wall-clock value; two regenerations at the same tree differ in that one line (artifacts/review-evidence/T-090-staff/regen-1 vs regen-2). evals/run.py:71-80 hashes() covers only app/llm/prompts/*.md and app/llm/lexicon.yaml, so check_fresh (evals/run.py:915) cannot see a stale calibration.json.",
   "why_it_matters": "This is how finding 1 went unnoticed: the served file can drift from latest.json with nothing to flag it. Counts are deterministic, which is good; the file is not checked.",
   "fix": "Add the calibration.json hash to the check-fresh comparison, and either drop generated_at from the served file or exclude it from the hash.",
   "acceptance_test": "Edit one count in evals/reports/calibration.json, then python -m evals.run --check-fresh exits 1."},
  {"severity": "nit",
   "title": "Card claims 6 new tests; the diff adds 7; the selector result differs from the card's 126",
   "evidence": "board/cards/T-090.md:18 says 'tests/unit/test_eval_runner.py 6 new tests'. git show d0aee83 -- tests/unit/test_eval_runner.py | grep -c '^+def test_' returns 7 (tests/unit/test_eval_runner.py:444, 459, 469, 480, 494, 515, 524). The brief's selector gives 71 passed, not 126.",
   "why_it_matters": "The card note is the only record of what was verified; small count errors reduce trust in the handoff.",
   "fix": "Correct the count in the card note and name the selector used for the 126 figure, or drop it.",
   "acceptance_test": "Card note matches the diff and the selector."}
 ],
 "whats_right": [
  "Counts regenerate deterministically at a fixed tree: two pinned runs differ only in generated_at.",
  "No percent sign is produced anywhere in the calibration code, calibration.json, or the rendered section; sentences are built in code with N/M and a caveat.",
  "Matching reuses the existing golden rules; the hand-checked amount cells agree (9/9 verified, 6/6 needs_review), and 9 of 13 scratch mutants die."
 ],
 "questions_for_chris": [
  "Is fixture-replay precision (recorded replies on the golden cases) an acceptable basis for the D-042 statement, or should the statement wait for a live-backend run before it is shown?"
 ]}
```
