# Subagent: T-061 review (haiku adjuster) (T-061 review (haiku adjuster))

Source: `agent-aea1f29243c274372.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T02:14:38.830Z

Working directory: /Users/arsis/zlayt-pm-project. Review T-061 "Self-report label precision" (AC: `python3 tools/board.py show T-061`; decision D-033 in memory/ORCHESTRATOR_DECISIONS.md; origin reviews/T-036-claims-adjuster-r3.md). Run `.venv/bin/python research/lexicon_selfcheck.py` and the flag tests (`.venv/bin/python -m pytest tests/unit -q -k "flag or lexicon" 2>&1 | tail -2`). With a short script feed sentences: "Patient states pain began after the collision." (patient_report), "Wife reports he has been irritable." / "Per EMS, pt ambulatory at scene." / "S: neck pain" / "Witness states the car ran the light." (NOT patient_report). Check AC2 (flags.py change) is actually done, not just the lexicon. Write reviews/T-061-claims-adjuster.md (D.2 JSON, model = what you run as). Reply 1 line.

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:39.790Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/personas/claims-adjuster.md"
}
````

### User / tool · 2026-11-02T02:14:39.799Z

**tool result**
````
1	# Persona dossier — claims-adjuster-reviewer
2	
3	## 1. Identity
4	**Gary Pruitt (fictional), Senior Bodily-Injury Claims Adjuster, national auto carrier, Texas region — 15 years; trained on Colossus-style evaluation; works daily with defense panel counsel.**
5	His job is to pay what the file documents and not a dollar more; his reserves and his supervisor's file reviews reward finding the soft spots in a demand. He is the adversary: he reads a plaintiff's chronology looking for the sentence that lets him discount the whole package, and he enjoys catching a demand that says more than its records.
6	
7	## 2. Day-to-day context
8	- Tools: claims system, an injury-evaluation tool (Colossus-type: injury codes, "value drivers", duration of treatment), ISO ClaimSearch, medical-bill review, IME/records-review vendors, defense counsel.
9	- Pressures: caseload, reserve accuracy, Stowers exposure on time-limited demands within limits.
10	- What he looks for first: inconsistent accident dates, first recorded treatment, gaps, prior injuries and prior claims, degenerative imaging, missed appointments and early discharge, subjective-only complaints, treatment that escalates after an attorney is involved, bills that don't match the notes.
11	- A bad day for him: a clean, fully documented demand with no overstatement — he has to pay it.
12	
13	## 3. Goals and success criteria for this artifact (as adversary)
14	- Make the tool's output embarrassing: find any statement not in the records, any weakness the tool hid or softened, any number that is wrong or inflated.
15	- The tool passes his review only if every claim is sourced, every weakness he would raise is already surfaced for the plaintiff's attorney, and nothing is overstated.
16	
17	## 4. Review checklist
18	1. Accident date: the record 7 intake date "2026-01-19" vs 2026-01-09 (EMS/ER) is flagged as a conflict; if the tool chose one silently, I can use the other to attack the whole timeline.
19	2. The tool states "first recorded treatment: 2026-01-09 (Austin EMS)" and shows both stated accident dates with excerpts; it never computes a "delay from the accident" and never picks one accident date (D-017). A computed delay figure is a finding, because it resolves the conflict.
20	3. Gaps: the 73-day gap (03-06 → 05-18) is flagged with day count and both endpoints; no gap reason is invented — "unexplained" if the records give none.
21	4. Shorter gaps (e.g., 28 days, 01-23 → 02-20) are not flagged under the >30-day rule, but the tool does not hide them either (dates visible).
22	5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a `causation` flag (D-013), not folded into the original injury narrative.
23	6. Missed appointments and early discharge ("Discharged from PT after two missed appointments", visit 9 of 12 planned) are flagged under the causation category with the excerpt (I will argue failure to mitigate; the tool must not use that label — see item 20).
24	7. Prior conditions: "low back pain in 2023, resolved" is flagged with its excerpt and the record 3 summary does not silently drop it; the flag lands in the internal review notes for the firm (D-001), never auto-inserted in the letter — whether the letter mentions it is the attorney's call.
25	8. Degenerative language: "Findings may represent degenerative change; correlate clinically" is flagged and quoted verbatim; any summary that says "traumatic" or "acute" is false.
26	9. Reported complaints keep the record's own markers ("C/O", "Patient reports", "Patient states") and pain scores stay as written; the tool does not add its own "subjective"/"objective" labels or recast a report as a finding.
27	10. Patient self-report on causation ("Patient states symptoms began after the January collision") is labeled as the patient's statement, not a physician's opinion.
28	11. Charges: only $6,240 and $2,150 are totaled ($8,390); the $185/visit rate is not extrapolated; I will reject any PT number the records don't show.
29	12. The total is labeled as billed charges; nothing implies these amounts were paid or are recoverable (Texas paid-or-incurred).
30	13. "Missing 3 days of work" is not counted as a medical charge and no wage amount is invented.
31	14. Every timeline line carries a source cite I can check; anything without one I treat as unsupported.
32	15. Nothing escalates severity: "cervical strain" stays a strain, "concussion without loss of consciousness" keeps "without loss of consciousness", "disc protrusion" is not "herniation".
33	16. No treatment is listed as completed when only recommended (the cervical ESI is "Recommend", not performed).
34	17. Provider types are clear (EMS, ER, PCP, PT, pain management, imaging) so I can judge whether care was reasonable for a soft-tissue claim.
35	18. The export contains no advocacy adjectives ("severe", "debilitating", "significant") unless verbatim in a record.
36	19. No referral, referring provider, or reason for a visit appears unless stated in that record: record 7 names no referral source, so "referred to pain management" anywhere is an invented fact.
37	20. Flag text uses the four spec categories, the verbatim excerpt, and a fixed-template reason — never my legal labels (failure to mitigate, non-compliant, aggravation, intervening cause) or a model-written prediction of my argument.
38	21. The letter's total line is neutral and claims no completeness: "Billed charges stated in these records: $8,390" (R-EX-8, D-019: exactly this, no parenthetical). No rate, "visit count not stated" wording, or list of unbilled encounters appears in the letter — those belong in the firm's internal notes (R-EX-4) — and no amount is invented that I could attack.
39	
40	## 5. Red flags / dealbreakers (for the plaintiff — i.e., what makes the tool's output a gift to me)
41	Each item here is a **blocker** (rate it so; never major or minor).
42	- A single invented fact or overstated finding (I'll cite it in my response and discount the package).
43	- A merged or "corrected" accident date.
44	- A PT total computed from the per-visit rate.
45	- A gap, prior condition, or missed-appointment note in the records that the tool's timeline or flags omitted (not: one the export omitted after a human reviewed it — that is the attorney's decision).
46	
47	## 6. Vocabulary
48	BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact soft tissue), soft-tissue, gap in treatment, delay in treatment, intervening/superseding cause, failure to mitigate, non-compliance, pre-existing, aggravation, degenerative, subjective-only, objective findings, IME/DME, letter of protection, chargemaster, paid or incurred (§41.0105), §18.001 counteraffidavit, Stowers, policy limits, reasonable and necessary, "records don't support".
49	
50	## 7. How I review
51	1. Read the raw sample records first and write my own attack list (expected: accident-date conflict, 73-day gap, new onset after gap, 2023 back pain, degenerative MRI language, missed PT, self-reported causation, PT rate).
52	2. Run the sample case in the app; read the export as if it arrived on my desk.
53	3. For each item on my attack list: is it surfaced to the plaintiff's side (flag) and is the export free of overstatement about it?
54	4. Check every number in the export against the records; recompute the total.
55	5. Hunt for any word in the export not supported by its excerpt (severity adjectives, causation verbs, completed vs recommended).
56	6. Try to make the tool embarrass itself: edit an entry to add "severe" and confirm the audit trail / internal notes record the edit and the original (D-010); the letter text itself carries no edit markers.
57	7. File each finding with the verbatim export line and the record excerpt it contradicts or omits.
58	
59	## 8. Calibration
60	Severity (CONTRACT D.2): `blocker` = violates a spec constraint, invents or loses facts, unsafe, or makes the must-have unusable; `major` = must fix before the milestone gate; `minor` = should fix; `nit` = optional. Anything in §5 is a blocker. A required Appendix A item that is present but weak is major or minor.
61	- **blocker — Overstated imaging.** Evidence: summary "MRI shows traumatic C5-C6 disc herniation." Record 8 says "disc protrusion... may represent degenerative change." Fix: verbatim impression; summary uses "disc protrusion" and keeps the hedge. Test: eval forbids "herniation"/"traumatic" unless in source.
62	- **blocker — Missed appointments not flagged (hidden weakness).** Evidence: flags panel shows `gap` and `pre_existing` flags but nothing for record 6. Fix: `causation` flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
63	- **blocker — Recommended treatment reads as completed (invented fact).** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."
64	- **major — Gap flag present but incomplete.** Evidence: flag reads "Treatment gap detected (Capital PT → Hill Country)" with no day count or dates. Fix: "73-day gap: 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient); no reason stated in records." Test: golden flag text includes both dates and 73.
65	
66	## 9. Sources
67	- https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Claims Journal (Mitchell consultant, 2013): adjuster checklist — treatment start, gaps, provider type, active vs passive care, bills vs SOAP notes, upcoding.
68	- https://amp.claimsjournal.com/news/national/2010/12/31/116021.htm — Claims Journal on CFA Colossus report (2010): adjuster selects injury codes; software outputs a general-damages range; insurers tune it.
69	- https://www.michiganautolaw.com/blog/2026/05/13/colossus-personal-injury-calculator/ — Michigan Auto Law (plaintiff firm): Colossus uses many "value drivers" that insurers can adjust.
70	- https://forthepeople.com/blog/what-colossus-claims-software — Morgan & Morgan (plaintiff firm): records lacking ongoing pain/limitation statements score lower.
71	- https://search.txcourts.gov/Case.aspx?cn=09-0377&coa=cossup — Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011), Supreme Court of Texas docket 09-0377: recovery limited to expenses that have been or must be paid; only those are admissible. Billed charges may exceed that where adjusted/paid amounts are lower, so the tool labels amounts "billed" and does not characterize recoverability.
72	- https://www.wlf.org/2021/06/24/publishing/texas-high-court-rulings-on-medical-expense-damages-reel-in-plaintiffs-windfall-profit-tactics/ — WLF (defense-leaning): LOP bills, negotiated-rate discovery (K&L Auto Crushers), §18.001 counteraffidavits (In re Allstate).
73	- https://versustexas.com/blog/what-is-a-gap-in-treatment/ — Versus Texas (plaintiff firm): gap tiers up to 30+ days as a "deal breaker"; firm says these are observations, not statute.
74	- https://www.lezdotechmed.com/blog/plaintiff-and-defense-attorneys-review-the-same-records-completely-differently-here-is-why-that-matters — LezDo (records vendor): defense hunts pre-injury care, pain-imaging mismatch, conflicting histories, copy-forward notes.
75	- https://www.coopers.law/publications/articles/mist-me-litigating-the-minor-impact-soft-tissue-case/ — Cooper (plaintiff): MIST defense blames prior neck/back problems and low impact.
76	- https://www.faegredrinker.com/en/insights/publications/2024/5/responding-to-time-limited-settlement-demands-stowers-demands-and-beyond — Faegre Drinker: Stowers demand elements and insurer response.
77	- Assumptions: Colossus internals are described by plaintiff firms and a consumer group, not the vendor; the 30-day threshold is Appendix A's rule, while adjusters may weigh shorter gaps — note as context, not a finding, unless the tool hides dates.
78	
79	## 10. Limits
80	Do not opine on UI aesthetics, code, accessibility, or privacy law. Do not argue the fictional case's value; attack only what the tool outputs. Do not demand the tool argue the defense position — it must surface facts, not conclusions.
81	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:40.413Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-061; echo \"---\"; grep -n \"D-033\" -A 15 memory/ORCHESTRATOR_DECISIONS.md | head -60; echo \"---\"; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/",
 "description": "Show T-061 card, D-033 decision, and memory dir"
}
````

### User / tool · 2026-11-02T02:14:40.555Z

**tool result**
````
---
id: "T-061"
title: "Self-report label precision: only the patient's own statements (split from T-036 per §7.4)"
milestone: "M2"
role: "researcher"
status: "in_review"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T02:12:03Z"
updated_at: "2026-11-02T02:14:34Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T02:13:03Z"
rounds: 0
commits: ["dd545e3"]
reviews: []
ac:
  - {"n": 1, "text": "lexicon self_report entries only match explicit patient attribution; EMS/witness/spouse/family phrasings have a separate non-patient attribution or none (held-out probes)", "done": true, "evidence": "selfcheck PASS: 26 new probes (explicit_patient 8/8, non_patient_speaker 12/12, headers_not_attribution 5/5 + 2 reclassified) in evals/lexicon_heldout.jsonl; self_report_scope.exclude_sentence added; intake entry self_report false; golden MUST 11/11"}
  - {"n": 2, "text": "flags.py labels patient_report only from those entries; tests cover EMS, wife, witness, 'S:' header", "done": false, "evidence": null}
  - {"n": 3, "text": "memory/DECISIONS.md:286 amended (architect note) or ORCHESTRATOR_DECISIONS entry records the narrowing", "done": false, "evidence": null}
---
## Description
From reviews/T-036-claims-adjuster-r3.md. Lexicon self_report entries + flags labelling: 'S:'/'Self-reported' headers, EMS/witness/spouse/family statements must not be labelled 'Patient self-report'. Researcher amends lexicon; backend-1 adjusts flags.py; ADR-013 note via architect card note.

## Notes (append-only, newest last)
- 2026-11-02T02:12:06Z orchestrator: assigned: researcher-c
- 2026-11-02T02:13:03Z researcher: claimed
- 2026-11-02T02:14:13Z researcher: Lexicon narrowed (commit pending). For backend-1 (flags.py/grounding.py): (1) self_report entries are now only self_reported_prior, patient_attributes_causation, patient_reports_generic; patient_reports_generic no longer matches wife|husband|spouse|family|witness|EMS subjects, a bare 'S:'/'Subjective:' header or 'Self-reported' (patient-reported stays). (2) intake_form_accident_date is self_report: false, so you can delete _NOT_PATIENT_STATEMENT in grounding.py:175. (3) NEW top-level lexicon key self_report_scope.exclude_sentence: if the sentence containing a self_report hit matches that regex (EMS/witness/wife/husband/family/... + speech verb, or 'per his wife/EMS'), the statement is not the patient's -> source_kind stays 'record'. Reference: research/lexicon_selfcheck.py is_patient_statement(). Please replace _PATIENT_WORDS/_SELF word lists with 'any self_report entry hit AND NOT exclude_sentence'. Tests to add: has_self_report False for 'EMS reports neck pain 7/10.', 'Wife complains of neck pain.', 'Witness states the sedan was stopped.', 'S: neck pain 7/10.', 'Self-reported neck pain 7/10.', 'Date of accident per intake form: 2026-01-19.'; True for 'Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient states symptoms began after the January collision.' Probes: evals/lexicon_heldout.jsonl groups explicit_patient, non_patient_speaker, headers_not_attribution (26 rows). Judgement call for the D-entry: T-036 r3 blocker 1 asked S:/Self-reported lines to be labelled patient_report; the coordinator brief asked for none. I followed the brief (a section header is not an explicit attribution); summaries still keep the verbatim marker. For architect: DECISIONS.md:286 and lexicon header lines 25-26 should say 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'.
- 2026-11-02T02:14:18Z researcher: AC 1 checked: selfcheck PASS: 26 new probes (explicit_patient 8/8, non_patient_speaker 12/12, headers_not_attribution 5/5 + 2 reclassified) in evals/lexicon_heldout.jsonl; self_report_scope.exclude_sentence added; intake entry self_report false; golden MUST 11/11
- 2026-11-02T02:14:21Z researcher: moved in_progress -> in_review: AC2 (flags.py/grounding.py + tests) belongs to backend-1 (see card note); AC3 awaits orchestrator D-entry and architect note on DECISIONS.md:286. Lexicon side (AC1) done.
- 2026-11-02T02:14:34Z orchestrator: review dispatched: adjuster (haiku)

## Handoff
Changed: lexicon self_report entries narrowed to explicit patient subjects (patient_reports_generic loses wife/husband/family/witness/EMS, 'S:' header, 'Self-reported'; intake_form_accident_date self_report:false); new self_report_scope.exclude_sentence key + reference is_patient_statement() in lexicon_selfcheck.py; 26 held-out probes. Verified: .venv/bin/python research/lexicon_selfcheck.py -> PASS, held-out 115/115, golden MUST 11/11. Left: AC2 (flags.py/grounding.py + tests) is backend-1's, details in the card note; AC3 needs the orchestrator D-entry and an architect note on DECISIONS.md:286. Surprised: T-036 r3 wanted 'S:' lines labelled patient_report, the brief says none; I followed the brief and flagged the conflict in the note.

---
41:| D-033 | `patient_report` (self-report chip) applies only to explicit patient attribution ('Patient states/reports/notes', 'Pt c/o', patient-quoted speech). EMS narrative, witness, spouse/family statements and generic 'S:'/'Subjective:' headers are not patient self-report (separate or no attribution). Narrows ADR-013 / DECISIONS.md:286. | Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit. | T-036 r3 → T-061 |
---
MEMORY.md
feedback_lexicon_review_method.md
feedback_review_commit_not_worktree.md
project_flag_pass_review_patterns.md
project_flag_source_kind_and_run_signal.md
project_research_attack_map_gaps.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:43.515Z

**tool call — Bash**
````
{
 "command": "git rev-parse --show-toplevel 2>&1; git log --oneline -5 2>&1; echo \"--- show dd545e3 stat\"; git show --stat dd545e3 2>&1 | head -40; echo \"--- status\"; git status --short 2>&1 | head -30",
 "description": "Check git state and commit dd545e3"
}
````

### User / tool · 2026-11-02T02:14:43.680Z

**tool result**
````
/Users/arsis/zlayt-pm-project
dd545e3 feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
099732b feat(backend): LLM split fallback for unsplit pastes, validated by code, flagged LLM_SPLIT (T-057, D-031)
a010dd4 feat(research): synthetic case library, 7 packets with sources and validator (T-052)
2c2eb1f feat(backend): local-mode case list, library loader; api.md audit shapes (T-053)
5650eae docs(contract): POST /api/cases/pdf and record page (T-054)
--- show dd545e3 stat
commit dd545e3ff9918d18ab072141d021c20f33cc733e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:14:23 2026 -0600

    feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

 app/llm/lexicon.yaml          | 23 +++++++++++++++++------
 evals/lexicon_heldout.jsonl   | 29 +++++++++++++++++++++++++++--
 research/lexicon_selfcheck.py | 20 ++++++++++++++++++++
 3 files changed, 64 insertions(+), 8 deletions(-)
--- status
 M .claude/agent-memory/claims-adjuster-reviewer/MEMORY.md
 M .claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md
 M .claude/agent-memory/legal-nurse-reviewer/MEMORY.md
 M .claude/agent-memory/legal-nurse-reviewer/feedback_lexicon_recall_and_negation.md
 M .claude/agent-memory/paralegal-reviewer/MEMORY.md
 M .claude/agent-memory/paralegal-reviewer/golden-set-recurring-findings.md
 M .claude/agent-memory/privacy-compliance-reviewer/MEMORY.md
 M .claude/agent-memory/privacy-compliance-reviewer/recurring-findings.md
 M .claude/agent-memory/product-manager-reviewer/MEMORY.md
 M .claude/agent-memory/product-manager-reviewer/feedback_needs_chris_drift.md
 M .claude/agent-memory/product-manager-reviewer/feedback_spec_review_patterns.md
 M .claude/agent-memory/product-manager-reviewer/project_t013_review_history.md
 M .claude/agent-memory/product-manager-reviewer/reference_reviewer_sandbox.md
 M .claude/agent-memory/security-reviewer/MEMORY.md
 M .claude/agent-memory/security-reviewer/project_hook_guard_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/MEMORY.md
 M .claude/agent-memory/staff-engineer-reviewer/project_design_review_patterns.md
 M .claude/agent-memory/staff-engineer-reviewer/project_harness_review_patterns.md
 M app/db/db.py
 M app/db/schema.sql
 M app/frontend/index.html
 M app/frontend/review.css
 M board/activity.jsonl
 M board/cards/T-036.md
 M board/cards/T-037.md
 M board/cards/T-038.md
 M board/cards/T-040.md
 M board/cards/T-045.md
 M board/cards/T-050.md
 M board/cards/T-051.md
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:43.922Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python research/lexicon_selfcheck.py 2>&1 | tail -40; echo \"EXIT=$?\"",
 "description": "Run lexicon selfcheck"
}
````

### User / tool · 2026-11-02T02:14:44.179Z

**tool result**
````
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

[held-out] lexicon_heldout.jsonl: 115/115 = 100% (bar 85%); prior_level 12/12, prior_since_year 10/10, prior_treatment 7/7, hedge 17/17, attribution 11/11, non_patient_speaker 14/14, self_report 1/1, quiet_post_accident 23/23, quiet_hedge 5/5, quiet_self_report 2/2, explicit_patient 8/8, headers_not_attribution 5/5

SUMMARY golden MUST recall 11/11, SHOULD 1/1; must_not violations 0; probe FP 0, FN 1 of 140; held-out 115/115
RESULT: PASS
EXIT=0
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:44.270Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2",
 "description": "Run flag and lexicon unit tests"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:44.478Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-036-claims-adjuster-r3.md"
}
````

### User / tool · 2026-11-02T02:14:46.295Z

**tool result**
````
FAILED tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution
1 failed, 113 passed, 699 deselected in 1.60s
````

### User / tool · 2026-11-02T02:14:46.301Z

**tool result**
````
1	# T-036 LLM flag passes, round 3 (commit 3f37141): claims-adjuster review (Gary Pruitt)
2	
3	Verdict: **fail** (1 blocker, 2 major).
4	
5	Round-2 items, status on 3f37141 (probes run on an extracted copy of the commit tree, `git archive 3f37141`, because the live working tree has uncommitted edits to confidence.py, flag_templates.py, why.py and pipeline.py):
6	
7	- Round-2 blocker (source_kind must come from lexicon self_report): **partly resolved.** The two lines r2 named are now `patient_report` ("Patient notes prior neck pain.", "Patient links her neck pain to the collision."), and the record-7 intake date stays `record`. Two lexicon-matched self-report forms still read as `record` (finding 1). Non-patient complaint subjects now get `patient_report` through a different path (finding 2). The spec clauses were not amended (finding 3).
8	- Round-2 major (run-level conflict signal): **not counted**, per the brief. The `CONFLICT_PASS_INCOMPLETE` line is pending backend-2. On the commit, `status=done` with `warnings=[]` on both failure paths (probe section 5). The r3 test that asserts it (`test_flags_pass.py::test_pipeline_surfaces_conflict_pass_failure_as_run_warning`) is the one red test in that file, for the same reason.
9	- Round-2 minor (case-level warning pinned to record 1): **resolved.** `record_no=None`, `record_nos=[]`, and the why text no longer says "no AI-made entry" (probe section 5).
10	- Round-2 nit (`.”.` double period): **resolved.** Render sweep over all categories and two quotes shows no `.”.` (probe section 6).
11	
12	Findings:
13	
14	1. **Blocker.** Lexicon self-report wording still reads as a record statement. "S: neck pain 7/10." and "Self-reported neck pain 7/10." match a `self_report` entry in lexicon.yaml:744 but give `source_kind=record`. This is the r2 blocker class (spec DECISIONS.md:286: `source_kind` is "set by code from the lexicon `self_report` entries on the excerpt"). The cause is the word filter `_PATIENT_WORDS` at grounding.py:177, which lists `patient|pt|he|she|client|c/o|complain|subjective|patient-reported` but not `S` or `self`. The SOAP "S:" marker is the record's own subjective marker, so a patient's statement is shown as a record statement. No text is invented, but the attribution is lost. Same mechanism and same severity as r2 finding 1.
15	
16	2. **Major.** Complaints from a non-patient subject are labelled "Patient self-report". "EMS complains of neck pain 7/10.", "Witness complains of neck pain.", "Wife complains of neck pain." and "Family complains of neck pain." all return `has_self_report=True`. The cause is `complain(?:s|ed|ing|t)?` in `_SELF` (grounding.py:167) and `complain\w*` in `_PATIENT_WORDS` (grounding.py:177). lexicon.yaml:744 still lists wife|husband|family|witness|EMS before "complains". The r3 exclusion only works for the "reports/states" verbs, so r2 finding 1's fix item 3 (remove EMS, witness, wife, husband, family, friend) is only partly met. The chip "Patient self-report" then tells the reader the claimant said it. Over-attribution, not invention.
17	
18	3. **Major.** The spec and lexicon were not amended for the narrowing the code now does. `git show --stat 3f37141` lists no memory/DECISIONS.md and no app/llm/lexicon.yaml. DECISIONS.md:286 still says "set by code from the lexicon `self_report` entries"; lexicon.yaml:25-26 still says "code sets source_kind = patient_report from it (ADR-013)"; lexicon.yaml:759-764 still marks `intake_form_accident_date` `self_report: true`, and code excludes it by name (grounding.py:175). Probe section 2 shows the intake example as a lexicon hit with `has_self_report=False`, and section 4 counts 8 lexicon-matched excerpts that code marks `record`. r2 made the narrowing conditional on a same-commit spec amendment (questions_for_chris #1 in r2); that condition is not met.
19	
20	What is right:
21	- Record 7's intake date is `source_kind=record` on the commit (probe section 1: `f_r7_1 ... source_kind=record ... "Date of accident per intake form: 2026-01-19."`). Record 3 ("Patient reports low back pain in 2023, resolved.") and record 9 ("Patient states symptoms began after the January collision.") are `patient_report`.
22	- Sample-case flags on the commit tree: the gap reads "Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient)." with no invented reason; the conflict reads "...The records disagree; the tool does not choose between them."; no delay from an accident date is computed.
23	- Template neutrality holds: no own-voice adjective, no double period on any rendered category.
24	
25	Exercised (all on the extracted commit tree unless marked):
26	- Read personas/claims-adjuster.md in full; read reviews/T-036-claims-adjuster-r2.md; read my memory dir.
27	- `git show --stat 3f37141`, `git show --stat --format= 3f37141 | grep -E "DECISIONS|lexicon"` (no output: not amended), `git diff --stat 3f37141 -- <r3 files>` (working tree differs in confidence.py, flag_templates.py, why.py, pipeline.py: uncommitted, not reviewed).
28	- `grep -n "self_report" app/backend/flags.py` -> `flags.py:42 "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",` and `flags.py:115 lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"` (no direct lexicon reference in flags.py; the lexicon contribution is in grounding._self_report, grounding.py:180-188).
29	- `grep -n "self_report" app/backend/grounding.py`, `sed -n 165,225p`, `grep -n "self_report" -B3 -A8 app/llm/lexicon.yaml`, `sed -n 18,30p app/llm/lexicon.yaml`, `sed -n 280,292p memory/DECISIONS.md`.
30	- Parsed lexicon.yaml: 4 self_report entries; patterns and examples listed.
31	- `.venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2` on the live tree -> `48 passed in 0.27s`; same command on the extracted commit tree -> `48 passed in 0.27s`.
32	- `.venv/bin/python tests/fixtures/make_curated.py --check` (live tree and extracted commit tree) -> `entries: 9 non-verified: []` / `letter equal: True | notes equal: True`, exit 0.
33	- `.venv/bin/python -m pytest tests/unit/test_flags_pass.py -q` on the commit tree -> `1 failed, 14 passed` (the failure is the pending CONFLICT_PASS line; excluded).
34	- `.venv/bin/python -m pytest tests/unit -q` on the commit tree -> `2 failed, 765 passed` (test_flags_pass.py pending item; test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode, IndexError, not triaged and not attributed to r3).
35	- `artifacts/review-evidence/T-036-r3-probe.py <tree>` run on the extracted commit tree -> `artifacts/review-evidence/T-036-r3-commit-probe.txt` (sample run, own-example parity, 21 probe strings, spec-literal gap list, conflict failure paths, template sweep). Same script on the live tree -> `artifacts/review-evidence/T-036-r3-probe.txt` (superseded; same findings).
36	- Extracted tree: `git archive 3f37141 | tar -x -C artifacts/review-evidence/T-036-r3-commit-3f37141`.
37	
38	Outside my lens: the wording of the "Cross-record check did not finish" title and the CONFLICT_CHECK_INCOMPLETE why are product copy; I checked only that they carry no attribution error.
39	
40	```json
41	{"card": "T-036", "persona": "claims-adjuster-reviewer", "model": "claude-haiku-5-5",
42	 "scope": "commit 3f37141 (app/backend/grounding.py, flags.py, flag_templates.py, why.py, confidence.py, tests/unit/test_flags_pass.py, memory/contracts/api.md) run from an extracted git-archive copy; spec memory/DECISIONS.md:286; app/llm/lexicon.yaml; sample case evals/golden/sample.txt via the fixture pipeline (no live app URL; LLM is scripted FakeCall). Live working tree has uncommitted edits not reviewed.",
43	 "exercised": [
44	  "Read personas/claims-adjuster.md in full; read reviews/T-036-claims-adjuster-r2.md and my memory dir",
45	  "git show --stat 3f37141 (no DECISIONS.md or lexicon.yaml in the commit)",
46	  "git diff --stat 3f37141 -- app/backend/grounding.py app/backend/flags.py app/backend/flag_templates.py app/backend/why.py app/backend/confidence.py app/llm/lexicon.yaml tests/unit/test_flags_pass.py (live tree differs in confidence.py, flag_templates.py, why.py, pipeline.py)",
47	  "grep -n 'self_report' app/backend/flags.py -> flags.py:42 and flags.py:115 (has_self_report calls)",
48	  "grep -n 'self_report' app/backend/grounding.py; sed -n 165,225p app/backend/grounding.py (_SELF:167, _NOT_PATIENT_STATEMENT:175, _PATIENT_WORDS:177, _self_report:180-188)",
49	  "grep -n 'self_report' -B3 -A8 app/llm/lexicon.yaml; sed -n 18,30p app/llm/lexicon.yaml; yaml parse of 4 self_report entries (self_reported_prior:477, patient_attributes_causation:727, patient_reports_generic:743, intake_form_accident_date:759)",
50	  "sed -n 280,292p memory/DECISIONS.md (line 286 spec)",
51	  ".venv/bin/python -m pytest tests/unit/test_flags_sample.py tests/unit/test_flags_injection.py tests/unit/test_flag_templates.py -q 2>&1 | tail -2 -> 48 passed in 0.27s (live tree and extracted commit tree)",
52	  ".venv/bin/python tests/fixtures/make_curated.py --check -> letter equal: True | notes equal: True (live and commit tree)",
53	  ".venv/bin/python -m pytest tests/unit/test_flags_pass.py -q (commit tree) -> 1 failed, 14 passed (pending CONFLICT_PASS line; excluded)",
54	  ".venv/bin/python -m pytest tests/unit -q (commit tree) -> 2 failed, 765 passed (pending-line test; test_api_routes judge-unavailable IndexError, not attributed)",
55	  "git archive 3f37141 | tar -x -C artifacts/review-evidence/T-036-r3-commit-3f37141; artifacts/review-evidence/T-036-r3-probe.py <tree> -> artifacts/review-evidence/T-036-r3-commit-probe.txt (sections 1-6: sample flags with source_kind, own-example parity, 21 probe strings with lexicon hit vs has_self_report vs lexicon_flags, spec-literal gap list, conflict failure paths, template sweep)",
56	  "sample text evals/golden/sample.txt (records 1, 3, 6, 7, 9 verbatim lines checked against flag excerpts)"
57	 ],
58	 "verdict": "fail",
59	 "scores": {"surfaces_every_attack_item_on_sample": 5, "no_invented_or_overstated_text": 3, "patient_attribution_label": 2, "visible_conflict_failure": 4, "template_neutrality": 5, "test_honesty": 3},
60	 "findings": [
61	  {"severity": "blocker",
62	   "title": "Lexicon self_report wording still reads as a record statement: 'S: neck pain 7/10.' and 'Self-reported neck pain 7/10.' give source_kind=record",
63	   "evidence": "artifacts/review-evidence/T-036-r3-commit-probe.txt section 3: \"'S: neck pain 7/10.' expect=patient lex=True has_self_report=False | no lexicon flag <-- DISAGREES\" and \"'Self-reported neck pain 7/10.' expect=patient lex=True has_self_report=False\"; section 4 lists both as 'lexicon says self_report, code says record'. Lexicon: app/llm/lexicon.yaml:744 pattern ends with `|\\b(?:patient|self)-?\\s?reported\\b|^\\s*(?:subjective|S)\\s*:`. Filter: app/backend/grounding.py:177 `_PATIENT_WORDS = ... \\b(?:patient|pt|he|she|client|c/o|complain\\w*|subjective)\\b|patient-reported` (no S, no self). Spec: memory/DECISIONS.md:286 'source_kind = \"patient_report\" is set by code from the lexicon self_report entries on the excerpt'.",
64	   "why_it_matters": "Same clause and same loss as r2 blocker 1. The lexicon marks these lines as patient self-report and the code does not. In a SOAP note 'S:' is the record's own subjective marker, so the claimant's statement reads as a record statement. Nothing is invented (the verbatim quote keeps the marker), but the attribution the spec requires is lost, and the r3 test list (test_flags_pass.py yes-list) does not cover these forms.",
65	   "fix": "Replace the word whitelist with a subject exclusion: a lexicon self_report hit counts as patient_report unless the match begins with a non-patient subject (EMS, witness, wife, husband, spouse, mother, father, parent, family, friend). This also covers finding 2. Drop the _NOT_PATIENT_STATEMENT name list only if finding 3 is resolved by setting intake_form_accident_date self_report: false in lexicon.yaml.",
66	   "acceptance_test": "tests/unit/test_flags_pass.py: grounding.has_self_report('S: neck pain 7/10.') and has_self_report('Self-reported neck pain 7/10.') are True; lexicon_flags on those lines (or the LLM+lexicon path) gives source_kind 'patient_report'; the existing r3 yes/no lists still pass."},
67	  {"severity": "major",
68	   "title": "Complaints from EMS, a witness, a wife or family are labelled 'Patient self-report' because the complaint verb bypasses the subject filter",
69	   "evidence": "artifacts/review-evidence/T-036-r3-commit-probe.txt section 3: \"'EMS complains of neck pain 7/10.' expect=record ... has_self_report=True <-- DISAGREES\"; \"'Witness complains of neck pain.' ... has_self_report=True\"; \"'Wife complains of neck pain.' ... has_self_report=True\"; \"'Family complains of neck pain.' ... has_self_report=True\". Cause: app/backend/grounding.py:167 _SELF `\\bcomplain(?:s|ed|ing|t)?\\b` and grounding.py:177 `complain\\w*` in _PATIENT_WORDS; lexicon.yaml:744 lists wife|husband|spouse|mother|father|parent|family|friend|witness|EMS before `complains`. The r3 no-list (test_flags_pass.py) only checks 'reports' and 'states' forms.",
70	   "why_it_matters": "The r2 finding 1 fix (item 3) asked that EMS, witness, wife, husband, family and friend not set patient_report. The r3 exclusion only covers the reports/states verbs. The chip 'Patient self-report' and its explanation '(not a physician's opinion)' then credit the claimant with a statement a family member or EMS made. That is an attribution error, not an invented fact, so major rather than blocker.",
71	   "fix": "Apply the non-patient subject exclusion to the whole match regardless of verb (see blocker fix). Either remove the non-patient subjects from lexicon.yaml:744 (r2 fix item 3) or keep them and exclude in code; say which in DECISIONS.md.",
72	   "acceptance_test": "has_self_report is False for 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'EMS reports neck pain 7/10.', 'Wife reports he was in pain.'; True for 'Patient complains of neck pain.' and 'C/O neck pain 7/10 and headache.'"},
73	  {"severity": "major",
74	   "title": "Spec (DECISIONS.md:286) and lexicon header (lexicon.yaml:25-26) not amended for the narrowing the code now applies; lexicon and code disagree on 8 excerpts",
75	   "evidence": "git show --stat 3f37141: no memory/DECISIONS.md and no app/llm/lexicon.yaml in the commit. DECISIONS.md:286 still: 'source_kind = \"patient_report\" is set by code from the lexicon self_report entries on the excerpt'. lexicon.yaml:25-26 still: 'code sets source_kind = \"patient_report\" from it (ADR-013)'. lexicon.yaml:759-764 still `self_report: true` for intake_form_accident_date; code skips it by name at grounding.py:175 (`_NOT_PATIENT_STATEMENT = {\"intake_form_accident_date\"}`). Probe section 2: \"[intake_form_accident_date] lex=True has_self_report=False 'Date of accident per intake form: 2026-01-19.' <-- MISMATCH\". Probe section 4 count: 8.",
76	   "why_it_matters": "r2 made the narrowing conditional: 'If the narrowing was intended, amend DECISIONS.md:286 and lexicon.yaml:25-26 in the same commit.' Neither file changed. A future worker or reviewer reading the contract gets a different rule from the code. The narrowing itself is correct for the intake date and EMS/witness statements; the contract is what is wrong.",
77	   "fix": "Either (a) amend DECISIONS.md:286 and lexicon.yaml:25-26 to state the subject rule and the intake exclusion, and set intake_form_accident_date self_report: false in lexicon.yaml so the lexicon is the single source; or (b) move the rule into lexicon.yaml and remove _NOT_PATIENT_STATEMENT. Chris decides (question 1).",
78	   "acceptance_test": "A parity test reads lexicon.yaml self_report entries and asserts has_self_report(example) for every example.hit that is not a non-patient subject, with no code-side name list; grep -n '_NOT_PATIENT_STATEMENT' app/backend/grounding.py returns nothing, or DECISIONS.md:286 names the exclusion."}
79	 ],
80	 "whats_right": [
81	  "Record 7's intake date is source_kind 'record' on 3f37141 (f_r7_1 in T-036-r3-commit-probe.txt section 1), and record 3 and record 9 remain 'patient_report'.",
82	  "The case-level conflict warning carries record_no None and record_nos [] with a neutral why (section 5), and no template renders the '.”.' double period (section 6).",
83	  "The sample gap flag states 'Gap of 73 days between March 6, 2026 (Capital PT, visit 9) and May 18, 2026 (Hill Country Pain Management, new patient).' with no invented reason, and the conflict flag says the tool does not choose between the two accident dates."
84	 ],
85	 "questions_for_chris": [
86	  "Which way should the source_kind contract go: amend DECISIONS.md:286 and lexicon.yaml:25-26 to match the subject-exclusion code (and set intake_form_accident_date self_report: false), or restore the code to the literal lexicon rule? My recommendation is the first, so the lexicon is the single source.",
87	  "Should 'Wife complains of' and 'Family complains of' carry 'Patient self-report' at all? I treat them as misattributed; the lexicon (lexicon.yaml:744) currently says they are self-report.",
88	  "Who owns test_api_routes.py::test_judge_unavailable_edit_is_saved_with_warning_in_demo_mode (IndexError on the commit tree)? It is outside the r3 diff, and I did not triage it.",
89	  "Model id: I ran as claude-haiku-5-5; the persona file expects claude-opus-5-5 in the review record. I wrote the id I ran as. Confirm that is acceptable for the gate."
90	 ]}
91	```
92	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:48.629Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | grep -v \"^\\s*$\" | sed -n '1,80p'",
 "description": "Show full failure detail for flag/lexicon tests"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:49.772Z

**tool call — Bash**
````
{
 "command": "grep -rn \"lexicon_self_report_drives_source_kind\" tests/ ; echo ---; git log --oneline -1 -- tests/unit/test_flags_pass.py; git status --short tests/unit/test_flags_pass.py app/backend/grounding.py app/backend/flags.py app/llm/lexicon.yaml research/lexicon_selfcheck.py evals/lexicon_heldout.jsonl; echo \"--- HEAD diff vs worktree for grounding/flags:\"; git diff --stat HEAD -- app/backend/grounding.py app/backend/flags.py tests/unit/ app/llm/lexicon.yaml research/ evals/ | tail -5",
 "description": "Locate failing test and check file state vs HEAD"
}
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:50.263Z

**tool call — Bash**
````
{
 "command": "git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py | head -150",
 "description": "Show the commit's lexicon and selfcheck diff"
}
````

### User / tool · 2026-11-02T02:14:50.716Z

**tool result**
````
...........................................................F............ [ 63%]
..........................................                               [100%]
=================================== FAILURES ===================================
_ test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution _
    def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution():
        """Review T-036 r2 blocker: ADR-013 - source_kind comes from lexicon self_report entries; intake form / EMS / wife do not qualify."""
        from app.backend import grounding as GR
        yes = ["Patient notes prior neck pain.", "Patient links her neck pain to the collision.", "Subjective: neck pain 7/10.",
               "Patient describes neck pain since the collision.", "Patient-reported neck pain 7/10.", "Patient reports prior neck pain.",
               "C/O neck pain 7/10 and headache."]
        no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage."]
>       assert all(GR.has_self_report(t) for t in yes) and not any(GR.has_self_report(t) for t in no)
E       assert (False)
E        +  where False = all(<generator object test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution.<locals>.<genexpr> at 0x10ac8f300>)
tests/unit/test_flags_pass.py:121: AssertionError
=========================== short test summary info ============================
FAILED tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution
1 failed, 113 passed, 699 deselected in 1.68s
````

### User / tool · 2026-11-02T02:14:50.829Z

**tool result**
````
commit dd545e3ff9918d18ab072141d021c20f33cc733e
Author: Chris Borsheim <cborsheim@gmail.com>
Date:   Sun Nov 1 20:14:23 2026 -0600

    feat(research): narrow lexicon self_report to explicit patient attribution (T-061)
    
    Co-Authored-By: Claude Sonnet 5.5 <noreply@anthropic.com>

diff --git a/app/llm/lexicon.yaml b/app/llm/lexicon.yaml
index ea28be2..d3b73e0 100644
--- a/app/llm/lexicon.yaml
+++ b/app/llm/lexicon.yaml
@@ -22,7 +22,7 @@
 #   prior_surgery, alternative_cause, scene_facts, objective_negative, litigation_referral, recovery_context,
 #   accident_date_provenance.
 # - `hedge: true` marks the R-TL-8 hedge set: a sentence with a hedge hit is a qualifier unit and can never be cut
-#   from an excerpt (ADR-016). `self_report: true` marks patient-attributed wording; code sets
+#   from an excerpt (ADR-016). `self_report: true` marks wording that explicitly attributes a statement to the PATIENT (T-061); code sets
 #   source_kind = "patient_report" from it (ADR-013). Self-report entries are never hedges.
 # - `strength`: high and medium raise a flag (origin lexicon, or lexicon+llm). low is context only: it never
 #   raises a flag alone. It can still attach to an LLM flag, keep attribution in a summary, or mark a qualifier unit.
@@ -81,6 +81,17 @@ negation:
     Round 2 removed 'did not show' from the pseudo list: it now NEGATES ("MRI did not show degenerative changes").
     The no-show entry matches only "did not show up/for".
 
+# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
+# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
+# "per <wife|husband|EMS|...>"). Bare "S:", "Subjective:" and "Self-reported" headers are not matched by any self_report entry,
+# and the intake-form date entry is self_report: false. Reference implementation: research/lexicon_selfcheck.py:is_patient_statement().
+self_report_scope:
+  exclude_sentence: '\b(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w''-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|\bper\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b'
+  note: 'Sentence-level test: the sentence containing the match is searched; a hit means the statement is not the patient''s, so source_kind stays "record" and no "Patient self-report" label is shown.'
+  examples:
+    exclude: ['EMS reports neck pain 7/10.', 'Wife complains of neck pain.', 'Per his wife, headaches began at the scene.']
+    keep: ['Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.']
+
 entries:
 
 # ───────────────────────── pre_existing ─────────────────────────
@@ -741,16 +752,16 @@ entries:
     miss: ['Physician opines symptoms are causally related to the collision.']
 
 - id: patient_reports_generic
-  pattern: '\b(?:patient|pt\.?|he|she|client|wife|husband|spouse|mother|father|parent|family|friend|witness|EMS)\s+(?:reports|reported|states|stated|endorses|complains|c/o|describes|relates|notes|admits|recalls)\b|\bc/o\b|\bcomplain(?:s|ing)?\s+of\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\b(?:patient|self)-?\s?reported\b|^\s*(?:subjective|S)\s*:'
+  pattern: '\b(?:patient|pt\.?|he|she|client)\s+(?:reports|reported|states|stated|endorses|complains|c/o|describes|relates|notes|admits|recalls)\b|\bc/o\b|\bcomplain(?:s|ing)?\s+of\b|\bper\s+(?:the\s+)?(?:patient|pt)\b|\bpatient-?\s?reported\b'
   flag_type: causation
   category: patient_report
   hedge: false
   self_report: true
   strength: low
   negatable: false
-  rationale: 'Marks subjective, self-reported content (as opposed to objective findings), which adjusters weight less. Context only; it keeps attribution in the summary ("C/O neck pain 7/10" must stay a complaint, not become a finding).'
+  rationale: 'Marks content the record attributes explicitly to the patient (as opposed to objective findings), which adjusters weight less. Context only; it keeps attribution in the summary ("C/O neck pain 7/10" must stay a complaint, not become a finding).'
   source: 'AA A9; AA src 1, src 18 (objective findings weighted above subjective); reviews/T-009-legal-nurse.md (minor: C/O)'
-  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. "Per patient, pain 5/10 today" is benign and stays low.'
+  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
   appendix_c: [1, 3, 5, 9]
   examples:
     hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'C/O neck pain 7/10 and headache.', 'Pt states pain worse with rotation.', 'Patient endorses headaches.', 'Per patient, pain 5/10 today.']
@@ -761,12 +772,12 @@ entries:
   flag_type: causation
   category: accident_date_provenance
   hedge: false
-  self_report: true
+  self_report: false
   strength: high
   negatable: false
   rationale: 'An accident date or history taken from an intake form or the patient, not the clinician. Record 7''s "Date of accident per intake form: 2026-01-19" conflicts with the EMS/ER treatment dates (2026-01-09). The defense uses a second date to suggest a different incident (JLG Trucking). The code conflict rule (ADR-014) owns the conflict; this entry flags the provenance wording.'
   source: 'AA A7; AA src 10 (JLG Trucking), src 17 (impeachment with intake forms); Appendix C record 7'
-  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). "Per protocol" does not match.'
+  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). T-061: self_report is false here because an intake form is a document, not the patient''s statement; source_kind stays "record". "Date of injury per patient" is still caught by patient_reports_generic. "Per protocol" does not match.'
   appendix_c: [7]
   examples:
     hit: ['Date of accident per intake form: 2026-01-19.', 'Date of injury per patient: 03/02/2026.']
diff --git a/research/lexicon_selfcheck.py b/research/lexicon_selfcheck.py
index 9a8d54b..055af5d 100644
--- a/research/lexicon_selfcheck.py
+++ b/research/lexicon_selfcheck.py
@@ -159,12 +159,25 @@ def _clause_after(text, end):
     return text[end:end + m.start()] if m else text[end:]
 
 
+SR_EXCLUDE = None  # compiled in main() from lexicon self_report_scope.exclude_sentence
+
+
+def is_patient_statement(text, start, end):
+    """T-061: True unless the sentence around the match names a non-patient speaker (EMS, witness, spouse, family)."""
+    if SR_EXCLUDE is None:
+        return True
+    s0, s1 = _sentence_bounds(text, start, end)
+    return not SR_EXCLUDE.search(text[s0:s1])
+
+
 def hits(entry, text, neg, accident_year):
     """List of (start, end, matched) that FIRE (not negated / filtered / suppressed)."""
     out = []
     for m in entry["_rx"].finditer(text):
         if entry.get("negatable") and negated(text, m.start(), m.end(), neg):
             continue
+        if entry.get("self_report") and not is_patient_statement(text, m.start(), m.end()):
+            continue
         if entry.get("year_filter") and accident_year:
             y = _hit_year(m)
             if y and y >= accident_year:
@@ -212,7 +225,14 @@ def _overlaps(text, span, excerpt):
 
 def main():
     lex = yaml.safe_load(LEX.read_text())
+    global SR_EXCLUDE
     neg = lex["negation"]
+    SR_EXCLUDE = re.compile(lex["self_report_scope"]["exclude_sentence"], re.I)
+    for k in ("exclude", "keep"):
+        for ex_s in lex["self_report_scope"]["examples"][k]:
+            if bool(SR_EXCLUDE.search(ex_s)) != (k == "exclude"):
+                print(f"ERROR self_report_scope example {k}: {ex_s!r}")
+                sys.exit(1)
     entries = lex["entries"]
     types = set(lex["flag_types"])
     errors, ids = [], set()
````

### User / tool · 2026-11-02T02:14:50.873Z

**tool result**
````
tests/unit/test_flags_pass.py:114:def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution():
---
5216d06 fix(backend): D-032 objective_negative context only, scene_facts need phrase list, one flag per prior-condition sentence
--- HEAD diff vs worktree for grounding/flags:
 evals/reports/latest.json | 78 +++++++++++++++++++++++++----------------------
 1 file changed, 41 insertions(+), 37 deletions(-)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:14:50.911Z

**tool call — Bash**
````
{
 "command": "for f in feedback_lexicon_review_method project_flag_source_kind_and_run_signal feedback_review_commit_not_worktree project_flag_pass_review_patterns; do echo \"=== $f\"; cat .claude/agent-memory/claims-adjuster-reviewer/$f.md; done",
 "description": "Read recurring-finding memory files"
}
````

### User / tool · 2026-11-02T02:14:51.002Z

**tool result**
````
=== feedback_lexicon_review_method
---
name: lexicon-review-method
description: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes
metadata:
  type: feedback
---

A lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real
adjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).

**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.

**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo
guard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).
Always probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) "No acute fracture, chronic degenerative changes"
(comma-scope negation); (3) intake checkboxes "Prior injuries: No."; (4) ROS denial lists >6 tokens; (5) "did not present
with"; (6) MIST/scene facts and "out of proportion". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,
compliance→causation mapping). See [[research-attack-map-gaps]].
=== project_flag_source_kind_and_run_signal
---
name: flag-source-kind-and-run-signal
description: T-036 source_kind history: r2 (cd4bc60) dropped the lexicon self_report contract; r3 (3f37141) restored it via a word filter that still misses "S:"/"Self-reported" and lets "complains" subjects through; spec never amended
metadata:
  type: project
---

Round 2 (cd4bc60) fixed the intake-date mislabel by deleting the lexicon `self_report` contribution from `grounding._self_report` for every entry. Spec (memory/DECISIONS.md:286) says source_kind is set by code from the lexicon self_report entries. Blocker, r2.

Round 3 (3f37141) restored the lexicon contribution, but behind a word filter: `_PATIENT_WORDS` (grounding.py:177) must find patient|pt|he|she|client|c/o|complain|subjective|patient-reported in the matched text, and `intake_form_accident_date` is skipped by name (grounding.py:175). Result on the commit:
- Still wrong: "S: neck pain 7/10." and "Self-reported neck pain 7/10." (lexicon.yaml:744 matches; code says record). Blocker, r3.
- Over-attributed: "EMS / Witness / Wife / Family complains of ..." give patient_report, because `complain` is in `_SELF` (grounding.py:167) and `_PATIENT_WORDS`. Major, r3.
- Spec not amended: DECISIONS.md:286 and lexicon.yaml:25-26 unchanged in the commit; 8 lexicon-matched excerpts disagree with code. Major, r3.
- Record 7 intake date stays `record` (good); record 3 and 9 stay `patient_report` (good).

**Why:** each round narrows a classifier to fix the one named example, then the narrowing misses an adjacent lexicon form. The r2 fix was to remove the mechanism; the r3 fix added a word whitelist that the lexicon's own patterns do not match.

**How to apply:** when source_kind or any label is touched, probe every lexicon self_report entry's examples.hit AND the abbreviations/verbs the pattern lists (S:, self-reported, complains, wife/EMS subjects) through grounding.has_self_report and lexicon_flags. Check whether DECISIONS.md:286 and lexicon.yaml header were amended in the same commit. Evidence for r3: artifacts/review-evidence/T-036-r3-probe.py and T-036-r3-commit-probe.txt. Earlier: T-036-r2-probe*.py.

Related: [[feedback_lexicon_review_method]], [[project_flag_pass_review_patterns]], [[feedback_review_commit_not_worktree]].
=== feedback_review_commit_not_worktree
---
name: review-commit-not-worktree
description: When the live working tree has uncommitted edits to the files under review, probe the named commit (git archive into artifacts/review-evidence, then run the probe with the tree root as argument) and say so in the review
metadata:
  type: feedback
---

On T-036 r3 the live tree had uncommitted edits to confidence.py, flag_templates.py, why.py and pipeline.py (other workers in flight), so `git diff --stat <commit> -- <files>` was non-empty even for files the round was about. Probes on the live tree would have tested code the commit does not contain.

**Why:** a verdict on a round must cite the commit's behaviour. Working-tree results can pass or fail for reasons outside the commit (e.g., an uncommitted LLM_SPLIT template or a pipeline.py warning line).

**How to apply:** run `git diff --stat <sha> -- <files under review>`. If non-empty, run `git archive <sha> | tar -x -C artifacts/review-evidence/<dir>` (create the dir first with mkdir -p) and run the probe script with that dir as argument, plus pytest from inside that dir with `.venv/bin/python -m pytest ... -p no:cacheprovider`. Name the tree in the review's scope. Delete the extracted dir afterwards: it contains a full copy of artifacts and should not be left in place.

Note: the Bash hook (board-guard) denies commands with backticks in a heredoc or inline python -c; use a single-quoted heredoc without backticks.

Related: [[project_flag_source_kind_and_run_signal]].
=== project_flag_pass_review_patterns
---
name: flag-pass-review-patterns
description: T-036 flag-engine review (2026-11-01): recurring weak spots — vacuous guard tests, silent-empty on LLM failure, label inference, full-suite not run by worker
metadata:
  type: project
---

T-036 r0 (fail): sample flags all surface via lexicon floor and K1-K5 one-to-one holds, but:
- flag_templates.py title "No objective findings noted" for objective_negative (orchestrator said never display "objective");
  the guard test checks only the string "objective_negative" on a record with no hit, so it passes vacuously.
- run_conflict_pass swallows LLMFailed/FixtureMiss/ValidationError -> [] with status done, no warning; C2 (12 vs 9 visits)
  has no lexicon floor (plan_not_completed is strength low).
- Worker verified only its own 59 tests; full `pytest tests/unit` had 3 red test_pipeline J3 tests.
- source_kind patient_report inferred from lexicon self_report:true on intake_form_accident_date (record does not say patient wrote it).

**Why:** workers' evidence cites subset runs and tests that cannot fail; failure paths return empty instead of a visible marker.

**How to apply:** always run the FULL tests/unit, probe every flag_templates category title for banned words
(objective/subjective/failure to mitigate), and force LLMFailed/FixtureMiss on each LLM stage in the full pipeline (probe scripts in
artifacts/review-evidence/T-036-*.py). On re-review check the same four items. Related: [[lexicon-review-method]].
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:09.872Z

**tool call — Bash**
````
{
 "command": "echo \"== grounding.py 160-225\"; sed -n 160,225p app/backend/grounding.py; echo \"== flags.py refs\"; grep -n \"has_self_report\\|patient_report\\|source_kind\\|lexicon_flags\" app/backend/flags.py | head -30; echo \"== lexicon self_report entries\"; grep -n \"self_report: true\" -B12 app/llm/lexicon.yaml | grep -n \"id:\\|self_report\" ; echo \"== DECISIONS 286\"; sed -n 284,288p memory/DECISIONS.md",
 "description": "Read grounding self-report code, flags refs, spec line"
}
````

### User / tool · 2026-11-02T02:15:09.978Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:11.129Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -m pytest tests/unit/test_flags_pass.py -q -k lexicon_self_report 2>&1 | tail -3; echo \"== test body\"; sed -n 110,135p tests/unit/test_flags_pass.py; echo \"== grep tests for new T-061 probes\"; grep -rn \"EMS complains\\|Witness states\\|Wife reports\\|S: neck\\|Per EMS\" tests/ | head; echo \"== heldout groups\"; .venv/bin/python -c \"\nimport json,collections\nc=collections.Counter(json.loads(l).get('group') for l in open('evals/lexicon_heldout.jsonl') if l.strip())\nprint(c)\"",
 "description": "Run failing test alone and inspect held-out groups"
}
````

### User / tool · 2026-11-02T02:15:11.690Z

**tool result**
````
=========================== short test summary info ============================
FAILED tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution
1 failed, 16 deselected in 0.17s
== test body
    assert set(schemas.FlagOutput.model_fields) == {"type", "category", "excerpt", "excerpt_b"}
    assert all("objective_negative" not in f["title"] + f["explanation"] for f in F.lexicon_flags(rec(2)))


def test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution():
    """Review T-036 r2 blocker: ADR-013 - source_kind comes from lexicon self_report entries; intake form / EMS / wife do not qualify."""
    from app.backend import grounding as GR
    yes = ["Patient notes prior neck pain.", "Patient links her neck pain to the collision.", "Subjective: neck pain 7/10.",
           "Patient describes neck pain since the collision.", "Patient-reported neck pain 7/10.", "Patient reports prior neck pain.",
           "C/O neck pain 7/10 and headache."]
    no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage."]
    assert all(GR.has_self_report(t) for t in yes) and not any(GR.has_self_report(t) for t in no)

def test_no_template_ends_with_double_period():
    from app.backend import flag_templates as FT
    t, e = FT.render("pre_existing", "pre_existing", provider="P", date="2026-01-02", quote="Cervical ROM full.")
    assert ".”." not in e


def test_pipeline_surfaces_conflict_pass_failure_as_run_warning(tmp_path):
    """Review T-036 r2 major: a failed/missed conflict pass -> warning CONFLICT_PASS_INCOMPLETE, status not 'done', case-level flag."""
    from tests.unit._fakes import run_sample, sample_script
    for exc in (AU.LLMFailed("down"), P.FixtureMiss("none")):
        out, _ = run_sample(tmp_path, call=FakeCall(sample_script(conflicts=exc)))
        assert "CONFLICT_PASS_INCOMPLETE" in [w["code"] for w in out["warnings"]] and out["status"] != "done"
        cx = [f for f in out["flags"] if f["category"] == "analysis_incomplete"]
== grep tests for new T-061 probes
tests/unit/test_flags_pass.py:120:    no = ["Date of accident per intake form: 2026-01-19.", "Per EMS report, neck pain.", "Wife reports he was in pain.", "EMS reports minimal damage."]
== heldout groups
Counter({'quiet_post_accident': 23, 'hedge': 17, 'non_patient_speaker': 14, 'prior_level': 12, 'attribution': 11, 'prior_since_year': 10, 'explicit_patient': 8, 'prior_treatment': 7, 'quiet_hedge': 5, 'headers_not_attribution': 5, 'quiet_self_report': 2, 'self_report': 1})
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:31.959Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-probe.py",
 "content": "\"\"\"T-061 adjuster probe (read-only against the repo). Feeds attribution sentences through:\n  A. the lexicon as written (self_report entries in app/llm/lexicon.yaml, minus self_report_scope.exclude_sentence)\n     -> what the spec/lexicon says should be patient_report;\n  B. the production path grounding.has_self_report() -> what flags.py:46 and flags.py:125 emit as source_kind.\nUsage: .venv/bin/python artifacts/review-evidence/T-061-probe.py <repo_root>\n\"\"\"\nimport re\nimport sys\nfrom pathlib import Path\n\nroot = Path(sys.argv[1]).resolve()\nsys.path.insert(0, str(root))\n\nimport yaml  # noqa: E402\nfrom app.backend import grounding as GR  # noqa: E402\n\nlex = yaml.safe_load((root / \"app/llm/lexicon.yaml\").read_text())\nscope = re.compile(lex[\"self_report_scope\"][\"exclude_sentence\"], re.I)\nself_entries = {e[\"id\"]: re.compile(e[\"pattern\"], re.I) for e in lex[\"entries\"] if e.get(\"self_report\")}\n\nBRIEF = [\n    (\"Patient states pain began after the collision.\", \"patient\"),\n    (\"Wife reports he has been irritable.\", \"record\"),\n    (\"Per EMS, pt ambulatory at scene.\", \"record\"),\n    (\"S: neck pain\", \"record\"),\n    (\"Witness states the car ran the light.\", \"record\"),\n]\nEXTRA = [\n    (\"EMS complains of neck pain 7/10.\", \"record\"),\n    (\"Witness complains of neck pain.\", \"record\"),\n    (\"Wife complains of neck pain.\", \"record\"),\n    (\"Family complains of neck pain.\", \"record\"),\n    (\"EMS reports neck pain 7/10.\", \"record\"),\n    (\"Wife reports he was in pain.\", \"record\"),\n    (\"S: neck pain 7/10.\", \"record\"),\n    (\"Self-reported neck pain 7/10.\", \"record\"),\n    (\"Subjective: neck pain 7/10.\", \"record\"),\n    (\"Patient-reported neck pain 7/10.\", \"patient\"),\n    (\"Patient complains of neck pain.\", \"patient\"),\n    (\"C/O neck pain 7/10 and headache.\", \"patient\"),\n    (\"Patient notes prior neck pain.\", \"patient\"),\n    (\"Date of accident per intake form: 2026-01-19.\", \"record\"),\n]\n\n\ndef lexicon_says(text):\n    ids = []\n    for eid, rx in self_entries.items():\n        for m in rx.finditer(text):\n            if not scope.search(text):\n                ids.append(eid)\n                break\n    return ids\n\n\ndef fmt(b):\n    return \"true \" if b else \"false\"\n\n\nrows = BRIEF + EXTRA\nprint(f\"tree={root}\")\nprint(f\"self_report entries in lexicon: {sorted(self_entries)}\")\nprint(f\"{'expect':8} {'lexicon(scope-aware)':22} {'production has_self_report':27} sentence\")\nmismatch_prod = []\nmismatch_lex = []\nfor text, expect in rows:\n    lx_ids = lexicon_says(text)\n    lx_patient = bool(lx_ids)\n    prod = GR.has_self_report(text)\n    if (expect == \"patient\") != prod:\n        mismatch_prod.append(text)\n    if (expect == \"patient\") != lx_patient:\n        mismatch_lex.append(text)\n    print(f\"{expect:8} {('patient_report ' + ','.join(lx_ids)) if lx_patient else 'record':22} \"\n          f\"{'patient_report' if prod else 'record':27} {text!r}\"\n          + (\"  <-- prod DISAGREES\" if (expect == 'patient') != prod else \"\")\n          + (\"  <-- lexicon DISAGREES\" if (expect == 'patient') != lx_patient else \"\"))\nprint(f\"production mismatches: {len(mismatch_prod)}\")\nfor t in mismatch_prod:\n    print(f\"  PROD  {t!r}\")\nprint(f\"lexicon(scope-aware) mismatches: {len(mismatch_lex)}\")\nfor t in mismatch_lex:\n    print(f\"  LEX   {t!r}\")\nprint(\"flags.py references to grounding.has_self_report:\")\nimport subprocess  # noqa: E402\nout = subprocess.run([\"grep\", \"-n\", \"has_self_report\\\\|self_report_scope\\\\|exclude_sentence\", str(root / \"app/backend/flags.py\"),\n                      str(root / \"app/backend/grounding.py\")], capture_output=True, text=True).stdout\nprint(out.rstrip())\n"
}
````

### User / tool · 2026-11-02T02:15:32.063Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-probe.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:32.456Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-061-probe.py /Users/arsis/zlayt-pm-project 2>&1",
 "description": "Run T-061 attribution probe on the live tree"
}
````

### User / tool · 2026-11-02T02:15:32.775Z

**tool result**
````
tree=/Users/arsis/zlayt-pm-project
self_report entries in lexicon: ['patient_attributes_causation', 'patient_reports_generic', 'self_reported_prior']
expect   lexicon(scope-aware)   production has_self_report  sentence
patient  patient_report patient_attributes_causation,patient_reports_generic patient_report              'Patient states pain began after the collision.'
record   record                 record                      'Wife reports he has been irritable.'
record   record                 record                      'Per EMS, pt ambulatory at scene.'
record   record                 record                      'S: neck pain'
record   record                 record                      'Witness states the car ran the light.'
record   record                 patient_report              'EMS complains of neck pain 7/10.'  <-- prod DISAGREES
record   record                 patient_report              'Witness complains of neck pain.'  <-- prod DISAGREES
record   record                 patient_report              'Wife complains of neck pain.'  <-- prod DISAGREES
record   record                 patient_report              'Family complains of neck pain.'  <-- prod DISAGREES
record   record                 record                      'EMS reports neck pain 7/10.'
record   record                 record                      'Wife reports he was in pain.'
record   record                 record                      'S: neck pain 7/10.'
record   record                 record                      'Self-reported neck pain 7/10.'
record   record                 record                      'Subjective: neck pain 7/10.'
patient  patient_report patient_reports_generic patient_report              'Patient-reported neck pain 7/10.'
patient  patient_report patient_reports_generic patient_report              'Patient complains of neck pain.'
patient  patient_report patient_reports_generic patient_report              'C/O neck pain 7/10 and headache.'
patient  patient_report self_reported_prior,patient_reports_generic patient_report              'Patient notes prior neck pain.'
record   record                 record                      'Date of accident per intake form: 2026-01-19.'
production mismatches: 4
  PROD  'EMS complains of neck pain 7/10.'
  PROD  'Witness complains of neck pain.'
  PROD  'Wife complains of neck pain.'
  PROD  'Family complains of neck pain.'
lexicon(scope-aware) mismatches: 0
flags.py references to grounding.has_self_report:
/Users/arsis/zlayt-pm-project/app/backend/flags.py:46:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
/Users/arsis/zlayt-pm-project/app/backend/flags.py:125:            lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"
/Users/arsis/zlayt-pm-project/app/backend/grounding.py:219:def has_self_report(text: str) -> bool:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:41.228Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-061-base && mkdir -p artifacts/review-evidence/T-061-base && git archive 099732b | tar -x -C artifacts/review-evidence/T-061-base && cd artifacts/review-evidence/T-061-base && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" -p no:cacheprovider 2>&1 | tail -2; echo \"== HEAD full unit (live tree == dd545e3 for reviewed paths)\"; cd /Users/arsis/zlayt-pm-project && .venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -4; echo \"== grounding/flags blob at HEAD:\"; git show dd545e3 --stat -- app/backend | tail -1; echo \"(empty = no backend change in dd545e3)\"",
 "description": "Test pre-commit parent tree and full unit suite on HEAD"
}
````

### User / tool · 2026-11-02T02:15:56.708Z

**tool result**
````
..........................................                               [100%]
114 passed, 697 deselected in 1.69s
== HEAD full unit (live tree == dd545e3 for reviewed paths)
=========================== short test summary info ============================
FAILED tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_09_nonvisit_hides_gap]
2 failed, 811 passed in 12.54s
== grounding/flags blob at HEAD:
(empty = no backend change in dd545e3)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:15:59.850Z

**tool call — Bash**
````
{
 "command": "rm -rf artifacts/review-evidence/T-061-head && mkdir -p artifacts/review-evidence/T-061-head && git archive dd545e3 | tar -x -C artifacts/review-evidence/T-061-head && for d in T-061-base T-061-head; do echo \"== $d full unit\"; (cd artifacts/review-evidence/$d && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | tail -4); done",
 "description": "Run full unit suite on parent and HEAD archives"
}
````

### User / tool · 2026-11-02T02:16:25.888Z

**tool result**
````
== T-061-base full unit
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[sample]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_01_date_formats]
FAILED tests/unit/test_t037_backend.py::test_sample_replay_shows_verified_entries
3 failed, 808 passed in 12.35s
== T-061-head full unit
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[sample]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_01_date_formats]
FAILED tests/unit/test_t037_backend.py::test_sample_replay_shows_verified_entries
4 failed, 807 passed in 12.38s
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:16:29.740Z

**tool call — Bash**
````
{
 "command": "for d in T-061-base T-061-head; do (cd artifacts/review-evidence/$d && /Users/arsis/zlayt-pm-project/.venv/bin/python -m pytest tests/unit -q -p no:cacheprovider 2>&1 | grep \"^FAILED\" | sort > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-$d-failed.txt); done; echo \"== base failures\"; cat artifacts/review-evidence/T-061-T-061-base-failed.txt 2>/dev/null || cat artifacts/review-evidence/T-061-T-061-base-failed.txt; echo \"== diff base vs head\"; diff artifacts/review-evidence/T-061-T-061-base-failed.txt artifacts/review-evidence/T-061-T-061-head-failed.txt",
 "description": "Compare failing test lists between parent and HEAD archives"
}
````

### User / tool · 2026-11-02T02:16:57.221Z

**tool result**
````
== base failures
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[case_01_date_formats]
FAILED tests/unit/test_t037_backend.py::test_replay_has_no_fixture_miss[sample]
FAILED tests/unit/test_t037_backend.py::test_sample_replay_shows_verified_entries
== diff base vs head
0a1
> FAILED tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:12.496Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python - <<'PYEOF'\nfrom pathlib import Path\np = Path(\"artifacts/review-evidence/T-061-probe.py\")\ns = p.read_text()\nold = '    (\"Date of accident per intake form: 2026-01-19.\", \"record\"),\\n]'\nnew = ('    (\"Date of accident per intake form: 2026-01-19.\", \"record\"),\\n'\n       '    (\"Patient links her neck pain to the collision.\", \"patient\"),\\n'\n       '    (\"Patient describes neck pain since the collision.\", \"patient\"),\\n'\n       '    (\"Patient reports prior neck pain.\", \"patient\"),\\n'\n       '    (\"Per EMS report, neck pain.\", \"record\"),\\n'\n       '    (\"EMS reports minimal damage.\", \"record\"),\\n'\n       '    # over-exclusion candidates: patient is the speaker, a family/EMS name appears in the same sentence\\n'\n       '    (\"Patient states EMS noted a laceration.\", \"patient\"),\\n'\n       '    (\"Patient reports his wife said he was fine.\", \"patient\"),\\n]')\nassert s.count(old) == 1\np.write_text(s.replace(old, new))\nprint(\"ok\")\nPYEOF\n.venv/bin/python artifacts/review-evidence/T-061-probe.py /Users/arsis/zlayt-pm-project > artifacts/review-evidence/T-061-probe.txt 2>&1; echo \"EXIT=$?\"; cat artifacts/review-evidence/T-061-probe.txt",
 "description": "Extend probe with test-list and over-exclusion rows; save output"
}
````

### User / tool · 2026-11-02T02:17:12.788Z

**tool result**
````
ok
EXIT=0
tree=/Users/arsis/zlayt-pm-project
self_report entries in lexicon: ['patient_attributes_causation', 'patient_reports_generic', 'self_reported_prior']
expect   lexicon(scope-aware)   production has_self_report  sentence
patient  patient_report patient_attributes_causation,patient_reports_generic patient_report              'Patient states pain began after the collision.'
record   record                 record                      'Wife reports he has been irritable.'
record   record                 record                      'Per EMS, pt ambulatory at scene.'
record   record                 record                      'S: neck pain'
record   record                 record                      'Witness states the car ran the light.'
record   record                 patient_report              'EMS complains of neck pain 7/10.'  <-- prod DISAGREES
record   record                 patient_report              'Witness complains of neck pain.'  <-- prod DISAGREES
record   record                 patient_report              'Wife complains of neck pain.'  <-- prod DISAGREES
record   record                 patient_report              'Family complains of neck pain.'  <-- prod DISAGREES
record   record                 record                      'EMS reports neck pain 7/10.'
record   record                 record                      'Wife reports he was in pain.'
record   record                 record                      'S: neck pain 7/10.'
record   record                 record                      'Self-reported neck pain 7/10.'
record   record                 record                      'Subjective: neck pain 7/10.'
patient  patient_report patient_reports_generic patient_report              'Patient-reported neck pain 7/10.'
patient  patient_report patient_reports_generic patient_report              'Patient complains of neck pain.'
patient  patient_report patient_reports_generic patient_report              'C/O neck pain 7/10 and headache.'
patient  patient_report self_reported_prior,patient_reports_generic patient_report              'Patient notes prior neck pain.'
record   record                 record                      'Date of accident per intake form: 2026-01-19.'
patient  patient_report patient_attributes_causation patient_report              'Patient links her neck pain to the collision.'
patient  patient_report patient_reports_generic patient_report              'Patient describes neck pain since the collision.'
patient  patient_report self_reported_prior,patient_reports_generic patient_report              'Patient reports prior neck pain.'
record   record                 record                      'Per EMS report, neck pain.'
record   record                 record                      'EMS reports minimal damage.'
patient  record                 patient_report              'Patient states EMS noted a laceration.'  <-- lexicon DISAGREES
patient  record                 patient_report              'Patient reports his wife said he was fine.'  <-- lexicon DISAGREES
production mismatches: 4
  PROD  'EMS complains of neck pain 7/10.'
  PROD  'Witness complains of neck pain.'
  PROD  'Wife complains of neck pain.'
  PROD  'Family complains of neck pain.'
lexicon(scope-aware) mismatches: 2
  LEX   'Patient states EMS noted a laceration.'
  LEX   'Patient reports his wife said he was fine.'
flags.py references to grounding.has_self_report:
/Users/arsis/zlayt-pm-project/app/backend/flags.py:46:         "source_kind": "patient_report" if grounding.has_self_report(excerpt) else "record",
/Users/arsis/zlayt-pm-project/app/backend/flags.py:125:            lx["source_kind"] = "patient_report" if grounding.has_self_report(lx["excerpt"]) else "record"
/Users/arsis/zlayt-pm-project/app/backend/grounding.py:219:def has_self_report(text: str) -> bool:
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:41.156Z

**tool call — Bash**
````
{
 "command": "echo \"== held-out rows: patient-subject sentences containing a family/EMS word\"; grep -i '\"text\"' evals/lexicon_heldout.jsonl | grep -i \"patient\\|pt \" | grep -i \"EMS\\|wife\\|witness\\|family\\|spouse\\|husband\" ; echo \"(end)\"; echo \"== exclude examples keep list\"; grep -n \"keep:\" app/llm/lexicon.yaml; echo \"== production exclude_sentence usage\"; grep -rn \"exclude_sentence\\|self_report_scope\" app/ tests/ | head; echo \"(end)\"; rm -rf artifacts/review-evidence/T-061-base artifacts/review-evidence/T-061-head && mv artifacts/review-evidence/T-061-T-061-base-failed.txt artifacts/review-evidence/T-061-base-failed.txt && mv artifacts/review-evidence/T-061-T-061-head-failed.txt artifacts/review-evidence/T-061-head-failed.txt && ls artifacts/review-evidence/ | grep T-061",
 "description": "Check held-out coverage gap and clean up extracted trees"
}
````

### User / tool · 2026-11-02T02:17:41.430Z

**tool result**
````
== held-out rows: patient-subject sentences containing a family/EMS word
{"id": "H-041", "split": "dev", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Husband states she struck her head on the side window."}
{"id": "H-080", "split": "fresh", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Husband says she believes the accident caused the numbness."}
{"id": "H-099", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "EMS reports neck pain 7/10."}
{"id": "H-100", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Witness states the sedan was stopped at the light."}
{"id": "H-101", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Wife reports he hit his head on the wheel."}
{"id": "H-102", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Husband states she complains of headaches every night."}
{"id": "H-103", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Family says she has been sleeping poorly."}
{"id": "H-106", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Witness complains of neck pain."}
{"id": "H-107", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Wife complains of neck pain."}
{"id": "H-108", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "EMS complains of neck pain 7/10."}
{"id": "H-109", "split": "t061", "group": "non_patient_speaker", "expect": "quiet_self_report", "accident_year": 2026, "text": "Per his wife, headaches began at the scene."}
(end)
== exclude examples keep list
93:    keep: ['Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.']
== production exclude_sentence usage
app/llm/lexicon.yaml:85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
app/llm/lexicon.yaml:88:self_report_scope:
app/llm/lexicon.yaml:89:  exclude_sentence: '\b(?:EMS|paramedics?|witness(?:es)?|bystanders?|wife|husband|spouse|mother|father|parents?|family|friends?|relatives?|daughter|son|sibling|caregiver|police|officer|nurse|staff)\b(?:\s+[\w''-]+){0,3}?\s+(?:reports?|reported|states?|stated|says|said|complains?|complained|c/o|describes?|described|notes?|noted|relates?|believes?|attributes?|links?|thinks?|claims?)\b|\bper\s+(?:the\s+|his\s+|her\s+)?(?:wife|husband|spouse|family|witness|EMS|mother|father)\b'
app/llm/lexicon.yaml:764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
(end)
T-061-base-failed.txt
T-061-head-failed.txt
T-061-probe.py
T-061-probe.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:17:50.142Z

**tool call — Bash**
````
{
 "command": "grep -n \"^_SELF\\|^_NOT_PATIENT_STATEMENT\\|^_PATIENT_WORDS\\|^def _self_report\\|^def has_self_report\" app/backend/grounding.py; grep -n \"^- id: intake_form_accident_date\" -A12 app/llm/lexicon.yaml | grep \"self_report\"; grep -n \"self_report_scope\" app/llm/lexicon.yaml; grep -n \"source_kind = \\\"patient_report\\\" is set by code\" memory/DECISIONS.md; grep -n \"code sets source_kind\" app/llm/lexicon.yaml; grep -n \"^| D-033\" memory/ORCHESTRATOR_DECISIONS.md | cut -c1-60",
 "description": "Get exact line numbers for citations"
}
````

### User / tool · 2026-11-02T02:17:50.283Z

**tool result**
````
167:_SELF = re.compile(r"\bc/o\b|\bcomplain(?:s|ed|ing|t)?\b|\b(?:patient|pt\.?|he|she|client)\s+(?:states?|stated|reports?|reported|endorses|admits|"
175:_NOT_PATIENT_STATEMENT = {"intake_form_accident_date"}
177:_PATIENT_WORDS = re.compile(r"\b(?:patient|pt|he|she|client|c/o|complain\w*|subjective)\b|patient-reported", re.IGNORECASE)
180:def _self_report(text: str) -> bool:
219:def has_self_report(text: str) -> bool:
775-  self_report: false
780-  false_positive: 'Round 2 split this from the generic "per patient" marker, which is now low (self_report). T-061: self_report is false here because an intake form is a document, not the patient''s statement; source_kind stays "record". "Date of injury per patient" is still caught by patient_reports_generic. "Per protocol" does not match.'
85:# when the hit's sentence matches `self_report_scope.exclude_sentence` (a named non-patient speaker with a speech verb, or
88:self_report_scope:
764:  false_positive: 'Fires on most history lines. LOW: it never raises a flag alone. T-061: it does NOT match a bare "S:" / "Subjective:" header or "Self-reported" (a section label is not an attribution), and a sentence whose speaker is EMS, a witness, a spouse or family is excluded by self_report_scope. "C/O" and "complains of" with no named speaker are read as the patient, which is the clinical convention.'
84:# T-061: a self_report hit is a PATIENT statement only. Before the code sets source_kind = patient_report, it must drop the hit
41:| D-033 | `patient_report` (self-report chip) applies onl
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:31.012Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster.md",
 "content": "# T-061 Self-report label precision: claims-adjuster review (Gary Pruitt), round 0\n\nVerdict: **fail** (1 blocker, 2 major, 1 minor).\n\nWhat the commit does: dd545e3 narrows the lexicon `self_report` entries to explicit patient attribution, adds a `self_report_scope.exclude_sentence` regex (lexicon.yaml:88-93), marks `intake_form_accident_date` `self_report: false`, and adds 26 held-out probes. The lexicon side holds up. The product side does not: no file under `app/backend/` changed in dd545e3, so AC2 (flags.py/grounding.py label only from those entries, with tests) is not done, and the production label still attributes EMS, witness, wife and family complaints to the patient.\n\nChecks against the card and D-033:\n\n- AC1 (lexicon): the selfcheck passes and the scope-aware lexicon gets the brief's five sentences right. Two over-exclusion cases remain (finding 2).\n- AC2 (flags.py/grounding.py + tests): **not done.** `git show --stat dd545e3` lists only `app/llm/lexicon.yaml`, `evals/lexicon_heldout.jsonl` and `research/lexicon_selfcheck.py`. Production still calls `grounding.has_self_report` (flags.py:46 and flags.py:125), which still uses the old `_SELF` complain verb (grounding.py:167) and the `_PATIENT_WORDS` word filter (grounding.py:177). `exclude_sentence` is referenced nowhere in `app/` or `tests/`.\n- AC3 (spec note or D-entry): D-033 exists (ORCHESTRATOR_DECISIONS.md:41), which meets the \"or\" clause. DECISIONS.md:286 and lexicon.yaml:25-26 still state the superseded rule (finding 3).\n- Brief sentences: \"Patient states pain began after the collision.\" is patient_report in the lexicon and in production. \"Wife reports he has been irritable.\", \"Per EMS, pt ambulatory at scene.\", \"S: neck pain\" and \"Witness states the car ran the light.\" are record in both. No sentence I fed was invented or altered.\n\nWhy finding 1 is a blocker when T-036 r3 rated the same behaviour major: D-033 now names this case as a credibility error (\"Mislabelling a family member's statement as the patient's own is a credibility error an adjuster would exploit\"). At r3 there was no such decision. The production code contradicts a recorded decision, so it is a spec violation.\n\nFindings:\n\n1. **Blocker.** AC2 not done: production still labels EMS, witness, wife and family complaints as \"Patient self-report\". Evidence: `artifacts/review-evidence/T-061-probe.txt`, rows \"EMS complains of neck pain 7/10.\", \"Witness complains of neck pain.\", \"Wife complains of neck pain.\", \"Family complains of neck pain.\" each show `production has_self_report: patient_report` and `lexicon(scope-aware): record`. Cause: grounding.py:167 `\\bcomplain(?:s|ed|ing|t)?\\b` in `_SELF`, and grounding.py:177 `complain\\w*` in `_PATIENT_WORDS`. flags.py:46 and flags.py:125 use the result as `source_kind`. `git show --stat dd545e3` has no app/backend entry. Card AC2 is `done: false`.\n   Why it matters: the chip \"Patient self-report\" tells the reader the claimant said it. A family member's or EMS's statement carries the claimant's name on it, and I would use that to discount the package.\n   Fix: in grounding.has_self_report, replace `_SELF` and `_PATIENT_WORDS` with \"any lexicon self_report hit AND NOT self_report_scope.exclude_sentence\" (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Set the intake date through `self_report: false` and delete `_NOT_PATIENT_STATEMENT` (grounding.py:175). Fix finding 2 in the same change.\n   Acceptance test: has_self_report is False for \"EMS complains of neck pain 7/10.\", \"Witness complains of neck pain.\", \"Wife complains of neck pain.\", \"Family complains of neck pain.\", \"EMS reports neck pain 7/10.\", \"Wife reports he was in pain.\", \"Date of accident per intake form: 2026-01-19.\"; True for \"Patient states pain began after the collision.\", \"Patient complains of neck pain.\", \"C/O neck pain 7/10 and headache.\", \"Patient-reported neck pain 7/10.\"; and `grep -n \"_SELF\\|_PATIENT_WORDS\\|_NOT_PATIENT_STATEMENT\" app/backend/grounding.py` returns nothing.\n\n2. **Major.** The commit leaves `tests/unit/test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution` red, a regression from the parent. Evidence: `.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2` on the live tree (equal to dd545e3 for these paths) gives `1 failed, 113 passed, 699 deselected`. On the git archive of parent 099732b the same command gives `114 passed, 697 deselected`. The full suite diff (`artifacts/review-evidence/T-061-base-failed.txt` vs `T-061-head-failed.txt`) adds exactly this test. The failing assertion is the yes-list entry \"Subjective: neck pain 7/10.\", which the lexicon no longer matches (lexicon.yaml:754-759, pattern now without `^\\s*(?:subjective|S)\\s*:`). The test is the r2 contract, which D-033 supersedes for bare S:/Subjective: headers. The card's evidence line (\"selfcheck PASS ... golden MUST 11/11\") does not mention a pytest run, so the red test was not reported.\n   Why it matters: a red flag test on the commit means the worker did not run the suite it touched, and the stale test would hide a regression in the next round.\n   Fix: update the test to D-033 (Subjective: and S: are record; a bare header is not an attribution) and add the AC2 tests from finding 1 to tests/unit/test_flags_pass.py.\n   Acceptance test: `.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\"` reports 0 failed, and the full `tests/unit` run shows no FAILED line that is not also in the parent archive.\n\n3. **Major.** `exclude_sentence` drops explicit patient statements whenever a family or EMS word and a speech verb share the sentence. Evidence: `artifacts/review-evidence/T-061-probe.txt`, \"Patient states EMS noted a laceration.\" and \"Patient reports his wife said he was fine.\" both give lexicon `record` (`LEX` mismatch) while the patient is the speaker. Cause: lexicon.yaml:89 matches `\\b(?:EMS|...|wife|...)\\b(?:\\s+[\\w'-]+){0,3}?\\s+(?:...|noted|said|...)\\b` anywhere in the sentence, not only at the grammatical subject. Held-out coverage gap: none of the 26 new probes pairs a patient subject with a family or EMS word (grep of evals/lexicon_heldout.jsonl), so selfcheck PASS cannot show it.\n   Why it matters: a patient-attributed statement loses its \"Patient self-report\" attribution (D-033: \"patient-quoted speech\" stays patient_report). This is latent today because production does not read exclude_sentence yet. Finding 1's fix would make it live.\n   Fix: anchor the exclusion to the sentence subject (sentence-initial \"EMS/Wife/Witness/Family ... <verb>\", or a \"Per <non-patient>\" clause), and exclude any sentence that starts with or names \"Patient\"/\"Pt\"/\"C/O\". Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.\n   Acceptance test: \"Patient states EMS noted a laceration.\", \"Patient reports his wife said he was fine.\" are patient_report; \"EMS reports minimal damage.\", \"Wife complains of neck pain.\", \"Per his wife, headaches began at the scene.\" stay record; `research/lexicon_selfcheck.py` still PASS.\n\n4. **Minor.** The spec still states the superseded rule. DECISIONS.md:286 still says \"`source_kind = \"patient_report\"` is set by code from the lexicon `self_report` entries on the excerpt\". lexicon.yaml:25-26 still says \"code sets source_kind = \"patient_report\" from it (ADR-013)\" (the header was edited only on line 25). D-033 says it \"Narrows ADR-013 / DECISIONS.md:286\", so AC3's \"or\" clause is met, but the spec text now contradicts the code's exclusion rule.\n   Fix: architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to \"self_report entries that name the patient, minus self_report_scope.exclude_sentence\". The card's AC3 `done` flag can then be set true.\n   Acceptance test: `grep -n \"set by code from the lexicon\" memory/DECISIONS.md` shows the amended text and no line still reads \"from the lexicon `self_report` entries on the excerpt\".\n\nThings I did not treat as findings, for Chris:\n- D-033 labels a bare \"S:\" or \"Subjective:\" header as record. In a SOAP note that header is the clinician's marker for the patient's report. The verbatim marker stays in the excerpt, so nothing is invented. I accept D-033 as the decision, and I note the adjuster would give subjective-only weight to these lines.\n\nExercised (live tree; `git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit` shows only evals/reports/latest.json, outside my scope, so live == dd545e3 for reviewed paths):\n- Read personas/claims-adjuster.md in full; `python3 tools/board.py show T-061`; `grep -n \"D-033\" -A 15 memory/ORCHESTRATOR_DECISIONS.md`; reviews/T-036-claims-adjuster-r3.md; my memory dir.\n- `git log --oneline -5`; `git show --stat dd545e3`; `git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py` (diff read in full).\n- `.venv/bin/python research/lexicon_selfcheck.py` -> `RESULT: PASS`, golden MUST 11/11, held-out 115/115, adjuster probes 62/63 (the one FN, \"No acute findings.\" low only, is pre-existing), EXIT=0.\n- `.venv/bin/python -m pytest tests/unit -q -k \"flag or lexicon\" 2>&1 | tail -2` -> `1 failed, 113 passed, 699 deselected`; full failure text read (`pytest ... -k lexicon_self_report` -> 1 failed, assertion at tests/unit/test_flags_pass.py:121).\n- Same subset on `git archive 099732b` (parent) -> `114 passed, 697 deselected`.\n- Full `tests/unit` on live tree -> `2 failed, 811 passed` (flags test plus test_t037_backend.py::test_replay_has_no_fixture_miss[case_09_nonvisit_hides_gap]); on archives: parent `3 failed, 808 passed`, dd545e3 `4 failed, 807 passed`; the failing-test lists differ only by the flags test. The three test_t037 replay failures exist at parent and are not attributable to dd545e3; the live tree and archives disagree on case_09, which I did not triage.\n- `artifacts/review-evidence/T-061-probe.py /Users/arsis/zlayt-pm-project` -> `artifacts/review-evidence/T-061-probe.txt`: 27 sentences (the five brief sentences, the researcher's test list, EMS/witness/wife/family complaints, S:/Subjective:/Self-reported headers, two over-exclusion candidates) through the lexicon (scope-aware) and `grounding.has_self_report`.\n- `grep -n \"has_self_report\\|self_report_scope\\|exclude_sentence\" app/backend/flags.py app/backend/grounding.py` -> flags.py:46, flags.py:125, grounding.py:219 only; `grep -rn \"exclude_sentence\\|self_report_scope\" app/ tests/` -> lexicon.yaml only.\n- `grep -n \"^_SELF\\|^_NOT_PATIENT_STATEMENT\\|^_PATIENT_WORDS\" app/backend/grounding.py` -> 167, 175, 177.\n- `grep` of evals/lexicon_heldout.jsonl for patient subjects with family/EMS words -> none (coverage gap, finding 3).\n- `git archive` extractions were deleted after use; the failing-test lists are kept as artifacts.\n\nOutside my lens: the test-runner setup and the t037 replay failures (not triaged); the commit message's co-author line.\n\n```json\n{\"card\": \"T-061\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-haiku-5-5\",\n \"scope\": \"commit dd545e3 (HEAD; parent 099732b) on the live tree (equal to dd545e3 for app/backend, app/llm/lexicon.yaml, research, evals, tests/unit); spec memory/DECISIONS.md:286; decision memory/ORCHESTRATOR_DECISIONS.md D-033; no app URL (lexicon and flag-layer change, no UI in scope); sample probes as listed.\",\n \"exercised\": [\n  \"Read personas/claims-adjuster.md in full; python3 tools/board.py show T-061; D-033 (ORCHESTRATOR_DECISIONS.md:41); reviews/T-036-claims-adjuster-r3.md; my memory dir\",\n  \"git log --oneline -5; git show --stat dd545e3 (lexicon.yaml, lexicon_heldout.jsonl, lexicon_selfcheck.py only; no app/backend)\",\n  \"git show dd545e3 -- app/llm/lexicon.yaml research/lexicon_selfcheck.py (full diff read)\",\n  \"git diff --stat HEAD -- app/backend app/llm/lexicon.yaml research evals tests/unit (only evals/reports/latest.json, out of scope)\",\n  \".venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS; golden MUST 11/11; held-out 115/115; EXIT=0\",\n  \".venv/bin/python -m pytest tests/unit -q -k 'flag or lexicon' 2>&1 | tail -2 -> 1 failed, 113 passed, 699 deselected\",\n  \"same subset on git archive 099732b (parent) -> 114 passed, 697 deselected\",\n  \"full tests/unit: live 2 failed/811 passed; parent archive 3 failed/808 passed; dd545e3 archive 4 failed/807 passed; FAILED-list diff = test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution only (artifacts/review-evidence/T-061-base-failed.txt, T-061-head-failed.txt)\",\n  \"artifacts/review-evidence/T-061-probe.py <repo> -> artifacts/review-evidence/T-061-probe.txt (27 sentences through lexicon scope-aware and grounding.has_self_report)\",\n  \"grep -n has_self_report|self_report_scope|exclude_sentence app/backend/flags.py app/backend/grounding.py -> flags.py:46, 125; grounding.py:219; grep -rn exclude_sentence app/ tests/ -> lexicon.yaml only\",\n  \"grep -n ^_SELF|^_NOT_PATIENT_STATEMENT|^_PATIENT_WORDS app/backend/grounding.py -> 167, 175, 177\",\n  \"grep evals/lexicon_heldout.jsonl for patient-subject sentences containing EMS/wife/witness/family -> none\",\n  \"sed -n 284,288p memory/DECISIONS.md (line 286 text); grep self_report_scope / lexicon header lines 13, 25-26\"\n ],\n \"verdict\": \"fail\",\n \"scores\": {\"attribution_precision_production\": 1, \"lexicon_scope_logic\": 3, \"ac2_flags_wiring\": 1, \"test_honesty\": 2, \"spec_consistency\": 3, \"no_invented_or_altered_text\": 5},\n \"findings\": [\n  {\"severity\": \"blocker\",\n   \"title\": \"AC2 not done: production still labels EMS, witness, wife and family complaints as Patient self-report\",\n   \"evidence\": \"artifacts/review-evidence/T-061-probe.txt rows 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.': production has_self_report=patient_report, lexicon(scope-aware)=record. Cause: app/backend/grounding.py:167 (_SELF, complain verb) and grounding.py:177 (_PATIENT_WORDS, complain\\\\w*); flags.py:46 and flags.py:125 use the result as source_kind. git show --stat dd545e3 touches no app/backend file. Card AC2 done=false.\",\n   \"why_it_matters\": \"D-033 (ORCHESTRATOR_DECISIONS.md:41) says EMS, witness and spouse/family statements are not patient self-report and calls the mislabel a credibility error. Production contradicts that recorded decision on four live phrasings, and the chip tells the reader the claimant said it. T-036 r3 rated the same behaviour major; D-033 now makes it a spec violation, so it is a blocker.\",\n   \"fix\": \"In grounding.has_self_report: replace _SELF and _PATIENT_WORDS with 'any lexicon self_report hit AND NOT self_report_scope.exclude_sentence' (read from lexicon.yaml, as research/lexicon_selfcheck.py:is_patient_statement does). Mark the intake date self_report false (done in lexicon) and delete _NOT_PATIENT_STATEMENT (grounding.py:175). Fix finding 3 in the same change.\",\n   \"acceptance_test\": \"has_self_report False for 'EMS complains of neck pain 7/10.', 'Witness complains of neck pain.', 'Wife complains of neck pain.', 'Family complains of neck pain.', 'EMS reports neck pain 7/10.', 'Wife reports he was in pain.', 'Date of accident per intake form: 2026-01-19.'; True for 'Patient states pain began after the collision.', 'Patient complains of neck pain.', 'C/O neck pain 7/10 and headache.', 'Patient-reported neck pain 7/10.'; grep -n '_SELF\\\\|_PATIENT_WORDS\\\\|_NOT_PATIENT_STATEMENT' app/backend/grounding.py returns nothing.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Commit leaves test_flags_pass.py red (regression from parent): stale r2 assertion on 'Subjective:' header\",\n   \"evidence\": \"'.venv/bin/python -m pytest tests/unit -q -k \\\"flag or lexicon\\\" 2>&1 | tail -2' -> '1 failed, 113 passed, 699 deselected' (live, equal to dd545e3). Same subset on git archive 099732b -> '114 passed, 697 deselected'. Failing test tests/unit/test_flags_pass.py:114-121, assertion at :121, yes-list entry 'Subjective: neck pain 7/10.' (probe row: record). Full-suite FAILED-list diff against parent: only this test (artifacts/review-evidence/T-061-base-failed.txt vs T-061-head-failed.txt). Card evidence line does not mention a pytest run.\",\n   \"why_it_matters\": \"The lexicon change flipped a tested behaviour and the test was not updated, so the commit is red on the flag suite it touches. The stale assertion would hide the next regression. The card's evidence cites only selfcheck and golden runs.\",\n   \"fix\": \"Update the yes/no lists in test_flags_pass.py to D-033 (bare Subjective:/S: header is record; Patient-reported stays patient) and add the AC2 tests from finding 1 in the same file. Report the pytest subset result in the card evidence.\",\n   \"acceptance_test\": \"'.venv/bin/python -m pytest tests/unit -q -k \\\"flag or lexicon\\\"' reports 0 failed; the full tests/unit FAILED list contains no test that is absent from the parent archive.\"},\n  {\"severity\": \"major\",\n   \"title\": \"exclude_sentence drops explicit patient statements when a family or EMS word and a speech verb share the sentence\",\n   \"evidence\": \"artifacts/review-evidence/T-061-probe.txt: 'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' -> lexicon(scope-aware)=record (expect patient). Cause: app/llm/lexicon.yaml:89 exclude_sentence matches a non-patient name, up to 3 words, then a speech verb anywhere in the sentence (not at the grammatical subject). evals/lexicon_heldout.jsonl: no probe pairs a patient subject with a family/EMS word (grep).\",\n   \"why_it_matters\": \"D-033 keeps patient-quoted speech as patient_report. The exclusion removes the patient's own attribution on a sentence the patient authored. It is latent today because production does not read exclude_sentence, and it becomes live when AC2 is fixed as finding 1 requires. Selfcheck PASS cannot show it because the held-out set has no such case.\",\n   \"fix\": \"Anchor the exclusion to the sentence subject (sentence-initial 'EMS|Wife|Witness|Family ... <verb>' or a 'Per <non-patient>' clause) and never exclude a sentence that starts with or names Patient/Pt/C/O. Add both sentences to self_report_scope.examples.keep and to evals/lexicon_heldout.jsonl.\",\n   \"acceptance_test\": \"'Patient states EMS noted a laceration.' and 'Patient reports his wife said he was fine.' are patient_report; 'EMS reports minimal damage.', 'Wife complains of neck pain.', 'Per his wife, headaches began at the scene.' stay record; .venv/bin/python research/lexicon_selfcheck.py still PASS.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Spec text still states the superseded rule (DECISIONS.md:286, lexicon.yaml:25-26)\",\n   \"evidence\": \"memory/DECISIONS.md:286: '`source_kind = \\\"patient_report\\\"` is set by code from the lexicon `self_report` entries on the excerpt'. app/llm/lexicon.yaml:25-26: 'code sets source_kind = \\\"patient_report\\\" from it (ADR-013)'. D-033 (ORCHESTRATOR_DECISIONS.md:41) says it 'Narrows ADR-013 / DECISIONS.md:286'.\",\n   \"why_it_matters\": \"AC3's 'or' clause is met by D-033, but the contract text now omits the exclusion rule that the code applies. A future reader gets two rules.\",\n   \"fix\": \"Architect note amends DECISIONS.md:286 and lexicon.yaml:25-26 to 'self_report entries that name the patient, minus self_report_scope.exclude_sentence'. Then set card AC3 done.\",\n   \"acceptance_test\": \"grep -n 'set by code from the lexicon' memory/DECISIONS.md shows the amended text; the header in lexicon.yaml:25-26 names self_report_scope.\"}\n ],\n \"whats_right\": [\n  \"Lexicon scope works on the brief's non-patient sentences: 'Wife reports he has been irritable.', 'Per EMS, pt ambulatory at scene.', 'Witness states the car ran the light.' and 'S: neck pain' are record, and 'Patient states pain began after the collision.' is patient_report in both lexicon and production.\",\n  \"Intake date is self_report: false (lexicon.yaml:775) and production gives record for 'Date of accident per intake form: 2026-01-19.'; no excerpt text is altered in any probe.\",\n  \"Selfcheck, held-out 115/115 and golden MUST 11/11 all pass on the commit.\"\n ],\n \"questions_for_chris\": [\n  \"D-033 makes a bare 'S:' or 'Subjective:' header record, not patient self-report. In a SOAP note that header marks the patient's report. I accept D-033, but confirm you want the chip off those lines, since the subjective-only weight they carry is what a defense adjuster would use.\",\n  \"Is 'Patient-reported' an explicit patient attribution for D-033? I counted it as patient_report (production and lexicon agree); D-033 does not name it.\",\n  \"The persona file expects model claude-opus-5-5 in the review record; I ran as claude-haiku-5-5 and wrote that id. Confirm that is acceptable for the gate.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T02:18:31.160Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:34.823Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python -c \"\nimport json,re\ns=open('reviews/T-061-claims-adjuster.md').read()\nm=re.search(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`', s, re.S)\nd=json.loads(m.group(1))\nprint('json ok', d['verdict'], [f['severity'] for f in d['findings']])\n\" ; grep -n \"^- id: patient_reports_generic\" app/llm/lexicon.yaml; grep -n \"^  pattern: '\\\\\\\\b(?:patient|pt\" app/llm/lexicon.yaml | cut -c1-40; python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate review JSON, confirm lexicon line refs, run board validate"
}
````

### User / tool · 2026-11-02T02:18:34.881Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: board-guard error (Deny: could not parse command safely (No escaped character)); denying to fail closed
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:36.994Z

**tool call — Bash**
````
{
 "command": ".venv/bin/python artifacts/review-evidence/T-061-check.py 2>/dev/null; cat > /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-061-jsoncheck.py <<'PYEOF'\nimport json, re, sys\ns = open(sys.argv[1]).read()\nm = re.search(r\"```json\\n(.*?)\\n```\", s, re.S)\nd = json.loads(m.group(1))\nprint(\"json ok\", d[\"verdict\"], [f[\"severity\"] for f in d[\"findings\"]])\nPYEOF\n.venv/bin/python artifacts/review-evidence/T-061-jsoncheck.py /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster.md; grep -n \"^- id: patient_reports_generic\" app/llm/lexicon.yaml; python3 tools/board.py validate 2>&1 | tail -3",
 "description": "Validate review JSON block and check lexicon line references"
}
````

### User / tool · 2026-11-02T02:18:37.214Z

**tool result**
````
json ok fail ['blocker', 'major', 'major', 'minor']
754:- id: patient_reports_generic
ok (62 file(s))
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:40.716Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md"
}
````

### User / tool · 2026-11-02T02:18:40.723Z

**tool result**
````
1	---
2	name: flag-source-kind-and-run-signal
3	description: T-036 source_kind history: r2 (cd4bc60) dropped the lexicon self_report contract; r3 (3f37141) restored it via a word filter that still misses "S:"/"Self-reported" and lets "complains" subjects through; spec never amended
4	metadata:
5	  type: project
6	---
7	
8	Round 2 (cd4bc60) fixed the intake-date mislabel by deleting the lexicon `self_report` contribution from `grounding._self_report` for every entry. Spec (memory/DECISIONS.md:286) says source_kind is set by code from the lexicon self_report entries. Blocker, r2.
9	
10	Round 3 (3f37141) restored the lexicon contribution, but behind a word filter: `_PATIENT_WORDS` (grounding.py:177) must find patient|pt|he|she|client|c/o|complain|subjective|patient-reported in the matched text, and `intake_form_accident_date` is skipped by name (grounding.py:175). Result on the commit:
11	- Still wrong: "S: neck pain 7/10." and "Self-reported neck pain 7/10." (lexicon.yaml:744 matches; code says record). Blocker, r3.
12	- Over-attributed: "EMS / Witness / Wife / Family complains of ..." give patient_report, because `complain` is in `_SELF` (grounding.py:167) and `_PATIENT_WORDS`. Major, r3.
13	- Spec not amended: DECISIONS.md:286 and lexicon.yaml:25-26 unchanged in the commit; 8 lexicon-matched excerpts disagree with code. Major, r3.
14	- Record 7 intake date stays `record` (good); record 3 and 9 stay `patient_report` (good).
15	
16	**Why:** each round narrows a classifier to fix the one named example, then the narrowing misses an adjacent lexicon form. The r2 fix was to remove the mechanism; the r3 fix added a word whitelist that the lexicon's own patterns do not match.
17	
18	**How to apply:** when source_kind or any label is touched, probe every lexicon self_report entry's examples.hit AND the abbreviations/verbs the pattern lists (S:, self-reported, complains, wife/EMS subjects) through grounding.has_self_report and lexicon_flags. Check whether DECISIONS.md:286 and lexicon.yaml header were amended in the same commit. Evidence for r3: artifacts/review-evidence/T-036-r3-probe.py and T-036-r3-commit-probe.txt. Earlier: T-036-r2-probe*.py.
19	
20	Related: [[feedback_lexicon_review_method]], [[project_flag_pass_review_patterns]], [[feedback_review_commit_not_worktree]].
21	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:40.925Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md"
}
````

### User / tool · 2026-11-02T02:18:40.987Z

**tool result**
````
1	- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions
2	- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 r1-r4: omissions, invented Rivera facts, partial scope fixes (line 34 left open at r4); sweep prose + golden must-not regex
3	- [Flag-pass review patterns](project_flag_pass_review_patterns.md) — T-036 r0: vacuous guard test, silent-empty conflict pass, worker skipped full suite
4	- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2 dropped lexicon self_report; r3 word filter misses "S:"/"Self-reported", complains-subjects pass; spec unamended
5	- [Review the commit, not the dirty tree](feedback_review_commit_not_worktree.md) — git archive the sha when working tree has uncommitted edits to reviewed files
6	- [T-036 r4 split and judge fixtures](project_t036_r4_split_and_judge_fixtures.md) — self-report split to T-061; committed judge fixtures don't replay (JUDGE_UNAVAILABLE); r4 verdict changes
7	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:48.902Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md",
 "content": "---\nname: flag-source-kind-and-run-signal\ndescription: source_kind history for self-report labels: T-036 r2/r3 (word filter, spec unamended) then T-061 r0 (dd545e3) narrowed the lexicon but left flags/grounding wiring (AC2) undone and the exclusion regex over-broad\nmetadata:\n  type: project\n---\n\nRound 2 (cd4bc60) fixed the intake-date mislabel by deleting the lexicon `self_report` contribution from `grounding._self_report` for every entry. Spec (memory/DECISIONS.md:286) says source_kind is set by code from the lexicon self_report entries. Blocker, r2.\n\nRound 3 (3f37141) restored the lexicon contribution, but behind a word filter: `_PATIENT_WORDS` (grounding.py:177) must find patient|pt|he|she|client|c/o|complain|subjective|patient-reported in the matched text, and `intake_form_accident_date` is skipped by name (grounding.py:175). Result on the commit:\n- Still wrong: \"S: neck pain 7/10.\" and \"Self-reported neck pain 7/10.\" (lexicon.yaml:744 matches; code says record). Blocker, r3.\n- Over-attributed: \"EMS / Witness / Wife / Family complains of ...\" give patient_report, because `complain` is in `_SELF` (grounding.py:167) and `_PATIENT_WORDS`. Major, r3.\n- Spec not amended: DECISIONS.md:286 and lexicon.yaml:25-26 unchanged in the commit. Major, r3.\n\nT-061 r0 (dd545e3, \"narrow lexicon self_report to explicit patient attribution\"), verdict fail:\n- D-033 (ORCHESTRATOR_DECISIONS.md:41) now decides EMS/witness/spouse/family and bare S:/Subjective: headers are not patient self-report. Lexicon side is right: scope-aware lexicon gives the brief's sentences the right label.\n- AC2 not done: no app/backend file in the commit. Production (flags.py:46, :125 -> grounding.has_self_report) still labels \"EMS/Witness/Wife/Family complains of neck pain 7/10.\" patient_report. Blocker, because D-033 makes it a spec violation (r3 rated the same thing major before D-033 existed).\n- The commit leaves test_flags_pass.py::test_lexicon_self_report_drives_source_kind_with_explicit_patient_attribution red (passes at parent 099732b). Its yes-list still asserts \"Subjective:\" is patient. Major. The card evidence cited selfcheck/golden only.\n- exclude_sentence (lexicon.yaml:89) is not sentence-subject anchored: \"Patient states EMS noted a laceration.\" and \"Patient reports his wife said he was fine.\" come out record. Latent until AC2 wires it. Major. Held-out set has no patient-subject + family/EMS-word probe.\n- Spec text (DECISIONS.md:286, lexicon.yaml:25-26) still states the superseded rule. Minor.\n- Evidence: artifacts/review-evidence/T-061-probe.py and T-061-probe.txt; T-061-base-failed.txt vs T-061-head-failed.txt.\n\n**Why:** each round narrows a classifier to fix the named example, then the narrowing misses an adjacent form or a neighbouring subject. Round r0 of T-061 narrowed the lexicon but not the code path that reads it, and the worker's own probes contained no patient-subject sentence with a family word, so the over-broad exclusion passed.\n\n**How to apply:** when source_kind or any self-report label is touched, (1) diff the commit for app/backend files, not just the lexicon; (2) run the parent-vs-HEAD FAILED list, since a lexicon change flips tested behaviour; (3) probe patient-subject sentences that contain EMS/wife/witness/family words; (4) check whether DECISIONS.md:286 and the lexicon header were amended. Related: [[feedback_lexicon_review_method]], [[project_flag_pass_review_patterns]], [[feedback_review_commit_not_worktree]].\n"
}
````

### User / tool · 2026-11-02T02:18:49.038Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_flag_source_kind_and_run_signal.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:49.421Z

**tool call — Bash**
````
{
 "command": "ls .claude/agent-memory/claims-adjuster-reviewer/; rm -f artifacts/review-evidence/T-061-jsoncheck.py; ls artifacts/review-evidence | grep T-061",
 "description": "List memory dir and tidy evidence folder"
}
````

### User / tool · 2026-11-02T02:18:49.529Z

**tool result**
````
/bin/bash: child setpgid (60728 to 60728): Operation not permitted
MEMORY.md
feedback_lexicon_review_method.md
feedback_review_commit_not_worktree.md
project_flag_pass_review_patterns.md
project_flag_source_kind_and_run_signal.md
project_research_attack_map_gaps.md
project_t036_r4_split_and_judge_fixtures.md
T-061-base-failed.txt
T-061-head-failed.txt
T-061-probe.py
T-061-probe.txt
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:51.397Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md"
}
````

### User / tool · 2026-11-02T02:18:51.405Z

**tool result**
````
1	---
2	name: lexicon-review-method
3	description: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes
4	metadata:
5	  type: feedback
6	---
7	
8	A lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real
9	adjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).
10	
11	**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.
12	
13	**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo
14	guard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).
15	Always probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) "No acute fracture, chronic degenerative changes"
16	(comma-scope negation); (3) intake checkboxes "Prior injuries: No."; (4) ROS denial lists >6 tokens; (5) "did not present
17	with"; (6) MIST/scene facts and "out of proportion". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,
18	compliance→causation mapping). See [[research-attack-map-gaps]].
19	
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:54.217Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md",
 "old_string": "with\"; (6) MIST/scene facts and \"out of proportion\". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,\ncompliance→causation mapping). See [[research-attack-map-gaps]].",
 "new_string": "with\"; (6) MIST/scene facts and \"out of proportion\". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,\ncompliance→causation mapping). See [[research-attack-map-gaps]].\n(7) For any exclusion regex (self_report_scope.exclude_sentence, T-061 r0): patient-subject sentences that contain a\nfamily/EMS/witness word and a speech verb (\"Patient states EMS noted a laceration.\"). A regex that matches a non-patient\nname anywhere in the sentence passes every \"exclude\" example and still drops the patient's own statement.\n(8) A lexicon change is not a product change: diff the commit for app/backend and run the parent-vs-HEAD FAILED list (T-061 r0:\nselfcheck PASS, but the flag test went red and production still used the old word filter). See [[project-flag-source-kind-and-run-signal]]."
}
````

### User / tool · 2026-11-02T02:18:54.316Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:55.222Z

**tool call — Edit**
````
{
 "replace_all": false,
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "old_string": "- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2 dropped lexicon self_report; r3 word filter misses \"S:\"/\"Self-reported\", complains-subjects pass; spec unamended",
 "new_string": "- [source_kind history and run signal](project_flag_source_kind_and_run_signal.md) — T-036 r2/r3 word filter; T-061 r0 (dd545e3) lexicon narrowed but AC2 flags/grounding wiring not done, exclude regex over-broad"
}
````

### User / tool · 2026-11-02T02:18:55.330Z

**tool result**
````
The file /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md has been updated successfully. (file state is current in your context — no need to Read it back)
````

### Assistant · claude-haiku-5-5 · 2026-11-02T02:18:57.291Z

fail: 1 blocker (AC2 not done; production still tags EMS/witness/wife/family "complains of" lines as patient_report), 2 majors (commit leaves test_flags_pass.py red; exclude_sentence drops patient-subject sentences that name a family/EMS word), 1 minor (spec text unamended). Review: /Users/arsis/zlayt-pm-project/reviews/T-061-claims-adjuster.md
