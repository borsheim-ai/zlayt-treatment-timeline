# T-093 r4 review: staff-engineer-reviewer (HEAD 3223e50)

Verdict: **changes**. No blocker. One major: the H3V5 label is not a real non-conflict on the judge rules as written, so the gate counts a correct judge answer as a false agree. J3V1, J3V9 and J3V13 are real non-conflicts that the judge wrongly agreed with. The reachability guard and the report's source and clean-tree evidence both hold.

Pinned state: `git rev-parse HEAD` = `3223e5017dfcd02e4f79d67d1674a95aa3b1c5be`. The card commits are 822ff38 (J3 rebuild, labels, reachability test) and 3223e50 (the report, from a clean worktree of 822ff38). Reviewed from `git archive 3223e50` extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-093-r4-3223e50`. Mutants were copies `.../scratchpad/T-093-r4-mutA` and `.../scratchpad/T-093-r4-mutB`. Nothing was written into the repo.

## The briefed checks

1. **Every J3 control is producible by `conflict_candidates`: PASS.** `tests/unit/test_t093_j3_controls_reachable.py` runs 11 tests, all pass on the archive. Mutant A appends one unreachable J3 row (J3X1: `Denies prior neck problems.` / `Left knee pain 3/10 at intake.`, rule history_denial) to `evals/golden/judge_controls.jsonl`. `test_every_j3_control_input_is_producible_by_the_candidate_generator` fails with `assert J3 and unreachable(J3) == []` where the unreachable list is `['J3X1']`. Mutant B removes `history_denials` from `candidates()` (`app/backend/conflict_candidates.py:148`). Three tests go red, including the producibility test and the real-candidate test. The weak spot is in the test named `test_the_reachability_check_goes_red_when_a_candidate_rule_is_removed` (F3, nit).
2. **Labels locked before the run, with a rationale per item: PASS, with a thin margin.** `git show 822ff38` (author date 09:09:15Z) precedes the run ID `controls-20261102T090925Z` (generated 09:09:25Z) by 10 seconds. `git log -S H3V5` and `-S J3V13` first show both ids in 822ff38, and no earlier report contains them. The 59 rows in the report's `judge_controls.rows` match the 822ff38 golden labels on id, expected, kind, origin and pair (0 mismatches). All 32 J3 rows carry a `why` (`test_j3_labels_are_the_locked_ones_and_every_item_gives_its_reason`, with the LOCKED table at `tests/unit/test_t093_j3_controls_reachable.py:84-90`). 3223e50 does not touch `evals/golden`. The caveat is that the labels, the generator and the lock table sit in one commit by one author. A later edit would show in a diff, but nothing outside the diff guards them.
3. **Report names its source commit and a clean tree: PASS.** `evals/reports/controls-20261102T090925Z.md:4` reads "Source commit `822ff38250ee68088e3ec64fb96adcd4a265753c`, tree clean." The json has `source_commit` 822ff38 and `source_tree_clean: true`. The `judge_conflict_v5.md` hash in the json (90deea93...) equals `git show 822ff38:app/llm/prompts/judge_conflict_v5.md | shasum -a 256`.
4. **The four false-agree labels: 3 of 4 confirmed, H3V5 not.** See the table below and F1.

| id | file:line | label | rule text on the shown quotes | verdict |
|---|---|---|---|---|
| J3V1 | evals/golden/judge_controls.jsonl:5 | wrong / benign | A PT plan of 12 visits against "Cyclobenzaprine discontinued due to drowsiness." A medicine stop is not the PT course ending. Judge answered conflict 1 of 3. | **Confirmed non-conflict** |
| J3V9 | evals/golden/judge_controls.jsonl:13 | wrong / benign | "The other driver reported a previous collision" is another person's history (judge_conflict_v5.md:7, rule 2b). Judge answered conflict 1 of 3. | **Confirmed non-conflict** |
| J3V13 | evals/golden/judge_controls.jsonl:17 | wrong / benign | "Family history: mother had a neck injury" against "Patient denies any prior injury." Another person's injury (rule 2b). Judge answered conflict 1 of 3. | **Confirmed non-conflict** |
| H3V5 | evals/golden/judge_controls_heldout.jsonl:5 | wrong / benign | See F1. | **Not confirmed. The label is wrong on the rules as written.** |

## F1 (major): H3V5 is mislabelled, so the gate counts a correct judge answer as a false agree

The record is one clause: `"excerpt": "Cancelled the Tuesday appointment;"` (record 2 of the row, after `"Chiropractic 3x/week for 4 weeks."`). The label is benign, and the why says "one cancelled appointment does not show the course ended ... the judge sees only this clause". The rules say otherwise:

- `app/llm/prompts/judge_conflict_v5.md:6` (rule 1): a plan against an outcome that shows "fewer visits attended than planned" is a conflict, and "the reason the course ended early (for example missed appointments) does not make it benign". One cancelled visit with no make-up in the shown text is fewer visits attended than planned.
- `docs/LLM_VS_CODE.md:39` (row 11) lists "a missed, no-show, cancelled, self-discharged or discontinued course" as the early-end signal that code proposes. The control is a cancellation.
- `app/llm/prompts/judge_conflict_v5.md:10` (rule 5): a quote that is cut off is `unsure` with `TEXT_AMBIGUOUS`. This quote ends in a semicolon, and the label itself says the judge sees only the clause. A `benign` label needs text the judge does not see.
- The benign labels that hold have a make-up or a rebook in the shown text: J3V2 "...and rebooked for the next day." (`evals/golden/judge_controls.jsonl:6`) and J3V5 "...made up the following week;" (`:9`). H3V5 has neither.
- The report agrees with the rule text: `evals/reports/controls-20261102T090925Z.md:38` shows conflict / conflict / conflict, reason `PLAN_VS_ACTUAL` on all three repeats.

The second-agent test for a relabel (`memory` on this card: does the rule text, applied to the quotes on their face, support the label? not does the judge agree?) fails for H3V5. The rule text supports conflict or unsure, not benign. So this is not a judge false agree. It is a mislabelled control, and the report's 13/17 counts it as a miss. The 13/17 is not the judge's catch rate on this item.

Why it matters: the controls gate is "every wrong item caught, no false agree" (D-046, `evals/run.py:864-869`). A mislabelled item keeps ship-bar item 4 red for a reason that is not in the product. T-113 AC 1 asks the judge to be taught that a discontinued medicine is not a contradiction. If the same route is taken for H3V5, the prompt would be told that a single cancellation is benign, which contradicts rule 1. That is the risk to avoid.

Fix (D-046 relabel, reviewed by a second agent; this review is that second-agent input and recommends the first option): change H3V5 to `kind: correct`, `expected: conflict`, reason `PLAN_VS_ACTUAL`, with the why citing judge_conflict_v5 rule 1 ("fewer visits attended than planned") and rule 5 (the clause is cut off). Make the same change in the `LOCKED` table (`tests/unit/test_t093_j3_controls_reachable.py:88`) and in the SPEC row in `evals/j3_controls.py:116-117`, and write the reason in `evals/golden/judge_controls.CHANGELOG.md`. The reason must be the rule text, not the failure. Alternatively, replace the record with a complete sentence whose label the rules settle on their face, locked before its first run. Do not add a prompt rule that makes a single cancellation benign.

Acceptance test: `python3 -m evals.j3_controls --check` exits 0 after the change. `test_j3_labels_are_the_locked_ones_and_every_item_gives_its_reason` passes with the new LOCKED value. The changelog entry cites the rule text. On the next controls run, false agree is limited to whichever of J3V1, J3V9, J3V13 the judge still answers `conflict` on, and the wrong total is 16 if H3V5 becomes correct.

## F2 (minor, carry-over from r3 M-5): the card still lists 81aa55e

`python3 tools/board.py show T-093` line 15: `commits: ["e491cad", "7df65fb", "9217f8a", "81aa55e", "2ab7896", "822ff38", "3223e50"]`. 81aa55e is a backend commit (T-092), not this card's. Fix (orchestrator, through board.py): remove 81aa55e. Acceptance: `python3 tools/board.py show T-093 | grep -c 81aa55e` prints 0.

## F3 (nit): a reachability test that does not exercise `candidates()`

`tests/unit/test_t093_j3_controls_reachable.py:38-45` is named as if it catches a removed rule. It passes `CC.plan_vs_outcome` and `CC.history_denials` as the candidate function, so it never calls `candidates()`. A real removal (mutant B) is caught by `test_every_j3_control_input_is_producible_by_the_candidate_generator`, not by this test. Fix: drive it through `candidates()` with `monkeypatch`, or rename it. Acceptance: mutant B still turns the renamed or rewritten test red.

## Carried from r3, not re-checked here

r3 M-2 (J4W7) is closed in the evidence: `evals/reports/controls-20261102T090925Z.md` shows J4 judge_flag_v3 12/12 with J4W7 disagree 3/3, and the J4W7 row is unchanged from e491cad. r3 M-3 (arithmetic guard) and M-4 (reject-all ship bar) were not re-run in this pass.

## What this review did not do

No live LLM or controls run. No network. No CLI sample case. No board write. The full unit suite was not run in this pass (r3 ran it at 2ab7896: 2214 passed).

## Exercised

- Read `personas/staff-engineer.md`, `reviews/T-093-staff-engineer-r3.md`, the T-093 memory file, and `memory/ORCHESTRATOR_DECISIONS.md:54` (D-046).
- `git rev-parse HEAD` (3223e50); `git log --oneline -n 8`; `git show --stat 822ff38 3223e50`; `git archive 3223e50 | tar -x` into the scratchpad.
- `python3 tools/board.py show T-093` and `show T-113` (read only).
- In the archive: `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t093_j3_controls_reachable.py` gives 11 passed. `tests/unit/test_t093_eval_signature.py` gives 65 passed.
- Mutant A (T-093-r4-mutA, J3X1 row added): reachability file gives 5 failed, 6 passed; the producibility assertion reports `['J3X1']`.
- Mutant B (T-093-r4-mutB, `history_denials` removed from `candidates()` at `conflict_candidates.py:148`): reachability file gives 3 failed, 8 passed.
- Read `evals/j3_controls.py` in full; `tests/unit/test_t093_j3_controls_reachable.py` in full; `app/backend/conflict_candidates.py` in full; `app/llm/prompts/judge_conflict_v5.md` (HEAD and archive); `evals/run.py:547-554, 864-869`.
- Printed all 32 J3 rows from both golden files with label, kind, rule, origin and why.
- Report `evals/reports/controls-20261102T090925Z.md` lines 1-40 and the rows for J3V1, J3V9, J3V13, H3V5 (lines 21, 29, 33, 38). Report json keys, `source_commit`, `source_tree_clean`, `hashes`. Compared its 59 rows to `git show 822ff38:` labels (0 mismatches).
- `git show 822ff38:` and `git show e491cad:`/`7df65fb:` for J4W7 (unchanged, `disagree`, `missed_care`).
- `git show 3223e50:memory/DECISIONS.md` line 274 ("Missed or ended care"); `git show 3223e50:spec/SAMPLE_CASE_TRUTHS.md` line 7; `docs/LLM_VS_CODE.md:39`.
- `git diff 9217f8a 822ff38 -- evals/golden/judge_controls.CHANGELOG.md` (round 4 entry).
- `git show 3223e50 --stat`: only `.claude/agent-memory/qa/project_judge_controls.md`, the json and the md under `evals/reports`; no `evals/golden` change.

## Outside my lens

Whether a single cancelled appointment is a clinically meaningful gap is a product and clinical call. My finding rests only on the rule text and the spec wording. The T-113 prompt design is out of scope for this card.

```json
{"card": "T-093", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 3223e5017dfcd02e4f79d67d1674a95aa3b1c5be (git archive in scratchpad T-093-r4-3223e50); card commits 822ff38 (J3 controls rebuilt from conflict_candidates output, labels, reachability test) and 3223e50 (controls report from a clean worktree of 822ff38). Files: evals/j3_controls.py, evals/golden/judge_controls.jsonl (J3 rows, lines 1-17), evals/golden/judge_controls_heldout.jsonl (J3 rows, line 5 is H3V5), tests/unit/test_t093_j3_controls_reachable.py, tests/unit/test_t093_eval_signature.py, app/backend/conflict_candidates.py, app/llm/prompts/judge_conflict_v5.md, evals/reports/controls-20261102T090925Z.md/.json, evals/golden/judge_controls.CHANGELOG.md, docs/LLM_VS_CODE.md:39. No app URL. No live LLM run. Sample CLI not run.",
 "exercised": [
  "personas/staff-engineer.md; reviews/T-093-staff-engineer-r3.md; T-093 memory file; memory/ORCHESTRATOR_DECISIONS.md:54 (D-046)",
  "git rev-parse HEAD = 3223e5017dfcd02e4f79d67d1674a95aa3b1c5be; git log -n 8; git show --stat 822ff38 3223e50; git archive 3223e50 extracted to scratchpad T-093-r4-3223e50",
  "python3 tools/board.py show T-093 and show T-113 (read only)",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_t093_j3_controls_reachable.py (archive) -> 11 passed; tests/unit/test_t093_eval_signature.py -> 65 passed",
  "mutant A (scratchpad T-093-r4-mutA): unreachable J3X1 row appended to judge_controls.jsonl -> reachability file 5 failed, 6 passed; producibility assertion reports ['J3X1']",
  "mutant B (scratchpad T-093-r4-mutB): history_denials removed from candidates() at app/backend/conflict_candidates.py:148 -> reachability file 3 failed, 8 passed",
  "read evals/j3_controls.py, tests/unit/test_t093_j3_controls_reachable.py, app/backend/conflict_candidates.py in full; app/llm/prompts/judge_conflict_v5.md (HEAD and archive); evals/run.py:547-554, 864-869",
  "printed all 32 J3 rows of both golden files (id, kind, expected, rule, origin, why) from the archive",
  "report evals/reports/controls-20261102T090925Z.md lines 1-40 and rows 21, 29, 33, 38; report json keys, source_commit, source_tree_clean, hashes (judge_conflict_v5 hash = git show 822ff38 blob)",
  "compared the 59 report rows with git show 822ff38:evals/golden labels on id, expected, kind, origin, pair: 0 mismatches",
  "git log -S H3V5 and -S J3V13: first appearance in 822ff38; commit author time 09:09:15Z vs run id 090925Z",
  "git show e491cad/7df65fb/822ff38 for J4W7 (disagree, missed_care, unchanged)",
  "git show 3223e50:memory/DECISIONS.md:274; git show 3223e50:spec/SAMPLE_CASE_TRUTHS.md:7; docs/LLM_VS_CODE.md:39",
  "git diff 9217f8a 822ff38 -- evals/golden/judge_controls.CHANGELOG.md (round 4 entry); git show --stat 3223e50 (no evals/golden change)",
  "No live LLM or controls run, no network, no CLI sample case, no full unit suite in this pass, no board write"
 ],
 "verdict": "changes",
 "scores": {"j3_inputs_producible_by_candidates": 5, "reachability_test_discriminates": 4, "labels_locked_before_run": 4, "report_names_source_commit_and_clean_tree": 5, "false_agree_labels_are_real_non_conflicts": 3, "control_files_equal_build": 5},
 "findings": [
  {"severity": "major",
   "title": "H3V5 is mislabelled benign; its conflict verdict is correct on the rules as written, so the gate counts a correct answer as a false agree",
   "evidence": "evals/golden/judge_controls_heldout.jsonl:5 (H3V5, kind wrong, expected benign, records [\"Chiropractic 3x/week for 4 weeks.\", \"Cancelled the Tuesday appointment;\"]); app/llm/prompts/judge_conflict_v5.md:6 (rule 1: 'fewer visits attended than planned' is a conflict; 'the reason the course ended early (for example missed appointments) does not make it benign'); app/llm/prompts/judge_conflict_v5.md:10 (rule 5: a cut-off quote is unsure/TEXT_AMBIGUOUS); docs/LLM_VS_CODE.md:39 (row 11: early end includes 'cancelled'); benign labels that hold have a make-up or rebook in the text: evals/golden/judge_controls.jsonl:6 (J3V2, rebooked) and :9 (J3V5, made up); evals/reports/controls-20261102T090925Z.md:38 (verdicts conflict / conflict / conflict, reason PLAN_VS_ACTUAL x3)",
   "why_it_matters": "The controls gate is every wrong item caught with no false agree (D-046; evals/run.py:864-869). The 13/17 counts H3V5 as a miss, but the judge's rules point to conflict or unsure for that text, not benign. The gate therefore reports a product miss that is a label error. Relabelling it is D-046 territory: a second-agent reason from the rule text, not from the failure. If T-113 instead teaches the judge that a single cancellation is benign, that contradicts rule 1 and the product's early-end definition.",
   "fix": "D-046 relabel with second-agent reason (this review): H3V5 kind correct, expected conflict, reason PLAN_VS_ACTUAL, why citing judge_conflict_v5 rule 1 and rule 5. Change the LOCKED table (tests/unit/test_t093_j3_controls_reachable.py:88), the SPEC row (evals/j3_controls.py:116-117) and the changelog in the same diff. Or replace the record with a complete sentence whose label the rules settle on their face, locked before its first run. Do not add a judge rule that makes a single cancellation benign.",
   "acceptance_test": "python3 -m evals.j3_controls --check exits 0 after the change; test_j3_labels_are_the_locked_ones_and_every_item_gives_its_reason passes with the new LOCKED value; the changelog cites the rule text; on the next controls run the false agree list is a subset of J3V1, J3V9, J3V13 and the wrong total is 16."},
  {"severity": "minor",
   "title": "Card T-093 still lists commit 81aa55e, which is not this card's (r3 M-5 not closed)",
   "evidence": "python3 tools/board.py show T-093 line 15: commits: [\"e491cad\", \"7df65fb\", \"9217f8a\", \"81aa55e\", \"2ab7896\", \"822ff38\", \"3223e50\"]",
   "why_it_matters": "The board is the source of truth; a wrong commit on the card misattributes the audit trail.",
   "fix": "Orchestrator removes 81aa55e through board.py (reviewers do not write the board).",
   "acceptance_test": "python3 tools/board.py show T-093 | grep -c 81aa55e prints 0."},
  {"severity": "nit",
   "title": "test_the_reachability_check_goes_red_when_a_candidate_rule_is_removed does not call candidates()",
   "evidence": "tests/unit/test_t093_j3_controls_reachable.py:38-45 passes CC.plan_vs_outcome and CC.history_denials to unreachable(); mutant B (history_denials removed from candidates() at app/backend/conflict_candidates.py:148) is caught only by test_every_j3_control_input_is_producible_by_the_candidate_generator",
   "why_it_matters": "The name overstates what the test guards; a future refactor of candidates() could keep this test green while the real guard is the other one.",
   "fix": "Drive the test through candidates() with monkeypatch, or rename it to what it checks.",
   "acceptance_test": "Mutant B still turns the rewritten or renamed test red."}
 ],
 "whats_right": [
  "The producibility guard is real: mutant A (unreachable J3X1 row) is named by the test, and mutant B (history_denials dropped from candidates()) turns three tests red.",
  "The report names source commit 822ff38 with source_tree_clean true, and its 59 rows match the 822ff38 golden labels with 0 mismatches; the judge_conflict_v5 hash equals the 822ff38 blob.",
  "J3V1, J3V9 and J3V13 are real non-conflicts on the rule text (a medicine stop, another driver's collision, another person's injury), so their conflict answers are real product findings for T-113."
 ],
 "questions_for_chris": [
  "H3V5: under product policy, does one cancelled appointment with no make-up, against a 3x/week for 4 weeks plan, need to be reconciled (judge_conflict_v5 rule 1 and LLM_VS_CODE row 11 say yes; the label says no)? This review reads it as conflict; the relabel is your call under D-046.",
  "Reviewer model: this review ran as claude-haiku-5-5, as the brief asks. CLAUDE.md section 6 puts engineering reviewers on Sonnet; raised in r1 to r3 and still open."
 ]}
```
