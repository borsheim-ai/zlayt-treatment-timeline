# T-010 review — litigation-lead-reviewer

**Verdict: changes** (0 blockers, 4 majors, 8 minors, 1 nit).

I read the five dossiers the way a Texas plaintiff PI partner would. I supervise the paralegal who builds the chronology, I sign the demand, and I negotiate with the adjuster who reads it. The structure is complete: 10 sections each, 18-23 checklist items, 8-12 URLs, 3 calibration findings each, and the files have not changed since 34e9398. The Texas damages law is right and current. §41.0105 and the Haygood holding check out against primary text, and 2025's SB 30 died in conference. The checklists also catch most of what really gets a demand discounted: gaps, the conflicting accident dates, the prior-condition and degenerative language, the missed PT, self-reported causation, and the PT rate.

There are four problems these dossiers would carry into every review they judge:
- **Adjuster checklist, delay to first treatment.** It asks the tool to compute this "from the accident date (here: same day, EMS)". To do that the tool has to pick one of the two conflicting accident dates.
- **Adjuster checklist, export contents.** It requires the export to include the prior condition. That takes the disclosure decision away from me, the attorney, and conflicts with the spec, which says the export contains "only what she accepted".
- **Litigation-lead dealbreaker on real client data.** It rejects "any suggestion" of real client records in development or testing. Part 2 area 4 explicitly asks how to build a test set "from real work product", and Opinion 705 allows using confidential information with precautions.
- **Privacy dossier, Texas Rule 1.05.** It treats Rule 1.05 as if it contained ABA 1.6(c)'s "reasonable efforts" duty. It does not. The Texas duty is "shall not knowingly reveal".

Smaller issues:
- Opinion 705 says relying on AI carries the same risks as relying on a nonlawyer assistant ("Cf. Rule 5.03"). The dossiers overstate that as an instruction to supervise AI like one.
- The litigation-lead's ethics framing is about candor to a court (Mata v. Avianca, Rule 3.03). A demand letter goes to an adjuster, so the governing rule is Rule 4.01, truthfulness to third persons.
- Nothing checks that the charges section says which providers have no bill in the records.
- Nothing checks for a referral to pain management that the records never mention.

Source verification: `artifacts/review-evidence/T-010-litlead-source-check.md` (11 sources; Op. 705, Haygood via txcourts.gov, §41.0105, §18.001, ch. 181 incl. §181.154, Rule 1.05, ABA 512 primary via Wayback).

```json
{"card": "T-010", "persona": "litigation-lead-reviewer", "model": "claude-opus-5-5",
 "scope": "commit 34e9398: personas/{paralegal,litigation-lead,claims-adjuster,legal-nurse,privacy-compliance}.md (git diff --stat 34e9398 -- <files> empty: working tree = commit); checked against spec/SPEC.md Appendix A, spec/SAMPLE_CASE_TRUTHS.md, docs/LLM_VS_CODE.md, docs/CONTRACT.md §6.3; no app (documents card)",
 "exercised": [
  "python3 tools/board.py show T-010 (AC 1-3 and handoff)",
  "read all five dossiers in full (cat -n), SPEC Appendix A, SAMPLE_CASE_TRUTHS, LLM_VS_CODE, CONTRACT §6.3 and D.2",
  "awk/grep count per dossier: sections=10/10/10/10/10, checklist=23/18/18/19/18, URLs=8/8/10/9/12, calibration=3 each (matches AC claims)",
  "git diff --stat 34e9398 -- the five dossiers -> empty",
  "curl-fetched and grepped 11 cited/primary sources (WebFetch not in my toolset): Tex. Op. 705; Haygood opinion from search.txcourts.gov 09-0377 (FindLaw 403); CPRC §41.0105 and §18.001 (texas.public.law; statutes.capitol.texas.gov links return the site shell); 2025 SB 30 bill history; Tex. H&S §§181.001/.051/.101/.154; Tex. Disc. R. 1.05 (legalethicstexas.com + State Bar PDF via pdftotext); ABA Op. 512 primary via Wayback + ezel.ai + 2civility; JLG Trucking; WLF 2021; Faegre Drinker Stowers; Claims Journal 2013",
  "walked each checklist against the nine sample records as a partner reviewing a demand: what the adjuster will attack vs what each checklist would catch",
  "wrote artifacts/review-evidence/T-010-litlead-source-check.md"
 ],
 "verdict": "changes",
 "scores": {"texas_law_accuracy": 3, "catches_what_gets_demands_discounted": 4, "adjuster_adversarial": 4, "keeps_tool_out_of_legal_medical_judgment": 3, "spec_alignment": 3, "source_grounding": 4},
 "findings": [
  {"severity": "major",
   "title": "Adjuster checklist makes the tool pick an accident date to compute delay-to-first-treatment",
   "evidence": "personas/claims-adjuster.md:19 \"Delay to first treatment is computed from the accident date (here: same day, EMS) and shown; a delay would be my first argument.\" vs the same file :18 (\"if the tool chose one silently, I can use the other\") and spec/SAMPLE_CASE_TRUTHS.md:13 \"Things the tool must not do ... merge the two accident dates into one\". Under the 2026-01-19 intake date the first treatment (01-09) precedes the accident, so any single 'delay' figure resolves the conflict.",
   "why_it_matters": "This file becomes the adjuster reviewer's prompt. A reviewer following item 2 will file a finding against a spec-compliant tool for not computing a delay, pushing the worker to resolve the accident-date conflict, which is a factual and legal call reserved to the attorney and an Appendix C must-not. Delay-to-first-care is also not one of the four spec flags.",
   "fix": "Rewrite item 2: \"Delay to first treatment is NOT computed while the accident date is in conflict; the timeline shows the first date of service (2026-01-09, EMS) and both stated accident dates with excerpts so the attorney can answer a delay argument.\"",
   "acceptance_test": "grep personas/claims-adjuster.md for 'computed from the accident date' returns nothing; item 2 references both dates and says no delay figure while they conflict."},
  {"severity": "major",
   "title": "Adjuster dossier requires the export to include adverse facts, overriding the attorney's disclosure decision and the spec's accepted-only export",
   "evidence": "personas/claims-adjuster.md:24 \"Prior conditions: 'low back pain in 2023, resolved' is flagged; the export does not drop it.\"; :41 red flag \"A hidden gap, prior condition, or missed-appointment note that I find in the records but the chronology omitted.\" vs spec/SPEC.md:42 \"Export. Copy-ready text ... containing only what she accepted\", docs/LLM_VS_CODE.md:78 \"The flag appears only in the internal notes, never in the letter\", and personas/litigation-lead.md:14 \"surfaced to him, not hidden, so he decides strategy\" / personas/paralegal.md:82 \"whether to disclose a gap in the demand — litigation-lead\".",
   "why_it_matters": "Whether a demand mentions the 2023 low back pain is my strategy call. In Texas the duty in negotiation is not to make false statements of material fact to a third person (Tex. Disc. R. 4.01). It is not a duty to put every adverse record line in the letter. A reviewer prompt that fails the tool when the attorney chose to omit a fact pushes the product into making the legal judgment. It also contradicts the spec's must-have and two sibling dossiers.",
   "fix": "Item 7: \"... is flagged with its excerpt, and the record 3 summary does not silently drop it; whether it appears in the export is the attorney's decision.\" Red flag: \"... that the tool's timeline or flags omitted (not: that the export omitted after a human dismissed it).\"",
   "acceptance_test": "No item in personas/claims-adjuster.md requires specific content in the export beyond 'only accepted items, nothing overstated'; the red flag targets tool omissions, not attorney omissions."},
  {"severity": "major",
   "title": "Litigation-lead dealbreaker bans any real-record testing, contradicting Part 2 area 4 and Op. 705",
   "evidence": "personas/litigation-lead.md:42 red flag \"Any suggestion of using real client records in development or testing.\" and :32 item 14. spec/SPEC.md:84 Part 2 area 4: \"How do you build a test set from real work product?\". Tex. Op. 705 (fetched): \"there may be circumstances where it is permissible to use confidential information in conjunction with a generative AI program\" with precautions (terms of service, data security, training, client consultation/consent).",
   "why_it_matters": "This persona would reject outright a Part 2 that correctly answers area 4, for example with a de-identified, firm-controlled test set from past chronologies, a reviewed vendor, and client consent where needed. The ground rule against real data (spec/SPEC.md:17) covers this candidate project, not the shipped feature at Zinda. A partner knows the firm will eventually run real files through it, because that is what shipping means.",
   "fix": "Split: \"(a) This prototype, repo, fixtures, demo and prompt log use only synthetic data (dealbreaker). (b) Part 2's plan for real work product names the controls: de-identification or firm-controlled environment, vendor terms reviewed (no training, retention), access limits, client consent where required (Op. 705 / ABA 512), attorney sign-off.\"",
   "acceptance_test": "personas/litigation-lead.md red flags distinguish prototype data from the Part 2 rollout plan; checklist item 14 asks for named controls rather than prohibiting real work product."},
  {"severity": "major",
   "title": "Privacy dossier states Texas Rule 1.05 carries an ABA 1.6(c)-style 'reasonable efforts' duty; it does not",
   "evidence": "personas/privacy-compliance.md:5 \"make sure the firm can show 'reasonable efforts' (Rule 1.6(c) / Texas 1.05)\"; :47 \"reasonable efforts (Rule 1.6(c) / Tex. 1.05)\". Texas Rule 1.05(b) as fetched: \"a lawyer shall not knowingly: (1) Reveal confidential information ...\". In the State Bar PDF (amendments eff. Jan 31, 2022), Rule 1.05 spans pdftotext lines 841-1122; no 'reasonable efforts'/'unauthorized access'/'inadvertent' hit falls inside it. Op. 705 derives precautions from Rule 1.01 cmt. 8 and Op. 680. Details: artifacts/review-evidence/T-010-litlead-source-check.md row 6.",
   "why_it_matters": "This dossier grades the product note and Part 2 \"against the sources below\" (privacy-compliance.md:54). It will reward a submission that tells a Texas law firm that its confidentiality rule says something it does not. Lawyers reading Part 2 will catch it, and it costs the same credibility a wrong date costs a demand. It is also within my lens: Texas confidentiality duties are what I am responsible for as a partner.",
   "fix": "Replace with: \"Texas: Rule 1.05 bars knowingly revealing confidential information (broader than privilege); technology competence (Rule 1.01 cmt. 8) and Ops. 680/705 call for reasonable precautions (understand the tool, review terms of service, data security, staff training). ABA Model Rule 1.6(c) states a reasonable-efforts duty expressly; Texas has no textual equivalent.\"",
   "acceptance_test": "No dossier attributes 'reasonable efforts' to Tex. Rule 1.05; the Texas precaution duty is cited to Rule 1.01 cmt. 8 and Ops. 680/705."},
  {"severity": "minor",
   "title": "Op. 705 overstated as 'supervise AI like a nonlawyer assistant'",
   "evidence": "personas/litigation-lead.md:31 item 13 \"(verify, don't rely blindly; supervise like a nonlawyer assistant)\" and :62; personas/privacy-compliance.md:34 \"(Op. 705: supervise AI like a nonlawyer assistant)\" and :72. Op. 705 text: \"Lawyers who rely on generative AI ... risk many of the same perils as those who rely on inexperienced or overconfident nonlawyer assistants. Cf. Rule 5.03.\"",
   "why_it_matters": "Op. 705 draws an analogy about risk. It does not hold that Rule 5.03 applies to AI. Reviewers checking Part 2 for 'consistency with Op. 705' will push the PM toward a paraphrase a Texas ethics-savvy partner would correct. ABA 512 is the source that ties AI to supervisory Rules 5.1/5.3 (verified in primary text).",
   "fix": "\"Op. 705: lawyers cannot blindly rely on AI output and must verify it; relying on AI carries the perils of relying on an overconfident nonlawyer assistant (cf. Rule 5.03); train lawyers and staff. ABA 512: managerial/supervisory duties (5.1/5.3) extend to firm AI policies.\"",
   "acceptance_test": "Each Op. 705 citation in the five dossiers matches the opinion's wording or is marked as a paraphrase of the 'Cf. Rule 5.03' analogy."},
  {"severity": "minor",
   "title": "Litigation-lead ethics frame is court candor (Mata, 3.03), not Rule 4.01 truthfulness to third persons, which governs a demand letter",
   "evidence": "personas/litigation-lead.md:5 \"Mata v. Avianca is the story every partner tells\"; :46 vocabulary \"candor\"; no mention of Rule 4.01 anywhere in the five dossiers (grep). Op. 705 lists 1.01, 3.01, 3.03, 3.04, all aimed at tribunals.",
   "why_it_matters": "The chronology goes to an adjuster, not a court. The rule a partner worries about is Tex. Disc. R. 4.01(a), which bars knowingly making a false statement of material fact to a third person. A Stowers demand built on a wrong medical fact can also give the carrier an argument that the demand was not one a reasonable insurer had to accept. That is the concrete reason accuracy matters here, and the reviewer should test Part 2 against it.",
   "fix": "Add to vocabulary/identity: 'Rule 4.01 (truthfulness in statements to others)'; add an item: 'Part 2 / product note tie the no-invention rule to statements the firm makes to adjusters (Rule 4.01) and to Stowers demand validity, not only to court filings.' Optionally cite N.D. Tex. LR 7.2(f) (named in Op. 705) as the Texas court AI rule.",
   "acceptance_test": "personas/litigation-lead.md names Rule 4.01 and links it to demand letters."},
  {"severity": "minor",
   "title": "No check that the charges section discloses providers with no bill in the records",
   "evidence": "personas/litigation-lead.md:24-25 (items 6-7) and personas/claims-adjuster.md:28 (item 11) check only $6,240 + $2,150 = $8,390 and the $185 rate. Records 1, 3, 5-7, 9 (EMS, PCP, PT visits, pain management x2) carry no amount (spec/SPEC.md:57-65). Only the litigation-lead calibration fix (:58, 'stated in records received') hints at it.",
   "why_it_matters": "A total labeled 'billed charges' next to a nine-entry timeline reads as complete specials. If the paralegal drops it into the demand, the firm under-demands or the adjuster values only the two bills. Specials anchor a Colossus-style valuation, so a missing bill gets the claim discounted just as surely as a wrong one. The Claims Journal source the dossiers cite lists 'bills vs SOAP notes' among adjuster checks.",
   "fix": "Add to litigation-lead (and adjuster) checklist: 'The charges section states the total covers only amounts stated in the records received and lists dated encounters with no stated charge (EMS 01-09, PCP 01-16, PT visits, pain management 05-18 and 06-12) — without inventing amounts.'",
   "acceptance_test": "Checklist item present; calibration example shows the 'no charge stated' list."},
  {"severity": "minor",
   "title": "No check against an invented referral chain into pain management",
   "evidence": "personas/claims-adjuster.md:10 lists 'treatment that escalates after an attorney is involved' in context but no checklist item covers it. Record 7 (spec/SPEC.md:63) has no referral source, and no earlier record refers to pain management. personas/litigation-lead.md:36 item 18 covers only the reverse case (referral mentioned but no record).",
   "why_it_matters": "After a 73-day gap and 'new onset' symptoms, the adjuster's next question is who sent him to pain management, because attorney-directed care gets discounted. A summarizer is likely to fill that in ('referred to pain management for persistent symptoms'). That would be an invented fact in exactly the spot the adversary is probing.",
   "fix": "Adjuster item: 'No referral, referring provider, or reason for a visit appears unless stated in that record (e.g., record 7 states no referral source).'",
   "acceptance_test": "Checklist item present in claims-adjuster.md; a golden-set negative for 'referred' on record 7 is suggested."},
  {"severity": "minor",
   "title": "Dossiers do not bar legal-conclusion labels in tool output; one example invites tool-predicted arguments",
   "evidence": "personas/litigation-lead.md:35 item 17 example \"('adjuster may argue...')\"; claims-adjuster.md:23 \"I call this failure to mitigate / non-compliance\" and :44 vocabulary (failure to mitigate, intervening/superseding cause, aggravation). No item in any of the five says the tool's flag text must not use those labels. Only legal-nurse.md:27 (aggravation) and claims-adjuster.md:74 (Limits) touch it. docs/LLM_VS_CODE.md:43 already makes the 'Why?' sentence a fixed template.",
   "why_it_matters": "Labeling my own client's missed PT 'failure to mitigate' in our work product is a legal conclusion drafted by a model. That is the judgment I am supposed to make, and it is the adversary's framing. The reviewers should catch it if a prompt or template drifts that way.",
   "fix": "Add to litigation-lead checklist: 'Flag text uses the spec's four categories plus the verbatim excerpt and a fixed-template reason; no legal-conclusion labels (failure to mitigate, aggravation, intervening cause, non-compliant) and no model-written predictions of adjuster arguments.' Change the item 17 example to a template string.",
   "acceptance_test": "Checklist item present; item 17 example is a fixed template, not model prose."},
  {"severity": "minor",
   "title": "Cross-dossier conflict on marking edits in the export",
   "evidence": "personas/claims-adjuster.md:52 \"edit an entry to add 'severe' and confirm the export marks it as edited (or the audit shows it)\" vs personas/litigation-lead.md:28 item 10 \"no AI disclaimers, UI labels, or internal state names\" and personas/paralegal.md:39 item 20 \"no UI labels\".",
   "why_it_matters": "An 'edited' marker in a demand letter tells the adjuster our staff rewrote a medical summary. Reviewers working from these prompts will file contradictory findings, and the worker will be pulled both ways.",
   "fix": "Adjuster step 6: \"... confirm the audit trail records the edit and the original; the export itself carries no edit markers.\"",
   "acceptance_test": "No dossier asks for edit markers in the export."},
  {"severity": "minor",
   "title": "Privacy dossier asserts ch. 181 applies to the firm but omits §181.154 (electronic disclosure authorization)",
   "evidence": "personas/privacy-compliance.md:35 item 16 and :67 cite ch. 181 for 'covered entity ... training; re-identification barred'. Tex. Health & Safety Code §181.154(b) (fetched): \"a covered entity may not electronically disclose an individual's protected health information to any person without a separate authorization from the individual ... for each disclosure\" (exceptions in (c)).",
   "why_it_matters": "If ch. 181 reaches the firm, as the dossier says, then electronically sending client records to an outside LLM vendor is the Texas question a Part 2 rollout has to answer. Whether §181.154 actually applies, and whether the (c)(2) exception covers it, is an interpretive call that is partly outside my lens. The dossier should at least make the reviewer ask.",
   "fix": "Add to the privacy checklist: 'Part 2 rollout addresses Tex. H&S §181.154 (notice; authorization for electronic disclosure of PHI to a vendor) or states why it does not apply.' Add the section to sources.",
   "acceptance_test": "privacy-compliance.md cites §181.154 with a one-line takeaway."},
  {"severity": "minor",
   "title": "Haygood paraphrased categorically as 'billed totals overstate'",
   "evidence": "personas/claims-adjuster.md:65 \"recovery limited to amounts paid or incurred; billed totals overstate.\" Haygood (txcourts.gov opinion, 09-0377, July 1, 2011): \"limits a claimant's recovery of medical expenses to those which have been or must be paid by or for the claimant\".",
   "why_it_matters": "Billed charges can equal the incurred amount when the claimant still owes the full bill, as with unpaid or letter-of-protection treatment. That is why K&L Auto Crushers is a fight over reasonableness. The labeling rule in the checklists is right. The overstated takeaway would lead a reviewer to demand that the tool caveat or discount billed amounts, which is a legal judgment.",
   "fix": "\"Haygood: recovery limited to amounts that have been or must be paid; only those are admissible at trial. Billed charges may exceed recoverable amounts where adjusted/paid amounts are lower, so the tool labels them 'billed' and does not characterize recoverability.\"",
   "acceptance_test": "No dossier states that billed totals categorically overstate damages."},
  {"severity": "nit",
   "title": "ABA 512 and Texas statutes cited via secondary or non-resolving URLs when primary text is reachable",
   "evidence": "personas/litigation-lead.md:63 and privacy-compliance.md:75 \"ABA PDFs block fetch\": primary 512 PDF fetched 200 via Wayback (evidence row 7). FindLaw Haygood 403; statutes.capitol.texas.gov /Docs/.../htm links return the site shell (evidence rows 2, 3, 5).",
   "why_it_matters": "Reviewers compiled from these dossiers will try to re-verify. Primary citations they can open carry more weight with lawyers than vendor summaries.",
   "fix": "Cite the Wayback ABA 512 PDF; cite Haygood as 356 S.W.3d 390 (Tex. 2011) with the txcourts.gov docket link; cite statutes by section with a resolving mirror.",
   "acceptance_test": "Each legal source URL returns the cited text on fetch."}
 ],
 "whats_right": [
  "Litigation-lead items 3, 6, 7 encode the Appendix C truths exactly: conflicting accident dates surfaced not reconciled, total labeled billed charges, no PT total from the $185 rate.",
  "§41.0105/Haygood, §18.001, ABA 512 boilerplate-consent, JLG Trucking and Stowers framing are accurate and current (SB 30, 2025, died in conference).",
  "Adjuster Limits ('surface facts, not conclusions') and legal-nurse items 9-10 keep the tool from deciding aggravation or linking new-onset symptoms to C5-C6."
 ],
 "questions_for_chris": [
  "Should the litigation-lead persona treat a Part 2 plan that uses de-identified real work product under firm controls as acceptable (my reading of spec area 4 and Op. 705), or do you want the persona to require synthetic-only even for the post-launch test set?"
 ]}
```
