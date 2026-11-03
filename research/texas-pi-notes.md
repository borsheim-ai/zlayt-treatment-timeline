# Texas PI norms relevant to billed charges and medical records

Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02.
Scenario: Zinda Law Group (Austin), fictional client Jordan Rivera, rear-ended in Austin (spec Appendix A); first records dated 2026-01-09. **Not legal advice**;
this is product research so the prototype does not mislead a Texas paralegal.

Method note: statutes.capitol.texas.gov renders only navigation to our fetch tool, so statute text was read via
mirrors (rulesofcivilprocedure.com, texas.public.law) and cross-checked against Texas Supreme Court opinions
(the In re Allstate PDF text was extracted and read directly). Each item says how it was verified.

## 1. Paid or incurred — CPRC §41.0105 (verified)

- **Rule.** Recovery of medical expenses is limited to "the amount actually paid or incurred by or on behalf
  of the claimant." Enacted 2003 (tort reform). (Src 1, 2.)
- **Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. July 1, 2011).** Amounts a provider has no right to collect
  (e.g., insurer-contracted write-offs) are not recoverable, and "only evidence of recoverable medical
  expenses is admissible at trial"; the jury is not told about insurance adjustments (collateral-source rule
  still applies). (Src 1 — full text read.)
- **Product consequence.** Records show **billed charges**. The prototype must label every dollar figure
  "billed (as written in record)" and never call the running total "medical damages", "specials owed" or
  "recoverable". Paid/adjusted amounts usually come from billing ledgers/EOBs, not clinical notes — out of scope.

## 2. Medical-expense affidavits — CPRC §18.001 (verified, current version)

- **Effect (b).** Absent a timely counteraffidavit, an affidavit that charges were reasonable and services
  necessary is *sufficient evidence* to support a finding on those points — and since the 2019 amendment
  "is not evidence of and does not support a finding of the causation element." (Src 3; Allstate fn. confirms
  the 2019 change, src 4.)
- **Who/what (c).** Made by the provider or the person in charge of its records, with an **itemized statement
  of the service and charge**. (Src 3.)
- **Deadlines (d),(e).** Serve by the earlier of 90 days after the defendant answers or the expert-designation
  deadline; counteraffidavit by the earliest of 120 days after answer or the designation deadlines.
  Supplementation (h): affidavit ≥60 days before trial, counteraffidavit ≥30. (Src 3.) Applies to actions
  commenced on/after 2019-09-01 (src 4).
- **Counteraffidavit (f).** Must give reasonable notice of the basis and be made by a qualified person; may not
  controvert causation. (Src 3.) *In re Allstate Indemnity Co.*, 622 S.W.3d 870 (Tex. 2021): §18.001 is
  "purely procedural," "streamline[s]" proof of reasonableness/necessity; a counteraffiant need not practice in
  the same specialty; striking a counteraffidavit and barring all contrary evidence was an abuse of discretion.
  (Src 4 — full text extracted and read.)
- **Product consequence.** (a) An itemized-by-provider charge list with record citations is the raw material
  for §18.001 affidavits — our "billed charges" list should group by provider and keep each source excerpt.
  (b) §18.001 says nothing about causation → the chronology can't lean on billing to prove causation either.
  (c) Deadlines are lawsuit-stage, not pre-suit demand-stage; the prototype doesn't compute them. (Scope cut.)

## 3. Discovery of negotiated rates / letters of protection (verified via secondary)

- *In re K & L Auto Crushers, LLC*, 627 S.W.3d 239 (Tex. 2021): providers' negotiated rates with insurers are
  relevant to reasonableness of the plaintiff's charges and discoverable (narrowed requests); the Court notes
  letter-of-protection (LOP) arrangements. *In re ExxonMobil Corp.* (Tex. Nov. 2021) followed it. (Src 5, 6.)
- **Product consequence.** Billed charges on LOP-treated care will be challenged as unreasonable. The tool should
  not imply a billed amount is reasonable; it reports what the record says.

## 4. Hospital and EMS liens — Property Code ch. 55 (partly verified)

- §55.004(b): a hospital lien is for the lesser of charges for the first 100 days of hospitalization or 50% of
  the patient's recovery (or the awarded hospital charges less a proportional share of fees). §55.004(f): an
  EMS lien may not exceed $1,000 and covers services within 72 hours after the accident. (Src 7 — mirror text.)
- Rivera has an EMS transport (rec 1 "Transported to Central ER.", no charge stated) and an ER visit (rec 2 "ER charges: $6,240."). **Assumption:** whether
  Central ER/Austin EMS filed liens is unknowable from clinical excerpts; lien tracking is a settlement-stage
  task, out of scope. County-population and filing-requirement details were **not verified** (official page
  unreadable to our tool; secondary sources conflict).

## 5. Records as evidence — TRE 902(10) business-records affidavits (verified via secondary)

- Medical records are commonly proved by a business-records affidavit under Tex. R. Evid. 902(10) (with notice
  to other parties); since 2014 they generally need not be filed with the court in advance (SB 679, 83rd Leg.).
  (Src 8, 9.)
- **Product consequence.** Firms think in terms of *records sets with affidavits*. Our "record #" + verbatim
  excerpt is the in-app analogue of a Bates/page cite. Real deployment should carry Bates numbers. (Assumption.)
- Not verified: how TRE 803(4) (statements for medical diagnosis) applies to "patient states…" lines. Treat
  patient-attributed causation statements as history, not opinion (Guevara, adjuster-attacks.md A6).

## 6. Causation proof (verified via primary summaries)

- Expert testimony is generally required to connect an accident to medical conditions outside lay knowledge
  (*Guevara v. Ferrer*, 247 S.W.3d 662 (Tex. 2007)); proof must reach reasonable medical probability, not
  possibility (*Jelinek v. Casas*, 328 S.W.3d 526 (Tex. 2010)); evidence of an alternative cause such as a
  second accident is admissible (*JLG Trucking v. Garza*, 466 S.W.3d 157 (Tex. 2015)). Details and URLs in
  adjuster-attacks.md srcs 9–11.

## 7. Other Texas context (secondary only — not needed by the prototype)

- Limitations: generally two years for personal injury, CPRC §16.003. Proportionate responsibility: a claimant
  more than 50% responsible recovers nothing, otherwise damages reduced by percentage (CPRC §33.001, §33.012).
  (Src 10, 11 — secondary; verify before relying.) Texas is an at-fault (tort) auto state; PIP is optional
  coverage. **Assumption**, not researched further: pre-suit demands go to the at-fault driver's liability carrier.
- Stowers doctrine: *G.A. Stowers Furniture Co. v. American Indemnity Co.*, 15 S.W.2d 544 (Tex. Comm'n App. 1929).
  A liability insurer that unreasonably rejects a demand within policy limits can be liable for the excess
  judgment. A valid Stowers demand covers the whole claim and is within limits; *American Physicians Ins. Exch. v.
  Garcia* (Tex. 1994) narrowed the doctrine (src 12). This affects demand-letter *strategy* (time-limited
  policy-limits demands), not the chronology. One more reason the chronology must be accurate: the carrier tests
  a Stowers demand's reasonableness against the records.

## Assumptions where sources are thin

- T1. A pre-suit demand to an adjuster is not bound by §18.001 or Haygood (those govern trial evidence), but
  adjusters evaluate with trial in mind, so they discount billed charges to expected paid amounts. (Inference
  from srcs 1, 4, 5; no adjuster source states it directly.)
- T2. Zinda (an Austin PI firm) sends demands with an itemized medical-specials table. (Industry practice from
  chronology-practice.md; not verified for Zinda specifically.)
- T3. Records in the demand package are the same records later proved by 902(10)/18.001 affidavits. (Inference.)

## Sources

1. Haygood v. De Escabedo, 356 S.W.3d 390 (Tex. 2011) — https://caselaw.findlaw.com/tx-supreme-court/1573065.html — §41.0105 limits recovery to amounts paid or incurred; unadjusted charges inadmissible; §18.001 is procedural. (Full text read.)
2. Jim Adler & Associates, "What are paid and incurred medical expenses?" (2017) — https://www.jimadler.com/blog/what-are-paid-and-incurred-medical-expenses/ — Texas plaintiff firm's explanation of §41.0105 in practice. (Secondary; via search snippet.)
3. Tex. Civ. Prac. & Rem. Code §18.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-18-001/ — Current text: sufficiency, itemized statement, 90/120-day deadlines, counteraffidavit limits, not evidence of causation. (Mirror of statute; cross-checked with src 4.)
4. In re Allstate Indemnity Co., 622 S.W.3d 870 (Tex. 2021) — https://www.txcourts.gov/media/1452189/200071.pdf — §18.001 is procedural; 2019 amendments (Acts 2019, 86th Leg., ch. 779) made affidavits non-evidence of causation and changed deadlines for suits after 2019-09-01. (Full text extracted and read.)
5. In re K & L Auto Crushers, LLC, 627 S.W.3d 239 (Tex. 2021) — https://law.justia.com/cases/texas/supreme-court/2021/19-1022.html — Negotiated insurer rates are relevant and discoverable on reasonableness of charges. (Primary; read via summaries.)
6. Claims Journal, "Texas Supreme Ct. Approves Discovery for Documents Related to Medical Charges" (2021) — https://amp.claimsjournal.com/news/southcentral/2021/06/02/304050.htm — Insurer-side press on K&L's practical effect. (Trade press; via search snippet.)
7. Tex. Prop. Code §55.004 (mirror) — https://texas.public.law/statutes/tex._prop._code_section_55.004 — Hospital lien lesser-of 100-day charges / 50% of recovery; EMS lien ≤$1,000 within 72 hours. (Mirror.)
8. Texas Rules of Evidence 902 — https://texasevidence.com/rule-902/ — 902(10) business-records affidavit admits records without live custodian; notice required; form for medical expenses. (Secondary reference.)
9. Senate Research Center bill analysis, SB 679 (83rd Leg.) — https://capitol.texas.gov/tlodocs/83R/analysis/pdf/SB00679F.pdf — Records served with a 902(10) affidavit need not be filed with the court beforehand. (Official legislative analysis; via search snippet.)
10. Tex. Civ. Prac. & Rem. Code §33.001 (mirror) — https://rulesofcivilprocedure.com/tx/cprc/section-33-001/ — Claimant >50% responsible may not recover. (Mirror; via search snippet.)
11. Blass Law, "Texas 51 percent rule" — https://www.blasslaw.com/faqs/texas-51-percent-rule-comparative-fault/ — Practitioner explanation of modified comparative fault and the two-year limitations period. (Plaintiff firm.)
12. IRMI, "Stowers doctrine" (insurance glossary) — https://irmi.com/term/insurance-definitions/stowers-doctrine — Insurer liable for the excess when it unreasonably refuses a within-limits demand; Thompson Coe practice paper https://www.thompsoncoe.com/content/uploads/2019/02/Stowers.pdf covers the elements and *Garcia*. (Secondary; via search excerpts.)
