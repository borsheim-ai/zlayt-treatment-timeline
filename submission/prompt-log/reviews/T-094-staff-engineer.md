# T-094 review: staff-engineer-reviewer (card commit a9a27ed)

Verdict: **fail**. One blocker, two majors, two minors. Every code citation is `a9a27ed` content, read with `git show a9a27ed:...` or from a `git archive a9a27ed` export in my scratchpad. HEAD moved during the review (a9a27ed -> 2ab7896); the later commits bf0c748 (docs), 9217f8a (controls) and 2ab7896 (controls evidence) are cited only where I say so.

Exercised: `git archive a9a27ed` export, `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit` = **2202 passed, 4 skipped** (157 s); 22-case probe of `conflict_candidates` (script in scratchpad `probe.py`); end-to-end probe of a suppressed flag through `run_pipeline` plus `present.case_view` and every DB table (`probe2.py`); audit-prompt probe over all 6 steps (`probe3.py`); D-050 translated probe (`probe4.py`); three scratch mutants (list in section 4); both live reports and their per-run artifacts; the three controls reports. I did not rerun the live eval (nothing looked off in the artifacts).

## 1. Check 1: candidates by code, arithmetic by code, model classifies only

True as built. `conflict_candidates.py` imports no `app.llm` module, multiplies frequency by duration in code (`per * weeks`), and `run_conflict_pass` only calls `judges.run_j3_meta` per candidate. 22-case probe (candidate list printed per case):

| Case | Result |
|---|---|
| "PT 2x/week for 6 weeks" + "Plan of care: 12 visits" + "Completed all 12 visits" | no candidate (right) |
| plan 12 visits, then "Discharged ... after two missed appointments" | 1 plan_vs_outcome (right) |
| "3 times per week for 4 weeks" then "no-show ... stopped attending" | 1 candidate, plan = 12 (right) |
| "denies prior neck problems" vs "seeing a chiropractor for neck pain since 2024"; "No history of back injury" vs "Prior lumbar surgery"; "denies any previous injury to the shoulder" vs "History of prior shoulder dislocation" | 1 history_denial each (right) |
| "Patient missed 3 visits" with no plan; missed visits dated before the plan; "Missing 3 days of work" with a plan; two undated records | none, none, none, 1 by record order (right) |
| "cancelled remaining appointments", "Discontinued therapy due to cost" | candidate (right) |
| "Twelve visits authorized" + "did not attend"; "PT x 12 visits recommended" + "Discontinued" | **no candidate** |
| "lost to follow-up; left therapy against advice"; "stopped going to PT" | **no candidate** |
| "No previous accidents reported" vs "prior car accident in 2020"; "twice-weekly for six weeks" + "Self-discharged" | **no candidate** |
| "Attended all visits with no missed appointments" after a 12-visit plan | **candidate** (false positive, J3 must say benign) |
| plan and "missed two appointments" in the same record | none |

The misses are finding F-2; the false positive is F-5. The unit tests in `tests/unit/test_conflict_candidates.py` are behavioural; mutant `per * weeks -> per + weeks` fails 2 of them.

## 2. Check 2: suppressed flags. Not honest product behaviour; it should be the could-not-verify tray (F-1)

`flags.py:292-293` sets `_suppressed` when J4 says `disagree` on a model-only flag; `pipeline.py:357-359` moves it into `suppressed_flags` and drops it from `llm_flags`. I followed that list: `api.py:339` calls `mod.run_pipeline(...)` and discards the return value; `present.case_view` has no field for it; and after a pipeline run with a suppressed `alternative_cause` flag, **no table in the case DB mentions it** (`flags` 10 rows, none `alternative_cause`; `llm_calls` 0 rows in the fake run) and the case view contains no `suppress` and no `alternative_cause`. So the list exists only in the in-memory return value of one function. No UI, no API, no DB, no eval report. The audit log keeps the J4 call in production (`make_call` writes `llm_calls`), but nothing links it to "this flag was hidden".

The card's own handoff gives the reason: "a rejected tray item still counts against eval precision ... only suppression fixes precision". That is a product behaviour changed to raise a metric. The correct fix is in the scorer (`pipeline.case_view` line 399 merges `out["tray"]` flags into `flags`, so rejected tray flags are scored as emitted), not in what the paralegal can see.

## 3. Checks 3 to 5

**3. Live reports are genuine.** `evals/reports/20261102T060623Z.md` and `20261102T062420Z.md`: backend `claude-cli`, models sonnet-5-5 / haiku-5-5. Per-run artifacts exist at `runs/20261102T054926Z` and `runs/20261102T060623Z` (the run dir is the start time; each holds run1-3.json, sample.json and the nine case files). Each run: backend claude-cli, status done, errors `[]`, 23 items. I recomputed: `signature_parts` (keys amounts, entries, entry_ids, flags, gap_flags, parsed_dates, record_split, totals, tray) is byte-identical in all three runs of both reports (sha256 prefix 39c2482715). The conflict item in run1 is `f_cx1`, `origin: code`, judge `judge_conflict_v4`, so the artifacts do come from the new code. Caveat F-3: the reports do not name a source commit or tree state for the evaluated code.

**4. Audit prompt versions match.** Probe over a full sample run (with a model-only flag so J4 fires): for `extract, j1, j2, j3, j4, flags` the system text sent equals `promptlib.load(PROMPT_OF_STEP[step]).text` and the id is `extract_v1, judge_faithfulness_v1, judge_amount_class_v1, judge_conflict_v4, judge_flag_v2, flags_v1`. `PROMPT_OF_STEP` has no `conflicts` key. Mutant `judges.py` j4 -> `judge_flag_v1` fails `test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names` and one more. The T-093 r2 blocker is fixed.

**5. J3W11 holds.** `benign / benign / benign` in both live reports and in controls-20261102T045207Z; the control text is unchanged since T-093 r2 ("Plan of care: 12 visits." vs "Completed all 12 planned visits; discharged with goals met."), the fix is in the prompt (v4 rule 1), not the label. Also verified: the D-050 translated hunk works (`es` and `uncertain` records give `needs_review` with `AI_TRANSLATION`, `en` gives `verified`).

## 4. Mutants run (scratch copies, nothing committed)

| Mutant | Result |
|---|---|
| `per * weeks -> per + weeks` in conflict_candidates | 2 tests fail (red) |
| remove the J4 suppression branch | `test_model_only_flag_rejected_by_j4_is_suppressed_and_listed` fails (red) |
| j4 prompt id -> `judge_flag_v1` in judges.py | 2 tests fail (red) |

## Findings

- **F-1 (blocker).** A model-only flag that J4 rejects is deleted from everything the paralegal or API can reach, contrary to R-FL-3 and the ladder.
- **F-2 (major).** With the open model search gone, conflict recall is now limited to two regex rules with silent misses, and the narrowing is not recorded as a scope cut.
- **F-3 (major).** The T-094 evidence cannot be tied to `a9a27ed`, ran against a controls set that was replaced three minutes later, and a clean rerun of the same prompts fails the controls gate on the judge that now decides suppression.
- **F-4 (minor).** J3 benign on a code pair that is really a no-op ("no missed appointments") fills the tray with noise because `_ENDED` has no negation handling.
- **F-5 (minor).** `suppressed_flags` and a J3C6 flip are not in any report or signature; a suppression flap would be invisible to R-CO-7.

```json
{"card": "T-094", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "a9a27ed (git archive export; HEAD moved to 2ab7896 during review); app/backend/conflict_candidates.py, flags.py, pipeline.py, judges.py, app/llm/audited.py, app/llm/prompts/judge_conflict_v4.md, tests/unit/test_conflict_candidates.py; evals/reports/20261102T060623Z.md, 20261102T062420Z.md, controls-20261102T045207Z.md, runs/20261102T054926Z, runs/20261102T060623Z; sample case",
 "exercised": [
  "git archive a9a27ed; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit = 2202 passed, 4 skipped",
  "22-case probe of conflict_candidates.candidates()/plans() (consistent plan, early end, denial vs prior, missed-visit count, odd phrasings)",
  "run_pipeline with a model-only alternative_cause flag and J4 disagree, then present.case_view and a scan of every DB table for the flag",
  "read app/backend/api.py _run_thread (return value of run_pipeline discarded) and pipeline.case_view",
  "compared system text sent per step with PROMPT_OF_STEP over a full sample run (extract, j1, j2, j3, j4, flags)",
  "D-050 translated probe: run_conflict_pass with lang es/uncertain/en records",
  "three scratch mutants (arithmetic, suppression branch, j4 prompt id)",
  "read both live reports, recomputed signature_parts equality over 6 run artifacts, checked backend/models/status/errors per run",
  "read controls-20261102T045207Z.md and controls-20261102T063331Z.md, judge_controls.CHANGELOG.md, R-FL-2, R-FL-3, R-CO-7, D-046, LLM_VS_CODE rows 11 and the ladder, SCOPE_CUTS at a9a27ed"
 ],
 "verdict": "fail",
 "scores": {"determinism_and_code_boundary": 4, "failure_visibility": 1, "evidence_reproducibility": 2, "test_quality": 4, "spec_conformance": 2},
 "findings": [
  {"severity": "blocker",
   "title": "A model-only flag that J4 rejects is suppressed: no UI, API, DB or report shows it (R-FL-3, ladder, metric-driven)",
   "evidence": "app/backend/flags.py:292-293 (`elif step == \"j4\" and v == \"disagree\" and f.get(\"origin\") == \"llm\": f[\"_suppressed\"] = True`); app/backend/pipeline.py:357-359 builds `suppressed_flags` then filters them out; app/backend/api.py:339 `mod.run_pipeline(c, token, raw, call=make_call(c, token), now=time.time)` discards the result; repro: scratchpad probe2.py runs the sample with a model-only `alternative_cause` flag and J4 disagree -> out['suppressed_flags'] has 1 entry, present.case_view contains no 'suppress' and no 'alternative_cause', no case DB table mentions it; `grep -rn suppressed app evals tests` finds only flags.py, pipeline.py and tests/unit/test_pipeline.py; no eval report or run artifact contains the word. Spec: spec/REQUIREMENTS.md R-FL-3 'if only one fires, the flag is needs_review (LEXICON_ONLY or LLM_ONLY)'; docs/LLM_VS_CODE.md ladder line 62 'partially / unsupported / disagrees / unsure / unavailable -> NEEDS_REVIEW (with reason)'. Motive in the card handoff: 'a rejected tray item still counts against eval precision ... only suppression fixes precision'.",
   "why_it_matters": "Two models disagree (Sonnet proposed it, Haiku rejected it) and the paralegal never learns the flag existed. That is a silent drop of a model-found item chosen to raise a precision number, not a product decision: it also hides the case where the judge is wrong, and J4 has just been shown to flap (F-3). The could-not-verify tray exists for exactly this: visible, labelled, never exported. No D-number or ADR authorizes the change; LLM_VS_CODE only documents it afterwards.",
   "fix": "Answer to question 2: it should be the could-not-verify tray (state rejected, reason JUDGE_DISAGREES), same as the J3 benign path. Remove `_suppressed` and `suppressed_flags`. Fix the precision problem in the scorer instead: score only flags whose state is not `rejected` (pipeline.case_view merges out['tray'] into flags at line 399; evals/run.py already declines to score rejected items in the calibration table), record it as an ADR/D-number because spec §7 bar 3 changes meaning, and rerun the live evals. If suppression is kept by decision, then at minimum persist each suppressed flag with its excerpt and J4 answer, show it in the UI and API, and print the suppressed count per run in the eval report and the determinism signature.",
   "acceptance_test": "tests/unit/test_pipeline.py: with a model-only flag and J4 disagree, the flag appears in out['tray'] with reasons[0] == 'JUDGE_DISAGREES' and in the GET case view tray; `suppressed_flags` no longer exists (or, if kept, is stored and returned by the API and counted in the eval report). An eval-scorer test: a rejected tray flag does not lower flag_precision, and a verified wrong flag does."},
  {"severity": "major",
   "title": "Conflict recall is limited to two regex rules with silent misses and no scope-cut row",
   "evidence": "Probe (scratchpad probe.py, python -I against the a9a27ed export): no candidate for 'Twelve visits authorized' + 'did not attend' (_COUNT needs digits, conflict_candidates.py:21-23); 'PT x 12 visits recommended' + 'Discontinued therapy due to cost' (plan keyword list); 'Patient lost to follow-up; left therapy against advice' and 'Patient stopped going to PT' (_ENDED list, lines 28-30); 'No previous accidents reported' vs 'prior car accident in 2020' (prior categories are only pre_existing/prior_surgery); 'twice-weekly for six weeks' (_FREQ week count is digits only). Dosage and laterality across records: 'not built' per the card handoff. memory/SCOPE_CUTS.md at a9a27ed: `git show a9a27ed:memory/SCOPE_CUTS.md | grep -i 'conflict\\|laterality\\|dosage'` returns nothing; no D-number in ORCHESTRATOR_DECISIONS for T-094. Spec: R-FL-2 'Flag facts that conflict across records, citing both excerpts.'",
   "why_it_matters": "Before this commit the model could find any cross-record contradiction; now a conflict outside two phrase patterns is never raised and there is no model backstop, no tray entry, no warning. Golden recall of 1.0 covers only the sample's own phrasing. CONTRACT.md:474 says silent scope cuts are penalized; this is a recall cut that is documented only in a later architect doc (bf0c748).",
   "fix": "Add a SCOPE_CUTS row (what: conflicts beyond plan-vs-early-end and denial-vs-prior; why: R-CO-7; cost to add: dosage/laterality/date candidate rules) and a D-number for the code-proposed design. Widen the cheap holes in code with tests: number words in _COUNT and _FREQ, 'lost to follow-up', 'left therapy', 'stopped going', 'No previous <noun>' denials against prior events. Show a one-line note in the flags panel or product note that conflict detection is rule-based.",
   "acceptance_test": "tests/unit/test_conflict_candidates.py gains the six missed phrasings above, each asserting one candidate (or a documented non-goal), and SCOPE_CUTS.md has a row naming dosage and laterality conflicts; `board.py validate` and the scope-cuts check pass."},
  {"severity": "major",
   "title": "AC 1 evidence is not tied to a9a27ed, used a controls set replaced three minutes later, and a clean rerun of the same prompts fails the controls gate",
   "evidence": "evals/reports/20261102T060623Z.md and 20261102T062420Z.md carry no source commit or tree state for the run itself; the only commit string is the calibration section ('source commit bcdcb919f1' and '1526a1fa04'), both earlier than a9a27ed (the code under test was uncommitted when evaluated; the card note says it committed 'from a temp index'). Both reports show J3 '19/19' wrong items including J3W10 and J3C6 (arithmetic pair); `git log` shows 9217f8a (00:33:15, three minutes after a9a27ed at 00:30:09, not its ancestor) removed those items because they make the judge multiply (judge_controls.CHANGELOG.md round 3). Then evals/reports/controls-20261102T063331Z.md (committed in 2ab7896, 'Source commit 9217f8af56, tree clean', same judge_flag_v2 hash 7b6b3471...): `controls_ok: False`, J4 '11/12 wrong caught', `J4W7 | wrong | disagree | agree / disagree / disagree | NO`. In report 20261102T062420Z the correct item J3C6 reads `conflict / benign / conflict | NO` (unstable).",
   "why_it_matters": "The card exists to stop the live ship-bar flap. Under the D-046 gate as it stands at HEAD, the controls leg of item 4 fails on a clean tree, so the bar still flaps; the two green reports measure a different control set and cannot be reproduced from the commit. A J4 false agree on a seeded wrong flag is also exactly what the suppression rule trusts the other way round: J4 'disagree' decides who is hidden.",
   "fix": "Rerun the two consecutive live 3-run evals and the controls from a clean worktree of the fix commit, with the report naming the source commit and 'tree clean' (the controls report already does this since 9217f8a; make the eval report do the same). Decide J4W7: either the prompt changes (new version, rerun) or the control is judged by the second-agent relabel rule; do not accept 'unstable, not gated'.",
   "acceptance_test": "Two consecutive evals/reports/<ts>.md whose header names `Source commit <sha>, tree clean`, ship_bar_met true, and a controls report from the same sha with controls_ok true and unstable [] for J4; `grep 'Source commit' evals/reports/<ts>.md` returns the commit that holds the fix."},
  {"severity": "minor",
   "title": "_ENDED has no negation handling, so completed courses produce a tray candidate",
   "evidence": "conflict_candidates.py:28-30. Probe: 'Plan of care: 12 visits.' then 'Attended all visits with no missed appointments.' -> candidate plan_vs_outcome (records 1, 2). J3 should answer benign and the pair lands in the tray as JUDGE_DISAGREES.",
   "why_it_matters": "A clean course shows up in the could-not-verify tray every time, which trains the paralegal to ignore the tray, and one J3 flip turns it into a verified conflict flag.",
   "fix": "Skip an outcome unit when `no|without|zero` precedes the matched phrase (same unit), with a test; leave the judge as the second check.",
   "acceptance_test": "tests/unit/test_conflict_candidates.py: 'Attended all visits with no missed appointments.' after a 12-visit plan yields []."},
  {"severity": "minor",
   "title": "Neither the determinism signature nor the report records suppressed_flags or a per-run suppressed count",
   "evidence": "No match for 'suppress' in evals/*.py, evals/reports/20261102T060623Z.md, 20261102T062420Z.md or any file under evals/reports/runs/20261102T054926Z and 20261102T060623Z (grep -c). signature_parts keys: amounts, entries, entry_ids, flags, gap_flags, parsed_dates, record_split, totals, tray.",
   "why_it_matters": "If J4 disagrees on a flag in run 1 and says unsure in run 2, the flag appears in one run and the difference is caught; if it disagrees in all runs the report never says it was dropped, so the card's claim that case_01's `alternative_cause` flag was suppressed cannot be checked from any artifact.",
   "fix": "If F-1 is resolved by the tray, nothing more is needed (the item is in `tray` in the signature). If suppression stays, add suppressed_flags to the per-run artifact and signature, and print the count in the report.",
   "acceptance_test": "A run artifact for a case with a suppressed flag lists it; a test shows determinism_3run falls below 1.0 when the suppressed set differs between runs."}
 ],
 "whats_right": [
  "conflict_candidates.py is pure code with no app.llm import, arithmetic (frequency x duration) done in code, and a fixed candidate order; mutants on the arithmetic are caught by tests.",
  "Audit prompt ids now equal the text sent for extract, j1, j2, j3, j4 and flags, and a test goes red when they drift (the T-093 r2 blocker is closed).",
  "Both live reports are real claude-cli runs with per-run artifacts; signature_parts is identical across all three runs of each, and the conflict item in the artifacts is the code-proposed f_cx1 judged by judge_conflict_v4."
 ],
 "questions_for_chris": [
  "Is a model-found flag that the second model rejects something the paralegal should see (tray) or something the product may drop? I rated the drop a blocker because R-FL-3 says needs_review; if you want it dropped, it needs a D-number and a visible count."
 ]}
```
