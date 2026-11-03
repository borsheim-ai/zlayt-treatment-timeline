# T-036 LLM flag passes, round 3 (commit 3f37141): claims-adjuster review (Gary Pruitt)

Verdict: **fail** (1 blocker, 2 major).

Round-2 items, status on 3f37141 (probes run on an extracted copy of the commit tree, `git archive 3f37141`, because the live working tree has uncommitted edits to confidence.py, flag_templates.py, why.py and pipeline.py):

- Round-2 blocker (source_kind must come from lexicon self_report): **partly resolved.** The two lines r2 named are now `patient_report` ("Patient notes prior neck pain.", "Patient links her neck pain to the collision."), and the record-7 intake date stays `record`. Two lexicon-matched self-report forms still read as `record` (finding 1). Non-patient complaint subjects now get `patient_report` through a different path (finding 2). The spec clauses were not amended (finding 3).
- Round-2 major (run-level conflict signal): **not counted**, per the brief. The `CONFLICT_PASS_INCOMPLETE` line is pending backend-2. On the commit, `status=done` with `warnings=[]` on both failure paths (probe section 5). The r3 test that asserts it (`test_flags_pass.py::test_pipeline_surfaces_conflict_pass_failure_as_run_warning`) is the one red test in that file, for the same reason.
- Round-2 minor (case-level warning pinned to record 1): **resolved.** `record_no=None`, `record_nos=[]`, and the why text no longer says "no AI-made entry" (probe section 5).
- Round-2 nit (`.”.` double period): **resolved.** Render sweep over all categories and two quotes shows no `.”.` (probe section 6).

Findings:

1. **Blocker.** Lexicon self-report wording still reads as a record statement. "S: neck pain 7/10." and "Self-reported neck pain 7/10." match a `self_report` entry in lexicon.yaml:744 but give `source_kind=record`. This is the r2 blocker class (spec DECISIONS.md:286: `source_kind` is "set by code from the lexicon `self_report` entries on the excerpt"). The cause is the word filter `_PATIENT_WORDS` at grounding.py:177, which lists `patient|pt|he|she|client|c/o|complain|subjective|patient-reported` but not `S` or `self`. The SOAP "S:" marker is the record's own subjective marker, so a patient's statement is shown as a record statement. No text is invented, but the attribution is lost. Same mechanism and same severity as r2 finding 1.

2. **Major.** Complaints from a non-patient subject are labelled "Patient self-report". "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain." and "Family complains of neck pain." all return `has_self_report=True`. The cause is `complain(?:s|ed|ing|t)?` in `_SELF` (grounding.py:167) and `complain\w*` in `_PATIENT_WORDS` (grounding.py:177). lexicon.yaml:744 still lists wife|husband|family|witness|EMS before "complains". The r3 exclusion only works for the "reports/states" verbs, so r2 finding 1's fix item 3 (remove EMS, witness, wife, husband, family, friend) is only partly met. The chip "Patient self-report" then tells the reader the claimant said it. Over-attribution, not invention.

3. **Major.** The spec and lexicon were not amended for the narrowing the code now does. `git show --stat 3f37141` lists no memory/DECISIONS.md and no app/llm/lexicon.yaml. DECISIONS.md:286 still says "set by code from the lexicon `self_report` entries"; lexicon.yaml:25-26 still says "code sets source_kind = patient_report from it (ADR-013)"; lexicon.yaml:759-764 still marks `intake_form_accident_date` `self_report: true`, and code excludes it by name (grounding.py:175). Probe section 2 shows the intake example as a lexicon hit with `has_self_report=False`, and section 4 counts 8 lexicon-matched excerpts that code marks `record`. r2 made the narrowing conditional on a same-commit spec amendment (questions_for_chris #1 in r2); that condition is not met.

What is right:
- Record 7's intake date is `source_kind=record` on the commit (probe section 1: `f_r7_1 ... source_kind=record ... "Date of accident per intake form: 2026-01-19."`). Record 3 ("Patient reports low back pain in 2023, resolved.") and record 9 ("Patient states symptoms began after the January collision.") are `patient_report`.
- Sample-case flags on the commit tree: the gap reads "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)." with no invented reason; the conflict reads "...The records disagree; the tool does not choose between them."; no delay from an accident date is computed.
- Template neutrality holds: no own-voice adjective, no double period on any rendered category.

Exercised (all on the extracted commit tree unless marked):
- Read personas/claims-adjuster.md in full; read reviews/T-036-claims-adjuster-r2.md; read my memory dir.
- `git show --stat 3f37141`, `git show --stat --format= 3f37141 | grep -E "DECISIONS|lexicon"` (no output: not amended), `git diff --stat 3f37141 -- <r3 files>` (working tree differs in confidence.py, flag_templates.py, why.py, pipeline.py: uncommitted, not reviewed).
- `grep -n "self_report" app/backend/flags.py` -> `flags.py:42 "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",` and `flags.py:115 lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"` (no direct lexicon reference in flags.py; the lexicon contribution is in grounding._self_report, grounding.py:180-188).
- `grep -n "self_report" app/backend/grounding.py`, `sed -n 165,225p`, `grep -n "self_report" -B3 -A8 app/llm/lexicon.yaml`, `sed -n 18,30p app/llm/lexicon.yaml`, `sed -n 280,292p memory/DECISIONS.md`.
- Parsed lexicon.yaml: 4 self_report entries; patterns and examples listed.
- `.venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2` on the live tree -> `48 passed in 0.27s`; same command on the extracted commit tree -> `48 passed in 0.27s`.
- `.venv/bin/python tests/fixtures/make_curated.py --check` (live tree and extracted commit tree) -> `entries: 9 non-verified: []` / `letter equal: True | notes equal: True`, exit 0.
- `.venv/bin/python -m pytest tests/unit/test_flags_pass.py -q` on the commit tree -> `1 failed, 14 passed` (the failure is the pending CONFLICT_PASS line; excluded).
- `.venv/bin/python -m pytest tests/unit -q` on the commit tree -> `2 failed, 765 passed` (test_flags_pass.py pending item; test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode, IndexError, not triaged and not attributed to r3).
- `artifacts/review-evidence/T-036-r3-probe.py <tree>` run on the extracted commit tree -> `artifacts/review-evidence/T-036-r3-commit-probe.txt` (sample run, own-example parity, 21 probe strings, spec-literal gap list, conflict failure paths, template sweep). Same script on the live tree -> `artifacts/review-evidence/T-036-r3-probe.txt` (superseded; same findings).
- Extracted tree: `git archive 3f37141 | tar -x -C artifacts/review-evidence/T-036-r3-commit-3f37141`.

Outside my lens: the wording of the "Cross-record check did not finish" title and the CONFLICT_CHECK_INCOMPLETE why are product copy; I checked only that they carry no attribution error.

```json
{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit 3f37141 (app/backend/grounding.py, flags.py, flag_templates.py, why.py, confidence.py, tests/unit/test_flags_pass.py, memory/contracts/api.md) run from an extracted git-archive copy; spec memory/DECISIONS.md:286; app/llm/lexicon.yaml; sample case evals/golden/sample.txt via the fixture pipeline (no live app URL; LLM is scripted FakeCall). Live working tree has uncommitted edits not reviewed.",
 "exercised": [
  "Read personas/claims-adjuster.md in full; read reviews/T-036-claims-adjuster-r2.md and my memory dir",
  "git show --stat 3f37141 (no DECISIONS.md or lexicon.yaml in the commit)",
  "git diff --stat 3f37141 -- app/backend/grounding.py app/backend/flags.py app/backend/flag_templates.py app/backend/why.py app/backend/confidence.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py (live tree differs in confidence.py, flag_templates.py, why.py, pipeline.py)",
  "grep -n 'self_report' app/backend/flags.py -> flags.py:42 and flags.py:115 (has_self_report calls)",
  "grep -n 'self_report' app/backend/grounding.py; sed -n 165,225p app/backend/grounding.py (_SELF:167, _NOT_PATIENT_STATEMENT:175, _PATIENT_WORDS:177, _self_report:180-188)",
  "grep -n 'self_report' -B3 -A8 app/llm/lexicon.yaml; sed -n 18,30p app/llm/lexicon.yaml; yaml parse of 4 self_report entries (self_reported_prior:477, patient_attributes_causation:727, patient_reports_generic:743, intake_form_accident_date:759)",
  "sed -n 280,292p memory/DECISIONS.md (line 286 spec)",
  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2 -> 48 passed in 0.27s (live tree and extracted commit tree)",
  ".venv/bin/python tests/fixtures/make_curated.py --check -> letter equal: True | notes equal: True (live and commit tree)",
  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py -q (commit tree) -> 1 failed, 14 passed (pending CONFLICT_PASS line; excluded)",
  ".venv/bin/python -m pytest tests/unit -q (commit tree) -> 2 failed, 765 passed (pending-line test; test_api_routes judge-unavailable IndexError, not attributed)",
  "git archive 3f37141 | tar -x -C artifacts/review-evidence/T-036-r3-commit-3f37141; artifacts/review-evidence/T-036-r3-probe.py <tree> -> artifacts/review-evidence/T-036-r3-commit-probe.txt (sections 1-6: sample flags with source_kind, own-example parity, 21 probe strings with lexicon hit vs has_self_report vs lexicon_flags, spec-literal gap list, conflict failure paths, template sweep)",
  "sample text evals/golden/sample.txt (records 1, 3, 6, 7, 9 verbatim lines checked against flag excerpts)"
 ],
 "verdict": "fail",
 "scores": {"surfaces_every_attack_item_on_sample": 5, "no_invented_or_overstated_text": 3, "patient_attribution_label": 2, "visible_conflict_failure": 4, "template_neutrality": 5, "test_honesty": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Lexicon self_report wording still reads as a record statement: 'S: neck pain 7/10.' and 'Self-reported neck pain 7/10.' give source_kind=record",
   "evidence": "artifacts/review-evidence/T-036-r3-commit-probe.txt section 3: \"'S: neck pain 7/10.' expect=patient lex=True has_self_report=False | no lexicon flag <-- DISAGREES\" and \"'Self-reported neck pain 7/10.' expect=patient lex=True has_self_report=False\"; section 4 lists both as 'lexicon says self_report, code says record'. Lexicon: app/llm/lexicon.yaml:744 pattern ends with `|\\b(?:patient|self)-?\\s?reported\\b|^\\s*(?:subjective|S)\\s*:`. Filter: app/backend/grounding.py:177 `_PATIENT_WORDS = ... \\b(?:patient|pt|he|she|client|c/o|complain\\w*|subjective)\\b|patient-reported` (no S, no self). Spec: memory/DECISIONS.md:286 'source_kind = \"patient_report\" is set by code from the lexicon self_report entries on the excerpt'.",
   "why_it_matters": "Same clause and same loss as r2 blocker 1. The lexicon marks these lines as patient self-report and the code does not. In a SOAP note 'S:' is the record's own subjective marker, so the claimant's statement reads as a record statement. Nothing is invented (the verbatim quote keeps the marker), but the attribution the spec requires is lost, and the r3 test list (test_flags_pass.py yes-list) does not cover these forms.",
   "fix": "Replace the word whitelist with a subject exclusion: a lexicon self_report hit counts as patient_report unless the match begins with a non-patient subject (EMS, witness, wife, husband, spouse, mother, father, parent, family, friend). This also covers finding 2. Drop the _NOT_PATIENT_STATEMENT name list only if finding 3 is resolved by setting intake_form_accident_date self_report: false in lexicon.yaml.",
   "acceptance_test": "tests/unit/test_flags_pass.py: grounding.has_self_report('S: neck pain 7/10.') and has_self_report('Self-reported neck pain 7/10.') are True; lexicon_flags on those lines (or the LLM+lexicon path) gives source_kind 'patient_report'; the existing r3 yes/no lists still pass."},
  {"severity": "major",
   "title": "Complaints from EMS, a witness, a wife or family are labelled 'Patient self-report' because the complaint verb bypasses the subject filter",
   "evidence": "artifacts/review-evidence/T-036-r3-commit-probe.txt section 3: \"'EMS complains of neck pain 7/10.' expect=record ... has_self_report=True <-- DISAGREES\"; \"'Witness complains of neck pain.' ... has_self_report=True\"; \"'Wife complains of neck pain.' ... has_self_report=True\"; \"'Family complains of neck pain.' ... has_self_report=True\". Cause: app/backend/grounding.py:167 _SELF `\\bcomplain(?:s|ed|ing|t)?\\b` and grounding.py:177 `complain\\w*` in _PATIENT_WORDS; lexicon.yaml:744 lists wife|husband|spouse|mother|father|parent|family|friend|witness|EMS before `complains`. The r3 no-list (test_flags_pass.py) only checks 'reports' and 'states' forms.",
   "why_it_matters": "The r2 finding 1 fix (item 3) asked that EMS, witness, wife, husband, family and friend not set patient_report. The r3 exclusion only covers the reports/states verbs. The chip 'Patient self-report' and its explanation '(not a physician's opinion)' then credit the claimant with a statement a family member or EMS made. That is an attribution error, not an invented fact, so major rather than blocker.",
   "fix": "Apply the non-patient subject exclusion to the whole match regardless of verb (see blocker fix). Either remove the non-patient subjects from lexicon.yaml:744 (r2 fix item 3) or keep them and exclude in code; say which in DECISIONS.md.",
   "acceptance_test": "has_self_report is False for 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'EMS reports neck pain 7/10.', 'Wife reports he was in pain.'; True for 'Patient complains of neck pain.' and 'C/O neck pain 7/10 and headache.'"},
  {"severity": "major",
   "title": "Spec (DECISIONS.md:286) and lexicon header (lexicon.yaml:25-26) not amended for the narrowing the code now applies; lexicon and code disagree on 8 excerpts",
   "evidence": "git show --stat 3f37141: no memory/DECISIONS.md and no app/llm/lexicon.yaml in the commit. DECISIONS.md:286 still: 'source_kind = \"patient_report\" is set by code from the lexicon self_report entries on the excerpt'. lexicon.yaml:25-26 still: 'code sets source_kind = \"patient_report\" from it (ADR-013)'. lexicon.yaml:759-764 still `self_report: true` for intake_form_accident_date; code skips it by name at grounding.py:175 (`_NOT_PATIENT_STATEMENT = {\"intake_form_accident_date\"}`). Probe section 2: \"[intake_form_accident_date] lex=True has_self_report=False 'Date of accident per intake form: 2026-01-19.' <-- MISMATCH\". Probe section 4 count: 8.",
   "why_it_matters": "r2 made the narrowing conditional: 'If the narrowing was intended, amend DECISIONS.md:286 and lexicon.yaml:25-26 in the same commit.' Neither file changed. A future worker or reviewer reading the contract gets a different rule from the code. The narrowing itself is correct for the intake date and EMS/witness statements; the contract is what is wrong.",
   "fix": "Either (a) amend DECISIONS.md:286 and lexicon.yaml:25-26 to state the subject rule and the intake exclusion, and set intake_form_accident_date self_report: false in lexicon.yaml so the lexicon is the single source; or (b) move the rule into lexicon.yaml and remove _NOT_PATIENT_STATEMENT. Chris decides (question 1).",
   "acceptance_test": "A parity test reads lexicon.yaml self_report entries and asserts has_self_report(example) for every example.hit that is not a non-patient subject, with no code-side name list; grep -n '_NOT_PATIENT_STATEMENT' app/backend/grounding.py returns nothing, or DECISIONS.md:286 names the exclusion."}
 ],
 "whats_right": [
  "Record 7's intake date is source_kind 'record' on 3f37141 (f_r7_1 in T-036-r3-commit-probe.txt section 1), and record 3 and record 9 remain 'patient_report'.",
  "The case-level conflict warning carries record_no None and record_nos [] with a neutral why (section 5), and no template renders the '.”.' double period (section 6).",
  "The sample gap flag states 'Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).' with no invented reason, and the conflict flag says the tool does not choose between the two accident dates."
 ],
 "questions_for_chris": [
  "Which way should the source_kind contract go: amend DECISIONS.md:286 and lexicon.yaml:25-26 to match the subject-exclusion code (and set intake_form_accident_date self_report: false), or restore the code to the literal lexicon rule? My recommendation is the first, so the lexicon is the single source.",
  "Should 'Wife complains of' and 'Family complains of' carry 'Patient self-report' at all? I treat them as misattributed; the lexicon (lexicon.yaml:744) currently says they are self-report.",
  "Who owns test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode (IndexError on the commit tree)? It is outside the r3 diff, and I did not triage it.",
  "Model id: I ran as claude-haiku-5-5; the persona file expects claude-opus-5-5 in the review record. I wrote the id I ran as. Confirm that is acceptable for the gate."
 ]}
```
