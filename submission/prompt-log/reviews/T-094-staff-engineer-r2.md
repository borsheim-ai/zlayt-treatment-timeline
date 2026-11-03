# T-094 round 2: staff-engineer-reviewer (commits dda614d, 8b54d40, 789cb39; evidence 62037fc; read at HEAD f187a30)

Verdict: **pass**. The round-1 blocker (F-1, model-only flags dropped) and both majors (F-2 recall holes with no scope-cut row, F-3 evidence not tied to a commit) are fixed and each fix is pinned by a test that goes red under a scratch mutant. Two findings remain: one minor (a D-032 filter drops some model proposals before the tray, which D-053's wording does not admit) and one nit (duplicate SCOPE_CUTS row number). Everything below is read from a `git archive HEAD` copy in my scratchpad (`.../scratchpad/t094r2/tree`), HEAD = `f187a307e44fca87a9e09c834d51081c8ae33535`, except where I name a report file.

Exercised: `git archive HEAD` export; `.venv/bin/python -m pytest -q -p no:cacheprovider tests/unit` = **2415 passed, 4 skipped** in 159 s (skips: tesseract missing x2-ish, no `.git` in the export, no generated calibration.json; all environmental); fixture-backend CLI `LLM_BACKEND=fixture python -m app.pipeline evals/golden/sample.txt` run twice (45 lines each, `cmp` identical, status done, conflict flag `[verified]` so the v5 fixture was hit); probe of the six round-1 phrasings plus 5 controls (`probes/p1.py`); probe of model-only `scene_facts` / `objective_negative` through `flags.merge` (`probes/p2.py`); four scratch mutants; read of `flags.py`, `pipeline.py`, `present.py`, `evals/run.py`, `conflict_candidates.py`, `judges.py`, `audited.py`, `memory/SCOPE_CUTS.md`, D-053, D-054, the card AC/handoff, `T-112`; both passing reports `20261102T083252Z.md` and `20261102T085207Z.md`, the failing `20261102T081339Z.md`, `controls-20261102T075238Z.md`, and run artifacts `runs/20261102T081339Z` and `runs/20261102T083312Z`.

## Check by check

**1. Rejected model output goes to the tray, nothing suppressed.** True. `flags.py:286-293` routes a J3-benign code candidate and a J4-disagree model-only flag through `_to_tray(f, "JUDGE_DISAGREES", reason)`; `flags.py:307-311` sends a model-proposed conflict to the tray as `LLM_ONLY`. `pipeline.py:359` keeps rejected flags in `tray`, `present.py:223-230` serves them as tray items of kind `flag` (id, record_ids, reasons, why, attempt excerpt, never in `flags` or the review queue). `grep -rn "suppressed_flags\|_suppressed" app evals tests` finds only the test that asserts `"suppressed_flags" not in out`. Judge `unsure` or unavailable keeps the flag visible (tested). Live: `runs/20261102T083312Z/case_01_date_formats.json` has the `alternative_cause` flag, origin llm, `reasons: [JUDGE_DISAGREES, LLM_ONLY]`, state rejected, `tray_flag_count 1`, and the report line "flag tray ... 1 {"JUDGE_DISAGREES": 1} by case {"case_01_date_formats": 1}". Mutants: (m1) remove the J4-disagree tray branch -> `test_model_only_flag_rejected_by_j4_goes_to_the_tray_with_the_judges_reason` red; (m3) model conflict no longer trayed -> `test_a_model_proposed_conflict_that_no_code_candidate_made_goes_to_the_tray` red. The grep for other drops is finding F-1 below.

**2. Eval scores emitted flags only, tray counts reported, signature rule stated.** True. `evals/run.py:197-204` `to_candidates` skips `state == rejected`; `tray_flags()` (line 190) feeds `flag_tray` (line 801) and the report line; `signature_parts` (lines 653-654) states in a comment that R-CO-7's flag signature covers emitted flags and that a flag flipping between tray and list still changes the signature (the `tray` and `flags` keys). Mutant (m2) letting rejected flags back into candidates -> `test_a_tray_flag_does_not_lower_precision_but_a_wrong_emitted_flag_does` red. Round-1 F-5 (signature blind to suppression) is closed: the tray is in the signature.

**3. Six probe phrasings give candidates; SCOPE_CUTS lists the rest.** True. `probes/p1.py`: "Twelve visits authorized" + "did not attend", "PT x 12 visits recommended" + "Discontinued", "lost to follow-up; left therapy against advice", "stopped going to PT", "No previous accidents reported" vs "prior car accident in 2020", "twice-weekly for six weeks" + "Self-discharged" each give one candidate. Controls stay quiet: consistent 2x/week x 6 plan with "Completed all 12 visits", "missing 3 days of work", and the round-1 false positive "Attended all visits with no missed appointments" now gives `[]`. `memory/SCOPE_CUTS.md:66` lists dosage, laterality, date/provider conflicts beyond the code rules, month durations, a plan with no count, free-wording contradictions, and says a model-proposed conflict goes to the tray. Number collision: F-2.

**4. Fixtures and audit prompt ids.** `app/llm/prompts/judge_flag_v3.md` and `judge_conflict_v5.md` exist; `judges.py:59,64` send them; `audited.py:123-124` `PROMPT_OF_STEP` names j3 `judge_conflict_v5`, j4 `judge_flag_v3`. dda614d added 70 and 8b54d40 added 2 fixture files; the fixture-backend CLI hits them (no fixture miss, conflict `[verified]`). Mutant (m4) j4 sends `judge_flag_v2` -> `test_judge_prompt_sent_is_the_prompt_version_the_audit_record_names` and `test_audit_prompt_ids_equal_the_ids_judges_py_sends` red. Run artifacts list `judge_conflict_v5` and `judge_flag_v3` as the judge prompt versions on all items in both passing runs.

**5. Provenance.** `20261102T083252Z.md`, `20261102T085207Z.md` and `controls-20261102T075238Z.md` each carry "Source commit `789cb39cad9fa38e6761c6336c2edd800d3805d2`, tree clean", `ship_bar_met True` / `controls_ok True` (J3 17/17, J4 12/12 including J4W7, false agree 0, unstable [] for both), backend claude-cli, models sonnet-5-5 / haiku-5-5. Run artifacts (`runs/20261102T081339Z`, `runs/20261102T083312Z`): per run backend claude-cli, status done, errors [], 23 items, `signature_parts` sha256 prefix `39c2482715` in all three runs of both. The failing report `20261102T081339Z.md` (same commit, `ship_bar_met False`, `golden_must_not_hits 1`, case_02 `unsupported_summaries 1`, entry_recall 0.965) is committed, not hidden. `git_source` change in 789cb39 (`evals/run.py:86`) excludes `evals/reports` from the dirty check only for tracked files; untracked inputs are still checked (line 87).

## The case_02 flap and D-054 routing to T-112

I agree with routing it to T-112. The cause (the extract step writes a summary using sentences outside its own excerpt, and J1 correctly says unsupported) is in the generator stage, independent of D-053's tray and the conflict candidates; D-054's fix is deterministic code on that stage; holding T-094 would block a correct D-053 fix behind an unrelated one. Two conditions I would keep: (a) the T-094 close note must say that the card's title symptom (case_02 must_not and recall 0.965) was seen again on commit 789cb39 in `20261102T081339Z.md` and is owned by T-112, so the board does not read it as "flap fixed"; AC 1 is met literally (two consecutive passes) but on this commit the observed sequence is fail, pass, pass; (b) T-112 AC 2 already asks for three consecutive live 3-runs from a clean HEAD, which is the right bar given a roughly 1-in-3 flap (two consecutive passes happen about 44% of the time by chance). D-054 itself is a doc at HEAD; no code for it exists yet, so nothing in this review depends on it.

## Findings

- **F-1 (minor).** Model proposals dropped by code before the judge, outside D-053's wording (D-032 filters).
- **F-2 (nit).** SCOPE_CUTS has two rows numbered 13.
- **F-3 (nit).** "Negation-aware" in SCOPE_CUTS row 13 covers only no/without/zero/never; "not lost to follow-up" yields a (harmless) candidate.

```json
{"card": "T-094", "persona": "staff-engineer-reviewer", "model": "claude-sonnet-5-5",
 "scope": "round 2: commits dda614d, 8b54d40, 789cb39, evidence 62037fc, read at HEAD f187a30 via git archive in scratchpad; app/backend/flags.py, pipeline.py, present.py, conflict_candidates.py, judges.py, app/llm/audited.py, evals/run.py, memory/SCOPE_CUTS.md; evals/reports 20261102T083252Z.md, 20261102T085207Z.md, 20261102T081339Z.md, controls-20261102T075238Z.md; sample case",
 "exercised": [
  "git archive HEAD (f187a307e44f) into scratchpad; .venv/bin/python -m pytest -q -p no:cacheprovider tests/unit = 2415 passed, 4 skipped",
  "fixture-backend CLI python -m app.pipeline evals/golden/sample.txt twice, cmp identical, conflict flag verified",
  "probes/p1.py: six round-1 phrasings and five controls through conflict_candidates.candidates",
  "probes/p2.py: model-only scene_facts and objective_negative through flags.merge",
  "four scratch mutants: J4-disagree tray branch removed, scorer admits rejected flags, model conflict not trayed, j4 sends judge_flag_v2; each red",
  "grep for suppressed_flags/_suppressed, continue/pop/filter/drop paths in flags.py and pipeline.py",
  "read the two passing live reports, the failing 081339Z report, the controls report, run1-3 signature_parts and prompt versions for runs/20261102T081339Z and runs/20261102T083312Z, case_01 tray flag artifact",
  "read D-032, D-053, D-054, card T-094 AC/handoff and card T-112"],
 "verdict": "pass",
 "scores": {"determinism_and_code_boundary": 5, "failure_visibility": 4, "evidence_reproducibility": 5, "test_quality": 5, "spec_conformance": 4},
 "findings": [
  {"severity": "minor",
   "title": "Some model proposals are dropped by code before any judge or tray, which D-053's 'nothing is silently dropped' does not admit",
   "evidence": "app/backend/flags.py:16-17 `_CONTEXT_ONLY = (\"objective_negative\",)`, `_NEEDS_LEXICON = (\"scene_facts\",)`; flags.py:118-119 `if lf.get(\"category\") in _CONTEXT_ONLY: continue`; flags.py:154-155 `if i in used or lf.get(\"category\") in _NEEDS_LEXICON: continue`; flags.py:202 `if f.type in _PER_RECORD_TYPES` (a model flag of any other type is filtered at parse). Repro: .venv/bin/python -I probes/p2.py <tree> -> `scene_facts model-only -> []` and `objective_negative model-only -> []`; no tray item, no count in the run artifact or report. memory/ORCHESTRATOR_DECISIONS.md D-053: 'Nothing the model proposes is silently dropped ... A model-only flag or conflict that the judge rejects, or that no code candidate confirms, goes to the could-not-verify tray'. The drops are authorised by D-032 (first-eval precision 0.5 from these categories), so this is a wording and visibility gap, not a hidden behaviour.",
   "why_it_matters": "Round 1 was failed for exactly this shape (model output that exists nowhere the paralegal or an auditor can see). D-032 is a deliberate rule and I do not ask for it to be reversed, but D-053 states a universal and the code has three exceptions with no trace; a later reader of D-053 will believe it, and a model that starts over-proposing scene_facts would be invisible.",
   "fix": "Either add one sentence to D-053 and docs/LLM_VS_CODE.md naming the three code filters as the only pre-judge drops (D-032 categories, record-level types), or count them: write `model_flags_filtered` (type, category) into the run artifact and the report next to flag_tray. No behaviour change needed.",
   "acceptance_test": "D-053 text (or LLM_VS_CODE row 11/ladder) names objective_negative, scene_facts and non-per-record types as filtered by code; or a unit test feeding flags.merge a model-only scene_facts flag asserts a counted filtered entry in the run output."},
  {"severity": "nit",
   "title": "memory/SCOPE_CUTS.md has two rows numbered 13",
   "evidence": "memory/SCOPE_CUTS.md:17 `| 13 | LLM fallback for ambiguous record splitting ...` and memory/SCOPE_CUTS.md:66 `| 13 | Cross-record conflict detection beyond the code candidate rules (T-094, D-053) ...`; the file's convention for later additions is a suffix (`21b`, `11b`, `7b`).",
   "why_it_matters": "'SCOPE_CUTS row 13' now names two different cuts; a reviewer or the product note citing it can point at the wrong one.",
   "fix": "Renumber the T-094 row to `13b` (same convention as 11b, 7b, 21b) and update the references in the card handoff, D-053 and docs/LLM_VS_CODE.md if any.",
   "acceptance_test": "grep -c '^| 13 |' memory/SCOPE_CUTS.md returns 1."},
  {"severity": "nit",
   "title": "Negation guard in conflict_candidates covers only no/without/zero/never",
   "evidence": "app/backend/conflict_candidates.py:34 `_NEGATED_BEFORE = re.compile(r\"\\b(?:no|without|zero|never)\\s+(?:\\w+\\s+)?$\", re.I)`. Repro: probes/p1.py `[R(1,'Plan of care: 12 visits.'), R(2,'Patient is not lost to follow-up and has not stopped therapy.')]` -> one plan_vs_outcome candidate. memory/SCOPE_CUTS.md:66 describes the rules as 'negation- and completion-aware'.",
   "why_it_matters": "The false candidate goes to J3, which should answer benign and land it in the tray, so no wrong flag results; but each such candidate costs a call and adds tray noise, and one J3 flip makes a verified false conflict.",
   "fix": "Add `not` / `n't` (and 'has not') to the same-unit negation guard with a test, or say in SCOPE_CUTS that only no/without/zero/never are handled.",
   "acceptance_test": "tests/unit/test_conflict_candidates.py: 'Patient is not lost to follow-up and has not stopped therapy.' after a 12-visit plan yields []."}
 ],
 "whats_right": [
  "D-053 is implemented end to end and pinned: tray routing in flags.py, tray kind flag in present.case_view, scorer on emitted flags, flag_tray in the report and signature, each with a mutant-red test.",
  "Evidence is now tied to a commit: every report and controls file names `789cb39cad9fa38e6761c6336c2edd800d3805d2, tree clean`, and the failing run on the same commit is committed alongside the passing ones.",
  "Round-1 recall holes were widened in code, with the false positive ('no missed appointments') fixed and the remaining gaps listed in SCOPE_CUTS rather than left silent."
 ],
 "questions_for_chris": []}
```
