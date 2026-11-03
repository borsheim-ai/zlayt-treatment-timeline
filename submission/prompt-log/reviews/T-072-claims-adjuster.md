# T-072 review: claims-adjuster-reviewer (D-040 follow-through)

**Verdict: fail** (one blocker). The export and golden are clean, and the flag template is neutral. The shipped frontend still shows the cut label in two places, which the brief's own grep check catches.

Model: claude-haiku-5-5, per the brief and the runtime. The dossier's expected id (opus) does not match the model actually running.

## What I checked

- **Export, golden, tests (pass).** The golden letter and notes, and the live export, carry no "(patient self-report)". The record 9 quote stays verbatim as "Patient states symptoms began after the January collision." (golden lines 38, 58, 69). No "physician" wording is added. The three brief test files pass (62 live; 61 at HEAD archive). The golden-byte tests pass (63 live, 42 at archive).
- **Neutral template (pass).** `app/backend/flag_templates.py:126` gives title "Reported onset" and explanation "Onset wording reported in ...". `tests/unit/test_export_edge.py:70` asserts no "self-report" or "patient self" in the title or explanation.
- **Internal id `patient_report` (not rendered as text, but exposed).** Text rendering uses `f.title` (`app/frontend/flags.js:66`). Export labels key on flag type only (`app/backend/export.py:248-257`). The id does appear in the API JSON (`app/backend/present.py:74`) and as a DOM attribute (`app/frontend/flags.js:65`). See F2.
- **User-facing "self-report" grep (fails).** See F1.

## Findings

- **F1 blocker.** `app/frontend/mock_flags.js:24` and `app/frontend/dev/mock-data.js:748-749` still show "Patient self-report (not a physician's opinion)". The overlay loads on every page (`index.html:45`). It is reached through the `?api=mock` override (`api.js:2`) and the `/dev/panels.html` harness (`panels.html:12`, served under the static mount at `api.py:508-511`). The default mode is "real" (`api.js:5`), so this is not in the default product path. I read the code path; I did not render it in a browser.
- **F2 minor.** Saying the id is "never shown to users" overstates it. It is not text, but `present.py:74` returns `"category": "patient_report"` in every flag payload, and `flags.js:65` writes it to `data-category`.
- **F3 minor.** `evals/golden/sample.expected.json:625` (flag K3) still has `"summary": "Causation rests on patient self-report, not a physician's causation opinion."` Commit 4594bb7 fixed only the `.txt` golden.
- **F4 nit.** "Reported onset" still implies a reporter. "Onset wording" would match the sibling "New-onset wording" (`flag_templates.py:127`). This is not a D-040 violation.
- **F5 nit.** `tests/e2e/test_flags_panel.py:19` is still named `test_patient_self_report_label`, though it asserts "Reported onset".

```json
{"card": "T-072", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commits 3b6a3fe and 4594bb7 (HEAD 83b4353 extracted with git archive to artifacts/review-evidence/T-072-T-074-83b4353 for test runs, extract removed afterwards); live tree /Users/arsis/zlayt-pm-project is dirty (tests/unit/test_eval_runner.py +9 lines uncommitted, app/llm/backends/fixture.py and others), so live results are reported separately; sample case Appendix A records 1-9; no browser run",
 "exercised": [
  "read personas/claims-adjuster.md in full; memory/ORCHESTRATOR_DECISIONS.md D-040, D-017, D-019; board show T-072; board validate -> 'ok (74 file(s))'",
  "git show --stat 3b6a3fe 4594bb7; git status --short; git diff HEAD -- tests/unit/test_eval_runner.py",
  "grep -rn -i 'self-report|self report|self-reported' app/ (excluding lexicon.yaml self_report keys); grep -rn 'patient_report|patient_reported_onset|source_kind' app/; grep -rln -i 'self.report|patient_report|source_kind' app/frontend",
  "read app/backend/flag_templates.py:120-135, app/backend/export.py:246-262, app/frontend/flags.js:60-70, app/backend/present.py:72-76, app/frontend/api.js:1-6, app/frontend/index.html:42-64, app/frontend/dev/panels.html, app/backend/api.py:505-512",
  "read app/frontend/mock_flags.js:20-30 and app/frontend/dev/mock-data.js:740-752; grep -n 'api=mock' tests/ (no e2e test uses mock mode)",
  "golden check: grep -n for Patient states|physician|self-report|Reported onset in evals/golden/sample.export.expected.txt (lines 38, 58, 69 only); diff of 4594bb7 golden hunk",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py -> 62 passed in 1.82s (live tree)",
  ".venv/bin/python -m pytest -q -p no:cacheprovider tests/unit/test_export.py tests/unit/test_eval_spec_check.py tests/unit/test_eval_runner.py at git archive 83b4353 -> 61 passed; tests/unit/test_export_edge.py tests/unit/test_case_extras.py tests/unit/test_flags_pass.py at 83b4353 -> 42 passed",
  ".venv/bin/python -m pytest -p no:cacheprovider tests/unit/test_export.py tests/unit/test_case_extras.py tests/unit/test_export_edge.py tests/unit/test_flags_pass.py (live) -> 63 passed; test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte PASSED",
  ".venv/bin/python tests/fixtures/make_curated.py --check -> 'letter equal: True | notes equal: True', exit 0 (live and at 83b4353)",
  "evals.run not re-run (writes evals/reports, outside my write paths); the hallucination figure in the card was not re-checked"
 ],
 "verdict": "fail",
 "scores": {"d040_no_speaker_label_user_facing": 2, "export_golden_fidelity": 5, "no_invented_facts_or_severity": 5, "internal_id_not_rendered_as_text": 4, "residue_cleanup_across_artifacts": 2, "tests_green_at_commit": 5},
 "findings": [
  {"severity": "blocker",
   "title": "User-reachable frontend code still displays 'Patient self-report' (D-040 violated; brief grep check fails)",
   "evidence": "app/frontend/mock_flags.js:24: mk(\"f_pat_9\", \"causation\", \"patient_report\", \"Patient self-report\", \"Patient self-report (not a physician's opinion) in Hill Country Pain Management, follow-up (June 12, 2026): ...\"; app/frontend/dev/mock-data.js:748-749: \"title\": \"Patient self-report\", \"explanation\": \"Patient self-report (not a physician's opinion) in Hill Country Pain Management ...\". Reachability: app/frontend/index.html:45 loads mock_flags.js on every page; app/frontend/api.js:2 documents the ?api=mock page-URL override; app/frontend/flags.js:64 uses f.title as aria-label and :66 renders it as the card heading; app/frontend/dev/panels.html:12 loads mock-data.js; app/backend/api.py:508-511 mounts all of app/frontend (including dev/) as static files. Default mode is real (api.js:5 API_MODE = \"real\"), so the text is not in the default path; not rendered in a browser (code-path evidence only).",
   "why_it_matters": "memory/ORCHESTRATOR_DECISIONS.md D-040: 'No code or model labels who is speaking.' This is the label the decision cut, with a 'not a physician's opinion' caveat, still in shipped code. A carrier or defense reviewer who opens ?api=mock sees a self-report label, which is the credibility problem D-040 exists to avoid. Severity is blocker under the D-040 rule. If Chris rules these overlays out of the deployed build, this drops to minor (see questions_for_chris).",
   "fix": "Frontend-owned (app/frontend/**; open a frontend card, cross-boundary from this backend card). Change mock_flags.js:24 and dev/mock-data.js:748-749 to the neutral template text from app/backend/flag_templates.py:126 ('Reported onset'; 'Onset wording reported in ...'), or delete the f_pat_9 overlay entry.",
   "acceptance_test": "grep -rn -i 'self-report|self report' app/frontend returns no hits; a Playwright test opens index.html?api=mock and asserts the flags panel contains 'Reported onset' and not 'self-report'; grep -c 'self-report' app/frontend/dev/mock-data.js is 0."},
  {"severity": "minor",
   "title": "'patient_report' is not rendered as text, but it is public API data; 'never shown to users' overstates",
   "evidence": "app/backend/present.py:74: flag_view returns \"category\": row[\"category\"], \"source_kind\": row[\"source_kind\"]; app/frontend/flags.js:65: \"data-category\": f.category; text rendering uses f.title (flags.js:66) and export labels key on flag type only (app/backend/export.py:248-257, _flag_label). Card T-072 note 2026-11-02T02:47:25Z: 'the id is never shown to users'. Producers still emit it: app/backend/flag_templates.py:25; app/llm/lexicon.yaml:741,757; app/llm/prompts/flags_v1.md:13 ('the patient's own statement').",
   "why_it_matters": "The brief's rendering check passes: the id is not text. But the id is the speaker label D-040 cut, it is returned in every flag payload, and the claim recorded on the card is inaccurate. An adjuster who inspects the network payload sees 'patient_report' on record 9.",
   "fix": "Either (a) correct the card and decision log to 'not rendered as text; present in API JSON and data-category', or (b) map to a neutral public id at the presentation layer (present.py:74 and flags.js:65), leaving the internal id and fixtures alone (this avoids the re-record the qa note cites). Owner: backend.",
   "acceptance_test": "Option (b): GET a sample case's flags and assert no category or data-* value contains 'patient'. Option (a): the card and decision note state the exposure."},
  {"severity": "minor",
   "title": "Golden expected flag K3 still carries the cut label",
   "evidence": "evals/golden/sample.expected.json:625: \"summary\": \"Causation rests on patient self-report, not a physician's causation opinion.\" (flag K3, subtype patient_reported_onset). Commit 4594bb7 edited only evals/golden/sample.export.expected.txt lines 58 and 69.",
   "why_it_matters": "The golden JSON is the expected-output authority for the flags. Keeping the cut label there means the expected output still says it. I did not trace whether evals compare K3.summary to product output (evals/run.py:118 and :229 read summaries; the K3 path was not traced).",
   "fix": "qa-owned (evals/**): change K3.summary to a neutral line that quotes the verbatim record, for example 'Causation language: record 9 verbatim \"Patient states ...\"'. Re-run evals.",
   "acceptance_test": "grep -n -i 'self-report' evals/golden/sample.expected.json returns only the M10 must_not statement (line 990) or nothing; eval gates unchanged."},
  {"severity": "nit",
   "title": "'Reported onset' still names an implied reporter",
   "evidence": "app/backend/flag_templates.py:126: \"patient_report\": lambda v: (\"Reported onset\", f\"Onset wording reported in {_at(v)}{_quote(v)}.\"). Sibling template at flag_templates.py:127: \"New-onset wording\".",
   "why_it_matters": "It names no speaker, so it passes D-040. 'Reported' still implies someone reported it. 'Onset wording' would match the sibling template.",
   "fix": "Optional: rename to 'Onset wording'. If renamed, update tests/unit/test_export_edge.py:70, tests/e2e/test_flags_panel.py, and the overlays in F1.",
   "acceptance_test": "None required."},
  {"severity": "nit",
   "title": "e2e test name still says 'self_report'",
   "evidence": "tests/e2e/test_flags_panel.py:19: def test_patient_self_report_label(page, sample_case): (body asserts \"Reported onset\").",
   "why_it_matters": "Test-only naming. It is not user-facing, but a grep for 'self_report' finds it.",
   "fix": "Rename to test_reported_onset_label.",
   "acceptance_test": "pytest collects the renamed test; grep -rn 'self_report_label' tests/ returns nothing."}
 ],
 "whats_right": [
  "The export matches the golden after the cut: the record 9 quote is still verbatim ('Patient states symptoms began after the January collision.') in letter line 38 and notes lines 58 and 69, with no added physician or opinion wording.",
  "The neutral template is in place and pinned: flag_templates.py:126 and tests/unit/test_export_edge.py:66-70 assert the title is 'Reported onset' and that no 'self-report' or 'patient self' appears in title or explanation.",
  "Golden and curated checks are green at the commit: test_export.py::test_sample_all_accepted_equals_golden_byte_for_byte, test_case_extras.py::test_default_export_is_byte_identical_to_golden_and_config_fills_the_citation, and make_curated --check (letter equal True, notes equal True)."
 ],
 "questions_for_chris": [
  "Are the ?api=mock overlay (app/frontend/mock_flags.js) and /dev/panels.html part of the deployed Space (D-008/D-020)? If they are stripped from the public build, F1 drops to minor and the verdict becomes changes.",
  "Keep the 'patient_report' id as internal only (F2 option a), or map it to a neutral public id at presentation (option b)?"
 ]}
```
