# T-143 review (legal-nurse-reviewer, also covering the staff-engineer lens)

**Verdict: changes.** No blocker, three majors.

The list does what the card names. On `git archive` copies of 225e666 and HEAD (137ae87) I confirmed the following.
- lib09 r6 `Pain 5/10.`, the lib09 r2 chief complaint and case_06 r3 `History: occasional stiffness in the mornings at baseline.` are all listed.
- Every item is a verbatim slice. I asserted `record.text[start-char_start:end-char_start] == text` over sample, lib09, lib01, lib11, lib13, lib14, case_06 and case_08.
- Nothing listed appears in the letter. For lib09, "Pain 5/10", "No [X]" and "Motivo" are all absent from `/export`.
- Billing rates do not resurface. lib09 r2 `Consulta: $650.00.`, lib09 r2 `Costo por sesión...`, lib09 r7 and the lib11 r9 ledger are all unlisted.

Three things cost the verdict.

1. **Major: the administrative filter silently removes clinical sentences, including treatment and pain scores.**
   - `_BILLING` contains the bare word `adjustment`, `balance` and `charges?`. `_SIGNATURE` contains the bare word `signed`.
   - lib14 (chiropractic) records the treatment as `[X] adjustment [X] e-stim [X] hot pack.` `is_administrative` returns True for it, so an uncovered chiropractic treatment line vanishes with no trace. This is the failure the card exists to stop.
   - `Spinal adjustment performed, pain 4/10.` is marked administrative, so its pain score is lost.
   - `Chiropractic adjustment to cervical spine.` and `Patient signed consent for cervical injection.` are also marked administrative.
   - No test covers a clinical sentence that contains one of these words.

2. **Major: recall is narrow, and the narrow part is what a nurse reads for.**
   - The kinds are only a number, a body part, a hand-picked term, or a negation.
   - These are not listed, and no entry quote covers them in the cases shown:
     - lib09 r1 `Patient states she was struck by a car while walking in a parking lot.` (patient-stated mechanism and causation, checklist item 8). The r1 entry quote is only the shoulder pain, X-ray, Dx and ED charge sentences.
     - lib11 r2 `Passenger vehicle struck from behind.`
     - lib09 r1, r3 and r6 interpreter and history-source lines. The original GATE finding cited them.
     - lib11 r5 `Patient referred by attorney.`
   - Probes of `clinical_kinds` returned `[]` for the following:
     - `Patient states symptoms began after the January collision.`
     - `Hx of hypertension and diabetes.`
     - `Prior similar episode last year.`
     - `Gait antalgic.`
     - `Sensation intact.`
     - `Neuro intact.`
     - `BP 120/80, HR 72.`
     - `Meds: lisinopril, metformin.`
     - `Off work for two weeks.`
     - `Paciente refiere que los síntomas comenzaron después del choque.`
   - The prior-history, causation and self-report lexicon categories already exist, but this module does not use them.
   - api.md does not tell the paralegal which kinds of sentence are out of scope. The list can therefore look complete when it is not.

3. **Major: the commit does not reproduce the card's "38 pass" claim.**
   - Commit 225e666 swept in another worker's hunk. `present.py:317` calls `conflict_candidates.checks()`, which does not exist in HEAD (`git show HEAD:app/backend/conflict_candidates.py | grep -c "def checks"` returns 0).
   - On `git archive HEAD`, `GET /api/cases/{token}` returns `{'error': {'code': 'internal'...}}` with `unhandled AttributeError`.
   - `tests/unit/test_uncovered.py` gives `2 failed, 36 passed`: `test_api_lib09_and_case_06` and `test_api_every_item_is_a_verbatim_uncovered_slice_and_not_in_the_letter`.
   - After I added a stub `checks()` in my copy only, it gave `38 passed`.
   - I rated this major and not blocker for two reasons. The dependency is another worker's uncommitted file, and the handoff discloses it.
   - Separately, the shared index currently shows `D  app/backend/uncovered.py` (a staged deletion). I did not touch it.

Minors are in the JSON below: the orphaned form answer, English billing words missing, term lists in code, and weak tests.

**Code and mutation testing.** I made 20 mutants in a copy. 17 were killed and 2 are equivalent mutants (touching spans; the no-body skip, which `quote_body` already covers). One real survivor: the `, MD` signature suffix has no test. One mutant did not apply. The code is short and readable. `attach` and `for_record` have a clear split, and offsets are applied once, in `attach`. The weak spots are in the findings.

**Exercised.**
- `git archive` copies of 225e666 and HEAD.
- `tests/unit/test_uncovered.py` (38 pass with the stub, 2 fail without it).
- The API via TestClient on the fixture backend: sample, lib01/02/03/04/05/08/09/11/13/14, case_06 and case_08.
- Per-sentence dumps comparing entry quotes against the list.
- A 50-sentence probe of `is_administrative` and `clinical_kinds`.
- The 20-mutant run.

```json
{"card": "T-143", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "225e666 and HEAD 137ae87: app/backend/uncovered.py, present.py wiring, memory/contracts/api.md T-143 paragraph, tests/unit/test_uncovered.py; git archive copies in the scratchpad (t143); TestClient on LLM_BACKEND=fixture; sample, lib01-05/08/09/11/13/14, case_06, case_08",
 "exercised": ["git archive 225e666 and HEAD; tests/unit/test_uncovered.py (HEAD: 2 failed 36 passed; with a stub checks(): 38 passed)", "GET case via TestClient on the sample, lib01/02/03/04/05/08/09/11/13/14, case_06 and case_08, with per-sentence coverage dumps and a start/end slice assertion", "/export letter text checked for listed sentences on lib09", "50-sentence probe of is_administrative and clinical_kinds", "20-mutant run on uncovered.py (17 killed, 2 equivalent, 1 real survivor, 1 did not apply)", "board.py show T-143; reviews/GATE-M2-legal-nurse.md major 2; read api.md paragraph and the T-105 precedent"],
 "verdict": "changes",
 "scores": {"covers_the_three_named_examples": 5, "recall_of_clinical_sentences": 2, "noise_and_billing_exclusion": 3, "quote_and_offset_fidelity": 5, "letter_isolation": 5, "code_quality": 3, "test_strength": 3, "commit_reproducibility": 2},
 "findings": [
  {"severity": "major", "title": "Administrative filter suppresses clinical sentences (chiropractic adjustment, balance, signed consent), including a pain score",
   "evidence": "app/backend/uncovered.py _BILLING contains bare 'adjustment' and 'balance'; _SIGNATURE contains bare 'signed'. Probe: is_administrative('[X] adjustment [X] e-stim [X] hot pack.') True (the lib14 chiropractic treatment line); is_administrative('Spinal adjustment performed, pain 4/10.') True; is_administrative('Chiropractic adjustment to cervical spine.') True; is_administrative('Patient signed consent for cervical injection.') True; is_administrative('Balance impaired on tandem gait.') True. No test in tests/unit/test_uncovered.py uses a clinical sentence containing these words.",
   "why_it_matters": "An uncovered treatment line or pain score vanishes from the letter with no trace and the list stays silent. That is the original GATE-M2 failure, now hidden by the filter meant to remove billing noise.",
   "fix": "Make the administrative test need money or billing context, not a bare word: 'adjustment' only with a dollar or negative amount; 'balance' only as 'balance due/forward/remaining'; 'signed' only as 'signed by', 'electronically signed' or a signature line. Apply is_administrative only when the sentence has no pain score and no clinical kind, or re-check kinds first for sentences that carry a number/10.",
   "acceptance_test": "Unit cases: '[X] adjustment [X] e-stim [X] hot pack.', 'Spinal adjustment performed, pain 4/10.', 'Balance impaired on tandem gait.', 'Patient signed consent for cervical injection.' are listed when uncovered; 'Adjustment (courtesy discount) -$274.00.', 'Balance due $2,166.00.', 'Electronically signed by J. Smith, MD' stay skipped."},
  {"severity": "major", "title": "Recall misses patient-stated mechanism and onset, prior history without a listed term, exam findings, work status, medications and interpreter lines",
   "evidence": "Real records: lib09 r1 'Patient states she was struck by a car while walking in a parking lot.' (r1 entry quote is 'Left shoulder pain 7/10. X-ray left shoulder negative for fracture. Dx: left shoulder contusion. ED charge: $2,940.') is neither covered nor listed; lib11 r2 'Passenger vehicle struck from behind.' and r5 'Patient referred by attorney.' unlisted; lib09 r1/r3/r6 interpreter and 'Hx obtained via patient's son, who interpreted.' unlisted. Probe clinical_kinds()==[] for: 'Patient states symptoms began after the January collision.', 'Hx of hypertension and diabetes.', 'Prior similar episode last year.', 'Gait antalgic.', 'Sensation intact.', 'Neuro intact.', 'BP 120/80, HR 72.', 'Meds: lisinopril, metformin.', 'Off work for two weeks.', 'Paciente refiere que los síntomas comenzaron después del choque.'. The module's term list (uncovered.py _CLINICAL_TERM) has no history, causation, self-report, exam, vitals or medication vocabulary.",
   "why_it_matters": "Patient-stated causation and onset (checklist 8), prior history (checklist 9) and who gave the history are exactly what a nurse reviewer reads for. They disappear while the panel says nothing, and a sentence the entry left out looks like one the record never had. api.md does not warn that these kinds are out of scope.",
   "fix": "Add kinds fed from the existing lexicon categories (pre_existing, causation, self_report, via grounding.view) plus a small exam/vitals/medication/work-status/informant set. At minimum list any sentence that starts 'Patient states/reports/denies/refers' or 'Paciente refiere/niega'. State in api.md which kinds are not covered.",
   "acceptance_test": "Unit and API tests: lib09 r1 'Patient states she was struck by a car...' and 'Hx obtained via patient's son, who interpreted.' appear in uncovered; lib11 r2 'Passenger vehicle struck from behind.' appears; 'Patient states symptoms began after the January collision.' is listed when no entry quotes it; the sample case list stays unchanged except for the already-listed r3 prior-history sentence."},
  {"severity": "major", "title": "Commit 225e666 is not self-consistent: GET case errors on HEAD and 2 of the 38 tests fail",
   "evidence": "present.py:317 (HEAD) calls conflict_candidates.checks(); git show HEAD:app/backend/conflict_candidates.py | grep -c 'def checks' -> 0 (the function exists only in the dirty working tree, conflict_candidates.py:244). git archive HEAD + pytest tests/unit/test_uncovered.py -> 'FAILED test_api_lib09_and_case_06 - KeyError: 'records'' and 'FAILED test_api_every_item_is_a_verbatim_uncovered_slice_and_not_in_the_letter', '2 failed, 36 passed'; log 'unhandled AttributeError', case = {'error': {'code': 'internal'}}. With a stub checks() added in my copy: 38 passed. git status in the shared repo shows 'D  app/backend/uncovered.py' staged (index deletion).",
   "why_it_matters": "The card's evidence ('38 pass') cannot be reproduced from the commit. At that commit the whole case endpoint returns an internal error, so T-143 cannot be exercised there. The handoff discloses the cause, but a done card must be reproducible from the commit.",
   "fix": "Land the conflict_candidates.checks() change in its owner's commit, or take the 'checks' hunk out of present.py until then. Re-run test_uncovered.py on a git archive of the final commit and record that run as evidence. Unstage the stray deletion of uncovered.py.",
   "acceptance_test": "git archive <final commit> | tar -x; pytest tests/unit/test_uncovered.py -> 38 passed, and GET /api/cases/{token} returns 200 with records[].uncovered present."},
  {"severity": "minor", "title": "A form answer is listed without its question",
   "evidence": "lib09 r4 'Accidentes anteriores? Si [ ] No [X].' splits at '?'. The listed item is only 'Si [ ] No [X].' (kinds negation); 'Accidentes anteriores?' is unlisted. The r4 entry quote is 'Motivo de la visita: dolor de espaIda y hombro derecho.'",
   "why_it_matters": "The verbatim sentence is correct but means nothing alone. The reader cannot tell what 'No' denies, and this is the prior-accident denial.",
   "fix": "When a listed sentence is a checkbox or short answer (starts with Si/No/Yes/[ ]) and the previous sentence ends in '?', list the pair as one item, or add the question to the item text.",
   "acceptance_test": "lib09 r4 yields one item whose text includes 'Accidentes anteriores?' and 'No [X]', and the slice assertion still holds."},
  {"severity": "minor", "title": "Noise: legal and cost sentences without a dollar sign are listed",
   "evidence": "lib11 r4 listed 'Letter of protection to Fennimoor Spine Clinic.' (kind body_part from 'Spine'). Probes: 'Cost of cervical collar was covered.' and 'Paid for chiropractic care out of pocket.' are not administrative. _BILLING has Spanish 'costo/pago' but no English cost, paid, fee, owed or letter of protection.",
   "why_it_matters": "A cost or payment sentence listed beside clinical ones erodes trust in the list. Money amounts are already caught, so only wording without a figure leaks.",
   "fix": "Add English cost/paid/fee/owed/letter of protection/lien words to the billing cues, keeping the clinical-context guard from the first finding.",
   "acceptance_test": "Those three sentences are skipped; 'Pain 5/10.' and 'Rx ibuprofen 800 mg.' are still listed."},
  {"severity": "minor", "title": "Clinical vocabulary is hard-coded in uncovered.py, with no card to move it",
   "evidence": "uncovered.py _BODY, _CLINICAL_TERM, _NUMBER_UNITS, _NEGATION_ES, _SIGNATURE and _BILLING (about 25 lines of word lists) sit outside app/llm/lexicon.yaml. The T-105 precedent made the lexicon the single source for qualifier lists. The docstring says 'a card, not an edit here' but board.py list shows no researcher card for a body-part/diagnosis family; T-144 is the frontend card. The Spanish negation list duplicates what the Spanish module holds.",
   "why_it_matters": "A second vocabulary drifts from the first. It is also where the recall gaps above come from, and a researcher owns clinical terms.",
   "fix": "Open a researcher card for the lexicon family (body parts, exam findings, history/causation cues, billing cues) and have uncovered.py read it through grounding.view; until then, add a test that fails when a term list is added here.",
   "acceptance_test": "board.py list shows the researcher card; after it ships, uncovered.py contains no word lists beyond number patterns."},
  {"severity": "minor", "title": "Tests are weaker than they look",
   "evidence": "test_api_every_item_is_a_verbatim_uncovered_slice_and_not_in_the_letter asserts only 'uncovered' not in letter.lower(), the word and not the sentences. Mutant S (the ', MD' signature-suffix alternative removed) survived 38 tests. test_no_second_source_and_never_in_letter_or_notes_code greps four filenames for the string 'uncovered'. No test has a clinical sentence that contains an administrative word.",
   "why_it_matters": "The letter-isolation guarantee rests on a word search, and the false-suppression bug above went through all 38 tests.",
   "fix": "Assert that no listed sentence text appears in the export or the internal notes when no entry quotes it (lib09 gives this). Add a ', MD' case and the clinical-sentence-with-admin-word cases.",
   "acceptance_test": "Mutants S and 'adjustment treated as billing' are killed."}
 ],
 "whats_right": ["The three named examples (lib09 r6 'Pain 5/10.', lib09 r2 chief complaint, case_06 r3 baseline history) are listed with exact verbatim slices and correct offsets across ten cases.", "The list never reaches the letter, and billing amounts and ledger lines (lib09 r2/r7, lib11 r9) do not resurface.", "Mutation testing killed 17 of 20 mutants. Offsets are applied in one place (attach) and rejected entries do not cover."],
 "questions_for_chris": ["Should patient-stated mechanism and onset sentences ('struck by a car', 'symptoms began after the collision') belong in this list even when a causation flag may already quote them? I treated them as in scope."]}
```
