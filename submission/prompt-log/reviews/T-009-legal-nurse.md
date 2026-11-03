# T-009 — Flag lexicon — legal-nurse review

**Verdict: fail** (2 blockers, 4 majors).

The sample case works: `research/lexicon_selfcheck.py` passes, and every Appendix C phrase fires with the expected entry and strength. The rationales for the hedge, degenerative and self-report entries are clinically sound. The trouble starts outside the sample. I ran 78 clinical probe sentences (`artifacts/review-evidence/T-009-nurse-probes.txt`, output in `T-009-nurse-probe-output.txt`). I also ran the lexicon over every golden record (`T-009-nurse-golden-scan.txt`). Results:

- **Missed prior-history wording.** The lexicon finds nothing in the most common ways a chart records prior history: `hx of`, `PMH significant for`, `s/p`, `status post`, `PSH:`, `prior ACL repair`, `at baseline`. It produces **no hit** on 2 of the 4 golden `must` pre_existing flags (case_06 P1, case_07 P1).
- **Negation guard hides real findings.** The guard's window crosses commas. "No acute fracture, mild degenerative changes at C5-C6" comes back NEGATED, so a degenerative finding is logged as absent.
- **High-strength flags on routine wording.** High-strength entries fire on everyday index-case language ("recent MVA", "previous treatment", "Per patient, pain 5/10").
- **Flag types don't match the spec.** The lexicon's flag types (`pre_existing | causation_weakening | compliance`) do not map to REQUIREMENTS §1.3 (`prior_condition | causation`). Record 6 sits under `compliance`, a type the app does not have.

```json
{"card": "T-009", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
 "scope": "commit f419c3b: app/llm/lexicon.yaml, research/lexicon_selfcheck.py; checked against spec/REQUIREMENTS.md §1.3, spec/SAMPLE_CASE_TRUTHS.md, evals/golden/*.txt + *.expected.json; no app URL (not built)",
 "exercised": [
  "python3 tools/board.py show T-009 (AC 1-3, handoff)",
  ".venv/bin/python research/lexicon_selfcheck.py -> 'entries: 48  by type: pre_existing=17, causation_weakening=21, compliance=10' ... 'RESULT: PASS'",
  "Wrote 78 clinical probe sentences: artifacts/review-evidence/T-009-nurse-probes.txt (degenerative, hedges, subjective markers, negations, hx/PMH/s-p, noise)",
  "Wrote artifacts/review-evidence/T-009-nurse-probe.py: loads lexicon.yaml with yaml.safe_load, compiles each pattern with re.I, applies research/lexicon_selfcheck.negated() (the reference guard); repo not modified",
  ".venv/bin/python artifacts/review-evidence/T-009-nurse-probe.py probes -> 'BAD count 37' (full output artifacts/review-evidence/T-009-nurse-probe-output.txt)",
  ".venv/bin/python artifacts/review-evidence/T-009-nurse-probe.py golden -> artifacts/review-evidence/T-009-nurse-golden-scan.txt (every record of sample + case_01..08)",
  "Read every one of the 48 entries' rationale and false_positive notes for clinical accuracy",
  "Compared flag types with spec/REQUIREMENTS.md:57 and the golden expected.json flag/must_not_flag lists"
 ],
 "verdict": "fail",
 "scores": {"appendix_c_coverage": 5, "clinical_vocabulary_recall": 2, "negation_handling": 2, "strength_calibration": 2, "rationale_clinical_accuracy": 4, "false_positive_notes_real": 3},
 "findings": [
  {"severity": "blocker",
   "title": "Standard prior-history and prior-surgery wording gets no hit; the lexicon misses 2 of 4 golden `must` pre_existing flags",
   "evidence": "probe output: 'BAD HX FIRE:pre_existing hx of lumbar strain.' (no hits); 'PMH significant for lumbar strain.' (none); 'Past medical history significant for cervical radiculopathy.' (none); 's/p ACDF C5-6.' (none); 'Status post lumbar fusion.' (none); 'PSH: L4-5 laminectomy.' (none). Golden scan: 'case_07_prompt_injection.txt 2 -' for record 2 'History: prior ACL repair of the same knee in 2019.' (golden P1 must, pre_existing, prior_surgery_same_region); 'case_06_subtle_pre_existing. 2 -' for 'Has been seeing a chiropractor off and on since a lifting injury several years ago.' (golden P1 must). Cause: prior_injury_or_event (lexicon.yaml:103) noun list has 'surgery' but not repair/fusion/ACDF/laminectomy; history_of (:62) needs 'history of'; pmh_section (:90) needs ':' or '-' right after PMH; there is no s/p, status post, hx or PSH entry.",
   "why_it_matters": "R-FL-3 and LLM_VS_CODE row 12 make the lexicon the independent deterministic signal that 'catches what a model overlooks'. Charts record prior history mostly as hx, PMH significant for, s/p and status post. A same-region prior surgery (case_07) is the most damaging pre-existing fact. If the LLM misses it too, nothing flags it and the fact is lost from review.",
   "fix": "Add entries (pre_existing, high unless noted). (1) s/p | status post + procedure or injury. (2) hx of | Hx: | PHx | PSH: | past surgical history. (3) PMH|past medical history + (significant|remarkable|notable|positive) for. (4) Widen the prior_injury_or_event nouns: repair, reconstruction, fusion, ACDF, laminectomy, discectomy, arthroscopy, problem(s), condition, complaint(s), pain. (5) 'at baseline' / 'baseline (pain|stiffness|symptoms)' at medium. (6) '(several|many|\\d+) years ago' and 'off and on since' at medium. (7) 'acting up again' / 'again' after a symptom at low.",
   "acceptance_test": "Every 'HX' line in artifacts/review-evidence/T-009-nurse-probes.txt fires a pre_existing entry. The lexicon fires on case_07 record 2 and case_06 record 2. The examples in lexicon.yaml include those sentences, and the selfcheck stays PASS."},
  {"severity": "blocker",
   "title": "The negation guard crosses commas and suppresses real degenerative and prior findings (they are logged as negated)",
   "evidence": "probe output: 'No acute fracture, mild degenerative changes at C5-C6.' -> 'degenerative[pre_existing,high,NEGATED]'; 'No acute osseous abnormality, mild multilevel spondylosis.' -> 'degenerative_imaging_terms[...,NEGATED]'; 'Patient denies numbness or tingling, reports chronic low back pain since 2015.' -> 'chronic[...,NEGATED]'; 'No LOC, history of migraines.' -> 'history_of[...,NEGATED]'; 'No neck complaints before the accident, history of lumbar strain.' -> NEGATED. Binding semantics are at lexicon.yaml:23-29: window_tokens 6, same sentence, and the terminators list has no comma and no reporting verbs.",
   "why_it_matters": "'No acute fracture, mild degenerative change' is the standard way a radiology impression is written. The guard does more than miss these findings. It records them as NEGATED in the audit, so the deterministic layer states the opposite of the record ('no degenerative change'). In case_06-style records a denial is followed by an admission in the same sentence, and the admission is the fact the adjuster will find.",
   "fix": "Make the scope end at the end of the negated noun phrase. Comma followed by a new finding is a terminator, and so are reporting/positive verbs (reports, endorses, has, with, notes, shows, demonstrates, 'history of'). Alternatively, make ', ' a terminator whenever the next token is not 'or'/'nor'. Leave 'No fracture, subluxation or degenerative change' negated. Add the probe sentences to examples.hit, and the true list negation to examples.negated.",
   "acceptance_test": "The five sentences above FIRE. 'No fracture, subluxation or degenerative change.' and 'Denies prior neck injury.' stay NEGATED. Selfcheck PASS."},
  {"severity": "major",
   "title": "Flag types don't map to REQUIREMENTS §1.3; the sample's record 6 lands under a type the app does not have",
   "evidence": "lexicon.yaml:19 'flag_types: [pre_existing, causation_weakening, compliance]' vs spec/REQUIREMENTS.md:57 'Four types: `gap`, `conflict`, `prior_condition`, `causation`'. R-FL-4 requires record 6 ('Discharged from PT after two missed appointments') as causation, and sample.expected.json K2 is type 'causation'. The lexicon tags it missed_appointments/discharged_from_care = compliance (golden scan sample.txt 6). The golden files use 'pre_existing' and 'causation'. Nothing in the YAML maps one set to the other.",
   "why_it_matters": "If the backend reads flag_type literally, the record 6 lexicon hit never pairs with the LLM's causation flag. The flag then comes out LLM_ONLY/needs_review, or its compliance hits are dropped. That puts K2 recall and the 'two signals agree' logic in R-FL-3/4 at risk.",
   "fix": "Add a binding mapping block to the semantics header: pre_existing->prior_condition, causation_weakening->causation, compliance->causation (with subtype compliance). Or rename the types to the app's names. Keep 'compliance' as a subtype.",
   "acceptance_test": "Every entry's effective app flag type is one of REQUIREMENTS §1.3's types. Running the lexicon on sample record 6 gives a causation-typed hit."},
  {"severity": "major",
   "title": "High-strength entries fire on routine index-case wording, and their false-positive notes don't mention it",
   "evidence": "probe output: 'Patient seen for neck pain after recent MVA.' -> 'intervening_event[causation_weakening,high,FIRE:\"recent MVA\"]' (lexicon.yaml:451; the pattern lists 'recent' and 'new', and the FP note covers only negation). 'Patient tolerated previous treatment well.' -> 'prior_injury_or_event[pre_existing,high,FIRE:\"previous treatment\"]'. 'Continue prior physical therapy plan of care.' -> high pre_existing. 'Per patient, pain 5/10 today.' -> 'per_patient_or_intake[causation_weakening,high]' (lexicon.yaml:411, where the FP note itself says 'Often benign ... High strength only because the date-conflict engine needs every sourced date').",
   "why_it_matters": "High means 'by itself warrants a review flag' (header). 'Recent MVA' calls the index accident an intervening event. 'Previous treatment' in a PT note is a session for the same injury, not a prior condition. A real chart has dozens of each, so the paralegal gets buried in false pre-existing and causation flags, and the ≥0.9 flag-precision bar is at risk. 'Per patient' is a subjective-source marker, the same class as 'patient reports', which the lexicon rates low. Rating it high because a code engine wants dates mixes up data tagging with flag strength.",
   "fix": "Remove 'recent' and 'new' from intervening_event, or require a date or 'second/another' cue. In prior_injury_or_event, require a noun that is not treatment/therapy, or drop treatment, chiropractic care and physical therapy to medium with a code check that the earlier care predates the accident. Split per_patient_or_intake: date/DOA provenance ('per intake form' + a date) stays high, and a generic 'per patient' becomes low. Write each of these cases into the false_positive notes.",
   "acceptance_test": "The four NOISE sentences above produce no high or medium flag. Sample record 7 still fires per_patient_or_intake high on 'Date of accident per intake form: 2026-01-19'."},
  {"severity": "major",
   "title": "The 'did not show' pseudo-negation and missing absence cues turn statements of absence into high flags",
   "evidence": "probe output: 'MRI did not show degenerative changes.' -> 'degenerative[pre_existing,high,FIRE]; no_show_cancel[compliance,high,FIRE:\"did not show\"]' (lexicon.yaml:32 lists 'did not show' as a pseudo-negation, so the real negation is removed). 'Degenerative changes are absent.' -> FIRE (post_cues have 'is absent'/'was absent' but not 'are absent'). 'Unlikely to be degenerative.' -> degenerative high FIRE ('unlikely' is not a cue).",
   "why_it_matters": "A high pre_existing flag on a record that says degenerative change is absent, plus a high compliance flag calling a negative MRI a no-show. The adjuster-facing review list then contains the opposite of what the record says.",
   "fix": "Remove 'did not show' from pseudo_negations (no_show_cancel is not negatable, so it gains nothing there). Restrict no_show_cancel's 'did not show' branch to 'did not show (up|for)'. Add pre-cues 'unlikely', 'did not show', 'does not show', 'no evidence', and post-cues 'are absent', 'were absent', 'not identified', 'not seen'.",
   "acceptance_test": "The three sentences fire no pre_existing hit and no compliance hit. 'No-show 2/14.' still fires no_show_cancel."},
  {"severity": "major",
   "title": "Hedge coverage is uneven: 'Clinical correlation recommended' is a high flag, but its common variants and 'suggestive of' get nothing",
   "evidence": "probe output: 'Clinical correlation recommended.' -> correlate_clinically high FIRE, but 'Correlate with clinical findings.' -> no hits; 'Recommend correlation with history and physical examination.' -> no hits; 'Signal change is suggestive of tendinosis.' -> no hits; 'Findings suggestive of chronic change.' -> only chronic (pre_existing); 'Edema, degenerative versus post-traumatic.' -> no causation hit. Golden case_08 K1 (must, causation) is exactly 'Clinical correlation recommended'.",
   "why_it_matters": "The golden set treats the correlation hedge as a must causation flag, so the same radiologist hedge flags or doesn't depending on word order. That inconsistency is what an adjuster exploits, and paralegals can't predict it. 'Suggestive of', 'compatible with', 'concerning for' and 'X versus Y' are standard radiology hedges named in the brief.",
   "fix": "Widen correlate_clinically to 'correlat\\w*\\s+with\\s+(?:the\\s+)?(?:clinical|history|physical|exam|symptoms|findings)'. Add a hedge entry (medium) for 'suggestive of | compatible with | concerning for | cannot be differentiated | (degenerative|chronic|acute|traumatic)\\s+(?:versus|vs\\.?)\\s+'.",
   "acceptance_test": "Every HEDGE FIRE line in the probe file fires causation_weakening, and 'Likely muscular strain.' and 'Findings consistent with acute cervical strain.' still fire nothing."},
  {"severity": "minor",
   "title": "Gaps in subjective-marker coverage, including the sample's own record 1 ('C/O')",
   "evidence": "probe output: 'C/O neck pain 7/10 and headache.' -> no hits (this is verbatim sample record 1; selfcheck output '1: ' is empty); 'Pt. reports neck pain since the MVA.' -> no hits ('pt.' with a period fails '\\bpt\\s+'); 'Complains of neck pain since the collision.' -> no hits. patient_reports_generic (lexicon.yaml:398) needs 'patient|pt' before the verb, and its own list contains 'c/o', which can only match after 'patient c/o'.",
   "why_it_matters": "patient_reports_generic exists 'to keep attribution in the summary'. Without it, an EMS chief complaint can be summarized as an objective finding ('neck pain 7/10' with no 'complains of'), which mixes subjective and objective.",
   "fix": "Allow a bare '\\bC/O\\b', '\\bcomplain(?:s|ing)?\\s+of\\b', 'pt\\.?', and he/she/client subjects. Add 'Subjective:' / 'S:' section headers (low).",
   "acceptance_test": "All SUBJ lines in the probe file fire, and sample record 1 shows patient_reports_generic[low]."},
  {"severity": "minor",
   "title": "Gaps in degenerative imaging vocabulary",
   "evidence": "probe output, no hits: 'Grade 1 anterolisthesis L4 on L5.'; 'Old compression deformity of T12.' (age_related_old_findings needs old + [healed] + fracture/injury/deformity, so 'compression' breaks it); 'Schmorl's node at L2 superior endplate.'; 'Ligamentum flavum hypertrophy at L4-5.'. degenerative_imaging_terms 'spondylo(?:sis|tic)' does not match 'spondylolisthesis'.",
   "why_it_matters": "Defense IME and peer reviewers cite these as chronic/pre-existing findings on spine imaging.",
   "fix": "Add (ante|retro)?listhesis|spondylolisthesis, Schmorl'?s?\\s+nodes?, ligamentum flavum (hypertrophy|thickening), annular (fissure|tear) at medium (it can be acute or chronic), and 'old (\\w+\\s+){0,2}(fracture|deformity)'.",
   "acceptance_test": "The four sentences fire pre_existing."},
  {"severity": "minor",
   "title": "Some false-positive notes are not real false-positive analysis",
   "evidence": "lexicon.yaml:301 correlate_clinically: 'Rarely benign in this context; strength high.' Clinically this is near-universal radiology boilerplate, appended to most imaging impressions whatever the finding. age_related_old_findings false_positive is only 'Negated by guard.'",
   "why_it_matters": "AC 3 asks every entry for a false-positive note. A note that claims a phrase is rarely benign when it is boilerplate gives the backend and QA no guidance on the noise it will produce. In a 10-study chart that is 10 high causation flags.",
   "fix": "Say that it is boilerplate, and that the flag matters most when a hedge or alternative-cause term co-occurs in the same impression. Consider downgrading the stand-alone hit to medium (see question). For age_related, write the real false positives: 'age-appropriate' attached to a normal finding, and congenital findings unrelated to the claimed region.",
   "acceptance_test": "Each false_positive note names at least one concrete benign context or states that none was found after a search."},
  {"severity": "nit",
   "title": "The new_onset rationale puts a clinical interpretation in place of the record's wording",
   "evidence": "lexicon.yaml:429 'record 7: new radicular arm symptoms'. Record 7 says 'pain radiating to right arm with numbness in fingers'.",
   "why_it_matters": "'Radicular' implies nerve-root involvement, a diagnosis-adjacent label. If rationales are ever shown as flag text, this is the tool speaking in its own voice (SPEC §6.6). Similarly, Modic type 1 in degenerative_imaging_terms is described as chronic, although type 1 is active edema-type change.",
   "fix": "Use the record's wording: 'new arm pain with numbness'.",
   "acceptance_test": "grep -n radicular app/llm/lexicon.yaml returns no rationale lines."}
 ],
 "whats_right": [
  "All sample-case Appendix C phrases fire with the expected entry and strength; selfcheck PASS, and the low tier keeps 'Pain 3/10' and 'CT head negative' from flagging alone.",
  "The rationales for may_represent (possibility vs reasonable medical probability), degenerative ('never resolve to degenerative or traumatic'), patient_attributes_causation and normal_imaging ('never summarize as no injury') are clinically correct.",
  "Simple negations (denies prior, no history of, negative for prior surgeries, no prior MVA) are suppressed, and 'but'/';' correctly end the negation scope ('Denies prior neck injury but reports a 2019 MVA' fires)."
 ],
 "questions_for_chris": [
  "Golden case_08 K1 makes a stand-alone 'Clinical correlation recommended' a must causation flag. Clinically it is boilerplate on nearly every imaging report. Should a stand-alone hit stay high (a flag every time), or be medium unless it co-occurs with a hedge or degenerative term in the same impression?"
 ]}
```
