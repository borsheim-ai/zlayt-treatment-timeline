# T-009 review — claims-adjuster-reviewer

**Verdict: changes** (0 blockers, 5 majors, 3 minors).

The deterministic check passes. `.venv/bin/python research/lexicon_selfcheck.py` reports 48 entries (pre_existing=17,
causation_weakening=21, compliance=10), every Appendix C phrase fires on its sample record, and the result is `RESULT: PASS`.
The ACs are met as written. The trouble starts off the sample. I ran 63 adversarial sentences through the YAML using the selfcheck's
own negation guard (imported, not modified). Results: **OK=10, FN=38, FP=15**. On pre-existing phrasing an adjuster would actually
exploit, the lexicon raised a high- or medium-strength hit on 3 of 28 probes. That includes all three subtle records of the
committed golden case `case_06_subtle_pre_existing`, one of which (P1) is a `must` flag. The negation guard has no clause boundary
at a comma. So "No acute fracture, chronic degenerative changes at C5-6", a standard radiology impression, has its `degenerative`
and `chronic` hits suppressed. Intake-form checkboxes ("Prior injuries: No.") and clinical negatives ("Did not present with loss
of consciousness.") raise high-strength flags that the FP notes don't cover. The lexicon's flag types also don't match the type
names in the golden set and REQUIREMENTS (no `hedge` category for R-TL-8, no mapping for `compliance`). A second signal is only
useful if it catches what the model misses. On this evidence it mostly catches what the model already sees.

Exercised: `python3 tools/board.py show T-009`. Ran `.venv/bin/python research/lexicon_selfcheck.py` → `RESULT: PASS`. Ran
`.venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py` (my script: loads app/llm/lexicon.yaml read-only, applies
every pattern with re.I and the reference guard `negated()` from research/lexicon_selfcheck.py). Full output is in
`artifacts/review-evidence/T-009-adjuster-probes.txt`. I read lexicon.yaml in full, lexicon_selfcheck.py, the
case_06_subtle_pre_existing .txt and .expected.json, sample.expected.json flags, REQUIREMENTS R-TL-8/R-FL-3/R-FL-4/§8 eval bar,
docs/LLM_VS_CODE.md row 12, and CONTRACT §5.2. I checked the lexicon's src-16 paraphrase against the source with curl (see
T-008 evidence file). `git log`: lexicon f419c3b (18:28:02) came after the golden set 47520a8 (18:25:39) and before REQUIREMENTS
round 2 64f766e (18:29:00).

```json
{"card": "T-009", "persona": "claims-adjuster-reviewer", "model": "claude-opus-5-5",
 "scope": "app/llm/lexicon.yaml + research/lexicon_selfcheck.py (commit f419c3b, read at HEAD 9e759a2); sample case + evals/golden/case_06_subtle_pre_existing; no app",
 "exercised": [
  "python3 tools/board.py show T-009 (3 ACs marked done)",
  ".venv/bin/python research/lexicon_selfcheck.py -> 'entries: 48 by type: pre_existing=17, causation_weakening=21, compliance=10' ... 'RESULT: PASS'",
  ".venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py > artifacts/review-evidence/T-009-adjuster-probes.txt -> 'TOTAL 63 OK=10 FN=38 FP=15'",
  "Probe set includes the 3 subtle records of evals/golden/case_06_subtle_pre_existing.txt verbatim",
  "Read app/llm/lexicon.yaml (699 lines), research/lexicon_selfcheck.py, evals/golden/case_06_subtle_pre_existing.expected.json, evals/golden/sample.expected.json flags",
  "Read spec/REQUIREMENTS.md R-TL-8, R-FL-3, R-FL-4, eval bar row 3; docs/LLM_VS_CODE.md row 12; CONTRACT §5.2",
  "git log --format='%h %ad %s' -8 (ordering of golden set, lexicon, requirements round 2)",
  "curl valawyersweekly src 16 to check lexicon delayed_onset rationale"
 ],
 "verdict": "changes",
 "scores": {"appendix_c_coverage": 5, "recall_on_adjuster_phrasing": 1, "precision_fp_control": 2, "negation_correctness": 2, "rationale_and_sourcing": 4, "contract_fit": 2},
 "findings": [
  {"severity": "major",
   "title": "Pre-existing recall is very low off the sample: 3 of 28 adjuster probes raise a flag, including 0 of 3 case_06 golden records",
   "evidence": "artifacts/review-evidence/T-009-adjuster-probes.txt, verbatim FN lines: '[FN] ... Symptoms predate the accident.'; '[FN] ... Prior to the accident she had intermittent neck pain.'; '[FN] ... Previously treated for neck pain by a chiropractor.'; '[FN] ... Patient was in a car accident in 2019.'; '[FN] ... Hx neck pain.'; '[FN] ... s/p ACDF 2015.'; '[FN] ... Has prior neck pain.'; '[FN] ... Previous cervical MRI in 2021.'; '[FN] ... Filed a workers' compensation claim for his back in 2020.'; '[FN] ... Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago.' (case_06 P1, level 'must'); '[FN] ... History: occasional stiffness in the mornings at baseline...' (case_06 P2); '[FN(low-only)] ... Patient notes the old shoulder problem is acting up again.' (case_06 P3). Causes: prior_injury_or_event (lexicon.yaml:104) noun list lacks pain/problems/symptoms/MRI/imaging/treated; dated_prior_event (lexicon.yaml:239) requires the year BEFORE the event noun; no entries for predate, Hx, s/p, previously, baseline, 'acting up again', workers' comp, 'since ... years ago'. case_06 was committed at 47520a8 before the lexicon (f419c3b).",
   "why_it_matters": "docs/LLM_VS_CODE.md row 12 justifies the lexicon as follows: 'a phrase list catches what a model overlooks.' The phrasings above are the ones I find in prior chiropractic and PCP records and use to discount a claim. If the LLM misses one, the lexicon misses it too, and the paralegal sends a demand with a prior condition I will find. On case_06, every catch will be LLM_ONLY → needs_review (R-FL-3), so the second signal adds nothing on the one golden case built to test it.",
   "fix": "Add or extend entries: predate/pre-date/antedate; 'prior to the (accident|collision|MVA) ... (had|with|pain|symptoms|treated)'; previously/formerly treated|seen; Hx and s/p abbreviations; 'at baseline'/'baseline (pain|stiffness|symptoms)'; '(acting up|flared) again'; 'since a ... (injury|accident|fall) ... ago'; '(car|auto|motor vehicle) accident in (19|20)\\d\\d' (year after noun); workers' comp(ensation) claim; prior/previous + (pain|problems|symptoms|complaints|MRI|imaging|x-rays|treatment). Add the case_06 records and these probes as examples.hit vectors.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-009-adjuster-probes.py: every pre_existing FLAG probe raises a high/medium hit except those explicitly documented as LLM-only in the entry's false_positive note; the 3 case_06 records each raise a pre_existing hit; selfcheck still PASS with no new appendix_c mismatches."},
  {"severity": "major",
   "title": "Negation guard has no comma/clause boundary and treats uncertainty or 'never resolved' as negation, so it suppresses the strongest defense findings",
   "evidence": "Probe output verbatim: '[FN(low-only)] ... No acute fracture, chronic degenerative changes at C5-6.' → 'negated:chronic[medium]:'chronic', degenerative[high]:'degenerative''; '[FN] ... Negative for fracture with moderate degenerative disc disease.' → 'negated:degenerative[high]'; '[FN] ... Without acute findings, with mild multilevel spondylosis.' → 'negated:degenerative_imaging_terms[high]'; '[FN] ... Denies headache, reports chronic neck pain since 2018.' → 'negated:chronic[medium]'; '[FN] ... Neck pain never fully resolved after the 2019 accident.' → 'negated:dated_prior_event[medium]:'2019 accident''; '[FN] ... Patient has not had neck pain since the 2019 MVA.' → negated; '[FN] ... Patient is not sure whether she had a prior neck injury.' → negated. Cause: lexicon.yaml:29 terminators omit ',' and 'with'/'reports'; research/lexicon_selfcheck.py:31 TOKEN = r\"[\\w'/-]+|;\" drops commas entirely; the 6-token window crosses into the next clause.",
   "why_it_matters": "'No acute X, [chronic/degenerative Y]' is how radiology impressions are written. These are the degenerative findings I lead with, and the binding semantics (lexicon.yaml:6-16) tell the backend to suppress them, leaving only an audit log line. 'Never fully resolved after the 2019 accident' is an admission of a prior accident with ongoing symptoms, and the guard treats it as a denial.",
   "fix": "Make ',' plus scope-breaking words ('with', 'reports', 'admits', 'endorses', 'but') terminators. Scope 'never'/'not' cues to the following clause only. Add 'not sure', 'unsure', 'unclear whether', 'never fully resolved', 'has not had ... since' as pseudo-negations. Have the binding semantics require that a suppressed high-strength hit still surface as needs_review when the LLM is silent, rather than being dropped.",
   "acceptance_test": "The 7 probes above raise their high/medium hit; examples.negated vectors still pass; new examples.hit vectors 'No acute fracture, chronic degenerative changes at C5-6.' and 'Neck pain never fully resolved after the 2019 accident.' added and passing in selfcheck."},
  {"severity": "major",
   "title": "Undocumented high-strength false positives on intake forms, long ROS lists, and clinical negatives",
   "evidence": "Probe output verbatim: '[FP] QUIET negation | Prior injuries: No.' → 'prior_injury_or_event[high/pre_existing]'; '[FP] ... Previous accidents: none.' → 'prior_injury_or_event[high/pre_existing]'; '[FP] ... ROS: Denies fever, chills, weight loss, chest pain, shortness of breath, or prior neck injury.' → 'prior_injury_or_event[high/pre_existing]' (cue outside 6-token window); '[FP] ... Did not present with loss of consciousness.' → 'no_show_cancel[high/compliance]:'Did not present''; '[FP] ... Comparison: No prior studies.' → 'comparison_prior_imaging[medium/pre_existing]:'Comparison: N''; '[FP] ... No change from prior visit; continue PT.' → comparison_prior_imaging[medium]. None of these is covered by the entries' false_positive notes (lexicon.yaml:110, 266-277, 583); post_cues (lexicon.yaml:28) lack 'no', 'none', 'n'.",
   "why_it_matters": "Every intake packet has 'Prior injuries: Y/N' checkboxes, and every ER note has an ROS denial list. A tool that raises a high-strength pre-existing flag on 'Prior injuries: No.' is wrong in a way the paralegal learns to ignore, and then she ignores the real one too. It also puts the ≥0.9 per-type precision bar (REQUIREMENTS eval row 3) at risk. A compliance flag on 'did not present with LOC' would read as a no-show to anyone skimming the export.",
   "fix": "Add post-colon negation: '<cue>: (no|none|denies|negative|n)' suppresses. Treat ROS-list denials as scoped to the list (cue to end of sentence when the sentence starts 'ROS'/'Denies'). Restrict no_show_cancel 'did not present' to 'did not present for (appointment|visit|session|therapy|follow-up)'. Exclude 'Comparison: no prior' and require an imaging noun after 'no change from prior'. Add each as an examples.miss or negated vector.",
   "acceptance_test": "The 6 probes above produce no high/medium hit; corresponding vectors added to lexicon.yaml examples and selfcheck PASS."},
  {"severity": "major",
   "title": "Flag taxonomy doesn't match the golden set or REQUIREMENTS: no `hedge` category for R-TL-8, `compliance` unmapped, self-report mixed in with hedges",
   "evidence": "lexicon.yaml:19 'flag_types: [pre_existing, causation_weakening, compliance]'. REQUIREMENTS.md:57 'Four types: gap, conflict, prior_condition, causation'. REQUIREMENTS.md:52 (R-TL-8): 'a sentence matching the `hedge` category of `app/llm/lexicon.yaml` ... Patient self-report phrases are not hedges'. evals/golden/sample.expected.json K2 (missed appointments) has \"type\": \"causation\", but lexicon.yaml:564 types missed_appointments as 'compliance'. patient_attributes_causation (:387) and patient_reports_generic (:399) share flag_type causation_weakening with may_represent (:283) and correlate_clinically (:296). No mapping table exists in the YAML.",
   "why_it_matters": "The backend can't implement R-TL-8 from this file. If it treats causation_weakening as the hedge category, records 3, 5 and 9 ('Patient reports…/states…') wrongly trigger EXCERPT_OMITS_QUALIFIER. If `compliance` isn't mapped to `causation`, the missed-appointment hit never pairs with the LLM's causation flag, so golden K2 always ends up LEXICON_ONLY/LLM_ONLY needs_review. (REQUIREMENTS round 2 landed 58 s after this commit, so this is a reconciliation job, not negligence, but it has to be done before the M2 build.)",
   "fix": "Add a per-entry `category` (hedge | self_report | prior | degenerative | compliance | recovery_context ...) and a top-level `maps_to` table from flag_type to spec type (pre_existing→prior_condition/pre_existing, causation_weakening→causation, compliance→causation). Mark may_represent, correlate_clinically, possibility_terms, cannot_exclude, nonspecific_indeterminate as category hedge; the patient_* entries as self_report.",
   "acceptance_test": "yaml.safe_load(lexicon)['entries'] where category=='hedge' contains may_represent and correlate_clinically and no patient_* entry; every flag_type has a maps_to value in {prior_condition|pre_existing, causation}; selfcheck asserts both."},
  {"severity": "major",
   "title": "Causation and credibility attacks I use are absent: objective-negative exams, out-of-proportion complaints, MIST scene facts, repeat accidents, attorney-referral variants",
   "evidence": "Probe output verbatim, all '[FN]' with no hit: 'Subjective complaints out of proportion to exam findings.'; 'No objective findings.'; 'Neurological exam within normal limits. Full cervical ROM. No paraspinal spasm.'; 'Patient was rear-ended again in March.'; 'Minimal damage to vehicle; airbags did not deploy.'; 'Ambulatory at scene, refused transport.'; 'Patient drove himself to urgent care three days later.'; 'Referred to this clinic by attorney after initial PCP visit.' (litigation_referral, lexicon.yaml:548, needs 'referred by'); compliance: 'Patient declined ambulance transport.', 'Attended 4 of 12 scheduled visits.', 'Released to full duty without restrictions.' all FN.",
   "why_it_matters": "EMS run reports and ER triage notes routinely carry 'ambulatory at scene', 'minimal vehicle damage', 'airbags not deployed', 'refused transport', and the cited Claims Journal checklist (AA src 1) names transport, vehicle damage, and treatment start. 'Out of proportion' and 'no objective findings' are what an IME report quotes. 'Rear-ended again' is the JLG Trucking second-accident fact the lexicon claims to cover (intervening_event, :452), but the pattern needs 'another/second/subsequent'. The paralegal never sees these.",
   "fix": "Add entries: subjective_exceeds_objective ('out of proportion', 'no objective (findings|evidence)', 'subjective complaints (only|exceed)'); normal_exam ('within normal limits|WNL|full (ROM|range of motion)|no (paraspinal )?spasm|no tenderness', low/medium context like normal_imaging); mist_scene ('minimal|minor|no visible (vehicle )?damage', 'airbags? (did not|not) deploy', 'ambulatory at (the )?scene', 'refused|declined transport', 'self-transported|drove (himself|herself)'); 'again' after an accident verb for intervening_event; 'by (his|her|the)? attorney' anywhere after 'referred'; 'attended N of M'. Coordinate with the T-008 MIST/delay rows.",
   "acceptance_test": "Re-run artifacts/review-evidence/T-009-adjuster-probes.py: the 11 probes listed raise at least a low hit, and the scene/out-of-proportion/repeat-accident ones raise medium or high."},
  {"severity": "minor",
   "title": "delayed_onset rationale overstates its source",
   "evidence": "lexicon.yaml:443: 'Virginia record-review example: symptoms not reported until weeks later'. AA src 16 verbatim: 'did not report injury until eight days later when he was seen at an urgent care facility'.",
   "why_it_matters": "A rationale that inflates its source is the same kind of overstatement the tool is meant to prevent. Eight days is a delayed-first-treatment fact, not 'weeks'.",
   "fix": "Quote 'eight days later' and cite it under a delay-to-first-treatment entry as well.",
   "acceptance_test": "grep -n 'eight days' app/llm/lexicon.yaml matches the delayed_onset rationale."},
  {"severity": "minor",
   "title": "discharged_from_care is high-strength compliance even on a successful discharge",
   "evidence": "Probe: '[FP] QUIET benign | Discharged from PT, goals met.' → 'discharged_from_care[high/compliance]:'Discharged from PT''. lexicon.yaml:596 acknowledges it ('the LLM decides').",
   "why_it_matters": "'Goals met' is the plaintiff's best compliance fact. A high-strength compliance flag on it is noise the paralegal has to dismiss on every completed course of PT.",
   "fix": "Add a post-window suppressor for 'goals met|completed|plan of care completed', or lower to medium unless a missed/no-show/non-compliance cue is in the same sentence.",
   "acceptance_test": "'Discharged from PT, goals met.' raises no high-strength hit; 'Discharged from PT after two missed appointments.' still does (appendix_c [6])."},
  {"severity": "minor",
   "title": "Selfcheck verifies only the hand-picked examples; nothing exercises the golden cases committed before the lexicon",
   "evidence": "research/lexicon_selfcheck.py:19-29 hardcodes only the 9 Appendix A excerpts; evals/golden/case_06_subtle_pre_existing.txt (commit 47520a8, earlier than f419c3b) is not loaded, and its 3 must/should pre_existing records all miss (finding 1).",
   "why_it_matters": "A self-check that only replays the author's own examples can't catch recall gaps. That is why an AC-level PASS coexists with 38 FNs.",
   "fix": "Have the selfcheck (or a qa test) run the lexicon over every evals/golden/*.txt and compare to expected pre_existing/causation evidence excerpts, reporting lexicon recall per case.",
   "acceptance_test": "Selfcheck output includes a per-golden-case lexicon recall line, and case_06 P1 is a hit."}
 ],
 "whats_right": [
  "All Appendix C phrases fire on exactly their sample records (selfcheck PASS, no appendix_c mismatches); don't regress this.",
  "'Patient reports missing 3 days of work' does not hit missed_appointments, and 'May return to work' does not hit may_represent; good precision on the sample traps.",
  "Every entry carries a rationale, source, false-positive note, strength, and test vectors; the low-strength tier for context-only hits (CT head negative) is the right call."
 ],
 "questions_for_chris": [
  "Should MIST/scene facts from EMS reports (speed, vehicle damage, ambulatory, transport) be surfaced as review flags at all, or only as context? They are adjuster attacks but are not one of the four required flag types."
 ]}
```
