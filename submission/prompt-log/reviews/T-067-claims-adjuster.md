# T-067 review: defense credibility phrases (D-038), commit 59c7edb

Reviewer: claims-adjuster-reviewer (Gary Pruitt persona), model claude-haiku-5-5.
Scope: commit 59c7edb, extracted with `git archive` into the session scratchpad. The live working tree is dirty and was not used. Parent 89a323a and HEAD a27e3a4 were extracted only to compare the red tests.

## Summary

The five named phrase families fire with the whole sentence as the excerpt, under their own category, and stay pending. Normal and context findings stay silent (D-032), and plain denials and rule-outs raise nothing. Two blockers:

1. **Negated or negative credibility wording raises a credibility flag.** "Waddell signs negative.", "Pain is not out of proportion to the injury.", "No non-physiologic sensory loss." and "Waddell signs negative, no symptom magnification." all do. The template then says the wording "questions effort or symptom credibility", which is the opposite of what the record reports. This breaks D-032 and the negation requirement of this card.
2. **Named-family variants are silent.** "Effort is inconsistent during grip testing.", "Effort was inconsistent across repeated trials.", "Waddell testing positive at 3 of 5 sites." and "Symptom-magnification noted on exam." raise no flag. Six of the twelve off-sample phrasings in the named families were missed.

One major: the commit leaves 4 flag tests red. They pass at the parent and at HEAD a27e3a4.

## Exercised

- `git show --stat 59c7edb` and `git show 59c7edb -- app/backend tests memory/contracts/api.md` (full diff read).
- `git archive 59c7edb | tar -x -C <scratchpad>/t067`, then from inside that tree `/Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit/test_flags*.py -p no:cacheprovider -q` gives `4 failed, 43 passed`. The failures are `test_flags_pass.py::test_intake_form_date_is_not_patient_self_report`, `::test_no_flag_is_ever_accepted_and_patient_report_is_set_by_code`, `::test_d033_lexicon_flags_label_source_kind_by_the_same_rule`, and `test_flags_sample.py::test_patient_report_flag_is_labelled`.
- Same command on parent 89a323a gives `43 passed`. On HEAD a27e3a4 it gives `44 passed`. `git diff 59c7edb a27e3a4 -- tests/unit/test_flags_pass.py tests/unit/test_flags_sample.py` shows the test rewrites that match D-040.
- `... -k d038` on 59c7edb gives `4 passed, 21 deselected`.
- `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-probe.py <tree>` on 59c7edb: 30 cases (14 must-flag, 15 must-not, 1 multi-sentence). Four mismatches, all negated or negative: N04, N09, N10, N15. Each probe calls `flags.run_flag_pass` with an empty LLM script, so only the lexicon floor fires, which is the production path.
- `.venv/bin/python -I artifacts/review-evidence/T-067-claims-adjuster-recall-probe.py <tree>` on 59c7edb: 14 off-sample phrasings, 7 MISS (6 of 12 in the named families, plus one lexicon-named form outside D-038).
- Read `app/llm/lexicon.yaml` 852-862 and 1159-1169, `app/backend/flags.py` 17-30, 61, 88-105, `app/backend/flag_templates.py` 133, `tests/unit/test_flags_pass.py` 224-251, and `memory/ORCHESTRATOR_DECISIONS.md` D-032 (line 40), D-038 (line 46), D-040 (line 48).
- Two probe runs were not clean on the first attempt: a hedged sentence (E05) gets a hedge flag beside the credibility flag by design (D-038 test), and my first expectation counted it as a mismatch. I corrected the probe to judge the credibility flag only. The four N-mismatches are real.

## Findings

Details are in the JSON block below. Verdict by rule: two blockers, so `fail`.

- **blocker**: negated or negative credibility wording raises a flag (N04, N09, N10, N15).
- **blocker**: named-family recall misses (six of twelve off-sample forms).
- **major**: four flag tests red at 59c7edb (D-040 source_kind change lands without its tests, and the commit message does not mention D-040).
- **minor**: credibility template title and explanation predict the defense's use and assert a credibility attack.
- **minor (question)**: "Subjective complaints only." raises no flag, and D-038 does not say whether it should.

```json
{"card": "T-067", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 59c7edb (git archive, scratchpad tree; live working tree dirty, not used); parent 89a323a and HEAD a27e3a4 extracted for the red-test comparison only; no app server used (lexicon/flag level)",
 "exercised": ["git show --stat and git show 59c7edb -- app/backend tests memory/contracts/api.md (full diff)",
   ".venv/bin/python -m pytest tests/unit/test_flags*.py -p no:cacheprovider -q on 59c7edb -> 4 failed, 43 passed; on parent 89a323a -> 43 passed; on HEAD a27e3a4 -> 44 passed",
   ".venv/bin/python -m pytest tests/unit/test_flags_pass.py -k d038 on 59c7edb -> 4 passed",
   "artifacts/review-evidence/T-067-claims-adjuster-probe.py on 59c7edb: 30 cases, 4 mismatches (N04, N09, N10, N15)",
   "artifacts/review-evidence/T-067-claims-adjuster-recall-probe.py on 59c7edb: 14 off-sample phrasings, 7 MISS",
   "read app/llm/lexicon.yaml 852-862, 1159-1169; app/backend/flags.py 17-30, 61, 88-105; app/backend/flag_templates.py 133; tests/unit/test_flags_pass.py 224-251; memory/ORCHESTRATOR_DECISIONS.md D-032, D-038, D-040"],
 "verdict": "fail",
 "scores": {"no_invented_or_overstated_findings": 2, "negation_and_D-032": 1, "named_family_recall": 2, "whole_sentence_excerpt_and_own_category": 4, "commit_suite_green": 2, "template_neutrality": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Negated or negative credibility wording raises a credibility flag; the template states the opposite of the record",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-probe.py on 59c7edb. N04 'Waddell signs negative.' -> credibility_language, explanation 'Wording in IME (June 1, 2026) that questions effort or symptom credibility: Waddell signs negative.' N09 'Pain is not out of proportion to the injury.' -> flagged. N10 'No non-physiologic sensory loss.' -> flagged. N15 'Waddell signs negative, no symptom magnification.' -> flagged. Cause: app/llm/lexicon.yaml:859 'negatable: false' on subjective_exceeds_objective, with :862 false_positive 'Already negative phrasing, so it is not negatable.'; app/llm/lexicon.yaml:1166 'negatable: true' on symptom_magnification but no negative-result cue for 'Waddell signs negative'; app/backend/flags.py:26-30 is_credibility_hit never consults negation; app/backend/flag_templates.py:133 explanation text. Existing negation test covers only 'No evidence of symptom magnification.' at tests/unit/test_flags_pass.py:246-248.",
   "why_it_matters": "D-032 (memory/ORCHESTRATOR_DECISIONS.md:40) says normal and negative objective findings are context only and never flags. D-038 (line 46) narrows that only for defense credibility phrases; a negative Waddell result or a negated 'out of proportion' is not a credibility phrase. The card requires negated phrases not to be over-flagged. The paralegal would read an internal note saying the record questions the claimant's effort when the record reports a normal result. That is an overstated finding in the firm's own notes, and the test suite did not catch it.",
   "fix": "Make the credibility branch negation-aware. Set negatable true on subjective_exceeds_objective for 'out of proportion' and 'non-physiologic', and handle 'not out of proportion' and 'no non-physiologic'. Treat a Waddell or symptom-magnification result followed by negative, normal, absent or 'not present' (for example 'Waddell signs negative') as a negative finding that raises nothing. Add the negated rows to the lexicon examples.negated list and to tests/unit/test_flags_pass.py beside test_d038_negated_credibility_phrase_raises_nothing.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-067-claims-adjuster-probe.py against the fixed commit: N04, N09, N10 and N15 print OK and the run reports 0 mismatches. tests/unit/test_flags_pass.py has one assertion per N04/N09/N10/N15 sentence and passes."},
  {"severity": "blocker",
   "title": "Named credibility families missed in common word order, inflection and hyphenation (hidden credibility wording)",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-recall-probe.py on 59c7edb. MISS 'Effort is inconsistent during grip testing.'; MISS 'The effort displayed was inconsistent.'; MISS 'Effort was inconsistent across repeated trials.'; MISS 'Waddell testing positive at 3 of 5 sites.'; MISS 'Waddell 3 of 5 positive.'; MISS 'Symptom-magnification noted on exam.'. Also MISS 'Non-organic physical signs present.' (lexicon-named, not in the D-038 list). Cause: app/llm/lexicon.yaml:1160 matches only adjacent 'inconsistent effort', 'Waddell signs|tests' (not 'testing'), and unhyphenated 'symptom magnification'.",
   "why_it_matters": "The card says each named family raises a flag. D-038 (memory/ORCHESTRATOR_DECISIONS.md:46) says these phrases are what an adjuster quotes against the claimant and that hiding them defeats the prep purpose. 'Effort is inconsistent' is the most common IME wording for this family. The paralegal is not shown the credibility weakness, which is the same class as the missed-appointment omission in persona section 8. Six of the twelve off-sample named-family phrasings were silent.",
   "fix": "Extend the symptom_magnification pattern at app/llm/lexicon.yaml:1160 to reversed word order ('effort is/was/displayed ... inconsistent'), 'Waddell testing' and 'Waddell N of N', and hyphenated 'symptom-magnification'. Keep the negation guard working on the new forms ('Effort was not inconsistent.' must stay silent). Add each form to examples.hit and its negated counterpart to examples.negated. Any form left out must be listed in SCOPE_CUTS.md with a reason.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-067-claims-adjuster-recall-probe.py: every named-family row prints FLAG, or the row is listed as a scope cut. The negated counterparts print nothing."},
  {"severity": "major",
   "title": "Commit 59c7edb leaves 4 flag tests red: the D-040 source_kind change lands without its tests",
   "evidence": "Extracted 59c7edb tree: .venv/bin/python -m pytest tests/unit/test_flags*.py -p no:cacheprovider -q -> FAILED test_flags_pass.py::test_intake_form_date_is_not_patient_self_report (assert at :99), ::test_no_flag_is_ever_accepted_and_patient_report_is_set_by_code (assert at :105), ::test_d033_lexicon_flags_label_source_kind_by_the_same_rule (assert at :221), test_flags_sample.py::test_patient_report_flag_is_labelled (assert at :60); '4 failed, 43 passed'. Parent 89a323a: '43 passed'. Cause: 59c7edb sets source_kind 'record' in flags.py:61 ('# D-040: no code or model labels who is speaking') and removes the lexicon source_kind line from merge. Commit message names T-069 and T-067/D-038 only. HEAD a27e3a4: '44 passed' after its test rewrite.",
   "why_it_matters": "A card cannot close on a commit whose own unit suite is red. The speaker-label change (D-040, memory/ORCHESTRATOR_DECISIONS.md:48) is silent in the commit message, so a reviewer of T-067 or T-069 would not know a self-report label was removed. I accept the D-040 decision itself; the defect is the red suite and the unrecorded change.",
   "fix": "Land the D-040 test rewrites (as in a27e3a4) in the same commit, or split the flags.py source_kind change into its own commit. Name D-040 in the commit message. Re-run tests/unit/test_flags*.py at the commit that closes T-067.",
   "acceptance_test": ".venv/bin/python -m pytest tests/unit/test_flags*.py -p no:cacheprovider -q reports 0 failed at the commit that closes T-067."},
  {"severity": "minor",
   "title": "Credibility template title predicts the defense's use and asserts a credibility attack for every hit",
   "evidence": "app/backend/flag_templates.py:133: title 'Credibility wording a defense reviewer may quote'; explanation 'Wording in {source} that questions effort or symptom credibility{quote}.' Rendered for 'Waddell signs negative.' (probe N04 output).",
   "why_it_matters": "Persona section 4 item 20 bars predictions of the adjuster's argument in flag text. The text is a code template, so D-007 holds, and the flag is internal only (D-001). The title and the phrase 'questions effort' are adjuster framing, and they are wrong for negative results (see the first blocker). Minor because it does not reach the letter.",
   "fix": "Neutral template: title 'Credibility-related wording'; explanation 'Wording in <source> (<date>) that uses a credibility term: <quote>.' No 'defense', no 'may quote', no 'questions'.",
   "acceptance_test": "tests/unit/test_flag_templates.py asserts the credibility title and explanation contain neither 'defense' nor 'questions'. Probe N04 shows the neutral text."},
  {"severity": "minor",
   "title": "Question: subjective-only wording ('Subjective complaints only.') raises no flag; D-038 does not decide it",
   "evidence": "artifacts/review-evidence/T-067-claims-adjuster-probe.py N14 'Subjective complaints only.' -> none (raw scan: subjective_exceeds_objective, app/llm/lexicon.yaml:852-853). N13 'No objective findings on examination.' -> none, which D-038 (memory/ORCHESTRATOR_DECISIONS.md:46) expressly keeps context-only.",
   "why_it_matters": "Subjective-only complaints are the first thing I check (persona section 2), and D-038's own rationale is 'what an adjuster quotes'. Whether it belongs in the credibility set is a spec call. I would have done it differently; I am not calling it a defect.",
   "fix": "Chris decides. Either add 'subjective complaints only' to the credibility set, or record in D-038 that it stays context-only.",
   "acceptance_test": "D-038 names the decision; probe N14 matches it."}
 ],
 "whats_right": [
  "Positive credibility phrases fire under their own category with the whole sentence as excerpt and stay pending: all 14 must-flag rows in the probe pass on the excerpt and category, and test_d038_credibility_phrases_raise_a_flag_with_the_sentence_excerpt passes.",
  "Normal and context findings stay silent (D-032): 'Full cervical ROM. Ankle exam normal.' and 'No objective findings on examination.' raise nothing (N12, N13).",
  "Plain denials and rule-outs raise nothing ('No Waddell signs.', 'No evidence of symptom magnification.', 'Symptom magnification was ruled out.', 'Patient denies symptom magnification.'), and a two-sentence record quotes only the credibility sentence (M01)."
 ],
 "questions_for_chris": [
  "Should 'subjective complaints only' join the D-038 credibility set, or stay context-only? (minor finding 4)",
  "Is the title 'Credibility wording a defense reviewer may quote' intended, or an internal label to neutralize? (minor finding 3)"
 ]}
```
