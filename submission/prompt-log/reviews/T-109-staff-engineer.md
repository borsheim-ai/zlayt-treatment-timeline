# T-109 review (staff-engineer-reviewer), commit bf0c748

Scope: `bf0c748` (docs/LLM_VS_CODE.md rows 4, 6, 7, 8, 11, 12, 15, 17, 19 and the rules list; memory/DECISIONS.md ADR-019 and in-place amendments). Claims were checked against code at HEAD `81aa55e` (read through `git archive` in a scratch copy). The doc and DECISIONS files are unchanged between `bf0c748` and HEAD. The code files changed since `bf0c748` (flags.py, credibility.py, T-092) do not touch any claim checked here.

Verdict: changes. No blocker. One major: row 7, row 103 and ADR-005/ADR-011 still say a rate can never become a charge, which D-042 reversed and `reclassify.py` implements.

Claim spot-check (all at HEAD):
- Conflicts are code-proposed candidates: holds. `conflict_candidates.py` has two fixed rules (`plans`, `history_denials`) and no model call; `flags.py:239-261` `run_conflict_pass` has no search call.
- Code does frequency x duration: holds. `conflict_candidates.py:23, 66-68`; the arithmetic string is carried in `ladder.code_checks.arithmetic` (`flags.py:231`).
- Model only classifies, judge_conflict_v4: holds. `judges.py:57-60`, `flags.py:269-272`, schema `Judge3` (verdict enum conflict/benign/unsure, `schemas.py:41-43`), prompt file `app/llm/prompts/judge_conflict_v4.md`. `conflicts_v1.md` is gone.
- suppressed_flags exists: holds. `flags.py:295-296` sets `_suppressed` on J4 disagree for origin llm only; `pipeline.py:357-359, 387` list it.
- Dosage and laterality not built: holds for candidates. Only two candidate rules exist; laterality appears only as a summary qualifier (`grounding.py:176, 228`).
- Hard 422 for side, negation, qualifier tokens: holds in both directions. `grounding.py:154-170` (added side/negation/qualifier tokens) and `grounding.py:217-232` (dropped qualifiers) feed `review.py:246-255`, which raises `_bad` (422 invalid_edit).
- Fail-safe language routing: holds on probes. `confidence.py:69` adds AI_TRANSLATION for Spanish or uncertain records. 19 probe lines gave no English leak (see nit 2).
- Billing is a listing: holds. `billing.py:3-6` says nothing is totaled or compared; no provider total, balance or complete flag; `billing.py:836` status is `listed`.
- Non-English never auto-verified: holds. `confidence.py:69` and `:76`; test `tests/unit/test_spanish_failsafe.py:111`.
- Code checks bind every accept: holds for entries. `review.py:159-166` (single accept and batch via `batch_apply`, `review.py:553-556`), `case_extras.py:46` (batch pre-check), `trace.py:437` (export gate). Amounts and flags have no editable wording; their accept is gated by stored state (rejected gives 409, `review.py:176-177`). See minor 1.

Exercised:
- `python3 tools/board.py show T-109`; `git show --stat bf0c748`; `git show bf0c748 -- docs/LLM_VS_CODE.md memory/DECISIONS.md`; `git diff --quiet bf0c748 HEAD -- docs/LLM_VS_CODE.md memory/DECISIONS.md` (both unchanged).
- Read docs/LLM_VS_CODE.md (120 lines at HEAD), memory/DECISIONS.md ADR-005, 011, 012, 013, 017, 019, memory/ORCHESTRATOR_DECISIONS.md D-034, D-042, D-047 to D-052 (grep).
- Read HEAD code: conflict_candidates.py (all), flags.py 186-310, judges.py, schemas.py, review.py (1-12, 30-200, 232-255), case_extras.py 17-76, grounding.py 150-232, language.py (all), confidence.py 50-76, billing.py (docstring and grep), reclassify.py (header), totals.py, trace.py 420-440.
- `git archive 81aa55e` and `git archive bf0c748` into a scratch directory. Ran `.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider` on the HEAD archive: 2214 passed, 4 skipped, exit 0 (158.67s). `tests/unit/test_conflict_candidates.py`: 16 passed. `tests/unit/test_reclassify.py`: 92 passed.
- Mutants (scratch copies only, nothing committed): M1 `flags.py` J4 suppression condition changed to a never-matching verdict, `test_pipeline.py` 1 failed; M2 `conflict_candidates.py` visits changed to `per` only, `test_conflict_candidates.py` 2 failed; M3 `review.py:159` entry gate disabled, `test_trace.py`, `test_review_rules.py`, `test_api_routes.py` 13 failed; M4 `flags.py` benign-to-tray branch disabled, 3 failed.
- Language probes with `language.detect` / `record_lang` on 19 lines (scratch scripts): no English leak.
- Greps: `dosage|laterality` across app and tests; `conflicts_v1` across app, tests, tools, evals; "no path to become a charge", "Still cut", "reclassif" across docs and memory.

## Findings

1. **major: rows 7 and 103 and ADR-005 and ADR-011 say a rate can never become a charge; D-042 and `reclassify.py` allow it.** Verbatim: docs/LLM_VS_CODE.md:35 "Charges are accept or dismiss only, so a rate has no path to become a charge." and :103 "Still cut, on purpose: reclassifying a charge (a rate must never become a charge)". Same claim in memory/DECISIONS.md:152 (ADR-005) and :235 (ADR-011). D-042 (memory/ORCHESTRATOR_DECISIONS.md:50) reinstated charge reclassification. `app/backend/reclassify.py:1, 5-9` implements it (not-a-charge to charge needs code charge wording with no rate cue, plus a J2 agreement). `tests/unit/test_reclassify.py:119-133` promotes an unclear $185 figure to a pending verified charge with J2 agree. T-109 rewrote row 7 and left this sentence in. The product is not unsafe: rate-cued sentences are refused (`test_reclassify.py:162, 191, 199`). The doc misstates the control. Not a blocker, because the product matches D-042 and the wording gate holds. Fix: rewrite row 7 and line 103 to describe the reclassify gate (charge to not-a-charge always allowed; not-a-charge to charge only with code wording and J2 agree; rate cues refused) and cite the tests. Amend ADR-005 and ADR-011 in place citing D-042. Acceptance: `git show HEAD:docs/LLM_VS_CODE.md` and `grep -rn "no path to become a charge\|a rate must never become a charge" docs memory` return nothing, and `.venv/bin/python -m pytest tests/unit/test_reclassify.py -q` stays green (92 passed at HEAD).

2. **minor: rule 7 says every accept must pass the code checks, but the code binds entries only.** Verbatim: docs/LLM_VS_CODE.md:17 "Every accept, single or batch, must pass the code checks first (D-051)." Code: `app/backend/review.py:159` `if kind == "entry" and DB.ACTIONS.get(action) in ("accepted", "edited"):`. Amounts and flags are accepted on the state their checks set at generation time, and their wording is immutable (charges accept or dismiss only; flags note only). That is sound, but the doc should say so. Fix: scope the sentence to entries and state why amounts and flags need no re-check. Acceptance: a grep of the sentence against `review.py:159` matches, and `tests/unit/test_trace.py` (CODE_CHECK_FAILED, lines 1151-1295) stays green.

3. **minor: ADR-019 cites an amendment that is not in ADR-013, and the "marked as amended" claim is only partly true.** memory/DECISIONS.md:349 (ADR-019 item 2) says "Amends the `LLM_ONLY` text of ADR-013." ADR-013 has no `LLM_ONLY` text; its origin paragraph says `LEXICON_ONLY` (memory/DECISIONS.md:285) and was not amended for model-only flags. Only ADR-005 carries the "amended by ADR-019" status (memory/DECISIONS.md:143). The commit message says ADR-005, 011, 012, 013, 014 and 017 are "marked as amended". Fix: amend the ADR-013 origin paragraph in place, and add an "amended by ADR-019" status mark to ADR-011 to ADR-017 as the commit claims. Acceptance: `grep -n "ADR-019" memory/DECISIONS.md` shows a status mark in each of ADR-011, 012, 013, 014 and 017, and the ADR-013 origin paragraph names the suppression rule.

4. **minor: the plan-vs-plan wording overstates what is tested.** `tests/unit/test_conflict_candidates.py:33` is named "frequency_times_duration_is_arithmetic_and_agrees_with_the_visit_count", but its assertions only check the arithmetic string and that no pair forms between records 3 and 4. No agreement comparison exists: `conflict_candidates.py:73-78` picks the explicit count and never compares it with a frequency plan. Line 8 of the same file says "Plans that agree make one plan", which implies a comparison. Row 11 itself is accurate ("no separate numeric agreement step"). Fix: rename the test to say it checks arithmetic and candidate absence; reword the module docstring line 8 to say the explicit count is quoted and nothing is compared. Acceptance: the renamed test passes, and `grep -n "agree" app/backend/conflict_candidates.py` shows no claim of a comparison.

5. **nit: the commit message and card AC overstate the arithmetic.** Commit bf0c748 body says code "resolves frequency x duration"; the card AC1 evidence says "code resolves frequency x duration". Row 11 says "multiplies", which is accurate. Fix: match the doc's word in future commit text. No code change.

6. **nit: row 4 says "enough English function and clinical words", but the code threshold is one English-only word.** `app/backend/language.py:28` `EN_CONFIDENT = 1.0`; `language.py:202-204` returns English on one English-only word with no foreign evidence. I could not reproduce a leak: 19 probe lines routed to Spanish, uncertain or mixed, never English (scratch scripts `lang_probe*.py`). Fix: say "at least one English-only word and no non-English evidence" in row 4, or raise the threshold. Acceptance: row 4 matches `language.py:28`.

7. **nit: the J3 eval set includes dosage and laterality pairs.** `tests/unit/test_t093_eval_signature.py:269-271` requires "P3-dosage" and "P3-laterality" pairs in the judge set. Row 11's "not built" is true for candidates, but a reader could take it as "not judged". Fix: say "not built as candidates; the judge eval includes sample pairs". Acceptance: row 11 names the eval scope.

## What is right

- Row 11, ADR-019 item 1 and `conflict_candidates.py` agree: two fixed rules, code arithmetic, no open model search, and 16 candidate tests pass. Mutants M2 and M4 are caught.
- The suppression path is real and tested: `flags.py:291-296`, `pipeline.py:357-359`, `test_pipeline.py:217-226`. Mutant M1 is caught.
- The 422 and code-check binding covers the cases the doc names, in both directions. Mutant M3 (entry gate off) fails 13 tests, and the batch path runs the same check (`case_extras.py:46`).

questions_for_chris:
- Should two plan statements that disagree (for example "2x/week for 6 weeks" = 12 visits against "Plan of care: 8 visits") form a candidate? Today code quotes the explicit count and never reports the mismatch (`conflict_candidates.py:73-78`).

```json
{"card": "T-109", "persona": "staff-engineer-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit bf0c748 (docs/LLM_VS_CODE.md rows 4,6,7,8,11,12,15,17,19 and rules list; memory/DECISIONS.md ADR-019 and in-place amendments); code checked at HEAD 81aa55e via git archive; no app URL (docs review); unit suite as the deterministic check; sample case through unit tests",
 "exercised": [
  "python3 tools/board.py show T-109",
  "git show --stat bf0c748; git show bf0c748 -- docs/LLM_VS_CODE.md memory/DECISIONS.md",
  "git diff --quiet bf0c748 HEAD -- docs/LLM_VS_CODE.md memory/DECISIONS.md (unchanged)",
  "read docs/LLM_VS_CODE.md (120 lines at HEAD), memory/DECISIONS.md ADR-005/011/012/013/014/017/019, memory/ORCHESTRATOR_DECISIONS.md D-034, D-042, D-047..D-052",
  "read HEAD code: app/backend/conflict_candidates.py, flags.py 186-310, judges.py, schemas.py, review.py, case_extras.py 17-76, grounding.py 150-232, language.py, confidence.py 50-76, billing.py docstring, reclassify.py header, totals.py, trace.py 420-440",
  "git archive 81aa55e and bf0c748 into scratchpad; .venv/bin/python -m pytest tests/unit -q on HEAD archive: 2214 passed, 4 skipped, exit 0",
  "pytest tests/unit/test_conflict_candidates.py: 16 passed; tests/unit/test_reclassify.py: 92 passed",
  "mutant M1 flags.py J4 suppression disabled: test_pipeline.py 1 failed; M2 freq arithmetic to per-only: 2 failed; M3 review.py:159 entry gate off: 13 failed; M4 benign-to-tray off: 3 failed (scratch copies only)",
  "language.detect/record_lang on 19 probe lines (scratch scripts): no English leak",
  "greps: dosage|laterality in app and tests; conflicts_v1 in app, tests, tools, evals; 'no path to become a charge', 'Still cut', 'reclassif' in docs and memory"],
 "verdict": "changes",
 "scores": {"claims_match_code": 3, "decisions_consistency": 3, "tests_backing_claims": 4, "fail_safe_and_binding": 4, "honest_limits_disclosed": 4},
 "findings": [
  {"severity": "major",
   "title": "Rows 7 and 103 and ADR-005/ADR-011 say a rate can never become a charge; D-042 and reclassify.py allow it",
   "evidence": "docs/LLM_VS_CODE.md:35 'Charges are accept or dismiss only, so a rate has no path to become a charge.'; docs/LLM_VS_CODE.md:103 'Still cut, on purpose: reclassifying a charge (a rate must never become a charge)'; memory/DECISIONS.md:152 and :235 same claim; memory/ORCHESTRATOR_DECISIONS.md:50 D-042 'charge reclassification (guarded...)'; app/backend/reclassify.py:1,5-9; tests/unit/test_reclassify.py:119-133 promotes an unclear $185 figure to a pending verified charge with J2 agree; tests/unit/test_reclassify.py:162,191,199 refuse rate-cued sentences",
   "why_it_matters": "The graded doc misstates a control. The reader is told a rate has no path to charge and that reclassification is cut, both false at HEAD. The product itself matches D-042 and the rate-cue gate holds, so this is not a blocker.",
   "fix": "Rewrite row 7 and line 103 to describe the reclassify gate: charge to not-a-charge always allowed; not-a-charge to charge only with code charge wording (no rate cue) and J2 agree; rate cues refused. Cite the tests. Amend ADR-005 and ADR-011 in place citing D-042.",
   "acceptance_test": "grep -rn 'no path to become a charge\\|a rate must never become a charge' docs memory returns nothing; .venv/bin/python -m pytest tests/unit/test_reclassify.py -q stays green (92 passed at HEAD)"},
  {"severity": "minor",
   "title": "Rule 7 says every accept must pass the code checks; the code binds entries only",
   "evidence": "docs/LLM_VS_CODE.md:17 'Every accept, single or batch, must pass the code checks first (D-051).'; app/backend/review.py:159 'if kind == \"entry\" and DB.ACTIONS.get(action) in (\"accepted\", \"edited\"):'",
   "why_it_matters": "Amounts and flags are accepted on the state their checks set at generation time, with immutable wording. That is sound, but the doc does not say so, and a reader would take the sentence literally.",
   "fix": "Scope the sentence to entries; state that amounts and flags carry their checks in the stored state and their wording is immutable.",
   "acceptance_test": "The reworded sentence matches review.py:159; tests/unit/test_trace.py CODE_CHECK_FAILED tests (lines 1151-1295) stay green"},
  {"severity": "minor",
   "title": "ADR-019 cites an LLM_ONLY text in ADR-013 that does not exist; only ADR-005 carries the amended-by mark",
   "evidence": "memory/DECISIONS.md:349 'Amends the `LLM_ONLY` text of ADR-013.'; memory/DECISIONS.md:285 ADR-013 origin paragraph says `LEXICON_ONLY` and has no LLM_ONLY text; memory/DECISIONS.md:143 is the only 'amended by ADR-019' status mark; commit bf0c748 body says ADR-005, 011, 012, 013, 014, 017 'marked as amended'",
   "why_it_matters": "The amendment trail is what a later reader uses to find the current rule. A dangling reference and missing marks make it harder to trust.",
   "fix": "Amend the ADR-013 origin paragraph in place for model-only flags; add an 'amended by ADR-019' status mark to ADR-011 through ADR-017 as the commit claims.",
   "acceptance_test": "grep -n 'ADR-019' memory/DECISIONS.md shows a status mark in ADR-011, 012, 013, 014 and 017; the ADR-013 origin paragraph names the suppression rule"},
  {"severity": "minor",
   "title": "Plan-vs-plan wording overstates the test and the docstring: no agreement comparison exists",
   "evidence": "tests/unit/test_conflict_candidates.py:33 test name 'frequency_times_duration_is_arithmetic_and_agrees_with_the_visit_count' asserts only the arithmetic string and absence of a 3-4 pair; app/backend/conflict_candidates.py:8 'Plans that agree make one plan'; app/backend/conflict_candidates.py:73-78 _canonical_plan picks the explicit count with no comparison",
   "why_it_matters": "A test name that claims agreement is checked invites a reader to think a mismatch between a frequency plan and a count is caught. It is not. Row 11 says so correctly.",
   "fix": "Rename the test to state what it checks; reword the docstring line to say the explicit count is quoted and nothing is compared.",
   "acceptance_test": "Renamed test passes; grep -n 'agree' app/backend/conflict_candidates.py shows no claim of a comparison"},
  {"severity": "nit",
   "title": "Commit message and card AC overstate: 'resolves' frequency x duration",
   "evidence": "git show -s bf0c748 body 'code resolves frequency x duration'; board show T-109 AC1 evidence 'code resolves frequency x duration'; docs/LLM_VS_CODE.md row 11 says 'multiplies'",
   "why_it_matters": "The doc is accurate; the commit text is not. Future readers of the log may take the wrong meaning.",
   "fix": "Use 'multiplies' in future commit text. No code change.",
   "acceptance_test": "None required"},
  {"severity": "nit",
   "title": "Row 4 says 'enough English words'; code accepts one English-only word",
   "evidence": "app/backend/language.py:28 EN_CONFIDENT = 1.0; app/backend/language.py:202-204 returns 'en' on one English-only word with no foreign evidence; 19 probe lines gave no English leak",
   "why_it_matters": "The doc describes a looser threshold than the code. No routing leak was reproduced, so this is wording only.",
   "fix": "Reword row 4 to 'at least one English-only word and no non-English evidence', or raise the threshold in code.",
   "acceptance_test": "Row 4 matches language.py:28 and 202-204"},
  {"severity": "nit",
   "title": "Judge eval set includes dosage and laterality pairs; row 11 says not built",
   "evidence": "tests/unit/test_t093_eval_signature.py:269-271 requires 'P3-dosage' and 'P3-laterality' pairs in the judge set",
   "why_it_matters": "Not built as candidates is true, but a reader could take it as not judged at all.",
   "fix": "Say 'not built as candidates; the judge eval includes sample pairs' in row 11.",
   "acceptance_test": "Row 11 names the eval scope"}
 ],
 "whats_right": [
  "Row 11, ADR-019 item 1 and conflict_candidates.py agree: two fixed rules, code arithmetic, no open model search; 16 candidate tests pass",
  "Suppression and the could-not-verify tray are real and tested (flags.py:291-296, pipeline.py:357-359, test_pipeline.py:217-226); the 422 and code-check binding hold for the named cases in both directions",
  "Full unit suite at HEAD archive 81aa55e: 2214 passed, 4 skipped; mutants M1-M4 each caught"
 ],
 "questions_for_chris": [
  "Should two plan statements that disagree (for example '2x/week for 6 weeks' = 12 visits against 'Plan of care: 8 visits') form a candidate? Today code quotes the explicit count and never reports the mismatch (app/backend/conflict_candidates.py:73-78)."
 ]}
```
