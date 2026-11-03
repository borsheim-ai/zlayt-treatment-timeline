# Case library sources v2 (T-077)

Seventeen real-world personal-injury record patterns from public sources, for the next round of fully synthetic packets in
`evals/library/` (after `case_lib01`–`case_lib07`, see `research/case-library-sources.md`). Researched 2026-11-01/02 by the
researcher agent. Feature names follow D-042 (`memory/ORCHESTRATOR_DECISIONS.md`) plus the base flag types (D-013) and the
credibility rule (D-043).

**No duplication with v1.** v1 covered: ER visit then a long gap; slip-and-fall onto a previously operated knee; chiropractic
volume on a truck rear-end; facial dog bite and scar revision; pedestrian ORIF and hardware removal; LOP billed-vs-adjusted
(Haygood line); missing out-of-state records. None of the patterns below reuses those scenarios or v1's sources. Sources
already cited in `research/texas-pi-notes.md` and `research/adjuster-attacks.md` (Haygood, In re Allstate, K&L Auto Crushers,
Brinjikji, Nakashima) are not used as primary sources here.

**Read depth (stated honestly).** "Full text" means the opinion or abstract itself was fetched and read. "Summary" means only
a secondary write-up or search excerpt was seen. Verify a summary-level source against the original before quoting it
outside this repo. Court opinions are authority for what the court said; firm write-ups and press are one side's account.
Medical studies describe record quality in general, not PI records specifically; the PI framing is ours.

## Synthetic-safety rules (apply to every pattern)

1. **Pattern, not facts.** We take the shape of the record (what kind of page, which wording, which billing columns, where
   the gap falls) and nothing else. No party, provider, clinic, county, road, date, amount or diagnosis code is copied.
2. **Invented people and places.** Every name, provider, clinic and town is invented (the v1 style: Marrowgate,
   Dr. Pennywhistle). The denylist scan in `research/validate_library.py` must pass. Every real name in this file is on
   that denylist (see "Denylist additions" below; matching is case- and accent-insensitive). `--self-test` extracts every
   author surname, every bare name in the opening citation list and every caption name from this file, fails if any is not
   listed, and fails if a planted packet containing one passes the scan. Common surnames that appear here
   (Garza, Rodriguez, Hills, Gunn, Hampton, Castro, Powell, Anderson, Flores) are banned as invented-name choices too,
   including in the Spanish-language packets: pick distinctive invented surnames instead.
3. **Dates shifted.** Packet dates run in 2025–2027 and keep only the *interval* shape the pattern needs (e.g. "second event
   about 12 weeks after the first"). Real dates in this file are citation dates for the source, not record dates.
4. **Facts recombined.** Each packet mixes features from two or more patterns, so no packet maps back to one real matter.
5. **Every packet text file starts with the SYNTHETIC banner line** used by v1 and is labeled synthetic in its expected JSON.
6. **No real records.** Nothing here was taken from a medical record; opinions describe facts in prose, and we use that prose
   only for scenario shape. Spanish text in packets is written fresh, not translated from any source.

## Patterns

### P1. Intervening second accident between first care and the key imaging
- **Source:** JLG Trucking, LLC v. Garza, 466 S.W.3d 157 (Tex. 2015), opinion delivered 2015-04-24 —
  https://www.txcourts.gov/media/943999/130978.pdf (full text, background section read).
- **Summary:** The plaintiff was rear-ended, saw an orthopedist five days later, did about eleven weeks of PT, then had a
  second crash shortly after PT ended and was taken by ambulance in a hard collar. The MRI showing herniations came only after
  the second crash; surgery followed years later. The court held the second accident was relevant to causation and its
  exclusion (including on cross of the treating doctor) was harmful error, even without a defense causation expert.
- **Record features (from source):** an orthopedic visit days after event 1, then about eleven weeks of PT; an ambulance
  transport in a hard collar after event 2; first MRI dated after event 2; a treating note whose history omits event 2;
  multi-year span ending in fusion.
- **Record features (our inference):** first-incident clinic records missing from the file; an ER record from event 2 with
  neck complaints; a surgeon's narrative "history" that attributes everything to event 1.
- **D-042 / flags:** conflict (two incident dates in the chart), causation (history-only attribution is self-reported/
  provider-recited, not an opinion), gap; multi-case library; vertical stepper must show "two incidents found: human
  decides relevance" as a HITL step. The tool never apportions.
- **Synthetic-safety:** invent both crashes, shift to 2025–2026, change the interval (e.g. 10–14 weeks), change body region
  if useful (lumbar instead of cervical); no county, highway or vehicle type from the opinion.

### P2. Immediate care is common-knowledge; later complex care needs an expert
- **Source:** Guevara v. Ferrer, 247 S.W.3d 662 (Tex. 2007), decided 2007-08-31 —
  https://caselaw.findlaw.com/summary/opinion/tx-supreme-court/2007/08/31/152297.html and commentary
  https://www.casemine.com/commentary/us/expert-medical-evidence-mandated-for-causation-in-high-cost-automobile-accident-claims:-guevara-v.-ferrer/view
  (summary only).
- **Summary:** An elderly passenger's family relied on lay testimony to tie over $1 million in medical expenses to a crash.
  The court held lay evidence can link a crash to conditions within common knowledge (immediate post-crash care), but
  conditions outside it need expert evidence; the claimant must show what conditions generated the expenses and that each
  was caused by the accident.
- **Record features (from source):** immediate post-crash care, then a long, medically complex course with large total
  expenses in an elderly patient.
- **Record features (our inference):** EMS and ER pages with visible injuries; later admission, procedure and rehab notes
  with no causation statement; one itemized hospital bill spanning both phases; comorbidities in the problem list.
- **D-042 / flags:** causation (absence of any provider causation statement on later care is shown as "no causation
  language found", not as a finding), pre_existing (comorbidity list), billing analysis (charges split by encounter, cited
  per line); calibrated confidence must not imply causation strength.
- **Synthetic-safety:** age band changed, no death in the packet, invented hospital, amounts invented and far smaller.

### P3. Billing affidavits and records are not causation; conclusory physician letter
- **Source:** Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute
  mem. op.) — opinion PDF via the court docket https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 (full
  text read, pdftotext). The docket shows the memorandum opinion of 2020-01-14, a rehearing motion, and on 2021-02-11
  rehearing denied, the 2020 opinion withdrawn and a substitute memorandum opinion issued; petition for review No. 21-0287
  denied 2021-07-23 (https://txcourts.gov/supreme/orders-opinions/2021/july/july-23-2021/). The firm newsbrief
  https://www.mdjwlaw.com/newsroom/news/TIN-20200211-item1 describes the 2020 opinion (2020 WL 206187) and does not mention
  the withdrawal; the withdrawal and substitution are shown only on the docket page above (the substitute opinion is not linked).
- **Summary (2021 substitute opinion):** Soft-tissue claims after a rear-end crash; no ambulance or ER. Past-medical awards
  for three plaintiffs were reversed and rendered: §18.001 affidavits prove reasonableness of charges, not causation, and
  a treating doctor's letters (and causation statements inside billing records) were conclusory because they gave no
  explanation of how and why the crash caused the diagnoses. The award for a fourth plaintiff's ankle injury, and her
  child's single visit, was affirmed on lay testimony and temporal proximity (Guevara).
- **Record features (from source):** letters from a treater stating the crash caused the injuries, with no reasoning;
  causation statements embedded in billing records; long diagnosis lists (radiculitis, disc displacement, discogenic pain)
  on the bills; one plaintiff's single-visit bill (evaluation plus hot/cold pack).
- **Record features (our inference):** billing-affidavit cover pages that look like records but carry no clinical content;
  the same diagnosis lines repeated on every bill.
- **D-042 / flags:** causation (letter language is shown verbatim with source; the tool never upgrades it to an opinion);
  billing analysis (affidavit totals cited to the page, not re-derived by the LLM); LLM-as-judge visible: the judge must
  reject any summary that turns "the accident caused" into a fact; record_warning for non-clinical pages.
- **Synthetic-safety:** invented clinic and letter text; diagnosis wording paraphrased generically; no amounts reused; no
  highway, county or party name from the opinion.

### P4. Spanish-speaking party, certified interpreter, uncertified translation; counteraffidavit fight
- **Source:** Chiv v. Figueroa, No. 01-23-00638-CV (Tex. App.—Houston [1st Dist.] 2025-08-21) —
  https://hallapproved.com/tx/cases/appeals/2025/10659616/ (page fetched; summarized by the fetch tool, not read line by line).
- **Summary:** A party sought to use a deposition taken in Spanish that lacked a certified translation, with a certified
  interpreter at trial; that point was not preserved. Separately, striking a §18.001 counteraffidavit was harmful because the
  only non-lay causation evidence came from admitted medical reports; past medical was reversed and remanded.
- **Scope of support:** this source supports only the scenario theme (Spanish-speaking party, translation and
  counteraffidavit disputes). The opinion says nothing about how records are charted.
- **Record features (our inference):** records where the history is given in Spanish and charted in English; a note line
  such as "history via interpreter" (or its absence); an itemized bill paired with a counteraffidavit-style rebuttal page.
- **D-042 / flags:** Spanish-language records (the excerpt stays in the original language; any LLM translation is labeled
  and judged); speaker attribution v2 (patient vs interpreter vs provider); billing analysis (contested line items shown, not
  resolved).
- **Synthetic-safety:** invented parties and providers; Spanish lines composed fresh; no deposition content used.

### P5. Prior accidents, claimed brain injury, memory gaps, and a six-column billing request
- **Source:** In re Central Oregon Truck Co., No. 20-0945 (Tex. 2022, per curiam), opinion delivered 2022-05-06 —
  https://www.txcourts.gov/media/1454150/200945pc.pdf (full text read).
- **Summary:** After a rear-end crash the plaintiff claimed a TBI and lost earning capacity; she had treated after two
  earlier car accidents and for other conditions with overlapping symptoms, and said at deposition that memory problems
  limited her recall. The court held pre-accident medical records and provider billing data relevant (subject to
  proportionality). The billing discovery listed six items: (1) total billed charges, (2) adjustments or write-offs,
  (3) amount paid to the provider and by whom, (4) outstanding balances, (5) copies of contracts with the health-insurance
  carrier, (6) any letters of protection, contracts, liens or other guarantees.
- **Record features (from source):** two earlier car accidents with treatment; memory complaints; a prior tailbone surgery;
  the six billing-discovery items above.
- **Record features (our inference):** intake forms answering "prior accidents: none" vs older notes that mention them; a
  neuro or neuropsych note with memory complaints; ledger columns derived from items 1-4 and 6 (billed, adjusted, paid,
  payer, balance, LOP/lien). Item 5 (carrier contracts) is a separate document a packet may reference but never reproduce
  as a ledger column.
- **D-042 / flags:** billing analysis (ledger columns from items 1-4 and 6, each cited; totals by code); pre_existing (prior accidents); conflict
  (intake denial vs older note); calibrated confidence (per-state precision, not a "TBI likely" score).
- **Synthetic-safety:** invented crash count and years (shift to e.g. 2019/2022 priors, 2026 index event); generic employment
  facts omitted; ledger numbers invented.

### P6. Health-insurer-paid claims: EOBs with billed, allowed, paid, patient share
- **Source:** Gunn v. McCoy, 554 S.W.3d 645 (Tex. 2018), decided 2018-06-15 (one secondary source says 2018-02-08; trust the
  reporter citation) — https://dallas-appellate.blogspot.com/2018/06/kmh-scotx-insurance-agents-may-know.html and
  https://painterfirm.com/medmal/texas-supreme-court-allows-streamlined-approach-to-medical-billing-affidavits/ (summary only).
- **Summary:** In a health care liability claim (medical malpractice, not a crash case), the plaintiff replaced provider
  billing affidavits with affidavits from health insurers' subrogation agents stating amounts actually paid; the court held
  §18.001 does not limit affiants to providers or their custodians.
- **Record features (from source):** insurer subrogation-agent affidavits stating amounts paid.
- **Record features (our inference):** insurer EOB pages (billed / allowed / plan paid / deductible / coinsurance / patient responsibility /
  "not covered" with a remark code); the same date of service appearing on a provider bill and an EOB with different numbers;
  the affidavit page itself.
- **D-042 / flags:** billing analysis (paid vs incurred, never chosen by the LLM; code reconciles EOB to provider bill and
  flags mismatches); charge reclassification guard (an "allowed amount" is not a charge); dedupe of the same service across
  two documents.
- **Synthetic-safety:** invented insurer, plan and remark codes; amounts invented; no real payer names.

### P7. Pain out of proportion, "somatization", "symptom magnification" in the exam note
- **Source:** Rodriguez v. Wal-Mart Stores, Inc., A-2/3-17 (N.J. 2019-03-04) —
  https://www.njcourts.gov/system/files/court-opinions/2019/a_2_3_17.pdf (syllabus read).
- **Summary:** A shopper hit by a falling display developed a CRPS diagnosis. A defense neurologist described a strong pain
  reaction to light touch while a companion rubbed the same arm without a reaction, found nothing objective, and used
  "somatization" and "symptom magnification". The court held such terms are admissible case by case, distinguished them from
  "malingering", and upheld admission of unrelated past medical history.
- **Record features (from source):** a defense neurologist's exam narrating observed behavior (pain reaction to light touch vs
  none when a companion touched the arm), no objective findings, "somatization" and "symptom magnification"; unrelated past
  medical history.
- **Record features (our inference):** treater notes using the same CRPS vocabulary in the opposite direction.
- **Case stage:** a defense medical exam is a post-suit event (in Texas, TRCP 204 needs a motion and court order). For a
  pre-suit demand packet use the same wording in a carrier records-review (peer-review) letter instead (see lib12).
- **D-042 / flags:** credibility flags (D-043: any credibility term flags; a second clause or contrast word always flags);
  speaker attribution v2 (examiner's observation vs patient's report vs companion's behavior); LLM-as-judge visible; the tool
  never concludes malingering.
- **Synthetic-safety:** different mechanism (e.g. falling shelf at a hardware store), different limb, invented examiner;
  no psychiatric details beyond a generic history line.

### P8. Waddell signs charted as a score
- **Source:** Fishbain et al., "A Structured Evidence-Based Review on the Meaning of Nonorganic Physical Signs: Waddell
  Signs", Pain Medicine 4(2):141–181 (2003); companion review Clin J Pain 20(6):399–408 (2004) —
  https://www.statpearls.com/articlelibrary/viewarticle/31286/ (StatPearls overview; reviews seen via search summaries only).
- **Summary:** Reviews of the Waddell literature found the signs associated with poorer treatment outcomes but not reliably
  with secondary gain or malingering; adjusters and IMEs still cite a positive count as a credibility point.
- **Record features (from source):** the five Waddell sign categories (superficial/non-anatomic tenderness, simulation,
  distraction, regional disturbance, overreaction) charted as a count.
- **Record features (our inference):** "Waddell 3/5 positive", "distraction SLR negative"; clean negations ("0/5 Waddell
  signs") on other dates; FCE "effort inconsistent" lines. "Waddell" is an eponymous clinical term and is allowed in
  packets (it is on the validator's eponym allow-list, not the denylist).
- **D-042 / flags:** credibility flags with the D-043 allow-list (clean negation does not flag; mixed sentence flags);
  dismissal-pattern learning must not learn to auto-dismiss credibility flags (eval-guarded).
- **Synthetic-safety:** all wording composed fresh; invented PT/FCE provider and dates.

### P9. Interpreter errors and ad hoc (family) interpreters in a Spanish-language history
- **Source:** Flores G. et al., "Errors in medical interpretation and their potential clinical consequences in pediatric
  encounters", Pediatrics 111(1):6–14 (2003) — AHRQ research summary
  https://webarchive.library.unt.edu/web/20081105020658/http:/www.ahrq.gov/research/apr03/0403RA20.htm (summary only).
  Corroborating (search excerpt only, page returned 403): Texas DWC Appeals Panel decisions on interpreter word choice
  ("espalda" for the area between the shoulder blades; "cane" vs "crutches") — https://texasworker.com/?p=38127.
- **Summary:** Thirteen audiotaped visits averaged 31 interpretation errors each; most had potential clinical consequences,
  ad hoc interpreters' errors more often so (77% vs 53%); omission was the commonest error. One reported example turned a fall
  into a reported assault.
- **Record features (from source):** an ad hoc family interpreter; omissions; a mechanism that changed in interpretation
  (fall reported as assault); "espalda" word choice (DWC excerpt only).
- **Record features (our inference):** "Hx obtained via patient's son (interpreter)"; mechanism worded differently on two
  records; a Spanish intake form beside an English provider note; DD/MM/YYYY dates on a form from a clinic across the
  border.
- **D-042 / flags:** Spanish-language records; speaker attribution v2 (who said it); conflict (mechanism mismatch, code
  surfaces both); date-convention suggestion (pre-select with reason, one confirm); body-region ambiguity goes to human.
- **Synthetic-safety:** no pediatric facts; adult patient, invented family member and clinic; Spanish text composed fresh.

### P10. Copy-forward (cloned) notes that contradict the visit
- **Source:** Steinkamp J., Kantrowitz J.J., Airan-Javia S., "Prevalence and Sources of Duplicate Information in the
  Electronic Medical Record", JAMA Network Open 5(9) (2022-09-01) — https://pubmed.ncbi.nlm.nih.gov/36156143/ (abstract read).
- **Summary:** Across about 104.5 million notes at one health system (2015–2020), 50.1% of text was duplicated from earlier
  notes about the same patient, rising from 33% to 54.2%; 45.9% of duplicated text came from a different author.
- **Record features (from source):** half of note text duplicated from earlier notes, often from another author.
- **Record features (our inference):** identical ROS/exam blocks across visits weeks apart ("denies neck pain" copied into a neck-pain
  follow-up); "pain 6/10" unchanged across six visits; a stale medication list; a plan that repeats a completed referral.
- **D-042 / flags:** conflict (same-visit contradiction between HPI and copied ROS); dedupe must *not* merge two visits just
  because text matches (code dedupes by date + provider + content, and shows near-duplicates for human review);
  LLM-as-judge must catch a summary that cites the copied line as current; vertical stepper shows "near-duplicate text
  across N visits".
- **Synthetic-safety:** template text invented; invented clinic.

### P11. Left/right transposition across records
- **Source:** ElGhrably I., Fraser S.G., "An observational study of laterality errors in a sample of clinical records",
  Eye 22(3):340–343 (2008) — https://www.nature.com/articles/6702590 (abstract via search excerpts).
- **Summary:** In 100 randomly selected ophthalmic record sets the authors found 44 left/right transposition errors in 32
  sets; 19 were later corrected; three consent forms named the wrong eye.
- **Record features (from source):** left/right transpositions across a record set, some later corrected; consent forms
  naming the wrong side.
- **Record features (our inference):** "right shoulder" in the ER note, "left shoulder" in the ortho note, MRI ordered on one side and read on
  the other; a radiculopathy side that flips; a correction addendum.
- **D-042 / flags:** conflict (mixed-side exam findings, code-detected by side tokens per body part; never resolved by the
  LLM); judge must reject a summary that silently picks a side; HITL step "confirm side".
- **Synthetic-safety:** orthopedic not ophthalmic; invented providers; side flip placed at an invented visit.

### P12. Handwritten, scanned pages with illegible entries
- **Source:** Rodríguez-Vera F.J. et al., "Illegible handwriting in medical records", J R Soc Med 95(11):545–546 (2002) —
  https://pmc.ncbi.nlm.nih.gov/articles/PMC1279250 (abstract-level via search; full text not read).
- **Summary:** Of 117 hospital case notes, 15% were so illegible that meaning was unclear; surgical departments scored worse.
- **Record features (from source):** illegible handwritten hospital notes whose meaning is unclear.
- **Record features (our inference):** faxed or scanned urgent-care and chiropractic daily notes; checkbox SOAP forms; handwritten pain
  scores and dates; signatures illegible; a typed later page that disagrees with a handwritten earlier page; skewed scans.
- **D-042 / flags:** local OCR (Tesseract) with page image beside OCR text, OCR-derived items always need review; date-
  convention suggestion for handwritten dates; PDF hidden-text detection (assumption, no public PI source found: a scanned
  page whose embedded text layer differs from the image, e.g. a copy-service OCR layer; we include it adversarially).
- **Synthetic-safety:** handwriting rendered synthetically (font or generated strokes), never scanned from a real chart.

### P13. Concussion not diagnosed in the ER; LOC history changes later
- **Source:** Powell J.M. et al., "Accuracy of Mild Traumatic Brain Injury Diagnosis", Arch Phys Med Rehabil 89(8):1550–1555
  (2008) — https://natlawreview.com/article/new-study-finds-emergency-room-physicians-often-fail-to-diagnose-tbi (summary only).
- **Summary:** Among ED patients who met CDC mild-TBI criteria by study interview, 56% had no documented TBI diagnosis in the
  ED record; ED care focused on ruling out severe injury.
- **Record features (from source):** an ED record with no TBI diagnosis for a patient who met mild-TBI criteria.
- **Record features (our inference):** ER "denies LOC", "CT head negative", discharge dx "neck strain"; a later neurology note "brief LOC per
  patient", headaches, word-finding complaints; a neuropsych page weeks later.
- **D-042 / flags:** conflict (LOC denied vs reported, both cited); causation (patient-stated onset); new body system after
  a gap; speaker attribution (per patient vs examiner). The tool does not diagnose concussion.
- **Synthetic-safety:** invented ED and neurologist; mechanism changed; dates shifted.

### P14. Chargemaster charge vs what is owed (rate-vs-charge trap on hospital bills)
- **Source:** Bai G., Anderson G.F., "Extreme Markup: The Fifty US Hospitals With The Highest Charge-To-Cost Ratios",
  Health Affairs 34(6) (2015) — https://publichealth.jhu.edu/2015/some-hospitals-marking-up-prices-more-than-1000-percent
  (press release; paper not opened).
- **Summary:** In 2012 Medicare cost-report data the typical hospital charged about 3.4 times Medicare-allowable cost; the 50
  highest-markup hospitals charged roughly ten times, 49 of them for-profit.
- **Record features (from source):** hospital charges several times cost.
- **Record features (our inference):** UB-04-style itemized bill with revenue codes, units and unit price; a "self-pay discount" line; a
  later statement with a contractual adjustment; a price list or rate sheet page that is not a charge.
- **D-042 / flags:** charge reclassification guard (a rate becomes a charge only with code-verified charge wording plus a
  judge re-check); billing analysis (units × unit price is recomputed in code and compared with the stated line total);
  totals in code only.
- **Synthetic-safety:** invented hospital, codes and prices; no real chargemaster data.

### P15. Ambulance bill: base rate plus per-mile mileage
- **Source:** FAIR Health, "A Window into Utilization and Cost of Ground Ambulance Services" (brief, 2023) —
  https://mma.prnewswire.com/media/2207553/A_Window_into_Utilization_and_Cost_of_Ground_Ambulance_Services___A_FAIR_Health_Brief.pdf?p=pdf
  (search excerpt only).
- **Summary:** Ground ambulance claims are billed as a base transport line plus mileage per statute mile; most claim lines
  were out of network (63.7% in 2018, 59.4% in 2022).
- **Record features (from source):** a base transport line plus per-mile mileage; out-of-network claim lines. Medicare billing
  rules confirm two lines per trip and loaded miles rounded up to the tenth (see research/record-formats.md §16).
- **Record features (our inference):** EMS run sheet (times, vitals, "ambulatory at scene" or "stretcher") plus an invoice with "ALS base",
  "mileage 14 mi @ $X/mi" and a line total; a balance-bill page.
- **D-042 / flags:** charge reclassification (the per-mile rate is a rate; only the extended line or stated total is a charge);
  billing analysis (lien/balance columns); code checks miles × rate = stated line.
- **Synthetic-safety:** invented EMS agency, mileage and rates.

### P16. Same-week symptom contradiction across two providers
- **Source:** Lewis Brisbois write-up of a Harris County zero-damages defense verdict (trial 2023-12; published 2024-06-25)
  — https://www.legal500.com/intelligence/united-states/litigation-mediation-arbitration/houston-office-secures-zero-damages-verdict-in-rear-end-collision-case
  (fetched; defense-side account).
- **Summary:** After an ER visit the next day and care with several providers, the plaintiff reported significant neck and
  back pain to an orthopedic surgeon while denying those symptoms to her primary-care doctor; the defense also disputed a
  recommended discectomy and pointed to photos of a minor impact. The jury awarded nothing.
- **Record features (from source):** neck and back pain reported to an orthopedic surgeon while denied to the primary-care
  doctor; a recommended discectomy; photos of minor impact.
- **Case stage and entry:** in the source the PCP records came in by defense subpoena (post-suit). In a pre-suit demand
  packet the PCP note arrives from the paralegal's own records request after the client lists the PCP on intake (lib13).
- **Record features (our inference):** ortho note "low back pain 8/10, radiating" and a PCP note days apart with ROS "denies back pain"
  (possibly copied forward, see P10); a surgical recommendation with a cost estimate; property-damage photos referenced but
  not in the file.
- **D-042 / flags:** conflict (cross-provider, code pairs nearby dates); billing analysis (estimate is not a charge, D-019);
  vertical stepper HITL "two providers disagree; paralegal decides which to cite".
- **Synthetic-safety:** drug-use facts from the write-up are **not** used; invented providers; shifted dates.

### P17. Minimal property damage, low-speed impact (MIST) language in records
- **Source:** Castro W.H. et al., "Do 'whiplash injuries' occur in low-speed rear impacts?", Eur Spine J 6(6):366–375
  (1997), PMID 9455663 — https://pubmed.ncbi.nlm.nih.gov/9455663/ (abstract read via PubMed). This replaces the round-1
  source (a Texas appellate summary on a reconstructionist's five-mph opinion) because no court, district, docket or
  reporter cite could be found for it and its page returned 403; its names stay on the denylist.
- **Summary:** Nineteen volunteers in staged rear impacts (velocity change about 9-14 km/h) showed no injury signs on exam,
  motion analysis or MRI, with one minor exception. The study is the kind of biomechanical evidence the defense cites for
  "minor impact, soft tissue" arguments.
- **Scope of support:** this source supports only the scenario theme (low-speed impacts are argued to be non-injurious).
  It says nothing about EMS or ER wording.
- **Record features (our inference):** EMS "minor damage to rear bumper", "ambulatory at scene", "refused transport"; ER
  "low-speed MVC"; later treater notes that describe the crash as "violent" or "high impact" (patient-reported).
- **D-042 / flags:** causation (scene facts per D-018 lexicon); conflict (mechanism description changes over time, both
  attributed); speaker attribution.
- **Synthetic-safety:** invented crash; no speeds or vehicles from the source; no study data reproduced in a packet.

## Coverage map: pattern x D-042 feature

| Feature (D-042 / base flags) | Patterns |
|---|---|
| Charge reclassification guard (rate vs charge) | P6, P14, P15 |
| Billing analysis (billed, adjusted, paid, LOP/lien, cited) | P2, P3, P4, P5, P6, P14, P15, P16 |
| Spanish-language records | P4, P9 |
| Local OCR, scanned/handwritten pages | P12 |
| PDF hidden-text detection | P12 (assumption-based, no public source) |
| Date-convention suggestion | P9 (assumption), P12 |
| Dismissal-pattern learning (eval guard) | P8 |
| Calibrated confidence | P2, P5 |
| Speaker attribution v2 | P4, P7, P9, P13, P17 |
| LLM-as-judge visible | P3, P7, P10, P11 |
| Vertical stepper / HITL hand-off | P1, P10, P11, P16 |
| Credibility flags (D-043) | P7, P8 |
| Conflict | P1, P5, P9, P10, P11, P13, P16, P17 |
| Pre-existing | P2, P5 |
| Causation language | P1, P2, P3, P13, P17 |
| Gap | P1, P13 |

## Suggested v2 packets (each recombines two or more patterns)

Stage: every packet simulates a **pre-suit demand file** unless marked otherwise. "Entry" says how each cross-provider record
reached the paralegal. Format sections refer to `research/record-formats.md`.

| Proposed id | Combines | One-line synthetic premise | Stage / entry |
|---|---|---|---|
| lib08_second_crash_mri_after | P1 + P13 | Rear-end, PT, second minor crash 11 weeks later, MRI and neuro note after crash 2 | Pre-suit; all records from the firm's requests to each provider |
| lib09_spanish_interpreter_espalda | P9 + P4 + P11 | History via son; "espalda" ambiguity; side flips between ER and ortho | Pre-suit; Spanish clinic note supplied by the client |
| lib10_eob_vs_provider_bill | P6 + P14 | Insured patient; hospital itemized bill plus EOBs with different numbers for same DOS | Pre-suit; EOBs from the client's health plan |
| lib11_priors_and_ledger | P5 + P2 | Two prior crashes denied on intake; ledgers; older patient comorbidities | Pre-suit; older notes from a records request to the PCP |
| lib12_records_review_credibility | P7 + P8 | Carrier records-review (peer-review) letter with symptom-magnification wording; PT/FCE notes with clean and mixed Waddell lines | Pre-suit; review letter came with the carrier's response to the demand. Litigation-stage variant: TRCP 204 exam report |
| lib13_cloned_notes_cross_provider | P10 + P16 | Copied ROS denies the complaint the ortho charts the same week | Pre-suit; PCP note from the firm's records request after the client listed the PCP |
| lib14_handwritten_chiro_scans | P12 + P15 | Scanned handwritten daily notes; ambulance base + mileage invoice; hidden text layer | Pre-suit; chiro records faxed by the provider |
| lib15_conclusory_letter_mist | P3 + P17 | "Accident caused all" letter; EMS minor-damage and refused-transport wording | Pre-suit; affidavits obtained from providers for later service, not yet served |

**Must contain** (the builder's checklist; each packet's expected JSON asserts these) and **formats used**:

| Proposed id | Must contain (D-042 features and flags) | Formats (record-formats.md §) |
|---|---|---|
| lib08 | Two incident dates in the chart (conflict); ED "denies LOC" vs neuro "brief LOC per patient" (conflict, speaker); first MRI dated after event 2; gap between PT discharge and the neuro visit; stepper HITL step "two incidents found" | EMS PCR §15, ED §2, PT §3, radiology §5, office/specialist note §19, ambulance invoice §16 |
| lib09 | One date `03/06/2026` day-first (truth 3 June 2026) and one `14/05/2026`; "Hx via son (interpreter)"; "espalda" with no level; right vs left shoulder across ER and ortho (conflict, HITL confirm side); translation labeled as LLM output | Spanish note §13, ED §2, office/specialist note §19, scanned intake §14 |
| lib10 | Same DOS on a provider bill and an EOB with different numbers (dedupe + mismatch flag); one UB-04 room line where FL44 rate × FL46 days = FL47 charge (rate-vs-charge guard); a 0001 total line; one CMS-1500 amount OCR'd without a separator with its truth stated | UB-04 §9, ledger §10, EOB §11, CMS-1500 §8 |
| lib11 | Intake "prior accidents: none" vs an older note naming two prior crashes (conflict, pre_existing); ledger with billed, adjustment, payment + payer, balance and LOP columns (items 1-4 and 6, no contract column); comorbidity problem list; calibrated confidence on pre-existing | scanned intake §14, office/specialist note §19, ledger §10, LOP §12 |
| lib12 | At least 4 credibility sentences across 3 dates: 2 clean negations ("0/5 Waddell signs") that must not flag, 2 mixed sentences ("Waddell 3/5; effort inconsistent") that must flag (D-043); at least 3 dismissable non-credibility flags so the dismissal-pattern guard is exercised | records-review/IME report §20, PT §3 |
| lib13 | PCP ROS "denies back pain" copied across 3 visits, and an ortho note "low back pain 8/10" in the same week (conflict, cloned text, no merge); a surgical cost estimate line (D-019: not a charge); HITL "two providers disagree" | office/specialist note §19 (PCP and ortho), ED §2 |
| lib14 | Scanned travel card with checkmarks; one handwritten date with no year; a CMS-1500 grouped line where days = units; an ambulance invoice where miles × per-mile rate = line total; a page whose hidden text layer differs from the image | chiro §4, scanned intake §14, CMS-1500 §8, EMS PCR §15, ambulance invoice §16 |
| lib15 | EMS "refused transport" and "minor damage" (causation lexicon, speaker); ER "low-speed MVC" vs later "violent impact" per patient (conflict); a narrative letter "caused all treatment" shown verbatim, never upgraded (judge rejects any summary that states it as fact); an 18.001 affidavit whose attached bill duplicates a bill already in the packet (dedupe) | EMS PCR §15, ED §2, chiro §4, narrative letter §18, 18.001 affidavit §17 |

## Denylist additions

Every real person's name and every firm-website slug or organisation name cited in this file's sources, including the
study authors (Steinkamp, Kantrowitz, Airan-Javia, ElGhrably, Fishbain, Powell, Anderson, Fraser, Brinjikji, Nakashima,
Rodríguez-Vera, Flores, Bai) and the bare-name citation list in the opening paragraph (Brinjikji, Nakashima). The same list is
in `DENYLIST_V2` / `DENY_CAPITALISED` of `research/validate_library.py`. `python3 research/validate_library.py --self-test`
fails if the two drift apart, if any surname it extracts from this file (author initials or 'et al', citation list, or
"X v. Y" caption) is not listed, or if a planted name in mixed case passes. Matching is case-insensitive and
accent-insensitive; the four capitalised-only terms are also ordinary lowercase words or phrases. Allowed on purpose:
"Waddell" (clinical eponym).

```text
JLG
Garza
Pechero
Zapata
Guevara
Ferrer
Donis
Matamoros
Castellanos
Morehouse
Reuben
Rueben
Poissant
I-45
Chiv
Figueroa
Central Oregon
Oregon
Broussard
Gunn
McCoy
Rodriguez
Wal-Mart
Walmart
Lewis Brisbois
Brisbois
Harris County
Hampton
Miskell
Baratta
I-635
Castro
Schilgen
Steinkamp
Kantrowitz
Airan-Javia
ElGhrably
Fishbain
Powell
Anderson
Houston
Dallas
Allstate
Fraser
Brinjikji
Nakashima
Vera
Rodríguez-Vera
mdjwlaw
painterfirm
Hills        # capitalised only
Flores       # capitalised only
Bai          # capitalised only
FAIR Health  # capitalised only (organisation)
```

## Assumptions and limits

- Hidden-text PDFs and DD/MM/YYYY dates in Spanish-language records are our adversarial assumptions; no public PI source
  documented them. They are included because D-042 reinstated those features and they need test cases.
- Texas DWC Appeals Panel decisions (P9) were seen only as a search excerpt (page returned 403). Hampton v. Miskell was
  dropped as P17's source in round 2: no court, district or docket could be found and its page returned 403.
- P4 (Chiv v. Figueroa) and P17 (Castro et al.) support only the scenario theme, not any record wording.
- Statute currency: CPRC §18.001/§18.002 text was checked 2026-11-02 through the texas.public.law mirror (amended through
  Acts 2019, 86th Leg., H.B. 1693; §18.001(b) now says the affidavit is not evidence of causation). The official
  statutes.capitol.texas.gov page is a JavaScript app that did not render for the fetch tool. Opinions are cited for
  scenario shape, not as current law.
- Medical studies (P8–P14, P17) describe general record quality or biomechanics, not PI files; every "Record features"
  line is tagged "(from source)" or "(our inference)".
- Defense-firm (P16) and plaintiff-side write-ups are advocacy; used for scenario shape only.
- Search also surfaced Texas Lawbook (2023-05-16) on a verdict where LOP provider entities were shown to the jury; it is
  paywalled and was not used.
