# Subagent: Researcher: T-077 case patterns (Researcher: T-077 case patterns)

Source: `agent-ac1ebeb544ee39022.jsonl` (Claude Code transcript). Unedited except redactions and format changes listed in the README.

### User / tool · 2026-11-02T03:11:17.338Z

You own board card T-077 (claimed by "researcher") in /Users/arsis/zlayt-pm-project. Run `python3 tools/board.py show T-077` and read memory/ORCHESTRATOR_DECISIONS.md D-042 and research/case-library-sources.md, which is the v1 research behind the existing 7 library packets in evals/library.

Goal: research real-world personal-injury case patterns from public sources, so we can build more fictitious, fully synthetic case packets for multi-case work. Use web search. Good sources include appellate opinions that discuss treatment gaps, prior injuries, causation testimony, billing disputes, LOP/lien, paid-vs-incurred, Waddell or credibility testimony, and Spanish-speaking plaintiffs or interpreters, plus jury verdict summaries, state bar or CLE materials, and published research on PI record review. Texas focus is preferred but not required.

Write research/case-library-sources-v2.md with at least 12 patterns that don't duplicate v1. For each pattern give:
- the source URL and date;
- a 2–3 line summary;
- the record features it implies (gaps, priors, causation wording, billing shape, language, scanned or handwritten pages, mixed-side exam findings, rate-vs-charge traps);
- which D-042 feature it exercises;
- a synthetic-safety note: no real names, dates shifted, facts recombined.

Never copy real records or personal data. Commit with `git add <path>` then `git commit -m "..." -- <path>` as separate commands, with the trailer "Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>". Then `board.py ac`, the handoff, and `move T-077 in_review --agent researcher`. Reply in 3 lines.

### User / tool · 2026-11-02T03:11:17.342Z

<system-reminder>
Other agents active in this session, addressable via SendMessage({to: name, message}): main, architect, backend-1, backend-2, backend-3, backend-4, db, frontend-2, frontend-office, office-builder, qa, qa-2, researcher-a, researcher-b, researcher-c, writer.
</system-reminder>

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:19.713Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py show T-077; grep -n \"D-042\" -A 40 memory/ORCHESTRATOR_DECISIONS.md | head -80; wc -l research/case-library-sources.md; ls evals/library; ls /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/",
 "description": "Show card, D-042, and v1 research context"
}
````

### User / tool · 2026-11-02T03:11:19.868Z

**tool result**
````
---
id: "T-077"
title: "Research: real-world PI case patterns for the multi-case library (v2)"
milestone: "M3"
role: "researcher"
status: "in_progress"
priority: "P1"
depends_on: []
created_by: "orchestrator"
created_at: "2026-11-02T03:11:04Z"
updated_at: "2026-11-02T03:11:11Z"
claimed_by: "researcher"
claimed_at: "2026-11-02T03:11:11Z"
rounds: 0
commits: []
reviews: []
ac:
  - {"n": 1, "text": "research/case-library-sources-v2.md lists >= 12 case patterns from public real-world sources (court opinions, verdict reports, bar/CLE materials, published studies) with URL, date and the record features each implies (gaps, priors, causation language, billing shape, language)", "done": false, "evidence": null}
  - {"n": 2, "text": "Each pattern names which product feature it exercises (D-042 list) and is marked synthetic-safe (no real names, dates shifted)", "done": false, "evidence": null}
---
## Description
(see title and acceptance criteria)

## Notes (append-only, newest last)
- 2026-11-02T03:11:11Z researcher: claimed

## Handoff (filled when moving to in_review)

50:| D-042 | **Second scope reinstatement (Chris, chat, 2026-11-02).** Build every remaining cut that needs neither a paid third-party integration nor auth/multi-user. Reinstated: charge reclassification (guarded: a rate becomes a charge only with code-verified charge wording plus a judge re-check); billing analysis on synthetic itemized ledgers (billed, adjusted, paid, LOP/lien, all cited); Spanish-language records (excerpt always the original text; an LLM translation is labeled and judged); local OCR with Tesseract for scanned PDFs (page image beside OCR text; OCR-derived items always need review); PDF hidden-text detection; date-convention *suggestion* (pre-selects with a stated reason, still needs one confirm); dismissal-pattern learning for a single local profile (suggestions only, eval-guarded); calibrated confidence (shown as measured precision per state from evals, never an invented %); speaker attribution v2 (ships only at 100% on an adversarial eval set, else stays off per D-040). New: the LLM-as-judge process is visible in every case analysis; every check and gate renders as a **vertical stepper** with pass/fail/skipped, plain-words why, the evidence, and what the human must do next (HITL hand-off), following the <outside project> vendor-triage flow-rail pattern. Multi-case library grows from researched real-world case patterns and document formats. **Still cut:** accounts/auth/roles/sharing and anything per-user (needs an identity provider and multi-user), real PHI handling, third-party integrations (EHR, case management, email intake), and medical/legal judgment (outside the tool's role, not an effort cut). | Chris's instruction; each reinstated item keeps the ladder, grounding and D-034/D-040/D-041 rules. | Chris chat 2026-11-02 |
51-| D-043 | Credibility flags fail toward flagging (2026-11-02, after T-067 r3): any sentence containing a credibility term flags, **unless** the whole sentence is one clause matching a short allow-list of clean negations ('No Waddell signs.', 'Waddell signs negative.', '0/5 Waddell signs.', 'Effort consistent.', 'Good/full effort.', 'Not tested/not performed.'). Anything with a second clause, contrast word or side qualifier flags. An extra flag costs one paralegal click; a missed one costs credibility at the adjuster. | Three rounds of clause-scoped negation each regressed a different word order. | T-067 claims-adjuster r3 |
      39 research/case-library-sources.md
case_lib01_er_only_then_gap.expected.json
case_lib01_er_only_then_gap.txt
case_lib02_slip_fall_prior_knee.expected.json
case_lib02_slip_fall_prior_knee.txt
case_lib03_truck_rear_end_chiro.expected.json
case_lib03_truck_rear_end_chiro.txt
case_lib04_dog_bite_scar_revision.expected.json
case_lib04_dog_bite_scar_revision.txt
case_lib05_pedestrian_orif_hardware.expected.json
case_lib05_pedestrian_orif_hardware.txt
case_lib06_lop_billed_vs_adjusted.expected.json
case_lib06_lop_billed_vs_adjusted.txt
case_lib07_parking_lot_fall_outside_records.expected.json
case_lib07_parking_lot_fall_outside_records.txt
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:21.172Z

**tool call — Bash**
````
{
 "command": "cat research/case-library-sources.md; ls research; git log --oneline -3",
 "description": "Read v1 case library research"
}
````

### User / tool · 2026-11-02T03:11:21.281Z

**tool result**
````
# Case library sources (T-052)

Seven synthetic packets in `evals/library/` (`case_lib01_*` to `case_lib07_*`, golden/1 schema), each mirroring one real-world PI scenario.
Rebuild: `python3 research/library_build.py`. Validate: `python3 research/validate_library.py` (runs `evals/golden/check_golden.py` over golden + library,
then a denylist scan for real identifiers).

**Rules followed.** No real name, provider, place, date, amount or case facts were copied. Each packet takes a *pattern* (what the treatment record looks like
and what the other side attacks) and re-expresses it with invented people, providers, towns and numbers. The sources are mostly plaintiff-side blogs and one
news report, so what they say about adjusters is advocacy; I use them for scenario shape, not as legal authority. Where a source was not opened I say so.

| # | Source (URL) | Opened? | Takeaway (one line) | What the packet mirrors | Packet |
|---|---|---|---|---|---|
| S1 | https://www.rmdlaw.com/blog/the-gap-in-treatment-insurance-trap-how-a-delay-can-lower-your-claim-value/ | yes (fetched) | Claims software reads treatment dates without context and treats a gap as a stand-in for severity; an ER-only visit followed by a long pause is scored as a gap, and the reason helps only if the provider charted it. | ER visit, negative x-ray, first follow-up 44 days later; the reason for the delay appears only as the patient's own statement, attributed; new symptom after the gap. | `case_lib01_er_only_then_gap` |
| S2 | https://www.studicata.com/summaries/superior-court-appellate-division-of-new-jersey/nichols-v-duke-linden-llc-2023-ox7g9x (a 2023 New Jersey appellate summary) | **no** (HTTP 403; takeaway from the search-result summary only) | A plaintiff who says a fall aggravated an earlier knee or back condition needs a comparative medical analysis; the defense leans on prior-symptom entries in treating records. Corroborated by S5 (defense expert attributes a future replacement to prior knee surgeries). | Store slip-and-fall, same knee previously operated, imaging that names both acute and prior surgical change, hedged "aggravation ... possible" wording; the tool shows the language and apportions nothing. | `case_lib02_slip_fall_prior_knee` |
| S3 | https://oklahomalawyer.com/soft-tissue-cases-and-chiropractic-care/ | yes (fetched) | Soft-tissue injuries are often treated by chiropractors several times a week for months; adjusters raise "excessive treatment" late, argue "if you're not treating, you're not hurt", and discount subjective pain when imaging is negative. | Tractor-trailer rear-end, plan of 36 visits, "unchanged" pain note, discharge after 31 visits, 28-day near-miss interval, then an MRI with "likely chronic" and desiccation. | `case_lib03_truck_rear_end_chiro` |
| S4 | https://plasticsurgerypractice.com/treatment-solutions/innovations/research/revision-surgery-often-needed-for-facial-dog-bite-injuries-in-children/ | yes (fetched) | In a study of facial dog bites in children, most wounds were closed at first repair, more than three quarters later had scar revision, and about a quarter needed a second or third revision. | Adult facial dog bite: ED repair, plastic-surgery follow-ups with photographs, a planned 8-week return that code still flags as a gap, a revision estimate, a later revision with a surgeon fee. The source is about children; the adult record shape is my assumption. | `case_lib04_dog_bite_scar_revision` |
| S5 | https://valawyersweekly.com/2013/04/01/pedestrian-struck-in-old-town-alexandria-crosswalk-550000-verdict/ | yes (fetched) | A pedestrian with a displaced tibial plateau fracture had ORIF within days, a second surgery about seven months later to remove screws, lasting atrophy and pain, and a defense expert who tied any future knee replacement to prior knee conditions. | Pedestrian in a crosswalk, ORIF, PT, hardware removal about seven months later, hedged future knee replacement, a prior arthroscopy in the history; two flagged gaps. | `case_lib05_pedestrian_orif_hardware` |
| S6 | https://www.thompsoncoe.com/resources/publications/texas-supreme-court-limits-evidence-on-medical-expenses/ | yes (fetched) | The Texas rule limiting medical-expense damages to amounts paid or incurred makes billed-but-not-owed amounts a litigation issue; letters of protection are the contested workaround. | Attorney-referred clinic treating under a letter of protection; billing statement with a balance; imaging bill with charge, adjustment and amount due. Only stated charges are counted (D-019); the rest is unclear and goes to internal notes. The tool decides no legal question. | `case_lib06_lop_billed_vs_adjusted` |
| S7 | https://www.rissman.com/?p=2203 | yes (fetched) | In a slip-and-fall defense result the plaintiff did not obtain earlier records from another jurisdiction, the treating surgeon did not use reasonable-probability language on aggravation, and treatment under letters of protection was questioned. | Fall in an employer's parking lot (patient says not on duty), prior back surgery in another state, outside records requested and not received, MRI hedge, surgeon who declines a causation opinion; all intervals 28 days (no gap flags). | `case_lib07_parking_lot_fall_outside_records` |

## What each packet stresses (coverage map)

| Packet | Gap flags | Pre-existing | Causation / hedge | Amounts | Special |
|---|---|---|---|---|---|
| lib01 | 44 d | none (must_not) | new onset after gap (should) | charge, rate | patient-stated reason is attributed, never the tool's |
| lib02 | 49 d (partial PT records) | prior arthroscopy, degenerative wording | "may reflect both", "possible" | 2 charges, rate | no apportionment |
| lib03 | 35 d, 28-d near-miss | desiccation | "likely chronic" | 2 charges, rate | plan vs actual visits; never "excessive" |
| lib04 | 56 d (planned), 273 d | none | none | charge, estimate, charge | estimate not counted; no permanence |
| lib05 | 49 d, 119 d | prior arthroscopy | "may be needed" | 2 charges, rate | second surgery |
| lib06 | 35 d (statement inside), 56 d | tendinosis (tolerated) | attorney referral | 4 charges, 3 unclear | billed vs adjusted |
| lib07 | none (all 28 d) | degenerative, prior surgery, post-op | "cannot be excluded", no causation opinion | 2 charges | work-adjacent, missing records |

## Assumptions and limits

- Dates, amounts and clinical wording are invented to exercise the tool; none is taken from a source. Dates run into late 2026 and one packet to 2026-09; the golden README says future-dated records are intentional.
- Every `must` flag in a packet is a record-language flag the tool should show, not a finding of fact. `should` and `tolerated` follow the golden README levels.
- S2 was not opened; if it matters for the submission, open the opinion itself before quoting it.
- Search results also surfaced a Manitoba auto-insurance tribunal decision on chiropractic visit counts and Texas cases on letters of protection (e.g. discovery of provider rates); I did not open them and did not use them for any packet.
- Packet names (e.g. Marrowgate, Dr. Pennywhistle) are invented; any resemblance to a real person or provider is unintended.
ASSUMPTIONS-proposed.md
__pycache__
adjuster-attacks.md
case-library-sources.md
chronology-practice.md
lexicon_selfcheck.py
library_build.py
office-view-references.md
phi-and-ai-supervision.md
texas-pi-notes.md
ui-references.md
validate_library.py
753b4a0 docs: D-043 credibility flags fail toward flagging
259310c docs: D-042 second scope reinstatement, judge visibility, vertical steppers
f4ef2ea fix(backend): confirm_date clears DATE_AMBIGUOUS on the entry, logs chosen date; api.md bulk-accept wording (T-076 r2)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:35.830Z

**tool call — ToolSearch**
````
{
 "query": "select:WebSearch,WebFetch",
 "max_results": 2
}
````

### User / tool · 2026-11-02T03:11:35.833Z

**tool result**
````
[tool_reference]
[tool_reference]
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:36.668Z

**tool call — Bash**
````
{
 "command": "head -60 research/adjuster-attacks.md; grep -n \"http\" research/texas-pi-notes.md | head -30",
 "description": "Check existing research sources to avoid duplication"
}
````

### User / tool · 2026-11-02T03:11:36.770Z

**tool result**
````
# What adjusters and defense counsel attack in a treatment chronology

Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
Purpose: ground the four required flags (gap, conflict, prior/pre-existing, causation-weakening language), the
claims-adjuster reviewer persona, and `app/llm/lexicon.yaml`.

**Source balance.** Plaintiff-firm blogs dominate search results. We deliberately added insurer-side and
neutral sources: Claims Journal (adjuster trade press, src 1), Verisk/ISO (insurer data vendor, src 2), Texas
Supreme Court opinions (srcs 9–12), and peer-reviewed radiology literature (srcs 6–8). Colossus internals are
proprietary; claims about it are second-hand (src 3) and labeled as such.
**Read depth.** Sources 1 and 12 were fetched and read in full; the rest were assessed from search-engine
excerpts of the page (the takeaway lines quote only what the excerpt showed). Verify before quoting externally.

## Attack map, applied to the Jordan Rivera sample

Flag-type column uses the D-013 vocabulary (`gap`, `conflict`, `pre_existing`, `causation`, `record_warning`); the
lexicon's former `causation_weakening` and `compliance` both map to `causation`.

| # | Attack | What the defense argues | Evidence | Rivera records that trigger it | Flag type |
|---|---|---|---|---|---|
| A1 | **Gap in treatment** | Claimant recovered; later care is for something else (intervening cause) | 1, 3, 4, 5 | 6→7: 73 days (2026-03-06 → 2026-05-18) | gap (code) |
| A2 | **Missed appointments / early discharge** | Non-compliance; failure to mitigate; injury not serious | 13, 14 | Rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9") vs rec 4 "Plan of care: 12 visits" | causation + conflict |
| A3 | **Pre-existing / prior condition** | Symptoms predate crash; at most aggravation | 1, 2, 15 | Rec 3 "low back pain in 2023, resolved" (different body region — still must surface) | pre_existing |
| A4 | **Degenerative imaging findings** | Findings are age-related wear, not trauma | 6 (lumbar), 19 (cervical), 7, 16 | Rec 8 "may represent degenerative change" | pre_existing + causation |
| A5 | **Hedged / possibility language** | No opinion to "reasonable medical probability" | 8, 11 | Rec 8 "may represent", "correlate clinically" | causation |
| A6 | **Self-reported causation** | Patient's statement is not a physician's causation opinion | 9, 11 | Rec 9 "Patient states symptoms began after the January collision" | causation |
| A7 | **Inconsistent history / dates** | Claimant unreliable; maybe a different incident | 10, 17 | Rec 7 "Date of accident per intake form: 2026-01-19" vs rec 1 (EMS) and rec 2 (ER), whose header dates are 2026-01-09; neither excerpt states an accident date | conflict (code) |
| A8 | **New-onset / new body part late** | New symptoms after a gap = new cause | 1, 10 | Rec 7 "New onset pain radiating to right arm"; header date 2026-05-18, 73 days after rec 6 (2026-03-06), by code date arithmetic | causation |
| A9 | **Subjective vs objective** | Pain scores only; no objective findings | 1, 3, 18 | Subjective: rec 1 "C/O neck pain 7/10", rec 6 "Pain 3/10"; objective: rec 4 "Cervical range of motion reduced approx. 40%", rec 2 "CT head negative", rec 8 "C5-C6 disc protrusion with mild right foraminal narrowing" | (context; not a required flag) |
| A10 | **Billing vs treatment mismatch / reasonableness** | Upcoding; billed ≠ paid; charges unreasonable | 1, 9, 12 | Rec 4 "Charge per visit $185." is a rate; no record states a PT charge → cannot total | amounts (code) |
| A11 | **Prior claims history** | ISO ClaimSearch shows earlier injury claims | 2 | Not in records — out of scope for the tool | — |
| A12 | **Delay to first treatment** | Not really hurt: a hurt person seeks care at once | 1, 16 | Rec 1 EMS and rec 2 ER both dated 2026-01-09; first recorded treatment = 2026-01-09. Only rec 7 states an accident date ("Date of accident per intake form: 2026-01-19"); records 1–2 state none | context only — per D-017 the tool states "first recorded treatment: <earliest record date>" and never computes delay from an accident date |
| A13 | **Mechanism / MIST (minor impact, soft tissue)** | Low-speed impact, little vehicle damage, ambulatory at scene or refused transport → no injury | 1, 3, 18 | Rec 1 "rear-ended at approx. 35 mph", "Transported to Central ER" (both *help* the claimant). No vehicle-damage facts in the records | causation (lexicon: scene facts such as ambulatory at scene, refused transport, minimal damage — D-018) |
| A14 | **Attorney involvement / LOP-funded care** | Counsel steered the claimant to high-cost providers; charges inflated under a letter of protection; (assumption) care began or escalated after the attorney was retained | 20, TX §3 (K&L); retention timing = assumption | Not in records. Rec 7 is a "new patient" visit dated 2026-05-18 and itself states no referral source or attorney (record 3 says only "Refer to physical therapy"; the lexicon `litigation_referral` entry fires on no sample record) | causation (lexicon `litigation_referral` — only when the record says it, D-018) |
| A15 | **Duration and type of care vs expected recovery** | Passive modalities (heat, massage, e-stim), chiropractor-only care, or treatment beyond typical recovery time | 1, 3, 18 | Rec 4 "Plan of care: 12 visits"; rec 6 "Discharged from PT after two missed appointments" (source label "Capital PT, visit 9"); records 4–6 name no PT modality, so active vs passive is not stated; rec 7 "Hill Country Pain Management, new patient", no referral source stated; rec 9 "Recommend cervical epidural steroid injection" (recommended, not performed) | context only — not a required flag; duration is visible from the timeline itself |

## Notes per attack

**A1 Gaps.** The adjuster checklist in Claims Journal names "treatment timing and gaps" explicitly (src 1).
Colossus is reported to score duration and frequency per injury (src 3, second-hand). Plaintiff firms say even
short gaps are used (src 4, 5). Nothing authoritative sets 30 days; the 30-day threshold is the Zlayt spec's.
Practitioners advise *explaining* a gap rather than hiding it (src 5) → the tool flags, the lawyer explains.

**A2 Missed appointments.** Mitigation is an affirmative defense — the defendant bears the burden and must show
the failure increased damages (src 13). Courts split on outcomes: an instruction was justified where >12 PT
sessions were missed (Herrera v. Madrak, src 14) but not where the plaintiff had reasons (Fletcher v. Simmons,
same source). So "two missed appointments" is a *review* flag, not a conclusion. The 12-planned-vs-discharged-at-9
discrepancy is a conflict an adjuster will see immediately.

**A3 Prior conditions.** Verisk sells ISO ClaimSearch to let adjusters "identify preexisting or subsequent injury"
(src 2). Concealing priors is described as a credibility killer (src 15). Even a *resolved, different-region*
prior (2023 low back vs 2026 neck) must be surfaced; the paralegal decides relevance.
False-positive risk: "denies prior neck injury" is a *negative* — it must not be flagged as a prior condition.

**A4/A5 Degenerative findings and hedges.** Brinjikji et al. (AJNR 2015, 33 studies, 3,110 asymptomatic people)
reviewed **lumbar** imaging: disc bulge prevalence rose from ~30% at age 20 to ~84% at 80, protrusion from 29% to
43% (src 6). It says nothing directly about the neck. For the **cervical** spine, Nakashima et al. (Spine 2015,
1,211 asymptomatic volunteers aged 20–70) found disc bulging in 87.6% overall and in most subjects in their 20s.
Bulging increased with age; cord compression was uncommon (5.3%) and most often at C5-C6 (41% of compressions) (src 19). The
study measured bulging, not protrusion, in Japanese volunteers. The
105:1. Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011) — https://caselaw.findlaw.com/tx-supreme-court/1573065.html — §41.0105 limits recovery to amounts paid or incurred; unadjusted charges inadmissible; §18.001 is procedural. (Full text read.)
106:2. Jim Adler & Associates, "What are paid and incurred medical expenses?" (2017) — https://www.jimadler.com/blog/what-are-paid-and-incurred-medical-expenses/ — Texas plaintiff firm's explanation of §41.0105 in practice. (Secondary; via search snippet.)
107:3. Tex. Civ. Prac. & Rem. Code §18.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-18-001/ — Current text: sufficiency, itemized statement, 90/120-day deadlines, counteraffidavit limits, not evidence of causation. (Mirror of statute; cross-checked with src 4.)
108:4. In re Allstate Indemnity Co., 622 S.W.3d 870 (Tex. 2021) — https://www.txcourts.gov/media/1452189/200071.pdf — §18.001 is procedural; 2019 amendments (Acts 2019, 86th Leg., ch. 779) made affidavits non-evidence of causation and changed deadlines for suits after 2019-09-01. (Full text extracted and read.)
109:5. In re K & L Auto Crushers, LLC, 627 S.W.3d 239 (Tex. 2021) — https://law.justia.com/cases/texas/supreme-court/2021/19-1022.html — Negotiated insurer rates are relevant and discoverable on reasonableness of charges. (Primary; read via summaries.)
110:6. Claims Journal, "Texas Supreme Ct. Approves Discovery for Documents Related to Medical Charges" (2021) — https://amp.claimsjournal.com/news/southcentral/2021/06/02/304050.htm — Insurer-side press on K&L's practical effect. (Trade press; via search snippet.)
111:7. Tex. Prop. Code §55.004 (mirror) — https://texas.public.law/statutes/tex._prop._code_section_55.004 — Hospital lien lesser-of 100-day charges / 50% of recovery; EMS lien ≤$1,000 within 72 hours. (Mirror.)
112:8. Texas Rules of Evidence 902 — https://texasevidence.com/rule-902/ — 902(10) business-records affidavit admits records without live custodian; notice required; form for medical expenses. (Secondary reference.)
113:9. Senate Research Center bill analysis, SB 679 (83rd Leg.) — https://capitol.texas.gov/tlodocs/83R/analysis/pdf/SB00679F.pdf — Records served with a 902(10) affidavit need not be filed with the court beforehand. (Official legislative analysis; via search snippet.)
114:10. Tex. Civ. Prac. & Rem. Code §33.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-33-001/ — Claimant >50% responsible may not recover. (Mirror; via search snippet.)
115:11. Blass Law, "Texas 51 percent rule" — https://www.blasslaw.com/faqs/texas-51-percent-rule-comparative-fault/ — Practitioner explanation of modified comparative fault and the two-year limitations period. (Plaintiff firm.)
116:12. IRMI, "Stowers doctrine" (insurance glossary) — https://irmi.com/term/insurance-definitions/stowers-doctrine — Insurer liable for the excess when it unreasonably refuses a within-limits demand; Thompson Coe practice paper https://www.thompsoncoe.com/content/uploads/2019/02/Stowers.pdf covers the elements and *Garcia*. (Secondary; via search excerpts.)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:39.358Z

**tool call — WebSearch**
````
{
 "query": "JLG Trucking v. Garza Texas Supreme Court 2015 second accident alternative causation",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:40.062Z

**tool call — WebSearch**
````
{
 "query": "Guevara v. Ferrer Texas Supreme Court 2007 lay evidence causation medical expenses",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:40.765Z

**tool call — WebSearch**
````
{
 "query": "Texas court of appeals personal injury Spanish interpreter medical records history inconsistent plaintiff",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:41.311Z

**tool call — WebSearch**
````
{
 "query": "court opinion \"Waddell signs\" symptom magnification personal injury appeal credibility",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:11:45.648Z

**tool result**
````
Web search results for query: "JLG Trucking v. Garza Texas Supreme Court 2015 second accident alternative causation"

Links: [{"title":"www.txcourts.gov","url":"https://www.txcourts.gov/media/943999/130978.pdf"},{"title":"Opinion issued 01","url":"https://www.docketalarm.com/cases/Texas_State_Supreme_Court/13-0978/JLG_TRUCKING_LLC_v._LAUREN_R._GARZA/04-24-15-Opinion_issued-01/Opinion_issued-01/"},{"title":"Get started","url":"https://www.studicata.com/summaries/supreme-court-of-texas/jlg-trucking-llc-v-garza-2015-5hx1fq"},{"title":"Get started","url":"https://www.studicata.com/summaries/supreme-court-of-texas/jlg-trucking-llc-v-garza-2015-5hxi05"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=11882"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/category/cases-from-bits/c203-volume-18-edition-5-cases/page/8"},{"title":"law.co","url":"https://law.co/app/cases/6856617"},{"title":"Supreme Court of Texas Update: JLG Trucking, LLC v. Garza","url":"https://texastechlawreview.org/supreme-court-of-texas-update-jlg-trucking-llc-v-garza"},{"title":"jlg trucking llc v lauren 2831492","url":"https://app.midpage.ai/case/jlg-trucking-llc-v-lauren-2831492"},{"title":"JLG Trucking, LLC v. Garza (Opinion)","url":"https://law.justia.com/cases/texas/supreme-court/2015/13-0978.html"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=11213"},{"title":"Justia Texas Supreme Court Opinion Summaries","url":"https://texassupremecourtopinions.justia.com/category/injury-law/page/5"},{"title":"Get started","url":"https://www.studicata.com/summaries/court-of-appeals-of-texas/jlg-trucking-llc-v-garza-2013-r767et"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/3082125/"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/3082121/"},{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/court/tx-court-of-appeals/1257543.html"},{"title":"Court of Civil Appeals of Texas, 2013","url":"https://hallapproved.com/tx/cases/appeals/2013/3114358/"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=9517"}]

The Texas Supreme Court reversed the exclusion of evidence about a second car accident and remanded for a new trial. The case is 466 S.W.3d 157 (Tex. 2015), decided April 24, 2015.

- **Background:** She sued JLG Trucking, claiming the first accident caused herniated discs in her neck that required eventual spinal fusion surgery. JLG sought to present evidence of the second accident as an alternative cause of her injuries, but the trial court excluded this evidence before trial on relevance grounds. The jury awarded her over $1.1 million. JLG also intended to introduce evidence of the October accident as an alternative cause of Garza's injuries, although JLG did not designate an expert to testify in support of that theory.
- **Holding:** The Court found the trial court abused its discretion. Evidence of the second accident had clear relevance to whether JLG's negligence caused the damages Garza claimed, particularly because she complained of neck pain immediately after the second accident. The Court also said expert testimony that the second accident was an alternative cause to Garza's injuries should not have been excluded.
- **Reasoning on burden:** One summary says the lower court's reasoning improperly shifted the burden of proof onto JLG, when in reality, it was Garza's burden to establish that the first accident caused her injuries.
- **Cross-examination:** The excluded evidence also compromised JLG's ability to cross-examine and probe Dr. Pechero's conclusions about the causation of Garza's injuries.
- **Lower court:** The Fourth Court of Appeals had affirmed. Its reasoning was that without competent expert evidence, the jury could not appropriately consider the second accident's potential impact on Garza's injuries.

The sources agree on the result but describe the court's reasoning somewhat differently. The Justia summary says the case was remanded for a new trial. The opinion's treatment of the expert-testimony question is the key point for your research, so I'd read the full opinion at txcourts.gov or Justia before relying on any summary.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:11:46.403Z

**tool result**
````
Web search results for query: "Guevara v. Ferrer Texas Supreme Court 2007 lay evidence causation medical expenses"

Links: [{"title":"Get started","url":"https://www.studicata.com/summaries/supreme-court-of-texas/guevara-v-ferrer-2007-5i4g4v"},{"title":"Expert Medical Evidence Mandated for Causation in High-Cost Automobile Accident Claims: Guevara v. Ferrer","url":"https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view"},{"title":"caselaw.findlaw.com","url":"https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=11213"},{"title":"texasworker.com","url":"https://texasworker.com/?p=17539"},{"title":"texasworker.com","url":"https://texasworker.com/?p=14805"},{"title":"Get started","url":"https://www.studicata.com/summaries/court-of-appeals-of-texas/ferrer-v-guevara-2005-qzdhgn"},{"title":"Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007). · Go Syfert","url":"https://syfert.com/texas/cases/247-s-w-3d-662/guevara-v-ferrer"},{"title":"tcjl.com","url":"https://tcjl.com/?p=218277"},{"title":"amigos meat distributors l p 4168048","url":"https://app.midpage.ai/case/amigos-meat-distributors-l-p-4168048"},{"title":"Eugene M. Sanchez v. David Leija & Lindale Wrecker Serv. (Tex. App. 2020). · Go Syfert","url":"https://syfert.com/caselaw/case.php?id=4841172"},{"title":"Court of Civil Appeals of Texas, 2012","url":"https://hallapproved.com/tx/cases/appeals/2012/3096395/"},{"title":"Teodoro Perez v. Dina Renee Johnson Appeal from 96th District Court of Tarrant County (memorandum opinion)","url":"https://law.justia.com/cases/texas/second-court-of-appeals/2020/02-19-00082-cv.html"},{"title":"texasworker.com","url":"https://texasworker.com/?p=59690"},{"title":"lauren lutkus v lorena garcia 11090078","url":"https://app.midpage.ai/case/lauren-lutkus-v-lorena-garcia-11090078"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9492611/"},{"title":"Court of Civil Appeals of Texas, 2012","url":"https://hallapproved.com/tx/cases/appeals/2012/2988963/"},{"title":"Texas Supreme Court, 2007","url":"https://hallapproved.com/tx/cases/supreme/2007/2833980/"},{"title":"Court of Civil Appeals of Texas, 2025","url":"https://hallapproved.com/tx/cases/appeals/2025/10664267/"}]

The search turned up consistent accounts of Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), though most results are secondary summaries rather than the opinion itself.

- **Facts and outcome:** The case arose from an October 2002 car accident involving an 86-year-old passenger, Arturo Labao. The Texas Supreme Court reversed the court of appeals, which had found the lay testimony sufficient to prove causation. Because only lay evidence was offered to prove that the accident caused all the medical expenses and expert evidence was required to prove many of them, we reverse and remand. The court of appeals' decision is Ferrer v. Guevara, 192 S.W.3d 39 (Tex. App.—El Paso 2005).
- **Rule:** The court restated that "expert testimony is necessary to establish causation as to medical conditions outside the common knowledge and experience of jurors." Lay testimony can suffice only where the causal link falls within common knowledge. One commentary notes the decision required expert evidence for high-cost claims exceeding $1 million. The Supreme Court of Texas addressed whether expert medical evidence is required to establish causation in cases where medical expenses are substantial.
- **Plaintiff's burden:** A claimant must show "what all the conditions were that generated the expenses and 'that all the conditions were caused by the accident.'" (quoting Guevara, 247 S.W.3d at 669).
- **Later use:** Courts cite Guevara for the general requirement of competent evidence on causation, and it is frequently invoked in medical-expense sufficiency challenges. Later decisions also note that Texas courts have held that lay testimony is sufficient to create a genuine fact issue on causation in certain instances.

For the exact holding and pin cites, read the full opinion (e.g., the texasworker.com or Findlaw copies), since the summaries above are secondary.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:11:48.137Z

**tool result**
````
Web search results for query: "court opinion "Waddell signs" symptom magnification personal injury appeal credibility"

Links: [{"title":"a4137 14","url":"https://www.njcourts.gov/system/files/court-opinions/2017/a4137-14.pdf"},{"title":"a 2 3 17","url":"https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf"},{"title":"Please ensure Javascript is enabled for purposes of website accessibility","url":"https://sclawyersweekly.com/?p=12766"},{"title":"Florida District Courts of Appeal, 2012","url":"https://hallapproved.com/fl/cases/appeals/2012/2550071/"},{"title":"The Use Of Waddell Tests In Workers Compensation Claims","url":"https://chiro.org/Graphics_Box_LINKS/FULL/Wadell_Tests.shtml"},{"title":"Supreme Court Appeal","url":"https://njcourts.gov/cases/23-17"},{"title":"Fishburne v. ATI Systems International","url":"https://hallapproved.com/sc/cases/appeals/2009/1292357/"},{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/court/la-supreme-court/2298518.html"},{"title":"cdn.ca9.uscourts.gov","url":"https://cdn.ca9.uscourts.gov/datastore/memoranda/2010/02/11/09-35136.pdf"},{"title":"The Use Of “Waddell” In Workers’ Compensation Claims","url":"https://corporate.findlaw.com/?p=37892"},{"title":"texasworker.com","url":"https://texasworker.com/?p=25174"},{"title":"NJ Supreme Court Rules Experts Can Testify About Symptom Magnification","url":"https://scarincilawyer.com/?p=3655"},{"title":"N.J. Supreme Court allows testimony on whether plaintiffs are faking injury symptoms","url":"https://whyy.org/articles/n-j-supreme-court-allows-testimony-on-whether-plaintiffs-are-faking-injury-symptoms"},{"title":"corporate.findlaw.com","url":"https://corporate.findlaw.com/legal-api/wp-json/wp/v2/corporate/37892"},{"title":"wadells signs","url":"https://bc-injury-law.com/tag/wadells-signs"},{"title":"cartercapner.com.au","url":"https://cartercapner.com.au/?p=3104"},{"title":"www.lexislegalnews.com","url":"https://www.lexislegalnews.com/mealeys/articles/1624501"},{"title":"Waddell's signs","url":"https://wikipedia.com/wiki/Waddell%27s_signs"}]

The search didn't turn up a single appellate opinion that matches all of your terms, but several related results are useful.

The closest match is the New Jersey *Rodriguez v. Wal-Mart* litigation. The Appellate Division ruled against admitting expert opinions on symptom magnification in civil jury trials. It found that such expert opinions about symptom magnification, malingering, or other equivalent concepts were improperly admitted in civil jury cases. The New Jersey Supreme Court later took a different view. It held that admissibility of expert testimony using terms like "somatization" and "symptom magnification" must be decided by trial courts case by case. The Supreme Court also noted that, unlike "somatization," "symptom magnification" is not defined in the medical literature. On the credibility concern, the court acknowledged that the term "malingering" raises heightened concerns since it may implicate credibility.

Waddell-specific material comes mainly from workers' compensation and medical-legal commentary, not from the appellate cases I found. One workers' compensation summary describes a holding in which three health-care providers noted either symptom magnification or Waddell signs, which the court relied on in a back-injury disability case. A medical reference notes that clinically significant Waddell scores are considered indicative only of symptom magnification or pain behavior, and have been misused in medical and medico-legal contexts. Commentary also observes that various court cases resulting in denial of Workers' Compensation benefits contained unchallenged expert testimony that a positive result on Waddell testing demonstrated "symptom magnification".

To find the specific opinion you have in mind, I'd suggest searching a case-law database with "Waddell" plus the jurisdiction and a term like "credibility." The results here may not reflect the exact case you're after.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:11:48.213Z

**tool result**
````
Web search results for query: "Texas court of appeals personal injury Spanish interpreter medical records history inconsistent plaintiff"

Links: [{"title":"Montoya v. State, 13-90-165-CR","url":"https://case-law.vlex.com/vid/montoya-v-state-no-892746390"},{"title":"texasworker.com","url":"https://texasworker.com/?p=38445"},{"title":"texasworker.com","url":"https://texasworker.com/?p=38127"},{"title":"texasworker.com","url":"https://texasworker.com/?p=19581"},{"title":"Camacho v. SAIF","url":"https://wlo.willamette.edu/orappeals/2014/06/camacho-v.-saif.html"},{"title":"texasworker.com","url":"https://texasworker.com/?p=30850"},{"title":"www.supremecourt.gov","url":"https://www.supremecourt.gov/DocketPDF/17/17-6327/34032/20180201131949973_00000001.pdf"},{"title":"cite.case.law","url":"https://cite.case.law/ill-app-2d/68/322/"},{"title":"Fla. court denies injured worker right to see Spanish-speaking psychologist","url":"https://www.businessinsurance.com/fla-court-denies-injured-worker-right-to-see-spanish-speaking-psychologist/"},{"title":"01 20 00443 cv","url":"https://law.justia.com/cases/texas/first-court-of-appeals/2021/01-20-00443-cv.html"},{"title":"Court of Civil Appeals of Texas, 2005","url":"https://hallapproved.com/tx/cases/appeals/2005/2922118/"},{"title":"01 18 00865 cv","url":"https://law.justia.com/cases/texas/first-court-of-appeals/2020/01-18-00865-cv.html"},{"title":"juan francisco hernandez vs citi staff","url":"https://compfox.io/caselaw/juan-francisco-hernandez-vs-citi-staff"},{"title":"abelardo zamora and janet zamora 4058613","url":"https://app.midpage.ai/case/abelardo-zamora-and-janet-zamora-4058613"},{"title":"A new, powerful Citizen Portal experience is ready. Switch now","url":"https://cpo.soar.com/articles/6146784/Texas/Witness-testifies-about-assault-911-call-and-photographs-entered-into-evidence"},{"title":"Court of Civil Appeals of Texas, 2009","url":"https://hallapproved.com/tx/cases/appeals/2009/2842648/"},{"title":"Court of Civil Appeals of Texas, 2025","url":"https://hallapproved.com/tx/cases/appeals/2025/10659616/"},{"title":"Court of Civil Appeals of Texas, 2014","url":"https://hallapproved.com/tx/cases/appeals/2014/3110501/"},{"title":"Court of Civil Appeals of Texas, 2019","url":"https://hallapproved.com/tx/cases/appeals/2019/4645468/"}]

I didn't find a Texas court of appeals personal injury opinion that squarely addresses a Spanish-speaking plaintiff whose medical history was inconsistent. The closest results are partial matches:

- **Chiv v. Figueroa (Tex. App.—Houston [1st Dist.], Aug. 2025):** This is the most relevant Texas civil appeal. It involves a personal injury dispute and a Spanish-language deposition whose translation was not certified, even though a certified interpreter was present at trial. Brandon Chiv v. Ranferi Monge Figueroa, Court of Civil Appeals of Texas, decided August 21, 2025. The excerpt doesn't show the holding on the translation issue, so you'd need the full opinion.
- **Hunter v. Hunter-related auto case (1st Dist., 2021):** The parties introduced more than 1,500 pages of Hunter's medical records into evidence, and the excerpt doesn't say anything about language or interpreters.
- **Zamora v. Davila (4th Dist., 2015):** This is a jury-credibility case. The court affirmed a low medical-expense award, holding that the jury could disbelieve testimony and records. Court applied Texas factual-sufficiency review, emphasized jury discretion to judge credibility and resolve conflicts, and affirmed the judgment. This is useful background for the standard of review if the inconsistency is framed as a credibility issue.
- **Mora v. Chacon (13th Dist., 2005):** The excerpt covers only the evidentiary issues list and the standard of review, which says decisions about the admissibility of evidence are left to the sound discretion of the trial court.

Results that don't fit your query: the Texas Workers' Compensation Appeals Panel decisions on texasworker.com involve interpreter translation errors, but they are administrative rulings, not court of appeals decisions. The Oregon case (Camacho v. SAIF) and the Illinois and Florida cases are out of state.

For a targeted search, try the Texas courts' opinion search or Westlaw/Lexis with terms like "interpreter" "credibility" "medical history" "personal injury" "Spanish" and "Tex. App."


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:51.176Z

**tool call — WebFetch**
````
{
 "url": "https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf",
 "prompt": "Give the case name, decision date, court, and a 4-sentence summary of facts and holding about symptom magnification / somatization expert testimony, and what medical record terms (e.g. Waddell, effort, inconsistent findings) were involved. Do not include any personal details beyond the case caption."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:52.625Z

**tool call — WebFetch**
````
{
 "url": "https://law.justia.com/cases/texas/supreme-court/2015/13-0978.html",
 "prompt": "Summarize facts relevant to medical records: timeline of first accident, ER visit, second accident, when neck complaints arose, imaging, surgery timing, and what the court said about alternative causation evidence and expert testimony. Give decision date. 6 sentences max."
}
````

### User / tool · 2026-11-02T03:11:52.943Z

**tool result**
````
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:53.476Z

**tool call — WebSearch**
````
{
 "query": "study copy and paste electronic health record notes duplicated text percentage JAMA cloned documentation",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:11:54.216Z

**tool call — WebSearch**
````
{
 "query": "Texas appellate opinion personal injury chiropractor causation testimony \"reasonable medical probability\" reversed soft tissue no expert",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:11:56.809Z

**tool result**
````
<outside-repo file omitted>
````

### User / tool · 2026-11-02T03:11:58.999Z

**tool result**
````
Web search results for query: "study copy and paste electronic health record notes duplicated text percentage JAMA cloned documentation"

Links: [{"title":"Half of words in clinical notes copied, pasted from prior visits","url":"https://www.ama-assn.org/practice-management/digital-health/half-words-clinical-notes-copied-pasted-prior-visits"},{"title":"Prevalence and Sources of Duplicate Information in the Electronic Medical Record","url":"https://pubmed.ncbi.nlm.nih.gov/36156143/"},{"title":"Half of words in clinical notes copied, pasted from prior visits","url":"https://www.ama-assn.org/practice-management/digital/half-words-clinical-notes-copied-pasted-prior-visits"},{"title":"AI study finds 50% of patient notes duplicated","url":"https://healthcareitnews.com/news/ai-study-finds-50-patient-notes-duplicated"},{"title":"htn.co.uk","url":"https://htn.co.uk/?p=42015"},{"title":"study explores prevalence and sources of duplicate content in electronic medical records","url":"https://htn.co.uk/2022/10/24/study-explores-prevalence-and-sources-of-duplicate-content-in-electronic-medical-records/"},{"title":"ai study finds 50 patient notes duplicated","url":"https://blue-harvest.healthcareitnews.com/news/ai-study-finds-50-patient-notes-duplicated"},{"title":"study ehrs full of copy and paste records","url":"https://healthmanagement.org/s/study-ehrs-full-of-copy-and-paste-records"},{"title":"Half of words in clinical notes copied, pasted from prior visits","url":"https://one-test.ama-assn.org/practice-management/digital-health/half-words-clinical-notes-copied-pasted-prior-visits"},{"title":"ai study finds 50 patient notes duplicated","url":"https://cloudgate.healthcareitnews.com/news/ai-study-finds-50-patient-notes-duplicated"}]

The most-cited study is the University of Pennsylvania analysis, published in JAMA Network Open in 2022. It found that 50.1% of the total text in the record was duplicated from prior text written about the same patient. Some news outlets describe it as a JAMA paper, but the journal is JAMA Network Open. The share of duplicated text rose over time, from 33% for notes written in 2015 to 54.2% for notes written in 2020. Of the duplicated text, 54.1% came from text written by the same author, whereas 45.9% was duplicated from a different author.

The authors also argued against a simple fix. They wrote that simple solutions such as banning copy-paste may have unintended consequences, such as worsening information scatter.

A separate study from UCSF in JAMA looked at inpatient progress notes. It found that 46 percent of notes were copied and 36 percent were imported. That work was smaller, covering 23,630 notes from 460 caregivers.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:02.921Z

**tool result**
````
Web search results for query: "Texas appellate opinion personal injury chiropractor causation testimony "reasonable medical probability" reversed soft tissue no expert"

Links: [{"title":"Jose Velasquez Sosa v. Montgomery County Appeal from 457th District Court of Montgomery County (memorandum opinion)","url":"https://law.justia.com/cases/texas/ninth-court-of-appeals/2023/09-22-00035-cv.html"},{"title":"Reversed and Rendered in part, Remanded in part and Affirmed in part Opinion Filed November 28, 2022","url":"https://law.counselstack.com/opinion/amanda-mcgee-v-ladonna-tatum-texapp-2022"},{"title":"2023 09 22 00035 cv","url":"https://cases.justia.com/texas/ninth-court-of-appeals/2023-09-22-00035-cv.pdf"},{"title":"14 22 00565 cv","url":"https://law.justia.com/cases/texas/fourteenth-court-of-appeals/2023/14-22-00565-cv.html"},{"title":"Court of Civil Appeals of Texas, 2022","url":"https://hallapproved.com/tx/cases/appeals/2022/9302204/"},{"title":"Court of Civil Appeals of Texas, 2012","url":"https://hallapproved.com/tx/cases/appeals/2012/3096395/"},{"title":"Opinion issued February 28, 2023","url":"https://law.counselstack.com/opinion/mary-lou-lara-v-jimmy-bui-texapp-2023"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9482641/"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9997961/"},{"title":"653 Insurance Newsbrief 20200211","url":"https://www.mdjwlaw.com/media/newsbrief/653_Insurance_Newsbrief_20200211.pdf"},{"title":"january 29 2021","url":"https://www.txcourts.gov/supreme/orders-opinions/2021/january/january-29-2021/"},{"title":"Court of Civil Appeals of Texas, 2020","url":"https://hallapproved.com/tx/cases/appeals/2020/4695721/"},{"title":"Court of Civil Appeals of Texas, 2022","url":"https://hallapproved.com/tx/cases/appeals/2022/6624242/"},{"title":"LACK OF EXPERT TESTIMONY RESULTS IN REVERSAL OF DAMAGES AWARD","url":"https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1"},{"title":"www.nmonesource.com","url":"https://www.nmonesource.com/nmos/nmsc/en/385817/1/document.do"},{"title":"04 16 00028 cv 0","url":"https://law.justia.com/cases/texas/fourth-court-of-appeals/2016/04-16-00028-cv-0.html"},{"title":"texasworker.com","url":"https://texasworker.com/?p=36607"},{"title":"Court of Civil Appeals of Texas, 2006","url":"https://hallapproved.com/tx/cases/appeals/2006/2849335/"},{"title":"Court of Civil Appeals of Texas, 2021","url":"https://hallapproved.com/tx/cases/appeals/2021/4856384/"}]

I ran one search and got excerpts from several Texas appellate opinions. I didn't see full holdings for most of them, so check each case before relying on it.

**Most relevant to soft-tissue causation without an expert**
- The Fourteenth Court of Appeals in the Donis Parties case (Ivory Hills) reversed a past-medical-expense award. The court held that soft-tissue injuries like cervical radiculitis and lumbar disc displacement were not matters of common knowledge, so expert testimony was needed to link them to the accident, and medical records alone did not supply that link. The Court held that, even considering the medical records, expert medical testimony was required to "establish a nexus between the accident and the Donis Parties' claimed injuries, and none was provided." The original 2020 memorandum opinion was withdrawn and replaced by a substitute opinion in February 2021, so cite the 2021 version (No. 14-18-00566-CV). See Motion Denied; Memorandum Opinion of January 14, 2020 Withdrawn; Reversed and Rendered in Part, Affirmed in Part, and Substitute Memorandum Opinion filed February 11, 2021.
- The Ninth Court's Sosa v. Montgomery County memorandum opinion (2023) involved a chiropractor-type soft-tissue claim. The court discussed whether treating physicians' records must read like expert testimony to establish causation. The trial court explained that to constitute evidence of causation, the statements of treating physicians found in medical records must read like expert witness testimony. The excerpt does not show the disposition.

**On the "reasonable medical probability" standard**
- The Fourteenth Court's 2023 opinion (No. 14-22-00565-CV) states the rule from *Burroughs Wellcome Co. v. Crye*: a medical expert's opinion must rest in reasonable medical probability. It also says courts look to the substance and context of the testimony rather than semantics or use of a particular term or phrase. That point cuts against arguments that depend on the exact words used.
- A 2024 Fourteenth Court opinion involving a chiropractor-treated plaintiff addressed conclusory causation testimony. It noted that to prove causation of medical conditions outside the common knowledge and experience of laymen, expert testimony is required. The excerpt does not show the outcome, but the heading says the court affirmed.

**Other**
- The Fifth District's *McGee v. Tatum* (2022) reversed in part and rendered, but the excerpts don't show whether causation was the basis.
- A 2024 Texas appellate opinion (No. 9997961) involved chiropractor Dr. Luna, whose causation opinion was elicited under the "reasonable medical probability" framing. The excerpt doesn't include the ruling.

I did not find a single case that squarely holds that a chiropractor's testimony is required, or that it is insufficient, for soft-tissue causation. For a precise holding, pull the full opinions from the links above, starting with the Donis Parties substitute opinion (2021) and the Fourteenth Court's 2023 opinion.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:08.616Z

**tool call — Bash**
````
{
 "command": "which pdftotext; f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589111887-oelhm2.pdf; python3 -I -c \"\nimport sys\ntry:\n    import pypdf\n    r=pypdf.PdfReader(sys.argv[1]); t='\\n'.join(p.extract_text() for p in r.pages[:4]); print(t[:5000])\nexcept Exception as e: print('ERR',e)\n\" \"$f\"",
 "description": "Extract text from the downloaded NJ opinion PDF"
}
````

### User / tool · 2026-11-02T03:12:08.729Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:09.719Z

**tool call — WebFetch**
````
{
 "url": "https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1",
 "prompt": "Summarize: case name, court, date, facts about medical records/billing affidavits, and holding on causation expert testimony. 5 sentences."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:10.372Z

**tool call — WebSearch**
````
{
 "query": "Flores 2003 Pediatrics errors in medical interpretation ad hoc interpreters clinical consequences",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:11.041Z

**tool call — WebSearch**
````
{
 "query": "study wrong-site laterality errors documentation left right discrepancy medical records",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:12:14.932Z

**tool result**
````
1. In *Hills v. Donis*, No. 14-18-00566-CV, decided January 14, 2020, the Texas Fourteenth District Court of Appeals in Houston reversed a trial court's judgment awarding $145,460 in past medical expenses.
2. The court explained that Section 18.001 affidavits can streamline the reasonableness and necessity of medical expenses but cannot establish that an accident caused a particular injury.
3. Medical records and billing affidavits therefore could not, on their own, prove causation.
4. The court also deemed a physician's letters, which claimed the accident caused all treated injuries, conclusory because they did not explain the basis for that conclusion.
5. Because soft tissue injuries like cervical radiculitis and lumbar disc displacement fell outside lay common knowledge, the court held that expert medical testimony was required to link the accident to the claimed injuries, found none was provided, and rendered a take-nothing judgment.
````

### User / tool · 2026-11-02T03:12:17.827Z

**tool result**
````
Web search results for query: "study wrong-site laterality errors documentation left right discrepancy medical records"

Links: [{"title":"formative.jmir.org","url":"https://formative.jmir.org/2025/1/e68436/PDF"},{"title":"Accessibility settings","url":"https://formative.jmir.org/2025/1/e68436"},{"title":"formative v9i1e68436","url":"https://formative.jmir.org/article/export/end/formative_v9i1e68436"},{"title":"formative v9i1e68436","url":"https://formative.jmir.org/article/export/ris/formative_v9i1e68436"},{"title":"machine learning approach to identifying wrong site surgeries usi","url":"https://hub.tmu.edu.tw/en/publications/machine-learning-approach-to-identifying-wrong-site-surgeries-usi/"},{"title":"www.nature.com","url":"https://www.nature.com/articles/6702590.pdf"},{"title":"An observational study of laterality errors in a sample of clinical records","url":"https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi.dedup.....79c22b5f2e483deb64b2627ef4449ead"},{"title":"20240521 19628 1b1m90i","url":"https://assets.cureus.com/uploads/original_article/pdf/254818/20240521-19628-1b1m90i.pdf"},{"title":"www.jstage.jst.go.jp","url":"https://www.jstage.jst.go.jp/browse/jodu/56/0/_contents/-char/ja"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC4501963"}]

The search turned up several studies on laterality errors in records. The most relevant ones are:

- **Eye ophthalmic clinical-notes study (ElGhrably & Fraser, 2006):** Reviewing 100 randomly selected patient record sets at an ophthalmic hospital, the authors found 44 transposition errors in 32 sets of notes. The most common error was drawing the eye on the wrong side of the page, and 19 of the errors had evidence of later correction. Three consent forms also listed the wrong eye. The authors noted they could not directly link these errors to wrong-side surgery, but suggested they could raise that risk if other safeguards failed.

- **Radiology report study (PACS/EMR database, Korea-type hospital setting, 2012–2013):** Among 29,257 radiographic examinations, 14 had laterality errors, a rate of 0.048%. Six were opposite-side errors and eight were bilateral errors. The detection and correction module caught and fixed all of them.

- **Japanese hospital incident-report analysis (2013–2021):** Left-right errors were the leading cause, accounting for 69.0% of all cases of wrong-site treatment or attempted treatment. Input errors in medical records made up about one-third of the total.

- **Machine learning study (Chen et al., JMIR Formative Research, 2025):** Using Medicare claims from 2017–2020, the researchers flagged procedure-diagnosis laterality mismatches. Among left-side procedures with right-side diagnoses, 54.5% were confirmed as errors after clinical review. The authors reported that their model outperformed traditional rule-based methods in identifying errors.

- **Cureus study on documentation of laterality in clinical letters:** This study focused on how clearly laterality is stated in diagnostic descriptions and on interventions such as provider education and reminder stickers. I didn't retrieve its results in full.

The overall picture is that documentation-level left/right errors are common relative to the rare wrong-site surgeries they can lead to. Detection through automated checks and targeted staff education both appear to help. The search returned only abstracts and excerpts, so the full methods and results of each study should be checked before relying on specific figures.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:18.171Z

**tool result**
````
Web search results for query: "Flores 2003 Pediatrics errors in medical interpretation ad hoc interpreters clinical consequences"

Links: [{"title":"Language a Barrier to Child's Health","url":"https://consumer.healthday.com/general-health-information-16/doctor-news-206/language-a-barrier-to-child-s-health-511127.html"},{"title":"medical interpreter errors","url":"https://www.newswise.com/articles/medical-interpreter-errors"},{"title":"language barriers result in high error rates in pediatric emergencies","url":"https://www.newswise.com/articles/language-barriers-result-in-high-error-rates-in-pediatric-emergencies"},{"title":"Interpreters in the ED: A Look at Errors & Consequences","url":"https://www.physiciansweekly.com/post/emergency-department-interpreter-errors"},{"title":"webarchive.library.unt.edu","url":"https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm"},{"title":"28038 speak my language lax interpreting may be a root cause of medical errors","url":"https://www.clinician.com/articles/28038-speak-my-language-lax-interpreting-may-be-a-root-cause-of-medical-errors"},{"title":"750 lost in translation lep patients often are seen and not heard","url":"https://www.clinician.com/articles/750-lost-in-translation-lep-patients-often-are-seen-and-not-heard"},{"title":"Interpreter errors are common","url":"https://www.clinician.com/articles/7148-lost-in-translation-helping-lep-patients"},{"title":"git.lsit.ucsb.edu","url":"https://git.lsit.ucsb.edu/publicdata/ahrq-gov/raw/commit/58222b51ed2ca5fbc109e641d86b5c7039a3725c/archive.ahrq.gov/research/apr03/0403RA20.htm"},{"title":"What a Human Interpreter Changes in a Research Interview (2026)","url":"https://www.koji.so/docs/interpreter-mediated-interviews-error"}]

The search turned up consistent coverage of the 2003 *Pediatrics* study (Flores, Laws, Mayo et al., vol. 111, pp. 6-14), though some results describe later work.

**The 2003 study:**
- It audiotaped 13 pediatric visits that used Spanish interpreters, and the transcripts showed about 31 interpretation errors per encounter, with a range of 10 to 60 per visit (They audiotaped 13 clinical encounters in a pediatric clinic where Spanish interpreters were used. Of the 13 visits, there were a total of 396 interpreter errors, an average of 31 errors per encounter).
- Overall, about 63% of the errors had potential medical consequences (Sixty-three percent of the errors were found to have potential medical consequences.).
- Errors by ad hoc interpreters were more likely to carry clinical consequences: 77% versus 53% for professional hospital interpreters (Mistakes by ad hoc interpreters were more likely to have potential clinical consequences than those made by professional hospital interpreters (77 percent versus 53 percent).). The ad hoc group included three nurses, three social workers and an eleven-year-old sibling.
- Error counts did not differ significantly between the two groups, so the difference lay in severity (There was no statistically significant difference between the number of errors made by hospital and ad hoc interpreters, but those made by hospital interpreters were significantly less likely to have medical consequences).
- Omission was the most common error type, at 52% (Omission: The interpreter left out a word or phrase (52%).).

**Clinical examples:** One reported case involved a misread injury. A physician believed a child had been hit, but the child had fallen off a tricycle, and the mother temporarily lost custody ("He thought the child had been hit, but in fact the child had fallen off her tricycle," Flores says, and the mother temporarily lost custody of her child.). Flores also noted that the most pressing omissions included omitting questions about drug allergies, omitting key information about the past medical history, and antibiotic dosing errors.

**Caveats:** Some results mix in later research. The figure of 1,884 errors across 57 encounters, and the 12% / 22% / 20% consequence rates, come from a 2012 *Annals of Emergency Medicine* study by Flores and colleagues, not the 2003 paper. A 2003 Pediatric Academic Societies presentation on pediatric emergency rooms also reported similar patterns. The search did not return the full text of the 2003 article, so the figures above come from press coverage and secondary summaries.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:20.506Z

**tool call — Bash**
````
{
 "command": "f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589111887-oelhm2.pdf; pdftotext -l 3 \"$f\" - | head -90",
 "description": "Extract first pages of NJ opinion text"
}
````

### User / tool · 2026-11-02T03:12:20.707Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:21.213Z

**tool call — WebSearch**
````
{
 "query": "Gunn v. McCoy Texas Supreme Court 2018 health insurer paid amounts 18.001 affidavit",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:21.965Z

**tool call — WebSearch**
````
{
 "query": "Bai Anderson Health Affairs 2015 chargemaster markup ratio hospitals charges to cost",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:22.564Z

**tool call — WebSearch**
````
{
 "query": "study handwritten medical records illegible percentage legibility doctors' handwriting audit",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:12:27.494Z

**tool result**
````
Web search results for query: "Bai Anderson Health Affairs 2015 chargemaster markup ratio hospitals charges to cost"

Links: [{"title":"Study: Chargemasters still drive up revenue at US hospitals","url":"https://www.beckershospitalreview.com/finance/study-chargemasters-still-drive-up-revenue-at-us-hospitals"},{"title":"Study: Chargemasters still drive up revenue at US hospitals","url":"https://www.beckershospitalreview.com/finance/study-chargemasters-still-drive-up-revenue-at-us-hospitals.html"},{"title":"study hospitals still using chargemaster markups maximize revenue","url":"https://www.healthcarefinancenews.com/news/study-hospitals-still-using-chargemaster-markups-maximize-revenue"},{"title":"healthcarefinancenews.com","url":"https://healthcarefinancenews.com/node/129601"},{"title":"hospitals ct scan and anesthesiology departments on average charge more than 20 times their costs","url":"https://www.newswise.com/articles/hospitals-ct-scan-and-anesthesiology-departments-on-average-charge-more-than-20-times-their-costs"},{"title":"olis.oregonlegislature.gov","url":"https://olis.oregonlegislature.gov/liz/2017I1/Downloads/CommitteeMeetingDocument/150470"},{"title":"139066 anesthesiology departments on average charge more than 20 times their costs","url":"https://www.clinician.com/articles/139066-anesthesiology-departments-on-average-charge-more-than-20-times-their-costs"},{"title":"many us hospitals mark up prices 1000 percent study says","url":"https://www.foxnews.com/health/many-us-hospitals-mark-up-prices-1000-percent-study-says"},{"title":"some hospitals marking up prices more than 1000 percent","url":"https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent"},{"title":"Some Hospitals Markup Service Costs by as Much as 1000","url":"https://www.ajmc.com/newsroom/-Some-Hospitals-Markup-Service-Costs-by-as-Much-as-1000"},{"title":"Hospitals use chargemasters to overcharge for specialty services","url":"https://www.fiercehealthcare.com/finance/hospitals-use-chargemasters-to-overcharge-for-specialty-services"},{"title":"Editor's Note","url":"https://ormanager.com/briefs/hospitals-still-using-chargemaster-markups-to-improve-revenue"},{"title":"Some Hospitals Marking Up Prices More Than Ten Times Medicare Allowables","url":"https://livingwithamplitude.com/news_2015-06-11_01/?amp=1"},{"title":"dev-hlm.wtwhmedia.com","url":"https://dev-hlm.wtwhmedia.com/node/41746"},{"title":"September 12, 2016","url":"https://www.periopleader.com/briefs/hospitals-still-using-chargemaster-markups-to-improve-revenue/"}]

The search turned up two Health Affairs papers by Ge Bai and Gerard Anderson, one from 2015 and a follow-up from 2016.

**2015 paper (2012 data):** Using Medicare cost reports, the authors measured each hospital's charge-to-cost ratio, which compares chargemaster prices with Medicare-allowable costs. The typical hospital charged, on average, 3.4 times the Medicare-allowable cost in 2012. The paper also highlighted extreme cases: of the 50 hospitals with the highest markups, 49 were for-profit, including 25 owned by Community Health Systems.

**2016 follow-up (2013 data):** This paper, titled "US Hospitals Are Still Using Chargemaster Markups To Maximize Revenues," found that a one-unit increase in the charge-to-cost ratio was associated with $64 higher patient care revenue per adjusted discharge. For hospitals with more than 50 beds, the average charge-to-cost ratio was 4.32 in 2013. By ownership type, the ratio was 3.47 in government-run hospitals, 3.79 in nonprofit hospitals, and 6.31 in for-profit hospitals.

If you need the 2015 article specifically, the 3.4x figure and the 50-hospital list are the key findings. The 2016 study is the one that reports the ratio-to-revenue link.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:28.817Z

**tool result**
````
Web search results for query: "study handwritten medical records illegible percentage legibility doctors' handwriting audit"

Links: [{"title":"An Audit of the Quality of Primary Care Medical Records 2","url":"https://imj.ie/wp-content/uploads/2023/12/An-Audit-of-the-Quality-of-Primary-Care-Medical-Records-2.pdf"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250"},{"title":"Doctors' Handwriting-- Is It Really That Bad?","url":"https://reliasmedia.com/articles/36982-doctors-handwriting-is-it-really-that-bad"},{"title":"Illegible handwriting in medical records","url":"https://scilit.com/publications/41918677245f7aa41c57e59e50307f8d"},{"title":"safpj.co.za","url":"https://safpj.co.za/index.php/safpj/article/download/4658/5518"},{"title":"can you read this legibility and hospital records a multi stakeho","url":"https://research.ucc.ie/en/publications/can-you-read-this-legibility-and-hospital-records-a-multi-stakeho/"},{"title":"36982 doctors handwriting is it really that bad","url":"https://www.clinician.com/articles/36982-doctors-handwriting-is-it-really-that-bad"},{"title":"mdl 9090521","url":"https://busqueda.bvsalud.org/portal/resource/es/mdl-9090521"},{"title":"Doctors handwriting","url":"https://accedacris.ulpgc.es/bitstream/10553/74578/2/Doctors_handwriting.pdf"},{"title":"Vol , Issue Date of Publication: January 01, 2009","url":"https://ijme.in/articles/doctor-is-your-writing-legible/?galley=html"}]

The search turned up several studies that measured legibility, with results that vary widely.

- **Spanish hospital audit (2002):** Rodríguez-Vera and colleagues examined 117 case notes and found 18 (15%) were scored 1 or 2—i.e. they were so illegible that the meaning was unclear. The authors noted that the study might have been skewed by the poor handwriting of just a few clinicians who were responsible for many admissions.
- **Medication orders (Winslow et al.):** Nurses rated handwritten orders, and 20 percent of the medication orders and 78% of the signatures were illegible or legible with effort. Twenty-four percent of the medication orders were incomplete.
- **Irish hospital records:** A study in Cork hospitals reported that 22.2% of records were signed, most were illegible, rendering them effectively anonymous. A separate Irish study on physicians' notes concluded that estimations of legibility of medical records are influenced by observer attributes and possibly by the discipline from which such case notes originate.
- **Doctors versus other professions:** Berwick and Winickoff's 1996 BMJ study found physicians' handwriting is no worse than a comparison group of other health care personnel. Lyons et al. (1998) likewise found no significant difference between doctors and non-doctors. A 2009 commentary cited a study claiming doctors write worse than other professionals, so the evidence is mixed.

The main takeaway is that reported illegibility rates range from roughly 15% to 20% in the audits above, but the figures depend on the reader, the setting, and the sample. I didn't find a single definitive national percentage.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:29.328Z

**tool result**
````
Web search results for query: "Gunn v. McCoy Texas Supreme Court 2018 health insurer paid amounts 18.001 affidavit"

Links: [{"title":"www.mwl law","url":"https://www.mwl-law.com/?p=8407"},{"title":"KMH SCOTX: INSURANCE AGENTS MAY KNOW MORE ABOUT REASONABLE AND NECESSARY MEDICAL EXPENSES THAN DOCTORS AND HOSPITALS","url":"https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html"},{"title":"GUNN v. MCCOY","url":"https://www.studicata.com/summaries/supreme-court-of-texas/gunn-v-mccoy-2018-5hujs2"},{"title":"fletcherfarley.com","url":"https://www.fletcherfarley.com/assets/htmldocuments/August%202018%20Newsletter.pdf"},{"title":"Texas Supreme Court allows streamlined approach to medical billing affidavits","url":"https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/"},{"title":"debra c gunn m d 4285232","url":"https://app.midpage.ai/case/debra-c-gunn-m-d-4285232"},{"title":"Recovery%20of%20Medical%20Expenses%20 %20DLF","url":"https://cooperscully.com/uploads/file/Recovery%20of%20Medical%20Expenses%20-%20DLF.pdf"},{"title":"utcle.org","url":"https://utcle.org/elibrary/download/a/38567/p/1"},{"title":"in re allstate indemnity company 10485066","url":"https://app.midpage.ai/case/in-re-allstate-indemnity-company-10485066"},{"title":"Developments in Texas 'paid and incurred' law for medical bills","url":"https://painterfirm.com/medmal/developments-in-texas-paid-and-incurred-law-for-medical-bills/"},{"title":"Gunn v. McCoy","url":"https://case-law.vlex.com/vid/gunn-v-mccoy-no-889244322"},{"title":"IN THE SUPREME COURT OF TEXAS","url":"https://www.txcourts.gov/media/1452189/200071.pdf"},{"title":"untdallas.edu","url":"https://onthecusp.untdallas.edu/docs/2022-and-prior/amendmentstotexascivilpracticeremediescodesection18.001.spring.2020.pdf"},{"title":"gunn v mccoy 5285320","url":"https://app.midpage.ai/case/gunn-v-mccoy-5285320"},{"title":"News & Blog","url":"https://settlepou.com/?p=1420"},{"title":"debra c gunn md obstetrical 4058342","url":"https://app.midpage.ai/case/debra-c-gunn-md-obstetrical-4058342"},{"title":"www.pappasgrubbs.com","url":"https://www.pappasgrubbs.com/?p=1380"}]

The Texas Supreme Court's decision in Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), held that subrogation agents for health insurers can sign § 18.001 affidavits proving paid medical amounts. The results agree on the holding but give conflicting dates.

- **Holding:** The plaintiff first used affidavits from providers, then replaced them with affidavits from the insurers' subrogation agents reflecting amounts actually paid. The defendants argued § 18.001 limits affiants to providers or their records custodians, and the Court rejected that argument. One source notes the statute's plain text does not require a records custodian for a medical provider. (Plaintiffs later withdrew those affidavits, however, and replaced them with affidavits from subrogation agents for the health insurance carriers that had actually paid the patient's medical expenses. But defendants objected to these affidavits arguing that section 18.001 limits the proper affiants to providers or the record custodians for those providers. The Court disagreed. The plain language of Section 18.001 "does not require that affidavits be made by a records custodian for a medical provider.")
- **Context:** The decision builds on Haygood v. De Escabedo (2011), which limited recovery to amounts actually paid or incurred. (The plaintiff withdrew those affidavits and substituted them with new affidavits from subrogation agents for the health insurance carriers who had paid the plaintiff's medical bills, reflecting the amounts that had actually been paid.)
- **Date conflict:** One source gives February 8, 2018, while others give June 15, 2018 (On June 15, 2018, the Texas Supreme Court released a major opinion). The June date matches the citation, and a rehearing denial dated September 28, 2018 is noted in one source. Treat June 15, 2018 as the decision date and verify before citing.
- **Later treatment:** The Court later cited Gunn for the point that vendors of pricing data can be qualified to testify about reasonableness of medical expenses (In re Allstate Indemnity, 2021). (Vendors of pricing data can be qualified to testify about reasonableness of medical expenses) In re Allstate, decided May 7, 2021, is a separate case on contesting § 18.001(f) affidavits.
- **Source caveat:** The summaries are secondary sources, and one has a typo in the case name ("McKoy"). I did not find the full opinion text in these results, so check the opinion itself before relying on specifics such as pin cites.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:48.321Z

**tool call — WebSearch**
````
{
 "query": "In re Central Oregon Truck Co. Texas Supreme Court 2022 letter of protection discovery referral relationship",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:49.670Z

**tool call — WebFetch**
````
{
 "url": "https://hallapproved.com/tx/cases/appeals/2025/10659616/",
 "prompt": "What is this case (name, court, date)? Summarize issues about Spanish language, interpreter, translation of deposition or medical records, and medical causation or damages. 5 sentences, no personal details beyond the caption."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:50.522Z

**tool call — WebSearch**
````
{
 "query": "Powell 2008 emergency department mild traumatic brain injury missed diagnosis 56% Archives Physical Medicine",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:12:51.113Z

**tool call — WebSearch**
````
{
 "query": "GAO ground ambulance billing mileage charges report 2023 out-of-network",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:12:56.278Z

**tool result**
````
Web search results for query: "Powell 2008 emergency department mild traumatic brain injury missed diagnosis 56% Archives Physical Medicine"

Links: [{"title":"new study finds emergency room physicians often fail to diagnose tbi","url":"https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi"},{"title":"Accuracy of Mild Traumatic Brain Injury Diagnosis","url":"https://vufind-test.katalog.k.utb.cz/SummonRecord/FETCH-LOGICAL-c588t-bdbaace62b54a7da18f0a28f06a918ebcd98bdd881efb5f64e2ce4c1507a04723"},{"title":"ott.law","url":"https://ott.law/?p=5243"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC5629740"},{"title":"Ott Law Firm","url":"https://ott.law/blog/emergency-room-misconceptions-unraveling-tbi-misdiagnoses"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC6479243"},{"title":"etd.library.emory.edu","url":"https://etd.library.emory.edu/concern/etds/x633f194s?locale=fr"},{"title":"Article Text","url":"https://bmjopen.bmj.com/content/10/2/e034494"},{"title":"core-cms.cambridgecore.org","url":"https://core-cms.cambridgecore.org/core/journals/canadian-journal-of-emergency-medicine/article/p057-diagnosis-for-mild-traumatic-brain-injury-in-three-canadian-emergency-departments-missed-opportunities/1A23762DE2B5100A6F671AD50125E06E"},{"title":"early identification and incidence of mild tbi in ontario","url":"https://core-prod.cambridgecore.org/core/services/aop-cambridge-core/content/view/F18D5FA11A6655640CEBFE0969275774/S0317167100007745a.pdf/early_identification_and_incidence_of_mild_tbi_in_ontario.pdf"}]

The search confirms the study and its headline figure. The 2008 paper is Powell et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis," in the Archives of Physical Medicine and Rehabilitation, vol. 89, no. 8, pp. 1550–1555. It asked how often emergency department patients meeting CDC mild TBI criteria were diagnosed with a mild TBI by the ED physician. The 56% figure refers to mild TBI cases identified by study personnel that lacked a documented mild TBI-related diagnosis in the ED record.

Later work cites the same number. One review describes it as 56% of patients with clinically defined mild TBI determined by patient interview did not have a documented TBI diagnosis from the ED. A Sydney protocol notes that ED staff were more focused on ruling out severe brain injury for patients with a likely mechanism for TBI.

The authors suggested that asking a few targeted questions of ED patients with likely mechanisms of injury that could result in mild TBI could begin to improve diagnosis.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:56.468Z

**tool result**
````
Web search results for query: "In re Central Oregon Truck Co. Texas Supreme Court 2022 letter of protection discovery referral relationship"

Links: [{"title":"txcourts.gov","url":"https://www.txcourts.gov/media/1454150/200945pc.pdf"},{"title":"cases.justia.com","url":"https://cases.justia.com/texas/supreme-court/2022-20-0945.pdf"},{"title":"texas high court rulings on medical expense damages reel in plaintiffs windfall profit tactics","url":"https://wlf.org/2021/06/24/publishing/texas-high-court-rulings-on-medical-expense-damages-reel-in-plaintiffs-windfall-profit-tactics"},{"title":"• Subscribe","url":"https://texaslawbook.net/scotx-ponders-demands-for-uninsured-medical-charges"},{"title":"• Subscribe","url":"https://texaslawbook.net/?p=71786"},{"title":"• Subscribe","url":"https://texaslawbook.net/verdict-in-personal-injury-case-may-limit-future-attorney-physician-protections/"},{"title":"Court of Civil Appeals of Texas, 2020","url":"https://hallapproved.com/tx/cases/appeals/2020/4788318/"},{"title":"texaslawbook.net","url":"https://texaslawbook.net/?p=101205"},{"title":"06252021Mickus2 LB","url":"https://www.wlf.org/wp-content/uploads/2021/06/06252021Mickus2_LB.pdf"},{"title":"1262022FieldFiloso LOL","url":"https://wlf.org/wp-content/uploads/2022/01/1262022FieldFiloso_LOL.pdf"},{"title":"show me the money texas expands the discoverability of medical providers billing practices","url":"https://wlf.org/2022/01/28/publishing/show-me-the-money-texas-expands-the-discoverability-of-medical-providers-billing-practices"},{"title":"U.S.20Chamber2C20et.20al20Amicus20Letter20 20In20re20K26L20Auto20Crushers2C20LLC20and20Thomas20Gothard20Jr.2028Texas20Supreme20Court29","url":"https://www.uschamber.com/assets/documents/U.S.20Chamber2C20et.20al20Amicus20Letter20-20In20re20K26L20Auto20Crushers2C20LLC20and20Thomas20Gothard20Jr.2028Texas20Supreme20Court29.pdf"},{"title":"Client%20Alert%20June 2 2021","url":"https://fletcherfarley.com/assets/htmldocuments/Client%20Alert%20June_2_2021.pdf"},{"title":"scotx grants mandamus in paid or incurred case involving letters of protection","url":"https://tcjl.com/scotx-grants-mandamus-in-paid-or-incurred-case-involving-letters-of-protection/"},{"title":"U.S.20Chamber2C20et.20al20Amicus20Letter20 20In20re20ExxonMobil20Corp.2028Texas20Supreme20Court29","url":"https://www.uschamber.com/assets/documents/U.S.20Chamber2C20et.20al20Amicus20Letter20-20In20re20ExxonMobil20Corp.2028Texas20Supreme20Court29.pdf"},{"title":"www.txcourts.gov","url":"https://www.txcourts.gov/media/1453166/200849pc.pdf"},{"title":"shippers prevail in trucking case discovery disputes","url":"https://tcjl.com/shippers-prevail-in-trucking-case-discovery-disputes/"}]

The search turned up the Texas Supreme Court's 2022 per curiam mandamus opinion, but the results didn't include its full text, so I can't confirm its holding on the referral relationship.

- **Case basics:** The docket is No. 20-0945, a mandamus proceeding with Christina Broussard suing Relators David Hupp and Central Oregon Truck Company for personal injuries and economic losses following a 2017 rear-end collision.
- **Outcome:** A Texas Courts summary of the opinion says the court granted mandamus relief to a relator whose discovery requests sought relevant evidence of a health care provider's negotiated rates for specific services performed on behalf of a plaintiff.
- **Related precedent:** Commentators describe a line of 2021 decisions. The May 28, 2021 In re K & L Auto Crushers decision lays the foundation for defendants to blunt the often-abusive effects of "letter of protection" arrangements. The earlier In re North Cypress ruling (2018) is also cited as the basis for these discovery rulings. In In re N. Cypress Medical Ctr. Operating Co., 559 S.W.3d 128 (Tex. 2018), North Cypress held that the discovery was permissible.
- **Referral relationship:** I found nothing in these results tying Central Oregon specifically to a referral relationship. One article notes that the Letters of Protection agreement was shown to the jury, exploring the entities set up by the providers solely for the purposes of handling letter of protection litigation patients. That appears to be from a different case, so treat it as context rather than as this opinion's facts.

For the actual holding and any discussion of referral arrangements, the opinion itself is at txcourts.gov (No. 20-0945) or cases.justia.com (2022-20-0945.pdf).


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:12:56.655Z

**tool result**
````
This is *Brandon Chiv v. Ranferi Monge Figueroa*, decided August 21, 2025, by the Court of Appeals of Texas, First District (No. 01-23-00638-CV). Chiv argued that the trial court wrongly barred him from refreshing a witness's memory with his deposition transcript because it was not a certified Spanish translation, even though a certified Spanish interpreter was present at trial. The appellate court overruled this issue, finding that the record did not support Chiv's account of the rulings and that he had not preserved error. On medical records and causation, the court held that the trial court erred by striking Chiv's counteraffidavit and admitting section 18.001 affidavits, and that this was harmful because the only non-lay causation evidence came from admitted medical reports, so it reversed the past medical expense award and remanded for a new trial. On damages, the court upheld the future pain award without expert testimony but found the evidence legally insufficient for past mental anguish, rendering a take-nothing judgment on that claim.
````

### User / tool · 2026-11-02T03:12:57.722Z

**tool result**
````
Web search results for query: "GAO ground ambulance billing mileage charges report 2023 out-of-network"

Links: [{"title":"Most Patients Undergoing Ground And Air Ambulance Transportation Receive Sizable Out-Of-Network Bills","url":"https://www.healthaffairs.org/doi/citedby/10.1377/hlthaff.2019.01484"},{"title":"Dive Brief:","url":"https://www.healthcaredive.com/news/out-of-network-transport-larger-share-ground-ambulance-claims-fair-health/693681/"},{"title":"PPI Emerg Ground Ambulance Costs","url":"https://www.elevancehealth.com/content/dam/elevance-health/articles/ppi_assets/reports/PPI_Emerg_Ground_Ambulance_Costs.pdf"},{"title":"A Window into Utilization and Cost of Ground Ambulance Services   A FAIR Health Brief","url":"https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf"},{"title":"• Skip to main content","url":"https://hitconsultant.net/2023/09/15/ground-ambulance-rides-were-out-of-network-in-2022"},{"title":"www.mass.gov","url":"https://www.mass.gov/doc/presentation-out-of-network-billing-in-massachusetts/download"},{"title":"Average In-Network Amount for Advanced-Life-Support Ground Ambulance Transport Rose 56 Percent from 2017 to 2020","url":"https://prnewswire.com/news-releases/average-in-network-amount-for-advanced-life-support-ground-ambulance-transport-rose-56-percent-from-2017-to-2020-301486164.html"},{"title":"www.pubmed.ncbi.nlm.nih.gov","url":"https://www.pubmed.ncbi.nlm.nih.gov/32293925/"},{"title":"masshpc.gov","url":"https://masshpc.gov/sites/default/files/2023-01/OON%20Billing%20Slides.pdf"},{"title":"www.healthaffairs.org","url":"https://www.healthaffairs.org/do/10.1377/forefront.20200415.924029"},{"title":"Trending Topics","url":"https://www.ems1.com/billing-and-administration/ground-ambulance-billing-reform-a-roadmap-for-congress"},{"title":"GAO: Air ambulances can come with big surprise bills—even for patients with private insurance","url":"https://fiercehealthcare.com/hospitals-health-systems/gao-air-ambulances-can-be-costly-ride-even-for-insured-patients"},{"title":"2022 08 ambulance patient","url":"https://medicalxpress.com/news/2022-08-ambulance-patient.pdf"},{"title":"emergency ground ambulance costs trends and policy implications","url":"https://www.elevancehealth.com/public-policy-institute/emergency-ground-ambulance-costs-trends-and-policy-implications"},{"title":"Over 25% of commercially insured ground ambulance trips could come with a surprise bill: study","url":"https://fiercehealthcare.com/providers/over-25-commercially-insured-ground-ambulance-trips-could-come-surprise-bill-study"},{"title":"SEIZE THE $50 BILLION SITE-OF-CARE SHIFT OPPORTUNITY","url":"https://advisory.com/daily-briefing/2022/12/15/ambulance-billing"}]

I didn't find a 2023 GAO report on ground ambulance mileage charges in these results, so I can't confirm that report exists.

- **Nearest GAO work:** The results cite a GAO air ambulance report from 2019 (GAO-19-292), but they don't describe its contents. A GAO air ambulance report from 2017 found that about 70% of about 21,000 transports were out of network. The GAO looked at nearly 21,000 air ambulance transports in 2017 and found nearly 70% were out of network. In comparison, research has previously shown that about half of all ground ambulance transports are out of network.
- **Ground ambulance prices:** A Health Affairs study of a large national plan (2013–17) found that out-of-network ground ambulance bills were more common, with an aggregate impact of $129 million per year.
- **Mileage data:** FAIR Health's brief on 2018–2022 claims reports that the lowest average allowed amounts for ground ambulance mileage per statute mile in 2022 occurred in Florida ($5.79), Maine ($7.55), North Carolina ($7.66), Vermont ($7.71) and Maryland ($8.21). It also reports that out-of-network rides made up 63.7 percent of all ground ambulance claim lines in 2018 and 59.4 percent in 2022.
- **Policy context:** Ground ambulances aren't covered by the No Surprises Act, per an Elevance Health PPI paper. A later advisory committee report to Congress, dated March 29, 2024 according to EMS1, recommended banning out-of-network balance billing for ground ambulance services.

For the GAO report you're after, I'd check gao.gov directly, searching for "ground ambulance" with the 2023 date filter.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:01.488Z

**tool call — WebFetch**
````
{
 "url": "https://www.txcourts.gov/media/1454150/200945pc.pdf",
 "prompt": "Give decision date and summarize: what billing/LOP facts (uninsured plaintiff, letters of protection, providers' billed charges, negotiated rates with insurers, Medicare rates), what discovery was sought, and the holding. 6 sentences."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:02.338Z

**tool call — WebSearch**
````
{
 "query": "Texas court of appeals biomechanical engineer testimony low speed collision minimal property damage injury causation admissible",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:03.189Z

**tool call — WebSearch**
````
{
 "query": "texasworker.com appeals panel interpreter mistranslation recorded statement medical history Spanish claimant credibility",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:03.834Z

**tool call — WebSearch**
````
{
 "query": "Rodriguez-Vera 2002 \"Illegible handwriting in medical records\" Journal of the Royal Society of Medicine 117 case notes",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:13:06.416Z

**tool result**
````
<outside-repo file omitted>
````

### User / tool · 2026-11-02T03:13:08.960Z

**tool result**
````
Web search results for query: "Rodriguez-Vera 2002 "Illegible handwriting in medical records" Journal of the Royal Society of Medicine 117 case notes"

Links: [{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC539384"},{"title":"Illegible handwriting in medical records","url":"https://scilit.com/publications/41918677245f7aa41c57e59e50307f8d"},{"title":"Vol , Issue Date of Publication: January 01, 2009","url":"https://ijme.in/articles/doctor-is-your-writing-legible/?galley=html"},{"title":"jhanley.biostat.mcgill.ca","url":"https://jhanley.biostat.mcgill.ca/bios601/Surveys/DoctorsHandwriting.pdf"},{"title":"ijme.in","url":"https://ijme.in/wp-content/uploads/2016/11/1420-5.pdf"},{"title":"pmc.ncbi.nlm.nih.gov","url":"https://pmc.ncbi.nlm.nih.gov/articles/PMC1676338"},{"title":"Poor Handwriting: Does it Lead to Medical Error?","url":"https://isqua.org/poor-handwriting-does-it-lead-to-medical-error/"},{"title":"poor handwriting does it lead to medical error","url":"https://isqua.org/resources-blog/blog/poor-handwriting-does-it-lead-to-medical-error.html"},{"title":"safpj.co.za","url":"https://safpj.co.za/index.php/safpj/article/download/4658/5518"}]

The paper is confirmed: Rodríguez-Vera FJ et al., "Illegible handwriting in medical records," *J R Soc Med* 2002;95(11):545–546, DOI 10.1258/jrsm.95.11.545.

- **The 117 case notes:** The authors examined 117 sets of notes. Eighteen (about 15%) were so unreadable that their meaning was unclear. Surgical departments scored worse than medical ones. 117 case notes were examined and 18 (15%) were scored 1 or 2—i.e. they were so illegible that the meaning was unclear.
- **Department breakdown:** The article's Table 1 gives per-specialty scores. Table 1, giving results for individual specialties, indicates that surgical departments performed worse than medical departments.
- **Follow-up letter:** A 2003 JRSM letter by Thompson, Jacob and Fulton cites the study and reports that in 53% of the records the doctor's name was either illegible or not documented. That figure comes from the letter, not the original paper, so I'd verify it against the article itself before relying on it.
- **Later citations:** Other papers cite this study for the 15% finding. One notes that in 2002, a report in this Journal revealed that 15% of case histories were illegible.

I did not access the full text, so the sample breakdown beyond these results and the exact table values are unverified.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:13:10.114Z

**tool result**
````
Web search results for query: "Texas court of appeals biomechanical engineer testimony low speed collision minimal property damage injury causation admissible"

Links: [{"title":"heplerbroom.com","url":"https://www.heplerbroom.com/assets/htmldocuments/DRI%20Are%20you%20Retaining%20the%20Right%20Expert.pdf"},{"title":"05 20 00443 cv","url":"https://law.justia.com/cases/texas/fifth-court-of-appeals/2022/05-20-00443-cv.html"},{"title":"Texas Appeals Court: Biomechanical Engineer Testimony Properly Excluded","url":"https://law360.com/mealeys/mealeys-daubert/articles/1855439/texas-appeals-court-biomechanical-engineer-testimony-properly-excluded"},{"title":"2004 UP 633","url":"https://sccourts.org/opinions/unpublishedopinions/HTMLFiles/COA/2004-UP-633.htm"},{"title":"2015 11 03 reda dri in transit retaining right expert winter 2015","url":"https://heplerbroom.com/wp-content/uploads/2026/07/2015-11-03-reda-dri-in-transit-retaining-right-expert-winter-2015.pdf"},{"title":"cabadvantage.com","url":"https://cabadvantage.com/articles/?p=15779"},{"title":"Texas Appeals Court: Biomechanical Engineer Testimony Properly Excluded","url":"https://www.mealeys.com/mealeys/amp/articles/1855439"},{"title":"Don’t let “junk science” ruin your low-impact, rear-ender case","url":"https://plaintiffmagazine.com/recent-issues/item/don-t-let-junk-science-ruin-your-low-impact-rear-ender-case"},{"title":"Call Us 281.395.5497Call Us 281.395.5497 ☰ ˟","url":"https://77cae6e0-1a1f-4870-b99b-bff5c53b5a9a.insurancewebsitebuilder.com/blog/Evaluating_Injury_Causation_in_Low_Speed_Automobile_Collisions.aspx"},{"title":"Brown v. United States of America, No. 1:2020cv00359 - Document 30 (W.D. Tex. 2021)","url":"https://law.justia.com/cases/federal/district-courts/texas/txwdce/1:2020cv00359/1094088/30/"},{"title":"HAMPTON v. MISKELL","url":"https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb"},{"title":"cite.case.law","url":"https://cite.case.law/a3d/171/98/"},{"title":"Please ensure Javascript is enabled for purposes of website accessibility","url":"https://sclawyersweekly.com/?p=2182"},{"title":"law review daubert to biomechanical experts ea37711a","url":"https://assets.noviams.com/novi-file-uploads/tbtla/Documents/Low_Speed_Measurement_and_Injury/law_review_daubert_to_biomechanical_experts-ea37711a.pdf"},{"title":"www.smithfreed.com","url":"https://www.smithfreed.com/?p=2864"},{"title":"Court of Civil Appeals of Texas, 2000","url":"https://hallapproved.com/tx/cases/appeals/2000/2862644/"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9992916/"},{"title":"Court of Civil Appeals of Texas, 2016","url":"https://hallapproved.com/tx/cases/appeals/2016/5447838/"},{"title":"Court of Civil Appeals of Texas, 2005","url":"https://hallapproved.com/tx/cases/appeals/2005/2922090/"}]

The search turned up a few Texas appellate matters, but only one has a holding I can describe, and it's about an accident reconstructionist rather than a biomechanical engineer.

**Texas authority**
- A Dallas-area appellate decision reported by Mealey's holds that Texas courts do allow biomechanical engineers to offer expert testimony in car accident cases, but a trial court did not err in excluding an expert who did not offer adequate support. The excerpt is cut off, so I couldn't confirm the expert's specific deficiency.
- In *Hampton v. Miskell* (2017), the court held that the trial court did not abuse its discretion in admitting an accident reconstructionist's opinion that the vehicle was moving at five miles per hour or less. The court also treated that low-speed testimony as cumulative of other evidence regarding minor property damage, so any error would not have materially affected the verdict.
- A Fifth District case, *Silva v. Diaz* (No. 05-20-00443-CV, 2022), appeared in results, but the excerpt contains only the caption, so I can't say what it held.

**Out-of-state and general commentary**
- A South Carolina decision (2-1) barred a defendant from introducing biomechanics testimony that a low-speed impact did not injure the plaintiff, and the dissent argued that exclusion was prejudicial. The court ruled 2-1 that the defendant could not introduce testimony from a biomechanics expert to show that a passenger was not injured by the low-speed impact.
- Commentary notes that some courts will not allow a non-physician biomedical/biomechanical engineer to testify as to whether or not a low speed motor vehicle collision caused or aggravated the claimant's condition. Another article reports that some states do not allow biomechanical engineers to testify as experts.

**Gaps:** I didn't find a Texas appellate opinion squarely deciding whether a biomechanical engineer may give injury-causation opinions in a low-speed, minimal-damage collision. For that, I'd pull the full text of the Mealey's-reported Dallas decision and search Texas case law for "biomechanical" with Rule 702 or *Robinson*/*Daubert* terms.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:13:13.273Z

**tool result**
````
Web search results for query: "texasworker.com appeals panel interpreter mistranslation recorded statement medical history Spanish claimant credibility"

Links: [{"title":"texasworker.com","url":"https://texasworker.com/?p=38445"},{"title":"texasworker.com","url":"https://texasworker.com/?p=38127"},{"title":"texasworker.com","url":"https://texasworker.com/?p=38671"},{"title":"texasworker.com","url":"https://texasworker.com/?p=28229"},{"title":"texasworker.com","url":"https://texasworker.com/?p=19110"},{"title":"texasworker.com","url":"https://texasworker.com/?p=19882"},{"title":"texasworker.com","url":"https://texasworker.com/?p=20695"},{"title":"texasworker.com","url":"https://texasworker.com/?p=33717"},{"title":"texasworker.com","url":"https://texasworker.com/?p=30712"},{"title":"texasworker.com","url":"https://texasworker.com/?p=28278"},{"title":"texasworker.com","url":"https://texasworker.com/?p=35825"},{"title":"texasworker.com","url":"https://texasworker.com/?p=35780"},{"title":"texasworker.com","url":"https://texasworker.com/?p=30253"},{"title":"texasworker.com","url":"https://texasworker.com/?p=36866"},{"title":"texasworker.com","url":"https://texasworker.com/?p=31997"},{"title":"texasworker.com","url":"https://texasworker.com/?p=19850"},{"title":"texasworker.com","url":"https://texasworker.com/?p=33093"},{"title":"texasworker.com","url":"https://texasworker.com/?p=18592"},{"title":"texasworker.com","url":"https://texasworker.com/?p=19581"},{"title":"texasworker.com","url":"https://texasworker.com/?p=20823"}]

I found several Appeals Panel decisions on interpreter problems and Spanish-language statements, but none that directly addresses a mistranslated medical history and claimant credibility. The results are mostly older decisions, and I didn't check whether they remain current.

- **Recording and translation review:** In one decision, the Division's own translator produced a translation for the panel, and the panel reviewed both the hearing recording and that translation on appeal. Following the receipt of the claimant's appeal and the carrier's response, the Division's own translator provided a translation to the Appeals Panel of the CCH. The CD recording and the Division's own translation were reviewed on appeal. In that case, the interpreter also used the Spanish word for cane where the claimant meant crutches. In some instances the interpreter used the Spanish word for cane rather than crutches.
- **Ambiguous word in a Spanish statement:** A claimant argued that the word "espalda" caused confusion, but the panel affirmed. It noted that a statement in Spanish by the claimant, which was one of the carrier's exhibits at the hearing, does include "espalda," the word that the claimant now says may have led to the confusion, and that the translation and the Spanish statement indicate that the claimant used another phrase when describing the area between his shoulder blades.
- **Interpreter adequacy:** A claimant's interpreter challenge was based on the hearing officer reprimanded the interpreter for not providing word-for-word translation. The search results don't show how that argument was resolved.
- **Unreliable recordings:** In an older case, the record was so poor that the panel remanded for reconstruction. On tape 1 of the tape-recorded record of the proceedings below, the statements by the person who provided the English-Spanish translations on April 23, 1993, are essentially inaudible making it virtually impossible for the Appeals Panel to decipher the testimony.
- **Admissibility of Spanish statements:** One decision addressed a recorded interview taken in Spanish and translated late. The claimant objected on hearsay grounds, and carrier did not state when the statement was taken nor explain the delay in obtaining the translation.
- **Accommodations rule:** 28 TEX. ADMIN. CODE § 140.2(a) (Rule 140.2(a)) provides that the Texas Department of Insurance, Division of Workers' Compensation (Division) on its own motion or upon request, will provide special accommodations to an individual who intends to participate in a proceeding and who does not speak English.

For the specific question, the closest results are the "espalda" decision, which turned on a translation comparison, and the Division-translation decision, which turned on reviewing the recording. Searching for the decision numbers or the phrase "credibility" with "interpreter" on texasworker.com would be the next step.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:15.344Z

**tool call — Bash**
````
{
 "command": "f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589181798-t7ymkl.pdf; pdftotext \"$f\" - | tr -s '\\n' | head -120",
 "description": "Extract Central Oregon Truck opinion text"
}
````

### User / tool · 2026-11-02T03:13:15.455Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:18.876Z

**tool call — Bash**
````
{
 "command": "f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589181798-t7ymkl.pdf; pdftotext \"$f\" - | grep -iE \"OPINION DELIVERED|20[12][0-9]$\" | tail -5",
 "description": "Find decision date in Central Oregon opinion"
}
````

### User / tool · 2026-11-02T03:13:18.997Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:22.491Z

**tool call — WebFetch**
````
{
 "url": "https://texasworker.com/?p=38127",
 "prompt": "Give appeal number, decision date, and summarize the interpreter/Spanish translation issue (e.g., 'espalda', cane vs crutches) and how it affected the injury/body-part determination. 4 sentences, no names."
}
````

### User / tool · 2026-11-02T03:13:22.871Z

**tool result**
````
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:23.827Z

**tool call — WebFetch**
````
{
 "url": "https://www.txcourts.gov/media/943999/130978.pdf",
 "prompt": "Summarize the medical-record timeline: first accident date (month/year), ER visit and complaints, second accident timing, complaints after second accident, MRI, surgery, and the court's holding on alternative causation evidence. Give opinion delivered date. 6 sentences."
}
````

### User / tool · 2026-11-02T03:13:27.211Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:30.437Z

**tool call — Bash**
````
{
 "command": "f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589203929-k5xovc.pdf; pdftotext \"$f\" - | tr -s '\\n' | sed -n '1,25p;/Background\\|I\\. /,+45p' | head -110; pdftotext \"$f\" - | grep -i \"delivered\"",
 "description": "Extract JLG Trucking opinion facts"
}
````

### User / tool · 2026-11-02T03:13:30.632Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:33.219Z

**tool call — Bash**
````
{
 "command": "f=/Users/arsis/.claude/projects/-Users-arsis-zlayt-pm-project/6ddf8076-ef73-4074-b5ec-179e748564f8/tool-results/webfetch-1793589203929-k5xovc.pdf; pdftotext \"$f\" - | tr -s '\\n' | sed -n '25,75p'",
 "description": "Read JLG facts section"
}
````

### User / tool · 2026-11-02T03:13:33.385Z

**tool result**
````
<outside-repo file omitted>
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:50.295Z

**tool call — WebSearch**
````
{
 "query": "Fishbain 2003 Waddell signs secondary gain malingering systematic review Clinical Journal of Pain",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:50.995Z

**tool call — WebSearch**
````
{
 "query": "ElGhrably Fraser \"observational study of laterality errors\" clinical records ophthalmic",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:52.047Z

**tool call — WebFetch**
````
{
 "url": "https://pubmed.ncbi.nlm.nih.gov/36156143/",
 "prompt": "Give authors, journal, year/date, sample size and main findings (percent duplicated text, same vs different author). 4 sentences."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:13:53.248Z

**tool call — WebFetch**
````
{
 "url": "https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb",
 "prompt": "Give court, date, and summarize facts about low-speed collision, property damage, medical treatment and the evidentiary holding. 4 sentences, no personal details beyond caption."
}
````

### User / tool · 2026-11-02T03:13:53.463Z

**tool result**
````
The server returned HTTP 403 Forbidden.

The response body was not retrieved. If this URL requires authentication, use an authenticated tool (e.g. `gh` for GitHub, or an MCP-provided fetch tool) instead of WebFetch.
````

### User / tool · 2026-11-02T03:13:55.730Z

**tool result**
````
Web search results for query: "ElGhrably Fraser "observational study of laterality errors" clinical records ophthalmic"

Links: [{"title":"www.nature.com","url":"https://www.nature.com/articles/6702590.pdf"},{"title":"An observational study of laterality errors in a sample of clinical records","url":"https://opact.sdu.edu.tr/vufind/SummonRecord/FETCH-LOGICAL-c452t-55ba8903b311cc5a0a84e6e677dca082a32aeb54e5f315760e956f5c19237e9b3"},{"title":"An observational study of laterality errors in a sample of clinical records","url":"https://katalog.lib.cas.cz/KNAV/EdsRecord/edsair,edsair.doi.dedup.....79c22b5f2e483deb64b2627ef4449ead"},{"title":"observational study laterality errors sample clinical records","url":"https://psnet.ahrq.gov/issue/observational-study-laterality-errors-sample-clinical-records"},{"title":"4.6 Article","url":"https://peeref.com/works/78533162"},{"title":"nature.com","url":"https://www.nature.com/articles/6702590"},{"title":"wrong site surgery","url":"https://psnet.ahrq.gov/issue/wrong-site-surgery"},{"title":"laterality errors and risk reduction across the entire care pathw","url":"https://researchnow.flinders.edu.au/en/publications/laterality-errors-and-risk-reduction-across-the-entire-care-pathw/"},{"title":"Systematic bias in real-world tonometry readings based on laterality?","url":"https://researchonline.lshtm.ac.uk/id/eprint/4653657"},{"title":"Lessons from Ophthalmology in Preventing Wrong-Site Errors in Paired-Organ Surgery","url":"https://library.kab.ac.ug/Record/doaj-art-4c1322cab250493aa8e09cd3a0794549/Description"}]

The study is ElGhrably I and Fraser SG, "An observational study of laterality errors in a sample of clinical records," published in *Eye* in 2008 (22(3):340-343). It was a chart review at Sunderland Eye Infirmary, a dedicated ophthalmic hospital.

- **Method:** One hundred patients were randomly selected and their clinical notes retrieved. Reviewers counted left/right transpositions, where in the notes each was found, and whether it was corrected.
- **Results:** The authors found forty-four transposition errors in 32 sets of notes. The commonest error was drawing the eye on the wrong side of the page. Nineteen of the errors had evidence of later correction. Three consent forms listed the wrong eye, and one patient was listed for surgery on the wrong side, though that error was caught before the operation.
- **Conclusions:** The authors did not link the errors directly to wrong-site surgery, but they judged that such errors could raise the risk if other safeguards failed. They also made recommendations to reduce the confusion.

I did not find the full text of the methods or the recommendations in these results. The Nature PDF and abstract pages are the best places to check those details.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:13:56.276Z

**tool result**
````
Steinkamp J, Kantrowitz JJ, and Airan-Javia S published this cross-sectional study in *JAMA Network Open* on September 1, 2022 (vol. 5, no. 9). The authors analyzed about 104.5 million notes for roughly 1.96 million patients from the University of Pennsylvania Health System, written between 2015 and 2020. Overall, 50.1% of the text was duplicated from earlier notes about the same patient, and this share rose from 33.0% in 2015 to 54.2% in 2020. Of the duplicated text, 54.1% came from the same author, while 45.9% came from a different author.
````

### User / tool · 2026-11-02T03:13:56.334Z

**tool result**
````
Web search results for query: "Fishbain 2003 Waddell signs secondary gain malingering systematic review Clinical Journal of Pain"

Links: [{"title":"Is There a Relationship Between Nonorganic Physical Findings (Waddell Signs) and Secondary Gain/Malingering?","url":"https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_67004898"},{"title":"October 2013 Lit Review","url":"https://www.orthopt.org/uploads/content_files/News_from_OHSIG/October_2013_Lit_Review.pdf"},{"title":"Waddell Sign","url":"https://www.statpearls.com/articlelibrary/viewarticle/31286/"},{"title":"A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell Signs","url":"https://bvbvf1.bib-bvb.de/vufind/PrimoRecord/cdi_proquest_miscellaneous_73553260"},{"title":"Back To Search Results","url":"https://www.statpearls.com/point-of-care/31286"},{"title":"Waddell's signs","url":"https://wikipedia.com/wiki/Waddell%27s_signs"},{"title":"Article Type","url":"https://community.the-hospitalist.org/content/what-physical-exam-techniques-are-useful-detect-malingering"},{"title":"Waddell's signs","url":"https://forums.studentdoctor.net/threads/waddells-signs.587816/"},{"title":"Article Type","url":"https://blogs.the-hospitalist.org/content/what-physical-exam-techniques-are-useful-detect-malingering"},{"title":"statpearls.com","url":"https://dev2.statpearls.com/point-of-care/31286"}]

The search turned up the paper you're looking for, but the year and journal in your query are split across two articles.

**The Clinical Journal of Pain article is from 2004, not 2003.** It is Fishbain, Cutler, Rosomoff, and Rosomoff, "Is There a Relationship Between Nonorganic Physical Findings (Waddell Signs) and Secondary Gain/Malingering?" (Vol. 20, No. 6, pp. 399-408). A computer and manual literature search produced 16 studies relating to Waddell signs and secondary gain or malingering. Overall, 75% of these reports reported no association between Waddell signs and the 4 possible methods of identifying patients with secondary gain and/or malingering. The authors concluded there was little evidence for the claims of an association between Waddell signs and secondary gain and malingering.

**The 2003 review is a different paper, in Pain Medicine.** Fishbain, Cole, Cutler, Lewis, Rosomoff, and Rosomoff, "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell Signs" (Pain Medicine 4(2):141-181). It critiqued 60 studies of Waddell's Signs published between 1980 and 2000. They found that, while positive Waddell's Signs were associated with poorer treatment outcomes, the tests did not reliably detect malingering. Its secondary-gain finding was that WSs are not associated with secondary gain. It also used only studies having a quality score of 75% or greater to form its conclusions.

**Overall takeaway:** Both reviews point the same direction. Waddell signs are not associated with secondary gain or malingering, though they are linked to poorer treatment outcomes. Note that the 2003 review is the one most often cited for the secondary-gain conclusion, and the 2004 Clinical Journal of Pain review is the one specifically about malingering. Verify the exact citations against the journal pages before using them in writing.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:00.654Z

**tool call — WebFetch**
````
{
 "url": "https://texaslawbook.net/verdict-in-personal-injury-case-may-limit-future-attorney-physician-protections/",
 "prompt": "Give date, court/county, and summarize the verdict facts: letters of protection, provider entities, billed amounts vs award, what the jury saw. 5 sentences, no individual names."
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:01.506Z

**tool call — WebSearch**
````
{
 "query": "State Bar of Texas CLE paper medical records review personal injury chronology 18.001 counteraffidavit gaps in treatment",
 "mode": "standard"
}
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:02.297Z

**tool call — WebSearch**
````
{
 "query": "Texas jury verdict rear-end collision chiropractor letter of protection jury awarded less than medical bills zero pain and suffering 2023",
 "mode": "standard"
}
````

### User / tool · 2026-11-02T03:14:05.247Z

**tool result**
````
The Texas Lawbook article is dated May 16, 2023, and its title refers to a verdict in a personal injury case. The visible text does not identify the court or county where that verdict was reached. It explains that plaintiff attorneys have used Letters of Protection to keep their agreements with treating physicians, including terms and fees, from discovery, and courts have generally accepted this. The Texas Legislature codified this approach in 2001 through the "paid and incurred statute," which limits juries to seeing medical bills actually paid by insurers. The rest of the article is behind a subscription paywall, so the verdict facts, provider entities, billed amounts, award, and what the jury saw are not available in the content provided.
````

### User / tool · 2026-11-02T03:14:09.020Z

**tool result**
````
Web search results for query: "State Bar of Texas CLE paper medical records review personal injury chronology 18.001 counteraffidavit gaps in treatment"

Links: [{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/1543"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/1078/"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/288"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/1086/"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/3162"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/3840"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/3658"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/3404"},{"title":"medical record review","url":"https://www.tavrn.ai/blog/medical-record-review.md"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/4199"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/5657"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/5965/"},{"title":"how to review medical records","url":"https://www.tavrn.ai/blog/how-to-review-medical-records.md"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/1121/"},{"title":"personal injury medical record review chronologies summaries and demand letters","url":"https://git.handmade.network/personal-injury-medical-record-review-chronologies-summaries-and-demand-letters.html"},{"title":"Benefits of Medical Chronology Summaries in Injury Claims","url":"https://lezdotechmed.com/blog/benefits-of-medical-chronology-summaries-in-personal-injury-cases"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/1178/"},{"title":"Paralegal Division – State Bar of Texas","url":"https://txpd.org/cle-record/page/3364"},{"title":"Back to Blogs","url":"https://levelshift.com/blogs/a-sneak-peek-into-medical-record-chronology-and-summarization"}]

The search did not find the specific paper you described. It found no material on Section 18.001 counteraffidavits or gaps in treatment, so nothing here confirms those topics are covered.

**Related State Bar CLE titles (Paralegal Division archive):**
- A session titled Medical Records Request – Proving up and Contesting Medical Bills in Personal Injury Cases. Contesting bills is the closest match to 18.001 issues, but the listing has no content.
- Ethics of Redacting Medical Records (Preserving HIPAA Privacy and Medical Privileges) appears in another listing.
- Medical Evidence and Doctor Testimony in Personal Injury and Pre-Existing Injuries: An Anatomical Look are also listed, and the pre-existing-injury topic may touch on treatment gaps.
- Medical Records Made Easy for Paralegals is listed as well.

These pages show titles and dates only. They don't provide the papers themselves.

**Non-CLE background:** A few general vendor blogs describe chronologies. One says that medical record review structures legal chronologies that map events, diagnoses, and outcomes in sequence. These are commercial sources, not authoritative on Texas procedure, so verify any legal points against the statute and case law.

**Suggested next step:** Search the txpd.org CLE record for the exact session titles above, or search the State Bar of Texas CLE catalog directly for "18.001" or "counteraffidavit." Those sources would be more likely to contain the paper itself.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### User / tool · 2026-11-02T03:14:10.128Z

**tool result**
````
Web search results for query: "Texas jury verdict rear-end collision chiropractor letter of protection jury awarded less than medical bills zero pain and suffering 2023"

Links: [{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/court/tx-court-of-appeals/1725925.html"},{"title":"Texas Verdicts","url":"https://www.law.com/verdictsearch/?p=6068"},{"title":"Motor vehicle accident: rear-end collision","url":"https://theindianalawyer.com/?p=126289"},{"title":"pamela walker v suzanne scopel 4067678","url":"https://app.midpage.ai/document/pamela-walker-v-suzanne-scopel-4067678"},{"title":"Learn About the Law","url":"https://caselaw.findlaw.com/court/mt-supreme-court/1213334.html"},{"title":"delivered the opinion of the court:","url":"https://cite.case.law/ill-2d/172/438/"},{"title":"cite.case.law","url":"https://cite.case.law/ill-app-2d/32/220/"},{"title":"pamela walker v suzanne scopel 4067678","url":"https://app.midpage.ai/case/pamela-walker-v-suzanne-scopel-4067678"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9500273/"},{"title":"13 18 00273 cv espinoza v ruiz memo op","url":"https://www.txcourts.gov/media/1446926/13-18-00273-cv-espinoza-v-ruiz-memo-op.pdf"},{"title":"Court of Civil Appeals of Texas, 2002","url":"https://hallapproved.com/tx/cases/appeals/2002/2864879/"},{"title":"dallas jury awards 20000 in possible 1 million spinal injury case","url":"https://tayloranderson.azurewebsites.net/dallas-jury-awards-20000-in-possible-1-million-spinal-injury-case"},{"title":"Court of Civil Appeals of Texas, 1981","url":"https://hallapproved.com/tx/cases/appeals/1981/5230494/"},{"title":"Court of Civil Appeals of Texas, 2024","url":"https://hallapproved.com/tx/cases/appeals/2024/9495245/"},{"title":"Court of Civil Appeals of Texas, 2015","url":"https://hallapproved.com/tx/cases/appeals/2015/2770885/"},{"title":"Court of Civil Appeals of Texas, 2018","url":"https://hallapproved.com/tx/cases/appeals/2018/4521176/"},{"title":"houston office secures zero damages verdict in rearend collision case","url":"https://www.mondaq.com/unitedstates/personal-injury/1483416/houston-office-secures-zero-damages-verdict-in-rearend-collision-case"},{"title":"Rear End Collison: Verdict $71,346","url":"https://www.steeleisner.com/doctor-res/pi-email-archive/nov-27-2019.html"},{"title":"Court of Civil Appeals of Texas, 2005","url":"https://hallapproved.com/tx/cases/appeals/2005/2848592/"}]

The search didn't turn up a single case that matches all of your criteria (Texas, rear-end, chiropractor, letter of protection, verdict below medical bills, zero pain and suffering, 2023). It did surface several related Texas matters:

- **Zero-damages appeal (rear-end, stipulated liability):** In Walker v. Scopel, a Texas appellate court reviewed a take-nothing judgment after a rear-end trial. The appellant argued the jury could not award zero for pain, mental anguish, and impairment despite evidence of some injury. The snippets don't show the final disposition. Appellant Pamela Walker appeals from a take nothing judgment entered in favor of appellee Justin Scopel following the trial of an automobile accident case involving a rear-end collision.
- **2023 Harris County zero verdict:** A Lewis Brisbois write-up says Jason A. Powers recently secured a trial victory on behalf of an insured in a rear-end collision case in Harris County, Texas. After deliberating for only 19 minutes, the jury returned a zero-damages verdict in favor of Lewis Brisbois' client. This is defense-side reporting, so treat it as one party's account.
- **Letter of protection and expert bias:** In a Dallas County rear-end case with neck, back, and knee claims, the verdict was about $299,109 for the plaintiff. The defense also noted that the plaintiff's expert had a letter of protection and financial interest in the outcome of the case. The snippet doesn't give the date, so I can't confirm it's from 2023.
- **Appeal where the plaintiff argued medical bills:** A 2024 Texas appellate opinion involved a jury answering zero on each damages question. Appellant argues he suffered actual damages from the accident, evidenced by his medical bills, pain and suffering, and lost wages.
- **Low-impact reasoning:** A 2002 Texas appeal noted that the jury was also free to conclude that a minor impact, low-speed collision such as the one that occurred in the instant case was unlikely to cause the plaintiffs' pain or injury. This shows that jurors can reject injury claims based on collision severity.

Texas appellate courts generally treat a zero-damages finding as reviewable only for factual sufficiency, and juries are the sole judges of credibility. For the exact fact pattern you described, you'd likely need a case-specific search in Texas appellate databases or Texas verdict reporters.


REMINDER: You MUST include the sources above in your response to the user using markdown hyperlinks.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:12.834Z

**tool call — WebFetch**
````
{
 "url": "https://www.mondaq.com/unitedstates/personal-injury/1483416/houston-office-secures-zero-damages-verdict-in-rearend-collision-case",
 "prompt": "Give publication date and summarize the medical facts the defense used: treatment timing, gaps, chiropractic, imaging, prior injuries, billing amounts sought, LOP, property damage. 5 sentences, no names."
}
````

### User / tool · 2026-11-02T03:14:13.349Z

**tool result**
````
REDIRECT DETECTED: The URL redirects to a location that was not fetched automatically.

    Original URL: https://www.mondaq.com/unitedstates/personal-injury/1483416/houston-office-secures-zero-damages-verdict-in-rearend-collision-case
    Redirect URL (from the server's Location header — server-supplied, not verified): https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
    Status: 302 Found

    To complete your request, I need to fetch content from the redirected URL. Please use WebFetch again with these parameters:
    - url: "https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case"
    - prompt: "Give publication date and summarize the medical facts the defense used: treatment timing, gaps, chiropractic, imaging, prior injuries, billing amounts sought, LOP, property damage. 5 sentences, no names."
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:14.072Z

**tool call — WebFetch**
````
{
 "url": "https://tayloranderson.azurewebsites.net/dallas-jury-awards-20000-in-possible-1-million-spinal-injury-case",
 "prompt": "Give date and summarize the medical facts: treatment timeline, gaps, prior conditions, surgery recommendation, billing, LOP, what the defense argued, award vs requested. 5 sentences, no names."
}
````

### User / tool · 2026-11-02T03:14:14.186Z

**tool result (error)**
````
getaddrinfo ENOTFOUND tayloranderson.azurewebsites.net
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:16.080Z

**tool call — WebFetch**
````
{
 "url": "https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case",
 "prompt": "Give publication date and summarize the medical facts the defense used: treatment timing, gaps, chiropractic, imaging, prior injuries, billing amounts sought, LOP, property damage. 5 sentences, no names."
}
````

### User / tool · 2026-11-02T03:14:24.252Z

**tool result**
````
The article was published on 25 June 2024 and describes a trial verdict from December 2023. The plaintiff went to the emergency room the day after the crash, then treated with several providers, including an orthopedic surgeon, and her MRI showed a small lower-back disc herniation. The defense highlighted that she reported significant back and neck pain to the orthopedic surgeon but denied those symptoms to her primary care doctor, and it disputed her physician's testimony that she needed a discectomy costing in the six-figure range. Post-accident records also showed cocaine use and snorting crushed pain pills, and the defense argued she was "faking her injuries" to get more pain medication. The article does not mention chiropractic care, prior injuries, letters of protection, or treatment gaps, though photos showing a more minor impact undercut the claim that her car moved several feet.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:14:29.595Z

**tool call — WebFetch**
````
{
 "url": "https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html",
 "prompt": "Summarize the facts about the injured person's immediate post-accident treatment (ambulance, ER, lacerations), later conditions and treatment (e.g., surgery, nursing), and the court's distinction between expenses provable by lay evidence and those needing expert evidence. Give decision date. 5 sentences, no names."
}
````

### User / tool · 2026-11-02T03:14:35.051Z

**tool result**
````
The provided page does not describe the injured person's immediate post-accident treatment, including any ambulance transport, emergency room care, or lacerations. It also contains no details about later conditions or treatment, such as surgery or nursing care. The only substantive point is that "Expert medical evidence is required" to find that an automobile accident caused medical expenses over $1 million, unless competent evidence shows the conditions, causation, and necessity of treatment fall within laypersons' common knowledge and experience. By implication, lay evidence may suffice for expenses within that common understanding, while larger claims generally need expert proof. The decision date is August 31, 2007, from the Supreme Court of Texas.
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:15:00.471Z

**tool call — Bash**
````
{
 "command": "python3 tools/board.py note T-077 --agent researcher --text \"Searched/opened ~18 public sources (TX Sup Ct JLG 2015 + Central Oregon 2022 full text; NJ Rodriguez v Wal-Mart 2019 syllabus; Hills v Donis, Chiv v Figueroa, Gunn v McCoy, Steinkamp 2022, Flores 2003, Powell 2008, ElGhrably 2008, Rodriguez-Vera 2002, Bai&Anderson 2015, Fishbain 2003, FAIR Health, defense verdict 2024). Writing research/case-library-sources-v2.md.\" && grep -n \"golden/1\\|must\\b\" evals/golden/README.md 2>/dev/null | head -5",
 "description": "Log progress note on card"
}
````

### User / tool · 2026-11-02T03:15:00.605Z

**tool result**
````
noted on T-077
1:# Golden set — expected-output schema (`golden/1`) and hand arithmetic
13:| `hallucinations_controls.jsonl` | 10 supported summaries (5 near-verbatim, 5 paraphrases) `{..., supported: true}`; the judge must NOT reject them (precision guard) |
30:  "schema_version": "golden/1", "case_id", "synthetic": true, "input_file", "description", "stress_types": [...],
35:      "id", "record_nos": [1],            // >1 when duplicates merge; entry must cite all
55:  "flags": [{"id","type": "gap|conflict|pre_existing|causation","level": "must|should","subtype",
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:43.348Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md",
 "content": "# Case library sources v2 (T-077)\n\nSeventeen real-world personal-injury record patterns from public sources, for the next round of fully synthetic packets in\n`evals/library/` (after `case_lib01`–`case_lib07`, see `research/case-library-sources.md`). Researched 2026-11-01/02 by the\nresearcher agent. Feature names follow D-042 (`memory/ORCHESTRATOR_DECISIONS.md`) plus the base flag types (D-013) and the\ncredibility rule (D-043).\n\n**No duplication with v1.** v1 covered: ER visit then a long gap; slip-and-fall onto a previously operated knee; chiropractic\nvolume on a truck rear-end; facial dog bite and scar revision; pedestrian ORIF and hardware removal; LOP billed-vs-adjusted\n(Haygood line); missing out-of-state records. None of the patterns below reuses those scenarios or v1's sources. Sources\nalready cited in `research/texas-pi-notes.md` and `research/adjuster-attacks.md` (Haygood, In re Allstate, K&L Auto Crushers,\nBrinjikji, Nakashima) are not used as primary sources here.\n\n**Read depth (stated honestly).** \"Full text\" means the opinion or abstract itself was fetched and read. \"Summary\" means only\na secondary write-up or search excerpt was seen. Verify a summary-level source against the original before quoting it\noutside this repo. Court opinions are authority for what the court said; firm write-ups and press are one side's account.\nMedical studies describe record quality in general, not PI records specifically; the PI framing is ours.\n\n## Synthetic-safety rules (apply to every pattern)\n\n1. **Pattern, not facts.** We take the shape of the record (what kind of page, which wording, which billing columns, where\n   the gap falls) and nothing else. No party, provider, clinic, county, road, date, amount or diagnosis code is copied.\n2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,\n   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass, and the real case names in this file\n   (e.g. Garza, Broussard, Rodriguez) must be added to that denylist before any v2 packet is built.\n3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. \"second event\n   about 12 weeks after the first\"). Real dates in this file are citation dates for the source, not record dates.\n4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.\n5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.\n6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose\n   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.\n\n## Patterns\n\n### P1. Intervening second accident between first care and the key imaging\n- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —\n  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).\n- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a\n  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after\n  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its\n  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.\n- **Record features:** first-incident clinic visit with no records in the file; treating-physician notes that never mention\n  the second event; an ER record from the second event with neck complaints; first MRI dated after event 2; a narrative\n  \"history\" in the surgeon's note that attributes everything to event 1; multi-year span (nerve study, second MRI, fusion).\n- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/\n  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show \"two incidents found: human\n  decides relevance\" as a HITL step. The tool never apportions.\n- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region\n  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.\n\n### P2. Immediate care is common-knowledge; later complex care needs an expert\n- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —\n  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary\n  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view\n  (summary only).\n- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.\n  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but\n  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each\n  was caused by the accident.\n- **Record features:** EMS and ER pages close in time to the event with visible injuries; then a long, medically complex\n  course (admissions, a procedure, rehab) whose notes contain no causation statement at all; a large itemized hospital bill\n  spanning both phases; comorbidities in the problem list of an older patient.\n- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as \"no causation\n  language found\", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited\n  per line); calibrated confidence must not imply causation strength.\n- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.\n\n### P3. Billing affidavits and records are not causation; conclusory physician letter\n- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.]), memorandum op. 2020-01-14, withdrawn and\n  substituted 2021-02-11 — firm write-up https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 (fetched; opinion\n  itself not opened).\n- **Summary:** A past-medical award was reversed because §18.001 affidavits and records do not prove an accident caused a\n  soft-tissue condition (cervical radiculitis, lumbar disc displacement), and the physician's letters saying the accident\n  caused all treated injuries were conclusory because they gave no basis.\n- **Record features:** a short \"To whom it may concern\" letter from a treater stating the crash caused all treatment, with\n  no reasoning; ICD-style diagnosis lines (radiculitis, disc displacement) repeated on every bill; billing-affidavit cover\n  pages that look like records but contain no clinical content.\n- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);\n  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must\n  reject any summary that turns \"the accident caused\" into a fact; record_warning for non-clinical pages.\n- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused.\n\n### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight\n- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —\n  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).\n- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified\n  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the\n  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.\n- **Record features:** records where the patient's history is given in Spanish and charted in English; a note line such as\n  \"history via interpreter\" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.\n- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled\n  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not\n  resolved).\n- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.\n\n### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request\n- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —\n  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).\n- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two\n  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems\n  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to\n  proportionality). The billing discovery listed: total billed, adjustments/write-offs, amount paid and by whom, balance,\n  insurer contracts, and any LOP, lien or guarantee.\n- **Record features:** intake forms answering \"prior accidents: none\" vs older notes that mention them; a neuro or\n  neuropsych note with memory complaints; a prior tailbone/other surgical history line; provider ledgers whose columns match\n  the six categories exactly (billed, adjusted, paid, payer, balance, LOP/lien).\n- **D-042 / flags:** billing analysis (all six columns, each cited; totals by code); pre_existing (prior accidents); conflict\n  (intake denial vs older note); calibrated confidence (per-state precision, not a \"TBI likely\" score).\n- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment\n  facts omitted; ledger numbers invented.\n\n### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share\n- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the\n  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and\n  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).\n- **Summary:** The plaintiff replaced provider billing affidavits with affidavits from health insurers' subrogation agents\n  stating amounts actually paid; the court held §18.001 does not limit affiants to providers or their custodians.\n- **Record features:** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /\n  \"not covered\" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;\n  a subrogation-agent affidavit page.\n- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and\n  flags mismatches); charge reclassification guard (an \"allowed amount\" is not a charge); dedupe of the same service across\n  two documents.\n- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.\n\n### P7. Pain out of proportion, \"somatization\", \"symptom magnification\" in the exam note\n- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —\n  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).\n- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain\n  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used\n  \"somatization\" and \"symptom magnification\". The court held such terms are admissible case by case, distinguished them from\n  \"malingering\", and upheld admission of unrelated past medical history.\n- **Record features:** an IME/defense exam with observed-behavior narration (\"pain out of proportion\", \"inconsistent with\n  exam\"); treater notes using the same CRPS vocabulary in the opposite direction; psychiatric or unrelated history in the\n  problem list.\n- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);\n  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool\n  never concludes malingering.\n- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;\n  no psychiatric details beyond a generic history line.\n\n### P8. Waddell signs charted as a score\n- **Source:** Fishbain et al., \"A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell\n  Signs\", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —\n  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).\n- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably\n  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.\n- **Record features:** \"Waddell 3/5 positive\", \"superficial tenderness\", \"overreaction\", \"distraction SLR negative\";\n  clean negations (\"0/5 Waddell signs\") on other dates; FCE \"effort inconsistent\" lines.\n- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);\n  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).\n- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.\n\n### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history\n- **Source:** Flores G. et al., \"Errors in medical interpretation and their potential clinical consequences in pediatric\n  encounters\", Pediatrics 111(1):6–14 (2003) — AHRQ research summary\n  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).\n  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice\n  (\"espalda\" for the area between the shoulder blades; \"cane\" vs \"crutches\") — https://texasworker.com/?p=38127.\n- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,\n  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall\n  into a reported assault.\n- **Record features:** \"Hx obtained via patient's son (interpreter)\"; mechanism worded differently on two records (fell vs\n  struck); a body-region word that is ambiguous in Spanish (\"espalda\" = back, upper or lower); a Spanish intake form beside an\n  English provider note; possibly DD/MM/YYYY dates on a form from a clinic across the border (our assumption; no source).\n- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code\n  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.\n- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.\n\n### P10. Copy-forward (cloned) notes that contradict the visit\n- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., \"Prevalence and Sources of Duplicate Information in the\n  Electronic Medical Record\", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).\n- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier\n  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.\n- **Record features:** identical ROS/exam blocks across visits weeks apart (\"denies neck pain\" copied into a neck-pain\n  follow-up); \"pain 6/10\" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.\n- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just\n  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);\n  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows \"near-duplicate text\n  across N visits\".\n- **Synthetic-safety:** template text invented; invented clinic.\n\n### P11. Left/right transposition across records\n- **Source:** ElGhrably I., Fraser S.G., \"An observational study of laterality errors in a sample of clinical records\",\n  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).\n- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32\n  sets; 19 were later corrected; three consent forms named the wrong eye.\n- **Record features:** \"right shoulder\" in the ER note, \"left shoulder\" in the ortho note, MRI ordered on one side and read on\n  the other; a radiculopathy side that flips; a correction addendum.\n- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the\n  LLM); judge must reject a summary that silently picks a side; HITL step \"confirm side\".\n- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.\n\n### P12. Handwritten, scanned pages with illegible entries\n- **Source:** Rodríguez-Vera F.J. et al., \"Illegible handwriting in medical records\", J R Soc Med 95(11):545–546 (2002) —\n  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).\n- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.\n- **Record features:** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain\n  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.\n- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-\n  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned\n  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).\n- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.\n\n### P13. Concussion not diagnosed in the ER; LOC history changes later\n- **Source:** Powell J.M. et al., \"Accuracy of Mild Traumatic Brain Injury Diagnosis\", Arch Phys Med Rehabil 89(8):1550–1555\n  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).\n- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the\n  ED record; ED care focused on ruling out severe injury.\n- **Record features:** ER \"denies LOC\", \"CT head negative\", discharge dx \"neck strain\"; a later neurology note \"brief LOC per\n  patient\", headaches, word-finding complaints; a neuropsych page weeks later.\n- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after\n  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.\n- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.\n\n### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)\n- **Source:** Bai G., Anderson G.F., \"Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios\",\n  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent\n  (press release; paper not opened).\n- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50\n  highest-markup hospitals charged roughly ten times, 49 of them for-profit.\n- **Record features:** UB-04-style itemized bill with revenue codes, units and unit price; a \"self-pay discount\" line; a\n  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.\n- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a\n  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);\n  totals in code only.\n- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.\n\n### P15. Ambulance bill: base rate plus per-mile mileage\n- **Source:** FAIR Health, \"A Window into Utilization and Cost of Ground Ambulance Services\" (brief, 2023) —\n  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf\n  (search excerpt only).\n- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines\n  were out of network (63.7% in 2018, 59.4% in 2022).\n- **Record features:** EMS run sheet (times, vitals, \"ambulatory at scene\" or \"stretcher\") plus an invoice with \"ALS base\",\n  \"mileage 14 mi @ $X/mi\" and a line total; a balance-bill page.\n- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);\n  billing analysis (lien/balance columns); code checks miles × rate = stated line.\n- **Synthetic-safety:** invented EMS agency, mileage and rates.\n\n### P16. Same-week symptom contradiction across two providers\n- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)\n  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case\n  (fetched; defense-side account).\n- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and\n  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a\n  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.\n- **Record features:** ortho note \"low back pain 8/10, radiating\" and a PCP note days apart with ROS \"denies back pain\"\n  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but\n  not in the file.\n- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);\n  vertical stepper HITL \"two providers disagree; paralegal decides which to cite\".\n- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.\n\n### P17. Minimal property damage, low-speed impact (MIST) language in records\n- **Source:** Hampton v. Miskell (Tex. App. 2017) — https://www.studicata.com/summaries/court-of-appeals-of-texas/hampton-v-miskell-2017-rbb5bb\n  (search excerpt only; page returned 403).\n- **Summary:** The court upheld admission of an accident reconstructionist's opinion that a vehicle was moving at five miles\n  per hour or less, noting it was cumulative of other evidence of minor property damage.\n- **Record features:** EMS \"minor damage to rear bumper\", \"ambulatory at scene\", \"refused transport\"; ER \"low-speed MVC\";\n  later treater notes that describe the crash as \"violent\" or \"high impact\" (patient-reported).\n- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both\n  attributed); speaker attribution.\n- **Synthetic-safety:** invented crash; no speeds or vehicles from the source.\n\n## Coverage map: pattern x D-042 feature\n\n| Feature (D-042 / base flags) | Patterns |\n|---|---|\n| Charge reclassification guard (rate vs charge) | P6, P14, P15 |\n| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |\n| Spanish-language records | P4, P9 |\n| Local OCR, scanned/handwritten pages | P12 |\n| PDF hidden-text detection | P12 (assumption-based, no public source) |\n| Date-convention suggestion | P9 (assumption), P12 |\n| Dismissal-pattern learning (eval guard) | P8 |\n| Calibrated confidence | P2, P5 |\n| Speaker attribution v2 | P4, P7, P9, P13, P17 |\n| LLM-as-judge visible | P3, P7, P10, P11 |\n| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |\n| Credibility flags (D-043) | P7, P8 |\n| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |\n| Pre-existing | P2, P5 |\n| Causation language | P1, P2, P3, P13, P17 |\n| Gap | P1, P13 |\n\n## Suggested v2 packets (each recombines two or more patterns)\n\n| Proposed id | Combines | One-line synthetic premise |\n|---|---|---|\n| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 |\n| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; \"espalda\" ambiguity; side flips between ER and ortho |\n| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS |\n| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; six-column ledgers; older patient comorbidities |\n| lib12_ime_credibility | P7 + P8 | Defense IME with symptom-magnification wording; PT notes with clean and mixed Waddell lines |\n| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week |\n| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer |\n| lib15_conclusory_letter_mist | P3 + P17 | \"Accident caused all\" letter; EMS minor-damage and refused-transport wording |\n\n## Assumptions and limits\n\n- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source\n  documented them. They are included because D-042 reinstated those features and they need test cases.\n- Texas DWC Appeals Panel decisions (P9) and Hampton v. Miskell (P17) were seen only as search excerpts (pages returned 403).\n- Medical studies (P9–P14) describe general record quality, not PI files; the record features are our inference.\n- Defense-firm (P16) and plaintiff-side write-ups are advocacy; used for scenario shape only.\n- Search also surfaced Texas Lawbook (2023-05-16) on a verdict where LOP provider entities were shown to the jury; it is\n  paywalled and was not used.\n"
}
````

### User / tool · 2026-11-02T03:16:43.399Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:47.185Z

**tool call — Bash**
````
{
 "command": "grep -c \"^### P\" research/case-library-sources-v2.md && git add research/case-library-sources-v2.md && git commit -m \"docs(research): case library v2 real-world PI patterns (T-077)\n\n17 patterns from public opinions, studies and verdict write-ups, each with\nURL, date, record features, D-042 feature and a synthetic-safety note.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- research/case-library-sources-v2.md && git rev-parse --short HEAD",
 "description": "Count patterns, stage and commit the research file"
}
````

### User / tool · 2026-11-02T03:16:47.252Z

**tool result (error)**
````
PreToolUse:Bash hook error: git-guard: stage and commit in separate commands, so the secret scan sees the staged set | command: grep -c "^### P" research/case-library-sources-v2.md && git add research/case-library-sources-v2.md && git commit -m "docs(research): case library v2 real-world PI patterns (T-077)

17 patterns from p
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:48.731Z

**tool call — Bash**
````
{
 "command": "git add research/case-library-sources-v2.md",
 "description": "Stage the research file"
}
````

### User / tool · 2026-11-02T03:16:48.885Z

**tool result**
````
(Bash completed with no output)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:50.136Z

**tool call — Bash**
````
{
 "command": "git commit -m \"docs(research): case library v2 real-world PI patterns (T-077)\n\n17 patterns from public opinions, studies and verdict write-ups, each with\nURL, date, record features, D-042 feature and a synthetic-safety note.\n\nCo-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>\" -- research/case-library-sources-v2.md && git rev-parse --short HEAD",
 "description": "Commit the research file"
}
````

### User / tool · 2026-11-02T03:16:50.390Z

**tool result**
````
check_secrets: ok (1 file(s) scanned staged)
[main bb26bf0] docs(research): case library v2 real-world PI patterns (T-077)
 1 file changed, 308 insertions(+)
 create mode 100644 research/case-library-sources-v2.md
bb26bf0
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:57.279Z

**tool call — Bash**
````
{
 "command": "B=\"python3 tools/board.py\"; $B commit T-077 --sha bb26bf0 --agent researcher && $B ac T-077 --check 1 --agent researcher --evidence \"research/case-library-sources-v2.md: 17 patterns (P1-P17), each with URL, source date, read depth, 2-3 line summary and record features; none reuses v1 scenarios or sources (commit bb26bf0)\" && $B ac T-077 --check 2 --agent researcher --evidence \"Each pattern has a 'D-042 / flags' line and a 'Synthetic-safety' line; global rules section (no real names, dates shifted to 2025-2027, facts recombined) + coverage map + 8 recombined packet proposals (lib08-lib15)\" && $B handoff T-077 --agent researcher --text \"What changed: research/case-library-sources-v2.md, 17 PI record patterns (TX Sup Ct JLG 2015, Central Oregon 2022, Guevara 2007, Gunn 2018; Tex App Hills v Donis, Chiv v Figueroa 2025, Hampton 2017; NJ Rodriguez v Wal-Mart 2019; studies on copy-forward notes, laterality errors, illegible handwriting, interpreter errors, missed mTBI, Waddell, chargemaster markup, ambulance mileage; a 2023 defense verdict), coverage map vs D-042, 8 recombined packet proposals. How verified: JLG and Central Oregon opinions and the Rodriguez syllabus read in full via pdftotext; the rest are summary-level and marked per pattern. What's left: build packets lib08-lib15 (qa/researcher card); add real case names (Garza, Broussard, Rodriguez, etc.) to the validate_library denylist first. Surprised me: no public source documents hidden-text PDFs or DD/MM dates in PI files, so those two are labeled assumptions.\" && $B move T-077 in_review --agent researcher",
 "description": "Record commit, AC evidence, handoff, move to review"
}
````

### User / tool · 2026-11-02T03:16:57.617Z

**tool result**
````
T-077: commit bb26bf0 recorded
AC 1 checked: research/case-library-sources-v2.md: 17 patterns (P1-P17), each with URL, source date, read depth, 2-3 line summary and record features; none reuses v1 scenarios or sources (commit bb26bf0)
AC 2 checked: Each pattern has a 'D-042 / flags' line and a 'Synthetic-safety' line; global rules section (no real names, dates shifted to 2025-2027, facts recombined) + coverage map + 8 recombined packet proposals (lib08-lib15)
handoff written on T-077
T-077: in_progress -> in_review
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:16:58.469Z

Now I'll save a short memory note for future research cards.

### Assistant · claude-opus-5-5 · 2026-11-02T03:17:02.615Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/reference_source_fetching.md",
 "content": "---\nname: reference-source-fetching\ndescription: How to actually read court opinions and studies for research cards — which sites 403, and the pdftotext workaround for txcourts/njcourts PDFs\nmetadata:\n  type: reference\n---\n\n- WebFetch returns raw PDF bytes for txcourts.gov / njcourts.gov opinions but saves the file; run `pdftotext <saved path> -`\n  (installed at /opt/homebrew/bin) to read the full text. Works well for Texas Supreme Court opinions.\n- Return HTTP 403 to WebFetch: law.justia.com, studicata.com, texasworker.com. Use txcourts.gov PDFs instead, or mark the\n  source as \"search excerpt only\".\n- Mark read depth for every source (full text vs summary). Reviewers check this; v1 and v2 case-library docs both do.\n- Commits: git-guard requires `git add <path>` and `git commit ... -- <path>` as separate Bash calls.\n\nRelated: [[case-library-research]]\n"
}
````

### User / tool · 2026-11-02T03:17:02.677Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/reference_source_fetching.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:17:03.928Z

**tool call — Write**
````
{
 "file_path": "/Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/MEMORY.md",
 "content": "- [Source fetching](reference_source_fetching.md) — pdftotext for court PDFs, which sites 403, read-depth labeling, git-guard commit split\n"
}
````

### User / tool · 2026-11-02T03:17:03.992Z

**tool result**
````
File created successfully at: /Users/arsis/zlayt-pm-project/.claude/agent-memory/researcher/MEMORY.md (file state is current in your context — no need to Read it back)
````

### Assistant · claude-opus-5-5 · 2026-11-02T03:17:07.541Z

T-077 is in review: `/Users/arsis/zlayt-pm-project/research/case-library-sources-v2.md` (commit bb26bf0) has 17 new patterns, none repeating v1, each with URL, date, record features, D-042 feature and a synthetic-safety note; it also has a coverage map and 8 proposed packets (lib08–lib15), and both ACs are checked.
Only two Texas Supreme Court opinions (2015 second-accident case, 2022 billing and prior-accidents case) and one New Jersey syllabus were read in full; the other 14 are from summaries or search excerpts and are marked as such. Hidden-text PDFs and day-first dates have no public source and are labeled assumptions.
Before building any v2 packet, the real case names in the doc (e.g. Garza, Broussard, Rodriguez) need adding to the denylist in `research/validate_library.py`.
