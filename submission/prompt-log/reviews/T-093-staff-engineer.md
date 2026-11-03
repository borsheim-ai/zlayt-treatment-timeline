# T-093 review: staff-engineer-reviewer (commit e491cad, HEAD at review time)

Verdict: **changes**. No blocker, two majors, three minors, one nit.

The determinism signature now covers every R-CO-7 field, and the 29 field mutations are red on HEAD. Three scratch breaks of the signature each turned red. Per-run artifacts are allowlisted and contain no prompts or secrets. The weak part is the judge controls. The J3 set cannot tell a judge that follows its rules from one that matches keywords, and its one same-fact item was relabelled after it failed. The ship-bar gate on those controls was added without the ADR the spec requires. The live bar has three failing blockers, not one; the causation precision failure is outside the conflict-flag framing.

Scope note: the live run was not re-run for this review. I read the committed live reports and the T-094 notes.

## Findings

**F1 major. The J3 control set cannot separate rule-following from keyword matching, and its one same-fact item was relabelled after it failed.**
- Evidence: `evals/golden/judge_controls.jsonl:17` (J3W1): `"excerpt_a": "Visit 1: neck pain 6/10, daily headaches.", "excerpt_b": "Visit 9: neck pain 3/10, headaches weekly."`, expected `benign`. Its `why` says v1 had no visit markers and J3 returned FACT_MISMATCH on run 20261102T035750Z, "a labelling error". `app/llm/prompts/judge_conflict_v2.md` rule 2 says FACT_MISMATCH when both quotes state a fact about the same thing (a number is named) and cannot both be accurate as written. Rule 3 says benign only for different visits, different topics, or a normal change over time. Without visit markers, the v1 pair falls under rule 2, so the judge's v1 answer followed the prompt. The expectation was wrong, and the input was changed to fit it. Of the five wrong J3 items, W1 and W4 are separated by visit words that rule 3 names, W2 and W5 are unrelated topics the generator would not propose, and W3 is a different-medication pair. None is a same-fact pair with consistent values. The 5/5 at `evals/reports/20261102T040933Z.md:20` therefore measures keyword matching more than rule 2 against rule 3. Repro: `grep '"judge": "j3", "kind": "wrong"' evals/golden/judge_controls.jsonl`.
- Why it matters: gate item 4 now depends on J3 catching these. 1.000 reads as strong evidence and is weak evidence.
- Fix: restore the markerless pair as a `correct` item with expected `conflict`, following rule 2. Keep W1 with its markers. Add at least three same-fact, consistent-value pairs as `wrong` items with expected `benign`, phrased the way the generator could propose them. Record the change in the item's changelog, citing run 20261102T035750Z and the v1 verdict.
- Acceptance test: a unit test asserts that every J3 wrong item shares a fact name or topic across its two quotes, and that the markerless measure pair is `kind: correct, expected: conflict`. A judge that answers by rule 2 for the markerless pair and rule 3 for the marked pair passes both sides of the J3 control.

**F2 major. Ship-bar item 4 now gates on the J3/J4 controls without the ADR the spec requires.**
- Evidence: `spec/REQUIREMENTS.md:319` "## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)". `docs/CONTRACT.md:417` "adjust only with an ADR". `spec/REQUIREMENTS.md:328`, row 4 "Measured by", lists `unsupported_count_3run`, `hallucination_catch_rate`, `determinism_3run` and golden must_not, with no controls. `evals/run.py:683` `and controls_ok(m.get("judge_controls"))` and `evals/run.py:657-661` `controls_ok` (catch at least 0.95 and zero false agree). The only record is `board/cards/T-094.md:28`, an orchestrator note: "Seeded controls gating in ship-bar item 4 is accepted." `grep -n -i control memory/DECISIONS.md memory/ORCHESTRATOR_DECISIONS.md` finds no decision for it. T-093 AC 2 asks for catch rates in the report, not for a gate.
- Why it matters: the change is stricter, so it does not weaken the bar. Its intent fits item 4's judge-recall wording and R-TL-4 / R-CO-2. It does not follow the spec's change procedure, and the 0.95 and zero-false-agree thresholds on 5 and 8 items appear nowhere in the spec. The product note quotes these numbers.
- Fix: write an ORCHESTRATOR_DECISIONS entry that names the controls gate, its item counts and its rule. Update the spec §7 row 4 "Measured by" to include `judge_controls` with its numbers. Keep the gate or drop it, decided on the record.
- Acceptance test: `grep -n judge_controls spec/REQUIREMENTS.md` returns the row-4 line, and `memory/ORCHESTRATOR_DECISIONS.md` contains a D-entry that names the gate.

**F3 minor. The controls gate on one sample per item, all-or-nothing.**
- Evidence: `evals/run.py:657-661`, `ge_(catch_rate, 0.95)`. With 5 J3 wrong items, 0.95 means 5/5. With 8 J4 wrong items, it means 8/8. `judge_controls_metrics` (`evals/run.py:388-410`) calls each control once per live eval. The T-075 probe ran 2 repetitions per item. The live eval ran once.
- Why it matters: one sampling miss on one item fails item 4, and the failure looks like a model regression. The report does not show how often that happens.
- Fix: run the controls on the same three runs as R-CO-7 and gate on all three, or report per-item stability in the report.
- Acceptance test: a judge that flips one item on run 2 fails the gate, and the live report lists the per-item verdict for each run.

**F4 minor. A judge that rejects everything passes the control gate, and nothing ties that to flag recall in a test.**
- Evidence: `evals/run.py:391` says correct_accepted is "reported (over-rejection is safe, so it is not gated)". `controls_ok` (`evals/run.py:657-661`) reads only catch and false agree. `tests/unit/test_t093_eval_signature.py`, `test_a_judge_that_rejects_everything_catches_all_but_the_correct_accept_rate_shows_it`, asserts catch 1.0 and correct_accepted 0 and makes no ship_bar assertion. Over-rejection is caught only by item 3 (flag recall) on a live run, and no test connects the two.
- Fix: gate correct_accepted at the same 0.95 for J3 and J4, or record why not. Add a test that a reject-all judge leaves `ship_bar_met` False.
- Acceptance test: that test, green.

**F5 minor. The live 3_flags blocker is wider than the conflict flag described in the T-094 framing.**
- Evidence: `evals/reports/20261102T040933Z.md:5` "Blockers: 3_flags; 4_no_invented_facts". `:13` flag_precision[conflict] 0.800. `:15` flag_precision[causation] 0.857. The T-093 notes attribute causation 0.857 to an extra causation flag in case_01. `board/cards/T-094.md:28` scopes "model conflict/flag generation", so causation is probably covered, but the card's stated cause does not name it.
- Why it matters: the live bar has three independent failures (conflict precision, causation precision, determinism 0.5). A fix aimed only at the conflict flag would leave it red. This is outside T-093's AC.
- Fix: T-094's AC should name both flag precision failures and the determinism 0.5.
- Acceptance test: two consecutive live 3-runs with `blockers: []`, which is T-094's own AC.

**F6 minor. The controls share authors and rules with the prompts they test, and there is no held-out set.**
- Evidence: `app/llm/prompts/judge_flag_v2.md` changelog "(T-075, R-CO-7)". Its category rules are the same ones the J4 controls exercise. `evals/golden/judge_controls.jsonl:22` (J3C1) "Plan of care: 12 visits." / "Discharged from PT after two missed appointments." is the sample's own conflict, and rule 1 of `judge_conflict_v2.md` describes it. The T-075 probe ran 8 seeded J4 cases in the same failure modes before these controls existed.
- Why it matters: 8/8 and 5/5 show the prompts follow their own rules on rule-shaped items. They do not show that a new bogus flag will be caught.
- Fix: keep a held-out set written before the next prompt edit. Label the current controls as in-sample in the report.
- Acceptance test: the report labels the controls in-sample, and a held-out file exists whose changelog predates the prompt edit it tests.

**F7 nit. Test and guard gaps.**
- `tests/unit/test_t093_eval_signature.py` MUTATIONS covers additions and renames for entries, but not entry removal, gap `from`/`to`, amount `record_ids`, or entry `date_status`. The signature already covers them, so a test is cheap.
- Correct control items in `evals/golden/judge_controls.jsonl` have no `why` field. Add one, as the wrong items have.
- `evals/run.py` `_SECRET` matches three patterns. The allowlist in `run_artifact` is the real control, so keep the allowlist as it is and do not widen the artifact.

## What I exercised

- `python3 tools/board.py show T-093`; `python3 tools/board.py --help` (read only).
- `git show --stat e491cad`; `git show e491cad -- evals/run.py`; `git show e491cad -- tests/unit/test_eval_runner.py`.
- `git diff --stat e491cad -- evals/run.py tests/unit/test_t093_eval_signature.py tests/unit/test_eval_runner.py evals/golden/judge_controls.jsonl app/backend/judges.py app/backend/flags.py` (empty: working tree matches HEAD for these files).
- `.venv/bin/python -m pytest -q tests/unit/test_eval_runner.py` gives **64 passed**.
- `.venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py` gives **47 passed**; `--collect-only -k r_co_7` gives **29** field mutation tests.
- `env -u ENABLE_LIVE .venv/bin/python -m pytest -q tests/unit/test_eval_runner.py tests/unit/test_t093_eval_signature.py` gives **111 passed**, so the tests do not depend on the environment.
- Signature breaks in scratch copies: `git archive e491cad evals tests app spec` extracted to `artifacts/review-evidence/T-093-staff/`, with `mutate.py` applied to three copies. The copies were removed afterwards; `mutate.py` is kept as the reproduction.
  - m1, own record_ids dropped from the flag term: **1 failed** (`flags:record_ids`), 46 passed.
  - m2, totals dict replaced with `{}`: **3 failed** (`totals:existing_key`, `totals:new_key`, `test_the_signature_compares_the_whole_totals_dict_of_the_real_shape`), 44 passed.
  - m3, record split without the excerpt hash: **1 failed** (`record_split:excerpt_changed`), 46 passed.
- Real `run_case` output, sample case, fixture backend, via `R.load_pipeline()`: top-level and item keys checked against every key the signature reads. All exist; `detected_not_a_total` is absent.
- Artifacts: `ls evals/reports/runs/` gives `20261102T034706Z` and `20261102T035806Z`, each with run1-3, sample and 9 case files. `grep -rhoi -E 'sk-…|ANTHROPIC|PRIVATE KEY|api_?key|password|secret|token|prompt[a-z_]*|nonce|<record-|system[a-z_]*' evals/reports/runs/ | sort | uniq -c` gives **666 `prompt_version`** and **2 `prompt_injection`** (case name), and nothing else. Key set enumerated with a script; no prompt text or raw model output.
- `python3 tools/check_secrets.py` gives `check_secrets: ok (1424 file(s) scanned)`.
- Controls: read `evals/golden/judge_controls.jsonl` (26 items), `app/llm/prompts/judge_conflict_v2.md`, `app/llm/prompts/judge_flag_v2.md`, `app/llm/prompts/flags_v1.md`. Checked `app/backend/judges.py:24-38` `_run`: LLMFailed and invalid output map to `unavailable`, so judge failure is never positive.
- Live reports: `evals/reports/20261102T040933Z.md` lines 5, 13, 15, 19-22, 38-39; `evals/reports/latest.json` gives `ship_bar_met False`, blockers `['3_flags', '4_no_invented_facts']`, `run_artifacts` path.
- Spec and decisions: `spec/REQUIREMENTS.md:319, 328`; `docs/CONTRACT.md:417`; `memory/ORCHESTRATOR_DECISIONS.md` (latest D-045) and `memory/DECISIONS.md` searched for control or gate decisions; `board/cards/T-094.md:26-28`.
- Outside my lens: the clinical meaning of the seeded items; the UX of the report.

```json
{"card": "T-093", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e491cad (evals/run.py, tests/unit/test_t093_eval_signature.py, tests/unit/test_eval_runner.py, evals/golden/judge_controls.jsonl, evals/reports/runs/20261102T034706Z and 20261102T035806Z, evals/reports/20261102T035750Z.md and 20261102T040933Z.md, evals/reports/latest.json); no app URL; sample case; live reports read, not re-run",
 "exercised": [
  "python3 tools/board.py show T-093; python3 tools/board.py --help",
  "git show --stat e491cad; git show e491cad -- evals/run.py; git show e491cad -- tests/unit/test_eval_runner.py; git diff --stat e491cad over T-093 files (empty)",
  ".venv/bin/python -m pytest -q tests/unit/test_eval_runner.py -> 64 passed",
  ".venv/bin/python -m pytest -q tests/unit/test_t093_eval_signature.py -> 47 passed; --collect-only -k r_co_7 -> 29",
  "env -u ENABLE_LIVE .venv/bin/python -m pytest -q tests/unit/test_eval_runner.py tests/unit/test_t093_eval_signature.py -> 111 passed",
  "scratch copies from git archive e491cad (artifacts/review-evidence/T-093-staff/mutate.py): m1 flag own record_ids dropped -> 1 failed (flags:record_ids); m2 totals {} -> 3 failed (totals:existing_key, totals:new_key, whole-totals test); m3 record excerpt hash dropped -> 1 failed (record_split:excerpt_changed); copies removed",
  "real run_case keys (fixture, sample, via R.load_pipeline) checked against every signature key read; detected_not_a_total absent",
  "ls evals/reports/runs/*; grep -rhoi for secret and prompt tokens across runs -> 666 prompt_version, 2 prompt_injection (case name), nothing else; key set enumerated",
  "python3 tools/check_secrets.py -> ok (1424 file(s) scanned)",
  "read evals/golden/judge_controls.jsonl (26 items), app/llm/prompts/judge_conflict_v2.md, judge_flag_v2.md, flags_v1.md; app/backend/judges.py:24-38 _run",
  "read evals/reports/20261102T040933Z.md lines 5, 13, 15, 19-22, 38-39; evals/reports/latest.json (ship_bar_met False; blockers 3_flags, 4_no_invented_facts)",
  "read spec/REQUIREMENTS.md:319, 328; docs/CONTRACT.md:417; grep memory/DECISIONS.md and memory/ORCHESTRATOR_DECISIONS.md for control/gate decisions (none); board/cards/T-094.md:26-28"
 ],
 "verdict": "changes",
 "scores": {"r_co_7_field_coverage": 5, "mutation_sensitivity": 5, "per_run_artifacts_and_secrets": 5, "determinism_failure_diagnosability": 5, "j4_control_soundness": 4, "j3_control_soundness": 2, "gate_consistency_with_spec": 2, "test_hermeticity": 5},
 "findings": [
  {"severity": "major",
   "title": "J3 control set cannot separate rule-following from keyword matching; its one same-fact item was relabelled after it failed",
   "evidence": "evals/golden/judge_controls.jsonl:17 J3W1 excerpt_a 'Visit 1: neck pain 6/10, daily headaches.' excerpt_b 'Visit 9: neck pain 3/10, headaches weekly.' expected benign; why: v1 had no visit markers, J3 called it FACT_MISMATCH on run 20261102T035750Z, 'a labelling error'. app/llm/prompts/judge_conflict_v2.md rule 2 (FACT_MISMATCH, same fact, cannot both be accurate as written) vs rule 3 (benign: different visits/topics). W1 and W4 separated by visit words; W2 and W5 unrelated topics; W3 different medications; no same-fact consistent-value wrong item. Result 5/5 at evals/reports/20261102T040933Z.md:20. Repro: grep '\"judge\": \"j3\", \"kind\": \"wrong\"' evals/golden/judge_controls.jsonl",
   "why_it_matters": "Gate item 4 now depends on J3 catching these. The 1.000 measures keyword matching more than the rule the prompt states, and the expectation was changed by changing the input after a failure.",
   "fix": "Restore the markerless pair as kind correct, expected conflict (rule 2). Keep W1 with markers. Add at least three same-fact, consistent-value wrong items expected benign. Changelog the change, citing run 20261102T035750Z and the v1 verdict.",
   "acceptance_test": "Unit test: every J3 wrong item shares a fact name or topic across its two quotes; the markerless measure pair is kind correct, expected conflict; a rule-2 judge passes the markerless pair and a rule-3 judge passes the marked pair."},
  {"severity": "major",
   "title": "Ship-bar item 4 gates on J3/J4 controls without the ADR the spec requires",
   "evidence": "spec/REQUIREMENTS.md:319 '## 7. Ship bar (mirrors CONTRACT §8.2; change only with an ADR)'; docs/CONTRACT.md:417 'adjust only with an ADR'; spec/REQUIREMENTS.md:328 row 4 Measured by omits controls; evals/run.py:683 'and controls_ok(m.get(\"judge_controls\"))'; evals/run.py:657-661 controls_ok; only record board/cards/T-094.md:28 'Seeded controls gating in ship-bar item 4 is accepted.'; no decision in memory/DECISIONS.md or memory/ORCHESTRATOR_DECISIONS.md",
   "why_it_matters": "Stricter, so not weakening, and the intent matches item 4 judge recall and R-TL-4 / R-CO-2. But the spec's change procedure was not followed, and the 0.95 and zero-false-agree thresholds on 5 and 8 items appear nowhere in the spec.",
   "fix": "Write an ORCHESTRATOR_DECISIONS entry naming the controls gate, its item counts and rule. Update spec §7 row 4 Measured by to include judge_controls with its numbers. Keep or drop the gate on the record.",
   "acceptance_test": "grep -n judge_controls spec/REQUIREMENTS.md returns the row-4 line; memory/ORCHESTRATOR_DECISIONS.md has a D-entry naming the gate."},
  {"severity": "minor",
   "title": "Controls gate on one sample per item, all-or-nothing",
   "evidence": "evals/run.py:657-661 ge_(catch_rate, 0.95): 5/5 for J3, 8/8 for J4. judge_controls_metrics (evals/run.py:388-410) calls each control once per live eval; T-075 probe ran 2 reps per item.",
   "why_it_matters": "One sampling miss fails item 4 and looks like a model regression; frequency unknown.",
   "fix": "Run controls on the same three runs as R-CO-7 and gate on all three, or report per-item stability.",
   "acceptance_test": "A judge that flips one item on run 2 fails the gate; the live report lists per-item verdicts per run."},
  {"severity": "minor",
   "title": "A reject-everything judge passes the control gate; no test ties over-rejection to flag recall",
   "evidence": "evals/run.py:391 'correct_accepted is reported (over-rejection is safe, so it is not gated)'; controls_ok (evals/run.py:657-661) reads catch and false agree only; tests/unit/test_t093_eval_signature.py test_a_judge_that_rejects_everything... asserts catch 1.0 and correct_accepted 0 with no ship_bar assertion.",
   "why_it_matters": "Over-rejection is caught only by item 3 flag_recall on a live run, and no test connects the two.",
   "fix": "Gate correct_accepted at 0.95 for J3 and J4, or record why not. Add a test that a reject-all judge leaves ship_bar_met False.",
   "acceptance_test": "That test is green."},
  {"severity": "minor",
   "title": "Live 3_flags blocker is wider than the conflict flag in the T-094 framing",
   "evidence": "evals/reports/20261102T040933Z.md:5 'Blockers: 3_flags; 4_no_invented_facts'; :13 flag_precision[conflict] 0.800; :15 flag_precision[causation] 0.857; board/cards/T-094.md:28 scopes 'model conflict/flag generation'.",
   "why_it_matters": "Three independent live failures (conflict precision, causation precision, determinism 0.5). A conflict-only fix leaves the bar red. Outside T-093's AC.",
   "fix": "T-094 AC names both flag precision failures and the determinism 0.5.",
   "acceptance_test": "Two consecutive live 3-runs with blockers []."},
  {"severity": "minor",
   "title": "Controls share authors and rules with the prompts they test; no held-out set",
   "evidence": "app/llm/prompts/judge_flag_v2.md changelog '(T-075, R-CO-7)'; evals/golden/judge_controls.jsonl:22 J3C1 is the sample's own plan-vs-discharge conflict, rule 1 of judge_conflict_v2.md; T-075 probe ran 8 seeded J4 cases in the same failure modes before the controls existed.",
   "why_it_matters": "8/8 and 5/5 show the prompts follow their own rules on rule-shaped items, not that a new bogus flag will be caught.",
   "fix": "Keep a held-out set written before the next prompt edit; label current controls in-sample in the report.",
   "acceptance_test": "Report labels the controls in-sample; a held-out file predates the prompt edit it tests."},
  {"severity": "nit",
   "title": "Mutation and control coverage gaps; guard is pattern-based",
   "evidence": "tests/unit/test_t093_eval_signature.py MUTATIONS has no entry removal, gap from/to, amount record_ids, or entry date_status mutation; evals/golden/judge_controls.jsonl correct rows have no why field; evals/run.py _SECRET matches three patterns (the run_artifact allowlist is the real control).",
   "why_it_matters": "Cheap coverage gaps; not a defect in the signature.",
   "fix": "Add the four mutations; add why to correct control items; keep the allowlist and do not widen the artifact.",
   "acceptance_test": "Four new parametrized cases red on a signature that drops each term."}
 ],
 "whats_right": [
  "Signature keys are real run_case keys (checked against a fixture run); detected_not_a_total is gone and a test keeps it gone.",
  "Per-run artifacts are allowlisted (items, states, judge verdict and reason codes, prompt version ids, summary hashes); the scan found only prompt_version ids and a case name, and the live report names the differing flag.",
  "J4 controls pair the same quote under two categories (C2/C6, C3/W3, C7/W7), testing category selection and not only the quote."
 ],
 "questions_for_chris": [
  "This review ran as claude-haiku-5-5 per the invocation; CLAUDE.md §6 puts engineering reviewers on Sonnet. Accept this review, or re-run on Sonnet?",
  "Should the J3/J4 controls count toward ship-bar item 4 at all until the ADR in F2 is written, given the spec's judge-recall wording covers only the hallucination set?"
 ]}
```
