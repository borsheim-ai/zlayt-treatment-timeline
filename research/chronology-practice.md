# How PI firms build treatment chronologies for demand packages

Card: T-008 · Author: researcher (instance A) · Researched 2026-11-01/02 with WebSearch/WebFetch.
Scope: what a personal-injury (PI) paralegal produces before a demand letter, what each entry contains, and
what that implies for the prototype. Synthetic case only (Jordan Rivera, spec Appendix A).

**Source quality warning.** Almost all public "how to build a medical chronology" material is written by
vendors that sell chronology services or software (EvenUp, Tavrn, LezDo TechMed, InPractice, CaseMark). There is
no bar-association or AALNC published standard for PI chronologies that we could find (see source 9). Treat
the conventions below as *industry practice*, not rules. Where all vendors agree, we treat it as reliable.

## 1. What the artifact is

- **Chronology vs. summary.** A *chronology* orders every encounter by date of service; a *medical summary*
  groups by provider, body part or injury and reads as narrative. Firms use both, often the chronology first
  and the summary as the demand letter's "medical treatment" section. (Sources 1, 2.)
- **When it is built.** Usually after the client reaches maximum medical improvement (MMI) or finishes
  treatment, so the demand can state total specials; earlier for policy-limits cases. (Source 2.) Our sample
  case is mid-treatment (rec 9, dated 2026-06-12: "Recommend cervical epidural steroid injection", recommended, not performed) — the export must
  not imply treatment is complete. **Assumption** (see ASSUMPTIONS-proposed P-04).
- **Who builds it.** Paralegal or case manager; nurse/LNC on larger cases; attorney reviews and signs the
  demand. Chronologies "do not decide causation" — they display the documented sequence; causation opinions
  belong to physicians and lawyers. (Sources 3, 9.)

## 2. Fields per entry (consensus across sources)

| Field | Sources | In the Zlayt must-have? | Prototype note |
|---|---|---|---|
| Date of service | 1, 2, 4 | yes | Code-parsed, one format throughout (source 1 insists on a single date format) |
| Provider / facility | 1, 2, 4 | yes | As written; name variants are a conflict signal |
| Encounter type (ER, PCP, PT, imaging, pain mgmt) | 1 | no | Cheap to derive from source line; optional column |
| Chief complaint / findings / diagnosis | 1, 2 | summary | One-line summary must not upgrade or downgrade a finding |
| Treatment, referrals, plan | 1, 2 | summary | "Recommend ESI" ≠ "received ESI" |
| Source page/citation | 1, 4 | **exact excerpt** | Source 1: "page number should never be left blank." Our equivalent is the verbatim excerpt + record # |
| Charges | 2, 4, 5 | yes | Itemized, cross-checked against treatment dates (source 5) |
| Missing records / gaps | 1, 2 | gap flag | Log, explain, request supplemental records |

## 3. Workflow steps paralegals follow

1. Request records from every provider (HIPAA authorization), with a broad date range — including *prior*
   records, because missing baseline records invite pre-existing-condition arguments. (Sources 1, 6.)
2. Index what arrived vs. what is outstanding. (Source 1.)
3. Order by date of service; extract per-entry fields. (Sources 1, 2.)
4. Flag gaps, pre-existing conditions, and contradictions *for attorney review*; distinguish aggravation of a
   prior condition from a new injury. (Source 1.)
5. Cross-check bills against treatment dates; a bill with no matching visit (or a visit with no bill) is a
   finding. (Source 5.)
6. Verify every entry against its source before it goes to the attorney. (Sources 1, 4.)
7. Keep it updated as treatment continues. (Source 2.)

Step 6 is the one the Zlayt brief cares about ("she reviews rather than trusts"). Every vendor sells
"source-linked" chronologies precisely because unverifiable entries cost credibility with adjusters (source 7).

## 4. Why accuracy matters to the adjuster (bridge to adjuster-attacks.md)

Practitioners say the package should be *easy to verify*, not just complete (source 5). Concealing a prior
condition or a gap "triggers credibility discounts across the entire case evaluation" (source 6, plaintiff-side
vendor claim). The implication for us: **surfacing** a gap or prior condition to the paralegal is the product's
job; deciding whether to explain it in the letter is the lawyer's job.

## 5. What this means for the prototype (design requirements)

- R1. Each entry carries record #, date, provider, one-line summary, verbatim excerpt. No entry without an excerpt.
- R2. Dates rendered in one format (ISO `YYYY-MM-DD`), parsed by code.
- R3. The summary must preserve hedges: "may represent degenerative change" stays hedged; "recommend" stays a
  recommendation; "patient states" stays attributed to the patient.
- R4. Gaps, prior conditions and conflicts are *flags for review*, not edits to the timeline and not
  conclusions in the export.
- R5. Charges are listed per source and cross-referenced to an entry; rates and unclear amounts are listed but
  not totaled (Appendix C).
- R6. Export header should say the chronology is through the last record date and that treatment may be
  ongoing if the last record contains a plan/recommendation. (Assumption P-04.)
- R7. A "missing records" note is out of scope for the prototype (we cannot know what wasn't sent) — record as
  a scope cut candidate for the orchestrator.

## Sources

1. EvenUp, "How to Prepare a Medical Chronology for Injury Claims" — https://evenuplaw.com/guides/how-to-prepare-medical-chronology — Fields per entry, never-blank source page, single date format, log gaps and pre-existing conditions, verify every entry before attorney review. (Vendor.)
2. EvenUp, "What is a Medical Summary?" — https://evenuplaw.com/guides/what-is-a-medical-summary — Summary vs chronology distinction; summary usually drafted after MMI/completion; itemized expenses and missing-records list; must be updated as treatment continues. (Vendor; content via search snippet.)
3. LezDo TechMed, "Why Legal Nurse Consultants Use Medical Chronologies" — https://www.lezdotechmed.com/blog/why-legal-nurse-consultants-use-medical-chronologies-for-medical-record-review — A chronology shows the documented sequence; qualified professionals, not the chronology, evaluate causation. (Vendor.)
4. Tavrn, "What is a medical chronology and how is it used" — https://www.tavrn.ai/blog/what-is-a-medical-chronology-and-how-is-it-used — Chronology contents (date of injury, providers, dates, tests) and its use in demand packages. (Vendor; via search snippet.)
5. Tavrn, "Demand letter preparation" — https://www.tavrn.ai/blog/demand-letter-preparation.md — Cross-checking billing against the treatment timeline is a paralegal task; the package should be easy to verify. (Vendor; via search snippet.)
6. Tavrn, "Legal demand letter best practices" — https://www.tavrn.ai/blog/legal-demand-letter-best-practices — Concealing pre-existing conditions draws credibility discounts; missing baseline records invite pre-existing arguments; absent objective findings trigger skepticism. (Vendor.)
7. EvenUp, "5 Steps to Mitigate Treatment Gaps and Preserve Case Value" — https://evenuplaw.com/blog/mitigate-treatment-gaps-preserve-case-value — Vendor claims gaps can reduce settlement value up to 20%; **unverified, vendor benchmark**. Useful only as a signal that firms care.
8. SF Bar, "Paralegal corner: collaboration of LNCs with paralegals and attorneys" — https://www.sfbar.org/blog/paralegal-corner-collaboration-of-legal-nurse-consultants-with-paralegals-and-attorneys/ — Paralegals and LNCs split record work: paralegal organizes, LNC interprets clinical meaning. (Bar-association blog; via search snippet.)
9. AALNC, "What is an LNC" brochure — https://www.aalnc.org/Portals/0/Docs/About/What%20is%20an%20LNC%20Brochure_Final.pdf — AALNC has a Code of Ethics but we found **no published AALNC chronology standard**; chronology conventions are industry practice. (Professional association.)
10. Claims Journal, C. Tidball, "How to Review Bodily Injury Demands" (2013) — https://www.claimsjournal.com/news/national/2013/06/05/230291.htm — The adjuster-side mirror image: what reviewers check in the chronology the paralegal sends (timing, gaps, priors, objective findings, billing vs SOAP notes). (Insurance trade press — the only non-plaintiff source here.)

Assumptions where sources are thin: no source states *how long* paralegals spend per chronology from
independent data (vendors claim "hours"; the Zlayt brief itself says "hours"). We use the brief's word, not a number.
