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
defense uses this kind of evidence to say a C5-C6 protrusion in a 41-year-old may be pre-existing; the plaintiff uses record 7 ("New onset pain radiating to right arm with numbness in fingers")
to argue aggravation. The record itself is equivocal — so the product must keep it
equivocal (Appendix C: never convert "may represent degenerative change" to "degenerative" or "traumatic").
Radiology literature treats "clinical correlation" and "cannot be excluded" as hedges that shift
interpretation to the clinician (src 7, 8). In Texas, causation testimony must reach *reasonable medical
probability*; possibility language does not (Jelinek v. Casas, src 11, secondary).

**A6 Patient self-report.** In Texas, lay testimony can prove causation only for conditions within common
knowledge; otherwise expert testimony is required (Guevara v. Ferrer, src 9). A PM-clinic note that the
"patient states symptoms began after the January collision" records history, not a physician's causation
opinion. The export may quote it but must attribute it ("patient states"), never restate it as fact.

**A7 Inconsistent dates.** Defense impeaches with the claimant's own intake forms (Georgia appeal, src 17);
a treating physician's causation opinion is only as good as the history the patient gave. In
JLG Trucking v. Garza (Tex. 2015) evidence of a *second* accident was relevant to causation and its exclusion
was reversible error (src 10) — a second accident date in the records is exactly what defense counsel looks for.
The tool must surface both dates and must not "fix" 2026-01-19 to 2026-01-09.

**A12 Delay to first treatment.** The insurer-side checklist asks "How soon did treatment start?" before it asks
about gaps (src 1). In the Virginia record-review case the defense relied on a report made "eight days later"
(src 16). Rivera's EMS run report (rec 1, "Transported to Central ER.") and ER discharge summary (rec 2) both carry
the header date 2026-01-09. That helps him, and the paralegal should see it. Per D-017 the tool does not compute a
delay from an accident date: the only stated accident date is rec 7's "2026-01-19", which is later than the first
recorded treatment, and the tool must never pick a date. It shows "first recorded treatment: 2026-01-09", and the attorney reads that
against whichever accident date the facts support.

**A13 Mechanism / MIST.** Src 1 lists the police report (transported?), vehicle photos (does the damage match? what
direction was the force?) and mechanism as first-line checks. Minor-impact soft-tissue (MIST) files are handled as
a category by many carriers (src 18, plaintiff-side; carrier MIST programs are not public). EMS run reports are where
scene facts live: speed, restraint, airbag deployment, ambulatory at scene, refused transport. Per D-018 those
phrases are `causation` flags citing the excerpt, and they go to the internal notes only (D-001).

**A14 Attorney involvement / LOP.** An insurer-side trade article describes providers, attorneys and clinics that
"steer claimants into higher cost services", with plaintiffs' counsel referring claimants to pain-management
centers, and says defense counsel then "may challenge causation or necessity" (src 20). Texas made providers'
negotiated rates discoverable to test LOP charges (*In re K & L Auto Crushers*, texas-pi-notes.md §3). **Assumption
(adjuster practice; claims-adjuster persona §2, no source found):** adjusters compare the attorney-retention date
with when care started or escalated. The tool cannot know the retention date from medical records, so it flags
only what a record says ("referred by attorney", "letter of protection"). Record 7 names no referral source (record 3 says only "Refer to physical therapy").

**A15 Duration and type of care.** Src 1 asks whether treatment was "active or passive" and "longer than an
anticipated expected recovery date". Colossus reportedly scores duration per injury (src 3, second-hand). For Rivera
the records do not say whether PT was active or passive: records 4–6 name no modality. They do support "shorter than
planned": rec 4 "Plan of care: 12 visits", and rec 6 "Discharged from PT after two missed appointments" under the
source label "Capital PT, visit 9". The ESI is only recommended (rec 9). This is context for the adjuster persona, not
a required flag.

**A9 Subjective vs objective.** Adjusters weigh objective findings (imaging, ROM measurements, spasm) above pain
scores (src 1, 18). Not a required flag; useful for the one-line summary (keep numbers verbatim) and for the
adjuster persona's checklist.

**A10 Billing.** Texas limits recovery to amounts "actually paid or incurred" and makes unadjusted list charges
inadmissible (Haygood, src 12); negotiated rates are discoverable to test reasonableness (K&L Auto Crushers,
see texas-pi-notes.md). Adjusters compare billing against SOAP notes for upcoding (src 1). For the tool: list
*billed* amounts exactly as written and never present them as the recoverable figure.

## Implications for flags and lexicon (handed to T-009)

- Lexicon categories (D-013/D-018): `pre_existing` (A3, A4); `causation` (A2, A4–A6, A8, A13, A14 — including
  the former `compliance` phrases: missed appointments, non-compliance, discharged/left AMA); `record_warning`
  (date ambiguity, injection). A12 and A15 are context only.
- Every phrase that is a *negation* ("denies", "no history of", "no prior") is a false-positive guard.
- Hedges are flagged *because* they are hedges; the flag rationale must say the record is equivocal, not that
  the finding is degenerative.
- Self-report markers ("patient states/reports/believes/attributes") are flagged only when attached to causation
  or onset, else they are noise (every history line starts "patient reports").

## Sources

1. Claims Journal, C. Tidball, "How to Review Bodily Injury Demands" (2013-06-05) — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — Adjuster checklist: treatment timing/gaps, priors and intervening causes, objective findings, provider credentials, duration vs typical recovery, billing vs SOAP notes, mechanism of injury. (Insurer-side trade press.)
2. Verisk, "5 reasons workers compensation adjusters need ISO ClaimSearch" — https://www.verisk.com/blog/5-reasons-workers-compensation-adjusters-need-iso-claimsearch/ — Insurer data vendor: ClaimSearch shows claimant loss history so adjusters can "identify preexisting or subsequent injury." (Insurer-side vendor; via search snippet.)
3. Simmons & Fletcher, "What is Colossus Claims Adjusting Software?" — https://www.simmonsandfletcher.com/car-accidents/auto-insurance-claims/colossus/ — Second-hand: Colossus records duration of treatment per injury, prognosis, future treatment. (Plaintiff firm; Colossus is proprietary — unverified.)
4. Butler Firm, "How insurance companies use gaps in medical treatment against you" — https://butlerfirm.com/blog/how-insurance-companies-use-gaps-in-medical-treatment-against-you/ — Gaps let insurers argue injuries were minor or unrelated. (Plaintiff firm.)
5. Young Injury Law, "Gap in medical treatment" — https://younginjurylaw.com/blog/gap-in-medical-treatment-ohio-injury-claim/ — Explain gaps proactively with referral/appointment paperwork; not every pause hurts. (Plaintiff firm.)
6. Brinjikji W. et al., "Systematic literature review of imaging features of spinal degeneration in asymptomatic populations," AJNR 36(4):811 (2015) — https://www.ajnr.org/content/36/4/811 — Degenerative disc findings are common in pain-free adults and rise with age (bulge ~30%→84%, protrusion 29%→43%, age 20→80). **Lumbar spine only** — for cervical prevalence see src 19. (Peer-reviewed; abstract figures via search index — page 403'd to WebFetch.)
7. AuntMinnie Europe, "Banned: top 8 words or phrases to avoid in radiology reports" — https://www.auntminnieeurope.com/clinical-news/article/15646568/banned-top-8-words-or-phrases-to-avoid-in-radiology-reports — Radiology chair lists "cannot rule out" and "clinical correlation" as hedges that can mislead. (Radiology trade press.)
8. UCSF study of uncertainty terms in 642,569 radiology impressions — https://escholarship.org/content/qt3f22329f/qt3f22329f.pdf — Hedging terms vary by radiologist and subspecialty; "cannot exclude" signals uncertainty. (Academic.)
9. Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007) — https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html — Expert testimony generally required for causation of conditions outside lay knowledge; lay evidence suffices only for basic, immediate injuries. (Primary; summary page.)
10. JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015) — https://www.txcourts.gov/media/943999/130978.pdf — Evidence of a second accident is relevant to causation; excluding it was harmful error. (Primary; read via summaries.)
11. Jelinek v. Casas, 328 S.W.3d 526 (Tex. 2010) — https://case-law.vlex.com/vid/jelinek-v-casas-no-887565131 — Causation needs "reasonable medical probability"; testimony that something is a *possible* cause ordinarily is not enough. (Primary; read via secondary summaries — verify pin cites.)
12. Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011) — https://caselaw.findlaw.com/tx-supreme-court/1573065.html — Recovery limited to amounts actually paid or incurred; only evidence of recoverable expenses is admissible. (Primary, full text read.)
13. Roman Austin, "Mitigate damages" — https://romanaustin.com/blog/mitigate-damages/ — Texas firm: failure to mitigate requires the insurer to show the claimant's conduct increased damages. (Plaintiff firm.)
14. Herrera v. Madrak (missed >12 PT sessions supported a mitigation instruction) — https://case-law.vlex.com/vid/herrera-v-madrak-ac-889277215 — Contrast Fletcher v. Simmons (La. App. 2003), https://www.studicata.com/summaries/court-of-appeal-of-louisiana/fletcher-v-simmons-2003-l2aha0 — insufficient evidence of failure to mitigate. (Primary/summaries; non-Texas.)
15. Tavrn, "Legal demand letter best practices" — https://www.tavrn.ai/blog/legal-demand-letter-best-practices — Concealed pre-existing conditions draw credibility discounts across the claim. (Vendor.)
16. Virginia Lawyers Weekly, "Plaintiff prevails in disputed back injury case" (2014) — https://valawyersweekly.com/2014/10/09/plaintiff-prevails-in-disputed-back-injury-case-100000-verdict/ — Defense expert attributed symptoms persisting past 6–9 weeks to pre-existing degenerative disc disease. (Legal press.)
17. Georgia Court of Appeals decision on impeachment with prior intake forms — https://caselaw.findlaw.com/court/ga-court-of-appeals/1418582.html — Defense may impeach with the claimant's own medical intake forms listing prior accidents/complaints. (Primary, non-Texas; via search summary.)
18. Braun Law, "Objective vs. Subjective" — https://braunslaw.com/claimclinic/claim-worth/specific-injuries/ — Claim evaluation software weighs objective injuries more heavily. (Plaintiff firm.)

19. Nakashima H. et al., "Abnormal findings on magnetic resonance images of the cervical spines in 1211 asymptomatic subjects," Spine 40(6):392–398 (2015) — https://pubmed.ncbi.nlm.nih.gov/25584950/ — Cervical disc bulging in 87.6% of asymptomatic adults aged 20–70, most already in their 20s; cord compression 5.3%, most often at C5-C6 (41%) and C6-C7 (27%). The study measured disc bulging (not protrusion) in Japanese volunteers. (Peer-reviewed; abstract figures confirmed by the claims-adjuster reviewer via NCBI efetch.)

20. Insurance Journal, P. Dhakal, "Viewpoint: Inside the Machinery of Medical Abuse in Liability Claims" (2026-01-21; author works for CLARA Analytics, a claims-analytics vendor to insurers) — https://www.insurancejournal.com/news/national/2026/01/21/854959.htm — Insurer-side view: referral networks "steer claimants into higher cost services"; plaintiffs' counsel refer claimants to pain-management centers; defense "may challenge causation or necessity". Says nothing about retention timing or LOPs. (Insurance trade press, opinion piece.)

Assumptions where sources are thin: (a) no public adjuster manual quantifies how much each attack reduces value;
(b) Colossus specifics are second-hand; (c) the 30-day gap threshold is the Zlayt spec's, not an industry rule —
real adjusters may treat shorter gaps as material, so the prototype's threshold should be configurable.
