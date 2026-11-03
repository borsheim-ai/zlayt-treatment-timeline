# T-122 review: staff-engineer-reviewer (fix e1ce8dc; code 5dfba88; live evidence 63e18ed)

Verdict: **pass**. The claim holds: the case_05 "judge unavailable 1" was a never-judged `LLM_ONLY` tray item that kept the compose default `JUDGE_UNAVAILABLE`; there was no missing recording, and e1ce8dc removes the cause. I found no blocker or major. Four minors and a nit are about evidence, card hygiene and one residual mislabel in the same tray.

Pinned state: `git rev-parse HEAD` printed `5dfba8889b9c5d98b2f29c6cea1fcf5ac23d51a7` at the start; it moved to `b348221875791414f7f36f3a0371b1424f81aba0`. `git diff --stat 5dfba88 b348221 -- app/backend/flags.py tests/unit/test_flags_pass.py` printed nothing. I used `git archive 5dfba88` (`.../scratchpad/T113_r1_head`), plus archives of `b66e748~1`, `b66e748` and `e1ce8dc`. Probes and scripts are in `artifacts/review-evidence/T-113-r1/`.

## Is the root cause right? (command evidence)

`probe_case05.py` runs `PL.run_case(text, "fixture")` on every golden case and prints `evals.run.judge_unavailable_in`:

| tree | `TOTAL judge_unavailable` | detail |
|---|---|---|
| `b66e748~1` (before T-113 code) | 0 | |
| `b66e748` (T-113 D-053 route) | 1 | `case_05_provider_conflict 1 [('f_r1_1', 'scene_facts', ['LLM_ONLY', 'JUDGE_UNAVAILABLE'], None)]` |
| `e1ce8dc` (the T-122 fix) | 0 | |
| `5dfba88` (HEAD at start) | 0 | |

So the claim is right, and it is slightly more than the card says: the unavailable item did not pre-exist, it was **created by b66e748** when T-113 turned a silent drop of the model's `scene_facts` proposal into a tray item (`flags.py:173-174`). Before that commit the item was dropped, so it was never counted. The item is never judged by design (`judge_flags` skips `rejected`, `flags.py:379`), so no recording could have changed the count: the card's own trace (notes 10:47Z) is right. `judge_unavailable_in` (`evals/run.py:421-424`) counts `"JUDGE_UNAVAILABLE" in reasons` or ladder verdict `unavailable`; the compose default put the reason there.

The fix, `flags.py:363-367` (`_to_tray`, `code == "LLM_ONLY"`), sets `_stage.judge = None` and removes `JUDGE_UNAVAILABLE`. `_to_tray(..., "LLM_ONLY")` is reached only from `run_flag_pass`'s `_tray` marker (scene_facts and `_model_conflicts`) and from `judge_flags` for model conflicts (`flags.py:381-382`); the judge path calls `_to_tray(f, "JUDGE_DISAGREES", reason)` (`:352`). So a judged item whose judge call fails still gets `JUDGE_UNAVAILABLE`; the fix does not hide a real unavailable judge. The suite is green (3214 passed) and the existing judge-failure tests are in it.

## Deterministic checks

- `pytest tests/unit -q -p no:cacheprovider` on the 5dfba88 archive: **3214 passed, 4 skipped** (3 "no git repository" in `test_eval_runner.py`, 1 live Spanish eval).
- Mutants against `test_flags_pass.py`, `test_conflict_candidates.py`, `test_t075_determinism.py`, `test_t126_filtered_by_rule.py`, `test_flags_sample.py`, `test_flags_injection.py` (`mutate.py`): FL4 (leave `_stage.judge` at the compose default, `flags.py:366`) -> red (pytest -x, first failure) on `test_a_tray_item_that_was_never_judged_does_not_carry_judge_unavailable`; FL5 (keep `JUDGE_UNAVAILABLE` in `reasons`, `flags.py:367`) -> red, same test. Both halves of the fix are pinned.
- `python -m evals.run --backend fixture --out <scratch>` on the 5dfba88 archive: `hallucination_catch_rate ... judge unavailable 0`; the blockers printed are `4_no_invented_facts` (only the fixture-backend unsupported_count/determinism it depends on) and `judge_controls not measured`; there is no "judge unavailable on N item(s) in the golden cases" blocker. The tray line reads `5 {"FILTERED_BY_RULE": 4, "LLM_ONLY": 1}` including `case_05_provider_conflict: 1`.
- Live reports at 63e18ed (`20261102T113305Z.md`, `115041Z.md`, `120809Z.md`): `Source commit 63e18ed41355dd5b9a7e4ef35cb1b9f936d0fbe6, tree clean`, `ship_bar_met: True`, `judge unavailable 0`. The per-run `case_05_provider_conflict.json` in `runs/20261102T111525Z`, `113305Z`, `115041Z` each have 0 flags with `JUDGE_UNAVAILABLE`.

## Findings

**F1 (minor) The fixture report cited as AC1 evidence is untracked and from a dirty tree.** AC1 cites `evals/reports/20261102T115517Z.md`. `git ls-files evals/reports | grep 115517` prints nothing (untracked); its lines 3-4 read `ship_bar_met: False` and `Source commit a44dced47c4baf691ad21b99fb2c7c373236e13a, tree DIRTY, not reproducible from the commit.` Someone cannot reproduce it from a commit. The claim it supports is true (I reproduced it on a clean archive), but the cited evidence does not meet the project's own provenance bar. Fix: cite the committed live reports at 63e18ed, or commit a clean-tree fixture report. Acceptance: the cited report is `git ls-files`-tracked and its header says `tree clean`.

**F2 (minor) AC1 is checked as done though its text was not what was done, and the card has no commit.** AC1 text: "Find the missing judge fixture key ... record it live (claude-cli, max 3 attempts ...)". No key existed and nothing was recorded (the right outcome under D-056, and the card notes say so). The AC was not amended or superseded on the board, and `python3 tools/board.py show T-122 | grep commits` prints `commits: []`, so e1ce8dc is not attached. Fix: orchestrator through board.py: attach e1ce8dc and record the AC as superseded by the root-cause finding. Acceptance: `python3 tools/board.py show T-122 | grep -c e1ce8dc` is at least 1.

**F3 (minor) A residual mislabel of the same kind remains in the same tray.** A model-proposed conflict is a `LLM_ONLY` tray item; archive probe `F.run_flag_pass` with `type=conflict` gives `reasons ['LLM_ONLY']`, `why` "The AI found this flag but the phrase list did not; check that it applies." (`why.py:25`). Conflicts have no phrase list; the reason is that only a code candidate can make a conflict (`flags.py:187-189`). T-122 fixed the judge-stage label of this tray item but not its reason sentence. Wording is outside my lens; the reason-to-cause mismatch is the T-122 class of defect. Fix: a conflict-specific reason code with its own sentence. Acceptance: a test that a model conflict's reasons/why do not mention the phrase list. (Also filed on T-113 as F5.)

**F4 (minor) The regression was introduced by a card that did not run the fixture eval before commit.** b66e748 is the commit that turned `judge_unavailable_in` from 0 to 1 (table above); T-113's note at 10:26Z records the unit suite only (2645 passed), and the qa card was opened at 10:44Z. Nothing in the unit suite pinned `judge_unavailable_in == 0` on case_05 until `test_case_05_has_no_judge_unavailable_item` arrived in e1ce8dc. The fix is in; the harness lesson is not recorded. Fix: orchestrator records a `board.py lesson` (a card that adds a tray route runs `python -m evals.run --backend fixture` and reads the case-level judge-unavailable count before review). Acceptance: `python3 tools/board.py` lesson text names the check.

**F5 (nit) The regression test hedges its own precondition.** `tests/unit/test_flags_pass.py` `test_case_05_has_no_judge_unavailable_item` reads `out = PL.run_case(...) if hasattr(PL, "run_case") else None` then `assert out is not None`. It fails loudly rather than silently, so it is safe, but the `hasattr` branch is dead. Fix: call `PL.run_case` directly. Acceptance: the test still passes and fails under FL4/FL5.

## Exercised

- `python3 tools/board.py show T-122` and `show T-113`; `git show e1ce8dc`; `git show b66e748 -- app/backend/flags.py`; `git ls-files evals/reports | grep 115517`.
- Archives of `b66e748~1`, `b66e748`, `e1ce8dc`, `5dfba88`: `probe_case05.py` (per-commit counts above).
- 5dfba88 archive: full unit suite, fixture eval, mutants FL4/FL5, probe of the model-conflict tray reason.
- Reports `20261102T113305Z.md`, `115041Z.md`, `120809Z.md` (headers, unavailable lines) and `runs/.../case_05_provider_conflict.json` x3.
- Not done: no live LLM run, no network, no UI. Recording a live judge answer was not needed and I did not attempt one.

```json
{"card": "T-122", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "fix e1ce8dc (app/backend/flags.py _to_tray LLM_ONLY branch, tests/unit/test_flags_pass.py); git archive 5dfba88 (files in scope identical at b348221); archives of b66e748~1, b66e748, e1ce8dc for the per-commit count; live evidence reports at 63e18ed; fixture backend; no app URL",
 "exercised": [
  "python3 tools/board.py show T-122 and show T-113; git show e1ce8dc; git show b66e748 -- app/backend/flags.py",
  "probe_case05.py (evals.run.judge_unavailable_in over every golden case, fixture backend) on archives of b66e748~1 (0), b66e748 (1: case_05 f_r1_1 scene_facts ['LLM_ONLY','JUDGE_UNAVAILABLE']), e1ce8dc (0), 5dfba88 (0)",
  "git archive 5dfba88: pytest tests/unit -q -> 3214 passed, 4 skipped",
  "mutants FL4 (judge stage left default) and FL5 (JUDGE_UNAVAILABLE kept) against the flags test files: both red on test_a_tray_item_that_was_never_judged_does_not_carry_judge_unavailable",
  "python -m evals.run --backend fixture on the 5dfba88 archive: judge unavailable 0, no case-level judge blocker",
  "reports 20261102T113305Z/115041Z/120809Z headers (source 63e18ed, tree clean, ship_bar_met True, unavailable 0) and case_05 run json x3 (0 JUDGE_UNAVAILABLE flags)",
  "git ls-files evals/reports | grep 115517 (untracked); head of evals/reports/20261102T115517Z.md (a44dced, tree DIRTY, ship_bar_met False)",
  "archive probe of a model-proposed conflict tray item: reasons ['LLM_ONLY'], why mentions the phrase list",
  "No live LLM run, no network, no UI"
 ],
 "verdict": "pass",
 "scores": {"root_cause_correct": 5, "fix_does_not_mask_real_failures": 5, "test_pins_the_fix": 4, "evidence_provenance": 3, "card_hygiene": 3},
 "findings": [
  {"severity": "minor",
   "title": "AC1 cites a fixture report that is untracked and from a dirty tree",
   "evidence": "git ls-files evals/reports | grep 115517 prints nothing; evals/reports/20261102T115517Z.md lines 3-4: 'ship_bar_met: False' and 'Source commit a44dced47c4baf691ad21b99fb2c7c373236e13a, tree DIRTY, not reproducible from the commit.'",
   "why_it_matters": "The claim it backs is true (reproduced on a clean archive: judge unavailable 0), but the evidence cannot be reproduced from a commit, which is the project's own provenance bar for eval reports.",
   "fix": "Cite the committed live reports at 63e18ed, or commit a clean-tree fixture report, and update the AC evidence.",
   "acceptance_test": "The cited report path is returned by git ls-files and its header says 'tree clean'."},
  {"severity": "minor",
   "title": "AC1 text does not match what was done, and the card carries no commit",
   "evidence": "AC1: 'Find the missing judge fixture key ... record it live (claude-cli, max 3 attempts ...)'; card notes 10:47Z: no FIXTURE_MISS exists, nothing recorded. python3 tools/board.py show T-122 prints 'commits: []'",
   "why_it_matters": "The board is the source of truth: an AC marked done for different work than it states, and no commit attached, weakens the audit trail.",
   "fix": "Orchestrator, through board.py: attach e1ce8dc and record that AC1 is superseded by the root-cause finding.",
   "acceptance_test": "python3 tools/board.py show T-122 | grep -c e1ce8dc prints at least 1."},
  {"severity": "minor",
   "title": "A model-proposed conflict in the same tray still carries a reason that is not its cause",
   "evidence": "Archive probe: F.run_flag_pass with a type 'conflict' proposal gives reasons ['LLM_ONLY'] and why 'The AI found this flag but the phrase list did not; check that it applies.' (app/backend/why.py:25); flags.py:187-189 says only a code candidate can make a conflict",
   "why_it_matters": "T-122 fixed the judge-stage label for this tray class; the reason sentence for conflicts is the same kind of mismatch between label and cause. Wording itself is outside my lens.",
   "fix": "Add a conflict-specific reason code and sentence (for example NO_CODE_CANDIDATE) for _model_conflicts.",
   "acceptance_test": "A test that a model conflict's reasons and why do not mention the phrase list."},
  {"severity": "minor",
   "title": "The regression came from T-113's own commit and no lesson or pre-commit eval check is recorded",
   "evidence": "probe_case05.py: judge_unavailable_in is 0 at b66e748~1, 1 at b66e748, 0 at e1ce8dc; board note T-113 10:26:13Z lists only 'unit suite 2645 passed'; T-122 was created 10:44:40Z",
   "why_it_matters": "A card that adds a tray route changed a gated eval count and merged without the eval being read; the harness should learn from it (CLAUDE.md non-negotiable 9).",
   "fix": "Orchestrator records a board.py lesson: a card that adds or changes a tray route runs the fixture eval and reads the case-level judge-unavailable count before review.",
   "acceptance_test": "A lesson entry in memory/LESSONS.md naming the check."},
  {"severity": "nit",
   "title": "Regression test hedges its own precondition",
   "evidence": "tests/unit/test_flags_pass.py:431 in test_case_05_has_no_judge_unavailable_item: out = PL.run_case(G.raw(case_05_provider_conflict), fixture) if hasattr(PL, run_case) else None, then assert out is not None",
   "why_it_matters": "It fails loudly, so it is safe; the hasattr branch is dead code that hides intent.",
   "fix": "Call PL.run_case directly.",
   "acceptance_test": "The test still passes and still goes red under mutants FL4 and FL5."}
 ],
 "whats_right": [
  "The diagnosis is correct and provable by command: judge_unavailable_in is 0, 1, 0 across b66e748~1, b66e748, e1ce8dc, so no recording could have fixed it, and D-056 (no scripted judge answers) was respected.",
  "The fix is narrow: only the LLM_ONLY branch clears the judge stage and JUDGE_UNAVAILABLE, so a judged flag whose call fails still reports JUDGE_UNAVAILABLE.",
  "Both halves of the fix are pinned: removing either the stage reset or the reason filter turns test_a_tray_item_that_was_never_judged_does_not_carry_judge_unavailable red."
 ],
 "questions_for_chris": []}
```
