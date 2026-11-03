# GATE-M2 round 2: legal-nurse-reviewer (Linda Chen, RN, LNC)

Pinned commit 7cfdb0b, `git archive` copy in the scratchpad (`gm2r2_legal/src`). App run with `ZLAYT_MODE=local`, `LLM_BACKEND=fixture`, `FIXTURE_SET=curated`, port 7947 (7931 was held by another process), SQLite in the scratchpad. Server stopped by PID 4241 and the port confirmed closed.

**Verdict: pass.** No blocker and no major. Both round-1 majors are fixed. Four minors and two nits remain, and they are listed below.

**Major 1, the conflict coverage overclaim: fixed.**
- The bare "No conflicts found." is gone. grep over `src/app` finds none outside a code comment.
- I rendered the UI in a browser (Playwright).
  - lib08 and lib14 now read "No conflicts found among the kinds checked. Other kinds of conflict are not checked."
  - Both then show "Not checked: left versus right across records, a change in loss of consciousness history between records, and any other kind of conflict not listed under Checked. Read the records for these."
  - Both list the four kinds that were checked.
- lib09 reads the same, plus "Did not run on this case, or not on every record (3)". The three English-wording checks each say "the records in Spanish were not read. Records 2, 4 and 7 were not read." The coverage box says "1 kind checked", provider name only.
- The sample shows its 2 conflict cards, and the not-checked line is still on screen with them.
- This is exactly what I asked for. The tool does not catch the lib09 left-versus-right shoulder or the lib08 LOC change, and it now says so.

**Major 2, clinical sentences silently dropped: fixed.**
- `records[].uncovered[]` now lists the sentences no entry quotes. The UI shows a "Not in an entry (n)" link in each entry's head line, and the list is headed "Also in this record, not in an entry (n)". I opened it in the browser. Every list shows the verbatim sentence with a "Show in record" button.
- The lib09 list now carries every sentence I named in round 1:
  - "Pain 5/10." (r6)
  - "Interpreter: patient's daughter." (r3 and r6)
  - "Hx obtained via patient's son, who interpreted." (r1)
  - "Motivo de consulta: dolor de espalda y hombro derecho desde el atropello del 3 de marzo." (r2)
  - "Accidentes anteriores? Si [ ] No [X]." (r4). The form answer is joined to its question.
- I audited every sentence of every record in the four cases against the entry quotes and the uncovered list. Nothing clinical is in neither place. What is left is billing lines (charge sentences go to Amounts) and administrative lines such as the signature line, "Date written 9/2l/26" and "No payments posted."
- The list is a review aid only. It is not in the letter or the internal notes, and the entry still shows "Quote matches" while omitting "Pain 5/10". I accept this as "no longer silent". See finding 1.

**Clinical language (sample, lib08, lib09, lib14; letter and internal notes from `/api/cases/{token}/export`).** No blocker found.
- No inferred diagnosis, severity or causation.
  - Sample r2 keeps "concussion without loss of consciousness". r8 keeps "may represent degenerative change; correlate clinically" and "mild right foraminal narrowing". r7 keeps "MRI ordered". r9 keeps "recommended" and "patient states symptoms began after the January collision".
  - lib08 r10 keeps "disc herniation", which is the record's own word.
  - lib14 keeps "Pain 7 circled on a 0-10 scale" and does not turn it into 7/10.
- Hedges, "approx." and the negations ("Denies LOC") are intact.
- Attribution is kept as "Patient states" or "Patient reports". The tool adds no subjective or objective labels.
- lib09 Spanish entries are `needs_review` with the "[AI translation of the Spanish original; check before sending]" label. The translations are faithful: "Refiere" became "Patient reports", "Niega pérdida del conocimiento" became "Denies loss of consciousness", and "Exploración" became "Exam".
- The edit guard still returns 422 when an edit drops a negation, a hedge, a self-report phrase or "approx.", so those are not at risk.

**Remaining findings (all minor or nit; none blocks the pass).** These are carried over or new, and none was mapped in the triage.

1. **Minor: the coverage statement and the omitted-sentence list exist only in the UI.**
   - The internal notes, the letter and the CLI carry neither. lib09's notes show no conflict section and no line that Spanish records were not read by the conflict checks or that laterality is unchecked. They also do not mention the omitted "Pain 5/10".
   - `checks.not_checked` in the API (`conflict_candidates.py` `NOT_CHECKED`) omits loss-of-consciousness history, although the UI line names it.
   - This is no longer an overclaim, so it is not a major.
2. **Minor, still open from round 1: provider-authored onset attribution is not flagged.** lib08 r11 "Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12." appears in the notes only as "Gap". It is absent from the CAUSATION LANGUAGE list.
3. **Minor, still open from round 1: no deterministic guard against added diagnosis or completion wording in a human edit.**
   - On the sample, edits to "whiplash", "disc herniation", "Cervical radiculopathy" and "injection performed" were saved with 200 and `needs_review` / JUDGE_UNAVAILABLE.
   - I accepted the whiplash edit on e2. `/export` returned 200 and the letter says "Diagnosed with whiplash and concussion without loss of consciousness". The edit is a human's choice, so this is not a tool inference, and the live judge was not exercised.
4. **Minor: the notes heading "Causation language" is attached to neutral lines.** lib14 shows "Pt ambulatory at scene." and "Letter of protection requested." under it. lib08 shows "Ambulatory at scene." under it. An attorney can read that heading as the record containing causation wording.
5. **Nit, still open: "Refer to physical therapy" is still rendered "referred to physical therapy"** (sample r3). This is an order stated as done.
6. **Nit: the not-checked label "Pain scores that differ on the same day" understates the gap.** lib14 r5 "Pain 4 circled" against r6 "Pain 6/10, unchanged from the initial visit" is a different-day difference. The golden expects it as a should-flag and the tool does not raise it. The catch-all line covers it.

```json
{"card": "GATE-M2", "persona": "legal-nurse-reviewer", "model": "claude-sonnet-5-5",
 "scope": "commit 7cfdb0b via git archive copy (scratchpad gm2r2_legal/src); app http://127.0.0.1:7947 (ZLAYT_MODE=local, LLM_BACKEND=fixture, FIXTURE_SET=curated, ZLAYT_DB in scratchpad); sample case plus library cases case_lib08_second_crash_mri_after, case_lib09_spanish_interpreter_espalda, case_lib14_handwritten_chiro_scans; round-1 review reviews/GATE-M2-legal-nurse.md and reviews/GATE-M2-round1-triage.md",
 "exercised": [
  "Read personas/legal-nurse.md, my round-1 review, the round-1 triage and my memory note first",
  "git archive 7cfdb0b into a fresh scratchpad dir; started the app on port 7947 (PID 4241); port 7931 was already held by another process",
  "POST /api/cases ({sample} and {library}), POST run, poll; GET case for the sample, lib08, lib09 and lib14; read checks (conflict_types, skipped, not_checked, notes) and records[].uncovered",
  "Accepted entries, flags and amounts via the review endpoint, then GET /export: letter_text and internal_notes_text read in full for all four cases",
  "Rendered the UI with Playwright: the Conflicts group (text read, details opened), the 'Not in an entry (n)' links and lists, and the lib09 r6 row screenshot; read app/frontend/flags.js lines 83-151 and uncovered.js",
  "Sentence-level audit of every record in the four cases: each sentence is quoted in an entry, listed in uncovered, or a billing/administrative line",
  "Read app/backend/conflict_candidates.py (CONFLICT_LABELS, NOT_CHECKED, checks()); grep for any remaining bare 'No conflicts found' in app and submission",
  "Probe edits on the sample via POST /items/{id}/review {action: edit, edits: {summary}}: whiplash, dropped LOC, herniation, dropped hedge, 'MRI performed', radiculopathy, 'injection performed', dropped self-report, dropped approx., added 'severe'; accepted the whiplash edit and read the export",
  "Ran python -m app.pipeline (fixture) on lib09 to see the CLI output",
  "Ran pytest on tests/unit test_conflict_candidates, test_conflicts, test_t141_checks_per_case, test_t146_r4_ladder_compare_and_conflicts, test_uncovered and related files: 305 passed",
  "Stopped the server by PID 4241 and confirmed port 7947 closed. Live-model generation and the live judge were not exercised (fixture backend only)"
 ],
 "verdict": "pass",
 "scores": {"clinical_fidelity": 5, "hedge_negation_attribution_preservation": 5, "no_inferred_dx_severity_causation": 5, "conflict_coverage_disclosure": 4, "completeness_of_quoted_findings": 4, "spanish_honesty": 5, "deterministic_guard_on_added_terms": 3},
 "findings": [
  {"severity": "minor", "title": "Conflict coverage and the omitted-sentence list exist only in the UI; internal notes, letter and CLI carry neither, and the API not_checked list omits LOC history",
   "evidence": "notes_case_lib09_spanish_interpreter_espalda.txt: no conflict section and no line about Spanish records unread by the conflict checks or about left/right not being checked; 'Pain 5/10.' appears nowhere in letter or notes. CLI (python -m app.pipeline on lib09) prints no conflict or coverage text. app/backend/conflict_candidates.py NOT_CHECKED lists dosage, laterality, diagnosis, pain_score, treatment_duration_months, informant_history, and no LOC history, while app/frontend/flags.js:106-107 hard-codes 'a change in loss of consciousness history between records'.",
   "why_it_matters": "Anyone who reads the notes without the UI, or the API without the hard-coded line, gets no coverage statement. The notes do not claim 'no conflicts', so this is not the round-1 overclaim.",
   "fix": "Add one coverage line to INTERNAL REVIEW NOTES (kinds checked, kinds skipped with record numbers, and the not-checked list) and add an 'loc_history' item to NOT_CHECKED so the API and the UI agree. Optionally list uncovered sentences by record under the notes.",
   "acceptance_test": "lib09 internal notes contain the Spanish-records-not-read line and 'left versus right'; GET case checks.not_checked contains an LOC-history item."},
  {"severity": "minor", "title": "Provider onset attribution 'since the rear-end collision of 2026-01-12' is not flagged as causation or onset language (open since round 1)",
   "evidence": "notes_case_lib08_second_crash_mri_after.txt: 'Record 11 ... \"Neck pain 7/10 with left arm numbness since the rear-end collision of 2026-01-12. MRI reviewed. Recommend referral to neurosurgery.\" Gap.' The CAUSATION LANGUAGE line lists records 3, 12, 1 and 8 only.",
   "why_it_matters": "This is an unattributed provider sentence that dates the numbness to crash 1. It conflicts with r3 ('without arm symptoms') and r8, where numbness first appears at crash 2. It should reach the attorney as causation or onset wording.",
   "fix": "Add 'since the <collision|accident|crash|fall> of <date>' to the lexicon causation/onset category, with rationale (provider-authored onset attribution, not a physician causation opinion).",
   "acceptance_test": "lib08 r11 appears under CAUSATION LANGUAGE; the sample flags are unchanged."},
  {"severity": "minor", "title": "No deterministic check for added diagnosis or completion wording in a human edit (open since round 1)",
   "evidence": "Sample probes: edit e2 to 'Diagnosed with whiplash and concussion without loss of consciousness; ...' -> 200 needs_review JUDGE_UNAVAILABLE; e8 'disc herniation' -> 200; e7 'Cervical radiculopathy ... MRI ordered.' -> 200; e9 'injection performed' -> 200. After POST accept on e2, GET /export returned 200 and the letter contains 'Diagnosed with whiplash and concussion without loss of consciousness'. Dropped negation, hedge, self-report and approx. edits returned 422 SUMMARY_DROPS_QUALIFIER.",
   "why_it_matters": "The only barrier to a term the record does not contain is the LLM judge, which does not block a human edit. The edit was human-made, so this is not a tool inference, but it reaches the export.",
   "fix": "Add a closed-list code check on edited summaries (whiplash, radiculopathy, herniat*, extrusion, bulge, TBI, fracture, tear, stenosis; 'performed/completed' when the quote says ordered or recommended) that returns needs_review with a named reason.",
   "acceptance_test": "The four probe edits return a reason code naming the added term; the sample golden summaries still pass."},
  {"severity": "minor", "title": "Notes heading 'Causation language' is attached to neutral scene and billing lines",
   "evidence": "notes_case_lib14_handwritten_chiro_scans.txt: 'Causation language: record 1 ... \"Pt ambulatory at scene.\"; record 8 ... \"Letter of protection requested.\"'. notes_case_lib08: 'Record 1 ... \"Ambulatory at scene.\" Causation language.'",
   "why_it_matters": "A reader can take the label to mean the record states causation. The sentences are scene facts or a legal item, and the UI flag titles ('Scene facts', 'Attorney referral') are more accurate than the notes heading.",
   "fix": "In the notes, print the flag title (Scene facts, Attorney referral, Reported onset) instead of the shared 'Causation language' type, or add a one-line gloss that the heading is a review category and not a finding.",
   "acceptance_test": "lib14 notes print 'Scene facts' and 'Attorney referral' for those two sentences."},
  {"severity": "nit", "title": "'Refer to physical therapy' is rendered 'referred to physical therapy' (open since round 1)",
   "evidence": "letter_sample.txt: 'Persistent neck pain 6/10 and daily headaches; referred to physical therapy 2x/week for 6 weeks.' Quote: 'Refer to physical therapy 2x/week for 6 weeks.'",
   "why_it_matters": "An order reads as a completed act; r4 does support the PT evaluation.",
   "fix": "Prefer 'referral to physical therapy 2x/week for 6 weeks' in the generator guidance.",
   "acceptance_test": "Golden sample r3 summary does not contain 'referred'."},
  {"severity": "nit", "title": "Not-checked label 'Pain scores that differ on the same day' understates the gap",
   "evidence": "lib14 r5 'Pain 4 circled' (undated) versus r6 'Pain 6/10, unchanged from the initial visit' with r3 'Pain 7 circled'; golden C1 expects it as a should-flag; the UI does not raise it. app/backend/conflict_candidates.py NOT_CHECKED pain_score label.",
   "why_it_matters": "The label implies different-day pain-score differences may be checked. The catch-all line covers it.",
   "fix": "Relabel as 'Pain scores that differ between records'.",
   "acceptance_test": "GET case checks.not_checked pain_score label has no 'same day'."}
 ],
 "whats_right": [
  "The conflict group now says 'among the kinds checked', lists skipped checks with the server's reason and record numbers, and always shows the Not checked line, so a paralegal cannot read zero conflicts as an all-clear.",
  "'Also in this record, not in an entry' puts the pain score, interpreter lines, chief complaint and form answer one click from the entry, verbatim, with a jump to the highlighted sentence. My audit found no clinical sentence in neither place.",
  "Every summary I compared keeps LOC negation, the MRI hedge, approx., pain scores as written (including 'Pain 7 circled'), 'Patient states'/'Patient reports', and 'ordered'/'recommended'; the edit guard still returns 422 when an edit drops any of them."
 ],
 "questions_for_chris": []}
```
