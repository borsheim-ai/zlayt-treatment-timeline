# T-061 round 2: self-report label precision, claims-adjuster review (Gary Pruitt)

Verdict: **fail** (2 blockers, 2 majors, 2 minors). Reviewed object: commit e1400d4 (backend round 2, on top of dd545e3). Git archive of e1400d4 and the live tree are identical for every reviewed file (grounding.py, flags.py, lexicon.yaml, test_flags_pass.py, research/lexicon_selfcheck.py). HEAD has since moved to 709397e; the live tree is still moving, so this review pins e1400d4.

Round 1 status (reviews/T-061-claims-adjuster.md):
- r1 blocker, EMS/witness/wife/family complaints labelled "Patient self-report": **closed for the phrasings r1 listed** (probe rows: 10/10 expected). The class is not closed: findings 1 and 2 below.
- r1 major, test_flags_pass.py red: **closed**. `-k "flag or lexicon"` gives 121 passed; full `tests/unit` gives 866 passed on the live tree.
- r1 major, over-exclusion of patient sentences naming EMS or a wife: **closed** for both r1 sentences (4/4 r1-f3 rows). Finding 3 is the mirror image.
- r1 minor, superseded spec text: **still open** (finding 5).

What e1400d4 does: `grounding._self_report` now returns True only when a lexicon self_report hit exists AND the hit's sentence does not match `self_report_scope.exclude_sentence` (grounding.py:188-197; lexicon.yaml:89). `_SELF`, `_PATIENT_WORDS` and `_NOT_PATIENT_STATEMENT` are gone (grep: none). `flags.py:46` and `flags.py:125` call `has_self_report`. The brief's six script-checks pass through the production constructor (6/6).

Findings:

1. **Blocker. Non-patient speakers in colon, abbreviation and long-subject forms are labelled patient_report.** Evidence: `artifacts/review-evidence/T-061-r2-probe.txt`, rows MISS:
   - `EMS: pt c/o neck pain.` gives patient_report.
   - `EMS: he complains of neck pain.` gives patient_report.
   - `Witness: patient states the car ran the light.` gives patient_report.
   - `Family: neck pain 7/10, C/O headache.` gives patient_report.
   - `Wife of 20 years and mother of two reports he complains of neck pain.` gives patient_report.
   - `Wife (Mrs. Ortiz) reports he complains of neck pain.` gives patient_report.
   Cause: lexicon.yaml:89 needs `\s+` directly after the speaker word, so a colon fails it, and it allows at most three words before the verb. grounding.py:177 `_SENT_END` splits at "Mrs."; for the Mrs. row the anchored sentence is ` Ortiz) reports he complains of neck pain`, and `excluded` is False (run on the e1400d4 archive).
   Why it matters: D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) says EMS narrative, witness and spouse/family statements are not patient self-report. The round-1 blocker was this same mislabel, and its acceptance list only covered the no-colon forms. The "EMS:" and "Witness:" speaker-label forms are standard in clinical notes, so the chip still tells the reader the claimant said what EMS or a witness said.
   Fix: anchor the exclusion to the clause, not to a whitespace-and-three-word window. Allow `:` or `-` after the speaker word and a parenthesised descriptor before the verb. Split sentences at abbreviations (Mr., Mrs., Ms., Dr., Pt.) before the anchor is applied.
   Acceptance test: the six rows above return record in flags._flag. `Patient states EMS noted a laceration.`, `Pt c/o neck pain; wife drove him in.` and `Patient states his wife drove him to the ER.` stay patient_report. `.venv/bin/python research/lexicon_selfcheck.py` still PASS.

2. **Blocker. A spouse or family clause inside a patient-subject sentence inherits "Patient self-report".** Evidence: probe row `C/O neck pain; wife reports headaches.` gives source_kind patient_report. The sentence contains a wife statement, and the excerpt carries the chip. The team's test `tests/unit/test_flags_pass.py:173-177` (test_d033_mixed_sentences_decide_per_sentence) pins per-sentence behaviour only with separate sentences, so the same-sentence case is not covered.
   Why it matters: D-033 says spouse and family statements are not patient self-report, and it names this exact error ("Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit"). The wife's headache complaint is quoted verbatim in an excerpt that tells the reader the claimant reported it.
   Fix: one boolean per excerpt cannot be right for a mixed excerpt. The architect chooses one of two. (a) Split the flag so each excerpt has one speaker; this is preferred. (b) Label any excerpt containing a non-patient speaker clause as record. Under (b) the patient's own clause loses its chip, which is finding 3's harm and which I accept as the lesser harm.
   Acceptance test: under (a), `C/O neck pain; wife reports headaches.` yields no patient_report flag whose text contains "wife reports headaches", and the "C/O neck pain" flag stays patient_report. Under (b), the same sentence yields record. test_flags_pass.py:173-177 is updated to match whichever is chosen.

3. **Major. A patient clause inside an EMS-subject sentence loses its attribution.** Evidence: probe row `EMS reports neck pain, patient states headaches.` gives record. The clause `patient states headaches` is explicit patient attribution (D-033 lists 'Patient states' as patient_report).
   Cause: lexicon.yaml:89 anchors on the sentence start `EMS reports` and excludes the whole sentence, so the patient clause is dropped (grounding.py:188-197).
   Why it matters: this is the opposite direction from round-1 finding 3. Under-attribution is the lesser harm, so this is major and not blocker. It is the same design gap as finding 2 and is resolved by the same choice: under (a) the patient clause gets its own flag.
   Fix: as finding 2. Acceptance test: under (a), `patient states headaches` is patient_report on its own flag. Under (b), the sentence is record and the trade-off is written into the D-entry.

4. **Major, pending Chris's ruling. Third-party speakers outside the closed list are labelled patient_report.** Evidence: probe rows `Girlfriend reports he complains of neck pain.`, `Co-worker reports patient c/o neck pain.` and `Passenger reports patient complains of neck pain.` all give patient_report. Several records pass only by accident: `Passenger reports patient complained of neck pain.` gives record only because 'complained' is not in patient_reports_generic (lexicon.yaml:754-755), and `Triage nurse reports he is in pain.` has no self_report hit at all. Neither result comes from the exclusion.
   Why it matters: the exclusion is a closed word list (lexicon.yaml:89). D-033's positive rule is that patient_report "applies only to explicit patient attribution". If that rule means the clause's speaker must be the patient or a quoted patient, these three rows are a blocker. If D-033's list (EMS, witness, spouse/family) is closed, they are not covered and need a ruling. I have rated this major and put the question to Chris.
   Fix: either state the rule as subject-based (the speaker of the clause is the patient or a quoted patient) and apply it to any speaker, or add the named speakers after a ruling. Acceptance test: the three rows return record, or Chris's ruling is written into D-033 and the test pins it.

5. **Minor. Spec text still states the superseded rule (round-1 finding 4, unchanged).** Evidence: memory/DECISIONS.md:286 reads "`source_kind = "patient_report"` is set by code from the lexicon `self_report` entries on the excerpt". app/llm/lexicon.yaml:25-26 reads "code sets source_kind = "patient_report" from it (ADR-013)". The exclusion rule appears only in the T-061 note at lexicon.yaml:84-87.
   Fix: architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to "self_report entries that name the patient, minus self_report_scope.exclude_sentence".
   Acceptance test: `grep -n "from the lexicon \`self_report\` entries on the excerpt" memory/DECISIONS.md` returns nothing, and the lexicon header names self_report_scope.

6. **Minor. The held-out set has no patient-subject sentence naming a family or EMS member (round-1 finding 3, coverage half).** Evidence: `grep -n -i` for a patient subject followed by EMS, wife, witness, family, husband or spouse in evals/lexicon_heldout.jsonl (115 rows) returns none. The unit test at test_flags_pass.py:179-187 covers it, so the regression is caught, but selfcheck PASS cannot show it.
   Fix: add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' to evals/lexicon_heldout.jsonl (researcher-owned).
   Acceptance test: both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report, and selfcheck PASS.

What is not a finding: `Per EMS, pt. c/o neck pain.` and `EMS noted pt. reports neck pain 7/10.` both give record. I expected the "pt." abbreviation to split the sentence, but the match starts at "pt. c/o", so the anchor still sees "Per EMS". Checked by running the function directly.

Outside my lens: the selfcheck's is_patient_statement reference implementation (I did not compare its output on the adversarial set); the rest of the test suite beyond the 866-pass count.

Exercised:
- Read personas/claims-adjuster.md (full); my memory index and the round-1 memory files; reviews/T-061-claims-adjuster.md (round 1, full); `python3 tools/board.py show T-061`; D-033 at memory/ORCHESTRATOR_DECISIONS.md:41.
- `.venv/bin/python research/lexicon_selfcheck.py | tail -3` gave `SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 115/115` and `RESULT: PASS`. A separate run with output to a file gave exit 0.
- `.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2` gave `121 passed, 745 deselected in 2.06s`. An earlier run in this review, at HEAD 4eebb2d, gave `120 passed, 731 deselected in 1.79s`; the count moved because the tree moved.
- `.venv/bin/python -m pytest tests/unit -q` gave `866 passed in 16.52s` (live tree).
- `git log --oneline -6`; `git show --stat e1400d4` (grounding.py, lexicon.yaml, test_flags_pass.py only); `git merge-base --is-ancestor dd545e3 HEAD` (ancestor); `git status --short -- app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py research evals app/llm` (no diffs on reviewed paths); `cmp` of the five reviewed files, live vs the e1400d4 archive (identical).
- `git archive e1400d4` extracted to the session scratchpad; the probe ran against that archive.
- `.venv/bin/python artifacts/review-evidence/T-061-r2-probe.py <archive>` gave `SUMMARY 31/42 match expected`, with brief 6/6, r1-acc 10/10, r1-f3 4/4, d033 3/3, adv 7/13, adv2 1/6. The probe calls flags._flag (flags.py:42, the constructor that sets source_kind at flags.py:46) and grounding.has_self_report. Output: `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-r2-probe.txt`.
- Ran `_sentence_around` and the exclusion regex directly on the three misses (Mrs., EMS colon, Family colon) to confirm the mechanism.
- `grep -n "_SELF\b\|_PATIENT_WORDS\|_NOT_PATIENT_STATEMENT" app/backend/grounding.py` gave no output. `grep -n` for "code sets source_kind" gave lexicon.yaml:84 and lines 25-26 (wrapped). DECISIONS.md:286 read with `sed`.
- `grep -n -i` on evals/lexicon_heldout.jsonl for patient-subject sentences naming EMS, wife, witness, family, husband or spouse: no output.
- Read tests/unit/test_flags_pass.py:95-190 and lexicon.yaml lines 23-27 and 82-93.

```json
{"card": "T-061", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
 "scope": "commit e1400d4 (T-061 round 2 backend: grounding.py, lexicon.yaml exclude_sentence, test_flags_pass.py), reviewed via git archive; live tree identical for those paths; HEAD 709397e not reviewed; spec memory/DECISIONS.md:286 and D-033 at memory/ORCHESTRATOR_DECISIONS.md:41; no app URL (flag and lexicon layer, no UI in scope); sample probes in artifacts/review-evidence/T-061-r2-probe.py.",
 "exercised": [
  "Read personas/claims-adjuster.md in full; memory index and round-1 memory files; reviews/T-061-claims-adjuster.md in full; python3 tools/board.py show T-061; D-033 (ORCHESTRATOR_DECISIONS.md:41)",
  ".venv/bin/python research/lexicon_selfcheck.py | tail -3 -> SUMMARY golden MUST 11/11, held-out 115/115, FN 1 of 140; RESULT: PASS; separate run exit 0",
  ".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon' 2>&1 | tail -2 -> 121 passed, 745 deselected",
  ".venv/bin/python -m pytest tests/unit -q -> 866 passed (live tree)",
  "git log --oneline -6; git show --stat e1400d4; git merge-base --is-ancestor dd545e3 HEAD; git status --short on reviewed paths (no diffs); cmp of five reviewed files live vs git archive e1400d4 (identical)",
  "git archive e1400d4 extracted to session scratchpad; artifacts/review-evidence/T-061-r2-probe.py run against it -> artifacts/review-evidence/T-061-r2-probe.txt (42 sentences through flags._flag and grounding.has_self_report: 31/42; 11 misses = findings 1-4)",
  "direct run of grounding._sentence_around and lexicon self_report_exclude on 'Wife (Mrs. Ortiz) reports he complains of neck pain.', 'EMS: he complains of neck pain.', 'Family: neck pain 7/10, C/O headache.'",
  "grep -n _SELF|_PATIENT_WORDS|_NOT_PATIENT_STATEMENT app/backend/grounding.py -> none; grep -n 'code sets source_kind' app/llm/lexicon.yaml -> 84 (+ wrapped 25-26); sed -n 286p memory/DECISIONS.md",
  "grep -n -i patient-subject + EMS/wife/witness/family/husband/spouse evals/lexicon_heldout.jsonl -> none (115 rows)",
  "read tests/unit/test_flags_pass.py:95-190 and app/llm/lexicon.yaml:23-27, 82-93, 488-493, 738-759"
 ],
 "verdict": "fail",
 "scores": {"attribution_precision_production": 2, "lexicon_scope_logic": 2, "ac2_flags_wiring": 4, "test_honesty": 3, "spec_consistency": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Non-patient speakers in colon, abbreviation and long-subject forms still labelled patient_report",
   "evidence": "artifacts/review-evidence/T-061-r2-probe.txt MISS rows: 'EMS: pt c/o neck pain.', 'EMS: he complains of neck pain.', 'Witness: patient states the car ran the light.', 'Family: neck pain 7/10, C/O headache.', 'Wife of 20 years and mother of two reports he complains of neck pain.', 'Wife (Mrs. Ortiz) reports he complains of neck pain.' each give source_kind patient_report. Cause: app/llm/lexicon.yaml:89 requires \\s+ directly after the speaker word (colon fails) and allows at most 3 words before the verb; app/backend/grounding.py:177 _SENT_END splits at 'Mrs.', so the anchored sentence is ' Ortiz) reports he complains of neck pain' and excluded is False (archive e1400d4).",
   "why_it_matters": "D-033 (memory/ORCHESTRATOR_DECISIONS.md:41) says EMS narrative, witness and spouse/family statements are not patient self-report. This is the round-1 blocker class in forms its acceptance list did not cover. The chip tells the reader the claimant said what EMS, a witness or a spouse said.",
   "fix": "Anchor the exclusion to the clause rather than a whitespace-and-3-word window: allow ':' or '-' after the speaker word and a parenthesised descriptor before the verb; split sentences at abbreviations (Mr., Mrs., Ms., Dr., Pt.) before the anchor.",
   "acceptance_test": "The six rows above return record via flags._flag. 'Patient states EMS noted a laceration.', 'Pt c/o neck pain; wife drove him in.' and 'Patient states his wife drove him to the ER.' stay patient_report. .venv/bin/python research/lexicon_selfcheck.py still PASS."},
  {"severity": "blocker",
   "title": "A spouse or family clause inside a patient-subject sentence inherits 'Patient self-report'",
   "evidence": "artifacts/review-evidence/T-061-r2-probe.txt: 'C/O neck pain; wife reports headaches.' gives source_kind patient_report. tests/unit/test_flags_pass.py:173-177 (test_d033_mixed_sentences_decide_per_sentence) pins per-sentence behaviour only for separate sentences.",
   "why_it_matters": "D-033 says spouse and family statements are not patient self-report and names this error: 'Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit.' The wife's headache complaint is quoted verbatim in an excerpt whose chip credits the claimant.",
   "fix": "Architect chooses: (a) split the flag so each excerpt has one speaker (preferred); or (b) label any excerpt containing a non-patient speaker clause as record, accepting that the patient clause loses its chip (finding 3).",
   "acceptance_test": "Under (a): 'C/O neck pain; wife reports headaches.' yields no patient_report flag whose text contains 'wife reports headaches', and the 'C/O neck pain' flag stays patient_report. Under (b): the sentence yields record. test_flags_pass.py:173-177 updated to the chosen rule."},
  {"severity": "major",
   "title": "A patient clause inside an EMS-subject sentence loses its attribution",
   "evidence": "artifacts/review-evidence/T-061-r2-probe.txt: 'EMS reports neck pain, patient states headaches.' gives record. Cause: app/llm/lexicon.yaml:89 anchors on the sentence start 'EMS reports' and excludes the whole sentence (grounding.py:188-197).",
   "why_it_matters": "Explicit patient attribution ('Patient states') is dropped. This is the opposite direction from round-1 finding 3; under-attribution is the lesser harm, so major and not blocker. Same design gap as finding 2.",
   "fix": "Resolved by the same choice as finding 2: under (a) the patient clause gets its own flag.",
   "acceptance_test": "Under (a): 'patient states headaches' is patient_report on its own flag. Under (b): the sentence is record and the trade-off is written into the D-entry."},
  {"severity": "major",
   "title": "Third-party speakers outside the closed word list are labelled patient_report (pending Chris's ruling)",
   "evidence": "artifacts/review-evidence/T-061-r2-probe.txt: 'Girlfriend reports he complains of neck pain.', 'Co-worker reports patient c/o neck pain.', 'Passenger reports patient complains of neck pain.' each give patient_report. lexicon.yaml:89 is a closed word list. 'Passenger reports patient complained of neck pain.' passes only because 'complained' is absent from patient_reports_generic (lexicon.yaml:754-755), not because of the exclusion.",
   "why_it_matters": "D-033 says patient_report 'applies only to explicit patient attribution'. If that means the clause's speaker must be the patient or a quoted patient, these rows are a blocker. If D-033's named list (EMS, witness, spouse/family) is closed, the question is open and needs a ruling.",
   "fix": "Either state the rule as subject-based and apply it to any speaker, or add named speakers after Chris's ruling and write it into D-033.",
   "acceptance_test": "The three rows return record, or Chris's ruling is in D-033 and the test pins it."},
  {"severity": "minor",
   "title": "Spec text still states the superseded rule (round-1 finding 4, unchanged)",
   "evidence": "memory/DECISIONS.md:286: '`source_kind = \\\"patient_report\\\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26: 'code sets source_kind = \\\"patient_report\\\" from it (ADR-013)'. The exclusion rule appears only in the T-061 note at lexicon.yaml:84-87.",
   "why_it_matters": "A future reader gets two rules: the spec says every self_report hit counts, and the code applies an exclusion the spec does not mention.",
   "fix": "Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'.",
   "acceptance_test": "grep for 'from the lexicon `self_report` entries on the excerpt' in memory/DECISIONS.md returns nothing; the lexicon header names self_report_scope."},
  {"severity": "minor",
   "title": "Held-out set has no patient-subject sentence naming a family or EMS member (round-1 finding 3, coverage half)",
   "evidence": "grep -n -i for patient subject + EMS/wife/witness/family/husband/spouse in evals/lexicon_heldout.jsonl (115 rows): no output. Unit test test_flags_pass.py:179-187 covers the case.",
   "why_it_matters": "The unit test catches a regression, but selfcheck PASS cannot show one, so the research gate is blind to this class.",
   "fix": "Add 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' to evals/lexicon_heldout.jsonl (researcher-owned).",
   "acceptance_test": "Both sentences appear in evals/lexicon_heldout.jsonl with expected patient_report, and selfcheck PASS."}
 ],
 "whats_right": [
  "Round-1 blocker phrasings are record through the production constructor: 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'Date of accident per intake form: 2026-01-19.' (10/10 r1 rows), and the brief's six script-checks pass (6/6).",
  "Round-1 over-exclusion is fixed: 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' stay patient_report, and the full tests/unit run is green at 866 passed.",
  "Bare 'S:', 'Subjective:' and 'Self-reported' headers are record, and the intake-form date is self_report: false, so the D-033 header rule holds with the verbatim marker still in the excerpt."
 ],
 "questions_for_chris": [
  "Is D-033's speaker list closed? Are a girlfriend or partner, a co-worker and a passenger 'family' or 'witness' for D-033 (finding 4)? If D-033 means the clause's speaker must be the patient, finding 4 is a blocker.",
  "For mixed excerpts (findings 2 and 3), do you prefer per-speaker flag splitting (a) or labelling mixed excerpts record (b), accepting that the patient clause loses its chip?",
  "The review object is e1400d4 via git archive, identical to the live tree for reviewed paths. HEAD is now 709397e and the live tree is moving (the -k count moved from 120 to 121 between two runs in this review). Should the gate review e1400d4 or a later commit?",
  "The persona file expects model claude-opus-5-5 in the review record. I ran as claude-haiku-5-5 and wrote that id, as in round 1. Confirm that is acceptable for the gate."
 ]}
```
