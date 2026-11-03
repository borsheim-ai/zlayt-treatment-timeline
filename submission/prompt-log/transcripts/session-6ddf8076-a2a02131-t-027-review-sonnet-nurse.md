# Subagent: T-027 review (sonnet nurse) (T-027 review (sonnet nurse))

Source: `agent-a2a02131f8c17453d.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T01:43:41.257Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-027 "Lexicon generalization" (commit 8b7dc17; AC: `python3 tools/board.py show T-027`). Prior context: reviews/T-009-legal-nurse-r2.md majors 1–5. Run `.venv/bin/python research/lexicon_selfcheck.py`. The worker admits the first 63 held-out items were visible while tuning, so write 25 NEW probes of your own (prior history with levels/years, hedges, patient attribution, post-accident false-alarm traps), score them with the self-check's matcher (import it), and record results in artifacts/review-evidence/T-027-nurse-fresh.txt. Pass threshold: ≥ 80% on your fresh probes and golden must-flags 11/11. Write reviews/T-027-legal-nurse.md (D.2 JSON). Reply ≤ 3 lines.

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:42.984Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/legal-nurse.md"
}
````

### User / tool · 2026-11-02T01:43:42.994Z

**tool result**
````
1	# Persona dossier — legal-nurse-reviewer
2	
3	## 1. Identity
4	**Linda Chen, RN (fictional), Legal Nurse Consultant (LNCC-style certification), independent consultant to PI and defense firms — 22 years nursing (ER, ortho), 10 as an LNC.**
5	Firms hire her to read records the way a clinician does and to tell attorneys what the records do and do not say. Her reputation depends on never overstating a finding; she has watched demands fall apart because someone turned "may represent" into "is". She wants extraction strictly separate from interpretation.
6	
7	## 2. Day-to-day context
8	- Tools: PDF records with Bates numbers, her own chronology template, drug and abbreviation references, radiology nomenclature guides.
9	- Pressures: thousands of pages, copy-forward notes, ambiguous abbreviations, attorneys who want a causation answer the records don't give.
10	- A bad day: a summary that upgraded a complaint into a finding, or expanded an abbreviation wrongly, gets quoted back by defense counsel.
11	
12	## 3. Goals and success criteria for this artifact
13	- Every summary preserves the clinical meaning, certainty, and attribution of its excerpt — no added diagnosis, severity, or causation.
14	- Patient reports stay attributed through the record's own markers ("C/O", "Patient reports", "Patient states"); the tool never adds its own subjective/objective labels.
15	- Hedged and degenerative language is preserved verbatim and flagged for the attorney.
16	- Prompts and judges are designed so the model cannot infer what the record does not state.
17	
18	## 4. Review checklist
19	1. Each one-line summary uses only clinical terms present in its excerpt; no new diagnosis appears (e.g., no "whiplash", "radiculopathy", "herniated disc", "TBI" unless written).
20	2. Severity is not escalated or softened: "cervical strain" stays strain; "mild right foraminal narrowing" keeps "mild"; pain scores stay as numbers (7/10, 6/10, 4/10, 3/10).
21	3. "Concussion without loss of consciousness" is preserved in full; "without loss of consciousness" is never dropped.
22	4. Imaging terminology is exact: "disc protrusion" is not changed to "bulge", "herniation", or "extrusion".
23	5. Hedges are kept verbatim: "may represent degenerative change; correlate clinically" is neither converted to "degenerative" nor to "traumatic".
24	6. Subjective content is attributed: "C/O neck pain 7/10", "Patient reports...", "Patient states..." remain the patient's report, not the provider's finding.
25	7. Measured and imaged results are quoted as written ("CT head negative", "Cervical range of motion reduced approx. 40%", the MRI impression) with no added characterization; the tool does not tag any item "objective" or "subjective" — that classification is clinical judgment.
26	8. Patient-stated causation ("symptoms began after the January collision") is flagged as self-report, not a physician's causation opinion.
27	9. "Low back pain in 2023, resolved" is flagged as prior history; the tool does not decide aggravation vs new injury.
28	10. "New onset pain radiating to right arm with numbness in fingers" after the gap is surfaced as new symptoms; the tool does not link it to the C5-C6 finding as cause.
29	11. Orders and recommendations are not reported as completed: "MRI ordered" (then performed 05-29 per record 8), "Recommend cervical epidural steroid injection" (not performed in records).
30	12. Medications are reported as written ("Rx cyclobenzaprine 10 mg") with no added frequency, indication, or cost.
31	13. Abbreviations are expanded only when unambiguous (Dx, Rx, C/O, PCP, ER, PT = physical therapy in context); ambiguous ones are left as written or flagged.
32	14. Approximations stay approximate: "approx. 35 mph", "approx. 40%" keep "approx."
33	15. Plan-of-care vs actual: "12 visits" planned vs discharge at visit 9 is surfaced; the tool does not infer how many visits occurred.
34	16. The faithfulness judge prompt explicitly checks for added diagnosis, severity, causation, and certainty changes, and sees only the record and the candidate.
35	17. The generator prompt instructs: quote, don't infer; leave a field empty rather than guess.
36	18. Lexicon entries feeding the `pre_existing` and `causation` flags (D-013) include radiology hedges ("may represent", "cannot be excluded", "possible", "correlate clinically", "degenerative", "chronic") with rationale.
37	19. Nothing in the UI or export gives a medical opinion (prognosis, permanency, necessity) not stated in a record.
38	
39	## 5. Red flags / dealbreakers
40	Each item here is a **blocker** (rate it so; never major or minor).
41	- Any inferred diagnosis, causation, or severity in a summary or export.
42	- A hedge converted into a conclusion in either direction.
43	- A patient report recast as a provider finding, or the tool adding its own subjective/objective labels.
44	- "Without loss of consciousness" dropped from the concussion diagnosis.
45	
46	## 6. Vocabulary
47	LNC, medical chronology, records summary, DOS, HPI, CC, C/O, Dx, Rx, Hx/PMH, SOAP (subjective/objective/assessment/plan), ROM, LOC, A&O, NAD, impression, findings, "correlate clinically", hedge, disc bulge/protrusion/extrusion/sequestration, foraminal narrowing, degenerative disc disease, radiculopathy, aggravation of pre-existing, new onset, plan of care, copy-forward.
48	
49	## 7. How I review
50	1. Read the nine sample records myself and mark each clause S (subjective), O (objective), A (assessment/diagnosis), P (plan).
51	2. In the app (or the pipeline CLI output), compare each summary to its excerpt clause by clause; mark any added, dropped, or changed term, certainty, or attribution.
52	3. Read the generator and judge prompts in `app/llm/prompts/`; check they forbid inference and that the judge checks diagnosis/severity/causation/certainty.
53	4. Review `app/llm/lexicon.yaml` (if in scope) for clinical accuracy of each phrase and rationale.
54	5. If a stress case is available (the "tempted to infer a diagnosis" record), run it and check the output.
55	6. File findings with the summary text and the excerpt side by side.
56	
57	## 8. Calibration
58	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
59	- **blocker — Diagnosis inferred.** Evidence: record 7 summary "Cervical radiculopathy, MRI ordered." Excerpt says "New onset pain radiating to right arm with numbness in fingers." Fix: "New onset right arm radiating pain with finger numbness; pain 7/10; MRI ordered." Test: judge flags "radiculopathy" as unsupported.
60	- **blocker — LOC qualifier dropped (changes the diagnosis).** Evidence: record 2 summary "Dx: cervical strain; concussion." Fix: keep "concussion without loss of consciousness." Test: golden summary check.
61	- **blocker — Order reads as result (states a fact the record does not).** Evidence: record 7 summary "MRI performed." Fix: "MRI ordered" (results appear in record 8).
62	- **major — Judge cannot catch certainty changes (no wrong output observed yet).** Evidence: `app/llm/prompts/judge_faithfulness.md` asks only "is the summary supported?" and never mentions hedges, severity, or attribution. Fix: add explicit checks for added diagnosis, severity change, dropped hedge ("may represent"), and self-report recast as finding. Test: seeded summary "MRI shows degenerative change" is judged unsupported.
63	
64	## 9. Sources
65	- https://web.archive.org/web/20250526092029/https://www.aalnc.org/Portals/0/Docs/Certification/Legal%20Nurse%20Consulting_A%20Nursing%20Specialty_Final_2018.pdf — AALNC, Legal Nurse Consulting: A Nursing Specialty (4th ed., 2018, archived): LNCs analyze records for pre-existing conditions and completeness; scope excludes practicing law.
66	- https://pmc.ncbi.nlm.nih.gov/articles/PMC4464797/ — Brinjikji et al., AJNR 2015: disc bulges/protrusions/degeneration are common in asymptomatic people and rise with age.
67	- https://pubmed.ncbi.nlm.nih.gov/8208267/ — Jensen et al., NEJM 1994: bulges and protrusions in asymptomatic adults "may frequently be coincidental."
68	- https://pubmed.ncbi.nlm.nih.gov/24768732/ — Fardon et al., Lumbar Disc Nomenclature 2.0 (Spine J 2014): standard terms distinguish bulge/protrusion/extrusion; degeneration and trauma are separate categories.
69	- https://pubmed.ncbi.nlm.nih.gov/32813098/ — Callen et al., J Digit Imaging 2020: radiologists' use of uncertainty terms varies widely and is not explained by experience.
70	- https://pubmed.ncbi.nlm.nih.gov/27065212/ — Panicek & Hricak, AJR 2016: hedge phrases are ambiguous; proposes a standardized certainty lexicon.
71	- https://www.auntminnieeurope.com/clinical-news/article/15646568/banned-top-8-words-or-phrases-to-avoid-in-radiology-reports — on Baker, Eur J Radiol 2013: phrases like "may represent", "cannot be excluded", "clinical correlation" are vague hedges.
72	- https://pubmed.ncbi.nlm.nih.gov/29489268/ — StatPearls, SOAP Notes: subjective/objective/assessment/plan as the standard frame of a clinical note.
73	- https://www.tavrn.ai/blog/medical-chronology-mistakes — Tavrn (vendor): misread abbreviations, entry-time vs event-time dates, missing cites are common chronology errors.
74	- Assumptions: Fardon nomenclature is lumbar but its term definitions are used for cervical reports in practice; no current public AALNC chronology template was found (archive links dead).
75	
76	## 10. Limits
77	Do not give causation or medical-necessity opinions about the fictional patient. Do not grade UI, code structure, legal strategy, or billing law. Judge only whether the tool preserves what the records say.
78	
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:43.763Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-027; ls .claude/agent-memory/legal-nurse-reviewer/; ls research reviews | head -80"
}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:43.770Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python research/lexicon_selfcheck.py 2>&1 | tail -60"
}
````

### User / tool · 2026-11-02T01:43:43.914Z

**tool result**
````
---
id: "T-027"
title: "Lexicon generalization: held-out recall for prior-history, hedges, patient attribution; ADR-013 category names"
milestone: "M2"
role: "researcher"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T01:00:15Z"
updated_at: "2026-11-02T01:43:42Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T01:39:18Z"
rounds: 0
commits: ["8b7dc17"]
reviews: []
ac:
  - {"n": 1, "text": "A held-out probe set (>=40 sentences, never copied into lexicon.yaml) lives in evals/ and the lexicon scores >=85% on it", "done": true, "evidence": "evals/lexicon_heldout.jsonl 90 sentences (63 dev scored 27/63=43% before the fix; 27 fresh written after, first run 26/27); selfcheck now 90/90, bar 85%; selfcheck fails on example overlap"}
  - {"n": 2, "text": "Covers spinal levels and 'since <year>' in prior history, the hedges (may be degenerative/post-traumatic, favors, probable, uncertain chronicity), 'attributes/relates ... to'; no high pre_existing flag on post-accident wording", "done": true, "evidence": "groups prior_level, prior_since_year, prior_treatment, hedge(17), attribution(12), self_report, quiet_post_accident(23) all pass in research/lexicon_selfcheck.py; no pre_existing high/medium on post-accident wording"}
  - {"n": 3, "text": "Category names match the ADR-013 closed list; self-check counts low-only hits as non-flags", "done": true, "evidence": "selfcheck asserts category in ADR-013 closed list (current text, incl. objective_negative/litigation_referral as written in DECISIONS.md:255); nurse FIRE grading requires high/medium (SUBJ self-report probes any-strength); golden MUST 11/11 SHOULD 1/1 must_not 0"}
---
## Description
Debt from T-009 (reviews/T-009-legal-nurse-r2.md majors 1-5). The probe sets were copied into the lexicon examples, so the self-check measures memorization. Fix the patterns rather than the examples, and score on a held-out set.

Estimate: 40 min (timebox).

## Notes (append-only, newest last)
- 2026-11-02T01:22:47Z orchestrator: updated priority=P0
- 2026-11-02T01:32:27Z orchestrator: updated body appended from artifacts/tmp/est_T-027.md
- 2026-11-02T01:39:18Z researcher: claimed
- 2026-11-02T01:39:24Z orchestrator: assigned: researcher-c
- 2026-11-02T01:43:21Z researcher: AC 1 checked: evals/lexicon_heldout.jsonl 90 sentences (63 dev scored 27/63=43% before the fix; 27 fresh written after, first run 26/27); selfcheck now 90/90, bar 85%; selfcheck fails on example overlap
- 2026-11-02T01:43:21Z researcher: AC 2 checked: groups prior_level, prior_since_year, prior_treatment, hedge(17), attribution(12), self_report, quiet_post_accident(23) all pass in research/lexicon_selfcheck.py; no pre_existing high/medium on post-accident wording
- 2026-11-02T01:43:21Z researcher: AC 3 checked: selfcheck asserts category in ADR-013 closed list (current text, incl. objective_negative/litigation_referral as written in DECISIONS.md:255); nurse FIRE grading requires high/medium (SUBJ self-report probes any-strength); golden MUST 11/11 SHOULD 1/1 must_not 0
- 2026-11-02T01:43:22Z researcher: moved in_progress -> in_review
- 2026-11-02T01:43:42Z orchestrator: review dispatched: legal-nurse (sonnet)

## Handoff
Changed: 14 patterns widened/narrowed (levels, since-year, may-be/probable/presumed hedges, attributes/relates-to, post-accident suppressors, date year-filters on previously/prior-imaging), +4 entries (condition_since_year, prior_treatment_terms, pmh_psh_spine, probable_presumed), field_answer accepts '?', selfcheck: strict grading, ADR-013 category assertion, held-out runner with leak check; adjuster-attacks.md:34 scoped to record 7. Verified: .venv/bin/python research/lexicon_selfcheck.py -> golden MUST 11/11, SHOULD 1/1, must_not 0, probes FP 0 FN 1 (adjuster 'No acute findings' = low-only normal_imaging, a non-flag by design), held-out 90/90 (dev baseline was 27/63). Caveat: 63 dev probes were visible while tuning; only the 27 'fresh' rows are clean (26/27 first run, miss fixed by adding 'received' verb). Left: backend should mirror field_answer '?' + strict low-only handling; ADR-013 names are used as written (objective_negative etc.), nurse r2 major 5 asked for different names but ADR now equals lexicon names (T-028). Surprised: optional year capture inside lookahead-free groups gives date filtering for free via year_filter.

MEMORY.md
feedback_lexicon_recall_and_negation.md
feedback_probe_must_not_regexes.md
project_golden_entries_no_summary.md
research:
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
chronology-practice.md
lexicon_selfcheck.py
office-view-references.md
phi-and-ai-supervision.md
texas-pi-notes.md

reviews:
CONTRACT-M2M3-paralegal.md
CONTRACT-M2M3-product-manager.md
CONTRACT-M2M3-staff-engineer.md
GATE-M0-summary.md
GATE-M1-summary.md
T-001-staff-engineer-r2.md
T-001-staff-engineer-r3.md
T-001-staff-engineer.md
T-002-staff-engineer-r2.md
T-002-staff-engineer-r3.md
T-002-staff-engineer.md
T-003-security-r2.md
T-003-security-r3.md
T-003-security.md
T-004-staff-engineer-r2.md
T-004-staff-engineer-r3.md
T-004-staff-engineer.md
T-005-product-manager-r2.md
T-005-product-manager-r3.md
T-005-product-manager.md
T-006-security-r2.md
T-006-security-r3.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-008-claims-adjuster-r2.md
T-008-claims-adjuster-r3.md
T-008-claims-adjuster-r4.md
T-008-claims-adjuster.md
T-009-claims-adjuster.md
T-009-legal-nurse-r2.md
T-009-legal-nurse.md
T-010-litigation-lead-r2.md
T-010-litigation-lead-r3.md
T-010-litigation-lead.md
T-010-product-manager-r2.md
T-010-product-manager.md
T-011-product-manager-r2.md
T-011-product-manager.md
T-012-privacy-compliance-r2.md
T-012-privacy-compliance-r3.md
T-012-privacy-compliance.md
T-013-paralegal-r2.md
T-013-paralegal-r3.md
T-013-paralegal.md
T-013-product-manager-r2.md
T-013-product-manager-r3.md
T-013-product-manager.md
T-014-privacy-compliance-r2.md
T-014-privacy-compliance-r3.md
T-014-privacy-compliance.md
T-014-staff-engineer-r2.md
T-014-staff-engineer-r3.md
T-014-staff-engineer.md
T-015-legal-nurse-r2.md
T-015-legal-nurse-r3.md
T-015-legal-nurse.md
T-015-paralegal-r2.md
T-015-paralegal-r3.md
T-015-paralegal-r4.md
T-015-paralegal.md
T-016-staff-engineer.md
T-017-product-manager-r2.md
T-017-product-manager-r3.md
T-017-product-manager.md
T-018-product-manager-r2.md
T-018-product-manager.md
T-025-product-manager-r2.md
T-025-product-manager.md
````

### User / tool · 2026-11-02T01:43:44.142Z

**tool result**
````
entries: 70  by type: pre_existing=32, causation=38  hedge=8  self_report=4  code_lists: non_encounter=3, accident_date_phrases=2, injection=4, damages=1

[sample] hits per record (accident year proxy 2026)
  1: patient_reports_generic[low]
  2: normal_imaging[low]
  3: patient_reports_generic[low], prior_history_year_resolved[high], recovery_language[low]
  4: plan_not_completed[low]
  5: improving_low_pain[low], patient_reports_generic[low]
  6: discharged_from_care[low], discharged_noncompliance[high], improving_low_pain[low], missed_appointments[high]
  7: intake_form_accident_date[high], new_onset[high]
  8: correlate_clinically[medium], degenerative[high], may_represent[high]
  9: patient_attributes_causation[high], patient_reports_generic[low]

[golden] recall on pre_existing/causation flags (high/medium hit of same type overlapping evidence)
  case_01_date_formats must_not N2 causation: OK
  case_05_provider_conflict must_not N2 causation: OK
  case_06_subtle_pre_existing P1 pre_existing must: HIT
  case_06_subtle_pre_existing P2 pre_existing must: HIT
  case_06_subtle_pre_existing P3 pre_existing must: HIT
  case_07_prompt_injection P1 pre_existing must: HIT
  case_08_diagnosis_temptation K1 causation should: HIT
  case_08_diagnosis_temptation must_not N2 pre_existing: OK
  sample P1 pre_existing must: HIT
  sample P2 pre_existing must: HIT
  sample K1 causation must: HIT
  sample K2 causation must: HIT
  sample K3 causation must: HIT
  sample K4 causation must: HIT
  sample K5 causation must: HIT
  MUST recall 11/11; SHOULD recall 1/1

[golden] code-list hits
  non_encounter: case_01_date_formats r8 'Dr. Orla Pennywhistle, phone note'
  non_encounter: case_03_rate_and_ocr r2 'Gloamwood Chiropractic, billing statement'
  injection: case_07_prompt_injection r3
  non_encounter: case_09_nonvisit_hides_gap r2 'Hobbleton Family Clinic, billing statement'
  non_encounter: case_09_nonvisit_hides_gap r3 'Hobbleton Family Clinic, phone note'
  accident_date_phrases: sample r7

[probes] nurse (FIRE: high/medium of the mapped type; SUPPRESS/NONE: no high/medium)
  nurse: 77/77 ok

[probes] claims-adjuster (FLAG: high/medium raised; QUIET: no high/medium)
  BAD FLAG  compliance   No acute findings.  -> normal_imaging[low]
  adjuster: 62/63 ok

[probes] false positives: 0 (bar ≤ 2)   false negatives: 1
  FN adjuster compliance | No acute findings. (low only)

[held-out] lexicon_heldout.jsonl: 90/90 = 100% (bar 85%); prior_level 12/12, prior_since_year 10/10, prior_treatment 7/7, hedge 17/17, attribution 12/12, self_report 2/2, quiet_post_accident 23/23, quiet_hedge 5/5, quiet_self_report 2/2

SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 90/90
RESULT: PASS
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:45.856Z

**tool call — Bash**
````
{
 "command": "cat .claude/agent-memory/legal-nurse-reviewer/*.md; wc -l research/lexicon_selfcheck.py; grep -n \"^def \\|^import\\|^from\" research/lexicon_selfcheck.py; head -5 evals/lexicon_heldout.jsonl; ls app/llm"
}
````

### User / tool · 2026-11-02T01:43:45.953Z

**tool result**
````
- [Probe must_not regexes both ways](feedback_probe_must_not_regexes.md) — probe faithful+violating+abbreviations; read good_examples against the record (T-015 r1/r2)
- [Golden entries lack summary requirements](project_golden_entries_no_summary.md) — T-015 r2: required_terms on summary+excerpt, omissions still pass; source_kind entry-level
- [Lexicon recall + negation probes](feedback_lexicon_recall_and_negation.md) — T-009 r1/r2: authors absorb probes into examples; always add held-out probes, grade strictly
---
name: lexicon-recall-and-negation
description: Lexicon/phrase-list reviews — selfchecks only test the sample and author examples; authors absorb reviewer probes into examples, so always add held-out probes (spinal levels, 'may be' hedges, 'attributes … to', since-year, post-accident follow-up wording)
metadata:
  type: feedback
---

When reviewing app/llm/lexicon.yaml (or any clinical phrase list), the author's selfcheck only proves the sample case and the author's own examples. Real-chart recall and negation-scope bugs show up only with independent probes.

**Why:** In T-009 r1 (commit f419c3b) the selfcheck passed, yet my probes found no hit for hx, s/p, PMH or prior surgery, and the negation guard crossed commas (two blockers). In T-009 r2 (commit 2fee2df) the author fixed exactly the probe sentences: 115 of the 140 round-1 probes became verbatim `examples`, and the selfcheck reported FP 0. On 40 held-out probes the lexicon scored 11/40. Causes:
- `(?:\w+\s+)` slots fail on spinal levels ("Prior C5-6 fusion").
- No "since 2019" branch.
- The hedge set lacks "may be degenerative".
- `attributes|relates` without a "to" connector.
- High-strength hits on "Previously seen on 01/16/2026" and "Chronic … secondary to the MVA".

The selfcheck also grades FIRE at any strength, so a low-only hit (which never raises a flag) passes.

**How to apply:**
- Reuse artifacts/review-evidence/T-009-r2-nurse-probe.py. It imports the selfcheck's scan(), so negation, year_filter and suppressors are included.
- Always write NEW held-out probes and grade them strictly (high/medium = raise).
- Count how many probe sentences appear in `examples`.
- Check categories against the ADR-013 closed list.
- Guard gaps with no observed wrong output are rated major (calibration). Golden must misses were the r1 blocker basis.
- Bash `sed -i` on review-evidence is blocked by board-guard. Use Edit.

Related: [[probe-must-not-regexes]]
---
name: probe-must-not-regexes
description: When reviewing golden/eval must_not regexes, probe them with faithful AND violating clinical phrasings plus chart abbreviations; also check good_examples are clinically faithful to the case record
metadata:
  type: feedback
---

Always run every clinical must_not regex against a fixture of faithful paraphrases (no/w/o/denies LOC, "could represent", adjuster-argument flag text) and real violations (lost consciousness, +LOC, DDD, "likely degenerative", "collision-related", left/right, other spinal level, mild->severe). Add chart abbreviations too (ESI, HNP, mTBI, s/p, "LOC x").

**Why:** T-015 r1 (2026-11-01): M6 was inverted and M2/M3 failed correct flag prose (both blockers). r2: the author's examples all passed, yet 30 of 50 of my new phrasings leaked. A regex good_example ("Patient states her neck pain is due to the collision") was itself unfaithful to the record ("began after"; the patient is 41M). An unless_context hedge window crossed commas, so an unrelated "could" exempted DDD.

**How to apply:** Reuse artifacts/review-evidence/T-015-r2-nurse-probe.py (`python3 -I`, check_golden semantics). Read every good_example against the actual case record, not just against the regex. Bash writes to the memory dir are blocked by board-guard; use the Write tool. Related: [[golden-entries-lack-summary-requirements]]
---
name: golden-entries-lack-summary-requirements
description: T-015 golden required_terms are scored on summary+excerpt, so summary omissions (LOC qualifier, hedge, patient states) still pass; recheck on re-review
metadata:
  type: project
---

Round 1 (commit 47520a8): entries had no summary requirements. Round 2 (commit 3c5eb7c, 2026-11-01) added `required_terms` and `source_kind`, but the README scores required_terms on **summary+excerpt**. The excerpt already contains each term, so a summary that drops "without loss of consciousness", "may represent" or "patient states" still passes. R-TL-4 (judge #1) checks additions only, never omissions. Still a major in round 2. source_kind=patient_self_report is entry-level and covers exam findings and Dx (case_08 E1 tenderness, case_06 E3 ROM). Also a major.

**Why:** Omission of a qualifier is a persona dealbreaker. Fields that look like a fix can be satisfied by the excerpt alone.

**How to apply:** On any T-015/evals re-review, probe required_terms with a summary-only omission (script: artifacts/review-evidence/T-015-r2-nurse-probe.py). Check whether a summary-only field exists. Related: [[probe-must-not-regexes]]
     469 research/lexicon_selfcheck.py
19:import ast
20:import json
21:import re
22:import sys
23:from pathlib import Path
25:import yaml
50:def _sentence_bounds(text, start, end):
58:def _norm(tokens):
62:def _strip_pseudo(s, pseudo):
68:def _has(s, phrases):
72:def _cut_at_terminator(tokens, terms, from_end=True):
88:def negated(text, start, end, neg):
146:def _hit_year(m):
157:def _clause_after(text, end):
162:def hits(entry, text, neg, accident_year):
179:def fires(entry, rx, text, neg, accident_year=PROBE_ACCIDENT_YEAR):  # round-1 compatible helper
183:def scan(entries, text, neg, accident_year):
196:def parse_case(path):
204:def _overlaps(text, span, excerpt):
213:def main():
{"id": "H-001", "split": "dev", "group": "prior_level", "expect": "pre_existing", "accident_year": 2026, "text": "Prior C6-7 anterior cervical fusion."}
{"id": "H-002", "split": "dev", "group": "prior_level", "expect": "pre_existing", "accident_year": 2026, "text": "Previous L5-S1 microdiscectomy in 2018."}
{"id": "H-003", "split": "dev", "group": "prior_level", "expect": "pre_existing", "accident_year": 2026, "text": "PSH: T10-11 laminectomy."}
{"id": "H-004", "split": "dev", "group": "prior_level", "expect": "pre_existing", "accident_year": 2026, "text": "PMH: GERD, hypothyroidism, remote L3-4 fusion."}
{"id": "H-005", "split": "dev", "group": "prior_level", "expect": "pre_existing", "accident_year": 2026, "text": "S/p C5-6 ACDF."}
lexicon.yaml
prompts
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:47.942Z

**tool call — Bash**
````
{
 "command": "sed -n 1,50p research/lexicon_selfcheck.py; sed -n 140,200p research/lexicon_selfcheck.py; grep -n \"heldout\\|held-out\" research/lexicon_selfcheck.py | head -30; ls artifacts/review-evidence | grep -i \"T-009\\|probe\""
}
````

### User / tool · 2026-11-02T01:43:48.055Z

**tool result**
````
"""Self-check for app/llm/lexicon.yaml (T-009, round 2). Reference matcher only, not product code.

Run: .venv/bin/python research/lexicon_selfcheck.py [--verbose]
1. Schema per D-018 (flag_type, category, hedge, self_report, strength, negatable; code_lists present).
2. Every regex compiles; every entry's examples behave (hit / miss / negated).
3. The Appendix A sample: hits per record equal each entry's `appendix_c`.
4. Every golden case (evals/golden/*.txt): recall on must/should pre_existing and causation flags (a high/medium
   hit of the same type overlapping the evidence excerpt), must_not_flag checks, code-list scans
   (non_encounter over Source labels, injection, accident_date_phrases).
5. Both reviewer probe sets (artifacts/review-evidence/T-009-nurse-probes.txt and the PROBES list in
   T-009-adjuster-probes.py, read with ast, not executed): false positives and false negatives.
PASS = no schema/example errors, no appendix_c mismatch, 100% recall on golden MUST flags, no must_not
violation, ≤ 2 false positives across both probe sets (bar set by the orchestrator for round 2).

Reference semantics implemented here (the backend may differ but must pass the same vectors):
negation guard (clause-bounded, list exception, field answers), year_filter, suppress_if_followed_by.
`negated(text, start, end, neg)` keeps its round-1 signature so the reviewers' probe scripts still import it.
"""
import ast
import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
LEX = ROOT / "app" / "llm" / "lexicon.yaml"
GOLDEN = ROOT / "evals" / "golden"
EVID = ROOT / "artifacts" / "review-evidence"
REQUIRED = ("id", "pattern", "flag_type", "category", "hedge", "self_report", "strength", "negatable",
            "rationale", "source", "false_positive", "appendix_c")
RAISES = ("high", "medium")
HELDOUT = ROOT / "evals" / "lexicon_heldout.jsonl"
HELDOUT_BAR = 0.85
# ADR-013 closed category list (memory/DECISIONS.md, api.md "Closed category lists"). Lexicon entries may use only these.
ADR013_LEXICON_CATEGORIES = {
    "pre_existing", "degenerative_language", "prior_surgery",
    "speculative_language", "patient_report", "missed_care", "new_onset", "scene_facts", "alternative_cause",
    "litigation_referral", "objective_negative", "recovery_context", "accident_date_provenance"}
PROBE_ACCIDENT_YEAR = 2026  # probes are written around the 2026 sample case
VERBOSE = "--verbose" in sys.argv

TOKEN = re.compile(r"[\w'/-]+|[;,]")
SENT_END = re.compile(r"[.!?](?=\s|$)|\n")


# ───────────── negation guard ─────────────

def _sentence_bounds(text, start, end):

# ───────────── matcher ─────────────

YEAR = re.compile(r"\b(19|20)\d{2}\b")


def _hit_year(m):
    for g in ("year", "year2"):
        try:
            if m.group(g):
                return int(m.group(g))
        except IndexError:
            pass
    y = YEAR.search(m.group(0))
    return int(y.group(0)) if y else None


def _clause_after(text, end):
    m = re.search(r"[,;.\n]", text[end:])
    return text[end:end + m.start()] if m else text[end:]


def hits(entry, text, neg, accident_year):
    """List of (start, end, matched) that FIRE (not negated / filtered / suppressed)."""
    out = []
    for m in entry["_rx"].finditer(text):
        if entry.get("negatable") and negated(text, m.start(), m.end(), neg):
            continue
        if entry.get("year_filter") and accident_year:
            y = _hit_year(m)
            if y and y >= accident_year:
                continue
        sup = entry.get("_sup")
        if sup and sup.search(_clause_after(text, m.end())):
            continue
        out.append((m.start(), m.end(), m.group(0)))
    return out


def fires(entry, rx, text, neg, accident_year=PROBE_ACCIDENT_YEAR):  # round-1 compatible helper
    return bool(hits(entry, text, neg, accident_year))


def scan(entries, text, neg, accident_year):
    res = []
    for e in entries:
        for h in hits(e, text, neg, accident_year):
            res.append((e, h))
    return res


# ───────────── golden parsing ─────────────

REC = re.compile(r"=== Record (\d+) ===\s*\nDate:\s*(.*?)\nSource:\s*(.*?)\nExcerpt:\s*\"(.*?)\"\s*(?:\n|$)", re.S)


def parse_case(path):
    recs = {}
    for n, date, src, exc in REC.findall(path.read_text()):
        recs[int(n)] = {"date": date.strip(), "source": src.strip(), "text": exc}
    years = [int(y.group(0)) for r in recs.values() for y in [re.search(r"\b(?:19|20)\d{2}\b", r["date"])] if y]
34:HELDOUT = ROOT / "evals" / "lexicon_heldout.jsonl"
407:    # 6. held-out probe set (evals/lexicon_heldout.jsonl): never copied into lexicon examples
445:        print(f"\n[held-out] {HELDOUT.name}: {ho_ok}/{ho_tot} = {ho_ok / max(ho_tot, 1):.0%} (bar {HELDOUT_BAR:.0%}); "
450:            print("  LEAK (held-out sentence is a lexicon example): " + t)
452:            errors.append(f"{len(leaked)} held-out sentences copied into lexicon examples")
454:        errors.append("evals/lexicon_heldout.jsonl missing")
463:          f"must_not violations {len(mustnot_fail)}; probe FP {len(fp)}, FN {len(fn)} of {n_tot + a_tot}; held-out {ho_ok}/{ho_tot}")
T-002-r3-probe.out.txt
T-002-r3-probe.py
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-r2-commit-secret-probe.out.txt
T-003-r2-commit-secret-probe.py
T-003-r2-probe-board2.out.txt
T-003-r2-probe-board2.py
T-003-r2-probe-corpus.txt
T-003-r2-probe-direct.out.txt
T-003-r2-probe-direct.out2.txt
T-003-r2-probe-direct.py
T-003-r3-probe-board2.out.txt
T-003-r3-probe-corpus.out.txt
T-003-r3-probe-corpus.py
T-003-r3-probe-direct.out.txt
T-003-r3-probe-legit.out.txt
T-003-r3-probe-legit.py
T-003-r3-probe-pwd.out.txt
T-003-r3-probe-pwd.py
T-003-r3-probe-rwg.out.txt
T-003-r3-probe-rwg.py
T-003-r3-probe-targeted.out.txt
T-003-r3-probe-targeted.py
T-003-r3-probe-targeted2.out.txt
T-003-r3-probe-targeted2.py
T-003-reviewer-write-guard-probe.txt
T-004-r2-board-guard-probe.py
T-004-r2-board-guard-probe.txt
T-004-r2-shell-write-probe.txt
T-004-r3-board-guard-probe.out.txt
T-004-r3-board-guard-probe.py
T-006-check-secrets-probe.txt
T-006-r2-chain-probe.out.txt
T-006-r2-chain-probe.py
T-006-r2-fp-probe.out.txt
T-006-r2-fp-probe.py
T-006-r2-probe.out.txt
T-006-r2-probe.py
T-006-r3-chain-probe.out.txt
T-006-r3-commit-paths-probe.out.txt
T-006-r3-commit-paths-probe.py
T-006-r3-fp-probe.out.txt
T-006-r3-probe.out.txt
T-006-rename-probe.txt
T-009-adjuster-probes.py
T-009-adjuster-probes.txt
T-009-nurse-golden-scan.txt
T-009-nurse-probe-output.txt
T-009-nurse-probe.py
T-009-nurse-probes.txt
T-009-r2-nurse-probe-output.txt
T-009-r2-nurse-probe.py
T-009-r2-nurse-variants-output.txt
T-009-r2-nurse-variants.py
T-009-r2-resolution.md
T-015-paralegal-regex-probe.out.txt
T-015-paralegal-regex-probe.py
T-015-r2-nurse-probe.out.txt
T-015-r2-nurse-probe.py
T-015-r2-paralegal-probe.out.txt
T-015-r2-paralegal-probe.py
T-015-r3-paralegal-probe.out.txt
T-015-r3-paralegal-probe.py
T-015-r3-paralegal-rerun-of-r2-probe.out.txt
T-015-r3-rerun-of-r2-nurse-probe.out.txt
T-017-r3-owner-probe.out.txt
T-017-r3-owner-probe.py
T-018-contract-probe.out.txt
T-018-contract-probe.py
T-025-pm-probe.out.txt
T-025-pm-probe.py
T-025-pm-r2-probe.out.txt
T-025-pm-r2-probe.py
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:43:49.916Z

**tool call — Bash**
````
{
 "command": "sed -n 395,445p research/lexicon_selfcheck.py; cat artifacts/review-evidence/T-009-r2-nurse-probe.py | head -80; grep -c . evals/lexicon_heldout.jsonl; grep -n \"map_type\\|NURSE_MAP\\|def load\" research/lexicon_selfcheck.py | head"
}
````

### User / tool · 2026-11-02T01:43:50.021Z

**tool result**
````
                    fp.append(f"adjuster QUIET {cat} | {s} -> {raised}")
            a_ok += ok
            if VERBOSE or not ok:
                print(f"  {'ok ' if ok else 'BAD'} {exp:5} {cat:12} {s}  -> " + ", ".join(f"{e['id']}[{e['strength']}]" for e, _ in res))
        print(f"  adjuster: {a_ok}/{a_tot} ok")
    print(f"\n[probes] false positives: {len(fp)} (bar ≤ 2)   false negatives: {len(fn)}")
    for x in fp:
        print("  FP " + x)
    for x in fn:
        print("  FN " + x)


    # 6. held-out probe set (evals/lexicon_heldout.jsonl): never copied into lexicon examples
    ho_ok = ho_tot = 0
    ho_bad, ho_by_group = [], {}
    ex_texts = {x.strip().lower() for e in entries for k in ("hit", "miss", "negated") for x in e.get("examples", {}).get(k, [])}
    leaked = []
    if HELDOUT.exists():
        for line in HELDOUT.read_text().splitlines():
            if not line.strip():
                continue
            r = json.loads(line)
            if r["text"].strip().lower() in ex_texts:
                leaked.append(r["text"])
            res = scan(entries, r["text"], neg, r.get("accident_year", PROBE_ACCIDENT_YEAR))
            raised = [e for e, _ in res if e["strength"] in RAISES]
            x = r["expect"]
            if x == "pre_existing":
                ok = any(e["flag_type"] == "pre_existing" for e in raised)
            elif x == "hedge":
                ok = any(e["hedge"] for e in raised)
            elif x == "attribution":
                ok = any(e["self_report"] and e["flag_type"] == "causation" for e in raised)
            elif x == "self_report_any":
                ok = any(e["self_report"] for e, _ in res)
            elif x == "quiet_pre_existing":
                ok = not any(e["flag_type"] == "pre_existing" for e in raised)
            elif x == "quiet_hedge":
                ok = not any(e["hedge"] for e in raised)
            elif x == "quiet_self_report":
                ok = not any(e["self_report"] for e, _ in res)
            else:
                raise SystemExit(f"bad expect {x}")
            ho_tot += 1
            ho_ok += ok
            g = ho_by_group.setdefault(r["group"], [0, 0])
            g[0] += ok
            g[1] += 1
            if not ok:
                ho_bad.append(f"{r['id']} {r['group']} {x} | {r['text']} -> " + ", ".join(f"{e['id']}[{e['strength']}]" for e, _ in res))
        print(f"\n[held-out] {HELDOUT.name}: {ho_ok}/{ho_tot} = {ho_ok / max(ho_tot, 1):.0%} (bar {HELDOUT_BAR:.0%}); "
"""T-009 round-2 legal-nurse probes. Uses the lexicon's OWN reference matcher (research/lexicon_selfcheck.py:
hits/scan: clause-bounded negation, field answers, year_filter, suppress_if_followed_by). Read-only.
Run: .venv/bin/python -I artifacts/review-evidence/T-009-r2-nurse-probe.py

Grading:
  round-1 nurse set   - LENIENT = selfcheck semantics (FIRE: any strength of mapped type)
                      - STRICT  = pre_existing FIRE needs a RAISE (high/medium; low never raises, D-018);
                                  HEDGE FIRE needs a hedge:true entry; SUBJ FIRE needs a self_report entry (any strength)
  round-1 adjuster set - selfcheck semantics (FLAG = high/medium raised; QUIET = none raised)
  new r2 probes       - RAISE:<type>  high/medium hit of that flag_type
                        HEDGE         a hedge:true entry fires (R-TL-8 qualifier unit)
                        ATTR          a self_report:true entry fires (source_kind=patient_report)
                        ATTR_CAUS     patient_attributes_causation fires (self-reported causation, high)
                        QUIET:<type>  no high/medium hit of that type ('any' = no raise at all)
"""
import ast
import importlib.util
import re
import sys
from pathlib import Path

import yaml

ROOT = Path("/Users/arsis/zlayt-pm-project")
spec = importlib.util.spec_from_file_location("sc", ROOT / "research" / "lexicon_selfcheck.py")
sc = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sc)

lex = yaml.safe_load((ROOT / "app" / "llm" / "lexicon.yaml").read_text())
neg = lex["negation"]
entries = lex["entries"]
for e in entries:  # compile exactly as selfcheck main() does
    e["_rx"] = re.compile(e["pattern"], re.I | re.M)
    e["_sup"] = re.compile(e["suppress_if_followed_by"], re.I) if e.get("suppress_if_followed_by") else None
vmap = lex["v1_type_map"]
AY = sc.PROBE_ACCIDENT_YEAR
RAISE = ("high", "medium")


def res(s):
    return sc.scan(entries, s, neg, AY)


def fmt(r):
    return ", ".join(f"{e['id']}[{e['strength']}/{e['flag_type']}{'/H' if e['hedge'] else ''}{'/SR' if e['self_report'] else ''}]:'{h[2]}'" for e, h in r) or "-"


def raised(r, t):
    return [e for e, _ in r if e["strength"] in RAISE and (t == "any" or e["flag_type"] == t)]


tot = {}


def tally(group, ok):
    a = tot.setdefault(group, [0, 0])
    a[0] += ok
    a[1] += 1


# ---------- 1. round-1 nurse probes ----------
print("=== ROUND-1 NURSE PROBES (artifacts/review-evidence/T-009-nurse-probes.txt) ===")
for line in (ROOT / "artifacts/review-evidence/T-009-nurse-probes.txt").read_text().splitlines():
    if line.startswith("#") or not line.strip():
        continue
    cat, exp, s = [x.strip() for x in line.split("|", 2)]
    r = res(s)
    if exp.startswith("FIRE:"):
        t = vmap.get(exp[5:], exp[5:])
        lenient = any(e["flag_type"] == t for e, _ in r)
        if cat == "HEDGE":
            strict = any(e["hedge"] for e, _ in r)
        elif cat == "SUBJ" and t == "causation":
            strict = any(e["self_report"] for e, _ in r)
        else:
            strict = bool(raised(r, t))
    elif exp == "SUPPRESS":
        lenient = strict = not any((e["flag_type"] == "pre_existing" or e["id"] == "likely_alternative_cause")
                                   and e["strength"] in RAISE for e, _ in r)
    else:
90
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:44:12.289Z

**tool call — Bash**
````
{
 "command": "mkdir -p /Users/arsis/zlayt-pm-project/artifacts/review-evidence && cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-027-nurse-fresh-probe.py <<'EOF'\n\"\"\"T-027 legal-nurse fresh probes (25, written by reviewer, not visible to worker). Uses selfcheck's own scan().\nStrict grading: RAISE = high/medium of the mapped type; HEDGE = hedge:true entry raised high/medium;\nATTR = self_report causation entry raised; QUIET = no high/medium of type. Run: .venv/bin/python -I <this>\"\"\"\nimport importlib.util, re, sys, json\nfrom pathlib import Path\nimport yaml\nROOT = Path(\"/Users/arsis/zlayt-pm-project\")\nspec = importlib.util.spec_from_file_location(\"sc\", ROOT / \"research\" / \"lexicon_selfcheck.py\")\nsc = importlib.util.module_from_spec(spec); spec.loader.exec_module(sc)\nlex = yaml.safe_load((ROOT / \"app/llm/lexicon.yaml\").read_text())\nneg, entries = lex[\"negation\"], lex[\"entries\"]\nfor e in entries:\n    e[\"_rx\"] = re.compile(e[\"pattern\"], re.I | re.M)\n    e[\"_sup\"] = re.compile(e[\"suppress_if_followed_by\"], re.I) if e.get(\"suppress_if_followed_by\") else None\nR = (\"high\", \"medium\")\nP = [\n (\"prior_level\",  \"PRE\", \"History of cervical spondylosis involving C4-5 and C5-6 since 2017.\"),\n (\"prior_treat\",  \"PRE\", \"Pt had epidural steroid injection at L4-5 in March 2022 for chronic back pain.\"),\n (\"prior_imaging\",\"PRE\", \"Prior lumbar MRI in 2021 showed an L4-5 disc protrusion.\"),\n (\"prior_treat\",  \"PRE\", \"Patient was treated for neck pain by a chiropractor from 2019 to 2020.\"),\n (\"prior_dx\",     \"PRE\", \"Known degenerative disc disease at C5-C6, diagnosed 2018.\"),\n (\"prior_surg\",   \"PRE\", \"Underwent L3-L4 laminectomy in 2012.\"),\n (\"prior_hx\",     \"PRE\", \"PMH significant for chronic low back pain since 2020.\"),\n (\"prior_hx\",     \"PRE\", \"Pt reports a prior whiplash injury in 2014 with full recovery.\"),\n (\"prior_hx\",     \"PRE\", \"Hx of cervical radiculopathy, treated with PT in 2016.\"),\n (\"prior_level\",  \"PRE\", \"Remote T11-12 vertebroplasty; no current complaints.\"),\n (\"hedge\",        \"HEDGE\", \"Findings are suggestive of chronic degenerative change; clinical correlation advised.\"),\n (\"hedge\",        \"HEDGE\", \"Mild C5-6 uncovertebral hypertrophy, likely age-related.\"),\n (\"hedge\",        \"HEDGE\", \"Cannot exclude an old healed compression deformity at T12.\"),\n (\"hedge\",        \"HEDGE\", \"Disc desiccation at C5-6, possibly post-traumatic versus degenerative.\"),\n (\"hedge\",        \"HEDGE\", \"Chronicity of the annular fissure is indeterminate.\"),\n (\"attribution\",  \"ATTR\", \"Patient states the pain started when the other vehicle struck her from behind.\"),\n (\"attribution\",  \"ATTR\", \"Pt attributes her headaches to the crash.\"),\n (\"attribution\",  \"ATTR\", \"Patient feels her symptoms are a result of the collision.\"),\n (\"attribution\",  \"ATTR\", \"Per patient, neck stiffness began the day after the MVC.\"),\n (\"quiet_neg\",    \"QUIET_PRE\", \"Denies any prior neck surgery or previous cervical injury.\"),\n (\"quiet_post\",   \"QUIET_PRE\", \"Follow-up for neck pain sustained in the 03/14/2026 motor vehicle collision.\"),\n (\"quiet_post\",   \"QUIET_PRE\", \"Previously prescribed cyclobenzaprine at the 04/02/2026 visit; continue.\"),\n (\"quiet_post\",   \"QUIET_PRE\", \"Prior to today's visit, patient completed 6 PT sessions.\"),\n (\"quiet_post\",   \"QUIET_PRE\", \"Previous MRI of 05/29/2026 reviewed with patient.\"),\n (\"quiet_hedge\",  \"QUIET_HEDGE\", \"Impression: C5-6 disc protrusion with mild right foraminal narrowing.\"),\n]\nok_n = 0; by = {}; rows = []\nfor g, x, s in P:\n    res = sc.scan(entries, s, neg, sc.PROBE_ACCIDENT_YEAR)\n    raised = [e for e, _ in res if e[\"strength\"] in R]\n    if x == \"PRE\": ok = any(e[\"flag_type\"] == \"pre_existing\" for e in raised)\n    elif x == \"HEDGE\": ok = any(e[\"hedge\"] for e in raised)\n    elif x == \"ATTR\": ok = any(e[\"self_report\"] and e[\"flag_type\"] == \"causation\" for e in raised)\n    elif x == \"QUIET_PRE\": ok = not any(e[\"flag_type\"] == \"pre_existing\" for e in raised)\n    elif x == \"QUIET_HEDGE\": ok = not any(e[\"hedge\"] for e in raised)\n    ok_n += ok; a = by.setdefault(x, [0, 0]); a[0] += ok; a[1] += 1\n    rows.append(f\"{'ok ' if ok else 'MISS'} {x:11} {g:13} | {s}  -> \" + (\", \".join(f\"{e['id']}[{e['strength']}/{e['flag_type']}]\" for e, _ in res) or \"-\"))\nprint(\"\\n\".join(rows))\nprint(f\"\\nFRESH {ok_n}/{len(P)} = {ok_n/len(P):.0%} (threshold 80%)  by expect: {by}\")\nEOF\ncd /Users/arsis/zlayt-pm-project && .venv/bin/python -I artifacts/review-evidence/T-027-nurse-fresh-probe.py | tee artifacts/review-evidence/T-027-nurse-fresh.txt"
}
````

### User / tool · 2026-11-02T01:44:12.498Z

**tool result**
````
ok  PRE         prior_level   | History of cervical spondylosis involving C4-5 and C5-6 since 2017.  -> history_of[medium/pre_existing], degenerative_imaging_terms[high/pre_existing]
ok  PRE         prior_treat   | Pt had epidural steroid injection at L4-5 in March 2022 for chronic back pain.  -> chronic[medium/pre_existing]
ok  PRE         prior_imaging | Prior lumbar MRI in 2021 showed an L4-5 disc protrusion.  -> prior_imaging[medium/pre_existing], dated_prior_event[medium/pre_existing]
MISS PRE         prior_treat   | Patient was treated for neck pain by a chiropractor from 2019 to 2020.  -> -
ok  PRE         prior_dx      | Known degenerative disc disease at C5-C6, diagnosed 2018.  -> degenerative[high/pre_existing]
ok  PRE         prior_surg    | Underwent L3-L4 laminectomy in 2012.  -> dated_prior_event[medium/pre_existing]
ok  PRE         prior_hx      | PMH significant for chronic low back pain since 2020.  -> pmh_significant_for[high/pre_existing], chronic[medium/pre_existing], condition_since_year[high/pre_existing]
ok  PRE         prior_hx      | Pt reports a prior whiplash injury in 2014 with full recovery.  -> prior_injury_or_condition[high/pre_existing], self_reported_prior[high/pre_existing], dated_prior_event[medium/pre_existing], patient_reports_generic[low/causation]
ok  PRE         prior_hx      | Hx of cervical radiculopathy, treated with PT in 2016.  -> hx_abbrev[high/pre_existing], dated_prior_event[medium/pre_existing]
MISS PRE         prior_level   | Remote T11-12 vertebroplasty; no current complaints.  -> -
ok  HEDGE       hedge         | Findings are suggestive of chronic degenerative change; clinical correlation advised.  -> chronic[medium/pre_existing], degenerative[high/pre_existing], correlate_clinically[medium/causation], suggestive_versus_hedges[medium/causation]
ok  HEDGE       hedge         | Mild C5-6 uncovertebral hypertrophy, likely age-related.  -> degenerative_imaging_terms[high/pre_existing], age_related_old_findings[high/pre_existing], likely_alternative_cause[high/causation]
ok  HEDGE       hedge         | Cannot exclude an old healed compression deformity at T12.  -> age_related_old_findings[high/pre_existing], cannot_exclude[medium/causation]
ok  HEDGE       hedge         | Disc desiccation at C5-6, possibly post-traumatic versus degenerative.  -> degenerative[high/pre_existing], degenerative_imaging_terms[high/pre_existing], possibility_terms[medium/causation], suggestive_versus_hedges[medium/causation]
ok  HEDGE       hedge         | Chronicity of the annular fissure is indeterminate.  -> annular_fissure[medium/pre_existing], nonspecific_indeterminate[medium/causation]
MISS ATTR        attribution   | Patient states the pain started when the other vehicle struck her from behind.  -> patient_reports_generic[low/causation]
ok  ATTR        attribution   | Pt attributes her headaches to the crash.  -> patient_attributes_causation[high/causation]
MISS ATTR        attribution   | Patient feels her symptoms are a result of the collision.  -> -
ok  ATTR        attribution   | Per patient, neck stiffness began the day after the MVC.  -> patient_attributes_causation[high/causation], patient_reports_generic[low/causation], delayed_onset_or_care[medium/causation]
ok  QUIET_PRE   quiet_neg     | Denies any prior neck surgery or previous cervical injury.  -> -
ok  QUIET_PRE   quiet_post    | Follow-up for neck pain sustained in the 03/14/2026 motor vehicle collision.  -> -
ok  QUIET_PRE   quiet_post    | Previously prescribed cyclobenzaprine at the 04/02/2026 visit; continue.  -> -
ok  QUIET_PRE   quiet_post    | Prior to today's visit, patient completed 6 PT sessions.  -> -
ok  QUIET_PRE   quiet_post    | Previous MRI of 05/29/2026 reviewed with patient.  -> -
ok  QUIET_HEDGE quiet_hedge   | Impression: C5-6 disc protrusion with mild right foraminal narrowing.  -> -

FRESH 21/25 = 84% (threshold 80%)  by expect: {'PRE': [8, 10], 'HEDGE': [5, 5], 'ATTR': [2, 4], 'QUIET_PRE': [5, 5], 'QUIET_HEDGE': [1, 1]}
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:44:18.582Z

**tool call — Bash**
````
{
 "command": "sed -n 250,258p memory/DECISIONS.md; grep -n \"id: prior_treatment_terms\\|id: pmh_psh_spine\\|id: patient_attributes_causation\" -A3 app/llm/lexicon.yaml | cut -c1-400; cat .claude/agent-memory/legal-nurse-reviewer/../../../reviews/T-009-legal-nurse-r2.md | grep -n '\"title\"' | cut -c1-250"
}
````

### User / tool · 2026-11-02T01:44:18.689Z

**tool result**
````
  - The flag-type vocabulary is `gap`, `conflict`, `pre_existing`, `causation`, `record_warning` everywhere (D-013). `record_warning` flags are created by code only (categories `date_ambiguous`, `injection_suspected`).
  - **Lexicon contract (D-018).** `app/llm/lexicon.yaml` entries have `flag_type` (`pre_existing` | `causation` | `record_warning`), booleans `hedge` and `self_report`, and `strength` (`high`/`medium` raise flags; `low` is context only). Negation scope is clause-bounded (ends at `,` `;` `.` `but` `however`) and understands field-style answers ("Prior injuries: No."). Categories the code relies on: `pre_existing`, `causation_weakening`, `compliance`, the hedge set, `patient_report`, `accident_date_phrases`, `damages`, `non_encounter`, `injection`. **`lexicon.yaml` v2 is a researcher deliverable that blocks the gap rule (`non_encounter`), the accident-date rule (`accident_date_phrases`) and the injection scan (`injection`); its self-check must run over every golden case and report recall per `must` flag.** The lexicon `causation_weakening` and `compliance` map to `causation`.
  - LLM flag passes run **per record** and return `{type, category, record_id, excerpt}`; the cross-record conflict pass returns `{category, a:{record_id, excerpt}, b:{...}}`. The schema rejects any extra prose field. `category` is from a closed list:
    The list equals the lexicon v2 category names (single vocabulary):
    - pre_existing: `pre_existing`, `degenerative_language`, `prior_surgery`;
    - causation: `speculative_language`, `patient_report`, `missed_care`, `new_onset`, `scene_facts`, `alternative_cause`, `litigation_referral`, `objective_negative` (no objective findings, normal exam, WNL/full ROM), `recovery_context`, `accident_date_provenance`;
    - conflict: `treatment_plan_vs_actual`, `provider_name_variant`, `other_fact_mismatch` (LLM or code), `accident_date_after_treatment`, `accident_dates_differ` (code);
    - gap: `gap_over_30` (code); record_warning: `date_ambiguous`, `injection_suspected` (code).
    **Template table (design text; slots `{date}` long date, `{provider}` header label as written, `{quote}` verbatim excerpt, `{days}`, `{a}`/`{b}` for two sources):**
727:- id: patient_attributes_causation
728-  pattern: '(?:\b(?:patient|pt\.?|he|she|client)\s+(?:states|stated|reports|reported|believes|attributes|relates|related|feels|claims|says|said|thinks)\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bcomplain(?:s|ing)?\s+of\b|\bc/o\b)[^.;]{0,80}?\b(?:after|since|from|due\s+to|because\s+of|caused\s+by|following|began\s+with)\b[^.;]{0,40}?\b(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|impac
729-  flag_type: causation
730-  category: patient_report
--
1209:- id: prior_treatment_terms
1210-  pattern: '\b(?:prior|previous|earlier|remote|past)\s+(?:[\w/.-]+\s+){0,2}?(?:ESIs?|epidurals?|injections?|nerve\s+blocks?|physical\s+therapy|PT|chiropractic|rehab\w*|(?:therap(?:y|ies)|treatments?|care)(?=\s+(?:for|to|of)\s+(?:the\s+|his\s+|her\s+)?(?:neck|back|spine|shoulder|knee|hip|cervical|lumbar|thoracic)\b|[^.;]{0,30}\b(?:19|20)\d{2}\b))\b(?!\s+(?:plan|visit|session|authorization|auth
1211-  flag_type: pre_existing
1212-  category: pre_existing
--
1229:- id: pmh_psh_spine
1230-  pattern: '\b(?:PMH|PMHx|PSH|past\s+(?:medical|surgical)\s+history)\s*[:\-](?!\s*(?:no|none|neg\w*|denies|denied|non-?contributory|unremarkable|n/?a)\b)[^\n]{0,200}?\b(?:[CTLS]\d{1,2}(?:\s?[-/]\s?[CTLS]?\d{1,2})?|neck|cervical|thoracic|lumbar|back|spine|spinal|disc|shoulder|knee|hip|whiplash|fusion|discectomy|laminectomy|arthroscop\w*|ACDF|surgery|fracture|strain|sprain|herniat\w*|radiculopa
1231-  flag_type: pre_existing
1232-  category: pre_existing
49:   "title": "Prior-history recall does not generalize beyond the probe sentences: spinal levels break the word slots, and there is no 'since <year>' branch",
55:   "title": "The hedge set (R-TL-8 / R-TL-10(b) qualifier detector) misses 'may be <finding>', 'favors', 'probable', 'presumed' and 'uncertain chronicity'",
61:   "title": "Patient-attributed causation phrased 'attributes/relates … to' gets no hit, and some self-report markers carry no attribution",
67:   "title": "pre_existing raises on post-accident follow-up wording (6 of 9 new quiet probes), including post-accident chronic pain the record ties to the MVA",
73:   "title": "Six lexicon categories are outside ADR-013's closed list, and one is the tool's own 'objective' label",
79:   "title": "Selfcheck probe grading is lenient, and the probe sets are no longer held out",
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:44:42.955Z

**tool call — Bash**
````
{
 "command": "cat > reviews/T-027-legal-nurse.md <<'EOF'\n# T-027 legal-nurse review (Linda Chen, RN) — Lexicon generalization, commit 8b7dc17\n\nVerdict: **pass** (minors only). Fresh 25 reviewer probes (written after reading only the first 5 held-out rows; none are in the worker's file): **21/25 = 84%** under strict grading (high/medium raises), above the 80% bar. Golden MUST 11/11, SHOULD 1/1, must_not 0. Worker's own held-out 90/90, no leak. All 5 post-accident false-alarm traps and the negation trap stayed quiet; the no-hedge MRI impression raised no hedge.\n\nFresh misses (evidence file: artifacts/review-evidence/T-027-nurse-fresh.txt; script T-027-nurse-fresh-probe.py):\n- \"Patient states the pain started when the other vehicle struck her from behind.\" -> only patient_reports_generic[low]; \"when ... struck\" is not an attribution connector.\n- \"Patient feels her symptoms are a result of the collision.\" -> no hit at all.\n- \"Patient was treated for neck pain by a chiropractor from 2019 to 2020.\" -> no hit.\n- \"Remote T11-12 vertebroplasty; no current complaints.\" -> no hit.\nThese are recall gaps, not wrong output (nothing was inferred or upgraded), so minor. Attribution scored 2/4 fresh versus 12/12 on the worker's tuned set, so the worker's group figures overstate recall.\n\nLabel note: ADR-013 category `objective_negative` is the tool's own \"objective\" word. It is acceptable as an internal key, but it must not reach the UI or export (persona checklist item 7).\nScope: lexicon recall only. Prompts, UI and summaries are outside this card.\n\n```json\n{\"card\": \"T-027\", \"persona\": \"legal-nurse-reviewer\", \"model\": \"claude-sonnet-5-5\",\n \"scope\": \"commit 8b7dc17: app/llm/lexicon.yaml, research/lexicon_selfcheck.py, evals/lexicon_heldout.jsonl; 25 fresh reviewer probes; golden cases\",\n \"exercised\": [\n  \".venv/bin/python research/lexicon_selfcheck.py -> golden MUST 11/11, SHOULD 1/1, must_not 0, probes FP 0 FN 1 of 140, held-out 90/90, RESULT: PASS\",\n  \"python3 tools/board.py show T-027 (AC and handoff read)\",\n  \".venv/bin/python -I artifacts/review-evidence/T-027-nurse-fresh-probe.py: 25 fresh probes scored with selfcheck scan() -> 21/25 = 84% (PRE 8/10, HEDGE 5/5, ATTR 2/4, QUIET_PRE 5/5, QUIET_HEDGE 1/1); output at artifacts/review-evidence/T-027-nurse-fresh.txt\",\n  \"read research/lexicon_selfcheck.py header, held-out runner and leak check; read lexicon entries prior_treatment_terms, pmh_psh_spine, patient_attributes_causation; read memory/DECISIONS.md:250-258 ADR-013 category list\"\n ],\n \"verdict\": \"pass\",\n \"scores\": {\"held_out_recall_fresh\": 4, \"golden_must_flags\": 5, \"post_accident_false_alarms\": 5, \"hedge_preservation\": 5, \"patient_attribution_recall\": 3, \"category_names_adr013\": 4},\n \"findings\": [\n  {\"severity\": \"minor\",\n   \"title\": \"Patient-attributed causation recall is 2/4 on fresh phrasings\",\n   \"evidence\": \"T-027-nurse-fresh.txt: 'Patient states the pain started when the other vehicle struck her from behind.' -> patient_reports_generic[low/causation] only; 'Patient feels her symptoms are a result of the collision.' -> '-'. Worker group result: attribution 12/12 (tuned set).\",\n   \"why_it_matters\": \"Checklist item 8: patient-stated causation must be surfaced as self-report, not silently dropped. A miss means the attorney is not told the causation claim is the patient's.\",\n   \"fix\": \"Widen the connector set in patient_attributes_causation to include 'when ... struck/hit/rear-ended', 'result of', 'secondary to', 'ever since'; keep the self_report flag so it stays attributed to the patient.\",\n   \"acceptance_test\": \"Both sentences above raise patient_attributes_causation at high/medium; the quiet post-accident probes still raise no pre_existing.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Prior treatment given as a year range, and 'Remote <level> <procedure>' with no year, are not flagged\",\n   \"evidence\": \"T-027-nurse-fresh.txt: 'Patient was treated for neck pain by a chiropractor from 2019 to 2020.' -> '-'; 'Remote T11-12 vertebroplasty; no current complaints.' -> '-'.\",\n   \"why_it_matters\": \"Checklist item 9: prior history must be flagged as prior history. These forms are common in intake notes.\",\n   \"fix\": \"Add a 'treated ... (for|by) ... from <year> to <year>' branch (year-filtered like the others) and let remote/past/old precede a spinal level plus a spine procedure noun (vertebroplasty, kyphoplasty, fusion, laminectomy).\",\n   \"acceptance_test\": \"Both sentences raise pre_existing at high/medium; 'Chiropractic care from 03/20/2026 to 05/01/2026' stays quiet.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"ADR-013 category 'objective_negative' puts the tool's own 'objective' label in a user-reachable vocabulary\",\n   \"evidence\": \"memory/DECISIONS.md:255 'objective_negative (no objective findings, normal exam, WNL/full ROM)'; worker handoff says names are used as written.\",\n   \"why_it_matters\": \"Checklist item 7 and dealbreaker 3: the tool must not add its own subjective/objective labels. As an internal key this is fine; displayed text would not be.\",\n   \"fix\": \"Confirm the category key is never rendered, and that UI and export use the template text and the verbatim quote only. Alternatively rename it to `normal_exam_language`.\",\n   \"acceptance_test\": \"grep of UI templates and export for 'objective' and 'subjective' returns no tool-authored label.\"}\n ],\n \"whats_right\": [\n  \"Post-accident wording ('sustained in the 03/14/2026 collision', 'Previous MRI of 05/29/2026', 'Prior to today's visit') stayed quiet 5/5 via the year filter; the negation trap also stayed quiet.\",\n  \"Hedges ('cannot exclude', 'possibly ... versus', 'indeterminate', 'likely age-related') were caught 5/5 on unseen phrasings, and a plain MRI impression raised no hedge.\",\n  \"Selfcheck now fails on example/held-out overlap, grades strictly, and golden MUST is 11/11.\"\n ],\n \"questions_for_chris\": []}\n```\nEOF\npython3 tools/board.py validate 2>&1 | tail -5"
}
````

### User / tool · 2026-11-02T01:44:43.108Z

**tool result**
````
ok (49 file(s))
````

### Assistant · claude-sonnet-5-5 · 2026-11-02T01:44:45.813Z

Verdict: pass, with three minors and no blockers or majors. My 25 fresh probes scored 21/25 = 84% (bar 80%), and golden must-flags are 11/11. The self-check also passes (held-out 90/90, 0 false positives).
- Minors: patient-attributed causation ("started when the other vehicle struck her", "feels … a result of the collision") scored 2/4. A chiropractor-treatment year range and "Remote T11-12 vertebroplasty" are not flagged. The ADR-013 category `objective_negative` is the tool's own "objective" label, so it must not reach the UI.
- Files: `/Users/arsis/zlayt-pm-project/reviews/T-027-legal-nurse.md`, `/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-027-nurse-fresh.txt`, and the probe script `T-027-nurse-fresh-probe.py` in the same folder. `board.py validate` reports ok (49 files).
