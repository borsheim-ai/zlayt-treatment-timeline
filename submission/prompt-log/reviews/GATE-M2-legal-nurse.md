# GATE-M2 review: legal-nurse-reviewer (Linda Chen, RN, LNC)

Pinned commit 0c24f5f, `git archive` copy in the scratchpad. App run with `ZLAYT_MODE=local`, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, port 7899, SQLite in the scratchpad. The server was stopped by PID (88848) and the port confirmed closed.

**Verdict: changes.** No blocker and two majors. I looked for the persona blockers and found none on the sample case or the two library cases. Specifically:
- No inferred diagnosis, severity or causation.
- "Concussion without loss of consciousness" is intact.
- The MRI hedge ("may represent degenerative change; correlate clinically") is intact in the summary and the letter.
- "MRI ordered" and "Recommend ... injection" are not reported as completed.
- Patient reports stay attributed ("C/O" became "complained of", "Patient states" is kept).
- "approx." is kept on 35 mph and 40%.
- The tool adds no subjective or objective labels.
- The sample matches every item in `spec/SAMPLE_CASE_TRUTHS.md`: 73-day gap flagged, 28-day interval not flagged, both conflicts, both pre-existing flags, causation language, $8,390 charges, PT shown as a rate with no total.

**Sample case: summary beside excerpt (letter text from `/api/cases/{token}/export`)**
- Record 2: "Diagnosed with cervical strain and concussion without loss of consciousness; CT head negative; cyclobenzaprine 10 mg prescribed" matches "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg."
- Record 8: "C5-C6 disc protrusion with mild right foraminal narrowing; the record states findings may represent degenerative change and to correlate clinically."
- Record 9: "Cervical epidural steroid injection recommended; patient states symptoms began after the January collision."

**Findings that cost the verdict**

1. **Major: "No conflicts found." reads as an all-clear.** Conflict detection is code-only (SCOPE_CUTS row 13). It covers plan vs early end, denial vs prior history, and the accident-date rule. It does not cover laterality across records or loss-of-consciousness history. On lib09 the ED record says left shoulder and every later record says right shoulder. On lib08 the ED denies loss of consciousness at crash 2 and neurology records it. Neither produces a conflict flag. The empty state in `app/frontend/flags.js:10` says "No conflicts found." The goldens mark these as must-flag, and `library-latest.md` shows must flags 1/2 and 1/3.
2. **Major: entry quotes drop clinical sentences with no marker, and no code check catches it.** The summary-side check only looks for tokens in the summary that are missing from the quote. It never checks the reverse. Examples:
   - lib09 r6 loses "Pain 5/10", which the golden requires.
   - lib09 r2 loses "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo."
   - lib09 r1, r3 and r6 lose the interpreter lines.
   - lib09 r4 loses "Accidentes anteriores? ... No [X]".
   - case_06 r3 (golden E3) loses "History: occasional stiffness in the mornings at baseline."
3. **Minor: a causation attribution goes unflagged.** lib08 r11 says "left arm numbness since the rear-end collision of 2026-01-12". That is an unattributed provider note dating the numbness to crash 1. It conflicts with r3 ("without arm symptoms") and with r8, where numbness first appears at the crash-2 EMS record. The record is flagged only as Gap. The summary itself is faithful.
4. **Minor: no deterministic check for added diagnosis wording.** Edits are screened for numbers, dates, dollar figures, sides and negations only. A human edit that adds "whiplash" is saved. Edits to "disc herniation" and "MRI performed" were also saved. In this fixture run the judge could not rule on new text (JUDGE_UNAVAILABLE), so these would have gone out on the paralegal's accept alone.
5. **Nit: "Refer to physical therapy" becomes "referred to physical therapy"** (sample r3). This is a tense change from an order to a completed act. The PT evaluation in r4 supports it, but the wording is stronger than the record.

**Spanish handling.** lib09 r2, r7 and the OCR intake r4 are `needs_review` with `AI_TRANSLATION`. The Spanish quote stays verbatim, and the letter appends "[AI translation of the Spanish original; check before sending]". The translation is faithful: Niega pérdida del conocimiento became "Denies loss of consciousness", and Refiere became "Patient reports". The OCR date "03/O5/2026" is held as "date to confirm", and the intake entry is held out of the letter until it is confirmed.

```json
{"card": "GATE-M2", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 0c24f5f via git archive copy; app http://127.0.0.1:7899 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_DB in scratchpad); sample case plus library cases case_lib09_spanish_interpreter_espalda, case_lib08_second_crash_mri_after, case_lib02_slip_fall_prior_knee; golden case_06_subtle_pre_existing via CLI; reference spec/SAMPLE_CASE_TRUTHS.md",
 "exercised": [
  "git archive 0c24f5f into a fresh scratchpad dir; read personas/legal-nurse.md and my memory notes first",
  "python -m app.pipeline (CLI, fixture/curated) on evals/golden/sample.txt, case_lib02, case_lib08, case_lib09 and golden case_06; compared every summary to its excerpt clause by clause",
  "Started the app on port 7899 (PID 88848); POST /api/cases for the sample and three library cases, POST run, poll status, accept all entries/flags/amounts, GET /export; read letter_text and internal_notes_text for all four",
  "Probe edits via POST /items/{id}/review on the sample: dropped LOC negation, dropped hedge, dropped side, dropped Patient states, added whiplash, protrusion to herniation, MRI ordered to performed",
  "Ran evals.run on the archive (fixture): ship_bar_met False, blockers 4_no_invented_facts, determinism and judge_controls not measured; entry_recall 0.982 with case_06 E3 excerpt miss",
  "Read app/llm/prompts/extract_v1.md and judge_faithfulness_v1.md, app/frontend/flags.js, app/backend/conflict_candidates.py, memory/SCOPE_CUTS.md row 13, evals/reports/library-latest.md, library expected.json for lib08 and lib09",
  "Stopped the server by PID 88848 and confirmed port 7899 closed. Did not render the UI in a browser; the 'No conflicts found.' text was read from flags.js, not seen on screen. Live-model judge behaviour was not exercised (fixture backend only)"
 ],
 "verdict": "changes",
 "scores": {"clinical_fidelity_sample_case": 5, "hedge_negation_attribution_preservation": 5, "no_inferred_dx_severity_causation": 5, "abbreviation_expansion": 5, "spanish_honesty": 4, "completeness_of_quoted_findings": 2, "conflict_coverage_disclosure": 2, "deterministic_guard_on_added_terms": 3},
 "findings": [
  {"severity": "major", "title": "Empty conflict state says 'No conflicts found.' although the tool does not check left/right or LOC-history conflicts",
   "evidence": "app/frontend/flags.js:10 [\"conflict\",\"Conflicts between records\",\"No conflicts found.\"]; memory/SCOPE_CUTS.md row 13 'NOT covered, so never raised: ... laterality across records (left vs right) ... any contradiction in free wording'. CLI/export for case_lib09 (r1 'Left shoulder pain 7/10 ... Dx: left shoulder contusion'; r3 'Right shoulder pain 6/10'; r2 'hombro derecho') and case_lib08 (r9 'Denies LOC per patient' vs r12 'Patient states brief loss of consciousness at the second collision') print no CONFLICTS section and the internal notes carry no conflict line. evals/reports/library-latest.md: lib09 must flags 1/2, lib08 1/3; goldens mark laterality_mismatch, the LOC change and the two-incident conflict as must.",
   "why_it_matters": "A paralegal reading 'No conflicts found.' on lib09 sees a left-shoulder ED entry followed by right-shoulder entries with no warning. That is the first thing a defense nurse reviewer would find. The tool's silence is an unsupported assurance, because it only checks three conflict types and does not say so.",
   "fix": "Say which conflict types were checked wherever zero conflicts show: the empty state, the internal notes and the CLI. For example: 'No conflicts found among the types checked (plan vs outcome, denial vs prior history, accident date). Not checked: left/right across records, LOC or symptom history changes, dosage.' Longer term, add the laterality and LOC-history candidate rules already estimated in SCOPE_CUTS.",
   "acceptance_test": "Export for case_lib09 and case_lib08 contains the coverage sentence naming the unchecked types; the flags.js empty-state test asserts the text; once the laterality rule ships, lib09 r1 vs r3 yields a conflict flag citing both sides without choosing one."},
  {"severity": "major", "title": "Entries silently omit clinical sentences (pain scores, onset/chief complaint, interpreter, prior-accident answer, baseline history); nothing in the export marks the omission and no code check catches it",
   "evidence": "case_lib09 r6 record 'Interpreter: patient's daughter. MRI reviewed. Recommend physical therapy and subacromial injection. Pain 5/10.' -> entry 'MRI reviewed. Physical therapy and subacromial injection recommended.' (golden E6 required_terms includes 5/10). case_lib09 r2 quote omits 'Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo.' (golden must_contain_excerpt). case_lib09 r1 omits 'Hx obtained via patient's son, who interpreted.'; r4 omits 'Accidentes anteriores? Si [ ] No [X]'. golden case_06 r3 'History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10.' -> entry 'Cervical range of motion reduced; pain 5/10.' (evals.run: entry misses case_06 E3 'excerpt misses must_contain_excerpt'; entry_recall 0.982). The generator prompt (extract_v1.md) lets the model 'Choose the sentences that carry the treatment...'; judge_faithfulness_v1 states 'Missing detail alone is fine'; code check summary_tokens_not_in_excerpt only compares summary to quote, never record to quote.",
   "why_it_matters": "Pain scores are a trend the chronology has to carry (7, 6, 6, 5). Interpreter-mediated history and baseline or prior-condition wording are what a nurse reviewer reads for. Flagged sentences reach the internal notes, but unflagged ones, such as a pain score, vanish with no trace. The letter then looks complete.",
   "fix": "Add a deterministic check: any pain score (N/10), measured value or 'approx. N' present in the record but absent from the chosen quote makes the entry needs_review with a reason like RECORD_NUMBER_NOT_QUOTED. List record sentences not quoted in the entry's side-by-side view. Tell the generator to include the interpreter and history-source sentence when the record has one.",
   "acceptance_test": "case_lib09 r6 is needs_review (or quotes Pain 5/10); case_06 E3 includes 'History: occasional stiffness ... baseline'; a unit test seeds a record with 'Pain 5/10' and a quote without it and expects the reason code."},
  {"severity": "minor", "title": "Provider note that dates the symptom to the first collision is not flagged as causation or onset language",
   "evidence": "case_lib08 r11 'Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12.' appears in the internal notes only under 'Gap'; the CAUSATION LANGUAGE section lists r3, r12, r1, r8 but not r11. Same case r3 says 'Neck pain 5/10 without arm symptoms' and r8 (EMS 2026-04-24) first records 'left arm numbness'. Golden C3 (should) expects this pair.",
   "why_it_matters": "This is an unattributed provider sentence that carries onset and causation. It should go to the attorney as causation language, as 'Patient states symptoms began after the January collision' does in the sample. The summary itself is faithful and adds nothing.",
   "fix": "Add 'since the <collision|accident|crash|fall> of <date>' and 'since the <event>' onset-attribution patterns to the lexicon causation/onset category, with rationale (provider-authored onset attribution, not a physician causation opinion).",
   "acceptance_test": "lib08 r11 appears under CAUSATION LANGUAGE in the internal notes; the sample case flags are unchanged."},
  {"severity": "minor", "title": "No deterministic guard against added diagnosis or severity vocabulary in a human edit",
   "evidence": "Probe on the sample case: edit r2 to 'Diagnosed with whiplash and concussion without loss of consciousness; CT head negative; ...' -> HTTP 200, state needs_review, JUDGE_UNAVAILABLE. Edit r8 to 'C5-C6 disc herniation with mild right foraminal narrowing; findings may represent degenerative change and to correlate clinically.' -> 200. Edit r7 to '...MRI performed.' -> 200. Dropped negation, hedge, side or 'Patient states' were rejected with 422 SUMMARY_DROPS_QUALIFIER. app/backend/review.py header: judge 1 'never blocks a human-written edit (D-045b)'.",
   "why_it_matters": "The only barrier against whiplash, herniation or 'performed' is the LLM judge, and it cannot block a human edit. Persona checklist items 1, 4 and 11 depend on it.",
   "fix": "Add a closed-list code check on summaries and edits: diagnosis and imaging terms (whiplash, radiculopathy, herniat*, extrusion, bulge, TBI, fracture, sprain, tear, stenosis), plus 'performed/completed/received' when the quote says ordered or recommended. The check returns needs_review with a reason; it need not hard-block.",
   "acceptance_test": "The three probe edits above return a reason code naming the added term. The sample case golden summaries still pass."},
  {"severity": "nit", "title": "Order verb turned into past tense",
   "evidence": "Sample r3 excerpt 'Refer to physical therapy 2x/week for 6 weeks.' -> letter 'referred to physical therapy 2x/week for 6 weeks.' The sample also lists summary 'cyclobenzaprine 10 mg prescribed' for 'Rx cyclobenzaprine 10 mg', which is fine.",
   "why_it_matters": "'Refer' is an order. 'Referred' states it was done, which is the same pattern as 'MRI ordered' becoming 'MRI performed', only milder.",
   "fix": "Prefer 'referral to physical therapy 2x/week for 6 weeks recommended' or 'refer to ...' in extract_v1.md guidance.",
   "acceptance_test": "Golden sample r3 summary does not contain 'referred'."}
 ],
 "whats_right": [
  "Sample letter and CLI preserve every clinical qualifier: LOC negation, MRI hedge, 'approx.', pain scores, 'C/O' as 'complained of', 'Patient states', 'ordered' and 'recommended', with no added diagnosis, severity or causation, and no tool-added subjective/objective labels.",
  "Code check rejects (422 SUMMARY_DROPS_QUALIFIER) any edit that drops a negation, hedge, side or self-report phrase, and holds back lib02's MRI summary for an unquoted 'right' (SUMMARY_TOKEN_NOT_IN_EXCERPT).",
  "Spanish entries stay verbatim in Spanish, are needs_review with AI_TRANSLATION, carry an 'AI translation ... check before sending' label in the letter, and the translations I checked are faithful. The OCR date is held as a date to confirm."
 ],
 "questions_for_chris": [
  "Is the all-clear wording 'No conflicts found.' acceptable for the demo given SCOPE_CUTS row 13, or should the empty state carry a coverage disclaimer before the M2 gate?"
 ]}
```
