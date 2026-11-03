# Record and billing document formats for synthetic PI packets (T-078)

**Purpose.** D-042 says the multi-case library grows from researched real-world document formats. This file describes the nineteen document
types a Texas PI paralegal typically receives, so the packet generator can produce realistic, **fully synthetic** records that exercise the
tool's hard parts: dates, charges versus rates versus adjustments, totals lines, multiple authors, Spanish text and OCR noise.

**Rules followed.** Every specimen below is invented and labeled SYNTHETIC. Every person, provider, payer, address, phone, NPI, tax ID, claim
number and NDC was made up for this file; identifiers use a `SYN-` prefix, phones use the 555-01xx fiction range, places are invented. A web
search for each provider, payer, firm and clinician name (2026-11-02, results in section 23) found no exact match; two names close to real
organizations were replaced. CPT, HCPCS, ICD-10 and
revenue codes are public code sets, used only as codes. Sources are listed per format with whether I opened the page or worked from a
search-result summary; where a source is thin I state the assumption.

**How to use.** Section 1 holds the cross-cutting traps (dates, money, authorship). Sections 2 to 20 cover one format each (fields, wording,
traps, sources, specimen): 2-14 from round 1, 15-20 added in round 2 for the v2 library packets (EMS report, ambulance invoice, §18.001
affidavit, narrative letter, office/specialist note, records-review/IME report). Section 21 maps formats to product rules and packet mixes.
Section 22 lists every cross-specimen mismatch as fixed or DELIBERATE. Section 23 lists assumptions, gaps and the name-collision search.
`python3 research/record_formats_check.py` re-adds every specimen and checks the rules each one claims to follow.

---

## 1. Cross-cutting traps (apply to every format)

### 1.1 Dates that are not service dates
| Date on the page | Where it appears | Why it is a trap |
|---|---|---|
| Date of injury / onset | CMS-1500 Item 14 (qualifier 431), UB-04 occurrence code date (accident codes 01-06), LOP letter "Re:" line, intake form, narrative letter "Re:" line | It is the accident date, not a visit. Treating it as an encounter creates a phantom visit and hides the real first-treatment gap. |
| Signature / creation date | CMS-1500 Item 31, UB-04 FL 45 on the total line (unverified convention, see section 23), radiology "Signed", op-note "D:/T:" dictation and transcription stamps |
| Sworn / letter / report date | §18.001 affidavit jurat and notary commission date, narrative letter date, records-review or IME report date | Paperwork about care, not care. The affidavit's own date-of-service range spans many visits. | Usually a day or more after the service. Using it shifts the chronology and can invent a gap. |
| Statement / print / fax date | Ledger "Statement date", pharmacy "Printed on", fax header line at the top of every page | Same date on every page of a records production; a naive extractor dates every entry to the production date. |
| Received / Bates stamp | Rubber stamp "RECEIVED NOV 03 2026", Bates footer | Law-firm intake date; never a service date. |
| Fill date vs written date | Pharmacy log | A refill is not a visit and not a new prescription. |
| Exam date vs report date vs addendum date | Radiology | Three dates for one study. |
| Date ranges | CMS-1500 24A From/To with 24G units, UB-04 FL 6 statement period, PT "Visits 1 to 12" summary | One line can stand for many consecutive days (NUCC allows grouping only on consecutive days with identical code, charge and provider; days must equal units). |

**Formats seen:** `05/14/2026`, `051426` (claim boxes, no separators), `05 | 14 | 2026` (boxed), `2026-05-14` (EHR exports), `14-MAY-26`
(pharmacy and lab systems), `14/05/2026` and `14 de mayo de 2026` (Spanish-language clinics, day first), `5/14` (handwritten, no year),
`ene/abr/ago/dic` (Spanish month abbreviations; `ago` = agosto, also an English word: "3 days ago").

### 1.2 Money: charges, rates, adjustments, estimates
| Wording | Meaning | Counted as a billed charge? (D-019, D-042) |
|---|---|---|
| "Charges", "Total charges", "$Charges", "Amount billed", "Gross charges" | A stated charge for a dated service | Yes, when tied to a date of service and accepted |
| "Rate", "per visit", "per unit", "per day", "fee schedule", "Usual & customary", UB-04 FL 44 accommodation rate | A price, not something billed for a visit | No. D-042: a rate becomes a charge only with code-verified charge wording plus a judge re-check |
| "Adjustment", "Contractual adj", "Write-off", "W/O", "Network discount", "Courtesy discount", CARC "CO-45" | Reduction by the provider or under a contract | No (separate column; never subtracted silently from billed) |
| "Payment", "Ins pmt", "Pt pmt", "Plan paid", "Amount paid" (Item 29) | Money received | No |
| "Balance", "Balance due", "Amount due", "You owe", "Patient responsibility" | Remaining amount | No (it is a derived figure) |
| "Estimate", "Anticipated", "Quote", "Future care" | Not yet incurred | No |
| "LOP balance", "Lien amount", "Reduced to", "Accept in full satisfaction" | Negotiated or asserted amount | No (internal notes only) |

**Number formats.** CMS-1500 boxes use no dollar sign, no comma and no decimal point, with cents in a separate box to the right of a vertical
line, so OCR reads `150 | 00` as `15000` or `150 00`. The shaded supplemental line *does* use a decimal point. Ledgers show credits as
`(45.00)`, `-45.00`, `45.00-` or `45.00 CR`. Spanish-language clinics in Mexico and much of Latin America use `$1.250,00`; Texas clinics
serving Spanish speakers usually print US format. A running-balance column is cumulative and must never be summed.

### 1.3 Authorship and voice
A single ED visit carries the triage nurse, the physician (sometimes "scribed for"), the radiologist and the discharge nurse. Therapy notes
carry the PT, the PTA and a co-signature. Intake forms are in the patient's own hand. Per D-040 the tool does not label speakers; the generator
should still produce these mixed voices ("Pt states", "wife reports", "per EMS") so the excerpt carries them.

### 1.4 One visit, several bills
An ED visit produces a facility bill (UB-04), an emergency-physician bill (CMS-1500), and a radiologist bill (CMS-1500 with modifier 26) for
the same date. Surgery adds surgeon, assistant, anesthesia, facility and implant lines. These are **not duplicates**; a dedupe that keys on
date plus amount, or date plus provider name, will wrongly merge or wrongly keep them. A true duplicate is the same bill reproduced twice
(e.g., once in the provider's production and again as an attachment to the §18.001 affidavit).

---

## 2. Emergency department note

**Fields.** Arrival date/time; mode of arrival (EMS, private vehicle); triage block (ESI level, vitals, pain score, triage nurse narrative);
chief complaint (often in the patient's words, with duration); HPI (mechanism, onset, OPQRST / OLD CARTS elements); ROS; PMH/PSH, meds,
allergies, social history; physical exam; results (labs, imaging with preliminary reads); MDM (differential, ED course, reassessments);
clinical impression / diagnoses; disposition (discharged, admitted, transferred) with follow-up and return precautions; attestation and
electronic signature with timestamp.

**Typical wording.** "Restrained driver in a rear-end MVC at approx 35 mph, + airbag deployment, ambulatory at scene." "Denies LOC, denies
head strike." "Pain 8/10." "ROS: all other systems reviewed and negative." "CT C-spine: no acute fracture (prelim)." "Dx: cervical strain,
initial encounter." "Dispo: home, f/u with PCP in 3 to 5 days, return for worsening." The ED note carries **no charges**; charges arrive on
the UB-04 and CMS-1500.

**Extraction traps.**
- Midnight rollover: arrival 23:48, physician exam 00:31 the next calendar day; the visit date is the arrival date.
- Templated negatives ("all other systems negative") sit next to positives; a negation scope error drops a finding.
- Copy-forward PMH ("hx chronic low back pain") is a pre-existing-condition flag the adjuster will use.
- Triage pain score and post-medication pain score differ in the same note.
- Preliminary ED read versus the radiologist's final read can disagree; the final report is the authority.
- "Scribed for Dr. X by Y" and nurse addenda are different authors within one document.

**Sources.**
- EMRA, *Medical Student Documentation* (ED note template: CC, HPI, PMH, exam, MDM, ED course, disposition): https://www.emra.org/be-involved/committees/education-committee/medical-student-documentation — search summary only (page 404 when fetched).
- IEM Student, *Documentation*: https://iem-student.org/documentation/ — search summary; takeaway: review triage notes and vitals before writing, CC ideally in the patient's words, mnemonics OLD CARS / OPQRST for HPI.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - NOT A REAL PATIENT
Quillfeather Regional Medical Center - Emergency Department        MRN: SYN-ED-40417
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOB: 03/09/1991
Arrival: 05/14/2026 23:48   Mode: EMS   ESI: 3
TRIAGE (RN Tamsin Brook, SYNTHETIC): BP 142/88 HR 96 RR 18 SpO2 98% Pain 8/10.
  Pt states "the truck hit me from behind and my neck snapped forward."
PHYSICIAN NOTE (Dr. Ilario Fenwick, SYNTHETIC)  Seen: 05/15/2026 00:31
CC: Neck pain x 1 hour.
HPI: Restrained driver, rear-end MVC, + airbag. Denies LOC. Reports tingling R hand.
PMH: Low back pain 2023, resolved per pt.
ROS: All other systems reviewed and negative.
EXAM: TTP C5-C7 paraspinals, no midline step-off. Grip 4/5 R.
RESULTS: CT cervical spine w/o contrast - no acute fracture (prelim, see final).
MDM: Strain vs radiculopathy. Toradol 30 mg IM. Reassessed 01:40, pain 5/10.
IMPRESSION: Cervical strain, initial encounter (S16.1XXA).
DISPO: Discharged 02:05 05/15/2026. F/U PCP 3-5 days. Return if weakness worsens.
Electronically signed 05/15/2026 03:12
```

---

## 3. Physical therapy daily note (SOAP)

**Fields.** Date; visit number against plan ("Visit 7 of 24"); authorization/referral; time in and time out; S (patient report, NPRS pain
0-10, function, home exercise compliance); O (ROM in degrees, MMT grades, special tests, gait); interventions table with CPT, minutes and
units; total timed minutes and total treatment minutes; A (progress toward goals, tolerance); P (frequency and duration, next visit focus);
signature with credential (PT, PTA, DPT) and co-signature when a PTA treats.

**Typical wording.** "Pt reports neck pain 5/10, improved from 7/10 at eval." "Cervical rotation R 55 deg, L 60 deg." "97110 TherEx 25 min
(2 units); 97140 Manual 13 min (1 unit); 97014 E-stim unattended 15 min." "Total timed: 38 min. Total tx: 53 min." "Tolerated well. Continue
POC 2x/wk x 6 wks." Cancellations appear as a note with no treatment: "Pt cancelled - no transportation." Charges usually do **not** appear
on the note; they appear on the CMS-1500 or ledger as units times a fee.

**Extraction traps.**
- Timed codes bill in 15-minute units under the 8-minute rule; minutes are not dollars and units are not visits.
- "Visit 7 of 24" states the plan, not the count delivered; the adjuster compares planned versus actual.
- Cancelled or no-show entries are dated documents that are **not** encounters, but they may state the reason for a gap.
- Identical copy-forward text across visits (a known audit flag) reads as "cloned notes" to the defense.
- Re-evaluation and discharge summaries restate earlier values; extracting them as new measurements double counts.

**Sources.**
- Colorado HCPF Bulletin B1900436 (timed-minute totals across codes, e.g. 40 minutes = 3 units): https://hcpf.colorado.gov/sites/hcpf/files/Bulletin_1019_B1900436.pdf — search summary.
- AAPC compliance article on therapist signatures and documented time after an OIG audit: https://aapc.com/codes/scc_articles/article_pdf/47/compliance-forget-your-john-hancock-and-you-could-be-out-thousands-41142 — search summary.
- WebPT, *SOAP note tips for PTs*: https://www.webpt.com/blog/soap-note-tips-for-pts-plus-examples — search result, not opened. Assumption: SOAP order and fields above match common PT EMR output.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Larkspur Hollow Physical Therapy (SYNTHETIC)        Daily Note        Visit 2 of 12
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date: 06/10/2026   In 09:02 Out 09:55
S: Pt reports neck pain 5/10 (7/10 at eval 05/27/2026). Still wakes at night.
O: Cerv rot R 55 deg / L 60 deg. Grip R 4/5.
Interventions:  97110 TherEx  25 min  2u
                97140 Manual  13 min  1u
                97014 E-stim  15 min  (untimed)
Total timed 38 min / Total tx 53 min
A: Tolerated well. Progressing toward goal of 70 deg rotation.
P: Continue POC 2x/wk x 6 wks.
Signed: Wren Abernathy, PTA (SYNTHETIC)   Co-signed: Odalys Kerr, DPT (SYNTHETIC) 06/11/2026
--
06/12/2026  Pt cancelled - no transportation. Rescheduled 06/15/2026.
```
(Units follow the CMS total-time 8-minute rule: 38 timed minutes = 3 units, the extra unit going to the code with more minutes. The AMA
per-code method gives the same 2 + 1 here. Visit 1 was the 05/27/2026 evaluation; 2x/wk x 6 wks = 12 planned visits.)

---

## 4. Chiropractic daily note and travel card

**Fields.** Date; subjective complaint with pain scale (VAS/NPRS) and functional change since last visit; objective exam documenting the
PART elements (Pain/tenderness, Asymmetry/misalignment, Range-of-motion abnormality, Tissue/tone change) at specific spinal levels;
segments adjusted (e.g., C5, C6, L4) and technique; modalities (97012 mechanical traction, 97014 e-stim, 97010 hot/cold); CPT for
manipulation (98940 one to two regions, 98941 three to four, 98942 five, 98943 extraspinal); assessment of progress; plan and visit
frequency; provider signature. Many PI chiropractic offices also keep a **travel card** (one row per visit with checkboxes for regions and
modalities), which arrives as a scanned grid.

**Typical wording.** "Pt states neck 6/10, better than last visit." "TTP and hypertonicity bilat C4-C6, ROM flex 35 deg." "Adjusted C5, C6,
T4, L5 - diversified." "98941, 97014, 97010." "Pt responding favorably, continue 3x/wk." Fee slips say "Adjustment 3-4 regions $85.00" -
which may be a fee schedule **rate** or a charge for that visit depending on whether a date of service is attached.

**Extraction traps.**
- Medicare guidance requires the exact segment, not just a region; PI notes often list both. Do not count segments as visits.
- "Same as last visit", "SALV", or identical text across weeks is the cloned-note pattern adjusters attack.
- Travel-card checkmarks are OCR-hostile (see section 14); a missed checkmark loses a modality, a stray mark invents one.
- Percent-improvement statements ("50% better") are patient report, not an objective measure.
- Post-visit narrative reports written for the attorney are supplemental reports, not daily notes; their date is the letter date.

**Sources.**
- Noridian JF Part B, *Chiropractic Documentation Guidelines - Initial vs Subsequent Visits*: https://med.noridianmedicare.com/web/jfb/specialties/chiropractic/documentation-guidelines — **opened**. Takeaway: subsequent-visit notes need updated history, exam supporting the subluxation, assessment of progress, the exact segment treated, and date-specific (not cloned) findings.
- CMS MLN, *Chiropractic Services* compliance tip: https://www.cms.gov/training-education/medicare-learning-networkr-mln/compliance/medicare-provider-compliance-tips/chiropractic-services — search summary; PART acronym and AT modifier for 98940-98942.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Brightwater Spine & Wellness (SYNTHETIC)         Daily Note
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   DOS: 06/03/2026   Visit #4
S: Neck 6/10, low back 4/10. Pt states "about 50% better since I started."
O: TTP + hypertonicity bilat C4-C6. Cerv flex 35 deg (norm 50). Asym: R high shoulder.
Adjusted: C5, C6, T4, L5 (diversified).  Modalities: 97014 e-stim 15 min, 97010 cold pack.
CPT: 98941, 97014, 97010
A: Improving. P: Daily through 06/05, then 3x/wk x 3 wks, re-exam 06/24/2026.
Dr. Corvin Ashdown, DC (SYNTHETIC)
--- Travel card (scanned) ---
DATE    | C | T | L | ES | H/C | TR
06/01   | x | x | x | x  |  x  |
06/02   | x | x | x | x  |  x  |
06/03   | x | x | x | x  |  x  |
```
(Visit #1 was the new-patient exam on 05/29/2026, the date the intake in section 14 is signed; it was billed on an earlier claim not shown.
Visits 2-4 are the three consecutive days on the travel card and on the CMS-1500 in section 8. C/T/L = regions adjusted, ES = 97014,
H/C = 97010 hot/cold pack.)

---

## 5. Radiology report (x-ray, CT, MRI)

**Fields.** Exam name and modality; exam date/time; accession number; ordering clinician; clinical indication/history; technique (contrast,
sequences); comparison (prior studies, or "None"); findings by structure; impression (most important first); recommendations; reading
radiologist and signature date/time; preliminary versus final status; addenda.

**Typical wording.** "INDICATION: MVC 05/14/2026, neck pain, R arm paresthesia." "COMPARISON: None." / "COMPARISON: MRI 08/2023." "C5-6: disc
osteophyte complex with mild foraminal narrowing." "Straightening of the normal cervical lordosis, which may be positional or reflect muscle
spasm." "No acute fracture." "Chronic-appearing." "Clinical correlation recommended." Charges appear separately: a technical (facility) bill
and a professional (radiologist, modifier 26) bill.

**Extraction traps.**
- Indication text is the ordering clinician's statement (often including the mechanism), not a finding by the radiologist.
- "Comparison: MRI 08/2023" reveals prior imaging - a pre-existing flag - even when the findings section is silent about it.
- Hedges ("may represent", "cannot be excluded", "likely chronic", "age-indeterminate", "degenerative") are the language adjusters quote.
- Exam date, signed date and addendum date differ; an addendum can change the impression.
- The ED's preliminary read and the final report may disagree; keep both, cite each.

**Sources.**
- ACR *Practice Parameter for Communication of Diagnostic Imaging Findings* (rev. 2020): https://gravitas.acr.org/PPTS/GetDocumentView?docId=74 — **opened**, but only section headings rendered (II.B Components of the Report, II.C Final Report, II.D Preliminary Report). Takeaway from the search summary: a final report must be generated by the interpreting physician; follow-up studies suggested when appropriate.
- UF Radiology, *Components of a Report*: https://protocols.xray.ufl.edu/live_crr/prog/home/module-components_report.php — search summary; impression summarizes toward a diagnosis with the most important finding first.
- APS Medical Billing white paper (demographics, clinical information, body, impression): https://apsmedbill.com/whitepapers/documenting-complete-interpretation-report-diagnostic-radiology-services — search summary.
- Assumption: the INDICATION / TECHNIQUE / COMPARISON / FINDINGS / IMPRESSION order is near-universal; I did not read the ACR II.B body text.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Ferncastle Imaging Associates (SYNTHETIC)          Accession: SYN-ACC-77120
EXAM: MRI CERVICAL SPINE WITHOUT CONTRAST     Exam date: 06/18/2026 14:05
Patient: Delphine Okonkwo-Vale (SYNTHETIC)    Ordering: Dr. Corvin Ashdown, DC (SYNTHETIC)
INDICATION: MVC 05/14/2026. Neck pain, R hand tingling.
TECHNIQUE: Sagittal T1, T2, STIR; axial T2.
COMPARISON: CT cervical spine 05/15/2026 (Quillfeather Regional ED).
FINDINGS: Straightening of the cervical lordosis, which may be positional or reflect spasm.
  C5-6: 3 mm posterior disc protrusion with mild R foraminal narrowing. Mild disc desiccation.
  No fracture. No marrow edema.
IMPRESSION:
  1. C5-6 disc protrusion with mild right foraminal narrowing. Age of finding cannot be determined.
  2. Mild C5-6 desiccation, likely degenerative.
Electronically signed: Dr. Peregrine Holt (SYNTHETIC) 06/19/2026 08:22
ADDENDUM 06/20/2026: Comparison CT images reviewed; no change to impression.
```

---

## 6. Operative report

**Fields.** Patient and record identifiers; date of surgery (start/stop times); preoperative diagnosis; postoperative diagnosis;
procedure(s) performed (often with CPT in the billing copy); surgeon, assistant(s); anesthesia type and anesthesiologist; estimated blood
loss (EBL) or quantitative blood loss; fluids; specimens; drains; implants (manufacturer, lot - often stickers); complications; indications
(history and consent); findings; description of procedure; condition and disposition; dictation and transcription stamps.

**Typical wording.** "PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy secondary to C5-6 disc protrusion." "PROCEDURE: C5-6 anterior cervical
discectomy and fusion." "EBL: 50 mL." "SPECIMENS: Disc material to pathology." "COMPLICATIONS: None." "INDICATIONS: The patient is a 35-year-old
who reports neck and arm pain since a motor vehicle collision..." "D: 08/04/2026 T: 08/05/2026."

**Extraction traps.**
- The INDICATIONS paragraph repeats history, including the patient's account of the accident; it is not a causation opinion by the surgeon.
- Dictation (D:) and transcription (T:) dates follow the surgery date.
- Pre- and postoperative diagnoses can differ; the postoperative one reflects what was found.
- One surgery date generates several bills (surgeon, assistant with modifier 80/AS, anesthesia time units, facility/ASC, implants); not duplicates.
- "No EBL" or "no specimens" may simply be omitted (a Joint Commission FAQ says documentation is not required when there were none).

**Sources.**
- Joint Commission FAQ, *Operative report - timing and content* (ambulatory RC): https://www.jointcommission.org/standards/standard-faqs/ambulatory/record-of-care-treatment-and-services-rc/000002043 — search summary; report written or dictated immediately after the procedure; no requirement to document absent EBL or specimens.
- ACDIS Q&A on the immediate post-op note elements (surgeons, procedures, findings, EBL, specimens, post-op diagnosis): https://www.acdis.org/articles/qa-anesthesia-records-and-querying-blood-transfusion — search summary.
- CAMC post-op documentation regulatory table (pre- and post-op diagnosis, dates and times, surgeon and assistants): https://camc.org/sites/default/files/MedicalAffairs/Post%20op%20Documentation%20Regulatory%20Requirements.pdf — search summary.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Thistledown Surgical Center (SYNTHETIC)      OPERATIVE REPORT
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Date of surgery: 08/04/2026  07:42-09:15
PREOPERATIVE DIAGNOSIS: Right C6 radiculopathy, C5-6 disc protrusion.
POSTOPERATIVE DIAGNOSIS: Same.
PROCEDURE: C5-6 anterior cervical discectomy and fusion with interbody device.
SURGEON: Dr. Anselm Greaves (SYNTHETIC)   ASSISTANT: Juno Pell, PA-C (SYNTHETIC)
ANESTHESIA: General, Dr. Marisol Quint (SYNTHETIC)
EBL: 50 mL.  SPECIMENS: Disc material to pathology.  COMPLICATIONS: None.
IMPLANTS: Interbody cage, lot SYN-LOT-0042.
INDICATIONS: Pt reports neck and R arm pain since a motor vehicle collision on 05/14/2026,
  not improved with 12 weeks of therapy.
FINDINGS: Posterior disc protrusion compressing R C6 root.
D: 08/04/2026  T: 08/05/2026
```
(DELIBERATE: "12 weeks of therapy" is the surgeon's recital. From the PT evaluation (05/27/2026) to surgery (08/04/2026) is 69 days, about 9.9 weeks.
Expected: the excerpt is shown verbatim and attributed; no automatic flag (the product has no duration check); golden truth must never
state "12 weeks" as fact. An adjuster will count the weeks, so the paralegal should see both dates.)

---

## 7. Pharmacy dispensing log (patient Rx history printout)

**Fields.** Pharmacy name, address and NABP/NCPDP number; patient; date range and "printed on" date; per fill: fill date, Rx number, refill
number (0 = new, 1..n = refill) or refills remaining, drug name and strength, NDC (11-digit, 5-4-2), quantity, days supply, prescriber,
price (usual and customary), plan paid, patient paid/copay, status (filled, reversed, returned to stock).

**Typical wording.** "Fill 05/15/26 Rx 6604412 R0 CYCLOBENZAPRINE 10MG TAB Q 30 DS 10 Dr. Fenwick." "U&C $24.99 Plan $0.00 Pt pd $24.99."
"REVERSED 05/22/26." "Q/DS 90/30."

**Extraction traps.**
- Days supply is not quantity (90 tabs over 30 days).
- Fill date is not the prescribing visit; refills (R1, R2) are not new prescriptions and not encounters.
- Reversed or returned-to-stock claims appear as a line with the same Rx number; counting them inflates both meds and money.
- U&C price, plan paid and patient paid are three different numbers on one line; which one is a "charge" for a demand is a legal choice
  the tool must not make (route to notes unless the record states a charge).
- NDC formats vary (10-digit hyphenated 4-4-2/5-3-2/5-4-1 vs 11-digit); generic substitution changes the drug name between fills.

**Sources.**
- CVS Caremark receipt requirements via NYC PBA (minimum fields: NDC, fill date, metric quantity, total charge, days supply, pharmacy NABP; days supply is not quantity): https://www.nycpba.org/media/2706/caremark.pdf — search summary.
- OPM FEHB data attachment (refill number: 0 for new): https://piv.opm.gov/healthcare-insurance/carriers/fehb/2007/2007-09attachment2.pdf — search summary.
- RedSail NRx help, *Prescription Record* (Rx number, refills remaining, NDC, Q/DS): https://hub.redsailtechnologies.com/documents/RS/NRX/NRx%20Help%20Center/Set_Up_Store_Control_Options/Set_Up_Store_Control_Options/Prescription_Record,_Alphabetical_Order.htm — search summary.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Mossgate Community Pharmacy (SYNTHETIC)  NCPDP SYN-0000123   Printed on: 11/02/2026
Patient Rx History  05/01/2026 - 10/31/2026   Patient: Delphine Okonkwo-Vale (SYNTHETIC)
FILL DT   RX#        RF DRUG                      NDC            QTY DS  PRESCRIBER        U&C    PLAN   PT PD  STATUS
05/15/26  SYN6604412 0  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  FILLED
05/15/26  SYN6604413 0  NAPROXEN 500MG TAB        00000-0000-02   60 30  FENWICK I (SYN)  18.40  0.00  18.40  FILLED
05/25/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-01   30 10  FENWICK I (SYN)  24.99  0.00  24.99  REVERSED 05/26/26
06/02/26  SYN6604412 1  CYCLOBENZAPRINE 10MG TAB  00000-0000-03   30 10  FENWICK I (SYN)  21.50  0.00  21.50  FILLED
```

---

## 8. CMS-1500 (02/12) professional claim

**Fields (NUCC numbering).** 1a insured ID; 2 patient name; 3 DOB (8-digit) and sex; 10a-c condition related to employment / **auto accident
(with state)** / other accident; 11 insured's policy; 14 date of current illness or injury with qualifier (431 onset); 17 referring provider;
21 ICD indicator (0 = ICD-10) and diagnoses A-L; 24A dates of service From/To; 24B place of service; 24D CPT/HCPCS with up to four modifiers;
24E diagnosis pointer (letters); 24F $charges; 24G days or units; 24J rendering provider NPI; 25 federal tax ID; 28 total charge; 29 amount
paid; 30 reserved for NUCC use (no balance-due box on 02/12); 31 signature and date; 32 service facility; 33 billing provider.

**Typical wording and number format.** 24F "is the total billed amount for each service line": dollars right-justified left of a vertical
line, cents to the right, no dollar sign, comma or decimal point. Shaded supplemental lines above each service line hold NDC and other data
and *do* use a decimal point (e.g., `1000.00`). Item 28 is the total of all 24F lines. Item 29 is money paid by patient or other payers.

**Extraction traps.**
- `150 | 00` OCRs as `15000` ($15,000) or `150 00`; the decimal is implied by the box, not printed.
- 24A From/To with 24G = 10 means ten consecutive days on one line; one line is not one visit (NUCC: days must equal units).
- 24F is the line total (units times fee), not a per-unit rate; a per-unit figure must not be read from it.
- Item 14 is the injury/onset date and Item 31 is the signature date: neither is a service date.
- Item 28 can disagree with the sum of lines (data entry), or a claim may run to a second page with its own lines; sum lines in code and
  compare to Item 28 rather than trusting either.
- 10b "Auto accident? YES  Place (State) TX" is a useful corroborating checkbox and an OCR checkbox trap.

**Sources.**
- NUCC, *1500 Health Insurance Claim Form Reference Instruction Manual for Form Version 02/12*, Version 8.0 (7/20): https://www.nucc.org/images/stories/PDF/1500_claim_form_instruction_manual_2020_07-v8.pdf — **opened** (text extracted locally). Takeaways: Items 14, 24A, 24F, 24G, 28, 29, 30 as stated above. Newer manual versions may exist (NUCC updates each July); field layout of the 02/12 form is unchanged.
- CMS MLN web-based training on the 1500 (lesson 5): https://cms.gov/Outreach-and-Education/MLN/WBT/MLN4462429-MLN-WBT-1500/1500/lesson05/02/index.html — search result, not opened.

**Specimen (SYNTHETIC), clean boxed form** (as printed; money boxes have no decimal point, cents sit right of the bar):
```
SYNTHETIC RECORD - HEALTH INSURANCE CLAIM FORM (1500) - ALL IDENTIFIERS FICTITIOUS
2. PATIENT'S NAME  OKONKWO-VALE, DELPHINE (SYNTHETIC)     3. DOB 03 | 09 | 1991  F
10b. AUTO ACCIDENT?  [X] YES  [ ] NO   PLACE (State) TX
14. DATE OF CURRENT ILLNESS  05 | 14 | 26   QUAL 431
21. ICD Ind 0   A. S13.4XXA   B. M54.12
24. A FROM   A TO     B POS  D CPT/HCPCS  MOD   E PTR  F $CHARGES   G UNITS  J NPI
    060126   060126   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060226   060226   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060326   060326   11     98941              AB     85 | 00       1      SYN-NPI-0001
    060126   060326   11     97014              A      90 | 00       3      SYN-NPI-0001
    060126   060326   11     97010              A      45 | 00       3      SYN-NPI-0001
25. FED TAX ID  SYN-TIN-0001     28. TOTAL CHARGE  390 | 00     29. AMOUNT PAID  0 | 00
31. SIGNATURE  Dr. Corvin Ashdown, DC (SYNTHETIC)  DATE 06/30/26
33. BILLING PROVIDER  Brightwater Spine & Wellness (SYNTHETIC)  555-0142
```
(Lines 4-5 group 06/01 to 06/03: three consecutive days, 3 units, each matching the travel card's ES and H/C marks on all three days in
section 4; $30.00 and $15.00 per day. Lines 1-3 bill the same code one line per day, which NUCC also allows. MOD is blank; AB and A are
diagnosis pointers in 24E. Line sum 85 + 85 + 85 + 90 + 45 = 390 = Item 28. Item 14 is the injury date and Item 31 the signature date;
neither is a visit.)

**Specimen (SYNTHETIC), the same claim as OCR text** (what a scanned copy returns; truth beside each money string):
```
SYNTHETIC RECORD - OCR OF SCANNED 1500 - ALL IDENTIFIERS FICTITIOUS
24. 060126 060126 11 98941 AB 8500 1 SYN-NPI-0001         <- truth 85.00 (not 8,500.00)
    060226 060226 11 98941 AB 85 00 1 SYN-NPI-0001        <- truth 85.00 (bar dropped, space kept)
    O60326 060326 11 98941 AB 85|00 1 SYN-NPI-0001        <- truth 85.00; O for 0 in the date
    060126 060326 11 97014 A 9000 3 SYN-NPI-0001          <- truth 90.00 (not 9,000.00)
    060126 060326 11 97010 A 45 OO 3 SYN-NPI-0001         <- truth 45.00; O for 0 in the cents
28. TOTAL CHARGE 39000   29. AMOUNT PAID 0 00             <- truth 390.00 and 0.00
```
(Expected tool behavior: money in 24F and Items 28-29 is parsed as implied-cents in code; the line sum is compared with Item 28 in code;
every OCR-derived amount and date goes to review with the page image. A parser that reads `8500` as dollars bills $8,500 per adjustment.)

---

## 9. UB-04 (CMS-1450) institutional claim

**Fields (form locators).** FL 1 provider; 3a patient control number, 3b medical record number; **FL 4 type of bill** (4-digit with leading zero,
e.g. 0131 hospital outpatient); **FL 6 statement covers period** From/Through; 8-11 patient name and demographics; 12-13 admission date/hour;
14 admission type; 15 source; 17 discharge status; 31-36 occurrence codes and dates (accident codes 01-06, see traps); 39-41 value codes; **FL 42
revenue code** (4-digit, e.g. 0450 emergency room, 0320 x-ray, 0350 CT, 0610 MRI, 0250 pharmacy, 0636 drugs requiring detailed coding);
43 description (and NDC); **FL 44 HCPCS / accommodation rate / HIPPS code**; 45 service date; 46 service units; **47 total charges** (per
line, plus the total after the last line); **48 non-covered charges**; 50 payer; 67 principal diagnosis and 67A-Q other diagnoses; 72
external cause of injury codes; 74 principal procedure; 76 attending provider; 80 remarks.

**Typical wording.** Line 23 carries revenue code `0001` = total charges (paper claims), with the **creation date** in FL 45 of that line
(unverified: common convention, not in the RI guide; NUBC manual not opened). "PAGE 1 OF 2" on multi-page claims. FL 44 holds a per-day accommodation rate on inpatient room lines (e.g., `1850.00`) and a HCPCS code on
outpatient lines.

**Extraction traps.**
- Summing every amount in FL 47 includes the 0001 total line and doubles the bill.
- FL 44 on room lines is a **rate**; FL 47 on the same line is the charge (rate times days). Classic rate-vs-charge confusion (D-042).
- FL 45 on the total line is the claim creation date (unverified convention), not a service date.
- Occurrence codes 01-06 all carry an accident date: 01 auto accident (current NUBC wording reported as accident/medical coverage), 02
  no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim. A PI claim may
  carry any of them (01 or 03 most often). Extraction treats every one as the accident date, never a service date; packets vary the code.
- On inpatient claims the room line has a rate in FL 44, days in FL 46 and often no FL 45 date; the stay dates come from FL 6 and FL 12.
- On multi-page claims the total appears only on the last page.
- FL 48 non-covered is not an adjustment by the provider; it is still a charge the payer did not cover.
- Payer guides disagree on whether Medicare's FL 47 total excludes non-covered charges; compute from lines and keep both.

**Sources.**
- Rhode Island EOHHS, *UB-04 Instructions*: https://eohhs.ri.gov/sites/g/files/xkgbur226/files/2021-03/ub04_instructions.pdf — **opened** (text extracted). Takeaways: FL 4 four-digit with leading zero; FL 6 MMDDYY; FL 42 enter "0001" after last revenue code for the total in column 47 (paper only); FL 47 per-line total plus grand total; FL 48 amount not covered by primary payer.
- NUBC, *Official UB-04 Data Specifications Manual 2024* (table of contents; FL 47 p.180, FL 48 p.181): https://www.nubc.org/system/files/media/file/2024/04/TOC%20FOR%20NUBC%20SITE%202024%20UB04%20Manual.pdf — search summary; the full manual is licensed.
- McGraw-Hill chapter summary on FL 47/48 Medicare treatment: https://highered.mheducation.com/sites/0073520896/student_view0/chapter12/chapter_summary.html — search summary.
- HL7 v2.4 NUBC occurrence-code vocabulary: https://build.fhir.org/ig/frankoemig/hl7.v2.terminology.v24/CodeSystem-nubc-OccurrenceCode-cs.json.html — **opened**. Takeaway: 01 auto accident, 02 no-fault insurance involved, 03 accident/tort liability, 04 accident/employment related, 05 other accident, 06 crime victim, 11 onset of symptoms. This is an older HL7 rendering; the current NUBC label for 01 may differ.
- Assumption: FL 44 title "HCPCS/Rate/HIPPS code" and the creation-date-on-line-23 convention are from prior knowledge, confirmed only by the T-078 reviewer's working knowledge; verify against the NUBC manual before quoting.

**Specimen 1 (SYNTHETIC), outpatient ED claim.**
```
SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Quillfeather Regional Medical Center (SYNTHETIC)   3a SYN-PCN-5521  3b SYN-ED-40417  4 0131
6 STATEMENT COVERS PERIOD  FROM 051426  THROUGH 051526
8 OKONKWO-VALE, DELPHINE (SYNTHETIC)   12 ADMISSION 051426  13 HR 23
31 OCCURRENCE  CODE 01  DATE 051426
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0450    EMERGENCY ROOM LVL 4          99284          051426        1          2,410.00
0350    CT CERVICAL SPINE W/O         72125          051526        1          3,185.00
0636    KETOROLAC INJ 15MG            J1885          051526        2             96.00
0250    PHARMACY GENERAL                             051526        1             38.50           38.50
0001    TOTAL                                        051826                   5,729.50           38.50
67 S16.1XXA   72 ECI V43.52XA   76 ATTENDING Dr. Ilario Fenwick (SYNTHETIC)
PAGE 1 OF 1
```
(The 0001 line repeats the sum; 051826 on that line is the creation date, an unverified convention. Occurrence code 01.)

**Specimen 2 (SYNTHETIC), inpatient claim with a room rate on the charge line** (a different synthetic patient):
```
SYNTHETIC RECORD - UB-04 - ALL IDENTIFIERS FICTITIOUS
1 Saltmarrow General Hospital (SYNTHETIC)   3a SYN-PCN-7730  3b SYN-IP-11902  4 0111
6 STATEMENT COVERS PERIOD  FROM 091526  THROUGH 091826
8 TELFAIR-NKEMELU, AMBROSE (SYNTHETIC)   12 ADMISSION 091526  13 HR 02  14 TYPE 1  17 STAT 01
31 OCCURRENCE  CODE 03  DATE 091426
42 REV  43 DESCRIPTION              44 HCPCS/RATE  45 SERV DATE  46 UNITS  47 TOTAL CHARGES  48 NON-COVERED
0120    ROOM & BOARD SEMI-PVT         1,850.00                     3          5,550.00
0450    EMERGENCY ROOM                               091526        1          1,975.00
0250    PHARMACY                                     091526       14            412.75
0300    LABORATORY                                   091526        6            688.00
0320    DX X-RAY                                     091526        2            540.00
0001    TOTAL                                        092226                   9,165.75
67 S42.201A   72 ECI V43.52XA   76 ATTENDING Dr. Rosamund Achterberg (SYNTHETIC)
PAGE 1 OF 1
```
(Room line: FL 44 rate 1,850.00 x FL 46 3 days = FL 47 5,550.00. Only FL 47 is a charge; 1,850.00 is a rate. A naive sum of every money
figure adds the rate and the 0001 line and reports 20,181.50 instead of 9,165.75. Admitted 09/15, discharged 09/18 = 3 room days.
Occurrence code 03, not 01: 09/14/2026 is the accident date, not a service date. 092226 on the 0001 line is the creation date.)

---

## 10. Itemized provider ledger / statement

**Fields.** Provider name and address; patient and account number; statement date; prior balance / balance forward; per line: date of
service, posting date, CPT or internal code, description, charge, payment, adjustment, running balance; totals block (total charges, total
payments, total adjustments, balance due); notes ("Account on LOP hold", "Sent to attorney").

**Typical wording.** CMS's consumer guide names the parts as total charges, allowed amount, adjustments, insurance payment, patient payment,
and balance due/patient responsibility. Real ledgers add: "Contractual adj", "W/O", "Courtesy disc", "Atty reduction", "Bal fwd", credits in
parentheses or with a trailing minus, "Pmt - Ck #SYN-1043". Hospital consumer statements often show only a total; the itemized version must be
requested.

**Extraction traps.**
- Running balance is cumulative; summing it multiplies the bill.
- Balance forward from a prior statement re-counts earlier charges if two statements are both in the packet.
- Posting date versus date of service: a charge posted 06/30 for a 06/03 visit.
- Reversals ("Void", "Reverse chg") paired with a re-bill on a later line.
- Fee-schedule summaries ("Office visit est. $150.00 per visit") look like charge lines but carry no date of service (rate, not charge).
- An attorney reduction recorded as an adjustment after settlement talks is a negotiated number, not a billed charge.

**Sources.**
- CMS, *How to read your medical bill*: https://www.cms.gov/initiatives/your-patient-rights/medical-bill-rights/get-help/medical-bill-guides-resources/how-read-your-medical-bill — **opened**. Takeaway: standard parts are total charges, allowed amount, adjustments, insurance payment, patient payment, balance due.
- Resolve Medical Bills, *Itemized Hospital Bills*: https://www.resolvemedicalbills.com/guides/itemized-hospital-bill — search summary; itemized bill is sent only on request and lists dates, codes and per-service prices.
- Texas CPRC §18.001 (affidavit must include an itemized statement of the service and charge): https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm — search summary; see also research/texas-pi-notes.md.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Larkspur Hollow Physical Therapy (SYNTHETIC)     ITEMIZED STATEMENT     Statement date: 07/31/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Acct: SYN-PT-2207   Financial class: LOP
DOS       POSTED    CODE   DESCRIPTION                  CHARGES   PAYMENTS   ADJ        BALANCE
05/27/26  05/28/26  97162  PT eval moderate complexity   210.00                         210.00
06/10/26  06/11/26  97110  Therapeutic exercise x2       130.00                         340.00
06/10/26  06/11/26  97140  Manual therapy x1              70.00                         410.00
06/10/26  06/11/26  97014  E-stim unattended              35.00                         445.00
06/10/26  06/30/26  97140  Manual therapy x1 VOID        (70.00)                        375.00
06/10/26  06/30/26  97140  Manual therapy x1              70.00                         445.00
07/15/26  07/15/26  ADJ    Courtesy discount                                 45.00-     400.00
                     TOTAL CHARGES 445.00  TOTAL PMTS 0.00  TOTAL ADJ (45.00)  BALANCE DUE 400.00
Fee schedule: Therapeutic exercise $65.00 per unit. Account held per letter of protection.
```
(DELIBERATE: no payment or contractual adjustment is posted, although the EOB in section 11 (processed 07/22/2026) shows plan paid 16.00 and
CO-45/CO-97 reductions for DOS 06/10/26. Expected: billing analysis cites both documents' figures and flags the ledger-vs-EOB mismatch for
review; the tool never picks paid or incurred. The $65.00 fee-schedule line has no date of service: a rate, not a charge.)

---

## 11. Explanation of Benefits (EOB) / remittance

**Fields.** "THIS IS NOT A BILL"; member name and ID; claim number; provider; processed date; per service: date of service, service
description or code, amount billed, network discount / not covered, allowed amount, deductible, copay, coinsurance, plan paid, patient
responsibility ("You may owe"); CARC/RARC codes with group code (CO contractual obligation, PR patient responsibility, OA other).

**Typical wording.** "Amount billed $410.00 - Network discount $162.40 = Allowed $247.60." "Deductible applied $100.00; Coinsurance 20%
$29.52; Plan paid $118.08; You may owe $129.52." "CO-45: charge exceeds fee schedule/maximum allowable." "PR-1 deductible, PR-2 coinsurance,
PR-3 copay."

**Extraction traps.**
- The EOB's "amount billed" restates the provider's charge; counting both the bill and the EOB double counts.
- The processed/paid date is not a service date.
- "You may owe" is not what the patient paid; for Texas paid-or-incurred analysis (out of scope for the tool) the numbers matter, so keep them in notes with citations.
- Group code decides who owes: CO amounts are written off by a contracted provider, PR amounts are the patient's.
- Health-plan EOBs in a PI file often signal a subrogation lien by the health plan.

**Sources.**
- Noridian JF-A, *MSP Calculation Examples on EOBs*: https://med.noridianmedicare.com/web/jfa/topics/msp/calculation-examples-eob — **opened**. Takeaway: billed minus total CARC amount equals allowed; allowed minus paid equals patient responsibility; examples with CARC CO-16 and a network discount.
- D3RX glossary, *CO (Contractual Obligation)*: https://d3rx.com/glossary/co-contractual-obligation — search summary; billed minus allowed is a contractual write-off the participating provider cannot balance-bill.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - THIS IS NOT A BILL
Quoinmere Mutual Health Plan (SYNTHETIC)   Explanation of Benefits   Processed 07/22/2026
Member: Delphine Okonkwo-Vale (SYNTHETIC)  ID SYN-MBR-88231  Claim SYN-CLM-0091
Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)
DOS       SERVICE  BILLED   DISCOUNT  ALLOWED  DEDUCT  COINS   PLAN PAID  YOU MAY OWE  CODES
06/10/26  97110    130.00    52.00     78.00    78.00    0.00     0.00      78.00     PR-1, CO-45
06/10/26  97140     70.00    28.00     42.00    22.00    4.00    16.00      26.00     PR-1, PR-2, CO-45
06/10/26  97014     35.00    35.00      0.00     0.00    0.00     0.00       0.00     CO-97
TOTAL              235.00   115.00    120.00   100.00    4.00    16.00     104.00
CO-97: payment included in allowance for another service.
```

---

## 12. Letter of protection (LOP) and lien letters

**Fields.** Law-firm letterhead; letter date; addressee (provider billing office); "Re:" block with client name, DOB, date of injury, sometimes
claim number; statement of representation; request that the provider treat and defer collection; promise to protect the bill from any
settlement or judgment; statement that the client remains responsible if the recovery is insufficient; request for records, itemized bill
and §18.001 affidavit; attorney signature; client acknowledgement and signature. Related documents: provider-side lien notice or
"Assignment and Authorization" signed by the patient at intake; hospital lien notice; reduction letters ("accept $X in full satisfaction").

**Typical wording.** "Please be advised this firm represents ___ for injuries sustained on ___." "We will protect your outstanding charges
from any recovery." "This letter does not relieve our client of responsibility for the balance." "Please forward complete records and an
itemized statement of charges." Provider intake LOPs add: the provider will not send the account to collections while the claim is pending,
a continuing lien on any recovery, a direction to pay, and duties to notify the provider before funds are disbursed.

**Extraction traps.**
- The LOP is not a medical record: its accident narrative is the attorney's, and its dates (letter date, injury date) are not encounters.
- Amounts in an LOP or lien notice ("current balance $4,860.00") are asserted totals without dates of service; never charges (D-019).
- Reduction letters state negotiated numbers; they belong in internal notes only.
- Sources disagree on whether "LOP" and "lien" are interchangeable; the tool should keep the document's own words.

**Sources.**
- Jotform HIPAA intake packet with an embedded LOP (chiropractic, auto/slip-and-fall): https://hipaa.jotform.com/221364153684052 — **opened**. Takeaway: patient signs; provider defers payment and collections; direction to pay from settlement after fees and costs; continuing lien; patient remains responsible for any shortfall; notice duties before disbursement.
- ChartRequest, *Letters of Protection and Medical Liens*: https://www.chartrequest.com/articles/letters-of-protection-medical-records — search summary; argues LOP and lien are distinct.
- D Law Group, *What is a Letter of Protection or Personal Injury Lien?*: https://dlawgroup.com/letter-of-protection-personal-injury-lien/ — search summary; LOP can operate as a contract; patient owes the balance if the case is lost.
- Miller & Zois forms library (sample assignment/LOP and hold-harmless letters): https://www.millerandzois.com/professional-attorney-information-center/forms-and-letters-for-personal-injury-lawyers/ — search result, not opened.
- Assumption: Texas hospital liens (Property Code ch. 55) produce a separate filed notice; I did not open the statute for this card.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Harrowgate & Vey, PLLC (SYNTHETIC)     100 Example Row, Suite 5, Fernhollow, TX     555-0177
July 2, 2026
Billing Department, Larkspur Hollow Physical Therapy (SYNTHETIC)
Re: Our client Delphine Okonkwo-Vale (SYNTHETIC); Date of injury 05/14/2026
This firm represents the above client for injuries from a motor vehicle collision. We ask
that you continue treatment and defer collection while the claim is pending. We will
protect your reasonable charges from any settlement or judgment. This letter does not
relieve our client of responsibility for the balance. Please send complete records and an
itemized statement of charges with a business-records affidavit.
Current balance per your office: $445.00.
/s/ Ottoline Vey, Attorney (SYNTHETIC)
Acknowledged: Delphine Okonkwo-Vale (SYNTHETIC)  07/02/2026
```

---

## 13. Spanish-language clinic note

**Fields.** Same structure as an English clinic note under Spanish headings: *Fecha*; *Ficha de identificación* (name, age, sex);
*Motivo de consulta* (reason for visit, with duration); *Enfermedad actual* / *Padecimiento actual* (onset, course, current state);
*Antecedentes* (personales patológicos, no patológicos, quirúrgicos, alergias); *Signos vitales*; *Exploración física*; *Impresión
diagnóstica* / *Diagnóstico* (IDx); *Plan* (diagnostic: *estudios solicitados*; therapeutic: drug, dose, *vía oral (VO)*, frequency *c/8h*,
duration); *Pronóstico*; signature with *cédula profesional* (Mexico) or license.

**Typical wording.** "Paciente femenina de 35 años que acude por dolor cervical de 3 días de evolución posterior a choque vehicular por
alcance." "Refiere dolor 7/10, irradiado a brazo derecho." "Niega pérdida del estado de alerta." "A la exploración física: contractura
paravertebral cervical, dolor a la palpación C5-C7." "IDx: Esguince cervical grado I." "Plan: naproxeno 500 mg VO c/12h por 7 días,
reposo relativo, cita en 1 semana." "Consulta: $650.00" (charge) vs "Costo por sesión de terapia: $400.00" (rate).

**Extraction traps.**
- Day-first dates: `03/06/2026` is 3 June, not March 6. Written months: `14 de mayo de 2026`, `14-may-26`, `12-ago-2026`.
- `ago` is a month abbreviation (agosto); `hace 3 días` is "3 days ago" and is relative to the visit date, not a date.
- `refiere` (patient reports) and `niega` (denies) mark voice and negation; a translation must keep them.
- Decimal comma and dot thousands in Latin American notes (`$1.250,00`); US-based clinics usually print `$1,250.00`. Currency may be MXN.
- Mixed English/Spanish ("dolor de low back", "MRI solicitada") in border-region clinics.
- Per D-042 the excerpt is always the original Spanish; any translation is LLM output, labeled, judged, and never the cited excerpt.

**Sources.**
- Huli Practice, *Ejemplo Formato Historia Clínica* (Mexican clinical-history template: motivo de consulta, enfermedad actual, antecedentes, exploración, diagnóstico, plan): https://blog.hulipractice.com/content/files/2023/08/Ejemplo-Formato-Historia-Cli-nica.pdf — search summary.
- Universitat de Barcelona, *Estructura de una entrevista diagnóstica - Motivo de consulta y enfermedad actual*: https://diposit.ub.edu/items/77b3b1a7-0b60-48b7-850d-224ebebcb4e5/full — search summary; enfermedad actual covers onset, evolution and current state; impresión diagnóstica is the clinician's, not asked of the patient.
- AgendaPro, *Formato de Historia Clínica*: https://agendapro.com/blog/wp-content/uploads/sites/2/2026/03/Formato-de-Historia-Clinica.pdf — search summary; plan split into estudios solicitados and treatment with drug, dose, frequency, duration.
- Assumption: common phrasing above ("acude por", "de N días de evolución", "refiere", "niega", "c/8h", "VO") is from general clinical Spanish usage; sources are teaching templates, not a terminology standard.

**Specimen (SYNTHETIC).**
```
REGISTRO SINTÉTICO / SYNTHETIC RECORD
Consultorio Médico Peñaverde (SINTÉTICO)          Nota de consulta
Fecha: 17/05/2026
Paciente: Rosalba Itzel Marqueño (SINTÉTICO)   Edad: 41 años   Sexo: F
Motivo de consulta: Dolor de cuello de 3 días de evolución posterior a choque vehicular por alcance.
Enfermedad actual: Refiere dolor 7/10, irradiado a brazo derecho, que aumenta al girar la cabeza.
  Niega pérdida del estado de alerta. Niega antecedentes de dolor cervical.
Signos vitales: TA 130/85, FC 88.
Exploración física: Contractura paravertebral cervical. Dolor a la palpación C5-C7.
IDx: Esguince cervical grado I.
Plan: Naproxeno 500 mg VO c/12h por 7 días. Reposo relativo. Rx de columna cervical.
  Cita de control en 3 semanas (07/06/2026).
Consulta: $650.00     Costo por sesión de terapia física: $400.00
Dra. Itziar Orbezua Lanz (SINTÉTICO)
```
(`17/05/2026` is 17 May: unambiguous, day > 12. `07/06/2026` is **7 June 2026**, not July 6: both parts are 12 or less, so only the
day-first convention decides; it is 21 days after the visit, matching "en 3 semanas". The $650.00 is the visit charge; the $400.00 is a
per-session rate, not a charge.)

---

## 14. Scanned and handwritten intake forms (and OCR failure modes)

**Fields.** Patient demographics; date of injury; "How did the injury occur?" (free text); body diagram with marked pain areas; pain scale
0-10 (circled); symptom checkboxes (headache, dizziness, numbness); "Prior injuries / accidents / chiropractic care? Yes / No" with
explanation lines; current medications; employer and work status; "Who referred you?" (often an attorney); attorney name; insurance (auto,
health, MedPay/PIP); signature and date; sometimes an embedded LOP or assignment of benefits (section 12).

**Typical wording.** Handwriting, abbreviations and the patient's own words: "rear ended at light, neck + back hurt", "no prior", "Dr. told
me to come", "pain 7-8". Stamps: "RECEIVED", "SCANNED", Bates numbers; fax header on every page.

**OCR failure modes to reproduce.**
| Failure | Example (truth → OCR) | Consequence |
|---|---|---|
| Checkbox read as character or dropped | `[X] No` → `IX] No` or `No`; `[ ] Yes [X] No` → `Yes No` | Prior-injury answer lost or flipped - high stakes for pre-existing flags |
| Glyph confusion | `0/O`, `1/l/I/7`, `5/S`, `8/B`, `2/Z` | `05/14/26` → `O5/l4/26`; `$150` → `$I50` |
| Dropped or added decimal | `$1,250.00` → `$125000` or `$1,25000` | Amount off by 100x |
| Implied decimal (CMS-1500 boxes) | `150 \| 00` → `15000` | Same |
| Circled number | Pain scale `0 1 2 3 4 5 6 7 8 9 10` with 7 circled → all digits | Pain score lost |
| Strike-through and correction | `6/12` struck, `6/15` written above | Both dates extracted |
| Two-column / form-grid reading order | Left and right columns interleaved | Answers attached to the wrong question |
| Fax header and stamps | `11/03/2026 09:14 FROM: 555-0199 P.3/14` | Fax date read as a record date |
| Skew, blur, shadow, bleed-through | Phone photo of a form | Character error rate rises; Tesseract was weakest on blur and shadow in one study |
| Hidden or layered text in PDFs | Searchable PDF with an invisible text layer that differs from the image | Extracted text not visible to the human reviewer (D-042 hidden-text detection) |

**Sources.**
- *Compact Multimodal Language Models as Robust OCR Alternatives for Noisy Textual Clinical Reports* (arXiv 2511.13523): https://arxiv.org/html/2511.13523v1 — **opened**. Takeaway: on smartphone photos of printed clinical reports, Tesseract scored CER 0.189, WER 0.276 and numeric accuracy 0.756, worse than neural pipelines and small multimodal models; Tesseract struggled most with blur and shadows. (Cite by arXiv number; authors not recorded here.)
- Tesseract OCR mailing list, thread on reading "X" checkboxes: https://groups.google.com/g/tesseract-ocr/c/r9mVUg76iE0 — search summary; out-of-the-box quality is medium; form jargon needs training; one user got better results at 150 dpi than 600 dpi.
- ImageToTable blog, *Why AI reads handwriting but misses a ticked box*: https://imagetotable.ai/blog/how-ai-reads-handwritten-forms-checkboxes-to-excel — search summary (vendor); generic OCR has no character for a tick and skips or garbles it.
- Assumption: glyph confusions in the table are the standard OCR confusion set; I found no Tesseract-specific measurement of them.

**Specimen (SYNTHETIC)** — what the page shows, then what OCR returns:
```
SYNTHETIC RECORD
[PAGE IMAGE, described] Brightwater Spine & Wellness New Patient Intake. Handwritten in blue ink.
  Date of injury: 5/14/26.  How did it happen: "rear ended at red light, neck and back hurt."
  Pain today: 7 circled on a 0-10 line.  Prior injuries? [ ] Yes [X] No.
  Who referred you? "my lawyer - Vey".  Signed 5/29/26.  Fax header: 11/03/2026 09:14 P.2/9.
  Stamp: RECEIVED NOV 03 2026.
[OCR TEXT as extracted]
  11/O3/2026 O9:14 FROM 555-0199 P.2/9
  Date of injury: 5/l4/26
  How did it happen: rear ended at red Iight, neck and back hurt
  Pain today: 0 1 2 3 4 5 6 7 8 9 10
  Prior injuries? Yes IX] No
  Who referred you? my Iawyer - Vey
  Signed 5/29/2G
  RECEIVED NOV O3 2026
```
(The chosen pain score and the prior-injury answer are not recoverable from the OCR text alone; the item needs the page image and review.)

---

## 15. EMS patient care report (ambulance run report)

**Fields (NEMSIS v3 names in brackets).** Agency, unit and crew with certification levels; incident and run numbers; call times: PSAP call
(eTimes.01), unit notified (eTimes.03), en route (eTimes.05), arrived on scene (eTimes.06), arrived at patient (eTimes.07), left scene
(eTimes.09), arrived at destination (eTimes.11), transfer of care (eTimes.12); scene location type; patient demographics; chief complaint;
mechanism of injury and vehicle/scene description; several timed vital-sign sets (BP, HR, RR, SpO2, GCS, pain); assessment by body region;
treatments with times (spinal motion restriction, cold pack, medications); narrative (often in CHART or SOAP order); disposition: unit
disposition, patient evaluation/care, crew disposition, transport disposition (eDisposition.27-30); reason for refusal or release
(eDisposition.31); destination; patient or witness signature on a refusal; crew signatures.

**Typical wording.** "Dispatched for MVC with injuries." "Arrived to find pt sitting in driver seat, self-extricated, ambulatory at scene."
"Moderate rear-end damage to pt's vehicle, airbags deployed." "Pt c/o neck pain 7/10, denies LOC." "GCS 15." "Pt placed in position of
comfort, c-collar applied." Refusal: "Pt refused transport against medical advice. Risks explained incl. worsening injury and death. Pt
verbalized understanding, signed refusal." "Minor damage to rear bumper." The run report carries **no charges**; the bill is section 16.

**Extraction traps.**
- The service date is the call date. A call at 23:12 that reaches the ED at 23:47 and is signed after midnight still belongs to the call date.
- Eight timestamps for one encounter; the ED's own arrival time (section 2) can differ by a minute or two. That is not a conflict.
- Scene descriptions ("minor damage", "ambulatory at scene", "self-extricated") are the crew's observations, not the patient's report and not
  a medical finding. They are the defense's MIST language (D-018 causation lexicon; speaker is EMS).
- A refusal is a dated encounter with no transport. The next care date after a refusal decides the first-treatment gap.
- "Pt states" lines (history) sit beside crew observations in one narrative; the excerpt keeps both voices.
- Repeated vital sets: pain 7/10 at 23:24 and 5/10 at 23:40 are both true at their times.

**Sources.**
- NASEMSO, *EMS Time Duration Definitions* (2024-06-18): https://nemsis.org/wp-content/uploads/2024/06/NASEMSO_EMS_Time_Duration_Definitions-6-18-24.pdf — **opened** (text extracted). Takeaway: the eTimes.01-17 list and interval formulas (scene time = left scene minus arrived on scene).
- Montana DPHHS, *NEMSIS disposition guide*: https://dphhs.mt.gov/assets/publichealth/EMSTS/EMS/Disposition.pdf — **opened** (text extracted). Takeaway: eDisposition.27-31 (unit, patient evaluation/care, crew, transport disposition, reason for refusal/release); "patient evaluated and refused care" and "patient refused transport" values; "against medical advice" as a refusal reason.
- NEMSIS v3.5 *Requisite National Elements*: https://nemsis.org/wp-content/uploads/2025/01/NEMSIS-v3.5-Requisite-National-Elements-EMS-DataSet.pdf — search summary (the URL returned an HTML page to curl).
- Assumption: the narrative wording above is common EMS charting style; no Texas agency template was opened.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - PATIENT CARE REPORT - ALL IDENTIFIERS FICTITIOUS
Fernhollow County EMS (SYNTHETIC)   Unit: Medic 14   Incident SYN-INC-26-04471   Run SYN-RUN-0912
Date: 05/14/2026   PSAP 23:12  Notified 23:13  En route 23:14  On scene 23:21  At pt 23:22
                   Left scene 23:36  At dest 23:47  Transfer of care 23:52
Patient: Delphine Okonkwo-Vale (SYNTHETIC)  DOB 03/09/1991  F
CC: Neck pain.  MOI: MVC, rear-end, restrained driver, airbag deployed.
Scene: Moderate rear damage to pt vehicle. Pt self-extricated, ambulatory at scene.
VITALS  23:24  BP 148/90  HR 102  RR 18  SpO2 98%  GCS 15  Pain 7/10
        23:40  BP 142/88  HR 96   RR 18  SpO2 98%  GCS 15  Pain 6/10
NARRATIVE: Pt states "the truck hit me from behind." Denies LOC. C/o neck pain and
  tingling R hand. C-collar applied, cold pack to neck. Transported to Quillfeather
  Regional ED without incident.
DISPOSITION: Patient treated, transported by this EMS unit.
Crew: Hollis Brandvold, Paramedic (SYNTHETIC); Pia Strandquist, EMT (SYNTHETIC)
--- Refusal variant (another synthetic run, for packets that need it) ---
Date: 03/02/2026  On scene 16:05  Left scene 16:31
Scene: Minor damage to rear bumper. Pt ambulatory at scene, no visible injury.
Pt c/o mild neck stiffness. Pt refused transport against medical advice; risks explained.
DISPOSITION: Patient evaluated and refused care / refused transport.  Pt signature on file.
```
(Arrival at destination 23:47 here vs ED arrival 23:48 in section 2: same event, not a conflict. "Moderate rear damage" is the crew's
observation; "the truck hit me from behind" is the patient's.)

---

## 16. Ambulance invoice (base rate plus mileage)

**Fields.** Agency billing name and tax ID; invoice number, invoice date and run number; date of service; patient; pick-up and drop-off
(origin/destination modifier letters); level of service line (HCPCS A0427 ALS1 emergency, A0429 BLS emergency, etc.); mileage line (A0425,
units = loaded miles, fractional to the tenth); per-unit rate and line charge; supplies lines if itemized; total charges; payments (auto
PIP/MedPay, health plan); adjustments; balance due; "out of network" or balance-billing notice.

**Typical wording.** "A0427-SH ALS emergency transport, Level 1 ... 1,450.00." "A0425-SH Ground mileage 8.7 mi @ 22.50/mi ... 195.75."
"Total charges 1,645.75." "Balance due upon receipt." Origin/destination modifiers pair a pick-up letter with a drop-off letter (S = scene of
accident or acute event, H = hospital, R = residence), so a crash scene to ED trip is SH.

**Extraction traps.**
- The per-mile figure (22.50/mi) is a **rate**; only the extended line (195.75) and the stated total are charges (D-042 rate-vs-charge guard;
  miles x rate is recomputed in code).
- Units are miles with a decimal (8.7), not visits and not integers. A parser that drops the decimal bills 87 miles.
- Every trip is normally two lines (service + mileage) for one encounter; they are not two encounters.
- Only loaded miles (patient on board) are billable for Medicare; commercial and auto carriers vary.
- The invoice date and any statement date are not the service date; the run number ties the invoice to the run report (section 15).
- A balance-billing notice states an asserted balance without a service line (notes only, D-019).

**Sources.**
- CMS, *Medicare Claims Processing Manual*, ch. 15 *Ambulance*: https://www.cms.gov/Regulations-and-Guidance/Guidance/Manuals/downloads/clm104c15.pdf — **opened** (text extracted). Takeaways: origin/destination modifier letters (S = scene of accident or acute event, H = hospital, R = residence ...; first letter origin, second destination); A0425 ground mileage per mile, A0427 ALS1 emergency; generally two lines per trip; mileage reported in fractional units, rounded up to the nearest tenth for trips under 100 miles; mileage means loaded mileage.
- Noridian JE, *Ambulance Mileage*: https://med.noridianmedicare.com/web/jeb/specialties/ambulance/mileage — **opened**. Takeaway: only loaded miles are paid; round up to the tenth for 100 miles or less; leading zero below 1 mile; missing mileage defaults to 0.1.
- FAIR Health ground-ambulance brief (2023) via research/case-library-sources-v2.md P15 — search excerpt; most claim lines out of network.
- Assumption: the rates in the specimen are invented and do not reflect any fee schedule.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - AMBULANCE INVOICE - ALL IDENTIFIERS FICTITIOUS
Fernhollow County EMS Billing (SYNTHETIC)   TIN SYN-TIN-0440   Invoice SYN-INV-77310   Invoice date 05/29/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Run SYN-RUN-0912   DOS 05/14/2026
Pick-up: Scene (S)   Drop-off: Quillfeather Regional Medical Center (H)
CODE      DESCRIPTION                          UNITS   RATE       CHARGE
A0427-SH  ALS emergency transport, Level 1      1      1,450.00   1,450.00
A0425-SH  Ground mileage, loaded                8.7       22.50     195.75
                                          TOTAL CHARGES          1,645.75
PAYMENTS 0.00   ADJUSTMENTS 0.00   BALANCE DUE 1,645.75
Account noted: attorney representation, letter of protection requested.
```
(8.7 x 22.50 = 195.75; 1,450.00 + 195.75 = 1,645.75. 22.50 is a rate. 05/29/2026 is the invoice date, not a service date.)

---

## 17. Texas CPRC §18.001 billing affidavit and records cover page

**Fields.** Optional caption (cause number, court, parties) when filed; affiant's name and role: the person who provided the service or the
person in charge of records (custodian); provider name; patient; date-of-service range; sworn statements that the records were kept in the
regular course of business and made at or near the time, and that the services were necessary and the charges reasonable at the time and
place; for medical expenses, the amount charged, the amount paid and the amount still unpaid that the provider has a right to be paid
after adjustments or credits (§18.002(b-1)); jurat with notary signature, date and commission expiry; attached itemized statement; page
count. A records-retrieval **cover page** often sits on top: vendor name, request number, page count, a list of what is enclosed, or a
"no records found" certification.

**Typical wording (paraphrased, not the statutory form).** "Before me, the undersigned authority, personally appeared ..., who being duly
sworn deposed as follows." "I am the custodian of records of ..." "Attached are 3 pages of records ... kept in the regular course of
business." "The total amount charged for the services was $445.00. The amount paid was $0.00. The amount unpaid that the provider has a
right to be paid is $400.00." "Sworn to and subscribed before me on ..." The exact form is in CPRC §18.002; quote it from the official text.

**Extraction traps.**
- The affidavit is **not a medical record**: no encounter, no clinical content. Its jurat date, notary commission date and cover-page date
  are not service dates; its DOS range spans many visits.
- §18.001(b) (as amended 2019): the affidavit supports reasonableness of the charge but is **not evidence of causation**. Diagnosis lines on
  the attached bill are not a causation opinion (Hills v. Donis, 2021).
- The attached itemized statement usually duplicates a bill already produced in the provider's records: a true duplicate (section 1.4).
  Dedupe must keep one copy and cite both locations, never add both.
- Charged / paid / unpaid totals are attested sums. Code recomputes totals from the attached lines and compares; paid vs unpaid is a
  paid-or-incurred figure for notes only.
- A counteraffidavit from the other side attacks the same lines; it is an opponent's opinion, not a provider record.
- "No records" certifications are non-record pages (record_warning), but their date tells the paralegal a request was answered.

**Sources.**
- Texas Civil Practice and Remedies Code §18.001 and §18.002, via https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.001 and https://texas.public.law/statutes/tex._civ._practice_and_remedies_code_section_18.002 — **opened** (fetch tool; short quotes only). Takeaways: affiant is the provider or the records custodian; affidavit must include an itemized statement and be sworn; 90-day / 120-day service deadlines for affidavits and counteraffidavits; §18.001(b) says it is not evidence of causation; §18.002(b-1) medical-expense form adds amount paid and amount unpaid; amended through Acts 2019 (H.B. 1693). Official page https://statutes.capitol.texas.gov/Docs/CP/htm/CP.18.htm is a JavaScript app that did not render for the fetch tool.
- Hills v. Donis, No. 14-18-00566-CV (Tex. App.—Houston [14th Dist.] Feb. 11, 2021, pet. denied) (substitute mem. op.), via https://search.txcourts.gov/Case.aspx?cn=14-18-00566-CV&coa=coa14 — **opened** (PDF, pdftotext). Takeaway: §18.001 affidavits do not establish causation.
- Assumption: the cover-page layout is a common records-retrieval vendor style; no vendor template was opened.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - RECORDS CERTIFICATION COVER - ALL IDENTIFIERS FICTITIOUS
Gallowmere Records Retrieval (SYNTHETIC)   Request SYN-RR-3310   Completed 08/14/2026
Provider: Larkspur Hollow Physical Therapy (SYNTHETIC)   Patient: Delphine Okonkwo-Vale (SYNTHETIC)
Enclosed: Affidavit (2 pp) | Itemized statement (1 p) | Daily notes (6 pp)   Total pages: 9
--- page 2 ---
AFFIDAVIT CONCERNING COST AND NECESSITY OF SERVICES (CPRC 18.001)
STATE OF TX  /  COUNTY OF FERNHOLLOW (SYNTHETIC)
Before me appeared Marguerite Oyelaran-Pike (SYNTHETIC), who being sworn stated: I am the custodian of
records of Larkspur Hollow Physical Therapy (SYNTHETIC). Attached are records of services provided to
Delphine Okonkwo-Vale (SYNTHETIC) from 05/27/2026 through 06/10/2026, kept in the regular course of business
and made at or near the time of service. The services were necessary and the charges reasonable.
Total amount charged: $445.00.  Amount paid: $0.00.  Amount unpaid that the provider has a right to be paid: $400.00.
Sworn to before me 08/12/2026.   /s/ Notary Public, State of TX (SYNTHETIC)   Commission expires 04/30/2029
--- page 3: itemized statement (same document as section 10) ---
```
(The figures match the ledger in section 10: charges 445.00, adjustment 45.00, payments 0.00, balance 400.00. Page 3 is a duplicate of the
section 10 statement and must not be counted twice. Packets write the state as "TX" because the spelled-out state name is on the v1
identifier denylist in research/validate_library.py.)

---

## 18. Treating-provider narrative letter

**Fields.** Letterhead; letter date; addressee (usually the patient's attorney); "Re:" line with patient, DOB, date of injury; records
reviewed; history as told by the patient; initial complaints; examination findings; diagnoses (often with ICD-10); treatment summary
(dates, visit count, modalities, referrals); current status and maximum medical improvement; prognosis and permanency; future care (type,
frequency, duration, estimated cost); work status and restrictions; causation statement; signature and credentials.

**Typical wording.** Explained form: "Based on the history, the timing of symptom onset, my examination and the MRI of 06/18/2026, it is my
opinion within reasonable medical probability that the C5-6 disc protrusion was caused or aggravated by the collision of 05/14/2026,
because ..." Conclusory form: "The accident caused all of the injuries and treatment listed above." Future care: "Ms. X will need an
estimated 12 additional visits at $150.00 per visit." "She has not reached MMI."

**Extraction traps.**
- The letter date is not a service date. The letter is a summary written for the attorney, not a visit (section 4 traps).
- The causation sentence is a provider statement: the D-018 causation lexicon flags it, the excerpt is shown verbatim, and no summary may
  restate it as fact (the judge rejects one that does). The tool never grades whether it is conclusory; that is a legal judgment.
- Restated history ("Pt reports she was rear-ended ...") is the patient's account repeated by the provider.
- Visit counts and dates in the letter can disagree with the notes; code counts dated notes, the letter's number is cited as the letter's.
- Future-care costs are estimates and per-visit prices are rates (D-019, D-042): never charges.
- The letter may cite records not in the packet (an MRI from another facility); cite the letter, do not invent the record.

**Sources.**
- Ezel, *Personal Injury Narrative Medical Report Request* template: https://ezel.ai/templates/narrative-medical-report-request/ — **opened**. Takeaways: requested sections (history, exam, diagnoses with ICD-10, treatment, causation, MMI, prognosis, permanency, future care with cost, work status); causation addressed only within the provider's own judgment and in counsel-approved terms.
- Hills v. Donis (2021), above — **opened**. Takeaway: a treater's letters that state the crash caused the injuries without explaining how and why are conclusory and no evidence of causation.
- Mondaq, *Tips for attorneys: direct exam of a treating physician* (2012): https://mondaq.com/unitedstates/healthcare/160998/tips-for-attorneys-direct-exam-of-a-treating-physician — search summary; future care, cost and a causation question in reasonable medical probability.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Brightwater Spine & Wellness (SYNTHETIC)   555-0142
July 20, 2026
Ottoline Vey, Attorney, Harrowgate & Vey, PLLC (SYNTHETIC)
Re: Delphine Okonkwo-Vale (SYNTHETIC)   DOB 03/09/1991   Date of injury 05/14/2026
Ms. Okonkwo-Vale has treated in this office since 05/29/2026. She reports she was rear-ended
on 05/14/2026 and developed neck pain and right hand tingling the same night.
Diagnoses: cervical sprain (S13.4XXA); cervical radiculopathy (M54.12).
Treatment: spinal manipulation, e-stim and hot/cold packs; MRI 06/18/2026 ordered by this office.
Prognosis: guarded. She has not reached maximum medical improvement.
Future care: an estimated 12 additional visits at $150.00 per visit ($1,800.00).
The motor vehicle collision of 05/14/2026 caused all of the injuries and treatment described in this letter.
Dr. Corvin Ashdown, DC (SYNTHETIC)
```
(Conclusory on purpose, as in v2 pattern P3: no explanation of how or why. $150.00 per visit is a rate and $1,800.00 an estimate; neither is
a charge. July 20, 2026 is the letter date. The diagnoses match the CMS-1500 in section 8.)

---

## 19. Physician office / specialist progress note (PCP, orthopedics, neurology, pain management)

**Fields.** Date; visit type (new, follow-up); chief complaint; HPI or interval history; ROS; PMH/PSH, medications, allergies, social
history (often carried forward); exam; data reviewed (imaging, outside records); assessment and plan (medical decision making); procedures
recommended or scheduled; referrals; work status; follow-up interval; E/M code on the billing copy (99202-99215); signature and date.

**Typical wording.** "Pt returns for f/u of neck pain." "Interval hx: no improvement with 6 wks of PT." "ROS: Negative except as noted in
HPI." "MRI C-spine 06/18/2026 reviewed: C5-6 protrusion with R foraminal narrowing." "A/P: 1. Cervical radiculopathy, R C6. Discussed
options. Recommend C5-6 ACDF." "Estimated surgeon fee $14,500.00." "Work status: off work through 08/31/2026." "RTC 4 wks."

**Extraction traps.**
- Carried-forward ROS and PMH ("denies back pain") can contradict the HPI of the same note or another provider's note the same week
  (v2 patterns P10, P16); code pairs nearby dates, never merges two visits because text matches.
- A recommended or scheduled procedure is not a performed one; its date is in the future.
- "Estimated" surgeon or facility fees are estimates (D-019), not charges.
- Work-status and follow-up dates are future dates, not encounters.
- History "per patient" and outside imaging "reviewed" are cited as the note's statements, not as new findings.
- A PCP note that predates the injury is a pre-existing-condition source even when it is about something else.

**Sources.**
- CMS MLN, *Evaluation and Management Services Guide* (MLN006764): https://www.cms.gov/files/document/mln006764-evaluation-management-services.pdf — search summary; history, exam and medical decision making as the documented elements; document during or soon after the encounter.
- Steinkamp et al. (2022) via research/case-library-sources-v2.md P10 — abstract read; about half of note text is duplicated from earlier notes.
- Assumption: the layout above is a common EHR office-note print; no specific vendor template was opened.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD
Thistledown Orthopedic & Spine Clinic (SYNTHETIC)      Office Visit      DOS 07/08/2026
Patient: Delphine Okonkwo-Vale (SYNTHETIC)   Referred by: Dr. Corvin Ashdown, DC (SYNTHETIC)
CC: Neck pain with R arm tingling.
HPI: Rear-end MVC 05/14/2026 per pt. PT since 05/27/2026 without lasting relief. Pain 7/10.
ROS: Negative except as noted in HPI.
PMH: Low back pain 2023, resolved per pt.
EXAM: Spurling + R. Grip 4/5 R. Diminished R biceps reflex.
DATA: MRI C-spine 06/18/2026 reviewed: C5-6 protrusion, mild R foraminal narrowing.
A/P: Cervical radiculopathy, R C6. Recommend C5-6 ACDF. Estimated surgeon fee $14,500.00.
Work status: off work through 08/31/2026.   RTC after surgery.
Dr. Anselm Greaves, MD (SYNTHETIC)   99204
```
(The ACDF is recommended here and performed on 08/04/2026 (section 6). $14,500.00 is an estimate. 08/31/2026 is a future work-status
date, not a visit.)

---

## 20. Records-review (peer-review) letter and independent medical exam (IME) report

**Fields.** Requesting party (liability carrier, PIP carrier or defense counsel); reviewer or examiner name, specialty and credentials;
report date; for an IME, the exam date and who attended; list of records reviewed with their dates; questions posed (Were the injuries
caused by the incident? Was treatment reasonable and necessary? Through what date? Has the person reached MMI?); the reviewer's history
summary; exam findings (IME only: inspection, ROM, neuro, non-organic signs such as Waddell signs, distraction tests); opinions; attestation.

**Typical wording.** "Based on my review of the records listed above ..." "Treatment after 07/15/2026 was not reasonable or medically
necessary." "Findings consistent with a self-limited cervical strain." "Degenerative changes that pre-date the incident." "Symptom
magnification." "Waddell signs 3/5." "Effort was inconsistent." "MMI as of 07/15/2026."

**Extraction traps.**
- Stage: a records review is often pre-suit (the carrier's response to the demand); a defense medical exam in Texas needs a motion and court
  order under TRCP 204, so it is post-suit. The packet should say which.
- The reviewer's history is a summary of other records, not an encounter. A records review has only a report date; only an IME has an exam
  date, and the examiner is an adverse party's expert, not a treater.
- Credibility words ("symptom magnification", "inconsistent effort", "Waddell 3/5") flag under D-043; a clean negation ("0/5 Waddell signs")
  does not, and a sentence that mixes both does.
- "Not reasonable or necessary after date X" and "MMI as of X" are opinions with dates; X is not a service date.
- The reviewer may misquote dates or findings from the records; code can compare quoted dates with the packet's own entries.

**Sources.**
- Texas Rule of Civil Procedure 204 (physical and mental examination): https://ruledex.com/texas/texas-rules-of-civil-procedure/part-ii-rules-of-practice-in-district-and-county-courts/section-9-evidence-and-discovery/b-discovery/rule-204-physical-and-mental-examination/ — search summary; motion no later than 30 days before the discovery period ends; written order setting time, place, scope and examiner; report delivered on request.
- Search summary of New York no-fault arbitration awards and Pennsylvania MVFRL decisions on peer reviews (e.g. https://aaa-nynf.modria.com/downloadAward/42428348): a peer review must state a factual basis and medical rationale; Pennsylvania peer review addresses reasonableness and necessity, not causation. Jurisdiction-specific; used for wording only.
- Fishbain et al. (2003) on Waddell signs via research/case-library-sources-v2.md P8 — search summary.
- Assumption: Texas third-party liability carriers commission records reviews informally; no Texas statute governs them. Not verified.

**Specimen (SYNTHETIC).**
```
SYNTHETIC RECORD - RECORDS REVIEW - ALL IDENTIFIERS FICTITIOUS
Requested by: Quillon Casualty Mutual (SYNTHETIC), claim SYN-BI-55120   Report date: 08/27/2026
Reviewer: Dr. Evander Pollitt-Rhys, MD, PM&R (SYNTHETIC)
Claimant: Corentin Abelard-Moss (SYNTHETIC)   Date of loss: 05/02/2026
Records reviewed: ED 05/02/2026; PT notes 05/12/2026-07/31/2026; FCE 07/20/2026.
Summary: The PT note of 06/12/2026 documents Waddell signs 0/5.
  The PT note of 07/01/2026 documents no non-organic signs.
  The FCE of 07/20/2026 documents Waddell 3/5 and inconsistent effort.
  The PT note of 07/31/2026 documents full effort but symptom magnification with light touch.
Opinions: Findings are consistent with a self-limited lumbar strain. Treatment after 07/20/2026 was
  not reasonable or necessary. MMI as of 07/20/2026.
/s/ Dr. Evander Pollitt-Rhys (SYNTHETIC)
```
(Credibility sentences across 4 dates: 06/12 and 07/01 are clean negations that must not flag; 07/20 and 07/31 must flag (07/31 mixes a
clean and an adverse clause). 08/27/2026 is the report date; 07/20/2026 in the opinions is the reviewer's cut-off, not a visit.)

---

## 21. Product mapping and proposed packet mixes

| Format | Main rule it exercises | Expected tool behavior |
|---|---|---|
| ED note | Dates (rollover), voice, pre-existing, hedges | Date = arrival; excerpt verbatim; PMH flag |
| PT note | Gaps vs cancellations; plan vs actual; timed units | Cancellation is not an encounter; reason shown verbatim |
| Chiro note + travel card | Cloned notes; checkbox OCR | Travel card rows need review when OCR-derived |
| Radiology | Hedge and prior-imaging language; three dates | Exam date used; "Comparison: prior" flagged |
| Op note | Indications ≠ causation; D:/T: dates | No causation inferred; surgery date used |
| Pharmacy log | Refills, reversals, three price columns | Reversed lines excluded; prices to notes unless charge wording |
| CMS-1500 | Implied decimal; date ranges; Item 14/31 dates | Code parses amounts as implied cents; line sum vs Item 28 compared; days = units checked |
| UB-04 | 0001 total; FL 44 rate on the charge line; creation date; occurrence codes 01-06 | Total line not summed; rate not a charge (D-042 guard); any accident code = accident date |
| Ledger | Running balance; voids; balance forward; fee schedule | Only dated charge lines counted; voids netted in code |
| EOB | Double count of billed; CO/PR; mismatch with ledger | EOB amounts to notes, never added to charges; mismatch flagged |
| LOP / lien | Non-record narrative; asserted totals | No entries created; amounts to notes only (D-019) |
| Spanish note | Day-first dates; voice; translation labeling | Original excerpt; date convention suggestion (D-042) needs confirm |
| Scanned intake | OCR glyphs, checkboxes, fax/stamp dates | OCR-derived items always need review; page image beside text |
| EMS report | Call date and eight times; crew vs patient voice; refusal | One encounter on the call date; MIST wording attributed to EMS; refusal is an encounter without transport |
| Ambulance invoice | Per-mile rate vs line; fractional units | Miles x rate recomputed in code; only line totals are charges |
| §18.001 affidavit | Non-record page; duplicate attached bill; not causation | No encounter; duplicate deduped with both cites; totals recomputed |
| Narrative letter | Causation statement; letter date; estimates | Causation shown verbatim and flagged, never upgraded; estimates to notes |
| Office/specialist note | Copied ROS; recommended vs performed; estimates | Same-week contradiction surfaced; future dates not encounters |
| Records review / IME | Adverse opinions; credibility words; report vs exam date | D-043 credibility flags; opinions attributed to the reviewer |

**Proposed synthetic packet mixes** (round 1; the v2 library packets lib08-lib15 and the sections each needs are in
`research/case-library-sources-v2.md`, "Must contain" table):
1. *ER-only then gap*: EMS report + ED note + UB-04 (with 0001 line) + ED-physician CMS-1500 + radiology report + ambulance invoice + fax headers.
2. *Chiro under LOP*: intake form (scanned) + LOP + chiro daily notes with a travel card + CMS-1500 with a grouped date range (clean and OCR
   versions) + ledger with a void and a courtesy adjustment + narrative letter + §18.001 affidavit with a duplicate attached statement.
3. *PT with health insurance*: PT eval + daily notes with two cancellations + ledger + EOB (CO-45, PR-1, CO-97) with the deliberate
   ledger-vs-EOB mismatch.
4. *Surgery*: MRI with prior comparison + ortho office note with a surgical estimate + op note with indications paragraph + surgeon/
   assistant/anesthesia/facility bills on one date + inpatient UB-04 with a room-rate line.
5. *Spanish-speaking client*: Spanish clinic note with a day-first date whose parts are both 12 or less + rate and charge on the same page +
   pharmacy log with a reversed fill.

---

## 22. Cross-specimen consistency (Delphine Okonkwo-Vale timeline)

| # | Mismatch found in round 1 review | Status | Expected tool behavior |
|---|---|---|---|
| 1 | Radiology compared with "cervical radiographs" though the ED did a CT | Fixed: comparison is the 05/15/2026 CT | None |
| 2 | Chiro "Visit #9" on 06/03 with intake signed 05/29 | Fixed: Visit #4 (05/29 exam, 06/01-06/03 daily) | None |
| 3 | PT "Visit 7 of 24" on 06/10 but the ledger shows only the eval and 06/10 | Fixed: Visit 2 of 12 | None |
| 4 | Ledger shows no payments; EOB for the same DOS shows plan paid 16.00 and CO reductions | DELIBERATE | Billing analysis cites both and flags the mismatch; never picks paid vs incurred |
| 5 | Op note "12 weeks of therapy"; PT eval 05/27 to surgery 08/04 is 9.9 weeks | DELIBERATE | Excerpt verbatim and attributed; no automatic flag; golden truth never states 12 weeks |
| 6 | PT plan "3x/wk x 4 wks" against 24 planned visits | Fixed: 2x/wk x 6 wks = 12 | None |
| 7 | CMS-1500 line grouped 06/01-06/05 (5 days) with 3 units; travel card had non-consecutive dates | Fixed: grouped lines 06/01-06/03 = 3 days = 3 units; travel card marks match | Code checks days = units |
| 8 | PT units: 35 timed minutes billed as 3 units | Fixed: 38 minutes = 3 units under the stated CMS method | None |
| 9 | EMS arrival at destination 23:47 vs ED arrival 23:48 (new in round 2) | DELIBERATE (realistic) | Same encounter chain; no conflict flag |
| 10 | §18.001 affidavit totals vs ledger (new in round 2) | Consistent: 445.00 / 0.00 / 400.00 | Attached statement deduped against section 10 |
| 11 | Narrative letter "since 05/29/2026" and diagnoses vs chiro records and CMS-1500 (new in round 2) | Consistent | Letter cited as the letter; no new encounter |

`python3 research/record_formats_check.py` re-checks rows 2, 3, 6, 7, 8 and 10 and every specimen total.

---

## 23. Assumptions, limits, gaps and the name-collision search

- **Search-summary sources.** Sources marked "search summary" were not opened; their takeaways come from the search tool's summary. Opened:
  NUCC 1500 manual, RI UB-04 instructions, HL7 NUBC occurrence-code list, Noridian chiro, EOB and ambulance-mileage pages, CMS bill guide,
  CMS Claims Processing Manual ch. 15, NASEMSO time definitions, Montana NEMSIS disposition guide, CPRC §18.001/§18.002 (mirror), Hills v.
  Donis 2021 opinion, Ezel narrative template, arXiv OCR paper, Jotform LOP packet.
- **ACR report components.** The ACR page rendered only headings; the component list rests on secondary sources plus common practice.
- **UB-04 specifics.** FL 44 accommodation-rate use and the creation date on line 23 are prior knowledge that the T-078 reviewer also
  judged correct from working knowledge; both are marked "unverified" where they appear. Occurrence codes 01-06 come from an HL7 v2.4
  rendering of the NUBC list; the current NUBC label for 01 may read "accident/medical coverage". Verify against the licensed NUBC manual
  before quoting any of these in the submission.
- **Payer variation.** CMS-1500, UB-04 and ambulance rules here are NUCC/NUBC, CMS and one Medicaid guide; commercial and auto carriers vary.
- **Pharmacy "charge".** Whether U&C, plan paid or patient paid is the recoverable amount is a legal question the tool does not decide.
- **Spanish phrasing** is drawn from Mexican and Spanish teaching templates; Central American and Caribbean usage may differ.
- **OCR figures** come from one paper on smartphone photos of printed reports, not handwritten forms; handwriting is likely worse.
- **Statute currency.** CPRC §18.001/§18.002 were read through a mirror (amended through 2019); the official site did not render. Not
  checked for 2025-2026 amendments.
- **Not covered.** Pain-management procedure notes (e.g. epidural steroid injection) and stand-alone work-status slips have no section;
  the office-note section covers the visit that orders them.
- **Name-collision search (2026-11-02).** Web searches for the invented provider, payer, firm and clinician names found no exact match for
  Brightwater Spine & Wellness, Larkspur Hollow Physical Therapy, Quillfeather Regional Medical Center, Ferncastle Imaging Associates,
  Thistledown Surgical Center, Mossgate Community Pharmacy or Harrowgate & Vey. Two names were replaced in round 2: "Bluebonnet Mutual
  Health Plan" (Texas has real "Bluebonnet" health plans) became Quoinmere Mutual Health Plan, and "Clínica Familiar Los Almendros" /
  "Dra. Inés Valcárcel" (a similarly named clinic and a real surname match) became Consultorio Médico Peñaverde / Dra. Itziar Orbezua Lanz.
  Names added in round 2 (Fernhollow County EMS, Gallowmere Records Retrieval, Saltmarrow General Hospital, Quillon Casualty Mutual and the
  clinicians) were built from uncommon word pairs and not searched individually. Any remaining resemblance is unintended; packets built
  from these specimens still pass `research/validate_library.py`.
