# T-091 review: claims-adjuster-reviewer (Gary Pruitt, defense BI adjuster)

Verdict: **fail**. I wrote 200 fresh attack sentences plus 50 genuine patient statements
(`artifacts/review-evidence/T-091/attacks.jsonl`, built by `build_attacks.py`, run by `probe.py`). `speaker.py` at 17cc9c7 labels
**110 of the 200 attacks "patient"** where a human reads "other" or "unknown". After I drop 13 rows that are arguable
(he/she/they pronouns, "Patient notes:", a nonsense token) the count is **97 of 200**. The gate is 100%, so the misses are blockers.
A second generated grid (patient head x 12 connectors x 12 unattributed clauses, `grid_and_corpus.py`) labels 432 of 468 "patient".
The worker's 310 rows contain none of these shapes (counted with a script: "advised", "informed", "described as", "noted to",
"responds", "Patient state:", "Patient records", "Pt Notes", "airbags", "gait steady", "I felt", "ER felt" each appear in 0 rows).
That is what a set written by the parser's author looks like. ENABLED stays False, which honours the AC ("otherwise stays off"),
so nothing ships wrong today. But the card claims a gate, and the gate does not hold against a fresh adversary.

Usefulness (the other half of the question): on my 50 genuine statements it labels 34 (68%); on the 23 repo-record sentences
that start "Patient/Pt + reporting verb" (evals/golden, evals/library) it labels 15 (65%). It misses the Appendix A sentence itself:
`Patient states symptoms began after the January collision.` -> unknown (a month name is outside the vocabulary).
It also misses "Patient states she missed two physical therapy visits in May." and "Patient denies chest pain or shortness of breath."

## Why it fails (mechanism, with locations)
- `_SAY_PATIENT` (speaker.py:86) keeps passive and description verbs: advised, told, informed, described, noted, reported,
  documented, recorded, thought, believed, said, responds, records, documents, state, note. The head test (`_head`, ~304) only checks
  "Patient + verb". Whether the patient is the speaker or the one being spoken to is never asked.
- A clause with no head inherits the current speaker if all its words are in the closed vocabulary (`_classify_sentence` ~368:
  `if not _complement_ok(toks, cur, False): ... ; continue`). So "; airbags deployed", "- alert and oriented", "\nGait steady" ride
  under the patient label. D-037 said "no further clause after ; , and or (" gets no chip, and D-040 recorded that this exact
  rule failed four rounds. v2 re-opened it with a vocabulary instead of a connector list.
- The "closed" vocabulary (`_BASE`, :170) contains the pronouns he/she/they/I/we/you (`_COMMON` :106) and institutional nouns
  er/ed/hospital/clinic/office/work/home (`_EVENT` :135), so a clause whose subject is one of those, with a vocabulary verb
  (felt, seemed, took, walked), is "the patient".

## Findings (JSON below holds the same, with fixes)
1. Blocker: patient as receiver or as the described party (30 attacks). "Patient advised to rest and ice.", "Patient told it was a strain.",
   "Patient responds well to therapy." (clinician assessment), "Patient described as anxious.", "Patient noted to have mild neck tenderness.",
   "Patient said to be fine.", "Patient recorded as ambulatory." All -> patient.
2. Blocker: unattributed observation clause under a patient head (about 50 attacks; grid 432/468). "Patient reports neck pain; airbags deployed.",
   "Patient denies loss of consciousness; alert and oriented.", "Patient states neck pain; gait steady.",
   "Patient reports neck pain\nAlert and oriented\nAmbulatory at scene". Every connector except an ellipsis leaks.
   For a MIST defense this is the worst direction: EMS/police scene facts (minimal damage, ambulatory at scene) get stamped as the claimant's words.
3. Blocker: "state/records/notes/report" as a noun or title (9 + 7 attacks). "Patient state: alert and oriented.",
   "Patient records: neck pain, headaches, nausea.", "Pt Notes: neck pain 5/10." (a physical therapy note), "Pt. Note: pain 4/10, stable, no distress."
   Uppercase "PT" is guarded (good); title-case "Pt Notes:" is the way a PT note is actually typed after OCR and is not.
4. Blocker: pronoun, first person, or institution as the speaker of a continuation (about 22 attacks).
   "Patient states neck pain; I felt a spasm.", "...; we walked to the car.", "...; I took her to the ER.",
   "Patient reports neck pain; ER felt it was a sprain.", "...; the hospital felt it was fine."
5. Major: the adversarial gate is not independent and not complete. The set and parser share an author, and the grid in
   `test_generated_mixed_grid_never_patient_or_other` only varies a second speaker with a speech verb, never an unattributed
   vocabulary-only clause. A 100% score on it measures recall of the author's list. Needed: a held-out set the parser's author never sees.
6. Minor: "other" is also a guess. "Driver states neck pain.", "Passenger reports neck pain.", "Driver denies loss of consciousness."
   are labelled other; in a crash file the claimant is very often the driver or passenger. Not shipped (chip_label returns None for
   non-patient), but the module docstring defines "other" as a named non-patient source.
7. Minor: usefulness 65-68%, and the first sentence a paralegal will test (Appendix A: "Patient states symptoms began after the January collision.")
   gets no label. Safe direction, but record it so nobody advertises the coverage.

## Things I checked that held
- Mixed speakers with a speech verb ("Patient states neck pain; wife reports headaches", "Per wife, patient states ...", Spanish "esposa refiere ...") -> unknown, across 40 new shapes.
- "Patient states his wife said he was fine" style hearsay keeps the patient label and nested patient-in-wife statements go unknown.
- Uppercase "PT reports ..." and "PT states pt reports ..." -> unknown.

## Exercised
`git rev-parse HEAD` = 02ff244; `git diff --quiet 17cc9c7 -- app/backend/speaker.py evals/adversarial/speaker_attribution.jsonl` printed "same"
(reviewed commit equals worktree for these files). `.venv/bin/python -m pytest tests/unit/test_speaker.py -q` -> 8 passed.
`probe.py` output: "attack rows 200; tool says PATIENT where a human reads other/unknown: 110"; "genuine patient statements: 50; labelled patient 34 (68%)".
`grid_and_corpus.py` output: "GRID unattributed clause: 432/468 labelled patient"; "REPO corpus: 31 ... starting with Patient/Pt: 23; ... patient share 65%".
`grep -rn "import speaker"` over app/tests/tools: only tests/unit/test_speaker.py imports it (module is not wired).

```json
{"card": "T-091", "persona": "claims-adjuster-reviewer", "model": "claude-sonnet-5-5",
 "scope": "app/backend/speaker.py and evals/adversarial/speaker_attribution.jsonl at 17cc9c7 (worktree identical); attack set artifacts/review-evidence/T-091/attacks.jsonl (200 attacks + 50 genuine); no app server needed, module is not wired",
 "exercised": ["python3 tools/board.py show T-091", "read D-035/D-037/D-040/D-042 in memory/ORCHESTRATOR_DECISIONS.md", "read app/backend/speaker.py in full", "pytest tests/unit/test_speaker.py -> 8 passed", "build_attacks.py + probe.py: 200 attacks, 110 labelled patient (97 after removing 13 arguable rows), 50 genuine, 34 labelled patient", "grid_and_corpus.py: 432/468 grid leak; 15/23 repo record sentences labelled patient", "counted worker set coverage of my hole classes: 0 rows each"],
 "verdict": "fail",
 "scores": {"safety_of_patient_label": 1, "adversarial_gate_validity": 1, "usefulness": 3, "fail_closed_design": 2, "consistency_with_D-037_D-040": 1},
 "findings": [
  {"severity": "blocker", "title": "Patient as receiver or described party is labelled patient (30 of 32 attacks)",
   "evidence": "attacks.jsonl CA-001 'Patient advised to rest and ice.' -> patient; CA-003 'Patient told it was a strain.'; CA-016 'Patient described as anxious.'; CA-019 'Patient noted to have mild neck tenderness.'; CA-026 'Patient said to be fine.'; CA-028 'Patient responds well to therapy.'; CA-025 'Patient recorded as ambulatory.'. Cause app/backend/speaker.py:86 _SAY_PATIENT keeps advised/told/informed/described/noted/reported/documented/recorded/thought/believed/said/responds; _head (~304) tests only 'Patient + verb'.",
   "why_it_matters": "Clinician advice and clinician assessment are printed as the claimant's own words. A defense reader cites it to say the claimant said 'responds well to therapy'. Invented attribution is a section 5 dealbreaker.",
   "fix": "Patient head requires an active reporting verb followed by a finite clause or noun phrase; a verb followed by 'to + verb', 'as', 'by', or 'to be' means the patient is the object, so unknown. Remove advised/told/informed/responds/documented/recorded/thought/believed/said from the patient verb list, or require a following 'that' or a symptom noun directly after the verb.",
   "acceptance_test": "All 30 rows of groups receiver_told_advised and description_by_someone_else in attacks.jsonl label unknown; held-out set of at least 100 such shapes at 100%."},
  {"severity": "blocker", "title": "Unattributed vocabulary-only clause after a patient head inherits the patient label (grid 432/468)",
   "evidence": "CA-053 'Patient reports neck pain; airbags deployed.' -> patient; CA-057 'Patient denies loss of consciousness; alert and oriented.'; CA-059 'Patient states neck pain; gait steady.'; CA-088 'Patient reports neck pain\\nAlert and oriented\\nAmbulatory at scene'; CA-079 'Patient states neck pain (gait steady, no distress).'. grid_and_corpus.py: 'GRID unattributed clause: 432/468 labelled patient' (every connector except an ellipsis, all 12 observation clauses). Cause speaker.py _classify_sentence ~368: a headless segment continues the current speaker if its words are in _BASE.",
   "why_it_matters": "EMS, police and examiner observations (airbags deployed, vehicle damage minimal, ambulatory at scene, no distress) become the claimant's statement. This is D-037's 'any further clause means no chip' rule, which D-040 says failed four rounds, re-opened through a vocabulary.",
   "fix": "A clause that has no explicit head of its own gets no speaker. Only an unbroken single clause 'Patient <verb> <complement>' (no ; , : - ( & / and but while or newline) is patient; a list of symptoms joined by 'and' or commas inside the complement is allowed only when every item is a symptom/body noun phrase, not a state or exam adjective.",
   "acceptance_test": "Rows in groups unattributed_observation_* in attacks.jsonl and the 468-cell grid all unknown; adversarial runner includes the grid."},
  {"severity": "blocker", "title": "'state/records/notes/report' used as a noun or title is read as a patient speech verb ('Pt Notes:' is a physical therapy note)",
   "evidence": "CA-033 'Patient state: alert and oriented.' -> patient; CA-036 'Patient records: neck pain, headaches, nausea.' -> patient; CA-038 'Patient documents: neck pain.' -> patient; CA-042 'Pt Notes: neck pain 5/10.' -> patient; CA-043 'Pt. Notes: neck pain 5/10.'; CA-046 'Pt Report: neck pain 5/10, headaches.'; CA-052 'Pt. Note: pain 4/10, stable, no distress.'. Uppercase PT is guarded at speaker.py:189 but title-case Pt is not.",
   "why_it_matters": "A physical-therapist's note or a chart heading is printed as the patient speaking. 'Patient state: alert and oriented' is a clinician observation.",
   "fix": "A label ending in ':' or '-' directly after Pt/Patient + noun-capable word (state, note, notes, record, records, report, document) is never a head; require a content word, not a delimiter, after the verb. Treat title-case 'Pt Notes/Note/Report/Eval' as ambiguous like uppercase PT.",
   "acceptance_test": "Groups noun_use_of_verb (excluding the 4 arguable rows) and pt_title_case_physical_therapy label unknown."},
  {"severity": "blocker", "title": "Pronoun, first person or an institution word as subject of a continuation is read as the patient",
   "evidence": "CA-102 'Patient states neck pain; I felt a spasm.' -> patient; CA-104 'Patient states neck pain; we walked to the car.'; CA-112 'Patient reports neck pain; I took her to the ER.'; CA-114 'Patient reports neck pain; ER felt it was a sprain.'; CA-116 'Patient states neck pain; the hospital felt it was fine.'; CA-117 '...; clinic felt it was a sprain.'. Cause speaker.py:106 _COMMON includes he she they i we you; :135 _EVENT includes er ed hospital clinic office work home.",
   "why_it_matters": "A clinician's first-person exam note and an institution's opinion are stamped as the claimant's words.",
   "fix": "Remove subject pronouns and institution nouns from the continuation vocabulary (allow them only inside a single patient clause as an object/location), and treat any subject in a continuation as a new unknown speaker.",
   "acceptance_test": "Groups pronoun_continuation (excluding the 8 arguable he/she/they rows) and vocab_word_as_source label unknown."},
  {"severity": "major", "title": "The 100% gate is self-authored and does not cover these hole classes",
   "evidence": "Counted in evals/adversarial/speaker_attribution.jsonl with a script: rows containing advised 0, informed 0, 'described as' 0, 'noted to' 0, responds 0, 'Patient state:' 0, 'Patient records' 0, 'Pt Notes' 0, airbags 0, 'I felt' 0, 'ER felt' 0. tests/unit/test_speaker.py::test_generated_mixed_grid_never_patient_or_other varies only a second speaker plus a speech verb. Handoff admits 'the set and parser share an author'.",
   "why_it_matters": "310/310 measures the author's list. A fresh reviewer's 200 sentences scored 90 correct (45%). The same pattern ended the T-061 chip in four rounds.",
   "fix": "Add all of attacks.jsonl to evals/adversarial/ as a held-out file the parser's author does not read before tuning; add grid cells for unattributed clauses, passive verbs and noun-use heads; report the score on the held-out file in the handoff.",
   "acceptance_test": "A new fresh adversary round (not the author, not this reviewer) of at least 100 sentences scores 0 patient misses before ENABLED can flip."},
  {"severity": "minor", "title": "'other' is a guess for Driver/Passenger, who is often the claimant",
   "evidence": "CA-170 'Driver states neck pain.' -> other; CA-171 'Driver states he was stopped at a red light.' -> other; CA-172 'Passenger reports neck pain.' -> other; CA-174 'Driver denies loss of consciousness.' -> other. speaker.py:67-75 _SRC lists driver, passenger, driver as non-patient sources.",
   "why_it_matters": "If a UI ever shows 'non-patient speaker' for these it states a fact the record does not. Not shipped today (chip_label returns None for non-patient).",
   "fix": "Drop driver and passenger (and occupant) from _SRC so they give unknown, or label the result 'third party or patient'.",
   "acceptance_test": "Group other_may_be_the_patient labels unknown."},
  {"severity": "minor", "title": "Coverage is about two thirds of genuine patient statements, and the Appendix A sentence is not labelled",
   "evidence": "probe.py: 'genuine patient statements: 50; labelled patient 34 (68%)'; grid_and_corpus.py: 'starting with Patient/Pt: 23; labels {patient: 15, unknown: 8} patient share 65%'; 'Patient states symptoms began after the January collision.' -> unknown (CA-201); 'Patient states she missed two physical therapy visits in May.' -> unknown.",
   "why_it_matters": "Safe direction, but the handoff's 28 of 226 and my 65-68% both mean the chip would be absent on common sentences, so adopting it for usefulness is weak.",
   "fix": "Accept numbers and month names, and plural nouns of already-listed words in the vocabulary, only after the blockers are closed; do not widen the vocabulary first.",
   "acceptance_test": "State coverage on the 23 record sentences in the handoff next to the safety score; target at least 80% after safety fixes."}
 ],
 "whats_right": ["Fail-closed default and ENABLED=False with chip_label() returning None keep nothing wrong on screen today.", "Mixed speakers joined by a speech verb (wife/EMS/officer/Spanish esposa) are reliably unknown across 40 new shapes.", "Uppercase PT and zero-width/homoglyph tricks are handled."],
 "questions_for_chris": ["D-042 says speaker attribution ships only at 100% on an adversarial set. Should that set be the held-out file from a reviewer round, so the worker never tunes against it?"]}
```
