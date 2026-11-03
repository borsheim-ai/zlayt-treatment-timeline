# T-015 Eval golden set, round 2: legal-nurse review

**Verdict: changes** (0 blockers, 3 majors). Both round-1 blockers are fixed. All 38 round-1 probe phrasings now behave correctly against the new regexes: 36 OK, and 2 are flag prose that is now out of regex scope (D-007). The hallucination set now covers laterality, level, region, severity, complaint-as-finding and negative-study flips, and every one of its 34 items is genuinely unsupported.

Three things still keep the eval from measuring the clinical distinctions:
- **Summary omissions are still unmeasured.** `required_terms` are scored on summary+excerpt, so a summary that drops "without loss of consciousness", "may represent" or "patient states" still passes.
- **Patient-attributed causation is allowed even when the patient never stated a cause.** Sample M2 lists "Patient states her neck pain is due to the collision." as a good example. The record says only "began after", and the patient is 41M.
- **`source_kind: patient_self_report` covers whole mixed entries.** That label now includes exam findings and a diagnosis.

Resolution table and per-item checks: `artifacts/review-evidence/T-015-r2-nurse.md`. Probe: `artifacts/review-evidence/T-015-r2-nurse-probe.py`, output in `.out.txt`.

```json
{"card": "T-015", "persona": "legal-nurse-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 3c5eb7c (git diff 47520a8..3c5eb7c -- evals/golden): README, check_golden.py, sample + case_01..09 (.txt/.expected.json), hallucinations.jsonl (34), hallucinations_controls.jsonl (10), sample.export.expected.txt, seeded_edits SE1-SE4; spec refs REQUIREMENTS R-TL-4/8/10, R-FL-7, R-RV-3; decisions D-006/D-007/D-012/D-014. No app (pre-code card).",
 "exercised": [
   "python3 tools/board.py show T-015 (AC 1-4, handoff notes)",
   "python3 evals/golden/check_golden.py -> 'golden OK: 10 cases (9 synthetic), 54 must_nots with tested examples, 34 hallucination items (12 synthetic-sourced), 10 controls (7 paraphrase), all stress types covered' EXIT=0",
   "read README.md and check_golden.py in full; printed every sample must_not (pattern, unless_context, bad/good examples)",
   "python3 -I artifacts/review-evidence/T-015-r2-nurse-probe.py: 38 round-1 phrasings (36 OK, 2 n/a flag prose, 0 leak, 0 false positive) + 50 new phrasings (18 OK, 30 LEAK, 2 FALSEPOS judged acceptable) against the live regexes with check_golden semantics; output saved to T-015-r2-nurse-probe.out.txt",
   "required_terms omission probe on sample E1/E2/E8/E9 (pass on summary+excerpt, fail on summary only)",
   "R-TL-10 number-check probe on E5 using check_golden nums(): 8/10, 2/10, 20/10 raise no code warning",
   "printed and judged all 34 hallucination items and 10 controls against record_text",
   "read case_06, case_08, case_09 .txt; printed entries/required_terms/source_kind/flags/tolerated/must_not for case_01..09",
   "read sample.export.expected.txt (letter + internal notes) and checked letter summaries against excerpts",
   "grep 'pre-existing) change|Ongoing chiropractic' evals/golden/*.json -> no output, exit 1",
   "grep source_kind in golden, README, REQUIREMENTS (R-FL-7 uses 'patient_report' on flags)",
   "read memory/ORCHESTRATOR_DECISIONS.md D-006..D-018"
 ],
 "verdict": "changes",
 "scores": {"clinical_fidelity_of_reference_wording": 4, "appendix_c_must_not_check_reliability": 4, "hallucination_set_genuineness": 5, "hallucination_failure_mode_coverage": 4, "controls_faithfulness": 4, "objective_vs_subjective_coverage": 3, "summary_omission_measurement": 2},
 "findings": [
  {"severity": "major", "title": "required_terms are scored on summary+excerpt, so a summary that drops the LOC qualifier, the hedge, 'patient states' or the complaint marker still passes (round-1 F4 only partly fixed)",
   "evidence": "evals/golden/README.md scoring 'Entries': '**summary+excerpt** satisfying every `required_terms` item'. Probe (T-015-r2-nurse-probe.out.txt): E2 summary 'Cervical strain and concussion; CT head negative; cyclobenzaprine 10 mg; PCP in 1 week.' -> pass_on_summary+excerpt=True pass_on_summary_only=False; same for E8 'C5-C6 disc protrusion with mild right foraminal narrowing.' (no hedge), E9 without 'patient states', E1 'exam showed neck injury with pain 7/10'. No regex fires on 'Diagnosed with cervical strain and concussion; CT head negative.' (LEAK row). R-TL-4 judge #1 checks only that the summary 'adds nothing', so it cannot catch an omission. The golden export's own E1 summary ('Restrained driver rear-ended at approx. 35 mph; neck pain 7/10 and headache; ...') has none of E1's complaint terms.",
   "why_it_matters": "Dropping 'without loss of consciousness' from the concussion diagnosis is a dealbreaker for this persona. The summary sentence is the tool's own statement in the letter. If it reads 'concussion' while the quote below reads 'concussion without loss of consciousness', defense counsel can quote either one. The same applies to a dropped 'may represent' or 'patient states'. The eval currently has no way to fail any of these.",
   "fix": "Add a summary-only field (e.g. `summary_required_terms`) for the qualifier tokens, with any-of alternatives so faithful wording passes. E2: 'concussion' + any of ['without loss of consciousness','no loss of consciousness','w/o loss of consciousness','without LOC','no LOC','w/o LOC']. E8: any of ['may represent','may be','possible','could represent']. E9: any of ['patient states','per patient','patient reports','patient-reported']. E1: any of ['C/O','complain','reports']. case_06 E1: any of ['denies','denied']. case_06 E2: any of ['off and on','intermittent']. A miss makes the entry needs_review (or fails it). Either align the export example's E1 summary or exempt it explicitly.",
   "acceptance_test": "A stub run where record 2's summary is 'Cervical strain and concussion; CT head negative.' marks E2 not-found or needs_review. The same happens for E8 without a hedge token and E9 without an attribution token. check_golden.py verifies each summary_required_terms alternative is consistent with its record."},
  {"severity": "major", "title": "Sample M2 lets patient-attributed causation through even when the patient never stated a cause; its good example also gets the patient's sex wrong; no judge item covers temporal-to-causal",
   "evidence": "sample.expected.json:735 good_examples includes 'Patient states her neck pain is due to the collision.'. M2 statement: \"Patient-attributed wording ('patient states ...') is allowed.\" Record 9 says only 'Patient states symptoms began after the January collision.' Record 1 says '41M'. Probe: 'Patient states the collision caused his symptoms.' -> LEAK. hallucinations.jsonl has no temporal_to_causal item (H10 covers only recasting as a physician opinion). M10 judge bad_examples cover only the physician recast.",
   "why_it_matters": "'Began after' is a temporal report. 'Due to' and 'caused' are causal claims. Putting a causal claim in the patient's mouth changes what the record says, even when 'patient states' is kept. This is the record an adjuster will read most closely. The golden marks the upgraded wording as acceptable for this exact case, and the judge's ship bar never tests it.",
   "fix": "Replace that good example with a faithful one (e.g. 'Per patient, symptoms began after the January collision.'). Narrow the M2 statement to 'patient-attributed wording that reproduces what the patient said'. Add a hallucination item, category temporal_to_causal: record 9, candidate 'Patient states the collision caused his symptoms.'. Add it to REQ_CAT and as an M10 judge bad_example.",
   "acceptance_test": "grep -n 'due to the collision' evals/golden/sample.expected.json shows no good_example; check_golden REQ_CAT contains temporal_to_causal; judge #1 flags the new item (partially or unsupported)."},
  {"severity": "major", "title": "source_kind 'patient_self_report' labels whole mixed entries, including exam findings and a diagnosis; vocabulary differs from R-FL-7",
   "evidence": "case_08_diagnosis_temptation.expected.json:61 E1 source_kind patient_self_report; record 1 includes 'Tenderness over the anterior shoulder.' (palpation finding). case_06_subtle_pre_existing.expected.json:109 E3 labels 'Cervical ROM reduced.' (measurement); :73 E1 labels 'Cervical strain' (ER assessment). sample.expected.json:104 E1 labels 'Alert and oriented.'. README:40 'content is the patient's own statement/complaint and must stay attributed'. REQUIREMENTS R-FL-7 uses source_kind = \"patient_report\" on flags.",
   "why_it_matters": "If the runner or the prompt follows this label, it requires exam findings and a diagnosis to be attributed to the patient ('patient reports tenderness', 'patient reports cervical strain'). That reverses the subjective/objective error and understates objective evidence. The golden should encode the S/O split exactly, not approximately.",
   "fix": "Make it span-level: `self_report_spans` lists the verbatim subjective sentences only. Sample E1: 'C/O neck pain 7/10 and headache'. E9: 'Patient states symptoms began after the January collision'. case_06 E1: 'Patient denies prior neck problems'. case_06 E3: 'History: occasional stiffness in the mornings at baseline'. case_08 E1: 'Shoulder pain after a fall'. Use R-FL-7's value name or document the difference.",
   "acceptance_test": "check_golden asserts each self_report_span is verbatim in its record and contains none of: tenderness, ROM, Dx, alert and oriented, strain; no entry-level patient_self_report remains on a record with an O/A sentence."},
  {"severity": "minor", "title": "Regex floor still leaks 30 of 50 new violating phrasings (judge #1 is the backstop)",
   "evidence": "T-015-r2-nurse-probe.out.txt r2 LEAK rows: M6 'Concussion with possible LOC.', 'Brief LOC at scene.', 'LOC x 2 minutes.', 'mTBI; cervical strain.'; M3 'Patient could not turn head, and MRI shows degenerative disc disease.' (unrelated 'could' exempts it across a comma), 'Findings may represent degenerative disc disease.'; M2 'Neck pain from the January collision.', 'Injured in the collision.', 'The crash resulted in a disc protrusion.', 'Disc protrusion because of the collision.'; M1/M8 'C5-C6 disc extrusion ...', 'HNP at C5-C6.', 'C5-C6 bulge.'; M13 'ESI performed.', 's/p cervical ESI.', '...injection scheduled.'; M9 'Neck pain resolved by discharge.'; case_06 M2 'No history of neck problems.', 'No past neck problems.', 'Negative for prior neck problems.'; case_05 M4 'The car caused the fracture.'",
   "why_it_matters": "Disc protrusion -> extrusion/bulge (Fardon nomenclature), ESI 'performed', and denial -> 'no history' are exactly the substitutions this persona checks. The README calls regex the deterministic floor, and today that floor misses common chart abbreviations (ESI, HNP, mTBI, LOC).",
   "fix": "M6: add (possible|questionable|brief) LOC, LOC x, mTBI. M3: require the hedge within ~4 words before the term, or stop the unless_context window at ',' / 'and'; add 'disc disease'. M2: 'from the (\\w+ )?collision', 'injured in', 'resulted in', 'because of'. M1/M8: extrusion, HNP, bulge. M13: ESI, s/p, scheduled. M9: resolved (excluding 2023 LBP context), 'patient recovered'. case_06 M2: history of, past, negative for. case_05 M4: 'caused the fracture', 'from being struck'.",
   "acceptance_test": "Every LEAK row in T-015-r2-nurse-probe.out.txt becomes a bad_example that check_golden proves fires; every OK faithful row stays a good_example."},
  {"severity": "minor", "title": "Two paraphrase controls are not cleanly faithful: S08 invents the patient's sex, S10 drops 'radiating'",
   "evidence": "hallucinations_controls.jsonl S08 'Her neck pain continues. She has visited a chiropractor ...'; case_06 never states sex. S10 'new onset of arm pain on the right side with numb fingers' vs record 'New onset pain radiating to right arm with numbness in fingers'.",
   "why_it_matters": "A judge that correctly returns `partially` on S08 is graded against a control labeled supported. 'Radiating' is the symptom character that ties the record to the later MRI, so losing it in an accepted paraphrase teaches the wrong house style.",
   "fix": "S08: 'Neck pain continues. The patient has seen a chiropractor intermittently since a lifting injury several years ago.' S10: 'new onset pain radiating to the right arm with numb fingers, rated 7/10; ...'.",
   "acceptance_test": "No control contains he/she/his/her unless the record states sex; S10 contains 'radiat'."},
  {"severity": "minor", "title": "Missing judge-calibration items: 'approx.' dropped, abbreviation mis-expansion, pain-score swap the R-TL-10 code check cannot see",
   "evidence": "No hallucination category for approximation or abbreviation. Probe: on E5 (source 'Capital PT, visit 8', date 2026-02-20), 'Visit 8: pain 8/10, improving.', 'pain 2/10' and 'pain 20/10' produce no new numbers, so no code warning. seeded_edits has no judge edit for this.",
   "why_it_matters": "'approx. 35 mph' -> '35 mph' and 'approx. 40%' -> '40%' turn estimates into measurements. A changed pain score is a severity change. Because R-TL-10 allows label and date digits, judge #1 is the only check, and nothing proves it catches this.",
   "fix": "Add hallucination items: approximation_dropped (record 1 '... rear-ended at 35 mph'), abbreviation_misexpanded (e.g. reading 'PT' in record 6 as 'patient'). Add seeded edit SE5 kind judge 'Visit 8: pain 8/10, improving.' -> needs_review.",
   "acceptance_test": "check_golden REQ_CAT includes approximation_dropped; SE5 exists and its expected_state is needs_review."},
  {"severity": "nit", "title": "case_01 E1 required_term is bare 'fracture' while the record says 'X-ray negative for fracture'",
   "evidence": "case_01_date_formats.expected.json E1 required_terms ['ankle','fracture']; case_01_date_formats.txt:6 'X-ray negative for fracture.'",
   "why_it_matters": "The protected fact is the negative study. A bare 'fracture' token is satisfied by a summary that says 'ankle fracture'.",
   "fix": "Use 'negative for fracture'.",
   "acceptance_test": "E1 required_terms contains 'negative for fracture'."}
 ],
 "whats_right": [
  "Both round-1 blockers are fixed. All 38 round-1 probe phrasings now behave correctly, and check_golden tests every regex's bad and good examples both ways.",
  "All 34 hallucination items are really unsupported. The new ones cover laterality, level, region, severity, complaint-as-finding, negative CT flipped and denial-as-fact, and none slipped in supported.",
  "Reference wording is now clinically careful: P2 quotes the hedge, case_06 P1 keeps 'off and on', case_06 C1 says 'not a finding that the patient misstated anything', case_08 K1 is `should`, and SE1-SE4 are right."
 ],
 "questions_for_chris": [
  "When a summary drops a qualifier the excerpt below it still carries (e.g. 'concussion' without 'without loss of consciousness'), should that make the entry needs_review (the paralegal fixes it) or fail the eval case outright?"
 ]}
```
