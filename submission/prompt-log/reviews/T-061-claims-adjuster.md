# T-061 Self-report label precision: claims-adjuster review (Gary Pruitt), round 0

Verdict: **fail** (1 blocker, 2 major, 1 minor).

What the commit does: dd545e3 narrows the lexicon `self_report` entries to explicit patient attribution, adds a `self_report_scope.exclude_sentence` regex (lexicon.yaml:88-93), marks `intake_form_accident_date` `self_report: false`, and adds 26 held-out probes. The lexicon side holds up. The product side does not: no file under `app/backend/` changed in dd545e3, so AC2 (flags.py/grounding.py label only from those entries, with tests) is not done, and the production label still attributes EMS, witness, wife and family complaints to the patient.

Checks against the card and D-033:

- AC1 (lexicon): the selfcheck passes and the scope-aware lexicon gets the brief's five sentences right. Two over-exclusion cases remain (finding 2).
- AC2 (flags.py/grounding.py + tests): **not done.** `git show --stat dd545e3` lists only `app/llm/lexicon.yaml`, `evals/lexicon_heldout.jsonl` and `research/lexicon_selfcheck.py`. Production still calls `grounding.has_self_report` (flags.py:46 and flags.py:125), which still uses the old `_SELF` complain verb (grounding.py:167) and the `_PATIENT_WORDS` word filter (grounding.py:177). `exclude_sentence` is referenced nowhere in `app/` or `tests/`.
- AC3 (spec note or D-entry): D-033 exists (ORCHESTRATOR_DECISIONS.md:41), which meets the "or" clause. DECISIONS.md:286 and lexicon.yaml:25-26 still state the superseded rule (finding 3).
- Brief sentences: "Patient states pain began after the collision." is patient_report in the lexicon and in production. "Wife reports he has been irritable.", "Per EMS, pt ambulatory at scene.", "S: neck pain" and "Witness states the car ran the light." are record in both. No sentence I fed was invented or altered.

Why finding 1 is a blocker when T-036 r3 rated the same behaviour major: D-033 now names this case as a credibility error ("Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit"). At r3 there was no such decision. The production code contradicts a recorded decision, so it is a spec violation.

Findings:

1. **Blocker.** AC2 not done: production still labels EMS, witness, wife and family complaints as "Patient self-report". Evidence: `artifacts/review-evidence/T-061-probe.txt`, rows "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain.", "Family complains of neck pain." each show `production has_self_report: patient_report` and `lexicon(scope-aware): record`. Cause: grounding.py:167 `\bcomplain(?:s|ed|ing|t)?\b` in `_SELF`, and grounding.py:177 `complain\w*` in `_PATIENT_WORDS`. flags.py:46 and flags.py:125 use the result as `source_kind`. `git show --stat dd545e3` has no app/backend entry. Card AC2 is `done: false`.
   Why it matters: the chip "Patient self-report" tells the reader the claimant said it. A family member's or EMS's statement carries the claimant's name on it, and I would use that to discount the package.
   Fix: in grounding.has_self_report, replace `_SELF` and `_PATIENT_WORDS` with "any lexicon self_report hit AND NOT self_report_scope.exclude_sentence" (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Set the intake date through `self_report: false` and delete `_NOT_PATIENT_STATEMENT` (grounding.py:175). Fix finding 2 in the same change.
   Acceptance test: has_self_report is False for "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain.", "Family complains of neck pain.", "EMS reports neck pain 7/10.", "Wife reports he was in pain.", "Date of accident per intake form: 2026-01-19."; True for "Patient states pain began after the collision.", "Patient complains of neck pain.", "C/O neck pain 7/10 and headache.", "Patient-reported neck pain 7/10."; and `grep -n "_SELF\|_PATIENT_WORDS\|_NOT_PATIENT_STATEMENT" app/backend/grounding.py` returns nothing.

2. **Major.** The commit leaves `tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution` red, a regression from the parent. Evidence: `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2` on the live tree (equal to dd545e3 for these paths) gives `1 failed, 113 passed, 699 deselected`. On the git archive of parent 099732b the same command gives `114 passed, 697 deselected`. The full suite diff (`artifacts/review-evidence/T-061-base-failed.txt` vs `T-061-head-failed.txt`) adds exactly this test. The failing assertion is the yes-list entry "Subjective: neck pain 7/10.", which the lexicon no longer matches (lexicon.yaml:754-759, pattern now without `^\s*(?:subjective|S)\s*:`). The test is the r2 contract, which D-033 supersedes for bare S:/Subjective: headers. The card's evidence line ("selfcheck PASS ... golden MUST 11/11") does not mention a pytest run, so the red test was not reported.
   Why it matters: a red flag test on the commit means the worker did not run the suite it touched, and the stale test would hide a regression in the next round.
   Fix: update the test to D-033 (Subjective: and S: are record; a bare header is not an attribution) and add the AC2 tests from finding 1 to tests/unit/test_flags_pass.py.
   Acceptance test: `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon"` reports 0 failed, and the full `tests/unit` run shows no FAILED line that is not also in the parent archive.

3. **Major.** `exclude_sentence` drops explicit patient statements whenever a family or EMS word and a speech verb share the sentence. Evidence: `artifacts/review-evidence/T-061-probe.txt`, "Patient states EMS noted a laceration." and "Patient reports his wife said he was fine." both give lexicon `record` (`LEX` mismatch) while the patient is the speaker. Cause: lexicon.yaml:89 matches `\b(?:EMS|...|wife|...)\b(?:\s+[\w'-]+){0,3}?\s+(?:...|noted|said|...)\b` anywhere in the sentence, not only at the grammatical subject. Held-out coverage gap: none of the 26 new probes pairs a patient subject with a family or EMS word (grep of evals/lexicon_heldout.jsonl), so selfcheck PASS cannot show it.
   Why it matters: a patient-attributed statement loses its "Patient self-report" attribution (D-033: "patient-quoted speech" stays patient_report). This is latent today because production does not read exclude_sentence yet. Finding 1's fix would make it live.
   Fix: anchor the exclusion to the sentence subject (sentence-initial "EMS/Wife/Witness/Family ... <verb>", or a "Per <non-patient>" clause), and exclude any sentence that starts with or names "Patient"/"Pt"/"C/O". Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.
   Acceptance test: "Patient states EMS noted a laceration.", "Patient reports his wife said he was fine." are patient_report; "EMS reports minimal damage.", "Wife complains of neck pain.", "Per his wife, headaches began at the scene." stay record; `research/lexicon_selfcheck.py` still PASS.

4. **Minor.** The spec still states the superseded rule. DECISIONS.md:286 still says "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". lexicon.yaml:25-26 still says "code sets source_kind = "patient_report" from it (ADR-013)" (the header was edited only on line 25). D-033 says it "Narrows ADR-013 / DECISIONS.md:286", so AC3's "or" clause is met, but the spec text now contradicts the code's exclusion rule.
   Fix: architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to "self_report entries that name the patient, minus self_report_scope.exclude_sentence". The card's AC3 `done` flag can then be set true.
   Acceptance test: `grep -n "set by code from the lexicon" memory/DECISIONS.md` shows the amended text and no line still reads "from the lexicon `self_report` entries on the excerpt".

Things I did not treat as findings, for Chris:
- D-033 labels a bare "S:" or "Subjective:" header as record. In a SOAP note that header is the clinician's marker for the patient's report. The verbatim marker stays in the excerpt, so nothing is invented. I accept D-033 as the decision, and I note the adjuster would give subjective-only weight to these lines.

Exercised (live tree; `git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit` shows only evals/reports/latest.json, outside my scope, so live == dd545e3 for reviewed paths):
- Read personas/claims-adjuster.md in full; `python3 tools/board.py show T-061`; `grep -n "D-033" -A 15 memory/ORCHESTRATOR_DECISIONS.md`; reviews/T-036-claims-adjuster-r3.md; my memory dir.
- `git log --oneline -5`; `git show --stat dd545e3`; `git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py` (diff read in full).
- `.venv/bin/python research/lexicon_selfcheck.py` -> `RESULT: PASS`, golden MUST 11/11, held-out 115/115, adjuster probes 62/63 (the one FN, "No acute findings." low only, is pre-existing), EXIT=0.
- `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2` -> `1 failed, 113 passed, 699 deselected`; full failure text read (`pytest ... -k lexicon_self_report` -> 1 failed, assertion at tests/unit/test_flags_pass.py:121).
- Same subset on `git archive 099732b` (parent) -> `114 passed, 697 deselected`.
- Full `tests/unit` on live tree -> `2 failed, 811 passed` (flags test plus test_t037_backend.py::test_replay_has_no_fixture_miss[case_09_nonvisit_hides_gap]); on archives: parent `3 failed, 808 passed`, dd545e3 `4 failed, 807 passed`; the failing-test lists differ only by the flags test. The three test_t037 replay failures exist at parent and are not attributable to dd545e3; the live tree and archives disagree on case_09, which I did not triage.
- `artifacts/review-evidence/T-061-probe.py /Users/arsis/zlayt-pm-project` -> `artifacts/review-evidence/T-061-probe.txt`: 27 sentences (the five brief sentences, the researcher's test list, EMS/witness/wife/family complaints, S:/Subjective:/Self-reported headers, two over-exclusion candidates) through the lexicon (scope-aware) and `grounding.has_self_report`.
- `grep -n "has_self_report\|self_report_scope\|exclude_sentence" app/backend/flags.py app/backend/grounding.py` -> flags.py:46, flags.py:125, grounding.py:219 only; `grep -rn "exclude_sentence\|self_report_scope" app/ tests/` -> lexicon.yaml only.
- `grep -n "^_SELF\|^_NOT_PATIENT_STATEMENT\|^_PATIENT_WORDS" app/backend/grounding.py` -> 167, 175, 177.
- `grep` of evals/lexicon_heldout.jsonl for patient subjects with family/EMS words -> none (coverage gap, finding 3).
- `git archive` extractions were deleted after use; the failing-test lists are kept as artifacts.

Outside my lens: the test-runner setup and the t037 replay failures (not triaged); the commit message's co-author line.

```json
{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit dd545e3 (HEAD; parent 099732b) on the live tree (equal to dd545e3 for app/backend, app/llm/lexicon.yaml, research, evals, tests/unit); spec memory/DECISIONS.md:286; decision memory/ORCHESTRATOR_DECISIONS.md D-033; no app URL (lexicon and flag-layer change, no UI in scope); sample probes as listed.",
 "exercised": [
  "Read personas/claims-adjuster.md in full; python3 tools/board.py show T-061; D-033 (ORCHESTRATOR_DECISIONS.md:41); reviews/T-036-claims-adjuster-r3.md; my memory dir",
  "git log --oneline -5; git show --stat dd545e3 (lexicon.yaml, lexicon_heldout.jsonl, lexicon_selfcheck.py only; no app/backend)",
  "git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py (full diff read)",
  "git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit (only evals/reports/latest.json, out of scope)",
  ".venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS; golden MUST 11/11; held-out 115/115; EXIT=0",
  ".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon' 2>&1 | tail -2 -> 1 failed, 113 passed, 699 deselected",
  "same subset on git archive 099732b (parent) -> 114 passed, 697 deselected",
  "full tests/unit: live 2 failed/811 passed; parent archive 3 failed/808 passed; dd545e3 archive 4 failed/807 passed; FAILED-list diff = test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution only (artifacts/review-evidence/T-061-base-failed.txt, T-061-head-failed.txt)",
  "artifacts/review-evidence/T-061-probe.py <repo> -> artifacts/review-evidence/T-061-probe.txt (27 sentences through lexicon scope-aware and grounding.has_self_report)",
  "grep -n has_self_report|self_report_scope|exclude_sentence app/backend/flags.py app/backend/grounding.py -> flags.py:46, 125; grounding.py:219; grep -rn exclude_sentence app/ tests/ -> lexicon.yaml only",
  "grep -n ^_SELF|^_NOT_PATIENT_STATEMENT|^_PATIENT_WORDS app/backend/grounding.py -> 167, 175, 177",
  "grep evals/lexicon_heldout.jsonl for patient-subject sentences containing EMS/wife/witness/family -> none",
  "sed -n 284,288p memory/DECISIONS.md (line 286 text); grep self_report_scope / lexicon header lines 13, 25-26"
 ],
 "verdict": "fail",
 "scores": {"attribution_precision_production": 1, "lexicon_scope_logic": 3, "ac2_flags_wiring": 1, "test_honesty": 2, "spec_consistency": 3, "no_invented_or_altered_text": 5},
 "findings": [
  {"severity": "blocker",
   "title": "AC2 not done: production still labels EMS, witness, wife and family complaints as Patient self-report",
   "evidence": "artifacts/review-evidence/T-061-probe.txt rows 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.': production has_self_report=patient_report, lexicon(scope-aware)=record. Cause: app/backend/grounding.py:167 (_SELF, complain verb) and grounding.py:177 (_PATIENT_WORDS, complain\\w*); flags.py:46 and flags.py:125 use the result as source_kind. git show --stat dd545e3 touches no app/backend file. Card AC2 done=false.",
   "why_it_matters": "D-033 (ORCHESTRATOR_DECISIONS.md:41) says EMS, witness and spouse/family statements are not patient self-report and calls the mislabel a credibility error. Production contradicts that recorded decision on four live phrasings, and the chip tells the reader the claimant said it. T-036 r3 rated the same behaviour major; D-033 now makes it a spec violation, so it is a blocker.",
   "fix": "In grounding.has_self_report: replace _SELF and _PATIENT_WORDS with 'any lexicon self_report hit AND NOT self_report_scope.exclude_sentence' (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Mark the intake date self_report false (done in lexicon) and delete _NOT_PATIENT_STATEMENT (grounding.py:175). Fix finding 3 in the same change.",
   "acceptance_test": "has_self_report False for 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'EMS reports neck pain 7/10.', 'Wife reports he was in pain.', 'Date of accident per intake form: 2026-01-19.'; True for 'Patient states pain began after the collision.', 'Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient-reported neck pain 7/10.'; grep -n '_SELF\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT' app/backend/grounding.py returns nothing."},
  {"severity": "major",
   "title": "Commit leaves test_flags_pass.py red (regression from parent): stale r2 assertion on 'Subjective:' header",
   "evidence": "'.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2' -> '1 failed, 113 passed, 699 deselected' (live, equal to dd545e3). Same subset on git archive 099732b -> '114 passed, 697 deselected'. Failing test tests/unit/test_flags_pass.py:114-121, assertion at :121, yes-list entry 'Subjective: neck pain 7/10.' (probe row: record). Full-suite FAILED-list diff against parent: only this test (artifacts/review-evidence/T-061-base-failed.txt vs T-061-head-failed.txt). Card evidence line does not mention a pytest run.",
   "why_it_matters": "The lexicon change flipped a tested behaviour and the test was not updated, so the commit is red on the flag suite it touches. The stale assertion would hide the next regression. The card's evidence cites only selfcheck and golden runs.",
   "fix": "Update the yes/no lists in test_flags_pass.py to D-033 (bare Subjective:/S: header is record; Patient-reported stays patient) and add the AC2 tests from finding 1 in the same file. Report the pytest subset result in the card evidence.",
   "acceptance_test": "'.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\"' reports 0 failed; the full tests/unit FAILED list contains no test that is absent from the parent archive."},
  {"severity": "major",
   "title": "exclude_sentence drops explicit patient statements when a family or EMS word and a speech verb share the sentence",
   "evidence": "artifacts/review-evidence/T-061-probe.txt: 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' -> lexicon(scope-aware)=record (expect patient). Cause: app/llm/lexicon.yaml:89 exclude_sentence matches a non-patient name, up to 3 words, then a speech verb anywhere in the sentence (not at the grammatical subject). evals/lexicon_heldout.jsonl: no probe pairs a patient subject with a family/EMS word (grep).",
   "why_it_matters": "D-033 keeps patient-quoted speech as patient_report. The exclusion removes the patient's own attribution on a sentence the patient authored. It is latent today because production does not read exclude_sentence, and it becomes live when AC2 is fixed as finding 1 requires. Selfcheck PASS cannot show it because the held-out set has no such case.",
   "fix": "Anchor the exclusion to the sentence subject (sentence-initial 'EMS|Wife|Witness|Family ... <verb>' or a 'Per <non-patient>' clause) and never exclude a sentence that starts with or names Patient/Pt/C/O. Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.",
   "acceptance_test": "'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' are patient_report; 'EMS reports minimal damage.', 'Wife complains of neck pain.', 'Per his wife, headaches began at the scene.' stay record; .venv/bin/python research/lexicon_selfcheck.py still PASS."},
  {"severity": "minor",
   "title": "Spec text still states the superseded rule (DECISIONS.md:286, lexicon.yaml:25-26)",
   "evidence": "memory/DECISIONS.md:286: '`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26: 'code sets source_kind = \"patient_report\" from it (ADR-013)'. D-033 (ORCHESTRATOR_DECISIONS.md:41) says it 'Narrows ADR-013 / DECISIONS.md:286'.",
   "why_it_matters": "AC3's 'or' clause is met by D-033, but the contract text now omits the exclusion rule that the code applies. A future reader gets two rules.",
   "fix": "Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'. Then set card AC3 done.",
   "acceptance_test": "grep -n 'set by code from the lexicon' memory/DECISIONS.md shows the amended text; the header in lexicon.yaml:25-26 names self_report_scope."}
 ],
 "whats_right": [
  "Lexicon scope works on the brief's non-patient sentences: 'Wife reports he has been irritable.', 'Per EMS, pt ambulatory at scene.', 'Witness states the car ran the light.' and 'S: neck pain' are record, and 'Patient states pain began after the collision.' is patient_report in both lexicon and production.",
  "Intake date is self_report: false (lexicon.yaml:775) and production gives record for 'Date of accident per intake form: 2026-01-19.'; no excerpt text is altered in any probe.",
  "Selfcheck, held-out 115/115 and golden MUST 11/11 all pass on the commit."
 ],
 "questions_for_chris": [
  "D-033 makes a bare 'S:' or 'Subjective:' header record, not patient self-report. In a SOAP note that header marks the patient's report. I accept D-033, but confirm you want the chip off those lines, since the subjective-only weight they carry is what a defense adjuster would use.",
  "Is 'Patient-reported' an explicit patient attribution for D-033? I counted it as patient_report (production and lexicon agree); D-033 does not name it.",
  "The persona file expects model claude-opus-5-5 in the review record; I ran as claude-haiku-5-5 and wrote that id. Confirm that is acceptable for the gate."
 ]}
```
