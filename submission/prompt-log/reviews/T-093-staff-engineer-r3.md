# T-093 r3 review: staff-engineer-reviewer (HEAD 2ab7896)

Verdict: **changes**. No blocker. Two majors: (1) most J3 control pairs are not pairs the shipped code ever proposes to the judge, so the J3 gate says 17/17 but measures 2 wrong items on the production path; (2) the J4W7 label stands, but judge_flag_v2 answered agree on 1 of 3 repeats, so ship-bar item 4 is red today and the fix is a prompt rule, not a relabel. Two minors: a regex arithmetic guard that a rewording evades, and a board card whose `commits` list names 81aa55e (not this card's commit).

Pinned state: `git rev-parse HEAD` = `2ab789601644357fd87b3b143d6cf50b17b68cd5`. Reviewed from `git archive 2ab7896` extracted to `/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-093-r3-2ab7896`. Source of the controls run: `9217f8a`.

## The six briefed checks

1. **Controls gate is "every" (1.0), pinned by a test: PASS.** `evals/run.py:840-845` (`controls_ok`) requires `wrong_caught == wrong_total` and no false agree for J3 and J4. `tests/unit/test_t093_eval_signature.py:335-349` pins 19/19 and 20/20 as pass, and 18/19, 19/20 and 99/100 as fail. Mutation in the archive copy: replacing the count test with `catch_rate >= 0.5` makes `test_the_controls_gate_is_every_wrong_item_not_a_rate` and `test_the_gate_does_not_read_the_catch_rate_threshold` fail (2 failed, 68 passed). The archive was restored from `git show 2ab7896:evals/run.py` and `cmp` against it matched.
2. **Arithmetic pairs moved to code tests against T-094's candidate code: PASS.** J3W10, J3C6, H3W1 and H3C1 are absent from `evals/golden/judge_controls.jsonl` and `judge_controls_heldout.jsonl`. `test_code_resolves_frequency_times_duration_against_a_visit_count` (test file lines 367-377) calls `app.backend.conflict_candidates.plans()` and asserts 12, 12, 8 and 12 visits. The guard against new arithmetic items is weak (minor M-3).
3. **J3 controls hold only judgment pairs that reach the judge: FAIL (major M-1).** Details below.
4. **J3C10 reason rewritten: PASS.** The `why` on the row (`judge_controls.jsonl`, J3C10) states "product policy, not rule 2" and gives the undated-disagreement basis. `judge_controls.CHANGELOG.md` round 3 states the same basis, cites run 20261102T035750Z and the FACT_MISMATCH verdict, and records the input edit. `judge_conflict_v4.md` rule 3 now says two values for one measure with no visit or date are a conflict.
5. **Controls evidence names its source commit and a clean tree: PASS.** `evals/reports/controls-20261102T063331Z.md` line 3: "Source commit `9217f8af56b72699c563aadb00d406a08d6bea20`, tree clean." The json has `source_commit` 9217f8a and `source_tree_clean: true`. All 14 hashes in the json were checked with `git show 9217f8a:<path> | sha256`; every one matches and every file exists at 9217f8a. `judge_conflict_v3.md` is absent at 9217f8a, and the report names v4.
6. **Audit prompt versions match what judges.py sends: PASS for J1-J4.** `app/backend/judges.py:48` judge_faithfulness_v1, `:53` judge_amount_class_v1, `:59` judge_conflict_v4, `:64` judge_flag_v2. `app/llm/audited.py:123-124` PROMPT_OF_STEP: j1 judge_faithfulness_v1, j2 judge_amount_class_v1, j3 judge_conflict_v4, j4 judge_flag_v2. Same at 9217f8a. The Spanish judge id is in the map but was not checked here (outside this card's J3/J4 scope).

## M-1 (major): J3 gate measures pairs the shipped code never proposes

`app/backend/conflict_candidates.py:121-123` `candidates()` returns only `plan_vs_outcome` (treatment_plan_vs_actual) and `history_denials` (other_fact_mismatch via a denial). There is no rule for laterality, date, dose, same-measure pain, or unrelated topics. `app/backend/flags.py:240-244` says CODE proposes the candidate pairs and "the model's only job is the classification of each candidate, by J3". `run_j3` has one call site, in `run_conflict_pass`.

I fed each J3 control pair to `candidates()` as two records (ids 1 and 2, dated 2026-01-10 and 2026-01-12). Result on 2ab7896: of 29 J3 rows, 23 are NOT PROPOSED. Reached: J3C1, J3C7, J3C2 (plan vs early end), J3C3, J3W12, J3W13 (denials).

- Wrong items that never reach J3 (15 of 17): J3W1, J3W2, J3W3, J3W4, J3W5, J3W11, J3W14, J3W15, J3W16, J3W17, J3W18, J3W19, H3W2, H3W3, H3W4.
- Correct items that never reach J3 (8 of 12): J3C4, J3C5, J3C8, J3C9, J3C10, H3C2, H3C3, H3C4.
- Also: J3W11 (completed plan, "discharged with goals met") and H3C4 ("did not return after the second session") are not matched by `_ENDED` (`conflict_candidates.py:26`), so the production path would not send them either.

So the "17/17 wrong caught x3" in the report (and AC 2) is a result on 2 wrong items the shipped pipeline sends J3. The changelog calls the set "judgment pairs" and says the rest "still share a fact word". That is true, but it does not say the code never sends them. The r2 minor ("report paired-subset catch rate separately") is not closed by this; it is the same problem at a larger scale.

Repro (from the archive; the script lives in the scratchpad, not in the repo):
`cd <archive> && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-093-r3-scripts/pairs_reach_judge.py <archive>`

Why it matters: the D-046 gate is meant to show the judges that decide flags catch seeded wrong decisions. For the shipped app at this commit, laterality, date, dose and pain-score conflicts are not flagged at all, so a judge gate on them tests a path that does not exist. The gate looks like coverage and is mostly not. This is not a fabricated fact, so it is major, not blocker.

Fix (pick one; record the choice in memory/ORCHESTRATOR_DECISIONS.md):
(a) add code candidate rules for same-measure pairs (laterality, date, dose, pain) in `conflict_candidates.py` (T-094 scope), then rerun the controls; or
(b) split the J3 control set into `reachable` (gated) and `capability` (reported, not gated), change the report's bar line to say which subset is gated, and say in the changelog which items the shipped code proposes.
Either way, the J3 gate must not count an item the code never sends.

Acceptance test: a unit test that, for each gated J3 item, builds two records from `excerpt_a`/`excerpt_b` and asserts `conflict_candidates.candidates()` proposes that pair. It goes red if a rule is removed. The live report lists the reachable and capability subsets separately.

## M-2 (major): J4W7 label stands; judge is unstable; fix the prompt, not the label

Second-agent review requested by the coordinator (D-046).

- Row: `evals/golden/judge_controls.jsonl`, J4W7: category `missed_care`, expected `disagree`, excerpt "Patient walked at the scene and declined ambulance transport.", why "quote has no missed care".
- Label history: the row was created in `e491cad` (round 1, before any live run) with the same category, excerpt and expected value. `git show e491cad:evals/golden/judge_controls.jsonl | grep J4W7` and `9217f8a` give the same `expected: disagree`. Only the `pair` field was added in `7df65fb`. The label has not changed after a failed run.
- Rule text: `app/llm/prompts/judge_flag_v2.md:17`: "missed_care: missed or cancelled appointments, non-attendance, discharge for non-attendance." The quote names none of these. A refusal at the scene is not a missed appointment, not non-attendance at scheduled care, and not a discharge. The product definition (`memory/DECISIONS.md:274`, "Missed or ended care in {provider} ({date})") is also about care in a provider's plan, which an EMS scene refusal is not.
- The same prompt puts the quote in scene_facts: `judge_flag_v2.md:19`, "scene_facts: ... (walked at scene, refused transport, minimal damage)". `app/llm/prompts/flags_v1.md:16` says the same. Under the prompt's own rule 4 the correct answer is `disagree` / `WRONG_CATEGORY`. The paired control J4C7 (same quote, scene_facts, agree) already encodes the right category.
- Verdict on the label: **the label is right; `missed_care` is wrong for this quote.** The judge's `agree` on 1 of 3 repeats (`evals/reports/controls-20261102T063331Z.md`, "unstable ['J4W7']") is a rule-application failure. It is not a reason to change the label.

Why it matters: a paralegal would see a scene refusal filed under missed care, and the one-of-three result keeps ship-bar item 4 red (controls_ok False). The control set is doing its job by failing.

Fix (backend): add a line to the missed_care rule in a new judge_flag version (for example `judge_flag_v3`, with the audit map and the judges.py id updated together): "A refusal at the scene or of transport is scene_facts, not missed_care." Rewrite the J4W7 `why` to cite rule 3 (scene_facts) and rule 4 (WRONG_CATEGORY). Do not change the label. If Chris decides that refused recommended transport should count as missed care (a failure-to-mitigate argument), that is a change to the category definition, which needs its own D-046 reason and a new label review. It is not a fix for this flag.

Acceptance test: a live controls run on the commit that changes the prompt cites J4W7 as disagree on 3 of 3 repeats, reason `WRONG_CATEGORY`, in the run artifacts; `git diff <prev>..<new> -- evals/golden` shows no change to J4W7's label.

Question for Chris (not blocking): see questions_for_chris.

## M-3 (minor): arithmetic guard is a regex a rewording evades

`tests/unit/test_t093_eval_signature.py:357-365` (`test_no_judge_control_needs_arithmetic_to_reach_its_label`) uses regexes on the excerpt text. Probe with the same regexes (python -I): "Physical therapy two visits per week for six weeks." + "Physical therapy plan of care: 12 visits." returns False, so the guard stays silent on a frequency times duration control. Fix: assert against `conflict_candidates.candidates()` output (each gated J3 pair either has no frequency or its `arithmetic` note is the only arithmetic), or keep an explicit list of removed arithmetic ids. Acceptance test: the reworded control above makes the guard fail.

## M-4 (minor): reject-all ship-bar test still missing (r2 F4)

`tests/unit/test_t093_eval_signature.py:214-218` checks catch rate and correct_accepted for a reject-all judge. It does not assert `ship_bar_met` is False. The r2 F4 fix asked for that. The handoff says it was not done. Fix: add `assert report(...)["ship_bar_met"] is False` for a judge that answers benign or disagree to everything. Acceptance test: that assertion, red if flag recall is removed from ship_bar.

## M-5 (minor): card `commits` names a commit that is not this card's

`python3 tools/board.py show T-093` lists `commits: ["e491cad", "7df65fb", "9217f8a", "81aa55e", "2ab7896"]`. The card's own note at 2026-11-02T06:36:37Z says 81aa55e is a backend commit (T-092). Fix (orchestrator, through board.py): remove 81aa55e. Acceptance: `board.py show T-093` no longer lists it.

## Test results and the worker's three failures

- `.venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py` on the archive: **70 passed** in 1.49s, 0 failed.
- `.venv/bin/python -m pytest -q tests/unit` on the archive: **2214 passed, 4 skipped, 0 failed** in 158.19s.
- The worker's 3 failures in `test_t093_eval_signature.py` **do not exist at 2ab7896**. No failing test on the archive belongs to this card.
- Working-tree state: `git diff --stat HEAD -- tests evals/run.py evals/golden app/backend/judges.py app/llm/audited.py` is empty, so this file and its code match HEAD. Uncommitted edits exist in `app/backend/{api,billing,credibility,generator,pipeline,trace,why}.py` and `tests/unit/test_flags_pass.py`, plus untracked fixtures. The 3 failures probably come from one of those or from a run before the commit. I did not run the working tree (pytest writes caches into the repo). Those edits belong to other cards, so they are outside this verdict.

## Live evidence

Not re-run. I did not call any LLM and made no network call. The controls report is cited as written, and its header and hashes check out (see item 5 above). The J4W7 instability is the report's own result.

## Exercised

- Read `personas/staff-engineer.md` (live dossier), my T-093 memory file, `reviews/T-093-staff-engineer-r2.md`, `memory/ORCHESTRATOR_DECISIONS.md:54` (D-046), `python3 tools/board.py show T-093`.
- `git rev-parse HEAD`; `git archive 2ab7896 | tar -x` into the scratchpad archive path above.
- `.venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py` (archive): 70 passed. `.venv/bin/python -m pytest -q tests/unit` (archive): 2214 passed, 4 skipped.
- Mutation in the archive copy: `evals/run.py` count test replaced with `catch_rate >= 0.5`; pytest on the T-093 file: 2 failed; restored from `git show 2ab7896:evals/run.py`, cmp matched.
- Read: `evals/run.py:840-845`; `tests/unit/test_t093_eval_signature.py:214-218, 335-377, 357-365, 391-410`; `app/backend/conflict_candidates.py:26, 121-125`; `app/backend/flags.py:240-244`; `app/backend/judges.py:48-64`; `app/llm/audited.py:123-124`; `app/llm/prompts/judge_conflict_v4.md`; `app/llm/prompts/judge_flag_v2.md`; `app/llm/prompts/flags_v1.md:16`; `memory/DECISIONS.md:256, 274`; `evals/golden/judge_controls.jsonl` (all J3/J4 rows); `evals/golden/judge_controls_heldout.jsonl`; `evals/golden/judge_controls.CHANGELOG.md`; `evals/reports/controls-20261102T063331Z.md` header and json keys.
- `git show 9217f8a:app/backend/judges.py | sed -n 58,60p`, `git show 9217f8a:app/llm/audited.py` PROMPT_OF_STEP; sha256 of the 14 `hashes` entries against `git show 9217f8a:<path>`.
- `git show e491cad|7df65fb|9217f8a:evals/golden/judge_controls.jsonl | grep J4W7`; `git log -G'P4-scene'`.
- Scratch script `pairs_reach_judge.py` (path above) run with `-I`: 29 J3 rows, 6 reach.
- Regex probe of the arithmetic guard (python -I, three strings).
- `git status` / `git diff --stat HEAD` on tests, evals, app/llm, app/backend.
- `python3 tools/board.py show T-093` (read only).
- Did not run: any live LLM or controls run, the CLI sample case, the working tree, or any board write.

## Outside my lens

The Spanish judge id in PROMPT_OF_STEP, the trace failures from r2, and the product question on refused transport (a policy call, questions_for_chris).

```json
{"card": "T-093", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "HEAD 2ab789601644357fd87b3b143d6cf50b17b68cd5 (git archive in scratchpad); card commits 9217f8a (controls gate, arithmetic pairs, J3C10 reason) and 2ab7896 (controls report from clean worktree of 9217f8a). Files: evals/run.py:840-845, tests/unit/test_t093_eval_signature.py, app/backend/conflict_candidates.py, app/backend/flags.py:240-244, app/backend/judges.py:48-64, app/llm/audited.py:123-124, app/llm/prompts/judge_conflict_v4.md, app/llm/prompts/judge_flag_v2.md, evals/golden/judge_controls*.jsonl, evals/golden/judge_controls.CHANGELOG.md, evals/reports/controls-20261102T063331Z.md/.json. No app URL. No live run. Sample case not run.",
 "exercised": [
  "personas/staff-engineer.md; board.py show T-093; reviews/T-093-staff-engineer-r2.md; memory/ORCHESTRATOR_DECISIONS.md:54 (D-046); git rev-parse HEAD = 2ab789601644357fd87b3b143d6cf50b17b68cd5",
  "git archive 2ab7896 extracted to the scratchpad T-093-r3-2ab7896 directory; .venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py -> 70 passed",
  ".venv/bin/python -m pytest -q tests/unit (archive) -> 2214 passed, 4 skipped, 0 failed (158.19s)",
  "mutation in archive copy: evals/run.py controls_ok count test replaced with catch_rate >= 0.5 -> 2 failed, 68 passed; restored from git show 2ab7896:evals/run.py, cmp matched",
  "read evals/run.py:840-845; tests/unit/test_t093_eval_signature.py:214-218, 335-377, 357-365, 391-410; app/backend/conflict_candidates.py:26, 121-125; app/backend/flags.py:240-244; app/backend/judges.py:48-64; app/llm/audited.py:123-124",
  "read judge_conflict_v4.md, judge_flag_v2.md (lines 10, 17, 19), flags_v1.md:16, memory/DECISIONS.md:256 and :274, judge_controls.jsonl and judge_controls_heldout.jsonl (all J3/J4 rows), judge_controls.CHANGELOG.md, controls report header and json keys",
  "git show 9217f8a:app/backend/judges.py and audited.py PROMPT_OF_STEP; sha256 of the 14 report hashes against git show 9217f8a:<path>: all match, all present",
  "git show e491cad / 7df65fb / 9217f8a : J4W7 row; git log -G P4-scene on judge_controls.jsonl",
  "scratch script pairs_reach_judge.py run with python -I on the archive: 29 J3 rows, 23 NOT PROPOSED by conflict_candidates.candidates(), 6 reach (J3C1, J3C7, J3C2, J3C3, J3W12, J3W13)",
  "regex probe of test_no_judge_control_needs_arithmetic_to_reach_its_label with python -I (three strings)",
  "git diff --stat HEAD and git status on tests, evals, app/llm, app/backend: no tracked diff in the T-093 chain; uncommitted edits in other cards' app/backend files",
  "python3 tools/board.py show T-093 (read only). No live LLM, no network, no board write, working tree not run"
 ],
 "verdict": "changes",
 "scores": {"gate_every_pinned": 5, "arithmetic_moved_to_code_tests": 4, "j3_controls_reach_judge": 2, "j3c10_reason": 4, "evidence_commit_and_clean_tree": 5, "audit_prompt_ids_match_judges": 5, "j4w7_second_agent_label": 4, "test_suite_green_at_head": 5, "llm_vs_code_boundary_in_controls": 3},
 "findings": [
  {"severity": "major",
   "title": "J3 controls hold mostly pairs the shipped code never proposes to the judge; the 17/17 gate measures 2 wrong items on the production path",
   "evidence": "app/backend/conflict_candidates.py:121-123 candidates() = plan_vs_outcome + history_denials, the only rules; app/backend/flags.py:240-244 'CODE proposes the candidate pairs ... The model's only job is the classification of each candidate, by J3'. Repro: cd <archive 2ab7896> && /Users/arsis/zlayt-pm-project/.venv/bin/python -I /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/T-093-r3-scripts/pairs_reach_judge.py <archive>: 23 of 29 J3 rows NOT PROPOSED, including 15 of 17 wrong items (J3W1-J3W5, J3W11, J3W14-J3W19, H3W2-H3W4) and 8 of 12 correct items. Reached: J3C1, J3C7, J3C2, J3C3, J3W12, J3W13.",
   "why_it_matters": "D-046 says the judges that decide flags must catch every seeded wrong decision. For the shipped app at this commit, laterality, date, dose and same-measure pain conflicts are never sent to J3, so the gate reports coverage of a path that does not exist and the AC 2 / changelog wording ('judgment pairs') hides it. Not a fabricated fact, so major, not blocker.",
   "fix": "Choose and record one in memory/ORCHESTRATOR_DECISIONS.md: (a) add code candidate rules for same-measure pairs (laterality, date, dose, pain) in conflict_candidates.py (T-094 scope) and rerun controls; or (b) split the J3 control set into reachable (gated) and capability (reported, not gated), state in the report and changelog which subset is gated and which items the shipped code proposes. Either way an item the code never sends must not count toward the gate.",
   "acceptance_test": "Unit test: for each gated J3 item, build two records from excerpt_a/excerpt_b and assert conflict_candidates.candidates() proposes that pair; red when a rule is removed. The next live controls report lists reachable and capability subsets separately."},
  {"severity": "major",
   "title": "J4W7 label stands (scene refusal is scene_facts, not missed_care); judge_flag_v2 said agree on 1 of 3 repeats, ship-bar item 4 is red; fix the prompt, do not relabel",
   "evidence": "evals/golden/judge_controls.jsonl row J4W7: category missed_care, expected disagree, excerpt 'Patient walked at the scene and declined ambulance transport.' Label unchanged since e491cad (git show e491cad:evals/golden/judge_controls.jsonl | grep J4W7 shows expected disagree). app/llm/prompts/judge_flag_v2.md:17 'missed_care: missed or cancelled appointments, non-attendance, discharge for non-attendance.'; :19 'scene_facts ... (walked at scene, refused transport, minimal damage)'. evals/reports/controls-20261102T063331Z.md: unstable ['J4W7']; controls_ok False. memory/DECISIONS.md:274 missed_care = 'Missed or ended care in {provider}'.",
   "why_it_matters": "Second-agent review: the label is correct. The quote names no missed or cancelled appointment, no non-attendance, no discharge, and rule 3 lists this quote under scene_facts, so rule 4 gives disagree / WRONG_CATEGORY. The paired J4C7 already encodes scene_facts. The 1-of-3 agree is a rule-application failure, and it keeps the every-wrong-item gate red. A paralegal would otherwise see a scene refusal filed as missed care.",
   "fix": "Backend: new judge_flag version (e.g. judge_flag_v3, with the judges.py id and audited.PROMPT_OF_STEP updated together) adding to the missed_care rule: 'A refusal at the scene or of transport is scene_facts, not missed_care.' Rewrite the J4W7 why to cite rule 3 (scene_facts) and rule 4 (WRONG_CATEGORY). Do not change the label. If Chris wants refused recommended transport to count as missed care, that is a category-definition change with its own D-046 reason and label review.",
   "acceptance_test": "Live controls run on the prompt-change commit: J4W7 disagree on 3 of 3 repeats with reason WRONG_CATEGORY in the run artifacts; git diff <prev>..<new> -- evals/golden shows no change to the J4W7 label."},
  {"severity": "minor",
   "title": "Arithmetic guard is a regex that a rewording evades",
   "evidence": "tests/unit/test_t093_eval_signature.py:357-365 test_no_judge_control_needs_arithmetic_to_reach_its_label. Probe (python -I, same regexes): 'Physical therapy two visits per week for six weeks.' + 'Physical therapy plan of care: 12 visits.' -> False (guard silent).",
   "why_it_matters": "The guard exists to keep frequency-times-duration arithmetic out of judge controls (LLM_VS_CODE row 1). A reworded control passes it.",
   "fix": "Assert against conflict_candidates.candidates() output, or keep an explicit list of removed arithmetic ids and assert none reappears.",
   "acceptance_test": "Adding the reworded control above to the J3 set makes the guard test fail."},
  {"severity": "minor",
   "title": "Reject-all ship-bar test still missing (carried from r2 F4)",
   "evidence": "tests/unit/test_t093_eval_signature.py:214-218 test_a_judge_that_rejects_everything_catches_all_but_the_correct_accept_rate_shows_it asserts catch rate and correct_accepted only; no ship_bar_met assertion. Card handoff: 'Not done: reject-all ship_bar test (r2 minor)'.",
   "why_it_matters": "Over-rejection is only caught by a live run unless ship_bar_met is pinned for a reject-all judge.",
   "fix": "Add assert report(...)['ship_bar_met'] is False for a judge that answers benign or disagree to everything.",
   "acceptance_test": "The new assertion is green, and goes red when flag recall is removed from ship_bar."},
  {"severity": "minor",
   "title": "Card commits list names 81aa55e, which is a backend commit, not this card's",
   "evidence": "python3 tools/board.py show T-093 -> commits: [\"e491cad\", \"7df65fb\", \"9217f8a\", \"81aa55e\", \"2ab7896\"]; card note 2026-11-02T06:36:37Z: 'the earlier 81aa55e line is a mistake (that is a backend commit)'.",
   "why_it_matters": "The board is the source of truth; a wrong commit on the card misattributes the audit trail.",
   "fix": "Orchestrator removes 81aa55e through board.py (reviewers do not write the board).",
   "acceptance_test": "python3 tools/board.py show T-093 no longer lists 81aa55e in commits."}
 ],
 "whats_right": [
  "The controls gate is count-based and pinned: evals/run.py:840-845 plus test_the_controls_gate_is_every_wrong_item_not_a_rate; a threshold mutation turns 2 tests red.",
  "The controls evidence reproduces: report header and json name 9217f8a with a clean tree; all 14 listed hashes match sha256 at 9217f8a; audit ids equal judges.py for J1-J4; full unit suite 2214 passed, 0 failed at 2ab7896.",
  "The J3C10 relabel history is recorded with the run ID, the verdict, and the input edit, and the label basis is stated as product policy rather than rule 2."
 ],
 "questions_for_chris": [
  "J4W7: should a refusal of recommended transport at the scene (a failure-to-mitigate argument) be flagged as missed_care? This review says no under the spec wording ('Missed or ended care in {provider}') and the prompt's scene_facts rule. Your answer decides whether the label or the category definition changes.",
  "Reviewer model: this review ran as claude-haiku-5-5. CLAUDE.md section 6 puts engineering reviewers on Sonnet; raised in r1 and r2, still open."
 ]}
```
