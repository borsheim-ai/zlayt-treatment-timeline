# T-093 r2 review: staff-engineer-reviewer (card commit 7df65fb)

Verdict: **fail**. One blocker, three majors, four minors, one nit. Every finding cites `7df65fb` content (read with `git show 7df65fb:...` or from a `git archive 7df65fb` export). HEAD moved to bc12d44 and then a850be0 during the review; I did not review those commits, but I checked the blocker's defect still exists at bc12d44.

## 1. Major 1 (r1 F1): fixed in substance, with residue

The J3 set is now matched pairs. Visit count (J3W10/J3C6, H3W1/H3C1), laterality (J3W14/J3C4, J3W15/J3C8), date (J3W17/J3C5), dosage (J3W18/J3C9), denial (J3W12, J3W13 / J3C3), and plan-vs-completion (J3W11 / J3C1, J3C7, J3C2) all share keywords and differ in the fact. There are 8 same-fact, consistent-value wrong items. All 60 items carry a `why`. The markerless pain pair is restored as `correct`/`conflict`, and the marked pair stays `wrong`/`benign`. Labels are fixed in the file, and the committed report matches them on all 60 rows.

Residue, all in the findings below: four unrelated-topic wrong items have no partner (F-5); the changelog does not cite run 20261102T035750Z as F1 asked (F-7); the J3C10 reason is not right as written (F-6). J4 pairs are done where cheap (six pairs), so J4 is fine.

## 2. D-046 second-agent review of the two label decisions

**J3W1, `Visit 1: neck pain 6/10, daily headaches.` / `Visit 9: neck pain 3/10, headaches weekly.`, expected benign: right.** Rule 3 applies on the face of the quotes. They name two different visits, the same measure, and a normal change over time (6 to 3, daily to weekly). The original relabel was not supported by the rules at the time, because the markerless text shows no visits. But the card records that the input was edited after a failed run, and D-046 says never because it failed. The split is the right repair in direction, and the changelog must say what happened (F-7).

**J3C10, `Neck pain 6/10, daily headaches.` / `Neck pain 3/10, headaches weekly.`, kind correct, expected conflict: right as a flag decision, wrong as the basis the card gives.** The card's reason is "as written, rule 2". Two undated pain scores for one body part can both be accurate, because pain changes over time, so rule 2's "cannot both be accurate" is not literally met. Rule 3's benign condition is not met either, since nothing in the quotes shows different visits. The conflict label holds on product policy: an undated disagreement is what the paralegal must reconcile, and a benign label would drop it silently. The item is `correct`, so it is reported and not gated, and the ship bar does not move. The reason and the changelog need rewriting, and T-094's rule 3 should say this outright (F-6).

## 3. J3W11 (expected benign) during T-094's v3 prompt

The control is correct. The plan was 12 visits, and the record says 12 were completed, with a discharge and goals met. There is nothing to reconcile. The miss comes from the rule-1 wording, which is identical in judge_conflict_v2 (committed) and judge_conflict_v3 (uncommitted, `app/llm/prompts/judge_conflict_v3.md:6`): "the other quote shows that course ended or changed (a discharge, a stop, ...)". Read literally, any discharge is an ended course, including a completed one. The fix belongs to T-094: "ended early, stopped, fewer visits than planned, or a different regimen; a discharge after the full planned course is not a conflict." Do not relabel J3W11 to conflict, because that is the D-046 failure mode. J3C1, J3C7 and J3C2 (conflict: discharged after missed or fewer visits) already separate the cases, so the rule can change without touching the set.

## 4. Brief's pytest selection

`.venv/bin/python -m pytest -q tests/unit -k "eval_runner or controls"` on the 7df65fb export: **73 passed, 1263 deselected**, exit 0. That selection does not include the round-2 label tests, because `test_t093_eval_signature.py` does not match either keyword (its test names say `control_file`, not `controls`). I ran that file separately: **61 passed**. Full `tests/unit`: 1330 passed, 6 failed (see outside-card section, and F-1 for the one in T-093's chain).

## Blocker and majors

- **F-1 (blocker).** Audit rows name `judge_conflict_v3` while the text sent is `judge_conflict_v2`. `audited.py:100` maps `j3` to v3 and `audited.py:113` stores it as `prompt_version`, while `judges.py:59` loads v2. The row's `prompt_sha256` is over the v2 text. The failing test is `test_t075_determinism.py:56`.
- **F-2 (major).** The committed controls report measured a prompt that is not in the commit. The gate numbers in AC 2 come from the uncommitted v3 file.
- **F-3 (major).** The gate is `catch_rate >= 0.95`, not "every" as D-046 and spec §7 row 4 say. A mutation to 0.5 leaves all 132 tests green.
- **F-4 (major).** Round 2 added J3 controls that have the judge multiply visit counts. LLM_VS_CODE row 1 says no model does arithmetic. Two gated wrong items (J3W10, H3W1) depend on it.

## Outside this card (observed at 7df65fb, not counted in this verdict)

- **CLI crash, blocker for the product's checklist item 20, route to backend.** `7df65fb:app/backend/pipeline.py:501` calls `IN.ingest(raw)` before `raw = open(a.file, ...)` at line 506. `.venv/bin/python -m app.pipeline evals/golden/sample.txt` raises `UnboundLocalError: cannot access local variable 'raw'`. That is `tests/unit/test_t037_backend.py:26` failing. Introduced by 865b186 (T-085). Still at bc12d44:501.
- **Four `tests/unit/test_trace.py` failures** (`KeyError: 'steps'` at line 519). I did not investigate them; outside my lens.

## Exercised

Listed in the JSON block.

```json
{"card": "T-093", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "card commit 7df65fb, pinned (HEAD moved to bc12d44 and a850be0 during review, not reviewed). Files: evals/golden/judge_controls.jsonl, evals/golden/judge_controls_heldout.jsonl, evals/golden/judge_controls.CHANGELOG.md, evals/run.py (judge_controls_metrics, controls_ok, control_prompt), tests/unit/test_t093_eval_signature.py, evals/reports/controls-20261102T042306Z.md and .json, app/backend/judges.py:59, app/llm/audited.py:74,100,113, spec/REQUIREMENTS.md:319-328, memory/ORCHESTRATOR_DECISIONS.md D-046. No app URL. Sample case not re-run. No live controls run. The working tree was not used for any finding; it lacked the changelog and held-out file at one point during the review.",
 "exercised": [
  "Read personas/staff-engineer.md, reviews/T-093-staff-engineer.md (r1), my T-093 memory file; python3 tools/board.py show T-093 (card notes 2026-11-02T04:23:02Z J3W1 relabel and round-2 labels); D-046 via git show 7df65fb:memory/ORCHESTRATOR_DECISIONS.md (line 54).",
  "git archive 7df65fb | tar -x -C artifacts/review-evidence/T-093-r2-HEAD. git worktree add was refused by board-guard outside /tmp, so the export is the same tracked tree. The export was left in place because rm was denied; reproduce with the same git archive command.",
  ".venv/bin/python -m pytest -q tests/unit -k \"eval_runner or controls\" (export) -> 73 passed, 1263 deselected, exit 0.",
  ".venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py (export) -> 61 passed.",
  ".venv/bin/python -m pytest -q tests/unit (export) -> 1330 passed, 6 failed: test_t037_backend.py::test_cli_sample_on_fixture_backend_under_60s (CLI UnboundLocalError), test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2 (judge_conflict_v3 != judge_conflict_v2, line 56), test_trace.py x4 (KeyError 'steps', line 519).",
  "Mutation in export: evals/run.py:793 ge_ threshold THRESHOLDS[hallucination_catch_rate] (0.95) replaced by 0.5; .venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py tests/unit/test_eval_runner.py -> 132 passed. Restored with git show 7df65fb:evals/run.py (grep confirmed the original line).",
  "Structural check over 60 rows (judge_controls.jsonl + judge_controls_heldout.jsonl at 7df65fb): missing why 0; kind/expected mismatches 0; same_fact wrong items 8 (J3W10, J3W11, J3W14, J3W15, J3W17, J3W18, H3W1, H3W4); pair groups with no correct partner: P4-ct, P3-unrelated, H3-bp, H3-ankle; pair groups with no wrong item: P4-onset, P4-surgery, H3-loc, H3-plan, H4-onset.",
  "Committed report: git show 7df65fb:evals/reports/controls-20261102T042306Z.md line 3 'prompts judge_conflict_v3, judge_flag_v2'; the .json has prompts j3 judge_conflict_v3 and hashes including app/llm/prompts/judge_conflict_v3.md; 60 item rows compared with the pinned jsonl -> 0 label mismatches; J3C10 conflict 3/3, J3W1 benign 3/3, J3W11 conflict 3/3, J3W10 benign 3/3.",
  "git cat-file -e 7df65fb:app/llm/prompts/judge_conflict_v3.md -> missing. git show 7df65fb:app/backend/judges.py | sed -n 59p -> _run(\"j3\", \"judge_conflict_v2\"). git show 7df65fb:app/llm/audited.py | grep -n PROMPT_OF_STEP -> line 100 j3 judge_conflict_v3. Export audited.py:74 (prompt_version=prompt_version, prompt_sha256=h) and :113 (prompt_version=PROMPT_OF_STEP.get(step)) read.",
  "git show 7df65fb:evals/golden/judge_controls.CHANGELOG.md | grep -c 035750Z -> 0. git show 7df65fb:spec/REQUIREMENTS.md | grep -n judge_controls -> no output. git show 7df65fb:spec/REQUIREMENTS.md line 328 read (row 4). git show 7df65fb:docs/LLM_VS_CODE.md line 11 read (arithmetic never done by a model).",
  "Read app/llm/prompts/judge_conflict_v2.md (7df65fb) and the uncommitted app/llm/prompts/judge_conflict_v3.md rule 1 (line 6) to compare the discharge wording.",
  "HEAD bc12d44 spot check: git show bc12d44:app/backend/judges.py line 59 (judge_conflict_v2); bc12d44:app/llm/audited.py line 123 (j3 judge_conflict_v3); bc12d44:app/backend/pipeline.py line 501 (IN.ingest(raw) before raw at 506). Both defects still present.",
  "Read evals/run.py judge_controls_metrics at 7df65fb (caught excludes unavailable, line 532; docstring at line 499 for the D-046 gate scope); tests/unit/test_t093_eval_signature.py:313 (controls_ok True for over-rejection, by design).",
  "Did not run any LLM call, live controls run, network call, or board.py review/write. Board used read-only (show)."
 ],
 "verdict": "fail",
 "scores": {"j3_matched_pairs": 4, "j3_label_decisions_d046": 3, "j4_matched_pairs": 4, "gate_matches_d046": 2, "gate_tested": 1, "evidence_reproducible_at_commit": 1, "audit_prompt_provenance": 1, "llm_vs_code_boundary_in_controls": 2, "report_labels_match_pinned_file": 5, "test_selection_as_briefed": 3},
 "findings": [
  {"severity": "blocker", "title": "Audit rows name judge_conflict_v3 for every J3 call; the text sent is judge_conflict_v2",
   "evidence": "7df65fb:app/llm/audited.py:100 PROMPT_OF_STEP 'j3': 'judge_conflict_v3' (added in 865b186); audited.py:113 passes prompt_version=PROMPT_OF_STEP.get(step) into audited_call; audited.py:74 stores prompt_version with prompt_sha256 computed over the system text actually sent; 7df65fb:app/backend/judges.py:59 run_j3_meta loads 'judge_conflict_v2'; git cat-file -e 7df65fb:app/llm/prompts/judge_conflict_v3.md fails. Repro: export 7df65fb, .venv/bin/python -m pytest -q tests/unit/test_t075_determinism.py::test_j3_prompt_carries_the_flag_category_and_judge_prompts_are_v2 -> AssertionError: assert ('judge_conflict_v3' == 'judge_conflict_v2') at test_t075_determinism.py:56. Same defect at bc12d44 (judges.py:59 v2, audited.py:123 v3).",
   "why_it_matters": "The audit record for every J3 decision names a prompt that did not run. The hash is correct, so the text is recoverable, but the named version is false. Checklist 9 and D.2 (invents a fact) apply. T-093's live evidence is attached to this record (F-2).",
   "fix": "Use one source for the id: have _run pass the id it loads (judge_conflict_v2 or whichever is committed) into the call and store that, or set PROMPT_OF_STEP['j3'] to the id judges.py loads. Owner: backend (app/llm/audited.py), in the same commit as the prompt change.",
   "acceptance_test": "tests/unit/test_t075_determinism.py green on the commit. New fixture-backend test: for each judge step, the audit row's prompt_version equals the loaded prompt id and prompt_sha256 equals the sha256 of the sent system text."},
  {"severity": "major", "title": "Committed controls evidence names a prompt that is not in the commit",
   "evidence": "7df65fb:evals/reports/controls-20261102T042306Z.md line 3: 'prompts judge_conflict_v3, judge_flag_v2'; the .json hashes include app/llm/prompts/judge_conflict_v3.md (2bd186744cf79f40...), which is absent from 7df65fb. board show T-093 AC 2 cites 'J3 18/19 wrong caught' from this report; the T-093 note at 2026-11-02T04:23:02Z says judges.py in the working tree calls judge_conflict_v3 (T-094, uncommitted).",
   "why_it_matters": "The 18/19 and the J3W11 finding were measured on code that is not in the commit. The report's controls_ok False is right, but the numbers cannot be reproduced from 7df65fb, where control_prompt('j3') reads judges.py and returns judge_conflict_v2.",
   "fix": "After T-094's prompt is committed, rerun LLM_BACKEND=claude-cli ENABLE_LIVE=1 python3 -m evals.run --controls on that commit and cite that report. Until then, the card should say the report measured the working-tree prompt.",
   "acceptance_test": "In the new report, the prompts line equals the id in the commit's judges.py, and every hash it lists is a file in that commit (git ls-tree)."},
  {"severity": "major", "title": "Gate is catch_rate >= 0.95, not 'every wrong item' as D-046 and spec §7 row 4 say; no test pins it",
   "evidence": "7df65fb:evals/run.py:793 'return all(ge_(jc[j][\"catch_rate\"], THRESHOLDS[\"hallucination_catch_rate\"]) and not jc[j][\"false_agree\"] ...)'; evals/run.py:37 hallucination_catch_rate 0.95; memory/ORCHESTRATOR_DECISIONS.md:54 D-046 'each must catch every seeded wrong item'; spec/REQUIREMENTS.md:328 'must also catch every seeded wrong item'; the report's bar cell says 'all wrong caught, 0 false agree'. Mutation: evals/run.py:793 threshold 0.95 -> 0.5 in the export; .venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py tests/unit/test_eval_runner.py -> 132 passed. 19 x 0.95 = 18.05, so 18/19 fails today only by rounding; with 20 wrong items, one miss passes.",
   "why_it_matters": "The displayed bar and the signed decision say 'every'; the code says 95%. The gate is right today by set size. A future threshold change or a larger set would pass a miss, and no test would notice.",
   "fix": "controls_ok requires wrong_caught == wrong_total for each judge and no false_agree. Leave the report's bar text as it is.",
   "acceptance_test": "Add to test_t093_eval_signature.py: 18 of 19 caught -> controls_ok False; 19 of 19 -> True; 20 wrong items with one miss -> False. Changing the threshold to 0.5 turns at least one test red."},
  {"severity": "major", "title": "J3 controls ask the judge to multiply visit counts; LLM_VS_CODE row 1 says no model does arithmetic",
   "evidence": "7df65fb:docs/LLM_VS_CODE.md:11 'Arithmetic, dates, totals, ... are never done by a model.' evals/golden/judge_controls.jsonl:21 J3W10 ('Physical therapy 2x/week for 6 weeks.' vs 'Physical therapy plan of care: 12 visits.', expected benign, gated); :22 J3C6 (same plan vs '10 visits', expected conflict); evals/golden/judge_controls_heldout.jsonl:1 H3W1 (2 x 4 = 8, benign, gated) and :2 H3C1 (3 x 4 = 12 vs 8, conflict). judge_conflict_v2 rule 2 at 7df65fb has the judge do the multiplication; uncommitted app/llm/prompts/judge_conflict_v3.md:6 says software does the arithmetic and the judge must not answer conflict over it.",
   "why_it_matters": "Round 2 added arithmetic items. They measure a behaviour the design forbids. After T-094, the path they test is not reached by the shipped judge, so two gated wrong items measure nothing about it. The matrix in LLM_VS_CODE is graded row by row.",
   "fix": "Replace these four items with pairs in which code has already supplied the visit count in the excerpt (the judge only classifies), or remove them from the judge gate and cover the arithmetic in code unit tests. Removing the judge-does-arithmetic path is T-094's.",
   "acceptance_test": "No judge control requires a multiplication to reach its label. A unit test on the code visit arithmetic covers 2x/week for 6 weeks = 12 visits and 2x/week for 4 weeks = 8."},
  {"severity": "minor", "title": "Unrelated-topic wrong items have no partner; F1's acceptance test is not met for them",
   "evidence": "evals/golden/judge_controls.jsonl:42 J3W2 ('Left shoulder pain, no radiation.' vs 'Left knee MRI unremarkable.'), :43 J3W3 (two different medications), :45 J3W5 ('Patient is right-hand dominant.' vs 'Right wrist X-ray negative for fracture.'). Structural check: pair P3-unrelated has 4 wrong items and no correct item; P4-ct has one wrong item and none correct. J3W2 and J3W5 share no fact name or topic across their quotes.",
   "why_it_matters": "These items carry the same weight in the gate as the paired ones. A keyword matcher passes most of them, so the 19-item figure mixes easy and hard cases. The r1 acceptance test asked for every J3 wrong item to share a fact name or topic across its two quotes.",
   "fix": "Report the paired and same_fact subset's catch rate separately in the controls report, or replace the four unrelated items with generator-plausible pairs.",
   "acceptance_test": "The controls report lists the paired-subset catch rate, or the unrelated items are removed from the gate and a test checks that each remaining wrong item shares a fact name or topic."},
  {"severity": "minor", "title": "J3C10 label is right, but the reason on the item and in the changelog is not",
   "evidence": "evals/golden/judge_controls.jsonl:40 J3C10 why: 'no visit or date in either quote, so as written they state two different pain levels (rule 2)'. judge_conflict_v2 rule 2 (7df65fb): 'cannot both be accurate as written'. Two undated pain scores can both be accurate. Rule 3's benign condition ('different visits ... a normal change over time') is also not shown on the face of J3C10.",
   "why_it_matters": "D-046 requires a written reason that a second agent reviews. This reason does not hold under a literal reading of rule 2, and the real basis is a product policy (an undated disagreement must be reconciled, not dropped) that is written nowhere. J3C10 is correct-kind and reported, not gated, so the gate does not move.",
   "fix": "Rewrite the why and the changelog entry to state the policy basis. Ask T-094 to make rule 3 say that two readings of one measure with no date or visit in either quote are a conflict to reconcile.",
   "acceptance_test": "evals/golden/judge_controls.CHANGELOG.md contains a J3C10 entry naming the policy and the rule; grep -n 'undated' on the changelog returns it."},
  {"severity": "minor", "title": "Changelog lacks the citation F1 asked for, and the input edit after the failed run is not recorded there",
   "evidence": "git show 7df65fb:evals/golden/judge_controls.CHANGELOG.md | grep -c 035750Z -> 0. The relabel (benign label kept while visit markers were added after run 20261102T035750Z failed) appears only in the card notes at 2026-11-02T04:23:02Z.",
   "why_it_matters": "F1's fix asked the changelog to cite run 20261102T035750Z and the verdict. The changelog is the file a later reader opens, and the D-046 rule (no relabel because it failed) is only checkable there.",
   "fix": "Add a changelog entry: run ID 20261102T035750Z, verdict FACT_MISMATCH on J3W1 as first written, the input edit made after that failure, and the split into J3C10 and J3W1 with the reason.",
   "acceptance_test": "grep -n 035750Z evals/golden/judge_controls.CHANGELOG.md returns a line."},
  {"severity": "minor", "title": "F4 is not closed: no test ties a reject-all judge to ship_bar_met",
   "evidence": "tests/unit/test_t093_eval_signature.py:313 asserts R.controls_ok(jc) for an over-rejecting judge with the message 'over-rejection is reported, not gated'. evals/run.py judge_controls_metrics docstring (line 499) records the reason correct_accepted is not gated. No test runs a reject-all judge through ship_bar.",
   "why_it_matters": "The reason is recorded, which is acceptable for correct_accepted. The other half of F4's fix (a test that a reject-all judge leaves ship_bar_met False) is missing. Over-rejection is then caught only by a live run.",
   "fix": "Add a fixture-backend test: a judge that answers benign or agree to everything leaves ship_bar_met False through flag recall (bar 3).",
   "acceptance_test": "The new test is green, and it goes red when flag recall is removed from ship_bar."},
  {"severity": "nit", "title": "Spec row 4 does not name the controls metric",
   "evidence": "git show 7df65fb:spec/REQUIREMENTS.md | grep -n judge_controls -> no output. Row 4 (line 328) says 'Seeded J3/J4 control sets must also catch every seeded wrong item with 0 false agrees (D-046)' but its Measured by column lists no controls key.",
   "why_it_matters": "The content is there. A grep-based check against the spec does not find the metric.",
   "fix": "Add judge_controls to row 4's Measured by column.",
   "acceptance_test": "grep -n judge_controls spec/REQUIREMENTS.md returns the row-4 line."}
 ],
 "whats_right": [
  "Matched pairs cover visit count, laterality, date, dosage, denial and plan-vs-completion, with 8 same-fact wrong items, and all 60 items carry a why.",
  "The committed report's 60 item labels equal the pinned controls file (0 mismatches), and J3W11's three false agrees are shown rather than relabelled.",
  "judge_controls_metrics does not count 'unavailable' as a catch (evals/run.py:532), so a dead judge cannot pass the catch gate."
 ],
 "questions_for_chris": [
  "Policy: should two undated readings of one measure (pain 6/10 vs 3/10, no visit or date in either quote) be a flag for the paralegal? The control labels them conflict; your answer decides that label.",
  "Reviewer model: this review ran as claude-haiku-5-5; CLAUDE.md section 6 puts engineering reviewers on Sonnet. Raised in r1 and still open."
 ]}
```
