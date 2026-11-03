# Subagent: T-008/T-009 review: claims-adjuster (T-008/T-009 review: claims-adjuster)

Source: `agent-a6962abd377e2495c.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T00:31:41.246Z

Working directory: /Users/arsis/zlayt-pm-project. Brief (D.6).
Cards T-008 (domain research: research/chronology-practice.md, adjuster-attacks.md, texas-pi-notes.md, ASSUMPTIONS-proposed.md, memory/GLOSSARY.md — commit 2c76cda) and T-009 (app/llm/lexicon.yaml + research/lexicon_selfcheck.py — commit f419c3b) — M1. AC: `python3 tools/board.py show T-008` / `show T-009` (ignore notes/handoff).
Exercise hands-on: (1) run `.venv/bin/python research/lexicon_selfcheck.py`; (2) write your own adversarial test sentences (save to artifacts/review-evidence/T-009-adjuster-probes.txt) — phrases you as an adjuster would exploit that the lexicon misses (e.g., "symptoms predate", "chronic", "history of", "similar complaints", "non-compliant", "self-discharged", "returned to full duty", "no acute findings", "age-related", "within normal limits") and negations/false positives that would make the tool cry wolf ("denies prior injury", "no history of"); run them through the lexicon matcher (load the YAML with .venv/bin/python and apply the patterns; don't modify the repo); (3) check adjuster-attacks.md against what you'd actually use to discount a demand — is anything missing (time-to-first-treatment, attorney-referral timing, gaps vs. plan of care, low property damage, prior claims)? Is anything overstated? Spot-check 3 sources with WebFetch.
Write reviews/T-008-claims-adjuster.md and reviews/T-009-claims-adjuster.md (D.2 JSON each). Do not fix anything. Reply ≤ 40 lines: verdicts, blockers, majors.

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:43.261Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; ls -la .claude/agent-memory/claims-adjuster-reviewer/; python3 tools/board.py show T-008; echo ----; python3 tools/board.py show T-009; ls research app/llm memory reviews artifacts/review-evidence 2>&1 | head -60",
 "description": "Check memory and show board cards"
}
````

### User / tool · 2026-11-02T00:31:43.445Z

**tool result**
````
total 0
drwxr-xr-x@ 2 arsis  staff   64 Nov  1 18:31 .
drwxr-xr-x@ 9 arsis  staff  288 Nov  1 18:31 ..
---
id: "T-008"
title: "Domain research: PI treatment chronologies, demand packages, what adjusters attack"
milestone: "M1"
role: "researcher"
status: "in_review"
priority: "P0"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:22:50Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T00:17:32Z"
rounds: 0
commits: ["2c76cda"]
reviews: []
ac:
  - {"n": 1, "text": "research/chronology-practice.md and research/adjuster-attacks.md exist, each with >=6 cited sources (URL + one-line takeaway)", "done": true, "evidence": "research/chronology-practice.md: 10 cited sources; research/adjuster-attacks.md: 18 cited sources (grep -cE '^[0-9]+\\. .*https?://'); each URL + one-line takeaway + read-depth label"}
  - {"n": 2, "text": "research/texas-pi-notes.md covers Texas-specific norms relevant to billed charges and records, with sources, and lists assumptions where sources are thin", "done": true, "evidence": "research/texas-pi-notes.md: §41.0105/Haygood (full text read), §18.001 current text + In re Allstate PDF read (2019 amendment: not causation evidence), K&L Auto Crushers, Prop Code §55.004 liens, TRE 902(10); 11 sources; 'Assumptions where sources are thin' T1-T3 + unverified items labeled"}
  - {"n": 3, "text": "memory/GLOSSARY.md has >=25 terms, each with a one-line definition and source or 'assumption'", "done": true, "evidence": "memory/GLOSSARY.md: 35 terms, each one line with research-file source # or 'assumption'"}
  - {"n": 4, "text": "research/ASSUMPTIONS-proposed.md lists >=8 proposed PI-practice assumptions for memory/ASSUMPTIONS.md, each with evidence", "done": true, "evidence": "research/ASSUMPTIONS-proposed.md: 13 proposals P-01..P-13 with evidence refs and confidence; refines A-101..A-103"}
---
## Description
How PI paralegals build treatment chronologies/medical summaries for demand packages; what adjusters and defense counsel attack (gaps, pre-existing/degenerative findings, inconsistent dates, missed appointments, subjective vs objective, causation hedges like 'may represent', 'correlate clinically', 'patient reports'); Texas PI norms relevant to the scenario (e.g., CPRC §41.0105 paid-vs-incurred, §18.001 affidavits) — verify, don't assume. Feeds GLOSSARY, lexicon, personas, ASSUMPTIONS. Use WebSearch/WebFetch; cite URLs.

## Notes (append-only, newest last)
- 2026-11-02T00:17:32Z researcher: claimed
- 2026-11-02T00:19:54Z researcher: Sources gathered: Tex statutes (18.001 via rulesofcivilprocedure mirror; statutes.capitol.texas.gov pages render as nav-only to WebFetch), Haygood (FindLaw), Allstate PDF text extracted (fn: 2019 amendment says 18.001 affidavits not causation evidence), K&L Auto Crushers, Guevara, JLG Trucking, Jelinek, Prop Code 55.004, Claims Journal adjuster checklist, Brinjikji AJNR 2015, EvenUp chronology guide. Writing research files now.
- 2026-11-02T00:22:47Z researcher: AC 1 checked: research/chronology-practice.md: 10 cited sources; research/adjuster-attacks.md: 18 cited sources (grep -cE '^[0-9]+\. .*https?://'); each URL + one-line takeaway + read-depth label
- 2026-11-02T00:22:47Z researcher: AC 2 checked: research/texas-pi-notes.md: §41.0105/Haygood (full text read), §18.001 current text + In re Allstate PDF read (2019 amendment: not causation evidence), K&L Auto Crushers, Prop Code §55.004 liens, TRE 902(10); 11 sources; 'Assumptions where sources are thin' T1-T3 + unverified items labeled
- 2026-11-02T00:22:47Z researcher: AC 3 checked: memory/GLOSSARY.md: 35 terms, each one line with research-file source # or 'assumption'
- 2026-11-02T00:22:47Z researcher: AC 4 checked: research/ASSUMPTIONS-proposed.md: 13 proposals P-01..P-13 with evidence refs and confidence; refines A-101..A-103
- 2026-11-02T00:22:47Z researcher: moved in_progress -> in_review

## Handoff
What changed: research/{chronology-practice,adjuster-attacks,texas-pi-notes,ASSUMPTIONS-proposed}.md + memory/GLOSSARY.md (35 terms). How verified: source counts by grep; Haygood and In re Allstate read in full (PDF text extracted); statute text via mirrors because statutes.capitol.texas.gov renders nav-only to WebFetch. What's left: orchestrator to merge P-01..P-13 into memory/ASSUMPTIONS.md; GLOSSARY PHI entries are finalized under T-012. Surprised: no published chronology standard exists (AALNC or bar) — all how-to material is vendor content; 2019 §18.001 amendment explicitly says affidavits are not causation evidence; Texas law makes billed charges inadmissible at trial (Haygood), so the tool must label totals 'billed', never 'damages'.

----
---
id: "T-009"
title: "Flag lexicon (app/llm/lexicon.yaml) with per-phrase rationale and source"
milestone: "M1"
role: "researcher"
status: "in_review"
priority: "P0"
depends_on: ["T-008"]
created_by: "orchestrator"
created_at: "2026-11-02T00:17:01Z"
updated_at: "2026-11-02T00:28:03Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T00:22:55Z"
rounds: 0
commits: ["f419c3b"]
reviews: []
ac:
  - {"n": 1, "text": "app/llm/lexicon.yaml parses with yaml.safe_load and every entry has pattern, flag_type, rationale, source", "done": true, "evidence": ".venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS (yaml.safe_load; required fields id/pattern/flag_type/rationale/source/false_positive/strength/negatable on all 48; all regexes compile with re.I)"}
  - {"n": 2, "text": "covers every Appendix C phrase: 'may represent', 'degenerative', 'correlate clinically', 'patient reports', 'patient states', 'missed appointment(s)', 'discharged', 'new onset', 'in 2023, resolved' style prior-history mentions", "done": true, "evidence": "Appendix C coverage, verified on sample records by selfcheck: may_represent(8), degenerative(8), correlate_clinically(8), patient_reports_generic(3,5,9), patient_attributes_causation(9 'patient states'), missed_appointments(6), discharged_from_care(6), new_onset(7), prior_history_year_resolved(3 'in 2023, resolved'), per_patient_or_intake(7 date conflict), plan_not_completed(4)"}
  - {"n": 3, "text": ">=30 entries total; each with a false-positive note (e.g. 'denies prior' must not count as a prior condition)", "done": true, "evidence": "48 entries, each with false_positive note; negation guard suppresses 'denies prior neck injury', 'no history of', 'no degenerative change', 'has not missed any sessions' (examples.negated, tested); 'missing 3 days of work' does not hit missed_appointments"}
---
## Description
Deterministic second signal for the pre-existing and causation-weakening flags (docs/CONTRACT.md §5.2). Each entry: pattern (literal or regex), flag_type (pre_existing | causation_weakening | compliance), rationale, source, false-positive notes.

## Notes (append-only, newest last)
- 2026-11-02T00:21:18Z orchestrator: assigned: researcher-a
- 2026-11-02T00:22:55Z researcher: claimed
- 2026-11-02T00:22:55Z researcher: Claimed with --force: depends on T-008, which is in_review (not done). Orchestrator assigned T-008->T-009 sequence to me; T-009 consumes T-008's adjuster-attacks.md, which is committed (2c76cda). If T-008 review changes the attack taxonomy, I'll update the lexicon in the same round.
- 2026-11-02T00:28:02Z researcher: lexicon.yaml v1: 48 entries (pre_existing 17, causation_weakening 21, compliance 10) + NegEx-style negation block (cues, terminators, pseudo-negations) + per-entry strength (high/medium/low; low never raises a flag alone) + examples (hit/miss/negated). research/lexicon_selfcheck.py is a reference guard implementation + example tests; PASS. Sample-case hits match each entry's appendix_c list exactly. Backend handoff: semantics block at top of the YAML is binding; examples are ready-made unit-test vectors for qa.
- 2026-11-02T00:28:02Z researcher: AC 1 checked: .venv/bin/python research/lexicon_selfcheck.py -> RESULT: PASS (yaml.safe_load; required fields id/pattern/flag_type/rationale/source/false_positive/strength/negatable on all 48; all regexes compile with re.I)
- 2026-11-02T00:28:02Z researcher: AC 2 checked: Appendix C coverage, verified on sample records by selfcheck: may_represent(8), degenerative(8), correlate_clinically(8), patient_reports_generic(3,5,9), patient_attributes_causation(9 'patient states'), missed_appointments(6), discharged_from_care(6), new_onset(7), prior_history_year_resolved(3 'in 2023, resolved'), per_patient_or_intake(7 date conflict), plan_not_completed(4)
- 2026-11-02T00:28:02Z researcher: AC 3 checked: 48 entries, each with false_positive note; negation guard suppresses 'denies prior neck injury', 'no history of', 'no degenerative change', 'has not missed any sessions' (examples.negated, tested); 'missing 3 days of work' does not hit missed_appointments
- 2026-11-02T00:28:02Z researcher: moved in_progress -> in_review

## Handoff
What changed: app/llm/lexicon.yaml (48 entries, negation block, strength tiers, test vectors) + research/lexicon_selfcheck.py (reference guard + example tests). How verified: selfcheck PASS; sample-record hits equal appendix_c expectations; FP probes clean. What's left: backend implements matcher per header semantics (dedupe per span+flag_type; year>=accident-year filter for prior_history_year_resolved and dated_prior_event); qa can lift examples into tests/. Surprised: the low-strength context entries (normal_imaging on 'CT head negative', improving pain) would hurt flag precision if treated as flags — hence the strength tier; recommend backend raise flags only on high/medium.

app/llm:
lexicon.yaml
prompts

artifacts/review-evidence:
T-001-exercise-1.txt
T-001-exercise-2.txt
T-001-exercise-3.txt
T-002-curl.txt
T-003-git-guard-commit-secret-probe.txt
T-003-git-guard-probe.txt
T-003-other-hooks-probe.txt
T-003-reviewer-write-guard-probe.txt
T-004-agent-check.txt
T-006-check-secrets-probe.txt
T-006-rename-probe.txt
T-010-011-sections.txt
T-013-paralegal-walkthrough.md
T-013-trace.md
T-014-amount-cue-demo.py
T-014-injection-trace.md
T-014-json-check.out
T-014-json-check.py
T-014-walkthrough.md
T-015-legal-nurse-items.md
T-015-paralegal-blind.md
T-015-paralegal-regex-probe.out.txt
T-015-paralegal-regex-probe.py

memory:
ASSUMPTIONS.md
DECISIONS.md
ENVIRONMENT.md
GLOSSARY.md
LESSONS.md
PROGRESS.md
SCOPE_CUTS.md
STATE.md
contracts

research:
ASSUMPTIONS-proposed.md
adjuster-attacks.md
chronology-practice.md
lexicon_selfcheck.py
phi-and-ai-supervision.md
texas-pi-notes.md

reviews:
T-001-staff-engineer.md
T-002-staff-engineer.md
T-003-security.md
T-004-staff-engineer.md
T-005-product-manager.md
T-006-security.md
T-007-staff-engineer-r2.md
T-007-staff-engineer.md
T-013-paralegal.md
T-013-product-manager.md
T-014-privacy-compliance.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:45.651Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python research/lexicon_selfcheck.py 2>&1 | tail -40; wc -l research/*.md memory/GLOSSARY.md app/llm/lexicon.yaml research/lexicon_selfcheck.py; git log --oneline -5 2>&1 | head",
 "description": "Run lexicon selfcheck and list file sizes"
}
````

### User / tool · 2026-11-02T00:31:45.820Z

**tool result**
````
entries: 48  by type: pre_existing=17, causation_weakening=21, compliance=10

Sample-case hits (record: entry[strength])
  1: 
  2: normal_imaging[low]
  3: prior_history_year_resolved[high], patient_reports_generic[low], recovery_language[low]
  4: plan_not_completed[medium]
  5: patient_reports_generic[low], improving_low_pain[low]
  6: improving_low_pain[low], missed_appointments[high], discharged_from_care[high]
  7: per_patient_or_intake[high], new_onset[high]
  8: degenerative[high], may_represent[high], correlate_clinically[high]
  9: patient_attributes_causation[high], patient_reports_generic[low]

RESULT: PASS
      23 research/ASSUMPTIONS-proposed.md
     110 research/adjuster-attacks.md
      90 research/chronology-practice.md
     119 research/phi-and-ai-supervision.md
     110 research/texas-pi-notes.md
      50 memory/GLOSSARY.md
     699 app/llm/lexicon.yaml
     135 research/lexicon_selfcheck.py
    1336 total
8a22a5c docs(research): PHI handling and AI-output supervision for Texas PI firm (T-012)
64f766e docs(spec): requirements round 2: split letter vs internal notes, edit rules, export template
f419c3b feat(research): flag lexicon with negation guard and test vectors (T-009)
0a10094 feat(personas): product/engineering reviewer dossiers (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
34e9398 feat(personas): domain reviewer dossiers (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:46.961Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/adjuster-attacks.md"
}
````

### User / tool · 2026-11-02T00:31:46.970Z

**tool result**
````
1	# What adjusters and defense counsel attack in a treatment chronology
2	
3	Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
4	Purpose: ground the four required flags (gap, conflict, prior/pre-existing, causation-weakening language), the
5	claims-adjuster reviewer persona, and `app/llm/lexicon.yaml`.
6	
7	**Source balance.** Plaintiff-firm blogs dominate search results. We deliberately added insurer-side and
8	neutral sources: Claims Journal (adjuster trade press, src 1), Verisk/ISO (insurer data vendor, src 2), Texas
9	Supreme Court opinions (srcs 9–12), and peer-reviewed radiology literature (srcs 6–8). Colossus internals are
10	proprietary; claims about it are second-hand (src 3) and labeled as such.
11	**Read depth.** Sources 1 and 12 were fetched and read in full; the rest were assessed from search-engine
12	excerpts of the page (the takeaway lines quote only what the excerpt showed). Verify before quoting externally.
13	
14	## Attack map, applied to the Jordan Rivera sample
15	
16	| # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
17	|---|---|---|---|---|---|
18	| A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
19	| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments"; 12 planned vs 9 | causation_weakening + conflict |
20	| A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
21	| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6, 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation_weakening |
22	| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation_weakening |
23	| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation_weakening |
24	| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs EMS/ER 2026-01-09 | conflict (code) |
25	| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm" after 73-day gap | causation_weakening |
26	| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Pain 7/10 → 3/10 subjective; objective: ROM −40% (rec 4), CT negative (rec 2), MRI C5-C6 (rec 8) | (context; not a required flag) |
27	| A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | PT rate $185/visit with no visit count → cannot total | amounts (code) |
28	| A11 | **Prior claims history** | ISO ClaimSearch shows earlier injury claims | 2 | Not in records — out of scope for the tool | — |
29	
30	## Notes per attack
31	
32	**A1 Gaps.** The adjuster checklist in Claims Journal names "treatment timing and gaps" explicitly (src 1).
33	Colossus is reported to score duration and frequency per injury (src 3, second-hand). Plaintiff firms say even
34	short gaps are used (src 4, 5). Nothing authoritative sets 30 days; the 30-day threshold is the Zlayt spec's.
35	Practitioners advise *explaining* a gap rather than hiding it (src 5) → the tool flags, the lawyer explains.
36	
37	**A2 Missed appointments.** Mitigation is an affirmative defense — the defendant bears the burden and must show
38	the failure increased damages (src 13). Courts split on outcomes: an instruction was justified where >12 PT
39	sessions were missed (Herrera v. Madrak, src 14) but not where the plaintiff had reasons (Fletcher v. Simmons,
40	same source). So "two missed appointments" is a *review* flag, not a conclusion. The 12-planned-vs-discharged-at-9
41	discrepancy is a conflict an adjuster will see immediately.
42	
43	**A3 Prior conditions.** Verisk sells ISO ClaimSearch to let adjusters "identify preexisting or subsequent injury"
44	(src 2). Concealing priors is described as a credibility killer (src 15). Even a *resolved, different-region*
45	prior (2023 low back vs 2026 neck) must be surfaced; the paralegal decides relevance.
46	False-positive risk: "denies prior neck injury" is a *negative* — it must not be flagged as a prior condition.
47	
48	**A4/A5 Degenerative findings and hedges.** Brinjikji et al. (AJNR 2015, 33 studies, 3,110 asymptomatic people):
49	disc bulge prevalence rose from ~30% at age 20 to ~84% at 80; protrusion from 29% to 43% (src 6). The defense
50	uses this to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses the "new onset"
51	radicular symptoms to argue aggravation. The record itself is equivocal — so the product must keep it
52	equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
53	Radiology literature treats "clinical correlation" and "cannot be excluded" as hedges that shift
54	interpretation to the clinician (src 7, 8). In Texas, causation testimony must reach *reasonable medical
55	probability*; possibility language does not (Jelinek v. Casas, src 11, secondary).
56	
57	**A6 Patient self-report.** In Texas, lay testimony can prove causation only for conditions within common
58	knowledge; otherwise expert testimony is required (Guevara v. Ferrer, src 9). A PM-clinic note that the
59	"patient states symptoms began after the January collision" records history, not a physician's causation
60	opinion. The export may quote it but must attribute it ("patient states"), never restate it as fact.
61	
62	**A7 Inconsistent dates.** Defense impeaches with the claimant's own intake forms (Georgia appeal, src 17);
63	contemporaneous records outweigh an expert relying on an incorrect history (src 17, Australian PIC). In
64	JLG Trucking v. Garza (Tex. 2015) evidence of a *second* accident was relevant to causation and its exclusion
65	was reversible error (src 10) — a second accident date in the records is exactly what defense counsel looks for.
66	The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.
67	
68	**A9 Subjective vs objective.** Adjusters weigh objective findings (imaging, ROM measurements, spasm) above pain
69	scores (src 1, 18). Not a required flag; useful for the one-line summary (keep numbers verbatim) and for the
70	adjuster persona's checklist.
71	
72	**A10 Billing.** Texas limits recovery to amounts "actually paid or incurred" and makes unadjusted list charges
73	inadmissible (Haygood, src 12); negotiated rates are discoverable to test reasonableness (K&L Auto Crushers,
74	see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcoding (src 1). For the tool: list
75	*billed* amounts exactly as written and never present them as the recoverable figure.
76	
77	## Implications for flags and lexicon (handed to T-009)
78	
79	- Lexicon categories: `pre_existing` (A3, A4), `causation_weakening` (A2, A4–A6, A8), `compliance` (A2 — missed
80	  appointments, non-compliance, discharged/left AMA).
81	- Every phrase that is a *negation* ("denies", "no history of", "no prior") is a false-positive guard.
82	- Hedges are flagged *because* they are hedges; the flag rationale must say the record is equivocal, not that
83	  the finding is degenerative.
84	- Self-report markers ("patient states/reports/believes/attributes") are flagged only when attached to causation
85	  or onset, else they are noise (every history line starts "patient reports").
86	
87	## Sources
88	
89	1. Claims Journal, C. Tidball, "How to Review Bodily Injury Demands" (2013-06-05) — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Adjuster checklist: treatment timing/gaps, priors and intervening causes, objective findings, provider credentials, duration vs typical recovery, billing vs SOAP notes, mechanism of injury. (Insurer-side trade press.)
90	2. Verisk, "5 reasons workers compensation adjusters need ISO ClaimSearch" — https://www.verisk.com/blog/5-reasons-workers-compensation-adjusters-need-iso-claimsearch/ — Insurer data vendor: ClaimSearch shows claimant loss history so adjusters can "identify preexisting or subsequent injury." (Insurer-side vendor; via search snippet.)
91	3. Simmons & Fletcher, "What is Colossus Claims Adjusting Software?" — https://www.simmonsandfletcher.com/car-accidents/auto-insurance-claims/colossus/ — Second-hand: Colossus records duration of treatment per injury, prognosis, future treatment. (Plaintiff firm; Colossus is proprietary — unverified.)
92	4. Butler Firm, "How insurance companies use gaps in medical treatment against you" — https://butlerfirm.com/blog/how-insurance-companies-use-gaps-in-medical-treatment-against-you/ — Gaps let insurers argue injuries were minor or unrelated. (Plaintiff firm.)
93	5. Young Injury Law, "Gap in medical treatment" — https://younginjurylaw.com/blog/gap-in-medical-treatment-ohio-injury-claim/ — Explain gaps proactively with referral/appointment paperwork; not every pause hurts. (Plaintiff firm.)
94	6. Brinjikji W. et al., "Systematic literature review of imaging features of spinal degeneration in asymptomatic populations," AJNR 36(4):811 (2015) — https://www.ajnr.org/content/36/4/811 — Degenerative disc findings are common in pain-free adults and rise with age (bulge ~30%→84%, protrusion 29%→43%, age 20→80). (Peer-reviewed; abstract figures via search index — page 403'd to WebFetch.)
95	7. AuntMinnie Europe, "Banned: top 8 words or phrases to avoid in radiology reports" — https://www.auntminnieeurope.com/clinical-news/article/15646568/banned-top-8-words-or-phrases-to-avoid-in-radiology-reports — Radiology chair lists "cannot rule out" and "clinical correlation" as hedges that can mislead. (Radiology trade press.)
96	8. UCSF study of uncertainty terms in 642,569 radiology impressions — https://escholarship.org/content/qt3f22329f/qt3f22329f.pdf — Hedging terms vary by radiologist and subspecialty; "cannot exclude" signals uncertainty. (Academic.)
97	9. Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007) — https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html — Expert testimony generally required for causation of conditions outside lay knowledge; lay evidence suffices only for basic, immediate injuries. (Primary; summary page.)
98	10. JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015) — https://www.txcourts.gov/media/943999/130978.pdf — Evidence of a second accident is relevant to causation; excluding it was harmful error. (Primary; read via summaries.)
99	11. Jelinek v. Casas, 328 S.W.3d 526 (Tex. 2010) — https://case-law.vlex.com/vid/jelinek-v-casas-no-887565131 — Causation needs "reasonable medical probability"; testimony that something is a *possible* cause ordinarily is not enough. (Primary; read via secondary summaries — verify pin cites.)
100	12. Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011) — https://caselaw.findlaw.com/tx-supreme-court/1573065.html — Recovery limited to amounts actually paid or incurred; only evidence of recoverable expenses is admissible. (Primary, full text read.)
101	13. Roman Austin, "Mitigate damages" — https://romanaustin.com/blog/mitigate-damages/ — Texas firm: failure to mitigate requires the insurer to show the claimant's conduct increased damages. (Plaintiff firm.)
102	14. Herrera v. Madrak (missed >12 PT sessions supported a mitigation instruction) — https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215 — Contrast Fletcher v. Simmons (La. App. 2003), https://www.studicata.com/summaries/court-of-appeal-of-louisiana/fletcher-v-simmons-2003-l2aha0 — insufficient evidence of failure to mitigate. (Primary/summaries; non-Texas.)
103	15. Tavrn, "Legal demand letter best practices" — https://www.tavrn.ai/blog/legal-demand-letter-best-practices — Concealed pre-existing conditions draw credibility discounts across the claim. (Vendor.)
104	16. Virginia Lawyers Weekly, "Plaintiff prevails in disputed back injury case" (2014) — https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/ — Defense expert attributed symptoms persisting past 6–9 weeks to pre-existing degenerative disc disease. (Legal press.)
105	17. Georgia Court of Appeals decision on impeachment with prior intake forms — https://caselaw.findlaw.com/court/ga-court-of-appeals/1418582.html — Defense may impeach with the claimant's own medical intake forms listing prior accidents/complaints. (Primary, non-Texas; via search summary.)
106	18. Braun Law, "Objective vs. Subjective" — https://braunslaw.com/claimclinic/claim-worth/specific-injuries/ — Claim evaluation software weighs objective injuries more heavily. (Plaintiff firm.)
107	
108	Assumptions where sources are thin: (a) no public adjuster manual quantifies how much each attack reduces value;
109	(b) Colossus specifics are second-hand; (c) the 30-day gap threshold is the Zlayt spec's, not an industry rule —
110	real adjusters may treat shorter gaps as material, so the prototype's threshold should be configurable.
111	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:47.626Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/app/llm/lexicon.yaml"
}
````

### User / tool · 2026-11-02T00:31:47.761Z

**tool result**
````
1	# Flag lexicon — deterministic second signal for review flags (contract §5.2).
2	# Owner: researcher (T-009). Consumer: backend flag engines (pre_existing, causation_weakening, compliance).
3	# Research basis: research/adjuster-attacks.md (attacks A1–A11, sources 1–18), research/texas-pi-notes.md,
4	# research/chronology-practice.md. "AA src N" below = research/adjuster-attacks.md source N.
5	#
6	# HOW TO USE (binding semantics for the backend)
7	# - Patterns are Python `re` regexes, compiled with re.IGNORECASE, matched against the VERBATIM record text.
8	# - A hit never creates an exported statement. It marks the span for review. Contract §5.2: a lexicon hit
9	#   without an LLM hit (or an LLM hit without a lexicon hit) => item state `needs_review`; the human decides.
10	# - `strength`: high = by itself warrants a review flag; medium = flag, but expect some noise;
11	#   low = annotation/context only — attach to an LLM flag if one exists, do not raise a flag alone.
12	# - `negatable: true` => apply the negation guard below; a negated hit is suppressed (but logged in audit).
13	# - `appendix_c`: the sample-case record(s) this entry is expected to fire on (spec Appendix C), else [].
14	# - examples.hit must match; examples.miss must not match the regex; examples.negated must match the regex
15	#   but be suppressed by the negation guard. Run `.venv/bin/python research/lexicon_selfcheck.py`.
16	# - Overlapping hits on the same span (e.g. "resolved" via two entries) are deduped by code per (span, flag_type).
17	
18	version: 1
19	flag_types: [pre_existing, causation_weakening, compliance]
20	
21	negation:
22	  # NegEx-style guard (Chapman et al. 2001; ConText/pyConText, Chapman et al. 2011 — see sources at bottom).
23	  # A pre-cue within `window_tokens` tokens BEFORE the hit, in the same sentence, with no terminator between,
24	  # negates the hit. Post-cues within the window AFTER the hit also negate.
25	  window_tokens: 6
26	  pre_cues: ['no', 'not', 'denies', 'denied', 'deny', 'negative for', 'no history of', 'no prior', 'no previous',
27	             'no known', 'no evidence of', 'without', 'free of', 'never', 'absence of', 'rules out', 'ruled out']
28	  post_cues: ['denied', 'ruled out', 'is absent', 'was absent', 'not seen', 'not present']
29	  terminators: ['but', 'however', 'although', 'though', 'except', 'aside from', 'apart from', 'which', ';']
30	  pseudo_negations: ['no increase', 'no change', 'not only', 'not necessarily', 'no significant change',
31	                     'cannot be excluded', 'can not be excluded', 'cannot exclude', 'not ruled out',
32	                     'cannot be ruled out', 'no further', 'did not show', 'did not attend', 'did not return',
33	                     'not complian', 'non-complian', 'not doing', 'not performing', 'not related']
34	  note: >
35	    Pseudo-negations are phrases containing a negation word that do NOT negate a finding (they are themselves
36	    hits or neutral). "no change from prior" still implies a prior study. The guard never applies to
37	    compliance entries whose meaning is already negative ("did not attend").
38	
39	entries:
40	
41	# ───────────────────────── pre_existing ─────────────────────────
42	
43	- id: prior_history_year_resolved
44	  pattern: '\b(?:19|20)\d{2}\b\s*[,;:-]?\s*(?:now\s+|since\s+|which\s+(?:has\s+)?|and\s+(?:has\s+)?)?(?:fully\s+|completely\s+)?(?:resolved|healed|recovered)\b'
45	  flag_type: pre_existing
46	  strength: high
47	  negatable: false
48	  rationale: >
49	    A dated prior condition described as resolved ("low back pain in 2023, resolved") is still a documented
50	    prior condition; adjusters and ISO ClaimSearch hunt for exactly these, and concealment costs credibility.
51	    "Resolved" helps the claimant, but the paralegal must see it and decide relevance (different body region here).
52	  source: 'AA A3; AA src 2 (Verisk ISO ClaimSearch), src 15; Appendix C record 3'
53	  false_positive: >
54	    The year may be the accident year or later (e.g. "headache 2026, resolved" after the crash) — code must
55	    compare the year with the earliest accident date and drop hits whose year >= accident year from pre_existing
56	    (they may still matter as "recovery" context).
57	  appendix_c: [3]
58	  examples:
59	    hit: ['Patient reports low back pain in 2023, resolved.', 'neck strain 2019 - fully resolved']
60	    miss: ['Seen 2026-01-16 for neck pain.', 'Symptoms improving since visit 3.']
61	
62	- id: history_of
63	  pattern: '\b(?:past\s+)?(?:medical\s+)?history\s+of\b(?!\s+(?:the\s+)?present\s+illness)'
64	  flag_type: pre_existing
65	  strength: medium
66	  negatable: true
67	  rationale: '"History of X" is the standard clinical way to record a prior condition (AA A3).'
68	  source: 'AA A3; AA src 1 (adjusters check pre-existing conditions), src 2'
69	  false_positive: '"No history of neck injury" / "denies history of" are negatives (negation guard). "History of present illness" is a section header, excluded by the lookahead. Family history ("family history of") is not the patient''s condition — LLM must check.'
70	  appendix_c: []
71	  examples:
72	    hit: ['History of migraines.', 'past medical history of cervical radiculopathy']
73	    miss: ['History of present illness: rear-ended at a light.']
74	    negated: ['Patient has no history of neck injury.', 'Denies history of back pain.']
75	
76	- id: h_o_abbrev
77	  pattern: '\bh/o\b'
78	  flag_type: pre_existing
79	  strength: medium
80	  negatable: true
81	  rationale: 'Abbreviation of "history of" common in dictated notes.'
82	  source: 'AA A3; assumption (standard clinical abbreviation, not separately sourced)'
83	  false_positive: '"No h/o" negated by guard.'
84	  appendix_c: []
85	  examples:
86	    hit: ['h/o lumbar strain']
87	    miss: ['ho hum', 'how often']
88	    negated: ['no h/o trauma']
89	
90	- id: pmh_section
91	  pattern: '\b(?:PMH|PMHx|past\s+medical\s+history)\s*[:\-]\s*(?!\s*(?:none|neg|negative|noncontributory|non-contributory|unremarkable|n/?a)\b)\S'
92	  flag_type: pre_existing
93	  strength: low
94	  negatable: false
95	  rationale: 'A non-empty past-medical-history section is where prior conditions live; low strength because most PMH entries are unrelated (hypertension, asthma).'
96	  source: 'AA A3; assumption (section convention)'
97	  false_positive: '"PMH: none" / "noncontributory" excluded by lookahead. Unrelated chronic diseases will hit — LLM decides relevance to the injured body region.'
98	  appendix_c: []
99	  examples:
100	    hit: ['PMH: hypertension, prior lumbar strain']
101	    miss: ['PMH: none', 'PMH: noncontributory']
102	
103	- id: prior_injury_or_event
104	  pattern: '\b(?:prior|previous|earlier|old|remote|past)\s+(?:\w+\s+)?(?:injur(?:y|ies)|accidents?|MVAs?|MVCs?|collisions?|wrecks?|claims?|surger(?:y|ies)|fractures?|episodes?|treatment|chiropractic\s+care|physical\s+therapy)\b'
105	  flag_type: pre_existing
106	  strength: high
107	  negatable: true
108	  rationale: 'Prior injuries and accidents are the core pre-existing attack; JLG Trucking shows other accidents are admissible on causation.'
109	  source: 'AA A3, A7; AA src 2, src 10 (JLG Trucking v. Garza)'
110	  false_positive: '"No prior injuries" / "denies prior MVA" negated by guard. "Prior to the accident she was working full time" does not match (no event noun).'
111	  appendix_c: []
112	  examples:
113	    hit: ['Prior MVA in 2019 with neck pain.', 'previous lumbar surgery', 'had prior chiropractic care']
114	    miss: ['Prior to the accident she worked full time.']
115	    negated: ['Denies prior neck injuries.', 'No previous accidents.']
116	
117	- id: pre_existing_literal
118	  pattern: '\bpre-?\s?existing\b|\bpreexisting\b'
119	  flag_type: pre_existing
120	  strength: high
121	  negatable: true
122	  rationale: 'Explicit label.'
123	  source: 'AA A3; AA src 15'
124	  false_positive: '"No pre-existing conditions" negated by guard.'
125	  appendix_c: []
126	  examples:
127	    hit: ['pre-existing cervical spondylosis', 'aggravation of preexisting condition']
128	    miss: ['existing plan of care continues']
129	    negated: ['No pre-existing conditions reported.']
130	
131	- id: chronic
132	  pattern: '\bchronic(?:ally)?\b'
133	  flag_type: pre_existing
134	  strength: medium
135	  negatable: true
136	  rationale: '"Chronic" implies duration predating or outlasting the incident; defense reads it as pre-existing.'
137	  source: 'AA A3, A4; AA src 16 (defense expert attributes persisting symptoms to pre-existing disease)'
138	  false_positive: 'Post-accident chronicity ("chronic neck pain since the January collision") is a damages fact, not a prior condition — LLM must check timing. Negated by guard: "no chronic conditions".'
139	  appendix_c: []
140	  examples:
141	    hit: ['chronic low back pain', 'chronically elevated']
142	    miss: ['chronology attached']
143	    negated: ['No chronic conditions.']
144	
145	- id: longstanding
146	  pattern: '\blong-?\s?standing\b|\bfor\s+(?:many\s+|several\s+)?years\b'
147	  flag_type: pre_existing
148	  strength: medium
149	  negatable: true
150	  rationale: 'Duration language that predates the incident.'
151	  source: 'AA A3; assumption (clinical usage)'
152	  false_positive: '"has worked as a driver for years" is social history — LLM must tie it to a symptom.'
153	  appendix_c: []
154	  examples:
155	    hit: ['longstanding neck stiffness', 'headaches for many years']
156	    miss: ['standing desk recommended']
157	
158	- id: flare_recurrence
159	  pattern: '\b(?:flare(?:-?\s?ups?)?|recurren(?:ce|t)|relaps(?:e|ed))\b'
160	  flag_type: pre_existing
161	  strength: medium
162	  negatable: true
163	  rationale: 'A flare or recurrence presupposes an earlier episode.'
164	  source: 'AA A3; assumption (clinical usage)'
165	  false_positive: '"Recurrent headaches since the accident" is post-incident — LLM checks timing.'
166	  appendix_c: []
167	  examples:
168	    hit: ['flare-up of back pain', 'recurrent neck pain']
169	    miss: ['flared jeans']
170	
171	- id: exacerbation_aggravation
172	  pattern: '\b(?:exacerbation|aggravation|worsening|exacerbated|aggravated)\s+(?:of\s+)?(?:(?:his|her|their|a|the|an)\s+)?(?:pre-?existing|prior|previous|underlying|baseline|chronic|known|old)\b'
173	  flag_type: pre_existing
174	  strength: high
175	  negatable: false
176	  rationale: 'Aggravation of a prior condition is compensable but argued differently from a new injury; chronologies must distinguish them.'
177	  source: 'research/chronology-practice.md src 1 (distinguish aggravation from new injury); AA A3'
178	  false_positive: '"Aggravated by turning head" (symptom trigger, no prior condition) does not match because a prior/underlying qualifier is required.'
179	  appendix_c: []
180	  examples:
181	    hit: ['exacerbation of underlying degenerative disease', 'aggravation of pre-existing cervical condition']
182	    miss: ['pain aggravated by turning head']
183	
184	- id: degenerative
185	  pattern: '\bdegenerat(?:ive|ion)\b|\bDDD\b|\bDJD\b'
186	  flag_type: pre_existing
187	  strength: high
188	  negatable: true
189	  rationale: 'Degenerative findings are the most common defense explanation for spinal imaging; they are common in asymptomatic adults (Brinjikji 2015). The tool must surface them and never resolve them to "degenerative" or "traumatic".'
190	  source: 'AA A4; AA src 6 (Brinjikji, AJNR 2015), src 16; Appendix C record 8'
191	  false_positive: '"No degenerative change" negated by guard. Must not be paraphrased to a conclusion — the flag text quotes the record.'
192	  appendix_c: [8]
193	  examples:
194	    hit: ['Findings may represent degenerative change', 'mild disc degeneration at C5-C6', 'DDD L4-5']
195	    miss: ['generated report']
196	    negated: ['No degenerative change identified.']
197	
198	- id: degenerative_imaging_terms
199	  pattern: '\b(?:spondylo(?:sis|tic)|osteoarthrit\w*|arthropath\w*|osteophyt\w*|desiccat\w*|uncovertebral\s+(?:joint\s+)?hypertroph\w*|facet\s+(?:joint\s+)?(?:hypertroph\w*|arthropath\w*|arthros\w*)|endplate\s+(?:changes?|sclerosis)|Modic\s+(?:type\s+)?[123I]+|loss\s+of\s+disc\s+height|disc\s+space\s+narrowing)\b'
200	  flag_type: pre_existing
201	  strength: high
202	  negatable: true
203	  rationale: 'Radiology vocabulary for chronic/degenerative change that defense reviewers cite as pre-existing.'
204	  source: 'AA A4; AA src 6 (Brinjikji lists these features in asymptomatic populations)'
205	  false_positive: 'Negated by guard ("no osteophytes"). Foraminal narrowing alone is NOT in this list (can be acute or chronic) — record 8 "mild right foraminal narrowing" should not fire here.'
206	  appendix_c: []
207	  examples:
208	    hit: ['C5-6 spondylosis', 'small anterior osteophytes', 'disc desiccation at C5-C6', 'Modic type 1 changes']
209	    miss: ['mild right foraminal narrowing']
210	    negated: ['No osteophytes or spondylosis.']
211	
212	- id: age_related_old_findings
213	  pattern: '\b(?:age-?\s?related|age-?\s?appropriate|chronic-?\s?appearing|old\s+(?:healed\s+)?(?:fracture|injury|deformity)|remote\s+(?:injury|fracture|history)|congenital(?:ly)?)\b'
214	  flag_type: pre_existing
215	  strength: high
216	  negatable: true
217	  rationale: 'Explicit statements that a finding predates the incident or is due to age.'
218	  source: 'AA A4; AA src 6'
219	  false_positive: 'Negated by guard.'
220	  appendix_c: []
221	  examples:
222	    hit: ['age-related changes', 'old healed fracture of the left clavicle', 'congenitally narrow canal']
223	    miss: ['aged 41']
224	
225	- id: self_reported_prior
226	  pattern: '\b(?:patient|pt|he|she|client)\s+(?:reports|reported|states|stated|notes|endorses|admits|recalls)\s+(?:(?:a|an|some)\s+)?(?:prior|previous|past|old|earlier|history)\b'
227	  flag_type: pre_existing
228	  strength: high
229	  negatable: false
230	  rationale: 'Self-reported prior history: the record''s own admission of an earlier condition.'
231	  source: 'AA A3, A6; Appendix C record 3 (self-reported prior)'
232	  false_positive: 'Requires a prior/previous/history word immediately after the reporting verb; "patient reports missing 3 days of work" does not match.'
233	  appendix_c: []
234	  examples:
235	    hit: ['Patient reports prior neck pain after a 2018 fall.', 'pt endorses history of migraines']
236	    miss: ['Patient reports missing 3 days of work.']
237	
238	- id: dated_prior_event
239	  pattern: '\b(?:in\s+)?(?:19|20)\d{2}\b[^.;]{0,30}?\b(?:injur(?:y|ed|ies)|accident|MVA|MVC|collision|wreck|fall|fell|surgery|fracture)\b'
240	  flag_type: pre_existing
241	  strength: medium
242	  negatable: true
243	  rationale: 'A dated event other than the incident (e.g. "2019 MVA") is a prior or intervening event.'
244	  source: 'AA A3, A7; AA src 10 (JLG Trucking — other accidents relevant)'
245	  false_positive: 'Will also fire on the incident itself ("2026 collision"). Code must drop hits whose year equals the accident year AND whose text refers to the same event; when unsure → needs_review. ISO dates like 2026-01-09 are matched as years too — code should skip hits where the year is part of a full date equal to a known accident date.'
246	  appendix_c: []
247	  examples:
248	    hit: ['MVA in 2019 with neck injury', '2021 fall at work']
249	    miss: ['Pain 4/10, improving.']
250	    negated: ['No 2019 injury reported.']
251	
252	- id: similar_symptoms_before
253	  pattern: '\b(?:similar|same|identical)\s+(?:symptoms|pain|complaints?|problems?)\s+(?:\w+\s+){0,3}(?:before|previously|in\s+the\s+past|years?\s+ago|prior)\b'
254	  flag_type: pre_existing
255	  strength: high
256	  negatable: true
257	  rationale: 'Direct statement that the current complaint pre-dates the incident.'
258	  source: 'AA A3'
259	  false_positive: 'Negated by guard: "never had similar symptoms before".'
260	  appendix_c: []
261	  examples:
262	    hit: ['had similar pain years ago', 'same symptoms previously']
263	    miss: ['similar to last visit']
264	    negated: ['Never had similar symptoms before.']
265	
266	- id: comparison_prior_imaging
267	  pattern: '\b(?:compared?\s+(?:with|to)\s+(?:the\s+)?(?:prior|previous|outside)|comparison\s*:\s*(?!none)\S|unchanged\s+(?:from|since|compared)|stable\s+(?:since|from|compared)|no\s+(?:significant\s+)?(?:interval\s+)?change\s+(?:from|since))'
268	  flag_type: pre_existing
269	  strength: medium
270	  negatable: false
271	  rationale: 'A comparison to a PRIOR study of the same region means there was earlier imaging — i.e., an earlier reason to image. Subtle, easily missed by a summary.'
272	  source: 'AA A3 (missing baseline records invite pre-existing arguments, CP src 6); assumption (radiology report convention)'
273	  false_positive: '"Comparison: none" excluded. A comparison to imaging from after the incident (e.g. the ER CT) is not a prior condition — code compares dates when the prior study date is given.'
274	  appendix_c: []
275	  examples:
276	    hit: ['Comparison: MRI cervical spine 2021-03-04.', 'Unchanged from prior study.', 'no interval change from 2020']
277	    miss: ['Comparison: none.']
278	
279	# ───────────────────────── causation_weakening ─────────────────────────
280	
281	- id: may_represent
282	  pattern: '\bmay\s+(?:represent|reflect|indicate|suggest|be\s+(?:due\s+to|related\s+to|secondary\s+to|consistent\s+with|from|a\s+result\s+of))\b'
283	  flag_type: causation_weakening
284	  strength: high
285	  negatable: false
286	  rationale: 'Possibility language. Texas causation requires reasonable medical probability; "may" signals possibility, and the defense reads "may represent degenerative change" as an alternative cause. Keep the hedge verbatim.'
287	  source: 'AA A5; AA src 11 (Jelinek v. Casas), src 7, src 8; Appendix C record 8'
288	  false_positive: '"May return to work" / "may follow up" are permissions, not hedges — they do not match because a diagnostic verb is required.'
289	  appendix_c: [8]
290	  examples:
291	    hit: ['Findings may represent degenerative change; correlate clinically.', 'may be related to the prior injury']
292	    miss: ['May return to work Monday.', 'may follow up as needed']
293	
294	- id: correlate_clinically
295	  pattern: '\bcorrelate\s+clinically\b|\bclinical(?:ly)?\s+correlat\w*|\bcorrelation\s+with\s+(?:clinical|symptoms|exam)'
296	  flag_type: causation_weakening
297	  strength: high
298	  negatable: false
299	  rationale: 'The radiologist declines to tie the finding to symptoms and hands interpretation to the clinician; it is not a causation opinion and defense treats it as equivocal.'
300	  source: 'AA A5; AA src 7 (radiology: "clinical correlation" as hedge), src 8; Appendix C record 8'
301	  false_positive: 'Rarely benign in this context; strength high.'
302	  appendix_c: [8]
303	  examples:
304	    hit: ['correlate clinically', 'Clinical correlation recommended.', 'clinically correlate']
305	    miss: ['clinic visit scheduled']
306	
307	- id: possibility_terms
308	  pattern: '\b(?:possibl[ey]|could\s+(?:be|represent|reflect|indicate)|might\s+(?:be|represent|reflect)|perhaps|questionabl[ey]|cannot\s+say)\b'
309	  flag_type: causation_weakening
310	  strength: medium
311	  negatable: false
312	  rationale: 'Possibility/conjecture words. Texas courts treat "possibly"/"perhaps" opinions as conjecture, not reasonable medical probability.'
313	  source: 'AA A5; AA src 11 (Jelinek v. Casas and decisions quoting it)'
314	  false_positive: 'Plans ("possible ESI if no improvement") are about treatment, not causation — LLM checks whether the hedge attaches to a diagnosis or cause. Medium strength for that reason.'
315	  appendix_c: []
316	  examples:
317	    hit: ['possible radiculopathy', 'could represent post-traumatic change', 'questionable relationship to MVA']
318	    miss: ['positive Spurling test']
319	
320	- id: cannot_exclude
321	  pattern: '\b(?:cannot|can\s?not|can''t)\s+(?:be\s+)?(?:exclude[ds]?|rule[ds]?\s+out|ruled\s+out|definitively\s+(?:determine|state))\b|\bnot\s+(?:be\s+)?(?:excluded|ruled\s+out)\b'
322	  flag_type: causation_weakening
323	  strength: medium
324	  negatable: false
325	  rationale: 'Radiology hedge: the finding is possible but unconfirmed; defense cites it to show uncertainty.'
326	  source: 'AA A5; AA src 7, src 8 (UCSF: "cannot exclude" signals uncertainty)'
327	  false_positive: 'Is itself a negation construction — listed as a pseudo-negation so the guard does not suppress other hits around it.'
328	  appendix_c: []
329	  examples:
330	    hit: ['Small protrusion cannot be excluded.', 'cannot rule out degenerative etiology']
331	    miss: ['excluded from study']
332	
333	- id: nonspecific_indeterminate
334	  pattern: '\b(?:non-?\s?specific|indeterminate|equivocal|uncertain\s+(?:significance|etiology|cause|origin)|unclear\s+(?:significance|etiology|cause|origin)|of\s+(?:undetermined|unknown)\s+(?:significance|etiology|cause|origin)|etiology\s+(?:unclear|unknown|uncertain|undetermined))\b'
335	  flag_type: causation_weakening
336	  strength: medium
337	  negatable: false
338	  rationale: 'The record says the cause is unknown — defense reads unknown cause as not-the-accident.'
339	  source: 'AA A5; AA src 8'
340	  false_positive: '"Nonspecific T-wave changes" in an unrelated EKG — LLM checks relevance to the claimed injury.'
341	  appendix_c: []
342	  examples:
343	    hit: ['etiology unclear', 'nonspecific findings', 'of uncertain significance']
344	    miss: ['specific exercises prescribed']
345	
346	- id: likely_alternative_cause
347	  pattern: '\b(?:likely|probably|presumably|most\s+consistent\s+with|suspect(?:ed)?|favor(?:ed)?)\s+(?:\w+\s+){0,2}(?:degenerative|chronic|age-?\s?related|pre-?existing|congenital|incidental|unrelated|longstanding|old)\b'
348	  flag_type: causation_weakening
349	  strength: high
350	  negatable: true
351	  rationale: 'A clinician''s lean toward a non-traumatic cause is the strongest form of the degenerative attack.'
352	  source: 'AA A4, A5; AA src 6, src 16'
353	  false_positive: 'Negated by guard ("not likely degenerative").'
354	  appendix_c: []
355	  examples:
356	    hit: ['likely degenerative in nature', 'most consistent with chronic change']
357	    miss: ['likely post-traumatic strain']
358	
359	- id: incidental_finding
360	  pattern: '\bincidental(?:ly)?\b'
361	  flag_type: causation_weakening
362	  strength: medium
363	  negatable: true
364	  rationale: '"Incidental" means unrelated to the reason for the study; if attached to the injured region, the defense will cite it.'
365	  source: 'AA A4; assumption (radiology usage)'
366	  false_positive: 'Incidental findings in unrelated organs (e.g. thyroid nodule on neck CT) are irrelevant to causation — LLM checks body region.'
367	  appendix_c: []
368	  examples:
369	    hit: ['incidental note of mild disc bulge']
370	    miss: ['accidentally fell']
371	
372	- id: unrelated_to_accident
373	  pattern: '\b(?:unrelated|not\s+related|no\s+(?:clear\s+)?(?:relation(?:ship)?|connection))\s+to\s+(?:the\s+)?(?:\w+\s+)?(?:accident|collision|MVA|MVC|crash|wreck|incident|injury|trauma)\b'
374	  flag_type: causation_weakening
375	  strength: high
376	  negatable: false
377	  rationale: 'An explicit no-causation statement in a treating record.'
378	  source: 'AA A5, A6; AA src 9 (Guevara — causation needs medical evidence; a contrary record undercuts it)'
379	  false_positive: 'Rare; the phrase itself is the negative.'
380	  appendix_c: []
381	  examples:
382	    hit: ['symptoms unrelated to the accident', 'no clear relationship to the MVA']
383	    miss: ['related to the accident']
384	
385	- id: patient_attributes_causation
386	  pattern: '\b(?:patient|pt|he|she|client)\s+(?:states|stated|reports|reported|believes|attributes|relates|related|feels|claims|says|said|thinks)\b[^.;]{0,80}?\b(?:after|since|from|due\s+to|because\s+of|caused\s+by|following|began\s+with)\b[^.;]{0,40}?\b(?:accident|collision|crash|MVA|MVC|wreck|incident|injury|impact)\b'
387	  flag_type: causation_weakening
388	  strength: high
389	  negatable: false
390	  rationale: 'Patient-attributed causation is history, not a physician''s causation opinion. Texas generally requires expert testimony for causation of conditions outside lay knowledge (Guevara). The export may quote it only with attribution.'
391	  source: 'AA A6; AA src 9 (Guevara v. Ferrer), src 11; Appendix C record 9'
392	  false_positive: 'The note is helpful to the claimant as history — the flag is about how it may be described, not that it is false.'
393	  appendix_c: [9]
394	  examples:
395	    hit: ['Patient states symptoms began after the January collision.', 'She believes the pain is from the accident.']
396	    miss: ['Physician opines symptoms are causally related to the collision.']
397	
398	- id: patient_reports_generic
399	  pattern: '\b(?:patient|pt)\s+(?:reports|reported|states|stated|endorses|complains|c/o)\b'
400	  flag_type: causation_weakening
401	  strength: low
402	  negatable: false
403	  rationale: 'Marks subjective, self-reported content (vs objective findings), which adjusters weight less. Context only.'
404	  source: 'AA A9; AA src 1, src 18 (objective findings weighted above subjective)'
405	  false_positive: 'Fires on most history lines ("Patient reports missing 3 days of work" is a damages mention, not a flag). LOW: never raises a flag alone; use only to keep attribution in the summary ("patient reports…").'
406	  appendix_c: [3, 5, 9]
407	  examples:
408	    hit: ['Patient reports low back pain in 2023, resolved.', 'Patient reports missing 3 days of work.', 'Patient states symptoms began after the January collision.']
409	    miss: ['Cervical range of motion reduced approx. 40%.']
410	
411	- id: per_patient_or_intake
412	  pattern: '\b(?:per\s+(?:the\s+)?(?:patient|pt|intake(?:\s+form)?|registration|patient\s+intake(?:\s+form)?|questionnaire)|according\s+to\s+(?:the\s+)?(?:patient|pt|intake)|by\s+(?:patient|pt)\s+report|(?:patient|self)-?\s?reported)\b'
413	  flag_type: causation_weakening
414	  strength: high
415	  negatable: false
416	  rationale: 'Information sourced from the patient or an intake form, not the clinician. Record 7''s "Date of accident per intake form: 2026-01-19" conflicts with EMS/ER (2026-01-09); defense uses a second date to suggest a different incident.'
417	  source: 'AA A7; AA src 10 (JLG Trucking), src 17 (impeachment with intake forms); Appendix C record 7'
418	  false_positive: 'Often benign ("per patient, pain 5/10"). High strength only because the date-conflict engine (code) needs every sourced date with its provenance; LLM decides whether it matters.'
419	  appendix_c: [7]
420	  examples:
421	    hit: ['Date of accident per intake form: 2026-01-19.', 'per patient, onset two weeks ago', 'self-reported pain 8/10']
422	    miss: ['Per protocol, ice applied.']
423	
424	- id: new_onset
425	  pattern: '\bnew(?:ly)?[-\s]+(?:onset|developed|complaints?|symptoms?|pain)\b'
426	  flag_type: causation_weakening
427	  strength: high
428	  negatable: true
429	  rationale: 'New symptoms appearing after a treatment gap invite the intervening-cause argument (record 7: new radicular arm symptoms 73 days after PT discharge, 129 days after the crash). Plaintiffs counter with progression; the tool must keep "new onset" verbatim and flag it.'
430	  source: 'AA A1, A8; AA src 1 (timing), src 16 (delayed-report argument); Appendix C record 7'
431	  false_positive: '"No new complaints" negated by guard. A new symptom documented within days of the crash is less concerning — code can attach days-since-incident to the flag.'
432	  appendix_c: [7]
433	  examples:
434	    hit: ['New onset pain radiating to right arm', 'newly developed numbness']
435	    miss: ['renewed prescription']
436	    negated: ['No new complaints today.']
437	
438	- id: delayed_onset
439	  pattern: '\b(?:delayed\s+onset|(?:began|started|developed|appeared|noticed)\s+(?:\w+\s+){0,3}(?:weeks?|months?)\s+(?:after|later|post)|(?:weeks?|months?)\s+(?:after|following)\s+the\s+(?:accident|collision|MVA|MVC|crash))\b'
440	  flag_type: causation_weakening
441	  strength: medium
442	  negatable: false
443	  rationale: 'Symptoms first reported weeks/months later are attacked as unrelated (Virginia record-review example: symptoms not reported until weeks later).'
444	  source: 'AA A8; AA src 16'
445	  false_positive: '"Two weeks after the accident he returned to work" — LLM checks it is about symptom onset.'
446	  appendix_c: []
447	  examples:
448	    hit: ['numbness began several weeks after the collision', 'delayed onset of headaches']
449	    miss: ['Follow up with PCP in 1 week.']
450	
451	- id: intervening_event
452	  pattern: '\b(?:another|second|subsequent|separate|recent|new|additional)\s+(?:\w+\s+)?(?:accidents?|collisions?|MVAs?|MVCs?|wrecks?|falls?|incidents?|trauma|injur(?:y|ies))\b'
453	  flag_type: causation_weakening
454	  strength: high
455	  negatable: true
456	  rationale: 'An intervening event is admissible alternative-cause evidence in Texas (JLG Trucking: a second accident three months later).'
457	  source: 'AA A7; AA src 10 (JLG Trucking v. Garza)'
458	  false_positive: '"No new injury" / "denies subsequent accidents" negated by guard.'
459	  appendix_c: []
460	  examples:
461	    hit: ['involved in a second accident in April', 'subsequent fall at home']
462	    miss: ['accident report reviewed']
463	    negated: ['Denies any subsequent accidents.']
464	
465	- id: other_activity_mechanism
466	  pattern: '\b(?:while|after|when)\s+(?:\w+\s+)?(?:lifting|moving|playing|exercising|working\s+out|lifting\s+weights|doing\s+yard\s+work|gardening|shoveling|carrying|helping\s+(?:a\s+)?(?:friend|family)\s+move|at\s+the\s+gym)\b'
467	  flag_type: causation_weakening
468	  strength: medium
469	  negatable: false
470	  rationale: 'A non-accident mechanism for current symptoms is an alternative-cause argument.'
471	  source: 'AA A7, A8; AA src 1 (mechanism of injury and intervening causes on the adjuster checklist)'
472	  false_positive: '"Pain while lifting groceries" is a symptom trigger, not a new mechanism — LLM checks whether it describes onset or aggravation.'
473	  appendix_c: []
474	  examples:
475	    hit: ['back pain started while lifting a couch', 'twisted knee when playing basketball']
476	    miss: ['pain with lifting arm overhead']
477	
478	- id: recovery_language
479	  pattern: '\b(?:resolved|resolving|fully\s+recovered|back\s+to\s+(?:baseline|normal)|returned\s+to\s+(?:full|regular|normal)\s+(?:duty|activit(?:y|ies)|work)|pain-?\s?free|asymptomatic|symptom-?\s?free|goals\s+met|released\s+from\s+care|MMI)\b'
480	  flag_type: causation_weakening
481	  strength: low
482	  negatable: true
483	  rationale: 'Documented recovery before later treatment supports the "injury resolved, later care is for something else" argument (gap attack).'
484	  source: 'AA A1; AA src 4, src 5'
485	  false_positive: 'Overlaps prior_history_year_resolved on "resolved" (dedupe by span). Recovery is also good for the claimant as an outcome — LOW strength, context for the gap flag.'
486	  appendix_c: [3]
487	  examples:
488	    hit: ['neck pain resolved', 'returned to full duty', 'Pain-free at discharge.']
489	    miss: ['resolve billing issue']
490	    negated: ['Pain has not resolved.']
491	
492	- id: improving_low_pain
493	  pattern: '\b(?:improv(?:ing|ed|ement)|much\s+better|significantly\s+better|minimal\s+pain|pain\s+(?:[0-3])\s*/\s*10)\b'
494	  flag_type: causation_weakening
495	  strength: low
496	  negatable: true
497	  rationale: 'Low or improving pain before a gap feeds the recovery argument (record 5 "Pain 4/10, improving"; record 6 "Pain 3/10").'
498	  source: 'AA A1, A9; AA src 1'
499	  false_positive: 'Improvement is the expected course of treatment and is good evidence of necessity. LOW: context for gap flags only.'
500	  appendix_c: [5, 6]
501	  examples:
502	    hit: ['Pain 4/10, improving.', 'Pain 3/10.']
503	    miss: ['Pain 7/10.']
504	    negated: ['Not improving with PT.']
505	
506	- id: normal_imaging
507	  pattern: '\b(?:no\s+acute\s+(?:\w+\s+){0,2}(?:abnormalit(?:y|ies)|findings?|fractures?|injur(?:y|ies)|process|pathology|osseous\s+abnormalit(?:y|ies))|(?:CT|MRI|x-?rays?|imaging|radiographs?|films?)\b[^.;]{0,25}\b(?:negative|normal|unremarkable|within\s+normal\s+limits|WNL))\b'
508	  flag_type: causation_weakening
509	  strength: low
510	  negatable: false
511	  rationale: 'Negative imaging is cited to argue a minor injury (absence of objective findings).'
512	  source: 'AA A9; AA src 1 (objective findings: X-ray/MRI/CT), CP src 6 (absent objective evidence triggers skepticism)'
513	  false_positive: 'Negative CT head is expected and not inconsistent with concussion or soft-tissue injury (record 2). LOW: never a flag alone; must never be summarized as "no injury".'
514	  appendix_c: [2]
515	  examples:
516	    hit: ['CT head negative.', 'No acute osseous abnormality.', 'x-rays unremarkable']
517	    miss: ['CT head shows small hemorrhage']
518	
519	- id: symptom_magnification
520	  pattern: '\b(?:symptom\s+magnification|Waddell(?:''s)?\s+(?:signs?|tests?)|non-?\s?organic\s+(?:signs?|findings?|pain)|inconsistent\s+effort|sub-?\s?maximal\s+effort|poor\s+effort|secondary\s+gain|malinger\w*|exaggerat\w*|pain\s+behaviou?rs?)\b'
521	  flag_type: causation_weakening
522	  strength: high
523	  negatable: true
524	  rationale: 'Credibility attack: defense IMEs and adjusters treat positive Waddell signs/symptom magnification as non-credible, although the signs were not designed to diagnose malingering.'
525	  source: 'Waddell''s signs literature (https://corporate.findlaw.com/litigation-disputes/the-use-of-waddell-in-workers-compensation-claims.html — defense/adjuster use; misuse concerns); AA A9'
526	  false_positive: '"Waddell signs negative" / "no signs of symptom magnification" negated by guard (post-cue "negative" is handled by LLM — add to review).'
527	  appendix_c: []
528	  examples:
529	    hit: ['3/5 Waddell signs positive', 'possible symptom magnification', 'secondary gain issues']
530	    miss: ['magnification views obtained']
531	    negated: ['No evidence of symptom magnification.']
532	
533	- id: inconsistent_history
534	  pattern: '\b(?:inconsistent\s+(?:with|history|reports?|accounts?|statements?)|history\s+(?:is\s+)?(?:inconsistent|unclear|vague|conflicting)|discrepan(?:cy|cies)|conflicting\s+(?:history|reports?|accounts?|dates?)|differs?\s+from\s+(?:prior|previous|the\s+(?:ER|EMS)))\b'
535	  flag_type: causation_weakening
536	  strength: high
537	  negatable: true
538	  rationale: 'Inconsistent histories are a primary impeachment tool; contemporaneous records outweigh later accounts.'
539	  source: 'AA A7; AA src 17'
540	  false_positive: '"Findings consistent with" is not matched (requires "inconsistent"). Negated by guard.'
541	  appendix_c: []
542	  examples:
543	    hit: ['history inconsistent with mechanism', 'discrepancy in date of injury']
544	    miss: ['findings consistent with strain']
545	    negated: ['No discrepancy noted.']
546	
547	- id: litigation_referral
548	  pattern: '\b(?:referred\s+by\s+(?:his|her|their|the\s+patient''s|the)?\s*(?:attorney|lawyer|counsel)|attorney\s+referr\w*|letter\s+of\s+protection|\bLOP\b|lien\s+basis|treating\s+on\s+(?:a\s+)?lien)\b'
549	  flag_type: causation_weakening
550	  strength: medium
551	  negatable: false
552	  rationale: 'Attorney-referred or LOP-funded care is attacked as litigation-driven, and its charges as unreasonable (K&L Auto Crushers made negotiated rates discoverable).'
553	  source: 'research/texas-pi-notes.md §3 (In re K & L Auto Crushers, Tex. 2021); AA src 1 (provider credentials/referral patterns)'
554	  false_positive: '"LOP" may be an unrelated abbreviation in some notes — LLM confirms.'
555	  appendix_c: []
556	  examples:
557	    hit: ['Referred by his attorney.', 'treating under a letter of protection']
558	    miss: ['Referred by PCP.']
559	
560	# ───────────────────────── compliance ─────────────────────────
561	
562	- id: missed_appointments
563	  pattern: '\b(?:missed|skipped|failed\s+to\s+(?:attend|keep|show\s+(?:up\s+)?for|appear\s+for|return\s+for))\s+(?:\w+\s+){0,2}(?:appointments?|appts?|visits?|sessions?|therapy|treatments?|follow-?\s?ups?)\b'
564	  flag_type: compliance
565	  strength: high
566	  negatable: true
567	  rationale: 'Missed care feeds failure-to-mitigate and "not really hurt" arguments; mitigation is the defendant''s burden and outcomes vary, so it is a review flag, not a conclusion.'
568	  source: 'AA A2; AA src 13, src 14 (Herrera v. Madrak; Fletcher v. Simmons); Appendix C record 6'
569	  false_positive: '"Patient reports missing 3 days of work" (record 5) is lost work, a damages mention — "missing" is not in the pattern and "work" is not an appointment noun. "Has not missed any sessions" negated by guard.'
570	  appendix_c: [6]
571	  examples:
572	    hit: ['Discharged from PT after two missed appointments.', 'failed to attend 3 sessions', 'skipped follow-up']
573	    miss: ['Patient reports missing 3 days of work.']
574	    negated: ['Has not missed any sessions.']
575	
576	- id: no_show_cancel
577	  pattern: '\b(?:no-?\s?show(?:ed|s)?|NS\s+x\s?\d|DNKA|did\s+not\s+(?:show|attend|return|keep|present)|cancell?ed\s+(?:\w+\s+){0,2}(?:appointments?|appts?|visits?|sessions?)|rescheduled\s+(?:\w+\s+){0,2}times)\b'
578	  flag_type: compliance
579	  strength: high
580	  negatable: false
581	  rationale: 'Attendance failures documented by the provider.'
582	  source: 'AA A2; AA src 13, src 14'
583	  false_positive: '"Did not show signs of infection" — the pattern requires a bare "did not show" so it WILL fire on that; LLM must check it refers to attendance. Insurer-requested IME no-shows are a different (no-fault) issue.'
584	  appendix_c: []
585	  examples:
586	    hit: ['No-show 2/14.', 'did not return for follow-up', 'cancelled two appointments']
587	    miss: ['showed improvement']
588	
589	- id: discharged_from_care
590	  pattern: '\b(?:discharged|dismissed|released)\s+from\s+(?:PT|physical\s+therapy|therapy|OT|chiropractic(?:\s+care)?|care|treatment|(?:the\s+)?(?:program|practice|clinic))\b|\bself-?\s?discharged?\b'
591	  flag_type: compliance
592	  strength: high
593	  negatable: false
594	  rationale: 'Discharge from therapy before the plan of care is complete creates both a compliance issue and a plan-vs-actual conflict (record 4: 12 visits planned; record 6: discharged at visit 9). Defense reads early discharge as recovery or non-compliance.'
595	  source: 'AA A2; AA src 14; Appendix C records 4 and 6'
596	  false_positive: '"Discharged from PT, goals met" is a good outcome; the LLM decides whether the reason is compliance or completion. ER "discharge summary" headers do not match (require "from PT/therapy/care…").'
597	  appendix_c: [6]
598	  examples:
599	    hit: ['Discharged from PT after two missed appointments.', 'self-discharged from therapy', 'dismissed from the practice']
600	    miss: ['Central ER discharge summary', 'discharged home in stable condition']
601	
602	- id: noncompliance
603	  pattern: '\bnon-?\s?complian(?:t|ce)\b|\bnot\s+(?:being\s+)?complian(?:t|ce)\b|\bpoor\s+(?:compliance|adherence|attendance|follow-?\s?through)\b|\bnon-?\s?adheren(?:t|ce)\b'
604	  flag_type: compliance
605	  strength: high
606	  negatable: false
607	  rationale: 'Explicit provider statement of non-compliance; the strongest mitigation evidence.'
608	  source: 'AA A2; AA src 13, src 14'
609	  false_positive: 'Rare. Already-negative phrasing, so not negatable.'
610	  appendix_c: []
611	  examples:
612	    hit: ['noncompliant with HEP', 'poor attendance', 'not compliant with medications']
613	    miss: ['compliant with plan']
614	
615	- id: against_medical_advice
616	  pattern: '\bagainst\s+medical\s+advice\b|\bleft\s+(?:AMA|without\s+being\s+seen)\b|\bLWBS\b|\beloped\b|\bsigned\s+out\s+AMA\b'
617	  flag_type: compliance
618	  strength: high
619	  negatable: false
620	  rationale: 'Leaving care against advice is used to argue the claimant did not follow medical advice.'
621	  source: 'AA A2; AA src 13 (mitigation); weak direct sourcing — insurer use of AMA in tort mitigation not found (assumption)'
622	  false_positive: 'Bare "AMA" is not matched (American Medical Association, AMA guides to impairment); only "left AMA"/"signed out AMA".'
623	  appendix_c: []
624	  examples:
625	    hit: ['Patient left AMA before CT.', 'left against medical advice']
626	    miss: ['per AMA Guides, 5th edition']
627	
628	- id: medication_nonadherence
629	  pattern: '\b(?:did\s+not|has\s+not|hasn''t|didn''t|never|not)\s+(?:fill(?:ed)?|take|taking|taken|start(?:ed)?|pick(?:ed)?\s+up)\s+(?:\w+\s+){0,2}(?:medications?|meds|prescriptions?|rx|muscle\s+relaxants?)\b|\bstopped\s+taking\b'
630	  flag_type: compliance
631	  strength: medium
632	  negatable: false
633	  rationale: 'Not taking prescribed medication is argued as failure to mitigate or as evidence that pain was not severe.'
634	  source: 'AA A2; AA src 13'
635	  false_positive: 'Stopped due to side effects is a medical reason — LLM records the reason.'
636	  appendix_c: []
637	  examples:
638	    hit: ['did not fill the cyclobenzaprine prescription', 'stopped taking meds']
639	    miss: ['Rx cyclobenzaprine 10 mg.']
640	
641	- id: hep_nonadherence
642	  pattern: '\b(?:not|isn''t|is\s+not|has\s+not\s+been|hasn''t\s+been)\s+(?:doing|performing|completing|following)\s+(?:(?:his|her|their|the)\s+)?(?:home\s+exercises?(?:\s+program)?|HEP|exercises?)\b'
643	  flag_type: compliance
644	  strength: medium
645	  negatable: false
646	  rationale: 'Home-exercise non-adherence is documented by therapists and used in mitigation arguments.'
647	  source: 'AA A2; AA src 14 (home exercises as alternative to formal PT in mitigation case)'
648	  false_positive: 'Already negative phrasing.'
649	  appendix_c: []
650	  examples:
651	    hit: ['not doing HEP', 'is not performing her home exercises']
652	    miss: ['HEP reviewed and performed correctly']
653	
654	- id: declined_treatment
655	  pattern: '\b(?:declined|refused|deferred|declines|refuses)\s+(?:\w+\s+){0,2}(?:treatment|therapy|PT|injections?|ESI|referral|surgery|MRI|imaging|medications?|follow-?\s?up)\b'
656	  flag_type: compliance
657	  strength: medium
658	  negatable: false
659	  rationale: 'Refusing recommended care is argued as failure to mitigate.'
660	  source: 'AA A2; AA src 13, src 14 (Fletcher: personal reasons weighed)'
661	  false_positive: 'Reasonable refusals (cost, fear of injections, pregnancy) defeat mitigation in some courts — LLM records the stated reason. "Insurance declined" is a payer action, not the patient''s.'
662	  appendix_c: []
663	  examples:
664	    hit: ['declined epidural steroid injection', 'refused MRI due to claustrophobia']
665	    miss: ['Recommend cervical epidural steroid injection.']
666	
667	- id: lost_to_follow_up
668	  pattern: '\b(?:lost\s+to\s+follow-?\s?up|not\s+(?:been\s+)?seen\s+since|last\s+seen\s+(?:on\s+|in\s+)?(?:\d|[A-Z][a-z]+)|returns?\s+after\s+(?:a\s+)?(?:\d+|several|many|few)\s+(?:weeks?|months?)|first\s+visit\s+(?:in|since)\s+(?:\d+|several|many)\s+(?:weeks?|months?))'
669	  flag_type: compliance
670	  strength: medium
671	  negatable: false
672	  rationale: 'Provider language that confirms a gap in care; corroborates the code-computed gap flag and sometimes states a reason.'
673	  source: 'AA A1; AA src 1, src 4, src 5'
674	  false_positive: 'Code computes gaps from dates; this entry only attaches the provider''s own words. Not negatable.'
675	  appendix_c: []
676	  examples:
677	    hit: ['lost to follow-up', 'returns after 3 months', 'not seen since March']
678	    miss: ['seen today']
679	
680	- id: plan_not_completed
681	  pattern: '\b(?:did\s+not\s+complete|incomplete|without\s+completing|prior\s+to\s+completing|before\s+completing)\s+(?:(?:the|his|her)\s+)?(?:plan\s+of\s+care|course|program|therapy|treatment|PT)\b|\bplan\s+of\s+care\s*:?\s*\d+\s+visits?\b'
682	  flag_type: compliance
683	  strength: medium
684	  negatable: false
685	  rationale: 'Planned vs completed care: record 4 "Plan of care: 12 visits" vs record 6 discharge at visit 9 is a treatment-plan discrepancy (Appendix C conflict) — this entry tags the planned count so the conflict engine can compare.'
686	  source: 'AA A2; Appendix C (treatment-plan discrepancy, records 4 and 6)'
687	  false_positive: 'The planned-count branch is not itself a problem; it is the second half of a plan-vs-actual comparison done in code.'
688	  appendix_c: [4]
689	  examples:
690	    hit: ['Plan of care: 12 visits.', 'did not complete the course of therapy']
691	    miss: ['Charge per visit $185.']
692	
693	sources:
694	  - 'research/adjuster-attacks.md (attack map A1–A11 and sources 1–18) — all AA src N references'
695	  - 'research/texas-pi-notes.md — Texas law (Haygood, §18.001, K&L Auto Crushers)'
696	  - 'research/chronology-practice.md — CP src N references'
697	  - 'Chapman WW et al., "A simple algorithm for identifying negated findings and diseases in discharge summaries," J Biomed Inform 34:301–310 (2001) — NegEx: phrase-list negation with a word window; 94.5% specificity (via search index; the PDF link returned 404 when fetched). https://www.bohrium.com/paper-details/a-simple-algorithm-for-identifying-negated-findings-and-diseases-in-discharge-summaries/812456728187633665-10652'
698	  - 'Chapman BE et al., "Document-level classification of CT pulmonary angiography reports based on an extension of the ConText algorithm," J Biomed Inform (2011) — pyConText builds on NegEx lists; "but"/"although" terminate negation scope. https://pmc.ncbi.nlm.nih.gov/articles/PMC3164892'
699	  - 'FindLaw, "The Use of Waddell in Workers'' Compensation Claims" — defense/adjuster use of Waddell signs as non-credibility; signs not designed to diagnose malingering. https://corporate.findlaw.com/litigation-disputes/the-use-of-waddell-in-workers-compensation-claims.html'
700	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:47.806Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/lexicon_selfcheck.py"
}
````

### User / tool · 2026-11-02T00:31:47.814Z

**tool result**
````
1	"""Self-check for app/llm/lexicon.yaml (T-009). Reference only — not product code.
2	
3	Run: .venv/bin/python research/lexicon_selfcheck.py
4	Checks: YAML parses; required fields; every regex compiles; examples behave (hit / miss / negated) under the
5	reference negation guard below; reports hits on the Appendix A sample records vs each entry's `appendix_c`.
6	The backend may implement the guard differently but should pass the same examples.
7	"""
8	import re
9	import sys
10	from pathlib import Path
11	
12	import yaml
13	
14	ROOT = Path(__file__).resolve().parents[1]
15	LEX = ROOT / "app" / "llm" / "lexicon.yaml"
16	REQUIRED = ("id", "pattern", "flag_type", "rationale", "source", "false_positive", "strength", "negatable")
17	
18	# Appendix A sample records (SYNTHETIC, spec/SPEC.md), excerpts only.
19	SAMPLE = {
20	    1: "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER.",
21	    2: "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240.",
22	    3: "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved.",
23	    4: "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185.",
24	    5: "Pain 4/10, improving. Patient reports missing 3 days of work.",
25	    6: "Discharged from PT after two missed appointments. Pain 3/10.",
26	    7: "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19.",
27	    8: "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150.",
28	    9: "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision.",
29	}
30	
31	TOKEN = re.compile(r"[\w'/-]+|;")
32	
33	
34	def _norm(tokens):
35	    return " " + " ".join(t.lower() for t in tokens) + " "
36	
37	
38	def _strip_pseudo(s, pseudo):
39	    for p in pseudo:
40	        s = s.replace(" " + p.lower() + " ", " ")
41	    return s
42	
43	
44	def _has_cue(s, cues):
45	    return any((" " + c.lower() + " ") in s for c in cues)
46	
47	
48	def negated(text, start, end, neg):
49	    """Reference NegEx-style guard: pre-cue within window before the hit (same sentence, no terminator)."""
50	    sent_start = max(text.rfind(". ", 0, start) + 1, 0)
51	    sent_end = text.find(". ", end)
52	    sent_end = len(text) if sent_end == -1 else sent_end
53	    before = TOKEN.findall(text[sent_start:start])
54	    after = TOKEN.findall(text[end:sent_end])
55	    terms = [t.lower() for t in neg["terminators"]]
56	    # cut the before-window at the last terminator
57	    for i in range(len(before) - 1, -1, -1):
58	        if before[i].lower() in terms:
59	            before = before[i + 1:]
60	            break
61	    for i, t in enumerate(after):
62	        if t.lower() in terms:
63	            after = after[:i]
64	            break
65	    w = neg["window_tokens"]
66	    pre = _strip_pseudo(_norm(before[-w:]), neg["pseudo_negations"])
67	    post = _strip_pseudo(_norm(after[:w]), neg["pseudo_negations"])
68	    return _has_cue(pre, neg["pre_cues"]) or _has_cue(post, neg["post_cues"])
69	
70	
71	def fires(entry, rx, text, neg):
72	    for m in rx.finditer(text):
73	        if entry["negatable"] and negated(text, m.start(), m.end(), neg):
74	            continue
75	        return True
76	    return False
77	
78	
79	def main():
80	    lex = yaml.safe_load(LEX.read_text())
81	    neg = lex["negation"]
82	    entries = lex["entries"]
83	    errors = []
84	    ids = set()
85	    for e in entries:
86	        for f in REQUIRED:
87	            if f not in e or e[f] in (None, ""):
88	                errors.append(f"{e.get('id')}: missing {f}")
89	        if e["id"] in ids:
90	            errors.append(f"duplicate id {e['id']}")
91	        ids.add(e["id"])
92	        if e["flag_type"] not in lex["flag_types"]:
93	            errors.append(f"{e['id']}: bad flag_type {e['flag_type']}")
94	        try:
95	            rx = re.compile(e["pattern"], re.IGNORECASE)
96	        except re.error as exc:
97	            errors.append(f"{e['id']}: regex error {exc}")
98	            continue
99	        ex = e.get("examples", {})
100	        for s in ex.get("hit", []):
101	            if not fires(e, rx, s, neg):
102	                errors.append(f"{e['id']}: should HIT: {s!r}")
103	        for s in ex.get("miss", []):
104	            if rx.search(s):
105	                errors.append(f"{e['id']}: should MISS: {s!r}")
106	        for s in ex.get("negated", []):
107	            if not rx.search(s):
108	                errors.append(f"{e['id']}: negated example does not match regex: {s!r}")
109	            elif fires(e, rx, s, neg):
110	                errors.append(f"{e['id']}: should be NEGATED: {s!r}")
111	        e["_rx"] = rx
112	
113	    print(f"entries: {len(entries)}  by type: " + ", ".join(
114	        f"{t}={sum(1 for e in entries if e['flag_type'] == t)}" for t in lex["flag_types"]))
115	    print("\nSample-case hits (record: entry[strength])")
116	    mismatch = []
117	    for n, text in SAMPLE.items():
118	        hits = [e for e in entries if "_rx" in e and fires(e, e["_rx"], text, neg)]
119	        print(f"  {n}: " + ", ".join(f"{e['id']}[{e['strength']}]" for e in hits))
120	        for e in entries:
121	            exp = n in (e.get("appendix_c") or [])
122	            got = e in hits
123	            if exp != got:
124	                mismatch.append(f"record {n}: {e['id']} expected={exp} got={got}")
125	    if mismatch:
126	        print("\nappendix_c mismatches:\n  " + "\n  ".join(mismatch))
127	    if errors:
128	        print("\nERRORS:\n  " + "\n  ".join(errors))
129	    ok = not errors and not mismatch
130	    print("\nRESULT:", "PASS" if ok else "FAIL")
131	    return 0 if ok else 1
132	
133	
134	if __name__ == "__main__":
135	    sys.exit(main())
136	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:51.267Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n \"Appendix\" spec/SPEC.md | head; ls spec docs personas 2>&1",
 "description": "Locate spec appendices and persona files"
}
````

### User / tool · 2026-11-02T00:31:51.361Z

**tool result**
````
1:## Appendix A — The Zlayt spec (verbatim)
docs:
CONTRACT.md
LLM_VS_CODE.md
RUNBOOK.md

personas:
accessibility.md
chaos-tester.md
claims-adjuster.md
hiring-panel.md
installer.md
legal-nurse.md
litigation-lead.md
paralegal.md
privacy-compliance.md
product-manager.md
security.md
staff-engineer.md
ux-designer.md

spec:
REQUIREMENTS.md
SAMPLE_CASE_TRUTHS.md
SPEC.md
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:51.915Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/texas-pi-notes.md"
}
````

### User / tool · 2026-11-02T00:31:51.923Z

**tool result**
````
1	# Texas PI norms relevant to billed charges and medical records
2	
3	Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
4	Scenario: Zinda Law Group (Austin), fictional client Jordan Rivera, Austin MVA 2026-01-09. **Not legal advice**;
5	this is product research so the prototype does not mislead a Texas paralegal.
6	
7	Method note: statutes.capitol.texas.gov renders only navigation to our fetch tool, so statute text was read via
8	mirrors (rulesofcivilprocedure.com, texas.public.law) and cross-checked against Texas Supreme Court opinions
9	(the In re Allstate PDF text was extracted and read directly). Each item says how it was verified.
10	
11	## 1. Paid or incurred — CPRC §41.0105 (verified)
12	
13	- **Rule.** Recovery of medical expenses is limited to "the amount actually paid or incurred by or on behalf
14	  of the claimant." Enacted 2003 (tort reform). (Src 1, 2.)
15	- **Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. July 1, 2011).** Amounts a provider has no right to collect
16	  (e.g., insurer-contracted write-offs) are not recoverable, and "only evidence of recoverable medical
17	  expenses is admissible at trial"; the jury is not told about insurance adjustments (collateral-source rule
18	  still applies). (Src 1 — full text read.)
19	- **Product consequence.** Records show **billed charges**. The prototype must label every dollar figure
20	  "billed (as written in record)" and never call the running total "medical damages", "specials owed" or
21	  "recoverable". Paid/adjusted amounts usually come from billing ledgers/EOBs, not clinical notes — out of scope.
22	
23	## 2. Medical-expense affidavits — CPRC §18.001 (verified, current version)
24	
25	- **Effect (b).** Absent a timely counteraffidavit, an affidavit that charges were reasonable and services
26	  necessary is *sufficient evidence* to support a finding on those points — and since the 2019 amendment
27	  "is not evidence of and does not support a finding of the causation element." (Src 3; Allstate fn. confirms
28	  the 2019 change, src 4.)
29	- **Who/what (c).** Made by the provider or the person in charge of its records, with an **itemized statement
30	  of the service and charge**. (Src 3.)
31	- **Deadlines (d),(e).** Serve by the earlier of 90 days after the defendant answers or the expert-designation
32	  deadline; counteraffidavit by the earliest of 120 days after answer or the designation deadlines.
33	  Supplementation (h): affidavit ≥60 days before trial, counteraffidavit ≥30. (Src 3.) Applies to actions
34	  commenced on/after 2019-09-01 (src 4).
35	- **Counteraffidavit (f).** Must give reasonable notice of the basis and be made by a qualified person; may not
36	  controvert causation. (Src 3.) *In re Allstate Indemnity Co.*, 622 S.W.3d 870 (Tex. 2021): §18.001 is
37	  "purely procedural," "streamline[s]" proof of reasonableness/necessity; a counteraffiant need not practice in
38	  the same specialty; striking a counteraffidavit and barring all contrary evidence was an abuse of discretion.
39	  (Src 4 — full text extracted and read.)
40	- **Product consequence.** (a) An itemized-by-provider charge list with record citations is the raw material
41	  for §18.001 affidavits — our "billed charges" list should group by provider and keep each source excerpt.
42	  (b) §18.001 says nothing about causation → the chronology can't lean on billing to prove causation either.
43	  (c) Deadlines are lawsuit-stage, not pre-suit demand-stage; the prototype doesn't compute them. (Scope cut.)
44	
45	## 3. Discovery of negotiated rates / letters of protection (verified via secondary)
46	
47	- *In re K & L Auto Crushers, LLC*, 627 S.W.3d 239 (Tex. 2021): providers' negotiated rates with insurers are
48	  relevant to reasonableness of the plaintiff's charges and discoverable (narrowed requests); the Court notes
49	  letter-of-protection (LOP) arrangements. *In re ExxonMobil Corp.* (Tex. Nov. 2021) followed it. (Src 5, 6.)
50	- **Product consequence.** Billed charges on LOP-treated care will be challenged as unreasonable. The tool should
51	  not imply a billed amount is reasonable; it reports what the record says.
52	
53	## 4. Hospital and EMS liens — Property Code ch. 55 (partly verified)
54	
55	- §55.004(b): a hospital lien is for the lesser of charges for the first 100 days of hospitalization or 50% of
56	  the patient's recovery (or the awarded hospital charges less a proportional share of fees). §55.004(f): an
57	  EMS lien may not exceed $1,000 and covers services within 72 hours after the accident. (Src 7 — mirror text.)
58	- Rivera has an EMS transport (record 1, no charge shown) and an ER visit ($6,240). **Assumption:** whether
59	  Central ER/Austin EMS filed liens is unknowable from clinical excerpts; lien tracking is a settlement-stage
60	  task, out of scope. County-population and filing-requirement details were **not verified** (official page
61	  unreadable to our tool; secondary sources conflict).
62	
63	## 5. Records as evidence — TRE 902(10) business-records affidavits (verified via secondary)
64	
65	- Medical records are commonly proved by a business-records affidavit under Tex. R. Evid. 902(10) (with notice
66	  to other parties); since 2014 they generally need not be filed with the court in advance (SB 679, 83rd Leg.).
67	  (Src 8, 9.)
68	- **Product consequence.** Firms think in terms of *records sets with affidavits*. Our "record #" + verbatim
69	  excerpt is the in-app analogue of a Bates/page cite. Real deployment should carry Bates numbers. (Assumption.)
70	- Not verified: how TRE 803(4) (statements for medical diagnosis) applies to "patient states…" lines. Treat
71	  patient-attributed causation statements as history, not opinion (Guevara, adjuster-attacks.md A6).
72	
73	## 6. Causation proof (verified via primary summaries)
74	
75	- Expert testimony is generally required to connect an accident to medical conditions outside lay knowledge
76	  (*Guevara v. Ferrer*, 247 S.W.3d 662 (Tex. 2007)); proof must reach reasonable medical probability, not
77	  possibility (*Jelinek v. Casas*, 328 S.W.3d 526 (Tex. 2010)); evidence of an alternative cause such as a
78	  second accident is admissible (*JLG Trucking v. Garza*, 466 S.W.3d 157 (Tex. 2015)). Details and URLs in
79	  adjuster-attacks.md srcs 9–11.
80	
81	## 7. Other Texas context (secondary only — not needed by the prototype)
82	
83	- Limitations: generally two years for personal injury, CPRC §16.003. Proportionate responsibility: a claimant
84	  more than 50% responsible recovers nothing, otherwise damages reduced by percentage (CPRC §33.001, §33.012).
85	  (Src 10, 11 — secondary; verify before relying.) Texas is an at-fault (tort) auto state; PIP is optional
86	  coverage. **Assumption**, not researched further: pre-suit demands go to the at-fault driver's liability carrier.
87	- Stowers (time-limited policy-limits demands) affects demand-letter *strategy*, not the chronology — not researched.
88	
89	## Assumptions where sources are thin
90	
91	- T1. A pre-suit demand to an adjuster is not bound by §18.001 or Haygood (those govern trial evidence), but
92	  adjusters evaluate with trial in mind, so they discount billed charges to expected paid amounts. (Inference
93	  from srcs 1, 4, 5; no adjuster source states it directly.)
94	- T2. Zinda (an Austin PI firm) sends demands with an itemized medical-specials table. (Industry practice from
95	  chronology-practice.md; not verified for Zinda specifically.)
96	- T3. Records in the demand package are the same records later proved by 902(10)/18.001 affidavits. (Inference.)
97	
98	## Sources
99	
100	1. Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011) — https://caselaw.findlaw.com/tx-supreme-court/1573065.html — §41.0105 limits recovery to amounts paid or incurred; unadjusted charges inadmissible; §18.001 is procedural. (Full text read.)
101	2. Jim Adler & Associates, "What are paid and incurred medical expenses?" (2017) — https://www.jimadler.com/blog/what-are-paid-and-incurred-medical-expenses/ — Texas plaintiff firm's explanation of §41.0105 in practice. (Secondary; via search snippet.)
102	3. Tex. Civ. Prac. & Rem. Code §18.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-18-001/ — Current text: sufficiency, itemized statement, 90/120-day deadlines, counteraffidavit limits, not evidence of causation. (Mirror of statute; cross-checked with src 4.)
103	4. In re Allstate Indemnity Co., 622 S.W.3d 870 (Tex. 2021) — https://www.txcourts.gov/media/1452189/200071.pdf — §18.001 is procedural; 2019 amendments (Acts 2019, 86th Leg., ch. 779) made affidavits non-evidence of causation and changed deadlines for suits after 2019-09-01. (Full text extracted and read.)
104	5. In re K & L Auto Crushers, LLC, 627 S.W.3d 239 (Tex. 2021) — https://law.justia.com/cases/texas/supreme-court/2021/19-1022.html — Negotiated insurer rates are relevant and discoverable on reasonableness of charges. (Primary; read via summaries.)
105	6. Claims Journal, "Texas Supreme Ct. Approves Discovery for Documents Related to Medical Charges" (2021) — https://amp.claimsjournal.com/news/southcentral/2021/06/02/304050.htm — Insurer-side press on K&L's practical effect. (Trade press; via search snippet.)
106	7. Tex. Prop. Code §55.004 (mirror) — https://texas.public.law/statutes/tex._prop._code_section_55.004 — Hospital lien lesser-of 100-day charges / 50% of recovery; EMS lien ≤$1,000 within 72 hours. (Mirror.)
107	8. Texas Rules of Evidence 902 — https://texasevidence.com/rule-902/ — 902(10) business-records affidavit admits records without live custodian; notice required; form for medical expenses. (Secondary reference.)
108	9. Senate Research Center bill analysis, SB 679 (83rd Leg.) — https://capitol.texas.gov/tlodocs/83R/analysis/pdf/SB00679F.pdf — Records served with a 902(10) affidavit need not be filed with the court beforehand. (Official legislative analysis; via search snippet.)
109	10. Tex. Civ. Prac. & Rem. Code §33.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-33-001/ — Claimant >50% responsible may not recover. (Mirror; via search snippet.)
110	11. Blass Law, "Texas 51 percent rule" — https://www.blasslaw.com/faqs/texas-51-percent-rule-comparative-fault/ — Practitioner explanation of modified comparative fault and the two-year limitations period. (Plaintiff firm.)
111	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:52.418Z

**tool call — Read**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/chronology-practice.md"
}
````

### User / tool · 2026-11-02T00:31:52.427Z

**tool result**
````
1	# How PI firms build treatment chronologies for demand packages
2	
3	Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02 with WebSearch/WebFetch.
4	Scope: what a personal-injury (PI) paralegal produces before a demand letter, what each entry contains, and
5	what that implies for the prototype. Synthetic case only (Jordan Rivera, spec Appendix A).
6	
7	**Source quality warning.** Almost all public "how to build a medical chronology" material is written by
8	vendors that sell chronology services or software (EvenUp, Tavrn, LezDo TechMed, InPractice, CaseMark). There is
9	no bar-association or AALNC published standard for PI chronologies that we could find (see source 9). Treat
10	the conventions below as *industry practice*, not rules. Where all vendors agree, we treat it as reliable.
11	
12	## 1. What the artifact is
13	
14	- **Chronology vs. summary.** A *chronology* orders every encounter by date of service; a *medical summary*
15	  groups by provider, body part or injury and reads as narrative. Firms use both, often the chronology first
16	  and the summary as the demand letter's "medical treatment" section. (Sources 1, 2.)
17	- **When it is built.** Usually after the client reaches maximum medical improvement (MMI) or finishes
18	  treatment, so the demand can state total specials; earlier for policy-limits cases. (Source 2.) Our sample
19	  case is mid-treatment (an epidural steroid injection is only *recommended* on 2026-06-12) — the export must
20	  not imply treatment is complete. **Assumption** (see ASSUMPTIONS-proposed P-04).
21	- **Who builds it.** Paralegal or case manager; nurse/LNC on larger cases; attorney reviews and signs the
22	  demand. Chronologies "do not decide causation" — they display the documented sequence; causation opinions
23	  belong to physicians and lawyers. (Sources 3, 9.)
24	
25	## 2. Fields per entry (consensus across sources)
26	
27	| Field | Sources | In the Zlayt must-have? | Prototype note |
28	|---|---|---|---|
29	| Date of service | 1, 2, 4 | yes | Code-parsed, one format throughout (source 1 insists on a single date format) |
30	| Provider / facility | 1, 2, 4 | yes | As written; name variants are a conflict signal |
31	| Encounter type (ER, PCP, PT, imaging, pain mgmt) | 1 | no | Cheap to derive from source line; optional column |
32	| Chief complaint / findings / diagnosis | 1, 2 | summary | One-line summary must not upgrade or downgrade a finding |
33	| Treatment, referrals, plan | 1, 2 | summary | "Recommend ESI" ≠ "received ESI" |
34	| Source page/citation | 1, 4 | **exact excerpt** | Source 1: "page number should never be left blank." Our equivalent is the verbatim excerpt + record # |
35	| Charges | 2, 4, 5 | yes | Itemized, cross-checked against treatment dates (source 5) |
36	| Missing records / gaps | 1, 2 | gap flag | Log, explain, request supplemental records |
37	
38	## 3. Workflow steps paralegals follow
39	
40	1. Request records from every provider (HIPAA authorization), with a broad date range — including *prior*
41	   records, because missing baseline records invite pre-existing-condition arguments. (Sources 1, 6.)
42	2. Index what arrived vs. what is outstanding. (Source 1.)
43	3. Order by date of service; extract per-entry fields. (Sources 1, 2.)
44	4. Flag gaps, pre-existing conditions, and contradictions *for attorney review*; distinguish aggravation of a
45	   prior condition from a new injury. (Source 1.)
46	5. Cross-check bills against treatment dates; a bill with no matching visit (or a visit with no bill) is a
47	   finding. (Source 5.)
48	6. Verify every entry against its source before it goes to the attorney. (Sources 1, 4.)
49	7. Keep it updated as treatment continues. (Source 2.)
50	
51	Step 6 is the one the Zlayt brief cares about ("she reviews rather than trusts"). Every vendor sells
52	"source-linked" chronologies precisely because unverifiable entries cost credibility with adjusters (source 7).
53	
54	## 4. Why accuracy matters to the adjuster (bridge to adjuster-attacks.md)
55	
56	Practitioners say the package should be *easy to verify*, not just complete (source 5). Concealing a prior
57	condition or a gap "triggers credibility discounts across the entire case evaluation" (source 6, plaintiff-side
58	vendor claim). The implication for us: **surfacing** a gap or prior condition to the paralegal is the product's
59	job; deciding whether to explain it in the letter is the lawyer's job.
60	
61	## 5. What this means for the prototype (design requirements)
62	
63	- R1. Each entry carries record #, date, provider, one-line summary, verbatim excerpt. No entry without an excerpt.
64	- R2. Dates rendered in one format (ISO `YYYY-MM-DD`), parsed by code.
65	- R3. The summary must preserve hedges: "may represent degenerative change" stays hedged; "recommend" stays a
66	  recommendation; "patient states" stays attributed to the patient.
67	- R4. Gaps, prior conditions and conflicts are *flags for review*, not edits to the timeline and not
68	  conclusions in the export.
69	- R5. Charges are listed per source and cross-referenced to an entry; rates and unclear amounts are listed but
70	  not totaled (Appendix C).
71	- R6. Export header should say the chronology is through the last record date and that treatment may be
72	  ongoing if the last record contains a plan/recommendation. (Assumption P-04.)
73	- R7. A "missing records" note is out of scope for the prototype (we cannot know what wasn't sent) — record as
74	  a scope cut candidate for the orchestrator.
75	
76	## Sources
77	
78	1. EvenUp, "How to Prepare a Medical Chronology for Injury Claims" — https://evenuplaw.com/guides/how-to-prepare-medical-chronology — Fields per entry, never-blank source page, single date format, log gaps and pre-existing conditions, verify every entry before attorney review. (Vendor.)
79	2. EvenUp, "What is a Medical Summary?" — https://evenuplaw.com/guides/what-is-a-medical-summary — Summary vs chronology distinction; summary usually drafted after MMI/completion; itemized expenses and missing-records list; must be updated as treatment continues. (Vendor; content via search snippet.)
80	3. LezDo TechMed, "Why Legal Nurse Consultants Use Medical Chronologies" — https://www.lezdotechmed.com/blog/why-legal-nurse-consultants-use-medical-chronologies-for-medical-record-review — A chronology shows the documented sequence; qualified professionals, not the chronology, evaluate causation. (Vendor.)
81	4. Tavrn, "What is a medical chronology and how is it used" — https://www.tavrn.ai/blog/what-is-a-medical-chronology-and-how-is-it-used — Chronology contents (date of injury, providers, dates, tests) and its use in demand packages. (Vendor; via search snippet.)
82	5. Tavrn, "Demand letter preparation" — https://www.tavrn.ai/blog/demand-letter-preparation.md — Cross-checking billing against the treatment timeline is a paralegal task; the package should be easy to verify. (Vendor; via search snippet.)
83	6. Tavrn, "Legal demand letter best practices" — https://www.tavrn.ai/blog/legal-demand-letter-best-practices — Concealing pre-existing conditions draws credibility discounts; missing baseline records invite pre-existing arguments; absent objective findings trigger skepticism. (Vendor.)
84	7. EvenUp, "5 Steps to Mitigate Treatment Gaps and Preserve Case Value" — https://evenuplaw.com/blog/mitigate-treatment-gaps-preserve-case-value — Vendor claims gaps can reduce settlement value up to 20%; **unverified, vendor benchmark**. Useful only as a signal that firms care.
85	8. SF Bar, "Paralegal corner: collaboration of LNCs with paralegals and attorneys" — https://www.sfbar.org/blog/paralegal-corner-collaboration-of-legal-nurse-consultants-with-paralegals-and-attorneys/ — Paralegals and LNCs split record work: paralegal organizes, LNC interprets clinical meaning. (Bar-association blog; via search snippet.)
86	9. AALNC, "What is an LNC" brochure — https://www.aalnc.org/Portals/0/Docs/About/What%20is%20an%20LNC%20Brochure_Final.pdf — AALNC has a Code of Ethics but we found **no published AALNC chronology standard**; chronology conventions are industry practice. (Professional association.)
87	10. Claims Journal, C. Tidball, "How to Review Bodily Injury Demands" (2013) — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — The adjuster-side mirror image: what reviewers check in the chronology the paralegal sends (timing, gaps, priors, objective findings, billing vs SOAP notes). (Insurance trade press — the only non-plaintiff source here.)
88	
89	Assumptions where sources are thin: no source states *how long* paralegals spend per chronology from
90	independent data (vendors claim "hours"; the Zlayt brief itself says "hours"). We use the brief's word, not a number.
91	
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:53.263Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat research/ASSUMPTIONS-proposed.md memory/GLOSSARY.md",
 "description": "Show proposed assumptions and glossary"
}
````

### User / tool · 2026-11-02T00:31:53.341Z

**tool result**
````
# Proposed PI-practice assumptions for memory/ASSUMPTIONS.md

Card: T-008 · Author: researcher (instance A). The orchestrator owns memory/ASSUMPTIONS.md; these are proposals.
Each has evidence (research file + source #) and a confidence. CP / AA / TX = chronology-practice / adjuster-attacks / texas-pi-notes.

| ID | Proposed assumption | Evidence | Confidence | Refines |
|---|---|---|---|---|
| P-01 | The paralegal assembles the chronology; an LNC may interpret clinical meaning on larger cases; the attorney decides what goes in the demand and signs it. | CP src 1, 8, 9 | Medium (vendor + bar blog) | A-101 |
| P-02 | A treatment gap is measured between consecutive dates of service across **all** providers (case-level), and the 30-day threshold comes from the Zlayt spec, not an industry rule — make it configurable. | AA src 1, 4, 5 (no source sets a number); spec | High for "case-level"; threshold is spec-given | A-102 |
| P-03 | The chronology feeds the medical-treatment section of a **pre-suit** demand to the at-fault driver's liability carrier (Texas is an at-fault state). | CP src 5; TX §7 | Medium | A-103 |
| P-04 | Demands are usually sent after MMI/completion; the Rivera records are mid-treatment (ESI only recommended), so the export must not imply treatment is complete. | CP src 2; record 9 | Medium | new |
| P-05 | Dollar amounts in clinical notes are **billed** charges; the tool must never label the total "damages" or "recoverable" because Texas limits recovery to paid/incurred amounts (Haygood). | TX src 1 | High (primary law) | new |
| P-06 | Surfacing a gap, prior condition or conflict is the tool's job; deciding whether and how to explain it in the letter is the attorney's. Hiding a known weakness costs credibility with adjusters. | CP src 1; AA src 5, 15 | Medium-high | new |
| P-07 | A patient's statement that symptoms began after the collision is history, not a causation opinion; Texas generally requires expert testimony for causation. The tool attributes it ("patient states") and never restates it as fact. | AA src 9, 11 | High (primary law) | new |
| P-08 | Hedged imaging language ("may represent degenerative change; correlate clinically") is equivocal by design; adjusters read it as pre-existing, plaintiffs as aggravation. The tool preserves the hedge verbatim and flags it. | AA src 6, 7, 8 | High | new |
| P-09 | Missed appointments/early discharge are review flags (mitigation is the defendant's burden and outcomes vary), not conclusions. | AA src 13, 14 | Medium | new |
| P-10 | A second, different accident date in any record is material — defense uses it to suggest a different incident (JLG Trucking). Both dates must be surfaced; neither is "corrected". | AA src 10, 17 | High | new |
| P-11 | A prior condition in a **different body region** (2023 low back vs 2026 neck) is still surfaced; relevance is the paralegal's call. | AA src 2, 15; Appendix C | Medium | new |
| P-12 | Firms cite records by Bates/page; the prototype's record # + verbatim excerpt stands in for that. | TX src 8; CP src 1 | Low-medium (assumption) | new |
| P-13 | Paralegals at PI firms are not covered by a single chronology standard; conventions vary by firm, so the export format should be plain, editable text, not a fixed template. | CP src 9 (no standard found) | Medium | new |

Not proposed (insufficient evidence): any number for time spent per chronology or for settlement-value impact of
gaps (only a vendor's "up to 20%" claim, AA/CP src 7).
# GLOSSARY (researcher owns)

One line each. Source = a research file + source number (URLs live there), or **assumption** when no source
pins it down. CP = research/chronology-practice.md · AA = research/adjuster-attacks.md · TX = research/texas-pi-notes.md · PHI = research/phi-and-ai-supervision.md.

## Practice and documents
- **Demand letter / demand package** — pre-suit letter (plus records, bills, chronology) to the at-fault party's liability insurer stating liability, damages and a settlement demand. Source: CP src 5, 6.
- **Treatment chronology** — date-ordered list of every medical encounter with provider, findings, charges and a citation to the source record. Source: CP src 1.
- **Medical summary** — narrative grouped by provider/injury rather than date; often the demand letter's treatment section. Source: CP src 2.
- **Medical specials (specials)** — economic damages for medical expenses, itemized by provider. Source: CP src 2 (itemized expenses); term usage: **assumption** (common PI usage, no single cited definition).
- **MMI (maximum medical improvement)** — point where further treatment is not expected to improve the condition; demands are usually sent after it. Source: CP src 2.
- **Records index / missing records log** — list of records requested vs received. Source: CP src 1.
- **Bates number** — sequential page stamp used to cite records in a production; our "record #" plays this role. Source: **assumption** (standard litigation practice, not researched).
- **Letter of protection (LOP)** — attorney's letter promising a provider payment from any recovery, so an uninsured client can treat; defense attacks LOP charges as inflated. Source: TX src 5.
- **Adjuster** — insurer employee who evaluates and negotiates the claim. Source: AA src 1.
- **Colossus** — proprietary claim-valuation software used by some carriers; scores injuries, treatment duration, objective findings (details second-hand). Source: AA src 3.
- **ISO ClaimSearch** — Verisk database of prior claims adjusters use to find prior/subsequent injuries. Source: AA src 2.
- **Legal nurse consultant (LNC)** — registered nurse who interprets medical records for attorneys; does not practice law. Source: CP src 8, 9.

## Flags and attacks
- **Gap in treatment** — period without care between dates of service; adjusters argue recovery or an intervening cause. Prototype threshold >30 days is the Zlayt spec's, not an industry rule. Source: AA src 1, 4.
- **Pre-existing condition** — injury or condition documented before the incident; defense argues it, not the crash, explains symptoms. Source: AA src 2, 15.
- **Aggravation (of a pre-existing condition)** — worsening of a prior condition by the incident; compensable for the worsening, argued separately from a new injury. Source: CP src 1.
- **Degenerative change** — age-related spinal wear (bulge, protrusion, disc desiccation) common in asymptomatic adults. Source: AA src 6.
- **Disc protrusion / bulge** — imaging descriptions of disc material extending beyond the vertebral margin; protrusion is focal, bulge is broad. Source: AA src 6 (prevalence); definitions **assumption** (standard radiology usage, not separately cited).
- **Hedge / equivocal language** — wording such as "may represent", "cannot be excluded", "correlate clinically" that leaves interpretation to the clinician. Source: AA src 7, 8.
- **Reasonable medical probability** — Texas causation standard (more likely than not); possibility is insufficient. Source: AA src 11.
- **Intervening (alternative) cause** — another event, e.g. a second accident, that could explain the injury. Source: AA src 10.
- **Failure to mitigate** — affirmative defense that the claimant's conduct (e.g., skipped therapy) increased damages; defendant bears the burden. Source: AA src 13, 14.
- **Subjective vs objective findings** — patient-reported symptoms (pain scores) vs measured or imaged findings (ROM, MRI); adjusters weight objective higher. Source: AA src 1, 18.
- **Patient self-report** — history recorded as "patient states/reports"; records what the patient said, not a physician's causation opinion. Source: AA src 9.
- **IME / defense medical exam** — exam or record review by a defense-retained physician, often attributing symptoms to degeneration. Source: AA src 16.

## Texas law
- **Paid or incurred (CPRC §41.0105)** — recovery of medical expenses limited to amounts actually paid or incurred by/for the claimant. Source: TX src 1.
- **Haygood v. De Escabedo (Tex. 2011)** — only evidence of recoverable (paid/incurred) expenses is admissible; write-offs not recoverable. Source: TX src 1.
- **§18.001 affidavit** — provider/records-custodian affidavit with itemized charges; uncontroverted, it is sufficient evidence of reasonableness and necessity, never of causation. Source: TX src 3, 4.
- **Counteraffidavit (§18.001(f))** — opposing party's timely affidavit by a qualified person giving reasonable notice of why charges are unreasonable/unnecessary. Source: TX src 3, 4.
- **Business-records affidavit (TRE 902(10))** — custodian affidavit that makes medical records admissible without live testimony. Source: TX src 8.
- **Hospital / EMS lien (Prop. Code ch. 55)** — statutory lien on the patient's recovery for emergency/hospital care, capped (EMS ≤ $1,000). Source: TX src 7.
- **Proportionate responsibility (CPRC ch. 33)** — damages reduced by claimant's fault share; barred above 50%. Source: TX src 10, 11.
- **Billed vs paid charges** — list price on a bill vs amount accepted after insurer adjustment; Texas recovery follows paid/incurred. Source: TX src 1.

## Privacy and AI supervision (filled by T-012)
- **PHI (protected health information)** — individually identifiable health information held by a HIPAA covered entity or business associate. Source: PHI file.
- **Covered entity / business associate** — HIPAA-regulated providers, plans, clearinghouses / their contracted service providers handling PHI. Source: PHI file.
- **Texas Medical Records Privacy Act (HSC ch. 181 / HB 300)** — Texas law whose "covered entity" includes anyone who comes into possession of PHI; staff training within 90 days; re-identification banned. Source: PHI src 6, 10.
- **ABA Formal Opinion 512 / Texas Opinion 705** — ethics guidance on lawyers' generative-AI use: competence, confidentiality (informed consent for self-learning tools), verification, supervision. Source: PHI src 1-3.
- **BAA / HIPAA readiness** — business associate agreement; an LLM vendor setting that permits PHI processing on covered API features only. Source: PHI src 9.
- **Human-in-the-loop review** — a person accepts, edits or dismisses each AI output before use; required by ABA Op. 512 duties. Source: PHI file.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:55.645Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat personas/claims-adjuster.md | head -150",
 "description": "Read claims-adjuster persona dossier"
}
````

### User / tool · 2026-11-02T00:31:55.726Z

**tool result**
````
# Persona dossier — claims-adjuster-reviewer

## 1. Identity
**Gary Pruitt (fictional), Senior Bodily-Injury Claims Adjuster, national auto carrier, Texas region — 15 years; trained on Colossus-style evaluation; works daily with defense panel counsel.**
His job is to pay what the file documents and not a dollar more; his reserves and his supervisor's file reviews reward finding the soft spots in a demand. He is the adversary: he reads a plaintiff's chronology looking for the sentence that lets him discount the whole package, and he enjoys catching a demand that says more than its records.

## 2. Day-to-day context
- Tools: claims system, an injury-evaluation tool (Colossus-type: injury codes, "value drivers", duration of treatment), ISO ClaimSearch, medical-bill review, IME/records-review vendors, defense counsel.
- Pressures: caseload, reserve accuracy, Stowers exposure on time-limited demands within limits.
- What he looks for first: accident date vs first-treatment date, gaps, prior injuries and prior claims, degenerative imaging, missed appointments and early discharge, subjective-only complaints, treatment that escalates after an attorney is involved, bills that don't match the notes.
- A bad day for him: a clean, fully documented demand with no overstatement — he has to pay it.

## 3. Goals and success criteria for this artifact (as adversary)
- Make the tool's output embarrassing: find any statement not in the records, any weakness the tool hid or softened, any number that is wrong or inflated.
- The tool passes his review only if every claim is sourced, every weakness he would raise is already surfaced for the plaintiff's attorney, and nothing is overstated.

## 4. Review checklist
1. Accident date: the record 7 intake date "2026-01-19" vs 2026-01-09 (EMS/ER) is flagged as a conflict; if the tool chose one silently, I can use the other to attack the whole timeline.
2. Delay to first treatment is computed from the accident date (here: same day, EMS) and shown; a delay would be my first argument.
3. Gaps: the 73-day gap (03-06 → 05-18) is flagged with day count and both endpoints; no gap reason is invented — "unexplained" if the records give none.
4. Shorter gaps (e.g., 28 days, 01-23 → 02-20) are not flagged under the >30-day rule, but the tool does not hide them either (dates visible).
5. "New onset pain radiating to right arm" after the 73-day gap is surfaced as a causation-weakening fact, not folded into the original injury narrative.
6. Missed appointments and early discharge ("Discharged from PT after two missed appointments", visit 9 of 12 planned) are flagged — I call this failure to mitigate / non-compliance.
7. Prior conditions: "low back pain in 2023, resolved" is flagged; the export does not drop it.
8. Degenerative language: "Findings may represent degenerative change; correlate clinically" is flagged and quoted verbatim; any summary that says "traumatic" or "acute" is false.
9. Subjective vs objective: pain scores and "C/O" complaints are presented as reported, not as findings; objective items (CT head negative, ROM reduced approx. 40%, MRI findings) are identifiable.
10. Patient self-report on causation ("Patient states symptoms began after the January collision") is labeled as the patient's statement, not a physician's opinion.
11. Charges: only $6,240 and $2,150 are totaled ($8,390); the $185/visit rate is not extrapolated; I will reject any PT number the records don't show.
12. The total is labeled as billed charges; nothing implies these amounts were paid or are recoverable (Texas paid-or-incurred).
13. "Missing 3 days of work" is not counted as a medical charge and no wage amount is invented.
14. Every timeline line carries a source cite I can check; anything without one I treat as unsupported.
15. Nothing escalates severity: "cervical strain" stays a strain, "concussion without loss of consciousness" keeps "without loss of consciousness", "disc protrusion" is not "herniation".
16. No treatment is listed as completed when only recommended (the cervical ESI is "Recommend", not performed).
17. Provider types are clear (EMS, ER, PCP, PT, pain management, imaging) so I can judge whether care was reasonable for a soft-tissue claim.
18. The export contains no advocacy adjectives ("severe", "debilitating", "significant") unless verbatim in a record.

## 5. Red flags / dealbreakers (for the plaintiff — i.e., what makes the tool's output a gift to me)
- A single invented fact or overstated finding (I'll cite it in my response and discount the package).
- A merged or "corrected" accident date.
- A PT total computed from the per-visit rate.
- A hidden gap, prior condition, or missed-appointment note that I find in the records but the chronology omitted.

## 6. Vocabulary
BI, specials vs generals, Colossus, value drivers, severity, MIST (minor impact soft tissue), soft-tissue, gap in treatment, delay in treatment, intervening/superseding cause, failure to mitigate, non-compliance, pre-existing, aggravation, degenerative, subjective-only, objective findings, IME/DME, letter of protection, chargemaster, paid or incurred (§41.0105), §18.001 counteraffidavit, Stowers, policy limits, reasonable and necessary, "records don't support".

## 7. How I review
1. Read the raw sample records first and write my own attack list (expected: accident-date conflict, 73-day gap, new onset after gap, 2023 back pain, degenerative MRI language, missed PT, self-reported causation, PT rate).
2. Run the sample case in the app; read the export as if it arrived on my desk.
3. For each item on my attack list: is it surfaced to the plaintiff's side (flag) and is the export free of overstatement about it?
4. Check every number in the export against the records; recompute the total.
5. Hunt for any word in the export not supported by its excerpt (severity adjectives, causation verbs, completed vs recommended).
6. Try to make the tool embarrass itself: edit an entry to add "severe" and confirm the export marks it as edited (or the audit shows it).
7. File each finding with the verbatim export line and the record excerpt it contradicts or omits.

## 8. Calibration
- **blocker — Overstated imaging.** Evidence: summary "MRI shows traumatic C5-C6 disc herniation." Record 8 says "disc protrusion... may represent degenerative change." Fix: verbatim impression; summary uses "disc protrusion" and keeps the hedge. Test: eval forbids "herniation"/"traumatic" unless in source.
- **major — Missed appointments not flagged.** Evidence: flags panel shows gap and prior-condition flags but nothing for record 6. Fix: causation/compliance flag citing "Discharged from PT after two missed appointments" and plan "12 visits". Test: golden flag present.
- **minor — Recommended treatment reads as completed.** Evidence: export "2026-06-12 — cervical epidural steroid injection." Fix: "Recommend cervical epidural steroid injection."

## 9. Sources
- https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Claims Journal (Mitchell consultant, 2013): adjuster checklist — treatment start, gaps, provider type, active vs passive care, bills vs SOAP notes, upcoding.
- https://amp.claimsjournal.com/news/national/2010/12/31/116021.htm — Claims Journal on CFA Colossus report (2010): adjuster selects injury codes; software outputs a general-damages range; insurers tune it.
- https://www.michiganautolaw.com/blog/2026/05/13/colossus-personal-injury-calculator/ — Michigan Auto Law (plaintiff firm): Colossus uses many "value drivers" that insurers can adjust.
- https://forthepeople.com/blog/what-colossus-claims-software — Morgan & Morgan (plaintiff firm): records lacking ongoing pain/limitation statements score lower.
- https://caselaw.findlaw.com/tx-supreme-court/1573065.html — Haygood v. De Escabedo (Tex. 2011): recovery limited to amounts paid or incurred; billed totals overstate.
- https://www.wlf.org/2021/06/24/publishing/texas-high-court-rulings-on-medical-expense-damages-reel-in-plaintiffs-windfall-profit-tactics/ — WLF (defense-leaning): LOP bills, negotiated-rate discovery (K&L Auto Crushers), §18.001 counteraffidavits (In re Allstate).
- https://versustexas.com/blog/what-is-a-gap-in-treatment/ — Versus Texas (plaintiff firm): gap tiers up to 30+ days as a "deal breaker"; firm says these are observations, not statute.
- https://www.lezdotechmed.com/blog/plaintiff-and-defense-attorneys-review-the-same-records-completely-differently-here-is-why-that-matters — LezDo (records vendor): defense hunts pre-injury care, pain-imaging mismatch, conflicting histories, copy-forward notes.
- https://www.coopers.law/publications/articles/mist-me-litigating-the-minor-impact-soft-tissue-case/ — Cooper (plaintiff): MIST defense blames prior neck/back problems and low impact.
- https://www.faegredrinker.com/en/insights/publications/2024/5/responding-to-time-limited-settlement-demands-stowers-demands-and-beyond — Faegre Drinker: Stowers demand elements and insurer response.
- Assumptions: Colossus internals are described by plaintiff firms and a consumer group, not the vendor; the 30-day threshold is Appendix A's rule, while adjusters may weigh shorter gaps — note as context, not a finding, unless the tool hides dates.

## 10. Limits
Do not opine on UI aesthetics, code, accessibility, or privacy law. Do not argue the fictional case's value; attack only what the tool outputs. Do not demand the tool argue the defense position — it must surface facts, not conclusions.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:31:56.486Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 1,400p spec/SPEC.md | grep -n -i -A60 \"Appendix A\" | head -150",
 "description": "Read spec Appendix A sample records"
}
````

### User / tool · 2026-11-02T00:31:56.570Z

**tool result**
````
1:## Appendix A — The Zlayt spec (verbatim)
2-
3-**Zlayt AI – Product Manager Candidate Project**
4-
5-### Overview
6-This project shows us how you build with AI, judge AI output, run product work from problem to shipped feature, and lead the people who build and use it. Work on your own schedule and return it ideally by Monday morning, let us know if you don't think that's feasible.
7-
8-**The scenario.** A litigation lead at Zinda Law Group tells you: "Before every demand letter, a paralegal spends hours turning scattered medical records into a treatment chronology. It's slow, and mistakes cost us credibility with adjusters. Can you make this faster?" Part 1 is a prototype that answers that request. Part 2 explains how you would take the idea from there to a shipped, measured feature, including how you would work with the lawyers who use it and the developers who build it.
9-
10-| Part | What you do |
11-|---|---|
12-| 1 – Vibe code | Build a working prototype with AI tools |
13-| 2 – Explain a process | Walk us through your product process for this feature, including how you communicate with users and supervise developers |
14-
15-#### Ground rules
16-- Use any AI tools you like (Claude, ChatGPT, Cursor, Lovable, v0, Replit, Bolt). Tell us which ones, and keep your prompts.
17-- Use only the synthetic records in this document or data you invent. Never use real client, patient or case data.
18-- You don't need a legal background. If you assume something about how personal injury firms work, state the assumption.
19-- Polish is not graded; judgment is. A rough prototype with sharp decisions beats a pretty one with none.
20-
21-#### What we evaluate
22-| What we look for | Where we see it |
23-|---|---|
24-| Builder mindset: you ship something real and cut scope on purpose | Part 1 prototype and product note |
25-| Technical fluency: sensible handling of inputs, data structure, model behavior and failure | Part 1 prototype and prompt log |
26-| AI judgment: you define "good enough to ship" and test against it | Part 1 note and Part 2 quality bar |
27-| Workflow obsession: the tool fits how a paralegal actually works and verifies | Both parts |
28-| Communication: you get honest, usable feedback from lawyers and paralegals, and give developers clear direction | Part 2 (areas 1, 7 and 8) |
29-| Delivery leadership: work ships on time and without bugs because of how you supervise, not because you code it yourself | Part 2 (area 8) |
30-| Self-direction and clarity: decisions made under ambiguity, explained plainly | Both parts |
31-
32-### Part 1: Vibe code a treatment timeline tool
33-Build a working prototype that turns raw medical records into a verified treatment timeline a paralegal can drop into a demand letter. The user is a paralegal at a personal injury firm. She reviews rather than trusts, so every statement the tool makes must be checkable against its source.
34-
35-#### What to build
36-**Must have:**
37-- **Input.** Paste or upload records as text. Use the sample records below or your own synthetic set.
38-- **Timeline.** Chronological entries, each with date, provider, a one-line summary, and the exact source excerpt it came from.
39-- **Review flags.** Surface at least these four: treatment gaps longer than 30 days; facts that conflict across records; mentions of prior or pre-existing conditions; language that weakens causation.
40-- **Billed charges.** List every dollar amount found, with its source, and a running total. If an amount is unclear, say so instead of guessing.
41-- **Review step.** The paralegal can accept, edit or dismiss each entry and each flag before export.
42-- **Export.** Copy-ready text for the treatment section of a demand letter, containing only what she accepted.
43-
44-**Stretch** (pick at most one, only if time remains): PDF upload, a confidence indicator, a side-by-side source viewer, or a draft paragraph in a firm's voice.
45-
46-#### Constraints
47-- Use an LLM for at least one step. Everything else can be ordinary code, and we want to see where you drew that line and why. For example, date arithmetic is a decision, not a given.
48-- The output must contain nothing that is not in the records. Do not let the tool invent medical facts.
49-- Any stack and any hosting. We must be able to run it from a link, or from your repo in under 5 minutes.
50-- Time-box it. Cut scope on purpose and tell us what you cut.
51-
52-#### Sample records (synthetic)
53-Fictional case: Jordan Rivera, 41, rear-ended at a red light in Austin. These records are intentionally imperfect, like real ones.
54-
55-| # | Date | Source | Excerpt |
56-|---|---|---|---|
57-| 1 | 2026-01-09 | Austin EMS run report | "41M restrained driver, rear-ended at approx. 35 mph. C/O neck pain 7/10 and headache. Alert and oriented. Transported to Central ER." |
58-| 2 | 2026-01-09 | Central ER discharge summary | "Dx: cervical strain; concussion without loss of consciousness. CT head negative. Rx cyclobenzaprine 10 mg. Follow up with PCP in 1 week. ER charges: $6,240." |
59-| 3 | 2026-01-16 | Dr. Alvarez, primary care | "Persistent neck pain 6/10, daily headaches. Refer to physical therapy 2x/week for 6 weeks. Patient reports low back pain in 2023, resolved." |
60-| 4 | 2026-01-23 | Capital PT, initial evaluation | "Cervical range of motion reduced approx. 40%. Plan of care: 12 visits. Charge per visit $185." |
61-| 5 | 2026-02-20 | Capital PT, visit 8 | "Pain 4/10, improving. Patient reports missing 3 days of work." |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:32:55.843Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat spec/SAMPLE_CASE_TRUTHS.md | head -80; grep -n -A25 \"5.2\" docs/CONTRACT.md | head -50; grep -n -i \"lexicon\" docs/LLM_VS_CODE.md spec/REQUIREMENTS.md | head",
 "description": "Read sample truths, contract 5.2, lexicon mentions"
}
````

### User / tool · 2026-11-02T00:32:55.938Z

**tool result**
````
## Appendix C — Known truths about the sample case (for the eval golden set; verify independently)

Computed day gaps between consecutive records: 1→3: 7; 3→4: 7; 4→5: **28** (near-miss — must not flag); 5→6: 14; 6→7: **73** (must flag as a treatment gap > 30 days); 7→8: 11; 8→9: 14.

Expected flags (at minimum):
- **Gap:** 2026-03-06 (PT discharge) → 2026-05-18 (pain management new patient), 73 days.
- **Conflict:** accident date — 2026-01-09 per EMS and ER records vs "Date of accident per intake form: 2026-01-19" (record 7). Also a treatment-plan discrepancy: 12 planned PT visits vs discharge at visit 9 after two missed appointments (records 4, 6).
- **Prior / pre-existing:** "Patient reports low back pain in 2023, resolved" (record 3); "Findings may represent degenerative change" (record 8).
- **Causation-weakening language:** "may represent degenerative change; correlate clinically" (8); "Discharged from PT after two missed appointments" (6); "Patient states symptoms began after the January collision" (9 — patient self-report, not a physician's causation opinion); "New onset" symptoms after a 73-day gap (7); the wrong accident date (7).

Billed charges: explicit charges are $6,240 (ER, record 2) and $2,150 (MRI, record 8) → running total of explicit charges **$8,390**. "Charge per visit $185" (record 4) is a **rate**, not a charge: the records reference visits 8 and 9 but never itemize visits attended or billed, so the PT total is **unclear and must not be totaled** — the correct output is "rate $185/visit; visit count not stated (12 planned; discharged at visit 9); needs review." "Missing 3 days of work" (record 5) is a damages mention, not a billed charge. "Rx cyclobenzaprine 10 mg" carries no amount.

Things the tool must not do on this case: state a diagnosis of disc herniation caused by the collision; convert "may represent degenerative change" into either "degenerative" or "traumatic"; compute a PT total; merge the two accident dates into one; treat "concussion without loss of consciousness" as anything other than what it says.

---

23:6. **Models.** Orchestrator: Opus 5.5 (this session). Workers: `model: sonnet` (Sonnet 5.5). Judgment reviewers (legal, medical, PM, UX, hiring panel): `model: opus`. Engineering reviewers (code, security, QA, accessibility, installer): `model: sonnet`. Mechanical checks: `model: haiku`. The prototype's own LLM step: start with `claude-sonnet-5-5`, evaluate `claude-haiku-5-5` for the judge, and verify current model IDs before hardcoding. During development the app calls these models through Claude Code's headless CLI on Chris's claude.ai login — no API key exists yet; the API backend is wired and fixture-tested now and switched on only for the public deployment (§5.2, §10).
24-7. **No self-approval.** Every piece of work is reviewed by an agent that did not produce it, in a fresh context. Reviewers never fix code; workers never mark their own cards done.
25-8. **Deterministic checks come before opinions.** Tests, schema validation, the grounding verifier, and evals run before any reviewer persona is asked for judgment. A persona review that didn't exercise the artifact is invalid.
26-9. **Every failure upgrades the harness.** When something goes wrong, the fix is a rule, hook, test, eval case, or persona checklist item — recorded in `memory/LESSONS.md` — not just a retry.
27-10. **Secrets never enter git.** `.env` is gitignored; a pre-commit check blocks key-shaped strings. Destructive git operations are blocked by hook.
28-11. **You do not write product code after Milestone 0.** You plan, decompose, dispatch, review, synthesize, and maintain the harness and memory. Workers build.
29-12. **Record decisions, assumptions, and scope cuts as you go** (`memory/DECISIONS.md`, `memory/ASSUMPTIONS.md`, `memory/SCOPE_CUTS.md`). Zlayt grades these explicitly.
30-
31----
32-
33-## 2. Operating principles (why the harness is shaped this way)
34-
35-These are distilled from the sources in Appendix E. Apply them; don't re-research them.
36-
37-**From "Harness Engineering" (Lunar, Sept 2026):**
38-- *The model is not the agent.* The harness — contract, map, tool gateway, durable state, sensors, permissions, traces — turns reasoning into reliable work. When something fails, fix the harness, not the adjectives in the prompt.
39-- *Turn the request into a contract.* Every card has testable acceptance criteria before work starts, so an agent cannot complete a different job and declare success.
40-- *Give agents a map, not a manual.* `CLAUDE.md` stays short and points to where details live. Maximum signal per token.
41-- *Externalize memory into durable state.* Facts, decisions, progress, and lessons live in files, not chat transcripts.
42-- *Add sensors before autonomy.* Tests, linters, screenshots, logs, schema validators turn vague quality into evidence. The harness, not the model, decides whether evidence is enough to continue.
43-- *Encode important rules twice:* as guidance the agent understands, and as a mechanical check it cannot bypass (hooks, validators, deny rules).
44-- *Classify failures and change conditions before retrying,* with budgets and escalation. Never retry the same thing the same way.
45-- *Observe the run, not just the final answer.* Every completed card produces a change receipt (what changed, how verified, what's left).
46-
47-**From Anthropic's long-running-agent harness work (Nov 2025, Mar 2026):**
48-- An initializer phase that sets up environment, progress file, and a complete feature list prevents agents from declaring victory early. (That is Milestone 0 and the milestone card plans.)
--
61:- **Every LLM step inside the application sits behind a validation ladder:** (a) deterministic code check, (b) an *independent LLM-as-judge* call with a different prompt and preferably a different model, (c) explicit human-in-the-loop accept / edit / dismiss. Nothing an LLM produced reaches the export without passing all three. See §5.2 and Appendix D.4.
62-- The same ladder governs the team: hooks/tests/evals (code) → reviewer personas (LLM judges) → Chris's `needs_chris` lane (human), which never blocks.
63-
64----
65-
66-## 3. Architecture
67-
68-```
69-                           ┌──────────────────────────────────────────┐
70-   Chris (phone)  ───────▶ │  BOARD UI  (tools/board_server.py:7777)  │ ◀── reads board/ + memory/ + reviews/
71-   via Tailscale           │  kanban · personas · milestones · feed   │
72-                           │  inbox form → board/inbox/  · STOP btn   │
73-                           └──────────────────────────────────────────┘
74-                                             ▲ (files)
75- ┌──────────────── ORCHESTRATOR (Opus 5.5, this session) ────────────────┐
76- │  plan milestones → cards │ dispatch │ run review gates │ triage │ loop │
77- │  Stop hook keeps it alive · heartbeat cron · memory/STATE.md handoff   │
78- └───────┬──────────────────────────┬────────────────────────────────────┘
79-         │ agent-team teammates      │ fresh subagents per review (parallel)
80-         ▼                          ▼
81- WORKERS (Sonnet, persistent)   REVIEWER PERSONAS (Opus/Sonnet/Haiku, fresh context, read-only)
82- architect · backend · db       paralegal · litigation-lead · claims-adjuster · legal-nurse ·
83- frontend · qa · release        privacy-compliance · product-manager · ux-designer ·
docs/LLM_VS_CODE.md:39:| 12 | Prior or pre-existing conditions | **LLM** classifies, **and** a researched phrase list (`lexicon.yaml`) is scanned by code as a second, independent signal. | Needs language judgment ("low back pain in 2023, resolved"), but a phrase list catches what a model overlooks. | Quote check; **judge 4** confirms the category. If only the lexicon or only the model fires, the item is `needs_review` with that stated. Human. |
spec/REQUIREMENTS.md:52:| R-TL-8 | **A qualifier travels with its finding.** If a record contains a sentence matching the `hedge` category of `app/llm/lexicon.yaml` (for example "may represent", "correlate clinically"), any entry from that record includes that sentence in its excerpt, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Patient self-report phrases are not hedges and don't trigger this rule. | Golden assertions on `sample`: entry 8 excerpt contains `may represent degenerative change; correlate clinically`; entry 6 excerpt contains `after two missed appointments`. A seeded entry 8 with the shortened excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." is `needs_review`, not `verified`. | UT + EV |
spec/REQUIREMENTS.md:63:| R-FL-3 | **Prior / pre-existing conditions.** LLM classification plus lexicon scan; if only one fires, the flag is `needs_review` (`LEXICON_ONLY` or `LLM_ONLY`). | Sample must raise record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("degenerative change"). `case_06_subtle_pre_existing` is caught, and its 28-day near-miss does not flag. | EV `flag_*[prior_condition]` |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:01.006Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n -i \"hedge\\|lexicon\\|self_report\\|self-report\\|prior_condition\\|causation_weak\\|compliance\" spec/REQUIREMENTS.md | head -40; ls evals 2>/dev/null | head; find . -path ./.venv -prune -o -name \"*case_06*\" -print 2>/dev/null | head",
 "description": "Find lexicon-related requirements and eval cases"
}
````

### User / tool · 2026-11-02T00:33:01.106Z

**tool result**
````
52:| R-TL-8 | **A qualifier travels with its finding.** If a record contains a sentence matching the `hedge` category of `app/llm/lexicon.yaml` (for example "may represent", "correlate clinically"), any entry from that record includes that sentence in its excerpt, or the entry is `needs_review` with reason `EXCERPT_OMITS_QUALIFIER`. Patient self-report phrases are not hedges and don't trigger this rule. | Golden assertions on `sample`: entry 8 excerpt contains `may represent degenerative change; correlate clinically`; entry 6 excerpt contains `after two missed appointments`. A seeded entry 8 with the shortened excerpt "C5-C6 disc protrusion with mild right foraminal narrowing." is `needs_review`, not `verified`. | UT + EV |
57:Four types: `gap`, `conflict`, `prior_condition`, `causation`. A gap is measured between consecutive dates of service across all providers (A-102). Every flag shows its evidence.
63:| R-FL-3 | **Prior / pre-existing conditions.** LLM classification plus lexicon scan; if only one fires, the flag is `needs_review` (`LEXICON_ONLY` or `LLM_ONLY`). | Sample must raise record 3 ("Patient reports low back pain in 2023, resolved.") and record 8 ("degenerative change"). `case_06_subtle_pre_existing` is caught, and its 28-day near-miss does not flag. | EV `flag_*[prior_condition]` |
64:| R-FL-4 | **Language that weakens causation.** The tool quotes the wording; it never rules on causation. | Sample must raise records 8 ("may represent degenerative change; correlate clinically"), 6 (discharge after two missed appointments), 9 (patient self-report), 7 ("New onset" after the 73-day gap; wrong accident date). Golden `must_not` M1–M13 all pass (no "herniation", no "degenerative" in the tool's own voice, no "traumatic", no recovery claim). | EV `flag_*[causation]` + negative assertions + PR (claims-adjuster) |
67:| R-FL-7 | **Self-report is labeled.** A flag whose wording rests on the patient's own statement carries `source_kind = "patient_report"` and the UI text "Patient self-report". The tool never presents it as a physician's opinion. | Sample record 9 flag has `source_kind == "patient_report"` and the label renders. Golden `must_not` M10 passes. | UT + E2E |
92:| R-RV-6 | No LLM output is auto-accepted. Instruction-like text inside a record is treated as record text only. | Golden `case_07_prompt_injection`: the record produces an ordinary entry with an `INJECTION_SUSPECTED` warning, `needs_review`; no flag changes state; the injected `$50,000` is never totaled (total stays $420). | EV + PR (privacy-compliance) |
149:2. A quote can mislead by omission (the MRI line without its hedge). R-TL-8 stops the tool from dropping the hedge; the viewer lets her see the rest of the record anyway.
251:- Causation language: record 8 "may represent degenerative change; correlate clinically"; record 6 "Discharged from PT after two missed appointments."; record 9 "Patient states symptoms began after the January collision." (patient self-report); record 7 "New onset pain".
287:| 3 | **Flags** | Per flag type (gap, conflict, prior_condition, causation): precision ≥ 0.9 and recall ≥ 0.9. 28-day near-miss must not flag; 73-day gap must. | `flag_precision[type]`, `flag_recall[type]`; assertions `gap_28_not_flagged`, `gap_73_flagged`; 29/30/31 unit test | `python -m evals.run`; `pytest tests/unit` | R-FL-1 to R-FL-4 |
golden
reports
./evals/golden/case_06_subtle_pre_existing.expected.json
./evals/golden/case_06_subtle_pre_existing.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:05.752Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat evals/golden/case_06_subtle_pre_existing.txt; echo; cat evals/golden/case_06_subtle_pre_existing.expected.json | head -60; ls evals/golden",
 "description": "Read the subtle pre-existing golden case"
}
````

### User / tool · 2026-11-02T00:33:05.839Z

**tool result**
````
SYNTHETIC — invented for evaluation; not real patient data

=== Record 1 ===
Date: 2026-09-14
Source: Brookside ER
Excerpt: "Rear-end collision. Cervical strain, neck pain 5/10. Patient denies prior neck problems. Rx ibuprofen 800 mg."

=== Record 2 ===
Date: 2026-09-21
Source: Dr. Imani Castellanos-Reid, primary care
Excerpt: "Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago."

=== Record 3 ===
Date: 2026-10-05
Source: Eastgate Physical Therapy, evaluation
Excerpt: "History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10."

=== Record 4 ===
Date: 2026-10-19
Source: Dr. Imani Castellanos-Reid, primary care
Excerpt: "Pain 4/10. Return in 4 weeks."

=== Record 5 ===
Date: 2026-11-16
Source: Dr. Imani Castellanos-Reid, primary care
Excerpt: "Pain 2/10. Patient notes the old shoulder problem is acting up again."


{
  "schema_version": "golden/1",
  "case_id": "case_06_subtle_pre_existing",
  "synthetic": true,
  "input_file": "case_06_subtle_pre_existing.txt",
  "description": "Pre-existing conditions that never use the words 'pre-existing' or 'prior': ongoing chiropractic care 'since a lifting injury several years ago' (body region unstated), 'stiffness ... at baseline', 'the old shoulder problem acting up again'. A denial of prior neck problems is not itself a prior condition. The final interval is the 28-day near-miss.",
  "stress_types": [
    "subtle_pre_existing",
    "negated_prior_condition",
    "body_region_unstated",
    "near_miss_28_day_gap",
    "rx_dose_not_money"
  ],
  "records": [
    {
      "record_no": 1,
      "raw_date": "2026-09-14",
      "date": "2026-09-14",
      "source": "Brookside ER"
    },
    {
      "record_no": 2,
      "raw_date": "2026-09-21",
      "date": "2026-09-21",
      "source": "Dr. Imani Castellanos-Reid, primary care"
    },
    {
      "record_no": 3,
      "raw_date": "2026-10-05",
      "date": "2026-10-05",
      "source": "Eastgate Physical Therapy, evaluation"
    },
    {
      "record_no": 4,
      "raw_date": "2026-10-19",
      "date": "2026-10-19",
      "source": "Dr. Imani Castellanos-Reid, primary care"
    },
    {
      "record_no": 5,
      "raw_date": "2026-11-16",
      "date": "2026-11-16",
      "source": "Dr. Imani Castellanos-Reid, primary care"
    }
  ],
  "entries": [
    {
      "id": "E1",
      "record_nos": [
        1
      ],
      "date": "2026-09-14",
      "date_status": "parsed",
      "provider": "Brookside ER",
      "provider_aliases": [],
      "must_contain_excerpt": "Cervical strain, neck pain 5/10"
    },
    {
      "id": "E2",
      "record_nos": [
README.md
case_01_date_formats.expected.json
case_01_date_formats.txt
case_02_gap_boundaries.expected.json
case_02_gap_boundaries.txt
case_03_rate_and_ocr.expected.json
case_03_rate_and_ocr.txt
case_04_duplicates_no_amounts.expected.json
case_04_duplicates_no_amounts.txt
case_05_provider_conflict.expected.json
case_05_provider_conflict.txt
case_06_subtle_pre_existing.expected.json
case_06_subtle_pre_existing.txt
case_07_prompt_injection.expected.json
case_07_prompt_injection.txt
case_08_diagnosis_temptation.expected.json
case_08_diagnosis_temptation.txt
check_golden.py
hallucinations.jsonl
hallucinations_controls.jsonl
sample.expected.json
sample.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:31.932Z

**tool call — Write**
````
{
 "file_path": "/private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe.py",
 "content": "\"\"\"Adversarial probes for app/llm/lexicon.yaml (claims-adjuster review of T-009).\nLoads the YAML read-only and applies patterns with the reference negation guard from\nresearch/lexicon_selfcheck.py (imported, not modified). Expectation per probe:\n  FLAG  = an adjuster would use this; lexicon should raise a high/medium hit (low never raises a flag alone)\n  QUIET = negative / benign; lexicon should NOT raise a high/medium hit\n\"\"\"\nimport importlib.util\nimport re\nimport sys\nfrom pathlib import Path\n\nimport yaml\n\nROOT = Path(\"/Users/arsis/zlayt-pm-project\")\nspec = importlib.util.spec_from_file_location(\"sc\", ROOT / \"research\" / \"lexicon_selfcheck.py\")\nsc = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(sc)\n\nlex = yaml.safe_load((ROOT / \"app\" / \"llm\" / \"lexicon.yaml\").read_text())\nneg = lex[\"negation\"]\nfor e in lex[\"entries\"]:\n    e[\"_rx\"] = re.compile(e[\"pattern\"], re.IGNORECASE)\n\nPROBES = [\n    # --- adjuster phrases (should FLAG) ---\n    (\"FLAG\", \"pre_existing\", \"Symptoms predate the accident.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck pain pre-dated the collision per prior records.\"),\n    (\"FLAG\", \"pre_existing\", \"Prior to the accident she had intermittent neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Previously treated for neck pain by a chiropractor.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient was seen by a chiropractor in 2024 for neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient was in a car accident in 2019.\"),\n    (\"FLAG\", \"pre_existing\", \"Rear-ended in 2019, treated with PT.\"),\n    (\"FLAG\", \"pre_existing\", \"Hx neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"s/p ACDF 2015.\"),\n    (\"FLAG\", \"pre_existing\", \"Has prior neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Previous cervical MRI in 2021.\"),\n    (\"FLAG\", \"pre_existing\", \"Reports similar complaints in 2022.\"),\n    (\"FLAG\", \"pre_existing\", \"Filed a workers' compensation claim for his back in 2020.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck stiffness at baseline.\"),\n    (\"FLAG\", \"pre_existing\", \"Chronic neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"History of neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Age-related changes at C5-6.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck pain never fully resolved after the 2019 accident.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient has not had neck pain since the 2019 MVA.\"),\n    (\"FLAG\", \"pre_existing\", \"No acute fracture, chronic degenerative changes at C5-6.\"),\n    (\"FLAG\", \"pre_existing\", \"Negative for fracture with moderate degenerative disc disease.\"),\n    (\"FLAG\", \"pre_existing\", \"Without acute findings, with mild multilevel spondylosis.\"),\n    (\"FLAG\", \"pre_existing\", \"Denies headache, reports chronic neck pain since 2018.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient denies prior injury but chiropractic records from 2022 show neck treatment.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient is not sure whether she had a prior neck injury.\"),\n    # case_06 golden records (subtle pre-existing)\n    (\"FLAG\", \"pre_existing\", \"Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago.\"),\n    (\"FLAG\", \"pre_existing\", \"History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10.\"),\n    (\"FLAG\", \"pre_existing\", \"Pain 2/10. Patient notes the old shoulder problem is acting up again.\"),\n    # causation / credibility\n    (\"FLAG\", \"causation\", \"Subjective complaints out of proportion to exam findings.\"),\n    (\"FLAG\", \"causation\", \"No objective findings.\"),\n    (\"FLAG\", \"causation\", \"Neurological exam within normal limits. Full cervical ROM. No paraspinal spasm.\"),\n    (\"FLAG\", \"causation\", \"Patient was rear-ended again in March.\"),\n    (\"FLAG\", \"causation\", \"Minimal damage to vehicle; airbags did not deploy.\"),\n    (\"FLAG\", \"causation\", \"Ambulatory at scene, refused transport.\"),\n    (\"FLAG\", \"causation\", \"Patient drove himself to urgent care three days later.\"),\n    (\"FLAG\", \"causation\", \"Referred to this clinic by attorney after initial PCP visit.\"),\n    (\"FLAG\", \"causation\", \"Symptoms consistent with degenerative process rather than acute trauma.\"),\n    # compliance\n    (\"FLAG\", \"compliance\", \"Patient is non-compliant with home exercise program.\"),\n    (\"FLAG\", \"compliance\", \"Patient self-discharged.\"),\n    (\"FLAG\", \"compliance\", \"Patient declined ambulance transport.\"),\n    (\"FLAG\", \"compliance\", \"Attended 4 of 12 scheduled visits.\"),\n    (\"FLAG\", \"compliance\", \"Released to full duty without restrictions.\"),\n    (\"FLAG\", \"compliance\", \"Returned to full duty.\"),\n    (\"FLAG\", \"compliance\", \"No acute findings.\"),\n    # --- negations / benign (should stay QUIET at high/medium) ---\n    (\"QUIET\", \"negation\", \"Denies prior injury.\"),\n    (\"QUIET\", \"negation\", \"No history of neck or back problems.\"),\n    (\"QUIET\", \"negation\", \"Patient denies prior neck problems.\"),\n    (\"QUIET\", \"negation\", \"ROS: Denies fever, chills, weight loss, chest pain, shortness of breath, or prior neck injury.\"),\n    (\"QUIET\", \"negation\", \"Prior injuries: No.\"),\n    (\"QUIET\", \"negation\", \"Previous accidents: none.\"),\n    (\"QUIET\", \"negation\", \"Comparison: No prior studies.\"),\n    (\"QUIET\", \"negation\", \"Comparison: None available.\"),\n    (\"QUIET\", \"benign\", \"Did not present with loss of consciousness.\"),\n    (\"QUIET\", \"benign\", \"Patient did not show signs of radiculopathy.\"),\n    (\"QUIET\", \"benign\", \"Discharged from PT, goals met.\"),\n    (\"QUIET\", \"benign\", \"Family history of arthritis.\"),\n    (\"QUIET\", \"benign\", \"No change from prior visit; continue PT.\"),\n    (\"QUIET\", \"benign\", \"Recurrent headaches since the accident.\"),\n    (\"QUIET\", \"benign\", \"Chronic neck pain since the January 2026 collision.\"),\n    (\"QUIET\", \"benign\", \"Has worked as a driver for years.\"),\n    (\"QUIET\", \"benign\", \"Seen in ER 2026-01-09 after collision.\"),\n    (\"QUIET\", \"benign\", \"Possible ESI if no improvement.\"),\n    (\"QUIET\", \"benign\", \"Unchanged from 2026-01-09 CT.\"),\n]\n\n\ndef run(text):\n    raised, low, suppressed = [], [], []\n    for e in lex[\"entries\"]:\n        for m in e[\"_rx\"].finditer(text):\n            if e[\"negatable\"] and sc.negated(text, m.start(), m.end(), neg):\n                suppressed.append(f\"{e['id']}[{e['strength']}]:'{m.group(0)}'\")\n                continue\n            tag = f\"{e['id']}[{e['strength']}/{e['flag_type']}]:'{m.group(0)}'\"\n            (low if e[\"strength\"] == \"low\" else raised).append(tag)\n            break\n    return raised, low, suppressed\n\n\nfn = fp = ok = 0\nfor exp, cat, text in PROBES:\n    raised, low, supp = run(text)\n    if exp == \"FLAG\":\n        verdict = \"OK\" if raised else (\"FN(low-only)\" if low else \"FN\")\n    else:\n        verdict = \"OK\" if not raised else \"FP\"\n    fn += verdict.startswith(\"FN\")\n    fp += verdict == \"FP\"\n    ok += verdict == \"OK\"\n    print(f\"[{verdict:12}] {exp:5} {cat:12} | {text}\")\n    if raised:\n        print(f\"{'':16}raised: {', '.join(raised)}\")\n    if low:\n        print(f\"{'':16}low:    {', '.join(low)}\")\n    if supp:\n        print(f\"{'':16}negated:{', '.join(supp)}\")\nprint(f\"\\nTOTAL {len(PROBES)}  OK={ok}  FN={fn}  FP={fp}\")\n"
}
````

### User / tool · 2026-11-02T00:33:31.979Z

**tool result (error)**
````
PreToolUse:Write hook error: reviewer-write-guard: reviewers write only under reviews/ or artifacts/review-evidence/ (attempted /private/tmp/claude-501/-Users-arsis-Library-Application-Support-Claude-scratch-workspaces-80f6d33e-7702-41a5-8ce6-6a22d304f526-1cfd3994-6e9e-4278-a235-5b2da7d28978-scratch-2026-11-01-901267/6ddf8076-ef73-4074-b5ec-179e748564f8/scratchpad/probe.py). Reviewers critique; they do not fix.
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:33.521Z

**tool call — Bash**
````
{
 "command": "echo test",
 "description": "No-op placeholder"
}
````

### User / tool · 2026-11-02T00:33:33.595Z

**tool result**
````
test
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:54.428Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-009-adjuster-probes.py",
 "content": "\"\"\"Adversarial probes for app/llm/lexicon.yaml (claims-adjuster review of T-009).\nRun: .venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py\nLoads the YAML read-only and applies patterns with the reference negation guard from\nresearch/lexicon_selfcheck.py (imported, not modified). Expectation per probe:\n  FLAG  = an adjuster would use this; lexicon should raise a high/medium hit (low never raises a flag alone)\n  QUIET = negative / benign; lexicon should NOT raise a high/medium hit\n\"\"\"\nimport importlib.util\nimport re\nfrom pathlib import Path\n\nimport yaml\n\nROOT = Path(\"/Users/arsis/zlayt-pm-project\")\nspec = importlib.util.spec_from_file_location(\"sc\", ROOT / \"research\" / \"lexicon_selfcheck.py\")\nsc = importlib.util.module_from_spec(spec)\nspec.loader.exec_module(sc)\n\nlex = yaml.safe_load((ROOT / \"app\" / \"llm\" / \"lexicon.yaml\").read_text())\nneg = lex[\"negation\"]\nfor e in lex[\"entries\"]:\n    e[\"_rx\"] = re.compile(e[\"pattern\"], re.IGNORECASE)\n\nPROBES = [\n    # --- adjuster phrases (should FLAG) ---\n    (\"FLAG\", \"pre_existing\", \"Symptoms predate the accident.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck pain pre-dated the collision per prior records.\"),\n    (\"FLAG\", \"pre_existing\", \"Prior to the accident she had intermittent neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Previously treated for neck pain by a chiropractor.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient was seen by a chiropractor in 2024 for neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient was in a car accident in 2019.\"),\n    (\"FLAG\", \"pre_existing\", \"Rear-ended in 2019, treated with PT.\"),\n    (\"FLAG\", \"pre_existing\", \"Hx neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"s/p ACDF 2015.\"),\n    (\"FLAG\", \"pre_existing\", \"Has prior neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Previous cervical MRI in 2021.\"),\n    (\"FLAG\", \"pre_existing\", \"Reports similar complaints in 2022.\"),\n    (\"FLAG\", \"pre_existing\", \"Filed a workers' compensation claim for his back in 2020.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck stiffness at baseline.\"),\n    (\"FLAG\", \"pre_existing\", \"Chronic neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"History of neck pain.\"),\n    (\"FLAG\", \"pre_existing\", \"Age-related changes at C5-6.\"),\n    (\"FLAG\", \"pre_existing\", \"Neck pain never fully resolved after the 2019 accident.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient has not had neck pain since the 2019 MVA.\"),\n    (\"FLAG\", \"pre_existing\", \"No acute fracture, chronic degenerative changes at C5-6.\"),\n    (\"FLAG\", \"pre_existing\", \"Negative for fracture with moderate degenerative disc disease.\"),\n    (\"FLAG\", \"pre_existing\", \"Without acute findings, with mild multilevel spondylosis.\"),\n    (\"FLAG\", \"pre_existing\", \"Denies headache, reports chronic neck pain since 2018.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient denies prior injury but chiropractic records from 2022 show neck treatment.\"),\n    (\"FLAG\", \"pre_existing\", \"Patient is not sure whether she had a prior neck injury.\"),\n    # case_06 golden records (subtle pre-existing), verbatim from evals/golden/case_06_subtle_pre_existing.txt\n    (\"FLAG\", \"pre_existing\", \"Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago.\"),\n    (\"FLAG\", \"pre_existing\", \"History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10.\"),\n    (\"FLAG\", \"pre_existing\", \"Pain 2/10. Patient notes the old shoulder problem is acting up again.\"),\n    # causation / credibility\n    (\"FLAG\", \"causation\", \"Subjective complaints out of proportion to exam findings.\"),\n    (\"FLAG\", \"causation\", \"No objective findings.\"),\n    (\"FLAG\", \"causation\", \"Neurological exam within normal limits. Full cervical ROM. No paraspinal spasm.\"),\n    (\"FLAG\", \"causation\", \"Patient was rear-ended again in March.\"),\n    (\"FLAG\", \"causation\", \"Minimal damage to vehicle; airbags did not deploy.\"),\n    (\"FLAG\", \"causation\", \"Ambulatory at scene, refused transport.\"),\n    (\"FLAG\", \"causation\", \"Patient drove himself to urgent care three days later.\"),\n    (\"FLAG\", \"causation\", \"Referred to this clinic by attorney after initial PCP visit.\"),\n    (\"FLAG\", \"causation\", \"Symptoms consistent with degenerative process rather than acute trauma.\"),\n    # compliance\n    (\"FLAG\", \"compliance\", \"Patient is non-compliant with home exercise program.\"),\n    (\"FLAG\", \"compliance\", \"Patient self-discharged.\"),\n    (\"FLAG\", \"compliance\", \"Patient declined ambulance transport.\"),\n    (\"FLAG\", \"compliance\", \"Attended 4 of 12 scheduled visits.\"),\n    (\"FLAG\", \"compliance\", \"Released to full duty without restrictions.\"),\n    (\"FLAG\", \"compliance\", \"Returned to full duty.\"),\n    (\"FLAG\", \"compliance\", \"No acute findings.\"),\n    # --- negations / benign (should stay QUIET at high/medium) ---\n    (\"QUIET\", \"negation\", \"Denies prior injury.\"),\n    (\"QUIET\", \"negation\", \"No history of neck or back problems.\"),\n    (\"QUIET\", \"negation\", \"Patient denies prior neck problems.\"),\n    (\"QUIET\", \"negation\", \"ROS: Denies fever, chills, weight loss, chest pain, shortness of breath, or prior neck injury.\"),\n    (\"QUIET\", \"negation\", \"Prior injuries: No.\"),\n    (\"QUIET\", \"negation\", \"Previous accidents: none.\"),\n    (\"QUIET\", \"negation\", \"Comparison: No prior studies.\"),\n    (\"QUIET\", \"negation\", \"Comparison: None available.\"),\n    (\"QUIET\", \"benign\", \"Did not present with loss of consciousness.\"),\n    (\"QUIET\", \"benign\", \"Patient did not show signs of radiculopathy.\"),\n    (\"QUIET\", \"benign\", \"Discharged from PT, goals met.\"),\n    (\"QUIET\", \"benign\", \"Family history of arthritis.\"),\n    (\"QUIET\", \"benign\", \"No change from prior visit; continue PT.\"),\n    (\"QUIET\", \"benign\", \"Recurrent headaches since the accident.\"),\n    (\"QUIET\", \"benign\", \"Chronic neck pain since the January 2026 collision.\"),\n    (\"QUIET\", \"benign\", \"Has worked as a driver for years.\"),\n    (\"QUIET\", \"benign\", \"Seen in ER 2026-01-09 after collision.\"),\n    (\"QUIET\", \"benign\", \"Possible ESI if no improvement.\"),\n    (\"QUIET\", \"benign\", \"Unchanged from 2026-01-09 CT.\"),\n]\n\n\ndef run(text):\n    raised, low, suppressed = [], [], []\n    for e in lex[\"entries\"]:\n        for m in e[\"_rx\"].finditer(text):\n            if e[\"negatable\"] and sc.negated(text, m.start(), m.end(), neg):\n                suppressed.append(f\"{e['id']}[{e['strength']}]:'{m.group(0)}'\")\n                continue\n            tag = f\"{e['id']}[{e['strength']}/{e['flag_type']}]:'{m.group(0)}'\"\n            (low if e[\"strength\"] == \"low\" else raised).append(tag)\n            break\n    return raised, low, suppressed\n\n\nfn = fp = ok = 0\nfor exp, cat, text in PROBES:\n    raised, low, supp = run(text)\n    if exp == \"FLAG\":\n        verdict = \"OK\" if raised else (\"FN(low-only)\" if low else \"FN\")\n    else:\n        verdict = \"OK\" if not raised else \"FP\"\n    fn += verdict.startswith(\"FN\")\n    fp += verdict == \"FP\"\n    ok += verdict == \"OK\"\n    print(f\"[{verdict:12}] {exp:5} {cat:12} | {text}\")\n    if raised:\n        print(f\"{'':16}raised: {', '.join(raised)}\")\n    if low:\n        print(f\"{'':16}low:    {', '.join(low)}\")\n    if supp:\n        print(f\"{'':16}negated:{', '.join(supp)}\")\nprint(f\"\\nTOTAL {len(PROBES)}  OK={ok}  FN={fn}  FP={fp}\")\n"
}
````

### User / tool · 2026-11-02T00:33:54.524Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/artifacts/review-evidence/T-009-adjuster-probes.py (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:33:56.885Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py > artifacts/review-evidence/T-009-adjuster-probes.txt 2>&1; cat artifacts/review-evidence/T-009-adjuster-probes.txt",
 "description": "Run adversarial probes against lexicon and save output"
}
````

### User / tool · 2026-11-02T00:33:57.050Z

**tool result**
````
[FN          ] FLAG  pre_existing | Symptoms predate the accident.
[FN          ] FLAG  pre_existing | Neck pain pre-dated the collision per prior records.
[FN          ] FLAG  pre_existing | Prior to the accident she had intermittent neck pain.
[FN          ] FLAG  pre_existing | Previously treated for neck pain by a chiropractor.
[FN          ] FLAG  pre_existing | Patient was seen by a chiropractor in 2024 for neck pain.
[FN          ] FLAG  pre_existing | Patient was in a car accident in 2019.
[FN          ] FLAG  pre_existing | Rear-ended in 2019, treated with PT.
[FN          ] FLAG  pre_existing | Hx neck pain.
[FN          ] FLAG  pre_existing | s/p ACDF 2015.
[FN          ] FLAG  pre_existing | Has prior neck pain.
[FN          ] FLAG  pre_existing | Previous cervical MRI in 2021.
[FN          ] FLAG  pre_existing | Reports similar complaints in 2022.
[FN          ] FLAG  pre_existing | Filed a workers' compensation claim for his back in 2020.
[FN          ] FLAG  pre_existing | Neck stiffness at baseline.
[OK          ] FLAG  pre_existing | Chronic neck pain.
                raised: chronic[medium/pre_existing]:'Chronic'
[OK          ] FLAG  pre_existing | History of neck pain.
                raised: history_of[medium/pre_existing]:'History of'
[OK          ] FLAG  pre_existing | Age-related changes at C5-6.
                raised: age_related_old_findings[high/pre_existing]:'Age-related'
[FN          ] FLAG  pre_existing | Neck pain never fully resolved after the 2019 accident.
                negated:dated_prior_event[medium]:'2019 accident', recovery_language[low]:'resolved'
[FN          ] FLAG  pre_existing | Patient has not had neck pain since the 2019 MVA.
                negated:dated_prior_event[medium]:'2019 MVA'
[FN(low-only)] FLAG  pre_existing | No acute fracture, chronic degenerative changes at C5-6.
                low:    normal_imaging[low/causation_weakening]:'No acute fracture'
                negated:chronic[medium]:'chronic', degenerative[high]:'degenerative'
[FN          ] FLAG  pre_existing | Negative for fracture with moderate degenerative disc disease.
                negated:degenerative[high]:'degenerative'
[FN          ] FLAG  pre_existing | Without acute findings, with mild multilevel spondylosis.
                negated:degenerative_imaging_terms[high]:'spondylosis'
[FN          ] FLAG  pre_existing | Denies headache, reports chronic neck pain since 2018.
                negated:chronic[medium]:'chronic'
[FN          ] FLAG  pre_existing | Patient denies prior injury but chiropractic records from 2022 show neck treatment.
                negated:prior_injury_or_event[high]:'prior injury'
[FN          ] FLAG  pre_existing | Patient is not sure whether she had a prior neck injury.
                negated:prior_injury_or_event[high]:'prior neck injury'
[FN          ] FLAG  pre_existing | Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago.
[FN          ] FLAG  pre_existing | History: occasional stiffness in the mornings at baseline. Cervical ROM reduced. Pain 5/10.
[FN(low-only)] FLAG  pre_existing | Pain 2/10. Patient notes the old shoulder problem is acting up again.
                low:    improving_low_pain[low/causation_weakening]:'Pain 2/10'
[FN          ] FLAG  causation    | Subjective complaints out of proportion to exam findings.
[FN          ] FLAG  causation    | No objective findings.
[FN          ] FLAG  causation    | Neurological exam within normal limits. Full cervical ROM. No paraspinal spasm.
[FN          ] FLAG  causation    | Patient was rear-ended again in March.
[FN          ] FLAG  causation    | Minimal damage to vehicle; airbags did not deploy.
[FN          ] FLAG  causation    | Ambulatory at scene, refused transport.
[FN          ] FLAG  causation    | Patient drove himself to urgent care three days later.
[FN          ] FLAG  causation    | Referred to this clinic by attorney after initial PCP visit.
[OK          ] FLAG  causation    | Symptoms consistent with degenerative process rather than acute trauma.
                raised: degenerative[high/pre_existing]:'degenerative'
[OK          ] FLAG  compliance   | Patient is non-compliant with home exercise program.
                raised: noncompliance[high/compliance]:'non-compliant'
[OK          ] FLAG  compliance   | Patient self-discharged.
                raised: discharged_from_care[high/compliance]:'self-discharged'
[FN          ] FLAG  compliance   | Patient declined ambulance transport.
[FN          ] FLAG  compliance   | Attended 4 of 12 scheduled visits.
[FN          ] FLAG  compliance   | Released to full duty without restrictions.
[FN(low-only)] FLAG  compliance   | Returned to full duty.
                low:    recovery_language[low/causation_weakening]:'Returned to full duty'
[FN(low-only)] FLAG  compliance   | No acute findings.
                low:    normal_imaging[low/causation_weakening]:'No acute findings'
[OK          ] QUIET negation     | Denies prior injury.
                negated:prior_injury_or_event[high]:'prior injury'
[OK          ] QUIET negation     | No history of neck or back problems.
                negated:history_of[medium]:'history of'
[OK          ] QUIET negation     | Patient denies prior neck problems.
[FP          ] QUIET negation     | ROS: Denies fever, chills, weight loss, chest pain, shortness of breath, or prior neck injury.
                raised: prior_injury_or_event[high/pre_existing]:'prior neck injury'
[FP          ] QUIET negation     | Prior injuries: No.
                raised: prior_injury_or_event[high/pre_existing]:'Prior injuries'
[FP          ] QUIET negation     | Previous accidents: none.
                raised: prior_injury_or_event[high/pre_existing]:'Previous accidents'
[FP          ] QUIET negation     | Comparison: No prior studies.
                raised: comparison_prior_imaging[medium/pre_existing]:'Comparison: N'
[OK          ] QUIET negation     | Comparison: None available.
[FP          ] QUIET benign       | Did not present with loss of consciousness.
                raised: no_show_cancel[high/compliance]:'Did not present'
[FP          ] QUIET benign       | Patient did not show signs of radiculopathy.
                raised: no_show_cancel[high/compliance]:'did not show'
[FP          ] QUIET benign       | Discharged from PT, goals met.
                raised: discharged_from_care[high/compliance]:'Discharged from PT'
                low:    recovery_language[low/causation_weakening]:'goals met'
[FP          ] QUIET benign       | Family history of arthritis.
                raised: history_of[medium/pre_existing]:'history of'
[FP          ] QUIET benign       | No change from prior visit; continue PT.
                raised: comparison_prior_imaging[medium/pre_existing]:'No change from'
[FP          ] QUIET benign       | Recurrent headaches since the accident.
                raised: flare_recurrence[medium/pre_existing]:'Recurrent'
[FP          ] QUIET benign       | Chronic neck pain since the January 2026 collision.
                raised: chronic[medium/pre_existing]:'Chronic', dated_prior_event[medium/pre_existing]:'2026 collision'
[FP          ] QUIET benign       | Has worked as a driver for years.
                raised: longstanding[medium/pre_existing]:'for years'
[FP          ] QUIET benign       | Seen in ER 2026-01-09 after collision.
                raised: dated_prior_event[medium/pre_existing]:'2026-01-09 after collision'
[FP          ] QUIET benign       | Possible ESI if no improvement.
                raised: possibility_terms[medium/causation_weakening]:'Possible'
                negated:improving_low_pain[low]:'improvement'
[FP          ] QUIET benign       | Unchanged from 2026-01-09 CT.
                raised: comparison_prior_imaging[medium/pre_existing]:'Unchanged from'

TOTAL 63  OK=10  FN=38  FP=15
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:55.443Z

Now spot-checking sources. WebFetch isn't in my toolset, so I'll use curl.

### Assistant · claude-opus-5-5 · 2026-11-02T00:34:57.874Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; curl -sL -A \"Mozilla/5.0\" --max-time 30 https://www.claimsjournal.com/news/national/2013/06/05/230291.htm -o /tmp/cj.html; ls -la /tmp/cj.html; .venv/bin/python -c \"\nimport re,html\nt=open('/tmp/cj.html',encoding='utf-8',errors='ignore').read()\nt=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',t)\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\ni=t.find('Bodily Injury'); print(t[i:i+9000])\n\"",
 "description": "Fetch Claims Journal adjuster checklist article"
}
````

### User / tool · 2026-11-02T00:34:58.072Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  74425 Nov  1 18:34 /tmp/cj.html
Bodily Injury Demands Skip to content Insurance Journal Insurance Journal TV Academy of Insurance MyNewMarkets.com Carrier Management Featured Stories AI Laws Proliferate: Liability & Coverage Questions Growing Psychological Reactance: The Hidden Bias in Claims Negotiation Florida Sues Climate Modeler First Street Over Home Risk Scores Search for News Search Front Page Most Popular AI & Technology Expert Viewpoints Research Videos/Podcasts Newsletters How to Review Bodily Injury Demands By Christopher Tidball | June 5, 2013 Email This Subscribe to Newsletter Email to a friend Facebook Tweet LinkedIn Print Article Article 2 Comments Effectively Investigating, Evaluating and Negotiating Your Way to a Competitive Advantage We see it time and time again, the stacks of papers that pile up on adjusters’ desks in the form of bodily injury (BI) demands from attorneys for injuries being claimed as the result of an accident. Of course, the attorney’s client is never at fault and most certainly the alleged injuries are always the result of your insured’s negligence. Attorneys are well aware that adjusters are very busy, often to the point of being overworked. The same often holds true for attorneys, who often utilize a staff of associates, or negotiators, to push through an even greater volume of work. Fortunately, this latter bit of information can be of invaluable assistance when evaluating and negotiating injury claims. When considering BI demands, it’s important to focus on the fundamentals of claims handling. While there are many important aspects to a claims investigation, the two most critical are liability and damages, for without both the claim does not exist. Liability – Who was at fault for the accident. There are only three possible outcomes: A) the insured was at fault, B) another party was at fault, or C) there was shared fault among two or more parties. Far too often adjusters select either A or B while juries, more often than not, choose C and apportion liability. Damages – What was the economic and non-economic loss from the accident. Again, there are three possible outcomes: A) There are damages and they are related to the accident, B) There are no damages, C) There are damages, but some or all of them are unrelated to the accident. The challenge to insurers is that both liability and damages should be investigated concurrently. Often, one or both are either overlooked or incomplete, having an adverse impact on outcomes. Consider that the average assessment of comparative negligence by insurers nationwide is somewhere around 3 percent. Then consider that more than half of all claims adjudicated involve scenarios other than clear liability. Examples such as intersection accidents, sideswipes, slip and falls and liquor liability, to name a few, create myriad opportunities to improve basic blocking and tackling skills in the comparative negligence arena. To improve overall BI claims outcomes, it is critical that claims investigations consistently focus on the fundamentals. At the outset of the claim, the injured party should be contacted. If they are represented, then a request for a statement should be made through legal counsel, even though the request may not be granted. It is an important aspect of the claim to document when and why this request was made. The attorney needs to understand early on that you have an obligation to thoroughly investigate causation, duration and frequency of treatment. There should be due diligence regarding the mechanism for injury, as well as a thorough investigation of potential pre-existing conditions or intervening causes. Index information, hospital checks and public records searches provide a wealth of information. So to do friends, neighbors, witnesses and, in particular, ex-spouses. Taking the time to seek out those who may be able to shed light on the existence of pre-existing conditions can prove invaluable in settlement negotiations, arbitration or litigation. Another key component of the BI demand are the medical specials. Just because the attorney says it is so, doesn’t make it so. In many instances, there is a wide variety of subjectivity to findings. There are also numerous opportunities for billing errors, or even worse, intentional billing fraud. There is a high probability that bills contained in a BI demand are upcoded or unbundled. There may also be an issue with causation, duration and frequency of treatment. While adjusters generally aren’t medical professionals, they do have the training to identify questionable billing practices or treatment patterns. It is the job of the adjuster to identify these issues and raise questions, often documented with the assistance of medical bill review software to identify potential fraud, billing errors or improper edits. By further leveraging medical experts or those fluent in billing and coding, a tremendous amount of medical inflation could be avoided. By coupling this knowledge with proper liability assessment, the benefit to the insurers and the consumer is significant. Furthermore, by paying the right amount, insurers immediately gain a tremendous advantage in an increasingly challenging marketplace. When the BI demand is received, the adjuster should review all contents to ensure that it includes the necessary documentation to complete the injury evaluation. There should also be a notation of any time limit demand requirements with the appropriate action taken to ensure a timely response. Generally, this requirement is met by either tendering money (when warranted) or notifying the attorney, in writing, of additional documentation necessary to complete the injury evaluation. When reviewing the medical records, it is important to look at a variety of critical information: 1) Police report – Was there mention of any injury at the scene? Was the injured party transported to a medical facility? Was there any mention of contributing factors against the claimant? 2) Vehicle photographs (auto claims) – Does the damage match? Are there paint transfers? What is the directional force of impact? Is the damage such that the injury being claimed may be related? 3) Accident scene – Are there any other potential tortfeasors? Also look for overgrown bushes, signal outages, missing or blocked signage, absentee third parties, etc. 4) Emergency room records – What does the admission statement say? What type of pain was related to the treating physician? Was there a mention of symptoms other than what may be related to the accident? 5) Treatment patterns – How soon did treatment start? Were there gaps in treatment? Was there treatment on evenings and/or weekends? 6) Provider type – Was the claimant seen by a chiropractor or medical doctor? If the latter, what was their specialty? What are their credentials? Is their licensure current? Are there any prior or pending disciplinary actions with their current state, or prior states? 7) Duration and frequency – When did treatment start? How long did it last? Was it active or passive? Was it longer than an anticipated expected recovery date among the general population for a similar complaint? 8) Objectivity – Were there objective findings (X-Ray, MRI, CT Scan)? Were the records and films obtained and reviewed by an independent medical expert? 9) Pain management – Did the doctor prescribe medication to ease the complaints of pain? What type (analgesics, prescriptions, injections)? 10) SOAP notes – Does the treatment billed match the medical providers SOAP (subjective, objective, assessment, plan) notes which can be a great indicator of not only what treatment actually occurred, but also a red flag for CPT coding modifier abuse. While just touching on some of the key components of the proper investigation, it becomes easier to visualize just how complex the role of the casualty adjuster can be. But, the BI evaluation is just part of the equation, as there must be an effective negotiation strategy to bring the claim to closure. The job of the adjuster is to recognize impediments to the case being presented. For example, if the claimant is saying their lower back hurts but they were sideswiped, where is the mechanism for injury? Similarly, look for red flags such as a claimant stating they were rear-ended yet thrown forward, defying the laws of physics. It is this attention to detail that allows for a case to be built to most accurately support and settle the pending claim. By further leveraging tools to identify potential fraud or billing errors, the adjuster not only increases productivity but also gathers the proof necessary to support contentions gathered during the investigative phase. Consider a recent situation on a claim where the adjuster reviewed a lumbar MRI billed under CPT codes 72148 (MRI lumbar spine with contrast) and 72149 (MRI lumbar spine without contrast) for $4200 dollars. At first glance, the adjuster may not realize that this is an unbundling scheme that should have been billed as CPT
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:02.695Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0\" --max-time 30 \"https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi?db=pubmed&id=25430861&rettype=abstract&retmode=text\" | head -60",
 "description": "Fetch Brinjikji 2015 abstract from PubMed"
}
````

### User / tool · 2026-11-02T00:35:03.167Z

**tool result**
````
1. AJNR Am J Neuroradiol. 2015 Apr;36(4):811-6. doi: 10.3174/ajnr.A4173. Epub
2014  Nov 27.

Systematic literature review of imaging features of spinal degeneration in 
asymptomatic populations.

Brinjikji W(1), Luetmer PH(2), Comstock B(3), Bresnahan BW(4), Chen LE(4), Deyo 
RA(5), Halabi S(6), Turner JA(7), Avins AL(8), James K(4), Wald JT(1), Kallmes 
DF(1), Jarvik JG(9).

Author information:
(1)From the Department of Radiology (W.B., P.H.L., J.T.W., D.F.K.), Mayo Clinic, 
Rochester, Minnesota.
(2)From the Department of Radiology (W.B., P.H.L., J.T.W., D.F.K.), Mayo Clinic, 
Rochester, Minnesota luetmer.patrick@mayo.edu.
(3)Departments of Biostatistics (B.C.) Radiology (B.C., B.W.B., L.E.C., K.J., 
J.G.J.).
(4)Radiology (B.C., B.W.B., L.E.C., K.J., J.G.J.).
(5)Departments of Family Medicine, Medicine, and Public Health and Preventive 
Medicine and the Oregon Institute of Occupational Health Sciences (R.A.D.), 
Oregon Health and Science University, Portland, Oregon.
(6)Department of Radiology (S.H.), Henry Ford Hospital, Detroit, Michigan.
(7)Psychiatry and Behavioral Sciences (J.A.T.).
(8)Department of Radiology (A.L.A.), University of California, San Francisco, 
San Francisco, California Division of Research (A.L.A.), Kaiser Permanente, 
Northern California, Oakland, California.
(9)Radiology (B.C., B.W.B., L.E.C., K.J., J.G.J.) Neurological Surgery and 
Health Services (J.G.J.), Comparative Effectiveness Cost and Outcomes Research 
Center, University of Washington, Seattle, Washington.

BACKGROUND AND PURPOSE: Degenerative changes are commonly found in spine imaging 
but often occur in pain-free individuals as well as those with back pain. We 
sought to estimate the prevalence, by age, of common degenerative spine 
conditions by performing a systematic review studying the prevalence of spine 
degeneration on imaging in asymptomatic individuals.
MATERIALS AND METHODS: We performed a systematic review of articles reporting 
the prevalence of imaging findings (CT or MR imaging) in asymptomatic 
individuals from published English literature through April 2014. Two reviewers 
evaluated each manuscript. We selected age groupings by decade (20, 30, 40, 50, 
60, 70, 80 years), determining age-specific prevalence estimates. For each 
imaging finding, we fit a generalized linear mixed-effects model for the 
age-specific prevalence estimate clustering in the study, adjusting for the 
midpoint of the reported age interval.
RESULTS: Thirty-three articles reporting imaging findings for 3110 asymptomatic 
individuals met our study inclusion criteria. The prevalence of disk 
degeneration in asymptomatic individuals increased from 37% of 20-year-old 
individuals to 96% of 80-year-old individuals. Disk bulge prevalence increased 
from 30% of those 20 years of age to 84% of those 80 years of age. Disk 
protrusion prevalence increased from 29% of those 20 years of age to 43% of 
those 80 years of age. The prevalence of annular fissure increased from 19% of 
those 20 years of age to 29% of those 80 years of age.
CONCLUSIONS: Imaging findings of spine degeneration are present in high 
proportions of asymptomatic individuals, increasing with age. Many imaging-based 
degenerative features are likely part of normal aging and unassociated with 
pain. These imaging findings must be interpreted in the context of the patient's 
clinical condition.

© 2015 by American Journal of Neuroradiology.

DOI: 10.3174/ajnr.A4173
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:08.105Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0\" --max-time 30 \"https://www.ncbi.nlm.nih.gov/research/bionlp/RESTful/pmcoa.cgi/BioC_json/PMC4464797/unicode\" -o /tmp/brin.json; ls -la /tmp/brin.json; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,re\nd=json.load(open('/tmp/brin.json'))\nd=d[0] if isinstance(d,list) else d\ntxt=' '.join(p['text'] for doc in d['documents'] for p in doc['passages'])\nfor m in re.finditer(r'[^.]*\\b(lumbar|cervical)\\b[^.]*\\.',txt):\n    print('-',m.group(0).strip()[:300])\n\" | head -15",
 "description": "Check whether Brinjikji review covers lumbar or cervical spine"
}
````

### User / tool · 2026-11-02T00:35:08.538Z

**tool result**
````
-rw-r--r--@ 1 arsis  wheel  66702 Nov  1 18:35 /tmp/brin.json
- The initial concept was spinal diseases or disorders affecting the spine: intervertebral disk degeneration or displacement, spondylolysis, low back pain, or specific vertebrae and joints (eg, lumbar vertebrae).
- We also searched references from multiple articles to find any additional studies that reported lumbar spine CT or MR imaging findings in individuals without low back pain.
- Findings from this systematic review are being used to help physicians with clinical decision-making for patients with low back pain in the Lumbar Imaging With Reporting of Epidemiology: A Pragmatic Cluster Randomized Trial, a multicenter randomized controlled trial aimed at determining whether inse
- REFERENCES Diagnostic evaluation of low back pain with emphasis on imaging Cost, controversy, crisis: low back pain and the health of the public Effect of increased MRI and CT scan utilization on clinical decision-making in patients referred to a surgical clinic for back pain Are first-time episodes
- The incidence of positive CAT scans in an asymptomatic group of patients Nomenclature and classification of lumbar disc pathology: recommendations of the combined task forces of the North American Spine Society, American Society of Spine Radiology, and American Society of Neuroradiology Imaging of d
- 5-T MR images by using the Nordic Modic Consensus Group classification form Publication bias in meta-analysis: its causes and consequences Orientation of the lumbar facet joints: association with degenerative disc disease 1995 Volvo Award in clinical sciences: the diagnostic accuracy of magnetic res
- Their incidence and clinical relevance Cervical and lumbar MRI in asymptomatic older male lifelong athletes: frequency of degenerative findings Magnetic resonanceimaging of the lumbar spine in people without back pain Cross-sectional magnetic resonance imaging study of lumbar disc degeneration in 20
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:15.284Z

**tool call — Bash**
````
{
 "command": "for u in \"https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215\" \"https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/\"; do echo \"=== $u\"; curl -sL -A \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36\" --max-time 30 \"$u\" -o /tmp/p.html -w \"HTTP %{http_code} bytes %{size_download}\\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport re,html\nt=open('/tmp/p.html',encoding='utf-8',errors='ignore').read()\nt=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',t)\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\nfor k in ['physical therapy','sessions','mitigat','weeks','degenerative','reported','six to nine','6']:\n    for m in list(re.finditer(k,t,re.I))[:2]:\n        print(k,'::',t[max(0,m.start()-250):m.end()+250]); print()\n\" | head -60; done",
 "description": "Fetch Herrera and Virginia Lawyers Weekly sources"
}
````

### User / tool · 2026-11-02T00:35:17.145Z

**tool result**
````
=== https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215
HTTP 200 bytes 184376
physical therapy :: began treatment with Stephen Beck , a physician, at the Hospital for Special Care in New Britain. The plaintiff continued to see Beck every four to eight weeks for treatment of pain in her arms and legs and for headaches. The plaintiff also attended physical therapy sessions at Beck's request. The plaintiff , however, missed more than twelve scheduled physical therapy sessions over a seven month period for various reasons. Further, she testified that she "tried to make up the missed appointments." Prior to the 

physical therapy :: aintiff continued to see Beck every four to eight weeks for treatment of pain in her arms and legs and for headaches. The plaintiff also attended physical therapy sessions at Beck's request. The plaintiff , however, missed more than twelve scheduled physical therapy sessions over a seven month period for various reasons. Further, she testified that she "tried to make up the missed appointments." Prior to the accident, the plaintiff had been active in sports and other physical activities. In May, 1995 , Beck ind

sessions :: ith Stephen Beck , a physician, at the Hospital for Special Care in New Britain. The plaintiff continued to see Beck every four to eight weeks for treatment of pain in her arms and legs and for headaches. The plaintiff also attended physical therapy sessions at Beck's request. The plaintiff , however, missed more than twelve scheduled physical therapy sessions over a seven month period for various reasons. Further, she testified that she "tried to make up the missed appointments." Prior to the accident,

sessions ::  to see Beck every four to eight weeks for treatment of pain in her arms and legs and for headaches. The plaintiff also attended physical therapy sessions at Beck's request. The plaintiff , however, missed more than twelve scheduled physical therapy sessions over a seven month period for various reasons. Further, she testified that she "tried to make up the missed appointments." Prior to the accident, the plaintiff had been active in sports and other physical activities. In May, 1995 , Beck indicated to

mitigat :: llee ( defendant ) . Opinion ZARELLA , J. The plaintiff , Linda Herrera , appeals from the judgment rendered after a jury trial awarding her $5000 in damages. On appeal, the plaintiff claims that the trial court improperly (1) instructed the jury on mitigation of damages when the evidence did not warrant such a charge, (2) failed to instruct the jury on the burden of proof with respect to mitigation of damages and (3) abused its discretion in denying the plaintiff 's motion to set aside the verdict and

mitigat :: 5000 in damages. On appeal, the plaintiff claims that the trial court improperly (1) instructed the jury on mitigation of damages when the evidence did not warrant such a charge, (2) failed to instruct the jury on the burden of proof with respect to mitigation of damages and (3) abused its discretion in denying the plaintiff 's motion to set aside the verdict and for additur . 1 We reverse in part the judgment of the trial court and remand the case for a new trial on the issue of damages. The jury reas

weeks ::  medication. After three days, the plaintiff returned to work but still suffered from pain. She began treatment with Stephen Beck , a physician, at the Hospital for Special Care in New Britain. The plaintiff continued to see Beck every four to eight weeks for treatment of pain in her arms and legs and for headaches. The plaintiff also attended physical therapy sessions at Beck's request. The plaintiff , however, missed more than twelve scheduled physical therapy sessions over a seven month period for

6 ::  Herrera v. Madrak (Herrera v. Madrak, 752 A.2d 1161, 58 Conn.App. 320 (Conn. App. 2000)) - vLex United States VINCENT AI Legal Research Coverage DOCKET ALARM Login Sign Up Home Case Law Herrera v. Madrak Document Cited authorities (18) Cited in (13) Precedent Map Related Court Connecticut Court of A

6 :: earch Coverage DOCKET ALARM Login Sign Up Home Case Law Herrera v. Madrak Document Cited authorities (18) Cited in (13) Precedent Map Related Court Connecticut Court of Appeals Writing for the Court ZARELLA, J. Citation Herrera v. Madrak, 752 A.2d 1161, 58 Conn.App. 320 (Conn. App. 2000) Decision Date 20 June 2000 Docket Number (AC 18735) Parties LINDA HERRERA v. JESSE MADRAK 58 Conn. App. 320 752 A.2d 1161 LINDA HERRERA v. JESSE MADRAK (AC 18735) Appellate Court of Connecticut . Argued February 

=== https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/
HTTP 200 bytes 200884
physical therapy ::  of the lumbar spine were performed, which revealed significant degenerative disc disease at multiple levels. Over the next few weeks, plaintiff’s low back pain worsened, prompting him to follow up with his family physician. After a failed course of physical therapy, an MRI was performed which revealed a moderate disc herniation at L3-4 compressing the thecal sac. Other degenerative changes of the lumbar spine were also demonstrated on the MRI, including spinal stenosis, facet joint arthropathy and other disc h

weeks :: s after the collision but did not report injury until eight days later when he was seen at an urgent care facility. X-rays of the lumbar spine were performed, which revealed significant degenerative disc disease at multiple levels. Over the next few weeks, plaintiff’s low back pain worsened, prompting him to follow up with his family physician. After a failed course of physical therapy, an MRI was performed which revealed a moderate disc herniation at L3-4 compressing the thecal sac. Other degenerati

degenerative :: e 264 in Norfolk. Plaintiff developed low back pain several hours after the collision but did not report injury until eight days later when he was seen at an urgent care facility. X-rays of the lumbar spine were performed, which revealed significant degenerative disc disease at multiple levels. Over the next few weeks, plaintiff’s low back pain worsened, prompting him to follow up with his family physician. After a failed course of physical therapy, an MRI was performed which revealed a moderate disc hernia

degenerative ::  few weeks, plaintiff’s low back pain worsened, prompting him to follow up with his family physician. After a failed course of physical therapy, an MRI was performed which revealed a moderate disc herniation at L3-4 compressing the thecal sac. Other degenerative changes of the lumbar spine were also demonstrated on the MRI, including spinal stenosis, facet joint arthropathy and other disc herniations above and below L3-4. Plaintiff was referred for a neurosurgical consultation. Plaintiff’s neurosurgeon orde

reported ::  4-3 ruling The Supreme Court of Virginia invalidated a redistricting referendum that would have favored Democra[...] Million Dollar Plus Settlements of 2025 Listen to this article Following are settlements of at least $1 million reached in 2025 and reported[...] Goochland supervisors OK $250K to fight lawsuit over potential data centers Goochland County shifts $250K to hire outside counsel as it faces a lawsuit challenging a technology[...] Important opinions published in Virginia Lawyers Weekly Listen

six to nine ::  Felix Kirven, M.D., a local orthopedic surgeon, to perform a medical record review and to testify at trial. Dr. Kirven testified that plaintiff sustained a lumbar strain in the collision and that to the extent plaintiff remained symptomatic after a six to nine week period, such was attributable to plaintiff’s pre-existing degenerative disc disease and not any accident related injury. Dr. Kirven also testified that the presence of disc protrusions at adjacent levels of the lumbar spine corroborated his opi

6 :: ls in disputed back injury case – $100,000 Verdict Plaintiff prevails in disputed back injury case – $100,000 Verdict Virginia Lawyers Weekly // October 9, 2014 // --> Listen to this article This case arose out of a rear end collision on Interstate 264 in Norfolk. Plaintiff developed low back pain several hours after the collision but did not report injury until eight days later when he was seen at an urgent care facility. X-rays of the lumbar spine were performed, which revealed significant dege

6 :: ct in the amount of $100,000, the exact amount of the liability insurance coverage. [14-T-135] Type of action: Personal injury – auto accident Injuries alleged: Acute disc herniation of the lumbar spine Name of case: Morris v. Elliott Case no.: CL13-6170 Court: Norfolk Circuit Court Tried before: Jury Date: Aug. 27, 2014 Special damages: Medical expenses – $39,370; lost wages – $3,222 Last offer: $27,500 Verdict or settlement: Verdict Amount: $100,000 Attorney for plaintiff: Derrick L. Walker, Vi
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:22.544Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36\" --max-time 30 \"https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215\" -o /tmp/h.html; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport re,html\nt=open('/tmp/h.html',encoding='utf-8',errors='ignore').read()\nt=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',t)\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\nfor k in ['we conclude','we agree','we disagree','was warranted','properly instructed','burden of proof','reasonable to']:\n    for m in list(re.finditer(k,t,re.I))[:2]:\n        print(k,'::',t[max(0,m.start()-300):m.end()+300]); print()\n\" | head -40",
 "description": "Check Herrera holding on mitigation instruction"
}
````

### User / tool · 2026-11-02T00:35:22.798Z

**tool result**
````
we conclude :: r the exception. See generally Herrera v. Madrak, 58 Conn.App. 320, 323, 752 A.2d 1161 (2000) .Our review of the record provided reveals that the first time the plaintiff raised his claim that the court should h...... Drake v. Bingham United States Connecticut Court of Appeals September 27, 2011 ...We conclude that the court did not err by instructing the jury on the doctrine of mitigation of damages. In Herrera v. Madrak, 58 Conn.App. 320, 324, 752 A.2d 1161 (2000) , this court held that there was evidence sufficient to warrant a jury charge on mitigation of damages where the plaintif...... Get Started 

we disagree :: es of law.... Thus, we must determine whether the charge as a whole presents the case to the jury so that no injustice will be done." ( Citation omitted ; internal quotation marks omitted .) Stewart v. Federated Dept. Stores, Inc. , 234 Conn. 597, 603 , 662 A.2d 753 ( 1995 ) . Upon review, however, we disagree with the plaintiffs claim that the trial court should not have instructed the jury on the doctrine of mitigation of damages. There was evidence sufficient to warrant the instruction. The plaintiff had missed more than twelve physical therapy appointments over a seven month period. The decision to i

properly instructed :: ten months later and resumed treatment with Beck. Additionally, the jury heard testimony from the plaintiff that the pain interfered with her ability to work at her job as a paralegal and adversely affected her ability to participate in athletics. I The plaintiff first claims that the trial court improperly instructed the jury on mitigation of damages when the evidence did not warrant the jury instruction. Prior to addressing this issue, we first consider whether it was properly preserved at trial. After the court delivered its instruction, the plaintiff took exception by stating, "I preserve my exception on the

burden of proof :: nda Herrera , appeals from the judgment rendered after a jury trial awarding her $5000 in damages. On appeal, the plaintiff claims that the trial court improperly (1) instructed the jury on mitigation of damages when the evidence did not warrant such a charge, (2) failed to instruct the jury on the burden of proof with respect to mitigation of damages and (3) abused its discretion in denying the plaintiff 's motion to set aside the verdict and for additur . 1 We reverse in part the judgment of the trial court and remand the case for a new trial on the issue of damages. The jury reasonably could have found th

burden of proof :: rns v. Hanson , 249 Conn. 809, 832 , 734 A.2d 964 ( 1999 ) . We find no abuse of that discretion by the trial court when it gave the instruction. II The plaintiff next claims that the court , having given the mitigation of damages charge, was required to give an additional instruction regarding the burden of proof. The record reflects that the plaintiff did not submit any specific requests to charge the jury and did not take exception to the lack of a burden of proof instruction. "In State v. Butler , 207 Conn. 619, 630 , 543 A.2d 270 ( 1988 ) , this court held that where a defendant fails to make a request
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:31.219Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 Chrome/120 Safari/537.36\" --max-time 30 \"https://www.studicata.com/summaries/court-of-appeal-of-louisiana/fletcher-v-simmons-2003-l2aha0\" -o /tmp/f.html -w \"HTTP %{http_code} bytes %{size_download}\\n\"; /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport re,html\nt=open('/tmp/f.html',encoding='utf-8',errors='ignore').read()\nt=re.sub(r'(?s)<script.*?</script>|<style.*?</style>','',t)\nt=html.unescape(re.sub(r'<[^>]+>',' ',t)); t=re.sub(r'\\s+',' ',t)\ni=t.lower().find('mitigat'); print(t[:300]); print('...'); print(t[max(0,i-1500):i+1500] if i>=0 else t[:3000])\n\"",
 "description": "Verify Fletcher v. Simmons source exists and supports claim"
}
````

### User / tool · 2026-11-02T00:35:31.983Z

**tool result**
````
HTTP 403 bytes 1398
 Access Denied Access denied This case summary is only available to active Case Briefs+ members. Get instant access to this case summary and 4 million+ more case summaries: Start your 7-day free trial 
...
 Access Denied Access denied This case summary is only available to active Case Briefs+ members. Get instant access to this case summary and 4 million+ more case summaries: Start your 7-day free trial
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:34.730Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0\" --max-time 30 \"https://www.courtlistener.com/api/rest/v4/search/?q=%22Fletcher%22+%22Simmons%22+mitigat*&type=o&court=lactapp\" | /Users/arsis/zlayt-pm-project/.venv/bin/python -c \"\nimport json,sys\ntry:\n  d=json.load(sys.stdin)\n  for r in d.get('results',[])[:8]: print(r.get('caseName'),r.get('dateFiled'),r.get('citation'))\n  print('count',d.get('count'))\nexcept Exception as e: print('err',e)\n\"",
 "description": "Search CourtListener for Fletcher v. Simmons"
}
````

### User / tool · 2026-11-02T00:35:35.783Z

**tool result**
````
count None
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:37.968Z

**tool call — Bash**
````
{
 "command": "curl -sL -A \"Mozilla/5.0\" --max-time 30 \"https://www.courtlistener.com/api/rest/v4/search/?q=caseName%3A(Fletcher+AND+Simmons)&type=o\" | head -c 1500; echo; curl -sL -A \"Mozilla/5.0\" --max-time 30 \"https://www.courtlistener.com/api/rest/v3/search/?q=caseName%3A(Fletcher+AND+Simmons)&type=o\" | head -c 800",
 "description": "Retry CourtListener case-name search"
}
````

### User / tool · 2026-11-02T00:35:38.288Z

**tool result**
````
{"detail":"Authentication credentials were not provided."}
{"detail":"Anonymous users don't have permission to access the API. "}
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:42.315Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; grep -n -i \"lexicon\\|flag_type\\|compliance\\|prior_condition\\|LEXICON_ONLY\" docs/CONTRACT.md app -r 2>/dev/null | grep -v \"^app/llm/lexicon.yaml\" | head -30; git log --format='%h %ad %s' --date=iso -8",
 "description": "Find contract mentions of lexicon and flag types"
}
````

### User / tool · 2026-11-02T00:35:42.410Z

**tool result**
````
docs/CONTRACT.md:83: frontend · qa · release        privacy-compliance · product-manager · ux-designer ·
docs/CONTRACT.md:238:Write one file per role in `.claude/agents/` using the template in Appendix D.5. Workers: `architect, backend, db, frontend, qa, release, writer, researcher`. Reviewers: `paralegal-reviewer, litigation-lead-reviewer, claims-adjuster-reviewer, legal-nurse-reviewer, privacy-compliance-reviewer, product-manager-reviewer, ux-designer-reviewer, staff-engineer-reviewer, security-reviewer, chaos-tester-reviewer, accessibility-reviewer, installer-reviewer, hiring-panel-reviewer`. Keep `description` fields to one or two lines (the combined-description budget is 15k tokens); put depth in the body. Reviewer bodies are compiled from the researched dossiers in M1 — in M0 write provisional versions marked `PROVISIONAL` so the roster exists.
docs/CONTRACT.md:265:- **Domain research** (researcher, Opus): how personal-injury paralegals build treatment chronologies / medical summaries for demand packages; what adjusters and defense counsel attack (gaps in treatment, pre-existing and degenerative findings, inconsistent dates, missed appointments, subjective vs objective findings, causation language such as "may represent," "correlate clinically," "patient reports"); Texas PI practice norms relevant to the scenario; how firms handle PHI and non-lawyer supervision of AI output. Use `/deep-research` if available; otherwise parallel researcher subagents. Output: `research/*.md` with sources, `memory/GLOSSARY.md`, and a **flag lexicon** (`app/llm/lexicon.yaml`) with per-phrase rationale and source.
docs/CONTRACT.md:286:| Pre-existing / prior conditions | LLM classification + lexicon (`lexicon.yaml`) as a second deterministic signal | Language judgment | Judge; lexicon hit without LLM hit (or vice versa) → "needs review"; human. |
docs/CONTRACT.md:302:Cards (backend, db, qa; architect consults): data model + persistence (db); ingest/split/date parsing (backend); generator extraction with structured output (backend); grounding verifier (backend — write it first, test-first); judges #1–#3 (backend); flag engines: gaps (code), amounts (code+LLM), conflicts (hybrid), pre-existing + causation (LLM+lexicon) (backend); audit log (db/backend); eval runner + report (qa): grounding rate, entry recall, amount recall, flag precision/recall per flag type, judge recall on seeded hallucinations (qa injects 20 synthetic unsupported summaries; judge must catch ≥ 95%), determinism across 3 runs; CLI `python -m app.pipeline evals/golden/sample.txt` prints the full result for the sample case.
docs/CONTRACT.md:304:Gate panel: staff-engineer, qa (eval report attached), paralegal, legal-nurse, claims-adjuster (reads the sample-case output and tries to discredit it), privacy-compliance (prompt-injection probe result, PHI handling design). Exit: evals meet the ship bar (§8.2), zero blockers, tag `m2`.
docs/CONTRACT.md:316:Gate panel: security, privacy-compliance, installer-reviewer (clones into a clean temp directory and times the README path; must be under 5 minutes), qa, release self-check against the HF/Replit requirements. Exit: tag `m4`.
docs/CONTRACT.md:343:| `researcher` (**`model: opus`**) | Domain research, persona dossiers, glossary, flag lexicon with sources. The quality of every reviewer depends on this work. | `research/**`, `personas/**`, `memory/GLOSSARY.md`, `app/llm/lexicon.yaml` (hands to backend) |
docs/CONTRACT.md:353:| `privacy-compliance-reviewer` | opus | Privacy/compliance counsel. PHI handling and retention, synthetic-data-only guardrails, prompt injection via record text, logging of LLM calls, AI disclosure, what "no invented facts" requires technically. |
docs/CONTRACT.md:381:- **Tier 1 (per card):** every card moving to `in_review` gets `staff-engineer-reviewer` (or `product-manager-reviewer` for documents) **plus one domain persona** chosen by the card's subject (e.g., anything touching flags → `claims-adjuster`; anything touching the UI flow → `paralegal`; anything touching prompts → `legal-nurse` + `privacy-compliance`). Run in parallel, background.
docs/CONTRACT.md:425:Any change to a prompt, model, lexicon, or schema requires re-running `evals.run` before `in_review`; the eval report path goes in the card handoff. Store prompts in versioned files (`app/llm/prompts/*.md`) with a changelog line each.
app/README-arch.md:23:  gaps.py  conflicts.py  flags.py   code flag engines + calls to LLM passes and lexicon
app/README-arch.md:32:  lexicon.yaml   [researcher] phrase list with rationale and source
app/README-arch.md:44:6. `gaps` (code), 7. `conflicts` (code structural + one LLM pass, J3), 8. `flags` (LLM pass + lexicon + J4), 9. `finalize` (compose states, sort).
9e759a2 2026-11-01 18:33:54 -0600 fix(harness): round-2 hardening from M0 security and staff-engineer reviews
8a22a5c 2026-11-01 18:30:34 -0600 docs(research): PHI handling and AI-output supervision for Texas PI firm (T-012)
64f766e 2026-11-01 18:29:00 -0600 docs(spec): requirements round 2: split letter vs internal notes, edit rules, export template
f419c3b 2026-11-01 18:28:02 -0600 feat(research): flag lexicon with negation guard and test vectors (T-009)
0a10094 2026-11-01 18:27:18 -0600 feat(personas): product/engineering reviewer dossiers (PM, UX, staff-eng, security, chaos, a11y, installer, hiring-panel)
34e9398 2026-11-01 18:27:14 -0600 feat(personas): domain reviewer dossiers (paralegal, litigation-lead, claims-adjuster, legal-nurse, privacy-compliance)
47520a8 2026-11-01 18:25:39 -0600 feat(evals): golden set - sample case, 8 synthetic cases, 20 seeded hallucinations, validator
94c7b08 2026-11-01 18:22:54 -0600 docs(architect): ADRs, LLM/code table, API contract draft
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:47.871Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python -c \"\nimport json\nfor f in ['case_06_subtle_pre_existing','sample']:\n  d=json.load(open(f'evals/golden/{f}.expected.json'))\n  for fl in d.get('flags',[]): print(f, json.dumps(fl)[:400])\n\"",
 "description": "Show golden expected flags for case_06 and sample"
}
````

### User / tool · 2026-11-02T00:35:47.960Z

**tool result**
````
case_06_subtle_pre_existing {"id": "P1", "type": "pre_existing", "level": "must", "cite": {"all": [2], "any": []}, "evidence": [{"record_no": 2, "field": "excerpt", "excerpt": "off and on since a lifting injury several years ago"}], "summary": "Ongoing chiropractic care dating to an earlier lifting injury; body region not stated in the record.", "subtype": "prior_injury_prior_treatment"}
case_06_subtle_pre_existing {"id": "P2", "type": "pre_existing", "level": "should", "cite": {"all": [3], "any": []}, "evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "occasional stiffness in the mornings at baseline"}], "summary": "Baseline morning stiffness in the history; region not stated.", "subtype": "baseline_symptom"}
case_06_subtle_pre_existing {"id": "P3", "type": "pre_existing", "level": "should", "cite": {"all": [5], "any": []}, "evidence": [{"record_no": 5, "field": "excerpt", "excerpt": "the old shoulder problem is acting up again"}], "summary": "A prior shoulder problem is mentioned (different region from the neck complaints).", "subtype": "prior_other_region"}
sample {"id": "G1", "type": "gap", "level": "must", "from_date": "2026-03-06", "to_date": "2026-05-18", "days": 73, "cite": {"all": [6, 7], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}, {"record_no": 7, "field": "excerpt", "excerpt": "New onset pain radiating to right arm"}], "summary": "Treatment gap of 73 days (2026-03-06 t
sample {"id": "C1", "type": "conflict", "level": "must", "cite": {"all": [7], "any": [1, 2]}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}, {"record_no": 1, "field": "excerpt", "excerpt": "rear-ended at approx. 35 mph"}, {"record_no": 2, "field": "excerpt", "excerpt": "CT head negative"}], "summary": "Accident date conflict: 2026-01-09 per E
sample {"id": "C2", "type": "conflict", "level": "must", "cite": {"all": [4, 6], "any": []}, "evidence": [{"record_no": 4, "field": "excerpt", "excerpt": "Plan of care: 12 visits"}, {"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Treatment-plan discrepancy: 12 visits planned (record 4) vs discharge at visit 9 after two missed appointments 
sample {"id": "P1", "type": "pre_existing", "level": "must", "cite": {"all": [3], "any": []}, "evidence": [{"record_no": 3, "field": "excerpt", "excerpt": "Patient reports low back pain in 2023, resolved"}], "summary": "Prior low back pain (2023), reported resolved. Different body region from the cervical complaints; the tool must not relate it to the neck.", "subtype": "prior_condition_reported"}
sample {"id": "P2", "type": "pre_existing", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "Findings may represent degenerative change"}], "summary": "MRI wording raises possible degenerative (pre-existing) change; hedged, not a diagnosis.", "subtype": "degenerative_language"}
sample {"id": "K1", "type": "causation", "level": "must", "cite": {"all": [8], "any": []}, "evidence": [{"record_no": 8, "field": "excerpt", "excerpt": "may represent degenerative change; correlate clinically"}], "summary": "Hedged imaging language that an adjuster can use against causation.", "subtype": "hedged_imaging"}
sample {"id": "K2", "type": "causation", "level": "must", "cite": {"all": [6], "any": []}, "evidence": [{"record_no": 6, "field": "excerpt", "excerpt": "Discharged from PT after two missed appointments"}], "summary": "Missed appointments / early discharge weaken the treatment-compliance narrative.", "subtype": "noncompliance"}
sample {"id": "K3", "type": "causation", "level": "must", "cite": {"all": [9], "any": []}, "evidence": [{"record_no": 9, "field": "excerpt", "excerpt": "Patient states symptoms began after the January collision"}], "summary": "Causation rests on patient self-report, not a physician's causation opinion.", "subtype": "patient_self_report"}
sample {"id": "K4", "type": "causation", "level": "should", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "New onset pain radiating to right arm"}], "summary": "'New onset' symptoms after a 73-day gap can be argued as a new cause. Overlaps G1; credit if surfaced either here or on G1.", "subtype": "temporal_after_gap"}
sample {"id": "K5", "type": "causation", "level": "should", "cite": {"all": [7], "any": []}, "evidence": [{"record_no": 7, "field": "excerpt", "excerpt": "Date of accident per intake form: 2026-01-19"}], "summary": "Wrong accident date on intake form undermines reliability. Overlaps C1.", "subtype": "accident_date_inconsistency"}
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:35:59.057Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; for f in research/chronology-practice.md research/adjuster-attacks.md research/texas-pi-notes.md; do echo \"$f: $(grep -cE '^[0-9]+\\. .*https?://' $f)\"; done; echo \"glossary terms: $(grep -cE '^- \\*\\*' memory/GLOSSARY.md)\"; grep -E '^- \\*\\*' memory/GLOSSARY.md | grep -vciE 'Source:'; echo \"assumptions: $(grep -cE '^\\| P-[0-9]+' research/ASSUMPTIONS-proposed.md)\"; grep -n -i \"delay\\|first treatment\\|property damage\\|MIST\\|minor impact\\|attorney\\|passive\\|IME\" research/adjuster-attacks.md | head",
 "description": "Verify T-008 AC counts and search attack coverage"
}
````

### User / tool · 2026-11-02T00:35:59.176Z

**tool result**
````
research/chronology-practice.md: 10
research/adjuster-attacks.md: 18
research/texas-pi-notes.md: 11
glossary terms: 38
0
assumptions: 13
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:36:16.892Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; sed -n 62,66p spec/SPEC.md",
 "description": "Show sample records 6-9 in spec"
}
````

### User / tool · 2026-11-02T00:36:16.970Z

**tool result**
````
| 6 | 2026-03-06 | Capital PT, visit 9 | "Discharged from PT after two missed appointments. Pain 3/10." |
| 7 | 2026-05-18 | Hill Country Pain Management, new patient | "New onset pain radiating to right arm with numbness in fingers. Pain 7/10. MRI ordered. Date of accident per intake form: 2026-01-19." |
| 8 | 2026-05-29 | Austin Imaging, cervical MRI | "C5-C6 disc protrusion with mild right foraminal narrowing. Findings may represent degenerative change; correlate clinically. Charge: $2,150." |
| 9 | 2026-06-12 | Hill Country Pain Management, follow-up | "Recommend cervical epidural steroid injection. Patient states symptoms began after the January collision." |
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:36:47.059Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; cat > artifacts/review-evidence/T-008-adjuster-source-checks.txt <<'EOF'\nT-008 claims-adjuster source spot-checks (2026-11-01). Fetched with curl (WebFetch not available to this reviewer).\n\n1) AA src 1 — Claims Journal, Tidball 2013 — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm (HTTP 200, 74,425 bytes)\n   Verbatim: \"1) Police report – Was there mention of any injury at the scene? Was the injured party transported to a medical facility?\"\n   Verbatim: \"2) Vehicle photographs (auto claims) – Does the damage match? Are there paint transfers? What is the directional force of impact?\"\n   Verbatim: \"5) Treatment patterns – How soon did treatment start? Were there gaps in treatment? Was there treatment on evenings and/or weekends?\"\n   Verbatim: \"6) Provider type – Was the claimant seen by a chiropractor or medical doctor?\"\n   Verbatim: \"7) Duration and frequency – When did treatment start? How long did it last? Was it active or passive? Was it longer than an anticipated expected recovery date...\"\n   Result: takeaway in AA is accurate, but the attack map (A1-A11) has no row for delay-to-first-treatment, vehicle damage/MIST,\n   transport at scene, provider type, active vs passive care, or duration vs expected recovery.\n   `grep -n -i \"delay\\|first treatment\\|property damage\\|MIST\\|minor impact\\|attorney\\|passive\\|IME\" research/adjuster-attacks.md` -> no output.\n\n2) AA src 6 — Brinjikji et al., AJNR 2015 — PubMed efetch id 25430861 + PMC4464797 BioC full text\n   Abstract figures CONFIRMED: \"Disk bulge prevalence increased from 30% of those 20 years of age to 84% of those 80 years of age.\n   Disk protrusion prevalence increased from 29% ... to 43%\".\n   Scope: full text: \"We also searched references from multiple articles to find any additional studies that reported lumbar spine CT or MR\n   imaging findings in individuals without low back pain.\" -> a LUMBAR review. adjuster-attacks.md:49-50 applies it to\n   \"a C5-C6 protrusion in a 41-year-old\" (cervical).\n\n3) AA src 14 — Herrera v. Madrak, 58 Conn.App. 320 (2000) — https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215 (HTTP 200)\n   CONFIRMED: \"There was evidence sufficient to warrant the instruction. The plaintiff had missed more than twelve physical therapy\n   appointments over a seven month period.\" (Connecticut; AA labels it non-Texas — OK.)\n   Fletcher v. Simmons (studicata URL) -> HTTP 403 \"only available to active Case Briefs+ members\"; not verifiable by me.\n\n4) AA src 16 — Virginia Lawyers Weekly 2014 — https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/ (HTTP 200)\n   CONFIRMED AA takeaway: \"to the extent plaintiff remained symptomatic after a six to nine week period, such was attributable to\n   plaintiff's pre-existing degenerative disc disease\".\n   Same page: \"did not report injury until eight days later when he was seen at an urgent care facility\" — lexicon.yaml:443\n   (delayed_onset) paraphrases this as \"symptoms not reported until weeks later\" (overstated: 8 days). It is also direct support for\n   a delay-to-first-treatment attack that AA does not list.\nEOF\necho done",
 "description": "Save source spot-check evidence file"
}
````

### User / tool · 2026-11-02T00:36:47.181Z

**tool result**
````
done
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:36:50.454Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; head -20 reviews/T-013-paralegal.md; grep -n \"verdict\" tools/board.py | head",
 "description": "Check existing review format and validator"
}
````

### User / tool · 2026-11-02T00:36:50.541Z

**tool result**
````
# T-013 review — paralegal-reviewer

**Verdict: fail** (1 blocker, 9 majors, 6 minors).

The requirements get the hard truths right: the rate-not-charge handling, the "not merged" accident dates, the self-report label on
record 9, nothing accepted by default, and the negative assertions are all there, word for word. The document fails at the end of
the job, though. As written, the copy-ready letter text includes the flags I accepted, so the defense's arguments end up in our own
demand letter. The export also has no template, so nothing says what a pasted line looks like. Several gaps let a correct-looking
chronology mislead an adjuster: excerpts can drop the hedge, provider names are never checked against the record, nothing stops a
duplicate bill from being totaled twice, records that drop out of the chronology are never disclosed, and the PT rate and the total
have no export wording.

Exercised (paper walkthrough; no app exists at this card): I ran all 9 sample records by hand through every R-ID group and wrote down the
timeline, flags, charges and the literal export → `artifacts/review-evidence/T-013-paralegal-walkthrough.md`. I recomputed the gaps and
the total in Python. I read spec/REQUIREMENTS.md@65894f6 (no diff to HEAD), SPEC Appendix A, SAMPLE_CASE_TRUTHS, CONTRACT §5 M1/§5.2/§8.2/D.2/D.4,
memory/ASSUMPTIONS.md, and docs/LLM_VS_CODE.md (written 2 minutes after this commit; cited where it contradicts REQUIREMENTS). Agent memory
directory was empty; I did not write to it because it is outside my permitted paths.

```json
{"card": "T-013", "persona": "paralegal-reviewer", "model": "claude-opus-5-5",
305:        if not isinstance(r, dict) or r.get("verdict") not in VERDICTS or not r.get("persona"):
318:        latest[r["persona"]] = r["verdict"]
624:                raise BoardError("cannot move to done: needs >=1 passing review and every persona's latest verdict = pass")
707:    if a.verdict not in VERDICTS:
708:        raise BoardError(f"verdict must be one of {VERDICTS}")
716:    if d.get("verdict") != a.verdict:
717:        raise BoardError(f"--verdict {a.verdict} does not match the review file's verdict {d.get('verdict')!r}")
722:        meta.setdefault("reviews", []).append({"persona": a.persona, "model": a.model, "verdict": a.verdict,
724:        msg = f"review {a.persona} ({a.model}): {a.verdict} — {a.file}"
725:        if a.verdict in ("changes", "fail") and meta["status"] == "in_review":
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:37:35.581Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster.md",
 "content": "# T-008 review — claims-adjuster-reviewer\n\n**Verdict: changes** (0 blockers, 2 majors, 3 minors, 1 nit).\n\nAll four ACs are met as written: `grep -cE '^[0-9]+\\. .*https?://'` returns chronology-practice.md 10, adjuster-attacks.md 18,\ntexas-pi-notes.md 11. GLOSSARY has 38 `- **` term lines, all with a source or \"assumption\". ASSUMPTIONS-proposed has 13 P-rows.\nThe attack map ties each attack to the exact Rivera excerpt, and the day counts are right (73 days 03-06→05-18; 129 days 01-09→05-18).\nAs the adjuster, my objection is what the map leaves out. The insurer-side checklist the researcher cites (Claims Journal, src 1)\nstarts with \"How soon did treatment start?\", vehicle damage, and whether the claimant was transported from the scene. None of those\nmade it into A1–A11. Attorney-driven care, active vs. passive care, and duration vs. expected recovery are missing too. Those are my\nfirst moves on a soft-tissue demand, and because T-009 builds on this map, the lexicon misses them as well (see T-009 review).\nOne cited study is stretched beyond its scope (a lumbar review used for a cervical finding), and one claim cites a source that isn't\nlisted.\n\nExercised: `python3 tools/board.py show T-008` (ACs above). I read all four research files and memory/GLOSSARY.md at HEAD (commit\n2c76cda content). I re-counted sources, glossary terms and P-rows with grep (output above). I ran a coverage grep:\n`grep -n -i \"delay\\|first treatment\\|property damage\\|MIST\\|minor impact\\|attorney\\|passive\\|IME\" research/adjuster-attacks.md` →\nno output. I spot-checked 4 sources with curl (WebFetch isn't in my toolset): Claims Journal src 1, Brinjikji src 6 (PubMed abstract\nplus PMC full text), Herrera v. Madrak src 14 (vLex), and Virginia Lawyers Weekly src 16. Fletcher v. Simmons returned HTTP 403\n(paywall). Verbatim excerpts are in `artifacts/review-evidence/T-008-adjuster-source-checks.txt`. I checked the claims against\npersonas/claims-adjuster.md §2/§4, spec Appendix A/C, and evals/golden/sample.expected.json. Agent memory was empty at start.\n\n```json\n{\"card\": \"T-008\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"research/chronology-practice.md, research/adjuster-attacks.md, research/texas-pi-notes.md, research/ASSUMPTIONS-proposed.md, memory/GLOSSARY.md (commit 2c76cda, read at HEAD 9e759a2); no app; Jordan Rivera sample case\",\n \"exercised\": [\n  \"python3 tools/board.py show T-008 (4 ACs, all marked done)\",\n  \"grep -cE '^[0-9]+\\\\. .*https?://' on the three research files -> 10 / 18 / 11\",\n  \"grep -cE '^- \\\\*\\\\*' memory/GLOSSARY.md -> 38 terms; every line contains 'Source:'\",\n  \"grep -cE '^\\\\| P-[0-9]+' research/ASSUMPTIONS-proposed.md -> 13\",\n  \"grep -n -i 'delay|first treatment|property damage|MIST|minor impact|attorney|passive|IME' research/adjuster-attacks.md -> no output\",\n  \"curl Claims Journal src 1 (HTTP 200) and extracted the 10-point medical-records checklist verbatim\",\n  \"curl PubMed efetch 25430861 + PMC4464797 BioC full text for Brinjikji src 6 (figures confirmed; lumbar-only scope found)\",\n  \"curl vLex Herrera v. Madrak src 14 (holding confirmed: >12 missed PT appointments warranted mitigation charge)\",\n  \"curl Virginia Lawyers Weekly src 16 (takeaway confirmed; 'eight days later' delayed report found)\",\n  \"curl studicata Fletcher v. Simmons -> HTTP 403, unverifiable\",\n  \"Recomputed Rivera day counts by hand: 73 (03-06->05-18), 129 (01-09->05-18), 28 (01-23->02-20)\",\n  \"Read personas/claims-adjuster.md, spec/SPEC.md Appendix A, spec/SAMPLE_CASE_TRUTHS.md, evals/golden/sample.expected.json\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"source_quality_and_labeling\": 4, \"adversarial_coverage\": 2, \"accuracy_vs_sources\": 3, \"texas_relevance\": 4, \"usefulness_to_flags_and_lexicon\": 3},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Attack map omits delay to first treatment, the adjuster's first check\",\n   \"evidence\": \"research/adjuster-attacks.md:16-28 (A1-A11) has no delay/first-treatment row; coverage grep for 'delay|first treatment' -> no output. Cited src 1 says verbatim: '5) Treatment patterns – How soon did treatment start? Were there gaps in treatment?' and '7) Duration and frequency – When did treatment start?' Src 16 (also cited) says verbatim: 'did not report injury until eight days later when he was seen at an urgent care facility.' personas/claims-adjuster.md §2: 'What he looks for first: accident date vs first-treatment date'; §4 item 2.\",\n   \"why_it_matters\": \"Delay between the accident and first care is the strongest 'not really hurt' argument and is separate from a gap between visits (A1). It isn't in the research, so it isn't in the lexicon or ASSUMPTIONS, and no flag or field is planned for it. For Rivera the delay is 0 days (EMS on 2026-01-09), which helps the claimant, and the paralegal should see it. On another case, a 5-day delay will be the first line of my response.\",\n   \"fix\": \"Add attack A12 'Delay to first treatment': what the defense argues; sources 1 and 16; Rivera = same day (record 1 EMS, record 2 ER). Note that code computes it from the earliest accident date to the first date of service, and that it must use both accident dates when they conflict (01-09 vs 01-19). Propose a matching P-row and a GLOSSARY term ('delay in treatment').\",\n   \"acceptance_test\": \"grep -n -i 'first treatment' research/adjuster-attacks.md returns an attack-map row citing src 1 with the Rivera value (0 days from 2026-01-09); ASSUMPTIONS-proposed.md has a P-row for it; GLOSSARY has 'Delay in treatment'.\"},\n  {\"severity\": \"major\",\n   \"title\": \"MIST/vehicle damage, attorney-driven care, and passive/over-long treatment are missing from the attack map even though the cited source lists them\",\n   \"evidence\": \"Src 1 verbatim: '1) Police report – ... Was the injured party transported to a medical facility?'; '2) Vehicle photographs – Does the damage match? ... What is the directional force of impact?'; '6) Provider type – Was the claimant seen by a chiropractor or medical doctor?'; '7) ... Was it active or passive? Was it longer than an anticipated expected recovery date...'. adjuster-attacks.md:89 summarizes src 1 as including 'duration vs typical recovery, ... mechanism of injury', but no A-row covers them. Attorney referral/LOP appears only in texas-pi-notes.md §3 and lexicon.yaml:547 (litigation_referral), not as an attack. Coverage grep for 'property damage|MIST|minor impact|attorney|passive' -> no output.\",\n   \"why_it_matters\": \"These are value drivers I use on every soft-tissue claim: low impact or no visible damage, ambulatory at scene or refused transport, care that starts or escalates after an attorney is retained, months of passive modalities beyond the expected recovery, and chiropractor-only care. Rivera record 1 has 'rear-ended at approx. 35 mph' and 'Transported to Central ER', both mechanism and transport facts. Because the map is the stated basis for T-009 and the adjuster persona, those layers inherit the gap. My T-009 probes confirm the lexicon misses 'Minimal damage to vehicle; airbags did not deploy', 'Ambulatory at scene, refused transport', and 'Referred to this clinic by attorney'.\",\n   \"fix\": \"Add rows for: A13 mechanism/MIST (vehicle damage, speed, airbags, ambulatory or transported at scene; Rivera records 1-2), A14 attorney involvement timing / LOP-funded care (texas-pi-notes §3; flag only if the record says it), A15 duration and type of care vs expected recovery (active vs passive, provider type; src 1, src 3 Colossus duration). For each, state the flag type, or 'context only, not a required flag', and whether code or lexicon owns it.\",\n   \"acceptance_test\": \"adjuster-attacks.md attack map has rows covering mechanism/MIST, attorney/LOP timing, and duration/passive care, each citing src 1 (and src 3 or TX §3 where relevant) and naming the Rivera record or 'not in records'; T-009 re-run of artifacts/review-evidence/T-009-adjuster-probes.py MIST/transport/attorney probes reflects the new rows.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Brinjikji (lumbar-only review) used to argue about a cervical C5-C6 finding\",\n   \"evidence\": \"adjuster-attacks.md:48-50: 'disc bulge prevalence rose from ~30% at age 20 to ~84% at 80 ... The defense uses this to say a C5-C6 protrusion in a 41-year-old may be pre-existing'. Brinjikji full text (PMC4464797) verbatim: 'additional studies that reported lumbar spine CT or MR imaging findings in individuals without low back pain.' Figures themselves confirmed against the PubMed abstract.\",\n   \"why_it_matters\": \"If the firm repeats this in a demand or a rebuttal, defense counsel will point out that the study is about the low back, not the neck. The direction of the point (degeneration is common in people without symptoms) probably holds for the cervical spine too, but this is the wrong citation for it.\",\n   \"fix\": \"Say explicitly that Brinjikji covers the lumbar spine, and add a cervical asymptomatic-MRI source if the research wants to make the C5-C6 point. Otherwise, limit the claim to 'spinal (lumbar) degeneration is common in asymptomatic adults'.\",\n   \"acceptance_test\": \"adjuster-attacks.md A4 text and src 6 line both say 'lumbar'; any cervical prevalence claim cites a cervical study with URL.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Unlisted source cited: 'Australian PIC'\",\n   \"evidence\": \"adjuster-attacks.md:62-63: 'contemporaneous records outweigh an expert relying on an incorrect history (src 17, Australian PIC)'. Src 17 (line 105) is a Georgia Court of Appeals decision; no Australian Personal Injury Commission source appears in the 18-item list.\",\n   \"why_it_matters\": \"A claim with no URL can't be checked, and it is also foreign law. lexicon.yaml:538 (inconsistent_history rationale: 'contemporaneous records outweigh later accounts') rests on it.\",\n   \"fix\": \"Either add the PIC source with a URL and a 'non-US' label, or remove the clause and keep only what src 17 supports (impeachment with the claimant's intake forms).\",\n   \"acceptance_test\": \"Every parenthetical source reference in adjuster-attacks.md resolves to a numbered entry with a URL.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"GLOSSARY lacks core adjuster vocabulary\",\n   \"evidence\": \"memory/GLOSSARY.md (38 terms) has no entry for MIST / minor impact soft tissue, delay in treatment, specials vs generals, soft-tissue injury, value drivers, Stowers demand, or BI. personas/claims-adjuster.md §6 lists these as the adjuster's vocabulary.\",\n   \"why_it_matters\": \"Workers and reviewers who write flag rationales and persona checks use the GLOSSARY. If these terms are missing, the adversary's actual arguments never make it into the vocabulary those people work from.\",\n   \"fix\": \"Add one-line entries for MIST, delay in treatment, specials vs generals, value drivers (Colossus), Stowers demand (texas-pi-notes §7 already names it), and BI, each with a source or 'assumption'.\",\n   \"acceptance_test\": \"grep -c -E 'MIST|Delay in treatment|Generals|Value drivers|Stowers' memory/GLOSSARY.md >= 5.\"},\n  {\"severity\": \"nit\",\n   \"title\": \"Attack map drops 'approx.' from the ROM finding\",\n   \"evidence\": \"adjuster-attacks.md:26: 'objective: ROM −40% (rec 4)'. Record 4 verbatim: 'Cervical range of motion reduced approx. 40%.'\",\n   \"why_it_matters\": \"This is the same kind of hedge-stripping the research tells the product never to do (chronology-practice.md R3). Research tables get copied into prompts and golden files.\",\n   \"fix\": \"Quote as 'reduced approx. 40%'.\",\n   \"acceptance_test\": \"grep -n 'approx. 40%' research/adjuster-attacks.md matches the A9 row.\"}\n ],\n \"whats_right\": [\n  \"Attack map ties each attack to the exact Rivera excerpt, and the day counts (73, 129) are right; keep this record-anchored format.\",\n  \"Read-depth and source-side labels (insurer, plaintiff, vendor, primary) are honest; the Herrera and Virginia takeaways check out against the sources.\",\n  \"Billed-not-damages (Haygood / §41.0105) and '§18.001 is not causation evidence' are correctly turned into product rules.\"\n ],\n \"questions_for_chris\": [\n  \"Should delay-to-first-treatment be a visible computed field in the timeline (outside the four required flags), or research context only? The adjuster persona checklist item 2 assumes it is shown.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T00:37:35.725Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-008-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:38:48.567Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/reviews/T-009-claims-adjuster.md",
 "content": "# T-009 review — claims-adjuster-reviewer\n\n**Verdict: changes** (0 blockers, 5 majors, 3 minors).\n\nThe deterministic check passes. `.venv/bin/python research/lexicon_selfcheck.py` reports 48 entries (pre_existing=17,\ncausation_weakening=21, compliance=10), every Appendix C phrase fires on its sample record, and the result is `RESULT: PASS`.\nThe ACs are met as written. The trouble starts off the sample. I ran 63 adversarial sentences through the YAML using the selfcheck's\nown negation guard (imported, not modified). Results: **OK=10, FN=38, FP=15**. On pre-existing phrasing an adjuster would actually\nexploit, the lexicon raised a high- or medium-strength hit on 3 of 28 probes. That includes all three subtle records of the\ncommitted golden case `case_06_subtle_pre_existing`, one of which (P1) is a `must` flag. The negation guard has no clause boundary\nat a comma. So \"No acute fracture, chronic degenerative changes at C5-6\", a standard radiology impression, has its `degenerative`\nand `chronic` hits suppressed. Intake-form checkboxes (\"Prior injuries: No.\") and clinical negatives (\"Did not present with loss\nof consciousness.\") raise high-strength flags that the FP notes don't cover. The lexicon's flag types also don't match the type\nnames in the golden set and REQUIREMENTS (no `hedge` category for R-TL-8, no mapping for `compliance`). A second signal is only\nuseful if it catches what the model misses. On this evidence it mostly catches what the model already sees.\n\nExercised: `python3 tools/board.py show T-009`. Ran `.venv/bin/python research/lexicon_selfcheck.py` → `RESULT: PASS`. Ran\n`.venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py` (my script: loads app/llm/lexicon.yaml read-only, applies\nevery pattern with re.I and the reference guard `negated()` from research/lexicon_selfcheck.py). Full output is in\n`artifacts/review-evidence/T-009-adjuster-probes.txt`. I read lexicon.yaml in full, lexicon_selfcheck.py, the\ncase_06_subtle_pre_existing .txt and .expected.json, sample.expected.json flags, REQUIREMENTS R-TL-8/R-FL-3/R-FL-4/§8 eval bar,\ndocs/LLM_VS_CODE.md row 12, and CONTRACT §5.2. I checked the lexicon's src-16 paraphrase against the source with curl (see\nT-008 evidence file). `git log`: lexicon f419c3b (18:28:02) came after the golden set 47520a8 (18:25:39) and before REQUIREMENTS\nround 2 64f766e (18:29:00).\n\n```json\n{\"card\": \"T-009\", \"persona\": \"claims-adjuster-reviewer\", \"model\": \"claude-opus-5-5\",\n \"scope\": \"app/llm/lexicon.yaml + research/lexicon_selfcheck.py (commit f419c3b, read at HEAD 9e759a2); sample case + evals/golden/case_06_subtle_pre_existing; no app\",\n \"exercised\": [\n  \"python3 tools/board.py show T-009 (3 ACs marked done)\",\n  \".venv/bin/python research/lexicon_selfcheck.py -> 'entries: 48 by type: pre_existing=17, causation_weakening=21, compliance=10' ... 'RESULT: PASS'\",\n  \".venv/bin/python artifacts/review-evidence/T-009-adjuster-probes.py > artifacts/review-evidence/T-009-adjuster-probes.txt -> 'TOTAL 63 OK=10 FN=38 FP=15'\",\n  \"Probe set includes the 3 subtle records of evals/golden/case_06_subtle_pre_existing.txt verbatim\",\n  \"Read app/llm/lexicon.yaml (699 lines), research/lexicon_selfcheck.py, evals/golden/case_06_subtle_pre_existing.expected.json, evals/golden/sample.expected.json flags\",\n  \"Read spec/REQUIREMENTS.md R-TL-8, R-FL-3, R-FL-4, eval bar row 3; docs/LLM_VS_CODE.md row 12; CONTRACT §5.2\",\n  \"git log --format='%h %ad %s' -8 (ordering of golden set, lexicon, requirements round 2)\",\n  \"curl valawyersweekly src 16 to check lexicon delayed_onset rationale\"\n ],\n \"verdict\": \"changes\",\n \"scores\": {\"appendix_c_coverage\": 5, \"recall_on_adjuster_phrasing\": 1, \"precision_fp_control\": 2, \"negation_correctness\": 2, \"rationale_and_sourcing\": 4, \"contract_fit\": 2},\n \"findings\": [\n  {\"severity\": \"major\",\n   \"title\": \"Pre-existing recall is very low off the sample: 3 of 28 adjuster probes raise a flag, including 0 of 3 case_06 golden records\",\n   \"evidence\": \"artifacts/review-evidence/T-009-adjuster-probes.txt, verbatim FN lines: '[FN] ... Symptoms predate the accident.'; '[FN] ... Prior to the accident she had intermittent neck pain.'; '[FN] ... Previously treated for neck pain by a chiropractor.'; '[FN] ... Patient was in a car accident in 2019.'; '[FN] ... Hx neck pain.'; '[FN] ... s/p ACDF 2015.'; '[FN] ... Has prior neck pain.'; '[FN] ... Previous cervical MRI in 2021.'; '[FN] ... Filed a workers' compensation claim for his back in 2020.'; '[FN] ... Neck pain persists. Has been seeing a chiropractor off and on since a lifting injury several years ago.' (case_06 P1, level 'must'); '[FN] ... History: occasional stiffness in the mornings at baseline...' (case_06 P2); '[FN(low-only)] ... Patient notes the old shoulder problem is acting up again.' (case_06 P3). Causes: prior_injury_or_event (lexicon.yaml:104) noun list lacks pain/problems/symptoms/MRI/imaging/treated; dated_prior_event (lexicon.yaml:239) requires the year BEFORE the event noun; no entries for predate, Hx, s/p, previously, baseline, 'acting up again', workers' comp, 'since ... years ago'. case_06 was committed at 47520a8 before the lexicon (f419c3b).\",\n   \"why_it_matters\": \"docs/LLM_VS_CODE.md row 12 justifies the lexicon as follows: 'a phrase list catches what a model overlooks.' The phrasings above are the ones I find in prior chiropractic and PCP records and use to discount a claim. If the LLM misses one, the lexicon misses it too, and the paralegal sends a demand with a prior condition I will find. On case_06, every catch will be LLM_ONLY → needs_review (R-FL-3), so the second signal adds nothing on the one golden case built to test it.\",\n   \"fix\": \"Add or extend entries: predate/pre-date/antedate; 'prior to the (accident|collision|MVA) ... (had|with|pain|symptoms|treated)'; previously/formerly treated|seen; Hx and s/p abbreviations; 'at baseline'/'baseline (pain|stiffness|symptoms)'; '(acting up|flared) again'; 'since a ... (injury|accident|fall) ... ago'; '(car|auto|motor vehicle) accident in (19|20)\\\\d\\\\d' (year after noun); workers' comp(ensation) claim; prior/previous + (pain|problems|symptoms|complaints|MRI|imaging|x-rays|treatment). Add the case_06 records and these probes as examples.hit vectors.\",\n   \"acceptance_test\": \"Re-run artifacts/review-evidence/T-009-adjuster-probes.py: every pre_existing FLAG probe raises a high/medium hit except those explicitly documented as LLM-only in the entry's false_positive note; the 3 case_06 records each raise a pre_existing hit; selfcheck still PASS with no new appendix_c mismatches.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Negation guard has no comma/clause boundary and treats uncertainty or 'never resolved' as negation, so it suppresses the strongest defense findings\",\n   \"evidence\": \"Probe output verbatim: '[FN(low-only)] ... No acute fracture, chronic degenerative changes at C5-6.' → 'negated:chronic[medium]:'chronic', degenerative[high]:'degenerative''; '[FN] ... Negative for fracture with moderate degenerative disc disease.' → 'negated:degenerative[high]'; '[FN] ... Without acute findings, with mild multilevel spondylosis.' → 'negated:degenerative_imaging_terms[high]'; '[FN] ... Denies headache, reports chronic neck pain since 2018.' → 'negated:chronic[medium]'; '[FN] ... Neck pain never fully resolved after the 2019 accident.' → 'negated:dated_prior_event[medium]:'2019 accident''; '[FN] ... Patient has not had neck pain since the 2019 MVA.' → negated; '[FN] ... Patient is not sure whether she had a prior neck injury.' → negated. Cause: lexicon.yaml:29 terminators omit ',' and 'with'/'reports'; research/lexicon_selfcheck.py:31 TOKEN = r\\\"[\\\\w'/-]+|;\\\" drops commas entirely; the 6-token window crosses into the next clause.\",\n   \"why_it_matters\": \"'No acute X, [chronic/degenerative Y]' is how radiology impressions are written. These are the degenerative findings I lead with, and the binding semantics (lexicon.yaml:6-16) tell the backend to suppress them, leaving only an audit log line. 'Never fully resolved after the 2019 accident' is an admission of a prior accident with ongoing symptoms, and the guard treats it as a denial.\",\n   \"fix\": \"Make ',' plus scope-breaking words ('with', 'reports', 'admits', 'endorses', 'but') terminators. Scope 'never'/'not' cues to the following clause only. Add 'not sure', 'unsure', 'unclear whether', 'never fully resolved', 'has not had ... since' as pseudo-negations. Have the binding semantics require that a suppressed high-strength hit still surface as needs_review when the LLM is silent, rather than being dropped.\",\n   \"acceptance_test\": \"The 7 probes above raise their high/medium hit; examples.negated vectors still pass; new examples.hit vectors 'No acute fracture, chronic degenerative changes at C5-6.' and 'Neck pain never fully resolved after the 2019 accident.' added and passing in selfcheck.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Undocumented high-strength false positives on intake forms, long ROS lists, and clinical negatives\",\n   \"evidence\": \"Probe output verbatim: '[FP] QUIET negation | Prior injuries: No.' → 'prior_injury_or_event[high/pre_existing]'; '[FP] ... Previous accidents: none.' → 'prior_injury_or_event[high/pre_existing]'; '[FP] ... ROS: Denies fever, chills, weight loss, chest pain, shortness of breath, or prior neck injury.' → 'prior_injury_or_event[high/pre_existing]' (cue outside 6-token window); '[FP] ... Did not present with loss of consciousness.' → 'no_show_cancel[high/compliance]:'Did not present''; '[FP] ... Comparison: No prior studies.' → 'comparison_prior_imaging[medium/pre_existing]:'Comparison: N''; '[FP] ... No change from prior visit; continue PT.' → comparison_prior_imaging[medium]. None of these is covered by the entries' false_positive notes (lexicon.yaml:110, 266-277, 583); post_cues (lexicon.yaml:28) lack 'no', 'none', 'n'.\",\n   \"why_it_matters\": \"Every intake packet has 'Prior injuries: Y/N' checkboxes, and every ER note has an ROS denial list. A tool that raises a high-strength pre-existing flag on 'Prior injuries: No.' is wrong in a way the paralegal learns to ignore, and then she ignores the real one too. It also puts the ≥0.9 per-type precision bar (REQUIREMENTS eval row 3) at risk. A compliance flag on 'did not present with LOC' would read as a no-show to anyone skimming the export.\",\n   \"fix\": \"Add post-colon negation: '<cue>: (no|none|denies|negative|n)' suppresses. Treat ROS-list denials as scoped to the list (cue to end of sentence when the sentence starts 'ROS'/'Denies'). Restrict no_show_cancel 'did not present' to 'did not present for (appointment|visit|session|therapy|follow-up)'. Exclude 'Comparison: no prior' and require an imaging noun after 'no change from prior'. Add each as an examples.miss or negated vector.\",\n   \"acceptance_test\": \"The 6 probes above produce no high/medium hit; corresponding vectors added to lexicon.yaml examples and selfcheck PASS.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Flag taxonomy doesn't match the golden set or REQUIREMENTS: no `hedge` category for R-TL-8, `compliance` unmapped, self-report mixed in with hedges\",\n   \"evidence\": \"lexicon.yaml:19 'flag_types: [pre_existing, causation_weakening, compliance]'. REQUIREMENTS.md:57 'Four types: gap, conflict, prior_condition, causation'. REQUIREMENTS.md:52 (R-TL-8): 'a sentence matching the `hedge` category of `app/llm/lexicon.yaml` ... Patient self-report phrases are not hedges'. evals/golden/sample.expected.json K2 (missed appointments) has \\\"type\\\": \\\"causation\\\", but lexicon.yaml:564 types missed_appointments as 'compliance'. patient_attributes_causation (:387) and patient_reports_generic (:399) share flag_type causation_weakening with may_represent (:283) and correlate_clinically (:296). No mapping table exists in the YAML.\",\n   \"why_it_matters\": \"The backend can't implement R-TL-8 from this file. If it treats causation_weakening as the hedge category, records 3, 5 and 9 ('Patient reports…/states…') wrongly trigger EXCERPT_OMITS_QUALIFIER. If `compliance` isn't mapped to `causation`, the missed-appointment hit never pairs with the LLM's causation flag, so golden K2 always ends up LEXICON_ONLY/LLM_ONLY needs_review. (REQUIREMENTS round 2 landed 58 s after this commit, so this is a reconciliation job, not negligence, but it has to be done before the M2 build.)\",\n   \"fix\": \"Add a per-entry `category` (hedge | self_report | prior | degenerative | compliance | recovery_context ...) and a top-level `maps_to` table from flag_type to spec type (pre_existing→prior_condition/pre_existing, causation_weakening→causation, compliance→causation). Mark may_represent, correlate_clinically, possibility_terms, cannot_exclude, nonspecific_indeterminate as category hedge; the patient_* entries as self_report.\",\n   \"acceptance_test\": \"yaml.safe_load(lexicon)['entries'] where category=='hedge' contains may_represent and correlate_clinically and no patient_* entry; every flag_type has a maps_to value in {prior_condition|pre_existing, causation}; selfcheck asserts both.\"},\n  {\"severity\": \"major\",\n   \"title\": \"Causation and credibility attacks I use are absent: objective-negative exams, out-of-proportion complaints, MIST scene facts, repeat accidents, attorney-referral variants\",\n   \"evidence\": \"Probe output verbatim, all '[FN]' with no hit: 'Subjective complaints out of proportion to exam findings.'; 'No objective findings.'; 'Neurological exam within normal limits. Full cervical ROM. No paraspinal spasm.'; 'Patient was rear-ended again in March.'; 'Minimal damage to vehicle; airbags did not deploy.'; 'Ambulatory at scene, refused transport.'; 'Patient drove himself to urgent care three days later.'; 'Referred to this clinic by attorney after initial PCP visit.' (litigation_referral, lexicon.yaml:548, needs 'referred by'); compliance: 'Patient declined ambulance transport.', 'Attended 4 of 12 scheduled visits.', 'Released to full duty without restrictions.' all FN.\",\n   \"why_it_matters\": \"EMS run reports and ER triage notes routinely carry 'ambulatory at scene', 'minimal vehicle damage', 'airbags not deployed', 'refused transport', and the cited Claims Journal checklist (AA src 1) names transport, vehicle damage, and treatment start. 'Out of proportion' and 'no objective findings' are what an IME report quotes. 'Rear-ended again' is the JLG Trucking second-accident fact the lexicon claims to cover (intervening_event, :452), but the pattern needs 'another/second/subsequent'. The paralegal never sees these.\",\n   \"fix\": \"Add entries: subjective_exceeds_objective ('out of proportion', 'no objective (findings|evidence)', 'subjective complaints (only|exceed)'); normal_exam ('within normal limits|WNL|full (ROM|range of motion)|no (paraspinal )?spasm|no tenderness', low/medium context like normal_imaging); mist_scene ('minimal|minor|no visible (vehicle )?damage', 'airbags? (did not|not) deploy', 'ambulatory at (the )?scene', 'refused|declined transport', 'self-transported|drove (himself|herself)'); 'again' after an accident verb for intervening_event; 'by (his|her|the)? attorney' anywhere after 'referred'; 'attended N of M'. Coordinate with the T-008 MIST/delay rows.\",\n   \"acceptance_test\": \"Re-run artifacts/review-evidence/T-009-adjuster-probes.py: the 11 probes listed raise at least a low hit, and the scene/out-of-proportion/repeat-accident ones raise medium or high.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"delayed_onset rationale overstates its source\",\n   \"evidence\": \"lexicon.yaml:443: 'Virginia record-review example: symptoms not reported until weeks later'. AA src 16 verbatim: 'did not report injury until eight days later when he was seen at an urgent care facility'.\",\n   \"why_it_matters\": \"A rationale that inflates its source is the same kind of overstatement the tool is meant to prevent. Eight days is a delayed-first-treatment fact, not 'weeks'.\",\n   \"fix\": \"Quote 'eight days later' and cite it under a delay-to-first-treatment entry as well.\",\n   \"acceptance_test\": \"grep -n 'eight days' app/llm/lexicon.yaml matches the delayed_onset rationale.\"},\n  {\"severity\": \"minor\",\n   \"title\": \"discharged_from_care is high-strength compliance even on a successful discharge\",\n   \"evidence\": \"Probe: '[FP] QUIET benign | Discharged from PT, goals met.' → 'discharged_from_care[high/compliance]:'Discharged from PT''. lexicon.yaml:596 acknowledges it ('the LLM decides').\",\n   \"why_it_matters\": \"'Goals met' is the plaintiff's best compliance fact. A high-strength compliance flag on it is noise the paralegal has to dismiss on every completed course of PT.\",\n   \"fix\": \"Add a post-window suppressor for 'goals met|completed|plan of care completed', or lower to medium unless a missed/no-show/non-compliance cue is in the same sentence.\",\n   \"acceptance_test\": \"'Discharged from PT, goals met.' raises no high-strength hit; 'Discharged from PT after two missed appointments.' still does (appendix_c [6]).\"},\n  {\"severity\": \"minor\",\n   \"title\": \"Selfcheck verifies only the hand-picked examples; nothing exercises the golden cases committed before the lexicon\",\n   \"evidence\": \"research/lexicon_selfcheck.py:19-29 hardcodes only the 9 Appendix A excerpts; evals/golden/case_06_subtle_pre_existing.txt (commit 47520a8, earlier than f419c3b) is not loaded, and its 3 must/should pre_existing records all miss (finding 1).\",\n   \"why_it_matters\": \"A self-check that only replays the author's own examples can't catch recall gaps. That is why an AC-level PASS coexists with 38 FNs.\",\n   \"fix\": \"Have the selfcheck (or a qa test) run the lexicon over every evals/golden/*.txt and compare to expected pre_existing/causation evidence excerpts, reporting lexicon recall per case.\",\n   \"acceptance_test\": \"Selfcheck output includes a per-golden-case lexicon recall line, and case_06 P1 is a hit.\"}\n ],\n \"whats_right\": [\n  \"All Appendix C phrases fire on exactly their sample records (selfcheck PASS, no appendix_c mismatches); don't regress this.\",\n  \"'Patient reports missing 3 days of work' does not hit missed_appointments, and 'May return to work' does not hit may_represent; good precision on the sample traps.\",\n  \"Every entry carries a rationale, source, false-positive note, strength, and test vectors; the low-strength tier for context-only hits (CT head negative) is the right call.\"\n ],\n \"questions_for_chris\": [\n  \"Should MIST/scene facts from EMS reports (speed, vehicle damage, ambulatory, transport) be surfaced as review flags at all, or only as context? They are adjuster attacks but are not one of the four required flag types.\"\n ]}\n```\n"
}
````

### User / tool · 2026-11-02T00:38:48.705Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/reviews/T-009-claims-adjuster.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:38:52.129Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; for f in reviews/T-008-claims-adjuster.md reviews/T-009-claims-adjuster.md; do .venv/bin/python -c \"\nimport json,re,sys\nt=open('$f').read(); b=re.findall(r'\\`\\`\\`json\\n(.*?)\\n\\`\\`\\`',t,re.S); assert len(b)==1\nd=json.loads(b[0]); sev=[x['severity'] for x in d['findings']]\nexp='fail' if 'blocker' in sev else 'changes' if 'major' in sev else 'pass'\nprint('$f', d['verdict'], exp, {s:sev.count(s) for s in set(sev)})\"; done; grep -n \"def.*valid\\|reviews/\" tools/board.py | head -5",
 "description": "Validate review JSON blocks and verdict rule"
}
````

### User / tool · 2026-11-02T00:38:52.179Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: could not parse command safely (No escaped character) | command: cd /Users/arsis/zlayt-pm-project; for f in reviews/T-008-claims-adjuster.md reviews/T-009-claims-adjuster.md; do .venv/bin/python -c "
import json,re,sys
t=open('$f').read(); b=re.findall(r'\`\`\`json
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:38:55.228Z

**tool call — Bash**
````
{
 "command": "cd /Users/arsis/zlayt-pm-project; .venv/bin/python - <<'EOF'\nimport json, re\nfor f in [\"reviews/T-008-claims-adjuster.md\", \"reviews/T-009-claims-adjuster.md\"]:\n    t = open(f).read()\n    fence = \"`\" * 3\n    b = re.findall(fence + r\"json\\n(.*?)\\n\" + fence, t, re.S)\n    assert len(b) == 1, f\n    d = json.loads(b[0])\n    sev = [x[\"severity\"] for x in d[\"findings\"]]\n    exp = \"fail\" if \"blocker\" in sev else \"changes\" if \"major\" in sev else \"pass\"\n    print(f, d[\"verdict\"], exp, {s: sev.count(s) for s in set(sev)})\nEOF",
 "description": "Validate review JSON blocks and verdict rule"
}
````

### User / tool · 2026-11-02T00:38:55.322Z

**tool result**
````
reviews/T-008-claims-adjuster.md changes changes {'minor': 3, 'major': 2, 'nit': 1}
reviews/T-009-claims-adjuster.md changes changes {'minor': 3, 'major': 5}
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:38:56.138Z

Now recording recurring patterns to memory.

### Assistant · claude-opus-5-5 · 2026-11-02T00:39:02.277Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md",
 "content": "---\nname: lexicon-review-method\ndescription: How to review flag lexicons/phrase lists as the adjuster — self-check PASS on author examples hides recall gaps; probe off-sample phrasing, comma-scoped negation, intake checkboxes\nmetadata:\n  type: feedback\n---\n\nA lexicon self-check that replays only the author's own examples + the 9 sample records will PASS while recall on real\nadjuster phrasing is near zero (T-009 round 0: selfcheck PASS, my 63 probes OK=10 FN=38 FP=15).\n\n**Why:** the second signal exists to catch what the LLM overlooks; testing it on the sample alone proves nothing.\n\n**How to apply:** for any lexicon/flag change, re-run artifacts/review-evidence/T-009-adjuster-probes.py (import the repo\nguard, never modify the repo; reviewer hook blocks writes outside reviews/ and artifacts/review-evidence/ — even scratchpad).\nAlways probe: (1) evals/golden/case_06_subtle_pre_existing records; (2) \"No acute fracture, chronic degenerative changes\"\n(comma-scope negation); (3) intake checkboxes \"Prior injuries: No.\"; (4) ROS denial lists >6 tokens; (5) \"did not present\nwith\"; (6) MIST/scene facts and \"out of proportion\". Also check flag_type names vs REQUIREMENTS/golden types (hedge category,\ncompliance→causation mapping). See [[research-attack-map-gaps]].\n"
}
````

### User / tool · 2026-11-02T00:39:02.369Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/feedback_lexicon_review_method.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:39:08.026Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md",
 "content": "---\nname: research-attack-map-gaps\ndescription: Recurring adjuster-attack omissions in Zlayt research (delay to first treatment, MIST, attorney timing, passive care) and source-check notes\nmetadata:\n  type: project\n---\n\nAs of 2026-11-01 (T-008 round 0), research/adjuster-attacks.md A1–A11 omitted delay-to-first-treatment, MIST/vehicle damage/\ntransport at scene, attorney-referral timing/LOP care, and duration/passive care/provider type — all listed verbatim in its own\nsrc 1 (Claims Journal 2013 checklist items 1, 2, 5, 6, 7).\n\n**Why:** researcher summarized src 1 but built rows only from the spec's four flags; downstream lexicon and personas inherit gaps.\n\n**How to apply:** on re-review, grep adjuster-attacks.md for these rows first. Source facts already verified by curl:\nBrinjikji AJNR 2015 is a LUMBAR review (don't accept it for cervical claims); Herrera v. Madrak (Conn. App. 2000) >12 missed PT\nsessions confirmed; Virginia Lawyers Weekly src 16 says \"eight days later\" (not \"weeks\"); studicata Fletcher v. Simmons is\npaywalled (403). WebFetch is not in this reviewer's toolset — use curl. Evidence: artifacts/review-evidence/T-008-adjuster-source-checks.txt.\nRelated: [[lexicon-review-method]].\n"
}
````

### User / tool · 2026-11-02T00:39:08.120Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/project_research_attack_map_gaps.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:39:09.793Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md",
 "content": "- [Lexicon review method](feedback_lexicon_review_method.md) — selfcheck PASS hides recall gaps; rerun probe script; must-probe constructions\n- [Research attack-map gaps](project_research_attack_map_gaps.md) — T-008 omissions (delay, MIST, attorney, passive care) + verified source facts\n"
}
````

### User / tool · 2026-11-02T00:39:09.890Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/claims-adjuster-reviewer/MEMORY.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T00:39:23.641Z

Both cards come back as **changes**: no blockers, 2 majors on T-008 and 5 on T-009. Both review files pass the verdict rule (any major → changes).

**T-008 (domain research):** all four ACs are met (sources 10/18/11, glossary 38 terms, 13 assumptions). I checked four sources with curl because WebFetch isn't available to me. Claims Journal, Brinjikji, Herrera v. Madrak and the Virginia Lawyers Weekly piece all support their takeaways. Fletcher v. Simmons is behind a paywall (HTTP 403), so I couldn't check it.
- **Major 1:** the attack map has no "delay to first treatment" row. Its own source 1 asks "How soon did treatment start?", and source 16 has the claimant reporting injury "eight days later". For Rivera the delay is zero days, which helps the claimant, and nothing surfaces it.
- **Major 2:** low-impact / vehicle-damage attacks, transport at the scene, attorney-referral timing and letter-of-protection care, and passive or over-long treatment are all missing. Source 1 lists every one of them. A grep of the file for these terms returns nothing.
- **Minors:** Brinjikji is a lumbar-spine review but is used for the C5-C6 neck finding; one claim cites an "Australian PIC" source that isn't in the source list; the glossary has no entries for minor-impact soft tissue, specials vs. generals, Stowers or similar adjuster terms. Nit: "approx." is dropped from the 40% range-of-motion figure.

**T-009 (lexicon):** the selfcheck reports `RESULT: PASS` with 48 entries, and every Appendix C phrase fires on its sample record. My 63 adversarial sentences, run through the YAML with the repo's own negation guard (repo unchanged), gave **OK=10, FN=38, FP=15**.
- **Major 1, pre-existing recall:** 3 of 28 pre-existing probes raised a flag. The golden case `case_06_subtle_pre_existing` scores 0 of 3, including its must-flag "since a lifting injury several years ago". Also missed: "predate", "Hx", "s/p", "previously treated", "car accident in 2019", "at baseline".
- **Major 2, negation:** the guard doesn't stop at commas. "No acute fracture, chronic degenerative changes at C5-6" has its degenerative hit suppressed. "Never fully resolved after the 2019 accident" and "not sure whether she had a prior neck injury" are also treated as denials.
- **Major 3, false alarms the notes don't cover:** high-strength flags fire on "Prior injuries: No.", "Previous accidents: none.", long review-of-systems denial lists, "Did not present with loss of consciousness" (flagged as a no-show) and "Comparison: No prior studies."
- **Major 4, flag types don't match the spec:** the YAML has no `hedge` category, which REQUIREMENTS R-TL-8 needs. Self-report phrases share a type with hedges, and `compliance` doesn't map to the golden set's `causation` type (the missed-appointments flag K2). The requirements update landed 58 seconds after the lexicon commit, so this is a reconciliation job.
- **Major 5, causation and credibility gaps:** nothing catches "out of proportion", "no objective findings", a normal exam (WNL, full ROM), scene facts from EMS reports (minimal damage, ambulatory, refused transport), "rear-ended again", or "Referred to this clinic by attorney".
- **Minors:** the delayed-onset rationale says "weeks later" where the source says eight days; "Discharged from PT, goals met" raises a high-strength compliance flag; the selfcheck never runs the golden cases that were committed before the lexicon.

I left one question for Chris in each review: should delay to first treatment, and the scene facts from EMS reports, appear as flags or computed fields, or stay as research context only?

I saved two notes to my agent memory: how to probe lexicons, and the attack-map gaps with the source facts I verified.

Files are in /Users/arsis/zlayt-pm-project:
- reviews/T-008-claims-adjuster.md
- reviews/T-009-claims-adjuster.md
- artifacts/review-evidence/T-009-adjuster-probes.txt
- artifacts/review-evidence/T-009-adjuster-probes.py
- artifacts/review-evidence/T-008-adjuster-source-checks.txt
